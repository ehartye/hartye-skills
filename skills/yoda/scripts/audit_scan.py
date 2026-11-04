#!/usr/bin/env python3
"""Read-only, dependency-free mechanical checks. See --help for scope."""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

TEXT = {'.md', '.txt', '.json', '.yaml', '.yml', '.py', '.js', '.mjs', '.ts', '.sh', '.ps1'}
SKIP = {'.git', 'node_modules', '.venv', '__pycache__'}


def prose(text, inline=True):
    """Mask fenced/inline code, preserving line positions for link diagnostics."""
    lines = text.splitlines(keepends=True)
    fence = None
    for i, line in enumerate(lines):
        match = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
                fence = None
            lines[i] = '\n' if line.endswith('\n') else ''
        elif match:
            fence = match[1]
            lines[i] = '\n' if line.endswith('\n') else ''
        elif inline:
            lines[i] = re.sub(r'(`+)([^`]*?)\1', lambda m: ' ' * len(m[0]), line)
    return ''.join(lines)


def anchors(text):
    result, used = set(), set()
    for line in prose(text, inline=False).splitlines():
        match = re.match(r'^ {0,3}#{1,6}\s+(.+?)(?:\s+#+\s*)?$', line)
        if not match:
            continue
        title = re.sub(r'<[^>]*>', '', match[1]).lower()
        slug = ''.join(c for c in title if c in '-_ ' or unicodedata.category(c)[0] in 'LNM')
        slug = slug.replace(' ', '-')
        candidate, suffix = slug, 0
        while candidate in used:
            suffix += 1
            candidate = f'{slug}-{suffix}'
        used.add(candidate)
        result.add(candidate)
    result.update(re.findall(r'<(?:a|[a-z][a-z0-9]*)\b[^>]*\b(?:id|name)=["\']([^"\']+)["\']', prose(text), re.I))
    return result


def scan(root, checks):
    root = Path(root).absolute()
    if root.is_symlink():
        raise ValueError('scan root must not be a symlink')
    if not root.exists():
        raise ValueError('scan root does not exist')
    root = root.resolve(strict=True)
    boundary = (root if root.is_dir() else root.parent).resolve(strict=True)
    findings = []
    visited = set()

    def emit(path, text, offset, kind, detail, severity='warning'):
        findings.append(dict(path=str(path.relative_to(boundary)), line=text.count('\n', 0, offset) + 1,
                             check=kind, severity=severity, detail=detail))

    def files(path):
        if path.is_symlink():
            emit(path, '', 0, 'scope', 'symlink skipped; not inspected')
        elif path.is_dir():
            resolved = path.resolve()
            if not resolved.is_relative_to(boundary) or resolved in visited:
                emit(path, '', 0, 'scope', 'directory alias escapes root or repeats a directory; not inspected')
                return
            visited.add(resolved)
            for child in sorted(path.iterdir()):
                if child.name not in SKIP:
                    yield from files(child)
        elif path.is_file() and (path == root or path.suffix.lower() in TEXT):
            yield path

    for path in files(root):
        try:
            text = path.read_bytes().decode('utf-8', errors='strict')
        except (OSError, UnicodeError) as exc:
            emit(path, '', 0, 'read', str(exc))
            continue
        if 'unicode' in checks:
            for offset, char in enumerate(text):
                cp, category = ord(char), unicodedata.category(char)
                if (category in {'Cf', 'Cc', 'Cs', 'Zl', 'Zp'} and char not in '\n\r\t') or (
                        category == 'Zs' and cp != 32) or 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF:
                    emit(path, text, offset, 'unicode', f'U+{cp:04X} {unicodedata.name(char, "UNNAMED")} ({category}); review context')
        if 'placeholders' in checks and path.name == 'SKILL.md':
            front = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
            hint_match = front and re.search(r'^argument-hint:[ \t]*([^\r\n]*)', front[1], re.M)
            hint_value = hint_match[1].strip() if hint_match else ''
            hint = bool(hint_value and hint_value not in {'""', "''"} and hint_value[0] not in '#>|')
            for match in re.finditer(r'\$(?:[0-9]|ARGUMENTS(?:\[[0-9]+\])?(?![A-Za-z0-9_]))', text):
                declared = hint and match[0].startswith('$ARGUMENTS')
                emit(path, text, match.start(), 'placeholders', match[0] + (
                    ': declared argument-hint; intended candidate, confirm manually' if declared else ': substitution candidate; confirm intent'),
                     'info' if declared else 'warning')
        if 'links' not in checks or path.suffix.lower() != '.md':
            continue
        body = prose(text)
        # Inline destinations, including multiline labels, angle paths and balanced single-level parentheses.
        pattern = r'!?\[[^\]]*\]\(\s*(<[^>\n]+>|(?:[^\s()]|\([^()]*\))+)\s*(?:["\'][^\n]*?["\']\s*)?\)'
        targets = [(m.start(), m[1].strip('<>')) for m in re.finditer(pattern, body)]
        # Check reference definitions even if no use is present.
        targets += [(m.start(), m[1].strip('<>')) for m in re.finditer(
            r'^ {0,3}\[[^\]]+\]:\s*(<[^>\n]+>|\S+)', body, re.M)]
        for offset, target in targets:
            try:
                url = urlsplit(target)
                if url.scheme or url.netloc:
                    continue  # Never fetch remote links, including file: URLs.
                decoded = unquote(url.path, errors='strict')
                if '\\' in decoded or '\x00' in decoded or decoded.startswith('/'):
                    raise ValueError('absolute, backslash or NUL path is unsupported')
                destination = (path.parent / decoded).resolve() if decoded else path.resolve()
                if not destination.is_relative_to(boundary):
                    raise ValueError('target leaves scan root (including symlink escape)')
                if not destination.exists():
                    raise ValueError('target does not exist')
                if url.fragment:
                    if destination.suffix.lower() != '.md':
                        raise ValueError('anchor on non-Markdown target is not checked')
                    if unquote(url.fragment, errors='strict') not in anchors(destination.read_bytes().decode('utf-8')):
                        raise ValueError('anchor not found in supported headings or explicit HTML IDs')
            except (OSError, ValueError, UnicodeError) as exc:
                emit(path, body, offset, 'links', f'{target}: {exc}')
    return findings


def main():
    parser = argparse.ArgumentParser(description='Read-only UTF-8 audit, including untracked files. Python 3.10+. '
        'Directory scans include common text extensions; exclude .git, node_modules, .venv and __pycache__. '
        'No Git/base filter, network, writes, YAML validation, length checks or safety certification. '
        'Links: inline/reference definitions, ATX headings and HTML IDs; not a complete Markdown renderer. '
        'Unsupported reference uses, setext headings and renderer-specific slugs need manual review.')
    parser.add_argument('root', help='file or directory; relative links must stay inside this directory (file: its parent)')
    parser.add_argument('--check', choices=['all', 'unicode', 'placeholders', 'links'], default='all')
    args = parser.parse_args()
    try:
        rows = scan(args.root, {'unicode', 'placeholders', 'links'} if args.check == 'all' else {args.check})
        for row in rows:
            print(json.dumps(row, ensure_ascii=True))
        return int(any(row['severity'] == 'warning' for row in rows))
    except (OSError, ValueError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / 'skills/yoda/scripts/audit_scan.py'
spec = importlib.util.spec_from_file_location('audit_scan', SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, body):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding='utf-8')
        return path

    def scan(self, mode='all'):
        return audit.scan(self.root, {mode} if mode != 'all' else {'unicode', 'placeholders', 'links'})

    def test_clean_untracked_unicode_paths_and_multiline_links(self):
        self.write('SKILL.md', '# Hello\n[wrapped\nlabel](<réf space.md#café>)\n')
        self.write('réf space.md', '# Café\nOrdinary 日本語 and U0001f642\n')
        self.assertEqual(self.scan(), [])

    def test_unicode_ranges_and_normal_whitespace(self):
        points = [0xE0061, 0x200B, 0x202E, 0xFEFF, 0xFE0F, 0xE0100, 0xA0, 0x2028, 1]
        self.write('untracked.txt', '\t\r\n' + ''.join(map(chr, points)))
        rows = self.scan('unicode')
        self.assertEqual(len(rows), len(points))
        for point, row in zip(points, rows):
            self.assertIn(f'U+{point:04X}', row['detail'])

    def test_placeholder_intent_is_not_blanket_exemption(self):
        self.write('SKILL.md', '---\nargument-hint: task\n---\n$ARGUMENTS $ARGUMENTS[1] $1 $10 $ARGUMENTS_EXTRA\n```sh\n$2\n```')
        rows = self.scan('placeholders')
        self.assertEqual([r['severity'] for r in rows], ['info', 'info', 'warning', 'warning', 'warning'])
        self.write('script.py', '$1 $ARGUMENTS')
        self.assertEqual(self.scan('placeholders'), rows)

    def test_undeclared_placeholder(self):
        self.write('SKILL.md', '$ARGUMENTS')
        self.assertEqual(self.scan('placeholders')[0]['severity'], 'warning')

    def test_empty_and_block_hints_do_not_exempt(self):
        for hint in ['', '|\n  task', '>\n  task', '""', "''", '# comment']:
            self.write('SKILL.md', f'---\nargument-hint: {hint}\nname: demo\n---\n$ARGUMENTS')
            self.assertEqual(self.scan('placeholders')[0]['severity'], 'warning', hint)

    def test_anchor_in_code_is_not_a_target(self):
        self.write('SKILL.md', '[x](#fake)\n```html\n<a id="fake"></a>\n```\n')
        self.assertEqual(len(self.scan('links')), 1)

    @unittest.skipUnless(os.name == 'nt', 'Windows junction fixture')
    def test_junction_escape_and_loop(self):
        with tempfile.TemporaryDirectory() as outside:
            Path(outside, 'bad.txt').write_text(chr(0x200B), encoding='utf-8')
            links = []
            try:
                for name, target in [('escape', outside), ('loop', str(self.root))]:
                    link = self.root / name
                    result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), target], capture_output=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    links.append(link)
                rows = self.scan()
                self.assertEqual([r['check'] for r in rows], ['scope', 'scope'])
            finally:
                for link in links:
                    os.rmdir(link)  # Remove only our junction, never its target.

    def test_aliased_ancestor(self):
        self.write('real/skills/SKILL.md', '$1')
        alias = self.root / 'alias'
        if os.name == 'nt':
            result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(alias), str(self.root / 'real')], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            alias.symlink_to(self.root / 'real', target_is_directory=True)
        try:
            rows = audit.scan(alias / 'skills', {'placeholders'})
            self.assertEqual(rows[0]['path'], 'SKILL.md')
        finally:
            os.rmdir(alias) if os.name == 'nt' else alias.unlink()

    def test_missing_links_and_anchor_and_reference_definition(self):
        self.write('SKILL.md', '[x](gone.md)\n[x](ref.md#absent)\n[r]: absent.md\n')
        self.write('ref.md', '# Present')
        self.assertEqual(len(self.scan('links')), 3)

    def test_fences_inline_examples_and_external_links(self):
        self.write('SKILL.md', '```md\n[x](gone.md)\n```\n`[x](gone.md)`\n[x](https://example.invalid)\n[x](mailto:a@b)\n')
        self.assertEqual(self.scan('links'), [])

    def test_anchors_duplicates_html_and_parentheses(self):
        self.write('SKILL.md', '[x](ref(1).md#a-1)\n[x](ref(1).md#custom)')
        self.write('ref(1).md', '# A\n# A\n<a id="custom"></a>')
        self.assertEqual(self.scan('links'), [])

    def test_paths_escape_percent_encoded_and_absolute(self):
        self.write('SKILL.md', '[x](%2e%2e/outside.md)\n[x](/absolute.md)\n[x](bad%00.md)')
        self.assertEqual(len(self.scan('links')), 3)

    def test_invalid_utf8_and_excluded_dependency(self):
        self.write('node_modules/ignored.md', '[x](missing)')
        (self.root / 'broken.txt').write_bytes(bytes([255]))
        self.assertEqual([r['check'] for r in self.scan()], ['read'])

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            Path(outside, 'sentinel.md').write_text('# Secret', encoding='utf-8')
            try:
                (self.root / 'escape').symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest('symlink creation unavailable')
            self.write('SKILL.md', '[x](escape/sentinel.md#secret)')
            self.assertEqual({r['check'] for r in self.scan()}, {'scope', 'links'})

    def test_cli_exit_and_no_mutation(self):
        path = self.write('SKILL.md', '# Clean\n')
        original = path.read_bytes()
        def run(root):
            return subprocess.run([sys.executable, str(SCRIPT), str(root)], capture_output=True, text=True)
        result = run(self.root)
        self.assertEqual((result.returncode, result.stdout), (0, ''))
        self.assertEqual(path.read_bytes(), original)
        self.write('new.md', '[x](missing)')
        self.assertEqual(run(self.root).returncode, 1)
        self.assertEqual(run(self.root / 'absent').returncode, 2)


if __name__ == '__main__':
    unittest.main()

"""Reference implementation used only to validate the hidden tests."""
import datetime as _dt
import decimal as _decimal
import math as _math

_INJECT = ("=", "+", "-", "@", "\t", "\r")


def _quote(s):
    if any(c in s for c in ',"\r\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def _fmt(v, key, idx):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if not _math.isfinite(v):
            raise ValueError(f"non-finite float in column {key!r} at exported row {idx}")
        return repr(v)
    if isinstance(v, _decimal.Decimal):
        return str(v)
    if isinstance(v, _dt.datetime):
        if v.tzinfo is None or v.utcoffset() is None:
            raise ValueError(f"naive datetime in column {key!r}")
        u = v.astimezone(_dt.timezone.utc).replace(microsecond=0)
        return u.strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(v, _dt.date):
        return v.isoformat()
    if isinstance(v, str):
        return "'" + v if v.startswith(_INJECT) else v
    raise TypeError(f"unsupported type {type(v).__name__} in column {key!r}")


def _keep(row, filters):
    for k, cond in (filters or {}).items():
        v = row.get(k)
        if v is None:
            return False
        if isinstance(cond, tuple) and len(cond) == 3 and cond[0] == "range":
            lo, hi = cond[1], cond[2]
            if lo is not None and not v >= lo:
                return False
            if hi is not None and not v < hi:
                return False
        elif v != cond:
            return False
    return True


def export(rows, columns, *, filters=None, bom=False, stream=None):
    """Export rows as RFC 4180 CSV."""
    cols = [(c, c) if isinstance(c, str) else (c[0], c[1]) for c in columns]
    parts = []
    write = stream.write if stream is not None else parts.append
    write(("\ufeff" if bom else "") + ",".join(_quote(h) for _, h in cols) + "\r\n")
    idx = 0
    for row in rows:
        if not _keep(row, filters):
            continue
        fields = [_quote(_fmt(row.get(k), k, idx)) for k, _ in cols]
        write(('""' if fields == [""] else ",".join(fields)) + "\r\n")
        idx += 1
    return None if stream is not None else "".join(parts)

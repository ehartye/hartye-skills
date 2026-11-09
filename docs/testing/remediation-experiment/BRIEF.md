# Brief: `csvexport` module

Build a single module, `csvexport.py`, at the repository root. Use the Python 3.12 standard library
only (no third-party packages). Tests use `unittest` and live in `tests/`.

## Function

```python
def export(rows, columns, *, filters=None, bom=False, stream=None):
    ...
```

### Inputs

- `rows` is an iterable of `dict`s. It may be a one-shot generator of any length. The function must
  process it lazily, one row at a time, and must never hold all rows or all output in memory at
  once when `stream` is given.
- `columns` is a list. Each item is either a string key (the header is the key itself) or a
  `(key, header)` tuple. Output columns follow this order exactly.
- `filters` is an optional `dict` mapping a key to a condition. Every condition must hold for a row
  to be exported. A condition is either:
  - a plain value, meaning the row's value must equal it; or
  - a tuple `("range", lo, hi)`, meaning `lo <= value < hi`, where `lo` or `hi` may be `None` for
    an unbounded side.

  A row that lacks a filtered key, or has `None` for it, is excluded.
- `bom`: when `True`, the output begins with the UTF-8 byte-order mark character `"\ufeff"`.
- `stream`: an optional writable text file-like object. When given, write the output to it
  incrementally and return `None`. Otherwise, return the whole output as a `str`.

### Output format

- RFC 4180 CSV: comma separator, `\r\n` after every record including the last, fields quoted with
  `"` when they contain a comma, a double quote, `\r` or `\n`, and embedded double quotes doubled.
- A header row is always written first, even when no rows are exported.
- A missing key or a `None` value produces an empty field.

### Value formatting

- `str`: as is, except for formula-injection protection (below).
- `bool`: `true` or `false`. Note that `bool` is a subclass of `int`.
- `int`: decimal digits.
- `float`: `repr(value)`. A NaN or infinite float raises `ValueError`. The message must name the
  column key and the 0-based index of the row among the *exported* rows.
- `decimal.Decimal`: `str(value)`.
- `datetime.date` (but not `datetime.datetime`): ISO `YYYY-MM-DD`.
- `datetime.datetime`: must be timezone-aware. Convert it to UTC and write
  `YYYY-MM-DDTHH:MM:SSZ`, dropping microseconds. A naive datetime raises `ValueError`, whose
  message names the column key.
- Any other type raises `TypeError`, whose message names the column key.

### Formula-injection protection

A data cell whose value is a `str` starting with `=`, `+`, `-`, `@`, a tab or `\r` is prefixed with a
single quote (`'`) before CSV quoting is applied. Header cells and non-string values are never
prefixed, so the integer `-5` is written as `-5`.

## Definition of done

- Tests in `tests/` cover every rule above. Write them first and see them fail.
- `python -m unittest discover -s tests -t .` passes.
- The module has docstrings, and no public names other than `export`.

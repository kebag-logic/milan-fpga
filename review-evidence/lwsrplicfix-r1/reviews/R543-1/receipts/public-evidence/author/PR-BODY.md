Closes [#13](https://github.com/kebag-logic/lwSRP/issues/13).

- [`LICENSE`](https://github.com/kebag-logic/lwSRP/blob/licence-canonical/LICENSE) drops its first two lines: the SPDX line and a blank line.
- The file is now byte-identical to the canonical [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) text (`cmp` returns 0).
- Every other file keeps its SPDX header.

## Validation

| Check | Result |
|---|---|
| `cmp LICENSE <canonical text>` | identical |
| [`doc/tools/check_links.py`](https://github.com/kebag-logic/lwSRP/blob/licence-canonical/doc/tools/check_links.py) | rc 0; 354 local links, 20 external, 0 failures |

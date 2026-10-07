Closes [#13](https://github.com/kebag-logic/lwSRP/issues/13).

- [`LICENSE`](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/LICENSE) drops its first two lines: the SPDX line and a blank line.
- The file is now byte-identical to the canonical [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) text (`cmp` returns 0).
- Every other file keeps its SPDX header.

## Validation at `f800a2b`

| Check | Result |
|---|---|
| `cmp LICENSE <canonical text>` | identical |
| [`doc/tools/check_links.py`](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/check_links.py) | rc 0; 354 local links, 20 external, 0 failures |
| `python3 doc/tools/check_sentences.py` | rc 0; 975 sentences, 0 over the limit |
| `python3 doc/tools/check_references.py` | rc 0; 0 unlinked references |
| `python3 doc/tools/check_references.py --self-test` | rc 0; 79 cases, 0 failures |
| CMake configure and build (Debug) | rc 0, rc 0 |
| `ctest --output-on-failure` | rc 0; 1/1 tests; the unit runner completes 19,885 passes |
| `behave` | rc 0; 1 feature, 3 scenarios, 10 steps passed |
| `python3 doc/tools/render_mermaid.py --output <scratch>` | rc 0; 27 graphs, 0 failures |
| `behave --dry-run` | rc 0; 1 feature, 3 scenarios, 10 steps matched (untested in dry-run) |


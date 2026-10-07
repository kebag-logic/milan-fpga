<!-- SPDX-License-Identifier: Apache-2.0 -->
Closes [#8](https://github.com/kebag-logic/lwSRP/issues/8).

## What changes

- [`LICENSE`](https://github.com/kebag-logic/lwSRP/blob/apache-2.0/LICENSE) holds the full [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) text.
- [`NOTICE`](https://github.com/kebag-logic/lwSRP/blob/apache-2.0/NOTICE) names kebag-logic as the copyright holder.
- Every tracked file except `LICENSE` and `NOTICE` starts with `SPDX-License-Identifier: Apache-2.0`, in its own comment syntax ([SPDX](https://spdx.dev/)).
- The licence commit was made on `19f5796`. The second commit merges `main`, which brings in the test-harness fix ([#3](https://github.com/kebag-logic/lwSRP/pull/3)) and the documentation ([#5](https://github.com/kebag-logic/lwSRP/pull/5)).
  - `README.md`: `main`'s version is kept. Its licence section already has the agreed text.
  - `tests/unit/placeholder.c`: `main` deleted it, so it stays deleted.

## Provenance

- Every commit before this one is by the owner, under the company and personal accounts.
- No file is third-party or carries another licence.

## Validation at the merge commit

| Check | Result |
|---|---|
| SPDX header on every tracked file except `LICENSE` and `NOTICE` | all present |
| CMake configure and build | rc 0 |
| `ctest` | rc 0; `mrp_pdu_suite` 1690 passes |
| `behave` | rc 0; 3 scenarios, 10 steps passed |
| [`doc/tools/check_links.py`](https://github.com/kebag-logic/lwSRP/blob/apache-2.0/doc/tools/check_links.py) | 290 local links resolve, including `LICENSE` and `NOTICE` |
| External links | 7 anonymous failures, all expected: 6 are this repository's own URLs, private until release; iso.org answers HTTP 403 to automated clients |

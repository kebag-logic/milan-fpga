# A192 handoff: issue #523 / PR #526, ci_scope selftest arm

- Branch: `523-isolate-mutation-cancellation` (local only, not pushed)
- Start head: `6674c278a8db5f0886d036dceff02d33b7ca6a37`
- New head: `26353960ae2763cc09741d0f7bcc720621bd5148`
- New tree: `b250c4b9445f6d6645d56941fbe388257f1d60e3`
- Commit: `Use the lifecycle test, not the suite README, as the unread suite-directory file`
- Changed: `tb/verilator/gptp_shadow/test_mutant_lifecycle.py` only (+7 -3)
- Decision: https://github.com/kebag-logic/milan-fpga/issues/523#issuecomment-5791137584 (option b)

## Cause

`ci_scope.py` resolves a literal ending in `/<page>` to that documentation page.
`"tb/verilator/gptp_shadow/README.md"` in `UNRELATED` therefore matched the
top-level `README.md`, which no gate reads. The suite README itself is already
relevant because everything under `tb/` is. Option (a) would have been a false
`GATE_READ_DOCS` entry, and it would also turn the `["README.md", "AGENTS.md"]`
docs-only case red.

## Fix

`UNRELATED[0]` (the staged, rewritten suite-directory file) is now
`tb/verilator/gptp_shadow/test_mutant_lifecycle.py`. That file is tracked and
is not documentation. The campaign's `make -s run` never reads it (it is not in
`print-inputs`). The F3 acceptance arm and the private-copy check are unchanged.
`ci_scope.py` is not touched.

## Gate exits at 26353960

| Command | Exit | Result |
|---|---|---|
| `python3 scripts/ci_scope.py --selftest` | 0 | `selftest: PASS` (was 1 at 6674c278) |
| `python3 scripts/ci_scope.py --check` | n/a | no such option |
| `python3 tb/verilator/gptp_shadow/test_mutant_lifecycle.py` | 0 | `mutant lifecycle: PASS`; `accept-unrelated` exit 0, controls 9 |
| `python3 scripts/check_py_idiom.py` | 0 | |
| `python3 scripts/docs_check.py` | 0 | 0 findings |
| `python3 scripts/check_em_dash.py --base 776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d` | 0 | 0 findings, arms 57/57 |
| `git diff --check HEAD~1 HEAD` | 0 | |

Not done: no push, no PR edit, no merge, no full bank.

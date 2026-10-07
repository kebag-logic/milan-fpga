In the separate dependency clone, local branch `f4-applicant-notes-r5` is at `ced667d8ee35929ab5f9e77a1c5396e173a693d8`. It merges main with `--no-ff` into rewritten notes head `72209a53a241cd5de4786d3e1b3aefcbdf5fa5d9`. Its parents are that notes head and `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`. Subject: `Merge main into Applicant note regressions`. README count and reversal-name conflicts were resolved by retaining both changes. Production `src/` is byte-identical to public main. This test merge is not the parent gitlink; the public main pin is already fetchable.

| Dependency file:line | Difference from public main |
|---|---|
--
| `tests/check_reversals.py:76` | Carry pending-condition reversal; lines 185-188 require exact note tests to fail. |

Both profiles pass 87 unit tests: OFF has 19901 assertions, ON has 19889. Each passes three behavior scenarios with ten steps, all 94 reversals and restored positive suites. The manager publishes this local branch before its dependency PR. No dependency branch was pushed.

## Tests and planted defects

--
| Dependency `tests/check_reversals.py`, OFF and ON | 94/94 caught each; 87.781 / 87.870 s | 0 |
| Dependency sentence, reference, reference-self-test and link gates | 975 sentences, 79 controls, 354 local and 20 public external links | 0 |
| `docs-00` through `docs-75` | All 76 assigned documentation-bank commands, including SDK provenance and 25 SDK controls | 0 |
| `docs-selftest`, `docs-wire`, `em-dash-final`, `docs-final`, `source-diff`, `ci-scope` | Final documentation checks, 77 wire checks, whitespace and CI scope controls | 0 |

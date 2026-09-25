[A319] REVIEW READY

Commit: `e122f3302cf8a8e89de960233a8638b9dd1387dc`
Branch: `400-403-declaration-truth` (local; not pushed, as assigned).

Assignment items 1-3 are addressed:

- The saved-state co-simulation derives its constants from the generated overlay and SRP table through the shared boot-policy function. The repository-wide caller census found no stale caller.
- Default `pp_shadow` and `csr` targets now generate and run committed distinct-VID, CRF-on and nonzero-reset-bit fixtures. Headers come from the builder. The two harness comments now describe these committed recipes.
- The cited reset, lwSRP/AAF VID, MAAP requirement and allocation, RX-filter presence, presentation-row and declaration-count contracts are corrected. The declaration table contains 71 rows.

The exact reviewer mutants were applied to this final head and detected by the default targets, then restored byte-for-byte:

| Receipt | Target | Exit | Observed failure |
|---|---|---:|---|
| 41 | `make -C tb/verilator/pp_shadow` | 2 | Three VID checks: 2 instead of 73 |
| 43 | `make -C tb/verilator/pp_shadow` | 2 | Three VID checks: 2 instead of 73 |
| 35 | `make -C tb/verilator/csr` | 2 | Both admission-reset outputs: 0 instead of 1 |

Restored default targets pass. Clean default wall clocks:

| Suite | Before, seconds | Final head, seconds | Unchanged budget, seconds |
|---|---:|---:|---:|
| `pp_shadow` | 18.502 | 52.735 | 1800 |
| `csr` | 30.480 | 35.146 | 1800 |

Validation: all required positive gates returned 0. Both complete builder modes, declaration tests, firmware self-test, all 48 manager-bank entries, both documentation modes, source/style gates, whitespace checks and all 344 behavior scenarios passed. Quick co-simulation passed 315 checks; the full target passed 465 checks and killed all 39 named mutants. The default datapath recipe passed all 33 recorded commands. The full `scripts/run_all_suites.sh` sweep covered all 55 suites exactly once in five chunks; chunks 0/5 through 4/5 each returned 0, with no failed or timed-out suite.

The repository OOC recipe reports zero delta in all eight resource counters for `KL_pp_shadow`, `milan_datapath` and `milan_csr` against `864b36f5e9450ef64f75ca3f0d68c44330e447d7` at the default shape. All temporary measurement inputs were restored.

The local `400-403-a319` evidence packet contains `HANDOFF.md` with the file:line change list, every gate/chunk exit, timings, mutant receipts and area comparison, plus `PR-BODY.md` containing the full current PR body with the Round 3 update. Both commits have one-line subjects and no trailers. The checkout is clean.

Limits: the historical placed-utilization calibration report and field-campaign generator remain unavailable. Compiler-dependent arms in the compiler-absent mode are covered separately by the pinned-SDK run. Manager bank entry 47 preserves the supplied helper logic, relocating only its receipt destination into this packet. An initial warning-flag style failure was fixed and rechecked; its receipt remains recorded. S1 remains outside scope under #495. Publication, hosted validation and independent re-review remain with the manager; no push, PR edit, merge, hardware operation or donor edit was performed.

[A393] Round 3 author handoff

Status: assigned implementation and local validation complete; independent review pending.
Head: `3b5603e3d16a164c35329efeb633800fe4fe9f95`. Branch: `395-timing-grade`.
Starting head: `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`.
Base: `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Physical worktree: `$LANES/395-timing-grade`.
Relates to #395. Items 3 and 4 remain open.
Executor: [A393]. Independent reviewers: [R372] and [R373].

Assignment: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860820812
Owner grade decision: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5789765635
Margin decision: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860418611
Margin correction: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860783553

## Per-item changes and reviewer responses

| Item | Change and file:line | How it answers the review |
|---|---|---|
| Required blocker | `docs/findings/COMMERCIAL_TIMING_395.md:117` | R372-2 F1 and R373-2 R2-F1: uses Ethernet-to-system wording while retaining unbounded false paths in both directions. The unchanged bare-metal check scans every tracked first-party file, including every new PR line, and returns zero findings. Its 700-arm self-test passes. |
| S1 | `docs/findings/COMMERCIAL_TIMING_395.md:119` | R372-2 S1: names shipping XDC 566's MultiReg exception and 568's AsyncResetSynchronizer exception. The table distinguishes 13/12 data D endpoints from 4/8 reset PRE endpoints, names FDPE_14/PRE and FDPE_18/PRE, and leaves the reset-assertion decision explicitly with #607. The fresh probe reproduces the review receipt byte for byte. |
| S2 | `sw/builder/test_timing_grade.py:190` | R372-2 S2 and R373-2 S-F: the standalone entry now invokes the PLL test alongside its platform test when supplied the platform interpreter. The real entry passes unchanged and fails at the changed-part assertion when the derived speed grade is replaced in memory by the old literal. |
| S3 | `sw/litex/milan_soc.py:207`; `docs/integration/BUILDING.md:33,49,72,540,626`; `docs/testing/RUNNING_TESTS.md:155`; `docs/litex/LITEX_SOC.md:161`; `docs/findings/COMMERCIAL_TIMING_395.md:65` | R372-2 S3 and R373-2 S-E: the PLL comment describes derivation from the declared part. The release wording consistently requires WNS >= +0.03 ns and WHS >= 0 at every corner, and states that enforcement is not automatic and sweep seed selection is manual. The margin correction is linked. |
| S4 | `docs/findings/COMMERCIAL_TIMING_395.md:143` | R372-2 S4: direct links locate the published crossing script and results under `fa9b0b5373abcb31b2ca6b20c3616b069d8672c4:review-evidence/395-r1/author-r2`. Both targets were verified through the repository API; metadata is in `public-evidence-locators.json`. |
| Retained S4 | `docs/findings/README.md:11` | R372-1 S4, retained in round 2: the current findings index now links the timing record and states its scope and remaining limits. |

The executable reporting chain, platform declaration and bare-metal gate remain
byte-identical to round 2. The SoC executable syntax tree is unchanged: its only
edit is the PLL comment. `unchanged-contracts.json` records these comparisons.
No firmware, RTL, constraint or timing fix is included.

## Gates at the committed head

All 21 accepted commands returned rc 0 at `3b5603e3d16a164c35329efeb633800fe4fe9f95`.
Every gate ran in the foreground with an explicit timeout and no pipeline.
`gate-results.json` records exact argv, cwd, head, UTC start, duration, exit code,
and each full log's size and SHA-256. `run_gates.py` retains the sequence.
The full logs are under `$VALIDATION_STORAGE/395-a393-work/gates-3b5603e3d`;
small copies are included below. Concurrency is capped at sixteen CPUs;
the corner report uses sixteen threads and the crossing probe uses eight.

| Gate | Exit | Seconds | Receipt |
|---|---:|---:|---|
| `baremetal-check` | 0 | 14.89 | `gates/baremetal-check.log` |
| `baremetal-selftest` | 0 | 6.62 | `gates/baremetal-selftest.log` |
| `standalone-pll` | 0 | 0.93 | `gates/standalone-pll.log` |
| `ci-scope-selftest` | 0 | 2.07 | `gates/ci-scope-selftest.log` |
| `docs` | 0 | 4.31 | `gates/docs.log` |
| `doc-paths` | 0 | 0.08 | `gates/doc-paths.log` |
| `toc` | 0 | 2.56 | `gates/toc.log` |
| `em-dash` | 0 | 3.18 | `gates/em-dash.log` |
| `feature-status` | 0 | 0.67 | `gates/feature-status.log` |
| `doc-style` | 0 | 0.05 | `gates/doc-style.log` |
| `doc-style-selftest` | 0 | 0.04 | `gates/doc-style-selftest.log` |
| `solution-docs` | 0 | 0.11 | `gates/solution-docs.log` |
| `python-idiom` | 0 | 3.37 | `gates/python-idiom.log` |
| `python-idiom-selftest` | 0 | 3.31 | `gates/python-idiom-selftest.log` |
| `diff-committed` | 0 | 0.02 | `gates/diff-committed.log` |
| `diff-worktree` | 0 | 0.02 | `gates/diff-worktree.log` |
| `timing-script` | 0 | 0.04 | `gates/timing-script.log` |
| `timing` | 0 | 59.27 | `gates/timing.log` |
| `crossings` | 0 | 55.47 | `gates/crossings.log` |
| `builder-present` | 0 | 767.4 | `gates/builder-present.log` |
| `builder-absent` | 0 | 601.01 | `gates/builder-absent.log` |

Compiler-present command:
`python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`.
Compiler-absent command: `python3 -B <packet>/run_builder_absent.py`.
That wrapper runs the full entry with `--require-elaboration`, hides exactly
the three RV32 compiler candidates, and asserts all three were probed.
Host compilers remain available. Both banks execute the timing-grade platform
and PLL arms and retain required elaboration.
`builder-present-summary.txt` and `builder-absent-summary.txt` list all skips.
Both record gate 11's unavailable historical Arty calibration report.
The absent mode additionally records its expected compiler-dependent skips.
These skips provide no validation of the omitted arms.

The bare-metal commands are
`python3 -B scripts/check_baremetal_only.py --check` and
`python3 -B scripts/check_baremetal_only.py --selftest`.
The unchanged check reports zero findings across 919 tracked first-party files.
The standalone PLL control returns 0; its deliberately wrong literal returns
1 at `test_pll_grade`, as required. The grading wrapper returns 0.

The first external mutation wrapper had a quoting error before loading the
mutated module. That non-acceptance attempt is retained separately in
`preliminary-gate-results.json` and `preliminary-standalone-pll.log`.
The corrected wrapper passed at the same repository head. Already successful
static checks were retained, and no repository change was needed for that repair.

## Fresh read-only timing evidence

The nominated shipping image remains `build_ax7101_eto_tdm8dev9e9954e9`.
The corner reporter returned 0 in 59.27 seconds; the endpoint-classification
probe returned 0 in 55.47 seconds. Exact commands and logs are in the gate table.

| Fixed model | Junction endpoints C | WNS ns | TNS ns | WHS ns | THS ns |
|---|---|---:|---:|---:|---:|
| Slow | 0 and 85 | 0.123 | 0.000 | 0.101 | 0.000 |
| Fast | 0 and 85 | 1.429 | 0.000 | 0.036 | 0.000 |

Every row meets WNS >= +0.03 ns and WHS >= 0 for the applied constraints.
The worst WNS surplus is 0.093 ns; minimum WHS is +0.036 ns.
These are two fixed timing models repeated at power metadata endpoints.
The fresh crossing receipt, `reports/crossings-r2-results.txt`, equals the
round-2 internal review's receipt byte for byte. All four directions meet the
diagnostic 8 ns bound at both models; minimum slack remains +2.560 ns.
Reset paths are included only after clearing the false paths in memory.
This diagnostic repairs no constraint and proves no CDC contract.

All seven shipping input size/hash pairs remain unchanged.
The checkpoint remains 115715651 bytes with SHA-256
`5f7a442b6a9327ad5d41aa0b10e18c84d9ca4c0aacd573d2ad25d444f5b2f5d1`.
See `shipping-inputs-before.json`, `shipping-inputs-after.json`,
`timing-metrics.json`, the five timing-summary excerpts and `report-artifacts.json`.
Reports over 200000 bytes remain under `$VALIDATION_STORAGE/395-a393-work/reports-3b5603e3d`,
with sizes and SHA-256 recorded instead of copies. No checkpoint or bitstream
was written. All files in this packet are at most 200000 bytes.

## Remaining boundaries and handoff

The retained ten Critical CDC diagnostics, two unsafe clock pairs, and 46 input
and 87 output ports without delay constraints remain unwaived. #607 owns the
constraint repair and the reset-assertion policy decision. Margin enforcement
is still manual. Items 3 and 4 still need physical temperature and oscillator
measurements. No hardware or bench access occurred.

The worktree is clean. Only this assigned worktree and branch were used.
No push, PR edit, merge, additional checkout or independent review was performed.
The manager owns publication, hosted acceptance and candidate-merge validation;
the reviewers own the new verdicts and any clean-lens ledger.
`PR-BODY.md` contains the Round 3 update and retains its original first line.
`REVIEW-READY.md` is the public handoff text; its posted URL is recorded separately.

Public review-ready notice: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5861083163

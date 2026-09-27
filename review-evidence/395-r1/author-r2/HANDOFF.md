# Round 2 author handoff

Status: implementation and assigned validation complete; ready for independent review. Executor [A390]; independent reviewers [R372] and [R373].
Final head: `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`.
Branch: `395-timing-grade`; starting head `66001a307ce5de57577e66d6e3a18b9f4020764b`.
Remote verified: `https://github.com/kebag-logic/milan-fpga.git`.
Scope: PR #605, issue #395 items 1, 2 and 5 only.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860419679
Margin decision: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860418611
WNS must be at least +0.03 ns at every corner; WHS must be nonnegative.
Items 3 and 4 remain open. Constraint fixes belong to #607.

## Changes and reviewer responses

| Item | Change and file:line | Reviewer response | Status |
|---|---|---|---|
| Item 2: constraint evidence | `docs/findings/COMMERCIAL_TIMING_395.md:77`, `docs/integration/BUILDING.md:554` | R372-1 F1; R373-1 F1: warning/source locations, clock-prefix cause, false-path precedence, #607 and retained census | Implemented |
| Items 1/2: builder planted faults | `sw/builder/test_timing_grade.py:73`, `sw/builder/test_timing_grade.py:118` | R372-1 F2: report-argument assertions and both refusal entry points | All five required faults fail through the full builder entry point |
| Item 2: acceptance margin | `docs/findings/COMMERCIAL_TIMING_395.md:61`; BUILDING section 5; RUNNING_TESTS section 5; LITEX_SOC section 7 | R372-1 F3: cite margin decision; WNS +0.123 exceeds +0.03 by 0.093 ns; minimum WHS +0.036 ns | Implemented |
| Item 1: derived PLL speed grade | `sw/litex/milan_soc.py:215`; `sw/builder/test_timing_grade.py:166`; `sw/builder/test_builder.py:27565` | R373-1 S2: derive speed grade from declared platform part; exercise real constructor with changed-part control | Implemented |

Item 5 documentation: `docs/integration/BUILDING.md:536` and `:554`,
`docs/testing/RUNNING_TESTS.md:168` and `:175`, and canonical
`docs/litex/LITEX_SOC.md:157` state the recorded thresholds and require the
implementation-log warning census alongside existing grade/corner reports.
These answer both reviewers' retention concerns and R372-1 F3's margin
concern. The grade remains commercial, 0 to 85 C junction.

The warning census retains original build log lines and all diagnostics.
Ten 12-4739, two 12-5201 and two 20-1307 warnings were emitted (14 total).
The fifteenth substring match is echoed IOB-check source at log line 6400.
The record names rejected XDC lines 583, 585, 587, 589, 591 and 595;
source lines 1520-1534 and 1550-1556; and the missing `milansoc_` prefix.
It explains both unsafe clock pairs and unbounded Ethernet/sys false paths,
including generic synchronizer false-path precedence. Issue #607 owns the fix.

## Ethernet crossing slack

The diagnostic clears constraints in memory, recreates the 200 MHz and
Ethernet primary clocks, and applies the intended 8 ns datapath-only bound.
It reproduces the internal review's reset-based method, extended to all four
directions. All inputs remain read-only. `crossings.tcl` is retained.

| Crossing | Slow maximum datapath ns | Slow worst slack ns | Fast maximum datapath ns | Fast worst slack ns |
|---|---:|---:|---:|---:|
| Ethernet to sys | 2.179 | 5.746 | 1.240 | 6.717 |
| Sys to Ethernet | 3.395 | 4.313 | 1.979 | 5.895 |
| Ethernet to milan | 5.373 | 2.560 | 3.092 | 4.823 |
| Milan to Ethernet | 3.652 | 4.056 | 1.996 | 5.878 |

The last direction includes fourteen endpoints after all false paths are
removed, with `FDPE_18/PRE` worst. The review's narrower measurement retained
generic false paths there and exposed six endpoints: Slow/Fast maximum
path delays 0.875/0.432 ns and slacks +7.066/+7.538 ns. The other three
rows reproduce the review's numbers exactly. Slack includes endpoint checks,
so it is not simply 8 ns minus datapath delay. This diagnostic proves no
CDC contract, repairs no constraint, and protects no future sweep seed.
Final-head rerun: rc 0 in 41.85 seconds, using eight threads.
Receipt: `reports/crossings-results.txt`; complete log: `reports/crossings.log`.
The original signoff report run used sixteen threads and returned rc 0
in 58.39 seconds. These runs read the same routed checkpoint.

## Shipping timing and margin decision

The [owner's margin decision](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860418611)
requires WNS >= +0.03 ns and WHS >= 0 at every declared corner.

| Model | Junction endpoints C | WNS ns | TNS ns | WHS ns | THS ns | Result |
|---|---|---:|---:|---:|---:|---|
| Slow | 0 and 85 | 0.123 | 0.000 | 0.101 | 0.000 | Applied constraints meet both thresholds |
| Fast | 0 and 85 | 1.429 | 0.000 | 0.036 | 0.000 | Applied constraints meet both thresholds |

These are two fixed speed models repeated at power metadata endpoints.
They are not four independent timing models. The WNS margin above the
required +0.03 ns is 0.093 ns at worst. Minimum WHS is +0.036 ns;
WPWS is +0.264 ns. Explicit negative-slack reports contain no paths.

The shipping build is `build_ax7101_eto_tdm8dev9e9954e9`, sourced from
`9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`. Its routed checkpoint is
115715651 bytes, SHA-256
`5f7a442b6a9327ad5d41aa0b10e18c84d9ca4c0aacd573d2ad25d444f5b2f5d1`.
The original directives, tool and speed-file revisions, input hashes and
per-corner metrics remain in `docs/findings/COMMERCIAL_TIMING_395.md`.
No implementation run was repeated, and no checkpoint or bitstream was written.

The report still carries ten Critical CDC diagnostics, two unsafe clock pairs,
and 46 input/87 output ports without I/O delay constraints. Positive
constrained-path slack and the diagnostic crossing probe waive none of them.
Items 3 and 4, physical temperature and oscillator evidence, remain open.

## Planted faults

| Fault | Expected result | Observed result |
|---|---|---|
| Remove report hook refusal | Builder fails | rc 1; `test_timing_grade.py:126` detects report output before refusal |
| Remove per-corner hold argument | Builder fails | rc 1; `test_timing_grade.py:78` requires `min_max` |
| Remove per-corner unconstrained argument | Builder fails | rc 1; `test_timing_grade.py:79` requires `-report_unconstrained` |
| Remove verbose timing-check argument | Builder fails | rc 1; `test_timing_grade.py:82` requires `-check_timing_verbose` |
| Remove clock-interaction hold argument | Builder fails | rc 1; `test_timing_grade.py:89` requires `min_max` |

The reviewer's unmodified `mutation_probes.py` reports `unexpected=0`:
21 fault injections fail, and the unmodified control passes. Its
`hook_refusal_probe.py` records hook rc 1 for all four wrong conditions.
`run_mutations.py` additionally drives each required fault through
`test_builder.py --require-rv32 --require-elaboration`; every one fails
in its first timing-grade arm with an assertion, before later arms run.
The corresponding `reports-*-bank.log` files preserve the diagnostics.

The new PLL probe also passes an unmodified control and rejects the old
`speedgrade=-2` literal, rc 1, using the actual constructor. Its disposable
fixture resolves pinned dependencies from the registered lane; no submodule
copy or link is used. The preliminary fixture omitted those dependencies,
failed before testing the PLL, and was corrected before final-head gates.
`preliminary-gate-results.json` retains that non-acceptance run separately.

## Gates at committed head

All nineteen commands returned rc 0 at `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`.
Each command ran in the foreground with an explicit timeout and no pipeline.
`gate-results.json` records full argv, cwd, head, times, exit codes, log sizes
and SHA-256 hashes; `run_gates.py` preserves the sequence.

| Gate | Exit | Seconds | Evidence |
|---|---:|---:|---|
| `timing-script` | 0 | 0.05 | `gates/timing-script.log` |
| `timing` | 0 | 58.39 | `gates/timing.log` |
| `crossings` | 0 | 41.85 | `gates/crossings.log` |
| `mutations` | 0 | 6.72 | `gates/mutations.log` |
| `builder-present` | 0 | 771.97 | `gates/builder-present.log` |
| `builder-absent` | 0 | 565.43 | `gates/builder-absent.log` |
| `ci-scope-selftest` | 0 | 2.08 | `gates/ci-scope-selftest.log` |
| `docs` | 0 | 4.47 | `gates/docs.log` |
| `doc-paths` | 0 | 0.06 | `gates/doc-paths.log` |
| `toc` | 0 | 2.65 | `gates/toc.log` |
| `em-dash` | 0 | 3.38 | `gates/em-dash.log` |
| `feature-status` | 0 | 0.67 | `gates/feature-status.log` |
| `doc-style` | 0 | 0.05 | `gates/doc-style.log` |
| `doc-style-selftest` | 0 | 0.05 | `gates/doc-style-selftest.log` |
| `solution-docs` | 0 | 0.11 | `gates/solution-docs.log` |
| `python-idiom` | 0 | 3.38 | `gates/python-idiom.log` |
| `python-idiom-selftest` | 0 | 3.43 | `gates/python-idiom-selftest.log` |
| `diff-committed` | 0 | 0.02 | `gates/diff-committed.log` |
| `diff-worktree` | 0 | 0.03 | `gates/diff-worktree.log` |

Compiler-present command:
`python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`.
Compiler-absent command: `python3 -B run_builder_absent.py`. That retained
wrapper runs the full entry point with `--require-elaboration`, hides exactly
three RV32 compiler candidates, and asserts all three were probed. Host
compilers stay available. Both modes executed the timing-grade platform and
PLL arms; neither skipped required elaboration.

Both modes record gate 11's unavailable historical Arty calibration report.
The absent mode also records expected compiler-dependent stand-downs.
Those skips are limits, not coverage; see `builder-*-summary.txt`.

## Limits and retained evidence

No hardware or bench access, firmware or RTL edit, timing or constraint fix,
push, PR edit, merge, or additional checkout occurred.
The three required submodules remain at their recorded pins. The unrelated
`external` submodule remains uninitialized; these gates do not consume it.
No hosted acceptance, local workflow replica or merge validation is claimed.
The assigned boundary ends with the public review-ready notice.
The shipping build and both review packets are read-only.
Builds use the physical data path. Reports over 200 KB remain outside this
packet and are represented by size and SHA-256 receipts.
Candidate head: `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`.
Worktree clean before and after commit. All final-head gate receipts are in `gate-results.json`.
Seven shipping input size/hash pairs remain unchanged. Report sizes and hashes
are in `report-artifacts.json`; larger reports remain under the physical data
path. All retained packet files are at most 200000 bytes.
`MANIFEST.sha256` inventories this packet. The worktree is clean.
Public review-ready notice: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860663722

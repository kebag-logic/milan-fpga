# [A155] Issue #407 author handoff

Commit: `6af65a151663e1301f1983a6c9d22650a0b35da9`

Message: `Pin every non-RTL carrier script and its mutation controls`

Branch: `407-carrier-script-pins`

Base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`

Implementation checkout: `$CANDIDATE`

The author task is committed and the checkout is clean. Nothing was pushed;
no PR, review request, host-side candidate act invocation, or merge was made.
All native focused commands below exited 0. Real-act AC5 evidence remains
unrun and manager-owned. This is an author evidence handoff, not approval.

## Changed files

| File | Result |
|---|---|
| `scripts/ci_events.py` | Records canonical normalized scripts directly in all 56 carrier run entries; compares by recorded position/name and reports the first differing line; refuses missing records; adds live-step-derived mutations, missing-record controls, and positive controls. |
| `docs/testing/CI_WORKFLOWS.md` | Item 11 states the complete carrier script pin and same-commit maintenance remedy; item 12 closes the non-RTL content residue and retains #439 for RTL script content. |

No workflow YAML, gate command, condition, dependency, ratchet budget, RTL,
submodule gitlink, or seven-RTL-job script policy changed. Existing specialized
gate, builder, environment-writer, sequence, key, and binding checks remain.

Useful source locations at this commit: `CARRIER_STEP_LISTS` line 869,
`check_carrier_script` line 3572, `_carrier_script_arms` line 7451,
`_selftest_carrier_script_pins` line 7804; policy item 11 addition line 635
and remaining item 12 residue line 765.

## Public contract and decisions

- [Current Issue #407](https://github.com/kebag-logic/milan-fpga/issues/407).
- [Manager's pre-implementation AC5 correction and roles](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5770808527).
- [A155 TAKEN, before first repository edit](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5770825317).
- [A155 material implementation and experiment decisions](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5770873818).

Canonical records are static reviewed data, never obtained from the candidate
workflow during checking. Existing canonical constants are reused where
available. Missing script records fail closed. Mutation populations derive
from the live carrier steps independently of those records.

Flag-removal controls apply where a proof/check flag actually exists.
Single-command bodies cannot lose one command while retaining another, and
the no-git body and docs builder call have no proof/check flag to remove.
Those cases receive no fabricated coverage claim. All bodies still receive
replacement, appended `|| true`, and continue-on-error controls.

## Acceptance mapping

| AC | Author evidence / remaining work |
|---|---|
| 1 | All 56 recognized run bodies recorded: docs-check 41, wire-accountability 2, docs-check-no-git 1, elaborate 12. Every body mutation requires the job, step, and first differing normalized line. Uses/with and existing specialized/sequence protections remain. |
| 2 | 243 new reason-pinned workflow mutation arms under `carrier-script-407`; all four carriers and every requested docs gate class included. Generic vacuity fails all 833 workflow mutation arms. Targeted disabling of only the new comparison fails all 187 new body assertions while specialized checks stay active. 56 missing-record controls and a matching-update positive control also pass. |
| 3 | `ci_events --check`: 1505 contract items, zero findings. `ci_events --selftest`: PASS, 931 total arms. |
| 4 | Policy items 11/12 updated; canonical-entry-plus-mutation maintenance remedy stated. All three acceptance documentation commands pass; style and added-line em-dash checks also pass. |
| 5 | Reproducible fixture and recipe prepared outside product source, with syntax/anchor checks only. Real-act measurements NOT RUN. Manager must measure the green tampered idiom step, both named contract refusals, failed complete docs-check job, and both failed exhaustive aggregates. |

The Python-gate example is the Python idiom gate; the bounded-ratchet example
is Boundary-unit naming ratchet (`--check` reads its existing budget). Builder
and HDL-reference steps are included in the same live-derived population.

## Mutation counts

| Carrier | No-op | `|| true` | Drop command | Drop flag | Continue-on-error |
|---|---:|---:|---:|---:|---:|
| docs-check | 41 | 41 | 30 | 32 | 41 |
| wire-accountability | 2 | 2 | 1 | 1 | 2 |
| docs-check-no-git | 1 | 1 | 1 | 0 | 1 |
| elaborate | 12 | 12 | 8 | 2 | 12 |
| Total | 56 | 56 | 40 | 35 | 56 |

Total new workflow mutations: 243; body mutations: 187; metadata mutations: 56.
Additional new record controls: 57 (56 missing, one matching update).
The existing whitespace positive control now covers every carrier body.
All workflow mutation labels are unique. The full selftest counts 931 arms,
including 833 workflow mutations and its disk/record/positive controls.

## Exact focused commands and results

Run from the implementation checkout. The `rtk proxy` prefix was used for
shell execution; combined log runs executed the listed commands via Python
subprocesses beneath that prefix. Logs preserve commands, output, and exit
codes under `logs/` beside this file.

| Command | Result | Log |
|---|---|---|
| `rtk proxy python3 scripts/ci_events.py --check` | PASS, 1505 items, zero findings | `01-ci_events.log` |
| `rtk proxy python3 scripts/ci_events.py --selftest` | PASS, 931 arms; stub checker fails all 833 workflow arms | `02-ci_events.log` |
| `rtk proxy python3 -B scripts/docs_check.py` | Zero findings, 163 Markdown files + 826 scrubbed files; 23/23 scrub and 4/4 routing controls | `03-docs_check.log` |
| `rtk proxy python3 scripts/gen_toc.py --check` | PASS, 105 annotated pages; 17 below threshold | `04-gen_toc.log` |
| `rtk proxy python3 scripts/check_doc_paths.py` | PASS, 824 cited paths; one existing allowance | `05-check_doc_paths.log` |
| `rtk proxy python3 scripts/check_py_idiom.py` | PASS, 209 first-party modules, no refusal finding or ratchet increase | `06-check_py_idiom.log` |
| `rtk proxy python3 scripts/check_py_idiom.py --selftest` | 54/54 PASS | `07-check_py_idiom.log` |
| `rtk proxy python3 scripts/ci_scope.py --selftest` | PASS | `08-ci_scope.log` |
| `rtk proxy python3 scripts/check_baremetal_only.py --check` | Zero findings across 824 tracked first-party files | `09-check_baremetal_only.log` |
| `rtk proxy python3 scripts/measure_control_flow.py --selftest` | 45/45 PASS, including both processor populations | `10-measure_control_flow.log` |
| `rtk proxy python3 scripts/check_doc_style.py` | PASS, 22 current documents | `11-check_doc_style.log` |
| `rtk proxy git diff --check` | PASS | `12-git.log` |
| `rtk proxy env VERILATOR_JOBS=8 MAKEFLAGS=-j8 python3 scripts/lint_rtl.py --check` | PASS, 90 <= ratchet 90; 17 waived, zero justified lint_off | `13-lint.log` |
| `rtk proxy env VERILATOR_JOBS=8 MAKEFLAGS=-j8 python3 scripts/xvlog_gate.py --check` | PASS with real Vivado analysis; zero parent findings, four pinned-processor findings equal existing ratchet | `14-xvlog.log` |
| `rtk proxy python3 $MANAGEMENT/407-author/PIN-VACUITY.py` | Unique labels and all 187 targeted vacuity assertions PASS | `15-pin-vacuity.log` |
| `rtk proxy python3 scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8` | Post-commit: zero findings over 30 added lines, one Markdown page; 34/34 controls | `16-em-dash.log` |

The final ci_events/docs/Python/helper run used the exact bytes subsequently
committed. Lint/xvlog ran before commit, with only later Python comment and
policy wording edits; no HDL or gitlink changed. The added-line em-dash gate
ran after commit so it checked the actual commit range.

Required submodules were at their normal gitlinks throughout these scans:

- `third_party/verilog-axis`: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`
- `protocol-processor`: `424c688fa2205b934a7689a58f2aa766420f2326`
- `gptp-processor`: `c1b617435824929a790739ea8585c3fe1a328cc0`

## AC5 execution handoff

Read [AC5-RECIPE.md](AC5-RECIPE.md). [AC5_FIXTURE.py](AC5_FIXTURE.py) generates
execution-only copies of the complete original workflows in a disposable
uncredentialed job. It must not execute on the host. The manager uses trusted
live-dev orchestration for real act, with candidate code confined to job
containers and normal verified cleanup. The execution copies are data, live
outside `.github/workflows`, and introduce no gate exemption in product code.

The docs experiment plants a genuine bare-except finding immediately before
the Python idiom step. Its direct unmasked call must return 1; the real
tampered step must then succeed; the following real contract step must fail.
The separate exhaustive experiment uses the same workflow mutation and real
job graph to prove independent refusal and aggregate fail-closed propagation.
The recipe specifies clean, defect-only, and swallowed controls plus the
exact required receipts. Generator/injection syntax and the unique source
mutation anchor were checked; none of these experiments was executed.

## Manager-owned remaining validation and publication

- Execute and publish real-act AC5 measured receipts; no green docs-check
  claim is valid for the swallowed mutation.
- Run the complete parent RTL/local verification bar and any other complete
  gates required by CONTRIBUTING; the author did not run the parent sweep.
- Push, open the draft PR against dev, start exact-head replicas from the
  trusted live-dev runner, and obtain required hosted evidence.
- Publish the saved REVIEW-READY.md evidence when appropriate, then arrange
  cold independent R219/R220 reviews and their five-lens coverage ledger.
- Complete candidate-merge validation, authorized merge, post-merge
  containment, and Issue/Project closure under the repository contract.

Known implementation maintenance cost: every legitimate carrier script edit
requires its static canonical entry and appropriate mutation coverage in the
same commit. No additional design decision or implementation blocker remains.

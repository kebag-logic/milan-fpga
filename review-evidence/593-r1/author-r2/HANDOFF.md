# Round 2 handoff

Status: assigned implementation and local validation complete; independent re-review pending.
Issue #593; PR #601; executor [A380]; reviewers [R362] and [R363].
Head: `68e801b2823f75e037152f7eb2ac4c5dcda5d919`.
Subject: `Close release soak timing and evidence gaps from round two`.
Starting head: `95bea7cf82fcf7cf034c156ef7aa6800ee769e05`.
Branch: `593-mr-tu-soak`; base: `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Working directory: `$LANES/593-mr-tu-soak`.
The worktree is clean. The commit is local and unpushed.

## Public contract

- [Round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/593#issuecomment-5859221324)
- [Round 1 assignment](https://github.com/kebag-logic/milan-fpga/issues/593#issuecomment-5858876858)
- [Corrected governing rule](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5857765949)
- [Superseded original rule](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5857762351)
- [PHC-step decision item](https://github.com/kebag-logic/milan-fpga/issues/602)
- [TAKEN](https://github.com/kebag-logic/milan-fpga/issues/593#issuecomment-5859228583)

The cited clauses were read directly from the local PDFs: IEEE 1722-2016
4.4.4.3 and 4.4.4.7 on PDF pages 36-37, and Milan v1.2 Tables 5.4/5.6
on PDF pages 40/44 and Annex B.1.1/B.1.2 on page 141.
Only hashes and sizes, not PDF or source-tree copies, are retained here.

## Assignment items and proof

| Item | Change with file:line | Reviewer probe or mutant and result |
|---|---|---|
| 1: rise edge (both F1) | `tb/tools/torture_campaign.py:3596`; `docs/testing/TESTING.md:1041`. Earliest contained event must be no later than rise + R. | Unchanged R362 S-R347-5-S1/S1b/S1c and R363 A1/A2 FAIL; R363 A3 PASS. Repository rise-removal and exclusive-edge mutants KILLED by `test_release_tu_before_first_discontinuity` / `test_release_tu_rise_boundary`. |
| 2: every GM change (both F2) | `tb/tools/torture_campaign.py:3611` adds the history oracle; `:3601` makes the diagnostic grade all supplied GM changes; `tests/steps/torture_release_steps.py:305` exercises the emitted oracle. | Unchanged R362 B1 and R363 B1/B2 FAIL. `test_release_tu_history` rejects no interval, a GM at clear and a later unserved GM; two served changes PASS. Coverage-removal and restored future-GM filtering mutants KILLED. |
| 3: deciding resolution (R362 F3 / R363 F4) | `tb/tools/torture_campaign.py:3583`, `:3622`, `:3763`; `docs/testing/TESTING.md:957`, `:1022`. R must be below min(0.25,0.5) for tu and below 1/2 seconds for the two-sided mr window. Limits are reported. | Unchanged R362 S-R346-3-S1/S1b/S1c and R363 C1/C2 give NOT RUN. `test_release_deciding_resolution` pins both sides and equality. Each ceiling-removal mutant KILLED. |
| 4: distinct causes (R363 F3) | `tb/tools/torture_campaign.py:3683`. Match earliest eligible causes, consuming one per toggle per stream. | Span-aware R363 D1/D2 FAIL, D3 PASS; R362 E1 FAIL. Reuse and reversed-consumption mutants KILLED by `test_release_mr_distinct_causes`. |
| 5: checks and assertion text (both F5, R346-3 S3) | `tb/tools/torture_campaign.py:5465`, `:5762`, `:5778`, `:5834`; `tb/tools/torture_release_mutants.py:158`. Add boundary/type/order/text fixtures and 62 controls beyond round 1's 44. | Unchanged R362: 32 applicable KILLED, no survivors; R363: 38 applicable KILLED, no survivors. Survivor recheck: all 17 applicable controls KILLED by self-test. Repository controls: 106/106 KILLED, including original 25. Changed anchors are accounted below. |
| 6: PHC conflict (R362 F4 / R363 S3) | `REQUIREMENTS.md:280`, `docs/testing/TESTING.md:936`, `docs/design/GM_LOSS_RECOVERY.md:155` link #602 and state current-image failure pending its ruling. | `scope-and-docs.log` verifies all three references. Span-aware R362 A4b and R363 G PHC-only FAIL; reviewer R36 and repository GM-only control are KILLED. No RTL change. |
| S1: capture span | `tb/tools/torture_campaign.py:3728`, `:3774`; `docs/testing/TESTING.md:974`. Recorded extent travels with completeness through `ReleaseCapture`; boolean True uses PDU endpoints conservatively. | Unchanged and span-aware R363 E1 are NOT RUN. `test_release_mr_capture_span` grades each edge, silence and packet containment; missing extent, start/end guard, PDU extent and metadata mutants KILLED. |
| S2: talker-start reset | `tb/tools/torture_campaign.py:3710`; `docs/testing/TESTING.md:967`. A decrease is classified as reset and fails for counter-walk investigation, without modulo inflation. | Span-aware R363 F1 / R362 E3 FAIL with counter-reset diagnosis and no huge delta. Reset-removal mutant KILLED by `test_release_media_reset_decrease`; high-value decreases are covered too. |

## Replay details and limits

The packet scripts remain read-only and byte-identical. Their originals run
unchanged; the receipt names are `r362-probe.log`, `r363-probe.log`,
`r362-mutants.log`, `r363-mutants.log` and `r363-survivor-recheck.log`.
`review-evidence.json` records exact commands, head, return codes and hashes.
The probe scripts always return zero; their case rows, not that exit, are proof.

The original mr fixtures contain only milliseconds of PDUs for much longer
counter windows. The new assigned span check therefore returns NOT RUN.
Separate `r362_span_probe.py` and `r363_span_probe.py` retain their stimuli,
adding recorded capture extent (-2,4) seconds to their mr helper. This span
still refuses the 3600-second cases. Their only expectation updates are the
assigned counter-reset rule and refusal of silence without sufficient span.
The original scripts and logs are retained alongside these explicit adaptations.

- External span probe: 21/21 expected results, zero gaps.
- Internal span probe: 61 matching rows, one information row, two mismatches.
  B2 asks the oracle to infer that an unkinded discontinuity is a GM change
  despite an explicit empty GM history (R362 S4). E2 asks for counter
  under-count detection (R362 S2). Neither suggestion was assigned in round 2.
  Neither is claimed fixed or silently promoted into this lane's scope.
- The survivor recheck copies only its documented partial fixture tree.
  Its behavior baseline has eight missing-asset errors, as in round 1.
  Those errors are not counted as kills. All 17 applicable self-test mutants
  fail with rc 1; the actual repository torture tier is clean (232 scenarios).

Changed review anchors are not falsely counted as killed:

| Old controls | Disposition at this head | Executed replacement |
|---|---|---|
| R362 R01/R02 | Cause matching now collects and consumes matches. | Same doubled/strict comparison re-anchored; KILLED. |
| R363 M01/M40/M41 | The former any-expression changed to consumed matches. | Same whole/first/last-loop omissions re-anchored; KILLED. |
| R363 M48 | The old GM filter was removed by the every-GM fix. | Reintroduce the pre-rise omission at the new assignment; KILLED. |
| R362 R13 / R363 M14 | Modulo wrap decoding was removed by S2. | Remove reset detection instead; KILLED. |
| R362 R24 / R363 M26 | Counting GM changes at/after clear is now required. The old mutation represents the fix, not a defect. | Restore the old filter that ignores them; KILLED. |

All eight re-anchored or replacement controls are in
`retarget_review_mutants.py`; see `review-reanchors.log`.
The repository driver retains PR #586's first 25 controls. All pass.
Its round-1 counter-delay anchor was qualified to select the same arithmetic
now that capture-span derivation also uses the interval constant.

The explicit capture metadata attests acquisition span and completeness;
it cannot independently discover dropped packets absent from the records.
Per-stream consecutive indices still reject observed gaps. Missing metadata
for a silent stream is NOT RUN. Every GM change supplied to the history
must be covered, including boundary events; callers retain their clear tails.
The PHC conflict remains open under #602, exactly as assigned. No physical
soak, hardware action, firmware/RTL/builder edit, push, PR edit or merge occurred.

## Gates at committed head

Every command below ran synchronously in the foreground, without a pipeline,
from the physical working directory above, with a 1800-second timeout.
Every receipt identifies `68e801b2823f75e037152f7eb2ac4c5dcda5d919` and rc 0.
The hash-locked Markdown dependencies were reused from `/tmp/milan-593-markdown`
through `PYTHONPATH`; no packages or toolchains were placed in this packet.

| Exact command | rc | Receipt |
|---|---|---|
| `rtk proxy python3 -B tb/tools/torture_campaign.py --self-test` | 0 | gate-01.log |
| `rtk proxy python3 -B tb/tools/torture_release_mutants.py` | 0 | gate-02.log |
| `rtk proxy python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress` | 0 | gate-03.log |
| `rtk proxy python3 -B -m behave tests/features --tags=@torture -f progress` | 0 | gate-04.log |
| `rtk proxy python3 scripts/ci_scope.py --selftest` | 0 | gate-05.log |
| `rtk proxy python3 scripts/check_baremetal_only.py --check` | 0 | gate-06.log |
| `rtk proxy python3 scripts/check_baremetal_only.py --selftest` | 0 | gate-07.log |
| `rtk proxy git diff --check` | 0 | gate-08.log |
| `rtk proxy git diff 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD --check` | 0 | gate-09.log |
| `rtk proxy python3 scripts/docs_check.py` | 0 | gate-10.log |
| `rtk proxy python3 scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04` | 0 | gate-11.log |
| `rtk proxy python3 scripts/check_em_dash.py --selftest` | 0 | gate-12.log |
| `rtk proxy python3 scripts/check_doc_style.py` | 0 | gate-13.log |
| `rtk proxy python3 scripts/check_doc_style.py --selftest` | 0 | gate-14.log |
| `rtk proxy python3 scripts/check_feature_status.py --self-test` | 0 | gate-15.log |
| `rtk proxy python3 scripts/check_doc_paths.py` | 0 | gate-16.log |
| `rtk proxy python3 scripts/check_archive.py` | 0 | gate-17.log |
| `rtk proxy python3 scripts/check_archive.py --selftest` | 0 | gate-18.log |
| `rtk proxy python3 scripts/gen_toc.py --selftest` | 0 | gate-19.log |
| `rtk proxy python3 scripts/gen_toc.py --verify-anchors` | 0 | gate-20.log |
| `rtk proxy python3 scripts/gen_toc.py --check` | 0 | gate-21.log |
| `rtk proxy python3 scripts/check_gptp_docs.py --with-submodule` | 0 | gate-22.log |
| `rtk proxy python3 scripts/check_gptp_docs.py --selftest` | 0 | gate-23.log |
| `rtk proxy python3 scripts/check_solution_docs.py` | 0 | gate-24.log |
| `rtk proxy python3 scripts/check_solution_docs.py --selftest` | 0 | gate-25.log |
| `rtk proxy python3 scripts/check_submodule_docs.py` | 0 | gate-26.log |
| `rtk proxy python3 scripts/check_submodule_docs.py --selftest` | 0 | gate-27.log |
| `rtk proxy python3 scripts/check_py_idiom.py` | 0 | gate-28.log |
| `rtk proxy python3 scripts/check_py_idiom.py --selftest` | 0 | gate-29.log |
| `rtk proxy python3 scripts/check_hygiene.py --check` | 0 | gate-30.log |
| `rtk proxy python3 scripts/check_hygiene.py --selftest` | 0 | gate-31.log |
| `rtk proxy python3 scripts/check_todo_ownership.py` | 0 | gate-32.log |
| `rtk proxy python3 scripts/check_todo_ownership.py --selftest` | 0 | gate-33.log |
| `rtk proxy python3 docs/traceability/gen_module_matrix.py --check` | 0 | gate-34.log |
| `rtk proxy python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power` | 0 | gate-35.log |

Planner: 75 tests. Repository mutants: 106 killed. Plan feature: 87 scenarios
and 356 steps. Torture tier: 232 scenarios and 901 steps passed; 172 scenarios
excluded by its tag selector. The docs and builder boundary gates all pass.
`gates.json` records durations, sizes and SHA-256 values for each receipt.
`artifact-manifest.json` records source/standards and read-only packet hashes.

## Handoff state

`PR-BODY.md` preserves its original first line and `Closes #593`, and adds
Round 2. It has not been applied to the PR. The independent reviewers must
re-review this head; this packet claims no verdict or lens coverage.
The final authorized publication is [A380] REVIEW READY on issue #593.

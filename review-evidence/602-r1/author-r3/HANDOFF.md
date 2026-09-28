[A397] Round 3 handoff for #602 / PR #603

Local candidate: `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` on `602-phc-step-mr`.
All assigned local gates returned 0 at this committed head.
This is implementation evidence; independent re-review remains required.

## Authority and boundaries

Origin: `https://github.com/kebag-logic/milan-fpga.git`, verified before work.
Starting head: `471892a9bcc2d26fdcfc19db01949ecea83c5e0f`, verified before work.
Base: `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
Executor: [A397]. Internal reviewer: [R366]. External reviewer: [R367].

Authority: [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5861304608),
[round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5860151273),
[round-1 assignment](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859299480),
[scope correction](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859621253),
and the [ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355).
The #387 decisions 5606198212 and 5794731090 and supersession note 5859297500
were read, as were the assigned desk analysis, previous author packets and
both rounds of review context. `input-fingerprints.json` records the inputs.

One local commit, with a one-line subject and no body or trailers:
`6b2ebd1c435136966f84ffc16d28a80c7d6b9387`: `test: cover delayed PHC restart causes and correct gate documentation`.
No RTL, builder, firmware, configuration or submodule change was made.
No push, remote PR edit, merge, other checkout or hardware operation occurred.
Only the authorized issue comments are published.

## Changes and proof

Finding lenses retain the reviewers' assignments.

| Item | Change with file:line | Reviewer probe or control | Result at candidate |
|---|---|---|---|
| R367-2 F1 (MINOR, Docs, Conformance) | `docs/integration/BAREMETAL_FIRMWARE.md:1469` and `:1471`: two re-base references, initializer plus render reader; CRF-only restart initializer; both rows cite #602 | R367 proximity scan, R366 five-pattern scan; unchanged `sw/builder/test_builder.py:10719` and `:10774` pins; full builder bank in both compiler modes | Zero stale current claims; both banks rc 0 |
| R366-2 F1 (MINOR, Tests, Robustness) | `tb/verilator/milan_dp/sim_main.cpp:110`, `:576`, `:1064`: keep the pre-adjtime level and grade it against the level after the existing settle interval, immediately before settime | R366 O4/O5 plants retained literally in `tb/verilator/milan_dp/gmstep_mutants.py:199` and `:210`; existing settime, adjtime and both-causes controls | Delays 16 and 256 fail only adjtime; original three failure sets unchanged; clean option-off remains 234/0 |
| R366-2 F2 = R367-2 F2 (SUGGESTION, Tests; taken) | `tb/verilator/milan_dp/sim_gmstep.cpp:1098` and `:1143`, `tb/verilator/milan_dp/gmstep_mutants.py:225`, `tb/verilator/milan_dp/README.md:661` and `:713`: name suppression coverage and explain pending-request merging | Coincident veto control; restored PHC term and removed CRF propagation controls | Veto fails only the renamed check; restored term fails isolated-step checks; CRF removal fails propagation and coincidence |
| R366-2 F3 = R367-2 F3 (SUGGESTION, Docs; taken) | `tb/verilator/milan_dp/README.md:684`: dated exact-head 42-phase measurement with both review links; `tb/verilator/milan_dp/Makefile:20`: #602 PHC-only exclusions | Compare with R366-2 and R367-2 measured 42/42 at 103/0; docs gates | Source wording corrected; docs gates rc 0 |
| Inventory required by the two retained controls | `tb/verilator/milan_dp/README.md:711`, `:718`, `:725`, `:985`, `:1001`; `docs/testing/TESTING.md:273`; `docs/design/GM_LOSS_RECOVERY.md:236` | Full inventory census and campaign | 15 gmstep + 5 option-off = 20 controls; 5 default controls unchanged |

The adjtime verdict reuses the same level that becomes the settime baseline.
No simulated cycle separates those observations. Both named delay controls use
the reviewer's actual plants: a 16-stage shift and a 256-cycle countdown.
`probe-equivalence-result.json` proves the planted source bytes are identical.
All mutation sources are disposable copies passed through the suite recipes;
the tracked RTL is unchanged.

## Stale-document rescan

Both reviewers' scans were repeated at the candidate. The R367 scanner is
unmodified; the R366 equivalent preserves all five expressions and filters
the fourth scan in Python instead of a shell pipeline.
R367: 197 proximity hits in 26 files. R366: scans 1-4 have 3/53/17/27 hit lines;
scan 5 has no hits. All were inspected in context: zero stale claims outside
`docs/history/**`. The full outputs, exact-head receipts and per-file
classification are `stale-r367.log/.json`, `stale-r366.log/.json` and
`stale-scan-classification.md`.

## Controls

Clean gmstep: 103/0. Clean option-off: 234/0, unchanged from round 2.
The full campaign passes 22/22: two clean baselines and 20 caught mutants.
The existing default campaign passes 6/6, including its clean baseline.
The five required option-off failure sets are checked exactly by
`finish_packet.py`, from the campaign's reported failures.

| Control | Required failure | Observed failures |
|---|---|---|
| the policy level is tied low at the servo | slew path: the actual servo receives the level | 2: slew path: the actual servo receives the level; slew path: every staged sample covers the PHC tail |
| the policy level omits the applied-rate tail | slew path: every staged sample covers the PHC tail | 1: slew path: every staged sample covers the PHC tail |
| the policy level misses an extra addend stage | slew path: every staged sample covers the PHC tail | 1: slew path: every staged sample covers the PHC tail |
| the PHC re-base restart term is restored | restart: a PHC-only step leaves outgoing mr unchanged | 2: restart: a PHC-only step leaves outgoing mr unchanged; restart: a PHC-only step adds no MEDIA_RESET |
| the source-change term is removed | source control: a real source change toggles mr once | 1: source control: a real source change toggles mr once |
| selected CRF mr propagation is removed | CRF control: selected CRF mr propagates exactly once | 2: CRF control: selected CRF mr propagates exactly once; coincident: a PHC step does not suppress the CRF restart |
| the grandmaster identity re-bases the render stage as well as the step | render: the GM change is one counted re-base event | 2: render: the GM change is one counted re-base event; render: every counted re-base lands at a PDU end right after the step |
| the step does not re-centre the render stage | render: the GM change is one counted re-base event | 1: render: the GM change is one counted re-base event |
| the render re-base is keyed to the identity, not the step | render: every counted re-base lands at a PDU end right after the step | 1: render: every counted re-base lands at a PDU end right after the step |
| tu reaches the talkers four cycles late | tu: set in the first cycle the bank names GM B | 1: tu: set in the first cycle the bank names GM B |
| the plane's step does not re-arm the holdover | tu: held at least the 0.25 s holdover after the step | 1: tu: held at least the 0.25 s holdover after the step |
| tu stops the talker | licence: the talker never pauses beyond four of its intervals | 6: tu: talker PDUs graded inside the hold; licence: the talker never pauses beyond four of its intervals; licence: the talker keeps its baseline rate within 1%; restart: a PHC-only step adds no MEDIA_RESET; coincident: PDUs bracket every trial and complete the hold; coincident: a PHC step does not suppress the CRF restart |
| the grandmaster change stops the talker for good | licence: the talker never pauses beyond four of its intervals | 8: tu: talker PDUs graded inside the hold; tu: talker PDUs graded after tu clears; licence: the talker never pauses beyond four of its intervals; licence: the talker keeps its baseline rate within 1%; CRF control: outgoing PDUs bracket the received toggle; CRF control: selected CRF mr propagates exactly once; coincident: PDUs bracket every trial and complete the hold; coincident: a PHC step does not suppress the CRF restart |
| the step's re-centre snaps one event off the setpoint | render: every PDU push leaves the target fill across the event | 1: render: every PDU push leaves the target fill across the event |
| software settime is restored as an mr cause | CLKV: the settime leaves mr unchanged (#602) | 2: CLKV: the settime leaves mr unchanged (#602); CLKV: settime adds no MEDIA_RESET (#602) |
| PHC adjtime is restored as an mr cause | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) |
| both PHC restart causes are restored | CLKV: the settime leaves mr unchanged (#602) | 3: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602); CLKV: the settime leaves mr unchanged (#602); CLKV: settime adds no MEDIA_RESET (#602) |
| PHC adjtime becomes an mr cause 16 cycles later | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) |
| PHC adjtime becomes an mr cause 256 cycles later | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) |
| a PHC step suppresses a coincident CRF restart | coincident: a PHC step does not suppress the CRF restart | 1: coincident: a PHC step does not suppress the CRF restart |


The full datapath target also passes both render-law modes and catches all
four render mutants (6/6). `tkdiag` passes 96/0 and catches all four engine
mutants (5/5 including its clean baseline).

## Gate table

Every row below covers `6b2ebd1c435136966f84ffc16d28a80c7d6b9387`. `$PACKET` is this evidence directory.
The physical worktree is `$LANES/602-phc-step-mr`.
`final_campaign.py`, `final_checks.py` and `run_gate.py` retain the commands,
environment and foreground timeout envelope. No gate command was piped.
Every JSON receipt records head, cwd, command, rc, timeout, elapsed time,
full-log size and SHA-256. Logs above the packet limit remain under
`$VALIDATION_STORAGE/602-a397-work`, with only a bounded tail in this packet.

| Gate / receipt | Command | Timeout (s) | Elapsed (s) | rc |
|---|---|---:|---:|---:|
| `rtl-lint.json` | `python3 scripts/lint_rtl.py --check --jobs 8` | 1800 | 9.16 | 0 |
| `ci-scope.json` | `python3 scripts/ci_scope.py --selftest` | 600 | 2.04 | 0 |
| `baremetal-check.json` | `python3 scripts/check_baremetal_only.py --check` | 600 | 15.21 | 0 |
| `baremetal-selftest.json` | `python3 scripts/check_baremetal_only.py --selftest` | 600 | 5.73 | 0 |
| `docs.json` | `python3 scripts/docs_check.py` | 600 | 4.38 | 0 |
| `doc-style.json` | `python3 scripts/check_doc_style.py` | 600 | 0.07 | 0 |
| `doc-style-selftest.json` | `python3 scripts/check_doc_style.py --selftest` | 600 | 0.05 | 0 |
| `em-dash.json` | `python3 scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04` | 600 | 3.31 | 0 |
| `doc-paths.json` | `python3 scripts/check_doc_paths.py` | 600 | 0.08 | 0 |
| `toc.json` | `python3 scripts/gen_toc.py --check` | 600 | 2.59 | 0 |
| `toc-selftest.json` | `python3 scripts/gen_toc.py --selftest` | 600 | 0.83 | 0 |
| `gptp-docs.json` | `python3 scripts/check_gptp_docs.py --with-submodule` | 600 | 0.16 | 0 |
| `feature-status.json` | `python3 scripts/check_feature_status.py --self-test` | 600 | 0.68 | 0 |
| `solution-docs.json` | `python3 scripts/check_solution_docs.py` | 600 | 0.12 | 0 |
| `submodule-docs.json` | `python3 scripts/check_submodule_docs.py` | 600 | 0.44 | 0 |
| `module-matrix.json` | `python3 docs/traceability/gen_module_matrix.py --check` | 600 | 0.98 | 0 |
| `diagram-pngs.json` | `python3 scripts/check_diagram_pngs.py` | 600 | 0.34 | 0 |
| `archive.json` | `python3 scripts/check_archive.py` | 600 | 0.29 | 0 |
| `source-lists.json` | `python3 scripts/check_rtl_source_lists.py` | 600 | 1.38 | 0 |
| `sv-idiom.json` | `python3 scripts/check_sv_idiom.py` | 600 | 0.45 | 0 |
| `cpp-idiom.json` | `python3 scripts/check_cpp_idiom.py` | 600 | 1.19 | 0 |
| `py-idiom.json` | `python3 scripts/check_py_idiom.py` | 600 | 3.42 | 0 |
| `hygiene.json` | `python3 scripts/check_hygiene.py --check` | 600 | 0.36 | 0 |
| `test-evidence.json` | `python3 scripts/measure_test_evidence.py --check` | 600 | 5.44 | 0 |
| `diff-check.json` | `git diff --check 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD` | 120 | 0.06 | 0 |
| `milan-dp.json` | `make -C $LANES/602-phc-step-mr/tb/verilator/milan_dp run` | 10800 | 1444.77 | 0 |
| `tkdiag.json` | `make -C $LANES/602-phc-step-mr/tb/verilator/tkdiag` | 1800 | 21.26 | 0 |
| `gmstep-mutants.json` | `make -C $LANES/602-phc-step-mr/tb/verilator/milan_dp gmstep-mutants` | 7200 | 911.89 | 0 |
| `builder-rv32.json` | `python3 sw/builder/test_builder.py --require-rv32` | 10800 | 756.82 | 0 |
| `builder-absent.json` | `python3 $PACKET/builder_absent.py` | 10800 | 550.53 | 0 |
| `ooc-after.json` | `python3 $PACKET/ooc_measure.py after` | 14400 | 1021.27 | 0 |
| `artifact-identity.json` | `python3 $PACKET/check_artifact_identity.py` | 1200 | 0.54 | 0 |
| `stale-r366.json` | `python3 $PACKET/stale_scan_r366.py` | 180 | 1.31 | 0 |
| `stale-r367.json` | `python3 $REVIEWS/602-r367-2-packet/stale_scan_r367_2.py $LANES/602-phc-step-mr` | 180 | 1.49 | 0 |
| `probe-equivalence.json` | `python3 $PACKET/check_probe_equivalence.py` | 180 | 0.1 | 0 |
| `candidate-audit.json` | `python3 $PACKET/audit_candidate.py` | 1100 | 0.68 | 0 |

Compiler-present mode uses `--require-rv32`. Compiler-absent mode executes the
unchanged full entry point while hiding only its three cross-compiler
candidates; `builder-absent-audit.json` records the calls and registered skips.
It does not claim compiled instruments ran. Both modes explicitly omit the
unavailable historical placed calibration report, as in the preceding round.
`versions.json` records executable identity and version. Local simulation and
lint used Verilator 5.052; OOC used Yosys 0.66 and sv2v 0.0.13.
The cited round-2 phase measurements used Verilator 5.050.

## No-side-effect evidence and limits

All 50 generated artifacts across five configurations match the prior
base-derived manifest byte for byte (`generated-before.json`,
`generated-after.json`, `artifact-identity.json`). The final audit verifies
tracked RTL, builder and configuration bytes, submodule pins and every pinned
submodule blob against the starting head, with each submodule root checked
before every Git command inside it. See `final-audit.json`.

Both AX OOC shapes pass at the committed head using the same shaped-default
recipe as round 2. `ooc-after-*-stat.txt` and the associated JSON receipts
record counts and input/artifact hashes. The earlier area question is closed
by the round-2 assignment: the reviewer measured one removed OR before LUT
mapping and mapping sensitivity in a comparable control. Release area remains
a placed-build measurement; this round adds no RTL or area claim.

The gmstep leg uses compressed clocks, zero DRP responses and the streaming
escape. It does not prove physical clock continuity or an lwSRP reservation.
The README's 42-phase statement explicitly cites the round-2 reviewed head;
this round does not claim a new 42-phase sweep. Coincidence grades suppression;
the pending merge can hide an added request there, which isolated-step checks
grade separately. Independent review, hosted checks and merge-candidate
validation remain with the reviewers and maintainer.

The first pre-commit style probe found one overlong sentence; it was corrected
before this commit. Its receipt is retained as `precommit-style.json` and is
not final-head gate evidence. Every required final-head gate passed.

## Delivery

`PR-BODY.md` preserves the [A383] first line and `Closes #602`, with a Round 3
section. It is prepared locally; the PR was not edited.
The takeover was posted as [A397] TAKEN:
https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5861314929
`REVIEW-READY.md` contains the final publication body.

Final audit: rc 0 at the candidate. Verified 203 protected repository blobs, 566 pinned submodule blobs, 15 read-only input fingerprints and 36 exact-head log receipts. Largest packet file: 126008 bytes. Worktree and all submodules are clean.

The final [A397] REVIEW READY comment was published: https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5861984828

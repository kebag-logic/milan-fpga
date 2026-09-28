[A388] Round 2 handoff for #602 / PR #603

Local candidate: `471892a9bcc2d26fdcfc19db01949ecea83c5e0f` on `602-phc-step-mr`.
All assigned local gates returned 0 at this committed head. The worktree is clean.
This is implementation evidence, not a review verdict. Independent re-review remains required.
No push, remote PR edit, merge or hardware work was performed.

## Authority and scope

Origin was verified as `https://github.com/kebag-logic/milan-fpga.git`.
Starting head: `49012143b335ea48d6a71c441a05d0c1796887ff`.
Validation base: `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
The public scope is the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5860151273),
[round-1 assignment](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859299480),
[scope correction](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859621253), and
[#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355).
The #387 decisions 5606198212 and 5794731090 retain genuine restart behavior;
supersession note 5859297500 excludes only the PHC-step obligation.
The assigned desk analysis and both round-1 review packets were read without modification.

Two local commits, each with a one-line subject and no body or trailers:

- `add85ca6a5945b7cb815ef53e9c916a3c22aa969`: test: isolate PHC restart exclusions and cover coincident CRF events
- `471892a9bcc2d26fdcfc19db01949ecea83c5e0f`: test: observe received CRF state independently of propagation

## Changes and proof

The finding lenses below retain the reviewers' labels.

| Item | Change with file:line | Reviewer probe or durable control | Final-head result |
|---|---|---|---|
| R366-1 F1 = R367-1 F1 (Docs) | `docs/fpga/FPGA_DESIGN.md:178`, `docs/reference/REGISTER_MAP.md:128`, `docs/MILAN_V12_ROADMAP.md:360`, `CHANGELOG.md:119`: PHC-only re-base preserves mr and adds no MEDIA_RESET; changelog records the reversal | Reviewer stale-document scan, including lines that mention #602 | All candidates classified below; no stale current-contract claim remains |
| R366-1 F2 = R367-1 F2 (Docs, Tests) | `docs/testing/TESTING.md:273`, `docs/testing/CI_WORKFLOWS.md:205`, `tb/verilator/milan_dp/README.md:704` and `:979`, `tb/verilator/milan_dp/Makefile:20`: 15 gmstep + 3 option-off controls, five default controls, restart-engine trigger path and historical count labels. `tb/verilator/tkdiag/sim_main.cpp:650` and `mcr_mutants.py:69`: genuine-request narrative and matching check names | CONTROLS census, full mutation inventory and tkdiag controls | Eighteen controls caught; default five caught; tkdiag 96/96 and all four mutants caught |
| R366-1 F3 (Tests) | `tb/verilator/milan_dp/sim_main.cpp:574` and `:1061`: snapshot the granted mr level before each event. `gmstep_mutants.py:183` and `:290`: enforce sibling-check isolation | Reviewer settime-only, adjtime-only and both-causes probes, retained as controls | Adjtime-only fails only adjtime; settime-only fails settime mr and MEDIA_RESET with adjtime clean; both-causes fails both event checks and settime MEDIA_RESET |
| R366-1 F4 = R367-1 F3 (Tests, Robustness; accepted suggestion) | `tb/verilator/milan_dp/sim_gmstep.cpp:1098`, `gmstep_mutants.py:197`, `README.md:659`, `docs/design/GM_LOSS_RECOVERY.md:207`: 32 real received-CRF/settime delays, an observed same-cycle overlap and exactly one outgoing toggle per trial | R366 P4 / R367 RV5 suppression expression retained in full inventory | Clean gmstep 103/103; delay 8 overlaps; every trial emits one toggle; suppression fails only the new named coincidence check |

R367-1 F4 remains under its assigned RTL lens and is closed by the round-2
assignment. It requires no further RTL edit; the two OOC receipts below provide
the requested final-head measurements. This statement is the recorded scope
decision, not a new review verdict.

The observation at `sim_gmstep.cpp:462` reads changes of the receiver's accepted
mr state, independently of restart propagation. The CRF-removal control compiles
and fails both ordinary propagation and coincidence checks. This avoids the
optimized-away alias that caused the first candidate's full target to fail.
The failed candidate receipt is retained as `milan-dp-first-candidate.json`;
it is not final-head evidence. Every assigned gate was repeated after the correction.

## Stale-document rescan

The final current-contract scan found 41 candidate lines, all inspected
in context, with zero stale claims. It includes #602 lines and excludes history,
submodules and external sources. `stale_doc_scan.py`, `stale_doc_scan.txt` and
`stale-doc-rescan.json` provide the method, candidates and committed-head receipt.

Candidates classify as the explicit PHC-only exclusion and its supersession
record; unchanged genuine-restart/pending behavior; render behavior kept separate
from restart; historical counts explicitly dated; or deliberate mutant/check
names expressing the defect under test. No candidate asserts that a PHC-only
re-base must change outgoing mr or add MEDIA_RESET. The changed current-contract
paragraphs and the tkdiag T17/T18 narrative were also inspected together.

## Controls

Both clean legs pass. The full inventory has fifteen gmstep controls and three
option-off controls; five gmstep controls remain in the default sweep.
The table reports the named failure required by each control and all observed
failures from `gmstep-mutants.log`. These are expected mutant failures; the
mutation gate itself returns 0 (20/20).

| Control | Required failure | Observed failures |
|---|---|---|
| the policy level is tied low at the servo | slew path: the actual servo receives the level | 2: slew path: the actual servo receives the level; slew path: every staged sample covers the PHC tail |
| the policy level omits the applied-rate tail | slew path: every staged sample covers the PHC tail | 1: slew path: every staged sample covers the PHC tail |
| the policy level misses an extra addend stage | slew path: every staged sample covers the PHC tail | 1: slew path: every staged sample covers the PHC tail |
| the PHC re-base restart term is restored | restart: a PHC-only step leaves outgoing mr unchanged | 2: restart: a PHC-only step leaves outgoing mr unchanged; restart: a PHC-only step adds no MEDIA_RESET |
| the source-change term is removed | source control: a real source change toggles mr once | 1: source control: a real source change toggles mr once |
| selected CRF mr propagation is removed | CRF control: selected CRF mr propagates exactly once | 2: CRF control: selected CRF mr propagates exactly once; coincident: a PHC step neither adds nor suppresses the CRF restart |
| the grandmaster identity re-bases the render stage as well as the step | render: the GM change is one counted re-base event | 2: render: the GM change is one counted re-base event; render: every counted re-base lands at a PDU end right after the step |
| the step does not re-centre the render stage | render: the GM change is one counted re-base event | 1: render: the GM change is one counted re-base event |
| the render re-base is keyed to the identity, not the step | render: every counted re-base lands at a PDU end right after the step | 1: render: every counted re-base lands at a PDU end right after the step |
| tu reaches the talkers four cycles late | tu: set in the first cycle the bank names GM B | 1: tu: set in the first cycle the bank names GM B |
| the plane's step does not re-arm the holdover | tu: held at least the 0.25 s holdover after the step | 1: tu: held at least the 0.25 s holdover after the step |
| tu stops the talker | licence: the talker never pauses beyond four of its intervals | 6: tu: talker PDUs graded inside the hold; licence: the talker never pauses beyond four of its intervals; licence: the talker keeps its baseline rate within 1%; restart: a PHC-only step adds no MEDIA_RESET; coincident: PDUs bracket every trial and complete the hold; coincident: a PHC step neither adds nor suppresses the CRF restart |
| the grandmaster change stops the talker for good | licence: the talker never pauses beyond four of its intervals | 8: tu: talker PDUs graded inside the hold; tu: talker PDUs graded after tu clears; licence: the talker never pauses beyond four of its intervals; licence: the talker keeps its baseline rate within 1%; CRF control: outgoing PDUs bracket the received toggle; CRF control: selected CRF mr propagates exactly once; coincident: PDUs bracket every trial and complete the hold; coincident: a PHC step neither adds nor suppresses the CRF restart |
| the step's re-centre snaps one event off the setpoint | render: every PDU push leaves the target fill across the event | 1: render: every PDU push leaves the target fill across the event |
| software settime is restored as an mr cause | CLKV: the settime leaves mr unchanged (#602) | 2: CLKV: the settime leaves mr unchanged (#602); CLKV: settime adds no MEDIA_RESET (#602) |
| PHC adjtime is restored as an mr cause | CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) | 1: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602) |
| both PHC restart causes are restored | CLKV: the settime leaves mr unchanged (#602) | 3: CLKV: PHC-only steps leave INTERNAL mr unchanged (#602); CLKV: the settime leaves mr unchanged (#602); CLKV: settime adds no MEDIA_RESET (#602) |
| a PHC step suppresses a coincident CRF restart | coincident: a PHC step neither adds nor suppresses the CRF restart | 1: coincident: a PHC step neither adds nor suppresses the CRF restart |

The full datapath target also passes both clean render-law modes and catches
all four render mutants (6/6). `tkdiag` passes 96 clean checks and catches all
four pending-window mutants (5/5 including its clean baseline).

## Gates

All rows below cover `471892a9bcc2d26fdcfc19db01949ecea83c5e0f`. `$ROOT` is the physical worktree
`$LANES/602-phc-step-mr`; `$PACKET` is this evidence directory.
`final_campaign.py`, `final_checks.py` and `run_gate.py` retain the exact ordering,
environment and foreground timeout envelope. Commands were not piped.
Each JSON receipt records the full command, head, cwd, rc, duration, log size and
SHA-256. Logs above the packet size limit remain in `$VALIDATION_STORAGE/602-a388-work`;
the packet retains only a bounded tail and the hash/size receipt.

| Gate / receipt | Command | Timeout (s) | Elapsed (s) | rc |
|---|---|---:|---:|---:|
| `rtl-lint.json` | `python3 scripts/lint_rtl.py --check --jobs 8` | 1800 | 9.52 | 0 |
| `ci-scope.json` | `python3 scripts/ci_scope.py --selftest` | 600 | 2.03 | 0 |
| `baremetal-check.json` | `python3 scripts/check_baremetal_only.py --check` | 600 | 14.98 | 0 |
| `baremetal-selftest.json` | `python3 scripts/check_baremetal_only.py --selftest` | 600 | 5.6 | 0 |
| `docs.json` | `python3 scripts/docs_check.py` | 600 | 4.3 | 0 |
| `doc-style.json` | `python3 scripts/check_doc_style.py` | 600 | 0.07 | 0 |
| `doc-style-selftest.json` | `python3 scripts/check_doc_style.py --selftest` | 600 | 0.05 | 0 |
| `em-dash.json` | `python3 scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04` | 600 | 3.43 | 0 |
| `doc-paths.json` | `python3 scripts/check_doc_paths.py` | 600 | 0.09 | 0 |
| `toc.json` | `python3 scripts/gen_toc.py --check` | 600 | 2.56 | 0 |
| `toc-selftest.json` | `python3 scripts/gen_toc.py --selftest` | 600 | 0.84 | 0 |
| `gptp-docs.json` | `python3 scripts/check_gptp_docs.py --with-submodule` | 600 | 0.18 | 0 |
| `feature-status.json` | `python3 scripts/check_feature_status.py --self-test` | 600 | 0.69 | 0 |
| `solution-docs.json` | `python3 scripts/check_solution_docs.py` | 600 | 0.13 | 0 |
| `submodule-docs.json` | `python3 scripts/check_submodule_docs.py` | 600 | 0.48 | 0 |
| `module-matrix.json` | `python3 docs/traceability/gen_module_matrix.py --check` | 600 | 0.99 | 0 |
| `diagram-pngs.json` | `python3 scripts/check_diagram_pngs.py` | 600 | 0.35 | 0 |
| `archive.json` | `python3 scripts/check_archive.py` | 600 | 0.28 | 0 |
| `source-lists.json` | `python3 scripts/check_rtl_source_lists.py` | 600 | 1.39 | 0 |
| `sv-idiom.json` | `python3 scripts/check_sv_idiom.py` | 600 | 0.45 | 0 |
| `cpp-idiom.json` | `python3 scripts/check_cpp_idiom.py` | 600 | 1.23 | 0 |
| `py-idiom.json` | `python3 scripts/check_py_idiom.py` | 600 | 3.46 | 0 |
| `hygiene.json` | `python3 scripts/check_hygiene.py --check` | 600 | 0.35 | 0 |
| `test-evidence.json` | `python3 scripts/measure_test_evidence.py --check` | 600 | 5.4 | 0 |
| `diff-check.json` | `git diff --check 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD` | 120 | 0.06 | 0 |
| `milan-dp.json` | `make -C $ROOT/tb/verilator/milan_dp run` | 10800 | 1425.01 | 0 |
| `tkdiag.json` | `make -C $ROOT/tb/verilator/tkdiag` | 1800 | 24.05 | 0 |
| `gmstep-mutants.json` | `make -C $ROOT/tb/verilator/milan_dp gmstep-mutants` | 7200 | 874.05 | 0 |
| `builder-rv32.json` | `python3 sw/builder/test_builder.py --require-rv32` | 10800 | 765.39 | 0 |
| `builder-absent.json` | `python3 $PACKET/builder_absent.py` | 10800 | 554.17 | 0 |
| `ooc-after.json` | `python3 $PACKET/ooc_measure.py after` | 14400 | 1088.44 | 0 |
| `artifact-identity.json` | `python3 $PACKET/check_artifact_identity.py` | 1200 | 0.53 | 0 |
| `stale-doc-rescan.json` | `python3 $PACKET/stale_doc_scan.py` | 180 | 1.36 | 0 |
| `candidate-audit.json` | `python3 $PACKET/audit_candidate.py` | 1200 | 0.69 | 0 |

The datapath run includes gPTP 181/181 in each latency variant, gmstep 103/103,
option-off and no-LPF 234/234, AX 1x1 231/231, and audio-clock 190/190.
The README's older dated counts are historical; these receipts hold this candidate's measurements.

## Builder, area and identity

See `builder-rv32.json`, `builder-absent.json` and `builder-absent-audit.json` for
both complete builder modes and the audited absence of all three compiler candidates.
The compiler-present mode rejects 358/358 mutations; the absent mode rejects
256/256. Each mode elaborates 53/53 RTL mutation variants.
The compiler-present mode covers the compiler-dependent checks omitted in the
absent mode. Both modes explicitly omit the unavailable historical placed calibration
report; no placed-build claim follows from these runs.

`ooc-after.json` covers both AX shapes, with parameters, source hashes and mapped
statistics in `ooc-after-endstation_ax7101_1x1_tdm8.json` and
`ooc-after-endstation_ax7101_8x8.json`. The round-2 assignment closes the earlier
area question: R366-1 established exactly one fewer OR gate before LUT mapping;
LUT movement under structural controls is mapping sensitivity.

| Shape | LUT | LUTRAM | LUT total | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AX 1x1 TDM8 | 97812 | 6764 | 104576 | 46021 | 16 | 20 | 17 | 3725 |
| AX 8x8 | 142972 | 6748 | 149720 | 60064 | 17 | 21 | 19 | 4523 |

No new area claim
or RTL explanation is introduced. Release area still requires a placed build.

`generated-before.json` and `generated-after.json` compare all fifty generated
artifacts across the five configurations; the committed-head identity gate requires
all sizes and SHA-256 values to match. `final-audit.json` confirms unchanged RTL,
configuration and builder bytes against the starting head, unchanged clean submodule
pins and contents, one-line commits, a clean worktree and valid receipt hashes.
Each submodule Git operation first verifies its actual checkout root. The audit
verifies 203 protected first-party blobs and 566 submodule blobs, including modes
and tracked symlink targets. Its first helper attempt treated a tracked README
symlink as a regular file; `candidate-audit-first.json` retains that helper failure.
The corrected audit passes without changing any checkout file.

## Evidence bounds and handoff

The gmstep harness uses compressed clocks, held audio clocks, zero DRP read data
and the streaming escape. It proves the simulated wiring and packet behavior;
it does not prove physical clock continuity, hardware servo action or an lwSRP
reservation. No hardware or placed implementation was run.

`PR-BODY.md` retains its [A383] first line and `Closes #602`, adds Round 2, and
contains no absolute home paths or attribution footer. It is prepared locally;
the remote PR was not edited. Independent re-review, hosted checks and eventual
merge-candidate validation remain completion requirements outside this assignment.

"""Finalize the handoff only after the candidate's recorded gates succeed."""
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
HEAD = '471892a9bcc2d26fdcfc19db01949ecea83c5e0f'
audit = json.loads((OUT/'final-audit.json').read_text())
assert audit['head'] == HEAD and audit['clean']
for name in ('milan-dp', 'tkdiag', 'gmstep-mutants', 'builder-rv32', 'builder-absent',
             'ooc-after', 'artifact-identity', 'stale-doc-rescan', 'candidate-audit'):
    receipt = json.loads((OUT/(name+'.json')).read_text())
    assert receipt['head'] == HEAD and receipt['rc'] == 0, name
controls = (OUT/'controls-table.md').read_text()
gates = (OUT/'gates-table.md').read_text()
scan_count = len((OUT/'stale_doc_scan.txt').read_text().splitlines())

handoff = f"""[A388] Round 2 handoff for #602 / PR #603

Local candidate: `{HEAD}` on `602-phc-step-mr`.
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
- `{HEAD}`: test: observe received CRF state independently of propagation

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

The final current-contract scan found {scan_count} candidate lines, all inspected
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

{controls}
The full datapath target also passes both clean render-law modes and catches
all four render mutants (6/6). `tkdiag` passes 96 clean checks and catches all
four pending-window mutants (5/5 including its clean baseline).

## Gates

All rows below cover `{HEAD}`. `$ROOT` is the physical worktree
`$LANES/602-phc-step-mr`; `$PACKET` is this evidence directory.
`final_campaign.py`, `final_checks.py` and `run_gate.py` retain the exact ordering,
environment and foreground timeout envelope. Commands were not piped.
Each JSON receipt records the full command, head, cwd, rc, duration, log size and
SHA-256. Logs above the packet size limit remain in `$VALIDATION_STORAGE/602-a388-work`;
the packet retains only a bounded tail and the hash/size receipt.

{gates}
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
"""
(OUT/'HANDOFF.md').write_text(handoff)

body = f"""[A383]

Closes #602

## Description

A PHC-only presentation-time re-base preserves outgoing `mr` and adds no MEDIA_RESET under the [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355). Render re-base, `tu` holdover, genuine source changes, selected-CRF disruption and received-`mr` propagation retain their behavior. The ruling supersedes only the PHC-step restart obligation of #387.

## Round 2

Local candidate: `{HEAD}`. All assigned local gates passed at this committed head.

- Correct the FPGA design, register map, roadmap and changelog. Current documents consistently exclude PHC-only `mr` and MEDIA_RESET causes.
- Correct campaign routing and inventory: fifteen gmstep controls, three option-off controls, five default controls, and the restart-engine source among the triggers. Mark historical counts explicitly. The restart-engine harness describes genuine restart requests.
- Compare each option-off event against its preceding `mr` level. Adjtime-only fails only its own event check; settime-only and both-causes fail the settime check. The mutation driver enforces the sibling-check exclusions.
- Add 32 timings of received CRF `mr` against software settime. Every trial steps the PHC and transmits exactly one outgoing toggle. The run observes same-cycle overlap at delay 8. A mutant that suppresses the received restart on that cycle fails only the new check.

RTL, the five configurations, builder code and submodule pins remain unchanged from round-1 head `49012143b335ea48d6a71c441a05d0c1796887ff`.

## Validation

- Full `milan_dp` target: rc 0; gmstep 103/103; render controls 6/6; default gmstep controls 6/6 including the clean baseline.
- Complete gmstep inventory: 20/20, comprising two clean baselines and eighteen caught mutants.
- `tkdiag`: 96/96, with all four mutants caught.
- Both complete builder modes, both AX datapath OOC shapes, RTL lint, CI-scope self-test, baremetal checks, documentation gates and diff hygiene: rc 0.
- All fifty generated artifacts match across the five configurations; RTL/configuration/builder bytes and submodule pins/contents match the starting head. Final stale-document rescan: {scan_count} candidates inspected, zero stale claims.

The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5860151273) closes the earlier OOC-area question. R366-1 measured exactly one fewer OR gate before LUT mapping; the mapped LUT changes reflect mapping sensitivity. Release area remains a placed-build measurement.

## Evidence bounds

The gmstep harness uses compressed clocks and the streaming escape. It does not prove physical clock continuity or an lwSRP reservation. The compiler-absent mode omits compiled instruments; both builder modes omit the unavailable historical placed calibration report. Controls and exact gate receipts are recorded in `HANDOFF.md`. Independent re-review, hosted checks and merge-candidate validation remain separate completion requirements.
"""
assert body.startswith('[A383]\n') and 'Closes #602' in body and '/home/' not in body
(OUT/'PR-BODY.md').write_text(body)
print('Final handoff and PR body written from successful candidate receipts.')

ready = f"""[A388] REVIEW READY

Commit: `{HEAD}` (local candidate on `602-phc-step-mr`; not pushed).

Changed: current PHC-only restart documentation and changelog, campaign inventory/routing, event-relative option-off checks with sibling isolation, and a 32-delay real CRF/settime coincidence test with a suppression control. RTL, configurations, builder code and submodule pins/contents remain unchanged from `49012143b335ea48d6a71c441a05d0c1796887ff`.

Validation at this committed head, all commands returned 0. `$ROOT` is `$LANES/602-phc-step-mr`; `$PACKET` is the round-2 evidence packet. Every command ran in the foreground with an explicit timeout and no pipeline.

- `make -C $ROOT/tb/verilator/milan_dp run`: full target passes; gmstep 103/103, render controls 6/6, default gmstep controls 6/6.
- `make -C $ROOT/tb/verilator/milan_dp gmstep-mutants`: 20/20 (two clean baselines, all eighteen controls caught).
- `make -C $ROOT/tb/verilator/tkdiag`: 96/96 and all four mutants caught.
- `python3 sw/builder/test_builder.py --require-rv32`: 358/358 mutations rejected, 53/53 RTL variants elaborated. `python3 $PACKET/builder_absent.py`: full bank, 256/256 mutations rejected, 53/53 RTL variants elaborated; all three compiler candidates audited absent.
- `python3 $PACKET/ooc_measure.py after`: both AX datapath shapes pass. The area question remains closed by the round-2 assignment.
- `python3 $PACKET/final_checks.py`: all 25 gates pass, including `scripts/lint_rtl.py --check --jobs 8`, `scripts/ci_scope.py --selftest`, both baremetal checks, documentation gates and diff hygiene.
- `python3 $PACKET/check_artifact_identity.py`: all fifty generated artifacts match across the five configurations. `python3 $PACKET/stale_doc_scan.py`: {scan_count} candidates inspected in context, zero stale current-contract claims. `python3 $PACKET/audit_candidate.py`: clean worktree, unchanged protected bytes and submodules, valid final-head receipt hashes.

Acceptance evidence: adjtime-only fails only adjtime; settime-only leaves adjtime clean and fails settime mr/MEDIA_RESET; both-causes fails settime. The clean coincidence phase observes same-cycle overlap at delay 8 and exactly one outgoing toggle in each of 32 trials; its suppression mutant fails only the new named check.

`HANDOFF.md` contains per-item file:line references, reviewer-probe mappings, the full controls table, stale-document classification, gate commands/results and log sizes/SHA-256 values. `PR-BODY.md` has its Round 2 section and retains `[A383]` and `Closes #602`; the remote PR was not edited.

Evidence bounds: compiler-absent instruments and the unavailable historical placed calibration report are explicitly not run; compiler-present instruments passed. Simulated packet behavior does not establish physical clock continuity, an lwSRP reservation or placed area. Independent re-review remains required; this is no review verdict. No push, merge or hardware work was performed.
"""
(OUT/'REVIEW-READY.md').write_text(ready)

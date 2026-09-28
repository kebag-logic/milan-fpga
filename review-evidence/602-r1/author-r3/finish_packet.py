"""Assemble the round-3 handoff from completed exact-head gate receipts."""
from pathlib import Path
import json
import re
import shlex

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/602-phc-step-mr')
HEAD = '6b2ebd1c435136966f84ffc16d28a80c7d6b9387'


def gates_table() -> str:
    """Require all assignment gates and render their exact commands."""
    required = ['rtl-lint', 'ci-scope', 'baremetal-check', 'baremetal-selftest',
                'docs', 'doc-style', 'doc-style-selftest', 'em-dash', 'doc-paths',
                'toc', 'toc-selftest', 'gptp-docs', 'feature-status', 'solution-docs',
                'submodule-docs', 'module-matrix', 'diagram-pngs', 'archive',
                'source-lists', 'sv-idiom', 'cpp-idiom', 'py-idiom', 'hygiene',
                'test-evidence', 'diff-check', 'milan-dp', 'tkdiag', 'gmstep-mutants',
                'builder-rv32', 'builder-absent', 'ooc-after', 'artifact-identity',
                'stale-r366', 'stale-r367', 'probe-equivalence']
    table = '| Gate / receipt | Command | Timeout (s) | Elapsed (s) | rc |\n'
    table += '|---|---|---:|---:|---:|\n'
    for name in required:
        receipt = json.loads((OUT / (name + '.json')).read_text())
        assert receipt['head'] == HEAD and receipt['rc'] == 0, name
        command = shlex.join(receipt['command']).replace(str(OUT), '$PACKET')
        table += (f'| `{name}.json` | `{command}` | {receipt["timeout"]} | '
                  f'{receipt["seconds"]} | 0 |\n')
    return table


def controls_table() -> str:
    """Verify the five required failure sets and report the full campaign."""
    log = (OUT / 'gmstep-mutants.log').read_text()
    records = re.findall(r'\[PASS\] control caught: (.+?) - breaks "(.+?)"\n'
                         r'    it broke (\d+) check\(s\): (.+)', log)
    assert len(records) == 20 and '22 checks: 22 PASS, 0 FAIL' in log
    adj = 'CLKV: PHC-only steps leave INTERNAL mr unchanged (#602)'
    sett = 'CLKV: the settime leaves mr unchanged (#602)'
    reset = 'CLKV: settime adds no MEDIA_RESET (#602)'
    expected = {
        'software settime is restored as an mr cause': {sett, reset},
        'PHC adjtime is restored as an mr cause': {adj},
        'both PHC restart causes are restored': {adj, sett, reset},
        'PHC adjtime becomes an mr cause 16 cycles later': {adj},
        'PHC adjtime becomes an mr cause 256 cycles later': {adj},
    }
    observed = {name: set(broken.split('; ')) for name, _, _, broken in records}
    for name, failures in expected.items():
        assert observed[name] == failures, (name, observed[name])
    table = '| Control | Required failure | Observed failures |\n|---|---|---|\n'
    for name, required, count, broken in records:
        table += f'| {name} | {required} | {count}: {broken} |\n'
    return table


gate_table = gates_table()
control_table = controls_table()
(OUT / 'gates-table.md').write_text(gate_table)
(OUT / 'controls-table.md').write_text(control_table)
assert json.loads((OUT / 'generated-before.json').read_text()) == json.loads(
    (OUT / 'generated-after.json').read_text())

handoff = f'''[A397] Round 3 handoff for #602 / PR #603

Local candidate: `{HEAD}` on `602-phc-step-mr`.
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
`{HEAD}`: `test: cover delayed PHC restart causes and correct gate documentation`.
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

{control_table}

The full datapath target also passes both render-law modes and catches all
four render mutants (6/6). `tkdiag` passes 96/0 and catches all four engine
mutants (5/5 including its clean baseline).

## Gate table

Every row below covers `{HEAD}`. `$PACKET` is this evidence directory.
The physical worktree is `$LANES/602-phc-step-mr`.
`final_campaign.py`, `final_checks.py` and `run_gate.py` retain the commands,
environment and foreground timeout envelope. No gate command was piped.
Every JSON receipt records head, cwd, command, rc, timeout, elapsed time,
full-log size and SHA-256. Logs above the packet limit remain under
`$VALIDATION_STORAGE/602-a397-work`, with only a bounded tail in this packet.

{gate_table}

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
'''
(OUT / 'HANDOFF.md').write_text(handoff)

body = f'''[A383]

Closes #602

## Description

A PHC-only presentation-time re-base preserves outgoing `mr` and adds no MEDIA_RESET under the [#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355). Render re-base, `tu` holdover, genuine source changes, selected-CRF disruption and received-`mr` propagation retain their behavior. The ruling supersedes only the PHC-step restart obligation of #387.

## Round 3

Local candidate: `{HEAD}`. All assigned local gates passed at this committed head.

- Correct the firmware gate contract to two `media_rebase_p_w` references and the CRF-only `mcr_restart_p_w` initializer, citing #602. Both reviewers' stale-document scans now find zero stale current claims.
- Grade adjtime after settling, immediately before the settime baseline. The retained 16-cycle and 256-cycle delayed-cause controls fail only the adjtime check. The three existing controls keep their exact failure sets; clean option-off remains 234/0.
- Name the coincident check for suppression and document its pending-merge limit. Cite the round-2 reviewers' 42-phase measurement and correct the Makefile labels.
- Update the full inventory to fifteen gmstep and five option-off controls. The five default controls are unchanged.

RTL, builder, configurations and submodule pins remain unchanged from round-2 head `471892a9bcc2d26fdcfc19db01949ecea83c5e0f`.

## Round 2

The preceding round corrected the FPGA design, register map, roadmap, changelog and harness narratives; made option-off checks event-relative; and added 32 timings of received CRF `mr` against software settime. Round 3 addresses the two remaining findings and the accepted wording suggestions.

## Validation

- Full `milan_dp` target: rc 0; gmstep 103/0; option-off 234/0; render controls 6/6; default gmstep campaign 6/6.
- Full gmstep campaign: 22/22, comprising two clean baselines and twenty caught mutants.
- `tkdiag`: 96/0, with all four mutants caught.
- Full builder bank in both compiler modes, both AX datapath OOC shapes, RTL lint, CI-scope self-test, baremetal checks, documentation gates and diff hygiene: rc 0.
- All fifty generated artifacts across the five configurations remain byte-identical. Both stale-document rescans are classified with zero stale claims outside history.

The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5860151273) closes the earlier OOC-area question. Release area remains a placed-build measurement.

## Evidence bounds

The gmstep harness uses compressed clocks and the streaming escape; it does not prove physical clock continuity or an lwSRP reservation. The compiler-absent mode omits compiled instruments; both builder modes omit the unavailable historical placed calibration report. `HANDOFF.md` records per-finding evidence, controls, scans and exact-head gate receipts. Independent re-review, hosted checks and merge-candidate validation remain separate completion requirements.
'''
(OUT / 'PR-BODY.md').write_text(body)
print('Wrote handoff, PR body, gate table and exact control table.')

review_ready = f"""[A397] REVIEW READY

Commit: `{HEAD}` on `602-phc-step-mr` (local; not pushed).

Changed: the option-off adjtime observation now spans the settle interval up to the settime baseline; the two delayed-cause controls are retained; the firmware gate contract and accepted coincidence/measurement labels are corrected. No RTL, builder, firmware, configuration or submodule change was made in this round.

Acceptance criteria: met at this committed head.

- R367-2 F1: the firmware contract names two `media_rebase_p_w` references and the CRF-only restart initializer, with #602 citations. Both stale-document scans were rerun and every hit classified: zero stale claims outside `docs/history/**`. The full builder bank passes in both compiler modes.
- R366-2 F1: the 16-cycle and 256-cycle controls each fail only adjtime. The original failure sets remain settime-only = settime `mr` plus MEDIA_RESET; adjtime-only = adjtime alone; both-causes = all three. Clean option-off remains 234/0.
- Accepted suggestions: coincidence is named as suppression coverage with the pending-merge bound; the README cites the round-2 reviewers' 42/42 phase measurement at `471892a9`; the Makefile labels #602 PHC-only exclusions.
- All 50 generated artifacts across five configurations match the base-derived manifest. Both AX OOC shapes pass. The area question remains closed by the round-2 assignment; no new area claim is made.

Validation: all commands below returned 0 at `{HEAD}`. Full `milan_dp` passes, including gmstep 103/0, option-off 234/0, render campaign 6/6 and default gmstep campaign 6/6. The full gmstep campaign passes 22/22 (two clean baselines, twenty caught controls). `tkdiag` passes 96/0 and catches all four mutants.

`$PACKET` denotes the supplied `602-a397` evidence directory. Commands ran from the physical `$LANES/602-phc-step-mr` worktree in the foreground with explicit timeouts; none was piped. Per-gate receipts record the head, command, elapsed time, rc, full-log size and SHA-256. `HANDOFF.md` supplies file:line mapping, controls, scan classification and gate tables; `PR-BODY.md` is updated locally.

{gate_table}

Open risks/questions: no unresolved implementation question. The compiler-absent bank explicitly omits compiled instruments; both builder modes omit the unavailable historical placed-calibration report. The gmstep harness uses compressed clocks and the streaming escape, and does not prove physical clock continuity or an lwSRP reservation. Coincidence grades suppression; isolated checks grade an added PHC-only cause. The final audit confirms a clean worktree, unchanged protected bytes and submodule pins, unchanged read-only inputs, bounded packet files and one commit with a one-line subject and no body or trailers. Independent re-review remains required. No push or PR edit was performed.
"""
(OUT / 'REVIEW-READY.md').write_text(review_ready)
print('Wrote final issue publication body.')

#!/usr/bin/env python3
"""Package completed factual receipts; never publish or approve a change."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANE = Path('$CANDIDATE')
HEAD = '7ab1c8d0ad073fbc1977c455dea89b7b318d4e52'
TREE = '790849ab7fcf7c712c77fe051bb5fb6a45d830c2'
BASE = '483a133ed08867ea0d300d2b4a027b5b48a4282f'
NAMES = ('cold-sequential', 'warm-sequential', 'cold-pooled', 'warm-pooled')

def load(path):
    return json.loads(path.read_text())

def main():
    assert subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(LANE), 'rev-parse', 'HEAD'], text=True).strip() == HEAD
    assert not subprocess.check_output(['rtk', 'proxy', 'git', '-C', str(LANE), 'status', '--porcelain'])
    comparisons = {t: load(ROOT / 'runs' / f'{t}-comparison.json') for t in ('cold', 'warm')}
    assert all(c['head'] == HEAD and c['measurably_faster'] for c in comparisons.values())
    analyses = {n: load(ROOT / 'runs' / n / 'analysis.json') for n in NAMES}
    timing = '| Run | Full suite s | Before ordinary s | Ordinary span s | Render span s |\n|---|---:|---:|---:|---:|\n'
    resource = '| Run | Peak ordinary/group children | Mean ordinary children | Peak ordinary RSS KiB | Peak aggregate RSS KiB | wait4 single RSS KiB |\n|---|---:|---:|---:|---:|---:|\n'
    commands = []
    for n, a in analyses.items():
        assert load(ROOT / 'runs' / n / 'exit.json') == dict(make=0, verdict=0, tally=0, clean=True, same_head=True)
        assert a['whole_log']['checks'] == 9324 and a['whole_log']['failures'] == 0
        assert all(leg['sightings'] == 1 for leg in a['legs'])
        phase = a['leg_phase']
        timing += f"| {n} | {a['summary']['wall_s']:.3f} | {phase['first_leg_seen_t']:.3f} | {phase['span_s']:.3f} | {a['render']['span_s']:.3f} |\n"
        resource += f"| {n} | {phase['max_alive']}/{phase['max_group_alive']} | {phase['mean_alive']:.3f} | {phase['peak_leg_rss_kb']} | {phase['peak_tree_rss_kb']} | {a['summary']['max_single_rss_kb']} |\n"
        i = load(ROOT / 'runs' / n / 'identity.json')
        cmd = ['rtk', 'proxy', 'python3', str(ROOT / 'bench/run_suite.py'), '--lane', str(LANE), '--out', str(ROOT / 'runs' / n), '--verilator', i['tool'], '--expect-head', HEAD, '--jobs', i['environment']['SIM_JOBS'], '--temperature', i['mode']]
        commands.append(dict(name=n, command=cmd, head=HEAD, tree=TREE, exit=0, summary=a['summary']))
    (ROOT / 'evidence/benchmark-command-receipts.json').write_text(json.dumps(commands, indent=2) + '\n')
    gains = '\n'.join(f"- {t}: {c['sequential_seconds']:.3f} -> {c['pooled_seconds']:.3f} seconds; saved {c['seconds_saved']:.3f} seconds ({c['percent_saved']:.3f}%)." for t, c in comparisons.items())
    identity = f"""Commit: `{HEAD}`
Tree: `{TREE}`
Starting dev: `{BASE}`
Branch: `517-bounded-simulation-pool`.
Lane: `{LANE}`.
Issue: https://github.com/kebag-logic/milan-fpga/issues/517
Settled decision: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5780545051
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5780571502

The lane is clean. One source commit, one line, no trailers. No push, PR,
merge, delegation, Docker/act, privilege, hardware operation, shared install,
or other-checkout edit was performed.

"""
    pending = """Manager-owned evidence remains pending: hosted dedicated-worker timing
comparison; full parent/PP/gPTP/Yosys/builder native banks; trusted act;
exact-head hosted contexts; independent R245 internal Codex and R246 external
Opus review across all five lenses; current merge-candidate validation;
authorized merge and post-merge containment. External Opus availability is
pending. This author handoff is not approval or completion of the merge bar.
"""
    acceptance = """| Acceptance | Author evidence | Pending work |
|---|---|---|
| 1: inventory/arguments/phases | Frozen ten-command integration control, unchanged build/gPTP/render recipes, one observation per ordinary executable in each run, identical binary/input hashes | Independent review |
| 2: measured speed | Complete same-head cold and warm one/two-worker pairs; full-suite gains below | Hosted comparison belongs to manager |
| 3: failures/shared state/cleanup | 17 real-process runner arms; six planted faults rejected, including contention after removing exclusivity; empty/nonempty frame-output cases; pidfd proof of descendant reaping | Independent review |
| 4: real suite/render/counts/policy | Four complete runs: 9324 checks, zero failures, 13 tallies each; 8956 ordinary checks; 24 phase controls; scoped policy checks pass with no ratchet change | Broader banks belong to manager |
| 5: full release/review/merge bar | Not claimed by A178 | Manager and reserved reviewers |

"""
    measurements = f"""## Committed-head measurements

{gains}

{timing}
{resource}
The phase spans and concurrency/RSS are observations sampled at a requested
0.1-second interval, not added tests. Aggregate RSS is the peak sum of sampled
command descendants, not an exact simultaneous host peak. wait4 reports the
separate peak single-process value. Both pooled runs observe independent/group
overlap, with at most two ordinary children and one grouped child in samples.
Failure-sensitive tests independently hold the limits and exclusion.

All runs inherit CPU affinity 96-103 (eight logical CPUs), memory.max
12884901888 bytes (12 GiB), outer make -j1 and VERILATOR_JOBS=8. The pinned
Verilator reports 5.050; its actual verilator_bin SHA-256 is
`44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`.
Driver/wrapper, compiler, Python and make identities are retained separately.

Cold means the existing suite clean target removed build artifacts; host
filesystem caches were not evicted. Warm reuses the preceding same-mode build
artifacts but reruns every simulation and mutant. One pair per temperature is
measured on this host; no guaranteed percentage or hosted gain is claimed.
Full-suite time includes unchanged builds, prerequisites and render phases.
No build-speed improvement is attributed to pooling.

Every ordinary capture matches byte for byte within each comparison. Cold and
warm sequential captures also match. Executable/input hashes, both gPTP
transcripts, all six render outcomes and the semantics of all 23 render phase
records match; measured timing fields differ. All three affected tracked-header
byte copies match the commit before and after every run. Each run ends at the
same clean head. See runs/*-comparison.json and each complete run directory.

"""
    detail = """## Implementation and provenance

The Makefile passes the same ten executable paths, without arguments, and
legacy banners to a suite-local runner. SIM_JOBS defaults to 2; only 1 and 2
are accepted independently of make flags. The five sim_nxn legs are one
exclusive group in legacy relative order. Independent work can bypass waiting
group members within the total two-child limit. MILAN_COUNTER_FRAME_OUT being
present, including empty, serializes the entire ordinary set. Complete merged
stdout/stderr stays in per-child obj_legs captures and replays in legacy order.
Failures stop later launches and fail the recipe. Interrupts kill process groups
and adopt, terminate and reap orphan descendants, including separate sessions.
Partial logs remain attributable, including independent logs beyond an unstarted
group member. The unchanged render driver follows ordinary success only.

A178 restored A176's preserved pending-source runner/tests as implementation
material, then completed exclusion, replay across unstarted group members, process controls,
Makefile integration and documentation. All prior artifacts remain untouched;
recovery-provenance.json records their hashes. No A173/A176 preliminary result
is accepted as a final measurement. The only C++ change corrects an inaccurate
comment: verify_source.py proves all 47519 executable tokens unchanged. It
also proves Makefile content outside the SIM_JOBS declaration and ordinary tail
unchanged. Models, generator argv, timers, scenarios, processor pins, workflows
and ratchets stay fixed. See evidence/WRITE-AUDIT.md and source integrity receipts.

## Commands and receipts

bench/COMMANDS.md has portable commands. evidence/benchmark-command-receipts.json
records exact executed benchmark argv, head/tree, exit, timing and wait4 usage.
Each run directory contains source/tool/resource identities, input and binary
hashes, complete suite and per-leg logs, all tracked-header byte copies,
process samples, analysis, tally and verdict. scripts/suite_tally.py --verdict
and its accounting command returned 0 for each complete real suite.

All thirteen commands in evidence/committed-controls/receipts.json returned 0:
runner, phase observation, tally, ownership, docs, contents, em-dash, Python
idiom, shell idiom, hygiene, evidence, fail-fast and TODO ownership. Runner:
17/17; observation: 24/24. Exact commands, wall times and clean head/tree are
in that receipt. Six planted runner faults were rejected by assertions,
including shared-state contention, masked exit, lost output, three workers,
parallel frame writers and unreaped descendants. The last uses pidfd reaping
state before fixture cleanup, so a zombie is not accepted as containment.
See evidence/committed-mutants/command.json and receipts.json. The external
120-second guard protects synthetic controls only; no simulation deadline changes.

The preliminary-* directories are uncommitted development receipts, not final
acceptance. Only committed-* controls and the four complete runs above are
final author evidence. Prior private reasoning or reviewer context was not read.

"""
    (ROOT / 'HANDOFF.md').write_text('# A178 factual implementation handoff\n\n' + identity + detail + acceptance + measurements + '## Pending manager and reviewer work\n\n' + pending)
    (ROOT / 'REVIEW-READY.md').write_text('# A178 REVIEW READY for independent source review\n\n' + identity + acceptance + measurements + pending)
    (ROOT / 'PR-BODY.md').write_text(f"""[A178]

## Status

Local implementation at `{HEAD}` is ready for independent review.
Manager validation and both reserved reviews remain pending.

## Description

The ten ordinary milan_dp executables previously ran sequentially. A suite-local
runner now allows two children while keeping the five sim_nxn header writers
exclusive and ordered. Independent legs can overlap that group. SIM_JOBS=1
reproduces sequential execution; presence of MILAN_COUNTER_FRAME_OUT preserves
the original whole-set order. Per-child logs replay in legacy order. Failures
stop the recipe, and interruption terminates and reaps owned descendants.
Build recipes, gPTP prerequisites and render mutation phases are unchanged.
The inaccurate sim_nxn explanatory comment is corrected; executable tokens match.

## How to reproduce

With pinned Verilator 5.050 on PATH, compare the complete suite:

```sh
make -C tb/verilator/milan_dp clean
make -C tb/verilator/milan_dp run SIM_JOBS=1 VERILATOR_JOBS=8
make -C tb/verilator/milan_dp clean
make -C tb/verilator/milan_dp run SIM_JOBS=2 VERILATOR_JOBS=8
```

## How to validate

Run `python3 tb/verilator/milan_dp/test_sim_pool.py`, the existing phase controls,
and the complete real suite with its unchanged render campaign. Preserve logs
and use `scripts/suite_tally.py --verdict`. Controlled cold/warm and fault-test
receipts are supplied in the author handoff for a PR evidence comment. The
manager owns full native banks, trusted act, hosted timing/gates and candidate checks.

## DoD

Local scope and measured comparisons are recorded. R245/R246 review, manager
validation, authorized merge and post-merge containment remain open. No author
approval is claimed.

Closes #517
Relates to #270
""")
    print('Packaged handoff, review-ready record, PR body and benchmark command receipts.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

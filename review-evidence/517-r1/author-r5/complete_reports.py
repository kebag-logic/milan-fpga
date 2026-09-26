import json
import subprocess
from run_gate import OUT, ROOT


def read(name):
    return json.loads((OUT / name).read_text())


head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
assert head == '1d694677c8f376ec44e3b59b1d7fa7abccda106b'
sweep = read('sweep-summary.json')
assert sweep['head'] == head and sweep['suites'] == 55 and sweep['failures'] == 0
assert all(row['exit'] == 0 for row in sweep['chunks'])
static = read('static-final-summary.json')
assert all(row['exit'] == 0 for row in static)
real = read('real-cancellation-exits.json')
assert len(real) == 5 and all(row['exit'] == 0 for row in real)
assert read('final-integrity.json')['clean']

chunk_table = '| Chunk | Suites | Checks | Exit | Seconds |\n|---|---:|---:|---:|---:|\n'
for row in sweep['chunks']:
    chunk_table += f"| {row['chunk']} | {row['suites']} | {row['checks']} | {row['exit']} | {row['seconds']:.3f} |\n"
summary = (f"All {sweep['suites']} default suites passed: {sweep['checks']} checks, "
           f"zero failures or timeouts, {sweep['declared_skips']} declared skips. "
           "The inventory contains no missing or duplicate suite, and tally accounting is complete.")

p = OUT / 'HANDOFF.md'
s = p.read_text()
a = s.index('Status:'); b = s.index('\nStart head:', a)
s = s[:a] + f'Status: Round 5 implemented and locally validated at `{head}`. All requested positive gates exit 0. Independent re-review and publication of the local head remain.' + s[b:]
a = s.index('## Full default sweep'); b = s.index('## Reviewer probes', a)
s = s[:a] + '## Full default sweep\n\n' + summary + '\n\n' + chunk_table + '''
Each chunk ran `env VERILATOR_JOBS=16 taskset -c 16-31 scripts/run_all_suites.sh <output>/sweep-N --shard N/5`, sequentially and without a timeout override. `sweep-exits.json` records every exit. `sweep-summary.json` records every suite and declared skip. `sweep-accounting.log` is the repository tally's successful `--expect-suite-root tb/verilator` check across all five directories. The four `tsn_fuzz` field-campaign/freshness skips contribute no checks and are not hardware evidence.

''' + s[b:]
real_text = 'Real-leg cancellation corroboration also passes:\n\n| Role | Mode | Signal | Exit | Evidence |\n|---|---|---|---:|---|\n'
for row in real:
    if row['probe'] == 'internal':
        name = f"real-internal-{row['mode']}-{row['signal']}"
        receipt = read(name + '/result.json')
        evidence = f"make status {receipt['make_exit']}; {receipt['seconds_to_exit']} s; no survivors"
    else:
        receipt = read('real-external-generator.receipt.json')
        evidence = f"runner status {receipt['runner_status']}; {receipt['runner_exit_within_s']} s; no survivors"
    real_text += f"| {row['probe'].title()} | {row['mode']} | {row['signal']} | {row['exit']} | {evidence} |\n"
real_text += '\nBoth public scripts ran unchanged under the repository ownership wrapper. Internal probes exercised the actual Makefile with real built legs; the external probe signaled while a real builder/image-generator descendant was live and stdout stayed unread. Raw receipts retain attribution, delivered-prefix checks, exit signals and survivor observations.\n'
s = s.replace('Real-leg cancellation corroboration is pending the full sweep.', real_text)
a = s.index('## Gates'); b = s.index('## Validation scope and limits', a)
gates = '## Gates\n\nNormal gates below all exit 0; deliberate restored defects have their expected nonzero outcomes in the probe table. No gate command was shell-piped. Each named gate has matching `.json` and `.log` receipts.\n\n| Gate | Command | Result | Exit |\n|---|---|---|---:|\n'
extra = [
    ('builder-sdk', 'python3 builder-sdk.py', 'complete test_builder.py --require-rv32; one declared NOT RUN arm'),
    ('builder-no-compiler', 'python3 builder-no-compiler.py', 'complete test_builder.py; two declared NOT RUN arms'),
    ('pool-unit-restored', 'python3 tb/verilator/milan_dp/test_sim_pool.py', '17/17'),
    ('pool-backpressure-restored', 'python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py', '28/28'),
    ('benchmark-before', 'taskset -c 16-23 make -C tb/verilator/milan_dp', 'default cold pool before; 10074/0'),
    ('benchmark-after', 'taskset -c 16-23 make -C tb/verilator/milan_dp', 'default cold pool after; 10074/0'),
    ('sweep-accounting', 'python3 scripts/suite_tally.py --expect-suite-root tb/verilator <five log directories>', summary),
]
for name, command, result in extra:
    row = read(name + '.json')
    assert row['exit'] == 0
    gates += f"| {name} | `{command}` | {result}; {row['seconds']:.3f} s | 0 |\n"
for row in static:
    command = ' '.join(row['argv'])
    if row['name'] == 'behave':
        command = 'cd tests && ' + command
    gates += f"| {row['name']} | `{command}` | PASS; {row['seconds']:.3f} s | 0 |\n"
gates += '\nBDD: 344 scenarios, 1739 steps. Bare-metal self-test: 700 arms. CI event check: 1647 items; self-test: 2188 arms. Phase observation: 24/24. Git-free docs: zero findings, one declared inventory-parity skip. Xvlog and RTL-lint ratchets remain unchanged.\n\n'
s = s[:a] + gates + s[b:]
a = s.index('## Remaining work')
s = s[:a] + '''## Final integrity and handoff

The final tracked worktree and initialized submodules are clean; the index matches the committed tree. The single Round 5 commit has a one-line subject and no body or trailers. `final-integrity.json` records the checks. The full original PR body was retrieved with `gh pr view 524 --json body`; `PR-BODY.md` is its updated local artifact, preserving `Closes #517`.

The public-evidence fetch and extracted scripts were read only during use, verified unchanged, and removed from temporary scratch after their final probes. No toolchain, SDK, installed package, virtual environment, tool prefix or tree export is stored in this output directory.

The head is local. No push, PR mutation, merge, additional checkout, hardware operation or donor edit was performed. Independent review, reviewer-owned lens coverage, trusted replication, hosted gates/timing, candidate validation, authorized merge and post-merge containment remain outside this author handoff. The review-ready issue comment is recorded below after posting.
'''
p.write_text(s)

p = OUT / 'PR-BODY.md'
s = p.read_text()
a = s.index('## Round 5'); b = s.index('## Status', a)
round5 = f'''## Round 5

Local head: `{head}`. Implements items 1-3 of [the assignment](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5843777653):

- Audited all eleven ordinary legs with tree/private nanosecond timestamps and file-operation traces, including a same-byte-write positive control. Five legs each write fourteen files in distinct private directories; the other six write no data files. A common-TMPDIR run confirms seventy distinct private paths with no intersection. Both unchanged reviewer builder probes confirm no suite-directory tracked-header write; the repository-root positive control detects one. Removed all five unsupported exclusivity marks, restored the accurate base comment and documented the measured writes.
- Made the backpressure fixture establish default signal dispositions and an empty mask, and read the ledger while both writers are held. Twenty default-SIGINT and twenty inherited-ignored runs all pass 28/28. Both reviewers' selected exclusivity, overlap, inventory and backpressure mutations reject their defects. The old runner blob `761ec858` fails 28/28. One overlap mutation is rejected by a guard timeout rather than an assertion; that existing fixture limitation remains under #495.
- Corrected the runner contract to eleven legs and included `obj_crflic` in the no-handler rationale. Runtime runner code is unchanged in this round.

The full default pooled cold command used pinned Verilator 5.050, CPUs 16-23 and eight build jobs, after `make clean` each time:

| State | Seconds | Exit | Checks / failures |
|---|---:|---:|---|
| Before, `f36b40dd` | 1356.114 | 0 | 10074 / 0 |
| After, final runtime artifacts | 1361.378 | 0 | 10074 / 0 |

The after sample is 5.264 s (0.388%) slower: this pair shows no incremental speed gain. Both are single shared-host samples; test activity used separate CPUs and static checks also overlapped the after run. All executable hashes, eleven captures and replay bytes match; tracked header bytes and nanosecond mtimes remain unchanged. The final amendment changes only the cancellation fixture's PID packaging, leaving timed artifacts identical. Final-head sequential/warm and hosted timing were not measured in this round.

All requested normal gates exit 0, including both builder modes, pool controls, every static/documentation/HDL/idiom gate and BDD. The unmodified complete builder test ran with a selector adapter for the supplied read-only SDK, and separately with RV32 candidates unavailable. Compiler argv receipts are retained; this is local compatibility evidence. The declared unavailable builder arms remain listed below. Real-leg blocked-output cancellation passes INT/TERM/HUP through the actual Makefile, plus TERM with file output and TERM while a real generator descendant is live; no owned process survives.

'''
s = s[:a] + round5 + s[b:]
s = s.replace('Round 5 results are recorded below; the five-chunk sweep is still running while this artifact is prepared.', 'Round 5 results are recorded below; every requested gate and all five default-sweep chunks exit 0.')
s = s.replace('The Round 5 sweep table will be populated from the recorded chunk exits and suite logs.', summary + '\n\n' + chunk_table)
assert s.startswith('[A324]\n') and 'Closes #517' in s and '/home/' not in s
assert 'pending final sweep' not in s.lower() and 'still running' not in s.lower()
p.write_text(s)

comment = f'''[A324] REVIEW READY

Commit: `{head}` (local; not pushed).

Changed: Round 5 items 1-3 only. All eleven leg write sets were measured with positive controls; the five private writers have disjoint fourteen-file sets, so their unsupported exclusivity marks are removed. The accurate base comment and measured-write documentation are restored. The backpressure fixture establishes its signal state and reads the ledger while writers are held. The contract states eleven legs and includes `obj_crflic`.

Validation: both complete builder modes exit 0; pool unit controls 17/17; backpressure controls 28/28 in each of twenty default-SIGINT and twenty inherited-ignored repeats. Both reviewers' finding-specific probes ran unchanged. Selected mutations reject their defects; the old runner fails 28/28. Real-leg cancellation probes pass, with no survivors. All requested static, documentation, HDL, idiom, BDD and CI-event gates exit 0. {summary} Every chunk exits 0.

Cold default-pool timing, same CPUs and build jobs: 1356.114 s before, 1361.378 s after. The after sample is 0.388% slower; no incremental speed gain is claimed. Executable hashes, eleven captures and replay bytes match, with tracked header bytes and nanosecond mtimes unchanged.

Limits: builder utilization calibration has no hardware report; no-compiler mode additionally declares compiler-dependent instruments unavailable. Four field/freshness skips contribute no checks. The overlap mutant reaches a guard timeout, not an assertion catch. Timing is one shared-host pair. Independent re-review, publication of the local head, trusted replication, hosted gates/timing and candidate checks remain.

Handoff and full updated PR body are prepared as local management artifacts. No PR edit, push or merge was performed. Suggestions remain under #495.
'''
(OUT / 'REVIEW-READY.md').write_text(comment)
print('HANDOFF.md, PR-BODY.md and REVIEW-READY.md finalized from receipts.')

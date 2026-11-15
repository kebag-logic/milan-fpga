#!/usr/bin/env python3
"""verify_r10.py RAW ROUND9_TABLE RERUN_JOBS OUT: round 10's verify table (lane 895). RAW is verify_wf.py's table at the
head over the four workflows; a step MISSING there must be of a job round 10 did not run again (RERUN_JOBS, comma
separated `workflow/job`) and must have rc 0 in round 9's table at 056d619d, the job reading none of the paths round 10
changed: it is carried. Exit 1 on a bad row, a MISSING step of a job run again, or a MISSING step with no rc 0 in
round 9's table."""
import sys
from pathlib import Path

raw, r9, rerun, out = Path(sys.argv[1]), Path(sys.argv[2]), set(sys.argv[3].split(',')), Path(sys.argv[4])


def rows(p):
    for line in p.read_text().splitlines():
        f = [c.strip() for c in line.split('|')]
        if len(f) > 6 and f[1] and f[1] not in ('Workflow', '---') and not f[1].startswith('-'):
            yield f[1:-1]


prior = {(r[0], r[1], r[2]): r for r in rows(r9)}
lines, bad, counts = [], 0, {'ran': 0, 'not run with a reason': 0, 'carried from round 9': 0}
for r in rows(raw):
    wf, job, step, name, verdict = r[:5]
    key = (wf, job, step)
    if verdict == 'MISSING':
        p = prior.get(key)
        if f'{wf}/{job}' in rerun or p is None or p[4] != '0':
            bad += 1
            lines.append(f'| {wf} | {job} | {step} | {name} | BAD: missing, {"run again" if f"{wf}/{job}" in rerun else "no rc 0 at 056d619d"} | |')
        else:
            counts['carried from round 9'] += 1
            lines.append(f'| {wf} | {job} | {step} | {name} | carried: 0 at 056d619d | {p[5] if len(p) > 5 else ""} |')
    elif verdict == '0':
        counts['ran'] += 1
        lines.append('| ' + ' | '.join(r) + ' |')
    elif verdict == 'NOT RUN':
        counts['not run with a reason'] += 1
        lines.append('| ' + ' | '.join(r) + ' |')
    else:
        bad += 1
        lines.append('| ' + ' | '.join(r) + ' | BAD |')
head = ['| Workflow | Job | Step | Name | rc | Log or reason |', '|---|---|---|---|---|---|']
summary = ', '.join(f'{v} {k}' for k, v in counts.items()) + f', {bad} bad'
out.write_text('\n'.join(head + lines + ['', summary, '']))
print(summary)
sys.exit(1 if bad else 0)

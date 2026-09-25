import json
import shlex
import re
from pathlib import Path

out = Path(__file__).resolve().parent
path = out/'HANDOFF.md'
text = path.read_text()
rows = [json.loads(line) for line in (out/'gates.jsonl').read_text().splitlines()]
section = '## Gates\n\nEvery invocation retains its own head, command, exit and raw log. Failed preliminary attempts remain listed.\n\n| Gate | Command | Head | Exit | Seconds | Log |\n| --- | --- | --- | --- | --- | --- |\n'
for row in rows:
    command = shlex.join(row['argv']).replace(str(out),'$EVIDENCE')
    section += f"| {row['name']} | `{command}` | `{row['head'][:8]}` | {row['exit_code']} | {row['seconds']:.3f} | `{row['name']}.log` |\n"
start = text.index('## Gates\n')
end = text.index('## Final state\n',start)
text = text[:start]+section+'\n'+text[end:]
text = '\n'.join(line for line in text.split('\n') if not line.startswith('Gate `'))
names = ['sequential-cold','sequential-warm','pooled-cold','pooled-warm']
wall = '## Wall-clock measurements\n\nThe unchanged budget is 3600 s (`docs/testing/CI_WORKFLOWS.md:159`). Cold means suite build artifacts were cleaned, not filesystem-cache eviction. Warm retains same-mode builds and reruns all phases. CPU affinity is 16-23 with eight build jobs and pinned version 5.050.\n\n| Run | CPUs | Seconds | Exit | Budget margin | Evidence |\n| --- | --- | --- | --- | --- | --- |\n'
for name in names:
    result = out/name/'result.json'
    if result.exists():
        row = json.loads(result.read_text())
        wall += f"| {name} | 16-23 | {row['seconds']:.3f} | {row['exit_code']} | {3600-row['seconds']:.3f} s | `{name}/result.json` |\n"
    else:
        wall += f"| {name} | 16-23 | pending | pending | pending | pending |\n"
a = text.index('## Wall-clock measurements\n')
b = text.index('## Gates\n',a)
text = text[:a]+wall+'\n'+text[b:]
completed_benchmarks = [name for name in names if (out/name/'result.json').exists()]
latest = {row['name']:row for row in rows}
completed_chunks = [i for i in range(5) if f'sweep-{i}' in latest]
for i in completed_chunks:
    row = latest[f'sweep-{i}']
    text = re.sub(rf'(\| {i}/5 \| .*? \| )pending( \|)',rf'\g<1>exit {row["exit_code"]}; {row["seconds"]:.3f} s\g<2>',text)
failures = [row['name'] for row in rows if row['head']=='f36b40ddb5bf7fa5b12bba47d136e0b9d429403c' and row['exit_code'] != 0]
verdict = ('Final-head nonzero exits: '+', '.join(failures)+'. ') if failures else 'Every completed final-head gate has exit 0. '
status = (f'Status: local validation in progress. Rebase, focused controls, all static gates and both builder modes are complete. '
          f'{len(completed_benchmarks)}/4 full-suite measurements and {len(completed_chunks)}/5 sweep chunks have completed. '
          + verdict + 'Preliminary failures and their resolutions remain recorded below.')
text = re.sub(r'^Status:.*$',status,text,count=1,flags=re.M)
path.write_text(text)

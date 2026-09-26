import json
from pathlib import Path
from run_gate import OUT

rows = []
for i in range(5):
    result = OUT / f'sweep-{i}.json'
    log = OUT / f'sweep-{i}.log'
    if result.exists():
        row = json.loads(result.read_text())
        text = log.read_text()
        summary = [line for line in text.splitlines() if line.startswith(('suites:', 'checks:'))]
        rows.append((str(i)+'/5', row['exit'], row['seconds'], '; '.join(summary)))
        print(f"Chunk {i}/5: exit {row['exit']}, {row['seconds']} s; " + '; '.join(summary))
    elif log.exists():
        lines = log.read_text().splitlines()
        passed = [line for line in lines if line.startswith('PASS ')]
        logs = list((OUT / f'sweep-{i}').glob('*.log'))
        active = max(logs, key=lambda path: path.stat().st_mtime).name if logs else 'preflight'
        print(f"Chunk {i}/5: active {active}; {len(passed)} completed PASS suites")
        if any(line.startswith(('FAIL ', 'TIMEOUT ')) for line in lines):
            print('Attention: nonpassing suite recorded')
section = '## Full default sweep\n\n| Chunk | Exit | Seconds | Summary |\n|---|---:|---:|---|\n'
for row in rows:
    section += '| ' + ' | '.join(map(str,row)) + ' |\n'
if len(rows) < 5:
    section += '\nRemaining chunks are pending; no complete-sweep verdict yet.\n'
else:
    section += '\nAll chunk exits recorded; see final inventory and tally accounting.\n'
p = OUT / 'HANDOFF.md'
s = p.read_text()
if '## Full default sweep' in s:
    a = s.index('## Full default sweep')
    b = s.index('## Reviewer probes', a)
    s = s[:a] + section + '\n' + s[b:]
else:
    s = s.replace('## Reviewer probes', section + '\n## Reviewer probes')
p.write_text(s)

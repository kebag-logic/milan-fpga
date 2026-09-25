from pathlib import Path
import collections
import json
import shlex

OUT = Path(__file__).resolve().parent
rows = [json.loads(line) for line in (OUT / 'gates.jsonl').read_text().splitlines()]
counts = collections.Counter()
table = ['| Gate / chunk | Command or recipe | Seconds | Exit |', '|---|---|---:|---:|']
for row in rows:
    label = row['label']
    counts[label] += 1
    argv = row['argv'][:]
    if argv[0] == 'env':
        argv.pop(0)
        while argv and '=' in argv[0]:
            argv.pop(0)
    if label.startswith('dp-'):
        command = 'Default datapath recipe, entry ' + str(int(label[3:])) + ' in dp-commands.json'
    else:
        command = shlex.join(argv).replace(str(OUT) + '/', './')
    command = command.replace('|', '\\|')
    log = label + '.log'
    if label == 'bank-10' and row['exit_code'] != 0:
        log = 'bank-10-initial.log'
    table.append(f"| [{label}, attempt {counts[label]}]({log}) | `{command}` | {row['seconds']:.3f} | {row['exit_code']} |")
text = '\n'.join(table)+'\n'
p = OUT / 'HANDOFF.md'
s = p.read_text()
a = s.index('## Gates\n')
b = s.index('## Remaining duties\n')
s = s[:a]+'## Gates\n\n'+text+'\nExact argv, working directory, UTC start, duration and exit: `gates.jsonl`.\nExpected mutant failures are separate evidence, not failed positive gates.\n\n'+s[b:]
p.write_text(s)
print(f'Rendered {len(rows)} recorded invocations.')

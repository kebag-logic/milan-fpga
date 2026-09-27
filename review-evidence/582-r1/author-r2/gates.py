"""Run assigned local gates sequentially in the physical lane, without pipes."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path('$LANES/582-baremetal-clock')
OUT = Path(__file__).resolve().parent
LOGS = Path('/tmp/582-a374-validation')
PY = '$WORKSPACE_HOME/litex-milan/venv/bin/python3'
DOC_PY = '/tmp/582-a370-docs/bin/python3'
BASE = '9e9954e96bf55181edb9949ae94c9abd4ab6aaf5'
assert Path.cwd().resolve() == ROOT
LOGS.mkdir(exist_ok=True)
(OUT / 'gates').mkdir(exist_ok=True)


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


head = git('rev-parse', 'HEAD')
assert not git('status', '--porcelain'), 'commit the candidate before running gates'
for rel in ('protocol-processor', 'gptp-processor', 'third_party/verilog-axis'):
    path = ROOT / rel
    assert Path(git('-C', str(path), 'rev-parse', '--show-toplevel')) == path
commands = [
    ('builder-rv32', [PY, '-u', 'sw/builder/test_builder.py', '--require-rv32'], 14400),
    ('builder-absent', [PY, '-u', str(OUT / 'builder-absent.py')], 14400),
    ('clock-contract', [PY, 'sw/builder/test_clock_contract.py', '--soc'], 1800),
    ('declarations', [PY, 'sw/builder/test_declarations.py'], 1800),
    ('capture', [PY, 'scripts/check_nvm_capture.py'], 1800),
    ('pp-mem', [PY, 'sw/litex/test_pp_mem_bridge.py'], 1800),
    ('identity', [PY, str(OUT / 'identity.py')], 1800),
    ('reviewer-mutants', [PY, '-u', str(OUT / 'reviewer-probes.py')], 7200),
    ('R354-bypass', [PY, '$REVIEWS/582-r354-1-packet/scripts/bypass_probe.py', str(ROOT)], 1800),
    ('R355-soc', [PY, '$REVIEWS/582-r355-1-packet/scripts/31_soc_behaviour.py', str(ROOT), 'round2'], 1800),
    ('usage', [PY, str(OUT / 'usage-probe.py')], 1800),
]
for index, args in enumerate(json.loads((OUT / 'docs-commands.json').read_text())):
    commands.append((f'docs-{index:02d}-{Path(args[0]).stem}', [DOC_PY, *args], 1800))
commands += [('diff-worktree', ['git', 'diff', '--check'], 600),
             ('diff-base', ['git', 'diff', '--check', BASE, 'HEAD'], 600)]
results = []
for name, command, timeout in commands:
    log = LOGS / f'{name}.log'
    started = time.monotonic()
    print(f'START {name} at {head}', flush=True)
    with log.open('w') as stream:
        proc = subprocess.run(['timeout', str(timeout), *command], cwd=ROOT,
                              stdout=stream, stderr=subprocess.STDOUT, timeout=timeout + 60)
    raw = log.read_bytes()
    evidence = OUT / 'gates' / log.name
    if len(raw) <= 200_000:
        shutil.copyfile(log, evidence)
    record = dict(gate=name, command=['timeout', str(timeout), *command], cwd=str(ROOT), head=head,
                  returncode=proc.returncode, seconds=round(time.monotonic()-started, 2),
                  log=str(log), size=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    if evidence.exists():
        record['packet_log'] = str(evidence.relative_to(OUT))
    results.append(record)
    (OUT / 'gate-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'END {name}: rc {proc.returncode}, {record["seconds"]} seconds, {len(raw)} log bytes', flush=True)
    handoff = OUT / 'HANDOFF.md'
    body = handoff.read_text().split('\n## Live committed-head gate progress', 1)[0]
    body += '\n## Live committed-head gate progress\n\n'
    body += f'Head: `{head}`. Details: `gate-results.json`.\n\n'
    body += '| Gate | rc | Seconds |\n|---|---:|---:|\n'
    body += ''.join(f'| {r["gate"]} | {r["returncode"]} | {r["seconds"]} |\n' for r in results)
    handoff.write_text(body)
    if proc.returncode:
        print(raw.decode(errors='replace')[-7000:], flush=True)
        sys.exit(proc.returncode)
assert git('rev-parse', 'HEAD') == head
assert not git('status', '--porcelain'), 'gate left tracked changes'
print(f'PASS: {len(results)} commands at committed head {head}', flush=True)

#!/usr/bin/env python3
"""Copy this round's measurements into receipts/, host paths replaced by names, and index the files present (lane 895).

Files over 200 KB are not copied: their size and sha256 are recorded instead (receipts/large.txt).
"""
import hashlib
import json
import re
import shutil
from pathlib import Path

O = Path('$MANAGEMENT/2026-09-23/895-a775/receipts')
T = Path('/data-2/milan/tmp/895-a775')
S = Path('$MANAGEMENT/2026-09-23/895-a775/scripts')
SUBS = [(str(T / 'builds'), '<builds>'), (str(T), '<scratch>'), ('/data-2/milan/tmp/665s2b-a683zm/builds', '<round 28 builds>'),
        ('$LANES/895-talker', '<lane>'), ('$MANAGEMENT/tools', '<tools>'),
        ('$MANAGEMENT/2026-09-23', '<management>'), ('$VALIDATION_TOOLS', '<tools>'),
        ('$VALIDATION_STORAGE/scratch', '<scratch2>'), ('$WORKSPACE_HOME', '<home>')]
large = []


def scrub(text: str) -> str:
    """Host paths as names."""
    for a, b in SUBS:
        text = text.replace(a, b)
    return text


def put(rel: str, src: Path | None = None, text: str | None = None) -> None:
    """One receipt, from a file or a text, scrubbed; a file over 200 KB recorded by size and sha256 only."""
    if src is not None:
        if not src.exists():
            return
        data = src.read_bytes()
        if len(data) > 200_000:
            large.append(f'{rel}\t{len(data)} B\tsha256 {hashlib.sha256(data).hexdigest()}')
            return
        text = data.decode(errors='replace')
    p = O / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(scrub(text))


def tail(path: Path, pattern: str) -> str:
    """The lines of a log that match."""
    return ''.join(l for l in path.read_text(errors='replace').splitlines(True) if re.search(pattern, l)) if path.exists() else ''


# the legs: each one's grading summary and findings, the helpers' duplicate stops, the merges
SUMMARY = r'^(BUDGET|STATED|SHARE|NOTICE|SAVE|STEPS|AGED|REFUSED|== |merged|regrade|CLOCK|\d+ groups graded)'
for name in ('GN1', 'GN8c', 'GW1', 'GW8', 'GB1', 'GB8', 'GN8b', 'GA1-p0', 'GA1-p1', 'GA8-p0', 'GA8-p1', 'GA8-h', 'GA8-h2'):
    put(f'legs/{name}.txt', text=tail(T / 'legs' / f'{name}.log', SUMMARY))
for name in ('GA8-h', 'GA8-h2'):
    put(f'legs/{name}-helper.txt', T / 'legs' / f'{name}.txt')
for name in ('mergeA1', 'mergeA8'):
    put(f'legs/{name}.txt', text=tail(T / 'units' / f'{name}.log', SUMMARY))
for b in ('GA1', 'GA8'):
    put(f'legs/{b}-merged-from.json', T / 'builds' / b / 'results-all' / 'merged-from.json')
    for k in ('part0', 'part1', 'parth', 'parth2'):
        put(f'legs/{b}-{k}.groups', T / 'builds' / b / f'{k}.groups')
for b, r in (('GA1', 'results-all'), ('GA8', 'results-all'), ('GN1', 'results'), ('GN8c', 'results'),
             ('GW1', 'results'), ('GW8', 'results'), ('GB1', 'results'), ('GB8', 'results')):
    put(f'legs/{b}-table.md', T / 'builds' / b / r / 'table.md')
    spec = T / 'builds' / b / 'build.json'
    if spec.exists():
        d = json.loads(spec.read_text())
        put(f'legs/{b}-build.txt', text=f"executable_sha256 {d['executable_sha256']}\nvariant {d.get('variant')}\n"
                                        f"inputs {json.dumps(d['inputs'], indent=1)}\n")
# the costs and the tables
for leg in ('G1', 'G8', 'N8'):
    for f in ('costs.txt', 'aecp.txt', 'costs.json', 'aecp.json', 'parts.txt'):
        put(f'costs/{leg}/{f}', T / 'costs' / leg / f)
put('costs/tables.json', T / 'costs' / 'tables.json')
for f in ('closes.txt', 'least-margin.txt', 'heaviest-work.txt', 'load-check.txt', 'flip-check.txt',
          'load-check-before.txt', 'flip-check-before.txt', 'layout-probe.txt'):
    put(f'costs/{f}', T / 'receipts-src' / f)
# the plants of this round and the SRP campaign shard run before the final pass
for run in ('lost1', 'lost2'):
    put(f'plants/{run}.txt', text=tail(T / 'units' / f'{run}.log', r'^\[|RESULT|planting'))
put('plants/srpcamp-shard3-9f0a12d3.txt', text=tail(T / 'units' / 'srpcamp.log', r'^\[|test_ctrl_firmware|PASS|FAIL'))
put('tests/gate-suites-8a407ed5.txt', text=tail(T / 'units' / 'gate1.log', r'verdict|RESULT|tsn-c-stack'))
put('rom/answering-every-port-8x8-if2-refused.txt', text=tail(T / 'builds' / 'GN8b' / 'image.log', r'REFUSED'))
# the final gate pass, on d023b77a (gates2); the pass on f44f0b6e it superseded keeps its two findings
G = T / 'gates2'
OLD = T / 'gates'
for name in ('rtl-fast__firmware-boundary__ci_step_9.log', 'rtl-fast__firmware-boundary__ci_step_9.rc'):
    put(f'gates-f44f0b6e/{name}', OLD / 'wf' / 'logs' / name)
for name in ('docs__docs-gates-1__gate_25_0.log', 'docs__docs-gates-1__gate_25_0.rc'):
    put(f'gates-f44f0b6e/first-docs-gates-1/{name}', OLD / 'wf' / 'first-docs-gates-1' / name)
    put(f'gates-f44f0b6e/rerun-docs-gates-1/{name}', OLD / 'wf' / 'logs' / name)
put('gates-f44f0b6e/dispatch.txt', OLD / 'dispatch.txt')
put('gates/rv32-sdk.txt', OLD / 'rv32-sdk-verify.txt')
put('costs/least-margin-final.txt', T / 'receipts-src' / 'least-margin-final.txt')
for p in sorted((G / 'wf' / 'logs').glob('*')) if (G / 'wf' / 'logs').exists() else []:
    put(f'gates/workflows/logs/{p.name}', p)
for p in sorted((G / 'wf').glob('*.driver.log')) if (G / 'wf').exists() else []:
    put(f'gates/workflows/drivers/{p.name}', p)
for p in sorted((G / 'out').rglob('*')) if (G / 'out').exists() else []:
    if p.is_file():
        put(f'gates/{p.relative_to(G / "out")}', p)
for f in ('dispatch.txt', 'verify-table.md', 'verify.rc'):
    put(f'gates/{f}', G / f)
for p in sorted((G / 'rc').glob('*.rc')) if (G / 'rc').exists() else []:
    put(f'gates/units/{p.name}', p)
# the tools these receipts came from
for p in [*sorted(S.glob('*.py')), *sorted(S.glob('*.sh')), *sorted((S / 'costs').glob('*')),
          *sorted((S / 'gates').glob('*'))]:
    if p.is_file():
        put(f'tools/{p.relative_to(S)}', p)
(O / 'large.txt').write_text('\n'.join(large) + '\n' if large else 'none\n')
# drop the empty files an earlier collector left, then the index from the files present
for p in O.rglob('*'):
    if p.is_file() and p.stat().st_size == 0:
        p.unlink()
rows = [f'| `{p.relative_to(O)}` | {p.stat().st_size} |' for p in sorted(O.rglob('*')) if p.is_file() and p.name != 'INDEX.md']
(O / 'INDEX.md').write_text('# Receipts index (generated from the files present)\n\n| File | Bytes |\n|---|---:|\n' +
                            '\n'.join(rows) + '\n')
big = [p for p in O.rglob('*') if p.is_file() and p.stat().st_size > 200_000]
hosts = [p for p in O.rglob('*') if p.is_file() and re.search(r'/data-2/|$VALIDATION_STORAGE|$WORKSPACE_HOME', p.read_text(errors='ignore'))]
print('files', len(rows), 'over 200 KB', big, 'with host paths', hosts, 'recorded by digest', len(large))

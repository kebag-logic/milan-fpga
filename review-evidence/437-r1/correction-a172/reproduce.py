"""Reproduce bounded correction evidence at the recorded local candidate."""
import json
import subprocess
import sys
from pathlib import Path
from run import OUT, LANE, run


def main():
    expected = 'b5e6c23e1b9802b5cacbc62db212064d7e429862'
    actual = subprocess.check_output(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], cwd=LANE, text=True).strip()
    assert actual == expected, (actual, expected)
    assert not subprocess.check_output(['rtk', 'proxy', 'git', 'status', '--porcelain'], cwd=LANE)
    tasks = [('preservation', 'preserve.py', []), ('renderer', 'render.py', []),
             ('probes-three-revisions', 'compare_probes.py', []),
             ('consumers', 'consumers.py', ['--assert-correct']),
             ('renderer-consumers', 'render_consumers.py', []),
             ('mutations', 'mutate.py', [])]
    results = []
    for name, file, args in tasks:
        results.append({'name': name, 'exit': run(name, ['python3', '-B', str(OUT / file), *args])})
    for label in ('baseline', 'starting'):
        results.append({'name': 'consumers-' + label,
                        'exit': run('consumers-' + label, ['python3', '-B', str(OUT / 'consumers.py'),
                                     '--scripts', str(OUT / 'snapshots' / label / 'scripts'), '--label', label])})
    results.append({'name': 'gates', 'exit': run('gates', ['python3', '-B', str(OUT / 'gates.py')])})
    results.append({'name': 'emdash-base', 'exit': run('emdash-base', ['python3', '-B', 'scripts/check_em_dash.py',
                    '--base', '52711029f374650dc93830d5ea28e81cb5c8f410'])})
    (OUT / 'reproduction-exits.json').write_text(json.dumps(results, indent=2) + '\n')
    return int(any(row['exit'] for row in results))


if __name__ == '__main__':
    sys.exit(main())

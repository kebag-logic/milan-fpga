#!/usr/bin/env python3
"""Compare the qualification the harness README names with the one the head's installed Arty row regrades to.

usage: python3 -I qualification_pointer.py SOURCE R7_QUALIFICATION R10_QUALIFICATION
"""
import hashlib
import json
import re
import sys
from pathlib import Path


def flat(node, prefix=''):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from flat(value, f'{prefix}/{key}')
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from flat(value, f'{prefix}[{index}]')
    else:
        yield prefix, node


def main(source: Path, r7: Path, r10: Path) -> int:
    readme = (source / 'tb/verilator/ctrl_service_budget/README.md').read_text()
    named = re.search(r"The installed Arty row's qualification is .*?Its published SHA256 is `([0-9a-f]{64})`", readme, re.S)
    print('README names SHA256', named.group(1))
    print('README says:', re.search(r'It records PASS over (\d+) measured cases', readme).group(0))
    for tag, path in (('round-7', r7), ('round-10', r10)):
        print(f'{tag} published-qualification.json SHA256', hashlib.sha256(path.read_bytes()).hexdigest())
    a, b = json.loads(r7.read_text()), json.loads(r10.read_text())
    fa, fb = dict(flat(a['model'])), dict(flat(b['model']))
    for key in sorted(set(fa) | set(fb)):
        if fa.get(key) != fb.get(key):
            print(f'MODEL DIFFERS {key}: round-7 {fa.get(key)} round-10 {fb.get(key)}')
    print('worst_pass round-7', a['worst_pass'], 'round-10', b['worst_pass'])
    print('checks round-10', json.dumps(b['checks']))
    sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
    import arty_grade
    model, findings = arty_grade.inspect(source)
    fm = dict(flat(model))
    print('head arty_grade model equals round-10 qualification model:', fm == fb)
    print('head arty_grade model equals round-7 qualification model (the one README names):', fm == fa)
    print('arty_grade findings:', findings)
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])))

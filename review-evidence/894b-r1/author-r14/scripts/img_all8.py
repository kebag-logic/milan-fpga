"""Hold a run of qimg.sh against a base receipt for every one of the 8 images (ELF and loadable sha256 identical), and
print a receipt; exit 1 on any difference. usage: python3 -I img_all8.py BASE_RECEIPT RUN_OUTPUT LABEL BASE_NAME"""
import re
import sys
from pathlib import Path

lines = lambda t: {m[1]: m[0] for m in re.finditer(r'^((?:fixture|platform)-\dx\d-\dif): .*$', t, re.M)}
dig = lambda l: (re.search(r'elf sha256 (\w+)', l)[1], re.search(r'loadable sha256 (\w+)', l)[1])
base, run = lines(Path(sys.argv[1]).read_text()), lines(Path(sys.argv[2]).read_text())
print(f'# {sys.argv[3]}: all 8 images against {sys.argv[4]}')
bad = []
for name in sorted(base):
    same = name in run and dig(run[name]) == dig(base[name])
    tiles = re.search(r'tiles ([\d.]+)', run.get(name, ''))
    print(f'{name}: {"identical" if same else "CHANGED"} (ELF {dig(run[name])[0][:12] if name in run else "-"}), '
          f'tiles {tiles[1] if tiles else "-"}')
    bad += [] if same else [name]
print('RESULT:', 'CHANGED ' + ', '.join(bad) if bad else 'PASS: all 8 identical')
sys.exit(1 if bad else 0)

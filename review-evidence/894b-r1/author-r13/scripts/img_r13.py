#!/usr/bin/env python3
"""Round 13's image identity: a run of qimg.sh against the 8883d499 receipt. The six 1x1/1if and 8x8/2if images must be
byte-identical (ELF and loadable sha256). Each 8x8/1if image must differ from its 8883d499 image in exactly one
instruction, the hold-off's immediate (`li a3,2026` to `li a3,2027`, SRP_REDECLARE_CS at CTRL_LOOP_TX_MS 75 ms), at the
same address, with every section's size and every other byte identical (objdump -d and -s of both ELFs, compared
section by section). Prints the receipt; exit 1 on anything else.
usage: python3 -I img_r13.py BASE_RECEIPT BASE_DIR RUN_RECEIPT RUN_DIR OBJDUMP"""
import re
import subprocess
import sys
from pathlib import Path

base_rcpt, base_dir, run_rcpt, run_dir, objdump = sys.argv[1:6]
lines = lambda t: {m[1]: m[0] for m in re.finditer(r'^((?:fixture|platform)-\dx\d-\dif): .*$', t, re.M)}
dig = lambda l: (re.search(r'elf sha256 (\w+)', l)[1], re.search(r'loadable sha256 (\w+)', l)[1])
base, run = lines(Path(base_rcpt).read_text()), lines(Path(run_rcpt).read_text())
bad = []
print('# image identity against 8883d499: the six 1x1/1if and 8x8/2if images byte-identical, each 8x8/1if image one '
      'instruction apart')
assert len(base) == 8, sorted(base)


def dump(elf: Path, flag: str) -> list[str]:
    out = subprocess.run([objdump, flag, '-z', str(elf)], capture_output=True, text=True, check=True).stdout
    return [l for l in out.splitlines()[2:] if l.strip()]


for name in sorted(base):
    b, r = dig(base[name]), dig(run.get(name, 'elf sha256 - loadable sha256 -'))
    if '8x8-1if' not in name:
        ok = b == r
        print(f'{name}: {"IDENTICAL" if ok else "DIFFERS"} elf {r[0][:12]} loadable {r[1][:12]}')
        if not ok:
            bad.append(name)
        continue
    print(f'{name}: elf {b[0][:12]} -> {r[0][:12]}, loadable {b[1][:12]} -> {r[1][:12]}')
    elfs = [Path(d) / name / 'image' / 'ctrl_app.elf' for d in (base_dir, run_dir)]
    d0, d1 = (dump(e, '-d') for e in elfs)
    moved = [(x, y) for x, y in zip(d0, d1) if x != y]
    want = len(d0) == len(d1) and len(moved) == 1 and re.search(r'\bli\s+a3,2026$', moved[0][0]) \
        and re.search(r'\bli\s+a3,2027$', moved[0][1]) and moved[0][0].split(':')[0] == moved[0][1].split(':')[0]
    for x, y in moved[:4]:
        print(f'  - {x.strip()}\n  + {y.strip()}')
    print(f'  disassembly: {len(d0)} and {len(d1)} lines, {len(moved)} differing')
    s0, s1 = (dump(e, '-s') for e in elfs)
    sect, sections = None, {}
    for x, y in zip(s0, s1):
        if x.startswith('Contents of section'):
            sect = x.split()[3].rstrip(':')
        elif x != y:
            sections[sect] = sections.get(sect, 0) + 1
    print(f'  contents: {len(s0)} and {len(s1)} lines, differing lines by section {sections or "none"}')
    if not (want and len(s0) == len(s1) and set(sections) <= {'.text'} and sections.get('.text', 0) == 1):
        bad.append(name)
print(f'RESULT: {"FAIL " + ", ".join(bad) if bad else "PASS"}')
sys.exit(1 if bad else 0)

"""Hold one run of qimg.sh (every image at every point) against a base head's receipt: every 1x1 image (one and two
interfaces) and every 8x8/2if image must have the same ELF and loadable sha256 (the round 2 ruling's STOP: a changed
1x1 or 8x8/2if image; round 3 holds them against round 2's final head 184d47ca), and the 8x8/1if platform image must be at most 56.0
RAMB36 (its STOP: the platform image over 56.0). Prints a receipt and exits 1 on a STOP condition.
usage: python3 -I img_check_base.py BASE_RECEIPT RUN_OUTPUT LABEL [BASE_NAME]"""
import re
import sys
from pathlib import Path

FIXED = ('fixture-1x1-1if', 'fixture-1x1-2if', 'fixture-8x8-2if',
         'platform-1x1-1if', 'platform-1x1-2if', 'platform-8x8-2if')
MOST_TILES = 56.0


def lines(text: str) -> dict[str, str]:
    """Each image's line, by its name, from a receipt or a run (comments and diff lines skipped)."""
    return {m[1]: m[0] for m in re.finditer(r'^((?:fixture|platform)-\dx\d-\dif): .*$', text, re.M)}


def digest(line: str) -> tuple[str, str]:
    """The ELF's and the loadable bytes' sha256 of one line."""
    return re.search(r'elf sha256 (\w+)', line)[1], re.search(r'loadable sha256 (\w+)', line)[1]


start, run, label = lines(Path(sys.argv[1]).read_text()), lines(Path(sys.argv[2]).read_text()), sys.argv[3]
base = sys.argv[4] if len(sys.argv) > 4 else 'the start head'
stop = []
print(f'# {label}: every image against {base}')
for name in sorted(run):
    line = run[name]
    rc = re.search(r': rc (\d+)', line)[1]
    if rc != '0':
        stop.append(f'{name}: rc {rc}')
    tiles = re.search(r'tiles ([\d.]+)', line)
    if name in FIXED:
        same = digest(line) == digest(start[name])
        print(f'{name}: {"identical" if same else "CHANGED"} (ELF {digest(line)[0][:12]}, loadable '
              f'{digest(line)[1][:12]}), tiles {tiles[1] if tiles else "-"}')
        stop += [] if same else [f'{name} changed']
    else:
        moved = 'unchanged' if digest(line) == digest(start[name]) else 'moved'
        print(f'{name}: {moved} from the start (ELF {digest(line)[0][:12]}), tiles {tiles[1] if tiles else "-"}'
              + (f', at most {MOST_TILES}' if name == 'platform-8x8-1if' else ''))
        if name == 'platform-8x8-1if' and (tiles is None or float(tiles[1]) > MOST_TILES):
            stop.append(f'{name}: {tiles[1] if tiles else "no"} tiles, over {MOST_TILES}')
missing = sorted(set(start) - set(run))
stop += [f'{name} not built' for name in missing]
print('RESULT:', 'STOP ' + '; '.join(stop) if stop else 'PASS: every fixed image identical, platform-8x8-1if within 56.0')
sys.exit(1 if stop else 0)

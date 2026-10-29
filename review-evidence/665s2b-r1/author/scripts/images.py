#!/usr/bin/env python3
"""Scratch: link the split image at the four points with ctrl_srp_image.py (--with-aecp --layout split), at a base
tree and a head tree, and compare their planned block RAM against ruling 6425357821's caps: 56 RAMB36 at every
point, 57.5 at 8x8 with two interfaces. A tree whose ctrl_srp_image.py takes --ledgered-point (contract 2.3's
merge) names the ledgered point there, as the harness does; a tree from before it has no override to name.

usage: images.py OUT BASE_TREE HEAD_TREE LIBC COMPILER_RT
Writes OUT/<label>-<shape>-if<n>-size.json (the builder's own report) and OUT/images.md; exits 1 over a cap."""
import json
import subprocess
import sys
from pathlib import Path

POINTS = (('endstation_ax7101_1x1_tdm8', 1), ('endstation_ax7101_1x1_tdm8', 2),
          ('endstation_ax7101_8x8', 1), ('endstation_ax7101_8x8', 2))
CAP = {('endstation_ax7101_8x8', 2): 57.5}


def tiles(split: dict) -> float:
    return sum(r['RAMB36'] + r['RAMB18'] / 2 for r in (split['rom'], split['sram']))


def link(tree: Path, shape: str, n: int, out: Path, libc: str, crt: str) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, '-B', str(tree / 'sw/firmware/ctrl/test/ctrl_srp_image.py'),
           '--config', str(tree / 'configs' / f'{shape}.yaml'), '--interfaces', str(n), '--with-aecp',
           '--layout', 'split', '--output', str(out), '--libc', libc, '--compiler-runtime', crt]
    if (shape, n) in CAP and '--ledgered-point' in (tree / 'sw/firmware/ctrl/test/ctrl_srp_image.py').read_text():
        cmd += ['--ledgered-point', '8x8-two-interfaces']
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f'link failed at {tree} {shape} if{n}:\n{r.stderr[-2000:]}')
    return json.loads((out / 'size.json').read_text())


def main() -> int:
    out, base, head = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    libc, crt = sys.argv[4], sys.argv[5]
    rows = ['| Point | .text base / head | rom bytes base / head (delta) | sram bytes base / head (delta) | '
            'planned tiles base / head | cap |', '|---|---:|---:|---:|---:|---:|']
    over = 0
    for shape, n in POINTS:
        got = {}
        for label, tree in (('base', base), ('head', head)):
            report = link(tree, shape, n, out / 'work' / f'{label}-{shape}-if{n}', libc, crt)
            (out / f'{label}-{shape}-if{n}-size.json').write_text(json.dumps(report, indent=1) + '\n')
            got[label] = report
        b, h = got['base'], got['head']
        cap = CAP.get((shape, n), 56)
        t = (tiles(b['split']), tiles(h['split']))
        over += t[1] > cap
        rb, rh = b['split']['rom']['bytes'], h['split']['rom']['bytes']
        sb, sh = b['split']['sram']['bytes'], h['split']['sram']['bytes']
        rows.append(f"| {shape.removeprefix('endstation_ax7101_')}, {n} interface{'s' if n > 1 else ''} | "
                    f"{b['sections']['.text']:,} / {h['sections']['.text']:,} | {rb:,} / {rh:,} ({rh - rb:+,}) | "
                    f"{sb:,} / {sh:,} ({sh - sb:+,}) | {t[0]} / {t[1]} | {cap} |")
    (out / 'images.md').write_text('\n'.join(rows) + '\n')
    print('\n'.join(rows))
    print(f'points over their cap at the head: {over}')
    return 1 if over else 0


if __name__ == '__main__':
    sys.exit(main())

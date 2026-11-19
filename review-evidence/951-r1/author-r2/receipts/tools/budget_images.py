#!/usr/bin/env python3
"""budget_images.py CLONE OUT: the CPU budget harness's twelve images (run.POINTS x the four arms) as build.build links
them before it builds the SoC model: build.flash_map once per shape (the stand-in and mapped SoC exports), then
build.firmware at each point and arm on that map. Writes OUT/<point>/<arm>/image/ctrl_app.elf and OUT/hashes.txt in
the train's format (point arm sha256). Read-only on CLONE apart from the builder's own ignored outputs."""
import concurrent.futures
import hashlib
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
harness = clone / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(harness))
import build  # noqa: E402
import run  # noqa: E402
import split_soc  # noqa: E402

assert build.ROOT == clone, build.ROOT
ARMS = ('none', 'answering-every-port', 'answering-ports', 'valid-destinations')
POINTS = ('1x1', '8x8-1if', '8x8')
maps = {}
for point in POINTS:
    shape, _ = run.POINTS[point]
    if shape not in maps:
        maps[shape] = build.flash_map(out / f'map-{shape}' / split_soc.FLASH_MAP, shape)
        print(f'flash map {shape}: {maps[shape]}', flush=True)


def link(point_arm):
    point, arm = point_arm
    shape, n_if = run.POINTS[point]
    elf = build.firmware(out / point / arm, shape, n_if, variant=arm, flash_map=maps[shape])
    return point, arm, hashlib.sha256(elf.read_bytes()).hexdigest()


with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    rows = list(pool.map(link, [(p, a) for p in POINTS for a in ARMS]))
(out / 'hashes.txt').write_text(''.join(f'{p} {a} {h}\n' for p, a, h in rows))
print((out / 'hashes.txt').read_text(), end='')

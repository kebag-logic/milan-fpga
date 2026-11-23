#!/usr/bin/env python3
"""Build the CPU budget harness's split images (no SoC, no native model) and print each ctrl_app.elf's sha256.

usage: budget_images.py CHECKOUT OUT POINT:VARIANT [POINT:VARIANT ...]
Uses the checkout's own tb/verilator/ctrl_service_budget/build.py: flash_map once per shape, then firmware() per arm,
exactly as build.build links the image (the image does not depend on the core options).
"""
import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
wanted = [a.split(':', 1) for a in sys.argv[3:]]
harness = clone / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(harness))
import build as builder  # noqa: E402
import run  # noqa: E402
import split_soc  # noqa: E402

maps = {}
for point, _ in wanted:
    shape, _n = run.POINTS[point]
    if shape not in maps:
        maps[shape] = None


def one_map(shape):
    return shape, builder.flash_map(out / f'map-{shape}' / split_soc.FLASH_MAP, shape)


with ThreadPoolExecutor(len(maps)) as ex:
    maps = dict(ex.map(one_map, list(maps)))


def one(pv):
    point, variant = pv
    shape, n_if = run.POINTS[point]
    elf = builder.firmware(out / f'{point}-{variant}', shape, n_if, 'none', variant, maps[shape])
    return point, variant, hashlib.sha256(elf.read_bytes()).hexdigest()


with ThreadPoolExecutor(8) as ex:
    for point, variant, digest in ex.map(one, wanted):
        print(f'{point} {variant} {digest}', flush=True)

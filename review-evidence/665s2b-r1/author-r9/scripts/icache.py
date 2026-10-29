#!/usr/bin/env python3
"""Scratch: the split CPU's instruction cache, modelled on committed-PC traces, under the link map's layout and others.

usage: icache.py MAP TRACE... [--hot-out FILE]

- MAP: ctrl_app.map of the traced image; its text input sections (-ffunction-sections, so one function each) are the
  units a layout places. Every one is 4-byte aligned (readelf of the objects).
- TRACE: a harness log run with BUDGET_TRACE_AFTER/BUDGET_TRACE_PCS: its PC lines (each committed PC, in order) and
  FETCH lines (each line refill the cache made, in order).
The model: 4 KiB direct mapped, 64-byte lines (milan_soc's fetch L1, 64 sets of 1 way), a miss on each committed PC
whose line is not held. The model's misses at the link map's layout are checked against the trace's FETCH count.
Layouts: the link map's (as linked); and the traced functions first, contiguous, in the order each first ran in the
traces (the hot section), then every other function in its linked order."""
import argparse
import re
from bisect import bisect_right
from pathlib import Path

LINE, SETS = 64, 64


def sections(mapfile: Path) -> list[tuple[int, int, str]]:
    """(start, size, label) of each linked .text input section, by address; label is object:section."""
    text = mapfile.read_text()
    body = text[text.index('Linker script and memory map'):]
    rows = re.findall(r'^ (\.text(?:\.\S+)?)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\S+)$', body, re.M)
    out = [(int(a, 16), int(s, 16), f'{Path(o).name}:{n}') for n, a, s, o in rows if int(s, 16)]
    return sorted(out)


def trace(path: Path) -> tuple[list[int], int]:
    pcs, fetches = [], 0
    for line in path.read_text().splitlines():
        if line.startswith('PC '):
            pcs.append(int(line.split()[2], 16))
        elif line.startswith('FETCH '):
            fetches += 1
    return pcs, fetches


def misses(pcs: list[int], remap) -> int:
    held = [-1] * SETS
    n = 0
    last = -1
    for pc in pcs:
        line = remap(pc) // LINE
        if line == last:
            continue
        last = line
        s = line % SETS
        if held[s] != line:
            held[s] = line
            n += 1
    return n


def layout(secs, order: list[int]):
    """A remap of PCs for the sections placed in `order` (indices into secs) from the first section's address."""
    base = secs[0][0]
    starts = [s[0] for s in secs]
    new = [0] * len(secs)
    at = base
    for k in order:
        at = (at + 3) & ~3
        new[k] = at
        at += secs[k][1]

    def remap(pc: int) -> int:
        k = bisect_right(starts, pc) - 1
        if k < 0 or pc >= secs[k][0] + secs[k][1]:
            return pc
        return new[k] + (pc - secs[k][0])
    return remap, at - base


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('map', type=Path)
    ap.add_argument('traces', type=Path, nargs='+')
    ap.add_argument('--hot-out', type=Path)
    args = ap.parse_args()
    secs = sections(args.map)
    starts = [s[0] for s in secs]
    loaded = {t: trace(t) for t in args.traces}
    first: dict[int, int] = {}
    order_seen = []
    for t, (pcs, _) in loaded.items():
        for pc in pcs:
            k = bisect_right(starts, pc) - 1
            if k >= 0 and pc < secs[k][0] + secs[k][1] and k not in first:
                first[k] = len(order_seen)
                order_seen.append(k)
    hot = order_seen
    cold = [k for k in range(len(secs)) if k not in first]
    hot_bytes = sum(secs[k][1] for k in hot)
    print(f'{len(secs)} text sections, {sum(s[1] for s in secs)} bytes; {len(hot)} ran in the traces, {hot_bytes} bytes')
    ident = lambda pc: pc
    hot_first, _ = layout(secs, hot + cold)
    for t, (pcs, fetches) in loaded.items():
        a, b = misses(pcs, ident), misses(pcs, hot_first)
        print(f'{t.name}: {len(pcs)} PCs; refills measured {fetches}; modelled as linked {a}; hot section first {b} '
              f'({100 * (b - a) / a:+.1f} %)')
    if args.hot_out:
        args.hot_out.write_text(''.join(f'{secs[k][2]}\n' for k in hot))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

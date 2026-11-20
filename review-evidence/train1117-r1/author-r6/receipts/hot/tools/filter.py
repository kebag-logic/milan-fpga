#!/usr/bin/env python3
"""filter.py ORDER OUT MAP...: #665's ruling of 2026-11-18, item 1, on a learned order (order.py): keep a traced entry
only if its section links in every image the list serves, read from each image's link map (its linked input sections,
not its discarded ones); nothing else is dropped, added or reordered. Writes the kept order to OUT and prints each
dropped entry with the images that lack it."""
import re
import sys
from pathlib import Path

SECTION = re.compile(r"^ \.text\.(\S+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)\s+\S*/"
                     r"(?:\d+-([A-Za-z0-9_]+)\.o|([A-Za-z0-9_.]+\.a)\(([A-Za-z0-9_]+)\.o\))$", re.M)


def linked(path: Path) -> set[tuple[str, str]]:
    """The `<stem> <function>` entries whose `.text.<function>` section the map links (its memory map part)."""
    text = path.read_text()
    body = text[text.index('Linker script and memory map'):]
    return {(stem or f'{archive}:{member}', name) for name, _, size, stem, archive, member in SECTION.findall(body)}


order = [tuple(line.split()) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
maps = [Path(m) for m in sys.argv[3:]]
have = {m: linked(m) for m in maps}
kept, dropped = [], []
for e in order:
    lacking = [m for m in maps if e not in have[m]]
    (dropped if lacking else kept).append((e, lacking))
Path(sys.argv[2]).write_text(''.join(f'{s} {f}\n' for (s, f), _ in kept))
print(f'{len(order)} traced, {len(kept)} kept, {len(dropped)} dropped, over {len(maps)} images')
for (s, f), lacking in dropped:
    print(f'DROPPED {s} {f}: lacking in {len(lacking)} of {len(maps)}: ' + ', '.join(str(m) for m in lacking))

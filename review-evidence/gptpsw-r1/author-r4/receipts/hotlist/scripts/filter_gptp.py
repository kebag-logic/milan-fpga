#!/usr/bin/env python3
"""filter_gptp.py ORDER OUT MAPDIR: the optimisation line's filter.py (#665's ruling of 2026-11-18, item 1) on a
learned order, over every link map under MAPDIR, with the scope ctrl_hot.py's LINKED rule has (#884): an entry of
gptp.c or gptp_mbx.c is kept only if its section links in every image built with gPTP (the image of a build
named *-gptp; its stand-in and mapped images are plain),
every other entry only if it links in every image; nothing else is dropped, added or reordered. Writes the kept order
to OUT and prints each dropped entry with how many images lack it and which."""
import re
import sys
from pathlib import Path

SECTION = re.compile(r"^ \.text\.(\S+)\s+(0x[0-9a-f]+)\s+(0x[0-9a-f]+)\s+\S*/"
                     r"(?:\d+-([A-Za-z0-9_]+)\.o|([A-Za-z0-9_.]+\.a)\(([A-Za-z0-9_]+)\.o\))$", re.M)
GPTP_OBJECTS = {"gptp", "gptp_mbx"}


def linked(path: Path) -> set[tuple[str, str]]:
    """The `<stem> <function>` entries whose `.text.<function>` section the map links (its memory map part)."""
    text = path.read_text()
    body = text[text.index('Linker script and memory map'):]
    return {(stem or f'{archive}:{member}', name) for name, _, size, stem, archive, member in SECTION.findall(body)}


order = [tuple(line.split()) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
maps = sorted(Path(sys.argv[3]).glob('*/**/ctrl_app.map'))
# a gPTP build's own image (<build>-gptp/image/); its SoC plan's stand-in and mapped images are the shape's
# one-interface image without gPTP (build.flash_map's firmware calls), so they are plain images
gptp = [m for m in maps if m.relative_to(sys.argv[3]).parts[0].endswith('-gptp')
        and m.relative_to(sys.argv[3]).parts[1:] == ('image', 'ctrl_app.map')]
have = {m: linked(m) for m in maps}
for m in maps:  # the scope's premise: an image without gPTP links none of its objects' sections
    if m not in gptp and any(s in GPTP_OBJECTS for s, _ in have[m]):
        sys.exit(f'{m} is built without gPTP, yet links a gPTP section')
kept, dropped = [], []
for e in order:
    served = gptp if e[0] in GPTP_OBJECTS else maps
    lacking = [m for m in served if e not in have[m]]
    (dropped if lacking else kept).append((e, lacking, len(served)))
Path(sys.argv[2]).write_text(''.join(f'{s} {f}\n' for (s, f), _, _ in kept))
print(f'{len(order)} traced, {len(kept)} kept, {len(dropped)} dropped, over {len(maps)} images ({len(gptp)} with gPTP)')
for (s, f), lacking, n in dropped:
    print(f'DROPPED {s} {f}: lacking in {len(lacking)} of {n}: '
          + ', '.join(str(m.relative_to(sys.argv[3])) for m in lacking))

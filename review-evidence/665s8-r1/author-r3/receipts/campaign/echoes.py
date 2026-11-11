#!/usr/bin/env python3
"""echoes.py <run dir>...: each loaded run's echo evidence (scratch tool): the offers queued before and after
interface 0's first ANNOUNCE left, the echoes they skipped and found (each load's echo items from the stimulus's
defload lines), and the MAAP frames sent by type."""
import sys
from pathlib import Path

ANNOUNCE = 3


def main():
    for run in map(Path, sys.argv[1:]):
        echo_items = {}
        for line in (run / 'wire.txt').read_text().splitlines():
            w = line.split()
            if w and w[0] == 'defload':
                echo_items[w[1]] = sum('/echo/' in item for item in w[2:])
        announced = False
        sides = {False: dict(offers=0, with_echoes=0, skipped=0, found=0),
                 True: dict(offers=0, with_echoes=0, skipped=0, found=0)}
        maap = {}
        for line in (run / 'wire.log').open(errors='replace'):
            w = line.split()
            if not w:
                continue
            if w[0] == 'TXW':
                data = bytes.fromhex(w[4])
                if data[12:15] == b'\x22\xf0\xfe':
                    kind = data[15] & 0x0F
                    maap[kind] = maap.get(kind, 0) + 1
                    announced = announced or kind == ANNOUNCE
            elif w[0] == 'LOAD' and len(w) == 8:
                side = sides[announced]
                items, skipped = echo_items[w[2]], int(w[4])
                side['offers'] += 1
                side['with_echoes'] += items > 0
                side['skipped'] += skipped
                side['found'] += items - skipped
        print(f'{run.name}: before the first ANNOUNCE {sides[False]}; after it {sides[True]}; MAAP frames sent by '
              f'type {dict(sorted(maap.items()))} (1 PROBE, 2 DEFEND, 3 ANNOUNCE)')


if __name__ == '__main__':
    main()

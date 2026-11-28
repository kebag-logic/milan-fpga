#!/usr/bin/env python3
"""The firmware boundary gate's listing rule (ctrl_configs.held's text loop), applied to the checkout without a capture.

Every file that names the firmware's tree and is a program must be a known builder, or be listed in PART_OF, OUTSIDE or
SUITES. This prints each program the head leaves unlisted; the hosted `firmware-boundary` job refuses on the same rule.

usage: python3 -B probe_boundary_listing.py SOURCE
"""
import sys
from pathlib import Path


def main(source: Path) -> int:
    sys.path.insert(0, str(source / 'sw/firmware/ctrl/test'))
    import ctrl_configs as cc
    names = {b.path for b in cc.BUILDERS}
    unlisted = []
    texts = cc.builder_texts()
    for path, text in texts.items():
        name = cc.rel(path)
        if name in names or name in cc.OUTSIDE or name in cc.SUITES:
            continue
        if cc.program(path, text) and name not in cc.PART_OF:
            unlisted.append(name)
    print(f'{len(texts)} files name the firmware tree; programs listed nowhere: {len(unlisted)}')
    for name in unlisted:
        print('UNLISTED PROGRAM', name)
    return int(bool(unlisted))


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))

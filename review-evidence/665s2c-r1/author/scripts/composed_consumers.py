#!/usr/bin/env python3
"""The consumers of each arm's composed maximum pass and of its longest released window's pass.

Reads each arm's graded results.json (the composed_maximum record) and the named group's graded
JSON (its composed window's longest pass and that pass's cycles by module); nothing is measured.
usage: composed_consumers.py REGRADE ARM..."""
import json
import sys
from pathlib import Path

SHARES = (('memset and memcpy', ('rt_memset', 'rt_memcpy')), ('the mailbox driver', ('mbx',)),
          ('AECP, ACMP and mrp_mad', ('aecp', 'acmp', 'mrp_mad')),
          ('software arithmetic', ('rt_umodsi3', 'rt_udivsi3', 'rt_lshrdi3', 'rt_clzsi2', 'rt_mulsi3', 'rt_divsi3',
                                   'rt_modsi3', 'rt_ashldi3', 'rt_ashrdi3', 'rt_muldi3', 'rt_udivdi3', 'rt_umoddi3')))
root = Path(sys.argv[1])
for arm in sys.argv[2:]:
    record = json.loads((root / arm / 'results.json').read_text())['composed_maximum']
    for label, entry in (('composed maximum', record), ('released windows only', record.get('released'))):
        if not entry:
            print(f'{arm} {label}: none')
            continue
        window = json.loads((root / arm / f"{entry['group']}.json").read_text())['passes']['composed']
        assert window['cycles'] == entry['cycles'], (arm, label)
        mods = window['modules']
        top = sorted(mods.items(), key=lambda kv: -kv[1])[:6]
        shares = '; '.join(f"{name} {sum(mods.get(m, 0) for m in keys) / entry['cycles']:.1%}" for name, keys in SHARES)
        print(f"{arm} {label}: {entry['cycles']:,} ({entry['ms']:.2f} ms), {entry['group']}"
              f"{', a lower bound' if label == 'composed maximum' and record['lower_bound'] else ''}; "
              f"top: {', '.join(f'{k} {v:,}' for k, v in top)}; shares: {shares}")

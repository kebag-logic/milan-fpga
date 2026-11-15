#!/usr/bin/env python3
"""Each AECP record handler's span (aecp_mbx:frame SPAN) in a harness log, by the probe whose receive preceded it
(the RXS line's name). usage: record_spans.py LOG..."""
import sys
for path in sys.argv[1:]:
    probe, rows = None, []
    for line in open(path, errors='replace'):
        p = line.split()
        if p and p[0] == 'RXS' and len(p) > 4:
            probe = p[4]
        elif p and p[0] == 'SPAN' and p[-1] == 'aecp_mbx:frame':
            rows.append((probe, int(p[3])))
    print(f'{path.split("/")[-4]}/{path.split("/")[-1]}: ' + ', '.join(f'{n} {c}' for n, c in rows))

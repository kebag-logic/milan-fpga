#!/usr/bin/env python3
"""The round of THE RETRY that built GET_AS_PATH's answered notice in the scratch arm (cl-path.diff): every
ctrl_loop:round_of SPAN holding the entry reads (mbx_win_read SPANs from the call site ENTRY_SITE), with the notices it
built (aecp:finish CALLs) and its attempts (aecp_command CALLs), and the cost round_grade.py admits it at:
AECP_ROUND_COLD_US + n x AECP_NOTICE_US + (attempts - n) x AECP_ATTEMPT_US, 1x1/1if (85, 255, 34 us at 100 MHz).
usage: path_round.py ENTRY_SITE LOG..."""
import sys
site, logs = sys.argv[1], sys.argv[2:]
for path in logs:
    spans, calls, reads, counts = [], [], [], []
    for line in open(path, errors='replace'):
        p = line.split()
        if not p:
            continue
        if p[0] == 'SPAN' and p[-1] == 'ctrl_loop:round_of':
            spans.append((int(p[2]), int(p[2]) + int(p[3])))
        elif p[0] == 'CALL' and p[-1] in ('aecp_command', 'aecp:finish'):
            calls.append((int(p[2]), p[-1]))
        elif p[0] == 'SPAN' and p[-1] == 'mbx_win_read':
            (reads if p[4] == site else counts).append((int(p[2]), int(p[3])))
    print(f'{path.split("/")[-1]}: {len(reads)} entry reads ({sum(c for _, c in reads)} cycles, at most '
          f'{max((c for _, c in reads), default=0)}), {len(counts)} count reads (at most {max((c for _, c in counts), default=0)})')
    for s, e in spans:
        inside = [c for t, c in reads if s <= t <= e]
        if inside:
            n = sum(1 for t, k in calls if s <= t <= e and k == 'aecp:finish')
            a = sum(1 for t, k in calls if s <= t <= e and k == 'aecp_command')
            admitted = 8500 + n * 25500 + (a - n) * 3400
            print(f'  round {e - s} CPU cycles: {len(inside)} entry reads ({sum(inside)} cycles), {n} notices, '
                  f'{a - n} refused attempts; admitted at {admitted}; margin {admitted - (e - s)}')

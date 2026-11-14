"""Round 1's SRP slices at 8x8/1if, read from its logs with the harness's own parser (grade.parse): for every ordinary
pass that took SRP records, the last record's start and end from the pass's start, in CPU cycles. The slice starts a
record only while it has CTRL_LOOP_SRP_UNIT_US left (ctrl_loop.c), so a slice's length is at most
(slice - unit) + the record as the loop charges it (its take before srp_mbx:receive, and the handler).
usage: python3 -I srp_slices.py <harness-dir> <builds-dir> <leg>..."""
import sys
from bisect import bisect_left
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import grade  # noqa: E402

builds = Path(sys.argv[2])
legs = sys.argv[3:]
SYS = CPU = 100_000_000
worst_len = (0, '')
worst_start = (0, '')
worst_charged = (0, '')
over = 0
for leg in legs:
    for log_path in sorted((builds / leg / 'results').glob('*.log')):
        log = grade.parse(log_path.read_text(), SYS, CPU)
        spans = sorted((int(r[1]), int(r[2])) for k, *r in log.traced if k == 'SPAN' and r[4] == 'srp_mbx:receive')
        starts = [s for s, _ in spans]
        for p in log.passes:
            inside = spans[bisect_left(starts, p.start_cpu):bisect_left(starts, p.start_cpu + p.cycles)]
            if not inside:
                continue
            last_start, last_len = inside[-1]
            off = last_start - p.start_cpu
            length = last_start + last_len - p.start_cpu
            # the record the loop started last: every record but the first in the slice began after a check
            prev_end = inside[-2][0] + inside[-2][1] - p.start_cpu if len(inside) > 1 else None
            charged = length - prev_end if prev_end is not None else 0
            where = f'{leg}/{log_path.stem} pass {p.index}'
            over += length > 147_500
            if length > worst_len[0]:
                worst_len = (length, f'{where}: last record at +{off:,} for {last_len:,}, {len(inside)} records')
            if off > worst_start[0]:
                worst_start = (off, where)
            if charged > worst_charged[0]:
                worst_charged = (charged, f'{where}: from the previous record\'s end to the last\'s end')
print('# legs:', ' '.join(legs))
print(f'longest SRP slice {worst_len[0]:,} CPU cycles: {worst_len[1]}')
print(f'latest last-record start {worst_start[0]:,} CPU cycles from its pass\'s start: {worst_start[1]}')
print(f'heaviest record as the loop charges it (previous end to its end) {worst_charged[0]:,}: {worst_charged[1]}')
print(f'slices over 147,500: {over}')

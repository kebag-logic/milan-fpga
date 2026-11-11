# Recompute, from each published results.json, the frame equation the round 3 ruling item 4 names:
# delivered load frames + 4 per draw == SUMMARY rx_frames + bench_rx. Also prints each load's skip count
# and the run's findings. Usage: python3 -I frame_equation.py <results.json>...
import json, sys
bad = 0
for path in sys.argv[1:]:
    d = json.load(open(path))
    words = dict(w.split('=', 1) for w in d['summary'].split()[1:])
    received = int(words['rx_frames']) + int(words['bench_rx'])
    delivered = sum(t['delivered_frames'] for t in d['load'].values())
    ok = delivered + 4 * d['draws'] == received
    bad += not ok
    skipped = {k: t['skipped'] for k, t in d['load'].items()}
    print(f"{path.split('receipts/')[-1]}: draws {d['draws']} delivered {delivered} + 4x{d['draws']} = "
          f"{delivered + 4 * d['draws']} vs received {received}: {'OK' if ok else 'MISMATCH'}; skipped {skipped}; "
          f"findings {len(d['findings'])}")
print('mismatches', bad)

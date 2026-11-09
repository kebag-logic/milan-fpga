"""book_shards.py <n>: n successive pick8 results, each taken as booked before the next pick (cpu_ranges.py's own
policy; a plain repeated `pick` returns the same range until a unit holds it). Prints one range per line."""
import sys

sys.path.insert(0, '$HOME/milan-fpga-management/2026-09-23')
import cpu_ranges  # noqa: E402

n = int(sys.argv[1])
taken = cpu_ranges.busy()
picked = []
for _ in range(n):
    r = cpu_ranges.pick8(taken)
    if not r:
        raise SystemExit(f'only {len(picked)} free: {picked}')
    picked.append(r)
    taken |= cpu_ranges.expand(r)
print('\n'.join(picked))

"""pick4.py: four disjoint 8-wide CPU ranges, each what `cpu_ranges.py pick` would print once the ranges before it
are booked (the module's own pick8 over the live busy set plus the earlier picks). Exits 1 if fewer than four."""
import sys
sys.path.insert(0, "$HOME/milan-fpga-management/2026-09-23")
import cpu_ranges

taken = cpu_ranges.busy()
picks = []
for _ in range(4):
    r = cpu_ranges.pick8(taken)
    if not r:
        sys.exit(f"only {len(picks)} free: {picks}")
    picks.append(r)
    taken |= cpu_ranges.expand(r)
print(" ".join(picks))

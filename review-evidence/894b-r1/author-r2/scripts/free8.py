"""The free 8-wide aligned CPU ranges by the shared picker's own busy set (cpu_ranges.busy), none while a release hold
collects CPUs (cpu_ranges.p0_acquiring). usage: python3 free8.py"""
import sys
sys.path.insert(0, '$MANAGEMENT/2026-09-23')
import cpu_ranges
print(' '.join([] if cpu_ranges.p0_acquiring() else cpu_ranges.free_ranges(8)))

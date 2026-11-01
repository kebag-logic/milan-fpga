#!/usr/bin/env python3
"""Run the witnesses of probe_fewer_bound.py through the author's published
model: its FIFO recursion and its event-exact IEEE 802.1Q-2022 8.6.8.2 credit
simulation, with its own phase-rule function reaching each placement.
Usage: python3 -I crosscheck_published_model.py <path to mixed_stagger.py>
"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("published_model", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
FIXED = {48: 40.325, 96: 32.491}
def report(name, khz, phases):
    r = m.Rate(khz)
    print(f"{name}: {khz} kHz {phases}: fifo wait {float(m.lindley_wait(r, phases, None)):.3f} us; "
          f"event-exact wait {float(m.cbs_sim(r, phases, None)):.3f} us; "
          f"idleSlope {float(m.idle_slope(r, phases, None)):.3f} Mb/s; total with the page's fixed terms "
          f"{float(m.lindley_wait(r, phases, None)) + FIXED[khz]:.3f} us")
r = m.Rate(48); ph = [[] for _ in range(6)]
for n in [1] + [8] * 5 + [1, 1] + [8] * 5 + [1, 1, 1]:
    m.greedy_add(r, ph, n)
print("48 kHz reached with the model's own phase rule at 16 streams:", ph)
six = [[n for n in p if n != 8] for p in ph]
report("six one-channel, phase 0 alone", 48, six)
report("page row, three eight-channel", 48, [[8, 8, 8], [], [], [], [], []])
report("two streams, one eight-channel then one one-channel", 48, [[8], [1], [], [], [], []])
r = m.Rate(96); ph = [[] for _ in range(12)]
for n in [1] + [8] * 11 + [1, 1, 1]:
    m.greedy_add(r, ph, n)
print("96 kHz reached with the model's own phase rule at 15 streams:", ph)
report("four one-channel, phase 0 alone", 96, [[n for n in p if n != 8] for p in ph])

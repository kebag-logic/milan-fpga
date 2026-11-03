"""Probe: legs at LARGEST against LEG_BUDGET, and the 927/926 control, in memory only."""
import sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import ci_litex_legs as m
names = m.inventory()
print("LEG_BUDGET", m.LEG_BUDGET, "=", m.JOB_LIMIT, m.HEADROOM, m.SETUP, m.COLD_VERILATOR, m.SELFTEST)
legs = m.partition(names)
for i, leg in enumerate(legs):
    print("leg", i, sum(m.SECONDS[n] for n in leg), sum(m.LARGEST[n] for n in leg), leg)
for v in (926, 927):
    big = dict(m.LARGEST, test_gptp_tx_timestamp=v)
    try:
        m.partition(names, largest=big); print(v, "accepted")
    except ValueError as e:
        print(v, "refused:", e)
cold = [m.SETUP + m.COLD_VERILATOR + m.SELFTEST + sum(m.LARGEST[n] for n in leg) for leg in legs]
print("cold", cold, "warm", [c - m.COLD_VERILATOR for c in cold], "margins", [m.JOB_LIMIT - c for c in cold])

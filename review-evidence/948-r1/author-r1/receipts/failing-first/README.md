# Failing tests first

Each new test, run against the base RTL (`15168e14`'s, unchanged by `755ed418`), then at the fix.

| File | Test | Base RTL |
|---|---|---|
| `avtp_rxmon-fanout-at-15168e14.log` | `sim_fanout.cpp` as first committed (`f3f4f7a6`), RTL `15168e14` | 176 checks, 91 failures, rc 1 |
| `avtp_rxmon-fanout-final-at-755ed418.log` | `sim_fanout.cpp` at `755ed418` ([FO1]-[FO8]), clean clone | 182 checks, 94 failures |
| `avtp_rxmon-fanout-final-at-base-rtl.log` | the final `sim_fanout.cpp` ([FO1]-[FO10]) on the base RTL, `make fanout` | 239 checks, 118 failures |
| `milan_dp-nxn8-FAN-at-755ed418.txt` | sim_nxn [FAN], window-bound version (`755ed418`), obj_nxn8 | 4017 checks, 11 failures, all [FAN] |
| `milan_dp-nxn8-FAN-acmp-at-base-rtl.txt` | the final sim_nxn [FAN] (ACMP binds, GET_COUNTERS) on the base RTL | 4027 checks, 11 failures, all [FAN] |
| `twin-fanout-at-base-rtl.log` | `twin_split.cpp --fanout` on the base RTL, the split half at 8x8/1if | 8 failed: input 0 counts 0 of 4 beside input 1 |
| `rtl-head.txt` | the first run's head and tools | |

At the fix: 239 of 239, 4027 of 4027, and `fanout: 0 failed` (`../rtl/`, `../twin/`).

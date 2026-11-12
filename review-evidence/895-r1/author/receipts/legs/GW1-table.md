### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

2 of 3 paths and 3 of 5 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (DA gate opens) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.555 (0.606) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (DA gate opens) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 197.019 (197.092) | MISS ceiling | 0 acmp | 2 | 2 |
| range lost (ANNOUNCE conflict) -> Talker Leave | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 199.406 (199.500) | MISS ceiling | 0 maap | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 1996 | 0 | 57,354 (0.574) | fits |
| srp-talker-loss | 641 | 0 | 52,998 (0.530) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 1945 | 20,682 (0.207) | 3,079 (0.031) |
| srp-talker-loss | 615 | 19,551 (0.196) | 3,079 (0.031) |

Longest pass that carries a step: 20,682 CPU cycles (0.207 ms), srp-talker; longest step: 3,079 (0.031 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s0.if0` | 55,550 | 0.555 | 20 | 20 | fits | 35,244 | 5 | 0.895 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s1.if0` | 19,701,867 | 197.019 | 20 | 20 | MISS ceiling | 31,824 | 3 | 0.843 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s0.if0` | 55,550 | 0.555 | 20 | 20 | fits | 35,244 | 5 | 0.895 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s1.if0` | 19,701,867 | 197.019 | 20 | 20 | MISS ceiling | 31,824 | 3 | 0.843 |
| range lost (ANNOUNCE conflict) -> Talker Leave | `srp.talker_loss.if0` | 19,940,599 | 199.406 | 20 | 20 | MISS ceiling | 33,805 | 3 | 0.846 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

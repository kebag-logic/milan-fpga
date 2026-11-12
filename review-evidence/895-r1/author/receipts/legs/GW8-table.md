### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

9 of 11 paths and 16 of 20 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (DA gate opens) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.700 (0.775) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (DA gate opens) | 1 | `srp.talker_declare.s1.if1` (srp-talker) | 0.673 (0.722) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (DA gate opens) | 0 | `srp.talker_declare.s2.if0` (srp-talker) | 194.330 (194.416) | MISS ceiling | 0 acmp | 2 | 2 |
| PROBE_TX -> Talker Advertise (DA gate opens) | 1 | `srp.talker_declare.s3.if1` (srp-talker) | 199.232 (199.282) | MISS ceiling | 0 acmp | 2 | 2 |
| PROBE_TX -> Talker Advertise (DA gate opens) | 0 | `srp.talker_declare.s4.if0` (srp-talker) | 199.096 (199.184) | MISS ceiling | 0 acmp | 2 | 2 |
| PROBE_TX -> Talker Advertise (DA gate opens) | 1 | `srp.talker_declare.s5.if1` (srp-talker) | 149.224 (149.274) | MISS ceiling | 0 acmp | 2 | 2 |
| PROBE_TX -> Talker Advertise (DA gate opens) | 0 | `srp.talker_declare.s6.if0` (srp-talker) | 48.787 (48.895) | MISS ceiling | 0 acmp | 2 | 2 |
| PROBE_TX -> Talker Advertise (DA gate opens) | 1 | `srp.talker_declare.s7.if1` (srp-talker) | 199.063 (199.129) | MISS ceiling | 0 acmp | 2 | 2 |
| PROBE_TX -> Talker Advertise (DA gate opens) | 0 | `srp.talker_declare.s8.if0` (srp-talker) | 198.709 (198.810) | MISS ceiling | 0 acmp | 2 | 2 |
| range lost (ANNOUNCE conflict) -> Talker Leave | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 198.934 (199.077) | MISS ceiling | 0 maap | 1 | 1 |
| range lost (ANNOUNCE conflict) -> Talker Leave | 1 | `srp.talker_loss.if1` (srp-talker-loss) | 198.761 (198.867) | MISS ceiling | 0 maap | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 2173 | 0 | 74,023 (0.740) | fits |
| srp-talker-loss | 807 | 0 | 53,083 (0.531) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 2045 | 35,818 (0.358) | 3,318 (0.033) |
| srp-talker-loss | 735 | 33,032 (0.330) | 3,223 (0.032) |

Longest pass that carries a step: 35,818 CPU cycles (0.358 ms), srp-talker; longest step: 3,318 (0.033 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s0.if0` | 70,021 | 0.700 | 20 | 20 | fits | 44,282 | 5 | 0.929 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s1.if1` | 67,315 | 0.673 | 20 | 20 | fits | 39,719 | 5 | 0.915 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s2.if0` | 19,433,017 | 194.330 | 20 | 20 | MISS ceiling | 36,231 | 3 | 0.895 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s3.if1` | 19,923,172 | 199.232 | 20 | 20 | MISS ceiling | 28,523 | 4 | 0.658 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s4.if0` | 19,909,624 | 199.096 | 20 | 20 | MISS ceiling | 36,420 | 3 | 0.895 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s5.if1` | 14,922,373 | 149.224 | 20 | 20 | MISS ceiling | 25,435 | 4 | 0.796 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s6.if0` | 4,878,662 | 48.787 | 20 | 20 | MISS ceiling | 46,516 | 3 | 0.864 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s7.if1` | 19,906,300 | 199.063 | 20 | 20 | MISS ceiling | 30,169 | 4 | 0.650 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s8.if0` | 19,870,882 | 198.709 | 20 | 20 | MISS ceiling | 38,679 | 4 | 0.873 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s0.if0` | 70,021 | 0.700 | 20 | 20 | fits | 44,282 | 5 | 0.929 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s1.if1` | 67,315 | 0.673 | 20 | 20 | fits | 39,719 | 5 | 0.915 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s2.if0` | 19,433,017 | 194.330 | 20 | 20 | MISS ceiling | 36,231 | 3 | 0.895 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s3.if1` | 19,923,172 | 199.232 | 20 | 20 | MISS ceiling | 28,523 | 4 | 0.658 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s4.if0` | 19,909,624 | 199.096 | 20 | 20 | MISS ceiling | 36,420 | 3 | 0.895 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s5.if1` | 14,922,373 | 149.224 | 20 | 20 | MISS ceiling | 25,435 | 4 | 0.796 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s6.if0` | 4,878,662 | 48.787 | 20 | 20 | MISS ceiling | 46,516 | 3 | 0.864 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s7.if1` | 19,906,300 | 199.063 | 20 | 20 | MISS ceiling | 30,169 | 4 | 0.650 |
| PROBE_TX -> Talker Advertise (DA gate opens) | `srp.talker_declare.s8.if0` | 19,870,882 | 198.709 | 20 | 20 | MISS ceiling | 38,679 | 4 | 0.873 |
| range lost (ANNOUNCE conflict) -> Talker Leave | `srp.talker_loss.if0` | 19,893,395 | 198.934 | 20 | 20 | MISS ceiling | 53,083 | 3 | 0.853 |
| range lost (ANNOUNCE conflict) -> Talker Leave | `srp.talker_loss.if1` | 19,876,094 | 198.761 | 20 | 20 | MISS ceiling | 42,493 | 4 | 0.835 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

Original file: <scratch>/budget/final/vd-8x8-1if/table.md
Original size: 5903 bytes
Original sha256: ab16857d2f50190ed84a2911ceb121ec917b11de79a59f7c5de3f234039d6f11

### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 10 paths and 0 of 19 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.675 (0.709) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 185.434 (185.489) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker) | 189.423 (189.487) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s3.if0` (srp-talker) | 188.671 (188.765) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker) | 179.295 (179.376) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s5.if0` (srp-talker) | 8.694 (8.817) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker) | 189.077 (189.202) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s7.if0` (srp-talker) | 187.464 (187.591) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker) | 182.695 (182.824) | fits | 0 acmp | 2 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 170.374 (170.838) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 33959 | 0 | 92,226 (0.922) | fits |
| srp-talker-loss | 8006 | 0 | 84,103 (0.841) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 2062 | 43,414 (0.434) | 2,754 (0.028) |
| srp-talker-loss | 731 | 39,724 (0.397) | 2,787 (0.028) |

Longest pass that carries a step: 43,414 CPU cycles (0.434 ms), srp-talker; longest step: 2,787 (0.028 ms), srp-talker-loss.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 67,480 | 0.675 | 220 | 220 | fits | 36,813 | 5 | 0.928 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,543,412 | 185.434 | 220 | 220 | fits | 30,254 | 3 | 0.897 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,942,319 | 189.423 | 220 | 220 | fits | 34,067 | 3 | 0.890 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,867,064 | 188.671 | 220 | 220 | fits | 40,678 | 3 | 0.889 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,929,460 | 179.295 | 220 | 220 | fits | 29,184 | 8 | 0.876 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 869,367 | 8.694 | 220 | 220 | fits | 62,760 | 3 | 0.847 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,907,657 | 189.077 | 220 | 220 | fits | 48,171 | 3 | 0.873 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,746,412 | 187.464 | 220 | 220 | fits | 47,762 | 3 | 0.874 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,269,546 | 182.695 | 220 | 220 | fits | 44,265 | 3 | 0.890 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 67,480 | 0.675 | 220 | 220 | fits | 36,813 | 5 | 0.928 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,543,412 | 185.434 | 220 | 220 | fits | 30,254 | 3 | 0.897 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,942,319 | 189.423 | 220 | 220 | fits | 34,067 | 3 | 0.890 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,867,064 | 188.671 | 220 | 220 | fits | 40,678 | 3 | 0.889 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,929,460 | 179.295 | 220 | 220 | fits | 29,184 | 8 | 0.876 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 869,367 | 8.694 | 220 | 220 | fits | 62,760 | 3 | 0.847 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,907,657 | 189.077 | 220 | 220 | fits | 48,171 | 3 | 0.873 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,746,412 | 187.464 | 220 | 220 | fits | 47,762 | 3 | 0.874 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,269,546 | 182.695 | 220 | 220 | fits | 44,265 | 3 | 0.890 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 17,037,366 | 170.374 | 220 | 220 | fits | 84,103 | 3 | 0.820 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `srp-talker`: wait quiet TIMEOUT
- `srp-talker`: wait quiet TIMEOUT
- `srp-talker-loss`: wait quiet TIMEOUT
- `srp-talker-loss`: wait quiet TIMEOUT
- `srp-talker-loss`: wait quiet TIMEOUT

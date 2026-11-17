Original file: <scratch>/budget/final/base-70f4056f/vd-8x8-1if/table.md
Original size: 5713 bytes
Original sha256: d0832beca22bdfd668ab846e3f867656e8a398fe936b83cc67dadfac9bc377b0

### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 10 paths and 0 of 19 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.676 (0.708) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 186.029 (186.076) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker) | 189.426 (189.480) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s3.if0` (srp-talker) | 189.399 (189.484) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker) | 179.612 (179.691) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s5.if0` (srp-talker) | 9.262 (9.376) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker) | 189.178 (189.292) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s7.if0` (srp-talker) | 189.387 (189.502) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker) | 189.261 (189.379) | fits | 0 acmp | 2 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 189.688 (189.856) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 2170 | 0 | 91,604 (0.916) | fits |
| srp-talker-loss | 817 | 0 | 82,920 (0.829) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 2058 | 31,870 (0.319) | 2,392 (0.024) |
| srp-talker-loss | 727 | 30,234 (0.302) | 2,392 (0.024) |

Longest pass that carries a step: 31,870 CPU cycles (0.319 ms), srp-talker; longest step: 2,392 (0.024 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 67,639 | 0.676 | 220 | 220 | fits | 36,819 | 5 | 0.911 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,602,870 | 186.029 | 220 | 220 | fits | 29,675 | 3 | 0.856 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,942,596 | 189.426 | 220 | 220 | fits | 33,192 | 3 | 0.845 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,939,911 | 189.399 | 220 | 220 | fits | 38,357 | 3 | 0.846 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,961,231 | 179.612 | 220 | 220 | fits | 29,276 | 8 | 0.852 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 926,237 | 9.262 | 220 | 220 | fits | 60,755 | 3 | 0.807 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,917,813 | 189.178 | 220 | 220 | fits | 46,640 | 3 | 0.837 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,938,728 | 189.387 | 220 | 220 | fits | 46,204 | 3 | 0.837 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,926,111 | 189.261 | 220 | 220 | fits | 43,207 | 3 | 0.845 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 67,639 | 0.676 | 220 | 220 | fits | 36,819 | 5 | 0.911 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,602,870 | 186.029 | 220 | 220 | fits | 29,675 | 3 | 0.856 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,942,596 | 189.426 | 220 | 220 | fits | 33,192 | 3 | 0.845 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,939,911 | 189.399 | 220 | 220 | fits | 38,357 | 3 | 0.846 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,961,231 | 179.612 | 220 | 220 | fits | 29,276 | 8 | 0.852 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 926,237 | 9.262 | 220 | 220 | fits | 60,755 | 3 | 0.807 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,917,813 | 189.178 | 220 | 220 | fits | 46,640 | 3 | 0.837 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,938,728 | 189.387 | 220 | 220 | fits | 46,204 | 3 | 0.837 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,926,111 | 189.261 | 220 | 220 | fits | 43,207 | 3 | 0.845 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 18,968,843 | 189.688 | 220 | 220 | fits | 82,920 | 3 | 0.763 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

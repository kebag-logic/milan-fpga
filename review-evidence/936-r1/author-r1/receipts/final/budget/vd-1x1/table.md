Original file: <scratch>/budget/final/vd-1x1/table.md
Original size: 2754 bytes
Original sha256: 4c12e772889884dc46eb973f087519bbfefa9353a4022772fdcbc95080408949

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 3 paths and 0 of 5 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.658 (0.728) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 186.953 (187.056) | fits | 0 acmp | 2 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 189.315 (189.431) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 9708 | 0 | 46,428 (0.464) | fits |
| srp-talker-loss | 2027 | 0 | 44,111 (0.441) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 1944 | 29,185 (0.292) | 2,939 (0.029) |
| srp-talker-loss | 613 | 24,501 (0.245) | 2,939 (0.029) |

Longest pass that carries a step: 29,185 CPU cycles (0.292 ms), srp-talker; longest step: 2,939 (0.029 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 65,802 | 0.658 | 220 | 220 | fits | 44,111 | 5 | 0.921 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,695,286 | 186.953 | 220 | 220 | fits | 38,872 | 3 | 0.893 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 65,802 | 0.658 | 220 | 220 | fits | 44,111 | 5 | 0.921 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,695,286 | 186.953 | 220 | 220 | fits | 38,872 | 3 | 0.893 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 18,931,508 | 189.315 | 220 | 220 | fits | 39,937 | 3 | 0.896 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

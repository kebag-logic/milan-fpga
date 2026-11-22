### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 1 paths and 0 of 2 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-master) | 0.197 (0.457) | fits | 0 gptp | 2 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| gptp-slave | 192 | 0 | 76,464 (0.765) | fits |
| gptp-master | 181 | 0 | 68,667 (0.687) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| gptp-slave | 165 | 20,805 (0.208) | 2,530 (0.025) |
| gptp-master | 165 | 20,823 (0.208) | 2,530 (0.025) |

Longest pass that carries a step: 20,823 CPU cycles (0.208 ms), gptp-master; longest step: 2,530 (0.025 ms), gptp-slave.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 19,296 | 0.193 | 10 | 10 | fits | 27,043 | 22 | 0.681 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 19,657 | 0.197 | 10 | 10 | fits | 27,059 | 22 | 0.686 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

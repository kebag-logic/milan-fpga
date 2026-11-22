### 1x1-2if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 1 paths and 0 of 1 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-slave) | 0.174 (0.422) | fits | 0 gptp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 10 ms over 10 passes, 1.000 ms, 100,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| gptp-slave | 205 | 0 | 96,409 (0.964) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| gptp-slave | 165 | 18,328 (0.183) | 2,340 (0.023) |

Longest pass that carries a step: 18,328 CPU cycles (0.183 ms), gptp-slave; longest step: 2,340 (0.023 ms), gptp-slave.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 17,413 | 0.174 | 10 | 10 | fits | 27,735 | 23 | 0.701 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

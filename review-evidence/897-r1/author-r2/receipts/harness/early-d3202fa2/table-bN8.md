### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 45 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.acmp.if0` (notice-burst-0) | 13.098 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-0.held.adp.if1` (notice-burst-0) | 11.159 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-burst-0.held.aecp.if1` (notice-burst-0) | 13.566 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.maap.if0` (notice-burst-0) | 10.561 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-burst-0.held.srp.if1` (notice-burst-0) | 8.730 | fits | 31 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.36.0.if0` (notice-burst-0) | 33.288 (33.656) | fits | 1 events | 40 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-burst-0 | 779 | 0 | 174,776 (1.748) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-burst-0 | 5.252 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.542 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.810 | 62 | 32 | 1 | within |
| notice-burst-0 | 6.100 | 62 | 32 | 1 | within |
| notice-burst-0 | 8.262 | 62 | 32 | 1 | within |
| notice-burst-0 | 13.631 | 62 | 32 | 1 | within |
| notice-burst-0 | 17.322 | 62 | 32 | 1 | within |
| notice-burst-0 | 21.296 | 62 | 32 | 1 | within |
| notice-burst-0 | 21.578 | 62 | 32 | 1 | within |
| notice-burst-0 | 21.867 | 62 | 32 | 1 | within |
| notice-burst-0 | 22.133 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.144 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.422 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.712 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.976 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.324 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.934 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.252 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.537 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.852 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.598 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.886 | 62 | 32 | 1 | within |
| notice-burst-0 | 26.145 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.143 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.410 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.698 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.523 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.866 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.172 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.505 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.956 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.214 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.481 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.769 | 62 | 32 | 1 | within |
| notice-burst-0 | 30.024 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.267 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.525 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.767 | 62 | 32 | 1 | within |
| notice-burst-0 | 32.053 | 62 | 32 | 1 | within |
| notice-burst-0 | 33.288 | 62 | 32 | 1 | within |

Latest: 33.288 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-burst-0 | 311 | 88,448 (0.884) | 40,230 (0.402) |

Longest pass that carries a step: 88,448 CPU cycles (0.884 ms), notice-burst-0; longest step: 40,230 (0.402 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 525,172 | 5.252 | 62 | 66 | fits | 122,686 | 403 | 0.029 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 554,208 | 5.542 | 62 | 66 | fits | 122,686 | 403 | 0.029 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 580,958 | 5.810 | 62 | 66 | fits | 122,686 | 403 | 0.029 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 609,961 | 6.100 | 62 | 66 | fits | 122,686 | 403 | 0.029 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 826,231 | 8.262 | 62 | 66 | fits | 39,818 | 103 | 0.298 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 1,363,136 | 13.631 | 62 | 66 | fits | 42,645 | 102 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 1,732,154 | 17.322 | 62 | 66 | fits | 39,998 | 101 | 0.325 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 2,129,583 | 21.296 | 62 | 66 | fits | 124,179 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 2,157,759 | 21.578 | 62 | 66 | fits | 124,179 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 2,186,678 | 21.867 | 62 | 66 | fits | 124,179 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 2,213,343 | 22.133 | 62 | 66 | fits | 124,179 | 400 | 0.086 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 2,314,425 | 23.144 | 62 | 66 | fits | 122,489 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 2,342,210 | 23.422 | 62 | 66 | fits | 122,489 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 2,371,249 | 23.712 | 62 | 66 | fits | 122,489 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 2,397,612 | 23.976 | 62 | 66 | fits | 122,489 | 400 | 0.073 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 2,532,352 | 25.324 | 62 | 66 | fits | 121,618 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 393,397 | 3.934 | 62 | 66 | fits | 133,234 | 402 | 0.026 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 425,203 | 4.252 | 62 | 66 | fits | 133,234 | 402 | 0.026 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 453,668 | 4.537 | 62 | 66 | fits | 133,234 | 402 | 0.026 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 485,191 | 4.852 | 62 | 66 | fits | 133,234 | 402 | 0.026 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 2,559,812 | 25.598 | 62 | 66 | fits | 121,618 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 2,588,606 | 25.886 | 62 | 66 | fits | 121,618 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 2,614,530 | 26.145 | 62 | 66 | fits | 121,618 | 400 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 2,714,314 | 27.143 | 62 | 66 | fits | 119,727 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 2,741,037 | 27.410 | 62 | 66 | fits | 119,727 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 2,769,829 | 27.698 | 62 | 66 | fits | 119,727 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 252,323 | 2.523 | 62 | 66 | fits | 170,388 | 409 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 286,615 | 2.866 | 62 | 66 | fits | 170,388 | 409 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 317,183 | 3.172 | 62 | 66 | fits | 170,388 | 409 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 350,491 | 3.505 | 62 | 66 | fits | 170,388 | 409 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,795,555 | 27.956 | 62 | 66 | fits | 119,727 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,921,419 | 29.214 | 62 | 66 | fits | 119,104 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,948,138 | 29.481 | 62 | 66 | fits | 119,104 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,976,927 | 29.769 | 62 | 66 | fits | 119,104 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 3,002,430 | 30.024 | 62 | 66 | fits | 119,104 | 400 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 3,126,750 | 31.267 | 62 | 66 | fits | 116,248 | 399 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 3,152,478 | 31.525 | 62 | 66 | fits | 116,248 | 399 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 3,176,662 | 31.767 | 62 | 66 | fits | 116,248 | 399 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 3,205,336 | 32.053 | 62 | 66 | fits | 116,248 | 399 | 0.063 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 3,328,774 | 33.288 | 62 | 66 | fits | 37,274 | 102 | 0.146 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 1,115,858 | 11.159 | 20 | 200 | fits | 161,114 | 150 | 0.528 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,309,825 | 13.098 | 20 | 20 | fits | 174,237 | 114 | 0.526 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 1,356,622 | 13.566 | 20 | 24 | fits | 67,001 | 39 | 0.591 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 1,056,115 | 10.561 | 20 | 50 | fits | 161,114 | 150 | 0.528 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 872,976 | 8.730 | 20 | 20 | fits | 167,593 | 123 | 0.623 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

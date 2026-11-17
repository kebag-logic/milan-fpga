Original file: <scratch>/r4/budget/r4-tn1/results/table.md
Original size: 7922 bytes
Original sha256: 85a84a67af41e38e850986fb69ca223e3c0d8d1bf05e80a5ae59a52c2e02e60c

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 2 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-1.declared.if0` (talker-notice-1) | 6.887 (7.383) | fits | 0 acmp | 8 | 0 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-0.withdrawn.if0` (talker-notice-0) | 5.585 (6.547) | fits | 0 maap | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| talker-notice-0 | 1560 | 0 | 161,568 (1.616) | fits |
| talker-notice-1 | 1559 | 0 | 160,611 (1.606) | fits |
| talker-notice-2 | 1559 | 0 | 156,133 (1.561) | fits |
| talker-notice-3 | 1562 | 0 | 156,133 (1.561) | fits |
| talker-notice-4 | 1565 | 0 | 156,268 (1.563) | fits |
| talker-notice-5 | 1565 | 0 | 156,357 (1.564) | fits |
| talker-notice-6 | 1564 | 0 | 156,297 (1.563) | fits |
| talker-notice-7 | 1564 | 0 | 156,297 (1.563) | fits |

A declared or withdrawn Talker's STREAM_OUTPUT notice, from its event's commit to the last recipient's commit (talker_notice.py; FR_NFR.md 3.4.1):

| Row | Event committed, sys | Last recipient committed, sys | Recipients | ms | Bound ms | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | 300000965 | 300530646 | 16 | 5.297 | 20 | within |
| `talker-notice-0.withdrawn.if0` | 360000955 | 360559486 | 16 | 5.585 | 20 | within |
| `talker-notice-1.declared.if0` | 300100141 | 300788856 | 16 | 6.887 | 20 | within |
| `talker-notice-1.withdrawn.if0` | 360100131 | 360564919 | 16 | 4.648 | 20 | within |
| `talker-notice-2.declared.if0` | 300200141 | 300757136 | 16 | 5.570 | 20 | within |
| `talker-notice-2.withdrawn.if0` | 360200131 | 360723208 | 16 | 5.231 | 20 | within |
| `talker-notice-3.declared.if0` | 300300141 | 300756493 | 16 | 4.564 | 20 | within |
| `talker-notice-3.withdrawn.if0` | 360300131 | 360721440 | 16 | 4.213 | 20 | within |
| `talker-notice-4.declared.if0` | 300400141 | 300831616 | 16 | 4.315 | 20 | within |
| `talker-notice-4.withdrawn.if0` | 360400131 | 360863436 | 16 | 4.633 | 20 | within |
| `talker-notice-5.declared.if0` | 300500141 | 300849003 | 16 | 3.489 | 20 | within |
| `talker-notice-5.withdrawn.if0` | 360500131 | 360878035 | 16 | 3.779 | 20 | within |
| `talker-notice-6.declared.if0` | 300600141 | 300868285 | 16 | 2.681 | 20 | within |
| `talker-notice-6.withdrawn.if0` | 360600131 | 360902162 | 16 | 3.020 | 20 | within |
| `talker-notice-7.declared.if0` | 300700141 | 300904430 | 16 | 2.043 | 20 | within |
| `talker-notice-7.withdrawn.if0` | 360700131 | 360918814 | 16 | 2.187 | 20 | within |

Latest: 6.887 ms, talker-notice-1.declared.if0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| talker-notice-0 | 354 | 100,769 (1.008) | 78,743 (0.787) |
| talker-notice-1 | 354 | 100,769 (1.008) | 78,743 (0.787) |
| talker-notice-2 | 354 | 100,769 (1.008) | 78,743 (0.787) |
| talker-notice-3 | 354 | 100,769 (1.008) | 78,743 (0.787) |
| talker-notice-4 | 354 | 97,137 (0.971) | 78,743 (0.787) |
| talker-notice-5 | 354 | 97,137 (0.971) | 78,743 (0.787) |
| talker-notice-6 | 354 | 97,137 (0.971) | 78,743 (0.787) |
| talker-notice-7 | 354 | 97,137 (0.971) | 78,743 (0.787) |

Longest pass that carries a step: 100,769 CPU cycles (1.008 ms), talker-notice-0; longest step: 78,743 (0.787 ms), talker-notice-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.declared.if0` | 529,681 | 5.297 | 20 | 24 | fits | 32,437 | 52 | 0.535 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.withdrawn.if0` | 558,531 | 5.585 | 20 | 24 | fits | 28,735 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.declared.if0` | 688,715 | 6.887 | 20 | 24 | fits | 28,228 | 52 | 0.485 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.withdrawn.if0` | 464,788 | 4.648 | 20 | 24 | fits | 28,735 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.declared.if0` | 556,995 | 5.570 | 20 | 24 | fits | 29,145 | 52 | 0.502 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.withdrawn.if0` | 523,077 | 5.231 | 20 | 24 | fits | 29,010 | 52 | 0.502 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.declared.if0` | 456,352 | 4.564 | 20 | 24 | fits | 29,145 | 52 | 0.502 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.withdrawn.if0` | 421,309 | 4.213 | 20 | 24 | fits | 29,010 | 52 | 0.502 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.declared.if0` | 431,475 | 4.315 | 20 | 24 | fits | 29,109 | 52 | 0.498 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.withdrawn.if0` | 463,305 | 4.633 | 20 | 24 | fits | 28,974 | 52 | 0.498 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.declared.if0` | 348,862 | 3.489 | 20 | 24 | fits | 29,017 | 52 | 0.500 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.withdrawn.if0` | 377,904 | 3.779 | 20 | 24 | fits | 28,946 | 52 | 0.500 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.declared.if0` | 268,144 | 2.681 | 20 | 24 | fits | 29,017 | 52 | 0.500 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.withdrawn.if0` | 302,031 | 3.020 | 20 | 24 | fits | 28,882 | 52 | 0.500 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.declared.if0` | 204,289 | 2.043 | 20 | 24 | fits | 28,721 | 52 | 0.496 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.withdrawn.if0` | 218,683 | 2.187 | 20 | 24 | fits | 28,659 | 52 | 0.494 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

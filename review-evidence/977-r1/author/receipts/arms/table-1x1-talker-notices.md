### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 2 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-1.declared.if0` (talker-notice-1) | 5.112 (5.683) | fits | 0 acmp | 8 | 0 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-0.withdrawn.if0` (talker-notice-0) | 4.916 (4.950) | fits | 0 maap | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| talker-notice-0 | 2121 | 0 | 150,848 (1.508) | fits |
| talker-notice-1 | 2121 | 0 | 150,178 (1.502) | fits |
| talker-notice-2 | 2120 | 0 | 144,198 (1.442) | fits |
| talker-notice-3 | 2120 | 0 | 144,118 (1.441) | fits |
| talker-notice-4 | 2120 | 0 | 144,325 (1.443) | fits |
| talker-notice-5 | 2120 | 0 | 144,220 (1.442) | fits |
| talker-notice-6 | 2120 | 0 | 144,325 (1.443) | fits |
| talker-notice-7 | 2120 | 0 | 144,140 (1.441) | fits |

A declared or withdrawn Talker's STREAM_OUTPUT notice, from its event's commit to the last recipient's commit (talker_notice.py; FR_NFR.md 3.4.1):

| Row | Event committed, sys | Last recipient committed, sys | Recipients | ms | Bound ms | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | 300000965 | 300454888 | 16 | 4.539 | 20 | within |
| `talker-notice-0.withdrawn.if0` | 360000955 | 360492549 | 16 | 4.916 | 20 | within |
| `talker-notice-1.declared.if0` | 300100141 | 300611297 | 16 | 5.112 | 20 | within |
| `talker-notice-1.withdrawn.if0` | 360100131 | 360505590 | 16 | 4.055 | 20 | within |
| `talker-notice-2.declared.if0` | 300200141 | 300611297 | 16 | 4.112 | 20 | within |
| `talker-notice-2.withdrawn.if0` | 360200131 | 360659512 | 16 | 4.594 | 20 | within |
| `talker-notice-3.declared.if0` | 300300141 | 300681916 | 16 | 3.818 | 20 | within |
| `talker-notice-3.withdrawn.if0` | 360300131 | 360659827 | 16 | 3.597 | 20 | within |
| `talker-notice-4.declared.if0` | 300400141 | 300761132 | 16 | 3.610 | 20 | within |
| `talker-notice-4.withdrawn.if0` | 360400131 | 360779921 | 16 | 3.798 | 20 | within |
| `talker-notice-5.declared.if0` | 300500141 | 300775206 | 16 | 2.751 | 20 | within |
| `talker-notice-5.withdrawn.if0` | 360500131 | 360795246 | 16 | 2.951 | 20 | within |
| `talker-notice-6.declared.if0` | 300600141 | 300788698 | 16 | 1.886 | 20 | within |
| `talker-notice-6.withdrawn.if0` | 360600131 | 360825670 | 16 | 2.255 | 20 | within |
| `talker-notice-7.declared.if0` | 300700141 | 300830806 | 16 | 1.307 | 20 | within |
| `talker-notice-7.withdrawn.if0` | 360700131 | 360839791 | 16 | 1.397 | 20 | within |

Latest: 5.112 ms, talker-notice-1.declared.if0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| talker-notice-0 | 448 | 92,912 (0.929) | 77,965 (0.780) |
| talker-notice-1 | 448 | 92,912 (0.929) | 77,965 (0.780) |
| talker-notice-2 | 448 | 92,912 (0.929) | 77,965 (0.780) |
| talker-notice-3 | 448 | 92,912 (0.929) | 77,965 (0.780) |
| talker-notice-4 | 448 | 92,912 (0.929) | 77,965 (0.780) |
| talker-notice-5 | 448 | 92,912 (0.929) | 77,965 (0.780) |
| talker-notice-6 | 448 | 92,912 (0.929) | 77,965 (0.780) |
| talker-notice-7 | 448 | 92,912 (0.929) | 77,965 (0.780) |

Longest pass that carries a step: 92,912 CPU cycles (0.929 ms), talker-notice-0; longest step: 77,965 (0.780 ms), talker-notice-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.declared.if0` | 453,923 | 4.539 | 20 | 24 | fits | 23,606 | 52 | 0.485 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.withdrawn.if0` | 491,594 | 4.916 | 20 | 24 | fits | 23,237 | 52 | 0.483 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.declared.if0` | 511,156 | 5.112 | 20 | 24 | fits | 23,659 | 52 | 0.489 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.withdrawn.if0` | 405,459 | 4.055 | 20 | 24 | fits | 25,806 | 54 | 0.525 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.declared.if0` | 411,156 | 4.112 | 20 | 24 | fits | 23,659 | 52 | 0.489 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.withdrawn.if0` | 459,381 | 4.594 | 20 | 24 | fits | 23,536 | 52 | 0.492 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.declared.if0` | 381,775 | 3.818 | 20 | 24 | fits | 23,598 | 52 | 0.487 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.withdrawn.if0` | 359,696 | 3.597 | 20 | 24 | fits | 23,536 | 52 | 0.492 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.declared.if0` | 360,991 | 3.610 | 20 | 24 | fits | 23,295 | 52 | 0.474 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.withdrawn.if0` | 379,790 | 3.798 | 20 | 24 | fits | 23,666 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.declared.if0` | 275,065 | 2.751 | 20 | 24 | fits | 23,295 | 52 | 0.476 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.withdrawn.if0` | 295,115 | 2.951 | 20 | 24 | fits | 23,286 | 52 | 0.481 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.declared.if0` | 188,557 | 1.886 | 20 | 24 | fits | 23,248 | 52 | 0.469 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.withdrawn.if0` | 225,539 | 2.255 | 20 | 24 | fits | 23,235 | 52 | 0.478 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.declared.if0` | 130,665 | 1.307 | 20 | 24 | fits | 23,324 | 52 | 0.472 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.withdrawn.if0` | 139,660 | 1.397 | 20 | 24 | fits | 23,235 | 52 | 0.478 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 2 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-0.declared.if0` (talker-notice-0) | 11.958 (12.946) | fits | 0 acmp | 8 | 0 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-0.withdrawn.if0` (talker-notice-0) | 10.447 (10.695) | fits | 0 maap | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| talker-notice-0 | 1466 | 0 | 160,930 (1.609) | fits |
| talker-notice-1 | 1465 | 0 | 161,240 (1.612) | fits |
| talker-notice-2 | 1465 | 0 | 160,671 (1.607) | fits |
| talker-notice-3 | 1466 | 0 | 160,703 (1.607) | fits |
| talker-notice-4 | 1465 | 0 | 160,532 (1.605) | fits |
| talker-notice-5 | 1464 | 0 | 160,703 (1.607) | fits |
| talker-notice-6 | 1464 | 0 | 160,571 (1.606) | fits |
| talker-notice-7 | 1471 | 0 | 160,600 (1.606) | fits |

A declared or withdrawn Talker's STREAM_OUTPUT notice, from its event's commit to the last recipient's commit (talker_notice.py; FR_NFR.md 3.4.1):

| Row | Event committed, sys | Last recipient committed, sys | Recipients | ms | Bound ms | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | 300000965 | 301196758 | 16 | 11.958 | 20 | within |
| `talker-notice-0.withdrawn.if0` | 360000955 | 361045661 | 16 | 10.447 | 20 | within |
| `talker-notice-1.declared.if0` | 300100141 | 301140140 | 16 | 10.400 | 20 | within |
| `talker-notice-1.withdrawn.if0` | 360100131 | 361044133 | 16 | 9.440 | 20 | within |
| `talker-notice-2.declared.if0` | 300200141 | 301141053 | 16 | 9.409 | 20 | within |
| `talker-notice-2.withdrawn.if0` | 360200131 | 361051967 | 16 | 8.518 | 20 | within |
| `talker-notice-3.declared.if0` | 300300141 | 301141053 | 16 | 8.409 | 20 | within |
| `talker-notice-3.withdrawn.if0` | 360300131 | 361049721 | 16 | 7.496 | 20 | within |
| `talker-notice-4.declared.if0` | 300400141 | 301141184 | 16 | 7.410 | 20 | within |
| `talker-notice-4.withdrawn.if0` | 360400131 | 361047204 | 16 | 6.471 | 20 | within |
| `talker-notice-5.declared.if0` | 300500141 | 301071873 | 16 | 5.717 | 20 | within |
| `talker-notice-5.withdrawn.if0` | 360500131 | 361054683 | 16 | 5.546 | 20 | within |
| `talker-notice-6.declared.if0` | 300600141 | 301073161 | 16 | 4.730 | 20 | within |
| `talker-notice-6.withdrawn.if0` | 360600131 | 361076467 | 16 | 4.763 | 20 | within |
| `talker-notice-7.declared.if0` | 300700141 | 301115492 | 16 | 4.154 | 20 | within |
| `talker-notice-7.withdrawn.if0` | 360700131 | 361096887 | 16 | 3.968 | 20 | within |

Latest: 11.958 ms, talker-notice-0.declared.if0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| talker-notice-0 | 711 | 100,299 (1.003) | 77,937 (0.779) |
| talker-notice-1 | 711 | 100,299 (1.003) | 77,937 (0.779) |
| talker-notice-2 | 711 | 100,299 (1.003) | 77,937 (0.779) |
| talker-notice-3 | 711 | 100,299 (1.003) | 77,937 (0.779) |
| talker-notice-4 | 711 | 100,299 (1.003) | 77,937 (0.779) |
| talker-notice-5 | 711 | 100,299 (1.003) | 77,937 (0.779) |
| talker-notice-6 | 711 | 100,299 (1.003) | 77,937 (0.779) |
| talker-notice-7 | 711 | 100,299 (1.003) | 77,937 (0.779) |

Longest pass that carries a step: 100,299 CPU cycles (1.003 ms), talker-notice-0; longest step: 77,937 (0.779 ms), talker-notice-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.declared.if0` | 1,195,793 | 11.958 | 20 | 24 | fits | 23,632 | 52 | 0.485 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.withdrawn.if0` | 1,044,706 | 10.447 | 20 | 24 | fits | 23,683 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.declared.if0` | 1,039,999 | 10.400 | 20 | 24 | fits | 23,704 | 52 | 0.489 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.withdrawn.if0` | 944,002 | 9.440 | 20 | 24 | fits | 23,683 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.declared.if0` | 940,912 | 9.409 | 20 | 24 | fits | 23,597 | 52 | 0.487 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.withdrawn.if0` | 851,836 | 8.518 | 20 | 24 | fits | 23,683 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.declared.if0` | 840,912 | 8.409 | 20 | 24 | fits | 23,597 | 52 | 0.487 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.withdrawn.if0` | 749,590 | 7.496 | 20 | 24 | fits | 23,683 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.declared.if0` | 741,043 | 7.410 | 20 | 24 | fits | 23,769 | 52 | 0.491 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.withdrawn.if0` | 647,073 | 6.471 | 20 | 24 | fits | 23,683 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.declared.if0` | 571,732 | 5.717 | 20 | 24 | fits | 23,700 | 52 | 0.487 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.withdrawn.if0` | 554,552 | 5.546 | 20 | 24 | fits | 23,683 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.declared.if0` | 473,020 | 4.730 | 20 | 24 | fits | 23,700 | 52 | 0.487 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.withdrawn.if0` | 476,336 | 4.763 | 20 | 24 | fits | 23,714 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.declared.if0` | 415,351 | 4.154 | 20 | 24 | fits | 23,729 | 52 | 0.487 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.withdrawn.if0` | 396,756 | 3.968 | 20 | 24 | fits | 23,712 | 52 | 0.489 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

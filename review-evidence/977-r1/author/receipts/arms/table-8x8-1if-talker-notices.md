### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 2 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-0.declared.if0` (talker-notice-0) | 11.441 (12.418) | fits | 0 acmp | 8 | 0 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-0.withdrawn.if0` (talker-notice-0) | 9.678 (9.912) | fits | 0 maap | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| talker-notice-0 | 1581 | 0 | 153,782 (1.538) | fits |
| talker-notice-1 | 1580 | 0 | 158,355 (1.584) | fits |
| talker-notice-2 | 1580 | 0 | 158,355 (1.584) | fits |
| talker-notice-3 | 1579 | 0 | 158,355 (1.584) | fits |
| talker-notice-4 | 1580 | 0 | 158,355 (1.584) | fits |
| talker-notice-5 | 1580 | 0 | 158,355 (1.584) | fits |
| talker-notice-6 | 1579 | 0 | 156,817 (1.568) | fits |
| talker-notice-7 | 1580 | 0 | 156,817 (1.568) | fits |

A declared or withdrawn Talker's STREAM_OUTPUT notice, from its event's commit to the last recipient's commit (talker_notice.py; FR_NFR.md 3.4.1):

| Row | Event committed, sys | Last recipient committed, sys | Recipients | ms | Bound ms | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | 300000965 | 301145065 | 16 | 11.441 | 20 | within |
| `talker-notice-0.withdrawn.if0` | 360000955 | 360968779 | 16 | 9.678 | 20 | within |
| `talker-notice-1.declared.if0` | 300100141 | 301164841 | 16 | 10.647 | 20 | within |
| `talker-notice-1.withdrawn.if0` | 360100131 | 360981113 | 16 | 8.810 | 20 | within |
| `talker-notice-2.declared.if0` | 300200141 | 301162569 | 16 | 9.624 | 20 | within |
| `talker-notice-2.withdrawn.if0` | 360200131 | 360973244 | 16 | 7.731 | 20 | within |
| `talker-notice-3.declared.if0` | 300300141 | 301162569 | 16 | 8.624 | 20 | within |
| `talker-notice-3.withdrawn.if0` | 360300131 | 360973522 | 16 | 6.734 | 20 | within |
| `talker-notice-4.declared.if0` | 300400141 | 301163362 | 16 | 7.632 | 20 | within |
| `talker-notice-4.withdrawn.if0` | 360400131 | 360975202 | 16 | 5.751 | 20 | within |
| `talker-notice-5.declared.if0` | 300500141 | 301050837 | 16 | 5.507 | 20 | within |
| `talker-notice-5.withdrawn.if0` | 360500131 | 360975981 | 16 | 4.758 | 20 | within |
| `talker-notice-6.declared.if0` | 300600141 | 301050976 | 16 | 4.508 | 20 | within |
| `talker-notice-6.withdrawn.if0` | 360600131 | 361021155 | 16 | 4.210 | 20 | within |
| `talker-notice-7.declared.if0` | 300700141 | 301064629 | 16 | 3.645 | 20 | within |
| `talker-notice-7.withdrawn.if0` | 360700131 | 361019053 | 16 | 3.189 | 20 | within |

Latest: 11.441 ms, talker-notice-0.declared.if0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| talker-notice-0 | 711 | 100,651 (1.007) | 77,975 (0.780) |
| talker-notice-1 | 711 | 100,651 (1.007) | 77,975 (0.780) |
| talker-notice-2 | 711 | 100,651 (1.007) | 77,975 (0.780) |
| talker-notice-3 | 711 | 100,651 (1.007) | 77,975 (0.780) |
| talker-notice-4 | 711 | 100,651 (1.007) | 77,975 (0.780) |
| talker-notice-5 | 711 | 100,651 (1.007) | 77,975 (0.780) |
| talker-notice-6 | 711 | 100,651 (1.007) | 77,975 (0.780) |
| talker-notice-7 | 711 | 100,651 (1.007) | 77,975 (0.780) |

Longest pass that carries a step: 100,651 CPU cycles (1.007 ms), talker-notice-0; longest step: 77,975 (0.780 ms), talker-notice-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.declared.if0` | 1,144,100 | 11.441 | 20 | 24 | fits | 24,365 | 52 | 0.474 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.withdrawn.if0` | 967,824 | 9.678 | 20 | 24 | fits | 24,478 | 52 | 0.480 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.declared.if0` | 1,064,700 | 10.647 | 20 | 24 | fits | 24,590 | 52 | 0.483 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.withdrawn.if0` | 880,982 | 8.810 | 20 | 24 | fits | 24,589 | 52 | 0.483 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.declared.if0` | 962,428 | 9.624 | 20 | 24 | fits | 24,544 | 52 | 0.480 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.withdrawn.if0` | 773,113 | 7.731 | 20 | 24 | fits | 24,589 | 52 | 0.483 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.declared.if0` | 862,428 | 8.624 | 20 | 24 | fits | 24,544 | 52 | 0.480 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.withdrawn.if0` | 673,391 | 6.734 | 20 | 24 | fits | 24,589 | 52 | 0.483 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.declared.if0` | 763,221 | 7.632 | 20 | 24 | fits | 24,544 | 52 | 0.480 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.withdrawn.if0` | 575,071 | 5.751 | 20 | 24 | fits | 24,589 | 52 | 0.483 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.declared.if0` | 550,696 | 5.507 | 20 | 24 | fits | 24,261 | 52 | 0.469 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.withdrawn.if0` | 475,850 | 4.758 | 20 | 24 | fits | 24,589 | 52 | 0.483 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.declared.if0` | 450,835 | 4.508 | 20 | 24 | fits | 24,307 | 52 | 0.471 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.withdrawn.if0` | 421,024 | 4.210 | 20 | 24 | fits | 24,209 | 52 | 0.469 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.declared.if0` | 364,488 | 3.645 | 20 | 24 | fits | 24,362 | 52 | 0.474 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.withdrawn.if0` | 318,922 | 3.189 | 20 | 24 | fits | 24,155 | 52 | 0.467 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

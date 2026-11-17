Original file: <scratch>/r4/budget/r4-de1/results/table.md
Original size: 8104 bytes
Original sha256: 7efd106b3f7efb1dbdfcfdf3526ba881a2d3f82b8db6613f214b1b44aac775e4

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

2 of 2 paths and 16 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-1.declared.if0` (talker-notice-1) | 30.568 (31.062) | MISS ceiling | 0 acmp | 8 | 8 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-2.withdrawn.if0` (talker-notice-2) | 29.594 (30.316) | MISS ceiling | 0 maap | 8 | 8 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| talker-notice-0 | 1561 | 0 | 160,613 (1.606) | fits |
| talker-notice-1 | 1561 | 0 | 159,340 (1.593) | fits |
| talker-notice-2 | 1561 | 0 | 154,992 (1.550) | fits |
| talker-notice-3 | 1564 | 0 | 155,134 (1.551) | fits |
| talker-notice-4 | 1566 | 0 | 155,242 (1.552) | fits |
| talker-notice-5 | 1566 | 0 | 155,218 (1.552) | fits |
| talker-notice-6 | 1566 | 0 | 155,218 (1.552) | fits |
| talker-notice-7 | 1566 | 0 | 155,218 (1.552) | fits |

A declared or withdrawn Talker's STREAM_OUTPUT notice, from its event's commit to the last recipient's commit (talker_notice.py; FR_NFR.md 3.4.1):

| Row | Event committed, sys | Last recipient committed, sys | Recipients | ms | Bound ms | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | 300000965 | 302967153 | 16 | 29.662 | 20 | OVER |
| `talker-notice-0.withdrawn.if0` | 360000955 | 362958274 | 16 | 29.573 | 20 | OVER |
| `talker-notice-1.declared.if0` | 300100141 | 303156918 | 16 | 30.568 | 20 | OVER |
| `talker-notice-1.withdrawn.if0` | 360100131 | 362962392 | 16 | 28.623 | 20 | OVER |
| `talker-notice-2.declared.if0` | 300200141 | 303173371 | 16 | 29.732 | 20 | OVER |
| `talker-notice-2.withdrawn.if0` | 360200131 | 363159503 | 16 | 29.594 | 20 | OVER |
| `talker-notice-3.declared.if0` | 300300141 | 303172368 | 16 | 28.722 | 20 | OVER |
| `talker-notice-3.withdrawn.if0` | 360300131 | 363061508 | 16 | 27.614 | 20 | OVER |
| `talker-notice-4.declared.if0` | 300400141 | 303265867 | 16 | 28.657 | 20 | OVER |
| `talker-notice-4.withdrawn.if0` | 360400131 | 363257290 | 16 | 28.572 | 20 | OVER |
| `talker-notice-5.declared.if0` | 300500141 | 303262513 | 16 | 27.624 | 20 | OVER |
| `talker-notice-5.withdrawn.if0` | 360500131 | 363364513 | 16 | 28.644 | 20 | OVER |
| `talker-notice-6.declared.if0` | 300600141 | 303357202 | 16 | 27.571 | 20 | OVER |
| `talker-notice-6.withdrawn.if0` | 360600131 | 363366241 | 16 | 27.661 | 20 | OVER |
| `talker-notice-7.declared.if0` | 300700141 | 303374260 | 16 | 26.741 | 20 | OVER |
| `talker-notice-7.withdrawn.if0` | 360700131 | 363364274 | 16 | 26.641 | 20 | OVER |

Latest: 30.568 ms, talker-notice-1.declared.if0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| talker-notice-0 | 354 | 100,560 (1.006) | 78,720 (0.787) |
| talker-notice-1 | 354 | 100,522 (1.005) | 78,720 (0.787) |
| talker-notice-2 | 354 | 100,560 (1.006) | 78,720 (0.787) |
| talker-notice-3 | 354 | 100,560 (1.006) | 78,720 (0.787) |
| talker-notice-4 | 354 | 96,857 (0.969) | 78,700 (0.787) |
| talker-notice-5 | 354 | 96,857 (0.969) | 78,700 (0.787) |
| talker-notice-6 | 354 | 96,857 (0.969) | 78,700 (0.787) |
| talker-notice-7 | 354 | 96,857 (0.969) | 78,700 (0.787) |

Longest pass that carries a step: 100,560 CPU cycles (1.006 ms), talker-notice-0; longest step: 78,720 (0.787 ms), talker-notice-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.declared.if0` | 2,966,188 | 29.662 | 20 | 24 | MISS ceiling | 28,868 | 52 | 0.496 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.withdrawn.if0` | 2,957,319 | 29.573 | 20 | 24 | MISS ceiling | 28,603 | 52 | 0.487 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.declared.if0` | 3,056,777 | 30.568 | 20 | 24 | MISS ceiling | 28,868 | 52 | 0.496 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.withdrawn.if0` | 2,862,261 | 28.623 | 20 | 24 | MISS ceiling | 28,603 | 52 | 0.487 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.declared.if0` | 2,973,230 | 29.732 | 20 | 24 | MISS ceiling | 28,868 | 52 | 0.496 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.withdrawn.if0` | 2,959,372 | 29.594 | 20 | 24 | MISS ceiling | 28,842 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.declared.if0` | 2,872,227 | 28.722 | 20 | 24 | MISS ceiling | 28,868 | 52 | 0.496 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.withdrawn.if0` | 2,761,377 | 27.614 | 20 | 24 | MISS ceiling | 28,842 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.declared.if0` | 2,865,726 | 28.657 | 20 | 24 | MISS ceiling | 28,868 | 52 | 0.496 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.withdrawn.if0` | 2,857,159 | 28.572 | 20 | 24 | MISS ceiling | 28,842 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.declared.if0` | 2,762,372 | 27.624 | 20 | 24 | MISS ceiling | 28,868 | 52 | 0.496 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.withdrawn.if0` | 2,864,382 | 28.644 | 20 | 24 | MISS ceiling | 28,842 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.declared.if0` | 2,757,061 | 27.571 | 20 | 24 | MISS ceiling | 28,798 | 52 | 0.494 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.withdrawn.if0` | 2,766,110 | 27.661 | 20 | 24 | MISS ceiling | 28,881 | 52 | 0.496 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.declared.if0` | 2,674,119 | 26.741 | 20 | 24 | MISS ceiling | 28,798 | 52 | 0.494 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.withdrawn.if0` | 2,664,143 | 26.641 | 20 | 24 | MISS ceiling | 28,837 | 52 | 0.491 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

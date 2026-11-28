### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

0 of 2 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-1.declared.if0` (talker-notice-1) | 7.957 (8.486) | fits | 0 acmp | 8 | 0 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-0.withdrawn.if0` (talker-notice-0) | 8.473 (8.510) | fits | 0 maap | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| talker-notice-0 | 2050 | 0 | 128,068 (1.601) | fits |
| talker-notice-1 | 2049 | 0 | 122,383 (1.530) | fits |
| talker-notice-2 | 2049 | 0 | 121,101 (1.514) | fits |
| talker-notice-3 | 2049 | 0 | 121,101 (1.514) | fits |
| talker-notice-4 | 2048 | 0 | 121,093 (1.514) | fits |
| talker-notice-5 | 2048 | 0 | 121,126 (1.514) | fits |
| talker-notice-6 | 2048 | 0 | 121,093 (1.514) | fits |
| talker-notice-7 | 2048 | 0 | 121,093 (1.514) | fits |

A declared or withdrawn Talker's STREAM_OUTPUT notice, from its event's commit to the last recipient's commit (talker_notice.py; FR_NFR.md 3.4.1):

| Row | Event committed, sys | Last recipient committed, sys | Recipients | ms | Bound ms | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | 240000965 | 240455464 | 16 | 5.681 | 20 | within |
| `talker-notice-0.withdrawn.if0` | 288000955 | 288678758 | 16 | 8.473 | 20 | within |
| `talker-notice-1.declared.if0` | 240080141 | 240716680 | 16 | 7.957 | 20 | within |
| `talker-notice-1.withdrawn.if0` | 288080131 | 288686409 | 16 | 7.578 | 20 | within |
| `talker-notice-2.declared.if0` | 240160141 | 240717283 | 16 | 6.964 | 20 | within |
| `talker-notice-2.withdrawn.if0` | 288160131 | 288685990 | 16 | 6.573 | 20 | within |
| `talker-notice-3.declared.if0` | 240240141 | 240695736 | 16 | 5.695 | 20 | within |
| `talker-notice-3.withdrawn.if0` | 288240131 | 288685517 | 16 | 5.567 | 20 | within |
| `talker-notice-4.declared.if0` | 240320141 | 240706714 | 16 | 4.832 | 20 | within |
| `talker-notice-4.withdrawn.if0` | 288320131 | 288688053 | 16 | 4.599 | 20 | within |
| `talker-notice-5.declared.if0` | 240400141 | 240715942 | 16 | 3.948 | 20 | within |
| `talker-notice-5.withdrawn.if0` | 288400131 | 288734327 | 16 | 4.177 | 20 | within |
| `talker-notice-6.declared.if0` | 240480141 | 240728001 | 16 | 3.098 | 20 | within |
| `talker-notice-6.withdrawn.if0` | 288480131 | 288746116 | 16 | 3.325 | 20 | within |
| `talker-notice-7.declared.if0` | 240560141 | 240739933 | 16 | 2.247 | 20 | within |
| `talker-notice-7.withdrawn.if0` | 288560131 | 288759848 | 16 | 2.496 | 20 | within |

Latest: 8.473 ms, talker-notice-0.withdrawn.if0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| talker-notice-0 | 428 | 90,527 (1.132) | 77,931 (0.974) |
| talker-notice-1 | 428 | 90,527 (1.132) | 77,931 (0.974) |
| talker-notice-2 | 428 | 90,527 (1.132) | 77,931 (0.974) |
| talker-notice-3 | 428 | 90,527 (1.132) | 77,931 (0.974) |
| talker-notice-4 | 428 | 90,527 (1.132) | 77,931 (0.974) |
| talker-notice-5 | 428 | 90,527 (1.132) | 77,931 (0.974) |
| talker-notice-6 | 428 | 90,527 (1.132) | 77,931 (0.974) |
| talker-notice-7 | 428 | 90,527 (1.132) | 77,931 (0.974) |

Longest pass that carries a step: 90,527 CPU cycles (1.132 ms), talker-notice-0; longest step: 77,931 (0.974 ms), talker-notice-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.declared.if0` | 454,499 | 5.681 | 20 | 24 | fits | 23,682 | 52 | 0.498 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.withdrawn.if0` | 677,803 | 8.473 | 20 | 24 | fits | 23,944 | 51 | 0.506 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.declared.if0` | 636,539 | 7.957 | 20 | 24 | fits | 23,740 | 52 | 0.498 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.withdrawn.if0` | 606,278 | 7.578 | 20 | 24 | fits | 23,840 | 51 | 0.502 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.declared.if0` | 557,142 | 6.964 | 20 | 24 | fits | 23,513 | 52 | 0.492 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.withdrawn.if0` | 525,859 | 6.573 | 20 | 24 | fits | 23,860 | 51 | 0.502 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.declared.if0` | 455,595 | 5.695 | 20 | 24 | fits | 23,959 | 52 | 0.502 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.withdrawn.if0` | 445,386 | 5.567 | 20 | 24 | fits | 23,900 | 51 | 0.504 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.declared.if0` | 386,573 | 4.832 | 20 | 24 | fits | 23,578 | 52 | 0.489 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.withdrawn.if0` | 367,922 | 4.599 | 20 | 24 | fits | 23,900 | 51 | 0.504 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.declared.if0` | 315,801 | 3.948 | 20 | 24 | fits | 23,588 | 52 | 0.492 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.withdrawn.if0` | 334,196 | 4.177 | 20 | 24 | fits | 23,525 | 51 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.declared.if0` | 247,860 | 3.098 | 20 | 24 | fits | 23,770 | 52 | 0.492 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.withdrawn.if0` | 265,985 | 3.325 | 20 | 24 | fits | 23,535 | 51 | 0.491 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.declared.if0` | 179,792 | 2.247 | 20 | 24 | fits | 23,770 | 52 | 0.492 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.withdrawn.if0` | 199,717 | 2.496 | 20 | 24 | fits | 23,787 | 51 | 0.494 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

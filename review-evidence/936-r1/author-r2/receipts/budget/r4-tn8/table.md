Original file: <scratch>/r4/budget/r4-tn8/results/table.md
Original size: 7922 bytes
Original sha256: 4c60147e173ecc568b75da46005843ed5f02fb48992046a11a757806c749b1b3

### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 2 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-1.declared.if0` (talker-notice-1) | 7.276 (7.679) | fits | 0 acmp | 8 | 0 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-0.withdrawn.if0` (talker-notice-0) | 7.553 (8.555) | fits | 0 maap | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| talker-notice-0 | 1366 | 0 | 157,947 (1.579) | fits |
| talker-notice-1 | 1365 | 0 | 159,188 (1.592) | fits |
| talker-notice-2 | 1365 | 0 | 159,188 (1.592) | fits |
| talker-notice-3 | 1368 | 0 | 159,188 (1.592) | fits |
| talker-notice-4 | 1371 | 0 | 153,444 (1.534) | fits |
| talker-notice-5 | 1371 | 0 | 153,603 (1.536) | fits |
| talker-notice-6 | 1371 | 0 | 153,444 (1.534) | fits |
| talker-notice-7 | 1371 | 0 | 153,444 (1.534) | fits |

A declared or withdrawn Talker's STREAM_OUTPUT notice, from its event's commit to the last recipient's commit (talker_notice.py; FR_NFR.md 3.4.1):

| Row | Event committed, sys | Last recipient committed, sys | Recipients | ms | Bound ms | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | 300000965 | 300542901 | 16 | 5.419 | 20 | within |
| `talker-notice-0.withdrawn.if0` | 360000955 | 360756249 | 16 | 7.553 | 20 | within |
| `talker-notice-1.declared.if0` | 300100141 | 300827737 | 16 | 7.276 | 20 | within |
| `talker-notice-1.withdrawn.if0` | 360100131 | 360760828 | 16 | 6.607 | 20 | within |
| `talker-notice-2.declared.if0` | 300200141 | 300778031 | 16 | 5.779 | 20 | within |
| `talker-notice-2.withdrawn.if0` | 360200131 | 360757666 | 16 | 5.575 | 20 | within |
| `talker-notice-3.declared.if0` | 300300141 | 300778031 | 16 | 4.779 | 20 | within |
| `talker-notice-3.withdrawn.if0` | 360300131 | 360757153 | 16 | 4.570 | 20 | within |
| `talker-notice-4.declared.if0` | 300400141 | 300855332 | 16 | 4.552 | 20 | within |
| `talker-notice-4.withdrawn.if0` | 360400131 | 360758710 | 16 | 3.586 | 20 | within |
| `talker-notice-5.declared.if0` | 300500141 | 300878554 | 16 | 3.784 | 20 | within |
| `talker-notice-5.withdrawn.if0` | 360500131 | 360881828 | 16 | 3.817 | 20 | within |
| `talker-notice-6.declared.if0` | 300600141 | 300902561 | 16 | 3.024 | 20 | within |
| `talker-notice-6.withdrawn.if0` | 360600131 | 360929780 | 16 | 3.296 | 20 | within |
| `talker-notice-7.declared.if0` | 300700141 | 300924649 | 16 | 2.245 | 20 | within |
| `talker-notice-7.withdrawn.if0` | 360700131 | 360961687 | 16 | 2.616 | 20 | within |

Latest: 7.553 ms, talker-notice-0.withdrawn.if0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| talker-notice-0 | 349 | 98,738 (0.987) | 76,252 (0.763) |
| talker-notice-1 | 349 | 98,801 (0.988) | 76,252 (0.763) |
| talker-notice-2 | 349 | 98,801 (0.988) | 76,252 (0.763) |
| talker-notice-3 | 349 | 98,801 (0.988) | 76,252 (0.763) |
| talker-notice-4 | 349 | 98,801 (0.988) | 76,252 (0.763) |
| talker-notice-5 | 349 | 98,755 (0.988) | 76,252 (0.763) |
| talker-notice-6 | 349 | 98,801 (0.988) | 76,252 (0.763) |
| talker-notice-7 | 349 | 98,801 (0.988) | 76,252 (0.763) |

Longest pass that carries a step: 98,801 CPU cycles (0.988 ms), talker-notice-1; longest step: 76,252 (0.763 ms), talker-notice-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.declared.if0` | 541,936 | 5.419 | 20 | 24 | fits | 27,448 | 52 | 0.514 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.withdrawn.if0` | 755,294 | 7.553 | 20 | 24 | fits | 25,596 | 52 | 0.496 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.declared.if0` | 727,596 | 7.276 | 20 | 24 | fits | 25,384 | 52 | 0.487 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.withdrawn.if0` | 660,697 | 6.607 | 20 | 24 | fits | 25,534 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.declared.if0` | 577,890 | 5.779 | 20 | 24 | fits | 25,635 | 52 | 0.496 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.withdrawn.if0` | 557,535 | 5.575 | 20 | 24 | fits | 25,534 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.declared.if0` | 477,890 | 4.779 | 20 | 24 | fits | 25,635 | 52 | 0.496 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.withdrawn.if0` | 457,022 | 4.570 | 20 | 24 | fits | 25,534 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.declared.if0` | 455,191 | 4.552 | 20 | 24 | fits | 25,677 | 52 | 0.494 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.withdrawn.if0` | 358,579 | 3.586 | 20 | 24 | fits | 25,534 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.declared.if0` | 378,413 | 3.784 | 20 | 24 | fits | 25,592 | 52 | 0.491 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.withdrawn.if0` | 381,697 | 3.817 | 20 | 24 | fits | 25,645 | 52 | 0.494 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.declared.if0` | 302,420 | 3.024 | 20 | 24 | fits | 25,592 | 52 | 0.491 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.withdrawn.if0` | 329,649 | 3.296 | 20 | 24 | fits | 25,708 | 52 | 0.496 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.declared.if0` | 224,508 | 2.245 | 20 | 24 | fits | 25,501 | 52 | 0.489 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.withdrawn.if0` | 261,556 | 2.616 | 20 | 24 | fits | 25,633 | 52 | 0.494 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

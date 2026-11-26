### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 2 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-1.declared.if0` (talker-notice-1) | 5.343 (5.988) | fits | 0 acmp | 8 | 0 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | 0 | `talker-notice-0.withdrawn.if0` (talker-notice-0) | 5.219 (5.393) | fits | 0 maap | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| talker-notice-0 | 2151 | 0 | 154,241 (1.542) | fits |
| talker-notice-1 | 2152 | 0 | 153,575 (1.536) | fits |
| talker-notice-2 | 2152 | 0 | 147,994 (1.480) | fits |
| talker-notice-3 | 2152 | 0 | 148,087 (1.481) | fits |
| talker-notice-4 | 2152 | 0 | 148,144 (1.481) | fits |
| talker-notice-5 | 2152 | 0 | 148,144 (1.481) | fits |
| talker-notice-6 | 2152 | 0 | 148,144 (1.481) | fits |
| talker-notice-7 | 2152 | 0 | 148,202 (1.482) | fits |

A declared or withdrawn Talker's STREAM_OUTPUT notice, from its event's commit to the last recipient's commit (talker_notice.py; FR_NFR.md 3.4.1):

| Row | Event committed, sys | Last recipient committed, sys | Recipients | ms | Bound ms | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `talker-notice-0.declared.if0` | 300000965 | 300485998 | 16 | 4.850 | 20 | within |
| `talker-notice-0.withdrawn.if0` | 360000955 | 360522846 | 16 | 5.219 | 20 | within |
| `talker-notice-1.declared.if0` | 300100141 | 300634448 | 16 | 5.343 | 20 | within |
| `talker-notice-1.withdrawn.if0` | 360100131 | 360521101 | 16 | 4.210 | 20 | within |
| `talker-notice-2.declared.if0` | 300200141 | 300634448 | 16 | 4.343 | 20 | within |
| `talker-notice-2.withdrawn.if0` | 360200131 | 360677464 | 16 | 4.773 | 20 | within |
| `talker-notice-3.declared.if0` | 300300141 | 300707930 | 16 | 4.078 | 20 | within |
| `talker-notice-3.withdrawn.if0` | 360300131 | 360678139 | 16 | 3.780 | 20 | within |
| `talker-notice-4.declared.if0` | 300400141 | 300791988 | 16 | 3.918 | 20 | within |
| `talker-notice-4.withdrawn.if0` | 360400131 | 360825976 | 16 | 4.258 | 20 | within |
| `talker-notice-5.declared.if0` | 300500141 | 300805713 | 16 | 3.056 | 20 | within |
| `talker-notice-5.withdrawn.if0` | 360500131 | 360841291 | 16 | 3.412 | 20 | within |
| `talker-notice-6.declared.if0` | 300600141 | 300817764 | 16 | 2.176 | 20 | within |
| `talker-notice-6.withdrawn.if0` | 360600131 | 360854585 | 16 | 2.545 | 20 | within |
| `talker-notice-7.declared.if0` | 300700141 | 300843986 | 16 | 1.438 | 20 | within |
| `talker-notice-7.withdrawn.if0` | 360700131 | 360881961 | 16 | 1.818 | 20 | within |

Latest: 5.343 ms, talker-notice-1.declared.if0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| talker-notice-0 | 448 | 93,002 (0.930) | 78,033 (0.780) |
| talker-notice-1 | 448 | 93,002 (0.930) | 78,033 (0.780) |
| talker-notice-2 | 448 | 93,002 (0.930) | 78,033 (0.780) |
| talker-notice-3 | 448 | 93,002 (0.930) | 78,033 (0.780) |
| talker-notice-4 | 448 | 93,002 (0.930) | 78,033 (0.780) |
| talker-notice-5 | 448 | 93,002 (0.930) | 78,033 (0.780) |
| talker-notice-6 | 448 | 93,002 (0.930) | 78,033 (0.780) |
| talker-notice-7 | 448 | 93,002 (0.930) | 78,033 (0.780) |

Longest pass that carries a step: 93,002 CPU cycles (0.930 ms), talker-notice-0; longest step: 78,033 (0.780 ms), talker-notice-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.declared.if0` | 485,033 | 4.850 | 20 | 24 | fits | 23,954 | 52 | 0.494 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.withdrawn.if0` | 521,891 | 5.219 | 20 | 24 | fits | 23,790 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.declared.if0` | 534,307 | 5.343 | 20 | 24 | fits | 23,680 | 52 | 0.483 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.withdrawn.if0` | 420,970 | 4.210 | 20 | 24 | fits | 23,602 | 52 | 0.483 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.declared.if0` | 434,307 | 4.343 | 20 | 24 | fits | 23,680 | 52 | 0.483 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.withdrawn.if0` | 477,333 | 4.773 | 20 | 24 | fits | 23,800 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.declared.if0` | 407,789 | 4.078 | 20 | 24 | fits | 23,711 | 52 | 0.485 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.withdrawn.if0` | 378,008 | 3.780 | 20 | 24 | fits | 23,800 | 52 | 0.489 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.declared.if0` | 391,847 | 3.918 | 20 | 24 | fits | 23,972 | 52 | 0.489 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.withdrawn.if0` | 425,845 | 4.258 | 20 | 24 | fits | 23,950 | 52 | 0.492 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.declared.if0` | 305,572 | 3.056 | 20 | 24 | fits | 24,082 | 52 | 0.489 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.withdrawn.if0` | 341,160 | 3.412 | 20 | 24 | fits | 23,971 | 52 | 0.492 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.declared.if0` | 217,623 | 2.176 | 20 | 24 | fits | 24,058 | 52 | 0.487 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.withdrawn.if0` | 254,454 | 2.545 | 20 | 24 | fits | 24,081 | 52 | 0.492 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.declared.if0` | 143,845 | 1.438 | 20 | 24 | fits | 24,058 | 52 | 0.487 |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.withdrawn.if0` | 181,830 | 1.818 | 20 | 24 | fits | 23,991 | 52 | 0.487 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

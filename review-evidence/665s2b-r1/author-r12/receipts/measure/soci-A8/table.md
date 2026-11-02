### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 17 paths and 13 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 14.419 (15.766) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 7.780 (11.536) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.213 (1.473) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 3.202 (5.477) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 67.775 (69.013) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.885 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 2.934 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 16.094 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.976 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 11.484 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 11.767 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.970 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 69.837 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.959 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 11.752 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 11.721 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 34.516 | MISS ceiling | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 29.853 | 21 | 370,941 (3.709) | yes | - |
| backlog-adp | 0 | 36.447 | 23 | 384,851 (3.849) | yes | - |
| backlog-adp-refill | 0 | 42.357 | 24 | 337,240 (3.372) | yes | - |
| backlog-owed | 0 | 360.935 | 64 | 384,601 (3.846) | yes | - |

Composed maximum over the 4 backlog windows: 384,851 CPU cycles (3.849 ms), backlog-adp.
Over the windows that released their whole load only: 384,851 (3.849 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 305 | 15 | 370,941 (3.709) | OVER the share |
| backlog-adp | 325 | 16 | 384,851 (3.849) | OVER the share |
| backlog-adp-refill | 326 | 15 | 355,737 (3.557) | OVER the share |
| backlog-owed | 359 | 18 | 384,601 (3.846) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 320,226 | 3.202 | 20 | 200 | fits | 249,903 | 125 | 0.818 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,441,921 | 14.419 | 20 | 20 | fits | 224,738 | 52 | 0.827 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 297,637 | 2.976 | 20 | 200 | fits | 297,845 | 143 | 0.824 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 1,173,662 | 11.737 | 20 | 200 | fits | 255,790 | 57 | 0.826 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 293,378 | 2.934 | 20 | 20 | fits | 297,845 | 143 | 0.824 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,571,293 | 15.713 | 20 | 20 | fits | 224,738 | 52 | 0.827 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 296,963 | 2.970 | 20 | 24 | fits | 297,845 | 143 | 0.824 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 2,484,262 | 24.843 | 20 | 24 | MISS ceiling | 93,065 | 31 | 0.829 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 295,923 | 2.959 | 20 | 50 | fits | 297,845 | 143 | 0.824 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 1,172,167 | 11.722 | 20 | 50 | fits | 255,790 | 57 | 0.826 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 1,172,102 | 11.721 | 18 | 18 | fits | 255,790 | 57 | 0.826 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 2,857,843 | 28.578 | 18 | 18 | MISS ceiling | 75,088 | 18 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 777,968 | 7.780 | 20 | 20 | fits | 384,851 | 89 | 0.827 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 254,890 | 2.549 | 20 | 200 | fits | 259,572 | 140 | 0.822 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 1,148,353 | 11.484 | 20 | 200 | fits | 384,851 | 89 | 0.827 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 255,802 | 2.558 | 20 | 20 | fits | 259,572 | 140 | 0.822 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 1,609,399 | 16.094 | 20 | 20 | fits | 207,730 | 53 | 0.822 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 259,387 | 2.594 | 20 | 24 | fits | 259,572 | 140 | 0.822 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 2,851,195 | 28.512 | 20 | 24 | MISS ceiling | 127,716 | 31 | 0.832 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 258,347 | 2.583 | 20 | 50 | fits | 259,572 | 140 | 0.822 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 1,152,029 | 11.520 | 20 | 50 | fits | 384,851 | 89 | 0.827 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 1,151,964 | 11.520 | 18 | 18 | fits | 384,851 | 89 | 0.827 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 3,451,591 | 34.516 | 18 | 18 | MISS ceiling | 76,878 | 14 | 0.828 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 21,322 | 0.213 | 20 | 20 | fits | 91,755 | 21 | 0.810 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 254,890 | 2.549 | 20 | 200 | fits | 259,572 | 140 | 0.822 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 103,260 | 1.033 | 20 | 200 | fits | 91,755 | 21 | 0.810 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 255,802 | 2.558 | 20 | 20 | fits | 259,572 | 140 | 0.822 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 1,550,149 | 15.501 | 20 | 20 | fits | 194,445 | 47 | 0.820 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 259,387 | 2.594 | 20 | 24 | fits | 259,572 | 140 | 0.822 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 2,839,513 | 28.395 | 20 | 24 | MISS ceiling | 127,716 | 31 | 0.832 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 258,347 | 2.583 | 20 | 50 | fits | 259,572 | 140 | 0.822 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 1,104,418 | 11.044 | 20 | 50 | fits | 337,240 | 79 | 0.830 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 1,104,353 | 11.044 | 18 | 18 | fits | 337,240 | 79 | 0.830 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 3,364,803 | 33.648 | 18 | 18 | MISS ceiling | 109,515 | 18 | 0.835 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,777,458 | 67.775 | 20 | 20 | MISS ceiling | 100,482 | 27 | 0.811 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,088,455 | 360.885 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,088,380 | 360.884 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,088,305 | 360.883 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,088,230 | 360.882 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 293,221 | 2.932 | 20 | 200 | fits | 254,452 | 134 | 0.820 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 1,176,735 | 11.767 | 20 | 200 | fits | 206,023 | 60 | 0.820 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 288,962 | 2.890 | 20 | 20 | fits | 254,452 | 134 | 0.820 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,599,581 | 15.996 | 20 | 20 | fits | 205,823 | 35 | 0.822 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 292,547 | 2.925 | 20 | 24 | fits | 254,452 | 134 | 0.820 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,983,722 | 69.837 | 20 | 24 | MISS ceiling | 61,283 | 23 | 0.811 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 291,507 | 2.915 | 20 | 50 | fits | 254,452 | 134 | 0.820 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 1,175,240 | 11.752 | 20 | 50 | fits | 206,023 | 60 | 0.820 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 675,653 | 6.757 | 18 | 18 | fits | 384,601 | 138 | 0.828 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 2,925,538 | 29.255 | 18 | 18 | MISS ceiling | 109,321 | 21 | 0.834 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT

### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.193 (6.872) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.951 (5.314) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.234 (0.759) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.350 (2.317) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.912 (64.442) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.512 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.212 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.420 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.255 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.261 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.137 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.248 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.938 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.238 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 5.298 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.986 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | 14.841 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 13.391 | 20 | 147,962 (1.480) | yes | - |
| backlog-adp | 0 | 15.350 | 18 | 170,664 (1.707) | yes | - |
| backlog-adp-refill | 0 | 41.117 | 26 | 170,664 (1.707) | yes | - |
| backlog-owed | 0 | 360.563 | 67 | 176,842 (1.768) | yes | - |

Composed maximum over the 4 backlog windows: 176,842 CPU cycles (1.768 ms), backlog-owed.
Over the windows that released their whole load only: 176,842 (1.768 ms), backlog-owed.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 303 | 0 | 147,962 (1.480) | fits |
| backlog-adp | 319 | 0 | 170,664 (1.707) | fits |
| backlog-adp-refill | 327 | 0 | 170,664 (1.707) | fits |
| backlog-owed | 361 | 0 | 176,842 (1.768) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 134,961 | 1.350 | 20 | 200 | fits | 106,024 | 125 | 0.530 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 619,326 | 6.193 | 20 | 20 | fits | 92,307 | 46 | 0.666 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 125,478 | 1.255 | 20 | 200 | fits | 125,686 | 143 | 0.519 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 500,123 | 5.001 | 20 | 200 | fits | 121,268 | 57 | 0.681 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 121,219 | 1.212 | 20 | 20 | fits | 125,686 | 143 | 0.519 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 681,952 | 6.820 | 20 | 20 | fits | 92,307 | 46 | 0.666 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 124,804 | 1.248 | 20 | 24 | fits | 125,686 | 143 | 0.519 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,160,433 | 11.604 | 20 | 24 | fits | 48,032 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 123,764 | 1.238 | 20 | 50 | fits | 125,686 | 143 | 0.519 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 498,628 | 4.986 | 20 | 50 | fits | 121,268 | 57 | 0.681 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 498,563 | 4.986 | 18 | 18 | fits | 121,268 | 57 | 0.681 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,286,540 | 12.865 | 18 | 18 | fits | 31,879 | 18 | 0.732 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 395,127 | 3.951 | 20 | 20 | fits | 148,514 | 89 | 0.677 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 99,305 | 0.993 | 20 | 200 | fits | 103,987 | 140 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 526,095 | 5.261 | 20 | 200 | fits | 148,514 | 89 | 0.677 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 100,217 | 1.002 | 20 | 20 | fits | 103,987 | 140 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 741,968 | 7.420 | 20 | 20 | fits | 107,049 | 46 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 103,802 | 1.038 | 20 | 24 | fits | 103,987 | 140 | 0.486 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,379,262 | 13.793 | 20 | 24 | fits | 62,254 | 31 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 102,762 | 1.028 | 20 | 50 | fits | 103,987 | 140 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 529,771 | 5.298 | 20 | 50 | fits | 148,514 | 89 | 0.677 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 381,192 | 3.812 | 18 | 18 | fits | 170,664 | 104 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,477,845 | 14.778 | 18 | 18 | fits | 45,256 | 18 | 0.760 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 23,408 | 0.234 | 20 | 20 | fits | 41,949 | 21 | 0.752 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 99,305 | 0.993 | 20 | 200 | fits | 103,987 | 140 | 0.486 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 58,191 | 0.582 | 20 | 200 | fits | 41,949 | 21 | 0.752 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 100,217 | 1.002 | 20 | 20 | fits | 103,987 | 140 | 0.486 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 722,856 | 7.229 | 20 | 20 | fits | 106,919 | 46 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 103,802 | 1.038 | 20 | 24 | fits | 103,987 | 140 | 0.486 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,363,039 | 13.630 | 20 | 24 | fits | 62,254 | 31 | 0.730 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 102,762 | 1.028 | 20 | 50 | fits | 103,987 | 140 | 0.486 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 511,065 | 5.111 | 20 | 50 | fits | 129,808 | 79 | 0.679 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 381,192 | 3.812 | 18 | 18 | fits | 170,664 | 104 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,484,054 | 14.841 | 18 | 18 | fits | 33,276 | 15 | 0.803 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,391,207 | 63.912 | 20 | 20 | MISS ceiling | 49,204 | 27 | 0.597 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,051,192 | 360.512 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,051,117 | 360.511 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,051,042 | 360.510 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,050,967 | 360.510 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 115,532 | 1.155 | 20 | 200 | fits | 102,616 | 134 | 0.489 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 513,734 | 5.137 | 20 | 200 | fits | 120,951 | 69 | 0.679 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 111,273 | 1.113 | 20 | 20 | fits | 102,616 | 134 | 0.489 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 702,318 | 7.023 | 20 | 20 | fits | 94,821 | 35 | 0.755 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 114,858 | 1.149 | 20 | 24 | fits | 102,616 | 134 | 0.489 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,493,823 | 64.938 | 20 | 24 | MISS ceiling | 31,101 | 23 | 0.593 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 113,818 | 1.138 | 20 | 50 | fits | 102,616 | 134 | 0.489 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 512,239 | 5.122 | 20 | 50 | fits | 120,951 | 69 | 0.679 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 391,223 | 3.912 | 18 | 18 | fits | 176,842 | 97 | 0.686 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,275,669 | 12.757 | 18 | 18 | fits | 33,408 | 18 | 0.792 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT

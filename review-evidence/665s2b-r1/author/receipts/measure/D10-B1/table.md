### 1x1

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.695 (4.030) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.601 (3.460) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.116 (0.341) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.152 (2.112) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.997 (62.182) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.202 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.012 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 4.761 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.054 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.407 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.048 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.827 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.037 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.443 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.089 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 10.188 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.657 | 17 | 105,646 (1.056) | yes | - |
| backlog-adp | 10.463 | 18 | 104,083 (1.041) | yes | - |
| backlog-adp-refill | 40.625 | 25 | 104,083 (1.041) | yes | - |
| backlog-owed | 360.252 | 64 | 102,817 (1.028) | yes | - |

Composed maximum over the 4 backlog windows: 105,646 CPU cycles (1.056 ms), backlog.
Over the windows that released their whole load only: 105,646 (1.056 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 115,156 | 1.152 | 20 | 200 | fits | 105,601 | 117 | 0.600 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 369,506 | 3.695 | 20 | 20 | fits | 43,676 | 44 | 0.498 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 105,438 | 1.054 | 20 | 200 | fits | 105,646 | 141 | 0.617 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 314,075 | 3.141 | 20 | 200 | fits | 50,182 | 55 | 0.487 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 101,179 | 1.012 | 20 | 20 | fits | 105,646 | 141 | 0.617 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 397,684 | 3.977 | 20 | 20 | fits | 43,676 | 44 | 0.498 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 104,764 | 1.048 | 20 | 24 | fits | 105,646 | 141 | 0.617 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 631,770 | 6.318 | 20 | 24 | fits | 22,973 | 29 | 0.487 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 103,724 | 1.037 | 20 | 50 | fits | 105,646 | 141 | 0.617 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 312,580 | 3.126 | 20 | 50 | fits | 50,182 | 55 | 0.487 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 208,870 | 2.089 | 18 | 18 | fits | 105,601 | 117 | 0.600 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 639,893 | 6.399 | 18 | 18 | fits | 10,658 | 19 | 0.444 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 260,076 | 2.601 | 20 | 20 | fits | 87,624 | 81 | 0.668 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 64,312 | 0.643 | 20 | 200 | fits | 68,994 | 135 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 340,669 | 3.407 | 20 | 200 | fits | 87,624 | 81 | 0.668 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 65,224 | 0.652 | 20 | 20 | fits | 68,994 | 135 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 476,128 | 4.761 | 20 | 20 | fits | 55,977 | 33 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 68,809 | 0.688 | 20 | 24 | fits | 68,994 | 135 | 0.496 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 997,617 | 9.976 | 20 | 24 | fits | 46,916 | 29 | 0.751 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 67,769 | 0.678 | 20 | 50 | fits | 68,994 | 135 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 344,345 | 3.443 | 20 | 50 | fits | 87,624 | 81 | 0.668 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 171,397 | 1.714 | 18 | 18 | fits | 104,083 | 138 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,018,764 | 10.188 | 18 | 18 | fits | 23,682 | 16 | 0.842 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,607 | 0.116 | 20 | 20 | fits | 20,114 | 20 | 0.752 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 64,312 | 0.643 | 20 | 200 | fits | 68,994 | 135 | 0.496 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 26,262 | 0.263 | 20 | 200 | fits | 20,114 | 20 | 0.752 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 65,224 | 0.652 | 20 | 20 | fits | 68,994 | 135 | 0.496 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 471,891 | 4.719 | 20 | 20 | fits | 69,151 | 44 | 0.696 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 68,809 | 0.688 | 20 | 24 | fits | 68,994 | 135 | 0.496 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 946,361 | 9.464 | 20 | 24 | fits | 46,948 | 29 | 0.752 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 67,769 | 0.678 | 20 | 50 | fits | 68,994 | 135 | 0.496 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 335,618 | 3.356 | 20 | 50 | fits | 78,897 | 71 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 171,397 | 1.714 | 18 | 18 | fits | 104,083 | 138 | 0.627 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 998,838 | 9.988 | 18 | 18 | fits | 22,514 | 14 | 0.843 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,199,672 | 61.997 | 20 | 20 | MISS ceiling | 27,012 | 25 | 0.568 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,020,162 | 360.202 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,020,087 | 360.201 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,020,012 | 360.200 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,019,937 | 360.199 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 67,326 | 0.673 | 20 | 200 | fits | 65,620 | 129 | 0.491 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 331,342 | 3.313 | 20 | 200 | fits | 78,306 | 67 | 0.685 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 63,067 | 0.631 | 20 | 20 | fits | 65,620 | 129 | 0.491 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 447,118 | 4.471 | 20 | 20 | fits | 58,096 | 33 | 0.781 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 66,652 | 0.667 | 20 | 24 | fits | 65,620 | 129 | 0.491 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,282,685 | 62.827 | 20 | 24 | MISS ceiling | 21,280 | 21 | 0.603 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 65,612 | 0.656 | 20 | 50 | fits | 65,620 | 129 | 0.491 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 329,847 | 3.298 | 20 | 50 | fits | 78,306 | 67 | 0.685 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 167,974 | 1.680 | 18 | 18 | fits | 102,817 | 131 | 0.650 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 806,634 | 8.066 | 18 | 18 | fits | 32,071 | 20 | 0.810 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT

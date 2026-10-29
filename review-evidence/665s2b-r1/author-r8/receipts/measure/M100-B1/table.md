### 1x1

3 of 16 paths and 6 of 49 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.694 (3.968) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.721 (3.617) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.073 (0.256) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.170 (2.103) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.641 (61.768) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.160 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.043 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 5.023 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.086 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.564 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.079 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.319 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.068 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.601 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.080 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 9.906 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 6.060 | 17 | 108,764 (1.088) | yes | - |
| backlog-adp | 10.112 | 17 | 109,137 (1.091) | yes | - |
| backlog-adp-refill | 40.506 | 25 | 109,137 (1.091) | yes | - |
| backlog-owed | 360.211 | 65 | 106,213 (1.062) | yes | - |

Composed maximum over the 4 backlog windows: 109,137 CPU cycles (1.091 ms), backlog-adp.
Over the windows that released their whole load only: 109,137 (1.091 ms), backlog-adp.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 116,993 | 1.170 | 10 | 200 | fits | 101,573 | 116 | 0.526 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 369,352 | 3.694 | 10 | 20 | fits | 42,863 | 43 | 0.385 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 108,556 | 1.086 | 10 | 200 | fits | 108,764 | 140 | 0.561 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 310,014 | 3.100 | 10 | 200 | fits | 48,162 | 54 | 0.362 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 104,297 | 1.043 | 10 | 20 | fits | 108,764 | 140 | 0.561 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 391,533 | 3.915 | 10 | 20 | fits | 42,863 | 43 | 0.385 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 107,882 | 1.079 | 10 | 24 | fits | 108,764 | 140 | 0.561 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 581,761 | 5.818 | 10 | 24 | fits | 18,585 | 28 | 0.331 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 106,842 | 1.068 | 10 | 50 | fits | 108,764 | 140 | 0.561 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 308,519 | 3.085 | 10 | 50 | fits | 48,162 | 54 | 0.362 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 207,960 | 2.080 | 10 | 18 | fits | 101,573 | 116 | 0.526 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 586,909 | 5.869 | 10 | 18 | fits | 7,683 | 19 | 0.093 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 272,127 | 2.721 | 10 | 20 | fits | 91,585 | 80 | 0.639 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 66,064 | 0.661 | 10 | 200 | fits | 70,746 | 134 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 356,427 | 3.564 | 10 | 200 | fits | 91,585 | 80 | 0.639 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 66,976 | 0.670 | 10 | 20 | fits | 70,746 | 134 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 502,255 | 5.023 | 10 | 20 | fits | 62,627 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 70,561 | 0.706 | 10 | 24 | fits | 70,746 | 134 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 993,112 | 9.931 | 10 | 24 | fits | 43,592 | 28 | 0.699 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 69,521 | 0.695 | 10 | 50 | fits | 70,746 | 134 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 360,103 | 3.601 | 10 | 50 | fits | 91,585 | 80 | 0.639 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 178,203 | 1.782 | 10 | 18 | fits | 109,137 | 137 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 990,577 | 9.906 | 10 | 18 | fits | 43,592 | 28 | 0.699 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 7,265 | 0.073 | 10 | 20 | fits | 18,379 | 20 | 0.718 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 66,064 | 0.661 | 10 | 200 | fits | 70,746 | 134 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 20,243 | 0.202 | 10 | 200 | fits | 18,379 | 20 | 0.718 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 66,976 | 0.670 | 10 | 20 | fits | 70,746 | 134 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 491,417 | 4.914 | 10 | 20 | fits | 71,569 | 43 | 0.656 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 70,561 | 0.706 | 10 | 24 | fits | 70,746 | 134 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 913,053 | 9.131 | 10 | 24 | fits | 43,661 | 28 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 69,521 | 0.695 | 10 | 50 | fits | 70,746 | 134 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 350,325 | 3.503 | 10 | 50 | fits | 81,807 | 70 | 0.630 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 178,203 | 1.782 | 10 | 18 | fits | 109,137 | 137 | 0.594 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 970,979 | 9.710 | 10 | 18 | fits | 30,091 | 17 | 0.778 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,164,143 | 61.641 | 10 | 20 | MISS ceiling | 22,539 | 24 | 0.393 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,015,996 | 360.160 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,015,921 | 360.159 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,015,846 | 360.158 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,015,771 | 360.158 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 72,631 | 0.726 | 10 | 200 | fits | 68,235 | 128 | 0.440 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 346,043 | 3.460 | 10 | 200 | fits | 80,258 | 66 | 0.643 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 68,372 | 0.684 | 10 | 20 | fits | 68,235 | 128 | 0.440 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 453,722 | 4.537 | 10 | 20 | fits | 54,461 | 32 | 0.747 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 71,957 | 0.720 | 10 | 24 | fits | 68,235 | 128 | 0.440 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,231,886 | 62.319 | 10 | 24 | MISS ceiling | 17,289 | 20 | 0.438 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 70,917 | 0.709 | 10 | 50 | fits | 68,235 | 128 | 0.440 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 344,548 | 3.445 | 10 | 50 | fits | 80,258 | 66 | 0.643 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 176,675 | 1.767 | 10 | 18 | fits | 106,213 | 130 | 0.616 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 817,111 | 8.171 | 10 | 18 | fits | 21,767 | 17 | 0.787 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT

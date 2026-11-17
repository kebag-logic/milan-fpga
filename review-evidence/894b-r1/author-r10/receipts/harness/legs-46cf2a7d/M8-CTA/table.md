### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 7 paths and 8 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-6.held.acmp.if0` (notice-retried-6) | 5.942 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-3.held.adp.if0` (notice-retried-3) | 1.719 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.aecp.if0` (notice-retried-4) | 4.531 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.maap.if0` (notice-retried-4) | 4.338 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.srp.if0` (notice-retried-7) | 7.816 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-4.mrpdu.periodic.if0` (notice-retried-4) | 72.534 | MISS ceiling | 0 srp | 8 | 8 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-7.stream_info.if0` (notice-retried-7) | 8.254 (8.354) | fits | 2 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1458 | 0 | 158,850 (1.589) | fits |
| notice-retried-1 | 1459 | 0 | 158,850 (1.589) | fits |
| notice-retried-2 | 1460 | 0 | 158,923 (1.589) | fits |
| notice-retried-3 | 1458 | 0 | 158,850 (1.589) | fits |
| notice-retried-4 | 1458 | 0 | 158,769 (1.588) | fits |
| notice-retried-5 | 1459 | 0 | 158,842 (1.588) | fits |
| notice-retried-6 | 1458 | 0 | 158,923 (1.589) | fits |
| notice-retried-7 | 1457 | 0 | 158,818 (1.588) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 8.084 | 20 | 16 | 1 | within |
| notice-retried-1 | 8.097 | 20 | 16 | 2 | within |
| notice-retried-2 | 8.097 | 20 | 16 | 2 | within |
| notice-retried-3 | 8.132 | 20 | 16 | 2 | within |
| notice-retried-4 | 8.132 | 20 | 16 | 2 | within |
| notice-retried-5 | 8.132 | 20 | 16 | 2 | within |
| notice-retried-6 | 7.991 | 20 | 16 | 1 | within |
| notice-retried-7 | 8.254 | 20 | 16 | 2 | within |

Latest: 8.254 ms, notice-retried-7.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 303 | 80,131 (0.801) | 47,909 (0.479) |
| notice-retried-1 | 303 | 80,131 (0.801) | 47,909 (0.479) |
| notice-retried-2 | 303 | 80,131 (0.801) | 47,909 (0.479) |
| notice-retried-3 | 303 | 80,131 (0.801) | 47,909 (0.479) |
| notice-retried-4 | 303 | 80,131 (0.801) | 47,909 (0.479) |
| notice-retried-5 | 303 | 80,131 (0.801) | 47,909 (0.479) |
| notice-retried-6 | 303 | 80,131 (0.801) | 47,909 (0.479) |
| notice-retried-7 | 303 | 80,131 (0.801) | 47,909 (0.479) |

Longest pass that carries a step: 80,131 CPU cycles (0.801 ms), notice-retried-0; longest step: 47,909 (0.479 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 808,445 | 8.084 | 20 | 24 | fits | 24,482 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 164,073 | 1.641 | 20 | 200 | fits | 152,686 | 216 | 0.343 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 453,763 | 4.538 | 20 | 20 | fits | 154,438 | 143 | 0.409 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 433,559 | 4.336 | 20 | 24 | fits | 154,438 | 143 | 0.409 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 414,288 | 4.143 | 20 | 50 | fits | 154,438 | 143 | 0.409 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 779,288 | 7.793 | 20 | 20 | fits | 104,549 | 50 | 0.518 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 7,214,968 | 72.150 | 49 | 49 | MISS ceiling | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 809,746 | 8.097 | 20 | 24 | fits | 24,482 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 162,188 | 1.622 | 20 | 200 | fits | 157,344 | 225 | 0.327 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 451,730 | 4.517 | 20 | 20 | fits | 154,098 | 144 | 0.402 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 431,526 | 4.315 | 20 | 24 | fits | 154,098 | 144 | 0.402 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 412,255 | 4.123 | 20 | 50 | fits | 154,098 | 144 | 0.402 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 780,730 | 7.807 | 20 | 20 | fits | 108,752 | 57 | 0.564 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 7,189,461 | 71.895 | 49 | 49 | MISS ceiling | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 809,710 | 8.097 | 20 | 24 | fits | 24,482 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 151,369 | 1.514 | 20 | 200 | fits | 149,189 | 205 | 0.332 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 575,912 | 5.759 | 20 | 20 | fits | 136,132 | 61 | 0.622 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 419,576 | 4.196 | 20 | 24 | fits | 152,897 | 156 | 0.405 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 400,305 | 4.003 | 20 | 50 | fits | 152,897 | 156 | 0.405 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 776,209 | 7.762 | 20 | 20 | fits | 118,805 | 67 | 0.541 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 7,186,993 | 71.870 | 49 | 49 | MISS ceiling | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 813,196 | 8.132 | 20 | 24 | fits | 24,482 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 171,862 | 1.719 | 20 | 200 | fits | 153,803 | 222 | 0.342 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 461,645 | 4.616 | 20 | 20 | fits | 154,397 | 143 | 0.408 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 441,441 | 4.414 | 20 | 24 | fits | 154,397 | 143 | 0.408 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 422,170 | 4.222 | 20 | 50 | fits | 154,397 | 143 | 0.408 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 769,821 | 7.698 | 20 | 20 | fits | 104,597 | 52 | 0.515 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 7,241,310 | 72.413 | 49 | 49 | MISS ceiling | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 813,196 | 8.132 | 20 | 24 | fits | 24,567 | 52 | 0.440 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 169,548 | 1.695 | 20 | 200 | fits | 152,183 | 218 | 0.337 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 473,267 | 4.733 | 20 | 20 | fits | 154,895 | 143 | 0.412 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 453,063 | 4.531 | 20 | 24 | fits | 154,895 | 143 | 0.412 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 433,792 | 4.338 | 20 | 50 | fits | 154,895 | 143 | 0.412 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 781,229 | 7.812 | 20 | 20 | fits | 104,328 | 50 | 0.514 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 7,253,424 | 72.534 | 49 | 49 | MISS ceiling | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 813,196 | 8.132 | 20 | 24 | fits | 24,567 | 52 | 0.440 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 160,625 | 1.606 | 20 | 200 | fits | 146,287 | 146 | 0.324 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 593,041 | 5.930 | 20 | 20 | fits | 135,701 | 61 | 0.615 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 437,136 | 4.371 | 20 | 24 | fits | 149,493 | 148 | 0.435 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 417,865 | 4.179 | 20 | 50 | fits | 149,493 | 148 | 0.435 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 775,563 | 7.756 | 20 | 20 | fits | 113,155 | 54 | 0.501 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 7,232,281 | 72.323 | 49 | 49 | MISS ceiling | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 799,105 | 7.991 | 20 | 24 | fits | 25,128 | 52 | 0.457 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 151,097 | 1.511 | 20 | 200 | fits | 150,583 | 208 | 0.325 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 594,216 | 5.942 | 20 | 20 | fits | 139,502 | 68 | 0.633 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 423,269 | 4.233 | 20 | 24 | fits | 156,957 | 165 | 0.409 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 403,998 | 4.040 | 20 | 50 | fits | 156,957 | 165 | 0.409 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 776,949 | 7.769 | 20 | 20 | fits | 113,411 | 54 | 0.507 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 7,210,123 | 72.101 | 49 | 49 | MISS ceiling | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 825,426 | 8.254 | 20 | 24 | fits | 25,197 | 52 | 0.460 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 169,190 | 1.692 | 20 | 200 | fits | 152,464 | 221 | 0.343 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 458,885 | 4.589 | 20 | 20 | fits | 154,430 | 144 | 0.409 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 438,681 | 4.387 | 20 | 24 | fits | 154,430 | 144 | 0.409 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 419,410 | 4.194 | 20 | 50 | fits | 154,430 | 144 | 0.409 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 781,563 | 7.816 | 20 | 20 | fits | 104,456 | 50 | 0.517 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 7,214,072 | 72.141 | 49 | 49 | MISS ceiling | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

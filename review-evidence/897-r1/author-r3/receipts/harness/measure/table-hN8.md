### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 92 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.acmp.if0` (notice-burst-0) | 6.841 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-0.held.adp.if1` (notice-burst-0) | 7.044 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.aecp.if1` (notice-every-0) | 5.085 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 6.376 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.srp.if1` (notice-every-0) | 12.408 | fits | 31 srp | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 2.366 | fits | 0 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-0.mrpdu.periodic.if1` (notice-every-0) | 3.823 | fits | 0 srp | 1 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-0.notices.29.36.0.if0` (notice-burst-0) | 52.175 (52.543) | fits | 1 events | 80 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1099 | 0 | 170,746 (1.707) | fits |
| notice-burst-0 | 948 | 0 | 169,371 (1.694) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 2.396 | 62 | 32 | 1 | within |
| notice-every-0 | 2.703 | 62 | 32 | 1 | within |
| notice-every-0 | 6.301 | 62 | 32 | 1 | within |
| notice-every-0 | 6.606 | 62 | 32 | 1 | within |
| notice-every-0 | 8.221 | 62 | 32 | 1 | within |
| notice-every-0 | 8.526 | 62 | 32 | 1 | within |
| notice-every-0 | 4.377 | 62 | 32 | 1 | within |
| notice-every-0 | 4.689 | 62 | 32 | 1 | within |
| notice-every-0 | 10.421 | 62 | 32 | 1 | within |
| notice-every-0 | 10.724 | 62 | 32 | 1 | within |
| notice-every-0 | 12.315 | 62 | 32 | 1 | within |
| notice-every-0 | 12.620 | 62 | 32 | 1 | within |
| notice-every-0 | 14.293 | 62 | 32 | 1 | within |
| notice-every-0 | 14.599 | 62 | 32 | 1 | within |
| notice-every-0 | 16.182 | 62 | 32 | 1 | within |
| notice-every-0 | 16.488 | 62 | 32 | 1 | within |
| notice-every-0 | 18.355 | 62 | 32 | 1 | within |
| notice-every-0 | 18.660 | 62 | 32 | 1 | within |
| notice-every-0 | 20.226 | 62 | 32 | 1 | within |
| notice-every-0 | 20.532 | 62 | 32 | 1 | within |
| notice-every-0 | 24.520 | 62 | 32 | 1 | within |
| notice-every-0 | 28.327 | 62 | 32 | 1 | within |
| notice-every-0 | 28.608 | 62 | 32 | 1 | within |
| notice-every-0 | 30.460 | 62 | 32 | 1 | within |
| notice-every-0 | 30.740 | 62 | 32 | 1 | within |
| notice-every-0 | 32.306 | 62 | 32 | 1 | within |
| notice-every-0 | 32.583 | 62 | 32 | 1 | within |
| notice-every-0 | 34.197 | 62 | 32 | 1 | within |
| notice-every-0 | 34.481 | 62 | 32 | 1 | within |
| notice-every-0 | 36.313 | 62 | 32 | 1 | within |
| notice-every-0 | 36.592 | 62 | 32 | 1 | within |
| notice-every-0 | 38.414 | 62 | 32 | 1 | within |
| notice-every-0 | 38.694 | 62 | 32 | 1 | within |
| notice-every-0 | 40.225 | 62 | 32 | 1 | within |
| notice-every-0 | 40.501 | 62 | 32 | 1 | within |
| notice-every-0 | 42.584 | 62 | 32 | 1 | within |
| notice-every-0 | 42.846 | 62 | 32 | 1 | within |
| notice-every-0 | 44.400 | 62 | 32 | 1 | within |
| notice-every-0 | 44.698 | 62 | 32 | 1 | within |
| notice-every-0 | 46.206 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.612 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.910 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.064 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.367 | 62 | 32 | 1 | within |
| notice-burst-0 | 18.251 | 62 | 32 | 1 | within |
| notice-burst-0 | 22.175 | 62 | 32 | 1 | within |
| notice-burst-0 | 22.462 | 62 | 32 | 1 | within |
| notice-burst-0 | 24.161 | 62 | 32 | 1 | within |
| notice-burst-0 | 24.450 | 62 | 32 | 1 | within |
| notice-burst-0 | 26.058 | 62 | 32 | 1 | within |
| notice-burst-0 | 26.348 | 62 | 32 | 1 | within |
| notice-burst-0 | 28.241 | 62 | 32 | 1 | within |
| notice-burst-0 | 28.531 | 62 | 32 | 1 | within |
| notice-burst-0 | 30.133 | 62 | 32 | 1 | within |
| notice-burst-0 | 30.420 | 62 | 32 | 1 | within |
| notice-burst-0 | 32.304 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.977 | 62 | 32 | 1 | within |
| notice-burst-0 | 6.302 | 62 | 32 | 1 | within |
| notice-burst-0 | 32.589 | 62 | 32 | 1 | within |
| notice-burst-0 | 34.232 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.862 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.200 | 62 | 32 | 1 | within |
| notice-burst-0 | 34.511 | 62 | 32 | 1 | within |
| notice-burst-0 | 36.082 | 62 | 32 | 1 | within |
| notice-burst-0 | 36.360 | 62 | 32 | 1 | within |
| notice-burst-0 | 38.205 | 62 | 32 | 1 | within |
| notice-burst-0 | 38.479 | 62 | 32 | 1 | within |
| notice-burst-0 | 40.309 | 62 | 32 | 1 | within |
| notice-burst-0 | 40.586 | 62 | 32 | 1 | within |
| notice-burst-0 | 42.140 | 62 | 32 | 1 | within |
| notice-burst-0 | 42.417 | 62 | 32 | 1 | within |
| notice-burst-0 | 44.044 | 62 | 32 | 1 | within |
| notice-burst-0 | 44.324 | 62 | 32 | 1 | within |
| notice-burst-0 | 46.128 | 62 | 32 | 1 | within |
| notice-burst-0 | 46.402 | 62 | 32 | 1 | within |
| notice-burst-0 | 48.200 | 62 | 32 | 1 | within |
| notice-burst-0 | 48.462 | 62 | 32 | 1 | within |
| notice-burst-0 | 50.190 | 62 | 32 | 1 | within |
| notice-burst-0 | 50.488 | 62 | 32 | 1 | within |
| notice-burst-0 | 52.175 | 62 | 32 | 1 | within |

Latest: 52.175 ms, notice-burst-0.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 303 | 86,744 (0.867) | 48,203 (0.482) |
| notice-burst-0 | 313 | 116,867 (1.169) | 48,203 (0.482) |

Longest pass that carries a step: 116,867 CPU cycles (1.169 ms), notice-burst-0; longest step: 48,203 (0.482 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 239,602 | 2.396 | 62 | 66 | fits | 70,827 | 201 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 270,287 | 2.703 | 62 | 66 | fits | 70,827 | 201 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 630,063 | 6.301 | 62 | 66 | fits | 69,232 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 660,605 | 6.606 | 62 | 66 | fits | 69,232 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 822,117 | 8.221 | 62 | 66 | fits | 68,865 | 203 | 0.146 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 852,589 | 8.526 | 62 | 66 | fits | 68,865 | 203 | 0.146 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 437,676 | 4.377 | 62 | 66 | fits | 70,311 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 468,916 | 4.689 | 62 | 66 | fits | 70,311 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 1,042,100 | 10.421 | 62 | 66 | fits | 68,505 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 1,072,418 | 10.724 | 62 | 66 | fits | 68,505 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 1,231,456 | 12.315 | 62 | 66 | fits | 68,588 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 1,262,004 | 12.620 | 62 | 66 | fits | 68,588 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 1,429,271 | 14.293 | 62 | 66 | fits | 68,754 | 201 | 0.142 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 1,459,893 | 14.599 | 62 | 66 | fits | 68,754 | 201 | 0.142 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 1,618,227 | 16.182 | 62 | 66 | fits | 68,502 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 1,648,776 | 16.488 | 62 | 66 | fits | 68,502 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,835,460 | 18.355 | 62 | 66 | fits | 68,606 | 201 | 0.142 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,866,009 | 18.660 | 62 | 66 | fits | 68,606 | 201 | 0.142 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 2,022,559 | 20.226 | 62 | 66 | fits | 67,517 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 2,053,205 | 20.532 | 62 | 66 | fits | 67,517 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 2,452,042 | 24.520 | 62 | 66 | fits | 36,589 | 101 | 0.250 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 2,832,657 | 28.327 | 62 | 66 | fits | 67,203 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 2,860,773 | 28.608 | 62 | 66 | fits | 67,203 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 3,046,043 | 30.460 | 62 | 66 | fits | 66,709 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 3,074,037 | 30.740 | 62 | 66 | fits | 66,709 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 3,230,645 | 32.306 | 62 | 66 | fits | 66,171 | 201 | 0.130 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 3,258,252 | 32.583 | 62 | 66 | fits | 66,171 | 201 | 0.130 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 3,419,728 | 34.197 | 62 | 66 | fits | 67,512 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 3,448,075 | 34.481 | 62 | 66 | fits | 67,512 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 3,631,252 | 36.313 | 62 | 66 | fits | 66,536 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 3,659,182 | 36.592 | 62 | 66 | fits | 66,536 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 3,841,366 | 38.414 | 62 | 66 | fits | 66,100 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 3,869,421 | 38.694 | 62 | 66 | fits | 66,100 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 4,022,496 | 40.225 | 62 | 66 | fits | 65,395 | 201 | 0.130 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 4,050,110 | 40.501 | 62 | 66 | fits | 65,395 | 201 | 0.130 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 4,258,359 | 42.584 | 62 | 66 | fits | 64,920 | 200 | 0.149 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 4,284,577 | 42.846 | 62 | 66 | fits | 64,920 | 200 | 0.149 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 4,440,017 | 44.400 | 62 | 66 | fits | 62,539 | 200 | 0.103 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 4,469,837 | 44.698 | 62 | 66 | fits | 62,539 | 200 | 0.103 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 4,620,630 | 46.206 | 62 | 66 | fits | 37,238 | 102 | 0.156 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 433,484 | 4.335 | 20 | 200 | fits | 39,693 | 27 | 0.584 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 677,041 | 6.770 | 20 | 20 | fits | 125,667 | 105 | 0.642 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 508,549 | 5.085 | 20 | 24 | fits | 169,848 | 106 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 637,566 | 6.376 | 20 | 50 | fits | 125,667 | 105 | 0.642 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 1,240,809 | 12.408 | 20 | 20 | fits | 64,760 | 26 | 0.753 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 236,598 | 2.366 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 382,284 | 3.823 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 361,227 | 3.612 | 62 | 66 | fits | 67,437 | 203 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 391,048 | 3.910 | 62 | 66 | fits | 67,437 | 203 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 506,435 | 5.064 | 62 | 66 | fits | 116,867 | 212 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 536,687 | 5.367 | 62 | 66 | fits | 116,867 | 212 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 1,825,082 | 18.251 | 62 | 66 | fits | 41,194 | 100 | 0.332 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 2,217,485 | 22.175 | 62 | 66 | fits | 69,094 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 2,246,173 | 22.462 | 62 | 66 | fits | 69,094 | 201 | 0.153 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 2,416,083 | 24.161 | 62 | 66 | fits | 68,917 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 2,444,953 | 24.450 | 62 | 66 | fits | 68,917 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 2,605,840 | 26.058 | 62 | 66 | fits | 68,735 | 201 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 2,634,751 | 26.348 | 62 | 66 | fits | 68,735 | 201 | 0.142 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 2,824,125 | 28.241 | 62 | 66 | fits | 68,991 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 2,853,088 | 28.531 | 62 | 66 | fits | 68,991 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 3,013,256 | 30.133 | 62 | 66 | fits | 68,483 | 201 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 3,042,009 | 30.420 | 62 | 66 | fits | 68,483 | 201 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 3,230,362 | 32.304 | 62 | 66 | fits | 67,973 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 597,741 | 5.977 | 62 | 66 | fits | 71,998 | 201 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 630,219 | 6.302 | 62 | 66 | fits | 71,998 | 201 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 3,258,920 | 32.589 | 62 | 66 | fits | 67,973 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 3,423,197 | 34.232 | 62 | 66 | fits | 67,464 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 286,177 | 2.862 | 62 | 66 | fits | 105,190 | 210 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 320,037 | 3.200 | 62 | 66 | fits | 105,190 | 210 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 3,451,121 | 34.511 | 62 | 66 | fits | 67,464 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 3,608,172 | 36.082 | 62 | 66 | fits | 66,550 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 3,635,962 | 36.360 | 62 | 66 | fits | 66,550 | 201 | 0.135 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 3,820,524 | 38.205 | 62 | 66 | fits | 65,965 | 201 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 3,847,927 | 38.479 | 62 | 66 | fits | 65,965 | 201 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 4,030,890 | 40.309 | 62 | 66 | fits | 66,407 | 201 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 4,058,646 | 40.586 | 62 | 66 | fits | 66,407 | 201 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 4,213,980 | 42.140 | 62 | 66 | fits | 66,157 | 201 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 4,241,656 | 42.417 | 62 | 66 | fits | 66,157 | 201 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 4,404,353 | 44.044 | 62 | 66 | fits | 66,062 | 201 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 4,432,358 | 44.324 | 62 | 66 | fits | 66,062 | 201 | 0.130 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 4,612,816 | 46.128 | 62 | 66 | fits | 65,180 | 201 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 4,640,217 | 46.402 | 62 | 66 | fits | 65,180 | 201 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 4,819,971 | 48.200 | 62 | 66 | fits | 63,847 | 201 | 0.123 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 4,846,189 | 48.462 | 62 | 66 | fits | 63,847 | 201 | 0.123 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 5,019,015 | 50.190 | 62 | 66 | fits | 62,361 | 200 | 0.098 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 5,048,837 | 50.488 | 62 | 66 | fits | 62,361 | 200 | 0.098 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 5,217,520 | 52.175 | 62 | 66 | fits | 38,884 | 102 | 0.218 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 704,352 | 7.044 | 20 | 200 | fits | 151,328 | 80 | 0.595 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 684,084 | 6.841 | 20 | 20 | fits | 151,328 | 80 | 0.595 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 355,225 | 3.552 | 20 | 24 | fits | 159,875 | 110 | 0.477 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 493,281 | 4.933 | 20 | 50 | fits | 157,327 | 243 | 0.374 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 1,136,311 | 11.363 | 20 | 20 | fits | 120,972 | 43 | 0.614 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.acmp.if0` (notice-burst-3) | 5.724 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.adp.if0` (notice-burst-3) | 5.926 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.aecp.if0` (notice-burst-0) | 4.560 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.maap.if0` (notice-burst-3) | 5.329 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.srp.if0` (notice-burst-3) | 10.685 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.267 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.36.0.if0` (notice-burst-6) | 22.325 (22.538) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1637 | 0 | 156,596 (1.566) | fits |
| notice-every-1 | 1633 | 0 | 149,803 (1.498) | fits |
| notice-every-2 | 1625 | 0 | 150,388 (1.504) | fits |
| notice-every-3 | 1629 | 0 | 156,334 (1.563) | fits |
| notice-every-4 | 1631 | 0 | 156,334 (1.563) | fits |
| notice-every-5 | 1632 | 0 | 156,481 (1.565) | fits |
| notice-every-6 | 1628 | 0 | 151,003 (1.510) | fits |
| notice-every-7 | 1624 | 0 | 149,803 (1.498) | fits |
| notice-burst-0 | 1122 | 0 | 156,808 (1.568) | fits |
| notice-burst-1 | 1142 | 0 | 156,956 (1.570) | fits |
| notice-burst-2 | 1103 | 0 | 150,005 (1.500) | fits |
| notice-burst-3 | 1082 | 0 | 158,682 (1.587) | fits |
| notice-burst-4 | 1115 | 0 | 149,962 (1.500) | fits |
| notice-burst-5 | 1118 | 0 | 150,572 (1.506) | fits |
| notice-burst-6 | 1109 | 0 | 150,042 (1.500) | fits |
| notice-burst-7 | 1110 | 0 | 154,293 (1.543) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.170 | 130 | 16 | 2 | within |
| notice-every-0 | 4.379 | 130 | 16 | 2 | within |
| notice-every-0 | 6.123 | 130 | 16 | 2 | within |
| notice-every-0 | 6.335 | 130 | 16 | 2 | within |
| notice-every-0 | 8.236 | 130 | 16 | 2 | within |
| notice-every-0 | 8.443 | 130 | 16 | 2 | within |
| notice-every-0 | 2.203 | 130 | 16 | 2 | within |
| notice-every-0 | 2.420 | 130 | 16 | 2 | within |
| notice-every-0 | 4.567 | 130 | 16 | 2 | within |
| notice-every-0 | 6.511 | 130 | 16 | 2 | within |
| notice-every-0 | 2.628 | 130 | 16 | 2 | within |
| notice-every-0 | 8.646 | 130 | 16 | 2 | within |
| notice-every-1 | 1.907 | 130 | 16 | 2 | within |
| notice-every-1 | 2.116 | 130 | 16 | 2 | within |
| notice-every-1 | 3.862 | 130 | 16 | 2 | within |
| notice-every-1 | 4.074 | 130 | 16 | 2 | within |
| notice-every-1 | 5.996 | 130 | 16 | 2 | within |
| notice-every-1 | 6.204 | 130 | 16 | 2 | within |
| notice-every-1 | 7.908 | 130 | 16 | 2 | within |
| notice-every-1 | 8.116 | 130 | 16 | 2 | within |
| notice-every-1 | 2.305 | 130 | 16 | 2 | within |
| notice-every-1 | 4.254 | 130 | 16 | 2 | within |
| notice-every-1 | 6.407 | 130 | 16 | 2 | within |
| notice-every-1 | 8.317 | 130 | 16 | 2 | within |
| notice-every-2 | 1.908 | 130 | 16 | 2 | within |
| notice-every-2 | 2.117 | 130 | 16 | 2 | within |
| notice-every-2 | 3.863 | 130 | 16 | 2 | within |
| notice-every-2 | 4.075 | 130 | 16 | 2 | within |
| notice-every-2 | 5.997 | 130 | 16 | 2 | within |
| notice-every-2 | 6.205 | 130 | 16 | 2 | within |
| notice-every-2 | 7.909 | 130 | 16 | 2 | within |
| notice-every-2 | 8.117 | 130 | 16 | 2 | within |
| notice-every-2 | 2.306 | 130 | 16 | 2 | within |
| notice-every-2 | 4.255 | 130 | 16 | 2 | within |
| notice-every-2 | 6.408 | 130 | 16 | 2 | within |
| notice-every-2 | 8.318 | 130 | 16 | 2 | within |
| notice-every-3 | 6.005 | 130 | 16 | 2 | within |
| notice-every-3 | 6.213 | 130 | 16 | 2 | within |
| notice-every-3 | 7.906 | 130 | 16 | 2 | within |
| notice-every-3 | 8.117 | 130 | 16 | 2 | within |
| notice-every-3 | 1.906 | 130 | 16 | 2 | within |
| notice-every-3 | 2.120 | 130 | 16 | 2 | within |
| notice-every-3 | 4.092 | 130 | 16 | 2 | within |
| notice-every-3 | 4.305 | 130 | 16 | 2 | within |
| notice-every-3 | 6.397 | 130 | 16 | 2 | within |
| notice-every-3 | 8.292 | 130 | 16 | 2 | within |
| notice-every-3 | 2.329 | 130 | 16 | 2 | within |
| notice-every-3 | 4.515 | 130 | 16 | 2 | within |
| notice-every-4 | 6.189 | 130 | 16 | 2 | within |
| notice-every-4 | 6.399 | 130 | 16 | 2 | within |
| notice-every-4 | 8.113 | 130 | 16 | 2 | within |
| notice-every-4 | 8.324 | 130 | 16 | 2 | within |
| notice-every-4 | 2.080 | 130 | 16 | 2 | within |
| notice-every-4 | 2.295 | 130 | 16 | 2 | within |
| notice-every-4 | 4.056 | 130 | 16 | 2 | within |
| notice-every-4 | 4.269 | 130 | 16 | 2 | within |
| notice-every-4 | 6.582 | 130 | 16 | 2 | within |
| notice-every-4 | 8.498 | 130 | 16 | 2 | within |
| notice-every-4 | 2.504 | 130 | 16 | 2 | within |
| notice-every-4 | 4.480 | 130 | 16 | 2 | within |
| notice-every-5 | 8.400 | 130 | 16 | 2 | within |
| notice-every-5 | 8.610 | 130 | 16 | 2 | within |
| notice-every-5 | 2.264 | 130 | 16 | 2 | within |
| notice-every-5 | 2.479 | 130 | 16 | 2 | within |
| notice-every-5 | 4.218 | 130 | 16 | 2 | within |
| notice-every-5 | 4.430 | 130 | 16 | 2 | within |
| notice-every-5 | 6.351 | 130 | 16 | 2 | within |
| notice-every-5 | 6.563 | 130 | 16 | 2 | within |
| notice-every-5 | 8.791 | 130 | 16 | 2 | within |
| notice-every-5 | 10.238 | 130 | 16 | 2 | within |
| notice-every-5 | 2.689 | 130 | 16 | 2 | within |
| notice-every-5 | 4.641 | 130 | 16 | 2 | within |
| notice-every-6 | 5.978 | 130 | 16 | 2 | within |
| notice-every-6 | 6.186 | 130 | 16 | 2 | within |
| notice-every-6 | 7.878 | 130 | 16 | 2 | within |
| notice-every-6 | 8.089 | 130 | 16 | 2 | within |
| notice-every-6 | 3.884 | 130 | 16 | 2 | within |
| notice-every-6 | 4.095 | 130 | 16 | 2 | within |
| notice-every-6 | 1.907 | 130 | 16 | 2 | within |
| notice-every-6 | 2.123 | 130 | 16 | 2 | within |
| notice-every-6 | 6.369 | 130 | 16 | 2 | within |
| notice-every-6 | 8.264 | 130 | 16 | 2 | within |
| notice-every-6 | 2.331 | 130 | 16 | 2 | within |
| notice-every-6 | 4.306 | 130 | 16 | 2 | within |
| notice-every-7 | 7.908 | 130 | 16 | 2 | within |
| notice-every-7 | 8.115 | 130 | 16 | 2 | within |
| notice-every-7 | 6.060 | 130 | 16 | 2 | within |
| notice-every-7 | 6.274 | 130 | 16 | 2 | within |
| notice-every-7 | 1.955 | 130 | 16 | 2 | within |
| notice-every-7 | 2.169 | 130 | 16 | 2 | within |
| notice-every-7 | 3.930 | 130 | 16 | 2 | within |
| notice-every-7 | 4.143 | 130 | 16 | 2 | within |
| notice-every-7 | 8.296 | 130 | 16 | 2 | within |
| notice-every-7 | 9.921 | 130 | 16 | 2 | within |
| notice-every-7 | 2.378 | 130 | 16 | 2 | within |
| notice-every-7 | 4.353 | 130 | 16 | 2 | within |
| notice-burst-0 | 8.438 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.293 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.515 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.719 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.208 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.415 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.429 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.646 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.597 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.050 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.254 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.594 | 130 | 16 | 1 | within |
| notice-burst-1 | 8.810 | 130 | 16 | 1 | within |
| notice-burst-1 | 14.393 | 130 | 16 | 1 | within |
| notice-burst-1 | 14.614 | 130 | 16 | 1 | within |
| notice-burst-1 | 14.818 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.623 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.837 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.489 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.703 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.121 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.293 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.492 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.701 | 130 | 16 | 1 | within |
| notice-burst-2 | 8.697 | 130 | 16 | 2 | within |
| notice-burst-2 | 14.425 | 130 | 16 | 2 | within |
| notice-burst-2 | 14.645 | 130 | 16 | 2 | within |
| notice-burst-2 | 14.848 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.164 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.375 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.568 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.833 | 130 | 16 | 2 | within |
| notice-burst-2 | 16.146 | 130 | 16 | 2 | within |
| notice-burst-2 | 16.318 | 130 | 16 | 2 | within |
| notice-burst-2 | 16.517 | 130 | 16 | 2 | within |
| notice-burst-2 | 5.576 | 130 | 16 | 2 | within |
| notice-burst-3 | 8.657 | 130 | 16 | 0 | within |
| notice-burst-3 | 13.368 | 130 | 16 | 0 | within |
| notice-burst-3 | 1.903 | 130 | 16 | 0 | within |
| notice-burst-3 | 2.115 | 130 | 16 | 0 | within |
| notice-burst-3 | 2.305 | 130 | 16 | 0 | within |
| notice-burst-3 | 2.563 | 130 | 16 | 0 | within |
| notice-burst-3 | 2.754 | 130 | 16 | 0 | within |
| notice-burst-3 | 2.956 | 130 | 16 | 0 | within |
| notice-burst-3 | 13.557 | 130 | 16 | 0 | within |
| notice-burst-3 | 13.726 | 130 | 16 | 0 | within |
| notice-burst-3 | 14.878 | 130 | 16 | 0 | within |
| notice-burst-3 | 4.818 | 130 | 16 | 0 | within |
| notice-burst-4 | 11.181 | 130 | 16 | 1 | within |
| notice-burst-4 | 11.392 | 130 | 16 | 1 | within |
| notice-burst-4 | 11.589 | 130 | 16 | 1 | within |
| notice-burst-4 | 13.119 | 130 | 16 | 1 | within |
| notice-burst-4 | 2.726 | 130 | 16 | 1 | within |
| notice-burst-4 | 13.327 | 130 | 16 | 1 | within |
| notice-burst-4 | 13.523 | 130 | 16 | 1 | within |
| notice-burst-4 | 15.199 | 130 | 16 | 1 | within |
| notice-burst-4 | 15.385 | 130 | 16 | 1 | within |
| notice-burst-4 | 15.554 | 130 | 16 | 1 | within |
| notice-burst-4 | 17.218 | 130 | 16 | 1 | within |
| notice-burst-4 | 17.423 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.229 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.437 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.634 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.894 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.096 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.309 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.496 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.172 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.083 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.256 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.375 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.577 | 130 | 16 | 1 | within |
| notice-burst-6 | 7.654 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.083 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.303 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.507 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.195 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.402 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.589 | 130 | 16 | 1 | within |
| notice-burst-6 | 20.100 | 130 | 16 | 1 | within |
| notice-burst-6 | 20.286 | 130 | 16 | 1 | within |
| notice-burst-6 | 20.454 | 130 | 16 | 1 | within |
| notice-burst-6 | 22.119 | 130 | 16 | 1 | within |
| notice-burst-6 | 22.325 | 130 | 16 | 1 | within |
| notice-burst-7 | 9.214 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.055 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.277 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.480 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.171 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.383 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.574 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.837 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.123 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.296 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.495 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.565 | 130 | 16 | 1 | within |

Latest: 22.325 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 101,105 (1.011) | 76,094 (0.761) |
| notice-every-1 | 307 | 100,920 (1.009) | 76,094 (0.761) |
| notice-every-2 | 307 | 101,379 (1.014) | 76,094 (0.761) |
| notice-every-3 | 307 | 110,568 (1.106) | 76,442 (0.764) |
| notice-every-4 | 307 | 90,915 (0.909) | 75,843 (0.758) |
| notice-every-5 | 307 | 90,127 (0.901) | 75,680 (0.757) |
| notice-every-6 | 307 | 90,127 (0.901) | 75,843 (0.758) |
| notice-every-7 | 307 | 90,127 (0.901) | 75,843 (0.758) |
| notice-burst-0 | 317 | 102,912 (1.029) | 77,577 (0.776) |
| notice-burst-1 | 317 | 100,920 (1.009) | 77,577 (0.776) |
| notice-burst-2 | 317 | 101,379 (1.014) | 77,577 (0.776) |
| notice-burst-3 | 317 | 110,568 (1.106) | 77,655 (0.777) |
| notice-burst-4 | 317 | 100,459 (1.005) | 77,577 (0.776) |
| notice-burst-5 | 317 | 99,956 (1.000) | 77,577 (0.776) |
| notice-burst-6 | 317 | 99,391 (0.994) | 77,577 (0.776) |
| notice-burst-7 | 317 | 117,084 (1.171) | 77,577 (0.776) |

Longest pass that carries a step: 117,084 CPU cycles (1.171 ms), notice-burst-7; longest step: 77,655 (0.777 ms), notice-burst-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 417,004 | 4.170 | 130 | 134 | fits | 69,540 | 160 | 0.283 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 437,919 | 4.379 | 130 | 134 | fits | 69,540 | 160 | 0.283 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 612,311 | 6.123 | 130 | 134 | fits | 66,215 | 153 | 0.258 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 633,452 | 6.335 | 130 | 134 | fits | 66,215 | 153 | 0.258 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 823,552 | 8.236 | 130 | 134 | fits | 66,629 | 153 | 0.249 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 844,263 | 8.443 | 130 | 134 | fits | 66,629 | 153 | 0.249 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 220,321 | 2.203 | 130 | 134 | fits | 71,880 | 153 | 0.291 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 242,017 | 2.420 | 130 | 134 | fits | 71,880 | 153 | 0.291 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 456,690 | 4.567 | 130 | 134 | fits | 69,540 | 160 | 0.283 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 651,124 | 6.511 | 130 | 134 | fits | 66,215 | 153 | 0.258 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 262,834 | 2.628 | 130 | 134 | fits | 71,880 | 153 | 0.291 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 864,622 | 8.646 | 130 | 134 | fits | 66,629 | 153 | 0.249 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 148,358 | 1.484 | 20 | 200 | fits | 150,153 | 252 | 0.365 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 536,155 | 5.362 | 20 | 20 | fits | 93,575 | 39 | 0.744 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 422,376 | 4.224 | 20 | 24 | fits | 147,987 | 147 | 0.496 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 403,105 | 4.031 | 20 | 50 | fits | 147,987 | 147 | 0.496 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 999,263 | 9.993 | 20 | 20 | fits | 48,492 | 23 | 0.755 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 126,690 | 1.267 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 190,700 | 1.907 | 130 | 134 | fits | 69,160 | 155 | 0.293 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 211,622 | 2.116 | 130 | 134 | fits | 69,160 | 155 | 0.293 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 386,214 | 3.862 | 130 | 134 | fits | 67,758 | 153 | 0.280 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 407,407 | 4.074 | 130 | 134 | fits | 67,758 | 153 | 0.280 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 599,626 | 5.996 | 130 | 134 | fits | 67,488 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 620,383 | 6.204 | 130 | 134 | fits | 67,488 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 790,801 | 7.908 | 130 | 134 | fits | 66,371 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 811,589 | 8.116 | 130 | 134 | fits | 66,371 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 230,528 | 2.305 | 130 | 134 | fits | 69,160 | 155 | 0.293 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 425,399 | 4.254 | 130 | 134 | fits | 67,758 | 153 | 0.280 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 640,711 | 6.407 | 130 | 134 | fits | 67,488 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 831,744 | 8.317 | 130 | 134 | fits | 66,371 | 153 | 0.252 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 138,305 | 1.383 | 20 | 200 | fits | 127,990 | 151 | 0.400 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 531,647 | 5.316 | 20 | 20 | fits | 90,804 | 62 | 0.725 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 410,790 | 4.108 | 20 | 24 | fits | 144,415 | 121 | 0.531 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 492,172 | 4.922 | 20 | 50 | fits | 90,804 | 62 | 0.725 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 962,914 | 9.629 | 20 | 20 | fits | 93,528 | 45 | 0.568 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 102,105 | 1.021 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 190,785 | 1.908 | 130 | 134 | fits | 69,083 | 155 | 0.292 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 211,707 | 2.117 | 130 | 134 | fits | 69,083 | 155 | 0.292 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 386,286 | 3.863 | 130 | 134 | fits | 67,758 | 153 | 0.280 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 407,479 | 4.075 | 130 | 134 | fits | 67,758 | 153 | 0.280 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 599,698 | 5.997 | 130 | 134 | fits | 67,488 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 620,455 | 6.205 | 130 | 134 | fits | 67,488 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 790,887 | 7.909 | 130 | 134 | fits | 66,371 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 811,675 | 8.117 | 130 | 134 | fits | 66,371 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 230,613 | 2.306 | 130 | 134 | fits | 69,083 | 155 | 0.292 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 425,471 | 4.255 | 130 | 134 | fits | 67,758 | 153 | 0.280 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 640,783 | 6.408 | 130 | 134 | fits | 67,488 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 831,830 | 8.318 | 130 | 134 | fits | 66,371 | 153 | 0.252 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 147,976 | 1.480 | 20 | 200 | fits | 148,993 | 250 | 0.371 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 447,893 | 4.479 | 20 | 20 | fits | 150,388 | 132 | 0.518 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 427,689 | 4.277 | 20 | 24 | fits | 150,388 | 132 | 0.518 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 500,180 | 5.002 | 20 | 50 | fits | 91,762 | 53 | 0.718 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,000,253 | 10.003 | 20 | 20 | fits | 37,407 | 19 | 0.815 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 122,887 | 1.229 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 600,524 | 6.005 | 130 | 134 | fits | 66,605 | 153 | 0.274 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 621,321 | 6.213 | 130 | 134 | fits | 66,605 | 153 | 0.274 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 790,629 | 7.906 | 130 | 134 | fits | 65,094 | 153 | 0.253 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 811,724 | 8.117 | 130 | 134 | fits | 65,094 | 153 | 0.253 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 190,615 | 1.906 | 130 | 134 | fits | 71,030 | 155 | 0.278 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 212,018 | 2.120 | 130 | 134 | fits | 71,030 | 155 | 0.278 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 409,246 | 4.092 | 130 | 134 | fits | 70,148 | 153 | 0.273 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 430,507 | 4.305 | 130 | 134 | fits | 70,148 | 153 | 0.273 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 639,698 | 6.397 | 130 | 134 | fits | 66,605 | 153 | 0.274 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 829,182 | 8.292 | 130 | 134 | fits | 65,094 | 153 | 0.253 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 232,917 | 2.329 | 130 | 134 | fits | 71,030 | 155 | 0.278 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 451,535 | 4.515 | 130 | 134 | fits | 70,148 | 153 | 0.273 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 176,381 | 1.764 | 20 | 200 | fits | 145,824 | 282 | 0.370 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 464,443 | 4.644 | 20 | 20 | fits | 151,996 | 121 | 0.517 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 444,239 | 4.442 | 20 | 24 | fits | 151,996 | 121 | 0.517 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 116,638 | 1.166 | 20 | 50 | fits | 145,824 | 282 | 0.370 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,008,702 | 10.087 | 20 | 20 | fits | 37,352 | 19 | 0.814 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 114,712 | 1.147 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 618,879 | 6.189 | 130 | 134 | fits | 66,897 | 153 | 0.276 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 639,868 | 6.399 | 130 | 134 | fits | 66,897 | 153 | 0.276 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 811,273 | 8.113 | 130 | 134 | fits | 64,828 | 151 | 0.249 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 832,368 | 8.324 | 130 | 134 | fits | 64,828 | 151 | 0.249 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 208,019 | 2.080 | 130 | 134 | fits | 71,140 | 153 | 0.284 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 229,495 | 2.295 | 130 | 134 | fits | 71,140 | 153 | 0.284 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 405,649 | 4.056 | 130 | 134 | fits | 70,237 | 153 | 0.276 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 426,933 | 4.269 | 130 | 134 | fits | 70,237 | 153 | 0.276 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 658,245 | 6.582 | 130 | 134 | fits | 66,897 | 153 | 0.276 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 849,826 | 8.498 | 130 | 134 | fits | 64,828 | 151 | 0.249 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 250,394 | 2.504 | 130 | 134 | fits | 71,140 | 153 | 0.284 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 447,961 | 4.480 | 130 | 134 | fits | 70,237 | 153 | 0.276 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 147,259 | 1.473 | 20 | 200 | fits | 148,911 | 253 | 0.368 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 454,715 | 4.547 | 20 | 20 | fits | 151,917 | 139 | 0.516 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 434,511 | 4.345 | 20 | 24 | fits | 151,917 | 139 | 0.516 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 507,176 | 5.072 | 20 | 50 | fits | 91,936 | 53 | 0.719 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,005,660 | 10.057 | 20 | 20 | fits | 37,476 | 19 | 0.816 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 113,396 | 1.134 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 839,986 | 8.400 | 130 | 134 | fits | 66,153 | 152 | 0.274 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 860,978 | 8.610 | 130 | 134 | fits | 66,153 | 152 | 0.274 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 226,392 | 2.264 | 130 | 134 | fits | 72,725 | 153 | 0.297 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 247,897 | 2.479 | 130 | 134 | fits | 72,725 | 153 | 0.297 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 421,819 | 4.218 | 130 | 134 | fits | 70,855 | 160 | 0.265 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 442,965 | 4.430 | 130 | 134 | fits | 70,855 | 160 | 0.265 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 635,122 | 6.351 | 130 | 134 | fits | 47,639 | 103 | 0.304 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 656,287 | 6.563 | 130 | 134 | fits | 47,639 | 103 | 0.304 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 879,141 | 8.791 | 130 | 134 | fits | 66,153 | 152 | 0.274 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 1,023,844 | 10.238 | 130 | 134 | fits | 23,110 | 51 | 0.360 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 268,856 | 2.689 | 130 | 134 | fits | 72,725 | 153 | 0.297 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 464,058 | 4.641 | 130 | 134 | fits | 70,855 | 160 | 0.265 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 148,422 | 1.484 | 20 | 200 | fits | 147,401 | 250 | 0.373 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 454,056 | 4.541 | 20 | 20 | fits | 152,358 | 139 | 0.519 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 433,852 | 4.339 | 20 | 24 | fits | 152,358 | 139 | 0.519 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 506,648 | 5.066 | 20 | 50 | fits | 92,067 | 55 | 0.716 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 974,235 | 9.742 | 20 | 20 | fits | 94,464 | 45 | 0.601 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 119,112 | 1.191 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 597,772 | 5.978 | 130 | 134 | fits | 66,693 | 153 | 0.274 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 618,569 | 6.186 | 130 | 134 | fits | 66,693 | 153 | 0.274 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 787,844 | 7.878 | 130 | 134 | fits | 65,038 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 808,939 | 8.089 | 130 | 134 | fits | 65,038 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 388,384 | 3.884 | 130 | 134 | fits | 70,330 | 155 | 0.273 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 409,538 | 4.095 | 130 | 134 | fits | 70,330 | 155 | 0.273 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 190,750 | 1.907 | 130 | 134 | fits | 71,236 | 155 | 0.272 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 212,285 | 2.123 | 130 | 134 | fits | 71,236 | 155 | 0.272 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 636,946 | 6.369 | 130 | 134 | fits | 66,693 | 153 | 0.274 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 826,397 | 8.264 | 130 | 134 | fits | 65,038 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 233,119 | 2.331 | 130 | 134 | fits | 71,236 | 155 | 0.272 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 430,631 | 4.306 | 130 | 134 | fits | 70,330 | 155 | 0.273 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 170,722 | 1.707 | 20 | 200 | fits | 151,003 | 283 | 0.376 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 470,197 | 4.702 | 20 | 20 | fits | 144,990 | 116 | 0.527 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 449,993 | 4.500 | 20 | 24 | fits | 144,990 | 116 | 0.527 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 110,979 | 1.110 | 20 | 50 | fits | 151,003 | 283 | 0.376 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 984,918 | 9.849 | 20 | 20 | fits | 94,464 | 45 | 0.601 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 114,582 | 1.146 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 790,756 | 7.908 | 130 | 134 | fits | 65,622 | 152 | 0.266 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 811,481 | 8.115 | 130 | 134 | fits | 65,622 | 152 | 0.266 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 605,970 | 6.060 | 130 | 134 | fits | 49,112 | 103 | 0.310 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 627,413 | 6.274 | 130 | 134 | fits | 49,112 | 103 | 0.310 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 195,542 | 1.955 | 130 | 134 | fits | 71,058 | 153 | 0.283 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 216,945 | 2.169 | 130 | 134 | fits | 71,058 | 153 | 0.283 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 393,035 | 3.930 | 130 | 134 | fits | 70,256 | 153 | 0.273 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 414,319 | 4.143 | 130 | 134 | fits | 70,256 | 153 | 0.273 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 829,565 | 8.296 | 130 | 134 | fits | 65,622 | 152 | 0.266 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 992,092 | 9.921 | 130 | 134 | fits | 22,954 | 51 | 0.350 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 237,844 | 2.378 | 130 | 134 | fits | 71,058 | 153 | 0.283 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 435,347 | 4.353 | 130 | 134 | fits | 70,256 | 153 | 0.273 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 171,482 | 1.715 | 20 | 200 | fits | 146,260 | 284 | 0.371 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 548,610 | 5.486 | 20 | 20 | fits | 94,908 | 44 | 0.731 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 433,498 | 4.335 | 20 | 24 | fits | 144,537 | 116 | 0.525 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 111,739 | 1.117 | 20 | 50 | fits | 146,260 | 284 | 0.371 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,008,363 | 10.084 | 20 | 20 | fits | 37,277 | 19 | 0.813 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 119,482 | 1.195 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 843,847 | 8.438 | 130 | 134 | fits | 27,300 | 52 | 0.429 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,529,333 | 15.293 | 130 | 134 | fits | 71,210 | 153 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,551,527 | 15.515 | 130 | 134 | fits | 71,210 | 153 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,571,894 | 15.719 | 130 | 134 | fits | 71,210 | 153 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 1,720,803 | 17.208 | 130 | 134 | fits | 64,863 | 152 | 0.269 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 1,741,454 | 17.415 | 130 | 134 | fits | 64,863 | 152 | 0.269 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 342,878 | 3.429 | 130 | 134 | fits | 50,911 | 102 | 0.335 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 364,575 | 3.646 | 130 | 134 | fits | 50,911 | 102 | 0.335 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,759,696 | 17.597 | 130 | 134 | fits | 64,863 | 152 | 0.269 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,904,994 | 19.050 | 130 | 134 | fits | 43,554 | 102 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,925,439 | 19.254 | 130 | 134 | fits | 43,554 | 102 | 0.271 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 659,389 | 6.594 | 130 | 134 | fits | 28,655 | 53 | 0.415 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 149,259 | 1.493 | 20 | 200 | fits | 147,386 | 249 | 0.383 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 476,201 | 4.762 | 20 | 20 | fits | 134,447 | 146 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 455,997 | 4.560 | 20 | 24 | fits | 134,447 | 146 | 0.509 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 436,726 | 4.367 | 20 | 50 | fits | 134,447 | 146 | 0.509 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 937,225 | 9.372 | 20 | 20 | fits | 79,947 | 34 | 0.600 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 881,048 | 8.810 | 130 | 134 | fits | 29,006 | 51 | 0.487 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,439,286 | 14.393 | 130 | 134 | fits | 70,926 | 153 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,461,404 | 14.614 | 130 | 134 | fits | 70,926 | 153 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,481,785 | 14.818 | 130 | 134 | fits | 70,926 | 153 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 262,284 | 2.623 | 130 | 134 | fits | 50,400 | 102 | 0.339 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 283,750 | 2.837 | 130 | 134 | fits | 50,400 | 102 | 0.339 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 348,947 | 3.489 | 130 | 134 | fits | 62,754 | 111 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 370,294 | 3.703 | 130 | 134 | fits | 62,754 | 111 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,612,068 | 16.121 | 130 | 134 | fits | 60,965 | 152 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,629,291 | 16.293 | 130 | 134 | fits | 60,965 | 152 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,649,202 | 16.492 | 130 | 134 | fits | 60,965 | 152 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 570,091 | 5.701 | 130 | 134 | fits | 28,442 | 52 | 0.422 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 158,044 | 1.580 | 20 | 200 | fits | 147,957 | 261 | 0.383 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 448,165 | 4.482 | 20 | 20 | fits | 124,991 | 111 | 0.527 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 427,961 | 4.280 | 20 | 24 | fits | 124,991 | 111 | 0.527 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 408,690 | 4.087 | 20 | 50 | fits | 124,991 | 111 | 0.527 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 945,258 | 9.453 | 20 | 20 | fits | 79,813 | 34 | 0.600 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 869,656 | 8.697 | 130 | 134 | fits | 29,095 | 51 | 0.494 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,442,531 | 14.425 | 130 | 134 | fits | 70,728 | 153 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,464,455 | 14.645 | 130 | 134 | fits | 70,728 | 153 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,484,836 | 14.848 | 130 | 134 | fits | 70,728 | 153 | 0.317 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 316,380 | 3.164 | 130 | 134 | fits | 81,857 | 161 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 337,545 | 3.375 | 130 | 134 | fits | 81,857 | 161 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 356,793 | 3.568 | 130 | 134 | fits | 81,857 | 161 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 383,258 | 3.833 | 130 | 134 | fits | 26,472 | 53 | 0.282 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,614,583 | 16.146 | 130 | 134 | fits | 60,965 | 152 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,631,806 | 16.318 | 130 | 134 | fits | 60,965 | 152 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,651,717 | 16.517 | 130 | 134 | fits | 60,965 | 152 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 557,624 | 5.576 | 130 | 134 | fits | 27,279 | 52 | 0.362 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 550,349 | 5.503 | 20 | 200 | fits | 134,018 | 231 | 0.378 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 530,081 | 5.301 | 20 | 20 | fits | 134,018 | 231 | 0.378 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 375,859 | 3.759 | 20 | 24 | fits | 148,906 | 157 | 0.487 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 490,606 | 4.906 | 20 | 50 | fits | 134,018 | 231 | 0.378 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,024,842 | 10.248 | 20 | 20 | fits | 90,492 | 38 | 0.563 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 865,669 | 8.657 | 130 | 134 | fits | 30,440 | 52 | 0.526 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,336,760 | 13.368 | 130 | 134 | fits | 63,854 | 152 | 0.278 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 190,295 | 1.903 | 130 | 134 | fits | 82,359 | 161 | 0.290 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 211,486 | 2.115 | 130 | 134 | fits | 82,359 | 161 | 0.290 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 230,455 | 2.305 | 130 | 134 | fits | 82,359 | 161 | 0.290 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 256,288 | 2.563 | 130 | 134 | fits | 64,756 | 153 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 275,375 | 2.754 | 130 | 134 | fits | 64,756 | 153 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 295,575 | 2.956 | 130 | 134 | fits | 64,756 | 153 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,355,675 | 13.557 | 130 | 134 | fits | 63,854 | 152 | 0.278 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,372,640 | 13.726 | 130 | 134 | fits | 63,854 | 152 | 0.278 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,487,824 | 14.878 | 130 | 134 | fits | 26,064 | 52 | 0.360 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 481,848 | 4.818 | 130 | 134 | fits | 26,995 | 53 | 0.360 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 592,623 | 5.926 | 20 | 200 | fits | 118,965 | 195 | 0.392 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 572,355 | 5.724 | 20 | 20 | fits | 118,965 | 195 | 0.392 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 433,186 | 4.332 | 20 | 24 | fits | 149,964 | 181 | 0.472 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 532,880 | 5.329 | 20 | 50 | fits | 118,965 | 195 | 0.392 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,068,517 | 10.685 | 20 | 20 | fits | 79,789 | 34 | 0.600 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,118,051 | 11.181 | 130 | 134 | fits | 71,280 | 152 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,139,210 | 11.392 | 130 | 134 | fits | 71,280 | 152 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,158,876 | 11.589 | 130 | 134 | fits | 71,280 | 152 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,311,905 | 13.119 | 130 | 134 | fits | 67,247 | 153 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 272,627 | 2.726 | 130 | 134 | fits | 28,845 | 52 | 0.489 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,332,701 | 13.327 | 130 | 134 | fits | 67,247 | 153 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,352,286 | 13.523 | 130 | 134 | fits | 67,247 | 153 | 0.244 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,519,879 | 15.199 | 130 | 134 | fits | 62,259 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,538,526 | 15.385 | 130 | 134 | fits | 62,259 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,555,352 | 15.554 | 130 | 134 | fits | 62,259 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,721,805 | 17.218 | 130 | 134 | fits | 46,263 | 103 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,742,325 | 17.423 | 130 | 134 | fits | 46,263 | 103 | 0.263 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 161,266 | 1.613 | 20 | 200 | fits | 146,202 | 261 | 0.387 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 458,190 | 4.582 | 20 | 20 | fits | 141,835 | 123 | 0.514 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 437,986 | 4.380 | 20 | 24 | fits | 141,835 | 123 | 0.514 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 418,715 | 4.187 | 20 | 50 | fits | 141,835 | 123 | 0.514 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 922,986 | 9.230 | 20 | 20 | fits | 80,443 | 34 | 0.603 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 622,858 | 6.229 | 130 | 134 | fits | 83,129 | 161 | 0.309 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 643,677 | 6.437 | 130 | 134 | fits | 83,129 | 161 | 0.309 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 663,396 | 6.634 | 130 | 134 | fits | 83,129 | 161 | 0.309 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 689,384 | 6.894 | 130 | 134 | fits | 61,860 | 152 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,709,571 | 17.096 | 130 | 134 | fits | 68,862 | 153 | 0.308 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,730,875 | 17.309 | 130 | 134 | fits | 68,862 | 153 | 0.308 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,749,625 | 17.496 | 130 | 134 | fits | 68,862 | 153 | 0.308 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,817,191 | 18.172 | 130 | 134 | fits | 66,697 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 708,338 | 7.083 | 130 | 134 | fits | 61,860 | 152 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 725,615 | 7.256 | 130 | 134 | fits | 61,860 | 152 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 1,837,550 | 18.375 | 130 | 134 | fits | 66,697 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 1,857,695 | 18.577 | 130 | 134 | fits | 66,697 | 153 | 0.235 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 569,974 | 5.700 | 20 | 200 | fits | 134,928 | 235 | 0.371 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 549,706 | 5.497 | 20 | 20 | fits | 134,928 | 235 | 0.371 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 394,574 | 3.946 | 20 | 24 | fits | 147,589 | 149 | 0.495 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 510,231 | 5.102 | 20 | 50 | fits | 134,928 | 235 | 0.371 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,009,610 | 10.096 | 20 | 20 | fits | 80,170 | 34 | 0.600 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 765,434 | 7.654 | 130 | 134 | fits | 29,291 | 52 | 0.496 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,608,314 | 16.083 | 130 | 134 | fits | 71,354 | 153 | 0.314 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,630,338 | 16.303 | 130 | 134 | fits | 71,354 | 153 | 0.314 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,650,655 | 16.507 | 130 | 134 | fits | 71,354 | 153 | 0.314 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,819,453 | 18.195 | 130 | 134 | fits | 65,663 | 152 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,840,183 | 18.402 | 130 | 134 | fits | 65,663 | 152 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,858,918 | 18.589 | 130 | 134 | fits | 65,663 | 152 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,009,954 | 20.100 | 130 | 134 | fits | 62,213 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,028,601 | 20.286 | 130 | 134 | fits | 62,213 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,045,362 | 20.454 | 130 | 134 | fits | 62,213 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,211,935 | 22.119 | 130 | 134 | fits | 46,320 | 103 | 0.268 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,232,457 | 22.325 | 130 | 134 | fits | 46,320 | 103 | 0.268 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 155,866 | 1.559 | 20 | 200 | fits | 150,042 | 266 | 0.371 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 454,408 | 4.544 | 20 | 20 | fits | 142,695 | 131 | 0.506 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 434,204 | 4.342 | 20 | 24 | fits | 142,695 | 131 | 0.506 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 414,933 | 4.149 | 20 | 50 | fits | 142,695 | 131 | 0.506 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 917,129 | 9.171 | 20 | 20 | fits | 80,328 | 34 | 0.600 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 921,393 | 9.214 | 130 | 134 | fits | 28,432 | 54 | 0.467 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,605,527 | 16.055 | 130 | 134 | fits | 70,937 | 153 | 0.316 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,627,707 | 16.277 | 130 | 134 | fits | 70,937 | 153 | 0.316 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,648,002 | 16.480 | 130 | 134 | fits | 70,937 | 153 | 0.316 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 217,102 | 2.171 | 130 | 134 | fits | 81,475 | 161 | 0.292 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 238,267 | 2.383 | 130 | 134 | fits | 81,475 | 161 | 0.292 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 257,371 | 2.574 | 130 | 134 | fits | 81,475 | 161 | 0.292 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 283,677 | 2.837 | 130 | 134 | fits | 26,167 | 53 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,712,328 | 17.123 | 130 | 134 | fits | 60,913 | 152 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,729,551 | 17.296 | 130 | 134 | fits | 60,913 | 152 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,749,462 | 17.495 | 130 | 134 | fits | 60,913 | 152 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 356,497 | 3.565 | 130 | 134 | fits | 117,084 | 60 | 0.292 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 149,527 | 1.495 | 20 | 200 | fits | 144,725 | 243 | 0.383 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 446,519 | 4.465 | 20 | 20 | fits | 134,535 | 150 | 0.503 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 426,315 | 4.263 | 20 | 24 | fits | 134,535 | 150 | 0.503 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 407,044 | 4.070 | 20 | 50 | fits | 134,535 | 150 | 0.503 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 905,648 | 9.056 | 20 | 20 | fits | 79,868 | 34 | 0.600 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

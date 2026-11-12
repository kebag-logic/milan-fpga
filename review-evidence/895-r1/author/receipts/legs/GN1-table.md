### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 10.479 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.adp.if0` (notice-burst-2) | 9.676 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.aecp.if0` (notice-burst-4) | 11.174 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.maap.if0` (notice-burst-5) | 10.085 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.srp.if0` (notice-burst-5) | 6.881 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 0.925 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-3.notices.29.9.0.if0` (notice-burst-3) | 12.683 (12.875) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1576 | 0 | 157,786 (1.578) | fits |
| notice-every-1 | 1565 | 0 | 155,719 (1.557) | fits |
| notice-every-2 | 1560 | 0 | 156,265 (1.563) | fits |
| notice-every-3 | 1566 | 0 | 154,696 (1.547) | fits |
| notice-every-4 | 1565 | 0 | 154,842 (1.548) | fits |
| notice-every-5 | 1568 | 0 | 156,449 (1.564) | fits |
| notice-every-6 | 1563 | 0 | 154,846 (1.548) | fits |
| notice-every-7 | 1563 | 0 | 161,566 (1.616) | fits |
| notice-burst-0 | 903 | 0 | 151,406 (1.514) | fits |
| notice-burst-1 | 904 | 0 | 157,597 (1.576) | fits |
| notice-burst-2 | 873 | 0 | 154,452 (1.545) | fits |
| notice-burst-3 | 890 | 0 | 151,791 (1.518) | fits |
| notice-burst-4 | 896 | 0 | 154,548 (1.545) | fits |
| notice-burst-5 | 902 | 0 | 149,928 (1.499) | fits |
| notice-burst-6 | 872 | 0 | 150,403 (1.504) | fits |
| notice-burst-7 | 911 | 0 | 157,419 (1.574) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.190 | 22 | 16 | 2 | within |
| notice-every-0 | 4.395 | 22 | 16 | 2 | within |
| notice-every-0 | 6.208 | 22 | 16 | 2 | within |
| notice-every-0 | 6.413 | 22 | 16 | 2 | within |
| notice-every-0 | 8.288 | 22 | 16 | 2 | within |
| notice-every-0 | 8.487 | 22 | 16 | 2 | within |
| notice-every-0 | 2.124 | 22 | 16 | 2 | within |
| notice-every-0 | 2.335 | 22 | 16 | 2 | within |
| notice-every-0 | 4.582 | 22 | 16 | 2 | within |
| notice-every-0 | 4.754 | 22 | 16 | 2 | within |
| notice-every-0 | 2.542 | 22 | 16 | 2 | within |
| notice-every-0 | 2.750 | 22 | 16 | 2 | within |
| notice-every-1 | 6.337 | 22 | 16 | 2 | within |
| notice-every-1 | 6.538 | 22 | 16 | 2 | within |
| notice-every-1 | 8.358 | 22 | 16 | 2 | within |
| notice-every-1 | 8.562 | 22 | 16 | 2 | within |
| notice-every-1 | 2.277 | 22 | 16 | 2 | within |
| notice-every-1 | 2.486 | 22 | 16 | 2 | within |
| notice-every-1 | 4.370 | 22 | 16 | 2 | within |
| notice-every-1 | 4.579 | 22 | 16 | 2 | within |
| notice-every-1 | 6.723 | 22 | 16 | 2 | within |
| notice-every-1 | 6.893 | 22 | 16 | 2 | within |
| notice-every-1 | 2.693 | 22 | 16 | 2 | within |
| notice-every-1 | 2.902 | 22 | 16 | 2 | within |
| notice-every-2 | 6.338 | 22 | 16 | 2 | within |
| notice-every-2 | 6.539 | 22 | 16 | 2 | within |
| notice-every-2 | 8.359 | 22 | 16 | 2 | within |
| notice-every-2 | 8.563 | 22 | 16 | 2 | within |
| notice-every-2 | 2.277 | 22 | 16 | 2 | within |
| notice-every-2 | 2.486 | 22 | 16 | 2 | within |
| notice-every-2 | 4.371 | 22 | 16 | 2 | within |
| notice-every-2 | 4.580 | 22 | 16 | 2 | within |
| notice-every-2 | 6.724 | 22 | 16 | 2 | within |
| notice-every-2 | 6.894 | 22 | 16 | 2 | within |
| notice-every-2 | 2.693 | 22 | 16 | 2 | within |
| notice-every-2 | 2.901 | 22 | 16 | 2 | within |
| notice-every-3 | 6.337 | 22 | 16 | 2 | within |
| notice-every-3 | 6.538 | 22 | 16 | 2 | within |
| notice-every-3 | 8.358 | 22 | 16 | 2 | within |
| notice-every-3 | 8.562 | 22 | 16 | 2 | within |
| notice-every-3 | 2.277 | 22 | 16 | 2 | within |
| notice-every-3 | 2.485 | 22 | 16 | 2 | within |
| notice-every-3 | 4.369 | 22 | 16 | 2 | within |
| notice-every-3 | 4.578 | 22 | 16 | 2 | within |
| notice-every-3 | 6.723 | 22 | 16 | 2 | within |
| notice-every-3 | 6.893 | 22 | 16 | 2 | within |
| notice-every-3 | 2.693 | 22 | 16 | 2 | within |
| notice-every-3 | 2.901 | 22 | 16 | 2 | within |
| notice-every-4 | 8.164 | 22 | 16 | 1 | within |
| notice-every-4 | 8.364 | 22 | 16 | 1 | within |
| notice-every-4 | 2.020 | 22 | 16 | 1 | within |
| notice-every-4 | 2.230 | 22 | 16 | 1 | within |
| notice-every-4 | 4.262 | 22 | 16 | 1 | within |
| notice-every-4 | 4.469 | 22 | 16 | 1 | within |
| notice-every-4 | 6.220 | 22 | 16 | 1 | within |
| notice-every-4 | 6.422 | 22 | 16 | 1 | within |
| notice-every-4 | 8.547 | 22 | 16 | 1 | within |
| notice-every-4 | 8.715 | 22 | 16 | 1 | within |
| notice-every-4 | 2.438 | 22 | 16 | 1 | within |
| notice-every-4 | 2.646 | 22 | 16 | 1 | within |
| notice-every-5 | 2.279 | 22 | 16 | 2 | within |
| notice-every-5 | 2.483 | 22 | 16 | 2 | within |
| notice-every-5 | 4.734 | 22 | 16 | 2 | within |
| notice-every-5 | 4.943 | 22 | 16 | 2 | within |
| notice-every-5 | 6.402 | 22 | 16 | 2 | within |
| notice-every-5 | 6.602 | 22 | 16 | 2 | within |
| notice-every-5 | 8.322 | 22 | 16 | 2 | within |
| notice-every-5 | 8.522 | 22 | 16 | 2 | within |
| notice-every-5 | 2.669 | 22 | 16 | 2 | within |
| notice-every-5 | 2.844 | 22 | 16 | 2 | within |
| notice-every-5 | 3.047 | 22 | 16 | 2 | within |
| notice-every-5 | 3.253 | 22 | 16 | 2 | within |
| notice-every-6 | 2.127 | 22 | 16 | 2 | within |
| notice-every-6 | 2.331 | 22 | 16 | 2 | within |
| notice-every-6 | 4.583 | 22 | 16 | 2 | within |
| notice-every-6 | 4.793 | 22 | 16 | 2 | within |
| notice-every-6 | 6.250 | 22 | 16 | 2 | within |
| notice-every-6 | 6.450 | 22 | 16 | 2 | within |
| notice-every-6 | 8.138 | 22 | 16 | 2 | within |
| notice-every-6 | 8.338 | 22 | 16 | 2 | within |
| notice-every-6 | 2.518 | 22 | 16 | 2 | within |
| notice-every-6 | 2.693 | 22 | 16 | 2 | within |
| notice-every-6 | 2.896 | 22 | 16 | 2 | within |
| notice-every-6 | 3.102 | 22 | 16 | 2 | within |
| notice-every-7 | 3.098 | 22 | 16 | 2 | within |
| notice-every-7 | 3.305 | 22 | 16 | 2 | within |
| notice-every-7 | 4.155 | 22 | 16 | 2 | within |
| notice-every-7 | 4.359 | 22 | 16 | 2 | within |
| notice-every-7 | 6.214 | 22 | 16 | 2 | within |
| notice-every-7 | 6.415 | 22 | 16 | 2 | within |
| notice-every-7 | 8.255 | 22 | 16 | 2 | within |
| notice-every-7 | 8.454 | 22 | 16 | 2 | within |
| notice-every-7 | 3.497 | 22 | 16 | 2 | within |
| notice-every-7 | 3.672 | 22 | 16 | 2 | within |
| notice-every-7 | 4.565 | 22 | 16 | 2 | within |
| notice-every-7 | 4.769 | 22 | 16 | 2 | within |
| notice-burst-0 | 8.186 | 22 | 16 | 0 | within |
| notice-burst-0 | 8.393 | 22 | 16 | 0 | within |
| notice-burst-0 | 10.586 | 22 | 16 | 0 | within |
| notice-burst-0 | 10.798 | 22 | 16 | 0 | within |
| notice-burst-0 | 10.987 | 22 | 16 | 0 | within |
| notice-burst-0 | 11.184 | 22 | 16 | 0 | within |
| notice-burst-0 | 3.183 | 22 | 16 | 0 | within |
| notice-burst-0 | 3.394 | 22 | 16 | 0 | within |
| notice-burst-0 | 8.584 | 22 | 16 | 0 | within |
| notice-burst-0 | 8.757 | 22 | 16 | 0 | within |
| notice-burst-0 | 8.958 | 22 | 16 | 0 | within |
| notice-burst-0 | 5.004 | 22 | 16 | 0 | within |
| notice-burst-1 | 8.661 | 22 | 16 | 2 | within |
| notice-burst-1 | 8.870 | 22 | 16 | 2 | within |
| notice-burst-1 | 10.710 | 22 | 16 | 2 | within |
| notice-burst-1 | 10.922 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.236 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.443 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.635 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.837 | 22 | 16 | 2 | within |
| notice-burst-1 | 9.056 | 22 | 16 | 2 | within |
| notice-burst-1 | 9.228 | 22 | 16 | 2 | within |
| notice-burst-1 | 9.426 | 22 | 16 | 2 | within |
| notice-burst-1 | 4.244 | 22 | 16 | 2 | within |
| notice-burst-2 | 8.487 | 22 | 16 | 0 | within |
| notice-burst-2 | 8.696 | 22 | 16 | 0 | within |
| notice-burst-2 | 1.892 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.099 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.291 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.490 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.679 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.879 | 22 | 16 | 0 | within |
| notice-burst-2 | 8.879 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.047 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.244 | 22 | 16 | 0 | within |
| notice-burst-2 | 4.667 | 22 | 16 | 0 | within |
| notice-burst-3 | 9.547 | 22 | 16 | 1 | within |
| notice-burst-3 | 9.756 | 22 | 16 | 1 | within |
| notice-burst-3 | 9.955 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.155 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.344 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.541 | 22 | 16 | 1 | within |
| notice-burst-3 | 2.191 | 22 | 16 | 1 | within |
| notice-burst-3 | 2.400 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.723 | 22 | 16 | 1 | within |
| notice-burst-3 | 12.476 | 22 | 16 | 1 | within |
| notice-burst-3 | 12.683 | 22 | 16 | 1 | within |
| notice-burst-3 | 4.209 | 22 | 16 | 1 | within |
| notice-burst-4 | 8.752 | 22 | 16 | 1 | within |
| notice-burst-4 | 8.958 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.158 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.358 | 22 | 16 | 1 | within |
| notice-burst-4 | 11.698 | 22 | 16 | 1 | within |
| notice-burst-4 | 11.904 | 22 | 16 | 1 | within |
| notice-burst-4 | 2.771 | 22 | 16 | 1 | within |
| notice-burst-4 | 2.986 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.545 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.714 | 22 | 16 | 1 | within |
| notice-burst-4 | 9.913 | 22 | 16 | 1 | within |
| notice-burst-4 | 4.756 | 22 | 16 | 1 | within |
| notice-burst-5 | 7.617 | 22 | 16 | 1 | within |
| notice-burst-5 | 7.826 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.024 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.224 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.412 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.611 | 22 | 16 | 1 | within |
| notice-burst-5 | 10.563 | 22 | 16 | 1 | within |
| notice-burst-5 | 10.771 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.796 | 22 | 16 | 1 | within |
| notice-burst-5 | 10.948 | 22 | 16 | 1 | within |
| notice-burst-5 | 11.144 | 22 | 16 | 1 | within |
| notice-burst-5 | 11.341 | 22 | 16 | 1 | within |
| notice-burst-6 | 7.656 | 22 | 16 | 1 | within |
| notice-burst-6 | 7.863 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.062 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.262 | 22 | 16 | 1 | within |
| notice-burst-6 | 10.560 | 22 | 16 | 1 | within |
| notice-burst-6 | 10.765 | 22 | 16 | 1 | within |
| notice-burst-6 | 2.119 | 22 | 16 | 1 | within |
| notice-burst-6 | 2.329 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.448 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.618 | 22 | 16 | 1 | within |
| notice-burst-6 | 8.816 | 22 | 16 | 1 | within |
| notice-burst-6 | 2.538 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.198 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.405 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.604 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.805 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.994 | 22 | 16 | 1 | within |
| notice-burst-7 | 10.191 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.175 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.385 | 22 | 16 | 1 | within |
| notice-burst-7 | 10.374 | 22 | 16 | 1 | within |
| notice-burst-7 | 11.943 | 22 | 16 | 1 | within |
| notice-burst-7 | 12.150 | 22 | 16 | 1 | within |
| notice-burst-7 | 3.985 | 22 | 16 | 1 | within |

Latest: 12.683 ms, notice-burst-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 306 | 98,883 (0.989) | 76,434 (0.764) |
| notice-every-1 | 306 | 103,371 (1.034) | 76,352 (0.764) |
| notice-every-2 | 306 | 108,746 (1.087) | 76,187 (0.762) |
| notice-every-3 | 306 | 89,037 (0.890) | 76,187 (0.762) |
| notice-every-4 | 306 | 89,037 (0.890) | 76,187 (0.762) |
| notice-every-5 | 306 | 89,037 (0.890) | 76,187 (0.762) |
| notice-every-6 | 306 | 89,069 (0.891) | 76,187 (0.762) |
| notice-every-7 | 306 | 161,566 (1.616) | 76,187 (0.762) |
| notice-burst-0 | 316 | 109,121 (1.091) | 78,195 (0.782) |
| notice-burst-1 | 316 | 103,371 (1.034) | 78,195 (0.782) |
| notice-burst-2 | 316 | 108,746 (1.087) | 78,195 (0.782) |
| notice-burst-3 | 316 | 96,389 (0.964) | 78,262 (0.783) |
| notice-burst-4 | 316 | 98,211 (0.982) | 78,262 (0.783) |
| notice-burst-5 | 316 | 101,259 (1.013) | 78,195 (0.782) |
| notice-burst-6 | 316 | 104,467 (1.045) | 78,195 (0.782) |
| notice-burst-7 | 316 | 101,021 (1.010) | 78,195 (0.782) |

Longest pass that carries a step: 161,566 CPU cycles (1.616 ms), notice-every-7; longest step: 78,262 (0.783 ms), notice-burst-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 419,035 | 4.190 | 22 | 26 | fits | 84,266 | 201 | 0.199 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 439,456 | 4.395 | 22 | 26 | fits | 84,266 | 201 | 0.199 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 620,752 | 6.208 | 22 | 26 | fits | 47,714 | 103 | 0.250 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 641,269 | 6.413 | 22 | 26 | fits | 47,714 | 103 | 0.250 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 828,769 | 8.288 | 22 | 26 | fits | 45,566 | 102 | 0.248 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 848,693 | 8.487 | 22 | 26 | fits | 45,566 | 102 | 0.248 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 212,396 | 2.124 | 22 | 26 | fits | 90,895 | 206 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 233,530 | 2.335 | 22 | 26 | fits | 90,895 | 206 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 458,221 | 4.582 | 22 | 26 | fits | 84,266 | 201 | 0.199 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 475,436 | 4.754 | 22 | 26 | fits | 84,266 | 201 | 0.199 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 254,183 | 2.542 | 22 | 26 | fits | 90,895 | 206 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 275,026 | 2.750 | 22 | 26 | fits | 90,895 | 206 | 0.173 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 695,512 | 6.955 | 20 | 200 | fits | 147,319 | 185 | 0.562 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 831,027 | 8.310 | 20 | 20 | fits | 155,783 | 121 | 0.547 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 875,570 | 8.756 | 20 | 24 | fits | 51,327 | 49 | 0.626 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 635,769 | 6.358 | 20 | 50 | fits | 147,319 | 185 | 0.562 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 448,337 | 4.483 | 20 | 20 | fits | 89,276 | 44 | 0.552 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 89,626 | 0.896 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 633,667 | 6.337 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 653,754 | 6.538 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 835,790 | 8.358 | 22 | 26 | fits | 47,277 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 856,189 | 8.562 | 22 | 26 | fits | 47,277 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 227,689 | 2.277 | 22 | 26 | fits | 90,411 | 204 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 248,592 | 2.486 | 22 | 26 | fits | 90,411 | 204 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 436,953 | 4.370 | 22 | 26 | fits | 48,593 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 457,889 | 4.579 | 22 | 26 | fits | 48,593 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 672,288 | 6.723 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 689,272 | 6.893 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 269,310 | 2.693 | 22 | 26 | fits | 90,411 | 204 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 290,153 | 2.902 | 22 | 26 | fits | 90,411 | 204 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 694,538 | 6.945 | 20 | 200 | fits | 146,497 | 178 | 0.566 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 826,395 | 8.264 | 20 | 20 | fits | 152,125 | 121 | 0.568 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 889,948 | 8.899 | 20 | 24 | fits | 66,338 | 57 | 0.591 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 634,795 | 6.348 | 20 | 50 | fits | 146,497 | 178 | 0.566 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 455,986 | 4.560 | 20 | 20 | fits | 89,411 | 43 | 0.551 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 92,516 | 0.925 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 633,791 | 6.338 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 653,878 | 6.539 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 835,931 | 8.359 | 22 | 26 | fits | 47,277 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 856,330 | 8.563 | 22 | 26 | fits | 47,277 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 227,686 | 2.277 | 22 | 26 | fits | 90,411 | 204 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 248,589 | 2.486 | 22 | 26 | fits | 90,411 | 204 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 437,101 | 4.371 | 22 | 26 | fits | 48,593 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 458,037 | 4.580 | 22 | 26 | fits | 48,593 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 672,412 | 6.724 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 689,396 | 6.894 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 269,307 | 2.693 | 22 | 26 | fits | 90,411 | 204 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 290,150 | 2.901 | 22 | 26 | fits | 90,411 | 204 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 713,162 | 7.132 | 20 | 200 | fits | 146,166 | 182 | 0.550 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 858,767 | 8.588 | 20 | 20 | fits | 147,981 | 121 | 0.538 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 888,114 | 8.881 | 20 | 24 | fits | 49,551 | 38 | 0.644 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 653,419 | 6.534 | 20 | 50 | fits | 146,166 | 182 | 0.550 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 471,764 | 4.718 | 20 | 20 | fits | 89,499 | 43 | 0.554 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 74,925 | 0.749 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 633,702 | 6.337 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 653,789 | 6.538 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 835,842 | 8.358 | 22 | 26 | fits | 47,277 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 856,241 | 8.562 | 22 | 26 | fits | 47,277 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 227,661 | 2.277 | 22 | 26 | fits | 90,309 | 204 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 248,539 | 2.485 | 22 | 26 | fits | 90,309 | 204 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 436,873 | 4.369 | 22 | 26 | fits | 48,593 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 457,809 | 4.578 | 22 | 26 | fits | 48,593 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 672,323 | 6.723 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 689,307 | 6.893 | 22 | 26 | fits | 82,558 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 269,257 | 2.693 | 22 | 26 | fits | 90,309 | 204 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 290,100 | 2.901 | 22 | 26 | fits | 90,309 | 204 | 0.172 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 716,053 | 7.161 | 20 | 200 | fits | 144,752 | 167 | 0.565 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 858,067 | 8.581 | 20 | 20 | fits | 148,737 | 115 | 0.575 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 888,218 | 8.882 | 20 | 24 | fits | 50,355 | 42 | 0.636 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 656,310 | 6.563 | 20 | 50 | fits | 144,752 | 167 | 0.565 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 475,889 | 4.759 | 20 | 20 | fits | 89,430 | 43 | 0.553 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 78,718 | 0.787 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 816,396 | 8.164 | 22 | 26 | fits | 81,474 | 201 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 836,412 | 8.364 | 22 | 26 | fits | 81,474 | 201 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 202,028 | 2.020 | 22 | 26 | fits | 91,826 | 206 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 222,978 | 2.230 | 22 | 26 | fits | 91,826 | 206 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 426,171 | 4.262 | 22 | 26 | fits | 48,150 | 102 | 0.286 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 446,885 | 4.469 | 22 | 26 | fits | 48,150 | 102 | 0.286 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 621,965 | 6.220 | 22 | 26 | fits | 46,713 | 103 | 0.243 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 642,191 | 6.422 | 22 | 26 | fits | 46,713 | 103 | 0.243 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 854,715 | 8.547 | 22 | 26 | fits | 81,474 | 201 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 871,468 | 8.715 | 22 | 26 | fits | 81,474 | 201 | 0.172 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 243,775 | 2.438 | 22 | 26 | fits | 91,826 | 206 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 264,618 | 2.646 | 22 | 26 | fits | 91,826 | 206 | 0.177 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 725,012 | 7.250 | 20 | 200 | fits | 148,391 | 183 | 0.554 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 865,169 | 8.652 | 20 | 20 | fits | 146,706 | 113 | 0.540 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 894,147 | 8.941 | 20 | 24 | fits | 49,182 | 38 | 0.638 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 665,269 | 6.653 | 20 | 50 | fits | 148,391 | 183 | 0.554 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 481,239 | 4.812 | 20 | 20 | fits | 90,636 | 49 | 0.547 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 85,749 | 0.857 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 227,852 | 2.279 | 22 | 26 | fits | 126,027 | 303 | 0.146 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 248,269 | 2.483 | 22 | 26 | fits | 126,027 | 303 | 0.146 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 473,398 | 4.734 | 22 | 26 | fits | 48,950 | 103 | 0.281 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 494,346 | 4.943 | 22 | 26 | fits | 48,950 | 103 | 0.281 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 640,162 | 6.402 | 22 | 26 | fits | 45,927 | 102 | 0.251 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 660,159 | 6.602 | 22 | 26 | fits | 45,927 | 102 | 0.251 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 832,188 | 8.322 | 22 | 26 | fits | 45,527 | 103 | 0.241 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 852,183 | 8.522 | 22 | 26 | fits | 45,527 | 103 | 0.241 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 266,935 | 2.669 | 22 | 26 | fits | 126,027 | 303 | 0.146 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 284,383 | 2.844 | 22 | 26 | fits | 126,027 | 303 | 0.146 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 304,715 | 3.047 | 22 | 26 | fits | 126,027 | 303 | 0.146 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 325,335 | 3.253 | 22 | 26 | fits | 126,027 | 303 | 0.146 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 723,448 | 7.234 | 20 | 200 | fits | 150,617 | 190 | 0.556 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 863,891 | 8.639 | 20 | 20 | fits | 146,746 | 127 | 0.559 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 892,999 | 8.930 | 20 | 24 | fits | 49,312 | 36 | 0.647 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 824,416 | 8.244 | 20 | 50 | fits | 146,746 | 127 | 0.559 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 477,089 | 4.771 | 20 | 20 | fits | 90,833 | 51 | 0.548 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 83,286 | 0.833 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 212,721 | 2.127 | 22 | 26 | fits | 126,229 | 305 | 0.148 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 233,138 | 2.331 | 22 | 26 | fits | 126,229 | 305 | 0.148 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 458,333 | 4.583 | 22 | 26 | fits | 48,950 | 103 | 0.281 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 479,281 | 4.793 | 22 | 26 | fits | 48,950 | 103 | 0.281 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 625,030 | 6.250 | 22 | 26 | fits | 45,927 | 102 | 0.251 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 645,027 | 6.450 | 22 | 26 | fits | 45,927 | 102 | 0.251 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 813,755 | 8.138 | 22 | 26 | fits | 45,527 | 103 | 0.241 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 833,750 | 8.338 | 22 | 26 | fits | 45,527 | 103 | 0.241 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 251,804 | 2.518 | 22 | 26 | fits | 126,229 | 305 | 0.148 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 269,252 | 2.693 | 22 | 26 | fits | 126,229 | 305 | 0.148 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 289,584 | 2.896 | 22 | 26 | fits | 126,229 | 305 | 0.148 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 310,204 | 3.102 | 22 | 26 | fits | 126,229 | 305 | 0.148 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 723,222 | 7.232 | 20 | 200 | fits | 153,867 | 175 | 0.553 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 871,729 | 8.717 | 20 | 20 | fits | 154,846 | 119 | 0.549 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 884,552 | 8.846 | 20 | 24 | fits | 33,027 | 24 | 0.738 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 663,479 | 6.635 | 20 | 50 | fits | 153,867 | 175 | 0.553 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 473,940 | 4.739 | 20 | 20 | fits | 90,769 | 49 | 0.552 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 74,941 | 0.749 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 309,787 | 3.098 | 22 | 26 | fits | 161,566 | 202 | 0.194 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 330,541 | 3.305 | 22 | 26 | fits | 161,566 | 202 | 0.194 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 415,470 | 4.155 | 22 | 26 | fits | 89,131 | 206 | 0.151 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 435,943 | 4.359 | 22 | 26 | fits | 89,131 | 206 | 0.151 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 621,398 | 6.214 | 22 | 26 | fits | 45,927 | 102 | 0.251 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 641,523 | 6.415 | 22 | 26 | fits | 45,927 | 102 | 0.251 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 825,460 | 8.255 | 22 | 26 | fits | 45,544 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 845,384 | 8.454 | 22 | 26 | fits | 45,544 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 349,721 | 3.497 | 22 | 26 | fits | 161,566 | 202 | 0.194 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 367,169 | 3.672 | 22 | 26 | fits | 161,566 | 202 | 0.194 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 456,479 | 4.565 | 22 | 26 | fits | 89,131 | 206 | 0.151 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 476,860 | 4.769 | 22 | 26 | fits | 89,131 | 206 | 0.151 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 152,762 | 1.528 | 20 | 200 | fits | 152,873 | 175 | 0.517 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 851,256 | 8.513 | 20 | 20 | fits | 149,062 | 135 | 0.561 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 896,414 | 8.964 | 20 | 24 | fits | 65,362 | 48 | 0.597 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 811,781 | 8.118 | 20 | 50 | fits | 149,062 | 135 | 0.561 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 463,091 | 4.631 | 20 | 20 | fits | 89,522 | 45 | 0.550 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 81,293 | 0.813 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 818,565 | 8.186 | 22 | 26 | fits | 107,102 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 839,336 | 8.393 | 22 | 26 | fits | 107,102 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,058,604 | 10.586 | 22 | 26 | fits | 88,720 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,079,771 | 10.798 | 22 | 26 | fits | 88,720 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 1,098,703 | 10.987 | 22 | 26 | fits | 88,720 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 1,118,426 | 11.184 | 22 | 26 | fits | 88,720 | 203 | 0.215 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 318,271 | 3.183 | 22 | 26 | fits | 49,477 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 339,400 | 3.394 | 22 | 26 | fits | 49,477 | 102 | 0.278 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 858,364 | 8.584 | 22 | 26 | fits | 107,102 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 875,650 | 8.757 | 22 | 26 | fits | 107,102 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 895,751 | 8.958 | 22 | 26 | fits | 107,102 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 500,429 | 5.004 | 22 | 26 | fits | 39,685 | 62 | 0.384 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 893,894 | 8.939 | 20 | 200 | fits | 151,406 | 169 | 0.552 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,020,712 | 10.207 | 20 | 20 | fits | 147,086 | 110 | 0.531 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 1,032,237 | 10.322 | 20 | 24 | fits | 31,729 | 23 | 0.739 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 834,151 | 8.342 | 20 | 50 | fits | 151,406 | 169 | 0.552 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 660,720 | 6.607 | 20 | 20 | fits | 97,704 | 57 | 0.618 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 866,060 | 8.661 | 22 | 26 | fits | 106,122 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 886,981 | 8.870 | 22 | 26 | fits | 106,122 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,071,009 | 10.710 | 22 | 26 | fits | 50,137 | 103 | 0.336 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,092,247 | 10.922 | 22 | 26 | fits | 50,137 | 103 | 0.336 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 223,576 | 2.236 | 22 | 26 | fits | 99,705 | 212 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 244,259 | 2.443 | 22 | 26 | fits | 99,705 | 212 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 263,479 | 2.635 | 22 | 26 | fits | 99,705 | 212 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 283,664 | 2.837 | 22 | 26 | fits | 99,705 | 212 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 905,628 | 9.056 | 22 | 26 | fits | 106,122 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 922,754 | 9.228 | 22 | 26 | fits | 106,122 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 942,553 | 9.426 | 22 | 26 | fits | 106,122 | 252 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 424,363 | 4.244 | 22 | 26 | fits | 39,321 | 61 | 0.394 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 855,726 | 8.557 | 20 | 200 | fits | 153,317 | 172 | 0.584 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 993,055 | 9.931 | 20 | 20 | fits | 157,597 | 117 | 0.550 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 1,004,535 | 10.045 | 20 | 24 | fits | 31,684 | 23 | 0.742 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 795,983 | 7.960 | 20 | 50 | fits | 153,317 | 172 | 0.584 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 570,504 | 5.705 | 20 | 20 | fits | 99,131 | 66 | 0.621 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 848,723 | 8.487 | 22 | 26 | fits | 104,607 | 252 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 869,573 | 8.696 | 22 | 26 | fits | 104,607 | 252 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 189,153 | 1.892 | 22 | 26 | fits | 139,157 | 312 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 209,883 | 2.099 | 22 | 26 | fits | 139,157 | 312 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 229,061 | 2.291 | 22 | 26 | fits | 139,157 | 312 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 249,039 | 2.490 | 22 | 26 | fits | 139,157 | 312 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 267,944 | 2.679 | 22 | 26 | fits | 139,157 | 312 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 287,906 | 2.879 | 22 | 26 | fits | 139,157 | 312 | 0.159 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 887,916 | 8.879 | 22 | 26 | fits | 104,607 | 252 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 904,740 | 9.047 | 22 | 26 | fits | 104,607 | 252 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 924,379 | 9.244 | 22 | 26 | fits | 104,607 | 252 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 466,701 | 4.667 | 22 | 26 | fits | 28,782 | 53 | 0.400 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 967,591 | 9.676 | 20 | 200 | fits | 154,452 | 116 | 0.573 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 947,323 | 9.473 | 20 | 20 | fits | 154,452 | 116 | 0.573 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 974,687 | 9.747 | 20 | 24 | fits | 47,568 | 35 | 0.646 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 753,396 | 7.534 | 20 | 50 | fits | 151,090 | 189 | 0.572 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 475,674 | 4.757 | 20 | 20 | fits | 88,556 | 44 | 0.549 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 954,663 | 9.547 | 22 | 26 | fits | 146,316 | 353 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 975,562 | 9.756 | 22 | 26 | fits | 146,316 | 353 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 995,456 | 9.955 | 22 | 26 | fits | 146,316 | 353 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,015,489 | 10.155 | 22 | 26 | fits | 146,316 | 353 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,034,394 | 10.344 | 22 | 26 | fits | 146,316 | 353 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,054,117 | 10.541 | 22 | 26 | fits | 146,316 | 353 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 219,060 | 2.191 | 22 | 26 | fits | 60,957 | 111 | 0.324 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 239,974 | 2.400 | 22 | 26 | fits | 60,957 | 111 | 0.324 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,072,276 | 10.723 | 22 | 26 | fits | 146,316 | 353 | 0.164 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,247,619 | 12.476 | 22 | 26 | fits | 44,773 | 102 | 0.276 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,268,310 | 12.683 | 22 | 26 | fits | 44,773 | 102 | 0.276 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 420,853 | 4.209 | 22 | 26 | fits | 30,025 | 53 | 0.411 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 740,458 | 7.405 | 20 | 200 | fits | 151,791 | 169 | 0.557 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 1,017,146 | 10.171 | 20 | 20 | fits | 150,640 | 127 | 0.577 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 1,091,474 | 10.915 | 20 | 24 | fits | 49,759 | 44 | 0.643 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 680,715 | 6.807 | 20 | 50 | fits | 151,791 | 169 | 0.557 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 506,899 | 5.069 | 20 | 20 | fits | 88,477 | 42 | 0.548 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 875,208 | 8.752 | 22 | 26 | fits | 144,474 | 353 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 895,832 | 8.958 | 22 | 26 | fits | 144,474 | 353 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 915,806 | 9.158 | 22 | 26 | fits | 144,474 | 353 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 935,839 | 9.358 | 22 | 26 | fits | 144,474 | 353 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,169,787 | 11.698 | 22 | 26 | fits | 47,245 | 103 | 0.302 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,190,368 | 11.904 | 22 | 26 | fits | 47,245 | 103 | 0.302 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 277,055 | 2.771 | 22 | 26 | fits | 51,187 | 102 | 0.335 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 298,584 | 2.986 | 22 | 26 | fits | 51,187 | 102 | 0.335 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 954,452 | 9.545 | 22 | 26 | fits | 144,474 | 353 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 971,438 | 9.714 | 22 | 26 | fits | 144,474 | 353 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 991,251 | 9.913 | 22 | 26 | fits | 144,474 | 353 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 475,621 | 4.756 | 22 | 26 | fits | 30,402 | 53 | 0.411 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 764,876 | 7.649 | 20 | 200 | fits | 154,548 | 180 | 0.573 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 1,040,350 | 10.403 | 20 | 20 | fits | 151,268 | 129 | 0.549 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 1,117,394 | 11.174 | 20 | 24 | fits | 50,003 | 44 | 0.645 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 705,133 | 7.051 | 20 | 50 | fits | 154,548 | 180 | 0.573 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 528,560 | 5.286 | 20 | 20 | fits | 88,851 | 42 | 0.558 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 761,690 | 7.617 | 22 | 26 | fits | 146,860 | 353 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 782,612 | 7.826 | 22 | 26 | fits | 146,860 | 353 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 802,445 | 8.024 | 22 | 26 | fits | 146,860 | 353 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 822,399 | 8.224 | 22 | 26 | fits | 146,860 | 353 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 841,239 | 8.412 | 22 | 26 | fits | 146,860 | 353 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 861,065 | 8.611 | 22 | 26 | fits | 146,860 | 353 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,056,291 | 10.563 | 22 | 26 | fits | 105,416 | 253 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,077,113 | 10.771 | 22 | 26 | fits | 105,416 | 253 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 879,599 | 8.796 | 22 | 26 | fits | 146,860 | 353 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 1,094,839 | 10.948 | 22 | 26 | fits | 105,416 | 253 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 1,114,353 | 11.144 | 22 | 26 | fits | 105,416 | 253 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 1,134,142 | 11.341 | 22 | 26 | fits | 105,416 | 253 | 0.185 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 147,813 | 1.478 | 20 | 200 | fits | 149,794 | 170 | 0.505 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 1,047,928 | 10.479 | 20 | 20 | fits | 148,371 | 126 | 0.530 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 1,074,883 | 10.749 | 20 | 24 | fits | 47,159 | 35 | 0.642 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 1,008,453 | 10.085 | 20 | 50 | fits | 148,371 | 126 | 0.530 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 688,129 | 6.881 | 20 | 20 | fits | 92,856 | 48 | 0.570 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 765,559 | 7.656 | 22 | 26 | fits | 145,031 | 352 | 0.155 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 786,278 | 7.863 | 22 | 26 | fits | 145,031 | 352 | 0.155 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 806,175 | 8.062 | 22 | 26 | fits | 145,031 | 352 | 0.155 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 826,208 | 8.262 | 22 | 26 | fits | 145,031 | 352 | 0.155 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,055,983 | 10.560 | 22 | 26 | fits | 48,045 | 102 | 0.324 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,076,527 | 10.765 | 22 | 26 | fits | 48,045 | 102 | 0.324 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 211,943 | 2.119 | 22 | 26 | fits | 81,484 | 162 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 232,923 | 2.329 | 22 | 26 | fits | 81,484 | 162 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 844,821 | 8.448 | 22 | 26 | fits | 145,031 | 352 | 0.155 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 861,807 | 8.618 | 22 | 26 | fits | 145,031 | 352 | 0.155 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 881,620 | 8.816 | 22 | 26 | fits | 145,031 | 352 | 0.155 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 253,838 | 2.538 | 22 | 26 | fits | 81,484 | 162 | 0.248 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 152,138 | 1.521 | 20 | 200 | fits | 145,857 | 180 | 0.523 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 991,107 | 9.911 | 20 | 20 | fits | 149,664 | 110 | 0.545 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 1,018,130 | 10.181 | 20 | 24 | fits | 47,227 | 35 | 0.643 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 801,968 | 8.020 | 20 | 50 | fits | 150,403 | 173 | 0.564 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 629,540 | 6.295 | 20 | 20 | fits | 92,743 | 48 | 0.568 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 919,770 | 9.198 | 22 | 26 | fits | 147,180 | 355 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 940,541 | 9.405 | 22 | 26 | fits | 147,180 | 355 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 960,436 | 9.604 | 22 | 26 | fits | 147,180 | 355 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 980,540 | 9.805 | 22 | 26 | fits | 147,180 | 355 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 999,445 | 9.994 | 22 | 26 | fits | 147,180 | 355 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 1,019,097 | 10.191 | 22 | 26 | fits | 147,180 | 355 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 217,471 | 2.175 | 22 | 26 | fits | 60,936 | 111 | 0.325 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 238,451 | 2.385 | 22 | 26 | fits | 60,936 | 111 | 0.325 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,037,400 | 10.374 | 22 | 26 | fits | 147,180 | 355 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,194,296 | 11.943 | 22 | 26 | fits | 45,838 | 102 | 0.309 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,214,969 | 12.150 | 22 | 26 | fits | 45,838 | 102 | 0.309 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 398,534 | 3.985 | 22 | 26 | fits | 28,800 | 53 | 0.315 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 878,309 | 8.783 | 20 | 200 | fits | 152,245 | 179 | 0.559 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 1,004,201 | 10.042 | 20 | 20 | fits | 146,160 | 127 | 0.513 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 1,015,494 | 10.155 | 20 | 24 | fits | 31,497 | 23 | 0.738 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 964,726 | 9.647 | 20 | 50 | fits | 146,160 | 127 | 0.513 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 644,296 | 6.443 | 20 | 20 | fits | 96,653 | 57 | 0.615 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

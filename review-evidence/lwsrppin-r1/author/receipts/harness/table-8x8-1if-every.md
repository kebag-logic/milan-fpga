### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 728 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-2.held.acmp.if0` (notice-every-2) | 6.721 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.adp.if0` (notice-burst-5) | 5.889 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-2.held.aecp.if0` (notice-every-2) | 4.927 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-1.held.maap.if0` (notice-every-1) | 6.072 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-3.held.srp.if0` (notice-every-3) | 9.399 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-2.mrpdu.periodic.if0` (notice-every-2) | 1.142 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-7.notices.28.9.0.if0` (notice-burst-7) | 26.218 (26.519) | fits | 1 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1522 | 0 | 161,778 (1.618) | fits |
| notice-every-1 | 1520 | 0 | 161,768 (1.618) | fits |
| notice-every-2 | 1529 | 0 | 161,778 (1.618) | fits |
| notice-every-3 | 1522 | 0 | 161,689 (1.617) | fits |
| notice-every-4 | 1514 | 0 | 162,392 (1.624) | fits |
| notice-every-5 | 1521 | 0 | 161,717 (1.617) | fits |
| notice-every-6 | 1520 | 0 | 161,861 (1.619) | fits |
| notice-every-7 | 1511 | 0 | 158,649 (1.586) | fits |
| notice-burst-0 | 1206 | 0 | 157,372 (1.574) | fits |
| notice-burst-1 | 1205 | 0 | 165,018 (1.650) | fits |
| notice-burst-2 | 1204 | 0 | 157,036 (1.570) | fits |
| notice-burst-3 | 1199 | 0 | 163,684 (1.637) | fits |
| notice-burst-4 | 1199 | 0 | 164,032 (1.640) | fits |
| notice-burst-5 | 1201 | 0 | 163,202 (1.632) | fits |
| notice-burst-6 | 1202 | 0 | 163,237 (1.632) | fits |
| notice-burst-7 | 1191 | 0 | 158,283 (1.583) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.109 | 130 | 16 | 2 | within |
| notice-every-0 | 4.282 | 130 | 16 | 2 | within |
| notice-every-0 | 6.124 | 130 | 16 | 2 | within |
| notice-every-0 | 6.297 | 130 | 16 | 2 | within |
| notice-every-0 | 8.120 | 130 | 16 | 2 | within |
| notice-every-0 | 8.294 | 130 | 16 | 2 | within |
| notice-every-0 | 2.166 | 130 | 16 | 2 | within |
| notice-every-0 | 2.349 | 130 | 16 | 2 | within |
| notice-every-0 | 2.515 | 130 | 16 | 2 | within |
| notice-every-0 | 2.688 | 130 | 16 | 2 | within |
| notice-every-0 | 4.443 | 130 | 16 | 2 | within |
| notice-every-0 | 4.612 | 130 | 16 | 2 | within |
| notice-every-0 | 6.454 | 130 | 16 | 2 | within |
| notice-every-0 | 6.621 | 130 | 16 | 2 | within |
| notice-every-0 | 8.449 | 130 | 16 | 2 | within |
| notice-every-0 | 8.613 | 130 | 16 | 2 | within |
| notice-every-0 | 10.098 | 130 | 16 | 2 | within |
| notice-every-0 | 10.270 | 130 | 16 | 2 | within |
| notice-every-0 | 10.417 | 130 | 16 | 2 | within |
| notice-every-0 | 10.581 | 130 | 16 | 2 | within |
| notice-every-0 | 12.045 | 130 | 16 | 2 | within |
| notice-every-0 | 12.222 | 130 | 16 | 2 | within |
| notice-every-0 | 12.379 | 130 | 16 | 2 | within |
| notice-every-0 | 12.549 | 130 | 16 | 2 | within |
| notice-every-0 | 14.031 | 130 | 16 | 2 | within |
| notice-every-0 | 14.205 | 130 | 16 | 2 | within |
| notice-every-0 | 14.357 | 130 | 16 | 2 | within |
| notice-every-0 | 14.523 | 130 | 16 | 2 | within |
| notice-every-0 | 16.146 | 130 | 16 | 2 | within |
| notice-every-0 | 16.317 | 130 | 16 | 2 | within |
| notice-every-0 | 16.466 | 130 | 16 | 2 | within |
| notice-every-0 | 16.630 | 130 | 16 | 2 | within |
| notice-every-0 | 18.051 | 130 | 16 | 2 | within |
| notice-every-0 | 18.222 | 130 | 16 | 2 | within |
| notice-every-0 | 18.371 | 130 | 16 | 2 | within |
| notice-every-0 | 18.536 | 130 | 16 | 2 | within |
| notice-every-0 | 20.098 | 130 | 16 | 2 | within |
| notice-every-0 | 20.219 | 130 | 16 | 2 | within |
| notice-every-0 | 20.386 | 130 | 16 | 2 | within |
| notice-every-0 | 20.551 | 130 | 16 | 2 | within |
| notice-every-1 | 4.108 | 130 | 16 | 2 | within |
| notice-every-1 | 4.282 | 130 | 16 | 2 | within |
| notice-every-1 | 6.123 | 130 | 16 | 2 | within |
| notice-every-1 | 6.296 | 130 | 16 | 2 | within |
| notice-every-1 | 8.120 | 130 | 16 | 2 | within |
| notice-every-1 | 8.293 | 130 | 16 | 2 | within |
| notice-every-1 | 2.167 | 130 | 16 | 2 | within |
| notice-every-1 | 2.349 | 130 | 16 | 2 | within |
| notice-every-1 | 2.515 | 130 | 16 | 2 | within |
| notice-every-1 | 2.688 | 130 | 16 | 2 | within |
| notice-every-1 | 4.442 | 130 | 16 | 2 | within |
| notice-every-1 | 4.612 | 130 | 16 | 2 | within |
| notice-every-1 | 6.454 | 130 | 16 | 2 | within |
| notice-every-1 | 6.621 | 130 | 16 | 2 | within |
| notice-every-1 | 8.448 | 130 | 16 | 2 | within |
| notice-every-1 | 8.612 | 130 | 16 | 2 | within |
| notice-every-1 | 10.098 | 130 | 16 | 2 | within |
| notice-every-1 | 10.269 | 130 | 16 | 2 | within |
| notice-every-1 | 10.417 | 130 | 16 | 2 | within |
| notice-every-1 | 10.581 | 130 | 16 | 2 | within |
| notice-every-1 | 12.044 | 130 | 16 | 2 | within |
| notice-every-1 | 12.221 | 130 | 16 | 2 | within |
| notice-every-1 | 12.379 | 130 | 16 | 2 | within |
| notice-every-1 | 12.549 | 130 | 16 | 2 | within |
| notice-every-1 | 14.031 | 130 | 16 | 2 | within |
| notice-every-1 | 14.204 | 130 | 16 | 2 | within |
| notice-every-1 | 14.356 | 130 | 16 | 2 | within |
| notice-every-1 | 14.523 | 130 | 16 | 2 | within |
| notice-every-1 | 16.146 | 130 | 16 | 2 | within |
| notice-every-1 | 16.317 | 130 | 16 | 2 | within |
| notice-every-1 | 16.466 | 130 | 16 | 2 | within |
| notice-every-1 | 16.630 | 130 | 16 | 2 | within |
| notice-every-1 | 18.051 | 130 | 16 | 2 | within |
| notice-every-1 | 18.222 | 130 | 16 | 2 | within |
| notice-every-1 | 18.371 | 130 | 16 | 2 | within |
| notice-every-1 | 18.535 | 130 | 16 | 2 | within |
| notice-every-1 | 20.097 | 130 | 16 | 2 | within |
| notice-every-1 | 20.218 | 130 | 16 | 2 | within |
| notice-every-1 | 20.385 | 130 | 16 | 2 | within |
| notice-every-1 | 20.551 | 130 | 16 | 2 | within |
| notice-every-2 | 4.109 | 130 | 16 | 2 | within |
| notice-every-2 | 4.283 | 130 | 16 | 2 | within |
| notice-every-2 | 6.126 | 130 | 16 | 2 | within |
| notice-every-2 | 6.299 | 130 | 16 | 2 | within |
| notice-every-2 | 8.123 | 130 | 16 | 2 | within |
| notice-every-2 | 8.296 | 130 | 16 | 2 | within |
| notice-every-2 | 2.166 | 130 | 16 | 2 | within |
| notice-every-2 | 2.349 | 130 | 16 | 2 | within |
| notice-every-2 | 2.515 | 130 | 16 | 2 | within |
| notice-every-2 | 2.688 | 130 | 16 | 2 | within |
| notice-every-2 | 4.443 | 130 | 16 | 2 | within |
| notice-every-2 | 4.613 | 130 | 16 | 2 | within |
| notice-every-2 | 6.457 | 130 | 16 | 2 | within |
| notice-every-2 | 6.624 | 130 | 16 | 2 | within |
| notice-every-2 | 8.451 | 130 | 16 | 2 | within |
| notice-every-2 | 8.615 | 130 | 16 | 2 | within |
| notice-every-2 | 10.102 | 130 | 16 | 2 | within |
| notice-every-2 | 10.273 | 130 | 16 | 2 | within |
| notice-every-2 | 10.421 | 130 | 16 | 2 | within |
| notice-every-2 | 10.585 | 130 | 16 | 2 | within |
| notice-every-2 | 12.239 | 130 | 16 | 2 | within |
| notice-every-2 | 12.417 | 130 | 16 | 2 | within |
| notice-every-2 | 12.574 | 130 | 16 | 2 | within |
| notice-every-2 | 12.744 | 130 | 16 | 2 | within |
| notice-every-2 | 14.226 | 130 | 16 | 2 | within |
| notice-every-2 | 14.399 | 130 | 16 | 2 | within |
| notice-every-2 | 14.552 | 130 | 16 | 2 | within |
| notice-every-2 | 14.718 | 130 | 16 | 2 | within |
| notice-every-2 | 16.153 | 130 | 16 | 2 | within |
| notice-every-2 | 16.324 | 130 | 16 | 2 | within |
| notice-every-2 | 16.472 | 130 | 16 | 2 | within |
| notice-every-2 | 16.637 | 130 | 16 | 2 | within |
| notice-every-2 | 18.244 | 130 | 16 | 2 | within |
| notice-every-2 | 18.416 | 130 | 16 | 2 | within |
| notice-every-2 | 18.565 | 130 | 16 | 2 | within |
| notice-every-2 | 18.729 | 130 | 16 | 2 | within |
| notice-every-2 | 20.107 | 130 | 16 | 2 | within |
| notice-every-2 | 20.229 | 130 | 16 | 2 | within |
| notice-every-2 | 20.396 | 130 | 16 | 2 | within |
| notice-every-2 | 20.561 | 130 | 16 | 2 | within |
| notice-every-3 | 8.228 | 130 | 16 | 2 | within |
| notice-every-3 | 8.401 | 130 | 16 | 2 | within |
| notice-every-3 | 2.307 | 130 | 16 | 2 | within |
| notice-every-3 | 2.485 | 130 | 16 | 2 | within |
| notice-every-3 | 6.184 | 130 | 16 | 2 | within |
| notice-every-3 | 6.360 | 130 | 16 | 2 | within |
| notice-every-3 | 4.159 | 130 | 16 | 2 | within |
| notice-every-3 | 4.337 | 130 | 16 | 2 | within |
| notice-every-3 | 2.651 | 130 | 16 | 2 | within |
| notice-every-3 | 2.824 | 130 | 16 | 2 | within |
| notice-every-3 | 4.498 | 130 | 16 | 2 | within |
| notice-every-3 | 4.668 | 130 | 16 | 2 | within |
| notice-every-3 | 6.517 | 130 | 16 | 2 | within |
| notice-every-3 | 6.684 | 130 | 16 | 2 | within |
| notice-every-3 | 8.556 | 130 | 16 | 2 | within |
| notice-every-3 | 8.720 | 130 | 16 | 2 | within |
| notice-every-3 | 10.001 | 130 | 16 | 2 | within |
| notice-every-3 | 10.172 | 130 | 16 | 2 | within |
| notice-every-3 | 10.320 | 130 | 16 | 2 | within |
| notice-every-3 | 10.484 | 130 | 16 | 2 | within |
| notice-every-3 | 12.139 | 130 | 16 | 2 | within |
| notice-every-3 | 12.317 | 130 | 16 | 2 | within |
| notice-every-3 | 12.474 | 130 | 16 | 2 | within |
| notice-every-3 | 12.644 | 130 | 16 | 2 | within |
| notice-every-3 | 14.126 | 130 | 16 | 2 | within |
| notice-every-3 | 14.299 | 130 | 16 | 2 | within |
| notice-every-3 | 14.452 | 130 | 16 | 2 | within |
| notice-every-3 | 14.618 | 130 | 16 | 2 | within |
| notice-every-3 | 16.053 | 130 | 16 | 2 | within |
| notice-every-3 | 16.224 | 130 | 16 | 2 | within |
| notice-every-3 | 16.372 | 130 | 16 | 2 | within |
| notice-every-3 | 16.537 | 130 | 16 | 2 | within |
| notice-every-3 | 18.144 | 130 | 16 | 2 | within |
| notice-every-3 | 18.316 | 130 | 16 | 2 | within |
| notice-every-3 | 18.465 | 130 | 16 | 2 | within |
| notice-every-3 | 18.629 | 130 | 16 | 2 | within |
| notice-every-3 | 20.007 | 130 | 16 | 2 | within |
| notice-every-3 | 20.129 | 130 | 16 | 2 | within |
| notice-every-3 | 20.296 | 130 | 16 | 2 | within |
| notice-every-3 | 20.461 | 130 | 16 | 2 | within |
| notice-every-4 | 7.959 | 130 | 16 | 1 | within |
| notice-every-4 | 8.132 | 130 | 16 | 1 | within |
| notice-every-4 | 1.995 | 130 | 16 | 1 | within |
| notice-every-4 | 2.174 | 130 | 16 | 1 | within |
| notice-every-4 | 3.938 | 130 | 16 | 1 | within |
| notice-every-4 | 4.113 | 130 | 16 | 1 | within |
| notice-every-4 | 5.957 | 130 | 16 | 1 | within |
| notice-every-4 | 6.134 | 130 | 16 | 1 | within |
| notice-every-4 | 2.340 | 130 | 16 | 1 | within |
| notice-every-4 | 2.513 | 130 | 16 | 1 | within |
| notice-every-4 | 4.273 | 130 | 16 | 1 | within |
| notice-every-4 | 4.443 | 130 | 16 | 1 | within |
| notice-every-4 | 6.291 | 130 | 16 | 1 | within |
| notice-every-4 | 6.459 | 130 | 16 | 1 | within |
| notice-every-4 | 8.287 | 130 | 16 | 1 | within |
| notice-every-4 | 8.452 | 130 | 16 | 1 | within |
| notice-every-4 | 9.938 | 130 | 16 | 1 | within |
| notice-every-4 | 10.109 | 130 | 16 | 1 | within |
| notice-every-4 | 10.256 | 130 | 16 | 1 | within |
| notice-every-4 | 10.421 | 130 | 16 | 1 | within |
| notice-every-4 | 12.076 | 130 | 16 | 1 | within |
| notice-every-4 | 12.253 | 130 | 16 | 1 | within |
| notice-every-4 | 12.410 | 130 | 16 | 1 | within |
| notice-every-4 | 12.581 | 130 | 16 | 1 | within |
| notice-every-4 | 14.062 | 130 | 16 | 1 | within |
| notice-every-4 | 14.236 | 130 | 16 | 1 | within |
| notice-every-4 | 14.388 | 130 | 16 | 1 | within |
| notice-every-4 | 14.555 | 130 | 16 | 1 | within |
| notice-every-4 | 15.989 | 130 | 16 | 1 | within |
| notice-every-4 | 16.160 | 130 | 16 | 1 | within |
| notice-every-4 | 16.309 | 130 | 16 | 1 | within |
| notice-every-4 | 16.473 | 130 | 16 | 1 | within |
| notice-every-4 | 18.081 | 130 | 16 | 1 | within |
| notice-every-4 | 18.252 | 130 | 16 | 1 | within |
| notice-every-4 | 18.401 | 130 | 16 | 1 | within |
| notice-every-4 | 18.565 | 130 | 16 | 1 | within |
| notice-every-4 | 19.944 | 130 | 16 | 1 | within |
| notice-every-4 | 20.065 | 130 | 16 | 1 | within |
| notice-every-4 | 20.232 | 130 | 16 | 1 | within |
| notice-every-4 | 20.397 | 130 | 16 | 1 | within |
| notice-every-5 | 8.173 | 130 | 16 | 2 | within |
| notice-every-5 | 8.346 | 130 | 16 | 2 | within |
| notice-every-5 | 2.209 | 130 | 16 | 2 | within |
| notice-every-5 | 2.387 | 130 | 16 | 2 | within |
| notice-every-5 | 4.151 | 130 | 16 | 2 | within |
| notice-every-5 | 4.326 | 130 | 16 | 2 | within |
| notice-every-5 | 6.170 | 130 | 16 | 2 | within |
| notice-every-5 | 6.347 | 130 | 16 | 2 | within |
| notice-every-5 | 2.553 | 130 | 16 | 2 | within |
| notice-every-5 | 2.727 | 130 | 16 | 2 | within |
| notice-every-5 | 4.486 | 130 | 16 | 2 | within |
| notice-every-5 | 4.656 | 130 | 16 | 2 | within |
| notice-every-5 | 6.505 | 130 | 16 | 2 | within |
| notice-every-5 | 6.672 | 130 | 16 | 2 | within |
| notice-every-5 | 8.501 | 130 | 16 | 2 | within |
| notice-every-5 | 8.666 | 130 | 16 | 2 | within |
| notice-every-5 | 10.150 | 130 | 16 | 2 | within |
| notice-every-5 | 10.321 | 130 | 16 | 2 | within |
| notice-every-5 | 10.469 | 130 | 16 | 2 | within |
| notice-every-5 | 10.633 | 130 | 16 | 2 | within |
| notice-every-5 | 12.097 | 130 | 16 | 2 | within |
| notice-every-5 | 12.274 | 130 | 16 | 2 | within |
| notice-every-5 | 12.432 | 130 | 16 | 2 | within |
| notice-every-5 | 12.602 | 130 | 16 | 2 | within |
| notice-every-5 | 14.084 | 130 | 16 | 2 | within |
| notice-every-5 | 14.257 | 130 | 16 | 2 | within |
| notice-every-5 | 14.409 | 130 | 16 | 2 | within |
| notice-every-5 | 14.576 | 130 | 16 | 2 | within |
| notice-every-5 | 16.199 | 130 | 16 | 2 | within |
| notice-every-5 | 16.370 | 130 | 16 | 2 | within |
| notice-every-5 | 16.518 | 130 | 16 | 2 | within |
| notice-every-5 | 16.683 | 130 | 16 | 2 | within |
| notice-every-5 | 18.104 | 130 | 16 | 2 | within |
| notice-every-5 | 18.275 | 130 | 16 | 2 | within |
| notice-every-5 | 18.424 | 130 | 16 | 2 | within |
| notice-every-5 | 18.588 | 130 | 16 | 2 | within |
| notice-every-5 | 20.150 | 130 | 16 | 2 | within |
| notice-every-5 | 20.271 | 130 | 16 | 2 | within |
| notice-every-5 | 20.438 | 130 | 16 | 2 | within |
| notice-every-5 | 20.604 | 130 | 16 | 2 | within |
| notice-every-6 | 2.162 | 130 | 16 | 2 | within |
| notice-every-6 | 2.339 | 130 | 16 | 2 | within |
| notice-every-6 | 4.296 | 130 | 16 | 2 | within |
| notice-every-6 | 4.468 | 130 | 16 | 2 | within |
| notice-every-6 | 6.355 | 130 | 16 | 2 | within |
| notice-every-6 | 6.528 | 130 | 16 | 2 | within |
| notice-every-6 | 8.144 | 130 | 16 | 2 | within |
| notice-every-6 | 8.316 | 130 | 16 | 2 | within |
| notice-every-6 | 2.505 | 130 | 16 | 2 | within |
| notice-every-6 | 2.678 | 130 | 16 | 2 | within |
| notice-every-6 | 4.629 | 130 | 16 | 2 | within |
| notice-every-6 | 4.799 | 130 | 16 | 2 | within |
| notice-every-6 | 6.686 | 130 | 16 | 2 | within |
| notice-every-6 | 6.853 | 130 | 16 | 2 | within |
| notice-every-6 | 8.471 | 130 | 16 | 2 | within |
| notice-every-6 | 8.635 | 130 | 16 | 2 | within |
| notice-every-6 | 10.121 | 130 | 16 | 2 | within |
| notice-every-6 | 10.292 | 130 | 16 | 2 | within |
| notice-every-6 | 10.440 | 130 | 16 | 2 | within |
| notice-every-6 | 10.604 | 130 | 16 | 2 | within |
| notice-every-6 | 12.259 | 130 | 16 | 2 | within |
| notice-every-6 | 12.436 | 130 | 16 | 2 | within |
| notice-every-6 | 12.593 | 130 | 16 | 2 | within |
| notice-every-6 | 12.763 | 130 | 16 | 2 | within |
| notice-every-6 | 14.245 | 130 | 16 | 2 | within |
| notice-every-6 | 14.419 | 130 | 16 | 2 | within |
| notice-every-6 | 14.571 | 130 | 16 | 2 | within |
| notice-every-6 | 14.737 | 130 | 16 | 2 | within |
| notice-every-6 | 16.172 | 130 | 16 | 2 | within |
| notice-every-6 | 16.343 | 130 | 16 | 2 | within |
| notice-every-6 | 16.492 | 130 | 16 | 2 | within |
| notice-every-6 | 16.656 | 130 | 16 | 2 | within |
| notice-every-6 | 18.264 | 130 | 16 | 2 | within |
| notice-every-6 | 18.435 | 130 | 16 | 2 | within |
| notice-every-6 | 18.584 | 130 | 16 | 2 | within |
| notice-every-6 | 18.748 | 130 | 16 | 2 | within |
| notice-every-6 | 20.127 | 130 | 16 | 2 | within |
| notice-every-6 | 20.249 | 130 | 16 | 2 | within |
| notice-every-6 | 20.416 | 130 | 16 | 2 | within |
| notice-every-6 | 20.581 | 130 | 16 | 2 | within |
| notice-every-7 | 4.109 | 130 | 16 | 2 | within |
| notice-every-7 | 4.282 | 130 | 16 | 2 | within |
| notice-every-7 | 6.123 | 130 | 16 | 2 | within |
| notice-every-7 | 6.296 | 130 | 16 | 2 | within |
| notice-every-7 | 8.119 | 130 | 16 | 2 | within |
| notice-every-7 | 8.292 | 130 | 16 | 2 | within |
| notice-every-7 | 2.167 | 130 | 16 | 2 | within |
| notice-every-7 | 2.349 | 130 | 16 | 2 | within |
| notice-every-7 | 2.514 | 130 | 16 | 2 | within |
| notice-every-7 | 2.688 | 130 | 16 | 2 | within |
| notice-every-7 | 4.443 | 130 | 16 | 2 | within |
| notice-every-7 | 4.612 | 130 | 16 | 2 | within |
| notice-every-7 | 6.453 | 130 | 16 | 2 | within |
| notice-every-7 | 6.621 | 130 | 16 | 2 | within |
| notice-every-7 | 8.447 | 130 | 16 | 2 | within |
| notice-every-7 | 8.612 | 130 | 16 | 2 | within |
| notice-every-7 | 10.099 | 130 | 16 | 2 | within |
| notice-every-7 | 10.270 | 130 | 16 | 2 | within |
| notice-every-7 | 10.417 | 130 | 16 | 2 | within |
| notice-every-7 | 10.581 | 130 | 16 | 2 | within |
| notice-every-7 | 12.236 | 130 | 16 | 2 | within |
| notice-every-7 | 12.413 | 130 | 16 | 2 | within |
| notice-every-7 | 12.571 | 130 | 16 | 2 | within |
| notice-every-7 | 12.741 | 130 | 16 | 2 | within |
| notice-every-7 | 14.223 | 130 | 16 | 2 | within |
| notice-every-7 | 14.396 | 130 | 16 | 2 | within |
| notice-every-7 | 14.548 | 130 | 16 | 2 | within |
| notice-every-7 | 14.715 | 130 | 16 | 2 | within |
| notice-every-7 | 16.149 | 130 | 16 | 2 | within |
| notice-every-7 | 16.321 | 130 | 16 | 2 | within |
| notice-every-7 | 16.469 | 130 | 16 | 2 | within |
| notice-every-7 | 16.633 | 130 | 16 | 2 | within |
| notice-every-7 | 18.241 | 130 | 16 | 2 | within |
| notice-every-7 | 18.412 | 130 | 16 | 2 | within |
| notice-every-7 | 18.561 | 130 | 16 | 2 | within |
| notice-every-7 | 18.726 | 130 | 16 | 2 | within |
| notice-every-7 | 20.104 | 130 | 16 | 2 | within |
| notice-every-7 | 20.225 | 130 | 16 | 2 | within |
| notice-every-7 | 20.392 | 130 | 16 | 2 | within |
| notice-every-7 | 20.558 | 130 | 16 | 2 | within |
| notice-burst-0 | 2.226 | 130 | 16 | 0 | within |
| notice-burst-0 | 2.402 | 130 | 16 | 0 | within |
| notice-burst-0 | 2.556 | 130 | 16 | 0 | within |
| notice-burst-0 | 2.721 | 130 | 16 | 0 | within |
| notice-burst-0 | 2.995 | 130 | 16 | 0 | within |
| notice-burst-0 | 3.164 | 130 | 16 | 0 | within |
| notice-burst-0 | 5.061 | 130 | 16 | 0 | within |
| notice-burst-0 | 5.229 | 130 | 16 | 0 | within |
| notice-burst-0 | 14.682 | 130 | 16 | 0 | within |
| notice-burst-0 | 14.860 | 130 | 16 | 0 | within |
| notice-burst-0 | 15.018 | 130 | 16 | 0 | within |
| notice-burst-0 | 15.184 | 130 | 16 | 0 | within |
| notice-burst-0 | 16.656 | 130 | 16 | 0 | within |
| notice-burst-0 | 16.830 | 130 | 16 | 0 | within |
| notice-burst-0 | 3.328 | 130 | 16 | 0 | within |
| notice-burst-0 | 3.503 | 130 | 16 | 0 | within |
| notice-burst-0 | 4.293 | 130 | 16 | 0 | within |
| notice-burst-0 | 4.474 | 130 | 16 | 0 | within |
| notice-burst-0 | 16.981 | 130 | 16 | 0 | within |
| notice-burst-0 | 17.148 | 130 | 16 | 0 | within |
| notice-burst-0 | 4.637 | 130 | 16 | 0 | within |
| notice-burst-0 | 4.817 | 130 | 16 | 0 | within |
| notice-burst-0 | 5.390 | 130 | 16 | 0 | within |
| notice-burst-0 | 5.569 | 130 | 16 | 0 | within |
| notice-burst-0 | 18.790 | 130 | 16 | 0 | within |
| notice-burst-0 | 18.963 | 130 | 16 | 0 | within |
| notice-burst-0 | 19.115 | 130 | 16 | 0 | within |
| notice-burst-0 | 19.282 | 130 | 16 | 0 | within |
| notice-burst-0 | 20.716 | 130 | 16 | 0 | within |
| notice-burst-0 | 20.886 | 130 | 16 | 0 | within |
| notice-burst-0 | 21.035 | 130 | 16 | 0 | within |
| notice-burst-0 | 21.199 | 130 | 16 | 0 | within |
| notice-burst-0 | 22.657 | 130 | 16 | 0 | within |
| notice-burst-0 | 22.827 | 130 | 16 | 0 | within |
| notice-burst-0 | 22.976 | 130 | 16 | 0 | within |
| notice-burst-0 | 23.141 | 130 | 16 | 0 | within |
| notice-burst-0 | 24.706 | 130 | 16 | 0 | within |
| notice-burst-0 | 24.827 | 130 | 16 | 0 | within |
| notice-burst-0 | 24.994 | 130 | 16 | 0 | within |
| notice-burst-0 | 25.158 | 130 | 16 | 0 | within |
| notice-burst-1 | 3.630 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.803 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.433 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.601 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.504 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.673 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.826 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.992 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.797 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.976 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.134 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.302 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.765 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.941 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.722 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.903 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.202 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.376 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.526 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.693 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.067 | 130 | 16 | 1 | within |
| notice-burst-1 | 6.250 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.324 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.499 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.211 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.415 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.982 | 130 | 16 | 1 | within |
| notice-burst-1 | 4.176 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.651 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.816 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.602 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.805 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.238 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.409 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.558 | 130 | 16 | 1 | within |
| notice-burst-1 | 21.723 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.140 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.261 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.428 | 130 | 16 | 1 | within |
| notice-burst-1 | 23.592 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.646 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.820 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.441 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.609 | 130 | 16 | 1 | within |
| notice-burst-2 | 14.854 | 130 | 16 | 1 | within |
| notice-burst-2 | 15.031 | 130 | 16 | 1 | within |
| notice-burst-2 | 15.187 | 130 | 16 | 1 | within |
| notice-burst-2 | 15.353 | 130 | 16 | 1 | within |
| notice-burst-2 | 16.067 | 130 | 16 | 1 | within |
| notice-burst-2 | 16.242 | 130 | 16 | 1 | within |
| notice-burst-2 | 16.400 | 130 | 16 | 1 | within |
| notice-burst-2 | 16.568 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.774 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.949 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.022 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.195 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.354 | 130 | 16 | 1 | within |
| notice-burst-2 | 18.520 | 130 | 16 | 1 | within |
| notice-burst-2 | 2.452 | 130 | 16 | 1 | within |
| notice-burst-2 | 2.646 | 130 | 16 | 1 | within |
| notice-burst-2 | 2.821 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.011 | 130 | 16 | 1 | within |
| notice-burst-2 | 19.961 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.135 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.299 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.493 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.668 | 130 | 16 | 1 | within |
| notice-burst-2 | 3.859 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.992 | 130 | 16 | 1 | within |
| notice-burst-2 | 5.180 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.287 | 130 | 16 | 1 | within |
| notice-burst-2 | 20.452 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.062 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.232 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.381 | 130 | 16 | 1 | within |
| notice-burst-2 | 22.546 | 130 | 16 | 1 | within |
| notice-burst-2 | 23.962 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.083 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.250 | 130 | 16 | 1 | within |
| notice-burst-2 | 24.414 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.365 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.535 | 130 | 16 | 1 | within |
| notice-burst-3 | 14.729 | 130 | 16 | 1 | within |
| notice-burst-3 | 14.905 | 130 | 16 | 1 | within |
| notice-burst-3 | 15.064 | 130 | 16 | 1 | within |
| notice-burst-3 | 15.230 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.133 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.307 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.466 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.633 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.700 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.876 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.085 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.258 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.414 | 130 | 16 | 1 | within |
| notice-burst-3 | 18.582 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.214 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.385 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.565 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.757 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.171 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.371 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.549 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.741 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.022 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.213 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.385 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.574 | 130 | 16 | 1 | within |
| notice-burst-3 | 4.930 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.117 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.535 | 130 | 16 | 1 | within |
| notice-burst-3 | 20.700 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.125 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.296 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.445 | 130 | 16 | 1 | within |
| notice-burst-3 | 22.610 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.073 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.194 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.361 | 130 | 16 | 1 | within |
| notice-burst-3 | 24.526 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.438 | 130 | 16 | 0 | within |
| notice-burst-4 | 14.616 | 130 | 16 | 0 | within |
| notice-burst-4 | 14.772 | 130 | 16 | 0 | within |
| notice-burst-4 | 14.937 | 130 | 16 | 0 | within |
| notice-burst-4 | 15.840 | 130 | 16 | 0 | within |
| notice-burst-4 | 16.015 | 130 | 16 | 0 | within |
| notice-burst-4 | 16.172 | 130 | 16 | 0 | within |
| notice-burst-4 | 16.339 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.905 | 130 | 16 | 0 | within |
| notice-burst-4 | 3.089 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.246 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.428 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.592 | 130 | 16 | 0 | within |
| notice-burst-4 | 4.768 | 130 | 16 | 0 | within |
| notice-burst-4 | 17.792 | 130 | 16 | 0 | within |
| notice-burst-4 | 17.965 | 130 | 16 | 0 | within |
| notice-burst-4 | 18.123 | 130 | 16 | 0 | within |
| notice-burst-4 | 18.290 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.031 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.213 | 130 | 16 | 0 | within |
| notice-burst-4 | 19.730 | 130 | 16 | 0 | within |
| notice-burst-4 | 19.904 | 130 | 16 | 0 | within |
| notice-burst-4 | 20.060 | 130 | 16 | 0 | within |
| notice-burst-4 | 20.229 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.388 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.576 | 130 | 16 | 0 | within |
| notice-burst-4 | 1.709 | 130 | 16 | 0 | within |
| notice-burst-4 | 1.917 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.102 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.302 | 130 | 16 | 0 | within |
| notice-burst-4 | 3.270 | 130 | 16 | 0 | within |
| notice-burst-4 | 3.468 | 130 | 16 | 0 | within |
| notice-burst-4 | 21.843 | 130 | 16 | 0 | within |
| notice-burst-4 | 22.013 | 130 | 16 | 0 | within |
| notice-burst-4 | 22.162 | 130 | 16 | 0 | within |
| notice-burst-4 | 22.327 | 130 | 16 | 0 | within |
| notice-burst-4 | 23.743 | 130 | 16 | 0 | within |
| notice-burst-4 | 23.864 | 130 | 16 | 0 | within |
| notice-burst-4 | 24.031 | 130 | 16 | 0 | within |
| notice-burst-4 | 24.195 | 130 | 16 | 0 | within |
| notice-burst-5 | 15.866 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.045 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.202 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.369 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.265 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.439 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.201 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.381 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.545 | 130 | 16 | 1 | within |
| notice-burst-5 | 2.719 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.508 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.684 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.597 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.764 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.205 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.376 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.709 | 130 | 16 | 1 | within |
| notice-burst-5 | 3.894 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.590 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.770 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.061 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.246 | 130 | 16 | 1 | within |
| notice-burst-5 | 4.849 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.033 | 130 | 16 | 1 | within |
| notice-burst-5 | 5.816 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.001 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.164 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.343 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.932 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.109 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.526 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.691 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.304 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.474 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.623 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.788 | 130 | 16 | 1 | within |
| notice-burst-5 | 23.204 | 130 | 16 | 1 | within |
| notice-burst-5 | 23.325 | 130 | 16 | 1 | within |
| notice-burst-5 | 23.492 | 130 | 16 | 1 | within |
| notice-burst-5 | 23.656 | 130 | 16 | 1 | within |
| notice-burst-6 | 14.752 | 130 | 16 | 1 | within |
| notice-burst-6 | 14.930 | 130 | 16 | 1 | within |
| notice-burst-6 | 15.087 | 130 | 16 | 1 | within |
| notice-burst-6 | 15.252 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.155 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.329 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.030 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.207 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.371 | 130 | 16 | 1 | within |
| notice-burst-6 | 3.545 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.488 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.656 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.222 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.411 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.581 | 130 | 16 | 1 | within |
| notice-burst-6 | 2.761 | 130 | 16 | 1 | within |
| notice-burst-6 | 4.579 | 130 | 16 | 1 | within |
| notice-burst-6 | 4.760 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.374 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.551 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.103 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.280 | 130 | 16 | 1 | within |
| notice-burst-6 | 4.928 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.112 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.716 | 130 | 16 | 1 | within |
| notice-burst-6 | 5.895 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.436 | 130 | 16 | 1 | within |
| notice-burst-6 | 18.603 | 130 | 16 | 1 | within |
| notice-burst-6 | 20.038 | 130 | 16 | 1 | within |
| notice-burst-6 | 20.209 | 130 | 16 | 1 | within |
| notice-burst-6 | 20.357 | 130 | 16 | 1 | within |
| notice-burst-6 | 20.522 | 130 | 16 | 1 | within |
| notice-burst-6 | 22.128 | 130 | 16 | 1 | within |
| notice-burst-6 | 22.298 | 130 | 16 | 1 | within |
| notice-burst-6 | 22.447 | 130 | 16 | 1 | within |
| notice-burst-6 | 22.612 | 130 | 16 | 1 | within |
| notice-burst-6 | 24.026 | 130 | 16 | 1 | within |
| notice-burst-6 | 24.148 | 130 | 16 | 1 | within |
| notice-burst-6 | 24.315 | 130 | 16 | 1 | within |
| notice-burst-6 | 24.479 | 130 | 16 | 1 | within |
| notice-burst-7 | 14.780 | 130 | 16 | 1 | within |
| notice-burst-7 | 14.958 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.207 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.383 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.540 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.708 | 130 | 16 | 1 | within |
| notice-burst-7 | 5.172 | 130 | 16 | 1 | within |
| notice-burst-7 | 5.348 | 130 | 16 | 1 | within |
| notice-burst-7 | 5.508 | 130 | 16 | 1 | within |
| notice-burst-7 | 5.678 | 130 | 16 | 1 | within |
| notice-burst-7 | 15.115 | 130 | 16 | 1 | within |
| notice-burst-7 | 15.281 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.060 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.243 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.406 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.581 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.185 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.357 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.507 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.674 | 130 | 16 | 1 | within |
| notice-burst-7 | 18.120 | 130 | 16 | 1 | within |
| notice-burst-7 | 18.297 | 130 | 16 | 1 | within |
| notice-burst-7 | 18.455 | 130 | 16 | 1 | within |
| notice-burst-7 | 18.626 | 130 | 16 | 1 | within |
| notice-burst-7 | 20.244 | 130 | 16 | 1 | within |
| notice-burst-7 | 20.416 | 130 | 16 | 1 | within |
| notice-burst-7 | 20.569 | 130 | 16 | 1 | within |
| notice-burst-7 | 20.734 | 130 | 16 | 1 | within |
| notice-burst-7 | 22.148 | 130 | 16 | 1 | within |
| notice-burst-7 | 22.318 | 130 | 16 | 1 | within |
| notice-burst-7 | 22.467 | 130 | 16 | 1 | within |
| notice-burst-7 | 22.632 | 130 | 16 | 1 | within |
| notice-burst-7 | 24.253 | 130 | 16 | 1 | within |
| notice-burst-7 | 24.423 | 130 | 16 | 1 | within |
| notice-burst-7 | 24.572 | 130 | 16 | 1 | within |
| notice-burst-7 | 24.737 | 130 | 16 | 1 | within |
| notice-burst-7 | 26.097 | 130 | 16 | 1 | within |
| notice-burst-7 | 26.218 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.024 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.232 | 130 | 16 | 1 | within |

Latest: 26.218 ms, notice-burst-7.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 656 | 98,536 (0.985) | 77,962 (0.780) |
| notice-every-1 | 656 | 98,536 (0.985) | 77,962 (0.780) |
| notice-every-2 | 656 | 98,536 (0.985) | 77,962 (0.780) |
| notice-every-3 | 656 | 98,536 (0.985) | 77,962 (0.780) |
| notice-every-4 | 656 | 98,536 (0.985) | 77,962 (0.780) |
| notice-every-5 | 656 | 98,536 (0.985) | 77,962 (0.780) |
| notice-every-6 | 656 | 98,536 (0.985) | 77,962 (0.780) |
| notice-every-7 | 656 | 98,536 (0.985) | 77,962 (0.780) |
| notice-burst-0 | 666 | 99,275 (0.993) | 77,962 (0.780) |
| notice-burst-1 | 666 | 100,052 (1.001) | 77,962 (0.780) |
| notice-burst-2 | 666 | 101,180 (1.012) | 77,962 (0.780) |
| notice-burst-3 | 665 | 98,536 (0.985) | 77,962 (0.780) |
| notice-burst-4 | 666 | 99,877 (0.999) | 77,962 (0.780) |
| notice-burst-5 | 666 | 98,931 (0.989) | 77,962 (0.780) |
| notice-burst-6 | 666 | 101,771 (1.018) | 77,962 (0.780) |
| notice-burst-7 | 666 | 100,960 (1.010) | 77,962 (0.780) |

Longest pass that carries a step: 101,771 CPU cycles (1.018 ms), notice-burst-6; longest step: 77,962 (0.780 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 410,875 | 4.109 | 130 | 134 | fits | 75,130 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 428,216 | 4.282 | 130 | 134 | fits | 75,130 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 612,364 | 6.124 | 130 | 134 | fits | 73,544 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 629,671 | 6.297 | 130 | 134 | fits | 73,544 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 812,043 | 8.120 | 130 | 134 | fits | 72,805 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 829,359 | 8.294 | 130 | 134 | fits | 72,805 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 216,643 | 2.166 | 130 | 134 | fits | 78,896 | 203 | 0.212 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 234,948 | 2.349 | 130 | 134 | fits | 78,896 | 203 | 0.212 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 251,478 | 2.515 | 130 | 134 | fits | 78,896 | 203 | 0.212 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 268,810 | 2.688 | 130 | 134 | fits | 78,896 | 203 | 0.212 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 444,271 | 4.443 | 130 | 134 | fits | 75,130 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 461,242 | 4.612 | 130 | 134 | fits | 75,130 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 645,403 | 6.454 | 130 | 134 | fits | 73,544 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 662,143 | 6.621 | 130 | 134 | fits | 73,544 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 844,857 | 8.449 | 130 | 134 | fits | 72,805 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 861,287 | 8.613 | 130 | 134 | fits | 72,805 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,009,832 | 10.098 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,026,950 | 10.270 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 1,041,701 | 10.417 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 1,058,121 | 10.581 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 1,204,452 | 12.045 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 1,222,174 | 12.222 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 1,237,908 | 12.379 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 1,254,932 | 12.549 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 1,403,122 | 14.031 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 1,420,463 | 14.205 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 1,435,690 | 14.357 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 1,452,333 | 14.523 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 1,614,631 | 16.146 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 1,631,749 | 16.317 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 1,646,595 | 16.466 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 1,663,015 | 16.630 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 1,805,109 | 18.051 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 1,822,227 | 18.222 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 1,837,138 | 18.371 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 1,853,558 | 18.536 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 2,009,780 | 20.098 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 2,021,893 | 20.219 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 2,038,591 | 20.386 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 2,055,128 | 20.551 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 335,998 | 3.360 | 20 | 200 | fits | 107,463 | 114 | 0.345 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 651,567 | 6.516 | 20 | 20 | fits | 132,336 | 83 | 0.617 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 479,920 | 4.799 | 20 | 24 | fits | 161,729 | 148 | 0.466 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 460,649 | 4.606 | 20 | 50 | fits | 161,729 | 148 | 0.466 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 927,537 | 9.275 | 20 | 20 | fits | 47,463 | 29 | 0.733 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 103,464 | 1.035 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 410,832 | 4.108 | 130 | 134 | fits | 75,130 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 428,173 | 4.282 | 130 | 134 | fits | 75,130 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 612,321 | 6.123 | 130 | 134 | fits | 73,544 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 629,628 | 6.296 | 130 | 134 | fits | 73,544 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 812,000 | 8.120 | 130 | 134 | fits | 72,805 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 829,316 | 8.293 | 130 | 134 | fits | 72,805 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 216,679 | 2.167 | 130 | 134 | fits | 78,855 | 203 | 0.211 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 234,943 | 2.349 | 130 | 134 | fits | 78,855 | 203 | 0.211 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 251,473 | 2.515 | 130 | 134 | fits | 78,855 | 203 | 0.211 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 268,805 | 2.688 | 130 | 134 | fits | 78,855 | 203 | 0.211 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 444,228 | 4.442 | 130 | 134 | fits | 75,130 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 461,199 | 4.612 | 130 | 134 | fits | 75,130 | 203 | 0.178 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 645,360 | 6.454 | 130 | 134 | fits | 73,544 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 662,100 | 6.621 | 130 | 134 | fits | 73,544 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 844,814 | 8.448 | 130 | 134 | fits | 72,805 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 861,244 | 8.612 | 130 | 134 | fits | 72,805 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 1,009,789 | 10.098 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 1,026,907 | 10.269 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 1,041,658 | 10.417 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 1,058,078 | 10.581 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 1,204,409 | 12.044 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 1,222,131 | 12.221 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 1,237,865 | 12.379 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 1,254,889 | 12.549 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 1,403,079 | 14.031 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 1,420,420 | 14.204 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 1,435,647 | 14.356 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 1,452,290 | 14.523 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 1,614,588 | 16.146 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 1,631,706 | 16.317 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 1,646,552 | 16.466 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 1,662,972 | 16.630 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 1,805,066 | 18.051 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 1,822,184 | 18.222 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 1,837,095 | 18.371 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 1,853,515 | 18.535 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 2,009,737 | 20.097 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 2,021,850 | 20.218 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 2,038,548 | 20.385 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 2,055,085 | 20.551 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 336,415 | 3.364 | 20 | 200 | fits | 107,463 | 114 | 0.345 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 646,694 | 6.467 | 20 | 20 | fits | 134,926 | 94 | 0.642 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 472,801 | 4.728 | 20 | 24 | fits | 159,134 | 134 | 0.468 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 607,219 | 6.072 | 20 | 50 | fits | 134,926 | 94 | 0.642 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 921,168 | 9.212 | 20 | 20 | fits | 46,410 | 23 | 0.755 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 99,281 | 0.993 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 410,914 | 4.109 | 130 | 134 | fits | 75,349 | 205 | 0.179 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 428,255 | 4.283 | 130 | 134 | fits | 75,349 | 205 | 0.179 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 612,599 | 6.126 | 130 | 134 | fits | 73,754 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 629,906 | 6.299 | 130 | 134 | fits | 73,754 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 812,252 | 8.123 | 130 | 134 | fits | 73,024 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 829,568 | 8.296 | 130 | 134 | fits | 73,024 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 216,621 | 2.166 | 130 | 134 | fits | 79,115 | 205 | 0.214 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 234,926 | 2.349 | 130 | 134 | fits | 79,115 | 205 | 0.214 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 251,456 | 2.515 | 130 | 134 | fits | 79,115 | 205 | 0.214 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 268,788 | 2.688 | 130 | 134 | fits | 79,115 | 205 | 0.214 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 444,310 | 4.443 | 130 | 134 | fits | 75,349 | 205 | 0.179 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 461,281 | 4.613 | 130 | 134 | fits | 75,349 | 205 | 0.179 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 645,668 | 6.457 | 130 | 134 | fits | 73,754 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 662,408 | 6.624 | 130 | 134 | fits | 73,754 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 845,066 | 8.451 | 130 | 134 | fits | 73,024 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 861,496 | 8.615 | 130 | 134 | fits | 73,024 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 1,010,182 | 10.102 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 1,027,300 | 10.273 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 1,042,051 | 10.421 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 1,058,471 | 10.585 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 1,223,936 | 12.239 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 1,241,658 | 12.417 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 1,257,392 | 12.574 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 1,274,416 | 12.744 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 1,422,606 | 14.226 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 1,439,947 | 14.399 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 1,455,174 | 14.552 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 1,471,817 | 14.718 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 1,615,273 | 16.153 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 1,632,391 | 16.324 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 1,647,237 | 16.472 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 1,663,657 | 16.637 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 1,824,447 | 18.244 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 1,841,565 | 18.416 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 1,856,476 | 18.565 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 1,872,896 | 18.729 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 2,010,749 | 20.107 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 2,022,862 | 20.229 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 2,039,560 | 20.396 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 2,056,097 | 20.561 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 533,216 | 5.332 | 20 | 200 | fits | 154,625 | 130 | 0.458 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 672,076 | 6.721 | 20 | 20 | fits | 139,971 | 79 | 0.618 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 492,744 | 4.927 | 20 | 24 | fits | 154,625 | 130 | 0.458 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 473,473 | 4.735 | 20 | 50 | fits | 154,625 | 130 | 0.458 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 938,157 | 9.382 | 20 | 20 | fits | 38,403 | 25 | 0.776 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 114,160 | 1.142 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 822,772 | 8.228 | 130 | 134 | fits | 72,923 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 840,113 | 8.401 | 130 | 134 | fits | 72,923 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 230,665 | 2.307 | 130 | 134 | fits | 80,283 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 248,458 | 2.485 | 130 | 134 | fits | 80,283 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 618,384 | 6.184 | 130 | 134 | fits | 74,326 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 635,970 | 6.360 | 130 | 134 | fits | 74,326 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 415,864 | 4.159 | 130 | 134 | fits | 75,685 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 433,746 | 4.337 | 130 | 134 | fits | 75,685 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 265,067 | 2.651 | 130 | 134 | fits | 80,283 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 282,399 | 2.824 | 130 | 134 | fits | 80,283 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 449,801 | 4.498 | 130 | 134 | fits | 75,685 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 466,772 | 4.668 | 130 | 134 | fits | 75,685 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 651,702 | 6.517 | 130 | 134 | fits | 74,326 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 668,442 | 6.684 | 130 | 134 | fits | 74,326 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 855,611 | 8.556 | 130 | 134 | fits | 72,923 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 872,041 | 8.720 | 130 | 134 | fits | 72,923 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 1,000,097 | 10.001 | 130 | 134 | fits | 72,004 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 1,017,215 | 10.172 | 130 | 134 | fits | 72,004 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 1,031,996 | 10.320 | 130 | 134 | fits | 72,004 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 1,048,416 | 10.484 | 130 | 134 | fits | 72,004 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 1,213,930 | 12.139 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 1,231,652 | 12.317 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 1,247,386 | 12.474 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 1,264,410 | 12.644 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 1,412,600 | 14.126 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 1,429,941 | 14.299 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 1,445,168 | 14.452 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 1,461,811 | 14.618 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 1,605,267 | 16.053 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 1,622,385 | 16.224 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 1,637,231 | 16.372 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 1,653,651 | 16.537 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 1,814,441 | 18.144 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 1,831,559 | 18.316 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 1,846,470 | 18.465 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 1,862,890 | 18.629 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 2,000,743 | 20.007 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 2,012,856 | 20.129 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 2,029,554 | 20.296 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 2,046,091 | 20.461 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 327,563 | 3.276 | 20 | 200 | fits | 107,394 | 114 | 0.344 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 642,058 | 6.421 | 20 | 20 | fits | 133,171 | 93 | 0.624 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 469,826 | 4.698 | 20 | 24 | fits | 151,457 | 131 | 0.482 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 602,583 | 6.026 | 20 | 50 | fits | 133,171 | 93 | 0.624 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 939,891 | 9.399 | 20 | 20 | fits | 48,875 | 29 | 0.767 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 79,643 | 0.796 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 795,899 | 7.959 | 130 | 134 | fits | 73,142 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 813,240 | 8.132 | 130 | 134 | fits | 73,142 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 199,531 | 1.995 | 130 | 134 | fits | 78,554 | 205 | 0.217 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 217,365 | 2.174 | 130 | 134 | fits | 78,554 | 205 | 0.217 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 393,810 | 3.938 | 130 | 134 | fits | 75,732 | 205 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 411,317 | 4.113 | 130 | 134 | fits | 75,732 | 205 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 595,655 | 5.957 | 130 | 134 | fits | 74,521 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 613,385 | 6.134 | 130 | 134 | fits | 74,521 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 234,004 | 2.340 | 130 | 134 | fits | 78,554 | 205 | 0.217 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 251,336 | 2.513 | 130 | 134 | fits | 78,554 | 205 | 0.217 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 427,307 | 4.273 | 130 | 134 | fits | 75,732 | 205 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 444,278 | 4.443 | 130 | 134 | fits | 75,732 | 205 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 629,117 | 6.291 | 130 | 134 | fits | 74,521 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 645,857 | 6.459 | 130 | 134 | fits | 74,521 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 828,738 | 8.287 | 130 | 134 | fits | 73,142 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 845,168 | 8.452 | 130 | 134 | fits | 73,142 | 205 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 993,775 | 9.938 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 1,010,893 | 10.109 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 1,025,644 | 10.256 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 1,042,064 | 10.421 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 1,207,578 | 12.076 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 1,225,300 | 12.253 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 1,241,034 | 12.410 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 1,258,058 | 12.581 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 1,406,248 | 14.062 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 1,423,589 | 14.236 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 1,438,816 | 14.388 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 1,455,459 | 14.555 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 1,598,915 | 15.989 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 1,616,033 | 16.160 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 1,630,879 | 16.309 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 1,647,299 | 16.473 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 1,808,089 | 18.081 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 1,825,207 | 18.252 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 1,840,118 | 18.401 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 1,856,538 | 18.565 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 1,994,391 | 19.944 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 2,006,504 | 20.065 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 2,023,202 | 20.232 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 2,039,739 | 20.397 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 330,289 | 3.303 | 20 | 200 | fits | 107,463 | 114 | 0.345 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 655,484 | 6.555 | 20 | 20 | fits | 132,083 | 81 | 0.618 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 484,298 | 4.843 | 20 | 24 | fits | 162,392 | 154 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 465,027 | 4.650 | 20 | 50 | fits | 162,392 | 154 | 0.467 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 922,680 | 9.227 | 20 | 20 | fits | 37,290 | 19 | 0.802 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 109,696 | 1.097 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 817,294 | 8.173 | 130 | 134 | fits | 72,923 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 834,635 | 8.346 | 130 | 134 | fits | 72,923 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 220,940 | 2.209 | 130 | 134 | fits | 78,264 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 238,733 | 2.387 | 130 | 134 | fits | 78,264 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 415,090 | 4.151 | 130 | 134 | fits | 75,513 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 432,597 | 4.326 | 130 | 134 | fits | 75,513 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 617,002 | 6.170 | 130 | 134 | fits | 74,302 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 634,732 | 6.347 | 130 | 134 | fits | 74,302 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 255,342 | 2.553 | 130 | 134 | fits | 78,264 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 272,674 | 2.727 | 130 | 134 | fits | 78,264 | 203 | 0.214 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 448,587 | 4.486 | 130 | 134 | fits | 75,513 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 465,558 | 4.656 | 130 | 134 | fits | 75,513 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 650,464 | 6.505 | 130 | 134 | fits | 74,302 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 667,204 | 6.672 | 130 | 134 | fits | 74,302 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 850,133 | 8.501 | 130 | 134 | fits | 72,923 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 866,563 | 8.666 | 130 | 134 | fits | 72,923 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 1,015,029 | 10.150 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 1,032,147 | 10.321 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 1,046,898 | 10.469 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 1,063,318 | 10.633 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 1,209,698 | 12.097 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 1,227,420 | 12.274 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 1,243,154 | 12.432 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 1,260,178 | 12.602 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 1,408,368 | 14.084 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 1,425,709 | 14.257 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 1,440,936 | 14.409 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 1,457,579 | 14.576 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 1,619,877 | 16.199 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 1,636,995 | 16.370 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 1,651,841 | 16.518 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 1,668,261 | 16.683 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 1,810,355 | 18.104 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 1,827,473 | 18.275 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 1,842,384 | 18.424 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 1,858,804 | 18.588 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 2,015,026 | 20.150 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 2,027,139 | 20.271 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 2,043,837 | 20.438 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 2,060,374 | 20.604 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 337,737 | 3.377 | 20 | 200 | fits | 107,463 | 114 | 0.345 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 637,381 | 6.374 | 20 | 20 | fits | 134,666 | 94 | 0.641 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 463,755 | 4.638 | 20 | 24 | fits | 158,854 | 134 | 0.468 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 597,906 | 5.979 | 20 | 50 | fits | 134,666 | 94 | 0.641 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 926,077 | 9.261 | 20 | 20 | fits | 39,607 | 25 | 0.805 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 80,329 | 0.803 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 216,172 | 2.162 | 130 | 134 | fits | 78,479 | 205 | 0.214 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 233,946 | 2.339 | 130 | 134 | fits | 78,479 | 205 | 0.214 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 429,614 | 4.296 | 130 | 134 | fits | 74,728 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 446,842 | 4.468 | 130 | 134 | fits | 74,728 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 635,453 | 6.355 | 130 | 134 | fits | 73,904 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 652,848 | 6.528 | 130 | 134 | fits | 73,904 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 814,415 | 8.144 | 130 | 134 | fits | 72,589 | 205 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 831,612 | 8.316 | 130 | 134 | fits | 72,589 | 205 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 250,510 | 2.505 | 130 | 134 | fits | 78,479 | 205 | 0.214 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 267,842 | 2.678 | 130 | 134 | fits | 78,479 | 205 | 0.214 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 462,897 | 4.629 | 130 | 134 | fits | 74,728 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 479,868 | 4.799 | 130 | 134 | fits | 74,728 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 668,580 | 6.686 | 130 | 134 | fits | 73,904 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 685,320 | 6.853 | 130 | 134 | fits | 73,904 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 847,061 | 8.471 | 130 | 134 | fits | 72,589 | 205 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 863,491 | 8.635 | 130 | 134 | fits | 72,589 | 205 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 1,012,098 | 10.121 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 1,029,216 | 10.292 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 1,043,967 | 10.440 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 1,060,387 | 10.604 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 1,225,852 | 12.259 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 1,243,574 | 12.436 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 1,259,308 | 12.593 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 1,276,332 | 12.763 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 1,424,522 | 14.245 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 1,441,863 | 14.419 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 1,457,090 | 14.571 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 1,473,733 | 14.737 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 1,617,189 | 16.172 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 1,634,307 | 16.343 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 1,649,153 | 16.492 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 1,665,573 | 16.656 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 1,826,363 | 18.264 | 130 | 134 | fits | 70,227 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 1,843,481 | 18.435 | 130 | 134 | fits | 70,227 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 1,858,392 | 18.584 | 130 | 134 | fits | 70,227 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 1,874,812 | 18.748 | 130 | 134 | fits | 70,227 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 2,012,744 | 20.127 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 2,024,857 | 20.249 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 2,041,555 | 20.416 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 2,058,092 | 20.581 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 527,496 | 5.275 | 20 | 200 | fits | 150,435 | 233 | 0.257 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 662,020 | 6.620 | 20 | 20 | fits | 132,125 | 86 | 0.597 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 337,538 | 3.375 | 20 | 24 | fits | 84,284 | 66 | 0.466 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 467,753 | 4.678 | 20 | 50 | fits | 150,435 | 233 | 0.257 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 939,533 | 9.395 | 20 | 20 | fits | 46,347 | 23 | 0.754 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 112,756 | 1.128 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 410,862 | 4.109 | 130 | 134 | fits | 75,425 | 205 | 0.181 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 428,203 | 4.282 | 130 | 134 | fits | 75,425 | 205 | 0.181 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 612,298 | 6.123 | 130 | 134 | fits | 73,763 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 629,605 | 6.296 | 130 | 134 | fits | 73,763 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 811,921 | 8.119 | 130 | 134 | fits | 73,024 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 829,237 | 8.292 | 130 | 134 | fits | 73,024 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 216,654 | 2.167 | 130 | 134 | fits | 79,073 | 205 | 0.211 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 234,918 | 2.349 | 130 | 134 | fits | 79,073 | 205 | 0.211 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 251,447 | 2.514 | 130 | 134 | fits | 79,073 | 205 | 0.211 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 268,779 | 2.688 | 130 | 134 | fits | 79,073 | 205 | 0.211 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 444,258 | 4.443 | 130 | 134 | fits | 75,425 | 205 | 0.181 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 461,229 | 4.612 | 130 | 134 | fits | 75,425 | 205 | 0.181 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 645,337 | 6.453 | 130 | 134 | fits | 73,763 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 662,077 | 6.621 | 130 | 134 | fits | 73,763 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 844,735 | 8.447 | 130 | 134 | fits | 73,024 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 861,165 | 8.612 | 130 | 134 | fits | 73,024 | 205 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 1,009,851 | 10.099 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 1,026,969 | 10.270 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 1,041,720 | 10.417 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 1,058,140 | 10.581 | 130 | 134 | fits | 72,073 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 1,223,605 | 12.236 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 1,241,327 | 12.413 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 1,257,061 | 12.571 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 1,274,085 | 12.741 | 130 | 134 | fits | 73,421 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 1,422,275 | 14.223 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 1,439,616 | 14.396 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 1,454,843 | 14.548 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 1,471,486 | 14.715 | 130 | 134 | fits | 71,735 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 1,614,942 | 16.149 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 1,632,060 | 16.321 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 1,646,906 | 16.469 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 1,663,326 | 16.633 | 130 | 134 | fits | 70,498 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 1,824,116 | 18.241 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 1,841,234 | 18.412 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 1,856,145 | 18.561 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 1,872,565 | 18.726 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 2,010,418 | 20.104 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 2,022,531 | 20.225 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 2,039,229 | 20.392 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 2,055,766 | 20.558 | 130 | 134 | fits | 64,395 | 203 | 0.138 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 328,640 | 3.286 | 20 | 200 | fits | 107,463 | 114 | 0.345 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 634,630 | 6.346 | 20 | 20 | fits | 133,547 | 88 | 0.646 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 462,132 | 4.621 | 20 | 24 | fits | 158,649 | 132 | 0.468 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 595,155 | 5.952 | 20 | 50 | fits | 133,547 | 88 | 0.646 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 931,363 | 9.314 | 20 | 20 | fits | 50,194 | 35 | 0.753 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 82,868 | 0.829 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 222,564 | 2.226 | 130 | 134 | fits | 99,275 | 211 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 240,163 | 2.402 | 130 | 134 | fits | 99,275 | 211 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 255,579 | 2.556 | 130 | 134 | fits | 99,275 | 211 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 272,147 | 2.721 | 130 | 134 | fits | 99,275 | 211 | 0.196 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 299,489 | 2.995 | 130 | 134 | fits | 74,632 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 316,400 | 3.164 | 130 | 134 | fits | 74,632 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 506,113 | 5.061 | 130 | 134 | fits | 73,578 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 522,945 | 5.229 | 130 | 134 | fits | 73,578 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 1,468,247 | 14.682 | 130 | 134 | fits | 75,909 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 1,486,000 | 14.860 | 130 | 134 | fits | 75,909 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 1,501,832 | 15.018 | 130 | 134 | fits | 75,909 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 1,518,414 | 15.184 | 130 | 134 | fits | 75,909 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 1,665,596 | 16.656 | 130 | 134 | fits | 72,755 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 1,682,973 | 16.830 | 130 | 134 | fits | 72,755 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 332,778 | 3.328 | 130 | 134 | fits | 74,632 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 350,270 | 3.503 | 130 | 134 | fits | 74,632 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 429,335 | 4.293 | 130 | 134 | fits | 98,847 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 447,442 | 4.474 | 130 | 134 | fits | 98,847 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 1,698,051 | 16.981 | 130 | 134 | fits | 72,755 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 1,714,767 | 17.148 | 130 | 134 | fits | 72,755 | 203 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 463,657 | 4.637 | 130 | 134 | fits | 98,847 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 481,686 | 4.817 | 130 | 134 | fits | 98,847 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 539,035 | 5.390 | 130 | 134 | fits | 73,578 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 556,898 | 5.569 | 130 | 134 | fits | 73,578 | 205 | 0.112 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 1,879,000 | 18.790 | 130 | 134 | fits | 71,484 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 1,896,268 | 18.963 | 130 | 134 | fits | 71,484 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 1,911,504 | 19.115 | 130 | 134 | fits | 71,484 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 1,928,220 | 19.282 | 130 | 134 | fits | 71,484 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 2,071,554 | 20.716 | 130 | 134 | fits | 70,402 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 2,088,599 | 20.886 | 130 | 134 | fits | 70,402 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 2,103,454 | 21.035 | 130 | 134 | fits | 70,402 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 2,119,947 | 21.199 | 130 | 134 | fits | 70,402 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 2,265,668 | 22.657 | 130 | 134 | fits | 70,573 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 2,282,713 | 22.827 | 130 | 134 | fits | 70,573 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 2,297,633 | 22.976 | 130 | 134 | fits | 70,573 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 2,314,126 | 23.141 | 130 | 134 | fits | 70,573 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 2,470,554 | 24.706 | 130 | 134 | fits | 64,403 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,482,667 | 24.827 | 130 | 134 | fits | 64,403 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,499,365 | 24.994 | 130 | 134 | fits | 64,403 | 202 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 2,515,838 | 25.158 | 130 | 134 | fits | 64,403 | 202 | 0.139 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 174,396 | 1.744 | 20 | 200 | fits | 155,646 | 228 | 0.324 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 599,749 | 5.997 | 20 | 20 | fits | 137,513 | 67 | 0.629 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 442,032 | 4.420 | 20 | 24 | fits | 150,736 | 146 | 0.414 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 422,761 | 4.228 | 20 | 50 | fits | 150,736 | 146 | 0.414 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 799,774 | 7.998 | 20 | 20 | fits | 132,674 | 62 | 0.524 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 362,979 | 3.630 | 130 | 134 | fits | 102,703 | 211 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 380,277 | 3.803 | 130 | 134 | fits | 102,703 | 211 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 443,292 | 4.433 | 130 | 134 | fits | 74,270 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 460,124 | 4.601 | 130 | 134 | fits | 74,270 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 650,411 | 6.504 | 130 | 134 | fits | 70,755 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 667,322 | 6.673 | 130 | 134 | fits | 70,755 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 682,621 | 6.826 | 130 | 134 | fits | 70,755 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 699,189 | 6.992 | 130 | 134 | fits | 70,755 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 1,579,696 | 15.797 | 130 | 134 | fits | 76,273 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 1,597,554 | 15.976 | 130 | 134 | fits | 76,273 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 1,613,418 | 16.134 | 130 | 134 | fits | 76,273 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 1,630,223 | 16.302 | 130 | 134 | fits | 76,273 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 476,505 | 4.765 | 130 | 134 | fits | 74,270 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 494,076 | 4.941 | 130 | 134 | fits | 74,270 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 572,159 | 5.722 | 130 | 134 | fits | 100,052 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 590,345 | 5.903 | 130 | 134 | fits | 100,052 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 1,720,176 | 17.202 | 130 | 134 | fits | 72,596 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 1,737,553 | 17.376 | 130 | 134 | fits | 72,596 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 1,752,552 | 17.526 | 130 | 134 | fits | 72,596 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 1,769,268 | 17.693 | 130 | 134 | fits | 72,596 | 203 | 0.177 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 606,741 | 6.067 | 130 | 134 | fits | 100,052 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 625,001 | 6.250 | 130 | 134 | fits | 100,052 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 1,932,442 | 19.324 | 130 | 134 | fits | 71,411 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 1,949,868 | 19.499 | 130 | 134 | fits | 71,411 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 221,092 | 2.211 | 130 | 134 | fits | 88,927 | 205 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 241,455 | 2.415 | 130 | 134 | fits | 88,927 | 205 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 398,155 | 3.982 | 130 | 134 | fits | 102,703 | 211 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 417,584 | 4.176 | 130 | 134 | fits | 102,703 | 211 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 1,965,107 | 19.651 | 130 | 134 | fits | 71,411 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 1,981,600 | 19.816 | 130 | 134 | fits | 71,411 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 260,249 | 2.602 | 130 | 134 | fits | 88,927 | 205 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 280,515 | 2.805 | 130 | 134 | fits | 88,927 | 205 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 2,123,833 | 21.238 | 130 | 134 | fits | 70,506 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 2,140,878 | 21.409 | 130 | 134 | fits | 70,506 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 2,155,789 | 21.558 | 130 | 134 | fits | 70,506 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 2,172,282 | 21.723 | 130 | 134 | fits | 70,506 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 2,313,962 | 23.140 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 2,326,075 | 23.261 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 2,342,773 | 23.428 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 2,359,237 | 23.592 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 582,593 | 5.826 | 20 | 200 | fits | 152,274 | 209 | 0.182 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 562,325 | 5.623 | 20 | 20 | fits | 152,274 | 209 | 0.182 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 389,847 | 3.898 | 20 | 24 | fits | 156,663 | 163 | 0.439 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 522,850 | 5.229 | 20 | 50 | fits | 152,274 | 209 | 0.182 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 879,934 | 8.799 | 20 | 20 | fits | 106,437 | 50 | 0.559 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 464,561 | 4.646 | 130 | 134 | fits | 101,180 | 211 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 481,967 | 4.820 | 130 | 134 | fits | 101,180 | 211 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 544,060 | 5.441 | 130 | 134 | fits | 73,403 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 560,892 | 5.609 | 130 | 134 | fits | 73,403 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 1,485,360 | 14.854 | 130 | 134 | fits | 75,591 | 203 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 1,503,088 | 15.031 | 130 | 134 | fits | 75,591 | 203 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 1,518,748 | 15.187 | 130 | 134 | fits | 75,591 | 203 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 1,535,251 | 15.353 | 130 | 134 | fits | 75,591 | 203 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 1,606,724 | 16.067 | 130 | 134 | fits | 73,503 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 1,624,166 | 16.242 | 130 | 134 | fits | 73,503 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 1,639,991 | 16.400 | 130 | 134 | fits | 73,503 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 1,656,796 | 16.568 | 130 | 134 | fits | 73,503 | 203 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 577,369 | 5.774 | 130 | 134 | fits | 73,403 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 594,940 | 5.949 | 130 | 134 | fits | 73,403 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 1,802,180 | 18.022 | 130 | 134 | fits | 72,848 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 1,819,527 | 18.195 | 130 | 134 | fits | 72,848 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 1,835,355 | 18.354 | 130 | 134 | fits | 72,848 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 1,852,002 | 18.520 | 130 | 134 | fits | 72,848 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 245,208 | 2.452 | 130 | 134 | fits | 105,951 | 211 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 264,633 | 2.646 | 130 | 134 | fits | 105,951 | 211 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 282,071 | 2.821 | 130 | 134 | fits | 105,951 | 211 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 301,089 | 3.011 | 130 | 134 | fits | 105,951 | 211 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 1,996,087 | 19.961 | 130 | 134 | fits | 71,408 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 2,013,513 | 20.135 | 130 | 134 | fits | 71,408 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 329,942 | 3.299 | 130 | 134 | fits | 82,604 | 205 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 349,322 | 3.493 | 130 | 134 | fits | 82,604 | 205 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 366,783 | 3.668 | 130 | 134 | fits | 82,604 | 205 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 385,888 | 3.859 | 130 | 134 | fits | 82,604 | 205 | 0.103 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 499,220 | 4.992 | 130 | 134 | fits | 101,180 | 211 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 518,029 | 5.180 | 130 | 134 | fits | 101,180 | 211 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 2,028,735 | 20.287 | 130 | 134 | fits | 71,408 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 2,045,228 | 20.452 | 130 | 134 | fits | 71,408 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 2,206,184 | 22.062 | 130 | 134 | fits | 70,371 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 2,223,229 | 22.232 | 130 | 134 | fits | 70,371 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 2,238,149 | 22.381 | 130 | 134 | fits | 70,371 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 2,254,642 | 22.546 | 130 | 134 | fits | 70,371 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 2,396,156 | 23.962 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,408,269 | 24.083 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,424,967 | 24.250 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 2,441,431 | 24.414 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 178,514 | 1.785 | 20 | 200 | fits | 155,422 | 228 | 0.324 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 603,602 | 6.036 | 20 | 20 | fits | 137,600 | 67 | 0.630 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 445,798 | 4.458 | 20 | 24 | fits | 150,720 | 146 | 0.415 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 426,527 | 4.265 | 20 | 50 | fits | 150,720 | 146 | 0.415 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 803,909 | 8.039 | 20 | 20 | fits | 124,418 | 58 | 0.535 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 536,533 | 5.365 | 130 | 134 | fits | 73,933 | 205 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 553,509 | 5.535 | 130 | 134 | fits | 73,933 | 205 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,472,921 | 14.729 | 130 | 134 | fits | 75,364 | 203 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,490,543 | 14.905 | 130 | 134 | fits | 75,364 | 203 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 1,506,392 | 15.064 | 130 | 134 | fits | 75,364 | 203 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 1,522,974 | 15.230 | 130 | 134 | fits | 75,364 | 203 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 1,613,274 | 16.133 | 130 | 134 | fits | 73,285 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 1,630,691 | 16.307 | 130 | 134 | fits | 73,285 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 1,646,554 | 16.466 | 130 | 134 | fits | 73,285 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 1,663,345 | 16.633 | 130 | 134 | fits | 73,285 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 569,983 | 5.700 | 130 | 134 | fits | 73,933 | 205 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 587,554 | 5.876 | 130 | 134 | fits | 73,933 | 205 | 0.110 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 1,808,485 | 18.085 | 130 | 134 | fits | 72,547 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 1,825,753 | 18.258 | 130 | 134 | fits | 72,547 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 1,841,434 | 18.414 | 130 | 134 | fits | 72,547 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 1,858,160 | 18.582 | 130 | 134 | fits | 72,547 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 2,021,444 | 20.214 | 130 | 134 | fits | 71,316 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 2,038,489 | 20.385 | 130 | 134 | fits | 71,316 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 456,535 | 4.565 | 130 | 134 | fits | 102,099 | 211 | 0.183 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 475,720 | 4.757 | 130 | 134 | fits | 102,099 | 211 | 0.183 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 217,136 | 2.171 | 130 | 134 | fits | 108,537 | 213 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 237,101 | 2.371 | 130 | 134 | fits | 108,537 | 213 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 254,886 | 2.549 | 130 | 134 | fits | 108,537 | 213 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 274,135 | 2.741 | 130 | 134 | fits | 108,537 | 213 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 302,197 | 3.022 | 130 | 134 | fits | 80,226 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 321,340 | 3.213 | 130 | 134 | fits | 80,226 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 338,499 | 3.385 | 130 | 134 | fits | 80,226 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 357,367 | 3.574 | 130 | 134 | fits | 80,226 | 205 | 0.105 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 493,038 | 4.930 | 130 | 134 | fits | 102,099 | 211 | 0.183 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 511,675 | 5.117 | 130 | 134 | fits | 102,099 | 211 | 0.183 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 2,053,488 | 20.535 | 130 | 134 | fits | 71,316 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 2,069,981 | 20.700 | 130 | 134 | fits | 71,316 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 2,212,542 | 22.125 | 130 | 134 | fits | 70,227 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 2,229,587 | 22.296 | 130 | 134 | fits | 70,227 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 2,244,498 | 22.445 | 130 | 134 | fits | 70,227 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 2,260,991 | 22.610 | 130 | 134 | fits | 70,227 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 2,407,303 | 24.073 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,419,416 | 24.194 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,436,114 | 24.361 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,452,578 | 24.526 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 172,193 | 1.722 | 20 | 200 | fits | 163,684 | 237 | 0.308 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 465,907 | 4.659 | 20 | 20 | fits | 158,204 | 155 | 0.397 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 445,703 | 4.457 | 20 | 24 | fits | 158,204 | 155 | 0.397 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 426,432 | 4.264 | 20 | 50 | fits | 158,204 | 155 | 0.397 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 784,635 | 7.846 | 20 | 20 | fits | 106,531 | 50 | 0.559 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,443,763 | 14.438 | 130 | 134 | fits | 75,538 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,461,556 | 14.616 | 130 | 134 | fits | 75,538 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,477,202 | 14.772 | 130 | 134 | fits | 75,538 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,493,705 | 14.937 | 130 | 134 | fits | 75,538 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 1,584,026 | 15.840 | 130 | 134 | fits | 73,223 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 1,601,482 | 16.015 | 130 | 134 | fits | 73,223 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 1,617,200 | 16.172 | 130 | 134 | fits | 73,223 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 1,633,926 | 16.339 | 130 | 134 | fits | 73,223 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 290,546 | 2.905 | 130 | 134 | fits | 84,802 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 308,861 | 3.089 | 130 | 134 | fits | 84,802 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 424,622 | 4.246 | 130 | 134 | fits | 99,877 | 211 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 442,847 | 4.428 | 130 | 134 | fits | 99,877 | 211 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 459,182 | 4.592 | 130 | 134 | fits | 99,877 | 211 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 476,767 | 4.768 | 130 | 134 | fits | 99,877 | 211 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 1,779,159 | 17.792 | 130 | 134 | fits | 72,854 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 1,796,506 | 17.965 | 130 | 134 | fits | 72,854 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 1,812,334 | 18.123 | 130 | 134 | fits | 72,854 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 1,828,981 | 18.290 | 130 | 134 | fits | 72,854 | 203 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 503,071 | 5.031 | 130 | 134 | fits | 77,961 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 521,290 | 5.213 | 130 | 134 | fits | 77,961 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,973,012 | 19.730 | 130 | 134 | fits | 72,350 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,990,438 | 19.904 | 130 | 134 | fits | 72,350 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 2,006,023 | 20.060 | 130 | 134 | fits | 72,350 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 2,022,897 | 20.229 | 130 | 134 | fits | 72,350 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 538,766 | 5.388 | 130 | 134 | fits | 77,961 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 557,567 | 5.576 | 130 | 134 | fits | 77,961 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 170,919 | 1.709 | 130 | 134 | fits | 111,742 | 213 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 191,670 | 1.917 | 130 | 134 | fits | 111,742 | 213 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 210,199 | 2.102 | 130 | 134 | fits | 111,742 | 213 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 230,234 | 2.302 | 130 | 134 | fits | 111,742 | 213 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 326,991 | 3.270 | 130 | 134 | fits | 84,802 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 346,795 | 3.468 | 130 | 134 | fits | 84,802 | 203 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 2,184,282 | 21.843 | 130 | 134 | fits | 70,524 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 2,201,327 | 22.013 | 130 | 134 | fits | 70,524 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 2,216,247 | 22.162 | 130 | 134 | fits | 70,524 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 2,232,740 | 22.327 | 130 | 134 | fits | 70,524 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 2,374,263 | 23.743 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 2,386,376 | 23.864 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,403,074 | 24.031 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,419,538 | 24.195 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 178,538 | 1.785 | 20 | 200 | fits | 164,032 | 237 | 0.311 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 472,251 | 4.723 | 20 | 20 | fits | 158,090 | 155 | 0.398 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 452,047 | 4.520 | 20 | 24 | fits | 158,090 | 155 | 0.398 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 432,776 | 4.328 | 20 | 50 | fits | 158,090 | 155 | 0.398 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 790,782 | 7.908 | 20 | 20 | fits | 106,452 | 50 | 0.559 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 1,586,585 | 15.866 | 130 | 134 | fits | 75,825 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,604,522 | 16.045 | 130 | 134 | fits | 75,825 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,620,200 | 16.202 | 130 | 134 | fits | 75,825 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,636,926 | 16.369 | 130 | 134 | fits | 75,825 | 203 | 0.221 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 1,726,452 | 17.265 | 130 | 134 | fits | 72,990 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 1,743,908 | 17.439 | 130 | 134 | fits | 72,990 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 220,108 | 2.201 | 130 | 134 | fits | 78,604 | 205 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 238,072 | 2.381 | 130 | 134 | fits | 78,604 | 205 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 254,450 | 2.545 | 130 | 134 | fits | 78,604 | 205 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 271,855 | 2.719 | 130 | 134 | fits | 78,604 | 205 | 0.151 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 450,776 | 4.508 | 130 | 134 | fits | 76,753 | 205 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 468,380 | 4.684 | 130 | 134 | fits | 76,753 | 205 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 1,759,736 | 17.597 | 130 | 134 | fits | 72,990 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 1,776,383 | 17.764 | 130 | 134 | fits | 72,990 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 1,920,490 | 19.205 | 130 | 134 | fits | 71,250 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 1,937,614 | 19.376 | 130 | 134 | fits | 71,250 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 370,936 | 3.709 | 130 | 134 | fits | 102,151 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 389,435 | 3.894 | 130 | 134 | fits | 102,151 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 659,015 | 6.590 | 130 | 134 | fits | 73,621 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 677,003 | 6.770 | 130 | 134 | fits | 73,621 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 406,143 | 4.061 | 130 | 134 | fits | 102,151 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 424,634 | 4.246 | 130 | 134 | fits | 102,151 | 211 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 484,932 | 4.849 | 130 | 134 | fits | 76,753 | 205 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 503,336 | 5.033 | 130 | 134 | fits | 76,753 | 205 | 0.108 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 581,612 | 5.816 | 130 | 134 | fits | 98,931 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 600,083 | 6.001 | 130 | 134 | fits | 98,931 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 616,403 | 6.164 | 130 | 134 | fits | 98,931 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 634,282 | 6.343 | 130 | 134 | fits | 98,931 | 211 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 693,168 | 6.932 | 130 | 134 | fits | 73,621 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 710,881 | 7.109 | 130 | 134 | fits | 73,621 | 205 | 0.106 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 1,952,613 | 19.526 | 130 | 134 | fits | 71,250 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 1,969,106 | 19.691 | 130 | 134 | fits | 71,250 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 2,130,367 | 21.304 | 130 | 134 | fits | 70,236 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 2,147,412 | 21.474 | 130 | 134 | fits | 70,236 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 2,162,332 | 21.623 | 130 | 134 | fits | 70,236 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 2,178,825 | 21.788 | 130 | 134 | fits | 70,236 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,320,356 | 23.204 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,332,469 | 23.325 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,349,167 | 23.492 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,365,631 | 23.656 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 588,939 | 5.889 | 20 | 200 | fits | 151,487 | 219 | 0.183 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 568,671 | 5.687 | 20 | 20 | fits | 151,487 | 219 | 0.183 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 396,980 | 3.970 | 20 | 24 | fits | 155,046 | 151 | 0.435 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 529,196 | 5.292 | 20 | 50 | fits | 151,487 | 219 | 0.183 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 886,266 | 8.863 | 20 | 20 | fits | 106,373 | 50 | 0.559 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 1,475,226 | 14.752 | 130 | 134 | fits | 75,538 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,493,019 | 14.930 | 130 | 134 | fits | 75,538 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,508,665 | 15.087 | 130 | 134 | fits | 75,538 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,525,168 | 15.252 | 130 | 134 | fits | 75,538 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 1,615,489 | 16.155 | 130 | 134 | fits | 73,409 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 1,632,945 | 16.329 | 130 | 134 | fits | 73,409 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 302,986 | 3.030 | 130 | 134 | fits | 76,839 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 320,734 | 3.207 | 130 | 134 | fits | 76,839 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 337,063 | 3.371 | 130 | 134 | fits | 76,839 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 354,468 | 3.545 | 130 | 134 | fits | 76,839 | 205 | 0.101 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 1,648,770 | 16.488 | 130 | 134 | fits | 73,409 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 1,665,575 | 16.656 | 130 | 134 | fits | 73,409 | 203 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 222,165 | 2.222 | 130 | 134 | fits | 104,467 | 213 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 241,074 | 2.411 | 130 | 134 | fits | 104,467 | 213 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 258,109 | 2.581 | 130 | 134 | fits | 104,467 | 213 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 276,063 | 2.761 | 130 | 134 | fits | 104,467 | 213 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 457,910 | 4.579 | 130 | 134 | fits | 101,771 | 211 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 476,017 | 4.760 | 130 | 134 | fits | 101,771 | 211 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 537,354 | 5.374 | 130 | 134 | fits | 75,278 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 555,111 | 5.551 | 130 | 134 | fits | 75,278 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,810,316 | 18.103 | 130 | 134 | fits | 72,306 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 1,828,044 | 18.280 | 130 | 134 | fits | 72,306 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 492,779 | 4.928 | 130 | 134 | fits | 101,771 | 211 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 511,197 | 5.112 | 130 | 134 | fits | 101,771 | 211 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 571,592 | 5.716 | 130 | 134 | fits | 75,278 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 589,542 | 5.895 | 130 | 134 | fits | 75,278 | 205 | 0.107 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 1,843,568 | 18.436 | 130 | 134 | fits | 72,306 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 1,860,284 | 18.603 | 130 | 134 | fits | 72,306 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 2,003,828 | 20.038 | 130 | 134 | fits | 70,405 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 2,020,873 | 20.209 | 130 | 134 | fits | 70,405 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 2,035,728 | 20.357 | 130 | 134 | fits | 70,405 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 2,052,221 | 20.522 | 130 | 134 | fits | 70,405 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 2,212,753 | 22.128 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 2,229,798 | 22.298 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 2,244,709 | 22.447 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 2,261,202 | 22.612 | 130 | 134 | fits | 70,148 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,402,646 | 24.026 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,414,759 | 24.148 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,431,457 | 24.315 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,447,921 | 24.479 | 130 | 134 | fits | 64,631 | 202 | 0.143 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 173,071 | 1.731 | 20 | 200 | fits | 163,237 | 236 | 0.314 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 466,743 | 4.667 | 20 | 20 | fits | 157,917 | 154 | 0.398 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 446,539 | 4.465 | 20 | 24 | fits | 157,917 | 154 | 0.398 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 427,268 | 4.273 | 20 | 50 | fits | 157,917 | 154 | 0.398 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 785,345 | 7.853 | 20 | 20 | fits | 106,519 | 50 | 0.560 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 1,478,035 | 14.780 | 130 | 134 | fits | 75,727 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,495,828 | 14.958 | 130 | 134 | fits | 75,727 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 220,654 | 2.207 | 130 | 134 | fits | 99,678 | 213 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 238,331 | 2.383 | 130 | 134 | fits | 99,678 | 213 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 253,972 | 2.540 | 130 | 134 | fits | 99,678 | 213 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 270,850 | 2.708 | 130 | 134 | fits | 99,678 | 213 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 517,154 | 5.172 | 130 | 134 | fits | 74,867 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 534,825 | 5.348 | 130 | 134 | fits | 74,867 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 550,834 | 5.508 | 130 | 134 | fits | 74,867 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 567,777 | 5.678 | 130 | 134 | fits | 74,867 | 205 | 0.173 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 1,511,534 | 15.115 | 130 | 134 | fits | 75,727 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 1,528,116 | 15.281 | 130 | 134 | fits | 75,727 | 203 | 0.223 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 405,999 | 4.060 | 130 | 134 | fits | 100,960 | 211 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 424,264 | 4.243 | 130 | 134 | fits | 100,960 | 211 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 440,646 | 4.406 | 130 | 134 | fits | 100,960 | 211 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 458,073 | 4.581 | 130 | 134 | fits | 100,960 | 211 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 1,618,516 | 16.185 | 130 | 134 | fits | 72,432 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 1,635,670 | 16.357 | 130 | 134 | fits | 72,432 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 1,650,669 | 16.507 | 130 | 134 | fits | 72,432 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 1,667,385 | 16.674 | 130 | 134 | fits | 72,432 | 203 | 0.176 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 1,812,029 | 18.120 | 130 | 134 | fits | 73,279 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 1,829,678 | 18.297 | 130 | 134 | fits | 73,279 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 1,845,486 | 18.455 | 130 | 134 | fits | 73,279 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 1,862,583 | 18.626 | 130 | 134 | fits | 73,279 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 2,024,377 | 20.244 | 130 | 134 | fits | 70,965 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 2,041,645 | 20.416 | 130 | 134 | fits | 70,965 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 2,056,881 | 20.569 | 130 | 134 | fits | 70,965 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 2,073,374 | 20.734 | 130 | 134 | fits | 70,965 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 2,214,794 | 22.148 | 130 | 134 | fits | 70,188 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 2,231,839 | 22.318 | 130 | 134 | fits | 70,188 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 2,246,694 | 22.467 | 130 | 134 | fits | 70,188 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 2,263,187 | 22.632 | 130 | 134 | fits | 70,188 | 203 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 2,425,272 | 24.253 | 130 | 134 | fits | 70,282 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 2,442,317 | 24.423 | 130 | 134 | fits | 70,282 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 2,457,237 | 24.572 | 130 | 134 | fits | 70,282 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 2,473,730 | 24.737 | 130 | 134 | fits | 70,282 | 203 | 0.175 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 2,609,680 | 26.097 | 130 | 134 | fits | 31,105 | 101 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,621,791 | 26.218 | 130 | 134 | fits | 31,105 | 101 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 302,390 | 3.024 | 130 | 134 | fits | 51,055 | 103 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 323,193 | 3.232 | 130 | 134 | fits | 51,055 | 103 | 0.070 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 166,544 | 1.665 | 20 | 200 | fits | 157,997 | 231 | 0.248 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 593,305 | 5.933 | 20 | 20 | fits | 137,594 | 61 | 0.655 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 435,507 | 4.355 | 20 | 24 | fits | 151,152 | 147 | 0.411 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 416,236 | 4.162 | 20 | 50 | fits | 151,152 | 147 | 0.411 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 784,212 | 7.842 | 20 | 20 | fits | 115,256 | 54 | 0.547 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

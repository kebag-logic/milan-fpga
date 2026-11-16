### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 5.431 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.adp.if0` (notice-burst-5) | 5.634 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.aecp.if0` (notice-burst-0) | 4.532 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.maap.if0` (notice-burst-5) | 5.037 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.srp.if0` (notice-burst-5) | 10.010 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-7.mrpdu.periodic.if0` (notice-every-7) | 1.260 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.36.0.if0` (notice-burst-6) | 21.496 (21.715) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1619 | 0 | 151,038 (1.510) | fits |
| notice-every-1 | 1625 | 0 | 151,038 (1.510) | fits |
| notice-every-2 | 1615 | 0 | 151,038 (1.510) | fits |
| notice-every-3 | 1612 | 0 | 150,828 (1.508) | fits |
| notice-every-4 | 1612 | 0 | 151,038 (1.510) | fits |
| notice-every-5 | 1609 | 0 | 151,110 (1.511) | fits |
| notice-every-6 | 1612 | 0 | 151,110 (1.511) | fits |
| notice-every-7 | 1605 | 0 | 150,750 (1.508) | fits |
| notice-burst-0 | 1112 | 0 | 151,074 (1.511) | fits |
| notice-burst-1 | 1147 | 0 | 151,122 (1.511) | fits |
| notice-burst-2 | 1104 | 0 | 157,340 (1.573) | fits |
| notice-burst-3 | 1092 | 0 | 150,750 (1.508) | fits |
| notice-burst-4 | 1099 | 0 | 150,732 (1.507) | fits |
| notice-burst-5 | 1101 | 0 | 151,164 (1.512) | fits |
| notice-burst-6 | 1100 | 0 | 151,883 (1.519) | fits |
| notice-burst-7 | 1101 | 0 | 154,530 (1.545) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.168 | 130 | 16 | 2 | within |
| notice-every-0 | 8.373 | 130 | 16 | 2 | within |
| notice-every-0 | 3.007 | 130 | 16 | 2 | within |
| notice-every-0 | 3.218 | 130 | 16 | 2 | within |
| notice-every-0 | 4.161 | 130 | 16 | 2 | within |
| notice-every-0 | 4.368 | 130 | 16 | 2 | within |
| notice-every-0 | 6.078 | 130 | 16 | 2 | within |
| notice-every-0 | 6.285 | 130 | 16 | 2 | within |
| notice-every-0 | 8.552 | 130 | 16 | 2 | within |
| notice-every-0 | 10.022 | 130 | 16 | 2 | within |
| notice-every-0 | 3.426 | 130 | 16 | 2 | within |
| notice-every-0 | 4.577 | 130 | 16 | 2 | within |
| notice-every-1 | 2.213 | 130 | 16 | 2 | within |
| notice-every-1 | 2.419 | 130 | 16 | 2 | within |
| notice-every-1 | 4.376 | 130 | 16 | 2 | within |
| notice-every-1 | 4.587 | 130 | 16 | 2 | within |
| notice-every-1 | 6.348 | 130 | 16 | 2 | within |
| notice-every-1 | 6.553 | 130 | 16 | 2 | within |
| notice-every-1 | 8.277 | 130 | 16 | 2 | within |
| notice-every-1 | 8.482 | 130 | 16 | 2 | within |
| notice-every-1 | 2.606 | 130 | 16 | 2 | within |
| notice-every-1 | 4.768 | 130 | 16 | 2 | within |
| notice-every-1 | 6.755 | 130 | 16 | 2 | within |
| notice-every-1 | 8.681 | 130 | 16 | 2 | within |
| notice-every-2 | 1.939 | 130 | 16 | 2 | within |
| notice-every-2 | 2.145 | 130 | 16 | 2 | within |
| notice-every-2 | 6.019 | 130 | 16 | 2 | within |
| notice-every-2 | 6.227 | 130 | 16 | 2 | within |
| notice-every-2 | 7.971 | 130 | 16 | 2 | within |
| notice-every-2 | 8.176 | 130 | 16 | 2 | within |
| notice-every-2 | 3.888 | 130 | 16 | 2 | within |
| notice-every-2 | 4.100 | 130 | 16 | 2 | within |
| notice-every-2 | 2.332 | 130 | 16 | 2 | within |
| notice-every-2 | 4.281 | 130 | 16 | 2 | within |
| notice-every-2 | 6.429 | 130 | 16 | 2 | within |
| notice-every-2 | 8.378 | 130 | 16 | 2 | within |
| notice-every-3 | 4.069 | 130 | 16 | 2 | within |
| notice-every-3 | 4.273 | 130 | 16 | 2 | within |
| notice-every-3 | 6.026 | 130 | 16 | 2 | within |
| notice-every-3 | 6.232 | 130 | 16 | 2 | within |
| notice-every-3 | 2.950 | 130 | 16 | 2 | within |
| notice-every-3 | 3.162 | 130 | 16 | 2 | within |
| notice-every-3 | 7.953 | 130 | 16 | 2 | within |
| notice-every-3 | 8.157 | 130 | 16 | 2 | within |
| notice-every-3 | 4.458 | 130 | 16 | 2 | within |
| notice-every-3 | 6.410 | 130 | 16 | 2 | within |
| notice-every-3 | 3.370 | 130 | 16 | 2 | within |
| notice-every-3 | 8.357 | 130 | 16 | 2 | within |
| notice-every-4 | 3.917 | 130 | 16 | 2 | within |
| notice-every-4 | 4.124 | 130 | 16 | 2 | within |
| notice-every-4 | 5.880 | 130 | 16 | 2 | within |
| notice-every-4 | 6.087 | 130 | 16 | 2 | within |
| notice-every-4 | 7.979 | 130 | 16 | 2 | within |
| notice-every-4 | 8.183 | 130 | 16 | 2 | within |
| notice-every-4 | 1.932 | 130 | 16 | 2 | within |
| notice-every-4 | 2.144 | 130 | 16 | 2 | within |
| notice-every-4 | 4.310 | 130 | 16 | 2 | within |
| notice-every-4 | 6.264 | 130 | 16 | 2 | within |
| notice-every-4 | 2.351 | 130 | 16 | 2 | within |
| notice-every-4 | 8.385 | 130 | 16 | 2 | within |
| notice-every-5 | 6.225 | 130 | 16 | 2 | within |
| notice-every-5 | 6.431 | 130 | 16 | 2 | within |
| notice-every-5 | 2.959 | 130 | 16 | 2 | within |
| notice-every-5 | 3.171 | 130 | 16 | 2 | within |
| notice-every-5 | 4.072 | 130 | 16 | 2 | within |
| notice-every-5 | 4.279 | 130 | 16 | 2 | within |
| notice-every-5 | 7.949 | 130 | 16 | 2 | within |
| notice-every-5 | 8.153 | 130 | 16 | 2 | within |
| notice-every-5 | 6.612 | 130 | 16 | 2 | within |
| notice-every-5 | 8.326 | 130 | 16 | 2 | within |
| notice-every-5 | 3.379 | 130 | 16 | 2 | within |
| notice-every-5 | 4.488 | 130 | 16 | 2 | within |
| notice-every-6 | 6.074 | 130 | 16 | 2 | within |
| notice-every-6 | 6.279 | 130 | 16 | 2 | within |
| notice-every-6 | 1.938 | 130 | 16 | 2 | within |
| notice-every-6 | 2.149 | 130 | 16 | 2 | within |
| notice-every-6 | 3.916 | 130 | 16 | 2 | within |
| notice-every-6 | 4.126 | 130 | 16 | 2 | within |
| notice-every-6 | 7.966 | 130 | 16 | 2 | within |
| notice-every-6 | 8.170 | 130 | 16 | 2 | within |
| notice-every-6 | 6.461 | 130 | 16 | 2 | within |
| notice-every-6 | 8.343 | 130 | 16 | 2 | within |
| notice-every-6 | 2.357 | 130 | 16 | 2 | within |
| notice-every-6 | 4.335 | 130 | 16 | 2 | within |
| notice-every-7 | 8.118 | 130 | 16 | 2 | within |
| notice-every-7 | 8.322 | 130 | 16 | 2 | within |
| notice-every-7 | 4.122 | 130 | 16 | 2 | within |
| notice-every-7 | 4.332 | 130 | 16 | 2 | within |
| notice-every-7 | 6.066 | 130 | 16 | 2 | within |
| notice-every-7 | 6.273 | 130 | 16 | 2 | within |
| notice-every-7 | 3.001 | 130 | 16 | 2 | within |
| notice-every-7 | 3.214 | 130 | 16 | 2 | within |
| notice-every-7 | 8.501 | 130 | 16 | 2 | within |
| notice-every-7 | 9.994 | 130 | 16 | 2 | within |
| notice-every-7 | 3.421 | 130 | 16 | 2 | within |
| notice-every-7 | 4.542 | 130 | 16 | 2 | within |
| notice-burst-0 | 8.367 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.326 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.545 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.745 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.261 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.465 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.659 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.872 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.645 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.285 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.489 | 130 | 16 | 1 | within |
| notice-burst-0 | 6.648 | 130 | 16 | 1 | within |
| notice-burst-1 | 8.823 | 130 | 16 | 1 | within |
| notice-burst-1 | 14.390 | 130 | 16 | 1 | within |
| notice-burst-1 | 14.608 | 130 | 16 | 1 | within |
| notice-burst-1 | 14.808 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.649 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.860 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.522 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.731 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.134 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.307 | 130 | 16 | 1 | within |
| notice-burst-1 | 16.506 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.761 | 130 | 16 | 1 | within |
| notice-burst-2 | 8.832 | 130 | 16 | 2 | within |
| notice-burst-2 | 13.743 | 130 | 16 | 2 | within |
| notice-burst-2 | 13.959 | 130 | 16 | 2 | within |
| notice-burst-2 | 14.160 | 130 | 16 | 2 | within |
| notice-burst-2 | 2.289 | 130 | 16 | 2 | within |
| notice-burst-2 | 2.499 | 130 | 16 | 2 | within |
| notice-burst-2 | 2.690 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.146 | 130 | 16 | 2 | within |
| notice-burst-2 | 15.141 | 130 | 16 | 2 | within |
| notice-burst-2 | 15.314 | 130 | 16 | 2 | within |
| notice-burst-2 | 15.514 | 130 | 16 | 2 | within |
| notice-burst-2 | 5.009 | 130 | 16 | 2 | within |
| notice-burst-3 | 11.736 | 130 | 16 | 0 | within |
| notice-burst-3 | 11.943 | 130 | 16 | 0 | within |
| notice-burst-3 | 3.266 | 130 | 16 | 0 | within |
| notice-burst-3 | 12.146 | 130 | 16 | 0 | within |
| notice-burst-3 | 12.833 | 130 | 16 | 0 | within |
| notice-burst-3 | 13.037 | 130 | 16 | 0 | within |
| notice-burst-3 | 13.223 | 130 | 16 | 0 | within |
| notice-burst-3 | 14.922 | 130 | 16 | 0 | within |
| notice-burst-3 | 15.107 | 130 | 16 | 0 | within |
| notice-burst-3 | 15.276 | 130 | 16 | 0 | within |
| notice-burst-3 | 16.795 | 130 | 16 | 0 | within |
| notice-burst-3 | 16.999 | 130 | 16 | 0 | within |
| notice-burst-4 | 11.151 | 130 | 16 | 1 | within |
| notice-burst-4 | 11.358 | 130 | 16 | 1 | within |
| notice-burst-4 | 2.677 | 130 | 16 | 1 | within |
| notice-burst-4 | 11.561 | 130 | 16 | 1 | within |
| notice-burst-4 | 12.248 | 130 | 16 | 1 | within |
| notice-burst-4 | 12.452 | 130 | 16 | 1 | within |
| notice-burst-4 | 12.638 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.337 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.522 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.691 | 130 | 16 | 1 | within |
| notice-burst-4 | 16.210 | 130 | 16 | 1 | within |
| notice-burst-4 | 16.413 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.194 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.402 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.597 | 130 | 16 | 1 | within |
| notice-burst-5 | 6.856 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.993 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.201 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.387 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.247 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.041 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.216 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.449 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.648 | 130 | 16 | 1 | within |
| notice-burst-6 | 6.819 | 130 | 16 | 1 | within |
| notice-burst-6 | 15.194 | 130 | 16 | 1 | within |
| notice-burst-6 | 15.412 | 130 | 16 | 1 | within |
| notice-burst-6 | 15.612 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.159 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.364 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.549 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.250 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.434 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.603 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.293 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.496 | 130 | 16 | 1 | within |
| notice-burst-7 | 9.191 | 130 | 16 | 1 | within |
| notice-burst-7 | 15.943 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.399 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.608 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.796 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.253 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.449 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.649 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.131 | 130 | 16 | 1 | within |
| notice-burst-7 | 16.301 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.306 | 130 | 16 | 1 | within |
| notice-burst-7 | 4.391 | 130 | 16 | 1 | within |

Latest: 21.496 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 147,276 (1.473) | 75,915 (0.759) |
| notice-every-1 | 307 | 100,616 (1.006) | 75,915 (0.759) |
| notice-every-2 | 307 | 104,851 (1.049) | 75,922 (0.759) |
| notice-every-3 | 307 | 146,266 (1.463) | 76,354 (0.764) |
| notice-every-4 | 307 | 90,430 (0.904) | 75,535 (0.755) |
| notice-every-5 | 307 | 147,364 (1.474) | 75,535 (0.755) |
| notice-every-6 | 307 | 90,430 (0.904) | 75,535 (0.755) |
| notice-every-7 | 307 | 146,547 (1.465) | 75,698 (0.757) |
| notice-burst-0 | 317 | 102,834 (1.028) | 77,810 (0.778) |
| notice-burst-1 | 317 | 100,616 (1.006) | 77,810 (0.778) |
| notice-burst-2 | 317 | 104,851 (1.049) | 77,888 (0.779) |
| notice-burst-3 | 317 | 110,220 (1.102) | 77,810 (0.778) |
| notice-burst-4 | 317 | 99,788 (0.998) | 77,810 (0.778) |
| notice-burst-5 | 317 | 105,164 (1.052) | 77,810 (0.778) |
| notice-burst-6 | 317 | 102,561 (1.026) | 77,810 (0.778) |
| notice-burst-7 | 317 | 100,725 (1.007) | 77,810 (0.778) |

Longest pass that carries a step: 147,364 CPU cycles (1.474 ms), notice-every-5; longest step: 77,888 (0.779 ms), notice-burst-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 816,840 | 8.168 | 130 | 134 | fits | 65,058 | 152 | 0.268 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 837,276 | 8.373 | 130 | 134 | fits | 65,058 | 152 | 0.268 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 300,656 | 3.007 | 130 | 134 | fits | 147,276 | 153 | 0.251 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 321,792 | 3.218 | 130 | 134 | fits | 147,276 | 153 | 0.251 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 416,097 | 4.161 | 130 | 134 | fits | 68,213 | 153 | 0.257 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 436,827 | 4.368 | 130 | 134 | fits | 68,213 | 153 | 0.257 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 607,807 | 6.078 | 130 | 134 | fits | 46,888 | 103 | 0.306 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 628,537 | 6.285 | 130 | 134 | fits | 46,888 | 103 | 0.306 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 855,226 | 8.552 | 130 | 134 | fits | 65,058 | 152 | 0.268 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 1,002,184 | 10.022 | 130 | 134 | fits | 23,113 | 51 | 0.367 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 342,650 | 3.426 | 130 | 134 | fits | 147,276 | 153 | 0.251 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 457,721 | 4.577 | 130 | 134 | fits | 68,213 | 153 | 0.257 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 161,021 | 1.610 | 20 | 200 | fits | 150,604 | 269 | 0.381 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 437,962 | 4.380 | 20 | 20 | fits | 142,908 | 127 | 0.515 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 417,758 | 4.178 | 20 | 24 | fits | 142,908 | 127 | 0.515 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 398,487 | 3.985 | 20 | 50 | fits | 142,908 | 127 | 0.515 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 956,438 | 9.564 | 20 | 20 | fits | 83,615 | 41 | 0.625 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 122,935 | 1.229 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 221,325 | 2.213 | 130 | 134 | fits | 68,953 | 155 | 0.302 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 241,895 | 2.419 | 130 | 134 | fits | 68,953 | 155 | 0.302 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 437,619 | 4.376 | 130 | 134 | fits | 67,587 | 151 | 0.284 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 458,665 | 4.587 | 130 | 134 | fits | 67,587 | 151 | 0.284 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 634,841 | 6.348 | 130 | 134 | fits | 66,765 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 655,275 | 6.553 | 130 | 134 | fits | 66,765 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 827,659 | 8.277 | 130 | 134 | fits | 65,676 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 848,158 | 8.482 | 130 | 134 | fits | 65,676 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 260,588 | 2.606 | 130 | 134 | fits | 68,953 | 155 | 0.302 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 476,836 | 4.768 | 130 | 134 | fits | 67,587 | 151 | 0.284 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 675,464 | 6.755 | 130 | 134 | fits | 66,765 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 868,114 | 8.681 | 130 | 134 | fits | 65,676 | 153 | 0.254 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 161,690 | 1.617 | 20 | 200 | fits | 150,760 | 269 | 0.366 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 452,669 | 4.527 | 20 | 20 | fits | 142,656 | 127 | 0.513 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 432,465 | 4.325 | 20 | 24 | fits | 142,656 | 127 | 0.513 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 413,194 | 4.132 | 20 | 50 | fits | 142,656 | 127 | 0.513 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 954,915 | 9.549 | 20 | 20 | fits | 82,493 | 41 | 0.597 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 101,361 | 1.014 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 193,929 | 1.939 | 130 | 134 | fits | 68,540 | 155 | 0.292 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 214,499 | 2.145 | 130 | 134 | fits | 68,540 | 155 | 0.292 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 601,946 | 6.019 | 130 | 134 | fits | 68,266 | 153 | 0.257 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 622,658 | 6.227 | 130 | 134 | fits | 68,266 | 153 | 0.257 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 797,136 | 7.971 | 130 | 134 | fits | 66,007 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 817,635 | 8.176 | 130 | 134 | fits | 66,007 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 388,794 | 3.888 | 130 | 134 | fits | 67,337 | 153 | 0.283 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 410,037 | 4.100 | 130 | 134 | fits | 67,337 | 153 | 0.283 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 233,192 | 2.332 | 130 | 134 | fits | 68,540 | 155 | 0.292 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 428,129 | 4.281 | 130 | 134 | fits | 67,337 | 153 | 0.283 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 642,945 | 6.429 | 130 | 134 | fits | 68,266 | 153 | 0.257 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 837,795 | 8.378 | 130 | 134 | fits | 66,007 | 153 | 0.255 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 164,673 | 1.647 | 20 | 200 | fits | 149,397 | 284 | 0.372 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 461,161 | 4.612 | 20 | 20 | fits | 145,378 | 113 | 0.521 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 440,957 | 4.410 | 20 | 24 | fits | 145,378 | 113 | 0.521 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 104,930 | 1.049 | 20 | 50 | fits | 149,397 | 284 | 0.372 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 975,099 | 9.751 | 20 | 20 | fits | 84,692 | 47 | 0.612 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 120,283 | 1.203 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 406,868 | 4.069 | 130 | 134 | fits | 66,664 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 427,343 | 4.273 | 130 | 134 | fits | 66,664 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 602,583 | 6.026 | 130 | 134 | fits | 65,559 | 153 | 0.256 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 623,241 | 6.232 | 130 | 134 | fits | 65,559 | 153 | 0.256 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 295,038 | 2.950 | 130 | 134 | fits | 146,266 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 316,174 | 3.162 | 130 | 134 | fits | 146,266 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 795,281 | 7.953 | 130 | 134 | fits | 65,895 | 155 | 0.251 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 815,715 | 8.157 | 130 | 134 | fits | 65,895 | 155 | 0.251 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 445,817 | 4.458 | 130 | 134 | fits | 66,664 | 153 | 0.271 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 640,953 | 6.410 | 130 | 134 | fits | 65,559 | 153 | 0.256 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 336,953 | 3.370 | 130 | 134 | fits | 146,266 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 835,671 | 8.357 | 130 | 134 | fits | 65,895 | 155 | 0.251 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 172,545 | 1.725 | 20 | 200 | fits | 149,098 | 289 | 0.372 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 455,905 | 4.559 | 20 | 20 | fits | 146,617 | 119 | 0.520 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 435,701 | 4.357 | 20 | 24 | fits | 146,617 | 119 | 0.520 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 112,802 | 1.128 | 20 | 50 | fits | 149,098 | 289 | 0.372 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 970,048 | 9.700 | 20 | 20 | fits | 73,233 | 37 | 0.673 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 115,242 | 1.152 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 391,744 | 3.917 | 130 | 134 | fits | 68,445 | 155 | 0.302 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 412,429 | 4.124 | 130 | 134 | fits | 68,445 | 155 | 0.302 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 587,980 | 5.880 | 130 | 134 | fits | 65,605 | 153 | 0.258 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 608,684 | 6.087 | 130 | 134 | fits | 65,605 | 153 | 0.258 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 797,913 | 7.979 | 130 | 134 | fits | 66,008 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 818,347 | 8.183 | 130 | 134 | fits | 66,008 | 153 | 0.254 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 193,156 | 1.932 | 130 | 134 | fits | 70,838 | 155 | 0.276 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 214,401 | 2.144 | 130 | 134 | fits | 70,838 | 155 | 0.276 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 430,970 | 4.310 | 130 | 134 | fits | 68,445 | 155 | 0.302 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 626,396 | 6.264 | 130 | 134 | fits | 65,605 | 153 | 0.258 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 235,115 | 2.351 | 130 | 134 | fits | 70,838 | 155 | 0.276 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 838,507 | 8.385 | 130 | 134 | fits | 66,008 | 153 | 0.254 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 136,652 | 1.367 | 20 | 200 | fits | 128,384 | 154 | 0.389 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 541,368 | 5.414 | 20 | 20 | fits | 93,615 | 38 | 0.741 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 427,549 | 4.275 | 20 | 24 | fits | 144,506 | 133 | 0.521 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 408,278 | 4.083 | 20 | 50 | fits | 144,506 | 133 | 0.521 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 970,281 | 9.703 | 20 | 20 | fits | 74,666 | 43 | 0.656 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 115,745 | 1.157 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 622,517 | 6.225 | 130 | 134 | fits | 65,718 | 153 | 0.268 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 643,071 | 6.431 | 130 | 134 | fits | 65,718 | 153 | 0.268 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 295,888 | 2.959 | 130 | 134 | fits | 147,364 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 317,064 | 3.171 | 130 | 134 | fits | 147,364 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 407,157 | 4.072 | 130 | 134 | fits | 68,204 | 153 | 0.257 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 427,887 | 4.279 | 130 | 134 | fits | 68,204 | 153 | 0.257 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 794,895 | 7.949 | 130 | 134 | fits | 62,852 | 153 | 0.250 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 815,275 | 8.153 | 130 | 134 | fits | 62,852 | 153 | 0.250 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 661,235 | 6.612 | 130 | 134 | fits | 65,718 | 153 | 0.268 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 832,615 | 8.326 | 130 | 134 | fits | 62,852 | 153 | 0.250 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 337,922 | 3.379 | 130 | 134 | fits | 147,364 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 448,781 | 4.488 | 130 | 134 | fits | 68,204 | 153 | 0.257 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 167,446 | 1.674 | 20 | 200 | fits | 149,010 | 284 | 0.370 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 467,792 | 4.678 | 20 | 20 | fits | 145,455 | 115 | 0.524 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 447,588 | 4.476 | 20 | 24 | fits | 145,455 | 115 | 0.524 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 107,703 | 1.077 | 20 | 50 | fits | 149,010 | 284 | 0.370 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 979,412 | 9.794 | 20 | 20 | fits | 83,498 | 41 | 0.625 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 114,559 | 1.146 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 607,398 | 6.074 | 130 | 134 | fits | 65,672 | 153 | 0.267 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 627,906 | 6.279 | 130 | 134 | fits | 65,672 | 153 | 0.267 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 193,801 | 1.938 | 130 | 134 | fits | 71,731 | 155 | 0.285 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 214,875 | 2.149 | 130 | 134 | fits | 71,731 | 155 | 0.285 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 391,628 | 3.916 | 130 | 134 | fits | 69,938 | 155 | 0.286 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 412,568 | 4.126 | 130 | 134 | fits | 69,938 | 155 | 0.286 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 796,602 | 7.966 | 130 | 134 | fits | 62,652 | 151 | 0.249 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 816,982 | 8.170 | 130 | 134 | fits | 62,652 | 151 | 0.249 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 646,070 | 6.461 | 130 | 134 | fits | 65,672 | 153 | 0.267 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 834,322 | 8.343 | 130 | 134 | fits | 62,652 | 151 | 0.249 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 235,733 | 2.357 | 130 | 134 | fits | 71,731 | 155 | 0.285 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 433,529 | 4.335 | 130 | 134 | fits | 69,938 | 155 | 0.286 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 175,545 | 1.755 | 20 | 200 | fits | 147,854 | 285 | 0.372 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 464,331 | 4.643 | 20 | 20 | fits | 146,393 | 117 | 0.520 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 444,127 | 4.441 | 20 | 24 | fits | 146,393 | 117 | 0.520 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 115,802 | 1.158 | 20 | 50 | fits | 147,854 | 285 | 0.372 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 972,481 | 9.725 | 20 | 20 | fits | 72,669 | 37 | 0.664 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 121,739 | 1.217 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 811,751 | 8.118 | 130 | 134 | fits | 65,102 | 152 | 0.268 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 832,187 | 8.322 | 130 | 134 | fits | 65,102 | 152 | 0.268 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 412,185 | 4.122 | 130 | 134 | fits | 69,795 | 153 | 0.261 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 433,193 | 4.332 | 130 | 134 | fits | 69,795 | 153 | 0.261 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 606,555 | 6.066 | 130 | 134 | fits | 47,015 | 103 | 0.308 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 627,285 | 6.273 | 130 | 134 | fits | 47,015 | 103 | 0.308 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 300,066 | 3.001 | 130 | 134 | fits | 146,547 | 153 | 0.244 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 321,373 | 3.214 | 130 | 134 | fits | 146,547 | 153 | 0.244 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 850,137 | 8.501 | 130 | 134 | fits | 65,102 | 152 | 0.268 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 999,353 | 9.994 | 130 | 134 | fits | 23,192 | 51 | 0.364 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 342,087 | 3.421 | 130 | 134 | fits | 146,547 | 153 | 0.244 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 454,166 | 4.542 | 130 | 134 | fits | 69,795 | 153 | 0.261 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 169,217 | 1.692 | 20 | 200 | fits | 147,632 | 281 | 0.377 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 462,922 | 4.629 | 20 | 20 | fits | 144,272 | 112 | 0.522 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 442,718 | 4.427 | 20 | 24 | fits | 144,272 | 112 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 109,474 | 1.095 | 20 | 50 | fits | 147,632 | 281 | 0.377 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 979,320 | 9.793 | 20 | 20 | fits | 83,571 | 41 | 0.625 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 126,032 | 1.260 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 836,743 | 8.367 | 130 | 134 | fits | 26,723 | 52 | 0.437 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,532,551 | 15.326 | 130 | 134 | fits | 70,743 | 153 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,554,484 | 15.545 | 130 | 134 | fits | 70,743 | 153 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,574,539 | 15.745 | 130 | 134 | fits | 70,743 | 153 | 0.321 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 1,726,148 | 17.261 | 130 | 134 | fits | 63,986 | 152 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 1,746,481 | 17.465 | 130 | 134 | fits | 63,986 | 152 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 365,862 | 3.659 | 130 | 134 | fits | 50,902 | 102 | 0.346 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 387,234 | 3.872 | 130 | 134 | fits | 50,902 | 102 | 0.346 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,764,510 | 17.645 | 130 | 134 | fits | 63,986 | 152 | 0.265 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,928,495 | 19.285 | 130 | 134 | fits | 43,538 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,948,872 | 19.489 | 130 | 134 | fits | 43,538 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 664,849 | 6.648 | 130 | 134 | fits | 28,808 | 53 | 0.426 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 146,220 | 1.462 | 20 | 200 | fits | 146,245 | 254 | 0.360 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 473,359 | 4.734 | 20 | 20 | fits | 147,272 | 152 | 0.500 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 453,155 | 4.532 | 20 | 24 | fits | 147,272 | 152 | 0.500 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 433,884 | 4.339 | 20 | 50 | fits | 147,272 | 152 | 0.500 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 932,000 | 9.320 | 20 | 20 | fits | 79,598 | 34 | 0.601 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 882,306 | 8.823 | 130 | 134 | fits | 28,598 | 51 | 0.487 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,438,967 | 14.390 | 130 | 134 | fits | 70,435 | 153 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,460,799 | 14.608 | 130 | 134 | fits | 70,435 | 153 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,480,782 | 14.808 | 130 | 134 | fits | 70,435 | 153 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 264,880 | 2.649 | 130 | 134 | fits | 50,364 | 102 | 0.346 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 286,008 | 2.860 | 130 | 134 | fits | 50,364 | 102 | 0.346 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 352,247 | 3.522 | 130 | 134 | fits | 62,296 | 111 | 0.334 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 373,143 | 3.731 | 130 | 134 | fits | 62,296 | 111 | 0.334 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,613,394 | 16.134 | 130 | 134 | fits | 60,925 | 152 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,630,695 | 16.307 | 130 | 134 | fits | 60,925 | 152 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,650,579 | 16.506 | 130 | 134 | fits | 60,925 | 152 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 576,087 | 5.761 | 130 | 134 | fits | 28,714 | 52 | 0.438 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 161,048 | 1.610 | 20 | 200 | fits | 151,122 | 270 | 0.369 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 446,869 | 4.469 | 20 | 20 | fits | 132,427 | 113 | 0.518 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 426,665 | 4.267 | 20 | 24 | fits | 132,427 | 113 | 0.518 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 407,394 | 4.074 | 20 | 50 | fits | 132,427 | 113 | 0.518 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 942,021 | 9.420 | 20 | 20 | fits | 79,542 | 34 | 0.602 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 883,208 | 8.832 | 130 | 134 | fits | 30,102 | 51 | 0.526 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,374,264 | 13.743 | 130 | 134 | fits | 70,026 | 153 | 0.310 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,395,922 | 13.959 | 130 | 134 | fits | 70,026 | 153 | 0.310 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,415,991 | 14.160 | 130 | 134 | fits | 70,026 | 153 | 0.310 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 228,932 | 2.289 | 130 | 134 | fits | 67,968 | 152 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 249,917 | 2.499 | 130 | 134 | fits | 67,968 | 152 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 269,032 | 2.690 | 130 | 134 | fits | 67,968 | 152 | 0.266 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 314,629 | 3.146 | 130 | 134 | fits | 46,849 | 68 | 0.500 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,514,114 | 15.141 | 130 | 134 | fits | 60,794 | 152 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,531,443 | 15.314 | 130 | 134 | fits | 60,794 | 152 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,551,373 | 15.514 | 130 | 134 | fits | 60,794 | 152 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 500,942 | 5.009 | 130 | 134 | fits | 27,293 | 52 | 0.375 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 487,289 | 4.873 | 20 | 200 | fits | 116,612 | 195 | 0.387 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 467,021 | 4.670 | 20 | 20 | fits | 116,612 | 195 | 0.387 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 330,205 | 3.302 | 20 | 24 | fits | 150,536 | 182 | 0.470 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 427,546 | 4.275 | 20 | 50 | fits | 116,612 | 195 | 0.387 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 965,334 | 9.653 | 20 | 20 | fits | 89,949 | 38 | 0.563 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,173,599 | 11.736 | 130 | 134 | fits | 71,385 | 153 | 0.330 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,194,283 | 11.943 | 130 | 134 | fits | 71,385 | 153 | 0.330 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 326,591 | 3.266 | 130 | 134 | fits | 29,750 | 52 | 0.500 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,214,580 | 12.146 | 130 | 134 | fits | 71,385 | 153 | 0.330 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,283,321 | 12.833 | 130 | 134 | fits | 64,684 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,303,731 | 13.037 | 130 | 134 | fits | 64,684 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 1,322,317 | 13.223 | 130 | 134 | fits | 64,684 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,492,248 | 14.922 | 130 | 134 | fits | 61,905 | 152 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,510,690 | 15.107 | 130 | 134 | fits | 61,905 | 152 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,527,580 | 15.276 | 130 | 134 | fits | 61,905 | 152 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,679,541 | 16.795 | 130 | 134 | fits | 46,161 | 103 | 0.274 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 1,699,856 | 16.999 | 130 | 134 | fits | 46,161 | 103 | 0.274 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 144,258 | 1.443 | 20 | 200 | fits | 144,910 | 255 | 0.358 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 447,513 | 4.475 | 20 | 20 | fits | 145,728 | 141 | 0.492 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 427,309 | 4.273 | 20 | 24 | fits | 145,728 | 141 | 0.492 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 408,038 | 4.080 | 20 | 50 | fits | 145,728 | 141 | 0.492 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 908,608 | 9.086 | 20 | 20 | fits | 79,979 | 34 | 0.601 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,115,106 | 11.151 | 130 | 134 | fits | 71,385 | 153 | 0.330 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,135,790 | 11.358 | 130 | 134 | fits | 71,385 | 153 | 0.330 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 267,687 | 2.677 | 130 | 134 | fits | 29,889 | 52 | 0.504 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,156,087 | 11.561 | 130 | 134 | fits | 71,385 | 153 | 0.330 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,224,814 | 12.248 | 130 | 134 | fits | 64,684 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,245,224 | 12.452 | 130 | 134 | fits | 64,684 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,263,810 | 12.638 | 130 | 134 | fits | 64,684 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,433,727 | 14.337 | 130 | 134 | fits | 61,905 | 152 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,452,169 | 14.522 | 130 | 134 | fits | 61,905 | 152 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,469,059 | 14.691 | 130 | 134 | fits | 61,905 | 152 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,621,020 | 16.210 | 130 | 134 | fits | 46,161 | 103 | 0.274 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,641,335 | 16.413 | 130 | 134 | fits | 46,161 | 103 | 0.274 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 144,992 | 1.450 | 20 | 200 | fits | 144,681 | 255 | 0.358 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 448,654 | 4.487 | 20 | 20 | fits | 145,617 | 141 | 0.492 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 428,450 | 4.285 | 20 | 24 | fits | 145,617 | 141 | 0.492 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 409,179 | 4.092 | 20 | 50 | fits | 145,617 | 141 | 0.492 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 909,822 | 9.098 | 20 | 20 | fits | 80,057 | 34 | 0.602 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 619,440 | 6.194 | 130 | 134 | fits | 83,512 | 161 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 640,214 | 6.402 | 130 | 134 | fits | 83,512 | 161 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 659,720 | 6.597 | 130 | 134 | fits | 83,512 | 161 | 0.318 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 685,573 | 6.856 | 130 | 134 | fits | 61,458 | 152 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,699,259 | 16.993 | 130 | 134 | fits | 68,388 | 153 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,720,088 | 17.201 | 130 | 134 | fits | 68,388 | 153 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,738,746 | 17.387 | 130 | 134 | fits | 68,388 | 153 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,824,668 | 18.247 | 130 | 134 | fits | 66,178 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 704,077 | 7.041 | 130 | 134 | fits | 61,458 | 152 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 721,565 | 7.216 | 130 | 134 | fits | 61,458 | 152 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 1,844,921 | 18.449 | 130 | 134 | fits | 66,178 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 1,864,802 | 18.648 | 130 | 134 | fits | 66,178 | 153 | 0.235 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 563,409 | 5.634 | 20 | 200 | fits | 133,870 | 241 | 0.367 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 543,141 | 5.431 | 20 | 20 | fits | 133,870 | 241 | 0.367 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 389,067 | 3.891 | 20 | 24 | fits | 147,834 | 151 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 503,666 | 5.037 | 20 | 50 | fits | 133,870 | 241 | 0.367 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,000,997 | 10.010 | 20 | 20 | fits | 79,781 | 34 | 0.599 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 681,861 | 6.819 | 130 | 134 | fits | 29,630 | 52 | 0.512 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,519,394 | 15.194 | 130 | 134 | fits | 71,100 | 153 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,541,164 | 15.412 | 130 | 134 | fits | 71,100 | 153 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,561,224 | 15.612 | 130 | 134 | fits | 71,100 | 153 | 0.322 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,715,944 | 17.159 | 130 | 134 | fits | 64,835 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,736,356 | 17.364 | 130 | 134 | fits | 64,835 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,754,894 | 17.549 | 130 | 134 | fits | 64,835 | 152 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 1,924,972 | 19.250 | 130 | 134 | fits | 62,005 | 152 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 1,943,414 | 19.434 | 130 | 134 | fits | 62,005 | 152 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 1,960,304 | 19.603 | 130 | 134 | fits | 62,005 | 152 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,129,250 | 21.293 | 130 | 134 | fits | 46,161 | 103 | 0.272 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,149,565 | 21.496 | 130 | 134 | fits | 46,161 | 103 | 0.272 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 161,669 | 1.617 | 20 | 200 | fits | 151,883 | 272 | 0.360 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 455,234 | 4.552 | 20 | 20 | fits | 135,645 | 118 | 0.513 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 435,030 | 4.350 | 20 | 24 | fits | 135,645 | 118 | 0.513 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 415,759 | 4.158 | 20 | 50 | fits | 135,645 | 118 | 0.513 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 917,781 | 9.178 | 20 | 20 | fits | 79,979 | 34 | 0.601 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 919,139 | 9.191 | 130 | 134 | fits | 27,529 | 52 | 0.464 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,594,341 | 15.943 | 130 | 134 | fits | 64,222 | 152 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 239,875 | 2.399 | 130 | 134 | fits | 68,494 | 152 | 0.269 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 260,785 | 2.608 | 130 | 134 | fits | 68,494 | 152 | 0.269 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 279,582 | 2.796 | 130 | 134 | fits | 68,494 | 152 | 0.269 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 325,301 | 3.253 | 130 | 134 | fits | 86,153 | 170 | 0.339 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 344,923 | 3.449 | 130 | 134 | fits | 86,153 | 170 | 0.339 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 364,916 | 3.649 | 130 | 134 | fits | 86,153 | 170 | 0.339 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,613,052 | 16.131 | 130 | 134 | fits | 64,222 | 152 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,630,081 | 16.301 | 130 | 134 | fits | 64,222 | 152 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,730,631 | 17.306 | 130 | 134 | fits | 26,242 | 52 | 0.376 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 439,148 | 4.391 | 130 | 134 | fits | 28,339 | 53 | 0.383 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 146,615 | 1.466 | 20 | 200 | fits | 147,401 | 271 | 0.342 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 436,843 | 4.368 | 20 | 20 | fits | 128,437 | 123 | 0.523 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 416,639 | 4.166 | 20 | 24 | fits | 128,437 | 123 | 0.523 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 397,368 | 3.974 | 20 | 50 | fits | 128,437 | 123 | 0.523 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 893,541 | 8.935 | 20 | 20 | fits | 79,518 | 34 | 0.602 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

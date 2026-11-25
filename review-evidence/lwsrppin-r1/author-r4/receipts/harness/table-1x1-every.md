### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.acmp.if0` (notice-burst-3) | 4.564 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.adp.if0` (notice-burst-3) | 4.767 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-7.held.aecp.if0` (notice-every-7) | 4.095 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.maap.if0` (notice-burst-3) | 4.169 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-7.held.srp.if0` (notice-every-7) | 9.632 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-7.mrpdu.periodic.if0` (notice-every-7) | 1.039 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.36.0.if0` (notice-burst-6) | 21.416 (21.608) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 2101 | 0 | 153,939 (1.539) | fits |
| notice-every-1 | 2104 | 0 | 153,912 (1.539) | fits |
| notice-every-2 | 2103 | 0 | 153,750 (1.538) | fits |
| notice-every-3 | 2099 | 0 | 153,651 (1.537) | fits |
| notice-every-4 | 2094 | 0 | 154,051 (1.541) | fits |
| notice-every-5 | 2097 | 0 | 154,723 (1.547) | fits |
| notice-every-6 | 2090 | 0 | 154,051 (1.541) | fits |
| notice-every-7 | 2089 | 0 | 154,025 (1.540) | fits |
| notice-burst-0 | 1399 | 0 | 152,979 (1.530) | fits |
| notice-burst-1 | 1395 | 0 | 153,619 (1.536) | fits |
| notice-burst-2 | 1396 | 0 | 153,371 (1.534) | fits |
| notice-burst-3 | 1396 | 0 | 146,219 (1.462) | fits |
| notice-burst-4 | 1354 | 0 | 152,152 (1.522) | fits |
| notice-burst-5 | 1392 | 0 | 145,668 (1.457) | fits |
| notice-burst-6 | 1386 | 0 | 150,621 (1.506) | fits |
| notice-burst-7 | 1389 | 0 | 153,290 (1.533) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.006 | 130 | 16 | 2 | within |
| notice-every-0 | 8.183 | 130 | 16 | 2 | within |
| notice-every-0 | 1.875 | 130 | 16 | 2 | within |
| notice-every-0 | 2.053 | 130 | 16 | 2 | within |
| notice-every-0 | 3.861 | 130 | 16 | 2 | within |
| notice-every-0 | 4.043 | 130 | 16 | 2 | within |
| notice-every-0 | 5.975 | 130 | 16 | 2 | within |
| notice-every-0 | 6.151 | 130 | 16 | 2 | within |
| notice-every-0 | 8.316 | 130 | 16 | 2 | within |
| notice-every-0 | 9.889 | 130 | 16 | 2 | within |
| notice-every-0 | 2.230 | 130 | 16 | 2 | within |
| notice-every-0 | 4.221 | 130 | 16 | 2 | within |
| notice-every-1 | 2.228 | 130 | 16 | 2 | within |
| notice-every-1 | 2.409 | 130 | 16 | 2 | within |
| notice-every-1 | 4.163 | 130 | 16 | 2 | within |
| notice-every-1 | 4.339 | 130 | 16 | 2 | within |
| notice-every-1 | 6.131 | 130 | 16 | 2 | within |
| notice-every-1 | 6.307 | 130 | 16 | 2 | within |
| notice-every-1 | 8.115 | 130 | 16 | 2 | within |
| notice-every-1 | 8.289 | 130 | 16 | 2 | within |
| notice-every-1 | 2.549 | 130 | 16 | 2 | within |
| notice-every-1 | 4.472 | 130 | 16 | 2 | within |
| notice-every-1 | 6.480 | 130 | 16 | 2 | within |
| notice-every-1 | 8.456 | 130 | 16 | 2 | within |
| notice-every-2 | 4.185 | 130 | 16 | 2 | within |
| notice-every-2 | 4.363 | 130 | 16 | 2 | within |
| notice-every-2 | 6.162 | 130 | 16 | 2 | within |
| notice-every-2 | 6.340 | 130 | 16 | 2 | within |
| notice-every-2 | 8.108 | 130 | 16 | 2 | within |
| notice-every-2 | 8.283 | 130 | 16 | 2 | within |
| notice-every-2 | 2.187 | 130 | 16 | 2 | within |
| notice-every-2 | 2.372 | 130 | 16 | 2 | within |
| notice-every-2 | 4.500 | 130 | 16 | 2 | within |
| notice-every-2 | 6.471 | 130 | 16 | 2 | within |
| notice-every-2 | 2.549 | 130 | 16 | 2 | within |
| notice-every-2 | 8.453 | 130 | 16 | 2 | within |
| notice-every-3 | 3.947 | 130 | 16 | 2 | within |
| notice-every-3 | 4.126 | 130 | 16 | 2 | within |
| notice-every-3 | 5.927 | 130 | 16 | 2 | within |
| notice-every-3 | 6.103 | 130 | 16 | 2 | within |
| notice-every-3 | 8.038 | 130 | 16 | 2 | within |
| notice-every-3 | 8.214 | 130 | 16 | 2 | within |
| notice-every-3 | 1.953 | 130 | 16 | 2 | within |
| notice-every-3 | 2.136 | 130 | 16 | 2 | within |
| notice-every-3 | 4.264 | 130 | 16 | 2 | within |
| notice-every-3 | 6.233 | 130 | 16 | 2 | within |
| notice-every-3 | 2.312 | 130 | 16 | 2 | within |
| notice-every-3 | 8.385 | 130 | 16 | 2 | within |
| notice-every-4 | 6.065 | 130 | 16 | 2 | within |
| notice-every-4 | 6.242 | 130 | 16 | 2 | within |
| notice-every-4 | 8.041 | 130 | 16 | 2 | within |
| notice-every-4 | 8.219 | 130 | 16 | 2 | within |
| notice-every-4 | 1.958 | 130 | 16 | 2 | within |
| notice-every-4 | 2.141 | 130 | 16 | 2 | within |
| notice-every-4 | 3.944 | 130 | 16 | 2 | within |
| notice-every-4 | 4.126 | 130 | 16 | 2 | within |
| notice-every-4 | 6.376 | 130 | 16 | 2 | within |
| notice-every-4 | 8.348 | 130 | 16 | 2 | within |
| notice-every-4 | 2.318 | 130 | 16 | 2 | within |
| notice-every-4 | 4.303 | 130 | 16 | 2 | within |
| notice-every-5 | 6.028 | 130 | 16 | 2 | within |
| notice-every-5 | 6.205 | 130 | 16 | 2 | within |
| notice-every-5 | 7.978 | 130 | 16 | 2 | within |
| notice-every-5 | 8.156 | 130 | 16 | 2 | within |
| notice-every-5 | 1.955 | 130 | 16 | 2 | within |
| notice-every-5 | 2.138 | 130 | 16 | 2 | within |
| notice-every-5 | 3.944 | 130 | 16 | 2 | within |
| notice-every-5 | 4.126 | 130 | 16 | 2 | within |
| notice-every-5 | 6.339 | 130 | 16 | 2 | within |
| notice-every-5 | 8.285 | 130 | 16 | 2 | within |
| notice-every-5 | 2.316 | 130 | 16 | 2 | within |
| notice-every-5 | 4.303 | 130 | 16 | 2 | within |
| notice-every-6 | 6.065 | 130 | 16 | 2 | within |
| notice-every-6 | 6.242 | 130 | 16 | 2 | within |
| notice-every-6 | 8.041 | 130 | 16 | 2 | within |
| notice-every-6 | 8.219 | 130 | 16 | 2 | within |
| notice-every-6 | 1.955 | 130 | 16 | 2 | within |
| notice-every-6 | 2.138 | 130 | 16 | 2 | within |
| notice-every-6 | 3.944 | 130 | 16 | 2 | within |
| notice-every-6 | 4.126 | 130 | 16 | 2 | within |
| notice-every-6 | 6.376 | 130 | 16 | 2 | within |
| notice-every-6 | 8.348 | 130 | 16 | 2 | within |
| notice-every-6 | 2.316 | 130 | 16 | 2 | within |
| notice-every-6 | 4.303 | 130 | 16 | 2 | within |
| notice-every-7 | 7.981 | 130 | 16 | 2 | within |
| notice-every-7 | 8.158 | 130 | 16 | 2 | within |
| notice-every-7 | 2.011 | 130 | 16 | 2 | within |
| notice-every-7 | 2.189 | 130 | 16 | 2 | within |
| notice-every-7 | 3.997 | 130 | 16 | 2 | within |
| notice-every-7 | 4.179 | 130 | 16 | 2 | within |
| notice-every-7 | 6.110 | 130 | 16 | 2 | within |
| notice-every-7 | 6.287 | 130 | 16 | 2 | within |
| notice-every-7 | 8.291 | 130 | 16 | 2 | within |
| notice-every-7 | 9.875 | 130 | 16 | 2 | within |
| notice-every-7 | 2.366 | 130 | 16 | 2 | within |
| notice-every-7 | 4.357 | 130 | 16 | 2 | within |
| notice-burst-0 | 8.197 | 130 | 16 | 1 | within |
| notice-burst-0 | 14.758 | 130 | 16 | 1 | within |
| notice-burst-0 | 14.928 | 130 | 16 | 1 | within |
| notice-burst-0 | 15.098 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.082 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.258 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.152 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.335 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.395 | 130 | 16 | 1 | within |
| notice-burst-0 | 18.098 | 130 | 16 | 1 | within |
| notice-burst-0 | 18.273 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.102 | 130 | 16 | 1 | within |
| notice-burst-1 | 8.925 | 130 | 16 | 1 | within |
| notice-burst-1 | 13.778 | 130 | 16 | 1 | within |
| notice-burst-1 | 13.946 | 130 | 16 | 1 | within |
| notice-burst-1 | 14.115 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.101 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.277 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.236 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.419 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.414 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.117 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.292 | 130 | 16 | 1 | within |
| notice-burst-1 | 3.163 | 130 | 16 | 1 | within |
| notice-burst-2 | 8.213 | 130 | 16 | 2 | within |
| notice-burst-2 | 12.917 | 130 | 16 | 2 | within |
| notice-burst-2 | 13.084 | 130 | 16 | 2 | within |
| notice-burst-2 | 13.254 | 130 | 16 | 2 | within |
| notice-burst-2 | 14.108 | 130 | 16 | 2 | within |
| notice-burst-2 | 14.285 | 130 | 16 | 2 | within |
| notice-burst-2 | 2.187 | 130 | 16 | 2 | within |
| notice-burst-2 | 2.368 | 130 | 16 | 2 | within |
| notice-burst-2 | 14.421 | 130 | 16 | 2 | within |
| notice-burst-2 | 16.124 | 130 | 16 | 2 | within |
| notice-burst-2 | 16.299 | 130 | 16 | 2 | within |
| notice-burst-2 | 3.094 | 130 | 16 | 2 | within |
| notice-burst-3 | 8.500 | 130 | 16 | 1 | within |
| notice-burst-3 | 12.539 | 130 | 16 | 1 | within |
| notice-burst-3 | 12.709 | 130 | 16 | 1 | within |
| notice-burst-3 | 12.878 | 130 | 16 | 1 | within |
| notice-burst-3 | 14.121 | 130 | 16 | 1 | within |
| notice-burst-3 | 14.298 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.158 | 130 | 16 | 1 | within |
| notice-burst-3 | 2.339 | 130 | 16 | 1 | within |
| notice-burst-3 | 14.434 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.135 | 130 | 16 | 1 | within |
| notice-burst-3 | 16.309 | 130 | 16 | 1 | within |
| notice-burst-3 | 5.544 | 130 | 16 | 1 | within |
| notice-burst-4 | 4.965 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.142 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.291 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.517 | 130 | 16 | 0 | within |
| notice-burst-4 | 15.304 | 130 | 16 | 0 | within |
| notice-burst-4 | 15.484 | 130 | 16 | 0 | within |
| notice-burst-4 | 15.635 | 130 | 16 | 0 | within |
| notice-burst-4 | 17.023 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.655 | 130 | 16 | 0 | within |
| notice-burst-4 | 5.779 | 130 | 16 | 0 | within |
| notice-burst-4 | 17.193 | 130 | 16 | 0 | within |
| notice-burst-4 | 17.359 | 130 | 16 | 0 | within |
| notice-burst-5 | 7.548 | 130 | 16 | 1 | within |
| notice-burst-5 | 15.733 | 130 | 16 | 1 | within |
| notice-burst-5 | 15.901 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.070 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.194 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.370 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.520 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.159 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.298 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.417 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.157 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.326 | 130 | 16 | 1 | within |
| notice-burst-6 | 7.683 | 130 | 16 | 1 | within |
| notice-burst-6 | 15.824 | 130 | 16 | 1 | within |
| notice-burst-6 | 15.992 | 130 | 16 | 1 | within |
| notice-burst-6 | 16.160 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.154 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.330 | 130 | 16 | 1 | within |
| notice-burst-6 | 17.480 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.249 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.389 | 130 | 16 | 1 | within |
| notice-burst-6 | 19.507 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.247 | 130 | 16 | 1 | within |
| notice-burst-6 | 21.416 | 130 | 16 | 1 | within |
| notice-burst-7 | 8.951 | 130 | 16 | 0 | within |
| notice-burst-7 | 15.595 | 130 | 16 | 0 | within |
| notice-burst-7 | 15.765 | 130 | 16 | 0 | within |
| notice-burst-7 | 15.935 | 130 | 16 | 0 | within |
| notice-burst-7 | 17.049 | 130 | 16 | 0 | within |
| notice-burst-7 | 17.225 | 130 | 16 | 0 | within |
| notice-burst-7 | 1.993 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.175 | 130 | 16 | 0 | within |
| notice-burst-7 | 17.363 | 130 | 16 | 0 | within |
| notice-burst-7 | 18.936 | 130 | 16 | 0 | within |
| notice-burst-7 | 19.111 | 130 | 16 | 0 | within |
| notice-burst-7 | 3.057 | 130 | 16 | 0 | within |

Latest: 21.416 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 403 | 93,056 (0.931) | 77,938 (0.779) |
| notice-every-1 | 403 | 93,056 (0.931) | 77,938 (0.779) |
| notice-every-2 | 403 | 93,056 (0.931) | 77,938 (0.779) |
| notice-every-3 | 403 | 93,056 (0.931) | 77,938 (0.779) |
| notice-every-4 | 403 | 93,056 (0.931) | 77,938 (0.779) |
| notice-every-5 | 403 | 93,056 (0.931) | 77,938 (0.779) |
| notice-every-6 | 403 | 93,056 (0.931) | 77,938 (0.779) |
| notice-every-7 | 403 | 93,056 (0.931) | 77,938 (0.779) |
| notice-burst-0 | 413 | 93,056 (0.931) | 77,938 (0.779) |
| notice-burst-1 | 413 | 93,056 (0.931) | 77,938 (0.779) |
| notice-burst-2 | 413 | 93,056 (0.931) | 77,938 (0.779) |
| notice-burst-3 | 413 | 93,056 (0.931) | 77,938 (0.779) |
| notice-burst-4 | 413 | 93,056 (0.931) | 77,938 (0.779) |
| notice-burst-5 | 413 | 93,056 (0.931) | 77,938 (0.779) |
| notice-burst-6 | 413 | 93,056 (0.931) | 77,938 (0.779) |
| notice-burst-7 | 413 | 93,056 (0.931) | 77,938 (0.779) |

Longest pass that carries a step: 93,056 CPU cycles (0.931 ms), notice-every-0; longest step: 77,938 (0.779 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 800,623 | 8.006 | 130 | 134 | fits | 54,710 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 818,280 | 8.183 | 130 | 134 | fits | 54,710 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 187,458 | 1.875 | 130 | 134 | fits | 60,792 | 155 | 0.201 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 205,335 | 2.053 | 130 | 134 | fits | 60,792 | 155 | 0.201 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 386,069 | 3.861 | 130 | 134 | fits | 60,653 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 404,303 | 4.043 | 130 | 134 | fits | 60,653 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 597,453 | 5.975 | 130 | 134 | fits | 41,083 | 103 | 0.253 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 615,139 | 6.151 | 130 | 134 | fits | 41,083 | 103 | 0.253 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 831,605 | 8.316 | 130 | 134 | fits | 54,710 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 988,882 | 9.889 | 130 | 134 | fits | 19,003 | 51 | 0.350 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 222,997 | 2.230 | 130 | 134 | fits | 60,792 | 155 | 0.201 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 422,085 | 4.221 | 130 | 134 | fits | 60,653 | 155 | 0.197 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 166,015 | 1.660 | 20 | 200 | fits | 149,553 | 292 | 0.213 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 395,312 | 3.953 | 20 | 20 | fits | 106,356 | 84 | 0.469 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 375,108 | 3.751 | 20 | 24 | fits | 106,356 | 84 | 0.469 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 106,272 | 1.063 | 20 | 50 | fits | 149,553 | 292 | 0.213 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 933,531 | 9.335 | 20 | 20 | fits | 60,082 | 33 | 0.783 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 100,516 | 1.005 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 222,815 | 2.228 | 130 | 134 | fits | 58,022 | 153 | 0.267 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 240,909 | 2.409 | 130 | 134 | fits | 58,022 | 153 | 0.267 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 416,332 | 4.163 | 130 | 134 | fits | 55,048 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 433,931 | 4.339 | 130 | 134 | fits | 55,048 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 613,060 | 6.131 | 130 | 134 | fits | 58,399 | 153 | 0.190 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 630,697 | 6.307 | 130 | 134 | fits | 58,399 | 153 | 0.190 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 811,530 | 8.115 | 130 | 134 | fits | 56,446 | 153 | 0.184 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 828,864 | 8.289 | 130 | 134 | fits | 56,446 | 153 | 0.184 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 254,873 | 2.549 | 130 | 134 | fits | 58,022 | 153 | 0.267 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 447,198 | 4.472 | 130 | 134 | fits | 55,048 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 648,011 | 6.480 | 130 | 134 | fits | 58,399 | 153 | 0.190 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 845,591 | 8.456 | 130 | 134 | fits | 56,446 | 153 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 164,756 | 1.648 | 20 | 200 | fits | 148,869 | 293 | 0.222 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 406,163 | 4.062 | 20 | 20 | fits | 105,988 | 84 | 0.468 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 385,959 | 3.860 | 20 | 24 | fits | 105,988 | 84 | 0.468 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 105,013 | 1.050 | 20 | 50 | fits | 148,869 | 293 | 0.222 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 928,330 | 9.283 | 20 | 20 | fits | 44,888 | 29 | 0.750 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 75,582 | 0.756 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 418,511 | 4.185 | 130 | 134 | fits | 56,597 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 436,302 | 4.363 | 130 | 134 | fits | 56,597 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 616,167 | 6.162 | 130 | 134 | fits | 54,629 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 633,962 | 6.340 | 130 | 134 | fits | 54,629 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 810,816 | 8.108 | 130 | 134 | fits | 57,208 | 155 | 0.185 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 828,290 | 8.283 | 130 | 134 | fits | 57,208 | 155 | 0.185 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 218,722 | 2.187 | 130 | 134 | fits | 61,920 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 237,232 | 2.372 | 130 | 134 | fits | 61,920 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 450,009 | 4.500 | 130 | 134 | fits | 56,597 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 647,076 | 6.471 | 130 | 134 | fits | 54,629 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 254,908 | 2.549 | 130 | 134 | fits | 61,920 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 845,300 | 8.453 | 130 | 134 | fits | 57,208 | 155 | 0.185 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 126,705 | 1.267 | 20 | 200 | fits | 121,397 | 160 | 0.161 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 423,935 | 4.239 | 20 | 20 | fits | 125,660 | 128 | 0.471 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 403,731 | 4.037 | 20 | 24 | fits | 125,660 | 128 | 0.471 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 384,460 | 3.845 | 20 | 50 | fits | 125,660 | 128 | 0.471 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 954,691 | 9.547 | 20 | 20 | fits | 61,129 | 39 | 0.768 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 91,013 | 0.910 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 394,661 | 3.947 | 130 | 134 | fits | 57,063 | 155 | 0.245 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 412,615 | 4.126 | 130 | 134 | fits | 57,063 | 155 | 0.245 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 592,670 | 5.927 | 130 | 134 | fits | 54,385 | 153 | 0.228 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 610,269 | 6.103 | 130 | 134 | fits | 54,385 | 153 | 0.228 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 803,776 | 8.038 | 130 | 134 | fits | 57,541 | 153 | 0.189 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 821,413 | 8.214 | 130 | 134 | fits | 57,541 | 153 | 0.189 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 195,290 | 1.953 | 130 | 134 | fits | 60,776 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 213,559 | 2.136 | 130 | 134 | fits | 60,776 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 426,402 | 4.264 | 130 | 134 | fits | 57,063 | 155 | 0.245 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 623,303 | 6.233 | 130 | 134 | fits | 54,385 | 153 | 0.228 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 231,156 | 2.312 | 130 | 134 | fits | 60,776 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 838,502 | 8.385 | 130 | 134 | fits | 57,541 | 153 | 0.189 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 174,418 | 1.744 | 20 | 200 | fits | 150,880 | 301 | 0.226 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 422,202 | 4.222 | 20 | 20 | fits | 110,062 | 97 | 0.479 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 401,998 | 4.020 | 20 | 24 | fits | 110,062 | 97 | 0.479 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 114,675 | 1.147 | 20 | 50 | fits | 150,880 | 301 | 0.226 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 957,178 | 9.572 | 20 | 20 | fits | 60,422 | 33 | 0.780 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 93,397 | 0.934 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 606,533 | 6.065 | 130 | 134 | fits | 55,294 | 153 | 0.232 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 624,151 | 6.242 | 130 | 134 | fits | 55,294 | 153 | 0.232 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 804,102 | 8.041 | 130 | 134 | fits | 53,973 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 821,897 | 8.219 | 130 | 134 | fits | 53,973 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 195,755 | 1.958 | 130 | 134 | fits | 60,988 | 153 | 0.189 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 214,081 | 2.141 | 130 | 134 | fits | 60,988 | 153 | 0.189 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 394,388 | 3.944 | 130 | 134 | fits | 60,304 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 412,630 | 4.126 | 130 | 134 | fits | 60,304 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 637,573 | 6.376 | 130 | 134 | fits | 55,294 | 153 | 0.232 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 834,830 | 8.348 | 130 | 134 | fits | 53,973 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 231,822 | 2.318 | 130 | 134 | fits | 60,988 | 153 | 0.189 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 430,268 | 4.303 | 130 | 134 | fits | 60,304 | 155 | 0.194 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 176,533 | 1.765 | 20 | 200 | fits | 150,076 | 299 | 0.222 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 429,303 | 4.293 | 20 | 20 | fits | 110,512 | 99 | 0.480 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 409,099 | 4.091 | 20 | 24 | fits | 110,512 | 99 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 116,790 | 1.168 | 20 | 50 | fits | 150,076 | 299 | 0.222 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 955,812 | 9.558 | 20 | 20 | fits | 60,025 | 33 | 0.782 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 97,858 | 0.979 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 602,843 | 6.028 | 130 | 134 | fits | 55,294 | 153 | 0.232 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 620,461 | 6.205 | 130 | 134 | fits | 55,294 | 153 | 0.232 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 797,812 | 7.978 | 130 | 134 | fits | 53,964 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 815,607 | 8.156 | 130 | 134 | fits | 53,964 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 195,523 | 1.955 | 130 | 134 | fits | 60,979 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 213,849 | 2.138 | 130 | 134 | fits | 60,979 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 394,393 | 3.944 | 130 | 134 | fits | 60,427 | 155 | 0.195 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 412,635 | 4.126 | 130 | 134 | fits | 60,427 | 155 | 0.195 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 633,883 | 6.339 | 130 | 134 | fits | 55,294 | 153 | 0.232 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 828,540 | 8.285 | 130 | 134 | fits | 53,964 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 231,590 | 2.316 | 130 | 134 | fits | 60,979 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 430,273 | 4.303 | 130 | 134 | fits | 60,427 | 155 | 0.195 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 164,204 | 1.642 | 20 | 200 | fits | 150,224 | 293 | 0.218 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 427,509 | 4.275 | 20 | 20 | fits | 99,086 | 96 | 0.494 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 407,305 | 4.073 | 20 | 24 | fits | 99,086 | 96 | 0.494 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 104,461 | 1.045 | 20 | 50 | fits | 150,224 | 293 | 0.218 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 953,963 | 9.540 | 20 | 20 | fits | 60,025 | 33 | 0.782 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 96,017 | 0.960 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 606,543 | 6.065 | 130 | 134 | fits | 55,294 | 153 | 0.232 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 624,161 | 6.242 | 130 | 134 | fits | 55,294 | 153 | 0.232 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 804,099 | 8.041 | 130 | 134 | fits | 53,973 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 821,894 | 8.219 | 130 | 134 | fits | 53,973 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 195,523 | 1.955 | 130 | 134 | fits | 60,979 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 213,849 | 2.138 | 130 | 134 | fits | 60,979 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 394,380 | 3.944 | 130 | 134 | fits | 60,427 | 155 | 0.195 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 412,622 | 4.126 | 130 | 134 | fits | 60,427 | 155 | 0.195 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 637,583 | 6.376 | 130 | 134 | fits | 55,294 | 153 | 0.232 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 834,827 | 8.348 | 130 | 134 | fits | 53,973 | 151 | 0.232 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 231,590 | 2.316 | 130 | 134 | fits | 60,979 | 155 | 0.188 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 430,260 | 4.303 | 130 | 134 | fits | 60,427 | 155 | 0.195 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 166,235 | 1.662 | 20 | 200 | fits | 150,674 | 302 | 0.222 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 419,741 | 4.197 | 20 | 20 | fits | 110,385 | 99 | 0.480 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 399,537 | 3.995 | 20 | 24 | fits | 110,385 | 99 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 106,492 | 1.065 | 20 | 50 | fits | 150,674 | 302 | 0.222 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 946,456 | 9.465 | 20 | 20 | fits | 60,025 | 33 | 0.782 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 90,793 | 0.908 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 798,146 | 7.981 | 130 | 134 | fits | 54,710 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 815,803 | 8.158 | 130 | 134 | fits | 54,710 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 201,056 | 2.011 | 130 | 134 | fits | 60,802 | 153 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 218,934 | 2.189 | 130 | 134 | fits | 60,802 | 153 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 399,662 | 3.997 | 130 | 134 | fits | 60,539 | 153 | 0.196 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 417,896 | 4.179 | 130 | 134 | fits | 60,539 | 153 | 0.196 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 610,983 | 6.110 | 130 | 134 | fits | 41,083 | 103 | 0.253 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 628,669 | 6.287 | 130 | 134 | fits | 41,083 | 103 | 0.253 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 829,128 | 8.291 | 130 | 134 | fits | 54,710 | 152 | 0.235 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 987,526 | 9.875 | 130 | 134 | fits | 18,895 | 51 | 0.343 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 236,596 | 2.366 | 130 | 134 | fits | 60,802 | 153 | 0.203 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 435,678 | 4.357 | 130 | 134 | fits | 60,539 | 153 | 0.196 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 148,726 | 1.487 | 20 | 200 | fits | 145,354 | 275 | 0.231 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 429,730 | 4.297 | 20 | 20 | fits | 124,081 | 122 | 0.472 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 409,526 | 4.095 | 20 | 24 | fits | 124,081 | 122 | 0.472 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 390,255 | 3.903 | 20 | 50 | fits | 124,081 | 122 | 0.472 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 963,237 | 9.632 | 20 | 20 | fits | 59,753 | 33 | 0.780 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 103,879 | 1.039 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 819,673 | 8.197 | 130 | 134 | fits | 25,461 | 52 | 0.478 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,475,750 | 14.758 | 130 | 134 | fits | 59,887 | 153 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,492,750 | 14.928 | 130 | 134 | fits | 59,887 | 153 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,509,785 | 15.098 | 130 | 134 | fits | 59,887 | 153 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 1,608,237 | 16.082 | 130 | 134 | fits | 53,966 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 1,625,834 | 16.258 | 130 | 134 | fits | 53,966 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 215,225 | 2.152 | 130 | 134 | fits | 54,183 | 111 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 233,468 | 2.335 | 130 | 134 | fits | 54,183 | 111 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,639,548 | 16.395 | 130 | 134 | fits | 53,966 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,809,784 | 18.098 | 130 | 134 | fits | 36,391 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,827,256 | 18.273 | 130 | 134 | fits | 36,391 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 310,161 | 3.102 | 130 | 134 | fits | 37,474 | 62 | 0.268 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 156,042 | 1.560 | 20 | 200 | fits | 144,826 | 269 | 0.219 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 416,486 | 4.165 | 20 | 20 | fits | 102,272 | 109 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 396,282 | 3.963 | 20 | 24 | fits | 102,272 | 109 | 0.509 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 377,011 | 3.770 | 20 | 50 | fits | 102,272 | 109 | 0.509 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 882,512 | 8.825 | 20 | 20 | fits | 54,241 | 26 | 0.749 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 892,530 | 8.925 | 130 | 134 | fits | 26,071 | 52 | 0.498 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,377,817 | 13.778 | 130 | 134 | fits | 59,251 | 153 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,394,556 | 13.946 | 130 | 134 | fits | 59,251 | 153 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,411,521 | 14.115 | 130 | 134 | fits | 59,251 | 153 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 1,510,053 | 15.101 | 130 | 134 | fits | 53,909 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 1,527,723 | 15.277 | 130 | 134 | fits | 53,909 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 223,560 | 2.236 | 130 | 134 | fits | 43,306 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 241,873 | 2.419 | 130 | 134 | fits | 43,306 | 102 | 0.263 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,541,364 | 15.414 | 130 | 134 | fits | 53,909 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,711,739 | 17.117 | 130 | 134 | fits | 36,430 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,729,177 | 17.292 | 130 | 134 | fits | 36,430 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 316,329 | 3.163 | 130 | 134 | fits | 36,508 | 62 | 0.221 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 34,679 | 0.347 | 20 | 200 | fits | 32,934 | 60 | 0.077 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 379,526 | 3.795 | 20 | 20 | fits | 103,102 | 99 | 0.461 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 359,322 | 3.593 | 20 | 24 | fits | 103,102 | 99 | 0.461 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 340,051 | 3.401 | 20 | 50 | fits | 103,102 | 99 | 0.461 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 886,471 | 8.865 | 20 | 20 | fits | 54,262 | 26 | 0.749 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 821,346 | 8.213 | 130 | 134 | fits | 26,088 | 52 | 0.498 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,291,678 | 12.917 | 130 | 134 | fits | 59,242 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,308,418 | 13.084 | 130 | 134 | fits | 59,242 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,325,383 | 13.254 | 130 | 134 | fits | 59,242 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 1,410,786 | 14.108 | 130 | 134 | fits | 53,883 | 152 | 0.225 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 1,428,456 | 14.285 | 130 | 134 | fits | 53,883 | 152 | 0.225 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 218,671 | 2.187 | 130 | 134 | fits | 54,095 | 111 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 236,811 | 2.368 | 130 | 134 | fits | 54,095 | 111 | 0.243 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,442,097 | 14.421 | 130 | 134 | fits | 53,883 | 152 | 0.225 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,612,434 | 16.124 | 130 | 134 | fits | 36,430 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,629,872 | 16.299 | 130 | 134 | fits | 36,430 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 309,380 | 3.094 | 130 | 134 | fits | 36,845 | 62 | 0.248 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 174,362 | 1.744 | 20 | 200 | fits | 150,368 | 292 | 0.240 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 397,853 | 3.979 | 20 | 20 | fits | 90,388 | 70 | 0.479 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 377,649 | 3.776 | 20 | 24 | fits | 90,388 | 70 | 0.479 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 114,619 | 1.146 | 20 | 50 | fits | 150,368 | 292 | 0.240 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 897,419 | 8.974 | 20 | 20 | fits | 42,465 | 22 | 0.765 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 850,013 | 8.500 | 130 | 134 | fits | 26,019 | 52 | 0.496 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,253,926 | 12.539 | 130 | 134 | fits | 59,360 | 153 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,270,880 | 12.709 | 130 | 134 | fits | 59,360 | 153 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,287,845 | 12.878 | 130 | 134 | fits | 59,360 | 153 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,412,109 | 14.121 | 130 | 134 | fits | 53,992 | 152 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,429,779 | 14.298 | 130 | 134 | fits | 53,992 | 152 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 215,752 | 2.158 | 130 | 134 | fits | 53,800 | 111 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 233,892 | 2.339 | 130 | 134 | fits | 53,800 | 111 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,443,420 | 14.434 | 130 | 134 | fits | 53,992 | 152 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,613,455 | 16.135 | 130 | 134 | fits | 36,391 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,630,854 | 16.309 | 130 | 134 | fits | 36,391 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 554,408 | 5.544 | 130 | 134 | fits | 26,765 | 52 | 0.366 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 476,658 | 4.767 | 20 | 200 | fits | 110,801 | 186 | 0.277 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 456,390 | 4.564 | 20 | 20 | fits | 110,801 | 186 | 0.277 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 298,620 | 2.986 | 20 | 24 | fits | 146,219 | 195 | 0.386 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 416,915 | 4.169 | 20 | 50 | fits | 110,801 | 186 | 0.277 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 958,041 | 9.580 | 20 | 20 | fits | 54,380 | 26 | 0.750 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 496,484 | 4.965 | 130 | 134 | fits | 68,374 | 161 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 514,159 | 5.142 | 130 | 134 | fits | 68,374 | 161 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 529,108 | 5.291 | 130 | 134 | fits | 68,374 | 161 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 551,721 | 5.517 | 130 | 134 | fits | 48,148 | 152 | 0.114 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,530,378 | 15.304 | 130 | 134 | fits | 57,948 | 153 | 0.274 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,548,381 | 15.484 | 130 | 134 | fits | 57,948 | 153 | 0.274 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,563,515 | 15.635 | 130 | 134 | fits | 57,948 | 153 | 0.274 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,702,308 | 17.023 | 130 | 134 | fits | 56,837 | 153 | 0.124 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 565,536 | 5.655 | 130 | 134 | fits | 48,148 | 152 | 0.114 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 577,899 | 5.779 | 130 | 134 | fits | 48,148 | 152 | 0.114 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,719,288 | 17.193 | 130 | 134 | fits | 56,837 | 153 | 0.124 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,735,945 | 17.359 | 130 | 134 | fits | 56,837 | 153 | 0.124 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 156,711 | 1.567 | 20 | 200 | fits | 152,152 | 283 | 0.248 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 386,341 | 3.863 | 20 | 20 | fits | 97,807 | 98 | 0.480 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 366,137 | 3.661 | 20 | 24 | fits | 97,807 | 98 | 0.480 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 346,866 | 3.469 | 20 | 50 | fits | 97,807 | 98 | 0.480 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 850,388 | 8.504 | 20 | 20 | fits | 30,524 | 18 | 0.786 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 754,786 | 7.548 | 130 | 134 | fits | 26,365 | 52 | 0.504 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,573,291 | 15.733 | 130 | 134 | fits | 59,834 | 153 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,590,132 | 15.901 | 130 | 134 | fits | 59,834 | 153 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,606,990 | 16.070 | 130 | 134 | fits | 59,834 | 153 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,719,419 | 17.194 | 130 | 134 | fits | 55,503 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,737,016 | 17.370 | 130 | 134 | fits | 55,503 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,752,039 | 17.520 | 130 | 134 | fits | 55,503 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,915,866 | 19.159 | 130 | 134 | fits | 49,390 | 152 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 1,929,848 | 19.298 | 130 | 134 | fits | 49,390 | 152 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 1,941,719 | 19.417 | 130 | 134 | fits | 49,390 | 152 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,115,671 | 21.157 | 130 | 134 | fits | 39,945 | 103 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,132,593 | 21.326 | 130 | 134 | fits | 39,945 | 103 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 40,270 | 0.403 | 20 | 200 | fits | 32,937 | 60 | 0.077 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 413,215 | 4.132 | 20 | 20 | fits | 118,077 | 116 | 0.462 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 393,011 | 3.930 | 20 | 24 | fits | 118,077 | 116 | 0.462 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 373,740 | 3.737 | 20 | 50 | fits | 118,077 | 116 | 0.462 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 879,958 | 8.800 | 20 | 20 | fits | 54,438 | 26 | 0.749 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 768,313 | 7.683 | 130 | 134 | fits | 26,255 | 52 | 0.498 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,582,351 | 15.824 | 130 | 134 | fits | 59,834 | 153 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,599,192 | 15.992 | 130 | 134 | fits | 59,834 | 153 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,616,050 | 16.160 | 130 | 134 | fits | 59,834 | 153 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,715,355 | 17.154 | 130 | 134 | fits | 55,503 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,732,952 | 17.330 | 130 | 134 | fits | 55,503 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,747,975 | 17.480 | 130 | 134 | fits | 55,503 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 1,924,883 | 19.249 | 130 | 134 | fits | 49,390 | 152 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 1,938,865 | 19.389 | 130 | 134 | fits | 49,390 | 152 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 1,950,736 | 19.507 | 130 | 134 | fits | 49,390 | 152 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,124,688 | 21.247 | 130 | 134 | fits | 39,945 | 103 | 0.161 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,141,610 | 21.416 | 130 | 134 | fits | 39,945 | 103 | 0.161 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 152,229 | 1.522 | 20 | 200 | fits | 150,621 | 282 | 0.206 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 417,368 | 4.174 | 20 | 20 | fits | 113,268 | 115 | 0.474 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 397,164 | 3.972 | 20 | 24 | fits | 113,268 | 115 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 377,893 | 3.779 | 20 | 50 | fits | 113,268 | 115 | 0.474 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 884,252 | 8.843 | 20 | 20 | fits | 54,420 | 26 | 0.749 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 895,065 | 8.951 | 130 | 134 | fits | 25,313 | 52 | 0.474 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,559,478 | 15.595 | 130 | 134 | fits | 59,864 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,576,455 | 15.765 | 130 | 134 | fits | 59,864 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,593,490 | 15.935 | 130 | 134 | fits | 59,864 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 1,704,939 | 17.049 | 130 | 134 | fits | 53,966 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 1,722,536 | 17.225 | 130 | 134 | fits | 53,966 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 199,333 | 1.993 | 130 | 134 | fits | 54,149 | 111 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 217,473 | 2.175 | 130 | 134 | fits | 54,149 | 111 | 0.245 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,736,250 | 17.363 | 130 | 134 | fits | 53,966 | 152 | 0.227 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,893,581 | 18.936 | 130 | 134 | fits | 36,391 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,911,053 | 19.111 | 130 | 134 | fits | 36,391 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 305,722 | 3.057 | 130 | 134 | fits | 36,865 | 62 | 0.248 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 38,663 | 0.387 | 20 | 200 | fits | 32,940 | 60 | 0.077 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 413,085 | 4.131 | 20 | 20 | fits | 111,938 | 123 | 0.494 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 392,881 | 3.929 | 20 | 24 | fits | 111,938 | 123 | 0.494 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 373,610 | 3.736 | 20 | 50 | fits | 111,938 | 123 | 0.494 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 877,781 | 8.778 | 20 | 20 | fits | 42,565 | 22 | 0.766 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

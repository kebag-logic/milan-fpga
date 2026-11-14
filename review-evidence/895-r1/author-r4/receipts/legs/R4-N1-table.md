### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.acmp.if0` (notice-burst-3) | 4.754 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.adp.if0` (notice-burst-3) | 4.957 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-3.held.aecp.if0` (notice-every-3) | 4.283 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.maap.if0` (notice-burst-3) | 4.360 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-3.held.srp.if0` (notice-every-3) | 11.098 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-3.mrpdu.periodic.if0` (notice-every-3) | 0.969 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 26.088 (26.314) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1549 | 0 | 154,830 (1.548) | fits |
| notice-every-1 | 1556 | 0 | 154,765 (1.548) | fits |
| notice-every-2 | 1549 | 0 | 154,810 (1.548) | fits |
| notice-every-3 | 1541 | 0 | 154,627 (1.546) | fits |
| notice-every-4 | 1536 | 0 | 154,808 (1.548) | fits |
| notice-every-5 | 1546 | 0 | 154,890 (1.549) | fits |
| notice-every-6 | 1547 | 0 | 154,723 (1.547) | fits |
| notice-every-7 | 1540 | 0 | 154,890 (1.549) | fits |
| notice-burst-0 | 1073 | 0 | 154,601 (1.546) | fits |
| notice-burst-1 | 1065 | 0 | 154,514 (1.545) | fits |
| notice-burst-2 | 1103 | 0 | 154,510 (1.545) | fits |
| notice-burst-3 | 1088 | 0 | 154,676 (1.547) | fits |
| notice-burst-4 | 1026 | 0 | 154,862 (1.549) | fits |
| notice-burst-5 | 1059 | 0 | 154,823 (1.548) | fits |
| notice-burst-6 | 1055 | 0 | 154,987 (1.550) | fits |
| notice-burst-7 | 1070 | 0 | 154,601 (1.546) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.169 | 130 | 16 | 2 | within |
| notice-every-0 | 8.367 | 130 | 16 | 2 | within |
| notice-every-0 | 2.045 | 130 | 16 | 2 | within |
| notice-every-0 | 2.250 | 130 | 16 | 2 | within |
| notice-every-0 | 3.967 | 130 | 16 | 2 | within |
| notice-every-0 | 4.167 | 130 | 16 | 2 | within |
| notice-every-0 | 5.968 | 130 | 16 | 2 | within |
| notice-every-0 | 6.168 | 130 | 16 | 2 | within |
| notice-every-0 | 10.090 | 130 | 16 | 2 | within |
| notice-every-0 | 10.257 | 130 | 16 | 2 | within |
| notice-every-0 | 11.989 | 130 | 16 | 2 | within |
| notice-every-0 | 12.184 | 130 | 16 | 2 | within |
| notice-every-1 | 4.106 | 130 | 16 | 2 | within |
| notice-every-1 | 4.302 | 130 | 16 | 2 | within |
| notice-every-1 | 6.261 | 130 | 16 | 2 | within |
| notice-every-1 | 6.464 | 130 | 16 | 2 | within |
| notice-every-1 | 8.257 | 130 | 16 | 2 | within |
| notice-every-1 | 8.452 | 130 | 16 | 2 | within |
| notice-every-1 | 2.087 | 130 | 16 | 2 | within |
| notice-every-1 | 2.295 | 130 | 16 | 2 | within |
| notice-every-1 | 10.173 | 130 | 16 | 2 | within |
| notice-every-1 | 10.340 | 130 | 16 | 2 | within |
| notice-every-1 | 12.072 | 130 | 16 | 2 | within |
| notice-every-1 | 12.267 | 130 | 16 | 2 | within |
| notice-every-2 | 2.040 | 130 | 16 | 2 | within |
| notice-every-2 | 2.239 | 130 | 16 | 2 | within |
| notice-every-2 | 3.942 | 130 | 16 | 2 | within |
| notice-every-2 | 4.144 | 130 | 16 | 2 | within |
| notice-every-2 | 5.939 | 130 | 16 | 2 | within |
| notice-every-2 | 6.135 | 130 | 16 | 2 | within |
| notice-every-2 | 7.900 | 130 | 16 | 2 | within |
| notice-every-2 | 8.094 | 130 | 16 | 2 | within |
| notice-every-2 | 9.834 | 130 | 16 | 2 | within |
| notice-every-2 | 10.001 | 130 | 16 | 2 | within |
| notice-every-2 | 11.912 | 130 | 16 | 2 | within |
| notice-every-2 | 12.107 | 130 | 16 | 2 | within |
| notice-every-3 | 3.924 | 130 | 16 | 2 | within |
| notice-every-3 | 4.122 | 130 | 16 | 2 | within |
| notice-every-3 | 5.931 | 130 | 16 | 2 | within |
| notice-every-3 | 6.133 | 130 | 16 | 2 | within |
| notice-every-3 | 7.899 | 130 | 16 | 2 | within |
| notice-every-3 | 8.094 | 130 | 16 | 2 | within |
| notice-every-3 | 1.995 | 130 | 16 | 2 | within |
| notice-every-3 | 2.202 | 130 | 16 | 2 | within |
| notice-every-3 | 10.012 | 130 | 16 | 2 | within |
| notice-every-3 | 10.179 | 130 | 16 | 2 | within |
| notice-every-3 | 11.913 | 130 | 16 | 2 | within |
| notice-every-3 | 12.108 | 130 | 16 | 2 | within |
| notice-every-4 | 3.921 | 130 | 16 | 2 | within |
| notice-every-4 | 4.119 | 130 | 16 | 2 | within |
| notice-every-4 | 5.928 | 130 | 16 | 2 | within |
| notice-every-4 | 6.129 | 130 | 16 | 2 | within |
| notice-every-4 | 7.896 | 130 | 16 | 2 | within |
| notice-every-4 | 8.091 | 130 | 16 | 2 | within |
| notice-every-4 | 1.996 | 130 | 16 | 2 | within |
| notice-every-4 | 2.202 | 130 | 16 | 2 | within |
| notice-every-4 | 9.831 | 130 | 16 | 2 | within |
| notice-every-4 | 9.999 | 130 | 16 | 2 | within |
| notice-every-4 | 11.910 | 130 | 16 | 2 | within |
| notice-every-4 | 12.105 | 130 | 16 | 2 | within |
| notice-every-5 | 8.221 | 130 | 16 | 2 | within |
| notice-every-5 | 8.419 | 130 | 16 | 2 | within |
| notice-every-5 | 2.322 | 130 | 16 | 2 | within |
| notice-every-5 | 2.529 | 130 | 16 | 2 | within |
| notice-every-5 | 5.172 | 130 | 16 | 2 | within |
| notice-every-5 | 5.373 | 130 | 16 | 2 | within |
| notice-every-5 | 6.239 | 130 | 16 | 2 | within |
| notice-every-5 | 6.440 | 130 | 16 | 2 | within |
| notice-every-5 | 10.160 | 130 | 16 | 2 | within |
| notice-every-5 | 10.327 | 130 | 16 | 2 | within |
| notice-every-5 | 12.239 | 130 | 16 | 2 | within |
| notice-every-5 | 12.434 | 130 | 16 | 2 | within |
| notice-every-6 | 8.233 | 130 | 16 | 2 | within |
| notice-every-6 | 8.431 | 130 | 16 | 2 | within |
| notice-every-6 | 2.135 | 130 | 16 | 2 | within |
| notice-every-6 | 2.343 | 130 | 16 | 2 | within |
| notice-every-6 | 4.143 | 130 | 16 | 2 | within |
| notice-every-6 | 4.341 | 130 | 16 | 2 | within |
| notice-every-6 | 6.248 | 130 | 16 | 2 | within |
| notice-every-6 | 6.450 | 130 | 16 | 2 | within |
| notice-every-6 | 10.167 | 130 | 16 | 2 | within |
| notice-every-6 | 10.335 | 130 | 16 | 2 | within |
| notice-every-6 | 12.245 | 130 | 16 | 2 | within |
| notice-every-6 | 12.440 | 130 | 16 | 2 | within |
| notice-every-7 | 7.942 | 130 | 16 | 2 | within |
| notice-every-7 | 8.140 | 130 | 16 | 2 | within |
| notice-every-7 | 2.046 | 130 | 16 | 2 | within |
| notice-every-7 | 2.251 | 130 | 16 | 2 | within |
| notice-every-7 | 3.960 | 130 | 16 | 2 | within |
| notice-every-7 | 4.160 | 130 | 16 | 2 | within |
| notice-every-7 | 5.959 | 130 | 16 | 2 | within |
| notice-every-7 | 6.160 | 130 | 16 | 2 | within |
| notice-every-7 | 9.880 | 130 | 16 | 2 | within |
| notice-every-7 | 10.047 | 130 | 16 | 2 | within |
| notice-every-7 | 11.959 | 130 | 16 | 2 | within |
| notice-every-7 | 12.154 | 130 | 16 | 2 | within |
| notice-burst-0 | 8.526 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.137 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.350 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.213 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.210 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.411 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.659 | 130 | 16 | 1 | within |
| notice-burst-0 | 2.858 | 130 | 16 | 1 | within |
| notice-burst-0 | 17.394 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.256 | 130 | 16 | 1 | within |
| notice-burst-0 | 19.450 | 130 | 16 | 1 | within |
| notice-burst-0 | 5.240 | 130 | 16 | 1 | within |
| notice-burst-1 | 8.763 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.292 | 130 | 16 | 1 | within |
| notice-burst-1 | 15.503 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.247 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.232 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.433 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.681 | 130 | 16 | 1 | within |
| notice-burst-1 | 2.880 | 130 | 16 | 1 | within |
| notice-burst-1 | 17.427 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.289 | 130 | 16 | 1 | within |
| notice-burst-1 | 19.483 | 130 | 16 | 1 | within |
| notice-burst-1 | 5.876 | 130 | 16 | 1 | within |
| notice-burst-2 | 13.999 | 130 | 16 | 1 | within |
| notice-burst-2 | 14.201 | 130 | 16 | 1 | within |
| notice-burst-2 | 15.274 | 130 | 16 | 1 | within |
| notice-burst-2 | 15.474 | 130 | 16 | 1 | within |
| notice-burst-2 | 2.700 | 130 | 16 | 1 | within |
| notice-burst-2 | 2.904 | 130 | 16 | 1 | within |
| notice-burst-2 | 4.732 | 130 | 16 | 1 | within |
| notice-burst-2 | 17.222 | 130 | 16 | 1 | within |
| notice-burst-2 | 17.401 | 130 | 16 | 1 | within |
| notice-burst-2 | 19.292 | 130 | 16 | 1 | within |
| notice-burst-2 | 19.485 | 130 | 16 | 1 | within |
| notice-burst-2 | 21.217 | 130 | 16 | 1 | within |
| notice-burst-3 | 13.437 | 130 | 16 | 2 | within |
| notice-burst-3 | 13.638 | 130 | 16 | 2 | within |
| notice-burst-3 | 15.253 | 130 | 16 | 2 | within |
| notice-burst-3 | 15.454 | 130 | 16 | 2 | within |
| notice-burst-3 | 2.242 | 130 | 16 | 2 | within |
| notice-burst-3 | 2.445 | 130 | 16 | 2 | within |
| notice-burst-3 | 4.274 | 130 | 16 | 2 | within |
| notice-burst-3 | 17.201 | 130 | 16 | 2 | within |
| notice-burst-3 | 17.380 | 130 | 16 | 2 | within |
| notice-burst-3 | 19.272 | 130 | 16 | 2 | within |
| notice-burst-3 | 19.465 | 130 | 16 | 2 | within |
| notice-burst-3 | 21.241 | 130 | 16 | 2 | within |
| notice-burst-4 | 11.609 | 130 | 16 | 0 | within |
| notice-burst-4 | 11.811 | 130 | 16 | 0 | within |
| notice-burst-4 | 2.337 | 130 | 16 | 0 | within |
| notice-burst-4 | 12.873 | 130 | 16 | 0 | within |
| notice-burst-4 | 13.071 | 130 | 16 | 0 | within |
| notice-burst-4 | 14.826 | 130 | 16 | 0 | within |
| notice-burst-4 | 15.020 | 130 | 16 | 0 | within |
| notice-burst-4 | 16.767 | 130 | 16 | 0 | within |
| notice-burst-4 | 16.946 | 130 | 16 | 0 | within |
| notice-burst-4 | 18.838 | 130 | 16 | 0 | within |
| notice-burst-4 | 19.031 | 130 | 16 | 0 | within |
| notice-burst-4 | 20.813 | 130 | 16 | 0 | within |
| notice-burst-5 | 7.565 | 130 | 16 | 1 | within |
| notice-burst-5 | 16.871 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.083 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.149 | 130 | 16 | 1 | within |
| notice-burst-5 | 18.345 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.101 | 130 | 16 | 1 | within |
| notice-burst-5 | 20.295 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.042 | 130 | 16 | 1 | within |
| notice-burst-5 | 22.221 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.113 | 130 | 16 | 1 | within |
| notice-burst-5 | 24.306 | 130 | 16 | 1 | within |
| notice-burst-5 | 26.088 | 130 | 16 | 1 | within |
| notice-burst-6 | 7.397 | 130 | 16 | 0 | within |
| notice-burst-6 | 16.671 | 130 | 16 | 0 | within |
| notice-burst-6 | 16.883 | 130 | 16 | 0 | within |
| notice-burst-6 | 17.948 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.144 | 130 | 16 | 0 | within |
| notice-burst-6 | 19.900 | 130 | 16 | 0 | within |
| notice-burst-6 | 20.094 | 130 | 16 | 0 | within |
| notice-burst-6 | 21.841 | 130 | 16 | 0 | within |
| notice-burst-6 | 22.020 | 130 | 16 | 0 | within |
| notice-burst-6 | 23.912 | 130 | 16 | 0 | within |
| notice-burst-6 | 24.105 | 130 | 16 | 0 | within |
| notice-burst-6 | 25.887 | 130 | 16 | 0 | within |
| notice-burst-7 | 9.016 | 130 | 16 | 0 | within |
| notice-burst-7 | 16.708 | 130 | 16 | 0 | within |
| notice-burst-7 | 16.921 | 130 | 16 | 0 | within |
| notice-burst-7 | 17.964 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.023 | 130 | 16 | 0 | within |
| notice-burst-7 | 2.225 | 130 | 16 | 0 | within |
| notice-burst-7 | 3.051 | 130 | 16 | 0 | within |
| notice-burst-7 | 3.253 | 130 | 16 | 0 | within |
| notice-burst-7 | 18.144 | 130 | 16 | 0 | within |
| notice-burst-7 | 20.007 | 130 | 16 | 0 | within |
| notice-burst-7 | 20.202 | 130 | 16 | 0 | within |
| notice-burst-7 | 3.510 | 130 | 16 | 0 | within |

Latest: 26.088 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 102,015 (1.020) | 76,499 (0.765) |
| notice-every-1 | 307 | 99,041 (0.990) | 76,499 (0.765) |
| notice-every-2 | 307 | 101,813 (1.018) | 76,503 (0.765) |
| notice-every-3 | 307 | 105,751 (1.058) | 76,563 (0.766) |
| notice-every-4 | 307 | 110,801 (1.108) | 76,471 (0.765) |
| notice-every-5 | 307 | 122,944 (1.229) | 75,807 (0.758) |
| notice-every-6 | 307 | 91,835 (0.918) | 75,807 (0.758) |
| notice-every-7 | 307 | 91,835 (0.918) | 75,807 (0.758) |
| notice-burst-0 | 317 | 104,006 (1.040) | 78,064 (0.781) |
| notice-burst-1 | 317 | 103,553 (1.036) | 78,000 (0.780) |
| notice-burst-2 | 317 | 101,813 (1.018) | 78,000 (0.780) |
| notice-burst-3 | 317 | 105,751 (1.058) | 78,000 (0.780) |
| notice-burst-4 | 317 | 110,801 (1.108) | 78,000 (0.780) |
| notice-burst-5 | 317 | 103,341 (1.033) | 78,064 (0.781) |
| notice-burst-6 | 317 | 105,367 (1.054) | 78,064 (0.781) |
| notice-burst-7 | 317 | 105,131 (1.051) | 78,000 (0.780) |

Longest pass that carries a step: 122,944 CPU cycles (1.229 ms), notice-every-5; longest step: 78,064 (0.781 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 816,946 | 8.169 | 130 | 134 | fits | 46,966 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 836,706 | 8.367 | 130 | 134 | fits | 46,966 | 102 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 204,540 | 2.045 | 130 | 134 | fits | 49,897 | 105 | 0.312 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 225,044 | 2.250 | 130 | 134 | fits | 49,897 | 105 | 0.312 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 396,733 | 3.967 | 130 | 134 | fits | 48,842 | 109 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 416,746 | 4.167 | 130 | 134 | fits | 48,842 | 109 | 0.284 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 596,758 | 5.968 | 130 | 134 | fits | 46,601 | 105 | 0.260 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 616,774 | 6.168 | 130 | 134 | fits | 46,601 | 105 | 0.260 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 1,008,980 | 10.090 | 130 | 134 | fits | 40,479 | 101 | 0.248 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 1,025,680 | 10.257 | 130 | 134 | fits | 40,479 | 101 | 0.248 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 1,198,880 | 11.989 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 1,218,420 | 12.184 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 162,352 | 1.624 | 20 | 200 | fits | 149,309 | 286 | 0.331 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 417,241 | 4.172 | 20 | 20 | fits | 113,701 | 92 | 0.485 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 397,037 | 3.970 | 20 | 24 | fits | 113,701 | 92 | 0.485 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 102,609 | 1.026 | 20 | 50 | fits | 149,309 | 286 | 0.331 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,082,877 | 10.829 | 20 | 20 | fits | 44,535 | 31 | 0.820 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 92,114 | 0.921 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 410,554 | 4.106 | 130 | 134 | fits | 47,648 | 104 | 0.286 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 430,235 | 4.302 | 130 | 134 | fits | 47,648 | 104 | 0.286 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 626,064 | 6.261 | 130 | 134 | fits | 48,494 | 103 | 0.300 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 646,385 | 6.464 | 130 | 134 | fits | 48,494 | 103 | 0.300 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 825,712 | 8.257 | 130 | 134 | fits | 45,488 | 102 | 0.269 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 845,202 | 8.452 | 130 | 134 | fits | 45,488 | 102 | 0.269 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 208,687 | 2.087 | 130 | 134 | fits | 49,686 | 105 | 0.323 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 229,531 | 2.295 | 130 | 134 | fits | 49,686 | 105 | 0.323 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 1,017,252 | 10.173 | 130 | 134 | fits | 40,557 | 101 | 0.253 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 1,034,030 | 10.340 | 130 | 134 | fits | 40,557 | 101 | 0.253 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 1,207,193 | 12.072 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 1,226,733 | 12.267 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 129,243 | 1.292 | 20 | 200 | fits | 124,716 | 160 | 0.328 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 427,173 | 4.272 | 20 | 20 | fits | 125,828 | 121 | 0.476 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 406,969 | 4.070 | 20 | 24 | fits | 125,828 | 121 | 0.476 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 387,698 | 3.877 | 20 | 50 | fits | 125,828 | 121 | 0.476 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,090,628 | 10.906 | 20 | 20 | fits | 44,611 | 31 | 0.820 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 96,255 | 0.963 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 203,989 | 2.040 | 130 | 134 | fits | 48,604 | 103 | 0.316 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 223,868 | 2.239 | 130 | 134 | fits | 48,604 | 103 | 0.316 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 394,205 | 3.942 | 130 | 134 | fits | 49,870 | 109 | 0.293 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 414,390 | 4.144 | 130 | 134 | fits | 49,870 | 109 | 0.293 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 593,862 | 5.939 | 130 | 134 | fits | 45,938 | 103 | 0.268 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 613,503 | 6.135 | 130 | 134 | fits | 45,938 | 103 | 0.268 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 789,951 | 7.900 | 130 | 134 | fits | 45,325 | 104 | 0.261 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 809,441 | 8.094 | 130 | 134 | fits | 45,325 | 104 | 0.261 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 983,403 | 9.834 | 130 | 134 | fits | 40,715 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 1,000,103 | 10.001 | 130 | 134 | fits | 40,715 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 1,191,197 | 11.912 | 130 | 134 | fits | 44,335 | 104 | 0.191 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 1,210,737 | 12.107 | 130 | 134 | fits | 44,335 | 104 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 166,741 | 1.667 | 20 | 200 | fits | 150,475 | 291 | 0.339 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 437,609 | 4.376 | 20 | 20 | fits | 114,472 | 92 | 0.494 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 417,405 | 4.174 | 20 | 24 | fits | 114,472 | 92 | 0.494 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 106,998 | 1.070 | 20 | 50 | fits | 150,475 | 291 | 0.339 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,100,568 | 11.006 | 20 | 20 | fits | 44,597 | 31 | 0.820 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 86,190 | 0.862 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 392,354 | 3.924 | 130 | 134 | fits | 49,513 | 109 | 0.301 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 412,183 | 4.122 | 130 | 134 | fits | 49,513 | 109 | 0.301 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 593,127 | 5.931 | 130 | 134 | fits | 47,810 | 105 | 0.275 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 613,266 | 6.133 | 130 | 134 | fits | 47,810 | 105 | 0.275 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 789,939 | 7.899 | 130 | 134 | fits | 45,482 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 809,429 | 8.094 | 130 | 134 | fits | 45,482 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 199,547 | 1.995 | 130 | 134 | fits | 49,025 | 105 | 0.304 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 220,154 | 2.202 | 130 | 134 | fits | 49,025 | 105 | 0.304 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 1,001,204 | 10.012 | 130 | 134 | fits | 40,669 | 101 | 0.253 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 1,017,937 | 10.179 | 130 | 134 | fits | 40,669 | 101 | 0.253 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 1,191,299 | 11.913 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 1,210,839 | 12.108 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 173,856 | 1.739 | 20 | 200 | fits | 151,030 | 294 | 0.339 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 448,466 | 4.485 | 20 | 20 | fits | 115,727 | 98 | 0.485 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 428,262 | 4.283 | 20 | 24 | fits | 115,727 | 98 | 0.485 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 114,113 | 1.141 | 20 | 50 | fits | 151,030 | 294 | 0.339 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,109,781 | 11.098 | 20 | 20 | fits | 44,472 | 31 | 0.819 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 96,930 | 0.969 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 392,115 | 3.921 | 130 | 134 | fits | 49,521 | 109 | 0.301 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 411,944 | 4.119 | 130 | 134 | fits | 49,521 | 109 | 0.301 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 592,779 | 5.928 | 130 | 134 | fits | 47,879 | 105 | 0.277 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 612,918 | 6.129 | 130 | 134 | fits | 47,879 | 105 | 0.277 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 789,646 | 7.896 | 130 | 134 | fits | 45,482 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 809,136 | 8.091 | 130 | 134 | fits | 45,482 | 104 | 0.265 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 199,601 | 1.996 | 130 | 134 | fits | 48,802 | 103 | 0.302 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 220,208 | 2.202 | 130 | 134 | fits | 48,802 | 103 | 0.302 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 983,125 | 9.831 | 130 | 134 | fits | 40,669 | 101 | 0.253 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 999,858 | 9.999 | 130 | 134 | fits | 40,669 | 101 | 0.253 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 1,191,006 | 11.910 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 1,210,546 | 12.105 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 155,849 | 1.558 | 20 | 200 | fits | 150,194 | 277 | 0.328 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 438,885 | 4.389 | 20 | 20 | fits | 120,793 | 114 | 0.493 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 418,681 | 4.187 | 20 | 24 | fits | 120,793 | 114 | 0.493 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 399,410 | 3.994 | 20 | 50 | fits | 120,793 | 114 | 0.493 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,101,816 | 11.018 | 20 | 20 | fits | 44,503 | 31 | 0.819 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 89,249 | 0.892 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 822,142 | 8.221 | 130 | 134 | fits | 47,029 | 104 | 0.282 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 841,902 | 8.419 | 130 | 134 | fits | 47,029 | 104 | 0.282 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 232,179 | 2.322 | 130 | 134 | fits | 50,259 | 103 | 0.329 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 252,916 | 2.529 | 130 | 134 | fits | 50,259 | 103 | 0.329 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 517,242 | 5.172 | 130 | 134 | fits | 122,944 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 537,255 | 5.373 | 130 | 134 | fits | 122,944 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 623,950 | 6.239 | 130 | 134 | fits | 46,660 | 105 | 0.264 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 643,966 | 6.440 | 130 | 134 | fits | 46,660 | 105 | 0.264 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 1,015,984 | 10.160 | 130 | 134 | fits | 40,636 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 1,032,684 | 10.327 | 130 | 134 | fits | 40,636 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 1,223,855 | 12.239 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 1,243,395 | 12.434 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 154,363 | 1.544 | 20 | 200 | fits | 148,361 | 275 | 0.345 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 437,795 | 4.378 | 20 | 20 | fits | 122,187 | 120 | 0.489 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 417,591 | 4.176 | 20 | 24 | fits | 122,187 | 120 | 0.489 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 398,320 | 3.983 | 20 | 50 | fits | 122,187 | 120 | 0.489 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,100,432 | 11.004 | 20 | 20 | fits | 44,777 | 31 | 0.821 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 88,058 | 0.881 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 823,315 | 8.233 | 130 | 134 | fits | 46,895 | 102 | 0.282 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 843,075 | 8.431 | 130 | 134 | fits | 46,895 | 102 | 0.282 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 213,516 | 2.135 | 130 | 134 | fits | 50,473 | 105 | 0.331 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 234,253 | 2.343 | 130 | 134 | fits | 50,473 | 105 | 0.331 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 414,263 | 4.143 | 130 | 134 | fits | 46,894 | 104 | 0.270 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 434,128 | 4.341 | 130 | 134 | fits | 46,894 | 104 | 0.270 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 624,845 | 6.248 | 130 | 134 | fits | 47,180 | 103 | 0.283 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 645,009 | 6.450 | 130 | 134 | fits | 47,180 | 103 | 0.283 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 1,016,742 | 10.167 | 130 | 134 | fits | 40,599 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 1,033,487 | 10.335 | 130 | 134 | fits | 40,599 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 1,224,459 | 12.245 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 1,243,999 | 12.440 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 166,982 | 1.670 | 20 | 200 | fits | 150,745 | 293 | 0.340 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 442,628 | 4.426 | 20 | 20 | fits | 114,802 | 94 | 0.499 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 422,424 | 4.224 | 20 | 24 | fits | 114,802 | 94 | 0.499 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 107,239 | 1.072 | 20 | 50 | fits | 150,745 | 293 | 0.340 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,106,704 | 11.067 | 20 | 20 | fits | 58,290 | 35 | 0.787 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 94,493 | 0.945 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 794,236 | 7.942 | 130 | 134 | fits | 46,960 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 813,996 | 8.140 | 130 | 134 | fits | 46,960 | 104 | 0.280 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 204,566 | 2.046 | 130 | 134 | fits | 49,674 | 103 | 0.310 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 225,070 | 2.251 | 130 | 134 | fits | 49,674 | 103 | 0.310 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 395,964 | 3.960 | 130 | 134 | fits | 48,850 | 109 | 0.284 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 415,977 | 4.160 | 130 | 134 | fits | 48,850 | 109 | 0.284 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 595,949 | 5.959 | 130 | 134 | fits | 46,670 | 105 | 0.262 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 615,965 | 6.160 | 130 | 134 | fits | 46,670 | 105 | 0.262 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 988,023 | 9.880 | 130 | 134 | fits | 40,636 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 1,004,723 | 10.047 | 130 | 134 | fits | 40,636 | 101 | 0.251 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 1,195,908 | 11.959 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 1,215,448 | 12.154 | 130 | 134 | fits | 44,460 | 104 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 173,678 | 1.737 | 20 | 200 | fits | 150,635 | 292 | 0.337 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 442,692 | 4.427 | 20 | 20 | fits | 112,538 | 88 | 0.490 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 422,488 | 4.225 | 20 | 24 | fits | 112,538 | 88 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 113,935 | 1.139 | 20 | 50 | fits | 150,635 | 292 | 0.337 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,105,571 | 11.056 | 20 | 20 | fits | 56,631 | 29 | 0.804 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 81,775 | 0.818 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 852,620 | 8.526 | 130 | 134 | fits | 27,817 | 51 | 0.485 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,613,708 | 16.137 | 130 | 134 | fits | 49,601 | 103 | 0.357 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,635,019 | 16.350 | 130 | 134 | fits | 49,601 | 103 | 0.357 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,721,306 | 17.213 | 130 | 134 | fits | 43,468 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 220,955 | 2.210 | 130 | 134 | fits | 62,591 | 111 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 241,085 | 2.411 | 130 | 134 | fits | 62,591 | 111 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 265,852 | 2.659 | 130 | 134 | fits | 44,298 | 103 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 285,763 | 2.858 | 130 | 134 | fits | 44,298 | 103 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,739,364 | 17.394 | 130 | 134 | fits | 43,468 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,925,628 | 19.256 | 130 | 134 | fits | 42,255 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,945,041 | 19.450 | 130 | 134 | fits | 42,255 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 523,960 | 5.240 | 130 | 134 | fits | 41,889 | 61 | 0.388 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 474,942 | 4.749 | 20 | 200 | fits | 113,437 | 191 | 0.385 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 454,674 | 4.547 | 20 | 20 | fits | 113,437 | 191 | 0.385 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 293,216 | 2.932 | 20 | 24 | fits | 148,022 | 191 | 0.426 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 415,199 | 4.152 | 20 | 50 | fits | 113,437 | 191 | 0.385 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 1,012,660 | 10.127 | 20 | 20 | fits | 78,783 | 30 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 876,333 | 8.763 | 130 | 134 | fits | 27,686 | 51 | 0.471 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,529,194 | 15.292 | 130 | 134 | fits | 49,153 | 103 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,550,319 | 15.503 | 130 | 134 | fits | 49,153 | 103 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,724,668 | 17.247 | 130 | 134 | fits | 43,468 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 223,198 | 2.232 | 130 | 134 | fits | 62,347 | 111 | 0.336 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 243,328 | 2.433 | 130 | 134 | fits | 62,347 | 111 | 0.336 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 268,095 | 2.681 | 130 | 134 | fits | 44,298 | 103 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 288,006 | 2.880 | 130 | 134 | fits | 44,298 | 103 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,742,726 | 17.427 | 130 | 134 | fits | 43,468 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,928,874 | 19.289 | 130 | 134 | fits | 42,210 | 102 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,948,287 | 19.483 | 130 | 134 | fits | 42,210 | 102 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 587,610 | 5.876 | 130 | 134 | fits | 28,263 | 52 | 0.421 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 167,449 | 1.674 | 20 | 200 | fits | 149,020 | 286 | 0.344 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 436,564 | 4.366 | 20 | 20 | fits | 109,263 | 82 | 0.498 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 416,360 | 4.164 | 20 | 24 | fits | 109,263 | 82 | 0.498 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 107,706 | 1.077 | 20 | 50 | fits | 149,020 | 286 | 0.344 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,027,477 | 10.275 | 20 | 20 | fits | 78,894 | 30 | 0.726 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 1,399,872 | 13.999 | 130 | 134 | fits | 50,020 | 103 | 0.375 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,420,114 | 14.201 | 130 | 134 | fits | 50,020 | 103 | 0.375 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,527,373 | 15.274 | 130 | 134 | fits | 47,450 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,547,440 | 15.474 | 130 | 134 | fits | 47,450 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 269,960 | 2.700 | 130 | 134 | fits | 49,440 | 102 | 0.326 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 290,363 | 2.904 | 130 | 134 | fits | 49,440 | 102 | 0.326 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 473,179 | 4.732 | 130 | 134 | fits | 26,961 | 52 | 0.452 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 1,722,157 | 17.222 | 130 | 134 | fits | 43,397 | 103 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,740,051 | 17.401 | 130 | 134 | fits | 43,397 | 103 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,929,228 | 19.292 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,948,516 | 19.485 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 2,121,653 | 21.217 | 130 | 134 | fits | 25,334 | 52 | 0.319 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 45,276 | 0.453 | 20 | 200 | fits | 35,913 | 60 | 0.229 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 431,948 | 4.319 | 20 | 20 | fits | 118,762 | 107 | 0.493 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 411,744 | 4.117 | 20 | 24 | fits | 118,762 | 107 | 0.493 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 392,473 | 3.925 | 20 | 50 | fits | 118,762 | 107 | 0.493 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 994,923 | 9.949 | 20 | 20 | fits | 79,121 | 30 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,343,716 | 13.437 | 130 | 134 | fits | 49,873 | 103 | 0.370 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,363,815 | 13.638 | 130 | 134 | fits | 49,873 | 103 | 0.370 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,525,317 | 15.253 | 130 | 134 | fits | 47,450 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,545,384 | 15.454 | 130 | 134 | fits | 47,450 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 224,222 | 2.242 | 130 | 134 | fits | 64,982 | 111 | 0.384 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 244,486 | 2.445 | 130 | 134 | fits | 64,982 | 111 | 0.384 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 427,407 | 4.274 | 130 | 134 | fits | 26,639 | 54 | 0.424 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,720,101 | 17.201 | 130 | 134 | fits | 43,397 | 103 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,737,995 | 17.380 | 130 | 134 | fits | 43,397 | 103 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,927,172 | 19.272 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,946,460 | 19.465 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,124,055 | 21.241 | 130 | 134 | fits | 25,697 | 52 | 0.333 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 495,694 | 4.957 | 20 | 200 | fits | 113,022 | 195 | 0.352 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 475,426 | 4.754 | 20 | 20 | fits | 113,022 | 195 | 0.352 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 342,200 | 3.422 | 20 | 24 | fits | 149,563 | 187 | 0.444 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 435,951 | 4.360 | 20 | 50 | fits | 113,022 | 195 | 0.352 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,038,169 | 10.382 | 20 | 20 | fits | 79,127 | 30 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,160,892 | 11.609 | 130 | 134 | fits | 49,908 | 102 | 0.373 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,181,062 | 11.811 | 130 | 134 | fits | 49,908 | 102 | 0.373 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 233,668 | 2.337 | 130 | 134 | fits | 29,429 | 52 | 0.502 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,287,309 | 12.873 | 130 | 134 | fits | 45,735 | 103 | 0.261 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,307,113 | 13.071 | 130 | 134 | fits | 45,735 | 103 | 0.261 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,482,607 | 14.826 | 130 | 134 | fits | 45,008 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,502,044 | 15.020 | 130 | 134 | fits | 45,008 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,676,738 | 16.767 | 130 | 134 | fits | 43,437 | 103 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,694,632 | 16.946 | 130 | 134 | fits | 43,437 | 103 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,883,847 | 18.838 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,903,135 | 19.031 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,081,294 | 20.813 | 130 | 134 | fits | 25,596 | 52 | 0.326 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 154,551 | 1.546 | 20 | 200 | fits | 150,998 | 280 | 0.324 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 437,558 | 4.376 | 20 | 20 | fits | 118,984 | 107 | 0.490 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 417,354 | 4.174 | 20 | 24 | fits | 118,984 | 107 | 0.490 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 398,083 | 3.981 | 20 | 50 | fits | 118,984 | 107 | 0.490 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 999,655 | 9.997 | 20 | 20 | fits | 79,206 | 30 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 756,494 | 7.565 | 130 | 134 | fits | 28,420 | 52 | 0.489 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,687,098 | 16.871 | 130 | 134 | fits | 49,932 | 102 | 0.369 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,708,334 | 17.083 | 130 | 134 | fits | 49,932 | 102 | 0.369 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,814,858 | 18.149 | 130 | 134 | fits | 45,816 | 103 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,834,524 | 18.345 | 130 | 134 | fits | 45,816 | 103 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,010,086 | 20.101 | 130 | 134 | fits | 45,008 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 2,029,523 | 20.295 | 130 | 134 | fits | 45,008 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 2,204,217 | 22.042 | 130 | 134 | fits | 43,437 | 103 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,222,111 | 22.221 | 130 | 134 | fits | 43,437 | 103 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,411,326 | 24.113 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,430,614 | 24.306 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,608,759 | 26.088 | 130 | 134 | fits | 25,596 | 52 | 0.326 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 148,156 | 1.482 | 20 | 200 | fits | 147,371 | 277 | 0.329 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 436,908 | 4.369 | 20 | 20 | fits | 125,777 | 120 | 0.474 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 416,704 | 4.167 | 20 | 24 | fits | 125,777 | 120 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 397,433 | 3.974 | 20 | 50 | fits | 125,777 | 120 | 0.474 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 996,910 | 9.969 | 20 | 20 | fits | 79,240 | 30 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 739,687 | 7.397 | 130 | 134 | fits | 28,874 | 52 | 0.502 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,667,066 | 16.671 | 130 | 134 | fits | 50,066 | 102 | 0.372 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,688,302 | 16.883 | 130 | 134 | fits | 50,066 | 102 | 0.372 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,794,777 | 17.948 | 130 | 134 | fits | 45,765 | 103 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,814,443 | 18.144 | 130 | 134 | fits | 45,765 | 103 | 0.262 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,990,005 | 19.900 | 130 | 134 | fits | 45,008 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,009,442 | 20.094 | 130 | 134 | fits | 45,008 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,184,136 | 21.841 | 130 | 134 | fits | 43,437 | 103 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,202,030 | 22.020 | 130 | 134 | fits | 43,437 | 103 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,391,245 | 23.912 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,410,533 | 24.105 | 130 | 134 | fits | 42,746 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,588,692 | 25.887 | 130 | 134 | fits | 25,596 | 52 | 0.326 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 155,100 | 1.551 | 20 | 200 | fits | 151,099 | 279 | 0.325 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 438,993 | 4.390 | 20 | 20 | fits | 120,300 | 113 | 0.481 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 418,789 | 4.188 | 20 | 24 | fits | 120,300 | 113 | 0.481 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 399,518 | 3.995 | 20 | 50 | fits | 120,300 | 113 | 0.481 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 1,000,913 | 10.009 | 20 | 20 | fits | 79,206 | 30 | 0.724 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 901,606 | 9.016 | 130 | 134 | fits | 27,610 | 54 | 0.470 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,670,772 | 16.708 | 130 | 134 | fits | 49,498 | 103 | 0.356 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,692,083 | 16.921 | 130 | 134 | fits | 49,498 | 103 | 0.356 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,796,352 | 17.964 | 130 | 134 | fits | 43,379 | 102 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 202,255 | 2.023 | 130 | 134 | fits | 62,961 | 111 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 222,481 | 2.225 | 130 | 134 | fits | 62,961 | 111 | 0.338 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 305,140 | 3.051 | 130 | 134 | fits | 61,142 | 112 | 0.287 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 325,287 | 3.253 | 130 | 134 | fits | 61,142 | 112 | 0.287 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,814,410 | 18.144 | 130 | 134 | fits | 43,379 | 102 | 0.236 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,000,680 | 20.007 | 130 | 134 | fits | 42,402 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,020,163 | 20.202 | 130 | 134 | fits | 42,402 | 102 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 351,045 | 3.510 | 130 | 134 | fits | 25,100 | 52 | 0.191 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 155,169 | 1.552 | 20 | 200 | fits | 149,050 | 274 | 0.329 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 433,198 | 4.332 | 20 | 20 | fits | 122,486 | 122 | 0.501 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 412,994 | 4.130 | 20 | 24 | fits | 122,486 | 122 | 0.501 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 393,723 | 3.937 | 20 | 50 | fits | 122,486 | 122 | 0.501 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 990,236 | 9.902 | 20 | 20 | fits | 78,783 | 30 | 0.724 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

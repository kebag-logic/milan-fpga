### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.acmp.if0` (notice-burst-3) | 4.425 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.adp.if0` (notice-burst-3) | 4.627 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.aecp.if0` (notice-every-5) | 3.954 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.maap.if0` (notice-burst-3) | 4.030 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-3.held.srp.if0` (notice-burst-3) | 9.453 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-1.mrpdu.periodic.if0` (notice-every-1) | 0.652 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-6.notices.29.36.0.if0` (notice-burst-6) | 21.380 (21.592) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 2052 | 0 | 147,512 (1.475) | fits |
| notice-every-1 | 2051 | 0 | 147,969 (1.480) | fits |
| notice-every-2 | 2048 | 0 | 148,373 (1.484) | fits |
| notice-every-3 | 2052 | 0 | 148,023 (1.480) | fits |
| notice-every-4 | 2050 | 0 | 148,258 (1.483) | fits |
| notice-every-5 | 2042 | 0 | 146,250 (1.462) | fits |
| notice-every-6 | 2045 | 0 | 148,847 (1.488) | fits |
| notice-every-7 | 2036 | 0 | 148,035 (1.480) | fits |
| notice-burst-0 | 1341 | 0 | 152,204 (1.522) | fits |
| notice-burst-1 | 1344 | 0 | 152,180 (1.522) | fits |
| notice-burst-2 | 1347 | 0 | 147,044 (1.470) | fits |
| notice-burst-3 | 1341 | 0 | 146,637 (1.466) | fits |
| notice-burst-4 | 1335 | 0 | 147,368 (1.474) | fits |
| notice-burst-5 | 1335 | 0 | 147,953 (1.480) | fits |
| notice-burst-6 | 1331 | 0 | 148,806 (1.488) | fits |
| notice-burst-7 | 1334 | 0 | 152,053 (1.521) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.050 | 135 | 16 | 2 | within |
| notice-every-0 | 8.224 | 135 | 16 | 2 | within |
| notice-every-0 | 2.062 | 135 | 16 | 2 | within |
| notice-every-0 | 2.239 | 135 | 16 | 2 | within |
| notice-every-0 | 3.900 | 135 | 16 | 2 | within |
| notice-every-0 | 4.079 | 135 | 16 | 2 | within |
| notice-every-0 | 6.077 | 135 | 16 | 2 | within |
| notice-every-0 | 6.254 | 135 | 16 | 2 | within |
| notice-every-0 | 8.354 | 135 | 16 | 2 | within |
| notice-every-0 | 9.953 | 135 | 16 | 2 | within |
| notice-every-0 | 2.414 | 135 | 16 | 2 | within |
| notice-every-0 | 4.253 | 135 | 16 | 2 | within |
| notice-every-1 | 2.203 | 135 | 16 | 2 | within |
| notice-every-1 | 2.379 | 135 | 16 | 2 | within |
| notice-every-1 | 4.084 | 135 | 16 | 2 | within |
| notice-every-1 | 4.258 | 135 | 16 | 2 | within |
| notice-every-1 | 6.146 | 135 | 16 | 2 | within |
| notice-every-1 | 6.321 | 135 | 16 | 2 | within |
| notice-every-1 | 8.144 | 135 | 16 | 2 | within |
| notice-every-1 | 8.316 | 135 | 16 | 2 | within |
| notice-every-1 | 2.522 | 135 | 16 | 2 | within |
| notice-every-1 | 4.389 | 135 | 16 | 2 | within |
| notice-every-1 | 6.491 | 135 | 16 | 2 | within |
| notice-every-1 | 8.480 | 135 | 16 | 2 | within |
| notice-every-2 | 1.962 | 135 | 16 | 2 | within |
| notice-every-2 | 2.138 | 135 | 16 | 2 | within |
| notice-every-2 | 4.092 | 135 | 16 | 2 | within |
| notice-every-2 | 4.267 | 135 | 16 | 2 | within |
| notice-every-2 | 5.930 | 135 | 16 | 2 | within |
| notice-every-2 | 6.104 | 135 | 16 | 2 | within |
| notice-every-2 | 7.927 | 135 | 16 | 2 | within |
| notice-every-2 | 8.099 | 135 | 16 | 2 | within |
| notice-every-2 | 2.279 | 135 | 16 | 2 | within |
| notice-every-2 | 4.398 | 135 | 16 | 2 | within |
| notice-every-2 | 6.273 | 135 | 16 | 2 | within |
| notice-every-2 | 8.263 | 135 | 16 | 2 | within |
| notice-every-3 | 3.957 | 135 | 16 | 2 | within |
| notice-every-3 | 4.132 | 135 | 16 | 2 | within |
| notice-every-3 | 5.954 | 135 | 16 | 2 | within |
| notice-every-3 | 6.129 | 135 | 16 | 2 | within |
| notice-every-3 | 7.918 | 135 | 16 | 2 | within |
| notice-every-3 | 8.092 | 135 | 16 | 2 | within |
| notice-every-3 | 1.962 | 135 | 16 | 2 | within |
| notice-every-3 | 2.145 | 135 | 16 | 2 | within |
| notice-every-3 | 4.268 | 135 | 16 | 2 | within |
| notice-every-3 | 6.257 | 135 | 16 | 2 | within |
| notice-every-3 | 2.319 | 135 | 16 | 2 | within |
| notice-every-3 | 8.259 | 135 | 16 | 2 | within |
| notice-every-4 | 3.961 | 135 | 16 | 2 | within |
| notice-every-4 | 4.136 | 135 | 16 | 2 | within |
| notice-every-4 | 5.959 | 135 | 16 | 2 | within |
| notice-every-4 | 6.133 | 135 | 16 | 2 | within |
| notice-every-4 | 7.920 | 135 | 16 | 2 | within |
| notice-every-4 | 8.094 | 135 | 16 | 2 | within |
| notice-every-4 | 1.965 | 135 | 16 | 2 | within |
| notice-every-4 | 2.148 | 135 | 16 | 2 | within |
| notice-every-4 | 4.272 | 135 | 16 | 2 | within |
| notice-every-4 | 6.262 | 135 | 16 | 2 | within |
| notice-every-4 | 2.323 | 135 | 16 | 2 | within |
| notice-every-4 | 8.261 | 135 | 16 | 2 | within |
| notice-every-5 | 6.027 | 135 | 16 | 2 | within |
| notice-every-5 | 6.201 | 135 | 16 | 2 | within |
| notice-every-5 | 7.851 | 135 | 16 | 2 | within |
| notice-every-5 | 8.026 | 135 | 16 | 2 | within |
| notice-every-5 | 2.006 | 135 | 16 | 2 | within |
| notice-every-5 | 2.189 | 135 | 16 | 2 | within |
| notice-every-5 | 3.847 | 135 | 16 | 2 | within |
| notice-every-5 | 4.027 | 135 | 16 | 2 | within |
| notice-every-5 | 6.335 | 135 | 16 | 2 | within |
| notice-every-5 | 8.152 | 135 | 16 | 2 | within |
| notice-every-5 | 2.365 | 135 | 16 | 2 | within |
| notice-every-5 | 4.199 | 135 | 16 | 2 | within |
| notice-every-6 | 6.137 | 135 | 16 | 2 | within |
| notice-every-6 | 6.311 | 135 | 16 | 2 | within |
| notice-every-6 | 7.961 | 135 | 16 | 2 | within |
| notice-every-6 | 8.136 | 135 | 16 | 2 | within |
| notice-every-6 | 1.966 | 135 | 16 | 2 | within |
| notice-every-6 | 2.149 | 135 | 16 | 2 | within |
| notice-every-6 | 3.957 | 135 | 16 | 2 | within |
| notice-every-6 | 4.137 | 135 | 16 | 2 | within |
| notice-every-6 | 6.445 | 135 | 16 | 2 | within |
| notice-every-6 | 8.262 | 135 | 16 | 2 | within |
| notice-every-6 | 2.325 | 135 | 16 | 2 | within |
| notice-every-6 | 4.309 | 135 | 16 | 2 | within |
| notice-every-7 | 8.026 | 135 | 16 | 2 | within |
| notice-every-7 | 8.200 | 135 | 16 | 2 | within |
| notice-every-7 | 1.886 | 135 | 16 | 2 | within |
| notice-every-7 | 2.064 | 135 | 16 | 2 | within |
| notice-every-7 | 3.876 | 135 | 16 | 2 | within |
| notice-every-7 | 4.055 | 135 | 16 | 2 | within |
| notice-every-7 | 6.052 | 135 | 16 | 2 | within |
| notice-every-7 | 6.229 | 135 | 16 | 2 | within |
| notice-every-7 | 8.330 | 135 | 16 | 2 | within |
| notice-every-7 | 9.928 | 135 | 16 | 2 | within |
| notice-every-7 | 2.238 | 135 | 16 | 2 | within |
| notice-every-7 | 4.229 | 135 | 16 | 2 | within |
| notice-burst-0 | 9.062 | 135 | 16 | 1 | within |
| notice-burst-0 | 14.693 | 135 | 16 | 1 | within |
| notice-burst-0 | 14.860 | 135 | 16 | 1 | within |
| notice-burst-0 | 15.027 | 135 | 16 | 1 | within |
| notice-burst-0 | 16.152 | 135 | 16 | 1 | within |
| notice-burst-0 | 16.326 | 135 | 16 | 1 | within |
| notice-burst-0 | 2.149 | 135 | 16 | 1 | within |
| notice-burst-0 | 2.330 | 135 | 16 | 1 | within |
| notice-burst-0 | 16.459 | 135 | 16 | 1 | within |
| notice-burst-0 | 18.188 | 135 | 16 | 1 | within |
| notice-burst-0 | 18.361 | 135 | 16 | 1 | within |
| notice-burst-0 | 3.217 | 135 | 16 | 1 | within |
| notice-burst-1 | 8.938 | 135 | 16 | 1 | within |
| notice-burst-1 | 13.732 | 135 | 16 | 1 | within |
| notice-burst-1 | 13.898 | 135 | 16 | 1 | within |
| notice-burst-1 | 14.064 | 135 | 16 | 1 | within |
| notice-burst-1 | 15.184 | 135 | 16 | 1 | within |
| notice-burst-1 | 15.359 | 135 | 16 | 1 | within |
| notice-burst-1 | 2.358 | 135 | 16 | 1 | within |
| notice-burst-1 | 2.541 | 135 | 16 | 1 | within |
| notice-burst-1 | 15.492 | 135 | 16 | 1 | within |
| notice-burst-1 | 17.220 | 135 | 16 | 1 | within |
| notice-burst-1 | 17.393 | 135 | 16 | 1 | within |
| notice-burst-1 | 3.472 | 135 | 16 | 1 | within |
| notice-burst-2 | 8.865 | 135 | 16 | 0 | within |
| notice-burst-2 | 12.861 | 135 | 16 | 0 | within |
| notice-burst-2 | 13.027 | 135 | 16 | 0 | within |
| notice-burst-2 | 13.193 | 135 | 16 | 0 | within |
| notice-burst-2 | 14.050 | 135 | 16 | 0 | within |
| notice-burst-2 | 14.225 | 135 | 16 | 0 | within |
| notice-burst-2 | 2.045 | 135 | 16 | 0 | within |
| notice-burst-2 | 2.226 | 135 | 16 | 0 | within |
| notice-burst-2 | 14.358 | 135 | 16 | 0 | within |
| notice-burst-2 | 15.955 | 135 | 16 | 0 | within |
| notice-burst-2 | 16.128 | 135 | 16 | 0 | within |
| notice-burst-2 | 4.478 | 135 | 16 | 0 | within |
| notice-burst-3 | 8.253 | 135 | 16 | 0 | within |
| notice-burst-3 | 12.237 | 135 | 16 | 0 | within |
| notice-burst-3 | 12.403 | 135 | 16 | 0 | within |
| notice-burst-3 | 12.570 | 135 | 16 | 0 | within |
| notice-burst-3 | 13.953 | 135 | 16 | 0 | within |
| notice-burst-3 | 14.127 | 135 | 16 | 0 | within |
| notice-burst-3 | 2.001 | 135 | 16 | 0 | within |
| notice-burst-3 | 2.183 | 135 | 16 | 0 | within |
| notice-burst-3 | 14.260 | 135 | 16 | 0 | within |
| notice-burst-3 | 15.988 | 135 | 16 | 0 | within |
| notice-burst-3 | 16.161 | 135 | 16 | 0 | within |
| notice-burst-3 | 5.375 | 135 | 16 | 0 | within |
| notice-burst-4 | 10.536 | 135 | 16 | 0 | within |
| notice-burst-4 | 10.714 | 135 | 16 | 0 | within |
| notice-burst-4 | 10.862 | 135 | 16 | 0 | within |
| notice-burst-4 | 12.017 | 135 | 16 | 0 | within |
| notice-burst-4 | 2.479 | 135 | 16 | 0 | within |
| notice-burst-4 | 12.188 | 135 | 16 | 0 | within |
| notice-burst-4 | 12.338 | 135 | 16 | 0 | within |
| notice-burst-4 | 13.992 | 135 | 16 | 0 | within |
| notice-burst-4 | 14.126 | 135 | 16 | 0 | within |
| notice-burst-4 | 14.242 | 135 | 16 | 0 | within |
| notice-burst-4 | 16.006 | 135 | 16 | 0 | within |
| notice-burst-4 | 16.174 | 135 | 16 | 0 | within |
| notice-burst-5 | 7.633 | 135 | 16 | 1 | within |
| notice-burst-5 | 15.690 | 135 | 16 | 1 | within |
| notice-burst-5 | 15.858 | 135 | 16 | 1 | within |
| notice-burst-5 | 16.022 | 135 | 16 | 1 | within |
| notice-burst-5 | 17.156 | 135 | 16 | 1 | within |
| notice-burst-5 | 17.331 | 135 | 16 | 1 | within |
| notice-burst-5 | 17.475 | 135 | 16 | 1 | within |
| notice-burst-5 | 19.131 | 135 | 16 | 1 | within |
| notice-burst-5 | 19.266 | 135 | 16 | 1 | within |
| notice-burst-5 | 19.382 | 135 | 16 | 1 | within |
| notice-burst-5 | 21.147 | 135 | 16 | 1 | within |
| notice-burst-5 | 21.315 | 135 | 16 | 1 | within |
| notice-burst-6 | 7.737 | 135 | 16 | 1 | within |
| notice-burst-6 | 15.754 | 135 | 16 | 1 | within |
| notice-burst-6 | 15.922 | 135 | 16 | 1 | within |
| notice-burst-6 | 16.087 | 135 | 16 | 1 | within |
| notice-burst-6 | 17.221 | 135 | 16 | 1 | within |
| notice-burst-6 | 17.396 | 135 | 16 | 1 | within |
| notice-burst-6 | 17.540 | 135 | 16 | 1 | within |
| notice-burst-6 | 19.197 | 135 | 16 | 1 | within |
| notice-burst-6 | 19.331 | 135 | 16 | 1 | within |
| notice-burst-6 | 19.447 | 135 | 16 | 1 | within |
| notice-burst-6 | 21.213 | 135 | 16 | 1 | within |
| notice-burst-6 | 21.380 | 135 | 16 | 1 | within |
| notice-burst-7 | 9.161 | 135 | 16 | 1 | within |
| notice-burst-7 | 15.637 | 135 | 16 | 1 | within |
| notice-burst-7 | 15.805 | 135 | 16 | 1 | within |
| notice-burst-7 | 15.972 | 135 | 16 | 1 | within |
| notice-burst-7 | 17.225 | 135 | 16 | 1 | within |
| notice-burst-7 | 17.399 | 135 | 16 | 1 | within |
| notice-burst-7 | 2.149 | 135 | 16 | 1 | within |
| notice-burst-7 | 2.330 | 135 | 16 | 1 | within |
| notice-burst-7 | 17.532 | 135 | 16 | 1 | within |
| notice-burst-7 | 19.129 | 135 | 16 | 1 | within |
| notice-burst-7 | 19.303 | 135 | 16 | 1 | within |
| notice-burst-7 | 3.218 | 135 | 16 | 1 | within |

Latest: 21.380 ms, notice-burst-6.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 402 | 93,889 (0.939) | 78,144 (0.781) |
| notice-every-1 | 402 | 93,889 (0.939) | 78,144 (0.781) |
| notice-every-2 | 402 | 93,889 (0.939) | 78,144 (0.781) |
| notice-every-3 | 402 | 93,889 (0.939) | 78,144 (0.781) |
| notice-every-4 | 402 | 93,889 (0.939) | 78,144 (0.781) |
| notice-every-5 | 402 | 93,889 (0.939) | 78,144 (0.781) |
| notice-every-6 | 402 | 93,889 (0.939) | 78,144 (0.781) |
| notice-every-7 | 402 | 93,889 (0.939) | 78,144 (0.781) |
| notice-burst-0 | 412 | 93,889 (0.939) | 78,144 (0.781) |
| notice-burst-1 | 412 | 93,889 (0.939) | 78,144 (0.781) |
| notice-burst-2 | 412 | 93,889 (0.939) | 78,144 (0.781) |
| notice-burst-3 | 412 | 93,889 (0.939) | 78,144 (0.781) |
| notice-burst-4 | 412 | 93,889 (0.939) | 78,144 (0.781) |
| notice-burst-5 | 412 | 93,889 (0.939) | 78,144 (0.781) |
| notice-burst-6 | 412 | 93,889 (0.939) | 78,144 (0.781) |
| notice-burst-7 | 412 | 93,889 (0.939) | 78,144 (0.781) |

Longest pass that carries a step: 93,889 CPU cycles (0.939 ms), notice-every-0; longest step: 78,144 (0.781 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 805,050 | 8.050 | 135 | 139 | fits | 53,181 | 152 | 0.219 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 822,400 | 8.224 | 135 | 139 | fits | 53,181 | 152 | 0.219 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 206,158 | 2.062 | 135 | 139 | fits | 59,949 | 153 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 223,936 | 2.239 | 135 | 139 | fits | 59,949 | 153 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 390,005 | 3.900 | 135 | 139 | fits | 58,754 | 155 | 0.177 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 407,942 | 4.079 | 135 | 139 | fits | 58,754 | 155 | 0.177 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 607,741 | 6.077 | 135 | 139 | fits | 40,156 | 103 | 0.239 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 625,395 | 6.254 | 135 | 139 | fits | 40,156 | 103 | 0.239 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 835,441 | 8.354 | 135 | 139 | fits | 53,181 | 152 | 0.219 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 995,291 | 9.953 | 135 | 139 | fits | 18,848 | 51 | 0.367 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 241,359 | 2.414 | 135 | 139 | fits | 59,949 | 153 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 425,316 | 4.253 | 135 | 139 | fits | 58,754 | 155 | 0.177 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 127,250 | 1.272 | 20 | 200 | fits | 119,723 | 154 | 0.252 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 381,707 | 3.817 | 20 | 20 | fits | 100,171 | 99 | 0.447 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 361,503 | 3.615 | 20 | 24 | fits | 100,171 | 99 | 0.447 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 342,232 | 3.422 | 20 | 50 | fits | 100,171 | 99 | 0.447 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 916,135 | 9.161 | 20 | 20 | fits | 50,530 | 53 | 0.755 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 55,113 | 0.551 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 220,268 | 2.203 | 135 | 139 | fits | 56,145 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 237,940 | 2.379 | 135 | 139 | fits | 56,145 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 408,397 | 4.084 | 135 | 139 | fits | 54,101 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 425,831 | 4.258 | 135 | 139 | fits | 54,101 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 614,647 | 6.146 | 135 | 139 | fits | 57,194 | 153 | 0.179 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 632,149 | 6.321 | 135 | 139 | fits | 57,194 | 153 | 0.179 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 814,383 | 8.144 | 135 | 139 | fits | 55,140 | 153 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 831,602 | 8.316 | 135 | 139 | fits | 55,140 | 153 | 0.169 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 252,194 | 2.522 | 135 | 139 | fits | 56,145 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 438,932 | 4.389 | 135 | 139 | fits | 54,101 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 649,055 | 6.491 | 135 | 139 | fits | 57,194 | 153 | 0.179 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 848,000 | 8.480 | 135 | 139 | fits | 55,140 | 153 | 0.169 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 162,982 | 1.630 | 20 | 200 | fits | 147,969 | 269 | 0.364 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 393,700 | 3.937 | 20 | 20 | fits | 95,063 | 92 | 0.469 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 373,496 | 3.735 | 20 | 24 | fits | 95,063 | 92 | 0.469 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 354,225 | 3.542 | 20 | 50 | fits | 95,063 | 92 | 0.469 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 911,384 | 9.114 | 20 | 20 | fits | 47,268 | 47 | 0.749 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 65,177 | 0.652 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 196,154 | 1.962 | 135 | 139 | fits | 55,904 | 155 | 0.238 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 213,826 | 2.138 | 135 | 139 | fits | 55,904 | 155 | 0.238 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 409,170 | 4.092 | 135 | 139 | fits | 54,399 | 151 | 0.224 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 426,683 | 4.267 | 135 | 139 | fits | 54,399 | 151 | 0.224 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 592,997 | 5.930 | 135 | 139 | fits | 56,896 | 155 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 610,420 | 6.104 | 135 | 139 | fits | 56,896 | 155 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 792,718 | 7.927 | 135 | 139 | fits | 55,264 | 155 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 809,937 | 8.099 | 135 | 139 | fits | 55,264 | 155 | 0.168 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 227,857 | 2.279 | 135 | 139 | fits | 55,904 | 155 | 0.238 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 439,784 | 4.398 | 135 | 139 | fits | 54,399 | 151 | 0.224 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 627,326 | 6.273 | 135 | 139 | fits | 56,896 | 155 | 0.172 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 826,335 | 8.263 | 135 | 139 | fits | 55,264 | 155 | 0.168 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 127,337 | 1.273 | 20 | 200 | fits | 121,453 | 157 | 0.248 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 400,128 | 4.001 | 20 | 20 | fits | 103,164 | 126 | 0.456 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 379,924 | 3.799 | 20 | 24 | fits | 103,164 | 126 | 0.456 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 360,653 | 3.607 | 20 | 50 | fits | 103,164 | 126 | 0.456 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 927,663 | 9.277 | 20 | 20 | fits | 50,574 | 53 | 0.755 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 49,588 | 0.496 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 395,703 | 3.957 | 135 | 139 | fits | 55,142 | 155 | 0.230 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 413,216 | 4.132 | 135 | 139 | fits | 55,142 | 155 | 0.230 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 595,428 | 5.954 | 135 | 139 | fits | 53,485 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 612,851 | 6.129 | 135 | 139 | fits | 53,485 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 791,802 | 7.918 | 135 | 139 | fits | 55,992 | 155 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 809,225 | 8.092 | 135 | 139 | fits | 55,992 | 155 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 196,198 | 1.962 | 135 | 139 | fits | 59,713 | 155 | 0.181 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 214,498 | 2.145 | 135 | 139 | fits | 59,713 | 155 | 0.181 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 426,800 | 4.268 | 135 | 139 | fits | 55,142 | 155 | 0.230 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 625,719 | 6.257 | 135 | 139 | fits | 53,485 | 153 | 0.217 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 231,908 | 2.319 | 135 | 139 | fits | 59,713 | 155 | 0.181 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 825,906 | 8.259 | 135 | 139 | fits | 55,992 | 155 | 0.169 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 179,400 | 1.794 | 20 | 200 | fits | 148,023 | 289 | 0.375 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 413,627 | 4.136 | 20 | 20 | fits | 96,436 | 90 | 0.443 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 393,423 | 3.934 | 20 | 24 | fits | 96,436 | 90 | 0.443 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 119,657 | 1.197 | 20 | 50 | fits | 148,023 | 289 | 0.375 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 939,154 | 9.392 | 20 | 20 | fits | 49,673 | 47 | 0.773 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 47,170 | 0.472 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 396,056 | 3.961 | 135 | 139 | fits | 55,018 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 413,569 | 4.136 | 135 | 139 | fits | 55,018 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 595,860 | 5.959 | 135 | 139 | fits | 53,361 | 151 | 0.218 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 613,283 | 6.133 | 135 | 139 | fits | 53,361 | 151 | 0.218 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 791,962 | 7.920 | 135 | 139 | fits | 55,992 | 155 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 809,385 | 8.094 | 135 | 139 | fits | 55,992 | 155 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 196,542 | 1.965 | 135 | 139 | fits | 59,589 | 153 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 214,842 | 2.148 | 135 | 139 | fits | 59,589 | 153 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 427,153 | 4.272 | 135 | 139 | fits | 55,018 | 153 | 0.231 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 626,151 | 6.262 | 135 | 139 | fits | 53,361 | 151 | 0.218 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 232,252 | 2.323 | 135 | 139 | fits | 59,589 | 153 | 0.182 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 826,066 | 8.261 | 135 | 139 | fits | 55,992 | 155 | 0.169 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 34,462 | 0.345 | 20 | 200 | fits | 33,918 | 60 | 0.118 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 406,596 | 4.066 | 20 | 20 | fits | 104,884 | 118 | 0.457 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 386,392 | 3.864 | 20 | 24 | fits | 104,884 | 118 | 0.457 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 367,121 | 3.671 | 20 | 50 | fits | 104,884 | 118 | 0.457 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 936,089 | 9.361 | 20 | 20 | fits | 51,233 | 53 | 0.760 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 47,150 | 0.471 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 602,687 | 6.027 | 135 | 139 | fits | 54,020 | 153 | 0.225 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 620,110 | 6.201 | 135 | 139 | fits | 54,020 | 153 | 0.225 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 785,136 | 7.851 | 135 | 139 | fits | 52,830 | 153 | 0.219 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 802,559 | 8.026 | 135 | 139 | fits | 52,830 | 153 | 0.219 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 200,596 | 2.006 | 135 | 139 | fits | 59,924 | 153 | 0.186 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 218,934 | 2.189 | 135 | 139 | fits | 59,924 | 153 | 0.186 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 384,719 | 3.847 | 135 | 139 | fits | 58,560 | 155 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 402,683 | 4.027 | 135 | 139 | fits | 58,560 | 155 | 0.172 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 633,463 | 6.335 | 135 | 139 | fits | 54,020 | 153 | 0.225 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 815,196 | 8.152 | 135 | 139 | fits | 52,830 | 153 | 0.219 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 236,488 | 2.365 | 135 | 139 | fits | 59,924 | 153 | 0.186 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 419,913 | 4.199 | 135 | 139 | fits | 58,560 | 155 | 0.172 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 165,564 | 1.656 | 20 | 200 | fits | 145,806 | 279 | 0.371 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 415,584 | 4.156 | 20 | 20 | fits | 98,078 | 98 | 0.449 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 395,380 | 3.954 | 20 | 24 | fits | 98,078 | 98 | 0.449 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 105,821 | 1.058 | 20 | 50 | fits | 145,806 | 279 | 0.371 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 941,711 | 9.417 | 20 | 20 | fits | 48,854 | 47 | 0.767 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 55,718 | 0.557 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 613,686 | 6.137 | 135 | 139 | fits | 54,020 | 153 | 0.225 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 631,109 | 6.311 | 135 | 139 | fits | 54,020 | 153 | 0.225 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 796,133 | 7.961 | 135 | 139 | fits | 52,830 | 153 | 0.219 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 813,556 | 8.136 | 135 | 139 | fits | 52,830 | 153 | 0.219 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 196,582 | 1.966 | 135 | 139 | fits | 60,048 | 155 | 0.185 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 214,920 | 2.149 | 135 | 139 | fits | 60,048 | 155 | 0.185 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 395,718 | 3.957 | 135 | 139 | fits | 58,560 | 155 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 413,682 | 4.137 | 135 | 139 | fits | 58,560 | 155 | 0.172 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 644,462 | 6.445 | 135 | 139 | fits | 54,020 | 153 | 0.225 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 826,193 | 8.262 | 135 | 139 | fits | 52,830 | 153 | 0.219 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 232,474 | 2.325 | 135 | 139 | fits | 60,048 | 155 | 0.185 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 430,912 | 4.309 | 135 | 139 | fits | 58,560 | 155 | 0.172 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 162,537 | 1.625 | 20 | 200 | fits | 148,847 | 278 | 0.359 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 403,598 | 4.036 | 20 | 20 | fits | 98,949 | 107 | 0.484 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 383,394 | 3.834 | 20 | 24 | fits | 98,949 | 107 | 0.484 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 364,123 | 3.641 | 20 | 50 | fits | 98,949 | 107 | 0.484 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 927,643 | 9.276 | 20 | 20 | fits | 49,100 | 47 | 0.769 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 55,443 | 0.554 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 802,608 | 8.026 | 135 | 139 | fits | 53,244 | 152 | 0.221 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 819,958 | 8.200 | 135 | 139 | fits | 53,244 | 152 | 0.221 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 188,611 | 1.886 | 135 | 139 | fits | 60,073 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 206,389 | 2.064 | 135 | 139 | fits | 60,073 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 387,558 | 3.876 | 135 | 139 | fits | 58,691 | 155 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 405,495 | 4.055 | 135 | 139 | fits | 58,691 | 155 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 605,222 | 6.052 | 135 | 139 | fits | 40,156 | 103 | 0.239 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 622,876 | 6.229 | 135 | 139 | fits | 40,156 | 103 | 0.239 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 832,999 | 8.330 | 135 | 139 | fits | 53,244 | 152 | 0.221 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 992,849 | 9.928 | 135 | 139 | fits | 18,848 | 51 | 0.367 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 223,812 | 2.238 | 135 | 139 | fits | 60,073 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 422,869 | 4.229 | 135 | 139 | fits | 58,691 | 155 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 149,212 | 1.492 | 20 | 200 | fits | 148,035 | 272 | 0.343 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 407,416 | 4.074 | 20 | 20 | fits | 102,405 | 106 | 0.467 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 387,212 | 3.872 | 20 | 24 | fits | 102,405 | 106 | 0.467 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 367,941 | 3.679 | 20 | 50 | fits | 102,405 | 106 | 0.467 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 939,541 | 9.395 | 20 | 20 | fits | 49,006 | 47 | 0.768 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 51,765 | 0.518 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 906,216 | 9.062 | 135 | 139 | fits | 24,571 | 52 | 0.478 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,469,271 | 14.693 | 135 | 139 | fits | 58,958 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,486,042 | 14.860 | 135 | 139 | fits | 58,958 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,502,742 | 15.027 | 135 | 139 | fits | 58,958 | 153 | 0.235 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 1,615,184 | 16.152 | 135 | 139 | fits | 52,595 | 152 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 1,632,607 | 16.326 | 135 | 139 | fits | 52,595 | 152 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 214,874 | 2.149 | 135 | 139 | fits | 53,256 | 111 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 232,982 | 2.330 | 135 | 139 | fits | 53,256 | 111 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,645,902 | 16.459 | 135 | 139 | fits | 52,595 | 152 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,818,775 | 18.188 | 135 | 139 | fits | 36,193 | 102 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,836,098 | 18.361 | 135 | 139 | fits | 36,193 | 102 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 321,678 | 3.217 | 135 | 139 | fits | 36,787 | 62 | 0.276 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 147,832 | 1.478 | 20 | 200 | fits | 144,041 | 264 | 0.325 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 371,360 | 3.714 | 20 | 20 | fits | 91,592 | 99 | 0.474 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 351,156 | 3.512 | 20 | 24 | fits | 91,592 | 99 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 331,885 | 3.319 | 20 | 50 | fits | 91,592 | 99 | 0.474 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 871,835 | 8.718 | 20 | 20 | fits | 45,117 | 40 | 0.765 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 893,818 | 8.938 | 135 | 139 | fits | 25,438 | 52 | 0.504 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,373,242 | 13.732 | 135 | 139 | fits | 57,931 | 153 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,389,792 | 13.898 | 135 | 139 | fits | 57,931 | 153 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,406,430 | 14.064 | 135 | 139 | fits | 57,931 | 153 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 1,518,444 | 15.184 | 135 | 139 | fits | 52,478 | 152 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 1,535,867 | 15.359 | 135 | 139 | fits | 52,478 | 152 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 235,782 | 2.358 | 135 | 139 | fits | 42,653 | 102 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 254,088 | 2.541 | 135 | 139 | fits | 42,653 | 102 | 0.259 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,549,162 | 15.492 | 135 | 139 | fits | 52,478 | 152 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,722,035 | 17.220 | 135 | 139 | fits | 36,165 | 102 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,739,330 | 17.393 | 135 | 139 | fits | 36,165 | 102 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 347,177 | 3.472 | 135 | 139 | fits | 37,001 | 61 | 0.281 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 149,102 | 1.491 | 20 | 200 | fits | 144,093 | 263 | 0.330 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 369,135 | 3.691 | 20 | 20 | fits | 88,121 | 90 | 0.473 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 348,931 | 3.489 | 20 | 24 | fits | 88,121 | 90 | 0.473 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 329,660 | 3.297 | 20 | 50 | fits | 88,121 | 90 | 0.473 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 873,403 | 8.734 | 20 | 20 | fits | 45,131 | 40 | 0.765 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 886,548 | 8.865 | 135 | 139 | fits | 25,260 | 52 | 0.500 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,286,063 | 12.861 | 135 | 139 | fits | 58,046 | 153 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,302,665 | 13.027 | 135 | 139 | fits | 58,046 | 153 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,319,303 | 13.193 | 135 | 139 | fits | 58,046 | 153 | 0.216 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 1,405,039 | 14.050 | 135 | 139 | fits | 52,469 | 152 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 1,422,462 | 14.225 | 135 | 139 | fits | 52,469 | 152 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 204,516 | 2.045 | 135 | 139 | fits | 53,599 | 111 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 222,624 | 2.226 | 135 | 139 | fits | 53,599 | 111 | 0.239 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,435,757 | 14.358 | 135 | 139 | fits | 52,469 | 152 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,595,472 | 15.955 | 135 | 139 | fits | 36,165 | 102 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,612,767 | 16.128 | 135 | 139 | fits | 36,165 | 102 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 447,838 | 4.478 | 135 | 139 | fits | 25,278 | 53 | 0.336 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 146,739 | 1.467 | 20 | 200 | fits | 147,044 | 271 | 0.315 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 396,659 | 3.967 | 20 | 20 | fits | 100,113 | 99 | 0.457 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 376,455 | 3.765 | 20 | 24 | fits | 100,113 | 99 | 0.457 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 357,184 | 3.572 | 20 | 50 | fits | 100,113 | 99 | 0.457 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 903,725 | 9.037 | 20 | 20 | fits | 45,117 | 40 | 0.765 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 825,308 | 8.253 | 135 | 139 | fits | 25,260 | 52 | 0.500 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,223,652 | 12.237 | 135 | 139 | fits | 58,112 | 153 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,240,321 | 12.403 | 135 | 139 | fits | 58,112 | 153 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,257,021 | 12.570 | 135 | 139 | fits | 58,112 | 153 | 0.218 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,395,277 | 13.953 | 135 | 139 | fits | 52,460 | 152 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,412,700 | 14.127 | 135 | 139 | fits | 52,460 | 152 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 200,068 | 2.001 | 135 | 139 | fits | 54,135 | 111 | 0.254 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 218,258 | 2.183 | 135 | 139 | fits | 54,135 | 111 | 0.254 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,425,995 | 14.260 | 135 | 139 | fits | 52,460 | 152 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,598,796 | 15.988 | 135 | 139 | fits | 36,165 | 102 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,616,091 | 16.161 | 135 | 139 | fits | 36,165 | 102 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 537,491 | 5.375 | 135 | 139 | fits | 25,386 | 52 | 0.351 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 462,722 | 4.627 | 20 | 200 | fits | 97,251 | 153 | 0.381 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 442,454 | 4.425 | 20 | 20 | fits | 97,251 | 153 | 0.381 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 299,613 | 2.996 | 20 | 24 | fits | 145,600 | 218 | 0.401 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 402,979 | 4.030 | 20 | 50 | fits | 97,251 | 153 | 0.381 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 945,260 | 9.453 | 20 | 20 | fits | 45,013 | 40 | 0.763 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,053,613 | 10.536 | 135 | 139 | fits | 58,435 | 152 | 0.277 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,071,355 | 10.714 | 135 | 139 | fits | 58,435 | 152 | 0.277 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,086,205 | 10.862 | 135 | 139 | fits | 58,435 | 152 | 0.277 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,201,671 | 12.017 | 135 | 139 | fits | 55,473 | 153 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 247,879 | 2.479 | 135 | 139 | fits | 23,999 | 52 | 0.457 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,218,774 | 12.188 | 135 | 139 | fits | 55,473 | 153 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,233,843 | 12.338 | 135 | 139 | fits | 55,473 | 153 | 0.167 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,399,165 | 13.992 | 135 | 139 | fits | 48,232 | 152 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,412,627 | 14.126 | 135 | 139 | fits | 48,232 | 152 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,424,225 | 14.242 | 135 | 139 | fits | 48,232 | 152 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,600,637 | 16.006 | 135 | 139 | fits | 39,539 | 103 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,617,361 | 16.174 | 135 | 139 | fits | 39,539 | 103 | 0.170 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 149,827 | 1.498 | 20 | 200 | fits | 147,368 | 272 | 0.339 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 402,552 | 4.026 | 20 | 20 | fits | 102,085 | 105 | 0.454 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 382,348 | 3.823 | 20 | 24 | fits | 102,085 | 105 | 0.454 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 363,077 | 3.631 | 20 | 50 | fits | 102,085 | 105 | 0.454 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 872,214 | 8.722 | 20 | 20 | fits | 45,249 | 40 | 0.765 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 763,288 | 7.633 | 135 | 139 | fits | 24,647 | 52 | 0.481 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,568,982 | 15.690 | 135 | 139 | fits | 59,213 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,585,759 | 15.858 | 135 | 139 | fits | 59,213 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,602,247 | 16.022 | 135 | 139 | fits | 59,213 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,715,572 | 17.156 | 135 | 139 | fits | 54,091 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,733,124 | 17.331 | 135 | 139 | fits | 54,091 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,747,475 | 17.475 | 135 | 139 | fits | 54,091 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,913,135 | 19.131 | 135 | 139 | fits | 48,308 | 152 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 1,926,597 | 19.266 | 135 | 139 | fits | 48,308 | 152 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 1,938,195 | 19.382 | 135 | 139 | fits | 48,308 | 152 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,114,732 | 21.147 | 135 | 139 | fits | 39,539 | 103 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,131,456 | 21.315 | 135 | 139 | fits | 39,539 | 103 | 0.170 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 148,964 | 1.490 | 20 | 200 | fits | 147,953 | 276 | 0.322 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 403,484 | 4.035 | 20 | 20 | fits | 103,240 | 111 | 0.454 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 383,280 | 3.833 | 20 | 24 | fits | 103,240 | 111 | 0.454 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 364,009 | 3.640 | 20 | 50 | fits | 103,240 | 111 | 0.454 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 871,480 | 8.715 | 20 | 20 | fits | 45,272 | 40 | 0.765 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 773,745 | 7.737 | 135 | 139 | fits | 24,489 | 52 | 0.474 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,575,412 | 15.754 | 135 | 139 | fits | 59,213 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,592,189 | 15.922 | 135 | 139 | fits | 59,213 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,608,677 | 16.087 | 135 | 139 | fits | 59,213 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,722,091 | 17.221 | 135 | 139 | fits | 54,091 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,739,643 | 17.396 | 135 | 139 | fits | 54,091 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,753,994 | 17.540 | 135 | 139 | fits | 54,091 | 152 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 1,919,654 | 19.197 | 135 | 139 | fits | 48,308 | 152 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 1,933,116 | 19.331 | 135 | 139 | fits | 48,308 | 152 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 1,944,714 | 19.447 | 135 | 139 | fits | 48,308 | 152 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,121,251 | 21.213 | 135 | 139 | fits | 39,539 | 103 | 0.170 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,137,975 | 21.380 | 135 | 139 | fits | 39,539 | 103 | 0.170 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 156,377 | 1.564 | 20 | 200 | fits | 148,806 | 270 | 0.331 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 405,464 | 4.055 | 20 | 20 | fits | 98,001 | 106 | 0.470 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 385,260 | 3.853 | 20 | 24 | fits | 98,001 | 106 | 0.470 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 365,989 | 3.660 | 20 | 50 | fits | 98,001 | 106 | 0.470 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 874,711 | 8.747 | 20 | 20 | fits | 45,272 | 40 | 0.765 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 916,142 | 9.161 | 135 | 139 | fits | 23,937 | 54 | 0.453 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,563,689 | 15.637 | 135 | 139 | fits | 59,237 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,580,472 | 15.805 | 135 | 139 | fits | 59,237 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,597,183 | 15.972 | 135 | 139 | fits | 59,237 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 1,722,502 | 17.225 | 135 | 139 | fits | 52,548 | 152 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 1,739,852 | 17.399 | 135 | 139 | fits | 52,548 | 152 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 214,888 | 2.149 | 135 | 139 | fits | 53,335 | 111 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 232,996 | 2.330 | 135 | 139 | fits | 53,335 | 111 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,753,220 | 17.532 | 135 | 139 | fits | 52,548 | 152 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,912,934 | 19.129 | 135 | 139 | fits | 36,165 | 102 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,930,302 | 19.303 | 135 | 139 | fits | 36,165 | 102 | 0.213 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 321,762 | 3.218 | 135 | 139 | fits | 36,787 | 62 | 0.276 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 149,082 | 1.491 | 20 | 200 | fits | 145,302 | 266 | 0.321 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 397,799 | 3.978 | 20 | 20 | fits | 92,995 | 111 | 0.477 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 377,595 | 3.776 | 20 | 24 | fits | 92,995 | 111 | 0.477 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 358,324 | 3.583 | 20 | 50 | fits | 92,995 | 111 | 0.477 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 864,745 | 8.647 | 20 | 20 | fits | 45,115 | 40 | 0.765 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

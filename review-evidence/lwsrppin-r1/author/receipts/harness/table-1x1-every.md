### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.acmp.if0` (notice-every-5) | 4.620 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-every-3.held.adp.if0` (notice-every-3) | 1.782 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.aecp.if0` (notice-every-5) | 4.418 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.maap.if0` (notice-every-5) | 4.225 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-3.held.srp.if0` (notice-every-3) | 9.315 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-4.mrpdu.periodic.if0` (notice-every-4) | 1.090 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 21.343 (21.559) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1866 | 0 | 148,184 (1.482) | fits |
| notice-every-1 | 1874 | 0 | 148,184 (1.482) | fits |
| notice-every-2 | 1865 | 0 | 148,877 (1.489) | fits |
| notice-every-3 | 1866 | 0 | 148,255 (1.483) | fits |
| notice-every-4 | 1873 | 0 | 149,447 (1.494) | fits |
| notice-every-5 | 1868 | 0 | 149,852 (1.499) | fits |
| notice-every-6 | 1867 | 0 | 148,332 (1.483) | fits |
| notice-every-7 | 1863 | 0 | 150,029 (1.500) | fits |
| notice-burst-0 | 1211 | 0 | 154,353 (1.544) | fits |
| notice-burst-1 | 1242 | 0 | 154,865 (1.549) | fits |
| notice-burst-2 | 1229 | 0 | 148,541 (1.485) | fits |
| notice-burst-3 | 1259 | 0 | 149,169 (1.492) | fits |
| notice-burst-4 | 1251 | 0 | 148,313 (1.483) | fits |
| notice-burst-5 | 1262 | 0 | 148,660 (1.487) | fits |
| notice-burst-6 | 1224 | 0 | 150,259 (1.503) | fits |
| notice-burst-7 | 1235 | 0 | 153,991 (1.540) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.134 | 130 | 16 | 2 | within |
| notice-every-0 | 8.311 | 130 | 16 | 2 | within |
| notice-every-0 | 1.948 | 130 | 16 | 2 | within |
| notice-every-0 | 2.128 | 130 | 16 | 2 | within |
| notice-every-0 | 3.978 | 130 | 16 | 2 | within |
| notice-every-0 | 4.160 | 130 | 16 | 2 | within |
| notice-every-0 | 5.985 | 130 | 16 | 2 | within |
| notice-every-0 | 6.162 | 130 | 16 | 2 | within |
| notice-every-0 | 8.443 | 130 | 16 | 2 | within |
| notice-every-0 | 9.931 | 130 | 16 | 2 | within |
| notice-every-0 | 2.304 | 130 | 16 | 2 | within |
| notice-every-0 | 4.337 | 130 | 16 | 2 | within |
| notice-every-1 | 2.093 | 130 | 16 | 2 | within |
| notice-every-1 | 2.273 | 130 | 16 | 2 | within |
| notice-every-1 | 4.084 | 130 | 16 | 2 | within |
| notice-every-1 | 4.262 | 130 | 16 | 2 | within |
| notice-every-1 | 6.112 | 130 | 16 | 2 | within |
| notice-every-1 | 6.288 | 130 | 16 | 2 | within |
| notice-every-1 | 8.150 | 130 | 16 | 2 | within |
| notice-every-1 | 8.323 | 130 | 16 | 2 | within |
| notice-every-1 | 2.412 | 130 | 16 | 2 | within |
| notice-every-1 | 4.395 | 130 | 16 | 2 | within |
| notice-every-1 | 6.460 | 130 | 16 | 2 | within |
| notice-every-1 | 8.489 | 130 | 16 | 2 | within |
| notice-every-2 | 1.896 | 130 | 16 | 2 | within |
| notice-every-2 | 2.075 | 130 | 16 | 2 | within |
| notice-every-2 | 3.886 | 130 | 16 | 2 | within |
| notice-every-2 | 4.064 | 130 | 16 | 2 | within |
| notice-every-2 | 5.953 | 130 | 16 | 2 | within |
| notice-every-2 | 6.129 | 130 | 16 | 2 | within |
| notice-every-2 | 7.826 | 130 | 16 | 2 | within |
| notice-every-2 | 7.998 | 130 | 16 | 2 | within |
| notice-every-2 | 2.213 | 130 | 16 | 2 | within |
| notice-every-2 | 4.196 | 130 | 16 | 2 | within |
| notice-every-2 | 6.300 | 130 | 16 | 2 | within |
| notice-every-2 | 8.164 | 130 | 16 | 2 | within |
| notice-every-3 | 3.971 | 130 | 16 | 2 | within |
| notice-every-3 | 4.149 | 130 | 16 | 2 | within |
| notice-every-3 | 5.842 | 130 | 16 | 2 | within |
| notice-every-3 | 6.020 | 130 | 16 | 2 | within |
| notice-every-3 | 7.849 | 130 | 16 | 2 | within |
| notice-every-3 | 8.026 | 130 | 16 | 2 | within |
| notice-every-3 | 1.893 | 130 | 16 | 2 | within |
| notice-every-3 | 2.077 | 130 | 16 | 2 | within |
| notice-every-3 | 4.286 | 130 | 16 | 2 | within |
| notice-every-3 | 6.150 | 130 | 16 | 2 | within |
| notice-every-3 | 2.251 | 130 | 16 | 2 | within |
| notice-every-3 | 8.196 | 130 | 16 | 2 | within |
| notice-every-4 | 3.929 | 130 | 16 | 2 | within |
| notice-every-4 | 4.108 | 130 | 16 | 2 | within |
| notice-every-4 | 5.969 | 130 | 16 | 2 | within |
| notice-every-4 | 6.147 | 130 | 16 | 2 | within |
| notice-every-4 | 7.974 | 130 | 16 | 2 | within |
| notice-every-4 | 8.151 | 130 | 16 | 2 | within |
| notice-every-4 | 1.892 | 130 | 16 | 2 | within |
| notice-every-4 | 2.076 | 130 | 16 | 2 | within |
| notice-every-4 | 4.245 | 130 | 16 | 2 | within |
| notice-every-4 | 6.277 | 130 | 16 | 2 | within |
| notice-every-4 | 2.250 | 130 | 16 | 2 | within |
| notice-every-4 | 8.321 | 130 | 16 | 2 | within |
| notice-every-5 | 5.937 | 130 | 16 | 2 | within |
| notice-every-5 | 6.115 | 130 | 16 | 2 | within |
| notice-every-5 | 7.955 | 130 | 16 | 2 | within |
| notice-every-5 | 8.133 | 130 | 16 | 2 | within |
| notice-every-5 | 1.892 | 130 | 16 | 2 | within |
| notice-every-5 | 2.077 | 130 | 16 | 2 | within |
| notice-every-5 | 3.923 | 130 | 16 | 2 | within |
| notice-every-5 | 4.103 | 130 | 16 | 2 | within |
| notice-every-5 | 6.249 | 130 | 16 | 2 | within |
| notice-every-5 | 8.260 | 130 | 16 | 2 | within |
| notice-every-5 | 2.254 | 130 | 16 | 2 | within |
| notice-every-5 | 4.277 | 130 | 16 | 2 | within |
| notice-every-6 | 6.122 | 130 | 16 | 2 | within |
| notice-every-6 | 6.300 | 130 | 16 | 2 | within |
| notice-every-6 | 7.978 | 130 | 16 | 2 | within |
| notice-every-6 | 8.156 | 130 | 16 | 2 | within |
| notice-every-6 | 1.892 | 130 | 16 | 2 | within |
| notice-every-6 | 2.077 | 130 | 16 | 2 | within |
| notice-every-6 | 3.922 | 130 | 16 | 2 | within |
| notice-every-6 | 4.102 | 130 | 16 | 2 | within |
| notice-every-6 | 6.434 | 130 | 16 | 2 | within |
| notice-every-6 | 8.284 | 130 | 16 | 2 | within |
| notice-every-6 | 2.255 | 130 | 16 | 2 | within |
| notice-every-6 | 4.276 | 130 | 16 | 2 | within |
| notice-every-7 | 8.007 | 130 | 16 | 2 | within |
| notice-every-7 | 8.183 | 130 | 16 | 2 | within |
| notice-every-7 | 2.043 | 130 | 16 | 2 | within |
| notice-every-7 | 2.223 | 130 | 16 | 2 | within |
| notice-every-7 | 3.823 | 130 | 16 | 2 | within |
| notice-every-7 | 4.004 | 130 | 16 | 2 | within |
| notice-every-7 | 6.014 | 130 | 16 | 2 | within |
| notice-every-7 | 6.191 | 130 | 16 | 2 | within |
| notice-every-7 | 8.315 | 130 | 16 | 2 | within |
| notice-every-7 | 9.801 | 130 | 16 | 2 | within |
| notice-every-7 | 2.399 | 130 | 16 | 2 | within |
| notice-every-7 | 4.181 | 130 | 16 | 2 | within |
| notice-burst-0 | 8.247 | 130 | 16 | 1 | within |
| notice-burst-0 | 14.408 | 130 | 16 | 1 | within |
| notice-burst-0 | 14.581 | 130 | 16 | 1 | within |
| notice-burst-0 | 14.751 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.260 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.443 | 130 | 16 | 1 | within |
| notice-burst-0 | 3.597 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.045 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.118 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.240 | 130 | 16 | 1 | within |
| notice-burst-0 | 16.409 | 130 | 16 | 1 | within |
| notice-burst-0 | 4.222 | 130 | 16 | 1 | within |
| notice-burst-1 | 8.247 | 130 | 16 | 0 | within |
| notice-burst-1 | 13.243 | 130 | 16 | 0 | within |
| notice-burst-1 | 13.415 | 130 | 16 | 0 | within |
| notice-burst-1 | 13.585 | 130 | 16 | 0 | within |
| notice-burst-1 | 2.170 | 130 | 16 | 0 | within |
| notice-burst-1 | 2.352 | 130 | 16 | 0 | within |
| notice-burst-1 | 2.966 | 130 | 16 | 0 | within |
| notice-burst-1 | 3.145 | 130 | 16 | 0 | within |
| notice-burst-1 | 14.956 | 130 | 16 | 0 | within |
| notice-burst-1 | 15.077 | 130 | 16 | 0 | within |
| notice-burst-1 | 15.246 | 130 | 16 | 0 | within |
| notice-burst-1 | 3.320 | 130 | 16 | 0 | within |
| notice-burst-2 | 12.253 | 130 | 16 | 0 | within |
| notice-burst-2 | 12.434 | 130 | 16 | 0 | within |
| notice-burst-2 | 12.588 | 130 | 16 | 0 | within |
| notice-burst-2 | 14.009 | 130 | 16 | 0 | within |
| notice-burst-2 | 1.937 | 130 | 16 | 0 | within |
| notice-burst-2 | 2.119 | 130 | 16 | 0 | within |
| notice-burst-2 | 4.449 | 130 | 16 | 0 | within |
| notice-burst-2 | 14.186 | 130 | 16 | 0 | within |
| notice-burst-2 | 14.317 | 130 | 16 | 0 | within |
| notice-burst-2 | 15.956 | 130 | 16 | 0 | within |
| notice-burst-2 | 16.130 | 130 | 16 | 0 | within |
| notice-burst-2 | 16.297 | 130 | 16 | 0 | within |
| notice-burst-3 | 11.427 | 130 | 16 | 1 | within |
| notice-burst-3 | 11.608 | 130 | 16 | 1 | within |
| notice-burst-3 | 11.761 | 130 | 16 | 1 | within |
| notice-burst-3 | 13.188 | 130 | 16 | 1 | within |
| notice-burst-3 | 13.353 | 130 | 16 | 1 | within |
| notice-burst-3 | 13.524 | 130 | 16 | 1 | within |
| notice-burst-3 | 3.570 | 130 | 16 | 1 | within |
| notice-burst-3 | 15.069 | 130 | 16 | 1 | within |
| notice-burst-3 | 15.206 | 130 | 16 | 1 | within |
| notice-burst-3 | 15.324 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.149 | 130 | 16 | 1 | within |
| notice-burst-3 | 17.320 | 130 | 16 | 1 | within |
| notice-burst-4 | 10.530 | 130 | 16 | 1 | within |
| notice-burst-4 | 10.710 | 130 | 16 | 1 | within |
| notice-burst-4 | 10.863 | 130 | 16 | 1 | within |
| notice-burst-4 | 12.138 | 130 | 16 | 1 | within |
| notice-burst-4 | 2.724 | 130 | 16 | 1 | within |
| notice-burst-4 | 12.315 | 130 | 16 | 1 | within |
| notice-burst-4 | 12.474 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.168 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.305 | 130 | 16 | 1 | within |
| notice-burst-4 | 14.423 | 130 | 16 | 1 | within |
| notice-burst-4 | 16.099 | 130 | 16 | 1 | within |
| notice-burst-4 | 16.270 | 130 | 16 | 1 | within |
| notice-burst-5 | 7.641 | 130 | 16 | 1 | within |
| notice-burst-5 | 15.476 | 130 | 16 | 1 | within |
| notice-burst-5 | 15.646 | 130 | 16 | 1 | within |
| notice-burst-5 | 15.815 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.225 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.399 | 130 | 16 | 1 | within |
| notice-burst-5 | 17.550 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.245 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.380 | 130 | 16 | 1 | within |
| notice-burst-5 | 19.498 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.173 | 130 | 16 | 1 | within |
| notice-burst-5 | 21.343 | 130 | 16 | 1 | within |
| notice-burst-6 | 6.541 | 130 | 16 | 0 | within |
| notice-burst-6 | 14.324 | 130 | 16 | 0 | within |
| notice-burst-6 | 14.495 | 130 | 16 | 0 | within |
| notice-burst-6 | 14.663 | 130 | 16 | 0 | within |
| notice-burst-6 | 15.921 | 130 | 16 | 0 | within |
| notice-burst-6 | 16.095 | 130 | 16 | 0 | within |
| notice-burst-6 | 16.247 | 130 | 16 | 0 | within |
| notice-burst-6 | 17.941 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.076 | 130 | 16 | 0 | within |
| notice-burst-6 | 18.194 | 130 | 16 | 0 | within |
| notice-burst-6 | 20.020 | 130 | 16 | 0 | within |
| notice-burst-6 | 20.190 | 130 | 16 | 0 | within |
| notice-burst-7 | 9.170 | 130 | 16 | 1 | within |
| notice-burst-7 | 15.332 | 130 | 16 | 1 | within |
| notice-burst-7 | 15.504 | 130 | 16 | 1 | within |
| notice-burst-7 | 15.675 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.102 | 130 | 16 | 1 | within |
| notice-burst-7 | 2.285 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.046 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.225 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.043 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.165 | 130 | 16 | 1 | within |
| notice-burst-7 | 17.334 | 130 | 16 | 1 | within |
| notice-burst-7 | 3.400 | 130 | 16 | 1 | within |

Latest: 21.343 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 402 | 95,686 (0.957) | 78,625 (0.786) |
| notice-every-1 | 402 | 95,686 (0.957) | 78,625 (0.786) |
| notice-every-2 | 402 | 95,686 (0.957) | 78,625 (0.786) |
| notice-every-3 | 402 | 95,686 (0.957) | 78,625 (0.786) |
| notice-every-4 | 402 | 95,686 (0.957) | 78,625 (0.786) |
| notice-every-5 | 402 | 95,686 (0.957) | 78,625 (0.786) |
| notice-every-6 | 402 | 95,686 (0.957) | 78,625 (0.786) |
| notice-every-7 | 402 | 95,686 (0.957) | 78,625 (0.786) |
| notice-burst-0 | 412 | 95,686 (0.957) | 78,625 (0.786) |
| notice-burst-1 | 412 | 95,686 (0.957) | 78,625 (0.786) |
| notice-burst-2 | 412 | 95,686 (0.957) | 78,625 (0.786) |
| notice-burst-3 | 412 | 95,686 (0.957) | 78,625 (0.786) |
| notice-burst-4 | 412 | 95,686 (0.957) | 78,625 (0.786) |
| notice-burst-5 | 412 | 95,686 (0.957) | 78,625 (0.786) |
| notice-burst-6 | 412 | 95,686 (0.957) | 78,625 (0.786) |
| notice-burst-7 | 412 | 95,686 (0.957) | 78,625 (0.786) |

Longest pass that carries a step: 95,686 CPU cycles (0.957 ms), notice-every-0; longest step: 78,625 (0.786 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 813,447 | 8.134 | 130 | 134 | fits | 55,824 | 152 | 0.239 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 831,082 | 8.311 | 130 | 134 | fits | 55,824 | 152 | 0.239 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 194,783 | 1.948 | 130 | 134 | fits | 62,252 | 155 | 0.210 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 212,835 | 2.128 | 130 | 134 | fits | 62,252 | 155 | 0.210 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 397,846 | 3.978 | 130 | 134 | fits | 60,972 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 415,985 | 4.160 | 130 | 134 | fits | 60,972 | 155 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 598,530 | 5.985 | 130 | 134 | fits | 41,829 | 103 | 0.259 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 616,209 | 6.162 | 130 | 134 | fits | 41,829 | 103 | 0.259 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 844,309 | 8.443 | 130 | 134 | fits | 55,824 | 152 | 0.239 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 993,055 | 9.931 | 130 | 134 | fits | 20,225 | 51 | 0.374 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 230,403 | 2.304 | 130 | 134 | fits | 62,252 | 155 | 0.210 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 433,673 | 4.337 | 130 | 134 | fits | 60,972 | 155 | 0.197 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 176,488 | 1.765 | 20 | 200 | fits | 147,708 | 288 | 0.239 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 451,584 | 4.516 | 20 | 20 | fits | 140,062 | 110 | 0.435 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 431,380 | 4.314 | 20 | 24 | fits | 140,062 | 110 | 0.435 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 116,745 | 1.167 | 20 | 50 | fits | 147,708 | 288 | 0.239 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 924,245 | 9.242 | 20 | 20 | fits | 56,190 | 33 | 0.737 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 108,422 | 1.084 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 209,311 | 2.093 | 130 | 134 | fits | 58,973 | 155 | 0.266 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 227,346 | 2.273 | 130 | 134 | fits | 58,973 | 155 | 0.266 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 408,422 | 4.084 | 130 | 134 | fits | 56,552 | 153 | 0.244 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 426,208 | 4.262 | 130 | 134 | fits | 56,552 | 153 | 0.244 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 611,172 | 6.112 | 130 | 134 | fits | 59,181 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 628,827 | 6.288 | 130 | 134 | fits | 59,181 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 815,033 | 8.150 | 130 | 134 | fits | 57,120 | 153 | 0.189 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 832,277 | 8.323 | 130 | 134 | fits | 57,120 | 153 | 0.189 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 241,221 | 2.412 | 130 | 134 | fits | 58,973 | 155 | 0.266 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 439,513 | 4.395 | 130 | 134 | fits | 56,552 | 153 | 0.244 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 645,968 | 6.460 | 130 | 134 | fits | 59,181 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 848,910 | 8.489 | 130 | 134 | fits | 57,120 | 153 | 0.189 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 163,787 | 1.638 | 20 | 200 | fits | 147,080 | 284 | 0.236 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 455,658 | 4.557 | 20 | 20 | fits | 140,140 | 110 | 0.436 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 435,454 | 4.355 | 20 | 24 | fits | 140,140 | 110 | 0.436 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 104,044 | 1.040 | 20 | 50 | fits | 147,080 | 284 | 0.236 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 911,868 | 9.119 | 20 | 20 | fits | 54,284 | 33 | 0.694 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 75,755 | 0.758 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 189,568 | 1.896 | 130 | 134 | fits | 57,970 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 207,534 | 2.075 | 130 | 134 | fits | 57,970 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 388,589 | 3.886 | 130 | 134 | fits | 56,364 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 406,375 | 4.064 | 130 | 134 | fits | 56,364 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 595,251 | 5.953 | 130 | 134 | fits | 59,047 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 612,906 | 6.129 | 130 | 134 | fits | 59,047 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 782,567 | 7.826 | 130 | 134 | fits | 57,219 | 155 | 0.190 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 799,811 | 7.998 | 130 | 134 | fits | 57,219 | 155 | 0.190 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 221,330 | 2.213 | 130 | 134 | fits | 57,970 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 419,626 | 4.196 | 130 | 134 | fits | 56,364 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 630,047 | 6.300 | 130 | 134 | fits | 59,047 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 816,444 | 8.164 | 130 | 134 | fits | 57,219 | 155 | 0.190 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 124,954 | 1.250 | 20 | 200 | fits | 125,401 | 163 | 0.158 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 450,884 | 4.509 | 20 | 20 | fits | 148,836 | 133 | 0.455 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 430,680 | 4.307 | 20 | 24 | fits | 148,836 | 133 | 0.455 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 411,409 | 4.114 | 20 | 50 | fits | 148,836 | 133 | 0.455 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 920,392 | 9.204 | 20 | 20 | fits | 57,509 | 39 | 0.727 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 103,401 | 1.034 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 397,053 | 3.971 | 130 | 134 | fits | 57,377 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 414,903 | 4.149 | 130 | 134 | fits | 57,377 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 584,230 | 5.842 | 130 | 134 | fits | 55,808 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 602,016 | 6.020 | 130 | 134 | fits | 55,808 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 784,940 | 7.849 | 130 | 134 | fits | 58,374 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 802,595 | 8.026 | 130 | 134 | fits | 58,374 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 189,334 | 1.893 | 130 | 134 | fits | 61,707 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 207,695 | 2.077 | 130 | 134 | fits | 61,707 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 428,592 | 4.286 | 130 | 134 | fits | 57,377 | 153 | 0.248 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 615,009 | 6.150 | 130 | 134 | fits | 55,808 | 153 | 0.242 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 225,119 | 2.251 | 130 | 134 | fits | 61,707 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 819,590 | 8.196 | 130 | 134 | fits | 58,374 | 153 | 0.193 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 178,221 | 1.782 | 20 | 200 | fits | 148,048 | 290 | 0.243 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 459,129 | 4.591 | 20 | 20 | fits | 141,314 | 116 | 0.437 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 438,925 | 4.389 | 20 | 24 | fits | 141,314 | 116 | 0.437 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 118,478 | 1.185 | 20 | 50 | fits | 148,048 | 290 | 0.243 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 931,454 | 9.315 | 20 | 20 | fits | 57,101 | 33 | 0.750 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 96,666 | 0.967 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 392,942 | 3.929 | 130 | 134 | fits | 57,511 | 155 | 0.249 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 410,792 | 4.108 | 130 | 134 | fits | 57,511 | 155 | 0.249 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 596,932 | 5.969 | 130 | 134 | fits | 55,714 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 614,718 | 6.147 | 130 | 134 | fits | 55,714 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 797,424 | 7.974 | 130 | 134 | fits | 58,374 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 815,079 | 8.151 | 130 | 134 | fits | 58,374 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 189,223 | 1.892 | 130 | 134 | fits | 61,801 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 207,584 | 2.076 | 130 | 134 | fits | 61,801 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 424,481 | 4.245 | 130 | 134 | fits | 57,511 | 155 | 0.249 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 627,711 | 6.277 | 130 | 134 | fits | 55,714 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 225,008 | 2.250 | 130 | 134 | fits | 61,801 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 832,074 | 8.321 | 130 | 134 | fits | 58,374 | 153 | 0.193 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 145,570 | 1.456 | 20 | 200 | fits | 148,061 | 270 | 0.200 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 455,473 | 4.555 | 20 | 20 | fits | 149,447 | 140 | 0.452 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 435,269 | 4.353 | 20 | 24 | fits | 149,447 | 140 | 0.452 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 415,998 | 4.160 | 20 | 50 | fits | 149,447 | 140 | 0.452 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 928,506 | 9.285 | 20 | 20 | fits | 58,308 | 39 | 0.738 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 108,964 | 1.090 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 593,723 | 5.937 | 130 | 134 | fits | 56,590 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 611,483 | 6.115 | 130 | 134 | fits | 56,590 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 795,468 | 7.955 | 130 | 134 | fits | 55,035 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 813,254 | 8.133 | 130 | 134 | fits | 55,035 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 189,175 | 1.892 | 130 | 134 | fits | 62,170 | 155 | 0.196 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 207,672 | 2.077 | 130 | 134 | fits | 62,170 | 155 | 0.196 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 392,275 | 3.923 | 130 | 134 | fits | 60,307 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 410,264 | 4.103 | 130 | 134 | fits | 60,307 | 153 | 0.193 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 624,896 | 6.249 | 130 | 134 | fits | 56,590 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 826,016 | 8.260 | 130 | 134 | fits | 55,035 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 225,398 | 2.254 | 130 | 134 | fits | 62,170 | 155 | 0.196 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 427,729 | 4.277 | 130 | 134 | fits | 60,307 | 153 | 0.193 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 152,577 | 1.526 | 20 | 200 | fits | 147,727 | 271 | 0.235 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 462,022 | 4.620 | 20 | 20 | fits | 149,852 | 139 | 0.455 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 441,818 | 4.418 | 20 | 24 | fits | 149,852 | 139 | 0.455 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 422,547 | 4.225 | 20 | 50 | fits | 149,852 | 139 | 0.455 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 929,405 | 9.294 | 20 | 20 | fits | 56,551 | 33 | 0.740 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 99,041 | 0.990 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 612,217 | 6.122 | 130 | 134 | fits | 56,590 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 629,977 | 6.300 | 130 | 134 | fits | 56,590 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 797,832 | 7.978 | 130 | 134 | fits | 55,035 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 815,618 | 8.156 | 130 | 134 | fits | 55,035 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 189,232 | 1.892 | 130 | 134 | fits | 62,170 | 155 | 0.196 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 207,729 | 2.077 | 130 | 134 | fits | 62,170 | 155 | 0.196 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 392,172 | 3.922 | 130 | 134 | fits | 60,441 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 410,161 | 4.102 | 130 | 134 | fits | 60,441 | 155 | 0.194 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 643,390 | 6.434 | 130 | 134 | fits | 56,590 | 153 | 0.241 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 828,380 | 8.284 | 130 | 134 | fits | 55,035 | 151 | 0.242 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 225,455 | 2.255 | 130 | 134 | fits | 62,170 | 155 | 0.196 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 427,626 | 4.276 | 130 | 134 | fits | 60,441 | 155 | 0.194 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 166,740 | 1.667 | 20 | 200 | fits | 146,512 | 286 | 0.234 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 454,022 | 4.540 | 20 | 20 | fits | 142,856 | 122 | 0.438 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 433,818 | 4.338 | 20 | 24 | fits | 142,856 | 122 | 0.438 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 106,997 | 1.070 | 20 | 50 | fits | 146,512 | 286 | 0.234 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 920,118 | 9.201 | 20 | 20 | fits | 56,491 | 33 | 0.739 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 107,744 | 1.077 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 800,683 | 8.007 | 130 | 134 | fits | 55,734 | 152 | 0.239 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 818,318 | 8.183 | 130 | 134 | fits | 55,734 | 152 | 0.239 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 204,259 | 2.043 | 130 | 134 | fits | 64,051 | 153 | 0.218 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 222,311 | 2.223 | 130 | 134 | fits | 64,051 | 153 | 0.218 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 382,286 | 3.823 | 130 | 134 | fits | 60,822 | 155 | 0.196 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 400,425 | 4.004 | 130 | 134 | fits | 60,822 | 155 | 0.196 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 601,402 | 6.014 | 130 | 134 | fits | 41,786 | 103 | 0.257 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 619,081 | 6.191 | 130 | 134 | fits | 41,786 | 103 | 0.257 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 831,545 | 8.315 | 130 | 134 | fits | 55,734 | 152 | 0.239 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 980,139 | 9.801 | 130 | 134 | fits | 20,225 | 51 | 0.374 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 239,879 | 2.399 | 130 | 134 | fits | 64,051 | 153 | 0.218 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 418,113 | 4.181 | 130 | 134 | fits | 60,822 | 155 | 0.196 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 149,844 | 1.498 | 20 | 200 | fits | 150,029 | 275 | 0.215 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 456,266 | 4.563 | 20 | 20 | fits | 147,297 | 127 | 0.459 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 436,062 | 4.361 | 20 | 24 | fits | 147,297 | 127 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 416,791 | 4.168 | 20 | 50 | fits | 147,297 | 127 | 0.459 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 930,580 | 9.306 | 20 | 20 | fits | 56,531 | 33 | 0.743 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 100,847 | 1.008 | 49 | 49 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 824,719 | 8.247 | 130 | 134 | fits | 25,802 | 52 | 0.471 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,440,843 | 14.408 | 130 | 134 | fits | 61,302 | 153 | 0.253 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,458,086 | 14.581 | 130 | 134 | fits | 61,302 | 153 | 0.253 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,475,135 | 14.751 | 130 | 134 | fits | 61,302 | 153 | 0.253 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 326,025 | 3.260 | 130 | 134 | fits | 58,924 | 152 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 344,267 | 3.443 | 130 | 134 | fits | 58,924 | 152 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 359,682 | 3.597 | 130 | 134 | fits | 58,924 | 152 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 404,483 | 4.045 | 130 | 134 | fits | 62,587 | 118 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,611,828 | 16.118 | 130 | 134 | fits | 50,178 | 152 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,623,959 | 16.240 | 130 | 134 | fits | 50,178 | 152 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,640,850 | 16.409 | 130 | 134 | fits | 50,178 | 152 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 422,195 | 4.222 | 130 | 134 | fits | 62,587 | 118 | 0.248 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 162,575 | 1.626 | 20 | 200 | fits | 148,995 | 267 | 0.228 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 445,380 | 4.454 | 20 | 20 | fits | 122,918 | 116 | 0.487 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 425,176 | 4.252 | 20 | 24 | fits | 122,918 | 116 | 0.487 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 405,905 | 4.059 | 20 | 50 | fits | 122,918 | 116 | 0.487 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 849,974 | 8.500 | 20 | 20 | fits | 51,212 | 26 | 0.696 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 824,654 | 8.247 | 130 | 134 | fits | 26,612 | 51 | 0.491 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,324,277 | 13.243 | 130 | 134 | fits | 61,077 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,341,477 | 13.415 | 130 | 134 | fits | 61,077 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,358,526 | 13.585 | 130 | 134 | fits | 61,077 | 153 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 217,005 | 2.170 | 130 | 134 | fits | 43,992 | 102 | 0.258 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 235,247 | 2.352 | 130 | 134 | fits | 43,992 | 102 | 0.258 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 296,644 | 2.966 | 130 | 134 | fits | 72,158 | 162 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 314,479 | 3.145 | 130 | 134 | fits | 72,158 | 162 | 0.178 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,495,554 | 14.956 | 130 | 134 | fits | 50,163 | 152 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,507,671 | 15.077 | 130 | 134 | fits | 50,163 | 152 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 1,524,562 | 15.246 | 130 | 134 | fits | 50,163 | 152 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 332,047 | 3.320 | 130 | 134 | fits | 72,158 | 162 | 0.178 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 146,837 | 1.468 | 20 | 200 | fits | 148,224 | 268 | 0.213 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 405,299 | 4.053 | 20 | 20 | fits | 123,865 | 111 | 0.450 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 385,095 | 3.851 | 20 | 24 | fits | 123,865 | 111 | 0.450 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 365,824 | 3.658 | 20 | 50 | fits | 123,865 | 111 | 0.450 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 842,901 | 8.429 | 20 | 20 | fits | 51,323 | 26 | 0.697 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 1,225,275 | 12.253 | 130 | 134 | fits | 60,680 | 153 | 0.286 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,243,360 | 12.434 | 130 | 134 | fits | 60,680 | 153 | 0.286 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,258,844 | 12.588 | 130 | 134 | fits | 60,680 | 153 | 0.286 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,400,920 | 14.009 | 130 | 134 | fits | 55,609 | 153 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 193,662 | 1.937 | 130 | 134 | fits | 56,193 | 111 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 211,904 | 2.119 | 130 | 134 | fits | 56,193 | 111 | 0.242 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 444,851 | 4.449 | 130 | 134 | fits | 26,153 | 52 | 0.487 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 1,418,582 | 14.186 | 130 | 134 | fits | 55,609 | 153 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,431,713 | 14.317 | 130 | 134 | fits | 55,609 | 153 | 0.186 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,595,596 | 15.956 | 130 | 134 | fits | 54,102 | 152 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,613,013 | 16.130 | 130 | 134 | fits | 54,102 | 152 | 0.163 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 1,629,657 | 16.297 | 130 | 134 | fits | 54,102 | 152 | 0.163 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 148,551 | 1.486 | 20 | 200 | fits | 148,541 | 274 | 0.218 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 438,899 | 4.389 | 20 | 20 | fits | 139,181 | 117 | 0.447 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 418,695 | 4.187 | 20 | 24 | fits | 139,181 | 117 | 0.447 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 399,424 | 3.994 | 20 | 50 | fits | 139,181 | 117 | 0.447 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 846,091 | 8.461 | 20 | 20 | fits | 51,370 | 26 | 0.696 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,142,709 | 11.427 | 130 | 134 | fits | 60,520 | 152 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,160,756 | 11.608 | 130 | 134 | fits | 60,520 | 152 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,176,068 | 11.761 | 130 | 134 | fits | 60,520 | 152 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,318,770 | 13.188 | 130 | 134 | fits | 58,857 | 153 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,335,336 | 13.353 | 130 | 134 | fits | 58,857 | 153 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,352,404 | 13.524 | 130 | 134 | fits | 58,857 | 153 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 356,951 | 3.570 | 130 | 134 | fits | 26,565 | 52 | 0.491 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,506,945 | 15.069 | 130 | 134 | fits | 50,158 | 152 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,520,628 | 15.206 | 130 | 134 | fits | 50,158 | 152 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,532,419 | 15.324 | 130 | 134 | fits | 50,158 | 152 | 0.198 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,714,898 | 17.149 | 130 | 134 | fits | 41,175 | 103 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 1,732,015 | 17.320 | 130 | 134 | fits | 41,175 | 103 | 0.180 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 148,412 | 1.484 | 20 | 200 | fits | 149,169 | 274 | 0.225 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 441,994 | 4.420 | 20 | 20 | fits | 141,081 | 123 | 0.445 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 421,790 | 4.218 | 20 | 24 | fits | 141,081 | 123 | 0.445 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 402,519 | 4.025 | 20 | 50 | fits | 141,081 | 123 | 0.445 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 851,495 | 8.515 | 20 | 20 | fits | 51,449 | 26 | 0.696 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,052,950 | 10.530 | 130 | 134 | fits | 60,492 | 152 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,070,997 | 10.710 | 130 | 134 | fits | 60,492 | 152 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,086,323 | 10.863 | 130 | 134 | fits | 60,492 | 152 | 0.285 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,213,831 | 12.138 | 130 | 134 | fits | 58,657 | 153 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 272,417 | 2.724 | 130 | 134 | fits | 26,472 | 52 | 0.489 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,231,485 | 12.315 | 130 | 134 | fits | 58,657 | 153 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,247,403 | 12.474 | 130 | 134 | fits | 58,657 | 153 | 0.203 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,416,836 | 14.168 | 130 | 134 | fits | 50,010 | 152 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,430,519 | 14.305 | 130 | 134 | fits | 50,010 | 152 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,442,310 | 14.423 | 130 | 134 | fits | 50,010 | 152 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 1,609,917 | 16.099 | 130 | 134 | fits | 41,185 | 103 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 1,627,034 | 16.270 | 130 | 134 | fits | 41,185 | 103 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 164,501 | 1.645 | 20 | 200 | fits | 148,313 | 271 | 0.244 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 453,198 | 4.532 | 20 | 20 | fits | 135,317 | 116 | 0.460 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 432,994 | 4.330 | 20 | 24 | fits | 135,317 | 116 | 0.460 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 413,723 | 4.137 | 20 | 50 | fits | 135,317 | 116 | 0.460 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 862,314 | 8.623 | 20 | 20 | fits | 51,500 | 26 | 0.697 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 764,070 | 7.641 | 130 | 134 | fits | 27,198 | 52 | 0.502 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,547,588 | 15.476 | 130 | 134 | fits | 61,129 | 153 | 0.251 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,564,611 | 15.646 | 130 | 134 | fits | 61,129 | 153 | 0.251 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,581,464 | 15.815 | 130 | 134 | fits | 61,129 | 153 | 0.251 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,722,491 | 17.225 | 130 | 134 | fits | 56,424 | 152 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 1,739,871 | 17.399 | 130 | 134 | fits | 56,424 | 152 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,755,049 | 17.550 | 130 | 134 | fits | 56,424 | 152 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,924,473 | 19.245 | 130 | 134 | fits | 49,873 | 152 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 1,937,996 | 19.380 | 130 | 134 | fits | 49,873 | 152 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 1,949,787 | 19.498 | 130 | 134 | fits | 49,873 | 152 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,117,322 | 21.173 | 130 | 134 | fits | 41,025 | 103 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,134,279 | 21.343 | 130 | 134 | fits | 41,025 | 103 | 0.180 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 149,245 | 1.492 | 20 | 200 | fits | 148,660 | 276 | 0.216 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 444,548 | 4.445 | 20 | 20 | fits | 141,510 | 129 | 0.440 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 424,344 | 4.243 | 20 | 24 | fits | 141,510 | 129 | 0.440 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 405,073 | 4.051 | 20 | 50 | fits | 141,510 | 129 | 0.440 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 850,554 | 8.506 | 20 | 20 | fits | 51,449 | 26 | 0.696 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 654,122 | 6.541 | 130 | 134 | fits | 27,117 | 52 | 0.500 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,432,428 | 14.324 | 130 | 134 | fits | 61,169 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,449,451 | 14.495 | 130 | 134 | fits | 61,169 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,466,304 | 14.663 | 130 | 134 | fits | 61,169 | 153 | 0.252 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,592,131 | 15.921 | 130 | 134 | fits | 56,424 | 152 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 1,609,511 | 16.095 | 130 | 134 | fits | 56,424 | 152 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,624,689 | 16.247 | 130 | 134 | fits | 56,424 | 152 | 0.232 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 1,794,113 | 17.941 | 130 | 134 | fits | 49,873 | 152 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 1,807,636 | 18.076 | 130 | 134 | fits | 49,873 | 152 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 1,819,427 | 18.194 | 130 | 134 | fits | 49,873 | 152 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,002,004 | 20.020 | 130 | 134 | fits | 41,025 | 103 | 0.180 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,018,961 | 20.190 | 130 | 134 | fits | 41,025 | 103 | 0.180 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 157,777 | 1.578 | 20 | 200 | fits | 150,259 | 274 | 0.214 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 446,684 | 4.467 | 20 | 20 | fits | 135,320 | 118 | 0.459 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 426,480 | 4.265 | 20 | 24 | fits | 135,320 | 118 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 407,209 | 4.072 | 20 | 50 | fits | 135,320 | 118 | 0.459 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 853,756 | 8.538 | 20 | 20 | fits | 51,450 | 26 | 0.696 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 916,980 | 9.170 | 130 | 134 | fits | 25,695 | 52 | 0.467 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,533,186 | 15.332 | 130 | 134 | fits | 61,311 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,550,428 | 15.504 | 130 | 134 | fits | 61,311 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,567,477 | 15.675 | 130 | 134 | fits | 61,311 | 153 | 0.255 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 210,247 | 2.102 | 130 | 134 | fits | 56,308 | 111 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 228,489 | 2.285 | 130 | 134 | fits | 56,308 | 111 | 0.247 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 304,648 | 3.046 | 130 | 134 | fits | 71,956 | 162 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 322,483 | 3.225 | 130 | 134 | fits | 71,956 | 162 | 0.172 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,704,336 | 17.043 | 130 | 134 | fits | 50,265 | 152 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 1,716,467 | 17.165 | 130 | 134 | fits | 50,265 | 152 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 1,733,358 | 17.334 | 130 | 134 | fits | 50,265 | 152 | 0.190 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 339,972 | 3.400 | 130 | 134 | fits | 71,956 | 162 | 0.172 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 156,515 | 1.565 | 20 | 200 | fits | 149,908 | 271 | 0.213 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 438,791 | 4.388 | 20 | 20 | fits | 122,858 | 116 | 0.487 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 418,587 | 4.186 | 20 | 24 | fits | 122,858 | 116 | 0.487 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 399,316 | 3.993 | 20 | 50 | fits | 122,858 | 116 | 0.487 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 843,517 | 8.435 | 20 | 20 | fits | 51,212 | 26 | 0.696 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

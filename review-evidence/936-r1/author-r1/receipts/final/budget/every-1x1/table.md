Original file: <scratch>/budget/final/every-1x1/table.md
Original size: 55388 bytes
Original sha256: 2ef1fff5d78a27307ef596e9aa20bbff627ec9aa5d179e51c4f30e15241709ce

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.acmp.if0` (notice-burst-2) | 5.466 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.adp.if0` (notice-burst-2) | 5.669 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.aecp.if0` (notice-burst-0) | 4.688 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.maap.if0` (notice-burst-2) | 5.071 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-2.held.srp.if0` (notice-burst-2) | 11.965 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-5.mrpdu.periodic.if0` (notice-every-5) | 0.959 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 27.073 (27.294) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1513 | 0 | 156,080 (1.561) | fits |
| notice-every-1 | 1501 | 0 | 156,052 (1.561) | fits |
| notice-every-2 | 1509 | 0 | 156,052 (1.561) | fits |
| notice-every-3 | 1501 | 0 | 157,071 (1.571) | fits |
| notice-every-4 | 1501 | 0 | 157,035 (1.570) | fits |
| notice-every-5 | 1504 | 0 | 156,983 (1.570) | fits |
| notice-every-6 | 1503 | 0 | 157,035 (1.570) | fits |
| notice-every-7 | 1498 | 0 | 157,035 (1.570) | fits |
| notice-burst-0 | 1060 | 0 | 155,783 (1.558) | fits |
| notice-burst-1 | 1024 | 0 | 156,365 (1.564) | fits |
| notice-burst-2 | 1044 | 0 | 155,988 (1.560) | fits |
| notice-burst-3 | 1076 | 0 | 159,978 (1.600) | fits |
| notice-burst-4 | 1014 | 0 | 155,695 (1.557) | fits |
| notice-burst-5 | 1044 | 0 | 155,783 (1.558) | fits |
| notice-burst-6 | 1044 | 0 | 155,783 (1.558) | fits |
| notice-burst-7 | 1053 | 0 | 155,695 (1.557) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 8.013 | 140 | 16 | 2 | within |
| notice-every-0 | 8.209 | 140 | 16 | 2 | within |
| notice-every-0 | 1.908 | 140 | 16 | 2 | within |
| notice-every-0 | 2.115 | 140 | 16 | 2 | within |
| notice-every-0 | 3.874 | 140 | 16 | 2 | within |
| notice-every-0 | 4.074 | 140 | 16 | 2 | within |
| notice-every-0 | 5.928 | 140 | 16 | 2 | within |
| notice-every-0 | 6.127 | 140 | 16 | 2 | within |
| notice-every-0 | 9.794 | 140 | 16 | 2 | within |
| notice-every-0 | 9.964 | 140 | 16 | 2 | within |
| notice-every-0 | 11.922 | 140 | 16 | 2 | within |
| notice-every-0 | 12.119 | 140 | 16 | 2 | within |
| notice-every-1 | 2.087 | 140 | 16 | 2 | within |
| notice-every-1 | 2.288 | 140 | 16 | 2 | within |
| notice-every-1 | 4.035 | 140 | 16 | 2 | within |
| notice-every-1 | 4.237 | 140 | 16 | 2 | within |
| notice-every-1 | 5.900 | 140 | 16 | 2 | within |
| notice-every-1 | 6.097 | 140 | 16 | 2 | within |
| notice-every-1 | 7.916 | 140 | 16 | 2 | within |
| notice-every-1 | 8.112 | 140 | 16 | 2 | within |
| notice-every-1 | 9.897 | 140 | 16 | 2 | within |
| notice-every-1 | 10.067 | 140 | 16 | 2 | within |
| notice-every-1 | 12.024 | 140 | 16 | 2 | within |
| notice-every-1 | 12.222 | 140 | 16 | 2 | within |
| notice-every-2 | 2.087 | 140 | 16 | 2 | within |
| notice-every-2 | 2.288 | 140 | 16 | 2 | within |
| notice-every-2 | 4.035 | 140 | 16 | 2 | within |
| notice-every-2 | 4.237 | 140 | 16 | 2 | within |
| notice-every-2 | 5.900 | 140 | 16 | 2 | within |
| notice-every-2 | 6.097 | 140 | 16 | 2 | within |
| notice-every-2 | 7.916 | 140 | 16 | 2 | within |
| notice-every-2 | 8.112 | 140 | 16 | 2 | within |
| notice-every-2 | 9.897 | 140 | 16 | 2 | within |
| notice-every-2 | 10.067 | 140 | 16 | 2 | within |
| notice-every-2 | 11.842 | 140 | 16 | 2 | within |
| notice-every-2 | 12.040 | 140 | 16 | 2 | within |
| notice-every-3 | 5.891 | 140 | 16 | 2 | within |
| notice-every-3 | 6.089 | 140 | 16 | 2 | within |
| notice-every-3 | 7.929 | 140 | 16 | 2 | within |
| notice-every-3 | 8.128 | 140 | 16 | 2 | within |
| notice-every-3 | 1.856 | 140 | 16 | 2 | within |
| notice-every-3 | 2.061 | 140 | 16 | 2 | within |
| notice-every-3 | 3.821 | 140 | 16 | 2 | within |
| notice-every-3 | 4.025 | 140 | 16 | 2 | within |
| notice-every-3 | 9.915 | 140 | 16 | 2 | within |
| notice-every-3 | 10.085 | 140 | 16 | 2 | within |
| notice-every-3 | 11.861 | 140 | 16 | 2 | within |
| notice-every-3 | 12.058 | 140 | 16 | 2 | within |
| notice-every-4 | 5.918 | 140 | 16 | 2 | within |
| notice-every-4 | 6.115 | 140 | 16 | 2 | within |
| notice-every-4 | 7.954 | 140 | 16 | 2 | within |
| notice-every-4 | 8.154 | 140 | 16 | 2 | within |
| notice-every-4 | 2.090 | 140 | 16 | 2 | within |
| notice-every-4 | 2.296 | 140 | 16 | 2 | within |
| notice-every-4 | 4.032 | 140 | 16 | 2 | within |
| notice-every-4 | 4.235 | 140 | 16 | 2 | within |
| notice-every-4 | 9.943 | 140 | 16 | 2 | within |
| notice-every-4 | 10.113 | 140 | 16 | 2 | within |
| notice-every-4 | 11.889 | 140 | 16 | 2 | within |
| notice-every-4 | 12.086 | 140 | 16 | 2 | within |
| notice-every-5 | 5.918 | 140 | 16 | 2 | within |
| notice-every-5 | 6.115 | 140 | 16 | 2 | within |
| notice-every-5 | 7.954 | 140 | 16 | 2 | within |
| notice-every-5 | 8.154 | 140 | 16 | 2 | within |
| notice-every-5 | 2.090 | 140 | 16 | 2 | within |
| notice-every-5 | 2.296 | 140 | 16 | 2 | within |
| notice-every-5 | 4.032 | 140 | 16 | 2 | within |
| notice-every-5 | 4.235 | 140 | 16 | 2 | within |
| notice-every-5 | 9.943 | 140 | 16 | 2 | within |
| notice-every-5 | 10.113 | 140 | 16 | 2 | within |
| notice-every-5 | 11.889 | 140 | 16 | 2 | within |
| notice-every-5 | 12.086 | 140 | 16 | 2 | within |
| notice-every-6 | 5.891 | 140 | 16 | 2 | within |
| notice-every-6 | 6.089 | 140 | 16 | 2 | within |
| notice-every-6 | 7.928 | 140 | 16 | 2 | within |
| notice-every-6 | 8.128 | 140 | 16 | 2 | within |
| notice-every-6 | 1.856 | 140 | 16 | 2 | within |
| notice-every-6 | 2.061 | 140 | 16 | 2 | within |
| notice-every-6 | 3.821 | 140 | 16 | 2 | within |
| notice-every-6 | 4.025 | 140 | 16 | 2 | within |
| notice-every-6 | 9.915 | 140 | 16 | 2 | within |
| notice-every-6 | 10.085 | 140 | 16 | 2 | within |
| notice-every-6 | 11.861 | 140 | 16 | 2 | within |
| notice-every-6 | 12.058 | 140 | 16 | 2 | within |
| notice-every-7 | 8.015 | 140 | 16 | 2 | within |
| notice-every-7 | 8.212 | 140 | 16 | 2 | within |
| notice-every-7 | 1.908 | 140 | 16 | 2 | within |
| notice-every-7 | 2.115 | 140 | 16 | 2 | within |
| notice-every-7 | 5.930 | 140 | 16 | 2 | within |
| notice-every-7 | 6.129 | 140 | 16 | 2 | within |
| notice-every-7 | 3.875 | 140 | 16 | 2 | within |
| notice-every-7 | 4.078 | 140 | 16 | 2 | within |
| notice-every-7 | 9.797 | 140 | 16 | 2 | within |
| notice-every-7 | 9.967 | 140 | 16 | 2 | within |
| notice-every-7 | 11.924 | 140 | 16 | 2 | within |
| notice-every-7 | 12.121 | 140 | 16 | 2 | within |
| notice-burst-0 | 8.311 | 140 | 16 | 0 | within |
| notice-burst-0 | 16.769 | 140 | 16 | 0 | within |
| notice-burst-0 | 2.203 | 140 | 16 | 0 | within |
| notice-burst-0 | 2.408 | 140 | 16 | 0 | within |
| notice-burst-0 | 3.341 | 140 | 16 | 0 | within |
| notice-burst-0 | 3.541 | 140 | 16 | 0 | within |
| notice-burst-0 | 4.539 | 140 | 16 | 0 | within |
| notice-burst-0 | 4.739 | 140 | 16 | 0 | within |
| notice-burst-0 | 16.954 | 140 | 16 | 0 | within |
| notice-burst-0 | 17.983 | 140 | 16 | 0 | within |
| notice-burst-0 | 18.177 | 140 | 16 | 0 | within |
| notice-burst-0 | 6.562 | 140 | 16 | 0 | within |
| notice-burst-1 | 9.480 | 140 | 16 | 1 | within |
| notice-burst-1 | 16.535 | 140 | 16 | 1 | within |
| notice-burst-1 | 16.753 | 140 | 16 | 1 | within |
| notice-burst-1 | 18.177 | 140 | 16 | 1 | within |
| notice-burst-1 | 3.641 | 140 | 16 | 1 | within |
| notice-burst-1 | 3.848 | 140 | 16 | 1 | within |
| notice-burst-1 | 4.309 | 140 | 16 | 1 | within |
| notice-burst-1 | 4.510 | 140 | 16 | 1 | within |
| notice-burst-1 | 18.360 | 140 | 16 | 1 | within |
| notice-burst-1 | 20.266 | 140 | 16 | 1 | within |
| notice-burst-1 | 20.461 | 140 | 16 | 1 | within |
| notice-burst-1 | 6.286 | 140 | 16 | 1 | within |
| notice-burst-2 | 8.858 | 140 | 16 | 1 | within |
| notice-burst-2 | 15.964 | 140 | 16 | 1 | within |
| notice-burst-2 | 16.181 | 140 | 16 | 1 | within |
| notice-burst-2 | 17.247 | 140 | 16 | 1 | within |
| notice-burst-2 | 3.201 | 140 | 16 | 1 | within |
| notice-burst-2 | 3.409 | 140 | 16 | 1 | within |
| notice-burst-2 | 3.662 | 140 | 16 | 1 | within |
| notice-burst-2 | 3.863 | 140 | 16 | 1 | within |
| notice-burst-2 | 17.429 | 140 | 16 | 1 | within |
| notice-burst-2 | 19.156 | 140 | 16 | 1 | within |
| notice-burst-2 | 19.351 | 140 | 16 | 1 | within |
| notice-burst-2 | 5.670 | 140 | 16 | 1 | within |
| notice-burst-3 | 14.243 | 140 | 16 | 2 | within |
| notice-burst-3 | 14.448 | 140 | 16 | 2 | within |
| notice-burst-3 | 16.276 | 140 | 16 | 2 | within |
| notice-burst-3 | 16.475 | 140 | 16 | 2 | within |
| notice-burst-3 | 2.251 | 140 | 16 | 2 | within |
| notice-burst-3 | 2.456 | 140 | 16 | 2 | within |
| notice-burst-3 | 4.256 | 140 | 16 | 2 | within |
| notice-burst-3 | 18.270 | 140 | 16 | 2 | within |
| notice-burst-3 | 18.451 | 140 | 16 | 2 | within |
| notice-burst-3 | 20.206 | 140 | 16 | 2 | within |
| notice-burst-3 | 20.399 | 140 | 16 | 2 | within |
| notice-burst-3 | 22.222 | 140 | 16 | 2 | within |
| notice-burst-4 | 12.366 | 140 | 16 | 0 | within |
| notice-burst-4 | 12.570 | 140 | 16 | 0 | within |
| notice-burst-4 | 2.302 | 140 | 16 | 0 | within |
| notice-burst-4 | 13.831 | 140 | 16 | 0 | within |
| notice-burst-4 | 14.031 | 140 | 16 | 0 | within |
| notice-burst-4 | 15.829 | 140 | 16 | 0 | within |
| notice-burst-4 | 16.029 | 140 | 16 | 0 | within |
| notice-burst-4 | 17.820 | 140 | 16 | 0 | within |
| notice-burst-4 | 18.001 | 140 | 16 | 0 | within |
| notice-burst-4 | 19.810 | 140 | 16 | 0 | within |
| notice-burst-4 | 20.005 | 140 | 16 | 0 | within |
| notice-burst-4 | 21.779 | 140 | 16 | 0 | within |
| notice-burst-5 | 7.601 | 140 | 16 | 1 | within |
| notice-burst-5 | 17.639 | 140 | 16 | 1 | within |
| notice-burst-5 | 17.858 | 140 | 16 | 1 | within |
| notice-burst-5 | 19.122 | 140 | 16 | 1 | within |
| notice-burst-5 | 19.324 | 140 | 16 | 1 | within |
| notice-burst-5 | 21.122 | 140 | 16 | 1 | within |
| notice-burst-5 | 21.322 | 140 | 16 | 1 | within |
| notice-burst-5 | 23.115 | 140 | 16 | 1 | within |
| notice-burst-5 | 23.295 | 140 | 16 | 1 | within |
| notice-burst-5 | 25.104 | 140 | 16 | 1 | within |
| notice-burst-5 | 25.299 | 140 | 16 | 1 | within |
| notice-burst-5 | 27.073 | 140 | 16 | 1 | within |
| notice-burst-6 | 7.420 | 140 | 16 | 0 | within |
| notice-burst-6 | 17.428 | 140 | 16 | 0 | within |
| notice-burst-6 | 17.648 | 140 | 16 | 0 | within |
| notice-burst-6 | 18.910 | 140 | 16 | 0 | within |
| notice-burst-6 | 19.112 | 140 | 16 | 0 | within |
| notice-burst-6 | 20.910 | 140 | 16 | 0 | within |
| notice-burst-6 | 21.109 | 140 | 16 | 0 | within |
| notice-burst-6 | 22.900 | 140 | 16 | 0 | within |
| notice-burst-6 | 23.081 | 140 | 16 | 0 | within |
| notice-burst-6 | 24.890 | 140 | 16 | 0 | within |
| notice-burst-6 | 25.085 | 140 | 16 | 0 | within |
| notice-burst-6 | 26.858 | 140 | 16 | 0 | within |
| notice-burst-7 | 9.009 | 140 | 16 | 0 | within |
| notice-burst-7 | 17.439 | 140 | 16 | 0 | within |
| notice-burst-7 | 17.659 | 140 | 16 | 0 | within |
| notice-burst-7 | 19.076 | 140 | 16 | 0 | within |
| notice-burst-7 | 1.994 | 140 | 16 | 0 | within |
| notice-burst-7 | 2.200 | 140 | 16 | 0 | within |
| notice-burst-7 | 3.045 | 140 | 16 | 0 | within |
| notice-burst-7 | 3.247 | 140 | 16 | 0 | within |
| notice-burst-7 | 19.260 | 140 | 16 | 0 | within |
| notice-burst-7 | 20.987 | 140 | 16 | 0 | within |
| notice-burst-7 | 21.181 | 140 | 16 | 0 | within |
| notice-burst-7 | 3.507 | 140 | 16 | 0 | within |

Latest: 27.073 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 101,191 (1.012) | 76,233 (0.762) |
| notice-every-1 | 307 | 101,679 (1.017) | 76,154 (0.762) |
| notice-every-2 | 307 | 98,213 (0.982) | 76,154 (0.762) |
| notice-every-3 | 307 | 105,223 (1.052) | 76,238 (0.762) |
| notice-every-4 | 307 | 110,678 (1.107) | 76,283 (0.763) |
| notice-every-5 | 307 | 91,577 (0.916) | 75,532 (0.755) |
| notice-every-6 | 307 | 91,577 (0.916) | 75,532 (0.755) |
| notice-every-7 | 307 | 91,577 (0.916) | 75,532 (0.755) |
| notice-burst-0 | 317 | 136,560 (1.366) | 77,690 (0.777) |
| notice-burst-1 | 317 | 104,683 (1.047) | 77,690 (0.777) |
| notice-burst-2 | 317 | 111,457 (1.115) | 77,690 (0.777) |
| notice-burst-3 | 317 | 105,223 (1.052) | 77,690 (0.777) |
| notice-burst-4 | 317 | 110,678 (1.107) | 77,690 (0.777) |
| notice-burst-5 | 317 | 103,284 (1.033) | 77,690 (0.777) |
| notice-burst-6 | 317 | 104,610 (1.046) | 77,690 (0.777) |
| notice-burst-7 | 317 | 104,571 (1.046) | 77,690 (0.777) |

Longest pass that carries a step: 136,560 CPU cycles (1.366 ms), notice-burst-0; longest step: 77,690 (0.777 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 801,282 | 8.013 | 140 | 144 | fits | 47,454 | 102 | 0.269 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 820,934 | 8.209 | 140 | 144 | fits | 47,454 | 102 | 0.269 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 190,794 | 1.908 | 140 | 144 | fits | 49,970 | 105 | 0.288 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 211,451 | 2.115 | 140 | 144 | fits | 49,970 | 105 | 0.288 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 387,354 | 3.874 | 140 | 144 | fits | 49,201 | 109 | 0.263 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 407,439 | 4.074 | 140 | 144 | fits | 49,201 | 109 | 0.263 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 592,832 | 5.928 | 140 | 144 | fits | 46,733 | 103 | 0.238 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 612,741 | 6.127 | 140 | 144 | fits | 46,733 | 103 | 0.238 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 979,434 | 9.794 | 140 | 144 | fits | 40,754 | 101 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 996,438 | 9.964 | 140 | 144 | fits | 40,754 | 101 | 0.197 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 1,192,158 | 11.922 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 1,211,921 | 12.119 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 165,427 | 1.654 | 20 | 200 | fits | 153,037 | 263 | 0.328 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 447,005 | 4.470 | 20 | 20 | fits | 142,916 | 123 | 0.522 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 426,801 | 4.268 | 20 | 24 | fits | 142,916 | 123 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 407,530 | 4.075 | 20 | 50 | fits | 142,916 | 123 | 0.522 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,147,478 | 11.475 | 20 | 20 | fits | 44,936 | 31 | 0.801 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 86,530 | 0.865 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 208,721 | 2.087 | 140 | 144 | fits | 48,826 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 228,841 | 2.288 | 140 | 144 | fits | 48,826 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 403,479 | 4.035 | 140 | 144 | fits | 50,638 | 109 | 0.286 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 423,699 | 4.237 | 140 | 144 | fits | 50,638 | 109 | 0.286 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 590,031 | 5.900 | 140 | 144 | fits | 46,227 | 105 | 0.239 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 609,709 | 6.097 | 140 | 144 | fits | 46,227 | 105 | 0.239 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 791,645 | 7.916 | 140 | 144 | fits | 45,649 | 104 | 0.237 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 811,172 | 8.112 | 140 | 144 | fits | 45,649 | 104 | 0.237 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 989,663 | 9.897 | 140 | 144 | fits | 40,884 | 101 | 0.199 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 1,006,667 | 10.067 | 140 | 144 | fits | 40,884 | 101 | 0.199 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 1,202,400 | 12.024 | 140 | 144 | fits | 44,542 | 104 | 0.156 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 1,222,163 | 12.222 | 140 | 144 | fits | 44,542 | 104 | 0.156 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 167,734 | 1.677 | 20 | 200 | fits | 153,214 | 265 | 0.327 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 466,268 | 4.663 | 20 | 20 | fits | 142,662 | 123 | 0.522 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 446,064 | 4.461 | 20 | 24 | fits | 142,662 | 123 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 426,793 | 4.268 | 20 | 50 | fits | 142,662 | 123 | 0.522 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,162,531 | 11.625 | 20 | 20 | fits | 39,076 | 19 | 0.810 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 78,382 | 0.784 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 208,721 | 2.087 | 140 | 144 | fits | 48,826 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 228,841 | 2.288 | 140 | 144 | fits | 48,826 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 403,479 | 4.035 | 140 | 144 | fits | 50,638 | 109 | 0.286 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 423,699 | 4.237 | 140 | 144 | fits | 50,638 | 109 | 0.286 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 590,031 | 5.900 | 140 | 144 | fits | 46,227 | 105 | 0.239 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 609,709 | 6.097 | 140 | 144 | fits | 46,227 | 105 | 0.239 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 791,645 | 7.916 | 140 | 144 | fits | 45,649 | 104 | 0.237 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 811,172 | 8.112 | 140 | 144 | fits | 45,649 | 104 | 0.237 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 989,663 | 9.897 | 140 | 144 | fits | 40,884 | 101 | 0.199 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 1,006,667 | 10.067 | 140 | 144 | fits | 40,884 | 101 | 0.199 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 1,184,218 | 11.842 | 140 | 144 | fits | 44,542 | 104 | 0.156 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 1,203,981 | 12.040 | 140 | 144 | fits | 44,542 | 104 | 0.156 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 166,896 | 1.669 | 20 | 200 | fits | 149,524 | 266 | 0.339 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 456,158 | 4.562 | 20 | 20 | fits | 148,189 | 129 | 0.518 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 435,954 | 4.360 | 20 | 24 | fits | 148,189 | 129 | 0.518 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 416,683 | 4.167 | 20 | 50 | fits | 148,189 | 129 | 0.518 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,156,843 | 11.568 | 20 | 20 | fits | 39,179 | 19 | 0.811 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 94,110 | 0.941 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 589,137 | 5.891 | 140 | 144 | fits | 47,962 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 608,910 | 6.089 | 140 | 144 | fits | 47,962 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 792,865 | 7.929 | 140 | 144 | fits | 47,762 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 812,815 | 8.128 | 140 | 144 | fits | 47,762 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 185,564 | 1.856 | 140 | 144 | fits | 48,687 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 206,148 | 2.061 | 140 | 144 | fits | 48,687 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 382,110 | 3.821 | 140 | 144 | fits | 49,760 | 109 | 0.266 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 402,474 | 4.025 | 140 | 144 | fits | 49,760 | 109 | 0.266 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 991,524 | 9.915 | 140 | 144 | fits | 40,754 | 101 | 0.197 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 1,008,528 | 10.085 | 140 | 144 | fits | 40,754 | 101 | 0.197 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 1,186,066 | 11.861 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 1,205,829 | 12.058 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 173,048 | 1.730 | 20 | 200 | fits | 147,965 | 276 | 0.336 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 477,925 | 4.779 | 20 | 20 | fits | 148,930 | 119 | 0.498 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 457,721 | 4.577 | 20 | 24 | fits | 148,930 | 119 | 0.498 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 113,305 | 1.133 | 20 | 50 | fits | 147,965 | 276 | 0.336 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,170,043 | 11.700 | 20 | 20 | fits | 39,048 | 19 | 0.810 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 85,830 | 0.858 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 591,764 | 5.918 | 140 | 144 | fits | 47,962 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 611,537 | 6.115 | 140 | 144 | fits | 47,962 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 795,435 | 7.954 | 140 | 144 | fits | 47,896 | 104 | 0.267 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 815,385 | 8.154 | 140 | 144 | fits | 47,896 | 104 | 0.267 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 209,000 | 2.090 | 140 | 144 | fits | 48,636 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 229,584 | 2.296 | 140 | 144 | fits | 48,636 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 403,183 | 4.032 | 140 | 144 | fits | 49,707 | 109 | 0.263 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 423,547 | 4.235 | 140 | 144 | fits | 49,707 | 109 | 0.263 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 994,315 | 9.943 | 140 | 144 | fits | 40,807 | 101 | 0.199 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 1,011,319 | 10.113 | 140 | 144 | fits | 40,807 | 101 | 0.199 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 1,188,871 | 11.889 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 1,208,634 | 12.086 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 132,597 | 1.326 | 20 | 200 | fits | 120,989 | 146 | 0.325 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 463,575 | 4.636 | 20 | 20 | fits | 147,941 | 127 | 0.520 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 443,371 | 4.434 | 20 | 24 | fits | 147,941 | 127 | 0.520 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 424,100 | 4.241 | 20 | 50 | fits | 147,941 | 127 | 0.520 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,159,933 | 11.599 | 20 | 20 | fits | 39,068 | 19 | 0.809 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 94,036 | 0.940 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 591,764 | 5.918 | 140 | 144 | fits | 47,962 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 611,537 | 6.115 | 140 | 144 | fits | 47,962 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 795,435 | 7.954 | 140 | 144 | fits | 47,896 | 104 | 0.267 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 815,385 | 8.154 | 140 | 144 | fits | 47,896 | 104 | 0.267 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 209,000 | 2.090 | 140 | 144 | fits | 48,636 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 229,584 | 2.296 | 140 | 144 | fits | 48,636 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 403,183 | 4.032 | 140 | 144 | fits | 49,707 | 109 | 0.263 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 423,547 | 4.235 | 140 | 144 | fits | 49,707 | 109 | 0.263 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 994,315 | 9.943 | 140 | 144 | fits | 40,807 | 101 | 0.199 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 1,011,319 | 10.113 | 140 | 144 | fits | 40,807 | 101 | 0.199 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 1,188,871 | 11.889 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 1,208,634 | 12.086 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 155,993 | 1.560 | 20 | 200 | fits | 150,559 | 265 | 0.336 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 464,242 | 4.642 | 20 | 20 | fits | 149,325 | 133 | 0.517 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 444,038 | 4.440 | 20 | 24 | fits | 149,325 | 133 | 0.517 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 424,767 | 4.248 | 20 | 50 | fits | 149,325 | 133 | 0.517 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,161,323 | 11.613 | 20 | 20 | fits | 39,130 | 19 | 0.811 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 95,944 | 0.959 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 589,123 | 5.891 | 140 | 144 | fits | 47,962 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 608,896 | 6.089 | 140 | 144 | fits | 47,962 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 792,837 | 7.928 | 140 | 144 | fits | 47,762 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 812,787 | 8.128 | 140 | 144 | fits | 47,762 | 102 | 0.267 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 185,564 | 1.856 | 140 | 144 | fits | 48,687 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 206,148 | 2.061 | 140 | 144 | fits | 48,687 | 105 | 0.271 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 382,110 | 3.821 | 140 | 144 | fits | 49,760 | 109 | 0.266 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 402,474 | 4.025 | 140 | 144 | fits | 49,760 | 109 | 0.266 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 991,510 | 9.915 | 140 | 144 | fits | 40,754 | 101 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 1,008,514 | 10.085 | 140 | 144 | fits | 40,754 | 101 | 0.197 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 1,186,066 | 11.861 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 1,205,829 | 12.058 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 158,149 | 1.581 | 20 | 200 | fits | 149,057 | 264 | 0.333 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 465,474 | 4.655 | 20 | 20 | fits | 148,754 | 129 | 0.523 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 445,270 | 4.453 | 20 | 24 | fits | 148,754 | 129 | 0.523 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 425,999 | 4.260 | 20 | 50 | fits | 148,754 | 129 | 0.523 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,164,260 | 11.643 | 20 | 20 | fits | 39,141 | 19 | 0.811 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 80,125 | 0.801 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 801,535 | 8.015 | 140 | 144 | fits | 47,454 | 102 | 0.269 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 821,187 | 8.212 | 140 | 144 | fits | 47,454 | 102 | 0.269 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 190,831 | 1.908 | 140 | 144 | fits | 49,847 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 211,488 | 2.115 | 140 | 144 | fits | 49,847 | 103 | 0.287 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 593,020 | 5.930 | 140 | 144 | fits | 46,680 | 103 | 0.238 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 612,929 | 6.129 | 140 | 144 | fits | 46,680 | 103 | 0.238 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 387,508 | 3.875 | 140 | 144 | fits | 49,594 | 109 | 0.261 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 407,759 | 4.078 | 140 | 144 | fits | 49,594 | 109 | 0.261 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 979,673 | 9.797 | 140 | 144 | fits | 40,754 | 101 | 0.197 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 996,677 | 9.967 | 140 | 144 | fits | 40,754 | 101 | 0.197 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 1,192,383 | 11.924 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 1,212,146 | 12.121 | 140 | 144 | fits | 44,667 | 104 | 0.156 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 168,683 | 1.687 | 20 | 200 | fits | 148,203 | 260 | 0.342 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 469,285 | 4.693 | 20 | 20 | fits | 146,681 | 123 | 0.521 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 449,081 | 4.491 | 20 | 24 | fits | 146,681 | 123 | 0.521 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 429,810 | 4.298 | 20 | 50 | fits | 146,681 | 123 | 0.521 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,169,721 | 11.697 | 20 | 20 | fits | 38,993 | 19 | 0.808 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 89,850 | 0.898 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 831,143 | 8.311 | 140 | 144 | fits | 27,231 | 52 | 0.431 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,676,898 | 16.769 | 140 | 144 | fits | 46,299 | 102 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 220,297 | 2.203 | 140 | 144 | fits | 50,037 | 102 | 0.290 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 240,839 | 2.408 | 140 | 144 | fits | 50,037 | 102 | 0.290 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 334,091 | 3.341 | 140 | 144 | fits | 136,560 | 111 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 354,145 | 3.541 | 140 | 144 | fits | 136,560 | 111 | 0.224 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 453,926 | 4.539 | 140 | 144 | fits | 44,790 | 102 | 0.145 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 473,873 | 4.739 | 140 | 144 | fits | 44,790 | 102 | 0.145 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,695,358 | 16.954 | 140 | 144 | fits | 46,299 | 102 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 1,798,299 | 17.983 | 140 | 144 | fits | 42,468 | 102 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,817,702 | 18.177 | 140 | 144 | fits | 42,468 | 102 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 656,225 | 6.562 | 140 | 144 | fits | 27,778 | 53 | 0.380 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 159,369 | 1.594 | 20 | 200 | fits | 153,615 | 267 | 0.361 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 489,052 | 4.891 | 20 | 20 | fits | 147,443 | 130 | 0.533 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 468,848 | 4.688 | 20 | 24 | fits | 147,443 | 130 | 0.533 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 449,577 | 4.496 | 20 | 50 | fits | 147,443 | 130 | 0.533 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 1,098,017 | 10.980 | 20 | 20 | fits | 37,799 | 18 | 0.810 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 948,026 | 9.480 | 140 | 144 | fits | 28,887 | 51 | 0.480 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,653,522 | 16.535 | 140 | 144 | fits | 49,655 | 103 | 0.333 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,675,292 | 16.753 | 140 | 144 | fits | 49,655 | 103 | 0.333 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,817,726 | 18.177 | 140 | 144 | fits | 43,414 | 102 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 364,054 | 3.641 | 140 | 144 | fits | 48,973 | 102 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 384,787 | 3.848 | 140 | 144 | fits | 48,973 | 102 | 0.296 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 430,855 | 4.309 | 140 | 144 | fits | 66,547 | 118 | 0.328 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 450,952 | 4.510 | 140 | 144 | fits | 66,547 | 118 | 0.328 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,835,978 | 18.360 | 140 | 144 | fits | 43,414 | 102 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 2,026,564 | 20.266 | 140 | 144 | fits | 42,387 | 102 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 2,046,058 | 20.461 | 140 | 144 | fits | 42,387 | 102 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 628,602 | 6.286 | 140 | 144 | fits | 26,712 | 52 | 0.320 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 525,556 | 5.256 | 20 | 200 | fits | 134,204 | 231 | 0.320 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 505,288 | 5.053 | 20 | 20 | fits | 134,204 | 231 | 0.320 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 350,880 | 3.509 | 20 | 24 | fits | 156,365 | 157 | 0.502 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 465,813 | 4.658 | 20 | 50 | fits | 134,204 | 231 | 0.320 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,150,250 | 11.502 | 20 | 20 | fits | 37,878 | 18 | 0.810 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 885,785 | 8.858 | 140 | 144 | fits | 28,752 | 51 | 0.476 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,596,373 | 15.964 | 140 | 144 | fits | 49,709 | 103 | 0.335 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,618,143 | 16.181 | 140 | 144 | fits | 49,709 | 103 | 0.335 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,724,675 | 17.247 | 140 | 144 | fits | 43,414 | 102 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 320,104 | 3.201 | 140 | 144 | fits | 63,619 | 111 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 340,929 | 3.409 | 140 | 144 | fits | 63,619 | 111 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 366,231 | 3.662 | 140 | 144 | fits | 45,057 | 103 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 386,314 | 3.863 | 140 | 144 | fits | 45,057 | 103 | 0.120 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 1,742,927 | 17.429 | 140 | 144 | fits | 43,414 | 102 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 1,915,641 | 19.156 | 140 | 144 | fits | 42,387 | 102 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 1,935,135 | 19.351 | 140 | 144 | fits | 42,387 | 102 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 567,005 | 5.670 | 140 | 144 | fits | 26,953 | 52 | 0.332 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 566,888 | 5.669 | 20 | 200 | fits | 134,053 | 231 | 0.319 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 546,620 | 5.466 | 20 | 20 | fits | 134,053 | 231 | 0.319 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 392,363 | 3.924 | 20 | 24 | fits | 155,988 | 157 | 0.499 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 507,145 | 5.071 | 20 | 50 | fits | 134,053 | 231 | 0.319 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,196,515 | 11.965 | 20 | 20 | fits | 37,878 | 18 | 0.810 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,424,252 | 14.243 | 140 | 144 | fits | 50,784 | 103 | 0.362 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,444,841 | 14.448 | 140 | 144 | fits | 50,784 | 103 | 0.362 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,627,598 | 16.276 | 140 | 144 | fits | 47,880 | 102 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,647,548 | 16.475 | 140 | 144 | fits | 47,880 | 102 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 225,060 | 2.251 | 140 | 144 | fits | 65,134 | 111 | 0.336 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 245,648 | 2.456 | 140 | 144 | fits | 65,134 | 111 | 0.336 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 425,563 | 4.256 | 140 | 144 | fits | 26,407 | 52 | 0.388 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,826,978 | 18.270 | 140 | 144 | fits | 43,481 | 103 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,845,066 | 18.451 | 140 | 144 | fits | 43,481 | 103 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,020,576 | 20.206 | 140 | 144 | fits | 42,878 | 102 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,039,945 | 20.399 | 140 | 144 | fits | 42,878 | 102 | 0.185 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,222,152 | 22.222 | 140 | 144 | fits | 25,749 | 52 | 0.297 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 533,384 | 5.334 | 20 | 200 | fits | 133,954 | 229 | 0.316 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 513,116 | 5.131 | 20 | 20 | fits | 133,954 | 229 | 0.316 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 358,958 | 3.590 | 20 | 24 | fits | 159,978 | 162 | 0.506 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 473,641 | 4.736 | 20 | 50 | fits | 133,954 | 229 | 0.316 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,107,318 | 11.073 | 20 | 20 | fits | 78,741 | 30 | 0.643 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,236,555 | 12.366 | 140 | 144 | fits | 50,739 | 102 | 0.361 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 1,257,009 | 12.570 | 140 | 144 | fits | 50,739 | 102 | 0.361 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 230,218 | 2.302 | 140 | 144 | fits | 29,367 | 52 | 0.471 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,383,084 | 13.831 | 140 | 144 | fits | 45,723 | 103 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,403,119 | 14.031 | 140 | 144 | fits | 45,723 | 103 | 0.226 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,582,913 | 15.829 | 140 | 144 | fits | 45,490 | 102 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 1,602,865 | 16.029 | 140 | 144 | fits | 45,490 | 102 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 1,782,012 | 17.820 | 140 | 144 | fits | 43,453 | 103 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 1,800,100 | 18.001 | 140 | 144 | fits | 43,453 | 103 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 1,981,000 | 19.810 | 140 | 144 | fits | 43,516 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,000,538 | 20.005 | 140 | 144 | fits | 43,516 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,177,897 | 21.779 | 140 | 144 | fits | 25,084 | 52 | 0.264 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 148,225 | 1.482 | 20 | 200 | fits | 147,173 | 248 | 0.320 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 462,709 | 4.627 | 20 | 20 | fits | 152,167 | 141 | 0.506 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 442,505 | 4.425 | 20 | 24 | fits | 152,167 | 141 | 0.506 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 423,234 | 4.232 | 20 | 50 | fits | 152,167 | 141 | 0.506 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 1,052,713 | 10.527 | 20 | 20 | fits | 78,737 | 30 | 0.642 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 760,105 | 7.601 | 140 | 144 | fits | 29,275 | 52 | 0.483 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,763,873 | 17.639 | 140 | 144 | fits | 50,731 | 102 | 0.359 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,785,840 | 17.858 | 140 | 144 | fits | 50,731 | 102 | 0.359 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,912,226 | 19.122 | 140 | 144 | fits | 46,036 | 103 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,932,392 | 19.324 | 140 | 144 | fits | 46,036 | 103 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,112,224 | 21.122 | 140 | 144 | fits | 45,552 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 2,132,176 | 21.322 | 140 | 144 | fits | 45,552 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 2,311,456 | 23.115 | 140 | 144 | fits | 43,515 | 103 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,329,544 | 23.295 | 140 | 144 | fits | 43,515 | 103 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,510,444 | 25.104 | 140 | 144 | fits | 43,489 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,529,932 | 25.299 | 140 | 144 | fits | 43,489 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,707,272 | 27.073 | 140 | 144 | fits | 25,084 | 52 | 0.264 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 149,736 | 1.497 | 20 | 200 | fits | 148,628 | 252 | 0.329 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 465,773 | 4.658 | 20 | 20 | fits | 154,169 | 147 | 0.507 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 445,569 | 4.456 | 20 | 24 | fits | 154,169 | 147 | 0.507 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 426,298 | 4.263 | 20 | 50 | fits | 154,169 | 147 | 0.507 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,053,061 | 10.531 | 20 | 20 | fits | 78,661 | 30 | 0.640 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 742,036 | 7.420 | 140 | 144 | fits | 28,870 | 52 | 0.471 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,742,830 | 17.428 | 140 | 144 | fits | 50,784 | 102 | 0.361 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,764,797 | 17.648 | 140 | 144 | fits | 50,784 | 102 | 0.361 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,891,030 | 18.910 | 140 | 144 | fits | 46,036 | 103 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,911,196 | 19.112 | 140 | 144 | fits | 46,036 | 103 | 0.238 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,090,956 | 20.910 | 140 | 144 | fits | 45,552 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,110,908 | 21.109 | 140 | 144 | fits | 45,552 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,290,035 | 22.900 | 140 | 144 | fits | 43,515 | 103 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,308,123 | 23.081 | 140 | 144 | fits | 43,515 | 103 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,489,023 | 24.890 | 140 | 144 | fits | 43,466 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,508,511 | 25.085 | 140 | 144 | fits | 43,466 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,685,814 | 26.858 | 140 | 144 | fits | 25,084 | 52 | 0.264 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 157,300 | 1.573 | 20 | 200 | fits | 152,563 | 268 | 0.313 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 467,658 | 4.677 | 20 | 20 | fits | 148,943 | 126 | 0.524 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 447,454 | 4.475 | 20 | 24 | fits | 148,943 | 126 | 0.524 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 428,183 | 4.282 | 20 | 50 | fits | 148,943 | 126 | 0.524 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 1,057,260 | 10.573 | 20 | 20 | fits | 78,737 | 30 | 0.642 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 900,865 | 9.009 | 140 | 144 | fits | 28,270 | 54 | 0.460 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,743,889 | 17.439 | 140 | 144 | fits | 50,325 | 103 | 0.355 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,765,905 | 17.659 | 140 | 144 | fits | 50,325 | 103 | 0.355 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,907,572 | 19.076 | 140 | 144 | fits | 43,545 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 199,394 | 1.994 | 140 | 144 | fits | 63,591 | 111 | 0.303 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 219,982 | 2.200 | 140 | 144 | fits | 63,591 | 111 | 0.303 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 304,515 | 3.045 | 140 | 144 | fits | 61,846 | 112 | 0.258 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 324,656 | 3.247 | 140 | 144 | fits | 61,846 | 112 | 0.258 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,925,955 | 19.260 | 140 | 144 | fits | 43,545 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,098,655 | 20.987 | 140 | 144 | fits | 42,387 | 102 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,118,149 | 21.181 | 140 | 144 | fits | 42,387 | 102 | 0.182 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 350,700 | 3.507 | 140 | 144 | fits | 25,282 | 52 | 0.132 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 158,477 | 1.585 | 20 | 200 | fits | 148,093 | 259 | 0.328 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 461,185 | 4.612 | 20 | 20 | fits | 149,025 | 135 | 0.528 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 440,981 | 4.410 | 20 | 24 | fits | 149,025 | 135 | 0.528 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 421,710 | 4.217 | 20 | 50 | fits | 149,025 | 135 | 0.528 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 1,046,489 | 10.465 | 20 | 20 | fits | 78,441 | 30 | 0.645 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

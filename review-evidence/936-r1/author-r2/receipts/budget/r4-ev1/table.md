Original file: <scratch>/r4/budget/r4-ev1/results/table.md
Original size: 55412 bytes
Original sha256: 83f86dff3f2f5f7a648c9667e9c3107b1e486bb56d4aa73e550fce588aa7b9c4

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.acmp.if0` (notice-burst-0) | 4.900 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.adp.if0` (notice-burst-4) | 5.016 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.aecp.if0` (notice-burst-0) | 4.698 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-0.held.maap.if0` (notice-burst-0) | 4.505 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-every-5.held.srp.if0` (notice-every-5) | 11.742 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-0.mrpdu.periodic.if0` (notice-every-0) | 1.039 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-5.notices.29.36.0.if0` (notice-burst-5) | 27.294 (27.513) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1509 | 0 | 156,208 (1.562) | fits |
| notice-every-1 | 1505 | 0 | 156,208 (1.562) | fits |
| notice-every-2 | 1504 | 0 | 156,208 (1.562) | fits |
| notice-every-3 | 1507 | 0 | 156,040 (1.560) | fits |
| notice-every-4 | 1499 | 0 | 156,040 (1.560) | fits |
| notice-every-5 | 1496 | 0 | 156,124 (1.561) | fits |
| notice-every-6 | 1502 | 0 | 156,124 (1.561) | fits |
| notice-every-7 | 1497 | 0 | 156,051 (1.561) | fits |
| notice-burst-0 | 1061 | 0 | 152,990 (1.530) | fits |
| notice-burst-1 | 1056 | 0 | 153,567 (1.536) | fits |
| notice-burst-2 | 1051 | 0 | 158,386 (1.584) | fits |
| notice-burst-3 | 1044 | 0 | 153,438 (1.534) | fits |
| notice-burst-4 | 1043 | 0 | 160,702 (1.607) | fits |
| notice-burst-5 | 1059 | 0 | 153,682 (1.537) | fits |
| notice-burst-6 | 1033 | 0 | 154,294 (1.543) | fits |
| notice-burst-7 | 1047 | 0 | 152,684 (1.527) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 2.190 | 140 | 16 | 2 | within |
| notice-every-0 | 2.395 | 140 | 16 | 2 | within |
| notice-every-0 | 5.107 | 140 | 16 | 2 | within |
| notice-every-0 | 5.312 | 140 | 16 | 2 | within |
| notice-every-0 | 6.258 | 140 | 16 | 2 | within |
| notice-every-0 | 6.458 | 140 | 16 | 2 | within |
| notice-every-0 | 8.077 | 140 | 16 | 2 | within |
| notice-every-0 | 8.275 | 140 | 16 | 2 | within |
| notice-every-0 | 10.065 | 140 | 16 | 2 | within |
| notice-every-0 | 10.238 | 140 | 16 | 2 | within |
| notice-every-0 | 12.206 | 140 | 16 | 2 | within |
| notice-every-0 | 12.405 | 140 | 16 | 2 | within |
| notice-every-1 | 1.858 | 140 | 16 | 2 | within |
| notice-every-1 | 2.061 | 140 | 16 | 2 | within |
| notice-every-1 | 3.825 | 140 | 16 | 2 | within |
| notice-every-1 | 4.030 | 140 | 16 | 2 | within |
| notice-every-1 | 5.879 | 140 | 16 | 2 | within |
| notice-every-1 | 6.080 | 140 | 16 | 2 | within |
| notice-every-1 | 7.902 | 140 | 16 | 2 | within |
| notice-every-1 | 8.100 | 140 | 16 | 2 | within |
| notice-every-1 | 9.887 | 140 | 16 | 2 | within |
| notice-every-1 | 10.059 | 140 | 16 | 2 | within |
| notice-every-1 | 11.845 | 140 | 16 | 2 | within |
| notice-every-1 | 12.044 | 140 | 16 | 2 | within |
| notice-every-2 | 1.858 | 140 | 16 | 2 | within |
| notice-every-2 | 2.061 | 140 | 16 | 2 | within |
| notice-every-2 | 3.825 | 140 | 16 | 2 | within |
| notice-every-2 | 4.030 | 140 | 16 | 2 | within |
| notice-every-2 | 5.880 | 140 | 16 | 2 | within |
| notice-every-2 | 6.081 | 140 | 16 | 2 | within |
| notice-every-2 | 7.902 | 140 | 16 | 2 | within |
| notice-every-2 | 8.101 | 140 | 16 | 2 | within |
| notice-every-2 | 9.888 | 140 | 16 | 2 | within |
| notice-every-2 | 10.060 | 140 | 16 | 2 | within |
| notice-every-2 | 11.846 | 140 | 16 | 2 | within |
| notice-every-2 | 12.045 | 140 | 16 | 2 | within |
| notice-every-3 | 3.828 | 140 | 16 | 2 | within |
| notice-every-3 | 4.030 | 140 | 16 | 2 | within |
| notice-every-3 | 5.896 | 140 | 16 | 2 | within |
| notice-every-3 | 6.100 | 140 | 16 | 2 | within |
| notice-every-3 | 7.925 | 140 | 16 | 2 | within |
| notice-every-3 | 8.124 | 140 | 16 | 2 | within |
| notice-every-3 | 1.858 | 140 | 16 | 2 | within |
| notice-every-3 | 2.067 | 140 | 16 | 2 | within |
| notice-every-3 | 9.914 | 140 | 16 | 2 | within |
| notice-every-3 | 10.086 | 140 | 16 | 2 | within |
| notice-every-3 | 11.872 | 140 | 16 | 2 | within |
| notice-every-3 | 12.071 | 140 | 16 | 2 | within |
| notice-every-4 | 3.828 | 140 | 16 | 2 | within |
| notice-every-4 | 4.030 | 140 | 16 | 2 | within |
| notice-every-4 | 5.896 | 140 | 16 | 2 | within |
| notice-every-4 | 6.100 | 140 | 16 | 2 | within |
| notice-every-4 | 7.925 | 140 | 16 | 2 | within |
| notice-every-4 | 8.124 | 140 | 16 | 2 | within |
| notice-every-4 | 1.858 | 140 | 16 | 2 | within |
| notice-every-4 | 2.067 | 140 | 16 | 2 | within |
| notice-every-4 | 9.914 | 140 | 16 | 2 | within |
| notice-every-4 | 10.086 | 140 | 16 | 2 | within |
| notice-every-4 | 11.872 | 140 | 16 | 2 | within |
| notice-every-4 | 12.071 | 140 | 16 | 2 | within |
| notice-every-5 | 5.887 | 140 | 16 | 2 | within |
| notice-every-5 | 6.089 | 140 | 16 | 2 | within |
| notice-every-5 | 7.971 | 140 | 16 | 2 | within |
| notice-every-5 | 8.175 | 140 | 16 | 2 | within |
| notice-every-5 | 1.860 | 140 | 16 | 2 | within |
| notice-every-5 | 2.067 | 140 | 16 | 2 | within |
| notice-every-5 | 3.818 | 140 | 16 | 2 | within |
| notice-every-5 | 4.024 | 140 | 16 | 2 | within |
| notice-every-5 | 9.769 | 140 | 16 | 2 | within |
| notice-every-5 | 9.942 | 140 | 16 | 2 | within |
| notice-every-5 | 11.910 | 140 | 16 | 2 | within |
| notice-every-5 | 12.109 | 140 | 16 | 2 | within |
| notice-every-6 | 5.890 | 140 | 16 | 2 | within |
| notice-every-6 | 6.091 | 140 | 16 | 2 | within |
| notice-every-6 | 7.975 | 140 | 16 | 2 | within |
| notice-every-6 | 8.178 | 140 | 16 | 2 | within |
| notice-every-6 | 1.861 | 140 | 16 | 2 | within |
| notice-every-6 | 2.068 | 140 | 16 | 2 | within |
| notice-every-6 | 3.820 | 140 | 16 | 2 | within |
| notice-every-6 | 4.026 | 140 | 16 | 2 | within |
| notice-every-6 | 9.773 | 140 | 16 | 2 | within |
| notice-every-6 | 9.946 | 140 | 16 | 2 | within |
| notice-every-6 | 11.914 | 140 | 16 | 2 | within |
| notice-every-6 | 12.113 | 140 | 16 | 2 | within |
| notice-every-7 | 8.023 | 140 | 16 | 2 | within |
| notice-every-7 | 8.223 | 140 | 16 | 2 | within |
| notice-every-7 | 1.916 | 140 | 16 | 2 | within |
| notice-every-7 | 2.123 | 140 | 16 | 2 | within |
| notice-every-7 | 3.878 | 140 | 16 | 2 | within |
| notice-every-7 | 4.081 | 140 | 16 | 2 | within |
| notice-every-7 | 5.936 | 140 | 16 | 2 | within |
| notice-every-7 | 6.139 | 140 | 16 | 2 | within |
| notice-every-7 | 9.817 | 140 | 16 | 2 | within |
| notice-every-7 | 9.989 | 140 | 16 | 2 | within |
| notice-every-7 | 11.958 | 140 | 16 | 2 | within |
| notice-every-7 | 12.157 | 140 | 16 | 2 | within |
| notice-burst-0 | 8.462 | 140 | 16 | 1 | within |
| notice-burst-0 | 16.967 | 140 | 16 | 1 | within |
| notice-burst-0 | 17.186 | 140 | 16 | 1 | within |
| notice-burst-0 | 18.254 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.217 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.423 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.672 | 140 | 16 | 1 | within |
| notice-burst-0 | 2.873 | 140 | 16 | 1 | within |
| notice-burst-0 | 18.437 | 140 | 16 | 1 | within |
| notice-burst-0 | 20.175 | 140 | 16 | 1 | within |
| notice-burst-0 | 20.371 | 140 | 16 | 1 | within |
| notice-burst-0 | 6.685 | 140 | 16 | 1 | within |
| notice-burst-1 | 8.871 | 140 | 16 | 0 | within |
| notice-burst-1 | 15.988 | 140 | 16 | 0 | within |
| notice-burst-1 | 16.205 | 140 | 16 | 0 | within |
| notice-burst-1 | 17.995 | 140 | 16 | 0 | within |
| notice-burst-1 | 2.002 | 140 | 16 | 0 | within |
| notice-burst-1 | 2.208 | 140 | 16 | 0 | within |
| notice-burst-1 | 2.459 | 140 | 16 | 0 | within |
| notice-burst-1 | 2.660 | 140 | 16 | 0 | within |
| notice-burst-1 | 18.178 | 140 | 16 | 0 | within |
| notice-burst-1 | 19.916 | 140 | 16 | 0 | within |
| notice-burst-1 | 20.112 | 140 | 16 | 0 | within |
| notice-burst-1 | 5.716 | 140 | 16 | 0 | within |
| notice-burst-2 | 15.027 | 140 | 16 | 1 | within |
| notice-burst-2 | 15.234 | 140 | 16 | 1 | within |
| notice-burst-2 | 16.336 | 140 | 16 | 1 | within |
| notice-burst-2 | 16.538 | 140 | 16 | 1 | within |
| notice-burst-2 | 18.163 | 140 | 16 | 1 | within |
| notice-burst-2 | 18.360 | 140 | 16 | 1 | within |
| notice-burst-2 | 4.897 | 140 | 16 | 1 | within |
| notice-burst-2 | 20.159 | 140 | 16 | 1 | within |
| notice-burst-2 | 20.341 | 140 | 16 | 1 | within |
| notice-burst-2 | 22.156 | 140 | 16 | 1 | within |
| notice-burst-2 | 22.353 | 140 | 16 | 1 | within |
| notice-burst-2 | 24.318 | 140 | 16 | 1 | within |
| notice-burst-3 | 13.842 | 140 | 16 | 2 | within |
| notice-burst-3 | 14.048 | 140 | 16 | 2 | within |
| notice-burst-3 | 15.325 | 140 | 16 | 2 | within |
| notice-burst-3 | 15.527 | 140 | 16 | 2 | within |
| notice-burst-3 | 3.792 | 140 | 16 | 2 | within |
| notice-burst-3 | 17.151 | 140 | 16 | 2 | within |
| notice-burst-3 | 17.351 | 140 | 16 | 2 | within |
| notice-burst-3 | 19.147 | 140 | 16 | 2 | within |
| notice-burst-3 | 19.330 | 140 | 16 | 2 | within |
| notice-burst-3 | 21.148 | 140 | 16 | 2 | within |
| notice-burst-3 | 21.343 | 140 | 16 | 2 | within |
| notice-burst-3 | 23.309 | 140 | 16 | 2 | within |
| notice-burst-4 | 5.248 | 140 | 16 | 0 | within |
| notice-burst-4 | 5.451 | 140 | 16 | 0 | within |
| notice-burst-4 | 17.541 | 140 | 16 | 0 | within |
| notice-burst-4 | 17.752 | 140 | 16 | 0 | within |
| notice-burst-4 | 18.829 | 140 | 16 | 0 | within |
| notice-burst-4 | 19.026 | 140 | 16 | 0 | within |
| notice-burst-4 | 20.825 | 140 | 16 | 0 | within |
| notice-burst-4 | 21.023 | 140 | 16 | 0 | within |
| notice-burst-4 | 5.899 | 140 | 16 | 0 | within |
| notice-burst-4 | 6.077 | 140 | 16 | 0 | within |
| notice-burst-4 | 22.809 | 140 | 16 | 0 | within |
| notice-burst-4 | 23.007 | 140 | 16 | 0 | within |
| notice-burst-5 | 7.689 | 140 | 16 | 1 | within |
| notice-burst-5 | 17.822 | 140 | 16 | 1 | within |
| notice-burst-5 | 18.040 | 140 | 16 | 1 | within |
| notice-burst-5 | 19.132 | 140 | 16 | 1 | within |
| notice-burst-5 | 19.331 | 140 | 16 | 1 | within |
| notice-burst-5 | 21.138 | 140 | 16 | 1 | within |
| notice-burst-5 | 21.336 | 140 | 16 | 1 | within |
| notice-burst-5 | 23.134 | 140 | 16 | 1 | within |
| notice-burst-5 | 23.315 | 140 | 16 | 1 | within |
| notice-burst-5 | 25.133 | 140 | 16 | 1 | within |
| notice-burst-5 | 25.329 | 140 | 16 | 1 | within |
| notice-burst-5 | 27.294 | 140 | 16 | 1 | within |
| notice-burst-6 | 7.285 | 140 | 16 | 0 | within |
| notice-burst-6 | 17.426 | 140 | 16 | 0 | within |
| notice-burst-6 | 17.645 | 140 | 16 | 0 | within |
| notice-burst-6 | 18.920 | 140 | 16 | 0 | within |
| notice-burst-6 | 19.119 | 140 | 16 | 0 | within |
| notice-burst-6 | 20.925 | 140 | 16 | 0 | within |
| notice-burst-6 | 21.123 | 140 | 16 | 0 | within |
| notice-burst-6 | 22.920 | 140 | 16 | 0 | within |
| notice-burst-6 | 23.101 | 140 | 16 | 0 | within |
| notice-burst-6 | 24.918 | 140 | 16 | 0 | within |
| notice-burst-6 | 25.114 | 140 | 16 | 0 | within |
| notice-burst-6 | 26.897 | 140 | 16 | 0 | within |
| notice-burst-7 | 9.188 | 140 | 16 | 1 | within |
| notice-burst-7 | 17.639 | 140 | 16 | 1 | within |
| notice-burst-7 | 17.858 | 140 | 16 | 1 | within |
| notice-burst-7 | 19.107 | 140 | 16 | 1 | within |
| notice-burst-7 | 2.292 | 140 | 16 | 1 | within |
| notice-burst-7 | 2.499 | 140 | 16 | 1 | within |
| notice-burst-7 | 2.955 | 140 | 16 | 1 | within |
| notice-burst-7 | 3.159 | 140 | 16 | 1 | within |
| notice-burst-7 | 19.290 | 140 | 16 | 1 | within |
| notice-burst-7 | 21.028 | 140 | 16 | 1 | within |
| notice-burst-7 | 21.224 | 140 | 16 | 1 | within |
| notice-burst-7 | 3.833 | 140 | 16 | 1 | within |

Latest: 27.294 ms, notice-burst-5.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 307 | 124,606 (1.246) | 76,208 (0.762) |
| notice-every-1 | 307 | 98,106 (0.981) | 76,142 (0.761) |
| notice-every-2 | 307 | 101,281 (1.013) | 76,155 (0.762) |
| notice-every-3 | 307 | 101,733 (1.017) | 76,154 (0.762) |
| notice-every-4 | 307 | 110,532 (1.105) | 76,292 (0.763) |
| notice-every-5 | 307 | 91,673 (0.917) | 75,572 (0.756) |
| notice-every-6 | 307 | 91,673 (0.917) | 75,572 (0.756) |
| notice-every-7 | 307 | 91,673 (0.917) | 75,572 (0.756) |
| notice-burst-0 | 317 | 103,358 (1.034) | 77,653 (0.777) |
| notice-burst-1 | 317 | 102,638 (1.026) | 77,653 (0.777) |
| notice-burst-2 | 317 | 111,487 (1.115) | 77,653 (0.777) |
| notice-burst-3 | 317 | 101,733 (1.017) | 77,653 (0.777) |
| notice-burst-4 | 317 | 110,532 (1.105) | 77,653 (0.777) |
| notice-burst-5 | 317 | 100,168 (1.002) | 77,653 (0.777) |
| notice-burst-6 | 317 | 101,130 (1.011) | 77,653 (0.777) |
| notice-burst-7 | 317 | 102,971 (1.030) | 77,653 (0.777) |

Longest pass that carries a step: 124,606 CPU cycles (1.246 ms), notice-every-0; longest step: 77,653 (0.777 ms), notice-burst-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 219,013 | 2.190 | 140 | 144 | fits | 49,199 | 103 | 0.304 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 239,478 | 2.395 | 140 | 144 | fits | 49,199 | 103 | 0.304 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 510,678 | 5.107 | 140 | 144 | fits | 124,606 | 102 | 0.240 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 531,160 | 5.312 | 140 | 144 | fits | 124,606 | 102 | 0.240 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 625,762 | 6.258 | 140 | 144 | fits | 46,286 | 103 | 0.250 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 645,812 | 6.458 | 140 | 144 | fits | 46,286 | 103 | 0.250 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 807,698 | 8.077 | 140 | 144 | fits | 45,722 | 104 | 0.242 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 827,546 | 8.275 | 140 | 144 | fits | 45,722 | 104 | 0.242 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 1,006,544 | 10.065 | 140 | 144 | fits | 41,126 | 101 | 0.213 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 1,023,771 | 10.238 | 140 | 144 | fits | 41,126 | 101 | 0.213 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 1,220,619 | 12.206 | 140 | 144 | fits | 44,969 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 1,240,519 | 12.405 | 140 | 144 | fits | 44,969 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 135,700 | 1.357 | 20 | 200 | fits | 123,973 | 151 | 0.320 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 435,341 | 4.353 | 20 | 20 | fits | 150,308 | 123 | 0.522 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 415,137 | 4.151 | 20 | 24 | fits | 150,308 | 123 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 395,866 | 3.959 | 20 | 50 | fits | 150,308 | 123 | 0.522 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 1,130,043 | 11.300 | 20 | 20 | fits | 39,243 | 21 | 0.799 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 103,911 | 1.039 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 185,827 | 1.858 | 140 | 144 | fits | 48,926 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 206,115 | 2.061 | 140 | 144 | fits | 48,926 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 382,515 | 3.825 | 140 | 144 | fits | 50,598 | 109 | 0.293 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 402,997 | 4.030 | 140 | 144 | fits | 50,598 | 109 | 0.293 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 587,940 | 5.879 | 140 | 144 | fits | 46,281 | 105 | 0.246 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 607,990 | 6.080 | 140 | 144 | fits | 46,281 | 105 | 0.246 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 790,154 | 7.902 | 140 | 144 | fits | 45,640 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 810,002 | 8.100 | 140 | 144 | fits | 45,640 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 988,712 | 9.887 | 140 | 144 | fits | 41,006 | 101 | 0.207 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 1,005,939 | 10.059 | 140 | 144 | fits | 41,006 | 101 | 0.207 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 1,184,538 | 11.845 | 140 | 144 | fits | 44,969 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 1,204,438 | 12.044 | 140 | 144 | fits | 44,969 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 149,102 | 1.491 | 20 | 200 | fits | 151,124 | 252 | 0.313 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 456,651 | 4.567 | 20 | 20 | fits | 153,389 | 148 | 0.501 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 436,447 | 4.364 | 20 | 24 | fits | 153,389 | 148 | 0.501 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 417,176 | 4.172 | 20 | 50 | fits | 153,389 | 148 | 0.501 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 1,155,362 | 11.554 | 20 | 20 | fits | 39,240 | 19 | 0.809 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 90,583 | 0.906 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 185,827 | 1.858 | 140 | 144 | fits | 48,926 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 206,115 | 2.061 | 140 | 144 | fits | 48,926 | 105 | 0.290 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 382,515 | 3.825 | 140 | 144 | fits | 50,598 | 109 | 0.293 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 402,997 | 4.030 | 140 | 144 | fits | 50,598 | 109 | 0.293 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 588,021 | 5.880 | 140 | 144 | fits | 46,281 | 105 | 0.246 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 608,071 | 6.081 | 140 | 144 | fits | 46,281 | 105 | 0.246 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 790,235 | 7.902 | 140 | 144 | fits | 45,640 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 810,083 | 8.101 | 140 | 144 | fits | 45,640 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 988,793 | 9.888 | 140 | 144 | fits | 41,006 | 101 | 0.207 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 1,006,020 | 10.060 | 140 | 144 | fits | 41,006 | 101 | 0.207 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 1,184,605 | 11.846 | 140 | 144 | fits | 44,969 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 1,204,505 | 12.045 | 140 | 144 | fits | 44,969 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 165,700 | 1.657 | 20 | 200 | fits | 148,636 | 261 | 0.344 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 468,589 | 4.686 | 20 | 20 | fits | 148,616 | 127 | 0.521 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 448,385 | 4.484 | 20 | 24 | fits | 148,616 | 127 | 0.521 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 429,114 | 4.291 | 20 | 50 | fits | 148,616 | 127 | 0.521 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 1,167,008 | 11.670 | 20 | 20 | fits | 39,328 | 19 | 0.810 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 81,387 | 0.814 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 382,813 | 3.828 | 140 | 144 | fits | 50,157 | 109 | 0.295 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 402,978 | 4.030 | 140 | 144 | fits | 50,157 | 109 | 0.295 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 589,563 | 5.896 | 140 | 144 | fits | 48,024 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 609,992 | 6.100 | 140 | 144 | fits | 48,024 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 792,484 | 7.925 | 140 | 144 | fits | 45,672 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 812,383 | 8.124 | 140 | 144 | fits | 45,672 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 185,753 | 1.858 | 140 | 144 | fits | 49,198 | 105 | 0.273 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 206,734 | 2.067 | 140 | 144 | fits | 49,198 | 105 | 0.273 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 991,402 | 9.914 | 140 | 144 | fits | 40,933 | 101 | 0.207 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 1,008,629 | 10.086 | 140 | 144 | fits | 40,933 | 101 | 0.207 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 1,187,199 | 11.872 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 1,207,099 | 12.071 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 178,796 | 1.788 | 20 | 200 | fits | 148,601 | 282 | 0.341 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 470,305 | 4.703 | 20 | 20 | fits | 148,198 | 114 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 450,101 | 4.501 | 20 | 24 | fits | 148,198 | 114 | 0.509 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 119,053 | 1.191 | 20 | 50 | fits | 148,601 | 282 | 0.341 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 1,168,353 | 11.684 | 20 | 20 | fits | 39,243 | 19 | 0.809 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 84,871 | 0.849 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 382,827 | 3.828 | 140 | 144 | fits | 50,157 | 109 | 0.295 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 402,992 | 4.030 | 140 | 144 | fits | 50,157 | 109 | 0.295 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 589,563 | 5.896 | 140 | 144 | fits | 48,024 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 609,992 | 6.100 | 140 | 144 | fits | 48,024 | 103 | 0.270 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 792,470 | 7.925 | 140 | 144 | fits | 45,672 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 812,369 | 8.124 | 140 | 144 | fits | 45,672 | 102 | 0.246 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 185,753 | 1.858 | 140 | 144 | fits | 49,198 | 105 | 0.273 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 206,734 | 2.067 | 140 | 144 | fits | 49,198 | 105 | 0.273 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 991,388 | 9.914 | 140 | 144 | fits | 40,933 | 101 | 0.207 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 1,008,615 | 10.086 | 140 | 144 | fits | 40,933 | 101 | 0.207 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 1,187,199 | 11.872 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 1,207,099 | 12.071 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 162,069 | 1.621 | 20 | 200 | fits | 148,222 | 261 | 0.344 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 470,796 | 4.708 | 20 | 20 | fits | 148,154 | 129 | 0.518 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 450,592 | 4.506 | 20 | 24 | fits | 148,154 | 129 | 0.518 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 431,321 | 4.313 | 20 | 50 | fits | 148,154 | 129 | 0.518 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 1,169,732 | 11.697 | 20 | 20 | fits | 39,129 | 19 | 0.807 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 86,166 | 0.862 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 588,736 | 5.887 | 140 | 144 | fits | 47,757 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 608,871 | 6.089 | 140 | 144 | fits | 47,757 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 797,147 | 7.971 | 140 | 144 | fits | 47,832 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 817,504 | 8.175 | 140 | 144 | fits | 47,832 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 185,963 | 1.860 | 140 | 144 | fits | 48,646 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 206,713 | 2.067 | 140 | 144 | fits | 48,646 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 381,833 | 3.818 | 140 | 144 | fits | 49,723 | 109 | 0.268 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 402,375 | 4.024 | 140 | 144 | fits | 49,723 | 109 | 0.268 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 976,900 | 9.769 | 140 | 144 | fits | 40,984 | 101 | 0.210 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 994,178 | 9.942 | 140 | 144 | fits | 40,984 | 101 | 0.210 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 1,191,025 | 11.910 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 1,210,925 | 12.109 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 162,998 | 1.630 | 20 | 200 | fits | 146,833 | 256 | 0.342 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 473,007 | 4.730 | 20 | 20 | fits | 150,467 | 133 | 0.523 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 452,803 | 4.528 | 20 | 24 | fits | 150,467 | 133 | 0.523 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 433,532 | 4.335 | 20 | 50 | fits | 150,467 | 133 | 0.523 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 1,174,243 | 11.742 | 20 | 20 | fits | 39,345 | 19 | 0.810 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 90,823 | 0.908 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 589,006 | 5.890 | 140 | 144 | fits | 47,757 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 609,141 | 6.091 | 140 | 144 | fits | 47,757 | 103 | 0.275 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 797,493 | 7.975 | 140 | 144 | fits | 47,832 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 817,850 | 8.178 | 140 | 144 | fits | 47,832 | 102 | 0.275 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 186,053 | 1.861 | 140 | 144 | fits | 48,646 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 206,803 | 2.068 | 140 | 144 | fits | 48,646 | 103 | 0.273 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 382,013 | 3.820 | 140 | 144 | fits | 49,723 | 109 | 0.268 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 402,555 | 4.026 | 140 | 144 | fits | 49,723 | 109 | 0.268 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 977,336 | 9.773 | 140 | 144 | fits | 40,984 | 101 | 0.210 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 994,614 | 9.946 | 140 | 144 | fits | 40,984 | 101 | 0.210 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 1,191,447 | 11.914 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 1,211,347 | 12.113 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 149,167 | 1.492 | 20 | 200 | fits | 149,551 | 252 | 0.332 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 463,084 | 4.631 | 20 | 20 | fits | 154,142 | 148 | 0.508 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 442,880 | 4.429 | 20 | 24 | fits | 154,142 | 148 | 0.508 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 423,609 | 4.236 | 20 | 50 | fits | 154,142 | 148 | 0.508 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 1,160,985 | 11.610 | 20 | 20 | fits | 39,279 | 19 | 0.810 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 96,168 | 0.962 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 802,265 | 8.023 | 140 | 144 | fits | 47,565 | 102 | 0.280 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 822,328 | 8.223 | 140 | 144 | fits | 47,565 | 102 | 0.280 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 191,554 | 1.916 | 140 | 144 | fits | 50,011 | 105 | 0.292 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 212,310 | 2.123 | 140 | 144 | fits | 50,011 | 105 | 0.292 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 387,822 | 3.878 | 140 | 144 | fits | 49,168 | 109 | 0.268 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 408,082 | 4.081 | 140 | 144 | fits | 49,168 | 109 | 0.268 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 593,635 | 5.936 | 140 | 144 | fits | 46,781 | 103 | 0.243 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 613,865 | 6.139 | 140 | 144 | fits | 46,781 | 103 | 0.243 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 981,657 | 9.817 | 140 | 144 | fits | 40,984 | 101 | 0.210 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 998,935 | 9.989 | 140 | 144 | fits | 40,984 | 101 | 0.210 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 1,195,768 | 11.958 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 1,215,668 | 12.157 | 140 | 144 | fits | 45,094 | 104 | 0.175 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 493,356 | 4.934 | 20 | 200 | fits | 139,091 | 244 | 0.331 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 473,088 | 4.731 | 20 | 20 | fits | 139,091 | 244 | 0.331 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 346,895 | 3.469 | 20 | 24 | fits | 116,881 | 78 | 0.516 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 433,613 | 4.336 | 20 | 50 | fits | 139,091 | 244 | 0.331 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 1,170,723 | 11.707 | 20 | 20 | fits | 39,054 | 19 | 0.806 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 91,462 | 0.915 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 846,192 | 8.462 | 140 | 144 | fits | 26,849 | 52 | 0.420 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 1,696,687 | 16.967 | 140 | 144 | fits | 50,481 | 103 | 0.357 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,718,572 | 17.186 | 140 | 144 | fits | 50,481 | 103 | 0.357 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,825,431 | 18.254 | 140 | 144 | fits | 43,528 | 102 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 221,743 | 2.217 | 140 | 144 | fits | 62,781 | 111 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 242,345 | 2.423 | 140 | 144 | fits | 62,781 | 111 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 267,178 | 2.672 | 140 | 144 | fits | 45,037 | 103 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 287,333 | 2.873 | 140 | 144 | fits | 45,037 | 103 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 1,843,695 | 18.437 | 140 | 144 | fits | 43,528 | 102 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 2,017,456 | 20.175 | 140 | 144 | fits | 42,698 | 102 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 2,037,073 | 20.371 | 140 | 144 | fits | 42,698 | 102 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 668,458 | 6.685 | 140 | 144 | fits | 28,721 | 52 | 0.400 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 155,861 | 1.559 | 20 | 200 | fits | 152,990 | 268 | 0.321 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 489,971 | 4.900 | 20 | 20 | fits | 148,438 | 131 | 0.536 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 469,767 | 4.698 | 20 | 24 | fits | 148,438 | 131 | 0.536 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 450,496 | 4.505 | 20 | 50 | fits | 148,438 | 131 | 0.536 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 1,102,373 | 11.024 | 20 | 20 | fits | 37,917 | 18 | 0.808 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 887,088 | 8.871 | 140 | 144 | fits | 27,933 | 51 | 0.454 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 1,598,784 | 15.988 | 140 | 144 | fits | 49,912 | 103 | 0.343 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,620,472 | 16.205 | 140 | 144 | fits | 49,912 | 103 | 0.343 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,799,542 | 17.995 | 140 | 144 | fits | 43,528 | 102 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 200,243 | 2.002 | 140 | 144 | fits | 62,899 | 111 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 220,847 | 2.208 | 140 | 144 | fits | 62,899 | 111 | 0.297 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 245,852 | 2.459 | 140 | 144 | fits | 45,075 | 103 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 266,007 | 2.660 | 140 | 144 | fits | 45,075 | 103 | 0.132 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 1,817,806 | 18.178 | 140 | 144 | fits | 43,528 | 102 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 1,991,562 | 19.916 | 140 | 144 | fits | 42,646 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 2,011,179 | 20.112 | 140 | 144 | fits | 42,646 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 571,601 | 5.716 | 140 | 144 | fits | 28,381 | 52 | 0.388 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 173,558 | 1.736 | 20 | 200 | fits | 153,567 | 278 | 0.336 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 469,083 | 4.691 | 20 | 20 | fits | 137,052 | 98 | 0.530 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 448,879 | 4.489 | 20 | 24 | fits | 137,052 | 98 | 0.530 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 113,815 | 1.138 | 20 | 50 | fits | 153,567 | 278 | 0.336 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 1,119,050 | 11.191 | 20 | 20 | fits | 37,917 | 18 | 0.808 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 1,502,704 | 15.027 | 140 | 144 | fits | 50,796 | 102 | 0.368 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 1,523,403 | 15.234 | 140 | 144 | fits | 50,796 | 102 | 0.368 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,633,612 | 16.336 | 140 | 144 | fits | 47,685 | 103 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 1,653,831 | 16.538 | 140 | 144 | fits | 47,685 | 103 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 1,816,267 | 18.163 | 140 | 144 | fits | 45,624 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 1,836,027 | 18.360 | 140 | 144 | fits | 45,624 | 102 | 0.237 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 489,677 | 4.897 | 140 | 144 | fits | 28,461 | 52 | 0.452 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 2,015,883 | 20.159 | 140 | 144 | fits | 43,617 | 103 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 2,034,068 | 20.341 | 140 | 144 | fits | 43,617 | 103 | 0.199 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 2,215,601 | 22.156 | 140 | 144 | fits | 43,733 | 102 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 2,235,326 | 22.353 | 140 | 144 | fits | 43,733 | 102 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 2,431,837 | 24.318 | 140 | 144 | fits | 25,228 | 52 | 0.272 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 169,908 | 1.699 | 20 | 200 | fits | 153,856 | 264 | 0.339 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 477,103 | 4.771 | 20 | 20 | fits | 140,616 | 110 | 0.536 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 456,899 | 4.569 | 20 | 24 | fits | 140,616 | 110 | 0.536 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 437,628 | 4.376 | 20 | 50 | fits | 140,616 | 110 | 0.536 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 1,099,901 | 10.999 | 20 | 20 | fits | 38,479 | 18 | 0.809 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 1,384,209 | 13.842 | 140 | 144 | fits | 50,552 | 102 | 0.363 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 1,404,773 | 14.048 | 140 | 144 | fits | 50,552 | 102 | 0.363 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,532,462 | 15.325 | 140 | 144 | fits | 47,775 | 103 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,552,681 | 15.527 | 140 | 144 | fits | 47,775 | 103 | 0.264 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 379,214 | 3.792 | 140 | 144 | fits | 28,024 | 52 | 0.450 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,715,071 | 17.151 | 140 | 144 | fits | 45,380 | 102 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 1,735,056 | 17.351 | 140 | 144 | fits | 45,380 | 102 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 1,914,739 | 19.147 | 140 | 144 | fits | 43,824 | 103 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,933,013 | 19.330 | 140 | 144 | fits | 43,824 | 103 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 2,114,753 | 21.148 | 140 | 144 | fits | 43,597 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 2,134,342 | 21.343 | 140 | 144 | fits | 43,597 | 102 | 0.209 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 2,330,853 | 23.309 | 140 | 144 | fits | 25,228 | 52 | 0.272 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 160,967 | 1.610 | 20 | 200 | fits | 147,475 | 257 | 0.340 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 469,554 | 4.696 | 20 | 20 | fits | 147,393 | 120 | 0.528 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 449,350 | 4.494 | 20 | 24 | fits | 147,393 | 120 | 0.528 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 430,079 | 4.301 | 20 | 50 | fits | 147,393 | 120 | 0.528 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 1,063,269 | 10.633 | 20 | 20 | fits | 79,061 | 30 | 0.646 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 524,803 | 5.248 | 140 | 144 | fits | 49,329 | 102 | 0.303 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 545,149 | 5.451 | 140 | 144 | fits | 49,329 | 102 | 0.303 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 1,754,065 | 17.541 | 140 | 144 | fits | 51,054 | 102 | 0.365 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 1,775,197 | 17.752 | 140 | 144 | fits | 51,054 | 102 | 0.365 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,882,922 | 18.829 | 140 | 144 | fits | 45,483 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,902,631 | 19.026 | 140 | 144 | fits | 45,483 | 102 | 0.234 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 2,082,512 | 20.825 | 140 | 144 | fits | 45,463 | 103 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 2,102,293 | 21.023 | 140 | 144 | fits | 45,463 | 103 | 0.233 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 589,941 | 5.899 | 140 | 144 | fits | 62,404 | 116 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 607,725 | 6.077 | 140 | 144 | fits | 62,404 | 116 | 0.315 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 2,280,889 | 22.809 | 140 | 144 | fits | 44,702 | 103 | 0.169 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 2,300,746 | 23.007 | 140 | 144 | fits | 44,702 | 103 | 0.169 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 501,571 | 5.016 | 20 | 200 | fits | 135,365 | 235 | 0.314 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 481,303 | 4.813 | 20 | 20 | fits | 135,365 | 235 | 0.314 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 325,734 | 3.257 | 20 | 24 | fits | 160,702 | 159 | 0.508 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 441,828 | 4.418 | 20 | 50 | fits | 135,365 | 235 | 0.314 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 1,069,713 | 10.697 | 20 | 20 | fits | 78,913 | 30 | 0.645 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 768,905 | 7.689 | 140 | 144 | fits | 29,035 | 52 | 0.476 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 1,782,195 | 17.822 | 140 | 144 | fits | 50,954 | 102 | 0.365 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 1,804,035 | 18.040 | 140 | 144 | fits | 50,954 | 102 | 0.365 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 1,913,212 | 19.132 | 140 | 144 | fits | 45,824 | 103 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 1,933,132 | 19.331 | 140 | 144 | fits | 45,824 | 103 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,113,839 | 21.138 | 140 | 144 | fits | 45,419 | 102 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 2,133,622 | 21.336 | 140 | 144 | fits | 45,419 | 102 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 2,313,438 | 23.134 | 140 | 144 | fits | 43,630 | 103 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 2,331,539 | 23.315 | 140 | 144 | fits | 43,630 | 103 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 2,513,296 | 25.133 | 140 | 144 | fits | 43,646 | 102 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 2,532,907 | 25.329 | 140 | 144 | fits | 43,646 | 102 | 0.214 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 2,729,445 | 27.294 | 140 | 144 | fits | 25,228 | 52 | 0.272 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 152,386 | 1.524 | 20 | 200 | fits | 149,980 | 253 | 0.329 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 468,035 | 4.680 | 20 | 20 | fits | 153,682 | 149 | 0.504 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 447,831 | 4.478 | 20 | 24 | fits | 153,682 | 149 | 0.504 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 428,560 | 4.286 | 20 | 50 | fits | 153,682 | 149 | 0.504 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 1,084,095 | 10.841 | 20 | 20 | fits | 38,377 | 18 | 0.808 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 728,492 | 7.285 | 140 | 144 | fits | 28,685 | 52 | 0.467 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 1,742,616 | 17.426 | 140 | 144 | fits | 50,954 | 102 | 0.365 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 1,764,456 | 17.645 | 140 | 144 | fits | 50,954 | 102 | 0.365 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 1,891,982 | 18.920 | 140 | 144 | fits | 45,824 | 103 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 1,911,902 | 19.119 | 140 | 144 | fits | 45,824 | 103 | 0.231 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 2,092,519 | 20.925 | 140 | 144 | fits | 45,419 | 102 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 2,112,302 | 21.123 | 140 | 144 | fits | 45,419 | 102 | 0.228 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 2,292,042 | 22.920 | 140 | 144 | fits | 43,630 | 103 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 2,310,143 | 23.101 | 140 | 144 | fits | 43,630 | 103 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 2,491,830 | 24.918 | 140 | 144 | fits | 43,619 | 102 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 2,511,441 | 25.114 | 140 | 144 | fits | 43,619 | 102 | 0.212 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 2,689,747 | 26.897 | 140 | 144 | fits | 25,228 | 52 | 0.272 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 146,722 | 1.467 | 20 | 200 | fits | 147,044 | 249 | 0.320 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 462,721 | 4.627 | 20 | 20 | fits | 154,294 | 149 | 0.508 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 442,517 | 4.425 | 20 | 24 | fits | 154,294 | 149 | 0.508 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 423,246 | 4.232 | 20 | 50 | fits | 154,294 | 149 | 0.508 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 1,078,985 | 10.790 | 20 | 20 | fits | 38,479 | 18 | 0.809 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 918,827 | 9.188 | 140 | 144 | fits | 27,937 | 52 | 0.457 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 1,763,874 | 17.639 | 140 | 144 | fits | 50,618 | 103 | 0.360 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,785,839 | 17.858 | 140 | 144 | fits | 50,618 | 103 | 0.360 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,910,726 | 19.107 | 140 | 144 | fits | 43,579 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 229,184 | 2.292 | 140 | 144 | fits | 48,587 | 102 | 0.286 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 249,887 | 2.499 | 140 | 144 | fits | 48,587 | 102 | 0.286 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 295,494 | 2.955 | 140 | 144 | fits | 66,447 | 118 | 0.332 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 315,876 | 3.159 | 140 | 144 | fits | 66,447 | 118 | 0.332 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 1,929,041 | 19.290 | 140 | 144 | fits | 43,579 | 102 | 0.207 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 2,102,816 | 21.028 | 140 | 144 | fits | 42,671 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 2,122,433 | 21.224 | 140 | 144 | fits | 42,671 | 102 | 0.191 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 383,328 | 3.833 | 140 | 144 | fits | 41,965 | 60 | 0.328 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 163,761 | 1.638 | 20 | 200 | fits | 152,684 | 263 | 0.334 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 461,908 | 4.619 | 20 | 20 | fits | 144,030 | 131 | 0.534 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 441,704 | 4.417 | 20 | 24 | fits | 144,030 | 131 | 0.534 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 422,433 | 4.224 | 20 | 50 | fits | 144,030 | 131 | 0.534 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 1,073,185 | 10.732 | 20 | 20 | fits | 38,019 | 18 | 0.809 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 280 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.acmp.if0` (notice-burst-4) | 12.106 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.adp.if0` (notice-burst-4) | 10.566 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-burst-4.held.aecp.if0` (notice-burst-4) | 11.904 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.maap.if0` (notice-burst-5) | 10.276 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.srp.if0` (notice-burst-5) | 7.008 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-6.mrpdu.periodic.if0` (notice-every-6) | 1.116 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-3.notices.29.9.0.if0` (notice-burst-3) | 12.691 (12.862) | fits | 1 events | 192 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1776 | 0 | 154,304 (1.543) | fits |
| notice-every-1 | 1760 | 0 | 152,172 (1.522) | fits |
| notice-every-2 | 1759 | 0 | 152,010 (1.520) | fits |
| notice-every-3 | 1767 | 0 | 153,245 (1.532) | fits |
| notice-every-4 | 1762 | 0 | 149,426 (1.494) | fits |
| notice-every-5 | 1763 | 0 | 156,234 (1.562) | fits |
| notice-every-6 | 1762 | 0 | 152,956 (1.530) | fits |
| notice-every-7 | 1763 | 0 | 154,325 (1.543) | fits |
| notice-burst-0 | 991 | 0 | 147,900 (1.479) | fits |
| notice-burst-1 | 951 | 0 | 157,388 (1.574) | fits |
| notice-burst-2 | 942 | 0 | 153,946 (1.539) | fits |
| notice-burst-3 | 961 | 0 | 165,634 (1.656) | fits |
| notice-burst-4 | 958 | 0 | 163,846 (1.638) | fits |
| notice-burst-5 | 954 | 0 | 166,266 (1.663) | fits |
| notice-burst-6 | 932 | 0 | 165,333 (1.653) | fits |
| notice-burst-7 | 965 | 0 | 156,001 (1.560) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 4.338 | 22 | 16 | 2 | within |
| notice-every-0 | 4.569 | 22 | 16 | 2 | within |
| notice-every-0 | 6.337 | 22 | 16 | 2 | within |
| notice-every-0 | 6.567 | 22 | 16 | 2 | within |
| notice-every-0 | 8.197 | 22 | 16 | 2 | within |
| notice-every-0 | 8.424 | 22 | 16 | 2 | within |
| notice-every-0 | 2.166 | 22 | 16 | 2 | within |
| notice-every-0 | 2.403 | 22 | 16 | 2 | within |
| notice-every-0 | 4.788 | 22 | 16 | 2 | within |
| notice-every-0 | 4.992 | 22 | 16 | 2 | within |
| notice-every-0 | 2.636 | 22 | 16 | 2 | within |
| notice-every-0 | 2.871 | 22 | 16 | 2 | within |
| notice-every-1 | 4.340 | 22 | 16 | 2 | within |
| notice-every-1 | 4.571 | 22 | 16 | 2 | within |
| notice-every-1 | 6.189 | 22 | 16 | 2 | within |
| notice-every-1 | 6.419 | 22 | 16 | 2 | within |
| notice-every-1 | 8.174 | 22 | 16 | 2 | within |
| notice-every-1 | 8.401 | 22 | 16 | 2 | within |
| notice-every-1 | 2.168 | 22 | 16 | 2 | within |
| notice-every-1 | 2.404 | 22 | 16 | 2 | within |
| notice-every-1 | 4.790 | 22 | 16 | 2 | within |
| notice-every-1 | 4.994 | 22 | 16 | 2 | within |
| notice-every-1 | 2.638 | 22 | 16 | 2 | within |
| notice-every-1 | 2.873 | 22 | 16 | 2 | within |
| notice-every-2 | 5.884 | 22 | 16 | 2 | within |
| notice-every-2 | 6.112 | 22 | 16 | 2 | within |
| notice-every-2 | 7.861 | 22 | 16 | 2 | within |
| notice-every-2 | 8.091 | 22 | 16 | 2 | within |
| notice-every-2 | 1.814 | 22 | 16 | 2 | within |
| notice-every-2 | 2.050 | 22 | 16 | 2 | within |
| notice-every-2 | 2.274 | 22 | 16 | 2 | within |
| notice-every-2 | 2.501 | 22 | 16 | 2 | within |
| notice-every-2 | 6.329 | 22 | 16 | 2 | within |
| notice-every-2 | 6.530 | 22 | 16 | 2 | within |
| notice-every-2 | 2.732 | 22 | 16 | 2 | within |
| notice-every-2 | 2.965 | 22 | 16 | 2 | within |
| notice-every-3 | 5.941 | 22 | 16 | 2 | within |
| notice-every-3 | 6.170 | 22 | 16 | 2 | within |
| notice-every-3 | 7.890 | 22 | 16 | 2 | within |
| notice-every-3 | 8.120 | 22 | 16 | 2 | within |
| notice-every-3 | 1.975 | 22 | 16 | 2 | within |
| notice-every-3 | 2.211 | 22 | 16 | 2 | within |
| notice-every-3 | 3.882 | 22 | 16 | 2 | within |
| notice-every-3 | 4.113 | 22 | 16 | 2 | within |
| notice-every-3 | 6.386 | 22 | 16 | 2 | within |
| notice-every-3 | 6.588 | 22 | 16 | 2 | within |
| notice-every-3 | 2.445 | 22 | 16 | 2 | within |
| notice-every-3 | 2.680 | 22 | 16 | 2 | within |
| notice-every-4 | 5.941 | 22 | 16 | 2 | within |
| notice-every-4 | 6.170 | 22 | 16 | 2 | within |
| notice-every-4 | 7.890 | 22 | 16 | 2 | within |
| notice-every-4 | 8.120 | 22 | 16 | 2 | within |
| notice-every-4 | 1.975 | 22 | 16 | 2 | within |
| notice-every-4 | 2.211 | 22 | 16 | 2 | within |
| notice-every-4 | 3.882 | 22 | 16 | 2 | within |
| notice-every-4 | 4.113 | 22 | 16 | 2 | within |
| notice-every-4 | 6.386 | 22 | 16 | 2 | within |
| notice-every-4 | 6.588 | 22 | 16 | 2 | within |
| notice-every-4 | 2.445 | 22 | 16 | 2 | within |
| notice-every-4 | 2.680 | 22 | 16 | 2 | within |
| notice-every-5 | 7.862 | 22 | 16 | 2 | within |
| notice-every-5 | 8.091 | 22 | 16 | 2 | within |
| notice-every-5 | 1.885 | 22 | 16 | 2 | within |
| notice-every-5 | 2.123 | 22 | 16 | 2 | within |
| notice-every-5 | 3.957 | 22 | 16 | 2 | within |
| notice-every-5 | 4.186 | 22 | 16 | 2 | within |
| notice-every-5 | 5.847 | 22 | 16 | 2 | within |
| notice-every-5 | 6.077 | 22 | 16 | 2 | within |
| notice-every-5 | 8.305 | 22 | 16 | 2 | within |
| notice-every-5 | 8.504 | 22 | 16 | 2 | within |
| notice-every-5 | 2.358 | 22 | 16 | 2 | within |
| notice-every-5 | 2.594 | 22 | 16 | 2 | within |
| notice-every-6 | 7.915 | 22 | 16 | 2 | within |
| notice-every-6 | 8.142 | 22 | 16 | 2 | within |
| notice-every-6 | 1.920 | 22 | 16 | 2 | within |
| notice-every-6 | 2.159 | 22 | 16 | 2 | within |
| notice-every-6 | 3.831 | 22 | 16 | 2 | within |
| notice-every-6 | 4.061 | 22 | 16 | 2 | within |
| notice-every-6 | 5.878 | 22 | 16 | 2 | within |
| notice-every-6 | 6.106 | 22 | 16 | 2 | within |
| notice-every-6 | 8.357 | 22 | 16 | 2 | within |
| notice-every-6 | 8.556 | 22 | 16 | 2 | within |
| notice-every-6 | 2.393 | 22 | 16 | 2 | within |
| notice-every-6 | 2.629 | 22 | 16 | 2 | within |
| notice-every-7 | 2.176 | 22 | 16 | 2 | within |
| notice-every-7 | 2.405 | 22 | 16 | 2 | within |
| notice-every-7 | 4.773 | 22 | 16 | 2 | within |
| notice-every-7 | 5.007 | 22 | 16 | 2 | within |
| notice-every-7 | 6.178 | 22 | 16 | 2 | within |
| notice-every-7 | 6.405 | 22 | 16 | 2 | within |
| notice-every-7 | 8.308 | 22 | 16 | 2 | within |
| notice-every-7 | 8.533 | 22 | 16 | 2 | within |
| notice-every-7 | 2.625 | 22 | 16 | 2 | within |
| notice-every-7 | 2.832 | 22 | 16 | 2 | within |
| notice-every-7 | 3.062 | 22 | 16 | 2 | within |
| notice-every-7 | 3.296 | 22 | 16 | 2 | within |
| notice-burst-0 | 9.168 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.404 | 22 | 16 | 1 | within |
| notice-burst-0 | 11.275 | 22 | 16 | 1 | within |
| notice-burst-0 | 11.510 | 22 | 16 | 1 | within |
| notice-burst-0 | 2.518 | 22 | 16 | 1 | within |
| notice-burst-0 | 2.752 | 22 | 16 | 1 | within |
| notice-burst-0 | 3.176 | 22 | 16 | 1 | within |
| notice-burst-0 | 3.407 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.623 | 22 | 16 | 1 | within |
| notice-burst-0 | 9.825 | 22 | 16 | 1 | within |
| notice-burst-0 | 10.050 | 22 | 16 | 1 | within |
| notice-burst-0 | 4.257 | 22 | 16 | 1 | within |
| notice-burst-1 | 8.499 | 22 | 16 | 2 | within |
| notice-burst-1 | 8.732 | 22 | 16 | 2 | within |
| notice-burst-1 | 10.601 | 22 | 16 | 2 | within |
| notice-burst-1 | 10.836 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.172 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.404 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.627 | 22 | 16 | 2 | within |
| notice-burst-1 | 2.855 | 22 | 16 | 2 | within |
| notice-burst-1 | 8.951 | 22 | 16 | 2 | within |
| notice-burst-1 | 9.153 | 22 | 16 | 2 | within |
| notice-burst-1 | 9.379 | 22 | 16 | 2 | within |
| notice-burst-1 | 5.704 | 22 | 16 | 2 | within |
| notice-burst-2 | 8.700 | 22 | 16 | 0 | within |
| notice-burst-2 | 8.934 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.114 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.348 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.572 | 22 | 16 | 0 | within |
| notice-burst-2 | 2.797 | 22 | 16 | 0 | within |
| notice-burst-2 | 3.018 | 22 | 16 | 0 | within |
| notice-burst-2 | 3.243 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.150 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.350 | 22 | 16 | 0 | within |
| notice-burst-2 | 9.573 | 22 | 16 | 0 | within |
| notice-burst-2 | 5.091 | 22 | 16 | 0 | within |
| notice-burst-3 | 9.321 | 22 | 16 | 1 | within |
| notice-burst-3 | 9.553 | 22 | 16 | 1 | within |
| notice-burst-3 | 9.784 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.010 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.232 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.454 | 22 | 16 | 1 | within |
| notice-burst-3 | 3.749 | 22 | 16 | 1 | within |
| notice-burst-3 | 3.986 | 22 | 16 | 1 | within |
| notice-burst-3 | 10.668 | 22 | 16 | 1 | within |
| notice-burst-3 | 12.462 | 22 | 16 | 1 | within |
| notice-burst-3 | 12.691 | 22 | 16 | 1 | within |
| notice-burst-3 | 4.222 | 22 | 16 | 1 | within |
| notice-burst-4 | 8.443 | 22 | 16 | 0 | within |
| notice-burst-4 | 8.673 | 22 | 16 | 0 | within |
| notice-burst-4 | 8.905 | 22 | 16 | 0 | within |
| notice-burst-4 | 9.130 | 22 | 16 | 0 | within |
| notice-burst-4 | 11.642 | 22 | 16 | 0 | within |
| notice-burst-4 | 11.872 | 22 | 16 | 0 | within |
| notice-burst-4 | 2.684 | 22 | 16 | 0 | within |
| notice-burst-4 | 2.921 | 22 | 16 | 0 | within |
| notice-burst-4 | 9.348 | 22 | 16 | 0 | within |
| notice-burst-4 | 9.549 | 22 | 16 | 0 | within |
| notice-burst-4 | 9.775 | 22 | 16 | 0 | within |
| notice-burst-4 | 4.623 | 22 | 16 | 0 | within |
| notice-burst-5 | 7.713 | 22 | 16 | 1 | within |
| notice-burst-5 | 7.945 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.175 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.400 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.621 | 22 | 16 | 1 | within |
| notice-burst-5 | 8.845 | 22 | 16 | 1 | within |
| notice-burst-5 | 10.754 | 22 | 16 | 1 | within |
| notice-burst-5 | 10.987 | 22 | 16 | 1 | within |
| notice-burst-5 | 9.061 | 22 | 16 | 1 | within |
| notice-burst-5 | 11.197 | 22 | 16 | 1 | within |
| notice-burst-5 | 11.420 | 22 | 16 | 1 | within |
| notice-burst-5 | 11.645 | 22 | 16 | 1 | within |
| notice-burst-6 | 6.610 | 22 | 16 | 1 | within |
| notice-burst-6 | 6.840 | 22 | 16 | 1 | within |
| notice-burst-6 | 7.071 | 22 | 16 | 1 | within |
| notice-burst-6 | 7.297 | 22 | 16 | 1 | within |
| notice-burst-6 | 9.639 | 22 | 16 | 1 | within |
| notice-burst-6 | 9.873 | 22 | 16 | 1 | within |
| notice-burst-6 | 10.094 | 22 | 16 | 1 | within |
| notice-burst-6 | 10.317 | 22 | 16 | 1 | within |
| notice-burst-6 | 7.516 | 22 | 16 | 1 | within |
| notice-burst-6 | 7.721 | 22 | 16 | 1 | within |
| notice-burst-6 | 7.949 | 22 | 16 | 1 | within |
| notice-burst-6 | 10.541 | 22 | 16 | 1 | within |
| notice-burst-7 | 8.997 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.231 | 22 | 16 | 1 | within |
| notice-burst-7 | 11.416 | 22 | 16 | 1 | within |
| notice-burst-7 | 11.650 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.341 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.575 | 22 | 16 | 1 | within |
| notice-burst-7 | 2.798 | 22 | 16 | 1 | within |
| notice-burst-7 | 3.026 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.451 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.653 | 22 | 16 | 1 | within |
| notice-burst-7 | 9.878 | 22 | 16 | 1 | within |
| notice-burst-7 | 3.617 | 22 | 16 | 1 | within |

Latest: 12.691 ms, notice-burst-3.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 306 | 97,386 (0.974) | 76,393 (0.764) |
| notice-every-1 | 306 | 101,568 (1.016) | 76,393 (0.764) |
| notice-every-2 | 306 | 106,608 (1.066) | 76,454 (0.765) |
| notice-every-3 | 306 | 86,941 (0.869) | 75,897 (0.759) |
| notice-every-4 | 306 | 87,672 (0.877) | 75,947 (0.759) |
| notice-every-5 | 306 | 88,449 (0.884) | 76,239 (0.762) |
| notice-every-6 | 306 | 86,941 (0.869) | 75,920 (0.759) |
| notice-every-7 | 306 | 86,941 (0.869) | 75,897 (0.759) |
| notice-burst-0 | 316 | 109,160 (1.092) | 77,935 (0.779) |
| notice-burst-1 | 316 | 101,568 (1.016) | 77,935 (0.779) |
| notice-burst-2 | 316 | 106,608 (1.066) | 77,935 (0.779) |
| notice-burst-3 | 316 | 99,280 (0.993) | 78,049 (0.780) |
| notice-burst-4 | 316 | 97,213 (0.972) | 78,049 (0.780) |
| notice-burst-5 | 316 | 101,308 (1.013) | 77,935 (0.779) |
| notice-burst-6 | 316 | 105,062 (1.051) | 78,049 (0.780) |
| notice-burst-7 | 316 | 114,644 (1.146) | 78,049 (0.780) |

Longest pass that carries a step: 114,644 CPU cycles (1.146 ms), notice-burst-7; longest step: 78,049 (0.780 ms), notice-burst-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 433,790 | 4.338 | 22 | 26 | fits | 95,396 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 456,907 | 4.569 | 22 | 26 | fits | 95,396 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 633,683 | 6.337 | 22 | 26 | fits | 52,577 | 103 | 0.248 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 656,705 | 6.567 | 22 | 26 | fits | 52,577 | 103 | 0.248 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 819,730 | 8.197 | 22 | 26 | fits | 50,413 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 842,414 | 8.424 | 22 | 26 | fits | 50,413 | 102 | 0.244 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 216,643 | 2.166 | 22 | 26 | fits | 100,887 | 206 | 0.162 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 240,255 | 2.403 | 22 | 26 | fits | 100,887 | 206 | 0.162 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 478,789 | 4.788 | 22 | 26 | fits | 95,396 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 499,200 | 4.992 | 22 | 26 | fits | 95,396 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 263,594 | 2.636 | 22 | 26 | fits | 100,887 | 206 | 0.162 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 287,122 | 2.871 | 22 | 26 | fits | 100,887 | 206 | 0.162 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if0` | 687,051 | 6.871 | 20 | 200 | fits | 154,304 | 164 | 0.509 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 811,699 | 8.117 | 20 | 20 | fits | 144,916 | 112 | 0.528 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if0` | 912,375 | 9.124 | 20 | 24 | fits | 107,992 | 100 | 0.392 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 772,224 | 7.722 | 20 | 50 | fits | 144,916 | 112 | 0.528 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if0` | 432,557 | 4.326 | 20 | 20 | fits | 82,424 | 44 | 0.537 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 107,918 | 1.079 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 433,981 | 4.340 | 22 | 26 | fits | 95,396 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 457,098 | 4.571 | 22 | 26 | fits | 95,396 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 618,909 | 6.189 | 22 | 26 | fits | 52,498 | 103 | 0.248 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 641,931 | 6.419 | 22 | 26 | fits | 52,498 | 103 | 0.248 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 817,444 | 8.174 | 22 | 26 | fits | 50,434 | 102 | 0.242 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 840,070 | 8.401 | 22 | 26 | fits | 50,434 | 102 | 0.242 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 216,834 | 2.168 | 22 | 26 | fits | 100,887 | 206 | 0.162 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 240,446 | 2.404 | 22 | 26 | fits | 100,887 | 206 | 0.162 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 478,980 | 4.790 | 22 | 26 | fits | 95,396 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 499,391 | 4.994 | 22 | 26 | fits | 95,396 | 201 | 0.192 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 263,785 | 2.638 | 22 | 26 | fits | 100,887 | 206 | 0.162 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 287,313 | 2.873 | 22 | 26 | fits | 100,887 | 206 | 0.162 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if0` | 657,117 | 6.571 | 20 | 200 | fits | 148,295 | 143 | 0.527 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 956,720 | 9.567 | 20 | 20 | fits | 141,268 | 119 | 0.436 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if0` | 936,516 | 9.365 | 20 | 24 | fits | 141,268 | 119 | 0.436 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 762,478 | 7.625 | 20 | 50 | fits | 146,831 | 151 | 0.514 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if0` | 427,054 | 4.271 | 20 | 20 | fits | 84,754 | 49 | 0.561 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 109,157 | 1.092 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 588,356 | 5.884 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 611,219 | 6.112 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 786,124 | 7.861 | 22 | 26 | fits | 52,258 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 809,138 | 8.091 | 22 | 26 | fits | 52,258 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 181,427 | 1.814 | 22 | 26 | fits | 145,226 | 304 | 0.126 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 204,982 | 2.050 | 22 | 26 | fits | 145,226 | 304 | 0.126 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 227,359 | 2.274 | 22 | 26 | fits | 145,226 | 304 | 0.126 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 250,054 | 2.501 | 22 | 26 | fits | 145,226 | 304 | 0.126 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 632,870 | 6.329 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 653,050 | 6.530 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 273,234 | 2.732 | 22 | 26 | fits | 145,226 | 304 | 0.126 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 296,538 | 2.965 | 22 | 26 | fits | 145,226 | 304 | 0.126 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if0` | 153,279 | 1.533 | 20 | 200 | fits | 148,947 | 149 | 0.488 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 949,256 | 9.493 | 20 | 20 | fits | 126,306 | 107 | 0.458 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if0` | 929,052 | 9.291 | 20 | 24 | fits | 126,306 | 107 | 0.458 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 766,295 | 7.663 | 20 | 50 | fits | 149,425 | 128 | 0.499 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if0` | 435,012 | 4.350 | 20 | 20 | fits | 82,830 | 43 | 0.545 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 104,267 | 1.043 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 594,091 | 5.941 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 616,954 | 6.170 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 788,982 | 7.890 | 22 | 26 | fits | 52,179 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 811,996 | 8.120 | 22 | 26 | fits | 52,179 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 197,514 | 1.975 | 22 | 26 | fits | 100,923 | 204 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 221,069 | 2.211 | 22 | 26 | fits | 100,923 | 204 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 388,185 | 3.882 | 22 | 26 | fits | 52,215 | 102 | 0.235 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 411,327 | 4.113 | 22 | 26 | fits | 52,215 | 102 | 0.235 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 638,605 | 6.386 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 658,785 | 6.588 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 244,473 | 2.445 | 22 | 26 | fits | 100,923 | 204 | 0.169 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 268,001 | 2.680 | 22 | 26 | fits | 100,923 | 204 | 0.169 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if0` | 859,418 | 8.594 | 20 | 200 | fits | 147,928 | 116 | 0.534 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 839,150 | 8.392 | 20 | 20 | fits | 147,928 | 116 | 0.534 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if0` | 924,315 | 9.243 | 20 | 24 | fits | 105,369 | 91 | 0.377 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 799,675 | 7.997 | 20 | 50 | fits | 147,928 | 116 | 0.534 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if0` | 453,311 | 4.533 | 20 | 20 | fits | 82,870 | 43 | 0.546 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 88,871 | 0.889 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 594,091 | 5.941 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 616,954 | 6.170 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 788,982 | 7.890 | 22 | 26 | fits | 52,179 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 811,996 | 8.120 | 22 | 26 | fits | 52,179 | 102 | 0.252 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 197,514 | 1.975 | 22 | 26 | fits | 100,923 | 204 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 221,069 | 2.211 | 22 | 26 | fits | 100,923 | 204 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 388,185 | 3.882 | 22 | 26 | fits | 52,215 | 102 | 0.235 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 411,327 | 4.113 | 22 | 26 | fits | 52,215 | 102 | 0.235 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 638,605 | 6.386 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 658,785 | 6.588 | 22 | 26 | fits | 93,910 | 202 | 0.177 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 244,473 | 2.445 | 22 | 26 | fits | 100,923 | 204 | 0.169 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 268,001 | 2.680 | 22 | 26 | fits | 100,923 | 204 | 0.169 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if0` | 666,209 | 6.662 | 20 | 200 | fits | 148,242 | 140 | 0.530 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 953,575 | 9.536 | 20 | 20 | fits | 135,983 | 108 | 0.433 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if0` | 933,371 | 9.334 | 20 | 24 | fits | 135,983 | 108 | 0.433 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 765,431 | 7.654 | 20 | 50 | fits | 145,334 | 144 | 0.502 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if0` | 436,199 | 4.362 | 20 | 20 | fits | 84,982 | 49 | 0.566 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 87,190 | 0.872 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 786,201 | 7.862 | 22 | 26 | fits | 92,990 | 201 | 0.177 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 809,050 | 8.091 | 22 | 26 | fits | 92,990 | 201 | 0.177 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 188,510 | 1.885 | 22 | 26 | fits | 102,773 | 204 | 0.183 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 212,348 | 2.123 | 22 | 26 | fits | 102,773 | 204 | 0.183 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 395,650 | 3.957 | 22 | 26 | fits | 51,875 | 102 | 0.240 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 418,569 | 4.186 | 22 | 26 | fits | 51,875 | 102 | 0.240 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 584,749 | 5.847 | 22 | 26 | fits | 51,425 | 103 | 0.234 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 607,653 | 6.077 | 22 | 26 | fits | 51,425 | 103 | 0.234 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 830,470 | 8.305 | 22 | 26 | fits | 92,990 | 201 | 0.177 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 850,419 | 8.504 | 22 | 26 | fits | 92,990 | 201 | 0.177 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 235,831 | 2.358 | 22 | 26 | fits | 102,773 | 204 | 0.183 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 259,359 | 2.594 | 22 | 26 | fits | 102,773 | 204 | 0.183 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if0` | 153,163 | 1.532 | 20 | 200 | fits | 152,428 | 157 | 0.484 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 815,826 | 8.158 | 20 | 20 | fits | 143,756 | 105 | 0.526 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if0` | 929,621 | 9.296 | 20 | 24 | fits | 121,197 | 104 | 0.364 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 776,351 | 7.764 | 20 | 50 | fits | 143,756 | 105 | 0.526 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if0` | 441,007 | 4.410 | 20 | 20 | fits | 82,855 | 45 | 0.540 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 107,889 | 1.079 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 791,450 | 7.915 | 22 | 26 | fits | 92,932 | 201 | 0.176 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 814,241 | 8.142 | 22 | 26 | fits | 92,932 | 201 | 0.176 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 191,968 | 1.920 | 22 | 26 | fits | 102,897 | 204 | 0.184 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 215,856 | 2.159 | 22 | 26 | fits | 102,897 | 204 | 0.184 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 383,108 | 3.831 | 22 | 26 | fits | 51,854 | 102 | 0.242 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 406,085 | 4.061 | 22 | 26 | fits | 51,854 | 102 | 0.242 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 587,788 | 5.878 | 22 | 26 | fits | 51,446 | 103 | 0.232 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 610,634 | 6.106 | 22 | 26 | fits | 51,446 | 103 | 0.232 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 835,661 | 8.357 | 22 | 26 | fits | 92,932 | 201 | 0.176 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 855,610 | 8.556 | 22 | 26 | fits | 92,932 | 201 | 0.176 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 239,339 | 2.393 | 22 | 26 | fits | 102,897 | 204 | 0.184 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 262,867 | 2.629 | 22 | 26 | fits | 102,897 | 204 | 0.184 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if0` | 843,834 | 8.438 | 20 | 200 | fits | 151,441 | 130 | 0.501 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 823,566 | 8.236 | 20 | 20 | fits | 151,441 | 130 | 0.501 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if0` | 923,343 | 9.233 | 20 | 24 | fits | 106,637 | 92 | 0.382 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 784,091 | 7.841 | 20 | 50 | fits | 151,441 | 130 | 0.501 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if0` | 445,041 | 4.450 | 20 | 20 | fits | 83,703 | 49 | 0.538 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 111,565 | 1.116 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 217,572 | 2.176 | 22 | 26 | fits | 143,036 | 305 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 240,549 | 2.405 | 22 | 26 | fits | 143,036 | 305 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 477,312 | 4.773 | 22 | 26 | fits | 53,906 | 102 | 0.276 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 500,669 | 5.007 | 22 | 26 | fits | 53,906 | 102 | 0.276 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 617,787 | 6.178 | 22 | 26 | fits | 50,760 | 103 | 0.244 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 640,543 | 6.405 | 22 | 26 | fits | 50,760 | 103 | 0.244 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 830,786 | 8.308 | 22 | 26 | fits | 50,237 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 853,329 | 8.533 | 22 | 26 | fits | 50,237 | 102 | 0.233 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 262,511 | 2.625 | 22 | 26 | fits | 143,036 | 305 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 283,227 | 2.832 | 22 | 26 | fits | 143,036 | 305 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 306,186 | 3.062 | 22 | 26 | fits | 143,036 | 305 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 329,562 | 3.296 | 22 | 26 | fits | 143,036 | 305 | 0.143 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if0` | 871,919 | 8.719 | 20 | 200 | fits | 149,157 | 120 | 0.537 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 851,651 | 8.517 | 20 | 20 | fits | 149,157 | 120 | 0.537 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if0` | 936,293 | 9.363 | 20 | 24 | fits | 104,846 | 85 | 0.380 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 812,176 | 8.122 | 20 | 50 | fits | 149,157 | 120 | 0.537 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if0` | 455,460 | 4.555 | 20 | 20 | fits | 83,726 | 51 | 0.533 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 94,775 | 0.948 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 916,812 | 9.168 | 22 | 26 | fits | 120,030 | 252 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 940,362 | 9.404 | 22 | 26 | fits | 120,030 | 252 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 1,127,500 | 11.275 | 22 | 26 | fits | 54,075 | 102 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 1,150,983 | 11.510 | 22 | 26 | fits | 54,075 | 102 | 0.305 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 251,778 | 2.518 | 22 | 26 | fits | 54,677 | 102 | 0.281 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 275,160 | 2.752 | 22 | 26 | fits | 54,677 | 102 | 0.281 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 317,648 | 3.176 | 22 | 26 | fits | 65,951 | 115 | 0.327 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 340,725 | 3.407 | 22 | 26 | fits | 65,951 | 115 | 0.327 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 962,297 | 9.623 | 22 | 26 | fits | 120,030 | 252 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 982,479 | 9.825 | 22 | 26 | fits | 120,030 | 252 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 1,005,048 | 10.050 | 22 | 26 | fits | 120,030 | 252 | 0.204 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 425,738 | 4.257 | 22 | 26 | fits | 39,560 | 61 | 0.325 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if0` | 805,077 | 8.051 | 20 | 200 | fits | 144,121 | 147 | 0.568 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 1,062,090 | 10.621 | 20 | 20 | fits | 129,381 | 98 | 0.424 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if0` | 1,041,886 | 10.419 | 20 | 24 | fits | 129,381 | 98 | 0.424 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 893,234 | 8.932 | 20 | 50 | fits | 147,900 | 123 | 0.515 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if0` | 525,113 | 5.251 | 20 | 20 | fits | 91,600 | 66 | 0.584 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 849,930 | 8.499 | 22 | 26 | fits | 119,342 | 252 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 873,228 | 8.732 | 22 | 26 | fits | 119,342 | 252 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 1,060,115 | 10.601 | 22 | 26 | fits | 54,120 | 102 | 0.309 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 1,083,598 | 10.836 | 22 | 26 | fits | 54,120 | 102 | 0.309 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 217,240 | 2.172 | 22 | 26 | fits | 109,081 | 212 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 240,443 | 2.404 | 22 | 26 | fits | 109,081 | 212 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 262,749 | 2.627 | 22 | 26 | fits | 109,081 | 212 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 285,516 | 2.855 | 22 | 26 | fits | 109,081 | 212 | 0.188 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 895,132 | 8.951 | 22 | 26 | fits | 119,342 | 252 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 915,314 | 9.153 | 22 | 26 | fits | 119,342 | 252 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 937,883 | 9.379 | 22 | 26 | fits | 119,342 | 252 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 570,368 | 5.704 | 22 | 26 | fits | 31,207 | 53 | 0.370 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if0` | 150,032 | 1.500 | 20 | 200 | fits | 150,841 | 150 | 0.493 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 981,893 | 9.819 | 20 | 20 | fits | 157,388 | 112 | 0.524 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if0` | 1,077,650 | 10.777 | 20 | 24 | fits | 115,961 | 96 | 0.370 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 942,418 | 9.424 | 20 | 50 | fits | 157,388 | 112 | 0.524 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if0` | 557,519 | 5.575 | 20 | 20 | fits | 91,405 | 66 | 0.581 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 870,017 | 8.700 | 22 | 26 | fits | 118,268 | 253 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 893,387 | 8.934 | 22 | 26 | fits | 118,268 | 253 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 211,445 | 2.114 | 22 | 26 | fits | 144,545 | 303 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 234,800 | 2.348 | 22 | 26 | fits | 144,545 | 303 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 257,167 | 2.572 | 22 | 26 | fits | 144,545 | 303 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 279,703 | 2.797 | 22 | 26 | fits | 144,545 | 303 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 301,776 | 3.018 | 22 | 26 | fits | 144,545 | 303 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 324,319 | 3.243 | 22 | 26 | fits | 144,545 | 303 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 915,012 | 9.150 | 22 | 26 | fits | 118,268 | 253 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 934,963 | 9.350 | 22 | 26 | fits | 118,268 | 253 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 957,301 | 9.573 | 22 | 26 | fits | 118,268 | 253 | 0.192 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 509,107 | 5.091 | 22 | 26 | fits | 30,323 | 52 | 0.357 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if0` | 986,233 | 9.862 | 20 | 200 | fits | 144,069 | 109 | 0.521 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 1,083,555 | 10.836 | 20 | 20 | fits | 117,590 | 91 | 0.434 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if0` | 1,063,351 | 10.634 | 20 | 24 | fits | 117,590 | 91 | 0.434 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 926,490 | 9.265 | 20 | 50 | fits | 144,069 | 109 | 0.521 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if0` | 493,561 | 4.936 | 20 | 20 | fits | 81,820 | 44 | 0.537 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 932,093 | 9.321 | 22 | 26 | fits | 165,634 | 355 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 955,275 | 9.553 | 22 | 26 | fits | 165,634 | 355 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 978,409 | 9.784 | 22 | 26 | fits | 165,634 | 355 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,001,043 | 10.010 | 22 | 26 | fits | 165,634 | 355 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 1,023,194 | 10.232 | 22 | 26 | fits | 165,634 | 355 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 1,045,427 | 10.454 | 22 | 26 | fits | 165,634 | 355 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 374,936 | 3.749 | 22 | 26 | fits | 78,802 | 153 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 398,637 | 3.986 | 22 | 26 | fits | 78,802 | 153 | 0.230 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 1,066,847 | 10.668 | 22 | 26 | fits | 165,634 | 355 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 1,246,210 | 12.462 | 22 | 26 | fits | 49,334 | 102 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 1,269,062 | 12.691 | 22 | 26 | fits | 49,334 | 102 | 0.248 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 422,182 | 4.222 | 22 | 26 | fits | 78,802 | 153 | 0.230 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if0` | 707,779 | 7.078 | 20 | 200 | fits | 147,525 | 141 | 0.536 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 1,191,077 | 11.911 | 20 | 20 | fits | 135,970 | 112 | 0.427 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if0` | 1,170,873 | 11.709 | 20 | 24 | fits | 135,970 | 112 | 0.427 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 966,298 | 9.663 | 20 | 50 | fits | 152,628 | 145 | 0.552 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if0` | 478,486 | 4.785 | 20 | 20 | fits | 81,892 | 42 | 0.538 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 844,276 | 8.443 | 22 | 26 | fits | 163,846 | 353 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 867,321 | 8.673 | 22 | 26 | fits | 163,846 | 353 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 890,459 | 8.905 | 22 | 26 | fits | 163,846 | 353 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 913,021 | 9.130 | 22 | 26 | fits | 163,846 | 353 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 1,164,237 | 11.642 | 22 | 26 | fits | 52,474 | 103 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 1,187,207 | 11.872 | 22 | 26 | fits | 52,474 | 103 | 0.294 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 268,420 | 2.684 | 22 | 26 | fits | 55,692 | 103 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 292,121 | 2.921 | 22 | 26 | fits | 55,692 | 103 | 0.301 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 934,751 | 9.348 | 22 | 26 | fits | 163,846 | 353 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 954,933 | 9.549 | 22 | 26 | fits | 163,846 | 353 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 977,502 | 9.775 | 22 | 26 | fits | 163,846 | 353 | 0.140 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 462,305 | 4.623 | 22 | 26 | fits | 32,137 | 52 | 0.385 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if0` | 1,056,637 | 10.566 | 20 | 200 | fits | 156,967 | 149 | 0.556 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 1,210,622 | 12.106 | 20 | 20 | fits | 121,779 | 100 | 0.457 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if0` | 1,190,418 | 11.904 | 20 | 24 | fits | 121,779 | 100 | 0.457 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 996,894 | 9.969 | 20 | 50 | fits | 156,967 | 149 | 0.556 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if0` | 504,509 | 5.045 | 20 | 20 | fits | 82,399 | 42 | 0.551 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 771,278 | 7.713 | 22 | 26 | fits | 166,266 | 353 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 794,489 | 7.945 | 22 | 26 | fits | 166,266 | 353 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 817,487 | 8.175 | 22 | 26 | fits | 166,266 | 353 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 840,049 | 8.400 | 22 | 26 | fits | 166,266 | 353 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 862,135 | 8.621 | 22 | 26 | fits | 166,266 | 353 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 884,519 | 8.845 | 22 | 26 | fits | 166,266 | 353 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 1,075,398 | 10.754 | 22 | 26 | fits | 119,179 | 254 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 1,098,693 | 10.987 | 22 | 26 | fits | 119,179 | 254 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 906,098 | 9.061 | 22 | 26 | fits | 166,266 | 353 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 1,119,729 | 11.197 | 22 | 26 | fits | 119,179 | 254 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 1,141,999 | 11.420 | 22 | 26 | fits | 119,179 | 254 | 0.179 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 1,164,473 | 11.645 | 22 | 26 | fits | 119,179 | 254 | 0.179 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if0` | 152,455 | 1.525 | 20 | 200 | fits | 152,998 | 157 | 0.491 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 1,067,105 | 10.671 | 20 | 20 | fits | 154,214 | 115 | 0.495 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if0` | 1,147,639 | 11.476 | 20 | 24 | fits | 100,738 | 84 | 0.377 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 1,027,630 | 10.276 | 20 | 50 | fits | 154,214 | 115 | 0.495 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if0` | 700,824 | 7.008 | 20 | 20 | fits | 86,490 | 48 | 0.561 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 661,035 | 6.610 | 22 | 26 | fits | 165,333 | 353 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 684,037 | 6.840 | 22 | 26 | fits | 165,333 | 353 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 707,096 | 7.071 | 22 | 26 | fits | 165,333 | 353 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 729,658 | 7.297 | 22 | 26 | fits | 165,333 | 353 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 963,944 | 9.639 | 22 | 26 | fits | 120,132 | 253 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 987,320 | 9.873 | 22 | 26 | fits | 120,132 | 253 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 1,009,367 | 10.094 | 22 | 26 | fits | 120,132 | 253 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 1,031,672 | 10.317 | 22 | 26 | fits | 120,132 | 253 | 0.171 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 751,619 | 7.516 | 22 | 26 | fits | 165,333 | 353 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 772,111 | 7.721 | 22 | 26 | fits | 165,333 | 353 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 794,911 | 7.949 | 22 | 26 | fits | 165,333 | 353 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 1,054,139 | 10.541 | 22 | 26 | fits | 120,132 | 253 | 0.171 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if0` | 142,384 | 1.424 | 20 | 200 | fits | 144,667 | 130 | 0.487 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 1,161,820 | 11.618 | 20 | 20 | fits | 114,861 | 86 | 0.445 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if0` | 1,141,616 | 11.416 | 20 | 24 | fits | 114,861 | 86 | 0.445 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 1,007,484 | 10.075 | 20 | 50 | fits | 145,358 | 124 | 0.489 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if0` | 690,739 | 6.907 | 20 | 20 | fits | 86,596 | 48 | 0.560 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 899,743 | 8.997 | 22 | 26 | fits | 119,829 | 252 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 923,142 | 9.231 | 22 | 26 | fits | 119,829 | 252 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 1,141,564 | 11.416 | 22 | 26 | fits | 54,142 | 102 | 0.307 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 1,165,047 | 11.650 | 22 | 26 | fits | 54,142 | 102 | 0.307 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 234,127 | 2.341 | 22 | 26 | fits | 99,261 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 257,516 | 2.575 | 22 | 26 | fits | 99,261 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 279,822 | 2.798 | 22 | 26 | fits | 99,261 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 302,589 | 3.026 | 22 | 26 | fits | 99,261 | 203 | 0.174 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 945,077 | 9.451 | 22 | 26 | fits | 119,829 | 252 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 965,259 | 9.653 | 22 | 26 | fits | 119,829 | 252 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 987,828 | 9.878 | 22 | 26 | fits | 119,829 | 252 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 361,711 | 3.617 | 22 | 26 | fits | 114,644 | 60 | 0.225 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if0` | 151,113 | 1.511 | 20 | 200 | fits | 151,720 | 150 | 0.495 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 946,112 | 9.461 | 20 | 20 | fits | 145,989 | 123 | 0.499 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if0` | 1,040,682 | 10.407 | 20 | 24 | fits | 114,774 | 96 | 0.354 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 906,637 | 9.066 | 20 | 50 | fits | 145,989 | 123 | 0.499 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if0` | 582,622 | 5.826 | 20 | 20 | fits | 86,574 | 51 | 0.595 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

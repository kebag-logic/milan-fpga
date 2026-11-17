Original file: <scratch>/budget/final/later-1x1/table.md
Original size: 12727 bytes
Original sha256: 0cd879045a50c782be1941a1066c50e9865c160c9a2d46a43a9f9bd4edaad726

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.acmp.if0` (notice-retried-4) | 4.287 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.adp.if0` (notice-retried-7) | 1.630 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.aecp.if0` (notice-retried-4) | 4.085 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.maap.if0` (notice-retried-4) | 3.892 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-4.held.srp.if0` (notice-retried-4) | 10.417 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-5.mrpdu.periodic.if0` (notice-retried-5) | 0.932 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-2.stream_info.if0` (notice-retried-2) | 8.301 (8.394) | fits | 2 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1568 | 0 | 154,751 (1.548) | fits |
| notice-retried-1 | 1568 | 0 | 154,380 (1.544) | fits |
| notice-retried-2 | 1570 | 0 | 154,445 (1.544) | fits |
| notice-retried-3 | 1567 | 0 | 154,745 (1.547) | fits |
| notice-retried-4 | 1566 | 0 | 153,476 (1.535) | fits |
| notice-retried-5 | 1563 | 0 | 154,581 (1.546) | fits |
| notice-retried-6 | 1567 | 0 | 154,476 (1.545) | fits |
| notice-retried-7 | 1563 | 0 | 154,690 (1.547) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 7.899 | 20 | 16 | 2 | within |
| notice-retried-1 | 8.098 | 20 | 16 | 1 | within |
| notice-retried-2 | 8.301 | 20 | 16 | 2 | within |
| notice-retried-3 | 8.070 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.070 | 20 | 16 | 1 | within |
| notice-retried-5 | 7.986 | 20 | 16 | 1 | within |
| notice-retried-6 | 8.275 | 20 | 16 | 1 | within |
| notice-retried-7 | 8.293 | 20 | 16 | 2 | within |

Latest: 8.301 ms, notice-retried-2.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 307 | 92,498 (0.925) | 75,992 (0.760) |
| notice-retried-1 | 307 | 92,845 (0.928) | 75,994 (0.760) |
| notice-retried-2 | 307 | 92,498 (0.925) | 75,992 (0.760) |
| notice-retried-3 | 307 | 92,984 (0.930) | 75,994 (0.760) |
| notice-retried-4 | 307 | 103,029 (1.030) | 76,225 (0.762) |
| notice-retried-5 | 307 | 91,916 (0.919) | 75,799 (0.758) |
| notice-retried-6 | 307 | 91,916 (0.919) | 75,799 (0.758) |
| notice-retried-7 | 307 | 91,916 (0.919) | 75,799 (0.758) |

Longest pass that carries a step: 103,029 CPU cycles (1.030 ms), notice-retried-4; longest step: 76,225 (0.762 ms), notice-retried-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 789,863 | 7.899 | 20 | 24 | fits | 27,503 | 52 | 0.442 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 129,963 | 1.300 | 20 | 200 | fits | 117,618 | 146 | 0.342 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 415,097 | 4.151 | 20 | 20 | fits | 120,126 | 101 | 0.523 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 394,893 | 3.949 | 20 | 24 | fits | 120,126 | 101 | 0.523 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 375,622 | 3.756 | 20 | 50 | fits | 120,126 | 101 | 0.523 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 1,028,357 | 10.284 | 20 | 20 | fits | 37,356 | 18 | 0.807 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 82,172 | 0.822 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 809,790 | 8.098 | 20 | 24 | fits | 27,577 | 52 | 0.444 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 128,374 | 1.284 | 20 | 200 | fits | 123,616 | 157 | 0.320 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 408,978 | 4.090 | 20 | 20 | fits | 125,632 | 108 | 0.512 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 388,774 | 3.888 | 20 | 24 | fits | 125,632 | 108 | 0.512 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 369,503 | 3.695 | 20 | 50 | fits | 125,632 | 108 | 0.512 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 1,022,332 | 10.223 | 20 | 20 | fits | 37,356 | 18 | 0.807 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 91,706 | 0.917 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 830,084 | 8.301 | 20 | 24 | fits | 27,645 | 52 | 0.447 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 128,645 | 1.286 | 20 | 200 | fits | 122,218 | 154 | 0.327 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 409,842 | 4.098 | 20 | 20 | fits | 125,691 | 108 | 0.512 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 389,638 | 3.896 | 20 | 24 | fits | 125,691 | 108 | 0.512 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 370,367 | 3.704 | 20 | 50 | fits | 125,691 | 108 | 0.512 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 1,023,028 | 10.230 | 20 | 20 | fits | 37,356 | 18 | 0.807 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 76,874 | 0.769 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 807,006 | 8.070 | 20 | 24 | fits | 27,471 | 52 | 0.447 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 161,549 | 1.615 | 20 | 200 | fits | 150,469 | 269 | 0.348 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 415,833 | 4.158 | 20 | 20 | fits | 119,807 | 101 | 0.523 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 395,629 | 3.956 | 20 | 24 | fits | 119,807 | 101 | 0.523 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 376,358 | 3.764 | 20 | 50 | fits | 119,807 | 101 | 0.523 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 1,029,022 | 10.290 | 20 | 20 | fits | 37,356 | 18 | 0.807 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 82,962 | 0.830 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 807,006 | 8.070 | 20 | 24 | fits | 27,471 | 52 | 0.447 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 160,659 | 1.607 | 20 | 200 | fits | 147,990 | 265 | 0.341 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 428,698 | 4.287 | 20 | 20 | fits | 133,554 | 110 | 0.516 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 408,494 | 4.085 | 20 | 24 | fits | 133,554 | 110 | 0.516 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 389,223 | 3.892 | 20 | 50 | fits | 133,554 | 110 | 0.516 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 1,041,746 | 10.417 | 20 | 20 | fits | 37,356 | 18 | 0.807 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 77,453 | 0.775 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 798,595 | 7.986 | 20 | 24 | fits | 27,503 | 52 | 0.442 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 149,133 | 1.491 | 20 | 200 | fits | 148,779 | 271 | 0.312 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 422,605 | 4.226 | 20 | 20 | fits | 129,376 | 121 | 0.517 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 402,401 | 4.024 | 20 | 24 | fits | 129,376 | 121 | 0.517 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 383,130 | 3.831 | 20 | 50 | fits | 129,376 | 121 | 0.517 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 1,018,076 | 10.181 | 20 | 20 | fits | 37,356 | 18 | 0.807 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 93,239 | 0.932 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 827,496 | 8.275 | 20 | 24 | fits | 28,100 | 52 | 0.462 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 130,823 | 1.308 | 20 | 200 | fits | 122,274 | 154 | 0.328 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 414,029 | 4.140 | 20 | 20 | fits | 129,339 | 117 | 0.512 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 393,825 | 3.938 | 20 | 24 | fits | 129,339 | 117 | 0.512 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 374,554 | 3.746 | 20 | 50 | fits | 129,339 | 117 | 0.512 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 1,022,504 | 10.225 | 20 | 20 | fits | 37,356 | 18 | 0.807 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 79,158 | 0.792 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 829,252 | 8.293 | 20 | 24 | fits | 28,100 | 52 | 0.462 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 162,995 | 1.630 | 20 | 200 | fits | 153,245 | 273 | 0.341 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 417,405 | 4.174 | 20 | 20 | fits | 119,988 | 103 | 0.521 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 397,201 | 3.972 | 20 | 24 | fits | 119,988 | 103 | 0.521 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 377,930 | 3.779 | 20 | 50 | fits | 119,988 | 103 | 0.521 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 1,027,793 | 10.278 | 20 | 20 | fits | 37,356 | 18 | 0.807 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 84,356 | 0.844 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

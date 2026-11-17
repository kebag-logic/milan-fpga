Original file: <scratch>/r4/budget/r4-lt8/results/table.md
Original size: 12700 bytes
Original sha256: 2e32ce81a3cadaf5854bf054459547ba1151e76337eb93cb9c35a8f56a5e298d

### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 7 paths and 0 of 56 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-retried-1.held.acmp.if0` (notice-retried-1) | 5.209 | fits | 11 acmp | 8 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `notice-retried-7.held.adp.if0` (notice-retried-7) | 1.761 | fits | 7 adp | 8 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.aecp.if0` (notice-retried-5) | 4.459 | fits | 15 aecp | 8 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-retried-5.held.maap.if0` (notice-retried-5) | 4.267 | fits | 6 maap | 8 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `notice-retried-1.held.srp.if0` (notice-retried-1) | 8.617 | fits | 31 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-retried-5.mrpdu.periodic.if0` (notice-retried-5) | 0.998 | fits | 0 srp | 8 | 0 |
| a retried notice, from its port's answer (THE RETRY) | 0 | `notice-retried-4.stream_info.if0` (notice-retried-4) | 8.164 (8.271) | fits | 1 events | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-retried-0 | 1428 | 0 | 159,289 (1.593) | fits |
| notice-retried-1 | 1428 | 0 | 159,342 (1.593) | fits |
| notice-retried-2 | 1429 | 0 | 159,342 (1.593) | fits |
| notice-retried-3 | 1428 | 0 | 157,033 (1.570) | fits |
| notice-retried-4 | 1427 | 0 | 159,867 (1.599) | fits |
| notice-retried-5 | 1427 | 0 | 159,402 (1.594) | fits |
| notice-retried-6 | 1427 | 0 | 159,402 (1.594) | fits |
| notice-retried-7 | 1427 | 0 | 159,379 (1.594) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-retried-0 | 7.982 | 20 | 16 | 3 | within |
| notice-retried-1 | 8.126 | 20 | 16 | 1 | within |
| notice-retried-2 | 8.159 | 20 | 16 | 1 | within |
| notice-retried-3 | 8.157 | 20 | 16 | 1 | within |
| notice-retried-4 | 8.164 | 20 | 16 | 1 | within |
| notice-retried-5 | 8.120 | 20 | 16 | 2 | within |
| notice-retried-6 | 8.120 | 20 | 16 | 2 | within |
| notice-retried-7 | 7.931 | 20 | 16 | 1 | within |

Latest: 8.164 ms, notice-retried-4.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-retried-0 | 303 | 81,115 (0.811) | 47,746 (0.477) |
| notice-retried-1 | 303 | 81,115 (0.811) | 47,746 (0.477) |
| notice-retried-2 | 303 | 81,115 (0.811) | 47,746 (0.477) |
| notice-retried-3 | 303 | 81,115 (0.811) | 47,746 (0.477) |
| notice-retried-4 | 303 | 81,115 (0.811) | 47,746 (0.477) |
| notice-retried-5 | 303 | 81,115 (0.811) | 47,746 (0.477) |
| notice-retried-6 | 303 | 81,115 (0.811) | 47,746 (0.477) |
| notice-retried-7 | 303 | 81,115 (0.811) | 47,746 (0.477) |

Longest pass that carries a step: 81,115 CPU cycles (0.811 ms), notice-retried-0; longest step: 47,746 (0.477 ms), notice-retried-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-0.stream_info.if0` | 798,196 | 7.982 | 20 | 24 | fits | 24,899 | 52 | 0.437 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-0.held.adp.if0` | 158,025 | 1.580 | 20 | 200 | fits | 146,385 | 146 | 0.341 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-0.held.acmp.if0` | 447,976 | 4.480 | 20 | 20 | fits | 152,338 | 144 | 0.412 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-0.held.aecp.if0` | 427,772 | 4.278 | 20 | 24 | fits | 152,338 | 144 | 0.412 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-0.held.maap.if0` | 408,501 | 4.085 | 20 | 50 | fits | 152,338 | 144 | 0.412 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-0.held.srp.if0` | 837,851 | 8.379 | 20 | 20 | fits | 88,603 | 42 | 0.581 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-0.mrpdu.periodic.if0` | 87,690 | 0.877 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-1.stream_info.if0` | 812,594 | 8.126 | 20 | 24 | fits | 24,822 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-1.held.adp.if0` | 157,695 | 1.577 | 20 | 200 | fits | 150,415 | 150 | 0.327 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-1.held.acmp.if0` | 520,912 | 5.209 | 20 | 20 | fits | 87,914 | 37 | 0.756 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-1.held.aecp.if0` | 364,712 | 3.647 | 20 | 24 | fits | 97,408 | 69 | 0.425 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-1.held.maap.if0` | 393,523 | 3.935 | 20 | 50 | fits | 150,317 | 156 | 0.408 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-1.held.srp.if0` | 861,717 | 8.617 | 20 | 20 | fits | 45,771 | 22 | 0.766 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-1.mrpdu.periodic.if0` | 78,532 | 0.785 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-2.stream_info.if0` | 815,890 | 8.159 | 20 | 24 | fits | 24,822 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-2.held.adp.if0` | 167,024 | 1.670 | 20 | 200 | fits | 154,819 | 219 | 0.363 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-2.held.acmp.if0` | 452,618 | 4.526 | 20 | 20 | fits | 152,387 | 144 | 0.413 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-2.held.aecp.if0` | 432,414 | 4.324 | 20 | 24 | fits | 152,387 | 144 | 0.413 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-2.held.maap.if0` | 413,143 | 4.131 | 20 | 50 | fits | 152,387 | 144 | 0.413 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-2.held.srp.if0` | 842,585 | 8.426 | 20 | 20 | fits | 89,075 | 42 | 0.592 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-2.mrpdu.periodic.if0` | 94,641 | 0.946 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-3.stream_info.if0` | 815,726 | 8.157 | 20 | 24 | fits | 24,822 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-3.held.adp.if0` | 165,569 | 1.656 | 20 | 200 | fits | 157,033 | 225 | 0.371 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-3.held.acmp.if0` | 451,312 | 4.513 | 20 | 20 | fits | 152,422 | 144 | 0.413 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-3.held.aecp.if0` | 431,108 | 4.311 | 20 | 24 | fits | 152,422 | 144 | 0.413 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-3.held.maap.if0` | 411,837 | 4.118 | 20 | 50 | fits | 152,422 | 144 | 0.413 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-3.held.srp.if0` | 840,881 | 8.409 | 20 | 20 | fits | 86,087 | 51 | 0.637 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-3.mrpdu.periodic.if0` | 80,102 | 0.801 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-4.stream_info.if0` | 816,370 | 8.164 | 20 | 24 | fits | 24,822 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-4.held.adp.if0` | 164,871 | 1.649 | 20 | 200 | fits | 152,889 | 218 | 0.367 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-4.held.acmp.if0` | 464,863 | 4.649 | 20 | 20 | fits | 153,094 | 143 | 0.423 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-4.held.aecp.if0` | 444,659 | 4.447 | 20 | 24 | fits | 153,094 | 143 | 0.423 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-4.held.maap.if0` | 425,388 | 4.254 | 20 | 50 | fits | 153,094 | 143 | 0.423 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-4.held.srp.if0` | 837,038 | 8.370 | 20 | 20 | fits | 80,391 | 40 | 0.608 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-4.mrpdu.periodic.if0` | 95,099 | 0.951 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-5.stream_info.if0` | 811,984 | 8.120 | 20 | 24 | fits | 24,823 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-5.held.adp.if0` | 164,146 | 1.641 | 20 | 200 | fits | 155,578 | 221 | 0.355 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-5.held.acmp.if0` | 466,128 | 4.661 | 20 | 20 | fits | 157,475 | 156 | 0.432 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-5.held.aecp.if0` | 445,924 | 4.459 | 20 | 24 | fits | 157,475 | 156 | 0.432 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-5.held.maap.if0` | 426,653 | 4.267 | 20 | 50 | fits | 157,475 | 156 | 0.432 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-5.held.srp.if0` | 837,758 | 8.378 | 20 | 20 | fits | 80,141 | 38 | 0.609 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-5.mrpdu.periodic.if0` | 99,795 | 0.998 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-6.stream_info.if0` | 811,984 | 8.120 | 20 | 24 | fits | 24,823 | 52 | 0.435 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-6.held.adp.if0` | 159,775 | 1.598 | 20 | 200 | fits | 146,380 | 146 | 0.341 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-6.held.acmp.if0` | 462,752 | 4.628 | 20 | 20 | fits | 157,094 | 156 | 0.428 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-6.held.aecp.if0` | 442,548 | 4.425 | 20 | 24 | fits | 157,094 | 156 | 0.428 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-6.held.maap.if0` | 423,277 | 4.233 | 20 | 50 | fits | 157,094 | 156 | 0.428 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-6.held.srp.if0` | 834,382 | 8.344 | 20 | 20 | fits | 80,141 | 38 | 0.609 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-6.mrpdu.periodic.if0` | 97,574 | 0.976 | 20 | 20 | fits | 0 | - | 0.000 |
| a retried notice, from its port's answer (THE RETRY) | `notice-retried-7.stream_info.if0` | 793,069 | 7.931 | 20 | 24 | fits | 25,368 | 52 | 0.453 |
| ADP record, every channel at its refill rate, the longest | `notice-retried-7.held.adp.if0` | 176,128 | 1.761 | 20 | 200 | fits | 153,669 | 221 | 0.376 |
| ACMP record, every channel at its refill rate, the longest | `notice-retried-7.held.acmp.if0` | 462,518 | 4.625 | 20 | 20 | fits | 152,847 | 145 | 0.419 |
| AECP record, every channel at its refill rate, the longest | `notice-retried-7.held.aecp.if0` | 442,314 | 4.423 | 20 | 24 | fits | 152,847 | 145 | 0.419 |
| MAAP record, every channel at its refill rate, the longest | `notice-retried-7.held.maap.if0` | 423,043 | 4.230 | 20 | 50 | fits | 152,847 | 145 | 0.419 |
| SRP record, every channel at its refill rate, the longest | `notice-retried-7.held.srp.if0` | 849,394 | 8.494 | 20 | 20 | fits | 80,143 | 38 | 0.609 |
| an MRPDU its periodic timer owes, the longest | `notice-retried-7.mrpdu.periodic.if0` | 74,442 | 0.744 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

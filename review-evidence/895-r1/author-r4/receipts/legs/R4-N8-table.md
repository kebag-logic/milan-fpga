### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 736 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `notice-burst-5.held.acmp.if0` (notice-burst-5) | 7.824 | fits | 11 acmp | 16 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `notice-burst-7.held.adp.if1` (notice-burst-7) | 7.653 | fits | 7 adp | 16 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `notice-every-0.held.aecp.if1` (notice-every-0) | 5.097 | fits | 15 aecp | 16 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `notice-every-0.held.maap.if0` (notice-every-0) | 6.551 | fits | 6 maap | 16 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `notice-every-1.held.srp.if1` (notice-every-1) | 11.439 | fits | 31 srp | 16 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `notice-every-4.mrpdu.periodic.if0` (notice-every-4) | 1.467 | fits | 0 srp | 8 | 0 |
| an MRPDU its periodic timer owes, the longest | 1 | `notice-every-4.mrpdu.periodic.if1` (notice-every-4) | 1.966 | fits | 0 srp | 8 | 0 |
| a queued notice, from its port's answer | 0 | `notice-burst-1.notices.29.36.0.if0` (notice-burst-1) | 51.275 (51.368) | fits | 1 events | 640 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| notice-every-0 | 1073 | 0 | 168,046 (1.680) | fits |
| notice-every-1 | 1073 | 0 | 165,730 (1.657) | fits |
| notice-every-2 | 1075 | 0 | 165,448 (1.654) | fits |
| notice-every-3 | 1068 | 0 | 165,448 (1.654) | fits |
| notice-every-4 | 1071 | 0 | 167,976 (1.680) | fits |
| notice-every-5 | 1068 | 0 | 165,386 (1.654) | fits |
| notice-every-6 | 1074 | 0 | 165,503 (1.655) | fits |
| notice-every-7 | 1073 | 0 | 165,448 (1.654) | fits |
| notice-burst-0 | 936 | 0 | 168,257 (1.683) | fits |
| notice-burst-1 | 941 | 0 | 167,787 (1.678) | fits |
| notice-burst-2 | 939 | 0 | 167,496 (1.675) | fits |
| notice-burst-3 | 931 | 0 | 163,741 (1.637) | fits |
| notice-burst-4 | 920 | 0 | 167,604 (1.676) | fits |
| notice-burst-5 | 940 | 0 | 195,306 (1.953) | fits |
| notice-burst-6 | 930 | 0 | 167,734 (1.677) | fits |
| notice-burst-7 | 938 | 0 | 166,725 (1.667) | fits |

Retried notices, from the port's answer to the last recipient's commit (notice_window.py; ctrl_loop.h, THE RETRY):

| Group | ms | Bound ms | Recipients | Events held at the answer | Verdict |
|---|---:|---:|---:|---:|---|
| notice-every-0 | 6.271 | 62 | 32 | 1 | within |
| notice-every-0 | 6.571 | 62 | 32 | 1 | within |
| notice-every-0 | 2.559 | 62 | 32 | 1 | within |
| notice-every-0 | 2.865 | 62 | 32 | 1 | within |
| notice-every-0 | 4.266 | 62 | 32 | 1 | within |
| notice-every-0 | 4.573 | 62 | 32 | 1 | within |
| notice-every-0 | 8.267 | 62 | 32 | 1 | within |
| notice-every-0 | 8.567 | 62 | 32 | 1 | within |
| notice-every-0 | 10.255 | 62 | 32 | 1 | within |
| notice-every-0 | 10.554 | 62 | 32 | 1 | within |
| notice-every-0 | 12.224 | 62 | 32 | 1 | within |
| notice-every-0 | 12.524 | 62 | 32 | 1 | within |
| notice-every-0 | 14.241 | 62 | 32 | 1 | within |
| notice-every-0 | 14.541 | 62 | 32 | 1 | within |
| notice-every-0 | 16.201 | 62 | 32 | 1 | within |
| notice-every-0 | 16.503 | 62 | 32 | 1 | within |
| notice-every-0 | 18.472 | 62 | 32 | 1 | within |
| notice-every-0 | 18.773 | 62 | 32 | 1 | within |
| notice-every-0 | 20.414 | 62 | 32 | 1 | within |
| notice-every-0 | 20.715 | 62 | 32 | 1 | within |
| notice-every-0 | 24.716 | 62 | 32 | 1 | within |
| notice-every-0 | 28.459 | 62 | 32 | 1 | within |
| notice-every-0 | 28.738 | 62 | 32 | 1 | within |
| notice-every-0 | 30.387 | 62 | 32 | 1 | within |
| notice-every-0 | 30.667 | 62 | 32 | 1 | within |
| notice-every-0 | 32.304 | 62 | 32 | 1 | within |
| notice-every-0 | 32.581 | 62 | 32 | 1 | within |
| notice-every-0 | 34.230 | 62 | 32 | 1 | within |
| notice-every-0 | 34.513 | 62 | 32 | 1 | within |
| notice-every-0 | 36.442 | 62 | 32 | 1 | within |
| notice-every-0 | 36.722 | 62 | 32 | 1 | within |
| notice-every-0 | 38.352 | 62 | 32 | 1 | within |
| notice-every-0 | 38.634 | 62 | 32 | 1 | within |
| notice-every-0 | 40.253 | 62 | 32 | 1 | within |
| notice-every-0 | 40.531 | 62 | 32 | 1 | within |
| notice-every-0 | 42.702 | 62 | 32 | 1 | within |
| notice-every-0 | 42.968 | 62 | 32 | 1 | within |
| notice-every-0 | 44.296 | 62 | 32 | 1 | within |
| notice-every-0 | 44.593 | 62 | 32 | 1 | within |
| notice-every-0 | 46.478 | 62 | 32 | 1 | within |
| notice-every-1 | 6.197 | 62 | 32 | 1 | within |
| notice-every-1 | 6.497 | 62 | 32 | 1 | within |
| notice-every-1 | 2.177 | 62 | 32 | 1 | within |
| notice-every-1 | 2.483 | 62 | 32 | 1 | within |
| notice-every-1 | 8.193 | 62 | 32 | 1 | within |
| notice-every-1 | 8.494 | 62 | 32 | 1 | within |
| notice-every-1 | 4.199 | 62 | 32 | 1 | within |
| notice-every-1 | 4.508 | 62 | 32 | 1 | within |
| notice-every-1 | 10.184 | 62 | 32 | 1 | within |
| notice-every-1 | 10.483 | 62 | 32 | 1 | within |
| notice-every-1 | 12.154 | 62 | 32 | 1 | within |
| notice-every-1 | 12.453 | 62 | 32 | 1 | within |
| notice-every-1 | 14.171 | 62 | 32 | 1 | within |
| notice-every-1 | 14.470 | 62 | 32 | 1 | within |
| notice-every-1 | 16.130 | 62 | 32 | 1 | within |
| notice-every-1 | 16.432 | 62 | 32 | 1 | within |
| notice-every-1 | 18.096 | 62 | 32 | 1 | within |
| notice-every-1 | 18.397 | 62 | 32 | 1 | within |
| notice-every-1 | 20.041 | 62 | 32 | 1 | within |
| notice-every-1 | 20.342 | 62 | 32 | 1 | within |
| notice-every-1 | 24.341 | 62 | 32 | 1 | within |
| notice-every-1 | 28.084 | 62 | 32 | 1 | within |
| notice-every-1 | 28.364 | 62 | 32 | 1 | within |
| notice-every-1 | 30.012 | 62 | 32 | 1 | within |
| notice-every-1 | 30.292 | 62 | 32 | 1 | within |
| notice-every-1 | 32.230 | 62 | 32 | 1 | within |
| notice-every-1 | 32.507 | 62 | 32 | 1 | within |
| notice-every-1 | 34.152 | 62 | 32 | 1 | within |
| notice-every-1 | 34.436 | 62 | 32 | 1 | within |
| notice-every-1 | 36.068 | 62 | 32 | 1 | within |
| notice-every-1 | 36.349 | 62 | 32 | 1 | within |
| notice-every-1 | 38.278 | 62 | 32 | 1 | within |
| notice-every-1 | 38.559 | 62 | 32 | 1 | within |
| notice-every-1 | 40.175 | 62 | 32 | 1 | within |
| notice-every-1 | 40.453 | 62 | 32 | 1 | within |
| notice-every-1 | 42.628 | 62 | 32 | 1 | within |
| notice-every-1 | 42.894 | 62 | 32 | 1 | within |
| notice-every-1 | 44.221 | 62 | 32 | 1 | within |
| notice-every-1 | 44.519 | 62 | 32 | 1 | within |
| notice-every-1 | 46.113 | 62 | 32 | 1 | within |
| notice-every-2 | 6.209 | 62 | 32 | 1 | within |
| notice-every-2 | 6.509 | 62 | 32 | 1 | within |
| notice-every-2 | 2.176 | 62 | 32 | 1 | within |
| notice-every-2 | 2.482 | 62 | 32 | 1 | within |
| notice-every-2 | 4.202 | 62 | 32 | 1 | within |
| notice-every-2 | 4.509 | 62 | 32 | 1 | within |
| notice-every-2 | 8.203 | 62 | 32 | 1 | within |
| notice-every-2 | 8.504 | 62 | 32 | 1 | within |
| notice-every-2 | 10.192 | 62 | 32 | 1 | within |
| notice-every-2 | 10.491 | 62 | 32 | 1 | within |
| notice-every-2 | 12.162 | 62 | 32 | 1 | within |
| notice-every-2 | 12.461 | 62 | 32 | 1 | within |
| notice-every-2 | 14.179 | 62 | 32 | 1 | within |
| notice-every-2 | 14.479 | 62 | 32 | 1 | within |
| notice-every-2 | 16.445 | 62 | 32 | 1 | within |
| notice-every-2 | 16.747 | 62 | 32 | 1 | within |
| notice-every-2 | 18.407 | 62 | 32 | 1 | within |
| notice-every-2 | 18.708 | 62 | 32 | 1 | within |
| notice-every-2 | 20.354 | 62 | 32 | 1 | within |
| notice-every-2 | 20.655 | 62 | 32 | 1 | within |
| notice-every-2 | 24.655 | 62 | 32 | 1 | within |
| notice-every-2 | 28.398 | 62 | 32 | 1 | within |
| notice-every-2 | 28.678 | 62 | 32 | 1 | within |
| notice-every-2 | 30.324 | 62 | 32 | 1 | within |
| notice-every-2 | 30.604 | 62 | 32 | 1 | within |
| notice-every-2 | 32.243 | 62 | 32 | 1 | within |
| notice-every-2 | 32.521 | 62 | 32 | 1 | within |
| notice-every-2 | 34.167 | 62 | 32 | 1 | within |
| notice-every-2 | 34.450 | 62 | 32 | 1 | within |
| notice-every-2 | 36.379 | 62 | 32 | 1 | within |
| notice-every-2 | 36.660 | 62 | 32 | 1 | within |
| notice-every-2 | 38.292 | 62 | 32 | 1 | within |
| notice-every-2 | 38.573 | 62 | 32 | 1 | within |
| notice-every-2 | 40.190 | 62 | 32 | 1 | within |
| notice-every-2 | 40.469 | 62 | 32 | 1 | within |
| notice-every-2 | 42.643 | 62 | 32 | 1 | within |
| notice-every-2 | 42.908 | 62 | 32 | 1 | within |
| notice-every-2 | 44.236 | 62 | 32 | 1 | within |
| notice-every-2 | 44.534 | 62 | 32 | 1 | within |
| notice-every-2 | 46.419 | 62 | 32 | 1 | within |
| notice-every-3 | 6.268 | 62 | 32 | 1 | within |
| notice-every-3 | 6.568 | 62 | 32 | 1 | within |
| notice-every-3 | 2.488 | 62 | 32 | 1 | within |
| notice-every-3 | 2.794 | 62 | 32 | 1 | within |
| notice-every-3 | 4.584 | 62 | 32 | 1 | within |
| notice-every-3 | 4.891 | 62 | 32 | 1 | within |
| notice-every-3 | 8.262 | 62 | 32 | 1 | within |
| notice-every-3 | 8.563 | 62 | 32 | 1 | within |
| notice-every-3 | 10.251 | 62 | 32 | 1 | within |
| notice-every-3 | 10.550 | 62 | 32 | 1 | within |
| notice-every-3 | 12.220 | 62 | 32 | 1 | within |
| notice-every-3 | 12.520 | 62 | 32 | 1 | within |
| notice-every-3 | 14.237 | 62 | 32 | 1 | within |
| notice-every-3 | 14.537 | 62 | 32 | 1 | within |
| notice-every-3 | 16.503 | 62 | 32 | 1 | within |
| notice-every-3 | 16.805 | 62 | 32 | 1 | within |
| notice-every-3 | 18.465 | 62 | 32 | 1 | within |
| notice-every-3 | 18.766 | 62 | 32 | 1 | within |
| notice-every-3 | 20.413 | 62 | 32 | 1 | within |
| notice-every-3 | 20.714 | 62 | 32 | 1 | within |
| notice-every-3 | 24.714 | 62 | 32 | 1 | within |
| notice-every-3 | 28.456 | 62 | 32 | 1 | within |
| notice-every-3 | 28.736 | 62 | 32 | 1 | within |
| notice-every-3 | 30.382 | 62 | 32 | 1 | within |
| notice-every-3 | 30.662 | 62 | 32 | 1 | within |
| notice-every-3 | 32.302 | 62 | 32 | 1 | within |
| notice-every-3 | 32.579 | 62 | 32 | 1 | within |
| notice-every-3 | 34.225 | 62 | 32 | 1 | within |
| notice-every-3 | 34.509 | 62 | 32 | 1 | within |
| notice-every-3 | 36.438 | 62 | 32 | 1 | within |
| notice-every-3 | 36.718 | 62 | 32 | 1 | within |
| notice-every-3 | 38.350 | 62 | 32 | 1 | within |
| notice-every-3 | 38.632 | 62 | 32 | 1 | within |
| notice-every-3 | 40.249 | 62 | 32 | 1 | within |
| notice-every-3 | 40.527 | 62 | 32 | 1 | within |
| notice-every-3 | 42.702 | 62 | 32 | 1 | within |
| notice-every-3 | 42.968 | 62 | 32 | 1 | within |
| notice-every-3 | 44.296 | 62 | 32 | 1 | within |
| notice-every-3 | 44.593 | 62 | 32 | 1 | within |
| notice-every-3 | 46.478 | 62 | 32 | 1 | within |
| notice-every-4 | 4.196 | 62 | 32 | 1 | within |
| notice-every-4 | 4.496 | 62 | 32 | 1 | within |
| notice-every-4 | 6.199 | 62 | 32 | 1 | within |
| notice-every-4 | 6.501 | 62 | 32 | 1 | within |
| notice-every-4 | 2.174 | 62 | 32 | 1 | within |
| notice-every-4 | 2.484 | 62 | 32 | 1 | within |
| notice-every-4 | 8.196 | 62 | 32 | 1 | within |
| notice-every-4 | 8.496 | 62 | 32 | 1 | within |
| notice-every-4 | 10.182 | 62 | 32 | 1 | within |
| notice-every-4 | 10.481 | 62 | 32 | 1 | within |
| notice-every-4 | 12.153 | 62 | 32 | 1 | within |
| notice-every-4 | 12.453 | 62 | 32 | 1 | within |
| notice-every-4 | 14.168 | 62 | 32 | 1 | within |
| notice-every-4 | 14.467 | 62 | 32 | 1 | within |
| notice-every-4 | 16.129 | 62 | 32 | 1 | within |
| notice-every-4 | 16.431 | 62 | 32 | 1 | within |
| notice-every-4 | 18.093 | 62 | 32 | 1 | within |
| notice-every-4 | 18.394 | 62 | 32 | 1 | within |
| notice-every-4 | 20.040 | 62 | 32 | 1 | within |
| notice-every-4 | 20.341 | 62 | 32 | 1 | within |
| notice-every-4 | 24.339 | 62 | 32 | 1 | within |
| notice-every-4 | 28.082 | 62 | 32 | 1 | within |
| notice-every-4 | 28.362 | 62 | 32 | 1 | within |
| notice-every-4 | 30.008 | 62 | 32 | 1 | within |
| notice-every-4 | 30.288 | 62 | 32 | 1 | within |
| notice-every-4 | 32.226 | 62 | 32 | 1 | within |
| notice-every-4 | 32.503 | 62 | 32 | 1 | within |
| notice-every-4 | 34.150 | 62 | 32 | 1 | within |
| notice-every-4 | 34.433 | 62 | 32 | 1 | within |
| notice-every-4 | 36.063 | 62 | 32 | 1 | within |
| notice-every-4 | 36.344 | 62 | 32 | 1 | within |
| notice-every-4 | 37.977 | 62 | 32 | 1 | within |
| notice-every-4 | 38.259 | 62 | 32 | 1 | within |
| notice-every-4 | 40.171 | 62 | 32 | 1 | within |
| notice-every-4 | 40.449 | 62 | 32 | 1 | within |
| notice-every-4 | 42.619 | 62 | 32 | 1 | within |
| notice-every-4 | 42.885 | 62 | 32 | 1 | within |
| notice-every-4 | 44.213 | 62 | 32 | 1 | within |
| notice-every-4 | 44.511 | 62 | 32 | 1 | within |
| notice-every-4 | 46.107 | 62 | 32 | 1 | within |
| notice-every-5 | 6.267 | 62 | 32 | 1 | within |
| notice-every-5 | 6.567 | 62 | 32 | 1 | within |
| notice-every-5 | 2.487 | 62 | 32 | 1 | within |
| notice-every-5 | 2.793 | 62 | 32 | 1 | within |
| notice-every-5 | 4.584 | 62 | 32 | 1 | within |
| notice-every-5 | 4.891 | 62 | 32 | 1 | within |
| notice-every-5 | 8.262 | 62 | 32 | 1 | within |
| notice-every-5 | 8.562 | 62 | 32 | 1 | within |
| notice-every-5 | 10.251 | 62 | 32 | 1 | within |
| notice-every-5 | 10.550 | 62 | 32 | 1 | within |
| notice-every-5 | 12.220 | 62 | 32 | 1 | within |
| notice-every-5 | 12.519 | 62 | 32 | 1 | within |
| notice-every-5 | 14.237 | 62 | 32 | 1 | within |
| notice-every-5 | 14.537 | 62 | 32 | 1 | within |
| notice-every-5 | 16.503 | 62 | 32 | 1 | within |
| notice-every-5 | 16.805 | 62 | 32 | 1 | within |
| notice-every-5 | 18.465 | 62 | 32 | 1 | within |
| notice-every-5 | 18.766 | 62 | 32 | 1 | within |
| notice-every-5 | 20.413 | 62 | 32 | 1 | within |
| notice-every-5 | 20.713 | 62 | 32 | 1 | within |
| notice-every-5 | 24.713 | 62 | 32 | 1 | within |
| notice-every-5 | 28.455 | 62 | 32 | 1 | within |
| notice-every-5 | 28.735 | 62 | 32 | 1 | within |
| notice-every-5 | 30.381 | 62 | 32 | 1 | within |
| notice-every-5 | 30.661 | 62 | 32 | 1 | within |
| notice-every-5 | 32.300 | 62 | 32 | 1 | within |
| notice-every-5 | 32.578 | 62 | 32 | 1 | within |
| notice-every-5 | 34.224 | 62 | 32 | 1 | within |
| notice-every-5 | 34.507 | 62 | 32 | 1 | within |
| notice-every-5 | 36.436 | 62 | 32 | 1 | within |
| notice-every-5 | 36.717 | 62 | 32 | 1 | within |
| notice-every-5 | 38.349 | 62 | 32 | 1 | within |
| notice-every-5 | 38.631 | 62 | 32 | 1 | within |
| notice-every-5 | 40.247 | 62 | 32 | 1 | within |
| notice-every-5 | 40.526 | 62 | 32 | 1 | within |
| notice-every-5 | 42.699 | 62 | 32 | 1 | within |
| notice-every-5 | 42.965 | 62 | 32 | 1 | within |
| notice-every-5 | 44.292 | 62 | 32 | 1 | within |
| notice-every-5 | 44.590 | 62 | 32 | 1 | within |
| notice-every-5 | 46.475 | 62 | 32 | 1 | within |
| notice-every-6 | 2.169 | 62 | 32 | 1 | within |
| notice-every-6 | 2.471 | 62 | 32 | 1 | within |
| notice-every-6 | 6.195 | 62 | 32 | 1 | within |
| notice-every-6 | 6.498 | 62 | 32 | 1 | within |
| notice-every-6 | 4.189 | 62 | 32 | 1 | within |
| notice-every-6 | 4.496 | 62 | 32 | 1 | within |
| notice-every-6 | 8.192 | 62 | 32 | 1 | within |
| notice-every-6 | 8.493 | 62 | 32 | 1 | within |
| notice-every-6 | 10.179 | 62 | 32 | 1 | within |
| notice-every-6 | 10.478 | 62 | 32 | 1 | within |
| notice-every-6 | 12.150 | 62 | 32 | 1 | within |
| notice-every-6 | 12.450 | 62 | 32 | 1 | within |
| notice-every-6 | 14.165 | 62 | 32 | 1 | within |
| notice-every-6 | 14.465 | 62 | 32 | 1 | within |
| notice-every-6 | 16.127 | 62 | 32 | 1 | within |
| notice-every-6 | 16.429 | 62 | 32 | 1 | within |
| notice-every-6 | 18.090 | 62 | 32 | 1 | within |
| notice-every-6 | 18.391 | 62 | 32 | 1 | within |
| notice-every-6 | 20.038 | 62 | 32 | 1 | within |
| notice-every-6 | 20.338 | 62 | 32 | 1 | within |
| notice-every-6 | 24.337 | 62 | 32 | 1 | within |
| notice-every-6 | 28.079 | 62 | 32 | 1 | within |
| notice-every-6 | 28.359 | 62 | 32 | 1 | within |
| notice-every-6 | 30.005 | 62 | 32 | 1 | within |
| notice-every-6 | 30.285 | 62 | 32 | 1 | within |
| notice-every-6 | 32.223 | 62 | 32 | 1 | within |
| notice-every-6 | 32.501 | 62 | 32 | 1 | within |
| notice-every-6 | 34.147 | 62 | 32 | 1 | within |
| notice-every-6 | 34.431 | 62 | 32 | 1 | within |
| notice-every-6 | 36.061 | 62 | 32 | 1 | within |
| notice-every-6 | 36.342 | 62 | 32 | 1 | within |
| notice-every-6 | 37.975 | 62 | 32 | 1 | within |
| notice-every-6 | 38.256 | 62 | 32 | 1 | within |
| notice-every-6 | 40.169 | 62 | 32 | 1 | within |
| notice-every-6 | 40.447 | 62 | 32 | 1 | within |
| notice-every-6 | 42.619 | 62 | 32 | 1 | within |
| notice-every-6 | 42.884 | 62 | 32 | 1 | within |
| notice-every-6 | 43.922 | 62 | 32 | 1 | within |
| notice-every-6 | 44.220 | 62 | 32 | 1 | within |
| notice-every-6 | 46.104 | 62 | 32 | 1 | within |
| notice-every-7 | 6.198 | 62 | 32 | 1 | within |
| notice-every-7 | 6.498 | 62 | 32 | 1 | within |
| notice-every-7 | 2.175 | 62 | 32 | 1 | within |
| notice-every-7 | 2.482 | 62 | 32 | 1 | within |
| notice-every-7 | 8.197 | 62 | 32 | 1 | within |
| notice-every-7 | 8.497 | 62 | 32 | 1 | within |
| notice-every-7 | 4.202 | 62 | 32 | 1 | within |
| notice-every-7 | 4.511 | 62 | 32 | 1 | within |
| notice-every-7 | 10.185 | 62 | 32 | 1 | within |
| notice-every-7 | 10.484 | 62 | 32 | 1 | within |
| notice-every-7 | 12.157 | 62 | 32 | 1 | within |
| notice-every-7 | 12.456 | 62 | 32 | 1 | within |
| notice-every-7 | 14.171 | 62 | 32 | 1 | within |
| notice-every-7 | 14.471 | 62 | 32 | 1 | within |
| notice-every-7 | 16.133 | 62 | 32 | 1 | within |
| notice-every-7 | 16.435 | 62 | 32 | 1 | within |
| notice-every-7 | 18.096 | 62 | 32 | 1 | within |
| notice-every-7 | 18.397 | 62 | 32 | 1 | within |
| notice-every-7 | 20.044 | 62 | 32 | 1 | within |
| notice-every-7 | 20.345 | 62 | 32 | 1 | within |
| notice-every-7 | 24.343 | 62 | 32 | 1 | within |
| notice-every-7 | 28.086 | 62 | 32 | 1 | within |
| notice-every-7 | 28.366 | 62 | 32 | 1 | within |
| notice-every-7 | 30.012 | 62 | 32 | 1 | within |
| notice-every-7 | 30.292 | 62 | 32 | 1 | within |
| notice-every-7 | 32.230 | 62 | 32 | 1 | within |
| notice-every-7 | 32.507 | 62 | 32 | 1 | within |
| notice-every-7 | 34.155 | 62 | 32 | 1 | within |
| notice-every-7 | 34.438 | 62 | 32 | 1 | within |
| notice-every-7 | 36.068 | 62 | 32 | 1 | within |
| notice-every-7 | 36.349 | 62 | 32 | 1 | within |
| notice-every-7 | 38.278 | 62 | 32 | 1 | within |
| notice-every-7 | 38.559 | 62 | 32 | 1 | within |
| notice-every-7 | 40.177 | 62 | 32 | 1 | within |
| notice-every-7 | 40.455 | 62 | 32 | 1 | within |
| notice-every-7 | 42.626 | 62 | 32 | 1 | within |
| notice-every-7 | 42.892 | 62 | 32 | 1 | within |
| notice-every-7 | 44.220 | 62 | 32 | 1 | within |
| notice-every-7 | 44.517 | 62 | 32 | 1 | within |
| notice-every-7 | 46.113 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.719 | 62 | 32 | 1 | within |
| notice-burst-0 | 4.013 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.189 | 62 | 32 | 1 | within |
| notice-burst-0 | 5.491 | 62 | 32 | 1 | within |
| notice-burst-0 | 17.390 | 62 | 32 | 1 | within |
| notice-burst-0 | 21.226 | 62 | 32 | 1 | within |
| notice-burst-0 | 21.517 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.199 | 62 | 32 | 1 | within |
| notice-burst-0 | 6.092 | 62 | 32 | 1 | within |
| notice-burst-0 | 6.391 | 62 | 32 | 1 | within |
| notice-burst-0 | 23.490 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.230 | 62 | 32 | 1 | within |
| notice-burst-0 | 25.520 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.194 | 62 | 32 | 1 | within |
| notice-burst-0 | 2.982 | 62 | 32 | 1 | within |
| notice-burst-0 | 3.306 | 62 | 32 | 1 | within |
| notice-burst-0 | 27.486 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.461 | 62 | 32 | 1 | within |
| notice-burst-0 | 29.740 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.402 | 62 | 32 | 1 | within |
| notice-burst-0 | 31.682 | 62 | 32 | 1 | within |
| notice-burst-0 | 33.335 | 62 | 32 | 1 | within |
| notice-burst-0 | 33.615 | 62 | 32 | 1 | within |
| notice-burst-0 | 35.279 | 62 | 32 | 1 | within |
| notice-burst-0 | 35.559 | 62 | 32 | 1 | within |
| notice-burst-0 | 37.200 | 62 | 32 | 1 | within |
| notice-burst-0 | 37.476 | 62 | 32 | 1 | within |
| notice-burst-0 | 39.409 | 62 | 32 | 1 | within |
| notice-burst-0 | 39.690 | 62 | 32 | 1 | within |
| notice-burst-0 | 41.323 | 62 | 32 | 1 | within |
| notice-burst-0 | 41.603 | 62 | 32 | 1 | within |
| notice-burst-0 | 43.235 | 62 | 32 | 1 | within |
| notice-burst-0 | 43.516 | 62 | 32 | 1 | within |
| notice-burst-0 | 45.191 | 62 | 32 | 1 | within |
| notice-burst-0 | 45.470 | 62 | 32 | 1 | within |
| notice-burst-0 | 47.378 | 62 | 32 | 1 | within |
| notice-burst-0 | 47.646 | 62 | 32 | 1 | within |
| notice-burst-0 | 49.202 | 62 | 32 | 1 | within |
| notice-burst-0 | 49.499 | 62 | 32 | 1 | within |
| notice-burst-0 | 51.274 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.205 | 62 | 32 | 1 | within |
| notice-burst-1 | 3.499 | 62 | 32 | 1 | within |
| notice-burst-1 | 4.999 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.301 | 62 | 32 | 1 | within |
| notice-burst-1 | 17.267 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.415 | 62 | 32 | 1 | within |
| notice-burst-1 | 21.706 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.386 | 62 | 32 | 1 | within |
| notice-burst-1 | 5.911 | 62 | 32 | 1 | within |
| notice-burst-1 | 6.210 | 62 | 32 | 1 | within |
| notice-burst-1 | 23.677 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.419 | 62 | 32 | 1 | within |
| notice-burst-1 | 25.709 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.381 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.474 | 62 | 32 | 1 | within |
| notice-burst-1 | 2.798 | 62 | 32 | 1 | within |
| notice-burst-1 | 27.674 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.345 | 62 | 32 | 1 | within |
| notice-burst-1 | 29.624 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.286 | 62 | 32 | 1 | within |
| notice-burst-1 | 31.567 | 62 | 32 | 1 | within |
| notice-burst-1 | 33.220 | 62 | 32 | 1 | within |
| notice-burst-1 | 33.500 | 62 | 32 | 1 | within |
| notice-burst-1 | 35.465 | 62 | 32 | 1 | within |
| notice-burst-1 | 35.745 | 62 | 32 | 1 | within |
| notice-burst-1 | 37.384 | 62 | 32 | 1 | within |
| notice-burst-1 | 37.661 | 62 | 32 | 1 | within |
| notice-burst-1 | 39.297 | 62 | 32 | 1 | within |
| notice-burst-1 | 39.577 | 62 | 32 | 1 | within |
| notice-burst-1 | 41.212 | 62 | 32 | 1 | within |
| notice-burst-1 | 41.491 | 62 | 32 | 1 | within |
| notice-burst-1 | 43.419 | 62 | 32 | 1 | within |
| notice-burst-1 | 43.700 | 62 | 32 | 1 | within |
| notice-burst-1 | 45.375 | 62 | 32 | 1 | within |
| notice-burst-1 | 45.654 | 62 | 32 | 1 | within |
| notice-burst-1 | 47.268 | 62 | 32 | 1 | within |
| notice-burst-1 | 47.536 | 62 | 32 | 1 | within |
| notice-burst-1 | 49.382 | 62 | 32 | 1 | within |
| notice-burst-1 | 49.679 | 62 | 32 | 1 | within |
| notice-burst-1 | 51.275 | 62 | 32 | 1 | within |
| notice-burst-2 | 5.115 | 62 | 32 | 0 | within |
| notice-burst-2 | 5.409 | 62 | 32 | 0 | within |
| notice-burst-2 | 16.459 | 62 | 32 | 0 | within |
| notice-burst-2 | 20.612 | 62 | 32 | 0 | within |
| notice-burst-2 | 20.905 | 62 | 32 | 0 | within |
| notice-burst-2 | 22.585 | 62 | 32 | 0 | within |
| notice-burst-2 | 22.874 | 62 | 32 | 0 | within |
| notice-burst-2 | 24.572 | 62 | 32 | 0 | within |
| notice-burst-2 | 24.864 | 62 | 32 | 0 | within |
| notice-burst-2 | 26.537 | 62 | 32 | 0 | within |
| notice-burst-2 | 2.168 | 62 | 32 | 0 | within |
| notice-burst-2 | 2.487 | 62 | 32 | 0 | within |
| notice-burst-2 | 2.908 | 62 | 32 | 0 | within |
| notice-burst-2 | 3.220 | 62 | 32 | 0 | within |
| notice-burst-2 | 26.828 | 62 | 32 | 0 | within |
| notice-burst-2 | 28.503 | 62 | 32 | 0 | within |
| notice-burst-2 | 4.401 | 62 | 32 | 0 | within |
| notice-burst-2 | 4.723 | 62 | 32 | 0 | within |
| notice-burst-2 | 28.785 | 62 | 32 | 0 | within |
| notice-burst-2 | 30.450 | 62 | 32 | 0 | within |
| notice-burst-2 | 30.731 | 62 | 32 | 0 | within |
| notice-burst-2 | 32.740 | 62 | 32 | 0 | within |
| notice-burst-2 | 33.021 | 62 | 32 | 0 | within |
| notice-burst-2 | 34.670 | 62 | 32 | 0 | within |
| notice-burst-2 | 34.949 | 62 | 32 | 0 | within |
| notice-burst-2 | 36.587 | 62 | 32 | 0 | within |
| notice-burst-2 | 36.864 | 62 | 32 | 0 | within |
| notice-burst-2 | 38.502 | 62 | 32 | 0 | within |
| notice-burst-2 | 38.782 | 62 | 32 | 0 | within |
| notice-burst-2 | 40.414 | 62 | 32 | 0 | within |
| notice-burst-2 | 40.694 | 62 | 32 | 0 | within |
| notice-burst-2 | 42.624 | 62 | 32 | 0 | within |
| notice-burst-2 | 42.905 | 62 | 32 | 0 | within |
| notice-burst-2 | 44.582 | 62 | 32 | 0 | within |
| notice-burst-2 | 44.861 | 62 | 32 | 0 | within |
| notice-burst-2 | 46.473 | 62 | 32 | 0 | within |
| notice-burst-2 | 46.741 | 62 | 32 | 0 | within |
| notice-burst-2 | 48.588 | 62 | 32 | 0 | within |
| notice-burst-2 | 48.886 | 62 | 32 | 0 | within |
| notice-burst-2 | 50.481 | 62 | 32 | 0 | within |
| notice-burst-3 | 5.062 | 62 | 32 | 0 | within |
| notice-burst-3 | 5.356 | 62 | 32 | 0 | within |
| notice-burst-3 | 16.407 | 62 | 32 | 0 | within |
| notice-burst-3 | 19.632 | 62 | 32 | 0 | within |
| notice-burst-3 | 19.925 | 62 | 32 | 0 | within |
| notice-burst-3 | 21.605 | 62 | 32 | 0 | within |
| notice-burst-3 | 21.894 | 62 | 32 | 0 | within |
| notice-burst-3 | 23.585 | 62 | 32 | 0 | within |
| notice-burst-3 | 2.527 | 62 | 32 | 0 | within |
| notice-burst-3 | 2.832 | 62 | 32 | 0 | within |
| notice-burst-3 | 23.879 | 62 | 32 | 0 | within |
| notice-burst-3 | 25.552 | 62 | 32 | 0 | within |
| notice-burst-3 | 25.841 | 62 | 32 | 0 | within |
| notice-burst-3 | 27.815 | 62 | 32 | 0 | within |
| notice-burst-3 | 1.785 | 62 | 32 | 0 | within |
| notice-burst-3 | 2.109 | 62 | 32 | 0 | within |
| notice-burst-3 | 4.348 | 62 | 32 | 0 | within |
| notice-burst-3 | 4.672 | 62 | 32 | 0 | within |
| notice-burst-3 | 28.096 | 62 | 32 | 0 | within |
| notice-burst-3 | 29.757 | 62 | 32 | 0 | within |
| notice-burst-3 | 30.037 | 62 | 32 | 0 | within |
| notice-burst-3 | 31.692 | 62 | 32 | 0 | within |
| notice-burst-3 | 31.972 | 62 | 32 | 0 | within |
| notice-burst-3 | 33.671 | 62 | 32 | 0 | within |
| notice-burst-3 | 33.950 | 62 | 32 | 0 | within |
| notice-burst-3 | 35.593 | 62 | 32 | 0 | within |
| notice-burst-3 | 35.870 | 62 | 32 | 0 | within |
| notice-burst-3 | 37.803 | 62 | 32 | 0 | within |
| notice-burst-3 | 38.083 | 62 | 32 | 0 | within |
| notice-burst-3 | 39.716 | 62 | 32 | 0 | within |
| notice-burst-3 | 39.996 | 62 | 32 | 0 | within |
| notice-burst-3 | 41.628 | 62 | 32 | 0 | within |
| notice-burst-3 | 41.909 | 62 | 32 | 0 | within |
| notice-burst-3 | 43.582 | 62 | 32 | 0 | within |
| notice-burst-3 | 43.861 | 62 | 32 | 0 | within |
| notice-burst-3 | 45.768 | 62 | 32 | 0 | within |
| notice-burst-3 | 46.036 | 62 | 32 | 0 | within |
| notice-burst-3 | 47.592 | 62 | 32 | 0 | within |
| notice-burst-3 | 47.890 | 62 | 32 | 0 | within |
| notice-burst-3 | 49.774 | 62 | 32 | 0 | within |
| notice-burst-4 | 16.560 | 62 | 32 | 0 | within |
| notice-burst-4 | 20.713 | 62 | 32 | 0 | within |
| notice-burst-4 | 21.005 | 62 | 32 | 0 | within |
| notice-burst-4 | 22.686 | 62 | 32 | 0 | within |
| notice-burst-4 | 22.978 | 62 | 32 | 0 | within |
| notice-burst-4 | 24.675 | 62 | 32 | 0 | within |
| notice-burst-4 | 5.187 | 62 | 32 | 0 | within |
| notice-burst-4 | 5.492 | 62 | 32 | 0 | within |
| notice-burst-4 | 24.972 | 62 | 32 | 0 | within |
| notice-burst-4 | 26.647 | 62 | 32 | 0 | within |
| notice-burst-4 | 1.785 | 62 | 32 | 0 | within |
| notice-burst-4 | 2.104 | 62 | 32 | 0 | within |
| notice-burst-4 | 26.939 | 62 | 32 | 0 | within |
| notice-burst-4 | 28.611 | 62 | 32 | 0 | within |
| notice-burst-4 | 3.028 | 62 | 32 | 0 | within |
| notice-burst-4 | 3.349 | 62 | 32 | 0 | within |
| notice-burst-4 | 4.465 | 62 | 32 | 0 | within |
| notice-burst-4 | 4.789 | 62 | 32 | 0 | within |
| notice-burst-4 | 28.892 | 62 | 32 | 0 | within |
| notice-burst-4 | 30.556 | 62 | 32 | 0 | within |
| notice-burst-4 | 30.836 | 62 | 32 | 0 | within |
| notice-burst-4 | 32.790 | 62 | 32 | 0 | within |
| notice-burst-4 | 33.069 | 62 | 32 | 0 | within |
| notice-burst-4 | 34.773 | 62 | 32 | 0 | within |
| notice-burst-4 | 35.052 | 62 | 32 | 0 | within |
| notice-burst-4 | 36.692 | 62 | 32 | 0 | within |
| notice-burst-4 | 36.969 | 62 | 32 | 0 | within |
| notice-burst-4 | 38.605 | 62 | 32 | 0 | within |
| notice-burst-4 | 38.885 | 62 | 32 | 0 | within |
| notice-burst-4 | 40.818 | 62 | 32 | 0 | within |
| notice-burst-4 | 41.098 | 62 | 32 | 0 | within |
| notice-burst-4 | 42.727 | 62 | 32 | 0 | within |
| notice-burst-4 | 43.008 | 62 | 32 | 0 | within |
| notice-burst-4 | 44.685 | 62 | 32 | 0 | within |
| notice-burst-4 | 44.964 | 62 | 32 | 0 | within |
| notice-burst-4 | 46.578 | 62 | 32 | 0 | within |
| notice-burst-4 | 46.846 | 62 | 32 | 0 | within |
| notice-burst-4 | 48.691 | 62 | 32 | 0 | within |
| notice-burst-4 | 48.989 | 62 | 32 | 0 | within |
| notice-burst-4 | 50.585 | 62 | 32 | 0 | within |
| notice-burst-5 | 17.798 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.325 | 62 | 32 | 1 | within |
| notice-burst-5 | 21.617 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.294 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.170 | 62 | 32 | 1 | within |
| notice-burst-5 | 2.478 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.875 | 62 | 32 | 1 | within |
| notice-burst-5 | 5.182 | 62 | 32 | 1 | within |
| notice-burst-5 | 3.956 | 62 | 32 | 1 | within |
| notice-burst-5 | 4.264 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.284 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.591 | 62 | 32 | 1 | within |
| notice-burst-5 | 6.968 | 62 | 32 | 1 | within |
| notice-burst-5 | 7.271 | 62 | 32 | 1 | within |
| notice-burst-5 | 23.586 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.327 | 62 | 32 | 1 | within |
| notice-burst-5 | 25.621 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.295 | 62 | 32 | 1 | within |
| notice-burst-5 | 27.574 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.238 | 62 | 32 | 1 | within |
| notice-burst-5 | 29.518 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.172 | 62 | 32 | 1 | within |
| notice-burst-5 | 31.452 | 62 | 32 | 1 | within |
| notice-burst-5 | 33.399 | 62 | 32 | 1 | within |
| notice-burst-5 | 33.677 | 62 | 32 | 1 | within |
| notice-burst-5 | 35.333 | 62 | 32 | 1 | within |
| notice-burst-5 | 35.612 | 62 | 32 | 1 | within |
| notice-burst-5 | 37.246 | 62 | 32 | 1 | within |
| notice-burst-5 | 37.526 | 62 | 32 | 1 | within |
| notice-burst-5 | 39.161 | 62 | 32 | 1 | within |
| notice-burst-5 | 39.440 | 62 | 32 | 1 | within |
| notice-burst-5 | 41.370 | 62 | 32 | 1 | within |
| notice-burst-5 | 41.651 | 62 | 32 | 1 | within |
| notice-burst-5 | 43.268 | 62 | 32 | 1 | within |
| notice-burst-5 | 43.545 | 62 | 32 | 1 | within |
| notice-burst-5 | 45.219 | 62 | 32 | 1 | within |
| notice-burst-5 | 45.487 | 62 | 32 | 1 | within |
| notice-burst-5 | 47.335 | 62 | 32 | 1 | within |
| notice-burst-5 | 47.633 | 62 | 32 | 1 | within |
| notice-burst-5 | 49.225 | 62 | 32 | 1 | within |
| notice-burst-6 | 16.686 | 62 | 32 | 0 | within |
| notice-burst-6 | 20.839 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.605 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.904 | 62 | 32 | 0 | within |
| notice-burst-6 | 4.401 | 62 | 32 | 0 | within |
| notice-burst-6 | 4.707 | 62 | 32 | 0 | within |
| notice-burst-6 | 21.130 | 62 | 32 | 0 | within |
| notice-burst-6 | 22.810 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.321 | 62 | 32 | 0 | within |
| notice-burst-6 | 5.623 | 62 | 32 | 0 | within |
| notice-burst-6 | 23.101 | 62 | 32 | 0 | within |
| notice-burst-6 | 24.842 | 62 | 32 | 0 | within |
| notice-burst-6 | 25.133 | 62 | 32 | 0 | within |
| notice-burst-6 | 26.804 | 62 | 32 | 0 | within |
| notice-burst-6 | 27.092 | 62 | 32 | 0 | within |
| notice-burst-6 | 28.763 | 62 | 32 | 0 | within |
| notice-burst-6 | 29.056 | 62 | 32 | 0 | within |
| notice-burst-6 | 30.724 | 62 | 32 | 0 | within |
| notice-burst-6 | 1.864 | 62 | 32 | 0 | within |
| notice-burst-6 | 2.194 | 62 | 32 | 0 | within |
| notice-burst-6 | 31.005 | 62 | 32 | 0 | within |
| notice-burst-6 | 32.659 | 62 | 32 | 0 | within |
| notice-burst-6 | 32.938 | 62 | 32 | 0 | within |
| notice-burst-6 | 34.602 | 62 | 32 | 0 | within |
| notice-burst-6 | 34.882 | 62 | 32 | 0 | within |
| notice-burst-6 | 36.821 | 62 | 32 | 0 | within |
| notice-burst-6 | 37.098 | 62 | 32 | 0 | within |
| notice-burst-6 | 38.732 | 62 | 32 | 0 | within |
| notice-burst-6 | 39.013 | 62 | 32 | 0 | within |
| notice-burst-6 | 40.647 | 62 | 32 | 0 | within |
| notice-burst-6 | 40.927 | 62 | 32 | 0 | within |
| notice-burst-6 | 42.855 | 62 | 32 | 0 | within |
| notice-burst-6 | 43.136 | 62 | 32 | 0 | within |
| notice-burst-6 | 44.811 | 62 | 32 | 0 | within |
| notice-burst-6 | 45.090 | 62 | 32 | 0 | within |
| notice-burst-6 | 46.704 | 62 | 32 | 0 | within |
| notice-burst-6 | 46.972 | 62 | 32 | 0 | within |
| notice-burst-6 | 48.817 | 62 | 32 | 0 | within |
| notice-burst-6 | 49.115 | 62 | 32 | 0 | within |
| notice-burst-6 | 50.711 | 62 | 32 | 0 | within |
| notice-burst-7 | 2.304 | 62 | 32 | 1 | within |
| notice-burst-7 | 2.603 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.071 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.372 | 62 | 32 | 1 | within |
| notice-burst-7 | 4.980 | 62 | 32 | 1 | within |
| notice-burst-7 | 5.276 | 62 | 32 | 1 | within |
| notice-burst-7 | 6.369 | 62 | 32 | 1 | within |
| notice-burst-7 | 6.670 | 62 | 32 | 1 | within |
| notice-burst-7 | 7.042 | 62 | 32 | 1 | within |
| notice-burst-7 | 7.336 | 62 | 32 | 1 | within |
| notice-burst-7 | 18.253 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.384 | 62 | 32 | 1 | within |
| notice-burst-7 | 22.674 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.409 | 62 | 32 | 1 | within |
| notice-burst-7 | 24.698 | 62 | 32 | 1 | within |
| notice-burst-7 | 26.373 | 62 | 32 | 1 | within |
| notice-burst-7 | 26.666 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.338 | 62 | 32 | 1 | within |
| notice-burst-7 | 28.617 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.280 | 62 | 32 | 1 | within |
| notice-burst-7 | 30.560 | 62 | 32 | 1 | within |
| notice-burst-7 | 32.513 | 62 | 32 | 1 | within |
| notice-burst-7 | 32.793 | 62 | 32 | 1 | within |
| notice-burst-7 | 34.460 | 62 | 32 | 1 | within |
| notice-burst-7 | 34.741 | 62 | 32 | 1 | within |
| notice-burst-7 | 36.377 | 62 | 32 | 1 | within |
| notice-burst-7 | 36.654 | 62 | 32 | 1 | within |
| notice-burst-7 | 38.292 | 62 | 32 | 1 | within |
| notice-burst-7 | 38.572 | 62 | 32 | 1 | within |
| notice-burst-7 | 40.503 | 62 | 32 | 1 | within |
| notice-burst-7 | 40.783 | 62 | 32 | 1 | within |
| notice-burst-7 | 42.414 | 62 | 32 | 1 | within |
| notice-burst-7 | 42.694 | 62 | 32 | 1 | within |
| notice-burst-7 | 44.368 | 62 | 32 | 1 | within |
| notice-burst-7 | 44.647 | 62 | 32 | 1 | within |
| notice-burst-7 | 46.261 | 62 | 32 | 1 | within |
| notice-burst-7 | 46.529 | 62 | 32 | 1 | within |
| notice-burst-7 | 48.374 | 62 | 32 | 1 | within |
| notice-burst-7 | 48.672 | 62 | 32 | 1 | within |
| notice-burst-7 | 50.269 | 62 | 32 | 1 | within |

Latest: 51.275 ms, notice-burst-1.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| notice-every-0 | 303 | 90,284 (0.903) | 48,410 (0.484) |
| notice-every-1 | 303 | 90,284 (0.903) | 48,410 (0.484) |
| notice-every-2 | 303 | 90,284 (0.903) | 48,410 (0.484) |
| notice-every-3 | 303 | 90,690 (0.907) | 48,410 (0.484) |
| notice-every-4 | 303 | 90,284 (0.903) | 48,410 (0.484) |
| notice-every-5 | 303 | 90,284 (0.903) | 48,410 (0.484) |
| notice-every-6 | 303 | 90,284 (0.903) | 48,410 (0.484) |
| notice-every-7 | 303 | 90,284 (0.903) | 48,410 (0.484) |
| notice-burst-0 | 313 | 119,041 (1.190) | 48,410 (0.484) |
| notice-burst-1 | 313 | 119,958 (1.200) | 48,410 (0.484) |
| notice-burst-2 | 313 | 90,284 (0.903) | 48,410 (0.484) |
| notice-burst-3 | 313 | 90,690 (0.907) | 48,410 (0.484) |
| notice-burst-4 | 313 | 90,284 (0.903) | 48,410 (0.484) |
| notice-burst-5 | 313 | 122,049 (1.220) | 48,410 (0.484) |
| notice-burst-6 | 313 | 120,748 (1.207) | 48,410 (0.484) |
| notice-burst-7 | 313 | 120,371 (1.204) | 48,410 (0.484) |

Longest pass that carries a step: 122,049 CPU cycles (1.220 ms), notice-burst-5; longest step: 48,410 (0.484 ms), notice-every-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.0.if0` | 627,138 | 6.271 | 62 | 66 | fits | 68,959 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.0.if0` | 657,121 | 6.571 | 62 | 66 | fits | 68,959 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.1.if0` | 255,894 | 2.559 | 62 | 66 | fits | 70,836 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.1.if0` | 286,508 | 2.865 | 62 | 66 | fits | 70,836 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.2.if0` | 426,575 | 4.266 | 62 | 66 | fits | 70,657 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.2.if0` | 457,279 | 4.573 | 62 | 66 | fits | 70,657 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.3.if0` | 826,652 | 8.267 | 62 | 66 | fits | 68,561 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.3.if0` | 856,700 | 8.567 | 62 | 66 | fits | 68,561 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.4.if0` | 1,025,473 | 10.255 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.4.if0` | 1,055,377 | 10.554 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.5.if0` | 1,222,420 | 12.224 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.5.if0` | 1,252,388 | 12.524 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.6.if0` | 1,424,114 | 14.241 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.6.if0` | 1,454,097 | 14.541 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.7.if0` | 1,620,071 | 16.201 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.7.if0` | 1,650,263 | 16.503 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.5.8.if0` | 1,847,172 | 18.472 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.5.8.if0` | 1,877,299 | 18.773 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.0.if0` | 2,041,421 | 20.414 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.0.if0` | 2,071,479 | 20.715 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.1.if0` | 2,471,590 | 24.716 | 62 | 66 | fits | 37,594 | 101 | 0.290 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.1.if0` | 2,845,859 | 28.459 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.2.if0` | 2,873,842 | 28.738 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.2.if0` | 3,038,677 | 30.387 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.3.if0` | 3,066,666 | 30.667 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.3.if0` | 3,230,375 | 32.304 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.4.if0` | 3,258,121 | 32.581 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.4.if0` | 3,422,961 | 34.230 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.5.if0` | 3,451,304 | 34.513 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.5.if0` | 3,644,203 | 36.442 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.6.if0` | 3,672,249 | 36.722 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.6.if0` | 3,835,228 | 38.352 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.7.if0` | 3,863,384 | 38.634 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.7.if0` | 4,025,276 | 40.253 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-0.notices.f.6.8.if0` | 4,053,112 | 40.531 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.6.8.if0` | 4,270,209 | 42.702 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-0.notices.27.9.0.if0` | 4,296,790 | 42.968 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-0.notices.28.9.0.if0` | 4,429,568 | 44.296 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.9.0.if0` | 4,459,330 | 44.593 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-0.notices.29.36.0.if0` | 4,647,798 | 46.478 | 62 | 66 | fits | 36,530 | 102 | 0.153 |
| ADP record, every channel at its refill rate, the longest | `notice-every-0.held.adp.if1` | 714,843 | 7.148 | 20 | 200 | fits | 142,145 | 105 | 0.607 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-0.held.acmp.if0` | 694,575 | 6.946 | 20 | 20 | fits | 142,145 | 105 | 0.607 |
| AECP record, every channel at its refill rate, the longest | `notice-every-0.held.aecp.if1` | 509,742 | 5.097 | 20 | 24 | fits | 165,002 | 108 | 0.428 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-0.held.maap.if0` | 655,100 | 6.551 | 20 | 50 | fits | 142,145 | 105 | 0.607 |
| SRP record, every channel at its refill rate, the longest | `notice-every-0.held.srp.if1` | 1,110,345 | 11.103 | 20 | 20 | fits | 58,628 | 24 | 0.778 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if0` | 131,562 | 1.316 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-0.mrpdu.periodic.if1` | 181,466 | 1.815 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.0.if0` | 619,735 | 6.197 | 62 | 66 | fits | 68,834 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.0.if0` | 649,718 | 6.497 | 62 | 66 | fits | 68,834 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.1.if0` | 217,668 | 2.177 | 62 | 66 | fits | 70,588 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.1.if0` | 248,282 | 2.483 | 62 | 66 | fits | 70,588 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.2.if0` | 819,345 | 8.193 | 62 | 66 | fits | 68,724 | 201 | 0.145 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.2.if0` | 849,406 | 8.494 | 62 | 66 | fits | 68,724 | 201 | 0.145 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.3.if0` | 419,920 | 4.199 | 62 | 66 | fits | 71,087 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.3.if0` | 450,777 | 4.508 | 62 | 66 | fits | 71,087 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.4.if0` | 1,018,412 | 10.184 | 62 | 66 | fits | 68,694 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.4.if0` | 1,048,316 | 10.483 | 62 | 66 | fits | 68,694 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.5.if0` | 1,215,363 | 12.154 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.5.if0` | 1,245,331 | 12.453 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.6.if0` | 1,417,067 | 14.171 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.6.if0` | 1,447,050 | 14.470 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.7.if0` | 1,613,014 | 16.130 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.7.if0` | 1,643,206 | 16.432 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.5.8.if0` | 1,809,552 | 18.096 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.5.8.if0` | 1,839,679 | 18.397 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.0.if0` | 2,004,102 | 20.041 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.0.if0` | 2,034,160 | 20.342 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.1.if0` | 2,434,121 | 24.341 | 62 | 66 | fits | 37,594 | 101 | 0.290 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.1.if0` | 2,808,376 | 28.084 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.2.if0` | 2,836,359 | 28.364 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.2.if0` | 3,001,194 | 30.012 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.3.if0` | 3,029,183 | 30.292 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.3.if0` | 3,222,979 | 32.230 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.4.if0` | 3,250,725 | 32.507 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.4.if0` | 3,415,226 | 34.152 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.5.if0` | 3,443,569 | 34.436 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.5.if0` | 3,606,815 | 36.068 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.6.if0` | 3,634,861 | 36.349 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.6.if0` | 3,827,759 | 38.278 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.7.if0` | 3,855,915 | 38.559 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.7.if0` | 4,017,496 | 40.175 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-1.notices.f.6.8.if0` | 4,045,332 | 40.453 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.6.8.if0` | 4,262,773 | 42.628 | 62 | 66 | fits | 64,788 | 200 | 0.160 |
| a queued notice, from its port's answer | `notice-every-1.notices.27.9.0.if0` | 4,289,354 | 42.894 | 62 | 66 | fits | 64,788 | 200 | 0.160 |
| a queued notice, from its port's answer | `notice-every-1.notices.28.9.0.if0` | 4,422,132 | 44.221 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.9.0.if0` | 4,451,894 | 44.519 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-1.notices.29.36.0.if0` | 4,611,255 | 46.113 | 62 | 66 | fits | 36,530 | 102 | 0.153 |
| ADP record, every channel at its refill rate, the longest | `notice-every-1.held.adp.if1` | 704,819 | 7.048 | 20 | 200 | fits | 129,393 | 102 | 0.545 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-1.held.acmp.if0` | 684,551 | 6.846 | 20 | 20 | fits | 129,393 | 102 | 0.545 |
| AECP record, every channel at its refill rate, the longest | `notice-every-1.held.aecp.if1` | 404,455 | 4.045 | 20 | 24 | fits | 129,412 | 92 | 0.481 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-1.held.maap.if0` | 645,076 | 6.451 | 20 | 50 | fits | 129,393 | 102 | 0.545 |
| SRP record, every channel at its refill rate, the longest | `notice-every-1.held.srp.if1` | 1,143,888 | 11.439 | 20 | 20 | fits | 80,398 | 43 | 0.696 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if0` | 132,158 | 1.322 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-1.mrpdu.periodic.if1` | 182,108 | 1.821 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.0.if0` | 620,901 | 6.209 | 62 | 66 | fits | 68,959 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.0.if0` | 650,884 | 6.509 | 62 | 66 | fits | 68,959 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.1.if0` | 217,614 | 2.176 | 62 | 66 | fits | 71,028 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.1.if0` | 248,228 | 2.482 | 62 | 66 | fits | 71,028 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.2.if0` | 420,241 | 4.202 | 62 | 66 | fits | 70,717 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.2.if0` | 450,945 | 4.509 | 62 | 66 | fits | 70,717 | 203 | 0.158 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.3.if0` | 820,318 | 8.203 | 62 | 66 | fits | 68,561 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.3.if0` | 850,366 | 8.504 | 62 | 66 | fits | 68,561 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.4.if0` | 1,019,236 | 10.192 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.4.if0` | 1,049,140 | 10.491 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.5.if0` | 1,216,173 | 12.162 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.5.if0` | 1,246,141 | 12.461 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.6.if0` | 1,417,877 | 14.179 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.6.if0` | 1,447,860 | 14.479 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.7.if0` | 1,644,470 | 16.445 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.7.if0` | 1,674,662 | 16.747 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.5.8.if0` | 1,840,669 | 18.407 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.5.8.if0` | 1,870,796 | 18.708 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.0.if0` | 2,035,442 | 20.354 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.0.if0` | 2,065,500 | 20.655 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.1.if0` | 2,465,524 | 24.655 | 62 | 66 | fits | 37,529 | 101 | 0.290 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.1.if0` | 2,839,793 | 28.398 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.2.if0` | 2,867,776 | 28.678 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.2.if0` | 3,032,388 | 30.324 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.3.if0` | 3,060,377 | 30.604 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.3.if0` | 3,224,309 | 32.243 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.4.if0` | 3,252,055 | 32.521 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.4.if0` | 3,416,672 | 34.167 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.5.if0` | 3,445,015 | 34.450 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.5.if0` | 3,637,928 | 36.379 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.6.if0` | 3,665,974 | 36.660 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.6.if0` | 3,829,190 | 38.292 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.7.if0` | 3,857,346 | 38.573 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.7.if0` | 4,019,015 | 40.190 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-2.notices.f.6.8.if0` | 4,046,851 | 40.469 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.6.8.if0` | 4,264,263 | 42.643 | 62 | 66 | fits | 64,788 | 200 | 0.160 |
| a queued notice, from its port's answer | `notice-every-2.notices.27.9.0.if0` | 4,290,844 | 42.908 | 62 | 66 | fits | 64,788 | 200 | 0.160 |
| a queued notice, from its port's answer | `notice-every-2.notices.28.9.0.if0` | 4,423,636 | 44.236 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.9.0.if0` | 4,453,398 | 44.534 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-2.notices.29.36.0.if0` | 4,641,866 | 46.419 | 62 | 66 | fits | 36,530 | 102 | 0.153 |
| ADP record, every channel at its refill rate, the longest | `notice-every-2.held.adp.if1` | 674,370 | 6.744 | 20 | 200 | fits | 129,059 | 129 | 0.589 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-2.held.acmp.if0` | 654,102 | 6.541 | 20 | 20 | fits | 129,059 | 129 | 0.589 |
| AECP record, every channel at its refill rate, the longest | `notice-every-2.held.aecp.if1` | 482,120 | 4.821 | 20 | 24 | fits | 164,303 | 106 | 0.425 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-2.held.maap.if0` | 614,627 | 6.146 | 20 | 50 | fits | 129,059 | 129 | 0.589 |
| SRP record, every channel at its refill rate, the longest | `notice-every-2.held.srp.if1` | 1,085,313 | 10.853 | 20 | 20 | fits | 76,912 | 32 | 0.697 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if0` | 140,437 | 1.404 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-2.mrpdu.periodic.if1` | 190,413 | 1.904 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.0.if0` | 626,791 | 6.268 | 62 | 66 | fits | 68,899 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.0.if0` | 656,774 | 6.568 | 62 | 66 | fits | 68,899 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.1.if0` | 248,792 | 2.488 | 62 | 66 | fits | 70,836 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.1.if0` | 279,406 | 2.794 | 62 | 66 | fits | 70,836 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.2.if0` | 458,420 | 4.584 | 62 | 66 | fits | 70,652 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.2.if0` | 489,124 | 4.891 | 62 | 66 | fits | 70,652 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.3.if0` | 826,208 | 8.262 | 62 | 66 | fits | 68,561 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.3.if0` | 856,256 | 8.563 | 62 | 66 | fits | 68,561 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.4.if0` | 1,025,126 | 10.251 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.4.if0` | 1,055,030 | 10.550 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.5.if0` | 1,222,025 | 12.220 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.5.if0` | 1,251,993 | 12.520 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.6.if0` | 1,423,729 | 14.237 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.6.if0` | 1,453,712 | 14.537 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.7.if0` | 1,650,322 | 16.503 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.7.if0` | 1,680,514 | 16.805 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.5.8.if0` | 1,846,521 | 18.465 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.5.8.if0` | 1,876,648 | 18.766 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.0.if0` | 2,041,294 | 20.413 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.0.if0` | 2,071,352 | 20.714 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.1.if0` | 2,471,376 | 24.714 | 62 | 66 | fits | 37,529 | 101 | 0.290 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.1.if0` | 2,845,645 | 28.456 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.2.if0` | 2,873,628 | 28.736 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.2.if0` | 3,038,240 | 30.382 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.3.if0` | 3,066,229 | 30.662 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.3.if0` | 3,230,161 | 32.302 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.4.if0` | 3,257,907 | 32.579 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.4.if0` | 3,422,524 | 34.225 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.5.if0` | 3,450,867 | 34.509 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.5.if0` | 3,643,780 | 36.438 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.6.if0` | 3,671,826 | 36.718 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.6.if0` | 3,835,042 | 38.350 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.7.if0` | 3,863,198 | 38.632 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.7.if0` | 4,024,867 | 40.249 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-3.notices.f.6.8.if0` | 4,052,703 | 40.527 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.6.8.if0` | 4,270,192 | 42.702 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-3.notices.27.9.0.if0` | 4,296,773 | 42.968 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-3.notices.28.9.0.if0` | 4,429,565 | 44.296 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.9.0.if0` | 4,459,327 | 44.593 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-3.notices.29.36.0.if0` | 4,647,795 | 46.478 | 62 | 66 | fits | 36,530 | 102 | 0.153 |
| ADP record, every channel at its refill rate, the longest | `notice-every-3.held.adp.if1` | 464,420 | 4.644 | 20 | 200 | fits | 74,483 | 79 | 0.315 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-3.held.acmp.if0` | 652,435 | 6.524 | 20 | 20 | fits | 136,305 | 134 | 0.564 |
| AECP record, every channel at its refill rate, the longest | `notice-every-3.held.aecp.if1` | 473,199 | 4.732 | 20 | 24 | fits | 164,810 | 106 | 0.427 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-3.held.maap.if0` | 612,960 | 6.130 | 20 | 50 | fits | 136,305 | 134 | 0.564 |
| SRP record, every channel at its refill rate, the longest | `notice-every-3.held.srp.if1` | 1,083,559 | 10.836 | 20 | 20 | fits | 76,912 | 32 | 0.697 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if0` | 133,902 | 1.339 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-3.mrpdu.periodic.if1` | 183,878 | 1.839 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.0.if0` | 419,564 | 4.196 | 62 | 66 | fits | 69,814 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.0.if0` | 449,592 | 4.496 | 62 | 66 | fits | 69,814 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.1.if0` | 619,852 | 6.199 | 62 | 66 | fits | 69,358 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.1.if0` | 650,069 | 6.501 | 62 | 66 | fits | 69,358 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.2.if0` | 217,397 | 2.174 | 62 | 66 | fits | 70,906 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.2.if0` | 248,423 | 2.484 | 62 | 66 | fits | 70,906 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.3.if0` | 819,558 | 8.196 | 62 | 66 | fits | 68,496 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.3.if0` | 849,606 | 8.496 | 62 | 66 | fits | 68,496 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.4.if0` | 1,018,188 | 10.182 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.4.if0` | 1,048,092 | 10.481 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.5.if0` | 1,215,348 | 12.153 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.5.if0` | 1,245,316 | 12.453 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.6.if0` | 1,416,766 | 14.168 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.6.if0` | 1,446,749 | 14.467 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.7.if0` | 1,612,936 | 16.129 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.7.if0` | 1,643,128 | 16.431 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.5.8.if0` | 1,809,251 | 18.093 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.5.8.if0` | 1,839,378 | 18.394 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.0.if0` | 2,004,024 | 20.040 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.0.if0` | 2,034,082 | 20.341 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.1.if0` | 2,433,920 | 24.339 | 62 | 66 | fits | 37,529 | 101 | 0.290 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.1.if0` | 2,808,175 | 28.082 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.2.if0` | 2,836,158 | 28.362 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.2.if0` | 3,000,784 | 30.008 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.3.if0` | 3,028,773 | 30.288 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.3.if0` | 3,222,569 | 32.226 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.4.if0` | 3,250,315 | 32.503 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.4.if0` | 3,414,983 | 34.150 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.5.if0` | 3,443,326 | 34.433 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.5.if0` | 3,606,349 | 36.063 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.6.if0` | 3,634,395 | 36.344 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.6.if0` | 3,797,699 | 37.977 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.7.if0` | 3,825,855 | 38.259 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.7.if0` | 4,017,110 | 40.171 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-4.notices.f.6.8.if0` | 4,044,946 | 40.449 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.6.8.if0` | 4,261,942 | 42.619 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-4.notices.27.9.0.if0` | 4,288,523 | 42.885 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-4.notices.28.9.0.if0` | 4,421,301 | 44.213 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.9.0.if0` | 4,451,063 | 44.511 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-4.notices.29.36.0.if0` | 4,610,661 | 46.107 | 62 | 66 | fits | 36,530 | 102 | 0.153 |
| ADP record, every channel at its refill rate, the longest | `notice-every-4.held.adp.if1` | 436,007 | 4.360 | 20 | 200 | fits | 39,830 | 27 | 0.630 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-4.held.acmp.if0` | 681,088 | 6.811 | 20 | 20 | fits | 139,244 | 113 | 0.619 |
| AECP record, every channel at its refill rate, the longest | `notice-every-4.held.aecp.if1` | 493,081 | 4.931 | 20 | 24 | fits | 164,647 | 108 | 0.424 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-4.held.maap.if0` | 641,613 | 6.416 | 20 | 50 | fits | 139,244 | 113 | 0.619 |
| SRP record, every channel at its refill rate, the longest | `notice-every-4.held.srp.if1` | 1,081,967 | 10.820 | 20 | 20 | fits | 58,503 | 24 | 0.775 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if0` | 146,653 | 1.467 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-4.mrpdu.periodic.if1` | 196,557 | 1.966 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.0.if0` | 626,745 | 6.267 | 62 | 66 | fits | 68,899 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.0.if0` | 656,728 | 6.567 | 62 | 66 | fits | 68,899 | 203 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.1.if0` | 248,733 | 2.487 | 62 | 66 | fits | 70,836 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.1.if0` | 279,347 | 2.793 | 62 | 66 | fits | 70,836 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.2.if0` | 458,388 | 4.584 | 62 | 66 | fits | 70,652 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.2.if0` | 489,092 | 4.891 | 62 | 66 | fits | 70,652 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.3.if0` | 826,162 | 8.262 | 62 | 66 | fits | 68,561 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.3.if0` | 856,210 | 8.562 | 62 | 66 | fits | 68,561 | 203 | 0.140 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.4.if0` | 1,025,080 | 10.251 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.4.if0` | 1,054,984 | 10.550 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.5.if0` | 1,221,979 | 12.220 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.5.if0` | 1,251,947 | 12.519 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.6.if0` | 1,423,669 | 14.237 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.6.if0` | 1,453,652 | 14.537 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.7.if0` | 1,650,276 | 16.503 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.7.if0` | 1,680,468 | 16.805 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.5.8.if0` | 1,846,489 | 18.465 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.5.8.if0` | 1,876,616 | 18.766 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.0.if0` | 2,041,262 | 20.413 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.0.if0` | 2,071,320 | 20.713 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.1.if0` | 2,471,262 | 24.713 | 62 | 66 | fits | 37,529 | 101 | 0.290 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.1.if0` | 2,845,517 | 28.455 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.2.if0` | 2,873,500 | 28.735 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.2.if0` | 3,038,112 | 30.381 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.3.if0` | 3,066,101 | 30.661 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.3.if0` | 3,230,019 | 32.300 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.4.if0` | 3,257,765 | 32.578 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.4.if0` | 3,422,382 | 34.224 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.5.if0` | 3,450,725 | 34.507 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.5.if0` | 3,643,638 | 36.436 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.6.if0` | 3,671,684 | 36.717 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.6.if0` | 3,834,900 | 38.349 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.7.if0` | 3,863,056 | 38.631 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.7.if0` | 4,024,725 | 40.247 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-5.notices.f.6.8.if0` | 4,052,561 | 40.526 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.6.8.if0` | 4,269,875 | 42.699 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-5.notices.27.9.0.if0` | 4,296,456 | 42.965 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-5.notices.28.9.0.if0` | 4,429,248 | 44.292 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.9.0.if0` | 4,459,010 | 44.590 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-5.notices.29.36.0.if0` | 4,647,464 | 46.475 | 62 | 66 | fits | 36,530 | 102 | 0.153 |
| ADP record, every channel at its refill rate, the longest | `notice-every-5.held.adp.if1` | 678,417 | 6.784 | 20 | 200 | fits | 131,103 | 110 | 0.541 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-5.held.acmp.if0` | 658,149 | 6.581 | 20 | 20 | fits | 131,103 | 110 | 0.541 |
| AECP record, every channel at its refill rate, the longest | `notice-every-5.held.aecp.if1` | 404,078 | 4.041 | 20 | 24 | fits | 117,368 | 83 | 0.462 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-5.held.maap.if0` | 618,674 | 6.187 | 20 | 50 | fits | 131,103 | 110 | 0.541 |
| SRP record, every channel at its refill rate, the longest | `notice-every-5.held.srp.if1` | 1,114,558 | 11.146 | 20 | 20 | fits | 69,037 | 33 | 0.740 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if0` | 130,844 | 1.308 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-5.mrpdu.periodic.if1` | 180,794 | 1.808 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.0.if0` | 216,932 | 2.169 | 62 | 66 | fits | 69,731 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.0.if0` | 247,052 | 2.471 | 62 | 66 | fits | 69,731 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.1.if0` | 619,543 | 6.195 | 62 | 66 | fits | 69,423 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.1.if0` | 649,760 | 6.498 | 62 | 66 | fits | 69,423 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.2.if0` | 418,876 | 4.189 | 62 | 66 | fits | 70,644 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.2.if0` | 449,580 | 4.496 | 62 | 66 | fits | 70,644 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.3.if0` | 819,249 | 8.192 | 62 | 66 | fits | 68,496 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.3.if0` | 849,297 | 8.493 | 62 | 66 | fits | 68,496 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.4.if0` | 1,017,879 | 10.179 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.4.if0` | 1,047,783 | 10.478 | 62 | 66 | fits | 68,565 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.5.if0` | 1,215,039 | 12.150 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.5.if0` | 1,245,007 | 12.450 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.6.if0` | 1,416,520 | 14.165 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.6.if0` | 1,446,503 | 14.465 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.7.if0` | 1,612,690 | 16.127 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.7.if0` | 1,642,882 | 16.429 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.5.8.if0` | 1,808,991 | 18.090 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.5.8.if0` | 1,839,118 | 18.391 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.0.if0` | 2,003,778 | 20.038 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.0.if0` | 2,033,836 | 20.338 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.1.if0` | 2,433,663 | 24.337 | 62 | 66 | fits | 37,529 | 101 | 0.290 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.1.if0` | 2,807,918 | 28.079 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.2.if0` | 2,835,901 | 28.359 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.2.if0` | 3,000,527 | 30.005 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.3.if0` | 3,028,516 | 30.285 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.3.if0` | 3,222,312 | 32.223 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.4.if0` | 3,250,058 | 32.501 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.4.if0` | 3,414,726 | 34.147 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.5.if0` | 3,443,069 | 34.431 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.5.if0` | 3,606,106 | 36.061 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.6.if0` | 3,634,152 | 36.342 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.6.if0` | 3,797,456 | 37.975 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.7.if0` | 3,825,612 | 38.256 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.7.if0` | 4,016,867 | 40.169 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-6.notices.f.6.8.if0` | 4,044,703 | 40.447 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.6.8.if0` | 4,261,860 | 42.619 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-6.notices.27.9.0.if0` | 4,288,441 | 42.884 | 62 | 66 | fits | 64,817 | 200 | 0.162 |
| a queued notice, from its port's answer | `notice-every-6.notices.28.9.0.if0` | 4,392,211 | 43.922 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.9.0.if0` | 4,421,973 | 44.220 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-6.notices.29.36.0.if0` | 4,610,448 | 46.104 | 62 | 66 | fits | 36,530 | 102 | 0.153 |
| ADP record, every channel at its refill rate, the longest | `notice-every-6.held.adp.if1` | 713,535 | 7.135 | 20 | 200 | fits | 141,863 | 123 | 0.607 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-6.held.acmp.if0` | 693,267 | 6.933 | 20 | 20 | fits | 141,863 | 123 | 0.607 |
| AECP record, every channel at its refill rate, the longest | `notice-every-6.held.aecp.if1` | 502,824 | 5.028 | 20 | 24 | fits | 163,327 | 104 | 0.430 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-6.held.maap.if0` | 653,792 | 6.538 | 20 | 50 | fits | 141,863 | 123 | 0.607 |
| SRP record, every channel at its refill rate, the longest | `notice-every-6.held.srp.if1` | 1,094,101 | 10.941 | 20 | 20 | fits | 58,503 | 24 | 0.775 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if0` | 140,196 | 1.402 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-6.mrpdu.periodic.if1` | 190,172 | 1.902 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.0.if0` | 619,825 | 6.198 | 62 | 66 | fits | 68,834 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.0.if0` | 649,808 | 6.498 | 62 | 66 | fits | 68,834 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.1.if0` | 217,538 | 2.175 | 62 | 66 | fits | 70,780 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.1.if0` | 248,152 | 2.482 | 62 | 66 | fits | 70,780 | 203 | 0.152 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.2.if0` | 819,658 | 8.197 | 62 | 66 | fits | 68,724 | 201 | 0.145 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.2.if0` | 849,719 | 8.497 | 62 | 66 | fits | 68,724 | 201 | 0.145 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.3.if0` | 420,219 | 4.202 | 62 | 66 | fits | 71,087 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.3.if0` | 451,076 | 4.511 | 62 | 66 | fits | 71,087 | 201 | 0.156 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.4.if0` | 1,018,502 | 10.185 | 62 | 66 | fits | 68,694 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.4.if0` | 1,048,406 | 10.484 | 62 | 66 | fits | 68,694 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.5.if0` | 1,215,662 | 12.157 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.5.if0` | 1,245,630 | 12.456 | 62 | 66 | fits | 68,049 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.6.if0` | 1,417,129 | 14.171 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.6.if0` | 1,447,112 | 14.471 | 62 | 66 | fits | 68,094 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.7.if0` | 1,613,313 | 16.133 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.7.if0` | 1,643,505 | 16.435 | 62 | 66 | fits | 68,026 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.5.8.if0` | 1,809,614 | 18.096 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.5.8.if0` | 1,839,741 | 18.397 | 62 | 66 | fits | 68,289 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.0.if0` | 2,004,401 | 20.044 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.0.if0` | 2,034,459 | 20.345 | 62 | 66 | fits | 66,717 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.1.if0` | 2,434,306 | 24.343 | 62 | 66 | fits | 37,529 | 101 | 0.290 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.1.if0` | 2,808,575 | 28.086 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.2.if0` | 2,836,558 | 28.366 | 62 | 66 | fits | 66,325 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.2.if0` | 3,001,170 | 30.012 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.3.if0` | 3,029,159 | 30.292 | 62 | 66 | fits | 66,111 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.3.if0` | 3,222,969 | 32.230 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.4.if0` | 3,250,715 | 32.507 | 62 | 66 | fits | 65,795 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.4.if0` | 3,415,453 | 34.155 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.5.if0` | 3,443,796 | 34.438 | 62 | 66 | fits | 67,104 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.5.if0` | 3,606,833 | 36.068 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.6.if0` | 3,634,879 | 36.349 | 62 | 66 | fits | 66,198 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.6.if0` | 3,827,763 | 38.278 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.7.if0` | 3,855,919 | 38.559 | 62 | 66 | fits | 66,257 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.7.if0` | 4,017,709 | 40.177 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-7.notices.f.6.8.if0` | 4,045,545 | 40.455 | 62 | 66 | fits | 65,432 | 201 | 0.131 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.6.8.if0` | 4,262,600 | 42.626 | 62 | 66 | fits | 64,788 | 200 | 0.160 |
| a queued notice, from its port's answer | `notice-every-7.notices.27.9.0.if0` | 4,289,181 | 42.892 | 62 | 66 | fits | 64,788 | 200 | 0.160 |
| a queued notice, from its port's answer | `notice-every-7.notices.28.9.0.if0` | 4,421,973 | 44.220 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.9.0.if0` | 4,451,735 | 44.517 | 62 | 66 | fits | 63,253 | 200 | 0.118 |
| a queued notice, from its port's answer | `notice-every-7.notices.29.36.0.if0` | 4,611,319 | 46.113 | 62 | 66 | fits | 36,530 | 102 | 0.153 |
| ADP record, every channel at its refill rate, the longest | `notice-every-7.held.adp.if1` | 703,864 | 7.039 | 20 | 200 | fits | 128,820 | 101 | 0.558 |
| ACMP record, every channel at its refill rate, the longest | `notice-every-7.held.acmp.if0` | 683,596 | 6.836 | 20 | 20 | fits | 128,820 | 101 | 0.558 |
| AECP record, every channel at its refill rate, the longest | `notice-every-7.held.aecp.if1` | 404,110 | 4.041 | 20 | 24 | fits | 117,285 | 83 | 0.460 |
| MAAP record, every channel at its refill rate, the longest | `notice-every-7.held.maap.if0` | 644,121 | 6.441 | 20 | 50 | fits | 128,820 | 101 | 0.558 |
| SRP record, every channel at its refill rate, the longest | `notice-every-7.held.srp.if1` | 1,140,059 | 11.401 | 20 | 20 | fits | 69,048 | 33 | 0.740 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if0` | 118,940 | 1.189 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `notice-every-7.mrpdu.periodic.if1` | 169,975 | 1.700 | 20 | 20 | fits | 0 | - | 0.000 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.0.if0` | 371,888 | 3.719 | 62 | 66 | fits | 67,919 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.0.if0` | 401,268 | 4.013 | 62 | 66 | fits | 67,919 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.1.if0` | 518,879 | 5.189 | 62 | 66 | fits | 119,041 | 212 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.1.if0` | 549,096 | 5.491 | 62 | 66 | fits | 119,041 | 212 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.2.if0` | 1,738,995 | 17.390 | 62 | 66 | fits | 40,615 | 100 | 0.341 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.2.if0` | 2,122,641 | 21.226 | 62 | 66 | fits | 68,822 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.3.if0` | 2,151,741 | 21.517 | 62 | 66 | fits | 68,822 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.3.if0` | 2,319,894 | 23.199 | 62 | 66 | fits | 68,491 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.4.if0` | 609,195 | 6.092 | 62 | 66 | fits | 68,036 | 201 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.4.if0` | 639,111 | 6.391 | 62 | 66 | fits | 68,036 | 201 | 0.082 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.5.if0` | 2,349,029 | 23.490 | 62 | 66 | fits | 68,491 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.5.if0` | 2,522,968 | 25.230 | 62 | 66 | fits | 68,313 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.6.if0` | 2,551,992 | 25.520 | 62 | 66 | fits | 68,313 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.6.if0` | 2,719,390 | 27.194 | 62 | 66 | fits | 67,995 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.7.if0` | 298,238 | 2.982 | 62 | 66 | fits | 104,856 | 210 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.7.if0` | 330,633 | 3.306 | 62 | 66 | fits | 104,856 | 210 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.5.8.if0` | 2,748,598 | 27.486 | 62 | 66 | fits | 67,995 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.5.8.if0` | 2,946,106 | 29.461 | 62 | 66 | fits | 66,877 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.0.if0` | 2,974,016 | 29.740 | 62 | 66 | fits | 66,877 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.0.if0` | 3,140,183 | 31.402 | 62 | 66 | fits | 66,603 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.1.if0` | 3,168,180 | 31.682 | 62 | 66 | fits | 66,603 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.1.if0` | 3,333,499 | 33.335 | 62 | 66 | fits | 66,307 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.2.if0` | 3,361,485 | 33.615 | 62 | 66 | fits | 66,307 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.2.if0` | 3,527,855 | 35.279 | 62 | 66 | fits | 66,732 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.3.if0` | 3,555,929 | 35.559 | 62 | 66 | fits | 66,732 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.3.if0` | 3,719,961 | 37.200 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.4.if0` | 3,747,636 | 37.476 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.4.if0` | 3,940,928 | 39.409 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.5.if0` | 3,968,988 | 39.690 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.5.if0` | 4,132,312 | 41.323 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.6.if0` | 4,160,287 | 41.603 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.6.if0` | 4,323,495 | 43.235 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.7.if0` | 4,351,580 | 43.516 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.7.if0` | 4,519,075 | 45.191 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-0.notices.f.6.8.if0` | 4,546,963 | 45.470 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.6.8.if0` | 4,737,839 | 47.378 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-0.notices.27.9.0.if0` | 4,764,645 | 47.646 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-0.notices.28.9.0.if0` | 4,920,180 | 49.202 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.9.0.if0` | 4,949,941 | 49.499 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-0.notices.29.36.0.if0` | 5,127,380 | 51.274 | 62 | 66 | fits | 38,111 | 102 | 0.219 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-0.held.adp.if1` | 681,957 | 6.820 | 20 | 200 | fits | 137,126 | 83 | 0.558 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-0.held.acmp.if0` | 661,689 | 6.617 | 20 | 20 | fits | 137,126 | 83 | 0.558 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-0.held.aecp.if1` | 344,444 | 3.444 | 20 | 24 | fits | 157,486 | 110 | 0.424 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-0.held.maap.if0` | 485,088 | 4.851 | 20 | 50 | fits | 159,915 | 239 | 0.351 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-0.held.srp.if1` | 1,035,969 | 10.360 | 20 | 20 | fits | 56,958 | 23 | 0.771 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.0.if0` | 320,522 | 3.205 | 62 | 66 | fits | 68,705 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.0.if0` | 349,902 | 3.499 | 62 | 66 | fits | 68,705 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.1.if0` | 499,868 | 4.999 | 62 | 66 | fits | 119,958 | 210 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.1.if0` | 530,085 | 5.301 | 62 | 66 | fits | 119,958 | 210 | 0.202 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.2.if0` | 1,726,732 | 17.267 | 62 | 66 | fits | 40,842 | 100 | 0.345 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.2.if0` | 2,141,454 | 21.415 | 62 | 66 | fits | 68,881 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.3.if0` | 2,170,554 | 21.706 | 62 | 66 | fits | 68,881 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.3.if0` | 2,338,586 | 23.386 | 62 | 66 | fits | 68,491 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.4.if0` | 591,124 | 5.911 | 62 | 66 | fits | 68,292 | 203 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.4.if0` | 621,040 | 6.210 | 62 | 66 | fits | 68,292 | 203 | 0.080 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.5.if0` | 2,367,721 | 23.677 | 62 | 66 | fits | 68,491 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.5.if0` | 2,541,883 | 25.419 | 62 | 66 | fits | 68,313 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.6.if0` | 2,570,907 | 25.709 | 62 | 66 | fits | 68,313 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.6.if0` | 2,738,082 | 27.381 | 62 | 66 | fits | 68,063 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.7.if0` | 247,447 | 2.474 | 62 | 66 | fits | 104,876 | 212 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.7.if0` | 279,842 | 2.798 | 62 | 66 | fits | 104,876 | 212 | 0.210 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.5.8.if0` | 2,767,364 | 27.674 | 62 | 66 | fits | 68,063 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.5.8.if0` | 2,934,479 | 29.345 | 62 | 66 | fits | 66,868 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.0.if0` | 2,962,380 | 29.624 | 62 | 66 | fits | 66,868 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.0.if0` | 3,128,649 | 31.286 | 62 | 66 | fits | 66,671 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.1.if0` | 3,156,720 | 31.567 | 62 | 66 | fits | 66,671 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.1.if0` | 3,322,009 | 33.220 | 62 | 66 | fits | 66,301 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.2.if0` | 3,349,995 | 33.500 | 62 | 66 | fits | 66,301 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.2.if0` | 3,546,510 | 35.465 | 62 | 66 | fits | 66,658 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.3.if0` | 3,574,510 | 35.745 | 62 | 66 | fits | 66,658 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.3.if0` | 3,738,421 | 37.384 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.4.if0` | 3,766,096 | 37.661 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.4.if0` | 3,929,667 | 39.297 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.5.if0` | 3,957,727 | 39.577 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.5.if0` | 4,121,153 | 41.212 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.6.if0` | 4,149,128 | 41.491 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.6.if0` | 4,341,897 | 43.419 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.7.if0` | 4,369,982 | 43.700 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.7.if0` | 4,537,492 | 45.375 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-1.notices.f.6.8.if0` | 4,565,380 | 45.654 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.6.8.if0` | 4,726,776 | 47.268 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-1.notices.27.9.0.if0` | 4,753,582 | 47.536 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-1.notices.28.9.0.if0` | 4,938,161 | 49.382 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.9.0.if0` | 4,967,922 | 49.679 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-1.notices.29.36.0.if0` | 5,127,543 | 51.275 | 62 | 66 | fits | 36,579 | 102 | 0.155 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-1.held.adp.if1` | 666,793 | 6.668 | 20 | 200 | fits | 136,456 | 93 | 0.590 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-1.held.acmp.if0` | 646,525 | 6.465 | 20 | 20 | fits | 136,456 | 93 | 0.590 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-1.held.aecp.if1` | 329,230 | 3.292 | 20 | 24 | fits | 162,919 | 113 | 0.425 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-1.held.maap.if0` | 607,050 | 6.071 | 20 | 50 | fits | 136,456 | 93 | 0.590 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-1.held.srp.if1` | 1,021,080 | 10.211 | 20 | 20 | fits | 56,958 | 23 | 0.771 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.0.if0` | 511,515 | 5.115 | 62 | 66 | fits | 66,671 | 203 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.0.if0` | 540,896 | 5.409 | 62 | 66 | fits | 66,671 | 203 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.1.if0` | 1,645,921 | 16.459 | 62 | 66 | fits | 41,220 | 100 | 0.343 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.1.if0` | 2,061,188 | 20.612 | 62 | 66 | fits | 69,210 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.2.if0` | 2,090,496 | 20.905 | 62 | 66 | fits | 69,210 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.2.if0` | 2,258,473 | 22.585 | 62 | 66 | fits | 68,350 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.3.if0` | 2,287,396 | 22.874 | 62 | 66 | fits | 68,350 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.3.if0` | 2,457,176 | 24.572 | 62 | 66 | fits | 68,926 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.4.if0` | 2,486,417 | 24.864 | 62 | 66 | fits | 68,926 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.4.if0` | 2,653,730 | 26.537 | 62 | 66 | fits | 68,131 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.5.if0` | 216,842 | 2.168 | 62 | 66 | fits | 103,765 | 210 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.5.if0` | 248,710 | 2.487 | 62 | 66 | fits | 103,765 | 210 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.6.if0` | 290,767 | 2.908 | 62 | 66 | fits | 70,041 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.6.if0` | 321,971 | 3.220 | 62 | 66 | fits | 70,041 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.7.if0` | 2,682,772 | 26.828 | 62 | 66 | fits | 68,131 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.7.if0` | 2,850,291 | 28.503 | 62 | 66 | fits | 67,365 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.5.8.if0` | 440,055 | 4.401 | 62 | 66 | fits | 102,830 | 210 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.5.8.if0` | 472,316 | 4.723 | 62 | 66 | fits | 102,830 | 210 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.0.if0` | 2,878,474 | 28.785 | 62 | 66 | fits | 67,365 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.0.if0` | 3,044,996 | 30.450 | 62 | 66 | fits | 66,821 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.1.if0` | 3,073,067 | 30.731 | 62 | 66 | fits | 66,821 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.1.if0` | 3,274,030 | 32.740 | 62 | 66 | fits | 66,521 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.2.if0` | 3,302,139 | 33.021 | 62 | 66 | fits | 66,521 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.2.if0` | 3,467,034 | 34.670 | 62 | 66 | fits | 66,147 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.3.if0` | 3,494,896 | 34.949 | 62 | 66 | fits | 66,147 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.3.if0` | 3,658,722 | 36.587 | 62 | 66 | fits | 65,844 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.4.if0` | 3,686,397 | 36.864 | 62 | 66 | fits | 65,844 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.4.if0` | 3,850,181 | 38.502 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.5.if0` | 3,878,241 | 38.782 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.5.if0` | 4,041,440 | 40.414 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.6.if0` | 4,069,415 | 40.694 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.6.if0` | 4,262,411 | 42.624 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.7.if0` | 4,290,496 | 42.905 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.7.if0` | 4,458,221 | 44.582 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-2.notices.f.6.8.if0` | 4,486,109 | 44.861 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.6.8.if0` | 4,647,278 | 46.473 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-2.notices.27.9.0.if0` | 4,674,084 | 46.741 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-2.notices.28.9.0.if0` | 4,858,827 | 48.588 | 62 | 66 | fits | 63,090 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.9.0.if0` | 4,888,588 | 48.886 | 62 | 66 | fits | 63,090 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-2.notices.29.36.0.if0` | 5,048,088 | 50.481 | 62 | 66 | fits | 36,657 | 102 | 0.158 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-2.held.adp.if1` | 664,274 | 6.643 | 20 | 200 | fits | 128,346 | 74 | 0.589 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-2.held.acmp.if0` | 644,006 | 6.440 | 20 | 20 | fits | 128,346 | 74 | 0.589 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-2.held.aecp.if1` | 328,501 | 3.285 | 20 | 24 | fits | 162,913 | 113 | 0.425 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-2.held.maap.if0` | 476,185 | 4.762 | 20 | 50 | fits | 166,955 | 246 | 0.344 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-2.held.srp.if1` | 1,019,712 | 10.197 | 20 | 20 | fits | 57,372 | 23 | 0.773 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.0.if0` | 506,249 | 5.062 | 62 | 66 | fits | 66,665 | 203 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.0.if0` | 535,630 | 5.356 | 62 | 66 | fits | 66,665 | 203 | 0.070 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.1.if0` | 1,640,719 | 16.407 | 62 | 66 | fits | 41,053 | 100 | 0.339 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.1.if0` | 1,963,157 | 19.632 | 62 | 66 | fits | 69,150 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.2.if0` | 1,992,465 | 19.925 | 62 | 66 | fits | 69,150 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.2.if0` | 2,160,505 | 21.605 | 62 | 66 | fits | 68,344 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.3.if0` | 2,189,428 | 21.894 | 62 | 66 | fits | 68,344 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.3.if0` | 2,358,485 | 23.585 | 62 | 66 | fits | 68,984 | 201 | 0.155 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.4.if0` | 252,692 | 2.527 | 62 | 66 | fits | 70,960 | 203 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.4.if0` | 283,219 | 2.832 | 62 | 66 | fits | 70,960 | 203 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.5.if0` | 2,387,855 | 23.879 | 62 | 66 | fits | 68,984 | 201 | 0.155 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.5.if0` | 2,555,235 | 25.552 | 62 | 66 | fits | 68,063 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.6.if0` | 2,584,136 | 25.841 | 62 | 66 | fits | 68,063 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.6.if0` | 2,781,453 | 27.815 | 62 | 66 | fits | 66,783 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.7.if0` | 178,517 | 1.785 | 62 | 66 | fits | 104,389 | 212 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.7.if0` | 210,912 | 2.109 | 62 | 66 | fits | 104,389 | 212 | 0.200 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.5.8.if0` | 434,773 | 4.348 | 62 | 66 | fits | 102,914 | 210 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.5.8.if0` | 467,178 | 4.672 | 62 | 66 | fits | 102,914 | 210 | 0.194 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.0.if0` | 2,809,571 | 28.096 | 62 | 66 | fits | 66,783 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.0.if0` | 2,975,669 | 29.757 | 62 | 66 | fits | 66,815 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.1.if0` | 3,003,740 | 30.037 | 62 | 66 | fits | 66,815 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.1.if0` | 3,169,242 | 31.692 | 62 | 66 | fits | 66,301 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.2.if0` | 3,197,228 | 31.972 | 62 | 66 | fits | 66,301 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.2.if0` | 3,367,130 | 33.671 | 62 | 66 | fits | 66,244 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.3.if0` | 3,395,041 | 33.950 | 62 | 66 | fits | 66,244 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.3.if0` | 3,559,346 | 35.593 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.4.if0` | 3,587,021 | 35.870 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.4.if0` | 3,780,299 | 37.803 | 62 | 66 | fits | 66,283 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.5.if0` | 3,808,280 | 38.083 | 62 | 66 | fits | 66,283 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.5.if0` | 3,971,590 | 39.716 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.6.if0` | 3,999,565 | 39.996 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.6.if0` | 4,162,787 | 41.628 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.7.if0` | 4,190,872 | 41.909 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.7.if0` | 4,358,220 | 43.582 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-3.notices.f.6.8.if0` | 4,386,108 | 43.861 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.6.8.if0` | 4,576,757 | 45.768 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-3.notices.27.9.0.if0` | 4,603,563 | 46.036 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-3.notices.28.9.0.if0` | 4,759,234 | 47.592 | 62 | 66 | fits | 63,090 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.9.0.if0` | 4,788,995 | 47.890 | 62 | 66 | fits | 63,090 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-3.notices.29.36.0.if0` | 4,977,384 | 49.774 | 62 | 66 | fits | 36,657 | 102 | 0.158 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-3.held.adp.if1` | 625,890 | 6.259 | 20 | 200 | fits | 127,450 | 110 | 0.575 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-3.held.acmp.if0` | 605,622 | 6.056 | 20 | 20 | fits | 127,450 | 110 | 0.575 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-3.held.aecp.if1` | 457,968 | 4.580 | 20 | 24 | fits | 156,185 | 105 | 0.413 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-3.held.maap.if0` | 566,147 | 5.661 | 20 | 50 | fits | 127,450 | 110 | 0.575 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-3.held.srp.if1` | 1,001,837 | 10.018 | 20 | 20 | fits | 75,343 | 31 | 0.685 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.0.if0` | 1,656,028 | 16.560 | 62 | 66 | fits | 40,946 | 100 | 0.345 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.0.if0` | 2,071,336 | 20.713 | 62 | 66 | fits | 69,201 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.1.if0` | 2,100,501 | 21.005 | 62 | 66 | fits | 69,201 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.1.if0` | 2,268,642 | 22.686 | 62 | 66 | fits | 68,516 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.2.if0` | 2,297,794 | 22.978 | 62 | 66 | fits | 68,516 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.2.if0` | 2,467,542 | 24.675 | 62 | 66 | fits | 69,354 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.3.if0` | 518,718 | 5.187 | 62 | 66 | fits | 68,126 | 203 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.3.if0` | 549,238 | 5.492 | 62 | 66 | fits | 68,126 | 203 | 0.072 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.4.if0` | 2,497,152 | 24.972 | 62 | 66 | fits | 69,354 | 201 | 0.157 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.4.if0` | 2,664,724 | 26.647 | 62 | 66 | fits | 68,591 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.5.if0` | 178,521 | 1.785 | 62 | 66 | fits | 103,359 | 212 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.5.if0` | 210,389 | 2.104 | 62 | 66 | fits | 103,359 | 212 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.6.if0` | 2,693,930 | 26.939 | 62 | 66 | fits | 68,591 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.6.if0` | 2,861,059 | 28.611 | 62 | 66 | fits | 66,927 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.7.if0` | 302,832 | 3.028 | 62 | 66 | fits | 75,356 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.7.if0` | 334,856 | 3.349 | 62 | 66 | fits | 75,356 | 201 | 0.149 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.5.8.if0` | 446,541 | 4.465 | 62 | 66 | fits | 102,643 | 210 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.5.8.if0` | 478,914 | 4.789 | 62 | 66 | fits | 102,643 | 210 | 0.189 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.0.if0` | 2,889,177 | 28.892 | 62 | 66 | fits | 66,927 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.0.if0` | 3,055,576 | 30.556 | 62 | 66 | fits | 66,815 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.1.if0` | 3,083,647 | 30.836 | 62 | 66 | fits | 66,815 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.1.if0` | 3,278,961 | 32.790 | 62 | 66 | fits | 66,301 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.2.if0` | 3,306,947 | 33.069 | 62 | 66 | fits | 66,301 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.2.if0` | 3,477,262 | 34.773 | 62 | 66 | fits | 66,244 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.3.if0` | 3,505,173 | 35.052 | 62 | 66 | fits | 66,244 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.3.if0` | 3,669,241 | 36.692 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.4.if0` | 3,696,916 | 36.969 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.4.if0` | 3,860,487 | 38.605 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.5.if0` | 3,888,547 | 38.885 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.5.if0` | 4,081,830 | 40.818 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.6.if0` | 4,109,805 | 41.098 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.6.if0` | 4,272,702 | 42.727 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.7.if0` | 4,300,787 | 43.008 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.7.if0` | 4,468,505 | 44.685 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-4.notices.f.6.8.if0` | 4,496,393 | 44.964 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.6.8.if0` | 4,657,789 | 46.578 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-4.notices.27.9.0.if0` | 4,684,595 | 46.846 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-4.notices.28.9.0.if0` | 4,869,111 | 48.691 | 62 | 66 | fits | 63,090 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.9.0.if0` | 4,898,872 | 48.989 | 62 | 66 | fits | 63,090 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-4.notices.29.36.0.if0` | 5,058,493 | 50.585 | 62 | 66 | fits | 36,579 | 102 | 0.155 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-4.held.adp.if1` | 661,145 | 6.611 | 20 | 200 | fits | 136,635 | 93 | 0.590 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-4.held.acmp.if0` | 640,877 | 6.409 | 20 | 20 | fits | 136,635 | 93 | 0.590 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-4.held.aecp.if1` | 323,400 | 3.234 | 20 | 24 | fits | 162,854 | 113 | 0.425 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-4.held.maap.if0` | 601,402 | 6.014 | 20 | 50 | fits | 136,635 | 93 | 0.590 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-4.held.srp.if1` | 1,017,014 | 10.170 | 20 | 20 | fits | 57,360 | 23 | 0.773 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.0.if0` | 1,779,780 | 17.798 | 62 | 66 | fits | 40,574 | 100 | 0.343 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.0.if0` | 2,132,526 | 21.325 | 62 | 66 | fits | 69,033 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.1.if0` | 2,161,670 | 21.617 | 62 | 66 | fits | 69,033 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.1.if0` | 2,329,423 | 23.294 | 62 | 66 | fits | 68,277 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.2.if0` | 217,044 | 2.170 | 62 | 66 | fits | 70,532 | 203 | 0.114 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.2.if0` | 247,782 | 2.478 | 62 | 66 | fits | 70,532 | 203 | 0.114 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.3.if0` | 487,533 | 4.875 | 62 | 66 | fits | 68,686 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.3.if0` | 518,169 | 5.182 | 62 | 66 | fits | 68,686 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.4.if0` | 395,575 | 3.956 | 62 | 66 | fits | 122,049 | 210 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.4.if0` | 426,395 | 4.264 | 62 | 66 | fits | 122,049 | 210 | 0.206 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.5.if0` | 628,361 | 6.284 | 62 | 66 | fits | 98,088 | 212 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.5.if0` | 659,126 | 6.591 | 62 | 66 | fits | 98,088 | 212 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.6.if0` | 696,850 | 6.968 | 62 | 66 | fits | 67,147 | 201 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.6.if0` | 727,138 | 7.271 | 62 | 66 | fits | 67,147 | 201 | 0.075 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.7.if0` | 2,358,603 | 23.586 | 62 | 66 | fits | 68,277 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.7.if0` | 2,532,685 | 25.327 | 62 | 66 | fits | 68,849 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.5.8.if0` | 2,562,146 | 25.621 | 62 | 66 | fits | 68,849 | 201 | 0.152 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.5.8.if0` | 2,729,524 | 27.295 | 62 | 66 | fits | 66,963 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.0.if0` | 2,757,434 | 27.574 | 62 | 66 | fits | 66,963 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.0.if0` | 2,923,834 | 29.238 | 62 | 66 | fits | 66,646 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.1.if0` | 2,951,831 | 29.518 | 62 | 66 | fits | 66,646 | 201 | 0.138 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.1.if0` | 3,117,207 | 31.172 | 62 | 66 | fits | 66,307 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.2.if0` | 3,145,193 | 31.452 | 62 | 66 | fits | 66,307 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.2.if0` | 3,339,886 | 33.399 | 62 | 66 | fits | 66,104 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.3.if0` | 3,367,748 | 33.677 | 62 | 66 | fits | 66,104 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.3.if0` | 3,533,308 | 35.333 | 62 | 66 | fits | 66,495 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.4.if0` | 3,561,218 | 35.612 | 62 | 66 | fits | 66,495 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.4.if0` | 3,724,563 | 37.246 | 62 | 66 | fits | 66,405 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.5.if0` | 3,752,623 | 37.526 | 62 | 66 | fits | 66,405 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.5.if0` | 3,916,059 | 39.161 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.6.if0` | 3,944,034 | 39.440 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.6.if0` | 4,137,016 | 41.370 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.7.if0` | 4,165,101 | 41.651 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.7.if0` | 4,326,785 | 43.268 | 62 | 66 | fits | 65,481 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.f.6.8.if0` | 4,354,550 | 43.545 | 62 | 66 | fits | 65,481 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.6.8.if0` | 4,521,924 | 45.219 | 62 | 66 | fits | 64,093 | 201 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-5.notices.27.9.0.if0` | 4,548,730 | 45.487 | 62 | 66 | fits | 64,093 | 201 | 0.127 |
| a queued notice, from its port's answer | `notice-burst-5.notices.28.9.0.if0` | 4,733,522 | 47.335 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.9.0.if0` | 4,763,283 | 47.633 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-5.notices.29.36.0.if0` | 4,922,546 | 49.225 | 62 | 66 | fits | 36,657 | 102 | 0.158 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-5.held.adp.if1` | 677,670 | 6.777 | 20 | 200 | fits | 164,711 | 218 | 0.298 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-5.held.acmp.if0` | 782,411 | 7.824 | 20 | 20 | fits | 125,009 | 46 | 0.714 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-5.held.aecp.if1` | 472,487 | 4.725 | 20 | 24 | fits | 195,306 | 172 | 0.421 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-5.held.maap.if0` | 617,927 | 6.179 | 20 | 50 | fits | 164,711 | 218 | 0.298 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-5.held.srp.if1` | 1,082,088 | 10.821 | 20 | 20 | fits | 102,340 | 43 | 0.611 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.0.if0` | 1,668,628 | 16.686 | 62 | 66 | fits | 40,901 | 100 | 0.343 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.0.if0` | 2,083,857 | 20.839 | 62 | 66 | fits | 69,071 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.1.if0` | 260,524 | 2.605 | 62 | 66 | fits | 69,590 | 203 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.1.if0` | 290,369 | 2.904 | 62 | 66 | fits | 69,590 | 203 | 0.077 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.2.if0` | 440,053 | 4.401 | 62 | 66 | fits | 120,748 | 210 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.2.if0` | 470,712 | 4.707 | 62 | 66 | fits | 120,748 | 210 | 0.205 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.3.if0` | 2,112,957 | 21.130 | 62 | 66 | fits | 69,071 | 201 | 0.158 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.3.if0` | 2,281,006 | 22.810 | 62 | 66 | fits | 68,417 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.4.if0` | 532,133 | 5.321 | 62 | 66 | fits | 67,985 | 203 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.4.if0` | 562,322 | 5.623 | 62 | 66 | fits | 67,985 | 203 | 0.079 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.5.if0` | 2,310,067 | 23.101 | 62 | 66 | fits | 68,417 | 201 | 0.141 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.5.if0` | 2,484,229 | 24.842 | 62 | 66 | fits | 68,313 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.6.if0` | 2,513,253 | 25.133 | 62 | 66 | fits | 68,313 | 201 | 0.150 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.6.if0` | 2,680,428 | 26.804 | 62 | 66 | fits | 67,518 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.7.if0` | 2,709,165 | 27.092 | 62 | 66 | fits | 67,518 | 201 | 0.143 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.7.if0` | 2,876,286 | 28.763 | 62 | 66 | fits | 68,308 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.5.8.if0` | 2,905,568 | 29.056 | 62 | 66 | fits | 68,308 | 201 | 0.144 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.5.8.if0` | 3,072,371 | 30.724 | 62 | 66 | fits | 66,970 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.0.if0` | 186,433 | 1.864 | 62 | 66 | fits | 104,622 | 212 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.0.if0` | 219,379 | 2.194 | 62 | 66 | fits | 104,622 | 212 | 0.193 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.1.if0` | 3,100,524 | 31.005 | 62 | 66 | fits | 66,970 | 201 | 0.137 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.1.if0` | 3,265,862 | 32.659 | 62 | 66 | fits | 66,227 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.2.if0` | 3,293,774 | 32.938 | 62 | 66 | fits | 66,227 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.2.if0` | 3,460,213 | 34.602 | 62 | 66 | fits | 66,658 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.3.if0` | 3,488,213 | 34.882 | 62 | 66 | fits | 66,658 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.3.if0` | 3,682,104 | 36.821 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.4.if0` | 3,709,779 | 37.098 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.4.if0` | 3,873,248 | 38.732 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.5.if0` | 3,901,308 | 39.013 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.5.if0` | 4,064,734 | 40.647 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.6.if0` | 4,092,709 | 40.927 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.6.if0` | 4,285,478 | 42.855 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.7.if0` | 4,313,563 | 43.136 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.7.if0` | 4,481,073 | 44.811 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.f.6.8.if0` | 4,508,961 | 45.090 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.6.8.if0` | 4,670,357 | 46.704 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-6.notices.27.9.0.if0` | 4,697,163 | 46.972 | 62 | 66 | fits | 63,822 | 201 | 0.126 |
| a queued notice, from its port's answer | `notice-burst-6.notices.28.9.0.if0` | 4,881,742 | 48.817 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.9.0.if0` | 4,911,503 | 49.115 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-6.notices.29.36.0.if0` | 5,071,124 | 50.711 | 62 | 66 | fits | 36,579 | 102 | 0.155 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-6.held.adp.if1` | 669,305 | 6.693 | 20 | 200 | fits | 136,578 | 93 | 0.590 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-6.held.acmp.if0` | 649,037 | 6.490 | 20 | 20 | fits | 136,578 | 93 | 0.590 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-6.held.aecp.if1` | 331,410 | 3.314 | 20 | 24 | fits | 163,039 | 113 | 0.425 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-6.held.maap.if0` | 609,562 | 6.096 | 20 | 50 | fits | 136,578 | 93 | 0.590 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-6.held.srp.if1` | 1,024,531 | 10.245 | 20 | 20 | fits | 57,175 | 23 | 0.771 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.0.if0` | 230,435 | 2.304 | 62 | 66 | fits | 69,287 | 203 | 0.114 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.0.if0` | 260,265 | 2.603 | 62 | 66 | fits | 69,287 | 203 | 0.114 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.1.if0` | 407,107 | 4.071 | 62 | 66 | fits | 120,371 | 210 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.1.if0` | 437,245 | 4.372 | 62 | 66 | fits | 120,371 | 210 | 0.201 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.2.if0` | 497,985 | 4.980 | 62 | 66 | fits | 67,552 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.2.if0` | 527,597 | 5.276 | 62 | 66 | fits | 67,552 | 203 | 0.078 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.3.if0` | 636,946 | 6.369 | 62 | 66 | fits | 96,309 | 212 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.3.if0` | 666,962 | 6.670 | 62 | 66 | fits | 96,309 | 212 | 0.184 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.4.if0` | 704,184 | 7.042 | 62 | 66 | fits | 65,351 | 201 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.4.if0` | 733,564 | 7.336 | 62 | 66 | fits | 65,351 | 201 | 0.074 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.5.if0` | 1,825,265 | 18.253 | 62 | 66 | fits | 40,277 | 100 | 0.341 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.5.if0` | 2,238,392 | 22.384 | 62 | 66 | fits | 68,598 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.6.if0` | 2,267,405 | 22.674 | 62 | 66 | fits | 68,598 | 201 | 0.160 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.6.if0` | 2,440,913 | 24.409 | 62 | 66 | fits | 67,847 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.7.if0` | 2,469,773 | 24.698 | 62 | 66 | fits | 67,847 | 201 | 0.147 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.7.if0` | 2,637,336 | 26.373 | 62 | 66 | fits | 68,430 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.5.8.if0` | 2,666,618 | 26.666 | 62 | 66 | fits | 68,430 | 201 | 0.146 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.5.8.if0` | 2,833,812 | 28.338 | 62 | 66 | fits | 66,868 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.0.if0` | 2,861,713 | 28.617 | 62 | 66 | fits | 66,868 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.0.if0` | 3,027,968 | 30.280 | 62 | 66 | fits | 66,603 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.1.if0` | 3,055,965 | 30.560 | 62 | 66 | fits | 66,603 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.1.if0` | 3,251,315 | 32.513 | 62 | 66 | fits | 66,307 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.2.if0` | 3,279,301 | 32.793 | 62 | 66 | fits | 66,307 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.2.if0` | 3,446,031 | 34.460 | 62 | 66 | fits | 66,732 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.3.if0` | 3,474,105 | 34.741 | 62 | 66 | fits | 66,732 | 201 | 0.148 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.3.if0` | 3,637,715 | 36.377 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.4.if0` | 3,665,390 | 36.654 | 62 | 66 | fits | 65,887 | 201 | 0.134 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.4.if0` | 3,829,174 | 38.292 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.5.if0` | 3,857,234 | 38.572 | 62 | 66 | fits | 66,362 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.5.if0` | 4,050,290 | 40.503 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.6.if0` | 4,078,265 | 40.783 | 62 | 66 | fits | 66,204 | 201 | 0.133 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.6.if0` | 4,241,361 | 42.414 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.7.if0` | 4,269,446 | 42.694 | 62 | 66 | fits | 66,306 | 201 | 0.136 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.7.if0` | 4,436,804 | 44.368 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-7.notices.f.6.8.if0` | 4,464,692 | 44.647 | 62 | 66 | fits | 65,774 | 201 | 0.139 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.6.8.if0` | 4,626,074 | 46.261 | 62 | 66 | fits | 63,743 | 201 | 0.124 |
| a queued notice, from its port's answer | `notice-burst-7.notices.27.9.0.if0` | 4,652,880 | 46.529 | 62 | 66 | fits | 63,743 | 201 | 0.124 |
| a queued notice, from its port's answer | `notice-burst-7.notices.28.9.0.if0` | 4,837,394 | 48.374 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.9.0.if0` | 4,867,155 | 48.672 | 62 | 66 | fits | 63,153 | 200 | 0.115 |
| a queued notice, from its port's answer | `notice-burst-7.notices.29.36.0.if0` | 5,026,868 | 50.269 | 62 | 66 | fits | 36,657 | 102 | 0.158 |
| ADP record, every channel at its refill rate, the longest | `notice-burst-7.held.adp.if1` | 765,348 | 7.653 | 20 | 200 | fits | 126,996 | 71 | 0.605 |
| ACMP record, every channel at its refill rate, the longest | `notice-burst-7.held.acmp.if0` | 745,080 | 7.451 | 20 | 20 | fits | 126,996 | 71 | 0.605 |
| AECP record, every channel at its refill rate, the longest | `notice-burst-7.held.aecp.if1` | 431,155 | 4.312 | 20 | 24 | fits | 159,259 | 108 | 0.416 |
| MAAP record, every channel at its refill rate, the longest | `notice-burst-7.held.maap.if0` | 578,609 | 5.786 | 20 | 50 | fits | 166,725 | 244 | 0.348 |
| SRP record, every channel at its refill rate, the longest | `notice-burst-7.held.srp.if1` | 1,116,750 | 11.168 | 20 | 20 | fits | 45,492 | 19 | 0.826 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

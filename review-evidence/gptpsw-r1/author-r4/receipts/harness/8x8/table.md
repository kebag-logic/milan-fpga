### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 20 paths and 7 of 59 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.563 (7.447) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.763 (6.545) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.153 (0.628) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.743 (2.309) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.828 (64.063) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.874 (65.112) | MISS ceiling | 11 acmp | 4 | 4 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-master) | 0.343 (0.787) | fits | 0 gptp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.532 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.513 | MISS ceiling | 11 acmp | 4 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.587 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.480 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.275 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.656 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 62.105 | MISS ceiling | 15 aecp | 4 | 1 |
| GPTP record released under the composed load, first | 0 | `backlog.service.gptp.first.if0` (backlog) | 4.544 | fits | 0 gptp | 4 | 0 |
| GPTP record released under the composed load, last | 1 | `backlog-adp.service.gptp.last.if1` (backlog-adp) | 7.967 | fits | 13 gptp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.569 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.529 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 8.008 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 13.316 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 10.777 | 10 | 163,656 (1.637) | yes | - |
| backlog-adp | 0 | 14.054 | 13 | 166,120 (1.661) | yes | - |
| backlog-adp-refill | 0 | 41.082 | 32 | 166,120 (1.661) | yes | - |
| backlog-owed | 0 | 65.786 | 25 | 164,080 (1.641) | yes | - |

Composed maximum over the 4 backlog windows: 166,120 CPU cycles (1.661 ms), backlog-adp.
Over the windows that released their whole load only: 166,120 (1.661 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 965 | 0 | 163,656 (1.637) | fits |
| backlog-adp | 1005 | 0 | 166,120 (1.661) | fits |
| backlog-adp-refill | 1024 | 0 | 166,120 (1.661) | fits |
| backlog-owed | 1000 | 0 | 164,080 (1.641) | fits |
| gptp-slave | 615 | 0 | 124,848 (1.248) | fits |
| gptp-master | 604 | 0 | 113,077 (1.131) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 266 | 27,415 (0.274) | 3,797 (0.038) |
| backlog-adp | 271 | 27,415 (0.274) | 3,797 (0.038) |
| backlog-adp-refill | 273 | 27,415 (0.274) | 3,797 (0.038) |
| backlog-owed | 277 | 28,037 (0.280) | 3,922 (0.039) |
| gptp-slave | 165 | 27,415 (0.274) | 3,797 (0.038) |
| gptp-master | 165 | 27,415 (0.274) | 3,797 (0.038) |

Longest pass that carries a step: 28,037 CPU cycles (0.280 ms), backlog-owed; longest step: 3,922 (0.039 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 174,298 | 1.743 | 20 | 200 | fits | 67,200 | 81 | 0.581 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 656,336 | 6.563 | 20 | 20 | fits | 116,338 | 88 | 0.670 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 458,687 | 4.587 | 20 | 200 | fits | 160,245 | 166 | 0.434 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 627,544 | 6.275 | 20 | 200 | fits | 158,230 | 134 | 0.413 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 453,217 | 4.532 | 20 | 20 | fits | 160,245 | 166 | 0.434 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 738,192 | 7.382 | 20 | 20 | fits | 116,338 | 88 | 0.670 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 162,765 | 1.628 | 20 | 24 | fits | 163,656 | 183 | 0.315 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 296,770 | 2.968 | 20 | 24 | fits | 67,795 | 29 | 0.689 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 456,949 | 4.569 | 20 | 50 | fits | 160,245 | 166 | 0.434 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 626,026 | 6.260 | 20 | 50 | fits | 158,230 | 134 | 0.413 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 742,298 | 7.423 | 20 | 20 | fits | 116,338 | 88 | 0.670 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,004,574 | 10.046 | 20 | 20 | fits | 48,120 | 22 | 0.745 |
| GPTP record released under the composed load, first | `backlog.service.gptp.first.if0` | 454,359 | 4.544 | 10 | 10 | fits | 160,245 | 166 | 0.434 |
| GPTP record released under the composed load, last | `backlog.service.gptp.last.if1` | 739,104 | 7.391 | 10 | 10 | fits | 116,338 | 88 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 576,305 | 5.763 | 20 | 20 | fits | 165,083 | 165 | 0.479 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 317,448 | 3.174 | 20 | 200 | fits | 158,546 | 181 | 0.458 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 648,035 | 6.480 | 20 | 200 | fits | 165,083 | 165 | 0.479 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 319,520 | 3.195 | 20 | 20 | fits | 158,546 | 181 | 0.458 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 797,837 | 7.978 | 20 | 20 | fits | 137,009 | 91 | 0.634 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 155,064 | 1.551 | 20 | 24 | fits | 155,250 | 182 | 0.296 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 322,170 | 3.222 | 20 | 24 | fits | 158,546 | 181 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 322,104 | 3.221 | 20 | 50 | fits | 158,546 | 181 | 0.458 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 652,911 | 6.529 | 20 | 50 | fits | 165,083 | 165 | 0.479 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 800,795 | 8.008 | 20 | 20 | fits | 137,009 | 91 | 0.634 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,331,614 | 13.316 | 20 | 20 | fits | 48,334 | 18 | 0.802 |
| GPTP record released under the composed load, first | `backlog-adp.service.gptp.first.if0` | 318,602 | 3.186 | 10 | 10 | fits | 158,546 | 181 | 0.458 |
| GPTP record released under the composed load, last | `backlog-adp.service.gptp.last.if1` | 796,689 | 7.967 | 10 | 10 | fits | 137,009 | 91 | 0.634 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,286 | 0.153 | 20 | 20 | fits | 36,185 | 21 | 0.778 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 317,448 | 3.174 | 20 | 200 | fits | 158,546 | 181 | 0.458 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 40,595 | 0.406 | 20 | 200 | fits | 36,185 | 21 | 0.778 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 319,520 | 3.195 | 20 | 20 | fits | 158,546 | 181 | 0.458 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 785,080 | 7.851 | 20 | 20 | fits | 129,087 | 85 | 0.647 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 155,064 | 1.551 | 20 | 24 | fits | 155,250 | 182 | 0.296 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 322,170 | 3.222 | 20 | 24 | fits | 158,546 | 181 | 0.458 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 322,104 | 3.221 | 20 | 50 | fits | 158,546 | 181 | 0.458 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 648,245 | 6.482 | 20 | 50 | fits | 160,417 | 163 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 788,038 | 7.880 | 20 | 20 | fits | 129,087 | 85 | 0.647 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,321,063 | 13.211 | 20 | 20 | fits | 48,767 | 18 | 0.807 |
| GPTP record released under the composed load, first | `backlog-adp-refill.service.gptp.first.if0` | 318,602 | 3.186 | 10 | 10 | fits | 158,546 | 181 | 0.458 |
| GPTP record released under the composed load, last | `backlog-adp-refill.service.gptp.last.if1` | 783,932 | 7.839 | 10 | 10 | fits | 129,087 | 85 | 0.647 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,382,750 | 63.828 | 20 | 20 | MISS ceiling | 26,366 | 15 | 0.463 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,408,986 | 64.090 | 20 | 20 | MISS ceiling | 26,312 | 15 | 0.439 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,435,140 | 64.351 | 20 | 20 | MISS ceiling | 26,211 | 15 | 0.455 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,461,319 | 64.613 | 20 | 20 | MISS ceiling | 26,255 | 15 | 0.455 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,487,376 | 64.874 | 20 | 20 | MISS ceiling | 26,120 | 15 | 0.472 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 166,266 | 1.663 | 20 | 200 | fits | 164,080 | 193 | 0.435 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 486,730 | 4.867 | 20 | 200 | fits | 161,707 | 116 | 0.437 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 160,796 | 1.608 | 20 | 20 | fits | 164,080 | 193 | 0.435 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,251,335 | 62.513 | 20 | 20 | MISS ceiling | 45,488 | 46 | 0.638 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 165,584 | 1.656 | 20 | 24 | fits | 164,080 | 193 | 0.435 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,210,481 | 62.105 | 20 | 24 | MISS ceiling | 156,438 | 165 | 0.375 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 164,528 | 1.645 | 20 | 50 | fits | 164,080 | 193 | 0.435 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 485,212 | 4.852 | 20 | 50 | fits | 161,707 | 116 | 0.437 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 606,794 | 6.068 | 20 | 20 | fits | 121,648 | 39 | 0.791 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 997,725 | 9.977 | 20 | 20 | fits | 47,945 | 18 | 0.799 |
| GPTP record released under the composed load, first | `backlog-owed.service.gptp.first.if0` | 161,938 | 1.619 | 10 | 10 | fits | 164,080 | 193 | 0.435 |
| GPTP record released under the composed load, last | `backlog-owed.service.gptp.last.if1` | 603,600 | 6.036 | 10 | 10 | fits | 121,648 | 39 | 0.791 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 26,576 | 0.266 | 10 | 10 | fits | 37,588 | 18 | 0.755 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 34,322 | 0.343 | 10 | 10 | fits | 37,765 | 18 | 0.750 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

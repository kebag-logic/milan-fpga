### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 20 paths and 7 of 59 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.897 (6.215) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.656 (6.437) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.173 (0.648) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.739 (2.281) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.910 (64.331) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.957 (65.377) | MISS ceiling | 11 acmp | 4 | 4 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | 0 | `gptp.pdelay_resp.if0` (gptp-slave) | 0.292 (0.725) | fits | 0 gptp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.478 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.587 | MISS ceiling | 11 acmp | 4 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.533 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.372 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.206 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.835 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 61.819 | MISS ceiling | 15 aecp | 4 | 1 |
| GPTP record released under the composed load, first | 0 | `backlog.service.gptp.first.if0` (backlog) | 4.489 | fits | 0 gptp | 4 | 0 |
| GPTP record released under the composed load, last | 1 | `backlog-adp.service.gptp.last.if1` (backlog-adp) | 7.750 | fits | 13 gptp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.515 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.420 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 9.008 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 13.249 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 10.705 | 10 | 162,896 (1.629) | yes | - |
| backlog-adp | 0 | 13.999 | 13 | 165,216 (1.652) | yes | - |
| backlog-adp-refill | 0 | 41.096 | 31 | 160,964 (1.610) | yes | - |
| backlog-owed | 0 | 65.873 | 26 | 165,729 (1.657) | yes | - |

Composed maximum over the 4 backlog windows: 165,729 CPU cycles (1.657 ms), backlog-owed.
Over the windows that released their whole load only: 165,729 (1.657 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 966 | 0 | 162,896 (1.629) | fits |
| backlog-adp | 1005 | 0 | 165,216 (1.652) | fits |
| backlog-adp-refill | 1023 | 0 | 160,964 (1.610) | fits |
| backlog-owed | 1002 | 0 | 165,729 (1.657) | fits |
| gptp-slave | 616 | 0 | 126,244 (1.262) | fits |
| gptp-master | 605 | 0 | 114,394 (1.144) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 266 | 27,617 (0.276) | 3,769 (0.038) |
| backlog-adp | 271 | 27,617 (0.276) | 3,746 (0.037) |
| backlog-adp-refill | 273 | 27,617 (0.276) | 3,746 (0.037) |
| backlog-owed | 277 | 27,928 (0.279) | 3,964 (0.040) |
| gptp-slave | 165 | 27,617 (0.276) | 3,811 (0.038) |
| gptp-master | 165 | 27,617 (0.276) | 3,811 (0.038) |

Longest pass that carries a step: 27,928 CPU cycles (0.279 ms), backlog-owed; longest step: 3,964 (0.040 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 173,927 | 1.739 | 20 | 200 | fits | 65,254 | 81 | 0.558 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 589,671 | 5.897 | 20 | 20 | fits | 157,149 | 147 | 0.455 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 453,266 | 4.533 | 20 | 200 | fits | 159,653 | 151 | 0.449 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 620,628 | 6.206 | 20 | 200 | fits | 157,149 | 147 | 0.455 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 447,796 | 4.478 | 20 | 20 | fits | 159,653 | 151 | 0.449 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 614,938 | 6.149 | 20 | 20 | fits | 157,149 | 147 | 0.455 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 162,005 | 1.620 | 20 | 24 | fits | 162,896 | 183 | 0.306 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 291,941 | 2.919 | 20 | 24 | fits | 65,672 | 29 | 0.659 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 451,528 | 4.515 | 20 | 50 | fits | 159,653 | 151 | 0.449 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 619,110 | 6.191 | 20 | 50 | fits | 157,149 | 147 | 0.455 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 734,945 | 7.349 | 20 | 20 | fits | 115,901 | 82 | 0.651 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 996,385 | 9.964 | 20 | 20 | fits | 49,270 | 26 | 0.687 |
| GPTP record released under the composed load, first | `backlog.service.gptp.first.if0` | 448,938 | 4.489 | 10 | 10 | fits | 159,653 | 151 | 0.449 |
| GPTP record released under the composed load, last | `backlog.service.gptp.last.if1` | 731,751 | 7.318 | 10 | 10 | fits | 115,901 | 82 | 0.651 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 565,604 | 5.656 | 20 | 20 | fits | 165,216 | 154 | 0.515 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 318,055 | 3.181 | 20 | 200 | fits | 159,501 | 181 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 637,165 | 6.372 | 20 | 200 | fits | 165,216 | 154 | 0.515 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 320,127 | 3.201 | 20 | 20 | fits | 159,501 | 181 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 776,154 | 7.762 | 20 | 20 | fits | 126,551 | 103 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 154,888 | 1.549 | 20 | 24 | fits | 155,074 | 182 | 0.291 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 322,777 | 3.228 | 20 | 24 | fits | 159,501 | 181 | 0.467 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 322,711 | 3.227 | 20 | 50 | fits | 159,501 | 181 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 642,041 | 6.420 | 20 | 50 | fits | 165,216 | 154 | 0.515 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 900,814 | 9.008 | 20 | 20 | fits | 121,702 | 61 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,324,887 | 13.249 | 20 | 20 | fits | 69,872 | 29 | 0.796 |
| GPTP record released under the composed load, first | `backlog-adp.service.gptp.first.if0` | 319,209 | 3.192 | 10 | 10 | fits | 159,501 | 181 | 0.467 |
| GPTP record released under the composed load, last | `backlog-adp.service.gptp.last.if1` | 775,006 | 7.750 | 10 | 10 | fits | 126,551 | 103 | 0.504 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 17,259 | 0.173 | 20 | 20 | fits | 35,786 | 21 | 0.769 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 318,055 | 3.181 | 20 | 200 | fits | 159,501 | 181 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 42,218 | 0.422 | 20 | 200 | fits | 35,786 | 21 | 0.769 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 320,127 | 3.201 | 20 | 20 | fits | 159,501 | 181 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 764,044 | 7.640 | 20 | 20 | fits | 118,829 | 97 | 0.508 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 154,888 | 1.549 | 20 | 24 | fits | 155,074 | 182 | 0.291 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 322,777 | 3.228 | 20 | 24 | fits | 159,501 | 181 | 0.467 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 322,711 | 3.227 | 20 | 50 | fits | 159,501 | 181 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 637,789 | 6.378 | 20 | 50 | fits | 160,964 | 152 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 888,645 | 8.886 | 20 | 20 | fits | 121,643 | 61 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,313,397 | 13.134 | 20 | 20 | fits | 58,400 | 25 | 0.809 |
| GPTP record released under the composed load, first | `backlog-adp-refill.service.gptp.first.if0` | 319,209 | 3.192 | 10 | 10 | fits | 159,501 | 181 | 0.467 |
| GPTP record released under the composed load, last | `backlog-adp-refill.service.gptp.last.if1` | 762,896 | 7.629 | 10 | 10 | fits | 118,829 | 97 | 0.508 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,391,048 | 63.910 | 20 | 20 | MISS ceiling | 26,390 | 15 | 0.456 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,417,273 | 64.173 | 20 | 20 | MISS ceiling | 26,301 | 15 | 0.441 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,443,417 | 64.434 | 20 | 20 | MISS ceiling | 26,201 | 15 | 0.456 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,469,623 | 64.696 | 20 | 20 | MISS ceiling | 26,282 | 15 | 0.456 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,495,703 | 64.957 | 20 | 20 | MISS ceiling | 26,143 | 15 | 0.464 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 184,183 | 1.842 | 20 | 200 | fits | 165,729 | 193 | 0.454 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 496,211 | 4.962 | 20 | 200 | fits | 157,251 | 111 | 0.481 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 178,713 | 1.787 | 20 | 20 | fits | 165,729 | 193 | 0.454 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,258,682 | 62.587 | 20 | 20 | MISS ceiling | 37,100 | 17 | 0.591 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 183,501 | 1.835 | 20 | 24 | fits | 165,729 | 193 | 0.454 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,181,864 | 61.819 | 20 | 24 | MISS ceiling | 155,235 | 166 | 0.358 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 182,445 | 1.824 | 20 | 50 | fits | 165,729 | 193 | 0.454 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 494,693 | 4.947 | 20 | 50 | fits | 157,251 | 111 | 0.481 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 619,794 | 6.198 | 20 | 20 | fits | 125,167 | 44 | 0.754 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,018,705 | 10.187 | 20 | 20 | fits | 36,167 | 14 | 0.823 |
| GPTP record released under the composed load, first | `backlog-owed.service.gptp.first.if0` | 179,855 | 1.799 | 10 | 10 | fits | 165,729 | 193 | 0.454 |
| GPTP record released under the composed load, last | `backlog-owed.service.gptp.last.if1` | 616,600 | 6.166 | 10 | 10 | fits | 125,167 | 44 | 0.754 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 29,195 | 0.292 | 10 | 10 | fits | 37,374 | 18 | 0.755 |
| Pdelay_Req -> Pdelay_Resp (responder turnaround) | `gptp.pdelay_resp.if0` | 29,058 | 0.291 | 10 | 10 | fits | 36,964 | 18 | 0.740 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

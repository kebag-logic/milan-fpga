### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 17 paths and 7 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.595 (5.449) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.580 (4.431) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.268 (0.721) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.649 (2.131) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.314 (63.722) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.415 (64.822) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.250 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.112 | MISS ceiling | 11 acmp | 4 | 1 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.293 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 4.377 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 5.441 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.604 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 61.769 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.276 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 4.414 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 5.635 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 8.901 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 8.168 | 8 | 154,278 (1.543) | yes | - |
| backlog-adp | 0 | 9.579 | 8 | 157,128 (1.571) | yes | - |
| backlog-adp-refill | 0 | 41.133 | 23 | 157,128 (1.571) | yes | - |
| backlog-owed | 0 | 65.274 | 23 | 153,324 (1.533) | yes | - |

Composed maximum over the 4 backlog windows: 157,128 CPU cycles (1.571 ms), backlog-adp.
Over the windows that released their whole load only: 157,128 (1.571 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 296 | 0 | 154,278 (1.543) | fits |
| backlog-adp | 319 | 0 | 157,128 (1.571) | fits |
| backlog-adp-refill | 334 | 0 | 157,128 (1.571) | fits |
| backlog-owed | 317 | 0 | 153,324 (1.533) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 266 | 26,151 (0.262) | 2,525 (0.025) |
| backlog-adp | 271 | 26,151 (0.262) | 2,499 (0.025) |
| backlog-adp-refill | 274 | 26,151 (0.262) | 2,499 (0.025) |
| backlog-owed | 277 | 27,057 (0.271) | 2,497 (0.025) |

Longest pass that carries a step: 27,057 CPU cycles (0.271 ms), backlog-owed; longest step: 2,525 (0.025 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 164,920 | 1.649 | 20 | 200 | fits | 58,779 | 81 | 0.548 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 459,460 | 4.595 | 20 | 20 | fits | 115,368 | 79 | 0.566 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 429,300 | 4.293 | 20 | 200 | fits | 152,181 | 173 | 0.346 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 544,052 | 5.441 | 20 | 200 | fits | 115,368 | 79 | 0.566 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 424,978 | 4.250 | 20 | 20 | fits | 152,181 | 173 | 0.346 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 539,510 | 5.395 | 20 | 20 | fits | 115,368 | 79 | 0.566 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 153,387 | 1.534 | 20 | 24 | fits | 154,278 | 183 | 0.318 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 275,447 | 2.754 | 20 | 24 | fits | 64,271 | 29 | 0.668 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 427,562 | 4.276 | 20 | 50 | fits | 152,181 | 173 | 0.346 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 427,166 | 4.272 | 20 | 50 | fits | 152,181 | 173 | 0.346 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 542,468 | 5.425 | 20 | 20 | fits | 115,368 | 79 | 0.566 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 723,837 | 7.238 | 20 | 20 | fits | 88,881 | 57 | 0.588 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 357,982 | 3.580 | 20 | 20 | fits | 130,337 | 159 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 298,174 | 2.982 | 20 | 200 | fits | 157,128 | 233 | 0.352 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 437,689 | 4.377 | 20 | 200 | fits | 130,337 | 159 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 299,098 | 2.991 | 20 | 20 | fits | 157,128 | 233 | 0.352 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 438,393 | 4.384 | 20 | 20 | fits | 130,337 | 159 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 145,610 | 1.456 | 20 | 24 | fits | 145,796 | 180 | 0.296 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 301,748 | 3.017 | 20 | 24 | fits | 157,128 | 233 | 0.352 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 301,682 | 3.017 | 20 | 50 | fits | 157,128 | 233 | 0.352 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 441,417 | 4.414 | 20 | 50 | fits | 130,337 | 159 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 563,541 | 5.635 | 20 | 20 | fits | 122,190 | 43 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 890,122 | 8.901 | 20 | 20 | fits | 95,719 | 37 | 0.709 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 26,807 | 0.268 | 20 | 20 | fits | 33,914 | 20 | 0.752 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 298,174 | 2.982 | 20 | 200 | fits | 157,128 | 233 | 0.352 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 51,116 | 0.511 | 20 | 200 | fits | 33,914 | 20 | 0.752 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 299,098 | 2.991 | 20 | 20 | fits | 157,128 | 233 | 0.352 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 424,944 | 4.249 | 20 | 20 | fits | 116,888 | 149 | 0.371 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 145,610 | 1.456 | 20 | 24 | fits | 145,796 | 180 | 0.296 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 301,748 | 3.017 | 20 | 24 | fits | 157,128 | 233 | 0.352 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 301,682 | 3.017 | 20 | 50 | fits | 157,128 | 233 | 0.352 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 427,968 | 4.280 | 20 | 50 | fits | 116,888 | 149 | 0.371 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 549,200 | 5.492 | 20 | 20 | fits | 121,298 | 43 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 875,068 | 8.751 | 20 | 20 | fits | 95,487 | 37 | 0.707 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,331,441 | 63.314 | 20 | 20 | MISS ceiling | 26,149 | 14 | 0.620 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,357,425 | 63.574 | 20 | 20 | MISS ceiling | 26,035 | 14 | 0.605 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,390,050 | 63.901 | 20 | 20 | MISS ceiling | 31,252 | 19 | 0.717 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,414,484 | 64.145 | 20 | 20 | MISS ceiling | 27,057 | 14 | 0.614 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,441,466 | 64.415 | 20 | 20 | MISS ceiling | 25,989 | 14 | 0.633 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 161,069 | 1.611 | 20 | 200 | fits | 153,324 | 213 | 0.394 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 280,358 | 2.804 | 20 | 200 | fits | 119,905 | 184 | 0.362 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 156,747 | 1.567 | 20 | 20 | fits | 153,324 | 213 | 0.394 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,211,189 | 62.112 | 20 | 20 | MISS ceiling | 37,817 | 16 | 0.722 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 160,387 | 1.604 | 20 | 24 | fits | 153,324 | 213 | 0.394 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,176,858 | 61.769 | 20 | 24 | MISS ceiling | 133,116 | 117 | 0.357 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 159,331 | 1.593 | 20 | 50 | fits | 153,324 | 213 | 0.394 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 278,840 | 2.788 | 20 | 50 | fits | 119,905 | 184 | 0.362 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 393,453 | 3.935 | 20 | 20 | fits | 114,679 | 37 | 0.775 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 728,907 | 7.289 | 20 | 20 | fits | 106,901 | 41 | 0.709 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

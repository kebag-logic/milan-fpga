### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 29 paths and 0 of 108 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.102 (0.495) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.322 (0.560) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.244 (0.531) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.067 (0.431) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.026 (0.165) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.028 (0.278) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.161 (0.483) | fits | 0 events | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.182 (2.499) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.299 (2.659) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.876 (4.231) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.304 (3.663) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.459 (1.793) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-3.adp_available.if0` (backlog-adp@verify-aged2-3) | 3.767 (4.311) | fits | 7 adp | 8 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-flight.held.acmp.if0` (save-flight) | 2.300 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-flight.held.adp.if0` (save-flight) | 1.574 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 2.821 | fits | 14 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.350 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-flight.held.srp.if0` (save-flight) | 9.089 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-flight.mrpdu.periodic.if0` (save-flight) | 1.908 | fits | 0 srp | 3 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-aged1-3.service.acmp.first.if0` (backlog-adp@program-aged1-3) | 3.146 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged1-3.service.acmp.last.if0` (backlog-adp@program-aged1-3) | 4.343 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-aged1-3.service.adp.first.if0` (backlog-adp@program-aged1-3) | 3.137 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged1-3.service.adp.last.if0` (backlog-adp@program-aged1-3) | 4.336 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-3.service.aecp.first.if0` (backlog-adp@program-3) | 1.617 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@program-aged1-3.service.aecp.last.if0` (backlog-adp@program-aged1-3) | 3.172 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-aged1-3.service.maap.first.if0` (backlog-adp@program-aged1-3) | 3.172 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged1-3.service.maap.last.if0` (backlog-adp@program-aged1-3) | 4.374 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged1-3.service.srp.first.if0` (backlog-adp@program-aged1-3) | 5.222 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-3.service.srp.last.if0` (backlog-adp@blank-aged2-3) | 10.952 | fits | 31 srp | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-3 | 0 | 12.396 | 11 | 152,911 (1.529) | yes | - |
| backlog-adp@verify-3 | 0 | 12.987 | 11 | 152,657 (1.527) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 15.853 | 13 | 151,380 (1.514) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.902 | 11 | 151,466 (1.515) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 12.296 | 10 | 149,626 (1.496) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 12.638 | 13 | 151,595 (1.516) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 14.010 | 13 | 151,369 (1.514) | yes | - |
| backlog-adp@verify-aged1-3 | 1 | 12.871 | 10 | 148,891 (1.489) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-flight | 3148 | 0 | 158,363 (1.584) | fits |
| backlog-adp@program-3 | 493 | 0 | 152,911 (1.529) | fits |
| backlog-adp@verify-3 | 499 | 0 | 152,657 (1.527) | fits |
| backlog-adp@blank-aged2-3 | 767 | 0 | 151,380 (1.514) | fits |
| backlog-adp@blank-aged1-3 | 704 | 0 | 151,466 (1.515) | fits |
| backlog-adp@program-aged2-3 | 792 | 0 | 151,393 (1.514) | fits |
| backlog-adp@program-aged1-3 | 734 | 0 | 151,595 (1.516) | fits |
| backlog-adp@verify-aged2-3 | 811 | 0 | 151,369 (1.514) | fits |
| backlog-adp@verify-aged1-3 | 748 | 0 | 151,480 (1.515) | fits |
| acmp-noresp | 1909 | 0 | 101,504 (1.015) | fits |
| adp-gm | 88 | 0 | 30,398 (0.304) | fits |
| aecp-largest-notice | 107 | 0 | 158,006 (1.580) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-3 | 2 | +6.784 ms, 76,941 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 10.952 (20) | 9.048 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.129 (20) | 9.871 |
| backlog-adp@program-aged2-3 | 2 | +6.600 ms, 80,447 (0.804 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.879 (20) | 9.121 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.164 (20) | 9.836 |
| backlog-adp@verify-aged2-3 | 2 | +6.848 ms, 77,604 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.895 (20) | 9.105 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.072 (20) | 9.928 |

Least margin over the aged windows: 9.048 ms, `backlog-adp@blank-aged2-3.service.srp.last.if0` at 10.952 ms.

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 163.761 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 7.698 ms | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-flight | 1553 | 93,940 (0.939) | 78,582 (0.786) |
| backlog-adp@program-3 | 372 | 96,134 (0.961) | 78,894 (0.789) |
| backlog-adp@verify-3 | 397 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@blank-aged2-3 | 342 | 93,218 (0.932) | 76,121 (0.761) |
| backlog-adp@blank-aged1-3 | 339 | 92,546 (0.925) | 76,468 (0.765) |
| backlog-adp@program-aged2-3 | 369 | 95,347 (0.953) | 78,531 (0.785) |
| backlog-adp@program-aged1-3 | 368 | 94,921 (0.949) | 78,843 (0.788) |
| backlog-adp@verify-aged2-3 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@verify-aged1-3 | 397 | 94,984 (0.950) | 78,276 (0.783) |
| acmp-noresp | 708 | 101,504 (1.015) | 78,276 (0.783) |
| adp-gm | 79 | 22,571 (0.226) | 2,593 (0.026) |
| aecp-largest-notice | 78 | 22,571 (0.226) | 2,593 (0.026) |

Longest pass that carries a step: 101,504 CPU cycles (1.015 ms), acmp-noresp; longest step: 78,894 (0.789 ms), backlog-adp@program-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 157,423 | 1.574 | 20 | 200 | fits | 158,363 | 243 | 0.494 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 229,985 | 2.300 | 20 | 20 | fits | 92,699 | 91 | 0.627 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 282,070 | 2.821 | 20 | 24 | fits | 49,241 | 35 | 0.522 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 235,044 | 2.350 | 20 | 50 | fits | 97,973 | 202 | 0.300 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 908,889 | 9.089 | 20 | 20 | fits | 85,828 | 28 | 0.607 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 59,681 | 0.597 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 49,176 | 0.492 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 190,835 | 1.908 | 49 | 49 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 367,907 | 3.679 | 20 | 20 | fits | 122,838 | 169 | 0.468 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 306,363 | 3.064 | 20 | 200 | fits | 149,257 | 226 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 428,585 | 4.286 | 20 | 200 | fits | 122,838 | 169 | 0.468 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 307,287 | 3.073 | 20 | 20 | fits | 149,257 | 226 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 429,289 | 4.293 | 20 | 20 | fits | 122,838 | 169 | 0.468 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 161,670 | 1.617 | 20 | 24 | fits | 152,911 | 155 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 309,937 | 3.099 | 20 | 24 | fits | 149,257 | 226 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 309,871 | 3.099 | 20 | 50 | fits | 149,257 | 226 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 432,313 | 4.323 | 20 | 50 | fits | 122,838 | 169 | 0.468 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 516,408 | 5.164 | 20 | 20 | fits | 84,161 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,023,488 | 10.235 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 357,872 | 3.579 | 20 | 20 | fits | 113,211 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 305,299 | 3.053 | 20 | 200 | fits | 148,682 | 226 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 417,894 | 4.179 | 20 | 200 | fits | 113,211 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 306,223 | 3.062 | 20 | 20 | fits | 148,682 | 226 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 418,598 | 4.186 | 20 | 20 | fits | 113,211 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 161,181 | 1.612 | 20 | 24 | fits | 152,657 | 155 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 308,873 | 3.089 | 20 | 24 | fits | 148,682 | 226 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 308,807 | 3.088 | 20 | 50 | fits | 148,682 | 226 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 421,622 | 4.216 | 20 | 50 | fits | 113,211 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 505,916 | 5.059 | 20 | 20 | fits | 84,360 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,018,698 | 10.187 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 364,975 | 3.650 | 20 | 20 | fits | 113,069 | 163 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 304,720 | 3.047 | 20 | 200 | fits | 149,124 | 226 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 417,173 | 4.172 | 20 | 200 | fits | 113,069 | 163 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 305,644 | 3.056 | 20 | 20 | fits | 149,124 | 226 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 417,877 | 4.179 | 20 | 20 | fits | 113,069 | 163 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 160,160 | 1.602 | 20 | 24 | fits | 151,380 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 308,294 | 3.083 | 20 | 24 | fits | 149,124 | 226 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 308,228 | 3.082 | 20 | 50 | fits | 149,124 | 226 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 420,901 | 4.209 | 20 | 50 | fits | 113,069 | 163 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 505,190 | 5.052 | 20 | 20 | fits | 84,355 | 25 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,095,156 | 10.952 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 358,458 | 3.585 | 20 | 20 | fits | 113,121 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 298,203 | 2.982 | 20 | 200 | fits | 149,032 | 226 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 410,708 | 4.107 | 20 | 200 | fits | 113,121 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 299,127 | 2.991 | 20 | 20 | fits | 149,032 | 226 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 411,412 | 4.114 | 20 | 20 | fits | 113,121 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 153,735 | 1.537 | 20 | 24 | fits | 151,466 | 152 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 301,777 | 3.018 | 20 | 24 | fits | 149,032 | 226 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 301,711 | 3.017 | 20 | 50 | fits | 149,032 | 226 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 414,436 | 4.144 | 20 | 50 | fits | 113,121 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 498,490 | 4.985 | 20 | 20 | fits | 84,120 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,012,876 | 10.129 | 20 | 20 | fits | 85,791 | 28 | 0.604 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 345,343 | 3.453 | 20 | 20 | fits | 112,878 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 292,447 | 2.924 | 20 | 200 | fits | 149,626 | 231 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 404,709 | 4.047 | 20 | 200 | fits | 112,878 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 293,371 | 2.934 | 20 | 20 | fits | 149,626 | 231 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 405,413 | 4.054 | 20 | 20 | fits | 112,878 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 147,385 | 1.474 | 20 | 24 | fits | 151,393 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 296,021 | 2.960 | 20 | 24 | fits | 149,626 | 231 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 295,955 | 2.960 | 20 | 50 | fits | 149,626 | 231 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 408,437 | 4.084 | 20 | 50 | fits | 112,878 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 492,822 | 4.928 | 20 | 20 | fits | 84,451 | 24 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,087,880 | 10.879 | 20 | 20 | fits | 85,791 | 28 | 0.604 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 366,402 | 3.664 | 20 | 20 | fits | 120,582 | 184 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 313,669 | 3.137 | 20 | 200 | fits | 146,326 | 209 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 433,635 | 4.336 | 20 | 200 | fits | 120,582 | 184 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 314,593 | 3.146 | 20 | 20 | fits | 146,326 | 209 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 434,339 | 4.343 | 20 | 20 | fits | 120,582 | 184 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 160,866 | 1.609 | 20 | 24 | fits | 151,595 | 153 | 0.422 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 317,243 | 3.172 | 20 | 24 | fits | 146,326 | 209 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 317,177 | 3.172 | 20 | 50 | fits | 146,326 | 209 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 437,363 | 4.374 | 20 | 50 | fits | 120,582 | 184 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 522,174 | 5.222 | 20 | 20 | fits | 84,877 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,016,357 | 10.164 | 20 | 20 | fits | 73,147 | 25 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 376,666 | 3.767 | 20 | 20 | fits | 120,215 | 173 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 298,265 | 2.983 | 20 | 200 | fits | 147,962 | 223 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 429,401 | 4.294 | 20 | 200 | fits | 120,215 | 173 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 299,189 | 2.992 | 20 | 20 | fits | 147,962 | 223 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 430,105 | 4.301 | 20 | 20 | fits | 120,215 | 173 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 154,867 | 1.549 | 20 | 24 | fits | 151,369 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 301,839 | 3.018 | 20 | 24 | fits | 147,962 | 223 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 301,773 | 3.018 | 20 | 50 | fits | 147,962 | 223 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 433,129 | 4.331 | 20 | 50 | fits | 120,215 | 173 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 517,306 | 5.173 | 20 | 20 | fits | 84,243 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,089,463 | 10.895 | 20 | 20 | fits | 73,147 | 25 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 355,002 | 3.550 | 20 | 20 | fits | 113,244 | 166 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 293,587 | 2.936 | 20 | 200 | fits | 148,891 | 227 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 406,215 | 4.062 | 20 | 200 | fits | 113,244 | 166 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 294,511 | 2.945 | 20 | 20 | fits | 148,891 | 227 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 406,919 | 4.069 | 20 | 20 | fits | 113,244 | 166 | 0.407 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 149,260 | 1.493 | 20 | 24 | fits | 151,480 | 152 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 297,161 | 2.972 | 20 | 24 | fits | 148,891 | 227 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 297,095 | 2.971 | 20 | 50 | fits | 148,891 | 227 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 409,943 | 4.099 | 20 | 50 | fits | 113,244 | 166 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 494,385 | 4.944 | 20 | 20 | fits | 84,508 | 25 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,007,156 | 10.072 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 32,167 | 0.322 | 20 | 20 | fits | 32,999 | 27 (35) | 0.811 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 24,372 | 0.244 | 20 | 20 | fits | 30,135 | 23 (14) | 0.847 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 6,700 | 0.067 | 20 | 20 | fits | 25,783 | 18 (14) | 0.845 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 10,231 | 0.102 | 20 | 20 | fits | 32,314 | 28 (35) | 0.786 |
| LINK_UP | `adp.link_up.if0` | 2,771 | 0.028 | 20 | 200 | fits | 27,812 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,072 | 0.161 | 20 | 200 | fits | 22,379 | 23 (39) | 0.719 |
| GM_CHANGE | `adp.gm_change.if0` | 2,588 | 0.026 | 20 | 200 | fits | 16,540 | 17 (11) | 0.672 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 145,914 | 1.459 | 20 | 24 | fits | 158,006 | 137 | 0.343 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 218,232 | 2.182 | 20 | 24 | fits | 147,302 | 113 | 0.312 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 229,949 | 2.299 | 20 | 24 | fits | 42,136 | 18 | 0.693 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 387,621 | 3.876 | 20 | 24 | fits | 99,235 | 17 | 0.683 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 330,364 | 3.304 | 20 | 24 | fits | 101,455 | 17 | 0.697 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

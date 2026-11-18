### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 20 paths and 0 of 104 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.026 (0.248) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-link) | 0.028 (0.278) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-link) | 0.161 (0.483) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged1-2.adp_available.if0` (backlog-adp@program-aged1-2) | 3.767 (4.309) | fits | 7 adp | 8 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.848 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.576 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.984 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-burst.held.maap.if0` (save-burst) | 1.673 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 10.017 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.903 | fits | 0 srp | 3 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-2.service.acmp.first.if0` (backlog-adp@verify-2) | 3.187 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-2.service.acmp.last.if0` (backlog-adp@program-2) | 4.321 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-2.service.adp.first.if0` (backlog-adp@verify-2) | 3.178 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-2.service.adp.last.if0` (backlog-adp@program-2) | 4.314 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-2.service.aecp.first.if0` (backlog-adp@verify-2) | 1.737 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-2.service.aecp.last.if0` (backlog-adp@verify-2) | 3.214 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-2.service.maap.first.if0` (backlog-adp@verify-2) | 3.213 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-2.service.maap.last.if0` (backlog-adp@program-2) | 4.351 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-2.service.srp.first.if0` (backlog-adp@program-2) | 5.191 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-2.service.srp.last.if0` (backlog-adp@program-aged2-2) | 11.090 | fits | 31 srp | 8 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-2 | 0 | 11.681 | 11 | 152,870 (1.529) | yes | - |
| backlog-adp@verify-2 | 0 | 13.112 | 11 | 152,657 (1.527) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 13.673 | 11 | 151,380 (1.514) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.997 | 11 | 151,353 (1.514) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 12.506 | 12 | 152,001 (1.520) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 12.806 | 13 | 151,252 (1.513) | yes | - |
| backlog-adp@verify-aged2-2 | 1 | 15.725 | 12 | 149,845 (1.498) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 12.998 | 11 | 151,480 (1.515) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-burst | 2902 | 0 | 158,363 (1.584) | fits |
| backlog-adp@program-2 | 493 | 0 | 152,870 (1.529) | fits |
| backlog-adp@verify-2 | 499 | 0 | 152,657 (1.527) | fits |
| backlog-adp@blank-aged2-2 | 757 | 0 | 151,380 (1.514) | fits |
| backlog-adp@blank-aged1-2 | 697 | 0 | 152,764 (1.528) | fits |
| backlog-adp@program-aged2-2 | 786 | 0 | 152,001 (1.520) | fits |
| backlog-adp@program-aged1-2 | 726 | 0 | 151,252 (1.513) | fits |
| backlog-adp@verify-aged2-2 | 803 | 0 | 151,369 (1.514) | fits |
| backlog-adp@verify-aged1-2 | 741 | 0 | 151,480 (1.515) | fits |
| save-starved | 24486 | 0 | 158,363 (1.584) | fits |
| adp-link | 89 | 0 | 39,777 (0.398) | fits |
| datapath-events | 117 | 0 | 30,398 (0.304) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-2 | 2 | +8.450 ms, 77,018 (0.770 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.903 (20) | 9.097 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.221 (20) | 9.779 |
| backlog-adp@program-aged2-2 | 2 | +7.670 ms, 80,506 (0.805 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.090 (20) | 8.910 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.115 (20) | 9.885 |
| backlog-adp@verify-aged2-2 | 2 | +8.498 ms, 77,604 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.828 (20) | 9.172 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.199 (20) | 9.801 |

Least margin over the aged windows: 8.910 ms, `backlog-adp@program-aged2-2.service.srp.last.if0` at 11.090 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 4048.898 | 4,070 | 102 | - | 31.501 | yes | within |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 39 | 1106.926 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-burst | 1479 | 93,815 (0.938) | 78,337 (0.783) |
| backlog-adp@program-2 | 371 | 95,469 (0.955) | 78,491 (0.785) |
| backlog-adp@verify-2 | 397 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@blank-aged2-2 | 340 | 92,291 (0.923) | 76,180 (0.762) |
| backlog-adp@blank-aged1-2 | 339 | 92,748 (0.927) | 76,409 (0.764) |
| backlog-adp@program-aged2-2 | 369 | 95,347 (0.953) | 78,531 (0.785) |
| backlog-adp@program-aged1-2 | 369 | 95,992 (0.960) | 78,835 (0.788) |
| backlog-adp@verify-aged2-2 | 400 | 100,005 (1.000) | 78,276 (0.783) |
| backlog-adp@verify-aged1-2 | 397 | 94,984 (0.950) | 78,276 (0.783) |
| save-starved | 418 | 81,013 (0.810) | 78,586 (0.786) |
| adp-link | 79 | 22,571 (0.226) | 2,593 (0.026) |
| datapath-events | 69 | 22,571 (0.226) | 2,593 (0.026) |

Longest pass that carries a step: 100,005 CPU cycles (1.000 ms), backlog-adp@verify-aged2-2; longest step: 78,835 (0.788 ms), backlog-adp@program-aged1-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 157,554 | 1.576 | 20 | 200 | fits | 158,363 | 243 | 0.494 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 242,783 | 2.428 | 20 | 20 | fits | 105,497 | 100 | 0.658 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 127,728 | 1.277 | 20 | 24 | fits | 65,562 | 56 | 0.720 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 167,292 | 1.673 | 20 | 50 | fits | 65,562 | 56 | 0.720 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 874,404 | 8.744 | 20 | 20 | fits | 81,454 | 32 | 0.716 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 55,028 | 0.550 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 256,516 | 2.565 | 49 | 49 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 370,828 | 3.708 | 20 | 20 | fits | 122,313 | 169 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 309,682 | 3.097 | 20 | 200 | fits | 148,441 | 226 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 431,379 | 4.314 | 20 | 200 | fits | 122,313 | 169 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 310,606 | 3.106 | 20 | 20 | fits | 148,441 | 226 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 432,083 | 4.321 | 20 | 20 | fits | 122,313 | 169 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 165,805 | 1.658 | 20 | 24 | fits | 152,870 | 155 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 313,256 | 3.133 | 20 | 24 | fits | 148,441 | 226 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 313,190 | 3.132 | 20 | 50 | fits | 148,441 | 226 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 435,107 | 4.351 | 20 | 50 | fits | 122,313 | 169 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 519,138 | 5.191 | 20 | 20 | fits | 84,097 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,026,091 | 10.261 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 370,372 | 3.704 | 20 | 20 | fits | 113,211 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 317,799 | 3.178 | 20 | 200 | fits | 148,682 | 226 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 430,394 | 4.304 | 20 | 200 | fits | 113,211 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 318,723 | 3.187 | 20 | 20 | fits | 148,682 | 226 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 431,098 | 4.311 | 20 | 20 | fits | 113,211 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 173,681 | 1.737 | 20 | 24 | fits | 152,657 | 155 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 321,373 | 3.214 | 20 | 24 | fits | 148,682 | 226 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 321,307 | 3.213 | 20 | 50 | fits | 148,682 | 226 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 434,122 | 4.341 | 20 | 50 | fits | 113,211 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 518,416 | 5.184 | 20 | 20 | fits | 84,360 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,031,198 | 10.312 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 351,458 | 3.515 | 20 | 20 | fits | 112,824 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 298,562 | 2.986 | 20 | 200 | fits | 148,566 | 226 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 410,770 | 4.108 | 20 | 200 | fits | 112,824 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 299,486 | 2.995 | 20 | 20 | fits | 148,566 | 226 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 411,474 | 4.115 | 20 | 20 | fits | 112,824 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 154,560 | 1.546 | 20 | 24 | fits | 151,380 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 302,136 | 3.021 | 20 | 24 | fits | 148,566 | 226 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 302,070 | 3.021 | 20 | 50 | fits | 148,566 | 226 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 414,498 | 4.145 | 20 | 50 | fits | 112,824 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 498,516 | 4.985 | 20 | 20 | fits | 84,084 | 24 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,090,304 | 10.903 | 20 | 20 | fits | 85,814 | 28 | 0.604 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 360,793 | 3.608 | 20 | 20 | fits | 117,760 | 169 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 304,459 | 3.045 | 20 | 200 | fits | 151,353 | 231 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 421,603 | 4.216 | 20 | 200 | fits | 117,760 | 169 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 305,383 | 3.054 | 20 | 20 | fits | 151,353 | 231 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 422,307 | 4.223 | 20 | 20 | fits | 117,760 | 169 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 146,790 | 1.468 | 20 | 24 | fits | 152,764 | 153 | 0.423 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 308,033 | 3.080 | 20 | 24 | fits | 151,353 | 231 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 307,967 | 3.080 | 20 | 50 | fits | 151,353 | 231 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 425,331 | 4.253 | 20 | 50 | fits | 117,760 | 169 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 509,567 | 5.096 | 20 | 20 | fits | 84,302 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,022,129 | 10.221 | 20 | 20 | fits | 78,983 | 31 | 0.715 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 374,247 | 3.742 | 20 | 20 | fits | 113,310 | 166 | 0.408 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 312,766 | 3.128 | 20 | 200 | fits | 147,854 | 222 | 0.438 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 425,460 | 4.255 | 20 | 200 | fits | 113,310 | 166 | 0.408 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 313,690 | 3.137 | 20 | 20 | fits | 147,854 | 222 | 0.438 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 426,164 | 4.262 | 20 | 20 | fits | 113,310 | 166 | 0.408 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 169,476 | 1.695 | 20 | 24 | fits | 152,001 | 153 | 0.427 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 316,340 | 3.163 | 20 | 24 | fits | 147,854 | 222 | 0.438 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 316,274 | 3.163 | 20 | 50 | fits | 147,854 | 222 | 0.438 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 429,188 | 4.292 | 20 | 50 | fits | 113,310 | 166 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 513,825 | 5.138 | 20 | 20 | fits | 84,703 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,108,980 | 11.090 | 20 | 20 | fits | 86,060 | 28 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 376,717 | 3.767 | 20 | 20 | fits | 120,034 | 173 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 298,514 | 2.985 | 20 | 200 | fits | 148,155 | 223 | 0.440 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 429,394 | 4.294 | 20 | 200 | fits | 120,034 | 173 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 299,438 | 2.994 | 20 | 20 | fits | 148,155 | 223 | 0.440 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 430,098 | 4.301 | 20 | 20 | fits | 120,034 | 173 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 154,923 | 1.549 | 20 | 24 | fits | 151,252 | 152 | 0.418 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 302,088 | 3.021 | 20 | 24 | fits | 148,155 | 223 | 0.440 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 302,022 | 3.020 | 20 | 50 | fits | 148,155 | 223 | 0.440 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 433,122 | 4.331 | 20 | 50 | fits | 120,034 | 173 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 517,453 | 5.175 | 20 | 20 | fits | 84,397 | 24 | 0.776 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,011,457 | 10.115 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 346,980 | 3.470 | 20 | 20 | fits | 113,320 | 164 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 294,430 | 2.944 | 20 | 200 | fits | 149,845 | 231 | 0.423 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 407,134 | 4.071 | 20 | 200 | fits | 113,320 | 164 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 295,354 | 2.954 | 20 | 20 | fits | 149,845 | 231 | 0.423 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 407,838 | 4.078 | 20 | 20 | fits | 113,320 | 164 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 149,149 | 1.491 | 20 | 24 | fits | 151,369 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 298,004 | 2.980 | 20 | 24 | fits | 149,845 | 231 | 0.423 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 297,938 | 2.979 | 20 | 50 | fits | 149,845 | 231 | 0.423 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 410,862 | 4.109 | 20 | 50 | fits | 113,320 | 164 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 510,952 | 5.110 | 20 | 20 | fits | 88,372 | 31 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,082,780 | 10.828 | 20 | 20 | fits | 73,004 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 357,020 | 3.570 | 20 | 20 | fits | 113,518 | 163 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 304,237 | 3.042 | 20 | 200 | fits | 148,996 | 226 | 0.433 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 417,139 | 4.171 | 20 | 200 | fits | 113,518 | 163 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 305,161 | 3.052 | 20 | 20 | fits | 148,996 | 226 | 0.433 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 417,843 | 4.178 | 20 | 20 | fits | 113,518 | 163 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 159,805 | 1.598 | 20 | 24 | fits | 151,480 | 152 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 307,811 | 3.078 | 20 | 24 | fits | 148,996 | 226 | 0.433 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 307,745 | 3.077 | 20 | 50 | fits | 148,996 | 226 | 0.433 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 420,867 | 4.209 | 20 | 50 | fits | 113,518 | 163 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 505,197 | 5.052 | 20 | 20 | fits | 84,396 | 24 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,019,870 | 10.199 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 157,423 | 1.574 | 20 | 200 | fits | 158,363 | 243 | 0.494 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 284,777 | 2.848 | 20 | 20 | fits | 81,801 | 42 | 0.677 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 298,443 | 2.984 | 20 | 24 | fits | 83,897 | 55 | 0.607 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 141,811 | 1.418 | 20 | 50 | fits | 34,679 | 43 | 0.665 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 1,001,724 | 10.017 | 20 | 20 | fits | 50,577 | 22 | 0.762 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 290,308 | 2.903 | 49 | 49 | fits | 0 | - | 0.000 |
| LINK_UP | `adp.link_up.if0` | 2,771 | 0.028 | 20 | 200 | fits | 27,812 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,072 | 0.161 | 20 | 200 | fits | 22,379 | 23 (39) | 0.719 |
| LINK_DOWN | `adp.link_down.if0` | 2,574 | 0.026 | 20 | 200 | fits | 24,786 | 23 (9) | 0.750 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

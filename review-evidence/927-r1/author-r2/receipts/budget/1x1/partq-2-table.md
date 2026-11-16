### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 28 paths and 0 of 73 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.246 (0.605) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.191 (0.534) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.160 (0.496) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.135 (0.494) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.046 (0.172) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.026 (0.271) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.095 (0.424) | fits | 0 events | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.165 (3.511) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.173 (2.553) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.834 (4.205) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.069 (3.432) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.348 (1.515) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.586 (4.144) | fits | 7 adp | 5 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.158 (0.498) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.095 (0.224) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.100 (0.271) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.136 (0.498) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.094 (0.417) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-3.service.acmp.first.if0` (backlog-adp@verify-aged1-3) | 3.068 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-3.service.acmp.last.if0` (backlog-adp@verify-aged2-3) | 4.167 | fits | 11 acmp | 5 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-3.service.adp.first.if0` (backlog-adp@verify-aged1-3) | 3.058 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-3.service.adp.last.if0` (backlog-adp@verify-aged2-3) | 4.160 | fits | 7 adp | 5 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-3.service.aecp.first.if0` (backlog-adp@verify-aged1-3) | 1.620 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-3.service.aecp.last.if0` (backlog-adp@verify-aged1-3) | 3.094 | fits | 15 aecp | 5 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-3.service.maap.first.if0` (backlog-adp@verify-aged1-3) | 3.094 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-3.service.maap.last.if0` (backlog-adp@verify-aged2-3) | 4.197 | fits | 6 maap | 5 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-7.service.srp.first.if0` (backlog-adp@verify-aged2-7) | 5.705 | fits | 0 srp | 5 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-3.service.srp.last.if0` (backlog-adp@verify-aged2-3) | 10.771 | fits | 31 srp | 5 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@verify-aged2-3 | 0 | 11.598 | 13 | 152,135 (1.521) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 12.228 | 11 | 149,802 (1.498) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.340 | 11 | 152,364 (1.524) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 12.390 | 12 | 152,056 (1.521) | yes | - |
| backlog-adp | 0 | 10.469 | 11 | 152,335 (1.523) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill, backlog-owed not run): 152,335 CPU cycles (1.523 ms), backlog-adp.
Over the windows that released their whole load only: 152,335 (1.523 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@verify-aged2-3 | 917 | 0 | 152,135 (1.521) | fits |
| backlog-adp@verify-aged2-7 | 945 | 0 | 152,317 (1.523) | fits |
| backlog-adp@verify-aged1-3 | 857 | 0 | 152,364 (1.524) | fits |
| backlog-adp@verify-aged1-7 | 887 | 0 | 152,056 (1.521) | fits |
| acmp-noresp | 2023 | 0 | 41,470 (0.415) | fits |
| backlog-adp | 315 | 0 | 152,335 (1.523) | fits |
| maap | 182 | 0 | 30,305 (0.303) | fits |
| control | 88 | 0 | 30,305 (0.303) | fits |
| aecp-largest-notice | 105 | 0 | 151,514 (1.515) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@verify-aged2-3 | 2 | +6.724 ms, 77,541 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 10.771 (20) | 9.229 |
| backlog-adp@verify-aged2-7 | 2 | +4.088 ms, 77,749 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 10.739 (20) | 9.261 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.045 (20) | 9.955 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.983 (20) | 10.017 |

Least margin over the aged windows: 9.229 ms, `backlog-adp@verify-aged2-3.service.srp.last.if0` at 10.771 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@verify-aged2-3 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged2-7 | 356 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-3 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-7 | 356 | 96,998 (0.970) | 78,341 (0.783) |
| acmp-noresp | 615 | 97,311 (0.973) | 78,205 (0.782) |
| backlog-adp | 271 | 22,507 (0.225) | 2,414 (0.024) |
| maap | 169 | 22,437 (0.224) | 2,414 (0.024) |
| control | 79 | 22,267 (0.223) | 2,414 (0.024) |
| aecp-largest-notice | 78 | 22,267 (0.223) | 2,414 (0.024) |

Longest pass that carries a step: 97,311 CPU cycles (0.973 ms), acmp-noresp; longest step: 78,341 (0.783 ms), backlog-adp@verify-aged2-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 351,378 | 3.514 | 20 | 20 | fits | 103,474 | 158 | 0.489 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 303,543 | 3.035 | 20 | 200 | fits | 151,496 | 238 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 415,965 | 4.160 | 20 | 200 | fits | 103,474 | 158 | 0.489 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 304,467 | 3.045 | 20 | 20 | fits | 151,496 | 238 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 416,669 | 4.167 | 20 | 20 | fits | 103,474 | 158 | 0.489 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 156,611 | 1.566 | 20 | 24 | fits | 152,135 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 307,117 | 3.071 | 20 | 24 | fits | 151,496 | 238 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 307,051 | 3.071 | 20 | 50 | fits | 151,496 | 238 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 419,693 | 4.197 | 20 | 50 | fits | 103,474 | 158 | 0.489 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 505,720 | 5.057 | 20 | 20 | fits | 86,093 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,077,135 | 10.771 | 20 | 20 | fits | 73,432 | 25 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 346,061 | 3.461 | 20 | 20 | fits | 108,680 | 148 | 0.471 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 295,416 | 2.954 | 20 | 200 | fits | 149,802 | 253 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 403,480 | 4.035 | 20 | 200 | fits | 108,680 | 148 | 0.471 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 296,340 | 2.963 | 20 | 20 | fits | 149,802 | 253 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 404,184 | 4.042 | 20 | 20 | fits | 108,680 | 148 | 0.471 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 150,178 | 1.502 | 20 | 24 | fits | 152,317 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 298,990 | 2.990 | 20 | 24 | fits | 149,802 | 253 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 298,924 | 2.989 | 20 | 50 | fits | 149,802 | 253 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 407,208 | 4.072 | 20 | 50 | fits | 108,680 | 148 | 0.471 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 570,527 | 5.705 | 20 | 20 | fits | 85,636 | 26 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,073,851 | 10.739 | 20 | 20 | fits | 73,340 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 348,718 | 3.487 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 305,847 | 3.058 | 20 | 200 | fits | 148,442 | 248 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 405,804 | 4.058 | 20 | 200 | fits | 100,573 | 142 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 306,771 | 3.068 | 20 | 20 | fits | 148,442 | 248 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 406,508 | 4.065 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 161,969 | 1.620 | 20 | 24 | fits | 152,364 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 309,421 | 3.094 | 20 | 24 | fits | 148,442 | 248 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 309,355 | 3.094 | 20 | 50 | fits | 148,442 | 248 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 409,532 | 4.095 | 20 | 50 | fits | 100,573 | 142 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 495,817 | 4.958 | 20 | 20 | fits | 86,351 | 25 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,004,462 | 10.045 | 20 | 20 | fits | 85,585 | 28 | 0.637 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 355,545 | 3.555 | 20 | 20 | fits | 105,910 | 163 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 300,937 | 3.009 | 20 | 200 | fits | 150,072 | 231 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 406,231 | 4.062 | 20 | 200 | fits | 105,910 | 163 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 301,861 | 3.019 | 20 | 20 | fits | 150,072 | 231 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 406,935 | 4.069 | 20 | 20 | fits | 105,910 | 163 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 155,429 | 1.554 | 20 | 24 | fits | 152,056 | 152 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 304,511 | 3.045 | 20 | 24 | fits | 150,072 | 231 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 304,445 | 3.044 | 20 | 50 | fits | 150,072 | 231 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 409,959 | 4.100 | 20 | 50 | fits | 105,910 | 163 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 496,174 | 4.962 | 20 | 20 | fits | 86,281 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 998,343 | 9.983 | 20 | 20 | fits | 73,608 | 24 | 0.693 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 19,112 | 0.191 | 20 | 20 | fits | 32,511 | 27 (35) | 0.812 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 15,969 | 0.160 | 20 | 20 | fits | 28,769 | 23 (14) | 0.838 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 13,492 | 0.135 | 20 | 20 | fits | 28,587 | 24 (14) | 0.841 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 24,584 | 0.246 | 20 | 20 | fits | 29,331 | 21 (35) | 0.812 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 358,627 | 3.586 | 20 | 20 | fits | 102,804 | 161 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 297,517 | 2.975 | 20 | 200 | fits | 149,932 | 234 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 409,062 | 4.091 | 20 | 200 | fits | 102,804 | 161 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 298,441 | 2.984 | 20 | 20 | fits | 149,932 | 234 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 409,766 | 4.098 | 20 | 20 | fits | 102,804 | 161 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 152,149 | 1.521 | 20 | 24 | fits | 152,335 | 155 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 301,091 | 3.011 | 20 | 24 | fits | 149,932 | 234 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 301,025 | 3.010 | 20 | 50 | fits | 149,932 | 234 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 412,790 | 4.128 | 20 | 50 | fits | 102,804 | 161 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 499,004 | 4.990 | 20 | 20 | fits | 86,280 | 24 | 0.792 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 992,224 | 9.922 | 20 | 20 | fits | 73,132 | 24 | 0.673 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,038 | 0.100 | 20 | 50 | fits | 27,119 | 43 | 0.739 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 9,371 | 0.094 | 20 | 50 | fits | 23,534 | 35 | 0.719 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 7,311 | 0.073 | 20 | 50 | fits | 23,515 | 35 | 0.723 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 13,559 | 0.136 | 20 | 50 | fits | 28,584 | 61 | 0.649 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 15,764 | 0.158 | 20 | 50 | fits | 28,584 | 61 | 0.649 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,538 | 0.095 | 20 | 50 | fits | 22,353 | 30 | 0.661 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,616 | 0.046 | 20 | 200 | fits | 17,250 | 16 (31) | 0.667 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 134,819 | 1.348 | 20 | 24 | fits | 151,514 | 98 | 0.346 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 316,510 | 3.165 | 20 | 24 | fits | 137,980 | 70 | 0.313 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 217,337 | 2.173 | 20 | 24 | fits | 42,242 | 17 | 0.698 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 383,383 | 3.834 | 20 | 24 | fits | 100,249 | 33 | 0.683 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 306,906 | 3.069 | 20 | 24 | fits | 93,278 | 17 | 0.667 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

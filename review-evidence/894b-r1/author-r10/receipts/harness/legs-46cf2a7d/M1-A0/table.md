### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 24 paths and 0 of 101 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.077 (0.269) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.055 (0.242) | fits | 0 adp | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.096 (0.299) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.176 (0.616) | fits | 0 events | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.104 (3.445) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.105 (2.480) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.936 (4.311) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.184 (3.547) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.475 (1.813) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-5.adp_available.if0` (backlog-adp@verify-aged2-5) | 3.617 (4.179) | fits | 7 adp | 8 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.acmp.first.if0` (backlog-adp@verify-5) | 3.085 | fits | 0 acmp | 8 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-5.service.acmp.last.if0` (backlog-adp@verify-aged1-5) | 4.172 | fits | 11 acmp | 8 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.adp.first.if0` (backlog-adp@verify-5) | 3.076 | fits | 0 adp | 8 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-5.service.adp.last.if0` (backlog-adp@verify-aged1-5) | 4.165 | fits | 7 adp | 8 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.aecp.first.if0` (backlog-adp@verify-5) | 1.642 | fits | 0 aecp | 8 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-5.service.aecp.last.if0` (backlog-adp@verify-5) | 3.112 | fits | 15 aecp | 8 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.maap.first.if0` (backlog-adp@verify-5) | 3.111 | fits | 0 maap | 8 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-5.service.maap.last.if0` (backlog-adp@verify-aged1-5) | 4.202 | fits | 6 maap | 8 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-5.service.srp.first.if0` (backlog-adp@verify-aged2-5) | 5.756 | fits | 0 srp | 8 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-5.service.srp.last.if0` (backlog-adp@verify-aged2-5) | 10.783 | fits | 31 srp | 8 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.867 (0.960) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.430 (0.430) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.221 (0.222) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.773 (0.854) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-5 | 0 | 10.537 | 11 | 152,479 (1.525) | yes | - |
| backlog-adp@verify-5 | 0 | 11.324 | 12 | 152,375 (1.524) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.174 | 11 | 151,895 (1.519) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.931 | 13 | 152,235 (1.522) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.449 | 12 | 149,528 (1.495) | yes | - |
| backlog-adp@program-aged1-5 | 1 | 11.210 | 10 | 152,018 (1.520) | yes | - |
| backlog-adp@verify-aged2-5 | 1 | 11.314 | 11 | 151,191 (1.512) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.650 | 13 | 152,485 (1.525) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3360 | 0 | 40,360 (0.404) | fits |
| backlog-adp@program-5 | 524 | 0 | 152,479 (1.525) | fits |
| backlog-adp@verify-5 | 616 | 0 | 152,375 (1.524) | fits |
| backlog-adp@blank-aged2-5 | 732 | 0 | 151,895 (1.519) | fits |
| backlog-adp@blank-aged1-5 | 678 | 0 | 152,235 (1.522) | fits |
| backlog-adp@program-aged2-5 | 834 | 0 | 152,316 (1.523) | fits |
| backlog-adp@program-aged1-5 | 774 | 0 | 152,316 (1.523) | fits |
| backlog-adp@verify-aged2-5 | 930 | 0 | 152,546 (1.525) | fits |
| backlog-adp@verify-aged1-5 | 873 | 0 | 152,485 (1.525) | fits |
| srp | 290 | 0 | 57,281 (0.573) | fits |
| acmp-disc | 878 | 0 | 40,360 (0.404) | fits |
| aecp-largest-notice | 105 | 0 | 150,533 (1.505) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.643 (20) | 9.357 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.640 (20) | 9.360 |
| backlog-adp@program-aged2-5 | 2 | +4.984 ms, 80,811 (0.808 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.626 (20) | 9.374 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.873 (20) | 10.127 |
| backlog-adp@verify-aged2-5 | 2 | +4.159 ms, 77,572 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.783 (20) | 9.217 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.892 (20) | 10.108 |

Least margin over the aged windows: 9.217 ms, `backlog-adp@verify-aged2-5.service.srp.last.if0` at 10.783 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 96,940 (0.969) | 78,143 (0.781) |
| backlog-adp@program-5 | 329 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-5 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@blank-aged2-5 | 297 | 86,151 (0.862) | 76,128 (0.761) |
| backlog-adp@blank-aged1-5 | 297 | 92,890 (0.929) | 76,289 (0.763) |
| backlog-adp@program-aged2-5 | 326 | 96,381 (0.964) | 78,636 (0.786) |
| backlog-adp@program-aged1-5 | 326 | 96,574 (0.966) | 78,878 (0.789) |
| backlog-adp@verify-aged2-5 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-aged1-5 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| srp | 271 | 22,268 (0.223) | 2,242 (0.022) |
| acmp-disc | 305 | 96,237 (0.962) | 78,143 (0.781) |
| aecp-largest-notice | 78 | 22,142 (0.221) | 2,242 (0.022) |

Longest pass that carries a step: 96,940 CPU cycles (0.969 ms), acmp-notk; longest step: 78,878 (0.789 ms), backlog-adp@program-aged1-5.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 17,595 | 0.176 | 20 | 20 | fits | 33,902 | 19 (14) | 0.889 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 344,799 | 3.448 | 20 | 20 | fits | 99,348 | 142 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 302,192 | 3.022 | 20 | 200 | fits | 148,028 | 248 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 400,924 | 4.009 | 20 | 200 | fits | 99,348 | 142 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 303,116 | 3.031 | 20 | 20 | fits | 148,028 | 248 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 401,628 | 4.016 | 20 | 20 | fits | 99,348 | 142 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 158,728 | 1.587 | 20 | 24 | fits | 152,479 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 305,766 | 3.058 | 20 | 24 | fits | 148,028 | 248 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 305,700 | 3.057 | 20 | 50 | fits | 148,028 | 248 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 404,652 | 4.047 | 20 | 50 | fits | 99,348 | 142 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 488,687 | 4.887 | 20 | 20 | fits | 84,101 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 995,704 | 9.957 | 20 | 20 | fits | 85,230 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 357,634 | 3.576 | 20 | 20 | fits | 106,763 | 148 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 307,616 | 3.076 | 20 | 200 | fits | 147,977 | 248 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 413,763 | 4.138 | 20 | 200 | fits | 106,763 | 148 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 308,540 | 3.085 | 20 | 20 | fits | 147,977 | 248 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 414,467 | 4.145 | 20 | 20 | fits | 106,763 | 148 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 164,203 | 1.642 | 20 | 24 | fits | 152,375 | 156 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 311,190 | 3.112 | 20 | 24 | fits | 147,977 | 248 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 311,124 | 3.111 | 20 | 50 | fits | 147,977 | 248 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 417,491 | 4.175 | 20 | 50 | fits | 106,763 | 148 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 501,770 | 5.018 | 20 | 20 | fits | 84,345 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,002,977 | 10.030 | 20 | 20 | fits | 73,031 | 24 | 0.662 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 345,547 | 3.455 | 20 | 20 | fits | 96,279 | 151 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 299,656 | 2.997 | 20 | 200 | fits | 150,441 | 237 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 395,319 | 3.953 | 20 | 200 | fits | 96,279 | 151 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 300,580 | 3.006 | 20 | 20 | fits | 150,441 | 237 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 396,023 | 3.960 | 20 | 20 | fits | 96,279 | 151 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 153,779 | 1.538 | 20 | 24 | fits | 151,895 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 303,230 | 3.032 | 20 | 24 | fits | 150,441 | 237 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 303,164 | 3.032 | 20 | 50 | fits | 150,441 | 237 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 399,047 | 3.990 | 20 | 50 | fits | 96,279 | 151 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 488,235 | 4.882 | 20 | 20 | fits | 89,254 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,064,267 | 10.643 | 20 | 20 | fits | 72,719 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 341,514 | 3.415 | 20 | 20 | fits | 99,266 | 142 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 298,903 | 2.989 | 20 | 200 | fits | 148,062 | 248 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 397,553 | 3.976 | 20 | 200 | fits | 99,266 | 142 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 299,827 | 2.998 | 20 | 20 | fits | 148,062 | 248 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 398,257 | 3.983 | 20 | 20 | fits | 99,266 | 142 | 0.416 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 155,405 | 1.554 | 20 | 24 | fits | 152,235 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 302,477 | 3.025 | 20 | 24 | fits | 148,062 | 248 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 302,411 | 3.024 | 20 | 50 | fits | 148,062 | 248 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 401,281 | 4.013 | 20 | 50 | fits | 99,266 | 142 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 482,864 | 4.829 | 20 | 20 | fits | 81,649 | 26 | 0.830 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,063,983 | 10.640 | 20 | 20 | fits | 85,270 | 28 | 0.617 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 347,768 | 3.478 | 20 | 20 | fits | 103,042 | 148 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 293,653 | 2.937 | 20 | 200 | fits | 149,528 | 254 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 404,394 | 4.044 | 20 | 200 | fits | 103,042 | 148 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 294,577 | 2.946 | 20 | 20 | fits | 149,528 | 254 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 405,098 | 4.051 | 20 | 20 | fits | 103,042 | 148 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 148,689 | 1.487 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 297,227 | 2.972 | 20 | 24 | fits | 149,528 | 254 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 297,161 | 2.972 | 20 | 50 | fits | 149,528 | 254 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 408,122 | 4.081 | 20 | 50 | fits | 103,042 | 148 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 496,693 | 4.967 | 20 | 20 | fits | 88,637 | 30 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,062,597 | 10.626 | 20 | 20 | fits | 59,793 | 21 | 0.694 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 343,722 | 3.437 | 20 | 20 | fits | 96,666 | 151 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 297,641 | 2.976 | 20 | 200 | fits | 152,018 | 242 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 393,691 | 3.937 | 20 | 200 | fits | 96,666 | 151 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 298,565 | 2.986 | 20 | 20 | fits | 152,018 | 242 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 394,395 | 3.944 | 20 | 20 | fits | 96,666 | 151 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 150,187 | 1.502 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 301,215 | 3.012 | 20 | 24 | fits | 152,018 | 242 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 301,149 | 3.011 | 20 | 50 | fits | 152,018 | 242 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 397,419 | 3.974 | 20 | 50 | fits | 96,666 | 151 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 486,517 | 4.865 | 20 | 20 | fits | 89,164 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 987,271 | 9.873 | 20 | 20 | fits | 72,855 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 361,679 | 3.617 | 20 | 20 | fits | 106,290 | 166 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 304,844 | 3.048 | 20 | 200 | fits | 151,191 | 238 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 410,518 | 4.105 | 20 | 200 | fits | 106,290 | 166 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 305,768 | 3.058 | 20 | 20 | fits | 151,191 | 238 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 411,222 | 4.112 | 20 | 20 | fits | 106,290 | 166 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 150,346 | 1.503 | 20 | 24 | fits | 152,546 | 153 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 308,418 | 3.084 | 20 | 24 | fits | 151,191 | 238 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 308,352 | 3.084 | 20 | 50 | fits | 151,191 | 238 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 414,246 | 4.142 | 20 | 50 | fits | 106,290 | 166 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 575,604 | 5.756 | 20 | 20 | fits | 83,852 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,078,287 | 10.783 | 20 | 20 | fits | 74,969 | 25 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 353,638 | 3.536 | 20 | 20 | fits | 108,091 | 164 | 0.481 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 300,518 | 3.005 | 20 | 200 | fits | 150,622 | 238 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 416,508 | 4.165 | 20 | 200 | fits | 108,091 | 164 | 0.481 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 301,442 | 3.014 | 20 | 20 | fits | 150,622 | 238 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 417,212 | 4.172 | 20 | 20 | fits | 108,091 | 164 | 0.481 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 154,460 | 1.545 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 304,092 | 3.041 | 20 | 24 | fits | 150,622 | 238 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 304,026 | 3.040 | 20 | 50 | fits | 150,622 | 238 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 420,236 | 4.202 | 20 | 50 | fits | 108,091 | 164 | 0.481 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 504,103 | 5.041 | 20 | 20 | fits | 83,933 | 24 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 989,156 | 9.892 | 20 | 20 | fits | 59,783 | 20 | 0.698 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 77,284 | 0.773 | 20 | 20 | fits | 28,540 | 8 | 0.769 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 42,979 | 0.430 | 20 | 20 | fits | 43,045 | 12 | 0.891 |
| malformed MRPDU discard | `srp.malformed.if0` | 22,140 | 0.221 | 20 | 20 | fits | 22,206 | 12 | 0.740 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 86,699 | 0.867 | 220 | 220 | fits | 57,281 | 6 | 0.899 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,511 | 0.055 | 20 | 20 | fits | 24,161 | 13 (29) | 0.801 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,750 | 0.077 | 20 | 20 | fits | 26,938 | 19 (35) | 0.809 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 9,566 | 0.096 | 20 | 20 | fits | 29,865 | 21 (12) | 0.823 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 147,482 | 1.475 | 20 | 24 | fits | 150,533 | 98 | 0.339 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 310,413 | 3.104 | 20 | 24 | fits | 136,972 | 70 | 0.301 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 210,476 | 2.105 | 20 | 24 | fits | 41,517 | 17 | 0.685 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 393,590 | 3.936 | 20 | 24 | fits | 100,444 | 33 | 0.682 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 318,408 | 3.184 | 20 | 24 | fits | 92,854 | 17 | 0.659 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

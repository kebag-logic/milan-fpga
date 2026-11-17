### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 23 paths and 0 of 133 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.191 (0.415) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.201 (0.579) | fits | 0 adp | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.207 (0.643) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.026 (0.259) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `fixture.link_up.if0` (fixture) | 0.027 (0.267) | fits | 0 events | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.092 (5.562) | fits | 7 adp | 10 | 0 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.316 (0.468) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.202 (0.546) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.090 (0.223) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.100 (0.267) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.180 (0.546) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.163 (0.490) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 3.675 | fits | 0 acmp | 11 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 4.660 | fits | 11 acmp | 11 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 3.666 | fits | 0 adp | 11 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.653 | fits | 7 adp | 11 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.230 | fits | 0 aecp | 11 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.aecp.last.if0` (backlog-adp@blank-0) | 3.702 | fits | 15 aecp | 11 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 3.701 | fits | 0 maap | 11 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.690 | fits | 6 maap | 11 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 5.895 | fits | 0 srp | 11 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.srp.last.if0` (backlog-adp@program-aged2-6) | 10.911 | fits | 31 srp | 11 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.227 (0.228) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.892 | 11 | 153,248 (1.532) | yes | - |
| backlog-adp@blank-6 | 0 | 11.177 | 10 | 147,268 (1.473) | yes | - |
| backlog-adp@program-6 | 0 | 10.581 | 11 | 152,479 (1.525) | yes | - |
| backlog-adp@verify-6 | 0 | 11.236 | 11 | 152,846 (1.528) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.683 | 13 | 151,895 (1.519) | yes | - |
| backlog-adp@blank-aged1-6 | 1 | 11.875 | 11 | 152,017 (1.520) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.442 | 12 | 152,441 (1.524) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 11.768 | 13 | 152,316 (1.523) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.302 | 11 | 152,485 (1.525) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.295 | 11 | 151,191 (1.512) | yes | - |
| fixture | 0 | 1.284 | 2 | 79,117 (0.791) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 416 | 0 | 153,248 (1.532) | fits |
| backlog-adp@blank-6 | 418 | 0 | 149,076 (1.491) | fits |
| backlog-adp@program-6 | 524 | 0 | 152,479 (1.525) | fits |
| backlog-adp@verify-6 | 616 | 0 | 152,846 (1.528) | fits |
| backlog-adp@blank-aged2-6 | 742 | 0 | 151,895 (1.519) | fits |
| backlog-adp@blank-aged1-6 | 684 | 0 | 152,235 (1.522) | fits |
| backlog-adp@program-aged2-6 | 841 | 0 | 152,441 (1.524) | fits |
| backlog-adp@program-aged1-6 | 784 | 0 | 152,316 (1.523) | fits |
| backlog-adp@verify-aged2-6 | 937 | 0 | 152,485 (1.525) | fits |
| backlog-adp@verify-aged1-6 | 879 | 0 | 152,619 (1.526) | fits |
| maap | 182 | 0 | 30,145 (0.301) | fits |
| fixture | 151 | 0 | 79,117 (0.791) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-6 | 2 | +4.308 ms, 76,816 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 10.735 (20) | 9.265 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.582 (20) | 9.418 |
| backlog-adp@program-aged2-6 | 2 | +4.273 ms, 80,296 (0.803 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.911 (20) | 9.089 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.971 (20) | 10.029 |
| backlog-adp@verify-aged2-6 | 2 | +4.161 ms, 77,572 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.770 (20) | 9.230 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.000 (20) | 10.000 |

Least margin over the aged windows: 9.089 ms, `backlog-adp@program-aged2-6.service.srp.last.if0` at 10.911 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 299 | 92,807 (0.928) | 76,336 (0.763) |
| backlog-adp@blank-6 | 299 | 92,719 (0.927) | 76,173 (0.762) |
| backlog-adp@program-6 | 329 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-6 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@blank-aged2-6 | 297 | 76,816 (0.768) | 75,641 (0.756) |
| backlog-adp@blank-aged1-6 | 297 | 93,046 (0.930) | 76,174 (0.762) |
| backlog-adp@program-aged2-6 | 326 | 96,381 (0.964) | 78,235 (0.782) |
| backlog-adp@program-aged1-6 | 326 | 96,793 (0.968) | 78,813 (0.788) |
| backlog-adp@verify-aged2-6 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-aged1-6 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| maap | 169 | 22,268 (0.223) | 2,242 (0.022) |
| fixture | 54 | 19,964 (0.200) | 2,242 (0.022) |

Longest pass that carries a step: 96,793 CPU cycles (0.968 ms), backlog-adp@program-aged1-6; longest step: 78,813 (0.788 ms), backlog-adp@program-aged1-6.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 409,183 | 4.092 | 20 | 20 | fits | 99,335 | 142 | 0.416 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 366,589 | 3.666 | 20 | 200 | fits | 148,155 | 248 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 465,308 | 4.653 | 20 | 200 | fits | 99,335 | 142 | 0.416 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 367,513 | 3.675 | 20 | 20 | fits | 148,155 | 248 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 466,012 | 4.660 | 20 | 20 | fits | 99,335 | 142 | 0.416 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 222,998 | 2.230 | 20 | 24 | fits | 153,248 | 155 | 0.396 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 370,163 | 3.702 | 20 | 24 | fits | 148,155 | 248 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 370,097 | 3.701 | 20 | 50 | fits | 148,155 | 248 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 469,036 | 4.690 | 20 | 50 | fits | 99,335 | 142 | 0.416 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 553,285 | 5.533 | 20 | 20 | fits | 84,315 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,060,212 | 10.602 | 20 | 20 | fits | 78,754 | 30 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 342,636 | 3.426 | 20 | 20 | fits | 109,710 | 177 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 290,419 | 2.904 | 20 | 200 | fits | 147,268 | 258 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 399,513 | 3.995 | 20 | 200 | fits | 109,710 | 177 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 291,343 | 2.913 | 20 | 20 | fits | 147,268 | 258 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 400,217 | 4.002 | 20 | 20 | fits | 109,710 | 177 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 147,715 | 1.477 | 20 | 24 | fits | 149,076 | 114 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 293,993 | 2.940 | 20 | 24 | fits | 147,268 | 258 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 293,927 | 2.939 | 20 | 50 | fits | 147,268 | 258 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 403,241 | 4.032 | 20 | 50 | fits | 109,710 | 177 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 487,683 | 4.877 | 20 | 20 | fits | 84,508 | 24 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 988,941 | 9.889 | 20 | 20 | fits | 72,754 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 350,233 | 3.502 | 20 | 20 | fits | 100,278 | 142 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 307,106 | 3.071 | 20 | 200 | fits | 148,014 | 248 | 0.383 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 406,768 | 4.068 | 20 | 200 | fits | 100,278 | 142 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 308,030 | 3.080 | 20 | 20 | fits | 148,014 | 248 | 0.383 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 407,472 | 4.075 | 20 | 20 | fits | 100,278 | 142 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 163,656 | 1.637 | 20 | 24 | fits | 152,479 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 310,680 | 3.107 | 20 | 24 | fits | 148,014 | 248 | 0.383 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 310,614 | 3.106 | 20 | 50 | fits | 148,014 | 248 | 0.383 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 410,496 | 4.105 | 20 | 50 | fits | 100,278 | 142 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 499,698 | 4.997 | 20 | 20 | fits | 89,268 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,000,367 | 10.004 | 20 | 20 | fits | 72,855 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 346,587 | 3.466 | 20 | 20 | fits | 105,229 | 163 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 298,657 | 2.987 | 20 | 200 | fits | 149,159 | 231 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 403,270 | 4.033 | 20 | 200 | fits | 105,229 | 163 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 299,581 | 2.996 | 20 | 20 | fits | 149,159 | 231 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 403,974 | 4.040 | 20 | 20 | fits | 105,229 | 163 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 154,062 | 1.541 | 20 | 24 | fits | 152,846 | 155 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 302,231 | 3.022 | 20 | 24 | fits | 149,159 | 231 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 302,165 | 3.022 | 20 | 50 | fits | 149,159 | 231 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 406,998 | 4.070 | 20 | 50 | fits | 105,229 | 163 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 491,219 | 4.912 | 20 | 20 | fits | 84,287 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 994,018 | 9.940 | 20 | 20 | fits | 72,829 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 368,561 | 3.686 | 20 | 20 | fits | 110,201 | 155 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 307,304 | 3.073 | 20 | 200 | fits | 147,937 | 249 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 425,384 | 4.254 | 20 | 200 | fits | 110,201 | 155 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 308,228 | 3.082 | 20 | 20 | fits | 147,937 | 249 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 426,088 | 4.261 | 20 | 20 | fits | 110,201 | 155 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 163,931 | 1.639 | 20 | 24 | fits | 151,895 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 310,878 | 3.109 | 20 | 24 | fits | 147,937 | 249 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 310,812 | 3.108 | 20 | 50 | fits | 147,937 | 249 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 429,112 | 4.291 | 20 | 50 | fits | 110,201 | 155 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 588,880 | 5.889 | 20 | 20 | fits | 83,018 | 25 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,073,462 | 10.735 | 20 | 20 | fits | 59,743 | 20 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 346,207 | 3.462 | 20 | 20 | fits | 112,906 | 157 | 0.504 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 297,567 | 2.976 | 20 | 200 | fits | 152,017 | 242 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 409,857 | 4.099 | 20 | 200 | fits | 112,906 | 157 | 0.504 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 298,491 | 2.985 | 20 | 20 | fits | 152,017 | 242 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 410,561 | 4.106 | 20 | 20 | fits | 112,906 | 157 | 0.504 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 150,114 | 1.501 | 20 | 24 | fits | 152,235 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 301,141 | 3.011 | 20 | 24 | fits | 152,017 | 242 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 301,075 | 3.011 | 20 | 50 | fits | 152,017 | 242 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 413,585 | 4.136 | 20 | 50 | fits | 112,906 | 157 | 0.504 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 526,248 | 5.262 | 20 | 20 | fits | 83,189 | 26 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,058,207 | 10.582 | 20 | 20 | fits | 72,793 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 364,631 | 3.646 | 20 | 20 | fits | 111,366 | 166 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 311,186 | 3.112 | 20 | 200 | fits | 146,515 | 235 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 421,936 | 4.219 | 20 | 200 | fits | 111,366 | 166 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 312,110 | 3.121 | 20 | 20 | fits | 146,515 | 235 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 422,640 | 4.226 | 20 | 20 | fits | 111,366 | 166 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 161,414 | 1.614 | 20 | 24 | fits | 152,441 | 153 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 314,760 | 3.148 | 20 | 24 | fits | 146,515 | 235 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 314,694 | 3.147 | 20 | 50 | fits | 146,515 | 235 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 425,664 | 4.257 | 20 | 50 | fits | 111,366 | 166 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 589,505 | 5.895 | 20 | 20 | fits | 83,611 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,091,114 | 10.911 | 20 | 20 | fits | 73,068 | 24 | 0.662 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 367,865 | 3.679 | 20 | 20 | fits | 110,420 | 155 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 306,782 | 3.068 | 20 | 200 | fits | 148,154 | 249 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 424,901 | 4.249 | 20 | 200 | fits | 110,420 | 155 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 307,706 | 3.077 | 20 | 20 | fits | 148,154 | 249 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 425,605 | 4.256 | 20 | 20 | fits | 110,420 | 155 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 163,192 | 1.632 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 310,356 | 3.104 | 20 | 24 | fits | 148,154 | 249 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 310,290 | 3.103 | 20 | 50 | fits | 148,154 | 249 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 428,629 | 4.286 | 20 | 50 | fits | 110,420 | 155 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 512,149 | 5.121 | 20 | 20 | fits | 83,586 | 24 | 0.780 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 997,127 | 9.971 | 20 | 20 | fits | 59,783 | 20 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 354,207 | 3.542 | 20 | 20 | fits | 107,284 | 148 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 304,090 | 3.041 | 20 | 200 | fits | 147,844 | 248 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 410,758 | 4.108 | 20 | 200 | fits | 107,284 | 148 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 305,014 | 3.050 | 20 | 20 | fits | 147,844 | 248 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 411,462 | 4.115 | 20 | 20 | fits | 107,284 | 148 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 160,810 | 1.608 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 307,664 | 3.077 | 20 | 24 | fits | 147,844 | 248 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 307,598 | 3.076 | 20 | 50 | fits | 147,844 | 248 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 414,486 | 4.145 | 20 | 50 | fits | 107,284 | 148 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 575,931 | 5.759 | 20 | 20 | fits | 83,939 | 25 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,076,977 | 10.770 | 20 | 20 | fits | 72,898 | 24 | 0.656 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 361,236 | 3.612 | 20 | 20 | fits | 106,249 | 166 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 304,442 | 3.044 | 20 | 200 | fits | 151,191 | 238 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 410,075 | 4.101 | 20 | 200 | fits | 106,249 | 166 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 305,366 | 3.054 | 20 | 20 | fits | 151,191 | 238 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 410,779 | 4.108 | 20 | 20 | fits | 106,249 | 166 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 149,994 | 1.500 | 20 | 24 | fits | 152,619 | 153 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 308,016 | 3.080 | 20 | 24 | fits | 151,191 | 238 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 307,950 | 3.079 | 20 | 50 | fits | 151,191 | 238 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 413,803 | 4.138 | 20 | 50 | fits | 106,249 | 166 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 497,956 | 4.980 | 20 | 20 | fits | 84,219 | 24 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,000,033 | 10.000 | 20 | 20 | fits | 65,563 | 27 | 0.756 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 9,981 | 0.100 | 20 | 50 | fits | 26,711 | 43 | 0.737 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 11,595 | 0.116 | 20 | 50 | fits | 23,748 | 35 | 0.733 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 16,322 | 0.163 | 20 | 50 | fits | 23,697 | 35 | 0.735 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 18,036 | 0.180 | 20 | 50 | fits | 28,473 | 61 | 0.656 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 20,193 | 0.202 | 20 | 50 | fits | 28,473 | 61 | 0.656 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,964 | 0.090 | 20 | 50 | fits | 22,278 | 30 | 0.664 |
| LINK_UP | `fixture.link_up.if0` | 2,674 | 0.027 | 20 | 200 | fits | 26,711 | 43 (11) | 0.737 |
| malformed MRPDU discard | `fixture.malformed.if0` | 22,685 | 0.227 | 20 | 20 | fits | 22,751 | 12 | 0.770 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 31,574 | 0.316 | 20 | 24 | fits | 46,750 | 43 | 0.785 |
| LINK_DOWN | `fixture.link_down.if0` | 2,613 | 0.026 | 20 | 200 | fits | 25,850 | 23 (9) | 0.784 |
| BIND_RX | `fixture.bind_rx.if0` | 19,115 | 0.191 | 20 | 20 | fits | 41,454 | 26 (77) | 0.804 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 20,737 | 0.207 | 20 | 20 | fits | 36,764 | 29 (35) | 0.794 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 20,096 | 0.201 | 20 | 20 | fits | 25,951 | 13 (29) | 0.830 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 79,013 | 0.790 | 20 | 200 | fits | 79,117 | 49 | 0.751 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 79,013 | 0.790 | 20 | 200 | fits | 79,117 | 49 | 0.751 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 78,739 | 0.787 | 20 | 20 | fits | 79,117 | 49 | 0.751 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 78,739 | 0.787 | 20 | 20 | fits | 79,117 | 49 | 0.751 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 78,947 | 0.789 | 20 | 24 | fits | 79,117 | 49 | 0.751 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 78,947 | 0.789 | 20 | 24 | fits | 79,117 | 49 | 0.751 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 78,881 | 0.789 | 20 | 50 | fits | 79,117 | 49 | 0.751 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 78,881 | 0.789 | 20 | 50 | fits | 79,117 | 49 | 0.751 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 78,815 | 0.788 | 20 | 20 | fits | 79,117 | 49 | 0.751 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 78,815 | 0.788 | 20 | 20 | fits | 79,117 | 49 | 0.751 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

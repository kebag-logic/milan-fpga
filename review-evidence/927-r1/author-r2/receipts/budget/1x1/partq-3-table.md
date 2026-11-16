### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 24 paths and 0 of 59 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.024 (0.249) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.026 (0.271) | fits | 0 events | 2 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.095 (0.260) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.095 (0.424) | fits | 0 events | 2 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.670 (2.995) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.405 (0.509) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.507 (0.833) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.440 (0.572) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.481 (0.771) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.520 (0.860) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.254 (3.581) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.453 (0.743) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged1-0.adp_available.if0` (backlog-adp@verify-aged1-0) | 3.674 (4.283) | fits | 7 adp | 3 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.156 (0.522) | fits | 0 adp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-0.service.acmp.first.if0` (backlog-adp@verify-aged1-0) | 3.203 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-0.service.acmp.last.if0` (backlog-adp@verify-aged1-0) | 4.177 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-0.service.adp.first.if0` (backlog-adp@verify-aged1-0) | 3.193 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-0.service.adp.last.if0` (backlog-adp@verify-aged1-0) | 4.169 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-0.service.aecp.first.if0` (backlog-adp@verify-aged1-0) | 1.632 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-0.service.aecp.last.if0` (backlog-adp@verify-aged1-0) | 3.229 | fits | 15 aecp | 4 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-0.service.maap.first.if0` (backlog-adp@verify-aged1-0) | 3.228 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-0.service.maap.last.if0` (backlog-adp@verify-aged1-0) | 4.207 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-0.service.srp.first.if0` (backlog-adp@verify-aged1-0) | 5.069 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-4.service.srp.last.if0` (backlog-adp@verify-aged2-4) | 10.828 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@verify-aged2-4 | 1 | 11.362 | 11 | 151,495 (1.515) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.450 | 12 | 152,267 (1.523) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.269 | 11 | 152,317 (1.523) | yes | - |
| backlog-adp-refill | 0 | 40.846 | 26 | 152,335 (1.523) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-owed not run): 152,335 CPU cycles (1.523 ms), backlog-adp-refill.
Over the windows that released their whole load only: 152,335 (1.523 ms), backlog-adp-refill.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@verify-aged2-4 | 923 | 0 | 152,346 (1.523) | fits |
| backlog-adp@verify-aged1-0 | 836 | 0 | 152,267 (1.523) | fits |
| backlog-adp@verify-aged1-4 | 864 | 0 | 152,317 (1.523) | fits |
| adp-advertise | 598 | 0 | 30,305 (0.303) | fits |
| save | 610 | 0 | 45,514 (0.455) | fits |
| backlog-adp-refill | 330 | 0 | 152,335 (1.523) | fits |
| adp-link | 89 | 0 | 39,548 (0.395) | fits |
| aecp-fanout | 112 | 0 | 67,866 (0.679) | fits |
| datapath-events | 116 | 0 | 30,305 (0.303) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@verify-aged2-4 | 2 | +5.776 ms, 77,375 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.828 (20) | 9.172 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.031 (20) | 9.969 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.974 (20) | 10.026 |

Least margin over the aged windows: 9.172 ms, `backlog-adp@verify-aged2-4.service.srp.last.if0` at 10.828 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save | 2019.618 | 4,070 | 102 | - | 10.875 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@verify-aged2-4 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-0 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-4 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| adp-advertise | 577 | 22,507 (0.225) | 2,414 (0.024) |
| save | 585 | 96,547 (0.965) | 78,190 (0.782) |
| backlog-adp-refill | 274 | 22,507 (0.225) | 2,414 (0.024) |
| adp-link | 79 | 22,267 (0.223) | 2,414 (0.024) |
| aecp-fanout | 80 | 23,660 (0.237) | 3,978 (0.040) |
| datapath-events | 69 | 22,267 (0.223) | 2,414 (0.024) |

Longest pass that carries a step: 96,998 CPU cycles (0.970 ms), backlog-adp@verify-aged2-4; longest step: 78,341 (0.783 ms), backlog-adp@verify-aged2-4.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 356,850 | 3.568 | 20 | 20 | fits | 101,245 | 160 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 306,058 | 3.061 | 20 | 200 | fits | 151,495 | 238 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 406,687 | 4.067 | 20 | 200 | fits | 101,245 | 160 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 306,982 | 3.070 | 20 | 20 | fits | 151,495 | 238 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 407,391 | 4.074 | 20 | 20 | fits | 101,245 | 160 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 150,207 | 1.502 | 20 | 24 | fits | 152,346 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 309,632 | 3.096 | 20 | 24 | fits | 151,495 | 238 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 309,566 | 3.096 | 20 | 50 | fits | 151,495 | 238 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 410,415 | 4.104 | 20 | 50 | fits | 101,245 | 160 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 496,715 | 4.967 | 20 | 20 | fits | 86,366 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,082,836 | 10.828 | 20 | 20 | fits | 77,894 | 31 | 0.724 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 367,445 | 3.674 | 20 | 20 | fits | 98,235 | 154 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 319,330 | 3.193 | 20 | 200 | fits | 151,759 | 238 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 416,949 | 4.169 | 20 | 200 | fits | 98,235 | 154 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 320,254 | 3.203 | 20 | 20 | fits | 151,759 | 238 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 417,653 | 4.177 | 20 | 20 | fits | 98,235 | 154 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 163,215 | 1.632 | 20 | 24 | fits | 152,267 | 153 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 322,904 | 3.229 | 20 | 24 | fits | 151,759 | 238 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 322,838 | 3.228 | 20 | 50 | fits | 151,759 | 238 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 420,677 | 4.207 | 20 | 50 | fits | 98,235 | 154 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 506,941 | 5.069 | 20 | 20 | fits | 86,330 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,003,067 | 10.031 | 20 | 20 | fits | 70,124 | 33 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 338,080 | 3.381 | 20 | 20 | fits | 98,582 | 152 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 303,756 | 3.038 | 20 | 200 | fits | 151,306 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 401,722 | 4.017 | 20 | 200 | fits | 98,582 | 152 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 304,680 | 3.047 | 20 | 20 | fits | 151,306 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 402,426 | 4.024 | 20 | 20 | fits | 98,582 | 152 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 157,014 | 1.570 | 20 | 24 | fits | 152,317 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 307,330 | 3.073 | 20 | 24 | fits | 151,306 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 307,264 | 3.073 | 20 | 50 | fits | 151,306 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 405,450 | 4.054 | 20 | 50 | fits | 98,582 | 152 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 504,092 | 5.041 | 20 | 20 | fits | 89,205 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 997,410 | 9.974 | 20 | 20 | fits | 73,137 | 24 | 0.673 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 9,457 | 0.095 | 20 | 200 | fits | 2,669 | 10 (11) | 0.571 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,632 | 0.156 | 20 | 20 | fits | 27,557 | 19 | 0.821 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 297,517 | 2.975 | 20 | 200 | fits | 149,932 | 234 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 35,156 | 0.352 | 20 | 200 | fits | 27,557 | 19 | 0.821 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 298,441 | 2.984 | 20 | 20 | fits | 149,932 | 234 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 400,263 | 4.003 | 20 | 20 | fits | 93,301 | 151 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 152,149 | 1.521 | 20 | 24 | fits | 152,335 | 155 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 301,091 | 3.011 | 20 | 24 | fits | 149,932 | 234 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 301,025 | 3.010 | 20 | 50 | fits | 149,932 | 234 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 403,287 | 4.033 | 20 | 50 | fits | 93,301 | 151 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 489,065 | 4.891 | 20 | 20 | fits | 85,844 | 24 | 0.791 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 982,244 | 9.822 | 20 | 20 | fits | 73,132 | 24 | 0.673 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| LINK_DOWN | `adp.link_down.if0` | 2,352 | 0.024 | 20 | 200 | fits | 24,885 | 23 (9) | 0.787 |
| set_name | `aecp_fanout.set_name.if0` | 52,028 | 0.520 | 20 | 24 | fits | 67,866 | 95 | 0.596 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 43,991 | 0.440 | 20 | 24 | fits | 57,203 | 78 | 0.607 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 48,131 | 0.481 | 20 | 24 | fits | 54,975 | 79 | 0.567 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,928 | 0.409 | 20 | 24 | fits | 51,498 | 78 | 0.558 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 50,661 | 0.507 | 20 | 24 | fits | 61,126 | 66 | 0.642 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 267,027 | 2.670 | 20 | 24 | fits | 59,166 | 65 | 0.641 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 325,444 | 3.254 | 20 | 24 | fits | 54,632 | 67 | 0.603 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 40,461 | 0.405 | 20 | 24 | fits | 50,904 | 78 | 0.556 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,319 | 0.453 | 20 | 24 | fits | 50,939 | 79 | 0.553 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

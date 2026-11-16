### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 50 paths and 0 of 93 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.081 (0.266) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.059 (0.247) | fits | 0 adp | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.127 (0.490) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.046 (0.172) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-discover) | 0.026 (0.271) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-discover) | 0.095 (0.424) | fits | 0 events | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.275 (0.591) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.269 (0.588) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.118 (0.433) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.151 (0.469) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.256 (0.587) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.188 (0.549) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.159 (0.465) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.192 (0.519) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.259 (0.580) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.255 (0.573) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.143 (0.464) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.277 (0.594) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.134 (0.456) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.135 (0.456) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.151 (0.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.252 (0.569) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.152 (0.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.255 (0.576) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.262 (0.580) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.263 (0.590) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.141 (0.462) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.249 (0.563) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.216 (0.640) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.128 (0.444) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.159 (0.369) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.992 (4.215) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged1-6.adp_available.if0` (backlog-adp@verify-aged1-6) | 3.574 (4.390) | fits | 7 adp | 4 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.702 (2.127) | fits | 15 events | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.012 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 1.577 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.869 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.294 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.921 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.655 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.169 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-6.service.acmp.last.if0` (backlog-adp@verify-aged1-6) | 4.294 | fits | 11 acmp | 5 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.213 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-6.service.adp.last.if0` (backlog-adp@verify-aged1-6) | 4.287 | fits | 7 adp | 5 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged1-6.service.aecp.first.if0` (backlog-adp@verify-aged1-6) | 1.646 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.196 | fits | 15 aecp | 5 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.195 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-aged1-6.service.maap.last.if0` (backlog-adp@verify-aged1-6) | 4.324 | fits | 6 maap | 5 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.srp.first.if0` (backlog-adp@verify-aged2-6) | 5.756 | fits | 0 srp | 5 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.srp.last.if0` (backlog-adp@verify-aged2-6) | 10.786 | fits | 31 srp | 5 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@verify-aged2-0 | 0 | 11.263 | 12 | 152,135 (1.521) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.317 | 11 | 152,364 (1.524) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 11.249 | 10 | 146,555 (1.466) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.498 | 12 | 152,532 (1.525) | yes | - |
| backlog | 0 | 5.629 | 7 | 156,321 (1.563) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 156,321 CPU cycles (1.563 ms), backlog.
Over the windows that released their whole load only: 156,321 (1.563 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@verify-aged2-0 | 894 | 0 | 152,135 (1.521) | fits |
| backlog-adp@verify-aged2-6 | 937 | 0 | 152,364 (1.524) | fits |
| backlog-adp@verify-aged1-2 | 849 | 0 | 152,364 (1.524) | fits |
| backlog-adp@verify-aged1-6 | 880 | 0 | 152,532 (1.525) | fits |
| save-starved | 23468 | 0 | 158,615 (1.586) | fits |
| backlog | 286 | 0 | 156,321 (1.563) | fits |
| acmp-disc | 937 | 0 | 41,470 (0.415) | fits |
| adp-discover | 88 | 0 | 30,305 (0.303) | fits |
| aecp | 111 | 0 | 44,645 (0.446) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@verify-aged2-0 | 2 | none | +10.151 ms, 77,343 (0.773 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.910 (20) | 10.090 |
| backlog-adp@verify-aged2-6 | 2 | +4.140 ms, 77,749 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.786 (20) | 9.214 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.954 (20) | 10.046 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.203 (20) | 9.797 |

Least margin over the aged windows: 9.214 ms, `backlog-adp@verify-aged2-6.service.srp.last.if0` at 10.786 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 4049.131 | 4,070 | 102 | - | 31.117 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@verify-aged2-0 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged2-6 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-2 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| backlog-adp@verify-aged1-6 | 355 | 96,998 (0.970) | 78,341 (0.783) |
| save-starved | 418 | 80,927 (0.809) | 78,361 (0.784) |
| backlog | 265 | 22,507 (0.225) | 2,414 (0.024) |
| acmp-disc | 305 | 97,227 (0.972) | 78,205 (0.782) |
| adp-discover | 79 | 22,267 (0.223) | 2,414 (0.024) |
| aecp | 79 | 22,267 (0.223) | 2,414 (0.024) |

Longest pass that carries a step: 97,227 CPU cycles (0.972 ms), acmp-disc; longest step: 78,361 (0.784 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 341,031 | 3.410 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 298,160 | 2.982 | 20 | 200 | fits | 148,545 | 248 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 398,117 | 3.981 | 20 | 200 | fits | 100,573 | 142 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 299,084 | 2.991 | 20 | 20 | fits | 148,545 | 248 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 398,821 | 3.988 | 20 | 20 | fits | 100,573 | 142 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 154,179 | 1.542 | 20 | 24 | fits | 152,135 | 152 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 301,734 | 3.017 | 20 | 24 | fits | 148,545 | 248 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 301,668 | 3.017 | 20 | 50 | fits | 148,545 | 248 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 401,845 | 4.018 | 20 | 50 | fits | 100,573 | 142 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 487,971 | 4.880 | 20 | 20 | fits | 86,192 | 24 | 0.789 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 990,980 | 9.910 | 20 | 20 | fits | 73,340 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 357,425 | 3.574 | 20 | 20 | fits | 105,453 | 157 | 0.477 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 303,797 | 3.038 | 20 | 200 | fits | 151,347 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 408,634 | 4.086 | 20 | 200 | fits | 105,453 | 157 | 0.477 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 304,721 | 3.047 | 20 | 20 | fits | 151,347 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 409,338 | 4.093 | 20 | 20 | fits | 105,453 | 157 | 0.477 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 157,014 | 1.570 | 20 | 24 | fits | 152,364 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 307,371 | 3.074 | 20 | 24 | fits | 151,347 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 307,305 | 3.073 | 20 | 50 | fits | 151,347 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 412,362 | 4.124 | 20 | 50 | fits | 105,453 | 157 | 0.477 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 575,553 | 5.756 | 20 | 20 | fits | 85,508 | 25 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,078,567 | 10.786 | 20 | 20 | fits | 73,340 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 325,715 | 3.257 | 20 | 20 | fits | 105,699 | 160 | 0.446 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 291,712 | 2.917 | 20 | 200 | fits | 146,555 | 235 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 396,795 | 3.968 | 20 | 200 | fits | 105,699 | 160 | 0.446 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 292,636 | 2.926 | 20 | 20 | fits | 146,555 | 235 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 397,499 | 3.975 | 20 | 20 | fits | 105,699 | 160 | 0.446 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 149,721 | 1.497 | 20 | 24 | fits | 152,364 | 152 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 295,286 | 2.953 | 20 | 24 | fits | 146,555 | 235 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 295,220 | 2.952 | 20 | 50 | fits | 146,555 | 235 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 400,523 | 4.005 | 20 | 50 | fits | 105,699 | 160 | 0.446 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 486,720 | 4.867 | 20 | 20 | fits | 86,263 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 995,391 | 9.954 | 20 | 20 | fits | 85,585 | 28 | 0.637 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 357,441 | 3.574 | 20 | 20 | fits | 113,527 | 166 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 315,797 | 3.158 | 20 | 200 | fits | 147,065 | 235 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 428,708 | 4.287 | 20 | 200 | fits | 113,527 | 166 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 316,721 | 3.167 | 20 | 20 | fits | 147,065 | 235 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 429,412 | 4.294 | 20 | 20 | fits | 113,527 | 166 | 0.474 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 164,569 | 1.646 | 20 | 24 | fits | 152,532 | 153 | 0.371 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 319,371 | 3.194 | 20 | 24 | fits | 147,065 | 235 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 319,305 | 3.193 | 20 | 50 | fits | 147,065 | 235 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 432,436 | 4.324 | 20 | 50 | fits | 113,527 | 166 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 518,696 | 5.187 | 20 | 20 | fits | 86,326 | 24 | 0.790 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,020,294 | 10.203 | 20 | 20 | fits | 65,483 | 27 | 0.762 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 157,675 | 1.577 | 20 | 200 | fits | 158,615 | 273 | 0.454 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 201,220 | 2.012 | 20 | 20 | fits | 145,683 | 267 | 0.365 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 286,904 | 2.869 | 20 | 24 | fits | 84,819 | 55 | 0.585 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 129,362 | 1.294 | 20 | 50 | fits | 33,558 | 43 | 0.681 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 992,122 | 9.921 | 20 | 20 | fits | 51,108 | 22 | 0.788 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 265,495 | 2.655 | 20 | 20 | fits | 0 | - | 0.000 |
| an event behind 15 others | `backlog.event.if0` | 170,222 | 1.702 | 20 | 200 | fits | 56,368 | 78 | 0.575 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 399,244 | 3.992 | 20 | 20 | fits | 148,870 | 167 | 0.396 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 421,260 | 4.213 | 20 | 200 | fits | 148,870 | 167 | 0.396 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 420,644 | 4.206 | 20 | 200 | fits | 148,870 | 167 | 0.396 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 416,938 | 4.169 | 20 | 20 | fits | 148,870 | 167 | 0.396 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 416,102 | 4.161 | 20 | 20 | fits | 148,870 | 167 | 0.396 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 155,430 | 1.554 | 20 | 24 | fits | 156,321 | 158 | 0.381 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 419,588 | 4.196 | 20 | 24 | fits | 148,870 | 167 | 0.396 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 419,522 | 4.195 | 20 | 50 | fits | 148,870 | 167 | 0.396 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 419,126 | 4.191 | 20 | 50 | fits | 148,870 | 167 | 0.396 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 450,436 | 4.504 | 20 | 20 | fits | 31,376 | 56 | 0.228 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 510,619 | 5.106 | 20 | 20 | fits | 24,668 | 41 | 0.192 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,929 | 0.059 | 20 | 20 | fits | 24,688 | 13 (29) | 0.809 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,148 | 0.081 | 20 | 20 | fits | 26,592 | 19 (35) | 0.808 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 12,734 | 0.127 | 20 | 20 | fits | 29,727 | 21 (12) | 0.822 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 27,119 | 43 (11) | 0.739 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 9,524 | 0.095 | 20 | 200 | fits | 23,107 | 23 (39) | 0.753 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,616 | 0.046 | 20 | 200 | fits | 17,250 | 16 (31) | 0.667 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 24,885 | 0.249 | 20 | 24 | fits | 27,993 | 20 | 0.776 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 19,218 | 0.192 | 20 | 24 | fits | 32,606 | 20 | 0.721 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 25,939 | 0.259 | 20 | 24 | fits | 27,588 | 20 | 0.734 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 15,103 | 0.151 | 20 | 24 | fits | 27,456 | 20 | 0.729 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 26,191 | 0.262 | 20 | 24 | fits | 27,741 | 20 | 0.726 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 26,259 | 0.263 | 20 | 24 | fits | 27,818 | 20 | 0.733 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,072 | 0.141 | 20 | 24 | fits | 26,739 | 20 | 0.729 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 25,532 | 0.255 | 20 | 24 | fits | 27,003 | 20 | 0.744 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,318 | 0.143 | 20 | 24 | fits | 26,387 | 20 | 0.746 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 27,710 | 0.277 | 20 | 24 | fits | 29,095 | 21 | 0.641 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 13,435 | 0.134 | 20 | 24 | fits | 26,088 | 20 | 0.762 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 13,516 | 0.135 | 20 | 24 | fits | 26,418 | 20 | 0.764 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 25,239 | 0.252 | 20 | 24 | fits | 26,624 | 20 | 0.727 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,156 | 0.152 | 20 | 24 | fits | 27,770 | 20 | 0.740 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 25,469 | 0.255 | 20 | 24 | fits | 27,108 | 20 | 0.744 |
| get_configuration | `aecp.get_configuration.if0` | 11,771 | 0.118 | 20 | 24 | fits | 24,044 | 20 | 0.736 |
| entity_available | `aecp.entity_available.if0` | 27,505 | 0.275 | 20 | 24 | fits | 28,898 | 26 | 0.731 |
| get_name | `aecp.get_name.if0` | 25,639 | 0.256 | 20 | 24 | fits | 27,284 | 20 | 0.747 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 15,098 | 0.151 | 20 | 24 | fits | 27,668 | 27 | 0.715 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 26,863 | 0.269 | 20 | 24 | fits | 28,601 | 29 | 0.758 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 12,759 | 0.128 | 20 | 24 | fits | 24,890 | 20 | 0.753 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 15,935 | 0.159 | 20 | 24 | fits | 24,058 | 20 | 0.727 |
| set_name | `aecp.set_name.if0` | 21,639 | 0.216 | 20 | 24 | fits | 44,645 | 43 | 0.765 |
| lock_entity | `aecp.lock_entity.if0` | 18,759 | 0.188 | 20 | 24 | fits | 35,606 | 34 | 0.779 |
| unlock_entity | `aecp.unlock_entity.if0` | 15,914 | 0.159 | 20 | 24 | fits | 36,897 | 33 | 0.779 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

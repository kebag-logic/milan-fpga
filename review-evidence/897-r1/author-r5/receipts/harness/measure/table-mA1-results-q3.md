### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 48 paths and 0 of 258 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.047 (0.159) | fits | 0 adp | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.021 (0.245) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-link) | 0.025 (0.257) | fits | 0 events | 2 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-link) | 0.087 (0.379) | fits | 0 events | 2 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.212 (0.501) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.153 (0.449) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.251 (0.546) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.129 (0.421) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.159 (0.455) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.237 (0.536) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.271 (0.659) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.208 (0.495) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.190 (0.488) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.233 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.235 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.144 (0.440) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.258 (0.550) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.142 (0.436) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.142 (0.437) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.149 (0.446) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.233 (0.526) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.155 (0.454) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.234 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.146 (0.450) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.241 (0.544) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.150 (0.443) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.128 (0.419) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.229 (0.623) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.217 (0.507) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.197 (0.533) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.234 (5.705) | fits | 7 adp | 19 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.100 (0.434) | fits | 0 adp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.193 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 1.525 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.894 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.798 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.373 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.506 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 3.775 | fits | 0 acmp | 20 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 4.822 | fits | 11 acmp | 20 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 3.766 | fits | 0 adp | 20 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.815 | fits | 7 adp | 20 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.373 | fits | 0 aecp | 20 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.aecp.last.if0` (backlog-adp@blank-0) | 3.802 | fits | 15 aecp | 20 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 3.801 | fits | 0 maap | 20 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.852 | fits | 6 maap | 20 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-6.service.srp.first.if0` (backlog-adp@blank-aged2-6) | 5.903 | fits | 0 srp | 20 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.srp.last.if0` (backlog-adp@verify-aged2-6) | 9.894 | fits | 31 srp | 20 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.248 | 11 | 150,277 (1.503) | yes | - |
| backlog-adp@blank-2 | 0 | 10.359 | 10 | 150,062 (1.501) | yes | - |
| backlog-adp@blank-6 | 0 | 10.618 | 12 | 150,160 (1.502) | yes | - |
| backlog-adp@program-2 | 0 | 10.378 | 10 | 149,664 (1.497) | yes | - |
| backlog-adp@program-6 | 0 | 9.585 | 10 | 149,460 (1.495) | yes | - |
| backlog-adp@verify-2 | 0 | 10.285 | 10 | 149,622 (1.496) | yes | - |
| backlog-adp@verify-6 | 0 | 10.365 | 10 | 149,539 (1.495) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.372 | 10 | 148,879 (1.489) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.286 | 10 | 149,137 (1.491) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.125 | 12 | 149,175 (1.492) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.088 | 11 | 150,229 (1.502) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 10.339 | 10 | 149,036 (1.490) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.250 | 10 | 149,036 (1.490) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.527 | 11 | 145,721 (1.457) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.325 | 10 | 149,055 (1.491) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.352 | 10 | 149,118 (1.491) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.375 | 11 | 148,618 (1.486) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.227 | 9 | 148,592 (1.486) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.295 | 10 | 149,099 (1.491) | yes | - |
| backlog-adp-refill | 0 | 40.718 | 24 | 150,154 (1.502) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-owed not run): 150,154 CPU cycles (1.502 ms), backlog-adp-refill.
Over the windows that released their whole load only: 150,154 (1.502 ms), backlog-adp-refill.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-0 | 407 | 0 | 150,277 (1.503) | fits |
| backlog-adp@blank-2 | 406 | 0 | 150,062 (1.501) | fits |
| backlog-adp@blank-6 | 408 | 0 | 150,160 (1.502) | fits |
| backlog-adp@program-2 | 504 | 0 | 149,664 (1.497) | fits |
| backlog-adp@program-6 | 507 | 0 | 149,460 (1.495) | fits |
| backlog-adp@verify-2 | 590 | 0 | 149,622 (1.496) | fits |
| backlog-adp@verify-6 | 592 | 0 | 149,539 (1.495) | fits |
| backlog-adp@blank-aged2-2 | 742 | 0 | 149,679 (1.497) | fits |
| backlog-adp@blank-aged2-6 | 775 | 0 | 149,137 (1.491) | fits |
| backlog-adp@blank-aged1-2 | 681 | 0 | 149,175 (1.492) | fits |
| backlog-adp@blank-aged1-6 | 714 | 0 | 150,229 (1.502) | fits |
| backlog-adp@program-aged2-2 | 836 | 0 | 149,036 (1.490) | fits |
| backlog-adp@program-aged2-6 | 869 | 0 | 149,036 (1.490) | fits |
| backlog-adp@program-aged1-2 | 771 | 0 | 149,176 (1.492) | fits |
| backlog-adp@program-aged1-6 | 803 | 0 | 149,055 (1.491) | fits |
| backlog-adp@verify-aged2-2 | 926 | 0 | 149,118 (1.491) | fits |
| backlog-adp@verify-aged2-6 | 960 | 0 | 148,618 (1.486) | fits |
| backlog-adp@verify-aged1-2 | 859 | 0 | 149,099 (1.491) | fits |
| backlog-adp@verify-aged1-6 | 893 | 0 | 149,099 (1.491) | fits |
| save-starved | 27083 | 0 | 153,485 (1.535) | fits |
| backlog-adp-refill | 326 | 0 | 150,154 (1.502) | fits |
| adp-link | 90 | 0 | 45,546 (0.455) | fits |
| adp-discover | 89 | 0 | 42,159 (0.422) | fits |
| aecp | 114 | 0 | 44,778 (0.448) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-2 | 2 | +8.462 ms, 76,435 (0.764 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 9.760 (20) | 10.240 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.803 (20) | 10.197 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 9.549 (20) | 10.451 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 9.852 (20) | 10.148 |
| backlog-adp@program-aged2-2 | 2 | +8.448 ms, 80,362 (0.804 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.856 (20) | 10.144 |
| backlog-adp@program-aged2-6 | 2 | +4.179 ms, 79,935 (0.799 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.766 (20) | 10.234 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.955 (20) | 11.045 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.034 (20) | 10.966 |
| backlog-adp@verify-aged2-2 | 2 | +8.608 ms, 77,281 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.871 (20) | 10.129 |
| backlog-adp@verify-aged2-6 | 2 | +4.167 ms, 76,914 (0.769 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.894 (20) | 10.106 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.983 (20) | 11.017 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.046 (20) | 10.954 |

Least margin over the aged windows: 10.106 ms, `backlog-adp@verify-aged2-6.service.srp.last.if0` at 9.894 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 4048.288 | 4,070 | 102 | - | 30.977 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-0 | 299 | 90,008 (0.900) | 75,853 (0.759) |
| backlog-adp@blank-2 | 299 | 90,747 (0.907) | 75,948 (0.759) |
| backlog-adp@blank-6 | 299 | 98,280 (0.983) | 76,031 (0.760) |
| backlog-adp@program-2 | 328 | 95,069 (0.951) | 78,482 (0.785) |
| backlog-adp@program-6 | 329 | 94,759 (0.948) | 77,749 (0.777) |
| backlog-adp@verify-2 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-6 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@blank-aged2-2 | 297 | 76,435 (0.764) | 75,481 (0.755) |
| backlog-adp@blank-aged2-6 | 297 | 84,797 (0.848) | 75,330 (0.753) |
| backlog-adp@blank-aged1-2 | 297 | 96,267 (0.963) | 75,943 (0.759) |
| backlog-adp@blank-aged1-6 | 297 | 90,627 (0.906) | 75,899 (0.759) |
| backlog-adp@program-aged2-2 | 326 | 94,759 (0.948) | 78,192 (0.782) |
| backlog-adp@program-aged2-6 | 326 | 94,759 (0.948) | 77,819 (0.778) |
| backlog-adp@program-aged1-2 | 326 | 94,759 (0.948) | 78,236 (0.782) |
| backlog-adp@program-aged1-6 | 326 | 94,899 (0.949) | 78,640 (0.786) |
| backlog-adp@verify-aged2-2 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged2-6 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged1-2 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged1-6 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| save-starved | 418 | 80,300 (0.803) | 77,841 (0.778) |
| backlog-adp-refill | 274 | 20,761 (0.208) | 2,254 (0.023) |
| adp-link | 80 | 20,719 (0.207) | 1,935 (0.019) |
| adp-discover | 80 | 20,719 (0.207) | 1,935 (0.019) |
| aecp | 80 | 20,719 (0.207) | 3,396 (0.034) |

Longest pass that carries a step: 98,280 CPU cycles (0.983 ms), backlog-adp@blank-6; longest step: 78,640 (0.786 ms), backlog-adp@program-aged1-6.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 423,447 | 4.234 | 20 | 20 | fits | 105,470 | 160 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 376,616 | 3.766 | 20 | 200 | fits | 143,920 | 230 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 481,470 | 4.815 | 20 | 200 | fits | 105,470 | 160 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 377,540 | 3.775 | 20 | 20 | fits | 143,920 | 230 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 482,174 | 4.822 | 20 | 20 | fits | 105,470 | 160 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 237,260 | 2.373 | 20 | 24 | fits | 150,277 | 155 | 0.398 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 380,190 | 3.802 | 20 | 24 | fits | 143,920 | 230 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 380,124 | 3.801 | 20 | 50 | fits | 143,920 | 230 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 485,198 | 4.852 | 20 | 50 | fits | 105,470 | 160 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 575,605 | 5.756 | 20 | 20 | fits | 90,473 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 982,668 | 9.827 | 20 | 20 | fits | 53,086 | 20 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 347,598 | 3.476 | 20 | 20 | fits | 100,818 | 142 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 303,967 | 3.040 | 20 | 200 | fits | 147,128 | 248 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 404,169 | 4.042 | 20 | 200 | fits | 100,818 | 142 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 304,891 | 3.049 | 20 | 20 | fits | 147,128 | 248 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 404,873 | 4.049 | 20 | 20 | fits | 100,818 | 142 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 161,403 | 1.614 | 20 | 24 | fits | 150,062 | 155 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 307,541 | 3.075 | 20 | 24 | fits | 147,128 | 248 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 307,475 | 3.075 | 20 | 50 | fits | 147,128 | 248 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 407,897 | 4.079 | 20 | 50 | fits | 100,818 | 142 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 498,372 | 4.984 | 20 | 20 | fits | 90,541 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 912,110 | 9.121 | 20 | 20 | fits | 52,685 | 20 | 0.659 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 357,595 | 3.576 | 20 | 20 | fits | 114,070 | 169 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 301,065 | 3.011 | 20 | 200 | fits | 143,610 | 231 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 414,519 | 4.145 | 20 | 200 | fits | 114,070 | 169 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 301,989 | 3.020 | 20 | 20 | fits | 143,610 | 231 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 415,223 | 4.152 | 20 | 20 | fits | 114,070 | 169 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 154,365 | 1.544 | 20 | 24 | fits | 150,160 | 156 | 0.397 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 304,639 | 3.046 | 20 | 24 | fits | 143,610 | 231 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 304,573 | 3.046 | 20 | 50 | fits | 143,610 | 231 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 418,247 | 4.182 | 20 | 50 | fits | 114,070 | 169 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 508,697 | 5.087 | 20 | 20 | fits | 90,516 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 898,615 | 8.986 | 20 | 20 | fits | 52,516 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 345,461 | 3.455 | 20 | 20 | fits | 100,748 | 142 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 301,910 | 3.019 | 20 | 200 | fits | 147,159 | 248 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 402,042 | 4.020 | 20 | 200 | fits | 100,748 | 142 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 302,834 | 3.028 | 20 | 20 | fits | 147,159 | 248 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 402,746 | 4.027 | 20 | 20 | fits | 100,748 | 142 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 159,315 | 1.593 | 20 | 24 | fits | 149,664 | 155 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 305,484 | 3.055 | 20 | 24 | fits | 147,159 | 248 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 305,418 | 3.054 | 20 | 50 | fits | 147,159 | 248 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 405,770 | 4.058 | 20 | 50 | fits | 100,748 | 142 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 491,139 | 4.911 | 20 | 20 | fits | 85,435 | 30 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 908,773 | 9.088 | 20 | 20 | fits | 69,083 | 31 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 339,972 | 3.400 | 20 | 20 | fits | 105,400 | 160 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 293,221 | 2.932 | 20 | 200 | fits | 144,043 | 230 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 398,005 | 3.980 | 20 | 200 | fits | 105,400 | 160 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 294,145 | 2.941 | 20 | 20 | fits | 144,043 | 230 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 398,709 | 3.987 | 20 | 20 | fits | 105,400 | 160 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 153,742 | 1.537 | 20 | 24 | fits | 149,460 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 296,795 | 2.968 | 20 | 24 | fits | 144,043 | 230 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 296,729 | 2.967 | 20 | 50 | fits | 144,043 | 230 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 401,733 | 4.017 | 20 | 50 | fits | 105,400 | 160 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 487,105 | 4.871 | 20 | 20 | fits | 85,438 | 30 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 905,333 | 9.053 | 20 | 20 | fits | 63,496 | 24 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 325,241 | 3.252 | 20 | 20 | fits | 106,101 | 160 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 290,608 | 2.906 | 20 | 200 | fits | 144,193 | 230 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 396,093 | 3.961 | 20 | 200 | fits | 106,101 | 160 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 291,532 | 2.915 | 20 | 20 | fits | 144,193 | 230 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 396,797 | 3.968 | 20 | 20 | fits | 106,101 | 160 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 150,979 | 1.510 | 20 | 24 | fits | 149,622 | 155 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 294,182 | 2.942 | 20 | 24 | fits | 144,193 | 230 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 294,116 | 2.941 | 20 | 50 | fits | 144,193 | 230 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 399,821 | 3.998 | 20 | 50 | fits | 106,101 | 160 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 490,286 | 4.903 | 20 | 20 | fits | 90,531 | 29 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 904,033 | 9.040 | 20 | 20 | fits | 52,572 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 347,744 | 3.477 | 20 | 20 | fits | 112,590 | 184 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 299,189 | 2.992 | 20 | 200 | fits | 143,302 | 209 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 411,163 | 4.112 | 20 | 200 | fits | 112,590 | 184 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 300,113 | 3.001 | 20 | 20 | fits | 143,302 | 209 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 411,867 | 4.119 | 20 | 20 | fits | 112,590 | 184 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 160,451 | 1.605 | 20 | 24 | fits | 149,539 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 302,763 | 3.028 | 20 | 24 | fits | 143,302 | 209 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 302,697 | 3.027 | 20 | 50 | fits | 143,302 | 209 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 414,891 | 4.149 | 20 | 50 | fits | 112,590 | 184 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 505,045 | 5.050 | 20 | 20 | fits | 90,220 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 911,821 | 9.118 | 20 | 20 | fits | 58,337 | 27 | 0.731 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 346,702 | 3.467 | 20 | 20 | fits | 104,387 | 148 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 300,374 | 3.004 | 20 | 200 | fits | 148,879 | 253 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 404,145 | 4.041 | 20 | 200 | fits | 104,387 | 148 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 301,298 | 3.013 | 20 | 20 | fits | 148,879 | 253 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 404,849 | 4.048 | 20 | 20 | fits | 104,387 | 148 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 147,103 | 1.471 | 20 | 24 | fits | 149,679 | 153 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 303,948 | 3.039 | 20 | 24 | fits | 148,879 | 253 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 303,882 | 3.039 | 20 | 50 | fits | 148,879 | 253 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 407,873 | 4.079 | 20 | 50 | fits | 104,387 | 148 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 498,136 | 4.981 | 20 | 20 | fits | 90,329 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 976,045 | 9.760 | 20 | 20 | fits | 57,160 | 28 | 0.689 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 359,144 | 3.591 | 20 | 20 | fits | 106,218 | 161 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 302,783 | 3.028 | 20 | 200 | fits | 148,945 | 233 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 408,385 | 4.084 | 20 | 200 | fits | 106,218 | 161 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 303,707 | 3.037 | 20 | 20 | fits | 148,945 | 233 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 409,089 | 4.091 | 20 | 20 | fits | 106,218 | 161 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 158,402 | 1.584 | 20 | 24 | fits | 149,137 | 152 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 306,357 | 3.064 | 20 | 24 | fits | 148,945 | 233 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 306,291 | 3.063 | 20 | 50 | fits | 148,945 | 233 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 412,113 | 4.121 | 20 | 50 | fits | 106,218 | 161 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 590,292 | 5.903 | 20 | 20 | fits | 93,448 | 35 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 980,323 | 9.803 | 20 | 20 | fits | 52,532 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 329,986 | 3.300 | 20 | 20 | fits | 109,684 | 167 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 291,385 | 2.914 | 20 | 200 | fits | 143,738 | 230 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 400,453 | 4.005 | 20 | 200 | fits | 109,684 | 167 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 292,309 | 2.923 | 20 | 20 | fits | 143,738 | 230 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 401,157 | 4.012 | 20 | 20 | fits | 109,684 | 167 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 152,211 | 1.522 | 20 | 24 | fits | 149,175 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 294,959 | 2.950 | 20 | 24 | fits | 143,738 | 230 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 294,893 | 2.949 | 20 | 50 | fits | 143,738 | 230 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 404,181 | 4.042 | 20 | 50 | fits | 109,684 | 167 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 504,363 | 5.044 | 20 | 20 | fits | 91,043 | 29 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 954,913 | 9.549 | 20 | 20 | fits | 65,680 | 25 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 360,412 | 3.604 | 20 | 20 | fits | 119,328 | 160 | 0.498 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 292,690 | 2.927 | 20 | 200 | fits | 150,229 | 238 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 411,402 | 4.114 | 20 | 200 | fits | 119,328 | 160 | 0.498 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 293,614 | 2.936 | 20 | 20 | fits | 150,229 | 238 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 412,106 | 4.121 | 20 | 20 | fits | 119,328 | 160 | 0.498 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 147,025 | 1.470 | 20 | 24 | fits | 149,118 | 152 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 296,264 | 2.963 | 20 | 24 | fits | 150,229 | 238 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 296,198 | 2.962 | 20 | 50 | fits | 150,229 | 238 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 415,130 | 4.151 | 20 | 50 | fits | 119,328 | 160 | 0.498 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 546,920 | 5.469 | 20 | 20 | fits | 90,093 | 29 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 985,221 | 9.852 | 20 | 20 | fits | 52,530 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 328,076 | 3.281 | 20 | 20 | fits | 106,101 | 160 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 293,443 | 2.934 | 20 | 200 | fits | 143,900 | 230 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 398,928 | 3.989 | 20 | 200 | fits | 106,101 | 160 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 294,367 | 2.944 | 20 | 20 | fits | 143,900 | 230 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 399,632 | 3.996 | 20 | 20 | fits | 106,101 | 160 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 154,107 | 1.541 | 20 | 24 | fits | 149,036 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 297,017 | 2.970 | 20 | 24 | fits | 143,900 | 230 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 296,951 | 2.970 | 20 | 50 | fits | 143,900 | 230 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 402,656 | 4.027 | 20 | 50 | fits | 106,101 | 160 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 492,698 | 4.927 | 20 | 20 | fits | 90,108 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 985,560 | 9.856 | 20 | 20 | fits | 64,128 | 25 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 355,155 | 3.552 | 20 | 20 | fits | 112,592 | 155 | 0.479 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 291,613 | 2.916 | 20 | 200 | fits | 147,136 | 249 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 412,519 | 4.125 | 20 | 200 | fits | 112,592 | 155 | 0.479 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 292,537 | 2.925 | 20 | 20 | fits | 147,136 | 249 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 413,223 | 4.132 | 20 | 20 | fits | 112,592 | 155 | 0.479 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 149,041 | 1.490 | 20 | 24 | fits | 149,036 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 295,187 | 2.952 | 20 | 24 | fits | 147,136 | 249 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 295,121 | 2.951 | 20 | 50 | fits | 147,136 | 249 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 416,247 | 4.162 | 20 | 50 | fits | 112,592 | 155 | 0.479 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 586,286 | 5.863 | 20 | 20 | fits | 90,170 | 29 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 976,632 | 9.766 | 20 | 20 | fits | 52,572 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 332,619 | 3.326 | 20 | 20 | fits | 109,001 | 166 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 295,377 | 2.954 | 20 | 200 | fits | 145,721 | 235 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 403,762 | 4.038 | 20 | 200 | fits | 109,001 | 166 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 296,301 | 2.963 | 20 | 20 | fits | 145,721 | 235 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 404,466 | 4.045 | 20 | 20 | fits | 109,001 | 166 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 146,470 | 1.465 | 20 | 24 | fits | 149,176 | 153 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 298,951 | 2.990 | 20 | 24 | fits | 145,721 | 235 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 298,885 | 2.989 | 20 | 50 | fits | 145,721 | 235 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 407,490 | 4.075 | 20 | 50 | fits | 109,001 | 166 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 497,890 | 4.979 | 20 | 20 | fits | 90,466 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 895,487 | 8.955 | 20 | 20 | fits | 52,976 | 21 | 0.663 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 349,322 | 3.493 | 20 | 20 | fits | 108,798 | 149 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 298,197 | 2.982 | 20 | 200 | fits | 146,982 | 248 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 406,379 | 4.064 | 20 | 200 | fits | 108,798 | 149 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 299,121 | 2.991 | 20 | 20 | fits | 146,982 | 248 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 407,083 | 4.071 | 20 | 20 | fits | 108,798 | 149 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 155,779 | 1.558 | 20 | 24 | fits | 149,055 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 301,771 | 3.018 | 20 | 24 | fits | 146,982 | 248 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 301,705 | 3.017 | 20 | 50 | fits | 146,982 | 248 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 410,107 | 4.101 | 20 | 50 | fits | 108,798 | 149 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 513,155 | 5.132 | 20 | 20 | fits | 93,561 | 35 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 903,445 | 9.034 | 20 | 20 | fits | 52,572 | 20 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 329,877 | 3.299 | 20 | 20 | fits | 106,075 | 160 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 295,244 | 2.952 | 20 | 200 | fits | 143,980 | 230 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 400,703 | 4.007 | 20 | 200 | fits | 106,075 | 160 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 296,168 | 2.962 | 20 | 20 | fits | 143,980 | 230 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 401,407 | 4.014 | 20 | 20 | fits | 106,075 | 160 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 155,828 | 1.558 | 20 | 24 | fits | 149,118 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 298,818 | 2.988 | 20 | 24 | fits | 143,980 | 230 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 298,752 | 2.988 | 20 | 50 | fits | 143,980 | 230 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 404,431 | 4.044 | 20 | 50 | fits | 106,075 | 160 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 494,647 | 4.946 | 20 | 20 | fits | 90,282 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 987,065 | 9.871 | 20 | 20 | fits | 52,698 | 21 | 0.657 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 354,450 | 3.545 | 20 | 20 | fits | 108,672 | 148 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 303,254 | 3.033 | 20 | 200 | fits | 147,354 | 248 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 411,310 | 4.113 | 20 | 200 | fits | 108,672 | 148 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 304,178 | 3.042 | 20 | 20 | fits | 147,354 | 248 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 412,014 | 4.120 | 20 | 20 | fits | 108,672 | 148 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 160,464 | 1.605 | 20 | 24 | fits | 148,618 | 153 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 306,828 | 3.068 | 20 | 24 | fits | 147,354 | 248 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 306,762 | 3.068 | 20 | 50 | fits | 147,354 | 248 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 415,038 | 4.150 | 20 | 50 | fits | 108,672 | 148 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 582,004 | 5.820 | 20 | 20 | fits | 90,118 | 29 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 989,406 | 9.894 | 20 | 20 | fits | 53,068 | 20 | 0.674 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 334,896 | 3.349 | 20 | 20 | fits | 101,623 | 142 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 291,221 | 2.912 | 20 | 200 | fits | 148,592 | 253 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 392,228 | 3.922 | 20 | 200 | fits | 101,623 | 142 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 292,145 | 2.921 | 20 | 20 | fits | 148,592 | 253 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 392,932 | 3.929 | 20 | 20 | fits | 101,623 | 142 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 147,193 | 1.472 | 20 | 24 | fits | 149,099 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 294,795 | 2.948 | 20 | 24 | fits | 148,592 | 253 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 294,729 | 2.947 | 20 | 50 | fits | 148,592 | 253 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 395,956 | 3.960 | 20 | 50 | fits | 101,623 | 142 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 486,160 | 4.862 | 20 | 20 | fits | 90,270 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 898,341 | 8.983 | 20 | 20 | fits | 63,797 | 24 | 0.614 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 363,211 | 3.632 | 20 | 20 | fits | 112,513 | 155 | 0.478 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 299,748 | 2.997 | 20 | 200 | fits | 147,187 | 249 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 420,575 | 4.206 | 20 | 200 | fits | 112,513 | 155 | 0.478 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 300,672 | 3.007 | 20 | 20 | fits | 147,187 | 249 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 421,279 | 4.213 | 20 | 20 | fits | 112,513 | 155 | 0.478 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 157,125 | 1.571 | 20 | 24 | fits | 149,099 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 303,322 | 3.033 | 20 | 24 | fits | 147,187 | 249 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 303,256 | 3.033 | 20 | 50 | fits | 147,187 | 249 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 424,303 | 4.243 | 20 | 50 | fits | 112,513 | 155 | 0.478 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 514,597 | 5.146 | 20 | 20 | fits | 90,360 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 904,623 | 9.046 | 20 | 20 | fits | 52,572 | 20 | 0.657 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 152,545 | 1.525 | 20 | 200 | fits | 153,485 | 250 | 0.463 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 219,288 | 2.193 | 20 | 20 | fits | 86,880 | 88 | 0.665 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 289,374 | 2.894 | 20 | 24 | fits | 85,818 | 61 | 0.563 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 179,813 | 1.798 | 20 | 50 | fits | 86,880 | 88 | 0.665 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 837,276 | 8.373 | 20 | 20 | fits | 89,198 | 38 | 0.582 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 250,639 | 2.506 | 20 | 20 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 10,034 | 0.100 | 20 | 20 | fits | 25,838 | 19 | 0.816 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 292,279 | 2.923 | 20 | 200 | fits | 146,875 | 248 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 27,869 | 0.279 | 20 | 200 | fits | 25,838 | 19 | 0.816 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 293,203 | 2.932 | 20 | 20 | fits | 146,875 | 248 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 387,021 | 3.870 | 20 | 20 | fits | 94,654 | 139 | 0.408 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 149,968 | 1.500 | 20 | 24 | fits | 150,154 | 155 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 295,853 | 2.959 | 20 | 24 | fits | 146,875 | 248 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 295,787 | 2.958 | 20 | 50 | fits | 146,875 | 248 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 390,045 | 3.900 | 20 | 50 | fits | 94,654 | 139 | 0.408 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 489,450 | 4.894 | 20 | 20 | fits | 90,395 | 29 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 886,572 | 8.866 | 20 | 20 | fits | 52,567 | 20 | 0.657 |
| LINK_UP | `adp.link_up.if0` | 2,501 | 0.025 | 20 | 200 | fits | 25,663 | 43 (11) | 0.728 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,715 | 0.087 | 20 | 200 | fits | 21,370 | 23 (39) | 0.723 |
| LINK_DOWN | `adp.link_down.if0` | 2,142 | 0.021 | 20 | 200 | fits | 24,536 | 23 (9) | 0.763 |
| LINK_UP | `adp.link_up.if0` | 2,501 | 0.025 | 20 | 200 | fits | 25,663 | 43 (11) | 0.728 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 8,715 | 0.087 | 20 | 200 | fits | 21,370 | 23 (39) | 0.723 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,683 | 0.047 | 20 | 200 | fits | 15,869 | 16 (31) | 0.667 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 12,785 | 0.128 | 20 | 24 | fits | 26,862 | 20 | 0.789 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 19,004 | 0.190 | 20 | 24 | fits | 30,813 | 20 | 0.727 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 23,349 | 0.233 | 20 | 24 | fits | 26,332 | 20 | 0.743 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 14,888 | 0.149 | 20 | 24 | fits | 26,537 | 20 | 0.740 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 14,585 | 0.146 | 20 | 24 | fits | 27,325 | 20 | 0.740 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 24,141 | 0.241 | 20 | 24 | fits | 26,971 | 20 | 0.743 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,964 | 0.150 | 20 | 24 | fits | 26,015 | 20 | 0.744 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 23,502 | 0.235 | 20 | 24 | fits | 26,409 | 20 | 0.756 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,434 | 0.144 | 20 | 24 | fits | 25,782 | 20 | 0.757 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 25,760 | 0.258 | 20 | 24 | fits | 28,543 | 21 | 0.662 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 14,152 | 0.142 | 20 | 24 | fits | 25,359 | 20 | 0.773 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 14,211 | 0.142 | 20 | 24 | fits | 25,746 | 20 | 0.775 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 23,334 | 0.233 | 20 | 24 | fits | 26,155 | 20 | 0.743 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,521 | 0.155 | 20 | 24 | fits | 27,256 | 20 | 0.749 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 23,393 | 0.234 | 20 | 24 | fits | 26,311 | 20 | 0.756 |
| get_configuration | `aecp.get_configuration.if0` | 12,856 | 0.129 | 20 | 24 | fits | 24,007 | 20 | 0.765 |
| entity_available | `aecp.entity_available.if0` | 21,216 | 0.212 | 20 | 24 | fits | 23,632 | 20 | 0.752 |
| get_name | `aecp.get_name.if0` | 23,673 | 0.237 | 20 | 24 | fits | 26,998 | 20 | 0.775 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 15,889 | 0.159 | 20 | 24 | fits | 27,449 | 25 | 0.749 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 25,069 | 0.251 | 20 | 24 | fits | 28,058 | 27 | 0.777 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 15,333 | 0.153 | 20 | 24 | fits | 26,720 | 27 | 0.775 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 21,729 | 0.217 | 20 | 24 | fits | 24,249 | 20 | 0.776 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 20,847 | 0.208 | 20 | 24 | fits | 24,125 | 20 | 0.765 |
| set_name | `aecp.set_name.if0` | 22,883 | 0.229 | 20 | 24 | fits | 44,778 | 43 | 0.761 |
| lock_entity | `aecp.lock_entity.if0` | 27,106 | 0.271 | 20 | 24 | fits | 33,795 | 34 | 0.770 |
| unlock_entity | `aecp.unlock_entity.if0` | 19,677 | 0.197 | 20 | 24 | fits | 34,147 | 33 | 0.772 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

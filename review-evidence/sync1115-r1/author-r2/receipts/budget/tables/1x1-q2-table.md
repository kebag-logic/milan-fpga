### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 61 paths and 0 of 218 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.076 (0.265) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.059 (0.247) | fits | 0 adp | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.108 (0.468) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.045 (0.170) | fits | 0 adp | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.024 (0.246) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.026 (0.268) | fits | 0 events | 3 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.041 (0.207) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.183 (0.513) | fits | 0 events | 3 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.224 (0.532) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.261 (0.577) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.120 (0.435) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.145 (0.463) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.110 (0.276) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.178 (0.540) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.153 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.186 (0.511) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.254 (0.570) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.250 (0.564) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.129 (0.449) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.272 (0.587) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.139 (0.459) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.130 (0.451) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.144 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.247 (0.561) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.140 (0.461) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.249 (0.567) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.255 (0.571) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.257 (0.581) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.136 (0.457) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.243 (0.557) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.210 (0.627) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.121 (0.439) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.152 (0.365) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.660 (2.980) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.397 (0.507) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.503 (0.824) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.445 (0.768) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.472 (0.760) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.466 (0.624) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.415 (3.738) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.455 (0.743) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.963 (4.186) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-6.adp_available.if0` (backlog-adp@program-aged2-6) | 3.625 (4.325) | fits | 7 adp | 13 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.085 (0.451) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.688 (2.111) | fits | 15 events | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 1.977 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 1.571 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.956 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.911 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.873 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.764 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.141 | fits | 0 acmp | 15 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.acmp.last.if0` (backlog-adp@program-aged2-6) | 4.196 | fits | 11 acmp | 15 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.184 | fits | 0 adp | 15 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.adp.last.if0` (backlog-adp@program-aged2-6) | 4.189 | fits | 7 adp | 15 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.aecp.first.if0` (backlog-adp@verify-aged2-6) | 1.629 | fits | 0 aecp | 15 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.167 | fits | 15 aecp | 15 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.167 | fits | 0 maap | 15 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.maap.last.if0` (backlog-adp@program-aged2-6) | 4.226 | fits | 6 maap | 15 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 5.886 | fits | 0 srp | 15 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.srp.last.if0` (backlog-adp@program-aged2-6) | 10.943 | fits | 31 srp | 15 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-aged2-6 | 0 | 11.470 | 12 | 150,828 (1.508) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.827 | 13 | 151,604 (1.516) | yes | - |
| backlog-adp@program-aged1-2 | 1 | 11.275 | 10 | 151,241 (1.512) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 11.266 | 10 | 148,670 (1.487) | yes | - |
| backlog-adp@program-aged1-6 | 1 | 11.713 | 12 | 148,909 (1.489) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.328 | 12 | 150,701 (1.507) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.341 | 11 | 150,748 (1.507) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.350 | 11 | 150,894 (1.509) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.374 | 11 | 150,571 (1.506) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.495 | 13 | 150,844 (1.508) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 11.262 | 11 | 150,571 (1.506) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 11.257 | 11 | 150,618 (1.506) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 11.416 | 12 | 150,750 (1.508) | yes | - |
| backlog | 0 | 5.590 | 7 | 154,943 (1.549) | yes | - |
| backlog-adp-refill | 0 | 40.772 | 26 | 150,933 (1.509) | yes | - |

Composed maximum over 2 of 4 backlog windows, a partial figure (backlog-adp, backlog-owed not run): 154,943 CPU cycles (1.549 ms), backlog.
Over the windows that released their whole load only: 154,943 (1.549 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@program-aged2-6 | 848 | 0 | 150,828 (1.508) | fits |
| backlog-adp@program-aged1-0 | 745 | 0 | 151,604 (1.516) | fits |
| backlog-adp@program-aged1-2 | 758 | 0 | 151,508 (1.515) | fits |
| backlog-adp@program-aged1-4 | 772 | 0 | 150,717 (1.507) | fits |
| backlog-adp@program-aged1-6 | 789 | 0 | 150,670 (1.507) | fits |
| backlog-adp@verify-aged2-0 | 900 | 0 | 150,701 (1.507) | fits |
| backlog-adp@verify-aged2-2 | 914 | 0 | 150,748 (1.507) | fits |
| backlog-adp@verify-aged2-4 | 929 | 0 | 150,914 (1.509) | fits |
| backlog-adp@verify-aged2-6 | 944 | 0 | 150,571 (1.506) | fits |
| backlog-adp@verify-aged1-0 | 841 | 0 | 150,844 (1.508) | fits |
| backlog-adp@verify-aged1-2 | 854 | 0 | 150,571 (1.506) | fits |
| backlog-adp@verify-aged1-4 | 869 | 0 | 150,618 (1.506) | fits |
| backlog-adp@verify-aged1-6 | 885 | 0 | 150,750 (1.508) | fits |
| adp-advertise | 598 | 0 | 30,379 (0.304) | fits |
| save-starved | 23881 | 0 | 158,049 (1.580) | fits |
| save | 610 | 0 | 44,923 (0.449) | fits |
| backlog | 286 | 0 | 154,943 (1.549) | fits |
| backlog-adp-refill | 329 | 0 | 150,933 (1.509) | fits |
| acmp-disc | 938 | 0 | 41,099 (0.411) | fits |
| adp-link | 89 | 0 | 39,840 (0.398) | fits |
| adp-discover | 88 | 0 | 30,379 (0.304) | fits |
| aecp-fanout | 113 | 0 | 62,439 (0.624) | fits |
| aecp | 112 | 0 | 43,866 (0.439) | fits |
| datapath-events | 116 | 0 | 30,379 (0.304) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@program-aged2-6 | 2 | +4.243 ms, 80,312 (0.803 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.943 (20) | 9.057 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.841 (20) | 10.159 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.944 (20) | 10.056 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.934 (20) | 10.066 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.917 (20) | 10.083 |
| backlog-adp@verify-aged2-0 | 2 | none | +10.219 ms, 77,270 (0.773 ms), read-back | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.982 (20) | 10.018 |
| backlog-adp@verify-aged2-2 | 2 | +8.472 ms, 77,468 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.812 (20) | 9.188 |
| backlog-adp@verify-aged2-4 | 2 | +5.737 ms, 77,414 (0.774 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.820 (20) | 9.180 |
| backlog-adp@verify-aged2-6 | 2 | +4.168 ms, 77,585 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.846 (20) | 9.154 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.872 (20) | 10.128 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.970 (20) | 10.030 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.966 (20) | 10.034 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.126 (20) | 9.874 |

Least margin over the aged windows: 9.057 ms, `backlog-adp@program-aged2-6.service.srp.last.if0` at 10.943 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 4049.017 | 4,070 | 102 | - | 31.239 | yes | within |
| save | 2019.630 | 4,070 | 102 | - | 10.882 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@program-aged2-6 | 326 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@program-aged1-0 | 326 | 97,240 (0.972) | 78,820 (0.788) |
| backlog-adp@program-aged1-2 | 326 | 97,240 (0.972) | 78,891 (0.789) |
| backlog-adp@program-aged1-4 | 326 | 97,240 (0.972) | 78,891 (0.789) |
| backlog-adp@program-aged1-6 | 326 | 97,240 (0.972) | 78,891 (0.789) |
| backlog-adp@verify-aged2-0 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged2-2 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged2-4 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged2-6 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged1-0 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged1-2 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged1-4 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| backlog-adp@verify-aged1-6 | 355 | 97,240 (0.972) | 78,381 (0.784) |
| adp-advertise | 577 | 22,757 (0.228) | 2,490 (0.025) |
| save-starved | 418 | 80,873 (0.809) | 78,158 (0.782) |
| save | 585 | 96,281 (0.963) | 78,143 (0.781) |
| backlog | 265 | 22,757 (0.228) | 2,490 (0.025) |
| backlog-adp-refill | 274 | 22,757 (0.228) | 2,511 (0.025) |
| acmp-disc | 305 | 97,005 (0.970) | 78,248 (0.782) |
| adp-link | 79 | 22,757 (0.228) | 2,490 (0.025) |
| adp-discover | 79 | 22,757 (0.228) | 2,490 (0.025) |
| aecp-fanout | 80 | 22,757 (0.228) | 2,490 (0.025) |
| aecp | 79 | 22,757 (0.228) | 2,490 (0.025) |
| datapath-events | 69 | 22,757 (0.228) | 2,490 (0.025) |

Longest pass that carries a step: 97,240 CPU cycles (0.972 ms), backlog-adp@program-aged2-6; longest step: 78,891 (0.789 ms), backlog-adp@program-aged1-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 362,474 | 3.625 | 20 | 20 | fits | 106,879 | 148 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 312,630 | 3.126 | 20 | 200 | fits | 149,598 | 253 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 418,893 | 4.189 | 20 | 200 | fits | 106,879 | 148 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 313,554 | 3.136 | 20 | 20 | fits | 149,598 | 253 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 419,597 | 4.196 | 20 | 20 | fits | 106,879 | 148 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 159,238 | 1.592 | 20 | 24 | fits | 150,828 | 153 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 316,204 | 3.162 | 20 | 24 | fits | 149,598 | 253 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 316,138 | 3.161 | 20 | 50 | fits | 149,598 | 253 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 422,621 | 4.226 | 20 | 50 | fits | 106,879 | 148 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 588,590 | 5.886 | 20 | 20 | fits | 85,723 | 25 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,094,319 | 10.943 | 20 | 20 | fits | 74,080 | 24 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 341,418 | 3.414 | 20 | 20 | fits | 102,470 | 157 | 0.481 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 294,091 | 2.941 | 20 | 200 | fits | 151,604 | 243 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 405,066 | 4.051 | 20 | 200 | fits | 102,470 | 157 | 0.481 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 295,015 | 2.950 | 20 | 20 | fits | 151,604 | 243 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 405,770 | 4.058 | 20 | 20 | fits | 102,470 | 157 | 0.481 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 147,051 | 1.471 | 20 | 24 | fits | 150,602 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 297,665 | 2.977 | 20 | 24 | fits | 151,604 | 243 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 297,599 | 2.976 | 20 | 50 | fits | 151,604 | 243 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 408,794 | 4.088 | 20 | 50 | fits | 102,470 | 157 | 0.481 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 494,556 | 4.946 | 20 | 20 | fits | 85,828 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 984,125 | 9.841 | 20 | 20 | fits | 60,416 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 329,913 | 3.299 | 20 | 20 | fits | 100,611 | 157 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 292,917 | 2.929 | 20 | 200 | fits | 151,241 | 242 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 392,912 | 3.929 | 20 | 200 | fits | 100,611 | 157 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 293,841 | 2.938 | 20 | 20 | fits | 151,241 | 242 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 393,616 | 3.936 | 20 | 20 | fits | 100,611 | 157 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 146,240 | 1.462 | 20 | 24 | fits | 151,508 | 157 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 296,491 | 2.965 | 20 | 24 | fits | 151,241 | 242 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 296,425 | 2.964 | 20 | 50 | fits | 151,241 | 242 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 396,640 | 3.966 | 20 | 50 | fits | 100,611 | 157 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 482,714 | 4.827 | 20 | 20 | fits | 86,140 | 24 | 0.788 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 994,434 | 9.944 | 20 | 20 | fits | 86,886 | 28 | 0.660 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 334,660 | 3.347 | 20 | 20 | fits | 100,159 | 142 | 0.434 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 291,706 | 2.917 | 20 | 200 | fits | 148,670 | 253 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 391,249 | 3.912 | 20 | 200 | fits | 100,159 | 142 | 0.434 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 292,630 | 2.926 | 20 | 20 | fits | 148,670 | 253 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 391,953 | 3.920 | 20 | 20 | fits | 100,159 | 142 | 0.434 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 147,600 | 1.476 | 20 | 24 | fits | 150,717 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 295,280 | 2.953 | 20 | 24 | fits | 148,670 | 253 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 295,214 | 2.952 | 20 | 50 | fits | 148,670 | 253 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 394,977 | 3.950 | 20 | 50 | fits | 100,159 | 142 | 0.434 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 480,899 | 4.809 | 20 | 20 | fits | 85,988 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 993,424 | 9.934 | 20 | 20 | fits | 86,466 | 28 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 355,145 | 3.551 | 20 | 20 | fits | 111,484 | 154 | 0.474 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 292,961 | 2.930 | 20 | 200 | fits | 148,909 | 254 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 412,672 | 4.127 | 20 | 200 | fits | 111,484 | 154 | 0.474 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 293,885 | 2.939 | 20 | 20 | fits | 148,909 | 254 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 413,376 | 4.134 | 20 | 20 | fits | 111,484 | 154 | 0.474 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 148,616 | 1.486 | 20 | 24 | fits | 150,670 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 296,535 | 2.965 | 20 | 24 | fits | 148,909 | 254 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 296,469 | 2.965 | 20 | 50 | fits | 148,909 | 254 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 416,400 | 4.164 | 20 | 50 | fits | 111,484 | 154 | 0.474 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 502,242 | 5.022 | 20 | 20 | fits | 85,908 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 991,749 | 9.917 | 20 | 20 | fits | 60,416 | 20 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 346,138 | 3.461 | 20 | 20 | fits | 99,273 | 142 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 303,607 | 3.036 | 20 | 200 | fits | 147,466 | 248 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 402,264 | 4.023 | 20 | 200 | fits | 99,273 | 142 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 304,531 | 3.045 | 20 | 20 | fits | 147,466 | 248 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 402,968 | 4.030 | 20 | 20 | fits | 99,273 | 142 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 160,705 | 1.607 | 20 | 24 | fits | 150,701 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 307,181 | 3.072 | 20 | 24 | fits | 147,466 | 248 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 307,115 | 3.071 | 20 | 50 | fits | 147,466 | 248 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 405,992 | 4.060 | 20 | 50 | fits | 99,273 | 142 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 491,906 | 4.919 | 20 | 20 | fits | 85,980 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 998,247 | 9.982 | 20 | 20 | fits | 73,812 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 348,049 | 3.480 | 20 | 20 | fits | 99,674 | 143 | 0.427 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 305,518 | 3.055 | 20 | 200 | fits | 147,390 | 248 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 404,576 | 4.046 | 20 | 200 | fits | 99,674 | 143 | 0.427 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 306,442 | 3.064 | 20 | 20 | fits | 147,390 | 248 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 405,280 | 4.053 | 20 | 20 | fits | 99,674 | 143 | 0.427 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 162,692 | 1.627 | 20 | 24 | fits | 150,748 | 152 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 309,092 | 3.091 | 20 | 24 | fits | 147,390 | 248 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 309,026 | 3.090 | 20 | 50 | fits | 147,390 | 248 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 408,304 | 4.083 | 20 | 50 | fits | 99,674 | 143 | 0.427 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 507,200 | 5.072 | 20 | 20 | fits | 89,647 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,081,200 | 10.812 | 20 | 20 | fits | 73,863 | 24 | 0.684 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 353,599 | 3.536 | 20 | 20 | fits | 100,293 | 160 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 302,893 | 3.029 | 20 | 200 | fits | 150,894 | 238 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 402,570 | 4.026 | 20 | 200 | fits | 100,293 | 160 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 303,817 | 3.038 | 20 | 20 | fits | 150,894 | 238 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 403,274 | 4.033 | 20 | 20 | fits | 100,293 | 160 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 148,002 | 1.480 | 20 | 24 | fits | 150,914 | 153 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 306,467 | 3.065 | 20 | 24 | fits | 150,894 | 238 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 306,401 | 3.064 | 20 | 50 | fits | 150,894 | 238 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 406,298 | 4.063 | 20 | 50 | fits | 100,293 | 160 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 492,522 | 4.925 | 20 | 20 | fits | 86,290 | 24 | 0.787 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,082,002 | 10.820 | 20 | 20 | fits | 78,615 | 31 | 0.725 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 362,377 | 3.624 | 20 | 20 | fits | 104,803 | 160 | 0.455 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 307,261 | 3.073 | 20 | 200 | fits | 148,876 | 233 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 411,448 | 4.114 | 20 | 200 | fits | 104,803 | 160 | 0.455 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 308,185 | 3.082 | 20 | 20 | fits | 148,876 | 233 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 412,152 | 4.122 | 20 | 20 | fits | 104,803 | 160 | 0.455 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 162,949 | 1.629 | 20 | 24 | fits | 150,571 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 310,835 | 3.108 | 20 | 24 | fits | 148,876 | 233 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 310,769 | 3.108 | 20 | 50 | fits | 148,876 | 233 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 415,176 | 4.152 | 20 | 50 | fits | 104,803 | 160 | 0.455 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 578,336 | 5.783 | 20 | 20 | fits | 85,641 | 25 | 0.781 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,084,624 | 10.846 | 20 | 20 | fits | 73,812 | 24 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 337,878 | 3.379 | 20 | 20 | fits | 104,506 | 160 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 303,945 | 3.039 | 20 | 200 | fits | 146,383 | 235 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 407,835 | 4.078 | 20 | 200 | fits | 104,506 | 160 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 304,869 | 3.049 | 20 | 20 | fits | 146,383 | 235 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 408,539 | 4.085 | 20 | 20 | fits | 104,506 | 160 | 0.432 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 153,565 | 1.536 | 20 | 24 | fits | 150,844 | 153 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 307,519 | 3.075 | 20 | 24 | fits | 146,383 | 235 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 307,453 | 3.075 | 20 | 50 | fits | 146,383 | 235 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 411,563 | 4.116 | 20 | 50 | fits | 104,506 | 160 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 497,644 | 4.976 | 20 | 20 | fits | 86,147 | 24 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 987,244 | 9.872 | 20 | 20 | fits | 60,509 | 21 | 0.709 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 339,007 | 3.390 | 20 | 20 | fits | 100,120 | 142 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 296,092 | 2.961 | 20 | 200 | fits | 147,475 | 248 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 395,596 | 3.956 | 20 | 200 | fits | 100,120 | 142 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 297,016 | 2.970 | 20 | 20 | fits | 147,475 | 248 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 396,300 | 3.963 | 20 | 20 | fits | 100,120 | 142 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 153,181 | 1.532 | 20 | 24 | fits | 150,571 | 152 | 0.347 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 299,666 | 2.997 | 20 | 24 | fits | 147,475 | 248 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 299,600 | 2.996 | 20 | 50 | fits | 147,475 | 248 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 399,324 | 3.993 | 20 | 50 | fits | 100,120 | 142 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 485,269 | 4.853 | 20 | 20 | fits | 86,011 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 996,992 | 9.970 | 20 | 20 | fits | 86,215 | 28 | 0.636 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 340,918 | 3.409 | 20 | 20 | fits | 100,521 | 143 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 298,003 | 2.980 | 20 | 200 | fits | 147,399 | 248 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 397,908 | 3.979 | 20 | 200 | fits | 100,521 | 143 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 298,927 | 2.989 | 20 | 20 | fits | 147,399 | 248 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 398,612 | 3.986 | 20 | 20 | fits | 100,521 | 143 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 155,168 | 1.552 | 20 | 24 | fits | 150,618 | 152 | 0.348 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 301,577 | 3.016 | 20 | 24 | fits | 147,399 | 248 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 301,511 | 3.015 | 20 | 50 | fits | 147,399 | 248 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 401,636 | 4.016 | 20 | 50 | fits | 100,521 | 143 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 500,347 | 5.003 | 20 | 20 | fits | 89,647 | 31 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 996,635 | 9.966 | 20 | 20 | fits | 73,609 | 24 | 0.671 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 360,742 | 3.607 | 20 | 20 | fits | 107,465 | 148 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 310,715 | 3.107 | 20 | 200 | fits | 149,681 | 253 | 0.376 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 417,564 | 4.176 | 20 | 200 | fits | 107,465 | 148 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 311,639 | 3.116 | 20 | 20 | fits | 149,681 | 253 | 0.376 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 418,268 | 4.183 | 20 | 20 | fits | 107,465 | 148 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 157,240 | 1.572 | 20 | 24 | fits | 150,750 | 153 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 314,289 | 3.143 | 20 | 24 | fits | 149,681 | 253 | 0.376 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 314,223 | 3.142 | 20 | 50 | fits | 149,681 | 253 | 0.376 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 421,292 | 4.213 | 20 | 50 | fits | 107,465 | 148 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 507,360 | 5.074 | 20 | 20 | fits | 86,134 | 24 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,012,560 | 10.126 | 20 | 20 | fits | 66,131 | 27 | 0.765 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 26,823 | 43 (11) | 0.735 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,339 | 0.183 | 20 | 200 | fits | 23,214 | 23 (39) | 0.757 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 4,110 | 0.041 | 20 | 200 | fits | 2,669 | 10 (11) | 0.571 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 157,109 | 1.571 | 20 | 200 | fits | 158,049 | 258 | 0.452 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 197,744 | 1.977 | 20 | 20 | fits | 144,636 | 267 | 0.357 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 295,553 | 2.956 | 20 | 24 | fits | 84,250 | 55 | 0.577 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 191,115 | 1.911 | 20 | 50 | fits | 93,618 | 83 | 0.696 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 987,265 | 9.873 | 20 | 20 | fits | 38,069 | 18 | 0.841 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 276,375 | 2.764 | 20 | 20 | fits | 0 | - | 0.000 |
| an event behind 15 others | `backlog.event.if0` | 168,783 | 1.688 | 20 | 200 | fits | 56,194 | 78 | 0.570 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 396,314 | 3.963 | 20 | 20 | fits | 147,550 | 167 | 0.385 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 418,397 | 4.184 | 20 | 200 | fits | 147,550 | 167 | 0.385 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 417,781 | 4.178 | 20 | 200 | fits | 147,550 | 167 | 0.385 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 414,075 | 4.141 | 20 | 20 | fits | 147,550 | 167 | 0.385 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 413,239 | 4.132 | 20 | 20 | fits | 147,550 | 167 | 0.385 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 154,052 | 1.541 | 20 | 24 | fits | 154,943 | 158 | 0.366 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 416,725 | 4.167 | 20 | 24 | fits | 147,550 | 167 | 0.385 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 416,659 | 4.167 | 20 | 50 | fits | 147,550 | 167 | 0.385 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 416,263 | 4.163 | 20 | 50 | fits | 147,550 | 167 | 0.385 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 447,359 | 4.474 | 20 | 20 | fits | 31,162 | 56 | 0.219 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 506,960 | 5.070 | 20 | 20 | fits | 24,506 | 41 | 0.177 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,547 | 0.085 | 20 | 20 | fits | 27,442 | 19 | 0.820 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 296,261 | 2.963 | 20 | 200 | fits | 150,078 | 238 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 27,976 | 0.280 | 20 | 200 | fits | 27,442 | 19 | 0.820 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 297,185 | 2.972 | 20 | 20 | fits | 150,078 | 238 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 396,952 | 3.970 | 20 | 20 | fits | 91,646 | 148 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 150,747 | 1.507 | 20 | 24 | fits | 150,933 | 155 | 0.351 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 299,835 | 2.998 | 20 | 24 | fits | 150,078 | 238 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 299,769 | 2.998 | 20 | 50 | fits | 150,078 | 238 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 399,976 | 4.000 | 20 | 50 | fits | 91,646 | 148 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 485,410 | 4.854 | 20 | 20 | fits | 85,500 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 981,711 | 9.817 | 20 | 20 | fits | 73,604 | 24 | 0.671 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,876 | 0.059 | 20 | 20 | fits | 24,667 | 13 (29) | 0.806 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,603 | 0.076 | 20 | 20 | fits | 26,529 | 19 (35) | 0.804 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 10,828 | 0.108 | 20 | 20 | fits | 29,566 | 21 (12) | 0.818 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 26,823 | 43 (11) | 0.735 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,339 | 0.183 | 20 | 200 | fits | 23,214 | 23 (39) | 0.757 |
| LINK_DOWN | `adp.link_down.if0` | 2,352 | 0.024 | 20 | 200 | fits | 24,597 | 23 (9) | 0.782 |
| LINK_UP | `adp.link_up.if0` | 2,571 | 0.026 | 20 | 200 | fits | 26,823 | 43 (11) | 0.735 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,339 | 0.183 | 20 | 200 | fits | 23,214 | 23 (39) | 0.757 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,535 | 0.045 | 20 | 200 | fits | 16,961 | 16 (31) | 0.655 |
| set_name | `aecp_fanout.set_name.if0` | 46,583 | 0.466 | 20 | 24 | fits | 62,439 | 89 | 0.575 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 44,536 | 0.445 | 20 | 24 | fits | 56,816 | 78 | 0.602 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 47,183 | 0.472 | 20 | 24 | fits | 54,650 | 79 | 0.563 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,443 | 0.404 | 20 | 24 | fits | 51,535 | 78 | 0.555 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 50,298 | 0.503 | 20 | 24 | fits | 60,790 | 66 | 0.636 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 265,995 | 2.660 | 20 | 24 | fits | 58,535 | 65 | 0.632 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 341,482 | 3.415 | 20 | 24 | fits | 54,099 | 67 | 0.594 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 39,730 | 0.397 | 20 | 24 | fits | 50,692 | 78 | 0.549 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,463 | 0.455 | 20 | 24 | fits | 50,975 | 79 | 0.551 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 24,313 | 0.243 | 20 | 24 | fits | 28,096 | 20 | 0.777 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 18,586 | 0.186 | 20 | 24 | fits | 32,560 | 20 | 0.719 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 25,434 | 0.254 | 20 | 24 | fits | 27,567 | 20 | 0.732 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 14,412 | 0.144 | 20 | 24 | fits | 27,479 | 20 | 0.729 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 25,466 | 0.255 | 20 | 24 | fits | 27,536 | 20 | 0.725 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 25,678 | 0.257 | 20 | 24 | fits | 27,755 | 20 | 0.731 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 13,627 | 0.136 | 20 | 24 | fits | 26,762 | 20 | 0.729 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 24,951 | 0.250 | 20 | 24 | fits | 26,942 | 20 | 0.742 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 12,895 | 0.129 | 20 | 24 | fits | 26,301 | 20 | 0.742 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 27,194 | 0.272 | 20 | 24 | fits | 29,185 | 21 | 0.641 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 13,886 | 0.139 | 20 | 24 | fits | 26,220 | 20 | 0.765 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 13,033 | 0.130 | 20 | 24 | fits | 26,441 | 20 | 0.764 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 24,658 | 0.247 | 20 | 24 | fits | 26,649 | 20 | 0.727 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 13,955 | 0.140 | 20 | 24 | fits | 27,598 | 20 | 0.735 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 24,888 | 0.249 | 20 | 24 | fits | 27,045 | 20 | 0.742 |
| get_configuration | `aecp.get_configuration.if0` | 12,021 | 0.120 | 20 | 24 | fits | 24,235 | 20 | 0.739 |
| entity_available | `aecp.entity_available.if0` | 22,413 | 0.224 | 20 | 24 | fits | 23,843 | 20 | 0.719 |
| get_name | `aecp.get_name.if0` | 10,973 | 0.110 | 20 | 24 | fits | 27,579 | 20 | 0.751 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 14,546 | 0.145 | 20 | 24 | fits | 27,796 | 27 | 0.715 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 26,088 | 0.261 | 20 | 24 | fits | 28,249 | 29 | 0.754 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 12,150 | 0.121 | 20 | 24 | fits | 25,102 | 20 | 0.757 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 15,325 | 0.153 | 20 | 24 | fits | 23,966 | 20 | 0.723 |
| set_name | `aecp.set_name.if0` | 20,955 | 0.210 | 20 | 24 | fits | 43,866 | 43 | 0.757 |
| lock_entity | `aecp.lock_entity.if0` | 17,755 | 0.178 | 20 | 24 | fits | 35,549 | 34 | 0.777 |
| unlock_entity | `aecp.unlock_entity.if0` | 15,210 | 0.152 | 20 | 24 | fits | 36,545 | 33 | 0.782 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

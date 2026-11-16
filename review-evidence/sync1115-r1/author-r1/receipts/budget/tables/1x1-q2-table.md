### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 61 paths and 0 of 218 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.071 (0.253) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.062 (0.231) | fits | 0 adp | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.135 (0.466) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.044 (0.159) | fits | 0 adp | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.024 (0.250) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.028 (0.264) | fits | 0 events | 3 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.029 (0.175) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.174 (0.464) | fits | 0 events | 3 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.177 (0.464) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.212 (0.514) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.093 (0.234) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.115 (0.275) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.114 (0.263) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.269 (0.652) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.178 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.159 (0.307) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.198 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.199 (0.490) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.107 (0.250) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.221 (0.512) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.105 (0.247) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.099 (0.254) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.114 (0.258) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.197 (0.496) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.119 (0.265) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.198 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.116 (0.320) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.205 (0.503) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.114 (0.402) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.168 (0.458) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.282 (0.667) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.099 (0.241) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.199 (0.537) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.221 (2.505) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.527 (0.817) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.494 (0.781) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.558 (0.845) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.522 (0.796) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.568 (0.872) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.391 (2.691) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.422 (0.682) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.229 (4.608) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-aged2-6.adp_available.if0` (backlog-adp@verify-aged2-6) | 3.698 (4.344) | fits | 7 adp | 13 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.117 (0.446) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.664 (2.070) | fits | 15 events | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.245 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 1.553 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.910 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.850 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.320 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.442 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.138 | fits | 0 acmp | 15 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 4.555 | fits | 11 acmp | 15 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.181 | fits | 0 adp | 15 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.adp.last.if0` (backlog-adp@program-aged2-6) | 4.252 | fits | 7 adp | 15 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-6.service.aecp.first.if0` (backlog-adp@verify-aged2-6) | 1.647 | fits | 0 aecp | 15 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.164 | fits | 15 aecp | 15 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.164 | fits | 0 maap | 15 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.maap.last.if0` (backlog-adp@program-aged2-6) | 4.290 | fits | 6 maap | 15 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 5.990 | fits | 0 srp | 15 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-6.service.srp.last.if0` (backlog-adp@verify-aged2-6) | 9.955 | fits | 31 srp | 15 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-aged2-6 | 0 | 10.370 | 10 | 147,787 (1.478) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.612 | 11 | 149,528 (1.495) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.499 | 12 | 147,984 (1.480) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.397 | 10 | 147,778 (1.478) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 10.348 | 10 | 147,778 (1.478) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.299 | 11 | 147,835 (1.478) | yes | - |
| backlog-adp@verify-aged2-2 | 1 | 10.254 | 9 | 144,388 (1.444) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 10.345 | 10 | 147,778 (1.478) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.447 | 11 | 147,467 (1.475) | yes | - |
| backlog-adp@verify-aged1-0 | 1 | 11.358 | 11 | 144,092 (1.441) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.339 | 10 | 147,844 (1.478) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.300 | 10 | 147,844 (1.478) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.259 | 10 | 147,844 (1.478) | yes | - |
| backlog | 0 | 5.679 | 7 | 151,519 (1.515) | yes | - |
| backlog-adp-refill | 0 | 40.746 | 24 | 149,643 (1.496) | yes | - |

Composed maximum over 2 of 4 backlog windows, a partial figure (backlog-adp, backlog-owed not run): 151,519 CPU cycles (1.515 ms), backlog.
Over the windows that released their whole load only: 151,519 (1.515 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@program-aged2-6 | 860 | 0 | 147,787 (1.478) | fits |
| backlog-adp@program-aged1-0 | 747 | 0 | 149,528 (1.495) | fits |
| backlog-adp@program-aged1-2 | 764 | 0 | 147,984 (1.480) | fits |
| backlog-adp@program-aged1-4 | 779 | 0 | 147,778 (1.478) | fits |
| backlog-adp@program-aged1-6 | 795 | 0 | 147,778 (1.478) | fits |
| backlog-adp@verify-aged2-0 | 902 | 0 | 147,835 (1.478) | fits |
| backlog-adp@verify-aged2-2 | 917 | 0 | 147,835 (1.478) | fits |
| backlog-adp@verify-aged2-4 | 934 | 0 | 147,778 (1.478) | fits |
| backlog-adp@verify-aged2-6 | 951 | 0 | 147,467 (1.475) | fits |
| backlog-adp@verify-aged1-0 | 838 | 0 | 147,953 (1.480) | fits |
| backlog-adp@verify-aged1-2 | 853 | 0 | 147,844 (1.478) | fits |
| backlog-adp@verify-aged1-4 | 869 | 0 | 147,844 (1.478) | fits |
| backlog-adp@verify-aged1-6 | 885 | 0 | 147,844 (1.478) | fits |
| adp-advertise | 598 | 0 | 41,738 (0.417) | fits |
| save-starved | 26724 | 0 | 156,249 (1.562) | fits |
| save | 609 | 0 | 44,323 (0.443) | fits |
| backlog | 285 | 0 | 151,519 (1.515) | fits |
| backlog-adp-refill | 325 | 0 | 149,643 (1.496) | fits |
| acmp-disc | 937 | 0 | 41,738 (0.417) | fits |
| adp-link | 90 | 0 | 46,247 (0.462) | fits |
| adp-discover | 89 | 0 | 41,738 (0.417) | fits |
| aecp-fanout | 113 | 0 | 62,223 (0.622) | fits |
| aecp | 111 | 0 | 43,402 (0.434) | fits |
| datapath-events | 118 | 0 | 41,738 (0.417) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@program-aged2-6 | 2 | +4.306 ms, 80,180 (0.802 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 9.874 (20) | 10.126 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.926 (20) | 11.074 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.921 (20) | 11.079 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.100 (20) | 10.900 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.047 (20) | 10.953 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.956 (20) | 11.044 |
| backlog-adp@verify-aged2-2 | 2 | +8.495 ms, 77,251 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 9.755 (20) | 10.245 |
| backlog-adp@verify-aged2-4 | 2 | +6.060 ms, 77,251 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.849 (20) | 10.151 |
| backlog-adp@verify-aged2-6 | 2 | +4.260 ms, 77,273 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 9.955 (20) | 10.045 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.864 (20) | 11.136 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.085 (20) | 10.915 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.046 (20) | 10.954 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.001 (20) | 10.999 |

Least margin over the aged windows: 10.045 ms, `backlog-adp@verify-aged2-6.service.srp.last.if0` at 9.955 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 4048.331 | 4,070 | 102 | - | 30.835 | yes | within |
| save | 2018.784 | 4,070 | 102 | - | 10.987 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@program-aged2-6 | 326 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@program-aged1-0 | 327 | 95,454 (0.955) | 78,959 (0.790) |
| backlog-adp@program-aged1-2 | 326 | 95,561 (0.956) | 78,632 (0.786) |
| backlog-adp@program-aged1-4 | 326 | 95,454 (0.955) | 78,828 (0.788) |
| backlog-adp@program-aged1-6 | 326 | 95,454 (0.955) | 78,959 (0.790) |
| backlog-adp@verify-aged2-0 | 356 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged2-2 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged2-4 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged2-6 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged1-0 | 356 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged1-2 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged1-4 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-aged1-6 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| adp-advertise | 578 | 21,172 (0.212) | 2,067 (0.021) |
| save-starved | 418 | 80,341 (0.803) | 77,974 (0.780) |
| save | 585 | 94,531 (0.945) | 77,757 (0.778) |
| backlog | 265 | 21,172 (0.212) | 2,067 (0.021) |
| backlog-adp-refill | 274 | 21,172 (0.212) | 2,340 (0.023) |
| acmp-disc | 305 | 95,462 (0.955) | 78,036 (0.780) |
| adp-link | 80 | 21,172 (0.212) | 2,067 (0.021) |
| adp-discover | 80 | 21,172 (0.212) | 2,067 (0.021) |
| aecp-fanout | 80 | 21,172 (0.212) | 2,067 (0.021) |
| aecp | 79 | 21,172 (0.212) | 2,067 (0.021) |
| datapath-events | 70 | 21,172 (0.212) | 2,067 (0.021) |

Longest pass that carries a step: 95,561 CPU cycles (0.956 ms), backlog-adp@program-aged1-2; longest step: 78,959 (0.790 ms), backlog-adp@program-aged1-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 366,492 | 3.665 | 20 | 20 | fits | 120,365 | 176 | 0.475 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 296,983 | 2.970 | 20 | 200 | fits | 143,979 | 227 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 425,236 | 4.252 | 20 | 200 | fits | 120,365 | 176 | 0.475 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 297,907 | 2.979 | 20 | 20 | fits | 143,979 | 227 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 425,940 | 4.259 | 20 | 20 | fits | 120,365 | 176 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 157,568 | 1.576 | 20 | 24 | fits | 147,787 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 300,557 | 3.006 | 20 | 24 | fits | 143,979 | 227 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 300,491 | 3.005 | 20 | 50 | fits | 143,979 | 227 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 428,964 | 4.290 | 20 | 50 | fits | 120,365 | 176 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 598,968 | 5.990 | 20 | 20 | fits | 89,890 | 29 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 987,396 | 9.874 | 20 | 20 | fits | 52,507 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 341,234 | 3.412 | 20 | 20 | fits | 102,846 | 143 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 296,708 | 2.967 | 20 | 200 | fits | 149,528 | 248 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 398,938 | 3.989 | 20 | 200 | fits | 102,846 | 143 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 297,632 | 2.976 | 20 | 20 | fits | 149,528 | 248 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 399,642 | 3.996 | 20 | 20 | fits | 102,846 | 143 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 151,744 | 1.517 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 300,282 | 3.003 | 20 | 24 | fits | 149,528 | 248 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 300,216 | 3.002 | 20 | 50 | fits | 149,528 | 248 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 402,666 | 4.027 | 20 | 50 | fits | 102,846 | 143 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 504,400 | 5.044 | 20 | 20 | fits | 93,095 | 35 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 892,573 | 8.926 | 20 | 20 | fits | 52,491 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 345,680 | 3.457 | 20 | 20 | fits | 108,977 | 163 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 295,516 | 2.955 | 20 | 200 | fits | 144,526 | 231 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 403,877 | 4.039 | 20 | 200 | fits | 108,977 | 163 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 296,440 | 2.964 | 20 | 20 | fits | 144,526 | 231 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 404,581 | 4.046 | 20 | 20 | fits | 108,977 | 163 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 148,156 | 1.482 | 20 | 24 | fits | 147,984 | 153 | 0.337 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 299,090 | 2.991 | 20 | 24 | fits | 144,526 | 231 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 299,024 | 2.990 | 20 | 50 | fits | 144,526 | 231 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 407,605 | 4.076 | 20 | 50 | fits | 108,977 | 163 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 497,278 | 4.973 | 20 | 20 | fits | 89,739 | 28 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 892,062 | 8.921 | 20 | 20 | fits | 52,689 | 20 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 348,087 | 3.481 | 20 | 20 | fits | 108,763 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 298,118 | 2.981 | 20 | 200 | fits | 143,831 | 226 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 406,265 | 4.063 | 20 | 200 | fits | 108,763 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 299,042 | 2.990 | 20 | 20 | fits | 143,831 | 226 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 406,969 | 4.070 | 20 | 20 | fits | 108,763 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 158,851 | 1.589 | 20 | 24 | fits | 147,778 | 152 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 301,692 | 3.017 | 20 | 24 | fits | 143,831 | 226 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 301,626 | 3.016 | 20 | 50 | fits | 143,831 | 226 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 409,993 | 4.100 | 20 | 50 | fits | 108,763 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 499,603 | 4.996 | 20 | 20 | fits | 89,676 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 910,016 | 9.100 | 20 | 20 | fits | 52,583 | 20 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 360,059 | 3.601 | 20 | 20 | fits | 117,356 | 170 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 294,282 | 2.943 | 20 | 200 | fits | 143,723 | 226 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 411,022 | 4.110 | 20 | 200 | fits | 117,356 | 170 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 295,206 | 2.952 | 20 | 20 | fits | 143,723 | 226 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 411,726 | 4.117 | 20 | 20 | fits | 117,356 | 170 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 155,123 | 1.551 | 20 | 24 | fits | 147,778 | 152 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 297,856 | 2.979 | 20 | 24 | fits | 143,723 | 226 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 297,790 | 2.978 | 20 | 50 | fits | 143,723 | 226 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 414,750 | 4.147 | 20 | 50 | fits | 117,356 | 170 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 516,454 | 5.165 | 20 | 20 | fits | 92,847 | 35 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 904,709 | 9.047 | 20 | 20 | fits | 52,491 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 339,693 | 3.397 | 20 | 20 | fits | 108,234 | 163 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 289,655 | 2.897 | 20 | 200 | fits | 143,769 | 226 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 397,273 | 3.973 | 20 | 200 | fits | 108,234 | 163 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 290,579 | 2.906 | 20 | 20 | fits | 143,769 | 226 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 397,977 | 3.980 | 20 | 20 | fits | 108,234 | 163 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 150,450 | 1.504 | 20 | 24 | fits | 147,835 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 293,229 | 2.932 | 20 | 24 | fits | 143,769 | 226 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 293,163 | 2.932 | 20 | 50 | fits | 143,769 | 226 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 401,001 | 4.010 | 20 | 50 | fits | 108,234 | 163 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 490,884 | 4.909 | 20 | 20 | fits | 89,949 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 895,568 | 8.956 | 20 | 20 | fits | 54,253 | 21 | 0.705 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 335,956 | 3.360 | 20 | 20 | fits | 108,343 | 163 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 285,622 | 2.856 | 20 | 200 | fits | 144,388 | 231 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 393,349 | 3.933 | 20 | 200 | fits | 108,343 | 163 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 286,546 | 2.865 | 20 | 20 | fits | 144,388 | 231 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 394,053 | 3.941 | 20 | 20 | fits | 108,343 | 163 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 145,798 | 1.458 | 20 | 24 | fits | 147,835 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 289,196 | 2.892 | 20 | 24 | fits | 144,388 | 231 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 289,130 | 2.891 | 20 | 50 | fits | 144,388 | 231 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 397,077 | 3.971 | 20 | 50 | fits | 108,343 | 163 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 487,050 | 4.870 | 20 | 20 | fits | 90,039 | 28 | 0.718 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 975,521 | 9.755 | 20 | 20 | fits | 52,505 | 21 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 359,532 | 3.595 | 20 | 20 | fits | 112,837 | 170 | 0.465 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 297,727 | 2.977 | 20 | 200 | fits | 143,962 | 227 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 418,404 | 4.184 | 20 | 200 | fits | 112,837 | 170 | 0.465 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 298,651 | 2.987 | 20 | 20 | fits | 143,962 | 227 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 419,108 | 4.191 | 20 | 20 | fits | 112,837 | 170 | 0.465 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 158,329 | 1.583 | 20 | 24 | fits | 147,778 | 152 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 301,301 | 3.013 | 20 | 24 | fits | 143,962 | 227 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 301,235 | 3.012 | 20 | 50 | fits | 143,962 | 227 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 422,132 | 4.221 | 20 | 50 | fits | 112,837 | 170 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 512,685 | 5.127 | 20 | 20 | fits | 90,619 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 984,879 | 9.849 | 20 | 20 | fits | 52,507 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 369,826 | 3.698 | 20 | 20 | fits | 117,268 | 169 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 303,978 | 3.040 | 20 | 200 | fits | 143,891 | 226 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 420,630 | 4.206 | 20 | 200 | fits | 117,268 | 169 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 304,902 | 3.049 | 20 | 20 | fits | 143,891 | 226 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 421,334 | 4.213 | 20 | 20 | fits | 117,268 | 169 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 164,651 | 1.647 | 20 | 24 | fits | 147,467 | 153 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 307,552 | 3.076 | 20 | 24 | fits | 143,891 | 226 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 307,486 | 3.075 | 20 | 50 | fits | 143,891 | 226 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 424,358 | 4.244 | 20 | 50 | fits | 117,268 | 169 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 591,318 | 5.913 | 20 | 20 | fits | 89,753 | 29 | 0.714 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 995,533 | 9.955 | 20 | 20 | fits | 52,962 | 20 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 346,024 | 3.460 | 20 | 20 | fits | 112,227 | 169 | 0.458 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 292,842 | 2.928 | 20 | 200 | fits | 144,092 | 231 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 404,453 | 4.045 | 20 | 200 | fits | 112,227 | 169 | 0.458 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 293,766 | 2.938 | 20 | 20 | fits | 144,092 | 231 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 405,157 | 4.052 | 20 | 20 | fits | 112,227 | 169 | 0.458 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 145,916 | 1.459 | 20 | 24 | fits | 147,953 | 153 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 296,416 | 2.964 | 20 | 24 | fits | 144,092 | 231 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 296,350 | 2.963 | 20 | 50 | fits | 144,092 | 231 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 408,181 | 4.082 | 20 | 50 | fits | 112,227 | 169 | 0.458 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 498,625 | 4.986 | 20 | 20 | fits | 90,510 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 886,356 | 8.864 | 20 | 20 | fits | 52,507 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 347,521 | 3.475 | 20 | 20 | fits | 108,789 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 297,552 | 2.976 | 20 | 200 | fits | 143,688 | 226 | 0.394 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 405,725 | 4.057 | 20 | 200 | fits | 108,789 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 298,476 | 2.985 | 20 | 20 | fits | 143,688 | 226 | 0.394 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 406,429 | 4.064 | 20 | 20 | fits | 108,789 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 158,428 | 1.584 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 301,126 | 3.011 | 20 | 24 | fits | 143,688 | 226 | 0.394 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 301,060 | 3.011 | 20 | 50 | fits | 143,688 | 226 | 0.394 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 409,453 | 4.095 | 20 | 50 | fits | 108,789 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 499,315 | 4.993 | 20 | 20 | fits | 89,928 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 908,534 | 9.085 | 20 | 20 | fits | 63,652 | 24 | 0.609 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 351,231 | 3.512 | 20 | 20 | fits | 108,778 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 293,716 | 2.937 | 20 | 200 | fits | 143,580 | 226 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 401,878 | 4.019 | 20 | 200 | fits | 108,778 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 294,640 | 2.946 | 20 | 20 | fits | 143,580 | 226 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 402,582 | 4.026 | 20 | 20 | fits | 108,778 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 154,700 | 1.547 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 297,290 | 2.973 | 20 | 24 | fits | 143,580 | 226 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 297,224 | 2.972 | 20 | 50 | fits | 143,580 | 226 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 405,606 | 4.056 | 20 | 50 | fits | 108,778 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 495,688 | 4.957 | 20 | 20 | fits | 90,148 | 29 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 904,640 | 9.046 | 20 | 20 | fits | 63,195 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 360,268 | 3.603 | 20 | 20 | fits | 120,204 | 176 | 0.475 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 290,325 | 2.903 | 20 | 200 | fits | 143,917 | 227 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 418,369 | 4.184 | 20 | 200 | fits | 120,204 | 176 | 0.475 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 291,249 | 2.912 | 20 | 20 | fits | 143,917 | 227 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 419,073 | 4.191 | 20 | 20 | fits | 120,204 | 176 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 150,972 | 1.510 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 293,899 | 2.939 | 20 | 24 | fits | 143,917 | 227 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 293,833 | 2.938 | 20 | 50 | fits | 143,917 | 227 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 422,097 | 4.221 | 20 | 50 | fits | 120,204 | 176 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 512,325 | 5.123 | 20 | 20 | fits | 90,294 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 900,076 | 9.001 | 20 | 20 | fits | 52,491 | 20 | 0.648 |
| LINK_UP | `adp.link_up.if0` | 2,785 | 0.028 | 20 | 200 | fits | 26,390 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,387 | 0.174 | 20 | 200 | fits | 21,319 | 23 (39) | 0.714 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 2,926 | 0.029 | 20 | 200 | fits | 2,871 | 10 (11) | 0.613 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 155,309 | 1.553 | 20 | 200 | fits | 156,249 | 251 | 0.470 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 224,463 | 2.245 | 20 | 20 | fits | 89,291 | 88 | 0.671 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 291,040 | 2.910 | 20 | 24 | fits | 90,754 | 59 | 0.534 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 184,988 | 1.850 | 20 | 50 | fits | 89,291 | 88 | 0.671 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 832,029 | 8.320 | 20 | 20 | fits | 82,285 | 40 | 0.600 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 244,211 | 2.442 | 20 | 20 | fits | 0 | - | 0.000 |
| an event behind 15 others | `backlog.event.if0` | 166,364 | 1.664 | 20 | 200 | fits | 55,472 | 78 | 0.540 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 422,870 | 4.229 | 20 | 20 | fits | 42,502 | 63 | 0.327 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 418,110 | 4.181 | 20 | 200 | fits | 144,743 | 158 | 0.420 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 417,494 | 4.175 | 20 | 200 | fits | 144,743 | 158 | 0.420 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 413,788 | 4.138 | 20 | 20 | fits | 144,743 | 158 | 0.420 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 455,454 | 4.555 | 20 | 20 | fits | 42,502 | 63 | 0.327 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 150,628 | 1.506 | 20 | 24 | fits | 151,519 | 158 | 0.339 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 416,438 | 4.164 | 20 | 24 | fits | 144,743 | 158 | 0.420 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 416,372 | 4.164 | 20 | 50 | fits | 144,743 | 158 | 0.420 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 415,976 | 4.160 | 20 | 50 | fits | 144,743 | 158 | 0.420 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 458,412 | 4.584 | 20 | 20 | fits | 42,502 | 63 | 0.327 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 521,412 | 5.214 | 20 | 20 | fits | 25,879 | 41 | 0.182 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,731 | 0.117 | 20 | 20 | fits | 25,898 | 19 | 0.805 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 292,894 | 2.929 | 20 | 200 | fits | 149,643 | 248 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 29,869 | 0.299 | 20 | 200 | fits | 25,898 | 19 | 0.805 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 293,818 | 2.938 | 20 | 20 | fits | 149,643 | 248 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 390,706 | 3.907 | 20 | 20 | fits | 97,724 | 139 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 147,815 | 1.478 | 20 | 24 | fits | 148,001 | 155 | 0.338 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 296,468 | 2.965 | 20 | 24 | fits | 149,643 | 248 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 296,402 | 2.964 | 20 | 50 | fits | 149,643 | 248 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 393,730 | 3.937 | 20 | 50 | fits | 97,724 | 139 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 491,713 | 4.917 | 20 | 20 | fits | 89,574 | 29 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 886,953 | 8.870 | 20 | 20 | fits | 52,486 | 20 | 0.648 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,177 | 0.062 | 20 | 20 | fits | 23,137 | 13 (29) | 0.795 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,145 | 0.071 | 20 | 20 | fits | 25,257 | 19 (35) | 0.795 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 13,507 | 0.135 | 20 | 20 | fits | 27,832 | 21 (12) | 0.809 |
| LINK_UP | `adp.link_up.if0` | 2,785 | 0.028 | 20 | 200 | fits | 26,390 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,387 | 0.174 | 20 | 200 | fits | 21,319 | 23 (39) | 0.714 |
| LINK_DOWN | `adp.link_down.if0` | 2,426 | 0.024 | 20 | 200 | fits | 24,982 | 23 (9) | 0.759 |
| LINK_UP | `adp.link_up.if0` | 2,785 | 0.028 | 20 | 200 | fits | 26,390 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,387 | 0.174 | 20 | 200 | fits | 21,319 | 23 (39) | 0.714 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,393 | 0.044 | 20 | 200 | fits | 15,870 | 16 (31) | 0.659 |
| set_name | `aecp_fanout.set_name.if0` | 56,787 | 0.568 | 20 | 24 | fits | 62,223 | 89 | 0.566 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 55,753 | 0.558 | 20 | 24 | fits | 55,680 | 78 | 0.596 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 45,538 | 0.455 | 20 | 24 | fits | 54,105 | 79 | 0.571 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 52,157 | 0.522 | 20 | 24 | fits | 49,718 | 78 | 0.540 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 49,426 | 0.494 | 20 | 24 | fits | 60,712 | 66 | 0.636 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 222,085 | 2.221 | 20 | 24 | fits | 58,123 | 65 | 0.629 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 239,118 | 2.391 | 20 | 24 | fits | 53,334 | 67 | 0.589 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 52,710 | 0.527 | 20 | 24 | fits | 50,344 | 78 | 0.559 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 42,240 | 0.422 | 20 | 24 | fits | 49,632 | 79 | 0.541 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 16,824 | 0.168 | 20 | 24 | fits | 26,581 | 20 | 0.782 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 15,905 | 0.159 | 20 | 24 | fits | 30,671 | 20 | 0.710 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 19,835 | 0.198 | 20 | 24 | fits | 25,729 | 20 | 0.720 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 11,425 | 0.114 | 20 | 24 | fits | 25,766 | 20 | 0.723 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 11,591 | 0.116 | 20 | 24 | fits | 31,953 | 26 | 0.717 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 20,506 | 0.205 | 20 | 24 | fits | 26,329 | 20 | 0.721 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 11,364 | 0.114 | 20 | 24 | fits | 25,448 | 20 | 0.727 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 19,875 | 0.199 | 20 | 24 | fits | 25,698 | 20 | 0.735 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 10,686 | 0.107 | 20 | 24 | fits | 24,987 | 20 | 0.740 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 22,068 | 0.221 | 20 | 24 | fits | 27,830 | 21 | 0.638 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 10,487 | 0.105 | 20 | 24 | fits | 24,693 | 20 | 0.758 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 9,949 | 0.099 | 20 | 24 | fits | 25,379 | 20 | 0.758 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 19,722 | 0.197 | 20 | 24 | fits | 25,500 | 20 | 0.725 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 11,894 | 0.119 | 20 | 24 | fits | 26,488 | 20 | 0.731 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 19,752 | 0.198 | 20 | 24 | fits | 25,717 | 20 | 0.735 |
| get_configuration | `aecp.get_configuration.if0` | 9,324 | 0.093 | 20 | 24 | fits | 23,391 | 20 | 0.747 |
| entity_available | `aecp.entity_available.if0` | 17,684 | 0.177 | 20 | 24 | fits | 23,043 | 20 | 0.728 |
| get_name | `aecp.get_name.if0` | 11,402 | 0.114 | 20 | 24 | fits | 26,331 | 20 | 0.757 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 11,494 | 0.115 | 20 | 24 | fits | 27,463 | 25 | 0.730 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 21,195 | 0.212 | 20 | 24 | fits | 27,105 | 27 | 0.760 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 9,881 | 0.099 | 20 | 24 | fits | 24,053 | 20 | 0.762 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 17,818 | 0.178 | 20 | 24 | fits | 23,430 | 20 | 0.740 |
| set_name | `aecp.set_name.if0` | 28,215 | 0.282 | 20 | 24 | fits | 43,402 | 43 | 0.756 |
| lock_entity | `aecp.lock_entity.if0` | 26,905 | 0.269 | 20 | 24 | fits | 33,661 | 34 | 0.768 |
| unlock_entity | `aecp.unlock_entity.if0` | 19,875 | 0.199 | 20 | 24 | fits | 34,506 | 33 | 0.773 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 62 paths and 0 of 472 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.083 (0.248) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.063 (0.225) | fits | 0 adp | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.216 (0.547) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.143 (0.549) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.046 (0.162) | fits | 0 adp | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.023 (0.251) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.026 (0.263) | fits | 0 events | 3 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.104 (0.255) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.174 (0.470) | fits | 0 events | 3 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.148 (0.442) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.186 (0.486) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.106 (0.403) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.138 (0.439) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.239 (0.541) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.252 (0.594) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.146 (0.441) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.175 (0.478) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.171 (0.473) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.168 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.121 (0.421) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.192 (0.489) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.118 (0.418) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.202 (0.500) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.127 (0.429) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.229 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.130 (0.432) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.166 (0.468) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.216 (0.517) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.236 (0.538) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.126 (0.426) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.209 (0.508) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.283 (0.684) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.110 (0.409) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.217 (0.573) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.467 (2.757) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.403 (0.499) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.518 (0.809) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.426 (0.554) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.482 (0.743) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.573 (0.889) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.197 (2.500) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.448 (0.708) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.335 (4.726) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-0.adp_available.if0` (backlog-adp@blank-0) | 4.356 (5.829) | fits | 7 adp | 36 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.208 (0.527) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.628 (2.053) | fits | 15 events | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.279 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 1.504 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.944 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.319 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.777 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.568 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.186 | fits | 0 acmp | 38 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.acmp.last.if0` (backlog-adp@blank-0) | 4.945 | fits | 11 acmp | 38 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.229 | fits | 0 adp | 38 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.adp.last.if0` (backlog-adp@blank-0) | 4.938 | fits | 7 adp | 38 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.306 | fits | 0 aecp | 38 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.212 | fits | 15 aecp | 38 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.212 | fits | 0 maap | 38 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.975 | fits | 6 maap | 38 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-6.service.srp.first.if0` (backlog-adp@program-aged2-6) | 6.111 | fits | 0 srp | 38 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-2.service.srp.last.if0` (backlog-adp@blank-aged1-2) | 10.102 | fits | 31 srp | 38 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 11.444 | 11 | 144,611 (1.446) | yes | - |
| backlog-adp@blank-2 | 0 | 10.466 | 10 | 144,592 (1.446) | yes | - |
| backlog-adp@blank-4 | 0 | 10.506 | 10 | 145,488 (1.455) | yes | - |
| backlog-adp@blank-6 | 0 | 10.636 | 10 | 146,069 (1.461) | yes | - |
| backlog-adp@program-0 | 0 | 10.689 | 11 | 145,218 (1.452) | yes | - |
| backlog-adp@program-2 | 1 | 10.495 | 9 | 145,794 (1.458) | yes | - |
| backlog-adp@program-4 | 0 | 9.873 | 11 | 144,538 (1.445) | yes | - |
| backlog-adp@program-6 | 0 | 9.757 | 10 | 145,140 (1.451) | yes | - |
| backlog-adp@verify-0 | 0 | 10.932 | 11 | 145,159 (1.452) | yes | - |
| backlog-adp@verify-2 | 0 | 10.559 | 10 | 145,297 (1.453) | yes | - |
| backlog-adp@verify-4 | 0 | 10.974 | 11 | 144,153 (1.442) | yes | - |
| backlog-adp@verify-6 | 0 | 10.589 | 10 | 144,084 (1.441) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 10.459 | 10 | 146,152 (1.462) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 10.595 | 11 | 145,159 (1.452) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 10.550 | 10 | 144,278 (1.443) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 10.430 | 10 | 144,278 (1.443) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.390 | 13 | 145,256 (1.453) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 11.360 | 12 | 144,497 (1.445) | yes | - |
| backlog-adp@blank-aged1-4 | 1 | 11.403 | 12 | 145,683 (1.457) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 11.354 | 12 | 145,155 (1.452) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.976 | 12 | 146,513 (1.465) | yes | - |
| backlog-adp@program-aged2-2 | 1 | 10.464 | 9 | 146,539 (1.465) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.498 | 10 | 144,456 (1.445) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 10.555 | 10 | 145,395 (1.454) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 10.782 | 10 | 146,617 (1.466) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 10.745 | 12 | 145,297 (1.453) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.571 | 10 | 144,520 (1.445) | yes | - |
| backlog-adp@program-aged1-6 | 1 | 10.479 | 9 | 145,880 (1.459) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.496 | 11 | 145,223 (1.452) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 10.529 | 10 | 144,579 (1.446) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.104 | 11 | 146,210 (1.462) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 10.590 | 11 | 145,143 (1.451) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.628 | 12 | 145,173 (1.452) | yes | - |
| backlog-adp@verify-aged1-2 | 0 | 10.411 | 9 | 145,132 (1.451) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.447 | 10 | 144,515 (1.445) | yes | - |
| backlog-adp@verify-aged1-6 | 0 | 10.515 | 10 | 145,375 (1.454) | yes | - |
| backlog | 0 | 5.820 | 7 | 149,348 (1.493) | yes | - |
| backlog-adp-refill | 0 | 40.827 | 25 | 144,750 (1.448) | yes | - |

Composed maximum over 2 of 4 backlog windows, a partial figure (backlog-adp, backlog-owed not run): 149,348 CPU cycles (1.493 ms), backlog.
Over the windows that released their whole load only: 149,348 (1.493 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3609 | 0 | 41,923 (0.419) | fits |
| backlog-adp@blank-0 | 406 | 0 | 144,611 (1.446) | fits |
| backlog-adp@blank-2 | 405 | 0 | 144,592 (1.446) | fits |
| backlog-adp@blank-4 | 405 | 0 | 145,488 (1.455) | fits |
| backlog-adp@blank-6 | 406 | 0 | 146,069 (1.461) | fits |
| backlog-adp@program-0 | 502 | 0 | 145,218 (1.452) | fits |
| backlog-adp@program-2 | 502 | 0 | 145,794 (1.458) | fits |
| backlog-adp@program-4 | 505 | 0 | 144,538 (1.445) | fits |
| backlog-adp@program-6 | 506 | 0 | 145,140 (1.451) | fits |
| backlog-adp@verify-0 | 590 | 0 | 145,159 (1.452) | fits |
| backlog-adp@verify-2 | 589 | 0 | 145,297 (1.453) | fits |
| backlog-adp@verify-4 | 591 | 0 | 144,153 (1.442) | fits |
| backlog-adp@verify-6 | 591 | 0 | 144,084 (1.441) | fits |
| backlog-adp@blank-aged2-0 | 729 | 0 | 148,930 (1.489) | fits |
| backlog-adp@blank-aged2-2 | 742 | 0 | 145,159 (1.452) | fits |
| backlog-adp@blank-aged2-4 | 758 | 0 | 144,278 (1.443) | fits |
| backlog-adp@blank-aged2-6 | 774 | 0 | 144,278 (1.443) | fits |
| backlog-adp@blank-aged1-0 | 665 | 0 | 145,256 (1.453) | fits |
| backlog-adp@blank-aged1-2 | 681 | 0 | 144,497 (1.445) | fits |
| backlog-adp@blank-aged1-4 | 698 | 0 | 145,683 (1.457) | fits |
| backlog-adp@blank-aged1-6 | 714 | 0 | 145,155 (1.452) | fits |
| backlog-adp@program-aged2-0 | 822 | 0 | 146,513 (1.465) | fits |
| backlog-adp@program-aged2-2 | 836 | 0 | 146,539 (1.465) | fits |
| backlog-adp@program-aged2-4 | 853 | 0 | 144,456 (1.445) | fits |
| backlog-adp@program-aged2-6 | 870 | 0 | 145,395 (1.454) | fits |
| backlog-adp@program-aged1-0 | 754 | 0 | 146,617 (1.466) | fits |
| backlog-adp@program-aged1-2 | 772 | 0 | 145,297 (1.453) | fits |
| backlog-adp@program-aged1-4 | 787 | 0 | 144,520 (1.445) | fits |
| backlog-adp@program-aged1-6 | 803 | 0 | 145,880 (1.459) | fits |
| backlog-adp@verify-aged2-0 | 909 | 0 | 145,223 (1.452) | fits |
| backlog-adp@verify-aged2-2 | 925 | 0 | 144,579 (1.446) | fits |
| backlog-adp@verify-aged2-4 | 943 | 0 | 146,210 (1.462) | fits |
| backlog-adp@verify-aged2-6 | 959 | 0 | 145,143 (1.451) | fits |
| backlog-adp@verify-aged1-0 | 844 | 0 | 145,173 (1.452) | fits |
| backlog-adp@verify-aged1-2 | 858 | 0 | 145,132 (1.451) | fits |
| backlog-adp@verify-aged1-4 | 875 | 0 | 144,515 (1.445) | fits |
| backlog-adp@verify-aged1-6 | 892 | 0 | 145,375 (1.454) | fits |
| adp-advertise | 599 | 0 | 41,923 (0.419) | fits |
| save-starved | 27128 | 0 | 151,313 (1.513) | fits |
| save | 610 | 0 | 46,436 (0.464) | fits |
| backlog | 286 | 0 | 149,348 (1.493) | fits |
| backlog-adp-refill | 327 | 0 | 144,750 (1.448) | fits |
| acmp-disc | 938 | 0 | 41,923 (0.419) | fits |
| adp-link | 90 | 0 | 45,556 (0.456) | fits |
| adp-discover | 89 | 0 | 41,923 (0.419) | fits |
| aecp-fanout | 113 | 0 | 63,813 (0.638) | fits |
| aecp | 112 | 0 | 45,662 (0.457) | fits |
| datapath-events | 118 | 0 | 41,923 (0.419) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | +9.379 ms, 76,468 (0.765 ms), read-back | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 9.143 (20) | 10.857 |
| backlog-adp@blank-aged2-2 | 2 | +7.712 ms, 76,679 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.100 (20) | 9.900 |
| backlog-adp@blank-aged2-4 | 2 | +5.946 ms, 76,679 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 10.059 (20) | 9.941 |
| backlog-adp@blank-aged2-6 | 2 | none | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 9.931 (20) | 10.069 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.155 (20) | 10.845 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.102 (20) | 9.898 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.020 (20) | 9.980 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.101 (20) | 9.899 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.140 (20) | 10.860 |
| backlog-adp@program-aged2-2 | 2 | +8.563 ms, 80,379 (0.804 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 9.970 (20) | 10.030 |
| backlog-adp@program-aged2-4 | 2 | +6.018 ms, 80,379 (0.804 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.004 (20) | 9.996 |
| backlog-adp@program-aged2-6 | 2 | +4.419 ms, 79,667 (0.797 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 10.061 (20) | 9.939 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 9.099 (20) | 10.901 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.160 (20) | 10.840 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.274 (20) | 10.726 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 9.177 (20) | 10.823 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.142 (20) | 10.858 |
| backlog-adp@verify-aged2-2 | 2 | +7.788 ms, 77,453 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.035 (20) | 9.965 |
| backlog-adp@verify-aged2-4 | 2 | +5.968 ms, 77,453 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.930 (20) | 10.070 |
| backlog-adp@verify-aged2-6 | 2 | +4.332 ms, 76,882 (0.769 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 10.098 (20) | 9.902 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.118 (20) | 10.882 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.151 (20) | 10.849 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.187 (20) | 10.813 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 9.250 (20) | 10.750 |

Least margin over the aged windows: 9.898 ms, `backlog-adp@blank-aged1-2.service.srp.last.if0` at 10.102 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 4048.286 | 4,070 | 102 | - | 31.031 | yes | within |
| save | 2018.642 | 4,070 | 102 | - | 10.852 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 96,803 (0.968) | 77,672 (0.777) |
| backlog-adp@blank-0 | 299 | 90,251 (0.903) | 75,942 (0.759) |
| backlog-adp@blank-2 | 299 | 91,243 (0.912) | 76,037 (0.760) |
| backlog-adp@blank-4 | 299 | 91,467 (0.915) | 76,037 (0.760) |
| backlog-adp@blank-6 | 299 | 91,517 (0.915) | 75,967 (0.760) |
| backlog-adp@program-0 | 328 | 95,908 (0.959) | 78,496 (0.785) |
| backlog-adp@program-2 | 328 | 95,908 (0.959) | 78,635 (0.786) |
| backlog-adp@program-4 | 329 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@program-6 | 329 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-0 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-2 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-4 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-6 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@blank-aged2-0 | 297 | 76,468 (0.765) | 75,486 (0.755) |
| backlog-adp@blank-aged2-2 | 297 | 76,679 (0.767) | 75,581 (0.756) |
| backlog-adp@blank-aged2-4 | 297 | 76,679 (0.767) | 75,581 (0.756) |
| backlog-adp@blank-aged2-6 | 297 | 84,918 (0.849) | 75,390 (0.754) |
| backlog-adp@blank-aged1-0 | 298 | 96,456 (0.965) | 75,968 (0.760) |
| backlog-adp@blank-aged1-2 | 297 | 91,658 (0.917) | 75,924 (0.759) |
| backlog-adp@blank-aged1-4 | 297 | 93,520 (0.935) | 75,870 (0.759) |
| backlog-adp@blank-aged1-6 | 297 | 91,210 (0.912) | 75,968 (0.760) |
| backlog-adp@program-aged2-0 | 327 | 95,908 (0.959) | 78,592 (0.786) |
| backlog-adp@program-aged2-2 | 326 | 95,908 (0.959) | 78,310 (0.783) |
| backlog-adp@program-aged2-4 | 326 | 95,908 (0.959) | 78,310 (0.783) |
| backlog-adp@program-aged2-6 | 326 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@program-aged1-0 | 327 | 95,908 (0.959) | 78,592 (0.786) |
| backlog-adp@program-aged1-2 | 326 | 95,908 (0.959) | 78,451 (0.785) |
| backlog-adp@program-aged1-4 | 326 | 95,908 (0.959) | 78,635 (0.786) |
| backlog-adp@program-aged1-6 | 326 | 95,908 (0.959) | 78,592 (0.786) |
| backlog-adp@verify-aged2-0 | 356 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged2-2 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged2-4 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged2-6 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged1-0 | 356 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged1-2 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged1-4 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged1-6 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| adp-advertise | 578 | 21,733 (0.217) | 1,982 (0.020) |
| save-starved | 418 | 80,298 (0.803) | 77,923 (0.779) |
| save | 585 | 95,155 (0.952) | 77,701 (0.777) |
| backlog | 265 | 21,733 (0.217) | 1,982 (0.020) |
| backlog-adp-refill | 274 | 21,733 (0.217) | 2,196 (0.022) |
| acmp-disc | 305 | 95,877 (0.959) | 77,672 (0.777) |
| adp-link | 80 | 21,733 (0.217) | 1,982 (0.020) |
| adp-discover | 80 | 21,733 (0.217) | 1,982 (0.020) |
| aecp-fanout | 80 | 21,733 (0.217) | 1,982 (0.020) |
| aecp | 79 | 21,733 (0.217) | 1,982 (0.020) |
| datapath-events | 70 | 21,733 (0.217) | 1,982 (0.020) |

Longest pass that carries a step: 96,803 CPU cycles (0.968 ms), acmp-notk; longest step: 78,635 (0.786 ms), backlog-adp@program-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 14,322 | 0.143 | 20 | 20 | fits | 33,001 | 19 (14) | 0.880 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 435,632 | 4.356 | 20 | 20 | fits | 123,745 | 196 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 370,685 | 3.707 | 20 | 200 | fits | 144,611 | 203 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 493,814 | 4.938 | 20 | 200 | fits | 123,745 | 196 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 371,609 | 3.716 | 20 | 20 | fits | 144,611 | 203 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 494,518 | 4.945 | 20 | 20 | fits | 123,745 | 196 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 230,638 | 2.306 | 20 | 24 | fits | 144,219 | 145 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 374,259 | 3.743 | 20 | 24 | fits | 144,611 | 203 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 374,193 | 3.742 | 20 | 50 | fits | 144,611 | 203 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 497,542 | 4.975 | 20 | 50 | fits | 123,745 | 196 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 588,651 | 5.887 | 20 | 20 | fits | 91,175 | 28 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,000,521 | 10.005 | 20 | 20 | fits | 64,124 | 24 | 0.618 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 350,240 | 3.502 | 20 | 20 | fits | 123,877 | 196 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 285,458 | 2.855 | 20 | 200 | fits | 144,592 | 203 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 408,719 | 4.087 | 20 | 200 | fits | 123,877 | 196 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 286,382 | 2.864 | 20 | 20 | fits | 144,592 | 203 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 409,423 | 4.094 | 20 | 20 | fits | 123,877 | 196 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 145,430 | 1.454 | 20 | 24 | fits | 143,900 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 289,032 | 2.890 | 20 | 24 | fits | 144,592 | 203 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 288,966 | 2.890 | 20 | 50 | fits | 144,592 | 203 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 412,447 | 4.124 | 20 | 50 | fits | 123,877 | 196 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 503,441 | 5.034 | 20 | 20 | fits | 91,060 | 28 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 921,243 | 9.212 | 20 | 20 | fits | 64,285 | 24 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 376,018 | 3.760 | 20 | 20 | fits | 127,810 | 203 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 290,908 | 2.909 | 20 | 200 | fits | 145,488 | 204 | 0.461 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 427,469 | 4.275 | 20 | 200 | fits | 127,810 | 203 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 291,832 | 2.918 | 20 | 20 | fits | 145,488 | 204 | 0.461 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 428,173 | 4.282 | 20 | 20 | fits | 127,810 | 203 | 0.469 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 149,984 | 1.500 | 20 | 24 | fits | 143,896 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 294,482 | 2.945 | 20 | 24 | fits | 145,488 | 204 | 0.461 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 294,416 | 2.944 | 20 | 50 | fits | 145,488 | 204 | 0.461 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 431,197 | 4.312 | 20 | 50 | fits | 127,810 | 203 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 522,980 | 5.230 | 20 | 20 | fits | 91,849 | 28 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 924,986 | 9.250 | 20 | 20 | fits | 64,131 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 374,097 | 3.741 | 20 | 20 | fits | 132,026 | 202 | 0.473 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 300,853 | 3.009 | 20 | 200 | fits | 146,069 | 208 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 432,263 | 4.323 | 20 | 200 | fits | 132,026 | 202 | 0.473 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 301,777 | 3.018 | 20 | 20 | fits | 146,069 | 208 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 432,967 | 4.330 | 20 | 20 | fits | 132,026 | 202 | 0.473 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 159,348 | 1.593 | 20 | 24 | fits | 144,199 | 145 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 304,427 | 3.044 | 20 | 24 | fits | 146,069 | 208 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 304,361 | 3.044 | 20 | 50 | fits | 146,069 | 208 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 435,991 | 4.360 | 20 | 50 | fits | 132,026 | 202 | 0.473 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 527,297 | 5.273 | 20 | 20 | fits | 91,372 | 28 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 937,995 | 9.380 | 20 | 20 | fits | 58,180 | 27 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 364,010 | 3.640 | 20 | 20 | fits | 123,599 | 196 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 291,871 | 2.919 | 20 | 200 | fits | 145,218 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 414,854 | 4.149 | 20 | 200 | fits | 123,599 | 196 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 292,795 | 2.928 | 20 | 20 | fits | 145,218 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 415,558 | 4.156 | 20 | 20 | fits | 123,599 | 196 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 151,217 | 1.512 | 20 | 24 | fits | 144,246 | 145 | 0.434 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 295,445 | 2.954 | 20 | 24 | fits | 145,218 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 295,379 | 2.954 | 20 | 50 | fits | 145,218 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 418,582 | 4.186 | 20 | 50 | fits | 123,599 | 196 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 509,508 | 5.095 | 20 | 20 | fits | 90,992 | 29 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 920,029 | 9.200 | 20 | 20 | fits | 53,031 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 348,536 | 3.485 | 20 | 20 | fits | 123,855 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 283,659 | 2.837 | 20 | 200 | fits | 145,794 | 208 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 406,898 | 4.069 | 20 | 200 | fits | 123,855 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 284,583 | 2.846 | 20 | 20 | fits | 145,794 | 208 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 407,602 | 4.076 | 20 | 20 | fits | 123,855 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 142,429 | 1.424 | 20 | 24 | fits | 144,385 | 145 | 0.438 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 287,233 | 2.872 | 20 | 24 | fits | 145,794 | 208 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 287,167 | 2.872 | 20 | 50 | fits | 145,794 | 208 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 410,626 | 4.106 | 20 | 50 | fits | 123,855 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 496,625 | 4.966 | 20 | 20 | fits | 86,065 | 30 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 918,963 | 9.190 | 20 | 20 | fits | 69,170 | 31 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 363,978 | 3.640 | 20 | 20 | fits | 128,675 | 206 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 285,823 | 2.858 | 20 | 200 | fits | 143,709 | 199 | 0.463 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 413,882 | 4.139 | 20 | 200 | fits | 128,675 | 206 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 286,747 | 2.867 | 20 | 20 | fits | 143,709 | 199 | 0.463 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 414,586 | 4.146 | 20 | 20 | fits | 128,675 | 206 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 146,678 | 1.467 | 20 | 24 | fits | 144,538 | 145 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 289,397 | 2.894 | 20 | 24 | fits | 143,709 | 199 | 0.463 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 289,331 | 2.893 | 20 | 50 | fits | 143,709 | 199 | 0.463 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 417,610 | 4.176 | 20 | 50 | fits | 128,675 | 206 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 518,684 | 5.187 | 20 | 20 | fits | 91,585 | 29 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 913,546 | 9.135 | 20 | 20 | fits | 53,001 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 350,647 | 3.506 | 20 | 20 | fits | 123,880 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 285,936 | 2.859 | 20 | 200 | fits | 145,140 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 409,200 | 4.092 | 20 | 200 | fits | 123,880 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 286,860 | 2.869 | 20 | 20 | fits | 145,140 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 409,904 | 4.099 | 20 | 20 | fits | 123,880 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 145,360 | 1.454 | 20 | 24 | fits | 144,169 | 145 | 0.434 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 289,510 | 2.895 | 20 | 24 | fits | 145,140 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 289,444 | 2.894 | 20 | 50 | fits | 145,140 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 412,928 | 4.129 | 20 | 50 | fits | 123,880 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 498,627 | 4.986 | 20 | 20 | fits | 85,765 | 30 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 920,881 | 9.209 | 20 | 20 | fits | 64,161 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 392,214 | 3.922 | 20 | 20 | fits | 123,569 | 196 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 320,120 | 3.201 | 20 | 200 | fits | 145,159 | 203 | 0.459 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 443,073 | 4.431 | 20 | 200 | fits | 123,569 | 196 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 321,044 | 3.210 | 20 | 20 | fits | 145,159 | 203 | 0.459 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 443,777 | 4.438 | 20 | 20 | fits | 123,569 | 196 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 179,525 | 1.795 | 20 | 24 | fits | 144,418 | 145 | 0.434 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 323,694 | 3.237 | 20 | 24 | fits | 145,159 | 203 | 0.459 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 323,628 | 3.236 | 20 | 50 | fits | 145,159 | 203 | 0.459 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 446,801 | 4.468 | 20 | 50 | fits | 123,569 | 196 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 537,692 | 5.377 | 20 | 20 | fits | 90,957 | 28 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 948,449 | 9.484 | 20 | 20 | fits | 53,136 | 20 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 366,902 | 3.669 | 20 | 20 | fits | 123,514 | 196 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 294,863 | 2.949 | 20 | 200 | fits | 145,297 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 417,761 | 4.178 | 20 | 200 | fits | 123,514 | 196 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 295,787 | 2.958 | 20 | 20 | fits | 145,297 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 418,465 | 4.185 | 20 | 20 | fits | 123,514 | 196 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 154,130 | 1.541 | 20 | 24 | fits | 144,133 | 145 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 298,437 | 2.984 | 20 | 24 | fits | 145,297 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 298,371 | 2.984 | 20 | 50 | fits | 145,297 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 421,489 | 4.215 | 20 | 50 | fits | 123,514 | 196 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 512,527 | 5.125 | 20 | 20 | fits | 91,104 | 29 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 929,703 | 9.297 | 20 | 20 | fits | 64,161 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 370,218 | 3.702 | 20 | 20 | fits | 128,631 | 206 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 283,303 | 2.833 | 20 | 200 | fits | 144,153 | 200 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 420,665 | 4.207 | 20 | 200 | fits | 128,631 | 206 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 284,227 | 2.842 | 20 | 20 | fits | 144,153 | 200 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 421,369 | 4.214 | 20 | 20 | fits | 128,631 | 206 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 143,714 | 1.437 | 20 | 24 | fits | 144,133 | 145 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 286,877 | 2.869 | 20 | 24 | fits | 144,153 | 200 | 0.467 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 286,811 | 2.868 | 20 | 50 | fits | 144,153 | 200 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 424,393 | 4.244 | 20 | 50 | fits | 128,631 | 206 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 510,680 | 5.107 | 20 | 20 | fits | 86,353 | 30 | 0.774 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 916,945 | 9.169 | 20 | 20 | fits | 64,131 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 368,612 | 3.686 | 20 | 20 | fits | 133,200 | 208 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 294,418 | 2.944 | 20 | 200 | fits | 143,934 | 197 | 0.470 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 427,002 | 4.270 | 20 | 200 | fits | 133,200 | 208 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 295,342 | 2.953 | 20 | 20 | fits | 143,934 | 197 | 0.470 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 427,706 | 4.277 | 20 | 20 | fits | 133,200 | 208 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 155,048 | 1.550 | 20 | 24 | fits | 144,084 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 297,992 | 2.980 | 20 | 24 | fits | 143,934 | 197 | 0.470 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 297,926 | 2.979 | 20 | 50 | fits | 143,934 | 197 | 0.470 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 430,730 | 4.307 | 20 | 50 | fits | 133,200 | 208 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 521,668 | 5.217 | 20 | 20 | fits | 91,004 | 28 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 932,763 | 9.328 | 20 | 20 | fits | 53,136 | 20 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 356,501 | 3.565 | 20 | 20 | fits | 128,153 | 203 | 0.464 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 287,218 | 2.872 | 20 | 200 | fits | 146,152 | 208 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 414,755 | 4.148 | 20 | 200 | fits | 128,153 | 203 | 0.464 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 288,142 | 2.881 | 20 | 20 | fits | 146,152 | 208 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 415,459 | 4.155 | 20 | 20 | fits | 128,153 | 203 | 0.464 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 145,630 | 1.456 | 20 | 24 | fits | 148,930 | 147 | 0.457 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 290,792 | 2.908 | 20 | 24 | fits | 146,152 | 208 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 290,726 | 2.907 | 20 | 50 | fits | 146,152 | 208 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 418,483 | 4.185 | 20 | 50 | fits | 128,153 | 203 | 0.464 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 519,780 | 5.198 | 20 | 20 | fits | 91,426 | 29 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 914,346 | 9.143 | 20 | 20 | fits | 52,961 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 371,631 | 3.716 | 20 | 20 | fits | 124,143 | 199 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 297,880 | 2.979 | 20 | 200 | fits | 145,159 | 204 | 0.467 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 421,407 | 4.214 | 20 | 200 | fits | 124,143 | 199 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 298,804 | 2.988 | 20 | 20 | fits | 145,159 | 204 | 0.467 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 422,111 | 4.221 | 20 | 20 | fits | 124,143 | 199 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 148,373 | 1.484 | 20 | 24 | fits | 143,943 | 143 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 301,454 | 3.015 | 20 | 24 | fits | 145,159 | 204 | 0.467 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 301,388 | 3.014 | 20 | 50 | fits | 145,159 | 204 | 0.467 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 425,135 | 4.251 | 20 | 50 | fits | 124,143 | 199 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 515,807 | 5.158 | 20 | 20 | fits | 90,738 | 28 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,010,028 | 10.100 | 20 | 20 | fits | 68,915 | 31 | 0.683 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 358,633 | 3.586 | 20 | 20 | fits | 123,518 | 196 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 293,777 | 2.938 | 20 | 200 | fits | 144,278 | 203 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 416,679 | 4.167 | 20 | 200 | fits | 123,518 | 196 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 294,701 | 2.947 | 20 | 20 | fits | 144,278 | 203 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 417,383 | 4.174 | 20 | 20 | fits | 123,518 | 196 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 154,063 | 1.541 | 20 | 24 | fits | 143,313 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 297,351 | 2.974 | 20 | 24 | fits | 144,278 | 203 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 297,285 | 2.973 | 20 | 50 | fits | 144,278 | 203 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 420,407 | 4.204 | 20 | 50 | fits | 123,518 | 196 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 510,884 | 5.109 | 20 | 20 | fits | 90,543 | 28 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,005,855 | 10.059 | 20 | 20 | fits | 64,033 | 24 | 0.618 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 356,554 | 3.566 | 20 | 20 | fits | 132,304 | 203 | 0.475 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 283,665 | 2.837 | 20 | 200 | fits | 144,278 | 203 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 415,353 | 4.154 | 20 | 200 | fits | 132,304 | 203 | 0.475 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 284,589 | 2.846 | 20 | 20 | fits | 144,278 | 203 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 416,057 | 4.161 | 20 | 20 | fits | 132,304 | 203 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 143,951 | 1.440 | 20 | 24 | fits | 143,313 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 287,239 | 2.872 | 20 | 24 | fits | 144,278 | 203 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 287,173 | 2.872 | 20 | 50 | fits | 144,278 | 203 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 419,081 | 4.191 | 20 | 50 | fits | 132,304 | 203 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 587,331 | 5.873 | 20 | 20 | fits | 83,398 | 31 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 993,140 | 9.931 | 20 | 20 | fits | 64,083 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 358,890 | 3.589 | 20 | 20 | fits | 123,441 | 196 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 286,924 | 2.869 | 20 | 200 | fits | 145,256 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 409,749 | 4.097 | 20 | 200 | fits | 123,441 | 196 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 287,848 | 2.878 | 20 | 20 | fits | 145,256 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 410,453 | 4.105 | 20 | 20 | fits | 123,441 | 196 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 146,232 | 1.462 | 20 | 24 | fits | 143,253 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 290,498 | 2.905 | 20 | 24 | fits | 145,256 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 290,432 | 2.904 | 20 | 50 | fits | 145,256 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 413,477 | 4.135 | 20 | 50 | fits | 123,441 | 196 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 504,682 | 5.047 | 20 | 20 | fits | 91,271 | 28 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 915,477 | 9.155 | 20 | 20 | fits | 52,991 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 360,687 | 3.607 | 20 | 20 | fits | 127,969 | 203 | 0.465 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 291,318 | 2.913 | 20 | 200 | fits | 144,497 | 203 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 418,671 | 4.187 | 20 | 200 | fits | 127,969 | 203 | 0.465 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 292,242 | 2.922 | 20 | 20 | fits | 144,497 | 203 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 419,375 | 4.194 | 20 | 20 | fits | 127,969 | 203 | 0.465 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 151,385 | 1.514 | 20 | 24 | fits | 143,253 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 294,892 | 2.949 | 20 | 24 | fits | 144,497 | 203 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 294,826 | 2.948 | 20 | 50 | fits | 144,497 | 203 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 422,399 | 4.224 | 20 | 50 | fits | 127,969 | 203 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 523,853 | 5.239 | 20 | 20 | fits | 92,068 | 29 | 0.743 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,010,173 | 10.102 | 20 | 20 | fits | 65,660 | 25 | 0.669 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 358,140 | 3.581 | 20 | 20 | fits | 126,593 | 202 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 290,577 | 2.906 | 20 | 200 | fits | 145,683 | 208 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 416,554 | 4.166 | 20 | 200 | fits | 126,593 | 202 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 291,501 | 2.915 | 20 | 20 | fits | 145,683 | 208 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 417,258 | 4.173 | 20 | 20 | fits | 126,593 | 202 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 141,448 | 1.414 | 20 | 24 | fits | 143,363 | 143 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 294,151 | 2.942 | 20 | 24 | fits | 145,683 | 208 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 294,085 | 2.941 | 20 | 50 | fits | 145,683 | 208 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 420,282 | 4.203 | 20 | 50 | fits | 126,593 | 202 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 511,385 | 5.114 | 20 | 20 | fits | 91,169 | 28 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,002,000 | 10.020 | 20 | 20 | fits | 68,709 | 31 | 0.652 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 370,947 | 3.709 | 20 | 20 | fits | 145,155 | 202 | 0.501 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 287,054 | 2.871 | 20 | 200 | fits | 145,018 | 203 | 0.459 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 431,593 | 4.316 | 20 | 200 | fits | 145,155 | 202 | 0.501 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 287,978 | 2.880 | 20 | 20 | fits | 145,018 | 203 | 0.459 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 432,297 | 4.323 | 20 | 20 | fits | 145,155 | 202 | 0.501 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 146,600 | 1.466 | 20 | 24 | fits | 143,099 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 290,628 | 2.906 | 20 | 24 | fits | 145,018 | 203 | 0.459 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 290,562 | 2.906 | 20 | 50 | fits | 145,018 | 203 | 0.459 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 435,321 | 4.353 | 20 | 50 | fits | 145,155 | 202 | 0.501 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 567,742 | 5.677 | 20 | 20 | fits | 91,345 | 29 | 0.737 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,010,071 | 10.101 | 20 | 20 | fits | 64,113 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 373,774 | 3.738 | 20 | 20 | fits | 123,844 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 301,489 | 3.015 | 20 | 200 | fits | 146,513 | 208 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 424,717 | 4.247 | 20 | 200 | fits | 123,844 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 302,413 | 3.024 | 20 | 20 | fits | 146,513 | 208 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 425,421 | 4.254 | 20 | 20 | fits | 123,844 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 151,514 | 1.515 | 20 | 24 | fits | 143,583 | 143 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 305,063 | 3.051 | 20 | 24 | fits | 146,513 | 208 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 304,997 | 3.050 | 20 | 50 | fits | 146,513 | 208 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 428,445 | 4.284 | 20 | 50 | fits | 123,844 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 519,122 | 5.191 | 20 | 20 | fits | 90,743 | 28 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 914,033 | 9.140 | 20 | 20 | fits | 53,031 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 355,501 | 3.555 | 20 | 20 | fits | 123,496 | 196 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 283,480 | 2.835 | 20 | 200 | fits | 146,539 | 208 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 406,360 | 4.064 | 20 | 200 | fits | 123,496 | 196 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 284,404 | 2.844 | 20 | 20 | fits | 146,539 | 208 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 407,064 | 4.071 | 20 | 20 | fits | 123,496 | 196 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 141,505 | 1.415 | 20 | 24 | fits | 143,420 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 287,054 | 2.871 | 20 | 24 | fits | 146,539 | 208 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 286,988 | 2.870 | 20 | 50 | fits | 146,539 | 208 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 410,088 | 4.101 | 20 | 50 | fits | 123,496 | 196 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 500,751 | 5.008 | 20 | 20 | fits | 90,729 | 28 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 997,016 | 9.970 | 20 | 20 | fits | 64,118 | 25 | 0.626 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 351,672 | 3.517 | 20 | 20 | fits | 123,794 | 196 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 286,676 | 2.867 | 20 | 200 | fits | 144,456 | 203 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 409,854 | 4.099 | 20 | 200 | fits | 123,794 | 196 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 287,600 | 2.876 | 20 | 20 | fits | 144,456 | 203 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 410,558 | 4.106 | 20 | 20 | fits | 123,794 | 196 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 146,784 | 1.468 | 20 | 24 | fits | 143,420 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 290,250 | 2.902 | 20 | 24 | fits | 144,456 | 203 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 290,184 | 2.902 | 20 | 50 | fits | 144,456 | 203 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 413,582 | 4.136 | 20 | 50 | fits | 123,794 | 196 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 504,356 | 5.044 | 20 | 20 | fits | 90,840 | 29 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,000,406 | 10.004 | 20 | 20 | fits | 64,156 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 377,574 | 3.776 | 20 | 20 | fits | 135,337 | 209 | 0.480 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 292,768 | 2.928 | 20 | 200 | fits | 145,395 | 204 | 0.461 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 436,574 | 4.366 | 20 | 200 | fits | 135,337 | 209 | 0.480 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 293,692 | 2.937 | 20 | 20 | fits | 145,395 | 204 | 0.461 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 437,278 | 4.373 | 20 | 20 | fits | 135,337 | 209 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 151,937 | 1.519 | 20 | 24 | fits | 143,420 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 296,342 | 2.963 | 20 | 24 | fits | 145,395 | 204 | 0.461 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 296,276 | 2.963 | 20 | 50 | fits | 145,395 | 204 | 0.461 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 440,302 | 4.403 | 20 | 50 | fits | 135,337 | 209 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 611,138 | 6.111 | 20 | 20 | fits | 91,235 | 29 | 0.734 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,006,084 | 10.061 | 20 | 20 | fits | 53,026 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 348,118 | 3.481 | 20 | 20 | fits | 124,074 | 197 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 283,525 | 2.835 | 20 | 200 | fits | 146,617 | 208 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 406,983 | 4.070 | 20 | 200 | fits | 124,074 | 197 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 284,449 | 2.844 | 20 | 20 | fits | 146,617 | 208 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 407,687 | 4.077 | 20 | 20 | fits | 124,074 | 197 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 141,472 | 1.415 | 20 | 24 | fits | 143,420 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 287,099 | 2.871 | 20 | 24 | fits | 146,617 | 208 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 287,033 | 2.870 | 20 | 50 | fits | 146,617 | 208 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 410,711 | 4.107 | 20 | 50 | fits | 124,074 | 197 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 503,640 | 5.036 | 20 | 20 | fits | 83,760 | 31 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 909,905 | 9.099 | 20 | 20 | fits | 64,131 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 369,342 | 3.693 | 20 | 20 | fits | 124,351 | 199 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 295,495 | 2.955 | 20 | 200 | fits | 145,297 | 204 | 0.466 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 419,230 | 4.192 | 20 | 200 | fits | 124,351 | 199 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 296,419 | 2.964 | 20 | 20 | fits | 145,297 | 204 | 0.466 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 419,934 | 4.199 | 20 | 20 | fits | 124,351 | 199 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 146,778 | 1.468 | 20 | 24 | fits | 143,573 | 143 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 299,069 | 2.991 | 20 | 24 | fits | 145,297 | 204 | 0.466 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 299,003 | 2.990 | 20 | 50 | fits | 145,297 | 204 | 0.466 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 422,958 | 4.230 | 20 | 50 | fits | 124,351 | 199 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 513,722 | 5.137 | 20 | 20 | fits | 90,830 | 28 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 916,046 | 9.160 | 20 | 20 | fits | 64,424 | 25 | 0.623 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 356,907 | 3.569 | 20 | 20 | fits | 123,855 | 196 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 291,850 | 2.918 | 20 | 200 | fits | 144,520 | 203 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 415,089 | 4.151 | 20 | 200 | fits | 123,855 | 196 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 292,774 | 2.928 | 20 | 20 | fits | 144,520 | 203 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 415,793 | 4.158 | 20 | 20 | fits | 123,855 | 196 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 151,894 | 1.519 | 20 | 24 | fits | 143,450 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 295,424 | 2.954 | 20 | 24 | fits | 144,520 | 203 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 295,358 | 2.954 | 20 | 50 | fits | 144,520 | 203 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 418,817 | 4.188 | 20 | 50 | fits | 123,855 | 196 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 509,525 | 5.095 | 20 | 20 | fits | 90,774 | 28 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 927,414 | 9.274 | 20 | 20 | fits | 64,161 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 355,786 | 3.558 | 20 | 20 | fits | 132,494 | 203 | 0.475 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 282,851 | 2.829 | 20 | 200 | fits | 145,880 | 208 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 414,729 | 4.147 | 20 | 200 | fits | 132,494 | 203 | 0.475 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 283,775 | 2.838 | 20 | 20 | fits | 145,880 | 208 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 415,433 | 4.154 | 20 | 20 | fits | 132,494 | 203 | 0.475 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 141,535 | 1.415 | 20 | 24 | fits | 143,450 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 286,425 | 2.864 | 20 | 24 | fits | 145,880 | 208 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 286,359 | 2.864 | 20 | 50 | fits | 145,880 | 208 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 418,457 | 4.185 | 20 | 50 | fits | 132,494 | 203 | 0.475 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 511,478 | 5.115 | 20 | 20 | fits | 83,571 | 31 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 917,682 | 9.177 | 20 | 20 | fits | 64,131 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 357,660 | 3.577 | 20 | 20 | fits | 123,557 | 196 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 285,578 | 2.856 | 20 | 200 | fits | 145,223 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 408,519 | 4.085 | 20 | 200 | fits | 123,557 | 196 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 286,502 | 2.865 | 20 | 20 | fits | 145,223 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 409,223 | 4.092 | 20 | 20 | fits | 123,557 | 196 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 144,919 | 1.449 | 20 | 24 | fits | 143,332 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 289,152 | 2.892 | 20 | 24 | fits | 145,223 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 289,086 | 2.891 | 20 | 50 | fits | 145,223 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 412,247 | 4.122 | 20 | 50 | fits | 123,557 | 196 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 503,219 | 5.032 | 20 | 20 | fits | 91,038 | 28 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 914,200 | 9.142 | 20 | 20 | fits | 53,136 | 20 | 0.670 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 355,144 | 3.551 | 20 | 20 | fits | 123,855 | 196 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 290,087 | 2.901 | 20 | 200 | fits | 144,579 | 203 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 413,326 | 4.133 | 20 | 200 | fits | 123,855 | 196 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 291,011 | 2.910 | 20 | 20 | fits | 144,579 | 203 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 414,030 | 4.140 | 20 | 20 | fits | 123,855 | 196 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 150,072 | 1.501 | 20 | 24 | fits | 143,378 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 293,661 | 2.937 | 20 | 24 | fits | 144,579 | 203 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 293,595 | 2.936 | 20 | 50 | fits | 144,579 | 203 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 417,054 | 4.171 | 20 | 50 | fits | 123,855 | 196 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 508,140 | 5.081 | 20 | 20 | fits | 91,152 | 29 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,003,454 | 10.035 | 20 | 20 | fits | 64,219 | 24 | 0.624 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 358,998 | 3.590 | 20 | 20 | fits | 127,557 | 202 | 0.469 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 281,862 | 2.819 | 20 | 200 | fits | 146,210 | 209 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 417,868 | 4.179 | 20 | 200 | fits | 127,557 | 202 | 0.469 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 282,786 | 2.828 | 20 | 20 | fits | 146,210 | 209 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 418,572 | 4.186 | 20 | 20 | fits | 127,557 | 202 | 0.469 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 140,216 | 1.402 | 20 | 24 | fits | 143,378 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 285,436 | 2.854 | 20 | 24 | fits | 146,210 | 209 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 285,370 | 2.854 | 20 | 50 | fits | 146,210 | 209 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 421,596 | 4.216 | 20 | 50 | fits | 127,557 | 202 | 0.469 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 512,939 | 5.129 | 20 | 20 | fits | 91,409 | 28 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 993,021 | 9.930 | 20 | 20 | fits | 64,085 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 376,804 | 3.768 | 20 | 20 | fits | 132,192 | 202 | 0.472 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 296,272 | 2.963 | 20 | 200 | fits | 145,143 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 427,848 | 4.278 | 20 | 200 | fits | 132,192 | 202 | 0.472 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 297,196 | 2.972 | 20 | 20 | fits | 145,143 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 428,552 | 4.286 | 20 | 20 | fits | 132,192 | 202 | 0.472 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 155,693 | 1.557 | 20 | 24 | fits | 143,281 | 143 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 299,846 | 2.998 | 20 | 24 | fits | 145,143 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 299,780 | 2.998 | 20 | 50 | fits | 145,143 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 431,576 | 4.316 | 20 | 50 | fits | 132,192 | 202 | 0.472 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 599,271 | 5.993 | 20 | 20 | fits | 90,879 | 29 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,009,822 | 10.098 | 20 | 20 | fits | 53,045 | 20 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 372,411 | 3.724 | 20 | 20 | fits | 124,351 | 199 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 298,564 | 2.986 | 20 | 200 | fits | 145,173 | 204 | 0.466 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 422,299 | 4.223 | 20 | 200 | fits | 124,351 | 199 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 299,488 | 2.995 | 20 | 20 | fits | 145,173 | 204 | 0.466 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 423,003 | 4.230 | 20 | 20 | fits | 124,351 | 199 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 149,929 | 1.499 | 20 | 24 | fits | 143,511 | 143 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 302,138 | 3.021 | 20 | 24 | fits | 145,173 | 204 | 0.466 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 302,072 | 3.021 | 20 | 50 | fits | 145,173 | 204 | 0.466 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 426,027 | 4.260 | 20 | 50 | fits | 124,351 | 199 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 516,961 | 5.170 | 20 | 20 | fits | 91,000 | 28 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 911,779 | 9.118 | 20 | 20 | fits | 53,031 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 354,444 | 3.544 | 20 | 20 | fits | 124,307 | 199 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 280,758 | 2.808 | 20 | 200 | fits | 145,132 | 204 | 0.463 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 404,449 | 4.044 | 20 | 200 | fits | 124,307 | 199 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 281,682 | 2.817 | 20 | 20 | fits | 145,132 | 204 | 0.463 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 405,153 | 4.052 | 20 | 20 | fits | 124,307 | 199 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 140,190 | 1.402 | 20 | 24 | fits | 143,492 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 284,332 | 2.843 | 20 | 24 | fits | 145,132 | 204 | 0.463 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 284,266 | 2.843 | 20 | 50 | fits | 145,132 | 204 | 0.463 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 408,177 | 4.082 | 20 | 50 | fits | 124,307 | 199 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 499,125 | 4.991 | 20 | 20 | fits | 91,014 | 28 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 915,128 | 9.151 | 20 | 20 | fits | 64,142 | 24 | 0.618 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 349,924 | 3.499 | 20 | 20 | fits | 123,725 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 285,294 | 2.853 | 20 | 200 | fits | 144,515 | 203 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 408,403 | 4.084 | 20 | 200 | fits | 123,725 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 286,218 | 2.862 | 20 | 20 | fits | 144,515 | 203 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 409,107 | 4.091 | 20 | 20 | fits | 123,725 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 145,343 | 1.453 | 20 | 24 | fits | 143,492 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 288,868 | 2.889 | 20 | 24 | fits | 144,515 | 203 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 288,802 | 2.888 | 20 | 50 | fits | 144,515 | 203 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 412,131 | 4.121 | 20 | 50 | fits | 123,725 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 503,119 | 5.031 | 20 | 20 | fits | 91,054 | 29 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 918,723 | 9.187 | 20 | 20 | fits | 64,161 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 383,668 | 3.837 | 20 | 20 | fits | 135,379 | 209 | 0.480 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 291,307 | 2.913 | 20 | 200 | fits | 145,375 | 204 | 0.461 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 435,155 | 4.352 | 20 | 200 | fits | 135,379 | 209 | 0.480 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 292,231 | 2.922 | 20 | 20 | fits | 145,375 | 204 | 0.461 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 435,859 | 4.359 | 20 | 20 | fits | 135,379 | 209 | 0.480 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 150,496 | 1.505 | 20 | 24 | fits | 143,492 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 294,881 | 2.949 | 20 | 24 | fits | 145,375 | 204 | 0.461 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 294,815 | 2.948 | 20 | 50 | fits | 145,375 | 204 | 0.461 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 438,883 | 4.389 | 20 | 50 | fits | 135,379 | 209 | 0.480 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 530,181 | 5.302 | 20 | 20 | fits | 91,364 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 925,002 | 9.250 | 20 | 20 | fits | 53,001 | 20 | 0.667 |
| LINK_UP | `adp.link_up.if0` | 2,593 | 0.026 | 20 | 200 | fits | 26,340 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,368 | 0.174 | 20 | 200 | fits | 21,586 | 23 (39) | 0.724 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 10,380 | 0.104 | 20 | 200 | fits | 2,604 | 10 (11) | 0.500 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 150,373 | 1.504 | 20 | 200 | fits | 151,313 | 242 | 0.499 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 227,869 | 2.279 | 20 | 20 | fits | 97,633 | 97 | 0.663 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 294,436 | 2.944 | 20 | 24 | fits | 82,378 | 66 | 0.511 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 131,932 | 1.319 | 20 | 50 | fits | 39,099 | 52 | 0.606 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 877,712 | 8.777 | 20 | 20 | fits | 34,270 | 18 | 0.811 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 256,771 | 2.568 | 20 | 20 | fits | 0 | - | 0.000 |
| an event behind 15 others | `backlog.event.if0` | 162,831 | 1.628 | 20 | 200 | fits | 56,000 | 79 | 0.566 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 433,494 | 4.335 | 20 | 20 | fits | 49,455 | 72 | 0.326 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 422,900 | 4.229 | 20 | 200 | fits | 149,069 | 158 | 0.452 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 422,284 | 4.223 | 20 | 200 | fits | 149,069 | 158 | 0.452 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 418,578 | 4.186 | 20 | 20 | fits | 149,069 | 158 | 0.452 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 467,197 | 4.672 | 20 | 20 | fits | 49,455 | 72 | 0.326 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 148,457 | 1.485 | 20 | 24 | fits | 149,348 | 148 | 0.427 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 421,228 | 4.212 | 20 | 24 | fits | 149,069 | 158 | 0.452 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 421,162 | 4.212 | 20 | 50 | fits | 149,069 | 158 | 0.452 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 420,766 | 4.208 | 20 | 50 | fits | 149,069 | 158 | 0.452 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 470,155 | 4.702 | 20 | 20 | fits | 49,455 | 72 | 0.326 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 532,858 | 5.329 | 20 | 20 | fits | 25,835 | 41 | 0.182 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 20,821 | 0.208 | 20 | 20 | fits | 25,522 | 19 | 0.804 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 283,897 | 2.839 | 20 | 200 | fits | 144,750 | 203 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 37,599 | 0.376 | 20 | 200 | fits | 25,522 | 19 | 0.804 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 284,821 | 2.848 | 20 | 20 | fits | 144,750 | 203 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 401,785 | 4.018 | 20 | 20 | fits | 117,800 | 193 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 143,711 | 1.437 | 20 | 24 | fits | 143,897 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 287,471 | 2.875 | 20 | 24 | fits | 144,750 | 203 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 287,405 | 2.874 | 20 | 50 | fits | 144,750 | 203 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 404,809 | 4.048 | 20 | 50 | fits | 117,800 | 193 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 505,748 | 5.057 | 20 | 20 | fits | 91,569 | 29 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 907,758 | 9.078 | 20 | 20 | fits | 64,126 | 24 | 0.620 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,271 | 0.063 | 20 | 20 | fits | 22,469 | 13 (29) | 0.771 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,258 | 0.083 | 20 | 20 | fits | 24,821 | 19 (35) | 0.788 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 21,585 | 0.216 | 20 | 20 | fits | 27,555 | 21 (12) | 0.804 |
| LINK_UP | `adp.link_up.if0` | 2,593 | 0.026 | 20 | 200 | fits | 26,340 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,368 | 0.174 | 20 | 200 | fits | 21,586 | 23 (39) | 0.724 |
| LINK_DOWN | `adp.link_down.if0` | 2,334 | 0.023 | 20 | 200 | fits | 25,135 | 23 (9) | 0.779 |
| LINK_UP | `adp.link_up.if0` | 2,593 | 0.026 | 20 | 200 | fits | 26,340 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,368 | 0.174 | 20 | 200 | fits | 21,586 | 23 (39) | 0.724 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,641 | 0.046 | 20 | 200 | fits | 16,191 | 16 (31) | 0.667 |
| set_name | `aecp_fanout.set_name.if0` | 57,295 | 0.573 | 20 | 24 | fits | 63,813 | 89 | 0.580 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 42,602 | 0.426 | 20 | 24 | fits | 55,391 | 78 | 0.607 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 48,218 | 0.482 | 20 | 24 | fits | 53,898 | 79 | 0.583 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,059 | 0.401 | 20 | 24 | fits | 49,490 | 78 | 0.558 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 51,835 | 0.518 | 20 | 24 | fits | 60,575 | 66 | 0.652 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 246,666 | 2.467 | 20 | 24 | fits | 58,530 | 65 | 0.645 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 219,711 | 2.197 | 20 | 24 | fits | 54,293 | 67 | 0.623 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 40,312 | 0.403 | 20 | 24 | fits | 49,943 | 78 | 0.567 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 44,805 | 0.448 | 20 | 24 | fits | 49,601 | 79 | 0.559 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 20,920 | 0.209 | 20 | 24 | fits | 28,010 | 20 | 0.807 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 17,464 | 0.175 | 20 | 24 | fits | 31,946 | 20 | 0.737 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 17,123 | 0.171 | 20 | 24 | fits | 27,294 | 20 | 0.760 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 12,679 | 0.127 | 20 | 24 | fits | 26,977 | 20 | 0.755 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 21,620 | 0.216 | 20 | 24 | fits | 27,570 | 20 | 0.762 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 23,646 | 0.236 | 20 | 24 | fits | 27,245 | 20 | 0.754 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 12,634 | 0.126 | 20 | 24 | fits | 26,537 | 20 | 0.760 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 16,812 | 0.168 | 20 | 24 | fits | 26,746 | 20 | 0.772 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 12,143 | 0.121 | 20 | 24 | fits | 26,046 | 20 | 0.772 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 19,204 | 0.192 | 20 | 24 | fits | 28,985 | 21 | 0.678 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 11,802 | 0.118 | 20 | 24 | fits | 25,702 | 20 | 0.790 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 20,187 | 0.202 | 20 | 24 | fits | 26,060 | 20 | 0.792 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 22,860 | 0.229 | 20 | 24 | fits | 26,382 | 20 | 0.758 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 12,963 | 0.130 | 20 | 24 | fits | 27,332 | 20 | 0.763 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 16,612 | 0.166 | 20 | 24 | fits | 26,775 | 20 | 0.772 |
| get_configuration | `aecp.get_configuration.if0` | 10,584 | 0.106 | 20 | 24 | fits | 24,374 | 20 | 0.774 |
| entity_available | `aecp.entity_available.if0` | 14,826 | 0.148 | 20 | 24 | fits | 24,258 | 20 | 0.772 |
| get_name | `aecp.get_name.if0` | 23,867 | 0.239 | 20 | 24 | fits | 27,802 | 20 | 0.785 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 13,772 | 0.138 | 20 | 24 | fits | 28,096 | 27 | 0.752 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 18,564 | 0.186 | 20 | 24 | fits | 28,601 | 29 | 0.785 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 11,009 | 0.110 | 20 | 24 | fits | 24,859 | 20 | 0.787 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,576 | 0.146 | 20 | 24 | fits | 24,173 | 20 | 0.774 |
| set_name | `aecp.set_name.if0` | 28,319 | 0.283 | 20 | 24 | fits | 45,662 | 43 | 0.769 |
| lock_entity | `aecp.lock_entity.if0` | 25,244 | 0.252 | 20 | 24 | fits | 35,294 | 34 | 0.795 |
| unlock_entity | `aecp.unlock_entity.if0` | 21,684 | 0.217 | 20 | 24 | fits | 35,084 | 33 | 0.780 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

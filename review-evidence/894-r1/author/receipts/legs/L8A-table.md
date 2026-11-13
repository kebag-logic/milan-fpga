### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 82 paths and 6 of 131 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.246 (0.648) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.177 (0.564) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.253 (0.646) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 1 | `aecp.get_avb_info.if1` (aecp) | 0.207 (0.598) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.153 (0.542) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.266 (0.667) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.188 (0.581) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 1 | `aecp.get_counters.if1` (aecp) | 0.304 (0.711) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.266 (0.673) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.201 (0.609) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.298 (0.656) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.420 (0.777) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.242 (0.644) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.246 (0.558) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.312 (0.722) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.322 (0.732) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.260 (0.666) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.291 (0.702) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.243 (0.580) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.173 (0.587) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.309 (0.720) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.167 (0.564) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.261 (0.668) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.178 (0.593) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.199 (0.597) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.246 (0.584) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.181 (0.595) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.270 (0.682) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.266 (0.677) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.179 (0.577) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.261 (0.668) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.158 (0.557) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.171 (0.574) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.480 (0.872) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.378 (0.752) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.154 (0.544) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 1 | `aecp.unknown_command.if1` (aecp) | 0.274 (0.679) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.399 (0.747) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.331 (0.681) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.648 (1.045) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.643 (1.039) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.669 (1.085) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.676 (1.084) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.726 (1.117) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 0.728 (1.120) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.836 (1.269) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.703 (1.105) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.659 (1.060) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.482 (0.624) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.482 (0.625) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.148 (7.898) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.072 (6.541) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.197 (0.750) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.876 (2.363) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.014 (64.390) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.585 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 5.031 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.802 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 3.065 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 3.993 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 11.342 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 4.273 | fits | 0 srp | 6 | 0 |
| an MRPDU its join timer owes, the longest | 1 | `save-starved.mrpdu.periodic.if1` (save-starved) | 5.572 | fits | 0 srp | 6 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.923 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.871 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.965 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.488 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.610 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.754 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 61.997 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.948 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.595 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 7.900 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 12.335 | fits | 31 srp | 4 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.901 (2.091) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.633 (1.797) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.574 (0.575) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.531 (0.532) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.262 (0.263) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.265 (0.266) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.501 (1.569) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.444 (1.503) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 11.089 | 9 | 176,292 (1.763) | yes | - |
| backlog-adp | 0 | 13.038 | 11 | 173,437 (1.734) | yes | - |
| backlog-adp-refill | 0 | 41.170 | 23 | 173,437 (1.734) | yes | - |
| backlog-owed | 0 | 360.636 | 52 | 171,288 (1.713) | yes | - |

Composed maximum over the 4 backlog windows: 176,292 CPU cycles (1.763 ms), backlog.
Over the windows that released their whole load only: 176,292 (1.763 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 111356 | 0 | 105,578 (1.056) | fits |
| save-held | 3172 | 0 | 169,034 (1.690) | fits |
| save-starved | 50850 | 0 | 170,946 (1.709) | fits |
| srp | 316 | 0 | 157,971 (1.580) | fits |
| backlog | 300 | 0 | 176,292 (1.763) | fits |
| backlog-adp | 327 | 0 | 173,437 (1.734) | fits |
| backlog-adp-refill | 339 | 0 | 173,437 (1.734) | fits |
| backlog-owed | 351 | 0 | 171,288 (1.713) | fits |
| aecp-fanout | 151 | 0 | 94,706 (0.947) | fits |
| aecp | 140 | 0 | 94,706 (0.947) | fits |
| datapath-events | 161 | 0 | 94,706 (0.947) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22110.206 | 22,150 | 370 | 2 | 32.803 | yes | within |
| save-held | 4697.688 | 12,110 | 370 | - | 17.983 | no | within |
| save-starved | 12088.059 | 12,110 | 370 | - | 35.228 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1056 | 81,420 (0.814) | 78,851 (0.789) |
| save-held | 1526 | 110,124 (1.101) | 79,562 (0.796) |
| save-starved | 686 | 81,583 (0.816) | 78,896 (0.789) |
| srp | 278 | 34,245 (0.342) | 3,919 (0.039) |
| backlog | 266 | 32,591 (0.326) | 3,758 (0.038) |
| backlog-adp | 271 | 32,591 (0.326) | 3,604 (0.036) |
| backlog-adp-refill | 274 | 32,591 (0.326) | 3,604 (0.036) |
| backlog-owed | 306 | 39,868 (0.399) | 3,676 (0.037) |
| aecp-fanout | 93 | 32,437 (0.324) | 3,601 (0.036) |
| aecp | 88 | 32,437 (0.324) | 3,601 (0.036) |
| datapath-events | 74 | 32,437 (0.324) | 3,601 (0.036) |

Longest pass that carries a step: 110,124 CPU cycles (1.101 ms), save-held; longest step: 79,562 (0.796 ms), save-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 472,311 | 4.723 | 20 | 200 | fits | 152,222 | 73 | 0.473 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 503,070 | 5.031 | 20 | 20 | fits | 124,994 | 42 | 0.586 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 288,612 | 2.886 | 20 | 24 | fits | 74,301 | 56 | 0.526 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 391,773 | 3.918 | 20 | 50 | fits | 126,986 | 65 | 0.472 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 1,108,865 | 11.089 | 20 | 20 | fits | 80,024 | 29 | 0.536 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 182,471 | 1.825 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if1` | 264,144 | 2.641 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 318,761 | 3.188 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if1` | 527,617 | 5.276 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 423,973 | 4.240 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if1` | 556,198 | 5.562 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 480,223 | 4.802 | 20 | 200 | fits | 156,200 | 79 | 0.509 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 460,086 | 4.601 | 20 | 20 | fits | 156,200 | 79 | 0.509 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 306,479 | 3.065 | 20 | 24 | fits | 75,406 | 62 | 0.514 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 399,310 | 3.993 | 20 | 50 | fits | 130,754 | 71 | 0.518 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,134,163 | 11.342 | 20 | 20 | fits | 94,143 | 39 | 0.552 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 185,946 | 1.859 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if1` | 267,763 | 2.678 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 316,171 | 3.162 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if1` | 379,419 | 3.794 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 427,298 | 4.273 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if1` | 557,169 | 5.572 | 20 | 20 | fits | 0 | - | 0.000 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 150,098 | 1.501 | 20 | 20 | fits | 26,779 | 8 | 0.776 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 144,401 | 1.444 | 20 | 20 | fits | 26,011 | 8 | 0.750 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 57,436 | 0.574 | 20 | 20 | fits | 57,501 | 13 | 0.880 |
| malformed MRPDU discard | `srp.malformed.if0` | 26,241 | 0.262 | 20 | 20 | fits | 26,306 | 13 | 0.692 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 190,092 | 1.901 | 220 | 220 | fits | 157,971 | 7 | 0.780 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 53,117 | 0.531 | 20 | 20 | fits | 53,182 | 13 | 0.879 |
| malformed MRPDU discard | `srp.malformed.if1` | 26,520 | 0.265 | 20 | 20 | fits | 26,585 | 13 | 0.689 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 163,349 | 1.633 | 220 | 220 | fits | 131,683 | 6 | 0.774 |
| an event behind 15 others | `backlog.event.if0` | 187,618 | 1.876 | 20 | 200 | fits | 60,008 | 81 | 0.581 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 714,834 | 7.148 | 20 | 20 | fits | 127,992 | 42 | 0.664 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 496,519 | 4.965 | 20 | 200 | fits | 159,089 | 102 | 0.492 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 660,990 | 6.610 | 20 | 200 | fits | 165,080 | 90 | 0.411 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 492,260 | 4.923 | 20 | 20 | fits | 159,089 | 102 | 0.492 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 784,507 | 7.845 | 20 | 20 | fits | 127,992 | 42 | 0.664 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 175,410 | 1.754 | 20 | 24 | fits | 176,292 | 183 | 0.384 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 335,781 | 3.358 | 20 | 24 | fits | 101,338 | 29 | 0.700 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 494,805 | 4.948 | 20 | 50 | fits | 159,089 | 102 | 0.492 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 659,495 | 6.595 | 20 | 50 | fits | 165,080 | 90 | 0.411 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 787,422 | 7.874 | 20 | 20 | fits | 127,992 | 42 | 0.664 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,039,625 | 10.396 | 20 | 20 | fits | 57,836 | 33 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 507,194 | 5.072 | 20 | 20 | fits | 152,283 | 75 | 0.523 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 313,097 | 3.131 | 20 | 200 | fits | 162,207 | 178 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 648,794 | 6.488 | 20 | 200 | fits | 152,283 | 75 | 0.523 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 314,009 | 3.140 | 20 | 20 | fits | 162,207 | 178 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 787,051 | 7.871 | 20 | 20 | fits | 137,561 | 34 | 0.738 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 155,387 | 1.554 | 20 | 24 | fits | 155,572 | 180 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 316,619 | 3.166 | 20 | 24 | fits | 162,207 | 178 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 316,554 | 3.166 | 20 | 50 | fits | 162,207 | 178 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 652,470 | 6.525 | 20 | 50 | fits | 152,283 | 75 | 0.523 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 789,966 | 7.900 | 20 | 20 | fits | 137,561 | 34 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,233,509 | 12.335 | 20 | 20 | fits | 66,182 | 27 | 0.732 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 19,722 | 0.197 | 20 | 20 | fits | 45,433 | 20 | 0.795 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 313,097 | 3.131 | 20 | 200 | fits | 162,207 | 178 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 54,080 | 0.541 | 20 | 200 | fits | 45,433 | 20 | 0.795 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 314,009 | 3.140 | 20 | 20 | fits | 162,207 | 178 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 778,409 | 7.784 | 20 | 20 | fits | 123,646 | 28 | 0.765 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 155,387 | 1.554 | 20 | 24 | fits | 155,572 | 180 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 316,619 | 3.166 | 20 | 24 | fits | 162,207 | 178 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 316,554 | 3.166 | 20 | 50 | fits | 162,207 | 178 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 657,743 | 6.577 | 20 | 50 | fits | 157,556 | 75 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 781,324 | 7.813 | 20 | 20 | fits | 123,646 | 28 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,215,255 | 12.153 | 20 | 20 | fits | 56,296 | 23 | 0.777 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,401,410 | 64.014 | 20 | 20 | MISS ceiling | 37,621 | 13 | 0.633 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,058,496 | 360.585 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,058,421 | 360.584 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,058,346 | 360.583 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,058,271 | 360.583 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 169,262 | 1.693 | 20 | 200 | fits | 170,087 | 179 | 0.474 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 496,344 | 4.963 | 20 | 200 | fits | 156,403 | 90 | 0.411 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 165,003 | 1.650 | 20 | 20 | fits | 170,087 | 179 | 0.474 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 491,869 | 4.919 | 20 | 20 | fits | 156,403 | 90 | 0.411 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 168,588 | 1.686 | 20 | 24 | fits | 170,087 | 179 | 0.474 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,199,741 | 61.997 | 20 | 24 | MISS ceiling | 144,163 | 114 | 0.392 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 167,548 | 1.675 | 20 | 50 | fits | 170,087 | 179 | 0.474 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 494,849 | 4.948 | 20 | 50 | fits | 156,403 | 90 | 0.411 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 614,494 | 6.145 | 20 | 20 | fits | 119,710 | 30 | 0.732 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 980,345 | 9.803 | 20 | 20 | fits | 122,043 | 46 | 0.468 |
| set_name | `aecp_fanout.set_name.if0` | 83,557 | 0.836 | 20 | 24 | fits | 77,912 | 159 | 0.430 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 66,904 | 0.669 | 20 | 24 | fits | 66,298 | 139 | 0.426 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 65,141 | 0.651 | 20 | 24 | fits | 63,389 | 139 | 0.406 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 72,550 | 0.726 | 20 | 24 | fits | 62,929 | 139 | 0.398 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 65,851 | 0.659 | 20 | 24 | fits | 64,990 | 116 | 0.426 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 64,772 | 0.648 | 20 | 24 | fits | 63,234 | 139 | 0.397 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 48,172 | 0.482 | 20 | 24 | fits | 62,391 | 139 | 0.383 |
| set_name | `aecp_fanout.set_name.if1` | 70,283 | 0.703 | 20 | 24 | fits | 69,793 | 117 | 0.403 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 67,558 | 0.676 | 20 | 24 | fits | 67,017 | 139 | 0.439 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 72,833 | 0.728 | 20 | 24 | fits | 63,133 | 139 | 0.403 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 64,099 | 0.641 | 20 | 24 | fits | 62,325 | 139 | 0.389 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 64,318 | 0.643 | 20 | 24 | fits | 62,636 | 139 | 0.385 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 48,163 | 0.482 | 20 | 24 | fits | 62,460 | 139 | 0.383 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 15,842 | 0.158 | 20 | 24 | fits | 31,817 | 22 | 0.783 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 31,237 | 0.312 | 20 | 24 | fits | 35,978 | 22 | 0.717 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 25,969 | 0.260 | 20 | 24 | fits | 40,640 | 28 | 0.745 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,824 | 0.178 | 20 | 24 | fits | 31,668 | 22 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 26,608 | 0.266 | 20 | 24 | fits | 32,039 | 22 | 0.743 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 17,914 | 0.179 | 20 | 24 | fits | 31,681 | 22 | 0.728 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 26,116 | 0.261 | 20 | 24 | fits | 31,284 | 22 | 0.747 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 24,306 | 0.243 | 20 | 24 | fits | 31,088 | 22 | 0.753 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,284 | 0.173 | 20 | 24 | fits | 31,039 | 22 | 0.756 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 30,875 | 0.309 | 20 | 24 | fits | 36,121 | 23 | 0.657 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 16,683 | 0.167 | 20 | 24 | fits | 30,426 | 22 | 0.756 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 26,120 | 0.261 | 20 | 24 | fits | 30,986 | 22 | 0.772 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 24,553 | 0.246 | 20 | 24 | fits | 31,478 | 22 | 0.744 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 18,061 | 0.181 | 20 | 24 | fits | 31,924 | 22 | 0.741 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 27,035 | 0.270 | 20 | 24 | fits | 32,411 | 22 | 0.750 |
| get_configuration | `aecp.get_configuration.if0` | 15,292 | 0.153 | 20 | 24 | fits | 28,209 | 22 | 0.735 |
| entity_available | `aecp.entity_available.if0` | 24,647 | 0.246 | 20 | 24 | fits | 29,195 | 22 | 0.750 |
| get_name | `aecp.get_name.if0` | 26,610 | 0.266 | 20 | 24 | fits | 31,519 | 22 | 0.762 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 18,787 | 0.188 | 20 | 24 | fits | 32,246 | 29 | 0.710 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 25,344 | 0.253 | 20 | 24 | fits | 32,806 | 31 | 0.760 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 15,381 | 0.154 | 20 | 24 | fits | 28,647 | 22 | 0.745 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 24,207 | 0.242 | 20 | 24 | fits | 28,611 | 22 | 0.740 |
| set_name | `aecp.set_name.if0` | 48,038 | 0.480 | 20 | 24 | fits | 51,693 | 64 | 0.708 |
| lock_entity | `aecp.lock_entity.if0` | 29,757 | 0.298 | 20 | 24 | fits | 37,262 | 46 | 0.717 |
| unlock_entity | `aecp.unlock_entity.if0` | 39,939 | 0.399 | 20 | 24 | fits | 37,869 | 45 | 0.728 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 17,131 | 0.171 | 20 | 24 | fits | 30,632 | 20 | 0.760 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 32,162 | 0.322 | 20 | 24 | fits | 34,801 | 20 | 0.718 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 29,083 | 0.291 | 20 | 24 | fits | 31,919 | 20 | 0.753 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 19,859 | 0.199 | 20 | 24 | fits | 31,179 | 20 | 0.732 |
| get_configuration | `aecp.get_configuration.if1` | 26,575 | 0.266 | 20 | 24 | fits | 28,709 | 20 | 0.758 |
| entity_available | `aecp.entity_available.if1` | 17,707 | 0.177 | 20 | 24 | fits | 28,252 | 20 | 0.738 |
| get_name | `aecp.get_name.if1` | 20,074 | 0.201 | 20 | 24 | fits | 31,346 | 20 | 0.765 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if1` | 30,432 | 0.304 | 20 | 24 | fits | 32,922 | 27 | 0.731 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if1` | 20,655 | 0.207 | 20 | 24 | fits | 31,800 | 29 | 0.754 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if1` | 27,374 | 0.274 | 20 | 24 | fits | 29,335 | 20 | 0.764 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 24,642 | 0.246 | 20 | 24 | fits | 28,766 | 20 | 0.748 |
| set_name | `aecp.set_name.if1` | 37,783 | 0.378 | 20 | 24 | fits | 45,391 | 25 | 0.765 |
| lock_entity | `aecp.lock_entity.if1` | 41,994 | 0.420 | 20 | 24 | fits | 39,050 | 49 | 0.712 |
| unlock_entity | `aecp.unlock_entity.if1` | 33,098 | 0.331 | 20 | 24 | fits | 38,076 | 48 | 0.701 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 40 paths and 0 of 229 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.077 (0.477) | fits | 0 events | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.223 (2.507) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.510 (0.793) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.497 (0.782) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.550 (0.834) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.514 (0.784) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.595 (0.900) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.241 (2.532) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.410 (0.668) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 1.487 (1.775) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.446 (1.784) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.879 (3.213) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.282 (2.616) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.418 (1.718) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged1-1.adp_available.if0` (backlog-adp@program-aged1-1) | 3.575 (4.101) | fits | 7 adp | 18 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.282 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.525 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.825 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.888 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 8.120 | fits | 31 srp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.205 (0.509) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.094 (0.202) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.103 (0.257) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.184 (0.509) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.170 (0.457) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.420 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-aged2-1.service.acmp.first.if0` (backlog-adp@program-aged2-1) | 3.129 | fits | 0 acmp | 18 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-1.service.acmp.last.if0` (backlog-adp@program-1) | 4.156 | fits | 11 acmp | 18 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-aged2-1.service.adp.first.if0` (backlog-adp@program-aged2-1) | 3.120 | fits | 0 adp | 18 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-1.service.adp.last.if0` (backlog-adp@program-1) | 4.149 | fits | 7 adp | 18 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-1.service.aecp.first.if0` (backlog-adp@verify-1) | 1.613 | fits | 0 aecp | 18 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@program-aged2-1.service.aecp.last.if0` (backlog-adp@program-aged2-1) | 3.155 | fits | 15 aecp | 18 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-aged2-1.service.maap.first.if0` (backlog-adp@program-aged2-1) | 3.155 | fits | 0 maap | 18 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-1.service.maap.last.if0` (backlog-adp@program-1) | 4.186 | fits | 6 maap | 18 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-1.service.srp.first.if0` (backlog-adp@program-1) | 5.089 | fits | 0 srp | 18 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-5.service.srp.last.if0` (backlog-adp@blank-aged1-5) | 9.875 | fits | 31 srp | 18 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.983 (1.096) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.438 (0.438) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.211 (0.212) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.888 (0.962) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-5 | 0 | 10.585 | 11 | 146,514 (1.465) | yes | - |
| backlog-adp@program-1 | 0 | 11.033 | 12 | 149,642 (1.496) | yes | - |
| backlog-adp@program-5 | 0 | 10.042 | 12 | 149,578 (1.496) | yes | - |
| backlog-adp@verify-1 | 0 | 10.363 | 10 | 149,622 (1.496) | yes | - |
| backlog-adp@verify-5 | 0 | 10.465 | 11 | 147,573 (1.476) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.117 | 10 | 149,539 (1.495) | yes | - |
| backlog-adp@blank-aged2-5 | 1 | 10.224 | 9 | 148,101 (1.481) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.154 | 12 | 149,175 (1.492) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.112 | 12 | 149,118 (1.491) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.629 | 12 | 149,164 (1.492) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.297 | 10 | 149,036 (1.490) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.850 | 12 | 149,211 (1.492) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.264 | 9 | 148,558 (1.486) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.110 | 9 | 145,232 (1.452) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.430 | 11 | 149,275 (1.493) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.607 | 12 | 149,184 (1.492) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.190 | 9 | 148,592 (1.486) | yes | - |
| backlog-adp | 0 | 9.466 | 10 | 150,154 (1.502) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill, backlog-owed not run): 150,154 CPU cycles (1.502 ms), backlog-adp.
Over the windows that released their whole load only: 150,154 (1.502 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3609 | 0 | 42,224 (0.422) | fits |
| backlog-adp@blank-5 | 408 | 0 | 147,315 (1.473) | fits |
| backlog-adp@program-1 | 504 | 0 | 149,642 (1.496) | fits |
| backlog-adp@program-5 | 507 | 0 | 149,578 (1.496) | fits |
| backlog-adp@verify-1 | 590 | 0 | 149,622 (1.496) | fits |
| backlog-adp@verify-5 | 592 | 0 | 147,573 (1.476) | fits |
| backlog-adp@blank-aged2-1 | 733 | 0 | 149,539 (1.495) | fits |
| backlog-adp@blank-aged2-5 | 766 | 0 | 149,137 (1.491) | fits |
| backlog-adp@blank-aged1-1 | 673 | 0 | 149,175 (1.492) | fits |
| backlog-adp@blank-aged1-5 | 706 | 0 | 149,118 (1.491) | fits |
| backlog-adp@program-aged2-1 | 830 | 0 | 149,164 (1.492) | fits |
| backlog-adp@program-aged2-5 | 861 | 0 | 149,036 (1.490) | fits |
| backlog-adp@program-aged1-1 | 763 | 0 | 149,211 (1.492) | fits |
| backlog-adp@program-aged1-5 | 794 | 0 | 149,055 (1.491) | fits |
| backlog-adp@verify-aged2-1 | 917 | 0 | 149,118 (1.491) | fits |
| backlog-adp@verify-aged2-5 | 952 | 0 | 149,275 (1.493) | fits |
| backlog-adp@verify-aged1-1 | 853 | 0 | 149,184 (1.492) | fits |
| backlog-adp@verify-aged1-5 | 884 | 0 | 149,099 (1.491) | fits |
| save-held | 1402 | 0 | 153,485 (1.535) | fits |
| srp | 290 | 0 | 69,059 (0.691) | fits |
| backlog-adp | 312 | 0 | 150,154 (1.502) | fits |
| maap | 176 | 0 | 42,159 (0.422) | fits |
| aecp-fanout | 110 | 0 | 66,208 (0.662) | fits |
| aecp-largest-notice | 106 | 0 | 144,287 (1.443) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-1 | 2 | none | +9.044 ms, 76,435 (0.764 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.006 (20) | 10.994 |
| backlog-adp@blank-aged2-5 | 2 | +4.815 ms, 76,706 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.745 (20) | 10.255 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.161 (20) | 10.839 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.875 (20) | 10.125 |
| backlog-adp@program-aged2-1 | 2 | none | +9.070 ms, 80,362 (0.804 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 9.032 (20) | 10.968 |
| backlog-adp@program-aged2-5 | 2 | +5.013 ms, 80,639 (0.806 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.816 (20) | 10.184 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.985 (20) | 11.015 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.980 (20) | 11.020 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.029 ms, 77,281 (0.773 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.991 (20) | 11.009 |
| backlog-adp@verify-aged2-5 | 2 | +4.999 ms, 77,552 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.816 (20) | 10.184 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.967 (20) | 11.033 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.944 (20) | 11.056 |

Least margin over the aged windows: 10.125 ms, `backlog-adp@blank-aged1-5.service.srp.last.if0` at 9.875 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 2018.440 | 4,070 | 102 | - | 15.367 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 95,267 (0.953) | 77,742 (0.777) |
| backlog-adp@blank-5 | 299 | 91,128 (0.911) | 76,157 (0.762) |
| backlog-adp@program-1 | 328 | 95,042 (0.950) | 78,484 (0.785) |
| backlog-adp@program-5 | 329 | 94,759 (0.948) | 77,749 (0.777) |
| backlog-adp@verify-1 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-5 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@blank-aged2-1 | 297 | 76,435 (0.764) | 75,481 (0.755) |
| backlog-adp@blank-aged2-5 | 297 | 76,706 (0.767) | 75,669 (0.757) |
| backlog-adp@blank-aged1-1 | 297 | 96,403 (0.964) | 75,898 (0.759) |
| backlog-adp@blank-aged1-5 | 297 | 90,627 (0.906) | 75,899 (0.759) |
| backlog-adp@program-aged2-1 | 326 | 94,759 (0.948) | 78,192 (0.782) |
| backlog-adp@program-aged2-5 | 326 | 94,759 (0.948) | 78,386 (0.784) |
| backlog-adp@program-aged1-1 | 326 | 94,827 (0.948) | 78,484 (0.785) |
| backlog-adp@program-aged1-5 | 326 | 94,759 (0.948) | 78,482 (0.785) |
| backlog-adp@verify-aged2-1 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged2-5 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| backlog-adp@verify-aged1-1 | 355 | 99,063 (0.991) | 77,749 (0.777) |
| backlog-adp@verify-aged1-5 | 355 | 95,201 (0.952) | 77,749 (0.777) |
| save-held | 722 | 94,090 (0.941) | 78,254 (0.783) |
| srp | 271 | 20,761 (0.208) | 1,935 (0.019) |
| backlog-adp | 271 | 20,761 (0.208) | 2,254 (0.023) |
| maap | 163 | 20,719 (0.207) | 1,935 (0.019) |
| aecp-fanout | 80 | 20,719 (0.207) | 1,935 (0.019) |
| aecp-largest-notice | 78 | 20,719 (0.207) | 1,935 (0.019) |

Longest pass that carries a step: 99,063 CPU cycles (0.991 ms), backlog-adp@verify-aged1-1; longest step: 78,484 (0.785 ms), backlog-adp@program-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 7,735 | 0.077 | 20 | 20 | fits | 32,462 | 19 (14) | 0.881 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 343,415 | 3.434 | 20 | 20 | fits | 105,383 | 177 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 295,633 | 2.956 | 20 | 200 | fits | 146,514 | 259 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 400,400 | 4.004 | 20 | 200 | fits | 105,383 | 177 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 296,557 | 2.966 | 20 | 20 | fits | 146,514 | 259 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 401,104 | 4.011 | 20 | 20 | fits | 105,383 | 177 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 146,056 | 1.461 | 20 | 24 | fits | 147,315 | 115 | 0.396 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 299,207 | 2.992 | 20 | 24 | fits | 146,514 | 259 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 299,141 | 2.991 | 20 | 50 | fits | 146,514 | 259 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 404,128 | 4.041 | 20 | 50 | fits | 105,383 | 177 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 489,918 | 4.899 | 20 | 20 | fits | 85,856 | 30 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 890,782 | 8.908 | 20 | 20 | fits | 63,418 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 356,059 | 3.561 | 20 | 20 | fits | 109,405 | 167 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 297,223 | 2.972 | 20 | 200 | fits | 144,237 | 231 | 0.400 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 414,865 | 4.149 | 20 | 200 | fits | 109,405 | 167 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 298,147 | 2.981 | 20 | 20 | fits | 144,237 | 231 | 0.400 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 415,569 | 4.156 | 20 | 20 | fits | 109,405 | 167 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 157,550 | 1.575 | 20 | 24 | fits | 149,642 | 155 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 300,797 | 3.008 | 20 | 24 | fits | 144,237 | 231 | 0.400 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 300,731 | 3.007 | 20 | 50 | fits | 144,237 | 231 | 0.400 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 418,593 | 4.186 | 20 | 50 | fits | 109,405 | 167 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 508,920 | 5.089 | 20 | 20 | fits | 90,393 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 906,282 | 9.063 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 348,524 | 3.485 | 20 | 20 | fits | 101,788 | 142 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 304,720 | 3.047 | 20 | 200 | fits | 149,353 | 253 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 405,892 | 4.059 | 20 | 200 | fits | 101,788 | 142 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 305,644 | 3.056 | 20 | 20 | fits | 149,353 | 253 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 406,596 | 4.066 | 20 | 20 | fits | 101,788 | 142 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 152,088 | 1.521 | 20 | 24 | fits | 149,578 | 156 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 308,294 | 3.083 | 20 | 24 | fits | 149,353 | 253 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 308,228 | 3.082 | 20 | 50 | fits | 149,353 | 253 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 409,620 | 4.096 | 20 | 50 | fits | 101,788 | 142 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 499,713 | 4.997 | 20 | 20 | fits | 90,159 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 896,954 | 8.970 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 354,879 | 3.549 | 20 | 20 | fits | 98,423 | 154 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 306,011 | 3.060 | 20 | 200 | fits | 149,236 | 233 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 403,818 | 4.038 | 20 | 200 | fits | 98,423 | 154 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 306,935 | 3.069 | 20 | 20 | fits | 149,236 | 233 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 404,522 | 4.045 | 20 | 20 | fits | 98,423 | 154 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 161,339 | 1.613 | 20 | 24 | fits | 149,622 | 155 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 309,585 | 3.096 | 20 | 24 | fits | 149,236 | 233 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 309,519 | 3.095 | 20 | 50 | fits | 149,236 | 233 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 407,546 | 4.075 | 20 | 50 | fits | 98,423 | 154 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 497,677 | 4.977 | 20 | 20 | fits | 90,197 | 28 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 911,695 | 9.117 | 20 | 20 | fits | 59,300 | 26 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 351,429 | 3.514 | 20 | 20 | fits | 105,806 | 177 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 296,576 | 2.966 | 20 | 200 | fits | 147,573 | 259 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 401,766 | 4.018 | 20 | 200 | fits | 105,806 | 177 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 297,500 | 2.975 | 20 | 20 | fits | 147,573 | 259 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 402,470 | 4.025 | 20 | 20 | fits | 105,806 | 177 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 145,938 | 1.459 | 20 | 24 | fits | 147,001 | 115 | 0.393 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 300,150 | 3.002 | 20 | 24 | fits | 147,573 | 259 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 300,084 | 3.001 | 20 | 50 | fits | 147,573 | 259 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 405,494 | 4.055 | 20 | 50 | fits | 105,806 | 177 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 491,227 | 4.912 | 20 | 20 | fits | 85,799 | 30 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 892,226 | 8.922 | 20 | 20 | fits | 63,418 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 350,972 | 3.510 | 20 | 20 | fits | 109,276 | 167 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 291,464 | 2.915 | 20 | 200 | fits | 143,921 | 231 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 409,665 | 4.097 | 20 | 200 | fits | 109,276 | 167 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 292,388 | 2.924 | 20 | 20 | fits | 143,921 | 231 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 410,369 | 4.104 | 20 | 20 | fits | 109,276 | 167 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 152,107 | 1.521 | 20 | 24 | fits | 149,539 | 152 | 0.387 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 295,038 | 2.950 | 20 | 24 | fits | 143,921 | 231 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 294,972 | 2.950 | 20 | 50 | fits | 143,921 | 231 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 413,393 | 4.134 | 20 | 50 | fits | 109,276 | 167 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 503,658 | 5.037 | 20 | 20 | fits | 90,331 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 900,623 | 9.006 | 20 | 20 | fits | 59,712 | 26 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 334,302 | 3.343 | 20 | 20 | fits | 100,528 | 142 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 290,799 | 2.908 | 20 | 200 | fits | 148,101 | 253 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 390,711 | 3.907 | 20 | 200 | fits | 100,528 | 142 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 291,723 | 2.917 | 20 | 20 | fits | 148,101 | 253 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 391,415 | 3.914 | 20 | 20 | fits | 100,528 | 142 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 147,262 | 1.473 | 20 | 24 | fits | 149,137 | 152 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 294,373 | 2.944 | 20 | 24 | fits | 148,101 | 253 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 294,307 | 2.943 | 20 | 50 | fits | 148,101 | 253 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 394,439 | 3.944 | 20 | 50 | fits | 100,528 | 142 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 479,821 | 4.798 | 20 | 20 | fits | 85,448 | 30 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 974,477 | 9.745 | 20 | 20 | fits | 63,317 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 350,695 | 3.507 | 20 | 20 | fits | 98,467 | 154 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 301,747 | 3.017 | 20 | 200 | fits | 149,084 | 233 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 399,598 | 3.996 | 20 | 200 | fits | 98,467 | 154 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 302,671 | 3.027 | 20 | 20 | fits | 149,084 | 233 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 400,302 | 4.003 | 20 | 20 | fits | 98,467 | 154 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 157,227 | 1.572 | 20 | 24 | fits | 149,175 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 305,321 | 3.053 | 20 | 24 | fits | 149,084 | 233 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 305,255 | 3.053 | 20 | 50 | fits | 149,084 | 233 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 403,326 | 4.033 | 20 | 50 | fits | 98,467 | 154 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 493,915 | 4.939 | 20 | 20 | fits | 90,655 | 29 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 916,117 | 9.161 | 20 | 20 | fits | 68,444 | 26 | 0.723 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 338,349 | 3.383 | 20 | 20 | fits | 101,483 | 142 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 294,634 | 2.946 | 20 | 200 | fits | 147,029 | 248 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 395,501 | 3.955 | 20 | 200 | fits | 101,483 | 142 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 295,558 | 2.956 | 20 | 20 | fits | 147,029 | 248 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 396,205 | 3.962 | 20 | 20 | fits | 101,483 | 142 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 152,169 | 1.522 | 20 | 24 | fits | 149,118 | 152 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 298,208 | 2.982 | 20 | 24 | fits | 147,029 | 248 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 298,142 | 2.981 | 20 | 50 | fits | 147,029 | 248 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 399,229 | 3.992 | 20 | 50 | fits | 101,483 | 142 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 483,519 | 4.835 | 20 | 20 | fits | 84,356 | 26 | 0.815 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 987,524 | 9.875 | 20 | 20 | fits | 74,288 | 28 | 0.554 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 355,637 | 3.556 | 20 | 20 | fits | 100,939 | 142 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 311,957 | 3.120 | 20 | 200 | fits | 149,018 | 253 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 412,280 | 4.123 | 20 | 200 | fits | 100,939 | 142 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 312,881 | 3.129 | 20 | 20 | fits | 149,018 | 253 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 412,984 | 4.130 | 20 | 20 | fits | 100,939 | 142 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 159,753 | 1.598 | 20 | 24 | fits | 149,164 | 153 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 315,531 | 3.155 | 20 | 24 | fits | 149,018 | 253 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 315,465 | 3.155 | 20 | 50 | fits | 149,018 | 253 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 416,008 | 4.160 | 20 | 50 | fits | 100,939 | 142 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 506,113 | 5.061 | 20 | 20 | fits | 90,171 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 903,241 | 9.032 | 20 | 20 | fits | 59,740 | 26 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 328,026 | 3.280 | 20 | 20 | fits | 106,386 | 161 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 293,393 | 2.934 | 20 | 200 | fits | 143,900 | 230 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 399,163 | 3.992 | 20 | 200 | fits | 106,386 | 161 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 294,317 | 2.943 | 20 | 20 | fits | 143,900 | 230 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 399,867 | 3.999 | 20 | 20 | fits | 106,386 | 161 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 154,057 | 1.541 | 20 | 24 | fits | 149,036 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 296,967 | 2.970 | 20 | 24 | fits | 143,900 | 230 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 296,901 | 2.969 | 20 | 50 | fits | 143,900 | 230 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 402,891 | 4.029 | 20 | 50 | fits | 106,386 | 161 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 499,559 | 4.996 | 20 | 20 | fits | 87,787 | 37 | 0.758 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 981,561 | 9.816 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 357,499 | 3.575 | 20 | 20 | fits | 102,708 | 161 | 0.467 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 295,993 | 2.960 | 20 | 200 | fits | 149,211 | 234 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 407,260 | 4.073 | 20 | 200 | fits | 102,708 | 161 | 0.467 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 296,917 | 2.969 | 20 | 20 | fits | 149,211 | 234 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 407,964 | 4.080 | 20 | 20 | fits | 102,708 | 161 | 0.467 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 151,346 | 1.513 | 20 | 24 | fits | 149,036 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 299,567 | 2.996 | 20 | 24 | fits | 149,211 | 234 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 299,501 | 2.995 | 20 | 50 | fits | 149,211 | 234 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 410,988 | 4.110 | 20 | 50 | fits | 102,708 | 161 | 0.467 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 501,297 | 5.013 | 20 | 20 | fits | 90,375 | 28 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 898,546 | 8.985 | 20 | 20 | fits | 59,740 | 26 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 333,466 | 3.335 | 20 | 20 | fits | 101,597 | 142 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 289,791 | 2.898 | 20 | 200 | fits | 148,558 | 253 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 390,772 | 3.908 | 20 | 200 | fits | 101,597 | 142 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 290,715 | 2.907 | 20 | 20 | fits | 148,558 | 253 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 391,476 | 3.915 | 20 | 20 | fits | 101,597 | 142 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 145,797 | 1.458 | 20 | 24 | fits | 149,055 | 152 | 0.382 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 293,365 | 2.934 | 20 | 24 | fits | 148,558 | 253 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 293,299 | 2.933 | 20 | 50 | fits | 148,558 | 253 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 394,500 | 3.945 | 20 | 50 | fits | 101,597 | 142 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 479,925 | 4.799 | 20 | 20 | fits | 85,491 | 30 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 898,034 | 8.980 | 20 | 20 | fits | 63,418 | 24 | 0.600 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 333,265 | 3.333 | 20 | 20 | fits | 105,400 | 160 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 286,514 | 2.865 | 20 | 200 | fits | 145,232 | 235 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 391,298 | 3.913 | 20 | 200 | fits | 105,400 | 160 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 287,438 | 2.874 | 20 | 20 | fits | 145,232 | 235 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 392,002 | 3.920 | 20 | 20 | fits | 105,400 | 160 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 145,846 | 1.458 | 20 | 24 | fits | 149,118 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 290,088 | 2.901 | 20 | 24 | fits | 145,232 | 235 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 290,022 | 2.900 | 20 | 50 | fits | 145,232 | 235 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 395,026 | 3.950 | 20 | 50 | fits | 105,400 | 160 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 485,106 | 4.851 | 20 | 20 | fits | 90,146 | 28 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 899,124 | 8.991 | 20 | 20 | fits | 59,300 | 26 | 0.704 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 351,213 | 3.512 | 20 | 20 | fits | 106,948 | 163 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 302,558 | 3.026 | 20 | 200 | fits | 143,516 | 231 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 408,890 | 4.089 | 20 | 200 | fits | 106,948 | 163 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 303,482 | 3.035 | 20 | 20 | fits | 143,516 | 231 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 409,594 | 4.096 | 20 | 20 | fits | 106,948 | 163 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 155,935 | 1.559 | 20 | 24 | fits | 149,275 | 153 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 306,132 | 3.061 | 20 | 24 | fits | 143,516 | 231 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 306,066 | 3.061 | 20 | 50 | fits | 143,516 | 231 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 412,618 | 4.126 | 20 | 50 | fits | 106,948 | 163 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 498,232 | 4.982 | 20 | 20 | fits | 85,680 | 30 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 981,556 | 9.816 | 20 | 20 | fits | 68,293 | 31 | 0.644 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 348,889 | 3.489 | 20 | 20 | fits | 106,070 | 163 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 300,157 | 3.002 | 20 | 200 | fits | 143,547 | 231 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 405,611 | 4.056 | 20 | 200 | fits | 106,070 | 163 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 301,081 | 3.011 | 20 | 20 | fits | 143,547 | 231 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 406,315 | 4.063 | 20 | 20 | fits | 106,070 | 163 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 153,424 | 1.534 | 20 | 24 | fits | 149,184 | 153 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 303,731 | 3.037 | 20 | 24 | fits | 143,547 | 231 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 303,665 | 3.037 | 20 | 50 | fits | 143,547 | 231 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 409,339 | 4.093 | 20 | 50 | fits | 106,070 | 163 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 499,606 | 4.996 | 20 | 20 | fits | 90,333 | 28 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 896,734 | 8.967 | 20 | 20 | fits | 59,740 | 26 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 334,846 | 3.348 | 20 | 20 | fits | 101,908 | 143 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 291,171 | 2.912 | 20 | 200 | fits | 148,592 | 253 | 0.387 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 392,463 | 3.925 | 20 | 200 | fits | 101,908 | 143 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 292,095 | 2.921 | 20 | 20 | fits | 148,592 | 253 | 0.387 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 393,167 | 3.932 | 20 | 20 | fits | 101,908 | 143 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 147,143 | 1.471 | 20 | 24 | fits | 149,099 | 152 | 0.383 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 294,745 | 2.947 | 20 | 24 | fits | 148,592 | 253 | 0.387 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 294,679 | 2.947 | 20 | 50 | fits | 148,592 | 253 | 0.387 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 396,191 | 3.962 | 20 | 50 | fits | 101,908 | 143 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 493,300 | 4.933 | 20 | 20 | fits | 87,889 | 37 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 894,434 | 8.944 | 20 | 20 | fits | 63,420 | 24 | 0.600 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 152,545 | 1.525 | 20 | 200 | fits | 153,485 | 250 | 0.463 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 228,243 | 2.282 | 20 | 20 | fits | 95,835 | 86 | 0.643 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 282,451 | 2.825 | 20 | 24 | fits | 88,261 | 53 | 0.530 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 188,768 | 1.888 | 20 | 50 | fits | 95,835 | 86 | 0.643 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 812,036 | 8.120 | 20 | 20 | fits | 70,881 | 30 | 0.669 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 241,997 | 2.420 | 20 | 20 | fits | 0 | - | 0.000 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 88,788 | 0.888 | 20 | 20 | fits | 28,415 | 8 | 0.833 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 43,758 | 0.438 | 20 | 20 | fits | 43,824 | 12 | 0.884 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,108 | 0.211 | 20 | 20 | fits | 21,174 | 12 | 0.707 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 98,282 | 0.983 | 220 | 220 | fits | 69,059 | 6 | 0.872 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 339,695 | 3.397 | 20 | 20 | fits | 104,425 | 149 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 292,279 | 2.923 | 20 | 200 | fits | 146,875 | 248 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 396,088 | 3.961 | 20 | 200 | fits | 104,425 | 149 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 293,203 | 2.932 | 20 | 20 | fits | 146,875 | 248 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 396,792 | 3.968 | 20 | 20 | fits | 104,425 | 149 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 149,968 | 1.500 | 20 | 24 | fits | 150,154 | 155 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 295,853 | 2.959 | 20 | 24 | fits | 146,875 | 248 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 295,787 | 2.958 | 20 | 50 | fits | 146,875 | 248 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 399,816 | 3.998 | 20 | 50 | fits | 104,425 | 149 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 499,618 | 4.996 | 20 | 20 | fits | 90,679 | 29 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 896,786 | 8.968 | 20 | 20 | fits | 63,415 | 24 | 0.600 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,291 | 0.103 | 20 | 50 | fits | 25,663 | 43 | 0.728 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 14,952 | 0.150 | 20 | 50 | fits | 21,965 | 35 | 0.702 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 17,026 | 0.170 | 20 | 50 | fits | 21,632 | 35 | 0.698 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 18,361 | 0.184 | 20 | 50 | fits | 26,852 | 61 | 0.637 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 20,525 | 0.205 | 20 | 50 | fits | 26,852 | 61 | 0.637 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 9,353 | 0.094 | 20 | 50 | fits | 20,161 | 30 | 0.626 |
| set_name | `aecp_fanout.set_name.if0` | 59,505 | 0.595 | 20 | 24 | fits | 62,052 | 89 | 0.572 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 55,034 | 0.550 | 20 | 24 | fits | 54,770 | 78 | 0.591 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 50,107 | 0.501 | 20 | 24 | fits | 53,116 | 79 | 0.562 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 51,430 | 0.514 | 20 | 24 | fits | 49,184 | 78 | 0.543 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 49,700 | 0.497 | 20 | 24 | fits | 60,455 | 66 | 0.640 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 222,330 | 2.223 | 20 | 24 | fits | 66,208 | 80 | 0.643 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 224,115 | 2.241 | 20 | 24 | fits | 57,608 | 73 | 0.593 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 50,994 | 0.510 | 20 | 24 | fits | 48,770 | 78 | 0.545 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 40,999 | 0.410 | 20 | 24 | fits | 48,099 | 79 | 0.530 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 141,789 | 1.418 | 20 | 24 | fits | 144,287 | 92 | 0.326 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 148,709 | 1.487 | 20 | 24 | fits | 137,151 | 69 | 0.310 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 144,599 | 1.446 | 20 | 24 | fits | 40,189 | 18 | 0.699 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 287,921 | 2.879 | 20 | 24 | fits | 91,297 | 17 | 0.684 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 228,234 | 2.282 | 20 | 24 | fits | 92,937 | 17 | 0.683 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

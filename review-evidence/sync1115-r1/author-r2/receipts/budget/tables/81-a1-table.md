### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 37 paths and 1 of 250 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.207 (0.466) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.121 (0.537) | fits | 0 adp | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.233 (0.756) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.028 (0.326) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.030 (0.337) | fits | 0 events | 2 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.127 (0.322) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.150 (0.535) | fits | 0 events | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.494 (0.813) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.488 (0.864) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.500 (0.817) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.540 (0.908) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.483 (0.834) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.464 (0.784) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@verify-0.adp_available.if0` (backlog-adp@verify-0) | 4.634 (6.133) | fits | 7 adp | 19 | 0 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.343 (0.490) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.400 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 2.601 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.938 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 2.005 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 8.174 | fits | 31 srp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.228 (0.625) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.113 (0.275) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.140 (0.337) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.209 (0.625) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.213 (0.594) | fits | 0 events | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-held.mrpdu.leaveall.if0` (save-held) | 160.557 | MISS ceiling | 0 srp | 3 | 1 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.acmp.first.if0` (backlog-adp@verify-0) | 3.605 | fits | 0 acmp | 20 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.acmp.last.if0` (backlog-adp@verify-0) | 5.981 | fits | 11 acmp | 20 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.adp.first.if0` (backlog-adp@verify-0) | 3.596 | fits | 0 adp | 20 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.adp.last.if0` (backlog-adp@verify-0) | 5.154 | fits | 7 adp | 20 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.aecp.first.if0` (backlog-adp@verify-0) | 2.135 | fits | 0 aecp | 20 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.aecp.last.if0` (backlog-adp@verify-0) | 3.631 | fits | 15 aecp | 20 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.maap.first.if0` (backlog-adp@verify-0) | 3.631 | fits | 0 maap | 20 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@verify-0.service.maap.last.if0` (backlog-adp@verify-0) | 5.192 | fits | 6 maap | 20 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-0.service.srp.first.if0` (backlog-adp@verify-0) | 6.011 | fits | 0 srp | 20 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.srp.last.if0` (backlog-adp@program-aged2-4) | 9.983 | fits | 31 srp | 20 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.231 (0.232) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-1 | 0 | 10.572 | 10 | 155,705 (1.557) | yes | - |
| backlog-adp@blank-4 | 0 | 11.446 | 11 | 153,403 (1.534) | yes | - |
| backlog-adp@program-0 | 0 | 10.525 | 10 | 155,705 (1.557) | yes | - |
| backlog-adp@program-4 | 0 | 9.963 | 10 | 151,383 (1.514) | yes | - |
| backlog-adp@verify-0 | 0 | 11.214 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@verify-4 | 0 | 11.416 | 11 | 151,504 (1.515) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 11.480 | 10 | 156,937 (1.569) | yes | - |
| backlog-adp@blank-aged2-4 | 1 | 10.562 | 9 | 155,130 (1.551) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.803 | 11 | 158,299 (1.583) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.951 | 11 | 158,380 (1.584) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 10.995 | 11 | 154,955 (1.550) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.625 | 10 | 155,960 (1.560) | yes | - |
| backlog-adp@program-aged1-0 | 1 | 10.731 | 9 | 155,210 (1.552) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.717 | 10 | 154,955 (1.550) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.725 | 11 | 158,459 (1.585) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.283 | 12 | 153,358 (1.534) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.117 | 12 | 151,507 (1.515) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.639 | 10 | 155,960 (1.560) | yes | - |
| backlog-adp | 0 | 9.800 | 10 | 151,603 (1.516) | yes | - |
| fixture | 0 | 1.516 | 2 | 92,728 (0.927) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill, backlog-owed not run): 151,603 CPU cycles (1.516 ms), backlog-adp.
Over the windows that released their whole load only: 151,603 (1.516 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3309 | 0 | 163,276 (1.633) | fits |
| backlog-adp@blank-1 | 537 | 0 | 155,705 (1.557) | fits |
| backlog-adp@blank-4 | 539 | 0 | 153,403 (1.534) | fits |
| backlog-adp@program-0 | 893 | 0 | 155,705 (1.557) | fits |
| backlog-adp@program-4 | 896 | 0 | 151,383 (1.514) | fits |
| backlog-adp@verify-0 | 1243 | 0 | 156,507 (1.565) | fits |
| backlog-adp@verify-4 | 1245 | 0 | 151,504 (1.515) | fits |
| backlog-adp@blank-aged2-0 | 779 | 0 | 156,937 (1.569) | fits |
| backlog-adp@blank-aged2-4 | 804 | 0 | 155,130 (1.551) | fits |
| backlog-adp@blank-aged1-0 | 730 | 0 | 158,299 (1.583) | fits |
| backlog-adp@blank-aged1-4 | 755 | 0 | 158,380 (1.584) | fits |
| backlog-adp@program-aged2-0 | 1132 | 0 | 154,955 (1.550) | fits |
| backlog-adp@program-aged2-4 | 1156 | 0 | 155,960 (1.560) | fits |
| backlog-adp@program-aged1-0 | 1080 | 0 | 155,210 (1.552) | fits |
| backlog-adp@program-aged1-4 | 1106 | 0 | 154,955 (1.550) | fits |
| backlog-adp@verify-aged2-0 | 1485 | 0 | 158,459 (1.585) | fits |
| backlog-adp@verify-aged2-4 | 1511 | 0 | 153,358 (1.534) | fits |
| backlog-adp@verify-aged1-0 | 1436 | 0 | 151,507 (1.515) | fits |
| backlog-adp@verify-aged1-4 | 1459 | 0 | 155,960 (1.560) | fits |
| adp-advertise | 598 | 0 | 34,402 (0.344) | fits |
| backlog-adp | 314 | 0 | 151,603 (1.516) | fits |
| maap | 187 | 0 | 34,402 (0.344) | fits |
| aecp-fanout | 109 | 0 | 60,701 (0.607) | fits |
| fixture | 161 | 0 | 92,728 (0.927) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.905 (20) | 11.095 |
| backlog-adp@blank-aged2-4 | 2 | +5.433 ms, 76,960 (0.770 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 9.924 (20) | 10.076 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.238 (20) | 10.762 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.003 (20) | 10.997 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.927 (20) | 11.073 |
| backlog-adp@program-aged2-4 | 2 | +5.533 ms, 80,308 (0.803 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 9.983 (20) | 10.017 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.824 (20) | 11.176 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.280 (20) | 10.720 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.144 (20) | 10.856 |
| backlog-adp@verify-aged2-4 | 2 | +5.537 ms, 77,833 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 9.961 (20) | 10.039 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.048 (20) | 10.952 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.231 (20) | 10.769 |

Least margin over the aged windows: 10.017 ms, `backlog-adp@program-aged2-4.service.srp.last.if0` at 9.983 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4818.227 | 12,470 | 382 | - | 15.047 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,931 (1.009) | 77,812 (0.778) |
| backlog-adp@blank-1 | 339 | 95,574 (0.956) | 76,095 (0.761) |
| backlog-adp@blank-4 | 339 | 96,222 (0.962) | 76,144 (0.761) |
| backlog-adp@program-0 | 448 | 100,633 (1.006) | 78,252 (0.783) |
| backlog-adp@program-4 | 449 | 100,633 (1.006) | 77,865 (0.779) |
| backlog-adp@verify-0 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-4 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@blank-aged2-0 | 338 | 96,417 (0.964) | 76,224 (0.762) |
| backlog-adp@blank-aged2-4 | 337 | 79,331 (0.793) | 75,701 (0.757) |
| backlog-adp@blank-aged1-0 | 338 | 95,833 (0.958) | 76,224 (0.762) |
| backlog-adp@blank-aged1-4 | 337 | 96,478 (0.965) | 76,224 (0.762) |
| backlog-adp@program-aged2-0 | 447 | 100,633 (1.006) | 78,388 (0.784) |
| backlog-adp@program-aged2-4 | 446 | 100,633 (1.006) | 78,011 (0.780) |
| backlog-adp@program-aged1-0 | 447 | 100,633 (1.006) | 78,388 (0.784) |
| backlog-adp@program-aged1-4 | 446 | 100,633 (1.006) | 78,388 (0.784) |
| backlog-adp@verify-aged2-0 | 556 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged2-4 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged1-0 | 556 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged1-4 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| adp-advertise | 577 | 26,258 (0.263) | 2,254 (0.023) |
| backlog-adp | 271 | 26,258 (0.263) | 2,298 (0.023) |
| maap | 174 | 26,196 (0.262) | 2,254 (0.023) |
| aecp-fanout | 79 | 26,196 (0.262) | 2,254 (0.023) |
| fixture | 54 | 21,080 (0.211) | 2,257 (0.023) |

Longest pass that carries a step: 104,368 CPU cycles (1.044 ms), backlog-adp@verify-0; longest step: 78,388 (0.784 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 260,091 | 2.601 | 20 | 200 | fits | 97,755 | 121 | 0.457 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 239,954 | 2.400 | 20 | 20 | fits | 97,755 | 121 | 0.457 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 293,847 | 2.938 | 20 | 24 | fits | 79,761 | 49 | 0.542 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 200,479 | 2.005 | 20 | 50 | fits | 97,755 | 121 | 0.457 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 817,447 | 8.174 | 20 | 20 | fits | 64,896 | 30 | 0.711 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 55,717 | 0.557 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 16,055,717 | 160.557 | 20 | 20 | MISS ceiling | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 179,045 | 1.790 | 20 | 20 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 380,298 | 3.803 | 20 | 20 | fits | 155,705 | 205 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 295,995 | 2.960 | 20 | 200 | fits | 152,208 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 451,084 | 4.511 | 20 | 200 | fits | 155,705 | 205 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 296,919 | 2.969 | 20 | 20 | fits | 152,208 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 534,052 | 5.341 | 20 | 20 | fits | 82,264 | 31 | 0.752 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 148,351 | 1.484 | 20 | 24 | fits | 148,171 | 145 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 299,569 | 2.996 | 20 | 24 | fits | 152,208 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 299,503 | 2.995 | 20 | 50 | fits | 152,208 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 454,812 | 4.548 | 20 | 50 | fits | 155,705 | 205 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 537,010 | 5.370 | 20 | 20 | fits | 82,264 | 31 | 0.752 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 918,020 | 9.180 | 20 | 20 | fits | 38,431 | 18 | 0.842 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 403,225 | 4.032 | 20 | 20 | fits | 153,403 | 192 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 293,182 | 2.932 | 20 | 200 | fits | 149,992 | 193 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 456,271 | 4.563 | 20 | 200 | fits | 153,403 | 192 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 294,106 | 2.941 | 20 | 20 | fits | 149,992 | 193 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 547,421 | 5.474 | 20 | 20 | fits | 90,446 | 45 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 147,754 | 1.478 | 20 | 24 | fits | 148,236 | 145 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 296,756 | 2.968 | 20 | 24 | fits | 149,992 | 193 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 296,690 | 2.967 | 20 | 50 | fits | 149,992 | 193 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 459,999 | 4.600 | 20 | 50 | fits | 153,403 | 192 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 550,379 | 5.504 | 20 | 20 | fits | 90,446 | 45 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 916,628 | 9.166 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 380,078 | 3.801 | 20 | 20 | fits | 155,705 | 205 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 295,775 | 2.958 | 20 | 200 | fits | 152,148 | 180 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 450,864 | 4.509 | 20 | 200 | fits | 155,705 | 205 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 296,699 | 2.967 | 20 | 20 | fits | 152,148 | 180 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 541,850 | 5.418 | 20 | 20 | fits | 90,282 | 36 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 148,191 | 1.482 | 20 | 24 | fits | 148,322 | 145 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 299,349 | 2.993 | 20 | 24 | fits | 152,148 | 180 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 299,283 | 2.993 | 20 | 50 | fits | 152,148 | 180 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 454,592 | 4.546 | 20 | 50 | fits | 155,705 | 205 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 544,808 | 5.448 | 20 | 20 | fits | 90,282 | 36 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 886,462 | 8.865 | 20 | 20 | fits | 83,795 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 426,126 | 4.261 | 20 | 20 | fits | 151,383 | 206 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 308,107 | 3.081 | 20 | 200 | fits | 150,756 | 177 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 469,137 | 4.691 | 20 | 200 | fits | 151,383 | 206 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 309,031 | 3.090 | 20 | 20 | fits | 150,756 | 177 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 552,153 | 5.522 | 20 | 20 | fits | 82,312 | 37 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 161,915 | 1.619 | 20 | 24 | fits | 148,271 | 145 | 0.365 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 311,681 | 3.117 | 20 | 24 | fits | 150,756 | 177 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 311,615 | 3.116 | 20 | 50 | fits | 150,756 | 177 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 472,865 | 4.729 | 20 | 50 | fits | 151,383 | 206 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 555,111 | 5.551 | 20 | 20 | fits | 82,312 | 37 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 927,372 | 9.274 | 20 | 20 | fits | 38,459 | 18 | 0.842 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 463,366 | 4.634 | 20 | 20 | fits | 156,507 | 209 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 359,559 | 3.596 | 20 | 200 | fits | 150,612 | 176 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 515,450 | 5.154 | 20 | 200 | fits | 156,507 | 209 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 360,483 | 3.605 | 20 | 20 | fits | 150,612 | 176 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 598,102 | 5.981 | 20 | 20 | fits | 81,948 | 31 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 213,511 | 2.135 | 20 | 24 | fits | 148,742 | 145 | 0.370 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 363,133 | 3.631 | 20 | 24 | fits | 150,612 | 176 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 363,067 | 3.631 | 20 | 50 | fits | 150,612 | 176 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 519,178 | 5.192 | 20 | 50 | fits | 156,507 | 209 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 601,060 | 6.011 | 20 | 20 | fits | 81,948 | 31 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 981,199 | 9.812 | 20 | 20 | fits | 38,298 | 18 | 0.841 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 399,341 | 3.993 | 20 | 20 | fits | 151,504 | 220 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 291,378 | 2.914 | 20 | 200 | fits | 150,874 | 202 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 452,529 | 4.525 | 20 | 200 | fits | 151,504 | 220 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 292,302 | 2.923 | 20 | 20 | fits | 150,874 | 202 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 543,618 | 5.436 | 20 | 20 | fits | 90,385 | 45 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 145,068 | 1.451 | 20 | 24 | fits | 146,413 | 105 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 294,952 | 2.950 | 20 | 24 | fits | 150,874 | 202 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 294,886 | 2.949 | 20 | 50 | fits | 150,874 | 202 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 456,257 | 4.563 | 20 | 50 | fits | 151,504 | 220 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 546,576 | 5.466 | 20 | 20 | fits | 90,385 | 45 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 912,753 | 9.128 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 403,920 | 4.039 | 20 | 20 | fits | 156,937 | 210 | 0.395 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 300,025 | 3.000 | 20 | 200 | fits | 150,691 | 176 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 456,346 | 4.563 | 20 | 200 | fits | 156,937 | 210 | 0.395 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 300,949 | 3.009 | 20 | 20 | fits | 150,691 | 176 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 553,735 | 5.537 | 20 | 20 | fits | 86,598 | 38 | 0.763 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 153,898 | 1.539 | 20 | 24 | fits | 147,121 | 142 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 303,599 | 3.036 | 20 | 24 | fits | 150,691 | 176 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 303,533 | 3.035 | 20 | 50 | fits | 150,691 | 176 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 460,074 | 4.601 | 20 | 50 | fits | 156,937 | 210 | 0.395 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 556,693 | 5.567 | 20 | 20 | fits | 86,598 | 38 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 890,546 | 8.905 | 20 | 20 | fits | 83,795 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 395,659 | 3.957 | 20 | 20 | fits | 155,130 | 204 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 294,229 | 2.942 | 20 | 200 | fits | 153,412 | 185 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 448,743 | 4.487 | 20 | 200 | fits | 155,130 | 204 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 295,153 | 2.952 | 20 | 20 | fits | 153,412 | 185 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 538,620 | 5.386 | 20 | 20 | fits | 89,173 | 39 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 145,381 | 1.454 | 20 | 24 | fits | 147,168 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 297,803 | 2.978 | 20 | 24 | fits | 153,412 | 185 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 297,737 | 2.977 | 20 | 50 | fits | 153,412 | 185 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 452,471 | 4.525 | 20 | 50 | fits | 155,130 | 204 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 541,578 | 5.416 | 20 | 20 | fits | 89,173 | 39 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 992,431 | 9.924 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 401,788 | 4.018 | 20 | 20 | fits | 158,299 | 196 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 306,106 | 3.061 | 20 | 200 | fits | 150,098 | 192 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 463,789 | 4.638 | 20 | 200 | fits | 158,299 | 196 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 307,030 | 3.070 | 20 | 20 | fits | 150,098 | 192 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 546,818 | 5.468 | 20 | 20 | fits | 82,325 | 32 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 160,572 | 1.606 | 20 | 24 | fits | 147,168 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 309,680 | 3.097 | 20 | 24 | fits | 150,098 | 192 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 309,614 | 3.096 | 20 | 50 | fits | 150,098 | 192 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 467,517 | 4.675 | 20 | 50 | fits | 158,299 | 196 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 549,776 | 5.498 | 20 | 20 | fits | 82,325 | 32 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 923,783 | 9.238 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 411,609 | 4.116 | 20 | 20 | fits | 158,380 | 196 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 315,852 | 3.159 | 20 | 200 | fits | 151,801 | 197 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 473,616 | 4.736 | 20 | 200 | fits | 158,380 | 196 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 316,776 | 3.168 | 20 | 20 | fits | 151,801 | 197 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 563,635 | 5.636 | 20 | 20 | fits | 89,315 | 39 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 158,805 | 1.588 | 20 | 24 | fits | 147,308 | 143 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 319,426 | 3.194 | 20 | 24 | fits | 151,801 | 197 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 319,360 | 3.194 | 20 | 50 | fits | 151,801 | 197 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 477,344 | 4.773 | 20 | 50 | fits | 158,380 | 196 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 566,593 | 5.666 | 20 | 20 | fits | 89,315 | 39 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 900,318 | 9.003 | 20 | 20 | fits | 83,795 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 420,702 | 4.207 | 20 | 20 | fits | 154,955 | 204 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 319,366 | 3.194 | 20 | 200 | fits | 154,050 | 185 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 473,705 | 4.737 | 20 | 200 | fits | 154,955 | 204 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 320,290 | 3.203 | 20 | 20 | fits | 154,050 | 185 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 564,398 | 5.644 | 20 | 20 | fits | 89,989 | 35 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 160,126 | 1.601 | 20 | 24 | fits | 147,219 | 143 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 322,940 | 3.229 | 20 | 24 | fits | 154,050 | 185 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 322,874 | 3.229 | 20 | 50 | fits | 154,050 | 185 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 477,433 | 4.774 | 20 | 50 | fits | 154,955 | 204 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 567,356 | 5.674 | 20 | 20 | fits | 89,989 | 35 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 892,681 | 8.927 | 20 | 20 | fits | 75,351 | 32 | 0.564 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 383,851 | 3.839 | 20 | 20 | fits | 155,960 | 206 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 299,548 | 2.995 | 20 | 200 | fits | 152,161 | 180 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 454,892 | 4.549 | 20 | 200 | fits | 155,960 | 206 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 300,472 | 3.005 | 20 | 20 | fits | 152,161 | 180 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 548,593 | 5.486 | 20 | 20 | fits | 82,795 | 42 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 151,951 | 1.520 | 20 | 24 | fits | 147,000 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 303,122 | 3.031 | 20 | 24 | fits | 152,161 | 180 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 303,056 | 3.031 | 20 | 50 | fits | 152,161 | 180 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 458,620 | 4.586 | 20 | 50 | fits | 155,960 | 206 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 551,551 | 5.516 | 20 | 20 | fits | 82,795 | 42 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 998,299 | 9.983 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 395,397 | 3.954 | 20 | 20 | fits | 155,210 | 205 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 294,055 | 2.941 | 20 | 200 | fits | 153,406 | 185 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 448,649 | 4.486 | 20 | 200 | fits | 155,210 | 205 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 294,979 | 2.950 | 20 | 20 | fits | 153,406 | 185 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 545,568 | 5.456 | 20 | 20 | fits | 85,940 | 38 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 145,213 | 1.452 | 20 | 24 | fits | 147,000 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 297,629 | 2.976 | 20 | 24 | fits | 153,406 | 185 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 297,563 | 2.976 | 20 | 50 | fits | 153,406 | 185 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 452,377 | 4.524 | 20 | 50 | fits | 155,210 | 205 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 548,526 | 5.485 | 20 | 20 | fits | 85,940 | 38 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 882,379 | 8.824 | 20 | 20 | fits | 83,795 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 408,047 | 4.080 | 20 | 20 | fits | 154,955 | 204 | 0.401 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 306,705 | 3.067 | 20 | 200 | fits | 152,280 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 461,044 | 4.610 | 20 | 200 | fits | 154,955 | 204 | 0.401 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 307,629 | 3.076 | 20 | 20 | fits | 152,280 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 550,305 | 5.503 | 20 | 20 | fits | 88,557 | 39 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 158,989 | 1.590 | 20 | 24 | fits | 147,047 | 142 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 310,279 | 3.103 | 20 | 24 | fits | 152,280 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 310,213 | 3.102 | 20 | 50 | fits | 152,280 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 464,772 | 4.648 | 20 | 50 | fits | 154,955 | 204 | 0.401 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 553,263 | 5.533 | 20 | 20 | fits | 88,557 | 39 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 928,008 | 9.280 | 20 | 20 | fits | 32,540 | 12 | 0.826 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 392,500 | 3.925 | 20 | 20 | fits | 158,459 | 195 | 0.405 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 296,910 | 2.969 | 20 | 200 | fits | 149,909 | 192 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 454,753 | 4.548 | 20 | 200 | fits | 158,459 | 195 | 0.405 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 297,834 | 2.978 | 20 | 20 | fits | 149,909 | 192 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 537,423 | 5.374 | 20 | 20 | fits | 81,966 | 31 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 151,565 | 1.516 | 20 | 24 | fits | 147,023 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 300,484 | 3.005 | 20 | 24 | fits | 149,909 | 192 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 300,418 | 3.004 | 20 | 50 | fits | 149,909 | 192 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 458,481 | 4.585 | 20 | 50 | fits | 158,459 | 195 | 0.405 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 540,381 | 5.404 | 20 | 20 | fits | 81,966 | 31 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 914,383 | 9.144 | 20 | 20 | fits | 33,000 | 12 | 0.833 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 405,008 | 4.050 | 20 | 20 | fits | 153,358 | 192 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 295,063 | 2.951 | 20 | 200 | fits | 150,055 | 193 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 458,009 | 4.580 | 20 | 200 | fits | 153,358 | 192 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 295,987 | 2.960 | 20 | 20 | fits | 150,055 | 193 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 549,002 | 5.490 | 20 | 20 | fits | 90,289 | 45 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 149,572 | 1.496 | 20 | 24 | fits | 147,023 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 298,637 | 2.986 | 20 | 24 | fits | 150,055 | 193 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 298,571 | 2.986 | 20 | 50 | fits | 150,055 | 193 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 461,737 | 4.617 | 20 | 50 | fits | 153,358 | 192 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 551,960 | 5.520 | 20 | 20 | fits | 90,289 | 45 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 996,096 | 9.961 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 398,777 | 3.988 | 20 | 20 | fits | 151,507 | 220 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 290,812 | 2.908 | 20 | 200 | fits | 150,311 | 199 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 451,963 | 4.520 | 20 | 200 | fits | 151,507 | 220 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 291,736 | 2.917 | 20 | 20 | fits | 150,311 | 199 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 535,546 | 5.355 | 20 | 20 | fits | 82,879 | 37 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 145,065 | 1.451 | 20 | 24 | fits | 149,168 | 111 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 294,386 | 2.944 | 20 | 24 | fits | 150,311 | 199 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 294,320 | 2.943 | 20 | 50 | fits | 150,311 | 199 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 455,691 | 4.557 | 20 | 50 | fits | 151,507 | 220 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 538,504 | 5.385 | 20 | 20 | fits | 82,879 | 37 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 904,764 | 9.048 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 388,484 | 3.885 | 20 | 20 | fits | 155,960 | 206 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 304,181 | 3.042 | 20 | 200 | fits | 152,302 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 459,525 | 4.595 | 20 | 200 | fits | 155,960 | 206 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 305,105 | 3.051 | 20 | 20 | fits | 152,302 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 553,678 | 5.537 | 20 | 20 | fits | 83,247 | 42 | 0.771 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 156,443 | 1.564 | 20 | 24 | fits | 146,958 | 142 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 307,755 | 3.078 | 20 | 24 | fits | 152,302 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 307,689 | 3.077 | 20 | 50 | fits | 152,302 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 463,253 | 4.633 | 20 | 50 | fits | 155,960 | 206 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 556,636 | 5.566 | 20 | 20 | fits | 83,247 | 42 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 923,106 | 9.231 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| LINK_UP | `adp.link_up.if0` | 2,986 | 0.030 | 20 | 200 | fits | 33,705 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,035 | 0.150 | 20 | 200 | fits | 26,764 | 23 (39) | 0.725 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 12,688 | 0.127 | 20 | 200 | fits | 3,116 | 10 (11) | 0.538 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 401,749 | 4.017 | 20 | 20 | fits | 149,616 | 187 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 294,985 | 2.950 | 20 | 200 | fits | 151,603 | 198 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 454,193 | 4.542 | 20 | 200 | fits | 149,616 | 187 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 295,909 | 2.959 | 20 | 20 | fits | 151,603 | 198 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 545,049 | 5.450 | 20 | 20 | fits | 90,152 | 45 | 0.732 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 147,946 | 1.479 | 20 | 24 | fits | 148,132 | 145 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 298,559 | 2.986 | 20 | 24 | fits | 151,603 | 198 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 298,493 | 2.985 | 20 | 50 | fits | 151,603 | 198 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 457,921 | 4.579 | 20 | 50 | fits | 149,616 | 187 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 548,007 | 5.480 | 20 | 20 | fits | 90,152 | 45 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 914,336 | 9.143 | 20 | 20 | fits | 32,486 | 12 | 0.824 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 14,049 | 0.140 | 20 | 50 | fits | 33,705 | 43 | 0.731 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 21,336 | 0.213 | 20 | 50 | fits | 29,381 | 35 | 0.727 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 19,872 | 0.199 | 20 | 50 | fits | 29,220 | 35 | 0.721 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 20,946 | 0.209 | 20 | 50 | fits | 34,402 | 61 | 0.633 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 22,823 | 0.228 | 20 | 50 | fits | 34,402 | 61 | 0.633 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 11,277 | 0.113 | 20 | 50 | fits | 27,525 | 30 | 0.628 |
| set_name | `aecp_fanout.set_name.if0` | 54,001 | 0.540 | 20 | 24 | fits | 59,564 | 89 | 0.566 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 48,761 | 0.488 | 20 | 24 | fits | 55,238 | 78 | 0.588 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 50,015 | 0.500 | 20 | 24 | fits | 50,382 | 79 | 0.532 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 39,598 | 0.396 | 20 | 24 | fits | 60,701 | 93 | 0.582 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 48,265 | 0.483 | 20 | 24 | fits | 54,542 | 67 | 0.579 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 49,417 | 0.494 | 20 | 24 | fits | 49,924 | 78 | 0.532 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 46,397 | 0.464 | 20 | 24 | fits | 49,480 | 79 | 0.531 |
| LINK_UP | `fixture.link_up.if0` | 2,986 | 0.030 | 20 | 200 | fits | 33,705 | 43 (11) | 0.731 |
| malformed MRPDU discard | `fixture.malformed.if0` | 23,140 | 0.231 | 20 | 20 | fits | 23,206 | 12 | 0.729 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 34,300 | 0.343 | 20 | 24 | fits | 49,031 | 43 | 0.777 |
| LINK_DOWN | `fixture.link_down.if0` | 2,847 | 0.028 | 20 | 200 | fits | 32,621 | 23 (9) | 0.798 |
| BIND_RX | `fixture.bind_rx.if0` | 20,676 | 0.207 | 20 | 20 | fits | 46,573 | 26 (77) | 0.802 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 23,338 | 0.233 | 20 | 20 | fits | 45,009 | 29 (35) | 0.784 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 12,149 | 0.121 | 20 | 20 | fits | 30,546 | 13 (29) | 0.801 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 92,624 | 0.926 | 20 | 200 | fits | 92,728 | 77 | 0.746 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 92,624 | 0.926 | 20 | 200 | fits | 92,728 | 77 | 0.746 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 92,350 | 0.923 | 20 | 20 | fits | 92,728 | 77 | 0.746 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 92,350 | 0.923 | 20 | 20 | fits | 92,728 | 77 | 0.746 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 92,558 | 0.926 | 20 | 24 | fits | 92,728 | 77 | 0.746 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 92,558 | 0.926 | 20 | 24 | fits | 92,728 | 77 | 0.746 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 92,492 | 0.925 | 20 | 50 | fits | 92,728 | 77 | 0.746 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 92,492 | 0.925 | 20 | 50 | fits | 92,728 | 77 | 0.746 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 92,426 | 0.924 | 20 | 20 | fits | 92,728 | 77 | 0.746 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 92,426 | 0.924 | 20 | 20 | fits | 92,728 | 77 | 0.746 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

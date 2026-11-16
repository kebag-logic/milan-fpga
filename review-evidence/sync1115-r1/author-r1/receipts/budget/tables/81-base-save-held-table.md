### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 23 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.211 (0.470) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.167 (0.503) | fits | 0 adp | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.166 (0.669) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.362) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `fixture.link_up.if0` (fixture) | 0.027 (0.313) | fits | 0 events | 1 | 0 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.371 (0.513) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.821 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 2.589 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.994 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.777 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 8.942 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 3.798 | fits | 0 srp | 3 | 0 |
| ACMP record released under the composed load, first | 0 | `fixture.service.acmp.first.if0` (fixture) | 0.918 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `fixture.service.acmp.last.if0` (fixture) | 0.918 | fits | 0 acmp | 1 | 0 |
| ADP record released under the composed load, first | 0 | `fixture.service.adp.first.if0` (fixture) | 0.920 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `fixture.service.adp.last.if0` (fixture) | 0.920 | fits | 0 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `fixture.service.aecp.first.if0` (fixture) | 0.920 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `fixture.service.aecp.last.if0` (fixture) | 0.920 | fits | 0 aecp | 1 | 0 |
| MAAP record released under the composed load, first | 0 | `fixture.service.maap.first.if0` (fixture) | 0.919 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `fixture.service.maap.last.if0` (fixture) | 0.919 | fits | 0 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `fixture.service.srp.first.if0` (fixture) | 0.918 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `fixture.service.srp.last.if0` (fixture) | 0.918 | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.242 (0.243) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| fixture | 0 | 1.451 | 2 | 92,141 (0.921) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3306 | 0 | 154,703 (1.547) | fits |
| fixture | 161 | 0 | 94,431 (0.944) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4817.268 | 12,470 | 382 | - | 16.687 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 101,182 (1.012) | 78,367 (0.784) |
| fixture | 54 | 21,862 (0.219) | 2,373 (0.024) |

Longest pass that carries a step: 101,182 CPU cycles (1.012 ms), save-held; longest step: 78,367 (0.784 ms), save-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 258,874 | 2.589 | 20 | 200 | fits | 105,111 | 130 | 0.445 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 282,064 | 2.821 | 20 | 20 | fits | 96,127 | 54 | 0.552 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 299,421 | 2.994 | 20 | 24 | fits | 93,597 | 59 | 0.569 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 177,706 | 1.777 | 20 | 50 | fits | 54,556 | 55 | 0.520 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 894,171 | 8.942 | 20 | 20 | fits | 45,945 | 16 | 0.727 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 184,098 | 1.841 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 266,949 | 2.669 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 379,797 | 3.798 | 20 | 20 | fits | 0 | - | 0.000 |
| LINK_UP | `fixture.link_up.if0` | 2,709 | 0.027 | 20 | 200 | fits | 31,287 | 43 (11) | 0.719 |
| malformed MRPDU discard | `fixture.malformed.if0` | 24,237 | 0.242 | 20 | 20 | fits | 24,303 | 12 | 0.713 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 37,099 | 0.371 | 20 | 24 | fits | 51,290 | 43 | 0.779 |
| LINK_DOWN | `fixture.link_down.if0` | 2,549 | 0.025 | 20 | 200 | fits | 36,240 | 23 (9) | 0.771 |
| BIND_RX | `fixture.bind_rx.if0` | 21,087 | 0.211 | 20 | 20 | fits | 46,995 | 26 (77) | 0.808 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 16,615 | 0.166 | 20 | 20 | fits | 48,598 | 37 (35) | 0.740 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 16,734 | 0.167 | 20 | 20 | fits | 29,398 | 13 (29) | 0.801 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 92,037 | 0.920 | 20 | 200 | fits | 92,141 | 51 | 0.755 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 92,037 | 0.920 | 20 | 200 | fits | 92,141 | 51 | 0.755 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 91,763 | 0.918 | 20 | 20 | fits | 92,141 | 51 | 0.755 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 91,763 | 0.918 | 20 | 20 | fits | 92,141 | 51 | 0.755 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 91,971 | 0.920 | 20 | 24 | fits | 92,141 | 51 | 0.755 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 91,971 | 0.920 | 20 | 24 | fits | 92,141 | 51 | 0.755 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 91,905 | 0.919 | 20 | 50 | fits | 92,141 | 51 | 0.755 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 91,905 | 0.919 | 20 | 50 | fits | 92,141 | 51 | 0.755 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 91,839 | 0.918 | 20 | 20 | fits | 92,141 | 51 | 0.755 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 91,839 | 0.918 | 20 | 20 | fits | 92,141 | 51 | 0.755 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

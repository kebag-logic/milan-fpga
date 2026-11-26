### 1x1

1 of 17 paths and 1 of 17 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 1.625 (3.594) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 25.174 (50.781) | MISS ceiling | 0 adp | 1 | 1 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 5.478 (47.980) | fits | 3 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.078 (5.551) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `fixture.link_up.if0` (fixture) | 0.106 (4.969) | fits | 0 events | 1 | 0 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 5.756 (8.837) | fits | 0 aecp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `fixture.service.acmp.first.if0` (fixture) | 8.363 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `fixture.service.acmp.last.if0` (fixture) | 8.363 | fits | 0 acmp | 1 | 0 |
| ADP record released under the composed load, first | 0 | `fixture.service.adp.first.if0` (fixture) | 8.366 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `fixture.service.adp.last.if0` (fixture) | 8.366 | fits | 0 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `fixture.service.aecp.first.if0` (fixture) | 8.365 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `fixture.service.aecp.last.if0` (fixture) | 8.365 | fits | 0 aecp | 1 | 0 |
| MAAP record released under the composed load, first | 0 | `fixture.service.maap.first.if0` (fixture) | 8.365 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `fixture.service.maap.last.if0` (fixture) | 8.365 | fits | 0 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `fixture.service.srp.first.if0` (fixture) | 11.722 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `fixture.service.srp.last.if0` (fixture) | 11.722 | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 2.149 (2.150) | fits | 0 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| fixture | 0 | 20.000 | 3 | 418,342 (8.367) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 100,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| fixture | 47 | 25 | 1,435,369 (28.707) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `fixture.link_up.if0` | 5,281 | 0.106 | 20 | 200 | fits | 248,452 | 88 (12) | 0.886 |
| malformed MRPDU discard | `fixture.malformed.if0` | 107,473 | 2.149 | 20 | 20 | fits | 107,505 | 35 | 0.871 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 287,812 | 5.756 | 20 | 24 | fits | 345,891 | 106 | 0.881 |
| LINK_DOWN | `fixture.link_down.if0` | 3,917 | 0.078 | 20 | 200 | fits | 277,531 | 33 (9) | 0.879 |
| BIND_RX | `fixture.bind_rx.if0` | 81,248 | 1.625 | 20 | 20 | fits | 179,721 | 82 (77) | 0.868 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 273,899 | 5.478 | 20 | 20 | fits | 1,151,720 | 124 (35) | 0.890 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 1,258,710 | 25.174 | 20 | 20 | MISS ceiling | 1,291,990 | 98 (29) | 0.892 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 418,291 | 8.366 | 20 | 200 | fits | 418,342 | 224 | 0.882 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 418,291 | 8.366 | 20 | 200 | fits | 418,342 | 224 | 0.882 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 418,156 | 8.363 | 20 | 20 | fits | 418,342 | 224 | 0.882 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 418,156 | 8.363 | 20 | 20 | fits | 418,342 | 224 | 0.882 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 418,258 | 8.365 | 20 | 24 | fits | 418,342 | 224 | 0.882 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 418,258 | 8.365 | 20 | 24 | fits | 418,342 | 224 | 0.882 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 418,226 | 8.365 | 20 | 50 | fits | 418,342 | 224 | 0.882 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 418,226 | 8.365 | 20 | 50 | fits | 418,342 | 224 | 0.882 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 586,102 | 11.722 | 20 | 20 | fits | 167,909 | 37 | 0.871 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 586,102 | 11.722 | 20 | 20 | fits | 167,909 | 37 | 0.871 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `fixture`: wait quiet TIMEOUT
- `fixture`: wait quiet TIMEOUT


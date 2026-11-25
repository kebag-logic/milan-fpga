### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 12 paths and 7 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.014 (64.315) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.778 (65.078) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 2.993 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 63.036 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 3.036 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 4.338 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.518 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 63.071 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 3.018 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 3.014 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 4.322 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 7.600 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 65.417 | 23 | 172,208 (1.722) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 172,208 CPU cycles (1.722 ms), backlog-owed.
Over the windows that released their whole load only: 172,208 (1.722 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-owed | 307 | 0 | 172,208 (1.722) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-owed | 277 | 22,867 (0.229) | 2,920 (0.029) |

Longest pass that carries a step: 22,867 CPU cycles (0.229 ms), backlog-owed; longest step: 2,920 (0.029 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,401,426 | 64.014 | 20 | 20 | MISS ceiling | 19,260 | 13 | 0.451 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,420,677 | 64.207 | 20 | 20 | MISS ceiling | 19,258 | 13 | 0.412 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,439,672 | 64.397 | 20 | 20 | MISS ceiling | 19,071 | 13 | 0.438 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,458,746 | 64.587 | 20 | 20 | MISS ceiling | 19,150 | 13 | 0.438 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,477,829 | 64.778 | 20 | 20 | MISS ceiling | 19,146 | 13 | 0.429 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 303,579 | 3.036 | 20 | 200 | fits | 151,116 | 252 | 0.233 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 433,812 | 4.338 | 20 | 200 | fits | 130,849 | 59 | 0.631 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 299,257 | 2.993 | 20 | 20 | fits | 151,116 | 252 | 0.233 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,303,567 | 63.036 | 20 | 20 | MISS ceiling | 92,944 | 42 | 0.524 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 151,781 | 1.518 | 20 | 24 | fits | 146,797 | 107 | 0.437 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,307,053 | 63.071 | 20 | 24 | MISS ceiling | 92,944 | 42 | 0.524 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 301,841 | 3.018 | 20 | 50 | fits | 151,116 | 252 | 0.233 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 301,445 | 3.014 | 20 | 50 | fits | 151,116 | 252 | 0.233 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 432,228 | 4.322 | 20 | 20 | fits | 130,849 | 59 | 0.631 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 759,952 | 7.600 | 20 | 20 | fits | 72,975 | 28 | 0.685 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

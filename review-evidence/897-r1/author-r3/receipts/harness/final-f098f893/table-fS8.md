### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 8 paths and 0 of 8 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.741 (1.907) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.812 (2.010) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.564 (0.564) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.552 (0.552) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.286 (0.287) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.290 (0.291) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.466 (1.534) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.488 (1.550) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp | 316 | 0 | 149,156 (1.492) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp | 278 | 34,212 (0.342) | 2,651 (0.027) |

Longest pass that carries a step: 34,212 CPU cycles (0.342 ms), srp; longest step: 2,651 (0.027 ms), srp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| startup declarations (LINK_UP) | `srp.startup.if0` | 146,641 | 1.466 | 20 | 20 | fits | 26,826 | 8 | 0.794 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 148,762 | 1.488 | 20 | 20 | fits | 26,713 | 8 | 0.808 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 56,351 | 0.564 | 20 | 20 | fits | 56,417 | 13 | 0.887 |
| malformed MRPDU discard | `srp.malformed.if0` | 28,604 | 0.286 | 20 | 20 | fits | 28,670 | 13 | 0.733 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 174,124 | 1.741 | 220 | 220 | fits | 138,998 | 7 | 0.795 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 55,168 | 0.552 | 20 | 20 | fits | 55,234 | 13 | 0.879 |
| malformed MRPDU discard | `srp.malformed.if1` | 29,011 | 0.290 | 20 | 20 | fits | 29,077 | 13 | 0.736 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 181,239 | 1.812 | 220 | 220 | fits | 149,156 | 6 | 0.788 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

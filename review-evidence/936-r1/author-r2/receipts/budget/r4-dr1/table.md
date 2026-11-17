Original file: <scratch>/r4/budget/r4-dr1/results/table.md
Original size: 11928 bytes
Original sha256: 232e5b9359a73f729f076161841c1db1aa9b3a361c026acdce8aa9364f268b42

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 0 paths and 0 of 0 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| talker-notice-0 | 1564 | 0 | 160,729 (1.607) | fits |
| talker-notice-1 | 1564 | 0 | 160,472 (1.605) | fits |
| talker-notice-2 | 1564 | 0 | 156,078 (1.561) | fits |
| talker-notice-3 | 1565 | 0 | 155,628 (1.556) | fits |
| talker-notice-4 | 1569 | 0 | 155,628 (1.556) | fits |
| talker-notice-5 | 1568 | 0 | 155,810 (1.558) | fits |
| talker-notice-6 | 1568 | 0 | 155,628 (1.556) | fits |
| talker-notice-7 | 1569 | 0 | 155,608 (1.556) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| talker-notice-0 | 354 | 100,561 (1.006) | 78,433 (0.784) |
| talker-notice-1 | 354 | 100,575 (1.006) | 78,433 (0.784) |
| talker-notice-2 | 354 | 100,561 (1.006) | 78,433 (0.784) |
| talker-notice-3 | 354 | 100,561 (1.006) | 78,433 (0.784) |
| talker-notice-4 | 354 | 96,418 (0.964) | 78,363 (0.784) |
| talker-notice-5 | 354 | 96,414 (0.964) | 78,363 (0.784) |
| talker-notice-6 | 354 | 96,418 (0.964) | 78,363 (0.784) |
| talker-notice-7 | 354 | 96,418 (0.964) | 78,363 (0.784) |

Longest pass that carries a step: 100,575 CPU cycles (1.006 ms), talker-notice-1; longest step: 78,433 (0.784 ms), talker-notice-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.declared.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-0.withdrawn.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.declared.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-1.withdrawn.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.declared.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-2.withdrawn.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.declared.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-3.withdrawn.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.declared.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-4.withdrawn.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.declared.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-5.withdrawn.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.declared.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-6.withdrawn.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.declared.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |
| a Talker withdrawn as MAAP loses its range, from the ANNOUNCE's commit to its STREAM_OUTPUT's notice to every registration (#936) | `talker-notice-7.withdrawn.if0` | - | - | - | - | no end: no notification to ['0a0b0c0d0e0f1000@if0', '0a0b0c0d0e0f1001@if0', '0a0b0c0d0e0f1002@if0', '0a0b0c0d0e0f1003@if0', '0a0b0c0d0e0f1004@if0', '0a0b0c0d0e0f1005@if0', '0a0b0c0d0e0f1006@if0', '0a0b0c0d0e0f1007@if0', '0a0b0c0d0e0f1008@if0', '0a0b0c0d0e0f1009@if0', '0a0b0c0d0e0f100a@if0', '0a0b0c0d0e0f100b@if0', '0a0b0c0d0e0f100c@if0', '0a0b0c0d0e0f100d@if0', '0a0b0c0d0e0f100e@if0', '0a0b0c0d0e0f100f@if0'] | - | - | - |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

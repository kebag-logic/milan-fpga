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
| save-bind | 1787 | 0 | 46,388 (0.464) | fits |
| save-bind-in-capture | 894 | 0 | 94,332 (0.943) | fits |
| save-bind-in-seal | 896 | 0 | 94,718 (0.947) | fits |
| save-bind-in-erase | 895 | 0 | 95,426 (0.954) | fits |
| save-bind-in-erase-late | 902 | 0 | 94,568 (0.946) | fits |
| save-bind-in-blank | 857 | 0 | 97,833 (0.978) | fits |
| save-bind-in-blank-late | 910 | 0 | 97,833 (0.978) | fits |
| save-bind-in-program | 858 | 0 | 46,133 (0.461) | fits |
| save-bind-in-program-late | 861 | 0 | 95,345 (0.953) | fits |
| save-bind-in-verify | 909 | 0 | 98,455 (0.985) | fits |
| save-bind-in-verify-late | 860 | 0 | 98,781 (0.988) | fits |
| save-bind-burst | 1743 | 0 | 98,772 (0.988) | fits |

Binding changes from their response to durable (bind_save.py; the binding class's 100 ms window, Milan v1.2 5.5.3.5.3 and 5.3.8.3), with the part's erase of 120 ms and page program of 0.5 ms modelled:

| Group | Command | Sink | Durable, ms | Target ms | Saves | Erases | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| save-bind | BIND_RX | 0 | 304.506 | 800 | 4 | 4 | within |
| save-bind | STOP_STREAMING | 0 | 304.212 | 800 | 4 | 4 | within |
| save-bind | START_STREAMING | 0 | 304.189 | 800 | 4 | 4 | within |
| save-bind | UNBIND_RX | 0 | 304.535 | 800 | 4 | 4 | within |
| save-bind-in-capture | BIND_RX | 0 | 394.959 | 450 | 2 | 2 | within |
| save-bind-in-seal | BIND_RX | 0 | 392.866 | 450 | 2 | 2 | within |
| save-bind-in-erase | BIND_RX | 0 | 391.169 | 450 | 2 | 2 | within |
| save-bind-in-erase-late | BIND_RX | 0 | 330.538 | 450 | 2 | 2 | within |
| save-bind-in-blank | BIND_RX | 0 | 298.809 | 450 | 2 | 2 | within |
| save-bind-in-blank-late | BIND_RX | 0 | 298.591 | 450 | 2 | 2 | within |
| save-bind-in-program | BIND_RX | 0 | 305.495 | 450 | 2 | 2 | within |
| save-bind-in-program-late | BIND_RX | 0 | 298.517 | 450 | 2 | 2 | within |
| save-bind-in-verify | BIND_RX | 0 | 305.254 | 450 | 2 | 2 | within |
| save-bind-in-verify-late | BIND_RX | 0 | 303.246 | 450 | 2 | 2 | within |
| save-bind-burst | UNBIND_RX | 0 | 306.463 | 450 | 4 | 4 | within |
| save-bind-burst | UNBIND_RX | 1 | 296.522 | 450 | 4 | 4 | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-bind | 3935 | 93,943 (0.939) | 78,458 (0.785) |
| save-bind-in-capture | 2059 | 94,332 (0.943) | 78,131 (0.781) |
| save-bind-in-seal | 2052 | 94,718 (0.947) | 78,131 (0.781) |
| save-bind-in-erase | 2055 | 95,426 (0.954) | 78,261 (0.783) |
| save-bind-in-erase-late | 2076 | 94,568 (0.946) | 78,261 (0.783) |
| save-bind-in-blank | 2107 | 97,833 (0.978) | 78,210 (0.782) |
| save-bind-in-blank-late | 2112 | 97,833 (0.978) | 78,261 (0.783) |
| save-bind-in-program | 2106 | 93,168 (0.932) | 78,210 (0.782) |
| save-bind-in-program-late | 2113 | 95,345 (0.953) | 78,543 (0.785) |
| save-bind-in-verify | 2121 | 98,455 (0.985) | 78,410 (0.784) |
| save-bind-in-verify-late | 2123 | 98,781 (0.988) | 78,210 (0.782) |
| save-bind-burst | 3463 | 98,772 (0.988) | 78,756 (0.788) |

Longest pass that carries a step: 98,781 CPU cycles (0.988 ms), save-bind-in-verify-late; longest step: 78,756 (0.788 ms), save-bind-burst.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|

Bounded waits that timed out (the probe is graded on what the log holds):

- none

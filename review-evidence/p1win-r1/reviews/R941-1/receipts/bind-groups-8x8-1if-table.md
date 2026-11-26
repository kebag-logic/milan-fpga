### 8x8-1if

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
| save-bind | 1664 | 0 | 114,024 (1.140) | fits |
| save-bind-in-capture | 843 | 0 | 113,802 (1.138) | fits |
| save-bind-in-seal | 845 | 0 | 113,623 (1.136) | fits |
| save-bind-in-erase | 846 | 0 | 113,753 (1.138) | fits |
| save-bind-in-erase-late | 853 | 0 | 113,802 (1.138) | fits |
| save-bind-in-blank | 909 | 0 | 113,753 (1.138) | fits |
| save-bind-in-blank-late | 871 | 0 | 114,088 (1.141) | fits |
| save-bind-in-program | 917 | 0 | 114,165 (1.142) | fits |
| save-bind-in-program-late | 927 | 0 | 113,712 (1.137) | fits |
| save-bind-in-verify | 875 | 0 | 113,702 (1.137) | fits |
| save-bind-in-verify-late | 935 | 0 | 113,797 (1.138) | fits |
| save-bind-burst | 5327 | 0 | 115,805 (1.158) | fits |

Binding changes from their response to durable (bind_save.py; the binding class's 100 ms window, Milan v1.2 5.5.3.5.3 and 5.3.8.3), with the part's erase of 120 ms and page program of 0.5 ms modelled:

| Group | Command | Sink | Durable, ms | Target ms | Saves | Erases | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| save-bind | BIND_RX | 0 | 550.477 | 800 | 4 | 4 | within |
| save-bind | STOP_STREAMING | 0 | 549.97 | 800 | 4 | 4 | within |
| save-bind | START_STREAMING | 0 | 550.481 | 800 | 4 | 4 | within |
| save-bind | UNBIND_RX | 0 | 550.417 | 800 | 4 | 4 | within |
| save-bind-in-capture | BIND_RX | 0 | 891.169 | 950 | 2 | 2 | within |
| save-bind-in-seal | BIND_RX | 0 | 880.349 | 950 | 2 | 2 | within |
| save-bind-in-erase | BIND_RX | 0 | 870.845 | 950 | 2 | 2 | within |
| save-bind-in-erase-late | BIND_RX | 0 | 810.709 | 950 | 2 | 2 | within |
| save-bind-in-blank | BIND_RX | 0 | 750.094 | 950 | 2 | 2 | within |
| save-bind-in-blank-late | BIND_RX | 0 | 650.089 | 950 | 2 | 2 | within |
| save-bind-in-program | BIND_RX | 0 | 649.101 | 950 | 2 | 2 | within |
| save-bind-in-program-late | BIND_RX | 0 | 558.193 | 950 | 2 | 2 | within |
| save-bind-in-verify | BIND_RX | 0 | 553.369 | 950 | 2 | 2 | within |
| save-bind-in-verify-late | BIND_RX | 0 | 552.76 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 1 | 646.392 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 2 | 637.148 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 3 | 626.699 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 4 | 616.649 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 5 | 607.244 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 6 | 596.839 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 7 | 586.566 | 950 | 2 | 2 | within |
| save-bind-burst | BIND_RX | 8 | 576.35 | 950 | 2 | 2 | within |
| save-bind-burst | UNBIND_RX | 0 | 567.193 | 950 | 2 | 2 | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-bind | 4705 | 114,024 (1.140) | 78,650 (0.786) |
| save-bind-in-capture | 2446 | 113,802 (1.138) | 78,650 (0.786) |
| save-bind-in-seal | 2446 | 113,623 (1.136) | 78,650 (0.786) |
| save-bind-in-erase | 2445 | 113,753 (1.138) | 78,650 (0.786) |
| save-bind-in-erase-late | 2469 | 113,802 (1.138) | 78,650 (0.786) |
| save-bind-in-blank | 2490 | 113,753 (1.138) | 78,681 (0.787) |
| save-bind-in-blank-late | 2507 | 114,088 (1.141) | 78,650 (0.786) |
| save-bind-in-program | 2501 | 114,165 (1.142) | 78,650 (0.786) |
| save-bind-in-program-late | 2510 | 113,712 (1.137) | 78,647 (0.786) |
| save-bind-in-verify | 2520 | 113,702 (1.137) | 78,647 (0.786) |
| save-bind-in-verify-late | 2526 | 113,797 (1.138) | 78,647 (0.786) |
| save-bind-burst | 1927 | 115,805 (1.158) | 79,101 (0.791) |

Longest pass that carries a step: 115,805 CPU cycles (1.158 ms), save-bind-burst; longest step: 79,101 (0.791 ms), save-bind-burst.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|

Bounded waits that timed out (the probe is graded on what the log holds):

- none

### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 124 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.186 (0.404) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.086 (0.239) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.101 (0.257) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.094 (0.247) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.098 (0.246) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.099 (0.255) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.092 (0.322) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.131 (0.391) | fits | 0 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-1.adp_available.if0` (backlog-adp@program-1) | 3.695 (4.377) | fits | 7 adp | 10 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.251 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.569 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.956 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.856 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 9.027 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.259 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@program-1.service.acmp.first.if0` (backlog-adp@program-1) | 3.226 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-1.service.acmp.last.if0` (backlog-adp@program-1) | 4.188 | fits | 11 acmp | 10 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@program-1.service.adp.first.if0` (backlog-adp@program-1) | 3.217 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-1.service.adp.last.if0` (backlog-adp@program-1) | 4.181 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@program-1.service.aecp.first.if0` (backlog-adp@program-1) | 1.668 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@program-1.service.aecp.last.if0` (backlog-adp@program-1) | 3.253 | fits | 15 aecp | 10 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@program-1.service.maap.first.if0` (backlog-adp@program-1) | 3.252 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-1.service.maap.last.if0` (backlog-adp@program-1) | 4.218 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-1.service.srp.first.if0` (backlog-adp@program-1) | 5.059 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-1.service.srp.last.if0` (backlog-adp@blank-aged2-1) | 10.867 | fits | 31 srp | 10 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-3 | 0 | 11.583 | 12 | 146,248 (1.462) | yes | - |
| backlog-adp@program-1 | 0 | 11.491 | 12 | 153,025 (1.530) | yes | - |
| backlog-adp@verify-1 | 0 | 11.274 | 11 | 152,836 (1.528) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.397 | 12 | 152,676 (1.527) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.017 | 13 | 152,191 (1.522) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.240 | 10 | 149,423 (1.494) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.394 | 12 | 152,327 (1.523) | yes | - |
| backlog-adp@verify-aged2-1 | 1 | 11.192 | 10 | 149,287 (1.493) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.229 | 11 | 152,485 (1.525) | yes | - |
| backlog-adp | 0 | 10.404 | 11 | 152,638 (1.526) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill, backlog-owed not run): 152,638 CPU cycles (1.526 ms), backlog-adp.
Over the windows that released their whole load only: 152,638 (1.526 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-3 | 418 | 0 | 149,185 (1.492) | fits |
| backlog-adp@program-1 | 520 | 0 | 153,025 (1.530) | fits |
| backlog-adp@verify-1 | 614 | 0 | 152,836 (1.528) | fits |
| backlog-adp@blank-aged2-1 | 704 | 0 | 152,676 (1.527) | fits |
| backlog-adp@blank-aged1-1 | 649 | 0 | 152,191 (1.522) | fits |
| backlog-adp@program-aged2-1 | 803 | 0 | 152,316 (1.523) | fits |
| backlog-adp@program-aged1-1 | 746 | 0 | 152,327 (1.523) | fits |
| backlog-adp@verify-aged2-1 | 900 | 0 | 152,485 (1.525) | fits |
| backlog-adp@verify-aged1-1 | 842 | 0 | 152,485 (1.525) | fits |
| save-held | 1472 | 0 | 157,878 (1.579) | fits |
| backlog-adp | 315 | 0 | 152,638 (1.526) | fits |
| acmp-cmd | 87 | 0 | 40,360 (0.404) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-1 | 2 | none | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 10.867 (20) | 9.133 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.374 (20) | 9.626 |
| backlog-adp@program-aged2-1 | 2 | +9.082 ms, 80,791 (0.808 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 10.708 (20) | 9.292 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.935 (20) | 10.065 |
| backlog-adp@verify-aged2-1 | 2 | +9.067 ms, 77,494 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 10.659 (20) | 9.341 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.931 (20) | 10.069 |

Least margin over the aged windows: 9.133 ms, `backlog-adp@blank-aged2-1.service.srp.last.if0` at 10.867 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 2019.481 | 4,070 | 102 | - | 15.422 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-3 | 299 | 93,276 (0.933) | 76,156 (0.762) |
| backlog-adp@program-1 | 328 | 98,762 (0.988) | 78,969 (0.790) |
| backlog-adp@verify-1 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@blank-aged2-1 | 297 | 86,104 (0.861) | 76,128 (0.761) |
| backlog-adp@blank-aged1-1 | 297 | 97,547 (0.975) | 76,224 (0.762) |
| backlog-adp@program-aged2-1 | 326 | 96,381 (0.964) | 78,703 (0.787) |
| backlog-adp@program-aged1-1 | 326 | 98,398 (0.984) | 78,969 (0.790) |
| backlog-adp@verify-aged2-1 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-aged1-1 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| save-held | 722 | 96,000 (0.960) | 78,497 (0.785) |
| backlog-adp | 271 | 22,268 (0.223) | 2,344 (0.023) |
| acmp-cmd | 65 | 22,142 (0.221) | 2,242 (0.022) |

Longest pass that carries a step: 98,762 CPU cycles (0.988 ms), backlog-adp@program-1; longest step: 78,969 (0.790 ms), backlog-adp@program-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 354,196 | 3.542 | 20 | 20 | fits | 106,122 | 180 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 289,439 | 2.894 | 20 | 200 | fits | 146,248 | 255 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 403,419 | 4.034 | 20 | 200 | fits | 106,122 | 180 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 290,363 | 2.904 | 20 | 20 | fits | 146,248 | 255 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 404,123 | 4.041 | 20 | 20 | fits | 106,122 | 180 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 147,755 | 1.478 | 20 | 24 | fits | 149,185 | 114 | 0.384 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 293,013 | 2.930 | 20 | 24 | fits | 146,248 | 255 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 292,947 | 2.929 | 20 | 50 | fits | 146,248 | 255 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 407,147 | 4.071 | 20 | 50 | fits | 106,122 | 180 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 491,260 | 4.913 | 20 | 20 | fits | 84,179 | 24 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 982,998 | 9.830 | 20 | 20 | fits | 72,841 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 369,481 | 3.695 | 20 | 20 | fits | 97,037 | 154 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 321,701 | 3.217 | 20 | 200 | fits | 151,401 | 238 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 418,122 | 4.181 | 20 | 200 | fits | 97,037 | 154 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 322,625 | 3.226 | 20 | 20 | fits | 151,401 | 238 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 418,826 | 4.188 | 20 | 20 | fits | 97,037 | 154 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 166,840 | 1.668 | 20 | 24 | fits | 153,025 | 156 | 0.396 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 325,275 | 3.253 | 20 | 24 | fits | 151,401 | 238 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 325,209 | 3.252 | 20 | 50 | fits | 151,401 | 238 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 421,850 | 4.218 | 20 | 50 | fits | 97,037 | 154 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 505,883 | 5.059 | 20 | 20 | fits | 84,099 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,002,804 | 10.028 | 20 | 20 | fits | 77,201 | 31 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 353,114 | 3.531 | 20 | 20 | fits | 97,069 | 154 | 0.417 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 305,307 | 3.053 | 20 | 200 | fits | 149,262 | 233 | 0.393 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 401,760 | 4.018 | 20 | 200 | fits | 97,069 | 154 | 0.417 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 306,231 | 3.062 | 20 | 20 | fits | 149,262 | 233 | 0.393 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 402,464 | 4.025 | 20 | 20 | fits | 97,069 | 154 | 0.417 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 160,609 | 1.606 | 20 | 24 | fits | 152,836 | 155 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 308,881 | 3.089 | 20 | 24 | fits | 149,262 | 233 | 0.393 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 308,815 | 3.088 | 20 | 50 | fits | 149,262 | 233 | 0.393 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 405,488 | 4.055 | 20 | 50 | fits | 97,069 | 154 | 0.417 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 489,678 | 4.897 | 20 | 20 | fits | 84,256 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 997,674 | 9.977 | 20 | 20 | fits | 85,260 | 28 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 359,597 | 3.596 | 20 | 20 | fits | 98,622 | 142 | 0.411 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 317,365 | 3.174 | 20 | 200 | fits | 149,996 | 253 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 415,371 | 4.154 | 20 | 200 | fits | 98,622 | 142 | 0.411 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 318,289 | 3.183 | 20 | 20 | fits | 149,996 | 253 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 416,075 | 4.161 | 20 | 20 | fits | 98,622 | 142 | 0.411 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 163,068 | 1.631 | 20 | 24 | fits | 152,676 | 153 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 320,939 | 3.209 | 20 | 24 | fits | 149,996 | 253 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 320,873 | 3.209 | 20 | 50 | fits | 149,996 | 253 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 419,099 | 4.191 | 20 | 50 | fits | 98,622 | 142 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 502,769 | 5.028 | 20 | 20 | fits | 83,736 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,086,687 | 10.867 | 20 | 20 | fits | 78,006 | 31 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 346,883 | 3.469 | 20 | 20 | fits | 101,071 | 158 | 0.456 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 308,420 | 3.084 | 20 | 200 | fits | 150,807 | 237 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 408,875 | 4.089 | 20 | 200 | fits | 101,071 | 158 | 0.456 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 309,344 | 3.093 | 20 | 20 | fits | 150,807 | 237 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 409,579 | 4.096 | 20 | 20 | fits | 101,071 | 158 | 0.456 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 162,177 | 1.622 | 20 | 24 | fits | 152,191 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 311,994 | 3.120 | 20 | 24 | fits | 150,807 | 237 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 311,928 | 3.119 | 20 | 50 | fits | 150,807 | 237 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 412,603 | 4.126 | 20 | 50 | fits | 101,071 | 158 | 0.456 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 505,662 | 5.057 | 20 | 20 | fits | 84,264 | 25 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,037,432 | 10.374 | 20 | 20 | fits | 75,365 | 25 | 0.717 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 337,875 | 3.379 | 20 | 20 | fits | 100,328 | 142 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 294,748 | 2.947 | 20 | 200 | fits | 149,423 | 253 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 394,460 | 3.945 | 20 | 200 | fits | 100,328 | 142 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 295,672 | 2.957 | 20 | 20 | fits | 149,423 | 253 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 395,164 | 3.952 | 20 | 20 | fits | 100,328 | 142 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 149,889 | 1.499 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 298,322 | 2.983 | 20 | 24 | fits | 149,423 | 253 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 298,256 | 2.983 | 20 | 50 | fits | 149,423 | 253 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 398,188 | 3.982 | 20 | 50 | fits | 100,328 | 142 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 482,179 | 4.822 | 20 | 20 | fits | 84,057 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,070,845 | 10.708 | 20 | 20 | fits | 85,631 | 29 | 0.625 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 353,197 | 3.532 | 20 | 20 | fits | 99,062 | 142 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 310,821 | 3.108 | 20 | 200 | fits | 150,232 | 253 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 409,267 | 4.093 | 20 | 200 | fits | 99,062 | 142 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 311,745 | 3.117 | 20 | 20 | fits | 150,232 | 253 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 409,971 | 4.100 | 20 | 20 | fits | 99,062 | 142 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 157,216 | 1.572 | 20 | 24 | fits | 152,327 | 153 | 0.389 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 314,395 | 3.144 | 20 | 24 | fits | 150,232 | 253 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 314,329 | 3.143 | 20 | 50 | fits | 150,232 | 253 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 412,995 | 4.130 | 20 | 50 | fits | 99,062 | 142 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 496,883 | 4.969 | 20 | 20 | fits | 83,954 | 24 | 0.783 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 993,507 | 9.935 | 20 | 20 | fits | 77,174 | 31 | 0.686 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 337,530 | 3.375 | 20 | 20 | fits | 99,222 | 142 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 295,008 | 2.950 | 20 | 200 | fits | 149,287 | 253 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 393,614 | 3.936 | 20 | 200 | fits | 99,222 | 142 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 295,932 | 2.959 | 20 | 20 | fits | 149,287 | 253 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 394,318 | 3.943 | 20 | 20 | fits | 99,222 | 142 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 150,285 | 1.503 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 298,582 | 2.986 | 20 | 24 | fits | 149,287 | 253 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 298,516 | 2.985 | 20 | 50 | fits | 149,287 | 253 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 397,342 | 3.973 | 20 | 50 | fits | 99,222 | 142 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 481,460 | 4.815 | 20 | 20 | fits | 84,184 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,065,933 | 10.659 | 20 | 20 | fits | 85,511 | 29 | 0.619 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 347,607 | 3.476 | 20 | 20 | fits | 96,490 | 151 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 301,611 | 3.016 | 20 | 200 | fits | 150,515 | 237 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 397,485 | 3.975 | 20 | 200 | fits | 96,490 | 151 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 302,535 | 3.025 | 20 | 20 | fits | 150,515 | 237 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 398,189 | 3.982 | 20 | 20 | fits | 96,490 | 151 | 0.426 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 155,660 | 1.557 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 305,185 | 3.052 | 20 | 24 | fits | 150,515 | 237 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 305,119 | 3.051 | 20 | 50 | fits | 150,515 | 237 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 401,213 | 4.012 | 20 | 50 | fits | 96,490 | 151 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 485,514 | 4.855 | 20 | 20 | fits | 84,367 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 993,121 | 9.931 | 20 | 20 | fits | 85,276 | 28 | 0.615 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 156,938 | 1.569 | 20 | 200 | fits | 157,878 | 259 | 0.445 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 225,071 | 2.251 | 20 | 20 | fits | 88,270 | 77 | 0.680 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 295,574 | 2.956 | 20 | 24 | fits | 80,843 | 49 | 0.560 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 185,596 | 1.856 | 20 | 50 | fits | 88,270 | 77 | 0.680 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 902,727 | 9.027 | 20 | 20 | fits | 79,127 | 30 | 0.704 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 225,861 | 2.259 | 49 | 49 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 356,790 | 3.568 | 20 | 20 | fits | 100,384 | 158 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 298,765 | 2.988 | 20 | 200 | fits | 150,877 | 238 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 407,210 | 4.072 | 20 | 200 | fits | 100,384 | 158 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 299,689 | 2.997 | 20 | 20 | fits | 150,877 | 238 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 407,914 | 4.079 | 20 | 20 | fits | 100,384 | 158 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 152,452 | 1.525 | 20 | 24 | fits | 152,638 | 155 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 302,339 | 3.023 | 20 | 24 | fits | 150,877 | 238 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 302,273 | 3.023 | 20 | 50 | fits | 150,877 | 238 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 410,938 | 4.109 | 20 | 50 | fits | 100,384 | 158 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 494,394 | 4.944 | 20 | 20 | fits | 83,522 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 985,488 | 9.855 | 20 | 20 | fits | 72,762 | 24 | 0.653 |
| BIND_RX | `acmp.bind_rx.if0` | 18,557 | 0.186 | 20 | 20 | fits | 40,360 | 26 (77) | 0.790 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,231 | 0.092 | 20 | 20 | fits | 32,173 | 19 (32) | 0.835 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,095 | 0.101 | 20 | 20 | fits | 25,746 | 15 (47) | 0.778 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,073 | 0.131 | 20 | 20 | fits | 39,079 | 18 (50) | 0.836 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 9,904 | 0.099 | 20 | 20 | fits | 25,519 | 17 (48) | 0.753 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,752 | 0.098 | 20 | 20 | fits | 24,586 | 16 (48) | 0.732 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,597 | 0.086 | 20 | 20 | fits | 23,888 | 16 (48) | 0.730 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,425 | 0.094 | 20 | 20 | fits | 24,673 | 16 (48) | 0.753 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

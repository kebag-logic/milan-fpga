### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 253 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged2-7.adp_available.if0` (backlog-adp@blank-aged2-7) | 4.351 (5.113) | fits | 7 adp | 23 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.acmp.first.if0` (backlog-adp@verify-5) | 3.047 | fits | 0 acmp | 23 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.acmp.last.if0` (backlog-adp@blank-aged2-7) | 5.015 | fits | 11 acmp | 23 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.adp.first.if0` (backlog-adp@verify-5) | 3.038 | fits | 0 adp | 23 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.adp.last.if0` (backlog-adp@blank-aged2-7) | 5.008 | fits | 7 adp | 23 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-3.service.aecp.first.if0` (backlog-adp@verify-3) | 1.596 | fits | 0 aecp | 23 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@verify-5.service.aecp.last.if0` (backlog-adp@verify-5) | 3.073 | fits | 15 aecp | 23 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.maap.first.if0` (backlog-adp@verify-5) | 3.073 | fits | 0 maap | 23 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.maap.last.if0` (backlog-adp@blank-aged2-7) | 5.045 | fits | 6 maap | 23 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-7.service.srp.first.if0` (backlog-adp@blank-aged2-7) | 5.945 | fits | 0 srp | 23 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-7.service.srp.last.if0` (backlog-adp@blank-aged1-7) | 9.937 | fits | 31 srp | 23 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-1 | 0 | 10.301 | 10 | 148,179 (1.482) | yes | - |
| backlog-adp@blank-3 | 0 | 10.259 | 10 | 148,236 (1.482) | yes | - |
| backlog-adp@blank-5 | 0 | 10.614 | 12 | 148,343 (1.483) | yes | - |
| backlog-adp@blank-7 | 0 | 10.319 | 10 | 148,206 (1.482) | yes | - |
| backlog-adp@program-1 | 0 | 10.305 | 10 | 148,335 (1.483) | yes | - |
| backlog-adp@program-3 | 0 | 10.380 | 10 | 148,251 (1.483) | yes | - |
| backlog-adp@program-5 | 0 | 10.056 | 12 | 148,395 (1.484) | yes | - |
| backlog-adp@program-7 | 0 | 9.579 | 10 | 148,267 (1.483) | yes | - |
| backlog-adp@verify-1 | 0 | 10.240 | 9 | 143,936 (1.439) | yes | - |
| backlog-adp@verify-3 | 0 | 10.337 | 10 | 148,136 (1.481) | yes | - |
| backlog-adp@verify-5 | 0 | 10.567 | 12 | 148,213 (1.482) | yes | - |
| backlog-adp@verify-7 | 0 | 10.255 | 10 | 148,251 (1.483) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.835 | 12 | 148,204 (1.482) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.261 | 10 | 147,664 (1.477) | yes | - |
| backlog-adp@blank-aged2-5 | 1 | 10.230 | 9 | 145,339 (1.453) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.315 | 10 | 147,567 (1.476) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.137 | 12 | 147,698 (1.477) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.502 | 14 | 147,698 (1.477) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.066 | 11 | 148,255 (1.483) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.271 | 12 | 149,376 (1.494) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.572 | 12 | 147,887 (1.479) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.284 | 10 | 147,844 (1.478) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 10.218 | 9 | 145,167 (1.452) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 49838 | 0 | 49,465 (0.495) | fits |
| backlog-adp@blank-1 | 405 | 0 | 148,179 (1.482) | fits |
| backlog-adp@blank-3 | 405 | 0 | 148,236 (1.482) | fits |
| backlog-adp@blank-5 | 407 | 0 | 148,343 (1.483) | fits |
| backlog-adp@blank-7 | 407 | 0 | 148,206 (1.482) | fits |
| backlog-adp@program-1 | 501 | 0 | 148,335 (1.483) | fits |
| backlog-adp@program-3 | 503 | 0 | 148,251 (1.483) | fits |
| backlog-adp@program-5 | 506 | 0 | 148,395 (1.484) | fits |
| backlog-adp@program-7 | 506 | 0 | 148,267 (1.483) | fits |
| backlog-adp@verify-1 | 589 | 0 | 148,136 (1.481) | fits |
| backlog-adp@verify-3 | 589 | 0 | 148,136 (1.481) | fits |
| backlog-adp@verify-5 | 591 | 0 | 148,213 (1.482) | fits |
| backlog-adp@verify-7 | 591 | 0 | 148,251 (1.483) | fits |
| backlog-adp@blank-aged2-1 | 727 | 0 | 148,204 (1.482) | fits |
| backlog-adp@blank-aged2-3 | 741 | 0 | 147,664 (1.477) | fits |
| backlog-adp@blank-aged2-5 | 757 | 0 | 147,510 (1.475) | fits |
| backlog-adp@blank-aged2-7 | 774 | 0 | 147,567 (1.476) | fits |
| backlog-adp@blank-aged1-1 | 666 | 0 | 147,698 (1.477) | fits |
| backlog-adp@blank-aged1-3 | 684 | 0 | 147,698 (1.477) | fits |
| backlog-adp@blank-aged1-5 | 698 | 0 | 148,255 (1.483) | fits |
| backlog-adp@blank-aged1-7 | 715 | 0 | 149,376 (1.494) | fits |
| backlog-adp@program-aged2-1 | 821 | 0 | 147,887 (1.479) | fits |
| backlog-adp@program-aged2-3 | 835 | 0 | 147,844 (1.478) | fits |
| backlog-adp@program-aged2-5 | 851 | 0 | 147,844 (1.478) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-1 | 2 | none | +9.080 ms, 76,572 (0.766 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.042 (20) | 10.958 |
| backlog-adp@blank-aged2-3 | 2 | +6.677 ms, 76,572 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.769 (20) | 10.231 |
| backlog-adp@blank-aged2-5 | 2 | +4.848 ms, 76,843 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 9.740 (20) | 10.260 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.819 (20) | 10.181 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.128 (20) | 10.872 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 9.815 (20) | 10.185 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.819 (20) | 10.181 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 9.937 (20) | 10.063 |
| backlog-adp@program-aged2-1 | 2 | none | +9.014 ms, 80,246 (0.802 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.976 (20) | 11.024 |
| backlog-adp@program-aged2-3 | 2 | +6.693 ms, 80,312 (0.803 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.789 (20) | 10.211 |
| backlog-adp@program-aged2-5 | 2 | +4.945 ms, 80,555 (0.806 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.723 (20) | 10.277 |

Least margin over the aged windows: 10.063 ms, `backlog-adp@blank-aged1-7.service.srp.last.if0` at 9.937 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.326 | 6,070 | 102 | 2 | 30.788 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 520 | 79,640 (0.796) | 77,551 (0.776) |
| backlog-adp@blank-1 | 299 | 91,495 (0.915) | 76,194 (0.762) |
| backlog-adp@blank-3 | 299 | 91,550 (0.915) | 76,106 (0.761) |
| backlog-adp@blank-5 | 299 | 91,707 (0.917) | 76,337 (0.763) |
| backlog-adp@blank-7 | 299 | 91,273 (0.913) | 76,209 (0.762) |
| backlog-adp@program-1 | 328 | 95,695 (0.957) | 78,828 (0.788) |
| backlog-adp@program-3 | 328 | 95,454 (0.955) | 78,891 (0.789) |
| backlog-adp@program-5 | 329 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@program-7 | 329 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-1 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-3 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-5 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@verify-7 | 355 | 95,454 (0.955) | 78,128 (0.781) |
| backlog-adp@blank-aged2-1 | 297 | 76,572 (0.766) | 75,648 (0.756) |
| backlog-adp@blank-aged2-3 | 297 | 76,572 (0.766) | 75,648 (0.756) |
| backlog-adp@blank-aged2-5 | 297 | 76,843 (0.768) | 75,836 (0.758) |
| backlog-adp@blank-aged2-7 | 297 | 84,127 (0.841) | 75,493 (0.755) |
| backlog-adp@blank-aged1-1 | 297 | 97,157 (0.972) | 76,199 (0.762) |
| backlog-adp@blank-aged1-3 | 297 | 91,724 (0.917) | 76,251 (0.763) |
| backlog-adp@blank-aged1-5 | 297 | 91,274 (0.913) | 76,210 (0.762) |
| backlog-adp@blank-aged1-7 | 298 | 91,317 (0.913) | 76,302 (0.763) |
| backlog-adp@program-aged2-1 | 326 | 95,454 (0.955) | 78,343 (0.783) |
| backlog-adp@program-aged2-3 | 326 | 95,454 (0.955) | 78,349 (0.783) |
| backlog-adp@program-aged2-5 | 326 | 95,454 (0.955) | 78,464 (0.785) |

Longest pass that carries a step: 97,157 CPU cycles (0.972 ms), backlog-adp@blank-aged1-1; longest step: 78,891 (0.789 ms), backlog-adp@program-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 343,300 | 3.433 | 20 | 20 | fits | 108,473 | 163 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 292,826 | 2.928 | 20 | 200 | fits | 143,171 | 226 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 400,683 | 4.007 | 20 | 200 | fits | 108,473 | 163 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 293,750 | 2.938 | 20 | 20 | fits | 143,171 | 226 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 401,387 | 4.014 | 20 | 20 | fits | 108,473 | 163 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 154,219 | 1.542 | 20 | 24 | fits | 148,179 | 155 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 296,400 | 2.964 | 20 | 24 | fits | 143,171 | 226 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 296,334 | 2.963 | 20 | 50 | fits | 143,171 | 226 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 404,411 | 4.044 | 20 | 50 | fits | 108,473 | 163 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 494,658 | 4.947 | 20 | 20 | fits | 90,313 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 905,084 | 9.051 | 20 | 20 | fits | 59,155 | 26 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 341,457 | 3.415 | 20 | 20 | fits | 109,178 | 164 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 291,348 | 2.913 | 20 | 200 | fits | 144,014 | 226 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 399,910 | 3.999 | 20 | 200 | fits | 109,178 | 164 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 292,272 | 2.923 | 20 | 20 | fits | 144,014 | 226 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 400,614 | 4.006 | 20 | 20 | fits | 109,178 | 164 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 151,898 | 1.519 | 20 | 24 | fits | 148,236 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 294,922 | 2.949 | 20 | 24 | fits | 144,014 | 226 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 294,856 | 2.949 | 20 | 50 | fits | 144,014 | 226 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 403,638 | 4.036 | 20 | 50 | fits | 109,178 | 164 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 494,898 | 4.949 | 20 | 20 | fits | 82,893 | 31 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 900,857 | 9.009 | 20 | 20 | fits | 63,259 | 24 | 0.593 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 355,547 | 3.555 | 20 | 20 | fits | 109,565 | 166 | 0.433 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 296,332 | 2.963 | 20 | 200 | fits | 143,810 | 227 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 405,281 | 4.053 | 20 | 200 | fits | 109,565 | 166 | 0.433 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 297,256 | 2.973 | 20 | 20 | fits | 143,810 | 227 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 405,985 | 4.060 | 20 | 20 | fits | 109,565 | 166 | 0.433 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 149,627 | 1.496 | 20 | 24 | fits | 148,343 | 156 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 299,906 | 2.999 | 20 | 24 | fits | 143,810 | 227 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 299,840 | 2.998 | 20 | 50 | fits | 143,810 | 227 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 409,009 | 4.090 | 20 | 50 | fits | 109,565 | 166 | 0.433 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 494,950 | 4.949 | 20 | 20 | fits | 86,007 | 30 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 893,277 | 8.933 | 20 | 20 | fits | 63,195 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 344,096 | 3.441 | 20 | 20 | fits | 116,722 | 172 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 293,950 | 2.939 | 20 | 200 | fits | 143,903 | 224 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 410,056 | 4.101 | 20 | 200 | fits | 116,722 | 172 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 294,874 | 2.949 | 20 | 20 | fits | 143,903 | 224 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 410,760 | 4.108 | 20 | 20 | fits | 116,722 | 172 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 154,611 | 1.546 | 20 | 24 | fits | 148,206 | 155 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 297,524 | 2.975 | 20 | 24 | fits | 143,903 | 224 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 297,458 | 2.975 | 20 | 50 | fits | 143,903 | 224 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 413,784 | 4.138 | 20 | 50 | fits | 116,722 | 172 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 503,699 | 5.037 | 20 | 20 | fits | 89,981 | 28 | 0.719 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 907,065 | 9.071 | 20 | 20 | fits | 52,922 | 20 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 359,298 | 3.593 | 20 | 20 | fits | 112,740 | 170 | 0.465 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 289,927 | 2.899 | 20 | 200 | fits | 143,987 | 227 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 410,613 | 4.106 | 20 | 200 | fits | 112,740 | 170 | 0.465 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 290,851 | 2.909 | 20 | 20 | fits | 143,987 | 227 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 411,317 | 4.113 | 20 | 20 | fits | 112,740 | 170 | 0.465 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 150,504 | 1.505 | 20 | 24 | fits | 148,335 | 155 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 293,501 | 2.935 | 20 | 24 | fits | 143,987 | 227 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 293,435 | 2.934 | 20 | 50 | fits | 143,987 | 227 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 414,341 | 4.143 | 20 | 50 | fits | 112,740 | 170 | 0.465 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 504,531 | 5.045 | 20 | 20 | fits | 90,256 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 899,760 | 8.998 | 20 | 20 | fits | 52,585 | 20 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 346,429 | 3.464 | 20 | 20 | fits | 114,957 | 184 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 296,512 | 2.965 | 20 | 200 | fits | 145,277 | 209 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 410,853 | 4.109 | 20 | 200 | fits | 114,957 | 184 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 297,436 | 2.974 | 20 | 20 | fits | 145,277 | 209 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 411,557 | 4.116 | 20 | 20 | fits | 114,957 | 184 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 155,799 | 1.558 | 20 | 24 | fits | 148,251 | 155 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 300,086 | 3.001 | 20 | 24 | fits | 145,277 | 209 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 300,020 | 3.000 | 20 | 50 | fits | 145,277 | 209 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 414,581 | 4.146 | 20 | 50 | fits | 114,957 | 184 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 504,123 | 5.041 | 20 | 20 | fits | 89,608 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 907,761 | 9.078 | 20 | 20 | fits | 52,505 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 347,322 | 3.473 | 20 | 20 | fits | 108,664 | 163 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 296,729 | 2.967 | 20 | 200 | fits | 144,206 | 231 | 0.386 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 404,777 | 4.048 | 20 | 200 | fits | 108,664 | 163 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 297,653 | 2.977 | 20 | 20 | fits | 144,206 | 231 | 0.386 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 405,481 | 4.055 | 20 | 20 | fits | 108,664 | 163 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 149,780 | 1.498 | 20 | 24 | fits | 148,395 | 156 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 300,303 | 3.003 | 20 | 24 | fits | 144,206 | 231 | 0.386 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 300,237 | 3.002 | 20 | 50 | fits | 144,206 | 231 | 0.386 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 408,505 | 4.085 | 20 | 50 | fits | 108,664 | 163 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 498,063 | 4.981 | 20 | 20 | fits | 89,624 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 892,957 | 8.930 | 20 | 20 | fits | 52,569 | 20 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 359,430 | 3.594 | 20 | 20 | fits | 115,444 | 188 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 294,595 | 2.946 | 20 | 200 | fits | 144,203 | 205 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 409,423 | 4.094 | 20 | 200 | fits | 115,444 | 188 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 295,519 | 2.955 | 20 | 20 | fits | 144,203 | 205 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 410,127 | 4.101 | 20 | 20 | fits | 115,444 | 188 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 154,956 | 1.550 | 20 | 24 | fits | 148,267 | 155 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 298,169 | 2.982 | 20 | 24 | fits | 144,203 | 205 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 298,103 | 2.981 | 20 | 50 | fits | 144,203 | 205 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 413,151 | 4.132 | 20 | 50 | fits | 115,444 | 188 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 514,679 | 5.147 | 20 | 20 | fits | 93,095 | 35 | 0.727 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 902,852 | 9.029 | 20 | 20 | fits | 52,491 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 336,758 | 3.368 | 20 | 20 | fits | 108,236 | 163 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 286,744 | 2.867 | 20 | 200 | fits | 143,936 | 226 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 394,364 | 3.944 | 20 | 200 | fits | 108,236 | 163 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 287,668 | 2.877 | 20 | 20 | fits | 143,936 | 226 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 395,068 | 3.951 | 20 | 20 | fits | 108,236 | 163 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 147,372 | 1.474 | 20 | 24 | fits | 148,136 | 155 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 290,318 | 2.903 | 20 | 24 | fits | 143,936 | 226 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 290,252 | 2.903 | 20 | 50 | fits | 143,936 | 226 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 398,092 | 3.981 | 20 | 50 | fits | 108,236 | 163 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 487,970 | 4.880 | 20 | 20 | fits | 89,944 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 898,590 | 8.986 | 20 | 20 | fits | 59,155 | 26 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 348,819 | 3.488 | 20 | 20 | fits | 109,050 | 164 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 298,874 | 2.989 | 20 | 200 | fits | 143,878 | 226 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 407,308 | 4.073 | 20 | 200 | fits | 109,050 | 164 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 299,798 | 2.998 | 20 | 20 | fits | 143,878 | 226 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 408,012 | 4.080 | 20 | 20 | fits | 109,050 | 164 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 159,560 | 1.596 | 20 | 24 | fits | 148,136 | 155 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 302,448 | 3.024 | 20 | 24 | fits | 143,878 | 226 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 302,382 | 3.024 | 20 | 50 | fits | 143,878 | 226 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 411,036 | 4.110 | 20 | 50 | fits | 109,050 | 164 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 502,084 | 5.021 | 20 | 20 | fits | 82,682 | 31 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 908,174 | 9.082 | 20 | 20 | fits | 63,181 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 371,499 | 3.715 | 20 | 20 | fits | 118,216 | 172 | 0.462 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 303,773 | 3.038 | 20 | 200 | fits | 143,619 | 227 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 421,373 | 4.214 | 20 | 200 | fits | 118,216 | 172 | 0.462 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 304,697 | 3.047 | 20 | 20 | fits | 143,619 | 227 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 422,077 | 4.221 | 20 | 20 | fits | 118,216 | 172 | 0.462 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 157,259 | 1.573 | 20 | 24 | fits | 148,213 | 156 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 307,347 | 3.073 | 20 | 24 | fits | 143,619 | 227 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 307,281 | 3.073 | 20 | 50 | fits | 143,619 | 227 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 425,101 | 4.251 | 20 | 50 | fits | 118,216 | 172 | 0.462 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 515,401 | 5.154 | 20 | 20 | fits | 90,366 | 28 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 903,300 | 9.033 | 20 | 20 | fits | 52,684 | 21 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 337,432 | 3.374 | 20 | 20 | fits | 116,054 | 172 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 287,212 | 2.872 | 20 | 200 | fits | 143,500 | 224 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 402,650 | 4.027 | 20 | 200 | fits | 116,054 | 172 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 288,136 | 2.881 | 20 | 20 | fits | 143,500 | 224 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 403,354 | 4.034 | 20 | 20 | fits | 116,054 | 172 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 148,276 | 1.483 | 20 | 24 | fits | 148,251 | 155 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 290,786 | 2.908 | 20 | 24 | fits | 143,500 | 224 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 290,720 | 2.907 | 20 | 50 | fits | 143,500 | 224 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 406,378 | 4.064 | 20 | 50 | fits | 116,054 | 172 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 496,283 | 4.963 | 20 | 20 | fits | 89,971 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 900,190 | 9.002 | 20 | 20 | fits | 52,583 | 20 | 0.650 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 357,109 | 3.571 | 20 | 20 | fits | 112,609 | 170 | 0.466 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 294,523 | 2.945 | 20 | 200 | fits | 144,219 | 227 | 0.399 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 415,837 | 4.158 | 20 | 200 | fits | 112,609 | 170 | 0.466 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 295,447 | 2.954 | 20 | 20 | fits | 144,219 | 227 | 0.399 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 416,541 | 4.165 | 20 | 20 | fits | 112,609 | 170 | 0.466 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 154,868 | 1.549 | 20 | 24 | fits | 148,204 | 152 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 298,097 | 2.981 | 20 | 24 | fits | 144,219 | 227 | 0.399 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 298,031 | 2.980 | 20 | 50 | fits | 144,219 | 227 | 0.399 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 419,565 | 4.196 | 20 | 50 | fits | 112,609 | 170 | 0.466 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 509,742 | 5.097 | 20 | 20 | fits | 90,243 | 28 | 0.726 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 904,241 | 9.042 | 20 | 20 | fits | 59,531 | 26 | 0.696 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 339,339 | 3.393 | 20 | 20 | fits | 108,579 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 289,410 | 2.894 | 20 | 200 | fits | 143,929 | 226 | 0.398 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 397,373 | 3.974 | 20 | 200 | fits | 108,579 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 290,334 | 2.903 | 20 | 20 | fits | 143,929 | 226 | 0.398 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 398,077 | 3.981 | 20 | 20 | fits | 108,579 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 150,045 | 1.500 | 20 | 24 | fits | 147,664 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 292,984 | 2.930 | 20 | 24 | fits | 143,929 | 226 | 0.398 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 292,918 | 2.929 | 20 | 50 | fits | 143,929 | 226 | 0.398 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 401,101 | 4.011 | 20 | 50 | fits | 108,579 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 490,518 | 4.905 | 20 | 20 | fits | 89,483 | 28 | 0.715 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 976,947 | 9.769 | 20 | 20 | fits | 52,979 | 20 | 0.665 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 343,715 | 3.437 | 20 | 20 | fits | 108,568 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 286,256 | 2.863 | 20 | 200 | fits | 145,339 | 231 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 394,208 | 3.942 | 20 | 200 | fits | 108,568 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 287,180 | 2.872 | 20 | 20 | fits | 145,339 | 231 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 394,912 | 3.949 | 20 | 20 | fits | 108,568 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 145,481 | 1.455 | 20 | 24 | fits | 147,510 | 152 | 0.334 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 289,830 | 2.898 | 20 | 24 | fits | 145,339 | 231 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 289,764 | 2.898 | 20 | 50 | fits | 145,339 | 231 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 397,936 | 3.979 | 20 | 50 | fits | 108,568 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 483,137 | 4.831 | 20 | 20 | fits | 85,267 | 30 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 974,009 | 9.740 | 20 | 20 | fits | 63,094 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 435,111 | 4.351 | 20 | 20 | fits | 120,281 | 178 | 0.459 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 296,999 | 2.970 | 20 | 200 | fits | 143,900 | 225 | 0.401 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 500,791 | 5.008 | 20 | 200 | fits | 120,281 | 178 | 0.459 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 297,923 | 2.979 | 20 | 20 | fits | 143,900 | 225 | 0.401 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 501,495 | 5.015 | 20 | 20 | fits | 120,281 | 178 | 0.459 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 157,663 | 1.577 | 20 | 24 | fits | 147,567 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 300,573 | 3.006 | 20 | 24 | fits | 143,900 | 225 | 0.401 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 300,507 | 3.005 | 20 | 50 | fits | 143,900 | 225 | 0.401 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 504,519 | 5.045 | 20 | 50 | fits | 120,281 | 178 | 0.459 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 594,457 | 5.945 | 20 | 20 | fits | 90,004 | 28 | 0.723 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 981,912 | 9.819 | 20 | 20 | fits | 52,451 | 20 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 343,077 | 3.431 | 20 | 20 | fits | 108,388 | 163 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 292,875 | 2.929 | 20 | 200 | fits | 144,012 | 226 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 400,647 | 4.006 | 20 | 200 | fits | 108,388 | 163 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 293,799 | 2.938 | 20 | 20 | fits | 144,012 | 226 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 401,351 | 4.014 | 20 | 20 | fits | 108,388 | 163 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 153,427 | 1.534 | 20 | 24 | fits | 147,698 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 296,449 | 2.964 | 20 | 24 | fits | 144,012 | 226 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 296,383 | 2.964 | 20 | 50 | fits | 144,012 | 226 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 404,375 | 4.044 | 20 | 50 | fits | 108,388 | 163 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 494,643 | 4.946 | 20 | 20 | fits | 90,334 | 29 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 912,812 | 9.128 | 20 | 20 | fits | 67,771 | 26 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 350,298 | 3.503 | 20 | 20 | fits | 109,369 | 163 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 290,809 | 2.908 | 20 | 200 | fits | 145,674 | 232 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 407,972 | 4.080 | 20 | 200 | fits | 109,369 | 163 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 291,733 | 2.917 | 20 | 20 | fits | 145,674 | 232 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 408,676 | 4.087 | 20 | 20 | fits | 109,369 | 163 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 149,699 | 1.497 | 20 | 24 | fits | 147,698 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 294,383 | 2.944 | 20 | 24 | fits | 145,674 | 232 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 294,317 | 2.943 | 20 | 50 | fits | 145,674 | 232 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 411,700 | 4.117 | 20 | 50 | fits | 109,369 | 163 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 502,010 | 5.020 | 20 | 20 | fits | 90,376 | 28 | 0.725 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 981,542 | 9.815 | 20 | 20 | fits | 63,699 | 24 | 0.615 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 335,308 | 3.353 | 20 | 20 | fits | 106,843 | 172 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 286,681 | 2.867 | 20 | 200 | fits | 148,255 | 255 | 0.385 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 392,908 | 3.929 | 20 | 200 | fits | 106,843 | 172 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 287,605 | 2.876 | 20 | 20 | fits | 148,255 | 255 | 0.385 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 393,612 | 3.936 | 20 | 20 | fits | 106,843 | 172 | 0.460 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 142,990 | 1.430 | 20 | 24 | fits | 146,863 | 120 | 0.346 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 290,255 | 2.903 | 20 | 24 | fits | 148,255 | 255 | 0.385 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 290,189 | 2.902 | 20 | 50 | fits | 148,255 | 255 | 0.385 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 396,636 | 3.966 | 20 | 50 | fits | 106,843 | 172 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 480,457 | 4.805 | 20 | 20 | fits | 83,887 | 26 | 0.812 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 981,895 | 9.819 | 20 | 20 | fits | 73,907 | 28 | 0.545 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 364,812 | 3.648 | 20 | 20 | fits | 123,762 | 196 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 300,000 | 3.000 | 20 | 200 | fits | 149,376 | 198 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 423,146 | 4.231 | 20 | 200 | fits | 123,762 | 196 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 300,924 | 3.009 | 20 | 20 | fits | 149,376 | 198 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 423,850 | 4.239 | 20 | 20 | fits | 123,762 | 196 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 155,188 | 1.552 | 20 | 24 | fits | 147,669 | 152 | 0.336 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 303,574 | 3.036 | 20 | 24 | fits | 149,376 | 198 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 303,508 | 3.035 | 20 | 50 | fits | 149,376 | 198 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 426,874 | 4.269 | 20 | 50 | fits | 123,762 | 196 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 552,715 | 5.527 | 20 | 20 | fits | 84,223 | 32 | 0.767 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 993,700 | 9.937 | 20 | 20 | fits | 63,094 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 351,462 | 3.515 | 20 | 20 | fits | 108,866 | 163 | 0.444 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 301,452 | 3.015 | 20 | 200 | fits | 145,008 | 231 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 409,702 | 4.097 | 20 | 200 | fits | 108,866 | 163 | 0.444 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 302,376 | 3.024 | 20 | 20 | fits | 145,008 | 231 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 410,406 | 4.104 | 20 | 20 | fits | 108,866 | 163 | 0.444 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 153,610 | 1.536 | 20 | 24 | fits | 147,887 | 153 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 305,026 | 3.050 | 20 | 24 | fits | 145,008 | 231 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 304,960 | 3.050 | 20 | 50 | fits | 145,008 | 231 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 413,430 | 4.134 | 20 | 50 | fits | 108,866 | 163 | 0.444 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 502,945 | 5.029 | 20 | 20 | fits | 89,581 | 28 | 0.716 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 897,634 | 8.976 | 20 | 20 | fits | 59,639 | 26 | 0.698 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 336,987 | 3.370 | 20 | 20 | fits | 108,789 | 163 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 287,018 | 2.870 | 20 | 200 | fits | 143,757 | 226 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 395,191 | 3.952 | 20 | 200 | fits | 108,789 | 163 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 287,942 | 2.879 | 20 | 20 | fits | 143,757 | 226 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 395,895 | 3.959 | 20 | 20 | fits | 108,789 | 163 | 0.443 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 147,825 | 1.478 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 290,592 | 2.906 | 20 | 24 | fits | 143,757 | 226 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 290,526 | 2.905 | 20 | 50 | fits | 143,757 | 226 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 398,919 | 3.989 | 20 | 50 | fits | 108,789 | 163 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 488,529 | 4.885 | 20 | 20 | fits | 89,676 | 28 | 0.717 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 978,942 | 9.789 | 20 | 20 | fits | 63,256 | 24 | 0.593 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 342,215 | 3.422 | 20 | 20 | fits | 109,063 | 164 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 284,700 | 2.847 | 20 | 200 | fits | 145,167 | 231 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 393,147 | 3.931 | 20 | 200 | fits | 109,063 | 164 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 285,624 | 2.856 | 20 | 20 | fits | 145,167 | 231 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 393,851 | 3.939 | 20 | 20 | fits | 109,063 | 164 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 144,097 | 1.441 | 20 | 24 | fits | 147,844 | 152 | 0.335 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 288,274 | 2.883 | 20 | 24 | fits | 145,167 | 231 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 288,208 | 2.882 | 20 | 50 | fits | 145,167 | 231 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 396,875 | 3.969 | 20 | 50 | fits | 109,063 | 164 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 492,752 | 4.928 | 20 | 20 | fits | 87,387 | 37 | 0.755 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 972,306 | 9.723 | 20 | 20 | fits | 63,181 | 24 | 0.591 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none

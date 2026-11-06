### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 22 paths and 6 of 587 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.328 (6.994) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 6.249 (7.484) | fits | 7 adp | 49 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.085 (0.408) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.404 (2.365) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.559 (63.934) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.447 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 6.985 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.337 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 9.665 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 4.732 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 13.590 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.766 | fits | 0 acmp | 52 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@verify-aged2-7.service.acmp.last.if0` (backlog-adp@verify-aged2-7) | 9.188 | fits | 11 acmp | 52 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.756 | fits | 0 adp | 52 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 7.398 | fits | 7 adp | 50 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.685 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.801 | fits | 0 aecp | 52 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.784 | MISS ceiling | 15 aecp | 52 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.791 | fits | 0 maap | 52 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 6.085 | fits | 6 maap | 52 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.104 | fits | 0 srp | 52 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp@verify-aged2-7.service.srp.last.if1` (backlog-adp@verify-aged2-7) | 15.682 | fits | 31 srp | 52 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 16.389 | 19 | 175,960 (1.760) | yes | - |
| backlog-adp@blank-1 | 0 | 16.570 | 22 | 176,323 (1.763) | yes | - |
| backlog-adp@blank-2 | 0 | 16.301 | 22 | 170,771 (1.708) | yes | - |
| backlog-adp@blank-3 | 0 | 17.201 | 22 | 177,382 (1.774) | yes | - |
| backlog-adp@blank-4 | 0 | 16.136 | 21 | 176,015 (1.760) | yes | - |
| backlog-adp@blank-5 | 0 | 16.301 | 21 | 176,015 (1.760) | yes | - |
| backlog-adp@blank-6 | 0 | 16.161 | 21 | 146,776 (1.468) | yes | - |
| backlog-adp@blank-7 | 0 | 16.637 | 21 | 147,102 (1.471) | yes | - |
| backlog-adp@program-0 | 0 | 15.928 | 20 | 174,943 (1.749) | yes | - |
| backlog-adp@program-1 | 0 | 15.910 | 19 | 174,948 (1.749) | yes | - |
| backlog-adp@program-2 | 0 | 16.562 | 22 | 175,232 (1.752) | yes | - |
| backlog-adp@program-3 | 0 | 16.765 | 23 | 146,935 (1.469) | yes | - |
| backlog-adp@program-4 | 0 | 15.366 | 21 | 174,948 (1.749) | yes | - |
| backlog-adp@program-5 | 0 | 15.173 | 20 | 174,948 (1.749) | yes | - |
| backlog-adp@program-6 | 0 | 15.634 | 21 | 176,434 (1.764) | yes | - |
| backlog-adp@program-7 | 0 | 15.385 | 20 | 146,757 (1.468) | yes | - |
| backlog-adp@verify-0 | 0 | 16.464 | 21 | 170,758 (1.708) | yes | - |
| backlog-adp@verify-1 | 0 | 16.266 | 20 | 177,261 (1.773) | yes | - |
| backlog-adp@verify-2 | 0 | 17.720 | 21 | 175,905 (1.759) | yes | - |
| backlog-adp@verify-3 | 0 | 16.584 | 21 | 175,905 (1.759) | yes | - |
| backlog-adp@verify-4 | 0 | 16.491 | 21 | 175,905 (1.759) | yes | - |
| backlog-adp@verify-5 | 0 | 16.748 | 21 | 175,905 (1.759) | yes | - |
| backlog-adp@verify-6 | 0 | 16.717 | 21 | 150,249 (1.502) | yes | - |
| backlog-adp@verify-7 | 1 | 17.009 | 21 | 170,723 (1.707) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 16.091 | 20 | 176,158 (1.762) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 15.826 | 20 | 176,158 (1.762) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 16.118 | 22 | 175,565 (1.756) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 17.379 | 22 | 175,935 (1.759) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 17.056 | 21 | 175,880 (1.759) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 17.222 | 22 | 175,905 (1.759) | yes | - |
| backlog-adp@blank-aged2-6 | 1 | 17.113 | 21 | 150,261 (1.503) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 16.771 | 20 | 150,016 (1.500) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 15.930 | 20 | 174,838 (1.748) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 16.405 | 22 | 174,923 (1.749) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 16.431 | 22 | 162,799 (1.628) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 16.575 | 22 | 176,580 (1.766) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 16.396 | 22 | 175,112 (1.751) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 16.334 | 21 | 175,082 (1.751) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 16.325 | 22 | 146,496 (1.465) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 16.239 | 20 | 146,595 (1.466) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 15.826 | 19 | 175,827 (1.758) | yes | - |
| backlog-adp@verify-aged2-1 | 1 | 15.685 | 18 | 176,687 (1.767) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 15.885 | 20 | 175,802 (1.758) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 17.477 | 22 | 176,111 (1.761) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 17.259 | 22 | 170,824 (1.708) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 17.185 | 22 | 177,533 (1.775) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 17.204 | 22 | 146,842 (1.468) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 17.060 | 21 | 146,794 (1.468) | yes | - |
| backlog | 0 | 13.424 | 20 | 152,526 (1.525) | yes | - |
| backlog-adp | 0 | 15.566 | 21 | 150,421 (1.504) | yes | - |
| backlog-adp-refill | 0 | 40.918 | 32 | 150,421 (1.504) | yes | - |
| backlog-owed | 0 | 360.498 | 67 | 145,047 (1.450) | yes | - |

Composed maximum over the 4 backlog windows: 152,526 CPU cycles (1.525 ms), backlog.
Over the windows that released their whole load only: 152,526 (1.525 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 8678 | 0 | 157,125 (1.571) | fits |
| save-starved | 58295 | 0 | 159,562 (1.596) | fits |
| backlog-adp@blank-0 | 572 | 0 | 175,960 (1.760) | fits |
| backlog-adp@blank-1 | 576 | 0 | 176,323 (1.763) | fits |
| backlog-adp@blank-2 | 575 | 0 | 170,771 (1.708) | fits |
| backlog-adp@blank-3 | 575 | 0 | 177,382 (1.774) | fits |
| backlog-adp@blank-4 | 576 | 0 | 176,015 (1.760) | fits |
| backlog-adp@blank-5 | 576 | 0 | 176,015 (1.760) | fits |
| backlog-adp@blank-6 | 576 | 0 | 146,776 (1.468) | fits |
| backlog-adp@blank-7 | 576 | 0 | 147,102 (1.471) | fits |
| backlog-adp@program-0 | 949 | 0 | 174,943 (1.749) | fits |
| backlog-adp@program-1 | 948 | 0 | 174,948 (1.749) | fits |
| backlog-adp@program-2 | 951 | 0 | 175,232 (1.752) | fits |
| backlog-adp@program-3 | 952 | 0 | 146,935 (1.469) | fits |
| backlog-adp@program-4 | 953 | 0 | 174,948 (1.749) | fits |
| backlog-adp@program-5 | 952 | 0 | 174,948 (1.749) | fits |
| backlog-adp@program-6 | 953 | 0 | 176,434 (1.764) | fits |
| backlog-adp@program-7 | 955 | 0 | 146,757 (1.468) | fits |
| backlog-adp@verify-0 | 1313 | 0 | 170,758 (1.708) | fits |
| backlog-adp@verify-1 | 1312 | 0 | 177,261 (1.773) | fits |
| backlog-adp@verify-2 | 1315 | 0 | 175,905 (1.759) | fits |
| backlog-adp@verify-3 | 1315 | 0 | 175,905 (1.759) | fits |
| backlog-adp@verify-4 | 1315 | 0 | 175,905 (1.759) | fits |
| backlog-adp@verify-5 | 1315 | 0 | 175,905 (1.759) | fits |
| backlog-adp@verify-6 | 1315 | 0 | 150,249 (1.502) | fits |
| backlog-adp@verify-7 | 1316 | 0 | 170,723 (1.707) | fits |
| backlog-adp@blank-aged2-0 | 830 | 0 | 176,158 (1.762) | fits |
| backlog-adp@blank-aged2-1 | 836 | 0 | 176,158 (1.762) | fits |
| backlog-adp@blank-aged2-2 | 845 | 0 | 175,565 (1.756) | fits |
| backlog-adp@blank-aged2-3 | 852 | 0 | 175,935 (1.759) | fits |
| backlog-adp@blank-aged2-4 | 858 | 0 | 175,880 (1.759) | fits |
| backlog-adp@blank-aged2-5 | 866 | 0 | 175,905 (1.759) | fits |
| backlog-adp@blank-aged2-6 | 872 | 0 | 150,261 (1.503) | fits |
| backlog-adp@blank-aged2-7 | 877 | 0 | 150,016 (1.500) | fits |
| backlog-adp@program-aged2-0 | 1202 | 0 | 174,838 (1.748) | fits |
| backlog-adp@program-aged2-1 | 1211 | 0 | 174,923 (1.749) | fits |
| backlog-adp@program-aged2-2 | 1218 | 0 | 162,799 (1.628) | fits |
| backlog-adp@program-aged2-3 | 1224 | 0 | 176,580 (1.766) | fits |
| backlog-adp@program-aged2-4 | 1231 | 0 | 175,112 (1.751) | fits |
| backlog-adp@program-aged2-5 | 1237 | 0 | 175,082 (1.751) | fits |
| backlog-adp@program-aged2-6 | 1244 | 0 | 146,496 (1.465) | fits |
| backlog-adp@program-aged2-7 | 1250 | 0 | 146,595 (1.466) | fits |
| backlog-adp@verify-aged2-0 | 1725 | 0 | 175,827 (1.758) | fits |
| backlog-adp@verify-aged2-1 | 1731 | 0 | 176,687 (1.767) | fits |
| backlog-adp@verify-aged2-2 | 1739 | 0 | 175,802 (1.758) | fits |
| backlog-adp@verify-aged2-3 | 1748 | 0 | 176,111 (1.761) | fits |
| backlog-adp@verify-aged2-4 | 1755 | 0 | 170,824 (1.708) | fits |
| backlog-adp@verify-aged2-5 | 1761 | 0 | 177,533 (1.775) | fits |
| backlog-adp@verify-aged2-6 | 1768 | 0 | 146,842 (1.468) | fits |
| backlog-adp@verify-aged2-7 | 1774 | 0 | 146,794 (1.468) | fits |
| save | 628 | 0 | 124,495 (1.245) | fits |
| backlog | 311 | 0 | 152,526 (1.525) | fits |
| backlog-adp | 335 | 0 | 150,421 (1.504) | fits |
| backlog-adp-refill | 346 | 0 | 150,421 (1.504) | fits |
| backlog-owed | 370 | 0 | 145,047 (1.450) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +10.145 ms, 78,012 (0.780 ms), read-back | none | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 15.230 (18) | 2.770 |
| backlog-adp@blank-aged2-1 | 2 | +8.832 ms, 78,012 (0.780 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 15.219 (18) | 2.781 |
| backlog-adp@blank-aged2-2 | 2 | +7.999 ms, 78,037 (0.780 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 15.509 (18) | 2.491 |
| backlog-adp@blank-aged2-3 | 2 | +7.079 ms, 84,569 (0.846 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 15.286 (18) | 2.714 |
| backlog-adp@blank-aged2-4 | 2 | +6.073 ms, 84,503 (0.845 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 15.431 (18) | 2.569 |
| backlog-adp@blank-aged2-5 | 2 | +4.863 ms, 84,484 (0.845 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 15.595 (18) | 2.405 |
| backlog-adp@blank-aged2-6 | 2 | +3.262 ms, 84,693 (0.847 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 15.485 (18) | 2.515 |
| backlog-adp@blank-aged2-7 | 2 | +2.359 ms, 84,693 (0.847 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 15.398 (18) | 2.602 |
| backlog-adp@program-aged2-0 | 2 | +10.262 ms, 83,931 (0.839 ms), issue | none | `backlog-adp@program-aged2-0.service.srp.last.if1` | 15.311 (18) | 2.689 |
| backlog-adp@program-aged2-1 | 2 | +8.953 ms, 83,932 (0.839 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if1` | 15.543 (18) | 2.457 |
| backlog-adp@program-aged2-2 | 2 | +7.977 ms, 83,927 (0.839 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if1` | 15.572 (18) | 2.428 |
| backlog-adp@program-aged2-3 | 2 | +7.175 ms, 84,102 (0.841 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if1` | 15.384 (18) | 2.616 |
| backlog-adp@program-aged2-4 | 2 | +6.166 ms, 84,102 (0.841 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if1` | 15.635 (18) | 2.365 |
| backlog-adp@program-aged2-5 | 2 | +4.962 ms, 84,043 (0.840 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if1` | 15.675 (18) | 2.325 |
| backlog-adp@program-aged2-6 | 2 | +3.364 ms, 84,355 (0.844 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if1` | 15.663 (18) | 2.337 |
| backlog-adp@program-aged2-7 | 2 | +2.800 ms, 84,317 (0.843 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if1` | 15.577 (18) | 2.423 |
| backlog-adp@verify-aged2-0 | 2 | +10.082 ms, 85,173 (0.852 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 15.211 (18) | 2.789 |
| backlog-adp@verify-aged2-1 | 2 | +8.758 ms, 85,148 (0.851 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 15.070 (18) | 2.930 |
| backlog-adp@verify-aged2-2 | 2 | +7.943 ms, 85,173 (0.852 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 15.269 (18) | 2.731 |
| backlog-adp@verify-aged2-3 | 2 | +7.192 ms, 85,473 (0.855 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 15.371 (18) | 2.629 |
| backlog-adp@verify-aged2-4 | 2 | +5.865 ms, 85,324 (0.853 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 15.627 (18) | 2.373 |
| backlog-adp@verify-aged2-5 | 2 | +4.769 ms, 85,388 (0.854 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 15.553 (18) | 2.447 |
| backlog-adp@verify-aged2-6 | 2 | +3.371 ms, 85,683 (0.857 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 15.570 (18) | 2.430 |
| backlog-adp@verify-aged2-7 | 2 | +2.466 ms, 85,683 (0.857 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 15.682 (18) | 2.318 |

Least margin over the aged windows: 2.318 ms, `backlog-adp@verify-aged2-7.service.srp.last.if1` at 15.682 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4707.885 | 12,110 | 370 | - | 17.255 | no | within |
| save-starved | 12087.884 | 12,110 | 370 | - | 31.115 | yes | within |
| save | 4698.247 | 12,110 | 370 | - | 11.322 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1524 | 125,743 (1.257) | 95,873 (0.959) |
| save-starved | 686 | 97,223 (0.972) | 95,563 (0.956) |
| backlog-adp@blank-0 | 337 | 98,192 (0.982) | 75,809 (0.758) |
| backlog-adp@blank-1 | 337 | 98,067 (0.981) | 75,748 (0.757) |
| backlog-adp@blank-2 | 337 | 104,747 (1.047) | 75,814 (0.758) |
| backlog-adp@blank-3 | 338 | 104,775 (1.048) | 75,814 (0.758) |
| backlog-adp@blank-4 | 337 | 98,020 (0.980) | 75,778 (0.758) |
| backlog-adp@blank-5 | 337 | 98,126 (0.981) | 75,723 (0.757) |
| backlog-adp@blank-6 | 337 | 98,220 (0.982) | 75,748 (0.757) |
| backlog-adp@blank-7 | 337 | 98,192 (0.982) | 75,809 (0.758) |
| backlog-adp@program-0 | 443 | 121,056 (1.211) | 81,628 (0.816) |
| backlog-adp@program-1 | 443 | 121,056 (1.211) | 81,689 (0.817) |
| backlog-adp@program-2 | 443 | 121,056 (1.211) | 81,694 (0.817) |
| backlog-adp@program-3 | 443 | 121,056 (1.211) | 81,719 (0.817) |
| backlog-adp@program-4 | 444 | 121,056 (1.211) | 81,155 (0.812) |
| backlog-adp@program-5 | 444 | 121,056 (1.211) | 81,155 (0.812) |
| backlog-adp@program-6 | 444 | 121,056 (1.211) | 81,155 (0.812) |
| backlog-adp@program-7 | 444 | 121,056 (1.211) | 81,155 (0.812) |
| backlog-adp@verify-0 | 546 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-1 | 546 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-2 | 547 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-3 | 546 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-4 | 546 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-5 | 546 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-6 | 546 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-7 | 546 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@blank-aged2-0 | 335 | 78,012 (0.780) | 75,673 (0.757) |
| backlog-adp@blank-aged2-1 | 335 | 78,012 (0.780) | 75,673 (0.757) |
| backlog-adp@blank-aged2-2 | 335 | 78,037 (0.780) | 75,698 (0.757) |
| backlog-adp@blank-aged2-3 | 336 | 96,305 (0.963) | 75,755 (0.758) |
| backlog-adp@blank-aged2-4 | 336 | 104,897 (1.049) | 75,780 (0.758) |
| backlog-adp@blank-aged2-5 | 336 | 105,097 (1.051) | 75,839 (0.758) |
| backlog-adp@blank-aged2-6 | 336 | 105,097 (1.051) | 75,929 (0.759) |
| backlog-adp@blank-aged2-7 | 336 | 98,145 (0.981) | 75,929 (0.759) |
| backlog-adp@program-aged2-0 | 441 | 121,056 (1.211) | 81,512 (0.815) |
| backlog-adp@program-aged2-1 | 441 | 121,056 (1.211) | 81,512 (0.815) |
| backlog-adp@program-aged2-2 | 441 | 121,056 (1.211) | 81,429 (0.814) |
| backlog-adp@program-aged2-3 | 442 | 121,056 (1.211) | 81,486 (0.815) |
| backlog-adp@program-aged2-4 | 442 | 121,056 (1.211) | 81,511 (0.815) |
| backlog-adp@program-aged2-5 | 442 | 121,056 (1.211) | 81,547 (0.815) |
| backlog-adp@program-aged2-6 | 442 | 121,056 (1.211) | 81,743 (0.817) |
| backlog-adp@program-aged2-7 | 442 | 121,056 (1.211) | 81,743 (0.817) |
| backlog-adp@verify-aged2-0 | 547 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-aged2-1 | 547 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-aged2-2 | 547 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-aged2-3 | 548 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-aged2-4 | 548 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-aged2-5 | 548 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-aged2-6 | 548 | 121,056 (1.211) | 95,345 (0.953) |
| backlog-adp@verify-aged2-7 | 548 | 121,056 (1.211) | 95,345 (0.953) |
| save | 585 | 124,495 (1.245) | 95,157 (0.952) |
| backlog | 266 | 47,599 (0.476) | 2,692 (0.027) |
| backlog-adp | 271 | 47,599 (0.476) | 2,692 (0.027) |
| backlog-adp-refill | 273 | 47,599 (0.476) | 2,692 (0.027) |
| backlog-owed | 305 | 47,599 (0.476) | 2,692 (0.027) |

Longest pass that carries a step: 125,743 CPU cycles (1.257 ms), save-held; longest step: 95,873 (0.959 ms), save-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if1` | 425,375 | 4.254 | 20 | 200 | fits | 105,734 | 85 | 0.546 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 696,056 | 6.961 | 20 | 20 | fits | 91,935 | 42 | 0.688 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if1` | 904,015 | 9.040 | 20 | 24 | fits | 28,666 | 23 | 0.539 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 461,694 | 4.617 | 20 | 50 | fits | 95,931 | 56 | 0.636 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if1` | 1,273,937 | 12.739 | 18 | 18 | fits | 58,277 | 31 | 0.701 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 433,710 | 4.337 | 20 | 200 | fits | 108,880 | 91 | 0.568 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 698,491 | 6.985 | 20 | 20 | fits | 79,595 | 43 | 0.658 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 966,527 | 9.665 | 20 | 24 | fits | 32,034 | 29 | 0.601 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 473,179 | 4.732 | 20 | 50 | fits | 99,081 | 62 | 0.653 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,358,975 | 13.590 | 18 | 18 | fits | 50,638 | 34 | 0.736 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 479,833 | 4.798 | 20 | 20 | fits | 138,599 | 90 | 0.658 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 175,645 | 1.756 | 20 | 200 | fits | 108,163 | 140 | 0.527 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 604,818 | 6.048 | 20 | 200 | fits | 138,599 | 90 | 0.658 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 176,557 | 1.766 | 20 | 20 | fits | 108,163 | 140 | 0.527 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 817,220 | 8.172 | 20 | 20 | fits | 105,433 | 47 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 180,142 | 1.801 | 20 | 24 | fits | 108,163 | 140 | 0.527 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if1` | 1,418,782 | 14.188 | 20 | 24 | fits | 59,139 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 179,102 | 1.791 | 20 | 50 | fits | 108,163 | 140 | 0.527 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 608,494 | 6.085 | 20 | 50 | fits | 138,599 | 90 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 354,607 | 3.546 | 18 | 18 | fits | 175,960 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if1` | 1,501,649 | 15.016 | 18 | 18 | fits | 42,099 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 461,063 | 4.611 | 20 | 20 | fits | 126,876 | 61 | 0.678 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 150,551 | 1.506 | 20 | 200 | fits | 107,612 | 142 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 576,716 | 5.767 | 20 | 200 | fits | 126,876 | 61 | 0.678 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 151,463 | 1.515 | 20 | 20 | fits | 107,612 | 142 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 788,581 | 7.886 | 20 | 20 | fits | 105,458 | 47 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 47,436 | 0.474 | 20 | 24 | fits | 48,446 | 65 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if1` | 1,301,920 | 13.019 | 20 | 24 | fits | 59,134 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 46,396 | 0.464 | 20 | 50 | fits | 48,446 | 65 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 453,516 | 4.535 | 20 | 50 | fits | 123,575 | 83 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 329,876 | 3.299 | 18 | 18 | fits | 176,323 | 140 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if1` | 1,457,533 | 14.575 | 18 | 18 | fits | 31,026 | 15 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 395,982 | 3.960 | 20 | 20 | fits | 137,043 | 84 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 111,285 | 1.113 | 20 | 200 | fits | 107,232 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 521,363 | 5.214 | 20 | 200 | fits | 137,043 | 84 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 112,197 | 1.122 | 20 | 20 | fits | 107,232 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 714,775 | 7.148 | 20 | 20 | fits | 77,092 | 37 | 0.637 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 115,782 | 1.158 | 20 | 24 | fits | 107,232 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if1` | 1,307,000 | 13.070 | 20 | 24 | fits | 59,134 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 114,742 | 1.147 | 20 | 50 | fits | 107,232 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 525,039 | 5.250 | 20 | 50 | fits | 137,043 | 84 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 387,931 | 3.879 | 18 | 18 | fits | 170,771 | 105 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if1` | 1,467,722 | 14.677 | 18 | 18 | fits | 31,347 | 16 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 419,123 | 4.191 | 20 | 20 | fits | 135,850 | 84 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 104,107 | 1.041 | 20 | 200 | fits | 107,314 | 141 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 543,786 | 5.438 | 20 | 200 | fits | 135,850 | 84 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 105,019 | 1.050 | 20 | 20 | fits | 107,314 | 141 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 800,020 | 8.000 | 20 | 20 | fits | 86,358 | 39 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 108,604 | 1.086 | 20 | 24 | fits | 107,314 | 141 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if1` | 1,340,219 | 13.402 | 20 | 24 | fits | 63,227 | 38 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 107,564 | 1.076 | 20 | 50 | fits | 107,314 | 141 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 547,462 | 5.475 | 20 | 50 | fits | 135,850 | 84 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 284,491 | 2.845 | 18 | 18 | fits | 177,382 | 146 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if1` | 1,454,419 | 14.544 | 18 | 18 | fits | 31,133 | 16 | 0.743 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 418,834 | 4.188 | 20 | 20 | fits | 107,256 | 74 | 0.616 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 105,686 | 1.057 | 20 | 200 | fits | 106,854 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 515,100 | 5.151 | 20 | 200 | fits | 107,256 | 74 | 0.616 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 106,598 | 1.066 | 20 | 20 | fits | 106,854 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 763,311 | 7.633 | 20 | 20 | fits | 59,590 | 31 | 0.700 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 110,183 | 1.102 | 20 | 24 | fits | 106,854 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if1` | 1,313,833 | 13.138 | 20 | 24 | fits | 59,108 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 109,143 | 1.091 | 20 | 50 | fits | 106,854 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 518,776 | 5.188 | 20 | 50 | fits | 107,256 | 74 | 0.616 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 284,703 | 2.847 | 18 | 18 | fits | 176,015 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if1` | 1,476,437 | 14.764 | 18 | 18 | fits | 38,232 | 19 | 0.786 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 491,432 | 4.914 | 20 | 20 | fits | 124,506 | 57 | 0.691 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 115,246 | 1.152 | 20 | 200 | fits | 106,854 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 606,643 | 6.066 | 20 | 200 | fits | 124,506 | 57 | 0.691 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 116,158 | 1.162 | 20 | 20 | fits | 106,854 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 805,537 | 8.055 | 20 | 20 | fits | 87,633 | 40 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 119,743 | 1.197 | 20 | 24 | fits | 106,854 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if1` | 1,340,285 | 13.403 | 20 | 24 | fits | 48,255 | 27 | 0.728 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 118,703 | 1.187 | 20 | 50 | fits | 106,854 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 485,813 | 4.858 | 20 | 50 | fits | 93,214 | 64 | 0.697 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 294,263 | 2.943 | 18 | 18 | fits | 176,015 | 140 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if1` | 1,492,812 | 14.928 | 18 | 18 | fits | 31,026 | 15 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 485,760 | 4.858 | 20 | 20 | fits | 98,509 | 49 | 0.666 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 107,915 | 1.079 | 20 | 200 | fits | 106,783 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 574,099 | 5.741 | 20 | 200 | fits | 98,509 | 49 | 0.666 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 108,827 | 1.088 | 20 | 20 | fits | 106,783 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 769,743 | 7.697 | 20 | 20 | fits | 87,338 | 40 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 112,412 | 1.124 | 20 | 24 | fits | 106,783 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if1` | 1,312,392 | 13.124 | 20 | 24 | fits | 59,031 | 31 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 111,372 | 1.114 | 20 | 50 | fits | 106,783 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 479,266 | 4.793 | 20 | 50 | fits | 146,776 | 98 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 332,425 | 3.324 | 18 | 18 | fits | 118,788 | 64 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if1` | 1,478,778 | 14.788 | 18 | 18 | fits | 41,780 | 18 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 529,532 | 5.295 | 20 | 20 | fits | 125,586 | 58 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 117,383 | 1.174 | 20 | 200 | fits | 106,783 | 140 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 645,247 | 6.452 | 20 | 200 | fits | 125,586 | 58 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 118,295 | 1.183 | 20 | 20 | fits | 106,783 | 140 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 838,990 | 8.390 | 20 | 20 | fits | 87,256 | 40 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 121,880 | 1.219 | 20 | 24 | fits | 106,783 | 140 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if1` | 1,381,275 | 13.813 | 20 | 24 | fits | 59,139 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 120,840 | 1.208 | 20 | 50 | fits | 106,783 | 140 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 523,337 | 5.233 | 20 | 50 | fits | 130,102 | 105 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 246,068 | 2.461 | 18 | 18 | fits | 125,683 | 105 | 0.694 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if1` | 1,464,142 | 14.641 | 18 | 18 | fits | 42,099 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 422,200 | 4.222 | 20 | 20 | fits | 135,758 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 110,084 | 1.101 | 20 | 200 | fits | 107,714 | 140 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 546,968 | 5.470 | 20 | 200 | fits | 135,758 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 110,996 | 1.110 | 20 | 20 | fits | 107,714 | 140 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 759,057 | 7.591 | 20 | 20 | fits | 105,275 | 46 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 114,581 | 1.146 | 20 | 24 | fits | 107,714 | 140 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if1` | 1,324,950 | 13.249 | 20 | 24 | fits | 59,111 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 113,541 | 1.135 | 20 | 50 | fits | 107,714 | 140 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 550,644 | 5.506 | 20 | 50 | fits | 135,758 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 288,029 | 2.880 | 18 | 18 | fits | 174,943 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if1` | 1,449,380 | 14.494 | 18 | 18 | fits | 41,739 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 424,485 | 4.245 | 20 | 20 | fits | 135,975 | 84 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 112,364 | 1.124 | 20 | 200 | fits | 107,307 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 549,470 | 5.495 | 20 | 200 | fits | 135,975 | 84 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 113,276 | 1.133 | 20 | 20 | fits | 107,307 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 819,229 | 8.192 | 20 | 20 | fits | 86,981 | 40 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 116,861 | 1.169 | 20 | 24 | fits | 107,307 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if1` | 1,364,665 | 13.647 | 20 | 24 | fits | 59,138 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 115,821 | 1.158 | 20 | 50 | fits | 107,307 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 553,146 | 5.531 | 20 | 50 | fits | 135,975 | 84 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 290,314 | 2.903 | 18 | 18 | fits | 174,948 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if1` | 1,447,564 | 14.476 | 18 | 18 | fits | 42,099 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 493,834 | 4.938 | 20 | 20 | fits | 124,488 | 58 | 0.689 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 114,735 | 1.147 | 20 | 200 | fits | 107,378 | 140 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 608,911 | 6.089 | 20 | 200 | fits | 124,488 | 58 | 0.689 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 115,647 | 1.156 | 20 | 20 | fits | 107,378 | 140 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 811,263 | 8.113 | 20 | 20 | fits | 86,706 | 39 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 119,232 | 1.192 | 20 | 24 | fits | 107,378 | 140 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if1` | 1,347,174 | 13.472 | 20 | 24 | fits | 59,134 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 118,192 | 1.182 | 20 | 50 | fits | 107,378 | 140 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 488,099 | 4.881 | 20 | 50 | fits | 93,295 | 65 | 0.693 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 292,969 | 2.930 | 18 | 18 | fits | 175,232 | 141 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if1` | 1,468,495 | 14.685 | 18 | 18 | fits | 41,690 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 504,842 | 5.048 | 20 | 20 | fits | 125,224 | 57 | 0.693 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 117,054 | 1.171 | 20 | 200 | fits | 107,397 | 141 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 620,638 | 6.206 | 20 | 200 | fits | 125,224 | 57 | 0.693 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 117,966 | 1.180 | 20 | 20 | fits | 107,397 | 141 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 813,950 | 8.139 | 20 | 20 | fits | 87,088 | 39 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 121,551 | 1.216 | 20 | 24 | fits | 107,397 | 141 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if1` | 1,310,483 | 13.105 | 20 | 24 | fits | 62,559 | 38 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 120,511 | 1.205 | 20 | 50 | fits | 107,397 | 141 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 489,222 | 4.892 | 20 | 50 | fits | 146,935 | 99 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 342,222 | 3.422 | 18 | 18 | fits | 118,026 | 65 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if1` | 1,508,137 | 15.081 | 18 | 18 | fits | 31,072 | 16 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 431,814 | 4.318 | 20 | 20 | fits | 135,691 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 119,646 | 1.196 | 20 | 200 | fits | 107,552 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 556,515 | 5.565 | 20 | 200 | fits | 135,691 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 120,558 | 1.206 | 20 | 20 | fits | 107,552 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 742,346 | 7.423 | 20 | 20 | fits | 106,785 | 53 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 124,143 | 1.241 | 20 | 24 | fits | 107,552 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if1` | 1,315,059 | 13.151 | 20 | 24 | fits | 59,135 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 123,103 | 1.231 | 20 | 50 | fits | 107,552 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 560,191 | 5.602 | 20 | 50 | fits | 135,691 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 297,596 | 2.976 | 18 | 18 | fits | 174,948 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if1` | 1,470,640 | 14.706 | 18 | 18 | fits | 31,026 | 15 | 0.748 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 390,702 | 3.907 | 20 | 20 | fits | 136,895 | 90 | 0.647 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 105,218 | 1.052 | 20 | 200 | fits | 107,552 | 140 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 514,803 | 5.148 | 20 | 200 | fits | 136,895 | 90 | 0.647 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 106,130 | 1.061 | 20 | 20 | fits | 107,552 | 140 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 792,181 | 7.922 | 20 | 20 | fits | 86,475 | 40 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 109,715 | 1.097 | 20 | 24 | fits | 107,552 | 140 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if1` | 1,337,265 | 13.373 | 20 | 24 | fits | 59,134 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 108,675 | 1.087 | 20 | 50 | fits | 107,552 | 140 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 518,479 | 5.185 | 20 | 50 | fits | 136,895 | 90 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 283,168 | 2.832 | 18 | 18 | fits | 174,948 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if1` | 1,451,223 | 14.512 | 18 | 18 | fits | 31,089 | 15 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 512,312 | 5.123 | 20 | 20 | fits | 124,418 | 57 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 107,600 | 1.076 | 20 | 200 | fits | 107,634 | 141 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 628,019 | 6.280 | 20 | 200 | fits | 124,418 | 57 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 108,512 | 1.085 | 20 | 20 | fits | 107,634 | 141 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 821,599 | 8.216 | 20 | 20 | fits | 87,222 | 39 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 112,097 | 1.121 | 20 | 24 | fits | 107,634 | 141 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if1` | 1,361,813 | 13.618 | 20 | 24 | fits | 63,210 | 38 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 111,057 | 1.111 | 20 | 50 | fits | 107,634 | 141 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 497,934 | 4.979 | 20 | 50 | fits | 95,713 | 65 | 0.712 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 287,036 | 2.870 | 18 | 18 | fits | 176,434 | 146 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if1` | 1,471,941 | 14.719 | 18 | 18 | fits | 41,734 | 19 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 479,090 | 4.791 | 20 | 20 | fits | 126,025 | 57 | 0.696 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 102,250 | 1.022 | 20 | 200 | fits | 107,308 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 594,945 | 5.949 | 20 | 200 | fits | 126,025 | 57 | 0.696 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 103,162 | 1.032 | 20 | 20 | fits | 107,308 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 762,797 | 7.628 | 20 | 20 | fits | 88,810 | 46 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 106,747 | 1.067 | 20 | 24 | fits | 107,308 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if1` | 1,305,853 | 13.059 | 20 | 24 | fits | 59,139 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 105,707 | 1.057 | 20 | 50 | fits | 107,308 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 472,596 | 4.726 | 20 | 50 | fits | 146,757 | 98 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 325,774 | 3.258 | 18 | 18 | fits | 117,857 | 64 | 0.739 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if1` | 1,472,239 | 14.722 | 18 | 18 | fits | 41,780 | 18 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 397,201 | 3.972 | 20 | 20 | fits | 137,018 | 84 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 112,622 | 1.126 | 20 | 200 | fits | 107,239 | 140 | 0.520 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 522,557 | 5.226 | 20 | 200 | fits | 137,018 | 84 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 113,534 | 1.135 | 20 | 20 | fits | 107,239 | 140 | 0.520 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 744,183 | 7.442 | 20 | 20 | fits | 105,306 | 46 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 117,119 | 1.171 | 20 | 24 | fits | 107,239 | 140 | 0.520 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if1` | 1,335,607 | 13.356 | 20 | 24 | fits | 59,123 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 116,079 | 1.161 | 20 | 50 | fits | 107,239 | 140 | 0.520 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 526,233 | 5.262 | 20 | 50 | fits | 137,018 | 84 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 389,150 | 3.892 | 18 | 18 | fits | 170,758 | 105 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if1` | 1,482,904 | 14.829 | 18 | 18 | fits | 31,809 | 16 | 0.763 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 420,251 | 4.203 | 20 | 20 | fits | 135,850 | 84 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 105,381 | 1.054 | 20 | 200 | fits | 107,258 | 141 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 544,914 | 5.449 | 20 | 200 | fits | 135,850 | 84 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 106,293 | 1.063 | 20 | 20 | fits | 107,258 | 141 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 766,133 | 7.661 | 20 | 20 | fits | 105,474 | 46 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 109,878 | 1.099 | 20 | 24 | fits | 107,258 | 141 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if1` | 1,357,896 | 13.579 | 20 | 24 | fits | 59,352 | 32 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 108,838 | 1.088 | 20 | 50 | fits | 107,258 | 141 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 548,590 | 5.486 | 20 | 50 | fits | 135,850 | 84 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 285,644 | 2.856 | 18 | 18 | fits | 177,261 | 146 | 0.615 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if1` | 1,463,130 | 14.631 | 18 | 18 | fits | 32,171 | 16 | 0.769 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 420,367 | 4.204 | 20 | 20 | fits | 135,691 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 107,354 | 1.074 | 20 | 200 | fits | 106,753 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 545,068 | 5.451 | 20 | 200 | fits | 135,691 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 108,266 | 1.083 | 20 | 20 | fits | 106,753 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 815,967 | 8.160 | 20 | 20 | fits | 91,880 | 46 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 111,851 | 1.119 | 20 | 24 | fits | 106,753 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if1` | 1,362,222 | 13.622 | 20 | 24 | fits | 59,139 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 110,811 | 1.108 | 20 | 50 | fits | 106,753 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 548,744 | 5.487 | 20 | 50 | fits | 135,691 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 286,261 | 2.863 | 18 | 18 | fits | 175,905 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if1` | 1,495,213 | 14.952 | 18 | 18 | fits | 61,051 | 29 | 0.798 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 429,927 | 4.299 | 20 | 20 | fits | 107,256 | 74 | 0.616 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 116,914 | 1.169 | 20 | 200 | fits | 106,753 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 526,193 | 5.262 | 20 | 200 | fits | 107,256 | 74 | 0.616 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 117,826 | 1.178 | 20 | 20 | fits | 106,753 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 806,430 | 8.064 | 20 | 20 | fits | 87,243 | 40 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 121,411 | 1.214 | 20 | 24 | fits | 106,753 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if1` | 1,351,954 | 13.520 | 20 | 24 | fits | 59,134 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 120,371 | 1.204 | 20 | 50 | fits | 106,753 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 529,869 | 5.299 | 20 | 50 | fits | 107,256 | 74 | 0.616 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 295,821 | 2.958 | 18 | 18 | fits | 175,905 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if1` | 1,496,996 | 14.970 | 18 | 18 | fits | 31,818 | 15 | 0.772 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 489,154 | 4.892 | 20 | 20 | fits | 127,915 | 64 | 0.696 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 109,725 | 1.097 | 20 | 200 | fits | 106,824 | 140 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 604,680 | 6.047 | 20 | 200 | fits | 127,915 | 64 | 0.696 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 110,637 | 1.106 | 20 | 20 | fits | 106,824 | 140 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 798,162 | 7.982 | 20 | 20 | fits | 87,173 | 40 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 114,222 | 1.142 | 20 | 24 | fits | 106,824 | 140 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if1` | 1,343,454 | 13.435 | 20 | 24 | fits | 59,134 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 113,182 | 1.132 | 20 | 50 | fits | 106,824 | 140 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 480,441 | 4.804 | 20 | 50 | fits | 93,473 | 65 | 0.696 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 288,632 | 2.886 | 18 | 18 | fits | 175,905 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if1` | 1,464,801 | 14.648 | 18 | 18 | fits | 41,725 | 18 | 0.702 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 511,309 | 5.113 | 20 | 20 | fits | 125,387 | 58 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 102,394 | 1.024 | 20 | 200 | fits | 106,753 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 626,825 | 6.268 | 20 | 200 | fits | 125,387 | 58 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 103,306 | 1.033 | 20 | 20 | fits | 106,753 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 820,402 | 8.204 | 20 | 20 | fits | 87,173 | 40 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 106,891 | 1.069 | 20 | 24 | fits | 106,753 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if1` | 1,362,290 | 13.623 | 20 | 24 | fits | 58,948 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 105,851 | 1.059 | 20 | 50 | fits | 106,753 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 505,114 | 5.051 | 20 | 50 | fits | 128,244 | 105 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 281,301 | 2.813 | 18 | 18 | fits | 175,905 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if1` | 1,445,189 | 14.452 | 18 | 18 | fits | 42,099 | 18 | 0.700 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 524,292 | 5.243 | 20 | 20 | fits | 125,417 | 58 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 111,954 | 1.120 | 20 | 200 | fits | 106,753 | 140 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 639,741 | 6.397 | 20 | 200 | fits | 125,417 | 58 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 112,866 | 1.129 | 20 | 20 | fits | 106,753 | 140 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 842,313 | 8.423 | 20 | 20 | fits | 87,237 | 39 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 116,451 | 1.165 | 20 | 24 | fits | 106,753 | 140 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if1` | 1,374,981 | 13.750 | 20 | 24 | fits | 59,088 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 115,411 | 1.154 | 20 | 50 | fits | 106,753 | 140 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 518,000 | 5.180 | 20 | 50 | fits | 126,763 | 99 | 0.601 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 240,923 | 2.409 | 18 | 18 | fits | 125,967 | 106 | 0.694 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if1` | 1,462,630 | 14.626 | 18 | 18 | fits | 46,849 | 25 | 0.720 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 489,485 | 4.895 | 20 | 20 | fits | 125,440 | 58 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 78,884 | 0.789 | 20 | 200 | fits | 85,056 | 105 | 0.606 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 604,957 | 6.050 | 20 | 200 | fits | 125,440 | 58 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 79,796 | 0.798 | 20 | 20 | fits | 85,056 | 105 | 0.606 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 807,683 | 8.077 | 20 | 20 | fits | 87,314 | 39 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 83,381 | 0.834 | 20 | 24 | fits | 85,056 | 105 | 0.606 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if1` | 1,339,946 | 13.399 | 20 | 24 | fits | 59,123 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 82,341 | 0.823 | 20 | 50 | fits | 85,056 | 105 | 0.606 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 483,193 | 4.832 | 20 | 50 | fits | 126,822 | 99 | 0.602 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 356,306 | 3.563 | 18 | 18 | fits | 170,723 | 105 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if1` | 1,457,492 | 14.575 | 18 | 18 | fits | 45,325 | 25 | 0.711 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 438,776 | 4.388 | 20 | 20 | fits | 135,825 | 83 | 0.654 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 116,162 | 1.162 | 20 | 200 | fits | 106,281 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 564,073 | 5.641 | 20 | 200 | fits | 135,825 | 83 | 0.654 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 117,074 | 1.171 | 20 | 20 | fits | 106,281 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 776,226 | 7.762 | 20 | 20 | fits | 105,342 | 46 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 120,659 | 1.207 | 20 | 24 | fits | 106,281 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if1` | 1,450,796 | 14.508 | 20 | 24 | fits | 59,243 | 32 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 119,619 | 1.196 | 20 | 50 | fits | 106,281 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 567,749 | 5.677 | 20 | 50 | fits | 135,825 | 83 | 0.654 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 295,322 | 2.953 | 18 | 18 | fits | 176,158 | 141 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if1` | 1,523,013 | 15.230 | 18 | 18 | fits | 31,389 | 16 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 425,507 | 4.255 | 20 | 20 | fits | 136,084 | 83 | 0.653 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 102,900 | 1.029 | 20 | 200 | fits | 106,309 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 550,532 | 5.505 | 20 | 200 | fits | 136,084 | 83 | 0.653 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 103,812 | 1.038 | 20 | 20 | fits | 106,309 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 762,780 | 7.628 | 20 | 20 | fits | 105,275 | 46 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 107,397 | 1.074 | 20 | 24 | fits | 106,309 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if1` | 1,438,731 | 14.387 | 20 | 24 | fits | 59,243 | 32 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 106,357 | 1.064 | 20 | 50 | fits | 106,309 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 554,208 | 5.542 | 20 | 50 | fits | 136,084 | 83 | 0.653 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 282,060 | 2.821 | 18 | 18 | fits | 176,158 | 141 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if1` | 1,521,859 | 15.219 | 18 | 18 | fits | 31,480 | 15 | 0.759 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 429,507 | 4.295 | 20 | 20 | fits | 135,691 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 108,299 | 1.083 | 20 | 200 | fits | 106,347 | 135 | 0.514 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 554,208 | 5.542 | 20 | 200 | fits | 135,691 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 109,211 | 1.092 | 20 | 20 | fits | 106,347 | 135 | 0.514 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 738,810 | 7.388 | 20 | 20 | fits | 77,788 | 37 | 0.642 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 112,796 | 1.128 | 20 | 24 | fits | 106,347 | 135 | 0.514 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if1` | 1,394,917 | 13.949 | 20 | 24 | fits | 59,586 | 31 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 111,756 | 1.118 | 20 | 50 | fits | 106,347 | 135 | 0.514 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 557,884 | 5.579 | 20 | 50 | fits | 135,691 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 295,539 | 2.955 | 18 | 18 | fits | 175,565 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if1` | 1,550,863 | 15.509 | 18 | 18 | fits | 31,130 | 15 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 417,354 | 4.174 | 20 | 20 | fits | 135,758 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 104,286 | 1.043 | 20 | 200 | fits | 105,868 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 542,122 | 5.421 | 20 | 200 | fits | 135,758 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 105,198 | 1.052 | 20 | 20 | fits | 105,868 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 878,302 | 8.783 | 20 | 20 | fits | 90,415 | 45 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 108,783 | 1.088 | 20 | 24 | fits | 105,868 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if1` | 1,414,531 | 14.145 | 20 | 24 | fits | 59,149 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 107,743 | 1.077 | 20 | 50 | fits | 105,868 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 545,798 | 5.458 | 20 | 50 | fits | 135,758 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 283,223 | 2.832 | 18 | 18 | fits | 175,935 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if1` | 1,528,567 | 15.286 | 18 | 18 | fits | 31,115 | 15 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 422,342 | 4.223 | 20 | 20 | fits | 107,323 | 74 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 109,329 | 1.093 | 20 | 200 | fits | 105,926 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 518,675 | 5.187 | 20 | 200 | fits | 107,323 | 74 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 110,241 | 1.102 | 20 | 20 | fits | 105,926 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 883,304 | 8.833 | 20 | 20 | fits | 87,431 | 39 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 113,826 | 1.138 | 20 | 24 | fits | 105,926 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if1` | 1,419,305 | 14.193 | 20 | 24 | fits | 59,160 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 112,786 | 1.128 | 20 | 50 | fits | 105,926 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 522,351 | 5.224 | 20 | 50 | fits | 107,323 | 74 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 288,211 | 2.882 | 18 | 18 | fits | 175,880 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if1` | 1,543,075 | 15.431 | 18 | 18 | fits | 41,734 | 19 | 0.692 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 577,569 | 5.776 | 20 | 20 | fits | 127,873 | 63 | 0.699 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 114,260 | 1.143 | 20 | 200 | fits | 105,888 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 693,398 | 6.934 | 20 | 200 | fits | 127,873 | 63 | 0.699 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 115,172 | 1.152 | 20 | 20 | fits | 105,888 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 886,611 | 8.866 | 20 | 20 | fits | 87,021 | 39 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 118,757 | 1.188 | 20 | 24 | fits | 105,888 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if1` | 1,393,023 | 13.930 | 20 | 24 | fits | 56,414 | 39 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 117,717 | 1.177 | 20 | 50 | fits | 105,888 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 484,717 | 4.847 | 20 | 50 | fits | 93,214 | 64 | 0.697 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 293,167 | 2.932 | 18 | 18 | fits | 175,905 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if1` | 1,559,454 | 15.595 | 18 | 18 | fits | 41,824 | 19 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 566,113 | 5.661 | 20 | 20 | fits | 125,957 | 57 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 99,413 | 0.994 | 20 | 200 | fits | 105,888 | 134 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 681,831 | 6.818 | 20 | 200 | fits | 125,957 | 57 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 100,325 | 1.003 | 20 | 20 | fits | 105,888 | 134 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 875,251 | 8.753 | 20 | 20 | fits | 87,021 | 39 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 103,910 | 1.039 | 20 | 24 | fits | 105,888 | 134 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if1` | 1,381,928 | 13.819 | 20 | 24 | fits | 59,259 | 32 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 102,870 | 1.029 | 20 | 50 | fits | 105,888 | 134 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 559,550 | 5.596 | 20 | 50 | fits | 150,261 | 104 | 0.658 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 324,531 | 3.245 | 18 | 18 | fits | 118,642 | 64 | 0.739 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if1` | 1,548,515 | 15.485 | 18 | 18 | fits | 41,824 | 19 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 601,498 | 6.015 | 20 | 20 | fits | 125,327 | 57 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 105,669 | 1.057 | 20 | 200 | fits | 105,926 | 134 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 716,985 | 7.170 | 20 | 200 | fits | 125,327 | 57 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 106,581 | 1.066 | 20 | 20 | fits | 105,926 | 134 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 910,285 | 9.103 | 20 | 20 | fits | 87,021 | 39 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 110,166 | 1.102 | 20 | 24 | fits | 105,926 | 134 | 0.512 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if1` | 1,445,787 | 14.458 | 20 | 24 | fits | 59,247 | 32 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 109,126 | 1.091 | 20 | 50 | fits | 105,926 | 134 | 0.512 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 595,334 | 5.953 | 20 | 50 | fits | 126,341 | 98 | 0.601 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 234,219 | 2.342 | 18 | 18 | fits | 125,548 | 105 | 0.693 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if1` | 1,539,848 | 15.398 | 18 | 18 | fits | 44,065 | 18 | 0.756 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 419,609 | 4.196 | 20 | 20 | fits | 107,419 | 75 | 0.617 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 107,551 | 1.076 | 20 | 200 | fits | 106,848 | 134 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 516,038 | 5.160 | 20 | 200 | fits | 107,419 | 75 | 0.617 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 108,463 | 1.085 | 20 | 20 | fits | 106,848 | 134 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 730,056 | 7.301 | 20 | 20 | fits | 105,625 | 47 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 112,048 | 1.120 | 20 | 24 | fits | 106,848 | 134 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if1` | 1,406,173 | 14.062 | 20 | 24 | fits | 59,258 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 111,008 | 1.110 | 20 | 50 | fits | 106,848 | 134 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 519,714 | 5.197 | 20 | 50 | fits | 107,419 | 75 | 0.617 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 285,391 | 2.854 | 18 | 18 | fits | 174,838 | 140 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if1` | 1,531,136 | 15.311 | 18 | 18 | fits | 41,858 | 18 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 398,017 | 3.980 | 20 | 20 | fits | 136,962 | 90 | 0.648 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 112,558 | 1.126 | 20 | 200 | fits | 106,914 | 134 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 522,185 | 5.222 | 20 | 200 | fits | 136,962 | 90 | 0.648 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 113,470 | 1.135 | 20 | 20 | fits | 106,914 | 134 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 734,732 | 7.347 | 20 | 20 | fits | 105,510 | 47 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 117,055 | 1.171 | 20 | 24 | fits | 106,914 | 134 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if1` | 1,393,483 | 13.935 | 20 | 24 | fits | 59,254 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 116,015 | 1.160 | 20 | 50 | fits | 106,914 | 134 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 525,861 | 5.259 | 20 | 50 | fits | 136,962 | 90 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 290,483 | 2.905 | 18 | 18 | fits | 174,923 | 140 | 0.619 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if1` | 1,554,326 | 15.543 | 18 | 18 | fits | 35,931 | 22 | 0.766 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 427,543 | 4.275 | 20 | 20 | fits | 127,712 | 61 | 0.681 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 150,972 | 1.510 | 20 | 200 | fits | 106,986 | 136 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 543,593 | 5.436 | 20 | 200 | fits | 127,712 | 61 | 0.681 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 151,884 | 1.519 | 20 | 20 | fits | 106,986 | 136 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 736,414 | 7.364 | 20 | 20 | fits | 77,034 | 37 | 0.637 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 48,483 | 0.485 | 20 | 24 | fits | 51,940 | 71 | 0.560 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if1` | 1,355,163 | 13.552 | 20 | 24 | fits | 59,253 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 47,443 | 0.474 | 20 | 50 | fits | 51,940 | 71 | 0.560 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 419,557 | 4.196 | 20 | 50 | fits | 162,799 | 83 | 0.682 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 419,492 | 4.195 | 18 | 18 | fits | 162,799 | 83 | 0.682 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if1` | 1,557,174 | 15.572 | 18 | 18 | fits | 31,072 | 16 | 0.740 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 418,298 | 4.183 | 20 | 20 | fits | 135,917 | 84 | 0.649 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 104,044 | 1.040 | 20 | 200 | fits | 107,029 | 135 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 543,028 | 5.430 | 20 | 200 | fits | 135,917 | 84 | 0.649 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 104,956 | 1.050 | 20 | 20 | fits | 107,029 | 135 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 883,810 | 8.838 | 20 | 20 | fits | 86,804 | 39 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 108,541 | 1.085 | 20 | 24 | fits | 107,029 | 135 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if1` | 1,413,618 | 14.136 | 20 | 24 | fits | 59,469 | 32 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 107,501 | 1.075 | 20 | 50 | fits | 107,029 | 135 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 546,704 | 5.467 | 20 | 50 | fits | 135,917 | 84 | 0.649 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 283,626 | 2.836 | 18 | 18 | fits | 176,580 | 146 | 0.614 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if1` | 1,538,392 | 15.384 | 18 | 18 | fits | 41,783 | 19 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 432,166 | 4.322 | 20 | 20 | fits | 106,583 | 74 | 0.612 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 110,558 | 1.106 | 20 | 200 | fits | 107,093 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 528,221 | 5.282 | 20 | 200 | fits | 106,583 | 74 | 0.612 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 111,470 | 1.115 | 20 | 20 | fits | 107,093 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 888,339 | 8.883 | 20 | 20 | fits | 87,276 | 39 | 0.727 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 115,055 | 1.151 | 20 | 24 | fits | 107,093 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if1` | 1,400,376 | 14.004 | 20 | 24 | fits | 59,244 | 32 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 114,015 | 1.140 | 20 | 50 | fits | 107,093 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 531,897 | 5.319 | 20 | 50 | fits | 106,583 | 74 | 0.612 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 288,672 | 2.887 | 18 | 18 | fits | 175,112 | 141 | 0.618 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if1` | 1,563,468 | 15.635 | 18 | 18 | fits | 41,722 | 19 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 583,507 | 5.835 | 20 | 20 | fits | 124,753 | 57 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 115,881 | 1.159 | 20 | 200 | fits | 107,055 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 699,669 | 6.997 | 20 | 200 | fits | 124,753 | 57 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 116,793 | 1.168 | 20 | 20 | fits | 107,055 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 893,137 | 8.931 | 20 | 20 | fits | 87,171 | 39 | 0.726 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 120,378 | 1.204 | 20 | 24 | fits | 107,055 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if1` | 1,431,707 | 14.317 | 20 | 24 | fits | 59,131 | 32 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 119,338 | 1.193 | 20 | 50 | fits | 107,055 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 494,549 | 4.945 | 20 | 50 | fits | 93,393 | 64 | 0.698 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 293,965 | 2.940 | 18 | 18 | fits | 175,082 | 141 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if1` | 1,567,452 | 15.675 | 18 | 18 | fits | 41,815 | 18 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 572,098 | 5.721 | 20 | 20 | fits | 125,926 | 57 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 102,619 | 1.026 | 20 | 200 | fits | 107,055 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 687,854 | 6.879 | 20 | 200 | fits | 125,926 | 57 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 103,531 | 1.035 | 20 | 20 | fits | 107,055 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 881,200 | 8.812 | 20 | 20 | fits | 87,021 | 39 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 107,116 | 1.071 | 20 | 24 | fits | 107,055 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if1` | 1,399,786 | 13.998 | 20 | 24 | fits | 59,872 | 31 | 0.718 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 106,076 | 1.061 | 20 | 50 | fits | 107,055 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 565,604 | 5.656 | 20 | 50 | fits | 146,496 | 98 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 334,688 | 3.347 | 18 | 18 | fits | 117,806 | 64 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if1` | 1,566,329 | 15.663 | 18 | 18 | fits | 41,754 | 18 | 0.691 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 624,854 | 6.249 | 20 | 20 | fits | 124,747 | 57 | 0.685 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 150,286 | 1.503 | 20 | 200 | fits | 106,737 | 136 | 0.512 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 739,835 | 7.398 | 20 | 200 | fits | 124,747 | 57 | 0.685 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 151,198 | 1.512 | 20 | 20 | fits | 106,737 | 136 | 0.512 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 907,560 | 9.076 | 20 | 20 | fits | 88,758 | 46 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 48,046 | 0.480 | 20 | 24 | fits | 51,519 | 71 | 0.550 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if1` | 1,391,368 | 13.914 | 20 | 24 | fits | 58,945 | 31 | 0.702 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 47,006 | 0.470 | 20 | 50 | fits | 51,519 | 71 | 0.550 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 509,322 | 5.093 | 20 | 50 | fits | 146,595 | 98 | 0.648 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 278,345 | 2.783 | 18 | 18 | fits | 125,057 | 105 | 0.694 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if1` | 1,557,736 | 15.577 | 18 | 18 | fits | 41,780 | 18 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 428,059 | 4.281 | 20 | 20 | fits | 135,758 | 83 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 115,109 | 1.151 | 20 | 200 | fits | 106,309 | 134 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 552,827 | 5.528 | 20 | 200 | fits | 135,758 | 83 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 116,021 | 1.160 | 20 | 20 | fits | 106,309 | 134 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 769,510 | 7.695 | 20 | 20 | fits | 109,585 | 53 | 0.694 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 119,606 | 1.196 | 20 | 24 | fits | 106,309 | 134 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if1` | 1,448,738 | 14.487 | 20 | 24 | fits | 59,254 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 118,566 | 1.186 | 20 | 50 | fits | 106,309 | 134 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 556,503 | 5.565 | 20 | 50 | fits | 135,758 | 83 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 293,938 | 2.939 | 18 | 18 | fits | 175,827 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if1` | 1,521,080 | 15.211 | 18 | 18 | fits | 31,464 | 15 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 413,672 | 4.137 | 20 | 20 | fits | 136,042 | 84 | 0.650 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 99,862 | 0.999 | 20 | 200 | fits | 106,337 | 134 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 538,724 | 5.387 | 20 | 200 | fits | 136,042 | 84 | 0.650 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 100,774 | 1.008 | 20 | 20 | fits | 106,337 | 134 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 755,162 | 7.552 | 20 | 20 | fits | 105,640 | 47 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 104,359 | 1.044 | 20 | 24 | fits | 106,337 | 134 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if1` | 1,434,650 | 14.347 | 20 | 24 | fits | 59,254 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 103,319 | 1.033 | 20 | 50 | fits | 106,337 | 134 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 542,400 | 5.424 | 20 | 50 | fits | 136,042 | 84 | 0.650 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 279,551 | 2.796 | 18 | 18 | fits | 176,687 | 145 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if1` | 1,506,992 | 15.070 | 18 | 18 | fits | 31,464 | 15 | 0.757 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 422,811 | 4.228 | 20 | 20 | fits | 139,489 | 90 | 0.659 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 106,518 | 1.065 | 20 | 200 | fits | 106,375 | 134 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 548,226 | 5.482 | 20 | 200 | fits | 139,489 | 90 | 0.659 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 107,430 | 1.074 | 20 | 20 | fits | 106,375 | 134 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 733,052 | 7.331 | 20 | 20 | fits | 77,780 | 38 | 0.638 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 111,015 | 1.110 | 20 | 24 | fits | 106,375 | 134 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if1` | 1,412,612 | 14.126 | 20 | 24 | fits | 59,254 | 31 | 0.704 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 109,975 | 1.100 | 20 | 50 | fits | 106,375 | 134 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 551,902 | 5.519 | 20 | 50 | fits | 139,489 | 90 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 285,322 | 2.853 | 18 | 18 | fits | 175,802 | 140 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if1` | 1,526,895 | 15.269 | 18 | 18 | fits | 31,208 | 15 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 428,445 | 4.284 | 20 | 20 | fits | 136,086 | 84 | 0.651 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 111,449 | 1.114 | 20 | 200 | fits | 106,337 | 134 | 0.518 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 553,441 | 5.534 | 20 | 200 | fits | 136,086 | 84 | 0.651 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 112,361 | 1.124 | 20 | 20 | fits | 106,337 | 134 | 0.518 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 887,146 | 8.871 | 20 | 20 | fits | 87,072 | 39 | 0.736 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 115,946 | 1.159 | 20 | 24 | fits | 106,337 | 134 | 0.518 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if1` | 1,423,107 | 14.231 | 20 | 24 | fits | 59,149 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 114,906 | 1.149 | 20 | 50 | fits | 106,337 | 134 | 0.518 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 557,117 | 5.571 | 20 | 50 | fits | 136,086 | 84 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 290,562 | 2.906 | 18 | 18 | fits | 176,111 | 141 | 0.620 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if1` | 1,537,143 | 15.371 | 18 | 18 | fits | 31,115 | 15 | 0.752 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 400,910 | 4.009 | 20 | 20 | fits | 108,570 | 75 | 0.621 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 116,364 | 1.164 | 20 | 200 | fits | 106,375 | 134 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 497,818 | 4.978 | 20 | 200 | fits | 108,570 | 75 | 0.621 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 117,276 | 1.173 | 20 | 20 | fits | 106,375 | 134 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 860,056 | 8.601 | 20 | 20 | fits | 87,387 | 39 | 0.729 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 120,861 | 1.209 | 20 | 24 | fits | 106,375 | 134 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if1` | 1,396,091 | 13.961 | 20 | 24 | fits | 59,150 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 119,821 | 1.198 | 20 | 50 | fits | 106,375 | 134 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 501,494 | 5.015 | 20 | 50 | fits | 108,570 | 75 | 0.621 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 392,859 | 3.929 | 18 | 18 | fits | 170,824 | 105 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if1` | 1,562,712 | 15.627 | 18 | 18 | fits | 41,798 | 19 | 0.682 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 566,112 | 5.661 | 20 | 20 | fits | 124,921 | 57 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 102,938 | 1.029 | 20 | 200 | fits | 106,455 | 135 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 681,922 | 6.819 | 20 | 200 | fits | 124,921 | 57 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 103,850 | 1.038 | 20 | 20 | fits | 106,455 | 135 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 875,328 | 8.753 | 20 | 20 | fits | 87,104 | 39 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 107,435 | 1.074 | 20 | 24 | fits | 106,455 | 135 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if1` | 1,399,197 | 13.992 | 20 | 24 | fits | 57,634 | 39 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 106,395 | 1.064 | 20 | 50 | fits | 106,455 | 135 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 475,289 | 4.753 | 20 | 50 | fits | 93,255 | 65 | 0.694 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 283,473 | 2.835 | 18 | 18 | fits | 177,533 | 146 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if1` | 1,555,278 | 15.553 | 18 | 18 | fits | 31,070 | 16 | 0.738 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 574,604 | 5.746 | 20 | 20 | fits | 126,004 | 57 | 0.695 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 110,862 | 1.109 | 20 | 200 | fits | 106,516 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 690,369 | 6.904 | 20 | 200 | fits | 126,004 | 57 | 0.695 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 111,774 | 1.118 | 20 | 20 | fits | 106,516 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 883,789 | 8.838 | 20 | 20 | fits | 87,021 | 39 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 115,359 | 1.154 | 20 | 24 | fits | 106,516 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if1` | 1,390,461 | 13.905 | 20 | 24 | fits | 59,259 | 32 | 0.701 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 114,319 | 1.143 | 20 | 50 | fits | 106,516 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 568,041 | 5.680 | 20 | 50 | fits | 146,842 | 98 | 0.651 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 335,451 | 3.355 | 18 | 18 | fits | 118,859 | 65 | 0.738 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if1` | 1,557,048 | 15.570 | 18 | 18 | fits | 41,824 | 19 | 0.685 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 610,030 | 6.100 | 20 | 20 | fits | 125,327 | 57 | 0.692 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 116,169 | 1.162 | 20 | 200 | fits | 106,554 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 725,517 | 7.255 | 20 | 200 | fits | 125,327 | 57 | 0.692 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 117,081 | 1.171 | 20 | 20 | fits | 106,554 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 918,817 | 9.188 | 20 | 20 | fits | 87,021 | 39 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 120,666 | 1.207 | 20 | 24 | fits | 106,554 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if1` | 1,443,031 | 14.430 | 20 | 24 | fits | 59,243 | 32 | 0.700 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 119,626 | 1.196 | 20 | 50 | fits | 106,554 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 603,866 | 6.039 | 20 | 50 | fits | 126,388 | 98 | 0.601 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 244,936 | 2.449 | 18 | 18 | fits | 125,765 | 106 | 0.692 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if1` | 1,568,165 | 15.682 | 18 | 18 | fits | 31,203 | 15 | 0.757 |
| an event behind 15 others | `backlog.event.if0` | 140,443 | 1.404 | 20 | 200 | fits | 107,328 | 125 | 0.527 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 632,756 | 6.328 | 20 | 20 | fits | 92,323 | 46 | 0.665 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 128,975 | 1.290 | 20 | 200 | fits | 129,183 | 143 | 0.531 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 512,002 | 5.120 | 20 | 200 | fits | 123,782 | 57 | 0.689 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 124,716 | 1.247 | 20 | 20 | fits | 129,183 | 143 | 0.531 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 694,156 | 6.942 | 20 | 20 | fits | 92,323 | 46 | 0.665 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 128,301 | 1.283 | 20 | 24 | fits | 129,183 | 143 | 0.531 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,163,236 | 11.632 | 20 | 24 | fits | 47,203 | 31 | 0.683 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 127,261 | 1.273 | 20 | 50 | fits | 129,183 | 143 | 0.531 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 510,507 | 5.105 | 20 | 50 | fits | 123,782 | 57 | 0.689 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 510,442 | 5.104 | 18 | 18 | fits | 123,782 | 57 | 0.689 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,283,622 | 12.836 | 18 | 18 | fits | 29,747 | 15 | 0.745 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 500,746 | 5.007 | 20 | 20 | fits | 125,035 | 58 | 0.690 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 99,817 | 0.998 | 20 | 200 | fits | 104,499 | 140 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 616,101 | 6.161 | 20 | 200 | fits | 125,035 | 58 | 0.690 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 100,729 | 1.007 | 20 | 20 | fits | 104,499 | 140 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 819,105 | 8.191 | 20 | 20 | fits | 87,392 | 39 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 104,314 | 1.043 | 20 | 24 | fits | 104,499 | 140 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,355,052 | 13.551 | 20 | 24 | fits | 59,070 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 103,274 | 1.033 | 20 | 50 | fits | 104,499 | 140 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 494,742 | 4.947 | 20 | 50 | fits | 96,007 | 65 | 0.716 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 248,249 | 2.482 | 18 | 18 | fits | 145,430 | 137 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,468,421 | 14.684 | 18 | 18 | fits | 31,305 | 16 | 0.745 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,480 | 0.085 | 20 | 20 | fits | 40,799 | 21 | 0.764 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 99,817 | 0.998 | 20 | 200 | fits | 104,499 | 140 | 0.501 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 40,643 | 0.406 | 20 | 200 | fits | 40,799 | 21 | 0.764 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 100,729 | 1.007 | 20 | 20 | fits | 104,499 | 140 | 0.501 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 799,637 | 7.996 | 20 | 20 | fits | 87,399 | 39 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 104,314 | 1.043 | 20 | 24 | fits | 104,499 | 140 | 0.501 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,337,501 | 13.375 | 20 | 24 | fits | 59,070 | 31 | 0.703 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 103,274 | 1.033 | 20 | 50 | fits | 104,499 | 140 | 0.501 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 494,742 | 4.947 | 20 | 50 | fits | 96,007 | 65 | 0.716 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 248,249 | 2.482 | 18 | 18 | fits | 145,430 | 137 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,450,336 | 14.503 | 18 | 18 | fits | 40,690 | 26 | 0.763 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,355,950 | 63.559 | 20 | 20 | MISS ceiling | 47,279 | 27 | 0.584 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,044,713 | 360.447 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,044,638 | 360.446 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,044,563 | 360.446 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,044,488 | 360.445 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 102,474 | 1.025 | 20 | 200 | fits | 102,750 | 134 | 0.505 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 568,509 | 5.685 | 20 | 200 | fits | 103,560 | 43 | 0.715 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 98,215 | 0.982 | 20 | 20 | fits | 102,750 | 134 | 0.505 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 720,539 | 7.205 | 20 | 20 | fits | 63,671 | 25 | 0.730 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 101,800 | 1.018 | 20 | 24 | fits | 102,750 | 134 | 0.505 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,478,391 | 64.784 | 20 | 24 | MISS ceiling | 28,592 | 23 | 0.539 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 100,760 | 1.008 | 20 | 50 | fits | 102,750 | 134 | 0.505 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 463,454 | 4.635 | 20 | 50 | fits | 145,047 | 91 | 0.669 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 318,342 | 3.183 | 18 | 18 | fits | 117,416 | 61 | 0.750 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,205,173 | 12.052 | 18 | 18 | fits | 30,533 | 17 | 0.720 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT

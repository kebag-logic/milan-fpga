### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 21 paths and 6 of 851 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.657 (3.990) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-6.adp_available.if0` (backlog-adp@program-aged2-6) | 4.412 (5.215) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.139 (0.408) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.943 (1.530) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.125 (62.294) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.267 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 4.418 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.811 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 6.062 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.871 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.611 | fits | 31 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.acmp.first.if0` (backlog-adp@blank-0) | 1.446 | fits | 0 acmp | 76 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.acmp.last.if0` (backlog-adp@program-aged2-6) | 6.568 | fits | 11 acmp | 76 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.adp.first.if0` (backlog-adp@blank-0) | 1.436 | fits | 0 adp | 76 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-6.service.adp.last.if0` (backlog-adp@program-aged2-6) | 5.200 | fits | 7 adp | 76 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 1.481 | fits | 0 aecp | 76 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.973 | MISS ceiling | 15 aecp | 76 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.maap.first.if0` (backlog-adp@blank-0) | 1.471 | fits | 0 maap | 76 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-0.service.maap.last.if0` (backlog-adp@blank-0) | 4.443 | fits | 6 maap | 76 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.957 | fits | 0 srp | 76 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.srp.last.if0` (backlog-adp@program-aged2-7) | 11.620 | fits | 31 srp | 76 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 12.360 | 18 | 110,871 (1.109) | yes | - |
| backlog-adp@blank-1 | 0 | 11.734 | 18 | 110,769 (1.108) | yes | - |
| backlog-adp@blank-2 | 0 | 11.784 | 19 | 110,769 (1.108) | yes | - |
| backlog-adp@blank-3 | 0 | 11.707 | 18 | 110,769 (1.108) | yes | - |
| backlog-adp@blank-4 | 0 | 11.771 | 19 | 110,769 (1.108) | yes | - |
| backlog-adp@blank-5 | 0 | 11.753 | 18 | 110,769 (1.108) | yes | - |
| backlog-adp@blank-6 | 0 | 11.806 | 19 | 110,769 (1.108) | yes | - |
| backlog-adp@blank-7 | 0 | 13.771 | 22 | 112,416 (1.124) | yes | - |
| backlog-adp@program-0 | 0 | 11.761 | 18 | 111,127 (1.111) | yes | - |
| backlog-adp@program-1 | 0 | 11.734 | 18 | 111,127 (1.111) | yes | - |
| backlog-adp@program-2 | 0 | 11.823 | 18 | 111,127 (1.111) | yes | - |
| backlog-adp@program-3 | 0 | 12.158 | 20 | 93,120 (0.931) | yes | - |
| backlog-adp@program-4 | 0 | 11.049 | 18 | 111,192 (1.112) | yes | - |
| backlog-adp@program-5 | 0 | 11.014 | 18 | 110,972 (1.110) | yes | - |
| backlog-adp@program-6 | 0 | 11.103 | 19 | 110,972 (1.110) | yes | - |
| backlog-adp@program-7 | 0 | 11.083 | 19 | 93,120 (0.931) | yes | - |
| backlog-adp@verify-0 | 0 | 12.364 | 18 | 111,022 (1.110) | yes | - |
| backlog-adp@verify-1 | 0 | 11.731 | 18 | 111,078 (1.111) | yes | - |
| backlog-adp@verify-2 | 0 | 11.716 | 18 | 111,078 (1.111) | yes | - |
| backlog-adp@verify-3 | 0 | 11.704 | 18 | 111,078 (1.111) | yes | - |
| backlog-adp@verify-4 | 0 | 11.768 | 19 | 111,078 (1.111) | yes | - |
| backlog-adp@verify-5 | 0 | 11.810 | 19 | 111,078 (1.111) | yes | - |
| backlog-adp@verify-6 | 0 | 11.807 | 19 | 111,078 (1.111) | yes | - |
| backlog-adp@verify-7 | 0 | 12.756 | 19 | 93,257 (0.933) | yes | - |
| backlog-adp@blank-aged2-0 | 0 | 12.201 | 19 | 110,969 (1.110) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.771 | 19 | 110,925 (1.109) | yes | - |
| backlog-adp@blank-aged2-2 | 1 | 11.658 | 17 | 111,903 (1.119) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 11.705 | 18 | 110,852 (1.109) | yes | - |
| backlog-adp@blank-aged2-4 | 1 | 11.727 | 17 | 111,830 (1.118) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.835 | 19 | 110,925 (1.109) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 11.739 | 18 | 110,852 (1.109) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 12.569 | 18 | 93,376 (0.934) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 12.669 | 20 | 113,185 (1.132) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 12.695 | 21 | 113,152 (1.132) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.669 | 20 | 113,502 (1.135) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 12.622 | 20 | 113,185 (1.132) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 12.731 | 20 | 113,184 (1.132) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 12.765 | 21 | 113,486 (1.135) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 13.649 | 21 | 120,051 (1.201) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 12.810 | 21 | 94,169 (0.942) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.764 | 18 | 110,922 (1.109) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.797 | 18 | 111,900 (1.119) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.766 | 18 | 110,995 (1.110) | yes | - |
| backlog-adp@program-aged2-3 | 1 | 11.726 | 17 | 111,973 (1.120) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 11.818 | 18 | 110,922 (1.109) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 11.843 | 18 | 111,900 (1.119) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 11.834 | 18 | 110,995 (1.110) | yes | - |
| backlog-adp@program-aged2-7 | 1 | 12.008 | 19 | 93,105 (0.931) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 11.707 | 17 | 111,973 (1.120) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.805 | 19 | 110,922 (1.109) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 11.702 | 17 | 111,900 (1.119) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 11.735 | 18 | 110,995 (1.110) | yes | - |
| backlog-adp@program-aged1-4 | 1 | 11.765 | 17 | 111,973 (1.120) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.867 | 19 | 110,922 (1.109) | yes | - |
| backlog-adp@program-aged1-6 | 1 | 11.771 | 17 | 111,900 (1.119) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 11.824 | 19 | 92,826 (0.928) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.718 | 18 | 111,028 (1.110) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 11.754 | 18 | 112,006 (1.120) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.720 | 18 | 110,955 (1.110) | yes | - |
| backlog-adp@verify-aged2-3 | 1 | 11.675 | 17 | 111,933 (1.119) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 11.771 | 18 | 111,028 (1.110) | yes | - |
| backlog-adp@verify-aged2-5 | 1 | 11.797 | 18 | 112,006 (1.120) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 11.792 | 18 | 110,955 (1.110) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 12.680 | 19 | 93,684 (0.937) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 11.659 | 17 | 111,933 (1.119) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.759 | 19 | 111,028 (1.110) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 11.658 | 17 | 112,006 (1.120) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 11.689 | 18 | 110,955 (1.110) | yes | - |
| backlog-adp@verify-aged1-4 | 1 | 11.714 | 17 | 111,933 (1.119) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.821 | 19 | 111,028 (1.110) | yes | - |
| backlog-adp@verify-aged1-6 | 1 | 11.725 | 17 | 112,006 (1.120) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 11.781 | 19 | 92,954 (0.930) | yes | - |
| backlog | 0 | 7.097 | 19 | 85,109 (0.851) | yes | - |
| backlog-adp | 0 | 10.912 | 18 | 110,920 (1.109) | yes | - |
| backlog-adp-refill | 0 | 40.686 | 24 | 110,920 (1.109) | yes | - |
| backlog-owed | 0 | 360.318 | 66 | 108,769 (1.088) | yes | - |

Composed maximum over the 4 backlog windows: 110,920 CPU cycles (1.109 ms), backlog-adp.
Over the windows that released their whole load only: 110,920 (1.109 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 81198 | 0 | 47,525 (0.475) | fits |
| backlog-adp@blank-0 | 336 | 0 | 110,871 (1.109) | fits |
| backlog-adp@blank-1 | 336 | 0 | 110,769 (1.108) | fits |
| backlog-adp@blank-2 | 337 | 0 | 110,769 (1.108) | fits |
| backlog-adp@blank-3 | 336 | 0 | 110,769 (1.108) | fits |
| backlog-adp@blank-4 | 337 | 0 | 110,769 (1.108) | fits |
| backlog-adp@blank-5 | 336 | 0 | 110,769 (1.108) | fits |
| backlog-adp@blank-6 | 337 | 0 | 110,769 (1.108) | fits |
| backlog-adp@blank-7 | 340 | 0 | 112,416 (1.124) | fits |
| backlog-adp@program-0 | 367 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-1 | 367 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-2 | 368 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-3 | 369 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-4 | 369 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-5 | 368 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-6 | 369 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-7 | 369 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-0 | 394 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-1 | 394 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-2 | 394 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-3 | 394 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-4 | 395 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-5 | 395 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-6 | 395 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-7 | 396 | 0 | 112,418 (1.124) | fits |
| backlog-adp@blank-aged2-0 | 870 | 0 | 110,969 (1.110) | fits |
| backlog-adp@blank-aged2-1 | 879 | 0 | 110,925 (1.109) | fits |
| backlog-adp@blank-aged2-2 | 891 | 0 | 111,903 (1.119) | fits |
| backlog-adp@blank-aged2-3 | 905 | 0 | 110,852 (1.109) | fits |
| backlog-adp@blank-aged2-4 | 918 | 0 | 111,830 (1.118) | fits |
| backlog-adp@blank-aged2-5 | 933 | 0 | 110,925 (1.109) | fits |
| backlog-adp@blank-aged2-6 | 945 | 0 | 110,852 (1.109) | fits |
| backlog-adp@blank-aged2-7 | 959 | 0 | 93,376 (0.934) | fits |
| backlog-adp@blank-aged1-0 | 768 | 0 | 113,185 (1.132) | fits |
| backlog-adp@blank-aged1-1 | 782 | 0 | 113,152 (1.132) | fits |
| backlog-adp@blank-aged1-2 | 795 | 0 | 113,502 (1.135) | fits |
| backlog-adp@blank-aged1-3 | 808 | 0 | 113,185 (1.132) | fits |
| backlog-adp@blank-aged1-4 | 822 | 0 | 113,184 (1.132) | fits |
| backlog-adp@blank-aged1-5 | 836 | 0 | 113,486 (1.135) | fits |
| backlog-adp@blank-aged1-6 | 850 | 0 | 120,051 (1.201) | fits |
| backlog-adp@blank-aged1-7 | 863 | 0 | 94,169 (0.942) | fits |
| backlog-adp@program-aged2-0 | 896 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged2-1 | 910 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged2-2 | 923 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged2-3 | 936 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged2-4 | 950 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged2-5 | 964 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged2-6 | 977 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged2-7 | 992 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged1-0 | 788 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged1-1 | 803 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged1-2 | 815 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged1-3 | 829 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged1-4 | 842 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged1-5 | 857 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged1-6 | 869 | 0 | 112,418 (1.124) | fits |
| backlog-adp@program-aged1-7 | 884 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged2-0 | 918 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged2-1 | 932 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged2-2 | 945 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged2-3 | 958 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged2-4 | 972 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged2-5 | 986 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged2-6 | 999 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged2-7 | 1014 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged1-0 | 810 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged1-1 | 825 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged1-2 | 837 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged1-3 | 851 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged1-4 | 864 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged1-5 | 879 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged1-6 | 891 | 0 | 112,418 (1.124) | fits |
| backlog-adp@verify-aged1-7 | 906 | 0 | 112,418 (1.124) | fits |
| save-held | 3429 | 0 | 112,650 (1.127) | fits |
| save-starved | 42843 | 0 | 92,180 (0.922) | fits |
| save | 610 | 0 | 111,800 (1.118) | fits |
| backlog | 298 | 0 | 85,109 (0.851) | fits |
| backlog-adp | 306 | 0 | 110,920 (1.109) | fits |
| backlog-adp-refill | 312 | 0 | 110,920 (1.109) | fits |
| backlog-owed | 356 | 0 | 108,769 (1.088) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | +9.933 ms, 77,539 (0.775 ms), read-back | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 11.377 (18) | 6.623 |
| backlog-adp@blank-aged2-1 | 2 | +8.752 ms, 77,629 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 11.433 (18) | 6.567 |
| backlog-adp@blank-aged2-2 | 2 | +7.464 ms, 77,539 (0.775 ms), read-back | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 11.316 (18) | 6.684 |
| backlog-adp@blank-aged2-3 | 2 | +6.192 ms, 77,539 (0.775 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 11.367 (18) | 6.633 |
| backlog-adp@blank-aged2-4 | 2 | +5.080 ms, 77,395 (0.774 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 11.390 (18) | 6.610 |
| backlog-adp@blank-aged2-5 | 2 | +4.276 ms, 77,327 (0.773 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.497 (18) | 6.503 |
| backlog-adp@blank-aged2-6 | 2 | +2.596 ms, 77,629 (0.776 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 11.401 (18) | 6.599 |
| backlog-adp@blank-aged2-7 | 2 | +1.687 ms, 77,691 (0.777 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 11.469 (18) | 6.531 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 10.688 (18) | 7.312 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 10.715 (18) | 7.285 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.684 (18) | 7.316 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.641 (18) | 7.359 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 10.753 (18) | 7.247 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.782 (18) | 7.218 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 10.767 (18) | 7.233 |
| backlog-adp@blank-aged1-7 | 1 | none | +10.854 ms, 77,050 (0.770 ms), read-back | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.687 (18) | 7.313 |
| backlog-adp@program-aged2-0 | 2 | +9.925 ms, 83,079 (0.831 ms), issue | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 11.426 (18) | 6.574 |
| backlog-adp@program-aged2-1 | 2 | +8.719 ms, 83,169 (0.832 ms), issue | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 11.458 (18) | 6.542 |
| backlog-adp@program-aged2-2 | 2 | +7.512 ms, 83,079 (0.831 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 11.424 (18) | 6.576 |
| backlog-adp@program-aged2-3 | 2 | +6.154 ms, 83,079 (0.831 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 11.388 (18) | 6.612 |
| backlog-adp@program-aged2-4 | 2 | +5.129 ms, 83,025 (0.830 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 11.480 (18) | 6.520 |
| backlog-adp@program-aged2-5 | 2 | +4.230 ms, 82,792 (0.828 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 11.505 (18) | 6.495 |
| backlog-adp@program-aged2-6 | 2 | +2.636 ms, 83,154 (0.832 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 11.496 (18) | 6.504 |
| backlog-adp@program-aged2-7 | 2 | +2.321 ms, 83,253 (0.833 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 11.620 (18) | 6.380 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 10.554 (18) | 7.446 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 10.652 (18) | 7.348 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 10.547 (18) | 7.453 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 10.582 (18) | 7.418 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 10.614 (18) | 7.386 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.713 (18) | 7.287 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 10.617 (18) | 7.383 |
| backlog-adp@program-aged1-7 | 1 | none | +10.791 ms, 82,590 (0.826 ms), issue | `backlog-adp@program-aged1-7.service.srp.last.if0` | 10.624 (18) | 7.376 |
| backlog-adp@verify-aged2-0 | 2 | +9.927 ms, 78,211 (0.782 ms), read-back | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 11.380 (18) | 6.620 |
| backlog-adp@verify-aged2-1 | 2 | +8.725 ms, 78,301 (0.783 ms), read-back | none | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 11.415 (18) | 6.585 |
| backlog-adp@verify-aged2-2 | 2 | +7.516 ms, 78,211 (0.782 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 11.378 (18) | 6.622 |
| backlog-adp@verify-aged2-3 | 2 | +6.151 ms, 78,211 (0.782 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 11.336 (18) | 6.664 |
| backlog-adp@verify-aged2-4 | 2 | +5.132 ms, 78,157 (0.782 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 11.433 (18) | 6.567 |
| backlog-adp@verify-aged2-5 | 2 | +4.232 ms, 77,999 (0.780 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.458 (18) | 6.542 |
| backlog-adp@verify-aged2-6 | 2 | +2.641 ms, 78,211 (0.782 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 11.454 (18) | 6.546 |
| backlog-adp@verify-aged2-7 | 2 | +2.320 ms, 78,363 (0.784 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 11.576 (18) | 6.424 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 10.556 (18) | 7.444 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 10.654 (18) | 7.346 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 10.551 (18) | 7.449 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 10.586 (18) | 7.414 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 10.611 (18) | 7.389 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.716 (18) | 7.284 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 10.620 (18) | 7.380 |
| backlog-adp@verify-aged1-7 | 1 | none | +10.797 ms, 77,722 (0.777 ms), read-back | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 10.631 (18) | 7.369 |

Least margin over the aged windows: 6.380 ms, `backlog-adp@program-aged2-7.service.srp.last.if0` at 11.620 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6029.855 | 6,070 | 102 | 2 | 30.937 | yes | within |
| save-held | 2018.303 | 4,070 | 102 | - | 14.275 | no | within |
| save-starved | 4048.191 | 4,070 | 102 | - | 31.119 | yes | within |
| save | 2018.527 | 4,070 | 102 | - | 10.988 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 520 | 96,696 (0.967) | 95,399 (0.954) |
| backlog-adp@blank-0 | 299 | 87,748 (0.877) | 76,321 (0.763) |
| backlog-adp@blank-1 | 299 | 87,748 (0.877) | 76,321 (0.763) |
| backlog-adp@blank-2 | 299 | 87,826 (0.878) | 76,321 (0.763) |
| backlog-adp@blank-3 | 299 | 87,996 (0.880) | 76,321 (0.763) |
| backlog-adp@blank-4 | 299 | 87,826 (0.878) | 76,321 (0.763) |
| backlog-adp@blank-5 | 299 | 87,991 (0.880) | 76,379 (0.764) |
| backlog-adp@blank-6 | 299 | 87,884 (0.879) | 76,379 (0.764) |
| backlog-adp@blank-7 | 300 | 112,416 (1.124) | 76,379 (0.764) |
| backlog-adp@program-0 | 328 | 112,418 (1.124) | 81,855 (0.819) |
| backlog-adp@program-1 | 328 | 112,418 (1.124) | 81,855 (0.819) |
| backlog-adp@program-2 | 328 | 112,418 (1.124) | 81,855 (0.819) |
| backlog-adp@program-3 | 329 | 112,418 (1.124) | 81,937 (0.819) |
| backlog-adp@program-4 | 329 | 112,418 (1.124) | 80,779 (0.808) |
| backlog-adp@program-5 | 329 | 112,418 (1.124) | 80,779 (0.808) |
| backlog-adp@program-6 | 329 | 112,418 (1.124) | 80,779 (0.808) |
| backlog-adp@program-7 | 329 | 112,418 (1.124) | 80,779 (0.808) |
| backlog-adp@verify-0 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-1 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-2 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-3 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-4 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-5 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-6 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-7 | 356 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@blank-aged2-0 | 297 | 77,539 (0.775) | 76,290 (0.763) |
| backlog-adp@blank-aged2-1 | 297 | 77,629 (0.776) | 76,278 (0.763) |
| backlog-adp@blank-aged2-2 | 297 | 77,539 (0.775) | 76,290 (0.763) |
| backlog-adp@blank-aged2-3 | 297 | 77,539 (0.775) | 76,290 (0.763) |
| backlog-adp@blank-aged2-4 | 297 | 77,395 (0.774) | 76,323 (0.763) |
| backlog-adp@blank-aged2-5 | 297 | 77,327 (0.773) | 76,340 (0.763) |
| backlog-adp@blank-aged2-6 | 297 | 77,629 (0.776) | 76,278 (0.763) |
| backlog-adp@blank-aged2-7 | 298 | 87,828 (0.878) | 76,340 (0.763) |
| backlog-adp@blank-aged1-0 | 297 | 113,185 (1.132) | 76,334 (0.763) |
| backlog-adp@blank-aged1-1 | 297 | 113,152 (1.132) | 76,334 (0.763) |
| backlog-adp@blank-aged1-2 | 297 | 113,502 (1.135) | 76,334 (0.763) |
| backlog-adp@blank-aged1-3 | 297 | 113,185 (1.132) | 76,334 (0.763) |
| backlog-adp@blank-aged1-4 | 297 | 113,184 (1.132) | 76,334 (0.763) |
| backlog-adp@blank-aged1-5 | 297 | 113,486 (1.135) | 76,416 (0.764) |
| backlog-adp@blank-aged1-6 | 298 | 120,051 (1.201) | 76,416 (0.764) |
| backlog-adp@blank-aged1-7 | 297 | 77,050 (0.770) | 75,978 (0.760) |
| backlog-adp@program-aged2-0 | 326 | 112,418 (1.124) | 81,680 (0.817) |
| backlog-adp@program-aged2-1 | 326 | 112,418 (1.124) | 81,668 (0.817) |
| backlog-adp@program-aged2-2 | 326 | 112,418 (1.124) | 81,680 (0.817) |
| backlog-adp@program-aged2-3 | 326 | 112,418 (1.124) | 81,680 (0.817) |
| backlog-adp@program-aged2-4 | 326 | 112,418 (1.124) | 81,668 (0.817) |
| backlog-adp@program-aged2-5 | 326 | 112,418 (1.124) | 81,730 (0.817) |
| backlog-adp@program-aged2-6 | 326 | 112,418 (1.124) | 81,680 (0.817) |
| backlog-adp@program-aged2-7 | 327 | 112,418 (1.124) | 81,730 (0.817) |
| backlog-adp@program-aged1-0 | 326 | 112,418 (1.124) | 81,711 (0.817) |
| backlog-adp@program-aged1-1 | 326 | 112,418 (1.124) | 81,711 (0.817) |
| backlog-adp@program-aged1-2 | 326 | 112,418 (1.124) | 81,711 (0.817) |
| backlog-adp@program-aged1-3 | 326 | 112,418 (1.124) | 81,711 (0.817) |
| backlog-adp@program-aged1-4 | 326 | 112,418 (1.124) | 81,711 (0.817) |
| backlog-adp@program-aged1-5 | 326 | 112,418 (1.124) | 81,793 (0.818) |
| backlog-adp@program-aged1-6 | 326 | 112,418 (1.124) | 81,793 (0.818) |
| backlog-adp@program-aged1-7 | 326 | 112,418 (1.124) | 81,368 (0.814) |
| backlog-adp@verify-aged2-0 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged2-1 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged2-2 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged2-3 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged2-4 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged2-5 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged2-6 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged2-7 | 356 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged1-0 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged1-1 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged1-2 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged1-3 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged1-4 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged1-5 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged1-6 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| backlog-adp@verify-aged1-7 | 355 | 112,418 (1.124) | 95,418 (0.954) |
| save-held | 722 | 112,650 (1.127) | 95,466 (0.955) |
| save-starved | 418 | 97,287 (0.973) | 95,990 (0.960) |
| save | 585 | 111,800 (1.118) | 95,466 (0.955) |
| backlog | 265 | 46,592 (0.466) | 2,940 (0.029) |
| backlog-adp | 271 | 46,592 (0.466) | 2,940 (0.029) |
| backlog-adp-refill | 274 | 46,592 (0.466) | 2,940 (0.029) |
| backlog-owed | 306 | 46,592 (0.466) | 2,940 (0.029) |

Longest pass that carries a step: 120,051 CPU cycles (1.201 ms), backlog-adp@blank-aged1-6; longest step: 95,990 (0.960 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 354,918 | 3.549 | 20 | 20 | fits | 94,489 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 143,641 | 1.436 | 20 | 200 | fits | 79,392 | 135 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 440,659 | 4.407 | 20 | 200 | fits | 94,489 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 144,553 | 1.446 | 20 | 20 | fits | 79,392 | 135 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 589,264 | 5.893 | 20 | 20 | fits | 62,299 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 148,138 | 1.481 | 20 | 24 | fits | 79,392 | 135 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 1,105,406 | 11.054 | 20 | 24 | fits | 46,658 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 147,098 | 1.471 | 20 | 50 | fits | 79,392 | 135 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 444,335 | 4.443 | 20 | 50 | fits | 94,489 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 257,514 | 2.575 | 18 | 18 | fits | 110,871 | 138 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 1,126,249 | 11.262 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 292,233 | 2.922 | 20 | 20 | fits | 94,533 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 81,039 | 0.810 | 20 | 200 | fits | 79,153 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 378,018 | 3.780 | 20 | 200 | fits | 94,533 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 81,951 | 0.820 | 20 | 20 | fits | 79,153 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 526,655 | 5.267 | 20 | 20 | fits | 62,299 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 85,536 | 0.855 | 20 | 24 | fits | 79,153 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 1,042,780 | 10.428 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 84,496 | 0.845 | 20 | 50 | fits | 79,153 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 381,694 | 3.817 | 20 | 50 | fits | 94,533 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 194,810 | 1.948 | 18 | 18 | fits | 110,769 | 138 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,063,623 | 10.636 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 291,203 | 2.912 | 20 | 20 | fits | 94,533 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 80,009 | 0.800 | 20 | 200 | fits | 79,153 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 376,988 | 3.770 | 20 | 200 | fits | 94,533 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 80,921 | 0.809 | 20 | 20 | fits | 79,153 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 525,625 | 5.256 | 20 | 20 | fits | 62,299 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 84,506 | 0.845 | 20 | 24 | fits | 79,153 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 1,017,825 | 10.178 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 83,466 | 0.835 | 20 | 50 | fits | 79,153 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 380,664 | 3.807 | 20 | 50 | fits | 94,533 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 193,780 | 1.938 | 18 | 18 | fits | 110,769 | 138 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 1,068,468 | 10.685 | 18 | 18 | fits | 22,059 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 290,173 | 2.902 | 20 | 20 | fits | 94,533 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 78,979 | 0.790 | 20 | 200 | fits | 79,153 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 375,958 | 3.760 | 20 | 200 | fits | 94,533 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 79,891 | 0.799 | 20 | 20 | fits | 79,153 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 524,595 | 5.246 | 20 | 20 | fits | 62,299 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 83,476 | 0.835 | 20 | 24 | fits | 79,153 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 1,032,011 | 10.320 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 82,436 | 0.824 | 20 | 50 | fits | 79,153 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 379,634 | 3.796 | 20 | 50 | fits | 94,533 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 192,750 | 1.927 | 18 | 18 | fits | 110,769 | 138 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 1,060,595 | 10.606 | 18 | 18 | fits | 31,119 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 289,143 | 2.891 | 20 | 20 | fits | 94,533 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 77,949 | 0.779 | 20 | 200 | fits | 79,153 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 374,928 | 3.749 | 20 | 200 | fits | 94,533 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 78,861 | 0.789 | 20 | 20 | fits | 79,153 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 501,448 | 5.014 | 20 | 20 | fits | 40,182 | 24 | 0.675 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 82,446 | 0.824 | 20 | 24 | fits | 79,153 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 1,016,615 | 10.166 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 81,406 | 0.814 | 20 | 50 | fits | 79,153 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 378,604 | 3.786 | 20 | 50 | fits | 94,533 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 191,720 | 1.917 | 18 | 18 | fits | 110,769 | 138 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 1,067,258 | 10.673 | 18 | 18 | fits | 22,059 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 288,113 | 2.881 | 20 | 20 | fits | 86,853 | 77 | 0.655 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 76,919 | 0.769 | 20 | 200 | fits | 79,153 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 366,218 | 3.662 | 20 | 200 | fits | 86,853 | 77 | 0.655 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 77,831 | 0.778 | 20 | 20 | fits | 79,153 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 563,679 | 5.637 | 20 | 20 | fits | 62,941 | 35 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 81,416 | 0.814 | 20 | 24 | fits | 79,153 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 1,036,491 | 10.365 | 20 | 24 | fits | 47,003 | 29 | 0.712 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 80,376 | 0.804 | 20 | 50 | fits | 79,153 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 369,894 | 3.699 | 20 | 50 | fits | 86,853 | 77 | 0.655 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 190,690 | 1.907 | 18 | 18 | fits | 110,769 | 138 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,065,161 | 10.652 | 18 | 18 | fits | 31,205 | 19 | 0.753 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 331,902 | 3.319 | 20 | 20 | fits | 86,396 | 55 | 0.686 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 75,889 | 0.759 | 20 | 200 | fits | 79,153 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 410,696 | 4.107 | 20 | 200 | fits | 86,396 | 55 | 0.686 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 76,801 | 0.768 | 20 | 20 | fits | 79,153 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 547,680 | 5.477 | 20 | 20 | fits | 51,300 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 80,386 | 0.804 | 20 | 24 | fits | 79,153 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 1,019,664 | 10.197 | 20 | 24 | fits | 46,791 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 79,346 | 0.793 | 20 | 50 | fits | 79,153 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 327,976 | 3.280 | 20 | 50 | fits | 68,781 | 62 | 0.695 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 189,660 | 1.897 | 18 | 18 | fits | 110,769 | 138 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 1,070,615 | 10.706 | 18 | 18 | fits | 22,213 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 329,490 | 3.295 | 20 | 20 | fits | 86,109 | 55 | 0.684 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 74,859 | 0.749 | 20 | 200 | fits | 79,153 | 135 | 0.513 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 407,997 | 4.080 | 20 | 200 | fits | 86,109 | 55 | 0.684 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 75,771 | 0.758 | 20 | 20 | fits | 79,153 | 135 | 0.513 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 544,600 | 5.446 | 20 | 20 | fits | 51,262 | 26 | 0.783 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 79,356 | 0.794 | 20 | 24 | fits | 79,153 | 135 | 0.513 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 1,016,815 | 10.168 | 20 | 24 | fits | 46,791 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 78,316 | 0.783 | 20 | 50 | fits | 79,153 | 135 | 0.513 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 325,564 | 3.256 | 20 | 50 | fits | 93,046 | 96 | 0.603 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 232,453 | 2.325 | 18 | 18 | fits | 79,484 | 62 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 1,067,766 | 10.678 | 18 | 18 | fits | 22,213 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 289,491 | 2.895 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 78,062 | 0.781 | 20 | 200 | fits | 79,232 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 375,146 | 3.751 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 78,974 | 0.790 | 20 | 20 | fits | 79,232 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 523,596 | 5.236 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 82,559 | 0.826 | 20 | 24 | fits | 79,232 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 1,039,832 | 10.398 | 20 | 24 | fits | 46,658 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 81,519 | 0.815 | 20 | 50 | fits | 79,232 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 378,822 | 3.788 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 192,191 | 1.922 | 18 | 18 | fits | 111,127 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 1,060,675 | 10.607 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 287,431 | 2.874 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 76,002 | 0.760 | 20 | 200 | fits | 79,232 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 373,086 | 3.731 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 76,914 | 0.769 | 20 | 20 | fits | 79,232 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 521,536 | 5.215 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 80,499 | 0.805 | 20 | 24 | fits | 79,232 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 1,029,063 | 10.291 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 79,459 | 0.795 | 20 | 50 | fits | 79,232 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 376,762 | 3.768 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 190,131 | 1.901 | 18 | 18 | fits | 111,127 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 1,057,647 | 10.576 | 18 | 18 | fits | 31,119 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 285,371 | 2.854 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 73,942 | 0.739 | 20 | 200 | fits | 79,232 | 135 | 0.515 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 371,026 | 3.710 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 74,854 | 0.749 | 20 | 20 | fits | 79,232 | 135 | 0.515 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 544,617 | 5.446 | 20 | 20 | fits | 63,365 | 35 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 78,439 | 0.784 | 20 | 24 | fits | 79,232 | 135 | 0.515 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 1,015,920 | 10.159 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 77,399 | 0.774 | 20 | 50 | fits | 79,232 | 135 | 0.515 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 374,702 | 3.747 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 188,071 | 1.881 | 18 | 18 | fits | 111,127 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 1,066,887 | 10.669 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 335,568 | 3.356 | 20 | 20 | fits | 86,119 | 55 | 0.684 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 80,874 | 0.809 | 20 | 200 | fits | 79,369 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 414,085 | 4.141 | 20 | 200 | fits | 86,119 | 55 | 0.684 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 81,786 | 0.818 | 20 | 20 | fits | 79,369 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 550,767 | 5.508 | 20 | 20 | fits | 51,229 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 85,371 | 0.854 | 20 | 24 | fits | 79,369 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 1,022,503 | 10.225 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 84,331 | 0.843 | 20 | 50 | fits | 79,369 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 331,642 | 3.316 | 20 | 50 | fits | 93,120 | 96 | 0.605 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 238,457 | 2.385 | 18 | 18 | fits | 79,430 | 62 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 1,073,470 | 10.735 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 319,483 | 3.195 | 20 | 20 | fits | 87,461 | 58 | 0.670 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 113,704 | 1.137 | 20 | 200 | fits | 78,968 | 137 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 398,196 | 3.982 | 20 | 200 | fits | 87,461 | 58 | 0.670 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 114,616 | 1.146 | 20 | 20 | fits | 78,968 | 137 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 546,113 | 5.461 | 20 | 20 | fits | 62,304 | 33 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 39,233 | 0.392 | 20 | 24 | fits | 40,522 | 63 | 0.598 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 1,007,674 | 10.077 | 20 | 24 | fits | 46,857 | 29 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 38,193 | 0.382 | 20 | 50 | fits | 40,522 | 63 | 0.598 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 314,411 | 3.144 | 20 | 50 | fits | 86,448 | 74 | 0.632 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 227,898 | 2.279 | 18 | 18 | fits | 111,192 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 1,065,945 | 10.659 | 18 | 18 | fits | 29,687 | 17 | 0.728 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 292,189 | 2.922 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 80,915 | 0.809 | 20 | 200 | fits | 79,358 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 377,844 | 3.778 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 81,827 | 0.818 | 20 | 20 | fits | 79,358 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 526,294 | 5.263 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 85,412 | 0.854 | 20 | 24 | fits | 79,358 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 1,033,821 | 10.338 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 84,372 | 0.844 | 20 | 50 | fits | 79,358 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 381,520 | 3.815 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 194,889 | 1.949 | 18 | 18 | fits | 110,972 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,062,405 | 10.624 | 18 | 18 | fits | 31,119 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 290,129 | 2.901 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 78,855 | 0.789 | 20 | 200 | fits | 79,358 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 375,784 | 3.758 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 79,767 | 0.798 | 20 | 20 | fits | 79,358 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 549,375 | 5.494 | 20 | 20 | fits | 63,365 | 35 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 83,352 | 0.834 | 20 | 24 | fits | 79,358 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 1,020,678 | 10.207 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 82,312 | 0.823 | 20 | 50 | fits | 79,358 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 379,460 | 3.795 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 192,829 | 1.928 | 18 | 18 | fits | 110,972 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 1,071,645 | 10.716 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 331,339 | 3.313 | 20 | 20 | fits | 86,119 | 55 | 0.684 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 76,795 | 0.768 | 20 | 200 | fits | 79,358 | 135 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 409,856 | 4.099 | 20 | 200 | fits | 86,119 | 55 | 0.684 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 77,707 | 0.777 | 20 | 20 | fits | 79,358 | 135 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 546,538 | 5.465 | 20 | 20 | fits | 51,229 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 81,292 | 0.813 | 20 | 24 | fits | 79,358 | 135 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 1,018,274 | 10.183 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 80,252 | 0.803 | 20 | 50 | fits | 79,358 | 135 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 327,413 | 3.274 | 20 | 50 | fits | 93,120 | 96 | 0.605 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 234,228 | 2.342 | 18 | 18 | fits | 79,430 | 62 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 1,069,241 | 10.692 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 354,840 | 3.548 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 143,475 | 1.435 | 20 | 200 | fits | 79,669 | 135 | 0.519 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 440,495 | 4.405 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 144,387 | 1.444 | 20 | 20 | fits | 79,669 | 135 | 0.519 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 588,913 | 5.889 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 147,972 | 1.480 | 20 | 24 | fits | 79,669 | 135 | 0.519 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 1,105,227 | 11.052 | 20 | 24 | fits | 46,658 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 146,932 | 1.469 | 20 | 50 | fits | 79,669 | 135 | 0.519 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 444,171 | 4.442 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 257,499 | 2.575 | 18 | 18 | fits | 111,022 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 1,126,070 | 11.261 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 291,749 | 2.917 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 80,369 | 0.804 | 20 | 200 | fits | 79,086 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 377,404 | 3.774 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 81,281 | 0.813 | 20 | 20 | fits | 79,086 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 525,854 | 5.259 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 84,866 | 0.849 | 20 | 24 | fits | 79,086 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 1,041,928 | 10.419 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 83,826 | 0.838 | 20 | 50 | fits | 79,086 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 381,080 | 3.811 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 194,449 | 1.944 | 18 | 18 | fits | 111,078 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 1,062,771 | 10.628 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 290,719 | 2.907 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 79,339 | 0.793 | 20 | 200 | fits | 79,086 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 376,374 | 3.764 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 80,251 | 0.803 | 20 | 20 | fits | 79,086 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 524,824 | 5.248 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 83,836 | 0.838 | 20 | 24 | fits | 79,086 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 1,040,412 | 10.404 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 82,796 | 0.828 | 20 | 50 | fits | 79,086 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 380,050 | 3.800 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 193,419 | 1.934 | 18 | 18 | fits | 111,078 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 1,061,255 | 10.613 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 289,689 | 2.897 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 78,309 | 0.783 | 20 | 200 | fits | 79,086 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 375,344 | 3.753 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 79,221 | 0.792 | 20 | 20 | fits | 79,086 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 523,794 | 5.238 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 82,806 | 0.828 | 20 | 24 | fits | 79,086 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 1,031,159 | 10.312 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 81,766 | 0.818 | 20 | 50 | fits | 79,086 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 379,020 | 3.790 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 192,389 | 1.924 | 18 | 18 | fits | 111,078 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 1,059,743 | 10.597 | 18 | 18 | fits | 31,119 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 288,659 | 2.887 | 20 | 20 | fits | 94,403 | 81 | 0.643 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 77,279 | 0.773 | 20 | 200 | fits | 79,086 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 374,314 | 3.743 | 20 | 200 | fits | 94,403 | 81 | 0.643 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 78,191 | 0.782 | 20 | 20 | fits | 79,086 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 500,647 | 5.006 | 20 | 20 | fits | 40,149 | 24 | 0.673 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 81,776 | 0.818 | 20 | 24 | fits | 79,086 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 1,015,749 | 10.157 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 80,736 | 0.807 | 20 | 50 | fits | 79,086 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 377,990 | 3.780 | 20 | 50 | fits | 94,403 | 81 | 0.643 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 191,359 | 1.914 | 18 | 18 | fits | 111,078 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 1,066,392 | 10.664 | 18 | 18 | fits | 22,059 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 287,629 | 2.876 | 20 | 20 | fits | 72,136 | 72 | 0.606 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 76,249 | 0.762 | 20 | 200 | fits | 79,086 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 351,017 | 3.510 | 20 | 200 | fits | 72,136 | 72 | 0.606 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 77,161 | 0.772 | 20 | 20 | fits | 79,086 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 547,070 | 5.471 | 20 | 20 | fits | 62,970 | 35 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 80,746 | 0.807 | 20 | 24 | fits | 79,086 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 1,019,617 | 10.196 | 20 | 24 | fits | 46,881 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 79,706 | 0.797 | 20 | 50 | fits | 79,086 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 354,693 | 3.547 | 20 | 50 | fits | 72,136 | 72 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 190,329 | 1.903 | 18 | 18 | fits | 111,078 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,070,524 | 10.705 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 331,713 | 3.317 | 20 | 20 | fits | 86,415 | 55 | 0.686 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 75,219 | 0.752 | 20 | 200 | fits | 79,086 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 410,526 | 4.105 | 20 | 200 | fits | 86,415 | 55 | 0.686 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 76,131 | 0.761 | 20 | 20 | fits | 79,086 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 547,521 | 5.475 | 20 | 20 | fits | 51,267 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 79,716 | 0.797 | 20 | 24 | fits | 79,086 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 1,019,174 | 10.192 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 78,676 | 0.787 | 20 | 50 | fits | 79,086 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 327,787 | 3.278 | 20 | 50 | fits | 68,862 | 62 | 0.696 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 189,299 | 1.893 | 18 | 18 | fits | 111,078 | 138 | 0.612 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 1,070,141 | 10.701 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 329,209 | 3.292 | 20 | 20 | fits | 86,179 | 55 | 0.684 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 74,189 | 0.742 | 20 | 200 | fits | 79,086 | 135 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 407,786 | 4.078 | 20 | 200 | fits | 86,179 | 55 | 0.684 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 75,101 | 0.751 | 20 | 20 | fits | 79,086 | 135 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 544,468 | 5.445 | 20 | 20 | fits | 51,229 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 78,686 | 0.787 | 20 | 24 | fits | 79,086 | 135 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 1,016,204 | 10.162 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 77,646 | 0.776 | 20 | 50 | fits | 79,086 | 135 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 325,283 | 3.253 | 20 | 50 | fits | 93,257 | 96 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 231,961 | 2.320 | 18 | 18 | fits | 79,471 | 62 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 1,067,171 | 10.672 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 288,464 | 2.885 | 20 | 20 | fits | 94,531 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 77,054 | 0.771 | 20 | 200 | fits | 80,708 | 132 | 0.532 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 374,255 | 3.743 | 20 | 200 | fits | 94,531 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 77,966 | 0.780 | 20 | 20 | fits | 80,708 | 132 | 0.532 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 522,801 | 5.228 | 20 | 20 | fits | 62,258 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 81,551 | 0.816 | 20 | 24 | fits | 80,708 | 132 | 0.532 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 1,116,907 | 11.169 | 20 | 24 | fits | 47,182 | 29 | 0.714 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 80,511 | 0.805 | 20 | 50 | fits | 80,708 | 132 | 0.532 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 377,931 | 3.779 | 20 | 50 | fits | 94,531 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 191,025 | 1.910 | 18 | 18 | fits | 110,969 | 138 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 1,137,742 | 11.377 | 18 | 18 | fits | 23,370 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 288,504 | 2.885 | 20 | 20 | fits | 94,377 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 77,295 | 0.773 | 20 | 200 | fits | 77,684 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 374,141 | 3.741 | 20 | 200 | fits | 94,377 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 78,207 | 0.782 | 20 | 20 | fits | 77,684 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 522,537 | 5.225 | 20 | 20 | fits | 62,282 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 81,792 | 0.818 | 20 | 24 | fits | 77,684 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 1,092,341 | 10.923 | 20 | 24 | fits | 46,791 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 80,752 | 0.808 | 20 | 50 | fits | 77,684 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 377,817 | 3.778 | 20 | 50 | fits | 94,377 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 191,222 | 1.912 | 18 | 18 | fits | 110,925 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 1,143,292 | 11.433 | 18 | 18 | fits | 22,213 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 283,857 | 2.839 | 20 | 20 | fits | 94,377 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 71,670 | 0.717 | 20 | 200 | fits | 77,821 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 369,494 | 3.695 | 20 | 200 | fits | 94,377 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 72,582 | 0.726 | 20 | 20 | fits | 77,821 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 517,890 | 5.179 | 20 | 20 | fits | 62,282 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 76,167 | 0.762 | 20 | 24 | fits | 77,821 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 1,103,012 | 11.030 | 20 | 24 | fits | 46,629 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 75,127 | 0.751 | 20 | 50 | fits | 77,821 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 373,170 | 3.732 | 20 | 50 | fits | 94,377 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 186,575 | 1.866 | 18 | 18 | fits | 111,903 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,131,588 | 11.316 | 18 | 18 | fits | 31,111 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 288,723 | 2.887 | 20 | 20 | fits | 94,377 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 77,587 | 0.776 | 20 | 200 | fits | 77,821 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 374,360 | 3.744 | 20 | 200 | fits | 94,377 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 78,499 | 0.785 | 20 | 20 | fits | 77,821 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 522,756 | 5.228 | 20 | 20 | fits | 62,282 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 82,084 | 0.821 | 20 | 24 | fits | 77,821 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 1,115,876 | 11.159 | 20 | 24 | fits | 46,629 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 81,044 | 0.810 | 20 | 50 | fits | 77,821 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 378,036 | 3.780 | 20 | 50 | fits | 94,377 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 191,441 | 1.914 | 18 | 18 | fits | 110,852 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 1,136,711 | 11.367 | 18 | 18 | fits | 23,370 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 283,647 | 2.836 | 20 | 20 | fits | 94,377 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 71,533 | 0.715 | 20 | 200 | fits | 77,684 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 369,284 | 3.693 | 20 | 200 | fits | 94,377 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 72,445 | 0.724 | 20 | 20 | fits | 77,684 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 644,859 | 6.449 | 20 | 20 | fits | 64,103 | 35 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 76,030 | 0.760 | 20 | 24 | fits | 77,684 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 1,118,044 | 11.180 | 20 | 24 | fits | 46,933 | 29 | 0.711 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 74,990 | 0.750 | 20 | 50 | fits | 77,684 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 372,960 | 3.730 | 20 | 50 | fits | 94,377 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 186,365 | 1.864 | 18 | 18 | fits | 111,830 | 143 | 0.606 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 1,138,981 | 11.390 | 18 | 18 | fits | 23,472 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 288,814 | 2.888 | 20 | 20 | fits | 72,196 | 72 | 0.608 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 77,605 | 0.776 | 20 | 200 | fits | 77,684 | 132 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 352,270 | 3.523 | 20 | 200 | fits | 72,196 | 72 | 0.608 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 78,517 | 0.785 | 20 | 20 | fits | 77,684 | 132 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 626,362 | 6.264 | 20 | 20 | fits | 63,235 | 35 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 82,102 | 0.821 | 20 | 24 | fits | 77,684 | 132 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 1,098,793 | 10.988 | 20 | 24 | fits | 46,873 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 81,062 | 0.811 | 20 | 50 | fits | 77,684 | 132 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 355,946 | 3.559 | 20 | 50 | fits | 72,196 | 72 | 0.608 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 191,532 | 1.915 | 18 | 18 | fits | 110,925 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,149,684 | 11.497 | 18 | 18 | fits | 22,213 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 431,853 | 4.319 | 20 | 20 | fits | 86,330 | 55 | 0.688 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 73,187 | 0.732 | 20 | 200 | fits | 77,821 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 510,589 | 5.106 | 20 | 200 | fits | 86,330 | 55 | 0.688 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 74,099 | 0.741 | 20 | 20 | fits | 77,821 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 647,402 | 6.474 | 20 | 20 | fits | 51,255 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 77,684 | 0.777 | 20 | 24 | fits | 77,821 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 1,119,058 | 11.191 | 20 | 24 | fits | 46,731 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 76,644 | 0.766 | 20 | 50 | fits | 77,821 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 427,935 | 4.279 | 20 | 50 | fits | 92,315 | 96 | 0.594 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 187,041 | 1.870 | 18 | 18 | fits | 110,852 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 1,140,055 | 11.401 | 18 | 18 | fits | 23,532 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 433,710 | 4.337 | 20 | 20 | fits | 86,065 | 55 | 0.684 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 77,897 | 0.779 | 20 | 200 | fits | 77,821 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 512,181 | 5.122 | 20 | 200 | fits | 86,065 | 55 | 0.684 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 78,809 | 0.788 | 20 | 20 | fits | 77,821 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 648,770 | 6.488 | 20 | 20 | fits | 51,176 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 82,394 | 0.824 | 20 | 24 | fits | 77,821 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 1,118,178 | 11.182 | 20 | 24 | fits | 44,483 | 30 | 0.764 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 81,354 | 0.814 | 20 | 50 | fits | 77,821 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 429,792 | 4.298 | 20 | 50 | fits | 91,690 | 96 | 0.590 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 166,970 | 1.670 | 18 | 18 | fits | 86,071 | 103 | 0.683 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,146,936 | 11.469 | 18 | 18 | fits | 31,293 | 19 | 0.755 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 289,870 | 2.899 | 20 | 20 | fits | 94,359 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 78,730 | 0.787 | 20 | 200 | fits | 77,894 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 375,481 | 3.755 | 20 | 200 | fits | 94,359 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 79,642 | 0.796 | 20 | 20 | fits | 77,894 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 523,968 | 5.240 | 20 | 20 | fits | 62,323 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 83,227 | 0.832 | 20 | 24 | fits | 77,894 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 1,048,011 | 10.480 | 20 | 24 | fits | 47,035 | 29 | 0.715 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 82,187 | 0.822 | 20 | 50 | fits | 77,894 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 379,157 | 3.792 | 20 | 50 | fits | 94,359 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 192,480 | 1.925 | 18 | 18 | fits | 110,748 | 138 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 1,068,846 | 10.688 | 18 | 18 | fits | 23,370 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 285,355 | 2.854 | 20 | 20 | fits | 94,359 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 74,142 | 0.741 | 20 | 200 | fits | 77,757 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 370,966 | 3.710 | 20 | 200 | fits | 94,359 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 75,054 | 0.751 | 20 | 20 | fits | 77,757 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 519,573 | 5.196 | 20 | 20 | fits | 62,443 | 33 | 0.719 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 78,639 | 0.786 | 20 | 24 | fits | 77,757 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 1,020,892 | 10.209 | 20 | 24 | fits | 46,629 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 77,599 | 0.776 | 20 | 50 | fits | 77,757 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 374,642 | 3.746 | 20 | 50 | fits | 94,359 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 187,965 | 1.880 | 18 | 18 | fits | 110,821 | 138 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 1,071,519 | 10.715 | 18 | 18 | fits | 22,051 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 290,086 | 2.901 | 20 | 20 | fits | 94,359 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 78,873 | 0.789 | 20 | 200 | fits | 77,757 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 375,697 | 3.757 | 20 | 200 | fits | 94,359 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 79,785 | 0.798 | 20 | 20 | fits | 77,757 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 524,298 | 5.243 | 20 | 20 | fits | 62,373 | 33 | 0.718 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 83,370 | 0.834 | 20 | 24 | fits | 77,757 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 1,039,820 | 10.398 | 20 | 24 | fits | 46,569 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 82,330 | 0.823 | 20 | 50 | fits | 77,757 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 379,373 | 3.794 | 20 | 50 | fits | 94,359 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 192,696 | 1.927 | 18 | 18 | fits | 110,821 | 138 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,068,396 | 10.684 | 18 | 18 | fits | 31,111 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 285,860 | 2.859 | 20 | 20 | fits | 94,431 | 81 | 0.645 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 74,650 | 0.747 | 20 | 200 | fits | 77,894 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 371,473 | 3.715 | 20 | 200 | fits | 94,431 | 81 | 0.645 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 75,562 | 0.756 | 20 | 20 | fits | 77,894 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 519,946 | 5.199 | 20 | 20 | fits | 62,315 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 79,147 | 0.791 | 20 | 24 | fits | 77,894 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 1,043,265 | 10.433 | 20 | 24 | fits | 46,569 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 78,107 | 0.781 | 20 | 50 | fits | 77,894 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 375,149 | 3.751 | 20 | 50 | fits | 94,431 | 81 | 0.645 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 188,400 | 1.884 | 18 | 18 | fits | 110,748 | 138 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,064,100 | 10.641 | 18 | 18 | fits | 23,370 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 290,569 | 2.906 | 20 | 20 | fits | 94,351 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 79,381 | 0.794 | 20 | 200 | fits | 77,894 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 376,180 | 3.762 | 20 | 200 | fits | 94,351 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 80,293 | 0.803 | 20 | 20 | fits | 77,894 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 581,778 | 5.818 | 20 | 20 | fits | 63,322 | 35 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 83,878 | 0.839 | 20 | 24 | fits | 77,894 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 1,054,388 | 10.544 | 20 | 24 | fits | 46,873 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 82,838 | 0.828 | 20 | 50 | fits | 77,894 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 379,856 | 3.799 | 20 | 50 | fits | 94,351 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 193,193 | 1.932 | 18 | 18 | fits | 110,810 | 138 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 1,075,325 | 10.753 | 18 | 18 | fits | 23,472 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 286,004 | 2.860 | 20 | 20 | fits | 72,128 | 72 | 0.607 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 74,815 | 0.748 | 20 | 200 | fits | 77,741 | 132 | 0.505 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 349,392 | 3.494 | 20 | 200 | fits | 72,128 | 72 | 0.607 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 75,727 | 0.757 | 20 | 20 | fits | 77,741 | 132 | 0.505 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 554,720 | 5.547 | 20 | 20 | fits | 62,890 | 35 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 79,312 | 0.793 | 20 | 24 | fits | 77,741 | 132 | 0.505 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 1,027,330 | 10.273 | 20 | 24 | fits | 46,873 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 78,272 | 0.783 | 20 | 50 | fits | 77,741 | 132 | 0.505 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 353,068 | 3.531 | 20 | 50 | fits | 72,128 | 72 | 0.607 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 188,630 | 1.886 | 18 | 18 | fits | 110,813 | 138 | 0.609 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,078,221 | 10.782 | 18 | 18 | fits | 22,213 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 377,794 | 3.778 | 20 | 20 | fits | 85,908 | 55 | 0.682 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 111,116 | 1.111 | 20 | 200 | fits | 77,358 | 134 | 0.497 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 456,108 | 4.561 | 20 | 200 | fits | 85,908 | 55 | 0.682 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 112,028 | 1.120 | 20 | 20 | fits | 77,358 | 134 | 0.497 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 593,209 | 5.932 | 20 | 20 | fits | 51,367 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 38,255 | 0.383 | 20 | 24 | fits | 41,255 | 69 | 0.572 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 1,018,134 | 10.181 | 20 | 24 | fits | 46,731 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 37,215 | 0.372 | 20 | 50 | fits | 41,255 | 69 | 0.572 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 295,099 | 2.951 | 20 | 50 | fits | 79,514 | 62 | 0.736 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 215,520 | 2.155 | 18 | 18 | fits | 101,402 | 134 | 0.602 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 1,076,713 | 10.767 | 18 | 18 | fits | 29,841 | 17 | 0.732 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 361,069 | 3.611 | 20 | 20 | fits | 86,043 | 55 | 0.684 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 75,099 | 0.751 | 20 | 200 | fits | 77,886 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 439,518 | 4.395 | 20 | 200 | fits | 86,043 | 55 | 0.684 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 76,011 | 0.760 | 20 | 20 | fits | 77,886 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 576,101 | 5.761 | 20 | 20 | fits | 51,250 | 26 | 0.783 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 79,596 | 0.796 | 20 | 24 | fits | 77,886 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 1,047,784 | 10.478 | 20 | 24 | fits | 46,731 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 78,556 | 0.786 | 20 | 50 | fits | 77,886 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 357,151 | 3.572 | 20 | 50 | fits | 91,634 | 96 | 0.589 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 172,270 | 1.723 | 18 | 18 | fits | 94,169 | 103 | 0.700 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,068,690 | 10.687 | 18 | 18 | fits | 23,441 | 15 | 0.813 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 287,617 | 2.876 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 76,217 | 0.762 | 20 | 200 | fits | 78,287 | 132 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 373,384 | 3.734 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 77,129 | 0.771 | 20 | 20 | fits | 78,287 | 132 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 521,946 | 5.219 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 80,714 | 0.807 | 20 | 24 | fits | 78,287 | 132 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 1,121,722 | 11.217 | 20 | 24 | fits | 47,314 | 29 | 0.719 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 79,674 | 0.797 | 20 | 50 | fits | 78,287 | 132 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 377,060 | 3.771 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 190,141 | 1.901 | 18 | 18 | fits | 110,922 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 1,142,565 | 11.426 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 284,007 | 2.840 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 71,629 | 0.716 | 20 | 200 | fits | 78,150 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 369,774 | 3.698 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 72,541 | 0.725 | 20 | 20 | fits | 78,150 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 518,336 | 5.183 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 76,126 | 0.761 | 20 | 24 | fits | 78,150 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 1,094,849 | 10.948 | 20 | 24 | fits | 46,710 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 75,086 | 0.751 | 20 | 50 | fits | 78,150 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 373,450 | 3.735 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 186,531 | 1.865 | 18 | 18 | fits | 111,900 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 1,145,816 | 11.458 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 287,924 | 2.879 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 76,451 | 0.765 | 20 | 200 | fits | 78,150 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 373,691 | 3.737 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 77,363 | 0.774 | 20 | 20 | fits | 78,150 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 522,253 | 5.223 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 80,948 | 0.809 | 20 | 24 | fits | 78,150 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 1,113,784 | 11.138 | 20 | 24 | fits | 46,637 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 79,908 | 0.799 | 20 | 50 | fits | 78,150 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 377,367 | 3.774 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 190,448 | 1.904 | 18 | 18 | fits | 110,995 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,142,368 | 11.424 | 18 | 18 | fits | 31,119 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 284,579 | 2.846 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 72,128 | 0.721 | 20 | 200 | fits | 78,287 | 132 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 370,346 | 3.703 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 73,040 | 0.730 | 20 | 20 | fits | 78,287 | 132 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 518,908 | 5.189 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 76,625 | 0.766 | 20 | 24 | fits | 78,287 | 132 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 1,117,951 | 11.180 | 20 | 24 | fits | 46,637 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 75,585 | 0.756 | 20 | 50 | fits | 78,287 | 132 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 374,022 | 3.740 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 187,103 | 1.871 | 18 | 18 | fits | 111,973 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,138,794 | 11.388 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 288,359 | 2.884 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 76,959 | 0.770 | 20 | 200 | fits | 78,287 | 132 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 374,126 | 3.741 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 77,871 | 0.779 | 20 | 20 | fits | 78,287 | 132 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 655,438 | 6.554 | 20 | 20 | fits | 64,097 | 35 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 81,456 | 0.815 | 20 | 24 | fits | 78,287 | 132 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 1,127,248 | 11.272 | 20 | 24 | fits | 46,779 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 80,416 | 0.804 | 20 | 50 | fits | 78,287 | 132 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 377,802 | 3.778 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 190,883 | 1.909 | 18 | 18 | fits | 110,922 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,148,031 | 11.480 | 18 | 18 | fits | 23,318 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 284,369 | 2.844 | 20 | 20 | fits | 72,136 | 72 | 0.606 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 71,991 | 0.720 | 20 | 200 | fits | 78,150 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 347,757 | 3.478 | 20 | 200 | fits | 72,136 | 72 | 0.606 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 72,903 | 0.729 | 20 | 20 | fits | 78,150 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 627,024 | 6.270 | 20 | 20 | fits | 62,961 | 35 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 76,488 | 0.765 | 20 | 24 | fits | 78,150 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 1,099,578 | 10.996 | 20 | 24 | fits | 46,881 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 75,448 | 0.754 | 20 | 50 | fits | 78,150 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 351,433 | 3.514 | 20 | 50 | fits | 72,136 | 72 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 186,893 | 1.869 | 18 | 18 | fits | 111,900 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,150,485 | 11.505 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 441,214 | 4.412 | 20 | 20 | fits | 86,362 | 55 | 0.688 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 77,193 | 0.772 | 20 | 200 | fits | 78,150 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 519,974 | 5.200 | 20 | 200 | fits | 86,362 | 55 | 0.688 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 78,105 | 0.781 | 20 | 20 | fits | 78,150 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 656,762 | 6.568 | 20 | 20 | fits | 51,222 | 26 | 0.781 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 81,690 | 0.817 | 20 | 24 | fits | 78,150 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 1,128,576 | 11.286 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 80,650 | 0.806 | 20 | 50 | fits | 78,150 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 437,288 | 4.373 | 20 | 50 | fits | 92,169 | 96 | 0.594 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 191,190 | 1.912 | 18 | 18 | fits | 110,995 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 1,149,581 | 11.496 | 18 | 18 | fits | 23,540 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 410,802 | 4.108 | 20 | 20 | fits | 86,429 | 55 | 0.688 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 72,128 | 0.721 | 20 | 200 | fits | 78,287 | 132 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 489,629 | 4.896 | 20 | 200 | fits | 86,429 | 55 | 0.688 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 73,040 | 0.730 | 20 | 20 | fits | 78,287 | 132 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 626,279 | 6.263 | 20 | 20 | fits | 51,229 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 76,625 | 0.766 | 20 | 24 | fits | 78,287 | 132 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 1,076,385 | 10.764 | 20 | 24 | fits | 25,031 | 20 | 0.670 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 75,585 | 0.756 | 20 | 50 | fits | 78,287 | 132 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 406,876 | 4.069 | 20 | 50 | fits | 93,105 | 96 | 0.605 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 230,453 | 2.305 | 18 | 18 | fits | 79,338 | 62 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,162,021 | 11.620 | 18 | 18 | fits | 29,651 | 17 | 0.726 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 283,956 | 2.840 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 71,505 | 0.715 | 20 | 200 | fits | 78,287 | 132 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 369,723 | 3.697 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 72,417 | 0.724 | 20 | 20 | fits | 78,287 | 132 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 518,285 | 5.183 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 76,002 | 0.760 | 20 | 24 | fits | 78,287 | 132 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 1,034,602 | 10.346 | 20 | 24 | fits | 46,934 | 29 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 74,962 | 0.750 | 20 | 50 | fits | 78,287 | 132 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 373,399 | 3.734 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 186,480 | 1.865 | 18 | 18 | fits | 111,973 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 1,055,445 | 10.554 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 287,727 | 2.877 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 76,327 | 0.763 | 20 | 200 | fits | 78,287 | 132 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 373,494 | 3.735 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 77,239 | 0.772 | 20 | 20 | fits | 78,287 | 132 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 522,056 | 5.221 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 80,824 | 0.808 | 20 | 24 | fits | 78,287 | 132 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 1,014,529 | 10.145 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 79,784 | 0.798 | 20 | 50 | fits | 78,287 | 132 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 377,170 | 3.772 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 190,251 | 1.903 | 18 | 18 | fits | 110,922 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 1,065,172 | 10.652 | 18 | 18 | fits | 22,059 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 284,117 | 2.841 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 71,739 | 0.717 | 20 | 200 | fits | 78,150 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 369,884 | 3.699 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 72,651 | 0.727 | 20 | 20 | fits | 78,150 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 518,446 | 5.184 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 76,236 | 0.762 | 20 | 24 | fits | 78,150 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 1,026,135 | 10.261 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 75,196 | 0.752 | 20 | 50 | fits | 78,150 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 373,560 | 3.736 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 186,641 | 1.866 | 18 | 18 | fits | 111,900 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 1,054,719 | 10.547 | 18 | 18 | fits | 31,119 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 288,034 | 2.880 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 76,561 | 0.766 | 20 | 200 | fits | 78,150 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 373,801 | 3.738 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 77,473 | 0.775 | 20 | 20 | fits | 78,150 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 522,363 | 5.224 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 81,058 | 0.811 | 20 | 24 | fits | 78,150 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 1,037,384 | 10.374 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 80,018 | 0.800 | 20 | 50 | fits | 78,150 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 377,477 | 3.775 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 190,558 | 1.906 | 18 | 18 | fits | 110,995 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 1,058,227 | 10.582 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 284,579 | 2.846 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 72,128 | 0.721 | 20 | 200 | fits | 78,287 | 132 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 370,346 | 3.703 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 73,040 | 0.730 | 20 | 20 | fits | 78,287 | 132 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 567,767 | 5.678 | 20 | 20 | fits | 63,231 | 35 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 76,625 | 0.766 | 20 | 24 | fits | 78,287 | 132 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 1,040,415 | 10.404 | 20 | 24 | fits | 46,881 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 75,585 | 0.756 | 20 | 50 | fits | 78,287 | 132 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 374,022 | 3.740 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 187,103 | 1.871 | 18 | 18 | fits | 111,973 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 1,061,360 | 10.614 | 18 | 18 | fits | 23,480 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 288,469 | 2.885 | 20 | 20 | fits | 72,136 | 72 | 0.606 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 77,069 | 0.771 | 20 | 200 | fits | 78,287 | 132 | 0.511 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 351,857 | 3.519 | 20 | 200 | fits | 72,136 | 72 | 0.606 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 77,981 | 0.780 | 20 | 20 | fits | 78,287 | 132 | 0.511 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 547,883 | 5.479 | 20 | 20 | fits | 62,970 | 35 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 81,566 | 0.816 | 20 | 24 | fits | 78,287 | 132 | 0.511 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 1,020,430 | 10.204 | 20 | 24 | fits | 46,881 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 80,526 | 0.805 | 20 | 50 | fits | 78,287 | 132 | 0.511 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 355,533 | 3.555 | 20 | 50 | fits | 72,136 | 72 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 190,993 | 1.910 | 18 | 18 | fits | 110,922 | 138 | 0.610 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,071,337 | 10.713 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 353,448 | 3.534 | 20 | 20 | fits | 86,218 | 55 | 0.686 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 71,991 | 0.720 | 20 | 200 | fits | 78,150 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 432,064 | 4.321 | 20 | 200 | fits | 86,218 | 55 | 0.686 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 72,903 | 0.729 | 20 | 20 | fits | 78,150 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 568,925 | 5.689 | 20 | 20 | fits | 51,263 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 76,488 | 0.765 | 20 | 24 | fits | 78,150 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 1,040,661 | 10.407 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 75,448 | 0.754 | 20 | 50 | fits | 78,150 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 349,522 | 3.495 | 20 | 50 | fits | 91,946 | 96 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 186,893 | 1.869 | 18 | 18 | fits | 111,900 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 1,061,666 | 10.617 | 18 | 18 | fits | 23,540 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 354,742 | 3.547 | 20 | 20 | fits | 85,961 | 55 | 0.683 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 77,303 | 0.773 | 20 | 200 | fits | 78,150 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 433,101 | 4.331 | 20 | 200 | fits | 85,961 | 55 | 0.683 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 78,215 | 0.782 | 20 | 20 | fits | 78,150 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 569,667 | 5.697 | 20 | 20 | fits | 51,225 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 81,800 | 0.818 | 20 | 24 | fits | 78,150 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 1,041,403 | 10.414 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 80,760 | 0.808 | 20 | 50 | fits | 78,150 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 350,816 | 3.508 | 20 | 50 | fits | 91,564 | 96 | 0.588 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 166,361 | 1.664 | 18 | 18 | fits | 86,056 | 103 | 0.683 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 1,062,408 | 10.624 | 18 | 18 | fits | 23,540 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 287,876 | 2.879 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 76,434 | 0.764 | 20 | 200 | fits | 78,146 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 373,643 | 3.736 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 77,346 | 0.773 | 20 | 20 | fits | 78,146 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 522,205 | 5.222 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 80,931 | 0.809 | 20 | 24 | fits | 78,146 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 1,117,148 | 11.171 | 20 | 24 | fits | 47,349 | 29 | 0.716 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 79,891 | 0.799 | 20 | 50 | fits | 78,146 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 377,319 | 3.773 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 190,464 | 1.905 | 18 | 18 | fits | 111,028 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 1,137,991 | 11.380 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 284,540 | 2.845 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 72,120 | 0.721 | 20 | 200 | fits | 78,283 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 370,307 | 3.703 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 73,032 | 0.730 | 20 | 20 | fits | 78,283 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 518,869 | 5.189 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 76,617 | 0.766 | 20 | 24 | fits | 78,283 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 1,090,520 | 10.905 | 20 | 24 | fits | 46,799 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 75,577 | 0.756 | 20 | 50 | fits | 78,283 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 373,983 | 3.740 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 187,128 | 1.871 | 18 | 18 | fits | 112,006 | 143 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 1,141,487 | 11.415 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 288,311 | 2.883 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 76,942 | 0.769 | 20 | 200 | fits | 78,283 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 374,078 | 3.741 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 77,854 | 0.779 | 20 | 20 | fits | 78,283 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 522,640 | 5.226 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 81,439 | 0.814 | 20 | 24 | fits | 78,283 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 1,109,227 | 11.092 | 20 | 24 | fits | 46,637 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 80,399 | 0.804 | 20 | 50 | fits | 78,283 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 377,754 | 3.778 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 190,899 | 1.909 | 18 | 18 | fits | 110,955 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,137,811 | 11.378 | 18 | 18 | fits | 31,119 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 284,334 | 2.843 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 71,987 | 0.720 | 20 | 200 | fits | 78,146 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 370,101 | 3.701 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 72,899 | 0.729 | 20 | 20 | fits | 78,146 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 518,663 | 5.187 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 76,484 | 0.765 | 20 | 24 | fits | 78,146 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 1,112,762 | 11.128 | 20 | 24 | fits | 46,637 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 75,444 | 0.754 | 20 | 50 | fits | 78,146 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 373,777 | 3.738 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 186,922 | 1.869 | 18 | 18 | fits | 111,933 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 1,133,605 | 11.336 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 288,618 | 2.886 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 77,176 | 0.772 | 20 | 200 | fits | 78,146 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 374,385 | 3.744 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 78,088 | 0.781 | 20 | 20 | fits | 78,146 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 650,799 | 6.508 | 20 | 20 | fits | 64,067 | 35 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 81,673 | 0.817 | 20 | 24 | fits | 78,146 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 1,122,566 | 11.226 | 20 | 24 | fits | 46,779 | 29 | 0.709 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 80,633 | 0.806 | 20 | 50 | fits | 78,146 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 378,061 | 3.781 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 191,206 | 1.912 | 18 | 18 | fits | 111,028 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,143,349 | 11.433 | 18 | 18 | fits | 23,318 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 284,544 | 2.845 | 20 | 20 | fits | 72,136 | 72 | 0.606 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 72,124 | 0.721 | 20 | 200 | fits | 78,283 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 347,932 | 3.479 | 20 | 200 | fits | 72,136 | 72 | 0.606 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 73,036 | 0.730 | 20 | 20 | fits | 78,283 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 622,411 | 6.224 | 20 | 20 | fits | 63,146 | 35 | 0.723 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 76,621 | 0.766 | 20 | 24 | fits | 78,283 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 1,094,922 | 10.949 | 20 | 24 | fits | 46,881 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 75,581 | 0.756 | 20 | 50 | fits | 78,283 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 351,608 | 3.516 | 20 | 50 | fits | 72,136 | 72 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 187,132 | 1.871 | 18 | 18 | fits | 112,006 | 143 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,145,829 | 11.458 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 436,947 | 4.369 | 20 | 20 | fits | 86,367 | 55 | 0.688 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 77,684 | 0.777 | 20 | 200 | fits | 78,283 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 515,712 | 5.157 | 20 | 200 | fits | 86,367 | 55 | 0.688 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 78,596 | 0.786 | 20 | 20 | fits | 78,283 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 652,541 | 6.525 | 20 | 20 | fits | 51,263 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 82,181 | 0.822 | 20 | 24 | fits | 78,283 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 1,124,355 | 11.244 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 81,141 | 0.811 | 20 | 50 | fits | 78,283 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 433,021 | 4.330 | 20 | 50 | fits | 92,348 | 96 | 0.594 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 191,641 | 1.916 | 18 | 18 | fits | 110,955 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 1,145,360 | 11.454 | 18 | 18 | fits | 23,540 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 406,393 | 4.064 | 20 | 20 | fits | 86,352 | 55 | 0.687 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 71,987 | 0.720 | 20 | 200 | fits | 78,146 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 485,143 | 4.851 | 20 | 200 | fits | 86,352 | 55 | 0.687 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 72,899 | 0.729 | 20 | 20 | fits | 78,146 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 621,834 | 6.218 | 20 | 20 | fits | 51,270 | 26 | 0.783 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 76,484 | 0.765 | 20 | 24 | fits | 78,146 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 1,071,940 | 10.719 | 20 | 24 | fits | 25,031 | 20 | 0.670 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 75,444 | 0.754 | 20 | 50 | fits | 78,146 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 402,467 | 4.025 | 20 | 50 | fits | 93,684 | 96 | 0.609 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 230,355 | 2.304 | 18 | 18 | fits | 79,379 | 62 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 1,157,597 | 11.576 | 18 | 18 | fits | 29,651 | 17 | 0.726 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 284,069 | 2.841 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 71,722 | 0.717 | 20 | 200 | fits | 78,146 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 369,836 | 3.698 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 72,634 | 0.726 | 20 | 20 | fits | 78,146 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 518,398 | 5.184 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 76,219 | 0.762 | 20 | 24 | fits | 78,146 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 1,034,715 | 10.347 | 20 | 24 | fits | 46,934 | 29 | 0.713 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 75,179 | 0.752 | 20 | 50 | fits | 78,146 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 373,512 | 3.735 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 186,657 | 1.867 | 18 | 18 | fits | 111,933 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 1,055,558 | 10.556 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 287,986 | 2.880 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 76,544 | 0.765 | 20 | 200 | fits | 78,146 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 373,753 | 3.738 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 77,456 | 0.775 | 20 | 20 | fits | 78,146 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 522,315 | 5.223 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 81,041 | 0.810 | 20 | 24 | fits | 78,146 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 1,014,788 | 10.148 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 80,001 | 0.800 | 20 | 50 | fits | 78,146 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 377,429 | 3.774 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 190,574 | 1.906 | 18 | 18 | fits | 111,028 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 1,065,431 | 10.654 | 18 | 18 | fits | 22,059 | 14 | 0.791 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 284,544 | 2.845 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 72,124 | 0.721 | 20 | 200 | fits | 78,283 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 370,311 | 3.703 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 73,036 | 0.730 | 20 | 20 | fits | 78,283 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 518,873 | 5.189 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 76,621 | 0.766 | 20 | 24 | fits | 78,283 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 1,026,562 | 10.266 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 75,581 | 0.756 | 20 | 50 | fits | 78,283 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 373,987 | 3.740 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 187,132 | 1.871 | 18 | 18 | fits | 112,006 | 143 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 1,055,146 | 10.551 | 18 | 18 | fits | 31,119 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 288,421 | 2.884 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 77,052 | 0.771 | 20 | 200 | fits | 78,283 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 374,188 | 3.742 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 77,964 | 0.780 | 20 | 20 | fits | 78,283 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 522,750 | 5.228 | 20 | 20 | fits | 62,266 | 33 | 0.716 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 81,549 | 0.815 | 20 | 24 | fits | 78,283 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 1,037,771 | 10.378 | 20 | 24 | fits | 46,577 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 80,509 | 0.805 | 20 | 50 | fits | 78,283 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 377,864 | 3.779 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 191,009 | 1.910 | 18 | 18 | fits | 110,955 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 1,058,614 | 10.586 | 18 | 18 | fits | 23,378 | 16 | 0.804 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 284,334 | 2.843 | 20 | 20 | fits | 94,515 | 81 | 0.644 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 71,987 | 0.720 | 20 | 200 | fits | 78,146 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 370,101 | 3.701 | 20 | 200 | fits | 94,515 | 81 | 0.644 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 72,899 | 0.729 | 20 | 20 | fits | 78,146 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 567,522 | 5.675 | 20 | 20 | fits | 63,231 | 35 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 76,484 | 0.765 | 20 | 24 | fits | 78,146 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 1,040,170 | 10.402 | 20 | 24 | fits | 46,881 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 75,444 | 0.754 | 20 | 50 | fits | 78,146 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 373,777 | 3.738 | 20 | 50 | fits | 94,515 | 81 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 186,922 | 1.869 | 18 | 18 | fits | 111,933 | 143 | 0.607 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 1,061,115 | 10.611 | 18 | 18 | fits | 23,480 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 288,728 | 2.887 | 20 | 20 | fits | 72,136 | 72 | 0.606 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 77,286 | 0.773 | 20 | 200 | fits | 78,146 | 132 | 0.507 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 352,116 | 3.521 | 20 | 200 | fits | 72,136 | 72 | 0.606 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 78,198 | 0.782 | 20 | 20 | fits | 78,146 | 132 | 0.507 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 548,142 | 5.481 | 20 | 20 | fits | 62,970 | 35 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 81,783 | 0.818 | 20 | 24 | fits | 78,146 | 132 | 0.507 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 1,020,689 | 10.207 | 20 | 24 | fits | 46,881 | 29 | 0.710 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 80,743 | 0.807 | 20 | 50 | fits | 78,146 | 132 | 0.507 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 355,792 | 3.558 | 20 | 50 | fits | 72,136 | 72 | 0.606 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 191,316 | 1.913 | 18 | 18 | fits | 111,028 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,071,596 | 10.716 | 18 | 18 | fits | 22,221 | 14 | 0.795 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 353,733 | 3.537 | 20 | 20 | fits | 86,218 | 55 | 0.686 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 72,124 | 0.721 | 20 | 200 | fits | 78,283 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 432,349 | 4.323 | 20 | 200 | fits | 86,218 | 55 | 0.686 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 73,036 | 0.730 | 20 | 20 | fits | 78,283 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 569,210 | 5.692 | 20 | 20 | fits | 51,263 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 76,621 | 0.766 | 20 | 24 | fits | 78,283 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 1,040,946 | 10.409 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 75,581 | 0.756 | 20 | 50 | fits | 78,283 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 349,807 | 3.498 | 20 | 50 | fits | 91,946 | 96 | 0.593 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 187,132 | 1.871 | 18 | 18 | fits | 112,006 | 143 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 1,061,951 | 10.620 | 18 | 18 | fits | 23,540 | 16 | 0.807 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 355,404 | 3.554 | 20 | 20 | fits | 85,961 | 55 | 0.683 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 77,794 | 0.778 | 20 | 200 | fits | 78,283 | 132 | 0.509 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 433,763 | 4.338 | 20 | 200 | fits | 85,961 | 55 | 0.683 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 78,706 | 0.787 | 20 | 20 | fits | 78,283 | 132 | 0.509 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 570,329 | 5.703 | 20 | 20 | fits | 51,225 | 26 | 0.782 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 82,291 | 0.823 | 20 | 24 | fits | 78,283 | 132 | 0.509 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 1,042,065 | 10.421 | 20 | 24 | fits | 46,739 | 29 | 0.708 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 81,251 | 0.813 | 20 | 50 | fits | 78,283 | 132 | 0.509 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 351,478 | 3.515 | 20 | 50 | fits | 91,550 | 96 | 0.588 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 166,909 | 1.669 | 18 | 18 | fits | 86,113 | 103 | 0.684 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 1,063,070 | 10.631 | 18 | 18 | fits | 23,540 | 16 | 0.807 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 272,350 | 2.724 | 20 | 200 | fits | 71,017 | 84 | 0.535 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 425,209 | 4.252 | 20 | 20 | fits | 55,084 | 32 | 0.665 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 547,854 | 5.479 | 20 | 24 | fits | 22,397 | 21 | 0.566 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 275,244 | 2.752 | 20 | 50 | fits | 62,506 | 55 | 0.623 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 802,104 | 8.021 | 18 | 18 | fits | 39,342 | 26 | 0.737 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 281,116 | 2.811 | 20 | 200 | fits | 73,993 | 90 | 0.562 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 441,755 | 4.418 | 20 | 20 | fits | 57,095 | 38 | 0.669 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 606,178 | 6.062 | 20 | 24 | fits | 25,106 | 27 | 0.606 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 287,098 | 2.871 | 20 | 50 | fits | 65,594 | 61 | 0.647 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 861,098 | 8.611 | 18 | 18 | fits | 41,975 | 32 | 0.742 |
| an event behind 15 others | `backlog.event.if0` | 94,290 | 0.943 | 20 | 200 | fits | 69,094 | 104 | 0.513 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 365,703 | 3.657 | 20 | 20 | fits | 50,041 | 44 | 0.517 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 83,677 | 0.837 | 20 | 200 | fits | 83,885 | 138 | 0.516 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 297,284 | 2.973 | 20 | 200 | fits | 60,013 | 55 | 0.570 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 79,418 | 0.794 | 20 | 20 | fits | 83,885 | 138 | 0.516 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 393,664 | 3.937 | 20 | 20 | fits | 50,041 | 44 | 0.517 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 83,003 | 0.830 | 20 | 24 | fits | 83,885 | 138 | 0.516 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 647,867 | 6.479 | 20 | 24 | fits | 24,993 | 29 | 0.497 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 81,963 | 0.820 | 20 | 50 | fits | 83,885 | 138 | 0.516 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 295,789 | 2.958 | 20 | 50 | fits | 60,013 | 55 | 0.570 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 295,724 | 2.957 | 18 | 18 | fits | 60,013 | 55 | 0.570 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 676,484 | 6.765 | 18 | 18 | fits | 10,050 | 17 | 0.178 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 284,540 | 2.845 | 20 | 20 | fits | 94,445 | 81 | 0.646 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 73,074 | 0.731 | 20 | 200 | fits | 77,756 | 135 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 370,419 | 3.704 | 20 | 200 | fits | 94,445 | 81 | 0.646 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 73,986 | 0.740 | 20 | 20 | fits | 77,756 | 135 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 519,071 | 5.191 | 20 | 20 | fits | 62,297 | 33 | 0.717 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 77,571 | 0.776 | 20 | 24 | fits | 77,756 | 135 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,026,541 | 10.265 | 20 | 24 | fits | 46,575 | 29 | 0.706 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 76,531 | 0.765 | 20 | 50 | fits | 77,756 | 135 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 374,095 | 3.741 | 20 | 50 | fits | 94,445 | 81 | 0.646 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 186,996 | 1.870 | 18 | 18 | fits | 110,920 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,055,120 | 10.551 | 18 | 18 | fits | 31,114 | 19 | 0.750 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 13,938 | 0.139 | 20 | 20 | fits | 21,557 | 20 | 0.769 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 73,074 | 0.731 | 20 | 200 | fits | 77,756 | 135 | 0.495 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 29,007 | 0.290 | 20 | 200 | fits | 21,557 | 20 | 0.769 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 73,986 | 0.740 | 20 | 20 | fits | 77,756 | 135 | 0.495 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 512,216 | 5.122 | 20 | 20 | fits | 74,825 | 44 | 0.674 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 77,571 | 0.776 | 20 | 24 | fits | 77,756 | 135 | 0.495 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 981,196 | 9.812 | 20 | 24 | fits | 46,641 | 29 | 0.707 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 76,531 | 0.765 | 20 | 50 | fits | 77,756 | 135 | 0.495 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 364,574 | 3.646 | 20 | 50 | fits | 84,924 | 71 | 0.644 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 186,996 | 1.870 | 18 | 18 | fits | 110,920 | 138 | 0.611 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,033,465 | 10.335 | 18 | 18 | fits | 23,769 | 18 | 0.726 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,212,533 | 62.125 | 20 | 20 | MISS ceiling | 28,810 | 25 | 0.570 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,026,733 | 360.267 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,026,658 | 360.267 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,026,583 | 360.266 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,026,508 | 360.265 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 77,500 | 0.775 | 20 | 200 | fits | 75,048 | 129 | 0.505 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 359,389 | 3.594 | 20 | 200 | fits | 83,492 | 67 | 0.654 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 73,241 | 0.732 | 20 | 20 | fits | 75,048 | 129 | 0.505 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 505,559 | 5.056 | 20 | 20 | fits | 39,295 | 24 | 0.756 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 76,826 | 0.768 | 20 | 24 | fits | 75,048 | 129 | 0.505 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,297,257 | 62.973 | 20 | 24 | MISS ceiling | 22,157 | 21 | 0.556 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 75,786 | 0.758 | 20 | 50 | fits | 75,048 | 129 | 0.505 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 357,894 | 3.579 | 20 | 50 | fits | 83,492 | 67 | 0.654 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 184,100 | 1.841 | 18 | 18 | fits | 108,769 | 131 | 0.633 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 840,213 | 8.402 | 18 | 18 | fits | 23,411 | 17 | 0.787 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT

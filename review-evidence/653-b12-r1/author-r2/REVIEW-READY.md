[A543] REVIEW READY
Commit: `bef8dd7036f711bf286929fa4cba6bf724c7118d`
Changed: appended the dated B12 VLAN-build section and its Contents entry in `docs/findings/653_DISCONNECT_ORDER_BENCH.md`.

Results: 182 SUCCESS responses, all response first; the library was NotConnected at every unlock update. Both ten-minute windows, all 546 early reads and all 1,510 counter reads showed zero sequence mismatches and interruptions. Hive's rule reported two peer timestamp increments, detailed below.

Scope interpretation: 140 fixed-hold cycles plus 40 separate counter-push boundary controls. Each fixed hold received five repetitions per direction and stream kind. Boundary controls report their actual duration and phase; a fixed duration cannot independently choose its push phase. The named source library was built on the controller host and used for every cycle. The complete graphical application was outside the method.

Restoration: bindings, formats, maps and clock sources match as-found protocol readbacks for both entities. All streams are unbound; DUT servo IDLE. NVM sequence 98 to 230 and commits 67 to 199 are retained residuals; failed commits stayed zero. Remote staging is removed; the bench lock is released.

Validation on the committed head: all rc 0, foreground with explicit deadlines, from the physical worktree. Markdown checks used the required pinned interpreter.

- `scripts/docs_check.py`
- `scripts/check_doc_style.py`
- `scripts/gen_toc.py --check`
- `scripts/check_em_dash.py --base fa450d30` (424 added lines)
- `scripts/check_doc_paths.py`
- `python3 scripts/check_baremetal_only.py --check`
- `git diff --check`

Eight ordering controls and eight extracted-rule controls passed. The inverted Connected predicate failed as expected. The capture-statistics wording was corrected after an initial bare-metal vocabulary-gate rejection; no gate was changed.

Acceptance: the assigned identity, library build, cycle matrix, wire observations, sequence windows and readback restoration are complete under the stated timing interpretation. No DUT wrong-order or wrong-status STOP condition was observed. Open limits: sampled runs on this flashed image; full graphical application outside the method; peer timestamp fault attribution unresolved.

Packet: `653-b12-a543`, including HANDOFF.md, PR-BODY.md, MANIFEST.sha256, small receipts and indexed hashes/sizes for the retained captures. These are operator observations for the assigned reviewers.


A means reference peer to DUT.
B means DUT to reference peer.

R means the response precedes the unlock notification.
NC means the library reported NotConnected at that update.

Intervals are microseconds; actual holds are milliseconds.
Zero denotes no increment under the implemented Hive rule.

A intervals use the DUT-link tap.
B intervals use the controller-side control capture.

#### B12 A AAF: fixed holds

| Cycle | Requested / actual hold | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---|---|
| A0300-1 | 300 / 302.212 | SUCCESS | R / 697287.022 | NC | 0 |
| AAAF0300-2 | 300 / 302.801 | SUCCESS | R / 696519.351 | NC | 0 |
| AAAF0300-3 | 300 / 302.869 | SUCCESS | R / 696534.254 | NC | 0 |
| AAAF0300-4 | 300 / 302.945 | SUCCESS | R / 696428.971 | NC | 0 |
| AAAF0300-5 | 300 / 302.922 | SUCCESS | R / 696474.388 | NC | 0 |
| AAAF0600-1 | 600 / 603.064 | SUCCESS | R / 396366.064 | NC | 0 |
| AAAF0600-2 | 600 / 603.046 | SUCCESS | R / 396330.640 | NC | 0 |
| AAAF0600-3 | 600 / 602.996 | SUCCESS | R / 396434.112 | NC | 0 |
| AAAF0600-4 | 600 / 603.086 | SUCCESS | R / 396347.160 | NC | 0 |
| AAAF0600-5 | 600 / 602.861 | SUCCESS | R / 396564.641 | NC | 0 |
| AAAF0900-1 | 900 / 903.011 | SUCCESS | R / 96463.960 | NC | 0 |
| AAAF0900-2 | 900 / 903.056 | SUCCESS | R / 96406.344 | NC | 0 |
| AAAF0900-3 | 900 / 903.026 | SUCCESS | R / 96473.272 | NC | 0 |
| AAAF0900-4 | 900 / 903.020 | SUCCESS | R / 96495.201 | NC | 0 |
| AAAF0900-5 | 900 / 903.081 | SUCCESS | R / 96438.136 | NC | 0 |
| AAAF1000-1 | 1000 / 1002.737 | SUCCESS | R / 996684.408 | NC | 0 |
| AAAF1000-2 | 1000 / 1003.035 | SUCCESS | R / 996505.429 | NC | 0 |
| AAAF1000-3 | 1000 / 1002.956 | SUCCESS | R / 996627.510 | NC | 0 |
| AAAF1000-4 | 1000 / 1002.919 | SUCCESS | R / 996634.052 | NC | 0 |
| AAAF1000-5 | 1000 / 1002.886 | SUCCESS | R / 996679.192 | NC | 0 |
| AAAF1100-1 | 1100 / 1102.999 | SUCCESS | R / 896578.879 | NC | 0 |
| AAAF1100-2 | 1100 / 1103.057 | SUCCESS | R / 896539.469 | NC | 0 |
| AAAF1100-3 | 1100 / 1103.028 | SUCCESS | R / 896576.626 | NC | 0 |
| AAAF1100-4 | 1100 / 1102.982 | SUCCESS | R / 896603.715 | NC | 0 |
| AAAF1100-5 | 1100 / 1102.945 | SUCCESS | R / 896666.651 | NC | 0 |
| AAAF1500-1 | 1500 / 1502.891 | SUCCESS | R / 496761.823 | NC | 0 |
| AAAF1500-2 | 1500 / 1503.077 | SUCCESS | R / 496585.142 | NC | 0 |
| AAAF1500-3 | 1500 / 1502.977 | SUCCESS | R / 496621.463 | NC | 0 |
| AAAF1500-4 | 1500 / 1502.855 | SUCCESS | R / 496785.670 | NC | 0 |
| AAAF1500-5 | 1500 / 1503.052 | SUCCESS | R / 496664.865 | NC | 0 |
| AAAF3000-1 | 3000 / 3003.065 | SUCCESS | R / 115.448 | NC | 0 |
| AAAF3000-2 | 3000 / 3003.066 | SUCCESS | R / 116.552 | NC | 0 |
| AAAF3000-3 | 3000 / 3003.099 | SUCCESS | R / 116.056 | NC | 0 |
| AAAF3000-4 | 3000 / 3002.869 | SUCCESS | R / 116.280 | NC | 0 |
| AAAF3000-5 | 3000 / 3002.872 | SUCCESS | R / 114.984 | NC | 0 |

#### B12 A CRF: fixed holds

| Cycle | Requested / actual hold | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---|---|
| ACRF0300-1 | 300 / 300.831 | SUCCESS | R / 698909.558 | NC | 0 |
| ACRF0300-2 | 300 / 300.850 | SUCCESS | R / 698909.137 | NC | 0 |
| ACRF0300-3 | 300 / 300.882 | SUCCESS | R / 698883.415 | NC | 0 |
| ACRF0300-4 | 300 / 301.009 | SUCCESS | R / 698696.478 | NC | 0 |
| ACRF0300-5 | 300 / 300.959 | SUCCESS | R / 698750.321 | NC | 0 |
| ACRF0600-1 | 600 / 601.006 | SUCCESS | R / 398740.353 | NC | 0 |
| ACRF0600-2 | 600 / 601.028 | SUCCESS | R / 398705.481 | NC | 0 |
| ACRF0600-3 | 600 / 600.997 | SUCCESS | R / 398710.319 | NC | 0 |
| ACRF0600-4 | 600 / 600.920 | SUCCESS | R / 398777.537 | NC | 0 |
| ACRF0600-5 | 600 / 600.953 | SUCCESS | R / 398781.695 | NC | 0 |
| ACRF0900-1 | 900 / 900.911 | SUCCESS | R / 98860.025 | NC | 0 |
| ACRF0900-2 | 900 / 901.051 | SUCCESS | R / 98754.776 | NC | 0 |
| ACRF0900-3 | 900 / 900.864 | SUCCESS | R / 98920.424 | NC | 0 |
| ACRF0900-4 | 900 / 900.916 | SUCCESS | R / 1098870.791 | NC | 0 |
| ACRF0900-5 | 900 / 900.874 | SUCCESS | R / 98938.432 | NC | 0 |
| ACRF1000-1 | 1000 / 1001.182 | SUCCESS | R / 998546.534 | NC | 0 |
| ACRF1000-2 | 1000 / 1000.847 | SUCCESS | R / 998953.939 | NC | 0 |
| ACRF1000-3 | 1000 / 1000.932 | SUCCESS | R / 998903.541 | NC | 0 |
| ACRF1000-4 | 1000 / 1000.795 | SUCCESS | R / 999004.483 | NC | 0 |
| ACRF1000-5 | 1000 / 1000.898 | SUCCESS | R / 998919.234 | NC | 0 |
| ACRF1100-1 | 1100 / 1100.886 | SUCCESS | R / 898906.906 | NC | 0 |
| ACRF1100-2 | 1100 / 1100.751 | SUCCESS | R / 898953.714 | NC | 0 |
| ACRF1100-3 | 1100 / 1100.911 | SUCCESS | R / 898907.633 | NC | 0 |
| ACRF1100-4 | 1100 / 1100.832 | SUCCESS | R / 899004.891 | NC | 0 |
| ACRF1100-5 | 1100 / 1100.942 | SUCCESS | R / 898877.122 | NC | 0 |
| ACRF1500-1 | 1500 / 1500.872 | SUCCESS | R / 498942.563 | NC | 0 |
| ACRF1500-2 | 1500 / 1500.940 | SUCCESS | R / 498838.325 | NC | 0 |
| ACRF1500-3 | 1500 / 1500.911 | SUCCESS | R / 498968.947 | NC | 0 |
| ACRF1500-4 | 1500 / 1500.914 | SUCCESS | R / 498863.524 | NC | 0 |
| ACRF1500-5 | 1500 / 1500.937 | SUCCESS | R / 498889.645 | NC | 0 |
| ACRF3000-1 | 3000 / 3000.867 | SUCCESS | R / 99033.528 | NC | 0 |
| ACRF3000-2 | 3000 / 3000.873 | SUCCESS | R / 99481.786 | NC | 0 |
| ACRF3000-3 | 3000 / 3000.987 | SUCCESS | R / 98942.841 | NC | 0 |
| ACRF3000-4 | 3000 / 3000.917 | SUCCESS | R / 99596.234 | NC | 0 |
| ACRF3000-5 | 3000 / 3001.033 | SUCCESS | R / 98231.943 | NC | 0 |

#### B12 B AAF: fixed holds

| Cycle | Requested / actual hold | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---|---|
| BAAF0300-1 | 300 / 304.955 | SUCCESS | R / 694946.000 | NC | 0 |
| BAAF0300-2 | 300 / 300.464 | SUCCESS | R / 35576.000 | NC | EARLY +1 |
| BAAF0300-3 | 300 / 300.925 | SUCCESS | R / 381282.000 | NC | 0 |
| BAAF0300-4 | 300 / 300.539 | SUCCESS | R / 756916.000 | NC | 0 |
| BAAF0300-5 | 300 / 301.067 | SUCCESS | R / 122530.000 | NC | 0 |
| BAAF0600-1 | 600 / 600.758 | SUCCESS | R / 98177.000 | NC | 0 |
| BAAF0600-2 | 600 / 601.282 | SUCCESS | R / 83899.000 | NC | 0 |
| BAAF0600-3 | 600 / 601.163 | SUCCESS | R / 54534.000 | NC | 0 |
| BAAF0600-4 | 600 / 600.803 | SUCCESS | R / 90300.000 | NC | 0 |
| BAAF0600-5 | 600 / 600.529 | SUCCESS | R / 116050.000 | NC | 0 |
| BAAF0900-1 | 900 / 901.180 | SUCCESS | R / 876929.000 | NC | 0 |
| BAAF0900-2 | 900 / 901.072 | SUCCESS | R / 552663.000 | NC | 0 |
| BAAF0900-3 | 900 / 900.873 | SUCCESS | R / 328399.000 | NC | 0 |
| BAAF0900-4 | 900 / 901.208 | SUCCESS | R / 249261.000 | NC | 0 |
| BAAF0900-5 | 900 / 901.206 | SUCCESS | R / 535195.000 | NC | LATE +1 |
| BAAF1000-1 | 1000 / 1000.357 | SUCCESS | R / 581040.000 | NC | 0 |
| BAAF1000-2 | 1000 / 1000.501 | SUCCESS | R / 167042.000 | NC | 0 |
| BAAF1000-3 | 1000 / 1000.726 | SUCCESS | R / 242916.000 | NC | 0 |
| BAAF1000-4 | 1000 / 1000.898 | SUCCESS | R / 213792.000 | NC | 0 |
| BAAF1000-5 | 1000 / 1000.873 | SUCCESS | R / 199687.000 | NC | 0 |
| BAAF1100-1 | 1100 / 1101.291 | SUCCESS | R / 675799.000 | NC | 0 |
| BAAF1100-2 | 1100 / 1100.490 | SUCCESS | R / 616686.000 | NC | 0 |
| BAAF1100-3 | 1100 / 1100.901 | SUCCESS | R / 502440.000 | NC | 0 |
| BAAF1100-4 | 1100 / 1100.976 | SUCCESS | R / 843312.000 | NC | 0 |
| BAAF1100-5 | 1100 / 1100.966 | SUCCESS | R / 394069.000 | NC | 0 |
| BAAF1500-1 | 1500 / 1500.796 | SUCCESS | R / 510157.000 | NC | 0 |
| BAAF1500-2 | 1500 / 1500.964 | SUCCESS | R / 786030.000 | NC | 0 |
| BAAF1500-3 | 1500 / 1501.127 | SUCCESS | R / 41791.000 | NC | 0 |
| BAAF1500-4 | 1500 / 1501.283 | SUCCESS | R / 247615.000 | NC | 0 |
| BAAF1500-5 | 1500 / 1501.410 | SUCCESS | R / 438512.000 | NC | 0 |
| BAAF3000-1 | 3000 / 3000.595 | SUCCESS | R / 179402.000 | NC | 0 |
| BAAF3000-2 | 3000 / 3000.545 | SUCCESS | R / 830662.000 | NC | 0 |
| BAAF3000-3 | 3000 / 3000.506 | SUCCESS | R / 416655.000 | NC | 0 |
| BAAF3000-4 | 3000 / 3000.460 | SUCCESS | R / 142626.000 | NC | 0 |
| BAAF3000-5 | 3000 / 3000.392 | SUCCESS | R / 908773.000 | NC | 0 |

#### B12 B CRF: fixed holds

| Cycle | Requested / actual hold | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---|---|
| BCRF0300-1 | 300 / 303.545 | SUCCESS | R / 649162.000 | NC | 0 |
| BCRF0300-2 | 300 / 304.061 | SUCCESS | R / 989885.000 | NC | 0 |
| BCRF0300-3 | 300 / 303.725 | SUCCESS | R / 310364.000 | NC | 0 |
| BCRF0300-4 | 300 / 304.217 | SUCCESS | R / 646108.000 | NC | 0 |
| BCRF0300-5 | 300 / 303.956 | SUCCESS | R / 901775.000 | NC | 0 |
| BCRF0600-1 | 600 / 604.571 | SUCCESS | R / 877408.000 | NC | 0 |
| BCRF0600-2 | 600 / 604.305 | SUCCESS | R / 953049.000 | NC | 0 |
| BCRF0600-3 | 600 / 603.897 | SUCCESS | R / 933910.000 | NC | 0 |
| BCRF0600-4 | 600 / 604.746 | SUCCESS | R / 889526.000 | NC | 0 |
| BCRF0600-5 | 600 / 604.320 | SUCCESS | R / 870298.000 | NC | 0 |
| BCRF0900-1 | 900 / 905.489 | SUCCESS | R / 490542.000 | NC | 0 |
| BCRF0900-2 | 900 / 904.081 | SUCCESS | R / 196542.000 | NC | 0 |
| BCRF0900-3 | 900 / 903.760 | SUCCESS | R / 62415.000 | NC | 0 |
| BCRF0900-4 | 900 / 904.701 | SUCCESS | R / 843195.000 | NC | 0 |
| BCRF0900-5 | 900 / 904.382 | SUCCESS | R / 609048.000 | NC | 0 |
| BCRF1000-1 | 1000 / 1004.430 | SUCCESS | R / 239548.000 | NC | 0 |
| BCRF1000-2 | 1000 / 1004.328 | SUCCESS | R / 960441.000 | NC | 0 |
| BCRF1000-3 | 1000 / 1004.191 | SUCCESS | R / 546185.000 | NC | 0 |
| BCRF1000-4 | 1000 / 1004.077 | SUCCESS | R / 127249.000 | NC | 0 |
| BCRF1000-5 | 1000 / 1004.021 | SUCCESS | R / 703114.000 | NC | 0 |
| BCRF1100-1 | 1100 / 1104.261 | SUCCESS | R / 193508.000 | NC | 0 |
| BCRF1100-2 | 1100 / 1104.061 | SUCCESS | R / 719521.000 | NC | 0 |
| BCRF1100-3 | 1100 / 1103.968 | SUCCESS | R / 275269.000 | NC | 0 |
| BCRF1100-4 | 1100 / 1103.827 | SUCCESS | R / 821260.000 | NC | 0 |
| BCRF1100-5 | 1100 / 1103.989 | SUCCESS | R / 391770.000 | NC | 0 |
| BCRF1500-1 | 1500 / 1503.900 | SUCCESS | R / 487777.000 | NC | 0 |
| BCRF1500-2 | 1500 / 1504.053 | SUCCESS | R / 608523.000 | NC | 0 |
| BCRF1500-3 | 1500 / 1504.324 | SUCCESS | R / 664399.000 | NC | 0 |
| BCRF1500-4 | 1500 / 1504.530 | SUCCESS | R / 710281.000 | NC | 0 |
| BCRF1500-5 | 1500 / 1503.780 | SUCCESS | R / 771145.000 | NC | 0 |
| BCRF3000-1 | 3000 / 3003.943 | SUCCESS | R / 427275.000 | NC | 0 |
| BCRF3000-2 | 3000 / 3004.510 | SUCCESS | R / 38355.000 | NC | 0 |
| BCRF3000-3 | 3000 / 3004.469 | SUCCESS | R / 689551.000 | NC | 0 |
| BCRF3000-4 | 3000 / 3004.665 | SUCCESS | R / 265408.000 | NC | 0 |
| BCRF3000-5 | 3000 / 3003.459 | SUCCESS | R / 946664.000 | NC | 0 |

#### B12 push-boundary controls

The prior-push column measures push-to-unbind command time.
Before and after refer to the observed one-second cadence.

The prior-push column uses milliseconds.

| Cycle | Phase | Actual hold | Since prior push | Status | Order / interval | State | Hive increments |
|---|---|---:|---:|---|---:|---|---|
| AAAF-edge1025-1 | after | 1028.804 | 29.389 | SUCCESS | R / 970605.895 | NC | 0 |
| AAAF-edge1025-2 | after | 1028.792 | 29.387 | SUCCESS | R / 970607.590 | NC | 0 |
| AAAF-edge1025-3 | after | 1028.738 | 29.325 | SUCCESS | R / 970670.309 | NC | 0 |
| AAAF-edge1025-4 | after | 1028.795 | 29.359 | SUCCESS | R / 970636.940 | NC | 0 |
| AAAF-edge1025-5 | after | 1028.750 | 29.284 | SUCCESS | R / 970710.920 | NC | 0 |
| AAAF-edge975-1 | before | 978.811 | 978.740 | SUCCESS | R / 20531.850 | NC | 0 |
| AAAF-edge975-2 | before | 978.873 | 978.802 | SUCCESS | R / 20469.602 | NC | 0 |
| AAAF-edge975-3 | before | 978.777 | 978.705 | SUCCESS | R / 20608.795 | NC | 0 |
| AAAF-edge975-4 | before | 978.846 | 978.775 | SUCCESS | R / 20518.634 | NC | 0 |
| AAAF-edge975-5 | before | 978.754 | 978.683 | SUCCESS | R / 20652.250 | NC | 0 |
| ACRF-edge1025-1 | after | 1028.800 | 29.237 | SUCCESS | R / 970757.683 | NC | 0 |
| ACRF-edge1025-2 | after | 1028.806 | 29.214 | SUCCESS | R / 970780.873 | NC | 0 |
| ACRF-edge1025-3 | after | 1028.750 | 29.153 | SUCCESS | R / 970841.201 | NC | 0 |
| ACRF-edge1025-4 | after | 1028.743 | 29.150 | SUCCESS | R / 970846.090 | NC | 0 |
| ACRF-edge1025-5 | after | 1029.193 | 29.656 | SUCCESS | R / 970338.914 | NC | 0 |
| ACRF-edge975-1 | before | 978.754 | 978.684 | SUCCESS | R / 1020770.347 | NC | 0 |
| ACRF-edge975-2 | before | 978.784 | 978.714 | SUCCESS | R / 1020747.309 | NC | 0 |
| ACRF-edge975-3 | before | 978.866 | 978.796 | SUCCESS | R / 1020682.637 | NC | 0 |
| ACRF-edge975-4 | before | 978.880 | 978.811 | SUCCESS | R / 1020669.967 | NC | 0 |
| ACRF-edge975-5 | before | 978.766 | 978.696 | SUCCESS | R / 1020783.264 | NC | 0 |
| BAAF-edge1025-1 | after | 910.695 | 29.445 | SUCCESS | R / 970241.000 | NC | 0 |
| BAAF-edge1025-2 | after | 986.069 | 28.306 | SUCCESS | R / 971394.000 | NC | 0 |
| BAAF-edge1025-3 | after | 660.978 | 27.595 | SUCCESS | R / 972165.000 | NC | 0 |
| BAAF-edge1025-4 | after | 825.697 | 26.963 | SUCCESS | R / 972780.000 | NC | 0 |
| BAAF-edge1025-5 | after | 696.411 | 26.167 | SUCCESS | R / 973489.000 | NC | 0 |
| BAAF-edge975-1 | before | 1555.647 | 978.764 | SUCCESS | R / 21000.000 | NC | 0 |
| BAAF-edge975-2 | before | 1740.794 | 977.904 | SUCCESS | R / 21877.000 | NC | 0 |
| BAAF-edge975-3 | before | 1761.063 | 977.038 | SUCCESS | R / 22593.000 | NC | 0 |
| BAAF-edge975-4 | before | 1801.375 | 976.252 | SUCCESS | R / 23463.000 | NC | 0 |
| BAAF-edge975-5 | before | 1805.597 | 975.355 | SUCCESS | R / 24377.000 | NC | 0 |
| BCRF-edge1025-1 | after | 916.006 | 28.850 | SUCCESS | R / 970873.000 | NC | 0 |
| BCRF-edge1025-2 | after | 812.656 | 29.984 | SUCCESS | R / 969781.000 | NC | 0 |
| BCRF-edge1025-3 | after | 890.673 | 27.632 | SUCCESS | R / 972030.000 | NC | 0 |
| BCRF-edge1025-4 | after | 971.132 | 26.696 | SUCCESS | R / 973032.000 | NC | 0 |
| BCRF-edge1025-5 | after | 821.043 | 26.047 | SUCCESS | R / 973652.000 | NC | 0 |
| BCRF-edge975-1 | before | 1331.006 | 978.130 | SUCCESS | R / 21568.000 | NC | 0 |
| BCRF-edge975-2 | before | 1871.031 | 977.361 | SUCCESS | R / 22352.000 | NC | 0 |
| BCRF-edge975-3 | before | 1841.376 | 976.515 | SUCCESS | R / 23243.000 | NC | 0 |
| BCRF-edge975-4 | before | 1890.763 | 975.877 | SUCCESS | R / 23885.000 | NC | 0 |
| BCRF-edge975-5 | before | 1781.683 | 980.562 | SUCCESS | R / 19113.000 | NC | 0 |

### B12 sequence windows

Each window held its AAF binding for ten minutes.
Each listener received 300 scheduled counter polls.

| Cycle | Actual bound ms | SEQ / SI increments | Captured stream frames | Sequence gaps | Status | Order / interval | State | Hive increments |
|---|---:|---|---:|---:|---|---:|---|---|
| A-600s | 600005.422 | 0 / 0 | 4,799,477 | 0 | SUCCESS | R / 116.128 | NC | 0 |
| B-600s | 600006.707 | 0 / 0 | 4,798,340 | 0 | SUCCESS | R / 318749.000 | NC | 0 |

Capture reports recorded zero drops on the capture hosts.
Sequence checks cover captured headers, including truncated payload frames.

Each bind also received 20/100/250 ms counter reads.
All 546 early reads showed zero SEQ and SI.

The following examples show arbitrary starting sequence values.
Receipts preserve twelve initial PDUs for every cycle.

| Cycle | First twelve sequence numbers after bind command |
|---|---|
| A0300-1 | 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130 |
| BAAF0300-1 | 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199 |
| ACRF0300-1 | 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38 |
| BCRF0300-1 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 |
| A-600s | 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83 |
| B-600s | 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59 |

### B12 peer observations

The peer reported two timestamp-counter increments during short cycles.
They were EARLY +1 and LATE +1.

| Cycle | Controller callback time, UTC | Library state | Hive increment | Classification |
|---|---|---|---|---|
| BAAF0300-2 | 2026-10-05T11:19:04.049264+00:00 | NotConnected | EARLY +1 | Peer behaviour |
| BAAF0900-5 | 2026-10-05T11:20:10.059350+00:00 | Connected | LATE +1 | Peer behaviour |

These observations identify the reporting listener, not fault ownership.
Timestamp fault attribution remains unresolved.

The library also flagged peer STREAM_INFO reserved bit 24.
See Milan v1.2, Section 5.4.2.10.1.

That compatibility warning is separate from Hive counter increments.
No corresponding DUT compatibility change was observed.


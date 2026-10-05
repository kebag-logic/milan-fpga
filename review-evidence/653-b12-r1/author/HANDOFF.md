# [A543] B12 handoff

Refs #653. Completed 2026-10-05. Status: REVIEW READY.
Head: `bef8dd7036f711bf286929fa4cba6bf724c7118d`.
Branch: `653-b12-bench`; base: `fa450d301805881ad713b67521477bf042ddadfd`.
Only `docs/findings/653_DISCONNECT_ORDER_BENCH.md` changed.
Reviewers: [R498] internal and [R499] external, as assigned.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5993102892
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5993133081

Identity: PASS, all four assigned ATDECC facts. See `identity.json`.
Image: flashed dev `bbf704ec`. No flash, power, wiring, register-write or audio-playback action occurred.
Bench lock: released; the final nonblocking acquisition check returned 0.
Remote staging and this lane's capture files are removed. No lane process remains.
All eight controller sessions deregistered successfully from both entities.

## Results

All 182 unbinds returned SUCCESS and response-first ordering. The library input was NotConnected at each unlock update. Hive's rule counted zero MEDIA_UNLOCKED, STREAM_INTERRUPTED, SEQ_NUM_MISMATCH or UNSUPPORTED_FORMAT increments. The peer reported EARLY +1 and LATE +1 in two short AAF cycles. Timestamp fault attribution remains unresolved. A separate peer STREAM_INFO reserved-bit warning is recorded in `library-observations.json`.

The named source library was built and linked on the controller host. Runtime version: `5.0.0-beta1`; shared-library filename version: `5.0.0.1`. Source and binary hashes are in `build-provenance.json`. The initial JSON-disabled build failed; the default JSON-enabled build supplied every verdict. The full graphical application was outside this method.

There are 140 fixed-hold cycles, five per requested hold, direction and stream kind. Forty separate boundary cycles bracket the observed push cadence. Exact holds and independently selected push phases cannot both be prescribed; the added cycles make that interpretation explicit. Actual holds and phase offsets are retained.

The plain tap capture is accompanied by tagged-frame and controller control captures. A uses the DUT-link tap for intervals; B uses the controller control capture. No interval subtracts different capture clocks. All 546 capture logs report zero drops on their hosts.

Final decoding includes solicited pre-unbind observations when selecting an unlock increase. Nine early peer rows initially lacked a selected notification; their immutable original results remain in scratch storage. `cycles.csv`, `cycles-*.json`, this ledger and the findings page use the corrected grading. Eight raw-byte ordering controls and eight extracted-rule controls passed; the inverted rule predicate failed as expected.

## Cycle ledger

A: reference peer to DUT. B: DUT to reference peer.
Intervals are microseconds. Holds are milliseconds. NC: NotConnected at the unlock update. R: response first. Zero means no Hive-rule increment.

| Cycle | Direction / kind | Requested / actual hold | Phase | Status | Order / interval | State | Hive increments |
|---|---|---:|---|---|---:|---|---|
| A0300-1 | A / AAF | 300 / 302.212 | exact | SUCCESS | R / 697287.022 | NC | 0 |
| AAAF0300-2 | A / AAF | 300 / 302.801 | exact | SUCCESS | R / 696519.351 | NC | 0 |
| AAAF0300-3 | A / AAF | 300 / 302.869 | exact | SUCCESS | R / 696534.254 | NC | 0 |
| AAAF0300-4 | A / AAF | 300 / 302.945 | exact | SUCCESS | R / 696428.971 | NC | 0 |
| AAAF0300-5 | A / AAF | 300 / 302.922 | exact | SUCCESS | R / 696474.388 | NC | 0 |
| AAAF0600-1 | A / AAF | 600 / 603.064 | exact | SUCCESS | R / 396366.064 | NC | 0 |
| AAAF0600-2 | A / AAF | 600 / 603.046 | exact | SUCCESS | R / 396330.640 | NC | 0 |
| AAAF0600-3 | A / AAF | 600 / 602.996 | exact | SUCCESS | R / 396434.112 | NC | 0 |
| AAAF0600-4 | A / AAF | 600 / 603.086 | exact | SUCCESS | R / 396347.160 | NC | 0 |
| AAAF0600-5 | A / AAF | 600 / 602.861 | exact | SUCCESS | R / 396564.641 | NC | 0 |
| AAAF0900-1 | A / AAF | 900 / 903.011 | exact | SUCCESS | R / 96463.960 | NC | 0 |
| AAAF0900-2 | A / AAF | 900 / 903.056 | exact | SUCCESS | R / 96406.344 | NC | 0 |
| AAAF0900-3 | A / AAF | 900 / 903.026 | exact | SUCCESS | R / 96473.272 | NC | 0 |
| AAAF0900-4 | A / AAF | 900 / 903.020 | exact | SUCCESS | R / 96495.201 | NC | 0 |
| AAAF0900-5 | A / AAF | 900 / 903.081 | exact | SUCCESS | R / 96438.136 | NC | 0 |
| AAAF1000-1 | A / AAF | 1000 / 1002.737 | exact | SUCCESS | R / 996684.408 | NC | 0 |
| AAAF1000-2 | A / AAF | 1000 / 1003.035 | exact | SUCCESS | R / 996505.429 | NC | 0 |
| AAAF1000-3 | A / AAF | 1000 / 1002.956 | exact | SUCCESS | R / 996627.510 | NC | 0 |
| AAAF1000-4 | A / AAF | 1000 / 1002.919 | exact | SUCCESS | R / 996634.052 | NC | 0 |
| AAAF1000-5 | A / AAF | 1000 / 1002.886 | exact | SUCCESS | R / 996679.192 | NC | 0 |
| AAAF1100-1 | A / AAF | 1100 / 1102.999 | exact | SUCCESS | R / 896578.879 | NC | 0 |
| AAAF1100-2 | A / AAF | 1100 / 1103.057 | exact | SUCCESS | R / 896539.469 | NC | 0 |
| AAAF1100-3 | A / AAF | 1100 / 1103.028 | exact | SUCCESS | R / 896576.626 | NC | 0 |
| AAAF1100-4 | A / AAF | 1100 / 1102.982 | exact | SUCCESS | R / 896603.715 | NC | 0 |
| AAAF1100-5 | A / AAF | 1100 / 1102.945 | exact | SUCCESS | R / 896666.651 | NC | 0 |
| AAAF1500-1 | A / AAF | 1500 / 1502.891 | exact | SUCCESS | R / 496761.823 | NC | 0 |
| AAAF1500-2 | A / AAF | 1500 / 1503.077 | exact | SUCCESS | R / 496585.142 | NC | 0 |
| AAAF1500-3 | A / AAF | 1500 / 1502.977 | exact | SUCCESS | R / 496621.463 | NC | 0 |
| AAAF1500-4 | A / AAF | 1500 / 1502.855 | exact | SUCCESS | R / 496785.670 | NC | 0 |
| AAAF1500-5 | A / AAF | 1500 / 1503.052 | exact | SUCCESS | R / 496664.865 | NC | 0 |
| AAAF3000-1 | A / AAF | 3000 / 3003.065 | exact | SUCCESS | R / 115.448 | NC | 0 |
| AAAF3000-2 | A / AAF | 3000 / 3003.066 | exact | SUCCESS | R / 116.552 | NC | 0 |
| AAAF3000-3 | A / AAF | 3000 / 3003.099 | exact | SUCCESS | R / 116.056 | NC | 0 |
| AAAF3000-4 | A / AAF | 3000 / 3002.869 | exact | SUCCESS | R / 116.280 | NC | 0 |
| AAAF3000-5 | A / AAF | 3000 / 3002.872 | exact | SUCCESS | R / 114.984 | NC | 0 |
| BAAF0300-1 | B / AAF | 300 / 304.955 | exact | SUCCESS | R / 694946.000 | NC | 0 |
| BAAF0300-2 | B / AAF | 300 / 300.464 | exact | SUCCESS | R / 35576.000 | NC | EARLY +1 |
| BAAF0300-3 | B / AAF | 300 / 300.925 | exact | SUCCESS | R / 381282.000 | NC | 0 |
| BAAF0300-4 | B / AAF | 300 / 300.539 | exact | SUCCESS | R / 756916.000 | NC | 0 |
| BAAF0300-5 | B / AAF | 300 / 301.067 | exact | SUCCESS | R / 122530.000 | NC | 0 |
| BAAF0600-1 | B / AAF | 600 / 600.758 | exact | SUCCESS | R / 98177.000 | NC | 0 |
| BAAF0600-2 | B / AAF | 600 / 601.282 | exact | SUCCESS | R / 83899.000 | NC | 0 |
| BAAF0600-3 | B / AAF | 600 / 601.163 | exact | SUCCESS | R / 54534.000 | NC | 0 |
| BAAF0600-4 | B / AAF | 600 / 600.803 | exact | SUCCESS | R / 90300.000 | NC | 0 |
| BAAF0600-5 | B / AAF | 600 / 600.529 | exact | SUCCESS | R / 116050.000 | NC | 0 |
| BAAF0900-1 | B / AAF | 900 / 901.180 | exact | SUCCESS | R / 876929.000 | NC | 0 |
| BAAF0900-2 | B / AAF | 900 / 901.072 | exact | SUCCESS | R / 552663.000 | NC | 0 |
| BAAF0900-3 | B / AAF | 900 / 900.873 | exact | SUCCESS | R / 328399.000 | NC | 0 |
| BAAF0900-4 | B / AAF | 900 / 901.208 | exact | SUCCESS | R / 249261.000 | NC | 0 |
| BAAF0900-5 | B / AAF | 900 / 901.206 | exact | SUCCESS | R / 535195.000 | NC | LATE +1 |
| BAAF1000-1 | B / AAF | 1000 / 1000.357 | exact | SUCCESS | R / 581040.000 | NC | 0 |
| BAAF1000-2 | B / AAF | 1000 / 1000.501 | exact | SUCCESS | R / 167042.000 | NC | 0 |
| BAAF1000-3 | B / AAF | 1000 / 1000.726 | exact | SUCCESS | R / 242916.000 | NC | 0 |
| BAAF1000-4 | B / AAF | 1000 / 1000.898 | exact | SUCCESS | R / 213792.000 | NC | 0 |
| BAAF1000-5 | B / AAF | 1000 / 1000.873 | exact | SUCCESS | R / 199687.000 | NC | 0 |
| BAAF1100-1 | B / AAF | 1100 / 1101.291 | exact | SUCCESS | R / 675799.000 | NC | 0 |
| BAAF1100-2 | B / AAF | 1100 / 1100.490 | exact | SUCCESS | R / 616686.000 | NC | 0 |
| BAAF1100-3 | B / AAF | 1100 / 1100.901 | exact | SUCCESS | R / 502440.000 | NC | 0 |
| BAAF1100-4 | B / AAF | 1100 / 1100.976 | exact | SUCCESS | R / 843312.000 | NC | 0 |
| BAAF1100-5 | B / AAF | 1100 / 1100.966 | exact | SUCCESS | R / 394069.000 | NC | 0 |
| BAAF1500-1 | B / AAF | 1500 / 1500.796 | exact | SUCCESS | R / 510157.000 | NC | 0 |
| BAAF1500-2 | B / AAF | 1500 / 1500.964 | exact | SUCCESS | R / 786030.000 | NC | 0 |
| BAAF1500-3 | B / AAF | 1500 / 1501.127 | exact | SUCCESS | R / 41791.000 | NC | 0 |
| BAAF1500-4 | B / AAF | 1500 / 1501.283 | exact | SUCCESS | R / 247615.000 | NC | 0 |
| BAAF1500-5 | B / AAF | 1500 / 1501.410 | exact | SUCCESS | R / 438512.000 | NC | 0 |
| BAAF3000-1 | B / AAF | 3000 / 3000.595 | exact | SUCCESS | R / 179402.000 | NC | 0 |
| BAAF3000-2 | B / AAF | 3000 / 3000.545 | exact | SUCCESS | R / 830662.000 | NC | 0 |
| BAAF3000-3 | B / AAF | 3000 / 3000.506 | exact | SUCCESS | R / 416655.000 | NC | 0 |
| BAAF3000-4 | B / AAF | 3000 / 3000.460 | exact | SUCCESS | R / 142626.000 | NC | 0 |
| BAAF3000-5 | B / AAF | 3000 / 3000.392 | exact | SUCCESS | R / 908773.000 | NC | 0 |
| ACRF0300-1 | A / CRF | 300 / 300.831 | exact | SUCCESS | R / 698909.558 | NC | 0 |
| ACRF0300-2 | A / CRF | 300 / 300.850 | exact | SUCCESS | R / 698909.137 | NC | 0 |
| ACRF0300-3 | A / CRF | 300 / 300.882 | exact | SUCCESS | R / 698883.415 | NC | 0 |
| ACRF0300-4 | A / CRF | 300 / 301.009 | exact | SUCCESS | R / 698696.478 | NC | 0 |
| ACRF0300-5 | A / CRF | 300 / 300.959 | exact | SUCCESS | R / 698750.321 | NC | 0 |
| ACRF0600-1 | A / CRF | 600 / 601.006 | exact | SUCCESS | R / 398740.353 | NC | 0 |
| ACRF0600-2 | A / CRF | 600 / 601.028 | exact | SUCCESS | R / 398705.481 | NC | 0 |
| ACRF0600-3 | A / CRF | 600 / 600.997 | exact | SUCCESS | R / 398710.319 | NC | 0 |
| ACRF0600-4 | A / CRF | 600 / 600.920 | exact | SUCCESS | R / 398777.537 | NC | 0 |
| ACRF0600-5 | A / CRF | 600 / 600.953 | exact | SUCCESS | R / 398781.695 | NC | 0 |
| ACRF0900-1 | A / CRF | 900 / 900.911 | exact | SUCCESS | R / 98860.025 | NC | 0 |
| ACRF0900-2 | A / CRF | 900 / 901.051 | exact | SUCCESS | R / 98754.776 | NC | 0 |
| ACRF0900-3 | A / CRF | 900 / 900.864 | exact | SUCCESS | R / 98920.424 | NC | 0 |
| ACRF0900-4 | A / CRF | 900 / 900.916 | exact | SUCCESS | R / 1098870.791 | NC | 0 |
| ACRF0900-5 | A / CRF | 900 / 900.874 | exact | SUCCESS | R / 98938.432 | NC | 0 |
| ACRF1000-1 | A / CRF | 1000 / 1001.182 | exact | SUCCESS | R / 998546.534 | NC | 0 |
| ACRF1000-2 | A / CRF | 1000 / 1000.847 | exact | SUCCESS | R / 998953.939 | NC | 0 |
| ACRF1000-3 | A / CRF | 1000 / 1000.932 | exact | SUCCESS | R / 998903.541 | NC | 0 |
| ACRF1000-4 | A / CRF | 1000 / 1000.795 | exact | SUCCESS | R / 999004.483 | NC | 0 |
| ACRF1000-5 | A / CRF | 1000 / 1000.898 | exact | SUCCESS | R / 998919.234 | NC | 0 |
| ACRF1100-1 | A / CRF | 1100 / 1100.886 | exact | SUCCESS | R / 898906.906 | NC | 0 |
| ACRF1100-2 | A / CRF | 1100 / 1100.751 | exact | SUCCESS | R / 898953.714 | NC | 0 |
| ACRF1100-3 | A / CRF | 1100 / 1100.911 | exact | SUCCESS | R / 898907.633 | NC | 0 |
| ACRF1100-4 | A / CRF | 1100 / 1100.832 | exact | SUCCESS | R / 899004.891 | NC | 0 |
| ACRF1100-5 | A / CRF | 1100 / 1100.942 | exact | SUCCESS | R / 898877.122 | NC | 0 |
| ACRF1500-1 | A / CRF | 1500 / 1500.872 | exact | SUCCESS | R / 498942.563 | NC | 0 |
| ACRF1500-2 | A / CRF | 1500 / 1500.940 | exact | SUCCESS | R / 498838.325 | NC | 0 |
| ACRF1500-3 | A / CRF | 1500 / 1500.911 | exact | SUCCESS | R / 498968.947 | NC | 0 |
| ACRF1500-4 | A / CRF | 1500 / 1500.914 | exact | SUCCESS | R / 498863.524 | NC | 0 |
| ACRF1500-5 | A / CRF | 1500 / 1500.937 | exact | SUCCESS | R / 498889.645 | NC | 0 |
| ACRF3000-1 | A / CRF | 3000 / 3000.867 | exact | SUCCESS | R / 99033.528 | NC | 0 |
| ACRF3000-2 | A / CRF | 3000 / 3000.873 | exact | SUCCESS | R / 99481.786 | NC | 0 |
| ACRF3000-3 | A / CRF | 3000 / 3000.987 | exact | SUCCESS | R / 98942.841 | NC | 0 |
| ACRF3000-4 | A / CRF | 3000 / 3000.917 | exact | SUCCESS | R / 99596.234 | NC | 0 |
| ACRF3000-5 | A / CRF | 3000 / 3001.033 | exact | SUCCESS | R / 98231.943 | NC | 0 |
| BCRF0300-1 | B / CRF | 300 / 303.545 | exact | SUCCESS | R / 649162.000 | NC | 0 |
| BCRF0300-2 | B / CRF | 300 / 304.061 | exact | SUCCESS | R / 989885.000 | NC | 0 |
| BCRF0300-3 | B / CRF | 300 / 303.725 | exact | SUCCESS | R / 310364.000 | NC | 0 |
| BCRF0300-4 | B / CRF | 300 / 304.217 | exact | SUCCESS | R / 646108.000 | NC | 0 |
| BCRF0300-5 | B / CRF | 300 / 303.956 | exact | SUCCESS | R / 901775.000 | NC | 0 |
| BCRF0600-1 | B / CRF | 600 / 604.571 | exact | SUCCESS | R / 877408.000 | NC | 0 |
| BCRF0600-2 | B / CRF | 600 / 604.305 | exact | SUCCESS | R / 953049.000 | NC | 0 |
| BCRF0600-3 | B / CRF | 600 / 603.897 | exact | SUCCESS | R / 933910.000 | NC | 0 |
| BCRF0600-4 | B / CRF | 600 / 604.746 | exact | SUCCESS | R / 889526.000 | NC | 0 |
| BCRF0600-5 | B / CRF | 600 / 604.320 | exact | SUCCESS | R / 870298.000 | NC | 0 |
| BCRF0900-1 | B / CRF | 900 / 905.489 | exact | SUCCESS | R / 490542.000 | NC | 0 |
| BCRF0900-2 | B / CRF | 900 / 904.081 | exact | SUCCESS | R / 196542.000 | NC | 0 |
| BCRF0900-3 | B / CRF | 900 / 903.760 | exact | SUCCESS | R / 62415.000 | NC | 0 |
| BCRF0900-4 | B / CRF | 900 / 904.701 | exact | SUCCESS | R / 843195.000 | NC | 0 |
| BCRF0900-5 | B / CRF | 900 / 904.382 | exact | SUCCESS | R / 609048.000 | NC | 0 |
| BCRF1000-1 | B / CRF | 1000 / 1004.430 | exact | SUCCESS | R / 239548.000 | NC | 0 |
| BCRF1000-2 | B / CRF | 1000 / 1004.328 | exact | SUCCESS | R / 960441.000 | NC | 0 |
| BCRF1000-3 | B / CRF | 1000 / 1004.191 | exact | SUCCESS | R / 546185.000 | NC | 0 |
| BCRF1000-4 | B / CRF | 1000 / 1004.077 | exact | SUCCESS | R / 127249.000 | NC | 0 |
| BCRF1000-5 | B / CRF | 1000 / 1004.021 | exact | SUCCESS | R / 703114.000 | NC | 0 |
| BCRF1100-1 | B / CRF | 1100 / 1104.261 | exact | SUCCESS | R / 193508.000 | NC | 0 |
| BCRF1100-2 | B / CRF | 1100 / 1104.061 | exact | SUCCESS | R / 719521.000 | NC | 0 |
| BCRF1100-3 | B / CRF | 1100 / 1103.968 | exact | SUCCESS | R / 275269.000 | NC | 0 |
| BCRF1100-4 | B / CRF | 1100 / 1103.827 | exact | SUCCESS | R / 821260.000 | NC | 0 |
| BCRF1100-5 | B / CRF | 1100 / 1103.989 | exact | SUCCESS | R / 391770.000 | NC | 0 |
| BCRF1500-1 | B / CRF | 1500 / 1503.900 | exact | SUCCESS | R / 487777.000 | NC | 0 |
| BCRF1500-2 | B / CRF | 1500 / 1504.053 | exact | SUCCESS | R / 608523.000 | NC | 0 |
| BCRF1500-3 | B / CRF | 1500 / 1504.324 | exact | SUCCESS | R / 664399.000 | NC | 0 |
| BCRF1500-4 | B / CRF | 1500 / 1504.530 | exact | SUCCESS | R / 710281.000 | NC | 0 |
| BCRF1500-5 | B / CRF | 1500 / 1503.780 | exact | SUCCESS | R / 771145.000 | NC | 0 |
| BCRF3000-1 | B / CRF | 3000 / 3003.943 | exact | SUCCESS | R / 427275.000 | NC | 0 |
| BCRF3000-2 | B / CRF | 3000 / 3004.510 | exact | SUCCESS | R / 38355.000 | NC | 0 |
| BCRF3000-3 | B / CRF | 3000 / 3004.469 | exact | SUCCESS | R / 689551.000 | NC | 0 |
| BCRF3000-4 | B / CRF | 3000 / 3004.665 | exact | SUCCESS | R / 265408.000 | NC | 0 |
| BCRF3000-5 | B / CRF | 3000 / 3003.459 | exact | SUCCESS | R / 946664.000 | NC | 0 |
| AAAF-edge975-1 | A / AAF | 975 / 978.811 | before | SUCCESS | R / 20531.850 | NC | 0 |
| AAAF-edge975-2 | A / AAF | 975 / 978.873 | before | SUCCESS | R / 20469.602 | NC | 0 |
| AAAF-edge975-3 | A / AAF | 975 / 978.777 | before | SUCCESS | R / 20608.795 | NC | 0 |
| AAAF-edge975-4 | A / AAF | 975 / 978.846 | before | SUCCESS | R / 20518.634 | NC | 0 |
| AAAF-edge975-5 | A / AAF | 975 / 978.754 | before | SUCCESS | R / 20652.250 | NC | 0 |
| AAAF-edge1025-1 | A / AAF | 1025 / 1028.804 | after | SUCCESS | R / 970605.895 | NC | 0 |
| AAAF-edge1025-2 | A / AAF | 1025 / 1028.792 | after | SUCCESS | R / 970607.590 | NC | 0 |
| AAAF-edge1025-3 | A / AAF | 1025 / 1028.738 | after | SUCCESS | R / 970670.309 | NC | 0 |
| AAAF-edge1025-4 | A / AAF | 1025 / 1028.795 | after | SUCCESS | R / 970636.940 | NC | 0 |
| AAAF-edge1025-5 | A / AAF | 1025 / 1028.750 | after | SUCCESS | R / 970710.920 | NC | 0 |
| BAAF-edge975-1 | B / AAF | 975 / 1555.647 | before | SUCCESS | R / 21000.000 | NC | 0 |
| BAAF-edge975-2 | B / AAF | 975 / 1740.794 | before | SUCCESS | R / 21877.000 | NC | 0 |
| BAAF-edge975-3 | B / AAF | 975 / 1761.063 | before | SUCCESS | R / 22593.000 | NC | 0 |
| BAAF-edge975-4 | B / AAF | 975 / 1801.375 | before | SUCCESS | R / 23463.000 | NC | 0 |
| BAAF-edge975-5 | B / AAF | 975 / 1805.597 | before | SUCCESS | R / 24377.000 | NC | 0 |
| BAAF-edge1025-1 | B / AAF | 1025 / 910.695 | after | SUCCESS | R / 970241.000 | NC | 0 |
| BAAF-edge1025-2 | B / AAF | 1025 / 986.069 | after | SUCCESS | R / 971394.000 | NC | 0 |
| BAAF-edge1025-3 | B / AAF | 1025 / 660.978 | after | SUCCESS | R / 972165.000 | NC | 0 |
| BAAF-edge1025-4 | B / AAF | 1025 / 825.697 | after | SUCCESS | R / 972780.000 | NC | 0 |
| BAAF-edge1025-5 | B / AAF | 1025 / 696.411 | after | SUCCESS | R / 973489.000 | NC | 0 |
| ACRF-edge975-1 | A / CRF | 975 / 978.754 | before | SUCCESS | R / 1020770.347 | NC | 0 |
| ACRF-edge975-2 | A / CRF | 975 / 978.784 | before | SUCCESS | R / 1020747.309 | NC | 0 |
| ACRF-edge975-3 | A / CRF | 975 / 978.866 | before | SUCCESS | R / 1020682.637 | NC | 0 |
| ACRF-edge975-4 | A / CRF | 975 / 978.880 | before | SUCCESS | R / 1020669.967 | NC | 0 |
| ACRF-edge975-5 | A / CRF | 975 / 978.766 | before | SUCCESS | R / 1020783.264 | NC | 0 |
| ACRF-edge1025-1 | A / CRF | 1025 / 1028.800 | after | SUCCESS | R / 970757.683 | NC | 0 |
| ACRF-edge1025-2 | A / CRF | 1025 / 1028.806 | after | SUCCESS | R / 970780.873 | NC | 0 |
| ACRF-edge1025-3 | A / CRF | 1025 / 1028.750 | after | SUCCESS | R / 970841.201 | NC | 0 |
| ACRF-edge1025-4 | A / CRF | 1025 / 1028.743 | after | SUCCESS | R / 970846.090 | NC | 0 |
| ACRF-edge1025-5 | A / CRF | 1025 / 1029.193 | after | SUCCESS | R / 970338.914 | NC | 0 |
| BCRF-edge975-1 | B / CRF | 975 / 1331.006 | before | SUCCESS | R / 21568.000 | NC | 0 |
| BCRF-edge975-2 | B / CRF | 975 / 1871.031 | before | SUCCESS | R / 22352.000 | NC | 0 |
| BCRF-edge975-3 | B / CRF | 975 / 1841.376 | before | SUCCESS | R / 23243.000 | NC | 0 |
| BCRF-edge975-4 | B / CRF | 975 / 1890.763 | before | SUCCESS | R / 23885.000 | NC | 0 |
| BCRF-edge975-5 | B / CRF | 975 / 1781.683 | before | SUCCESS | R / 19113.000 | NC | 0 |
| BCRF-edge1025-1 | B / CRF | 1025 / 916.006 | after | SUCCESS | R / 970873.000 | NC | 0 |
| BCRF-edge1025-2 | B / CRF | 1025 / 812.656 | after | SUCCESS | R / 969781.000 | NC | 0 |
| BCRF-edge1025-3 | B / CRF | 1025 / 890.673 | after | SUCCESS | R / 972030.000 | NC | 0 |
| BCRF-edge1025-4 | B / CRF | 1025 / 971.132 | after | SUCCESS | R / 973032.000 | NC | 0 |
| BCRF-edge1025-5 | B / CRF | 1025 / 821.043 | after | SUCCESS | R / 973652.000 | NC | 0 |
| A-600s | A / AAF | 600000 / 600005.422 | exact | SUCCESS | R / 116.128 | NC | 0 |
| B-600s | B / AAF | 600000 / 600006.707 | exact | SUCCESS | R / 318749.000 | NC | 0 |

## Sequence windows

| Direction | Bound duration | Scheduled polls | SEQ / SI increments | Captured frames / gaps |
|---|---|---|---|---|
| Reference peer to DUT | 600.005422 s | 300 at 2 s | 0 / 0 | 4,799,477 / 0 |
| DUT to reference peer | 600.006707 s | 300 at 2 s | 0 / 0 | 4,798,340 / 0 |

All 1,510 counter reads succeeded. All 546 early 20/100/250 ms reads showed zero SEQ and SI. The first twelve wire PDUs after every bind command are preserved in `wire-receipts-*.json`. Poll timestamps and values are in `short-polls.csv` and `long-polls.csv`.

## Restore ledger

| Role | Category | Readbacks | Comparison |
|---|---|---:|---|
| dut | bindings | 4 | Equal to baseline |
| dut | formats | 4 | Equal to baseline |
| dut | maps | 2 | Equal to baseline |
| dut | clocks | 2 | Equal to baseline |
| peer | bindings | 14 | Equal to baseline |
| peer | formats | 14 | Equal to baseline |
| peer | maps | 2 | Equal to baseline |
| peer | clocks | 1 | Equal to baseline |

All streams are unbound. The DUT servo returned to its as-found IDLE word, 0x00000020. The established AEM source-release sequence cleared CRF-induced holdover and read back the original selection. Format and map writes were unnecessary.

NVM image sequence advanced 98 to 230; successful commits advanced 67 to 199. Failed commits stayed zero; dirty and stale remained clear. Monotonic counters were not rolled back. The required board-link address and UAC2 card remained present; a read-only root-shell check passed. No bridge restart was performed.

`restore-comparison.json` records semantic equality and hashes; `restore-summary.json` records residuals. `controller-cleanup.json`, `tap-cleanup.json`, `host-prerequisites-end.json` and `soc-readonly-end.json` record the final checks.

## Validation and artifacts

Every required final gate returned 0 on the committed head. `validation.json` records exact commands, the physical worktree, the pinned Markdown interpreter and log names. The em-dash gate inspected all 424 added lines. The initial wording-gate failure is retained separately.

`MANIFEST.sha256` covers the packet. Every packet file is at most 200,000 bytes. No binaries, archives, source-tree exports, installed packages or large captures are inside it. `artifacts-*.csv` lists retained scratch evidence with absolute scratch locations, byte sizes and SHA-256 values. All 546 live captures and seven synthetic capture controls remain under `/tmp/653-b12/raw`; the newly built library binaries and probe executables remain under `/tmp/653-b12` with hashes verified after transfer.

`PR-BODY.md` contains the proposed description. `REVIEW-READY.md` contains the issue comment and every per-cycle table. The branch is local; no push, PR operation or merge was performed.

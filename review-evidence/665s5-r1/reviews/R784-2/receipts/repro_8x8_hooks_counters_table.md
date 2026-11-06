### 8x8, CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz, face arm answering

Graded against the bounds in the tree at this base. The amended column gives the owner's decisions of 2026-11-06 on #665, for information: it grades nothing, and this harness re-grades when #810 merges.

| Hook | Paths | Over its bound | Within it by less than the layout swing | Worst alone, ms (bound) | Worst under the composed load, ms (bound) | Amended service bound, ms, for information | Ordering check applied (undecided) | Ordering findings |
|---|---:|---:|---:|---|---|---:|---:|---:|
| H-ADP | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-DISC | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-ACMP | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-AECP | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-NOTIFY | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-COUNTERS | 22 | 19 | 0 | 218.712 (20) **over its bound**, `counters.all.if0`, margin 781.3 of 1000 | - | 20, 60 | 32 (0) | 0 |
| H-MAAP | 0 | 0 | 0 | - | - | - | 2 (0) | 0 |
| H-SRP | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |

| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound at this base, ms | Amended bound, ms, for information | Within | Slack, CPU cycles | Under load | Margin to the normative timeout, ms |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|---:|
| H-COUNTERS | `counters.all.if0` | hooks-counters | 0 | 218.712 | 21,871,183 | 0 | 20 | 60 | NO | -19,871,183 | no | 781.288 of 1000 |
| H-COUNTERS | `counters.all.t36.i0.if0` | hooks-counters | 0 | 218.712 | 21,871,183 | 0 | 20 | 60 | NO | -19,871,183 | no | 781.288 of 1000 |
| H-COUNTERS | `counters.all.t5.i1.if0` | hooks-counters | 0 | 21.699 | 2,169,871 | 0 | 20 | 60 | NO | -169,871 | no | 978.301 of 1000 |
| H-COUNTERS | `counters.all.t5.i2.if0` | hooks-counters | 0 | 33.434 | 3,343,421 | 0 | 20 | 60 | NO | -1,343,421 | no | 966.566 of 1000 |
| H-COUNTERS | `counters.all.t5.i3.if0` | hooks-counters | 0 | 44.890 | 4,489,005 | 0 | 20 | 60 | NO | -2,489,005 | no | 955.110 of 1000 |
| H-COUNTERS | `counters.all.t5.i4.if0` | hooks-counters | 0 | 57.150 | 5,715,022 | 0 | 20 | 60 | NO | -3,715,022 | no | 942.850 of 1000 |
| H-COUNTERS | `counters.all.t5.i5.if0` | hooks-counters | 0 | 68.580 | 6,857,973 | 0 | 20 | 60 | NO | -4,857,973 | no | 931.420 of 1000 |
| H-COUNTERS | `counters.all.t5.i6.if0` | hooks-counters | 0 | 80.066 | 8,006,635 | 0 | 20 | 60 | NO | -6,006,635 | no | 919.934 of 1000 |
| H-COUNTERS | `counters.all.t5.i7.if0` | hooks-counters | 0 | 91.535 | 9,153,484 | 0 | 20 | 60 | NO | -7,153,484 | no | 908.465 of 1000 |
| H-COUNTERS | `counters.all.t5.i8.if0` | hooks-counters | 0 | 103.252 | 10,325,175 | 0 | 20 | 60 | NO | -8,325,175 | no | 896.748 of 1000 |
| H-COUNTERS | `counters.all.t6.i0.if0` | hooks-counters | 0 | 10.551 | 1,055,053 | 0 | 20 | 60 | yes | 944,947 | no | 989.449 of 1000 |
| H-COUNTERS | `counters.all.t6.i1.if0` | hooks-counters | 0 | 114.696 | 11,469,575 | 0 | 20 | 60 | NO | -9,469,575 | no | 885.304 of 1000 |
| H-COUNTERS | `counters.all.t6.i2.if0` | hooks-counters | 0 | 126.196 | 12,619,556 | 0 | 20 | 60 | NO | -10,619,556 | no | 873.804 of 1000 |
| H-COUNTERS | `counters.all.t6.i3.if0` | hooks-counters | 0 | 137.678 | 13,767,770 | 0 | 20 | 60 | NO | -11,767,770 | no | 862.322 of 1000 |
| H-COUNTERS | `counters.all.t6.i4.if0` | hooks-counters | 0 | 149.146 | 14,914,595 | 0 | 20 | 60 | NO | -12,914,595 | no | 850.854 of 1000 |
| H-COUNTERS | `counters.all.t6.i5.if0` | hooks-counters | 0 | 160.605 | 16,060,462 | 0 | 20 | 60 | NO | -14,060,462 | no | 839.395 of 1000 |
| H-COUNTERS | `counters.all.t6.i6.if0` | hooks-counters | 0 | 172.118 | 17,211,764 | 0 | 20 | 60 | NO | -15,211,764 | no | 827.882 of 1000 |
| H-COUNTERS | `counters.all.t6.i7.if0` | hooks-counters | 0 | 183.874 | 18,387,375 | 0 | 20 | 60 | NO | -16,387,375 | no | 816.126 of 1000 |
| H-COUNTERS | `counters.all.t6.i8.if0` | hooks-counters | 0 | 195.356 | 19,535,580 | 0 | 20 | 60 | NO | -17,535,580 | no | 804.644 of 1000 |
| H-COUNTERS | `counters.all.t9.i0.if0` | hooks-counters | 0 | 206.826 | 20,682,606 | 0 | 20 | 60 | NO | -18,682,606 | no | 793.174 of 1000 |
| H-COUNTERS | `counters.first.if0` | hooks-counters | 0 | 10.164 | 1,016,443 | 0 | 20 | 20 | yes | 983,557 | no | 989.836 of 1000 |
| H-COUNTERS | `counters.held.if0` | hooks-counters | 0 | 9.931 | 993,084 | 880.002 | 20 | 20 | yes | 1,006,916 | no | 110.067 of 1000 |

Refusals:

- none

Probes of the CPU budget harness this harness measured again (hooks.SUPERSEDED):

- none

Findings:

- LATE H-COUNTERS: counters.all.if0: 218.712 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i1.if0: 21.699 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i2.if0: 33.434 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i3.if0: 44.890 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i4.if0: 57.150 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i5.if0: 68.580 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i6.if0: 80.066 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i7.if0: 91.535 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i8.if0: 103.252 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i1.if0: 114.696 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i2.if0: 126.196 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i3.if0: 137.678 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i4.if0: 149.146 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i5.if0: 160.605 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i6.if0: 172.118 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i7.if0: 183.874 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i8.if0: 195.356 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t9.i0.if0: 206.826 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t36.i0.if0: 218.712 ms against its bound 20 ms (hooks-counters)

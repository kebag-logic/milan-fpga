# aecp-fanout group, arm A, 8x8: S2's final regrade beside this head

reference: 665s2-a681e/receipts/head-regrade/A8/table.md (sha256 599f196187b5fd5d...)
this run: AF8/results/table.md (sha256 27e72ff342eb25e8...)

reference rows 13, this run 13, common 13
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp_fanout.lock_entity.if0 | 803,735 | 16.075 | MISS T_svc | 825,430 | 662 | 837,681 | 16.754 | MISS T_svc | 860,954 | 686 | +0.679 | +24 |
| aecp_fanout.lock_entity.if1 | 819,673 | 16.393 | MISS T_svc | 824,048 | 662 | 814,768 | 16.295 | MISS T_svc | 821,427 | 679 | -0.098 | +17 |
| aecp_fanout.set_clock_source.if0 | 754,267 | 15.085 | MISS T_svc | 794,840 | 596 | 817,561 | 16.351 | MISS T_svc | 790,356 | 613 | +1.266 | +17 |
| aecp_fanout.set_clock_source.if1 | 739,685 | 14.794 | MISS T_svc | 761,014 | 590 | 700,438 | 14.009 | MISS T_svc | 957,244 | 681 | -0.785 | +91 |
| aecp_fanout.set_control_identify_off.if0 | 619,292 | 12.386 | MISS T_svc | 787,071 | 563 | 774,415 | 15.488 | MISS T_svc | 782,838 | 580 | +3.102 | +17 |
| aecp_fanout.set_control_identify_off.if1 | 748,139 | 14.963 | MISS T_svc | 752,249 | 556 | 655,318 | 13.106 | MISS T_svc | 822,590 | 587 | -1.857 | +31 |
| aecp_fanout.set_control_identify_on.if0 | 730,813 | 14.616 | MISS T_svc | 751,081 | 556 | 798,831 | 15.977 | MISS T_svc | 821,254 | 587 | +1.361 | +31 |
| aecp_fanout.set_control_identify_on.if1 | 771,679 | 15.434 | MISS T_svc | 790,359 | 563 | 765,679 | 15.314 | MISS T_svc | 786,118 | 580 | -0.120 | +17 |
| aecp_fanout.set_name.if0 | 1,034,137 | 20.683 | MISS T_svc | 1,205,519 | 1137 | 1,022,780 | 20.456 | MISS T_svc | 1,231,178 | 1172 | -0.227 | +35 |
| aecp_fanout.set_name.if1 | 1,148,961 | 22.979 | MISS T_svc | 1,186,488 | 1137 | 1,061,527 | 21.231 | MISS T_svc | 1,187,452 | 1139 | -1.748 | +2 |
| aecp_fanout.set_sampling_rate.if0 | 754,072 | 15.081 | MISS T_svc | 744,918 | 589 | 790,531 | 15.811 | MISS T_svc | 746,389 | 592 | +0.730 | +3 |
| aecp_fanout.unlock_entity.if0 | 782,173 | 15.643 | MISS T_svc | 787,713 | 655 | 814,078 | 16.282 | MISS T_svc | 821,810 | 679 | +0.639 | +24 |
| aecp_fanout.unlock_entity.if1 | 786,796 | 15.736 | MISS T_svc | 791,521 | 655 | 696,236 | 13.925 | MISS T_svc | 863,199 | 686 | -1.811 | +31 |

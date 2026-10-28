# aecp-fanout group, arm B, 8x8: S2's final regrade beside this head

reference: 665s2-a681e/receipts/head-regrade/B8/table.md (sha256 2d7d87e812c8114e...)
this run: B8/results/table.md (sha256 1c2c1fa0eb72e6f9...)

reference rows 22, this run 22, common 22
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp_fanout.add_audio_mappings_output.if0 | 754,176 | 15.084 | MISS T_svc | 921,712 | 662 | 717,565 | 14.351 | MISS T_svc | 885,077 | 657 | -0.733 | -5 |
| aecp_fanout.add_audio_mappings_output.if1 | 751,097 | 15.022 | MISS T_svc | 882,937 | 656 | 1,570,597 | 31.412 | MISS ceiling | 956,640 | 670 | +16.390 | +14 |
| aecp_fanout.bind_rx_stream_info.if0 | 1,289,474 | 25.789 | MISS ceiling | 785,722 | 943 | 1,448,819 | 28.976 | MISS ceiling | 784,891 | 943 | +3.187 | +0 |
| aecp_fanout.bind_rx_stream_info.if1 | 1,446,074 | 28.921 | MISS ceiling | 789,373 | 943 | 1,445,070 | 28.901 | MISS ceiling | 788,939 | 943 | -0.020 | +0 |
| aecp_fanout.lock_entity.if0 | 679,780 | 13.596 | MISS T_svc | 826,901 | 662 | 713,000 | 14.260 | MISS T_svc | 823,871 | 679 | +0.664 | +17 |
| aecp_fanout.lock_entity.if1 | 678,888 | 13.578 | MISS T_svc | 826,113 | 662 | 712,526 | 14.251 | MISS T_svc | 823,367 | 679 | +0.673 | +17 |
| aecp_fanout.remove_audio_mappings_output.if0 | 839,940 | 16.799 | MISS T_svc | 884,220 | 655 | 875,281 | 17.506 | MISS T_svc | 884,573 | 657 | +0.707 | +2 |
| aecp_fanout.remove_audio_mappings_output.if1 | 836,630 | 16.733 | MISS T_svc | 881,476 | 655 | 835,540 | 16.711 | MISS T_svc | 881,829 | 657 | -0.022 | +2 |
| aecp_fanout.set_clock_source.if0 | 754,267 | 15.085 | MISS T_svc | 794,840 | 596 | 817,561 | 16.351 | MISS T_svc | 790,356 | 613 | +1.266 | +17 |
| aecp_fanout.set_clock_source.if1 | 739,317 | 14.786 | MISS T_svc | 761,410 | 590 | 771,184 | 15.424 | MISS T_svc | 829,614 | 620 | +0.638 | +30 |
| aecp_fanout.set_configuration.if0 | 989,421 | 19.788 | MISS T_svc | 977,541 | 563 | 1,349,014 | 26.980 | MISS ceiling | 1,426,162 | 643 | +7.192 | +80 |
| aecp_fanout.set_control_identify_off.if0 | 619,292 | 12.386 | MISS T_svc | 787,071 | 563 | 774,415 | 15.488 | MISS T_svc | 782,838 | 580 | +3.102 | +17 |
| aecp_fanout.set_control_identify_off.if1 | 781,899 | 15.638 | MISS T_svc | 753,022 | 557 | 813,499 | 16.270 | MISS T_svc | 785,631 | 581 | +0.632 | +24 |
| aecp_fanout.set_control_identify_on.if0 | 730,813 | 14.616 | MISS T_svc | 751,081 | 556 | 798,831 | 15.977 | MISS T_svc | 821,254 | 587 | +1.361 | +31 |
| aecp_fanout.set_control_identify_on.if1 | 729,079 | 14.582 | MISS T_svc | 753,887 | 556 | 761,788 | 15.236 | MISS T_svc | 786,496 | 580 | +0.654 | +24 |
| aecp_fanout.set_name.if0 | 1,034,137 | 20.683 | MISS T_svc | 1,205,519 | 1137 | 1,022,780 | 20.456 | MISS T_svc | 1,231,178 | 1172 | -0.227 | +35 |
| aecp_fanout.set_name.if1 | 1,135,979 | 22.720 | MISS T_svc | 1,186,836 | 1137 | 1,134,630 | 22.693 | MISS T_svc | 1,187,955 | 1139 | -0.027 | +2 |
| aecp_fanout.set_sampling_rate.if0 | 629,117 | 12.582 | MISS T_svc | 742,693 | 590 | 666,587 | 13.332 | MISS T_svc | 743,769 | 592 | +0.750 | +2 |
| aecp_fanout.set_stream_info.if0 | 1,128,045 | 22.561 | MISS T_svc | 1,170,557 | 1239 | 1,098,169 | 21.963 | MISS T_svc | 1,139,836 | 1244 | -0.598 | +5 |
| aecp_fanout.set_stream_info.if1 | 1,639,151 | 32.783 | MISS ceiling | 1,242,402 | 1251 | 989,248 | 19.785 | MISS T_svc | 1,139,289 | 1244 | -12.998 | -7 |
| aecp_fanout.unlock_entity.if0 | 784,099 | 15.682 | MISS T_svc | 788,491 | 655 | 853,984 | 17.080 | MISS T_svc | 860,421 | 686 | +1.398 | +31 |
| aecp_fanout.unlock_entity.if1 | 782,899 | 15.658 | MISS T_svc | 787,979 | 655 | 852,316 | 17.046 | MISS T_svc | 859,604 | 686 | +1.388 | +31 |

# S2's own first-round arm B 8x8 fan-out beside its final regrade

reference: 665s2-a681c/receipts/runs/B8/table.md (sha256 a515cd80f21b6141...)
this run: <management>/665s2-a681e/receipts/head-regrade/B8/table.md (sha256 2d7d87e812c8114e...)

reference rows 22, this run 22, common 22
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp_fanout.add_audio_mappings_output.if0 | 754,176 | 15.084 | MISS T_svc | 921,712 | 662 | 754,176 | 15.084 | MISS T_svc | 921,712 | 662 | +0.000 | +0 |
| aecp_fanout.add_audio_mappings_output.if1 | 751,097 | 15.022 | MISS T_svc | 882,937 | 656 | 751,097 | 15.022 | MISS T_svc | 882,937 | 656 | +0.000 | +0 |
| aecp_fanout.bind_rx_stream_info.if0 | 1,289,474 | 25.789 | MISS ceiling | 785,722 | 943 | 1,289,474 | 25.789 | MISS ceiling | 785,722 | 943 | +0.000 | +0 |
| aecp_fanout.bind_rx_stream_info.if1 | 1,446,074 | 28.921 | MISS ceiling | 789,373 | 943 | 1,446,074 | 28.921 | MISS ceiling | 789,373 | 943 | +0.000 | +0 |
| aecp_fanout.lock_entity.if0 | 679,780 | 13.596 | MISS T_svc | 826,901 | 662 | 679,780 | 13.596 | MISS T_svc | 826,901 | 662 | +0.000 | +0 |
| aecp_fanout.lock_entity.if1 | 678,888 | 13.578 | MISS T_svc | 826,113 | 662 | 678,888 | 13.578 | MISS T_svc | 826,113 | 662 | +0.000 | +0 |
| aecp_fanout.remove_audio_mappings_output.if0 | 839,940 | 16.799 | MISS T_svc | 884,220 | 655 | 839,940 | 16.799 | MISS T_svc | 884,220 | 655 | +0.000 | +0 |
| aecp_fanout.remove_audio_mappings_output.if1 | 836,630 | 16.733 | MISS T_svc | 881,476 | 655 | 836,630 | 16.733 | MISS T_svc | 881,476 | 655 | +0.000 | +0 |
| aecp_fanout.set_clock_source.if0 | 754,267 | 15.085 | MISS T_svc | 794,840 | 596 | 754,267 | 15.085 | MISS T_svc | 794,840 | 596 | +0.000 | +0 |
| aecp_fanout.set_clock_source.if1 | 739,317 | 14.786 | MISS T_svc | 761,410 | 590 | 739,317 | 14.786 | MISS T_svc | 761,410 | 590 | +0.000 | +0 |
| aecp_fanout.set_configuration.if0 | 989,421 | 19.788 | MISS T_svc | 977,541 | 563 | 989,421 | 19.788 | MISS T_svc | 977,541 | 563 | +0.000 | +0 |
| aecp_fanout.set_control_identify_off.if0 | 619,292 | 12.386 | MISS T_svc | 787,071 | 563 | 619,292 | 12.386 | MISS T_svc | 787,071 | 563 | +0.000 | +0 |
| aecp_fanout.set_control_identify_off.if1 | 781,899 | 15.638 | MISS T_svc | 753,022 | 557 | 781,899 | 15.638 | MISS T_svc | 753,022 | 557 | +0.000 | +0 |
| aecp_fanout.set_control_identify_on.if0 | 730,813 | 14.616 | MISS T_svc | 751,081 | 556 | 730,813 | 14.616 | MISS T_svc | 751,081 | 556 | +0.000 | +0 |
| aecp_fanout.set_control_identify_on.if1 | 729,079 | 14.582 | MISS T_svc | 753,887 | 556 | 729,079 | 14.582 | MISS T_svc | 753,887 | 556 | +0.000 | +0 |
| aecp_fanout.set_name.if0 | 1,034,137 | 20.683 | MISS T_svc | 1,205,519 | 1137 | 1,034,137 | 20.683 | MISS T_svc | 1,205,519 | 1137 | +0.000 | +0 |
| aecp_fanout.set_name.if1 | 1,135,979 | 22.720 | MISS T_svc | 1,186,836 | 1137 | 1,135,979 | 22.720 | MISS T_svc | 1,186,836 | 1137 | +0.000 | +0 |
| aecp_fanout.set_sampling_rate.if0 | 629,117 | 12.582 | MISS T_svc | 742,693 | 590 | 629,117 | 12.582 | MISS T_svc | 742,693 | 590 | +0.000 | +0 |
| aecp_fanout.set_stream_info.if0 | 1,128,045 | 22.561 | MISS T_svc | 1,170,557 | 1239 | 1,128,045 | 22.561 | MISS T_svc | 1,170,557 | 1239 | +0.000 | +0 |
| aecp_fanout.set_stream_info.if1 | 1,639,151 | 32.783 | MISS ceiling | 1,242,402 | 1251 | 1,639,151 | 32.783 | MISS ceiling | 1,242,402 | 1251 | +0.000 | +0 |
| aecp_fanout.unlock_entity.if0 | 784,099 | 15.682 | MISS T_svc | 788,491 | 655 | 784,099 | 15.682 | MISS T_svc | 788,491 | 655 | +0.000 | +0 |
| aecp_fanout.unlock_entity.if1 | 782,899 | 15.658 | MISS T_svc | 787,979 | 655 | 782,899 | 15.658 | MISS T_svc | 787,979 | 655 | +0.000 | +0 |

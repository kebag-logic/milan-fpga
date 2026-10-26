### 8x8

36 of 36 paths and 60 of 60 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 15.084 (22.399) | MISS T_svc | 0 aecp | 1 | 1 |
| add_audio_mappings_output | 1 | `aecp_fanout.add_audio_mappings_output.if1` (aecp-fanout) | 15.022 (22.345) | MISS T_svc | 0 aecp | 1 | 1 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 25.789 (29.123) | MISS ceiling | 0 acmp | 1 | 1 |
| BIND_RX -> GET_STREAM_INFO notice | 1 | `aecp_fanout.bind_rx_stream_info.if1` (aecp-fanout) | 28.921 (34.778) | MISS ceiling | 0 acmp | 1 | 1 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 13.596 (16.538) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 13.578 (16.522) | MISS T_svc | 0 aecp | 1 | 1 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 16.799 (21.648) | MISS T_svc | 0 aecp | 1 | 1 |
| remove_audio_mappings_output | 1 | `aecp_fanout.remove_audio_mappings_output.if1` (aecp-fanout) | 16.733 (23.343) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 15.085 (19.863) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 14.786 (19.935) | MISS T_svc | 0 aecp | 1 | 1 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 19.788 (27.041) | MISS T_svc | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 14.616 (20.463) | MISS T_svc | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 15.638 (19.016) | MISS T_svc | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 20.683 (27.815) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 22.720 (29.510) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 12.582 (19.553) | MISS T_svc | 0 aecp | 1 | 1 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 22.561 (28.808) | MISS T_svc | 0 aecp | 1 | 1 |
| set_stream_info | 1 | `aecp_fanout.set_stream_info.if1` (aecp-fanout) | 32.783 (52.422) | MISS ceiling | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 15.682 (19.742) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 15.658 (21.513) | MISS T_svc | 0 aecp | 1 | 1 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 108.712 (120.299) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 55.792 (76.284) | MISS ceiling | 7 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 44.651 (73.699) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 161.102 (170.624) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind1.if0` (backlog-owed) | at least 860.001 | NEVER ANSWERED | 9 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 27.363 | MISS ceiling | 0 acmp | 3 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 118.960 | MISS ceiling | 11 acmp | 3 | 3 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 27.406 | MISS T_svc | 0 adp | 3 | 3 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 72.708 | MISS T_svc | 7 adp | 1 | 1 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 88.955 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 27.399 | MISS ceiling | 0 aecp | 3 | 3 |
| AECP record released under the composed load, last | 1 | `backlog.service.aecp.last.if1` (backlog) | 224.967 | MISS ceiling | 15 aecp | 3 | 3 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 27.388 | MISS T_svc | 0 maap | 3 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 88.941 | MISS ceiling | 6 maap | 3 | 3 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 143.913 | MISS ceiling | 0 srp | 3 | 3 |
| SRP record released under the composed load, last | 1 | `backlog-owed.service.srp.last.if1` (backlog-owed) | 340.848 | MISS ceiling | 31 srp | 3 | 3 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 608.765 | 59 | 1,392,016 (27.840) | yes | - |
| backlog-adp | 555.844 | 55 | 1,111,647 (22.233) | yes | - |
| backlog-owed | 860.053 | 84 | 1,111,766 (22.235) | yes | - |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 2,232,539 | 44.651 | 10 | 200 | MISS T_svc | 1,392,016 | 364 | 0.877 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 5,435,592 | 108.712 | 10 | 20 | MISS ceiling | 732,610 | 217 | 0.877 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 1,370,279 | 27.406 | 10 | 200 | MISS T_svc | 881,915 | 386 | 0.876 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 4,447,775 | 88.955 | 10 | 200 | MISS T_svc | 827,550 | 291 | 0.877 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 1,368,150 | 27.363 | 10 | 20 | MISS ceiling | 881,915 | 386 | 0.876 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 5,948,006 | 118.960 | 10 | 20 | MISS ceiling | 732,610 | 217 | 0.877 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 1,369,942 | 27.399 | 10 | 24 | MISS ceiling | 881,915 | 386 | 0.876 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 11,248,370 | 224.967 | 10 | 24 | MISS ceiling | 478,451 | 130 | 0.882 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 1,369,422 | 27.388 | 10 | 50 | MISS T_svc | 881,915 | 386 | 0.876 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 4,447,027 | 88.941 | 10 | 50 | MISS ceiling | 827,550 | 291 | 0.877 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 6,562,356 | 131.247 | 10 | 18 | MISS ceiling | 612,892 | 175 | 0.879 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 13,926,804 | 278.536 | 10 | 18 | MISS ceiling | 283,960 | 54 | 0.866 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,789,577 | 55.792 | 10 | 20 | MISS ceiling | 917,291 | 311 | 0.874 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 876,704 | 17.534 | 10 | 200 | MISS T_svc | 856,699 | 386 | 0.875 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 3,635,395 | 72.708 | 10 | 200 | MISS T_svc | 917,291 | 311 | 0.874 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 877,160 | 17.543 | 10 | 20 | MISS T_svc | 856,699 | 386 | 0.875 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 5,065,840 | 101.317 | 10 | 20 | MISS ceiling | 525,124 | 109 | 0.869 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 878,953 | 17.579 | 10 | 24 | MISS T_svc | 856,699 | 386 | 0.875 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 10,540,251 | 210.805 | 10 | 24 | MISS ceiling | 492,056 | 130 | 0.881 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 878,433 | 17.569 | 10 | 50 | MISS T_svc | 856,699 | 386 | 0.875 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 3,637,233 | 72.745 | 10 | 50 | MISS ceiling | 917,291 | 311 | 0.874 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 6,555,396 | 131.108 | 10 | 18 | MISS ceiling | 566,800 | 150 | 0.878 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 16,734,684 | 334.694 | 10 | 18 | MISS ceiling | 290,584 | 36 | 0.864 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 8,055,113 | 161.102 | 10 | 20 | MISS ceiling | 587,791 | 152 | 0.878 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 8,825,989 | 176.520 | 10 | 20 | MISS ceiling | 770,914 | 197 | 0.874 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 43,000,073 | 860.001 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 9,413,605 | 188.272 | 10 | 20 | MISS ceiling | 587,691 | 152 | 0.878 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 42,999,998 | 860.000 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 903,416 | 18.068 | 10 | 200 | MISS T_svc | 875,875 | 344 | 0.875 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 3,618,084 | 72.362 | 10 | 200 | MISS T_svc | 959,228 | 288 | 0.875 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 901,286 | 18.026 | 10 | 20 | MISS T_svc | 875,875 | 344 | 0.875 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 5,269,518 | 105.390 | 10 | 20 | MISS ceiling | 826,771 | 201 | 0.875 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 903,079 | 18.062 | 10 | 24 | MISS T_svc | 875,875 | 344 | 0.875 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 11,205,284 | 224.106 | 10 | 24 | MISS ceiling | 491,827 | 130 | 0.881 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 902,559 | 18.051 | 10 | 50 | MISS T_svc | 875,875 | 344 | 0.875 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 3,617,337 | 72.347 | 10 | 50 | MISS ceiling | 959,228 | 288 | 0.875 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 7,195,626 | 143.913 | 10 | 18 | MISS ceiling | 799,904 | 197 | 0.875 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 17,042,393 | 340.848 | 10 | 18 | MISS ceiling | 241,120 | 30 | 0.861 |
| set_name | `aecp_fanout.set_name.if0` | 1,034,137 | 20.683 | 10 | 24 | MISS T_svc | 1,205,519 | 1137 | 0.883 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 754,267 | 15.085 | 10 | 24 | MISS T_svc | 794,840 | 596 | 0.879 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 730,813 | 14.616 | 10 | 24 | MISS T_svc | 751,081 | 556 | 0.879 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 619,292 | 12.386 | 10 | 24 | MISS T_svc | 787,071 | 563 | 0.880 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 839,940 | 16.799 | 10 | 24 | MISS T_svc | 884,220 | 655 | 0.876 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 754,176 | 15.084 | 10 | 24 | MISS T_svc | 921,712 | 662 | 0.876 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 629,117 | 12.582 | 10 | 24 | MISS T_svc | 742,693 | 590 | 0.879 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 989,421 | 19.788 | 10 | 24 | MISS T_svc | 977,541 | 563 | 0.874 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 1,128,045 | 22.561 | 10 | 24 | MISS T_svc | 1,170,557 | 1239 | 0.887 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 679,780 | 13.596 | 10 | 24 | MISS T_svc | 826,901 | 662 | 0.882 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 784,099 | 15.682 | 10 | 24 | MISS T_svc | 788,491 | 655 | 0.882 |
| set_name | `aecp_fanout.set_name.if1` | 1,135,979 | 22.720 | 10 | 24 | MISS T_svc | 1,186,836 | 1137 | 0.882 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 739,317 | 14.786 | 10 | 24 | MISS T_svc | 761,410 | 590 | 0.879 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 729,079 | 14.582 | 10 | 24 | MISS T_svc | 753,887 | 556 | 0.880 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 781,899 | 15.638 | 10 | 24 | MISS T_svc | 753,022 | 557 | 0.880 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if1` | 836,630 | 16.733 | 10 | 24 | MISS T_svc | 881,476 | 655 | 0.876 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if1` | 751,097 | 15.022 | 10 | 24 | MISS T_svc | 882,937 | 656 | 0.876 |
| set_stream_info | `aecp_fanout.set_stream_info.if1` | 1,639,151 | 32.783 | 10 | 24 | MISS ceiling | 1,242,402 | 1251 | 0.886 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 678,888 | 13.578 | 10 | 24 | MISS T_svc | 826,113 | 662 | 0.882 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 782,899 | 15.658 | 10 | 24 | MISS T_svc | 787,979 | 655 | 0.882 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 1,289,474 | 25.789 | 10 | 24 | MISS ceiling | 785,722 | 943 | 0.885 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if1` | 1,446,074 | 28.921 | 10 | 24 | MISS ceiling | 789,373 | 943 | 0.886 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait tx TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT

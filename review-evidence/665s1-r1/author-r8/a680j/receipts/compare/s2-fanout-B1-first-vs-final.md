# S2's own first-round arm B 1x1 fan-out beside its final regrade (equal: its per-module record is comparable)

reference: 665s2-a681c/receipts/runs/B1/table.md (sha256 143ba5830e0eb462...)
this run: <management>/665s2-a681e/receipts/head-regrade/B1/table.md (sha256 d0be884a0c77dff9...)

reference rows 14, this run 14, common 14
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp_fanout.add_audio_mappings.if0 | 428,446 | 8.569 | fits | 488,907 | 350 | 428,446 | 8.569 | fits | 488,907 | 350 | +0.000 | +0 |
| aecp_fanout.add_audio_mappings_output.if0 | 437,297 | 8.746 | fits | 500,124 | 350 | 437,297 | 8.746 | fits | 500,124 | 350 | +0.000 | +0 |
| aecp_fanout.bind_rx_stream_info.if0 | 740,205 | 14.804 | MISS T_svc | 386,020 | 478 | 740,205 | 14.804 | MISS T_svc | 386,020 | 478 | +0.000 | +0 |
| aecp_fanout.lock_entity.if0 | 411,500 | 8.230 | fits | 469,037 | 350 | 411,500 | 8.230 | fits | 469,037 | 350 | +0.000 | +0 |
| aecp_fanout.remove_audio_mappings.if0 | 428,827 | 8.577 | fits | 489,414 | 350 | 428,827 | 8.577 | fits | 489,414 | 350 | +0.000 | +0 |
| aecp_fanout.remove_audio_mappings_output.if0 | 436,891 | 8.738 | fits | 499,844 | 350 | 436,891 | 8.738 | fits | 499,844 | 350 | +0.000 | +0 |
| aecp_fanout.set_clock_source.if0 | 402,339 | 8.047 | fits | 445,942 | 316 | 402,339 | 8.047 | fits | 445,942 | 316 | +0.000 | +0 |
| aecp_fanout.set_configuration.if0 | 461,671 | 9.233 | fits | 501,232 | 306 | 461,671 | 9.233 | fits | 501,232 | 306 | +0.000 | +0 |
| aecp_fanout.set_control_identify_off.if0 | 389,281 | 7.786 | fits | 446,753 | 299 | 389,281 | 7.786 | fits | 446,753 | 299 | +0.000 | +0 |
| aecp_fanout.set_control_identify_on.if0 | 388,673 | 7.773 | fits | 446,073 | 299 | 388,673 | 7.773 | fits | 446,073 | 299 | +0.000 | +0 |
| aecp_fanout.set_name.if0 | 566,621 | 11.332 | MISS T_svc | 649,006 | 601 | 566,621 | 11.332 | MISS T_svc | 649,006 | 601 | +0.000 | +0 |
| aecp_fanout.set_sampling_rate.if0 | 397,147 | 7.943 | fits | 438,980 | 316 | 397,147 | 7.943 | fits | 438,980 | 316 | +0.000 | +0 |
| aecp_fanout.set_stream_info.if0 | 584,038 | 11.681 | MISS T_svc | 641,310 | 655 | 584,038 | 11.681 | MISS T_svc | 641,310 | 655 | +0.000 | +0 |
| aecp_fanout.unlock_entity.if0 | 410,195 | 8.204 | fits | 467,595 | 350 | 410,195 | 8.204 | fits | 467,595 | 350 | +0.000 | +0 |

# aecp-fanout group, arm B, 1x1: S2's final regrade beside this head

reference: 665s2-a681e/receipts/head-regrade/B1/table.md (sha256 d0be884a0c77dff9...)
this run: B1/results/table.md (sha256 903810e5206c9100...)

reference rows 14, this run 14, common 14
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp_fanout.add_audio_mappings.if0 | 428,446 | 8.569 | fits | 488,907 | 350 | 429,815 | 8.596 | fits | 490,506 | 351 | +0.027 | +1 |
| aecp_fanout.add_audio_mappings_output.if0 | 437,297 | 8.746 | fits | 500,124 | 350 | 438,666 | 8.773 | fits | 501,723 | 351 | +0.027 | +1 |
| aecp_fanout.bind_rx_stream_info.if0 | 740,205 | 14.804 | MISS T_svc | 386,020 | 478 | 741,822 | 14.836 | MISS T_svc | 361,227 | 472 | +0.032 | -6 |
| aecp_fanout.lock_entity.if0 | 411,500 | 8.230 | fits | 469,037 | 350 | 448,079 | 8.962 | fits | 505,874 | 369 | +0.732 | +19 |
| aecp_fanout.remove_audio_mappings.if0 | 428,827 | 8.577 | fits | 489,414 | 350 | 430,196 | 8.604 | fits | 491,013 | 351 | +0.027 | +1 |
| aecp_fanout.remove_audio_mappings_output.if0 | 436,891 | 8.738 | fits | 499,844 | 350 | 438,260 | 8.765 | fits | 501,443 | 351 | +0.027 | +1 |
| aecp_fanout.set_clock_source.if0 | 402,339 | 8.047 | fits | 445,942 | 316 | 438,537 | 8.771 | fits | 482,370 | 335 | +0.724 | +19 |
| aecp_fanout.set_configuration.if0 | 461,671 | 9.233 | fits | 501,232 | 306 | 582,989 | 11.660 | MISS T_svc | 622,780 | 325 | +2.427 | +19 |
| aecp_fanout.set_control_identify_off.if0 | 389,281 | 7.786 | fits | 446,753 | 299 | 398,391 | 7.968 | fits | 456,093 | 311 | +0.182 | +12 |
| aecp_fanout.set_control_identify_on.if0 | 388,673 | 7.773 | fits | 446,073 | 299 | 397,783 | 7.956 | fits | 455,413 | 311 | +0.183 | +12 |
| aecp_fanout.set_name.if0 | 566,621 | 11.332 | MISS T_svc | 649,006 | 601 | 574,631 | 11.493 | MISS T_svc | 664,036 | 622 | +0.161 | +21 |
| aecp_fanout.set_sampling_rate.if0 | 397,147 | 7.943 | fits | 438,980 | 316 | 399,246 | 7.985 | fits | 441,309 | 317 | +0.042 | +1 |
| aecp_fanout.set_stream_info.if0 | 584,038 | 11.681 | MISS T_svc | 641,310 | 655 | 616,177 | 12.324 | MISS T_svc | 673,679 | 672 | +0.643 | +17 |
| aecp_fanout.unlock_entity.if0 | 410,195 | 8.204 | fits | 467,595 | 350 | 420,793 | 8.416 | fits | 478,423 | 362 | +0.212 | +12 |

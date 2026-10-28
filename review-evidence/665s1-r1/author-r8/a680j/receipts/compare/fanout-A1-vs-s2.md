# aecp-fanout group, arm A, 1x1: S2's final regrade beside this head

reference: 665s2-a681e/receipts/head-regrade/A1/table.md (sha256 a835c98b8bb61393...)
this run: AF1/results/table.md (sha256 69cdd5accd6c5d06...)

reference rows 9, this run 9, common 9
| Probe | ref cycles | ref ms | ref verdict | ref pass cycles | ref accesses | cycles | ms | verdict | pass cycles | accesses | d ms | d accesses |
|---|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| aecp_fanout.add_audio_mappings.if0 | 428,446 | 8.569 | fits | 488,907 | 350 | 429,815 | 8.596 | fits | 490,506 | 351 | +0.027 | +1 |
| aecp_fanout.lock_entity.if0 | 410,172 | 8.203 | fits | 467,583 | 350 | 420,777 | 8.416 | fits | 478,446 | 362 | +0.213 | +12 |
| aecp_fanout.remove_audio_mappings.if0 | 428,827 | 8.577 | fits | 489,414 | 350 | 430,196 | 8.604 | fits | 491,013 | 351 | +0.027 | +1 |
| aecp_fanout.set_clock_source.if0 | 402,339 | 8.047 | fits | 445,942 | 316 | 438,537 | 8.771 | fits | 482,370 | 335 | +0.724 | +19 |
| aecp_fanout.set_control_identify_off.if0 | 389,281 | 7.786 | fits | 446,753 | 299 | 398,391 | 7.968 | fits | 456,093 | 311 | +0.182 | +12 |
| aecp_fanout.set_control_identify_on.if0 | 388,673 | 7.773 | fits | 446,073 | 299 | 397,783 | 7.956 | fits | 455,413 | 311 | +0.183 | +12 |
| aecp_fanout.set_name.if0 | 566,621 | 11.332 | MISS T_svc | 649,005 | 601 | 574,631 | 11.493 | MISS T_svc | 664,036 | 622 | +0.161 | +21 |
| aecp_fanout.set_sampling_rate.if0 | 398,460 | 7.969 | fits | 440,347 | 317 | 400,164 | 8.003 | fits | 442,281 | 317 | +0.034 | +0 |
| aecp_fanout.unlock_entity.if0 | 410,731 | 8.215 | fits | 468,203 | 350 | 421,329 | 8.427 | fits | 479,031 | 362 | +0.212 | +12 |

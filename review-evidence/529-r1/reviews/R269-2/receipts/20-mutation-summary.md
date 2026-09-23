| mutant | leg | class | verdict | tally | FAIL lines | CRF-tagged FAIL | event-arm quadlets red | own quadlets | first CRF-tagged (else first) FAIL |
|---|---|---|---|---|---|---|---|---|---|
| base | notify | base | SURVIVED | checks: 145   failures: 0 | 0 | 0 | - |  |  |
| base | nxn4c | base | SURVIVED | checks: 1705   failures: 0 | 0 | 0 | - |  |  |
| base | nxn8 | base | SURVIVED | checks: 3133   failures: 0 | 0 | 0 | - |  |  |
| base | nxndv | base | SURVIVED | checks: 1707   failures: 0 | 0 | 0 | - |  |  |
| vd-avb-pick | notify | arbiter | KILLED | checks: 145   failures: 2 | 2 | 0 | - |  | [FAIL] [NOTIFY] ...A's entry starts its own sequence at 0 got=0x1 exp=0x0 |
| vd-avb-pick | nxn | arbiter | KILLED | checks: 1705   failures: 1 | 1 | 0 | - |  | [FAIL] [CTRS2] retired clock controls do not reach the arbiter got=0x1 exp=0x0 |
| vd-clear-stuck | notify | arbiter | KILLED | checks: 145   failures: 2 | 2 | 2 | - |  | [FAIL] [NOTIFY-CRF] ...and no further push to B in the next two seconds without a change got=0x4 exp=0x2 |
| vd-clear-stuck | nxn | arbiter | SURVIVED | checks: 1705   failures: 0 | 0 | 0 | - |  |  |
| vd-nodirty | notify | arbiter | KILLED | checks: 145   failures: 10 | 10 | 10 | - |  | [FAIL] [NOTIFY-CRF] the CRF bind edge pushed GET_COUNTERS(STREAM_INPUT, N) to A got=0x0 exp=0x1 |
| vd-nodirty | nxn | arbiter | KILLED | checks: 1705   failures: 1 | 1 | 1 | - |  | [FAIL] [CTRS-CRF] the bind edge reached the arbiter as STREAM_INPUT N only got=0x0 exp=0x10 |
| vd-rr-sout | notify | arbiter | SURVIVED | checks: 145   failures: 0 | 0 | 0 | - |  |  |
| vd-rr-sout | nxn | arbiter | SURVIVED | checks: 1705   failures: 0 | 0 | 0 | - |  |  |
| vd-sout-off | notify | arbiter | SURVIVED | checks: 145   failures: 0 | 0 | 0 | - |  |  |
| vd-sout-off | nxn | arbiter | KILLED | checks: 1705   failures: 1 | 1 | 0 | - |  | [FAIL] [CTRS-OUT] simultaneous output changes ALL reached the arbiter got=0xa exp=0x1f |
| vd-to-idx0 | notify | arbiter | KILLED | checks: 145   failures: 10 | 10 | 10 | - |  | [FAIL] [NOTIFY-CRF] the CRF bind edge pushed GET_COUNTERS(STREAM_INPUT, N) to A got=0x0 exp=0x1 |
| vd-to-idx0 | nxn | arbiter | KILLED | checks: 1705   failures: 1 | 1 | 1 | - |  | [FAIL] [CTRS-CRF] the bind edge reached the arbiter as STREAM_INPUT N only got=0x1 exp=0x10 |
| ve-also-ckd | notify | extra-tuple | SURVIVED | checks: 145   failures: 0 | 0 | 0 | - |  |  |
| ve-also-ckd | nxn | extra-tuple | SURVIVED | checks: 1705   failures: 0 | 0 | 0 | - |  |  |
| ve-also-ckd | nxn8 | extra-tuple | SURVIVED | checks: 3133   failures: 0 | 0 | 0 | - |  |  |
| ve-also-sout | notify | extra-tuple | SURVIVED | checks: 145   failures: 0 | 0 | 0 | - |  |  |
| ve-also-sout | nxn | extra-tuple | SURVIVED | checks: 1705   failures: 0 | 0 | 0 | - |  |  |
| ve-also-sout | nxn8 | extra-tuple | SURVIVED | checks: 3133   failures: 0 | 0 | 0 | - |  |  |
| vg-crf-first-noidx | nxn | guard | KILLED | checks: 1705   failures: 8 | 8 | 1 | - |  | [FAIL] [CTRS-CRF] every AAF input keeps 0xFFF and none carries a CRF quadlet got=0x0 exp=0x1 |
| vg-ctl-marked | nxn | control | SURVIVED | checks: 1705   failures: 0 | 0 | 0 | - |  |  |
| vg-dup-q1 | nxn | row | KILLED | checks: 1705   failures: 3 | 3 | 3 | @4 |  | [FAIL] [CTRS-CRF] signatures: @4 MEDIA_UNLOCKED       got=0xa5010101 exp=0xa5020202 |
| vg-idx-plus1 | nxn | guard | KILLED | checks: 1705   failures: 32 | 32 | 32 | @0,@4,@8,@12,@16,@20,@32,@36,@40,@44 |  | [FAIL] [CTRS-CRF] counters_valid = 0xF3F (the Table 5.16 ten) got=0x0 exp=0xf3f |
| vg-lvl-q0 | nxn | row | KILLED | checks: 1705   failures: 3 | 3 | 3 | @0 |  | [FAIL] [CTRS-CRF] signatures: @0 MEDIA_LOCKED         got=0x0 exp=0xa5010101 |
| vg-mask-3f | nxn | row | KILLED | checks: 1705   failures: 4 | 4 | 4 | - |  | [FAIL] [CTRS-CRF] counters_valid = 0xF3F (the Table 5.16 ten) got=0x3f exp=0xf3f |
| vg-mask-fff | nxn | row | KILLED | checks: 1705   failures: 4 | 4 | 4 | - |  | [FAIL] [CTRS-CRF] counters_valid = 0xF3F (the Table 5.16 ten) got=0xfff exp=0xf3f |
| vg-no-type | nxn | guard | KILLED | checks: 1705   failures: 6 | 6 | 0 | - |  | [FAIL] [CTRS-OUT] every AAF and CRF output returns mask 0x1F got=0x0 exp=0x1 |
| vg-q2-zero | nxn | row | KILLED | checks: 1705   failures: 4 | 4 | 4 | @8 |  | [FAIL] [CTRS-CRF] signatures: @8 STREAM_INTERRUPTED   got=0x0 exp=0xa5030303 |
| vg-q9-q10 | nxn | row | KILLED | checks: 1705   failures: 4 | 4 | 4 | @36,@40 |  | [FAIL] [CTRS-CRF] signatures: @36 LATE_TIMESTAMP      got=0xa50b0b0b exp=0xa50a0a0a |
| vg-row-removed | nxn | row | KILLED | checks: 1705   failures: 32 | 32 | 32 | @0,@4,@8,@12,@16,@20,@32,@36,@40,@44 |  | [FAIL] [CTRS-CRF] counters_valid = 0xF3F (the Table 5.16 ten) got=0x0 exp=0xf3f |
| vg-sin-le | nxn | guard | KILLED | checks: 1705   failures: 32 | 32 | 32 | @0,@4,@8,@12,@16,@20,@32,@36,@40,@44 |  | [FAIL] [CTRS-CRF] counters_valid = 0xF3F (the Table 5.16 ten) got=0xfff exp=0xf3f |
| vg-slice-q2 | nxn | row | KILLED | checks: 1705   failures: 3 | 3 | 3 | - |  | [FAIL] [CTRS-CRF] signatures: @8 STREAM_INTERRUPTED   got=0x303 exp=0xa5030303 |
| vr10 | nxn | rotation | KILLED | checks: 1705   failures: 20 | 20 | 17 | @0,@4,@8,@12,@16,@20,@32,@36,@40,@44 | own quadlets [0, 4, 8, 12, 16, 20, 32, 36, 40, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vr3-mr-tu-late | nxn | rotation | KILLED | checks: 1705   failures: 3 | 3 | 3 | @16,@20,@36 | own quadlets [16, 20, 36] red: yes | [FAIL] [CTRS-CRF] events, all ten: @16 MEDIA_RESET    got=0x8 exp=0x5 |
| vx-cnt_locked-cnt_intr | nxn | exchange | KILLED | checks: 1705   failures: 5 | 5 | 5 | @0,@8 | own quadlets [0, 8] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-cnt_locked-cnt_intr | nxn8 | exchange | KILLED | checks: 3133   failures: 5 | 5 | 5 | @0,@8 | own quadlets [0, 8] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-cnt_locked-cnt_unlocked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @0,@4 | own quadlets [0, 4] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x0 exp=0x1 |
| vx-cnt_locked-cnt_unlocked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @0,@4 | own quadlets [0, 4] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x0 exp=0x1 |
| vx-cnt_unlocked-cnt_intr | nxn | exchange | KILLED | checks: 1705   failures: 5 | 5 | 5 | @4,@8 | own quadlets [4, 8] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-cnt_unlocked-cnt_intr | nxn8 | exchange | KILLED | checks: 3133   failures: 5 | 5 | 5 | @4,@8 | own quadlets [4, 8] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-early_cnt-cnt_intr | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @8,@40 | own quadlets [8, 40] red: yes | [FAIL] [CTRS-CRF] wrap: ...and STREAM_INTERRUPTED did not move got=0x0 exp=0xffffffff |
| vx-early_cnt-cnt_intr | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @8,@40 | own quadlets [8, 40] red: yes | [FAIL] [CTRS-CRF] wrap: ...and STREAM_INTERRUPTED did not move got=0x0 exp=0xffffffff |
| vx-early_cnt-cnt_locked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @0,@40 | own quadlets [0, 40] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x5 exp=0x1 |
| vx-early_cnt-cnt_locked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @0,@40 | own quadlets [0, 40] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x5 exp=0x1 |
| vx-early_cnt-cnt_unlocked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @4,@40 | own quadlets [4, 40] red: yes | [FAIL] [CTRS-CRF] events: ...and MEDIA_UNLOCKED 0 @4 (Table 5.6 locked form) got=0x5 exp=0x0 |
| vx-early_cnt-cnt_unlocked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @4,@40 | own quadlets [4, 40] red: yes | [FAIL] [CTRS-CRF] events: ...and MEDIA_UNLOCKED 0 @4 (Table 5.6 locked form) got=0x5 exp=0x0 |
| vx-fmt_err-cnt_intr | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 3 | @8,@32 | own quadlets [8, 32] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-fmt_err-cnt_intr | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 3 | @8,@32 | own quadlets [8, 32] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-fmt_err-cnt_locked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @0,@32 | own quadlets [0, 32] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x7 exp=0x1 |
| vx-fmt_err-cnt_locked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @0,@32 | own quadlets [0, 32] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x7 exp=0x1 |
| vx-fmt_err-cnt_unlocked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @4,@32 | own quadlets [4, 32] red: yes | [FAIL] [CTRS-CRF] events: ...and MEDIA_UNLOCKED 0 @4 (Table 5.6 locked form) got=0x7 exp=0x0 |
| vx-fmt_err-cnt_unlocked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @4,@32 | own quadlets [4, 32] red: yes | [FAIL] [CTRS-CRF] events: ...and MEDIA_UNLOCKED 0 @4 (Table 5.6 locked form) got=0x7 exp=0x0 |
| vx-fmt_err-early_cnt | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 2 | @32,@40 | own quadlets [32, 40] red: yes | [FAIL] [CTRS-CRF] events, all ten: @32 UNSUPPORTED_FORMAT got=0x9 exp=0x7 |
| vx-fmt_err-early_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 2 | @32,@40 | own quadlets [32, 40] red: yes | [FAIL] [CTRS-CRF] events, all ten: @32 UNSUPPORTED_FORMAT got=0x9 exp=0x7 |
| vx-fmt_err-late_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @32,@36 | own quadlets [32, 36] red: yes | [FAIL] [CTRS-CRF] events, all ten: @32 UNSUPPORTED_FORMAT got=0x8 exp=0x7 |
| vx-fmt_err-late_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @32,@36 | own quadlets [32, 36] red: yes | [FAIL] [CTRS-CRF] events, all ten: @32 UNSUPPORTED_FORMAT got=0x8 exp=0x7 |
| vx-fmt_err-mr_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @16,@32 | own quadlets [16, 32] red: yes | [FAIL] [CTRS-CRF] events, all ten: @16 MEDIA_RESET    got=0x7 exp=0x5 |
| vx-fmt_err-mr_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @16,@32 | own quadlets [16, 32] red: yes | [FAIL] [CTRS-CRF] events, all ten: @16 MEDIA_RESET    got=0x7 exp=0x5 |
| vx-fmt_err-seq_err | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 3 | @12,@32 | own quadlets [12, 32] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-fmt_err-seq_err | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 3 | @12,@32 | own quadlets [12, 32] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-fmt_err-tu_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @20,@32 | own quadlets [20, 32] red: yes | [FAIL] [CTRS-CRF] events, all ten: @20 TIMESTAMP_UNCERTAIN got=0x7 exp=0x6 |
| vx-fmt_err-tu_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @20,@32 | own quadlets [20, 32] red: yes | [FAIL] [CTRS-CRF] events, all ten: @20 TIMESTAMP_UNCERTAIN got=0x7 exp=0x6 |
| vx-late_cnt-cnt_intr | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 3 | @8,@36 | own quadlets [8, 36] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-late_cnt-cnt_intr | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 3 | @8,@36 | own quadlets [8, 36] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-late_cnt-cnt_locked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @0,@36 | own quadlets [0, 36] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x8 exp=0x1 |
| vx-late_cnt-cnt_locked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @0,@36 | own quadlets [0, 36] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x8 exp=0x1 |
| vx-late_cnt-cnt_unlocked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @4,@36 | own quadlets [4, 36] red: yes | [FAIL] [CTRS-CRF] events: ...and MEDIA_UNLOCKED 0 @4 (Table 5.6 locked form) got=0x8 exp=0x0 |
| vx-late_cnt-cnt_unlocked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @4,@36 | own quadlets [4, 36] red: yes | [FAIL] [CTRS-CRF] events: ...and MEDIA_UNLOCKED 0 @4 (Table 5.6 locked form) got=0x8 exp=0x0 |
| vx-late_cnt-early_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @36,@40 | own quadlets [36, 40] red: yes | [FAIL] [CTRS-CRF] events, all ten: @36 LATE_TIMESTAMP got=0x9 exp=0x8 |
| vx-late_cnt-early_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @36,@40 | own quadlets [36, 40] red: yes | [FAIL] [CTRS-CRF] events, all ten: @36 LATE_TIMESTAMP got=0x9 exp=0x8 |
| vx-mr_cnt-cnt_intr | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 3 | @8,@16 | own quadlets [8, 16] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-mr_cnt-cnt_intr | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 3 | @8,@16 | own quadlets [8, 16] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-mr_cnt-cnt_locked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @0,@16 | own quadlets [0, 16] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x5 exp=0x1 |
| vx-mr_cnt-cnt_locked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @0,@16 | own quadlets [0, 16] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x5 exp=0x1 |
| vx-mr_cnt-cnt_unlocked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @4,@16 | own quadlets [4, 16] red: yes | [FAIL] [CTRS-CRF] events: ...and MEDIA_UNLOCKED 0 @4 (Table 5.6 locked form) got=0x5 exp=0x0 |
| vx-mr_cnt-cnt_unlocked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @4,@16 | own quadlets [4, 16] red: yes | [FAIL] [CTRS-CRF] events: ...and MEDIA_UNLOCKED 0 @4 (Table 5.6 locked form) got=0x5 exp=0x0 |
| vx-mr_cnt-early_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @16,@40 | own quadlets [16, 40] red: yes | [FAIL] [CTRS-CRF] events, all ten: @16 MEDIA_RESET    got=0x9 exp=0x5 |
| vx-mr_cnt-early_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @16,@40 | own quadlets [16, 40] red: yes | [FAIL] [CTRS-CRF] events, all ten: @16 MEDIA_RESET    got=0x9 exp=0x5 |
| vx-mr_cnt-late_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @16,@36 | own quadlets [16, 36] red: yes | [FAIL] [CTRS-CRF] events, all ten: @16 MEDIA_RESET    got=0x8 exp=0x5 |
| vx-mr_cnt-late_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @16,@36 | own quadlets [16, 36] red: yes | [FAIL] [CTRS-CRF] events, all ten: @16 MEDIA_RESET    got=0x8 exp=0x5 |
| vx-mr_cnt-tu_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @16,@20 | own quadlets [16, 20] red: yes | [FAIL] [CTRS-CRF] events, all ten: @16 MEDIA_RESET    got=0x6 exp=0x5 |
| vx-mr_cnt-tu_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @16,@20 | own quadlets [16, 20] red: yes | [FAIL] [CTRS-CRF] events, all ten: @16 MEDIA_RESET    got=0x6 exp=0x5 |
| vx-pdu_count-cnt_intr | nxn | exchange | KILLED | checks: 1705   failures: 8 | 8 | 6 | @8,@44 | own quadlets [8, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-cnt_intr | nxn8 | exchange | KILLED | checks: 3133   failures: 8 | 8 | 6 | @8,@44 | own quadlets [8, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-cnt_locked | nxn | exchange | KILLED | checks: 1705   failures: 8 | 8 | 6 | @0,@44 | own quadlets [0, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-cnt_locked | nxn8 | exchange | KILLED | checks: 3133   failures: 8 | 8 | 6 | @0,@44 | own quadlets [0, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-cnt_unlocked | nxn | exchange | KILLED | checks: 1705   failures: 8 | 8 | 6 | @4,@44 | own quadlets [4, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-cnt_unlocked | nxn8 | exchange | KILLED | checks: 3133   failures: 8 | 8 | 6 | @4,@44 | own quadlets [4, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-early_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @40,@44 | own quadlets [40, 44] red: yes | [FAIL] [CTRS-CRF] events, all ten: @40 EARLY_TIMESTAMP got=0x15 exp=0x9 |
| vx-pdu_count-early_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @40,@44 | own quadlets [40, 44] red: yes | [FAIL] [CTRS-CRF] events, all ten: @40 EARLY_TIMESTAMP got=0x15 exp=0x9 |
| vx-pdu_count-fmt_err | nxn | exchange | KILLED | checks: 1705   failures: 7 | 7 | 4 | @32,@44 | own quadlets [32, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-fmt_err | nxn8 | exchange | KILLED | checks: 3133   failures: 7 | 7 | 4 | @32,@44 | own quadlets [32, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-late_cnt | nxn | exchange | KILLED | checks: 1705   failures: 6 | 6 | 4 | @36,@44 | own quadlets [36, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-late_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 6 | 6 | 4 | @36,@44 | own quadlets [36, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-mr_cnt | nxn | exchange | KILLED | checks: 1705   failures: 6 | 6 | 4 | @16,@44 | own quadlets [16, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-mr_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 6 | 6 | 4 | @16,@44 | own quadlets [16, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-seq_err | nxn | exchange | KILLED | checks: 1705   failures: 8 | 8 | 5 | @12,@44 | own quadlets [12, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-seq_err | nxn8 | exchange | KILLED | checks: 3133   failures: 8 | 8 | 5 | @12,@44 | own quadlets [12, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-tu_cnt | nxn | exchange | KILLED | checks: 1705   failures: 6 | 6 | 4 | @20,@44 | own quadlets [20, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-pdu_count-tu_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 6 | 6 | 4 | @20,@44 | own quadlets [20, 44] red: yes | [FAIL] [CTRS-CRF] wrap: one accepted PDU's interval takes FRAMES_RX to 0 got=0xffffffff exp=0x0 |
| vx-seq_err-cnt_intr | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @8,@12 | own quadlets [8, 12] red: yes | [FAIL] [CTRS-CRF] events, all ten: @8 STREAM_INTERRUPTED got=0x4 exp=0x3 |
| vx-seq_err-cnt_intr | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @8,@12 | own quadlets [8, 12] red: yes | [FAIL] [CTRS-CRF] events, all ten: @8 STREAM_INTERRUPTED got=0x4 exp=0x3 |
| vx-seq_err-cnt_locked | nxn | exchange | KILLED | checks: 1705   failures: 5 | 5 | 5 | @0,@12 | own quadlets [0, 12] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-seq_err-cnt_locked | nxn8 | exchange | KILLED | checks: 3133   failures: 5 | 5 | 5 | @0,@12 | own quadlets [0, 12] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-seq_err-cnt_unlocked | nxn | exchange | KILLED | checks: 1705   failures: 5 | 5 | 5 | @4,@12 | own quadlets [4, 12] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-seq_err-cnt_unlocked | nxn8 | exchange | KILLED | checks: 3133   failures: 5 | 5 | 5 | @4,@12 | own quadlets [4, 12] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-seq_err-early_cnt | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 3 | @12,@40 | own quadlets [12, 40] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x2 exp=0x1 |
| vx-seq_err-early_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 3 | @12,@40 | own quadlets [12, 40] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x2 exp=0x1 |
| vx-seq_err-late_cnt | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 3 | @12,@36 | own quadlets [12, 36] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-seq_err-late_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 3 | @12,@36 | own quadlets [12, 36] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-seq_err-mr_cnt | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 3 | @12,@16 | own quadlets [12, 16] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-seq_err-mr_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 3 | @12,@16 | own quadlets [12, 16] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-seq_err-tu_cnt | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 3 | @12,@20 | own quadlets [12, 20] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-seq_err-tu_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 3 | @12,@20 | own quadlets [12, 20] red: yes | [FAIL] [CTRS-CRF] wrap: ...SEQ_NUM_MISMATCH counts its interval once got=0x0 exp=0x1 |
| vx-tu_cnt-cnt_intr | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 3 | @8,@20 | own quadlets [8, 20] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-tu_cnt-cnt_intr | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 3 | @8,@20 | own quadlets [8, 20] red: yes | [FAIL] [CTRS-CRF] wrap: a two-PDU gap takes STREAM_INTERRUPTED to 0 got=0xffffffff exp=0x0 |
| vx-tu_cnt-cnt_locked | nxn | exchange | KILLED | checks: 1705   failures: 4 | 4 | 4 | @0,@20 | own quadlets [0, 20] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x0 exp=0x1 |
| vx-tu_cnt-cnt_locked | nxn8 | exchange | KILLED | checks: 3133   failures: 4 | 4 | 4 | @0,@20 | own quadlets [0, 20] red: yes | [FAIL] [CTRS-CRF] events: the first lock reads MEDIA_LOCKED 1 @0 got=0x0 exp=0x1 |
| vx-tu_cnt-cnt_unlocked | nxn | exchange | KILLED | checks: 1705   failures: 3 | 3 | 3 | @4,@20 | own quadlets [4, 20] red: yes | [FAIL] [CTRS-CRF] events: the 100 ms silence reads MEDIA_UNLOCKED 1 @4 got=0x0 exp=0x1 |
| vx-tu_cnt-cnt_unlocked | nxn8 | exchange | KILLED | checks: 3133   failures: 3 | 3 | 3 | @4,@20 | own quadlets [4, 20] red: yes | [FAIL] [CTRS-CRF] events: the 100 ms silence reads MEDIA_UNLOCKED 1 @4 got=0x0 exp=0x1 |
| vx-tu_cnt-early_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @20,@40 | own quadlets [20, 40] red: yes | [FAIL] [CTRS-CRF] events, all ten: @20 TIMESTAMP_UNCERTAIN got=0x9 exp=0x6 |
| vx-tu_cnt-early_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @20,@40 | own quadlets [20, 40] red: yes | [FAIL] [CTRS-CRF] events, all ten: @20 TIMESTAMP_UNCERTAIN got=0x9 exp=0x6 |
| vx-tu_cnt-late_cnt | nxn | exchange | KILLED | checks: 1705   failures: 2 | 2 | 2 | @20,@36 | own quadlets [20, 36] red: yes | [FAIL] [CTRS-CRF] events, all ten: @20 TIMESTAMP_UNCERTAIN got=0x8 exp=0x6 |
| vx-tu_cnt-late_cnt | nxn8 | exchange | KILLED | checks: 3133   failures: 2 | 2 | 2 | @20,@36 | own quadlets [20, 36] red: yes | [FAIL] [CTRS-CRF] events, all ten: @20 TIMESTAMP_UNCERTAIN got=0x8 exp=0x6 |

exchange/rotation logs missing an own-quadlet red: 0 []

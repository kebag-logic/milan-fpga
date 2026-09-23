# [A216] #529 mutant receipts

| tag | leg | harness | datapath | build | checks | failures | CRF-tag red | other red | pair's own quadlets red | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| base_nxn_pw_early_intr | nxn | 3f948b1b | e8add015 | 0 | 1687 | 2 | 2 | 0 |  | RED |
| base_nxn_pw_early_lock | nxn | 3f948b1b | 20e71520 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_early_unlock | nxn | 3f948b1b | 30ed16d2 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_fmt_early | nxn | 3f948b1b | b7082861 | 0 | 1687 | 1 | 0 | 1 |  | RED |
| base_nxn_pw_fmt_intr | nxn | 3f948b1b | 78b1b0b6 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_fmt_late | nxn | 3f948b1b | 895f9735 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_fmt_lock | nxn | 3f948b1b | aac9dfc1 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_fmt_mr | nxn | 3f948b1b | 48801155 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_fmt_seq | nxn | 3f948b1b | 1593f85d | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_fmt_tu | nxn | 3f948b1b | 7ed71789 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_fmt_unlock | nxn | 3f948b1b | 710f069e | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_late_early | nxn | 3f948b1b | d1256fdc | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_late_intr | nxn | 3f948b1b | b874d7b2 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_late_lock | nxn | 3f948b1b | 9fe35135 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_late_unlock | nxn | 3f948b1b | 398185e3 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_lock_intr | nxn | 3f948b1b | 502a4a50 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_lock_unlock | nxn | 3f948b1b | c7cba1b5 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_mr_early | nxn | 3f948b1b | 9cd7d5fd | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_mr_intr | nxn | 3f948b1b | e1af3612 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_mr_late | nxn | 3f948b1b | a9d1b6e4 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_mr_lock | nxn | 3f948b1b | 0b749fdc | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_mr_tu | nxn | 3f948b1b | 453bee83 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_mr_unlock | nxn | 3f948b1b | f5d0a573 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_pdu_early | nxn | 3f948b1b | 0df67db0 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_pdu_fmt | nxn | 3f948b1b | 26c992c1 | 0 | 1687 | 5 | 2 | 3 |  | RED |
| base_nxn_pw_pdu_intr | nxn | 3f948b1b | 5e6e7fff | 0 | 1687 | 6 | 4 | 2 |  | RED |
| base_nxn_pw_pdu_late | nxn | 3f948b1b | ec2ed862 | 0 | 1687 | 4 | 2 | 2 |  | RED |
| base_nxn_pw_pdu_lock | nxn | 3f948b1b | 1f16e27e | 0 | 1687 | 4 | 2 | 2 |  | RED |
| base_nxn_pw_pdu_mr | nxn | 3f948b1b | ef39441a | 0 | 1687 | 4 | 2 | 2 |  | RED |
| base_nxn_pw_pdu_seq | nxn | 3f948b1b | c0359436 | 0 | 1687 | 6 | 3 | 3 |  | RED |
| base_nxn_pw_pdu_tu | nxn | 3f948b1b | e075990f | 0 | 1687 | 4 | 2 | 2 |  | RED |
| base_nxn_pw_pdu_unlock | nxn | 3f948b1b | cf348925 | 0 | 1687 | 4 | 2 | 2 |  | RED |
| base_nxn_pw_seq_early | nxn | 3f948b1b | 65b05319 | 0 | 1687 | 2 | 1 | 1 |  | RED |
| base_nxn_pw_seq_intr | nxn | 3f948b1b | 4ea7d438 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_seq_late | nxn | 3f948b1b | 2e969957 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_seq_lock | nxn | 3f948b1b | aca8a43f | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_seq_mr | nxn | 3f948b1b | 8fdb00a1 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_seq_tu | nxn | 3f948b1b | 32016867 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_seq_unlock | nxn | 3f948b1b | 671c6fa8 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_tu_early | nxn | 3f948b1b | 979ab55d | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_tu_intr | nxn | 3f948b1b | 2f97bb36 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| base_nxn_pw_tu_late | nxn | 3f948b1b | 34aa5354 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_tu_lock | nxn | 3f948b1b | 2c4d8975 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_tu_unlock | nxn | 3f948b1b | b49ab4c0 | 0 | 1687 | 0 | 0 | 0 |  | green |
| base_nxn_pw_unlock_intr | nxn | 3f948b1b | fa89ccd8 | 0 | 1687 | 1 | 1 | 0 |  | RED |
| notify_r268_a5_dirty_removed | notify | fe0e4c37 | 2d076efe | 0 | 145 | 10 | 10 | 0 |  | RED |
| notify_r268_ctl_marked | notify | fe0e4c37 | 285fcc52 | 0 | 145 | 0 | 0 | 0 |  | green |
| notify_r268_r3_crf_pend_stuck | notify | fe0e4c37 | 6e876a42 | 0 | 145 | 2 | 2 | 0 |  | RED |
| nxn4c_r268_p1_bind_lock_unlock | nxn4c | fe0e4c37 | c258524d | 0 | 1705 | 4 | 4 | 0 |  | RED |
| nxn4c_r268_p2_bind_late_early | nxn4c | fe0e4c37 | 1b5419b3 | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn4c_r268_p3_bind_mr_tu | nxn4c | fe0e4c37 | efefbfaf | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn4c_r268_p4_bind_intr_lock | nxn4c | fe0e4c37 | 4839430b | 0 | 1705 | 5 | 5 | 0 |  | RED |
| nxn4c_r268_p5_bind_fmt_late | nxn4c | fe0e4c37 | 0612257a | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn4c_r269_mx1_port_swap_mr_tu | nxn4c | fe0e4c37 | 453bee83 | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn4c_r269_mx2_port_swap_locked_unlocked | nxn4c | fe0e4c37 | c7cba1b5 | 0 | 1705 | 4 | 4 | 0 |  | RED |
| nxn4c_r269_mx3_port_swap_late_early | nxn4c | fe0e4c37 | d1256fdc | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn4c_r269_mx4_port_swap_intr_locked | nxn4c | fe0e4c37 | 502a4a50 | 0 | 1705 | 5 | 5 | 0 |  | RED |
| nxn8_pw_early_intr | nxn8 | fe0e4c37 | e8add015 | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_early_lock | nxn8 | fe0e4c37 | 20e71520 | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_early_unlock | nxn8 | fe0e4c37 | 30ed16d2 | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_fmt_early | nxn8 | fe0e4c37 | b7082861 | 0 | 3133 | 3 | 2 | 1 | both | RED |
| nxn8_pw_fmt_intr | nxn8 | fe0e4c37 | 78b1b0b6 | 0 | 3133 | 3 | 3 | 0 | both | RED |
| nxn8_pw_fmt_late | nxn8 | fe0e4c37 | 895f9735 | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_fmt_lock | nxn8 | fe0e4c37 | aac9dfc1 | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_fmt_mr | nxn8 | fe0e4c37 | 48801155 | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_fmt_seq | nxn8 | fe0e4c37 | 1593f85d | 0 | 3133 | 3 | 3 | 0 | both | RED |
| nxn8_pw_fmt_tu | nxn8 | fe0e4c37 | 7ed71789 | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_fmt_unlock | nxn8 | fe0e4c37 | 710f069e | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_late_early | nxn8 | fe0e4c37 | d1256fdc | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_late_intr | nxn8 | fe0e4c37 | b874d7b2 | 0 | 3133 | 3 | 3 | 0 | both | RED |
| nxn8_pw_late_lock | nxn8 | fe0e4c37 | 9fe35135 | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_late_unlock | nxn8 | fe0e4c37 | 398185e3 | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_lock_intr | nxn8 | fe0e4c37 | 502a4a50 | 0 | 3133 | 5 | 5 | 0 | both | RED |
| nxn8_pw_lock_unlock | nxn8 | fe0e4c37 | c7cba1b5 | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_mr_early | nxn8 | fe0e4c37 | 9cd7d5fd | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_mr_intr | nxn8 | fe0e4c37 | e1af3612 | 0 | 3133 | 3 | 3 | 0 | both | RED |
| nxn8_pw_mr_late | nxn8 | fe0e4c37 | a9d1b6e4 | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_mr_lock | nxn8 | fe0e4c37 | 0b749fdc | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_mr_tu | nxn8 | fe0e4c37 | 453bee83 | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_mr_unlock | nxn8 | fe0e4c37 | f5d0a573 | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_pdu_early | nxn8 | fe0e4c37 | 0df67db0 | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_pdu_fmt | nxn8 | fe0e4c37 | 26c992c1 | 0 | 3133 | 7 | 4 | 3 | both | RED |
| nxn8_pw_pdu_intr | nxn8 | fe0e4c37 | 5e6e7fff | 0 | 3133 | 8 | 6 | 2 | both | RED |
| nxn8_pw_pdu_late | nxn8 | fe0e4c37 | ec2ed862 | 0 | 3133 | 6 | 4 | 2 | both | RED |
| nxn8_pw_pdu_lock | nxn8 | fe0e4c37 | 1f16e27e | 0 | 3133 | 8 | 6 | 2 | both | RED |
| nxn8_pw_pdu_mr | nxn8 | fe0e4c37 | ef39441a | 0 | 3133 | 6 | 4 | 2 | both | RED |
| nxn8_pw_pdu_seq | nxn8 | fe0e4c37 | c0359436 | 0 | 3133 | 8 | 5 | 3 | both | RED |
| nxn8_pw_pdu_tu | nxn8 | fe0e4c37 | e075990f | 0 | 3133 | 6 | 4 | 2 | both | RED |
| nxn8_pw_pdu_unlock | nxn8 | fe0e4c37 | cf348925 | 0 | 3133 | 8 | 6 | 2 | both | RED |
| nxn8_pw_seq_early | nxn8 | fe0e4c37 | 65b05319 | 0 | 3133 | 4 | 3 | 1 | both | RED |
| nxn8_pw_seq_intr | nxn8 | fe0e4c37 | 4ea7d438 | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_seq_late | nxn8 | fe0e4c37 | 2e969957 | 0 | 3133 | 3 | 3 | 0 | both | RED |
| nxn8_pw_seq_lock | nxn8 | fe0e4c37 | aca8a43f | 0 | 3133 | 5 | 5 | 0 | both | RED |
| nxn8_pw_seq_mr | nxn8 | fe0e4c37 | 8fdb00a1 | 0 | 3133 | 3 | 3 | 0 | both | RED |
| nxn8_pw_seq_tu | nxn8 | fe0e4c37 | 32016867 | 0 | 3133 | 3 | 3 | 0 | both | RED |
| nxn8_pw_seq_unlock | nxn8 | fe0e4c37 | 671c6fa8 | 0 | 3133 | 5 | 5 | 0 | both | RED |
| nxn8_pw_tu_early | nxn8 | fe0e4c37 | 979ab55d | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_tu_intr | nxn8 | fe0e4c37 | 2f97bb36 | 0 | 3133 | 3 | 3 | 0 | both | RED |
| nxn8_pw_tu_late | nxn8 | fe0e4c37 | 34aa5354 | 0 | 3133 | 2 | 2 | 0 | both | RED |
| nxn8_pw_tu_lock | nxn8 | fe0e4c37 | 2c4d8975 | 0 | 3133 | 4 | 4 | 0 | both | RED |
| nxn8_pw_tu_unlock | nxn8 | fe0e4c37 | b49ab4c0 | 0 | 3133 | 3 | 3 | 0 | both | RED |
| nxn8_pw_unlock_intr | nxn8 | fe0e4c37 | fa89ccd8 | 0 | 3133 | 5 | 5 | 0 | both | RED |
| nxn8_r268_p1_bind_lock_unlock | nxn8 | fe0e4c37 | c258524d | 0 | 3133 | 4 | 4 | 0 |  | RED |
| nxn8_r268_p2_bind_late_early | nxn8 | fe0e4c37 | 1b5419b3 | 0 | 3133 | 2 | 2 | 0 |  | RED |
| nxn8_r268_p3_bind_mr_tu | nxn8 | fe0e4c37 | efefbfaf | 0 | 3133 | 2 | 2 | 0 |  | RED |
| nxn8_r268_p4_bind_intr_lock | nxn8 | fe0e4c37 | 4839430b | 0 | 3133 | 5 | 5 | 0 |  | RED |
| nxn8_r268_p5_bind_fmt_late | nxn8 | fe0e4c37 | 0612257a | 0 | 3133 | 2 | 2 | 0 |  | RED |
| nxn8_r269_mx1_port_swap_mr_tu | nxn8 | fe0e4c37 | 453bee83 | 0 | 3133 | 2 | 2 | 0 |  | RED |
| nxn8_r269_mx2_port_swap_locked_unlocked | nxn8 | fe0e4c37 | c7cba1b5 | 0 | 3133 | 4 | 4 | 0 |  | RED |
| nxn8_r269_mx3_port_swap_late_early | nxn8 | fe0e4c37 | d1256fdc | 0 | 3133 | 2 | 2 | 0 |  | RED |
| nxn8_r269_mx4_port_swap_intr_locked | nxn8 | fe0e4c37 | 502a4a50 | 0 | 3133 | 5 | 5 | 0 |  | RED |
| nxn_pw_early_intr | nxn | fe0e4c37 | e8add015 | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_early_lock | nxn | fe0e4c37 | 20e71520 | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_early_unlock | nxn | fe0e4c37 | 30ed16d2 | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_fmt_early | nxn | fe0e4c37 | b7082861 | 0 | 1705 | 3 | 2 | 1 | both | RED |
| nxn_pw_fmt_intr | nxn | fe0e4c37 | 78b1b0b6 | 0 | 1705 | 3 | 3 | 0 | both | RED |
| nxn_pw_fmt_late | nxn | fe0e4c37 | 895f9735 | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_fmt_lock | nxn | fe0e4c37 | aac9dfc1 | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_fmt_mr | nxn | fe0e4c37 | 48801155 | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_fmt_seq | nxn | fe0e4c37 | 1593f85d | 0 | 1705 | 3 | 3 | 0 | both | RED |
| nxn_pw_fmt_tu | nxn | fe0e4c37 | 7ed71789 | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_fmt_unlock | nxn | fe0e4c37 | 710f069e | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_late_early | nxn | fe0e4c37 | d1256fdc | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_late_intr | nxn | fe0e4c37 | b874d7b2 | 0 | 1705 | 3 | 3 | 0 | both | RED |
| nxn_pw_late_lock | nxn | fe0e4c37 | 9fe35135 | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_late_unlock | nxn | fe0e4c37 | 398185e3 | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_lock_intr | nxn | fe0e4c37 | 502a4a50 | 0 | 1705 | 5 | 5 | 0 | both | RED |
| nxn_pw_lock_unlock | nxn | fe0e4c37 | c7cba1b5 | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_mr_early | nxn | fe0e4c37 | 9cd7d5fd | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_mr_intr | nxn | fe0e4c37 | e1af3612 | 0 | 1705 | 3 | 3 | 0 | both | RED |
| nxn_pw_mr_late | nxn | fe0e4c37 | a9d1b6e4 | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_mr_lock | nxn | fe0e4c37 | 0b749fdc | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_mr_tu | nxn | fe0e4c37 | 453bee83 | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_mr_unlock | nxn | fe0e4c37 | f5d0a573 | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_pdu_early | nxn | fe0e4c37 | 0df67db0 | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_pdu_fmt | nxn | fe0e4c37 | 26c992c1 | 0 | 1705 | 7 | 4 | 3 | both | RED |
| nxn_pw_pdu_intr | nxn | fe0e4c37 | 5e6e7fff | 0 | 1705 | 8 | 6 | 2 | both | RED |
| nxn_pw_pdu_late | nxn | fe0e4c37 | ec2ed862 | 0 | 1705 | 6 | 4 | 2 | both | RED |
| nxn_pw_pdu_lock | nxn | fe0e4c37 | 1f16e27e | 0 | 1705 | 8 | 6 | 2 | both | RED |
| nxn_pw_pdu_mr | nxn | fe0e4c37 | ef39441a | 0 | 1705 | 6 | 4 | 2 | both | RED |
| nxn_pw_pdu_seq | nxn | fe0e4c37 | c0359436 | 0 | 1705 | 8 | 5 | 3 | both | RED |
| nxn_pw_pdu_tu | nxn | fe0e4c37 | e075990f | 0 | 1705 | 6 | 4 | 2 | both | RED |
| nxn_pw_pdu_unlock | nxn | fe0e4c37 | cf348925 | 0 | 1705 | 8 | 6 | 2 | both | RED |
| nxn_pw_seq_early | nxn | fe0e4c37 | 65b05319 | 0 | 1705 | 4 | 3 | 1 | both | RED |
| nxn_pw_seq_intr | nxn | fe0e4c37 | 4ea7d438 | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_seq_late | nxn | fe0e4c37 | 2e969957 | 0 | 1705 | 3 | 3 | 0 | both | RED |
| nxn_pw_seq_lock | nxn | fe0e4c37 | aca8a43f | 0 | 1705 | 5 | 5 | 0 | both | RED |
| nxn_pw_seq_mr | nxn | fe0e4c37 | 8fdb00a1 | 0 | 1705 | 3 | 3 | 0 | both | RED |
| nxn_pw_seq_tu | nxn | fe0e4c37 | 32016867 | 0 | 1705 | 3 | 3 | 0 | both | RED |
| nxn_pw_seq_unlock | nxn | fe0e4c37 | 671c6fa8 | 0 | 1705 | 5 | 5 | 0 | both | RED |
| nxn_pw_tu_early | nxn | fe0e4c37 | 979ab55d | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_tu_intr | nxn | fe0e4c37 | 2f97bb36 | 0 | 1705 | 3 | 3 | 0 | both | RED |
| nxn_pw_tu_late | nxn | fe0e4c37 | 34aa5354 | 0 | 1705 | 2 | 2 | 0 | both | RED |
| nxn_pw_tu_lock | nxn | fe0e4c37 | 2c4d8975 | 0 | 1705 | 4 | 4 | 0 | both | RED |
| nxn_pw_tu_unlock | nxn | fe0e4c37 | b49ab4c0 | 0 | 1705 | 3 | 3 | 0 | both | RED |
| nxn_pw_unlock_intr | nxn | fe0e4c37 | fa89ccd8 | 0 | 1705 | 5 | 5 | 0 | both | RED |
| nxn_r268_a1_row_removed | nxn | fe0e4c37 | de66991e | 0 | 1705 | 32 | 32 | 0 |  | RED |
| nxn_r268_a2_q0_q1_swap | nxn | fe0e4c37 | 74d89986 | 0 | 1705 | 6 | 6 | 0 |  | RED |
| nxn_r268_a3_q11_16bit | nxn | fe0e4c37 | 5e40fe25 | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn_r268_a4_mask_fff | nxn | fe0e4c37 | ff513c3f | 0 | 1705 | 4 | 4 | 0 |  | RED |
| nxn_r268_a5_dirty_removed | nxn | fe0e4c37 | 2d076efe | 0 | 1705 | 1 | 1 | 0 |  | RED |
| nxn_r268_a6_crf_answers_aaf | nxn | fe0e4c37 | 6d311956 | 0 | 1705 | 8 | 1 | 7 |  | RED |
| nxn_r268_a7_aaf_guard_le | nxn | fe0e4c37 | df5e01ed | 0 | 1705 | 32 | 32 | 0 |  | RED |
| nxn_r268_a8_q2_zero | nxn | fe0e4c37 | 32cc3767 | 0 | 1705 | 4 | 4 | 0 |  | RED |
| nxn_r268_ctl_marked | nxn | fe0e4c37 | 285fcc52 | 0 | 1705 | 0 | 0 | 0 |  | green |
| nxn_r268_p1_bind_lock_unlock | nxn | fe0e4c37 | c258524d | 0 | 1705 | 4 | 4 | 0 |  | RED |
| nxn_r268_p2_bind_late_early | nxn | fe0e4c37 | 1b5419b3 | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn_r268_p3_bind_mr_tu | nxn | fe0e4c37 | efefbfaf | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn_r268_p4_bind_intr_lock | nxn | fe0e4c37 | 4839430b | 0 | 1705 | 5 | 5 | 0 |  | RED |
| nxn_r268_p5_bind_fmt_late | nxn | fe0e4c37 | 0612257a | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn_r268_r1_index_ge | nxn | fe0e4c37 | 052d6258 | 0 | 1705 | 0 | 0 | 0 |  | green |
| nxn_r268_r2_sout_offset | nxn | fe0e4c37 | 254ef967 | 0 | 1705 | 1 | 0 | 1 |  | RED |
| nxn_r268_r3_crf_pend_stuck | nxn | fe0e4c37 | 6e876a42 | 0 | 1705 | 0 | 0 | 0 |  | green |
| nxn_r268_r4_type_dropped | nxn | fe0e4c37 | f9409fcc | 0 | 1705 | 6 | 0 | 6 |  | RED |
| nxn_r268_r5_dirty_order | nxn | fe0e4c37 | e7d71aa3 | 0 | 1705 | 2 | 1 | 1 |  | RED |
| nxn_r268_r6_rr_sout_old | nxn | fe0e4c37 | d98edcb5 | 0 | 1705 | 0 | 0 | 0 |  | green |
| nxn_r268_r7_pick_sin_old | nxn | fe0e4c37 | dc291f0f | 0 | 1705 | 1 | 1 | 0 |  | RED |
| nxn_r269_ma1_mask_fff | nxn | fe0e4c37 | 061ca21c | 0 | 1705 | 4 | 4 | 0 |  | RED |
| nxn_r269_ma2_mux_swap_q0_q1 | nxn | fe0e4c37 | 4db0ad5d | 0 | 1705 | 6 | 6 | 0 |  | RED |
| nxn_r269_ma3_dirty_removed | nxn | fe0e4c37 | 53f38c46 | 0 | 1705 | 1 | 1 | 0 |  | RED |
| nxn_r269_ma4_crf_arm_no_index_first | nxn | fe0e4c37 | 24283fcc | 0 | 1705 | 8 | 1 | 7 |  | RED |
| nxn_r269_ma5_q11_16bit_slice | nxn | fe0e4c37 | 921f098c | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn_r269_ma6_aaf_guard_le | nxn | fe0e4c37 | 79d64376 | 0 | 1705 | 32 | 32 | 0 |  | RED |
| nxn_r269_ma7_row_removed_public | nxn | fe0e4c37 | de66991e | 0 | 1705 | 32 | 32 | 0 |  | RED |
| nxn_r269_mx1_port_swap_mr_tu | nxn | fe0e4c37 | 453bee83 | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn_r269_mx2_port_swap_locked_unlocked | nxn | fe0e4c37 | c7cba1b5 | 0 | 1705 | 4 | 4 | 0 |  | RED |
| nxn_r269_mx3_port_swap_late_early | nxn | fe0e4c37 | d1256fdc | 0 | 1705 | 2 | 2 | 0 |  | RED |
| nxn_r269_mx4_port_swap_intr_locked | nxn | fe0e4c37 | 502a4a50 | 0 | 1705 | 5 | 5 | 0 |  | RED |
| nxndv_r268_p1_bind_lock_unlock | nxndv | fe0e4c37 | c258524d | 0 | 1707 | 4 | 4 | 0 |  | RED |
| nxndv_r268_p2_bind_late_early | nxndv | fe0e4c37 | 1b5419b3 | 0 | 1707 | 2 | 2 | 0 |  | RED |
| nxndv_r268_p3_bind_mr_tu | nxndv | fe0e4c37 | efefbfaf | 0 | 1707 | 2 | 2 | 0 |  | RED |
| nxndv_r268_p4_bind_intr_lock | nxndv | fe0e4c37 | 4839430b | 0 | 1707 | 5 | 5 | 0 |  | RED |
| nxndv_r268_p5_bind_fmt_late | nxndv | fe0e4c37 | 0612257a | 0 | 1707 | 2 | 2 | 0 |  | RED |
| nxndv_r269_mx1_port_swap_mr_tu | nxndv | fe0e4c37 | 453bee83 | 0 | 1707 | 2 | 2 | 0 |  | RED |
| nxndv_r269_mx2_port_swap_locked_unlocked | nxndv | fe0e4c37 | c7cba1b5 | 0 | 1707 | 4 | 4 | 0 |  | RED |
| nxndv_r269_mx3_port_swap_late_early | nxndv | fe0e4c37 | d1256fdc | 0 | 1707 | 2 | 2 | 0 |  | RED |
| nxndv_r269_mx4_port_swap_intr_locked | nxndv | fe0e4c37 | 502a4a50 | 0 | 1707 | 5 | 5 | 0 |  | RED |

pairwise receipts missing a red on either own quadlet: none

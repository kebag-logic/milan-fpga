"""Insert $info prints of the #773 derived terms into a disposable copy of the
tree (KL_aaf_packetizer, KL_crf_tx, milan_datapath) for derive_probe.sh.
usage: python3 derive_probe_insert.py <tree-copy>"""
import sys
T = sys.argv[1]
def ins(path, anchor, text):
    s = open(path).read()
    assert s.count(anchor) == 1, (path, anchor)
    open(path, 'w').write(s.replace(anchor, anchor + text))
ins(T + '/hdl/ieee1722/aaf/KL_aaf_packetizer.sv', '  end : g_lead_delay\n',
    '  if (LEAD_P) begin : g_probe\n    $info("PROBE aaf N=%0d FS=%0d CLK=%0d IN_LATE=%0d PIPE_CYC=%0d LATE_NS=%0d DELAY_PER=%0d LEAD_NS=%0d SPARE=%0d", N_TALKERS_P, FS_HZ_P, CLK_HZ_P, IN_LATE_NS_P, PIPE_CYC_C, LATE_NS_C, DELAY_PER_C, LEAD_NS_C, (DELAY_PER_C*64\'d1_000_000_000)/FS_HZ_P - LATE_NS_C);\n  end\n')
ins(T + '/hdl/ieee1722/crf/KL_crf_tx.sv', '  end : g_tc_clock\n',
    '  if (TC_P) begin : g_probe\n    $info("PROBE crf EV_LATE=%0d PIPE_CYC=%0d LATE_NS=%0d TC_PER=%0d TC_NS=%0d SPARE=%0d", EV_LATE_NS_P, PIPE_CYC_C, LATE_NS_C, TC_PER_C, TC_NS_C, (TC_PER_C*MCLK_NUM_C)/MCLK_DEN_C - LATE_NS_C);\n  end\n')
ins(T + '/hdl/milan/milan_datapath.sv', "      64'd1, 64'(MILAN_CLK_FREQ_HZ)));\n",
    '  if (1) begin : g_probe_tlk\n    $info("PROBE tlk FS=%0d SLOTS=%0d N=%0d MARK_LAT=%0d SPAN=%0d AGE=%0d WALK=%0d LB_PAIRS=%0d AAF_IN=%0d CRF_EV=%0d", AUDIO_IF_FS_HZ_P, AUDIO_IF_SLOTS_P, N_STREAMS, DOM_MARK_LAT_NS_C, TLK_SPAN_NS_C, TLK_AGE_CYC_C, TLK_WALK_CYC_C, TLK_LB_PAIRS_C, TLK_AAF_IN_NS_C, TLK_CRF_EV_NS_C);\n  end\n')

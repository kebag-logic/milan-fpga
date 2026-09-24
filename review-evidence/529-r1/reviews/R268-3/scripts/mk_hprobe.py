#!/usr/bin/env python3
"""Disposable harness-only probe on TREE/tb/verilator/milan_dp/sim_nxn.cpp.
Adds no check and changes no verdict; it only prints [probe] lines:
 (1) every arbiter delivery inside the CRF bind-edge window, with the step
     number at which step() saw it, and the window's total step count;
 (2) around the [NOTIFY-CRF] solicited exchange (aecp_xact_from), whether
     uns_log's storage moved (the n1 pointer held across it would dangle),
     with size and capacity before and after.
usage: mk_hprobe.py TREE"""
import sys
p = sys.argv[1] + "/tb/verilator/milan_dp/sim_nxn.cpp"
s = open(p).read()

def sub(old, new, n=1):
    global s
    assert s.count(old) == n, (old, s.count(old))
    s = s.replace(old, new)

sub("""    unsigned long pp_ctr_evt_other_n = 0;
""", """    unsigned long pp_ctr_evt_other_n = 0;
    bool probe_win = false; long probe_k = 0;
""")
sub("""        tkd_dirty_seen |= dut->rootp->milan_datapath__DOT__tkd_dirty_p_w;
""", """        tkd_dirty_seen |= dut->rootp->milan_datapath__DOT__tkd_dirty_p_w;
        if (probe_win) {
            if (dut->rootp->milan_datapath__DOT__pp_ctr_evt_valid_w)
                printf("  [probe] window step %ld: delivered ty=0x%04x ix=%u\\n", probe_k,
                       (unsigned)dut->rootp->milan_datapath__DOT__pp_ctr_evt_type_w,
                       (unsigned)dut->rootp->milan_datapath__DOT__pp_ctr_evt_index_w);
            probe_k++;
        }
""")
sub("""        pp_ctr_evt_other_n = 0;
        crf_lever(true);
""", """        pp_ctr_evt_other_n = 0;
        probe_win = true; probe_k = 0;
        crf_lever(true);
        probe_win = false;
        printf("  [probe] bind-edge window: %ld steps observed\\n", probe_k);
""")
sub("""        const std::vector<uint8_t> g = aecp_xact_from(CTL_B, 0x0029, notify_sq++, key);
        ck("[NOTIFY-CRF] ...byte-identical""", """        const void* probe_d0 = uns_log.data();
        const size_t probe_s0 = uns_log.size(), probe_c0 = uns_log.capacity();
        const std::vector<uint8_t> g = aecp_xact_from(CTL_B, 0x0029, notify_sq++, key);
        printf("  [probe] NOTIFY-CRF exchange: uns_log size %zu->%zu capacity %zu->%zu storage %s\\n",
               probe_s0, uns_log.size(), probe_c0, uns_log.capacity(),
               probe_d0 == static_cast<const void*>(uns_log.data()) ? "UNMOVED" : "MOVED");
        ck("[NOTIFY-CRF] ...byte-identical""")
open(p, "w").write(s)
print("patched", p)

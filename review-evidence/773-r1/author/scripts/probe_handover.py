#!/usr/bin/env python3
"""Scratch probe (#773), applied to a disposable clone only: in the
capture_coherence whole-datapath leg (sim_dp.cpp, the shipping 1x1 TDM8
shape), record for every AAF PDU the PHC at its MAC hand-over (the accepted
first and last beat at m_axis_mac_tx) minus (avtp_timestamp - the 2 ms
offset), i.e. the hand-over measured from the stamped media instant M.
Usage: probe_handover.py <path to sim_dp.cpp>"""
import sys
p = sys.argv[1]
s = open(p).read()
def sub(old, new):
    global s
    if old not in s:
        sys.exit("anchor not found: " + old[:60])
    s = s.replace(old, new, 1)
sub("""    std::uint64_t dom_prev_ = 0;
    long dom_events_ = 0;
    double dom_max_ = 0;
    void note_pins();""", """    std::uint64_t dom_prev_ = 0;
    long dom_events_ = 0;
    double dom_max_ = 0;
    bool pr_inframe_ = false;
    std::int64_t pr_first_ = 0;
    long pr_n_ = 0;
    std::int64_t pr_lmin_ = 0, pr_lmax_ = 0, pr_fmin_ = 0, pr_fmax_ = 0;
    std::int64_t pr_amin_ = 0, pr_amax_ = 0;
    long pr_fb_ = 0, pr_fb_last_ = -1;
    std::int64_t pr_dmin_ = 0, pr_dmax_ = 0;
    void note_pins();""")
sub("""    dom_prev_ = 0;
    dom_events_ = 0;
    dom_max_ = 0;
    dut_->axis_resetn = 0;""", """    dom_prev_ = 0;
    dom_events_ = 0;
    dom_max_ = 0;
    pr_inframe_ = false;
    pr_n_ = 0;
    pr_lmin_ = pr_fmin_ = pr_amin_ = INT64_MAX;
    pr_lmax_ = pr_fmax_ = pr_amax_ = INT64_MIN;
    pr_fb_ = 0; pr_fb_last_ = -1;
    pr_dmin_ = INT64_MAX; pr_dmax_ = INT64_MIN;
    dut_->axis_resetn = 0;""")
sub("""    if (dut_->m_axis_mac_tx_tvalid && dut_->m_axis_mac_tx_tready) {
        bench_.beat(dut_->m_axis_mac_tx_tdata, dut_->m_axis_mac_tx_tkeep, dut_->m_axis_mac_tx_tlast != 0);
    }""", """    if (dut_->m_axis_mac_tx_tvalid && dut_->m_axis_mac_tx_tready) {
        if (!pr_inframe_) { pr_first_ = phc_edge_; pr_inframe_ = true; }
        const size_t before = bench_.stamps.size();
        const bool last = dut_->m_axis_mac_tx_tlast != 0;
        bench_.beat(dut_->m_axis_mac_tx_tdata, dut_->m_axis_mac_tx_tkeep, last);
        if (last) {
            pr_inframe_ = false;
            if (bench_.stamps.size() > before) {
                const std::uint32_t base = bench_.stamps.back().ts - kPtoNs;
                const std::int64_t dl = static_cast<std::int32_t>(static_cast<std::uint32_t>(phc_edge_) - base);
                const std::int64_t df = static_cast<std::int32_t>(static_cast<std::uint32_t>(pr_first_) - base);
                pr_n_++;
                pr_lmin_ = std::min(pr_lmin_, dl); pr_lmax_ = std::max(pr_lmax_, dl);
                pr_fmin_ = std::min(pr_fmin_, df); pr_fmax_ = std::max(pr_fmax_, df);
                if (tail_) { pr_amin_ = std::min(pr_amin_, dl); pr_amax_ = std::max(pr_amax_, dl); }
                //! below 5 Ps + the marker latency (125,130 ns) a PDU cannot carry a domain-event base: its sixth
                //! frame is not complete before then, so it is the live-PHC fallback (dom_live_w low at its stamp)
                if (dl < 125'130) { pr_fb_++; pr_fb_last_ = pr_n_ - 1; }
                else { pr_dmin_ = std::min(pr_dmin_, dl); pr_dmax_ = std::max(pr_dmax_, dl); }
            }
        }
    }""")
sub("""    bench_.finish();
    const std::uint64_t fails_before = check_.failures();""", """    bench_.finish();
    std::printf("  [PROBE] %s: %ld AAF PDUs; MAC hand-over minus (avtp_timestamp - offset): last beat %lld..%lld ns, "
                "first beat %lld..%lld ns; second half (CRF tail) last beat %lld..%lld ns\\n", sc.name.c_str(), pr_n_,
                (long long)pr_lmin_, (long long)pr_lmax_, (long long)pr_fmin_, (long long)pr_fmax_,
                (long long)(pr_amin_ == INT64_MAX ? 0 : pr_amin_), (long long)(pr_amax_ == INT64_MIN ? 0 : pr_amax_));
    std::printf("  [PROBE] %s: domain-event-stamped PDUs %ld, last beat %lld..%lld ns; live-PHC fallback PDUs %ld "
                "(last at PDU index %ld)\\n", sc.name.c_str(), pr_n_ - pr_fb_,
                (long long)(pr_dmin_ == INT64_MAX ? 0 : pr_dmin_), (long long)(pr_dmax_ == INT64_MIN ? 0 : pr_dmax_),
                pr_fb_, pr_fb_last_);
    const std::uint64_t fails_before = check_.failures();""")
open(p, "w").write(s)
print("probe applied:", p)

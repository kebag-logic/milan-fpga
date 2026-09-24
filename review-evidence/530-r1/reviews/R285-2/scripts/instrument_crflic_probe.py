#!/usr/bin/env python3
"""Instrument a DISPOSABLE copy of tb/verilator/milan_dp/sim_crf_licence.cpp.

Usage: instrument_crflic_probe.py <copy-of-sim_crf_licence.cpp>

Adds a passive observer (no stimulus change, no check change) that, every
cycle, per source uid, records:
  * each Talker Advertise self-declaration edge (tk_decl_state NONE -> set),
    the Listener registration code seen in the cycle before the edge, at the
    edge, and whether a Ready/ReadyFailed registration was seen at any cycle in
    the 200 ms before the edge (a re-declaration a Listener registration
    "outlived");
  * each ACTIVE rising edge, whether the raw verdict sr_admitted was 0 at that
    cycle (an opening inside the optimistic window), and its distance in
    cycles from the latest declaration edge.
It prints one PROBE block before the leg's RESULT line. The leg's own checks
and verdict are untouched.
"""
import sys

path = sys.argv[1]
src = open(path, encoding='utf-8').read()

GLOBALS = '''
// ---- R285-2 disposable probe (passive observer) ----
struct ProbeSrc {
    unsigned prev_tks = 0, prev_lstn = 0, prev_act = 0;
    uint64_t last_ready_cyc = 0; bool ever_ready = false;
    uint64_t last_decl_cyc = 0; bool have_decl = false;
    long decl_edges = 0, decl_lstn_ready_before = 0, decl_lstn_ready_at = 0;
    long decl_ready_within_window = 0;
    long act_rises = 0, act_rise_unadmitted = 0;
    uint64_t min_rise_after_decl = ~0ull;
};
static ProbeSrc g_probe[8];
'''

anchor = 'void CrfLicenceHarness::sample_levels() {'
assert src.count(anchor) == 1
src = src.replace(anchor, GLOBALS + anchor, 1)

HOOK_ANCHOR = '    const bool lic = rp->milan_datapath__DOT__crft_emit_en_w & 1u;'
assert src.count(HOOK_ANCHOR) == 1
HOOK = '''    {
        const unsigned lrs = rp->milan_datapath__DOT__pp_cd_srp_lstn_reg_state_w;
        for (int s = 0; s < kSources; s++) {
            ProbeSrc& p = g_probe[s];
            const unsigned t = (tks >> (2 * s)) & 3u;
            const unsigned l = (lrs >> (2 * s)) & 3u;
            const unsigned a = (act >> s) & 1u;
            const unsigned m = (adm >> s) & 1u;
            const uint64_t win = static_cast<uint64_t>(200) * static_cast<uint64_t>(MS_CYC_TB);
            if (p.prev_tks == 0 && t != 0) {
                p.decl_edges++;
                if (p.prev_lstn == 2 || p.prev_lstn == 3) p.decl_lstn_ready_before++;
                if (l == 2 || l == 3) p.decl_lstn_ready_at++;
                if (p.ever_ready && cyc - p.last_ready_cyc <= win) p.decl_ready_within_window++;
                p.last_decl_cyc = cyc; p.have_decl = true;
                printf("[PROBE] uid %d decl edge @%llu cyc: lstn before=%u at=%u, Ready seen %lld cyc earlier\\n",
                       s, static_cast<unsigned long long>(cyc), p.prev_lstn, l,
                       p.ever_ready ? static_cast<long long>(cyc - p.last_ready_cyc) : -1ll);
            }
            if (!p.prev_act && a) {
                p.act_rises++;
                if (!m) p.act_rise_unadmitted++;
                const uint64_t d = p.have_decl ? cyc - p.last_decl_cyc : ~0ull;
                if (d < p.min_rise_after_decl) p.min_rise_after_decl = d;
                printf("[PROBE] uid %d ACTIVE rise @%llu cyc: sr_admitted=%u, %llu cyc after decl edge\\n",
                       s, static_cast<unsigned long long>(cyc), m, static_cast<unsigned long long>(d));
            }
            if (l == 2 || l == 3) { p.last_ready_cyc = cyc; p.ever_ready = true; }
            p.prev_tks = t; p.prev_lstn = l; p.prev_act = a;
        }
    }
'''
src = src.replace(HOOK_ANCHOR, HOOK + HOOK_ANCHOR, 1)

SUM_ANCHOR = '    printf("checks: %ld   failures: %ld\\n", checks, fails);'
assert src.count(SUM_ANCHOR) == 1
SUMMARY = '''    for (int s = 0; s < kSources; s++) {
        const ProbeSrc& p = g_probe[s];
        printf("[PROBE-SUMMARY] uid %d: decl_edges=%ld lstn_ready_cycle_before_edge=%ld "
               "lstn_ready_at_edge=%ld ready_within_200ms_before_edge=%ld act_rises=%ld "
               "act_rise_with_sr_admitted_0=%ld min_cyc_decl_to_act_rise=%llu\\n",
               s, p.decl_edges, p.decl_lstn_ready_before, p.decl_lstn_ready_at,
               p.decl_ready_within_window, p.act_rises, p.act_rise_unadmitted,
               static_cast<unsigned long long>(p.min_rise_after_decl));
    }
'''
src = src.replace(SUM_ANCHOR, SUMMARY + SUM_ANCHOR, 1)
open(path, 'w', encoding='utf-8').write(src)
print('instrumented', path)

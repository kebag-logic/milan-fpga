# R437-3: my round-2 F1/F2 plants (Y1, Y11, Y16; the exact round-2 edit text,
# copied from r2/spec_y_pause.py and r2/spec_z2_directed.py) at the head, under
# the seven contract-legal models, at the third build's bound 20 (100 and 37
# are re-run by the round-2 specs unchanged), and Y11 at 100 and 37 under all
# seven as well.
PROBES = {
    "Y1_wewait_owes_latched": [('RTL', '                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)\n                       || (state_r == S_RPWAIT)) && !done_seen_r)\n', '                  || (((state_r == S_WWAIT) || (state_r == S_RHWAIT) || (state_r == S_RPWAIT)) && !done_seen_r) || (state_r == S_WEWAIT)\n')],
    "Y11_verdict_on_paused_cycle": [('RTL', '  assign dl_w = owe_w && !prog_w && tmo_hit_w;', '  assign dl_w = (owe_w || (state_r == S_WDPUMP) || (state_r == S_RPPUMP)) && !prog_w && tmo_hit_w;')],
    "Y16_verdict_any_busy_cycle": [("RTL", "  assign dl_w = owe_w && !prog_w && tmo_hit_w;",
                                    "  assign dl_w = (state_r != S_IDLE) && (state_r != S_FIN) && !prog_w && tmo_hit_w;")],
}
LEGAL7 = ["pristine", "half-page", "page-buffered NOR", "lazy erase", "lazy erase + page-buffered",
          "coincident completion", "unsolicited completion"]
RUNS = [(p, m, 20) for p in PROBES for m in LEGAL7]
RUNS += [("Y11_verdict_on_paused_cycle", m, t) for m in LEGAL7[1:] for t in (100, 37)]

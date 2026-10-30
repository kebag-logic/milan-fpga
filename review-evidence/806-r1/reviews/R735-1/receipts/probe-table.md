# Reviewer probe table, exact head f99405af0b2caad46e84f50f8251ffbffaa80836

Each probe is one text replacement from `scripts/mutate.py`, applied alone to a
fresh disposable copy of the reviewed clone (`scripts/probe.sh`). The leg is
rebuilt from scratch with the pinned Verilator 5.050 (`Verilator 5.050
2026-07-01 rev v5.050`, the build log's report line) and run once. Logs are
`probes/<id>.log`; exit status is `probes/<id>.rc`.

| Probe | Planted change | Leg tally | `#94` checks that print FAIL |
|---|---|---|---|
| C0 | none, `make gptp` | 210 / 210 | none |
| C0_lat | none, `make gptp-lat` | 210 / 210 | none |
| D0_diag | prints the graded quantities (no check changed) | 210 / 210 | none; `req-back=316` cycles (158 us at 2 MHz), countdown `req-last=9999990` against 10,000,000 +/- 2,000 |
| W1_tie_high | datapath `.port_enabled_i (1'b1)` | 206 / 210 | link loss, LINK_CTRL[0], toggle exit, guard |
| W2_phy_only | datapath `.port_enabled_i (i_link_up)` | 208 / 210 | LINK_CTRL[0], guard |
| W3_no_guard | datapath `i_link_up & cfg_sw_link` | 209 / 210 | guard |
| W4_no_linkctrl | datapath `i_link_up & (cfg_linkg_dis \| linkg_est_w)` | 209 / 210 | LINK_CTRL[0] |
| W5_no_phy | datapath `cfg_sw_link & (cfg_linkg_dis \| linkg_est_w)` | 208 / 210 | link loss, toggle exit |
| W6_tie_low | datapath `.port_enabled_i (1'b0)` | 99 / 201 | all three preconditions, toggle exit, countdown (the leg loses asCapable from the start) |
| W7_shadow_ignores | `KL_gptp_shadow` passes `1'b1` to the engine | 206 / 210 | link loss, LINK_CTRL[0], toggle exit, guard |
| E1_edge_keeps_cease | donor text "a portEnabled edge keeps the cease" | 207 / 210 | toggle exit, countdown, guard precondition |
| E2_fall_no_event | donor text "the falling edge raises no event" | 207 / 210 | link loss, LINK_CTRL[0], guard |
| E3_countdown_short | donor text "the countdown loads one beat less" | 209 / 210 | countdown |
| E4_slot6_no_leg | donor text "slot 6 runs no NOT_ENABLED leg" | 206 / 210 | link loss, LINK_CTRL[0], toggle exit, guard |
| E5_rise_no_request | donor text "a rise sends no request at once" | 210 / 210 | none: survives, see SUGGESTION S1 |
| E6_disabled_sends | donor text "a disabled port keeps its credit and starts its frames" | 210 / 210 | none: survives, see SUGGESTION S2 |
| T1_no_toggle | the toggle phase keeps the link up (tautology probe) | 209 / 210 | toggle exit |

Consumers on one more disposable copy (`scripts/consumers.sh`), exact head:
`gptp_shadow run` 325 / 325; `gptp_plane run` 29 / 29; `gptp_txts run` 85
checks, 0 failures; `milan_dp gmstep` 196 checks, 0 failures. All rc 0; that
copy's `git status` is empty afterwards.

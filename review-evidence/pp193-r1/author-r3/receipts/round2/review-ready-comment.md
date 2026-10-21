[A661] REVIEW READY
Head: processor `193-shared-listener-leave` = 7b424cdfe111a426f00517ff471246b4b9650726. That is five new commits on the PR #198 head 6ddfcda4; not pushed, no rebase, no amend.

Round 2 (the [A10] assignment on PR #198, answering R679-1 and R680-1). The RTL change is in `KL_srp_listener_fsm` only; no port, parameter or register-map change.
- F1: a parked applicant (#188) is now in the group of the value it holds, by its leave copy. A sink that settles on that StreamID is a rider of it. The group's first declaration takes the applicant over through the existing handover: LA/LO + New! = VN, the #188 re-probe rule. So one New goes out and no Lv, and the parker's own request is released. While no sink on the value declares, the owed Lv goes out once, unchanged. If it went out in a walk, the sinks on the value take its walk mark. Banner and 10 §6.4 ("A parked Leave") describe it.
- New checks, each failing on 6ddfcda4 and KILLED by a named control:
  - SH10-SH13 (both index orders x A15 / A8+A15): per tick, peer Registrar IN.
  - SW4-SW7 (the same forms on the wire): byte-exact one-value frame, peer Registrar IN, 0 deregistrations, 0 Lv.
  - SH14: no declarer, so one Lv and no Empty from the rider after a LeaveAll.
  - SH15: a declaration after the walk sent the parked Lv waits for the next tx!.
  - SH16: a sink whose own Leave goes first, then declares, takes the parked applicant over.
  - Five new controls; `listener-settle-compare-dropped` is re-anchored with its edit unchanged; coverage SH1-SH16, SW1-SW7.
- R679-1's `run_probes.sh` (one wire-probe anchor adapted, since its comment lost the `SW3:` prefix under F3) on the head: no `FAIL: PR`/`FAIL: PW`, one value per tick in every variant, no Lv while the joiner declares, peer IN with 0 deregistrations. R680-1's two parked probes (revision guard set to the head): 2/2 PASS each.
- F2: the PR body states the shape beside the area figure, the module defaults (8 Stream Inputs, 8 Stream Outputs). It says no 1x1 figure was measured and the 4th pin adoption's route-1x1 measures the shipped cost.
- F4/F3: the two test comments cite 35.1.2.2 and 35.2.4.4.3 (Table 35-14), keeping 35.2.6 for the change in place; the `SW` labels are gone.
- S2: probed. A handover to a slot the walk has passed sends at the next tx!; never lost, never twice. No change; the one-tick delay is now documented.
- Commit 4: the compare copy of the leave copies was first written at a variable index of a packed array, which synthesized as a shifter. One enable per sink: the listener alone at 8 sinks is +322 LUT over 6ddfcda4 instead of +2,251.

Gates, base 6ddfcda4 vs head, all rc 0:
- run_suites: 1,030,356 -> 1,030,367 (only srp_stream_fsms +7 and srp_top +4).
- lint, make check, matrix, portability elaboration and guards: identical.
- srp_top campaign: 196/196 -> 203/203, coverage 113/113 -> 124/124; every base arm keeps its verdict and tags.
- Every other campaign that builds the listener FSM (acmp, notify, d3, aecp, dispatch, ctr, gsi, name_wr, name_state, elab guards) is identical.
- Commit 5 (README counts only): the gates that read the README, run again at 7b424cdf, are identical.

Parent consumer gates (dev 78ca9bdf + the four adoption patches, gitlink committed per pin): all rc 0 at base and head, with `check_submodule_docs` failing identically at both. KL_pp_shadow out-of-context at the module defaults: main 08023123 -> head +1,335 LUT, +618 FF, of which round 2 is +812 LUT, +568 FF; LUTRAM, BRAM, DSP and carry are unchanged.

To confirm: the area above (8x8; no 1x1 figure measured here).

Evidence: lane receipts (HANDOFF Round 2, PR body Round 2, records, index).

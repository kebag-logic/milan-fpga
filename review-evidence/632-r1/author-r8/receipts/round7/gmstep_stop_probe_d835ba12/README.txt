Round 7b: why gmstep-mutants --all fails one control at d835ba12, and that dev e5b480a3 fails it the same way.

The campaign (../gmstep_mutants_d835ba12/) ends "22 checks: 21 PASS, 1 FAIL" (make exit 2): the control
"the grandmaster change stops the talker for good" fails the leg, but not its named check
"licence: the talker never pauses beyond four of its intervals". The driver does not print which checks broke in
that case, so scripts/round7b/gm_stop_probe.py plants that one control exactly as gmstep_mutants.run_control does
(a disposable copy of milan_datapath.sv, the driver's own build() and run_leg()) and prints every failed check.

probe_d835ba12.out, leg_d835ba12.log            the control at this PR's head: 14 checks fail, the named one not among
                                                them; "baseline: the talker streams" fails (the talker never sent a PDU).
probe_dev_e5b480a3.out, leg_dev_e5b480a3.log    the same probe on a clean clone of dev e5b480a3 (the fourth pin
                                                adoption, #771): the same 14 checks fail, the same verdict. Pre-existing.
gm_change_probe_d835ba12.out, gm_change_leg_d835ba12.log
                                                scripts/round7b/gm_change_probe.py: a display of every change of the
                                                detector's input cfg_adp_gptp_gm and every gm_recentre_p_r pulse on the
                                                clean leg (no mutation). At boot the published grandmaster goes
                                                0 -> 02a1b2fffec3d4e5 (this station's own identity, FPGA-gPTP #82's boot
                                                grandmaster, adopted by #771) -> 00aaccfffe010203 (GM A, at acquisition);
                                                the second change is non-zero to non-zero, so the detector pulses there,
                                                before the baseline. The control's gm_stop_r therefore stops the talker
                                                from acquisition on, and the pause check has no PDU to measure.

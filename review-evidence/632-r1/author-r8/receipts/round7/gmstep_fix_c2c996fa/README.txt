Round 7c: the test-only fix of the gmstep control "the grandmaster change stops
the talker for good", proven planted alone, and the new control.

Probe: scripts/round7b/gm_stop_probe.py <out> [control name] - the driver's own
plant, build (gmstep-build through the milan_dp recipe) and run, on the whole
leg (no --no-small-steps), from tb/verilator/milan_dp_gm_steps.

"head": the lane tree before the commit; its four test files (Makefile,
sim_gmstep.cpp, gmstep_mutants.py, gmstep_probes.vlt) are byte-equal to
c2c996fa's (sha256 compared after applying the archived patch to d835ba12).
"dev": a clean clone of dev e5b480a3 with only the test fix applied
(dev_e5b480a3_testfix.patch; dev_clone_head.txt, dev_clone_status.txt: the
four test files and nothing else modified; no hdl file).

stop_probe_*.out / stop_leg_*.log: the fixed control planted alone. Verdict
"caught"; "baseline: the talker streams" ok; the boot record ok; 12 failed
checks, "licence: the talker never pauses beyond four of its intervals" among
them (TALKER: 0 PDUs over 825871 cycles to the window end). Same on both.

exempt_probe_*.out / exempt_leg_*.log: the new control "the detector exempts
this station's own boot identity" planted alone. Verdict "caught"; exactly one
failed check, "boot grandmaster: the detector pulsed once, at this station's
own identity -> GM A, and the baseline talker streams after it"; no GMDET line.

clean_leg_tree.log: the clean leg at the same tree: 196 checks, 0 failures;
GMDET: pulse at cycle 6001430, 02a1b2fffec3d4e5 -> 00aaccfffe010203.

lint_c2c996fa.log: lint_rtl.py --check, PASS 89 <= 89.
check_baseline_c2c996fa.log: pp_resource_gate.py check-baseline, PASS.

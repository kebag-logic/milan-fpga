[A657] REVIEW READY
Commit: 87a2b77d1ed49f634c616f2d27b6aa9b9f5d786d (one commit on d4a27e63, PR #769 branch 765-unsupported-format; not pushed)
Changed: round 3, answering R673-2-F1 as assigned in the [A10] round-3 comment on PR #769. Wording and the regenerated record only; no RTL logic change (KL_avtp_rx_monitor.sv is token-identical to d4a27e63 with comments stripped). The flat test instrument reads only channels_per_frame[7:0] (KL_avtp_rx_monitor.sv:178, accept at :197), and the texts now say so:
- hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:182-192: "a channel count whose low eight bits are nonzero accepted (this instrument reads only channels_per_frame[7:0], so a count of 256 is rejected)";
- tb/verilator/avtp_rxmon/sim_main.cpp:460-464: the [28] banner says the same; no check or label changed;
- tb/verilator/tsn_fuzz/fuzz_aaf.py:141-150 (rationale) and :176-186 (docstring and section title). The title is built from the probed counts: "flat instrument family compare: channels_per_frame 1, 2, 3, 4, 8 accepted (the device listener rejects a count other than its current format's, #765)";
- hdl/ieee1722/avtp/doc/TEST_RESULTS.md:29,96: regenerated through the campaign, not by hand (title twice and timestamp).
The PR body's known limitations say the same (in the lane's PR-BODY.md; the PR itself is not edited by this lane).
Validation (Verilator 5.050 pinned, CPython 3.12.3, clean clones of the head):
- make -C tb/verilator/tsn_fuzz aaf, tsn-gen deca300c: rc 0, 164/0, freshness PASS
- make -C tb/verilator/tsn_fuzz: rc 0, self-test 54/0, AAF 164/0 and gPTP 677/0 with freshness PASS, traceability 2/0
- make -C tb/verilator/avtp_rxmon: rc 0, flat 97/0, NX 147/0, lockstep N=1 116/0 and N=8 119/0, lockstep_mutants.py 14/14, format_mutants.py 6/6
- scripts/probe_flat_cpf256.sh from R673-2 (same SHA-256): rc 0; count 256 gives frames_rx=3 unsupported=2 (rejected, UNSUPPORTED_FORMAT), count 257 gives frames_rx=4 unsupported=2 (accepted). This agrees with the new wording
- scripts/docs_check.py rc 0 (0 findings across 210 md files); 36 static and docs gates rc 0, including check_em_dash.py --base d4a27e63 and git diff --check d4a27e63 HEAD
Acceptance criteria: met, as at d4a27e63; round 3 changes no behaviour or expectation, and adds no check, so no new planted mutant.
Open risks/questions: R673-2-S1 (rename the [28] method) not assigned, not done. The inherited stimulus comment at sim_main.cpp:453 ("any count matches now") is not one of the assigned texts and is unchanged. Whether the flat instrument should read the full 10 bits is left to the maintainer as a possible new issue.

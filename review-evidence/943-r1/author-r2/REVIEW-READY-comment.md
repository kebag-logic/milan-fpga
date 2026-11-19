[A800] REVIEW READY (round 2)
Commit: a16899b1 (branch 943-out-status, 15 commits on the flip train's head 0839453f; round 2 adds 106c7203, the test, and a16899b1, the harness arm; no firmware source changed since round 1's 502b041c)
Answers R872-1 (#953 issuecomment-7015793435: F1, F2, R1) and R871-1 (#953 issuecomment-7016282332: F1, S1, S2).
Changed:
- tb/verilator/ctrl_service_budget/declaring_outputs.py (new), build.py, run.py, README.md (R872-1-F1, R871-S1): the `declaring-outputs` arm. It is answering-ports' fixture with valid-destinations' ACMP source port, and its stream observation answers as the face does for a declaring STREAM_OUTPUT (word 0's flags, STREAM_DEST_MAC_VALID among them, brief kept), so the bridge completes every whole observation of an output and no brief one. The bridge's ACMP owner enters the source port through `completion_source`, whose entry the testbench reports; each entry inside an AECP record or a round is one completion.
  - It runs arm B's four AECP groups as answering-ports builds them, plus `aecp-outputs`:
    - a declared Talker's completed notice to every registration;
    - a Listener Ready for output 0;
    - GET_STREAM_INFO of every output;
    - SET_STREAM_INFO refused NOT_SUPPORTED and ENTITY_LOCKED after its whole observation;
    - behind a held egress, an accepted SET_STREAM_INFO whose notices pass the AECP ring's room, and a GET_STREAM_INFO behind it.
  - The run fails on any `DECLARING` finding: a whole observation's record without exactly one completion, any other record with one, no round with one, or an answer without the completion's values.
  - Three plants: `completion-unexecuted`, `brief-completed`, `completion-dearer`.
- tb/verilator/ctrl_service_budget/record_classes.py: each record counts its completions.
  - The declaring arm's records that ran one are held at their class's statement; the rest are reported.
  - A pass is refused at 1x1/1if or 8x8/1if without a declaring leg that ran an answered GET_STREAM_INFO, an accepted SET_STREAM_INFO and a refused one, each with its completion.
  - Six new self-test controls, plus the arm's own checks; a fixture that clears brief is refused (R872-1-F2).
- sw/firmware/ctrl/test/test_aecp.cpp, aecp_output_mutants.py (R871-F1): AppOutputs pins the whole flags word under Ready, Ready Failed and Asking Failed (the face's flags, REGISTERING_FAILED for Asking Failed alone, never MSRP_FAILURE_VALID).
  - At two interfaces it first registers each output's stream on the other interface and expects neither flag.
  - Two new rows: `output-registering-failed-msrp-failure-valid` and `output-listener-any-interface`.
  - `output-listener-on-interface-zero` and `output-listener-of-output-zero` are now named by the checks that catch them.
- docs/design/SPLIT_CONTROL_MEMORY.md: the arm's records.
- No firmware source, RTL, mailbox contract, CPU-budget bound or stated cost changed.
Validation (at a16899b1 unless named):
- declaring-outputs arm, 1x1/1if: 5 groups, 0 refusals, 0 budget misses (0 of 57 instances), 0 of 839 passes over the share.
  - 6 completions in 6 records of aecp-outputs, 1 in a round of THE RETRY, 19 GET_STREAM_INFOs of outputs, each with its MAAP address and Listener flags.
  - Rows: the declared notice 1.337 ms; behind the held egress the SET's last notice 9.104 ms and the GET 4.068 ms; each of 20 ms.
- declaring-outputs arm, 8x8/1if: 0 refusals, 0 budget misses (0 of 62).
  - 13 completions in 13 records, 1 in a round, 26 answers.
  - 2 of 845 passes over the share, both in aecp-largest-notice, as arm B records there (2.224 to 2.321 ms on round 1's images).
- Plants, each `CONTROL <name> caught` with 0 refusals at both points (on a16899b1's tree):
  - completion-unexecuted: 7 and 14 records with no completion;
  - brief-completed: the map edits' and SET_CONFIGURATION's records ran completions (3 findings at each point);
  - completion-dearer: 7 and 14 held records over record.aecp, for example 49,658 cycles, 525 of 245 us.
- record_classes.py over arm A (every group), arm B, answering-every-port and the declaring leg: RESULT: PASS at both points.
  - Held other 23,330 cycles, 245 of 245 us (1x1/1if, the declaring SET_STREAM_INFO; arm B's 21,409), and 20,707, 220 of 265 (8x8/1if).
  - The same legs without the declaring leg: RESULT: FAIL, its three paths missing by name.
- flip_grade.py --check: PASS at both points, unchanged. run.py --self-test: 0 failures.
- The 17 output rows, each planted alone (the internal review's probe), 17 of 17 caught by their named words at 1x1/2if, the campaign's arm.
  - At 1x1/1if and 8x8/1if, 15 of 17: `output-listener-on-interface-zero` and `output-listener-any-interface` are the fix's own code at one interface.
- test_ctrl_firmware.py --require-rv32 --self-test, 4 shards: PASS (1,806 live invocations; control campaign 825 of 825; AECP campaign 383 caught, the 17 output plants among them; SRP campaigns and pins; 0 escaped). fw_coverage.py --check: PASS, 40 files.
- docs.yml gate steps: every step rc 0 but the RV32 SDK install's verify, which refuses this host's SDK (no provenance receipt), as in round 1. ctrl_boundary.py --require-rv32 --selftest --without verilator: refuses sink_mutants.py and talker_notice.py, the same text as at 0839453f and 502b041c; declaring_outputs.py names no firmware path and is not refused.
- Carried from round 1, the firmware unchanged (git diff 502b041c..a16899b1 -- sw/firmware: test_aecp.cpp, aecp_output_mutants.py): twin and plants, plat_ledger, the memory test, the release image, arm A and the answering-ports, answering-every-port and talker-notices arms.
Acceptance criteria: as round 1 (met), with the completion now graded in a maintained arm at both points (R872-1-F1).
Correction to round 1's REVIEW READY (issuecomment-7015365492), whose risk item said the paced edit's 325 us and the largest legal command's 1,920 us on the measurement-only declaring-face image were placement: that image's fixture cleared `brief`, so its brief checks ran the completion too (R872-1-F2). Those figures are withdrawn, and their excess is not apportioned between placement and execution.
  - The maintained arm keeps brief. The bridge probe gives brief=1 with 0 source calls for a brief read, and 1 call with the source's address for a whole one.
  - On its image, the map edits' and the largest legal command's records each count 0 completions.
Open risks/questions:
- On the declaring arm's image, the records that run no completion are arm B's commands on another placement, reported, not held (R871-S1's second half, the owner's):
  - the paced REMOVE: 30,226 cycles, 320 us at 1x1/1if (arm B 29,422, 310 of 310);
  - the largest legal command: 167,522 cycles, 1,760 us at 8x8/1if (arm B 163,520, 1,720 of 1,720).
  - The held declaring SET_STREAM_INFO is 3 cycles inside 1x1/1if's 245 us.
  - A merged image's placement can therefore refuse where this head passes. Restating the paced edit to 320 us would put 1x1/1if's last queued notice row over 140 ms.
- R871-S2: round 1's per-shape plant receipts (firmware/plants-*.txt, 14 rows) are an intermediate row set; round 2's receipts carry the current 17 at three shapes.
- Unchanged from round 1: firmware-boundary refuses sink_mutants.py and talker_notice.py (unclassified, the composition lane's), the out-of-scope items #943 records, and the GET_TX_STATE REGISTERING_FAILED report for the manager.

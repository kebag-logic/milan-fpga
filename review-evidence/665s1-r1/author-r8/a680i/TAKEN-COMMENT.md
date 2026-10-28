[A680i] TAKEN
Branch: 665-s1-faces (PR #795), on the merge-round head `0052e62e`
Authoritative references: round-8 assignment issuecomment-6461128613 (ruling on R701-7-F1), answering R701-7 (PR #795 issuecomment-6461122749, with its three probe scripts); rulings 6412739248 item 1, 6425357821 and 6421238472 still in force
Interpreted scope:
- F1: the CPU budget harness names the ledgered point `8x8-two-interfaces` for its 8x8 two-interface image and SoC plan, and nowhere else. The product SoC path names none, and `test_ctrl_memory.py` still proves that the default `add_ctrl_memory` refuses the ledgered image. `ctrl_memory.py`'s comment takes the ruling's words. The PR body says what `run.py --self-test` does not cover.
- F2: the harness's `KL_mbx` instance connects every contract 2.3 port the way `milan_soc.CtrlMailbox` does: outputs named, inputs tied idle by name. Arm B is re-anchored to the face-block observation. The README names the firmware head its figures were measured at, and its fixture claims and line citations match the head.
- W1: applied to the PR body.
Validation plan:
- the reviewer's `probe_harness_8x8.py`, `probe_harness_ports.py` and `probe_harness_anchors.py`, unchanged;
- `test_ctrl_memory.py`;
- a real harness build at 1x1/1if and at 8x8/2if, arm A, one group each, run to the measurement and compared with S2's recorded figures;
- the round-7 gate set: the firmware-boundary steps, the firmware self-test (four shards), `fw_coverage.py --check`, `test_builder.py`, the linked images at four points, the harness self-test, the docs gates, the bare-metal scope gate, `behave`, and the four-shard Verilator sweep.
Blockers: none yet. One thing to check first, by the real build: with contract 2.3's commit acknowledgement tied idle (as `CtrlMailbox` ties it), the face block's first commit is never acknowledged. `aecp_face_open` would then fail and the fixture's `main` would return before the loop (`ctrl_aecp_image.c`, `return 6`), so arm A would reach no measurement. If the build confirms this, I will STOP with the evidence.

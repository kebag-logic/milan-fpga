# #894 round 13, item 5: an accepted SET_CONFIGURATION cannot complete late on the product port

The ruling (#894 issuecomment-6888782796, item 5) asks either to stage a late-acknowledged SET_CONFIGURATION's
completion in one group at each point and hold it by the rule, or to show from the product port that it cannot
complete late. This is the second: the chain from the contract to the core, each link a file and line at the head.

1. **The contract bounds the acknowledgement.** Contract 2.3: a commit raises `fw_send_o` and every setting holds
   "until the datapath's acknowledgement `fw_ack_p_i`, within 64 cycles" (`docs/reference/MAILBOX_CONTRACT.md:346`;
   `MBX_FACE_ACK_CYCLES` 0x40, `:1133`).
2. **The product's datapath meets it unconditionally.** The product connects the face block through `KL_mbx_cdc`
   (`sw/litex/milan_soc.py:3154`, `CtrlMailbox` WITH A DATAPATH, the MilanNIC built with `CTRL_SPLIT_P = 1`).
   There the commit's rising edge crosses to the datapath as one pulse (`hdl/milan/mailbox/KL_mbx_cdc.sv:272`), the
   datapath takes every setting on that pulse with no ready or backpressure (`:278`), and the same pulse is the
   acknowledgement's source, crossed back as one pulse (`:274`). Nothing can hold it.
3. **It is measured on the product composition.** `tb/verilator/milan_dp/sim_split.cpp:367-372` composes KL_mbx
   (100 MHz), KL_mbx_cdc and milan_datapath with `CTRL_SPLIT_P = 1` (50 MHz), as the split SoC does. It checks
   "[FACE] the commit is acknowledged within MBX_FACE_ACK_CYCLES" and prints the polls the BUSY bit took: 2 polls
   against 64 (the sweep's `milan_dp` suite, shard 0, at `a47cd3f2` and again at `ed0df35b`, `receipts/sweep/milan_dp-face-lines.txt`).
4. **The firmware outwaits the bound.** `mbx_face_commit` (`sw/firmware/ctrl/mbx/mbx.c:337`) refuses a commit while
   one waits (`:343`, FULL), else writes GO and reads F_STATUS up to `MBX_FACE_ACK_CYCLES` + 1 times, each read a bus
   cycle or more (`:346`), and returns OK once BUSY is clear. Every commit waits for its own acknowledgement inside
   the port, so the next one never finds the block busy, and FULL is unreachable.
5. **So the face never owes an interface after its open.** `publish` (`sw/firmware/ctrl/aecp/aecp_face.c:79-101`)
   marks an interface owed only when it is owed already, when a change waits, when the block is busy, or when the
   commit is not OK (`:97`, `:101`). After `aecp_face_open` published every interface (`:286`), none of these holds,
   so `applied` is true after every change.
6. **So the core never enters the wait.** A change of face state waits, undone, behind IN_PROGRESS only when
   `applied` is false after it (`sw/firmware/ctrl/aecp/aecp.c:489`, `:498`). With every commit acknowledged inside
   the port it is never false, and the completion in `aecp_poll` (`:906-929`) and the owed interface's whole
   republication in `aecp_face_poll` never run.
7. **The measured record already takes the longest wait.** The CPU budget harness acknowledges every commit at
   exactly the contract's bound (`tb/verilator/ctrl_service_budget/split_soc.py:226`, `slowest_ack`), so the
   SET_CONFIGURATION record held by `record_classes.py` includes the slowest commit the contract allows, at both
   points.
8. **The path itself is still tested.** A datapath that broke the contract would make the change wait, and that fault
   path's behaviour is held by `Face.ALateCommitIsOwedAndPublishedAgainWhole`
   (`sw/firmware/ctrl/test/test_aecp.cpp:3944`). `Face.EachSettingIsCommittedBeforeTheResponseThatPromisesIt`
   (`:3770`) holds that SET_CONFIGURATION's commit is taken inside the port, one response, no IN_PROGRESS.

An SoC built with no datapath (the CPU harnesses' own build, `milan_soc.py:3162`) holds the acknowledgement idle, so
there every commit waits as the contract defines. That is a test fixture, not the product port.

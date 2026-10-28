[A680i] STOP
Head: `27c541718f00550dc4fe489c8d170902cb1678cf` (one commit on the merge head `0052e62e`; nothing pushed)

**Why I stopped: two items of the round-8 assignment cannot both hold.**
- F2 (assignment 6461128613): the harness's `KL_mbx` instance takes every contract 2.3 port "as `milan_soc.CtrlMailbox` does: outputs named, inputs tied idle by name".
- Gates (same assignment): "a real harness build at both points (1x1/1if and 8x8/2if, arm A, one group each, to the measurement)".

With the face block's commit acknowledgement held idle, this branch's size fixture never opens AECP, so no group reaches a measurement:
- The fixture commits each interface's face block before AECP opens (`aecp_face_open`, called by `ctrl_app_open_aecp`).
- `KL_mbx` clears a commit only on `fw_ack_p_i` (`KL_mbx.sv:487-496`).
- With that input at 0, `mbx_face_commit` gives up after its bound (`mbx.c:281`), and the interface stays owed.
- `ctrl_app_open_aecp` then returns false, `main` returns 6 (`ctrl_aecp_image.c:132-133`), and the hart parks (`ctrl_split_start.S:28`).

**Evidence (real builds of the harness, arm A, group `aecp`):**
- **At this head, unchanged.**
  - Both points build: `image.log`, the SoC export, Verilator and `make`.
  - 8x8 plans 57.5 RAMB36 with `"ledgered": "8x8-two-interfaces"`; 1x1 plans 37.0 and names none.
  - 0 mailbox ports are unconnected (77 at the merge head).
  - The sampled PC reaches `mbx_face_busy` and `aecp_face_poll`, then parks at 0x5c: 125 ms into the boot at 1x1, 308 ms at 8x8.
  - `wait ready` (an open filter and a first pass) never completes.
  - With the testbench's 60 s limit shortened to 1 s in a scratch copy, `run.py` prints `REFUSED aecp: the simulation did not complete: ['FAIL: simulation exceeded its time limit']`, rc 1.
- **At the merge head `0052e62e`**, where those inputs were simply unconnected, it parks the same way at 125 ms. So the harness has not measured this branch's firmware at any head. The tie-off does not cause this.
- **Probe, outside the tree:** this head, plus a datapath that acknowledges each face commit one bus cycle after `fw_send_o` rises, with every other face input still idle. The `aecp` group then measures every probe: 25 of 25 at 1x1 and 39 of 39 at 8x8, 0 refusals, 0 T_svc misses.

  Against S2's recorded figures, the differences the S1 firmware explains:
  - Each AECP command makes one more mailbox access an interface (+1 at 1x1, +2 at 8x8): the core's `applied` check reads `F_STATUS.BUSY` (`aecp.c:347`).
  - LOCK_ENTITY and its release add 12 accesses an interface, about 0.21 ms at 1x1: the `F_AECP.LOCK_HELD` publication (six setting writes, the commit and its acknowledgement).
  - The first SET_NAME adds 21 accesses at 1x1 and 42 on 8x8 interface 0: its publication on every interface.
  - An idle pass is 218 CPU cycles longer at 1x1.

  Every other difference lies outside AECP's modules and is phase (one phase is one sample). That includes S2's one 8x8 miss, `get_configuration.if0`, which measured 14.82 ms there and 7.68 ms here.

**Decision needed:**
- **(a) Recommended.** The harness's SoC models a datapath that takes every face commit: `fw_ack_p_i` pulses one bus cycle after `fw_send_o` rises, inside the contract's `ack_cycles` (64). Every other face input stays idle by name, so window requests time out, as the fabric-less split SoC sees them. The README states this one difference from `CtrlMailbox` and why. That is the probe above: arm A and arm B then measure this firmware at both points.
- **(b)** Keep every input idle, as the ruling's words say. The harness then measures nothing until the placement switch wires the datapath side, and the README and PR body say so. S2b and S2c inherit no measurement once they sync with `dev-soft-core`.
- **(c)** As (a), but acknowledge at the contract's bound (64 bus cycles), the slowest datapath the contract allows.

**Done at `27c54171`, independent of the decision:**
- F1:
  - `build.py` `LEDGERED_POINTS` names `8x8-two-interfaces` for `(endstation_ax7101_8x8, 2)` only, for the image (`--ledgered-point`) and for the SoC's plan (`split_soc.ledgered_plan`).
  - `ctrl_memory.py` and `SPLIT_CONTROL_MEMORY.md` now say "the product SoC build names none; the measurement harness names it for that point only".
  - `test_ctrl_memory.py`: 0 failures, and the default `add_ctrl_memory` still refuses the ledgered image.
- F2:
  - The 19 face inputs are held idle by name (`split_soc.FACE_IDLE_INPUTS`), refused unless they are exactly the inputs `CtrlMailbox` holds idle. The outputs come from `ctrl_mailbox_face_ports` at the build's interface count.
  - The build refuses any unconnected mailbox port (Verilator PINMISSING). Planted mutant: the face ports removed, and the build exits 1 with `the mailbox instances leave ports unconnected (verilate.log, PINMISSING): [...]`, 77 ports.
  - Arm B is re-anchored: the face's `stream`, `avb` and `counters` ports answer, and so does the fixture's `path`.
  - The README names the firmware its figures were measured at (`e76a755a`, before contract 2.3), states what this head does, and its line citations resolve at the head.
- Self-test: two new checks and mutants (the ledgered point at its point only; every arm and plant applies). 89 checks pass, 64 mutants are caught, 0 escaped.
- W1 is applied in the PR body, which also says what `run.py --self-test` does not cover.
- R701-7's probes, unchanged, at the head:
  - `probe_harness_8x8.py ... endstation_ax7101_8x8 2`: `FIRMWARE-STEP OK`. Its no-override plan is `REFUSED`, which is the default path the planner keeps.
  - `probe_harness_anchors.py`: all four `APPLIES`.
  - `probe_harness_ports.py`: "inputs left unconnected:" none. Its "outputs left unconnected: 58" is a text count: the outputs come in through `**face_ports(...)`, and the build's own check finds 0 unconnected. The probe's regex also misses the last port, `amap_wr_p_i`, which has no trailing comma.

**Gates at `27c54171`:**
- the harness self-test;
- `test_ctrl_memory.py`;
- the docs workflow's 69 commands, 69 of 69, including the bare-metal scope gate;
- `gen_mailbox.py --check` (0 findings);
- `behave` (14 features, 406 scenarios);
- the rtl-fast `firmware-boundary` steps: rc 0.

Not run this round: the firmware self-test shards, `fw_coverage.py`, `test_builder.py`, the four-shard sweep, and the linked images as their own gate. This round changes no firmware, RTL, contract or generated file, and the harness's images at both points are byte-identical to the merge round's. The full round-7 set is owed at the head that answers this decision.

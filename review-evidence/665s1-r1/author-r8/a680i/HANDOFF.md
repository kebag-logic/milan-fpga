STATUS: STOP (round 8, executor [A680i]): head `27c541718f00550dc4fe489c8d170902cb1678cf`; needs a decision on the harness's face commit acknowledgement

# #665 lane S1 ([A680i]): round 8 on PR #795

- Branch `665-s1-faces` (`origin` is `kebag-logic/milan-fpga`), from `dev-soft-core` `e76a755a`. One commit on the merge
  head `0052e62e`: `27c54171` (one-line subject, no body, no trailers). Nothing pushed.
- Assignment: #665 issuecomment-6461128613, answering R701-7 (PR #795 issuecomment-6461122749; its text is in
  `receipts/r701-7-comment.md`). TAKEN: issuecomment-6461207110 (`TAKEN-COMMENT.md`). STOP: issuecomment-6461886441 (`STOP-COMMENT.md`).
- Rulings still in force: 6412739248 item 1, 6425357821, 6421238472.

## Why STOP

Two items of the assignment cannot both hold at this head:
- F2 asks for the harness's `KL_mbx` instance to take every contract 2.3 port "as `milan_soc.CtrlMailbox` does:
  outputs named, inputs tied idle by name".
- The gates ask for "a real harness build at both points ... to the measurement".

The size fixture commits each interface's face block before AECP opens (`aecp_face_open`, called by
`ctrl_app_open_aecp`, `ctrl_app_aecp.c:237`).
- `KL_mbx` clears `fw_busy_r` only on `fw_ack_p_i` (`KL_mbx.sv:487-496`).
- With that input at 0, `mbx_face_commit` (`mbx.c:281`) returns BAD after `MBX_FACE_ACK_CYCLES`, and the interface
  stays owed.
- `aecp_face_open` (`aecp_face.c:278`) then returns false, `main` returns 6 (`ctrl_aecp_image.c:132-133`), and the hart
  parks (`ctrl_split_start.S:28`, `5: j 5b`).

The testbench's `wait ready` needs an open filter and a first pass (`sim_main.cpp:355`), so every group waits until the
60 s simulated limit and is refused.

This happens at the merge head as well, where the face inputs were unconnected (Verilator ties them to 0). The tie-off
by name does not cause it; it makes it explicit. The STOP comment gives options (a) to (c), and recommends (a): model a
datapath that takes every commit.

## Work list

- [x] F1: `build.py` `LEDGERED_POINTS` / `ledgered_point`; `firmware()` passes `--ledgered-point` at 8x8/2if only;
  `split_soc.ledgered_plan` holds `add_ctrl_memory`'s plan to that point
- [x] F1: `ctrl_memory.py` comment and `SPLIT_CONTROL_MEMORY.md` section 3 in the ruling's words; `test_ctrl_memory.py`
  still refuses through the default path (run, PASS)
- [x] F1: `probe_harness_8x8.py` unchanged: `FIRMWARE-STEP OK`; `run.py --point 8x8` gets past `image.log` and the SoC
  export (and Verilator and `make`)
- [x] F1: PR body says what `run.py --self-test` does not cover
- [x] F2: every contract 2.3 port connected as `CtrlMailbox` connects it; the build refuses an unconnected mailbox port
- [x] F2: arm B re-anchored to the face-block observation
- [x] F2: README names the firmware head of its figures; its fixture claims and citations match the head
- [x] F2: `probe_harness_ports.py` and `probe_harness_anchors.py` unchanged
- [x] W1 (R701-7-W1): PR body, "How to validate"
- [ ] Gate "real harness build at both points ... to the measurement": both build, neither reaches a measurement. STOP.
- [ ] The rest of the round-7 gate set (firmware shards, `fw_coverage.py`, `test_builder.py`, linked images, sweep): not
  run, owed at the head that answers the decision (section "Not run")

## Changes (`git diff 0052e62e 27c54171`, 10 files, +200 -49)

| File:line at `27c54171` | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/build.py:134-143` | `LEDGERED_POINTS = {('endstation_ax7101_8x8', 2): '8x8-two-interfaces'}`, `ledgered_point()` | F1: the harness names the ledgered point for that point only |
| `build.py:162-166` | `firmware()` adds `--ledgered-point <name>` when `ledgered_point()` names one | F1: the image step (`image.log`) |
| `build.py:452` | `build()` passes `ledgered_point(shape, n_if)` to `split_soc.build` | F1: the SoC plan |
| `build.py:357-369`, `:383-385` | `MAILBOX_MODULES`, `mailbox_pins_missing()`; `verilate()` raises on any | F2: Verilator's PINMISSING is a warning under `-Wno-fatal`; the build refuses a mailbox port left unconnected |
| `build.py:59-90` | `answering-ports` re-anchored: `b_stream`, `b_avb` and `b_counters` added after `image_face`, and set in `image_face.ports` after `aecp_face_init`; `a_path` answers `*count = 0` | F2: arm B on the face block; the old anchors (`a_stream`, `a_avb`, `a_counters`) are gone at the head |
| `build.py:50`, `:68`, `:90` | `MAILBOX_SPLIT.md:502` -> `:506` | the SHUTDOWN row moved in S1's `MAILBOX_SPLIT.md` |
| `tb/verilator/ctrl_service_budget/split_soc.py:12-24` | docstring: the face block connected as `CtrlMailbox` connects it | F2 |
| `split_soc.py:197` | `**face_ports(contract, n_if)` on the `KL_mbx` instance | F2 |
| `split_soc.py:216-237` | `FACE_IDLE_INPUTS` (19 inputs, idle, by name), `face_ports()`: the outputs from `ctrl_mailbox_face_ports(with_interfaces(contract, n_if))`, the inputs refused unless exactly `CtrlMailbox`'s | F2: "inputs tied idle by name", widths at the build's interface count |
| `split_soc.py:316-334`, `:349-350` | `ledgered_plan()`; `build(..., ledgered=None)` wraps `add_ctrl_memory` | F1 |
| `tb/verilator/ctrl_service_budget/selftest.py:723-751` | `build_checks()`: the ledgered point is named at 8x8/2if only, by a name the planner ledgers; every arm and control plant applies | tests for F1 and F2 (the arm-B break would have been caught at the merge round) |
| `tb/verilator/ctrl_service_budget/selftest_mutants.py:413-418` | two mutants | each new check can fail |
| `tb/verilator/ctrl_service_budget/run.py:189-191` | `--variant` help text | arm B's new meaning |
| `tb/verilator/ctrl_service_budget/README.md` | ledgered point (`:42-44`); what this head does (`:46-52`); arm B (`:76-78`); the test SoC (`:93-102`); the firmware the figures measured (`:195-198`); past/present tense of the fixture claims (`:345`, `:514-519`, `:679-680`); controls at this head (`:667-669`); a limit (`:681`); self-test bullet (`:568`) and mutant rows; citations `aecp.c:66`, `aecp_commands.c:593`, `aecp.c:535-569`, `MAILBOX_SPLIT.md:499-506`/`:649-661`/`:757-762`; one limit added | F2 README; R701-7 citations |
| `scenario.py:275`, `:312`, `:797`, `:843`, `:845`, `:904`; `grade.py:52`, `:461` | `MAILBOX_SPLIT.md` line citations moved to the head's | the same moved tables |
| `sw/litex/ctrl_memory.py:197-203` | "the product SoC build names none ...; the measurement harness names it for that point only" | F1, the ruling's words |
| `docs/design/SPLIT_CONTROL_MEMORY.md:94-95` | the same statement, linking the harness | F1: the doc said "every SoC build is still held to 56" |

## Checks and planted mutants

| Check | Planted mutant | Failing words |
|---|---|---|
| self-test: "the ledgered point is named at 8x8 with two interfaces only, as the planner ledgers it" | `build: the 1x1 point names the ledgered override too` (`LEDGERED_POINTS` gains the 1x1 point) | `MUTANT caught: ... ({'1x1': '8x8-two-interfaces', '8x8': '8x8-two-interfaces'}; ...)` (`receipts/gates/harness-selftest.txt`) |
| self-test: "every labelled arm and control plant applies to the checkout's sources" | `build: arm B anchors the fixture's own observation callbacks (earlier rule)` (the merge head's `a_avb` anchor) | `MUTANT caught: ... (variant answering-ports: an anchor is not unique in ctrl_aecp_image.c: '{ (void)ctx; ... }\nstatic bool a_avb')` |
| build: a mailbox port left unconnected is refused | `probes/plant-pins.diff` (the `**face_ports(...)` dropped), a real build at 1x1 | rc 1 in 13 s: `RuntimeError: the mailbox instances leave ports unconnected (verilate.log, PINMISSING): ['KL_mbx.amap_ans_data_i', ...]`, 77 ports (`receipts/runs/plant-pins-1x1/driver.log`) |
| `face_ports`: the inputs differ from `CtrlMailbox`'s | not planted as a build (it raises before the SoC exists); its comparison is a dict equality on the 19 names | `the face inputs differ from those CtrlMailbox holds idle: [...]` |

## Real harness builds (`receipts/runs/`, generated by `probes/collect_receipts.py`)

| Leg | Tree | Result |
|---|---|---|
| `base-1x1` | merge head `0052e62e`, unchanged | builds; 77 mailbox ports unconnected; parks at 125 ms (`pc-trace.txt`); stopped at 3.7 s simulated |
| `head-1x1` | this head, unchanged | builds; plan 37.0, no ledger; 0 mailbox ports unconnected; `mbx_face_busy` at 124 ms, parked at 125 ms; stopped at 0.83 s |
| `head-8x8` | this head, unchanged | builds; plan 57.5, `"ledgered": "8x8-two-interfaces"`; 0 unconnected; `aecp_face_poll` at 303 ms, parked at 308 ms; stopped at 0.71 s; ELF `654921b6...` = the merge round's 8x8/2if linked image |
| `limit-1x1` | PROBE `probes/probe-limit.diff` (`SIM_LIMIT_S = 1`) | rc 1: `REFUSED aecp: the simulation did not complete: ['FAIL: simulation exceeded its time limit']` |
| `ack-1x1` | PROBE `probes/probe-ack.diff` (each face commit acknowledged one bus cycle after `fw_send_o` rises) | rc 0: 1 group graded, 0 refusals, 0 of 25 instances miss T_svc |
| `ack-8x8` | the same probe | rc 0: 1 group graded, 0 refusals, 0 of 39 instances miss T_svc |
| `plant-pins-1x1` | PLANT `probes/plant-pins.diff` | rc 1 at the Verilator step (above) |

Comparison with S2 (`receipts/compare/aecp-1x1.md`, `aecp-8x8.md`, `passes.md`; S2's final regrade tables). The `aecp`
scripts are the same stimulus: the 1x1 script equals S2's first-round script, and S2's final regrade refuses stale
scripts. The S1 firmware explains these differences:
- One more mailbox access an AECP command, an interface: `applied` reads `F_STATUS.BUSY` (`aecp.c:347`).
- LOCK_ENTITY and unlock: +12 an interface (+0.21 ms at 1x1), the `F_AECP.LOCK_HELD` publication.
- SET_NAME: +21 at 1x1, +42 on 8x8 if0, the persisted change's publication.
- Idle passes +218 cycles at 1x1. `aecp_face` costs about 290k cycles over the run.

The other rows differ by phase, outside AECP's modules (`aecp`, `aecp_nvm` and `memset` agree within 2 %). They include
S2's one 8x8 miss, `get_configuration.if0`, at 14.82 ms against 7.68 ms here.

## Gate table (head `27c541718f00550dc4fe489c8d170902cb1678cf`)

| Gate | Result | Receipt |
|---|---|---|
| harness self-test `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | rc 0: 89 PASS, 64 MUTANT caught, 0 ESCAPED, `self-test: 0 failures` | `gates/harness-selftest.txt` |
| `sw/litex/test_ctrl_memory.py` (LiteX's interpreter) | rc 0, `test_ctrl_memory: 0 failure(s)`; "the SoC build's add_ctrl_memory given the ledgered point's image: refused by ... 'budget'" (run on the working tree before the commit; the commit changed none of its inputs after) | `gates/test-ctrl-memory.txt` |
| docs workflow, 69 commands (`probes/docs_gates.sh`), including `check_em_dash.py --base` over `e76a755a..HEAD`, `gen_toc.py --check`, `check_doc_paths.py`, `check_py_idiom.py`, the bare-metal scope gate | 69 of 69 rc 0 | `gates/docs-gates.txt` |
| `sw/mailbox/gen_mailbox.py --check` | 0 findings | `gates/gen-mailbox-check.txt` |
| `cd tests && behave --no-capture -f plain` | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| rtl-fast `firmware-boundary` steps (`probes/firmware_boundary.sh` via `boundary_unit.sh`, own unit, the pinned archive installed into a new scratch destination) | rc 0, 1,024 s: SDK self-test OK; the pinned archive installed into a new destination and verified; `ctrl_boundary: PASS`, 2,864 compiled sources of 3,094 invocations, 0 findings, 112 boundary, 167 pin and 4 figure controls; tree clean after (the merge round: the same counts) | `gates/firmware-boundary.txt` |
| R701-7 probes, unchanged (sha256 `be4d89ca...`, `166491a1...`, `af8763fd...`, as published) | 8x8: `FIRMWARE-STEP OK`, no-override plan REFUSED (57.5); 1x1 control OK 37.0; anchors: 4 of 4 APPLIES; ports: no input unconnected (58 outputs by text count, see STOP) | `probes/8x8.txt`, `1x1-control.txt`, `anchors.txt`, `ports.txt` |

## Not run, and why

The firmware self-test shards, `fw_coverage.py --check`, `test_builder.py`, the linked images at four points and the
four-shard sweep were not run. This round changes no firmware, RTL, contract, generated or `configs/` file
(`git diff --name-only 0052e62e 27c54171 -- sw/mailbox hdl syn configs sw/firmware` is empty). The harness's images
at both points are byte-identical to the merge round's linked images (`fe939fff...`, `654921b6...`), and the merge
round's receipts for these gates stand. The decision will change the harness again, so the full round-7 set is owed at
that head.

## Process notes

- The CPUs were all booked (`cpu_ranges.py pick`: no free range). Every run used this session's own CPUs, 48-55, in its
  own transient unit (`probes/unit.sh`, MemoryMax 12G or less; peak 1.5 GB). No Vivado.
- The three head and merge-head simulations were stopped once the hart was parked. `wait ready` cannot complete, and the
  60 s limit is about ten hours of wall time here. Each driver log says so on its last line.
- Scratch worktrees (`head0`, `head1`, `probe-ack`, `probe-limit`, `plant-pins`), each with submodule worktrees at the
  pins, are under `$VALIDATION_STORAGE/scratch/665s1-a680i-work/`, outside the tree. So are the builds and the boundary job's SDK.
- `probe_harness_ports.py` counts only the ports spelled in the text between the `KL_mbx` instance and
  `FlashBoundary`. Its regex misses the last declared port, `amap_wr_p_i`, which has no trailing comma: 113 ports, not 112.

## Receipts

`receipts/INDEX.md` is generated by `probes/collect_receipts.py` from the files present, with host paths replaced by
placeholders. One file over 200 KB, `runs/ack-8x8/results/aecp.log`, is recorded in `receipts/large-files.txt` by size
and sha256 and not copied. Scripts under `probes/`: `env.sh`, `leg.sh`, `unit.sh`, `pc_trace.py`, `compare_aecp.py`,
`collect_receipts.py`, `docs_gates.sh`, `run_gate.sh`, `firmware_boundary.sh`, `boundary_unit.sh`, `behave_unit.sh`,
and the three probe diffs.

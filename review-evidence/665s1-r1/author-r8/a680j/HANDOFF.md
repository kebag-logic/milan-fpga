STATUS: REVIEW READY (round 8 continuation, executor [A680j]): head `bdad673a7824d84c922d771ff5950e8f69083c27`; every gate rc 0; two findings open for a decision

# #665 lane S1 ([A680j]): round 8 on PR #795, ruling 6461910715 option (c)

- Branch `665-s1-faces` (`origin` is `kebag-logic/milan-fpga`), from `dev-soft-core` `e76a755a`. Three commits on
  [A680i]'s `27c54171` (one-line subjects, no body, no trailers), nothing pushed:
  - `c2c5abd2` the bound acknowledgement and the build's check of it, README;
  - `0eda061a` the idiom fix (the bench's stimulus annotated and documented) and the README's statements on this head;
  - `bdad673a` README only: a sooner acknowledgement measures the same on this core; the as-built address is the 1x1 image's.
- REVIEW READY: issuecomment-6463943143 (`REVIEW-READY-COMMENT.md`).
- Ruling: #665 issuecomment-6461910715 (option (c) of [A680i]'s STOP 6461886441). Round-8 assignment 6461128613 and
  rulings 6412739248 item 1, 6425357821 and 6421238472 still in force. TAKEN: issuecomment-6461920520.

## Work list

- [x] 1. The SoC pulses `fw_ack_p_i` at the contract bound, `FACE_ACK_CYCLES` (64) bus cycles after each interface's
  `fw_send_o` rises; the bound is the generated constant, not a literal. Every other face input stays idle by name.
- [x] 2. README states this one difference from `CtrlMailbox` and why; the PR body too.
- [x] 3. Real harness builds at both points, arm A (`aecp`) and arm B (`aecp-fanout`), one group each, to the measurement;
  compared with S2's recorded figures, differences S1's firmware explains stated (below).
- [x] 4. Everything else done at `27c54171` kept (the diff touches `split_soc.py` and `README.md` only).
- [x] Round-8 gates (table below), all rc 0

## Changes (`git diff 27c54171 bdad673a`, 2 files, +119 -13)

| File:line at `bdad673a` | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/split_soc.py:192-193` | `face = face_ports(...)`; `face['i_fw_ack_p_i'] = self.slowest_ack(face['o_fw_send_o'], n_if, contract)`; the instance takes `**face` | ruling item 1: the one face input not held idle |
| `split_soc.py:207-218` | `StimulusMailbox.slowest_ack`: per interface a counter `waited` (cleared while `fw_send_o` is low, saturating at the bound) and `ack = send & (waited == bound)`; `bound = face_ack_cycles(contract)` inside it | the slowest datapath the contract allows; the bound is derived where it is used, so the check below tests what is instantiated |
| `split_soc.py:262-266` | `face_ack_cycles(contract)`: `FACE_ACK_CYCLES` from `mailbox_model.constants(contract)` | "take the bound from the contract (the generated constant), not a literal" |
| `split_soc.py:269-279` | `_CommitBench`: `KL_mbx`'s commit rule (`face_commit`, `KL_mbx.sv:485-496`) around `slowest_ack` | the check's bench |
| `split_soc.py:282-327` | `ack_deviations(contract)`: the bound against the firmware header's `MBX_FACE_ACK_CYCLES`; a migen simulation with three back-to-back commits on interface 0 and one overlapping on interface 1; each commit must get exactly one pulse at rise + bound and `fw_send_o` must fall the next cycle | a check that can fail for the defect (planted below) |
| `split_soc.py:427-429` | `build()` refuses before the SoC exists: `the commit acknowledgement is not at the contract bound: [...]` | the real build carries the check (the self-test is portable and has no migen) |
| `split_soc.py:23-28`, `:236-239`, `:39` | docstring and `FACE_IDLE_INPUTS` comment state the exception; `Iterator` import | docs; `check_py_idiom` (the nested generator must be annotated and documented) |
| `tb/verilator/ctrl_service_budget/README.md:46-52` | "The commit acknowledgement is at the contract's bound": why the harness differs from `CtrlMailbox` in that one input | ruling item 2 |
| `README.md:102-108` | the test SoC: the acknowledgement's timing, the constant, the firmware's wait, the build's check | ruling item 2 |
| `README.md:205-206` | Results: at this head the image boots and the groups run; the section's figures are not re-measured | was "no group measures", false now |
| `README.md:545-546` | defect 1 (#791): cause 1 was `e76a755a`'s; at this head the 1x1 image's `.data` copy load (0x197b0, bit 15 set) faults first, cause 5 | observed (below) |
| `README.md:677-681` | controls at this head: `slow-adp-rx` caught (24.614 ms); `slow-adp-shutdown` not run; `as-built` ESCAPES (cause 5), also at the merge head; rule unchanged | was "cannot be caught" and "faults at aecp_image_load", both false |
| `README.md:693-696` | Limits: the datapath idle except the acknowledgement; a sooner one measures the same on this core | true statement of the model |

## Checks and planted mutants

| Check | Planted mutant | Failing words (real 1x1 build, `receipts/runs/<leg>/driver.log`) |
|---|---|---|
| `split_soc.ack_deviations` in `build()`: each commit acknowledged by one pulse at rise + `FACE_ACK_CYCLES` | `probes/plant-ack-early.diff`: `waited == bound - 1` (one cycle early) | rc 1 in 5 s: `RuntimeError: the commit acknowledgement is not at the contract bound: ['interface 0: fw_send_o rises at [3, 69, 135], fw_ack_p_i at [66, 132, 198], falls at [67, 133, 199], bound 64', 'interface 1: fw_send_o rises at [34], fw_ack_p_i at [97], falls at [98], bound 64']` (`plant-ack-early-1x1`) |
| the same | `probes/plant-ack-probe.diff`: `bound = 1` (the one-cycle datapath of [A680i]'s probe) | rc 1 in 6 s: `... 'interface 0: fw_send_o rises at [3, 7, 11], fw_ack_p_i at [4, 8, 12], falls at [5, 9, 13], bound 64', ...` (`plant-ack-probe-1x1`) |
| the same: the bound against the firmware's `MBX_FACE_ACK_CYCLES` | `face_ack_cycles` patched to return 1 (in-process, on the working tree before the first commit) | `['the bound is 1, the firmware waits 64']` |

Not caught by this check: a call site that bypasses `slowest_ack` (the input tied to 0). That build parks the hart as at
`27c54171`, and the run is refused at the testbench's 60 s limit ([A680i]'s `limit-1x1` receipt shows the words).

## Real harness builds at `0eda061a` (`receipts/runs/`; `bdad673a` changes only the README)

| Leg | Arm, group | Result |
|---|---|---|
| `A1` | 1x1/1if, A, `aecp` | rc 0, 193 s: 25 of 25 measured, 0 refusals, 0 T_svc misses |
| `A8` | 8x8/2if, A, `aecp` | rc 0, 363 s: 39 of 39, 0 refusals, 0 misses |
| `B1` | 1x1/1if, B, `aecp-fanout` | rc 0, 215 s: 14 measured, 4 T_svc misses (S2: 3) |
| `B8` | 8x8/2if, B, `aecp-fanout` | rc 0, 470 s: 22 of 22 miss T_svc, 4 over the 24 ms ceiling (S2: 22 and 3) |
| `AF1`, `AF8` | A, `aecp-fanout` (beyond the ruling, to see whether the formal arm gains a miss) | 1 of 9 misses (`set_name`, as S2); 13 of 13 at 8x8 (as S2), none over the ceiling |
| `C-slow` | 1x1, `slow-adp-rx` control | caught: `control.discover.if0` 24.614 ms (S2: 24.614) |
| `C-asbuilt`, `C-asbuilt-merge` | 1x1, `as-built` control, this head and the merge head `0052e62e` | ESCAPED at both, rc 1: `TRAP 166 0 5 00000020` (cause 5) where the control names cause 1 (S2: `TRAP 330592 0 1 00006880`) |
| `probe-ack256-1x1`, `probe-ack1024-1x1` | PROBE, `aecp`, acknowledged later than the contract allows (`probes/probe-ack-*.diff`) | one more F_STATUS read per commit at 256 (+1 access, +170 CPU cycles on lock and unlock, +2 on set_name), three at 1024 |

Comparisons (`receipts/compare/`, generated by `probes/compare_all.sh`):
- **Arm A against the one-cycle probe of `27c54171`: identical**, row for row and cycle for cycle, at both points (the 8x8
  `table.md` has the same sha256). The firmware's first F_STATUS read after a commit comes more than 64 bus cycles
  after it, so the acknowledgement at the bound is already in when the first read samples. The late probes show the
  measurement does see the acknowledgement: one more read per commit at 256 bus cycles.
- **Arm A against S2** (the final regrade, `665s2-a681e head-regrade/A1`, `A8`): [A680i]'s analysis stands unchanged, since
  the figures are the probe's:
  - +1 access per AECP command per interface (+1 at 1x1, +2 at 8x8): the core's `applied` check reads `F_STATUS.BUSY` (`aecp.c:347`);
  - LOCK_ENTITY and unlock +12 per interface (+0.21 ms at 1x1): the `F_AECP.LOCK_HELD` publication;
  - SET_NAME +21 at 1x1, +42 on 8x8 if0: the persisted change's publication on every interface;
  - the rest (-0.5 ms, -6 accesses on nine 1x1 rows; the 8x8 rows) is phase. That includes S2's one 8x8 miss,
    `get_configuration.if0`, which measured 14.822 ms there and 7.675 ms here.
- **Arm B against S2**:
  - **SET_CONFIGURATION** (`aecp_face.c` `publish(..., every)`, from `changed` on `AECP_CHANGE_CONFIGURATION`):
    - the face writes every stream entry of the configuration on every interface;
    - each entry is looked up through `current()`, which is `aecp_find`, a linear search over the model's descriptors;
    - +131,573 CPU cycles in `aecp_commands` (where `aecp_find` lives; the PC samples sit in it for 3 ms) and +19 accesses at 1x1: 9.233 -> 11.660 ms, **fits -> T_svc miss**;
    - +439,826 CPU cycles and +80 accesses at 8x8 if0: 19.788 -> 26.980 ms, **T_svc miss -> over the 24 ms ceiling**.
  - LOCK/UNLOCK +12, IDENTIFY +12, SET_CLOCK_SOURCE +19 accesses at 1x1, +0.18 to +0.72 ms: the settings publication.
  - SET_NAME +21 and SET_STREAM_INFO +17: the publication.
  - The +1 rows: the `applied` read.
  - At 8x8 the rest is phase: `add_audio_mappings_output.if1` 15.0 -> 31.4 ms with +74k pass cycles, and
    `set_stream_info.if1` 32.8 -> 19.8 ms.
- Arm A's fan-out has no SET_CONFIGURATION row, so the formal arm gains no miss.

## Gate table (head `bdad673a7824d84c922d771ff5950e8f69083c27`; each receipt's `.head` or first line names it)

| Gate | Result | Receipt (`receipts/`) |
|---|---|---|
| harness self-test `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | rc 0: 89 PASS, 64 MUTANT caught, 0 ESCAPED, `self-test: 0 failures` | `gates/harness-selftest.txt` |
| real harness builds, both points, arm A (`aecp`) and arm B (`aecp-fanout`), to the measurement (at `0eda061a`; `bdad673a` changes only the README) | rc 0 each; above | `runs/A1`, `A8`, `B1`, `B8` |
| the build's acknowledgement check, two planted mutants (real builds) | each refused, rc 1, with the deviation | `runs/plant-ack-*` |
| R701-7's three probes, unchanged (sha256 `be4d89ca...`, `166491a1...`, `af8763fd...`) | 8x8 `FIRMWARE-STEP OK`, no-override plan REFUSED (57.5); 1x1 control OK (37.0); anchors 4 of 4 APPLIES; ports: no input unconnected by text (58 outputs come in through `**face`; the build's PINMISSING check finds 0) | `probes/` |
| `sw/litex/test_ctrl_memory.py` (LiteX's interpreter) | rc 0, 0 failures; the SoC build's default `add_ctrl_memory` refuses the ledgered image | `gates/test-ctrl-memory.txt` |
| `sw/mailbox/gen_mailbox.py --check` | rc 0, 0 findings | `gates/gen-mailbox-check.txt` |
| docs workflow, 69 commands (`probes/docs_gates.sh`), with `check_em_dash.py --base`, `check_py_idiom.py` and the bare-metal scope gate (`check_baremetal_only.py --check`, `--selftest`) | 69 of 69 rc 0 (the first run, at `c2c5abd2`'s tree, failed `check_py_idiom.py` on the bench's nested generator; fixed in `0eda061a`) | `gates/docs-gates.txt` |
| the docs workflow's CI self-tests (`probes/docs_ci_selftests.sh`, 16) | 16 of 16 rc 0 (the 515,180 B log is recorded by size and sha256 in `gates/docs-ci-selftests-large.txt`, not copied) | `gates/docs-ci-selftests-summary.txt` |
| `cd tests && behave --no-capture -f plain` | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| rtl-fast `firmware-boundary` steps (`probes/boundary_unit.sh`: SDK self-test, the pinned archive into a new destination and verified, `ctrl_boundary.py --require-rv32 --selftest --without verilator`) | rc 0, 1,094 s: `ctrl_boundary: PASS`, 2,864 compiled sources of 3,094 invocations (as the merge round); tree clean after | `gates/firmware-boundary.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (pinned Verilator 5.050) | rc 0, 728 s, PASS: 775 compiled sources of 885 invocations (as the merge round) | `gates/ctrl-boundary-only-verilator.txt` |
| `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | rc 0, 108 s: OK across 5 shapes, 435 tests | `gates/test-ctrl-nvm.txt` |
| `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`, four units | rc 0 each (409, 1,256, 593, 868 s); `[ok]` plants 61, 528, 137 and 280, the merge round's; 0 escaped (also rc 0 at `0eda061a`, receipts moved to scratch `pre/at-0eda061a`) | `fw/shard-*.txt` |
| `fw_coverage.py --check --jobs 4` | rc 0, 290 s: 100 % lines and branches over every file; `aecp.c` 417/417 360/360, `aecp_commands.c` 450/450 374/374, `aecp_face.c` 172/172 152/152, `ctrl_app_aecp.c` 164/164 124/124 | `gates/fw-coverage-check.txt` |
| `sw/builder/test_builder.py --require-rv32` (without `MILAN_RV32_CC`) | rc 0, 1,777 s: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11 needs a local Arty build report, as before) | `gates/test-builder.txt` |
| linked images, four points (`probes/image_points.sh ... ledgered`, the `-fno-stack-protector` runtime) | rc 0: 37.0, 40.5, 50.5 within 56; 8x8/2if 57.5 with `--ledgered-point`, refused without (rc 2); the override refused on the other three (rc 2). The four ELFs are byte-identical to the merge round's (`fe939fff`, `18c5055b`, `d92a7f96`, `654921b6`), and the harness's 1x1 and 8x8 images equal them | `images/` |
| four-shard Verilator sweep (`native-shards.py`, pinned Verilator 5.050 and sv2v 0.0.12, CPUs 112-115, 116-119, 120-123, 124-127) | rc 0 each (4,740, 3,990, 5,339, 3,741 s): 15, 17, 16 and 16 suites pass (64 of 64), 250,913 + 1,536,446 + 380,086 + 23,679 = 2,191,124 checks, 0 in-suite failures, 0 timed out; declared skips only `tsn_fuzz`'s two field campaigns (tsn-gen absent). Suites and checks equal the merge round's | `sweep/sweep-bdad673a/` (files over 200 KB in `sweep/large-files.txt`) |

## Open questions for the manager

1. **`as-built` control escapes** at this head and at the merge head `0052e62e`. Neither [A680h] nor [A680i] ran it.
   The 1x1 image's `.data` load image (0x197b0, bit 15 set) is copied by the start code first (`lw` at 0x24), so the
   generator's decode defect (#791) surfaces as a load access fault, cause 5, before any fetch above 0x8000. The control
   names cause 1 (`run.py:262-264`). The rule is not changed here (that would choose an interpretation privately):
   (a) widen the control to an access fault, cause 1 or 5, or (b) keep cause 1 and move the fixture's first rom access
   above 0x8000 to be a fetch.
2. **SET_CONFIGURATION's every-entry publication** costs about 2.6 ms at 1x1 and 8.8 ms at 8x8 in `aecp_find`, and makes
   arm B's 1x1 row miss T_svc and its 8x8 row exceed the ceiling. Arm A does not run that command. A follow-up issue
   for the firmware (look each entry up once, not by a linear search per entry) is the manager's to file.

## Process notes

- CPUs: `cpu_ranges.py pick` found none free until 112-127 appeared; harness legs and gates ran on this session's CPUs
  80-95 in their own units (`probes/unit.sh`, MemoryMax 4-8 G; peak well under 2 GB); the sweep on 112-127. No Vivado.
- A first sweep at `0eda061a` was stopped after a minute for the README fix (`bdad673a`) and restarted;
  its directory was moved aside, not deleted.
- Scratch: `$VALIDATION_STORAGE/scratch/665s1-a680j-work/` (worktrees `plant` and `probe` with submodule worktrees at the pins,
  builds, logs, earlier legs under `pre/`). Sweep clones `$LANES/665s1-a680j-shard{0..3}`.

## Receipts

`receipts/INDEX.md` is generated by `probes/collect_receipts.py` from the files present, with host paths replaced by
placeholders. Files over 200 KB are recorded by sha256 and size in `receipts/large-files.txt`,
`receipts/sweep/large-files.txt` and `receipts/gates/docs-ci-selftests-large.txt`, and not copied. Scripts under
`probes/`: `env.sh`, `leg.sh`, `unit.sh`, `gate_unit.sh`, `run_gate.sh`, `controls.sh`, `plants.sh`,
`controls_plants.sh`, `probes_late.sh`, `compare_rows.py`, `compare_aecp.py`, `module_diff.py`, `compare_all.sh`,
`pc_trace.py`, `collect_receipts.py`, `docs_gates.sh`, `docs_unit.sh`, `docs_ci_selftests.sh`, `firmware_boundary.sh`,
`boundary_unit.sh`, `behave_unit.sh`, `image_points.sh`, and the diffs `plant-ack-early.diff`, `plant-ack-probe.diff`,
`probe-ack-256.diff`, `probe-ack-1024.diff`.

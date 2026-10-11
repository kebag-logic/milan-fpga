[A592] REVIEW READY (round 3)
Commit: `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08` on `671-read-fault`. This is a local branch, not pushed under the lane rules. The round started at `9112a0df`, and five new commits answer [R602-2](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6103023016) and [R603-2](https://github.com/kebag-logic/milan-fpga/pull/715#issuecomment-6102963708) per [the round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6103025987). No rebase or amend.
Changed:
- Item 1, R603-2-F1 and R602-2-F1: the writer restart (re-attach) path is now under the gate.
  - The host suite has a CPU-only restart, `--restart`. It returns every writer static to its initial value and runs `nvm_boot()` again, with the fabric kept at load pending 0, load accepted 1. It is `run_cases.host_restart()`, moved verbatim to `sw/firmware/nvm_hosttest/writer_restart.py`, which the co-simulation now imports. The generated C and the statics list are identical.
  - A fault armed after `--boot` counts from that read, so it aims at the restart's reads.
  - Check 13 walks 26 restart cases per shape first (472 cases per shape in all):
    - the valid slot faulted for the whole restart at sequences 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF, and once on a record-area byte;
    - one faulty read at each of the restart's first four reads;
    - both slots valid (0x5A5A5, and the wrap), with the newer faulted for the whole restart or on its three re-stage reads.
  - A restart that leaves a slot unread must hold:
    - after the restart, no heartbeat, erase, program, START or acknowledgement;
    - the state ends `backed=0 stale=1 dirty=1`;
    - the line says "re-attached and HELD", and the window is not reloaded;
    - the clean reboot restores every saved record, then recovers through a change and another reboot.
    - One faulty read must not hold, and the change must commit and survive.
  - New control `r_reattach_goes_live` is R603-2's `p_reattach_goes_live` text, byte-identical. It is caught on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8` by "the restart left a slot unread, yet the writer re-attached live": 18 named findings on each, all restart cases, none cold. Its other findings are the loss:
    - B valid: "was lost on the clean reboot";
    - A valid: the writer erases A and "163 other saved record(s) did not survive" (8x8).
  - Checks 1 to 14 on that plant give 41 findings per shape, so R602-2's `run_probe.sh` gate run is red on it. Every R602-2 and R603-2 plant text, and `probe_reattach.py`'s anchors, still occur exactly once (parsed, not executed).
- Item 2:
  - R603-2-S1: every whole-boot fault asserts its exact read count, 6 on a cold boot and 5 on a restart. New control `r_judge_four_tries` (R603-2's text) is caught by "want exactly" on the three shapes, 40 named findings each. The 26 cold whole-boot cases catch it on their own.
  - R603-2-S2: a held re-attach prints "re-attached and HELD" (`milan_baremetal.c:1699-1701`), and this is graded.
  - R602-2-S1: `BAREMETAL_FIRMWARE.md` states that a slot that never reads cleanly holds the writer on every boot, with `milan_nvm wipe` as the only recovery.
- Item 3, residue, exact texts: R603-2-R1 (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:725-729`) and R602-2-R1 (`:1654`).
- The firmware changed (a console line only), so capture was re-measured at `5f174859`, all six arms. All 96 captures are cycle-identical to round 2. The 8x8 contract maximum is 13.86328 ms against 24.5 ms (margin 10.63672 ms, 3.5345x); 1x1 is 3.96548 ms.
- Firmware size with the pinned SDK (`riscv32-linux` GCC 14.3.0): text 17,297 B, +56 B this round and +1,768 B over the base; bss +12 B.
- The prefill read (#717) is out of scope and untouched.
Validation (rc 0 each; CPython 3.12.3; pinned Verilator 5.050 for the suites; at `fc0c517c` unless noted, and nothing a row reads changed after the head it ran at):
- `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`: "OK across 5 shape(s), and every planted defect reddened", 40 controls; 202 s here, 235 s with `--jobs 4`.
- `make -C tb/verilator/nvm_cosim run`: "465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed" (at `1d517428`).
- `python3 sw/builder/test_builder.py --require-elaboration --require-rv32`, product venv: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11) (at `4886f231`).
- `python3 scripts/check_nvm_capture.py`: PASS; its four `--mutation` arms exit 1.
- Step replicas:
  - docs.yml 81/81, which includes `test_builder.py --require-rv32` ("ALL GATES PASS EXCEPT 1 NOT RUN"), the capture gate and the writer gate;
  - rtl-fast firmware-unit 7/7, with the A/B power-loss store gate "OK across 5 shape(s), 435 tests" (at `4886f231`);
  - lint/BDD 5/5.
- `make -C tb/verilator/fw_service_budget`; the record-space gate with `--self-test`; the C and Python idiom and hygiene ratchets (`test_nvm_firmware.py` is 998 lines, inside the module ratchet).
- Full-count runs of all eleven #671 controls on the three shapes, split into restart and cold-boot cases, are in the handoff.
- The act replica was not run: this round's commits are not pushed, and the runner checks out the remote PR head (`9112a0df`).
Acceptance criteria:
1. Met in the firmware host tests, now on both boot paths, the cold boot and the writer restart. The cases cover both orientations, the sequence boundaries, header, sequence and record-area faults, and both slots valid across the wrap. Every case runs a change, its commit and a clean reboot. The processor writer carries no generation, so its half does not apply.
2. Met on both paths. `restart_at_zero` removes the hold in `nvm_go_live()` and fails on both. `r_reattach_goes_live` removes it on the re-attach path alone and fails by name on three shapes. With the other nine controls, check 13 can fail for every mechanism the fix depends on.
3. Met. The A/B write path is unchanged; `nvm_cosim` and the Mark II power-cut suite pass.
"Closes #671" stays in the PR body.
Open risks/questions:
- The detection limit is unchanged and stated: the same wrong bytes twice, all `0xFF` twice, and an address fault on a judgement read.
- The restart model is the co-simulation's. It resets the writer's statics only, so the boot code's memory initialisation, the window memory and the bus fabric stay assumed (obligation O4), as for W1 to W4.
- The worst-case boot (about 17.1 s at 8x8) is still an estimate. A restart opens at most twelve slot reads.
- `--self-test` takes 235 s here at four jobs against the builder bank's 600 s timeout; the hosted time is unknown until it runs.
- dev moved to `ac2c5e77`. #710 changes `sw/litex/milan_soc.py`. The trial merge is clean and no file overlaps. The capture receipt binds the firmware, census and harness, not the SoC source, so the capture time on a merge candidate is not measured here.

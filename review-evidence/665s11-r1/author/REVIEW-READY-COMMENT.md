[A761] REVIEW READY
Commit: b29f94d7aa1d73c4d1eef705a42d9a3a34fc4702 (branch `665-s11-aecp-reboot`, six commits on `dev-soft-core` 1d6bf5556a; not pushed)

Changed:
- Reset port: the split tied the REBOOT request to 0. One CSR bit (`ctrl_reboot_req`, `milan_soc.CtrlReboot`) is crossed by a `MultiReg` onto a new `milan_datapath` input `i_reboot_req`, which drives `reboot_ctrl.reboot_req_i` in the split. `KL_reboot_ctrl` is unchanged and there is no `mailbox.yaml` change. The split census holds the net to that port, with two plants.
- AECP owner: REBOOT (0x002A) is answered as IEEE 1722.1-2021 7.4.43 states. It answers BAD_ARGUMENTS short of Figure 7-68, NOT_SUPPORTED for a type other than ENTITY, NO_SUCH_DESCRIPTOR for another ENTITY index, and ENTITY_LOCKED under another controller's lock. Otherwise it answers SUCCESS and notifies the other registered controllers. No command is taken after it. Without a reset port it stays NOT_IMPLEMENTED.
- Platform: once the response and its notifications have left the mailbox, ADP shuts down (ENTITY_DEPARTING, Milan v1.2 5.6.3.3). Once ADP's ring has drained, the platform writes the port. From then on it services the saved-state store and F_NVM alone.
- Tests: 3 AECP core tests and 11 planted defects; platform tests B11 to B18 and 10 planted defects; a new CPU simulation, `tb/verilator/ctrl_reboot`, with 4 planted images and 5 grader controls.
- Docs: `REBOOT_RESET.md` section 8, `MAILBOX_SPLIT.md`, `CLOCK_DOMAINS.md`, the CDC census diagram, the integrator tables and the memory ledger.

Validation (at the commit, each on a fresh clean clone):
- `rtl-fast`, `elaborate` and `rtl`, every `run:` step of every job a pull_request to `dev-soft-core` triggers: 88 ran with rc 0, 167 not run with a stated reason, 0 bad. This includes `rtl-fast` (the verdict job), `ctrl_boundary.py` PASS, all 4 `yosys-shards`, `gate_19` with 8 of 8 LiteX simulations, and the publication census: 6 shapes, 246 checks, 0 failures, 0 of 164 self-test arms failed, REBOOT plants refused.
- `docs.yml`: 64 ran with rc 0, 31 not run with a stated reason, 0 bad.
- Full Verilator sweep as four native shards: 65 of 65 suites, 2,192,899 checks, 0 in-suite failures. The suite-cancellation preflight passed on each shard.
- `test_ctrl_firmware.py --require-rv32 --self-test`: PASS, 580 of 580 control mutants caught.
- `fw_coverage.py --check`: PASS (35 files).
- Mutant drivers: `aecp_mutants.py` 150 of 150; SRP campaign PASS; `test_ctrl_nvm.py --require-rv32 --self-test`: 109 of 109 planted defects reddened.
- `tb/verilator/ctrl_service_budget/run.py` at 1x1/1if and 8x8/2if with `--record-budget-findings`, and its self-test: rc 0, 0 refusals.
- `test_builder.py --require-rv32`: all gates pass except gate 11's calibration arm, which needs a Vivado place report this host does not have.
- `cd tests && behave`: 508 scenarios passed.
- `git diff --check` against the merge base: clean.
- `python3 -B tb/verilator/ctrl_reboot/run.py --build-dir <dir> --self-test`: `ctrl_reboot: PASS (0 finding(s))`, 9 of 9 plants and controls caught.
- Not run: the full mailbox RTL mutant set (`make -C tb/verilator/mbx mutants`). The mailbox RTL is unchanged here, and the sweep's mbx suite ran its quick set, 7 of 7 caught.

Acceptance criteria:
1. Partly met. In the CPU simulation the #396 grader `check_release_state_restored` passes after the reset over 6 items and the binding: stream format, presentation time offset, channel mappings, clock source, entity names and object name, each set away from its default first. The first ENTITY_AVAILABLE comes 4,590.218 ms after the REBOOT, inside the 20,000 ms valid time. The configuration and the sampling rate cannot leave their defaults at the shipping shape (one configuration, one 48 kHz rate). They read back unchanged and are reported NOT RUN, not graded.
2. Met. The command arrives at 0; SUCCESS leaves at 2.166 ms, the notification at 2.309 ms, ENTITY_DEPARTING at 3.799 ms, and the reset port fires at 4.457 ms. The plant `reset-before-the-response` and the defects `plat-reboot-before-the-response` and `reboot-due-before-its-frames-complete` fail.
3. Met. The plant `request-ignored` fails ("the reset port never fired"), and so do `plat-reboot-ignored` and `reboot-never-accepted`.
4. Met. The REBOOT arrives 62 bus cycles after a journal write's erase and 14 page programs follow. The drain ends durable and every item reads back (completed). The cut's replay reads the saved snapshot whole (abandoned). The plant `write-torn` and the defect `plat-reboot-stops-the-store` fail.
5. Met. STREAM_INPUT and MEMORY_OBJECT get NOT_SUPPORTED, ENTITY index 1 gets NO_SUCH_DESCRIPTOR, and a short command gets BAD_ARGUMENTS. None of them notifies anyone or resets anything. Covered by `Core.RebootRefusalsLeaveTheEntityInService`, B13 and the plant `any-descriptor-type`.

Measurements:
- Request to reset: 222,853 CPU cycles (445,707 bus cycles, 4.457 ms) from the command's last byte to the port. After that, `KL_reboot_ctrl`'s stated bound applies; here the drain for the write in progress took 582.094 ms.
- Linked size: +868 B ROM at every point and +48 B (1x1) or +32 B (8x8) SRAM. No point's RAMB36 plan moves; 8x8/2if stays at 59.0 with 125,916 of 126,976 B of ROM.

Open risks/questions:
1. Item 1 is short of the configuration and the sampling rate, as above, so the PR body relates to #871 and does not close it.
2. S2's harness against the base: at 1x1/1if the same 13 of 81 paths are over T_svc. At 8x8/2if 29 of 129 are over at the head and 31 at the base. `acmp.probe_tx.if1` is newly over (5.416 ms at the base, 13.602 ms at the head), and three paths fall under it. These misses are recorded, not graded; the loop's budget is S2b's (#810).
3. The CPU simulation builds no datapath, so "on the wire" means the mailbox's transmit face. The PHY hold is simulated for 50 of its 3,500 ms, and the IPROG word and configuration load are not modelled. The bench cycles belong to S12.

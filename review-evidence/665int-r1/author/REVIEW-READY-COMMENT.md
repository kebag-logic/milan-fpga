[A582] REVIEW READY
Commit: 25bbe4d956e79de979783d7e4706a5581c0742a7
Branch: `665-int-split` -> `dev`, base `7c1b52be`, not pushed (no PR yet). PR 1 of 2 per ruling 6088423771.

Changed:
- Contract 2.2 (additive): a publication block in the mailbox window, `0x800 + 0x200 * i`: `DA_GATE`, `LICENCE`, `IDLE_SLOPE`, `SR_DOMAIN`, and per sink `SID_LO`, `SID_HI`, `BINDING{BOUND, SID_VALID}`. Generated into `KL_mbx` (nine `pub_*_o` ports), the package, the C header and the contract reference. Holes and absent interfaces read 0 and take no write; partial strobes are refused into `BUS_ERR`.
- Writers, each before the response that promises the value: ACMP (binding and settled stream_id, before any frame of the entry), MAAP (`DA_GATE`, before the allocation is reported), SRP (`LICENCE` before each licence report and revocation; `IDLE_SLOPE` and `SR_DOMAIN` before the declarations they admit or carry). ADP owns no consumed value, so it has no writer. Every write is counted in its path's access bound.
- Docs: `docs/ARCHITECTURE_HW_SW_SPLIT.md` and `docs/design/MAILBOX_SPLIT.md` (The publication block, Verification, Measured area). `milan_soc.py` changes only in the `--ctrl-mailbox` instance (ports named, unread). VERSION unchanged.
- Three fixes found while validating the earlier session's commits: the generated skeleton read the publication storage before declaring it (Vivado front end); `pub_idle_slope_o` is now `pub_idle_slope_bps_o` (naming ratchet); an existing SRP plant, `cancelled-link-never-recovers`, escaped because the reset's new publication writes posted the LINK record its test relies on being held. The host model gains `mbx_model_evt_pause` (held as a full RTL ring), the test asserts the hold, and a new plant proves the assertion.

Validation (head unless marked P = `9b73a8c6`, whose child changes only the host model and two SRP test files, which no P gate reads), all rc 0:
- `python3 sw/mailbox/gen_mailbox.py --check` / `--crosscheck` / `--selftest`: 0 findings.
- `make` arms of `tb/verilator/mbx` (Verilator 5.050): 401 Wishbone, 446 AXI4-Lite, 32 co-simulation, 403 / 448 / 388 at two interfaces, 0 failures; quick plants 6 of 6. `mutants.py`: 167 of 167 (P).
- `python3 scripts/lint_rtl.py --check --self-test`: 90 <= 90. `python3 scripts/xvlog_gate.py --check`: 0 findings (P). `syn/yosys/run.sh`: 58 of 58 tops (P). The `yosys-elaboration` job's OOC instrument commands (P). `behave` in `tests/`: 404 scenarios.
- `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2`: 51 arms, 492 of 492 and 186 of 186 plants. `test_ctrl_nvm.py --require-rv32`: 435 tests. `fw_coverage.py --selftest` 28 of 28; `fw_coverage.py --check`: PASS, 22 files; every writer file at 100 % lines and branches, no exclusion.
- The docs workflow's 76 checking commands (incl. `docs_check.py`, `check_em_dash.py --base 7c1b52be`, `gen_toc.py --check`, `measure_naming.py --check`, hygiene and idiom ratchets); `gen_hdl_reference.py --selftest` 44 of 44 (P).
- Builder: `test_firmware_compiler.py --selftest` and `--absent`, `test_builder.py --require-rv32` (P), `test_builder.py --require-elaboration --require-rv32` (P; one calibration arm not run, needs an unrelated local build tree). `scripts/run_litex_sims.sh`: self-test 10 of 10, 5 of 5 sims. `fw_service_budget`: 52 checks.

Acceptance criteria (ruling 6088423771, PR 1):
- Block, map, docs in both pages: met (above).
- Writers before the promising response in the adapters: met for ACMP, MAAP, SRP; no ADP writer, reason in MAILBOX_SPLIT.md.
- GoogleTest at the 100 % branch ratchet with ordering tests, and plants for moved, wrong-field and skipped publishes, each failing a named test: met (coverage above; plants listed per writer in the handoff).
- RTL simulation of the block (write and read-back, reset values, out-of-window refusal) with plants: met (checks P0 to P5, ten plants through both adapters).
- Comparator commits kept: met.
- All-fabric image byte-identical to dev: met at export level. Both AX7101 shipping configs exported at dev and at P from one tree path: 3,856 of 3,876 files byte-identical, 5 date-only, 13 archives with identical members. The 1x1 generated Verilog matches in all 30,946 lines outside date lines and LiteX's comment-only hierarchy tree; two sibling lines in that tree swapped places. Every checkout and submodule file the TCL reads is unchanged. No bitstream built.
- Firmware size against 224 KB: 1x1 at one interface 80,368 -> 81,376 B (35.5 %); 8x8 at two 122,672 -> 123,856 B (54.0 %). AECP is not linked (F5).
- Mailbox area delta via M0s, no re-record: the M0s all-fabric selection measures zero (no mailbox in that image). Its split selections need PR 2's route (PR #702 open; M0s STOP 6087021702) and were not run. The block's own out-of-context figure, re-run at P: +446 LUT, +1,136 FF, BRAM unchanged, WNS +0.329 ns at 10 ns. Nothing re-recorded.

Open risks/questions:
- Confirm that the zero all-fabric M0s delta plus the out-of-context block figure satisfy the area item for PR 1.
- Not run: the full 64-suite `run_all_suites.sh` sweep. Only `mbx` reads the changed RTL or firmware, and it ran in full. `act_ci.py --pr` waits for a PR.
- Choices visible to PR 2's comparison: the published stream_id follows the core's GET_RX_STATE (settled until SRP stops), whereas the processor holds the last settled one until the unbind. `LICENCE` already includes admission.
- Independent review not started; all five lenses uncovered.

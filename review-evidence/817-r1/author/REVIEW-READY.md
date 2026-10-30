[A709] REVIEW READY
Commit: `6cfb27dacafb2e5b693412db3342ca0fccc9c0bc` (branch `817-servo-reset-cdc`, two commits on dev `1e80128f`: `a7ff491a` the change, `6cfb27da` docs and one test docstring; local, not pushed, no PR)

Changed:
- `sw/litex/clock_constraints.tcl`: new `kl_servo_reset_sync_constraints`. It finds the servo's two-flop PS-clock reset synchronizer by structure and cuts only `psrst_sync_r_reg[0]/D`, only from the milan clock (`set_false_path`). It refuses a stage count other than two, a missing ASYNC_REG, a broken chain, or a PS clock that is not one clock distinct from milan.
- `sw/litex/clock_constraints.py`, `sw/litex/milan_soc.py`: the hook runs in the #607 post-synthesis, pre-optimize phase on the milan PLL output (`_CRG.milan_pll_clk`), wherever the servo's MMCM boundary is wired and the servo is not pruned.
- `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:1292-1294`: `(* ASYNC_REG = "TRUE" *)` on `psrst_sync_r`. No behaviour change.
- `sw/builder/test_shipping_clock_constraints.py`: each shipping elaboration must carry exactly one hook naming the milan PLL output, between synthesis and optimization. `sw/builder/test_clock_constraints.py`: a stub-netlist control of the one cut and each refusal.
- Docs: `docs/litex/CLOCK_DOMAINS.md`, `docs/integration/BUILDING.md` section 5, `docs/testing/RUNNING_TESTS.md`.

Validation (all at `6cfb27da` unless stated; the route at `a7ff491a`, whose child changes no build input):
- **route-1x1, ExtraPostPlacementOpt**, recipe unchanged, through the slot wrapper: rc 0. WNS / WHS +0.166 / +0.055 ns slow 0C and 85C, +1.481 / +0.020 ns fast 0C and 85C. TNS / THS 0, route complete. Dev's own route: +0.303 / +0.051 and +1.633 / +0.028.
- **The crossing**: before (dev's route) +1.975 ns setup, requirement 5.000 ns, timed as synchronous, 1 level; hold +0.634 ns. After: `Timing Exception: False Path` for setup and hold. `report_exceptions -to` the pin shows `-from [get_clocks -of_objects [get_nets milansoc_crg_clkout1]] -to [get_pins {milan_datapath/g_mmcm_servo.mmcm_servo/psrst_sync_r_reg[0]/D}]`, setup false, hold false. Both stages ASYNC_REG, in one slice.
- **No other constraint changed**: the routed exception list is dev's 25 plus exactly the new one, and the ignored-exception reports are identical. The XDC is identical, and the build Tcl gains one line. The handshake's 16 milan -> PS endpoints keep their 5.000 ns requirement.
- **Top 10 setup**: +0.166 LiteEth TX CRC -> `KL_gptp_gmii_launch/mine_r_reg` (Ethernet RX clock, 10 levels); +0.196 x4 and +0.336 x4 LiteDRAM ZQCS timer -> bank-machine level enables (`sys`, 15 levels); +0.390 `write_w_buffer_level0` -> `storage_10_dat1` (`sys`, 13 levels). At dev those families were +1.320 and +0.303. This change touches neither.
- **CDC report line for the crossing's pair** (dev and here alike): `Info milansoc_crg_clkout1 milansoc_crg_clkout4 Safely Timed None 17 17 0 0 0`. The whole-design CDC report has identical rows. Diagnostic only (the pair declared asynchronous in memory, not shipped): this crossing is `CDC-3 Info 1-bit synchronized with ASYNC_REG property` here, against `CDC-2 Warning ... missing ASYNC_REG property` at dev.
- **`python3 syn/ooc/pp_resource_gate.py check <route> --endpoint route-1x1`: exit 1, `RESULT: MATERIAL REGRESSION`, on WNS alone** (0.44 -> 0.166, -0.274 against the 0.25 limit). LUT 51,805 (-207), FF 53,759 (+52), slices 15,834 (+54), RAMB / DSP equal, WHS ok. Against dev's own route, which passes the same gate: LUT +4, FF -1, slices 0. Reported for the manager's WNS ruling.
- #607 log gate on the route log: no 12-4739, 20-1307 or 12-5201.
- **Constraint-presence check** `sw/builder/test_clock_constraints.py`: rc 0 at `a7ff491a` and `6cfb27da`. **Five planted mutants, all killed** (check rc 1): hook call removed (`shipping servo reset synchronizer hook missing, duplicated or renamed: []`); cut removed (`servo cut missing or widened: `); cut widened to every clock; ASYNC_REG refusal disabled (`accepted: *lacks ASYNC_REG*`); hook skipped with the servo present. Live, on dev's real netlist (no attribute), the hook refuses: `... psrst_sync_r_reg[0] lacks ASYNC_REG`.
- **The 17 suites that compile the servo**, each with `suite_tally.py --verdict`: all rc 0, 73,367 checks, 0 failures. They are capture_coherence, follow_ring, mmcm_servo, mmcm_servo_autorepair, mbx, crf_tx, crf_rx, milan_dp, milan_dp_mclk, milan_dp_render, media_phase, media_grid_align, media_nco, pp_shadow, aaf_clock_meter, csr and avtp_parser. `mbx` first failed from a missing `--no-print-directory` in my MAKEFLAGS and passed with CI's.
- `syn/yosys/run.sh`: `tops: 60 pass: 60 fail: 0`, `RESULT: PASS`.
- rtl-fast replica (changes, verilator-lint, bdd-conformance, yosys-tool, yosys-elaboration): all success. `LINT GATE: PASS (89 <= 89)`; behave `14 features passed, 0 failed`, `495 scenarios passed`.
- Docs gates replica (docs.yml): `44 steps, 0 failed`. Builder leg 1 with the LiteX interpreter: `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11 needs a board report absent here). Markdown gates on CPython 3.12.3: 5 of 5. No-git `docs_check` and `check_feature_status`: rc 0.

Acceptance criteria:
- Not timed as synchronous, and a constraint report shows the constraint applied: **met** (above).
- No other path's constraint changes: **met** (exception sets and the ignored report identical apart from the cut; XDC identical).
- A planted removal fails the constraint-presence check: **met** (M1, M2, M5; and the attribute's removal at the live hook).
- The CDC report lists the crossing as safe: **met at the pair level** (Safe 17 of 17, as at dev). Structurally it is CDC-3 Safe only under the diagnostic, because the shipped exception is endpoint-scoped between related clocks. Reviewer's reading requested.
- route-1x1 at the shipping directive meets the floor at every corner: **met**.

Open risks/questions:
1. The CDC-report criterion's reading (above). A shipped structural row would need a clock-level exception, which would change the handshake's 16 endpoints.
2. The cut leaves the reset route unbounded: 11.368 ns in this route, 2.671 ns at dev. It is a level held for the whole reset, the handshake is toggle-based, and the servo issues no batch until a window has produced a nonzero command. A `set_max_delay -datapath_only` bound is a one-line alternative.
3. The batch handshake's 16 milan -> PS endpoints stay timed as synchronous. `cdc_handshake.sv` asks for an exception; that would be a new issue.
4. The resource gate's WNS verdict (exit 1) is for the manager's ruling.

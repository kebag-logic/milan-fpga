# R367-2 stale-claim scan classification, exact head 471892a9

Scan: `python3 stale_scan_r367_2.py <clone>` (raw hits in `stale_scan_hits.txt`).
Scope: every tracked text file except `docs/history/**` and the submodules.
Match: a PHC-step, re-base, settime, adjtime or step term within +-2 lines of an `mr`, MEDIA_RESET or restart term.
Total: 185 hits in 26 files.

## STALE (current document states the superseded #387 PHC-step restart coupling)

| Location | Text at head | Current truth |
|---|---|---|
| `docs/integration/BAREMETAL_FIRMWARE.md:1469` | "`media_rebase_p_w` has exactly three references: Its initializer and two readers: `render_recentre_p_w` and `mcr_restart_p_w`." | `sw/builder/test_builder.py:10719` censuses 2 references; `hdl/milan/milan_datapath.sv:3132-3134` has no restart reader |
| `docs/integration/BAREMETAL_FIRMWARE.md:1471` | "`mcr_restart_p_w` is exactly `(crf_clk_selected_r & (...)) \| media_rebase_p_w`: The step is ungated by clock selection." | `test_builder.py:10774-10780` pins `crf_clk_selected_r & ((tkd_crflk_q_r & ~crf_locked_w) \| crf_mr_toggle_p_w)`; `milan_datapath.sv:3133-3134` |

## Current and correct (state the #602 exclusion, or describe genuine causes only)

- `CHANGELOG.md:16,116-139` (records the #602 reversal).
- `docs/MILAN_V12_ROADMAP.md:360-362`, `docs/fpga/FPGA_DESIGN.md:178-180`, `docs/reference/REGISTER_MAP.md:128-130`.
- `docs/design/GM_LOSS_RECOVERY.md:142-157,170-243,268`, `docs/design/TIME_SYNC.md:113,255-261,354`.
- `docs/reference/MILAN_COMPLIANCE_MATRIX.md:120,206`, `docs/testing/TESTING.md:273`.
- `hdl/milan/milan_datapath.sv:3094-3134`, `hdl/ieee1722/avtp/KL_media_clock_restart.sv:60-62,105-109,168-172`.
- `tb/verilator/milan_dp/README.md`, `sim_gmstep.cpp`, `sim_main.cpp`, `gmstep_mutants.py`, `Makefile:117,397-399`.
- `tb/verilator/tkdiag/sim_main.cpp:650-652` and the renamed T17/T18 stimulus comments.
- `sw/builder/test_builder.py` hunks (census 2, initializer without re-base, mutant anchors, diagnostics).

## Current, correct but dated wording (SUGGESTION F3)

- `tb/verilator/milan_dp/Makefile:19-20`: "three controls of the option-off leg's #387 mr checks". The checks are #602 exclusion checks. No PHC-step `mr` claim.
- `tb/verilator/milan_dp/README.md:680`: "later counts require re-measurement". This round measured 42/42 feed delays at 103/0 (`feed/feed_sweep.tsv`).

## Unrelated senses (no media-clock claim)

- Render re-centre and step-policy text: `docs/design/TIME_SYNC.md:354` (Recentre row), `tb/verilator/milan_dp/sim_aclk.cpp:148`.
- CRF servo guard "streak restarts": `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:707`, `tb/verilator/mmcm_servo/sim_main.cpp:25-26,521-554`.
- NVM snapshot "re-base"/"restart": `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` (9 hits), `tb/verilator/nvm_cosim/cosim_case_map.py` (4), `cosim_cases.cpp:1171`.
- Field evidence of PHC steps covered by holdover/`tu`: `docs/findings/117_GPTP_SILICON_EVIDENCE.md:500`.
- Presentation-time wrap prose: `docs/design/PRESENTATION_TIME_WRAP.md:31`.
- `docs/integration/BAREMETAL_FIRMWARE.md:1468,1470,1520-1524`: still true at this head (the `cfg_ptp_cmd_load` 5 and `eff_ptp_adjust_w` 3 censuses at `test_builder.py:10705,10716`; the render initializer; the control summary).

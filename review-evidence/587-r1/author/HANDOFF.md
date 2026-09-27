# Issue #587 handoff

Author: [A360]
Status: local implementation and all assigned gates complete; independent review pending.
Head: `55079500483970ee244f12fa4c94401783f3df6f`
Subject: `Record the 8x8 protocol baseline at the declared 50 MHz`
Branch: `587-8x8-baseline-50mhz`
Base and measured input tree: `63fe4fb0164d798d44a6476001dc8b887cdd4609`
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`
Worktree: `$LANES/587-8x8-baseline-50mhz`
Build root: `/tmp/milan-587-a360`
Assignment: https://github.com/kebag-logic/milan-fpga/issues/587#issuecomment-5855348441
Independent reviewers: [R350] internal and [R351] external.

## Change list

- `docs/findings/PP_SHADOW_BASELINE.md:61`: explicit clocks on original measurements; 100 MHz 8x8 figures remain history.
- `docs/findings/PP_SHADOW_BASELINE.md:111`: new 50 MHz comparison, synthesis totals, timer parameters, attribution counts, timing subset, probe evidence, provenance and reproduction notes.
- `docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json:1`: measured revision, tool/dependency versions, parameters, complete source/image hashes, report/checkpoint hashes and sizes, probe results and load stems.
- `docs/findings/PP_SHADOW_BASELINE_50MHZ_RANKING.tsv:1`: 82 rows covering every direct wrapper/processor child, own logic and reconciliation in both 50 MHz variants.

Only these three documentation/evidence files changed. RTL, configuration, tooling and submodule pins are unchanged. Both initialized processor checkouts and the AXIS checkout are clean. The commit has one subject line, no body and no trailers.

## 100 MHz versus 50 MHz figures

| Measurement | Historical 100 MHz | Declared 50 MHz | Delta, 50 minus 100 MHz |
|---|---:|---:|---:|
| Default whole LUTs | 68,136 | 68,047 | -89 |
| Default whole FFs | 70,835 | 70,744 | -91 |
| Default whole RAMB36 / RAMB18 | 80 / 29 | 80 / 29 | 0 / 0 |
| Default whole DSPs | 11 | 11 | 0 |
| Default whole CARRY4s | 3,916 | 3,913 | -3 |
| Default whole WNS (ns) | -11.331 | -1.708 | +9.623 |
| Attribution wrapper LUTs | 29,489 | 28,955 | -534 |
| Attribution wrapper FFs | 32,991 | 32,982 | -9 |
| Attribution wrapper RAMB36 / RAMB18 | 26 / 5 | 26 / 5 | 0 / 0 |
| Attribution wrapper DSPs | 8 | 5 | -3 |
| Attribution wrapper CARRY4s | 1,809 | 1,774 | -35 |
| Attribution wrapper internal WNS (ns) | -10.846 | -1.700 | +9.146 |
| Attribution whole LUTs | 70,206 | 69,923 | -283 |
| Default rebuilt wrapper-name LUTs | 37,809 | 38,351 | +542 |
| Attribution AECP LUTs | 5,025 | 5,022 | -3 |
| Attribution dynamic-state LUTs | 574 | 574 | 0 |


The default total remains 4,647 LUTs above the 63,400-LUT device capacity. Default WNS is a synthesis estimate. The worst default path runs from `u_pp/u_notify/ctr_pend_r_reg[3]/C` to `u_pp/u_event_router/sel_r_reg[3]/D`, at a measured 20.000 ns clock period, through 43 logic levels.

The 50 MHz attribution whole-design figures are 69,923 LUTs, 72,421 FFs, 80 RAMB36s, 29 RAMB18s, 11 DSPs, 4,013 CARRY4s and -1.700 ns WNS. These remain separate from the default fit baseline. The three historical extra NVM DSPs disappear in the 50 MHz attribution run.

Both 50 MHz checkpoints were probed with the unchanged public scripts from `e21bc530eb89f7bd325f8d774aad5b5d95c70c1c`. Dynamic-state raw LUTs are 9,010 / 607 in default / attribution; external-only loads are 5,824 / 0. Attribution retains 518 wrapper-level external-only raw LUT cells. Recorded stems include `gsi_data_r`, `csr/live_mux_q` and `ctl_tx_mux`. These counts describe primitive locations; they do not measure reverse relocation. The complete load stems are committed in the input manifest.

## Input hashes and versions

Configuration SHA-256: `ede309aa78d5eb566e9a3c93a0ef6c843cc181c1d3f2bbe32eda5db62961983e`.
The current processor pin is `0922e43408f891fc0b84a84691df86b4fd0f1c0d`; historical pin was `990f96526bb89356c963a260ebbdcf2a77e6623a`. Their HDL trees compare byte-for-byte equal. gPTP remains `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`; AXIS remains `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

The launcher emitted `--milan-clk-freq 50e6` from the configuration. Synthesis bound `CLK_HZ_P=50000000`, `TIM_DIV_US_P=50`, `TIM_DIV_MS_P=1000`, nine processor inputs and nine outputs. Only the clock and microsecond divider differ among the 20 historical wrapper parameters. The two 50 MHz exports have the same 118 source reads and order, matching image bytes and matching generated RTL after normalizing comments and build-root strings.

| Image, identical between the two 50 MHz variants | Bytes | Words | SHA-256 |
|---|---:|---:|---|
| `alinx_ax7101_rom.init` | 116811 | 12979 | `c05e5c24ed202eee530f6dcd44585eafca46e74d94d82865bbf404e03cd964dd` |
| `alinx_ax7101_sram.init` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `alinx_ax7101_mem.init` | 147 | 49 | `d1657b93f1791073b22bd153501d5b9474a7676633af2a6c7b049a155b818335` |
| `ltn_rom.hex` | 6138 | 128 | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` |
| `ucode.hex` | 26624 | 2048 | `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144` |
| `gptp_ucode.hex` | 13312 | 1024 | `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b` |

Firmware and both processor ROM hashes match the historical 100 MHz inputs. The generated gPTP image changes with the clock. Empty SRAM initialization is intentional and is not an instruction ROM. All source and image hashes matched after each synthesis and again after both completed. Every synthesis log has zero missing-ROM diagnostics.

The complete input ledger is `docs/findings/PP_SHADOW_BASELINE_50MHZ_INPUTS.json`. Packet files `SOURCE-HASHES-DEFAULT.json` and `SOURCE-HASHES-ATTRIBUTION.json` retain the concrete local paths for inspection. `ARTIFACTS.tsv` records raw report/checkpoint SHA-256 and byte sizes; raw large files remain only under the build root.

| Tool or environment component | Version or identity |
|---|---|
| Vivado | 2026.1, SW 6511674, IP 6504888, SharedData 6501428 |
| Part / synthesis directive | xc7a100tfgg484-2 / AreaOptimized_high |
| Threads / seed | 32 / default; public probes retain 2 threads |
| Python | 3.14.7 |
| Target GCC | 14.3.0 |
| Verified SDK | riscv32-ilp32d--glibc--stable-2025.08-1 |
| SDK archive SHA-256 | d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f |
| cmarkgfm / html5lib | 2025.10.22 / 1.1 |

Required dependency patches were already applied and verified without modification. Dependency revisions and patch hashes are in the committed manifest. An initial unreceipted SDK candidate was rejected during environment discovery; the actual measured builds used the verified SDK at `$VALIDATION_STORAGE/231-a337-sdk`.

## Measurement commands and results

Commands ran in the foreground, with explicit generous subprocess timeouts and no pipelines. Only the `ax8x8` branch of the existing recipe was executed; it compiled firmware and generated the design, without `--build`, into separate default and attribution directories. All design arguments were retained. The preparation helper remained unchanged.

| Step | Command or operation | rc |
|---|---|---:|
| Configuration preview | `bash sw/litex/build.sh ax8x8 --dry-run` | 0 |
| Default export | Printed `milan_soc.py` command, omit `--build`, change output directory only | 0 |
| Attribution export | Same printed command, separate output directory | 0 |
| Default preparation | `python3 syn/ooc/pp_baseline.py /tmp/milan-587-a360/default/ax8x8/gateware --synthesis-only` | 0 |
| Attribution preparation | `python3 syn/ooc/pp_baseline.py /tmp/milan-587-a360/attribution/ax8x8/gateware --synthesis-only --attribution-only` | 0 |
| Default synthesis | `vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log`, default gateware cwd; 1208.61 s | 0 |
| Attribution synthesis | Same command, attribution gateware cwd; 1173.75 s | 0 |
| Boundary probes | Unchanged `boundary.tcl` on both synthesis checkpoints | 0 / 0 |
| Dynamic-state load probes | Unchanged `loads.tcl`, `milan_datapath/pp_shadow/u_pp/u_aecp/u_dyn` | 0 / 0 |
| Wrapper load probes | Unchanged `loads.tcl`, `milan_datapath/pp_shadow` | 0 / 0 |

The dry-run's tracked-header ownership warning is expected under the original recipe: the explicit 8x8 include selects the measurement shape and the tracked shipping header stays unchanged. No STOP condition occurred.

## Gate table

Every gate below ran from the physical worktree at the stated final head. `GATE-RECEIPTS.json` records argv, cwd, head, elapsed seconds and rc. Each named log is included in this packet. The locked documentation environment was selected through PATH; no environment or packages were copied into this packet.

| Command | rc | Evidence |
|---|---:|---|
| `python3 syn/ooc/pp_baseline.py --selftest` | 0 | `baseline-selftest.log` |
| `python3 syn/ooc/pp_baseline_mutants.py` | 0 | `baseline-mutants.log` |
| `python3 -B scripts/docs_check.py` | 0 | `docs-git.log` |
| `env GIT_DIR=/dev/null python3 -B scripts/docs_check.py` | 0 | `docs-no-git.log` |
| `python3 scripts/check_em_dash.py --base 63fe4fb0` | 0 | `em-dash.log` |
| `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `contents.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `anchors.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| `git diff --check` | 0 | `whitespace.log` |
| `git diff --check 63fe4fb0 HEAD` | 0 | `committed-whitespace.log` |

The pristine baseline control passed, all 28 maintained mutants were killed, and 40 synthetic inventory refusals passed. Both documentation modes inspected 901 text files with zero findings. The no-Git mode omits only Git inventory parity. The em-dash gate passed all 339 control arms. All 179 cross-page anchors and 848 cited paths resolved. The whitespace checks cover both the clean worktree and the committed delta.

## Limits and delivery

Both measurements are synthesis-only. Both retain warnings 12-4739, 12-5201 and 20-1307. The reports have zero unclocked or unconstrained internal endpoints, but 46 inputs and 86 outputs lack I/O delays. There is no placement, routing, board-interface signoff, bitstream or hardware claim. Original 1x1 and standalone measurements remain unchanged.

The #229 reference comment was updated and read-back verified at https://github.com/kebag-logic/milan-fpga/issues/229#issuecomment-5847400261. The project card is In review. The final action is the `[A360] REVIEW READY` comment on #587, identifying this local head and results. Publication and independent review remain pending. No push, PR creation/edit, merge, other checkout, submodule edit or hardware operation was performed. Temporary artifact symlinks were removed; build evidence remains outside the repository.

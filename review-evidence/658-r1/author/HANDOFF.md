# #658 stage 2 - [A539] handoff

Role: executor (author). Lane `658-dynmap-default`, stage 2 on top of `c36bfb03`
(stage 1 handoff preserved in `HANDOFF-stage1.md`).
Ruling: #658 comment 5988843004 (option A reset image; Milan 5.4.2.7 refusal
kept; clip the default to a restored format before AECP release; docs; tests
and controls). TAKEN (stage 2): #658 comment 5988924925.

Status: REVIEW READY at `fb4953bd61b0f6ca61ab067081e766fe37f96076` (8 commits
on `c36bfb03`, not pushed). Every gate in section 6 exits 0; area in 6a.

## 0. Summary

- Every dynamic Stream Port now powers up mapped: stream channel c on the
  port's cluster c, for c below min(channels, clusters). Input store and
  output owner/cluster registers reset to it; both crossbar RAMs are filled
  from it by a boot writer on the existing AECP write legs.
- Milan 5.4.2.7 refusal kept: 8 -> 4 with 4..7 mapped answers BAD_ARGUMENTS
  (status 7), format and maps unchanged. REMOVE first, then SET.
- Until the restore's terminal (D3 COMPLETE/DEFAULTS = AECP release, or
  CLOSED) the stores hold the image clipped to the live formats. A saved 4 ch
  input format restores beside 4 identity mappings; SET 8 ch then succeeds.
- No port, register field, parameter, leaf or processor change.

## 1. Map stores and their reset values at the head (`fb4953bd`)

| Store | Reset value now | Who writes it after reset | file:line |
|---|---|---|---|
| `amap_in_store_r` (input store, key = global cluster) | `AMAP_IN_IMAGE_C`: key PBASE[p]+c = {en, AVB, stream p, ch c} for c < min(SCH, PCLS, declared default ch) on dynamic AAF ports | boot window: `amap_in_boot_w` (clip) every cycle until the terminal; then ADD/REMOVE phase 5 and the CSR window | decl `hdl/milan/milan_datapath.sv:3767`; reset `:4629`; image `:4495`; clip `:4535`; window override `:4761` |
| `amap_out_owner_v_r`/`_owner_r`/`_cluster_r` | `AMAP_OUT_IMAGE_C`: key p*8+c owned by port p, cluster c, same bounds (dynamic outputs, p < N_STREAMS) | same | decl `:1222-1224`; reset `:4630-4632`; image `:4496` |
| Capture map RAM (`KL_chan_map_capture` `map_r`) | still 0 at reset (leaf unchanged) | boot writer `amap_boot_walk`/`amap_boot_slot` (`:4562`, `:4589`) writes `AMAP_OUT_WORDS_C[k]` where owned, else 0, through `amap_edit_owr_*` | `hdl/ieee1722/aaf/KL_chan_map_capture.sv:500` |
| Render map RAM (`KL_chan_map_render` `map_r`) | still 0 at reset (leaf unchanged) | boot writer writes the store word at RPHYS[k] through `amap_edit_iwr_*` | `hdl/ieee1722/aaf/KL_chan_map_render.sv:143` |
| Boot window / writer state | `amap_boot_r` 1, last-sweep/drain 0, cursor 0 | ends at `pp_restore_done_w || pp_restore_closed_w` (`:4570`) | `:4562` |
| Edit-face wait, CSR hold | `amap_boot_busy_w` | `pp_amap_edit_wait_w` (`:4358`), CSR gates (`:1259`, `:4742`, `:4754`, `:6786`) | `:1155` |

## 2. Simulated readbacks (dynmap leg, AX7101 1x1 TDM8 geometry)

| Step | STREAM_INPUT 0 | SPI 0 GET | SPO 0 GET | crossbar RAMs |
|---|---|---|---|---|
| power-on | 8 ch | 8 identity | 8 identity | render keys 2..9 = 0x80+c; capture keys 0..7 = TDM slot c |
| SET 4 ch | refused 7, still 8 ch | 8 | 8 | - |
| REMOVE 4..7 | 8 ch | 4 | 8 | render keys 6..9 = 0 |
| SET 4 ch | 4 ch | 4 | 8 | - |
| SET 8 ch | 8 ch | 4 (kept) | 8 | unchanged |
| new boot, output row staged at 4 ch in the window | - | - | - | capture keys 4..7 empty; refill when the row is invalid again |
| new boot with a saved 4 ch record 0x30 | restored 4 ch; PP_STAT done 1, fail 0, blank 0 | 4 identity | 8 identity | render 2..5 mapped, 6..9 empty |
| then SET 8 ch | 8 ch, SUCCESS | 4 | - | - |

142 checks, 0 failures (`make -C tb/verilator/milan_dp dynmap`).

## 3. How the observed bench state arises

Unchanged from stage 1 (`HANDOFF-stage1.md` section 3): a controller's ADD of
s0.c0 -> cluster 0 after REMOVE of the rest, carried by "restore as found",
with no power cycle since. With this image a power cycle reads the identity
on both ports, clipped to the persisted 4 ch input format (4 mappings).

## 4. The option implemented, and why the RAMs use a writer

- Option A as ruled. Files: `hdl/milan/milan_datapath.sv` only.
- RAM reset images in the leaves would still need the writer for the clip and
  would be leaf parameter changes, so the writer is smaller and changes no
  interface. It also re-grows the map after a roll-back to default formats.
- Protocol-visible: GET reads the identity from the first answer after AECP
  release; nothing is notified (no controller can be registered before it).
  An ADD onto an identity-held cluster (input) or stream channel (output) is
  BAD_ARGUMENTS until it is REMOVEd (Milan 5.4.2.27 allows it).
- Window also ends at CLOSED: AECP stays held there, and the legacy leg
  (`obj_dir`) programs the capture map through the CSR window in that state.
- Race analysis for the final sweep (<= AMAP_BOOT_KEYS_C + 2 cycles after the
  terminal): GET reads the stores, which are final; ADD/REMOVE wait at phase
  0 (processor bound 4096 cycles); the CSR writer is refused. The output
  format verdict (`sfv_out_need`) reads the capture RAM, which may lag for
  those cycles, but an output format is accepted only at its declared channel
  count and the identity never exceeds it, so no verdict can change.

## 5. Tests

- `[DYNMAP]` rewritten and in `run`; `gen_nvm_window.py`; NVM window model and
  firmware load sequence in `sim_nxn.cpp`; `dynmap_probes.vlt`.
- Planted controls `make dynmap-mutants`: 9/9 (6 mutants caught, 3 clean
  controls pass), 662 s. Table in `tb/verilator/milan_dp/README.md`.
- Re-based: `[AMAP]`, `#67`, `#67dv`, 8x8 `0x002C`, `[T66]` (sim_nxn.cpp);
  render `[MAP]`, `[MULTI]`, T18 recovery; pp_shadow K12 boots.
- E2E with no map command: listener `T18 POWER-ON` (milan_dp_render),
  talker capture_coherence datapath leg (332/0).

## 6. Gate table (head `fb4953bd`)

Pinned Verilator 5.050 throughout.

| Gate | Command | rc | Result |
|---|---|---|---|
| milan_dp legs, each alone | scratch driver over `make -n run`'s builds | 0 | 12/12 legs 0 FAIL (pre-commit tree) |
| milan_dp_render | `make` in the suite dir | 0 | tdm8render 258/0, multi 70/0, leg defects 5/5 |
| capture_coherence | `make -C tb/verilator/capture_coherence` | 0 | junction 20832/0, datapath 332/0, mutants 30/30 |
| milan_dp_mclk | `make -C tb/verilator/milan_dp_mclk` | 0 | 32/0, 50/0, mutants 31/31 |
| pp_shadow | `make -C tb/verilator/pp_shadow` | 0 | 609, 609, 649, 317 checks, 0 failures |
| planted controls | `python3 dynmap_mutants.py` | 0 | 9/9 |
| Yosys | `syn/yosys/run.sh` | 0 | 55/55 tops, tap purity PASS, wall 690 s |
| lint | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| docs workflow gates | docs_check, em-dash (base e6172750), doc style, gen_toc, idioms (sv/cpp/py/sh), hygiene, naming, fail-fast, test evidence, port contracts, doc paths, module matrix, feature status, TODO, solution docs, source lists, pp_srcs, archive, bare-metal, ci_events, act selftest, SoC sources, wire accountability, NVM record space, NVM capture, AEM store, shape self-tests, DOC_MAP, gPTP docs, submodule docs, diagram PNGs, HDL reference | 0 each | - |
| full sweep, first run | `scripts/run_all_suites.sh <dir>` at `fb4953bd` | killed | stopped by the 2 h tool limit after 45 suites, all PASS; the other 14 ran by the same per-suite recipe (`timeout 1800 make -C <suite>` + `suite_tally.py --verdict`), each make rc 0 and verdict rc 0. Tally over all 59: 2,149,203 checks, 0 failures, 4 declared skips (tsn_fuzz, tsn-gen absent) |
| full sweep, sharded rerun | `scripts/run_all_suites.sh <dir> --shard i/5`, shards 4 and 0 in the lane, 1-3 in a clean `fb4953bd` worktree | 0 x5 | 59/59 PASS, 0 timed out; walls 4: 1832 s, 0: 860 s, 1: 2856 s, 2: 2369 s, 3: 555 s. `scripts/suite_tally.py` over the five dirs rc 0: 2,149,203 checks, 0 failures (`stage2_sweep_sharded_tally.txt`). milan_dp 12044/0 (dynmap leg 142/0), milan_dp_render 334/0, capture_coherence 21194/0, pp_shadow 2184/0, milan_dp_mclk 168/0 |
| docs/source gates re-run at the final head | the docs workflow commands (docs_check, em-dash vs `e6172750`, doc style + selftest, doc paths, gen_toc anchors/check, hygiene, test evidence + selftest, naming, py/cpp/sv idioms, fail-fast, feature status, TODO, module matrix, DOC_MAP, source lists, port contracts), `lint_rtl.py --check`, `pp_srcs.py --check --selftest` | 0 each | at `fb4953bd`, clean tree |
| physical gPTP leg on the trial merge | `make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4` in a worktree holding `git merge-tree --write-tree origin/dev HEAD` = `bf00f45c` (dev `fa450d30`, #662 changed this harness) | 0 | physical 139/0, setup abort 6/0, no-TX accounting 20/0, no-Pdelay accounting 14/0 (179 checks, 0 failures), 3960 s; `stage2_gptp_physical_trial_merge.log` |
| builder bank | `python3 sw/builder/test_builder.py` | 0 | every gate OK except gate 11 SKIP (calibration needs the mf48 Arty place report, not on this host) |
| xvlog | `flock $VIVADO_LOCK python3 scripts/xvlog_gate.py --check` | 0 | PASS, 4 findings == ratchet (0 in hdl/, 4 pinned processors), 4717 s |
| planted controls on the head | `make -C tb/verilator/milan_dp dynmap-mutants` | 0 | 9 checks, 9 PASS, 710 s |
| area | `syn/resmap/datapath_ooc.tcl`, `ship` point, base `c36bfb03` vs head `fb4953bd`, under `flock $VIVADO_LOCK` | 0, 0 | section 6a |

## 6a. Area (OOC 1x1, `endstation_ax7101_1x1_tdm8`, xc7a100tfgg484-2, Vivado 2026.1)

Both points were made with `vivado-point ship` from clean checkouts. The source
lists are identical apart from the tree prefix. Point sha256: base `fef861c8...`,
head `3e9b8545...`. Walls: base 1256 s, head 1028 s. The reports and the
per-instance delta are in `area_ooc_1x1/`.

| whole OOC top | base | head | delta |
|---|---|---|---|
| Slice LUTs, synth | 44253 | 44393 | +140 |
| Slice LUTs, opt_design | 43634 | 43769 | +135 |
| FF, synth | 48858 | 48858 | 0 |
| FF, opt_design | 48764 | 48770 | +6 |
| F7 muxes, opt_design | 1260 | 1146 | -114 |
| LUTRAM / BRAM tiles / DSP | 1822 / 36 / 14 | same | 0 |

The ruling expected 0 LUT and 0 FF for the reset image, and the image alone
meets that: only reset values change, and no flip-flop is added. The +135 LUT
comes from the writer, the clip and the edit-face wait. The base tied
`amap_edit_wait_i` to 0, so its wait path was optimized out of `pp_shadow`. It
is now live, and `pp_shadow` shows +189 LUT after opt. The parent's own cells
show +5 LUT and +6 FF. Other instances move by small amounts in both
directions; that is cross-boundary optimization.

## 7. Open questions to publish

- 8x8 (non-shipping): the literal ruling maps each output's stream channels
  1..7 to unbacked loopback clusters (silent with the lane off); the builder's
  unconsumed `AEM_ODMAP_INIT_C` (task #65 rule) maps only the backed Pilot.
  Restricting to CSRC-backed clusters is a one-term change.
- #70 stage 3 must take the boot window over for ports whose map records it
  restores (it drives the edit face inside the window).

## 8. Public record

- Stage-2 TAKEN: #658 comment 5988924925 (`TAKEN-stage2.md`).
- REVIEW READY: #658 comment 5996651751 (`REVIEW-READY.md`), head `fb4953bd`.
- Nothing pushed; no PR. `PR-BODY.md` here.

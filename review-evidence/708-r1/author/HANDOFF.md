# [A585] lane 708: third processor pin adoption (protocol-processor main 2cbed0a9)

## Resume (after the #696 hold)

Authority: the [resume comment](https://github.com/kebag-logic/milan-fpga/issues/708#issuecomment-6207474061), the
[08:46 ruling](https://github.com/kebag-logic/milan-fpga/issues/708#issuecomment-6095815359), the
[flow decision](https://github.com/kebag-logic/milan-fpga/issues/708#issuecomment-6100507393) and the original
[assignment](https://github.com/kebag-logic/milan-fpga/issues/708#issuecomment-6094788195). Resumed from the STOP head
`99a5a2ac`. TAKEN was not posted again.

Status: **REVIEW READY** at `5c6f50eefa4c5545f052ec843363ace5e7936e8a` (branch `708-pin3`, not pushed; worktree clean).

The route meets the floor at +0.215 ns, the three endpoints are re-baselined, and every gate and suite ran rc 0. That
includes the 63-suite sweep, the physical gPTP suite, the processor and gPTP processor sweeps, Yosys, `xvlog`, the builder
bank, the docs workflow and the image.

### Acceptance (#708)

| # | Item | Status | Evidence |
|---|---|---|---|
| 1 | gitlink at `2cbed0a9`, with the adaptations and no other processor change | met | `75a28523` changes the gitlink only. The adaptations are under "Changes", and the processor checkout is clean at `2cbed0a9` |
| 2 | resource gate re-baselined at the adopted image under the rule; route WNS at or above the floor, no exception | met | "Re-route" and "Standalone endpoints". `check` rc 0 x3 against #696's record, then `record --write` (`9ac9f5ca`). WNS +0.215 ns |
| 3 | capture re-measured if the firmware digest moves | met (not triggered) | The firmware ROM and init images are byte-identical to dev's, and `check_nvm_capture.py` passes ("Capture comparison") |
| 4 | every parent gate and suite passes, including the image build | met, one declared difference | "Gates after the merge". The image is the measured route's bitstream, DRC clean. The shipping launcher's eight-worker synthesis does not fit the lane's memory budget and was stopped; none of its output is used ("Image build") |
| 5 | post-merge flash and soak | manager, after the merge | |

The PR body uses `Closes #708` on that basis. A reviewer who reads acceptance 4 as requiring the shipping launcher's
own run should change it to `Relates to #708`.

### Review-ready comment

[REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/708#issuecomment-6218773474), posted 2026-10-16 at
head `5c6f50ee`. Nothing was pushed, and no PR was opened.

### Continuation after the host shutdown (2026-10-16, from 16:00)

The resume session was cut by a host shutdown, not by a gate failure. The worktree was clean at `5c6f50ee`: every
commit above had been made, and nothing was uncommitted. Two runs had started and had no exit code when the host went
down, so neither is counted from the cut session:

- The physical gPTP suite (`run_all_suites.sh --physical-gptp`, started 09:03 in a clone of `82227af0`). Its suite
  log ended in `RESULT: PASS`, but the driver never wrote its own verdict, and the tally step never ran.
- The gPTP processor's own tests (`make contract tb lint` at `e4869fd0`, started 10:09). Its log stops inside the engine
  mutation arm.

Both were re-run from scratch at the final head, in fresh clones (see "Gates after the merge"). No commit was made in
the continuation, so the head is still `5c6f50ee`. TAKEN was not posted again.

### Merge

- `origin/dev` `734eb780dc93896a5961cd95180f79475a401650` merged into `708-pin3` as `a1dfbfad` (merge commit, no rebase).
- Conflicts (5): `docs/reference/SUBMODULES.md` pin table, `sw/firmware/ctrl/aecp/README.md`, and the three generated
  diagram files with `docs/diagrams/PNG_MANIFEST.json`. They were resolved as follows:
  - `docs/reference/SUBMODULES.md:20-29` pin table: dev's rows (gptp `e4869fd0`, lwSRP `08ee86e8`, the new
    `third_party/tsn-c-stack` `70936b77`) with the processor row at the lane's `2cbed0a9`. The rows equal
    `check_submodule_docs.gitlink_pins()` at the merge (`check_submodule_docs.py` rc 0, 6 exact gitlinks).
  - `sw/firmware/ctrl/aecp/README.md:136-145`: the lane's statement that the single-interface reference `2ad2f845` is no
    longer the pin, so `--reference` takes a checkout of it. Dev's added sentence on the TSN stack's wire layer
    (`--stack`) is kept. Dev's new `--every` mode extracts both references from the processor submodule's own objects.
    `2ad2f845` and `c9f74b68` are ancestors of `2cbed0a9`, so both remain resolvable.
  - `docs/diagrams/submodule_boundaries.{drawio,svg,png}` and `PNG_MANIFEST.json`: dev's side taken, then regenerated
    with `python3 docs/diagrams/submodule_boundaries.gen.py` at the merged gitlinks; `--check` rc 0 (6 exact gitlinks,
    decoded PNG). Raster inspected: six boxes, with the processor pin `2cbed0a987c1`.
- Auto-merged without conflict and checked: `syn/yosys/rom_digests.tsv` (the generator re-run at the merge is
  byte-identical), `scripts/measure_test_evidence_readers.py` (the pp170 entry kept; `measure_test_evidence.py --check`
  rc 0), `docs/design/MAILBOX_SPLIT.md` and `sw/firmware/ctrl/README.md` (the lane's ACMP text kept beside dev's F3b
  and publication-block text).
- Submodules after the merge: gptp-processor `e4869fd0`, lwSRP `08ee86e8` and tsn-c-stack `70936b77` (new) were checked
  out at their gitlinks. Each was verified for toplevel and origin. The processor stays at `2cbed0a9`.

Commits after the merge:

| Commit | Change | Generator / evidence |
|---|---|---|
| `a1dfbfadfb02c52f7ab917bbf4d3761b6f8a0d35` | merge of dev `734eb780` | conflict resolutions above |
| `435af429dc313465954c8bb59892f8bcc08ccf45` | `scripts/port_docs.budget:21` census header `hdl 2089` -> `2103` | `python3 scripts/check_port_contracts.py --write-budget` (only the header line moved; every ratchet unchanged; `check_port_contracts.py` rc 0). `measure_naming.py --write-budget` and `ooc.sh --record-rom-digests` reproduce their records byte for byte |
| `82227af0c44164610e302f6144fa2775a18653b3` | `docs/design/MAILBOX_SPLIT.md:32` contents entry: "the four former differences from the processor, each now a check that fails if the old answer returns" | the entry still said "the four differences" (stale since `afc0b831`); `gen_toc.py --check`, `check_doc_style.py`, `check_em_dash.py --base 734eb780` rc 0 |

### Re-route

The shipping 1x1 TDM8 image was re-routed with the **unchanged recipe**: default directives
(`ExtraPostPlacementOpt`), `--single-thread-synthesis`, Vivado v.2026.1 build 6511674, `xc7a100tfgg484-2`, default
seed, the gate's flow identity. It ran in a fresh clone of `435af429` (image inputs identical to every later commit),
exported by the recipe's own commands, under the exclusive `$VIVADO_LOCK` as a background job. The lock was
first held by another job (a dev `734eb780` image build), and this route waited for it.

**The route meets the floor, so no register boundary was added.** `pp_resource_gate.py check --endpoint route-1x1` exits 0.

| `route-1x1` | Record (`bee1b0d7`, processor `2ad2f845`) | Candidate (`435af429`, processor `2cbed0a9`) | Delta | Verdict |
|---|---:|---:|---:|---|
| LUT | 50,013 | 49,613 | -400 | ok |
| FF | 54,306 | 52,353 | -1,953 | ok, re-baseline recommended |
| Slice (of 15,850) | 15,753 | 15,725 | -28 | ok (125 free) |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 25 | 0 / -2 | ok, RAMB18 re-baseline recommended |
| BRAM tiles (ceiling 121.5) | 87.5 | 86.5 | -1 | ok |
| DSP / CARRY4 | 14 / 3,397 | 14 / 3,399 | 0 / +2 | ok |
| **WNS ns** | +0.233 | **+0.215** | -0.018 | ok: 0.185 above the +0.030 floor; fall 0.018 of the 0.25 limit |
| WHS ns | +0.017 | +0.036 | +0.019 | ok |

Against dev's own route, the manager's reference is +0.346 ns at `9ef71772`. The dev `734eb780` shipping build on this
host also reads +0.346 / +0.036 ns, and `734eb780`'s image inputs equal `9ef71772`'s: the commits between them touch only
CI scripts, workflows and docs. The candidate's fall from that figure is 0.131 ns, inside the 0.25 ns limit. That
figure comes from the shipping flow, not the recipe; the like-for-like shipping comparison is the image build below.

The RAMB18 drop and most of the FF drop come from dev, not the adoption. Mark II M7 (`f6260253`) merged under the D7
exception without re-recording. In its own route it freed 2 RAMB18 and 1,193 FFs against the record's dev
(`docs/design/MARK_II_AREA_PLAN.md`, "M7 intermediate measurement"). M2, M5, M6 and M8a-1 also merged under D7. The
processor change's own movement is isolated in the standalone endpoints, whose wrapper sees no parent change.

| Corner | WNS ns | WHS ns |
|---|---:|---:|
| Slow_0C | +0.215 | +0.102 |
| Slow_85C | +0.215 | +0.102 |
| Fast_0C | +1.683 | +0.036 |
| Fast_85C | +1.683 | +0.036 |

- Route status: 99,235 of 99,235 routable nets fully routed, 0 routing errors. No negative-slack path at any corner.
  The IOB pack check passes, with no FAIL line.
- Log: the one `CRITICAL WARNING` match is the echoed IOB-check Tcl text, not a diagnostic. `Synth 8-4445` appears
  only as the echoed severity command. `Synth 8-6901` appears once: the known parent `crft_emit_en_w`
  (`hdl/milan/milan_datapath.sv:3177`).
- Worst setup path (SoC side, `milansoc_crg_clkout0`, 10 ns): `FSM_onehot_socbushandler0_axilite2wishbone_state_reg[3]`
  -> `milansoc_spiflash_phy_cnt_reg[8]/D`. It has 17 logic levels, and its data path is 9.724 ns (3.494 logic, 6.230
  routing, 64 %). That differs from the STOP route's worst path (`subfragments_fsm0` -> `tmod0`, 78 % routing); both are
  SoC-side.
- Worst hold path: `u_gptp_shadow/u_engine/frame_cid_r_reg[34]` -> `evq_pd_ctx_r_reg_0_3_114_119/RAMA/I`, +0.036 ns
  (`milansoc_crg_clkout1`).
- Route sub-block movements against the record (printed, not gated): wrapper +121 LUT / +22 FF; `u_pp` +96 / +22;
  `u_pp/u_listener` +100 / +12 and `u_pp/u_talker` +51 (both changed by processor #168); `u_pp/u_aecp/u_dyn` -113;
  `u_pp/u_notify` -20 / -19.
- Input digest (the gate's `inputs()`): `af3597b2bacbe13bb2d871cc2fc3c061bbf3595c708929fdaa5a46de232419bd`, 127 files,
  6 images.
- Run: 06:03:14 to 06:48:24 (45.2 min), rc 0, Vivado peak 7,829 MB. `baseline.log` SHA-256
  `f999e306a9e6f15ae16e8091809f6f494d8e68a88642502a51e6b8f0acedac05`, 719,382 bytes.

Attribution against dev: dev `734eb780` was exported with the same recipe commands in its own clone. Its 127 route
inputs differ from the candidate's only in the six processor RTL files the pin changes: `hdl/acmp/KL_acmp_talker.sv`,
`hdl/acmp/KL_pp_acmp_listener.sv`, `hdl/acmp/pp_acmp_pkg.sv`, `hdl/aecp/KL_aecp_notify.sv`,
`hdl/packet_engine/KL_pp_tx_arbiter.sv` and `hdl/top/protocol_processor_top.sv`. Generics and all six memory images
are identical, firmware ROM and RAM inits included. Base inputs digest
`cbed58b4220fac2945f5f0895f017e7e24a558399e7d029398ecc562e1a73ecf`.

### Standalone endpoints and the re-baseline

Same clone and export as the route. An RTL elaboration supplies the 8x8 bound parameters, and each standalone run uses
the integrated 20 ns clock (`--integrated-clock`). The four runs were serial under the lock (06:54-07:38).

| Endpoint | Record (`bee1b0d7`) LUT / FF | Candidate LUT / FF | Delta | RAMB36 / RAMB18 / DSP / CARRY4 | WNS / WHS ns (ungated) | Gate |
|---|---:|---:|---:|---|---:|---|
| `ooc-1x1` | 23,179 / 19,779 | 23,314 / 19,821 | +135 / +42 | 16 / 3 / 8 / 1,500 (+6 CARRY4) | +3.884 / +0.159 | rc 0 |
| `ooc-8x8` | 30,135 / 27,380 | 30,211 / 27,451 | +76 / +71 | 21 / 5 / 8 / 1,895 (+6 CARRY4) | -1.942 / +0.159 | rc 0 |

- Both standalone figures equal the STOP lane's to the cell, at the same processor pin. Dev's merge did change 15 of the
  124 files the standalone script reads, but in the wrapper itself only a comment line of `hdl/milan/KL_pp_shadow.sv`
  (`073b0985`). The other 14 files and the two moved images (`alinx_ax7101_rom.init`, `gptp_ucode.hex`) are outside the
  synthesized wrapper. The bound parameters (`baseline_chparam.txt`) equal the STOP lane's at both shapes.
- The 1x1 standalone worst setup path is now `u_pp/u_talker/maap_stale_r_reg[1]` -> `u_pp/u_event_router/sel_r_reg[0]`,
  31 logic levels. The STOP section's attribution of the -3.562 -> +3.884 ns move to processor #166 was not verified
  against the record's own path (its reports are not available here) and is withdrawn.
- 1x1 sub-blocks (printed, not gated): `u_tx_slots` +131, `u_aecp/u_resp` -117, `u_notify` +77 / +17, `u_listener`
  +78 / +9. 8x8: `u_aecp/u_resp` -88, `u_srp` +84, `u_listener` +65 / +8, `u_talker` -62.
- Receipts: `rtl-8x8` 1.1 min, peak 4,193 MB, log `ddb8cfbf1d5b15438777b369329fe0ee70e0fb1d47bf847b351ee14419c6d925`
  (207,108 B). `ooc-1x1` 10.6 min, peak 4,938 MB, log
  `c0014ca69d6a266a3d10b3e5deece3d561111ecac1e6bb444ebd213beb2164fb` (314,014 B). `ooc-8x8` 32.1 min, peak 6,098 MB,
  log `eca23d349680a79272417578bb9b008d4ba7098f3ebc46c523b1c2788b394def` (319,840 B). All rc 0. Each standalone log has
  one `Synth 8-6901` (parent `crft_emit_en_w`), no `Synth 8-4445` diagnostic and no critical warning.
- Input digests: `ooc-1x1` `a8a05debfe69361a29f38ef7095627bcfa7c9e8b458c16fae26a848dbdf7e417`, `ooc-8x8`
  `23a6c117ab7b2c53ae863dd296b0146e9fe093f2929099352d9c54106670c2fc`. After all runs, the 24 image entries of the four
  `baseline_images.json` manifests rehash to their recorded digests.

**Re-baseline.** All three `check` runs passed against #696's first-draw record, every floor and the drop limit
included, so the records were written, as the ruling allows.

| Commit | Change | Generator / evidence |
|---|---|---|
| `9ac9f5ca1844e92fab0b0016c6c9707ee067bd37` | `syn/ooc/pp_resource_baseline.json`: the three `record` objects and their `measured` notes | `python3 syn/ooc/pp_resource_gate.py record <dir> --endpoint <e> --write` for each endpoint; then `check` against the new records rc 0 (x3), `check-baseline` rc 0. Only `record` and `measured` changed: identity, tolerance, floor and ceiling are byte-equal |
| `5c6f50eefa4c5545f052ec843363ace5e7936e8a` | documentation of the re-baseline | see "Changes in the resume" |

### Changes in the resume (file:line at the head, clause)

No processor file and no RTL, firmware or SoC source changed in the resume. The route met the floor, so the flow
decision's register boundary in `sw/litex/milan_soc.py` was not needed and was not added.

| File:line | Change | Clause / authority |
|---|---|---|
| merge `a1dfbfad` | dev `734eb780`; the five conflicts resolved as listed under "Merge" | resume step 1 |
| `scripts/port_docs.budget:21` | census header re-recorded by its writer | generator |
| `docs/design/MAILBOX_SPLIT.md:32` | contents entry: the four former processor differences are now checks | Milan v1.2 Table 5.36, 5.5.3.5.30, 5.5.4.2; IEEE 1722.1-2021 Table 8-3 (as in the section it summarises) |
| `syn/ooc/pp_resource_baseline.json` | three records and `measured` notes | `pp_resource_gate.py record --write`; the re-baseline rule (`docs/design/AREA_BUDGET.md:455-459`) |
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:8-13`, `:18`, `:36-118` | the current-record pointer, contents entry and the new section "Re-baseline of 2026-10-16, processor 2cbed0a9" | re-baseline rule |
| `docs/design/AREA_BUDGET.md:13`, `:111-116`, `:124-137`, `:149-155`, `:389`, `:429`, `:489-493` | record pointer, history (fifth measurement), headroom table, critical path, allocation arithmetic (wrapper at most 11,541 LUTs, 11,573 to remove, 50 %), the floor sentence (+0.215, fall 0.185), the ninth re-baseline | NFR-RES-01; resource gate policy (unchanged) |
| `docs/design/MARK_II_AREA_PLAN.md:56`, `:110`, `:658-659` | gate-comparison row, the inventory's record pointer, the comparison anchor (49,613 LUTs, 74/25) | D7 (Mark II compares against the last gate record) |
| `docs/reference/SUBMODULES.md:204-207` | the #708 adoption notes the re-baselined gate | acceptance 2 |

### Image build

The image is the measured route's own bitstream: the routed checkpoint of the run above
(`alinx_ax7101_route.dcp`), with the shipping Tcl's five bitstream properties and its `write_bitstream` line, copied
from the generated `alinx_ax7101.tcl` (SPI x4, `CONFIGRATE` 50, `CFGBVS` VCCO, 3.3 V). It ran under the exclusive lock.

| Image | Bytes | SHA-256 | DRC | Run |
|---|---:|---|---|---|
| `alinx_ax7101.bit` | 3,825,992 | `67078a9b29365e0f3d385d907ead1608d40d71dbd46a60c781db346e07ba2152` | 0 errors, 0 warnings, 0 critical warnings | 06:53:07-06:54:18, rc 0, peak 3,837 MB |

The flash side matches dev's build: `aem_desc.bin` (7,512 bytes, SHA-256 `4fc8d615...396d`) is byte-identical to the
dev `734eb780` shipping build's. `flashboot_layout.json` differs only by the two bitstream fields a `--build` appends.

**The shipping launcher's own build was started and then stopped by me.** That is
`bash sw/litex/build.sh ax7101`'s exact command, from its own preview in a clean clone, with only the output directory
moved. Its synthesis runs eight parallel Vivado workers of about 1.8 GB each, and the lane's anonymous memory reached
11.0 GB within three minutes, against the lane's 9 GB budget under its 12 GB cap. That is why the recipe synthesizes on
one worker. No result of that run is used. The bitstream above is the image of exactly the netlist and route the gate
measured. The shipping launcher's multi-worker synthesis is not reproduced here. The dev `734eb780` shipping build,
outside this lane, gives that flow's reference (+0.346 / +0.036 ns).

### Gates after the merge

Heads: `82227af0` is the tree every RTL, firmware and suite gate ran on. The final head `5c6f50ee` differs from it only in
`syn/ooc/pp_resource_baseline.json` and four Markdown pages (`git diff --name-only 82227af0 5c6f50ee`). The docs, record
and builder gates ran at `5c6f50ee`, and so did the two gPTP runs re-made in the continuation. Every gate ran in a clean
clone of its head, not in the lane worktree, except the quick read-only checks marked "lane".

| Gate | Head | rc | Result |
|---|---|---:|---|
| `check_submodule_docs.py`, `--selftest` | lane `a1dfbfad`+ | 0 / 0 | 6 exact gitlinks |
| `submodule_boundaries.gen.py --check` | lane | 0 | 6 exact gitlinks, decoded PNG |
| `check_port_contracts.py` (after `--write-budget`) | lane `435af429` | 0 | 3989 ports; every ratchet unchanged |
| `measure_naming.py --check` / `--write-budget` | lane | 0 / 0 | 95 identities, byte-identical |
| `ooc.sh --record-rom-digests` | lane | 0 | byte-identical ledger |
| `measure_test_evidence.py --check` / `--selftest` | lane | 0 / 0 | ratchet PASS (66 <= 77); 105/105 |
| `lint_rtl.py --check --self-test` | lane `82227af0` | 0 | 90 <= 90, 18 waived |
| `pp_resource_gate.py --selftest`, `check-baseline` | lane | 0 / 0 | |
| `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_resource_gate_mutants.py` (cpu 4) | lane | 0 / 0 / 0 | 192/192 gate mutants fail |
| `behave --no-capture -f plain` (`tests`) | lane | 0 | 14 features, 406 scenarios, 1,977 steps |
| `test_ctrl_firmware.py --require-rv32 --jobs 2` | lane `82227af0` | 0 | 61 arms; `acmpwalk` 127/127 |
| `fw_rv32_selftest.py --require-rv32` + `test_ctrl_firmware.py --require-rv32 --self-test --jobs 2` (rtl-fast's firmware commands; the union of the four campaign shards) | clone `82227af0` | 0 / 0 | RV32 17 checks; **520 mutants** caught, 937 `[ok]` arms, 0 escapes; 05:46-06:33; log SHA-256 `49be9ca209f5962fc9328e499ac4673b2d0325ada7a3a1d3ff4337bf30aa0580` (344,848 B) |
| `check_nvm_capture.py` | lane | 0 | PASS, seven controls |
| docs.yml `wire-accountability`, `docs-gates-0/1/2` (literal run steps) | clone `82227af0` | 0 | 70 run, 7 hosted-bookkeeping steps skipped, 0 failed |
| same | clone `5c6f50ee` | 0 | 70 run, 7 skipped, 0 failed (final head) |
| docs.yml `docs-check-no-git` | clone `82227af0` | 0 | 0 findings; feature status 0 findings |
| `gen_toc.py --check`, `--verify-anchors`, `check_doc_style.py`, `check_doc_paths.py`, `docs_check.py`, `check_em_dash.py --base 734eb780` | lane `5c6f50ee` | 0 | |
| `xvlog_gate.py --check` (exclusive lock) | clone `82227af0` | 0 | 0 findings == ratchet |
| `syn/yosys/run.sh --results` (full serial, all tops) | clone `82227af0` | 0 | **58/58 tops**; tap purity PASS; Yosys 0.66 `86f2ddeb` |
| `pp_resource_gate.py check` route-1x1 / ooc-1x1 / ooc-8x8 | measured `435af429` | 0 / 0 / 0 | see "Re-route" and "Standalone endpoints" |
| bitstream from the measured route | measured `435af429` | 0 | DRC 0 errors, 0 warnings |
| 63-suite sweep, shard 0/5 | clone `82227af0` | 0 | 11/11 suites, 12,514 checks, 0 failures, 0 timeouts |
| 63-suite sweep, shard 1/5 | clone `82227af0` | 0 | 13/13 suites, 35,539 checks, 0 failures, 0 timeouts |
| 63-suite sweep, shard 2/5 | clone `82227af0` | 0 | 12/12 suites, 424,667 checks, 0 failures, 0 timeouts |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` (elaborate.yml's command; host LiteX environment with the patch series via `MILAN_LITEX_PYTHON`) | clone `5c6f50ee` | 0 | "ALL GATES PASS EXCEPT 2 NOT RUN"; no elaboration arm skipped for a toolchain reason. Not run, by the bank's own records: gate 11, the historical calibration that needs the old mf48 build tree (as on #696), and gate 1b's `MAKEFLAGS += -e` mutation, which has nothing to detect on GNU Make 4.3 (CI's version too). 08:27-08:53; log SHA-256 `91be5601eb013fad90973c585e5231d2e9e2147e75d453fba8070ecdf9b6e11b` (122,002 B) |
| 63-suite sweep, shard 3/5 | clone `82227af0` | 0 | 13/13 suites, 1,672,577 checks, 0 failures, 0 timeouts; `tsn_fuzz` field campaigns ran (tsn-gen `deca300c`), no declared skip |
| 63-suite sweep, shard 4/5 | clone `82227af0` | 0 | 14/14 suites, 41,952 checks, 0 failures, 0 timeouts |
| **63-suite sweep, total** (`bash scripts/run_all_suites.sh <logs> --shard i/5`, i = 0..4, two clean clones) | `82227af0` | 0 x5 | **63/63 suites, 2,187,249 checks, 0 failures, 0 timeouts**. The union of the five shard lists equals `run_all_suites.sh --list` (63), with no duplicate. Each shard's preflight (cancellation controls) passed. Interpreter: CI's CPython 3.12.3 |
| processor sweep: `bash scripts/run_suites.sh` in a clean processor clone, sv2v v0.0.13 first on PATH (see below) | processor `2cbed0a9` | 0 | UPC map and M9 opcode gates PASS; **34/34 suites, 1,029,620 checks, 0 failing**; 09:39-10:09; log SHA-256 `b1205c5d8cfb979eb93a54b692587924790bdf4c4de46ddf82547223d37c36f5` |
| physical gPTP suite: rtl.yml `physical-gptp`'s run steps (`suite_shards.py --selftest`; `run_all_suites.sh --physical-gptp --list` is `milan_dp_gptp`; `env -u SUITE_TIMEOUT VERILATOR_JOBS=2 scripts/run_all_suites.sh <logs> --physical-gptp`; `suite_tally.py <logs> --quiet --expect-suite-root tb/verilator --physical-gptp`; control logs copied) | fresh clone `5c6f50ee` | 0 | **PASS, 197 checks, 0 failures**: physical leg 143/0 (`RESULT: PASS`, simulation exit 0, 3,599.96 s), setup abort 6/0, no-TX accounting 20/0, no-Pdelay accounting 14/0, recentre controls 14/0. The driver's own suite deadline applied (5,400 s, `SUITE_TIMEOUT` unset). 16:05:10-17:22:56, driver 4,664.51 s; preflight cancellation controls passed. CI's CPython 3.12.3. Suite log SHA-256 `e78b7adbfe2dc0d51a58cd4c62890b964eaacc191682fb84f45dee864d5becf3` (110,476 B) |
| gPTP processor: `make -j8 contract tb lint` (the #661 lane's command, with `-j8`), `TSAGEN_DIR` at the workflow's tsn-gen `deca300c` | fresh clone of `Mister-M-alt/FPGA-gPTP` at the gitlink `e4869fd0` | 0 | PHC contract PASS; ucpu 768/0; parser 337/0; engine 1613/0 in each of its three passes; gaskets 81/0; tsngen 290/0 (tsn-gen cross-check ran, no SKIP); `bench/arty` tag test PASS; lint (engine and bench) clean. Mutation arms (tallies include each arm's unmutated pass): parser 9/0 (8 mutants), engine 34/0 (33), gaskets 5/0 (4), tsngen 4/0 (3), so **48 mutants caught, 0 escapes**. 16:05:11-16:30:52; log SHA-256 `8cb9b622e9106e4c262349f83983ce41f8e15e0fd7076b1e751eb637b4f16968` (44,943 B) |

**Dev since the merge.** `origin/dev` moved after the merge, from `734eb780` to `8eacc408` (checked with `git ls-remote`
at 16:05). It adds two first-parent merges: PR #745 (CI replay OOM refusal and memory-bounded census, #744) and PR #753
(the board deployment guide, with the pinned LiteX install in README and QUICKSTART). Its 14 changed files are CI
templates, workflows, `scripts/act_ci.py`, `scripts/check_baremetal_only.py`, `scripts/check_doc_style.py`, two CI
helper scripts and six Markdown pages. None is an RTL, firmware, configuration or image input. The resume assignment
named `734eb780`, so the lane was not merged again. A trial merge was made in a scratch clone, never in the lane: it
merges `5c6f50ee` with `8eacc408` as `a7c29052`, without conflict (`MAILBOX_SPLIT.md` auto-merges: dev's hunk is at
`:1033`, far from the lane's). On that trial tree, these all exit 0:

- `gen_toc.py --check` and `--verify-anchors`;
- `check_doc_style.py` (23 documents, including dev's new guide);
- `check_doc_paths.py`, `docs_check.py` and `check_submodule_docs.py`;
- `check_em_dash.py --base 8eacc408` (0 findings over 192 added lines);
- `check_baremetal_only.py --check` and `--selftest`.

The candidate-merge validation that CONTRIBUTING requires is still owed at merge time.

**Processor sweep and sv2v.** A first processor sweep (`protocol-processor/scripts/run_suites.sh`) ran in the gate
environment, where the parent's pinned sv2v 0.0.12 is first on PATH. It failed one arm: `tb/nvm_port`'s optional Yosys
guard (`elab_bounds.sh:83-106`) reported `YOSYS FAIL MAX_PAYLOAD_P=65528 failed, but not at the guard's $finish`.
The arm runs only when sv2v and Yosys are both on PATH, and the processor's CI `suites` job installs neither. Its
`portability` job installs sv2v's latest release, v0.0.13. Neither `tb/nvm_port` nor `KL_pp_nvm_port.sv` changes in
`2ad2f845..2cbed0a9`. The #661 lane recorded the same sv2v 0.0.12 lowering. Controls, each `make elab` in a clean
processor clone:

| Pin | sv2v 0.0.12 | sv2v 0.0.13 |
|---|---|---|
| `2ad2f845` (old) | rc 2, the same `YOSYS FAIL` | rc 0 |
| `2cbed0a9` (adopted) | the same `YOSYS FAIL` (first sweep) | rc 0, `YOSYS OK ... stops at the guard's $finish` |

So the failure is the sv2v version's, present at the old pin too, and not the adoption's. The first sweep was stopped
after that suite to keep two Verilator streams at most, and its partial log is kept apart. The counted processor sweep
runs at `2cbed0a9` in a clean clone with sv2v v0.0.13 first on PATH: `sv2v-Linux.zip` from release v0.0.13, 2,197,565
bytes (the release API's size), SHA-256 `552799a1d76cd177b9b4cc63a3e77823a3d2a6eb4ec006569288abeff28e1ff8`; binary
`b80a8ac6212aa72a196d9d6129cda35f16dbfa799ec61848c46321f845b6b635`. The parent's own gates stay on their pinned 0.0.12.

**Concurrency.** At times a third Verilator user ran beside the two sweep streams, above the two-builds limit:

- 08:27-08:53, the builder elaboration bank, whose elaborations use Verilator;
- 09:03-09:24, the physical gPTP suite beside shards 3 and 4, then the first processor sweep. That physical run is the
  one the host shutdown cut, and it is not counted.

The memory coordinator has watched every heavy job since 07:44. Anonymous memory never crossed its 8.9 GB pause line,
so it paused nothing. Since 09:24 at most two Verilator streams run at a time.

In the continuation, the only work was the two gPTP runs, side by side: two Verilator streams, no Vivado job. The lane
unit's memory peaked at 2,668,163,072 bytes (`memory.peak`, page cache included); `memory.events` shows oom 0.

Environment notes for this resume:

- The 63-suite sweep's new process-ownership guard (`scripts/owned_process.py:62`, from dev) requires `os.pidfd_open`,
  and the standalone CPython 3.12.3 build lacks it. `run_all_suites.sh` refuses it with `REFUSED: ... unsupported process
  facilities` (exit 2). The sweep therefore uses hosted CI's own CPython 3.12.3 build: actions/python-versions release
  `3.12.3-11057844995`, asset `python-3.12.3-linux-24.04-x64.tar.gz`, the URL setup-python's manifest names for Ubuntu
  24.04. It is 121,683,532 bytes (equal to the release API's size), SHA-256
  `07ef2452a390e76505b5a26b37bae7f88bc260926ca70ae88cb679003ab42279`, kept in scratch only. The venv has the same 16 pinned
  packages as the gate venv (`pip freeze` identical).
- A first sweep launch under `nohup` stopped in all three of its shards' preflight (rc 2, no suite run). `nohup`
  makes SIGHUP ignored for the whole tree, so the cancellation controls' `hard-HUP` case
  (`scripts/test_suite_cancellation.py`) could not stop its sweep shell and timed out. That is an artefact of the
  launcher. The sweep was relaunched under `setsid` alone, with no inherited ignored signal except SIGQUIT, which no
  control uses. The preflight then passed. The aborted attempt's logs are kept apart and not counted.
- Memory: anonymous memory in the lane's unit briefly exceeded the 9 GB target twice. It reached 9.33 GB while the
  candidate route ran beside the docs builder legs and the firmware campaign; a watchdog paused the campaign twice for
  under 10 s each. It reached 11.28 GB at the campaign's end, beside the route's placement. There was no OOM event
  (`memory.events` oom 0). After that, no heavy job ran beside a route; the sweep runs beside synthesis-only Vivado jobs
  under a watchdog that pauses its process tree above 8.9 GB.

## Status at the STOP (2026-10-10, kept for history)

**STOP.** The adopted image's shipping route misses the WNS floor. This is one of the assignment's STOP conditions,
"any route below the floor", and it also fails #708 acceptance 2.

- `route-1x1`, recipe default directives: WNS **+0.025 ns** at both slow corners, against the **+0.030 ns** floor.
- `pp_resource_gate.py check` exits **1**: `REGRESSION: below the floor 0.03`.
- The fall from the record's +0.299 ns is 0.274 ns, which also exceeds the 0.25 ns timing-fall limit.
- The route is complete: no unrouted net and no routing error. WHS is +0.015 ns, which meets its 0 ns floor.

After the STOP I did not start any new work. Not run: the 61-suite sweep, the processor and gPTP sweeps, Yosys, the
vendor-syntax gate, the builder elaboration bank, the two alternative directives, the bitstream/image build and the
re-baseline (`record --write`). The gate record in `syn/ooc/pp_resource_baseline.json` is unchanged. Runs already in
flight when the route finished were allowed to complete and are reported below.

- Issue: kebag-logic/milan-fpga #708; [assignment](https://github.com/kebag-logic/milan-fpga/issues/708#issuecomment-6094788195);
  [TAKEN](https://github.com/kebag-logic/milan-fpga/issues/708#issuecomment-6094845313);
  [STOP](https://github.com/kebag-logic/milan-fpga/issues/708#issuecomment-6095805419) at head `99a5a2ac`.
- Branch `708-pin3`, base dev `554e61d299ef7ddb5aca6fb9ce0e6a6cd076d8cb` (dev unmoved at 10:00).
- Head: see "Commits"; the worktree is clean, and nothing has been pushed.
- Roles: executor [A585]; reviewers [R588] (internal) and [R589] (external).
- Origins verified: parent `https://github.com/kebag-logic/milan-fpga.git`; processor
  `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`. Every command inside the processor
  was preceded by `git -C protocol-processor rev-parse --show-toplevel` equal to that directory.

## Commits

| Commit | Step | Gate evidence (all rc 0 unless stated) |
|---|---|---|
| `75a28523eeb00f8c46477db62e7bd98a2afd4965` | gitlink `2ad2f845` -> `2cbed0a9` only | processor checkout clean at `2cbed0a9` |
| `df70d8f0355bb2703cd110a5f4fb96afa31b5dee` | `parent-name-evidence.patch` (lane pp170) | `measure_test_evidence.py --check` and `--selftest` (105/105); without the patch `--check` exits 1, `protocol-processor/tb/name_state/mutants.py: UNEXPLAINED` |
| `afc0b831aef9201c969ba7b0bbd0ac8a05ae1aea` | F3 ACMP normalisation retired; MAILBOX_SPLIT and ctrl README | control-firmware bank PASS; campaign 471/471; old-pin control fails as designed (below) |
| `c673ff85166b91783ba5a96534a37124f0464b4a` | ROM digests, pin page, boundary diagram, port census re-recorded | record gates below |
| `99a5a2ac6fbbf1268f57008b42b5b26ccf6ae731` | F5 AECP wire README: single-interface reference is a `2ad2f845` checkout | docs gates |

One-line subjects, no body, no trailer. The configured author identity was not changed.

## Processor range and parent-visible changes

`git rev-list --count 2ad2f845..2cbed0a9` is 49. The first-parent merges are listed below. The processor top-level and
submodule checkout were proved at `2cbed0a9`, and no processor file was edited. The adapted parent has no processor
change beyond the gitlink.

| PR | Merge | Issue | Parent-visible result |
|---|---|---|---|
| [165](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/165) | `c9f74b68` | #69 | Top gains `parameter int unsigned N_AVB_IF_P = 1` and `input wire [1:0] rx_if_index_i = 2'd0`. `KL_pp_shadow.sv` names its connections (`hdl/milan/KL_pp_shadow.sv:1079`, instance at `:1109`) and leaves both at their defaults; lint is identical to base (90 <= 90, 18 waived, PINMISSING 15 at both). **Not in #708's list**; declared in TAKEN |
| [166](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/166) | `ed340b9b` | #163 | Registered withdraw mask (+1 cycle to the arbiter's pre-start abort), parallel arbiter ranking. No port, parameter or register change. **Not in #708's list**; declared in TAKEN |
| [169](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/169) | `09e357fb` | #167 | Coincident probe cancel and TIME_LIMITED drain: both cancels sent. No port change |
| [171](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/171) | `336e9f36` | #168 | ACMP fields corrected (below). `acmp_bound_vlan_o` stays 12 bits per sink |
| [172](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/172) | `2cbed0a9` | #170 | Tests and docs only (`tb/name_state`) |

Processor RTL that changed: `hdl/acmp/KL_acmp_talker.sv`, `hdl/acmp/KL_pp_acmp_listener.sv`, `hdl/acmp/pp_acmp_pkg.sv`,
`hdl/aecp/KL_aecp_notify.sv`, `hdl/packet_engine/KL_pp_tx_arbiter.sv` and `hdl/top/protocol_processor_top.sv`. These are
exactly the files by which the candidate's resource inputs differ from base (see "Resource attribution").

## Changes (file:line, clause)

| File:line (at head) | Change | Clause |
|---|---|---|
| `scripts/measure_test_evidence_readers.py:21` | pp170 patch, applied without context repair (`git apply --check` clean; patch SHA-256 `2ec42e1fb5bba4cf620db85bad880ae485a3d4042dd7bc833da4439c38b2b007`, 701 bytes, from `c8ef8d9d:review-evidence/pp170-r1/author/parent-name-evidence.patch`) | n/a (evidence classification) |
| `sw/firmware/ctrl/test/acmp_walk.cpp:42-65` | header: "THE FORMER DIFFERENCES"; each of LD1 to LD3 is now a control for the old answer | as below |
| `sw/firmware/ctrl/test/acmp_walk.cpp:435-441` | **LD1**: the `std::memset` normalisation of the processor's UNBIND_RX_RESPONSE talker fields is removed; the frame is compared raw; a named check fails if `talker_entity_id`/`talker_unique_id` are not 0 (the fabric echo returning) | Milan v1.2 Table 5.36 |
| `sw/firmware/ctrl/test/acmp_walk.cpp:443-447` | **LD2**: the record normalisation (`acmpsta = before`) is removed; a named check fails if the processor zeroes the status after TMR_RETRY with the talker discovered | Milan v1.2 5.5.3.5.30 step 2 (5.3.8.6) |
| `sw/firmware/ctrl/test/acmp_walk.cpp:523-540` | **LD3**: `ST_NOAUTH == 13` becomes `== 16`; the byte patch before the compare is removed, so the two refusals compare byte for byte | IEEE 1722.1-2021 8.2.1.5, Table 8-3 (16 CONTROLLER_NOT_AUTHORIZED; 13 is TALKER_MISBEHAVING) |
| `sw/firmware/ctrl/test/acmp_walk.cpp:797-799` | **TD1** message: the processor's talker suite now requires TALKER_UNKNOWN_ID too (`tb/acmp_talker/sim_main.cpp`, "TD1 invalid disconnect"); the firmware check is unchanged | Milan v1.2 5.5.4.2 step 1, Table 5.44 |
| `docs/design/MAILBOX_SPLIT.md:759-789`, `:805` | "Differences from the processor": none remain; the four former ones listed as controls | same clauses |
| `sw/firmware/ctrl/README.md:238-250` | same, in the firmware README | same clauses |
| `sw/firmware/ctrl/aecp/README.md:125-137` | F5 AECP wire reference: `aecp_wire.py` content-pins its single-interface reference to `2ad2f845` (`sw/firmware/ctrl/test/aecp_wire.py:17`, unchanged, deliberately not the gitlink: the two-interface reference `c9f74b68` was never a gitlink). The README's `--reference protocol-processor` would now be refused by that content check, so it names a checkout of `2ad2f845` | n/a |
| `docs/reference/SUBMODULES.md:25`, `:188-205` | pin row, and the #708 adoption table | as listed |

Old-fabric control (`--require-rv32 --jobs 2`, the candidate `acmp_walk.cpp` applied to a clean dev `554e61d2` clone
whose processor is `2ad2f845`, then restored): rc 1. Every new control fails there, and by name:

- LD1 fails in all eight `UNBIND_*` cells, each with "the processor's talker fields are 0 ... not the command's echo".
  Each cell also fails "frame 0 byte for byte".
- LD2 fails in `TMR_RETRY_PWT_disc` with "keeps the status the retry was for", and its record compare shows
  `PWD 2 5 want PWD 2 0`.
- LD3 fails with "which is 16 ... not 13" and with "the two refusals agree byte for byte".

At the adopted pin, before the edit, the unchanged walk failed exactly on the old encodings: LD1 in eight cells, LD2 in
one, LD3 once. Nothing else differed (VLAN width, probe controller and retry status all agree). After the edit,
`acmpwalk` passes 127/127.

No other parent test encoded the old #168 behaviour among those run here. The firmware bank, the firmware campaign and
BDD pass, and the walk was the only failing arm at the new pin. The Verilator suites were not run (STOP), so this is not
established for them. A static search found only the not-discovered retry branch (`tb/verilator/milan_dp/sim_nxn.cpp`
G3, 5.5.3.5.30 step 1), which is unchanged.

## Re-recorded records (generator)

| Record | Generator | Result |
|---|---|---|
| `syn/yosys/rom_digests.tsv:17-18` | `bash syn/yosys/ooc.sh --record-rom-digests` | two `2cbed0a9` rows; LTN `23cc67ee...e956` and microcode `518b900c...37f8`, both equal to the `2ad2f845` rows (ROMs unchanged) |
| `docs/reference/SUBMODULES.md:25` | pin row rewritten from `check_submodule_docs.gitlink_pins()` (no dedicated writer, as in #682) | `protocol-processor` -> `2cbed0a987c1e68402658d69459ab7e5aa571adc` |
| `docs/diagrams/submodule_boundaries.{drawio,svg,png}`, `PNG_MANIFEST.json` | `python3 docs/diagrams/submodule_boundaries.gen.py` | pin `2cbed0a987c1`; raster inspected |
| `scripts/port_docs.budget:21-22`, `:82` | `python3 scripts/check_port_contracts.py --write-budget` | processor ports 1759 -> 1761 (+`rx_if_index_i`, +`KL_aecp_notify.rgy_port_i`); unjustified processor 4 -> 3 (`u_normalizer.rx_if_index_i` literal binding left); hdl 2079 -> 2089 is dev's stale census header (base already measures 2089); ratchets unchanged |
| `scripts/naming.budget` | `python3 scripts/measure_naming.py --write-budget` | byte-identical (95 identities) |
| `syn/ooc/pp_resource_baseline.json` | `pp_resource_gate.py record --write` | **not written**: the route fails the floor (STOP) |

Record gates at `c673ff85`: `check_submodule_docs.py` and `--selftest`, `submodule_boundaries.gen.py --check` and
`--selftest`, `check_diagram_pngs.py` (6 rasters), `check_port_contracts.py`, `measure_naming.py --check`, `docs_check.py`,
`check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --check` and `check_em_dash.py --base 554e61d2`, all rc 0.

## Resource before/after and route timing

Recipe: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, with `--single-thread-synthesis` and `--integrated-clock`.
Toolchain: Vivado v.2026.1 build 6511674, `xc7a100tfgg484-2`, default seed. Every run took the exclusive
`$VIVADO_LOCK` around Vivado only, and ran in a fresh directory of a dedicated clone of the commit under
measurement, outside the lane worktree. "Before" is the gate record (`a5ca6e51`, processor `2ad2f845`).

| Endpoint | Figure | Record (before) | Candidate (after) | Delta | Gate |
|---|---|---:|---:|---:|---|
| `route-1x1` | LUT | 50,267 | 49,787 | -480 | ok |
| | FF | 54,413 | 54,172 | -241 | ok |
| | Slice (of 15,850) | 15,779 | 15,831 | +52 | ok (19 free; record 71) |
| | RAMB36 / RAMB18 / tiles | 74 / 27 / 87.5 | 74 / 27 / 87.5 | 0 | ok |
| | DSP / CARRY4 | 14 / 3,402 | 14 / 3,390 | 0 / -12 | ok |
| | **WNS ns** | +0.299 | **+0.025** | -0.274 | **REGRESSION: below the floor 0.03** |
| | WHS ns | +0.031 | +0.015 | -0.016 | ok |
| `ooc-1x1` | LUT / FF | 23,179 / 19,779 | 23,314 / 19,821 | +135 / +42 | PASS (rc 0) |
| | RAMB36 / RAMB18 / DSP / CARRY4 | 16 / 3 / 8 / 1,494 | 16 / 3 / 8 / 1,500 | 0 / 0 / 0 / +6 | |
| | WNS / WHS ns (ungated) | -3.562 / +0.159 | +3.884 / +0.159 | +7.446 | cause not established (attribution withdrawn in the Resume) |
| `ooc-8x8` | LUT / FF | 30,135 / 27,380 | 30,211 / 27,451 | +76 / +71 | PASS (rc 0) |
| | RAMB36 / RAMB18 / DSP / CARRY4 | 21 / 5 / 8 / 1,889 | 21 / 5 / 8 / 1,895 | 0 / 0 / 0 / +6 | |
| | WNS / WHS ns (ungated) | -2.278 / +0.159 | -1.942 / +0.159 | +0.336 | |

Route corners (`kl_timing_grade_reports`; commercial 0-85 C, fixed Slow/Fast models):

| Corner | WNS ns | WHS ns |
|---|---:|---:|
| Slow_0C | +0.025 | +0.102 |
| Slow_85C | +0.025 | +0.102 |
| Fast_0C | +1.633 | +0.015 |
| Fast_85C | +1.633 | +0.015 |

The route is complete: 100,885 of 100,885 routable nets routed, 0 routing errors, no negative-slack path at any corner,
the IOB pack check passes, and the log has no CRITICAL WARNING. `Synth 8-4445` appears only as the echoed
severity-setting command, which the recipe excludes. `Synth 8-6901` appears once, the known parent
`crft_emit_en_w` (`hdl/milan/milan_datapath.sv:3177`); the processor has none.

Worst setup path: `FSM_sequential_subfragments_fsm0_state_reg[0]` -> `milansoc_tmod0_reg[10]/CE`, clock
`milansoc_crg_clkout0` (10 ns). Data path 9.808 ns, of which 2.151 ns is logic and 7.657 ns (78 %) is routing. It has
10 logic levels. This is a SoC-side path, not a processor or wrapper path. Worst hold path:
`milan_datapath/csr/g_pp_csr.pp_nvm_wdata_r_reg[15]` -> `milan_datapath/pp_shadow/u_nvm/img_base_r_reg[15]/D`,
+0.015 ns. The record's worst setup path was SoC-side too, from `milansoc_write_w_buffer_level0_reg[1]`.

Route sub-block movements against the record, which the gate prints without gating: wrapper -530 LUT / +18 FF; `u_pp`
-554 / +18; `u_pp/u_aecp` -458; `u_pp/u_aecp/u_dyn` -399; `u_pp/u_listener` +88 / +12; `u_pp/u_aecp/u_d3` +84;
`u_pp/u_notify` -77 / -14. Standalone 1x1: wrapper +135 / +42; `u_pp/u_tx_slots` +131; `u_pp/u_aecp/u_resp` -117;
`u_pp/u_notify` +77 / +17; `u_pp/u_listener` +78 / +9. The processor PRs' own fresh 1x1 deltas were #169 +11/+20,
#171 +29/+14, #166 -39/+10 and #165/#172 0/0.

| Run | Start | End | rc | Log SHA-256 | Bytes |
|---|---|---|---:|---|---:|
| `route-1x1` | 09:00:41 | 09:51:05 | 0 | `6e2fda6319069d242c7395fa4789783addabc4f7c9fcdf6e989179d8b24c8ba5` | 794,928 |
| `rtl-8x8` (parameter binding) | 09:51:05 | 09:52:18 | 0 | `fd95bea35edd1ead92ca891a140c997c9eb51b74e6a30ba68838f289ccee3d39` | 206,984 |
| `ooc-1x1` | 09:52:18 | 10:06:36 | 0 | `99ad1dd483a66a1b0eaae3307bc1cac471d2bd472ea2990447b4c863ae1af1b6` | 313,396 |
| `ooc-8x8` | 10:06:36 | 10:43:49 | 0 | `fcc9f2d74e840780352a778c0c4e3bc650e7cb174d19967eb36ff734725989ff` | 319,227 |

Input digests (the gate's own `inputs()`): candidate route `c0ad97e713b43e93d284ee3ac979252af34ea54f7df9d025a473c8303c4b477e`;
candidate ooc-1x1 `b5a743c6df93629d7eddec501fd97bbcf2685f8a9eeab3758ad88c9caf8f31d4`; candidate ooc-8x8
`971c5617ad83673dc4ff6a56cffbae1140fcc9489cf7c7ce23a86b0c3acd767a`. After all runs, the 24 image entries of the four
`baseline_images.json` manifests rehash to their recorded digests. Each standalone log has one `Synth 8-6901` (the
parent `crft_emit_en_w`) and no `Synth 8-4445` diagnostic. `pp_resource_gate.py check-baseline` rc 0 (record
unchanged).

### Resource attribution

- Candidate (`75a28523`) and base (`554e61d2`) exports: of 127 route inputs, only the six processor RTL files above
  differ. Generics and all six images are identical: `alinx_ax7101_mem.init`, `alinx_ax7101_rom.init`,
  `alinx_ax7101_sram.init`, `gptp_ucode.hex`, `ltn_rom.hex` and `ucode.hex`.
- Base and a fresh export of the record's own commit `a5ca6e51` (processor `2ad2f845`) differ only in
  `hdl/ieee8021q/filtering/rx_mac_filter.sv`. That change (`2aa74ab9e`, #651) touches comment lines only.
- A fresh export of `a5ca6e51` digests to `d1abd61e...` rather than the recorded `95a6cc95...`. The record lane's
  generated `alinx_ax7101.v` (raw 1,763,070 bytes) is gone, and its manifest keeps only that raw digest. So the residue
  lies in the generated netlist, and the export's repository files and images all match the record lane's manifest.
  This is the same kind of fresh-export digest movement #682 documented.
- The 8x8 standalone script binds parameters identical to the record's (`baseline_chparam.txt` equal at both shapes).
  The 8x8 binding here comes from RTL elaboration (recipe, "Standalone measurements"). The record used a full
  integrated 8x8 synthesis.

So the movement against the record belongs to the adoption, as a placement result of the processor change in an image
with 19 free slices. A base route was not run; the comparison is against the record.

## Capture comparison

Not re-measured, because the firmware digest did not move:

- `sw/firmware/milan_baremetal/milan_baremetal.c` SHA-256 is `a73ecc25c77bfb7c4e1c2c711d72f0b560dd7e8d18cde92f40e67efcc84f0eb3`.
  That is the receipt's `product_firmware_sha256` in `tb/verilator/nvm_capture_cpu/measurements.json`.
- No file under `sw/firmware/milan_baremetal`, `tb/verilator/nvm_capture_cpu` or `configs` changed (`554e61d2..HEAD`).
- The shipping image's firmware ROM and init images are byte-identical between base and candidate.
- `python3 scripts/check_nvm_capture.py` rc 0: "PASS: capture census, clocks, both timing arms and receipt agree", with
  all seven controls detected.

## Gate table

Environment (scratch only, nothing in the output directory):

- Gates: CPython 3.12.3 venv with the repository's hash-pinned Markdown and HDL-reference requirements; GNU Make 4.3,
  built from the verified GNU tarball; Verilator 5.050 (pinned); sv2v v0.0.12 (CI's pinned zip, sha256-verified); the
  pinned RV32 SDK, freshly installed and verified by `scripts/ci_rv32_sdk.py`; tsn-gen at the workflow's
  `TSN_GEN_REV deca300c`.
- Host compiler: GCC 16.2.1 with GoogleTest 1.18.0. CI uses the distribution's packages.
- Measurements: the LiteX venv plus the same SDK.

| Gate | Head | rc | Result |
|---|---|---:|---|
| `scripts/measure_test_evidence.py --check` / `--selftest` | `df70d8f0` tree | 0 / 0 | PASS; ratchet 71 <= 77 (base 70: the new `tb/name_state` suite) |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 2` | `afc0b831` tree | 0 | PASS, `acmpwalk` 127/127 |
| same, before the walk edit, at the new pin | `df70d8f0` | 1 | expected: LD1 x8, LD2, LD3 |
| same, candidate walk on old pin `2ad2f845` (control) | dev + walk | 1 | expected: each control fails by name |
| `fw_rv32_selftest.py --require-rv32` and `test_ctrl_firmware.py --require-rv32 --self-test --jobs 2` (rtl-fast firmware-unit commands) | `afc0b831` | 0 / 0 | RV32 self-test 17 checks; **471/471** mutants, 843 `[ok]` arms, 0 escapes; 09:21:30-10:03:07; log SHA-256 `d5b95dee9b6b3f929df78196244d3c627f898271aadbf271ff28813c3e3b4833` (283,646 B). Its temporary root defaulted to `/tmp` (344 MB at peak, removed by the script); later runs set `TMPDIR` to scratch |
| `python3 scripts/lint_rtl.py --check --self-test` | `df70d8f0` | 0 | 90 <= 90, identical findings to base |
| ROM digest generator, record gates, docs gates | `c673ff85` | 0 | see "Re-recorded records" |
| `python3 scripts/check_nvm_capture.py` | `99a5a2ac` | 0 | PASS |
| `behave --no-capture -f plain` (in `tests`) | `99a5a2ac` | 0 | 14 features, 404 scenarios, 1,968 steps |
| docs.yml `docs-check` (46 run steps) and `wire-accountability` (2), literal bodies | `99a5a2ac` | 0 | 48/48 rc 0 under GNU Make 4.3. Two `sudo apt` installs substituted: rsvg-convert already on the host; sv2v 0.0.12 already installed in scratch from the same verified zip |
| docs.yml `docs-check-no-git` | `99a5a2ac` (`git archive` copy) | 0 | 0 findings; feature status 0 findings |
| `pp_resource_gate.py check ... --endpoint route-1x1` | image of `75a28523` (= head) | **1** | **MATERIAL REGRESSION, WNS below the floor** |
| `pp_resource_gate.py check ... --endpoint ooc-1x1` | same | 0 | PASS |
| `pp_resource_gate.py check ... --endpoint ooc-8x8` | same | 0 | PASS |
| `pp_resource_gate.py check-baseline` | `99a5a2ac` | 0 | `baseline PASS: 3 endpoints` (record unchanged) |
| 61-suite sweep, processor sweep, gPTP, Yosys, xvlog, builder elaboration, render campaign, alternative directives, image build | | not run | STOP |

The image inputs at `99a5a2ac` equal those at `75a28523`. Commits after the gitlink touch only scripts, tests, docs and
records, none of them read by the measured build; the input digest is recomputed from each measured clone's own files.

## Decision needed (for the manager, not taken here)

The default-directive route of the adopted image is 0.005 ns under the +0.030 ns floor. It also exceeds the 0.25 ns
fall limit, with 19 slices free. The worst path is SoC-side and 78 % routing. Possible routes forward each need a ruling:

- The repository's other two placement directives, `AltSpreadLogic_high` and `ExtraTimingOpt`. CONTRIBUTING's
  3-directive discipline applies, but a non-default directive changes the gate's flow identity.
- A placement or seed change.
- A processor-side change.

Whether a repeat of the same recipe reproduces +0.025 ns was not measured.

Nothing was weakened, and no record was written.

## Artifacts

Small receipts are copied to `evidence/` beside this file. These include the three gate outputs, the route status,
corner grade, negative-slack and utilization reports, the IOB pack check, the capture check, lint, the three per-file
route input manifests, the docs workflow receipts (48 steps, with commands, rc, log digests and the two substitutions),
the walk diff, the old-pin and new-pin failure lines, and the BDD tail.

The resume's receipts are in `evidence/resume/`:

- the three endpoints' `check` outputs, before and after `record --write`;
- the per-file input manifests of the candidate route, dev's route and the two standalone endpoints;
- the corner grade and worst paths, the port-census diff, the capture check, `check-baseline` and `xvlog`;
- the gPTP processor's full `make` log;
- the physical gPTP suite's log, driver output and control logs (`evidence/resume/physical-gptp/`);
- the trial-merge gate outputs (`trial-*.log`).

Larger artifacts stay in the lane's scratch area, outside this directory. All paths below are relative to that scratch
root:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `meas/cand/ax7101/gateware/alinx_ax7101_route.dcp` | 108,612,014 | `51ae0de13b8ccfcbdbdeae40944cb29607363c5c15ca7acb139d379a5f7e9729` |
| `meas/cand/ax7101/gateware/alinx_ax7101_synth.dcp` | 88,774,568 | `62659aaa188651ea163d82ddbcf1559317ab252055200f1a621714cd7da73b49` |
| `meas/cand/ax7101/gateware/baseline.log` | 794,928 | `6e2fda6319069d242c7395fa4789783addabc4f7c9fcdf6e989179d8b24c8ba5` |
| `meas/cand/ax7101/gateware/alinx_ax7101_signoff_all_timing.rpt` | 1,340,610 | `813aa5a7b2f252d2ea6a8261fc12e83069c725746c1e35fb7538643c400d3346` |
| `meas/cand/ax7101/gateware/baseline_hierarchy.rpt` | 46,405 | `83404e6483dc24fae54dbcb8ee786f55f684aaada285b93fc6bf6644b30220a5` |
| `meas/cand/ax7101-ooc/baseline_synth.dcp` | 8,925,791 | `7889ca32a052264fa5607b442d11e1aae3c63149be234b6a4e987e8146057792` |
| `meas/cand/ax8x8-ooc/baseline_synth.dcp` | 11,365,642 | `2b09ebf83cece6305473e31e96122ea7424558912560379f3d69c775d5102395` |
| `gates/fw-ctrl-selftest.log` | 283,646 | `d5b95dee9b6b3f929df78196244d3c627f898271aadbf271ff28813c3e3b4833` |
| `fw/post.log` (bank at the walk edit) | 67,894 | `92cd3033d989eae83a9b64f5b0a815e6dc2484f9b83c2a6c643db6e0220b698c` |
| `fw/oldpin.log` (old-pin control) | 72,467 | `99ef0fca8bc55b798bdcb194ec98768c27c92d0dc8f0234ee05b7013adf6f1b3` |
| `fw/pre.log` (unchanged walk, new pin) | 69,074 | `d2c7492044a4b212b1a37ed483905b03739342fb1563eb07b31af679524e66cd` |
| `docs-wf/run1/steps/docs-check-25.log` (builder gates) | 102,154 | `7e7b9fff1eabb17d2387c9ce858d99048181b00629ca38b1e5463d1c1a1145a7` |

The three measurement clones (`meas/cand-src` at `75a28523`, `meas/base-src` at `554e61d2` and `meas/rec-src` at
`a5ca6e51`) each still carry the recipe's untracked `sw/builder/out` link, by design for a measurement clone. `base-src`
was restored after the old-pin control and is clean apart from that link.

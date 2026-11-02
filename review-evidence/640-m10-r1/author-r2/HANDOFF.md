# HANDOFF - [A720l] issue #640, PR #835 round 2 (docs only)

Status: REVIEW READY (2026-11-02). All 55 rc files read 0. Head 30eb4834e0d258668a7bdfece187f9d7d9fccd0b (tree 81f7e650087b8445b45b6fec2f1c8921f7e48626), on dev 503bc97c. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-charter-followup. Started at 3f8ed303 (640-a720k's head, PR #835's round 1 head). `git merge-base HEAD origin/dev` is 503bc97cd4f24ad07596c17e7188f2024617972d; origin/dev is still 503bc97c.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Round 1 reviews: R765-1 (PR #835 issuecomment-6577388726) and R766-1 (issuecomment-6577608536), both NEGATIVE, MINOR only. Both public comments match the packets' REPORT.md.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6577649057 (text: evidence/taken.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6578986708 (text: evidence/review_ready.md)
- Scratch: $VALIDATION_STORAGE/640-a720l (gate clone, venv copied from 640-a720k, fresh scratch HOME with a freshly installed pinned SDK). Evidence: ./evidence/.
- Pages changed this round: docs/design/MARK_II_AREA_PLAN.md (AP) and one line of docs/design/MAILBOX_SPLIT.md (MS). No RTL, firmware, generator, gate or configuration file. No generated page reads either changed block; DOC_MAP, the TOC gate and the path gate pass unchanged.

## Read this first

1. **No STOP.** Every new fate rests on a recorded decision or a normative requirement, or keeps today's behaviour. D19 removes every LiteX block; D15 gives the stage 3 top the clocking; D4 and D18 put the firmware in on-chip Block RAM; REQ-MAC-03 keeps the link, speed and duplex inputs.
2. **Two fates keep today's behaviour rather than choose.** (a) The audio MMCM's `PSCLK` and the servo's `ps_clk_i` stay on the 200 MHz `idelay` clock; `_CRG` itself falls back to `sys` only when neither DDR3 nor Ethernet is built. (b) The PHY reset pin keeps both its uses: LiteEth's power-on pulse and `KL_reboot_ctrl`'s hold before a reload (REBOOT_RESET.md section 1). Changing either would be a new choice; the page does not make it.
3. **"311 of 311" is dropped, not receipted.** The probe's receipt (image B's `ppmem` read, `0x01370137`) exists in 640-a722b, but the page can only cite a public URL, and this packet's archive path and commit are not known to me. A docs link to a guessed evidence path would fail the same way F4 did. The page now states what the cited public comment shows for the SoC bus route.
4. **The residue's exact text broke the 10-word limit.** "Its sources also include fabric timer expiries, tagged with their arm." is 11 words. MS:151 reads "..., tagged by arm." Round 1 handled its residue the same way (R765-1 focus item 5).
5. **The BIOS move touched three lines outside the census table.** The page said in three places that the LiteX stages remove the BIOS memory. AP:235-236 adds a note under the stage table (the owner's stage 1 cells are unchanged), AP:112 says "The switch-over and LiteX stages 1 to 3", AP:383 says "All 47 are gone once LiteX stage 3 ends." Lane 2's scope (AP:427) still reads "Drop DDR3 and the BIOS ROM", the stage 1 wording; the note explains it.
6. **The re-derivation found one thing neither review named:** the PHY reset pin, whose CSR storage `KL_reboot_ctrl` sets through `MilanMAC` (milan_soc.py:2127-2132). Its fate is in the Ethernet row (AP:319).

## Commits (one-line subjects, no body, no trailers)

Commits 1 to 7 (640-a720j and 640-a720k) are unchanged; this round adds one per finding, and one for the suggestion taken:

| # | SHA | Subject |
|---|---|---|
| 8 | 7f5ea1c85685ba23cae7ad69a48492a1ceb82d44 | Give every LiteX block of the basis and the split build a census row with a stage and a non-LiteX fate: the IDELAYCTRL and its PSCLK clock, MilanMAC's link_status and loopback CSRs, the BIOS at the switch-over, ctrl_memory and ctrl_mbx (#640) |
| 9 | 7d71f4ba6e6ca70074d2401f857947aacff4a6ec | State that the console buffer's 2.0 ms share and T_svc = 20 ms are #665's unmerged S2b work, that dev still proposes 10 ms, under which the buffer would be 128 bytes, and that 32 bytes holds only while passes fit the share (#640) |
| 10 | 639e1efc6fc5dd4e3f731697f6d93b4addad2d13 | Drop the unpublished 311-of-311 read count from the stage 1 text and keep what the public probe comment shows for the SoC bus route: the entity advertised and all 33 descriptors read back byte-identical (#640) |
| 11 | 6b14a0cbf123d33ec3e06bbc7d1e869144f56d80 | Name the event record's sources as the subject of its timer-expiry sentence, so it cannot be read as the grandmaster changes (#640) |
| 12 | 30eb4834e0d258668a7bdfece187f9d7d9fccd0b | Drop the split CPU's netlist identifier, which no public source records, and keep the cited #665 comment as the source of 3,948 and 3,543 (#640) |

## Findings (each listed once, with every ID)

### 1. Census - R765-1-F1, R765-1-F2, R765-1-F3, R766-1-F1 (commit 8)

| Where (at head) | Change |
|---|---|
| AP:297-306 | Scope: rows follow the basis build's module tree and CSR map; the split build adds the last two rows; every tree node and CSR register maps to one row; no fate is a LiteX block |
| AP:313 (new) | `_CRG`'s 200 MHz `idelay` clock and the `IDELAYCTRL`, built while DDR3 or Ethernet is; the clock is also the audio MMCM's `PSCLK` and the servo's `ps_clk_i`. Stage 3. Replaced by the top's clocking (D15), keeping today's 200 MHz `PSCLK`. Stage 1 removes neither. All 32 basis `IDELAYE2` are DDR3's and GMII uses none, so the top builds an `IDELAYCTRL` only if the stage 2 MAC uses an `IDELAYE2` (R765-1-F2) |
| AP:319 | Ethernet row names `LiteEthPHYGMII`'s clocking and PHY reset, `tx_sf`, `mac_tx_cdc`, `mac_rx_cdc` and their CSRs; the PHY reset pin gets a first-party driver keeping its power-on pulse and `KL_reboot_ctrl`'s hold |
| AP:322 (new) | `MilanMAC`'s `link_status` CSR (MAC_STATUS, REQ-MAC-03) and the 2-flop crossing of link and duplex. Stage 3. Replaced by a first-party register the firmware writes, feeding the same three inputs (R765-1-F3, R766-1-F1) |
| AP:323 (new) | `MilanMAC`'s `loopback` CSR and its mux. Stage 3. Removed: nothing in the repository writes `milan_mac_loopback` (git grep), and its reset value 0 routes the datapath to the MAC (R765-1-F3, R766-1-F1) |
| AP:324 | Bus row adds the CPU wrapper's `ioBus_to_peripheral_bus_cc` 166 |
| AP:326 | Processor row adds `dma_filter_down_to_unified_mBus_cc` 104 |
| AP:327 | DDR3 row: the `IDELAYCTRL` moves out; adds the CPU memory port's clock crossing and ready stage (`memory_port_cdc0`, `memory_port_stage0`) and `_CRG`'s two 400 MHz `sys4x` clocks |
| AP:328-329 | BIOS ROM and SRAM: stage "Switch-over, lane 1" (milan_soc.py:3172-3176); fate "Removed, nothing in its place", no longer naming `ctrl_memory`; from stage 1 the boot loader fills the firmware's memory (D18) (R765-1-F1, R766-1-F1) |
| AP:330 | LED row names `user_led0` in its block cell, so R766's census probe reads every basis object "as a block" |
| AP:331 (new) | Split build: `ctrl_memory`'s `wishbone.SRAM` banks, `wishbone.Decoder` and error answer. Stage 3. Replaced by first-party Block RAM in the top (D4, D18); stage 1 already fills `rom` from the flash copy (R765-1-F1, R766-1-F1) |
| AP:332 (new) | Split build: `ctrl_mbx`'s `EventManager`, its CSR bank and the millisecond tick. Stage 3. Event manager and CSR bank removed: the firmware polls `KL_mbx`'s own status (mbx.c:422-425) and reads no `ctrl_mbx` CSR; no platform defines `CTRL_MBX_WFI`. A first-party counter replaces the tick (R765-1-F1, R766-1-F1) |
| AP:235-236, :112, :383 | The BIOS memory leaves at the switch-over (Read this first, 5) |

**How nothing is missing.** `evidence/census/census_coverage.py` maps, by explicit rules, every depth-0 node of the basis SoC hierarchy and every depth-1 node under `cpu`, `crg`, `milan` and `milan_mac`; every `csr_register` and `csr_base` of the basis `csr.csv`; every placed child of the CPU wrapper; and the split-only parts `milan_soc.py` builds at the head. Each object must match exactly one census row whose block cell names it and whose stage and fate are filled. Result at the head: PASS, 165 objects, 23 rows, every row hit but the LED row (none built). The same check against the round 1 page fails on nine objects: the `IDELAYCTRL`, `link_status`, `loopback`, the three `ctrl_memory` parts and the three `ctrl_mbx` parts. R766-1's own `census_probe.py` reads every object "as a block". Only `milan_datapath` is left out, as first-party RTL.

Sources (digests in evidence/census/basis_sources.txt): litex.log's SoC hierarchy, csr.csv, the placed hierarchical report (sha256 ec345a49..., the digest AP records), and alinx_ax7101.v for the `IDELAYE2` sources, `PSCLK` and the PHY reset logic.

### 2. Console buffer basis - R765-1-F5, R766-1-F2 (commit 9)

| Where (at head) | Change |
|---|---|
| AP:351 | Gap row: kind "Bound, if the share holds"; source adds "both are #665's S2b work, PR #810, not merged" |
| AP:353 | Buffer row: kind "Chosen, under the share" |
| AP:355 (new) | Under dev's T_svc = 10 ms: dev states no per-pass share; taking 10 ms as the gap, 116 characters complete (115 character times are 9.983 ms, 116 are 10.069 ms), so the buffer would be 128 bytes, holding 11.111 ms. Cites FR_NFR.md 3.4.1 |
| AP:356 (new) | At 32x32: the longest pass is estimated 1.7 to 5.9 ms over the share (#665 issuecomment-6569635407), so the 32-byte bound does not hold there |
| AP:359-369 | Prose: the share and 20 ms come from S2b, PR #810 not merged; dev's FR_NFR.md still proposes 10 ms, under which 128 bytes; 32 bytes holds only while passes fit the share, and is derived again if the share changes; at 32x32 the loss rule applies |
| AP:317, :412 | Census UART row and D20's consequence: "a polled receive buffer, 32 bytes under the S2b share" |

Checked: PR #810 is OPEN against `dev-soft-core` (gh pr view, 2026-11-02); FR_NFR.md:329 and :339 say 10 ms proposed.

### 3. "311 of 311" - R765-1-F4, R766-1-F3 (commit 10)

AP:284-287: "On the SoC bus, 311 of 311 reads were answered. That is a measurement, not a diagnosis." becomes "With the masters on the SoC bus, the entity advertised. All 33 descriptors read back byte-identical." and "Both are measurements, not a diagnosis." Both facts are in #640 issuecomment-6556743957 ("ENTITY_AVAILABLE", "all 33 descriptors byte-identical"). `grep -n "311 of 311"` on the tree finds nothing. The PR body's item 4 drops it too.

### 4. Residue - R766-1-R1 (commit 11)

MS:151: "They also include fabric timer expiries, tagged with their arm." becomes "Its sources also include fabric timer expiries, tagged by arm." (Read this first, 4).

### 5. Suggestions

| IDs | Taken? | Reason |
|---|---|---|
| R765-1-S1, R766-1-S1 | Taken, commit 12 | AP:167 drops the netlist identifier no public source records; the cited #665 comment carries 3,948 and 3,543 |
| R765-1-S2 | No | The lever 4 figures recomputed clean in both reviews; which CPU figure the start uses moves with the S2b work, which puts the CPU on `sys`, so the sentence belongs with that change |
| R765-1-S3 | No | The public probe comment does not name the image behind the console-loss figure; naming it would add another unsourced fact, the class of F4 |
| R766-1-S2 | No | Recasting lever 4's "Why" cell and lane 7 changes the owner's text; it needs the owner |
| R766-1-S3 | No | The probe's AX7101 -3,758 LUT includes the failing DMA route and was not re-routed (issuecomment-6556743957), so it does not measure stage 1 as planned; listed for the stage 1 lane below |

## Gate table

All 55 rc files read 0.

Every run step of `.github/workflows/docs.yml` at 503bc97c (no `.github/` or `scripts/` diff on the branch), as its jobs run it, sequentially, on $VALIDATION_STORAGE/640-a720l/gates/wt: a fresh clone of the lane at 30eb4834e0d258668a7bdfece187f9d7d9fccd0b, with gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77 and verilog-axis 48ff7a7e (depth 1 from 640-a720k's clone, each origin its .gitmodules URL; the same pins as HEAD's gitlinks). Venv: 640-a720k's, copied. RV32 SDK: installed fresh into $VALIDATION_STORAGE/640-a720l/home; the shared SDK was not touched. TMPDIR and RUNNER_TEMP point into scratch. Run 2026-11-02T14:07:20+01:00 to 2026-11-02T14:56:52+01:00. Step list: evidence/gates/run_gates.sh, run_all.sh; readers and census steps: evidence/gates/run_extra.sh.

| Job | Step | Command | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD`, no .git | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | Wrote: $VALIDATION_STORAGE/640-a720l/gates/runner_temp/milan-hdl-reference/index.html |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | docs_check: 0 finding(s) across 213 md files + 1436 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 225 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| docs-gates-0 | gate_9 concise docs | `check_doc_style.py` (+ `--selftest`), `check_gptp_docs.py` (+ `--selftest`) | 0 | gPTP documentation selftest: OK (30 controls) |
| docs-gates-0 | gate_10 diagram no-drift | `DOC_MAP.gen.py`, `timesync_chain.gen.py` `--check`/`--selftest` | 0 | time-sync diagram selftest: OK (source, status, XML, raster) |
| docs-gates-0 | gate_11 solution docs | `check_solution_docs.py` (+ `--selftest`) | 0 | solution documentation selftest: OK (45 mutation controls) |
| docs-gates-0 | gate_12 submodule docs | `submodule_boundaries.gen.py`, `check_submodule_docs.py` | 0 | submodule documentation selftest: OK (table and diagram controls) |
| docs-gates-0 | gate_13 WaveDrom | `gen_wavedrom.py --selftest` and three `--check` | 0 | WaveDrom current: docs/diagrams/wd_gptp_pdelay.json |
| docs-gates-0 | gate_14 PNGs | `check_diagram_pngs.py` (+ `--selftest`) | 0 | diagram PNG selftest: OK (6 rasters, 28 mutation controls) |
| docs-gates-0 | gate_15 feature status | `check_feature_status.py --self-test` | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_16 traceability | `gen_module_matrix.py --check` | 0 | traceability matrix up to date (80 modules, 0 untested <= ratchet 0, 0 archived) |
| docs-gates-0 | gate_18 imported gPTP docs | `check_gptp_docs.py --with-submodule`; `make -C gptp-processor docs` | 0 | source evidence selftest: PASS (7 arms) |
| docs-gates-0 | gate_19 measurement self-tests | `measure_control_flow.py`, `measure_cohesion.py` `--selftest` | 0 | 18 checks: 18 PASS, 0 FAIL |
| docs-gates-0 | gate_21 bare-metal scope | `check_baremetal_only.py --check`/`--selftest` | 0 | baremetal-only selftest: PASS (867 arm(s)) |
| docs-gates-0 | ci_step_28 RV32 SDK | `ci_rv32_sdk_selftest.py`; `ci_rv32_sdk.py --destination $HOME/br-milan-rv32/host` | 0 | SDK fresh installation: verified |
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations |
| docs-gates-0 | gate_26 NVM record space | `check_nvm_record_space.py` (+ `--self-test`) | 0 | 0 finding(s) across 5 config(s): the inventory's (group, index) key set is exactly the set the shape requires with no key claimed twice, every persist |
| docs-gates-0 | gate_27 capture census | `check_nvm_capture.py` | 0 | PASS: capture census, clocks, both timing arms and receipt agree |
| docs-gates-0 | gate_28 saved-state writer | `test_nvm_firmware.py --self-test` | 0 | saved-state writer gate: OK across 5 shape(s), and every planted defect reddened |
| docs-gates-0 | gate_29 SoC sources | `check_soc_sources.py` (+ `--selftest`), `iob_pack_selftest.py` | 0 | iob_pack_selftest: 22 arms, 21 mutants, 0 failure(s) |
| docs-gates-0 | gate_30 RTL source lists | `check_rtl_source_lists.py` (+ `--selftest`) | 0 | 50 checks: 50 PASS, 0 FAIL |
| docs-gates-0 | gate_31 naming | `measure_naming.py --check`/`--selftest` | 0 | 66 checks: 66 PASS, 0 FAIL |
| docs-gates-0 | gate_32 port contracts | `check_port_contracts.py` (+ `--selftest`) | 0 | 82 checks: 82 PASS, 0 FAIL |
| docs-gates-0 | gate_33 fail-fast | `measure_fail_fast.py --check`/`--selftest` | 0 | 106 checks: 106 PASS, 0 FAIL |
| docs-gates-0 | gate_34 TODO ownership | `check_todo_ownership.py` (+ `--selftest`) | 0 | 45 checks: 45 PASS, 0 FAIL |
| docs-gates-0 | gate_35 test evidence | `measure_test_evidence.py --check`/`--selftest` | 0 | 105 checks: 105 PASS, 0 FAIL |
| docs-gates-0 | gate_36 hygiene | `check_hygiene.py --check`/`--selftest` | 0 | 35 checks: 35 PASS, 0 FAIL |
| docs-gates-0 | gate_37 SV idiom | `check_sv_idiom.py` (+ `--selftest`) | 0 | 55 checks: 55 PASS, 0 FAIL |
| docs-gates-0 | gate_38 C++ idiom | `check_cpp_idiom.py` (+ `--selftest`) | 0 | 75 checks: 75 PASS, 0 FAIL |
| docs-gates-0 | gate_39 Python idiom | `check_py_idiom.py` (+ `--selftest`) | 0 | 54 checks: 54 PASS, 0 FAIL |
| docs-gates-0 | gate_40 shell idiom | `check_sh_idiom.py` (+ `--selftest`) | 0 | 48 checks: 48 PASS, 0 FAIL |
| docs-gates-0 | gate_43 cited paths | `check_doc_paths.py` | 0 | doc path gate: OK (1084 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| docs-gates-0 | gate_44 archive | `check_archive.py` (+ `--selftest`) | 0 | archive selftest: OK (24 controls) |
| docs-gates-0 | gate_45 contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| docs-gates-0 | gate_46 AEM store | `gen_aem_store.py --self-test` | 0 | gen_aem_store self-test: PASS |
| docs-gates-0 | gate_47 sweep shape | `check_sweep_shape.py --self-test` | 0 |   [self-test] OK: 1 drift(s) reported |
| docs-gates-0 | gate_48 deploy shape | `check_deploy_shape.py --self-test` | 0 |   [selftest] OK: 1 drift(s) reported |
| docs-gates-0 | gate_49 entity shape | `check_entity_shape.py --self-test` | 0 | RESULT: PASS |
| docs-gates-0 | gate_50 CI controls | `ci_gate_workflows.py --check` and the thirteen self-tests | 0 | manifest comparison controls: PASS |
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check`/`--selftest` | 0 | selftest: PASS (2199 contract items, 5258 arms) |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | selftest: PASS |
| (lane) | Markdown gates, pinned venv | `docs_check.py` | 0 | docs_check: 0 finding(s) across 213 md files + 1436 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| (lane) | Markdown gates, pinned venv | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 225 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| (lane) | Markdown gates, pinned venv | `check_doc_style.py` | 0 | documentation style: OK (23 current documents) |
| (lane) | Markdown gates, pinned venv | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| (lane) | whitespace | `git diff --check 503bc97c HEAD` | 0 |  |
| (lane) | style on changed blocks | check_doc_style's `analyze()` on every changed block of the 4 pages against 503bc97c, and of this round's 2 pages against 3f8ed303 | 0 | docs/design/MAILBOX_SPLIT.md: 0 finding(s) in changed blocks |
| (reader) | AREA_BUDGET.md's gate reader (rtl-fast) | `syn/ooc/pp_resource_gate.py check-baseline` | 0 | baseline PASS: 3 endpoints |
| (reader) | MAILBOX_SPLIT.md's gate reader (rtl-fast firmware-unit) | `ctrl_service_bounds.arm_service_bounds` via `service_bounds_arm.py` | 0 | rc 0 |
| (lane) | census coverage | `census_coverage.py` over the basis hierarchy, CSR map and placed rows, and the split-only parts | 0 | RESULT: PASS |
| (lane) | census coverage control | `! census_coverage.py` against the round 1 page (3f8ed303): rc 0 means the check failed there, as it must | 0 | RESULT: FAIL |

Notes:
- docs-check's "Require every gate exactly once" verifies uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. Not run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Builder leg 1's 16 NOT RUN arms need migen, LiteX and an Arty report, which the docs workflow never installs; the leg's rc is what counts.
- The `style_touched` step checks the four branch pages against 503bc97c and this round's two pages against 3f8ed303.
- MS is gate-read, so its reader ran; AREA_BUDGET.md's reader ran too, though this round does not touch that page.
- Large logs are listed in evidence/gates/LARGE_LOGS.txt by sha256 and size, not copied.

## Open list (as it now stands)

1. #640's body still shows 34.2k, 26.9k and 20.7k (640-a720j). Unchanged.
2. Exact-head long gates apply when the PR is ready: AREA_BUDGET.md and MAILBOX_SPLIT.md are gate-read. Unchanged.
3. The console buffer still rests on S2b's 2.0 ms share; the page now says so and gives 128 bytes under 10 ms. When PR #810 merges or the share changes, the buffer is derived again.
4. D21's slot offset and budget wait for the stage 1 lane. Unchanged.
5. New: the census keeps today's `PSCLK` and PHY reset behaviour (Read this first, 2). If the owner wants either changed, that is a new decision.
6. New, for the stage 1 lane: the probe's AX7101 -3,758 LUT figure includes the failing route (R766-1-S3).
7. Coverage: every scope touched this round is Conformance, RTL (census) and Docs; Robustness for the console bound. No RTL, firmware, generator, gate or configuration file changed.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md, taken_url.txt | The TAKEN text as posted, and its URL |
| review_ready.md, review_ready_url.txt | The REVIEW READY text as posted, and its URL |
| census/census_coverage.py | The coverage check (Findings, 1) |
| census/census_coverage.out, census_coverage_control_r1.out | Its output at the head (PASS) and against the round 1 page (nine misses) |
| census/r766_census_probe.out | R766-1's `census_probe.py` at the head |
| census/basis_soc_hierarchy.txt, basis_csr.csv, basis_place_top_excerpt.rpt | The basis inputs, excerpted without host names or paths |
| census/basis_sources.txt | sha256 and size of every basis source used |
| census/tree_depth.py | Prints the hierarchy to a depth |
| style_touched.py, service_bounds_arm.py | The changed-block style probe; MS's gate reader |
| write_handoff.py, handoff_body.md, make_pr_body.py | Build this file and PR-BODY.md |
| gates/ | Every step's log and rc, run_all.out, run_all.sh, run_gates.sh, run_extra.sh, setup_clone.sh; LARGE_LOGS.txt |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR creation or edit, merge, rebase, sub-agent, bench, flashing or Vivado. No existing comment edited. Only TAKEN and REVIEW READY posted on #640. 640-a722b's receipts were read, not copied.

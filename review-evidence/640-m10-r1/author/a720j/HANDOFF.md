# HANDOFF - [A720j] issue #640 Mark II charter follow-up (docs only)

Status: REVIEW READY (2026-11-02). Every recorded docs-workflow step rc 0 on a clean clone of the head; git diff --check 503bc97c HEAD rc 0. Head 7aa996e3816a2e68e5d1672d2379a3f97cc304af (tree 47bb540920e4b02af13161665f7381a94a7357dd). Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-charter-followup, from dev 503bc97c (the PR #828 merge). Base resolved with `git merge-base HEAD origin/dev`: 503bc97cd4f24ad07596c17e7188f2024617972d. The local `dev` ref is stale (e5b8405d); I used origin/dev.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6574060952 (text: evidence/taken.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6575241037 (text: evidence/review_ready.md)
- Scratch: $VALIDATION_STORAGE/640-a720j (gate clone, venv copy, scratch HOME with a fresh pinned SDK). Evidence: ./evidence/.
- Four pages change, all Markdown: docs/design/MARK_II_AREA_PLAN.md (AP), docs/design/AREA_BUDGET.md (AB), docs/design/MAILBOX_SPLIT.md (MS), docs/findings/README.md (FR). No RTL, firmware, generator, gate or configuration file.

## Read this first

1. **The owner's 2026-11-02 decisions are not on #640.** I found no owner comment at 07:21 or 07:22 on #640, #665, #495 or PR #828 (searched every comment since 2026-11-02 00:00 UTC). AP:373-375 (D18 to D20) therefore link to issue #640 itself, without a comment anchor. Please post them on #640; the three links can then point at that comment. My TAKEN says so.
2. **Copy from flash plus an unchanged layout leave one place for the image.** The baremetal layout (QSPI_FLASHBOOT.md:49-52) has the bitstream (4 MiB budget) and the AEM (64 KiB) slots, and no firmware slot; A722's report said a copying loader "needs a firmware slot the baremetal layout lacks". The 1x1 firmware's rom alone needs 96,624 B (SPLIT_CONTROL_MEMORY.md section 5), more than the AEM slot. The basis build's `alinx_ax7101.bit` is 3,825,992 B (uncompressed), so the bitstream slot leaves 368,312 B after it. I published this as open owner decision 4 (AP:432-441) and did not choose. The stage 1 lane's dependency names it (AP:389).
3. **Lever 4's end point is unchanged exactly, and its central figure moves 0.3k.** Crediting lever 4 with the 3,249 it really removes, both chains reach 27,224 after lever 4 (AP:156-178). The owner's middle 3.55k overstated that by 301, so the central running totals from lever 4 on move up: 26.9k to 27.2k, 25.9k to 26.2k, 20.7k to 21.0k, and the 32x32 central from 21.45k to 21.75k. #640's issue body still carries the owner's 34.2k chain; I cannot edit it.
4. **CI will not treat this PR as docs-only.** AB and MS are in `GATE_READ_DOCS` (scripts/ci_scope.py:69-78), so the exact-head `verilator-suites` and `yosys-portability` gates apply once it is marked ready. I ran both pages' readers at the head on the clone: `pp_resource_gate.py check-baseline` "baseline PASS: 3 endpoints", and the `ctrl_service_bounds` arm "RESULT: PASS", 47 checks, 0 failures. Neither reads a line this PR changes.

## Commits (one-line subjects, no body, no trailers)

| # | SHA | Subject |
|---|---|---|
| 1 | 4c128f1a5a79fe2110d4e8f975121ae30b26bae0 | Count the SoC CPU once in the Mark II start estimate, so lever 4 is an accounting correction that leaves the estimate after it unchanged (#640) |
| 2 | bc789366e801e64077606cbc499ba20bfaeb1c77 | List every LiteX block the shipping SoC builds with the stage that removes it and its fate, under the owner's 2026-11-02 decisions (#640) |
| 3 | b03df2ccf0b9da36f697484677fd12a870e845b6 | Size the first-party console UART's polled receive buffer from the measured console loss and the per-pass share, and accept console loss beyond that bound (#640) |
| 4 | 1dfc097cca05a46e042ad564beab7ba44b67cba4 | State that LiteX stage 1 copies the firmware from QSPI flash into Block RAM with the flash layout unchanged, and that masters use the SoC bus because the DMA-port route hung on silicon (#640) |
| 5 | 7aa996e3816a2e68e5d1672d2379a3f97cc304af | Take the exact residue of PR #828 listed on #495: the target wording, the Block RAM bar, the placement pointer, the stale gap and the gPTP plane until #665 lane F6 (#640) |

Item order: 1 lever 4, 2 census, 3 UART, 4 stage 1, 5 residue. Commit 2 also adds the D18 to D20 decision rows, since the census fates rest on them; commit 4 adds open decision 4 and points D18 at it.

## 1. Lever 4 accounting (AP, commit 1)

| Where (at head) | Change | Source |
|---|---|---|
| AP:17 | Contents: about 21.75k | Derived below |
| AP:40-47 | Summary: start about 31.0k; owner's 34.2k counted the CPU twice; six levers about 21.0k; lever 4 saves nothing; 32x32 near 21.75k | Derived below |
| AP:113 | Basis row `VexiiRiscvLitex_*`: "Replaced by the split CPU, the one hart" (was "Kept; lever 4 removes the second split CPU instead") | #665 issuecomment-6569635407 |
| AP:144-154 | Code block: the owner's chain, then `- 3,249` and `=30,974` (derived) | Basis row 3,249 |
| AP:156-178 | New `### Lever 4 accounting`: one hart under `--ctrl-mailbox`; table of measured and derived rows; both chains reach 27,224 | S2b round 12 handoff line 284 and section 5.2; #665 issuecomment-6569635407 |
| AP:180-198 | New `### Lever order`; running totals from 30,974 (derived, marked); lever 4 saving 0, "the owner's table had ~3.55k" | Owner 16:40 table |
| AP:200 | "The ranges then give 19.8k to 22.4k" | Derived below |
| AP:207, :213, :215 | 32x32 table row 1 ~21.0k, 19.8k to 22.4k; sum ~21.75k, 18.5k to 25.45k; misses by about 1.75k | Derived below |
| AP:388, :394 | Lane 1 "Basis to ~31.0k"; lane 7 saving 0 (accounting) | Derived below |

Netlist rows used:
- 3,249 LUT: `VexiiRiscvLitex_f5f08b170311db53220574624f819159`, row 32 of `alinx_ax7101_utilization_hierarchical_place.rpt` in build_ax7101_asl_e240b77bbd (sha256 ec345a49..., as AP:100 records). Measured.
- 3,948 LUT: the product split CPU netlist `VexiiRiscvLitex_7ee512a1cb1c336731b7f28188c9814f`, out of context, behind the clock crossing (3,543 on `sys` without it): S2b round 12 handoff section 5.2 and #665 issuecomment-6569635407. Measured. Line 284 of that handoff is the double-count finding.

Derivations (all derived, none measured as a whole image):
- 34,223 = 52,008 - 24,354 - 481 + 3,948 + 3,102 (the owner's chain, unchanged).
- 30,974 = 34,223 - 3,249 (CPU counted once). Net change of the one CPU: 3,948 - 3,249 = +699.
- After levers 1 to 3 (central 1,000 + 1,000 + 1,750 = 3,750): 30,974 - 3,750 = 27,224. Lever 4: 0, so 27,224.
- The owner's chain crediting lever 4 with the 3,249 it removes: 34,223 - 3,750 - 3,249 = 27,224. Same end point.
- Central running totals: 29,974 (~30.0k), 28,974 (~29.0k), 27,224 (~27.2k), 27,224, 26,224 (~26.2k), 21,024 (~21.0k).
- Ranges with lever 4 at 0: best 30,974 - (1,500 + 1,500 + 2,000 + 1,000 + 5,200) = 19,774 (19.8k); worst 30,974 - (400 + 500 + 1,500 + 1,000 + 5,200) = 22,374 (22.4k). The owner's old ranges were 19,123 and 22,423.
- 32x32: 21.0 + 0.25 + 1.75 + 1.0 - 1.75 - 0.5 = 21.75k; low 19.8 + 0.25 + 1.25 + 0.5 - 2.5 - 0.8 = 18.5k; high 22.4 + 0.25 + 2.25 + 1.75 - 1.0 - 0.2 = 25.45k. Ceiling miss 21.75 - 20 = 1.75k.

## 2. LiteX block census (AP, commit 2)

AP:279-312, `### LiteX block census`, 18 rows (AP:311-312 the generated FIFOs); AP:373-375 D18 to D20; AP:18 and :20 contents.

Sources for the block list: the module tree in build_ax7101_asl_e240b77bbd/litex.log (lines 175-1000: `bus`, `csr`, `irq`, `ctrl`, `cpu`, `dma_bus`, `rom`, `sram`, `identifier`, `uart`, `timer0`, `crg`, `ddrphy`, `sdram`, `litedramaxi2native_0`, `spiflash`, `milan_mac`, `milan`, `descmem_fsm`, `respmem_fsm`, `nvmmem_fsm`, `ppmem`, `csr_bridge`, `csr_bankarray`, `csr_interconnect`), its CSR map (`ctrl`, `ddrphy`, `identifier_mem`, `milan_mac`, `sdram`, `spiflash`, `timer0`, `uart`, `ppmem`; IRQ `uart` 1, `timer0` 2) and `sw/litex/milan_soc.py` (3166-3310 SoC core, DRAM, SPI flash; 1636-1644 PHY; 1940-1942 MDIO bit-bang; 2133 ICAPE2). `STARTUPE2` sits under `spiflash/phy` (litex.log:717). `user_led0` is assigned from `milansoc_milannic_identify` (alinx_ax7101.v:8096); no LED or GPIO block exists.

Placed rows cited (hierarchical placement report, measured): `VexiiRiscvLitex_*` 3,249; `vexiis_0_logic_core` 1,150; `peripheral_plic_intc_thread_logic` 34; `peripheral_clint_thread_core` 55; `peripheral_clint_time_cc_driver` 3; `peripheral_toAxiLite4_logic_bridge` 227; `dma_bridge_read_bridge` 105; `dma_bridge_write_bridge` 176; `mem_toAxi4_logic_bridge` 225; `unified_mBus_to_mem_toAxi4_up_widthAdapter` 136; `KL_gptp_gmii_launch` 192; `KL_mac_rmon_events` 51. The LiteX top is one flat row, 5,119, so its blocks get "LiteX top", said so on the page. The 18 RAMB36 BIOS ROM and SRAM and the 29 generated FIFO RAMB36 are the figures posted on #640 (issuecomment-6545523624), as the page says.

Fates and their basis:

| Block | Fate | Basis |
|---|---|---|
| CPU wrapper | Core kept, generated without LiteX, in the top | Owner 17:21 stage 3 (CPU in the top); core survey: vexiiriscv.Generate builds a standalone AXI4 core |
| Interrupt controller | Removed | The split firmware writes no `mie`/`mstatus`/`mtvec` (grep of sw/firmware); it polls `mbx_irq_status` |
| `_CRG` | Top's clocking and reset | Owner 17:21 stage 3 |
| `ctrl` | Removed | No firmware or script reads `ctrl_*`; reboot is KL_reboot_ctrl's IPROG through ICAPE2 |
| Identifier | Removed | No reader; `milan_csr` VERSION identifies the image |
| `timer0` | First-party free-running counter | Its one reader is sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c:24-85 (elapsed time, not the PHC) |
| UART | First-party UART, TX/RX, no RTS/CTS | Owner 2026-11-02 07:22 |
| SPI flash | Donor QSPI core by survey | Owner 17:21 stage 2; survey caveat stated |
| MAC, PHY interface | Donor GMII MAC | Owner 17:21 stage 2; survey proposal stated |
| MDIO | First-party pin register | LiteEthPHYMDIO is a bit-bang register pair (milan_soc.py:1940-1942); firmware does the protocol (milan_baremetal.c:935-995) |
| MilanMAC's own parts | Kept, move into the top | First-party |
| Bus and CSR interconnect | Top's fixed AXI4-Lite interconnect | Owner 17:21 stage 3 |
| `milan_axil_cdc` | First-party AXI4-Lite crossing from approved CDC primitives | Owner 17:21; CPU on `sys`, `milan_csr` on the datapath clock |
| Processor memory paths, `ppmem` | Removed at the switch-over | D11; lane 1 deletes the processor |
| DDR3, CPU memory port, IDELAYCTRL | Removed at stage 1 | D4; A722 measured IDELAYCTRL trimmed |
| BIOS ROM | First-party boot loader | Owner 2026-11-02 07:21 (D18) |
| BIOS SRAM | Firmware block RAM banks (`ctrl_memory`) | milan_soc.py:3003-3019 |
| LEDs or GPIO | None built | litex.log tree; alinx_ax7101.v:8096 |

No STOP: every block has a fate under a recorded owner decision or the code. Four fates name a first-party replacement that no owner comment names (the `timer0` counter, the MDIO register, the `milan_axil_cdc` crossing, the BIOS SRAM banks). Each keeps today's function under D19. The SPI flash's donor is not yet chosen: the core survey found no AXI core with both 7-series use and an active maintainer. The fate itself is the owner's 17:21 decision. If lane 4 finds no candidate meeting the owner's criteria, that is a later owner choice; it is not needed to give the fate.

## 3. Console UART (AP, commit 3)

AP:314-338 `### Console UART`; census UART row; D20 consequence.

| Number | Value | Derivation |
|---|---|---|
| Line | 115,200 baud, 8N1 | Basis build argv `--uart-baudrate 115200` (litex.log:3) |
| Character time | 86.806 µs | 10 bits / 115,200 |
| Measured loss | 22-character line: 17 of 300 sends lost characters; 14-character line: 0 of 300 | A722b REPORT risk 14 and receipts/console-drop/image-a.txt (lines `mem_read 0x90000110 4`, 21 characters plus newline, and `milan_gettime`, 13 plus newline) |
| 16-byte FIFO fill time | 1.389 ms | 16 x 86.806 µs |
| Gap bound | 2.0 ms | The per-pass share, 18 ms / 9 passes (#665 issuecomment-6514866239 item 3), under T_svc = 20 ms (#665 issuecomment-6495692075); console polled once per pass |
| Characters in the gap | 24 | 23 x 86.806 = 1,996.5 µs <= 2,000; 24 x 86.806 = 2,083.3 µs |
| Receive buffer | 32 bytes | Next power of two at or above 24 |
| Coverage | 2.778 ms | 32 x 86.806 µs; a 32-character line fits whole at any gap |

Notes:
- The console-drop receipt is named image-a.txt, the image with the DMA-port route. Both probe images had interrupts off and no BIOS, and the report says "on an idle console".
- The share is S2b's rule (PR #810, not merged); dev's FR_NFR.md:339 still says T_svc = 10 ms "proposed". With the 10 ms figure as the gap, the derivation would give 116 characters and 128 bytes. I used the per-pass share because the gap between polls is one pass. If the share changes, the buffer must be re-derived.
- At 32x32 the S2b estimates put the longest pass at 7.9 ms, over the share. The page states that console loss beyond the bound is accepted and never stretches a service bound.

## 4. Stage 1 text (AP, commit 4)

| Where | Change | Source |
|---|---|---|
| AP:231 | Stage 1 row: copy from QSPI flash into Block RAM (D18); flash layout unchanged; masters on the SoC bus | Owner 2026-11-02 07:21; QSPI_FLASHBOOT.md:43-64 |
| AP:259-277 | `### Stage 1 boot and bus`: the copy; layout unchanged, no firmware slot (open decision 4); masters use the SoC bus, never the CPU's DMA port; the probe measured 3 reads issued, none answered; cause not established; 311 of 311 answered on the SoC bus; a measurement, not a diagnosis; the processor's masters leave at the switch-over | A722b REPORT sections 4 and 7; #640 issuecomment-6556743957 |
| AP:373 | D18 consequence points at open decision 4 | |
| AP:389 | Lane 2 scope and dependency on open decision 4 | |
| AP:432-441 | Open owner decision 4: where the copied image sits | build_ax7101_asl_e240b77bbd/gateware/alinx_ax7101.bit 3,825,992 B; 4,194,304 - 3,825,992 = 368,312 |

## 5. #828 residue on #495 (commit 5)

From the [A10] comment https://github.com/kebag-logic/milan-fpga/issues/495#issuecomment-6573412222 (line numbers there are at 503bc97c).

| Item on #495 | Resolved? | Now (at head) |
|---|---|---|
| AREA_BUDGET.md:129 "accepted target" (R757-10-R2) | Yes | AB:129, exact. AB:130 reworded to the sentence limit: "Mark II needs fewer than 20,000 `xc7a100t` LUTs at 32x32." |
| AREA_BUDGET.md:180 Block RAM and timing (R757-10-R2) | Yes | AB:180-182. The exact sentence has 15 words, over the 10-word limit, so it is split: "That is fewer than 20,000 LUTs at 32x32." and "The image must also fit Block RAM, with timing met." |
| MAILBOX_SPLIT.md:13 "defines the transition and end state" (R757-10-R3) | Yes | MS:22, exact. The 154-word status paragraph it sat in (MS:3-20) is split into short paragraphs with the same content (MS:4-31) |
| docs/findings/README.md:26 stale gap (R757-10-R3) | Yes | FR:26 "a tenth of the gap to NFR-RES-01's former 60 % target" |
| MAILBOX_SPLIT.md:134 "until F6" (R758-11-R4) | Yes | MS:151; "until #665 lane F6", to match the :43 wording; the figure node (MS:74) unchanged. The list item is one line, for the sentence limit |
| Optional MAILBOX_SPLIT.md:43 (R757-11-S1) | Yes, agreed | MS:58 "It keeps the gPTP plane until #665 lane F6." The 66-word paragraph (MS:41-46) is split, content unchanged (MS:52-64) |
| Optional SYSTEM_INTEGRATOR.md:95, BUILD_FLASH_BOOT.gen.py:44 (R757-10-S1) | No | Not in this assignment; the second is a generator |
| PR #828 body stops at round 9 (R757-11-R2, R758-11-R1) | No | PR edits are not allowed in this lane |
| Evidence prose in author-r10/HANDOFF.md | No | Not a repository file |

## Gate table

All 53 rc files read 0.

Every run step of `.github/workflows/docs.yml` at 503bc97c (unchanged since round 9's base 1f29f189: no `.github/` or `scripts/` diff), as its jobs run it, sequentially, on $VALIDATION_STORAGE/640-a720j/gates/wt: a fresh clone of the lane at 7aa996e3816a2e68e5d1672d2379a3f97cc304af, with gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77 and verilog-axis 48ff7a7e (depth 1 from round 9's scratch clone, each origin its .gitmodules URL). Venv: round 9's, copied. RV32 SDK: installed fresh into $VALIDATION_STORAGE/640-a720j/home; the shared SDK was not touched. TMPDIR and RUNNER_TEMP point into scratch. Step list: evidence/gates/run_gates.sh, run_all.sh.

| Job | Step | Command | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD`, no .git | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | Wrote: $VALIDATION_STORAGE/640-a720j/gates/runner_temp/milan-hdl-reference/index.html |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | docs_check: 0 finding(s) across 213 md files + 1436 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 195 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
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
| (lane) | Markdown gates, pinned venv | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 195 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| (lane) | Markdown gates, pinned venv | `check_doc_style.py` | 0 | documentation style: OK (23 current documents) |
| (lane) | Markdown gates, pinned venv | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| (lane) | whitespace | `git diff --check 503bc97c HEAD` | 0 |  |
| (lane) | style on changed blocks | check_doc_style's `analyze()` on every changed block of the 4 pages | 0 | docs/findings/README.md: 0 finding(s) in changed blocks |
| (reader) | AREA_BUDGET.md's gate reader (rtl-fast) | `syn/ooc/pp_resource_gate.py check-baseline` | 0 | baseline PASS: 3 endpoints |
| (reader) | MAILBOX_SPLIT.md's gate reader (rtl-fast firmware-unit) | `ctrl_service_bounds.arm_service_bounds` via `service_bounds_arm.py` | 0 | rc 0 |

Notes:
- docs-check's "Require every gate exactly once" verifies uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. Not run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Builder leg 1's NOT RUN arms need migen, LiteX and an Arty report, which the docs workflow never installs; the leg's rc is what counts.
- Clone status after the run: empty.

## Open points for the manager

1. Post the owner's 2026-11-02 decisions on #640 (Read this first, 1).
2. Open owner decision 4, where the copied firmware sits in flash (Read this first, 2).
3. #640's body still shows 34.2k, 26.9k and 20.7k (Read this first, 3).
4. Exact-head long gates apply when the PR is ready (Read this first, 4).
5. The UART buffer rests on the 2.0 ms per-pass share, which is S2b's unmerged rule (section 3).
6. Coverage: every touched scope is Conformance and Docs. No RTL, firmware, generator, gate or configuration file changed.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md | The TAKEN text as posted |
| review_ready.md | The REVIEW READY text as posted |
| style_touched.py | check_doc_style's analyze() over every changed block of a page against a base |
| service_bounds_arm.py | Runs MS's gate reader on the clone |
| write_handoff.py, make_pr_body.py | Build this file and PR-BODY.md |
| gates/ | Every step's log and rc, run_all.out, run_all.sh, run_gates.sh, setup_clone.sh; LARGE_LOGS.txt lists logs over 200 KB by sha256 and size |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR creation or edit, merge, rebase, sub-agent, bench, flashing or Vivado. No existing comment edited. Only TAKEN and REVIEW READY posted on #640.

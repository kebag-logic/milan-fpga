[R792] NEGATIVE - exact head 6584b7bfdf19e923153820c60190d87964e8f57b

# R792-1: external review of PR #853 (#665 S6a, the placement switch)

- Head `6584b7bfdf19e923153820c60190d87964e8f57b`, tree `7a2f8067e677854fd50fca47c178270910fdacdb`.
- Source base `dev-soft-core` `a9d69c774dee18b90eead74c9f2dda24cf8fdeb8`, 14 commits, no merge.
- Covering round: R792-1. All five lenses applied.
- Verdict: NEGATIVE. Two MINOR findings are open: T-1 under Conformance, Tests and Docs, and D-1 under Docs.
- RTL and Robustness are clean. Three RESIDUE items and five SUGGESTIONs do not affect the verdict.

## Scope as reconstructed

Read in this order:

- AGENTS.md and CONTRIBUTING.md section 1 (CDC primitives), then docs/README.md.
- The #665 body and the [A10] S6 assignment (issuecomment-6712890110).
- The [A745] TAKEN (6713000589) and STOP (6715517869).
- The S6 round 1 ruling (6715535566). It moves these out of S6a:
  - the two-placement simulation, the split census population and the CDC CI job, to S6b;
  - the REBOOT carrier and the AECP-owned items, to S11;
  - the firmware-before-SoC link, to S9;
  - `pp_placement` f0-f4, ruled dead until the flip.
- None of those is reported as missing here.
- Interface authorities: `docs/design/MAILBOX_SPLIT.md` (publication block, contract 2.3, "The placement switch"), `sw/mailbox/census_ports.py` (port classes), and `docs/litex/CLOCK_DOMAINS.md`.
- Then `git diff a9d69c77..6584b7bf` and its history, and the author receipts at `2743f68b:review-evidence/665s6-r1`.
- PR #853 had no earlier public review finding (0 reviews, 0 review comments; only the two review-start comments). Nothing is carried forward.

The plan text "[A678] section S6" is not in any public #665 comment I could find. So mutants and controls were checked against the assignment, the STOP, the ruling and the PR body. See Limits.

## The six checks

| # | Check | Result | Evidence (this round, exact head unless stated) |
|---|---|---|---|
| 1 | All-fabric placement unchanged | Holds | `placement_identity.py --dump` of a9d69c77 and of the head: 6 of 6 shape digests equal, and they equal the author's (receipts/ident-*.json, ident-compare.txt). Self-test 6 of 6 (ident-selftest.log). Three reviewer plants inside `g_af_amr` each change the digest (identity-probes.txt). Gateware export of all 5 shipped configs, base vs head, from one path: each 3,876 files, 3,856 identical, 20 normalised, 0 different (export5/). Each config's 20 are 5 stamp, 13 ar-mtime, 1 hierarchy tree and 1 litex.log. Raw diffs of the shipping config show only date lines and 6 reordered tree-glyph lines (export-normalised-diffs.txt) |
| 2 | Split: no processor, MAAP engine or map writer; class D behind SID_VALID; G tied with reasons | Holds | `split_population.py --check`: 6 shapes, wrapper/adp/acmp/srp/maap/aecp/notify 0, mailbox 1, gptp 1; self-test 3 of 3. `milan_datapath.sv:9972-9988` routes class C from `i_ctl_pub_*`, with each sink's SID muxed on `i_ctl_pub_sid_valid[k]`. The tied class-D values (`:9992-10005`) have only CSR or GSI-answer readers (checked by grep of each net's readers, and by the census at the head, 246 checks, 0 failures). Map writer: 56 split ties against g_af_amr reset values, 55 equal; the one departure, `amr_rs_hold_r = 0`, is the documented intent (amr-tie-check.txt). G ties `:10106-10153`, each with its reason; the host window answers at once, refused, as documented |
| 3 | sys/milan_cd crossings through approved primitives; split_cdc_check refuses a raw one | Partly. See T-1 | `split_cdc_check.py --selftest` reproduces 152 sinks clean, 4 of 4 plants. The split SoC export at the head (split_top_wiring.txt): KL_mbx_cdc on `sys_clk` and `milan_clk`; KL_mbx and milan_datapath share 0 nets; 72 of 80 ctl ports bind KL_mbx_cdc's d-side; the 8 frame ports enter LiteX async FIFOs with 5-bit gray pointers; 82 of 82 m-side ports reach KL_mbx. But the check accepts a raw capture of the settings bus (T-1) |
| 4 | control.placement selects both flags and the parameter consistently; split cannot link the fabric firmware | Holds | Gates 23d, 23n, 23m (6 real SoC elaborations, one split case) and its 4-cut mutation arm pass at the head (builder-gates.txt). The split export builds no `libmilan_baremetal`, and its flash layout equals the all-fabric one (bitstream + entity model only) |
| 5 | Split leg's 48 checks and 13 mutants test what they name | Holds, with the scope the suite README states | `make split` with pinned Verilator 5.050: 48 checks, 0 failures (split-leg.log). `split-mutants`: 13 of 13, each caught by the label it names (split-mutants.log). I reviewed each arm against its label. The README (`tb/verilator/milan_dp/README.md:1148`) states that the EDIT window, the face events and the GM event are not held; see S-1 |
| 6 | Area and placement figures match receipts and are labelled as measurements | Holds | The Yosys table equals the per-run JSON, and every difference column recomputes. Vivado `utilization_place.rpt`: 34,225 LUT (53.98 %), 45,222 FF, 14,147 of 15,850 slices (89.26 %), 93 BRAM tiles, 5 DSP. `timing_place-summary.rpt`: WNS -0.071 over 24 endpoints, WHS -0.245. The memory plan is 27 + 12 = 39.0 of 56 tiles. All are labelled estimates or measurements, "not routed", "not a gate" |

## Findings

### T-1 MINOR: the CDC check's exemption accepts a raw capture of the settings bus

`[R792] MINOR Conformance, Tests, Docs - tb/verilator/milan_dp/split_cdc_check.py:57,136,153 - the fw_r exemption admits any m_fw_* source, including the enable`

- **Requirement and evidence.**
  - CONTRIBUTING.md section 1 allows crossings only through the approved primitives.
  - The check's docstring (`:24-27`) allows one named reading: `fw_r` taking the held `m_fw_*` bus, "enabled by u_fw_req's dest_pulse".
  - The code exempts every `m_fw_*` input read by the flop named `fw_r` (`HELD = ("fw_r", "m_fw_")`, `:153`). That includes `m_fw_send_i`, and it never checks that the enable is the synchronised pulse.
  - Reviewer probes (scripts/cdc_check_probes.py, receipts/cdc-check-probes.txt): `fw_r <= fw_bus_w` every datapath cycle, with no qualifier, passes clean (152 sinks).
  - `else if (m_fw_send_i) fw_r <= fw_bus_w;`, enabled by the raw sys-domain level, passes clean.
  - Two controls are refused as they should be: an enable from `fw_req_p_w`, and a non-`fw_r` flop sampling `m_fw_identify_i`.
  - `docs/design/MAILBOX_SPLIT.md:1426-1427` claims the check "refuses any crossing that skips a primitive".
  - The STOP and the PR body list "a netlist check that refuses a raw one" as met.
- **Impact.** A later edit can capture the 2,671-bit settings bus (`FW_W_C` at 16 sources and sinks) without synchronisation. That means metastable or torn F-class settings in the datapath clock, and the structural gate stays green. The split leg's functional mutant catches the unqualified form only by behaviour, and does not catch the raw-enable form at all, since it behaves identically in simulation. The RTL at this head is correct (`KL_mbx_cdc.sv:267-270`).
- **Required outcome.** The exemption holds only data bits of the held bus (not `m_fw_send_i`), taken by `fw_r` whose enable reads only `u_fw_req.dest_pulse`. Any other reading of the bus is refused. Plants cover the unqualified capture and the raw-enable capture. Or the docs and PR claims are narrowed to what the check proves.
- **Verification.** Both HOLE probes in receipts/cdc-check-probes.txt are refused by `split_cdc_check.py`. `--selftest` keeps 4 of 4 plants plus the new ones, and the tracked sources stay clean.

### D-1 MINOR: authoritative pages still describe the `--ctrl-mailbox` SoC as idle and unread

`[R792] MINOR Docs - docs/design/MAILBOX_SPLIT.md:828-831; docs/design/MARK_II_AREA_PLAN.md:423-425; docs/litex/CLOCK_DOMAINS.md:215-232 - stale or missing statements of the switched SoC and its crossing`

- **Requirement and evidence.**
  - AGENTS.md section 6 (Docs) requires changed contracts to be reflected in the authoritative docs.
  - At this head the `--ctrl-mailbox` SoC builds the `CTRL_SPLIT_P = 1` datapath and reads every `pub_*_o` through KL_mbx_cdc (`sw/litex/milan_soc.py:3109-3165`, and the export in split_top_wiring.txt).
  - Yet the publication-block section of the page this PR edits still says the selection is something "the placement switch adds after F5", and that "the `--ctrl-mailbox` SoC names the ports and leaves them unread" (`MAILBOX_SPLIT.md:828-831`, present tense).
  - `MARK_II_AREA_PLAN.md:423-425` still says the SoC "holds the mailbox datapath idle", the datapath "still instantiates KL_pp_shadow unconditionally", and "enabling `--ctrl-mailbox` alone saves no processor logic".
  - The clock-domain guide's crossing map has no row for the new sys/milan path: KL_mbx_cdc and the `ctl_rx_cdc`/`ctl_tx_cdc` FIFOs. That guide is the docs index's authority for "Trace clocks, resets, and crossings". Only the generated CDC census shows it.
- **Impact.** A cold reader of the contract pages gets the pre-switch behaviour of the build that now removes the processor. The crossing map omits the one new integration crossing.
- **Required outcome.** Those statements match the head, or are explicitly dated. The crossing map carries the split's crossing, with its primitives and FIFOs.
- **Verification.** Re-read the three locations at the fixed head. The docs gates stay at 0 findings.
- The same staleness sits in `sw/firmware/ctrl/plat/README.md:137`. That is S2b's area, which this lane was told to leave, so it is noted for the manager and not required here.

### R-1 RESIDUE: new source comments cite issue-comment IDs

- **Rule.** Owner rule 2026-10-15.
- **Where.**
  - `hdl/milan/milan_datapath.sv:380`: "mailbox (ruling 6088423771, decision 1)".
  - `hdl/milan/milan_datapath.sv:5633`: "(ruling 6410169666 item 1)".
- **Exact fix.**
  - Line 380: replace "(ruling 6088423771, decision 1)" with "(#665)".
  - Line 5633: replace "(ruling 6410169666 item 1)" with "(#665, #637)".
- **For the manager's call.** The plan label "F-INT PR 2" appears in about 20 new comment banners (for example `KL_mbx_cdc.sv:7`, `milan_datapath.sv:376,9959`, `milan_soc.py:990,2886`). If the manager counts it as a lane name, the fix is to drop "F-INT PR 2" and keep "#665".

### R-2 RESIDUE: PR body still asks for rulings that were given

- **Where.** PR #853 body, "Known limitations": "A ruling is asked on where that recipe lives." and, for `pp_placement.py` f0-f4, "A ruling is asked." Ruling 6715535566 answered both (items 4 and 5).
- **Exact fix.**
  - Replace the first with "The link before the SoC is S9's, with the split image recipe (ruling 6715535566 item 4)."
  - Replace the second with "f0-f4 is ruled dead until the flip, S13 (ruling 6715535566 item 5)."

### R-3 RESIDUE: a test comment names the wrong counter word

- **Where.** `tb/verilator/milan_dp/sim_split.cpp:329` says "GET_COUNTERS of STREAM_OUTPUT 0 ..., word 0, its counters_valid".
- **Evidence.** Word 0 of STREAM_OUTPUT is the STREAM_START counter (`milan_datapath.sv:4099`). counters_valid is word 32.
- **Exact fix.** Replace "word 0, its counters_valid" with "word 0, its STREAM_START counter".

### Suggestions (optional, no lens effect)

- **S-1 (Tests).** The split leg does not exercise the EDIT window, the counter-change and face events, or the GM event. The suite README (`:1148`) states this, and the ruled S6b comparison owes them.
  - A reviewer probe of KL_mbx_cdc's event crossing alone passed 19 of 19 (scripts/tb_cdc_events.sv, receipts/cdc-events-probe.txt). It covered descriptor mapping, the ALL record, a 16-descriptor burst with none lost, the GM pulse carrying its identity and domain, the three face events and LINK.
  - A unit leg of that kind, plus a mutant, would cost little in S6b.
- **S-2 (Robustness, inherited).** `rx_drops_o` can never count.
  - `axis_fifo` with `FRAME_FIFO = 1` and `DROP_WHEN_FULL = 1` holds `s_axis_tready` high (`third_party/verilog-axis/rtl/axis_fifo.v:217`), so `drop_p_w` (`KL_ctrl_split.sv:176`) is constant 0.
  - It is copied from `KL_pp_shadow.sv:860`, so both placements read 0. Worth a new issue, not a change here.
- **S-3 (Robustness).** `KL_mbx_cdc_window.sv:62-66` drops a request edge that rises while the previous transfer still waits for its handshake. That can happen only if the datapath clock stalls or resets beyond the 64-cycle window bound, and it recovers after one more timeout. A held "pending" bit would remove even that.
- **S-4 (RTL, measurement).** The all-fabric netlist is identical, but Vivado now names the processor `g_af_pp.pp_shadow`. No all-fabric Vivado run re-measured QoR after the rename. One measurement before the flip would close it.
- **S-5 (Docs).** `syn/ooc/split_population.py` carries `SPDX-License-Identifier: MIT`, as 11 of the other 16 `syn/ooc` scripts do. No change is needed if that directory's MIT convention is intended.

## Clean lenses, with evidence

- `[R792] PASS RTL - hdl/milan/milan_datapath.sv:9958-10154, KL_mbx_cdc.sv, KL_mbx_cdc_window.sv, KL_ctrl_split.sv, sw/litex/milan_soc.py:2886-3175 - clocks, CDC, FSMs, widths, interfaces`
  - Clocks: every ctl port is in `axis_clk`. The split SoC binds `sys_clk` and `milan_clk` as intended (split_top_wiring.txt).
  - CDC structure: publication by free-running `cdc_handshake` with one coherent snapshot. Settings by `cdc_pulse` in and out over the bus KL_mbx holds; KL_mbx refuses F-register writes while busy (`KL_mbx.sv:365-379`).
  - Windows by tagged `cdc_handshake`. The req/wait protocol matches the datapath's combinational `wait = req && !served` faces (`milan_datapath.sv:4158,4538,6673`).
  - Events by gathered pending bits, with none lost (my probe, 19 of 19).
  - Widths: the concatenation widths on both sides of each bus agree. Standalone `-Wall` lint of KL_mbx_cdc and KL_ctrl_split shows no WIDTH or latch warning, only empty-pin and unused-parameter notes (lint-new-modules.txt).
  - Interfaces: the class C, F, R, E and M mapping matches `census_ports.py`. The map-writer ties match their reset values, with the documented exception. The frame tap's EtherTypes, subtypes and group addresses are correct (0x22F0 with 0xFA/0xFB/0xFC/0xFE; 01-80-C2-00-00-0E with 0x22EA; 01-80-C2-00-00-21 with 0x88F5).
  - Repository lint ratchet: 89 <= 89, PASS (lint_rtl.txt).
- `[R792] PASS Robustness - KL_ctrl_split.sv:131-226, KL_mbx_cdc_window.sv:76-124, KL_mbx.sv:497-535 - malformed input, ordering, reset, timeouts`
  - A runt frame (`TAP_HEAD0` with last) and a refused frame (bad-marked at beat 1) are reclaimed by the frame FIFO.
  - A stale window answer carries the old tag, which KL_mbx discards. A newer request restarts the requester.
  - A commit waits for an acknowledgement that the round trip delivers well inside `MBX_FACE_ACK_CYCLES`; the split leg measured 3 polls.
  - Both domains reset from one CRG.
  - My event-burst probe found no loss.
  - The residual edge case is S-3.
- PR #853 had no earlier review findings to resolve.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (T-1) | assignment 6712890110, ruling 6715535566, STOP 6715517869; identity, export, population, census, builder gates, split SoC export | R792-1 | 6584b7bfdf19e923153820c60190d87964e8f57b |
| RTL | CLEAN | milan_datapath.sv split branches, KL_mbx_cdc.sv, KL_mbx_cdc_window.sv, KL_ctrl_split.sv, milan_soc.py split binding, split SoC top Verilog | R792-1 | 6584b7bfdf19e923153820c60190d87964e8f57b |
| Robustness | CLEAN | KL_ctrl_split tap and serializer, window requester FSM, KL_mbx commit and timeouts, event gather; reviewer event probe | R792-1 | 6584b7bfdf19e923153820c60190d87964e8f57b |
| Tests | UNCLEAN (T-1) | sim_split.cpp, tb_split_top.sv, split_mutants.py (13 arms re-run), split_cdc_check.py (re-run, 5 probes), placement_identity.py (self-test, 3 probes), split_population.py (check, self-test), test_builder gates 23d/23m/23n | R792-1 | 6584b7bfdf19e923153820c60190d87964e8f57b |
| Docs | UNCLEAN (T-1, D-1) | MAILBOX_SPLIT.md, ARCHITECTURE_HW_SW_SPLIT.md, MARK_II_AREA_PLAN.md, CLOCK_DOMAINS.md, milan_dp README, MODULE_MATRIX, integrator pages; docs gates re-run (7, all 0 findings) | R792-1 | 6584b7bfdf19e923153820c60190d87964e8f57b |

## What was executed (all at the exact head unless stated)

Pinned tools: sv2v v0.0.12 and Yosys 0.66 for the elaborations; scoped Verilator 5.050 (identity verified by `--version`) for the split leg, the mutants and the probes.

- `placement_identity.py --dump` of a9d69c77 (a shared scratch clone, gitlinks equal to the head's) and of the head. Then `--compare` (rc 0) and `--selftest` (6 of 6).
- `split_population.py --check` (rc 0) and `--selftest` (3 of 3).
- `publication_census.py --check` (246 checks, 0 failures).
- `make split` (48/0), `make split-mutants` (13 of 13) and `split_cdc_check.py --selftest` (5/0).
- Gateware export of the 5 shipped configs, base vs head, with the author's published `export_compare.sh` and `compare_same.py` (copied into scripts/, CONFIGS made overridable).
- A split SoC export with gate 23m's synthetic image, analysed for its wiring.
- Builder gates 23d, 23n, 23m and the 23m mutation arm.
- `lint_rtl.py --check`.
- Docs gates: `docs_check.py`, `check_solution_docs.py`, `check_doc_style.py`, `check_diagram_pngs.py`, `gen_module_matrix.py --check`, `check_soc_sources.py`, `check_rtl_source_lists.py`.
- Reviewer probes: cdc_check_probes.py, identity_probes.py, tb_cdc_events.sv, amr_tie_check.py and split_top_wiring.py.

After the probes the clone is at exact head bytes:

- `HEAD` = 6584b7bf and `write-tree` = 7a2f8067.
- All 1,527 tracked blobs re-hashed equal, and the index's mode/blob/path list equals `ls-tree HEAD`.
- The six gitlinks are at their pins and the submodule worktrees are clean.
- No untracked or ignored file is left; the five build outputs my runs created were removed.

## Hosted evidence at review time (read-only, not a verdict)

At head 6584b7bf:

- **Completed, success:** `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, `firmware-aecp-mutants`, `firmware-srp-mutants`, `firmware-unit`, Verilator shard 6/19.
- **Skipped:** "Physical gPTP (nightly and manual)".
- **Still running or queued:** the docs gates, the elaborate gates, `publication-census`, the remaining Verilator shards, `yosys-elaboration` and the Yosys shards.

The manager owns hosted and act acceptance.

## Real limits

- The plan's section S6 ([A678]) is not public in #665's thread, so its mutant and control list was not compared line by line.
- Not re-run by me, so author receipts only:
  - the full four-shard sweep;
  - `test_ctrl_firmware.py --require-rv32 --self-test`;
  - the whole `test_builder.py` (only the four changed gates were run);
  - `xvlog_gate.py`;
  - the Vivado-side tool self-tests and mutants;
  - `behave`;
  - the census `--selftest`;
  - the Yosys `synth_xilinx` area runs;
  - the Vivado placement, which may not run beside other heavy builds.
- The figures in check 6 were checked against those receipts, not re-measured.
- The split leg's testbench joins the mailbox through verilog-axis `axis_async_fifo`. The real SoC uses LiteX's FIFOs, which I checked structurally in the export, not in simulation.
- No manager source bank ran at this head, and none is inferred. Physical calibration was not run. Field skips are not hardware proof.

## Pending manager duties

- Hosted checks to completion at this head.
- The current-dev merge-candidate builder and native banks at the merge turn: source base a9d69c77, live dev 1eb5289db8fc9d139ce90cad2e380b4515793806.
- Carry R-1, R-2 and R-3 to the residue checklist.
- Route the `sw/firmware/ctrl/plat/README.md:137` staleness (D-1 note) to S2b or S6b.

R792-1 FINISHED

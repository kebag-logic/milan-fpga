[R791] NEGATIVE - exact head 6584b7bfdf19e923153820c60190d87964e8f57b

# R791-1: internal cleared-context review of PR #853 (#665 S6a, the placement switch)

- **Head:** `6584b7bfdf19e923153820c60190d87964e8f57b`, tree `7a2f8067e677854fd50fca47c178270910fdacdb`.
- **Source base:** `dev-soft-core` `a9d69c77`.
- **Diff reviewed:** `a9d69c77..6584b7bf`, 14 commits, 44 files.
- **Scope:**
  - The assignment is issuecomment-6712890110 with the split plan's section S6.
  - The round-1 ruling is issuecomment-6715535566. It moves to S6b the two-placement simulation, the split census population and the CDC CI job. It moves the REBOOT carrier and the AECP-owned items to S11, and the firmware-before-SoC link to S9. It rules `pp_placement.py` `f0-f4` dead until the flip.
  - None of those is reported as missing here.
- **Lenses:** all five were applied independently: Conformance, RTL, Robustness, Tests and Docs.
- **Prior public findings on PR #853:** none. The PR thread holds only the two review-start comments, so nothing is retained or resolved from an earlier round.

## Verdict summary

The all-fabric placement is unchanged. I reproduced the elaborated-netlist identity independently on all six shapes: base `a9d69c77` equals head, and both equal the author's receipt. The split datapath is otherwise well built:
- it contains no `KL_pp_shadow`, `KL_maap`, shim or map writer in any shape;
- it lints clean in all five shipped shapes, with no undriven or multidriven nets;
- its tie-offs equal the reset values they replace;
- every crossing in `KL_mbx_cdc` uses an approved primitive.

The verdict is NEGATIVE for two reasons:
1. **Three executed hosted jobs at this exact head fail, and each failure traces to this delta** (R791-F1, R791-F2). Both causes reproduce locally.
2. **Three MINOR test and RTL defects are open** (R791-F3 to R791-F5).

## Findings

### R791-F1 MAJOR - RTL, Tests - `hdl/milan/milan_datapath.sv:714`, `:731` - two new boundaries hide their unit; the naming ratchet fails at the exact head
- **Requirement/evidence:**
  - CONTRIBUTING.md section 1 requires a boundary whose value has a unit to carry the unit in its name (CODE_QUALITY Rule 4).
  - `i_ctl_pub_idle_slope` is documented `IDLE_SLOPE.BPS`, and `i_ctl_pt_offset` is documented `F_PT_OFFSET.NS`.
  - At this head, `python3 scripts/measure_naming.py --check` exits 1 with `NEW: ...i_ctl_pt_offset`, `NEW: ...i_ctl_pub_idle_slope` and `NAMING RATCHET: FAIL (2 new, 0 stripped)` (receipts/naming-ratchet.log).
  - The hosted `docs-gates-0` job at this head fails on the same gate, gate_31. That makes the required `docs-check` context red (receipts/hosted-failures-excerpt.txt, receipts/hosted-check-runs.tsv).
  - The author's validation table reports the docs gates as "0 findings", but this gate is not among them.
- **Impact:** a required status context is red at the head, so the PR cannot merge. The new split interface also departs from the house naming rule on its first two unit-bearing buses.
- **Required change:** the two boundaries state their units (bps, ns) in their names, through every binding: `milan_soc.py` `CTRL_SPLIT_PORTS`/`_CTRL_CDC_DP`, `tb_split_top.sv` and the docs tables. Alternatively, the ratchet records a reasoned exclusion, if the owner accepts one. The local evidence includes `measure_naming.py --check`.
- **Verification:** `python3 scripts/measure_naming.py --check` and `--selftest` pass at the new head. Exact-head hosted `docs-gates-0` succeeds. The split leg and gate 23m still pass.

### R791-F2 MAJOR - Tests, Docs - `sw/builder/endstation_builder.py:4425`, `sw/firmware/ctrl/README.md:255`, `tb/verilator/milan_dp/Makefile` (the split targets) - the firmware boundary gate fails twice at the exact head
- **Evidence (a), firmware-boundary:** the new builder comment names `sw/firmware/ctrl/test/ctrl_plat_image.py`. That makes `endstation_builder.py` a program that names the firmware's tree while being in none of `ctrl_configs.BUILDERS`, `PART_OF`, `OUTSIDE` or `SUITES`.
  - The hosted `firmware-boundary` job ends `REFUSED: sw/builder/endstation_builder.py names the firmware's tree and is a program ...` with exit code 2.
  - Reproduced: receipts/ctrl-boundary-probe.txt reports `1 unclassified`, that file. At the base the builder names the tree 0 times.
- **Evidence (b), firmware-verilator:** the milan_dp Makefile adds four stack-pinned targets: `build-split`, `split`, `run-split` and `split-mutants`. They raise `ctrl_pin.pin_controls` from 171 to 175, while the firmware README still states 171.
  - The hosted `firmware-verilator` job fails with `[FAIL] sw/firmware/ctrl/README.md gives the pin controls as 171, where the self-test has 175` and `ctrl_boundary: FAIL`.
  - Reproduced: receipts/ctrl-boundary-probe.txt reports `the self-test's 175 ... the README states 171`.
- **Base:** the S5 branch head before the base merge (`c73be9b9`) is green on both jobs.
- **Impact:** two executed hosted firmware jobs are red at this head. They trigger the fail-fast cancellation of the rest of the hosted run: 30 cancelled, including `rtl-fast`. So the head has no successful `rtl-fast` verdict.
- **Required change:** the firmware boundary gate holds at the head, both its builder classification and its README figures. Assignment item 6 asks the lane to stay out of `sw/firmware/ctrl/` (S2b's area, #810) unless needed and to say where it touches it. Any edit there, or the decision to drop the path from the builder comment instead, is stated publicly.
- **Verification:**
  - `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` passes.
  - `--only verilator` passes, or the hosted `firmware-boundary` and `firmware-verilator` jobs succeed at the exact head.
  - Without the builds, scripts/ctrl_boundary_probe.py reports 0 unclassified and equal pin-control figures.

### R791-F3 MINOR - Tests - `tb/verilator/milan_dp/sim_split.cpp:381-400` against `hdl/milan/KL_ctrl_split.sv:121-125` and `hdl/milan/milan_datapath.sv:9983` - the split tap's classification and the Talker declaration encoding are untested beyond one tuple
- **Requirement/evidence:**
  - AGENTS.md section 5 asks for self-checking tests of changed behaviour, with negative and boundary paths. `KL_ctrl_split` accepts six tuple classes: ADP, AECP, ACMP and MAAP subtypes on 0x22F0, and MSRP and MVRP at their group addresses. The leg checks one accepted tuple (ADP) and one refused (AAF).
  - Reviewer mutants built through the leg's own recipe both survive with `checks: 48 failures: 0`: T1, the tap refuses MSRP, and T2, the tap refuses MAAP (receipts/split-reviewer-mutants.log).
  - Likewise D1, the Talker declaration published as FAILED (`2'd2`) instead of ADVERTISE, survives. The check reads only "not NONE", but the datapath's own GET_STREAM_INFO answer distinguishes FAILED (`milan_datapath.sv:6366`, `gsi_ofail_w`).
  - None of these is in the milan_dp README's "Not held here" list (`tb/verilator/milan_dp/README.md`, the split section). They are not covered by the ruling's move of the two-placement comparison either.
- **Impact:** a split image whose tap never hands MSRP, MVRP or MAAP frames to the mailbox would leave the firmware's SRP and MAAP owners deaf, and it passes every gate at this head. So would one that reports every declared Talker as failed.
- **Required change:** the leg (or a focused bench of `KL_ctrl_split`) holds each accepted tuple class, at least the MRP pair and MAAP, and a refusal at the wrong group address. The declaration check pins the encoding the datapath consumers distinguish. Alternatively, the gap is listed among the leg's "Not held here" items, with the stage that owes it named by a ruling.
- **Verification:** mutants T1, T2 and D1 (scripts/split_reviewer_mutants.py) are each caught by a named check.

### R791-F4 MINOR - RTL, Robustness, Tests - `hdl/milan/KL_ctrl_split.sv:38-41`, `:78`, `:176`, `:199`, `:329` - the drop counter cannot count: frames lost to a full FIFO are not counted
- **Requirement/evidence:**
  - The banner states that `rx_drops_o` counts "a beat a full FIFO refused, saturating at 255". `drop_p_w` is `fw_valid_w & ~fw_ready_w`, but the FIFO is built with `FRAME_FIFO=1, DROP_WHEN_FULL=1`. verilog-axis `axis_fifo.v:217` then holds `s_axis_tready` at 1, so `drop_p_w` is never 1. The FIFO drops the frame silently.
  - Reviewer probe (scripts/ctrl_split_drop_probe.cpp, receipts/ctrl-split-drop-probe.txt): 100 accepted 64-byte ADP frames are offered back to back while the mailbox is not ready. 64 are handed out and 36 are lost, with `rx_drops_o 0`.
  - The same construction is pre-existing in `KL_pp_shadow.sv:859-883`, whose banner says such a loss is "COUNTED ... never silently absorbed".
- **Impact:** in the split, the PP drops CSR word reads 0 while control frames are being lost under a burst. That is the one diagnostic that would show the tap overflowing.
- **Required change:**
  - A frame the split tap loses to a full FIFO is counted. For example, take the count from the FIFO's own overflow or drop indication rather than from `tready`.
  - Alternatively, the banner and the CSR documentation state that the counter never counts, with an Issue that tracks it.
  - In both cases, a self-checking overflow test.
  - The wrapper's identical defect becomes its own public Issue (AGENTS.md section 4), not a change in this lane.
- **Verification:** the probe, or a tracked equivalent, reports frames lost equal to `rx_drops_o` (saturating), and a mutant that removes the count is caught.

### R791-F5 MINOR - Tests, Docs - `tb/verilator/milan_dp/split_cdc_check.py:23-27`, `:57`, `:136`, `:153`; `docs/design/MAILBOX_SPLIT.md:1426-1427` - the netlist CDC check lets three raw crossings through
- **Requirement/evidence:** CONTRIBUTING.md section 1 allows crossings only through `cdc_pulse`, `cdc_handshake` or toggle+sync. The tool claims to refuse "any other reading across the two domains", and the design doc says it "refuses any crossing that skips a primitive".
  - **How the exemption works:** the settings exemption (`HELD = ("fw_r", "m_fw_")`) matches the flop name and any `m_fw_*` input. It never checks the capture enable that its docstring names ("enabled by u_fw_req's dest_pulse"). Primitive reset ports are never sinks.
  - **Reviewer plants on copies (scripts/cdc_plants.py, receipts/cdc-reviewer-plants.log)** each pass the check with 152 sinks:
    - R1, the held bus sampled every datapath cycle, with no enable;
    - R2, `u_pub`'s `dest_rst_n` taken from `sys_rst_n`;
    - R3, the capture enabled by the sys-domain level `m_fw_send_i`.
  - The tracked RTL is correct: I read every crossing, `KL_mbx` refuses face writes and GO while busy, and the tracked self-test passes. The defect is the check's strength and the claim made for it.
- **Impact:** S6b plans to make this tool the CI guard of the crossing. As written, it would accept an unqualified sample of the settings bus or a cross-domain synchronous reset.
- **Required change:**
  - The exemption admits the held bus only through a capture enabled by `u_fw_req`'s destination pulse.
  - Primitive reset (and clock) ports are judged in their own domain.
  - The doc and docstring claim no more than the tool checks.
- **Verification:** plants R1, R2 and R3 are each refused by name, and the tracked sources and the four existing plants still behave.

### R791-F6 RESIDUE - source comments - new lane labels and issue-comment IDs (owner comment rule 2026-10-15)
- **Evidence:** receipts/comment-rule-scan.txt.
  - The lane label "F-INT PR 2" appears 22 times in new source comments and strings. Locations:
    - `hdl/milan/KL_ctrl_split.sv:12`, `hdl/milan/mailbox/KL_mbx_cdc.sv:7`, `hdl/milan/mailbox/KL_mbx_cdc_window.sv:7`, `hdl/milan/milan_datapath.sv:376,9959`;
    - `sw/builder/endstation_builder.py:4417`, `sw/builder/test_builder.py:23490,23601`, `sw/litex/milan_soc.py:990,2886,3037,3749`;
    - `sw/mailbox/placement_identity.py:7`, `syn/ooc/split_population.py:3`, `syn/yosys/run.sh:306`;
    - `tb/verilator/milan_dp/Makefile:34,715,838`, `tb/verilator/milan_dp/sim_split.cpp:4`, `split_cdc_check.py:4`, `split_mutants.py:4`, `tb_split_top.sv:6`.
  - Issue-comment IDs appear twice: `hdl/milan/milan_datapath.sv:380` ("ruling 6088423771, decision 1") and `:5633` ("ruling 6410169666 item 1").
  - Docs pages are not counted.
- **Exact fix:** write "(#665)" for "(#665 F-INT PR 2)". At `:380`, write "(#665: the firmware owns every control protocol)". At `:5633`, write "(#665: the firmware's AECP owner holds the maps)".

### R791-F7 RESIDUE - prose - `docs/design/MAILBOX_SPLIT.md:1739-1744` and the PR body
- **Evidence:**
  - The REBOOT open item still says "the placement switch gives the request its carrier". The ruling (item 3) places the carrier in S11, after S2b (#810), and holds `reboot_req_i` tied 0 through S6a and S6b.
  - The PR body's Known limitations still say "A ruling is asked" for the firmware link and `pp_placement.py` `f0-f4`, both of which the ruling decided.
- **Exact fix:** "S11 (#665), after #810, gives the request its carrier; until then the split ties `reboot_req_i` to 0". In the PR body, replace each "A ruling is asked" with the ruling's outcome: S9 for the link, and `f0-f4` ruled dead until the flip.

### R791-S1 SUGGESTION - Tests - `sw/litex/milan_soc.py:2891-2993` (the `CtrlMailbox._split` tables) against `tb/verilator/milan_dp/tb_split_top.sv`
No tracked test runs the SoC's split binding. Gate 23m's spy stops at the datapath Instance, and the split leg simulates a hand-copied wiring.

My static check (scripts/soc_vs_tb_wiring.py) composes each `KL_mbx_cdc` port through the testbench nets. The SoC's 138 table bindings agree with it (receipts/soc-vs-tb-wiring.txt). A planted swap of `m_amap_type_i`/`m_amap_index_i` is caught (receipts/soc-vs-tb-wiring-plant.txt).

A tracked equivalent, or a split-SoC export elaboration in S9's image gate, would keep the two from drifting apart.

## Clean results, with evidence (per lens)

```text
[R791] PASS Conformance - sw/mailbox/placement_identity.py at head, receipts/identity/identity-compare-reviewer.txt (one shape per process) and receipts/identity-full-compare.txt (the tool's own --dump of each tree and --compare, rc 0) - all-fabric elaborated netlist, 6 shapes (recipe, arty_4x4, arty_8ch, arty_current, ax7101_1x1_tdm8, ax7101_8x8): base a9d69c77 (git archive with its gitlinks) digest == head digest == author's receipt, pinned sv2v v0.0.12 / Yosys 0.66
[R791] PASS Conformance - review-evidence/665s6-r1 export receipts + author/scripts/compare_same.py, receipts/export-receipts-tabulated.txt - 5 configs x 2 heads: 3876 files, 3856 identical, 20 = 5 stamp (csr.csv, csr.h, git.h, mem.h, soc.h) + 13 ar (member names and bytes equal) + 1 tree (the gateware top .v, comment-only hierarchy tree compared as a multiset) + 1 log (litex.log), 0 different, 0 missing; each normalisation read in the script and nothing else excused
[R791] PASS Conformance - syn/ooc/split_population.py --check at head, two runs (receipts/population-check.log, receipts/split-population.log) - 6 shapes: wrapper 0, adp 0, acmp 0, srp 0, maap 0, processor-maap 0, aecp 0, notify 0, mailbox 1, gptp 1
[R791] PASS Conformance - hdl/milan/milan_datapath.sv:9958-10154 (g_sp_ctrl) against docs/design/MAILBOX_SPLIT.md:835-843 and sw/mailbox/census_ports.py - class-D consumers on pub_* (DA_GATE->acmp_declaring, LICENCE->srp_active AND sr_admitted, TALKER_DECL->ADVERTISE, SID behind SID_VALID), G memory masters at reset, host window acked and refused, reboot_req tied 0; split leg [PUB]/[FACE] checks and the author's 13 mutants reproduce (receipts/split-leg.log, receipts/split-mutants.log)
[R791] PASS Conformance - hdl/milan/KL_ctrl_split.sv:88-97 - EtherType 0x22F0 with subtypes ADP 0xFA, AECP 0xFB, ACMP 0xFC (IEEE 1722.1-2021), MAAP 0xFE (IEEE 1722-2016 Annex B), MSRP 01-80-C2-00-00-0E/0x22EA, MVRP 01-80-C2-00-00-21/0x88F5, as the wrapper's tap
[R791] PASS Conformance - sw/builder/endstation_builder.py:4417-4446, 5091-5124; gates 23n, 23m (with its 4 cuts) and 23d run at head (receipts/gate23n.log, gate23m.log, gate23d.log) - control.placement selects --ctrl-mailbox --ctrl-firmware <its split image> and CTRL_SPLIT_P = 1 together; the SoC derives CTRL_SPLIT_P from --ctrl-mailbox; bad keys refused; a split key naming the fabric firmware refused
[R791] PASS Conformance - review-evidence/665s6-r1/author/receipts/area/*.json, vivado/*.rpt, image/memory-plan.txt against the PR body - every area and placement figure matches its receipt and its arithmetic (e.g. 99,794 - 60,298 = 39,496); labelled Yosys estimates, and one unrouted Vivado placement as a measurement, not a gate; RTL after 61d680dd changed only inside a block comment
[R791] PASS RTL (CDC) - hdl/milan/mailbox/KL_mbx_cdc.sv, KL_mbx_cdc_window.sv, hdl/common/cdc_handshake.sv, cdc_pulse.sv, hdl/milan/mailbox/KL_mbx.sv:362-508 - every sys<->dp crossing is a cdc_handshake, a cdc_pulse, or the pulse-qualified capture of a bus KL_mbx holds (face writes and GO refused while busy, so the request edge always falls between commits); the window requester waits on combinational wait (ctr, amap, gsi) before taking an answer; split_cdc_check self-test 5/5 at head (receipts/split-cdc-selftest.log)
[R791] PASS RTL (elaboration) - Verilator 5.050 --lint-only, milan_datapath -GCTRL_SPLIT_P=1, 5 shipped shapes with the builder's parameters, receipts/lint-split/*.log - 0 errors, 0 UNDRIVEN, 0 MULTIDRIVEN
[R791] PASS RTL (tie-offs) - hdl/milan/milan_datapath.sv g_af_amr vs g_sp_amr, receipts/amr-tieoff-vs-reset.txt - 56 registers, 56 tie-offs, each equal to its reset value except amr_rs_hold_r = 0, which the comment states
[R791] PASS Docs (generated artefacts) - docs/diagrams/cdc_census.gen.py regenerated into scratch, receipts/cdc-census-regen.log - drawio and svg byte-equal to the tracked files; publication census --check at head 246 checks, 0 failures (receipts/publication-census-check.log)
[R791] PASS Docs (contracts) - docs/design/MAILBOX_SPLIT.md "The placement switch", ARCHITECTURE_HW_SW_SPLIT.md section 5, ENDSTATION_BUILDER.md row 34a, the SYSTEM_INTEGRATOR and INTEGRATION_GUIDE split port group, the milan_dp README split section - match the RTL and builder, except as F2, F5 and F7 record
```

The EDIT window, the class-E events, the counter-change mapping and the GM change/identity cross without any check in the split leg. Reviewer mutants E1-E3, G1, G2, C1 and W1 all survive (receipts/split-reviewer-mutants.log). The milan_dp README lists exactly these as "Not held here ... The two-placement comparison owes them", and the ruling moves that comparison to S6b. They are recorded as S6b's obligation, not as a finding of this round.

## Reviewer-owned ledger

| Lens | Result | Examined artefacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | identity (6 shapes, both trees), export receipts and normalisation script, split population, class-D mapping vs the contract table and census classes, tap tuples, builder key and gates 23m/23n/23d, area and placement receipts | R791-1 | `6584b7bfdf19e923153820c60190d87964e8f57b` |
| RTL | UNCLEAN (F1, F4) | `milan_datapath.sv` split branches, `KL_ctrl_split.sv`, `KL_mbx_cdc.sv`, `KL_mbx_cdc_window.sv`, `KL_mbx.sv` commit and refusal, the primitives, split lint in 5 shapes, tie-offs vs reset | R791-1 | `6584b7bfdf19e923153820c60190d87964e8f57b` |
| Robustness | UNCLEAN (F4) | tap overflow (probe), window restart and tag discard, the commit edge under busy refusal, reset sources of sys and milan_cd (one PLL), publication coherence | R791-1 | `6584b7bfdf19e923153820c60190d87964e8f57b` |
| Tests | UNCLEAN (F1, F2, F3, F4, F5) | split leg 48/48 and the author's 13/13 mutants reproduced; 10 reviewer mutants; 3 reviewer CDC plants; ctrl_boundary probe; naming ratchet; the exact-head hosted job logs; SoC-vs-tb wiring | R791-1 | `6584b7bfdf19e923153820c60190d87964e8f57b` |
| Docs | UNCLEAN (F2, F5); RESIDUE F6, F7 | MAILBOX_SPLIT.md diff, ARCHITECTURE_HW_SW_SPLIT.md, ENDSTATION_BUILDER.md, integrator pages, milan_dp README, MODULE_MATRIX and README-tests, PP_SHADOW_BASELINE_RECIPE.md, CDC census regeneration, the firmware README figure, the PR body | R791-1 | `6584b7bfdf19e923153820c60190d87964e8f57b` |

## Real limits

- I did not regenerate the gateware export of the five configs. Finding (1)'s export half rests on the author's receipts and a reading of their comparison script. The netlist half I re-ran.
- The base tree for the identity check is a `git archive` of `a9d69c77`, with each submodule archived at the base's gitlink, in scratch git repositories. It is not a clone.
- The identity digest covers the datapath module with every other module as a blackbox. The only HDL files the delta changes are `milan_datapath.sv`, the new `KL_ctrl_split.sv` and the two new mailbox crossings, so no submodule source instantiated in the all-fabric build changed.
- I did not run:
  - the full sweep, the Yosys area synthesis, the Vivado placement or the full builder bank;
  - `test_ctrl_firmware.py`, or the full `ctrl_boundary` self-test with its builds (only the two judgements that failed hosted, via a probe);
  - the docs gates other than the naming ratchet and the CDC census regeneration;
  - behave.
- Physical calibration NOT RUN. Field skips are not hardware proof, and no hardware was used.
- No manager source bank runs at this head, and none is claimed or inferred.
- The hosted evidence was inspected read-only. At the exact head, 3 executed jobs failed (F1, F2), 30 were cancelled by fail-fast and 1 was skipped. `rtl-fast`, 18 of the 19 Verilator shards and all 4 Yosys shards were cancelled, not executed.

## Pending manager duties

- Hosted acceptance at the exact head. The required contexts are red or cancelled: `docs-check`, `verilator-suites`, `yosys-portability` and `elaborate` failed, and `rtl-fast` was cancelled.
- The current-dev merge candidate: builder and native banks at the merge turn (source base `a9d69c77`, live dev `1eb5289d`).
- The external review (R792).
- Carry RESIDUE F6 and F7 to the residue checklist.
- Open a public Issue for `KL_pp_shadow`'s identical uncounted-drop defect (F4).
- S6b owes the EDIT, class-E, counter-change and GM coverage, and the CI job for `make split-cdc`, which should follow F5's strengthening.

## Receipts

All listed in MANIFEST.sha256. Scripts are in `scripts/`, raw outputs in `receipts/`. The clone was restored and verified: index entries equal the HEAD tree, the worktree is clean, and every submodule is clean at its gitlink (receipts/restore-verify.txt).

R791-1 FINISHED

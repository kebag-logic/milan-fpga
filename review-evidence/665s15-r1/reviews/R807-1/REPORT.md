[R807] NEGATIVE - exact head 7aa6ef0c0312818fc8da36d39bbc468f54ac265b

# R807-1: internal cleared-context review of PR #864 (issue #859, part of #665, Mark II split S15)

- Head under review: `7aa6ef0c0312818fc8da36d39bbc468f54ac265b`, tree `18a65c314bc65ecd804acb6c30d04dbe8b01182a`, base `dev-soft-core` `1d6bf5556ae28764361d85012b86394eb467d294` (19 commits, 48 files, +2023/-128).
- Reconstructed from: AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #859 (body, the assignment, the STOP, the round 2 ruling, the three TAKEN and two REVIEW READY comments), the PR body, the diff `1d6bf555..7aa6ef0c` and its history, and the published evidence at `74cae218` `review-evidence/665s15-r1`.
- Prior public review findings on PR #864: none. The PR's only comments are the two review-start notices. The one earlier finding on the lane, the author's own MINOR that the byte-identity gate reused builder gate number 40, is resolved at this head: `c81640ad` renumbers it to 41, `sw/builder/test_declarations.py` alone carries `[gate 40]`, and `sw/builder/test_builder.py` alone carries `[gate 41]` (`receipts/gates/test_builder_subset.log`).
- Verdict: NEGATIVE. One MAJOR and three MINOR findings are open; one RESIDUE and two SUGGESTIONs are recorded.

## Findings

### R807-1-F1 MAJOR - Conformance, RTL, Robustness, Tests, Docs - the 32x32 image builds tsn-c-stack's ACMP at 33 sinks, past its 32-bit owed-release mask: sink 32 and sink 0 alias

- **Where:** `sw/firmware/ctrl/test/ctrl_srp_image.py:77-89` (`acmp_sizing`, which passes `-DACMP_MAX_SINKS=33u -DACMP_MAX_SOURCES=33u`; the head's 32x32 image report `receipts/harness/H32-image-size.json` carries exactly those flags), against `third_party/tsn-c-stack/include/acmp.h:400` (`uint32_t release`) and `third_party/tsn-c-stack/src/acmp.c:310`, `:816`, `:871`, `:1225` (`1u << k`, `(release >> k) & 1u`, `(o->release >> k) & 1u`). The census's description of the effect is at `docs/design/SHAPE_32X32_CENSUS.md:242`.
- **Authority/evidence:** the assignment's item 4 on #859 ("Upstream sizing changes, if any, go as donor PRs: lwSRP, tsn-c-stack"); the round 2 ruling's item 4, whose premise was that `acmp.h` "already allows" 33 sinks through its defines; AGENTS.md section 2 (a conflict between a ruling and the requirements is published and marked as needing a decision); AGENTS.md section 7 (a defect left in the tree is not resolved, and one not even moved to an issue is not either); C11 6.5.7p3 (a shift count not below the width of the promoted operand is undefined behaviour); Milan v1.2 5.5 and #653 (a sink's change notice waits only behind its own owed response).
- **Probe** (`scripts/acmp_mask_probe.sh`, `scripts/acmp_mask_probe.cpp`): the pinned stack compiled with `ACMP_MAX_SINKS=33u` and `-fsanitize=shift`. A BIND_RX for sink 32 with no transmit room stops at `src/acmp.c:816:31: runtime error: shift exponent 32 is too large for 32-bit type 'unsigned int'` (`receipts/acmp_mask_probe_33.log`). Run so that it continues after each report, it also reports `acmp.c:310:75`, and then shows `change_owed[32]=1 change_owed[0]=1`: sink 0, which owes nothing, is held. A BIND_RX for sink 0 likewise holds sink 32 (`change_owed[32]=1`); both checks fail (`receipts/acmp_mask_probe_33_recover.log`). The control is a scratch copy of the stack with the mask and its four shifts widened to 64 bits (`receipts/acmp_mask_widened_control.diff`); the same probe passes on it, 2 of 2 (`receipts/acmp_mask_probe_33_widened_control.log`). The probe therefore fails for this defect and for no other reason.
- **Impact:** the simulation shape's firmware, the one S2's harness measures at 32x32/2if and S2b grades, runs undefined behaviour in ACMP's response-before-notice ordering (#653). On RV32 and on the host, a shift masks its count to 5 bits, so sink 32 (the CRF sink) and sink 0 hold each other's change notices behind each other's owed responses. The census says the CRF sink's "change notice is not held behind its owed response". The probe shows the opposite failure: the CRF sink is held, and so is sink 0, which should not be. The PR itself adds `_Static_assert(ACMP_MAX_SINKS <= 32u, ...)` for its own 32-bit bindings word (`sw/firmware/ctrl/app/ctrl_app_aecp.c:17`). The stack's mask, the same hazard, gets no such guard. No gate at the shape detects the alias, and no issue tracks it. The donor patch is drafted but not part of the PR.
- **Required outcome:** before merge, either (a) the stack's owed-release mask holds every sink the shape builds, landed as the donor change the assignment asks for together with the submodule pin it needs, or (b) a recorded maintainer decision accepts the alias for the simulation shape, with an issue filed, a build-time refusal or marker so that the shape's rows are not read as alias-free, and the census row corrected to the effect the probe shows. In both cases the census describes the effect accurately.
- **Verification:** `scripts/acmp_mask_probe.sh <tsn-c-stack> <out> 33` exits 0 against the stack the head pins, with no shift report; or the decision, the issue and the guard are linked from the census row; and the 32x32 point is re-run on the resulting image.

### R807-1-F2 MINOR - Conformance, Robustness, Docs - the shape's ACMP transmit ring is below the lane's own derived rule at 32x32, and the ring is neither sized nor filed

- **Where:** `docs/design/SHAPE_32X32_CENSUS.md:230-238` (transmit table: "**short at 32x32** (finding): 20 of 33 leave and the rest are lost to a TMR_NO_RESP retry ... The rule gives 660 words, a 1,024-word ring, or 21 owed frames"; ":238 No ring or bucket of the shape's layout differs from the contract's ... sizing them is a decision for the issue each is filed under"); `sw/mailbox/mailbox_model.py:741-771` (`with_shape`: no ring moves). The contract's figures, read at the head: acmp `tx_words` 256, `burst` 16, `rx_words` 256; maap `rx_words` 128, `burst` 8.
- **Authority/evidence:** the assignment's item 3 ("Each ring depth and bucket is derived from a protocol rate or timer, citing its clause, never fitted to a run"); the round 2 ruling's item 4 ("Each ring and bucket comes from a cited rate or timer"); AGENTS.md section 4 (newly discovered work becomes a public issue); AGENTS.md section 2 (a choice the task cannot make is published as needing a decision). The REVIEW READY comment says "items 1 to 4 are met".
- **Impact:** at the one channel where the lane's rule and the contract's constant disagree at the new shape (ACMP transmit at 32x32: 20 of a possible 33 PROBE_TX_COMMANDs in one pass), the shape keeps the constant. The ruling's "comes from a cited rate or timer" is met only as a derivation on paper, while the layout the harness measures takes the constant. Neither this shortfall nor the two every-shape shortfalls (ACMP receive 12 of 16, MAAP receive 7 of 8) has an issue: the PR lists them under "Findings, each needing its own issue". The claim that items 1 to 4 are met overstates item 3 and the ruling's item 4.
- **Required outcome:** either the shape layout sizes the ACMP transmit ring (or the owed-frame count) from the stated rule and the point is re-run, or a public decision records that the shape keeps the contract's ring. Each shortfall gets an owner issue linked from its census row, and the acceptance statement says which ring items are met and which are owed.
- **Verification:** the census rows name an issue or a decision. If the ring is resized, the shape's generated `mbx_contract.h` shows the new `tx_words`, and the 32x32 point is re-run.

### R807-1-F3 MINOR - Docs, Conformance - census limits crossed at 32x32 without an owner, a dangling pointer, and a stale current-state citation

- **Where:** `docs/design/SHAPE_32X32_CENSUS.md`:
  - `:82` (the `aem` flash slot, 64 KiB, against the 69,488 B image at 32x32: no owner);
  - `:70` (COUNTERS_CHANGED bits, 16 per direction against 33: no owner);
  - `:244` (SRP declares every source on each interface: no issue);
  - `:194` (the hook harness "do[es] not (below)", but nothing below gives a reason or an owner for the hook harness; the F5 stream counters at `:139` are likewise not carried into section 5);
  - `:210` (the current-state table "Owed to #823 and #640" cites `hdl/milan/milan_datapath.sv:5228-5232` for the channel-map writer's guard).
- **Authority/evidence:** the scope of #859 ("every per-shape limit 32x32/2if crosses"); the assignment's item 1 ("Name the rule each limit follows"); the ruling's item 3 (the five guards recorded as owed to #640); AGENTS.md section 4 (new findings become issues). At the head the guard is at `hdl/milan/milan_datapath.sv:5354-5358`: the sync brought in 438 lines of `milan_datapath.sv` from `dev-soft-core`, and `:5228-5232` now holds an `amap_in_store_r` write. The head's own elaboration at 32 streams reports `milan_datapath.sv:5358:5` (`receipts/datapath_lint_32.log`, command in `receipts/datapath_lint_32_cmd.txt`; the five guards still fire: `KL_nvm_backend.sv:286`, `KL_render_queue.sv:325`, `KL_talker_diag_ctx.sv:132`, `KL_media_clock_restart.sv:197`, `milan_datapath.sv:5358`).
- **Impact:** a reader of the census cannot tell who owes these crossed limits. The PR's "Findings, each needing its own issue" have no issue, so each can be lost at merge. The section-5 table owed to #640 points at the wrong RTL for one of its five guards. Sections 1 to 4 are labelled as measured at `a9d69c77`, so their line numbers are not findings; section 5 is the head's state and carries no such label.
- **Required outcome:** every crossed limit in the census names an owner issue (existing or new) or states why none is owed. The hook harness and F5 counters get their reason. The section-5 guard citation matches the head (or the section states the commit its lines are at).
- **Verification:** reread the census rows against `git grep` at the merge candidate, and rerun the elaboration at 32 streams.

### R807-1-F4 MINOR - Conformance, Tests - the ruling's item 5 comparison (measured cost per item type next to S2b's projection, with the error) is not at this head

- **Where:** the PR body, Known limitations ("compared in round 2, on round 2's firmware ... they were not re-measured in the sync"); the comparison exists only as round 2 evidence (`review-evidence/665s15-r1/author/a752b/receipts/costs/project-vs-measured.md` at `74cae218`), on an image that this head no longer links.
- **Authority/evidence:** the round 2 ruling's item 5 ("Put your measured costs per item type next to its projection, and give the error where both exist") and its Done means ("items 1 to 5 are committed and gated"). At the head the 32x32 image is `5b0c3ce2...` (`receipts/image_identity_8x8.txt`). Its rom need is 155,196 B, against the 155,188 B that `docs/design/SPLIT_CONTROL_MEMORY.md` section 8 records at `4ebd2a3b`.
- **Impact:** the costs this base can measure (`record.*`, `rebuild`, `centisecond`) have no comparison against the head's image. The remaining costs are listed as unmeasurable on this base, which is why the PR only "Relates to #859". Item 5 is therefore open for the measurable costs as well as for the unmeasurable ones, and no ruling has accepted either as owed.
- **Required outcome:** the measurable costs are re-measured on the head's (or the merge candidate's) 32x32 image and published next to the projection with the error, and a public decision states where the unmeasurable ones are owed (or that #859 stays open for them).
- **Verification:** a published table at the merge candidate's image hash.

### R807-1-R1 RESIDUE - an issue-comment ID in a new source comment

- **Where:** `sw/builder/endstation_builder.py:201`: `#: at that shape (#859, ruling issuecomment-6727773362, item 1).`
- **Authority:** the owner's comment rule of 2026-10-15 (source comments never show issue-comment IDs; a new instance in the reviewed delta is RESIDUE).
- **Exact fix:** `#: at that shape (#859).`
- **Scope:** this is the only instance in the delta's source files. The deny-list scan for lane labels, review rounds, reviewer IDs and issue-comment IDs over every added non-markdown line in `1d6bf555..7aa6ef0c` finds no other.

### R807-1-S1 SUGGESTION - refresh the simulation map's fit table at the merge head

`docs/design/SPLIT_CONTROL_MEMORY.md` section 8 gives the 32x32 fit "at `4ebd2a3b`": rom need 155,188 B. The head's image needs 155,196 B; banks, tiles (114.0), the 237,568 B over the budget and the five largest objects are unchanged (`receipts/harness/H32-build-soc.json`, `ctrl_plan`). The table is true as labelled. Restating it at the merge head would let a reader use it without a second link.

### R807-1-S2 SUGGESTION - two small test and message gaps

- Gate 39 (`sw/builder/test_builder.py:29362`, `_simulation_refusals`) plants the `--write-rtl` and `--write-fragment` refusals but not `srp.rtl_table`, which `build()` also refuses for a simulation shape (`sw/builder/endstation_builder.py:6156`, `owns`).
- `ctrl_memory.simulated()` (`sw/litex/ctrl_memory.py:257`) raises its identity mismatch under the `budget` rule, which prints as "allocation over budget: the simulation map ... is for the endstation_ax7101_32x32 image alone" (`receipts/gates/ctrl_memory.log`): the label says budget for what is an identity refusal.

## Scope items, one by one

1. **Census, each limit with its owner.** Present: `docs/design/SHAPE_32X32_CENSUS.md` covers the generators, the contract's tables and its rings and buckets, the AEM image (69,488 B against the 64 KiB `aem` flash slot), the SRP pool (144,832 B from `srp_mbx.h`'s formula), the name store (#823), the saved-state records (#823), the stream ID ranges, the firmware memory map (#640) and the five datapath guards (#640), each with a file:line. The AEM descriptor ROM at the shape is 41,465 B (`AEM_ROM_BYTES_C` in the head's builder output `aecp_aem_rom.svh`), so the 64 KiB ceiling the shape crosses is the flash slot's, not the ROM's. The owners are incomplete (F3), as are the ring shortfalls (F2) and the ACMP mask (F1).
2. **Simulation-only, and the route refused.** Met. `simulation_only: true` and `saved_state: none` are refused on any other shape (gate 39, two plants each turned red). `build()` refuses `--write-rtl` and `--write-fragment` by their words (`receipts/gates/builder32_write_rtl.log`, rc 1). `emit_soc_argv` adds `--simulation-only`, and `milan_soc.py` refuses `--build` and `--load` with it (`test_soc_options.py`: 4 CLI cases, 2 killed controls). Independently, `BUILD_CFG=configs/endstation_ax7101_32x32.yaml ./build.sh ax7101 --dry-run` reports that the launch would be refused by the entity-shape check, and the argv it would launch carries `--simulation-only ... --build`, which `milan_soc.py` refuses (`receipts/build_sh_dry_32x32.log`); the tree was clean afterwards.
3. **Contract sizing from its own rule.** The tables are met. `gen_mailbox.shape_streams` reads the counts from the builder's own ADP derivation (33 and 33), and `per_interface` splits them by n mod 2 into 17 on the primary. Nothing is a mirrored constant. The generator's self-test refuses a layout one sink entry short by its words. A disposable probe that removes the generator's check and links the firmware against that short layout is refused by `acmp_mbx.c:15` and `:16` ("every sink needs a bound-talker entry", "every sink needs a publication entry"; `receipts/probe_short_layout_link.log`, the probe's edit in `receipts/probe_short_layout.diff`). The rings and buckets are not met (F2).
4. **Firmware links on a simulation-only map, the excess ledgered to #640.** Met. The head's 32x32 image links into `32x32-two-interfaces` (rom 256 KiB, sram 512 KiB at the split origins). Its plan is 114.0 RAMB36: rom need 155,196 B, sram 310,544 B, 237,568 B over the 229,376 B budget, owed to #640 by region and by the five largest objects (`image_arena` 144,832 B, `aecp_entity_image` 69,488 B, `image_maps` 67,584 B, `image_values` 41,465 B, `image_app` 15,136 B; `receipts/harness/H32-build-soc.json`). It links no store symbol and builds ACMP at 33/33 (`receipts/harness/H32-image-size.json`), which is where F1 enters.
5. **Mailbox elaborates and runs in Verilator; S2's harness records every row at 32x32/2if with 0 refusals.** Met for the mailbox and the harness. At the head, on a clean clone, `ctrl_service_budget/build.py` then `run.py --point 32x32 --reuse-build --record-budget-findings` ended rc 0 with "17 groups graded, 0 refusals, 90 T_svc misses (90 of 182 probe instances, 56 of 129 paths), 10 save groups owed to #823". Each save group is named in an `OWED` line, in `results.json`'s `owed` and in the table's last line, and none is graded. The 90 `BUDGET` lines, the 10 `OWED` lines and the summary are identical to the author's published 32x32 run (`receipts/harness/H32-run.log`, `H32-results.json`, `H32-table.md`). The build took 17.0 s at a 358,044 kB peak. The run took 2 h 33 min 53 s at a 53,104 kB peak, on a host whose CPUs were shared three ways (`H32-build.time`, `H32-run.time`). The mailbox at the shape is the Verilated test SoC's `KL_mbx` from `gen_mailbox.py --variant-shape` (17 bound-talker entries at `0x3400`, publication stride `0x400`; `receipts/harness/H32-build-soc.json` records `mailbox_layout: shape`). The misses are recorded, not graded, as the ruling says. The datapath at the shape is owed to #640 under the ruling: the head's elaboration at 32 streams stops on the five guards (`receipts/datapath_lint_32.log`). The mailbox variant at the shape lints under `-Wall` exactly as the shipped two-interface variant does, apart from one unused constant, `MBX_ENTRY_ORDINAL_C` (`receipts/mbx_lint_32x32.log`, `receipts/mbx_lint_if2.log`: only UNUSEDPARAM warnings, 62 against 61).
6. **No existing shape's output changes; the twin equals the base.** Met. All five shipped configs, through each tree's own builder and generators, give 89 digests (every builder output, the design argv, the three firmware entity headers, and the one- and two-interface mailbox variants), byte-identical at `1d6bf555` and at the head (`receipts/digests_base.json`, `receipts/digests_head.json`; `scripts/shape_digests.py`). Gate 41 passes with its plant turned red. The 8x8/2if firmware image is byte-identical (`548a04b1...`, `receipts/image_identity_8x8.txt`), as are the harness's testbench config, its gateware (apart from timestamps) and its scripts (`receipts/harness_8x8_scripts_*.sha256`). The twin exits 0 with "twin: 0 finding(s)" at both the head and the base, and the two `report.json` files are byte-identical to each other and to both published ones (`41e234b1...`; `receipts/twin_*`).
7. **The `load_config` move is the branch's own lines.** Met. `7aa6ef0c` touches only `_load_streams`'s signature and its `cap` line, both added by this branch, and the call, which goes back to the base's own line. Against `1d6bf555`, `load_config` gains three lines and loses none. The merge `df362e7c`'s combined diff shows only the `load_config` and `emit_soc_argv` regions, with both sides' arms kept. `check_py_idiom.py` passes.
8. **8x8/2if T_svc misses 57 -> 63 reproduced at the base.** Reproduced. At the base `1d6bf555`, on a clean clone, the 8x8/2if point ended rc 0 with "17 groups graded, 0 refusals, 63 T_svc misses (63 of 182 probe instances, 31 of 129 paths)". Its 63 `BUDGET` lines and its summary are identical to this review's head run and to the author's published head run, and `results.json` is equal apart from the build hash (`receipts/harness/B8-*`, `H8-*`). With the image, testbench config, gateware and scripts byte-identical (item 6), the move from round 2's 57 came with `dev-soft-core`, not from this branch.

## Lens results

Every lens was applied at the head. Each is UNCLEAN because of the open findings filed under it. The parts of each lens that came out clean are recorded in the same format, so that a re-review covers only what is open.

- **Conformance** (UNCLEAN: F1 MAJOR, F2, F3, F4 MINOR).
  - Examined: issue #859's scope, the assignment and the round 2 ruling, item by item, against `configs/endstation_ax7101_32x32.yaml`, `sw/builder/endstation_builder.py` (`_load_simulation`, `_streams`, `build`, `emit_soc_argv`, `_marks_srp`), `sw/litex/milan_soc.py` (`--simulation-only`), `sw/mailbox/gen_mailbox.py` and `sw/mailbox/mailbox_model.py` (`with_shape`), `sw/litex/ctrl_memory.py` (`SIMULATION`), the firmware's `MBX_ENTRY_ORDINAL` paths and the census's clauses.
  - Clean within the lens: `[R807] PASS Conformance - configs/endstation_ax7101_32x32.yaml, endstation_builder.py:196-247, milan_soc.py main(), gen_mailbox.py:196-248, ctrl_memory.py:227-288 - items 2, 3 (tables), 4, 6, 7 and 8 met against the ruling, each with its gate or probe above`.
- **RTL** (UNCLEAN: F1 MAJOR, under architecture and interface contracts: the stack's `ACMP_MAX_SINKS` define is used past the width of the mask it feeds).
  - Examined: the generated mailbox at the shape (`KL_mbx_pkg.sv`, `KL_mbx.sv`, the bound-talker decode's 5-bit entry field holding 17, the window placement), its `-Wall` lint against the shipped two-interface variant, the head's datapath elaboration at 32 streams, the tracked `configs/generated/endstation_ax7101_32x32/gen/adp_shape_defaults.svh` against its generator, and the census's guard citations.
  - Clean within the lens: `[R807] PASS RTL - receipts/mbx_lint_32x32.log, receipts/mbx_lint_if2.log, receipts/datapath_lint_32.log - the shape's mailbox lints with UNUSEDPARAM only, as the shipped variant does; no hdl/ source changed in 1d6bf555..HEAD; the datapath refuses the shape at its five guards, owed to #640`.
- **Robustness** (UNCLEAN: F1 MAJOR at the 33-sink boundary; F2 MINOR on transmit backpressure).
  - Examined: the boundaries 16, 17, 32 and 33 in the builder, the contract layout, the firmware masks (`maap_mbx_demand`, `ctrl_app_aecp.c` bindings, `srp_mbx.c`, `ctrl_plat.c`) and tsn-c-stack's `acmp.c`; the refusals for `saved_state` values and for an image that is not the simulation map's; the firmware link against a layout one entry short; the stream placement check in `acmp_mbx_init`.
  - Clean within the lens: `[R807] PASS Robustness - receipts/probe_short_layout_link.log, receipts/gates/ctrl_memory.log, receipts/gates/test_builder_subset.log - the short layout, a foreign image on the simulation map and an unknown or misplaced saved_state are each refused by their words`.
- **Tests** (UNCLEAN: F1 MAJOR, since no gate at the shape detects the alias the probe shows; F4 MINOR).
  - Examined: gate 39 and its two plants, gate 41 and its plant, `test_soc_options.py`'s route refusal and its two kills, `gen_mailbox.py --selftest`'s two shape arms, `test_ctrl_memory.py`'s simulation-map arm and its plant, `selftest_shape.py`'s checks, and the harness at three runs against the published ones.
  - Clean within the lens: `[R807] PASS Tests - receipts/gates/*.log, receipts/harness/*, receipts/digests_*.json - every new gate passes and its plant turns it red; the harness rows reproduce the author's exactly at 32x32/2if and at 8x8/2if (head and base)`.
- **Docs** (UNCLEAN: F1 MAJOR, whose census row misdescribes the alias; F3 MINOR). RESIDUE R807-1-R1 and SUGGESTION S1 are recorded as well.
  - Examined: `docs/design/SHAPE_32X32_CENSUS.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` section 8, `docs/ENDSTATION_BUILDER.md` rows 0a and 0b, `docs/README.md`, the two harness READMEs, the PR body, and the delta's source comments against the comment rule.
  - Clean within the lens: `[R807] PASS Docs - receipts/gates/docs_check.log; SPLIT_CONTROL_MEMORY.md section 8; MAILBOX_SPLIT.md shape layout paragraph - docs_check clean; the memory map and layout prose match the head's soc.json and generated contract (0x3400, stride 0x400, sinks at 0x110 and 0x210)`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | issue #859 scope, assignment, ruling; 32x32 config; builder; milan_soc.py; gen_mailbox.py; mailbox_model.py; ctrl_memory.py; census clauses; F1, F2, F3, F4 open | R807-1 | `7aa6ef0c0312818fc8da36d39bbc468f54ac265b` |
| RTL | UNCLEAN | generated KL_mbx_pkg.sv/KL_mbx.sv at the shape, -Wall lint against if2; datapath elaboration at 32 streams; tracked 32x32 shape include; tsn-c-stack acmp.h:400 against ACMP_MAX_SINKS=33; F1 open | R807-1 | `7aa6ef0c0312818fc8da36d39bbc468f54ac265b` |
| Robustness | UNCLEAN | 16/17/32/33 boundaries in builder, layout, firmware masks, acmp.c; refusals; short-layout link probe; F1, F2 open | R807-1 | `7aa6ef0c0312818fc8da36d39bbc468f54ac265b` |
| Tests | UNCLEAN | gates 39 and 41 with plants; test_soc_options; gen_mailbox selftest; test_ctrl_memory; selftest_shape; harness 32x32 and 8x8 (head and base); twin (head and base); ACMP mask probe and control; F1, F4 open | R807-1 | `7aa6ef0c0312818fc8da36d39bbc468f54ac265b` |
| Docs | UNCLEAN | SHAPE_32X32_CENSUS.md; MAILBOX_SPLIT.md; SPLIT_CONTROL_MEMORY.md section 8; ENDSTATION_BUILDER.md 0a/0b; READMEs; PR body; source comments; F1, F3 open (R1 RESIDUE, S1 SUGGESTION) | R807-1 | `7aa6ef0c0312818fc8da36d39bbc468f54ac265b` |

## Gates run at the head by this review

Each gate ran on a fresh clean clone at the head (the clone script is `scripts/clone.sh`; the submodules come from the review clone's checkouts, with no network). The environment is `scripts/env.sh`: the product LiteX venv, the pinned RV32 SDK, the pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), sv2v and make 4.3. Logs and rc files are under `receipts/gates/` (`scripts/gates.sh`).

| Gate | rc | Result |
|---|---:|---|
| builder on `endstation_ax7101_32x32.yaml` | 0 | outputs written, no routed output, tree clean afterwards (the tracked shape include equals the generator's) |
| the same with `--write-rtl` | 1 | refused: "is a simulation-only shape (#859): it takes no --write-rtl ... no --write-fragment" (intended) |
| `test_builder.py --gates test_control_placement_key,test_simulation_shape_option,test_shipped_shape_outputs_unchanged` | 0 | ALL GATES PASS (3 of 108); gate 39 2/2 plants red; gate 41 33 outputs, 1/1 plant red |
| `check_py_idiom.py` | 0 | at the ratchets |
| `test_soc_options.py` | 0 | RESULT: PASS; 4 CLI cases, 2 killed controls |
| `gen_mailbox.py --check --crosscheck`, `--selftest`, `--variant-shape` | 0, 0, 0 | 0 arms failed; the short layout refused by its words |
| `test_ctrl_memory.py` | 0 | 0 failures, the simulation-map arm and its plant included |
| `ctrl_service_budget/run.py --self-test` | 0 | 0 failures; the shape checks PASS |
| `nvm_split_target/run.py --point 32x32` | 1 | the 10 save groups listed as owed to #823, nothing built (intended) |
| `docs_check.py` | 0 | 0 findings over 218 md and 1,521 scrubbed text files |
| `check_nvm_record_space.py` | 0 | 0 findings across the 5 shipped configs |
| `check_baremetal_only.py --check` | 0 | pass |
| `git diff --check 1d6bf555 HEAD` | 0 | clean |
| shipped-shape digests, head against base | 0, 0 | 89 of 89 equal |
| twin, head and base | 0, 0 | 0 findings each; reports byte-identical |
| harness 32x32/2if, 8x8/2if (head), 8x8/2if (base) | 0, 0, 0 | see item 5 and item 8 |
| mailbox `-Wall` lint, shape variant and two-interface variant | - | UNUSEDPARAM only, 62 and 61 |
| datapath elaboration at 32 streams | 1 | the five guards (intended; owed to #640) |
| probes: ACMP mask at 33 sinks, the widened control, the short-layout link | 1, 0, 2 | F1 shown, the control green, the short layout refused |

## Real limits of this review

- No full builder, parent, PP, gPTP or Yosys bank ran here, and no workflow replica: those are outside this review's authority. `test_builder.py` ran as the three gates the PR names. The full-sweep, firmware self-test and mutant-campaign figures are the author's published receipts, not re-run here.
- No hosted context was inspected beyond noting that none is relied on: hosted and act acceptance are the manager's.
- No manager source bank ran at this exact head, and none is claimed or inferred. This review validated the source head only, not the current-dev merge candidate (live `dev` `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`).
- Physical calibration was NOT RUN. The shape is simulation-only, and nothing here is hardware evidence.
- The host was heavily shared (load 50 to 120 on its CPUs), so this review's wall-clock and peak-memory figures are not comparable with the author's. The harness grades simulated time, which the host load does not change.
- The clause citations in the census's rings table (Milan v1.2 Tables 4.3, 5.26 and 5.50 and 5.5.2.3; IEEE 1722.1-2021 6.2.2.5; IEEE 1722-2016 B.3.4; IEEE 802.1Q-2018 10.7.4.1) were checked for consistency against their other uses in the tree and the stack's own constants, not against the standards' text.
- The F1 probe drives the stack on the host. RV32's shift instructions mask the count to 5 bits as x86's do, so the aliasing is the same on the target, but the UB itself is the defect whichever way a compiler resolves it.

## Pending manager duties

- Publish this report and the receipts listed in `MANIFEST.sha256`.
- Obtain or record the decisions F1, F2 and F4 ask for (the ACMP mask at 33 sinks; the ACMP transmit ring at the shape; item 5's comparison and the unmeasurable costs), and file the owner issues F2 and F3 ask for.
- Carry R807-1-R1 to the residue checklist.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and own hosted and act acceptance.
- Re-review: after the fixes, re-apply every lens left unclean here at the new head.

R807-1 FINISHED

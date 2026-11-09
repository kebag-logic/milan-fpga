[R806] NEGATIVE - exact head f3e902f2a96bb27eac6ed7780c70905af34f389e

# R806-1: external independent review of #823 round 3 / PR #863

- Head reviewed: `f3e902f2a96bb27eac6ed7780c70905af34f389e`, tree `fb23779a1492fa2192c4683e7f31ef053c026604`. Source base `a9d69c77`.
- Merge probe: a disposable merge of this head onto live `dev-soft-core` `1d6bf5556ae28764361d85012b86394eb467d294` gave merge commit `bf005066`, tree `a643419a`. It merged without textual conflict and is local only.
- Live `dev` is `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`. It was not used: the PR targets `dev-soft-core`.
- Authorities read: AGENTS.md; the #823 body and amendments; the owner's 0.5 s comments; the round 1 assignment; rulings issuecomment-6730773797 (decisions 1, 2 and 6), issuecomment-6730985093 and issuecomment-6739542795; the PR body; the full diff `a9d69c77..f3e902f2`; and the author's published receipts at `1f9fe825`, read only.
- No prior public review finding exists on PR #863. It has 0 reviews and 0 review comments, and its 2 comments are review-start notices. So there is nothing to resolve or retain.
- The other reviewer's report was not read.

## Verdict

NEGATIVE. One MAJOR and four MINOR findings are open, plus three RESIDUE items and two SUGGESTIONs.

The implementation of the record space and framing itself is correct, as far as I read and probed it:
- one declaration, two readers, nothing mirrored;
- the 16-bit id and the 1,129-id space;
- KLJ3 in `journal_klj3`;
- KLJ2 refused `VD_VER` with `legacy` recorded;
- today's journal never written;
- the all-fabric placement untouched.

What fails:
- **F1 (MAJOR):** the format page's drift gate goes red on the merge with current `dev-soft-core`.
- **F2, F3 (MINOR):** two new rules have test gaps. Planted defects I added survive the suite.
- **F4, F7 (MINOR):** two authoritative-document gaps.

## Findings

### F1 — MAJOR — Docs, Tests, Conformance — `scripts/nvm_format_32x32_tables.py:91,152,153` and the layer and cited anchors, run on the merge candidate — the page's drift gate is red after merging with `dev-soft-core`

- **Authority:** item (8) of the review brief, which asks for semantic conflicts on the merged result.
  - Ruling issuecomment-6730985093: "Update the design page … Keep its drift gate green."
  - AGENTS section 7: the candidate merge result is validated.
  - This PR adds `check_nvm_format_32x32.py` and its `--self-test` to the docs workflow's `NVM record-space gate` step (`.github/workflows/docs.yml:332-333`, `gate_26`).
- **Evidence:**
  - At head, `check_nvm_format_32x32.py` reports 0 findings (`receipts/check_nvm_format_32x32.log`).
  - On merge `bf005066` it exits 1 with 5 findings (`receipts/merged_check_nvm_format_32x32.log`). Its own clean-tree control fails too: `receipts/merged_check_nvm_format_32x32_selftest.log`, "clean tree: 5 finding(s)", rc 1.
  - The moved anchors (`receipts/merged_anchor_moves.txt`):

    | Anchor at head | On the merge |
    |---|---|
    | `sw/litex/milan_soc.py:4682` | 4872 |
    | `sw/litex/milan_soc.py:3367` | 3550 |
    | `sw/litex/milan_soc.py:3352` | 3535 |
    | `hdl/milan/milan_datapath.sv:5252` | 5378 |
    | `hdl/milan/milan_datapath.sv:5211` | 5337 |

    S6a/S6b added 237 lines to `milan_soc.py` and changed `milan_datapath.sv`.
- **Impact:** merging this head as it stands turns the `docs` workflow red on `dev-soft-core`. The anchors fix whole line numbers in shared files that other lanes edit, so the same breakage comes back with any unrelated edit above an anchor.
- **Required outcome:** at a head that includes current `dev-soft-core`, `python3 scripts/check_nvm_format_32x32.py` and its `--self-test` both exit 0, with every anchor pointing at its token. See also S1.
- **Verification:** both commands on the corrected head and on the manager's merge candidate, each exit 0 with 0 findings.

### F2 — MINOR — Tests — `sw/firmware/ctrl_nvm/test/test_nvm_boot.cpp:147-191`, `sw/firmware/ctrl_nvm/test/nvm_rig.cpp:517-520` — the `legacy` rule's negative paths and placement are not pinned

- **Authority:**
  - Decision 2: refuse KLJ2, boot blank, and record the reason.
  - The rule as the head states it (`nvm_store.h:113-119`, `nvm_store.c:408-418,465-472`, page section 5): a KLJ2 header sets `legacy`, and only when the store's own slots are blank does the verdict become `VD_VER`.
  - AGENTS section 6, Tests lens: positive, negative and boundary behaviour; tests must not merely reproduce implementation assumptions.
- **Evidence:** reviewer probes, each planted into a copy of the head at 1x1, with every binary's whole suite run (`scripts/f1_probe.py`, `receipts/f1_probes_1.log`, `receipts/f1_probes_2.log`). Three survive:

  | Probe | Mutation | Result |
  |---|---|---|
  | `p07_legacy_any_nonblank_header` | `legacy` set for any non-erased header in today's journal, not only KLJ2 | 0 tests fail |
  | `p08_ver_overrides_own_refusal` | `VD_VER` replaces the verdict even when an own slot was refused, not blank | 0 tests fail |
  | `p12_legacy_b_wrong_place` | `NVM_LEGACY_B` moved to `MILAN_FLASH_JOURNAL_OFFSET + MILAN_FLASH_JOURNAL_SIZE` (the `user` slot) | 0 tests fail |

  The rig plants `--legacy-b` at the store's own `NVM_LEGACY_B` (`nvm_rig.cpp:520`). So the "either slot" test cannot detect a wrong address for today's slot B.
- **Impact:** the code at head is correct (an exact magic compare, gated on `VD_BLANK`). But a regression that records a wrong reason, or reads the wrong place for the all-fabric slot B, would pass the gate.
- **Required outcome:** tests that fail on each of these three probes:
  - a non-blank, non-KLJ2 header in today's journal leaves `legacy` 0 and the verdict `VD_BLANK`;
  - an own slot that is refused, with a KLJ2 header in today's journal, keeps the own slot's verdict;
  - today's two slot addresses are checked against a source independent of the store's macros, for example the `FLASHBOOT_RESERVED["journal"]` halves through the fixture.
- **Verification:** `python3 -I scripts/f1_probe.py <tree> <work> --probes --only p07_legacy_any_nonblank_header,p08_ver_overrides_own_refusal,p12_legacy_b_wrong_place`. Each must be CAUGHT, ideally also as planted defects in `nvm_mutants.py`.

### F3 — MINOR — Tests — `sw/firmware/ctrl_nvm/test/test_nvm_capacity.cpp:55-70` (`capacity_round_trip`) — the multi-block erase is graded only on blank flash, so its addressing is unproven

- **Authority:**
  - This round's one change to the whole-image commit: "erases every block its container spans". That is `nvm_store.c:686-695,804-808` and page section 3.
  - At the bound shape the base is 548 pages: 140,208 B, three erase blocks.
- **Evidence:**
  - Probe `p05_erase_same_block_twice` erases the slot's first block `NVM_ERASE_BLOCKS` times instead of each block once. It survives the whole suite (`receipts/f1_probes_2.log`).
  - The only multi-block test commits once onto blank flash. It counts the erases but not their addresses, and the blank check passes because block 1 was already blank. The tree's plant `first_block_only` is caught only because it changes the count.
- **Impact:** such a defect would make every later commit into a used slot fail its blank check (`VD_ERASE`) at any shape whose container spans more than one block. That is the 32x32 point this format is sized for.
- **Required outcome:** a test whose commit at capacity lands in a slot holding stale data past its first block (for example commits A, B, then A again, or a pre-filled slot), with each erase address checked.
- **Verification:** `p05_erase_same_block_twice` CAUGHT, and the new test named by a planted defect.

### F4 — MINOR — Docs — `docs/design/SAVED_STATE_FASTCONNECT.md:533-552` (section 5); also `sw/litex/milan_soc.py:149-168` — the flash-map table omits the new `journal_klj3` slot

- **Authority:**
  - Decision 3: a 640 KiB journal directly below today's.
  - `FLASHBOOT_RESERVED` now holds `journal_klj3` at `0xE4_0000`, 640 KiB (`milan_soc.py:179`), so every build reserves it, its `flashboot_layout.json` and `MILAN_FLASH_JOURNAL_KLJ3_*` constants included.
  - FASTCONNECT section 5, "Where it lives in the 16 MB QSPI", is presented as the map generated from that dict. It still lists only `journal` and `user`, and its prose says each slot is one erase block.
  - The writable-slot comment block in `milan_soc.py` likewise names only `journal` and `user`.
  - The PR edits FASTCONNECT section 6 but not section 5.
- **Impact:** the authoritative flash map shows `0xE4_0000..0xEE_0000` as unreserved. Deployment and board work that reads the map misses the split's saved state.
- **Required outcome:**
  - FASTCONNECT section 5's table and prose state `journal_klj3`: offset, size, two slots of five erase blocks, written by the split store only, and the all-fabric writer never touching it.
  - The `milan_soc.py` slot comment says the same.
- **Verification:** read section 5 against `python3 sw/litex/flash_map.py` (`receipts/merged_flash_map.log`).

### F7 — MINOR — Docs — `docs/design/SAVED_STATE_FORMAT_32X32.md:376,528` and `scripts/nvm_format_32x32_tables.py:529` (the generated section 8 T16 cell) — the page still calls the gateware VERSION open after it was ruled

- **Authority:** ruling issuecomment-6739542795: the CSR is not moved, no commit is needed, and the "VERSION step" is the format's own chain, which is done.
- **Evidence:**
  - Page line 376: "is not moved, and is an open question".
  - Line 528: "Open: the gateware VERSION … asks for a ruling".
  - The generated T16 cell: "the gateware VERSION open (section 5)".
- **Classification:** MINOR rather than RESIDUE, because the T16 cell is generated by a script string, so the fix touches a generator and a generated block.
- **Impact:** a cold reader of the authoritative page sees an open decision that was taken.
- **Required outcome:** sections 5, 8 and 9 state the ruling: not moved this round, and VERSION 3 lands with the default flip. Regenerate the page and keep its gate green.
- **Verification:** `check_nvm_format_32x32.py` exits 0, and no "open question" remains for VERSION.

### R1 — RESIDUE — Docs — `docs/design/SAVED_STATE_FORMAT_32X32.md:76,243,267,269` — stale prose citations and one stale format name

- **Evidence:** `receipts/head_prose_citations.txt`. The PR's own added lines in `milan_soc.py` and in the builder shifted these lines. The gate checks only its anchor tables, not prose `path:line`.
- **Exact fixes:**
  - :76: `sw/builder/endstation_builder.py:2714` is a blank line at head. Change it to "`aem_name_count`, `sw/builder/endstation_builder.py:2715`" (the refusal is `_adp_name_entries` at `:2739`).
  - :267: `sw/litex/milan_soc.py:3361` becomes `sw/litex/milan_soc.py:3367` at head.
  - :269: `sw/litex/milan_soc.py:3346` becomes `sw/litex/milan_soc.py:3352` at head.
  - :243: "Each segment carries the KLJ2 header" becomes "Each segment carries the container header (KLJ3 in the split)".
  - At the merge, the lines move again (see F1).

### R2 — RESIDUE — Docs — new source comments carrying issue-comment IDs (owner comment rule of 2026-10-15)

- **Evidence:** `receipts/residue_scan_nondoc.txt`. New instances in the delta:
  - `sw/firmware/ctrl_nvm/nvm_layout3.h:4-5`: "scoped to the split by #823 issue comment 6730985093";
  - `sw/builder/test_builder.py:29255`: the same phrase;
  - `scripts/nvm_format_32x32.py:116-117`: "(#823 issue comment 6730985093 item 3)";
  - `scripts/nvm_format_32x32_tables.py:55`: "since #823 issue comment 6730985093".
- **Exact fix:** replace each comment ID with the decision it records. For example: "(#823 decision 1, scoped to the split placement)", and "(#823: the suspend latency graded at its typical value)".
- **Not counted:** lane names that were already on lines this delta merely touched ("#665 lane F1" in `nvm_shape.h:4`, `nvm_klj2.c:3`, `nvm_klj2.h:4`). They are tracked by #746.
- **Optional:** "round 3" and "round 4" in comments and docstrings of `scripts/nvm_format_32x32_tables.py:61,455` are this issue's implementation rounds. Wording them as "this change" / "the append path (#823 decisions 3, 4, 5 and 7)" would follow the rule's intent.

### R3 — RESIDUE — PR body

- "**The gateware VERSION is not moved.** … Posted as an open question on #823." should now cite ruling issuecomment-6739542795: not moved, the format's chain done.
- Its other validation expectations match what I reproduced.

### S1 — SUGGESTION — Tests — `scripts/nvm_format_32x32_tables.py` (`Anchor`, `anchor_findings`)

- Locate each anchor's token by search, with a uniqueness check, or have `--write` refresh anchor lines. Whole line numbers pinned in `milan_soc.py` and `milan_datapath.sv` redden the docs gate on unrelated edits (F1).
- Also check the page's prose `path:line` citations against the same anchors (R1).

### S2 — SUGGESTION — Robustness — `sw/firmware/ctrl_nvm/nvm_klj2.c:30-62` (`nvm_mapin_entries` as `uint8_t`, `nvm_mapout_entries` as `uint16_t`)

- A compile-time assert that each `MILAN_NVM3_MAPIN_ENTRIES_k` is at most 255, and each `MAPOUT` entry at most 65535, would refuse a too-wide count at build time. Today the walk and the sizes disagree and persistence turns off at run time (DR3b), as the comment says.
- No shipped or bound shape reaches either limit: the bound shape has 8 entries per input port and 264 per output port.

## Lens results (clean results carry their artifact)

```text
[R806] UNCLEAN Conformance — merge bf005066, receipts/merged_check_nvm_format_32x32.log — F1: the ruling's "keep its drift gate green" fails on the merged result. Checked and met at head:
  (1) sw/firmware/ctrl_nvm/nvm_layout3.h:36-63 is the one declaration. It is read by scripts/nvm_layout3.py:111-133, the builder's emit_nvm_split (sw/builder/endstation_builder.py:2762-2817), the F1 codec (nvm_shape.h:33-176), the KLJ3 reference (scripts/nvm_klj3.py:47-60) and the F1 bench (nvm_bench.py:80,152). No capacity is restated; gate 39 pins 222/1128/1129 on purpose, as a gate.
  (2) 12 blocks, 1,129 ids, a 16-bit field (receipts/nvm_layout3.log). Gate 39 accepts 907 names at 32x32 TDM8 and refuses 908 (receipts/builder_gates_38_39.log). The reference gate covers 5 shapes (receipts/check_nvm_klj3_selftest.log). The F1 capacity build reaches id 1128 (receipts/f1_named_2.log).
  (3) journal_klj3 at 0xE4_0000+0xA_0000 ends at 0xEE_0000, today's journal (sw/litex/milan_soc.py:174-179). The KLJ2 magic gives VD_VER before any other rule (nvm_klj2.c:284-285). legacy is recorded and the blank verdict becomes VD_VER (nvm_store.c:408-418,465-472). The port refuses program or erase outside journal_klj3 (nvm_flash_litespi.c:179-184).
  (4) git diff a9d69c77..HEAD touches nothing under hdl/, protocol-processor (gitlink a9e84b66 unchanged), sw/firmware/milan_baremetal, sw/firmware/nvm_hosttest, scripts/nvm_klj2.py, scripts/nvm_contract.py or scripts/nvm_shape.py. Gate 38 passes 9/9.
  (5) The commit sequence is unchanged apart from the per-block erase loop (nvm_store.c:686-695,804-808).
  (6) receipts/test_ctrl_nvm_plain.log: 474 tests across 5 shapes, rc 0.
  (7) receipts/check_nvm_format_32x32.log: 0 findings at head.
  (8) Fails: F1.
[R806] PASS RTL — sw/firmware/ctrl_nvm/nvm_klj2.c:30-372, nvm_store.c:57-160,686-808, nvm_shape.h:33-176, host/nvm_fmodel.c:65-90,182-220, and the unchanged all-fabric RTL (hdl/milan/KL_nvm_backend.sv:248, elaborated at 128/129 by gate 38) — widths and indexing: the id is uint16, bytes 4-5 big-endian; rec.off is uint32 for record areas over 64 KiB; NVM_WORDS is rounded up to 36 for 1,129 ids (probe p09, the short array, is caught); the map index is modulo 32 under _Static_asserts; the erase-block counter resets at every seal. The changed interfaces (nvm_fmodel_protect/nvm_fmodel_slots, nvm_bench.shape_header) have no stale caller at head or on the merge (git grep; receipts/merged_twin_fw.log). No RTL is in the delta; the processor pin is unchanged.
[R806] PASS Robustness — nvm_klj2.c:278-372 (refusal order), nvm_store.c:408-418,465-472, nvm_flash_litespi.c:179-184, scripts/nvm_klj3.py:149-216; probes p02, p03, p04, p06, p09, p10 and p11 all CAUGHT (receipts/f1_probes_1.log, receipts/f1_probes_2.log) — malformed input: KLJ2 in an own slot, the reserved byte set, an id past the space, a 64 KiB cap at a 2-block container. A legacy read fault records nothing (legacy_read_fault_recorded caught, receipts/f1_named_1.log). A power cut between per-block erases leaves an erased header, so the slot reads blank. A stale tail past IMG_LEN is never read as records. The behaviour is correct; the test gaps are filed under Tests (F2, F3).
[R806] UNCLEAN Tests — F1, F2 and F3 open. Checked clean: the 13 new F1 plants all caught (receipts/f1_named_1.log 6, receipts/f1_named_2.log 7); 6 re-anchored plants caught (receipts/f1_named_3.log); the reference gate 6/6, and the page gate's 9 plants and clean control at head; gate 39 10/10 and gate 38 9/9; the author's 123/123 receipt cross-read at 1f9fe825.
[R806] UNCLEAN Docs — F1, F4 and F7 open; R1, R2 and R3 residue. Checked clean: the docs/README.md index link; sw/firmware/ctrl_nvm/README.md; docs/design/SPLIT_CONTROL_MEMORY.md (the KLJ3 table and the 3,454/13,594 B stages, matching sw/litex/ctrl_memory_ledger.py:22); tb/verilator/nvm_split_target/README.md; the FASTCONNECT section 6 pointer; the page's statement that the format is the split's and the all-fabric placement keeps KLJ2 (lines 8-11, 142-145, 397); A3 graded at the typical 15 us with a 6,352x margin (lines 321-326).
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Rulings 6730773797 (decisions 1, 2, 6), 6730985093, 6739542795; `nvm_layout3.h`; `nvm_layout3.py`; `emit_nvm_split`; `nvm_shape.h`; `nvm_klj2.c`; `nvm_store.c`; `milan_soc.py:171-180`; gates 38 and 39; merge `bf005066` | R806-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |
| RTL | CLEAN | F1 codec and store widths and indexing; the flash-model API; unchanged `KL_nvm_backend` and processor pin; merged `twin_fw.py` compile (36 units) | R806-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |
| Robustness | CLEAN | Refusal order; `legacy` read faults; power-cut and stale-tail reasoning; 7 malformed-input probes caught | R806-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |
| Tests | UNCLEAN (F1, F2, F3) | `test_ctrl_nvm.py` plain run; 19 tree plants graded; 12 reviewer probes; the reference, page and builder gates at head and on the merge; merged AECP nvm/app and ACMP-NVM arms | R806-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |
| Docs | UNCLEAN (F1, F4, F7) | `SAVED_STATE_FORMAT_32X32.md` in full; FASTCONNECT sections 5 and 6; ctrl_nvm README; SPLIT_CONTROL_MEMORY; split-target README; the delta's source comments | R806-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |

## Gates I ran (exact head unless marked MERGE = `bf005066`)

| Command | Result | Receipt |
|---|---|---|
| `python3 scripts/nvm_layout3.py` | rc 0; 1129 ids, NAME 222..1128 | `receipts/nvm_layout3.log` |
| `python3 scripts/check_nvm_klj3.py --self-test` | rc 0; 6/6 plants caught | `receipts/check_nvm_klj3_selftest.log` |
| `python3 scripts/check_nvm_format_32x32.py` | rc 0; 0 findings | `receipts/check_nvm_format_32x32.log` |
| `python3 scripts/check_nvm_format_32x32.py --self-test` | rc 0; clean control and 9 plants | `receipts/check_nvm_format_32x32_selftest.log` |
| `test_builder.py --gates test_name_count_fits_the_nvm_name_block,test_split_record_space_bounds_the_split_output` | rc 0; 9/9 and 10/10 | `receipts/builder_gates_38_39.log` |
| `test_ctrl_nvm.py --require-rv32 --jobs 8` (no self-test) | rc 0; 474 tests over 5 shapes, 908 names refused at compile time | `receipts/test_ctrl_nvm_plain.log` |
| The tree's plants, graded by the suite's own `plant_and_grade` (`scripts/f1_probe.py --named`) | 19/19 caught | `receipts/f1_named_{1,2,3}.log` |
| Reviewer probes p01-p12 (`scripts/f1_probe.py --probes`) | 8 caught; p05 survived (F3); p07, p08, p12 survived (F2) | `receipts/f1_probes_{1,2}.log` |
| MERGE `check_nvm_format_32x32.py`, and `--self-test` | **rc 1 and rc 1, 5 findings** | `receipts/merged_check_nvm_format_32x32.log`, `receipts/merged_check_nvm_format_32x32_selftest.log` |
| MERGE `check_nvm_klj3.py`, and `--self-test` | rc 0 and rc 0 | `receipts/merged_check_nvm_klj3.log`, `receipts/merged_check_nvm_klj3_selftest.log` |
| MERGE gate 39 | rc 0; 10/10 | `receipts/merged_builder_gate39.log` |
| MERGE `check_nvm_record_space.py`, `gen_flash_port.py --self-test`, `flash_map.py`, `ci_events.py --check` | rc 0 each | `receipts/merged_check_nvm_record_space.log`, `receipts/merged_gen_flash_port_selftest.log`, `receipts/merged_flash_map.log`, `receipts/merged_ci_events_check.log` |
| MERGE `twin_fw.py` (the two-placement simulation's split firmware, new on `dev-soft-core`, which compiles this store) | rc 0; 36 units | `receipts/merged_twin_fw.log` |
| MERGE `aecp_arms.py --nvm` and `--app`; `ctrl_arms.arm_acmpnvm` | rc 0 each: 64, 101 and 7 checks, 0 failures | `receipts/merged_aecp_nvm_arm.log`, `receipts/merged_aecp_app_arm.log`, `receipts/merged_acmpnvm_arm.log` |
| `ci_events.py --check` at head | rc 0 | `receipts/head_ci_events_check.log` |

Receipts named `head_rerun_*` are four commands I meant to run on the merge. A shell grouping error ran them in the head clone instead (all rc 0). They are kept and labelled as head runs, and each was then re-run on the merge as the `merged_*` receipts above.

## Real limits

- **F1 self-test, not run in full by me.** `test_ctrl_nvm.py --require-rv32 --self-test` (all 123 plants) could not finish inside one 10-minute foreground command at host load averages of 65 to 217. Detached background attempts were killed when each tool call ended, so their empty receipts were discarded.
  - What I ran instead: the plain suite (474 tests) and 19 plants through the suite's own `plant_and_grade` (all 13 new plus 6 re-anchored).
  - The author's 123/123 receipt (`extra.ctrl_nvm_selftest_final`, rc 0, at `1f9fe825`) was read, not reproduced.
- **Not run on the merge:**
  - the full control-firmware suite: four slices each hit 585 s; only its AECP nvm/app and ACMP-NVM arms ran;
  - the two-placement simulation itself (`make -C tb/verilator/milan_dp twin`), which needs two Verilator datapath builds;
  - the full sweep, the builder bank, and every workflow's `run:` steps;
  - `sw/litex/test_ctrl_memory.py`: no migen in this environment (`receipts/notrun_merged_test_ctrl_memory_no_migen.log`).
- **Pinned Verilator not used.** No RTL changed in the delta, and gate 38's elaborations used the tool the gate selects.
- **No hardware.** No physical calibration and no target run. The split target harness's recorded results predate KLJ3, as the PR states.
- **No manager source bank** is claimed or inferred at this head.
- **Head clone after probes:** tracked bytes, modes and index are identical to HEAD (index tree `fb23779a`). The six gitlinks are at their recorded commits and each submodule worktree is clean (`receipts/head_clone_integrity.txt`). Only gitignored `__pycache__` directories exist. Every probe ran in disposable copies under `scratch/`.

## Pending manager duties

- Hosted and act acceptance of the exact head.
- The current-dev merge-candidate builder and native banks at the merge turn. F1 shows the candidate's docs gate red until the anchors are refreshed on a head that includes `dev-soft-core`.
- Carry R1, R2 and R3 to the residue checklist.
- Re-review of F1, F2, F3, F4 and F7 at the corrected head. Conformance, Tests and Docs must be covered again; so must RTL and Robustness if the store's C or the gate scripts change.

R806-1 FINISHED

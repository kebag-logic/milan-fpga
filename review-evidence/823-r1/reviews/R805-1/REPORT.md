[R805] NEGATIVE - exact head f3e902f2a96bb27eac6ed7780c70905af34f389e

# R805-1: internal cleared-context review of PR #863 (#823 round 3)

- Head under review: `f3e902f2a96bb27eac6ed7780c70905af34f389e`, tree `fb23779a1492fa2192c4683e7f31ef053c026604`, branch `823-nvm-format` -> `dev-soft-core`.
- Source base: `a9d69c77`. Merge candidate examined: `git merge-tree --write-tree 1d6bf555 f3e902f2` = tree `a643419a36a64bd168c8d5633b7adfb17a521bd1` (clean textual merge). The hosted pull_request runs checked out `refs/pull/863/merge` = `4055401462` "Merge f3e902f2... into 1d6bf555...", the same merge.
- Authorities: #823 body and amendment; rulings issuecomment-6730773797 (decisions 1, 2, 6), issuecomment-6730985093 (round 3 scope), issuecomment-6739542795 (gateware VERSION not moved); AGENTS.md sections 6 and 7; `docs/design/SAVED_STATE_FORMAT_32X32.md`; `docs/design/SAVED_STATE_FASTCONNECT.md` sections 4.2, 5, 6, 7.
- Verdict: **NEGATIVE**. Open findings:
  - 1 MAJOR (F1): the format page's drift gate is red on the merge candidate, and the hosted docs workflow failed on it.
  - 5 MINOR (F2 to F6).
  - 4 RESIDUE (RS1 to RS4).
  - 2 SUGGESTION (SG1, SG2).
  - F4 and F5 are findings of the other reviewer's report at this head. I reproduced each with my own probe and retain them (section "Prior public review findings").

The core of round 3 is correct as far as I read and ran it:
- one declaration (`nvm_layout3.h`), read by both the F1 codec and the builder's split output, with nothing mirrored;
- a correct 16-bit layout;
- KLJ3 in a 640 KiB journal directly below today's;
- KLJ2 refused `VD_VER`, the boot blank and the reason recorded;
- today's journal never written;
- the all-fabric paths untouched;
- the whole-image commit unchanged, apart from erasing every block its container spans.

All 122 planted defects and the compile-time NAME control were caught when I ran them myself.

What blocks:
- the merge with current `dev-soft-core` (F1);
- a stale header length in an asserted bound, which its test pins (F2);
- a flash map that the docs do not show (F3);
- two rules whose regressions the suite cannot see (F4, F5);
- a settled decision still published as open in a generated table (F6).

## Findings

### F1 - MAJOR - Conformance, Tests, Docs - the format page's drift gate is red on the merge candidate

- **Where:** `docs/design/SAVED_STATE_FORMAT_32X32.md` section 6 (the layers table) and the cited anchors, generated from `scripts/nvm_format_32x32_tables.py` (`LAYERS`, and its rows for `milan_soc.py` and `milan_datapath.sv`). The five stale anchors are `sw/litex/milan_soc.py:4682`, `sw/litex/milan_soc.py:3367`, `sw/litex/milan_soc.py:3352`, `hdl/milan/milan_datapath.sv:5252` and `hdl/milan/milan_datapath.sv:5211`.
- **Evidence:**
  - Hosted `docs-gates-0` (job 129147950753, run 42613618773) on `refs/pull/863/merge` failed at step "NVM record-space gate", with exit code 1 (`receipts/hosted/docs-gates-0_129147950753.log`). Its findings: `FINDING: anchor sw/litex/milan_soc.py:4682 no longer reads split_constants(_nvm_split, _nvm_shape)`, plus the four others.
  - The `docs-check`, `elaborate`, `verilator-suites` and `yosys-portability` failures at this head are "Require every gate exactly once" and fail-fast aggregation steps (`receipts/hosted/failed_job_steps.tsv`). No other executed gate failed.
  - I reproduced it on the merge tree `a643419a`: `python3 scripts/check_nvm_format_32x32.py` rc 1, `5 finding(s)` (`receipts/merge/fmt32_on_merge.log`). At the source head it is rc 0 (`receipts/gates/fmt32.log`).
  - The cause is S6a/S6b on `dev-soft-core` (`a9d69c77..1d6bf555`). They changed `sw/litex/milan_soc.py` (+237/-47) and `hdl/milan/milan_datapath.sv`, so the cited lines move. For example, `split_constants(_nvm_split, _nvm_shape)` is line 4682 at the head and line 4872 in the merge.
- **Authority:**
  - issuecomment-6730985093: "Update the design page ... Keep its drift gate green".
  - Focus items 7 and 8.
  - AGENTS.md section 7: the candidate merge result is validated.
- **Impact:**
  - The mandatory docs workflow is red on the merge candidate.
  - Once merged, the page cites five lines that do not say what it claims.
  - This is the semantic conflict in `sw/litex/milan_soc.py` that item 8 asks about. The code in that file merges correctly; the conflict is in the page that cites it.
- **Required outcome:** The page and its anchors are true against current `dev-soft-core`. `check_nvm_format_32x32.py` and its `--self-test` are rc 0 on the merge candidate.
- **Verification:** Both commands rc 0 on the new head's merge with live `dev-soft-core`. Hosted `docs-gates` "NVM record-space gate" green on `refs/pull/863/merge`.

### F2 - MINOR - RTL, Tests, Docs - the store's asserted per-step byte bound still counts the layout 2 header

- **Where:**
  - `sw/firmware/ctrl_nvm/nvm_store.c:575`: `nvm.step_bytes += 6u + r.plen;`
  - `sw/firmware/ctrl_nvm/nvm_store.h:62`: `NVM_STEP_BOUND ... 2u * NVM_PAYLOAD_MAX + 6u`
  - `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:678`: `want = max(NVM_STEP_BYTES, 2 * max_plen + 6)`
  - `sw/firmware/ctrl_nvm/README.md:304-307`: "`max(256, 2 x P + 6)` ... 278 bytes at 1x1 and 1,158 at 8x8"
- **Evidence:**
  - Under layout 3 the frame's crc16 runs over `NVM_REC_HDR - 2` = 8 header bytes plus the payload (`sw/firmware/ctrl_nvm/nvm_klj2.c:229`). Under layout 2 it was 6. This delta changed `nvm_rec_frame` but not the accounting.
  - Disposable probe `scripts/probe_step_bytes.py` (`receipts/probe_step_bytes.log`) grades the way the self-test grades a defect:
    - (A) Only the count corrected to `(NVM_REC_HDR - 2u) + r.plen`: the suite's own invariant fails, `step_max=280 > step_bound=278`.
    - (B) The count and the bound both corrected: `service_bound` fails, `step bytes 280, want 278 (bound 280)`.
- **Authority:**
  - The store's stated contract (`nvm_store.c:52-53`, README "Bytes, asserted"): "No step touches more than NVM_STEP_BOUND bytes: ... one latched record's copy and crc16".
  - AGENTS.md section 6, Tests lens: tests do not merely reproduce implementation assumptions.
- **Impact:**
  - The asserted bound, the reported `step_bytes_max` and the README figures all under-state each latched step by 2 B, at every shape.
  - The test hard-codes the same stale `+ 6`, so it cannot detect the error, and it rejects the correct count.
- **Required outcome:**
  - The accounting and the bound count the crc span from `NVM_REC_HDR`.
  - `service_bound` derives its expected value from the header size or the fixture, not a literal.
  - The README figures are recomputed: 280 B at 1x1 and 1,160 B at 8x8 by this arithmetic.
- **Verification:** Both probe variants become the passing tree. A planted `6u` is caught by `service_bound`.

### F3 - MINOR - Docs - the authoritative flash maps do not show `journal_klj3`

This merges my finding with the other reviewer's F4.

- **Where:**
  - `docs/diagrams/flash_layout.svg`, `.drawio` and `.png`, generated by `docs/diagrams/flash_layout.gen.py` from `FLASHBOOT_RESERVED` (`sw/litex/milan_soc.py:179`);
  - `docs/integration/QSPI_FLASHBOOT.md:58`;
  - `docs/design/SAVED_STATE_FASTCONNECT.md` section 5 (lines 533-552);
  - the writable-slot comment block above `FLASHBOOT_RESERVED` in `sw/litex/milan_soc.py`.
- **Evidence:**
  - Regenerated at the head, the SVG and drawio differ from the committed files (`receipts/flash_layout_regen.txt`, `receipts/flash_layout_head.svg`):
    - a new `journal_klj3` band at `0x0E40000 .. 0x0EDFFFF   640 KiB`, marked "WRITABLE - a reflash must NEVER erase this";
    - the free span shrinks from 10.81 to 10.19 MiB.
  - Regenerated at the base `a9d69c77`, both are byte-identical to the committed files, so this delta introduces the drift.
  - QSPI_FLASHBOOT says "The map and this picture move together or not at all". Its RESERVED paragraph names only `journal` and `user`.
  - FASTCONNECT section 5 says its table is "generated from `FLASHBOOT_LAYOUT` and `FLASHBOOT_RESERVED` ... slots are added there, never by hand". It still lists only `journal` (at `0xEE_0000`) and `user`.
- **Authority:** AGENTS.md section 6, Docs lens: changed contracts are reflected in authoritative docs. Decision 3: a 640 KiB journal directly below today's.
- **Impact:**
  - Every authoritative flash map omits a new 640 KiB writable range that a reflash must preserve.
  - A reader planning flash use, or a reflash, from them gets it wrong.
  - The diagram is a generated artifact, so this is not RESIDUE.
- **Required outcome:**
  - Regenerate the diagram from the map.
  - Name `journal_klj3` (offset, size, two slots of five blocks, written only by the split store) wherever the reserved ranges are listed.
- **Verification:** The generator's output equals the committed files. FASTCONNECT section 5 and QSPI_FLASHBOOT list every `FLASHBOOT_RESERVED` entry (`python3 sw/litex/flash_map.py`).

### F4 - MINOR - Tests - the `legacy` rule's negative paths and today's slot B address are not pinned

This is the other reviewer's F2, retained. I reproduced it.

- **Where:** `sw/firmware/ctrl_nvm/test/test_nvm_boot.cpp:142-191`. The rig plants `--legacy-b` at the store's own `NVM_LEGACY_B` (`sw/firmware/ctrl_nvm/test/nvm_rig.cpp:519-520`).
- **Evidence:** `scripts/probe_prior_findings.py` (`receipts/probe_prior_findings.log`) runs every binary's whole suite at 1x1. Its positive control (`klj2_not_recognised`) is caught, with 8 failing lines. Three probes survive with 0 failing tests:
  - `legacy_any_nonblank_header`: `legacy` set for any non-erased header in today's journal;
  - `ver_overrides_own_refusal`: `VD_VER` replaces the verdict of a refused own slot, not only a blank one;
  - `legacy_b_wrong_place`: `NVM_LEGACY_B` moved to the end of today's journal, which is the `user` slot.
- **Authority:**
  - Decision 2: refuse, boot blank, record the reason.
  - The rule as the head states it: only a KLJ2 header sets `legacy`, and only blank own slots turn the verdict into `VD_VER` (`nvm_store.h:113-119`).
  - AGENTS.md section 6, Tests lens: negative and boundary behaviour.
- **Impact:** The code at the head is correct. A regression that records a wrong reason, or reads the wrong place for the all-fabric slot B, would pass every gate.
- **Required outcome:** Tests that fail on each of the three probes. Today's slot addresses must be checked against a source independent of the store's macros, such as the `FLASHBOOT_RESERVED["journal"]` halves through the fixture.
- **Verification:** The three probes are caught, ideally as planted defects in `nvm_mutants.py`.

### F5 - MINOR - Tests - the multi-block erase is graded only on blank flash, so its addresses are unproven

This is the other reviewer's F3, retained. I reproduced it.

- **Where:** `sw/firmware/ctrl_nvm/test/test_nvm_capacity.cpp:55-70` (`capacity_round_trip`), covering `nvm_store.c:686-695, 804-808`.
- **Evidence:**
  - Probe `erase_first_block_every_time` erases the slot's first block `NVM_ERASE_BLOCKS` times instead of each block once. It survives the whole suite with 0 failing tests (`receipts/probe_prior_findings.log`).
  - The only multi-block commit lands once on blank flash and counts erases, not their addresses. The tree's `first_block_only` plant is caught only because it changes the count.
- **Authority:** This round's one change to the whole-image commit ("erases every block its container spans", page section 3). The bound shape's container spans 3 blocks.
- **Impact:** With such a defect, every later commit into a used slot fails its blank check (`VD_ERASE`) at any shape over one block, which is the 32x32 point the format is sized for. No gate would see it.
- **Required outcome:** A test whose commit at capacity lands in a slot holding stale data past its first block, with every erase address checked.
- **Verification:** `erase_first_block_every_time` is caught, and the new test is named by a planted defect.

### F6 - MINOR - Docs - the page still publishes the gateware VERSION as open after it was ruled

This was RS2 in my draft. I reclassified it after the other reviewer's F7, because a generated table cell carries it.

- **Where:**
  - `docs/design/SAVED_STATE_FORMAT_32X32.md:34` (contents: "the one question left open: the gateware VERSION");
  - `:376` ("is not moved, and is an open question");
  - `:510`, the T16 cell of the generated `tests` block, from `scripts/nvm_format_32x32_tables.py:529`: "the gateware VERSION open (section 5)";
  - `:528` ("Open: the gateware VERSION ... asks for a ruling").
- **Evidence:** Ruling issuecomment-6739542795 decided this: the CSR is not moved; the VERSION step is the format's own chain, which is done; VERSION 3 lands with the default flip.
- **Impact:** A cold reader of the authoritative page sees a taken decision as open. The owner's RESIDUE rule excludes a generated artifact, so this is not RESIDUE.
- **Required outcome:** Sections 5, 8 and 9 and the contents line state the ruling. Regenerate the page with its gate green.
- **Verification:** `check_nvm_format_32x32.py` rc 0, and no "open" wording for VERSION remains.

### RESIDUE (wording only; changes no measurement, figure, test, code, generated artifact or verdict)

- **RS1 - comment rule (the other reviewer's R2, same items).** New issue-comment IDs and round labels in source comments in this delta:
  - `sw/firmware/ctrl_nvm/nvm_layout3.h:4-5`: "(#823 decision 1, scoped to the split by #823 issue comment 6730985093)";
  - `sw/builder/test_builder.py:29254-29255`: "scoped to the split by #823 issue comment 6730985093";
  - `scripts/nvm_format_32x32.py:116-117`: "(#823 issue comment 6730985093 item 3)";
  - `scripts/nvm_format_32x32_tables.py:55`: "since #823 issue comment 6730985093";
  - `scripts/nvm_format_32x32_tables.py:61`: "(round 3)".

  Exact fix: drop the comment ID and the round label, and keep the behaviour and IDs. For example: "(#823 decision 1, the split placement's)", "(#823: A3 graded at the typical suspend latency)" and "the split placement: the one declaration and its two readers".

  The "(#665 lane F1)" in `nvm_shape.h:4`, `nvm_klj2.c:3` and `nvm_klj2.h:4` was in those header lines at the base, and is tracked by #746.
- **RS2 - stale prose citations (the other reviewer's R1, which I confirmed).**
  - `docs/design/SAVED_STATE_FORMAT_32X32.md:76` cites `sw/builder/endstation_builder.py:2714`, which is a blank line at the head. Fix: "`aem_name_count`, `sw/builder/endstation_builder.py:2715`".
  - `:267`: `sw/litex/milan_soc.py:3361` becomes `:3367`.
  - `:269`: `sw/litex/milan_soc.py:3346` becomes `:3352`.
  - These move again at the merge (F1).
- **RS3 - stale KLJ2 wording.**
  - `docs/design/SPLIT_CONTROL_MEMORY.md:86`: "its KLJ2 container plus one record header" becomes "its KLJ3 container plus one record header".
  - `:144`: "3,344 against 13,264 bytes" becomes "3,454 against 13,594 bytes".
  - `docs/design/SAVED_STATE_FORMAT_32X32.md:243`: "Each segment carries the KLJ2 header" becomes "the KLJ3 header".
  - `sw/firmware/ctrl_nvm/nvm_store.c:682`: "the blank check reads them all" becomes "the blank check reads the container's span of them".
- **RS4 - PR body (the other reviewer's R3).** "Posted as an open question on #823" becomes "Not moved, as ruled on #823 (issuecomment-6739542795): the format's own chain is the VERSION step."

### SUGGESTION

- **SG1 (Tests; the other reviewer's S1).** Locate each anchor of `scripts/nvm_format_32x32_tables.py` by a unique token rather than a whole line number, or let `--write` refresh the lines. Check the page's prose `path:line` against the same reader. Whole line numbers in shared files redden the gate on unrelated edits (F1, RS2).
- **SG2 (Robustness; the other reviewer's S2, which I also noted).** Add a compile-time assert that each `MILAN_NVM3_MAPIN_ENTRIES_k` is at most 255 and each `MAPOUT` entry at most 65,535 (`nvm_klj2.c` tables). Today a too-wide count only switches persistence off at run time, through `nvm_shape_consistent`. No shipped or bound shape is near either limit: 8 and 264 at the bound.

## Focus items, as found

1. **One declaration, nothing mirrored: met.**
   - `nvm_layout3.h:34-61` holds the capacities, and the bases are chained.
   - `nvm_shape.h` aliases them, and its `_Static_assert`s refuse a shape over any block.
   - `endstation_builder.py` `emit_nvm_split` reads them through `scripts/nvm_layout3.py` `read()`. That reader refuses none, two, a non-decimal or an off-chain base (gate 39 plants).
   - `nvm_klj3.py` reads the same declaration and `milan_soc.py`'s `journal_klj3`.
   - `NVM_MAP_PORTS 32u` is a table size asserted at or above both MAPS capacities, not a second capacity.
   - The all-fabric 128-name check still reads `KL_nvm_backend.sv`.
2. **Id layout covers every shape: met.**
   - 1,129 ids, 11 bits, carried in a 16-bit field, with reserved byte 0 checked. NAME runs from 222 to 1,128.
   - The format gate pins the declaration to the 32x32 TDM8 bound shape as the builder builds it.
   - The reference gate's ledger holds every id inside its block at all 5 shipped shapes.
   - The F1 capacity build at 907 names runs `name_block_ends`, `capacity_round_trip` and `one_past_refused`, and 908 names do not compile.
3. **KLJ3 journal and the KLJ2 refusal: met in the code. Test gaps are F4.**
   - `journal_klj3` is `0xE4_0000 + 0xA_0000`, ending at today's `0xEE_0000`.
   - The LiteSPI guard (`ls_in_journal`) admits a program or erase only inside it (plant `litespi_guard_admits_klj2`).
   - A KLJ2 magic gets `VD_VER` before anything else is read.
   - `nvm_legacy_check` reads only the two headers. A blank boot over a KLJ2 journal reports `VD_VER`, with `legacy` set. Today's journal is unchanged byte for byte after a commit.
4. **All-fabric placement unchanged: met for the image.**
   - `git diff a9d69c77 HEAD` touches nothing under `hdl/`, `protocol-processor`, `gptp-processor`, `sw/firmware/milan_baremetal`, `scripts/nvm_klj2.py`, `nvm_shape.py`, `nvm_contract.py` or `sw/firmware/nvm_hosttest`.
   - The saved-state writer gate and `check_nvm_record_space.py` are green.
   - Limit: every SoC now publishes `MILAN_FLASH_JOURNAL_KLJ3_*` and one more `reserved` row. That is metadata, not gateware, and I did not elaborate the all-fabric SoC to diff it.
5. **Whole-image commit: unchanged apart from the erase loop.**
   - The erase loop runs over `NVM_ERASE_BLOCKS`, which is 1 at every shipped shape.
   - `nvm.block` is reset at every seal, the only way into ERASE.
   - The erase addresses are correct in the code, but no test proves them (F5).
6. **Tables, reference and gates agree; every listed plant bites: met, with F2, F4 and F5.**
   - F1 suite: 474 tests over 5 shapes.
   - 122 of 122 planted defects caught, plus the NAME control.
   - Gate 39: 10 of 10. Reference gate: 6 of 6. Page gate: 9 of 9.
   - Flash-port self-test: 37 checks. Split target self-test: 73 checks.
7. **Design page says the format is the split's: met.** The drift gate is green at the head and red on the merge (F1). Stale VERSION wording is F6.
8. **Merge onto 1d6bf555: clean textually, one semantic conflict (F1).**
   - `milan_soc.py`: the split block sits after dev's rework, and the merged file parses.
   - Dev's S6b twin firmware (`tb/verilator/milan_dp/twin_fw.py`) compiles the KLJ3 store and `nvm_fmodel.c` on the merge: 36 units, rc 0. `twin_split.cpp` uses only `nvm_fmodel_window` and the slot macros.
   - `ctrl_configs.py` and `test_aecp.cpp`: the hunks do not interact.
   - `endstation_builder.py` and `test_builder.py`: gate 39 and the name gate pass on the merge.
   - `ci_events.py`: both sides only add step lists.
   - `SPLIT_CONTROL_MEMORY.md`: dev changed wording only (RS3 applies).
   - On the merge tree these all pass: the F1 suite, gate 39, the reference gate, the flash port, `test_ctrl_memory.py`, `check_nvm_record_space.py` and the split target. Only `check_nvm_format_32x32.py` fails.

## Lens results (clean lens in finding format)

```text
[R805] PASS Robustness - sw/firmware/ctrl_nvm/nvm_klj2.c (nvm_klj2_check_head, nvm_klj2_record, nvm_klj2_check), nvm_store.c:400-472 and 640-830, plat/nvm_flash_litespi.c ls_in_journal, host/nvm_fmodel.c protect/slots/read-alias - the code's behaviour on malformed and truncated input (KLJ2 magic, other majors, reserved byte, id past the space, length over the slot or the room, crc), an unreadable or foreign legacy header, KLJ2 in the store's own slot, multi-block erase failure and retry (block reset at seal, per-block address), the guard against today's journal, and repeated open-bit set/take idempotence, read against #823 decisions 2 and 6 and FASTCONNECT 6.2: correct; where the suite cannot see a regression of it, that is recorded under Tests (F4, F5)
```

Conformance, RTL, Tests and Docs are UNCLEAN (F1 to F6). Each was applied in full, and its clean parts are in the focus items.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #823 body, amendment and rulings 6730773797, 6730985093 and 6739542795, against `nvm_layout3.h`, `nvm_shape.h`, `nvm_klj2.c`, `nvm_store.c`, `nvm_flash_litespi.c`, `milan_soc.py:174-179,4664-4687`, `endstation_builder.py` `emit_nvm_split`, `SAVED_STATE_FORMAT_32X32.md`, and the merge tree `a643419a` | R805-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |
| RTL (architecture; no RTL changed) | UNCLEAN (F2) | widths and indexing in `nvm_klj2.c` (`uint16_t` id and index, `uint32_t` off, map tables of 8 and 16 bits with `nvm_shape_consistent`); `nvm_store.c` open bits (`(NVM_ID_SPACE+31)/32` words), the erase loop and phases, the step accounting; the `nvm_shape.h` asserts; no `hdl/` or processor change in the diff | R805-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |
| Robustness | CLEAN | as in the PASS line above | R805-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |
| Tests | UNCLEAN (F1, F2, F4, F5) | `test_nvm_boot.cpp`, `test_nvm_capacity.cpp`, `test_nvm_write.cpp:672-683`, `nvm_rig.cpp:517-520`, `nvm_mutants.py` (122 run), the over-capacity control, gate 39 (`test_builder.py:29253-29450`), the `check_nvm_klj3.py` and `check_nvm_format_32x32.py` plants, the `gen_flash_port.py` and split target self-tests, probes `probe_step_bytes.py` and `probe_prior_findings.py`, and the merge-tree runs | R805-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |
| Docs | UNCLEAN (F1, F2, F3, F6) | `SAVED_STATE_FORMAT_32X32.md` (whole), `SAVED_STATE_FASTCONNECT.md` sections 5 and 6, `SPLIT_CONTROL_MEMORY.md` (head and merge), `ctrl_nvm/README.md`, `nvm_split_target/README.md`, the `docs/README.md` row, `QSPI_FLASHBOOT.md`, and `flash_layout.*` regenerated at the head and at the base | R805-1 | f3e902f2a96bb27eac6ed7780c70905af34f389e |

## Gates I ran at the exact head (receipts under `receipts/gates/`)

| Gate | rc | Result |
|---|---:|---|
| `scripts/nvm_layout3.py` | 0 | 12 blocks, id space 1,129, layout 3, 10-byte header |
| `scripts/check_nvm_klj3.py` / `--self-test` | 0 / 0 | OK across 5 shapes; 6 of 6 plants caught |
| `scripts/check_nvm_format_32x32.py` / `--self-test` | 0 / 0 | 0 findings; 9 plants caught |
| `scripts/check_nvm_record_space.py` | 0 | all-fabric KLJ2 unchanged, 0 findings |
| `sw/firmware/ctrl_nvm/plat/gen_flash_port.py --self-test` | 0 | 37 checks, 0 failures |
| `tb/verilator/nvm_split_target/run.py --self-test` | 0 | 73 checks, 0 failures |
| `sw/litex/test_ctrl_memory.py` (LiteX venv) | 0 | PASS. The system Python lacks migen; that log is kept as `ctrl_memory_systempython_nomigen.log` |
| `sw/builder/test_builder.py --gates test_name_count_fits_the_nvm_name_block,test_split_record_space_bounds_the_split_output` | 0 | ALL GATES PASS (2 of 106) |
| `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32` | 0 | 474 tests, 5 shapes, RV32 arm built |
| F1 planted defects, `scripts/f1_selftest_slice.py` in 8 slices (the same functions as `--self-test`) | 0 | 122 of 122 caught, plus `name_assert_removed`; no unnamed test |
| `sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | OK across 5 shapes, every plant reddened |
| `git diff --check a9d69c77 HEAD` | 0 | clean |

A single `test_ctrl_nvm.py --require-rv32 --self-test` does not fit one bounded call. It timed out at 590 s (`ctrl_nvm_selftest_timeout590.*`), so I ran its parts separately:
- The slice driver calls the module's own `prepare`, `build`, `suite_tests`, `plant_and_grade`, `unnamed_checks` and `over_capacity_control`.
- The first slice's partial log (`f1_self_000_030_timeout_partial.log`) graded 16 defects; slice 16:30 graded the other 14.

On the merge tree `a643419a` (`receipts/merge/`), these are all rc 0: the F1 suite, gate 39, the reference gate, the flash port, `test_ctrl_memory.py`, the record space, the split target and the twin firmware compile. `check_nvm_format_32x32.py` is rc 1 (F1).

Hosted evidence at this head, which I inspected and do not own (`receipts/hosted/check_runs_f3e902f2.tsv`):
- The executed `docs-gates-0` failed on F1.
- The other failures are aggregation and fail-fast steps.
- Most Verilator and Yosys shards and `rtl-fast` were cancelled, not run.

## Prior public review findings

- **Order of work:** My verdict, ledger and findings F1, F2 and F3 (its flash-diagram and QSPI_FLASHBOOT half), RS1, RS3 and the VERSION wording (then RS2, now F6) were written before I read any other review.
- **What was there:** The only prior public review on PR #863 is the other reviewer's `[R806] NEGATIVE` (issuecomment-6741711708, at this head). It was posted while this round was running. There are no PR reviews and no review comments.
- **How each of its findings stands at this head:**

| Its finding | Resolution here |
|---|---|
| F1 MAJOR (drift gate red on the merge) | Retained. It is my F1, found independently and reproduced. |
| F2 MINOR (the `legacy` negative paths and slot B address untested) | Retained as F4. Its three probes reproduced with my own probe script, with a positive control caught. |
| F3 MINOR (multi-block erase addresses untested) | Retained as F5. Reproduced the same way. |
| F4 MINOR (FASTCONNECT section 5 and the `milan_soc.py` slot comment omit `journal_klj3`) | Retained, merged into F3. Confirmed at `SAVED_STATE_FASTCONNECT.md:533-552`. |
| F7 MINOR (VERSION still "open") | Retained as F6. My draft had it as RESIDUE; it carries a generated cell, so it is MINOR. |
| R1 RESIDUE (stale prose citations) | Retained as RS2. Confirmed at the head. |
| R2 RESIDUE (comment IDs) | Retained. It is my RS1. |
| R3 RESIDUE (PR body) | Retained as RS4. |
| S1, S2 SUGGESTION | Kept as SG1 and SG2. |

- **What that changed:** Reading that report produced F4 and F5, which my own pass had missed. My Robustness evidence line no longer claims that every path's regression is caught by a planted defect.

## Real limits

- I ran no full parent, processor, gPTP, Yosys or builder bank, no sweep, no Docker or act, no Vivado and no hardware. The 106-gate builder bank, the full sweep and the `run:` steps are the author's published receipts (`review-evidence/823-r1`), not mine.
- The dev twin simulation (Verilator) on the merge was not run, only its firmware compile. The all-fabric SoC was not elaborated to diff its generated headers or `flashboot_layout.json`.
- The merge tree is a scratch extraction of `a643419a`, with submodule content from the same gitlinks. `third_party/lwSRP` and `tsn-c-stack` are symlinks to this clone's pinned checkouts for the pin checks. Live `dev` `ac0a01e3` is not in this clone and was not examined.
- Physical calibration NOT RUN. The split target's recorded timing predates KLJ3, as the PR states.

## Pending manager duties

- After F1 to F6 are fixed:
  - re-review at the new head;
  - the current-dev merge candidate's builder and native banks;
  - hosted `docs`, `rtl-fast`, `verilator-suites` and `yosys-portability` evidence on the exact new head and its merge.
- Carry RS1 to RS4 to the residue checklist.

R805-1 FINISHED

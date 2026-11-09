[R805] NEGATIVE - exact head 30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14

# R805-4: internal cleared-context review of PR #863 (#823 round 4)

- Head `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14`, tree `f3b5048c7aa07f2cfcf0bd7de144422acc9c0fdc`, `823-nvm-format` to `dev-soft-core`. The remote branch is at this head, and remote `dev-soft-core` is still `1d6bf555`, the merge's second parent.
- Scope: the delta `f3e902f2..30ca4b21`, which is merge commit `3bcf0cdd` of `dev-soft-core` `1d6bf555` plus five commits. It is judged against the round 4 ruling (issuecomment-6742264763) and against each finding of my round 3 (R805-1). The append-only save path is round 5 and was not reviewed.
- Order of reading: AGENTS.md; the #823 body and amendments; the round 4 ruling; the TAKEN and REVIEW READY comments; the PR body; the delta and its history; the hosted checks at this head; my own runs. I read the earlier review findings (R805-1, R806-1) only after my own pass over the diff.

## Verdict

Four of the five lenses are clean. The ruling's seven items are implemented, and every round 3 finding of mine is resolved at its cause (table below). Two new **MINOR Docs** findings leave Docs unclean, so the verdict is NEGATIVE:

- **N1:** a historical measurement in `SPLIT_CONTROL_MEMORY.md` was rewritten to figures that run never produced. My own round 3 residue item RS3 asked for this edit, and I retract that part of it.
- **N2:** QSPI_FLASHBOOT still says nothing reads or writes `journal`. The PR's own FASTCONNECT section 5 and `milan_soc.py` comment now contradict it.

Both fixes are prose-only and need no code or test change.

## Findings

### N1 - MINOR - Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:144` - a one-off run at `c20ed894` is now reported with figures it could not print

- **Evidence:** `receipts/n1_split_memory_record.txt`.
  - Lines 139-144 record "The same three controls, on the firmware linked at `c20ed894`, were also run once through the SoC build". The third bullet now reads "the 1x1 image in an 8x8 build, 3,454 against 13,594 bytes".
  - At `f3e902f2` it read "3,344 against 13,264 bytes". Commit `8c66ab1e` changed it.
  - `c20ed894` (2026-10-10) is an ancestor of the base `a9d69c77`, so it predates #823, and its stage was KLJ2. Section 5 of the same page (line 173) says so: "The stage was 3,344 / 13,264 B in KLJ2 and is 3,454 / 13,594 B in the split's KLJ3".
  - So the run named there printed 3,344 against 13,264. Nothing in REVIEW READY says the control was run again.
- **Cause:** my round 3 residue item RS3 asked for exactly this replacement. That part of RS3 was wrong, and I retract it. The KLJ3 figures belong in section 5, which already states them, not in the record of an earlier run.
- **Authority:** AGENTS.md section 6, Docs lens (the evidence must be true for a cold reviewer); section 8 (generated prose is not more authoritative than executable evidence). The owner's RESIDUE rule excludes a changed measurement figure, so this is not RESIDUE.
- **Impact:** the memory plan now credits a recorded run with output it did not produce. Anyone who re-runs the `c20ed894` control gets different numbers from the ones the page gives.
- **Required outcome:** line 144 reports what that run printed, "3,344 against 13,264 bytes". The alternative is to run the control again at a named head and record that head with its printed figures.
- **Verification:** line 144 matches the `c20ed894` record, or names the head it was re-run at. `sw/litex/test_ctrl_memory.py` stays green (its register check reads the section 3 rule table, not this bullet).

### N2 - MINOR - Docs - `docs/integration/QSPI_FLASHBOOT.md:61-66` - "nothing writes or reads them today" contradicts this PR's own flash-map text

- **Evidence:** `receipts/n2_qspi_flashboot.txt`.
  - The delta rewrote this paragraph to add `journal_klj3`. It kept, and made more specific, the claim "The saved-state journal that used `journal` and `user` was deleted 2026-08-13 ..., so nothing writes or reads them today", followed by "Persistence is a genuine loss ... a blank-flash responder".
  - The same delta says otherwise in three places:
    - FASTCONNECT section 5 (lines 544 and 558): `journal` is written by "the all-fabric persistence writer only", and the split's store "reads the two headers of `journal` and never writes it".
    - The `milan_soc.py` slot comment (line 164): the store "reads journal's two headers".
    - The store's code: `nvm_legacy_check` (#823 decision 2) reads `NVM_LEGACY_A + i * slot` at `nvm_store.c:415`.
  - `milan_baremetal.c:133-137` validates and stages the journal's KLJ2 container. The author's REVIEW READY reports this as found and not changed.
- **Authority:** AGENTS.md section 6, Docs lens: changed contracts are reflected in authoritative docs. #823 decision 2 added the reader. My round 3 F3 required `journal_klj3` to be named wherever the reserved ranges are listed, and this is the paragraph where that was done.
- **Impact:** two authoritative pages edited by this PR disagree about who accesses one flash slot. A reader of the integration page is told the slot is dead, which this PR's own decision 2 makes false.
- **Required outcome:** the paragraph does not say that nothing reads or writes `journal`. It agrees with FASTCONNECT section 5: the all-fabric writer owns it, and the split store reads its two headers and never writes it. The older "blank-flash responder" text, which predates #823, may instead move to a new public Issue that the paragraph points to. It must not stay as a statement of today's behaviour next to this PR's text.
- **Verification:** read QSPI_FLASHBOOT lines 58-66 against FASTCONNECT section 5 and `nvm_store.c` `nvm_legacy_check`.

### RESIDUE (wording only; no figure, test, code, generated artifact or conformance claim)

- **RS5:** `docs/design/SAVED_STATE_FASTCONNECT.md:101`. The contents entry for section 5 says "The two reserved slots and why `journal` is raw". Section 5 now has three. Exact fix: "The three reserved slots (`journal_klj3`, `journal`, `user`) and why the journals are raw ...".
- **RS6:** `docs/design/SAVED_STATE_FASTCONNECT.md:118`. The status row "The flash map reserves the media" lists `journal` and `user` only. Exact fix: add "`journal_klj3` at `0xE4_0000`, 640 KiB (#823)," before `journal`.
- Comment-rule scan (owner rule 2026-10-15): none found. Every added line of `git diff 1d6bf555 30ca4b21`, docs excluded, has no issue-comment ID, round label, reviewer ID or lane label. "(#665 lane F1)" became "(#665, the F1 store)". "The F1 store" is the component name the ruling itself uses, so I do not count it. The remaining "round 4 ([R0] ...)" at `sw/builder/test_builder.py:16693` is not in this PR's diff; #746 tracks it.

### SUGGESTION

- **SG3 (Tests):** `scripts/check_nvm_format_32x32.py` `LINE_CITE_RE`. It refuses only a backticked `` `path.ext:N` ``. A backticked range `` `path.ext:N-M` `` or an unquoted `path.ext:N` passes. Widening the pattern to `:\d+(-\d+)?` with or without backticks closes that. Nothing on the page uses either form today (I checked).
- **SG4 (Robustness, Tests):** `sw/firmware/ctrl_nvm/nvm_shape.h:177-182`. The width asserts are graded one past the limit (256 and 65,536) and by removing each one. Nothing compiles a count at the limit (255). So a stricter defect, `> 254u`, survives, and no shipped or bound shape is near the limit to show it. An at-limit accept build for the input table would pin the boundary.
- **SG5 (Docs, manager):** FASTCONNECT section 5.1's citation table (lines 566-573) says it was "Re-derived at this head". It cites `milan_soc.py` lines 137 and 159. The section 5 citation was already at line 153 at the base `a9d69c77` and is at 154 here. The author reported this as found and not changed. It predates the lane, so a new Issue is the right home for it.

## Round 3 findings (R805-1), at this head

| ID | Status | Evidence |
|---|---|---|
| F1 MAJOR, the drift gate red on the merge | **Resolved** | See the F1 notes below the table. |
| F2 MINOR, the step bound counts the layout 2 header | **Resolved** | See the F2 notes below the table. |
| F3 MINOR, the flash maps omit `journal_klj3` | **Resolved**, with N2 and RS5/RS6 left in the same pages | See the F3 notes below the table. |
| F4 MINOR, the `legacy` negative paths and slot B address | **Resolved** | See the F4 notes below the table. |
| F5 MINOR, the multi-block erase on blank flash only | **Resolved** | See the F5 notes below the table. |
| F6 MINOR, VERSION shown as open | **Resolved** | See the F6 notes below the table. |
| RS1 comment rule | **Resolved** | Scan above. |
| RS2 stale prose citations | **Resolved** | The page now cites by token. No `path:NNN` remains in the page or in the delta's added docs lines, and the gate refuses one (plant `line-number`). |
| RS3 KLJ2 wording | **Resolved, except the `:144` item, which I retract (N1)** | Line 86 says KLJ3, as does `ctrl_memory.RULES`. The page's line 243 says "the container header, KLJ3 in the split". The `nvm_store.c` comment is corrected. |
| RS4 PR body | **Resolved** | The PR body cites the VERSION ruling issuecomment-6739542795. |
| SG1 anchors by token | **Done** | Same evidence as F1. |
| SG2 width asserts | **Done** | `nvm_shape.h:177-182`. Both refusals are required in their words (`over width: ... refused at compile time`). The controls `mapin_width_assert_removed` and `mapout_width_assert_removed` are caught. The doctored DR3b build alone compiles without the input assert, and its run-time test passes ("a build whose record walk and sizes disagree: checks: 1 failures: 0"). |

Details for the first six rows:

- **F1.**
  - `git merge-tree --write-tree f3e902f2 1d6bf555` gives `a643419a`, which is the merge commit's own tree. The merge is automatic, with no hand edits (`receipts/merge_tree.txt`).
  - `check_nvm_format_32x32.py` reports 0 findings, and `--self-test` passes (`receipts/fmt32_*.log`).
  - The self-test catches every plant: token gone, token on two lines, line-number citation, dropped citation.
  - The 300-line prepend control gives 0 findings.
  - Hosted `docs-gates-*` pass at this exact head.
- **F2.**
  - `nvm_store.c:577` counts `(NVM_REC_HDR - 2u) + r.plen`, and `nvm_store.h:63` bounds it the same way. That matches `nvm_rec_frame`'s crc span (`nvm_klj2.c:229-230`).
  - `service_bound` takes `rec_hdr` from the reference fixture.
  - Plant `step_bytes_layout2` is caught: "step bytes 278, want 280 (bound 280)".
  - The README gives 280 / 1,160.
- **F3.**
  - FASTCONNECT section 5's table and prose, QSPI_FLASHBOOT and the `milan_soc.py` slot comment all name `journal_klj3`.
  - Regenerated from `FLASHBOOT_RESERVED`, the SVG and drawio are byte-identical to the committed files. The committed PNG re-renders byte-identical from the committed SVG at 1,800 px on this host.
  - `flash_map.py` lists 5 slots with 0 problems (`receipts/regen_and_small_gates.log`).
- **F4.**
  - Three new tests: `legacy_other_format_not_recorded`, `own_refusal_kept_over_legacy` and `klj2_journal_at_its_flash_map_address`.
  - The last reads today's slots from `FLASHBOOT_RESERVED["journal"]` through the fixture, not from the store's macros.
  - My three round 3 probes are now plants, and each is caught by its test: `legacy_any_nonblank_header`, `ver_overrides_own_refusal` and `legacy_b_wrong_place` ("KLJ2 at 0xef0000, today's slot 1").
- **F5.**
  - `capacity_commit_over_stale` commits into A, B, then A at capacity.
  - It checks `erases == 3 x NVM_ERASE_BLOCKS` and every erase address against `journal_klj3` and `FLASH_ERASE_BLOCK` read from the SoC source, then compares the third container with the reference byte for byte.
  - Plant `erase_first_block_every_time` is caught.
- **F6.**
  - The contents line, section 5 (line 376), section 9 (line 532) and the generated T16 cell (line 513, from `nvm_format_32x32_tables.py:554`) say "not moved, as ruled (#823)".
  - The drift gate is green, so the generated cell equals the generator's output.

The other review's round 3 findings (R806-1: F1, F2, F3, F4, F7, R1, R2, R3, S1, S2) are the same defects as my F1, F4, F5, F3, F6, RS2, RS1, RS4, SG1 and SG2. Each is resolved with the evidence above. R806-1 R1's `:243` and its comment-ID items are fixed.

## Ruling items (issuecomment-6742264763)

1. **The sync.**
   - Merge commit `3bcf0cdd`, no rebase. Its tree equals a fresh automatic merge.
   - The seven files both sides changed (`receipts/both_sides_files.txt`) are the ones the PR body lists. I judged each one:
     - `ci_events.py`: both sides only add step lists.
     - `ctrl_configs.py`: both sides only add classification rows.
     - `test_aecp.cpp`: dev's ENTITY `available_index` test and this branch's two KLJ3 macro renames are disjoint hunks.
     - `SPLIT_CONTROL_MEMORY.md`: wording on dev's side; see N1 for this branch's side.
     - `endstation_builder.py`: `emit_nvm_split` is written for every build, so S6a's `control.placement: split` argv (`--ctrl-mailbox --ctrl-firmware`) reaches `milan_soc.py:4866-4881`, and that block reads `nvm_split.json` from the same output.
     - `test_builder.py`: gate 39 and gate 23m are separate gates.
     - `milan_soc.py`: the split constants block sits under `if args.ctrl_mailbox:` after S6a's rework. Its only conflict was the page's line anchors, now found by token.
   - The S6b twin compiles this store (`twin_fw.py` adds `nvm_klj2.c`, `nvm_store.c` and `host/nvm_fmodel.c`). I re-ran it: `make twin` rc 0, "twin: 0 finding(s)". `make twin-plants` rc 0, all 20 distinct plants REFUSED (`receipts/twin*.log`, `receipts/twin_report.json`).
2. **The step bound:** met (F2 above).
3. **The flash maps:** met (F3 above). The surrounding residue is N2, RS5 and RS6.
4. **The legacy and erase tests:** met (F4, F5 above).
5. **The VERSION wording:** met through the generator (F6 above).
6. **RS1 to RS4:** met, except the line 144 edit (N1). The KLJ3 rule text in `ctrl_memory.py:98`, which the first run failed on, now matches the section 3 table. I could not run `sw/litex/test_ctrl_memory.py` here (no `migen` on this host). It ran in hosted `elaborate`, which passes at this exact head.
7. **The width asserts:** met (SG2 row above), with controls.

## Lens results

```text
[R805] PASS Conformance - issuecomment-6742264763 items 1-7 against merge 3bcf0cdd (tree a643419a = fresh merge-tree), scripts/check_nvm_format_32x32.py + nvm_format_32x32_tables.py (token anchors, LINE_CITE_RE, CITED), sw/firmware/ctrl_nvm/nvm_store.c:577, nvm_store.h:63, nvm_shape.h:171-182, test_nvm_boot.cpp:169-211, test_nvm_capacity.cpp:73-94, SAVED_STATE_FORMAT_32X32.md:34,376,513,532, milan_soc.py:162-165,4866-4881 - every ruling item is implemented as ruled; #823 decision 2 (KLJ2 refused, boot blank, reason recorded) and decision 3 (640 KiB directly below today's journal) hold in code and tests; the all-fabric placement is untouched (git diff 1d6bf555 30ca4b21 -- hdl protocol-processor gptp-processor sw/firmware/milan_baremetal scripts/nvm_klj2.py scripts/nvm_shape.py scripts/nvm_contract.py sw/firmware/nvm_hosttest is empty). The documentation defects are filed under Docs.
[R805] PASS RTL - sw/firmware/ctrl_nvm/nvm_klj2.c:217-233 (crc span NVM_REC_HDR-2 then payload), nvm_store.c:577 and nvm_store.h:63 (the step accounting and its bound), nvm_shape.h:95-98,177-182 (NVM_SUM32 over all 32 table entries, 255 and 65,535 against the uint8_t and uint16_t tables), nvm_fmodel.c:279-282 (erase_addr recorded only inside the 16-entry array), nvm_rig.cpp load_at bounds (addr < NVM_FMODEL_BYTES, length clipped to the room); no HDL or processor gitlink in 1d6bf555..30ca4b21 - widths, truncation and indexing are correct. The merge's S6a CTRL_SPLIT_P and S6b twin RTL compile and run with this store (twin rc 0).
[R805] PASS Robustness - nvm_store.c:408-472 (nvm_legacy_check: only a KLJ2 magic sets legacy, and VD_VER replaces only a blank verdict), the whole-image commit over a non-blank slot (capacity_commit_over_stale: three commits A/B/A at capacity, each erase at its block, the third container byte-exact), the too-wide map refused at compile time with the run-time DR3b fallback still reached by the doctored build (mapin binary: 1 check, 0 failures), the NVM_DOCTORED_MAPIN escape used only by nvm_bench.py:84 (git grep) - malformed, foreign-format and stale-flash behaviour is correct and is now pinned.
[R805] PASS Tests - receipts/ctrl_nvm_selftest.log: test_ctrl_nvm.py --require-rv32 --self-test rc 0, "OK across 5 shape(s), 506 tests, and all 130 planted defects reddened", the round 4 plants each caught by its named test (step_bytes_layout2 by service_bound; legacy_any_nonblank_header, ver_overrides_own_refusal and legacy_b_wrong_place by their three tests; erase_first_block_every_time by capacity_commit_over_stale; mapin and mapout _width_assert_removed by over_width); receipts/fmt32_selftest.log PASS with 12 plants caught and the moved-lines control at 0; receipts/twin.log and twin-plants.log rc 0 with 20 of 20 plants refused; receipts/regen_and_small_gates.log (check_nvm_klj3 6 of 6, nvm_layout3, flash_map 0 problems, diagram byte-identical); hosted, all 69 check runs at head 30ca4b21: 68 success, 1 skipped (physical gPTP, nightly/manual) - each new test fails on the defect it claims to catch, and the expected values come from the reference or the flash map, not from the store's own macros. SG3 and SG4 are optional.
[R805] UNCLEAN Docs - N1 (SPLIT_CONTROL_MEMORY.md:144) and N2 (QSPI_FLASHBOOT.md:61-66) open; RS5 and RS6 are residue. Checked clean: SAVED_STATE_FORMAT_32X32.md (drift gate 0 findings, no path:line citation, VERSION wording), SAVED_STATE_FASTCONNECT.md section 5 table and prose (lines 543-558), milan_soc.py slot comment (lines 162-165), docs/diagrams/flash_layout.{svg,drawio,png} (regenerated and re-rendered byte-identical), sw/firmware/ctrl_nvm/README.md (280 / 1,160 B, 60 checks in 98 tests, 127 defects and three controls), the test_ctrl_nvm.py docstring, and the PR body's seven-file table and validation list.
```

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling items 1-7; merge `3bcf0cdd` vs merge-tree; `nvm_store.c`/`.h`, `nvm_shape.h`, the new tests; format page gate; `milan_soc.py` map and split block | R805-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |
| RTL | CLEAN | `nvm_klj2.c` framing, step accounting and bound, width asserts, `nvm_fmodel` erase log, rig `load_at`; no HDL in the delta; twin RTL run | R805-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |
| Robustness | CLEAN | `nvm_legacy_check` paths, commit over stale flash, DR3b doctored build, the doctored-macro scope | R805-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |
| Tests | CLEAN | F1 campaign self-test (506 tests, 130/130), page gate self-test, twin and 20 plants, reference gate, hosted 68/69 pass and 1 skipped | R805-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |
| Docs | UNCLEAN (N1, N2) | format page, FASTCONNECT 5, QSPI_FLASHBOOT, SPLIT_CONTROL_MEMORY, the flash diagram, the store README, the PR body | R805-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |

To clear: fix N1 and N2, which are prose-only, then re-cover Docs at the new head. A commit that touches only those two documents changes nothing in the scope of the other four lenses, so their coverage at this head carries forward.

## What I ran (receipts under `receipts/`; portable script `scripts/run_r805_4.sh`)

- **Merge check:** `git merge-tree --write-tree f3e902f2 1d6bf555` gives `a643419a` (rc 0, no conflicts), which equals the tree of `3bcf0cdd`. The seven both-sides files are in `both_sides_files.txt`.
- **Format page gate:** `check_nvm_format_32x32.py` rc 0 (0 findings). `--self-test` rc 0, PASS.
- **Store campaign:** `test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` rc 0. It printed "OK across 5 shape(s), 506 tests, and all 130 planted defects reddened". At each shape the suite ran 98 checks with 0 failures, and the RV32 arm ran.
- **Two-placement simulation:** `make -C tb/verilator/milan_dp twin` rc 0, "twin: 0 finding(s)". `twin-plants` rc 0, with 20 of 20 plants refused. Both ran with Verilator 5.050 (`--version`: "Verilator 5.050 2026-07-01 rev v5.050").
- **Diagram and small gates:**
  - `flash_layout.gen.py`: SVG and drawio identical to the committed files; PNG re-render identical.
  - `flash_map.py` rc 0; `nvm_layout3.py` rc 0; `check_nvm_klj3.py --self-test` rc 0 (6 of 6).
- **Hosted checks:** `gh pr checks 863` and the check runs for the exact head: 69 runs, all at `30ca4b21`. 68 succeeded, including `rtl-fast`, `split-cdc`, `verilator-suites`, `yosys-portability`, `elaborate`, the docs gates and `full-ci-gate`. One was skipped: physical gPTP (nightly/manual). The PR is not a draft.
- **Head checks:** `git diff --check 1d6bf555 30ca4b21` rc 0. Every commit in the delta has a one-line message.
- **Clone restored:** HEAD, tree and index are `f3b5048c`. There are no tracked changes or untracked files, the ignored build outputs were removed, and the submodule gitlinks match HEAD (`restore_check.txt`).
- **Published logs:** in `twin.log` and `twin-plants.log` the host home directory is replaced by `<home>`. `receipts/RAW.tsv` holds the sha256 of each log before that replacement. Every published file is listed in `MANIFEST.sha256`.
- **Process note:** my first attempt at the store campaign overlapped with a second launch. I stopped it, and it left no receipt. The receipt is from one clean run.

## Real limits

- `sw/litex/test_ctrl_memory.py` and the other LiteX simulations could not run on this host (no `migen`), so for them I rely on hosted `elaborate` at this exact head (pass).
- I did not run the full sweep, the builder bank, the gPTP/protocol-processor/Yosys banks, Vivado or the area runs. That was ruled out for this round, and the hosted shards at this head cover them as hosted evidence only.
- The published evidence tree `1f9fe825` (`review-evidence/823-r1`) holds the round 3 receipts at `f3e902f2`. The author's round 4 receipts directory is described in REVIEW READY, but I did not find it in that tree. Where I cite the author's round 4 figures, I reproduced them myself (campaign, page gate, twin) or rely on the hosted runs.
- Physical calibration was not run, and skipped field contexts are not hardware proof.

## Pending manager duties

- Carry N1 and N2 to the author, and RS5 and RS6 to the residue checklist.
- Open an Issue for SG5 (FASTCONNECT 5.1's stale citation table) and for QSPI_FLASHBOOT's pre-#823 "blank-flash responder" text, unless N2's fix absorbs it.
- Build and validate the current-dev merge candidate at the merge turn (source base `a9d69c77`; live `dev` `123f57a922bf07476cd69f91867f3b6f07080804`; PR base `dev-soft-core` at `1d6bf555`), and link its receipts. No manager source bank has run at this head, and I claim none.
- Accept hosted and act results. A Docs re-cover is needed at the fixing head.

R805-4 FINISHED

[R806] NEGATIVE - exact head 30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14

# R806-4: external independent review of #823 round 4 / PR #863

- **Head:** `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14`, tree `f3b5048c7aa07f2cfcf0bd7de144422acc9c0fdc`. Source base `a9d69c77`.
- **Delta judged:** `f3e902f2..30ca4b21`. That is the sync merge `3bcf0cdd` of `dev-soft-core` `1d6bf555`, then five commits: `57bb34fc`, `f3e64bbc`, `d24f386d`, `8c66ab1e` and `30ca4b21`.
- **Authorities:**
  - AGENTS.md;
  - the round 4 ruling (issuecomment-6742264763) and the VERSION ruling (issuecomment-6739542795);
  - the round 4 TAKEN and REVIEW READY (issuecomment-6742338270, issuecomment-6748055403);
  - the PR body at head;
  - my own R806-1 findings (PR #863 issuecomment-6741711708);
  - the author's round 4 receipts on `823-review-evidence` at `c4844245`, `review-evidence/823-r1/author-r4/`.
- The other reviewer's R805-1 report was read only after this verdict and the ledger were written. Its findings are resolved in the last section.
- Live `dev-soft-core` is still `1d6bf555` (fetched at review time), so the merged base is current.

## Verdict

NEGATIVE. Two MINOR findings are open, both under Docs. Three RESIDUE items and three SUGGESTIONs are recorded.

Every ruling item and every one of my R806-1 findings is met at its cause:
- the sync merge;
- token anchors;
- the step bound;
- the flash maps;
- the legacy and erase tests;
- VERSION;
- RS1 to RS4;
- the width asserts.

What remains is two authoritative documents that this delta left false:
- **N1:** a one-time run's measured figures were rewritten to figures that run could not have produced.
- **N2:** the flash-boot page still says nothing reads or writes `journal`. FASTCONNECT section 5 and the `milan_soc.py` comment, as this PR edits them, say the split store reads it.

## Findings

### N1 — MINOR — Docs — `docs/design/SPLIT_CONTROL_MEMORY.md:140,144` — a historical run's receipt now carries figures that run could not produce

- **Authority:** AGENTS section 6, Docs lens: changed contracts are reflected truthfully, and the PR carries enough evidence for a cold reviewer. Owner rule: a defect that changes a measurement or figure is not RESIDUE.
- **Evidence:**
  - Line 140 reads: "The same three controls, on the firmware linked at `c20ed894`, were also run once through the SoC build".
  - Commit `8c66ab1e` changed line 144, that run's third result, from "3,344 against 13,264 bytes" to "3,454 against 13,594 bytes".
  - `c20ed894` is an ancestor of the source base `a9d69c77`. It predates KLJ3: the base's own copy of this list reads 3,344 / 13,264.
  - Line 173 of the same page states the change correctly: "The stage was 3,344 / 13,264 B in KLJ2 and is 3,454 / 13,594 B in the split's KLJ3".
  - Line 144 now attributes the KLJ3 sizes to a KLJ2-era run that was not repeated.
- **Impact:** a reader of the evidence trail believes the SoC-build control was run with the KLJ3 stage, which it was not.
- **Provenance:** this is a ruled fix that went too far, not a lapse by the author. The other reviewer's R805-1 RS3, which I read after this verdict, prescribed exactly this change ("`:144`: '3,344 against 13,264 bytes' becomes '3,454 against 13,594 bytes'"). The round 4 ruling adopted RS3 as item 6. Line 86 of that same RS3 (the rule text) was right to change, because it states the current rule. Line 144 records a past run. I publish the conflict for the manager's decision rather than choosing privately. My classification is MINOR, because the owner's RESIDUE rule excludes a change to a measurement or figure.
- **Required outcome:** one of these two.
  - Restore "3,344 against 13,264 bytes" as the `c20ed894` run's result. Optionally add that the stage is now 3,454 / 13,594 B (line 173).
  - Or re-run the control and cite the head it ran at.
- **Verification:** `git show a9d69c77:docs/design/SPLIT_CONTROL_MEMORY.md` agrees with the `c20ed894` sentence. Any new figure names the head it was measured at.

### N2 — MINOR — Docs — `docs/integration/QSPI_FLASHBOOT.md:58-66` — the reserved-range paragraph this delta edited says nothing reads or writes `journal`

- **Authority:**
  - Decision 2 as built: the split store reads today's journal's two headers (`legacy`, `nvm_legacy_check` in `sw/firmware/ctrl_nvm/nvm_store.c`).
  - FASTCONNECT section 5, edited in this delta (`docs/design/SAVED_STATE_FASTCONNECT.md:542,558`): `journal` is "the all-fabric placement's KLJ2", written by "the all-fabric persistence writer only", and the split store "reads the two headers of `journal`".
  - The `milan_soc.py` slot comment added in `d24f386d` says the same.
- **Evidence:**
  - `d24f386d` rewrote this paragraph to add `journal_klj3`. It kept "The saved-state journal that used `journal` and `user` was deleted 2026-08-13 … so nothing writes or reads them today. Persistence is a genuine loss … nothing survives a power cycle."
  - Two authoritative pages now disagree about who touches `journal`. The paragraph's new `journal_klj3` sentence sits next to a claim that persistence is lost.
  - The REVIEW READY discloses the write half (the all-fabric KLJ2 writer in `milan_baremetal.c`) as found and predating the lane. The read half is this PR's own behaviour.
- **Impact:** deployment or board work that trusts the flash-boot page treats `journal` as dead. It may also conclude that the split placement does not persist.
- **Required outcome:** the paragraph states who reads and writes `journal` today, consistent with FASTCONNECT section 5:
  - the split store reads its two headers and never writes it;
  - the all-fabric firmware's KLJ2 writer writes it.

  The "genuine loss" sentences are scoped to what is still true, or removed.
- **Verification:** read the QSPI_FLASHBOOT paragraph against FASTCONNECT section 5's table and prose and against `nvm_legacy_check`.

### RS-a — RESIDUE — Docs — lane label in source comments this delta rewrote

- **Where:** `sw/firmware/ctrl_nvm/nvm_klj2.c:3`, `sw/firmware/ctrl_nvm/nvm_klj2.h:4` and `sw/firmware/ctrl_nvm/nvm_shape.h:4`.
- This delta rewrote "(#665 lane F1)" as "(#665, the F1 store)". F1 is #665's lane label. The owner comment rule bars lane names in source comments, and these three lines are new text in this delta.
- The round 3 delta's new files also use "the F1 store" in comments (`receipts/residue_f1_label_scan.txt`). That use is pre-existing at this round, and `dev-soft-core`'s `sw/litex/ctrl_memory.py` already uses the phrase.
- **Exact fix:** "(#665, the split placement's saved-state store)". The same wording serves the other instances.

### RS-b — RESIDUE — Tests (wording) — `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:15,67,75,83,98,667` — the split store's reference named as `nvm_klj2.py`

- The fixture assembles the split store's containers with `scripts/nvm_klj3.py` (`nvm_fixture.py:44`).
- These comments and assertion messages still say "byte for byte as nvm_klj2.py writes it" / "differs from nvm_klj2.py's". One fires in this round's self-test log (`frame_crc_init`: "the committed container differs from nvm_klj2.py's").
- Pre-existing since round 3, missed by my R806-1. Assertions and behaviour are unaffected.
- **Exact fix:** say `nvm_klj3.py` in those six places.
- **Leave unchanged:**
  - `nvm_rig.cpp:179`: the payload rule really is `nvm_klj2.payload_bytes`;
  - `test_nvm_boot.cpp:12`: the all-fabric container really is `nvm_klj2.py`'s.

### RS-c — RESIDUE — Docs — `docs/design/SAVED_STATE_FASTCONNECT.md` section 5.1 citation table

- The author's REVIEW READY says it gives `milan_soc.py` line numbers from an older head, predating this lane.
- Not part of this delta. Carry it to the residue checklist (or #746) so it is not lost.

### S-a — SUGGESTION — Tests — `scripts/check_nvm_format_32x32.py:51` (`LINE_CITE_RE`)

- The gate states "no line by its number" (docstring item 5). It refuses only the single form `` `path.ext:123` ``.
- `receipts/linecite_probe.txt` (`scripts/linecite_probe.py`): these forms are all accepted:
  - a range, `` `sw/litex/milan_soc.py:179-181` ``;
  - a list, `` `nvm_store.c:408,465` `` (the form round 3's prose used);
  - an unquoted `path:179`;
  - "`path` line 179";
  - a `#L179` link.
- The page carries none of these today, so nothing is false now.
- Widening the pattern (`:\d+([-,]\d+)*`, backticks optional, plus `#L\d+`) makes the gate as strong as its docstring. Add a plant for the range form.

### S-b — SUGGESTION — Tests — `sw/firmware/ctrl_nvm/nvm_shape.h:177-182`, `test_ctrl_nvm.py` `WIDTHS`

- The width refusals are graded one past the table (256, 65,536) and by removal. The accepted boundary (255 input entries) is not compiled.
- So an off-by-one (`>= 255u`) would survive. No shipped or bound shape is near it: the bound shape has 8 entries per input port.
- Compiling the codec at 255 input entries and requiring success would pin the boundary.

### S-c — SUGGESTION — Robustness — `sw/firmware/ctrl_nvm/nvm_shape.h:179` (`#ifndef NVM_DOCTORED_MAPIN`)

- Any build that defines `NVM_DOCTORED_MAPIN` silently drops the input-width refusal.
- Only the host bench defines it today (`sw/firmware/ctrl_nvm/test/nvm_bench.py:84`).
- An `#error` when it is defined outside the host test build would keep the seam test-only.

## Ruling items and R806-1 findings, at their cause

| Item | Result | Evidence |
|---|---|---|
| (1) sync merge | Met. `3bcf0cdd`'s tree `a643419a` equals `git merge-tree --write-tree f3e902f2 1d6bf555`: a clean textual merge with nothing added by hand. It is also the tree my R806-1 merge probe examined. | `receipts/merge_tree_check.txt` |
| (1) seven both-sides files | Met. All seven are disjoint hunks (`receipts/both_sides_files.txt`). `ci_events.py`: their `split-cdc` job, our four commands in the NVM step. `ctrl_configs.py`: separate dict rows. `test_aecp.cpp`: their `available_index` test; our two `NVM_KLJ_HDR` lines and one `MILAN_NVM3_N_NAME` line. `endstation_builder.py`: their `control.placement` and split argv; our `emit_nvm_split`, written for every build (`:6077`), so an S6a split build finds `nvm_split.json`. `test_builder.py`: gate 23m vs gate 39. `SPLIT_CONTROL_MEMORY.md`: wording vs KLJ3 rows. `milan_soc.py`: S6a's `i_ctl_nvm_verdict` is 4 bits (`:2924`), and this PR adds no verdict code. `git diff 1d6bf555 HEAD -- hdl/` is empty. | diffs read on each side |
| (1) S6b twin compiles this store | Met. `twin_fw.py:55` compiles `nvm_klj2.c`, `nvm_store.c` and `nvm_fmodel.c`. `make -C tb/verilator/milan_dp -j4 twin` with Verilator 5.050: rc 0, `twin: 0 finding(s)`. `twin-plants`: rc 0, 20 of 20 plants REFUSED. | `receipts/twin.log`, `twin.rc`, `twin_plants.log`, `twin_plants.rc` |
| (1) drift gate by token | Met. Each `Anchor` is a file plus a token, and `anchor_findings` requires exactly one line (`scripts/nvm_format_32x32_tables.py:172-187`). Every prose citation on the page is a graded token (7 of 7, each on 1 line). The page has no `path:NNN` of any form. Gate rc 0, 0 findings. Self-test PASS: token gone, token on two lines, line-number citation, dropped citation, and the 300-line prepend control at 0 findings. | `receipts/check_nvm_format_32x32*.log`, `receipts/cited_scan.txt`; see S-a |
| (2) step bound | Met. `nvm_latch` counts `(NVM_REC_HDR - 2u) + plen`, exactly the bytes `nvm_rec_frame` runs the crc16 over (`nvm_klj2.c:229-230`). `NVM_STEP_BOUND` matches, and `service_bound` takes `rec_hdr` from the reference fixture. Plant `step_bytes_layout2` is caught: "step bytes 278, want 280". | `receipts/new_plants_caught.txt` |
| (3) flash maps | Met. FASTCONNECT section 5 table and prose, the `milan_soc.py` slot comment, and QSPI_FLASHBOOT's first sentence all show `journal_klj3`. `flash_layout.gen.py` regenerates `.drawio` and `.svg` byte-identical to head. The PNG shows the slot. `flash_map.py`: 5 slots, 0 problems. | regenerated under scratch; see N2 |
| (4) legacy negative paths and slot B | Met. `legacy_other_format_not_recorded`, `own_refusal_kept_over_legacy` and `klj2_journal_at_its_flash_map_address` (addresses from `FLASHBOOT_RESERVED` through `nvm_bench`/fixture, loaded with `--load-at`). Plants caught: `legacy_any_nonblank_header`, `ver_overrides_own_refusal`, `legacy_b_wrong_place`. These are my R806-1 probes p07, p08 and p12. | `receipts/new_plants_caught.txt` |
| (4) multi-block erase over stale flash | Met. `capacity_commit_over_stale` commits A, B, A at capacity and checks every erase address (`erase_addr`, `nvm_fmodel.c:280-281`, 9 of a 16-entry log) against the flash map. Plant `erase_first_block_every_time` (my p05) is caught. | same |
| (5) VERSION | Met. Page lines 376 and 532 and the generated T16 cell (`scripts/nvm_format_32x32_tables.py:554`) say "not moved, as ruled (#823)". No "open question" remains. | page read |
| (6) RS1-RS4 | Met. No issue-comment ID or round label is added in source vs `1d6bf555` (`receipts/residue_scan_pr_vs_dsc.txt`); the lane label is RS-a. `ctrl_memory.RULES` says KLJ3, matching the plan's table. The page says "the container header, KLJ3 in the split". The PR body cites the VERSION ruling. | |
| (7) width asserts | Met. `nvm_shape.h:177-182`. `over_width` requires both refusals in their words at 1x1. Controls `mapin_width_assert_removed` and `mapout_width_assert_removed` are caught. `NVM_DOCTORED_MAPIN` is only on the DR3b bench build (`nvm_bench.py:84`), whose run-time test still passes. | `receipts/test_ctrl_nvm_selftest.log`; see S-b, S-c |

All of my R806-1 findings are resolved:
- **F1 (MAJOR):** resolved by item (1).
- **F2, F3 (MINOR):** resolved by item (4).
- **F4 (MINOR):** resolved by item (3). The flash-boot page's remaining sentence is the new N2.
- **F7 (MINOR):** resolved by item (5).
- **R1, R2, R3 (RESIDUE):** resolved. There are no line citations, the page says "the container header, KLJ3 in the split", no comment IDs remain, and the PR body cites the ruling.
- **S1, S2 (SUGGESTION):** adopted.

## Lens results (clean results carry their artifact)

```text
[R806] PASS Conformance — merge 3bcf0cdd (tree a643419a = git merge-tree f3e902f2 1d6bf555); nvm_store.c nvm_latch, nvm_legacy_check, nvm_erase_start; nvm_klj2.c:229-230; nvm_shape.h:177-182; FASTCONNECT section 5; format page lines 376/532 and the T16 cell — every ruling item 1-7 of issuecomment-6742264763 checked against the code, with the plants and runs above. Decisions 2 and 3 (KLJ2 refused with legacy recorded; journal_klj3 directly below journal) hold at head. The gateware VERSION is untouched (git diff 1d6bf555 HEAD -- hdl/ is empty).
[R806] PASS RTL — git diff 1d6bf555..30ca4b21 -- hdl/ (empty: this PR adds no RTL); milan_soc.py:2924 — the S6a placement switch's i_ctl_nvm_verdict (4 bits) carries the unchanged verdict enum. C widths: step_bytes adds NVM_REC_HDR-2 (unsigned, no wrap); the width asserts compare all 32 per-port macros against 255/65535 through NVM_SUM32; erase_addr is bounded to 16 entries (nvm_fmodel.c:280), with at most 15 erases per test.
[R806] PASS Robustness — test_nvm_boot.cpp legacy_other_format_not_recorded / own_refusal_kept_over_legacy / klj2_journal_at_its_flash_map_address; test_nvm_capacity.cpp capacity_commit_over_stale; nvm_shape.h width refusals — each path is refused or reported as ruled: a foreign header in today's journal, a refused own slot beside KLJ2, a misplaced slot-B read, an erase over non-blank multi-block slots, and over-wide map counts. A plant per path is caught (receipts/new_plants_caught.txt). S-c is optional.
[R806] PASS Tests — receipts/test_ctrl_nvm_selftest.log: test_ctrl_nvm.py --require-rv32 --self-test --jobs 8 at head, rc 0, "OK across 5 shape(s), 506 tests, and all 130 planted defects reddened". receipts/check_nvm_format_32x32_selftest.log PASS, with the 300-line control at 0. receipts/twin*.log rc 0, 0 findings, 20/20 plants. Hosted CI at this exact head: the docs, rtl-fast, elaborate and rtl-full pull_request runs all succeeded; 68 checks pass, 1 skipped (Physical gPTP, nightly/manual) (receipts/hosted_pr_checks.txt, hosted_runs.txt). S-a and S-b are optional; RS-b is wording.
[R806] UNCLEAN Docs — N1 (SPLIT_CONTROL_MEMORY.md:144) and N2 (QSPI_FLASHBOOT.md:58-66) open. Checked clean: SAVED_STATE_FORMAT_32X32.md at the delta (token citations, VERSION, KLJ3 wording); FASTCONNECT section 5; the milan_soc.py slot comment; flash_layout.drawio/svg byte-identical regeneration and the PNG; the counts in sw/firmware/ctrl_nvm/README.md (60 checks, 98 tests per shape, 38 on both ports, 280/1,160 B, 127 defects + 3 controls = the self-test's 130); the test_nvm_shapes.cpp header; the PR body's seven-file table.
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling items 1-7 against the merge tree, `nvm_store.c`, `nvm_klj2.c`, `nvm_shape.h`, the format page, FASTCONNECT section 5 and the PR body; decisions 2 and 3 | R806-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |
| RTL | CLEAN | No RTL in this PR vs `1d6bf555`; the S6a switch's NVM verdict width vs the unchanged enum; the C widths of the step bound, width asserts and erase log | R806-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |
| Robustness | CLEAN | The legacy rule's negative paths, the misplaced-slot read, erase over stale multi-block flash, the over-wide map refusals, each with a caught plant | R806-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |
| Tests | CLEAN | `test_ctrl_nvm.py --require-rv32 --self-test` (506 tests, 130/130); drift gate and self-test; twin and twin-plants; hosted runs at head | R806-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |
| Docs | UNCLEAN (N1, N2) | The format page, FASTCONNECT section 5, QSPI_FLASHBOOT, SPLIT_CONTROL_MEMORY, the store README, the flash diagram, the PR body | R806-4 | `30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14` |

## Commands I ran (exact head)

| Command | Result | Receipt |
|---|---|---|
| `git merge-tree --write-tree f3e902f2 1d6bf555` vs `3bcf0cdd^{tree}` | both `a643419a…` | `receipts/merge_tree_check.txt` |
| `python3 -I scripts/check_nvm_format_32x32.py` / `--self-test` | rc 0, 0 findings / PASS | `receipts/check_nvm_format_32x32*.log` |
| `python3 -I scripts/cited_scan.py <clone>` (reviewer) | 7 prose citations, all graded, each 1 line | `receipts/cited_scan.txt` |
| `python3 -I scripts/linecite_probe.py <clone>` (reviewer) | single form refused; 5 other forms accepted | `receipts/linecite_probe.txt` |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | rc 0; 506 tests; 130/130 | `receipts/test_ctrl_nvm_selftest.log`, `.rc` |
| `make -C tb/verilator/milan_dp -j4 VERILATOR=<pinned 5.050> twin`, then `twin-plants` | rc 0, 0 findings; rc 0, 20/20 REFUSED | `receipts/twin.log`, `twin_plants.log`, `.rc` (host paths redacted; raw digests in `receipts/RAW_DIGESTS.txt`) |
| `python3 -I docs/diagrams/flash_layout.gen.py <scratch>`, then `cmp` | `.drawio` and `.svg` identical | (scratch only) |
| `gh pr checks 863`; runs by head SHA | 68 pass, 1 skipping; 4 runs success | `receipts/hosted_pr_checks.txt`, `hosted_runs.txt` |
| Author receipts at `c4844245`: four files' digests vs `MANIFEST.json` | 4/4 MATCH | `receipts/author_r4_manifest_spotcheck.txt` |
| Restore check | worktree, index and modes equal HEAD; 6 gitlinks as recorded; 0 untracked or ignored | `receipts/restore_check.txt` |

Verilator identity: the pinned wrapper reports `Verilator 5.050 2026-07-01 rev v5.050`.

## Prior public findings by the other reviewer (R805-1)

Read after the verdict and ledger above were written (PR #863 issuecomment-6742254074, at `f3e902f2`). Each finding is judged at this head:

| R805-1 item | At `30ca4b21` | Evidence |
|---|---|---|
| F1 MAJOR, drift gate red on the merge | RESOLVED | Ruling item (1) above; gate rc 0 at the merged head, with the token anchors and the 300-line control |
| F2 MINOR, step bound counts the layout 2 header | RESOLVED | Count and bound both use `NVM_REC_HDR - 2u`; README 280 / 1,160 B; plant `step_bytes_layout2` caught ("step bytes 278, want 280") |
| F3 MINOR, flash maps omit `journal_klj3` | RESOLVED | Diagram regenerates byte-identical; FASTCONNECT section 5, QSPI_FLASHBOOT's reserved list and the `milan_soc.py` comment name it. The paragraph's remaining stale sentence is my new N2 |
| F4 MINOR, `legacy` negative paths and slot B | RESOLVED | Three tests, three plants caught |
| F5 MINOR, multi-block erase on blank flash only | RESOLVED | `capacity_commit_over_stale`, plant `erase_first_block_every_time` caught |
| F6 MINOR, VERSION published as open | RESOLVED | Page and generated T16 cell: "not moved, as ruled (#823)" |
| RS1, comment rule | RESOLVED | No comment ID or round label remains in `nvm_layout3.h`, `test_builder.py`, `nvm_format_32x32.py` or `nvm_format_32x32_tables.py`. The `F1` lane label on the three rewritten header lines is my RS-a |
| RS2, stale prose citations | RESOLVED | The page cites by token only (`receipts/cited_scan.txt`) |
| RS3, KLJ2 wording | RESOLVED except one item, which is RETAINED AS N1 | `SPLIT_CONTROL_MEMORY.md:86`, page `:243` and `nvm_store.c` erase comment are all correct. The prescribed `:144` change rewrote a past run's figures (N1) |
| RS4, PR body | RESOLVED | The PR body cites issuecomment-6739542795 |
| SG1, SG2 | ADOPTED | Token anchors; width asserts with controls |

## Real limits

- No physical hardware, no Vivado, and no physical calibration (NOT RUN). Field skips are not hardware proof.
- I did not re-run the full sweep, the builder bank, the workflow `run:` steps or the LiteX simulations. For those I rely on:
  - the author's published round 4 receipts (four digests spot-checked against `MANIFEST.json`);
  - the hosted runs, which executed at this exact head: `docs`, `rtl-fast` (with `split-cdc`), `elaborate` and `rtl-full`, all success. The one skipped context is Physical gPTP (nightly/manual).
- The twin is not in any workflow. My run above is its only independent execution at this head.
- No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Validate the current-dev merge candidate (source base `a9d69c77`, live `dev` `123f57a9…`) with the builder and native banks at the merge turn, and link the receipts.
- Hosted/act acceptance of this head.
- Carry RS-a, RS-b and RS-c to the residue checklist.
- Merge only with maintainer authorization and two independent positive reviews.

R806-4 FINISHED

[R479] NEGATIVE - exact head 2f0f59291080aeab934e0d72e124fb448c105e12

# R479-1: external review of PR #660 / issue #652

- Round: R479-1, external, cleared context.
- Exact head: `2f0f59291080aeab934e0d72e124fb448c105e12`, tree `a094320f330221d3941c4a417283000b7b13a10a`.
- Source base: `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`. Five commits, 12 files, +780/-102.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. Each lens has artifact-specific evidence below.
- Verdict: NEGATIVE. One MINOR finding (F1) is open under Robustness and Tests. Conformance, RTL and Docs are clean.

## Reconstruction

I read the following, in order:

1. AGENTS.md and CONTRIBUTING.md (commit rule, review format).
2. Issue #652: body, acceptance 1-3, the lane comment, the executor's STOP and the ruling (comment 5983995755: option 1 and items 1-4).
3. The REVIEW READY comment on the issue and the PR #660 body.
4. `hdl/milan/KL_nvm_backend.sv`, `docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2, and `docs/ENDSTATION_BUILDER.md` D8 and section 4.
5. The full diff `6c22d3ca..2f0f5929` and its five one-line commits.
6. The published evidence tree `7ac6966b/review-evidence/652-r1`. From it I compared only the byte-identity hash lists against my own regeneration.

I read no other reviewer's report before writing this verdict and ledger.

## Findings

### F1 - MINOR - Robustness, Tests - `scripts/check_nvm_record_space.py:722` (`allocation_findings`, lines 702-733): check 14 passes a section 4.2 row that has lost a column figure

- **Authority/evidence.** Ruling item 3 asks for the section 4.2 counts "derived and not mirrored". The PR does this through check 14, which it describes in three places:
  - the docstring: "every figure ... that is not the derived one";
  - the page, `SAVED_STATE_FASTCONNECT.md:288-290`: "checks every figure in both ... so a count here moves with the shape or reddens the gate";
  - the PASS line: "every allocation-table figure at 1x1 ..., 8x8 ... is the derived one".

  The loop pairs cells to columns with `zip(ALLOCATION_COLUMNS.items(), cells)`, which stops at the shorter list. A row with one cell fewer therefore skips the missing column without a finding.
- **Reproduction.** Receipt `receipts/c9_short_row.txt`, script `scripts/c9_short_row.sh`, in a disposable copy of the head:
  1. Delete only the 8x8 user-name cell `**107**` from the row `0x80 .. 0xFF`.
  2. Run `check_nvm_record_space.py`. It exits 0 and prints the "every allocation-table figure ... is the derived one" line.
  3. Run `docs_check.py`, `check_doc_style.py` and `gen_toc.py --check`. All three exit 0.
- **Related probe.** A trailing extra cell is also accepted (`receipts/c5_page/results_page.json`, probe p7).
- **Impact.**
  - The 8x8 writable-name count is the figure #652 is about. Once it is absent, nothing checks it, and the page's "reddens the gate" promise is false for that edit.
  - Today's page is correct, so the defect is latent.
  - The self-test has a single control (`stale_allocation_table`, a wrong value). No control covers a missing figure.
- **Required outcome.**
  - Check 14 refuses any body row whose figure-cell count is not exactly the number of named columns. Equivalently, every (row, column) figure must be present and equal to its derived value.
  - A planted control that drops one figure turns the gate red.
- **Verification.** Re-run `scripts/c9_short_row.sh`: `check_nvm_record_space` must exit 1 and name the missing 8x8 user-name figure. The new `--self-test` arm must exit 1 for that reason. The unmutated gate must stay rc 0.

### S1 - SUGGESTION - Conformance, RTL - `scripts/nvm_contract.py:164` `ALLOC["NAME"] = (0x80, 128)`

The focus asked whether this second statement of 128 is a mirror the acceptance forbids. My judgment is that it is not:

- Acceptance 1 and the lane comment bind the builder: "`sw/builder` refuses ... The limit is derived from the RTL ... never mirrored". The builder holds no copy. Its only route to the number is `nvm_name_capacity()`, which reads `KL_nvm_backend.sv:247` and refuses on zero or two matches. Probes b2 and b6 prove the builder follows the RTL.
- `ALLOC` predates #652 and holds the record-space gate's own id map, all twelve bases and blocks. That gate grades the RTL against `ALLOC` by design, so it is an independent expectation, the same kind as gate 38's pinned `_NAME_BLOCK_RECORDS = 128`. It is not a configuration value the builder consumes.
- The PR body discloses it.

Two probes show the trip-wires:

- With `N_NAME_MAX_C` moved to 100 in the RTL, gate 38 goes red ("declares 100 NAME records, the block holds 128"; `receipts/c5_capacity`, k1).
- With `ALLOC` moved to 100, check 14 goes red (k4).

The remaining gap: if the RTL capacity and gate 38's pin moved together to a value from 107 to 127, nothing would compare `ALLOC`, or the page's "128", with `N_NAME_MAX_C`. A one-line equality check in check 14 or gate 38 would close this. Optional.

### S2 - SUGGESTION - Robustness - `syn/resmap/yosys_sweep.py:360-366`: `"expect": "refused"` accepts any builder refusal

For an expected-refused variant, the step accepts any single `CONFIG ERROR:` line, whatever its cause. The line is recorded and flows into the regenerated `guard-refusals` table, so a change of cause would show up on the page. Pinning the expected cause, for example `writable names`, would fail the step earlier. Optional.

### S3 - SUGGESTION - RTL - `hdl/milan/KL_nvm_backend.sv:247`

`ID_NAME_C + N_NAME_MAX_C` filling exactly the 8-bit `record_id` space is unchecked, as it was with the old literal. The PR body discloses this.

My probe planted `N_NAME_MAX_C = 129`. `N_NAME_P = 129` then lints clean under Verilator 5.050 (`receipts/c2/c2_guard.tsv`, rows head-cap129), so an over-large capacity would pass silently. An elaboration check that `ID_NAME_C + N_NAME_MAX_C <= 256` would close this. Optional, and outside #652's acceptance.

No RESIDUE item.

## Lens results (clean lenses in findings format)

```text
[R479] PASS Conformance — issue #652 acceptance 1-3 + ruling 5983995755 items 1-4 vs sw/builder/endstation_builder.py:2689-2750, sw/builder/test_builder.py gate 38 and 24a(d)/(e), syn/resmap/*, docs/design/SAVED_STATE_FASTCONNECT.md 4.2, receipts c1/c3/c4/c5/c7 — refusal fires in the write-free _derive_artifacts pass (endstation_builder.py:5757) before _write_artifact_dir; message names count, capacity and path:line; the capacity is read from the RTL and never mirrored in the builder (probes b2, b6); 128 builds, 129 and 235 refused; gate 38's 235 shape has descriptor counts identical to plan variant rm_ax7101_8x8_tdm8 (c7); five tracked configs: 50 written artifacts byte-identical base vs head, equal to the author's published hashes, and in-tree rewrites leave both trees clean (c3); shapes step: 7 built, 2 refused as expected, rc 0, unmarked plan rc 1 (c4); page refusal rows equal the live refusal lines (c7); only the guard-refusals and datapath-marginals blocks changed of 26, and the marginals lost exactly the two refused rows
[R479] PASS RTL — hdl/milan/KL_nvm_backend.sv:240-295 at 2f0f5929, receipts/c2/c2_guard.tsv, receipts/c6 — N_NAME_MAX_C is declared once as a localparam int unsigned; no port, parameter, default or register changed; base and head give the same verdict and the byte-identical message for N_NAME_P 0/1/99/128/129/235 under pinned Verilator 5.050; with the capacity planted at 127 and at 129 the guard follows it; the AEM_NAME_ENTRIES_C -> DESC_NAME_ENTRIES_P -> N_NAME_P binding (milan_datapath.sv:7681, KL_pp_shadow.sv:1007) is the same count the builder bounds; nvm_backend 751 checks (39/39 mutants killed) and nvm_cosim 465 checks, rc 0; lint_rtl and check_sv_idiom rc 0
[R479] PASS Docs — docs/ENDSTATION_BUILDER.md:99-104, 754-774, 1108-1119; docs/design/SAVED_STATE_FASTCONNECT.md:283-311; docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:26, 91, 103, 597-604, 1118; PR #660 body — D8 restated (712 = 8x(16+1+72) clusters, NAME block first, ROM ceiling second), matching the gate 24a output (747 names); the section 4.2 figures are the derived ones (check 14 rc 0); the 649 page prose matches the regenerated tables and the live refusal; docs_check, check_doc_paths, gen_toc --check, check_em_dash --base 6c22d3ca (0 findings over 66 added lines) rc 0 with the pinned Markdown renderer; commits one-line with no trailers
```

Robustness and Tests are UNCLEAN under F1. Everything else in those lenses was applied and found clean:

- **Gate 38.** Nine controls, all red, at the head. My six builder faults are all caught (`receipts/c5_builder`):
  - `>=` off-by-one;
  - capacity mirrored as a literal;
  - refusal removed;
  - figure dropped from the message;
  - write before derivation;
  - RTL guard on a literal.
- **Gate 24a.** (d) and (e) with 2/2 controls each. Removing the refusal turns 24a(d) red (b8).
- **Name count.** The test's count comes from `nvm_shape.expected_names`, which uses `NAME_SLOTS`, independent of the builder's formula. It is 128, 129 and 235 for the three shapes.
- **Resmap.** All five `--selftest` runs are rc 0. My seven resmap faults are all caught (`receipts/c10_resmap_mutations.json`).
- **Record-space gate.** The `--self-test` controls are all red, including `stale_allocation_table`. Probes p1, p3, p4, p5, p6 and p8 all turn check 14 red.
- **Builder consumers.** `check_entity_shape` and `check_wire_accountability` `--self-test` are rc 0.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #652 acceptance + ruling vs `endstation_builder.py:2689-2750,5747-5960`; gate 38, 24a; `syn/resmap/*`; c3 byte identity (50/50 + in-tree clean); c4 shapes; c7 | R479-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |
| RTL | CLEAN | `KL_nvm_backend.sv:240-295`; c2 guard table base/head/planted; c6 nvm_backend 751 + nvm_cosim 465; lint_rtl, sv_idiom | R479-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |
| Robustness | UNCLEAN (F1) | check 14 malformed-row probes (c5_page, c9); builder refusal ordering (b5); resmap outcome classification (c10, c4 unmarked); unreadable declaration controls | R479-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |
| Tests | UNCLEAN (F1) | gate 38 (9 controls), 24a(d)/(e); c5_builder 8/8 as expected; c10 7/7 red; record-space self-test; resmap self-tests | R479-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |
| Docs | CLEAN | ENDSTATION_BUILDER D8/s1/s4; SAVED_STATE 4.2; 649 page; PR body; doc gates rc 0 | R479-1 | `2f0f59291080aeab934e0d72e124fb448c105e12` |

## Prior public review findings

When this round started, PR #660 and issue #652 carried no review findings, only the two review-start comments. There is nothing to resolve or retain. See the addendum at the end of this report for the check repeated after the verdict.

## Real limits

- **Full builder bank not run.** Per the scope limit, I did not run `test_builder.py --require-rv32`, the full Verilator sweep, Yosys or the PP/gPTP banks. Gates 38 and 24a ran alone, by calling their test functions directly.
- **#649 page tables not regenerated.** That needs the Yosys sweep and #649's published inputs. I verified the following instead:
  - only those two blocks changed, of 26;
  - the marginals table lost exactly the two refused rows;
  - the refusal rows equal the live builder lines.

  "Every other table equals a fresh generation" remains the author's evidence (`new-tables-check.log`). I did not reproduce it.
- **Byte identity, partial comparison.** I compared the 50 written artifacts and the in-tree rewrites. The author's 120 also include 70 in-memory dumps from their own script, which I did not regenerate.
- **No physical calibration or hardware.** Field skips are not hardware proof.
- **Hosted CI incomplete when read.** At this head, `docs-check`, `elaborate` and Verilator shards 0, 1, 2 and 4 were `in_progress`. Physical gPTP was `skipped`. `rtl-fast`, the four Yosys shards, `yosys-elaboration`, `verilator-lint`, Verilator shard 3, `bdd-conformance`, `wire-accountability`, `docs-check-no-git`, `changes` and `full-ci-gate` were `success`. I did not run act.

## Pending manager duties

- Carry F1 back to the executor. Re-review the corrected head on Robustness and Tests (check 14 code and its self-test). Any change to `check_nvm_record_space.py` un-covers those two lenses only, unless it touches other scope.
- Own hosted and act acceptance at the exact head. Several contexts were still running when I read them.
- Build and validate the current-dev candidate at the merge turn. Live dev was `6c22d3ca`, equal to the source base, when this round started.
- Track S1-S3 as optional follow-ups if wanted.

## Receipts

The published files are `REPORT.md` and those listed in `MANIFEST.sha256`:

- `scripts/`: the campaign drivers c1-c5 and c9-c10.
- `receipts/c1`: focused gates and doc gates, with a `head` line.
- `receipts/c2`: the RTL guard table.
- `receipts/c3`: byte-identity hash lists, summary and the comparison with the author's subset.
- `receipts/c4`: shapes step outcomes.
- `receipts/c5_*`: mutation probes.
- `receipts/c6`: the nvm suites.
- `receipts/c7_*`: shape-equality and refusal-row checks.
- `receipts/c8`: clone integrity.
- `receipts/c9`: the F1 reproduction.
- `receipts/c10`: resmap faults.

After the probes, the review clone is unchanged:

- HEAD is `2f0f5929`.
- The index (mode, blob, path) hash equals the `HEAD` tree hash.
- The worktree is clean.
- The gitlinks are `external` efeb541a, `gptp-processor` 5dce647a, `protocol-processor` 631eeb34 and `verilog-axis` 48ff7a7e.

Every probe ran in a disposable copy under `scratch/` and was restored there.

## Addendum: prior findings, re-checked after the verdict

After writing the verdict and ledger above, I listed the public record again: PR #660 issue comments, PR reviews, inline review comments, and #652 comments after REVIEW READY.

- PR #660 carries only the two review-start comments: R478-1 at 5984490362 and R479-1 at 5984490772.
- PR #660 has no review objects and no inline comments.
- #652 has no comment after REVIEW READY.

No prior public finding exists at this head, so none is resolved or retained.

R479-1 FINISHED

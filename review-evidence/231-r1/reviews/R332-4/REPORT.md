[R332] NEGATIVE - exact head 3a1477c528bdf71b7cecadf86383b7579c9197d6

Round R332-4 is an internal, cleared-context delta review of PR #572 for issue #231 (parent epic #229).

- Head: `3a1477c528bdf71b7cecadf86383b7579c9197d6`, tree `054bd9bbf5778ff87649491a10c9b726dea6b37d`.
- Delta judged: `0a506fa8..3a1477c5`. It is one commit touching two files, `syn/ooc/pp_baseline.py` (+138/-23) and `syn/ooc/pp_baseline_mutants.py` (+39). It changes no Markdown, no `hdl/` and no gitlink.
- Full base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`. My previous round, R332-3, covered `0a506fa8`.

All five lenses were applied.

**Verdict: NEGATIVE, on one MINOR Docs finding.**

- **F1:** the committed page and recipe still state the pre-delta self-test counts: "six additional inventory refusals" and "ten" removal mutants. At this head there are 40 inventory refusals and 28 maintained mutants.
- Conformance, RTL, Robustness and Tests are CLEAN.
- The substance of the round is sound:
  - every claimed refusal named in the assignment is now exercised;
  - every maintained mutant is killed by its intended oracle;
  - both prior reviewer mutant scripts, run unchanged, kill every mutant;
  - the production preparation code is unchanged.

## Reconstruction

**Authorities read:**
- AGENTS.md, CONTRIBUTING.md (section 3 review bar) and docs/README.md;
- the #231 body and its frozen acceptance criteria;
- scope decision 5844867171;
- round-two decision 5846064333;
- the round-three assignment 5847401184, which reads "Tests only ... No measurement or page change, except the claim text if a refusal is narrowed";
- [A339] TAKEN 5847417376 and REVIEW READY 5847478136;
- the live PR #572 body at this head;
- the corrected #229 reference, comment 5847400261.

**Public evidence:**
- `c8a1a9a2.../review-evidence/231-r1/author-r3/` (read for the stated claims only; my conclusions rest on my own runs);
- the published reviewer scripts at `c8a1a9a2.../review-evidence/231-r1/reviews/R332-3/scripts/` and `.../R333-2/probe_selftest/`. My local copies are byte-identical by git blob id (`receipts/prior-scripts-blob-ids.txt`).

**Order:**
- The prior public review findings (R332-1, R333-1, R333-2 and my own R332-3) were read only after my independent pass over the diff and after my probes had run.
- The concurrent same-head report of the other reviewer was not read.

## What was executed (review clone at the exact head; Python 3.14.7)

| Check | Result | Receipt |
|---|---|---|
| `python3 -B syn/ooc/pp_baseline.py --selftest` | rc 0. It reports: 9 original refusals, 5 parameter/template refusals, **40 inventory refusals** plus the restored control, 9 endpoint refusals plus a valid pathname, and CLI containment | `receipts/selftest.log` |
| `python3 -B syn/ooc/pp_baseline_mutants.py` | control rc 0; **all 28** maintained mutants rc 1 | `receipts/maintained-mutants.log` |
| Kill reason for each maintained mutant (my `scripts/kill_reasons.py`) | Each of the 28 dies on its intended oracle:<br>- 19 on `missing refusal: <named message>`;<br>- 4 on a named emitted-script assertion (ROM promotion, both attribution constraints, unfiltered hierarchy report);<br>- 3 on the original unit arm (`image depth`, `image width`, `hexadecimal image words`);<br>- `microcode address depth` on the positive-control inventory (`2 != 1`);<br>- `outside repository guard` on the directory mismatch the in-code comment documents.<br>None dies on an unrelated crash | `receipts/maintained-kill-reasons.log` |
| R332-3 `scripts/extra_mutants.py`, **unchanged** (blob `d538928a`) | control-pass; **15/15 killed** | `receipts/R332-3-extra-mutants.log` |
| R333-2 `probe_selftest/mutate2.py`, **unchanged** (blob `1afe4c0a`) | pristine rc 0; **17/17 killed** | `receipts/R333-2-mutate2.log` |
| R332-3 `scripts/ambiguity_probe.py`, unchanged | pristine helper refuses the duplicated `PP_UCODE_HEX_P` binding; the guard-removed helper still accepts it. That mutant is now killed by the self-test (row 1 of the extra-mutants log) | `receipts/R332-3-ambiguity-probe.log` |
| Partial-strength probes of the round's refusals (my `scripts/delta_probe_mutants.py`, 17 mutants) | 11 killed, 6 survived. The survivors are discussed under S1/S2 and are equivalent or outside the claims | `receipts/delta-probe-mutants.log` |
| Production code unchanged (`scripts/prod_unchanged.py`, AST comparison of every non-self-test definition between `0a506fa8` and `3a1477c5`) | All `same`. The only addition is `from collections.abc import Iterator` for the new test helper | `receipts/prod-unchanged.txt` |
| No page or measurement change | 0 Markdown files in the delta; the PR's raw diff has the same 13 paths as before; gitlinks are identical to the base | `receipts/doc-claims-vs-selftest.txt`, `receipts/pr-raw-diff.txt`, `receipts/gitlinks-head.txt` |
| Focused gates | `check_py_idiom`, `measure_test_evidence --check`, `check_doc_paths`, `check_doc_style` and `docs_check -B` all rc 0. `check_em_dash` gave rc 2 because the pinned renderer is not installed (environment only, no shared installs allowed). A direct substitute found 0 U+2014 in added Markdown lines since the base, and the delta has no Markdown | `receipts/gate-*.log`, `receipts/em-dash-substitute.txt` |
| #229 reference 5847400261 | carries the default-versus-attribution distinction. All 12 quoted figures equal page rows `:192-193`, and that page is unchanged since `0a506fa8` | `receipts/issue229-comment-5847400261.txt`, `receipts/issue229-figures-vs-page.txt` |
| Clone restored | HEAD, tree, index tree `054bd9bb`, index entries equal to HEAD tree entries (mode, oid, path), empty status including ignored files, and submodule gitlinks all verified | `receipts/clone-state-after.txt` |

**Assignment items checked against the head:**
- Duplicated binding: `pp_baseline.py:345-346`, all three image parameters. Missing binding: `:347`.
- Duplicated package: `:354`. Missing package: `:355`.
- Duplicated or missing depth/width declaration, for all three packages: `:357-362`.
- Generated-ROM short, long, narrow and wide: `:325-329`.
- Parameter-ROM short, narrow and wide: `:342-344`.

Each case asserts its own diagnostic through `expect_refusal` (`:240-249`), so an unrelated exception cannot count as a refusal. A restored control follows the cases (`:375-377`). The maintained list names a mutant for each claimed line (`pp_baseline_mutants.py:23-43, 59-76`), and each one uniquely matches its line.

## Findings

### F1 - MINOR - Docs - `docs/findings/PP_SHADOW_BASELINE.md:282`, `:285`; `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:382` - The page and recipe state the superseded self-test and mutant counts

**Authority:**
- AGENTS.md section 6, Docs lens: changed contracts are reflected in authoritative docs, and the PR and issue carry enough evidence for another cold reviewer.
- The recipe's verification step is a documented instruction whose expected output a reader checks.

**Evidence** (`receipts/doc-claims-vs-selftest.txt`):
- At this head the page says "Synthetic exports exercise six additional inventory refusals and CLI containment" (`:282`). The self-test prints "40 refusals and restored control" for the inventory and "9 refusals" for the endpoint arm.
- The page says "Ten enforcement-removal mutants all fail" (`:285`). The recipe says "Run the ten removal mutants alongside the positive control" (`:382`), directly above the command. That command now runs 28 mutants. There were 10 at `0a506fa8` and 28 at this head.
- The delta itself removed the self-test's "6 inventory refusals" output text, so the page now disagrees with the tool it describes.
- The PR body's Round 3 section says 28 and 40, but the committed documentation does not.

**Impact:**
- A cold reader following the recipe sees 28 mutant rows where the recipe promises ten, and 40 inventory refusals where the page promises six.
- The page is the reference #229 will point at for the remaining optimization tickets. Its verification claims are no longer checkable as written.
- The error understates coverage, so it misleads nobody about safety. That is why it is MINOR, not MAJOR.

**Required outcome:** the page and recipe state counts that match the self-test and the maintained list at the merge head, or wording that does not go stale with every mutant added. The round-three assignment permits a page change only "if a refusal is narrowed". So this needs the manager either to authorize a claim-text-only edit of these three lines, or to record a public decision to accept the stale counts. Under AGENTS.md section 2, I am publishing the conflict rather than choosing between those.

**Verification:** at the corrected head, check `grep -rn 'six additional\|ten removal\|Ten enforcement' docs/` against `pp_baseline.py --selftest` output and the length of `MUTANTS`. Docs is then re-covered, along with any other lens whose scope the edit touches.

### Suggestions (do not affect coverage)

**S1 - SUGGESTION - Tests - `syn/ooc/pp_baseline.py:433` (fixture `UPC_W_C = 1`), guarding `:179-180`.**
- With an address width of 1, `1 << n` equals `2 * n` and `n + 1`. Those two alternative derivations therefore survive (`receipts/delta-probe-mutants.log`).
- In the real flow `UPC_W_C = 11`, so a wrong derivation would refuse the valid 2,048-word images loudly rather than accept a truncated one. That is why this is not a finding.
- A fixture width of 3 (8 words) would distinguish all three derivations.

**S2 - SUGGESTION - Tests - `syn/ooc/pp_baseline.py:164-166`.**
- Weakening readmemh equality to "every readmemh file is inventoried" (a subset check) survives. No synthetic case has a declared, present `.init` file that is not read by `$readmemh`.
- The effect would be an extra hashed image that synthesis does not consume, not a missing one. This behaviour predates the delta.

**Equivalent or benign survivors (no action):**
- deduplication of `packages` by path and of `matches` by value: the tests use distinct paths, so behaviour differs only when the same file is named twice;
- my `name != "rom" and name == "sram"` probe, which is logically identical to the original.

**Carried from R332-3, unchanged and still optional:**
- S1: assert after synthesis that `KEEP_HIERARCHY` took effect;
- S2: name the attribution residual's load stems.

## Prior public review findings: resolution at this head

| Prior finding | Status at `3a1477c5` | Evidence |
|---|---|---|
| R332-3 F1 MINOR (Tests, Conformance): the ambiguity guard `:174-175` and declaration uniqueness `:143-144` survive removal | **Closed** | Mutants "image and geometry ambiguity", "image binding uniqueness", "geometry package uniqueness" and "geometry declaration uniqueness" are killed on the named refusal (`receipts/maintained-kill-reasons.log`). The unchanged `extra_mutants.py` rows 1-2 are killed. In `delta-probe-mutants.log`, each one-direction weakening is killed. The allow-duplicate direction dies on the named refusal. The allow-missing direction dies on an `IndexError` at `matches[0]`, `packages[0]` or `hits[0]`, so it cannot pass silently. |
| R332-3 F2 MINOR (Conformance, Docs): the #229 reference publishes unqualified default-flow figures | **Closed at this head; merge-turn link update pending** | Comment 5847400261 explicitly supersedes 5845524962. It separates default-flow totals from boundary-preserving attribution, gives both columns (matching page `:192-193`), and says to use attribution for ticket choice. It names PR #572 at `0a506fa8` rather than `af6d19c5`; the page is byte-unchanged since then. It promises an update with the merge commit, which R332-3 F2's own verification places at the merge turn (a manager duty below). |
| R332-3 S3 (seven lesser guards survive) | **Answered** | All seven are now maintained mutants, killed on their named refusal. |
| R333-2 F4 residual MINOR (Tests): five claimed-enforcement mutants survive | **Closed** | `mutate2.py`, unchanged: generated-ROM depth and width, parameter-ROM width, the ambiguity refusal and declaration ambiguity are all killed, and so are the seven lesser guards (17/17). |
| R333-2 F1 residual MINOR (Conformance, Docs): #229 reference | **Closed at this head**, same evidence as R332-3 F2 | |
| R333-2 S1, S3-S6 | Not in this delta's scope and unchanged; still optional | |
| R332-1 F1-F3, R333-1 F1-F4 | Closed at `0a506fa8` (R332-3, R333-2). The delta touches none of their artifacts except the self-test, which only gains arms | `receipts/prod-unchanged.txt` |

Reading these findings changed no verdict, finding or ledger row above.

## Clean lenses

- `[R332] PASS Conformance - issue 231 comment 5847401184 items 1-2; syn/ooc/pp_baseline.py:314-377 and pp_baseline_mutants.py:12-77 at 3a1477c5; issue 229 comment 5847400261 - checked each assignment bullet against a named case and a maintained mutant (above).`
  - The frozen #231 acceptance criteria are unaffected: no measurement, page or RTL change (`receipts/pr-raw-diff.txt`, `receipts/prod-unchanged.txt`).
  - The #229 reference now carries the default-versus-attribution distinction with figures equal to the page.
- `[R332] PASS RTL - git diff --raw 7eb3b0d4..3a1477c5 (no hdl/ path) and git ls-tree gitlinks equal to base (receipts/gitlinks-head.txt); AST identity of REPORTS, PP_REPORTS, SCOPE_TIMING, ROM_ERROR and prepare() (receipts/prod-unchanged.txt) - the emitted Vivado scripts, constraints and clocks cannot differ from those covered at 0a506fa8, and no module or interface contract is touched.`
- `[R332] PASS Robustness - syn/ooc/pp_baseline.py:139-236 unchanged (receipts/prod-unchanged.txt); :363-377 restore-in-finally with restored control; receipts/R332-3-ambiguity-probe.log; receipts/clone-state-after.txt - checked the following.`
  - The pristine helper still refuses malformed, ambiguous and truncated inputs.
  - Every self-test mutation is restored before the next one, and a clean inventory is re-proved afterwards.
  - Test fixtures live only under a temporary directory.
  - The review clone is byte-identical after all probes.
- `[R332] PASS Tests - syn/ooc/pp_baseline.py:240-418, pp_baseline_mutants.py at 3a1477c5; receipts/maintained-mutants.log, maintained-kill-reasons.log, R332-3-extra-mutants.log, R333-2-mutate2.log, delta-probe-mutants.log - checked the following.`
  - All 28 maintained, 15 R332-3 and 17 R333-2 mutants are killed, with each maintained kill on its intended oracle.
  - All controls pass.
  - `rtl-fast.yml:209-211` still runs the self-test and the mutant driver.
  - S1 and S2 are optional.

Docs is UNCLEAN (F1). It was applied to page `:276-290`, recipe `:370-391`, the PR body Round 3 section and #229 comment 5847400261. The gates listed above passed.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 5847401184 items 1-2 against `pp_baseline.py:314-377` and `pp_baseline_mutants.py:12-77`; #231 AC; `pr-raw-diff.txt`; `prod-unchanged.txt`; #229 comment 5847400261 against page `:192-193` | R332-4 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |
| RTL | CLEAN | `git diff --raw 7eb3b0d4..3a1477c5` (no `hdl/`); gitlinks equal to base; AST identity of emitted-script constants and `prepare()` | R332-4 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |
| Robustness | CLEAN | `pp_baseline.py:139-236` (unchanged), `:363-377`; `R332-3-ambiguity-probe.log`; `clone-state-after.txt` | R332-4 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |
| Tests | CLEAN | self-test (9 + 5 + 40 + 9 refusals); 28 maintained mutants with kill reasons; unchanged R332-3 (15/15) and R333-2 (17/17) scripts; 17 partial-strength probes; `rtl-fast.yml:209-211`; focused gates | R332-4 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |
| Docs | UNCLEAN (F1, MINOR) | `PP_SHADOW_BASELINE.md:276-290`; `PP_SHADOW_BASELINE_RECIPE.md:370-391`; PR body Round 3; #229 comment 5847400261; `check_doc_paths`/`check_doc_style`/`docs_check` rc 0; em-dash substitute | R332-4 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |

## Real limits

- **Delta round.** No synthesis, place-and-route, Yosys or builder run was repeated. The measurements are unchanged since `0a506fa8`, where R332-3 reproduced them, and this delta touches none of them.
- **Em-dash gate.** `check_em_dash` could not run because its pinned renderer is not installed and shared installs were not allowed. A direct U+2014 scan of added Markdown lines substitutes for it, and the delta adds no Markdown.
- **Hosted checks.** Exact-head hosted checks were read at review time (`receipts/hosted-check-runs.txt`):
  - `docs-check`, `elaborate`, `yosys-elaboration` and the five Verilator shards were still in progress;
  - the other contexts had succeeded;
  - `Physical gPTP` was skipped, and that skip is not hardware evidence.

  Hosted and act acceptance belong to the manager.
- **Not run:** no full parent, processor, gPTP, Yosys or builder bank; no candidate build, act, Docker or hardware run. The scoped Verilator was not needed and was not used. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Resolve F1: authorize a claim-text-only edit of page `:282`, `:285` and recipe `:382`, or record a public decision to accept the stale counts. Then have the corrected head re-reviewed. A Markdown-only claim edit re-opens Docs at minimum.
- Update #229 comment 5847400261 with the merge commit, as it promises, at the merge turn.
- Complete hosted and act acceptance on the final head.
- Build and validate the current-dev candidate at the merge turn (source base `7eb3b0d4`, live dev `831f94f4`).
- Assemble the completion ledger with the external review.
- Merge only with maintainer authorization, then run post-merge containment.

Receipts and portable scripts are listed in `MANIFEST.sha256`. Prior reviewer scripts are under `scripts/prior-unchanged/`, byte-identical to their published blobs.

R332-4 FINISHED

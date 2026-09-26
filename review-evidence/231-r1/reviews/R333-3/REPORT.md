[R333] NEGATIVE - exact head 3a1477c528bdf71b7cecadf86383b7579c9197d6

# R333-3 external review: issue #231 / PR #572

Reviewer: [R333], external independent reviewer, round R333-3.
Head `3a1477c528bdf71b7cecadf86383b7579c9197d6`, tree `054bd9bbf5778ff87649491a10c9b726dea6b37d`
(verified in the review clone, `receipts/review_clone_integrity.txt`).

This is a delta review. Round R333-2 covered `0a506fa8`. This round judges `0a506fa8..3a1477c5`:
one commit, `test: cover baseline export geometry and ambiguity refusals`. It is one line with no
trailers and touches two files, `syn/ooc/pp_baseline.py` (+138 / -23) and
`syn/ooc/pp_baseline_mutants.py` (+39). Every lens is re-applied at this head.

Context was reconstructed from these sources:

- AGENTS.md and CONTRIBUTING.md.
- docs/README.md.
- Issue #231: the round-three assignment 5847401184, TAKEN 5847417376 and REVIEW READY 5847478136.
- The corrected #229 reference 5847400261 and the superseded one, 5845524962.
- The PR #572 body at this head.
- The diff and its history.
- The public evidence tree `review-evidence/231-r1/author-r3` at `c8a1a9a2`.

The verdict, findings and ledger below were written before any other reviewer's report was read.
The disposition of prior findings follows them and says when it was written.

## Verdict

NEGATIVE, on one MINOR documentation finding that this commit introduced. The substance of the
round is done well:

- Every refusal the assignment enumerates is now exercised on a synthetic export and is checked
  by its own diagnostic.
- Every maintained mutant dies at the refusal it is named for.
- Both reviewers' earlier probe scripts, rerun unchanged, kill every mutant.
- Production code is unchanged apart from one type-hint import.

The finding is that the page and the recipe still state the old self-test and mutant counts
("six additional inventory refusals", "ten" mutants). At this head the self-test runs 40
inventory refusals and the maintained list has 28 mutants.

## Checks against the round-three assignment (issue 231 comment 5847401184)

1. **Synthetic export refuses each claimed case.** Met. `syn/ooc/pp_baseline.py:314-377` builds
   40 independent mutations of a valid synthetic export. Each is checked with
   `expect_refusal` (`:240-249`), which requires the named `ValueError` text and rejects any other
   exception. After each mutation, the clean input is restored in `finally`, and the restored
   export must pass again (`:375-376`). The cases, one run each (`receipts/selftest_head.txt`):
   - A duplicated `.<PARAM>("...")` binding and a missing binding, for all three control-ROM
     families (`:345-347`). The diagnostic names the family.
   - A duplicated geometry package (a second `read_verilog` of the same basename) and a missing
     one, for all three families (`:349-356`).
   - A duplicated and a missing depth and width declaration, for each of the three packages
     (`:357-362`).
   - Generated-ROM short, long, narrow and wide (`:325-329`).
   - Parameter-ROM short, narrow and wide, for each family (`:342-344`).
   - The three earlier inventory cases, now with their diagnostics pinned (`:319-323`).

   Nine endpoint and pathname refusals (`:380-418`) and five parameter and template refusals
   (`:299-310`) were added as well. A valid string pathname positive control is included
   (`:401-403`).
2. **Maintained mutant for each line, killed by name; clean control passes.** Met.
   - `syn/ooc/pp_baseline_mutants.py:23-43` adds `generated ROM depth`, `generated ROM width`,
     `parameter ROM width`, `image and geometry ambiguity`, `image binding uniqueness`,
     `geometry package uniqueness`, `geometry declaration uniqueness` and
     `microcode address depth`.
   - `:59-76` adds ten further guards.
   - The runner refuses a non-unique pattern (`:89-90`), so each mutant's line exists exactly
     once.
   - `receipts/maintained_mutants_head.txt`: control rc 0 and all 28 mutants rc 1.
   - `receipts/round3_probe_head.txt` part A imports the same list and records each mutant's
     final diagnostic. Every mutant fails at its own refusal: for example, "missing refusal:
     ambiguous image or geometry source: PP_TROM_HEX_P" for both uniqueness halves, and "expected
     one decimal declaration of TROM_DEPTH_C" for the declaration guard. None fails at an
     unrelated crash.
3. **Both reviewers' scripts, unchanged, kill every mutant.**
   - The copies are hash-identical to the public revisions (`receipts/rerun_script_identity.txt`:
     `7846af5f...` and `7a12dd2a...`, the same as `author-r3/probe-provenance.json`).
   - `receipts/r333_mutate2_head.txt`: pristine rc 0 and 17/17 killed. At `0a506fa8`, 12 of these
     survived.
   - `receipts/r332_3_extra_mutants_head.txt`: control passes and 15/15 killed.
4. **No measurement or page change beyond claim text.** Met literally: `git diff 0a506fa8..HEAD
   -- docs` is empty, and `receipts/production_unchanged.txt` shows every production definition
   identical. The only production-level addition is `from collections.abc import Iterator`,
   which the test helper uses. As a result, though, the claim text now understates the self-test
   (F1).
5. **#229 reference carries the default-versus-attribution distinction.** Met. Comment 5847400261
   explicitly supersedes 5845524962. It names default-flow totals as the implementation baseline
   and attribution as the source for choosing tickets. All twelve of its figures equal
   `docs/findings/PP_SHADOW_BASELINE.md:192-193` at this head. It says "currently at head
   `0a506fa8`". That is harmless because the pages are byte-identical at `3a1477c5`, and the
   comment promises an update at merge.

## Additional probes (reviewer-owned)

- `scripts/round3_probe.py` part B applies 18 partial or boundary weakenings that the maintained
  list does not spell. Examples: ambiguity checked for only the first or only the last family,
  one-directional `<` or `>` uniqueness, suffix-matched package names, a binding regex without
  its leading dot (which makes `PP_UCODE_HEX_P` match `GPTP_UCODE_HEX_P`), one-directional depth
  and width, and width ignored for the gPTP family only. Results:
  - 17 are killed.
  - The three "missing crashes with `IndexError`" variants (B04, B06, B08) are killed because
    `expect_refusal` does not accept an unrelated exception. The production behaviour in those
    variants would still be a refusal, so these are strictness, not gaps.
  - B18 survives. It is pre-existing and outside this delta; see S1.
- `receipts/gates.txt` and `receipts/gates_markdown.txt`: rc 0 for all of these at this head:
  - `docs_check.py`: 0 findings across 894 files;
  - `check_doc_paths.py`: 848 paths;
  - `check_py_idiom.py`;
  - `check_doc_style.py`;
  - `gen_toc.py --check` and `--verify-anchors`;
  - `check_em_dash.py --base 7eb3b0d4`;
  - `measure_test_evidence.py --check`;
  - `ci_events.py --check`;
  - `pp_baseline_reports_selftest.py`;
  - `git diff --check 7eb3b0d4 3a1477c5`.

  The pinned Markdown renderer was loaded read-only from an existing environment through
  `PYTHONPATH`; nothing was installed.
- Hosted, exact head (`receipts/hosted_check_runs_head.tsv`, first read at 15:36Z and refreshed at 15:39Z; shard 3/5 has since succeeded):
  - Completed successfully: `verilator-lint`, the four Yosys shards, `bdd-conformance`,
    `changes`, `full-ci-gate`, `wire-accountability` and `docs-check-no-git`.
  - Still in progress: `yosys-elaboration` (the job that runs the baseline self-test and
    mutants), `elaborate`, `docs-check` and the Verilator shards.
  - `Physical gPTP` is **skipped**, which is not hardware evidence.

## Findings

### F1 - MINOR - Docs

Location:

- `docs/findings/PP_SHADOW_BASELINE.md:282` ("Synthetic exports exercise six additional inventory
  refusals and CLI containment.");
- `docs/findings/PP_SHADOW_BASELINE.md:285` ("Ten enforcement-removal mutants all fail; the
  unchanged control passes.");
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:382` ("Run the ten removal mutants alongside the
  positive control:").

Title: the authoritative page and recipe state self-test and mutant counts that this commit made
false.

Authority and evidence:

- AGENTS.md section 6 Docs lens: "Changed contracts are reflected in authoritative docs" and "the
  PR and Issue contain enough evidence for another cold reviewer".
- At `0a506fa8` both counts were true: six inventory mutations and ten `MUTANTS` entries.
- At this head, `python3 syn/ooc/pp_baseline_mutants.py` prints 28 mutant lines
  (`receipts/maintained_mutants_head.txt`), and the self-test prints "40 refusals"
  (`receipts/selftest_head.txt`).
- The PR body's Round 3 section states the new counts (40, 28), so the PR and the committed page
  now disagree.
- The assignment allowed "the claim text if a refusal is narrowed". Here the coverage widened,
  so the executor reasonably left the page alone. That is a scope gap, not an executor error, and
  it is published here as such.

Impact: an operator following the recipe is told to expect ten removal mutants and sees 28. A
cold reviewer comparing the durable record with its own gate output finds a numeric
contradiction in the claim the round existed to make true. The error understates enforcement,
so no guarantee is overstated. That is why this is MINOR and not higher.

Required outcome: the page and the recipe describe the self-test and maintained mutants as they
are at the merge head. Either state the current counts or use count-free wording such as "every
maintained enforcement-removal mutant fails". This is a claim-text change only, with no
measurement, and needs the manager's scope confirmation because the frozen assignment named no
page change.

Verification: the three cited lines match `pp_baseline_mutants.py` and the self-test's printed
refusal counts at the new head, and the documentation gates stay rc 0.

### Suggestions (do not affect coverage)

- **S1 (Tests, Robustness). The unsupported-log-value refusal is unpinned. It is pre-existing and
  outside the delta.**
  - `syn/ooc/pp_baseline.py:99` refuses a parameter line whose value format the parser does not
    model.
  - Replacing that `raise` with `continue` leaves the self-test green (probe B18).
  - `receipts/unsupported_value_probe.txt` shows the consequence. The mutant turns a log override
    `32'h2` into the wrapper default `8`, silently, and would emit standalone scripts at the wrong
    geometry. The pristine helper refuses.
  - The page and recipe claim this refusal only generically ("malformed ... inputs"). The
    measured logs parsed all 20 parameters, so no published figure is affected.
  - A one-line synthetic case and a maintained mutant would pin it.
- **S2 (Docs).** The PR body's Round 3 section ends "The local round-three commit is ready for
  independent re-review", but that commit is now the published head. The corrected #229 comment
  says "currently at head `0a506fa8`". Both are accurate in substance and can be refreshed when
  the manager next edits them.
- My earlier suggestions S1 (a rehash command in the recipe), S3 (a post-synthesis
  `KEEP_HIERARCHY` assertion), S4 (the routed attribution probe result on the page) and S6
  (report self-test survivors) are untouched by this delta and remain optional. S5 (the stale
  "unpushed" PR-body text) is resolved: that text is gone.

## Lens results

- **Conformance: CLEAN.** Assignment items 1 and 2 were verified with receipts above. The unchanged
  reviewer scripts kill every mutant. Measurement and page are unchanged, and the #229 reference
  carries the qualification with figures equal to the page. No acceptance criterion was
  rewritten.
- **RTL: CLEAN.** The lens is inapplicable to the delta, and here is the evidence:
  - `git diff --name-only 7eb3b0d4..3a1477c5` contains no `hdl/` or submodule path.
  - All four gitlinks are identical to base `7eb3b0d4`.
  - Every production definition of the measurement helper is AST-source-identical to
    `0a506fa8`, so no measured figure or emitted script can differ.
  - The RTL-facing measurement evidence covered at `0a506fa8` is unaffected, since nothing in the
    lens's scope changed.
- **Robustness: CLEAN.**
  - The test harness restores every mutated fixture in `finally` and re-proves the restored
    export.
  - Unrelated exceptions are not counted as refusals (B04, B06, B08, B17).
  - Output containment and the two endpoint guards are now exercised at both `prepare()` and
    the CLI.
  - The self-test leaves no residue: the review clone's status is empty after every run.
  - S1 is optional.
- **Tests: CLEAN.**
  - 28 of 28 maintained mutants are killed, each at its named refusal.
  - My reviewer probes kill 17 of 17 (earlier script) and 17 of 18 new boundary variants. The
    survivor is pre-existing and not an enumerated claim (S1).
  - The other reviewer's script kills 15 of 15.
  - The report self-test passes.
  - Positive controls (three default scripts, attribution, a valid pathname, the restored
    export) pass.
- **Docs: UNCLEAN** (F1).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue 231 comment 5847401184 items 1-2; `syn/ooc/pp_baseline.py:314-418`; `syn/ooc/pp_baseline_mutants.py:12-77`; `receipts/selftest_head.txt`, `maintained_mutants_head.txt`, `r333_mutate2_head.txt`, `r332_3_extra_mutants_head.txt`, `rerun_script_identity.txt`; #229 comment 5847400261 against `docs/findings/PP_SHADOW_BASELINE.md:189-193` | R333-3 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |
| RTL | CLEAN | `receipts/review_clone_integrity.txt` (gitlinks at base and head, no `hdl/` or submodule path in `7eb3b0d4..3a1477c5`); `receipts/production_unchanged.txt` (every production definition identical to `0a506fa8`) | R333-3 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |
| Robustness | CLEAN | `syn/ooc/pp_baseline.py:240-249,363-376,380-418,99`; `receipts/round3_probe_head.txt` (B04/B06/B08/B17 and B18); `receipts/unsupported_value_probe.txt`; empty `git status` after each run | R333-3 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |
| Tests | CLEAN | `syn/ooc/pp_baseline.py:252-496`; `syn/ooc/pp_baseline_mutants.py`; `receipts/maintained_mutants_head.txt`, `round3_probe_head.txt` (parts A and B), `r333_mutate2_head.txt`, `r332_3_extra_mutants_head.txt`, `r332_2_extra_mutants_head.txt`, `gates.txt` (reports self-test, test-evidence ratchet) | R333-3 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |
| Docs | UNCLEAN (F1, MINOR) | `docs/findings/PP_SHADOW_BASELINE.md:278-287`; `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:236-252,372-392`; PR #572 body; #229 comment 5847400261; `receipts/gates.txt`, `gates_markdown.txt` | R333-3 | 3a1477c528bdf71b7cecadf86383b7579c9197d6 |

## Limits

- No synthesis, route or builder run was repeated. Production code is identical to `0a506fa8`,
  where round R333-2 reproduced the measurements from a clean checkout. The earlier real-export
  truncated-ROM probe was not re-run; its export was disposable. The mutant it demonstrated,
  generated-ROM depth, is now killed by the self-test.
- The scoped Verilator was not used: the delta contains no RTL or testbench.
- The older script from round R332-2 (`receipts/r332_2_extra_mutants_head.txt`) was also run
  unchanged, for information. Four mutants survive:
  - X05 is S1.
  - X07 is equivalent. `int()` still refuses a non-literal default, which is the recipe's claim.
  - X14 and X16 alter emitted Tcl checks that no document claims the self-test pins.
- Physical calibration was not run. The hosted `Physical gPTP` context is skipped and is not
  hardware proof.
- The Markdown gates used a pinned renderer loaded from another local environment's
  site-packages, read-only. Their output matches the executor's published logs.

## Pending manager duties

- Decide F1's claim-text change and obtain a re-review of it.
- Accept the exact-head hosted `rtl-fast`, `yosys-elaboration`, Verilator and Yosys contexts,
  which were partly still running at 15:36Z, and the act replica.
- Build and validate the final candidate on live `dev` (`831f94f4`). It is distinct from this
  source validation on base `7eb3b0d4`.
- Obtain two independent positive reviews and the explicit maintainer merge authorization.
- Update the #229 reference with the merge commit, as it promises.

## Prior public review findings on this PR

This section was written at about 15:39Z. That was after the verdict, findings and ledger above,
and after reading PR comment 5847397455 ([R332] round 3, the other published round at
`0a506fa8`). Round R332-2 was voided by the manager (5847037668) and published no findings.

| Finding | Status at `3a1477c5` | Evidence |
|---|---|---|
| R332-3 F1 MINOR (Tests, Conformance) = R333-2 F4 residual: claimed ambiguity and geometry refusals removable with the self-test green | **CLOSED** | The ambiguity guard (`pp_baseline.py:175`) and the declaration guard (`:144`) are each killed, as the full mutant and as each half. All five R333-2 F4 mutants are killed (`r333_mutate2_head.txt`). The finding's own verification passes: `r332_3_extra_mutants_head.txt` shows the first two rows killed and the control passing. `maintained_mutants_head.txt` passes, and the maintained list includes each removal. The functional case R332-3 probed, a second partial `PP_UCODE_HEX_P` binding, is exactly the `PP_UCODE_HEX_P duplicate` refusal in `selftest_head.txt`. |
| R332-3 F2 MINOR (Conformance, Docs) = R333-2 F1 residual: #229 reference unqualified | **CLOSED** at this head | Comment 5847400261 supersedes 5845524962. It states that default-flow totals are the implementation baseline and that attribution is the ownership source. It gives both figures side by side, equal to page `:192-193`, and no longer links `af6d19c5`. Linking the merged page is promised for the merge turn, and that is listed as a manager duty above. |
| R332-3 S3 (seven further guards unpinned) and the seven lesser guards in R333-2 F4 | **Resolved** | Wrapper-declaration equality, empty block, integrated directory, both attribution endpoints, single `synth_design` and pathname characters are each killed by name (`maintained_mutants_head.txt`, `round3_probe_head.txt` part A). |
| R332-3 S1 = R333-2 S3 (no post-synthesis `KEEP_HIERARCHY` assertion) | Unchanged; optional | Untouched by the delta. |
| R332-3 S2 (residual load stems and SRP increase not named) | Unchanged; optional | Untouched by the delta (docs byte-identical). |
| R333-2 S5 (PR body "unpushed") | **Resolved** | That text is gone. A similar round-three phrase is noted as S2 above. |
| R333-2 S1, S4, S6; R332-1 S1, S2; R333-1 S2 | Unchanged; optional | Untouched by the delta. |
| R333-1 F1-F4, R332-1 F1-F3 | Remain **CLOSED** | Both rounds at `0a506fa8` closed them. This delta changes no document, measurement or production code (`production_unchanged.txt`, empty docs diff). |

Reading these did not change the verdict, findings or ledger above. No prior round raised F1,
because it did not exist before this commit.

Receipts and portable scripts are listed in `MANIFEST.sha256`. The `scratch/` tree is disposable
and is not published. The hosted-context receipt was refreshed at 15:39Z:
`yosys-elaboration`, `elaborate`, `docs-check` and four Verilator shards were still in progress,
the remaining executed contexts had succeeded, and `Physical gPTP` was skipped. After all probes,
the review clone is exactly at `3a1477c5`, with an identical index and worktree, 918 of 918
tracked blobs rehashed identical, and four gitlinks equal to base
(`receipts/review_clone_integrity.txt`).

R333-3 FINISHED

[R831] POSITIVE - exact head 3c58b143eac812d173b4326423c030b65ec63f9a

# R831-2: internal cleared-context delta review of PR #893 (issue #883)

- Head `3c58b143eac812d173b4326423c030b65ec63f9a`, tree `df75ea455a6bd742a4614b97e6dd5813d369991f` (`git rev-parse HEAD HEAD^{tree}`, and `git write-tree` gives the same tree).
- Previously reviewed head `e18c822536ebeaf1cb0f42abea74513501aa26c7` (R831-1 and R832-1, both NEGATIVE on the same MINOR F1). The source base is `46c971fa`, an ancestor of the head. Live dev is `fa6c094b`.
- Scope: the round 3 ruling (#883 issuecomment-6809058443) allows tooling and docs only. That means F1 in `scripts/check_cpp_idiom.py` and the residue R1 (the PR body's #495 row) and R2 (`TESTING.md:357`).
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR is open. F1 and both residue items are resolved at this head. Three SUGGESTIONs and one RESIDUE are listed below, and none of them moves a lens.

## Delta scope (verified)

- `git diff --raw e18c8225..3c58b143` touches exactly two blobs, both mode 100644:
  - `scripts/check_cpp_idiom.py` (`ce7df5cd` -> `4de2cf2d`), which holds both the rule and its selftest;
  - `docs/testing/TESTING.md` (`b1e46db9` -> `05e39eb3`).
- No other path changed: no image, RTL, firmware, generated record or budget file.
- The six gitlinks are identical to `e18c8225`, including protocol-processor `801ef228` and gptp-processor `1616fc8f`.
- Two commits, `8f3735d7` and `3c58b143`. Each is a one-line subject with no body or trailer.
- The PR text was changed outside git. I read it at this head (`receipts/pr893_body_at_3c58b143.txt`; the API reports PR head `3c58b143`).
- Dev drift `46c971fa..fa6c094b` touches 3 paths, none of them `check_cpp_idiom.py`, `cpp_idiom.budget`, `check_py_idiom.py` or `TESTING.md`. The manager still owns the merge candidate.

## Prior public findings at this head

I resolved these after my own independent pass over the diff.

| Prior finding | Status at `3c58b143` | Evidence |
|---|---|---|
| F1 (R831-1 = R832-1 F1), MINOR, Tests and Robustness: the multi-declarator rule stopped counting a second declarator beside a nested brace initialiser | **Resolved.** | See "F1 verification" below. |
| R831-1 R1 = R832-1 R3, RESIDUE, Docs: the PR body's #495 row 6731336971 claimed the whole row was taken | **Resolved.** | PR body line 86 now lists the four items one by one: item 3 taken (`Makefile:667-670`), item 2 taken (`TESTING.md:357`), items 1 (`SUBMODULES.md:813`) and 4 (the route note's "(80)") open on #495. This matches both prior exact fixes. |
| R831-1 R2 = R832-1 R1, RESIDUE, Docs: `TESTING.md:357` said "the three gate mutants" | **Resolved.** | `TESTING.md:357` now reads "the six gate mutants". `crflic_mutants.py:91-116` holds six gate arms: every gate, the CRF licence alone and the AAF source 0 gate alone, each once reading the raw verdict and once dropping the real grant. The Makefile (`:665`) says the same. No other "three gate mutants" remains in the parent tree. |
| R832-1 R2, RESIDUE, `syn/ooc/pp_resource_baseline.json:451` "+29 slices (80)" | **Retained** as residue on #495. | The round 3 ruling did not take it, and PR body line 86 says it stays open on #495. It is outside this delta. |
| R831-1 S1 to S3, SUGGESTION | **Retained**, optional. | Their artifacts are outside the delta. |

## F1 verification

All runs are mine, at this head.

- **The pattern** (`scripts/check_cpp_idiom.py:270`): `_DECL_TEXT = (?:[^;(){}\n]|\{(?:[^{}\n]|\{(?:[^{}\n]|\{[^{}\n]*\})*\})*\})*`.
  - At top level a declarator's text may hold no `;(){}`, but it may hold a balanced brace group up to three braces deep.
  - Inside those braces, commas are consumed. The literal `,` in `MULTI_DECL_RE` (`:271`) can therefore only match a comma at brace depth 0, which is a comma between declarators.
  - The comment at `:269` states exactly this bound ("a balanced one-line `{...}` initialiser up to three braces deep is one declarator"). This answers R832-1's note that the old comment claimed more than the pattern did.
- **The selftest arms** (`:705-712`):
  - One declarator gives 0 with flat, once-nested and twice-nested braces (3 arms).
  - Two declarators give 1 beside flat, `{1}`-style, once-nested in either order, and twice-nested braces (5 arms).
  - `python3 -I scripts/check_cpp_idiom.py --selftest` gives `83 checks: 83 PASS, 0 FAIL`, rc 0 (`receipts/check_cpp_idiom.py___selftest.log`). That is the previous 78, minus 3 arms rewritten, plus 8.
- **Planted mutants.** I planted each pattern into a disposable copy with `plant_decl_text_r831.py` and ran the rule-arm group with `ratchet_arms_r831.py` (`receipts/ratchet_arms_*.log`). The unmutated head copy is the control.

  | Copy | Result | Arms that fail |
  |---|---|---|
  | Control (head) | 34/34 PASS | none |
  | Flat-brace pattern of `e18c8225` (the base pattern planted back) | 3 FAIL | the three nested two-declarator arms |
  | Dev's brace-blind pattern | 3 FAIL | the three single-declarator "a brace initialiser's commas separate elements, not declarators (#495)" arms |
  | Pattern reading only one nested level | 1 FAIL | the three-deep two-declarator arm |

  - The `receipts/mutant_selftest_*.log` files are full `--selftest` runs in git-less archive copies. Their non-zero exit is partly a crash in the live-tree stage, which needs `git submodule status`. The unmutated control crashes the same way with 0 FAIL lines (`receipts/mutant_selftest_control_nogit.*`). So the `[FAIL]` lines are the evidence there, and the `ratchet_arms_*` runs are the clean form of the same check.
- **Earlier probe.** R832-1's `probe_cpp_multidecl.py` (blob `c301c0bb`, read before running, read-only) agrees with `real>1` on all 9 rows at this head (`receipts/prior_probe/run_at_3c58b143.log`). The two nested two-declarator rows it flagged at `e18c8225` now give 1, and the nested single row gives 0.
- **Independent oracle.** `probe_multidecl_r831.py` counts declarators as the commas at brace, paren, angle and bracket depth 0, plus one.
  - At the head it agrees on 22 of 22 in-scope rows: up to three braces deep, both orders, three declarators, two nested initialisers on one line, `{}` and empty nested groups, `static const`, `CData`, and pointer declarators.
  - The three mutant patterns are each caught (7, 6 and 1 in-scope disagreements).
  - A 15 kB pathological line scans in 1.0 s, so there is no catastrophic backtracking.
  - Three rows outside the rule's bound are reported, not graded; see S1 and S2.
  - Result: `PROBE PASS`, rc 0 (`receipts/probe_multidecl.log`).
- **The tree scan.** `python3 -I scripts/check_cpp_idiom.py` gives `multi-declarator declaration: 0 <= 0`, rc 0 (`receipts/check_cpp_idiom.py.log`).
- **The Python idiom bound.** The file is exactly 1000 lines and has no line over 120 columns. `python3 -I scripts/check_py_idiom.py` and `--selftest` (54/54) pass, rc 0.

## Findings

### S1 - SUGGESTION - Robustness, Tests - `scripts/check_cpp_idiom.py:269-271`: a line nesting braces four deep is not read at all

- **Evidence:** `int c[1][1][1][2] = {{{{1, 2}}}}, d = 0;` gives 0 at the head (`receipts/probe_multidecl.log`, out-of-bound rows). Dev's brace-blind pattern counted it, though it also miscounted the single-declarator four-deep line. The parent's C/C++ outside the submodules has no initialiser four braces deep (`git grep` gives 0), so nothing is hidden today.
- **Why only a suggestion:** the bound is stated in the comment at `:269`. It also meets F1's frozen required outcome, "at any nesting depth the gate claims to read, or at least one nested level".
- **Optional outcome:** either fail closed past the bound (count an unreadable line), or add one selftest arm that records the four-deep behaviour as intended.

### S2 - SUGGESTION - Robustness - `scripts/check_cpp_idiom.py:264-271`: a template argument comma in an `auto` initialiser is counted as a second declarator

- **Evidence:** `auto p = std::pair<int, int>{1, 2};` gives 1. This predates the PR: the dev and `e18c8225` patterns give 1 too, and the tree count is 0. It is outside the delta, and I record it for #495 only.

### S3 - SUGGESTION - Robustness - `MULTI_DECL_RE`: the scan cost is quadratic in line length

- **Evidence:** a 15 kB line takes 1.0 s and a 10 kB line 0.6 s (`receipts/probe_multidecl.log`). This is harmless for real source and only noted.

### R1 - RESIDUE - Docs - PR #893 body, line 119 (C++ idiom gate evidence row): "a one-level pattern the three-deep arm"

- **Problem:** the same sentence calls `e18c8225`'s flat pattern "the flat-brace pattern". "One-level" can therefore be read as that same flat pattern. The pattern that fails only the three-deep arm reads one nested level (two braces deep).
- **Exact fix:** "a one-level pattern the three-deep arm" -> "a pattern reading one nested level (two braces deep) the three-deep arm".
- This changes no measurement or verdict.

### Comment rule

- The added source lines are the comment at `:269` and the selftest labels at `:705-712`. They name only #495 and state behaviour.
- No lane label, lane name, review round, reviewer ID or issue-comment ID appears.
- The commit subjects cite #495 row and comment IDs. Commit text is not source, and the commit-shape rule (one line, no trailers) holds.

## Per-lens results (artifact evidence at this head)

```text
[R831] PASS Conformance - git diff --raw e18c8225..3c58b143 (2 blobs) and git ls-tree HEAD gitlinks (protocol-processor 801ef228, gptp-processor 1616fc8f, unchanged) - the delta changes no protocol behaviour, image, RTL, firmware or pin. #883 acceptance 2 ("each changed check gets its planted mutant") holds for the changed rule: the flat, brace-blind and one-nested patterns planted back each fail named arms (receipts/ratchet_arms_*). F1's frozen required outcome is met as worded. The rest of acceptance 1 to 5 keeps R831-1's coverage, because nothing it depends on changed.
[R831] PASS RTL - git diff --raw e18c8225..3c58b143 - no HDL, CDC, FSM or interface artifact in the delta. Not applicable; R831-1's RTL coverage at e18c8225 stands, since no path in RTL scope changed.
[R831] PASS Robustness - scripts/check_cpp_idiom.py:269-271 against the probe_multidecl_r831.py oracle (22/22 in-scope rows: nesting to three deep, both declarator orders, three declarators, empty groups, pointer declarators) and a 15 kB pathological line (1.0 s) - F1's boundary is closed. S1 to S3 are optional.
[R831] PASS Tests - scripts/check_cpp_idiom.py:705-712; --selftest 83/83 rc 0; the rule group 34/34 on the control; the flat pattern 3 FAIL, the brace-blind 3 FAIL and the one-nested 1 FAIL by name; R832-1's probe 9/9 equal to real>1; the tree scan 0 <= 0; check_py_idiom 0/0 and selftest 54/54 - each new arm fails for the defect it names.
[R831] PASS Docs - docs/testing/TESTING.md:357 against tb/verilator/milan_dp/crflic_mutants.py:91-116 and Makefile:665 (six gate mutants); PR body lines 44, 50, 85, 86 and 119 against the code (:269-271 and :705-712 line citations verified); docs_check.py 0 findings across 215 md files, rc 0; git diff --check 46c971fa..HEAD rc 0; comment rule; commit shape - R1 is RESIDUE and does not uncover the lens.
```

## Completion ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta raw diff (2 blobs); gitlinks; #883 acceptance 1-5 and the round 3 ruling; F1 required outcome; planted mutants | R831-2 | `3c58b143eac812d173b4326423c030b65ec63f9a` |
| RTL | CLEAN | the delta carries no RTL path; R831-1's RTL coverage, whose scope the delta does not touch | R831-2 (R831-1 for the RTL artifacts) | `3c58b143eac812d173b4326423c030b65ec63f9a` (RTL artifacts unchanged since `e18c822536ebeaf1cb0f42abea74513501aa26c7`) |
| Robustness | CLEAN (S1 to S3 optional) | `check_cpp_idiom.py:269-271`; oracle probe 22/22; timing probe | R831-2 | `3c58b143eac812d173b4326423c030b65ec63f9a` |
| Tests | CLEAN | `check_cpp_idiom.py:705-712`; selftest 83/83; rule group control and 3 mutants; prior probe 9/9; tree scan; Python idiom gate | R831-2 | `3c58b143eac812d173b4326423c030b65ec63f9a` |
| Docs | CLEAN (R1 RESIDUE) | `TESTING.md:357`; the PR body; docs_check; `git diff --check`; comment rule; commits | R831-2 | `3c58b143eac812d173b4326423c030b65ec63f9a` |

- Conformance, RTL and Docs for the artifacts outside this delta stay banked from R831-1 at `e18c8225`. That head is an ancestor of this one, and nothing in their scope changed except the two blobs reviewed here.

## Real limits

- **What I executed:** only the focused gates and probes above. I ran no parent, processor, gPTP, Yosys or builder bank, no Verilator suite, no Docker or act, and no hosted job.
- **Source-head execution evidence:** this is the author's published receipts, `review-evidence/883-r1/author-r3/receipts/gates-3c58b143` at `5e628298`.
  - I spot-checked them: `tree-after.txt` names head `3c58b143` and merge `736d5f59`.
  - The runner groups docs-check-no-git, docs-gates-0/1/2 and wire-accountability are rc 0, and unit-docs is rc 0.
  - gate_38 is the C++ idiom selftest at 83/83 and gate_37 the Python idiom selftest at 55/55. I did not re-run the whole docs group.
- **Hosted contexts at the exact head** (check-runs API, read once): 1 completed success (bdd-conformance). Every other context is queued (the docs, elaborate-gates, wire-accountability, changes and full-ci-gate jobs, plus 4 "Fail fast across this head"). None has executed, so there is no hosted proof yet.
- **Manager source bank:** none at this head, and I claim none.
- **Hardware:** physical calibration was NOT RUN, and field skips are not hardware proof.
- **Mutant full-selftest exit codes:** the `--selftest` runs in git-less copies exit non-zero partly because of the live-tree crash; see F1 verification. The `ratchet_arms_*` receipts are the clean evidence.

## Pending manager duties

- Validate the current-dev merge candidate (source base `46c971fa`, live dev `fa6c094b`) through the builder and native banks, and link the receipts on the PR.
- Own hosted and act acceptance at this head. The act run is due again under the ruling, and the hosted contexts were still queued.
- Carry RESIDUE R1 (this round) and R832-1 R2 (`pp_resource_baseline.json:451`) to the residue checklist. Items 1 and 4 of #495 row 6731336971 stay open there.
- S1 to S3 and R831-1 S1 to S3 are optional, for #495 or a follow-up.
- Merge still requires the external reviewer's positive verdict at this head and explicit maintainer authorisation.

## Clone restoration

- After the probes: `git status --porcelain --ignored` is empty, the worktree and index are clean, and `git write-tree` equals `df75ea45`.
- `scripts/check_cpp_idiom.py` is blob `4de2cf2d` and `docs/testing/TESTING.md` is blob `05e39eb3`, both mode 100644 in the index and 644 on disk.
- The gitlinks match HEAD: external `efeb541a`, gptp-processor `1616fc8f`, protocol-processor `801ef228`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`.
- My runs created a `scripts/__pycache__` (ignored, all timestamps after this session began), and I removed it.
- Every probe tree is under `scratch/`, which is not published.

## Receipts

Every published file is listed in `MANIFEST.sha256`. The scripts are `probe_multidecl_r831.py`, `plant_decl_text_r831.py` and `ratchet_arms_r831.py`; run them with `python3 -I`. Raw logs and rc files are under `receipts/`, the earlier external probe and its run at this head under `receipts/prior_probe/`, and the PR body snapshot is `receipts/pr893_body_at_3c58b143.txt`. Host scratch paths in the mutant logs are replaced by `<packet>`.

R831-2 FINISHED

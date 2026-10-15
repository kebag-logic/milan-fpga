[R636] POSITIVE - exact head 30f7b0ef9d7ab073dccd9bda1130a630aef633b1

Internal cleared-context re-review R636-8, issue #737 / PR #739. This is a delta review of `fe2e2a54..30f7b0ef`, one commit by the coordinating role. The exact tree is `8a4e88e6b8f94dd1c603eb4c6d4f8ddedd01dccb`.

All five lenses were applied to the delta and are CLEAN at this head. All four assigned checks hold:

1. The delta is exactly one added `.gitattributes` line.
2. `git diff --check` against dev `65617779` now returns 0. At `fe2e2a54` it was nonzero only because of `ci/act/fail-fast.patch`.
3. Today the exemption matches only that file, and it hides only unified-diff context markers.
4. The patch bytes are unchanged, and the patch still applies cleanly to the pinned act source.

There is no BLOCKER, MAJOR or MINOR finding. There are two new RESIDUE items and one SUGGESTION. Prior findings are resolved or retained as tabulated below.

## Contents

- Context reconstructed
- Check 1: the delta
- Check 2: `git diff --check` at both heads
- Check 3: scope of the exemption
- Check 4: patch bytes and the act build
- Findings
- Lens results
- Prior findings at this head
- Reviewer-owned ledger
- Real limits and pending manager duties

## Context reconstructed

- I read AGENTS.md section 6 and section 7 again, and CONTRIBUTING.md, in this clone.
- The round-8 assignment is issue #737 comment [6192211250](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6192211250) ([A10], 12:37:24Z). A copy is in `receipts/issue737-round8-assignment.md`. Under the round-8 decision, the coordinating role makes this one-line change. The finding behind it is a merge-bar failure: on candidate `23869591` (dev `65617779` + `fe2e2a54`), `git diff --check 65617779 23869591` reported 37 whitespace findings, all in `ci/act/fail-fast.patch`.
- The live PR head is `30f7b0ef9d7ab073dccd9bda1130a630aef633b1`, with base `dev` and recorded base oid `f6260253` (`receipts/pr739-body.md`, sha256 `0c1c7937...3991`).
- The merge bar is the place `git diff --check` runs. `scripts/xvlog_gate.py:1149` records this. No hosted workflow step runs `git diff --check`; a search of `.github`, `ci` and `scripts` finds none.
- I read the prior public findings (R636-7, [6191436051](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6191436051)) only after Checks 1 to 4 were complete.

## Check 1: the delta

Receipt: `receipts/01-delta.txt`.

- `30f7b0ef` has the single parent `fe2e2a543474dd9a932383052bb6fe14bfbbb1fe`.
- `git diff --raw` gives `:100644 100644 187cad540 137263407 M .gitattributes`, and nothing else.
- The diff is one added line, `ci/act/*.patch -whitespace`, after the existing `sw/litex/patches/*.patch -whitespace`.
- The commit message is one line with no trailers, as CONTRIBUTING requires.
- No path under `scripts`, `ci`, `.github`, `docs` or `sw` changes. No gitlink changes (`receipts/10-integrity.txt`).

## Check 2: `git diff --check` at both heads

Receipts: `receipts/02-diff-check-attr-source.txt`, `receipts/03-scope.txt`, `receipts/05-hygiene-and-base.txt`, `receipts/script-run/p2-diff-check-rc.txt`.

I judged each head with its own attributes (`git --attr-source=<head>`), so the checkout's `.gitattributes` could not mask the parent's result.

| Head | Base `65617779` (live dev) | Base `fa7347fc` (source base) | Base `f6260253` (merge base) |
|---|---|---|---|
| `fe2e2a54` | exit 2, 37 findings, all `ci/act/fail-fast.patch` | exit 2, same 37 | exit 2, same 37 |
| `30f7b0ef` | **exit 0** | **exit 0** | **exit 0** |

- **Control.** I applied the parent's attributes to the new head's content: exit 2, with the same 37 lines. So the added line, not a content change, is what clears the check.
- **Isolation.** I ran the parent with its own attributes and excluded `ci/act/fail-fast.patch` from the pathspec: exit 0. So at `fe2e2a54` the patch was the only failing path, as the assignment states.
- **Plain form.** In the clean exact-head checkout, `git diff --check 65617779 30f7b0ef` also returns 0.
- **Exit status.** For `--check` failures git uses exit status 2, not 1. The assignment says "rc 1". Either value is a failure, so this changes no conclusion; see the limits section.
- **Other claims.** The assignment says `check_hygiene.py` and `check_todo_ownership.py` pass. I reproduced both at this head: `HYGIENE RATCHET: PASS (3 population(s), 1199 file(s))`, rc 0; and `TODO ownership gate: OK`, rc 0.

## Check 3: scope of the exemption

Receipts: `receipts/03-scope.txt`, `receipts/06-glob-scope.txt`, `receipts/08b-flagged-line-markers.txt`, `receipts/08-patch-whitespace-anatomy.txt`.

- **Tracked paths.** I compared `check-attr whitespace` over all 1,376 tracked paths under the parent's attributes and under the head's. Exactly one path changes, `ci/act/fail-fast.patch`, from `unspecified` to `unset`. Every other tracked path keeps its attribute.
- **Other files.** At head the only tracked `ci/act/*.patch` is `fail-fast.patch`. The other six files in `ci/act/` are `.go` sources, and they stay `unspecified`. The only `.gitattributes` in the tree is the top-level one. No repo config sets `core.whitespace`, `apply.whitespace` or `core.attributesfile`, and there is no `info/attributes`.
- **Glob semantics** (hypothetical paths, `core.ignorecase=false`):
  - `ci/act/new.patch` and `ci/act/.patch` are exempt.
  - These are not exempt: `ci/act/sub/x.patch`, `ci/act/x.diff`, `ci/act/x.patch.go`, `ci/act/fail-fast.go`, `ci/x.patch`, `ci/act.patch`, `x/ci/act/y.patch`, `CI/act/y.patch` and `ci/act/y.PATCH`.
  - So the pattern is anchored to `ci/act/`, does not recurse, and is case-sensitive.
- **What it hides.** I classified each of the 37 flagged lines by the first byte of its line in the patch. All 37 start with the unified-diff context marker, a space:
  - 8 are empty context lines (`trailing whitespace`).
  - 29 are tab-indented context lines (`space before tab in indent`).
- **Payload.** No `+` or `-` payload line and no context payload in the patch carries trailing whitespace or a space before a tab. The file has no CR byte.
- **Conclusion.** Today the exemption hides only patch syntax. It cannot hide whitespace in any other current path. The one forward-looking gap is recorded as R636-8-S1.

## Check 4: patch bytes and the act build

Receipts: `receipts/04-patch-bytes.txt`, `receipts/09-patch-dry-run.txt`, `receipts/script-run/p6-patch-sha.txt`, `receipts/script-run/p7-dry-run.txt`.

- **Unchanged bytes.** `ci/act/fail-fast.patch` is blob `197702fa1678e9d3d69a7de0d931c019b70aa3c8` with mode 100644 at both `fe2e2a54` and `30f7b0ef`. Its sha256 is `7182699a726258e068992a9cb14237f27487c0b633d643ff8305c80fe289edb4` in the git blob at both heads and in the checked-out file.
- **No conversion.** `whitespace` is not a checkout-conversion attribute. `check-attr -a` reports only `whitespace: unset` for the file, with no `text`, `eol` or `filter`. So the working-tree bytes the build hashes are unchanged.
- **The build ignores git attributes.** `scripts/build_ci_act.py:66` and `:80` apply the patch with GNU `patch --batch --fuzz=0 -p1`, not `git apply`. The delta does not touch the build recipe. The `patch_sha256` that the recipe binds is therefore unchanged.
- **Falsification probe.** I downloaded the pinned source `nektos/act@4f411281`. Its archive sha256 is `0d151c0a...ae98`, equal to `ACT_SHA256` at `scripts/build_ci_act.py:26`. With GNU patch 2.8, `patch --dry-run --batch --fuzz=0 -p1` of the head blob checks `pkg/common/executor.go`, `pkg/runner/runner.go` and `pkg/runner/run_context.go`, and returns 0. A real apply also returns 0, with no `.rej` file. I did not compile anything, and I did not run act or Docker.
- **Published receipts.** The published `review-evidence/737-r1/author*/dispatcher-build-receipt.json` files at `c3d4b118` carry an older patch digest (`88a5b2c9...`, version `0.2.89+milan-ci3`). They predate the later patch revisions (`c3ab1b2b`..`e3a92e58`), so they are not evidence for the current bytes. I rely on the byte identity and the probe above, not on those receipts.

## Findings

### R636-8-R1 - RESIDUE - Docs - PR #739 body, Status l.22 and Contents l.15-18

**Evidence.** The live head is `30f7b0ef`. The Status section still opens "Round 7 is complete at `fe2e2a54` ...". The body has no Round 8 entry, and it never mentions the `.gitattributes` change. Round 8 is recorded only in issue comment 6192211250. A cold reader of the PR cannot tell from the body why the head moved. This is wording only: no measurement, figure, test or verdict depends on it.

**Exact fix.**

- In Contents, after `- [Round 7](#round-7)`, add `- [Round 8](#round-8)`.
- In Status, add before l.22: "Round 8 is complete at `30f7b0ef`, from `fe2e2a54`. The coordinating role added `ci/act/*.patch -whitespace` to `.gitattributes`, so `git diff --check` no longer reports the unified-diff context markers of the vendored `ci/act/fail-fast.patch`. No other file changed, and the patch bytes are unchanged."
- Append a section:

  > "## Round 8
  >
  > One line from `fe2e2a54` to `30f7b0ef`, under the round-8 decision (#737 comment 6192211250): `.gitattributes` gains `ci/act/*.patch -whitespace`. `git diff --check 65617779 30f7b0ef` returns 0; at `fe2e2a54` it reported 37 findings, all context markers in `ci/act/fail-fast.patch`."

**Verification.** Read the live PR body against the PR head.

### R636-8-R2 - RESIDUE - Docs - issue #737 comment 6192211250, finding bullet: "The round-5 candidate (`5687e34c`) failed the same gate, and no review caught it."

**Evidence.** R637-3 ([6180643633](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6180643633), l.57) did see this output. It recorded that "the full-range check reports whitespace only inside unchanged unified-diff context in `ci/act/fail-fast.patch`", and judged it patch syntax rather than a defect. Nobody raised it as a finding. This changes only the account of the review history, not any measurement or verdict.

**Exact fix.** Replace "and no review caught it" with "and no review raised it as a finding: R637-3 (6180643633) saw the full-range report and judged it patch syntax". Make the change in the manager's next status note or in the residue checklist. The original comment does not need an edit.

**Verification.** Read R637-3 l.57.

### R636-8-S1 - SUGGESTION - Robustness, Tests - `.gitattributes:2`

**Evidence.** The glob exempts every present and future top-level `ci/act/*.patch` (Check 3 probe: `ci/act/new.patch` is `unset`). The exemption covers whole files, so `git diff --check` would also miss whitespace that a later edit adds inside the patch's `+` payload, which is Go source compiled into the dispatcher. Today the gap is empty: there is one matching file, and its payload has 0 such defects. The pattern also mirrors the existing `sw/litex/patches/*.patch` precedent. So this is optional.

**Suggested outcome.** Either name the file exactly (`ci/act/fail-fast.patch -whitespace`), or keep the glob and accept that payload whitespace in vendored patches is left to the act build's own controls.

**Verification.** `git check-attr whitespace ci/act/new.patch` reports `unspecified` with the narrow form, and `git diff --check 65617779 HEAD` still returns 0.

## Lens results

[R636] PASS Conformance - `.gitattributes:2`; `receipts/02-diff-check-attr-source.txt`; `receipts/script-run/p2-diff-check-rc.txt`; round-8 assignment 6192211250 - The merge-bar check `git diff --check` returns 0 against dev `65617779`, source base `fa7347fc` and merge base `f6260253`. With the parent's attributes it is nonzero, and the 37 findings are all in the patch. The change does exactly what the round-8 decision states, and no other file changes. Issue acceptance does not depend on any other artifact in the delta.

[R636] PASS RTL - `receipts/01-delta.txt`; `receipts/10-integrity.txt` - Inapplicable. The delta contains no HDL, constraint, gitlink, workflow template or generated workflow. All six gitlinks are identical at both heads. The dispatcher source the RTL lens previously examined (`ci/act/*`, `scripts/build_ci_act.py`) is byte-unchanged.

[R636] PASS Robustness - `.gitattributes:2`; `receipts/06-glob-scope.txt`; `receipts/08b-flagged-line-markers.txt`; `receipts/09-patch-dry-run.txt` - The exemption changes one tracked path's attribute. It is anchored, non-recursive and case-sensitive. It hides only context markers, 37 of 37. The patch still applies with `--fuzz=0` to the pinned source, whose sha256 I verified. The forward-looking scope is S1, which is optional.

[R636] PASS Tests - `receipts/02-diff-check-attr-source.txt` (control row); `receipts/05-hygiene-and-base.txt` - No test or self-test changed. The executable check for this delta is `git diff --check` itself. Its control, the parent's attributes on the new content, fails with exit 2, and its pristine run at head passes with exit 0, so the check discriminates. `check_hygiene.py --check` and `check_todo_ownership.py` pass at head. The prior Tests coverage at `fe2e2a54` depends on no file the delta touches.

[R636] PASS Docs - `.gitattributes`; `docs/` search for `-whitespace` and `.gitattributes`; `receipts/pr739-body.md` l.15-29 - No authoritative document describes the `.gitattributes` exemptions; the litex precedent is undocumented too. So no contract text is stale. The PR body has no round-8 record (R636-8-R1, RESIDUE), and the manager's issue note slightly misstates the review history (R636-8-R2, RESIDUE). Both are wording only.

## Prior findings at this head

| Finding | Status at `30f7b0ef` | Evidence |
|---|---|---|
| R636-7-R1 (RESIDUE: PR body l.29, "The author does not push.") | **Retained** | Still present at live body l.29 |
| R636-7-R2 (RESIDUE: `docs/testing/CI_WORKFLOWS.md:1766` is 101 characters) | **Retained** | Still 101 characters; `docs/` is not in the delta |
| R636-7-S1 (planted arm lacks a direct "recorded" assertion) | **Retained** | `scripts/act_ci_small_host_selftest.py` is not in the delta |
| R636-7-S2 (small-host control not run by any workflow) | **Retained** | No workflow is in the delta |
| R636-6-F1 (BLOCKER: runner self-test on fewer than 64 CPUs) | **Remains resolved** | `scripts/act_ci.py` is not in the delta |
| R636-5-S2, R636-4-S1, R636-4-S2, R636-4-S3, R636-1-S4 | **Retained** | Their artifacts (`scripts/ci_suite_workflows.py`, `ci_builder_legs.py`, `ci_gate_receipts.py`, `sw/builder/test_builder.py`, `scripts/run_all_suites.sh`) are not in the delta |
| R637-6 and every finding listed as resolved before | **Remain resolved** | The delta touches none of their artifacts |

## Reviewer-owned ledger

Coverage for artifacts the delta does not touch rests on R636-7 at `fe2e2a54`. That commit is the parent of `30f7b0ef`, and nothing in those lenses' scope has changed since, apart from the one `.gitattributes` line that this round covers.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `.gitattributes`; `git diff --check` at both heads against `65617779`, `fa7347fc` and `f6260253`; round-8 decision 6192211250 | R636-8 (delta); R636-7 (rest) | `30f7b0ef9d7ab073dccd9bda1130a630aef633b1`; `fe2e2a543474dd9a932383052bb6fe14bfbbb1fe` (ancestor, untouched since) |
| RTL | CLEAN (inapplicable to the delta) | Delta raw list; six gitlinks; `ci/act/*` and `scripts/build_ci_act.py` byte identity | R636-8 (delta); R636-7 (rest) | `30f7b0ef9d7ab073dccd9bda1130a630aef633b1`; `fe2e2a54...` |
| Robustness | CLEAN (S1 optional) | `check-attr` over 1,376 paths; glob probes; marker classification of all 37 lines; `--fuzz=0` dry run against pinned act | R636-8 | `30f7b0ef9d7ab073dccd9bda1130a630aef633b1` |
| Tests | CLEAN (S1 optional) | `git diff --check` control and pristine runs; `check_hygiene.py --check`; `check_todo_ownership.py` | R636-8 (delta); R636-7 (rest) | `30f7b0ef9d7ab073dccd9bda1130a630aef633b1`; `fe2e2a54...` |
| Docs | CLEAN (R1, R2 RESIDUE) | `docs/` search; live PR #739 body; issue #737 comment 6192211250; R637-3 l.57 | R636-8 | `30f7b0ef9d7ab073dccd9bda1130a630aef633b1` |

## Real limits and pending manager duties

**What I ran.** I ran read-only git probes in the review clone: `diff --check` with `--attr-source`, `check-attr`, and blob reads. I ran `check_hygiene.py --check` and `check_todo_ownership.py` at head. I also ran one GNU `patch` dry run and apply of the head blob, in a disposable extraction of the pinned act source under `scratch/`.

**What I did not run.** I did not run act or Docker. I did not run `act_ci.py` or its self-test, any dispatcher compile, or any parent, PP, gPTP, Yosys, builder or Verilator bank. A one-line attribute delta does not call for any of these.

**Exit status.** The assignment says the check was "rc 1" at `fe2e2a54`. Git 2.56.0 exits with 2 for `--check` failures. The failure is real, and only the number differs.

**Hosted state.** At my snapshot (12:40:15Z), runs 38736064617 (rtl-full), 38736064477 (elaborate), 38736064462 (docs) and 38736064304 (rtl-fast) for this head were queued, pending or in progress. Only `docs-check-no-git` had completed, with success (`receipts/07-hosted-*`). No hosted job runs `git diff --check`. I claim no workflow verdict, duration or 30-minute readback.

**Not claimed.** Physical calibration is NOT RUN, and field skips are not hardware proof. No manager source bank exists at this head, and none is inferred. Source-head execution evidence is the author's published gate receipts. The final current-dev candidate is distinct from this source head.

**Pending manager duties.**

1. Rebuild the current-dev merge candidate (dev `65617779` + `30f7b0ef`; source base `fa7347fc59173f90e4feec2df207692e6e6e72ec`). Confirm `git diff --check 65617779 <candidate>` returns 0 there, run the builder and native banks, and link the receipts.
2. Run the act replay on the repinned runner (`7ff18c6a...46fd`), and read back the exact-head hosted runs listed above.
3. Carry R636-8-R1, R636-8-R2, R636-7-R1 and R636-7-R2 to the residue checklist.

**Clone integrity.** The review clone is at `30f7b0ef9d7ab073dccd9bda1130a630aef633b1`, tree `8a4e88e6b8f94dd1c603eb4c6d4f8ddedd01dccb`. It has 0 status entries, including ignored files; I removed the `scripts/__pycache__/` that the hygiene run created, and none of it was tracked. The index has 1,376 entries, and its written tree equals the head tree. The index and worktree have no differences, and all six gitlinks are unchanged (`receipts/10-integrity.txt`).

**Portable script.** `scripts/r636_8_probes.sh <clone> <scratch> <receipts>` reproduces Checks 1 to 4. Its output from my run is in `receipts/script-run/`.

R636-8 FINISHED

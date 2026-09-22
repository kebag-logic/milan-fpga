https://github.com/kebag-logic/milan-fpga/issues/423#issuecomment-5777123829
[R242] DESIGN READY — trusted head 88e9276b2a220c716f64a843f7e1eb8f9265e896; exact public scope: kebag-logic/milan-fpga#423 (body; comments 5771938635, 5772003744, 5776564663), readiness-evidence/423 at 6181e900cd9f7ae618e1603e2ea867a5bb4d41a6, Mister-M-alt/FPGA-gPTP PR62 history (head 3db86812096830fada2f5f276fa5f4d9f37d1d14; targets f0f1c055ee5226f08e656c27cb1bf4c355be11ae and live main c1b617435824929a790739ea8585c3fe1a328cc0). Readiness/design review only: not a POSITIVE merge verdict, no code approval, no containment waiver, no processor-pin adoption, no lens coverage banked for any implementation head.

## 0. Outcome

- **Proposed criterion: RMR-1** (one redundant-merge replay, retained at the tip) = **G1 ∧ H ∧ T** (§3). It meets #423 AC1–AC3 with executable fixtures: 31/31 outcomes as expected, 10/10 guard mutations killed, 145/145 unchanged self-test arms still pass on a scratch prototype.
- **Actual public PR62 history does NOT pass.** At both targets: G1 yes, H yes, T no. The prototype reports an explicit `UNKNOWN` (rc 1) that names the replay evidence and the two unretained paths. The unchanged checker reports `STRANDED` (rc 1). This is a deliberate conservative false negative (§6).
- **The published structural shortcut (G1 ∧ H without T) is unsafe.** Removing T makes 11 fixtures `contained`, among them exact reverts, a partial revert and a reversion by edit (§5, mutation log).
- **One policy decision remains (D1, §6), and it does not block the criterion:** keep AC3 as written, which leaves PR62 explicitly unresolved and is recommended, or amend it to historical semantics.

## 1. Sources, integrity, method

- Read: #423 body and the three A10 comments listed above; the assignment comment 5776564663; CONTRIBUTING.md:178-246 (§2.1 step 7); AGENTS.md:91-116 (§4) and :191-358 (§6); REQUIREMENTS.md:213-234 (§8, REQ-VER-04 :222-224); scripts/check_merge_containment.py (blob 9da08386de180a2b74e7ed13412625b485562540) and its self-test modules; the public donor repository via a scratch mirror clone; PR62 API metadata.
- Not read: comments 5776812551 (`[R241]`) and 5776812920 (`[A10]`, posted 2 s later), both posted after the assignment (rawlogs/issue-423-comment-identities-final.tsv lists identities only). I also read no private manager, author or other-reviewer material.
- Published evidence: all 8 blobs under readiness-evidence/423 re-hash to their Git ids at 6181e900. All 6 MANIFEST.json rows match, with original equal to published and no redaction. README.md and MANIFEST.json are covered only by blob ids (rawlogs/verify-published-manifest.log). The published probe, re-run unchanged against the trusted checker, reproduces both published verdicts and both helper results (rawlogs/published-probe-trusted.json).
- Checkout integrity: HEAD, index, the 855 tracked entries (mode, blob, kind), status and refs are identical before and after (§13). Every Python run used `-B`. No file under the checkout was written.
- Tools: git 2.55.0, Python 3.14.7. The fixtures fix identities and dates, so every object id reproduces: two independent builds gave identical OIDs, exits and verdict lines (rawlogs/fixture-determinism.log).

## 2. Reconstructed public history (AC1)

| role | original | on donor main | parents (original → replay) | tree |
|---|---|---|---|---|
| PR61 commit | 9790ac7 | 20927af | 7fa64e9 → 7fa64e9 | cf1818d9 |
| PR61 redundant no-ff merge | f27b455 | 377b8c4 | [7fa64e9, 9790ac7] → [7fa64e9, 20927af] | cf1818d9 |
| PR62 commit (PR head) | 3db8681 | 5602e70 | f27b455 → 377b8c4 | df933eb8 |
| PR62 merge | f5ba2db6 (API merge_commit_sha; object absent from every public ref) | 676d2f6 = no-ff merge of 5602e70 into 377b8c4 | — | df933eb8 |

- PR62 (API): base `main`@f27b455 and head 3db8681, one commit, merged 2026-09-03T06:49:47Z. The live branch `arms-use-dut-cycles-not-host-time` is still at 3db8681, and first-parent continuity holds in the mirror. The issue's own sweep reached `contained()`. I did not re-query the timeline events.
- Donor main is a **tree-identical, parent-isomorphic replay** of the original chain. For each original commit there is exactly one counterpart on main with the same tree whose parents map to the original's parents. The patches are byte-identical. The issue's SHA-256 values (fa20a251…, d3d164b3…) reproduce exactly with `git diff --no-ext-diff --no-textconv --no-renames <parent> <commit>`. The verbatim patch-ids are equal (922d71f2…, f21aa8a0…). Source: rawlogs/pr62-reconstruction.{log,json}.
- The branch range at both targets is {9790ac7, f27b455, 3db8681}, with the single merge base 7fa64e9. f27b455 has exactly two parents; its second parent's only parent is its first parent, and its tree equals its second parent's tree.
- Net touched paths (7fa64e9..3db8681) and their retention at **both** targets:

| path | tip vs head | re-merge no-op | later editor |
|---|---|---|---|
| tb/mutation_verdict.py | identical | — | none |
| tb/tsngen/Makefile | differs | yes (CFLAGS edit clear of the PR61 hunks) | 0ac3e2c |
| tb/verilator/gaskets/Makefile | differs | yes | 0ac3e2c |
| tb/tsngen/mutants.py (added by PR61) | differs | **no (conflict)** | 0ac3e2c |
| tb/verilator/gaskets/mutants.py (added by PR61) | differs | **no (conflict)** | 0ac3e2c |

  0ac3e2c ("Rule 11/12: clear the debt donor main brought") is an ancestor of both targets. It replaces PR-introduced lines in the two added files (for example `def stage(work, tag, mutate=None):` becomes a typed signature with a longer docstring).
- Reproductions of the same failure: the unchanged checker gives `STRANDED 3` at both targets, and its output lines equal the published baseline logs. The offline fixtures 1 and 6 (§5) and the published probe reproduce the same `STRANDED 3 commit(s)` with the unchanged checker.

## 3. Criterion RMR-1 (AC2)

RMR-1 is a new final arm in `contained()`. It is evaluated only where the unchanged arms would return STRANDED: after `_patch_id_verdict` and before the final return (check_merge_containment.py:567-585).

- **G1, shape (exact):** `rev-list --min-parents=2 base..branch` yields **exactly one** commit M. M has exactly two parents (P1, P2). P2 has exactly one parent, and that parent is P1. `tree(M) = tree(P2)`.
- **H, historical replay (existing helper, unchanged):** `_linear_patches_contained(branch, base)` (check_merge_containment.py:194-231) holds. Every non-merge commit of base..branch then has a distinct whitespace-exact (`patch-id --verbatim`) equivalent in branch..base with an identical touched-path postimage.
- **T, retention at the current base tip:** `merge-base --all base branch` is exactly one commit B. Each path p in the raw `diff --no-renames B branch` is retained when one of these holds:
  - the tip entry equals the branch entry (mode, type and oid, absence included); or
  - all three entries are absent or regular blobs; the tip keeps the branch's mode (tip mode = branch mode, or branch mode = B mode); and `git merge-file -p` over the raw blobs (tip, B, branch) exits 0 with output byte-identical to the tip blob.

  Any other result means p is not retained. A merge-file error, such as a binary file, makes T unmeasurable.
- **Verdicts:**

| G1 | H | T | verdict |
|---|---|---|---|
| holds | holds | holds | `contained`, rc 0 |
| holds | holds | fails | `UNKNOWN`, rc 1 ("replayed exactly in <base> history; retention at <base> not proven: <paths>") |
| holds | holds | unmeasurable | `UNKNOWN`, rc 1 |
| fails | any | any | unchanged `STRANDED`, rc 1 |
| any | fails | any | unchanged `STRANDED`, rc 1 |
- **Separation:** *historical replay equivalence* is G1 ∧ H, which is what the published shortcut computes. RMR-1 reports it but never accepts it alone. *Retention at the current target tip* is T, and rc 0 requires T. RMR-1 does not change the existing linear arm.
- Scratch prototype: scripts/candidate_arm.py, inserted by scripts/make_prototype.py into copies under prototype/. The diff is rawlogs/prototype.diff (200 lines). The prototype is design evidence, not an implementation proposal.

## 4. Safety argument (conclusions)

1. **Monotone.** RMR-1 can change only a STRANDED verdict. It turns STRANDED into `contained` only when G1 ∧ H ∧ T all hold; otherwise it turns STRANDED into `UNKNOWN`, which is still rc 1. No existing `contained` or `UNKNOWN` verdict changes. The rc 0/1/2/3 contract (check_merge_containment.py:73-77) is unchanged, and all 145 unchanged self-test arms pass on the prototype.
2. **G1 makes the merge content-free.** `diff(P2, M)` is empty and `diff(P1, M) = diff(P1, P2)`. P1 lies on P2's line, so the branch's tree sequence equals the linear history with M removed, and `--no-merges base..branch` is exactly that history. H is therefore the existing linear proof on an equivalent linear history, not a new equivalence notion. The reason merges are excluded today (patch IDs omit resolution content, :490-497) does not apply, because G1 proves the merge adds no resolution content. G1 refuses:
   - one byte of resolution work (fixture 23);
   - octopus merges (fixtures 24 and 25);
   - an unrelated or other-line parent (fixtures 26 and 29);
   - a first parent two commits back (fixture 28);
   - a second merge (fixtures 3 and 27).
3. With one merge of this shape the branch has a single entry point into base history, so the merge base is unique. T still checks this and fails closed.
4. **T.** A clean raw three-way merge whose result is the tip means that re-merging the branch now would change nothing. Every region the branch changed relative to B is byte-identical at the tip: a region the tip left at B's content would be re-applied and change the result, and a region the tip changed differently conflicts. So T fails for every later reversion, and those cases fall to `UNKNOWN`:
   - exact revert of either commit (fixtures 12 and 13);
   - manual one-hunk restore (fixture 14);
   - revert combined with an unrelated extension (fixture 15);
   - revert under an `ours` merge driver and a silent textconv (fixture 16);
   - rewrite of a PR-introduced line to disable it (fixture 7);
   - exec-bit reversion (fixture 10);
   - deletion of a touched file (fixture 9).

   Whitespace differences are content: fixture 19 fails H first, and T would also fail.
5. **Configuration-independent.** T reads raw blobs with `ls-tree` and `cat-file blob` and merges them with `merge-file`. `merge-file` reads no attributes, merge drivers, textconv or rename settings. `_git` keeps `--no-replace-objects`, and the existing graft refusal still applies. Symlinks and gitlinks are compared only by identity. A binary edit makes T unmeasurable, which gives `UNKNOWN` (fixture 11).

## 5. Positive and negative counterexamples, with actual exits (AC3)

Unchanged = trusted checker CLI. Candidate = prototype CLI (`--no-fetch --base main pr`). Source: rawlogs/fixture-matrix.{log,json}, built by scripts/fixtures.py.

| # | fixture | class | unchanged rc / verdict | candidate rc / verdict | G1 H T |
|---|---|---|---|---|---|
| 1 | `positive-replay-far-extension` | positive | 1 STRANDED | 0 contained | Y Y Y |
| 2 | `positive-replay-two-later-commits` | positive | 1 STRANDED | 0 contained | Y Y Y |
| 3 | `two-redundant-merges` | conservative FN (one-merge cap; per-merge variant would accept) | 1 STRANDED | 1 STRANDED | N Y Y |
| 4 | `control-replay-no-later-edit` | control: existing path arm | 0 contained | 0 contained | Y Y Y |
| 5 | `control-revert-then-reapply` | control: existing path arm | 0 contained | 0 contained | Y Y Y |
| 6 | `pr62-faithful-later-rewrite` | conservative FN (mirrors actual PR62) | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 7 | `later-disabling-rewrite` | negative: reversion by edit (twin of 6) | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 8 | `published-shape-adjacent-extension` | conservative FN (legit extension adjacent to a replayed hunk) | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 9 | `later-deletion-of-touched-file` | refused: later deletion removes replayed work | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 10 | `later-exec-bit-loss` | refused: later exec-bit reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 11 | `later-binary-edit` | explicitly unresolved: binary later edit unmeasurable | 1 STRANDED | 1 UNKNOWN | Y Y ? |
| 12 | `exact-revert-whole-replay` | negative: later reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 13 | `exact-revert-pr-commit` | negative: later reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 14 | `partial-revert-one-hunk` | negative: later reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 15 | `revert-plus-far-extension` | negative: later reversion | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 16 | `revert-under-hostile-merge-config` | negative: reversion + ours driver/textconv | 1 STRANDED | 1 UNKNOWN | Y Y N |
| 17 | `omitted-linear-commit` | negative: omitted linear work | 1 STRANDED | 1 STRANDED | Y N N |
| 18 | `omitted-part-of-a-commit` | negative: omitted linear work | 1 STRANDED | 1 STRANDED | Y N N |
| 19 | `whitespace-different-postimage` | negative: whitespace | 1 STRANDED | 1 STRANDED | Y N N |
| 20 | `repeated-block-other-location` | negative: hunk position | 1 STRANDED | 1 STRANDED | Y N N |
| 21 | `merge-resolution-work-missing` | negative: resolution work | 1 STRANDED | 1 STRANDED | N Y N |
| 22 | `merge-resolution-work-present` | conservative FN (AC2 "unless") | 1 STRANDED | 1 STRANDED | N Y Y |
| 23 | `merge-one-byte-evil-change` | negative: resolution work | 1 STRANDED | 1 STRANDED | N N N |
| 24 | `octopus-merge` | negative: octopus | 1 STRANDED | 1 STRANDED | N Y Y |
| 25 | `octopus-absorbed-third-parent` | conservative FN (scope: two parents only) | 1 STRANDED | 1 STRANDED | N Y Y |
| 26 | `unrelated-parent-merge` | negative: unrelated parent | 1 STRANDED | 1 STRANDED | N Y Y |
| 27 | `redundant-plus-nonredundant-merge` | negative: multiple merges | 1 STRANDED | 1 STRANDED | N Y Y |
| 28 | `first-parent-is-grandparent` | conservative FN (distance 2) | 1 STRANDED | 1 STRANDED | N Y Y |
| 29 | `reversed-parent-order` | negative: shape | 1 STRANDED | 1 STRANDED | N Y Y |
| 30 | `linear-control-exact-revert` | pre-existing linear historical arm (unchanged) | 0 contained | 0 contained | N Y N |
| 31 | `linear-control-adjacent-extension` | pre-existing linear historical arm (unchanged) | 0 contained | 0 contained | N Y N |

- **Guard mutations** (rawlogs/mutations.log; all 10 killed). Each row names the fixture or fixtures whose verdict changes when that guard is weakened.

| weakened guard | fixtures that change |
|---|---|
| any number of merges | 3 |
| any parent count | 25 |
| drop the P1-is-parent-of-P2 check | 28 |
| drop the tree-equality check | 21 (STRANDED → UNKNOWN), 22 (STRANDED → contained) |
| skip H | 17–20 |
| **skip T (the published shortcut)** | 6–16, every one to `contained` |
| exact tip equality instead of T | 1 and 2 (contained → UNKNOWN) |
| ignore modes | 10 |
| clean merge without the tip comparison | 14 |
| count merge errors as retained | 11 |
- The published probe on the prototype gives `UNKNOWN` for both published cases (rawlogs/published-probe-prototype.json). Its "later extension" is adjacent to the replayed line, which is conservative false negative 8.

## 6. Actual PR62, the remaining decision, and a pre-existing asymmetry

- **Actual history under RMR-1:** `UNKNOWN`, rc 1, at f0f1c055 and at c1b61743. The note names tb/tsngen/mutants.py and tb/verilator/gaskets/mutants.py. Neither the unchanged checker (STRANDED) nor RMR-1 accepts it; only the rejected shortcut would.
- **Why a fail-closed rule cannot accept it while AC3 stands:** 0ac3e2c replaces PR-introduced lines. Fixture 6 (a signature annotation) and fixture 7 (a disabling rewrite) belong to the same observable class: a later commit replaces PR-introduced lines. The shortcut accepts both, and it also accepts exact reverts (fixtures 12 and 13). A rule that accepts actual PR62 at either target must therefore accept fixture 7 as well, or judge intent.
- **D1 (for A10 or the maintainer; not a blocker for RMR-1).** Choose one:
  - **(a) Keep AC3 as written (recommended).** Implement RMR-1. The donor sweep for PR62 stays rc 1, now an evidence-bearing `UNKNOWN`, until PR62 is disposed of separately.
  - **(b) Amend AC3 to historical semantics for this shape.** Drop T. PR62 then passes, and later exact or partial reversions of such branches pass as well, as they already do for linear branches.
- **O1 (pre-existing, outside #423):** the linear arm certifies historical replay only.
  - A linear exact replay followed by an exact revert is `contained` rc 0 (fixture 30).
  - In the public donor history, sibling PR61 (linear, and edited by the same later commit 0ac3e2c) is `contained` rc 0 at both targets with both checkers (rawlogs/pr61-linear-verdicts.log).
  - Requiring T in the linear arm would flip the existing self-test arm `linear-patch-fallback` (merge_containment_selftest_content.py:254). On a replica, T is false (rawlogs/linear-fallback-retention-probe.log). Harmonizing the arms is therefore a policy change that needs its own Issue.

## 7. Deliberate conservative false negatives

| fixtures | case | RMR-1 verdict |
|---|---|---|
| 6, 8, and actual PR62 | legitimate later edits that overlap, touch or rewrite replayed regions, or edit a branch-added file | UNKNOWN |
| 9, 10 | later deletion, rename or mode change of a touched path | UNKNOWN |
| 11 | binary later edits | UNKNOWN |
| 3 | more than one redundant merge (the per-merge variant is safe by composition but not proposed) | STRANDED |
| 25 | octopus with an absorbed parent | STRANDED |
| 28 | first parent two or more commits back | STRANDED |
| 22 | resolution work that is present but not independently proved by this arm | STRANDED |
| — | replays that are not whitespace-exact | STRANDED (by design) |

## 8. Acceptance mapping

| AC | status | evidence |
|---|---|---|
| AC1 | met | §2 reconstruction; STRANDED 3 reproduced on public history, on fixtures 1 and 6, and by the published probe (unchanged checker) |
| AC2 | met (design) | §3 exact criterion. Resolution work: fixtures 21 and 23 STRANDED; fixture 22 stays uncontained (not independently proved) |
| AC3 | met (prototype) | Positive: 1, 2 → rc 0. Missing linear work: 17, 18 STRANDED. Missing resolution work: 21, 23 STRANDED. Whitespace: 19 (and hunk position 20) STRANDED. Later reversions: 7, 9, 10, 12–16 UNKNOWN rc 1 |
| AC4 | not assessed | Implementation-time. Prototype 145/145 shows only that the existing arms do not regress; the full root gates and two completed reviews on the final head remain required |

## 9. Lens coverage (design readiness only; no production coverage claimed)

| lens | artifacts examined | result |
|---|---|---|
| Conformance | #423 AC1–4 and comments; CONTRIBUTING.md:178-246; AGENTS.md §4/§6; REQUIREMENTS.md:213-234 | The criterion maps to AC1–3 (§8). Findings F1 and D1 |
| RTL | #423 scope ("No product RTL or protocol behavior changes"); PR62 paths are tb/*.py and Makefiles; the candidate touches only scripts/check_merge_containment.py | No HDL in scope. The tool's interface-contract analog was checked: exit codes :73-77 are unchanged, no new flag, the new arm is ordered after the existing arms (:567-585). No design blocker |
| Robustness | fixtures 9–11, 16, 20–29; the mutations | Modes, deletion, binary files, hostile configuration and parent shapes all fail closed. Not exercised: SHA-256 object format, non-UTF-8 paths, symlink/gitlink/type-change paths, CRLF-only diffs, large files |
| Tests | unchanged self-test 145/145 (rawlogs/unchanged-selftest.log); prototype 145/145; 31 fixtures; 10/10 mutations; published probe reproduced; determinism | Finding F4 |
| Docs | checker docstring :44-56; `_report` :912-915; CONTRIBUTING step 7; published README | Findings F2, F3 and F5 |

Design findings:

```text
[R242] MINOR Conformance, Docs — #423 AC3 wording; fixture 30; pr61-linear-verdicts.log — "later reversions remain refused ... under the existing policy" holds only for merge-shaped branches
Requirement/evidence: the unchanged linear arm returns contained rc 0 for replay-then-exact-revert and certifies PR61 despite 0ac3e2c.
Impact: readers may assume containment means retention; RMR-1 is deliberately stricter than the linear arm.
Required change: record the asymmetry in #423; file a separate Issue for linear-arm retention semantics (it would change linear-patch-fallback).
Verification: fixture 30 and the replica log remain as cited.

[R242] MINOR Docs — readiness-evidence/423 README.md, probe_ff_merge.py — shape measured as "first parent is an ancestor of second"
Requirement/evidence: the public merge satisfies the narrower "first parent is the second parent's only parent"; the ancestor form admits distance-2 merges, which G1 refuses (fixture 28).
Impact: an implementation keyed to the README wording would be broader than the proven shape.
Required change: state the parent relation in the implementation Issue text.
Verification: pr62-reconstruction.json commit table.

[R242] SUGGESTION Docs — #423 body patch hashes — record the command that reproduces them
Requirement/evidence: both SHA-256 values reproduce exactly with git diff --no-ext-diff --no-textconv --no-renames <parent> <commit>.

[R242] SUGGESTION Tests — implementation self-test design — assert verdict words, not only rc; use a non-adjacent positive extension
Requirement/evidence: weakening the G1 tree guard changes fixture 21 only STRANDED->UNKNOWN (same rc); fixture 22 is what flips rc. The published extension is adjacent (fixture 8) and is UNKNOWN under RMR-1.

[R242] SUGGESTION Docs — check_merge_containment.py:44-56, :912-915; CONTRIBUTING.md step 7 — describe historical replay versus retention and the new UNKNOWN meaning
Requirement/evidence: the footer "could not be resolved" misdescribes a replayed-but-not-retained UNKNOWN.
```

## 10. What proof remains

1. An implementation reproducing RMR-1 exactly, with self-test arms asserting verdict words for at least fixtures 1, 3, 6/7, 8, 12, 14, 16, 17, 19, 21, 22, 25, 28 and 30, a repeat of the guard mutations, and the unchanged 145 arms passing.
2. T's safety rests on one stated property: a clean `merge-file` result that is byte-identical to the tip means a no-op re-merge. The fixtures and mutations exercise this; it is not formally proved for every xdiff alignment. Safety does not depend on alignment beyond that property.
3. The items listed as not exercised in §9 Robustness. Performance is O(paths) subprocesses, which a batched `cat-file` implementation can reduce.
4. The D1 record, and a separate Issue for O1/F1.
5. AC4: the full local bar and two completed independent reviews on the final head.

## 11. Lane impact

- **Scope once promoted:** only scripts/check_merge_containment.py, its self-test modules (the content module is already 509 lines, so a third module is likely), the checker docstring and CONTRIBUTING.md step 7. No RTL, processor pin or workflow change. `--selftest` already runs in scripts/run_all_suites.sh:237-258.
- **Implementing RMR-1 does not clear PR62.** Its sweep entry moves from STRANDED to UNKNOWN and stays rc 1. Anything currently waiting on a clean donor sweep stays where it is.
- **Value if implemented:** future exact replays across one redundant no-ff merge become rc 0 when later base edits avoid the replayed regions. Replays whose regions were later edited become an evidence-bearing UNKNOWN instead of a false STRANDED. If that value is judged insufficient, keeping #423 as a documented limitation without code is a scheduling choice, not a design gap.
- **Conflicts:** any lane editing check_merge_containment.py or merge_containment_selftest*.py. The A170/#372 slot is untouched by this text.

## 12. Reproduction

```sh
sh scripts/run_all.sh <clean-checkout-at-88e9276b> [OUTDIR] [WORKDIR]
```

This runs the manifest check, prototype build, both self-tests, fixtures, mutations, a donor mirror clone with the PR62 reconstruction, and the published probe against both checkers, bracketed by integrity snapshots. One scratch run took 38 s and reproduced every recorded result, with integrity IDENTICAL. Raw logs are in rawlogs/, and published-fixture-6181e900/ holds the verified public blobs.

## 13. Checkout integrity

The initial and final snapshots were taken by scripts/integrity.py and compared as `IDENTICAL` (rawlogs/integrity-initial.json, rawlogs/integrity-final.json, rawlogs/integrity-compare.log). They cover HEAD 88e9276b2a220c716f64a843f7e1eb8f9265e896, the raw index sha256 5c23a0ec…, `ls-files -s`, the 855 tracked entries' working-tree kind, mode and blob, status with ignored files, and refs.

R242-DESIGN FINISHED

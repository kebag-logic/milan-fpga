[R859] NEGATIVE - exact head ee5c6f922a5863e25cef5bbc5f37289acf4e4777

Round R859-1. Internal cleared-context review of PR #942 for issue #940 (docs only, base `dev`).
Head `ee5c6f922a5863e25cef5bbc5f37289acf4e4777`, tree `6c9fce3f9da97088789783556f38aac79a288d4c`.
Source base and live `dev` are both `6b66f66d89cf25d2717687bcc2c3bf617685a99a`, so the head descends directly from the unchanged base.

The verdict is NEGATIVE because two MINOR findings are open: R859-001 and R859-002.
Both concern the scope and authority of the new process rules, not the gates.
Every docs gate I ran passes, both diagrams render, and every new link resolves.

## Reconstruction

I read these in order: AGENTS.md and CONTRIBUTING.md at the head, then docs/README.md, then issue #940 (body and its three comments).
Next came the two owner decisions on #665: issuecomment-6939460730 (option B) and issuecomment-6939574513 (way of working).
Then the diff `6b66f66d..ee5c6f92` and its two commits, PR #942's body, and the author packets at archive `fd6e25a4`.
Before my own pass there were no prior public review findings on PR #942: no reviews, and only two "review started" comments.
So I had nothing to resolve or retain.

## Findings

### R859-001 MINOR: freezing is not limited to batch members, so an unbatched PR whose merge conflicts has no lawful path

- **Lenses:** Conformance, Robustness, Docs.
- **Where:** `CONTRIBUTING.md:445-450` (Freeze), `CONTRIBUTING.md:502-509` (Not batched), `AGENTS.md:298-300`, `AGENTS.md:472`.
- **Authority and evidence:**
  - `CONTRIBUTING.md:445` defines frozen for every PR: "A PR with both positive reviews at its own head is frozen".
  - `:447` adds "A frozen PR takes no merge of the moving base", and `:449` adds "It changes only for a defect in its own change".
  - `AGENTS.md:299` repeats the rule for any PR ("freezes a PR at two positives"). `AGENTS.md:472` makes it a non-negotiable rule: "Never merge the moving base into a frozen PR".
  - `CONTRIBUTING.md:504-505` sends an urgent fix or a shared-infrastructure change down section 2.1 alone.
  - The owner's decision (issuecomment-6939574513 item 1) froze only train members: "no sync round onto dev-soft-core".
  - The 2.1 diagram (`CONTRIBUTING.md:78`) also shows freezing on the batched path only.
- **Impact:** take an unbatched PR, for example an urgent fix, that has two positives and then conflicts with the moving base. It cannot take a base merge, cannot change for anything except its own defect, and cannot join a batch. Section 2.1 step 7 still needs a mergeable candidate, so the documented rules give it no lawful way to merge. Brief check (2), that no rule is left contradicting, is not met for this case.
- **Required outcome:** sections 2.3, AGENTS 6 and AGENTS 8 must say whether freezing applies only to PRs that merge through a batch. If it applies to every PR, they must state the path for an unbatched frozen PR whose merge conflicts. For example, the base merge and its resolution could be reviewed under 2.1 as new change.
- **Verification:** reread 2.1 step 7, 2.3 Freeze and Not batched, and AGENTS sections 6 and 8. They must give one consistent answer for an urgent fix that conflicts with `dev` after two positives.

### R859-002 MINOR: section 2.3 adds rules that no public authority supports

- **Lenses:** Conformance, Docs.
- **Where:** `CONTRIBUTING.md:454-456`, `:484`, `:495-500`, `:504-509`, and the PR #942 description ("The text is the reviewed draft's").
- **Authority and evidence:**
  - The two #665 decisions and the #940 body support: two positives per PR, freeze, compose once with `--no-ff`, one composition review, one full candidate plus a bench gate on the same images, one merge, and fixes in the composition lane.
  - Some section 2.3 rules appear in neither decision nor in #940:
    - the batch size ("four to eight frozen PRs from one area", `:455`);
    - the ordering rule (`:456`);
    - "Allow one fix round per finding. If it fails, drop the PR", with the bisect, rebuild and return-to-2.1 steps (`:495-500`);
    - the Not-batched classes and their definition of shared infrastructure (`:504-508`);
    - "only an urgent fix may move the base" (`:509`);
    - "If the base moved, merge it in and run the candidate again" (`:484`).
  - The drop rule also changes option B item 5, which said a fix after composition "rebuilds the composition and reruns the train candidate".
  - The PR cites a "reviewed draft" as the source. That draft and its review are not public: #940 has 3 comments, #665 has 5 comments dated 2026-11-17, PR #942 has none, and a repository search for the draft's wording finds only #940, #941 and #942. The author receipt `draft-exact.txt` compares against a draft file that is not in the archive.
  - AGENTS.md section 2 says a cold reviewer must be able to rebuild the task from GitHub and the repository alone. Section 5 says material assumptions are made public in the Issue or PR.
- **Impact:** permanent process rules land, and a reader cannot tell which come from the owner and which the lane wrote. One of them (drop after one fix round) is a real policy change, not a restatement. None of them loosens an existing rule: they all add limits.
- **Required outcome:** do one of these:
  - publish the reviewed draft, or a maintainer or owner comment accepting these specific rules, and link it from the PR and #940;
  - remove the rules that have no authority.
  No change to the text is needed if the authority is published.
- **Verification:** every normative bullet in 2.3 traces to a public decision, or to the published, accepted draft.

### R859-003 RESIDUE (wording only): "Those banks" lost its antecedent

- **Lenses:** Docs.
- **Where:** `docs/testing/CI_WORKFLOWS.md:279`.
- **Evidence:** the inserted paragraph at `:276-277` now sits between "runs builder and full native banks" (`:274`) and "Those banks catch interactions..." (`:279`).
- **Exact fix:** move the two lines "A batch merges once, ..." and "[CONTRIBUTING.md section 2.3](...) defines that path." to after `:281` ("...remain mandatory."). Or start `:279` with "The builder and native banks catch interactions with intervening base changes."

### R859-004 SUGGESTION: the 2.3 flowchart has no path back from a review finding

- **Lenses:** Docs.
- **Where:** `CONTRIBUTING.md:432-441`.
- Only `CA -->|finding| CO` exists, yet the text (`:493-494`) also handles composition-review findings.
- Optional: add `CR -->|finding| CO`. The text governs, so this is not a defect.

### R859-005 SUGGESTION: state the Git version and the base-merge review

- **Lenses:** Docs.
- **Where:** `CONTRIBUTING.md:472` and `:484`.
- My probe confirms the `--remerge-diff` claim (see Tests below). The option needs Git 2.36 or newer, and step 7 states minimum versions for its other tools.
- `:484` is silent on whether the composition reviewers cover a conflicted base merge. AGENTS section 7 already implies that they do.
- Optional: add one line for each.

### R859-006 SUGGESTION: the Contents summaries do not mention batched merges

- **Lenses:** Docs.
- **Where:** `CONTRIBUTING.md:10`, and the AGENTS.md Contents entries for sections 6, 7 and 8.
- These descriptions do not mention batched merges. The gates pass, because the descriptions are hand-written.

## Lens results with evidence

Conformance is UNCLEAN (R859-001, R859-002).
I checked the text against both #665 decisions and the #940 body.
These match:

- two positives at the PR's own head, plus the ancestor-positive rule (`CONTRIBUTING.md:445-446`);
- compose once from the live base, one `--no-ff` merge per member, and no push to member branches (`:460-466`);
- one composition verdict from each reviewer, and one full candidate on the final tree with the builder bank and the full native bank, with bench gates on the same images (`:470-477`);
- one merge commit, never a squash or a rebase, with containment and review-integrity checks for every member (`:481-489`).

None of these loosens another rule:

- The composition PR still meets the protected merge bar and needs two positives (`:470` and `:482`).
- Step 7's per-PR candidate stays for unbatched PRs (`:189-190`).
- The completion bullet is amended at `AGENTS.md:433-434`.
- The ledger scoping at `AGENTS.md:401-408` is the exception the decision allows ("no re-review after a sync").

Every rule the change amends is updated where it is written: the 2.1 diagram (`:78-79`), step 7 (`:189-190`), the AGENTS section 7 ledger and the old line 414, and CI_WORKFLOWS `:273-277`. The one exception is R859-001.

RTL is CLEAN. `receipts/diff-facts.txt` shows the diff `6b66f66d..ee5c6f92` touches only `AGENTS.md`, `CONTRIBUTING.md` and `docs/testing/CI_WORKFLOWS.md`: 122 insertions and 3 deletions. It contains no HDL, no script, no workflow and no gitlink. The four gitlinks the gates need equal `dev`'s pins (`receipts/clone-integrity.txt`). CONTRIBUTING section 1, the HDL, reset and CDC rules, is untouched. So this lens has no scope in this diff, and those artifacts are what make it inapplicable.

Robustness is UNCLEAN (R859-001). I traced the configuration-dependent paths through 2.1, 2.3 and AGENTS sections 6, 7 and 8. These cases all have a defined path:

- a finding after composition (`:493-500`);
- a base that moves before the merge (`:483-484`);
- a round still in flight (`:481`);
- a dropped member (`:500`).

The case with no defined path is a frozen PR that is not batched and whose merge conflicts.

Tests is CLEAN. The PR changes no test. I proved the existing gates catch faults in the new links, using planted mutants in a scratch clone that I then restored (`receipts/mutants.txt`):

| Mutant | Gate | Result |
|---|---|---|
| M1: AGENTS fragment changed | `gen_toc.py --verify-anchors` | rc 1 |
| M2: CI_WORKFLOWS fragment changed | `gen_toc.py --verify-anchors` | rc 1 |
| M3: CI_WORKFLOWS path changed | `docs_check.py` | rc 1 |
| M5: heading renamed | `gen_toc.py --verify-anchors` | rc 1 |
| M6: em dash in a committed line | `check_em_dash.py --base` | rc 1 |
| M4: same-page fragment in CONTRIBUTING | both gates | pass, which is the known #941 gap |

The `--remerge-diff` probe (`tools/remerge_probe.sh`, receipt `receipts/remerge-diff-probe.txt`) checks the claim at `:472`. In a throwaway repo, `git show --remerge-diff` showed both the conflict resolution and an unrelated edit hidden in the merge, and nothing for a clean merge. The claim holds on Git 2.56.1.

The PR's own figures match mine:

- 620 cross-page fragment links;
- 0 em-dash findings over 122 added lines;
- 122 insertions and 3 deletions;
- the diff from `490d54ee` to the head is empty when whitespace is ignored (0 bytes).

Docs is UNCLEAN (R859-001, R859-002). R859-003 is residue and does not count against the lens. My checks:

- **Paragraph and bullet lengths, counted by `tools/para_words.py`** (`receipts/para-words.txt`):
  - every new paragraph has at most 27 words (link targets excluded);
  - every new bullet has at most 18 words;
  - none is over the 20-30 limit.
- **Anchor:** the `2.3 Batched merges` heading has the slug `23-batched-merges`, exactly once. All four links resolve to CONTRIBUTING.md: `CONTRIBUTING.md:189`, `AGENTS.md:299`, `AGENTS.md:434` and `CI_WORKFLOWS.md:277` (`receipts/anchors-mermaid.txt`).
- **Diagrams:** both CONTRIBUTING flowcharts render with exit code 0 using the local diagram tool listed in `receipts/tool-versions.txt`.
  - Diagram 1 has a single `M` node, and the new `BT` node and edges are present.
  - Diagram 2 has every label.
  - See `receipts/mermaid-render.txt` and `receipts/mermaid/`.
- **Names:** the added lines contain no lane labels, session prefixes, or tool or model names. The only matches are decision URLs with `#issuecomment` fragments, the same link form the existing #514 and #423 decision links use. The source-comment rule does not apply to a docs-only change.
- **Commits:** both are one-line, with no body and no trailers.

## Docs gates I ran at the exact head

I ran these on a clean clone, with the pinned renderer installed into a scratch environment (`receipts/gates/`). All exit with rc 0:

- `docs_check.py`: 0 findings.
- `check_doc_style.py`: OK.
- `check_em_dash.py --base 6b66f66d`: 0 findings over 122 added lines.
- `gen_toc.py --verify-anchors`: 620 links.
- `gen_toc.py --check`: OK.
- `check_doc_paths.py`: OK.
- `docs_inventory.py --check`: fresh.
- `check_feature_status.py`: 0 findings.

The author's round-2 replay of the five docs workflow jobs (`author-r2/receipts/gate-table.md`) shows every job succeeded and no step exited non-zero. I did not re-run the builder legs or the RV32 SDK install.

## Reviewer-owned ledger

| Lens | Result | Artifacts examined | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R859-001, R859-002) | `CONTRIBUTING.md:67-85,180-190,423-509`; `AGENTS.md:295-306,398-434,465-474`; `CI_WORKFLOWS.md:270-281`; both #665 decisions; #940 | R859-1 | ee5c6f922a5863e25cef5bbc5f37289acf4e4777 |
| RTL | CLEAN | `receipts/diff-facts.txt` (3 Markdown files only); `receipts/clone-integrity.txt` (gitlinks unchanged); CONTRIBUTING section 1 untouched | R859-1 | ee5c6f922a5863e25cef5bbc5f37289acf4e4777 |
| Robustness | UNCLEAN (R859-001) | `CONTRIBUTING.md:443-509` paths; `AGENTS.md:298-306,472-473` | R859-1 | ee5c6f922a5863e25cef5bbc5f37289acf4e4777 |
| Tests | CLEAN | `receipts/mutants.txt` (M1-M6); `receipts/remerge-diff-probe.txt`; `receipts/gates/RC.txt`; `author-r2/receipts/gate-table.md` | R859-1 | ee5c6f922a5863e25cef5bbc5f37289acf4e4777 |
| Docs | UNCLEAN (R859-001, R859-002; residue R859-003) | `receipts/para-words.txt`; `receipts/anchors-mermaid.txt`; `receipts/mermaid-render.txt`; `receipts/diff-facts.txt` | R859-1 | ee5c6f922a5863e25cef5bbc5f37289acf4e4777 |

## Limits

- **Hosted checks:** when I queried, `docs-gates-0`, `docs-gates-1` and `docs-gates-2` and one "Fail fast" job were still in progress, and no `docs-check` aggregate had been emitted yet. These completed with success:
  - `rtl-fast`;
  - `docs-check-no-git`;
  - `wire-accountability`;
  - `elaborate` and its five gate jobs;
  - `full-ci-gate`;
  - `bdd-conformance`.

  `verilator-suites` and `yosys-portability` were skipped contexts, as expected for docs only. Skipped contexts are not executed evidence. See `receipts/hosted-check-runs.txt`.
- **Docs gates:** I ran 8 docs gate scripts locally, not the full five-job replay: no submodules, no builder legs, no SDK install. For those I rely on the author's published receipts.
- **Draft:** I could not see the private draft that R859-002 refers to.
- **Not run:** no source bank, candidate, act run, hardware run or physical calibration. Field skips are not hardware proof.
- **Probes:** the mutants and the remerge-diff probe ran only in scratch copies. The review clone is unchanged at the exact head: worktree, index, modes and gitlinks all match (`receipts/clone-integrity.txt`).

## Manager duties still pending

- Get R859-001 and R859-002 answered, then have this lane re-reviewed at the new head.
- Carry R859-003 to the residue checklist.
- Accept the hosted `docs-gates-*` and the `docs-check` aggregate at the exact head.
- Build the current-dev merge candidate at the merge turn. The head descends directly from the unchanged `dev` tip `6b66f66d`.
- Get explicit maintainer authorization for the merge.
- Run containment and review-integrity after the merge.
- Keep the follow-up on #940 for members marked merged by ancestry.
- The external review is a separate requirement.

R859-1 FINISHED

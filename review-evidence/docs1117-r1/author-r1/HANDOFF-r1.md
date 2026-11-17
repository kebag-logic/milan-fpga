# HANDOFF r1: docs1117, issue #940 (author [A795])

Status: REVIEW READY (all docs gates green on a clean clone of 490d54ee)

- Repository: milan-fpga, branch `docs-batch-merge`.
- Base: origin/dev `6b66f66d`, verified with `git rev-parse` and `git ls-remote` (live dev unchanged).
- Head: `490d54ee` (one commit, one-line subject, no body, no trailers).
- Scope: docs only. Draft sections (a) to (h) applied verbatim at their anchors.
- Not pushed and no PR opened: the manager pushes and opens the PR.
- TAKEN posted: #940 issuecomment-6939809424.

## Anchors (draft hint -> dev location)

Every anchor was found by its quoted text. Two had moved by a few lines, and the text landed at the quoted anchor.

| Draft | File | Anchor text | Draft line | Dev line |
|---|---|---|---|---|
| (a) | CONTRIBUTING.md | end of 2.2, before `## 3. Verification bar` | 416 | 418 |
| (b) | CONTRIBUTING.md | diagram `RV -->\|2 positive:<br/>1 own + 1 EXTERNAL\|` | 77 | 77 |
| (c) | CONTRIBUTING.md | step 7 "record both object IDs with the local gate results." | 181 | 185 |
| (d) | AGENTS.md | section 6 "publish a new verdict." | 296 | 296 |
| (e) | AGENTS.md | section 7 "three columns" paragraph | 389 | 389 |
| (f) | AGENTS.md | "- the candidate merge result is validated;" | 414 | 414 |
| (g) | AGENTS.md | section 8, before the last bullet | 452 | 452 |
| (h) | docs/testing/CI_WORKFLOWS.md | "The merge train validates composition..." | 273-274 | 273-274 |

## Changes (file:line at head 490d54ee, and reason)

| Draft | Head location | Change | Reason |
|---|---|---|---|
| (a) | CONTRIBUTING.md:423-510 | new `### 2.3 Batched merges`: two decision links, scope lines, mermaid flowchart, Freeze / Batch / Compose once / Check once / Merge once / Findings after composition / Not batched | records the #665 decisions as standing process; appended after 2.2 so `#22-lanes-and-traps` does not move |
| (b) | CONTRIBUTING.md:78-79 | 2.1 diagram: `RV -->\|2 positive, batched\| BT[...]` and `BT -->\|batch candidate clean\| M` | the diagram showed the per-PR candidate as the only path to merge |
| (c) | CONTRIBUTING.md:189-190 | step 7: a batched PR uses the batch's candidate on the composed tree | step 7 required a candidate per PR from latest dev plus the PR head |
| (d) | AGENTS.md:298-306 | section 6: a frozen PR is not re-reviewed for a base move; a composition review's narrow diff and how lens coverage is stated | the sync re-reviews the decision removes |
| (e) | AGENTS.md:400-405 | section 7: each member's ledger stays banked at its frozen head; the composition ledger covers resolutions and fixes; conflict-free interactions go to the batch candidate | read strictly, "a later commit ... un-covers that lens" un-covers a frozen PR when another member merges |
| (f) | AGENTS.md:430-431 | section 7 bullet: "validated, or for a batched PR the batch candidate of section 2.3" | the completion bar named only the per-PR candidate |
| (g) | AGENTS.md:469-470 | section 8: two new never-rules (no base merge into or base-move re-review of a frozen PR; no member-branch fix after composition) | the non-negotiable list |
| (h) | docs/testing/CI_WORKFLOWS.md:273-276 | "Fast feedback": merge validation gates the composed tree; one batch candidate covers all members; link to 2.3 | the old two lines described a per-merge "merge train" candidate |

Nothing else changed. `receipts/draft-exact.txt` shows the commit's added and removed lines equal the draft's, file by file.

## Checks and planted mutants (no new check was added; the existing gates were proved to bite on the new links)

| Mutant (planted in the worktree, then restored) | Gate | Failing words |
|---|---|---|
| M1 AGENTS.md `CONTRIBUTING.md#23-batched-merges` -> `#23-batched-mergez` | `gen_toc.py --verify-anchors` rc 1 | `MISS AGENTS.md -> CONTRIBUTING.md#23-batched-mergez` |
| M2 CONTRIBUTING.md same-page `(#23-batched-merges)` -> `mergez` | no repo gate fails (gap, see open points); scratch check `same_page_anchors.py` rc 1 | `CONTRIBUTING.md#23-batched-mergez: MISSING` |
| M3 CI_WORKFLOWS.md `../../CONTRIBUTING.md` -> `../CONTRIBUTING.md` | `docs_check.py` rc 1 | `docs/testing/CI_WORKFLOWS.md:276: broken link -> ../CONTRIBUTING.md` |
| M4 CI_WORKFLOWS.md `#23-batched-merges` -> `mergez` | `gen_toc.py --verify-anchors` rc 1 | `MISS docs/testing/CI_WORKFLOWS.md -> ../../CONTRIBUTING.md#23-batched-mergez` |

- Cross-page fragment links reproduced: 617 on dev, 620 at head (the three new links from (d), (f) and (h)).
- Mermaid: both CONTRIBUTING.md flowcharts render with `mmdc` rc 0, and the new nodes are in the SVG (`receipts/mermaid.txt`).

## Gates

Each job of `.github/workflows/docs.yml` was replayed by `receipts/tools/replay_docs.py`. Each job got a fresh `--no-local` clone detached at `490d54ee`, origin set to the public repository, and a fresh CPython 3.12 venv (the CI constraints pin cp312 wheels). HOME was a fresh scratch directory, so the RV32 SDK installed from its pinned archive exactly as on a hosted runner. Every `run:` body executed verbatim under `bash --noprofile --norc -eo pipefail`, with GITHUB_ENV folded in after each step. The pull_request context was dev as base.

| Job | Run steps | Result | Longest step |
|---|---|---|---|
| wire-accountability | 3 | success | submodule fetch (the gate itself 1 s) |
| docs-check-no-git | 2 | success | docs_check + feature status without .git |
| docs-gates-0 | 48 | success | gate_24 compiler-absent firmware controls, 568 s |
| docs-gates-1 | 8 | success | builder leg 0 of 2, 1072 s |
| docs-gates-2 | 10 | success | builder leg 1 of 2, 492 s |

- 71 run steps across the five jobs, all rc 0. The full per-step table is `receipts/gate-table.md`, and the logs are in `receipts/logs/<job>/`.
- Not run (hosted-only): action steps (checkout, cache, upload), evidence recording, apt package resolution, and the `docs-check` receipt-union job.
- Substituted: the sv2v install uses the same pinned v0.0.12 archive and sha256, installed into a scratch bin instead of `sudo /usr/local/bin`. The diagram-dependency step dropped its apt line (librsvg2-bin is on the host) and ran its pip line.
- Every clone was still clean (`git status --porcelain` empty) after its job.
- protocol-processor in each clone: its own toplevel, origin the processor repository, at `801ef22`.
- CPU: `cpu_ranges.py pick` returned 1 (all 128 CPUs booked, no free range). So the jobs ran in this session, pinned with `taskset -c 96-103` (the session pool). No unit was created. Peak MemAvailable stayed above 67 GB.

Targeted checks:

| Check | Result | Receipt |
|---|---|---|
| draft text verbatim and nothing else changed | PASS | `receipts/draft-exact.txt` |
| check_em_dash on 117 added lines (base = merge-base with live dev) | 0 findings, rc 0 | `receipts/anchors-and-em-dash.txt` |
| gen_toc --verify-anchors dev vs head | 617 -> 620, rc 0 | `receipts/anchors-and-em-dash.txt` |
| same-page `#23-batched-merges` | resolves; mutant MISSING rc 1 | `receipts/mutants.txt` |
| mutants M1 to M4 | M1, M4 caught by gen_toc; M3 by docs_check; M2 only by the scratch check | `receipts/mutants.txt` |
| mermaid render, both CONTRIBUTING.md flowcharts | rc 0, new nodes present | `receipts/mermaid.txt` |
| check_doc_style limits on added lines (informational) | gate OK; 46 limit hits on pages outside its list | `receipts/style-on-added.txt` |

## Comments posted on #940

- `[A795] TAKEN`: issuecomment-6939809424.
- `[A795] REVIEW READY`: issuecomment-6940360656 (text in `REVIEW-READY.md`).
- No other comment was posted, edited or deleted.

## For the manager

- Push `docs-batch-merge` at `490d54ee`, then open the PR against `dev` with `PR-BODY.md` (first line `[A795]`, `Closes #940`, `Relates to #665`).
- Reviewers are not yet named in #940 or in the PR body (`[R<n>]` placeholders).
- The scratch directory (replay clones, venvs, the RV32 SDK, the SVG renders) is outside this output directory. No process of this lane is left running.

## Open points for the reviewer

1. **Paragraph length.** check_doc_style.py does not list CONTRIBUTING.md, AGENTS.md or CI_WORKFLOWS.md, so the gate has no finding. Its limits applied to the new lines anyway: (d) renders as paragraphs of 29 and 40 words, (e) 63 words, and (h) joins an existing block that was already five sentences. The draft text is kept verbatim, as instructed; splitting these would be a reviewer call.
2. **Same-page anchors are not gated.** No docs gate checks a `(#frag)` link inside its own page (M2). The new one resolves (checked with gen_toc's own anchor walk). This is a pre-existing gap and belongs in a new Issue, not in this PR.
3. **Draft caveats carried forward** (the draft's section 3 notes): the decision comments scope option B to the flip train; recording it as standing process rests on the owner's 11-17 request in #940. Ancestry-merged member PRs are not yet proved against `check_merge_review_integrity.py` and `check_merge_containment.py --merged-prs`; #940 records that follow-up.

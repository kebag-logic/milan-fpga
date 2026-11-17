[A795]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN. Docs only. All five docs workflow jobs pass on a clean clone of `ee5c6f92`. `docs-batch-merge` -> `dev`.

Author packets: [`review-evidence/docs1117-r1/author-r1` and `author-r2`](https://github.com/kebag-logic/milan-fpga/tree/docs1117-review-evidence/review-evidence/docs1117-r1) on branch `docs1117-review-evidence` (archive `fd6e25a4`).

## Linked Issue / roles

Closes #940
Relates to #665

Executor: `[A795]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

Records the batched-merge process from the two #665 decisions as standing process, as the owner asked in #940. The text is the reviewed draft's, applied at each named anchor. Nothing else changes.

Two commits:

- `490d54ee` applies draft pieces (a) to (h) verbatim.
- `ee5c6f92` splits the three new or changed paragraphs over 30 words into short paragraphs. It adds 5 blank lines and changes no word or order.

| Draft piece | Where | Change |
|---|---|---|
| (a) | `CONTRIBUTING.md` new `### 2.3 Batched merges`, after 2.2 | Freeze, Batch, Compose once, Check once, Merge once, Findings after composition, Not batched, with a flowchart. Appending after 2.2 keeps `#22-lanes-and-traps` stable. |
| (b) | `CONTRIBUTING.md` 2.1 diagram | Adds the batched path: `2 positive, batched` -> frozen and composed once (section 2.3) -> merge when the batch candidate is clean. |
| (c) | `CONTRIBUTING.md` 2.1 step 7 | A PR merged through a batch uses the batch's candidate, which gates the composed tree. |
| (d) | `AGENTS.md` section 6 | A frozen PR is not re-reviewed because its base moved. A composition review has a narrow diff, and states lens coverage at the composition head. |
| (e) | `AGENTS.md` section 7, after the "three columns" paragraph | Each member's ledger stays banked at its frozen head. The composition ledger covers resolutions and composition fixes. Conflict-free interactions are left to the batch candidate. |
| (f) | `AGENTS.md` section 7 completion bullet | "the candidate merge result is validated, or for a batched PR the batch candidate of section 2.3". |
| (g) | `AGENTS.md` section 8 | Two never-rules: no base merge into a frozen PR or re-review for a base move, and no fix on a member's branch after composition. |
| (h) | `docs/testing/CI_WORKFLOWS.md` "Fast feedback" | Replaces the two "merge train" lines. Merge validation gates the composed tree, one batch candidate covers all members, and the text links to section 2.3. |

Existing rules the draft amends, and how:

- Step 7's per-PR candidate stays for unbatched PRs; (c) redirects only batched ones.
- The 2.1 diagram gains a second path through (b).
- AGENTS section 7's "a later commit un-covers that lens" is scoped by (e), so another member's merge no longer un-covers a frozen PR.
- The completion bullet is amended by (f).
- "One lane = one branch = one PR" and "never change another lane's branch" stand. The composition is its own lane and PR, and 2.3 forbids pushing to member branches.

Every new or changed paragraph is 30 words or fewer:

| Paragraph | Words |
|---|---|
| CONTRIBUTING.md step 7, batch note | 22 |
| CONTRIBUTING.md 2.3, decision links | 16 |
| CONTRIBUTING.md 2.3, scope | 24 |
| AGENTS.md section 6, frozen PR | 29 |
| AGENTS.md section 6, composition review (split) | 19, 21 |
| AGENTS.md section 7, composed batch (split) | 23, 21, 19 |
| CI_WORKFLOWS.md "Fast feedback" (split) | 24, 19, 27 |

The 27-word paragraph is the existing lines that follow the draft's. The new bullets are at most 20 words each.

## Authoritative references

- #665 [one-candidate decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939460730) and [way-of-working decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939574513).
- #940, the task.
- `CONTRIBUTING.md` 2.1 and 2.2; `AGENTS.md` sections 6, 7 and 8; `docs/testing/CI_WORKFLOWS.md` "Fast feedback".

## How to get into the same state

```sh
git fetch origin
git switch --detach ee5c6f92
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/docs_inventory.py --check
python3 scripts/check_feature_status.py
git diff --shortstat 6b66f66d ee5c6f92
git diff --ignore-all-space --ignore-blank-lines 490d54ee ee5c6f92
```

Expected result / pass criteria:

- Every command exits 0.
- `gen_toc.py --verify-anchors` reports 620 cross-page fragment links (617 on `dev`); the three new ones are the `CONTRIBUTING.md#23-batched-merges` links from (d), (f) and (h).
- `check_em_dash.py` reports 0 findings over 122 added lines in 3 pages.
- The diff touches only `AGENTS.md`, `CONTRIBUTING.md` and `docs/testing/CI_WORKFLOWS.md`: 122 insertions, 3 deletions.
- The last command prints nothing: the second commit changes only whitespace.
- The bad-link mutants were caught: a broken `#23-batched-merges` fragment in `AGENTS.md` or `CI_WORKFLOWS.md` fails `gen_toc.py --verify-anchors`, and a wrong `../CONTRIBUTING.md` path fails `docs_check.py`.
- Both `CONTRIBUTING.md` flowcharts parse and render.

## Known limitations / out of scope

- No docs gate checks a same-page `(#fragment)` link. The new `#23-batched-merges` link inside `CONTRIBUTING.md` resolves against the heading-anchor walk in `gen_toc.py`, but a broken one would pass the gates today. That gap needs a new Issue and is not fixed here.
- `check_doc_style.py` does not cover these three pages. The 30-word paragraph limit was applied by hand; the table above lists the counts.
- It is not yet proved that `check_merge_review_integrity.py` and `check_merge_containment.py --merged-prs` judge member PRs correctly when they are marked merged by ancestry. #940 records this as a follow-up after the first batch merge. Any fix is shared infrastructure and merges unbatched.
- `dev-soft-core` gets the same text as the first unbatched change after its current train merges (#940).

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests (docs only; the existing link and anchor gates were shown to fail on planted bad links)
- [x] Required local verification bar passes (docs workflow jobs on a clean clone)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

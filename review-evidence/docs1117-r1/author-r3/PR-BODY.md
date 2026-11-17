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

GREEN. Docs only. All five docs workflow jobs pass on a clean clone of `eade77c9`. `docs-batch-merge` -> `dev`.

## Linked Issue / roles

Closes #940
Relates to #665

Executor: `[A795]`
Internal cleared-context reviewer: `[R859]`
External reviewer: `[R860]`

## Description

Records the batched-merge process from the two #665 decisions as standing process, as the owner asked in #940. The details each rule adds, and the reason for each, are the [maintainer decision on #940](https://github.com/kebag-logic/milan-fpga/issues/940#issuecomment-6941861692).

Three commits:

- `490d54ee` adds section 2.3 and the pointers and amendments.
- `ee5c6f92` splits paragraphs over 30 words. It only adds blank lines.
- `eade77c9` answers review round R859-1.

| Where | Change |
|---|---|
| `CONTRIBUTING.md` new `### 2.3 Batched merges`, after 2.2 | Freeze, Batch, Compose once, Check once, Merge once, Findings after composition, Not batched, with a flowchart. Appending after 2.2 keeps `#22-lanes-and-traps` stable. |
| `CONTRIBUTING.md` 2.1 diagram | Adds the batched path: `2 positive, batched` -> frozen and composed once (section 2.3) -> merge when the batch candidate is clean. |
| `CONTRIBUTING.md` 2.1 step 7 | A PR merged through a batch uses the batch's candidate, which gates the composed tree. |
| `AGENTS.md` section 6 | A frozen batch member is not re-reviewed because its base moved. An unbatched PR is never frozen. A composition review has a narrow diff, and states lens coverage at the composition head. |
| `AGENTS.md` section 7 | Each member's ledger stays banked at its frozen head; the composition ledger covers resolutions and composition fixes. The completion bullet accepts the batch candidate for a batched PR. |
| `AGENTS.md` section 8 | Never merge the moving base into a frozen batch member or re-review one for a base move, and never fix a member on its own branch after composition. |
| `docs/testing/CI_WORKFLOWS.md` "Fast feedback" | Merge validation gates the composed tree; one batch candidate covers all members, with a link to section 2.3. |

Answers to review round R859-1:

- **R859-001:** freezing applies only to a PR a maintainer has named in a batch. An unbatched PR follows section 2.1 as before. It may merge the moving base, and that merge is reviewed under 2.1 as new change. This is stated in 2.3 Freeze and AGENTS.md sections 6 and 8. So an urgent fix that conflicts after two positives has one path: merge the base, have that reviewed, then go through step 7's candidate.
- **R859-002:** section 2.3 now links the maintainer decision on #940 next to the two #665 decisions. No rule text changed for this.
- **R859-003:** in "Fast feedback", "Those banks" follows its antecedent again.
- **R859-004:** the 2.3 flowchart has a path back from a composition-review finding.
- **R859-006:** not taken. Three of the four Contents entries are already over 30 words (31, 36 and 76), so adding to them would break the 30-word limit. The fourth has room for only three words.

Existing rules this amends, and how:

- Step 7's per-PR candidate stays for unbatched PRs, and only batched ones use the batch candidate.
- AGENTS section 7's "a later commit un-covers that lens" is scoped for batch members only.
- "One lane = one branch = one PR" and "never change another lane's branch" stand. The composition is its own lane and PR.

Every new or changed paragraph is 30 words or fewer, and every new bullet 23 or fewer.

## Authoritative references

- #665 [one-candidate decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939460730) and [way-of-working decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6939574513).
- #940 [maintainer decision on the details](https://github.com/kebag-logic/milan-fpga/issues/940#issuecomment-6941861692).
- `CONTRIBUTING.md` 2.1 and 2.2; `AGENTS.md` sections 6, 7 and 8; `docs/testing/CI_WORKFLOWS.md` "Fast feedback".

## How to get into the same state

```sh
git fetch origin
git switch --detach eade77c9
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
git diff --shortstat 6b66f66d eade77c9
git diff ee5c6f92 eade77c9
```

Expected result / pass criteria:

- Every command exits 0.
- `gen_toc.py --verify-anchors` reports 621 cross-page fragment links (617 on `dev`). The new ones are three `CONTRIBUTING.md#23-batched-merges` links and one `CONTRIBUTING.md#21-the-issue-to-merge-lane` link.
- `check_em_dash.py` reports 0 findings over 130 added lines in 3 pages.
- The diff touches only `AGENTS.md`, `CONTRIBUTING.md` and `docs/testing/CI_WORKFLOWS.md`: 130 insertions, 3 deletions.
- Bad links were caught when planted. A broken fragment in `AGENTS.md` or `CI_WORKFLOWS.md` fails `gen_toc.py --verify-anchors`. A wrong `../CONTRIBUTING.md` path fails `docs_check.py`.
- Both `CONTRIBUTING.md` flowcharts parse and render.

## Known limitations / out of scope

- No docs gate checks a same-page `(#fragment)` link (#941). The new `#23-batched-merges` link inside `CONTRIBUTING.md` resolves under the heading-anchor walk in `gen_toc.py`.
- `check_doc_style.py` does not cover these three pages. The 30-word paragraph limit was applied by hand and counted.
- It is not yet proved that `check_merge_review_integrity.py` and `check_merge_containment.py --merged-prs` judge member PRs correctly when they are marked merged by ancestry. #940 records this as a follow-up after the first batch merge.
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

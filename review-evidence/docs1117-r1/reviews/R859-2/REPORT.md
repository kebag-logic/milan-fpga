[R859] POSITIVE - exact head eade77c95b997e5d9176b58e1f06266aea92c19f

Internal cleared-context review of issue #940 / PR #942, round R859-2. This is a narrow delta review: `ee5c6f92..eade77c9`. It also resolves every finding of round R859-1 (issuecomment-6941855275) at this head.

The verdict is POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. Both R859-1 MINOR findings are resolved at their cause. This round adds one RESIDUE and two SUGGESTIONs. None of them changes the verdict or leaves a lens unclean.

## Reconstruction

- **Contract:** I read AGENTS.md sections 2 to 8 and CONTRIBUTING.md 2.1 and 2.3 at the head.
- **Issue #940:** the body asks for section 2.3 and for pointers in 2.1, AGENTS 6, 7 and 8, and CI_WORKFLOWS "Fast feedback", as docs only and as standing process.
- **Authorities:**
  - #665 issuecomment-6939460730 (option B, one candidate);
  - #665 issuecomment-6939574513 (freeze, compose once, check once, merge once);
  - #940 issuecomment-6941861692, the maintainer decision on each batch detail, posted for the owner.
  - Copies are in `receipts/issue665-decisions.txt` and `receipts/issue940-comments.txt`.
- **Diff:** I reviewed `git diff ee5c6f92..eade77c9` (+14/-6, three Markdown pages; `receipts/diff-ee5c6f92-eade77c9.patch`). It is byte-identical to the author's `round3.diff`. I also reread all of 2.3 at the head, because the delta changes what its rules depend on.
- **Order kept:** I read the prior R859-1 and R860-1 reports only after my own pass over the diff.
- **History:** `490d54ee` -> `ee5c6f92` -> `eade77c9`, on dev `6b66f66d`. Live `dev` is still `6b66f66d89cf25d2717687bcc2c3bf617685a99a` (`receipts/live-dev.txt`). So the head's tree is the candidate merge tree.

## Prior findings, resolved or retained at this head

| ID | Prior severity | Status at eade77c9 | Evidence |
|---|---|---|---|
| R859-001 | MINOR | RESOLVED | See below. |
| R859-002 | MINOR | RESOLVED | See below. |
| R859-003 | RESIDUE | RESOLVED | `docs/testing/CI_WORKFLOWS.md:273-281`. "Those banks" (`:276`) follows the "builder and full native banks" paragraph (`:273-274`). The batch lines moved to `:280-281`. |
| R859-004 | SUGGESTION | TAKEN | `CONTRIBUTING.md:439` adds `CR -->|finding| CO`. I rendered it with mmdc 11.16.0: rc 0, 2 `finding` edge labels. The SVG sha256 `d85e69f6...` matches the author's receipt (`receipts/mermaid-render.txt`). |
| R859-005 | SUGGESTION | RETAINED, optional | Not answered. Still optional: `--remerge-diff` needs Git 2.36 or newer (`CONTRIBUTING.md:477`). AGENTS 7 (`:407-408`) implies that composition reviewers cover a conflicted base merge (`CONTRIBUTING.md:489`). |
| R859-006 | SUGGESTION | NOT TAKEN, reason accepted | The author says three of the four Contents entries are already over 30 words. Adding to them would break the limit. That is a fair reason for an optional item. |

**R859-001 resolved: freezing applies only to batch members.**

- `CONTRIBUTING.md:447-448`: "Freezing applies only to a PR a maintainer has named in a batch. Such a PR ... is frozen."
- `:454-455`: an unbatched PR follows 2.1, may merge the moving base, and that merge is reviewed under 2.1 as new change.
- `AGENTS.md:299` says "freezes a batch member". `:302-303` says an unbatched PR is never frozen, and its base merge is reviewed under 2.1 as new change.
- `AGENTS.md:475` is now "Never merge the moving base into a frozen batch member ...; an unbatched PR is never frozen."
- The 2.1 diagram (`CONTRIBUTING.md:78`) already showed freezing only on the `batched` edge. All four places now agree.

**R859-001, the urgent-fix case: one consistent path.** I traced an urgent fix that conflicts with `dev` after two positives:

1. `CONTRIBUTING.md:509`: it is not batched.
2. `:447`: it is therefore not frozen.
3. `:454-455`: it merges the base, and that merge is reviewed under 2.1 as new change.
4. AGENTS 7 (`:390-402`): the coverage rule then re-banks every lens whose scope the merge touched.
5. `CONTRIBUTING.md:180-187`: it goes through step 7's per-PR candidate (2.3 applies only to batch members).
6. `:514`: if a batch candidate is running, only this urgent fix may move the base. The batch then merges the base and reruns its candidate (`:489`).

No rule in 2.1, 2.3, AGENTS 6, 7 or 8 forbids any step. A dropped member (`:505`) leaves its batch, so it is unbatched and takes the same path. `grep -i 'froze|freez|frozen'` over all tracked Markdown finds no other process text that freezes an unbatched PR.

**R859-002 resolved: every 2.3 rule now has a public source.**

- `CONTRIBUTING.md:428` links #940 issuecomment-6941861692. The live PR #942 body links it twice (Description and Authoritative references; `receipts/pr942.json`).
- I traced every normative bullet of 2.3 (`:447-514`) to a public source:
  - **#940 decision:** freeze scope (`:447`, `:454-455`); batch formed by a maintainer on a public Issue (`:459`); four to eight PRs as guidance, written as "normally" (`:460`); order (`:461`); composition as its own PR (`:471`); base moved, merge in and rerun (`:489`); merge commit only (`:491`); one fix round, then drop (`:500-501`); narrowing, rebuild and full rerun (`:502-503`); dropped PR returns to 2.1 (`:505`); the two Not-batched classes, "settled", and only an urgent fix moving the base (`:509-514`).
  - **#665 issuecomment-6939574513:** freeze, no sync, no re-review, changes only for its own defect (`:448`, `:450-452`); compose once, `--no-ff`, resolve once, re-measure, fix only what composition breaks (`:465-470`); one composition review by both reviewers on resolutions and measurements (`:475-478`); one merge, members marked merged (`:492-493`); fix in the composition lane (`:498`).
  - **#665 issuecomment-6939460730:** an earlier positive counts (`:449`); one full candidate with builder and full native banks, bench gate on the same images, no intermediate candidate (`:479-482`).
  - **Existing repository rules:** never push to a member's branch is AGENTS 8 "never change another active lane's branch" (`:468`). No round in flight, the protected bar, maintainer authorization and per-member containment come from AGENTS 7 and CONTRIBUTING 2.1 step 7 (`:486-488`, `:490`, `:494`). A re-reviewed own-defect fix (`:453`), composition fixes covered by the composition review (`:499`) and rebuilt resolutions reviewed again (`:504`) follow from 2.1 and #665 item 3.
- Two bullets generalize a train-specific item into standing process, as #940 asks:
  - `:469` "every measurement a member reported" generalizes the named 1x1/1if and 8x8/1if measurements.
  - `:481` "any bench gate" generalizes "the gating S12b".
- `:471` "lists the conflicted paths of each merge" is a record-keeping duty. It backs the composition review's scope (#665 item 3).

None of these needs further authority. The decision post-dates R859-1. It comes through the same owner-delegated channel as both #665 decisions.

## Findings of this round

### R859-2-001 RESIDUE (wording only): PR body line on the AGENTS section 7 exception can be read backwards

- **Lenses:** Docs.
- **Where:** the PR #942 body, "Existing rules this amends, and how", second bullet.
- **Evidence:** it reads "AGENTS section 7's 'a later commit un-covers that lens' is scoped for batch members only." A reader could take this to mean the un-cover rule now applies only to batch members. The repository text says the opposite. `AGENTS.md:404-411` adds one exception for batch members (each member's ledger stays banked at its frozen head), and the general rule at `:390-402` is unchanged.
- **Exact fix:** "AGENTS section 7's 'a later commit un-covers that lens' keeps its scope; batch members get one exception: each member's ledger stays banked at its frozen head."

### R859-2-002 SUGGESTION: the 2.3 flowchart's freeze node does not show the batch condition

- **Lenses:** Docs.
- **Where:** `CONTRIBUTING.md:435`, `RV[2 positive<br/>at the PR head] --> FZ[frozen]`.
- **Evidence:** the first Freeze bullet (`:447`) and the 2.1 diagram (`:78`, the `batched` edge) both give the condition. The 2.3 node, read alone, still shows the pre-R859-001 rule. The text governs, so this is not a defect.
- **Optional:** `RV[2 positive at the PR head<br/>named in a batch] --> FZ[frozen]`.

### R859-2-003 SUGGESTION: the order tie-break can tie now that freezing waits for naming

- **Lenses:** Conformance, Robustness.
- **Where:** `CONTRIBUTING.md:461`, "Order follows dependencies first, then the time each PR froze."
- **Evidence:** under `:447-448`, a PR that had two positives before it was named freezes when it is named. Several PRs named in one comment can therefore freeze at the same moment. The #940 decision gives this rule as "deterministic".
- **Why this is not a defect:** order is reconstructable regardless. `:459` has the maintainer publish the members and their order on a public Issue, and the doc records the decision faithfully.
- **Optional:** ask the maintainer to confirm the tie-break, for example "the time each PR reached its second positive". Record it on #940 before the first standing batch.

## Lens results with evidence

Every lens was applied at `eade77c95b997e5d9176b58e1f06266aea92c19f`.

```text
[R859] PASS Conformance — CONTRIBUTING.md:423-514, AGENTS.md:298-303,404-411,436-437,475, CI_WORKFLOWS.md:273-281 — R859-001 and R859-002 checked against #665 issuecomment-6939460730 and -6939574513 and #940 issuecomment-6941861692; every 2.3 bullet traced (list above); issue #940 scope met (2.3 plus pointers in 2.1, AGENTS 6/7/8, CI_WORKFLOWS); R859-2-003 is a SUGGESTION
[R859] PASS RTL — receipts/clone-integrity.txt (delta files vs dev: AGENTS.md, CONTRIBUTING.md, docs/testing/CI_WORKFLOWS.md only; 0 gitlink changes) — no HDL, CDC, tooling or interface artifact is in scope; the workflow claims in CI_WORKFLOWS.md:273-278 were only re-paragraphed in this delta; inapplicable by that artifact
[R859] PASS Robustness — CONTRIBUTING.md:447-455,489,498-505,509-514, AGENTS.md:298-303,475 — configuration paths traced: urgent fix that conflicts after two positives, shared-infrastructure change, named-but-not-yet-positive member, dropped member, base move during a batch candidate, composition-review finding (new CR edge); each has exactly one lawful path
[R859] PASS Tests — receipts/rc.txt, receipts/probe_agents21_mutant.log, receipts/author-r3-manifest-check.txt — docs gates re-run at head (all rc 0); planted mutant on the new AGENTS #21-the-issue-to-merge-lane link fails gen_toc --verify-anchors (rc 1, "MISS"), then restored; the author's M0-M5 mutant receipts verified against the packet MANIFEST.json (9/9 author-r3 files downloaded, all hashes OK)
[R859] PASS Docs — receipts/para_words.txt, receipts/mermaid-render.txt, receipts/gen_toc_verify.log, receipts/pr942.json — every added paragraph 30 words or fewer (largest 28, links collapsed) and every added bullet 23 or fewer; 621 cross-page fragment links resolve; the same-page #23-batched-merges link resolves (author M0/M2; gap tracked by #941); both flowcharts render; the PR body links the #940 decision; no lane, round or reviewer label in any added line; R859-2-001 is RESIDUE
```

## Docs gates I ran at the exact head

I ran these on the clean clone at `eade77c9`, using a private virtualenv with the pinned renderer (`receipts/tool-versions.txt`: cmarkgfm 2025.10.22, html5lib 1.1).

| Gate | rc | Result |
|---|---|---|
| `docs_check.py` | 0 | 0 findings across 215 md + 1706 scrubbed files |
| `check_feature_status.py` | 0 | 0 findings |
| `check_doc_style.py` / `--selftest` | 0 / 0 | OK (25 current documents) / OK |
| `check_em_dash.py --base 6b66f66d` | 0 | 0 findings over 130 added lines in 3 pages |
| `check_doc_paths.py` | 0 | 1638 cited paths resolve |
| `gen_toc.py --verify-anchors` | 0 | 621 cross-page fragment links |
| `gen_toc.py --check` / `--selftest` | 0 / 0 | OK / 1501/1501 arms |
| `docs_inventory.py --check` | 0 | fresh |
| Mutant: AGENTS `#21-the-issue-to-merge-lanx` | 1 | `MISS AGENTS.md -> CONTRIBUTING.md#21-the-issue-to-merge-lanx`; restored |

The first pass of three gates returned rc 2 because the system interpreter lacked the pinned renderer. I re-ran them in the virtualenv, and `receipts/rc.txt` keeps only the valid runs.

After the probe, the worktree and index equal HEAD. HEAD is `eade77c95b997e5d9176b58e1f06266aea92c19f` and the tree is `e4c7e595...`. The gitlinks are unchanged (`receipts/clone-integrity.txt`).

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `CONTRIBUTING.md:423-514`; `AGENTS.md:298-303,404-411,436-437,475`; `CI_WORKFLOWS.md:273-281`; #665 x2 and #940 decisions; issue #940 body | R859-2 | eade77c95b997e5d9176b58e1f06266aea92c19f |
| RTL | CLEAN (inapplicable: docs only, no gitlink change) | `receipts/clone-integrity.txt`; `receipts/diff-ee5c6f92-eade77c9.patch` | R859-2 | eade77c95b997e5d9176b58e1f06266aea92c19f |
| Robustness | CLEAN | `CONTRIBUTING.md:447-514` paths; `AGENTS.md:298-303,475` | R859-2 | eade77c95b997e5d9176b58e1f06266aea92c19f |
| Tests | CLEAN | `receipts/rc.txt`; `receipts/probe_agents21_mutant.log`; `receipts/author-r3-manifest-check.txt` | R859-2 | eade77c95b997e5d9176b58e1f06266aea92c19f |
| Docs | CLEAN (residue R859-2-001) | `receipts/para_words.txt`; `receipts/mermaid-render.txt`; `receipts/gen_toc_verify.log`; `receipts/pr942.json` | R859-2 | eade77c95b997e5d9176b58e1f06266aea92c19f |

## Limits

- **Hosted runs:** at the time of reading, the exact-head runs showed 19 success, 22 skipped and 5 in progress (`receipts/hosted-check-runs.txt`). `docs-gates-0/1/2` were still in progress. `rtl-fast`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate` and the elaborate jobs had succeeded. Skipped contexts are not executed evidence. Hosted and act acceptance belong to the manager.
- **Gates not run:** I did not run the full docs workflow jobs, the builder legs, the RV32 SDK install or `--self-test` arms other than those listed. For those I rely on the author's step-by-step replay receipts (`gate-table.md`: five jobs, every job success). I verified that file's hash against the packet manifest but did not re-execute it.
- **Packet signature:** the evidence archive commit `07d93759` is unsigned (GitHub verification: `unsigned`). Integrity rests on `MANIFEST.json` hashes, which I checked for the nine author-r3 files I downloaded.
- **No manager source bank** runs at this head, and I neither claim nor infer one. Physical calibration was NOT RUN, and nothing here is hardware evidence.
- **Same-page fragments** are not gated in CI (#941). I relied on the author's heading-anchor walk (M0/M2) for `CONTRIBUTING.md#23-batched-merges`.

## Manager duties still pending

- Accept the hosted exact-head contexts once `docs-gates-0/1/2` finish, and the act replica.
- Build and validate the current-dev merge candidate at the merge turn, and link its receipts on the PR.
- Carry R859-2-001 to the residue checklist. R859-2-002, R859-2-003 and R859-005 are optional.
- Get explicit maintainer authorization before the merge, then run post-merge containment.
- Keep #940's follow-up open: check that review-integrity and containment judge ancestry-merged member PRs correctly after the first batch merge.

R859-2 FINISHED

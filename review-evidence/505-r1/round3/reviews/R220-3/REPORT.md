[R220] POSITIVE - exact head 5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7

Cold external targeted re-review R220-3 of PR #505 / issue #407 by the Opus reviewer, cleared context.

- **Base:** `b17580b91deb11f3441dfc5d7f9fafe539d929b8`. Live `dev` was still `b17580b9` at 08:58:07 UTC.
- **Head:** `5d45ecc0`, tree `2ec2d2e9931d250dacb945643cf3a444ec0e9a91`.
  - Its sole parent is the R220-2 head `ad62493186576144f9fa1568babad012bc9ad8ca`, whose parent `6af65a15` has the base as its sole parent.
  - The PR head and branch both resolve to `5d45ecc0`, and the PR is a draft.
  - The head descends directly from live `dev`, so the head tree is the candidate merge tree.
- **Diff since R220-2:** `git diff --raw ad624931 5d45ecc0` lists one entry: `docs/testing/CI_WORKFLOWS.md`, blob `00b1b852` to `89c221da`, 4 lines added and 2 removed in item 12.
  - The other 849 tracked non-gitlink files and all four gitlinks are identical (logs/00).
  - Base to head still changes only that page and `scripts/ci_events.py`.
- **Public sources read:**
  - AGENTS.md; CONTRIBUTING.md sections 3 and 6; docs/README.md (the CI policy entry); REQUIREMENTS.md section 8;
  - the #407 body and comments;
  - the #439 title, body and scope decision 5772547851;
  - the PR #505 body and thread through 5773795039: R220-2 5772521129, the F3 acceptance 5772548304, A163 REVIEW READY 5773079502, and A10 5773344355, 5773657048 and 5773795039;
  - CI_WORKFLOWS.md items 4, 11 and 12, the `--selftest` list, and the "One authoritative SHA" and Elaboration sections;
  - the rtl.yml gate job;
  - the relevant checker functions;
  - these files on the public `505-review-evidence` branch at `11bc4775`:
    - `round3/author/REVIEW-READY.md` and `round3/author/RESPONSE.md`;
    - `round3/manager` (candidate, builder integrity, the 40-command results, the draft replica receipts and the hosted snapshot);
    - `ac5/`, `ac5-act/` and `act-draft-fast/01.log`.
- **Not read:** R219's reports beyond their comment header lines (R219-3 included), R219 receipt files, the author's HANDOFF.md, and any private transcript.
- **Attribution:** "measured" means reproduced by R220-3, in the review clone or in a disposable scratch copy. Every other result is attributed to its owner.

**Why the verdict is POSITIVE:**

- R220-2 F3 (MINOR, Docs) is resolved at this head, under its original lens. The false sentence is gone and the replacement is true of the current tree, not merely tracked.
- Docs and Conformance were applied afresh at `5d45ecc0` and are clean.
- RTL, Robustness and Tests stay banked at R220-2 / `ad624931`, because nothing within their scope changed. They were not re-applied at this head.
- There is no open BLOCKER, MAJOR or MINOR. One new optional SUGGESTION concerns the PR description.
- A positive review does not complete the merge bar. The execution obligations listed below remain open.

## R220-F3 (MINOR, Docs): RESOLVED at 5d45ecc0

The finding stays under Docs. It is not relabeled, and it is not disposed of by the #439 link alone.

| Required outcome (R220-2) | Evidence at 5d45ecc0 |
|---|---|
| The residue statement names every recognized step whose script no rule pins. | CI_WORKFLOWS.md:768-771 names two gaps: the seven RTL jobs' scripts without specialized pins, and `full-ci-gate`'s "Print the event and pin the one SHA this run validates" (rtl.yml:54-64). See the census below this table. |
| The statement is true of the current tree. | Through the real CLI, three edits to the pin step each leave `--check` at `OK (1505 contract item(s))` (p2): deleting its checkout-HEAD mismatch block, replacing its `exit 1` with `true`, and dropping its `target_sha` line. So "remains unpinned" is accurate. |
| The pin-step gap has a public tracker. | #439 is open. Its title, body, AC1 and AC5 name the step, and the scope decision is 5772547851. The decision changes no #407 acceptance criterion. The prose now links #439 at :771. |
| The false sentence is corrected, not just tracked. | "The remaining content gap belongs to the seven RTL jobs" no longer appears at the head (`git grep`, p6). The remaining #407/#439 statements in docs and code comments were checked. None claims that the seven RTL jobs hold the whole gap (p6; ci_events.py:865-869, :1981-1992, :2016-2018). |
| The verification F3 named has been rerun. | Item 12 was re-read against a wider census (p1 replaces R220-2 p11). docs_check, gen_toc --check, check_doc_paths and check_em_dash --base b17580b9 all exit 0 (logs/03). ci_events --check and --selftest exit 0 (logs/01 and 02). |

**Census (p1).** p1 applies these levers to every `run:` step of the four workflow files, through the head's own `check()`:

- the body replaced by `true`;
- a command appended, and `set +e` prepended;
- for each normalized line: `|| true` appended, the line dropped, and the line replaced by `true`;
- each adjacent distinct pair of lines swapped.

Results at the head:

| Step class | Run steps | Levers | Accepted | Steps accepting any edit |
|---|---|---|---|---|
| Four non-RTL carriers | 56 | 788 | 0 | 0 |
| Siblings (gate, physical leg, fast selector, fast verdict) | 12 | 442 | 32 | 1: `full-ci-gate` step 2 |
| Seven RTL jobs | 37 | 865 | 599 | 25 |

- **Completeness.** No other step anywhere in the four files accepts a content edit, so "Both remaining content gaps" is the complete set. `.github/workflows/` holds no fifth file, and `uses:` steps stay held by their recorded `with`.
- **The pin step.** The only rule that reads its text is the presence check at ci_events.py:1786-1789: some gate step must mention `GITHUB_EVENT_NAME` and `GITHUB_SHA`. That rule refuses 3 of the 35 levers (`true`, and dropping or replacing line 2). It is not a script pin.
- **Detection control (p1b).** The same probe at base finds 450 accepted levers across 41 carrier bodies. The sibling and RTL-job results are identical at base and head, so the SHA-pin gap predates this PR.

## Findings at this head

[R220] SUGGESTION Docs - PR #505 description ("Known limitations / out of scope"; "Revision head") - the description still names ad624931 as the revision head, and lists only the seven RTL jobs' content gap
- **Requirement/evidence:**
  - AGENTS section 6, Docs: "The PR and Issue contain enough evidence for another cold reviewer."
  - The description (receipts/pr505_view.json) says "Revision head: `ad62493186576144f9fa1568babad012bc9ad8ca`".
  - Under known limitations it says: "The seven RTL jobs' remaining content gap belongs to #439."
  - The sibling SHA-pin gap that item 12 now names is absent from it.
- **Impact:**
  - Nothing reaches the merge result. The description is not committed; recent merge commits carry one- or two-line messages.
  - The thread (5773079502) and #439 carry the correct state, and R220-3 reconstructed the task from them.
  - A reader of the description alone sees a superseded head and an incomplete limitation list.
- **Optional change:** name `5d45ecc0` and add the `full-ci-gate` SHA-pin step to the known-limitations line, matching CI_WORKFLOWS.md:768-771.
- **Verification:** re-read the description against item 12.
- **Coverage:** a SUGGESTION, so it does not affect Docs coverage.

**Carried from R220-2.** The SUGGESTION under Robustness (a traceback on a malformed pristine tree at ci_events.py:7439 and :7476) was not adopted (5772548304). It still fails closed and is optional.

**Context, not a finding against this diff:**

- **"Machine-checked" wording.** "One authoritative SHA" (CI_WORKFLOWS.md:917-922) and the comment at ci_events.py:1782 are unchanged since base. They describe the workflow's run-time refusal, which the current rtl.yml:60-63 performs.
- **Scope paragraph.** The `--check` scope paragraph (:961-968) does not claim the pin step's script is held.
- **Tracker.** The #439 decision owns their wording when the pin lands.
- **E3.** Dropping the `target_sha` publication (p2) is one more edit `--check` accepts today. #439 AC1's content pin covers it, so no further tracker is needed.

## Lens results at 5d45ecc0 (applied this round)

[R220] PASS Docs - docs/testing/CI_WORKFLOWS.md:768-777, :635-656, :897-908 and :1053-1057 (blob 89c221da); scripts/ci_events.py:865-869, :1981-1992 and :2016-2018; logs/p1-content-gap-census.json, logs/p2-cli-sha-pin-edits.log, logs/p6-residue-claims-grep.log, logs/03-doc-gates-head.log, logs/04-docs-check-no-git.log - every documentation statement the PR adds or changes was checked against the head's measured behaviour

- **Item 12 (:768-777).**
  - Both named gaps exist, and they are the only ones (p1, p2).
  - "The four non-RTL carriers now pin every recognized script": 56 of 56 bodies refuse every lever.
  - The second runner's `--check` holds these pins (rtl.yml:92-95).
  - The AC5 consequence sentences match the retained measurement (see the AC5 section).
- **Item 11 (:635-656).** Each claim was checked against the head:
  - normalized comparison (ci_events.py:3574-3591);
  - refusals that name the job, step and first differing line (p2 C1);
  - missing records fail closed;
  - live-derived arms: 456 carrier arms, one `|| true` per normalized line (117 non-last plus 56 last), 56 appended-command, 56 `true`-replacement, 56 `continue-on-error`, 40 dropped-command, 40 reordered-lines and 35 dropped-flag (p5);
  - the same-commit maintenance remedy.
- **Other changed text.**
  - The `--selftest` list (:897-908) matches the arm kinds above.
  - The shape-gate paragraph (:1053-1057) matches the canonical records of docs-check steps 41-43 (p5).
- **Doc gates.** All exit 0 (logs/03, logs/04):
  - docs_check: 0 findings over 163 md and 826 scrubbed files, and the no-git carrier is also 0;
  - check_em_dash: 0 over 49 added lines from b17580b9, and 0 over 4 from ad624931;
  - gen_toc --check, --verify-anchors and --selftest;
  - check_doc_paths: 824 paths resolve;
  - check_doc_style, check_feature_status, the traceability matrix, check_archive, check_baremetal_only and DOC_MAP;
  - `git diff --check` from both bases.
- **Rendering.** The new paragraph keeps item 12's 4-space list continuation. No obsolete wording is restored.

[R220] PASS Conformance - issue #407 AC1-AC5 and decision 5770808527; issue #439 AC1/AC5 and decision 5772547851; CI_WORKFLOWS.md:635-656 and :768-777; scripts/ci_events.py:3574-3591 and :3651-3652; logs/01, 02, 03, p1, p1b, p2, p3, p4, p5 - each acceptance criterion holds at 5d45ecc0, and the correction changes no criterion and implements no #439 work

- **AC1.**
  - All 56 recognized carrier `run` bodies refuse all 788 content levers.
  - The same probe detects 450 accepted levers at base (p1, p1b).
  - A refusal names the job, the step number and name, and the first differing line (p2 C1).
- **AC2.**
  - The arm population at the head is the one R220-2 verified, with the same composition (p5).
  - That includes `docs-check step 34 or-true-line-1`, the AC5 arm.
  - The flag-less builder and no-git bodies carry no flag arm, as recorded publicly in 5770873818.
- **AC3.** `--check` is OK over 1505 items, and `--selftest` passes with 1144 arms (logs/01 and 02).
- **AC4.**
  - Item 12 names no carrier content as open.
  - Item 11 states the pins, their cost and the remedy.
  - docs_check, gen_toc --check and check_doc_paths exit 0.
- **AC5.** Met by the retained measurement at 6af65a15; see below.
- **No criterion changed.**
  - The corrected sentence stays within #407's out-of-scope boundary ("the seven RTL jobs") and within #439's settled scope.
  - The checker, the workflows, the normalization, the canonical records and the mutation population are unchanged: blob ids, the AST comparison in p4, and the arm composition in p5.
- **REQUIREMENTS section 8.** REQ-VER-04's documentation, feature-status, traceability and bare-metal gates are green with zero findings at the head (logs/03).

## Banked lenses: R220-3 accepts R220-2 coverage at ad624931

RTL, Robustness and Tests were covered clean by R220-2 at `ad62493186576144f9fa1568babad012bc9ad8ca`, the parent of this head. They were not re-applied here. This evidence shows that nothing within their scope changed between `ad624931` and `5d45ecc0`:

- **Tree.** `git diff --raw` lists only the policy page. These blobs are identical: docs.yml `f5a45401`, elaborate.yml `54c71a04`, rtl-fast.yml `f7c502c9`, rtl.yml `8510159e`, act_ci.py `794794b1` and ci_events.py `b90ae46b`. No gitlink changed (logs/00).
- **Checker (p4).** ci_events.py is AST-identical: 333 of 333 functions and every module-level statement.
- **Pristine behaviour.** The one changed file is prose that `--check` reads as POLICY. At this head `--check` stays OK over the same 1505 items, and `--selftest` passes the same 1144 arms (logs/01 and 02). So neither the pristine verdict nor the self-test population moved.
- **What these head-level results are.** They are evidence of no change in scope. They are not a new application of those three lenses.

## Prior findings

| Item | Lens | State at 5d45ecc0 | Evidence |
|---|---|---|---|
| F1: the shape-gate paragraph said "not pinned yet (#407)" (R219 F1 and R220 F1) | Docs | Resolved; no regression | `git grep "pinned yet"` finds nothing (p6). :1053-1057 is unchanged since ad624931. Steps 41-43 have canonical records, and every lever is refused on them (p5, p1). |
| F2: only the last line of a body had a swallowing arm (R220 F2) | Tests, Conformance | Resolved; no regression | ci_events.py is byte-identical to ad624931. 117 `or-true-line-N` arms are present, including the AC5 line (p5), and `--selftest` passes with 1144 arms. |
| F3: the item-12 residue sentence (R220 F3) | Docs | Resolved | See the section above. |

## AC5: retaining A10's measurement at 6af65a15

**Attribution.** The measurement is A10's.

- It ran the standard trusted live-dev runner on scratch PR #506 at `66ba2106`. That commit's sole parent is `6af65a15`, and its only change is `|| true` on docs.yml:323.
- Both invocations exited 1 as workflow failures, not with setup refusal exit 2. Both completed their cleanup.
- PR #506 is closed and was never merged.

**What R220-3 did with the receipts (p3).**

- R220-3 re-hashed the archived receipts. The AC5 blobs are unchanged at evidence commit `11bc4775`.
- The published `ac5/verify_receipts.py` exits 0 on them.
- R220-3 re-read these raw lines:
  - 01.log:1837: the idiom step succeeds;
  - 01.log:1902-1904: the contract step fails over 1505 items;
  - 01.log:1909: the docs-check job fails;
  - 02.log:37-39 and :44: `full-ci-gate` fails;
  - 02.log:88/99/105 and :149/161/167: both aggregates fail closed on zero shards.

**Decision: retention stays valid at 5d45ecc0.** The evidence:

- **Workflows and runner.** The AC5 path's workflow files and act_ci.py are byte-identical at 6af65a15, ad624931 and 5d45ecc0.
- **Checker.** Every ci_events.py function reachable from `check()` or `run_check()`, and every module-level statement, is AST-identical from 6af65a15 to 5d45ecc0. Only the two self-test-only arm generators differ (p4).
- **Policy page.** It is the only changed input on the path. Under the identical AC5 edit, the head's real CLI reports a finding byte-identical to 01.log:1902 and 02.log:37, over the same 1505 items (p2 C1, p3).
- **Pristine docs path.** At this head the pristine docs path passes. A10's draft replica at `5d45ecc0` has docs-check succeed, with its contract step `OK (1505)` and `PASS (1144)`. The hosted docs-check succeeded at 08:05:44 UTC. Both are attributed.

This remains a measurement at 6af65a15. It is not an act execution at 5d45ecc0, and this report does not present it as one.

## Completion ledger (reviewer-owned, R220-3)

| Lens | Covering round | Head | State |
|---|---|---|---|
| Conformance | R220-3 | 5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7 | covered clean (applied at this head) |
| Docs | R220-3 | 5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7 | covered clean (applied at this head; F3 resolved; one SUGGESTION) |
| RTL | R220-2 | ad62493186576144f9fa1568babad012bc9ad8ca | covered clean; banked, since nothing in scope changed through 5d45ecc0 |
| Robustness | R220-2 | ad62493186576144f9fa1568babad012bc9ad8ca | covered clean (one optional SUGGESTION); banked on the same evidence |
| Tests | R220-2 | ad62493186576144f9fa1568babad012bc9ad8ca | covered clean; banked on the same evidence |

- Every ledger head is the candidate itself or its parent, and the parent has no in-scope change since.
- A later commit touching the checker, a workflow file or act_ci.py un-covers RTL, Robustness and Tests. Any change to CI_WORKFLOWS.md or the checker un-covers Docs and Conformance.
- This ledger is R220's. R219-3's verdict is separate, and CONTRIBUTING's two-positive rule is judged by the manager.

## Execution and merge obligations not judged here

None of these is called PASS in this report:

- **Full native validation at 5d45ecc0.** A10 reported it still running at 08:57 UTC (5773795039), and no receipts are published.
- **Ready-state replicas.** The trusted act replicas for all four workflows at the ready head are pending.
- **Hosted exhaustive contexts.**
  - At 5d45ecc0 (draft), `verilator-suites` and `yosys-portability` were SKIPPED on the no-op path. That is not exhaustive evidence.
  - `ci_scope.py` answers `rtl=true` for this change set (logs/05), so the ready head owes both.
- **The rest of the bar:** candidate-merge validation against the then-live `dev`, post-merge containment, and closing #407 to Done. An agent merges only under the maintainer authorization the PR cites, after the full bar.

**Attributed, not reproduced:**

- **A10 static and builder evidence** (evidence commit `ffdfe935`):
  - 40 commands exit 0 at 5d45ecc0, with candidate tree equal to head tree;
  - builder gate 11 is reported NOT RUN.
- **A10 draft replica** (`11bc4775`), at 5d45ecc0 with `draft=true`: docs, rtl-fast and elaborate PASS, exit 0, cleanup at 10:36:31 CEST.
- **Hosted fast contexts at 5d45ecc0** (GitHub state at 08:53:59 UTC): docs-check, docs-check-no-git, wire-accountability, elaborate, full-ci-gate, changes, verilator-lint, bdd-conformance, yosys-elaboration and rtl-fast succeeded.
- **A163's author evidence** (`d1c7f12f`).

## Gates run by R220-3 at 5d45ecc0

These exit 0 (logs/01-05):

- `ci_events.py --check` (1505 items) and `--selftest` (1144 arms);
- docs_check, in the clone and on a `.git`-less copy;
- check_em_dash `--base` b17580b9 and ad624931, plus `--selftest`;
- gen_toc `--selftest`, `--verify-anchors` and `--check`;
- check_doc_paths;
- check_doc_style and its `--selftest`;
- check_feature_status and its `--self-test`;
- `gen_module_matrix.py --check`;
- check_archive and its `--selftest`;
- check_baremetal_only `--check` and `--selftest`;
- `DOC_MAP.gen.py --check`;
- `git diff --check` from b17580b9 and from ad624931;
- `ci_scope.py` over the changed-file set.

## Evidence limits

- **Not run by R220-3:**
  - act or Docker;
  - hosted runs;
  - the full parent RTL sweep, Yosys, the processor suites, gPTP make, behave, the builder, lint and xvlog;
  - gates that need initialized submodules;
  - `act_ci.py --selftest`, since the candidate's copy is not run on the host.
- **Submodules:** all four were uninitialized (`-`) at entry and at exit, and R220 did not initialize them. The checker and the doc gates run here do not read submodule trees.
- **Run-time effect:** p1 and p2 are static checker measurements. R220-3 ran no workflow to observe the run-time effect of the pin-step edits.
- **Probe hygiene:** probes ran on in-memory worlds or on disposable `git archive` copies, plus a sparse clone of the public evidence branch, all under `/tmp/r220-3-scratch`. These were removed at exit.
- **Independence:** R220 did not contact the author or R219.

## Integrity

At exit, the clone is unchanged (logs/99-exit-integrity.log):

- HEAD is `5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7`, with tree `2ec2d2e9`.
- `git status --porcelain=v2 --untracked-files=all --ignored` is empty.
- The sha256 of `git ls-files -s` equals its entry value, `2cd50841...`.
- The index equals HEAD, and the worktree equals the index.
- All 850 tracked non-gitlink files re-hash to their index blobs, with matching file modes (core.filemode=true).
- No assume-unchanged or skip-worktree flag is set, and there is no `__pycache__`.
- `git submodule status` is unchanged from entry: all four gitlinks are uninitialized at their recorded commits.

No commit, push, public write, PR metadata change, merge, install, privileged action, hardware access or subagent was made.

## Receipts

`README.md` beside this report lists the layout and the reproduction commands:

- `logs/`: entry and exit state, gate runs, and the outputs of probes p1-p6;
- `probes/`: p1-p6 and p9;
- `receipts/`: snapshots of the public state, and the blob ids with re-hash results of every archived evidence file read.

R220-3 FINISHED

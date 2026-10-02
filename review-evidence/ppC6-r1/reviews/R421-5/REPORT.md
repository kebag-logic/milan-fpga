[R421] POSITIVE - exact head 95a78c099ee5aa914521975355adc1dfef99d01c

# R421-5: body-only re-review of processor PR #139 (lane C6, notifications and Identify)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #80, PR #139 (closes #54, #58, #80, #86).
- Exact head `95a78c099ee5aa914521975355adc1dfef99d01c`, tree `d0be0f91665f4e6b8e16bfa3aa8f53bbeaff518f`. The head is unchanged since round 4: the API and GraphQL `headRefOid` both report it (`receipts/clone_verification.txt`, `receipts/rendered_links.txt`).
- Public review start: PR #139 comment 5950042993.
- Scope, as assigned: only the delta after my round-4 NEGATIVE (R421-4 F1, MINOR, Docs: the condensed PR body drops recorded earlier-round figures). The delta has three parts:
  1. the manager's ruling (PR #139 comment 5948641217, outcome (b)) and its follow-up (comment 5950041174), with the PR-body edit they describe;
  2. that nothing else in the body changed;
  3. the corrected sentence in `author-r4b/HANDOFF.md` (evidence `a6ea796e`) and its manifest digest (evidence `2a98e7d4`).

  The code, tests and merges are unchanged since round 4, when I found them sound. They were not re-reviewed.

## Verdict

**POSITIVE.** This round has no MINOR, MAJOR, BLOCKER or RESIDUE finding. R421-4 F1 is resolved, and so is the same finding from the other reviewer (R420-4 F1).

Outcome (b) is implemented as the ruling states it:
- **Pointers.** Each of the four condensed validation sections now opens with a pointer:
  - "Validation" (round 1);
  - "Validation, round 2";
  - "Validation, round 3";
  - "Validation, round 4".
- **One link target.** All four pointers resolve, through one link definition at the end of the body, to `review-evidence/ppC6-r1/author-r4/PR-BODY.md` at evidence commit `ca50262850d156308a45ce5237e9adff64419f89`.
- **Linked file is my reference.** The linked file is byte-identical to the round-4 body I used as my reference at round 4: sha256 `a72a4fde…`, git blob `8b028649`.
- **Every dropped figure is there.** All 61 figures my round-4 receipt lists as dropped occur in the same round's validation section of the linked file. So do all 61 items the other reviewer lists.
- **Tables are verbatim.** The round-1, round-2 and round-3 validation sections in the linked file are byte-identical to the same sections in the round-1, round-2 and round-3 bodies where those tables first appeared.
- **Nothing else changed.** The live body equals `author-r4b/PR-BODY.md` plus 11 inserted lines and no other change. Those lines are the four pointer sentences, their blank-line separators, and the link definition. The body has had exactly one edit since round 4b.
- **Handoff and manifest.** The handoff sentence is corrected, and the manifest records its new digest.

## What I checked

| # | Check | Result | Receipt |
|---|---|---|---|
| 1 | The linked file against my round-4 reference copy (`../ppC6-r421-4-packet/receipts/pr_body_round4_author_packet.md`, archived as `reviews/R421-4/receipts/pr_body_round4_author_packet.md` at `ca502628`) | byte-identical, sha256 `a72a4fde…`. The blob `8b028649` is the same at `72483b72` (archived), `ca502628` (linked) and `2a98e7d4` (branch tip). | `receipts/linked_vs_r421-4_reference.txt`; `receipts/evidence/author-r4_PR-BODY_ca502628.md` |
| 2 | The link resolves publicly | Raw fetch at `ca502628`: same sha256 `a72a4fde…`. Blob URL: HTTP 200. `ca502628` is an ancestor of the public branch `ppC6-review-evidence` (tip `2a98e7d4`). | `receipts/link_target_check.txt` |
| 3 | The pointers render as links | GitHub's rendered `bodyHTML` has 4 anchors "full tables" to that URL. No unresolved `[c6-r1-r4-tables]` is left, and the definition does not show as text. | `receipts/rendered_links.txt` |
| 4 | Each pointer opens its section, and each named section exists in the linked file | In the live body, each pointer is the first paragraph under its heading: "Validation" :104/:106, "Validation, round 2" :238/:240, "Validation, round 3" :327/:329, "Validation, round 4" :384/:386. Round 4b's own "Validation, round 4b" (:445) has no pointer and is not condensed. Linked body headings: `## Validation` at :102, `### Validation, round 2` at :269, `### Validation, round 3` at :401, `### Validation, round 4` at :498. | `receipts/body_delta_live_vs_r4b.txt`; `receipts/section_verbatim.txt` |
| 5 | My figure comparison, re-run against the linked file (`scripts/dropped_in_linked.py`) | Round 1: 5 of 5. Round 2: 15 of 15. Round 3: 21 of 21. Round 4: 20 of 20. Each was found in the same round's validation section of the linked body; 0 absent. Re-running my round-4 `scripts/pr_body_figures.py` (linked body → live body) gives the same dropped lists as at round 4, so the edit removed no further figure. | `receipts/dropped_figures_in_linked.txt`; `receipts/r421-4_pr_body_figures_per_round.txt` |
| 6 | "Verbatim": each earlier round's tables in the linked file against the body where they first appeared (`scripts/section_verbatim.py`) | "Validation" is identical in the round-1, 2, 3 and 4 bodies (4,213 chars, 38 table rows). "Validation, round 2" is identical in the round-2, 3 and 4 bodies (5,671 chars, 43 rows). "Validation, round 3" is identical in the round-3 and 4 bodies (5,499 chars, 37 rows). Round 4's own tables are in the linked file (round 4's body), and the live body condenses them. | `receipts/section_verbatim.txt` |
| 7 | The other reviewer's R420-4 F1 items, as strings, in the linked sections | 8/8, 19/19, 17/17 and 17/17 present, 0 missing. This was run after my verdict was recorded. | `receipts/r420-4_f1_strings_in_linked.txt` |
| 8 | Live body against `author-r4b/PR-BODY.md` (`scripts/body_delta.py`) | 0 replaced or deleted lines; 5 insert hunks (11 lines). Removing the inserted lines gives the archived body byte for byte. The archived body is 64,316 chars; the live body is 65,196 chars (+880; `wc` shows 65,197 because of the fetch's trailing newline). The headroom is 340, as the ruling says. | `receipts/body_delta_live_vs_r4b.txt`; `receipts/pr_body_live.md` |
| 9 | Body edit history (GraphQL `userContentEdits`) | 5 edits in total. The 07:24:17Z edit equals `author-r4b/PR-BODY.md` (sha256 `173c49ca…`), and the only later edit (08:58:02Z) equals the live body. So there was no intermediate edit. | `receipts/body_edit_history.txt` |
| 10 | Handoff correction, `ca502628` → `a6ea796e` | One file, +3/−2, inside the `## PR-BODY.md` paragraph only. "paragraphs carrying the same figures" became "paragraphs that keep only some of their figures", with a dated manager-correction note. The note says the full tables, verbatim, are in `../author-r4/PR-BODY.md` and that the PR body links them from each condensed round. Checks 1 to 6 confirm both claims. The file's last line ("64,316 characters … 1,220 under") describes the archived `author-r4b/PR-BODY.md`, which is unchanged, so it is still true. | `receipts/evidence/author-r4b_HANDOFF_ca502628.md`; `receipts/evidence/author-r4b_HANDOFF_a6ea796e.md` |
| 11 | Manifest digest at `2a98e7d4` | The `author-r4b/HANDOFF.md` `published_sha256` changed from `bbc5df58…` (the pre-correction file) to `062510e3…`, which equals the corrected file. `author-r4/PR-BODY.md` and `author-r4b/PR-BODY.md` digests match their files. Between `ca502628` and `2a98e7d4`, the only author entry that changed is `author-r4b/HANDOFF.md`; the other changes are the archive of the other reviewer's round-4 packet. The HANDOFF bytes are the same at `a6ea796e` and `2a98e7d4`. | `receipts/manifest_digest_check.txt` |
| 12 | Clone integrity | HEAD and tree are exact; the status is empty; the index equals the tree (sha256 over mode/blob/path lists `7daa950c…` both). The head has no submodule gitlinks. No tracked file was modified: no probe was needed in this round. | `receipts/clone_verification.txt` |
| 13 | Hosted checks at the head (read-only, for context) | 6/6 completed `success`: `suites`, `docs-gates` and `portability`, each on both events. | `receipts/hosted_checks_95a78c0.txt` |

Reconstruction order was followed:
- **Repository rules and docs.** The head has no `AGENTS.md` or `CONTRIBUTING.md`. `docs/README.md` holds the authoring conventions.
- **Issue #80.** It is still open. It has no comment after the REVIEW READY comment 5947318179, so the scope this round comes from the ruling and follow-up on PR #139 (`receipts/comment_5948641217.md`, `receipts/comment_5950041174.md`, `receipts/comment_5950042993.md`).

## Findings

None. This round has no BLOCKER, MAJOR, MINOR or RESIDUE finding, and no new SUGGESTION.

One candidate was checked and dropped. The corrected handoff sentence now has two parentheticals in a row ("…some of their figures (manager correction …) (round 1: processor and parent tables; …)"). It reads clumsily, but it is accurate: the second parenthetical still lists the tables that became paragraphs. Nothing in it is wrong, so I raise no wording defect.

## Prior public review findings at this head

I read these only after recording my verdict and ledger (`receipts/verdict_before_prior_findings.txt`, 10:14:52Z).

| Finding | State at 95a78c09 | Evidence |
|---|---|---|
| R421-4 F1 (MINOR, Docs: condensed body drops figures) | **Resolved** by outcome (b), ruled in comment 5948641217. Its verification for (b) holds: each of the four paragraphs carries the pointer, and the linked file holds the tables. The handoff sentence is corrected. | checks 1-6, 8, 10, 11 |
| R420-4 F1 (MINOR, Docs: the same defect) | **Resolved.** Comment 5950041174 records that ruling 5948641217 covers it, which is the finding's own alternative: "link each condensed section to the archived full body at a pinned evidence commit, and record that ruling". Every item it lists is in the linked sections. | check 7 |
| R420-4 S1 (SUGGESTION: `sim_main.cpp` harness comment names two of four builds) | **Open, retained.** The code is unchanged, and the item is outside this delta and non-gating. | the head is unchanged |
| R420-3 S1, R421-3 S1 (SUGGESTIONs) | **Open, retained**, as recorded at round 4. The code is unchanged and they are non-gating. | the head is unchanged |
| R420-1 F1/F2, R421-1 F1, R420-2 F1, R421-2 F1 (MINOR) | **Still resolved.** I verified this at round 4 (R421-4), and the code is unchanged since. | R421-4 packet, archived as `reviews/R421-4` at `ca502628` |

## Lens results

- **Conformance: CLEAN.** The delta makes no clause or conformance claim. The body's design text and clause references are byte-unchanged (check 8).
- **RTL: CLEAN.** No RTL changed: the head is identical to round 4, where RTL was CLEAN.
- **Robustness: CLEAN.** No code or test changed, so no new robustness surface exists. The body edit adds no behavioural claim.
- **Tests: CLEAN.** No test changed. The test figures in the record are preserved: 61 of 61 dropped figures are in the linked tables, and no further figure was removed (check 5).
- **Docs: CLEAN.** R421-4 F1 is resolved. The pointers resolve and render. The linked record holds the tables verbatim and is pinned to an immutable commit. The handoff sentence is accurate, and its manifest digest matches.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | live PR body vs `author-r4b/PR-BODY.md` (insertions only; clause text unchanged); code unchanged since R421-4 | R421-5 (delta); R421-4 (code) | `95a78c099ee5aa914521975355adc1dfef99d01c` |
| RTL | CLEAN | head and tree identical to R421-4's; no RTL in the delta | R421-4; R421-5 confirms the head | `95a78c099ee5aa914521975355adc1dfef99d01c` |
| Robustness | CLEAN | no code or test in the delta; body edit adds no behavioural claim | R421-4; R421-5 confirms the head | `95a78c099ee5aa914521975355adc1dfef99d01c` |
| Tests | CLEAN | 61/61 dropped test and gate figures located in the linked tables; no further figure dropped by the edit | R421-5 (record); R421-4 (execution) | `95a78c099ee5aa914521975355adc1dfef99d01c` |
| Docs | CLEAN | live PR body (4 pointers, 1 link definition, rendered anchors), `author-r4/PR-BODY.md` at `ca502628`, `author/`, `author-r2/`, `author-r3/` bodies, `author-r4b/HANDOFF.md` at `ca502628`/`a6ea796e`/`2a98e7d4`, `MANIFEST.json` at `ca502628`/`a6ea796e`/`2a98e7d4`, body edit history | R421-5 | `95a78c099ee5aa914521975355adc1dfef99d01c` |

## Real limits

- **Body-only round, as assigned.** No build, suite, campaign, probe or Verilator run was made in this round. Code, tests and merges rest on R421-4 at this same head and tree.
- **Ruling not re-litigated.** Whether outcome (b) satisfies "keeps every figure" was the manager's ruling. I verified the ruling's implementation and did not revisit the ruling itself.
- **The live body is only in public comments and this packet.** The evidence repository's `author-r4b/PR-BODY.md` is the pre-pointer body (64,316 chars). The live 65,196-character body is described in the ruling comment and kept verbatim in `receipts/pr_body_live.md` of this packet; it has no author-archive copy.
- **Hosted CI was only read.** I read the hosted check runs and did not execute them.
- **No hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Hosted/act acceptance and the final current-dev candidate at the merge turn: source base `03c842a780064048b0a1a3de29214174a1c13934`, live dev `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- The open SUGGESTIONs: R420-4 S1, R420-3 S1 and R421-3 S1, all non-gating.
- Optionally, archive the live 65,196-character PR body next to `author-r4b/PR-BODY.md`. The evidence record would then hold the body as merged.
- The second independent positive review and the remaining completion bar before merge.

R421-5 FINISHED

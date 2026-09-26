[R327] POSITIVE - exact head 9143e21a57e6315c7678430cfc45b4a2b7e10c09

# R327-2 external independent review: issue #567 / PR #569

Round: R327-2 (delta round). Head `9143e21a57e6315c7678430cfc45b4a2b7e10c09`, tree `12bc47c065c23b6a8a2a9ab766ca0b63f533d3ad`, parent `54b4c3bbbc8cdea5ced0be29c9226fdf82233b74`.
Source base and live `dev`: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
The PR head read publicly is `9143e21a`, not a draft (`receipts/pr_body_check.txt`).

I reconstructed the task from public sources in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The issue #567 body, acceptance 1-4 and the A10 decisions (Round 2 ledger 5845149786, Round 3 text 5845274184, Round 4 assignment 5845507642).
4. The A335 TAKEN and REVIEW READY comments.
5. The PR #569 body.
6. `syn/yosys/ooc.sh:370-396,463-470` and `syn/yosys/rom_digests.tsv`.
7. The diffs `7eb3b0d4..9143e21a` and `54b4c3bb..9143e21a`, and the history.
8. The manager's public evidence tree at `270ee694` (`review-evidence/567-r1`) and the exact-head hosted check runs.

I read prior review findings (R326-1, R327-1) only after my own pass over the delta was complete and the findings below were drafted.

The verdict is POSITIVE. The delta is one commit that changes two Markdown files (+3/-2). It resolves R327-1 F1 and applies S1. The PR body no longer carries the stale S3 lines. Every path outside the two documents is byte-identical to `54b4c3bb`, including all four gitlinks. No BLOCKER, MAJOR or MINOR finding is open. One new SUGGESTION is recorded, and it does not affect coverage.

## Delta under review

| Commit | File | Change |
|---|---|---|
| `9143e21a` | `tb/verilator/milan_dp/README.md:468` | "then restore `990f9652`" becomes "then restore the pin of record". "The same fixture passes at the restored pin." becomes "The same fixture passed at `990f9652`, the measurement pin." |
| `9143e21a` | `docs/reference/SUBMODULES.md:57-58` | "OOC synthesis requires rows for every pin." becomes "OOC synthesis requires ledger rows for the pin of record. Rows must match that exact pin." |

- The commit message is one line with no body or trailers.
- My `git diff 54b4c3bb 9143e21a` is byte-identical to the author's published `author-r4/receipts/round4.diff` (`receipts/delta_54b4c3bb_9143e21a.diff`).

## Findings

No BLOCKER, MAJOR or MINOR.

### S1: SUGGESTION (Docs): a pre-existing row label calls `424c688f` "the previous processor pin"

- **Location:** `tb/verilator/milan_dp/README.md:470`, first cell: "the previous processor pin `424c688f`".
- **Authority/evidence:** the pin of record is `0922e434`, and the previous pin is `990f9652` (`docs/reference/SUBMODULES.md:42`). The label is relative to when commit `8eca7031` wrote it (2026-09-24). It is byte-identical at base `7eb3b0d4` and is not touched by this PR. The section's preface (`:459`) says "The #530 rows retain their dated evidence". The row's instruction is already pin-neutral ("then restore the pin"). So, unlike R327-1 F1, the row gives no wrong restore target.
- **Impact:** cosmetic. A reader may mistake the label for the pin before `0922e434`.
- **Suggested outcome:** optional, and outside #567's frozen scope. On a later touch of this section, give a dated label such as "the #530-era processor pin `424c688f`". Record it as a new Issue if the manager wants it tracked.
- **Verification:** `git grep -n "previous processor pin"` shows no relative pin label that disagrees with `SUBMODULES.md`.

## Round 4 focus items, checked

1. **F1 (R327-1 MINOR, Docs and Conformance): RESOLVED.** `git grep -n 990f965` has 12 hits (`receipts/grep_990f965.txt`), and none is an instruction or a current-state statement:
   - `CHANGELOG.md:14,72,74` are the earlier #508 entry.
   - `CHANGELOG.md:36,45` record the #567 transition and the digest comparison.
   - `SUBMODULES.md:42` says "the previous pin", and `SUBMODULES.md:55` is the digest comparison.
   - `rom_digests.tsv:32-33` are retained ledger rows.
   - `README.md:442` is dated measurement provenance ("Measured ... at processor pin `990f9652`").
   - `README.md:468` now names the restore target as "the pin of record" and uses `990f9652` only in the past-tense measurement clause.
   - `README.md:552` holds two fixed permalinks. `05_acmp_engine.md` has the same blob at both pins. `06_aecp_engine.md` differs, but no diff hunk touches the F06.13 anchor at line 297 (`receipts/probes.txt` P4). The permalinks select no checkout revision.

   Executed restore step (`receipts/probes2.txt` P6/P6b): I repinned the processor checkout to `7a47f578`, then restored it to the superproject gitlink. The checkout then equals `0922e434` and is clean. In this offline clone, `git submodule update` tried a fetch because no ref reaches the pin and file transport is disabled. This is an artifact of the clone, not a document defect: the README names the target, not a command. The restore was completed with an explicit checkout of the gitlink.

2. **S1 (R327-1 SUGGESTION): APPLIED with a justified wording adaptation.**
   - "Pin of record" is the tool's own term: `ooc.sh:370-396` `submodule_pin_of_record` returns the superproject gitlink and refuses a mismatched checkout. `ooc.sh:463-470` looks up rows by exact `$1 == pin` and refuses when they are absent. The two sentences state exactly that.
   - P1 shows that the assigned 11-word sentence fails the unchanged style gate: "sentence has 11 words; maximum is 10", rc 1. The head bytes pass with rc 0.
   - P2 shows one row per image for the gitlink `0922e434`, both equal to the `990f9652` rows. Removing those rows from a copy of the ledger empties the lookup, which is the branch `ooc.sh` refuses on.

3. **S3 (R327-1 SUGGESTION): RESOLVED.**
   - The PR body contains neither "The branch remains unpublished" nor "Round 3 documentation evidence is posted on the issue for the candidate head".
   - Its status section names this exact head, and "Known limitations" lists the review, hosted, candidate-merge and containment steps as pending, which is accurate.
   - `Closes #567` is retained (`receipts/pr_body_check.txt`, body sha256 `00a349cd...`).
   - The status line calls the head "local head", although the head is now published. That wording is harmless and is not a finding.

4. **S2 (R327-1 SUGGESTION):** filed as #571 ("Bind N_AUDIO_UNIT_P, N_CLK_DOMAIN_P and N_CONTROL_P from the entity model", OPEN). It remains a SUGGESTION, out of scope.

5. **Docs gates pass at this head** (`receipts/docs_gates/summary.txt`, locked renderer set `cmarkgfm==2025.10.22` / `html5lib==1.1` in a disposable environment). Every command below returned rc 0:

   | Gate | Result |
   |---|---|
   | `docs_check.py`, Git mode | 0 findings over 166 md + 884 files, scrub 23/23, routing 4/4 |
   | `docs_check.py`, metadata-free `git archive` export | 0 findings, 22/22, 4/4; inventory parity skipped because it needs Git (not counted as a pass) |
   | `check_em_dash.py --base 7eb3b0d4...` | 0 findings over 44 added lines, arms 339/339 |
   | `check_doc_style.py` | 22 current documents, which include `SUBMODULES.md` |
   | `gen_toc.py --check` | 108 lists |
   | `gen_toc.py --verify-anchors` | 176 links |
   | `check_doc_paths.py` | 847 paths |
   | `check_submodule_docs.py` | 4 exact gitlinks |
   | `submodule_boundaries.gen.py --check` | pass |
   | `check_diagram_pngs.py` | 6 PNGs |
   | `git diff --check`, worktree and `7eb3b0d4..HEAD` | clean |

6. **Nothing else changed.** P5 (`receipts/probes2.txt`): `git ls-tree -r` of `54b4c3bb` and `9143e21a`, excluding the two documents, is identical at 910 entries (modes, blob ids, gitlink ids). The only changed paths are the two documents.

## Per-lens results (all applied at 9143e21a)

- `[R327] PASS Conformance — issue #567 acceptance 1-4; A10 Round 4 assignment 5845507642; tb/verilator/milan_dp/README.md:442,468,470,520,552; docs/reference/SUBMODULES.md:25,42-58; syn/yosys/ooc.sh:370-396,463-470; rom_digests.tsv:7-8,32-33 — the F1 restore target is now the pin of record; git grep 990f965 has no instruction or current-state hit; README:520 names 0922e434 as the adopted pin, and 990f9652 is its ancestor; SUBMODULES.md:57-58 matches the gitlink-keyed exact-row lookup (P2); acceptance 2-4 and the gitlink are byte-identical to 54b4c3bb (P5), so the R326-1/R327-1 acceptance evidence carries to this head unchanged`
- `[R327] PASS RTL — git ls-tree 54b4c3bb vs 9143e21a (P5); git diff --name-only 7eb3b0d4..9143e21a (no hdl/, scripts/, syn/*.sh or tb/ source path); protocol-processor hdl tree d8879608 at 990f9652 and 0922e434 (P3) — this round changes no RTL, gitlink, synthesis script or source list; every RTL-scope artifact is byte-identical to the head where R327-1 ran elaboration, KL_pp_shadow OOC, xvlog and lint clean`
- `[R327] PASS Robustness — syn/yosys/ooc.sh:378-396,463-470 against rom_digests.tsv (P2 and its missing-rows mutant); README:468 restore step executed from an off-pin 7a47f578 checkout (P6/P6b) — a ledger without the pin-of-record rows makes the lookup empty, which ooc.sh refuses on; an off-pin checkout is detectable (submodule status '+') and restoring to the gitlink leaves a clean checkout at 0922e434; the new wording directs the reader to the state the tool accepts`
- `[R327] PASS Tests — scripts/check_doc_style.py fault probe (P1); docs gate set at head (receipts/docs_gates); tb/ tree identity (P5) — the style gate fails the assigned 11-word sentence and passes the committed wording, so the adaptation is gate-driven and does not weaken a test; no test, fixture or gate changed; the milan_dp harness sources the README row describes are byte-identical to 54b4c3bb, where R327-1 ran crflic 415/0 and notify 381/0`
- `[R327] PASS Docs — CHANGELOG.md:14,36,45,72,74; docs/reference/SUBMODULES.md:42,55,57-58; tb/verilator/milan_dp/README.md:442,459,468,470,520,552; PR #569 body (sha256 00a349cd...); author-r4 receipts round4.diff and old-pin-hits.txt — F1 fixed; S1 applied; S3 stale lines absent; all docs gates rc 0 in both modes; the author's hit list matches my grep; the only new item is SUGGESTION S1 above, which is pre-existing`

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #567 acceptance 1-4, A10 Round 2/3/4 decisions, README:442-552 pin statements, SUBMODULES.md:25-58, ooc.sh pin-of-record and ledger lookup, rom_digests.tsv, 54b4c3bb..9143e21a tree identity | R327-2 | 9143e21a57e6315c7678430cfc45b4a2b7e10c09 |
| RTL | CLEAN | tree identity of every non-doc path and gitlink vs 54b4c3bb (P5); PR-range name-only diff; processor hdl tree ids (P3); R327-1 RTL evidence at the byte-identical RTL scope | R327-2 | 9143e21a57e6315c7678430cfc45b4a2b7e10c09 |
| Robustness | CLEAN | ooc.sh missing-row refusal branch (P2 mutant); executed off-pin to pin-of-record restore (P6/P6b); off-pin detectability | R327-2 | 9143e21a57e6315c7678430cfc45b4a2b7e10c09 |
| Tests | CLEAN | check_doc_style fault probe (P1); full docs gate set, both modes; tb/ byte identity (P5) | R327-2 | 9143e21a57e6315c7678430cfc45b4a2b7e10c09 |
| Docs | CLEAN | CHANGELOG.md, SUBMODULES.md, milan_dp README, PR body, docs gates both modes, author-r4 receipts cross-check | R327-2 | 9143e21a57e6315c7678430cfc45b4a2b7e10c09 |

The internal review is R326-1 POSITIVE at ancestor `54b4c3bb`. Per the Round 4 assignment it stands as the ancestor positive. Between that head and this one, only the two Docs-scope Markdown files changed (P5). Whether R326-1's Docs and Conformance coverage carries across that change is the manager's merge-bar judgement. This ledger covers all five lenses itself at the exact head.

## Prior public review findings (read after the pass above)

| prior item | status at 9143e21a | assessment |
|---|---|---|
| R327-1 F1 MINOR (Docs, Conformance), README:468 restores `990f9652` | RESOLVED | See focus item 1. |
| R327-1 S1 SUGGESTION, SUBMODULES.md:57 "every pin" | RESOLVED | Applied as two sentences. P1 proves the adaptation was needed. |
| R327-1 S2 SUGGESTION, unbound N_AUDIO_UNIT_P / N_CLK_DOMAIN_P / N_CONTROL_P | RETAINED as SUGGESTION, tracked in #571 (OPEN) | Out of scope; does not affect coverage. |
| R327-1 S3 SUGGESTION, stale PR-body status lines | RESOLVED | `receipts/pr_body_check.txt`. |
| R326-1 S1 SUGGESTION, MILAN_COMPLIANCE_MATRIX.md:136-137 / FR_NFR.md:194 lag the adopted MVU coverage | RETAINED as SUGGESTION | Unchanged at this head (P5). Outside #567's file list. |
| R326-1 S2 SUGGESTION, README:552 permalinks at `990f9652` | RETAINED as SUGGESTION | Target anchors are content-unchanged (P4). The R326-1 note that ":468 is correct as history" is now true, after the F1 fix. |
| R326-1 S3 SUGGESTION, SUBMODULES.md:57 and CHANGELOG.md:42 wording | PARTLY RESOLVED | The `:57` half is applied. The `CHANGELOG.md:42` half ("The repository generator refreshes the submodule diagram and pin text") is unchanged and stays a SUGGESTION. |
| R326-1 S4 SUGGESTION (RTL, Robustness), AEM counts not forwarded to the processor top | RETAINED as SUGGESTION | The same concern as R327-1 S2, tracked in #571. |

No prior finding above SUGGESTION remains open.

## Commands and receipts

Scripts are portable. Each takes a checkout path, and they are run from any directory:

- `run_docs_gates.sh <checkout> <python-with-locked-docs-deps> <receipt-dir>` runs the docs gates in Git mode, then in a `git archive` export. Output: `receipts/docs_gates/`.
- `probes.sh <checkout> <python> <scratch-dir>`:
  - P1: style-gate fault probe on an archive copy.
  - P2: ledger lookup plus a missing-row mutant.
  - P3: processor HDL identity.
  - P4: permalink targets.
  - Output: `receipts/probes.txt`.
- `probes2.sh <checkout>`:
  - P5: tree identity against `54b4c3bb`.
  - P6: repin the processor checkout to `7a47f578`, then restore it. P6b completed the restore by an explicit gitlink checkout and was run inline.
  - Output: `receipts/probes2.txt`.
- `receipts/grep_990f965.txt`, `receipts/delta_54b4c3bb_9143e21a.diff`, `receipts/pr_body_check.txt`, `receipts/hosted_checks.tsv` (two read-only snapshots) and `receipts/final_integrity.txt`.

## Clone state after probes

Verified in `receipts/final_integrity.txt`:

- HEAD is `9143e21a`, and the tree and the index-written tree are both `12bc47c0`.
- The worktree equals the index, and the index equals HEAD. `git status --porcelain` shows 0 lines.
- The protocol-processor, gptp-processor and verilog-axis checkouts equal their gitlinks (`0922e434`, `5dce647a`, `48ff7a7e`) and are clean.
- Both changed files are mode 100644, and their blob ids match `git hash-object`.

## Real limits

- The scoped Verilator 5.050 path named in the assignment does not exist on this host, so no simulation ran in this round. RTL and Tests coverage at this head rests on:
  - byte identity of every non-document path with `54b4c3bb`, where R327-1 executed the simulation and synthesis legs;
  - the probes above.

  This is a delta argument, not a fresh execution.
- No full parent, processor, gPTP, Yosys or builder bank ran. No act or Docker ran, and no hardware was used.
- The Round 4 assignment says the manager's full-source static, builder and native banks passed at this head. I did not find receipts for them at `9143e21a` in the public evidence tree at `270ee694`, which holds the author-r4 receipts and the R326-1/R327-1 packets. I have not verified that claim.
- Hosted contexts at the exact head were read only (snapshot 2, 10:47:57Z):
  - completed with success: the Yosys shards 0-3, full-ci-gate, verilator-lint, wire-accountability, docs-check-no-git, bdd-conformance and changes;
  - still `in_progress`: Verilator shards 0-4, yosys-elaboration, elaborate and docs-check;
  - skipped: "Physical gPTP (nightly and manual)", and a skip is not a pass;
  - combined status: `pending`.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Publish or link the exact-head source-bank receipts cited in the assignment.
- Accept the hosted and act results at `9143e21a`, including the Verilator shards, yosys-elaboration, elaborate and docs-check that were still running.
- Decide the merge bar for the internal review: R326-1 is POSITIVE at ancestor `54b4c3bb`, and this delta touched Docs-scope files.
- Validate the candidate merge against live `dev` (`7eb3b0d4`), then run post-merge containment.
- Optionally file S1 above, and R326-1 S1 and S3 (CHANGELOG half), as follow-up Issues.

R327-2 FINISHED

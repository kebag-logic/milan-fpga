[R420] POSITIVE - exact head 95a78c099ee5aa914521975355adc1dfef99d01c

# R420-5: PR-body re-review of PR #139 (lane C6) at the unchanged head `95a78c09`

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, issue #80 / PR #139, round R420-5.
- Exact head: `95a78c099ee5aa914521975355adc1dfef99d01c`, tree `d0be0f91665f4e6b8e16bfa3aa8f53bbeaff518f`. It is unchanged since R420-4: the PR API reports this head with 14 commits, and my clone is byte-exact at it (section 8).
- Scope: only the delta since my R420-4 NEGATIVE. That review's one open finding, R420-4-F1 (the same finding as R421-4-F1), concerned the condensed PR body. The code, tests and merges are not re-reviewed: R420-4 found them sound, and they have not changed.

## Verdict

**POSITIVE.** The ruling's outcome (b) is implemented as stated, and nothing else changed:

1. **The pointers.** Each of the four condensed validation sections opens with a pointer. They are round 1 ("Validation") and rounds 2, 3 and 4 ("Validation, round N"). Each pointer leads to `review-evidence/ppC6-r1/author-r4/PR-BODY.md` at evidence `ca502628`.
   - That file holds each of those sections byte for byte.
   - Every figure my round-4 receipt listed as dropped is in it, 67 of 67 entries, each with its quoted context verbatim.
   - My unchanged round-4 `figures_dropped.py` reports nothing dropped between the source bodies and the linked file.
2. **Nothing else changed in the body.** The live body differs from `author-r4b/PR-BODY.md` only by the four pointer lines (each followed by a blank line) and one link definition at the end. The PR's edit history shows exactly one body edit since round 4b. Its earlier stored revision equals `author-r4b/PR-BODY.md`, and its current one equals the live body.
3. **The handoff and its digest.** `author-r4b/HANDOFF.md` is corrected in place at `a6ea796e`: "carrying the same figures" becomes "keep only some of their figures", with a pointer to the archived tables. Nothing else in the file changed. At `2a98e7d4`, `MANIFEST.json` records the corrected file's sha256, which equals the bytes I fetched.

R420-4-F1 is therefore **resolved**. Two new SUGGESTIONs (R420-5-S1, S2) and the retained R420-4-S1 and R420-3-S1 do not gate the verdict.

## 1. How the task was reconstructed

1. **Contributor rules and docs.** The repository has no AGENTS.md or CONTRIBUTING.md; `docs/README.md` holds the conventions. These were re-checked only as context, since no repository file changed.
2. **Scope and decisions.**
   - Issue #80 has no new comments since round 4b (5944153047); the last is REVIEW READY 5947318179.
   - On PR #139:
     - the ruling 5948641217: [A10], R421-4 F1, outcome (b);
     - the follow-up 5950041174: R420-4 F1 is the same finding, so the ruling covers it; the digest is updated at `2a98e7d4`;
     - the review start 5950042106.
   - R421-4's report (5948622718) was read only after my verdict and ledger were fixed (`receipts/verdict_before_prior_findings.txt`, 10:15:41Z), and then only for its findings (section 5).
3. **The diff and history.** `03c842a7..95a78c09` is unchanged from R420-4: the same head, the same 14 commits, and a clean clone.
4. **Public evidence.**
   - On `kebag-logic/milan-fpga`, branch `ppC6-review-evidence`, I fetched read-only from the GitHub API, with git-blob identities recorded in `receipts/evidence-fetch.txt`:
     - commits `72483b72`, `7d8194b5`, `ca502628`, `a6ea796e`, `5d9d643e` and `2a98e7d4`;
     - the files `author{,-r2,-r3,-r4,-r4b}/PR-BODY.md`, `author-r4b/HANDOFF.md` and `MANIFEST.json`.
   - The pinned evidence commit in the assignment (`2c532827`) holds only the round-1 packet. As in R420-4, I read the later packets on the evidence branch.

## 2. The linked file holds rounds 1-4's validation tables verbatim (`receipts/linked-tables-check.txt`, rc 0, 0 FAIL)

`scripts/verify_linked_tables.py` makes four checks.

### A. Validation sections, byte for byte

Each section below runs from its heading to the next heading of equal or higher level.

| Section | Source bodies compared | Bytes | Tables / table lines in the linked file |
|---|---|---:|---|
| `## Validation` (round 1) | `author` (first) and `author-r3` (last full) | 4,227 | 3 / 38 |
| `### Validation, round 2` | `author-r2` and `author-r3` | 5,695 | 4 / 43 |
| `### Validation, round 3` | `author-r3` | 5,523 | 3 / 37 |
| `### Validation, round 4` | `author-r4` | 6,300 | 3 / 40 |

All are identical. The whole round sections are identical too:
- 19,516, 18,768 and 12,677 bytes for rounds 1, 2 and 4;
- 13,879 bytes for round 3, where the linked file adds only the blank line before "## Round 4".

`author-r4/PR-BODY.md` is byte-identical at `72483b72`, `7d8194b5`, `ca502628`, `a6ea796e` and `2a98e7d4` (sha256 `a72a4fde…`). Its first 461 lines equal all of `author-r3/PR-BODY.md`.

### B. My figure comparison, re-run

| Run | Result |
|---|---|
| `scripts/verify_linked_tables.py` (R420-4's regex), source round section -> linked round section | 138, 122, 90 and 97 distinct figures for rounds 1-4; none missing |
| R420-4's `figures_dropped.py`, copied unchanged, `author-r3` -> linked `author-r4` | empty output, rc 0 (`receipts/figures-dropped-rerun.txt`) |
| same, `author-r4` at `72483b72` -> linked | empty, rc 0 |
| control, `author-r3` -> live body | still 47 round 1-3 entries, as in R420-4 |

The control shows the condensed paragraphs themselves are unchanged: the figures are recovered through the link, not restored inline. This is exactly outcome (b).

### C. Every entry of my round-4 dropped receipt

All 67 entries (round 1: 7, round 2: 18, round 3: 22, round 4: 20) are found in the linked file's same round section, both as the figure and with the receipt's quoted context verbatim. R421-4-F1's own list (42 items, including 3,793, "184 md + 955", 15,230, 15,301 and 15,232) is all present as well (`receipts/r421-4-f1-figures-in-linked.txt`).

### D. The pointers and the link

- In each condensed section, the first non-empty line after the heading is exactly: `This round's tables, verbatim with every figure, are in the archived round-4 body, section "<that heading>" ([full tables][c6-r1-r4-tables]). The paragraphs below condense them.`
- There is one definition, `[c6-r1-r4-tables]: https://github.com/kebag-logic/milan-fpga/blob/ca50262850d156308a45ce5237e9adff64419f89/review-evidence/ppC6-r1/author-r4/PR-BODY.md`, and it is used 4 times.
- The blob URL answers HTTP 200 without authentication. The unauthenticated raw fetch hashes to the same `a72a4fde…`.
- Each named section heading exists exactly once in the linked file (`:102`, `:269`, `:401`, `:498`).

## 3. No other body text changed (`receipts/live-vs-r4b.diff`, `receipts/body-edit-history.txt`)

`diff author-r4b/PR-BODY.md live-body` gives five hunks, all additions:
- the pointer plus a blank line after `## Validation` (live `:106`), `### Validation, round 2` (`:240`), `### Validation, round 3` (`:329`) and `### Validation, round 4` (`:386`);
- a blank line plus the link definition after the last line (`:504`).

There are no deletions and no changed lines, and no carriage returns in either file.

Lengths:
- `author-r4b`: 64,316 characters;
- live: 65,196 characters, 880 added;
- headroom: 340, as the ruling says.

GraphQL `userContentEdits` shows two body revisions since round 4b began:
- 07:24:17Z, equal to `author-r4b/PR-BODY.md`;
- 08:58:02Z, equal to the live body.

`lastEditedAt` is 08:58:02Z. Round 4b's own section (`### Validation, round 4b` and the rest) is untouched.

## 4. The handoff correction and its digest (`receipts/handoff-diff.txt`, `receipts/manifest-diff.txt`, `receipts/manifest-digest-check.txt`)

**`author-r4b/HANDOFF.md`, `7d8194b5` -> `a6ea796e`:** one hunk, `:225-227`. The word diff:
- removes "carrying the same";
- adds "that keep only some of their" and "(manager correction, 2026-10-02, review R421-4 F1: the full tables, verbatim, are in `../author-r4/PR-BODY.md`, and the PR body now links them from each condensed round)".

Nothing else changed. The file is identical at `a6ea796e` and `2a98e7d4`, and identical at `7d8194b5` and `ca502628`.

The corrected sentence is now true:
- the paragraphs do keep only some figures (the control in section 2B);
- `../author-r4/PR-BODY.md` resolves to the linked file;
- the PR body links it from each condensed round.

**`MANIFEST.json`, `5d9d643e` -> `2a98e7d4`:** one entry changes, `author-r4b/HANDOFF.md`.
- `published_sha256` goes from `bbc5df58…` (the `7d8194b5` bytes) to `062510e3…`, which is the sha256 of the bytes fetched at `a6ea796e` and `2a98e7d4`.
- A `manager_correction` note naming `a6ea796e` is added.
- `original_sha256` is kept, as the pre-redaction author file, with the note recording the divergence.

The manifest's `published_sha256` also matches the fetched bytes of all six PR-BODY.md files (`author`, `-r2`, `-r3`, `-r4`, `-r4b`). Between `a6ea796e` and `2a98e7d4` the manifest carried the old digest, and `2a98e7d4` closes that gap.

## 5. Prior findings at this head

| Finding | Status at `95a78c09` | Evidence |
|---|---|---|
| **R420-4-F1 MINOR** (the condensed body drops figures) | **resolved** by ruling 5948641217, outcome (b) (my required outcome's alternative: pointers at a pinned evidence commit, with the ruling recorded) | sections 2-4; the verification I set (pointers plus a recorded ruling) is met |
| **R421-4-F1 MINOR** (same defect; read after my verdict) | **resolved**, outcome (b) | its verification for (b) is "each of the four paragraphs carries the pointer and the pointed files hold the tables": section 2D and 2A/2C; the handoff sentence is corrected (section 4) |
| R420-4-S1 SUGGESTION (`sim_main.cpp:13566-13568` names two of four single-section builds) | **open, retained** (no code change this round) | head unchanged |
| R420-3-S1 SUGGESTION (latch boundary cycle) | **open, retained** | as at R420-4 |
| R421-3-S1 SUGGESTION (FT4 at phase 99,999) | **open, retained** | as at R420-4 |
| R420-1-F1/F2, R420-2-F1, R421-1-F1, R421-2-F1 | still resolved | code unchanged since R420-4, which re-ran their probes at this head |
| R420-1-S1, S4 | retained, recorded | unchanged |

## 6. Findings this round

No BLOCKER, MAJOR, MINOR or RESIDUE.

### R420-5-S1 SUGGESTION: the corrected handoff sentence stacks two parentheticals

- **Lenses:** Docs.
- **Where:** `review-evidence/ppC6-r1/author-r4b/HANDOFF.md:225-228` at evidence `a6ea796e`/`2a98e7d4`.
- **Evidence:** "…paragraphs that keep only some of their figures (manager correction, … from each condensed round) (round 1: processor and parent tables; …)". The per-round list of *tables* now follows the correction's parenthetical and reads as if it qualified "figures". The facts are right.
- **Proposal:** "…the older rounds' validation tables became paragraphs that keep only some of their figures (round 1: processor and parent tables; round 2: processor, campaign and parent tables; round 3: the same; round 4: processor, campaign, probe and parent tables). Manager correction, 2026-10-02, review R421-4 F1: the full tables, verbatim, are in `../author-r4/PR-BODY.md`, and the PR body links them from each condensed round. The rounds' design text, …"
- **Verification:** a re-read of the paragraph.

### R420-5-S2 SUGGESTION: the posted body is not itself archived

- **Lenses:** Docs.
- **Where:** evidence `author-r4b/` (`PR-BODY.md`, and the HANDOFF's last-line length "64,316 characters … 1,220 under").
- **Evidence:** the body now posted (65,196 characters, 340 under the limit) exists only on the PR and in its edit history. The archive's `PR-BODY.md` and its length line describe the pre-pointer body. The handoff's new sentence ("the PR body now links them") is the only record of the difference.
- **Proposal:** at the next evidence archive (for example the merge turn), either archive the posted body, or add one line to the handoff: "Posted body = this PR-BODY.md + four pointer lines + one link definition; 65,196 characters, 340 under the limit."
- **Verification:** the archived body or the line equals the PR body at merge.

## 7. Lens results (artifact-specific)

- **Conformance: CLEAN.** No clause claim, code or generated artifact changed (same head). The body edit adds no conformance claim: the pointer lines name only sections and a file. R420-4's conformance evidence (both relocated bodies byte-exact at 464/480, and the others) stands at this head.
- **RTL: CLEAN.** The head and tree are unchanged, and the clone is byte-exact (section 8). R420-4's RTL evidence stands.
- **Robustness: CLEAN.** No artifact changed. The new evidence is pinned: the link is to a full commit SHA, not to the branch. That file is byte-stable across the five later evidence commits, and the manifest digests match the fetched bytes. R420-4's probes stand.
- **Tests: CLEAN.** No test or campaign changed. The figures the body now points to are the recorded ones (sections 2A-2C). Hosted checks at the head: 6 check runs, all `completed/success` (`suites` ×2, `docs-gates` ×2, `portability` ×2; `receipts/pr-state.txt`). These were read only; the manager owns hosted acceptance.
- **Docs: CLEAN.** R420-4-F1 is resolved (sections 2-4). The body diff is exactly the ruling's addition, and the handoff is corrected and re-digested. S1 and S2 are SUGGESTIONs.

## 8. Clone integrity (`receipts/clone_integrity.txt`)

- HEAD and tree are exact.
- There are 0 porcelain entries, ignored files included.
- The worktree equals the index, which equals HEAD.
- The index's 470 entries equal the HEAD tree in mode, blob and path.
- Re-hashing every tracked file gives 0 mismatches.
- There is no gitlink and no `.gitmodules`, so no submodule gitlinks are required.

No probe or build ran in the clone this round: nothing was modified, so nothing needed restoring.

## 9. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | live body pointer lines and link (no clause claims added); head/tree unchanged; R420-4's conformance evidence carried | R420-4 (code), R420-5 (body) | `95a78c09` |
| RTL | CLEAN | head/tree identity (PR API, clone); R420-4's RTL evidence carried | R420-4 | `95a78c09` |
| Robustness | CLEAN | link pinned to full SHA `ca502628`; linked file byte-stable over 5 commits; 6 manifest digests equal fetched bytes; R420-4 probes carried | R420-4 (code), R420-5 (evidence) | `95a78c09` |
| Tests | CLEAN | linked tables vs. source bodies (A-C); 6/6 hosted check runs success (read only); R420-4 suites and campaigns carried | R420-4 (code), R420-5 (figures) | `95a78c09` |
| Docs | CLEAN | live body vs. `author-r4b/PR-BODY.md` (5 additive hunks); edit history (1 edit); `author-r4/PR-BODY.md` at `ca502628` vs. `author`, `-r2`, `-r3`, `-r4` sections; R420-4 and R421-4 dropped lists; `HANDOFF.md:225-228` at `a6ea796e`; `MANIFEST.json` at `2a98e7d4` (S1, S2) | R420-5 | `95a78c09` |

## 10. Real limits and pending manager duties

- **Not re-run this round, by scope:** builds, suites, campaigns and probes. The code is unchanged since R420-4, and its measurements are carried from that review. The pinned Verilator was not used.
- **Not run, as not allowed:** the processor-wide, yosys, donor and parent banks. Their results are the manager's: donor bank 9/9 and parent consumer set 16/16 at this head. The final current-dev candidate at the merge turn (source base `03c842a7`, live dev `cdf49d1a`) also belongs to the manager.
- **Evidence location:** as in R420-4, the assignment's pinned evidence commit (`2c532827`) predates the round-4 packets. The evidence branch commits named in section 1 were used.
- **Physical calibration NOT RUN.** No hardware was used. Field skips are not hardware proof.
- **Hosted/act acceptance** is the manager's. I only read the exact-head check runs.
- **Pending for the manager:**
  - publish this report;
  - optionally carry S1 and S2;
  - the merge-turn candidate build;
  - the two-positive-review bar, with R421-5 still pending.

## 11. Packet

Every file below is listed in `MANIFEST.sha256`.

- **Scripts** (`scripts/`):
  - `fetch_evidence.sh`: read-only API fetch of the evidence files and the live body;
  - `verify_linked_tables.py`: checks A-D;
  - `figures_dropped.py`: R420-4's script, unchanged.
- **Receipts** (`receipts/`):
  - `evidence-fetch.txt`;
  - `linked-tables-check.txt`;
  - `figures-dropped-rerun.txt`;
  - `r420-4-prbody-figures-dropped.txt`: R420-4's receipt, the input to check C;
  - `r421-4-f1-figures-in-linked.txt`;
  - `live-vs-r4b.diff`;
  - `live-body-at-review.md`;
  - `body-edit-history.txt`;
  - `handoff-diff.txt`;
  - `manifest-diff.txt`;
  - `manifest-digest-check.txt`;
  - `pr-state.txt`;
  - `clone_integrity.txt`;
  - `verdict_before_prior_findings.txt`.
- **Not published:** `scratch/`, which holds the fetched evidence files and API responses.

R420-5 FINISHED

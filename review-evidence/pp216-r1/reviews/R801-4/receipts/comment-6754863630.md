[R801] NEGATIVE - exact head 03862f75c89e5c1d84baa4735eff1c1c6f796e25

# R801-3 independent review: processor issue #216 / PR #218, round 3 (docs-only delta)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #218, branch `216-mrp-applicant`.
- Exact head `03862f75c89e5c1d84baa4735eff1c1c6f796e25`, tree `dec0f2f79439b89af8686f87bd1db6653a0585fd`. The PR's `headRefOid` at review time was this head.
- Delta reviewed: `84f6d6a..03862f7`, one commit, `docs/` only. Ruling: issue #216 issuecomment-6751398007 (round 3).
- Previously reviewed head: `84f6d6a` (R801-2 POSITIVE; R802-2 NEGATIVE on one MINOR).

## Verdict

**NEGATIVE, on one MINOR (R801-3-F01). The fix is an edit to the PR body only.**

- The repository delta does what the ruling asked:
  - 10 §6.2 now gives the right basis (Table 10-3 has no Flush! row).
  - It discloses the leavealltimer! omission.
  - GAP-19 records that omission, with its clause, its effect and an owner.
  - R802-2's two exact wording fixes are in.
  - The tree outside `docs/` is byte-identical to `84f6d6a`.
  - `make check` and `gen_matrix.py --check` pass when I run them at this head.
- The PR body still has the basis the ruling replaced. Line 39 of the per-file summary reads "LINK_DOWN leaves the Applicants as they are (Flush! is a Registrar event, 10.7.5.2)". That is the cause of R802-2-F1, so the cause is fixed in the repository but not in the PR text. The PR body's own "Round 3" section says this basis was replaced.
- This is a clause basis, not pure wording. Under the residue rule, a defect that touches a clause claim is not RESIDUE. So it is a MINOR.
- Nothing in the delta contradicts my R801-2 POSITIVE at `84f6d6a`. The RTL, Robustness and Tests lens verdicts carry over unchanged, because the delta does not touch anything they depend on.

## Findings

### R801-3-F01 - MINOR - Docs, Conformance - the PR body still cites §10.7.5.2 as the reason LINK_DOWN leaves the Applicants alone

- **Where:** the body of PR #218, line 39, in the `hdl/srp/KL_srp_vlan.sv` bullet of the per-file summary: "LINK_DOWN leaves the Applicants as they are (Flush! is a Registrar event, 10.7.5.2)." Receipts: `receipts/pr218-body-at-review.md` (sha256 `a37dbac3…0a42`) and `receipts/pr-body-basis.txt`.
- **Authority and evidence:**
  - Ruling item 1 (issuecomment-6751398007): the accurate basis is "Table 10-3 has no Flush! row, so LINK_DOWN leaves the Applicants as they are". It also requires disclosure that §10.7.5.2 signals leavealltimer! to the LeaveAll state machine.
  - The author's round-3 clause record (`author-r3/STANDARDS.txt`, evidence commit `6c2007ae`) quotes the second paragraph of 10.7.5.2: "a leavealltimer! event (10.7.5.22) is also signaled to the LeaveAll state machine". From that it concludes: "So Flush! is not a Registrar event only".
  - The same PR body says the opposite in three places:
    - line 99 gives the ruled basis ("Table 10-3 has no Flush! row");
    - lines 192-194 say the docs basis now reads that way, "in place of 'Flush! is a Registrar event only (§10.7.5.2)'";
    - line 39 still gives the old basis.
  - The sentence is unchanged since round 2: the published `author-r2/PR-BODY.md:39` is word-for-word the same. Round 3 fixed the docs but not this copy.
- **Impact:**
  - No behaviour, gate or repository-file effect.
  - In the PR text, the summary a reader sees first gives the clause basis that R802-2-F1 found and the ruling replaced. It also leaves out the leavealltimer! half of Flush!.
  - If the PR body is used as the merge commit message, the replaced basis goes into history.
- **Required outcome:** edit PR body line 39 to the ruled basis. Exact text: replace "LINK_DOWN leaves the Applicants as they are (Flush! is a Registrar event, 10.7.5.2)." with "LINK_DOWN leaves the Applicants as they are (Table 10-3 has no Flush! row); it signals no leavealltimer! to either LeaveAll state machine (GAP-19)." No source, docs or head change is needed.
- **Verification:**
  - Run `gh pr view 218 --json body` and confirm that no line cites 10.7.5.2 as the reason for the Applicants and that line 39 names Table 10-3.
  - The head stays `03862f7`, so a reviewer can close this by reading the text alone. Every gate in this report still stands.

### R801-3-R01 - RESIDUE - Docs - a ragged wrap in the reworded 10 §6.2 paragraph

- **Where:** `docs/architecture/10_srp_engine.md:530`. "over a received value of its clock," is a 35-character line in a paragraph that wraps at about 95 characters. The F1 rewording left it there.
- It is wording only, with the same layout class as R802-2-R2. It renders identically in Markdown.
- **Exact fix:** re-flow lines 529 to 539 of that paragraph at the paragraph's 95-character width, changing no words.

### R801-3-S01 - SUGGESTION - Conformance, Docs - when the GAP-19 issue is filed, cover LINK_UP's Begin! as well

- **Where:** GAP-19 (`docs/00_MILAN_COMPLIANCE_REVIEW.md:384-392`) and 10 §6.2 (`:518`, "maps … LINK_UP to Begin!").
- **What I observe:**
  - The same RTL trace that supports GAP-19 (`receipts/rtl-link-leaveall-trace.txt`) shows that LINK_UP does not reach the LeaveAll state or the `periodic!` cadence either. In `KL_srp_top`, `link_up_i` goes only to `KL_srp_domain`, `KL_srp_vlan` and `KL_srp_listener_fsm`. The `la_*_pend_r` and `need_draw_r` registers and the CAD_PERIODIC slot have no link term.
  - Begin! (10.7.5.1) initialises every state machine of the participant. On the LeaveAll machine (Table 10-5) that would mean a fresh leavealltimer and Passive; on the PeriodicTransmission machine (Table 10-6), a restarted periodictimer.
  - No claim in the delta is wrong. The docs scope LINK_UP's Begin! to the Registrars and the VID Applicants. But GAP-19 discloses only the LINK_DOWN half of the link mapping that leaves these machines alone.
- **Why only a suggestion:** I did not read the 802.1Q text for 10.7.5.1 or Tables 10-5 and 10-6 (see Real limits). The wire effect is at most one early or late own LeaveAll after a link bounce, which is harmless. And #216's acceptance says "MRP timers unchanged".
- **Suggested outcome:** the issue the manager files for GAP-19 should name both edges: Flush!'s leavealltimer!, and Begin!'s LeaveAll and periodic restarts at LINK_UP. Alternatively, it should say why the Begin! half is not owed.

### R801-3-S02 - SUGGESTION - Docs - point GAP-19's owner cell at the issue once it is filed

- **Where:** the F00.2 row `docs/00_MILAN_COMPLIANCE_REVIEW.md:609` ("owed, not filed").
- **Suggested outcome:** once the manager files the issue (ruling item 1), replace "owed, not filed" with its link, in the same form as the other rows' Open residue cells. This belongs on the residue checklist, not this round.

## Ruling items (issuecomment-6751398007), judged at their cause

1. **Item 1: 10 §6.2 basis and disclosure. Met in the repository.**
   - `10_srp_engine.md:525-529` reads "Table 10-3 has no Flush! row, so LINK_DOWN leaves the Applicants as they are". It then says "§10.7.5.2 also signals leavealltimer! to the LeaveAll state machine at a Flush!; this engine's LINK_DOWN does not, on either participant, since issue #216 changes no MRP timers", with a link to GAP-19. That is the ruling's text.
   - The RTL fact behind it holds (`receipts/rtl-link-leaveall-trace.txt`):
     - `link_up_i` is used in `KL_srp_top` only at its port (`:147`) and at three instance connections: `:399` `KL_srp_domain`, `:476` `KL_srp_vlan`, `:670` `KL_srp_listener_fsm`.
     - No other non-comment line of `KL_srp_top` mentions the link.
     - The two LeaveAll state machines live in `KL_srp_top` (`la_msrp_pend_r`, `la_mvrp_pend_r`, `need_draw_r`, `:1138-1139`, `:1201-1234`, `:1275-1333`). They are set only by the timer expiry and cleared by rLA!, the tx! round and reset. None of them reads the link.
     - So a LINK_DOWN leaves each participant on its `T-MRP-LEAVEALL` cycle, as GAP-19 says.
   - The PR-body copy of the old basis is R801-3-F01.
2. **Item 1: GAP-19 and its owner. Met. The owner is right at this head; the manager still has to file the issue.**
   - GAP-19 (`00:384-392`) gives the omission, its clauses (10.7.5.2, 10.7.5.22, Table 10-5), its effect ("starts a fresh leavealltimer and enters Active, whose tx! is sLA") and its disposition.
   - Those clause readings match the author's round-3 clause record.
   - The F00.2 row (`:609`) is graded honestly: "none: the omission is not graded".
   - REQ-SRP-001 links GAP-19 (`:546`), and the matrix gate counts "19 GAP findings, OK".
   - **Owner.** I searched the open issues of the processor repository for leavealltimer, Flush!, LeaveAll, LINK_DOWN, link change and GAP-19. Only two match:
     - #216, this PR's issue. Its acceptance says "MRP timers unchanged", and it keeps the omission as a disclosed item.
     - #220, which owns the MSRP stream Applicants' Begin! at LINK_UP, not the LeaveAll machine.
   - No open issue owns the omission, so "owed, not filed" is accurate. It is the form the ruling prescribes.
   - **An issue must still be filed.** The ruling commits the manager to filing it ("I file it"). It is not the author's to file, and filing it is not a defect of this head. I list it under pending manager duties and suggest its scope in S01.
3. **Item 2 (R802-2 R1): met.** Once newlines are normalised, `10_srp_engine.md:536-537` carry the exact fix, word for word: "A link change does not reset `vid_sent_o`, the talker's streaming licence of [Join before the stream](#sec-10-join-before-stream) below." The anchor `sec-10-join-before-stream` exists (`:554`), and `make check` links passes.
4. **Item 3 (R802-2 R2): met.** That hunk breaks the line after "never JoinIn without IN." (`:509` / `:510`) and changes nothing else.
5. **Item 4 (S1 and S2 of both reviews): not in this round, as ruled.** They are still open as suggestions on the residue checklist. The new R1 text does not take R801-2-S2's argument, and does not have to.
6. **Gates and byte identity: met.**
   - `git diff --stat 84f6d6a 03862f7 -- . ':(exclude)docs'` is empty.
   - The `git ls-tree -r` of each commit, without `docs/`, hashes to the same sha256, `3797e11b…524e`.
   - So the round-2 suites, campaign, area and scratch-parent results stand for this head.

## Prior findings at this head

| Finding | Severity | Status at `03862f7` | Evidence |
|---|---|---|---|
| R802-2-F1: "Flush! is a Registrar event only (§10.7.5.2)" | MINOR | **RESOLVED in the repository**; the cause **survives in the PR body**, carried as R801-3-F01 | `10_srp_engine.md:525-529`; GAP-19; PR body `:39` |
| R802-2-R1: "(below)" target | RESIDUE | **RESOLVED** (exact fix) | `10_srp_engine.md:536-537` |
| R802-2-R2: unwrapped long line | RESIDUE | **RESOLVED** (exact fix) | `10_srp_engine.md:509-510` |
| R802-2-S1 / R801-2-S1: AP8 arms graded on the `AP8:` prefix | SUGGESTION | open; deferred to the residue checklist by the ruling | `tb/srp_top/mutants.py` unchanged (tree outside docs identical) |
| R802-2-S2 / R801-2-S2: `vid_sent_o` across a link bounce | SUGGESTION | open; deferred by the ruling | `KL_srp_vlan.sv` unchanged |
| R802-2-S3: two-suite arm keeps one log | SUGGESTION | open; pre-existing, not this PR's | unchanged |
| R801-2 POSITIVE at `84f6d6a` | - | **not contradicted**: the delta changes no code, test, generated file or measured figure; the RTL fact it adds is true | this report |

## Lens verdicts and evidence

- **Conformance: UNCLEAN (F01).**
  - The docs' clause basis now matches the clause record: 10.7.5.2's two paragraphs, 10.7.5.22 and Table 10-5.
  - GAP-19's effect statement is right, and its disposition matches #216's frozen acceptance ("MRP timers unchanged").
  - The PR body still gives the replaced basis (F01).
  - S01 is the LINK_UP counterpart. It is a suggestion only.
- **RTL: CLEAN (carried from R801-2).**
  - No RTL change: the tree outside `docs/` is byte-identical.
  - I re-traced, statically, the one RTL fact the delta adds (the link input and the LeaveAll state), and it is true.
- **Robustness: CLEAN (carried from R801-2).** No change. GAP-19 adds no new hazard; it discloses an existing omission.
- **Tests: CLEAN (carried from R801-2).**
  - No testbench or campaign change.
  - The register's "Verified by: none: the omission is not graded" is honest.
  - `make check` (its req-tags, ids and AECP-command self-tests included) and `gen_matrix.py --check` pass at this head when I run them.
- **Docs: UNCLEAN (F01; R01 is residue).**
  - 10 §6.2 and 00 GAP-19, F00.2 and REQ-SRP-001 are accurate. Every link and anchor resolves.
  - `git diff --check` is empty against both `84f6d6a` and `044cb25f`.
  - Comment rule: the delta has no source comments. The docs delta names no lane, round, reviewer or comment ID.
  - The PR body has F01.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F01) | 10 §6.2 `:516-539`; 00 GAP-19 `:384-392`, F00.2 `:609`, REQ-SRP-001 `:546`; ruling 6751398007; #216 acceptance; author `author-r3/STANDARDS.txt`; PR body `:39`, `:99-102`, `:187-220`; open issues #216 and #220; S01 | R801-3 | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| RTL | CLEAN | byte identity outside `docs/` vs `84f6d6a` (diff stat empty, ls-tree hash equal); `KL_srp_top.sv` link fan-out and LeaveAll state (`receipts/rtl-link-leaveall-trace.txt`); R801-2 RTL verdict carried | R801-3 (delta), R801-2 (code) | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| Robustness | CLEAN | byte identity outside `docs/`; GAP-19 adds no new behaviour; R801-2 verdict carried | R801-3 (delta), R801-2 (code) | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| Tests | CLEAN | `make check` rc 0, `gen_matrix.py --check` rc 0 (own runs); author round-3 gate receipts (48/48 manifest hashes, rc 0, logs equal to mine); tb unchanged; R801-2 suite and campaign verdict carried | R801-3 (delta), R801-2 (code) | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |
| Docs | UNCLEAN (F01; R01 residue) | the two-file delta; anchors `gap-19`, `sec-10-vid-link`, `sec-10-join-before-stream`; R802-2 R1 and R2 exact fixes; `git diff --check` vs `84f6d6a` and `044cb25f`; comment rule; PR body | R801-3 | 03862f75c89e5c1d84baa4735eff1c1c6f796e25 |

## Gates and probes I ran at the exact head

Every run was on a fresh clone of the exact head under the packet's `scratch/clones/gates`. Receipts are in `receipts/<name>.{cmd,log,rc,start,end}`.

| Gate | rc | Result |
|---|---|---|
| `make check` (Mermaid CLI 11.16.0; wavedrom 2.0.3.post3 in the gate's own venv) | 0 | lint 41 mermaid + 18 wavedrom OK; links 1334 OK; matrix 115 REQ rows, 19 GAP findings OK; req-tags selftest 29, 101 traced / 8 waived / 6 need no check, 266 tags OK; parameters 29 OK; AECP selftest 231/231, 32 commands OK; ids selftest 30, 822 files OK; figures selftest 17, OK; stale silent |
| `python3 scripts/gen_matrix.py --check` | 0 | `matrix: OK (94 rows, 0 untested)` |
| `git diff --check 84f6d6a 03862f7` / `044cb25f 03862f7` | 0 / 0 | empty / empty |
| `git diff --stat 84f6d6a 03862f7 -- . ':(exclude)docs'` | 0 | empty |
| `git ls-tree -r` without `docs/`, at `84f6d6a` and at `03862f7` | 0 | both sha256 `3797e11bd02cb835b13706d6d5a68660d2929b5d2822ebf9d1e35337ac19524e` |
| Static RTL trace (`receipts/rtl-link-leaveall-trace.txt`) | - | `link_up_i` reaches only `KL_srp_domain`, `KL_srp_vlan`, `KL_srp_listener_fsm`; no LeaveAll state term reads the link |
| Clone integrity (`receipts/clone-integrity.txt`) | - | both clones: HEAD and tree exact; index equals `ls-tree -r HEAD` (mode, blob, path); 0 gitlinks at the head (the repository has no submodules); the review clone is clean; the gate clone holds only the ignored `.venv-wavedrom/` |

I ran no suites, campaigns or Verilator builds: the delta changes nothing they read. No probe changed tracked bytes.

## Published evidence checked

- **Evidence tree:** milan-fpga `6c2007ae9f50f0ed87076dcf04e7ec7268b5068e`, `review-evidence/pp216-r1/`. Its commit carries no verified signature on GitHub. Its integrity is the content manifest `MANIFEST.json`.
- **Hashes:** all 48 `author-r3/` entries in `MANIFEST.json` match the published bytes, with none missing, unlisted or redacted (`receipts/evidence-r3-manifest-check.txt`, `scripts/verify_evidence.py`). I did not open the `reviews/` subtree.
- **Cross-check against my own runs** (`receipts/author-r3-crosscheck.txt`):
  - the author's `head.txt` is the exact head;
  - every author rc is 0;
  - the author's `diff-84f6d6a-HEAD.patch` is byte-identical to my `git diff`;
  - the author's `outside_docs` log is empty;
  - the gate lines of the author's `make_check.log` are identical to mine;
  - `gen_matrix.log` is byte-identical.
- **Interpreter:** the author's gates ran on a 3.12.3 interpreter and mine on 3.14.9, with the same results.

## Hosted evidence at the exact head (inspected, not owned)

`receipts/hosted-checks-at-head.tsv`: `docs-gates` succeeded twice and `portability` succeeded twice. Both `suites` runs were still `in_progress` when I checked, started 2026-11-09T22:19Z. There are no commit-status contexts. Hosted and act acceptance belong to the manager.

## Real limits

- I did not read the IEEE 802.1Q-2018 text. The clause content comes from the author's round-3 clause record and the repository docs, and the S01 reading of 10.7.5.1 and Tables 10-5 and 10-6 comes from neither. That is why S01 is a suggestion.
- No manager source bank ran at this exact head, and I claim none.
- The current-dev merge candidate (source base `044cb25f`, live dev `123f57a922bf07476cd69f91867f3b6f07080804`) is the manager's to build and validate at the merge turn. This review does not stand in for it.
- The round-2 suite, campaign, area and scratch-parent results carry to this head only through the byte identity outside `docs/`. I did not re-execute them.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry R801-3-F01 to the PR body (a text edit; the head stays `03862f7`).
- File the GAP-19 issue as ruling item 1 commits, preferably naming both link edges (S01). Then link it from the F00.2 row (S02, residue checklist).
- Add R801-3-R01 to the residue checklist. Carry R802-2-S1 to S3 and R801-2-S1 and S2 there too, as ruled.
- Accept the hosted `suites` runs at this head once they finish. Build and validate the current-dev merge candidate at the merge turn.

R801-3 FINISHED

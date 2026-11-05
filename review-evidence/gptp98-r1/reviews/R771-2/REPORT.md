[R771] POSITIVE - exact head 762fbd6716b50337e7644a4918c216b3143aeb5b

# R771-2 internal independent review: FPGA-gPTP PR #99 (issue #98), round 2

- **Head:** `762fbd6716b50337e7644a4918c216b3143aeb5b`, tree `1354fd45f1bb7dbe0e967367731243a2d2049d97`. Verified in the detached review clone and in a fresh clone used for the gates.
- **Base:** `3e3a4e7695ce66eed609089f280c2fba45b24d36`.
- **Round 2 delta:** `5b10675c..762fbd67`, four commits: `fc13a65`, `a030c62`, `6e27cd6` and `762fbd6`. They touch seven files: `tb/verilator/parser/{sim_main.cpp,mutants.py,Makefile}`, `tb/verilator/engine/sim_main.cpp` (comments only), `docs/HDL_DEVELOPER.md`, `docs/TEST_DEVELOPER.md` and `scripts/check_docs.py`.
- **`hdl/`:** tree `360f2459ad13e9fddeec2a2c1fb49e2cb6377556` at both `5b10675c` and `762fbd67`, so the RTL is unchanged.
- **Scope:** the round 2 assignment on issue #98 (issuecomment-6640832434). I judged only the delta and every round 1 finding at its cause. Code the delta does not touch keeps its round 1 lens verdict.

## Verdict

POSITIVE. Every round 1 MINOR is resolved at its cause, and so are both reviewers' residue items. The taken suggestions are in place and each is proven by name.

I found no MINOR or worse issue. The report records:
- one RESIDUE: a docstring claim my probe falsifies, a wording-only fix;
- three SUGGESTIONS.

## Reconstruction

- **Repository guides.** The repo has no `AGENTS.md` or `CONTRIBUTING.md`. `docs/README.md` sets the truth order: RTL, then executable tests, then role guides, then historical records.
- **Issue #98 acceptance.** I re-read items 1-4. Item 2: no information TLV, a TLV past messageLength or a truncated header is still dropped and counted. Item 3: harness rows for each refusal, each with a parser mutant caught by name.
- **Round 2 assignment (A10).** Items 1-5 below are checked against it.
- **Prior findings.** I read R771-1 (issuecomment-6640825036) and R772-1 (issuecomment-6640756256) only after my own pass over the diff.
- **PR body.** Read at the exact head through the PR's `headRefOid`.
- **Published author evidence.** `kebag-logic/milan-fpga@59152409…/review-evidence/gptp98-r1/author-r2`, hash-checked against its `MANIFEST.json` (see below).
- **Manager evidence.** No manager evidence comment exists at this head on the issue or the PR. The only items are the REVIEW READY notice and the review-start notice. No manager source bank ran at this head, and I claim none.

## Assignment items, checked

### 1. R772-1 F1: latch rows, latch mutant, and the split

**Rows.** Both rows are in `tb/verilator/parser/sim_main.cpp`, each checked by `expect_fu_refused(…, true)`, so each expects no event, one drop and no w11 write:
- `:998`, frame A: `{0x000A, 0x0100}` with no value, then the information TLV, messageLength 80.
- `:1002`, frame B: `{0x000A, 0x0001}`, then the information TLV.

I checked the arithmetic: 44 + 4 + 4 + 28 = 80, which matches the comment.

**Mutant.** `mutants.py:340`, "a malformed TLV header does not latch the refusal". It replaces `FU_LATCH + "bad_r <= 1'b1;\n"` with `FU_LATCH`, and names `refused(A, True) + refused(B, True)`. Receipt: `receipts/gates/parser_mutants.log:22`, "[PASS] mutant caught … fails all 6 named check(s)".

My own copy of this deletion (`latch_deleted`) runs against the unmodified head harness. It fails exactly those 6 checks and no others: 482 checks, 476 PASS (`receipts/reviewer-mutants/summary.txt`, `latch_deleted.log`).

**Split.** Each term now has its own mutant, and each is caught alone:
- **Walk latch** (`:330`): the latch condition keeps only the odd term. Caught on 5 checks: the information-TLV and trailing overrun rows (`parser_mutants.log:21`).
- **End-of-frame current-byte term** (`:347`): caught on "#98 header ends messageLength, value to come" (`:23`).
- **Cut term** (`:355`): caught on the six header-cut rows (`:25`).

Under round 1's combined edit, the value-to-come row was named by both halves at once. It is now named only by the end-of-frame half. **Resolved.**

### 2. R771-1 F1: "#98 unknown TLVs after"

- `FU_AFTER` (`mutants.py:176`) holds "#98 unknown TLVs after: event" and ": no drop".
- Two mutants name it:
  - the cut-after mutant (`:399`) edits `fu_tlv_cut_after_w`;
  - the zero-length-after mutant (`:403`) refuses a zero-length TLV after the information TLV.
- A third mutant also names it: the last declared octet is not walked (`:408`).
- All three are caught on both checks (`parser_mutants.log:33-35`), and the control passes (`:1`).

The row's frame is `{INFO, ZERO_LEN, ORG_OTHER, ZERO_LEN}` with no padding. Its last octet is the header's last byte at `cnt_r == msg_end_r`, so the cut-after mutant really exercises the header-byte branch.

My round 1 reviewer mutants rerun against the unmodified head harness. Each still fails exactly these 2 checks (`receipts/reviewer-mutants/summary.txt`). **Resolved.**

### 3. Taken suggestions

**Length-30 refusal row.** The row is at `sim_main.cpp:1005-1011`: Table 11-10 fields in place plus two octets, lengthField 30, no other TLV. It expects refusal with no w11.

Its mutant is at `mutants.py:388`. It takes any lengthField of at least 28 and re-bases the organizationId and word-11 offsets on the captured length. That makes it a real "accepts a longer information TLV" defect. Plain `>= 28` alone would still miss the identifiers, so it would prove nothing. The mutant is caught on 3 checks (`parser_mutants.log:32`).

**X3 and X4.** Both are named:
- X3 is a zero-length header at messageLength counted as cut: the cut-after mutant.
- X4 is the last declared octet not walked: `:408`.

**Word-11 offset mutant.** At `:317`, `FU_LEFT_AT_TBI_C` changes from 17 to 15. It names "#98 plain fu: w11 as the plain case", "fu w11" and "#98 unknown TLV first: w11 …", and is caught (`:19`).

**Isolated docs selftest.** `python3 -I scripts/check_docs.py --selftest` gives rc 0 and "PASS (127 arms)":
- from the repository root: `receipts/gates/docs_selftest_I.*`;
- from `/tmp`: `docs_selftest_I_from_tmp.*`.

The plain invocation gives the same output (`docs_selftest.*`). `_load_sibling` (`scripts/check_docs.py:644`) uses `types` and `importlib.util`, both already imported.

### 4. Residue and counts

**R771-1 R1.** Both texts are applied verbatim, with no change of meaning:
- `tb/verilator/engine/sim_main.cpp:3423-3425`: "(refused at end of frame: the TLV is skipped and the chain holds no information TLV, #98)".
- `:3501-3502`: "the span of the former fixed Follow_Up TLV header arm (octets 44..59, before #98)".

**R771-1 R2 / R772-1 R1.** `docs/HDL_DEVELOPER.md:44` reads "The first information TLV supplies word 11." and `:46` reads "A malformed chain still refuses the Follow_Up." This is the assignment's two-sentence text, and it supersedes my round 1 single-sentence wording with the same meaning.

**Counts.** All agree with what make reports:
- Makefile `:23`: "Thirty-four defects".
- `mutants.py` docstring: 8 + 7 (#87/#88, corrected from "Six") + 19 (#98) = 34. I counted the `MUTATIONS` entries: 8 rx_err, 7 #87/#88, 19 #98.
- `docs/TEST_DEVELOPER.md:125`: "thirty-four parser defects, nineteen for the TLV walk".
- PR body: "482 checks", "34 defects and the control", "19 of the defects for #98", "35/35", "Six new parser mutants. One mutant is reworked". Round 1 had 28 defects, 13 of them for #98; 13 + 6 = 19.
- make reports: parser 482/482 (`receipts/gates/parser_run.log`) and arm "35 checks: 35 PASS, 0 FAIL" (`parser_mutants.log:37`).

### Comment rule

Every line the delta adds is free of bench lane labels, lane names, review rounds, reviewer IDs and issue-comment IDs. The scan for `B\d+`, `R77x`, `round`, `issuecomment`, `lane`, `reviewer`, `X1-4`, `F1` and `S1/S2` returns no hit. The new comments cite #98, 802.1AS-2011 11.4.4.3.3 and IEEE 1588-2008 5.3.8.

## Executed evidence (this review, pinned simulator 5.050)

- **Simulator.** The pinned wrapper's `--version` gives "Verilator 5.050 2026-07-01 rev v5.050". It was first on PATH for every build.
- **Clone.** All gates ran on a fresh clone at the exact head (`scripts/run_gates.sh`). Its working tree was clean afterwards. In `parser_run.log` and `engine_run.log`, I replaced the simulator's install-root prefix with `<verilator-5.050-root>`; no other byte was edited.

| Run | Result | Receipt |
|---|---|---|
| Parser suite (`make run`) | 482 checks: 482 PASS, rc 0 | `receipts/gates/parser_run.*` |
| Parser mutation arm | 35/35: the control plus 34 defects; all 19 #98 mutants caught on every named check; rc 0 | `receipts/gates/parser_mutants.*` |
| Engine suite (`make run`) | 2048 ×3 + 60, all PASS, rc 0 | `receipts/gates/engine_run.*` |
| Engine mutation arm | Started, then stopped by me. It is serial, and the author's exact-head receipt took about 12,350 s. The round 2 engine delta has no non-comment line. I relied on the hash-verified author receipt instead (see below) | `receipts/gates/engine_mutants.STOPPED.txt` |
| `scripts/check_docs.py` | "docs check: PASS (14 current pages, 18 historical pages)", rc 0 | `receipts/gates/docs_gate.*` |
| `--selftest`, plain, `-I`, and `-I` from `/tmp` | "PASS (127 arms)" each, rc 0 | `receipts/gates/docs_selftest*.*` |
| `git diff --check 3e3a4e7 762fbd6` | rc 0, empty | `receipts/gates/diff_check.*` |
| Reviewer mutants (round 1's three plus the latch deletion), unmodified head harness | Each fails exactly the named checks listed above | `receipts/reviewer-mutants/` |
| Reviewer probe rows (round 1's plus five round 2 shapes), head RTL | 555 checks: 555 PASS | `receipts/probes/probes-head-rtl.log` |
| The same probe harness, head RTL with the latch deleted | 555 checks: 537 PASS, 18 FAIL. The 6 arm checks, round 1's 0xFFFE-first probe, and all five round 2 probes (see R771-2-R1) | `receipts/probes/probes-latch-deleted-rtl.log` |

**Round 2 probe shapes.** All five are refused at head with one drop and no event:
- a past-messageLength header after the information TLV, then a zero-length header ending at messageLength;
- an odd header after the information TLV, then a zero-length header at the end;
- frame A padded by 8 octets;
- two malformed headers ahead of the information TLV;
- an odd header after the information TLV, then another TLV to the end.

With the latch deleted, each is accepted: event, no drop. No probe showed an RTL defect.

**Published author evidence (spot-checked).** `scripts/verify_evidence.py` checked 11 receipts against the published `MANIFEST.json`. All 11 match, rc 0 (`receipts/evidence-spotcheck.txt`):
- **Engine arm.** `repo-head-arm/results.json` is for head `762fbd67`, rc 0. Its log reads "136 checks: 136 PASS, 0 FAIL", and its verdict and fail-line diffs against base are empty.
- **Parent consumer gates.** `parent-head-A` shows 19 commands, all rc 0, with `xvlog` stating "gptp-processor@762fbd67". They cover:
  - cpp/py idiom and xvlog;
  - gptp_shadow;
  - `milan_dp gptp` and `gptp-lat`;
  - gm_steps, plane, txts, tables;
  - tsn_fuzz ptp;
  - a clean status check.

**Hosted checks.** The PR's status rollup at this head is empty: no hosted context was executed or skipped.

## Findings

### R771-2-R1: RESIDUE (Docs, Tests)

- **Where:** `tb/verilator/parser/mutants.py:45-46` (module docstring): "and the refusal latch itself, which only a malformed header ahead of a well-formed information TLV can show."
- **Evidence:** With the latch deleted, the head RTL also accepts a malformed header *after* the information TLV when the octets behind it still read as a well-formed chain, such as `{INFO, {0x000A,0x0100}, ZERO_LEN}` or `{INFO, {0x000A,1}, ORG_OTHER}`. The result is event 1, drops +0, where head refuses (`receipts/probes/probes-latch-deleted-rtl.log`, "R2 … after info" rows). The PR body's narrower statement, that only the two new rows *in the suite* catch it, is true. The docstring's general "only … can show" is not.
- **Impact:** Wording only. No test, count, figure or verdict changes.
- **Exact fix:** Replace "and the refusal latch itself, which only a malformed header ahead of a well-formed information TLV can show." with "and the refusal latch itself, which a malformed header shows only when the octets after it still read as a well-formed chain, as ahead of a well-formed information TLV."
- **Verification:** Read `mutants.py:45-46` at the next head. `make -C tb/verilator/parser mutants` still reports 35/35.

### R771-2-S1: SUGGESTION (Tests, Robustness)

The latch is now pinned only where the malformed header comes ahead of the information TLV. A refusal row for the trailing position would pin it in both positions:
- the row: `{INFO, {0x000A, 0x0100, {}}, ZERO_LEN}`;
- its checks: no event and one drop, with no "no w11" check, because word 11 is written before the malformed header;
- the latch mutant would also name this row.

`receipts/probes/` shows head refuses this shape and the latch deletion accepts it.

### R771-2-S2: SUGGESTION (Docs)

My round 1 exact fix at `tb/verilator/engine/sim_main.cpp:3501-3503` now leaves two parentheticals back to back and a short wrapped line: "(octets 44..59, before #98) (octets past messageLength are padding to a receiver whatever their count). Each is accepted". An optional merge would read "(octets 44..59, before #98; octets past messageLength are padding to a receiver whatever their count)", followed by a reflow. The applied text is exactly what was asked, so this is not a defect.

### R771-2-S3: SUGGESTION (Docs)

Optional wording polish:
- `docs/TEST_DEVELOPER.md:123`: "Refuses an information TLV whose lengthField is not 28." could read "Refuses a 00-80-C2/1 TLV whose lengthField is not 28." A TLV of another length is, by 11.4.4.3.3, not the information TLV.
- `mutants.py:48-49`: "…without one of its four header values, or with any lengthField of at least 28" has a double "or". It could read "…without one of its four header values or with any lengthField of at least 28".

## Prior findings at this head

| Finding | Status at `762fbd67` | Evidence |
|---|---|---|
| R771-1-F1 MINOR (Tests) | RESOLVED | Item 2 above; `parser_mutants.log:33-35`; reviewer mutants fail exactly the 2 named checks |
| R771-1-R1 RESIDUE | RESOLVED, text exact | `engine/sim_main.cpp:3423-3425`, `:3501-3502` |
| R771-1-R2 RESIDUE | RESOLVED, assignment text | `docs/HDL_DEVELOPER.md:44`, `:46` |
| R771-1-S1 SUGGESTION | TAKEN | `parser/sim_main.cpp:1005-1011`; `mutants.py:388` caught |
| R771-1-S2 SUGGESTION | TAKEN | `mutants.py:317` caught, naming "#98 plain fu" |
| R771-1-S3 SUGGESTION (pre-existing) | NOT TAKEN by manager decision; retained for awareness only, no action | outside the 1514-octet boundary; predates #98 |
| R772-1-F1 MINOR (Tests, Robustness) | RESOLVED | Item 1 above; latch mutant caught on 6 checks; walk, end-of-frame and cut halves each caught alone |
| R772-1-S1 SUGGESTION | TAKEN | length-30 row; X3 and X4 named (`mutants.py:399`, `:408`) |
| R772-1-S2 SUGGESTION | TAKEN | `-I` selftest rc 0 from the root and from `/tmp` |
| R772-1-R1 RESIDUE | RESOLVED, text exact | `docs/HDL_DEVELOPER.md:44`, `:46` |

## Lens evidence

**Conformance: CLEAN.** The delta adds refusal rows that pin three rules:
- 802.1AS-2011 11.4.4.3.3: lengthField 28;
- 11.4.2.2: the value must end within messageLength;
- IEEE 1588-2008 5.3.8: an odd lengthField is refused.

The last two are pinned ahead of a well-formed information TLV, and head refuses each shape. The RTL is unchanged, so the round 1 conformance verdict on the walk carries.

**RTL: CLEAN.** The `hdl/` tree is identical across the delta (`receipts/restore-and-identity.txt`). No new row or reviewer probe shows an RTL defect: 482/482 and 555/555 at head. Round 1's RTL verdict carries.

**Robustness: CLEAN.** The malformed-header shapes are refused at head, ahead of and after the information TLV, padded or not, singly or two in a row. The refusal latch is now proven by name. The docs selftest no longer depends on the interpreter's path setup.

**Tests: CLEAN (S1 open as a suggestion).** Suite 482/482 and arm 35/35. Every new mutant is caught on every check it names, with the control passing. Each term of the split is proven alone. My independent mutants confirm the named checks are exactly the ones that fail.

**Docs: CLEAN (R1 carried as residue; S2 and S3 suggestions).** The two residue texts are applied, the counts agree with what make reports, and the docs gate and selftest pass. Comments in the delta follow the comment rule.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | parser rows `sim_main.cpp:960-1011` against 802.1AS-2011 11.4.2.2 / 11.4.4.3.3 and IEEE 1588-2008 5.3.8; `hdl/` tree identity; probe rows | R771-2 (delta); walk RTL R771-1 | 762fbd6716b50337e7644a4918c216b3143aeb5b |
| RTL | CLEAN | `hdl/` tree `360f2459…` unchanged across `5b10675c..762fbd67`; parser 482/482; probes 555/555 at head | R771-1 (carried; delta changes no dependency) | 762fbd6716b50337e7644a4918c216b3143aeb5b |
| Robustness | CLEAN | five round 2 probe shapes at head and with the latch deleted; `scripts/check_docs.py:636-655` under `-I` from two cwds | R771-2 | 762fbd6716b50337e7644a4918c216b3143aeb5b |
| Tests | CLEAN | `mutants.py` (docstring, anchors, 19 #98 entries), `parser/sim_main.cpp` new rows, `parser/Makefile`; arm 35/35; reviewer mutants; author engine-arm receipt 136/136 (hash-verified) | R771-2 | 762fbd6716b50337e7644a4918c216b3143aeb5b |
| Docs | CLEAN (RESIDUE R771-2-R1 carried) | `docs/HDL_DEVELOPER.md:44-46`, `docs/TEST_DEVELOPER.md:117-125`, `engine/sim_main.cpp:3414-3430` / `:3495-3510`, `mutants.py:1-52`, PR body counts and round 2 section; docs gate and selftest | R771-2 | 762fbd6716b50337e7644a4918c216b3143aeb5b |

## Real limits

- **Engine mutation arm.** I did not rerun it to completion: it is serial and takes about 3.4 h. The round 2 engine delta is comment lines only, and the author's exact-head receipt (136/136, empty diffs against base) is hash-verified against the published manifest.
- **Parent consumer gates.** I did not run them. The author's `parent-head-A` receipts at gitlink `762fbd67` were spot-checked by hash and exit code only.
- **Gates outside the delta.** I did not rerun OOC, area or timing, `make contract`, lint, ucpu, gaskets, tsngen or `bench/arty`. The delta touches none of their inputs, and the PR body states the OOC reports are identical to round 1's.
- **Hardware.** Physical calibration was NOT RUN. Simulation results and field skips are not hardware proof.
- **Hosted checks.** None are reported for this head.
- **Restore.** After the runs, the review clone is at the exact head with a clean index and worktree (ignored files included). `git write-tree` equals the head tree `1354fd45…`, and the repository has no submodule gitlinks (`receipts/restore-and-identity.txt`).

## Pending manager duties

- At the merge turn, build and validate the current-dev merge candidate (source base `3e3a4e7`, live dev `604899c0`) with the builder and native banks, and link the receipts on the PR.
- Own hosted and act acceptance.
- Carry R771-2-R1 to the residue checklist.
- Round 1 noted that the parent's imported gPTP docs gate (`check_gptp_docs.py --with-submodule`) fails on donor deep links pinned to `135afd04` at any gitlink move. That gate belongs to the merge-candidate turn.

## Reproduction (portable)

1. Clone the repository at `762fbd67`.
2. Run `scripts/run_gates.sh <clone> <outdir>`. It puts pinned Verilator 5.050 first on PATH.
3. Run `scripts/run_probes.sh <tree> <outdir> <log>`. Set `RTL=<edited parser>` to run the same probe harness against a mutated parser.
4. Run `python3 -I scripts/reviewer_mutants.py <tree> <work> <out>`.
5. Run `python3 -I scripts/verify_evidence.py <evidence dir> <files…>`.

`probe_splice.py` and `r771_probes.cpp` are the probe rows: round 1's, plus a round 2 block.

R771-2 FINISHED

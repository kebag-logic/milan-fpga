[R821] POSITIVE - exact head d3e61e37aa9ff50949d3561bc061bc610163ffbc

# R821-7: internal cleared-context delta review of PR #881 (issue #871, S11 AECP REBOOT), round 7

- **Head:** `d3e61e37aa9ff50949d3561bc061bc610163ffbc`, tree `6f55d8a0bd34c52b5fc6d22eb10a0f7500f27882`. The live PR head equals it, and the PR is not a draft.
- **Delta:** `33b0d03a..d3e61e37`. One commit by the executor, four files, +9/-9. It changes Markdown, comments and whitespace only.
- **Prior state:**
  - R821-6 was NEGATIVE at `33b0d03a` on F1-R6 (MINOR, Docs), with RS-R6-1 (RESIDUE) and S-R6-1 (SUGGESTION).
  - R822-5 was POSITIVE at `d3566d44`.
- **Verdict: POSITIVE.**
  - F1-R6 is resolved at its cause. The cell now reads `285 (250)`. All 11 parentheses of the table equal round 22's figures at `8684993388`, and every head figure equals `poll_grade.STATED_US`.
  - RS-R6-1 is resolved as prescribed. No word changed and no code line changed.
  - No firmware image changed.
  - Every gate I reran is rc 0.
  - Two new wording/layout residues are recorded below. Neither blocks the verdict.
- **Scope:** I wrote my own pass over the delta, the probes and the lens results before reading R821-6's findings. I then read R821-6 only to check how its findings were resolved. I read no other reviewer's report for this round.

## Inputs, in order

1. AGENTS.md (sections 3 and 5 to 8) and CONTRIBUTING.md, through AGENTS.md's contract: the lens, severity, verdict and ledger rules. Also docs/README.
2. Issue #871 (read-only through the CLI).
   - Its frozen scope: AECP REBOOT (IEEE 1722.1-2021 7.4.43), with the SUCCESS response before the reset port, and the journal.
   - Its acceptance items 1 to 5.
   - The manager's ruling on R821-6, as carried by the round-7 review start (PR #881 issuecomment-6902259404) and REVIEW READY (#871 issuecomment-6902228089). The ruling covers F1-R6 and the PR body row, RS-R6-1 exactly, and S-R6-1 out of scope.
3. Interface authorities for the delta:
   - `docs/design/SPLIT_CONTROL_MEMORY.md` "The polls by source" (header `:2231`, legend `:2243`);
   - `tb/verilator/ctrl_service_budget/poll_grade.py:67-94` (`STATED_US` and its docstring);
   - `sw/firmware/ctrl/plat/ctrl_plat.h:28-46`;
   - `sw/firmware/ctrl/test/test_plat_boot.cpp:183-215`.
4. `git diff 33b0d03a..d3e61e37` and its history:
   - `git show 8684993388` for round 22's table;
   - `git log -S` on the `adp_full` comment back to `88b0fcd105`;
   - the base `1d6bf555` version of `test_plat_boot.cpp`.
5. The author packet `review-evidence/665s11-r1/author-r7` at archive `018a4ca2`, plus the author-r6 identity receipts at the same archive.
   - The archive commit is unsigned (`%G?` = N).
   - Of the INDEX's 188 rows, 182 match by size and sha256 prefix. Six docs.yml and firmware-unit logs differ: each is shorter than indexed and carries `<scratch>` path redactions, which is consistent with publisher redaction. None is missing and none is unindexed (`receipts/packet-index-audit.txt`).
   - This shows hash consistency, not an independent signer.
6. Prior public findings: R821-6 (PR #881 issuecomment-6901483802), read after my own pass.

## What was executed

Scripts are under `scripts/` and receipts under `receipts/`. `receipts/commands.log` lists each command.

| What | Result | Receipt |
|---|---|---|
| `round22_parens.py`: every cell of the polls table at the head against round 22's `8684993388` row and against `poll_grade.STATED_US` | 18 cells, 11 parentheses, 0 differing, rc 0 | `round22-parentheses.txt` |
| Negative control: the same script at `33b0d03a` | rc 1, flagging only `retained col1 285 (280)` against round 22's 250 | `round22-parentheses-negative-control-33b0d03a.txt` |
| `text_identity.py`: word sequence with comment markers removed, plus non-comment lines exactly, `33b0d03a` against the head, for the three rewrapped files | all `IDENTICAL-TEXT`, code lines `EQUAL`, rc 0 | `text-identity.txt` |
| Negative control: the same script on `SPLIT_CONTROL_MEMORY.md` | `CHANGED`, rc 1 | `text-identity-negative-control.txt` |
| `ctrl_plat.h` comment-stripped token stream (`gcc -fpreprocessed -dD -E -P`) at both heads | sha256 equal. The header has no `__LINE__` or `assert(`, so the +1 line shift cannot reach code | `ctrl_plat_h-tokens.txt` |
| Image identity: the author's r7 `sha256.txt` against the author's r6 receipts for `33b0d03a` and `d3566d44` | 8 of 8 lines equal at both (fixture and platform, ELF and loadable binary, 1x1_tdm8 and 8x8) | `image-identity-compare.txt` and the three `*-identity-*.sha256.txt` |
| Gates at the head: `git diff --check 1d6bf555 HEAD`, `git diff --check 33b0d03a HEAD`, `docs_check.py`, `check_doc_style.py`, `check_py_idiom.py`, `check_cpp_idiom.py`, and an AST parse of `poll_grade.py` | all rc 0. docs_check: 0 findings over 220 md files | `gates/*.log`, `gates/*.rc` |
| `platboot.py` (`plat_arms.arm_platboot` at 1 and 2 interfaces), which compiles and runs `test_plat_boot.cpp` | if1 23 of 23 passed, if2 23 of 23 passed, rc 0 | `gates/platboot.log` |
| The author's workflow receipts (`receipts/wf`) | 71 `.rc` files, all 0. firmware-unit shows the saved-state gate with 526 tests, coverage PASS on 39 files and `[ok] arm platboot` | packet `receipts/wf/` (spot-checked) |
| Hosted snapshot at the head (read-only) | 11 success, 1 skipped (Physical gPTP, nightly/manual), 17 in progress, 21 queued at 2026-11-15T22:34:37Z. This is not a verdict; the manager owns hosted acceptance | `hosted-snapshot.tsv` |
| State of the review clone after the probes | HEAD and tree exact; porcelain, index and worktree clean; 0 untracked files; the four delta blobs' modes and hashes equal HEAD's; gitlinks unchanged | `clone-integrity.txt` |

The review clone was never edited, so there was nothing to restore.

The gitlinks are:
- gptp-processor `135afd04`;
- protocol-processor `a9e84b66`;
- lwSRP `08ee86e8`;
- tsn-c-stack `715589c1`;
- verilog-axis `48ff7a7e`;
- external `efeb541a` (not initialised).

## The assignment's items

### (1) F1-R6: the polls table's retained row

- `SPLIT_CONTROL_MEMORY.md:2238` reads `| retained | ... | 285 (250) | 365 (395) |`.
- At round 22's `86849933881c0c93a6435f8bc720d33f1577fe94`, the same row (`:2053` there) reads `| 250 | 395 |`.
- My script checks all 18 cells against round 22's row and against the head's gate values:
  - Each of the 11 parentheses equals round 22's figure.
  - Each of the 7 bare cells (withdraw 90/245, rebuild 290, walk 60, reclaim 25/35, mrpdu 1,215) equals round 22's figure unchanged.
  - Every head figure equals `poll_grade.STATED_US` (`poll_grade.py:91-94`).
- The script would have failed on the defect: at `33b0d03a` it flags exactly the old `285 (280)`.
- The legend `:2243` ("Each figure in parentheses was round 22's") now holds for every cell.
- The PR body:
  - In both the packet and the live body, the round-6 row says "`285 (250)` since round 7 (round 22's figure in parentheses, as the table's legend states)" (live line 51).
  - The F1-R6 row says `285 (250) | 365 (395)` (live line 40).
  - No `(280)` remains in the live body.
  - The live body differs from the packet only by the manager's author-packet link line, inserted at line 18, which shifts the later lines.
- **Resolved.**

### (2) RS-R6-1: the three rewraps

- **`test_plat_boot.cpp:189`:** the last two lines are joined into "the room it last read is short (mbx.c), reads it at each send; else the model's" (82 columns). This is exactly the prescribed text.
- **`poll_grade.py:72-73`:** the short line is refilled from the next line (now 113 columns). This is as prescribed. The short line moved down one, to `:74` (see RS-R7-1).
- **`ctrl_plat.h:38-42`:** the paragraph's tail is rewrapped to 74 to 78 columns, matching its neighbours.
- Word sequences are equal for each file, and so are the non-comment lines (`text-identity.txt`).
- The `ctrl_plat.h` token stream is equal (`ctrl_plat_h-tokens.txt`).
- **Resolved.**

### (3) No firmware image changed

- The delta's only firmware-image input is `ctrl_plat.h`. Its comment-stripped token stream is identical, and nothing in it expands `__LINE__`.
- The author's r7 hashes for the 8 split image files equal the author's published r6 hashes at both `33b0d03a` and `d3566d44`, all 8 of 8.
- `test_plat_boot.cpp` is a host test and `poll_grade.py` is a harness grader. Neither is an image input.

### (4) The rerun gates

- My reruns are all rc 0: whitespace against the merge base and `33b0d03a`, both idiom gates, `docs_check.py`, `check_doc_style.py`, and the boot arm at one and two interfaces.
- The author's docs.yml and firmware-unit receipts are rc 0 throughout (spot-checked).

### Comment rule

- The added comment lines in the delta carry no bench lane labels, lane names, review rounds, reviewer IDs or comment IDs.
- `ctrl_plat.h:38-42` cites nothing.
- `test_plat_boot.cpp:189` cites `mbx.c`.
- `poll_grade.py:73` cites `#665`.

## Findings

No BLOCKER, MAJOR or MINOR.

### RESIDUE

- **RS-R7-1 (Docs; layout only):** the `poll_grade.py` refill moved the short line instead of removing it.
  - **Where:** `tb/verilator/ctrl_service_budget/poll_grade.py:74`. The line `#: cuts), over every group of both arms. On the merge` is 53 columns among 111- to 119-column neighbours (`:65-89`).
  - **Authority:** RS-R6-1's intent was a paragraph without ragged lines. The fix was applied as literally prescribed ("refill it with the next line"), so the raggedness moved from `:73` to `:74`.
  - **Impact:** layout only. The words, code and gate values are unchanged.
  - **Exact fix:** refill `:73-80` to the neighbours' width (no more than 119 columns) with the words unchanged, so that no line short of the paragraph's last ends mid-sentence.
  - **Verification:** `text_identity.py` reports `IDENTICAL-TEXT`, and `check_py_idiom.py` over-long line stays 0.

- **RS-R7-2 (Docs, Tests; comment placement, pre-existing in the lane, not introduced by this round):** a function's comment no longer heads its function.
  - **Where:** `sw/firmware/ctrl/test/test_plat_boot.cpp:185-186`. The comment "mbx_hal.h on the model, every access in the shared order; another contract's bitstream answers ID without this contract's magic" documents `mbx_hal_read32` (`:198`).
  - **Evidence:** at the base `1d6bf555` it sat directly above `mbx_hal_read32` (`:118-120` there). Since `88b0fcd105` it heads the `adp_full`/`adp_one`/`kAdpRecord`/`busy_ch`/`aecp_full` declarations instead. As a result, two unrelated comments run together (`:185-189`), and `mbx_hal_read32` has no heading comment.
  - **Impact:** wording and placement only. No test, code or figure changes.
  - **Exact fix:** move the two lines `:185-186` unchanged to directly above `extern "C" std::uint32_t mbx_hal_read32(std::uint32_t offset) {` (`:198`).
  - **Verification:** the moved words are byte-identical, and `platboot` if1 and if2 pass.

### SUGGESTIONS

- **S-R6-1 (Tests):** out of scope by the manager's ruling, which opens its own issue. Retained, not this lane's.
- **Optional suggestions from earlier rounds:** R821-5 S1 and S2, and R822-5 S1 to S13, remain optional and untaken.

## Prior findings, resolved or retained at this head

| Finding | State at `d3e61e37` | Evidence |
|---|---|---|
| R821-6 F1-R6 (MINOR, Docs) | **Resolved**: `285 (250)`; all 11 parentheses are round 22's; the PR body's rows agree | item (1); `round22-parentheses.txt` |
| R821-6 RS-R6-1 (RESIDUE) | **Resolved** as prescribed, with words unchanged. Its `poll_grade.py` part leaves RS-R7-1 | item (2); `text-identity.txt` |
| R821-6 S-R6-1 (SUGGESTION) | Out of scope; the manager opens its own issue | review start |
| R821-5 F1 (MINOR, Tests, Docs) | Tests part resolved at R821-6. Its Docs part, which became F1-R6, is resolved here | item (1) |
| R821-5 RS-1, RS-2; R822-5-R1 to R3 (RESIDUE) | Resolved at R821-6; the delta does not touch them | `git diff 33b0d03a..d3e61e37` |
| R821-5 S1, S2; R822-5 S1 to S13 (SUGGESTION) | Retained, optional | not taken by the ruling |

No BLOCKER or MAJOR from any earlier round is open.

## Lens results (each at `d3e61e37`)

```text
[R821] PASS Conformance - SPLIT_CONTROL_MEMORY.md:2231-2243 against 8684993388:docs/design/SPLIT_CONTROL_MEMORY.md:2046-2056 and poll_grade.py:91-94; receipts/round22-parentheses.txt - every stated figure equals its gate value and every parenthesis its round-22 figure; the delta changes no protocol path (IEEE 1722.1-2021 7.4.43 REBOOT, Milan v1.2 5.6.3.3 ENTITY_DEPARTING) and no acceptance item of #871
[R821] PASS RTL - git diff --name-only 33b0d03a..d3e61e37 (no hdl/, sw/litex/, CSR, census or SoC file); receipts/ctrl_plat_h-tokens.txt; receipts/image-identity-compare.txt - no RTL or SoC input; the only image input's token stream is identical, and 8 of 8 split image hashes equal 33b0d03a's and d3566d44's
[R821] PASS Robustness - ctrl_plat.h:28-46, test_plat_boot.cpp:185-196, poll_grade.py:65-94; receipts/text-identity.txt - no executable firmware, test or grader line changed (non-comment lines equal), so no malformed-input, reset, backpressure or timeout path moves
[R821] PASS Tests - receipts/gates/platboot.log (test_plat_boot.cpp built and run: if1 23/23, if2 23/23); receipts/gates/{py_idiom,cpp_idiom}.log; both negative controls (rc 1 on the defect) - the touched test compiles and passes at both shapes; the reviewer probes are shown to fail on the defect they check; RS-R7-2 is RESIDUE (comment placement)
[R821] PASS Docs - SPLIT_CONTROL_MEMORY.md:2238; PR #881 live body lines 40 and 51; ctrl_plat.h:30-42; receipts/gates/{docs_check,doc_style,diffcheck_*}.log - F1-R6's cell and the PR rows state round 22's 250; the rewrapped prose is word-identical; docs and style gates rc 0; RS-R7-1 and RS-R7-2 are RESIDUE
```

## Reviewer-owned ledger

- **Coverage outside the delta:** coverage of the rest of the PR carries from R821-5 (`d3566d44`) and R821-6 (`33b0d03a`). This delta changes nothing those lenses depend on beyond the four files named below.
- **Earlier UNCLEAN lens:** Docs, which was UNCLEAN at R821-6, is covered clean here.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | polls table against round 22's `8684993388` and `poll_grade.STATED_US`; delta file list against #871 scope | R821-7 | `d3e61e37aa9ff50949d3561bc061bc610163ffbc` |
| RTL | CLEAN | delta file list (no RTL, SoC or image input except `ctrl_plat.h`); `ctrl_plat.h` token stream; 8 image hashes against r6's two heads | R821-7 | `d3e61e37aa9ff50949d3561bc061bc610163ffbc` |
| Robustness | CLEAN | `ctrl_plat.h`, `test_plat_boot.cpp`, `poll_grade.py`, non-comment lines equal | R821-7 | `d3e61e37aa9ff50949d3561bc061bc610163ffbc` |
| Tests | CLEAN | `test_plat_boot.cpp` built and run at if1 and if2; idiom gates; probe negative controls | R821-7 | `d3e61e37aa9ff50949d3561bc061bc610163ffbc` |
| Docs | CLEAN | `SPLIT_CONTROL_MEMORY.md` polls table and legend; PR #881 live body; rewrapped comments; `docs_check`, `doc_style`, `diff --check` | R821-7 | `d3e61e37aa9ff50949d3561bc061bc610163ffbc` |

## Real limits

- **Firmware images not rebuilt:** I did not rebuild them. Image identity rests on:
  - the author's published r7 hashes compared with the author's published r6 hashes;
  - my independent token-stream identity of `ctrl_plat.h`, the only image input in the delta.
- **Workflows:** I did not rerun the full firmware-unit, docs.yml or load/flip/polls workflows. I ran the boot arm that compiles the touched test and the lightweight gates. The rest is the author's receipts, spot-checked: 71 of 71 rc 0.
- **Packet signature:** the packet archive commit is unsigned. Six INDEX rows differ, consistent with publisher path redaction. Hash consistency is not independent provenance.
- **Hosted runs:** they were still running at the snapshot. Executed jobs are distinct from the skipped nightly/manual Physical gPTP context.
- **Hardware:** physical calibration was NOT RUN, and field skips are not hardware proof.
- **Manager source bank:** none ran at this head, and none is claimed or inferred.

## Pending manager duties

- **Merge candidate:** build and validate the current-dev merge candidate (source base `1d6bf555`; live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a`), with the builder and native banks, at the merge turn, and link its receipts on the PR.
- **Hosted and act acceptance** at the exact head, including `verilator-suites` and `yosys-portability`.
- **Residues:** carry RS-R7-1 and RS-R7-2 to the residue checklist.
- **Acceptance item 1:** the PR still says `Relates to #871`, because acceptance item 1 is met for six of eight items. The issue's closure stays the manager's and maintainer's decision.
- **Merge authorization:** obtain the maintainer's explicit merge authorization.

R821-7 FINISHED

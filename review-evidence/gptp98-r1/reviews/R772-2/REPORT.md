[R772] POSITIVE - exact head 762fbd6716b50337e7644a4918c216b3143aeb5b

# R772-2 external independent review: Mister-M-alt/FPGA-gPTP PR #99 (issue #98), round 2

- Exact head `762fbd6716b50337e7644a4918c216b3143aeb5b`, tree `1354fd45f1bb7dbe0e967367731243a2d2049d97`. Source base `3e3a4e7695ce66eed609089f280c2fba45b24d36`. Live parent dev `604899c08ff1cd1830e1dd08b733109ef852400c`.
- Round 2 delta judged: `5b10675c..762fbd67`, four commits (`fc13a65`, `a030c62`, `6e27cd6`, `762fbd6`). `hdl/` is byte-identical to round 1 (`receipts/diff_check.log`). Files touched: `tb/verilator/parser/{sim_main.cpp,mutants.py,Makefile}`, `tb/verilator/engine/sim_main.cpp` (comments only), `scripts/check_docs.py`, `docs/HDL_DEVELOPER.md` and `docs/TEST_DEVELOPER.md`.
- Inputs, in this order:
  - README and docs/README. The repository has no AGENTS.md or CONTRIBUTING.md.
  - The issue #98 body (acceptance 1-4) and the round 2 assignment on the issue (issuecomment-6640832434).
  - The PR #99 body at this head.
  - The delta diff and its history.
  - The round 1 public findings of both reviews. I read these only after my own pass over the delta.
  - Published evidence at kebag-logic/milan-fpga `59152409`, `review-evidence/gptp98-r1` (MANIFEST.json and `author-r2/receipts`).
- The other round 2 report on this PR was not read.

## Verdict

POSITIVE. Every round 1 finding is resolved at its cause, every taken suggestion is in place, and both residues were applied with the exact text the assignment names.

- The new rows for frames A and B catch the latch mutant by name: 6 named failures, and no other row fails.
- The latch and the end-of-frame overrun term are each proven on their own.
- The three mutants that refuse the `#98 unknown TLVs after` chain are caught on ": event" and ": no drop", and the control passes.
- The counts agree everywhere with what `make` reports.

No MINOR, MAJOR or BLOCKER is open. One RESIDUE and one SUGGESTION are recorded below.

## Prior findings, resolved or retained at this head

| ID | Severity | Status at 762fbd67 | Evidence |
|---|---|---|---|
| R772-1 F1 | MINOR | **RESOLVED** | See item (1) below. |
| R772-1 S1 | SUGGESTION | **TAKEN** | The length-30 row is at `sim_main.cpp:1005-1011` and its mutant at `mutants.py:388-397`. X3 and X4 are named at `mutants.py:399-402` and `:408-411`. |
| R772-1 S2 | SUGGESTION | **TAKEN** | `scripts/check_docs.py:638-655`. `python3 -I` passes from the repository root and from `/tmp`. |
| R772-1 R1 = R771-1 R2 | RESIDUE | **APPLIED, exact text** | `docs/HDL_DEVELOPER.md:44` reads "The first information TLV supplies word 11." and `:46` reads "A malformed chain still refuses the Follow_Up." This is the text the assignment chose. |
| R771-1 F1 | MINOR | **RESOLVED** | See item (2) below. |
| R771-1 R1 | RESIDUE | **APPLIED, exact text** | `tb/verilator/engine/sim_main.cpp:3423-3425` and `:3501-3502` carry the review's replacement texts word for word. |
| R771-1 S1 | SUGGESTION | **TAKEN** | Same row as R772-1 S1. |
| R771-1 S2 | SUGGESTION | **TAKEN** | "word 11 read two octets late (#98)" is at `mutants.py:317-321` and names "#98 plain fu: w11 as the plain case". |
| R771-1 S3 | SUGGESTION | **NOT TAKEN** (manager decision) | The 11-bit counter wrap predates this PR and lies outside the 1514-octet boundary. Retained for awareness only. |

### (1) R772-1 F1: the latch and the end-of-frame term

**Rows.** Both rows are at `tb/verilator/parser/sim_main.cpp:995-1004`:

- Frame A: `{0x000A, 0x0100, {}}` then INFO, messageLength 80.
- Frame B: `{0x000A, 0x0001, {}}` then INFO.

Each calls `expect_fu_refused(..., true)`, so each expects no event, one drop and no w11 write. Both are byte-for-byte my round 1 demonstrator frames. `receipts/latch_demo_head.log` shows `events 0, drops 1` for each at head.

**Latch mutant.** "a malformed TLV header does not latch the refusal (#98)" (`mutants.py:340-346`) deletes exactly `bad_r <= 1'b1;` after `if (fu_tlv_header_bad_w) begin`.

- The arm reports it caught, failing all 6 named checks (`logs/parser_mutants.log:22`).
- My round 1 X1, the same edit, re-run against the head harness gives `482 checks: 476 PASS, 6 FAIL`.
- The 6 FAIL lines are exactly the 3 checks of each new row, with no other row failing (`receipts/extra_mutants_r2.log`). So the new rows are the load-bearing ones.

**The split, each half proven on its own.**

- **Walk half:** "a TLV value past messageLength is walked" (`mutants.py:327-333`) now edits only the latch condition. The end-of-frame gate is unchanged. The arm catches it on the `information TLV past messageLength` and `trailing TLV past messageLength` rows. My Y3 is the same edit and shows the same 5 FAIL lines.
- **End-of-frame half:** "an EOF header's own overrun is not refused" removes the header verdict from the gate only, and the latch is unchanged. It is caught on `#98 header ends messageLength, value to come`.
- **My finer probe Y1** removes only the overrun part at the end-of-frame gate and keeps the odd term and the latch. It is caught by the same row (2 FAIL). The overrun term at end of frame is therefore proven independently of the latch.
- **Cut term:** "a TLV header cut by messageLength is accepted" removes only the cut term (`mutants.py` FU_FIN edit). The arm catches it on all 6 cut rows.
- **My probe Y2** keeps only the overrun term at the latch. It is caught by `#98 odd lengthField` (3 FAIL). The odd half of the latch is covered too. At end of frame, the odd term is implied by the overrun term: an odd lengthField on a header ending at messageLength always overruns.

### (2) R771-1 F1: the `#98 unknown TLVs after` control

- `FU_AFTER = ("#98 unknown TLVs after: event", "#98 unknown TLVs after: no drop")` (`mutants.py:175-176`) is named by three mutants:
  - the cut-after mutant (`fu_tlv_cut_after_w` header-byte arm forced to 1, `:399-402`);
  - the zero-length-after mutant (a zero-length header with `fu_found_r` set latches `bad_r`, `:403-407`);
  - the last-octet mutant, X4 (`:408-411`).
- The arm reports each one caught on both checks (`logs/parser_mutants.log:33-35`).
- The control passes: the arm's line 1 PASS, and the parser suite gives 482/482 with 0 FAIL lines (`logs/parser_run.log`).
- The row (`sim_main.cpp:914`, `{INFO, ZERO_LEN, ORG_OTHER, ZERO_LEN}`) does end on a zero-length header at messageLength.

### (3) Taken suggestions

- **Length-30 row.** It is refused at head, and at base too: base fails only the 31 pre-existing #98 checks and none of the 9 new ones (`receipts/head_harness_on_base_rtl.log`, `482 checks: 451 PASS, 31 FAIL`), as the PR body states.
- **Length-30 mutant.** It loads lengthField and moves both offsets to `len-5` / `len-11`, which equal 23 / 17 at 28, so it is a faithful "any lengthField of at least 28" walk. It is caught on all 3 named checks.
- **Simpler variants.** My Y5 (`>= 28` only) and Y6 (any even length only), with the offsets unchanged, are both caught by `#98 identifiers at octet 6`.
- **Two-octets-late mutant.** It is caught on "#98 plain fu: w11 as the plain case", "fu w11" and "#98 unknown TLV first: w11 as the plain case" (`logs/parser_mutants.log:19`). My Y7, the same edit, fails 12 checks.
- **Docs selftest.** `python3 -I scripts/check_docs.py --selftest` gives `docs selftest: PASS (127 arms)`, rc 0, from the repository root (`logs/docs_selftest_isolated.log`) and from `/tmp` (`receipts/docs_selftest_isolated_tmpcwd.log`). The output is identical to the plain invocation (`logs/docs_selftest.log`). `make docs` rc 0 (`logs/make_docs.log`).

### (4) Counts

- `MUTATIONS` holds 34 entries: 8 rx_err, 7 for #87/#88 and 19 for #98, counted by name.
- These agree with each stated count:
  - `tb/verilator/parser/Makefile:23` ("Thirty-four");
  - the `mutants.py` docstring ("Seven belong to #87 and #88", "The last nineteen belong to #98"; the listed #98 defects number 19);
  - `docs/TEST_DEVELOPER.md:125` ("thirty-four parser defects, nineteen for the TLV walk");
  - the PR body ("34 defects and the control ... 19 of the defects for #98"; "Parser arm: 35/35"; "Parser suite: 482/482").
- `make` reports `35 checks: 35 PASS, 0 FAIL` (`logs/parser_mutants.log`) and `482 checks: 482 PASS, 0 FAIL` (`logs/parser_run.log`).
- The round 1 docstring said "Six" for a group of seven. `762fbd6` corrects it.
- The PR body's "Engine suite: 2,048 ×3 + 60" matches `logs/engine_run.log` (3 × `2048 checks: 2048 PASS`, then `60 checks: 60 PASS`).

## Findings (this round)

### R772-2 RES-1 - RESIDUE - lens: Docs

- **Where:** `docs/TEST_DEVELOPER.md:123`: "Refuses an information TLV whose lengthField is not 28."
- **Authority:** 802.1AS-2011 11.4.4.3.3 fixes the information TLV's lengthField at 28. A TLV with another lengthField is not the information TLV. The row's own comment says so (`tb/verilator/parser/sim_main.cpp:956-959`: "A 00-80-C2/1 TLV whose lengthField is even but not 28 ... is not the information TLV").
- **Problem:** The line is wording only. It names as "an information TLV" a TLV the walk does not take as one. It also leaves out the fact that the row is refused because no other TLV follows. A 00-80-C2/1 TLV of length 30 followed by a real information TLV is accepted.
- **Exact fix:** "Refuses a lone 00-80-C2/1 TLV whose lengthField is not 28." (ten words).
- **Impact:** None on any measurement, test or claim. The manager carries it to the residue checklist.

### R772-2 S1 - SUGGESTION - lens: Docs

- **Where:** `tb/verilator/engine/sim_main.cpp:3501-3504`. The R771-1 R1 replacement text was applied exactly as required. It now sits next to the existing parenthetical, giving "... arm (octets 44..59, before #98) (octets past messageLength are padding to a receiver whatever their count). Each is accepted" followed by a short wrapped line.
- **Optional:** turn the second parenthetical into its own clause ("...; octets past messageLength are padding to a receiver whatever their count.") and reflow the lines.
- This is optional polish and not a defect.

## Lens evidence

### Conformance: CLEAN

- The delta changes no RTL, so round 1's clause walk stands: 802.1AS-2011 11.4.1, 11.4.2.2, 11.4.4.3 / Table 11-10, 11.4.4.3.3, 1588-2008 5.3.8 and 14.1.
- The new rows match the clauses:
  - Frame A is refused because a TLV value must end within messageLength (11.4.2.2).
  - Frame B is refused because a lengthField must be even (5.3.8).
  - The length-30 TLV is not the information TLV (11.4.4.3.3).
- The independent 300,000-frame random-chain reference probe re-run at head gives `mismatches=0` and an EOF-to-event latency of 1 cycle (`receipts/diff_head.log`).
- Acceptance items 2 and 3 now hold for the mid-chain refusal shape that was missing in round 1.

### RTL: CLEAN

- `hdl/` is unchanged in the delta (`git diff --quiet 5b10675c 762fbd67 -- hdl` rc 0), so round 1's RTL verdict stands.
- The probes exercise the head RTL exactly: the mutants are staged from the head's own `KL_gptp_rx_parser.sv`, and each pattern is checked to occur exactly once.

### Robustness: CLEAN

- Frames A and B are refused at head (`receipts/latch_demo_head.log`).
- All 22 reviewer mutants (X1-X15 from round 1, Y1-Y7 this round) are caught by the head harness (`receipts/extra_mutants_r2.log`).
  - X1, which survived in round 1, is now caught by the harness. The random probe also catches it in 1,347 of 100,000 frames.
  - X6 and X15 survive only the random probe, which does not check word-11 writes on refused frames or bank writes. The harness catches both.
- `check_docs.py` `_load_sibling` resolves the sibling by `Path(__file__).resolve()` and registers it in `sys.modules` before executing it.
  - When run as a script, it loads `check_docs` under its module name, so the selftest module's `import check_docs` finds that same object.
  - Both the `-I` invocation and the plain invocation pass (127 arms) from any directory.

### Tests: CLEAN

- Parser suite: 482/482 at head (473 in round 1 plus 9: 3 rows × 3 checks).
- Parser mutation arm: 35/35. Every one of the 19 #98 mutants is caught on every check it names (`logs/parser_mutants.log:17-35`).
- Engine suite: 2048 ×3 and 60/60. The delta touches only comments in that file. The engine mutation arm was not re-run; the author's receipt reports 136/136.
- The head harness on base RTL fails exactly 31 checks, and none in the three new refusal rows (`receipts/head_harness_on_base_rtl.log`), as the PR body states.
- Each row named in the PR body's table maps to a mutant that fails it, checked against the arm output.

### Docs: CLEAN (RES-1 recorded as residue)

- `docs/HDL_DEVELOPER.md:44-46` carries the assignment's exact text.
- `docs/TEST_DEVELOPER.md:120-125` matches the suite and the counts, apart from RES-1.
- The engine comments carry R771-1 R1's exact text.
- The comment rule: I scanned the added lines of the delta for lane labels, lane names, review rounds, reviewer IDs, MR-style labels and issue-comment IDs. There are none. The added comments cite issue #98 and clauses (11.4.4.3.3, 11.4.2.2, 1588-2008 5.3.8). The only such label nearby ("the #18 review's MR7", `engine/sim_main.cpp:3500`) predates this delta and is tracked by #746.
- `make docs` rc 0, and `git diff --check 3e3a4e7..762fbd67` rc 0 (`receipts/diff_check.log`).
- PR body round 2 section: its statements check out against the receipts above. Its description of the split matches the arm and my Y1/Y3/Y4 probes.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | new rows against 11.4.2.2 / 5.3.8 / 11.4.4.3.3; 300,000-frame random reference probe at head; RTL unchanged since R772-1 | R772-2 | 762fbd6716b50337e7644a4918c216b3143aeb5b |
| RTL | CLEAN | `hdl/` byte-identity across the delta; mutant staging from head RTL; round 1 verdict carried | R772-2 (carries R772-1) | 762fbd6716b50337e7644a4918c216b3143aeb5b |
| Robustness | CLEAN | frames A/B at head; 22 reviewer mutants (X1-X15, Y1-Y7); `check_docs.py` sibling loader under `-I` from two cwds | R772-2 | 762fbd6716b50337e7644a4918c216b3143aeb5b |
| Tests | CLEAN | parser suite 482/482; parser arm 35/35 with named catches; engine suite; head harness on base RTL (31 FAIL); counts in Makefile, docstring, guide and PR body | R772-2 | 762fbd6716b50337e7644a4918c216b3143aeb5b |
| Docs | CLEAN (RES-1 residue) | HDL_DEVELOPER, TEST_DEVELOPER, engine comment residues, mutants.py docstring and comments, comment-rule scan, `make docs`, `git diff --check`, PR body round 2 section | R772-2 | 762fbd6716b50337e7644a4918c216b3143aeb5b |

## Real limits

- No manager source bank runs at this exact head, and none is claimed or inferred.
  - Source-head execution evidence beyond my own runs is the author's published receipts.
  - I checked five of them (`author-r2/receipts/INDEX.md`, `extra/r772-extra-mutants.log` and three parent-head-A JSON files) against the evidence MANIFEST.json, and all hashes match.
  - The evidence commit `59152409` carries no signature (`verification: unsigned`). "Signed packet" was therefore checked as manifest-hash integrity only.
- The parent consumer gates (gptp_shadow and the milan_dp gptp and gptp-lat legs included) are known only from the author's receipts. Each of the 19 entries reports exit code 0, on scratch parent head `768b3d60` over live dev `604899c0`. That parent commit is not public, so its gitlink to `762fbd6` was not verified independently. The parent gates were not run, as scope requires.
- Not run: the engine mutation arm and the µCPU suite. The delta does not touch the engine's behaviour, and the author reports 136/136. Also not run: the OOC/Vivado runs, the builder and tsngen suites, and any parent bank.
- The mutation and probe runs used the scoped Verilator 5.050 wrapper, not the host default 5.052.
- No copy of the standards was used. The clause reading is the reviewer's own.
- The random probe uses one seed, and it does not drive `rx_err_i`, inter-byte gaps or word-11 writes on refused frames. The repository harness covers those.
- Hosted evidence: 0 check runs and 0 statuses exist for this head.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, on source base `3e3a4e7`, live dev `604899c0` and this repository's gitlink `762fbd6`. Link the receipts on the PR.
- Own hosted/act acceptance.
- Carry RES-1 to the residue checklist. S1 is optional.
- Reconcile with the second independent round 2 review and the full completion bar.

## Reproduction (portable)

See `probes/README.md`. In short:

1. `python3 -I probes/extra_mutants_r2.py <tree> <work> 8`
2. `sh probes/build_diff.sh <tree>/hdl <obj>`, then `<obj>/Vdiff 300000`.
3. Build `probes/fu_latch_demo.cpp` the same way, then run it.
4. `make -C <tree>/tb/verilator/parser run mutants`, `make -C <tree>/tb/verilator/engine run`, `python3 -I <tree>/scripts/check_docs.py --selftest` and `make -C <tree> docs`.

The receipts are in `logs/` and `receipts/`; `receipts/identity.txt` records the head, the tree, the simulator and the post-probe clone state.

After the probes, the review clone is at HEAD `762fbd67` and tree `1354fd45`. `git status --porcelain --ignored` is empty, and the index and worktree equal HEAD. It has 114 tracked entries (110 × 100644, 4 × 100755) and no gitlinks. Two bytecode caches that the reviewer's count check created were removed.

R772-2 FINISHED

[R772] NEGATIVE - exact head 5b10675c3a22acc85bad7c150e1cd25984928385

# R772-1 external independent review: Mister-M-alt/FPGA-gPTP PR #99 (issue #98)

- Exact head `5b10675c3a22acc85bad7c150e1cd25984928385`, tree `405ab40b58cc53d6b57d819d83616c8c1b4d3fc7` (verified in the review clone; `receipts/clone_verify.txt`).
- Source base `3e3a4e7695ce66eed609089f280c2fba45b24d36`. Live parent dev `604899c08ff1cd1830e1dd08b733109ef852400c`, which pins this repository at `135afd04`.
- Delta reviewed: `git diff 3e3a4e7..5b10675`, four commits (`434527a` RTL, `dbe1acb` harness and mutants, `6f3f003` guides, `5b10675` docs-gate split). 13 files, +881/-396.
- Inputs, in this order: README, docs/README (the repository has no AGENTS.md or CONTRIBUTING.md), the issue #98 body and acceptance, the PR #99 body, the diff and history, the published evidence at kebag-logic/milan-fpga `b5042b8e` `review-evidence/gptp98-r1`, and the PR's review-start comments. The issue has no maintainer or manager scope comments beyond TAKEN and REVIEW READY.
- Prior public review findings on this PR: none. The PR has no reviews, and its only comments are the two review-start notices. There is nothing to resolve or retain.

## Verdict

NEGATIVE. The RTL change is correct against the clauses. An independent 300,000-frame random-chain check found 0 mismatches against a reference model written from the clauses. Area, timing and parent receipts match the PR. One MINOR Tests/Robustness finding is open (F1). A one-line parser defect makes the parser accept Follow_Ups that acceptance item 2 requires it to refuse, yet it passes the parser suite (473/473), the engine suite (60/60) and the mutation arm. Acceptance item 3 therefore does not yet prove the mid-chain refusal.

## Findings

### F1 - MINOR - lenses: Tests, Robustness

- **Where:** `tb/verilator/parser/sim_main.cpp:949-991` (`check_follow_up_tlv_walk_refuses`) and `tb/verilator/parser/mutants.py:313-332` (the #98 refusal mutants). The term left unproven is `hdl/wire/KL_gptp_rx_parser.sv:578-579`:

  ```
  if (fu_tlv_header_bad_w) begin
    bad_r <= 1'b1;
  ```

- **Authority:**
  - Issue #98, acceptance 2: a TLV whose length runs past messageLength is still dropped and counted.
  - Issue #98, acceptance 3: each refusal in 2 has a harness row with a parser mutant caught by name.
  - IEEE 802.1AS-2011 11.4.2.2: messageLength ends with the last TLV octet.
  - IEEE 1588-2008 5.3.8: TLV lengths are even.
- **Evidence:**
  - Deleting only the line `bad_r <= 1'b1;` (mutant X1) leaves the parser suite at 473 checks, 473 PASS (`receipts/extra_mutants.log`). The engine suite stays at 60 checks, 60 PASS (`receipts/engine_run_X1.log`). The repository's 29-entry arm does not contain this edit.
  - The same mutant accepts two Follow_Ups that the head RTL refuses (`receipts/latch_demo.log`, probe `probes/fu_latch_demo.cpp`):
    - A: `{tlvType 0x000A, lengthField 0x0100}` followed by the information TLV, messageLength 80.
    - B: `{tlvType 0x000A, lengthField 0x0001}` with no value, followed by the information TLV.
  - Results: head gives `events 0, drops 1` for both frames. X1 gives `events 1, drops 0` for both.
  - The reviewer's random-chain probe catches X1 in 1,347 of 100,000 frames.
  - The harness's refusal rows refuse under X1 only by coincidence. After the malformed header, their remaining octets never re-synchronise onto an information TLV, so the refusal still arrives through `!fu_found_r` or the end-of-frame cut term. The listed mutant "a TLV value past messageLength is walked" removes the latch and the end-of-frame term together, so neither one is proven on its own.
- **Impact:** #98 first makes a TLV ahead of the information TLV reachable. That is the shape where a lost latch turns a malformed chain into an accepted Follow_Up with an event and a word 11. No suite in this repository would flag that regression. The RTL at this head is correct; the gap is in the proof.
- **Required outcome:**
  1. Add parser rows "TLV past messageLength ahead of the information TLV" (frame A) and "odd lengthField ahead of the information TLV" (frame B). Each expects no event, one drop and no w11 write.
  2. Add a parser mutant that deletes the `bad_r <= 1'b1;` of the `fu_tlv_header_bad_w` branch, named against those rows.
  3. Update the defect counts in `tb/verilator/parser/Makefile`, the `mutants.py` docstring and the PR body.
- **Verification:**
  - `make -C tb/verilator/parser` passes at the new head, and the new mutant is reported caught by name.
  - `python3 probes/extra_mutants.py <tree> <work>` reports X1 `harness: CAUGHT`.

### S1 - SUGGESTION - lens: Tests

- No row checks an even wrong-length information TLV on its own (tlvType 3, lengthField 30, 00-80-C2/1). The existing `fu lengthField 27 drop` row is now refused by the odd-length rule, not by the length match.
- The `#98 unknown TLVs after` control row is the only row that catches reviewer mutants X3 (a zero-length header at messageLength counted as cut) and X4 (the last declared octet not walked). Neither is named in the arm.
- The RTL behaves correctly in all three cases (random probe, `receipts/diff_head.log`). Naming X3 and X4 and adding the length-30 row would pin them.

### S2 - SUGGESTION - lens: Robustness

- `scripts/check_docs.py:639` imports `check_docs_selftest` from the script directory on `sys.path`. As a result, `python3 -I scripts/check_docs.py --selftest` fails at head with `ModuleNotFoundError`, while it passes at base.
- The documented invocations (`make docs`, and `python3 scripts/check_docs.py` from any cwd) pass with 127 arms, and the parent's docs gate does not invoke this script.
- Loading the sibling module by its own path would remove the dependence on the interpreter's path setup.

### R1 - RESIDUE - lens: Docs

- **Where:** `docs/HDL_DEVELOPER.md:44`, which reads "The first information TLV accepts the Follow_Up."
- **Problem:** The sentence is imprecise. A later TLV that overruns messageLength, a header cut by messageLength, or an odd lengthField still refuses the Follow_Up. The RTL and `docs/TEST_DEVELOPER.md:120` say so.
- **Exact fix:** replace the sentence with two sentences: "The first information TLV supplies word 11." and "A malformed chain still refuses the Follow_Up." Each stays within the docs gate's ten-word limit.

## Lens evidence

### Conformance: CLEAN

**Clause walk, done by the reviewer against `hdl/wire/KL_gptp_rx_parser.sv`:**

1. The walk starts at octet 44 (frame byte 58). It is armed at `cnt_r == 57` (line 566).
2. Header bytes count only while `cnt_r <= msg_end_r` (line 365), so padding is never walked.
3. Each header's lengthField either loads `tlv_left_r` or keeps a zero-length TLV in header mode (lines 578-583).
4. The value is skipped byte by byte, and header mode resumes at `tlv_left_r == 1` (line 596).
5. The information TLV is identified by:
   - tlvType 0x0003 and lengthField 28 at the header end (lines 575-577);
   - `00-80-C2 00-00-01` in value bytes 0..5, compared when `tlv_left_r == 23` (lines 587-588);
   - the `!fu_found_r` gate, so only the first match counts.
6. Word 11 is `{csro, gmTimeBaseIndicator, 16'd0}` taken from TLV octets 10..15 at `tlv_left_r == 17` (lines 589-595). This matches Table 11-10.

**Refusals:**

- No information TLV (`fu_found_r` at end of frame).
- A value past messageLength: `cnt + len > msg_end`, latched or taken from the current byte (lines 374-376, 707).
- An odd lengthField.
- A header cut by messageLength, with or without padding (lines 379-381, 708).
- Each refusal goes through `fin_drop_w`, giving one drop and no event.

**Accepted shapes:** an unknown TLV first, several unknown TLVs including zero-length ones, a second information TLV (word 11 comes from the first), unknown TLVs after the information TLV, a chain ending exactly at messageLength, and padding after messageLength.

**Nothing 802.1AS-2011 requires to be accepted is refused.** Any Follow_Up that carries the 32-octet information TLV has messageLength ≥ 76, so the Table 11-9 minimum excludes none. The newly refused trailing-chain shapes are malformed under 11.4.2.2 or 1588-2008 5.3.8, and acceptance item 2 requires their refusal. The PR body discloses this behaviour change.

**Independent check:** `probes/fu_walk_diff.cpp` holds a reference model written only from the clauses. It fed 300,000 random chains into the head RTL with 0 mismatches (`receipts/diff_head.log`).

The chain menu covered:

- real information TLVs;
- near-miss information TLVs: wrong subtype, wrong OUI, wrong length (26..32, 32..38), wrong type;
- random even-length TLVs, zero-length TLVs and odd-length TLVs;
- a shifted 00-80-C2/1 inside another TLV;
- PATH_TRACE-typed TLVs and cut tails.

Each frame was then varied by: messageLength over- or under-declared, padding, and physical truncation.

Coverage of the 300,000 frames:

| Outcome | Frames |
|---|---:|
| Accepted, information TLV first | 31,432 |
| Accepted, information TLV after an unknown TLV | 28,298 |
| Refused, cut header | 21,993 |
| Refused, no information TLV | 36,194 |
| Refused, odd length | 71,607 |
| Refused, past messageLength | 11,609 |
| Refused, short messageLength | 71,336 |
| Refused, truncated frame | 27,531 |

The same probe disagrees with the base RTL on 53,204 frames (`receipts/diff_base.log`). That shows the probe can see the #98 defect.

### RTL: CLEAN

- The walk is byte-serial with no frame buffer. It reuses the Announce chain's `tlv_hdr_run_r`, `tlv_hdr_pos_r` and `tlv_left_r`, and adds two flip-flops (`fu_info_r`, `fu_found_r`).
- All arithmetic is 17-bit, with no overflow at `lengthField 0xFFFE`.
- In every accepted frame of the random probe, at both base and head, the event fires 1 cycle after the EOF byte's edge. That covers per-byte timing.
- The head harness on the base RTL fails exactly 31 checks, as the PR states (`receipts/headharness_on_baseRTL.log`).
- `verilator -Wall --lint-only` on the parser shows no new warning at head. One unused parameter is removed (`receipts/lint_parser_nonpkg_*.txt`). `make lint` exits 0.

**Area and timing tables, checked against the published reports (`receipts/evidence_extract.txt`):**

| Run | Engine LUTs | Engine FFs | Slices | Parser LUTs | Parser FFs | WNS |
|---|---:|---:|---:|---:|---:|---:|
| Base, out of context | 4,926 | 3,459 | - | 927 | 302 | 2.249 ns |
| Head, out of context | 4,920 | 3,461 | - | 921 | 304 | 2.249 ns |
| Base, placed | 4,876 | 3,459 | 1,634 | 912 | - | 0.506 ns |
| Head, placed | 4,874 | 3,461 | 1,634 | 907 | - | 0.513 ns |

- These figures match the PR body exactly.
- The worst path at base and at head is inside `u_ucpu`.
- No run reports a critical warning.
- The placement script reads the same sources and `synth_design` line as `syn/ooc/engine_ooc.tcl`.

### Robustness: UNCLEAN (F1)

- The head RTL's refusals hold under random malformed input. Both F1 demonstrator frames are refused at head and at base.
- The hostile-length and padding arms are bounded: `cnt_r <= msg_end_r` and `MAX_MSG_LEN_C`.
- F1: the mid-chain refusal latch is not protected by any suite.
- S2 is a gate-invocation robustness note only.

### Tests: UNCLEAN (F1)

Reviewer runs at the exact head, with the pinned Verilator 5.050 (`receipts/tool_identity.txt`):

| Run | Result |
|---|---|
| Parser suite | 473/473 (base 378/378) |
| Parser mutation arm | 29/29: 28 defects plus the control (base 16/16) |
| Engine suite run | 60/60 |
| µCPU suite | 768/768 |
| `make contract`, `make lint`, `make docs` | rc 0 |

- Each new #98 row maps to a named mutant that fails it, except the `#98 plain fu` reference row and the `#98 unknown TLVs after` control row (S1).
- 15 extra reviewer mutants were run (`receipts/extra_mutants.log`). The harness catches 14 of them. X1 survives (F1).

### Docs: CLEAN (R1 recorded as residue)

- The guide changes in `docs/HDL_DEVELOPER.md:40-44` and `docs/TEST_DEVELOPER.md:25,48,119-120` match the RTL, apart from R1.
- `SOURCE_EVIDENCE` anchors were moved to lines 439 and 521, and both hold (`check_source_evidence`: 20 exact).
- The three `selftest()` links now point to the new module.
- The docs gate passes.
- Comment rule: the added lines carry issue and clause IDs only. No bench lane label, lane name, review round, reviewer ID or issue-comment ID was found in the delta.

**Fourth commit (`5b10675`):**

- The parent's `check_py_idiom.scan()` (fetched at dev `604899c0`, run through `probes/py_idiom_scan.py`) gives these results on this repository:
  - Base: `scripts/check_docs.py` has one long function (`selftest`, 339 lines) and 3 unannotated public functions (`load_generator`, `constant_findings`, `copy_findings`).
  - Head: neither finding remains.
  - Both: the existing long module `hdl/ucode/gen_gptp_ucode.py`, already within the parent ratchet.
- The commit's other hunks are the three annotations, the selftest move, three link retargets and one TEST_DEVELOPER row. That is what the parent gate needs and nothing more.
- The 42 failure messages and the 41 `arms += 1` sites are identical and in the same order. Both base and head report `PASS (127 arms)`.

**Parent consumer gates (author receipts):**

- The head run (`parent-head-A/B`, local parent commit `09d163f9` on dev `604899c0`) analysed `gptp-processor@5b10675c`. The base run analysed `@135afd04`.
- Every listed gate exits 0 in both runs: the code-quality gates, the builder test, `gptp_shadow` 325/325 with controls 9/9, milan_dp `gptp` 210/210 and `gptp-lat` 210/210, `milan_dp_gptp`, `milan_dp_gm_steps` 6/6, `gptp_plane`, `gptp_txts`, `gptp_tables` and tsn_fuzz `ptp` (675 pass, 0 fail).
- `milan_dp_gptp`'s event, progress and verdict lines are identical (`lines-vs-base.diff` is empty).
- At both pins, the final `git status --porcelain` step lists the campaign's own rewritten `TEST_RESULTS.md` timestamp. This is the campaign's behaviour, not a delta effect.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_gptp_rx_parser.sv` delta and clause walk; 300,000-frame independent random probe | R772-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |
| RTL | CLEAN | parser RTL, -Wall lint, EOF-to-event latency, base-RTL run of the head harness, OOC and placed reports | R772-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |
| Robustness | UNCLEAN (F1) | malformed-chain behaviour, demonstrator frames, hostile lengths, docs-gate invocation | R772-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |
| Tests | UNCLEAN (F1) | parser suite and arm at base and head, engine and µCPU suites, 15 extra mutants | R772-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |
| Docs | CLEAN (R1 residue) | guides, SOURCE_EVIDENCE, docs gate split, parent idiom scan, comment rule, parent receipts | R772-1 | 5b10675c3a22acc85bad7c150e1cd25984928385 |

## Real limits

- No copy of the standards was used during this review. The clause reading of 802.1AS-2011 11.4.1, 11.4.2.2, 11.4.4.3 / Table 11-10 and 1588-2008 5.3.8 / 14.1 is the reviewer's own.
- No parent gate, Vivado run, builder bank or tsngen suite was run by the reviewer; they are outside the allowed scope. The parent and area figures come from the author's published receipts. The engine mutation arm was not re-run.
- The random probe uses one seed. It does not drive `rx_err_i` or inter-byte gaps, and it does not check word-11 writes on refused frames. The repository harness covers all three.
- X1 was assessed against this repository's parser and engine suites only, not the parent's tsn_fuzz campaign.
- Frames longer than 2,048 octets (11-bit `cnt_r` wrap) were not examined. The integration contract bounds the frame, and that behaviour predates this delta.
- No hosted checks exist for this head: zero check runs and zero statuses.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, with source base `3e3a4e7`, live dev `604899c0` and this repository's gitlink. Link the receipts on the PR.
- Own hosted/act acceptance.
- Carry R1 to the residue checklist.
- Obtain the second independent review and the full completion bar. F1 must be closed before a positive verdict.

## Reproduction (portable)

1. `probes/build_diff.sh <tree>/hdl <obj>`, then `<obj>/Vdiff 300000` runs the random-chain reference probe.
2. `python3 probes/extra_mutants.py <tree> <work> 8` runs the extra mutants against the harness and the probe. It needs `verilator` on PATH.
3. Build `probes/fu_latch_demo.cpp` against `KL_gptp_rx_parser` the same way as `build_diff.sh` builds its probe. It runs the F1 demonstrator frames.
4. `python3 -I probes/py_idiom_scan.py <parent scripts/check_py_idiom.py> <tree>` runs the parent's idiom scan with a stub scope module.

R772-1 FINISHED

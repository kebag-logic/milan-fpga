[R380] POSITIVE - exact head 6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14

# R380-4: internal independent re-review of PR #610 (issue #70, lane 0: adopt the D3 contract)

- Head `6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14`, tree `51d3da2ae73cfac903adee71371d069bd53a0955`. Its parent is `816c3b742940b9ac8d160ff03e05553a47e5e66d`, the round-3 head.
- Delta under review: `816c3b74..6b76f2d8`. It is one commit by [A409], "docs: finish D3 sweep coverage and contract refinements", with a one-line subject, no body and no trailers.
- The delta changes two files: `docs/design/SAVED_STATE_MATERIALIZATION.md` (+16/-7) and `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` (+1/-1) (`receipts/46`).
- Whole PR: `c07232228c12b72805dd20e6852bf93f25794da0..6b76f2d8`. It has five single-parent commits touching five documentation files.
- All four gitlinks are unchanged. The processor gitlink is `16be6768f710e79450aace277abacd6c2c3336e5` (`receipts/00`, `receipts/40`, `receipts/90`).
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding is open. All five lenses are covered clean at this head.
- My round-3 finding R380-3 F1 is **resolved**, and R380-3 suggestions S1, S2 and S3 are **applied**. One new SUGGESTION (S1 below) does not affect coverage.

## Reconstruction (public state only)

I read these sources in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.
3. The issue #70 body. Its last edit is 2026-08-22, so it has not been edited since round 3 (`receipts/52`, `receipts/53`).
4. The manager's comments on #70:
   - the rulings DR1a to DR6, 5862405632;
   - the DR2c-carrier ruling, 5863247772;
   - the round-4 assignment, 5865266525 (`receipts/50`).

   Both ruling comments have `updated_at == created_at`. Their bodies hash-equal my round-3 copies (`receipts/54`). The rulings are fixed and are not reopened here.
5. The executor's public [A409] TAKEN (5865286202) and REVIEW READY (5865437850) comments (`receipts/55`).
6. The review-start comment on PR #610, 5865484149 (`receipts/51`).
7. The processor tree at `16be6768`.
8. The delta diff and the whole-PR history.
9. Public evidence:
   - the evidence tree `6cf46c2a:review-evidence/70-r1` (`receipts/61`);
   - the exact-head hosted runs (`receipts/60`, `receipts/62`).

My round-3 packet was read-only input. I copied its scripts into this packet byte-identically: `wrap_tolerance.py` is sha256 `fd042cc1...` and `finding_evidence.py` is `dc2ca436...`, both equal to the round-3 files. I ran them unchanged. I read the other reviewer's public round-3 report only after this verdict and the ledger below were written.

## Round-4 focus items

### 1. R380-3 F1 (sweep joints versus comment prefixes): RESOLVED

- **Pattern.** The sweep at D3 `:2377` now joins every multi-word alternative with `[[:space:]/!#*]+`. There are 12 joints in the pattern, and all 12 use exactly that class (`receipts/12`). No `[[:space:]]+` or `[[:space:]/]*` joint remains.
- **Claim.** D3 `:2381-2382` reads: "Multiword separators accept whitespace and `/`, `!`, `#`, `*` characters. This crosses prose wraps and `//`, `//!`, `#`, `*` prefixes."
  - That is exactly what the class does, and no more.
  - The earlier, unbounded claim, "intervening comment prefixes", is gone.
  - The duty to reconcile every statement is still carried by the surrounding text: `:2373` "reconciles every affected statement" and `:2395` "Gate success alone does not replace this statement-by-statement reconciliation".
- **My round-3 `wrap_tolerance.py`, run unchanged** (`receipts/10`). All 7 fixtures report `strict=1`, including `//`, `//!` and `#` wraps.
  - Part B at the pin: the sweep matches 464 lines, the comment-tolerant variant matches 464, and 0 are added.
  - The script's "tolerant" rewrite is now a no-op, because the strict pattern already carries the class.
- **My round-3 `finding_evidence.py`, run unchanged** (`receipts/11`). It reports `RESULT PASS`, rc 0, with 464 matched and 1415 context-only lines.
  - All 31 required locations are MATCH or CONTEXT, and all are ROW-CITED.
  - This includes `protocol_processor_top.sv:2450` (`//!` banner) and `gen_ucode.py:1582-1584`.
- **A wider matrix of my own** (`scripts/separator_matrix.py`, `receipts/12`). For every joint of every multi-word alternative (12 joints), it wraps the phrase at that joint behind each claimed prefix: bare prose, `//`, `//!`, `#` and ` * `.
  - At this head, all 60 claimed cells match (`RESULT PASS`).
  - The unclaimed prefixes `--`, `;`, `>` and a Mermaid `<br/>` do not match. The text does not claim them.
  - **Negative control** (`receipts/13`). Against the round-3 D3 text at `816c3b74`, the same script fails:
    - 13 of 60 claimed cells match: 12 prose, plus `integrating` with `//`;
    - 47 miss;
    - `RESULT FAIL`, rc 1.

    So the fixtures can detect the defect F1 described.
- **Exposure to unclaimed separators at the pin** (`scripts/unclaimed_prefix_exposure.py`, `receipts/14`).
  - The pinned `docs hdl tb` has no line-leading `--`, `;` or `%%` at all.
  - It does have 72 blockquote `>` lines, 3 lines containing `<br/>`, and 355 SVG `<text>`/`<tspan>` lines.
  - A variant whose joints also cross `-`, `;`, `>`, `%` and any tag run adds 0 matched lines.
  - Flattening all 26 SVGs to text gives 0 multi-word hits.
  - So nothing is missed at the pin. That residue is recorded as S1 below, not as a finding.

### 2. Taken suggestions: APPLIED

- **R380-3 S1: the three rows** (`scripts/row_extension_evidence.py`, `receipts/32`, `RESULT PASS`).
  - **`tb/acmp_nvm` row, D3 `:2356`.** It now links `tb/acmp_nvm/acmp_nvm_wrap.sv` at the pin, "banner, lines 12-14". At the pin those lines are "manager 1 / is a harness face, as the platform's saved-state writer / will be), the REAL" (`receipts/30`). The contract adds "in both descriptions". The sweep matches `:13` and shows `:12` and `:14` as context.
  - **`gen_ucode.py` row, D3 `:2364`.** It cites the "E_SETSR exemplar comment at line 472". At the pin that line is `u('NVM_MARK', imm=0x21), # sampling_rate record`. The contract says: "Correct the E_SETSR exemplar comment likewise: the accepted rate write selects its record, never the mark."
    - This row's line list now covers every `NVM_MARK` instruction site in the file: 472, 1364, 1439, 1675, 1791, 1925, 2002 and 2091, plus the 1582 rationale.
    - The only other hit is the opcode table at `:27` (`receipts/30`).
  - **06 row, D3 `:2334`.** It cites "8 SET_SAMPLING_RATE exemplar, line 874". At the pin, `:874` is inside `## 8. µcode architecture` (heading at `:832`) and reads `COMMIT; NVM_MARK sampling_rate`. The contract adds "its mark remains a completion effect".
  - **Negative control** (`receipts/33`). The same script against D3 at `816c3b74` reports all five locations NOT-CITED (`RESULT FAIL`, script rc 1).
  - **Links.** 15.2 now has 40 links, all pinned to `16be6768`. All 32 distinct targets exist at the pin, including `tb/acmp_nvm/acmp_nvm_wrap.sv` (`receipts/44`, `receipts/45`).
- **R380-3 S2: `CLK_HZ_P` and an overflow-free BACKOFF.** D3 `:546-560` now says:
  - "`CLK_HZ_P` gives the unsigned processor clock frequency in hertz";
  - `RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2)`;
  - "ceil(CLK_HZ_P / 2) without multiplication or overflow";
  - "Lane 1 derives both producers' backoff from the top's `CLK_HZ_P`".

  The pinned top declares `parameter int unsigned CLK_HZ_P = 100_000_000` (`protocol_processor_top.sv:91`), and its existing conversions divide the same way (`:93`, `:129`).

  **Executable check** (`scripts/backoff_probe/backoff_probe.sv`, `receipts/20`).
  - The documented expression is evaluated as a SystemVerilog parameter of an `int unsigned CLK_HZ_P`, and compared with an exact 64-bit `ceil(CLK_HZ_P*500/1000)`.
  - Values tested: 0, 1, 3, 50 MHz, 100 MHz, an odd 156,250,001, 2^32-2 and 2^32-1.
  - Result: all 8 match (`BACKOFF_PROBE PASS 8/8`). This includes 50,000,000 at 100 MHz, 25,000,000 at 50 MHz, and 2,147,483,648 at 2^32-1, so the result fits in 32 bits.

  **Mutant controls** (`receipts/21`). Both mutants fail the same probe:
  - the literal 32-bit `(CLK_HZ_P * 32'd500) / 32'd1000` passes only 1 of 8;
  - the floor form `CLK_HZ_P / 32'd2` passes 4 of 8.

  The documented form is better than the one I suggested in round 3: `(CLK_HZ_P + 1) / 2` would wrap to 0 at 2^32-1.

  The time-domain statements elsewhere are consistent with a 500 ms minimum: `:641`, `:661-662`, `:704-705`, `:781`, and the 08_timing row `:2336` ("section 5.1's `RETRY_BACKOFF_CYC_P` conversion"). 5.1 is the section that holds `:546` (`receipts/30`).
- **R380-3 S3: the snapshot count.** Snapshot `:188` now reads "Eight items this contract does not settle".
  - Section 20 (`:1768-1885`) lists 11 numbered items.
  - Items 2 and 3 are marked CLOSED and item 7 is marked RULED, which leaves 8 unsettled: 1, 4, 5, 6, 8, 9, 10 and 11.
  - `:188` is the only count statement on the page (`receipts/31`).

### 3. Scope and frozen items: MET

- Only the two documents changed, and all four gitlinks are identical (`receipts/40`, `receipts/46`).
- No changed line in the delta carries a checkbox, a DR register row or a RULED marker (count 0). Neither changed page carries any checkbox (`receipts/41`).
- FASTCONNECT section 16 has the same 5 checked and 21 unchecked states, in the same order, at `c0723222`, `816c3b74` and this head.
- The D3 15.1 register rows, and the whole 15.1 section, are byte-identical to `816c3b74`. There are 10 RULED rows (`receipts/40`).
- `compare_rulings.py` shows all 10 "Selected option" cells equal to ruling 5862405632 (`receipts/41`, rc 0).
- The DR2c-carrier text was not touched by the delta.
- The nine lane-0 gates return rc 0 at this head (`receipts/42`). They ran with the hash-locked `tools/markdown/requirements.txt` wheels and PyYAML 6.0.3 in a disposable environment.
- 171 fragment links on the five PR pages resolve, and 0 do not (`receipts/43`).

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### Suggestions (non-blocking; they do not affect coverage)

- **S1 (Tests, Docs).** D3 `:2381-2382` now says exactly which separators the sweep crosses. Two kinds of wrap remain uncrossed:
  - Markdown blockquote continuations (`>`, 72 lines in the pinned tree);
  - diagram text split across SVG `<text>`/`<tspan>` runs or Mermaid `<br/>`.

  D3 `:2389` names diagrams as in scope. At the pin, neither kind hides any statement (`receipts/14`: 0 added lines, 0 flattened SVG hits). Lane 1 rewrites these statements, so it could add one sentence saying that blockquote and diagram-text wraps are reviewed by reading, not by the search. The text makes no false claim today, and `:2395` already rules that gate success does not replace reconciliation.

## Lens results (clean lens lines carry their evidence)

```text
[R380] PASS Conformance — D3 :2372-2395 sweep and claim vs round-4 assignment 5865266525 item 1 and R380-3 F1's required outcome (receipts/10, 11, 12, 13); D3 15.2 rows :2334/:2356/:2364 vs pinned 06_aecp_engine.md:874, acmp_nvm_wrap.sv:12-14, gen_ucode.py:472 (receipts/30, 32, 33); D3 15.1 byte-identical and 10/10 selected options equal ruling 5862405632; DR2c-carrier 5863247772 unchanged; FASTCONNECT §16 5/21 checkbox states unchanged (receipts/40, 41, 54); snapshot :188 vs section 20 :1768-1885 (receipts/31)
[R380] PASS RTL — D3 :546-560 RETRY_BACKOFF_CYC_P = (CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2) vs processor 16be6768 protocol_processor_top.sv:91 (int unsigned CLK_HZ_P) and :93/:129 divide-first conversions; SV evaluation of the documented expression at 8 boundary values vs 64-bit ceil reference, 8/8, plus 2 failing mutants (receipts/20, 21); consistency with DR2c FSM :641/:661-662/:704-705 and the 08/01 rows :2336/:2338
[R380] PASS Robustness — BACKOFF boundary and wrap behaviour: CLK_HZ_P = 0, 1, odd, 2^32-2, 2^32-1 (max 2,147,483,648 fits 32 bits; receipts/20); sweep joint x prefix matrix incl. unclaimed prefixes and pin exposure to -- ; > %% <br/> and SVG text runs, 0 missed statements at 16be6768 (receipts/12, 14)
[R380] PASS Tests — round-3 wrap_tolerance.py 7/7 non-zero and finding_evidence.py RESULT PASS, both run unchanged (receipts/10, 11); separator matrix 60/60 claimed cells with negative control FAIL on 816c3b74 (receipts/12, 13); row-extension check PASS with negative control FAIL (receipts/32, 33); nine lane-0 gates rc 0 (receipts/42); 171/0 anchors (receipts/43); 40 pinned 15.2 links, 32/32 targets exist (receipts/44, 45)
[R380] PASS Docs — D3 :546-560 wording ("unsigned", "without multiplication or overflow", "Odd frequencies round upward") vs probe; :2381-2382 claim vs pattern; row contract wording at :2334/:2356/:2364; snapshot :188 count; commit 6b76f2d8 one-line subject, no body/trailers (receipts/46); executor REVIEW READY 5865437850 claims vs receipts
```

S1 is a SUGGESTION, so it leaves Tests and Docs clean.

## Reviewer-owned completion ledger

This ledger covers the round-4 delta at this head. The delta touches only D3 5.1, D3 15.2 and the snapshot TOC line. The whole-PR artifacts outside the delta keep their round-3 coverage on the ancestor `816c3b74` (R380-3 RTL and Robustness; R381-3 POSITIVE). Every lens is re-applied here at the exact head.

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 5865266525 items; D3 `:2372-2395` sweep and claim; 15.2 rows `:2334/:2356/:2364` vs pinned `06:874`, `acmp_nvm_wrap.sv:12-14`, `gen_ucode.py:472`; 15.1 vs ruling 5862405632; carrier 5863247772; FASTCONNECT §16 checkboxes; snapshot `:188` vs §20 (receipts/10-13, 30-33, 40, 41, 54) | R380-4 | 6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14 |
| RTL | CLEAN | D3 5.1 `:546-560` vs top `CLK_HZ_P` `:91/:93/:129`; SV parameter evaluation and mutants (receipts/20, 21); DR2c FSM time statements | R380-4 | 6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14 |
| Robustness | CLEAN | BACKOFF extremes (0, odd, 2^32-1); sweep separators incl. unclaimed prefixes; pin exposure (receipts/12, 14, 20) | R380-4 | 6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14 |
| Tests | CLEAN | round-3 scripts run unchanged; separator matrix and row checks with negative controls; nine gates; anchors; link targets (receipts/10-14, 32, 33, 42-45) | R380-4 | 6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14 |
| Docs | CLEAN | two delta pages; BACKOFF wording; sweep claim; row wording; snapshot count; commit form; executor evidence claims (receipts/31, 46, 55) | R380-4 | 6b76f2d8260b57c49e2fd3a619d269eb3a7fbd14 |

## Prior public review findings: resolved or retained at this head

I wrote this table after the verdict and ledger above. I read R381-3 (PR comment 5865262556, `receipts/56`) only at that point.

| Finding | State at `6b76f2d8` | Evidence |
|---|---|---|
| R380-3 F1 (MINOR; Conformance, Tests, Docs): the sweep claims to cross comment prefixes that its joints do not | **RESOLVED** | Focus item 1. My round-3 `wrap_tolerance.py` gives 7/7 non-zero and `finding_evidence.py` gives PASS, both run unchanged (`receipts/10`, `receipts/11`). The claim at `:2381-2382` equals the pattern, and the 60-cell matrix PASSes, with a negative control (`receipts/12`, `receipts/13`) |
| R380-3 S1 = R381-3 S1 (SUGGESTION): the `acmp_nvm_wrap.sv:12-13` banner and the E_SETSR exemplar at `gen_ucode.py:472` / `06:874` | **APPLIED** | Rows `:2356` (lines 12-14), `:2364` (line 472) and `:2334` (line 874), with contract text for each. The check PASSes, with a negative control (`receipts/32`, `receipts/33`) |
| R380-3 S2 = R381-3 S3 (SUGGESTION): the 32-bit transcription of the BACKOFF formula | **APPLIED** | `:546-560` names `CLK_HZ_P` and uses the divide-first form. The probe gives 8/8, and both mutants fail. R381-3's wrapped 100 MHz value, 2,755,359, is reproduced by my multiply-first mutant (`receipts/20`, `receipts/21`) |
| R381-3 S2 = R380-3 F1 (SUGGESTION there): the prefix claim is broader than the pattern | **RESOLVED** | As R380-3 F1 above. R381-3 proposed exactly the class `[[:space:]/!#*]+`, and that is the class adopted |
| R380-3 S3 (SUGGESTION): the snapshot count "Seven" | **APPLIED** | `:188` now says "Eight": 11 items, less 2 CLOSED and 1 RULED (`receipts/31`) |
| Earlier rounds: R380-1/2 and R381-1/2 findings and suggestions | **STILL RESOLVED** | The delta touches none of their artifacts outside D3 5.1 and 15.2. `finding_evidence.py`, which carries R380-2 F1 and R381-2 F1's 31 locations, still PASSes (`receipts/11`). 15.1 and the carrier text are byte-identical (`receipts/40`) |

No prior finding is retained open.

## Real limits

- **Manager bank receipts.** As of 07:43 UTC I found no public receipt for this head's static, builder or native banks:
  - the evidence tree `6cf46c2a:review-evidence/70-r1` holds the round-1 author logs only (19 entries, 0 mentioning `6b76f2d8`; `receipts/61`);
  - no manager evidence comment had been posted on #70 or PR #610 since the assignment.

  The assignment brief says those banks passed. This review does not rely on them and did not run them.
- **Hosted checks at 07:43 UTC** (`receipts/60`, `receipts/62`):
  - completed successfully: `rtl-fast` (workflow), `bdd-conformance`, `changes`, `docs-check-no-git`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, Yosys shards 0-3, and Verilator shards 0 and 3;
  - still in progress: the `docs`, `elaborate` and `rtl-full` workflows, including `docs-check`, `elaborate` and Verilator shards 1, 2 and 4;
  - skipped, so not executed evidence: `Physical gPTP (nightly and manual)`.

  None of these is relied on. The manager owns hosted and act acceptance.
- **Pinned simulator path.** The brief names `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`, and that path does not exist in this environment. The BACKOFF probe used a sibling wrapper, `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`. Its identity is `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/20`). The probe tests SystemVerilog constant-expression arithmetic only, and no product RTL was compiled.
- **Live `dev` has moved.** The source base is `c0723222`, while live `dev` is `54ce8773` per the assignment. This review says nothing about the final current-dev candidate.
- **Clause text.** Milan and IEEE clause text was not re-read. The delta changes no clause interpretation.
- **No hardware.** Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof.
- **Clone state.** The clone was never written. Its exact-head bytes, index and gitlinks were verified at the start and at the end (`receipts/00`, `receipts/90`).

## Pending manager duties

- Publish this report.
- Publish the exact-head static, builder and native bank receipts.
- Let the in-progress hosted workflows finish at `6b76f2d8`, and own hosted and act acceptance.
- Confirm that the second positive required by CONTRIBUTING is satisfied. R381-3 is POSITIVE on ancestor `816c3b74`, and the assignment says it "stands". The delta touches Conformance, RTL, Tests and Docs scope artifacts, so the manager decides whether that ancestor positive clears the bar or whether a re-review at this head is needed.
- At the merge turn, build and validate the current-dev candidate against live `dev` (`54ce8773`), and do post-merge containment.
- Later, not this lane: DR3a ratification after lane 1 measures.

R380-4 FINISHED

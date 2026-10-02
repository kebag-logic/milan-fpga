[R435] POSITIVE - exact head bd86f6466baa77113eea2266c00044c3a29678f2

# R435-4: external review of PR #144 (lane C8, descriptor model lint), round 4 (merge only)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. PR #144 serves issues #38, #39, #60 and #89.
- Exact head `bd86f6466baa77113eea2266c00044c3a29678f2`, tree `973da49d27ae9f7e160d7480ba1af4ef96e54821` (verified in the review clone).
- Scope (assignment #60 comment 5958629222): the `--no-ff` merge `3bfc7c6` of `main` `631eeb34` (PR #142, P141) into the round-3 head `97f6eace` (R434-3 and R435-3 POSITIVE there), and the one commit `bd86f64` that adds L6's positive case. Nothing else is judged.
- Review start: PR #144 comment 5960190387.
- Scope reconstructed in this order:
  1. README.md and docs/README.md. The repository has no AGENTS.md or CONTRIBUTING.md.
  2. Issue #60's body and acceptance, and every #60 comment: the lane assignment, the STOP and its ruling (5948872196), the round-2, round-3 and round-4 assignments, and the four REVIEW READY notes.
  3. The PR body, including its Round 4 section.
  4. The linked requirement and interface rows: 07 §3.1 (L6 row, the model-lint text), 00 REQ-MDL-005 and REQ-AEM-013, 06 §6.4's SET_CLOCK_SOURCE row, 09 §8.2 and §8.5, the `tb/desc_store` and `tb/pp_top` READMEs, and `model_rules.py`'s L6 code.
  5. `git diff 631eeb34..bd86f646`, `97f6eace..3bfc7c6`, `3bfc7c6..bd86f646`, the merge base `2ebd4fe8`, and the history.
  6. The public author-r4 packet (milan-fpga archive `962593ca`, `review-evidence/ppC8-r1/author-r4`). Both parent patches there hash to the stated values: C8 `aa5a88eb…`, C4C6 `67bcd698…`.
- Order of work:
  - I wrote my verdict and ledger (`receipts/verdict_before_prior_findings.txt`) before I read any prior review report.
  - I read prior public findings only after my own pass, and resolve them below.

## Verdict

**POSITIVE.** The merge keeps both sides, and the one extra line is exactly as declared. The new positive case packs the shape it claims with the lint on and no waiver, and kills every stricter set reading I planted. P141's work is intact. The parent models pack byte-identically to round 3 at both parent heads.

No BLOCKER, MAJOR, MINOR or RESIDUE finding is open at this head. One SUGGESTION is below.

1. **Both conflicts keep both sides.** I re-did the merge (`97f6eace` + `631eeb34`, `--no-ff --no-commit`):
   - It conflicts in exactly `docs/00_MILAN_COMPLIANCE_REVIEW.md` and `docs/architecture/07_memory_maps.md`.
   - Every non-conflicted path of my trial merge equals `3bfc7c6` byte for byte. The one exception is `model_rules.py`, which is the declared extra line.
   - Main changed three rows (merge base `2ebd4fe8`): 07 L6, REQ-MDL-005 and REQ-AEM-013. REQ-AEM-013 auto-merged to main's text.
   - `scripts/keep_both.py` splits each side's version of the two hand-resolved rows into cells and sentences (`receipts/keep_both.txt`):
     - **07 L6.** Main's restatement is kept: set as a minimum; one INPUT_STREAM source per AAF input beside the CRF input's (§7.2.9.2, Table 7-17); the D1 order; up to Table 7-61's 216; §7.2.32 membership; BAD_ARGUMENTS per Table 7-141 carrying the current index (§7.4.23.1); "Milan v1.2 §5.3.3.6, §7.5" and main's clause column. The lane's Checks column is verbatim. Two of main's sentences are extended, not dropped:
       - "the processor reads no order" became "neither the processor nor the lint reads an order";
       - the identity-list sentence gains the lane's "sits at 76, is `76 + 2 × count` long" and "(76 + 2 × 216 is §7.2's 508 octets, L12's `descriptor-maximum`)". 76 + 432 = 508.

       The lane sentences that are no longer verbatim are its own old L6 wording, which main's restatement supersedes. That includes the old "§7.4.23.1 membership test" credit.
     - **REQ-MDL-005.** It has main's clause and requirement. The Arch cell joins both sides: "the processor's range check over L6's identity list; packer model lint L6, which accepts that set and reads no order (defence in depth)". Doc `07 §3.1, 09 §8.5` and Ver `DIR` are the lane's, where main had `07 §3.1` and `—`. The row reads as one statement with the 07 L6 row.
2. **The one extra line.** `97f6eace..3bfc7c6` changes `hdl/aecp/desc/model_rules.py` in exactly one line (`:174`): `"§7.4.23.1; 06 §6.4"` becomes `"§7.2.32; 06 §6.4"` in `domain-source-identity`'s clause. The check id, the rule, the description and the code are unchanged. Probe P6 shows the refusal now ends "(IEEE 1722.1-2021 §7.2.32; 06 §6.4)". No file of the parent at dev `cdf49d1a` or at #634 `0b066b6e` quotes the old or the new text. Other §7.4.23.1 citations in the tree are about the command's response body, which is that clause's subject.
3. **L6's positive case** (`test_gen_desc_image.py:455`).
   - P1 rebuilds its model exactly as the test does and decodes it: one domain, count 10, list 0..9; CLOCK_SOURCE 0 INTERNAL; 1 INPUT_STREAM at STREAM_INPUT 1 (CRF); 2..9 INPUT_STREAM at AAF STREAM_INPUT 0, 2..8. It packs with "lint waivers applied: 0". The test's own `packs()` asserts that same line with `build()`'s default `lint=True`.
   - My nine plants (`scripts/l6_plants.py`) are each one edit to `_rule_sources` in a disposable copy (`receipts/l6_plants.txt`). The no-plant control passes both variants.
     - Six stricter set readings: at most 9 sources; no more sources than Stream Inputs; beside CRF at most one AAF source; beside CRF no AAF source; at most CRF inputs + 1 INPUT_STREAM sources; beside CRF at most half the AAF inputs.
     - With the new test, all six are KILLED. Without it, four survive and only the two that `test_boundaries_pack` already catches are killed.
     - This matches the PR body's "1 of 5 without, 5 of 5 with" on the author's own five.
4. **Nothing of P141 lost.** Every file P141 touched (`2ebd4fe8..631eeb34`) equals main at the head, except four. The three docs files differ only by the lane's own rows. `tb/pp_top/README.md` differs only by the lane's seven-line fixture note, and that note is still true after D3C: D3C's re-packed ten-source image also "carries no CLOCK_SOURCE descriptor" (`d3_phases.hpp:2753-2754`). Evidence:
   - D3C, the two `sclks-*` patches, `gen_ucode.py`, 06 and 09 §8.2's D3C row are present (`receipts/p141_preserved.txt`);
   - all 207 campaign patches apply;
   - `tb/pp_top` passes 9,168 of 9,168;
   - the packer gate passes 59 tests (58 at round 3, plus only the new case), and `tb/desc_store` passes 584 of 584;
   - the suppression driver kills 56 of 56, and its output is byte-identical to its output at `97f6eace`;
   - `example_milan_8` and `milan_min` images are byte-identical to round 3's;
   - the five parent models pack byte-identically, at dev `cdf49d1a` and at #634 `0b066b6e`, with the processor at `97f6eace` and at `bd86f646`. All 16 outputs per head are identical (images, reports, digests, refusal text), and the digests equal the author's receipts.
   - At `0b066b6e` the models carry 3, 6, 6, 3 and 10 sources in the order INTERNAL 0, CRF 1, AAF k at 2 + k. `ax7101_8x8` packs only with its #584 waiver, and is refused on 8 lines without it.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding.

### S1: SUGGESTION. "The lint reads no order" is true by code but pinned by no test

- **Lenses:** Tests, Docs.
- **Where:** `docs/architecture/07_memory_maps.md:186` ("neither the processor nor the lint reads an order", added by this merge) and `docs/00_MILAN_COMPLIANCE_REVIEW.md:450` ("packer model lint L6, which accepts that set and reads no order"). The code is `hdl/aecp/desc/model_rules.py:703-732`.
- **Evidence:**
  - Three order-reading plants survive the gate, with and without the new test (`receipts/l6_plants.txt`): `o1-internal-first` (CLOCK_SOURCE 0 must be INTERNAL), `o2-crf-source-at-1` (CLOCK_SOURCE 1 must be the CRF input's) and `o3-aaf-in-stream-order`.
  - Every positive model in the gate uses the class order INTERNAL 0, CRF 1, AAF 2 + k.
  - Probe P2 shows the head accepts another order (AAF sources first, INTERNAL fourth, the CRF input's source last), so the statement is true today (`receipts/l6_probes.txt`).
- **Impact:** none at this head. A later change that made the lint enforce the consumer's D1 order would refuse standard-conforming models, and the gate would not notice. That would contradict main's L6 ("the processor reads no order") and the manager's round-2 rule that strictness beyond the standard is kept only where the processor needs it.
- **Suggested outcome:** add one `ConformingModelTest` case that packs P2's permuted ten-source domain (or any order other than INTERNAL 0, CRF 1).
- **Verification:** `scripts/l6_plants.py` reports `o1`, `o2` and `o3` KILLED.

Note (not a finding): beside a CRF input, two INPUT_STREAM sources at the same AAF input pack (P5). That goes beyond "one per AAF input is allowed", but it matches main's own reason ("no clause sets a count for an AAF input beside a CRF input") and the PR body's "the lint sets no count". With no CRF input, one source per AAF input is refused by `aaf-input-source` (P4), which matches main's "(or on the single AAF input when no CRF input exists)".

## Prior public findings at this head

Read after my verdict and ledger were written.

| Finding | Original severity | Status at bd86f646 | Evidence |
|---|---|---|---|
| R435-1 F1 to F6, R434-1 F1 to F4 | MINOR | **Remain closed** | The merge changes no lint code except `:174`'s clause string. R435-2 `r2_plants.py`, run unchanged: 37 of 37 KILLED. R434-3's `plant_r2.py`: 37 KILLED, none survived (`receipts/prior_*`) |
| R435-2 F1, R434-2 F1 (L4 Annex C) | MINOR | **Remain closed** | R435-3 `r3_probes.py`, run unchanged with the round-3 tree as base: 31 probes, 0 unexpected |
| R435-2 F2, R434-2 F2 (unpinned arms, digest) | MINOR | **Remain closed** | R434-3 `plant_r3.py`: 40 KILLED. R435-3 `r3_plants.py`: 15 of 16 KILLED; the survivor is R435-3 S1 |
| R435-2 R1 (title "L1 to L11") | RESIDUE | **Remains closed** | The title reads "rules L1 to L12" |
| R435-3 S1 (pin that `model_rules` loads through the shared loader) | SUGGESTION | **Retained, not taken** (merge-only round) | `g-own-loader` still SURVIVES (`receipts/prior_r435_3_r3_plants.txt`) |
| R434-3 S1 (direct `import model_lint` gives a `NameError`) | SUGGESTION | **Retained** | Still `NameError: name 'beside' is not defined` (`receipts/carried_suggestions.txt`) |
| R434-2 S2; R434-1 S3, S4 | SUGGESTION | **Retained, not taken** | The code is unchanged (`model_rules.py:796-797`); listed in the PR body's "What remains (round 4)" |

## The five lenses

### Conformance: CLEAN
- The 07 L6 row and REQ-MDL-005 state main's restated L6. The lint accepts it exactly as the Checks column says:
  - `crf-input-source`: exactly one at each CRF input;
  - `aaf-input-source`: with no CRF input, exactly one at the AAF inputs;
  - `internal-source`: at least one INTERNAL where a Stream Output exists;
  - beside CRF, no AAF count; no order.
- Probes P1 to P5 confirm each arm.
- The clause credit of `domain-source-identity` (§7.2.32) now matches L6's and 06 §6.4's.
- The 216 statement holds on both sides of the bound: 216 sources make a 508-octet CLOCK_DOMAIN and pack, and 217 (510 octets) are refused by `L12 descriptor-maximum` alone (P3).
- No rule changed (`97f6eace..bd86f646` touches no other line of `hdl/aecp/desc`).

### RTL: CLEAN
- The lane's RTL delta against `631eeb34` is one comment in `KL_aecp_desc_store.sv` (the 46-cap sizes). It equals round 3's.
- P141's `gen_ucode.py`, `pp_top_wrap.sv`, `sim_main.cpp`, `d3_phases.hpp` and mutant drivers equal main at the head. There is no port, parameter or register change.
- `lint_hdl.sh` rc 0.
- `tb/pp_top`: 9,168 of 9,168 with the pinned Verilator 5.050 (identity verified: `--version` "5.050 rev v5.050"). That includes D3C.
- `tb/desc_store`: 584 of 584.

### Robustness: CLEAN
- The L6 bound edges (216/217), a permuted class order, the no-CRF multi-source case and a duplicated AAF source each behave as the docs state (`receipts/l6_probes.txt`).
- The parent consumers' models pack byte-identically to round 3 at two parent heads, waiver behaviour included (`receipts/pack_parent*.txt`).
- At #634 the C8 patch's `aem_assemble.py` hunk needs a one-line port, as the author records. `scripts/mkparent.sh` makes it by one asserted substitution.

### Tests: CLEAN (S1 is a suggestion)
- Gate: 59 tests OK; `-v` lists differ from round 3's only by the new case (`receipts/gate_v_*.log`).
- Suppression: 56 of 56, byte-identical to round 3.
- Nine own L6 plants: all six set readings KILLED only with the new test; three order plants survive (S1).
- Campaign patches: 207 of 207 apply.
- Prior reviewers' scripts, run unchanged: R435-3 15/16 (S1 survivor), R435-2 37/37, R434-3 40/40 and 37/37, R435-3 probes 0 unexpected.

### Docs: CLEAN
- The keep-both analysis is above.
- The 09 §8.5 `ConformingModelTest` row and the `tb/desc_store` README list the new case and the plants table. The README's "Also fails" column agrees with my without-test runs: the two "no AAF beside CRF" readings also fail `test_boundaries_pack`, and the others fail nothing else.
- REQ-AEM-013 is main's. 06 §6.4's row links 07 §3.1 L6 and agrees with it.
- `make check` rc 0 (115 REQ rows, 17 GAP findings; matrix 94 rows, 0 untested). `gen_matrix.py --check` rc 0. `git diff --check` over `631eeb34..head` and `97f6eace..head` rc 0.
- The PR body's Round 4 line numbers hold: `07_memory_maps.md:186`, `00_MILAN_COMPLIANCE_REVIEW.md:450`, `model_rules.py:174` and `test_gen_desc_image.py:455`. So does "the same 19 files" (`receipts/history.txt`).

## Executed checks at this head

| Check | Result | Receipt |
|---|---|---|
| re-done merge `97f6eace` + `631eeb34` | conflicts in exactly the two files; non-conflicted paths equal `3bfc7c6` except the declared `model_rules.py:174` | this report §Verdict 1; `receipts/keep_both.txt` |
| merge history | `3bfc7c6` parents `97f6eace` and `631eeb34` (`--no-ff`, no rebase); two first-parent commits on `97f6eace` | `receipts/history.txt` |
| `make -C tb/desc_store run` (pinned Verilator 5.050) | rc 0; 59 tests OK; 584 PASS, 0 FAIL | `receipts/desc_store_suite.log`, `.rc` |
| gate `-v` at round 3 and at the head | 58 vs 59; the only new test is the L6 positive case | `receipts/gate_v_97f6eac.log`, `receipts/gate_v_bd86f646.log` |
| `lint_suppression.py --jobs 16` at the head and at `97f6eace` | rc 0; 56 of 56 killed; byte-identical | `receipts/lint_suppression*.log`, `.rc` |
| `make -C tb/pp_top` (pinned Verilator 5.050) | rc 0; 9,168 PASS, 0 FAIL | `receipts/pp_top_suite.log`, `.rc` |
| `make check`, `gen_matrix.py --check`, `lint_hdl.sh`, `git diff --check` (two ranges), `git apply --check` on every campaign patch | all rc 0; 207 of 207 | `receipts/static_checks.txt`, `receipts/make_check.log`, `receipts/gen_matrix.log`, `receipts/lint_hdl.log` |
| packer images, round 3 vs head | `example_milan_8` (lint off) and `milan_min` identical | `receipts/images_r3_vs_head.txt` |
| own L6 plants (1 control + 9) | control green; 6 of 6 set readings KILLED with the new test (2 of 6 without); 3 order plants survive | `receipts/l6_plants.txt` |
| own L6 probes P1 to P6 | as stated above | `receipts/l6_probes.txt` |
| parent five models, processor `97f6eace` vs `bd86f646`, at dev `cdf49d1a` and #634 `0b066b6e`, C4C6 then C8 patch | 4 pack without waiver, `ax7101_8x8` with its #584 waiver only; outputs identical; digests equal the author's | `receipts/mkparent.txt`, `receipts/pack_parent.txt`, `receipts/pack_parent_compare.txt` |
| parent clock-source shapes | dev: 2 each; #634: 3, 6, 6, 3, 10 in INTERNAL 0, CRF 1, AAF 2 + k order | `receipts/parent_clock_sources.txt` |
| P141 preservation | every P141 file equals main, except the lane's rows and README note | `receipts/p141_preserved.txt` |
| prior reviewers' scripts, unchanged | as in the prior-findings table | `receipts/prior_*.txt` |
| hosted runs at the head (read-only) | `docs-gates` and `portability` succeeded (2 runs each); `suites` still in progress at 20:08Z | `receipts/hosted_check_runs_bd86f646.txt` |
| review clone restored | HEAD/tree exact; worktree, index and tree agree on blob bytes, modes and paths; nothing untracked or ignored; no gitlinks (no `.gitmodules`) | `receipts/restore_check.txt` |

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 07 §3.1 L6 row and REQ-MDL-005 (both sides and resolution); `model_rules.py:171-181`, `_rule_domains`, `_rule_sources`; 06 §6.4 SET_CLOCK_SOURCE row; probes P1 to P6; parent clock-source shapes at #634 | R435-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |
| RTL | CLEAN | lane RTL delta vs `631eeb34` (one comment); P141 RTL, microcode and harness equal main; `lint_hdl.sh`; `tb/pp_top` 9,168 and `tb/desc_store` 584 with the pinned Verilator 5.050 | R435-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |
| Robustness | CLEAN | 216/217 bound, permuted order, no-CRF and duplicate-source cases; parent five models byte-identical round 3 vs head at dev `cdf49d1a` and #634 `0b066b6e`; waiver removal | R435-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |
| Tests | CLEAN | `test_gen_desc_image.py:455`; gate 59; suppression 56/56 identical to round 3; 9 own L6 plants (S1); 207 campaign patches; prior reviewers' scripts unchanged | R435-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |
| Docs | CLEAN | re-done merge and keep-both split; 09 §8.5 row; `tb/desc_store` README plants table; `tb/pp_top` README note vs D3C; REQ-AEM-013; PR body Round 4; `make check`, `gen_matrix --check` | R435-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |

## Real limits

- The standards' text was not re-read for this round; the specification documents are not distributed with the repository. Clause conformance is judged against the rows' own citations and main's reviewed restatement. "Table 7-61's 216" is main's figure; I checked only its arithmetic against §7.2's 508 octets (76 + 2 × 216) and the lint's behaviour at the bound.
- Of the 33 suites, I ran only the two this round moves or exercises (`tb/desc_store`, `tb/pp_top`). The 1,019,127 total is checked arithmetically from the author's sweep log, against my two suite counts. The full sweep is the manager's bank, and the hosted `suites` job had not finished.
- The RTL mutation campaigns were not re-run. The merge changes no RTL, harness or campaign patch beyond main's own, and all 207 patches apply.
- At #634, the C8 parent patch's `aem_assemble.py` hunk was ported by one substitution, as the author did. That is a scratch adaptation, not the parent's adoption.
- Physical calibration NOT RUN. Field skips are not hardware proof. No hardware was used.

## Pending manager duties

- Run the donor bank (9) and the parent consumer set (16) at dev `cdf49d1a` with `parent-adoption-c4c6-ea3fb388.patch` and then `parent-adoption-c8-cdf49d1a.patch`, at this head.
- Hosted/act acceptance: the `suites` job at the head was still in progress at my last look. Distinguish executed jobs from skipped contexts.
- Build and validate the final current-dev candidate at the merge turn (source base `631eeb34`, live dev `cdf49d1a`). That is distinct from this source validation.
- Carry S1 and the retained suggestions (R435-3 S1, R434-3 S1, R434-2 S2, R434-1 S3/S4) to the follow-up list as the manager sees fit. None is verdict-bearing.

R435-4 FINISHED

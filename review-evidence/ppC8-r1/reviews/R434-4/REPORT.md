[R434] POSITIVE - exact head bd86f6466baa77113eea2266c00044c3a29678f2

# R434-4: internal independent review of processor PR #144 (lane C8, descriptor model lint), round 4 (merge only)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #144 (issues #38, #39, #60, #89). Review start: PR #144 comment 5960189449.
- Exact head `bd86f6466baa77113eea2266c00044c3a29678f2`, tree `973da49d27ae9f7e160d7480ba1af4ef96e54821`. It is two commits on the round-3 head `97f6eace` (R434-3 and R435-3 POSITIVE there):
  - `3bfc7c6`: the `--no-ff` merge of main `631eeb34` (PR #142, P141);
  - `bd86f64`: L6's positive case.
- Scope judged: the merge and that commit only (assignment, #60 comment 5958629222).
- Reconstruction order:
  1. README.md and docs/README.md. The repository has no AGENTS.md or CONTRIBUTING.md.
  2. Issue #60: body and frozen acceptance, and every comment. That covers the 46-cap report, the lane assignment, the STOP and its ruling (5948872196), the round-2, round-3 and round-4 assignments, and each REVIEW READY.
  3. The PR body, Round 4 section included.
  4. The requirement rows (00 §6.6 REQ-MDL-005, 07 §3.1 L6) and the interfaces they name: 06 §6.4, `gen_ucode.py` E_SCLKS, the `tb/pp_top` D3C header.
  5. `git diff 631eeb34..bd86f646`, `97f6eace..bd86f646`, `2ebd4fe8..631eeb34`, and the history.
  6. Public evidence: milan-fpga `fec8f8ad` (round-1 packet), and the author-r4 packet at archive `962593ca` (`review-evidence/ppC8-r1/author-r4`). Its two parent patches hash `aa5a88eb…` and `67bcd698…`, equal to author-r3's.
- Order of work:
  - The merge re-do, plants, probes, suites and parent packing were done before I read any prior review findings.
  - Prior public findings (R434-1..3, R435-1..3, as PR comments) were read after that pass and are dispositioned below.
  - I have not read the concurrent R435-4 report.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open, and all five lenses are CLEAN. One RESIDUE (R1, PR-body wording) and two new SUGGESTIONS (S1, S2) are recorded. Each assignment focus item is reproduced:

1. **Both conflicts keep both sides.** I re-did the merge (`97f6eace` + `--no-ff` `631eeb34`). It conflicts in exactly the two files the assignment names, and every auto-merged file is byte-equal to `3bfc7c6` (12 of 12). Cell by cell:
   - **07 §3.1 L6:**
     - the clause column is main's;
     - the Checks column is the lane's;
     - the statement is main's text whole, with three lane insertions: the list "sits at 76, is `76 + 2 × count` long", "neither the processor nor the lint reads an order", and "(76 + 2 × 216 is §7.2's 508 octets, L12's `descriptor-maximum`)".
   - **REQ-MDL-005:**
     - Clause and Requirement are main's;
     - Arch is main's cell plus "; packer model lint L6, which accepts that set and reads no order (defence in depth)";
     - Doc and Ver are the lane's.

   It reads as one statement. For every other file either side touched, each side's diff survives the merge exactly.
2. **The one extra line.** Outside the two conflicted docs, the trial merge differs from `3bfc7c6` only in `model_rules.py:174`, where `domain-source-identity` now cites "§7.2.32; 06 §6.4" instead of "§7.4.23.1; 06 §6.4". Nothing else in that check or file changes.
   - This agrees with main's L6, which makes §7.2.32 the membership test.
   - The other L6 checks already cite §7.2.32.
   - No lane file still credits the identity check to §7.4.23.1. The remaining §7.4.23.1 citations in the tree are the response-carries-current-value semantics, all main's.
3. **The new L6 positive case** is `test_gen_desc_image.py:455`.
   - It packs with the lint on and no waiver. Its report reads "semantic lint: on" and "lint waivers applied: 0".
   - Its shape, dumped: INTERNAL 0; CRF source 1 at STREAM_INPUT 1 (`041060010000BB80`); then AAF inputs 0, 2..8 (`0205022002006000`) at sources 2..9. CLOCK_DOMAIN list 0..9, 96 octets.
   - My own copies of the author's five stricter readings are each KILLED at head. The merge commit's gate kills only 1 of 5 (`aaf-none-beside-crf`, via `test_boundaries_pack`).
   - Five further non-order readings of my own are also KILLED at head (see Tests).
4. **Nothing of P141 is lost.**
   - The D3C section, the `sclks-*` patches, 06, `hdl/aecp/ucode` and the 09 §8.2 D3C row equal main's.
   - `tb/pp_top/README.md` equals main's plus the lane's own 7-line note, which is unchanged since round 3 and still true: D3C's own header says the image "carries no CLOCK_SOURCE descriptor".
   - 207 of 207 campaign patches apply.
   - The packer gate passes 59 tests. That is round 3's 58 plus the new one, with the test list otherwise identical.
   - The suppression driver kills 56 of 56. Its log is byte-equal at `97f6eace` and at head, and equal to the author's.
   - `run_suites.sh` rc 0: 33 suites, 1,019,127 checks, per-suite tallies equal to the author's. Against round 3, only `pp_top` moves (+17, main's D3C).
   - The five parent models pack byte-identically between processor `97f6eace` and head, at dev `cdf49d1a` and at PR #634 `0b066b6e`. That covers image sha256, report sha256 and model digest. The digests equal the author's receipts.

Issue acceptance:

- The round touches no rule, so #38, #39, #60 and #89 stay met as at round 3.
- #60's L6 acceptance, including the identity permutation that E_SCLKS relies on, still has its negatives: the 56/56 suppression covers `domain-source-identity`.
- The four Closes lines stand.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### R1: RESIDUE. The PR body's "What remains (round 4)" omits a carried suggestion

- **Lenses:** Docs.
- **Where:** the PR #144 body, section "What remains (round 4)".
- **Evidence:**
  - The section lists R435-3 S1, R434-2 S2 and R434-1 S3/S4 as not taken.
  - It omits R434-3 S1, which is also carried. Loading `model_lint.py` directly still fails with `NameError: name 'beside' is not defined` (`receipts/direct_import_model_lint_bd86f64.txt`).
- **Impact:** wording only. No measurement, figure, verdict, test, code, artifact or clause claim changes.
- **Exact fix:** add "R434-3 S1 (a self-explaining `ImportError` when `model_lint.py` is loaded other than through `gen_desc_image`) is not taken" to that list.
- **Verification:** read the PR body.

### S1: SUGGESTION. "The lint reads no order" is true of the code but not pinned by the gate

- **Lenses:** Tests.
- **Where:** `docs/architecture/07_memory_maps.md:186` and the REQ-MDL-005 Arch cell (`docs/00_MILAN_COMPLIANCE_REVIEW.md:450`) both claim the lint reads no order. Every gate positive puts INTERNAL at 0 and CRF at 1.
- **Evidence:**
  - My plant `order-internal-first` refuses a model whose CLOCK_SOURCE 0 is not INTERNAL. It SURVIVES at head and at the merge (`receipts/l6_plants_reviewer.txt`).
  - The code reads no order: `_rule_sources` (`model_rules.py:703-732`) counts by location only. My probes pack AAF-first, CRF-first-INTERNAL-last and interleaved-reverse orders at head, at the merge and at round 3 (`receipts/l6_probes.txt`).
- **Why it is not MINOR:** the assignment requires the lint to accept main's order, and it does (KILLED plants). The no-order claim is currently true.
- **Outcome:** add one `ConformingModelTest` positive whose sources are in a non-D1 order, for example INTERNAL last.

### S2: SUGGESTION. The 216-source boundary is a probe, not a gate case

- **Lenses:** Tests.
- **Where:** the L6 row's "of any length up to Table 7-61's 216 (76 + 2 × 216 is §7.2's 508 octets, L12's `descriptor-maximum`)".
- **Evidence:**
  - My probes: 216 sources pack, and 217 are refused only by `L12 descriptor-maximum: … is 510 bytes, above 508` (`receipts/l6_probes.txt`). This agrees with the author's `probe_216`.
  - A plant capping `clock_sources_count` at 215 SURVIVES the gate. The generic 508-octet boundary is pinned (`test_boundaries_pack`), but not on a CLOCK_DOMAIN.
- **Outcome:** optionally, a 216-source positive and a 217-source negative in the gate.

### Carried suggestions (retained, not taken; this round is merge-only)

- R434-3 S1: direct `model_lint` load. Unchanged; see R1.
- R435-3 S1: `test_one_guarded_loader` does not pin the `model_rules` route. Unchanged; the author reports `g-own-loader` still survives.
- R434-2 S2: a top-level IDENTIFY preference.
- R434-1 S3: a verbatim `ut` `current_format`.
- R434-1 S4: mutations pin their named check, not their exact check set.

### Observation (not a finding)

- Beside a CRF input, the lint sets no per-AAF-input count. Two INPUT_STREAM sources at each AAF input pack (`receipts/l6_probes.txt`).
- This is disclosed: "Beside a CRF input, the lint sets no count for an AAF input, as §5.3.3.6 sets none". It follows the round-2 ruling (conform to the standard; no strictness the processor does not need), and the processor reads only `clock_sources_count`.
- Without a CRF input, sources at two AAF inputs are refused (`aaf-input-source`), as main's L6 ("or on the single AAF input when no CRF input exists") states. That behaviour is unchanged since round 3.

## Prior public findings at this head

| Finding | Original severity | Status at bd86f646 | Evidence |
|---|---|---|---|
| R434-1 F1-F4, R435-1 F1-F6 (closed round 2) | MINOR | still CLOSED | My role's `plant.py`, run unchanged: 24 KILLED, 4 not applicable (rewritten targets, as at round 3), expected-pass control green (`receipts/prior_r434_plant_bd86f64.txt`) |
| R434-2 F1, F2; R435-2 F1, F2 (closed round 3) | MINOR | still CLOSED | `plant_r2.py` 37/37, `plant_r3.py` 40/40, `plant_r435_titles.py` 8/8 KILLED, scripts sha256-equal to the R434-3 manifest (`receipts/prior_r434_plant_r*_bd86f64.txt`); refusal-statement deletion 85/85 KILLED (`receipts/prior_r434_refusal_statements_bd86f64.txt`) |
| R435-2 R1 (PR title) | RESIDUE | still CLOSED | title reads "L1 to L12" |
| R434-3 S1 | SUGGESTION | retained (not taken) | `receipts/direct_import_model_lint_bd86f64.txt`; see R1 |
| R435-3 S1 | SUGGESTION | retained (not taken) | `model_lint.py`, `gen_desc_image.py` and the test unchanged since round 3 (`receipts/merge_sides.txt`) |
| R434-2 S2; R434-1 S3, S4 | SUGGESTION | retained (not taken) | unchanged code |

R434-3 and R435-3 recorded no open MINOR or higher finding, and none reopens here.

## Lens evidence

### Conformance: CLEAN

- **07 §3.1 L6** (`07_memory_maps.md:186`) against the code (`model_rules.py:672-732`):
  - "≥1 CLOCK_SOURCE per CLOCK_DOMAIN" is `domain-source-count`.
  - "exactly one INPUT_STREAM per CRF-capable input" is `crf-input-source`.
  - "or on the single AAF input when no CRF input exists" is `aaf-input-source` (total == 1).
  - "≥1 INTERNAL if any output" is `internal-source`.
  - "list sits at 76, `76 + 2 × count` long, identity 0..count-1" is `domain-source-offset`, `-length` and `-identity`.
  - "names existing CLOCK_SOURCEs" is `domain-source-exists`.
  - "gPTP … single-interface" is `gptp-source-interfaces`.
  - "the AAF allowance beside a CRF input" matches: no check counts AAF inputs while a CRF input exists.
  - "neither … reads an order" matches: no check reads a descriptor index's class.
- **Arithmetic and probe:** 76 + 2 × 216 = 508. 216 sources pack and 217 are refused by `descriptor-maximum`.
- **The citation change:** `domain-source-identity` → IEEE 1722.1-2021 §7.2.32 (the CLOCK_DOMAIN descriptor's `clock_sources`). This is the clause main's L6 names for the membership test. §7.4.23.1 stays in the row for the response's current index, as main has it.
- **REQ-MDL-005:** main's clause and requirement, with the lint added to Arch. It is consistent with the L6 row.
- **Parent models** (`receipts/pack-*.txt`; scratch parents built by `scripts/mk_parent.sh` with C4C6 then C8; at #634 the C8 `aem_assemble.py` hunk is ported by its one line, as disclosed):
  - At #634 `0b066b6e`, each model carries #629's sources in D1 order: arty_4x4 6, arty_8ch 6, arty_current 3, ax7101_1x1_tdm8 3, ax7101_8x8 10. At dev `cdf49d1a` each has 2.
  - Four pack with no waiver.
  - `ax7101_8x8` packs only with its #584 waiver. It is refused without it, and refused as stale when the waiver is widened by one.
  - Every builder image equals `build(adp=)`'s image, and the driven ADP values are checked.
  - Output is byte-identical with the processor at `97f6eace` and at head, at both parent heads, and the digests equal the author's.

### RTL: CLEAN

- The merge plus commit add no RTL of the lane's own.
- Against main, the only `.sv` delta is the lane's comment-only `KL_aecp_desc_store.sv` edit, unchanged since round 3.
- main's `pp_top_wrap.sv` and `gen_ucode.py` (comment) changes are carried byte-exact.
- No port, parameter or register changes.
- `lint_hdl.sh` rc 0 with pinned Verilator 5.050 (`receipts/lint_hdl_bd86f64.log`, `receipts/tool_identity.txt`).
- `run_suites.sh` rc 0, `desc_store` 584 and `pp_top` 9,168 (`receipts/run_suites_bd86f64.log`).

### Robustness: CLEAN

- The merge changes no code path except one refusal string (`model_rules.py:174`).
- No parent file at either head names the check (`receipts/parent_quote_grep.txt`).
- In the processor, only 07's Checks column, `lint_mutations.py` and `CHECKS` name it, and none of them quotes its clause parenthesis.
- The new test builds its model only through the gate's existing helpers.
- L6 on unusual shapes behaves as at round 3. That covers reordered lists, duplicate AAF sources, the 216/217 boundary, and no-CRF models with several AAF sources (`receipts/l6_probes.txt`, identical at head, merge and `97f6eace`).

### Tests: CLEAN (S1, S2 suggestions)

- **Gate:** 59 tests OK at head and 58 at `97f6eace`. The verbose test lists differ only by the new case (`receipts/gate_verbose_*.log`).
- **Suppression:** 56/56 at both heads, logs equal (`receipts/lint_suppression_*.log`).
- **Reviewer plants** (`scripts/l6_plants.py`, `receipts/l6_plants_reviewer.txt`), each run at head and at merge `3bfc7c6`:
  - The author's five: at most one AAF source beside CRF; none beside CRF; count cap 8; cap 9; at most two INPUT_STREAM sources. All KILLED at head; at the merge, 1 of 5.
  - Mine: AAF sources only below input 2; sources ≤ STREAM_INPUT count; one AAF input with a source; CRF source after AAF sources; CLOCK_SOURCE descriptors ≤ 9. All KILLED at head.
  - `order-internal-first` and `domain-count-cap-215` SURVIVE (S1, S2).
- **The author's README plant table** (`tb/desc_store/README.md:202-212`) matches my results row by row, including that only "no AAF source beside CRF" is also caught by `test_boundaries_pack`.
- **Prior R434 scripts, unchanged** (sha256 equal to the R434-3 manifest):
  - `plant_r3.py` 40/40;
  - `plant_r2.py` 37/37;
  - `plant_r435_titles.py` 8/8;
  - `plant.py` 24 KILLED, 4 not applicable, control green;
  - `refusal_statements.py` 85/85.

### Docs: CLEAN (R1 residue)

- 07 L6 and REQ-MDL-005: see Verdict item 1 (`receipts/conflict_cells.txt`).
- 09 §8.5 `ConformingModelTest` row (`09_verification.md:313`) and `tb/desc_store/README.md:96-104, 202-212` describe the new case and the plants accurately.
- The PR body's line references all resolve: `07:186`, `00:450`, `model_rules.py:174`, `test_gen_desc_image.py:455`.
- **Gates at head:**
  - `make check` rc 0 (41 mermaid / 18 wavedrom, 1,050 links, 115 REQ / 17 GAP, 94 module rows, 27 parameters);
  - `gen_matrix.py --check` rc 0;
  - `git diff --check` over `631eeb34..` and `97f6eace..` rc 0.
- Every Round 4 claim in the PR body is reproduced above, except the parent consumer set of 16 (manager's). The only defect is R1.

## Executed checks at this head

| Check | Result | Receipt |
|---|---|---|
| re-merge `97f6eace` + `631eeb34` | 2 conflicts (00, 07); 12/12 auto-merged files equal `3bfc7c6`; one extra line (`model_rules.py:174`) | `receipts/remerge.txt`, `receipts/merge_sides.txt`, `receipts/conflict_cells.txt` |
| `run_suites.sh` (pinned Verilator 5.050) | rc 0; 33 suites; 1,019,127 checks; tallies equal the author's | `receipts/run_suites_bd86f64.log`, `.rc` |
| packer gate | 59 OK (58 at `97f6eace`) | `receipts/gate_*` |
| `lint_suppression.py --jobs 4` | 56/56 both heads, logs equal | `receipts/lint_suppression_*.log` |
| `git apply --check`, campaign patches | 207/207 | `receipts/apply_check_bd86f64.txt` |
| `make check`, `gen_matrix.py --check`, `lint_hdl.sh`, `git diff --check` | rc 0 each | `receipts/make_check_bd86f64.log`, `gen_matrix_bd86f64.log`, `lint_hdl_bd86f64.log`, `diff_check_bd86f64.txt` |
| L6 plants (12) at head and merge | head: 10 KILLED, 2 SURVIVED (S1, S2); merge kills 1 of the author's 5 | `receipts/l6_plants_reviewer.txt` |
| L6 probes (11) at head, merge, `97f6eace` | identical at all three | `receipts/l6_probes.txt` |
| new case shape | INTERNAL 0, CRF 1, AAF k at 2 + k, ten sources | `receipts/new_case_shape.txt` |
| parent five models, processor head vs `97f6eace`, at dev `cdf49d1a` and #634 `0b066b6e` | byte-identical; digests equal the author's | `receipts/pack-*.txt`, `receipts/mkparent-*.txt` |
| prior R434 scripts, unchanged | 40/40, 37/37, 8/8, 24+4 n/a, 85/85 | `receipts/prior_r434_*` |
| hosted runs (read-only, 20:03Z) | `docs-gates` and `portability` succeeded in runs 37056441023 and 37056436937; both `suites` jobs were in progress | `receipts/hosted_check_runs_bd86f64.txt` |

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 07 §3.1 L6 and 00 REQ-MDL-005 at base, lane, main, merge, head; `model_rules.py` `CHECKS` L6 and `_rule_domains`/`_rule_sources`; 06 §6.4 and the E_SCLKS comment; 11 L6 probes; five parent models at dev `cdf49d1a` and #634 `0b066b6e` | R434-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |
| RTL | CLEAN | `.sv`/ucode delta against main and round 3 (lane comment-only; main's carried byte-exact); `lint_hdl.sh`; `run_suites.sh` 33 suites | R434-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |
| Robustness | CLEAN | the one changed refusal string and its consumers; L6 edge shapes (order, duplicates, 216/217, no-CRF) at three trees | R434-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |
| Tests | CLEAN (S1, S2) | new `test_a_source_per_aaf_input_beside_crf`; gate 59; suppression 56/56; 12 L6 plants at head and merge; prior R434 scripts unchanged; 85 refusal statements | R434-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |
| Docs | CLEAN (R1 residue) | 07 L6 row, 00 REQ-MDL-005, 09 §8.5 row, `tb/desc_store` README, `tb/pp_top` README note, PR body Round 4; `make check`, `gen_matrix --check`, `git diff --check`, 207 patches | R434-4 | bd86f6466baa77113eea2266c00044c3a29678f2 |

## Real limits

- **Not run, by assignment:** the parent consumer set (16), the donor bank (9), the parent builder test, the RTL mutation campaigns, and the Yosys/builder banks. I ran the processor suites, the gate, the suppression driver, the docs gates, the patch apply check, and my own packing through the parent's builder and `build(adp=)` paths.
- **The parent CLI caller (`gen_aemi_image.py`) was not run.** The author's `cli-*` receipts cover it.
- **The parent trees are scratch:**
  - `git archive` of dev `cdf49d1a` and #634 `0b066b6e`;
  - gptp-processor at its gitlink `5dce647a`;
  - the processor a clone at the stated commit;
  - `third_party/verilog-axis` and `external` not checked out, which packing does not read.
- **`suites` contention:** another reviewer session's `run_suites.sh` shared the host while mine ran. Mine finished rc 0.
- **Clause readings:** the clause checks rest on the text of the docs and code, and on clause numbers established in prior rounds. No spec text is in this packet.
- **Hosted `suites`** was in progress at my look. It is not evidence here.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- The donor bank (9) and the parent consumer set (16) at this head, with `parent-adoption-c4c6-ea3fb388.patch` then `parent-adoption-c8-cdf49d1a.patch`. At #634, the C8 `aem_assemble.py` hunk needs its one-line port.
- Hosted and act acceptance of the exact head, including both in-progress `suites` jobs.
- The final current-dev candidate at the merge turn: source base `631eeb34`, live dev `cdf49d1a`.
- Carry R1 to the residue checklist.

## Restore check

- The review clone is at `bd86f6466baa77113eea2266c00044c3a29678f2`, and `write-tree` equals tree `973da49d27ae9f7e160d7480ba1af4ef96e54821`.
- `status --porcelain --ignored`, `diff-index HEAD` and `diff-files` are empty.
- The index equals the HEAD tree in mode, blob and path for all 478 entries.
- The repository records no gitlinks and has no `.gitmodules`, so no submodule pin applies (`receipts/restore_check.txt`).
- Every build, plant and probe ran in copies under `scratch/`, which is not published.

R434-4 FINISHED

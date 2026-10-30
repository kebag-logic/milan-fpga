[R743] POSITIVE - exact head 6d1d038343e1f0a6b2027cce857a33528b8c2ac7

Issue #210 / PR #211, round R743-3. This is a delta review from the round-2 head `0ea635ea22eeb6d97335c4e814eede1ac0d67ebc` to the exact head `6d1d038343e1f0a6b2027cce857a33528b8c2ac7` (tree `dafc0c31e941eb3bf7106fa4da39c1415a9afc6c`, source base `a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645`). The delta is 4 commits and 11 files: 9 Markdown pages, `docs/INVENTORY.md` and `scripts/check-doc-inventory.py`. It changes no RTL, generator, generated file, test source or workflow. The repository has no AGENTS.md or CONTRIBUTING.md. The scope and authorities are those reconstructed in R743-1 and R743-2, and this delta does not change them.

## Verdict

R743-2-F1 is resolved at its cause. The concept page's banner no longer states a count: it names the `ucpu_op_e` enum and links to 06 §8. The inventory gate now fails on a µISA operation count stated on any current page, or in a retired page's banner, other than 06 §8's derived heading. Every drift this round asked for was planted at the exact head, and each one fails a gate:
- a fake operation in the table, and a fake operation in the enum;
- a wrong count on the heading line;
- the banner's old count;
- each dropped link target.

The clean head passes every gate. Every count this round changed is now derived, linked, or reworded so that it states no count. No MINOR, MAJOR or BLOCKER finding is open. This report records three suggestions and one wording residue, plus the prior items carried forward.

## Prior findings at this head

| Finding | Status | Evidence |
|---|---|---|
| R743-2-F1 (MINOR, Docs, RTL): the concept page banner said "29-operation ISA", but `ucpu_pkg.sv` declares 30 | **RESOLVED** | `IEEE_1722_1_Hardware_Protocol_Processor.md:18` now reads "a different ISA, the `ucpu_op_e` enum in [`hdl/aecp/ucpu_pkg.sv`] ... [06 §8](docs/architecture/06_aecp_engine.md#8-µcode-architecture) lists it and records which sketch operations were dropped and why". This is the outcome R743-2 asked for. The enum has 30 `OP_` members, and 06:1427 says 30. The gate holds it there (`receipts/plant-r3.txt` C0, T1, T2, H1). The anchor resolves: the link gate passes, and plant L1 shows that renaming `## 8. µcode architecture` fails this link and two others. The optional extension R743-2 offered is also taken: the gate now holds the banner. B1 and B2 fail; B3, a historical body count, passes. A paragraph-joined scan of every tracked Markdown file (`receipts/para-scan.txt`) finds µISA counts only in the derived heading and in the retired concept page's body (`:1098`, history). |
| R743-2-S1 (SUGGESTION): `target_findings` reads only the first `check:` line | **Retained, disclosed** | The code is unchanged (`scripts/check-doc-inventory.py:91`). The PR body now lists it under "Not fixed here". |
| R743-2-S2 (SUGGESTION): the operation spelling comes from any upper-case leading comment word | **Retained** | `OP_MEMBER` and `SPELLED` are unchanged. The gate still fails closed, never open. |
| R743-2-S3 (SUGGESTION): name the commit the plants ran on | **RESOLVED** | The PR body says the round-3 plants ran "on a disposable clone of exactly `6d1d038`", and the round-2 plants "at `06c934b`; reproduced by review at `0ea635e`". |
| R744-2-RES1 (RESIDUE): `tb/adp_engine/README.md:330` still has "(review R406-1 F-1)" | **Retained (inherited residue)** | `:330` is unchanged, and the round-3 diff of that file does not touch the label (0 hits). It is one of the 156 R-labels the PR discloses, tracked by #746. It remains RESIDUE; the fix is to delete the parenthetical. |
| R743-1-S1 to S4 (carried in R743-2 and R744-2) | **Retained as suggestions** | None of the code they concern changed (`ROW`, `markdown_files`, the stale-row evidence, the glossary citation). |

## Findings at this head

No MINOR, MAJOR or BLOCKER.

### R743-3-S1: SUGGESTION. The restated-count check works per line and on digits only, but its descriptions read wider
- **Lenses:** Robustness, Docs.
- **Where:**
  - The check: `scripts/check-doc-inventory.py:113` (`UISA_COUNT`), matched line by line at `:131`.
  - Its descriptions: `docs/architecture/09_verification.md:138` ("no other current page, and no retired page's banner, states a µISA operation count"), `docs/INVENTORY.md:12-13`, and the Gates section of the PR body.
- **Evidence:** the following plants on `tb/ucpu/README.md:5`, a current page, pass the gate with rc 0 at the exact head (`receipts/plant-r3.txt`):
  - G1: a count wrapped across a line break ("µISA, all 30 / operations of it");
  - G2: "thirty operations";
  - G3: "a 30-op ISA";
  - G4: "30 opcodes";
  - G5: "µcode set of 30 operations", without the word ISA.

  These pages are hard-wrapped at about 90 columns, so G1 is the case most likely to occur. The one-line digit form, which both real instances used, is caught (B1, B2, R1, R2, H2 to H4).
- **Why this is not a MINOR:** the gate is neither broken nor vacuous. It catches the class it was built for. The tree is clean under a stricter scan that joins each paragraph's lines and also accepts number words, opcodes and instructions (`receipts/para-scan.txt`, `scripts/para_scan.py`). No statement in the tree is wrong. This matches how R743-2-S1 graded the analogous `check:`-line limit.
- **Suggested outcome:** one of the following.
  - Match over paragraphs instead of lines: split on blank lines, join each paragraph's lines before applying `UISA_COUNT`, and report the paragraph's first line. Also accept `opcodes?`, `op`, `instructions?`, `µops` and number words. Add a self-test case with the count wrapped across two lines.
  - Or narrow the descriptions to what the check does: "states a µISA operation count on one line, in digits". Then add the remaining limit to "Not fixed here", as was done for the `check:` line.
- **Verification:** re-run G1 to G4; each must be named RESTATED. C0 must still pass.

### R743-3-S2: SUGGESTION. `tb/timer_map/README.md` now says two independent shape lists agree, and nothing checks it
- **Lenses:** Tests, Docs.
- **Where:** `tb/timer_map/README.md:57` ("elaborates both maps at the same shapes (`SI_TBL_C`, `SO_TBL_C`)") and `:93` ("both maps at gate 1's shapes").
- **Evidence:** the statement is true at the head. `shape_elab.sh:42` `LEGAL="1:1 1:8 8:1 2:2 4:4 8:8 9:9 9:2 3:12 16:16"` equals `timer_map_wrap.sv:107-108` `SI_TBL_C`/`SO_TBL_C`, pair for pair and in order. No file in `tb/timer_map/` compares the two lists. The old wording ("ten shapes", twice) was no better guarded, so this round makes nothing worse.
- **Suggested outcome:** either have `shape_elab.sh` or the C++ model assert that `LEGAL` equals the wrap's tables, or write "at the shapes of `SI_TBL_C`/`SO_TBL_C`, which today equal gate 1's `LEGAL`". The second option keeps the README accurate if the lists diverge.
- **Verification:** change one pair in `LEGAL`; the new check, if added, must fail.

### R743-3-S3: SUGGESTION. Cite the issue in the new check's docstring
- **Lenses:** Docs.
- **Where:** `scripts/check-doc-inventory.py:116-121` (`restated_uisa`).
- **Evidence:** the comment rule says source comments state behaviour and reason, with issue and requirement IDs. The new docstring states behaviour and reason but cites no issue ID, and the module docstring cites none either. The delta adds no lane, round, reviewer or comment label (scan of the lines `git diff 0ea635ea..HEAD` adds: no hits).
- **Suggested outcome:** add "(#210)" where the docstring gives the reason.

### R743-3-RES1: RESIDUE. The rewording lengthened lines past the pages' wrap width
- **Lenses:** Docs.
- **Where:** added prose lines over 100 columns, table rows excluded:

  | File | Lines (length) |
  |---|---|
  | `README.md` | `:74` (101) |
  | `docs/architecture/09_verification.md` | `:379` (142), `:383` (102) |
  | `tb/acmp_nvm/README.md` | `:9` (118) |
  | `tb/nvm_port/README.md` | `:15` (105), `:17` (128) |
  | `tb/srp_top/README.md` | `:710` (120) |
  | `tb/timer_map/README.md` | `:39` (133) |
- **Impact:** source readability only. The pages render the same.
- **Exact fix:** reflow each paragraph to the surrounding width of about 90 columns. Change no words.

## Lens results

| Lens | Result | Artifact-specific evidence |
|---|---|---|
| Conformance | CLEAN (carried) | The delta changes no clause citation and no conformance statement. Its Markdown edits are counts of builds, shapes, models, guides and operations, plus the µISA banner. The R743-2 verdict over 02 §4.1 and the 802.1Q-2014 §34 citations stands. |
| RTL | CLEAN | In `hdl/aecp/ucpu_pkg.sv`, the `ucpu_op_e` enum has 30 `OP_` members (`OP_NOP = 5'd0` to `OP_SHIFT_R = 5'd29`), and the banner now names the enum without a count. No RTL changed in this delta. 06 §8's count and table equal the enum (C0), and a planted enum member is caught (T2). The "29 operations" comments at `ucpu_pkg.sv:14,48` remain; the PR body discloses them. |
| Robustness | CLEAN | Examined the delta in `scripts/check-doc-inventory.py`: `UISA_COUNT`, `restated_uisa`, its call in `check`, and the five new self-test cases. The self-test runs 30 cases, OK: 25 faults plus 5 clean controls, as the PR body says. I ran a control plus 24 plants at the exact head (`receipts/plant-r3.txt`). Every required drift fails, and the history-body control passes. A retired page's banner is taken as its first contiguous `>` block, which covers the whole concept-page banner (`:4-24`). In 06, only `**µISA (N operations)**` at the start of the line is stripped, so the rest of that line is still checked (H2, H3). The limits are recorded as S1. |
| Tests | CLEAN | I checked each rewritten build or shape statement against its Makefile or source: <ul><li>`tb/acmp_nvm` `run`: two builds, NR == 2.</li><li>`tb/adp_engine` `run`: two builds, NR == 2.</li><li>`tb/dyn_state` `run`: 2x2, then 1x1.</li><li>`tb/nvm_port` `run`: `suite` at `TMO`=100, `TMO_ALT`=37, `TMO_MIN`=20, then `FUZZ_TMOS`.</li><li>`tb/srp_top` `STORE_SHAPES = 1x1 2x2 3x5 9x9`.</li><li>`tb/srp_admission` `shapes`: N=1,2,3,5,8.</li><li>`tb/nvm_port/measure_figures.py:500` `MODELS`: nine entries.</li><li>`tb/timer_map`: see S2.</li></ul> The measured tallies are unchanged: 388 = 372 + 16, 1359 = 1348 + 11, 118 = 62 + 56, and 393. The README inputs to the `tb/nvm_port` figures gate are byte-identical at `0ea635e` and `6d1d038`: the author's two JSON receipts are identical and match their published hashes. |
| Docs | CLEAN | I read all 11 changed files. Every count this round changed is now in one of three forms. **Derived:** the 06 µISA count. **Linked:** each suite's Makefile `run`; `TMO`, `TMO_ALT` and `TMO_MIN`; `STORE_SHAPES`; the admission Makefile's `shapes`; `MODELS`; `LEGAL`; 09 §7; 06 §8. **Reworded with no count:** "the others", "every guide", "every build", "each state of the port's machine". The figures kept are measured tallies, deadline bounds and the history body. Plants L1 to L7 show that dropping any new link target fails the link gate or the inventory gate. The renamed srp_top heading's anchor resolves, and no link to the old anchor remains (the link gate checks 1418 links, OK). The scan of added lines finds no lane, round, reviewer or issue-comment label. Wording residue: RES1. |

## Ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta Markdown (no clause edits); R743-2 verdict on 02 §4.1 and 802.1Q-2014 §34 carried | R743-3 (delta), R743-2, R743-1 | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |
| RTL | CLEAN | `hdl/aecp/ucpu_pkg.sv` enum; concept banner `:18`; 06 `:1411`, `:1427` | R743-3 | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |
| Robustness | CLEAN | `scripts/check-doc-inventory.py` delta and self-test; control plus 24 plants; paragraph scan | R743-3 | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |
| Tests | CLEAN | Makefiles of acmp_nvm, adp_engine, dyn_state, nvm_port, srp_top and srp_admission; `measure_figures.py` `MODELS`; `shape_elab.sh`; `timer_map_wrap.sv`; author's nvm-inputs receipts | R743-3 (delta), R743-1 (suite runs) | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |
| Docs | CLEAN | all 11 changed files; label scan of added lines; link gate; R744-2-RES1 row | R743-3 | 6d1d038343e1f0a6b2027cce857a33528b8c2ac7 |

## Gates run in this review (`receipts/gates-head/`, a disposable clone of the exact head)

| Gate | rc |
|---|---|
| `make check` (wavedrom 2.0.3.post3, Mermaid CLI, pinned Verilator 5.050 with its identity checked): inventory self-test 30 cases OK, 63 files OK | 0 |
| `python3 scripts/gen_matrix.py --check` | 0 |
| `python3 scripts/check_upc_map.py` | 0 |
| `python3 scripts/check_m9_opcodes.py --selftest`, then without | 0, 0 |
| `./scripts/lint_hdl.sh` | 0 |

The plants are in `receipts/plant-r3.txt`, produced by `scripts/plant_r3.sh`. Each plant was restored before the next, and the clone ends at the head with an empty status.

## Published evidence checked

- **Author's round-3 receipts:** milan-fpga `a397e609…/review-evidence/pp210-r1`, against its `MANIFEST.json`. The downloaded bytes match the published sha256 for the author's round-3 `rc.txt`, `plant-6d1d038.txt`, `head-6d1d038-make_check.log` and both `nvm-inputs-*.json` (`receipts/author-r3-hashcheck.txt`). The author's `rc.txt` shows every gate at rc 0, at base and at `6d1d038`. The author's plant receipt names RESTATED for the banner (with either count), for a current page and for 06's heading line, which agrees with my independent plants.
- **Signature:** the evidence commits are integrity-checked by the manifest's hashes. GitHub reports them as unsigned, so I verified no cryptographic signature. That is a limit, not a finding.
- **Hosted check runs** at the exact head: `docs-gates` completed with success (2 runs), `portability` completed with success (2 runs), and `suites` was still in progress (2 runs). I draw no conclusion from the suites job; the manager owns hosted acceptance.

## Real limits

- Physical calibration was not run, and no hardware was used. No field skip is hardware proof.
- I did not run `make -C tb/nvm_port figures` or any suite bank. The delta changes no test source or RTL, and the figures gate's README inputs are byte-identical across the round. The hosted suites job was still in progress.
- No manager source bank exists at this exact head, and I neither claim nor infer one. The source-head execution evidence is the author's published receipts plus the gates I ran.
- I did not read the other reviewer's round-3 report.

## Pending manager duties

- At the merge turn, validate the current-dev merge candidate with the builder and native banks (source base `a9e84b66`, live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`), and link the receipts on the PR.
- Own hosted and act acceptance, including the `suites` job, which was in progress when I inspected it.
- Carry R743-3-RES1 and R744-2-RES1 to the residue checklist.
- Track the PR's "Not fixed here" items as follow-ups: the source-comment clause numbers, `ucpu_pkg.sv:14,48`, diagram 22, the 156 R-labels under #746, and `shape_tally.txt`. The PR keeps "Refs" for issue #210.
- This head still needs two independent positive reviews.

## Receipts and scripts

- `scripts/gates.sh <checkout> <outdir>` runs the gates. Put a `python3` that imports wavedrom 2.0.3.post3, and the pinned Verilator, first on `PATH`.
- `scripts/plant_r3.sh <head-clone> <out>` runs the plants and restores the clone after each.
- `scripts/para_scan.py <checkout>` is the paragraph-joined count scan. Run it with `python3 -I`.
- `receipts/final-integrity.txt` records the review clone's state after all probes:
  - it is at the exact head and tree, with an empty status (ignored files included);
  - the index equals the tree, blob IDs and modes included (736 files at 100644, 18 at 100755), and the worktree equals the index;
  - the repository has no submodule gitlinks.
- The disposable clones and the downloaded evidence stayed under `scratch/` and are not published.

R743-3 FINISHED

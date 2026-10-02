[R431] NEGATIVE - exact head 4a40b1798e463d09aafd74632408003229bcc673

# R431-1: independent external review of protocol-processor issue #141 / PR #142

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `4a40b1798e463d09aafd74632408003229bcc673`, tree `b258cbd7b41dc2b96354173e9297427295be117b`
- Base: `03c842a780064048b0a1a3de29214174a1c13934` (processor `main`); four lane commits `c8edfe5`, `9afbc48`, `39fd019`, `4a40b17`
- Scope reconstructed from: the repository's `README.md` and `docs/README.md` (the tree has no `AGENTS.md` or `CONTRIBUTING.md`), issue #141's body and comments (assignment 5942683005, ruling 5946147101), the PR body, the parent design `docs/design/MEDIA_CLOCK_FOLLOWING.md` at milan-fpga `cdf49d1a` ("Clause findings" (a) and (d), "Source list and order", "Protocol-processor changes", D1), the diff `03c842a7..4a40b179` and its history, and the public evidence at milan-fpga `d57953c0` `review-evidence/pp141-r1` (author `HANDOFF.md`, `PR-BODY.md`).
- All receipts were produced in this review at the exact head. The pinned Verilator 5.050 was used, and each build was capped at 8 jobs.

## Verdict

**NEGATIVE.** The documentation and the D3C tests meet the issue in full, and so do the pre-check and the mutants. I re-ran all of them at the head. One gate fails: **the AECP dispatch mutation campaign does not complete at this head** (F1). The ruling's comment-only commit `4a40b17` re-wrapped two `gen_ucode.py` comment lines. `tb/pp_top/aecp_dispatch_mutations/lk-prefix-zero-body.patch` carries those two lines as context. At `4a40b17` that patch no longer applies, and `make -C tb/pp_top aecp-dispatch-mutants` aborts with rc 1. The local run shows this, and so does the hosted CI `suites` job at the exact head. The assignment's gate "every processor suite and campaign rc 0" (dispatch 37/37) is therefore not met at this head. The PR body's figures for that campaign were measured at `39fd019`, before the commit that broke it.

## What was verified (all at the exact head unless stated)

| Item | Result | Receipt |
|---|---|---|
| Pre-check: SET range check (`hdl/aecp/ucode/gen_ucode.py:1663-1664`) | `CHECK_ARG ra=12 rb=9 FMT_W REL_LT`. r9 is the located domain's `clock_sources_count` (lane 72, bits 47:32, `FMT_W`). r12 is `{48'd0, setval_r[63:48]}` (`KL_aecp_engine.sv:1563`). The compare is the unsigned 33-bit borrow of the zero-extended operands (`KL_aecp_ucpu.sv:236-239`, `:248`). It accepts exactly index < count, for any count up to 65,535 | reading |
| Pre-check: restore compare (`hdl/aecp/KL_aecp_nvm_writer.sv:502`) | `rval_r[15:0] < sb_rdata_i[47:32]`, unsigned 16-bit, against the same lane. The row is 16 bits (`KL_aecp_dyn_state.sv:186`), and so is the export (`:114`, `:352`; `protocol_processor_top.sv:712`) | reading |
| No RTL or microcode change | `git diff 03c842a7..4a40b179 -- hdl` touches only `gen_ucode.py`, which differs in comment tokens only (13,424 identical non-comment tokens). `ucode.hex` (26,624 B, `3559d0a6...`), `ltn_rom.hex` (6,138 B, `23cc67ee...`) and `image.bin` (1,880 B, `20356f59...`) are byte-identical at the base and the head, and equal the PR body's hashes | `receipts/rom_identity.txt` |
| Section D3 at the head | `D3: 150 checks, 0 failures` | `receipts/head_d3.log` |
| Every D3C check executed | A disposable probe printed passing checks. All 17 D3C checks ran and passed, with these measured values: D3C1 effects (1,1,1), row 9 valid 1 export 9; D3C3 save 1 erase 1 write 0 other; D3C2 effects (0,0,0), 0 frames, 0 pending cycles, 0 operations; D3C3 restore applied 1 refused 0 blank 26; D3C4 at the count and above it applied 0 refused 1 blank 26, row 0 valid 0 export 0 | `receipts/verbose_head_d3.log` |
| All four `tb/pp_top` builds (the wrap and `sim_main.cpp` changes reach each) | default 8,624/0, line 218/0, timebase 56/0, fixture 20/0 = 8,918, as the PR states. The wrap change only removes one pre-existing `PINCONNECTEMPTY` warning | `receipts/head_pp_top_*_build.log` |
| `d3_mutants.py`, all 87 | 87 of 87 KILLED and every golden PASS, run in seven `--only` chunks. All 75 `tb/pp_top` README rows agree with the measured failing counts, the five raised ones included: `TRG_clks` 10, `RPL_clks` 5, `rule_ignored` 7, `unframed_reads_as_device_error` 42, `done_without_d3` 45. So do the four new rows (`clks_row_two_bits` 10, `clks_restore_count_narrowed` 2, `clks_restore_index_narrowed` 4, `clks_restore_bound_inclusive` 4), the 11 `tb/acmp_nvm` rows and the `tb/rx_validator` M4 row | `receipts/head_d3_mutants_*.log`, `receipts/d3_mutants_counts.txt`, `receipts/d3_mutants_*.results.json` |
| The two new dispatch arms (`d3` target) | control `d3` PASS. `sclks-bound-three` KILLED with 11 failures, `sclks-bound-inclusive` KILLED with 6, both equal to the README | `receipts/head_dispatch_sclks.log` |
| Whole default build with `sclks-bound-three` planted | 8,624 checks, 11 failures, all of them D3C. This confirms the README's "fails D3C's eleven checks and nothing else" | `receipts/probe_whole_default_sclks_bound_three.log` |
| The other 34 dispatch arms | Run with `--only` around the broken arm: all KILLED, controls PASS, every count equals the README | `receipts/head_dispatch_c0*.log`, `receipts/dispatch_counts.txt` |
| `lk-prefix-zero-body` at the head | Refused by `git apply --check`. The campaign aborts with `CalledProcessError`, rc 1, and writes no `results.json`. The patch applies at `39fd019` (F1) | `receipts/head_dispatch_lk_prefix.log`, `receipts/lk_prefix_apply_by_rev.txt`, `receipts/patch_apply_check.txt` |
| Hosted CI at the exact head (read-only) | Push run 36969624563, job `suites`, failed at step 10 "AECP dispatch mutation campaign" with the same traceback. Steps 11 and 12 were skipped. `docs-gates` and `portability` passed. The pull-request run 36969627550 was still in progress when read | `receipts/hosted_head_suites_failure_excerpt.txt` |
| Every other campaign patch | All 77 other patches in `aecp_dispatch_mutations/` and `mutations/` apply at the head. The hosted step 9 (`aecp-mutants`) passed at the head | `receipts/patch_apply_check.txt` |
| Docs gates | `make check` (41 mermaid + 18 wavedrom, 1,017 links, 115 REQ / 17 GAP, 94 rows 0 untested, 26 parameters), `check-links`, `check-matrix`, `check-integrator-params`, `render-wavedrom --check`, `make stale`, `gen_matrix --check`, `check_upc_map` (59/87), `check_m9_opcodes` (30), and `git diff --check 03c842a7 4a40b179`: each rc 0 | `receipts/docs_gates_head.log` |
| Clone integrity after all probes | HEAD and tree exact. `git status --porcelain --ignored` is empty, and index blobs and modes equal the HEAD tree. The repository has no `.gitmodules` and no gitlinks, so it has no submodule pins to verify. Every probe ran in exported copies under the packet's scratch directory | `receipts/clone_integrity.txt` |

## Findings

### F1 - MAJOR - Tests, Robustness, Docs - the AECP dispatch mutation campaign aborts at the head

- **Where:**
  - `tb/pp_top/aecp_dispatch_mutations/lk-prefix-zero-body.patch:97-99`: hunk `@@ -1427,31 +1417,25 @@`. Its leading context is `# stored, read back and announced while the media plane resolved it to` / `# INTERNAL. The count sits mid-lane, hence SHIFT_R + a FMT_W MOVE.`
  - The head's text at `hdl/aecp/ucode/gen_ucode.py:1637-1638` is now `# backed was stored, read back and announced while the media plane resolved` / `# it to INTERNAL. The count sits mid-lane, hence SHIFT_R + a FMT_W MOVE.`, re-wrapped by `4a40b17`.
  - The CI step is `.github/workflows/hdl.yml:72-74`.
  - The README row is `tb/pp_top/README.md:1085`, under "failed at the lane head" (`:1066-1067`).
  - PR body, section "Validation": "Under the targeted re-measure rule, a comment-only change with identical ROMs re-runs no campaign", "`make -C tb/pp_top aecp-dispatch-mutants` | 4 controls PASS (`d3` new), 37 of 37 KILLED", and "No file cites `gen_ucode.py` by line number, so the one added line moves no reference".
- **Authority:**
  - The assignment (#141 comment 5942683005), "Gates: every processor suite and campaign rc 0".
  - The review focus: "every suite and campaign rc 0 (D3 87/87, dispatch 37/37)".
  - The repository's consumption contract: the pin moves only to a commit whose gates are green here (`.github/workflows/hdl.yml:2-3`, `README.md` "Building and checking").
- **Evidence:**
  - `git apply --check` of the patch: rc 0 at `39fd019`, rc 1 at `4a40b179` (`receipts/lk_prefix_apply_by_rev.txt`).
  - `aecp_dispatch_mutants.py --only lk-prefix-zero-body` at the head: control PASS, then `error: patch failed: hdl/aecp/ucode/gen_ucode.py:1427`, a `CalledProcessError` traceback, rc 1, and no `results.json` (`receipts/head_dispatch_lk_prefix.log`).
  - Hosted push run 36969624563 at the exact head: job `suites`, step 10 failed with the same error (`receipts/hosted_head_suites_failure_excerpt.txt`).
  - The published author handoff states that the campaigns were not re-run at `4a40b17`.
- **Impact:**
  - The campaign the PR adds two arms to cannot run at the head. `plant()` (`tb/pp_top/aecp_dispatch_mutants.py:150-157`) raises on the refused patch, so it does not count the arm as UNPROVEN, and every arm after `lk-prefix-zero-body` in a full run goes unrun. Those include the two new `sclks-*` arms that grade D3C1 and D3C2.
  - CI is red at the head.
  - The PR body's 37/37 claim and the README's "at the lane head" count for `lk-prefix-zero-body` cannot be reproduced at the head.
  - The PR body's premise is that a comment-only edit moves nothing a campaign consumes. It does not hold: a committed patch consumes the comment text as context. The lane's own two new patches also carry pre-`4a40b17` line numbers (both apply at offset 1).
  - Merging would put `main` red and block the parent's pin bump under the consumption contract.
- **Required outcome:**
  - Refresh `lk-prefix-zero-body.patch` against the head's `gen_ucode.py`. Its two leading context lines become the head's re-wrapped lines. Preferably regenerate the hunk headers of `sclks-bound-three.patch` and `sclks-bound-inclusive.patch` against the head too.
  - Then re-run `make -C tb/pp_top aecp-dispatch-mutants` in full at the new head: 4 controls PASS, 37 of 37 KILLED, every count equal to the README.
  - Correct the PR body's statements about the re-measure and `gen_ucode.py` references.
  - Post the hosted `suites` job green at the new head.
- **Verification:**
  - In a disposable scratch copy of the head, this review replaced exactly those two context lines one for one. The patch then applies, and the arm is KILLED with 7 failures, the README's count (`receipts/probe_lk_prefix_refresh.log`). So the fix is a test-artifact refresh with no RTL, ROM or count change.
  - Re-verify with `git apply --check` of every patch in `tb/pp_top/aecp_dispatch_mutations/` at the new head, plus the full campaign run and the hosted job.

### S1 - SUGGESTION - Conformance, Docs - state the order rule's condition

- **Where:** `docs/architecture/07_memory_maps.md:135` (L6) and `docs/00_MILAN_COMPLIANCE_REVIEW.md:425` (REQ-MDL-005).
- **Issue:** Both give "INTERNAL 0, CRF 1, AAF input k at 2 + k" without a condition. The parent design (D1, "Shapes without INTERNAL or CRF") states those numbers for shapes that declare both INTERNAL and CRF, as all five shipping shapes do. An absent class takes no index; for example, CRF is 0 on a shape without outputs.
- **Why not a defect:** The processor reads no order (L6 says so), and the frozen acceptance words the order the same way.
- **Suggested fix:** Add "where INTERNAL and CRF are both declared, as on every shipping shape; an absent class takes no index".

### S2 - SUGGESTION - Robustness, Tests - make a refused patch an UNPROVEN arm

- **Where:** `tb/pp_top/aecp_dispatch_mutants.py:150-157`.
- **Issue:** A patch that `git apply --check` refuses raises an uncaught exception. That aborts the whole campaign, and no `results.json` is written.
- **Suggested fix:** Record the refused arm as UNPROVEN, with the apply error, and continue. The campaign would still exit non-zero, and the report would show every other arm's verdict. This is pre-existing driver behaviour; F1's fix does not depend on it.

## Lens results

| Lens | Result | Artifact-specific evidence |
|---|---|---|
| Conformance | CLEAN | L6 (`07:135`) states Milan v1.2 §5.3.3.6's set as a minimum and allows one INPUT_STREAM source per AAF input beside the CRF input's (§7.2.9.2, Table 7-17). It gives the D1 order and credits membership to IEEE 1722.1-2021 §7.2.32 and BAD_ARGUMENTS to Table 7-141. It cites §7.4.23.1 only for the current index, and says Milan §5.4.2.15/.16 add no argument rule. REQ-MDL-005 (`00:425`) says the same, and its clause column gains §7.2.32 and Table 7-141. 06 §6.4 (`06:462`) and the E_SCLKS comment (`gen_ucode.py:1629-1638`) now credit the membership test to §7.2.32 and Table 7-141, as the ruling required. A sweep of every `7.4.23` citation in the tree found the rest cite it for the command or for the current-value rule. The readings agree with the parent design's clause table (a) and (d)2. The "up to 216" bound is consistent with Table 7-61 as the design reads it. S1 is a suggestion only |
| RTL | CLEAN | No RTL or microcode change: the `hdl/` diff is one comment, the ROMs are byte-identical and the non-comment tokens identical. The pre-check holds by reading the µCPU compare, the operand forms, the restore lane rule, the 16-bit row and the export. The wrap change is bench-only: it connects the existing `aecp_clk_src_index_o` (16 bits), and the top is unchanged |
| Robustness | UNCLEAN | F1: a non-semantic comment edit broke a committed campaign patch, and the driver aborts instead of grading. Otherwise robust: D3C runs on its own model; arm order makes a stored refusal show as a second save; D3C2 grades effects, pending cycles and device operations for two windows; D3C4 grades both at-count and above-count images, with the record's bytes re-checked before each restore. S2 is a suggestion |
| Tests | UNCLEAN | F1: the dispatch campaign is rc 1 at the head. All else re-run and agreeing: D3 150/0; all 17 D3C checks executed with the expected values; each item of the issue has a failing mutant (D3C1: `sclks-bound-three`, `clks_row_two_bits`; D3C2: `sclks-bound-inclusive`; D3C3: `clks_restore_count_narrowed`, `clks_row_two_bits`; D3C4: `clks_restore_index_narrowed`, `clks_restore_bound_inclusive`); `d3_mutants.py` 87/87 with every count equal to its README; the other 36 dispatch arms KILLED at their recorded counts; the four `tb/pp_top` builds 8,918/0 |
| Docs | UNCLEAN | F1: the PR body's re-measure premise, its dispatch 37/37 and "no file cites `gen_ucode.py` by line number" do not hold at the head, and neither does the README's "at the lane head" count for `lk-prefix-zero-body` (`README.md:1085`). Otherwise accurate: the `tb/pp_top` README's D3C text, its two mutation tables and its five raised counts; 09 §8.2's D3C row and "87"; REQ-AEM-013's cell; the PR body's line references (`gen_ucode.py:1663-1664`, `:1629-1638`, `:1649-1686`, `KL_aecp_nvm_writer.sv:502`, `KL_aecp_dyn_state.sv:186`, `KL_aecp_engine.sv:1563`) all check out at the head. All docs gates rc 0 |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `docs/architecture/07_memory_maps.md:135`, `docs/00_MILAN_COMPLIANCE_REVIEW.md:382,425`, `docs/architecture/06_aecp_engine.md:462`, `hdl/aecp/ucode/gen_ucode.py:1619-1686`; every `7.4.23` citation in the tree; parent `MEDIA_CLOCK_FOLLOWING.md` at `cdf49d1a` | R431-1 | `4a40b1798e463d09aafd74632408003229bcc673` |
| RTL | CLEAN | `hdl/` diff; `KL_aecp_ucpu.sv:220-250,351`; `KL_aecp_engine.sv:1555-1567`; `KL_aecp_nvm_writer.sv:80-95,486-520`; `KL_aecp_dyn_state.sv:114,180-190,352`; `protocol_processor_top.sv:712,3862`; `tb/pp_top/pp_top_wrap.sv` diff; ROM regeneration at base and head | R431-1 | `4a40b1798e463d09aafd74632408003229bcc673` |
| Robustness | UNCLEAN (F1) | `tb/pp_top/aecp_dispatch_mutants.py`, `aecp_dispatch_mutations/*.patch`, `mutations/*.patch` apply check; `d3_phases.hpp` D3C phase and image packer; `.github/workflows/hdl.yml`; hosted job at the head | R431-1 | `4a40b1798e463d09aafd74632408003229bcc673` |
| Tests | UNCLEAN (F1) | section D3 run and verbose probe; four `tb/pp_top` builds; `d3_mutants.py` 87 arms; `aecp_dispatch_mutants.py` 37 arms (36 runnable at the head, 1 refused; refreshed-context probe); whole-default `sclks-bound-three` probe | R431-1 | `4a40b1798e463d09aafd74632408003229bcc673` |
| Docs | UNCLEAN (F1) | `tb/pp_top/README.md` diff (D3C text, D3 and dispatch tables, raised counts); `docs/architecture/09_verification.md` §8.2; REQ-AEM-013; PR body; docs gates and generator-consistency scripts | R431-1 | `4a40b1798e463d09aafd74632408003229bcc673` |

## Real limits

- The IEEE 1722.1-2021 and Milan v1.2 texts are copyrighted and not distributed. I checked the clause readings against the merged parent design's clause tables and the tree's own internal consistency, not against the PDFs.
- I did not run `./scripts/run_suites.sh`, `./scripts/lint_hdl.sh` or the other processor campaigns (SRP, MAAP, ADP, `aecp-mutants`, `acmp_mutants.py`, `gsi_mutants.py`, `name_wr_mutant.py`, `tb/nvm_port figures`, and the others in the PR's table) locally. The diff does not reach their inputs beyond `tb/pp_top`, whose four builds and two affected campaigns I ran. The hosted job at the head passed lint, every suite and the SRP, MAAP, ADP and `aecp-mutants` steps. Its traceability and `nvm_port` steps were skipped after F1's failure; I ran `gen_matrix.py --check` locally.
- I ran nothing in the parent repository. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The pull-request-event hosted run (36969627550) was in progress when read; its `suites` job will meet the same step.
- `scripts/verilator-capped` in this packet now defaults to `verilator` on PATH. The receipts were produced with it resolving to the pinned 5.050 build (`receipts/tool_identity.txt`).

## Pending manager duties

- After F1 is fixed: the full `aecp-dispatch-mutants` at the new head and the hosted `suites` job green there.
- The donor bank and the parent consumer set at milan-fpga dev `cdf49d1a`, with #137's `acmp_mutants.py` disposition line, using the gitlink at the new head. The author's parent set ran at `39fd019`, and its `xvlog_gate` pin line names `39fd0191`.
- The final current-dev candidate at the merge turn.
- Hosted and act acceptance.
- Carrying S1 and S2 at the manager's discretion.

## Prior public review findings on this PR

I wrote this section after the verdict, findings and ledger above. Before this review, PR #142 had no reviews and no inline comments. The two review-start notices carry no findings. The [A10] ruling on #141 (comment 5946147101) named two citation sites, 06 §6.4 (`06_aecp_engine.md:462`) and the E_SCLKS comment (`gen_ucode.py:1629-1638`). Both are **resolved** at this head: each now credits the membership test to IEEE 1722.1-2021 §7.2.32 and BAD_ARGUMENTS to Table 7-141, as L6 does. The one public review report on the PR is the internal reviewer's R430-1 (POSITIVE, issue comment 5946693777). It records two SUGGESTIONs and no other finding:

| Prior finding | Disposition at this head | Basis |
|---|---|---|
| R430 S1, SUGGESTION: the SET range check's compare width is not graded | **Retained as SUGGESTION**; I agree | A disposable probe made E_SCLKS's `CHECK_ARG` byte-wide (`FMT_B`). Section D3 still passes, 150 checks with 0 failures (`receipts/probe_sclks_byte_compare_d3.log`). D3C's indices 9 and 10 cannot tell a byte-wide compare from a 16-bit one. The frozen acceptance names 9 and 10 only, so the gap is outside #141's scope. An optional arm such as SET_CLOCK_SOURCE(0x0109) over the ten-source domain would close it |
| R430 S2, SUGGESTION: the D1 index numbers lack D1's own condition | **Retained as SUGGESTION**; the same as this report's S1 | Same evidence and fix as S1 above |

R430-1's POSITIVE rests partly on the author's evidence for the full dispatch campaign: R430 re-ran only the `d3` control and the two new arms. This review's F1 is new. It concerns the campaign arm `lk-prefix-zero-body`, which no earlier review ran at this head. F1 keeps this verdict NEGATIVE until it is fixed and re-measured as F1's "Required outcome" states.

R431-1 FINISHED

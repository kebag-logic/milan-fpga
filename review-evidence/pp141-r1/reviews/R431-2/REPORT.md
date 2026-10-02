[R431] POSITIVE - exact head a90ca735844a3e7a5bdfd2d1baeba24c95608992

# R431-2: independent external delta review of protocol-processor issue #141 / PR #142

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `a90ca735844a3e7a5bdfd2d1baeba24c95608992`, tree `877a0f78e3b6f15c1159899c10d7ba5e3ca3c836`. It is a `--no-ff` merge: first parent `76b09ff0` (round 2), second parent `2ebd4fe8` (`main`, PR #139, lane C6).
- Scope of this round:
  - round 2 (`76b09ff0`, assignment #141 comment 5947144104), which answers R431-1's MAJOR F1;
  - round 2b (`a90ca735`, the merge of `main` `2ebd4fe8`, assignment #141 comment 5950735422).
- How the scope was reconstructed: the repository's `README.md` and `docs/README.md` (the tree has no `AGENTS.md` or `CONTRIBUTING.md`), the issue's body and its assignment, ruling and round comments, and the PR body including its "Round 2" and "Round 2b" sections. Then the diff `2ebd4fe8..a90ca735` and its history, and `4a40b179..76b09ff0`. The public evidence at milan-fpga `d57953c0` `review-evidence/pp141-r1` holds only round 1's author packet (see "Real limits").
- Order of work: I made my own pass over the diff and wrote my findings first. Only then did I read the prior public reviews (R430-1, R431-1); their dispositions are in the last section.
- Toolchain: every build used the pinned Verilator 5.050 (`receipts/integrity/tool_identity.txt`). Every campaign ran in a clone of the exact head under the packet's scratch directory (the `tb/pp_top` campaigns each in a clone of their own); the review clone was never built in.

## Verdict

**POSITIVE.** R431-1 F1 is closed. The merge keeps both sides exactly, and the whole re-measure at the head agrees with every README record. I found no BLOCKER, MAJOR or MINOR. There is one RESIDUE, a wording issue in the PR body, and three SUGGESTIONs carried over from the earlier reviews.

1. **F1 is closed.**
   - The refreshed `lk-prefix-zero-body.patch` keeps byte-identical `-`/`+` lines (151; the two `sclks-*` patches 2 and 4).
   - The old patch planted at `39fd019` and the refreshed one planted at `76b09ff0` generate a byte-identical `ucode.hex` (98 changed words). The same holds for both `sclks-*` patches.
   - At the head, `git apply --check` accepts all 207 campaign patches; the old form of `lk-prefix-zero-body` is still refused there, as expected.
   - The dispatch campaign is rc 0: 4 controls PASS and **37 of 37 KILLED**, each count equal to its `tb/pp_top/README.md` row. That includes `lk-prefix-zero-body` 7, `sclks-bound-three` 11 and `sclks-bound-inclusive` 6.
   - Hosted `suites` at `76b09ff0` ran all of its steps and was green on both events (step 4 was skipped on a cache hit).
2. **The merge keeps both sides.**
   - My own `git merge --no-ff 2ebd4fe8` from `76b09ff0` gives tree `877a0f78`, the published tree. The merge base is `03c842a7`.
   - The patch-ids match: `03c842a7..76b09ff0` equals `2ebd4fe8..a90ca735` (`d6247794…`), and `03c842a7..2ebd4fe8` equals `76b09ff0..a90ca735` (`30d3367d…`).
   - The five `tb/pp_top` builds are numbered the same in every file I checked:

     | Number | Build | Section |
     |---:|---|---|
     | 1 | default | every section |
     | 2 | fixture | DV |
     | 3 | identify | ID |
     | 4 | line | AX |
     | 5 | timebase | TB |

     The files are the Makefile, `sim_main.cpp`, the README, 06, 08, 09, 00 and the drivers.
3. **The ROMs are regenerated and match main's.**
   - The head's `ucode.hex` is byte-identical to main's (`518b900c…`), and so is its program map: 89 programs, 1,107 words.
   - The head's ROM differs from the lane head's in exactly C6's 27 words, 464..469 and 480..500.
   - E_SCLKS holds 1184..1209 and its tail E_SCLKSRF holds 1144..1150. Neither overlaps C6's programs, and both are word-identical to the base's.
   - Each of the 22 `gen_ucode.py` campaign patches plants the same words with the same values at the merge as at `76b09ff0`, and none touches C6's words.
4. **The re-measure agrees.** Every campaign is rc 0, with every failing count equal to its README record:

   | Campaign | Result |
   |---|---|
   | dispatch | 37 |
   | D3 | 87 |
   | notify | 40 |
   | AECP | 55 |
   | ACMP | 19 |
   | GSI | 20 |
   | MAAP | 32 |
   | ADP | 32 |
   | SRP | 90 |
   | retry | 62 + 7 + 1 |
   | SRP admission | 12 |

   The sweep is 33 suites with **1,019,127 checks** and 0 failing. `tb/pp_top` has 9,168: 8,696 + 20 + 178 + 218 + 56.
5. **No port, parameter or RTL change beyond C6's.**
   - `hdl/` differs from `main` only in the E_SCLKS comment: 6+/5− lines, and no changed line outside a comment.
   - No file outside `docs/` and `tb/` differs from `main`, apart from that `gen_ucode.py` comment.

## Re-measured at the exact head

| Item | Result | Receipt |
|---|---|---|
| The reviewer's re-merge | `76b09ff0` + `git merge --no-ff 2ebd4fe8`: no conflict, tree `877a0f78…` = the published tree, an empty diff against `a90ca735` | `receipts/merge/remerge.log`, `receipts/merge/merge-check.txt` |
| Each side against the merge | patch-id of the lane side (`03c842a7..76b09ff0`) = (`2ebd4fe8..a90ca735`); of the main side (`03c842a7..2ebd4fe8`) = (`76b09ff0..a90ca735`) | `receipts/merge/merge-check.txt` |
| `hdl/` against `main` | only `hdl/aecp/ucode/gen_ucode.py:1658-1663`, a comment; the same hunk as the lane side's `hdl/` diff (equal sha256 after the index and hunk lines are dropped) | `receipts/merge/hdl-vs-main.txt` |
| ROMs at base, `39fd019`, `4a40b179`, `76b09ff0`, main and the head | see the four rows below | `receipts/rom/rom_probe.txt`, `rom_probe.json`, `sclks_words_base_vs_head.txt` |
| `ucode.hex` | the base and the lane heads give `3559d0a6…`; main and the head give `518b900c…` | the same |
| `ltn_rom.hex` | `23cc67ee…` at every revision | the same |
| `image.bin` | `20356f59…` at every revision | the same |
| ROM map, from the generator's own `placed`/`occupied` | the head's equals main's | the same |
| Patch refresh (`4a40b179..76b09ff0`) | `lk-prefix-zero-body`: two leading context lines of hunk `@@ -1427,31 +1417,25 @@` replaced one for one. Each `sclks-*` hunk header moved one line. The `-`/`+` bodies are sha-identical to `39fd019`'s | `receipts/rom/patch-refresh.txt`, the old forms in `receipts/rom/*.39fd019.patch`, `*.4a40b17.patch` |
| Planted defect identity | see the two rows below | `receipts/rom/rom_compare.txt` |
| The old and refreshed patches | old `lk-prefix-zero-body` at `39fd019` and the refreshed one at `76b09ff0`: the full `ucode.hex` is identical. The same holds for `sclks-bound-three` (word 1196) and `sclks-bound-inclusive` (word 1197). The old `lk` form is refused at `76b09ff0` and at the head | the same |
| The 22 `gen_ucode.py` patches | each plants the same words with the same values at the head as at `76b09ff0`; the 20 that exist on `main` plant the same at `main`; none touches 464..469 or 480..500 | the same |
| `git apply --check -v` of every committed patch | the head: 207 of 207 apply. `4a40b179`: 1 refused (`lk-prefix-zero-body`, F1's state). `76b09ff0`: 207 of 207. At the head, `sclks-*` apply at offset 25, and `lk-prefix-zero-body`'s hunks apply at offsets 9, 234 and 235 | `receipts/rom/rom_probe.json` (`apply_check`), `patch-refresh.txt` |
| `./scripts/run_suites.sh` (whole) | rc 0; the UPC map gate (61/89) and the M9 gate (30) pass; 33 suites, **1,019,127 checks, 0 failing**; `tb/pp_top` 9,168 (build tallies 8,696, 20, 178, 218, 56) | `receipts/campaigns/suites.log`, `pp_top_build_tally.txt` |
| `./scripts/lint_hdl.sh` | rc 0, 41 modules | `receipts/campaigns/lint_hdl.log` |
| `aecp_dispatch_mutants.py` (whole) | rc 0; controls `aecp-dispatch`, `aecp-line`, `d3`, `line-guards` PASS; **37 of 37 KILLED**; 37 of 37 counts equal the README | `receipts/campaigns/disp.log`, `disp.results.json`, `readme_compare.txt` |
| `aecp_mutants.py` (whole) | rc 0; 5 controls PASS; **55 of 55 KILLED**; 55 of 55 counts equal the README (`-talker` shorthand rows expanded) | `aecp.log`, `readme_compare.txt` |
| `d3_mutants.py --jobs 3` (whole) | rc 0; 3 goldens PASS; **87 of 87 KILLED**. The counts equal the README rows: 75 `tb/pp_top` (the four `clks_*` rows and the five raised rows included), 11 `tb/acmp_nvm` and the `tb/rx_validator` M4 row | `d3.log`, `d3.results.json`, `readme_compare.txt` |
| `notify_mutants.py --jobs 2` (whole) | rc 0; goldens PASS; **40 of 40 KILLED**; 40 of 40 counts equal the `tb/pp_top` record | `notify.log`, `notify.results.json`, `readme_compare.txt` |
| `acmp_mutants.py --jobs 2` (whole) | rc 0; 3 goldens PASS; **19 of 19 KILLED**. The counts equal the READMEs: 14 `tb/pp_top`; `tb/acmp_listener` 93, 50, 40 and 30; `tb/rx_validator` M6 27 | `acmp.log`, `acmp.results.json`, `readme_compare.txt` |
| `gsi_mutants.py`; `name_wr_mutant.py` | rc 0; 20 detected, golden and restored PASS; decode KILLED, golden and restored PASS | `gsi_name.log` |
| `tb/maap` `mutants.py` | rc 0; **32 of 32**; 29 of 29 "F FAIL of T" records equal (two `pp_top` legs at `tb/pp_top/README.md:1554,1564`) | `maap.log`, `maap_adp_readme_compare.txt` |
| `tb/adp_engine` `mutants.py` | rc 0; **32 of 32**; 30 of 30 counts equal | `adp.log`, `maap_adp_readme_compare.txt` |
| `tb/srp_top` `mutants.py` (whole) | rc 0; 11 controls PASS, 78 entries KILLED, assertion coverage 65/65: **90 checks, 90 PASS** | `srp.log` |
| `retry_mutants.py`; `srp_admission/mutants.py` | rc 0; 62 KILLED, 7 equivalence, 1 performance (70 of 70 rows equal); **12 of 12** | `retry_adm.log`, `retry_readme_compare.txt` |
| `desc_mem_guard/mutate.py` | rc 0; the hold-deleted mutant is detected | `dmg.log` |
| `make -C tb/nvm_port figures` | rc 0; all measured figures agree with the tree | `nvm_fig.log` |
| Docs and static gates | `make check` (41 mermaid, 18 wavedrom, 1,035 links, 115 REQ, 17 GAP, 94 rows 0 untested, 27 parameters); `check-links`, `check-matrix`, `check-integrator-params`, `render-wavedrom --check` and `make stale`, one by one; `gen_matrix --check`; `check_upc_map` (61/89); `check_m9_opcodes` with its selftest (9/9) and the gate (30); `git diff --check` against `2ebd4fe8`, `76b09ff0` and `03c842a7`. Every one is rc 0 | `receipts/static/docs-gates.txt` |
| PR body line references at the head | each holds:<br>`gen_ucode.py:1654-1663`, `:1662-1663`, `:1674-1711` (E_SCLKSRF at `:1703`), `:1688-1689`<br>`KL_aecp_engine.sv:1579`<br>`00:406`, `00:449`<br>`06:465`, `07:135`<br>`KL_aecp_dyn_state.sv:186`, `KL_aecp_nvm_writer.sv:502` | `receipts/static/line-refs.txt` |
| Hosted CI at the exact head (read-only) | push run 37034569811 and pull-request run 37034574936: `docs-gates` and `portability` completed with success. `suites` was in progress on both events when I last read it (17:48 UTC). Steps 5 (lint and every suite), 6 (SRP), 7 (MAAP), 8 (ADP) and 9 (AECP deadline and hazard) succeeded on both. Steps 10 (AECP dispatch) and 11 (traceability) succeeded on the pull-request event, and the rest were still running. At `76b09ff0`, runs 36997454013 and 36997457966 completed `suites` green, with steps 5 to 12 all executed. Step 4 was skipped there on a cache hit | `receipts/github/check-runs-*.json`, `jobs-*.json` |
| Resources | Peak memory of the review unit was 7.97 GB, under the 12 GB cap. At most 12 campaign jobs ran at once, and no Vivado run was made | this report |

## Findings

No BLOCKER, MAJOR or MINOR finding.

### RS1 - RESIDUE - Docs - the PR body's "the rest of the round-1 list stands"

- **Where:** PR #142 body, "Parent-visible list, round 2b", last bullet: "The rest of the round-1 list stands."
- **Evidence:**
  - The round-1 list includes "The processor RTL at this head is `main` `03c842a7`'s" and "The parent set above ran them with the gitlink at `39fd019`".
  - Read at `a90ca735`, both are stale. The RTL is `main` `2ebd4fe8`'s, apart from the `gen_ucode.py` comment (`receipts/merge/hdl-vs-main.txt`), and the round-2b parent set ran with the gitlink at `a90ca73`.
  - Both correct facts are already stated and measured in the same round-2b section (its first bullet, and "Parent consumer gates ... gitlink at `a90ca73`").
- **Why RESIDUE:** the problem is only how far the sentence's "this head" reaches. No measurement, figure, verdict, test, code, artifact, conformance or clause claim changes, and no privacy rule is touched.
- **Exact fix:** replace the bullet with "The rest of the round-1 list stands, read at the merge: the processor RTL is `main` `2ebd4fe8`'s apart from the `gen_ucode.py` comment, and the parent set above ran with the gitlink at `a90ca73`."
- **Verification:** a text check of the PR body.

### Suggestions (carried, still applicable at this head)

- **S1 (R430-1 S1) - SUGGESTION - Tests, Robustness:** the SET range check's compare width is not graded (`hdl/aecp/ucode/gen_ucode.py:1688-1689`, `FMT_W`). E_SCLKS and E_SCLKSRF are word-identical to the base's at the head (`receipts/rom/sclks_words_base_vs_head.txt`), so R430-1's probe result stands: a byte-wide compare passes section D3. An optional arm would close the gap: SET_CLOCK_SOURCE(0x0109) over the ten-source domain, answered BAD_ARGUMENTS, with the `FMT_B` edit as its control. This is outside #141's frozen acceptance.
- **S2 (R430-1 S2 = R431-1 S1) - SUGGESTION - Conformance, Docs:** `07_memory_maps.md:135` (L6) and `00_MILAN_COMPLIANCE_REVIEW.md:449` (REQ-MDL-005) give "INTERNAL 0, CRF 1, AAF input k at 2 + k" without D1's own condition, that both INTERNAL and CRF are declared. The lane's documentation diff is unchanged by rounds 2 and 2b (equal patch-id). The processor reads no order.
- **S3 (R431-1 S2) - SUGGESTION - Robustness, Tests:** `tb/pp_top/aecp_dispatch_mutants.py`'s `plant()` still raises on a refused patch instead of recording an UNPROVEN arm. The driver is unchanged by rounds 2 and 2b. At the head the patches apply by context at offsets: `sclks-*` at 25, and `lk-prefix-zero-body` at 9, 234 and 235. Every plant is word-identical, so this is not a defect. Refreshing the hunk headers at the merge would remove the offsets, and grading a refusal as UNPROVEN would keep a future refusal from aborting the run.

## Lens results

| Lens | Result | Artifact-specific evidence |
|---|---|---|
| Conformance | CLEAN | The rounds change no clause claim. The lane's L6, REQ-MDL-005, REQ-AEM-013 and 06 §6.4 hunks reach the merge byte-for-byte (equal patch-id). At the head they sit at `07:135`, `00:449`, `00:406` and `06:465`, with C6's 00/06/09 text beside them. The E_SCLKS comment at `gen_ucode.py:1658-1663` credits the membership test to IEEE 1722.1-2021 §7.2.32 and BAD_ARGUMENTS to Table 7-141. S2 is a suggestion only |
| RTL | CLEAN | `hdl/` against `main`: one comment hunk, and no non-comment line. No port, parameter or RTL change beyond C6's. Every ROM is regenerated: `ucode.hex` and its program map equal main's; E_SCLKS (1184..1209) and E_SCLKSRF (1144..1150) are disjoint from C6's 464..469 and 480..500 and word-identical to the base's. The lane-to-merge ROM delta is exactly C6's 27 words. The wrap carries both sides: `aecp_clk_src_index_o` connected, and `identify_button_i`, `EN_IDENTIFY_NOTIF_P` and the `dbg_ident_gap_*` taps |
| Robustness | CLEAN | F1's failure mode is closed: all 207 patches apply at the head, each of the 22 on `gen_ucode.py` plants the same words as at `76b09ff0`, and the old `lk` form is still refused (so the refresh was needed and suffices). The hosted dispatch step (10) passed at the head on the pull-request event. Every driver completed, each in a scratch clone. S1 and S3 are suggestions |
| Tests | CLEAN | Each campaign was re-run whole at the head and is rc 0, with every failing count equal to its README record: dispatch 37, D3 87, notify 40, AECP 55, ACMP 19, GSI 20, MAAP 32, ADP 32, SRP 90 (coverage 65/65), retry 62 + 7 + 1, SRP admission 12, `desc_mem_guard` detected, `nvm_port` figures. The sweep is 1,019,127 checks with 0 failing, and lint covers 41 modules. D3C runs in the default build's section D3 after D3R, beside C6's ID0, NP, ST and RN (`sim_main.cpp:10750`, `:13621`) |
| Docs | CLEAN | The build numbering is the same across the Makefile, the bench, the README, 06, 08, 09 and 00. The PR body's round-2 and round-2b figures and line references all hold at the head: patches 207 with 0 refused, offset 25, words 1196 and 1197, 61/89, 1,035 links, 27 parameters, 9,168 and 1,019,127. All docs gates are rc 0. RS1 is RESIDUE and leaves the lens clean |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `docs/architecture/07_memory_maps.md:135`; `docs/00_MILAN_COMPLIANCE_REVIEW.md:406,449`; `docs/architecture/06_aecp_engine.md:465`; `hdl/aecp/ucode/gen_ucode.py:1652-1711`; the lane-side and main-side patch-ids | R431-2 | `a90ca735844a3e7a5bdfd2d1baeba24c95608992` |
| RTL | CLEAN | `hdl/` diff against `2ebd4fe8` and `03c842a7`; ROMs and program maps at six revisions; `tb/pp_top/pp_top_wrap.sv` (both sides' ports and connections); the reviewer's re-merge | R431-2 | `a90ca735844a3e7a5bdfd2d1baeba24c95608992` |
| Robustness | CLEAN | `git apply --check -v` of all 207 patches at five revisions; plants of the 22 `gen_ucode.py` patches and of the old forms; `aecp_dispatch_mutants.py` `plant()`; hosted runs at `76b09ff0` and at the head | R431-2 | `a90ca735844a3e7a5bdfd2d1baeba24c95608992` |
| Tests | CLEAN | `run_suites.sh`; `lint_hdl.sh`; the dispatch, AECP, D3, notify, ACMP, GSI, name-write, MAAP, ADP, SRP, retry, SRP-admission and `desc_mem_guard` campaigns; `nvm_port figures`; README count comparison scripts | R431-2 | `a90ca735844a3e7a5bdfd2d1baeba24c95608992` |
| Docs | CLEAN (RS1 RESIDUE) | `tb/pp_top/README.md`, `Makefile`, `sim_main.cpp` header and `main()`; 06/08/09/00 build references; the PR body's round 2 and 2b sections and line references; docs gates | R431-2 | `a90ca735844a3e7a5bdfd2d1baeba24c95608992` |

## Real limits

- The public evidence named for this round, milan-fpga `d57953c0` `review-evidence/pp141-r1`, holds only `MANIFEST.json`, `author/HANDOFF.md` and `author/PR-BODY.md` (round 1). I found no `author-r2` or `author-r2b` directory there, so I took the round-2 and round-2b author claims from the PR body alone. The manager's source bank evidence that the brief refers to is not in that tree either. I did not rely on it: every figure above is my own measurement.
- The hosted `suites` job at the exact head was still in progress when I last read it: step 12 was pending on the pull-request event, and steps 10 to 12 on the push event. I record what had executed; acceptance of the hosted runs belongs to the manager.
- I did not script a comparison of SRP failing counts per label with the README, because the records are spread over round tables and re-measure prose. The campaign's own verdict (90/90, assertion coverage 65/65) and rc 0 stand. The SRP inputs are unchanged against `main` apart from the `gen_ucode.py` comment, which SRP does not read.
- A reviewer shim rewrote each Verilator `--build -j 0` to `-j 2`, so that campaigns could build concurrently inside the memory cap (`scripts/verilator-shim.sh`). It changes build parallelism only; the generated model is otherwise identical.
- One local invocation error was mine: `desc_mem_guard/mutate.py` was first started without `--output` (usage error). It was re-run correctly, rc 0 (`receipts/campaigns/lint_hdl.note`, `dmg.log`).
- I did not run `./syn/yosys/run.sh` (the Yosys bank is out of scope). Hosted `portability` passed at the exact head on both events.
- I ran nothing in the parent repository. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The IEEE 1722.1-2021 and Milan v1.2 texts are not distributed; this round changes no clause reading.
- The review clone ends at its exact head. HEAD and tree are exact, `git status --porcelain --ignored` is empty, and the index equals the HEAD tree in blobs and modes. The repository has no `.gitmodules` and no gitlinks, so there are no submodule pins to check (`receipts/integrity/clone_integrity.txt`).

## Pending manager duties

- Hosted and act acceptance at the exact head, including the completion of the `suites` job (step 12 on the pull-request event, steps 10 to 12 on the push event).
- The donor bank (9) and the parent consumer set (16, with `test_builder.py` whole) at milan-fpga dev `cdf49d1a`, with `parent-adoption-c4c6-ea3fb388.patch` and the gitlink at `a90ca735`. The author reports `test_builder.py` gate 12 (`test_baremetal_profile_contract`) as not completed in rounds 2 and 2b.
- The final current-dev candidate at the merge turn (source base `2ebd4fe8`, live dev `cdf49d1a`).
- Publishing the round-2 and round-2b author packets, if intended; they are not at `d57953c0`.
- RS1 to the residue checklist. S1 to S3 at the manager's discretion.

## Prior public review findings on this PR

I wrote this section after the verdict, findings and ledger above. I read the review-start notices and two reports: R430-1 (POSITIVE at `4a40b179`, issue comment 5946693777) and R431-1 (NEGATIVE at `4a40b179`, issue comment 5947143563). The PR has no formal reviews or inline comments.

| Prior finding | Disposition at this head | Basis |
|---|---|---|
| R431-1 F1, MAJOR: the dispatch campaign aborts (`lk-prefix-zero-body.patch` refused) | **Resolved** | The patch refresh in `76b09ff0` plants byte-identical defects (the old patch at `39fd019` and the new one at `76b09ff0` give the same `ucode.hex`). All 207 patches apply at the head, and the 22 on `gen_ucode.py` plant the same words as at `76b09ff0`. The whole dispatch campaign at the head: 4 controls PASS, 37 of 37 KILLED, every count equal to the README. The PR body's re-measure statement and `gen_ucode.py` references were corrected (round 2, item 3) and hold at the head. Hosted `suites` was green at `76b09ff0` with step 10 executed. F1's "preferably regenerate the `sclks-*` headers" was done at `76b09ff0`; at the merge they apply at offset 25 with identical plants (S3) |
| R431-1 S1 / R430-1 S2, SUGGESTION: the D1 order without its condition | **Retained as SUGGESTION** (S2 above) | The L6 and REQ-MDL-005 text is unchanged |
| R431-1 S2, SUGGESTION: a refused patch should be UNPROVEN, not abort | **Retained as SUGGESTION** (S3 above) | `plant()` is unchanged |
| R430-1 S1, SUGGESTION: the SET compare width is not graded | **Retained as SUGGESTION** (S1 above) | E_SCLKS is word-identical to the base's |
| The [A10] ruling (#141 comment 5946147101): two §7.4.23.1 citation sites | **Resolved** (as R431-1 found) | `06_aecp_engine.md:465` and `gen_ucode.py:1658-1663` credit §7.2.32 and Table 7-141 at the head |

R431-2 FINISHED

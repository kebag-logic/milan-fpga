[R442] POSITIVE - exact head af751a5aa9a809c982949cfb838a0de1fffc3e46

# R442-4 internal independent review: issue #79 / PR #147 (lane C7, counters), rounds 3 and 4

- **Head:** exact head `af751a5aa9a809c982949cfb838a0de1fffc3e46`, tree `71cd581ed0e0590cdeb7e3c1c5ed9629af3bed84`. Checked in the review clone after every probe (`receipts/clone_integrity.txt`).
- **Delta reviewed:**
  - Round 3: `81edaaa..9758a98`, commits `0bcf856` and `9758a98`. They change 7 files: three draw.io sources, their three SVG exports, and F01.5 in 01.
  - Round 4: `af751a5`, a `--no-ff` merge of main `ddb3119d` (PR #145, lane P2). Its parents are `9758a98` and `ddb3119d`.
  - I also re-read the whole PR diff at the new base, `ddb3119d..af751a5` (51 files, +1,452 / -287), to find anything the merge left inconsistent.
- **Authorities:**
  - #79's acceptance list, and the acceptance lists of #44 and #78.
  - The owner decision of 2026-09-19 (#79 comment 5740180166).
  - The lane assignment (5962255629) and the GPTP_GM_CHANGED ruling (5963704232).
  - The round-2, round-3 and round-4 assignments (5963890173, 5965236068, 5965782033).
  - The conventions in `docs/README.md` §2 and §3, and `docs/diagrams/README.md`.
  - The repository has no AGENTS.md or CONTRIBUTING.md.
  - The 02 §1 and §4.1 to §4.6 interface authority at this head.
- **Prior public findings:** read only after my own pass over the delta was complete. They are resolved below.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open. One RESIDUE and two SUGGESTIONs are new. Two earlier SUGGESTIONs stay open (R443-2-S1, and the F09.1 half of R443-2-S2), and neither affects the verdict.

### (1) R442-2 F1 and S1 are closed

**Label search.** I searched every figure source and render: all three draw.io sources (every cell label, and every edge with its endpoints), all 26 committed SVGs (8 in `docs/diagrams/`, 18 in `docs/diagrams/wavedrom/`), and every fenced Mermaid and WaveDrom block in every Markdown file. The search covered "counter", "adapter", "bank", "tick", "mask ROM", "B/C/D" and every removed op or event name (`READ_AS_PATH`, `AS_CAPABLE_CHANGE`, `PATH_CHANGE`, `INPUT_*`, `SET_*_FORMAT`, `OUTPUT_SET_PT_OFFSET`, `OUTPUT_STATUS`, `SET_CLOCK_SOURCE`, `GET_MCR_DEFAULTS`, `MC_LOCKED/UNLOCKED`, `gm_changed`). Output: `receipts/figure_label_search.txt`; script: `scripts/figure_label_search.py`.

- No figure draws an in-processor counter block, counter banks or a gPTP, AVTP or media-clock adapter, and no figure names a removed op.
- The remaining hits are all legitimate:
  - F01.1's "GET_COUNTERS reporting" and its `B/C/D` edge for srp/maap. 02 F02.9 gives srp B+C+D and maap B+C.
  - 02 F02.1's `ctr` node, "the integrator's counters".
  - 06's `ctrs` "ctr read face: the integrator's counters".
  - Prescaler ticks.
  - 23-bringup's own diagnostic drop counters.
  - F09.1's "mask ROMs", which is the pre-existing R443-2-S2 and is below.
- R442-2's own verification grep prints exactly the four labels the PR body names (`receipts/r442_2_grep_at_head.txt`). None of them is a counter block or an adapter.
- Against R442-2-F1's required outcome, item by item:

| R442-2-F1 required outcome | At this head |
|---|---|
| F01.2 has no "Counters subsystem" | Removed (cell `ctrs` gone, edge `e14` re-pointed) |
| F01.2's gPTP, AVTP and media-clock adapter boxes become the landed faces, with SRP/MAAP kept as class B | Group `faces` "External-engine faces (02 §4)" holds `f-srp` "srp · maap faces (class B)", `f-lvl` "gPTP · AVTP · media clock / class-D levels + change strobes" and `f-rd` "gsi · ctr read faces". A `words` edge runs `f-rd -> aecp`, matching 01's block table row `:92` and F01.3's `gsi / ctr read words` |
| F03.1 has no "counter banks" | Removed. The state-RAM complex holds image+overlay, dynamic state and registry, as 03's table row `:31` says |
| F03.1 relabels "adapter events" | `evsrc` "integrator strobes + level edges / SRP · MAAP · ADP engine events", the producers in 02 §5's catalog |
| F03.1's "to SMs / counters" becomes "to SMs / notifications" | Done (`d20`) |
| F01.1's "counters" becomes "GET_COUNTERS reporting" | Done |
| The PR body's Round 2 item 2 is corrected | The "Correction to Round 2, item 2" section |

**F01.1's edge tags match 02's landed faces.**
- gPTP `D · gsi · ctr` matches 02 §4.3: `gm_id_i` and `gptp_domain_i` class D, the `gsi` kind 1 and 2 words, and the AVB_INTERFACE counters on `ctr` at `:360`.
- AVTP `D · gsi · ctr` matches 02 §4.4: the binding and settings levels, the `gsi` kind 0 words, and the stream counters on `ctr` at `:395`.
- Media clock `D · ctr` matches 02 §4.5: the `aecp_clk_src_index_o` level, and LOCKED/UNLOCKED on `ctr` at `:405`.
- srp/maap `B/C/D` matches F02.9.
- The legend line, "gPTP, AVTP and media clocking have no class-B face", restates 02 §1 `:21-29`.

**Sources and renders agree. No SVG was edited by hand.**
- I re-exported each of the three figures from a clean clone at the head through the repository's own rule, `make docs/diagrams/<name>.svg` (draw.io CLI with its xvfb fallback).
- All three re-exports are byte-identical to the committed SVGs (`receipts/drawio_reexport.sha256`, three equal pairs).
- I rendered them to PNG and inspected them: no overlap, clipped label or edge through a box (`receipts/renders/*.png`).
- The draw.io "Text is not SVG - cannot display" fallback string is in the exports at `81edaaa` too. It is the exporter's standard switch fallback, not this round's.
- `make check` rc 0, `stale` included (`receipts/make_check.log`).

**R442-2-S1 is closed.**
- F01.5's P-N-STREAM-IN and P-N-STREAM-OUT rows now affect "counter-notification slots". The CLOCK_DOMAIN row no longer names counters. P-N-AVB-INTERFACES's seam note reads "counter-notification slots".
- This agrees with `KL_aecp_notify.sv:382-385`: `N_CTR_DESC_C = N_STREAM_IN_P + N_STREAM_OUT_P + 2`, one AVB_INTERFACE 0 slot and one CLOCK_DOMAIN 0 slot.

### (2) The merge keeps both sides of every shared file

I redid the merge in a scratch clone (`scripts/remerge_compare.sh`, `receipts/remerge_compare.txt`): `git merge --no-ff ddb3119d` from `9758a98`.

- **Conflicts.** Only `09_verification.md` conflicts.
- **Auto-merged files.** Git auto-merges 01, 02, 07, 08, `integrator.md` and `protocol_processor_top.sv`. Each of these, and every other file of the merge, is blob-identical to `af751a5`.
- **09 resolved mechanically.** Main's §8.6 goes first, then the lane's section renumbered "### 8.7 The counters face (issues #44, #79)". The result is byte-identical to the published 09.
- **One remaining difference from the head:** the GAP-05 "Verified by" cell in 00 (`:539`), which now cites `09 §8.7` / `#87-the-counters-face-issues-44-79`. That is the citation the assignment requires to move.
- **Main's side is kept.** For every file main changed, `diff(c74711d..ddb3119)` and `diff(9758a98..af751a5)` carry the same changed lines. The only extra is the renumbering.
- **The lane's side is kept.** For every file the PR changes, `diff(c74711d..9758a98)` and `diff(ddb3119..af751a5)` carry the same changed lines, apart from the 8.6 to 8.7 renumbering and its one citation. Both diffs are 51 files, +1,452 / -287.
- **Citations.**
  - No link to `#86-the-counters…` remains. The new anchor resolves (`make check` links: 1,105 OK).
  - Every remaining "§8.6" in the tree is P2's NVM section (09 `:215`, `:323`), parent D3 §8.6 (07 `:755`, `:797`; `KL_aecp_nvm_writer.sv:145`; `sim_main.cpp:11118`), Milan 5.3.8.6, 802.1Q 8.6.8.2, or the LICENSE.
- **The top.** P2's `NVM_MEM_TMO_CYC_P = CLK_HZ_P` (`:173`) is bound to the NVM port's `MEM_TIMEOUT_CYC_P` (`:2884`). Beside it are this lane's edits: the comment at `:382`, and the removal of `adp_gm_tick_nc_w` and `.gm_changed_tick_o`.
- **02, `integrator.md` and F01.5.**
  - 02 §8 carries P2's deadline text, and §4.6 still bounds the `ctr_*` face by `DESC_MEM_TMO_CYC_P`. They name different parameters, so they do not collide.
  - In `integrator.md`, the §7 tie-off table holds P2's NVM-device row and the lane's Counters row, and §7.1 (`counters-face`) is intact.
  - F01.5 holds the `P-NVM-MEM-TMO-CYC` row beside the round-3 cells. The `params` gate agrees: top 28, guide 28, diagram 28.

### (3) Re-measure

All runs used the pinned Verilator 5.050 (identity in `receipts/tool_identity.txt`) on `git archive` copies of the head.

| Run | Result | Receipt |
|---|---|---|
| `./scripts/run_suites.sh` | rc 0. 33 suites, **1,020,227** checks, 0 failing. `tb/pp_top` 9,196, `tb/adp_engine` 1,328, `tb/acmp_nvm` 388, `tb/nvm_port` 1,219. 1,067 s | `run_suites.log`, `.rc` |
| `./scripts/lint_hdl.sh` | rc 0 | `lint_hdl.log`, `.rc` |
| `make check` | rc 0. 41 mermaid + 18 wavedrom blocks, 1,105 links, 115 REQ rows, 17 GAP findings, 94 module rows with 0 untested, parameters 28/28/28, `stale` | `make_check.log` |
| `git apply --check`, every `tb/**/*.patch` | **224 of 224**: adp_engine 28, maap 27, pp_top aecp_dispatch 37, ctr 17, mutations 42, srp_top 73 | `apply_check.txt` |
| `git diff --check` against `c74711d4`, `9758a98` and `ddb3119d` | rc 0 for each | `diff_check.txt` |
| `ctr_mutants.py --jobs 4` | rc 0. Control PASS, **17 of 17 KILLED**, every arm's failing-check count equal to the README table. The log is byte-identical to the author's record (sha256 `0fd23cc6151456be…`) | `ctr_mutants.log`, `ctr_mutants.readme_compare.txt` |
| `aecp_mutants.py --jobs 4` | rc 0. 5 controls PASS, 55 of 55 KILLED, counts equal to the README | `aecp_mutants.*` |
| `aecp_dispatch_mutants.py --jobs 2` | rc 0. 4 controls PASS, 37 of 37 KILLED, counts equal to the README | `aecp_dispatch_mutants.*` |
| `d3_mutants.py --jobs 4` | rc 0. 3 goldens PASS, 87 of 87 KILLED. The 75 `tb/pp_top` rows match the README counts | `d3_mutants.*` |
| `notify_mutants.py --jobs 2` | rc 0. 5 goldens PASS, 40 of 40 KILLED, counts equal to the README | `notify_mutants.*` |
| `acmp_mutants.py --jobs 2` | rc 0. 3 goldens PASS, 19 of 19 KILLED. The 14 pp_top rows match the README. The `acmp_listener` arms give 93, 50, 40 and 30 and `rx_validator`'s gives 27, all equal to those suites' READMEs | `acmp_mutants.*` |
| `gsi_mutants.py --jobs 4` | rc 0. Golden, 20 variants detected by their named checks, restored PASS, as the README records | `gsi_mutants.log` |
| `name_wr_mutant.py` | rc 0. Decode killed, golden and restored PASS | `name_wr_mutant.log` |

Each campaign took (`receipts/campaign_times.txt`): aecp 442 s, dispatch 545 s, d3 1,779 s, notify 590 s, acmp 225 s, gsi 375 s, name_wr 44 s. The count comparisons are scripted (`scripts/compare_readme_counts.py`, `scripts/compare_json_campaign.py`).

### (4) RTL and the out-of-context note

- **Changed files.** `git diff ddb3119d af751a5 -- hdl` touches three files: `KL_pp_acmp_listener.sv`, `KL_adp_engine.sv` and `protocol_processor_top.sv`.
- **Preprocessed comparison.** I ran each file at both revisions through the pinned simulator's preprocessor (`-E -P`, comments stripped) and compared (`receipts/rtl_preprocessed_delta.txt`):
  - `KL_pp_acmp_listener.sv`: no logic change.
  - `KL_adp_engine.sv`: exactly five removed lines, `gm_changed_tick_o`, `gm_tick_r`, its reset, its update and the assign.
  - `protocol_processor_top.sv`: exactly two removed lines, `adp_gm_tick_nc_w` and `.gm_changed_tick_o(...)`.
  - **The lane's RTL change at the new base is exactly the GM-tick removal.** No port, parameter or register of the top changes.
- **The -43 LUT / -81 FF note is plausible.** A one-flop, port-less removal can move synthesis mapping in modules it does not touch. The author's split control is an independent check: the logic half reproduces the head and the comment half reproduces the base. I did not re-run Vivado (see limits).

## Findings

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R442-4-R1 | RESIDUE | Docs | `docs/architecture/03_packet_engine.md:18` (the note under F03.1) | The note says "This export **predates** the move of the descriptor image…". Round 3 re-exported F03.1 on 2026-10-03 (`0bcf856`; my re-export is byte-identical), so the export no longer predates the move. What is still true is that the drawing keeps the image on chip. Only the prose wording is wrong. The figure, the component table and every claim stay as they are | A reader may think the export is stale, which `make stale` disproves | Replace "This export **predates** the move of the descriptor image and the AECP response buffer into the integrator's main memory, so its" with "This drawing was **not redrawn** for the move of the descriptor image and the AECP response buffer into the integrator's main memory, so its". The rest of the note stays | Read `03:18`; `make check` rc 0 |
| R442-4-S1 | SUGGESTION | RTL, Docs | `syn/ooc/README.md:218-238` | The in-tree record of the GM-tick removal is pinned to base `88969246` (0 / 0). At the merge base `ddb3119d` the author measured -43 LUT / -81 FF, from mapping changes in modules the change does not touch. That figure lives only in the PR body's Round 4 | None at this head: the record is dated, base-pinned and true. A later reader of the tree does not see the new-base figure | Optional: at the merge turn, add one paragraph with the `ddb3119d` / `af751a5` measurement and the split control | Doc review |
| R442-4-S2 | SUGGESTION | Docs, Conformance | `docs/00_MILAN_COMPLIANCE_REVIEW.md:366` (REQ-ADP-009, mechanism "GPTP adapter event") | Pre-existing (2026-08-11) and outside every acceptance item and assignment of this lane. #78 acceptance 1 binds 02 §4.3 to §4.5 and §5. Round 2 bound 01, 05 and 06, and round 3 bound the figures. The author records it under "What remains". The landed mechanism is the `gm_change_i` strobe (02 §4.3, §5). The row's requirement, coverage and verdict are unaffected | The compliance matrix names an adapter that 02 says does not exist | Optional, in a docs pass: "`gm_change_i` strobe ([02 §4.3](architecture/02_interfaces.md))" | `make check` links |

### Prior public findings at this head

| Finding | Original severity | Status at `af751a5` | Evidence |
|---|---|---|---|
| R442-2-F1: F01.2 and F03.1 (and F01.1) draw an in-processor counter block and the removed adapters | MINOR | **CLOSED** | §(1) above: every required item; label search over every source and render; re-exports byte-identical; `make check` rc 0 |
| R442-2-S1: F01.5 "counters" | SUGGESTION, taken | **CLOSED** | §(1); `KL_aecp_notify.sv:382-385` |
| R442-1-F1, R442-1-F2, R442-1-S1, R442-1-S2 | MINOR, MINOR, SUGGESTION, SUGGESTION | **CLOSED, and they stay closed** | R442-2 and R443-2 recorded them closed at `81edaaa`. Round 3 touches only the three figures and F01.5. The merge adds only main's lines and the 8.6 to 8.7 renumbering (§2), so none of the closed locations moved. K9 to K17 and the ctr campaign re-ran green with the recorded counts |
| R443-1-F1 to F6 and the `.gitattributes` addendum | MINOR, SUGGESTION x3, RESIDUE x2, assignment item | **CLOSED, and they stay closed** | As above. `git diff --check` against `c74711d4` gives rc 0 |
| R443-2-S1: the GPTP_GM_CHANGED rule's zero-identity corner (`integrator.md:486-498` against the parent's nonzero-prior edge) | SUGGESTION | **OPEN, retained as SUGGESTION** | Not taken by any assignment; the text is unchanged. Neither standard defines the A → 0 → B case |
| R443-2-S2: F09.1 "mask ROMs", and F01.5 "counters" | SUGGESTION | **F01.5 half CLOSED** (round 3). **The F09.1 half is OPEN, retained as SUGGESTION** | `09_verification.md:11` still reads "dispatch / response-size / transition / mask ROMs". It is a Mermaid node of the generated-environment concept, it does not name a counter block, and 07 says no mask ROM is stored |

## Lenses

- **Conformance: CLEAN.**
  - #79 acceptance 1, 3 and 4 still hold at the merged head: the GAP-05 decision in 00 §7, the `ctr_*` contract in `integrator.md` §7.1 with REQ pointers, F07.10 corrected, and 06 §6.6 naming the landed push. Item 2 is the processor-owned option and does not apply.
  - #44 acceptance 1 to 3 still hold: the tick is removed, K9 to K11 run byte-exact at offsets 0, 4 and 20, and the ctr campaign kills both store arms.
  - #78 acceptance 1 and 2 still hold in 02, and F01.1's tags now agree with them. Acceptance 3 and 4 were met on main by #133.
  - Rounds 3 and 4 add no clause claim. The only new citation is 00's link to 09 §8.7, which resolves.
- **RTL: CLEAN.**
  - Preprocessed delta at the new base: exactly the GM-tick removal, plus comments.
  - P2's parameter and binding are intact. `lint_hdl.sh` gives rc 0. The suites and every pp_top campaign build the merged top.
- **Robustness: CLEAN.**
  - The merge leaves the face's safety properties untouched: the `ctr_wait_i` hold polarity, the `DESC_MEM_TMO_CYC_P` watchdog, and a tied-off `ctr_change_i` that sends no push.
  - P2's deadline machinery is graded green beside them: `tb/nvm_port` 1,219, `tb/acmp_nvm` 388, and the d3 campaign 87 of 87.
  - Two shared-file risks were checked. 02's §4.6 and §8 cite different watchdogs. `integrator.md`'s tie-off rows keep both.
- **Tests: CLEAN.**
  - 1,020,227 checks across 33 suites, 0 failing.
  - Every pp_top campaign re-run, with verdicts and per-arm counts equal to the READMEs: ctr 17, aecp 55, dispatch 37, d3 87, notify 40, acmp 19, gsi 20, name_wr 1.
  - 224 of 224 campaign patches apply. `git diff --check` gives rc 0 three ways.
- **Docs: CLEAN.**
  - The figures were redrawn from their sources, and the exports are reproducible byte for byte.
  - The label search over every figure is clean.
  - 09's renumbering and its one citation are right. `make check` gives rc 0.
  - One wording RESIDUE (R1) and two SUGGESTIONs, none of which makes a lens unclean.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #79, #44 and #78 acceptance; owner decision and ruling; 02 §1, §4.3 to §4.6, F02.9, F02.10; 00 GAP-04, GAP-05 and REQ-ADP-009; F01.1 edge tags; 09 §8.7 and its citation | R442-4 (rounds 3 and 4) | `af751a5aa9a809c982949cfb838a0de1fffc3e46` |
| RTL | CLEAN | `git diff ddb3119d..af751a5 -- hdl` (3 files); preprocessed delta; P2's `NVM_MEM_TMO_CYC_P` binding; `KL_aecp_notify.sv:382-385`; `lint_hdl.sh` | R442-4 | `af751a5aa9a809c982949cfb838a0de1fffc3e46` |
| Robustness | CLEAN | Watchdogs and tie-offs in 02 §4 (read faces), §4.6, §8 and `integrator.md` §7/§7.1; `tb/nvm_port`, `tb/acmp_nvm`, d3 and ctr campaigns | R442-4 | `af751a5aa9a809c982949cfb838a0de1fffc3e46` |
| Tests | CLEAN | `run_suites.sh` (33 suites); 8 pp_top campaigns against their README records; 224 patch apply-checks; `git diff --check` x3 | R442-4 | `af751a5aa9a809c982949cfb838a0de1fffc3e46` |
| Docs | CLEAN (R1 RESIDUE carried) | 3 draw.io sources and exports (re-exported, rendered, inspected); all 26 SVGs; every Mermaid and WaveDrom block; F01.5; 09 merge; `make check` | R442-4 | `af751a5aa9a809c982949cfb838a0de1fffc3e46` |

## Real limits

- **Out-of-context synthesis not re-run.** I did not run Vivado, so the -43 LUT / -81 FF figures and the author's split control are not independently reproduced. I verified only that the RTL change being measured is exactly the GM-tick removal. `./syn/yosys/run.sh` was not run either.
- **Some campaigns not run.** Outside `tb/pp_top`: the hdl workflow's `srp_top`, `maap` and `adp_engine` campaigns, and `tb/srp_admission`, the `tb/acmp_talker` retry and `tb/desc_store` lint-suppression. Their patches all apply at the head, and the merge changed none of their inputs.
- **d3 counts outside `tb/pp_top`.** For d3's 12 arms run in `tb/acmp_nvm` and `tb/rx_validator`, I checked the verdict only (KILLED), not the counts in those suites' READMEs.
- **Campaign concurrency.** The campaigns ran at `--jobs` 2 or 4, not at both 1 and 8. The ctr record's byte identity with the author's `--jobs 8` and `--jobs 5` records stands in for that.
- **Specifications not re-read.** I did not re-open the printed IEEE 1722.1-2021 or Milan v1.2 for this delta. Rounds 3 and 4 add no clause claim, and the clause checks of the counters contract are R442-2's and R443-2's at `81edaaa`, unchanged since.
- **Hosted evidence.** At the time of reading, the exact-head hosted runs were `docs-gates` x2 success, `portability` x2 success, and `suites` x2 still in progress (`receipts/hosted_check_runs.txt`). I found no manager evidence comment for this head on #79 or #147. The public evidence tree `kebag-logic/milan-fpga@c0212c4d:review-evidence/ppC7-r1` holds the round-1 author archive only.
- **Hardware and field skips.** No hardware was used, and physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- The donor bank (9) and the parent consumer set (16) at milan-fpga dev `1269cdaf`, with `parent-adoption-c8-cdf49d1a.patch` and then `parent-adoption-p2-cdf49d1a.patch`.
- Hosted and act acceptance at the exact head, including the two `suites` runs that were in progress.
- The final current-dev candidate at the merge turn: source base `ddb3119dbbce59f81bf7a536a1ad90a20546edb2`, live dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- Carry R442-4-R1 to the residue checklist with its exact text. S1 and S2, and the retained R443-2-S1 and R443-2-S2 (F09.1), are optional.
- Merge requires the second independent review as well.

## Packet

- `scripts/`: `run_campaigns.sh`, `compare_readme_counts.py`, `compare_json_campaign.py`, `figure_label_search.py`, `remerge_compare.sh`.
- `receipts/`: logs, rc files and comparisons, all listed in `MANIFEST.sha256`.
- `scratch/` is not published.

R442-4 FINISHED

[R443] POSITIVE - exact head af751a5aa9a809c982949cfb838a0de1fffc3e46

# R443-4: external independent review of processor PR #147 (lane C7, counters), delta for rounds 3 and 4

- Exact head `af751a5aa9a809c982949cfb838a0de1fffc3e46`, tree `71cd581ed0e0590cdeb7e3c1c5ed9629af3bed84`. Parents: `9758a98` (round 3) and `ddb3119` (main, PR #145, lane P2).
- Scope:
  - round 3 (`0bcf856`, `9758a98`; assignment #79 comment 5965236068): F01.1, F01.2 and F03.1 redrawn, and F01.5's cells;
  - round 4 (`af751a5`; assignment #79 comment 5965782033): a `--no-ff` merge of main `ddb3119d`.
- Reconstruction order:
  1. Contributor guides. The tree has no AGENTS.md or CONTRIBUTING.md; `docs/README.md` and `docs/diagrams/README.md` hold the author conventions.
  2. Issue #79: its body and every manager comment, including the owner decision of 2026-09-19, the GPTP_GM_CHANGED ruling and the round 2 to 4 assignments.
  3. #78's acceptance, 02 §1 and §4 to §6, and 01, 03 and 09.
  4. `git diff ddb3119..af751a5` and the history.
  5. The public evidence at milan-fpga `c0212c4d` (`review-evidence/ppC7-r1`).
  6. The PR body.
- I read the prior public review findings only after my own pass over the diff.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open. All five lenses are clean.

- **R442-2 F1 is closed.**
  - Each figure is regenerated from its draw.io source. My own export through the repository's draw.io CLI under `xvfb-run` is byte-identical to each committed SVG, so no SVG was hand-edited.
  - My label search over every draw.io source, every committed SVG (draw.io exports, the five hand-authored figures and the wavedrom renders) and every Mermaid fence finds no removed op, no adapter and no in-processor counter block.
  - The same search catches every old label at `81edaaa` (positive control).
  - F01.1's edge tags match 02's landed faces.
- **R442-2 S1 is closed.** F01.5's cells match `KL_aecp_notify.sv:382-385`.
- **The merge keeps both sides.**
  - I redid the merge myself (`9758a98` + `ddb3119`, `--no-ff`). Only 09 conflicted. I resolved it as assigned: P2's §8.6 first, the counters section as §8.7, and the one GAP-05 citation moved. The result is the head's tree exactly (`71cd581…`).
  - For each of the seven shared files, the changed-line sets on each side are kept unchanged; the only addition is the §8.6 → §8.7 renumbering.
- **The re-measure reproduces.**
  - `run_suites.sh`: rc 0, 33 suites, **1,020,227** checks, 0 failing.
  - Every campaign patch applies: 224 of 224.
  - The ctr campaign: control PASS, **17 of 17 KILLED**. Its printed record is byte-identical to the author's (sha256 `0fd23cc6…`, 11,104 bytes), and every arm's per-check failures agree with the `tb/pp_top` README.
  - Every other `tb/pp_top` campaign was re-run and matches its README record: aecp, aecp_dispatch, notify, acmp, d3, gsi and name_wr. So does the adp_engine unit campaign.
- **The lane's own RTL change on the new base is exactly the GM-tick removal.**
  - After comment stripping (`verilator -E -P`), only two files differ from `ddb3119`: `KL_adp_engine.sv` loses `gm_changed_tick_o`, `gm_tick_r` and its two assignments; the top loses `adp_gm_tick_nc_w` and its connection.
  - The `hdl/` patch-id is identical at both bases (`e368d122…`).
  - The -43 LUT / -81 FF out-of-context delta therefore comes from no other logic change. I did not run synthesis (see limits).

New items: three SUGGESTIONs and one RESIDUE. Retained from earlier rounds: two SUGGESTIONs (one narrowed). None affects the verdict.

## Findings of this round

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R443-4-S1 | SUGGESTION | Docs, RTL | `docs/diagrams/src/03-shared-datapath.drawio:72` (box `evsrc`, "integrator strobes + level edges · SRP · MAAP · ADP engine events" → event router, `:117`); `docs/diagrams/src/01-top-level.drawio:150` (`e22`: the whole faces group "events" → event router) | The router's sources at the top are the SRP Talker-attribute events, the ADP discovered/departed events, the SRP domain change, the listener-registration changes, `gm_change_i` and the `link_up_i` edges (`hdl/top/protocol_processor_top.sv:3143-3164`). The MAAP conflict pair goes to the talker (`:2268`). `gsi_avb_chg_i`, `gsi_asp_chg_i` and `ctr_change_i` go to the notifier directly. 02 §5 says which events are routed and which are "wired directly and NOT routed". The previous box also listed maap, and this relabel follows R442-2's required wording | A reader of F03.1 may think the MAAP conflict and every integrator strobe pass through the router. Nothing removed is named, and 03 §5 points to 02 §5's catalog | Optional: drop "MAAP" from the router's source box, or add "(02 §5: the routed subset)" | Re-export, then `make check` |
| R443-4-S2 | SUGGESTION | RTL, Docs | `syn/ooc/README.md:218-239` (the issue #44 record, base `88969246`) | The round-4 OOC re-measure on base `ddb3119` (-43 LUT, -81 FF, `u_adp` unchanged) appears only in the PR body. The README keeps round 1's 0/0, with its own base named, so it is not false | A later reader of `syn/ooc` does not see the new-base delta or its explanation (mapping changes in untouched modules) | Optional: append the round-4 table and the split-half reproduction to the README section | Read the section |
| R443-4-S3 | SUGGESTION | Tests | `.github/workflows/hdl.yml` (`suites` job: srp_top, maap, adp_engine, aecp-mutants and aecp-dispatch-mutants only) | The ctr campaign (`make -C tb/pp_top ctr-mutants`, 17 arms) gates the lane's checks K9 to K17 but runs only by hand. Here it took 2 min 43 s at `--jobs 3` | A later change that silences K9 to K17 is not caught by hosted CI | Optional: add a `ctr-mutants` step beside the aecp campaigns | The hosted job log names the step and shows 17 of 17 |
| R443-4-R1 | RESIDUE | Docs | `docs/00_MILAN_COMPLIANCE_REVIEW.md:366` (REQ-ADP-009, mechanism cell "GPTP adapter event") | 02 §4.3 and §5 at this head: GM_CHANGE is the integrator's `gm_change_i` strobe, and there is no gPTP adapter. The author discloses this cell under "What remains (round 4)". It is outside the round-3 and round-4 assignments and outside #78's acceptance, which covers 02 only. The requirement, its verdict (DIR) and its clause are unchanged, so this is wording only | One table cell still names a removed adapter in prose | Exact fix: replace `GPTP adapter event` with ``the `gm_change_i` strobe ([02 §4.3](architecture/02_interfaces.md))`` | `grep -rn 'GPTP adapter' docs` prints nothing; `make check` (links) rc 0 |

## Prior public findings at this head

| Finding | Severity | Status at af751a5 | Evidence |
|---|---|---|---|
| R442-2-F1: F01.2 and F03.1 (and F01.1) draw a counter block, counter banks and the gPTP/AVTP/media-clock adapters | MINOR | **CLOSED** | See the bullets below this table |
| R442-2-S1: F01.5 "Affects" cells list "counters" | SUGGESTION | **CLOSED** | `01_overview.md:154-156` reads "counter-notification slots" for P-N-AVB-INTERFACES (seam note), P-N-STREAM-IN and P-N-STREAM-OUT. The CLOCK_DOMAIN row drops "counters". This matches `KL_aecp_notify.sv:382-385`: `N_STREAM_IN_P + N_STREAM_OUT_P + 2` slots, with AVB_INTERFACE and CLOCK_DOMAIN index 0 only (`:491-508`) |
| R443-2-S1: the zero-identity case of the GPTP_GM_CHANGED rule | SUGGESTION | **RETAINED** (not taken; the assignment did not take it) | `integrator.md:487-499` is unchanged |
| R443-2-S2: F09.1 "mask ROMs"; F01.5 "counters" | SUGGESTION | **F01.5 part CLOSED** (as R442-2-S1). **F09.1 part RETAINED** | `09_verification.md:11` still reads "dispatch / response-size / transition / mask ROMs" (`receipts/figure_label_search_head.txt`) |
| R442-1-F1, R442-1-F2, R443-1-F1 | MINOR | **still CLOSED** (closed at round 2; checked again after the merge) | R443-1's grep finds nothing (rc 1). The identity-comparison rule is at `integrator.md:487-499`. Nothing in 01, 05 or 06 names a removed op (`receipts/prior_findings_recheck.txt`) |
| R442-1-S1, R442-1-S2, R443-1-F2 to F4 | SUGGESTION | **still CLOSED** | K17 is present; `ctr_mutants.py --jobs` is used here; the STREAM_INPUT quadlet 6 and 7 rows are at `integrator.md:457`, `:471` |
| R443-1-F5, F6 | RESIDUE | **still CLOSED** (exact text, one occurrence each) | `receipts/prior_findings_recheck.txt` |

Evidence for closing R442-2-F1:
- **Sources** (`0bcf856`):
  - `01-top-level.drawio` has no `ctrs` cell. The "External-engine faces (02 §4)" group (`:80`) holds three faces: "srp · maap faces (class B)" (`:83`), "gPTP · AVTP · media clock class-D levels + change strobes" (`:86`) and "gsi · ctr read faces" (`:89`). A `words` edge runs from the read faces into AECP (`:129`).
  - `03-shared-datapath.drawio` has no `ram4` store; it has `evsrc` (`:72`) and "to SMs / notifications" (`:118`).
  - `01-system-context.drawio:25` reads "GET_COUNTERS reporting".
- **Renders:** re-exported, all three byte-identical to the commits (`receipts/drawio_reexport.txt`).
- **Label search:** clean at the head, while the control at `81edaaa` catches all ten old labels (`receipts/figure_label_search_*.txt`).
- **Visual check:** rendered to PNG and inspected. No overlap, no clipped text, no edge through a box. The "Text is not SVG" footer is draw.io's standard fallback and is present at the base too.
- **PR body:** Round 2 item 2 is corrected (sections "Corrected in Round 3" and "Correction to Round 2, item 2").

## Focus items

1. **R442-2 F1 and S1: closed** (above).
   - F01.1's edge tags against 02:
     - gPTP `D · gsi · ctr`: §4.3 has the levels and strobes, the `gsi` kinds 1 and 2, and LINK_UP, LINK_DOWN and GPTP_GM_CHANGED on `ctr`.
     - AVTP `D · gsi · ctr`: §4.4 has the output levels, `gsi` kind 0, and the stream counters on `ctr`.
     - Media clock `D · ctr`: §4.5 has `aecp_clk_src_index_o` and LOCKED/UNLOCKED on `ctr`; it has no `gsi` word.
     - srp/maap keeps `B/C/D`, matching F02.9's `B+C+D` and `B+C`.
     - The legend line matches 02 §1.
   - F01.2's "SRP engine (10, default), MAAP engine (11, opt-in)" matches 02 §4.1 (`P-EN-SRP-ENGINE`, the F01.5 default) and §4.2 (`cfg_maap_internal_i` = 0 by default).
2. **The merge.**
   - Re-done independently. The tree is identical, and both sides are kept in every shared file (`receipts/merge_sides_check.txt`; `scripts/merge_sides_check.sh`). The patch-ids agree for 01, 02, 07, 08 and the top. For `integrator.md` and 09 the sorted changed-line sets agree, except 09's one renumbered heading.
   - 09: P2's §8.6 is at `:323`, the counters §8.7 at `:352`, and P2's back-reference at `:215`.
   - The GAP-05 citation is moved (`00:539`, `#87-the-counters-face-issues-44-79`); no other citation of either anchor exists.
   - The top keeps P2's `NVM_MEM_TMO_CYC_P` (`:173`, bound at `:2884`) beside this lane's removals.
   - 02 §8 keeps DEADLINE (`:594`, `:603-618`) beside §4.6. The guide's `NVM_MEM_TMO_CYC_P` row (`:99`) and its NVM-device tie-off row (`:387`) sit beside the Counters row (`:389`). F01.5 `P-NVM-MEM-TMO-CYC` is at `:181`.
   - No sentence P2 retired survives.
   - `git diff --check` is rc 0 against `ddb3119`, `9758a98` and `81edaaa`.
   - `git diff ddb3119 af751a5` is 51 files, +1,452 / -287, the same as `c74711d..9758a98`.
3. **The re-measure:** all reproduced. The table below lists every run.
4. **The OOC note.**
   - The lane's RTL at the new base is exactly the tick removal: comment-stripped preprocessing differs from `ddb3119` in two files only (`receipts/rtl_preproc_diff.txt`).
   - The tick was a flop with no load at the base, so a netlist delta outside `u_adp` is a synthesis-path effect, not a logic change. The PR body records `u_adp` as unchanged (865 / 507).
   - I did not reproduce the -43 / -81 figures.

## Executed evidence (exact head; pinned simulator 5.050, `receipts/verilator_version.txt`; each campaign in its own `git archive` copy, scratch under the packet)

| Command | Result | Receipt |
|---|---|---|
| `scripts/run_suites.sh` | rc 0. UPC map, M9 self-test and M9 gates PASS. 33 suites, **1,020,227 checks**, 0 failing. Per suite: `pp_top` 9,196, `adp_engine` 1,328, `acmp_nvm` 388, `nvm_port` 1,219 | `receipts/run_suites.log`, `.rc` |
| `scripts/lint_hdl.sh` | rc 0, 41 of 41 LINT OK | `receipts/lint_hdl.log`, `.rc` |
| `make check` (separate clone at the head) | rc 0: 41 mermaid + 18 wavedrom blocks, 1,105 links, 115 REQ rows, 17 GAP findings, 94 module rows with 0 untested, parameters top/guide/diagram 28/28/28; `stale` passes | `receipts/make_check.log`, `.rc` |
| `make stale` negative control | rc 0 at the head. rc 2 after an uncommitted edit to `01-top-level.drawio` ("uncommitted source edit newer than the export"). rc 0 after reverting it | `receipts/make_stale_negative_control.txt` |
| draw.io re-export of all three sources, then `cmp` | 3 of 3 byte-identical to the committed SVGs | `receipts/drawio_reexport.txt` |
| label search, head and the `81edaaa` control | head: no removed op, adapter or counter block. Remaining hits: "GET_COUNTERS reporting", figure 23's own saturating debug counters, and F09.1's "mask ROMs". Control: all ten old labels found | `scripts/figure_label_search.sh`, `receipts/figure_label_search_head.txt`, `receipts/figure_label_search_81edaaa_control.txt` |
| independent re-merge | tree `71cd581…` == head | `receipts/merge_sides_check.txt` |
| `git apply --check`, every `tb/**/*.patch` | 224 of 224 | `receipts/campaign_patch_apply_check.txt` |
| `ctr_mutants.py --jobs 3` | rc 0: control PASS, 17 of 17 KILLED. Record sha256 `0fd23cc6…`, 11,104 bytes, identical to the author's. 17 of 17 arms agree with the README, per check | `receipts/ctr_mutants.log`, `receipts/ctr_record_vs_readme.txt` |
| `aecp_mutants.py --jobs 3` | rc 0: 5 controls PASS, 55 of 55 KILLED, each arm's count = README | `receipts/aecp_mutants.log`, `receipts/aecp_vs_readme.txt` |
| `aecp_dispatch_mutants.py --jobs 3` | rc 0: 4 controls PASS, 37 of 37 KILLED, each = README | `receipts/aecp_dispatch_mutants.log`, `receipts/aecp_dispatch_vs_readme.txt` |
| `notify_mutants.py --jobs 3` | rc 0: goldens PASS, 40 of 40 KILLED, each arm's failing-check count = README | `receipts/notify_mutants.log`, `receipts/notify_vs_readme.txt` |
| `acmp_mutants.py --jobs 3` | rc 0: 3 goldens PASS, 19 of 19 KILLED; the 14 `pp_top` arms = README "N of 43" | `receipts/acmp_mutants.log`, `receipts/acmp_vs_readme.txt` |
| `d3_mutants.py --jobs 3` | rc 0: goldens `acmp_nvm`, `pp_top` and `rx_validator` PASS; 87 of 87 KILLED, every named check failing | `receipts/d3_mutants.log` |
| `gsi_mutants.py --jobs 3` | rc 0: golden PASS, 20 variants detected, restored PASS | `receipts/gsi_mutants.log` |
| `name_wr_mutant.py` | rc 0: decode killed; golden and restored PASS | `receipts/name_wr_mutant.log` |
| `tb/adp_engine/mutants.py --jobs 4` | rc 0: 2 controls PASS, 30 of 30 KILLED, each = README | `receipts/adp_engine_mutants.log`, `receipts/adp_engine_vs_readme.txt` |
| comment-stripped preprocessing, every `hdl/**/*.sv`, `ddb3119` against the head | 2 files differ, exactly the tick removal; `hdl/` patch-id identical at both bases | `scripts/rtl_preproc_compare.sh`, `receipts/rtl_preproc_compare.txt`, `receipts/rtl_preproc_diff.txt` |
| review clone after all work | HEAD and tree exact; 0 status entries; index == HEAD == worktree; index and tree blob/mode lists equal (sha256 `81d0ef18…`); 0 gitlinks, no `.gitmodules` | `receipts/clone_integrity.txt` |
| hosted checks at the exact head (read only, 07:41Z) | `docs-gates` and `portability` completed **success** (push and pull_request runs); `suites` **in progress** | `receipts/hosted_checks_at_head.txt` |

Wall times are in `receipts/*.time`. The longest run was d3 at 36 min. The unit's memory never OOM-killed anything (`memory.events` `oom_kill 0`).

## Five lenses

- **Conformance: CLEAN.**
  - The figures now agree with 02's landed faces and with the owner decision: the processor keeps no counter bank.
  - F01.1 claims no class-B face for gPTP, AVTP or media clocking, as 02 §1 states, citing Milan v1.2 §5.4.2.10, .15/.16, .19/.20 and .23 to .25.
  - The merge leaves the `ctr_*` contract (02 §4.6, integrator guide §7.1) and P2's DEADLINE contract (02 §8) each intact.
  - The only residue is the 00 mechanism cell (R443-4-R1).
- **RTL: CLEAN.**
  - Rounds 3 and 4 add no logic of this lane's.
  - The merged top is git's clean auto-merge, equal to my re-merge.
  - The lane's net RTL on the new base is the tick removal only, and lint is 41/41.
  - The OOC re-measure is a PR-body record (S2).
- **Robustness: CLEAN.**
  - The merge does not touch the face's hold/watchdog contract (`DESC_MEM_TMO_CYC_P`, 02:209-210, :435) or P2's NVM deadline bound.
  - The slot decode is unchanged and still graded by K17. All four K17 arms are KILLED here.
- **Tests: CLEAN.**
  - Sweep 1,020,227; every `tb/pp_top` campaign and the adp_engine campaign reproduce their README records arm by arm; patches 224/224.
  - Hosted CI does not run the ctr campaign (S3).
- **Docs: CLEAN.**
  - Figures: source equals render, the gates pass, the stale negative control works, and the labels are clean.
  - F01.5 is correct; 09's numbering and citation are correct; the PR body's round 3 and 4 claims check out.
  - Open items are SUGGESTIONs S1 and S2 and RESIDUE R1, plus the retained R443-2-S1 and the F09.1 half of R443-2-S2.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 02 §1, §4.1 to §4.6, §5, §8; integrator guide §7, §7.1, the `NVM_MEM_TMO_CYC_P` row; 00 GAP-04/05 and REQ-ADP-009; F01.1 tags against 02; #78 and #79 acceptance; the owner decision and the GM ruling | R443-4 (rounds 3 and 4) | af751a5aa9a809c982949cfb838a0de1fffc3e46 |
| RTL | CLEAN | `hdl/adp/KL_adp_engine.sv`, `hdl/top/protocol_processor_top.sv` (`:173`, `:1100-1180`, `:2268`, `:2884`, `:3143-3164`), `hdl/aecp/KL_aecp_notify.sv:382-508`; comment-stripped preprocessing of all `hdl/**/*.sv` at both bases; the `hdl/` patch-id; `lint_hdl.sh`; `syn/ooc/README.md` | R443-4 | af751a5aa9a809c982949cfb838a0de1fffc3e46 |
| Robustness | CLEAN | the read-face hold and watchdog text (02:205-211, :430-437); the notify slot decode with K17 and its four arms; P2's deadline text kept; merge-side integrity | R443-4 | af751a5aa9a809c982949cfb838a0de1fffc3e46 |
| Tests | CLEAN | `run_suites.sh` (33 suites); ctr, aecp, aecp_dispatch, notify, acmp, d3, gsi and name_wr campaigns; adp_engine campaign; 224 campaign patches; each against `tb/pp_top/README.md` and `tb/adp_engine/README.md`; `.github/workflows/hdl.yml` | R443-4 | af751a5aa9a809c982949cfb838a0de1fffc3e46 |
| Docs | CLEAN | `docs/diagrams/src/{01-system-context,01-top-level,03-shared-datapath}.drawio` and their SVGs (re-exported and rendered); every SVG and Mermaid fence (label search); 01 §2, §4, F01.5; 03 §2, §5; 09 §8.6/§8.7; 00:539; `make check`; stale control; PR body rounds 3 and 4 | R443-4 | af751a5aa9a809c982949cfb838a0de1fffc3e46 |

## Real limits

- **No synthesis run.** I did not reproduce the out-of-context -43 LUT / -81 FF figures (or the base's 30,701 / 32,025). The lane-side logic delta is proved to be the tick removal only. The numbers are the author's.
- **Not run:**
  - the parent consumer set (16) and the donor bank (9) at milan-fpga dev `1269cdaf` with the c8 and p2 adoption patches (manager's);
  - `make -C tb/nvm_port figures` (160 builds, P2's gate; the hosted `suites` job carries it);
  - `syn/yosys/run.sh` (the hosted `portability` job is success at this head);
  - the srp_top and maap unit campaigns. The merge changes none of their inputs; `git apply --check` covers their patches.
- **Not reproduced:** `ctr_mutants.py` at `--jobs 1` against `--jobs 8`. I ran `--jobs 3`, and its record is byte-identical to the author's `--jobs 1`, `--jobs 5` and `--jobs 8` records (same sha256).
- **Public evidence directory:** `review-evidence/ppC7-r1` at `c0212c4d` holds round-1 author artifacts only. I found no exact-head bank receipts there; that claim is the manager's.
- **Hosted CI:** at 07:41Z the `suites` job was still in progress at the exact head; `docs-gates` and `portability` had succeeded. I own neither result.
- **No hardware:** physical calibration NOT RUN, and no hardware or field claim is made.

## Pending manager duties

- The donor bank (9) and the parent consumer set (16) at milan-fpga dev `1269cdaf` with `parent-adoption-c8-cdf49d1a.patch` then `parent-adoption-p2-cdf49d1a.patch`. Then the final current-dev candidate at the merge turn (source base `ddb3119d`, live dev `1269cdaf`).
- Hosted/act acceptance: the `hdl` workflow's `suites` job at `af751a5` (push run 37104039718, pull_request run 37104042596) was in progress when this review ended.
- Carry R443-4-R1 (exact fix above) to the residue checklist.
- Decide whether to take the SUGGESTIONs: R443-4-S1 to S3, plus the retained R443-2-S1 and the F09.1 half of R443-2-S2.

R443-4 FINISHED

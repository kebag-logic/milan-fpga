[R558] NEGATIVE - exact head eb86b843557c6d9300847e3b6e12851604580b69

# R558-9 - issue #696 / PR #706 - composition review of the merge-train candidate

- **Candidate:** `eb86b843557c6d9300847e3b6e12851604580b69`, tree `623d921bf8c84cd9f3717887ce2702cbaf1448f8`.
  - First parent: live dev `cfadd767a7ad47aaee68de655e1066cc000fb8a0`.
  - Second parent: the PR source head `32582421bbf095a7b5a7d4b953c4d737b86fe54b`.
- **Role:** cleared-context internal reviewer, composition acceptance only. The source head already has two POSITIVE source reviews: R558-8 (comment 6103750948) and R559-7 (comment 6103915710).
- **Verdict:** NEGATIVE on one composition MINOR (R558-9-F1, Docs).
  - The merge leaves `MARK_II_AREA_PLAN.md` claiming that M2's base route equals the `route-1x1` record. In the composed tree that record is this PR's 50,013-LUT re-record, not the 50,267-LUT record the sentence was written against.
  - Every RTL, test and gate result on the composed tree is clean.

## 1. Scope reconstructed from public state

- **Read in order:**
  - AGENTS.md and CONTRIBUTING.md;
  - docs/README.md;
  - the #696 issue body and every assignment and ruling comment (6076750392, 6076940309, 6079087547, 6079463350, 6080332335, 6089712293, 6093171536, 6097504752, 6102832618);
  - the round's start comment, 6112976769;
  - `docs/design/AREA_BUDGET.md` (the resource-gate policy, the Mark II exception D7 and the bank rule at `:444-449` and `:514-527`);
  - `docs/design/MARK_II_AREA_PLAN.md`;
  - `syn/ooc/pp_resource_baseline.json`;
  - then the diff `cfadd767..eb86b843` and the history.
- **Composition question:** does the composed tree introduce any defect beyond the two reviewed sources (dev `cfadd767` and PR `32582421`)?
- **Dev merges since the lane base `e8454e27`** (`receipts/composition.txt`):
  - #709 (B14 bench);
  - #712 (B15 tone lane);
  - #710 (Mark II M2);
  - #719 (Mark II M6);
  - #718 (lwSRP `08ee86e8`).

## 2. Composition facts (`receipts/composition.txt`)

- **The candidate is the mechanical merge.**
  - `git merge-tree --write-tree cfadd767 32582421` gives `623d921b`, the candidate's tree, with no conflict.
  - Every one of the PR's 17 per-file patches (`e8454e27..32582421`) has the same stable patch-id in `cfadd767..eb86b843`. The PR is carried byte-for-byte.
- **Files changed on both sides since the lane base:** exactly the four the manager named.

| File | Dev hunks (commit) | PR hunks | Overlap |
|---|---|---|---|
| `hdl/milan/milan_datapath.sv` | `+3450..3533`, `+6337..6344` (M6 `6bfeeb13`) | `+267`, `+7171,2` | none; the closest pair is more than 800 lines apart |
| `docs/design/AREA_BUDGET.md` | `+197..211`, `+277` (M2 `ac2c5e77`, M6) | `13`, `107..152`, `371`, `410`, `463..469` | none |
| `docs/design/MARK_II_AREA_PLAN.md` | `+454`, `+556`, `+673..703`, `+860..862`, `+920..965` (M2, M6) | `56`, `110..147`, `653..654` | none textually. **Semantic interaction found: R558-9-F1** |
| `docs/findings/README.md` | row 15 (#712, B15) | row 25 (the #234 row) | none |

- **Other shared surfaces I checked:**
  - Registries and workflow pins: `ci_events.py --check` / `--selftest`, `check_rtl_source_lists.py`, `pp_srcs.py --check`, `suite_shards.py --selftest`.
  - Generated pages and TOC/anchors: `gen_toc.py --check` / `--verify-anchors`, `DOC_MAP.gen.py --check`, `submodule_boundaries.gen.py --check`, `check_diagram_pngs.py`.
  - The record file: `pp_resource_gate.py check-baseline`.
  - Line citations into `milan_datapath.sv` that M6's added lines could shift: the PR adds no `milan_datapath.sv:<line>` citation.
  - The findings index: the composed table has 21 rows, each page once, the same row set as dev. The PR changes only the #234 row's last sentence.

## 3. Findings of this round

### R558-9-F1 - MINOR - Docs - `docs/design/MARK_II_AREA_PLAN.md:695-696`, `:947` - after the merge, M2's base route is said to equal the `route-1x1` record, which is now #696's

- **Authority/evidence:**
  - At the candidate, `syn/ooc/pp_resource_baseline.json` records `route-1x1` as follows:
    - LUT 50013, FF 54306, SLICE 15753, WNS 0.233, WHS 0.017;
    - its `measured` note names #696's lane head `bee1b0d7`.
  - The same page says so at `MARK_II_AREA_PLAN.md:110`: "the gate's current record, #696's first-draw re-baseline". `:656` says "now at 50,013 LUTs ... that record is the comparison anchor".
  - Dev's M2 section (`2b22bf29`, PR #710) tabulates "Base route at dev `e8454e27` | 50,267 | 54,413 | 15,779 | 74 / 27 | +0.299 / +0.031" (`:690`). It then states at `:695`: "The base route equals the `route-1x1` record in every gated figure."
  - `:696` ("Against that record, the M2 route passes") and M6's `:947` ("Against the record, the M6 route passes") use the same referent.
  - `scripts/record_vs_lane_routes.py` (`receipts/record_vs_lane_routes.txt`) reads the record and the plan at each revision:
    - At dev `cfadd767` the base row equals the record: YES.
    - At the PR head `32582421` the M2/M6 sections do not exist.
    - At the candidate the base row does **not** equal the record: LUT, FF, SLICE, WNS and WHS all differ.
  - So neither source carries the defect. The merge alone makes `:695` false.
- **Why MINOR and not RESIDUE:** the sentence states the identity and figures of the *gate* record ("equals the `route-1x1` record in every gated figure"). It is not a baseline-scoped sentence.
  - This is the same class as R558-5-F1 on this PR (comment 6097253076). There, the merge made M0s's "the accepted 50,267-LUT route remains the comparison record" false, and that finding was MINOR and was fixed at `:656`.
  - It differs from R558-2-R1 / R559-2-R1, where each figure was correct for a baseline the page explicitly retains.
- **Impact:**
  - The merged page names two different records as the `route-1x1` record (`:110`/`:656` against `:695`).
  - D7 lanes take their comparison anchor from these intermediate-measurement sections (`AREA_BUDGET.md:365,452`). The next lane modelled on M2/M6 would anchor on 50,267, which is no longer the gate's record.
  - No gate detects it: all 39 documentation, static and record gates pass on the candidate.
  - The M2 and M6 pass verdicts themselves survive. Against #696's record, M2 moves +126 LUT, +48 FF and +18 slices, and its WNS rises. M6 moves +38 slices, and its WNS falls 0.092 ns to +0.141. Both are within every tolerance and floor (`receipts/record_vs_lane_routes.txt`). So no measurement or verdict is wrong, only the record each section names.
- **Required outcome:** at the merged head, `:695-696` and `:947` name the record each lane was compared against: #645/#647's `route-1x1` record, the gate record at dev `e8454e27`. Either they say that #696's record has since replaced it, or they name both. None of them may imply that the current `route-1x1` record is the 50,267 figure. One fix that keeps every figure:
  - `:695`: "The base route equals #645/#647's `route-1x1` record, the gate record at dev `e8454e27`, in every gated figure; [#696](https://github.com/kebag-logic/milan-fpga/issues/696)'s 50,013-LUT re-record has since replaced it."
  - `:696`: "Against that record, the M2 route passes with no failing endpoint; it also passes against #696's record."
  - `:947`: "Against #645/#647's record, the M6 route passes with no failing endpoint; it also passes against #696's record."
- **Verification:**
  - `python3 -I scripts/record_vs_lane_routes.py <repo> <merged-head>` reports the base row against the record. The sentences must then name the record that row matches.
  - `docs_check.py`, `gen_toc.py --check` / `--verify-anchors`, `check_em_dash.py --base <first parent>` and `pp_resource_gate.py check-baseline` exit 0.

### R558-9-R1 - RESIDUE - Docs - `docs/design/MARK_II_AREA_PLAN.md:706`, `:968` - lane-scoped "gate record stays unchanged" lines now sit beside #696's re-record

- Both M2 and M6 end with "The gate record stays unchanged under D7." Each is true of its lane, and the paragraph makes the lane its subject. On the composed page, though, the gate record did change, through #696.
- This is wording only: it states no figure or record identity, and it changes no verdict. It is the same class as retained R558-5-R1.
- **Exact fix:** `:706` "M2 does not re-record the gate under D7." and `:968` "M6 does not re-record the gate under D7."

No BLOCKER or MAJOR.

## 4. Executed evidence on the candidate (this round, this clone)

- **Toolchain:** pinned Verilator 5.050 (`verilator --version`: `Verilator 5.050 2026-07-01 rev v5.050`, through the scoped wrapper; the binary's sha256 is `44898b22...`). Documentation gates ran in a private venv holding `tools/markdown/requirements.txt` installed with `--require-hashes`, plus pyyaml and wavedrom 2.0.3.post3. Host python3 3.14, GNU make.
- **MAAP suite** (`make all VERILATOR_JOBS=2`, rc 0; `receipts/maap_all.log`):
  - unit `KL_maap: 186 checks, 0 failures`;
  - campaign `checks: 65 failures: 0`: the unit clean control and the real-datapath clean control (`m4_datapath_clean`) pass, and all 63 planted defects fail their named checks;
  - the integration build derives its sources from the composed `milan_datapath`.
- **Datapath wiring probes** (`scripts/probe_datapath_wiring.py`; `receipts/probe_a.log`, `probe_b.log`, `receipts/probes/`):
  - **Why:** the datapath flags waive `PINMISSING`, so a connection dropped in a merge would compile silently. Each probe edits one exact-once anchor in a scratch copy of the candidate datapath and builds the real-datapath MAAP harness with the suite's own source list and flags.
  - clean control: 5 checks, 0 failures;
  - `.port_operational_i` tied to `1'b1`: CAUGHT at "M5 datapath: link return starts four fresh PROBEs";
  - `.port_operational_i` connection deleted: CAUGHT at the same check;
  - `.realtime_ns_i` connection deleted: CAUGHT at "M3 datapath: real-time clock changes probe intervals" and "M3 datapath: fixed PHC time pair claims different first offsets".
- **Datapath suite** `make -C tb/verilator/milan_dp -j2 run SIM_JOBS=2 VERILATOR_JOBS=2`: rc 0, 32 min 34 s, 0 failures in every leg (`receipts/milan_dp_run.log`). The legs:
  - gptp 182 and gptp-lat 182, gmstep 104;
  - 1x1 legacy 236, notify 421, crflic 417, dynmap 162;
  - nxn 1967, divergent 1969, nxn8 3751, nxn4c 1967;
  - nolpf 236, prune 33 (MAAP_P = 0), ax1x1 233, aclk 193;
  - render and gmstep mutant campaigns 6/6 and 6/6.
  - They cover:
    - KL_maap's claim walk and DA grant (log lines 1054-1074);
    - "MAAP unclaimed/off" talker holds (log lines 3502-3504);
    - 13 passing GET_COUNTERS checks, which read M6's counter table.
  - The total is 12,065 checks. The manager's candidate shard for `milan_dp` reports the same 12,065 with 0 in-suite failures.
  - A first attempt with `SIM_JOBS=4` stopped at `sim_pool.py`'s 1-2 job guard before any simulation. It is retained unpublished under scratch, and the rerun above is the evidence.
- **Firmware MAAP differential** `maap_differential.py --self-test`, rc 0 (`receipts/maap_differential_selftest.log`): clean 12/12; differential mutants 17/17 caught. It imports `ctrl_mutants`, which imports dev-changed `ctrl_arms.py`.
- **Lint** `lint_rtl.py --check --self-test`: rc 0, `90 violation(s) <= ratchet 90`.
- **Static and documentation set** (`scripts/doc_gates.sh`; `receipts/doc_gates/summary.tsv`): 39 commands, 39 rc 0. Among them:
  - `docs_check.py`: 0 findings over 203 md files;
  - `check_em_dash.py --base cfadd767`: 0 findings over 339 added lines in 7 pages;
  - `gen_toc.py --selftest` / `--verify-anchors` (477 links) / `--check` (143 pages);
  - `ci_events.py --check` / `--selftest` (1749 items, 2374 arms);
  - `pp_resource_gate.py check-baseline` (`baseline PASS: 3 endpoints`) and `--selftest`; `pp_baseline.py --selftest`;
  - `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest`, `check_port_contracts.py`, `measure_test_evidence.py --check`, `check_hygiene.py --check`, `check_wire_accountability.py --self-test`, the idiom and naming gates.
- **Further self-tests:** `suite_shards.py`, `check_sweep_shape.py`, `check_entity_shape.py`, `check_deploy_shape.py` and `ci_scope.py`, all rc 0 (`receipts/static2/`).
- **Hosted checks:** a snapshot at PR head `32582421` (`receipts/hosted_checks_32582421.tsv`) shows 22 success and 1 skipped (the nightly/manual physical gPTP context, which is not hardware proof).
  - These runs were created at 2026-10-10T23:55Z, before dev reached `cfadd767` (2026-10-11T19:41Z).
  - The candidate commit is not on GitHub.
  - So no hosted evidence covers the composed tree.
- **Tree after all runs** (`receipts/tree_state_final.txt`):
  - HEAD `eb86b843`, tree `623d921b`;
  - index identical to HEAD and worktree identical to index (bytes and modes); no untracked non-ignored file;
  - gitlinks: protocol-processor `2ad2f845`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`, lwSRP `08ee86e8` (not checked out), external `efeb541a` (not checked out);
  - probes wrote only under the packet's scratch directory.

## 5. Prior public findings on this PR, at this head (read after my own pass)

| Finding | State at `eb86b843` | Evidence |
|---|---|---|
| R558-7-F1, R559-6-F1, R559-6-F2 (MINOR, Tests/Conformance/Docs) | **Still resolved; unchanged by composition** | `sim_main.cpp`, `mutants.py` and `MAAP_FABRIC.md` patches are identical to source. The named checks pass and plants q3, q9, q1 and `m2_echo_overlap_start` are rejected in this round's campaign |
| R558-6-F1 (MINOR; Conformance, RTL, Robustness, Tests) | **Still resolved** | `KL_maap.sv` patch identical to source. Both p7 plants are rejected (unit and datapath) in this round's campaign |
| R558-5-F1 (MINOR, Docs) | **Still resolved** | `AREA_BUDGET.md:379` and `MARK_II_AREA_PLAN.md:655-656` name #696's 50,013-LUT record. The dev M2/M6 sections that arrived later reopen the same class at other lines: **R558-9-F1** |
| R558-3-F1 = R559-3-F1 (BLOCKER, `integration.mk`) | **Still resolved** | `integration.mk` identical to source. The composed integration build derives its sources and runs 5/0 (campaign and probe controls) |
| R558-1-F1, R559-1-F1/F2/F3 (MINOR) | **Still resolved** | The inventory route column equals the record scopes, 22 rows with 0 differences (`receipts/record_vs_lane_routes.txt`). The M5 loss check passes |
| R558-2-R1 / R559-2-R1 (RESIDUE) | **Retained** on the residue checklist | Still applies at `MARK_II_AREA_PLAN.md:66-67`, `:317`, `:1086` (cited earlier as `:970`/`:1007`; only the line numbers moved) |
| R558-5-R1 (RESIDUE) | **Retained** | `AREA_BUDGET.md:370`, `:387`; `MARK_II_AREA_PLAN.md:668` |
| R559-7-R1 (RESIDUE, PR body) | **Retained** | The PR body still says "Hosted checks and the local workflow replica need the pushed head." |
| R558-8-S1 (SUGGESTION, `TESTING.md` maap row) | **Retained, optional** | Dev changed `TESTING.md`, but the maap row (`:606`) is unchanged |
| R559-7-S1, R558-6-S1, R558-6-S2, R558-7-S2, R559-6-S2, R559-6-S3, R559-5-S1, R558-3-S1/S2, R559-3-S1, R558-4-S1/S2, R559-4-S1/S2, R559-1-S1..S4 (SUGGESTION) | **Retained, optional, no lens effect** | Cited sources are identical to source; composition touches none of them |

## 6. Lens results (same format as findings)

```text
[R558] PASS Conformance - hdl/milan/milan_datapath.sv:7181-7186 (composed KL_maap instance) and tb/verilator/maap at eb86b843 - checked against #696 acceptance 1-3 and rulings 6079463350/6102832618: KL_maap.sv patch byte-identical to source; candidate unit 186/0, real datapath 5/0, campaign 65/65, differential 12/12 + 17/17; the M5 link-return and M3 clock-seed behaviour hold through the composed datapath (probes: dropping either connection fails its named check)
[R558] PASS RTL - hdl/milan/milan_datapath.sv:267,2124,2165,3000,3450-3533,6337-6344,7181-7186 - PR hunks (+267, +7171) and M6 hunks (+3450..3533, +6337..6344) are disjoint; port_operational_i and realtime_ns_i are connected once each to nets declared once (eff_link_w :2165, ptp_now_w :2124) under `default_nettype none; fresh merge-tree equals the candidate tree; lint 90 <= 90; every composed milan_dp shape elaborates and passes (incl. MAAP_P=0 prune leg)
[R558] PASS Robustness - receipts/probes/*.run.log, receipts/milan_dp_run.log - the PINMISSING waiver means a dropped connection compiles; three wiring faults (link tied high, link dropped, clock dropped) are each caught by the composed suite; pruned-engine leg 33/0; link-return and MAAP-off talker holds pass on the composed datapath; GET_COUNTERS checks that read M6's counter table pass beside the live MAAP engine
[R558] PASS Tests - tb/verilator/maap/{integration.mk,mutants.py,sim_integration.cpp} and tb/verilator/milan_dp at eb86b843 - integration build derives the composed source list (milan_dp unchanged by dev); 65-row campaign with both clean controls; milan_dp run rc 0 (12,065 checks, matches the manager's candidate shard); no test changed by composition (patch-ids identical); R558-8-S1 retained as optional
[R558] UNCLEAN Docs - docs/design/MARK_II_AREA_PLAN.md:695-696,947 - open MINOR R558-9-F1; also examined and otherwise clean: AREA_BUDGET.md:10,104-152,197-212,277,365-387,410-470 (record table arithmetic 50,013/63,400 = 78.88 %, 11,973 over, 97 slices free, wrapper 22,993 - 11,973 = 11,020); MARK_II_AREA_PLAN.md:56,107-147,650-668,677-706,924-968; docs/findings/README.md (21 rows, each once, dev's row set); 39 documentation/static/record gates rc 0; RESIDUE R558-9-R1
```

## 7. Reviewer-owned completion ledger

The composition touches the scope of all five lenses: RTL through `milan_datapath.sv`, Docs through three shared pages, and Conformance, Robustness and Tests through the composed datapath that the MAAP integration and `milan_dp` suites elaborate. Each lens was therefore applied at the candidate. None is banked from the source reviews alone, although R558-8 and R559-7 cover the source head `32582421` for every lens.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | composed KL_maap instance; MAAP unit/datapath/campaign; differential; wiring probes | R558-9 | `eb86b843557c6d9300847e3b6e12851604580b69` |
| RTL | CLEAN | `milan_datapath.sv` hunks of both sides, declarations, merge-tree, lint, all milan_dp elaborations | R558-9 | `eb86b843557c6d9300847e3b6e12851604580b69` |
| Robustness | CLEAN | 3 wiring probes plus control; prune leg; link/MAAP-off holds; GET_COUNTERS checks | R558-9 | `eb86b843557c6d9300847e3b6e12851604580b69` |
| Tests | CLEAN (SUGGESTION R558-8-S1 retained) | MAAP target 186/0 and 65/65; milan_dp 12,065/0; differential 12/12, 17/17 | R558-9 | `eb86b843557c6d9300847e3b6e12851604580b69` |
| Docs | **UNCLEAN** (MINOR R558-9-F1 open; RESIDUE R558-9-R1, R558-2-R1 / R559-2-R1, R558-5-R1, R559-7-R1 on the checklist) | `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, findings index, record file; 39 gates | R558-9 | `eb86b843557c6d9300847e3b6e12851604580b69` |

## 8. Real limits

- **No Vivado, Yosys or xvlog run.**
  - The resource record is verified by `check-baseline` and arithmetic, not by re-measurement.
  - The composed image (M2 + M6 + #696) has never been measured. The record describes `bee1b0d7`, which has neither M2 nor M6.
- **Not run here:** the full parent sweep, processor/gPTP/Yosys/builder banks, `act`/`act_ci`, the firmware bank, field campaigns and the M6 lockstep suites (`avtp_rxmon`, `chmap_capture`, whose inputs the PR does not touch).
- **Submodules:** lwSRP and `external` are not checked out in this clone. No suite I ran needs them.
- **Toolchain:** host python3 3.14 and GNU make, not the hosted 3.12 / make 4.3 image.
- **Hardware:** no physical calibration, bench or hardware run. Acceptance 4 (bench interop) is not exercised, and field skips are not hardware proof.
- **Hosted evidence:** it exists only for the PR head and predates dev `cfadd767`, so none covers this tree.
- **Manager bank:** the candidate bank's `complete.json` was absent when read. Only its `milan_dp` shard summary was visible.
- **Out of scope:** two observations predate this PR and are not counted:
  - Five findings pages (`387_SOFTWARE_GM_STEP.md`, `394_387_E1_SWITCH_CYCLES.md`, `599_394_E1_LINK_CYCLES.md`, `667_TALKER_START_BENCH.md`, `B14_BENCH_5603C353.md`) are on dev but not in the findings index.
  - Three citations point at `KL_maap.sv` line numbers that were already stale at the lane base: `KL_pp_shadow.sv:739` cites `:275-277`, and `tb/verilator/pp_shadow/README.md:342` and `sim_main.cpp:95` cite `:154`.

## 9. Pending manager duties

- Disposition R558-9-F1 on the lane or the merge, then re-review the Docs lens at the new candidate.
- **Merge-bank resource comparison** for this candidate (`AREA_BUDGET.md:514-527`). Dev's delta since the record's `measured` revision `e8454e27` touches RTL: M2 `KL_pp_shadow.sv` and `milan_soc.py`, M6 `KL_avtp_rx_monitor_ctx.sv`, `KL_chan_map_capture.sv` and `milan_datapath.sv`.
  - Decide whether #696's record must be re-recorded on this merge result under `:444-446`, or stand under D7 with the ledger separating predecessor movement from the lane delta.
- Accept the hosted contexts and the act replica (running at the PR head), and publish the candidate builder and native bank receipts (`complete.json` pending).
- Carry RESIDUE R558-9-R1, R558-2-R1 / R559-2-R1, R558-5-R1 and R559-7-R1 on the residue checklist.
- Route acceptance 4 to the post-merge bench lane, then run post-merge containment.
- Obtain the external composition verdict if the bar requires it; this report is the internal one.
- Optionally open Issues for the two out-of-scope observations in section 8.

## 10. Packet

Paths are relative to this packet and listed with their SHA-256 in `MANIFEST.sha256`.

- **Scripts:**
  - `scripts/composition_check.sh <repo> <candidate> <dev> <pr>`;
  - `scripts/record_vs_lane_routes.py <repo> <rev>...`;
  - `scripts/probe_datapath_wiring.py <repo> <scratch> <probe>...`;
  - `scripts/doc_gates.sh <repo> <venv-python> <em-dash-base> <out>`.
- **Receipts:**
  - `receipts/composition.txt`, `receipts/record_vs_lane_routes.txt`, `receipts/tree_state_final.txt`, `receipts/hosted_checks_32582421.tsv`;
  - `receipts/maap_all.{log,rc}`, `receipts/milan_dp_run.{log,rc}`, `receipts/maap_differential_selftest.{log,rc}`;
  - `receipts/probe_{a,b}.{log,rc}`, `receipts/probes/*.run.log`;
  - `receipts/doc_gates/` (39 logs plus `summary.tsv`), `receipts/static2/`.
- **Redaction:** home-directory paths in receipts are written as `$HOME`, as CONTRIBUTING section 6 requires. Nothing else is altered.

R558-9 FINISHED

[R592] NEGATIVE - exact head 412e3f6c8c402bce63e94c291d2782b5579aaa1d

# R592-4: internal review of PR #713 (issue #640, Mark II lane M7), round 4

- Parent head `412e3f6c8c402bce63e94c291d2782b5579aaa1d`, tree `3a0b668761728b2e9fcc328f71f67f885ef3d11e`. Merge parents `354f7818` (lane) and `fa820988` (dev).
- Donor head `e4869fd0c42889b2ac806587cc5c78afb1c33461` (Mister-M-alt/FPGA-gPTP#78, public PR head). It sits on donor merge `6b5a4282` (parents `18dd997b`, `61d486e9`).
- Scope: the delta in the round-4 assignment (issue #640 comment 6161607579) and the continuation ruling (comment 6162175442). R592-3 and R593-3 cover `354f7818` / `18dd997b`; earlier rounds stand for anything this delta does not touch.
- Reviewer: [R592], internal, cleared context. I reconstructed the task from AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #640 (body, M7 assignment 6097272538, round-4 assignment, STOP 6162158855, ruling, REVIEW READY 6162686301), the PR body, the diff and history, and public evidence. I read prior public review findings only after my own pass over the diff. I have not read the concurrent external round.

## Summary

- The ruling's five judged items hold:
  - (1) The donor merge is correct.
  - (2) The donor style commit changes no behaviour.
  - (3) The parent pin, diagram and ROM records reproduce from their generators.
  - (4) The M7 26-arm verdict is 26/26 at this head.
  - (5) The PR body labels every area and timing figure historical at its own revision.
- **One BLOCKER is new and was introduced by the merge commit (R592-4-F1).**
  - The lane's new default suite `gptp_tables` meets dev's per-suite duration table (#727, dev commits from 2026-10-12) for the first time in this merge. The table has no entry for it.
  - So `scripts/suite_shards.py --selftest` fails at this head (rc 1). Both merge parents pass it.
  - The mandatory serial sweep aborts in its preflight.
  - All five hosted Verilator workers at this exact head fail before running any suite, and `verilator-suites` fails.
  - The executor's 35-gate static table does not include this check.
- Lenses: RTL, Robustness and Docs are CLEAN. Conformance and Tests are UNCLEAN because of F1.
- New this round: one SUGGESTION (R592-4-S1). Prior RESIDUEs and SUGGESTIONs are carried as listed below.

## Independent executions at this head

All receipts are in `receipts/`. Verilator is the pinned 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`). Build logs show its install root as `<PINNED_VERILATOR_ROOT>`; that is the only edit made to any receipt.

| What | Command (cwd) | Result | Receipt |
|---|---|---|---|
| Donor merge recomputed | `git merge-tree --write-tree --name-only 18dd997b 61d486e9` | One conflict, `docs/MANAGER.md`. Recorded merge `6b5a4282` differs from the automatic merge in that file only | `donor_merge_verification.txt` |
| Donor clock refactor, AST | `scripts/compare_clock_arms.py old.py new.py` | Arm-building statements identical (10/10, 29/29 arms). Rest of `selftest` identical once docstrings are ignored. Every other definition and module statement unchanged | `donor_clock_arms_ast.txt` |
| Donor clock self-test before/after | `check_ooc_clock.py --selftest` at `6b5a4282` and `e4869fd0` | Both `PASS (30 arms)`. Probes: a disabled `timing_findings` fails ("wrong period escaped"); a dropped arm reports 29 | `donor_clock_selftest_before_after.txt` |
| Donor parser simulation before/after | `make run` in git-archive extractions of both heads | 337/337 both. Simulation output byte-identical (sha256 `95f9e764…`) | `donor_parser_run_*.log`, `donor_parser_before_after_compare.txt` |
| Donor contract and docs | `make contract docs` (extraction of `e4869fd0`) | rc 0 | `donor_contract_docs_e4869fd0.txt` |
| Donor ROM figures | `gen_gptp_ucode.py -o …` | `1024 words, 1016 real (99.2%)`; `FUTO@249`, `SERVO@0`, no other leg in 0..15; sha256 `a435fba6…` | `donor_ucode_gen.txt` |
| Parent ROM ledger | `./ooc.sh --record-rom-digests` then `git diff` | Recorder rc 0; ledger byte-identical to the committed one. Rows = union of both parents plus `6b5a4282` and `e4869fd0`; none dropped, no duplicate key | `parent_rom_digests_rerecord.txt`, `parent_rom_digests_rowset.txt` |
| Parent diagrams | both `.gen.py` in `--check`, `--selftest` and write mode, then `git diff` | All rc 0. Write-mode output byte-identical to the committed files. `check_diagram_pngs.py` (6 rasters) and `--selftest` (28 controls) rc 0 | `parent_diagram_*.txt`, `parent_check_diagram_pngs*.txt` |
| Parent merge recomputed | `git merge-tree --write-tree 354f7818 fa820988` | 18 conflicts (docs, diagrams, gitlink). Every file differing from the automatic merge is in that list or is the ROM ledger. All 17 lane files dev did not touch are blob-identical to `354f7818`. The lane's delta over dev equals its delta over base, except for pin rebases, regenerated diagrams and two `MARK_II_AREA_PLAN.md` sentences that now date the `route-1x1` record to `e8454e27` (dev's `b7f342ae` re-recorded it) | `parent_merge_verification.txt`, `parent_lane_delta_preserved.txt` |
| Idiom gates | `check_py_idiom.py`, `check_cpp_idiom.py` | rc 0; long function 9 <= 9, undocumented public 0 <= 0, multi-declarator 0 <= 0. No budget file or exception differs from dev. `selftest_arms` is 95 lines (limit 100) | `parent_check_py_idiom.txt`, `parent_check_cpp_idiom.txt`, `parent_idiom_no_exception.txt` |
| Idiom gates, fault demo | index gitlink and checkout set to `6b5a4282`, then restored | py rc 1 (long function 10 > 9, undocumented 1 > 0); cpp rc 1 (multi-declarator 4 > 0) | `probe_idiom_gates_at_6b5a4282.txt` |
| M7 26-arm mutation verdict | committed `mutants.py` run as four disjoint shards (`scripts/mutants_shard.py`) | 26/26 caught, each by its named check. Audit: every control exactly once | `m7_mutants/shard*.log`, `m7_mutants/coverage_audit.txt` |
| M7 census and declarations | `make run` in `tb/verilator/gptp_tables`; `gen_one_valued_table.py --check` | 36 checks, 0 failures; README table current | `m7_suite_run.log`, `parent_one_valued_table_check.txt` |
| Parent gPTP suites | `make run` in `gptp_shadow` and `gptp_plane`; `phc_step.py --mutants` | 309/309; 29/29; 62 checks and 8/8 campaign | `parent_gptp_*` |
| CI contract | `ci_scope.py --selftest`; `ci_events.py --check` | PASS; OK (2,174 items) | `parent_ci_scope_selftest.txt`, `parent_ci_events_check.txt` |
| Pins and docs | `check_submodule_docs.py` (+`--selftest`), `check_gptp_docs.py` (+`--selftest`, `--with-submodule`), `check_doc_paths.py`, `pp_resource_gate.py check-baseline` | all rc 0 (6 exact gitlinks; 8 pages, donor verified; 985 paths; baseline 3 endpoints) | `parent_check_*`, `parent_pp_resource_gate_check_baseline.txt` |
| **Suite selector** | `python3 scripts/suite_shards.py --selftest` | **rc 1**: `gptp_tables: inventory suite with no recorded duration in SUITE_SECONDS` | `parent_suite_shards_selftest.txt` |
| Suite selector at both parents | same, in git-archive extractions | `fa820988` PASS; `354f7818` PASS | `suite_shards_selftest_at_parents.txt` |
| Serial sweep entry | `scripts/run_all_suites.sh --shard 0/5 --list` | rc 2, same refusal | `parent_run_all_suites_list.txt` |
| Hosted, exact head (read only) | job logs of the five Verilator workers and `verilator-suites` | Each worker fails at "Prove specialized suite ownership" with the same `SUITE_SECONDS` line; aggregate fails | `hosted/verilator_shards_failure_lines.txt`, `hosted_check_runs_412e3f6c.tsv` |
| Em-dash | `check_em_dash.py --base …` | not judged: pinned renderer absent here (rc 2). Raw scan of added Markdown lines: 0 U+2014 in parent and donor deltas | `parent_em_dash_base_*.txt`, `em_dash_raw_scan.txt` |

## Findings

### R592-4-F1: BLOCKER (Tests, Conformance). The merge leaves the new `gptp_tables` suite out of the selector's duration table, so no Verilator sweep can start at this head

- **Location:**
  - `scripts/suite_shards.py:132-195` (`SUITE_SECONDS`) and `:200` (`PROVISIONAL_SUITES`), which do not name `gptp_tables`.
  - The suite itself: `tb/verilator/gptp_tables/`, a default inventory suite since this lane.
- **Authority and evidence:**
  - The selector's docstring (`scripts/suite_shards.py:5-12, 22-29, 53-86`) and `docs/testing/TESTING.md:514-517` require a change that adds a default suite to record its provisional figure in the same change, adding a worker if that predicts one over 60 %. These came from dev (#727, `111611fa9` through `2c2f3369`, 2026-10-12) and entered the lane through this merge.
  - `python3 scripts/suite_shards.py --selftest` returns rc 1 at `412e3f6c` and PASS at both parents. The merge commit created the failure.
  - `scripts/run_all_suites.sh:291-296` runs that self-test as the mandatory serial sweep's preflight, and `--list` already refuses with rc 2.
  - At this exact head, hosted jobs 115723316359, 115723316477, 115723316484, 115723316464 and 115723316351 fail before any suite with the same line, and `verilator-suites` (job 115724424278) fails.
  - The REVIEW READY's "All 35 recorded parent static gates pass" and the PR body's validation list do not include this check.
- **Probe (disposable, restored):** recording `gptp_tables` at the `suite_timeout` figure (`*` arm, 1800 s) and naming it provisional is not enough. The self-test then predicts workers 0-3 at 4,628-4,730 s against the 4,320 s bound. So the documented steps also require step 2, which adds a worker in `.github/workflows/rtl.yml` and `scripts/ci_events.py` (`receipts/probe_suite_shards_provisional_gptp_tables.txt`).
- **Impact:**
  - The issue's acceptance ("every suite, campaign and compliance check passes at the same counts") cannot be shown at this head.
  - CONTRIBUTING's mandatory serial sweep cannot run.
  - Section 7's exact-head `verilator-suites` evidence cannot exist.
  - Merged as is, every later dev sweep and every hosted Verilator worker would refuse to start.
- **Required outcome:**
  - A new head where `scripts/suite_shards.py --selftest`, `scripts/ci_events.py --check` and `--selftest`, and the serial sweep preflight all pass.
  - `gptp_tables` is recorded by the selector's documented new-suite steps, with no suite dropped or renamed to evade the inventory.
  - The hosted Verilator workers and `verilator-suites` then run on that exact head.
  - The ruling said "Nothing else changes", and the probe shows a workflow worker change may be needed. So the manager should rule publicly on the route before the executor edits.
- **Verification:**
  - The three commands above return rc 0 at the new head.
  - `scripts/run_all_suites.sh --shard I/N --list` places `gptp_tables` on exactly one worker.
  - The hosted workers report `gptp_tables` with its 36 checks.
  - Step 3's measured figure follows from that hosted run.

### R592-4-S1: SUGGESTION (Docs). The ROM ledger keeps a row for a donor revision no parent commit pins

- **Location:** `syn/yosys/rom_digests.tsv:32`, row `6b5a4282… gptp_ucode.hex a435fba6…`.
- **Evidence:** `6b5a4282` was staged during the STOP but never committed as a parent gitlink; the gitlink is `e4869fd0` (row `:61`). The recorder keeps other pins' rows by design, and re-recording at this head reproduces the file byte for byte, so the row is generator output and its digest is correct. Because `ooc.sh` refuses a checkout that disagrees with the gitlink, the row is inert.
- **Suggested outcome (optional):** drop the row in the commit that answers F1, or leave it as harmless history.

## Prior public review findings at this head (read after this round's own pass)

| Finding | Status at `412e3f6c` | Evidence |
|---|---|---|
| R592-1-F1..F5, R593-1-S-01, R593-1-S-02, R593-2-F1, R593-2-R-01, R593-2-S-01, R592-2-RES1 | Resolved (as R592-3 and R593-3 found) | The lane files that carried them are blob-identical to `354f7818` (`parent_merge_verification.txt`); M7 36/36 and 26/26 at this head |
| R592-3-RES1 RESIDUE (Tests, Docs): reference-independence wording | Open RESIDUE, carried to the residue checklist | `tb/verilator/gptp_tables/README.md:10`, `gptp_tables_wrap.sv:15` unchanged; exact fix as published in R592-3 |
| R592-3-RES2 RESIDUE (Docs): "widths ... unchanged" | Open RESIDUE, carried | `docs/design/MARK_II_AREA_PLAN.md:713`; exact fix as published in R592-3 |
| R593-3-R-01 RESIDUE (Tests, Docs): "two wrong declaration lists" | Open RESIDUE, carried | `tb/verilator/gptp_tables/Makefile:63`; the fix is "four" |
| R593-3-S-01 SUGGESTION: donor M7 figures without an evidence link | Retained | Donor `docs/MANAGER.md:72-99` at `e4869fd0` still has no link in that section |
| R592-2-S1 SUGGESTION (optional): full-ledger guard unexercised | Retained | Lane RTL unchanged |
| R593-1-S-03 SUGGESTION: lane guard widths | Retained, pre-existing, routed to #495 | `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:271` unchanged |

## Lens results

```text
[R592] BLOCKER Tests - scripts/suite_shards.py:132-200, tb/verilator/gptp_tables/, hosted jobs 115723316359..115724424278 - R592-4-F1
[R592] BLOCKER Conformance - issue #640 acceptance "every suite ... passes", AGENTS.md section 7 exact-head verilator-suites - R592-4-F1
[R592] PASS RTL - gptp-processor e4869fd0 hdl/ vs 7dda9c3b (timer = lane 18dd997b blob; parser rx_err_i change from FPGA-gPTP #80) against hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:690 (rx_err_i tied 1'b0, so no parent functional path); lane RTL blob-identical to 354f7818; gptp_tables 36/36, gptp_shadow 309/309, gptp_plane 29/29, PHC-step 62 + 8/8 at 412e3f6c
[R592] PASS Robustness - gptp-processor syn/ooc/check_ooc_clock.py (all 29 negative arms AST-identical, 30-control self-test, planted check-disable caught); parser 337 identical incl. the rx_err-on-any-byte arms; syn/yosys/ooc.sh record mode (anti-truncation count, rows retained, re-record byte-identical); idiom gates catch the pre-fix donor
[R592] PASS Docs - gptp-processor docs/MANAGER.md:33-125 at e4869fd0 (both measurement histories kept and dated; 1,016 words, eight free, FUTO@249 equal to generator output); parent pin pages (GPTP_PLANE, TIME_SYNC, SUBMODULES, four guides, ieee8021as) all name e4869fd0; diagrams and PNG manifest reproduce byte-for-byte; PR #713 body lines 45-78 label every area and timing figure historical at e8454e27 / 49e1ce48 / ba350298 and state that none qualifies the merged tree
```

Conformance on the ruling's own items is otherwise satisfied: (1) through (5) all hold, as shown in the table above. The F1 defect is what leaves Conformance unclean.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 open) | Round-4 assignment and ruling items (1)-(5); issue acceptance; merge recomputations; suite selector | R592-4 (not clean) | `412e3f6c` |
| RTL | CLEAN | Donor `hdl/` delta vs dev pin and vs `18dd997b`; parent tie-off `KL_gptp_shadow.sv:690`; lane RTL blobs; four parent gPTP suites | R592-4 | `412e3f6c` / donor `e4869fd0` |
| Robustness | CLEAN | Clock-checker negative arms; parser rx_err arms; ROM-ledger recorder; idiom-gate fault demo | R592-4 | `412e3f6c` / donor `e4869fd0` |
| Tests | UNCLEAN (F1 open) | M7 26 controls, 36 checks, census; donor clock 30 and parser 337 before/after; suite selector and sweep preflight; hosted Verilator jobs | R592-4 (not clean) | `412e3f6c` |
| Docs | CLEAN (S1 optional; three RESIDUEs carried) | Donor `MANAGER.md`; parent pin pages; diagrams; ROM ledger; PR body | R592-4 | `412e3f6c` / donor `e4869fd0` |

## Real limits of this round

- I ran no full parent, protocol-processor, gPTP or Yosys bank and no serial sweep, which cannot start at this head anyway.
- I did not run `milan_dp`, `milan_dp_gptp`, `gptp_txts`, `tsn_fuzz`, Docker, act, or the offline workflow self-test.
- I did not run the donor engine, microCPU, gaskets, traffic-generator or Arty targets. The style commit does not touch them, and the parser was re-run.
- I did not run the donor lint target.
- The pinned em-dash gate could not judge here because its renderer is not installed. Only a raw scan was run.
- No physical measurement was made. Physical calibration was NOT RUN, and field skips are not hardware proof.
- I did not re-verify the area and timing figures. Per the ruling they are historical, and I checked only that they are labelled that way.
- I read hosted results only. The manager owns hosted and act acceptance. Several hosted contexts were still in progress when read; the skipped "Physical gPTP" context is not an execution.
- Before writing this report I had not read the concurrent external round.

## Pending manager duties

- Rule on the route for F1 (provisional figure alone, or a worker added in `rtl.yml` and `ci_events.py`), since the ruling said "Nothing else changes". Then re-assign the fix and a fresh review at the new head.
- Build and validate the current-dev candidate merge (builder and native banks) at the merge turn, and link its receipts.
- The parent pins `e4869fd0`, which is the open head of FPGA-gPTP#78 and not on donor `main`. `docs/guides/gptp/HDL_DEVELOPER.md:31` says "Land donor changes before advancing its pin". Order the donor merge and the parent pin accordingly.
- Carry R592-3-RES1, R592-3-RES2 and R593-3-R-01 on the residue checklist.
- Run the daily #640 area measurement after merge, per the ruling.
- Check post-merge containment.

## Clone integrity after probes

- HEAD is `412e3f6c`. `git write-tree` equals tree `3a0b6687`.
- Worktree, index and HEAD agree in all 1,329 paths (mode, blob, path).
- The six gitlinks equal the submodule HEADs: gptp-processor `e4869fd0` on `640-m7`, protocol-processor `2ad2f845`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`; `external` is uninitialised as before.
- No untracked or ignored files remain (`receipts/clone_integrity_after_probes.txt`).

R592-4 FINISHED

[R909] NEGATIVE - exact head 9acb9b828b29aba71bd51303a4836f86c2278267

# R909-3: internal independent delta re-review of PR #987 (issue #979)

- **Head:** `9acb9b828b29aba71bd51303a4836f86c2278267`, tree `fd76b3610f374ccf589e220ef60e83d84a71f6e1`.
- **Delta:** the seven commits `dc78aeda..9acb9b82`. The implementation base is `3cda030c17`.
- **Evidence:** the author packet `review-evidence/loopbram-r1/author-r5` at public commit `0f09f6eeb886aa832b4401026be0d2c91dcdcb29`.
- **Method:** I used a cleared context and public state only. I did my own pass over the diff before I read the prior round's findings (R909-2, R910-2).
- **Lenses applied:** all five.

## Verdict summary

The fixes this round are real, and I checked them at their cause.

- **R910-2-F1 (missing output):** RESOLVED. I reproduced the external reviewer's talker-7 plant: it now fails exactly the four new named checks. Two plants of my own, each holding a stream off in one phase only, show that each phase is graded on its own.
- **R909-2-N2 / R910-2-F2 (enabled 8x8 route):** RESOLVED. The route was built from the same `hdl/`, `sw/` and `configs/` trees as this head and meets #818 on its best directive. I re-read the raw corner reports.
- **R909-2-N3 (campaign registry):** RESOLVED.
- **R909-2-R1 (residue):** RESOLVED.
- **R909-2-N1 (suites missing from the planner):** RESOLVED at its cause. The planner self-test passes, all 19 listings exit 0, each new suite has exactly one owner, and both owning shards pass through the real driver and tally. The registration method departs from the planner's own documented new-suite contract, though, and from the outcome N1 required, with no public decision. I file that as R909-3-N1 (MINOR), so the verdict is NEGATIVE.
- **Fix path:** R909-3-N1 can be closed by a public decision alone. No source change is needed for that option.

## Delta scope (proved)

From `receipts/delta_scope.txt`:

- 18 files changed: Markdown under `docs/` and three Markdown files under `hdl/`, two `scripts/` modules, and the `tb/verilator/input_loopback{,_dp}` and `render_queue/mutants.py` test files.
- Filtering for `.sv/.v/.svh/.vh/.c/.h/.xdc/.tcl/.ld/.mk/.yml/.yaml`, `.github/`, firmware, `sw/`, Makefiles and `.gitmodules` returns NONE. There are no gitlink changes.
- The six gitlinks at the head are unchanged.
- Tree identity: `sw` is `374e7a0c` and `configs` is `645784f4` at both heads. Between `hdl` trees `115838d1` (prior head) and `aefab080` (this head), only the three Markdown files differ.
- The 8x8 route started from those exact prior-head trees, which are byte-identical to this head outside Markdown (author `source-binding.json.txt`).
- So the RTL, firmware, config, submodule and workflow bytes are unchanged. The round-4 disabled-identity hashes (1x1 `18af89e6...`, 8x8 `fe344bba...`) and the equal disabled utilization carry over by construction.

## Packet verification

From `receipts/packet_verify.txt` and `scripts/verify_packet.py`:

- **Publication manifest:** all 438 `author-r5` files match the published SHA256 in `review-evidence/loopbram-r1/MANIFEST.json`.
- **Author manifests:** of the 426 author `manifest-*.jsonl` entries, 369 match byte for byte. The other 57 are exactly the files that `MANIFEST.json` marks `path_redacted: true`, and for every one of them the manager's `original_sha256` equals the author's recorded hash. The packet is therefore internally consistent.
- **Signature:** the evidence commit carries no Git signature (`%G?` = `N`). Integrity here rests on the content hashes, not on signer authentication.

## Findings

### R909-3-N1 - MINOR - Tests, Docs - new suites registered with non-provisional, non-hosted figures, against the planner's own new-suite contract and with no recorded decision

- **Where:**
  - `scripts/suite_shards.py:111-112` (`"input_loopback": 38`, `"input_loopback_dp": 107`).
  - `scripts/suite_shards.py:148-151` (`PROVISIONAL_SUITES` still `{"reboot_ctrl"}`).
  - `docs/testing/TESTING.md:441-445`.
- **Authority:**
  - The `scripts/suite_shards.py:15-17` docstring: "Until a hosted window is measured, register the exact run_all_suites.sh timeout as a provisional estimate; the selftest checks that value against the driver."
  - The same steps are repeated in `table_problems()` (`:236-243`): "record suite_timeout's figure for it as provisional, add a worker if one is then predicted over ... and replace the figure from the change's own hosted run".
  - `docs/testing/TESTING.md:643-645`: "a change that adds a suite first records a provisional figure for it, by the new-suite steps".
  - The `gptp_tables` precedent in `docs/testing/CI_WORKFLOWS.md:525-534` followed those steps.
  - R909-2-N1's required outcome: "following the docstring's new-suite steps: a provisional `suite_timeout` figure".
  - AGENTS.md section 2: where documentation and implementation conflict, publish the conflict and get a decision "rather than choosing an interpretation".
- **Evidence:**
  - The author chose local cold runs on four pinned CPUs, scaled by 1.58 (23.8 s and 67.7 s give 38 and 107, which I confirmed from `measure--*.time.txt`). The figures are not marked provisional.
  - The packet gives the reason: `PROVISIONAL_SUITES` "requires the suite_timeout figure rather than a measurement".
  - The cited `ship8` precedent (`TESTING.md:435-439`) is a leg figure in `PIECE_SECONDS` for an already registered parent, not a new suite in `SUITE_SECONDS`.
  - `TESTING.md:412` records that the same 1.58 factor under-projected `follow_ring` (actual ratio 1.78).
  - No public comment on #979 or #987 rules on the deviation. I searched both threads for "provisional", "SUITE_SECONDS" and "sweep".
  - The head now states both the rule (`TESTING.md:644`, the docstring) and an unratified exception (`TESTING.md:441-445`).
- **Impact:**
  - The figure that sets shard placement departs from the stated contract without a decision.
  - Two methods now coexist in the authority, so the next new suite cannot tell which applies.
  - The practical overrun risk is low: workers 15 and 16 are predicted at 1508 and 1507 s against a 1620 s bound under a 2700 s job limit. Even a doubled hosted window for `input_loopback_dp` (214 s) keeps worker 15 at 1615 s or less.
  - It is not wording only, because it decides a registered figure. Under the owner's rule it is therefore MINOR, not RESIDUE.
- **Required outcome (either one):**
  - (a) Follow the docstring's steps: register both at the driver's `suite_timeout` figure in `PROVISIONAL_SUITES`, add a worker if the self-test then requires one, and replace the figures from this change's own hosted run.
  - (b) Publish a maintainer or manager decision on #979 or #987 that accepts the measured cold-run x1.58 figures for these two suites in place of the provisional figure. The `TESTING.md:644` / docstring wording would then go to the residue checklist, or get a one-line note citing the decision.
- **Verification:**
  - For (a), the self-test prints the provisional figures as matching `suite_timeout` and exits 0, with all 19 listings at exit 0.
  - For (b), the public decision link.

### R909-3-S1 - SUGGESTION - Tests - `tb/verilator/input_loopback_dp/sim_main.cpp:44-45, 609` - the completeness bound has zero headroom

- In every clean run, the peak backlog equals the bound exactly: 48 for every stream, in both phases, at both shapes (`receipts/run_dp.txt`). So `WIRE_STREAM_COMPLETE` also asserts, implicitly, that each stream's packet leaves before the next frame's capture, meaning talker latency is under one media frame.
- That is a sound property, but a legitimate change to transmit scheduling could trip it without a delivery defect.
- Suggested change: state that latency meaning in the comment at `:42-45` and the README, or bound the backlog at one packet plus one event (`kWireTail + kChans`) and keep the delivery check as the absence detector.

### R909-3-S2 - SUGGESTION - Robustness, Tests - `tb/verilator/input_loopback_dp/sim_main.cpp:639, 747` - unbounded waits now that the host deadline is removed

- `while(!((...cmap_walk_ns_w >> 39) & 1)) step();` has no cycle cap.
- The delta removed `timeout=7200`/`1800`/`3600` from `mutants.py`, `bounds.py` and `run.py` under the host-deadline ratchet, saying the sweep guard bounds them.
- That guard covers `make -C` suite runs. It does not cover the explicit campaigns registered at `TESTING.md:353-354`, which run outside the sweep.
- A future plant that stops the capture walk would hang a campaign instead of failing it. That is a stall, not a false pass, so this is not a defect today.
- Suggested change: cap both waits and fail a named check (for example `WALK_CLAIM_DEADLINE`). The harness then bounds itself, which is the form the ratchet asks for.

### R909-3-S3 - SUGGESTION - Docs - `docs/design/INPUT_MAPPED_LOOPBACK.md:65-71`

- The placement sensitivity of the enabled 8x8 route is recorded in the PR body (`:50-54`) and the receipts, which is enough for #818. #818 judges a route set, and the set meets the floor.
- One line under "Implementation status" would keep it findable after merge. It should say that at the reviewed RTL only one of the three directives meets the floor (+0.223 ns, with the other two at +0.008 and +0.003 ns), that the worst paths are in `KL_mbx` on the 100 MHz system clock, not in the loopback logic, and that LUT is 48901.
- My judgment is that this is not owed: the enabled shape is default-off, its product allocation is refused as S14 debt, and the disabled images are unchanged.

No RESIDUE. The comment-rule scan of every added line under `scripts/` and `tb/` finds no lane labels, review rounds, reviewer IDs or issue-comment IDs (`receipts/comment_rule_scan.txt`). The new design-page contents list and README text match their sections; I checked each description against its section's text.

## Prior findings: disposition at this head (read after my own pass)

| Finding | Disposition | Evidence at this head |
|---|---|---|
| R909-2-N1 BLOCKER (suites not in `SUITE_SECONDS`) | **RESOLVED at cause**. Method part retained as R909-3-N1. Complete local sweep not run: see pending duties | I re-ran `suite_shards.py --selftest`: `selftest: PASS`, exit 0 (`receipts/planner_selftest.txt`). `run_all_suites.sh --ci-pieces --shard i/19 --list`: 19 of 19 exit 0, `input_loopback_dp` only in 15/19 and `input_loopback` only in 16/19 (`receipts/shard_listings.txt`). Author plan (`measure--shard-plan.txt.txt`): maximum worker 0 at 1615 s against a 1620 s bound, with a regular job limit of 2700 s; 1615 s is also under 30 minutes. The author's driver runs of shards 15 and 16 (`gates--sweep-shard1{5,6}.log.txt`) pass 8/8 and 9/9 with 662439 and 356128 checks and complete accounting. I re-ran the leaf suite and passed its log through `scripts/suite_tally.py`: 155604 checks in 2 tallies. The old `checks=N` shape gives "INCOMPLETE", exit 1, and a planted `FAIL ... 1 failures` line is refused by `--verdict`, exit 1 (`receipts/tally_probe.txt`). |
| R910-2-F1 MAJOR (a missing output passes) | **RESOLVED** | Per-stream `WIRE_STREAM_DELIVERY` (16 or more packets, at least one word captured, delivered no less than captured minus 48) and `WIRE_STREAM_COMPLETE` (tail and peak backlog no more than 48) run in both phases (`sim_main.cpp:601-615`, called at `:618` and `:647`). No `check.` line was removed (diff grep, rc 1). Clean runs I made: 1x1 16173/0, 8x8 122549/0 (`receipts/run_dp.txt`). The external reviewer's exact plant `& N_STREAMS'(8'h7f)` builds and fails exactly `WIRE_STREAM_{DELIVERY,COMPLETE} {edits,clipped} stream 7`: 113837 checks, 4 failures, captured 3088/1160, delivered 0 (`receipts/run_whole7.txt`). My phase-only plants (`scripts/plant_phase.py`, `receipts/plant_phase*.diff`): at 8x8, stream 3 held off in the edit phase only and stream 5 in the clipped phase only fail exactly `edits stream 3` and `clipped stream 5`, while stream 3 recovers and passes in the clipped phase (`receipts/run_phase8.txt`). At 1x1, a clipped-only hold fails `clipped stream 0` (plus the existing `CLIPPED_WIRE_TRANSMITS`) while its edit phase passes (`receipts/run_phase1.txt`). The author's campaign results show 17 of 17 passing, the nine output plants are at each 8x8 talker and the 1x1 talker, and every plant must build and fail all four named tags (`gates--parent-plants--results.json.txt`, `mutants.py:41-47, 68-69`). |
| R909-2-N2 MINOR / R910-2-F2 MAJOR (enabled 8x8 route) | **RESOLVED** | Raw `Design Timing Summary` of all 12 corner reports (`receipts/route_corners.txt`): ExtraPostPlacementOpt +0.008/+0.036; **AltSpreadLogic_high +0.223 (Slow) / +1.436 (Fast) setup, +0.102 / +0.036 hold**; ExtraTimingOpt +0.003/+0.036. Zero failing endpoints and zero routing errors throughout. The best directive meets #818 (+0.030 setup, 0 hold) at every corner. The worst setup paths are all `KL_mbx` on `milansoc_crg_clkout0`, with 76-81% route delay (`receipts/route_worst_paths.txt`). Utilization is LUT 48901, FF 54672, BRAM tiles 111 (RAMB36 94, RAMB18 34), DSP 11. The 70.5-tile control memory (ROM 39 RAMB36 plus 1 RAMB18, SRAM 31 RAMB36) is refused by the product allocator. It is recorded as S14 debt, 11.5 tiles over the 59 ledger (`firmware-memory.json.txt`), per the owner rule. The 1x1 route at `dc78aeda` stands for byte-identical RTL. |
| R909-2-N3 MINOR (campaign registry) | **RESOLVED** | `docs/testing/TESTING.md:354` names `make -C tb/verilator/input_loopback_dp` and `mutants.py --output`, triggered by the map writers, `g_input_invalidation`, the talker enable, the packed fields, the harness and the campaign. |
| R909-2-R1 RESIDUE | **RESOLVED** | `tb/verilator/input_loopback/README.md:17-18` carries the exact fix. |
| R909-2-S1 (1x1 connection plants) | **ADOPTED** | `mutants.py:32, 34`. |
| R909-2-S2 (hash reproducibility) | **ADDRESSED** by statement in the packet | No change was needed at this head. |
| R909-2-S3, S4 | Not adopted. Both remain optional | S4 would touch RTL and reopen the identity proof. I agree with not adopting it in this lane. |
| Author-fixed gates (seven) | **VERIFIED** where I could run them | `check_py_idiom.py` and `check_cpp_idiom.py` (0 multi-declarators) give rc 0. So do `measure_test_evidence_readers.py --check`, `gen_module_matrix.py --check` (84 modules) and `docs_inventory.py --check` (fresh). `docs_check.py` reports 0 findings across 226 pages, and `check_doc_paths.py`, `check_doc_style.py` and the leaf tally fix pass too (`receipts/doc_gates.txt`, `receipts/idiom_tally_gates.txt`). `gen_toc.py` and `check_em_dash.py` need the pinned Markdown renderer, which is not installed here, so for those two I rely on the author's 43-step docs workflow replay (all exits 0, lane clean after every step) and the `gates--em-dash.log.txt` result of 0 findings over 638 added lines. The leaf's bounded `strtol` refuses `abc`, `12x`, empty and `7.5` with exit 2, and `0` passes (`receipts/env_int_probe.txt`). |

## Lens results (artifact-specific)

```text
[R909] PASS Conformance - issue #979 acceptance (Area, Routing, End-to-end, Behind a build option) against author-r5 route-summary/corner reports, firmware-memory.json, source-binding.json and receipts/delta_scope.txt; tb/verilator/input_loopback_dp/sim_main.cpp:601-647 against the "received audio re-transmitted by a talker" criterion and design doc :372 - both shapes routed at the #818 floor on identical RTL (8x8 best +0.223/+0.036, 1x1 +0.124/+0.036); every output stream's delivery graded; disabled images unchanged by construction; S14 debt per owner rule
[R909] PASS RTL - receipts/delta_scope.txt (no .sv/.v byte, hdl tree aefab080 vs 115838d1 differs in 3 Markdown files only); receipts/route_corners.txt and route_worst_paths.txt - no RTL changed, so the R909-2 RTL verdict stands; its only open item (N2, exact-head route) is now met; worst paths are outside the loopback logic; S4 remains a suggestion
[R909] PASS Robustness - tb/verilator/input_loopback_dp/sim_main.cpp:594-647 (phase reset, queue clear at :637 before begin_phase :640); tb/verilator/input_loopback/sim_main.cpp:21-31 (env_int) - phase-only plants show independent per-phase grading; malformed controls refuse with exit 2; timeout removal yields a hang not a false pass (S2)
[R909] MINOR Tests, Docs - scripts/suite_shards.py:111-112, 148-151; docs/testing/TESTING.md:441-445 vs :643-645 and the :15-17 docstring - R909-3-N1
[R909] MINOR Docs - (same finding, R909-3-N1; the remaining Docs artifacts checked clean: INPUT_MAPPED_LOOPBACK.md contents list and :372, both READMEs, TESTING.md:354, DOCUMENTATION_AUDIT.md / MODULE_MATRIX.md / README-tests.md regeneration via their --check gates, PR body :36-59 against receipts)
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #979 acceptance and option-B ruling. Author-r5 route summary, all 12 corner reports, route status, firmware-memory and source-binding receipts. `sim_main.cpp:601-647`. Design doc `:65-71, 372`. `receipts/delta_scope.txt` | R909-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |
| RTL | CLEAN | `receipts/delta_scope.txt` (`hdl` tree identity apart from 3 Markdown files, no `.sv/.v` change). Route corners and worst paths. The R909-2 RTL artifacts (`KL_render_queue.sv:776-939`, `KL_chan_map_capture.sv:1376-1426`, `milan_datapath.sv` enabled branch) are unchanged since `dc78aeda` | R909-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |
| Robustness | CLEAN | `input_loopback_dp/sim_main.cpp:594-647, 639, 747`. `input_loopback/sim_main.cpp:21-31`. Phase-only plants. `env_int` probe | R909-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |
| Tests | UNCLEAN (R909-3-N1) | `scripts/suite_shards.py` (self-test, listings, `:15-17, 111-112, 148-151, 236-243`). `input_loopback_dp/{sim_main.cpp,mutants.py,run.py}`. `input_loopback/{sim_main.cpp,bounds.py,mutants.py}`. `render_queue/mutants.py:145-146`. `suite_tally.py` probe. My clean, talker-7 and phase-only runs | R909-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |
| Docs | UNCLEAN (R909-3-N1) | `docs/testing/TESTING.md:354, 441-445, 643-645`. `docs/design/INPUT_MAPPED_LOOPBACK.md` (contents list, `:65-71, 372`). Both READMEs. `README-parameters.md` contents list. Regenerated inventories (by `--check`). PR body | R909-3 | 9acb9b828b29aba71bd51303a4836f86c2278267 |

## Commands and receipts (listed in MANIFEST.sha256)

- **Packet integrity:** `python3 -I scripts/verify_packet.py <extracted review-evidence/loopbram-r1>` gives `receipts/packet_verify.txt`.
- **Route corners:** `sh scripts/route_corners.sh <author-r5/receipts>` gives `receipts/route_corners.txt`. `receipts/route_worst_paths.txt` holds the worst `clkout0` path of each recipe.
- **Delta scope:** `receipts/delta_scope.txt`.
- **Planner:** `python3 scripts/suite_shards.py --selftest` and `scripts/run_all_suites.sh --ci-pieces --shard i/19 --list` for i = 0..18 give `receipts/planner_selftest.txt` and `receipts/shard_listings.txt`.
- **Suite runs:** made with pinned Verilator 5.050 (wrapper verified as `Verilator 5.050 2026-07-01 rev v5.050`) and `VERILATOR_JOBS` 3-4, run concurrently:
  - `make -C tb/verilator/input_loopback MDIR=<scratch>` gives `receipts/run_leaf.txt`;
  - `make -C tb/verilator/input_loopback_dp WORK=<scratch>` gives `receipts/run_dp.txt`;
  - `run.py --shape 8 --dp-source <plant>` gives `run_whole7.txt` and `run_phase8.txt`;
  - `run.py --shape 1 --dp-source <plant>` gives `run_phase1.txt`.
- **Plants:** `scripts/plant_phase.py` produced `receipts/plant_{whole7,phase8,phase1}.diff`. These were disposable copies outside the clone.
- **Gates and probes:** `receipts/doc_gates.txt`, `receipts/idiom_tally_gates.txt`, `receipts/tally_probe.txt`, `receipts/env_int_probe.txt` and `receipts/comment_rule_scan.txt`.
- **Clone restoration:** `receipts/restore_check.txt`.
  - HEAD and tree are as stated, the index tree equals `fd76b361`, and the worktree and index equal HEAD in content and mode.
  - There are 0 untracked or ignored entries after I removed the caches this review created.
  - The six gitlinks are unchanged and the initialized submodules are clean.
  - The `external` submodule was already uninitialized in this clone, at its recorded gitlink.

## Real limits

- **No complete serial sweep.** I did not run the complete serial sweep, or the parent, PP, gPTP, Yosys or builder banks (not allowed). The sweep evidence is the author's shards 15 and 16 plus my listings, self-test and the two new suites.
- **No route of my own.** I ran no route. The route figures are the author's, and I re-read them from the raw reports.
- **Two docs gates not run here.** `gen_toc.py` and `check_em_dash.py` could not run without the pinned Markdown renderer, so I rely on the author's docs-workflow replay for those two.
- **Hosted evidence is incomplete.** At review time, the exact-head hosted runs were in progress or queued: 19 Verilator shards, firmware and Yosys jobs. `wire-accountability`, `verilator-lint`, `full-ci-gate` and `elaborate-gates-0/2/3` had completed successfully, and the physical gPTP context was skipped. I make no hosted, act or manager source-bank claim.
- **The packet is unsigned.** Integrity is by content hash only.
- **Not hardware proof.** Physical calibration was NOT RUN, the builder union's one calibration row is NOT RUN, and skipped field contexts are not hardware proof.

## Pending manager duties

- **R909-3-N1:** obtain and publish the decision (outcome b), or return the lane for outcome (a).
- **Complete-sweep evidence:** CONTRIBUTING section 2.1 and AGENTS section 7 require it before merge. It has not been run at this head. The act replica's Verilator workflow (all 19 shards) and the hosted `verilator-suites` aggregate at the final head cover it, and the merge-turn native bank covers the candidate. This ledger does not substitute for it.
- **Hosted and act acceptance:** `rtl-fast`, `verilator-suites` and `yosys-portability` at the final head.
- **Candidate-merge validation:** source base `3cda030c17`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, with the builder and native banks at the merge turn.
- **Hosted windows:** the hosted windows for `input_loopback` and `input_loopback_dp` are owed by the first hosted run that carries them (`TESTING.md:445`).
- **S14 debt:** the enabled 8x8 control memory (70.5 tiles) remains open S14 debt under the owner rule.
- **Suggestions:** carry R909-3-S1, S2 and S3 as optional.

R909-3 FINISHED

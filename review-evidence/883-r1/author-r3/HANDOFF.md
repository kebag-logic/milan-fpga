# HANDOFF: [A768], issue #883, seventh parent pin adoption

**Outcome: REVIEW READY** at `3c58b143eac812d173b4326423c030b65ec63f9a` (round 3: F1 and two residues, section 00), under the manager's ruling on the STOP (#883 issuecomment-6805166676, `[A10]`, option (b)): the processor gitlink moves to `801ef228`; `gptp-processor` stays at `1616fc8f` through a revert commit; FPGA-gPTP PR #103 rides with the next adoption.

- Lane `883-adopt-processor-801ef228`, from dev `46c971fa`. Live `origin/dev` is `fa6c094b` (PR #875: `scripts/act_ci.py`, `docs/testing/CI_WORKFLOWS.md`; no file in common with this lane; `git merge-tree` clean). Origin `https://github.com/kebag-logic/milan-fpga.git`.
- Final head `3c58b143eac812d173b4326423c030b65ec63f9a`: 18 commits, each a one-line subject, no body, no trailer, none rewritten. Nothing pushed.
- Processor `044cb25f` -> `801ef2283ec793e35a2590fc6593c90313a64041` (processor #216 via PR #218, merged `45f03e04`; #217 via PR #219, merged `801ef228`), a fast-forward on the donor's `main`.
- FPGA-gPTP: `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, dev's pin. `4bf3eb72` moved it to `a64be73d`; `8edfae99` reverts that move in a new commit.
- Comments: TAKEN issuecomment-6793519648; STOP issuecomment-6802822181 (text `STOP-COMMENT.md`); REVIEW READY issuecomment-6806761644 at `e18c8225` (text `REVIEW-READY-COMMENT-e18c8225.md`); round 3's REVIEW READY issuecomment-6810008166 at `3c58b143` (text `REVIEW-READY-COMMENT.md`). Each posted once.
- Output files: `PR-BODY.md` (the PR body, template order), `STOP-COMMENT.md`, `REVIEW-READY-COMMENT.md`, `receipts/` (index `receipts/INDEX.md`, generated from the files present).

## 00. Round 3, after the ruling on the delta reviews

The ruling (#883 issuecomment-6809058443, `[A10]`) on R831-1 and R832-1, both NEGATIVE on the same MINOR at `e18c8225`: fix F1 with selftest arms, take two residues, run `check_cpp_idiom.py --selftest`, the docs gates and `git diff --check` on a clean clone, then REVIEW READY. No image, RTL, firmware or pin change.

| Commit | Change |
|---|---|
| `8f3735d7` | **F1.** `scripts/check_cpp_idiom.py:269-271`: `_DECL_TEXT` reads a balanced one-line `{...}` initialiser up to three braces deep as one declarator's text (it read only flat braces, so a line with a nested initialiser matched nothing and a second declarator beside it escaped). The comment states that limit. Arms `:705-712`: one declarator with flat, once-nested and twice-nested braces gives 0; two declarators beside flat, `{1}`-style, once-nested (either order) and twice-nested braces give 1. The file stays at 1,000 lines (the Python idiom gate's module limit): three wrapped arms in the same function (`:699-700`, `:726-727`, `:737-738`) are joined onto one line each, every line within 120 columns |
| `3c58b143` | **Residue R2 (= R832-1 R1).** `docs/testing/TESTING.md:357`: "the three gate mutants" -> "the six gate mutants", #495 row 6731336971 item 2's exact text; the Makefile (`:665`) and README (`:617`) already say six |
| PR body | **Residue R831-1 R1.** The #495 table row 6731336971 now states its four items: item 3 (Makefile) and item 2 (`TESTING.md:357`) taken; item 1 (`SUBMODULES.md:813`) open on #495; item 4's note is rewritten here but keeps the form, now "+29 slices (80)" at `syn/ooc/pp_resource_baseline.json:451` (R832-1 R2, not in the ruling), so it stays open on #495 |

Evidence at `3c58b143` (clean clone; receipts under `receipts/misc/` and `receipts/mutant-cppidiom-f1/`):
- `python3 scripts/check_cpp_idiom.py --selftest`: 83 / 83, rc 0 (78 at `e18c8225`); the tree scan `multi-declarator declaration: 0 <= 0` (`cpp-idiom-3c58b143.txt`).
- Planted controls, each one line replaced in the clean clone and restored (`mutant-cppidiom-f1/SUMMARY.txt`): dev `46c971fa`'s `MULTI_DECL_RE` fails the three "a brace initialiser's commas separate elements, not declarators (#495)" arms (80 / 83); `e18c8225`'s flat-brace `_DECL_TEXT` fails the three nested two-declarator arms (80 / 83); a one-nested-level `_DECL_TEXT` fails the three-deep two-declarator arm (82 / 83).
- The reviewers' probes, unchanged, with `-I` (`f1-reviewer-probes-3c58b143.txt`): R832-1's `probe_cpp_multidecl.py` gives the head verdict `real>1` on all nine rows; R831-1's `probe_cpp_edges.py` prints 1 for `int a[2][2] = {{1, 2}, {3, 4}}, b = 0;` and 0 for its single-declarator form; R831-1's `probe_cpp_old_regex.py --selftest` fails the three brace-initialiser arms by name. One probe row, `int a = f(1, 2), b;`, reads 0 at this head and at dev alike: both patterns exclude parentheses by design (`:263-264`, so `f(a, b);` is never a declaration). Not F1, and not changed here.
- `git diff --check 46c971fa HEAD`: rc 0 (`diff-check-3c58b143.log`).
- docs.yml, all five jobs, on the merge commit with live dev `fa6c094b`: 64 steps rc 0, 33 not run with a reason, 0 failing (`receipts/gates-3c58b143/`, `verify-docs-3c58b143.txt`).
- The two changed files are read only by docs.yml steps: `check_cpp_idiom.py` is named in no other workflow, and `TESTING.md` appears in the scripts other workflows run only as comments. So every other gate stands from section 5.

## 0. This round, after the ruling

| Commit | Change |
|---|---|
| `8edfae99` | `gptp-processor` gitlink `a64be73d` -> `1616fc8f` (the ruling's revert; `4bf3eb72`'s processor half stands) |
| `f746d659` | The gPTP pin-derived records back at `1616fc8f`, each through its generator: `scripts/check_submodule_docs.py` pin row and links, `docs/diagrams/submodule_boundaries.gen.py`, `docs/diagrams/timesync_chain.gen.py`, `scripts/check_gptp_docs.py --with-submodule` donor links, `scripts/check_diagram_pngs.py` manifest. Every gPTP-only page and the time-sync diagram are byte-identical to dev `46c971fa`'s; the boundary diagram differs from dev's only in the processor pin. `bash syn/yosys/ooc.sh --record-rom-digests` leaves `syn/yosys/rom_digests.tsv` unchanged (finding 4) |
| `e18c8225` | The wording: item 1 as the ruling gives it on `CHANGELOG.md`, `docs/reference/SUBMODULES.md` (#883 block; the FPGA-gPTP #102 row removed; the leg table's new-pin column now `801ef228`, `1616fc8f`), `docs/design/AREA_BUDGET.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` (heading `Re-baseline of 2026-11-11, processor 801ef228`, contents through `gen_toc.py --write` and its description written), and the three records' `measured` notes in `syn/ooc/pp_resource_baseline.json` (notes only; `set_measured.py` refuses any other difference) |

**The resource record holds at the final pins.** It was measured at `a89802c8`, whose tree carried gPTP `a64be73d`. An export at `f746d659` (gPTP `1616fc8f`) reads the same 131 files and six ROM images through the gate's own `located()` normalisation; the one file whose digest differs, the generated `alinx_ax7101.v`, differs only inside its `/* */` hierarchy comment (lines 76 to 922), where the same black-box lines appear in another order. So the gate's `inputs_sha256` of that export is `805d2a0c...` against the record's `0c7a1ee8...` while every byte Vivado reads is equal (`receipts/misc/route-input-digest.txt`, `receipts/scripts/digest_diag.py`). No re-route was needed. The cause is pre-existing (finding 5).

## 1. Acceptance items

| Item | State | Evidence |
|---|---|---|
| 1. The processor gitlink moves to `801ef228` (the ruling's wording); a fast-forward of `044cb25f` on the donor's `main` | met | `receipts/misc/fast-forward.txt`; `git ls-tree HEAD gptp-processor` is `1616fc8f`, dev's pin |
| 2. Parent changes each PR needs, #495 dispositions and rows, each changed check with its planted mutant | met | sections 2 and 3; the #851 control fix |
| 3. #857/#860 (802.1Q-2018 10.7.9, 10.7.7, Table 10-3, Milan v1.2 MVRP) and #858 (1722.1-2021 7.2.1, available_index), each with a parent test at the AX7101 1x1 shape that fails at the old pins | met | at `e18c8225`: crflic 458 / 0, notify 535 / 0; old pins: 7 and 4 failures |
| 4. AX7101 route at every corner, +0.030 ns floor on the best of the three #818 directives; LUT/FF/slice deltas against `46c971fa` under NFR-RES-01 | met | section 4; the record holds at the final pins (section 0) |
| 5. Every gate a PR to `dev` triggers, on a clean clone of the final head | met under the ruling | section 5: the gates the revert touches re-run at `e18c8225`, every step rc 0; the rest stand from `f58347df` and `6c6706e5`, whose inputs they read are unchanged |

## 2. Changes (file:line, clause)

| Change | Where | Clause |
|---|---|---|
| processor gitlink | `protocol-processor` (`4bf3eb72`); `gptp-processor` moved there and reverted in `8edfae99` | #883 item 1, the ruling |
| ROM digests (generator `syn/yosys/ooc.sh --record-rom-digests`) | `syn/yosys/rom_digests.tsv` rows `801ef228` ucode/ltn (`a89802c8`); the `a64be73d` gptp row stays (finding 4) | pin record |
| pin table, boundary and time-sync diagrams (generators), gPTP donor links | `docs/reference/SUBMODULES.md:24-25`, `docs/diagrams/submodule_boundaries.*`, `timesync_chain.*`, `PNG_MANIFEST.json`, the gPTP pages (`a89802c8`, back at `1616fc8f` in `f746d659`) | pin record |
| crflic `[MRPAPP]` | `tb/verilator/milan_dp/sim_crf_licence.cpp:929` `grade_first_messages`, `:955` `grade_mrp_applicant`, recording in the `[ONEVEC]` walk `:874-893` | 802.1Q-2018 Table 10-3 (VN/AN tx! sN, note 8), 10.7.6.3 |
| crflic `[MVRPLA]` | `sim_crf_licence.cpp:991` `grade_leave_all_gaps`, `:1035` `phase_nothing_declared`, run after `[E]` `:1681` | 802.1Q-2018 10.7.9, Table 10-5; Milan v1.2 Table 4.3 |
| notify `[AIDX]` | `tb/verilator/milan_dp/sim_nxn.cpp:2092` ADP capture in `gsi_tx_frame`, `:3036` `aidx_read_entity`, `:3053` `aidx_grade`, `:3073` the section, `:3506` its call | 1722.1-2021 Table 7-2, 6.2.2.15; Milan v1.2 5.6.3.5.2/.5/.9 (the 10 s wait bound) |
| crflic-mutants arms | `tb/verilator/milan_dp/crflic_mutants.py:144-178` (multi-edit arms, `run_pp_mutant`) | #216's own arms; #851's now both layers |
| gsi-mutants arms | `tb/verilator/milan_dp/gsi_mutants.py:91` `PP_FILES`, `:234-246` | #217's own arms |
| #495 row 6758088112 | `scripts/check_cpp_idiom.py:270-271`, arms `:706-710` | the C++ idiom gate's ES.10 rule |
| campaign comments (and #495 row 6731336971's line) | `tb/verilator/milan_dp/Makefile:664-671`, `:682-683` | - |
| docs | compliance matrix rows 4.2.7.1, 4.2.7.3/4.4.1, 5.4.2.4; 802.1Q traceability MRP-3, MRP-5; `docs/testing/TESTING.md:357-358`; `tb/verilator/milan_dp/README.md` (leg rows, crflic phase rows, arms rows, the #858 section, contents via `gen_toc.py`) | - |
| resource record | `syn/ooc/pp_resource_baseline.json` via `pp_resource_gate.py record --write` (`93d371cb`), notes via `set_measured.py` (`93d371cb`, `e18c8225`) | NFR-RES-01; the re-baseline rule |
| area and pin records | `docs/design/AREA_BUDGET.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` (new top section, contents via `gen_toc.py`), `docs/reference/SUBMODULES.md` (#883 block), `CHANGELOG.md` (`f58347df`, `e18c8225`) | - |

## 3. New checks, planted mutants, failing words

| Check | Planted mutant | Failing words |
|---|---|---|
| `[MRPAPP]` Domain message 2 | `KL_srp_domain.sv`: LINK_UP enters AN | `MSRP Domain {class A, 3, VID 2}: message 2 is New again (AN tx!: sN)` |
| `[MRPAPP]` VID 2 message 2 | `KL_srp_vlan.sv`: New! row goes to AN | `MVRP VID 2: message 2 is New again (AN tx!: sN)` |
| `[MRPAPP]` no VID JoinIn | `KL_srp_vlan.sv`: Registrar read as IN | `no MVRP JoinIn in the whole run: no VID was ever registered (10.7.6.3)` |
| `[MVRPLA]` MVRP LeaveAll | `KL_srp_encoder.sv`: MVRP drain needs a pending VID | `MVRP, nothing declared: at least two LeaveAll MRPDUs after the withdrawal` |
| `[MVRPLA]` MSRP LeaveAll | `KL_srp_top.sv`: the MSRP leavealltimer expiry lost | `MSRP, the Domain alone: at least two LeaveAll MRPDUs after the withdrawal` |
| `[ONEVEC]` (existing; its control fixed) | `KL_srp_top.sv` intake takes every push twice + `KL_srp_encoder.sv` never merges | `no DUT MRPDU carries one attribute value in two VectorAttributes` (591) |
| `[AIDX]` A1 | `gen_ucode.py` copies the image whole | `[AIDX] A1 after an ENTITY_AVAILABLE: available_index (octets 36..39) is the wire's` (4 of 535) |
| `[AIDX]` A1 | `KL_aecp_engine.sv` gather answers 0 | the same (4 of 535) |
| `[AIDX]` A1 | `KL_adp_engine.sv` serves the next index | the same (5 of 535) |
| `[AIDX]` D | `KL_adp_engine.sv` keeps the index across DEPARTING | `[AIDX] D after ENTITY_DEPARTING: available_index (octets 36..39) is the wire's` (1 of 535) |
| `check_cpp_idiom.py` brace initialiser | the old `MULTI_DECL_RE` restored in a scratch copy | `[FAIL] a brace initialiser's commas separate elements, not declarators (#495)` |
| both legs, the old pins | processor `044cb25f`, gPTP `1616fc8f`, the same harness (scratch clone) | crflic 7 failures (Domain `0 1 1`, VID 2 `0 1 1` and message 3, 185 VID JoinIns, 3 MVRP LeaveAll); notify 4 (A1-A3, R2 read 0) |

Campaigns: `crflic-mutants` 16 / 16 at `6c6706e5`; `gsi-mutants` 19 / 19 at `21fcc20a`; `unb-mutants` 6 / 6 at `cc8ee337`; `dynmap-mutants` 69 / 71 at `f2f3d9f5`, the two its listener leg's precondition (finding 3), then `dynmap_mutants.py 36` 2 / 2 with that suite's inputs built. They build the processor's `hdl/` copy and milan_dp's harness, which no later commit changes; none reads the gPTP tree's `docs/` or `tb/`.

## 4. Resources and timing

Vivado 2026.1, the recipe's flows (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`), single-thread synthesis, `general.maxThreads` 32, at `a89802c8` (synthesis inputs equal the final head's, section 0), three directives from one synthesis checkpoint, default seed.

| Directive | Slow 0/85 C WNS / WHS | Fast 0/85 C WNS / WHS | LUT | FF | Slice (free) | RAMB36/18, DSP |
|---|---|---|---:|---:|---:|---|
| ExtraPostPlacementOpt, selected | +0.334 / +0.045 | +1.350 / +0.017 | 53,461 | 54,971 | 15,849 (1) | 74/27, 15 |
| ExtraTimingOpt | +0.218 / +0.102 | +1.548 / +0.036 | 53,474 | 54,974 | 15,850 (0) | 74/27, 15 |
| AltSpreadLogic_high | +0.162 / +0.104 | +1.488 / +0.039 | 53,494 | 54,976 | 15,850 (0) | 74/27, 15 |

Before (`46c971fa`, = #854's record at `7a19f62b`, no synthesis input between): EPPO 53,534 / 54,850 / 15,820 (30 free), +0.166 / +0.032 ns; ASLH 53,513 / 54,847 / 15,846, +0.147; ETO 53,512 / 54,847 / 15,846, +0.127. Best against best (EPPO both): LUT -73, FF +121, slice +29, RAMB/DSP 0, WNS +0.168, WHS -0.015 ns. Standalone: `ooc-1x1` 25,423 / 21,084 (+214 / +64), `ooc-8x8` 37,276 / 32,192 (+218 / +66). Resource gate against the sixteenth record: PASS at all three; re-recorded (seventeenth); `check-baseline` and `check` exit 0 after, and `check-baseline` again at `e18c8225`. Worst setup path: SoC SDRAM controller, 10 ns clock, all three directives. Run times (host shared): EPPO with synthesis 171.6 min, ASLH 43.6, ETO 65.4, ooc-1x1 43.4, rtl-8x8 3.2, ooc-8x8 124.3; peak 8,540 MB.

## 5. Gate table

**Re-run at the final head `e18c8225`** (the ruling: the gates the revert touches), each on a fresh clean clone, the workflow jobs on the pull_request merge commit `9a803dbe` (live dev `fa6c094b` and the head):

| Gate | Command | rc / result | Receipt |
|---|---|---|---|
| docs.yml, all five jobs | `run_wf.py` per job: `wire-accountability`, `docs-check-no-git`, `docs-gates-0..2` | every step rc 0: `64 steps ran rc 0, 33 not run with a reason, 0 bad` (the same 97 steps as at `f58347df`, where `gate_39` was the one bad); each job's tree clean after | `receipts/gates-e18c8225/`, `receipts/misc/verify-docs-e18c8225.txt` |
| `gate_39`, `python3 scripts/check_py_idiom.py` | in `docs-gates-0`, and on the clean clone | rc 0: `long module: 10 <= 10`, `unannotated public function: 0 <= 0`, `undocumented public function: 0 <= 0` (at `f58347df`: 11, 4, 4, rc 1) | `receipts/gates-e18c8225/logs/docs__docs-gates-0__gate_39.log`, `receipts/misc/py-idiom-final.txt` |
| rtl-fast.yml `yosys-elaboration` | `run_wf.py`; its step reads `syn/ooc/pp_resource_baseline.json` (`pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py`, `check-baseline`), whose notes `e18c8225` changed | every step rc 0: 7 ran rc 0, 3 not run with a reason (two sudo tool installs the host already has pinned, the hosted step record); `baseline PASS: 3 endpoints`; tree clean after | `receipts/gates-e18c8225/`, `receipts/misc/verify-yosys-elab-e18c8225.txt` |
| The gPTP consumer legs, 11 suites, each its own unit, the sweep's environment and wall clocks | `make -C tb/verilator/<suite>`, then `python3 scripts/suite_tally.py <logs> --quiet --expect-suite-root tb/verilator` | every `make` rc 0 and every log's `suite_tally.py --verdict` rc 0; 11 / 11 suites, 40,591 checks, 0 failures, 0 timed out; milan_dp's 19 legs `RESULT: PASS` among them, gptp and gptp-lat `212 checks: 212 PASS, 0 FAIL` each, crflic `checks: 458 failures: 0`, notify `checks: 535 failures: 0`. Each suite's checks, failures and tallies equal the `6c6706e5` sweep's (gPTP `a64be73d`) | `receipts/legs-e18c8225/` (`tally.log`, `compare-sweep.txt`) |
| `git diff --check` against the merge base | `git diff --check 46c971fa HEAD` | rc 0, empty | `receipts/misc/diff-check-final.log` |
| Pin and doc gates, on a clean clone of the head | `check_submodule_docs.py`, `check_gptp_docs.py --with-submodule`, `check_diagram_pngs.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 46c971fa`, `docs_check.py`, `check_doc_paths.py`, `docs_inventory.py --check`, `pp_resource_gate.py check-baseline` | 10 / 10 rc 0 (each also a docs.yml step above) | `receipts/misc/pin-doc-gates-e18c8225.txt` |

The consumer set is read from the builds, not chosen: the suites whose Verilator dependency files (`*__ver.d`, in the `6c6706e5` sweep clones) name a file under `gptp-processor/`, and the suites whose logs name it: capture_coherence, gptp_plane, gptp_shadow, gptp_tables, gptp_txts, milan_dp, milan_dp_gm_steps (builds in `../milan_dp`), milan_dp_mclk, milan_dp_render, pp_shadow, tsn_fuzz (`receipts/misc/revert-scope.txt`).

**Standing from the earlier pass**, because the revert changes only the gPTP tree's `docs/TEST_DEVELOPER.md`, `tb/mutation_jobs_test.py`, `tb/verilator/engine/Makefile` and `mutants.py` (its `hdl/` and `syn/` are equal, `git diff --quiet 1616fc8f a64be73d -- hdl syn` rc 0), and every parent gate that reads a submodule's `docs/` or `tb/` is a docs.yml step (`receipts/misc/revert-scope.txt`):

| Gate | Command | Head | rc / result | Receipt |
|---|---|---|---|---|
| Full sweep, 4 native-shards units (MemoryMax 10G, -j4; capture_coherence's shard on 4 CPUs) | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, then `suite_tally.py` | `6c6706e5` | rc 0 each; 65 / 65 suites, 2,192,633 checks, 0 failures, 0 timed out; tally rc 0 | `receipts/sweep-6c6706e5/` |
| rtl-fast.yml, every `run:` step of its 16 jobs | `run_wf.py` per job, on the merge commit | `f58347df` | every step rc 0 (behave 14 features, 508 scenarios, 2,330 steps; lint `89 <= ratchet 89`; census 0 of 31 rules unproven; the four firmware campaigns PASS) | `receipts/gates-f58347df/` |
| rtl.yml | `full-ci-gate`, `yosys-shards` 0..3 of 4, `yosys-portability` | `f58347df` | every step rc 0; Yosys `expected=61 observed=61 errors=0` | same |
| elaborate.yml | `elaborate-gates-0..4` | `f58347df` | every step rc 0 | same |
| `test_builder.py --require-rv32` | `python3 sw/builder/test_builder.py --require-rv32`, own clone | `f58347df` | rc 0, `ALL GATES PASS EXCEPT 17 NOT RUN` (no LiteX interpreter); with `MILAN_LITEX_PYTHON` rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b: this make does not re-read MAKEFLAGS mid-parse; gate 11: needs a board build's Vivado report) | `receipts/gates-f58347df/logs/builder*` |
| Campaigns | `crflic-mutants`; `gsi-mutants`; `unb-mutants`; `dynmap-mutants`, then `dynmap_mutants.py 36` | `6c6706e5`, `21fcc20a`, `cc8ee337`, `f2f3d9f5` | 16 / 16; 19 / 19; 6 / 6; 69 / 71 (the listener precondition), then 2 / 2 | `receipts/legs/` |
| Resource gate | `pp_resource_gate.py check` (three endpoints), `record --write`, `check-baseline`, `check` | route set at `a89802c8` | check rc 0 at all three against the sixteenth record; after re-record `check-baseline` and `check` rc 0 | `receipts/gate/`, `receipts/vivado/` |
| Old pins | crflic and notify with processor `044cb25f`, gPTP `1616fc8f` | lane tests at `21fcc20a` | 7 and 4 failures, each a new check | `receipts/legs/crflic-old.log`, `notify-old.log` |

## 6. Findings for the manager

1. **The ruling, applied.** Revert by a new commit, no rewrite; the parent ratchet untouched (`scripts/py_idiom.budget` and `scripts/code_quality_scope.py` unchanged from dev; the lane's only `scripts/` change is `check_cpp_idiom.py`). The FPGA-gPTP follow-up under #102 the ruling names: annotate `named_verdict` (`tb/verilator/engine/mutants.py:890`), `run_mutant` (926), `in_list_order` (986), `planted` (1044); document `control` (1041), `planted` (1044), `task` (1045) and `tb/mutation_jobs_test.py` `main` (66); bring `mutants.py` (1080 lines at `a64be73d`) to 1,000 or fewer. #495 row 6777009988 (`docs/TEST_DEVELOPER.md:60`, a fast order check in `make all`) is FPGA-gPTP's and fits the same follow-up.
2. **Fixed in this lane: the #851 `[ONEVEC]` control.** Vacuous at the new pin with either harness; now both layers, caught.
3. **Pre-existing, for its own issue (the ruling): `dynmap-mutants` on a fresh clone.** Suggested text:

   > **`dynmap-mutants`: the listener leg's clean control fails on a fresh clone**
   >
   > On a fresh clone, `make -C tb/verilator/milan_dp dynmap-mutants` reports `71 checks: 69 PASS, 2 FAIL`: `[FAIL] the unmutated gateware does NOT pass the listener leg (caught) - its mutant results are meaningless`, and the listener arm "an empty reset, under the listener's end-to-end check" `failed, but not the named check`.
   >
   > Cause: `tb/verilator/milan_dp/dynmap_mutants.py:113-115` builds the listener leg in `tb/verilator/milan_dp_render` (`tdm8render-build`) with `ltn_rom.hex`, `ucode.hex` and `tdm8r_aemi.bin` marked as inputs the build may not remake (`make -o`). The `dynmap-mutants` target (`tb/verilator/milan_dp/Makefile:717`) prepares only milan_dp's own `dynmap maprec8 maprec4`. Where `milan_dp_render` was never built, those three inputs are absent and the clean control runs without them.
   >
   > Evidence that only the precondition fails: with `milan_dp_render` built, the leg passes 263 / 263 standalone, and `python3 dynmap_mutants.py 36` reads `2 checks: 2 PASS` (the arm caught: 8 failures across 261 checks). The other 69 checks pass. Neither the campaign nor `milan_dp_render` changed in #883.
   >
   > Acceptance: on a fresh clone the campaign either prepares every input it marks with `-o`, or refuses before its clean controls, naming the missing input; a self-check removes the listener's inputs and shows which. The campaign reads 71 / 71 on a fresh clone.

4. **The ROM ledger keeps an `a64be73d` row.** `syn/yosys/rom_digests.tsv:66`, `a64be73de32f... gptp_ucode.hex e83709d9...`, added at `a89802c8`. The generator rewrites only the current pins' rows and keeps every other pin's (`syn/yosys/ooc.sh:500-513`: a dropped row would read to a bump's reviewer as "a deliberate prune"), so re-recording at `1616fc8f` leaves it, and removing it by hand would edit a generated file. The row is true (`a64be73d`'s `gptp_ucode.hex` digest, equal to the `1616fc8f` row's); the next gPTP adoption records its own pin's row beside it.
5. **Pre-existing, for a new issue: the resource gate's input digest depends on a comment's order.** Suggested text:

   > **`pp_resource_gate.py` `inputs()`: the digest varies with the exporter's hierarchy comment**
   >
   > Two AX7101 1x1 exports of the same synthesis sources (#883's `a89802c8` and `f746d659`, whose gPTP pins differ only in `docs/` and `tb/`) give `inputs_sha256` `0c7a1ee8...` and `805d2a0c...`. With the gate's own normalisation the only differing file is the generated `alinx_ax7101.v`, and every difference lies inside its `/* */` hierarchy comment: the same black-box lines in another order. Outside it the file is identical; the 130 other files and the six ROM images match.
   >
   > Cause: `syn/ooc/pp_resource_gate.py:233-238` strips `//` comments from generated files but not block comments. The LiteX hierarchy printer sorts black-box instances by `str(x)` (`litex/gen/fhdl/hierarchy.py:48`); migen's `Instance` defines no `__str__` or `__repr__`, so the key is the default object string with its address, and the order follows object addresses.
   >
   > Impact: a fresh export of an unchanged tree can digest differently, so `inputs_sha256` cannot confirm that a record measures a given tree, and the guard at `pp_resource_gate.py:526` ("identical inputs measured differently") does not fire when it should.
   >
   > Acceptance: the digest ignores comment content of generated files, with selftest arms (two tops that differ only inside a block comment digest equal; tops that differ outside one do not). Changing the digest moves every recorded `inputs_sha256`, so the fix states how the records are carried over under the re-baseline rule.

6. **Shard plan.** No milan_dp case added, so no re-deal (#804). crflic +3.6 M cycles (+20.6 %), notify about +3 M; `PIECE_SECONDS` unchanged until a hosted run re-measures.
7. **Slice margin.** 1 of 15,850 left on the selected route.
8. Not available in this tree: `docs/spec-refs.md` (clauses read from the standards' text) and the two-placement twin (on #665's unmerged branch; its owed rows are deleted by the lane that lands it).

## 7. Process notes

- The host restart cut the round after `f746d659`'s pin checks. Nothing it killed needed repeating: the route-input check was redone at `f746d659`, and the units of this round all ran after it.
- Vivado: only in the earlier pass, through `vivado-slot.sh`, at most two of mine at once; none this round (the record holds, section 0). The `f746d659` export ran LiteX only.
- Units this round, each on a range from `cpu_ranges.py` (`pick`, or `show` for the gate launcher), MemoryMax 10G: `milan-883-a768-gates-docs`, `-gates-fast-yosys`, and `milan-883-a768-leg-<suite>` for the 11 suites, started one after another per chain in three clean clones so that no two share an `obj_*` tree (`receipts/scripts/legs_launcher.py`). Nothing reserved while waiting.
- tsn_fuzz rewrites `hdl/ieee1722/avtp/doc/TEST_RESULTS.md` and `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md` in the tree it runs in, by design ("Do not hand-edit"): only the date line moves (675 pass, 0 fail). The scratch clone that ran it shows those two files modified, as the `6c6706e5` sweep shard that ran it did; nothing of it is in the lane.
- One `fast-yosys` launch at 21:32:56 matched no group in `wf_all.sh` (the group was added a minute later) and ran no job; the relaunch at 21:33:44 is the run reported. Both lines are in `receipts/gates-e18c8225/runner/progress.txt`.
- The workflow replay (`receipts/scripts/run_wf.py`) runs each job's `run:` steps from the workflow file on a fresh clone, on the pull_request merge commit. The earlier pass's runner fixes and invalidated attempts are kept under `receipts/gates-f58347df/attempt1/`; some wrapper rc files of that pass read 2 (`wf_all.sh` edited while it ran), every job's own rc is complete.
- Two of my own scratch processes were killed in the earlier pass while stopping a poll loop (a `pgrep -f` that also matched my shell); no other process was touched.

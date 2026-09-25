[R321] POSITIVE - exact head 4ee96a61bf35402a6f88e1ebad1167e9873721c5

# R321-3: composition review of issue #443 / PR #561 on the merge-train candidate

- Candidate `4ee96a61bf35402a6f88e1ebad1167e9873721c5`, tree `42e0c2ec133cf57a8c5f22069b7f08af39f1fddb`.
- Parents: `ec9cf454bf997fab230d0216dc609e737bc47caa` (C_541, the #541 train candidate) and `b3458db0db5a7c8b15582d80b492620f05f62e70` (PR #561 source head).
- Role: composition independent reviewer, cleared context. Scope: composition acceptance only. The source head already has POSITIVE source reviews R320-2 and R321-2 (at `5beebb7c`) and R320-3 (merge-dev delta at `b3458db0`).
- Reconstruction order: AGENTS.md and CONTRIBUTING.md step 7; the issue body; manager decisions on the issue (item 4, scope, round 2, merge-dev); the diff `ec9cf454..4ee96a61` and history; then this round's own executable evidence. Prior public review findings were read only after the independent pass below and are resolved or retained in their own section.

## Verdict summary

The composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR or MINOR finding is open. Two SUGGESTIONs from earlier rounds are retained unchanged.

1. **The tree is the merge the train will produce.** Real dev `864b36f5` has the same tree as the #508 train candidate `b1b33472`. Merging dev with the #541 head `fa1b5c36` reproduces C_541's tree exactly. Merging that result with `b3458db0` over the single merge base `864b36f5` reproduces the candidate tree `42e0c2ec` exactly. So does a direct merge of `ec9cf454` with `b3458db0`, despite that pair's criss-cross set of four merge bases (`5b73d3f4`, `9d66cfe0`, `8383e929`, `022290e4`). Live remote dev has since moved to `fd9e0ebf` (merged PR #562, the #541 lane). Its parents are `864b36f5` and `fa1b5c36`, and its tree `6cc8996a` equals C_541's. The candidate is therefore also merge(live dev, `b3458db0`). Receipts: `receipts/merge_reconstruction.txt`, `receipts/live_dev_tip.txt`.
2. **Only three paths are shared, and each side's hunks carry over verbatim.** The #443 lane changes 17 paths against dev. The #541 side changes 6. The two sets share `docs/reference/REGISTER_MAP.md`, `docs/testing/TESTING.md` and `scripts/measure_test_evidence.py`. For each shared path, the stable patch-id of #443's change (dev to source) equals the patch-id of the composed change (C_541 to candidate). Likewise the patch-id of #541's change (dev to C_541) equals that of source to candidate. The other 14 #443 paths are byte-identical to the source head. The candidate differs from the reviewed source only in #541's six paths. The one RTL file among those, `hdl/ieee1722/crf/KL_crf_rx.sv`, is identical from `module` to end of file, so the difference sits in the file-header block comment. Receipts: `receipts/overlap_patch_ids.txt`, `receipts/merge_reconstruction.txt`.
3. **The #508 train paths named in the assignment are not a composition seam at this candidate.** These are `TIME_SYNC.md`, `milan_datapath.sv`, `tb/verilator/milan_dp/*`, `sim_tdm8_render.cpp` and the rest. #508 is inside real dev `864b36f5`, which `b3458db0` already merged. R320-3 reviewed that merge. Every such path in the candidate equals its `b3458db0` blob.
4. **The shared registries are consistent.** The four points below are covered in detail under "Composition checks".
   - `DUT_READER_DISPOSITIONS` holds both the #541 `crf_rx/mutants.py` disposition (`measure_test_evidence.py:597-600`) and the #443 `render_csr_controls.py` disposition (`:632-636`). It has 21 keys and no duplicate.
   - `--check` and `--selftest` both pass.
   - The TESTING.md rows match what the suites execute on the candidate.
   - `CRF_CTRL` (`REGISTER_MAP.md:839`) and the `0x8DC` rows (`:242`, `:1825`, `:1957`) coexist, and anchors resolve in both docs_check modes and `gen_toc --verify-anchors`.
5. **The composed suites pass with the source-published counts.** The composed tree builds and passes every suite that reads the shared or neighbouring artifacts. Counts equal the numbers published for the source head.
   - CSR bench: 380/380/115/38/380.
   - `milan_dp` `aclk`: 190/0.
   - `render-csr-controls`: clean 64/0, absent stage 33/0, campaign 4/4, with both named mutants caught.
   - `milan_dp_render`: 152/0, 65/0 and 5/5.
   - `crf_rx`: unit 13836/0, discontinuity 2201/0, talker step 69/0, mutants 10/10, with `validation_error_unlocks` and `validation_error_refreshes_timeout` both caught.

## Composition checks (independent pass)

| # | Question | Result | Evidence |
|---|---|---|---|
| 1 | `measure_test_evidence.py --check` / `--selftest` on the candidate, with the #541 and #443 dispositions coexisting | PASS. The ratchet reads 75 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers and 3 <= 3. The self-test passes 101/101, including "every DUT-source reader has a current disposition". No duplicate dict key, so neither disposition was silently overwritten | `receipts/static_venv/measure_test_evidence*.log`, `receipts/registry_duplicates.txt`, `check_registry_duplicates.py` |
| 2 | TESTING.md rows for `crf_rx`, `render_setpoint` and `milan_dp` agree with the candidate's suites | PASS. The `crf_rx` row (`TESTING.md:465`) names `validation_error_unlocks` and `validation_error_refreshes_timeout`. `crf_rx/mutants.py:20,23` defines them, and the composed run catches both. The #443 explicit-target row (`TESTING.md:265`) names `render-csr-controls`, and `milan_dp/Makefile:434-436` defines that target, which ran 4/4. The `milan_dp` row (`:481`) and `render_setpoint` row (`:496`) are unchanged by either side. No duplicate table line | `receipts/focused/crf_rx.log`, `receipts/focused/render_csr_controls.log`, `receipts/registry_duplicates.txt` |
| 3 | REGISTER_MAP.md `CRF_CTRL` and render CSR rows consistent, with anchors resolving | PASS. The #541 hunk rewrites only the `0x738` `CRF_CTRL` row (`:839`). The #443 hunks add the contents entry, the `0x8DC` group-index row (`:242`), the debug-group span sentence (`:1824-1826`) and the `### 0x8DC` section (`:1946-1996`). They are disjoint and each carries over verbatim. `REGISTER_MAP_CLASSES.md:107` is #443-only. docs_check reports 0 findings in both git and filesystem-walk modes. `gen_toc --check` passes. `--verify-anchors` reports 176 cross-page fragment links reproduced. em dash vs `ec9cf454` shows 0 findings over 109 added lines | `receipts/static_venv/` |
| 4 | Candidate tree equals merge(dev after #541, `b3458db0`), with no divergence from the criss-cross base | PASS. Every reconstruction reproduces `42e0c2ec`: via real dev, directly, and against live dev `fd9e0ebf` | `receipts/merge_reconstruction.txt`, `receipts/live_dev_tip.txt`, `reproduce_merge_reconstruction.sh` |
| 5 | Submodule gitlinks | Identical in the candidate, C_541 and the source for all four gitlinks (`external` `efeb541a`, `gptp-processor` `e5dcea6e`, `protocol-processor` `990f9652`, `third_party/verilog-axis` `48ff7a7e`) | `receipts/merge_reconstruction.txt` |
| 6 | Other workflow and record pins touched by the composition | None. Neither side changes workflows, `VERSION` (`milan_csr.sv:196` stays `0x0002_0060`, and the #443 `CHANGELOG.md:32-40` deferral is the only CHANGELOG change), budgets or pin records. `ci_events.py --check` passes with 1647 items, `--selftest` passes with 2188 arms, and `check_feature_status`, `check_hygiene --check` and the source-list and idiom gates pass | `receipts/static_venv/SUMMARY.txt` |

Static gate bank on the candidate: 19/19 rc 0 (`receipts/static_venv/SUMMARY.txt`). The first attempt, with the system interpreter, lacked the locked Markdown dependencies. Three Markdown gates (`gen_toc` x2, `check_em_dash`) returned 2 and named the missing package. That attempt is kept at `receipts/static_sys/`. The recorded bank ran in an isolated scratch environment holding `tools/markdown/requirements.txt`, installed with `--require-hashes`, plus system packages.

Focused composed suites, run in the foreground on the candidate with the scoped simulator 5.050 (identity in `receipts/verilator_identity.txt`) and at most 8 jobs: `receipts/focused/SUMMARY.txt`, all rc 0.

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head. This round raises no new finding.

Retained SUGGESTIONs (optional; they do not affect coverage):

- **S-A (from R320-2 S2-residual, retained by R320-3), SUGGESTION, Tests.** `hdl/milan/milan_datapath.sv:6163-6167`. No integration leg reaches 256 rails, so a datapath packing that dropped `rsp_rails_w[15:8]` would stay green. The file is byte-identical to `b3458db0` in the candidate, so the composition neither worsens nor fixes it.
- **S-B (from R321-2 S1, retained by R320-3), SUGGESTION, Tests.** The neighbour reads in `tb/verilator/csr/sim_main.cpp` run with `i_render_status` tied to zero, so a decode that aliased `0x8E0` to `RENDER_STAT` would survive there. The file is byte-identical to `b3458db0` in the candidate.

## Prior public review findings: status at this head

Read after the pass above; nothing in it changed as a result.

| Finding | Status at `4ee96a61` | Evidence |
|---|---|---|
| R321-1 F1 / R320-1 F1: CSR bench asserts `0x8DC` unmapped | RESOLVED, and carried into the composition | `tb/verilator/csr/sim_main.cpp:142,1430` grade `RENDER_STAT`, and no "unmapped" claim for `0x8DC` remains. The composed CSR bench passes (`receipts/focused/csr.log`) |
| R321-1 F2: `STRM_SEL[9]` not graded | RESOLVED | `sim_aclk.cpp:405,409`. The composed `bit9_window_selection` control is caught at `RENDER-CSR: bit 9 preserves talker rejection` (`receipts/focused/render_csr_controls.log`) |
| R321-1 F3: campaign missing from TESTING.md | RESOLVED | `TESTING.md:265` |
| R321-1 F4 / R320-1 F2: VERSION bump or deferral | RESOLVED (deferral recorded) | `CHANGELOG.md:32-40`, `REGISTER_MAP.md:1950-1953`, `milan_csr.sv:196` |
| R321-1 F5 / R320-1 F3: group index lacks `0x8DC` | RESOLVED | `REGISTER_MAP.md:242` |
| R321-1 S1, S2 | Taken earlier (reset/selector note at `REGISTER_MAP.md:1959-1966`; synthesis wording in the PR body) | read at this head |
| R320-2 S2-residual and R321-2 S1 | RETAINED as S-A and S-B, SUGGESTION | blobs unchanged |
| R320-3 | POSITIVE, no MINOR or higher | nothing to resolve |

## Per-lens results at this head

```text
[R321] PASS Conformance - REGISTER_MAP.md:242,839,1824-1826,1946-1996; CHANGELOG.md:32-40; milan_csr.sv:196,922,2389-2395,2561 - issue #443 items 1, 2, 3 and 5 plus the item-4 decision still hold in the composed tree; the #541 CRF_CTRL contract text and the #443 RENDER_STAT contract coexist without contradiction, and VERSION is untouched by both sides
[R321] PASS RTL - receipts/merge_reconstruction.txt (KL_crf_rx.sv identical from module to EOF; every #443 hdl blob equal to b3458db0); receipts/focused/{csr,milan_dp_aclk,render_csr_controls,milan_dp_render,crf_rx}.log - the composition adds no functional RTL beyond the reviewed sources; the composed elaborations of milan_csr and milan_datapath (N=1, N=4 window, two-listener render, absent-stage copy) build and pass
[R321] PASS Robustness - receipts/focused/render_csr_controls.log (absent stage 33/0 under accepted ingress; talker, out-of-range and bit-9 selections; RVALID/RDATA held under backpressure; reset after a rail); receipts/focused/crf_rx.log (validation-error retention and timeout mutants) - both lanes' negative and reset paths still hold when composed
[R321] PASS Tests - scripts/measure_test_evidence.py:597-600,632-636; TESTING.md:265,465; receipts/static_venv/measure_test_evidence*.log; receipts/registry_duplicates.txt; receipts/focused/SUMMARY.txt - both dispositions present once each, ratchet and self-test pass, and composed counts equal the source-published counts, with every named mutant caught
[R321] PASS Docs - receipts/static_venv/{docs_check_git,docs_check_walk,gen_toc_check,gen_toc_verify_anchors,check_em_dash_parent,check_doc_style,check_doc_paths}.log; receipts/overlap_patch_ids.txt - shared pages carry both sides verbatim, anchors resolve, and no stale or duplicated row
```

## Reviewer-owned completion ledger

| Lens | Result | Does the composition touch this lens's scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes: the ABI page carries both sides' contract text | `REGISTER_MAP.md:242,839,1824-1826,1946-1996`; `REGISTER_MAP_CLASSES.md:107`; `CHANGELOG.md:32-40`; `milan_csr.sv:196,922,2389-2395,2561`; issue decisions | R321-3 (source acceptance: R320-2, R321-2 at `5beebb7c`; R320-3 at `b3458db0`) | `4ee96a61bf35402a6f88e1ebad1167e9873721c5` |
| RTL | CLEAN | Functionally no: the only RTL change beyond the source is #541's header comment in `KL_crf_rx.sv`. Re-applied at this head anyway | `receipts/merge_reconstruction.txt`; composed elaborations in `receipts/focused/` | R321-3 (source RTL: R320-3 at `b3458db0`, R321-2 at `5beebb7c`) | `4ee96a61bf35402a6f88e1ebad1167e9873721c5` |
| Robustness | CLEAN | No new robustness-relevant code; composed controls re-run | `receipts/focused/render_csr_controls.log`, `milan_dp_aclk.log`, `crf_rx.log`, `csr.log` | R321-3 (source: R320-3 at `b3458db0`) | `4ee96a61bf35402a6f88e1ebad1167e9873721c5` |
| Tests | CLEAN (S-A, S-B optional) | Yes: the shared `measure_test_evidence.py` dispositions and the TESTING.md tables | `measure_test_evidence.py:597-600,632-636`; `TESTING.md:265,465,481,496`; `crf_rx/mutants.py:20,23`; `milan_dp/Makefile:434-436`; `receipts/focused/`; `receipts/static_venv/` | R321-3 | `4ee96a61bf35402a6f88e1ebad1167e9873721c5` |
| Docs | CLEAN | Yes: `REGISTER_MAP.md` and `TESTING.md` are shared | docs gate logs in `receipts/static_venv/`; `receipts/overlap_patch_ids.txt`; `receipts/registry_duplicates.txt` | R321-3 | `4ee96a61bf35402a6f88e1ebad1167e9873721c5` |

## Real limits

- **Not run** (outside this round's allowance, and owned by the manager):
  - the full `milan_dp` default sweep, the parent, protocol-processor and gPTP banks, behave, the builder, Yosys, act, and the host act runner.
  - **Why the missing Yosys run does not weaken the composition claim:** the composed RTL is functionally identical to the source's. The source cell counts were reproduced by R321-1 and R320-1 on byte-identical RTL.
- **Manager candidate-bank receipts not located.** The public evidence tree at `667ec7db/review-evidence/443-r1` contains author rounds and review packets. No manager bank receipt for `4ee96a61` was found there or in the PR/issue comments. This round relies only on its own runs.
- **No hosted evidence for the candidate.** GitHub reports no commit `4ee96a61` because it is unpushed. The source head `b3458db0` shows executed successes for `rtl-fast`, `verilator-suites` (5 shards), `yosys-portability` (4 shards), `docs-check`, `docs-check-no-git`, `bdd-conformance`, `elaborate`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, `changes` and `full-ci-gate`. `Physical gPTP (nightly and manual)` was **skipped** there, which is not hardware evidence (`receipts/hosted_checks.txt`).
- **Physical calibration NOT RUN.** No hardware was used, and field skips are not hardware proof.
- **Probe object left in the clone.** The reconstruction wrote unreferenced probe commit objects (merges of dev and the #541 head) into this clone's object store. No ref, index or worktree changed.
- **Clone restored and verified** (`receipts/final_restore_check.txt`):
  - HEAD `4ee96a61`; the index writes tree `42e0c2ec`.
  - `diff-files` and `diff-index --cached` are clean, and all 892 tracked regular files re-hash to their index blobs.
  - No untracked or ignored residue remains in the superproject or its submodules. The build outputs and caches this round created were removed.
  - The four gitlinks are unchanged.

## Pending manager duties

- **Build the final current-dev candidate at the merge turn.** Live dev `fd9e0ebf` already equals C_541 in tree, so merge(`fd9e0ebf`, `b3458db0`) should reproduce `42e0c2ec`. Re-check if dev moves again.
- **Run the full CONTRIBUTING step-7 bar on that tree:** the full Verilator sweep, both repositories' suites, behave, the lint ratchet and Yosys. Publish the receipts.
- **Own hosted and act acceptance** at the exact merged head, distinguishing executed jobs from skipped contexts.
- **Obtain the maintainer's explicit merge authorization.**
- **After merge:** run `check_merge_containment.py`, `--merged-prs` and `check_merge_review_integrity.py`, close issue #443 and move it to Done.
- **Publish this packet** (REPORT.md plus the files in MANIFEST.sha256).

R321-3 FINISHED

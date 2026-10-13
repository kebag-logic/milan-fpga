[R584] POSITIVE - exact head 7094848c928c4c04bf5fae51346b0e1e5848a971

Composition review R584-20 of issue #697 / PR #705, merge-train candidate `7094848c928c4c04bf5fae51346b0e1e5848a971`, tree `34b24fec86f5b1c43e6b4142f1c38facc5a72835`. This is a composition acceptance review, not a new source review. The candidate's parents are, in order, the predecessor candidate `ac0142539856222b84ef8e5af414d12132a5bebf` (live dev `e81ce82f` plus B16 / PR #725 and #730 / PR #731) and the PR #705 source head `d40e4e9827be2516f8f34b9d65f0a483fff2194c`. That source head holds two independent POSITIVE source reviews: R584-19 ([6142728394](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6142728394)) and R585-19 ([6142799225](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6142799225)).

I applied all five lenses to the composed tree. No BLOCKER, MAJOR or MINOR is open. One optional SUGGESTION is recorded. The composed tree adds no defect beyond the reviewed sources.

## What was reconstructed, and from what

- **Contract.** AGENTS.md sections 5 to 8. CONTRIBUTING.md sections 3 and 6, including the em-dash rule and the documentation privacy rules. docs/README.md as the documentation map.
- **Issue #697.**
  - The frozen acceptance items 1 to 5.
  - The owner decisions that replace option (a) with the `tsn-c-stack` submodule: [6074093506](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074093506), [6074191062](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074191062) and [6074877336](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074877336). Acceptance item 3 of 6074093506 requires `.gitmodules` and `act_ci.py` `TRUSTED_SUBMODULES` to change in the same PR.
  - The lane assignment [6091228902](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6091228902).
  - The round-19 ruling [6137497435](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6137497435), which adds the fifth capture.
  - The round-20 ruling [6140933191](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6140933191), which adds the sixth capture, F5. Its bar is `ctrl_boundary.py --require-rv32 --selftest --without verilator` ending `PASS` and the held-text probe reporting 0 program refusals.
  - The author's round-20 REVIEW READY ([6142003922](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6142003922)).
- **Interface authorities.** `docs/testing/CI_WORKFLOWS.md` (both sides), `.github/workflows/*.yml` and `scripts/act_ci.py`. Also the boundary gate's own contract in the docstring at `sw/firmware/ctrl/test/ctrl_boundary.py:60-112`.
- **Diff and history.**
  - `git diff ac014253..7094848c`: 77 files, the PR's side.
  - `git diff d40e4e98..7094848c`: 4 files, the predecessors' side.
  - The history of both parents.
  - The train PRs' live heads: #725 `f1b2489f`, #731 `b341e875` and #705 `d40e4e98`. All three are ancestors of the candidate. Live dev is `e81ce82f`.
- **Public executable evidence.** [747eb1ee / review-evidence/697c-r1](https://github.com/kebag-logic/milan-fpga/tree/747eb1eecc60d94c6d13d9da8735404b2c7b2fa1/review-evidence/697c-r1). In `author-r20`, the published `images-dev.json` and `images-head.json` are the same blob, `b21b06e2`. I compared my linked standalone images against it.

I read the prior public review findings on this PR only after my own pass over the composition. They are dispositioned below.

## The composition, file by file

Receipt: `receipts/compose_check.log`, made by `scripts/compose_check.sh`.

- **The merge is clean.**
  - `git merge-tree --write-tree ac014253 d40e4e98` gives `34b24fec`, which is the published tree.
  - The PR source contains live dev `e81ce82f`. Its tree `ab5a465c` is also the tree of `cdb49e7e`, the #726 train candidate on the predecessor's first-parent chain. So live dev is the common content base of both sides.
- **79 paths differ from live dev.**
  - 75 paths come from the PR alone, and each equals the PR source's blob.
  - 2 paths come from the predecessors alone, and each equals the predecessor's blob: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`, both from B16.
  - 2 paths are changed by **both** sides: `docs/testing/CI_WORKFLOWS.md` and `scripts/act_ci.py`. The second one is not in the manager's note, which names only `CI_WORKFLOWS.md`. In `act_ci.py`, #730 adds the CPU-range monitor, and this PR adds the sixth `TRUSTED_SUBMODULES` entry and its self-test. Their hunks do not overlap, and git merged them without conflict.
- **The predecessors add only 4 files to the PR source:** the two B16 findings pages, `CI_WORKFLOWS.md` and `act_ci.py` (`receipts/composition_delta.log`). They add nothing under `hdl/`, `configs/`, `sw/`, `tb/`, `syn/`, `.github/`, `.gitmodules` or any gitlink. The candidate's six gitlinks equal the PR source's. `tsn-c-stack` is at `405dc683`, and lwSRP is unchanged at `08ee86e8`.

### Semantic interactions examined

1. **`CI_WORKFLOWS.md`, both sides.**
   - **PR side.** The firmware jobs' stack initialization (`:59-60`). The `firmware-boundary` job with six captures, its budget and its timing (`:66-104`). The `firmware-verilator` job (`:105-120`). The aggregate (`:135`). The job inventory (`:164`). The Verilator workers' stack initialization and pin check (`:323-328`). The act manifest, six gitlinks and five fetched pins (`:1725-1733`). The local commands (`:2632-2642`).
   - **#730 side.** The interrupted job under the CPU-range monitor (`:1654-1658`). Staging and job ranges, and the per-workflow derivation (`:1846-1898`). Warnings, signal mask and cleanup precedence (`:1903-1990`). Slot layout (`:2280-2290`). Self-test list (`:2500`).
   - **The two do not contradict each other.**
     - #730 says "`docs`, `elaborate` and `rtl-fast` derive 1" (`:1878-1879`). In the composed tree, `rtl-fast.yml` has 12 jobs, including this PR's `firmware-boundary` and `firmware-verilator`, and none has a matrix. It still derives 1. `rtl.yml` still derives 4. A reimplementation of the stated rule that imports nothing from the tree confirms all four workflows (`receipts/derive_concurrency.log`). The runner's own standing check (`act_ci.py:7245-7250`) requires each shipping workflow to derive 1 to `SLOT_JOB_RANGES` (= 4). That holds.
     - #730 says "a leg's `nproc` is the hosted runner's 4 before and after the move" (`:1855-1856`). This PR's boundary step runs its controls "four at once, the hosted runner's CPU count" (`:99`). The code uses a fixed `JOBS = 4` (`ctrl_boundary.py:154`, `ctrl_runs.py:59`) and does not read the CPU count. So a move between ranges cannot change it.
     - #730's text says nothing about the submodule manifest or the job inventory. The PR's "six gitlink paths" and "five allowlisted public pinned dependencies" (`:1725-1733`) stay true at the composed `act_ci.py:227-262`.
2. **`act_ci.py`, both sides.** I checked it statically, by parsing the code without importing or running it (`scripts/act_ci_static.py`, `receipts/act_ci_static.log`). Running the runner's self-test on a host is not allowed for this round.
   - The PR's `selftest_stack_manifest` (`:13091`) is defined once. `selftest_submodule_manifest` (`:12946`) calls it.
   - Every name it uses is defined in the merged module.
   - No self-test function is defined twice.
   - `TRUSTED_SUBMODULES` lists exactly six entries, ending with `third_party/tsn-c-stack`.
   - #730's diff touches neither `validate_submodule_manifest`, `GitFixture` nor the tally's `refused` and `check` methods, which the PR's arms call.
3. **Gate inventories and registries.**
   - The boundary gate's text cross-check (`ctrl_configs.builder_texts`/`held`) scans the tree for any program that names the firmware's tree. The predecessors' new `act_ci.py` code and the B16 pages add no such program: `receipts/held_text_probe.log` shows 39 text candidates and **0 program refusals**. The 7 module refusals come only from the stand-in capture holding no compile, as recorded in earlier rounds.
   - `ci_events.py --check` reads `CI_WORKFLOWS.md` and the four workflows: 2169 contract items, the same count as at the source head.
4. **Documentation tables, Contents blocks and anchors.** B16 edits one `docs/findings/README.md` table row (`:15`) and appends to its findings page. This PR edits neither. `gen_toc.py --check` and `--verify-anchors` pass over the composed tree, and so does `check_em_dash.py` against both the first parent and live dev (table below).

## Gates and probes run on the candidate

The environment was CPython 3.12.3 (venv with pyyaml, `sw/litex/litex_pins.txt` and the hash-locked `tools/markdown/requirements.txt`), GCC 16.2.1, Clang 18.1.3, GoogleTest/GMock 1.14.0, and the pinned RV32 SDK. I installed the SDK with `scripts/ci_rv32_sdk.py` from the pinned archive, and the digest `d42680e9...` verified (`receipts/rv32_sdk_install.log`). `scripts/env.sh` records the setup.

| Command (on the composed tree) | Result | Receipt |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (the `firmware-boundary` step) | rc 0, `ctrl_boundary: PASS`. 2852 compiled sources of 3082 recorded invocations: 1639 the firmware's, 347 the stack's, 866 test equipment's and builders' own. 0 findings. 112 boundary, 120 pin and 4 figure controls, 0 misbehaved. 878 s. All six known builders ran under the capture: `fw_rv32_selftest.py`, `test_ctrl_firmware.py`, `test_ctrl_nvm.py`, `fw_coverage.py --build-only`, `test_ctrl_memory.py --build-only` and `stream_counter_f5.py --build-only` at both shapes. The F5 and reset-entry removal controls are refused by name (`:38-43`), and the F5 pin controls hold (`:248-251`). The figures equal those both source reviews report at `d40e4e98`. | `receipts/boundary_without_verilator.log`, `.rc` |
| Held-text probe (the round-20 bar's `held_text_probe.py`, the same probe as R584-18's) | rc 0, 0 program refusals | `receipts/held_text_probe.log`, `scripts/held_text_probe.py` |
| Standalone RV32 control image at all 5 shipped shapes, candidate and predecessor candidate `ac014253` | 5 of 5 ELFs byte-identical by SHA-256 and size. Both manifests hash `546b0d42...`. All 5 hashes also equal the author's published `images-dev.json` / `images-head.json` (blob `b21b06e2`) at `747eb1ee`. | `receipts/images_candidate.*`, `receipts/images_predecessor.*`, `scripts/images.sh` |
| 47 documentation and CI-contract commands: `docs_check.py`; `check_em_dash.py --base ac014253` (0 findings over 457 added lines on 12 pages) and `--base e81ce82f` (0 over 2965 lines on 14 pages) and `--selftest`; `gen_toc.py --selftest/--verify-anchors/--check`; `ci_events.py --check` (2169 items), `--selftest` (2169 items, 3064 arms) and `--firmware-census`; `ci_scope.py --selftest`; `suite_shards.py --selftest`; `check_submodule_docs.py` and `--selftest`; `submodule_boundaries.gen.py --check/--selftest`; `measure_test_evidence.py --check/--selftest`; `measure_test_evidence_readers.py`; `DOC_MAP.gen.py`; the idiom, hygiene, naming, port-contract, archive, source-list and bare-metal checks; `ctrl_build.py --stack-pin` | 47 of 47 rc 0 | `receipts/docs_gates.txt`, `scripts/docs_gates.sh` |
| Independent workflow-concurrency derivation | docs 1, elaborate 1, rtl-fast 1 (12 jobs), rtl 4. This matches `CI_WORKFLOWS.md:1878-1879`. | `receipts/derive_concurrency.log`, `scripts/derive_concurrency.py` |
| Static check of the merged runner | OK (see interaction 2) | `receipts/act_ci_static.log`, `scripts/act_ci_static.py` |
| Disposable probe: the candidate tree with `CI_WORKFLOWS.md` taken from only one side | `ci_events.py --check` rc 0 both ways (see R584-20-S1) | `receipts/probe_doc_side_loss.log` |
| Clone integrity after all probes | HEAD and tree exact. Index equals HEAD (1315 entries, stage 0). Every tracked byte and mode hashed from disk equals the index. `status --porcelain --ignored` is empty. All five required submodules are at their gitlinks, with clean status and index. | `receipts/verify_clone.log`, `scripts/verify_clone.sh` |

## Judgement of the manager's items

| Item | Result | Evidence |
|---|---|---|
| The merged `CI_WORKFLOWS.md` states both sides correctly | Holds | Interaction 1 above. Each side's text equals its source byte for byte, because the merge is clean. Neither side's statements are made false by the other, as checked against the composed workflows and runner. |
| The boundary gate passes on the composed tree with all six captures | Holds | `ctrl_boundary: PASS`. Six builders captured, F5 at both shapes. 112/120/4 controls, 0 misbehaved. |
| `held_text_probe` reports 0 refusals | Holds: 0 program refusals | `receipts/held_text_probe.log` |
| `act_ci.py --selftest` passes | **Not run by this review.** Running the runner's self-test on a host is not allowed for this round. Static composition check instead. Pending for the manager. | `receipts/act_ci_static.log` |
| `suite_shards.py --selftest` passes | Holds | `receipts/docs_gates.txt` |
| Images equal the composed dev side | Holds for the 5 standalone shapes, executed on both parents' content. The 60 runtime variants were not relinked. Their inputs are identical to the PR source's, because the predecessors change no file under `sw/`, `configs/` or any gitlink. The author's published receipts cover those variants at the source head. | `receipts/images_*`, `receipts/composition_delta.log` |
| Nothing became false in combination with B16 and #730 | Holds | B16's two pages are read by no gate or builder except the documentation gates, which pass. #730's derivation and slot statements hold with this PR's two new `rtl-fast` jobs. The PR's manifest statements hold with #730's runner. |

## Findings

### R584-20-S1 - SUGGESTION - Tests, Docs - no gate pins either side's prose in `CI_WORKFLOWS.md`, so the merge train relies on a clean merge for it

- **Artifact:** `docs/testing/CI_WORKFLOWS.md:59-135,323-328,1725-1733` (this PR) and `:1654-1658,1846-1990,2280-2290` (#730). `scripts/ci_events.py --check`.
- **Evidence:** in a disposable copy of the candidate, I replaced `CI_WORKFLOWS.md` with the predecessor's version, which drops every `firmware-boundary`, `firmware-verilator` and `tsn-c-stack` statement. `ci_events.py --check` still passed, 2169 items. It also passed with the PR source's version, which drops #730's CPU-range sections (`receipts/probe_doc_side_loss.log`). At this head the merge is clean and the merged page is correct, so nothing is wrong in the tree.
- **Impact:** none at this head. A future train whose resolution drops one side of this page would pass the documentation gates. Only review would catch it.
- **Optional outcome:** none required. If wanted, a later Issue could have `ci_events.py` pin the job inventory sentence (`:164`) against the `rtl-fast` aggregate's job list.

No other defect was found. I tested these suspicions and refuted each one:
- #730's "`rtl-fast` derives 1" made false by this PR's two new jobs: refuted, since neither job has a matrix (`receipts/derive_concurrency.log`).
- This PR's boundary parallelism depending on the act container's CPU set: refuted, since it is a fixed 4 (`ctrl_boundary.py:154`, `ctrl_runs.py:59`).
- #730's runner code adding a program the boundary's text cross-check refuses: refuted (`receipts/held_text_probe.log`).
- The PR's manifest arms calling a helper that #730 changed: refuted (`receipts/act_ci_static.log`).

## Prior public findings at this head

| Finding | Disposition at `7094848c` | Evidence |
|---|---|---|
| R584-18-F1 (BLOCKER, the boundary refused #726's F5 program on the composed tree) | RESOLVED, and it stays resolved in this composition | `ctrl_boundary: PASS`; held-text 0 program refusals; F5 removal controls `:38-39` |
| R584-18-F2 (MINOR, F5 and counter targets ran without the stack pin check) | RESOLVED and unchanged by the composition | F5 pin controls `boundary_without_verilator.log:248-251`; `tb/verilator/milan_dp/` is not in the predecessors' delta |
| R584-19-RES-1 (test prerequisite pages omit `third_party/tsn-c-stack`) | RETAINED RESIDUE, carried with its exact fix as R584-19 states it | The pages it names (`TESTING.md`, `tb/verilator/README.md`, `milan_dp/README.md`, `726_STREAM_COUNTERS.md`, `QUICKSTART.md`) are not in the predecessors' delta |
| R584-19-S1 (`run`'s own `stack-pin` prerequisite is redundant) | RETAINED SUGGESTION | `tb/verilator/milan_dp/Makefile` unchanged by the composition |
| R585-16-RES-1 and R584-8-RES-1 (wording residue), R584-17-S1/S2 and the earlier carried suggestions and #495 residue | RETAINED as R584-19 and R585-19 list them. The composition touches none of their artifacts. | `receipts/composition_delta.log` |
| R584-17-RES-1/2, R585-18-RES-1 | RESOLVED at the source head per R584-19 and R585-19 | PR body; not affected by the composition |
| Every earlier blocking finding (R584-1 to R584-18, R585-1 to R585-18) | RESOLVED at the source head per R584-19 and R585-19, and not reopened by the composition | the predecessors' delta is 4 files, none in their scope |

## Lens results

[R584] PASS Conformance - `receipts/compose_check.log`, `receipts/composition_delta.log`, `receipts/images_*.MANIFEST`, `receipts/boundary_without_verilator.log`, `scripts/act_ci.py:227-262` at `7094848c`, issue #697 acceptance 1-5 and rulings 6074093506, 6091228902, 6137497435, 6140933191 - checked that the composed tree still meets the acceptance items. The pin is `405dc683` and lwSRP `08ee86e8` is unchanged. The six gitlinks equal the PR source's. The standalone images equal the predecessor candidate's and the published dev manifest. The required boundary step passes with all six captures. `TRUSTED_SUBMODULES` holds the six entries the owner's item 3 requires. The composition touches this lens only through `act_ci.py` and the CI page, and both hold.

[R584] PASS RTL - `receipts/composition_delta.log` (no path under `hdl/`, `configs/`, `syn/`, `tb/` or any gitlink between `d40e4e98` and `7094848c`), `receipts/derive_concurrency.log` - the composition changes no RTL, clock, reset, CDC, register or build-input artifact, so the RTL lens is covered by the source reviews R584-19 and R585-19 at `d40e4e98`. Within this lens's resource and scheduling scope, I checked #730's container-concurrency rule against the composed workflows. It derives the same widths, so no job's hosted-shaped `nproc` changes.

[R584] PASS Robustness - `scripts/act_ci.py:12946-13117` (manifest refusal arms, including the PR's four `tsn-c-stack` variants) and `:2095-2150` (#730's refusals of an unreadable `max-parallel`), `receipts/act_ci_static.log`, `receipts/boundary_without_verilator.log` (120 pin controls, including the F5 off-pin and edited-stack refusals) - checked that each side's refusal paths survive the merge intact and are still reached. Nothing about one side's refusal paths depends on the other side. Not executed here: the runner's own self-test (limit below).

[R584] PASS Tests - `receipts/boundary_without_verilator.log` (112 boundary, 120 pin and 4 figure controls, 0 misbehaved), `receipts/held_text_probe.log`, `receipts/docs_gates.txt` (`ci_events.py --selftest` 3064 arms, `suite_shards.py --selftest`, `ci_scope.py --selftest`, `measure_test_evidence.py --selftest`, `check_submodule_docs.py --selftest`), `receipts/probe_doc_side_loss.log` - checked that the standing gates that read the overlapping files pass on the composed tree with the source head's figures. I also ran a planted side-loss probe of the shared page. It shows the documentation contract does not pin that prose (R584-20-S1, SUGGESTION, which does not affect coverage).

[R584] PASS Docs - `docs/testing/CI_WORKFLOWS.md:59-135,164,323-328,1654-1658,1725-1733,1846-1990,2280-2290,2500,2632-2642`; `docs/findings/README.md:15`; `receipts/docs_gates.txt` (`docs_check.py`, `check_em_dash.py` at both bases, `gen_toc.py --check/--verify-anchors`, `DOC_MAP.gen.py --check`, `check_doc_style.py`, `check_doc_paths.py`) - checked both sides' statements on the shared page against the composed workflows (`receipts/derive_concurrency.log`), runner (`receipts/act_ci_static.log`) and boundary run, and the documentation gates on the combined tree. R584-20-S1 is a SUGGESTION. The carried residues are listed above and are not opened by the composition.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #697 acceptance and rulings; three-way composition and merge-tree identity; gitlinks; `TRUSTED_SUBMODULES`; 5 standalone images vs predecessor and published dev manifest; required boundary step | R584-20 | `7094848c928c4c04bf5fae51346b0e1e5848a971` |
| RTL | CLEAN. The composition does not touch it, so it is covered by the source reviews R584-19 and R585-19 at `d40e4e9827be2516f8f34b9d65f0a483fff2194c` | predecessors' delta (no RTL/config/build-input path); concurrency derivation on the composed workflows | R584-20 (composition), with R584-19 / R585-19 (source) | `7094848c928c4c04bf5fae51346b0e1e5848a971` |
| Robustness | CLEAN | merged runner refusal arms (static); #730 derivation refusals; 120 pin controls on the composed tree | R584-20 | `7094848c928c4c04bf5fae51346b0e1e5848a971` |
| Tests | CLEAN (SUGGESTION S1) | boundary self-test; held-text probe; CI contract, shard, scope and evidence self-tests; side-loss probe | R584-20 | `7094848c928c4c04bf5fae51346b0e1e5848a971` |
| Docs | CLEAN (SUGGESTION S1; carried residues R584-19-RES-1, R585-16-RES-1, R584-8-RES-1) | `CI_WORKFLOWS.md` both sides; findings index row; 47 documentation and contract commands | R584-20 | `7094848c928c4c04bf5fae51346b0e1e5848a971` |

## Real limits

- `act_ci.py --selftest` was **not run**, because running it on a host is not allowed for this round. Docker, act and the local replica were not used. My evidence for the runner's composition is static only: parsing, definitions, call wiring and the manifest literal. The author's runner self-test receipt (`author-r20/logs/act-selftest.log`) is for the source head, not this candidate.
- `ctrl_boundary.py --only verilator` (the `firmware-verilator` step) was not run. None of its inputs differ between the candidate and the PR source (`receipts/composition_delta.log`), and both source reviews ran it at `d40e4e98`.
- Of the 65 images, only the 5 standalone ones were linked here. The 60 runtime variants' inputs are identical to the source head's, where the author's receipts cover them. They were not rebuilt here.
- No coverage, mutation, configuration, entry-point or #726 campaign was rerun. The composition changes none of their inputs.
- No full parent, processor, gPTP, Yosys or builder bank was run, and no manager source bank is claimed or inferred. `7094848c` is not on GitHub (the commits API returns 422), so it has no hosted run, and none is claimed.
- Physical calibration NOT RUN. Field skips and skipped physical jobs are not hardware proof.
- The local toolchain is not the hosted image: GCC 16.2.1 here, 13.3 hosted. The boundary step's 878 s is a local wall time, not a hosted calibration.

## Pending manager duties

- Run the runner self-test (`act_ci.py --selftest`) on the candidate inside the disposable CI job boundary, and do hosted and act acceptance on the merge candidate.
- Validate the final current-dev merge candidate at the merge turn, with the builder and native banks, and link the receipts on the PR.
- Carry R584-19-RES-1, R585-16-RES-1 and R584-8-RES-1 to the residue checklist with their exact fixes. S1 here and the carried suggestions are optional.
- Do the completion ledger, merge authorization, post-merge containment and the issue/project closure.

## Clone integrity

After all probes, the clone holds exact head `7094848c928c4c04bf5fae51346b0e1e5848a971`, tree `34b24fec86f5b1c43e6b4142f1c38facc5a72835`:
- Index equals HEAD: 1315 entries, stage 0.
- Every tracked byte and mode hashed from disk equals the index.
- No untracked or ignored files.
- `third_party/verilog-axis`, `protocol-processor`, `gptp-processor`, `third_party/lwSRP` and `third_party/tsn-c-stack` are each at their gitlink, with clean status and index.

The temporary predecessor worktree was removed and pruned (`receipts/verify_clone.log`). Disposable trees live only under `scratch/`, which is not published.

R584-20 FINISHED

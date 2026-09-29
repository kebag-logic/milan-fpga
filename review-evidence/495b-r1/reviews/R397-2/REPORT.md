[R397] POSITIVE - exact head 0cc00731692c9f985f49953200f2c6bdaaddf790

# R397-2: composition review of PR #619 (issue #495, builder and tooling residue) on the merge-train candidate

- **Candidate:** `0cc00731692c9f985f49953200f2c6bdaaddf790`, tree `1cc24ebd427192b9bfb64af68679e4ceef7ea57e`.
- **Parents:** `5c908c7128484e20e388b14d74d83630fa10f6b5` (C_451 = dev `13eda870` + #616) and the PR source head `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0`.
- **Source base:** dev `eaa88a32eb77adeba9c1c631198c7fb516a11095`, which is the merge base of both parents.
- **Scope:** composition acceptance only. The source head already has two POSITIVE reviews: R396-1 (PR comment 5883623883) and R397-1 (PR comment 5883933048). In this report, POSITIVE means the composed tree introduces no defect beyond the reviewed sources.
- **Reconstruction order:**
  1. AGENTS.md and CONTRIBUTING.md (sections 3 and 6).
  2. docs/README.md.
  3. The #495 body and the lane scope comments: assignment 5880790651, STOP 5882153376, disposition 5882165062 (option 2), REVIEW READY, and the #609 residue comment.
  4. The PR #619 body.
  5. `git diff 5c908c71..0cc00731` and the history of both parents.
  6. The public evidence tree `f5de5de1…/review-evidence/495b-r1` (a listing only; it is the author's source evidence at `859fa5d5`).
  7. The manager's review-start comments.
- **Prior findings:** read only after my own verdict and ledger were written and timestamped (receipts/70, receipts/70_written_at_utc.txt, 2026-09-29T06:11:15Z).
- **Not read:** private author material, lane scratchpads, the management directory, or any other reviewer's report before that point.

## 1. What the composition is

- **Clean merge.** `git merge-tree --write-tree 5c908c71 859fa5d5` independently yields `1cc24ebd…`, which is exactly the candidate tree (receipts/merge_tree.txt).
- **Files the PR changes:** 16 (receipts/pr_files.txt).
- **Files the predecessors change against the same base:** 32 (receipts/pred_files.txt):
  - #609 (`eaa88a32..13eda870`) changes 30 of them;
  - #616 (`13eda870..5c908c71`) changes 4, all documentation: `docs/findings/451_TDM8_FIRST_LIGHT.md`, `docs/findings/README.md`, `docs/litex/CLOCK_DOMAINS.md` and `docs/reference/MILAN_COMPLIANCE_MATRIX.md`.
- **Overlap:** two files, `sw/builder/test_builder.py` and `docs/integration/BAREMETAL_FIRMWARE.md`, both touched by #609 only (receipts/overlap_files.txt). #616 shares no file with this PR.
- **Blob provenance** (receipts/21_blob_provenance.txt):
  - Every other PR file in the candidate is byte-identical to its `859fa5d5` blob.
  - Every other predecessor file is byte-identical to its `5c908c71` blob.
  - `git diff --name-only 5c908c71 0cc00731` is exactly the PR's 16 files.
- **Nothing is lost from the overlapping files.** Every line either side added against the base survives verbatim in the candidate (receipts/20_added_lines_survive.txt):
  - `BAREMETAL_FIRMWARE.md`: 62 lines from #609 and 6 from the PR, 0 missing;
  - `test_builder.py`: 5 lines from #609 and 51 from the PR, 0 missing.
- **No submodule gitlink or RTL moves.** The predecessors change nothing under `hdl/`, `configs/`, `tb/verilator/milan_dp*`, `gptp-processor`, `protocol-processor` or `third_party`. The gitlinks are equal in C_451, the PR head and the candidate, and `tb/verilator/nvm_capture_cpu/recipe.py` is the same blob in all four trees (receipts/24_milan_dp_input_identity.txt).

### Semantic interactions examined

| Surface | Interaction | Result |
|---|---|---|
| `test_builder.py` run list and gate numbering | #609 changes gate 1b's split-digraph selection count (2 to 4), the patch-count prose and the fabric-host fixture stub `bios_dispatch_hook_required`. The PR adds `test_rom_clock_contract`, `test_rom_clock_skip_reaches_the_ledger` and three imported arms, changes one print string in `test_baremetal_profile_contract` and gate 25b's `vendor_oui "-1"` reason. | See the detail below the table. |
| `BAREMETAL_FIRMWARE.md` | #609 adds the service-budget paragraph (`:73-78`), the dispatch-hook runtime block, the MDIO/PHY block and the capture word-copy block. The PR edits `:45-46` (clock read by path) and `:2087-2090` (contract clock). | See the detail below the table. |
| Builder output consumed by #609 | #609's capture receipt, host firmware tests and `nvm_cosim` consume shapes and tables the builder generates, and the PR changes `endstation_builder.py`. | Builder outputs for all 5 tracked configurations are **byte-identical** between C_451 and the candidate: 50 files, and 0 stdout differences once the output directory name is normalized (receipts/23). `check_nvm_capture.py` passes against #609's receipt. |
| Strict quoted MAC/hex shapes over the composed inventory | #609 and #616 could add YAML or documented examples. | See the detail below the table. |
| Ratchet budgets (py/sh/cpp idiom, hygiene, test evidence, fail-fast, naming, TODO, port contracts, sv idiom) | Neither side edits a budget, but both add counted code. | All pass at the candidate (receipts/30_gate_22..31). Several sit exactly at budget (for example, py "too many parameters 7 <= 7", sh "no strict mode 5 <= 5"), so the composition consumed no headroom it lacks. |
| CI contract (`ci_events.py`) reading `CI_WORKFLOWS.md` | The PR edits the policy page; neither predecessor edits a workflow or the page. | `--check`: OK over 1655 items. `--selftest`: rc 0. |
| TOC, anchors and em dash | Both sides add Markdown. | `gen_toc --check`, `--verify-anchors` (241 cross-page fragments) and `--selftest` pass. `check_em_dash` gives 0 findings: 28 added lines vs `5c908c71`, 1024 lines vs `eaa88a32` and 469 lines vs live dev `13eda870`. The self-test covers 339/339 arms. |

**Run list and gate numbering (`test_builder.py`):**

- No textual adjacency between the two sides' hunks.
- The run list is 100 entries, all unique. There are no duplicate top-level definitions, and every name is defined or imported (receipts/runlist_*.txt).
- The candidate's run list is byte-equal to the PR head's, and C_451's is equal to the base's.
- No `gate N` label was added or removed by either side.
- In both full banks, the executed sequence equals the run list, with each entry run exactly once (receipts/15).

**`BAREMETAL_FIRMWARE.md` statements:**

- Both sides' statements are present (see the survival check above).
- The clock statements (single `CPU_HZ` in `recipe.py`, read by path; the Milan/CPU plane at the contract clock; the 50 MHz named as what the dated cell measured) do not touch any #609 statement.
- None of #609's service-budget, dispatch-hook, MDIO or capture sentences names a clock value.
- The `#build-contract` target exists at `:29`.

**MAC/hex inventory on the composed tree** (receipts/22, rerun with the candidate's own parsers):

- All 5 tracked configurations `load_config` OK.
- Every builder MAC/hex value in tracked YAML is accepted or is a selector.
- The one hit, `entity_id: x64` in `sw/trace/milan_trace.yaml`, is a barectf field-type alias in a trace schema that no builder code reads. The script's key-name walk is deliberately broad.
- Every quoted documented example keeps its documented verdict:
  - `README-parameters.md:162-171`: `"0x001B_C50A_C100_0005"` and `"1234567890123456"` are accepted as hex, the four MAC spellings are accepted, and `"0:2"` and `"2:0:0:0:0:2"` are refused.
  - The other quoted hits are not builder examples: an IEEE document alias, a Python `bytes.fromhex` literal, a seed, and history-page labels.
- #609 and #616 add no YAML and no MAC or hex example. Their 10 added quoted tokens are JSON hashes, dates and zeros in test code.

## 2. Gates run on the candidate

All ran in this clone at `0cc00731`, with at most 8 parallel jobs. Tool identity is in receipts/00_tool_identity.txt:

- Verilator 5.050: `verilator_bin` sha256 `44898b22…`.
- The RV32 selector: Buildroot 2026.05 GCC 14.3.0.
- Markdown runs used the lock-named environment `md-venv-40cdefe08ebd`, which matches `tools/markdown/requirements.txt` sha256 `40cdefe0…`. It carries the exact locked cmarkgfm, cffi, pycparser, html5lib, six and webencodings.

| Gate | Result | Receipt |
|---|---|---|
| `test_builder.py --require-rv32 --require-elaboration`, full and unmodified (937 s) | rc 0. `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11: the historical Arty place report is not on this host). The elaboration verdict found the patched interpreter and skipped no arm for a toolchain reason. | 14, 15 |
| Same bank, compiler absent: all three RV32 candidates hidden (empty HOME for the absolute selector, and PATH mirroring `/usr/bin` without `riscv*`); `--require-elaboration` (656 s) | rc 0. `ALL GATES PASS EXCEPT 2 NOT RUN` (gate 1b's compiled census, gate 11). | 16, 17, 15 |
| `test_firmware_compiler.py --selftest`, `--absent --audit` | rc 0, rc 0 | 40_gate_01, 02 |
| `test_declarations.py` (includes `[495 MAC]` 9 rules over 30 spellings and `[495 hex]` 10 fields) and `test_clock_contract.py` | rc 0 each | 40_gate_03, 04 |
| LiteX-environment tests: `test_clock_constraints.py`, `test_shipping_clock_constraints.py` (both shipping shapes, both ports), `test_timing_grade.py`, `test_clock_contract.py --soc`, `sw/litex/test_pp_mem_bridge.py` (113/113) | rc 0 each | 40_gate_05..08, 41_gate_01 |
| `check_nvm_capture.py` (census and clocks regenerated through the PR's builder against #609's receipt; five input controls and two timing controls) | rc 0, `PASS` | 40_gate_10 |
| `check_nvm_record_space.py`, with `--self-test` | rc 0, rc 0 | 40_gate_11, 12 |
| #609's host tests on the composed builder: `test_nvm_firmware.py --self-test`, `test_phy_firmware.py`, `test_disabled_writer.py` | rc 0 each | 41_gate_02..04 |
| `check_soc_sources.py`, `check_entity_shape.py --self-test`, `check_wire_accountability.py --self-test`, `pp_srcs.py --check` | rc 0 each | 41_gate_05..08 |
| `make -C tb/verilator/nvm_cosim JOBS=8` (Verilator 5.050) | rc 0. 465 checks, 465 PASS; 39 of 39 mutants killed. | 50 |
| Markdown and documentation gates: `docs_check`, `check_em_dash` (3 bases and `--selftest`), `gen_toc` (`--selftest`, `--verify-anchors`, `--check`), `check_doc_style` (and `--selftest`), `check_gptp_docs`, `DOC_MAP --check`, `check_solution_docs`, `check_submodule_docs`, `check_feature_status` (and `--self-test`), `gen_module_matrix --check`, `check_doc_paths`, `check_archive` | rc 0 each (19 runs) | 30_gate_01..19 |
| `ci_events.py --check`, `--selftest` | rc 0, rc 0 | 30_gate_20, 21 |
| Code-quality ratchets: `check_py_idiom`, `check_sh_idiom`, `check_cpp_idiom`, `check_hygiene --check`, `measure_test_evidence --check`, `measure_fail_fast --check`, `check_todo_ownership`, `measure_naming --check`, `check_sv_idiom`, `check_port_contracts` | rc 0 each | 30_gate_22..31 |
| `check_baremetal_only --check`, `check_sweep_shape --self-test`, `check_deploy_shape --self-test`, `bash -n sw/litex/sweep_extra.sh` | rc 0 each | 30_gate_32..35 |

### Run notes

- **The full bank exceeds one ten-minute foreground command on this host.** Gate 1b alone runs longer than that.
  - The first foreground attempt was cut off at 585 s while still passing (receipt 10, superseded).
  - Two diagnostic slices through `scripts/bank_chunk.py` passed: run-list entries 0-9 and entry 10 (receipts 11, 12). A third slice, 11-29, was cut off inside gate 1b (receipt 13).
  - The verdicts above come from the two **unmodified** full runs (receipts 14 and 17). Each ran as a detached process inside this session and was waited on by foreground polling until it exited. Nothing was left running.
- **`sw/litex/test_pp_mem_bridge.py`** first returned rc 1 under the system interpreter (`No module named 'migen'`, receipt 40_gate_09). That was an environment miss. It passed 113/113 under the LiteX interpreter (41_gate_01).

## 3. Composition probes

These were disposable probes, restored afterwards.

- **P1** (receipts/60): the composed run list is changed to call `test_gptp_rom_clock` directly instead of through the ledger wrapper. The PR's `test_rom_clock_skip_reaches_the_ledger` then fails with its named assertion. So the ledger check still reads the merged file's single `for fn` loop.
- **P3** (receipts/60): `## Build contract` is renamed in the composed `BAREMETAL_FIRMWARE.md`. `gen_toc.py --check` fails.
- **P3b** (receipts/61): the heading is renamed together with its Contents entry.
  - `gen_toc.py --verify-anchors` fails, naming both cross-page fragments into it: this PR's `tb/verilator/milan_dp/README.md:85` and `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1620`.
  - No gate names the in-page fragment `#build-contract` at `BAREMETAL_FIRMWARE.md:2088`. `docs_check` skips anchor-only links. See S1.
- **After the probes** (receipts/90), the clone checks out clean:
  - HEAD is `0cc00731`, tree `1cc24ebd`;
  - all 961 tracked files hash to their index blobs with their index modes, and the index equals HEAD's tree;
  - no assume-unchanged or skip-worktree flag, and no untracked non-ignored file;
  - `gptp-processor` `5dce647a`, `protocol-processor` `c951a9ff` and `third_party/verilog-axis` `48ff7a7e` are at their gitlinks and clean;
  - `external` is uninitialized, as it was at the start.

## 4. Findings

No BLOCKER, MAJOR or MINOR finding.

```text
[R397] SUGGESTION Docs, Tests - docs/integration/BAREMETAL_FIRMWARE.md:2088 - the in-page fragment `#build-contract` is checked by no docs gate
Requirement/evidence: receipts/61. With the heading and its Contents entry renamed, docs_check, gen_toc --check, check_doc_paths and check_doc_style all stay rc 0. Only gen_toc --verify-anchors reacts, and it names only the two cross-page fragments. docs_check.py:26 skips anchor-only links.
Impact: none at this head, because the target exists at :29. The limit comes from the gates and predates this work. The PR added this in-page link; the composition neither introduces it nor changes it.
Required outcome (optional): a later docs-gate change could verify same-page fragments as --verify-anchors does for cross-page ones. Alternatively, the #495 checklist can carry this line.
Verification: P3b turns red at the in-page link.
```

## 5. Prior public findings on this PR, at this head

Both source reviews publish SUGGESTIONs only:

- R396-1: S1-S6.
- R397-1: four suggestions, on `PP_DESCRIPTOR_OWNERSHIP.md:289`, `CI_WORKFLOWS.md:46`, `milan_dp/README.md:121/160/502`, and `test_shipping_clock_constraints.py:44`, where the reports are bounded by the last `route_design`.

Every file they name is byte-identical at the candidate to its `859fa5d5` blob (receipts/71): `test_clock_contract.py`, `sweep_extra.sh`, `CI_WORKFLOWS.md`, `PP_DESCRIPTOR_OWNERSHIP.md`, `milan_dp/README.md`, `endstation_builder.py` and `test_shipping_clock_constraints.py`. So all ten are **retained unchanged**, and all remain optional. None is resolved or worsened by the composition.

Two line references move because of #609's insertions:

| Reference | Source head | Candidate |
|---|---|---|
| `BAREMETAL_FIRMWARE.md`, the contract-clock sentence cited as `:2036` | `:2038` | `:2088` |
| `test_builder.py`, `test_rom_clock_skip_reaches_the_ledger` | `:27828` | `:27830` |

No prior finding was MINOR or above, so no prior finding keeps a lens unclean.

## 6. Lens results

```text
[R397] PASS Conformance - receipts/22 (candidate parsers over all tracked YAML and every quoted documented example), receipts/20 (both sides' BAREMETAL_FIRMWARE.md statements present), receipts/23 (builder outputs byte-identical to C_451 for 5 configs), 40_gate_03/10 - item 6 of assignment 5880790651 as disposed in 5882165062 holds over the composed inventory including #609/#616; #609's capture receipt still matches the census the PR's builder generates
[R397] PASS RTL - receipts/24 and receipts/pred_files.txt - inapplicable to the composition: the predecessors change no file under hdl/, configs/, tb/verilator/milan_dp*, no submodule gitlink, and not recipe.py; the PR's RTL-adjacent files (milan_dp Makefile, sim_ax1x1gptp.cpp) are the 859fa5d5 blobs, covered clean there by R396-1 and R397-1; nvm_cosim (the one Verilator suite #609 touches) is green at the candidate (receipt 50)
[R397] PASS Robustness - 40_gate_03 ([495 MAC] 9 rules/30 spellings, [495 hex] 10 fields), receipts/14 gate 25b (schema-12 refusals incl. the changed vendor_oui "-1" reason) in the merged test_builder.py, receipts/17 (compiler-absent stand-down path) - refusal and feature-absent paths hold in the composed tree
[R397] PASS Tests - receipts/runlist_0cc00731.txt, 14, 15, 17, 60 - merged test_builder.py: 100 unique run-list entries, no duplicate definition, each executed exactly once in both full banks; #609's gate 1b arm and the PR's ledger/sim/sweep/source arms all run; P1 shows the PR's ledger self-check still bites on the merged file; nvm_cosim 465/465 and 39/39 mutants
[R397] PASS Docs - docs/integration/BAREMETAL_FIRMWARE.md:29-51,73-78,2078-2090 at 0cc00731; receipts/30_gate_01..21 - merged page consistent (contract-clock wording beside #609's service-budget, dispatch-hook, MDIO and capture statements, no contradiction); docs_check, em-dash at three bases, gen_toc check/anchors, ci_events and all documentation gates rc 0; one SUGGESTION (S1) does not affect coverage
```

## 7. Reviewer-owned ledger

A lens with no composition surface is also covered by the source reviews, which are named for it.

| Lens | State | Composition touches scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes: the builder parser over the composed inventory; statements in the merged `BAREMETAL_FIRMWARE.md` | receipts 20, 22, 23, 40_gate_03, 40_gate_10 | R397-2 | `0cc00731692c9f985f49953200f2c6bdaaddf790` |
| RTL | CLEAN | No: no RTL, HDL, CDC, submodule or `milan_dp` input changes in the predecessors (receipt 24) | receipts 24, 50, pred_files | R397-2 (inapplicability shown) + R396-1 and R397-1 (source) | `0cc00731…` (composition); `859fa5d5b9ce6762c38eb683c8d3f5e565dbcff0` (source, an ancestor, with nothing in RTL scope touched since) |
| Robustness | CLEAN | Yes: refusal shapes and the gate 25b row in the merged bank | receipts 14, 17, 40_gate_03 | R397-2 | `0cc00731…` |
| Tests | CLEAN | Yes: merged `test_builder.py`, run list, ledger | receipts runlist_*, 14, 15, 17, 50, 60 | R397-2 | `0cc00731…` |
| Docs | CLEAN (S1 is a SUGGESTION) | Yes: merged `BAREMETAL_FIRMWARE.md`, Markdown gates | receipts 20, 30_gate_01..21, 61 | R397-2 | `0cc00731…` |

## 8. Real limits

- **Verilator path.** The requested `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used a reviewer wrapper to the same Verilator 5.050 binary that the existing pinned wrappers on this host point to (identity and hashes are in receipt 00).
- **LiteX environment.** The LiteX-environment tests ran in the local LiteX environment. All seven pinned repositories are at the revisions `sw/litex/litex_pins.txt` names (migen `4c2ae8df`, litex `a1e1c365`, litedram `f9b75e03`, liteeth `276c9e37`, litespi `02d5a209`, litex-boards `9ac53c7a`, pythondata-cpu-vexiiriscv `15cfab52`), with the patch series the bank verified. It is Python 3.14, not a fresh Python 3.12 venv with only the pins, so it is not the hosted `elaborate` environment.
- **Bank execution.** The full banks ran as detached processes waited on in the foreground (see section 2), not as one foreground command.
- **Not run:**
  - `milan_dp`'s `ax1x1gptp` target, whose inputs are identical to the source head (receipt 24);
  - the full parent, processor, gPTP, Yosys and Verilator banks, which are out of this round's allowance;
  - act, Docker and any hardware.
- **Hosted checks.** The candidate is not on the remote, so it has no hosted checks. At the source head `859fa5d5`, every hosted context executed and succeeded except "Physical gPTP (nightly and manual)", which was **skipped**. A skipped context is not hardware proof.
- **Physical calibration** was NOT RUN. Gate 11 is NOT RUN in both banks, and gate 1b's compiled census is NOT RUN in the compiler-absent bank.
- **The candidate is not the final base.** It composes onto C_451 (dev `13eda870` + #616). The final current-dev candidate is built by the manager at the merge turn.

## 9. Pending manager duties

- Build and validate the final current-dev candidate at the merge turn (source base `5c908c71`, live dev `13eda870`). Re-run this composition's gates if dev or the queued predecessors move.
- Hosted and act acceptance on the pushed candidate.
- Obtain explicit maintainer authorization before merging.
- After merge:
  - post-merge containment;
  - tick the #495 items per the assignment;
  - optionally carry S1 and the retained source suggestions onto the #495 checklist.

R397-2 FINISHED

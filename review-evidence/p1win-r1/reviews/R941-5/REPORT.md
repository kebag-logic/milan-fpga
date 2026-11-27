[R941] POSITIVE - exact head 04a20c74d986e6d939d517a469bcbbdf37a8377d

Composition review R941-5 of issue kebag-logic/milan-fpga#1009 / PR #1017 (base `dev-soft-core`). Candidate `04a20c74d986e6d939d517a469bcbbdf37a8377d`, tree `f3839b37d8256e5530b16dfb3a579bfc0c7e5ddd`, parents `8156dc7aeb2cae7f86843ba9946acae99ff885f4` (the candidate that queued predecessor PR #1019 on top of PR #1016) and `079c4fa1514be460949ddc28ae3277ea1873cb48` (the PR source head). R942-2 and R941-4 each published POSITIVE at that source head. All five lenses were applied to the composition. No BLOCKER, MAJOR, MINOR or new RESIDUE was found. The composed tree introduces no defect beyond the reviewed sources.

Scope: composition acceptance only. The source delta keeps its verdicts from R942-2 and R941-4. Code that the composition does not touch keeps those verdicts, and the review checks whether the composition changes anything that code depends on.

## 1. What the composition is

Receipt: `receipts/composition.txt` (script `composition.sh`).

- The merge base of the two parents is `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`, the PR's source base. Recomputing the merge with `git merge-tree --write-tree 8156dc7a 079c4fa1` gives `f3839b37`, the candidate's exact tree. No hand edit was made in the merge.
- **The live base is unchanged.** `origin/dev-soft-core` is now `ba13338b805e4cc820a2dd50210ae9868ed030ed`, the merge of PR #1019. Its tree `dbdf163a` is the candidate's first-parent tree. Merging the PR head onto the live tip also gives `f3839b37`. This candidate is therefore exactly the tree the merge will produce today.
- **The PR's changes:** 7 commits and 31 files, under `sw/firmware/ctrl_nvm`, `tb/verilator/ctrl_service_budget` and `tb/verilator/nvm_split_target`, plus `sw/firmware/gtest/{README.md,coverage.ratchet}` and three design/audit docs.
- **The predecessors' changes:** 25 commits and 49 paths. They bump gptp-processor to `3ce71b76` and tsn-c-stack `715589c1` -> `a795471c`. They change `.github/workflows/{docs,rtl-fast}.yml`, `scripts/ci_events.py`, `ci_fast_legs.py`, `suite_shards.py`, `ci_gate_workflows.py`, `docs/testing/CI_WORKFLOWS.md`, the ctrl firmware tests, `syn/yosys/rom_digests.tsv`, the gPTP benches and the gPTP docs.
- **Files both sides change:** one, `sw/firmware/gtest/README.md`. The hunks are disjoint:
  - the predecessor changes four tsn-c-stack link pins at lines 246-247, 291 and 299;
  - the PR changes the `nvm_idle` coverage-exclusion row at line 330.

  Each path that only one side changes carries that side's exact blob in the candidate. The shared path carries both sides' hunks and nothing else.

### Semantic interactions checked

1. **Coverage ratchet.** `coverage.ratchet` comes from the PR. `fw_coverage.py` measures `ctrl_nvm` (PR) and the tsn-c-stack sources (predecessor pin) together. I ran `--check` on the candidate and it returned PASS (40 files). `nvm_store.c` measures 513/513 lines and 317/326 arcs, which matches the ratchet's 513/513 and 317/317 after exclusions. `adp.c` is at 206/208 and 99/106. The `nvm_idle` exclusion row from the PR (README:330) is accepted at the new tsn-c-stack pin.
2. **tsn-c-stack `adp.c` and the PR's measured figures.** The bump's only shipped-source change is at `adp.c:309,314`, where `!=` becomes `<` (IEEE 1722.1-2021 6.2.7.1.3). The PR states its save timings and ROM bytes at its source base (`SPLIT_CONTROL_MEMORY.md`, store README). I built `adp.c` at both pins with the firmware's RV32 flags (`ctrl_build.py:72`, rv32i and rv32im, `-Os -DNDEBUG`) using the pinned SDK, whose archive sha256 `d42680e9...` matches `ci_rv32_sdk.py:25`.
   - Text is 3524 B (rv32i) and 3504 B (rv32im) at both pins.
   - Exactly two instructions differ: `li 56; bne` becomes `li 55; bge`, at the same offsets.

   Image layout, ROM bytes and the cycle cost of every path, ADP's receive check included, are unchanged. The PR's stated figures still hold at the merged tree. Receipt: `receipts/adp_rv32_object_diff.txt`.
3. **gptp-processor `3ce71b76`.** The PR's harnesses do not instantiate gPTP RTL. `split_soc.py:221` only drives the `i_gptp_domain_i` input. `rom_digests.tsv` is keyed by processor pin, and the predecessor added the `3ce71b76` row. The PR touches no ROM digest input.
4. **CI inventories and workflows.** The predecessor re-dealt the legs (`rtl-fast.yml`, `ci_events.py`). The PR adds tests inside suites the workflow already invokes: `test_ctrl_nvm.py` (rtl-fast leg 1) and `fw_coverage.py --check` (leg 2). The PR adds no workflow, leg or registry entry. On the candidate, `ci_events.py --check`, `ci_events.py --selftest` and `ci_gate_workflows.py --check` pass.
5. **Docs registries, TOC and anchors.** On the candidate, `docs_check`, `docs_inventory --check`, `DOC_MAP.gen --check`, `gen_toc --check`, `gen_toc --verify-anchors` (759 links) and `check_submodule_docs` pass. So does `check_em_dash --base 8156dc7a`: 0 findings over the 88 added lines in 7 pages.
6. **Comment rule.** I scanned the lines added to C, C++ and Python files in the candidate delta (`8156dc7a..04a20c74`). None names a bench lane label, lane name, review round, reviewer ID or issue-comment ID.

## 2. Gates run on the candidate

All runs are at `04a20c74` in the isolated clone. Each run has its own log and rc file.

| Campaign | Result | Receipt |
|---|---|---|
| 33 docs and CI gates, listed in `run_gates.sh` (docs_check, gen_toc --check / --verify-anchors, check_em_dash --base parent, ci_events --check / --selftest, ci_gate_workflows --check, generate_ci_evidence_pins --check, docs_inventory, DOC_MAP, doc paths, doc style, hygiene, submodule docs, gPTP docs, feature status, solution docs, TODO ownership, py/cpp idiom, bare-metal-only, port contracts, the four NVM checkers, the three measure_* checks, module matrix, three diagram checks) | 33/33 rc=0 | `receipts/gates/*.log`, `*.rc`, `summary.txt` |
| `test_ctrl_nvm.py --require-rv32 --jobs 5` (pinned RV32 SDK, GoogleTest 1.14.0) | PASS: 5 shapes, 656 tests, RV32 text=14004 B; 446 s | `receipts/firmware/ctrl_nvm.*` |
| `fw_coverage.py --check --jobs 5` | PASS (40 files); 862 s | `receipts/firmware/fw_coverage.*` |
| `test_ctrl_firmware.py --require-rv32 --jobs 4`, which compiles the PR's `nvm_store.h` with the predecessor's ctrl tests | PASS; 866 s | `receipts/firmware/ctrl_fw.*` |
| `tb/verilator/nvm_split_target/run.py --self-test` | 79 checks, 0 failures | `receipts/selftests/split_target.*` |
| `tb/verilator/ctrl_service_budget/run.py --self-test`, including the #1009 bind grade and its mutants | `self-test: 0 failures`; 321 mutants caught, none escaped | `receipts/selftests/budget.*` |

These match the author's published receipts at `a7eb193a/review-evidence/p1win-r1`. I fetched them read-only, and every sha256 matches its `MANIFEST.json`. The figures in `gates.txt:4,21,23,73` match the candidate's: 656 tests, `nvm_store.c` 513/513 and 317/326, coverage PASS on 40 files, and ctrl firmware PASS. Receipt: `receipts/evidence_check.txt`.

The `CONTROL ... ESCAPED` lines in the budget log come from the harness's control arms, not from mutants. No mutant line escaped.

## 3. Findings

No new BLOCKER, MAJOR, MINOR or RESIDUE.

**R941-5-S1 SUGGESTION - Tests, Docs - `tb/verilator/ctrl_service_budget/run.py --self-test`, `docs/design/SPLIT_CONTROL_MEMORY.md` (#1009 paragraph).**
- **Evidence:** no hosted workflow runs the budget harness self-test. That self-test holds the #1009 bind grade and its mutants. Only the author's receipts and reviewers' runs exercise it. This predates the composition and is unchanged by it.
- **Impact:** none at this merge. The run above passes at the candidate.
- **Optional outcome:** state where the bind grade's self-test is gated, or open an Issue to put it in a hosted leg.
- **Verification:** the policy page or the Issue names the gate.

## 4. Prior public findings, resolved or retained at this head

I read these after my own pass and ledger were drafted.

| Finding | Disposition at `04a20c74` |
|---|---|
| R941-3-F1 MINOR, R941-3-RES1 | **Resolved** (R941-4, manager ruling 7191672753 and its correction 7191857005). Their artifacts are the PR body and board evidence, which are not in the tree. The composition does not touch them. |
| R942-1-F1 (resource attribution) | **Resolved for the source delta** (R942-2). The composition adds the predecessor's gptp-processor `3ce71b76` RTL, whose resource effect is #1016's own evidence. The PR's ROM bytes are unchanged at the merged tree (section 1, item 2). Routed totals of the merged tree are a manager duty (section 6). |
| R942-1-F2, R941-2-F1, R941-2-RES1/RES2/S1/S2, R941-1-RES1/S1/S2, R931-1-F1/F2/F6/F7/F8, R932-1-F2 | **Retained as disposed** by R942-2 and R941-4. None of their artifacts is a path that the predecessors change. |
| R941-4-RES1, RES2, RES3, RES4 (PR body and board-evidence wording) | **Retained as RESIDUE** for the manager's checklist, with R941-4's exact fixes. They are prose outside the tree, and the composition does not change them. |
| R942-2-RES1 (PR body "Memory and fit" headline) | **Retained as RESIDUE**, carried as R942-2 states it. |
| R941-4-S1 to S5 | **Retained** as optional suggestions. |

## 5. Lens results and reviewer-owned ledger

[R941] PASS Conformance - `receipts/adp_rv32_object_diff.txt`, `SPLIT_CONTROL_MEMORY.md` (#1009 figures, base `c34e7d8b`), `third_party/tsn-c-stack` `a795471c` `src/adp.c:309-315`, `receipts/composition.txt` - the composition changes no file in the PR's conformance scope: the store, the DR2a window and the binding class. The predecessor's ADP length rule leaves the PR's stated ROM bytes and timings unchanged, because the object is the same size and layout with two instructions swapped. The source conformance verdicts of R942-2 and R941-4 at `079c4fa1` carry.

[R941] PASS RTL - `receipts/composition.txt` (no PR path under `hdl/`, gitlinks `gptp-processor` `3ce71b76` and `protocol-processor` `801ef228` from the first parent), `tb/verilator/ctrl_service_budget/split_soc.py:221`, `syn/yosys/rom_digests.tsv` - the PR carries no RTL. The predecessor's gPTP RTL is not instantiated by the PR's harnesses, and the digest ledger is keyed per processor pin. The composition does not touch the PR's RTL scope. R942-2 and R941-4 (R941-3 at the same head) cover it at `079c4fa1`.

[R941] PASS Robustness - `receipts/firmware/ctrl_nvm.log` (5 shapes, 656 tests), `receipts/selftests/budget.log` (#1009 bind grade and mutants), `receipts/selftests/split_target.log` - the composition does not touch the PR's robustness scope, which covers the window class boundaries, in-flight binds and the verify's byte coverage. Those suites still pass on the candidate. The source rounds R942-2 and R941-4 at `079c4fa1` carry.

[R941] PASS Tests - `receipts/firmware/fw_coverage.log`, `ctrl_fw.log`, `ctrl_nvm.log`, `receipts/gates/ci_events_check.log`, `ci_events_selftest.log`, `ci_gate_workflows.log`, `.github/workflows/rtl-fast.yml:893-902` - the composition touches this lens. The PR's ratchet and tests run beside the predecessor's tsn-c-stack pin, legs and ctrl tests. The coverage ratchet, both firmware suites, the CI inventory checks and both harness self-tests pass at the candidate.

[R941] PASS Docs - `sw/firmware/gtest/README.md:246-247,291,299,330`, `receipts/gates/{docs_check,docs_inventory,doc_map,toc_check,toc_anchors,em_dash,submodule_docs,doc_paths,doc_style}.log` - the composition touches this lens through one shared file in disjoint hunks. Its tsn-c-stack links name `a795471c`, the candidate's gitlink. Every docs registry, TOC, anchor and em-dash gate passes at the candidate.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | composition.txt; adp_rv32_object_diff.txt; SPLIT_CONTROL_MEMORY #1009 figures; tsn-c-stack adp.c at both pins | R941-5 (composition); R942-2, R941-4 (source) | 04a20c74d986e6d939d517a469bcbbdf37a8377d (source: 079c4fa1514be460949ddc28ae3277ea1873cb48) |
| RTL | CLEAN (composition does not touch its scope) | composition.txt (gitlinks, no PR RTL); split_soc.py:221; rom_digests.tsv | R941-5 (composition); R942-2, R941-4/R941-3 (source) | 04a20c74d986e6d939d517a469bcbbdf37a8377d (source: 079c4fa1514be460949ddc28ae3277ea1873cb48) |
| Robustness | CLEAN (composition does not touch its scope) | ctrl_nvm.log; budget.log; split_target.log | R941-5 (composition); R942-2, R941-4 (source) | 04a20c74d986e6d939d517a469bcbbdf37a8377d (source: 079c4fa1514be460949ddc28ae3277ea1873cb48) |
| Tests | CLEAN | fw_coverage.log; ctrl_fw.log; ctrl_nvm.log; ci_events / ci_gate_workflows logs; both self-test logs | R941-5 | 04a20c74d986e6d939d517a469bcbbdf37a8377d |
| Docs | CLEAN (S1 optional; prior RESIDUE carried) | gtest README shared hunks; 9 docs gate logs | R941-5 | 04a20c74d986e6d939d517a469bcbbdf37a8377d |

## 6. Real limits and pending manager duties

- **Not run here:** no manager source bank, builder bank, native bank, full Verilator, protocol-processor, gPTP or Yosys bank, Vivado routing, hosted or act run. None is claimed or inferred. The candidate is a local commit with no hosted check runs; the check-runs API returns 422 for it.
- **Toolchain:** the firmware gates used the pinned RV32 SDK, extracted from an archive whose sha256 matches the pin, and the pinned GoogleTest 1.14.0. The renderer-dependent docs gates used the pinned Markdown renderer (`tools/markdown/requirements.txt`, `--require-hashes`) in a private virtual environment.
- **Not hardware proof:** physical calibration was NOT RUN, and field skips do not count as hardware proof. Board acceptance of the bind window rests on the source rounds' public evidence and the manager's rulings.
- **Manager duties at the merge turn:**
  - Build and gate the current-dev-soft-core merge candidate with the builder and native banks.
  - Confirm that the tip is still `ba13338b`, or a descendant whose tree changes nothing; the candidate tree `f3839b37` is that merge today.
  - Take routed totals of the merged tree, which include the predecessor's gPTP `3ce71b76` RTL, against the LUT band of issue criterion 2.
  - Take exact-head hosted and act evidence.
  - Carry RESIDUE R941-4-RES1 to RES4 and R942-2-RES1 to the residue checklist.
  - Check post-merge containment.
- **Clone restored:** HEAD, tree, `write-tree`, the index (mode, blob, path) and the working tree all equal `04a20c74`/`f3839b37`. There are zero untracked or ignored entries. The five initialised gitlinks match HEAD and are clean. Receipt: `restore_check.txt`.

R941-5 FINISHED

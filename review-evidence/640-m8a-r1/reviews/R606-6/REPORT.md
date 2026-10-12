[R606] POSITIVE - exact head b503c41b8fe3b5276b6650a6058458b9ac2c609c

Composition review R606-6, issue #640 (lane M8a-1) / PR #721. Candidate `b503c41b8fe3b5276b6650a6058458b9ac2c609c`, tree `1385e356e7fd5fa7095d795cd36d119a2b4f135a`, parents dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae` and PR head `42678ae2f77fbbef056f7fb99859e0193181e6d7`. Public review start: PR #721 comment 6131048253.

- Scope: composition acceptance only. The PR source head `42678ae2` already holds two independent POSITIVE source reviews, R606-5 (PR comment 6119365890) and R607-5 (PR comment 6119358678).
- Result: the composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR, MINOR or RESIDUE is open. One new SUGGESTION is recorded, and it concerns dev-owned text. All five lenses are covered clean at this head.
- Independence: the verdict and ledger below were formed before prior public findings were read. Those findings were read afterwards only to resolve or retain them (section 6). No private author material, lane scratchpad, management checkout or concurrent reviewer report was read. The author evidence tree was listed but not opened.

## 1. Reconstruction

- Contract: AGENTS.md sections 6-7 and CONTRIBUTING.md.
- Issue #640:
  - acceptance and the owner decisions (body);
  - the M8a lane assignment (comment 6100371426);
  - ruling 6101485877 (224 KB, no power-of-two waste, the split image owns the reset entry, two-step sequencing);
  - the round-5 assignment (6118560882);
  - the author's round-5 REVIEW READY at `42678ae2`.
- Predecessor in the candidate: dev `dc4d06cb` = PR #724 (#716). It splits `firmware-unit` into four required firmware jobs, each with a 45-minute timeout. Commits `b27c5537`, `f41e4f2d` and `941e1559` sit on the PR's last dev merge, `c6bd08c6`.

## 2. Composition identity

| Check | Result | Receipt |
|---|---|---|
| `git merge-tree --write-tree dc4d06cb 42678ae2` | `1385e356…` = the candidate tree, a clean automatic merge with no conflict | `receipts/overlap_merge.txt` |
| Paths changed on either side since merge base `c6bd08c6` | 24 paths. 19 are PR-only and equal the PR-head blobs. 4 are #716-only and equal the dev blobs. 1 is shared and merged: `docs/testing/CI_WORKFLOWS.md`. No candidate-vs-dev difference outside the PR's file set | `receipts/blob_identity.txt` |
| Shared file `docs/testing/CI_WORKFLOWS.md` | Changed-line digests: candidate-vs-dev equals the PR side (`a1119f97…`), and candidate-vs-PR equals the #716 side (`9627ec51…`). The merged page carries exactly both sides' lines, with none lost or duplicated | `receipts/overlap_merge.txt` |
| Submodule gitlinks | All 5 are identical to dev `dc4d06cb`. `gptp-processor`, `protocol-processor` and `verilog-axis` are checked out at their gitlinks | `receipts/integrity.txt` |
| `git diff --check dc4d06cb..b503c41b` | clean | `receipts/integrity.txt` |

## 3. Semantic interactions examined

1. **`CI_WORKFLOWS.md`, #716's text (`:44-105`).**
   - The page says there are four firmware jobs, each requiring `changes`, under one relevance condition (`:64-67`), with 45 min / 1890 s / 1620 s rows, and that a docs-only change skips all four (`:104-105`).
   - These statements match `.github/workflows/rtl-fast.yml:317-473`: four jobs, each `if: needs.changes.outputs.rtl == 'true'`, `timeout-minutes: 45`, and all required by the `rtl-fast` aggregate.
   - `ci_events.py --check` passes over 2016 contract items, and that check reads this table: a planted `40 min` in the srp row fails by name (`receipts/probes/probe_doc_fw_timeout.log`).
2. **`CI_WORKFLOWS.md`, this PR's text.**
   - `:120` says "Seven pages". `scripts/ci_scope.py:66-74` `GATE_READ_DOCS` has exactly 7 entries, and the paragraph names all 7.
   - `:138-141` (the `test_ctrl_memory` reader) and `:1265-1276` (the elaborate job's RV32 SDK and LiteX member) describe `elaborate.yml`, which neither side changed.
   - The PR's added lines never mention the firmware jobs, so #716 made none of them false.
   - #716's "All jobs verify the same pinned SDK" stays true: the SDK cache key is identical in `docs.yml:191`, `elaborate.yml:247` and `rtl-fast.yml:344,390,424,458` (`receipts/sdk_keys.txt`).
3. **The PR's `scripts/ci_scope.py` against #716's workflow.** All four firmware jobs, `publication-census`, lint and Yosys consume the one `changes.outputs.rtl`, which comes from `ci_scope.py` via stdin (`rtl-fast.yml:64`). I fed each of the PR's 20 paths through the candidate's classifier exactly as that job does (`receipts/scope_probe.txt`):
   - `SPLIT_CONTROL_MEMORY.md` and `AREA_BUDGET.md` → `true`, so all four firmware jobs run;
   - every `sw/`, `syn/` and `scripts/` path → `true`;
   - the other docs pages, including `CI_WORKFLOWS.md` → `false`;
   - a docs-only subset of the PR → `false`, so all four firmware jobs are skipped, as the page states;
   - the whole PR list and the whole candidate list → `true`.
4. **Firmware directory sharing.**
   - The PR's `sw/firmware/ctrl/test/ctrl_srp_image.py` and `plat/*` are not referenced by `test_ctrl_firmware.py`, the shard census, `rtl-fast.yml` or `ci_events.py`.
   - Its imports (`ctrl_build`, `srp_arms`, `ctrl_arms`, `fw_gtest`, `fw_rv32`, `nvm_bench`, `aecp_arms`, `ctrl_memory`) were not changed by #716.
   - The coverage ratchet reads `sw/firmware/gtest/README.md`, not the `sw/firmware/ctrl/README.md` that this PR edits.
   - On the candidate, both `ctrl_srp_image.py --help` and `test_ctrl_firmware.py --help` exit 0, and the latter offers `--shard` (`receipts/import_smoke.txt`).
5. **TOC, anchors and the docs map** over the merged page: see the gate table in section 4.

## 4. Gates run on the candidate (concurrent, `scripts/run_gates.sh`, rc 0 for all 16)

The receipts are in `receipts/candidate/<gate>.{log,rc}`. The pinned Markdown renderer was installed in a private venv from `tools/markdown/requirements.txt` with `--require-hashes` (`receipts/env.txt`). A first attempt without that renderer refused to judge (rc 2); its logs were discarded and every gate was re-run.

| Gate | Result |
|---|---|
| `docs_check.py` | 0 findings, 205 md + 1278 scrubbed files |
| `check_em_dash.py --base dc4d06cb` | 0 findings over 324 added lines in 10 pages |
| `gen_toc.py --selftest` / `--verify-anchors` / `--check` | 1501/1501 arms; 485 cross-page fragments; 145 pages OK |
| `check_doc_style.py`, `check_doc_paths.py`, `DOC_MAP.gen.py --check` | OK |
| `ci_events.py --check` / `--selftest` / `--firmware-census` | OK over 2016 items, including `CI_WORKFLOWS.md`; PASS with 2828 arms; census emitted |
| `ci_scope.py --selftest` | PASS |
| `check_py_idiom.py` / `--selftest` | PASS; 54/54 |
| `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py` | PASS |
| `check_hygiene.py --check` | PASS |

## 5. Fault probes (`scripts/probes.sh`; each restored from HEAD; `receipts/probes/`)

| Probe | Gate | Result |
|---|---|---|
| Drop `SPLIT_CONTROL_MEMORY.md` from `GATE_READ_DOCS` | `ci_scope.py --selftest` | rc 1, caught (2 failures) |
| Drop the PR's classification case | `ci_scope.py --selftest` | rc 1 |
| Make `firmware-srp-mutants` run when `rtl == 'false'` | `ci_events.py --check` | rc 1, caught (`if` and census) |
| Duplicate shard 2/4 in place of 3/4 | `ci_events.py --check` | rc 1, caught |
| `CI_WORKFLOWS.md` srp row 45 → 40 min | `ci_events.py --check` | rc 1, caught by name |
| Rename the `## Elaboration` heading | `gen_toc.py --check` | rc 1, TOC drift |
| "Seven" → "Six" pages | `docs_check.py` | rc 0. Prose count is not machine-checked; I verified it by hand (section 3.2) |
| Em dash in the PR paragraph (working tree) | `check_em_dash.py` | rc 0. The probe is invalid by design: the checker reads the committed range, not the working tree. The committed-range run is in section 4 |

After the probes: the worktree and index equal HEAD, the index tree is `1385e356…`, the gitlinks are unchanged and the status is clean (`receipts/integrity.txt`).

## 6. Prior public findings at this head

All of the PR's artifacts other than `CI_WORKFLOWS.md` are blob-identical to `42678ae2` (section 2), so every disposition by R606-5 and R607-5 carries over unchanged.

| Finding | Status at `b503c41b` |
|---|---|
| R606-4-F1 = R607-4-F1, MINOR; R606-4-R1, R606-3-R1, R607-3-R1, R607-1-R1/R2, R606-1-R1/R2, RESIDUE; R606-1-F1..F5, R607-1-F1..F3, R606-2-F1 BLOCKER, R606-2-F2 MAJOR, R606-2-F3 MINOR, R607-2-F1 MINOR | Resolved and preserved. The artifacts are byte-identical to the reviewed source head. R606-2-F1's `ci_scope.py:69` registration survives the merge and is probe-enforced (section 5) |
| R606-5-S1; R606-4-S1; R606-2-S1..S5 (S5 = R607-1-S3, #723); R606-3-S-a/b/c, SUGGESTION | Retained, optional, unchanged |

## 7. Findings

### R606-6-S1 - SUGGESTION - Docs - `scripts/ci_scope.py` module docstring ("rtl-fast's `firmware-unit` job ... gates on the same answer")

- **Evidence:** after #716, four firmware jobs gate on the classifier's answer (`rtl-fast.yml:317-438`). The docstring names one.
- **Why not a finding against this lane:**
  - The sentence is dev-owned. This PR does not change that hunk.
  - The sentence is still true.
  - `CI_WORKFLOWS.md:64-67` states the four-job rule authoritatively.
- **Optional outcome:** name all four jobs, or "the firmware jobs", in a later dev change.
- **Verification:** `ci_scope.py --help`.

## 8. Reviewer-owned ledger

| Lens | State | Composition touches its scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Yes, for the CI contract: the merged `CI_WORKFLOWS.md` against `rtl-fast.yml` and `elaborate.yml`. The M8a-1 fit acceptance is untouched (blob-identical) | `CI_WORKFLOWS.md:44-105,120-141,1265-1276`; `rtl-fast.yml:64,317-473`; `ci_scope.py:66-74`; `receipts/candidate/ci_events_check.log`, `receipts/scope_probe.txt` | R606-6; the fit acceptance by R606-5 and R607-5 | `b503c41b8fe3b5276b6650a6058458b9ac2c609c`; fit at ancestor `42678ae2f77fbbef056f7fb99859e0193181e6d7`, untouched since |
| RTL | CLEAN | No. No `hdl/`, `configs/`, `sw/litex/` or `syn/` blob differs from the reviewed source or from dev, and no gitlink changes. The adjacent job wiring is CI scope | `receipts/blob_identity.txt`, `receipts/integrity.txt` (gitlinks) | R606-5 and R607-5 (`milan_soc.py`, `ctrl_memory.py`, `ctrl_split.ld`, `ctrl_split_start.S`, `ctrl_memory_ooc.py`); identity confirmed by R606-6 | `42678ae2f77fbbef056f7fb99859e0193181e6d7`, unchanged in `b503c41b8fe3b5276b6650a6058458b9ac2c609c` |
| Robustness | CLEAN | Yes, for classifier behaviour under the four-job layout: the docs-only skip, the gate-read page, and the `if`/shard faults | `receipts/scope_probe.txt`; `receipts/probes/probe_fw_job_if_unscoped.log`, `probe_fw_shard_duplicated.log`, `probe_drop_gate_read_doc.log` | R606-6; the memory-layer robustness by R606-5 and R607-5 | `b503c41b8fe3b5276b6650a6058458b9ac2c609c`; memory layer at `42678ae2f77fbbef056f7fb99859e0193181e6d7`, untouched since |
| Tests | CLEAN | Yes, for the gate inventories: the `ci_scope` self-test, the `ci_events` contract, self-test and census, and the shard partition test | `receipts/candidate/*.log` (16 gates, rc 0); 6 of 6 valid probes caught (section 5) | R606-6; `test_ctrl_memory.py` by R606-5 and R607-5 | `b503c41b8fe3b5276b6650a6058458b9ac2c609c`; `test_ctrl_memory.py` at `42678ae2f77fbbef056f7fb99859e0193181e6d7`, untouched since |
| Docs | CLEAN | Yes: the one merged page, plus the TOC, anchors and docs map | `docs/testing/CI_WORKFLOWS.md` (merged hunks, line by line), `receipts/overlap_merge.txt`; `docs_check`, `gen_toc` ×3, `check_em_dash --base dc4d06cb`, `doc_style`, `doc_paths`, `DOC_MAP` logs. The other 8 PR pages are blob-identical to `42678ae2` | R606-6; the other pages by R606-5 and R607-5 | `b503c41b8fe3b5276b6650a6058458b9ac2c609c`; the other pages at `42678ae2f77fbbef056f7fb99859e0193181e6d7`, untouched since |

## 9. Real limits

- The candidate was not pushed (GitHub reports no commit `b503c41b`), so there is no hosted or Actions-replica evidence at this exact head.
  - The source head `42678ae2` has hosted successes. That run used the pre-#716 single `firmware-unit` job, and Physical gPTP was skipped.
  - Dev `dc4d06cb` ran the four firmware jobs successfully. Verilator shards 1/5 and 2/5 were still in progress when sampled (`receipts/hosted_checks.txt`).
  - Neither run executed the composed tree.
- Not run here, because the composition changes none of their inputs (blob identity, section 2):
  - the firmware suites and mutation campaigns;
  - the LiteX aggregate and `test_ctrl_memory`;
  - the builder;
  - Verilator and Yosys;
  - the `ctrl_memory` fit links and mapping.
- The local interpreter is CPython 3.14, while the hosted docs job uses 3.12. The renderer wheels are the hash-pinned ones.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## 10. Pending manager duties

- Build and validate the current-dev merge candidate: the builder and native banks, and the Actions replica and hosted contexts for the candidate, including the four firmware jobs and `elaborate` with `test_ctrl_memory`. Link the receipts on the PR.
- Merge only with explicit maintainer authorization. Then run the post-merge containment.
- Carry R606-6-S1 and the retained optional suggestions as the manager sees fit. No RESIDUE is open.
- M8a-2 remains open: the integrated route, the split-image boot and the service checks.

R606-6 FINISHED

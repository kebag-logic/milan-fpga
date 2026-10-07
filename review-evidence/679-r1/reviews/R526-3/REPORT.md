[R526] POSITIVE - exact head af5be4710c3516cc247c353213d6939fa8d23f57

R526-3 independently applied all five lenses to the composition of issue #679 / PR #683. The composed tree introduces no defect beyond the reviewed sources. All five lenses are CLEAN. There are no new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION findings. R526-1-F1 remains resolved. This verdict covers composition acceptance only.

Reviewed tree: `c2aaa434de409dd97074d71567c2df41d38af65e`. Ordered parents: predecessor candidate `72d3780d23a0b96362f8ae64059311b866ff5776` and reviewed PR source `04e1435a218908d2b12b4053e5dab2c2dcac2ebf`. The original PR source base is `6714181d0c8a16e2983f85b724f4d688f5111835`. The stated live dev `79b086d44eb62d007d38e18f5618b98e8e2a33e6` and the candidate's first parent both have tree `286ad25c56908e8d1987ae90db41a474c70a6fba`. This proves equality of those inputs, not completion of the manager's final merge turn. See `tree-identities.json`, `candidate.diff`, `composition-from-source.diff` and `history.log`.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/679), its [assignment](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6021510923), [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6022358702) and public scope decisions, requirements/interfaces, then the complete requested diff/history and public executable evidence. The ruling accepts object sizes and individual static frames; linked-image sizing and whole-program stack bounds remain integration obligations. No private author material was read. `independent-verdict.md` records the independently written verdict and ledger before prior public review bodies were opened.

The source reviews carried forward are [R526-2](https://github.com/kebag-logic/milan-fpga/pull/683#issuecomment-6023315222) and [R527-2](https://github.com/kebag-logic/milan-fpga/pull/683#issuecomment-6023392064), both POSITIVE at `04e1435a218908d2b12b4053e5dab2c2dcac2ebf`. Composition checks below establish retention and examine the new interactions; they do not repeat the complete source review.

`docs/testing/CI_WORKFLOWS.md` is the only file changed both by the PR's 15-file delta and by the additional predecessor changes relative to the PR source base. Thus the overlap is not empty. Commit `26bd6334a` adds the per-suite policy; `793dcd3f7` adjusts historical deadline references. The PR changes the separate firmware-unit paragraph. Raw three-way merging of the source/base/predecessor document reproduces the candidate bytes exactly. All other 14 PR entries match the reviewed source in mode and object ID. Every path outside the PR delta matches the predecessor. `composition.log` enumerates every PR path and every retained additional predecessor path.

Historical FT also touched ten PR paths: `.github/workflows/rtl-fast.yml`, `docs/testing/CI_WORKFLOWS.md`, `scripts/ci_events.py`, `sw/firmware/ctrl/README.md`, `sw/firmware/ctrl/test/ctrl_arms.py`, `sw/firmware/ctrl/test/ctrl_build.py`, `sw/firmware/ctrl/test/test_ctrl_firmware.py`, `sw/firmware/ctrl_nvm/README.md`, `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py`, and `sw/firmware/gtest/README.md`. Those FT changes were already in the reviewed PR source base. Their predecessor entries equal that base except for the known #673 document change. They are not an additional unreviewed firmware merge.

The semantic interactions were checked as follows:

- `docs/testing/CI_WORKFLOWS.md:188` agrees with `scripts/run_all_suites.sh:245`: default and mmcm_servo 1800 seconds, capture_coherence 2400, milan_dp_mclk 3600, milan_dp 4800, and scheduled milan_dp_gptp 5400. The actual shell function returned every documented value and honored an explicit override in all six cases. Historical measurements and timeout qualifications from #673 remain intact.
- `docs/testing/CI_WORKFLOWS.md:42`, `.github/workflows/rtl-fast.yml:273` and `sw/firmware/gtest/README.md:386` agree: SDK installation precedes the RV32 controls and both required firmware arms. Only the opt-in private-dependency arm and both full firmware mutation campaigns remain local. Object/frame reports are not presented as linked-image bounds.
- `scripts/ci_events.py:2362` retains the exact workflow step sequence, required flags, SDK/cache contract and aggregate dependency. Its check and mutation tests pass on the candidate, including stale/missing workflow records and removal of required compiler flags. No local container runner was executed.
- `scripts/ci_scope.py:22` classifies every changed firmware/workflow path as relevant. The classifier self-test scans the composed gate readers successfully. FT's tally, coverage ratchet and exclusion table remain source-identical.
- The predecessor's AAF changes and gate-reader registration remain predecessor-identical. `scripts/measure_test_evidence.py --check/--selftest` confirms the composed registry and deadline contract; shard tests retain the default/physical partition. The NVM record check passes all five shipping shapes, and the submodule-documentation check confirms all four recorded gitlinks.
- Documentation/privacy, contents generation, cross-page anchors, cited paths, feature status and the added-line punctuation gate all pass. No duplicate table, stale anchor or lost policy paragraph was found.

Every command below returned zero on the exact candidate. Each receipt basename has a full `.log`, a `.rc`, and a `.json` command/duration record. Independent gates ran concurrently under a foreground supervisor with six workers; all children were joined.

| Executed command or probe | Result | Receipt basename |
|---|---|---|
| `composition_probe.py` | Exact inputs, overlap, retained entries, raw document merge, six deadlines/overrides, required steps and classification PASS | `composition` |
| `python scripts/docs_check.py` | 0 findings; 198 Markdown files, 1123 scrubbed text files; 23/23 scrub controls | `docs_check` |
| `python scripts/gen_toc.py --check` | 138 contents lists pass | `toc_check` |
| `python scripts/gen_toc.py --verify-anchors` | 388 existing cross-page fragment links reproduced | `toc_anchors` |
| `python scripts/check_em_dash.py --base 72d3780d23a0b96362f8ae64059311b866ff5776` | 0 findings over 72 added lines in four pages; 339/339 controls | `em_dash` |
| `python scripts/ci_events.py --check` | 1741 contract items pass | `ci_events_check` |
| `python scripts/ci_events.py --selftest` | 2361 mutation arms pass | `ci_events_selftest` |
| `python scripts/ci_scope.py --selftest` | PASS | `ci_scope` |
| `python scripts/check_doc_style.py` | 22 current documents pass | `doc_style` |
| `python scripts/check_doc_paths.py` | 933 cited paths resolve; ten line anchors valid | `doc_paths` |
| `python scripts/check_feature_status.py` | 0 findings | `feature_status` |
| `python scripts/measure_test_evidence.py --check` | Ratchets and runner contract pass; 60 default suites retained | `test_evidence_check` |
| `python scripts/measure_test_evidence.py --selftest` | 105/105 checks pass, including deadline mutations | `test_evidence_selftest` |
| `python scripts/check_nvm_record_space.py` | 0 findings across five shapes | `nvm_record_space` |
| `python scripts/suite_shards.py --selftest` | Partition, dedicated-suite and negative-input checks pass | `suite_shards` |
| `python scripts/check_submodule_docs.py` | Four exact gitlinks pass | `submodule_docs` |
| `integrity_probe.py` | Every tracked blob/mode/index and required submodule population matches | `integrity` |

The first reviewer composition probe had an assertion error: it treated the already identified shared document as an equality-only path. `composition_initial.log` retains that nonzero result. The corrected probe excludes the known overlap from that assertion and separately checks its exact raw three-way merge. No source was changed to obtain a pass. Locked Markdown dependencies were installed only under packet scratch; no shared installation occurred.

Prior finding disposition: **R526-1-F1, MAJOR, RESOLVED AND RETAINED**. All attributable lenses: **Conformance, Robustness, Tests, Docs**. Artifacts: `sw/firmware/ctrl/test/ctrl_arms.py:163`, `sw/firmware/ctrl_nvm/test/nvm_rv32.py:68`, `sw/firmware/gtest/fw_rv32_selftest.py:107` and `:132`, `sw/firmware/gtest/README.md:358`.

- Authority/evidence: the [public finding](https://github.com/kebag-logic/milan-fpga/pull/683#issuecomment-6022774174) and [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6022780134) require external references to resolve only through global or weak definitions.
- Previous impact: a same-name local definition could conceal an unapproved unresolved runtime service from either object check.
- Required outcome: both real arms reject the dependency, preserve valid resolution, carry effective compiled controls and state the guarantee accurately.
- Verification at this composition: both `--extern-only --defined-only` queries, both same-name static controls, the allowlists and the corrected guarantee are byte-identical to the exact source head re-reviewed positively by R526-2 and R527-2. Their compiled rejection/positive controls remain banked at that source head; they were not rerun in this composition round. No predecessor changes those inputs. The finding is not deferred or relabeled.

The four prior public review comments were reconciled after the independent verdict. They contain this one finding; both corrected-head reviews resolve it and report no additional findings. Submitted-review and inline-comment endpoints contain zero records. `public/issues-683-comments.json`, `public/pulls-683-reviews.json` and `public/pulls-683-comments.json` retain that snapshot.

Reviewer-owned ledger (CLEAN is limited to the assigned composition scope):

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition touches CI acceptance: issue #679/ruling 6022358702; REQUIREMENTS.md:306; `.github/workflows/rtl-fast.yml:273`; `docs/testing/CI_WORKFLOWS.md:42`; `composition.log`. Required RV32 execution and object-only scope preserved. | R526-3 composition; source behavior covered by R526-2 and R527-2 | Composition `af5be4710c3516cc247c353213d6939fa8d23f57`; source `04e1435a218908d2b12b4053e5dab2c2dcac2ebf` |
| RTL | CLEAN | Composition does not touch the PR's RTL/interface scope: `candidate.diff`, `composition.log`, `integrity.log`; production C, shipping inputs and gitlinks retained; predecessor `hdl/ieee1722/aaf/KL_aaf_packetizer.sv` retained exactly. No new firmware/AAF coupling. | Covered by source reviews R526-2 and R527-2; R526-3 verifies absence of a composition interaction | Source `04e1435a218908d2b12b4053e5dab2c2dcac2ebf`; retention `af5be4710c3516cc247c353213d6939fa8d23f57` |
| Robustness | CLEAN | Composition touches CI refusal/timeout contracts: `scripts/run_all_suites.sh:245`, `scripts/ci_events.py:7763`, `ci_events_selftest.log`, `test_evidence_selftest.log`; runtime checks and fixes source-identical. | R526-3 composition; firmware adverse-input coverage remains R526-2 and R527-2 | Composition `af5be4710c3516cc247c353213d6939fa8d23f57`; source `04e1435a218908d2b12b4053e5dab2c2dcac2ebf` |
| Tests | CLEAN | Composition touches scheduling/registries: `scripts/ci_scope.py:22`, `scripts/measure_test_evidence.py`, `scripts/suite_shards.py`, `ci_scope.log`, `test_evidence_check.log`, `suite_shards.log`, `nvm_record_space.log`; 15 focused gates pass. | R526-3 composition; complete source campaigns covered by R526-2 and R527-2 | Composition `af5be4710c3516cc247c353213d6939fa8d23f57`; source `04e1435a218908d2b12b4053e5dab2c2dcac2ebf` |
| Docs | CLEAN | Direct overlap: `docs/testing/CI_WORKFLOWS.md:42` and `:188`; `sw/firmware/gtest/README.md:345`; `composition.log`, `docs_check.log`, `toc_check.log`, `toc_anchors.log`, `em_dash.log`, `doc_paths.log`. Both policies, tables and anchors retained. | R526-3 | `af5be4710c3516cc247c353213d6939fa8d23f57` |

The supplied [public evidence snapshot](https://github.com/kebag-logic/milan-fpga/tree/4c5eb3ab1e9ceeb076a9e274fd1a4c8cf52f72d0/review-evidence/679-r1) was inspected after the diff. Eight selected evidence files matched their published SHA-256 values. Its 15-control results and partial builder receipts are historical source evidence, not fresh 17-control or candidate-bank evidence. The issue's round-2 REVIEW READY records the later 17 controls and complete campaigns; the two independent source reviews assess that corrected head.

The assignment reports candidate builder 48/48 and native 5/5 at `af5be471`, supported local replica PASS at source `04e1435a`, and hosted 22/22. Those remain manager-reported evidence: this round did not rerun those banks or inspect hosted job execution. No skipped context is promoted to executed validation. The retrieved manager comments identify scope and review starts; the manager must attach or identify the superseding complete bank receipts and accept the exact-head hosted/local-replica evidence.

Remaining manager duties are to publish this packet, reconcile both independent source reviews and this composition ledger, confirm no review remains in flight, construct/record the final candidate against current dev at the merge turn and meet the required local/hosted bar, obtain merge authorization, then perform post-merge containment and issue/project closure. A different final tree requires reassessing affected composition coverage.

Full parent, processor, gPTP, synthesis and builder banks, full firmware campaigns and optional private-dependency execution were not run here. No RTL compiler was needed for these composition gates. Linked runtime compatibility, bootability, nested-call/interrupt stack bounds and target service timing remain integration obligations. Physical calibration was **NOT RUN**. Field skips and desk checks are not hardware proof.

Final integrity proves 1147 superproject tracked blobs and all 1151 stage-zero entries, including executable/symlink modes. It also proves registered submodule heads, indexes and every tracked byte: protocol-processor `ead8036035affd53ef4b29979190f2f4f67084c0` (558 blobs), gptp-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104), and third_party/verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214). The optional external gitlink remains unchanged and uninitialized. The detached checkout is clean. No tracked source edits, commits, pushes, GitHub writes, author contact, delegation, container execution, privilege, shared installs, hardware access or merge occurred.

`REPRODUCE.md` and the portable scripts reproduce the focused checks. `MANIFEST.sha256` lists every publishable file; scratch is excluded. Local path normalization in two setup/probe logs is recorded with original and publication hashes in `publication-normalization.json`; raw originals remain in unpublished scratch. All successful gate logs retain their original command output.

R526-3 FINISHED

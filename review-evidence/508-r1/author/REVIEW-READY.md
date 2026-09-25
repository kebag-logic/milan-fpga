[A295] REVIEW READY

Commit: `6a9828c172aa4d5d8ee49725e357a10bae2caa52`
Branch: `508-pp-pin-adopt` (local, unpushed). Assignment items 1-3 are complete. The superproject and all three required submodules are clean. No PR was created or edited.

Changed:

- Merged the requested dev commit `c266432dcb0cdd464205823a3d82cad260eedde2` in merge commit `cec6b99da7b26ce9962bcf9a6c05161c9f99439a`. Retained both sides in all five conflicts: CHANGELOG, TESTING, the test-evidence dispositions, the datapath Makefile, and its README. Both GSI and GM-step legs, controls, dispositions and historical measurement rows remain.
- Advanced the processor gitlink to `990f96526bb89356c963a260ebbdcf2a77e6623a`. Re-recorded ROM digests using `cd syn/yosys && ./ooc.sh --record-rom-digests` (rc 0); no manual digest or processor source edits. Updated SUBMODULES, CHANGELOG and the regenerated diagram.
- Extended the adopted-change table with processor [#116](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/116) / [PR #117](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/117) (parent-gate fixes, no behavior or port change), and [#113](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/113) / [PR #115](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/115) (latency-only GET_STREAM_INFO notification). Earlier adopted issues #92, #93, #94, #43, #49 and #112, through PRs #109, #110, #111 and #114, remain listed.

Latency notification: no existing parent notify/[GSI] check drives an isolated latency-only refresh. `tb/verilator/milan_dp/sim_nxn.cpp:gsi_talker_failed()` fixes latency at 500000 ns. G5 changes latency alongside registration/failure data and observes the coalesced notification; G6 keeps latency unchanged, and G7 changes only FailureInformation. Earlier notify phases do not register a Talker attribute. No check adaptation was needed. Isolated latency-only coverage remains in the processor PR #115 response tests.

Validation: all 65 gate commands returned rc 0 at the exact final head, from cleared generated outputs. Commands ran in the foreground without shell pipelines. The completion audit checked head identity, each exit, the complete synthesis inventory, clean trees and one-line commit messages without bodies or trailers.

| Gate | Result |
|---|---|
| Full builder with pinned SDK | rc 0; 471 audited compiler invocations using the assignment's argv[0]-only SDK mapping |
| Full builder without a cross compiler | rc 0; all three compiler candidates unavailable, entire builder executed |
| `make -C tb/verilator/pp_shadow` | 371 checks, 0 failures |
| Default `make -C tb/verilator/milan_dp run` recipe, executed in chunks | All 36 expanded recipe commands rc 0; chunks 1-12, 13-23, 24-30 and 31-36 all rc 0 |
| Notify/[GSI] leg | 345 checks, 0 failures |
| GM-step and default mutation controls | GM-step 48/0; render controls 6/6; GM-step controls 4/4 |
| `make -C tb/verilator/milan_dp_render` | Integration legs 152/0 and 60/0; control/defect checks 5/5 |
| `make -C tb/verilator/nvm_cosim` | 465/465 checks; 39/39 mutations caught by named checks |
| `make -C tb/verilator/milan_dp gsi-mutants` | 8/8: golden control plus seven mutations detected |
| `syn/yosys/run.sh --shard I/4 --results <evidence>/yosys-results`, I = 0, 1, 2, 3 | Each shard rc 0; 54/54 full synthesis tops; tied-input and tap-purity checks pass |
| `cd tests && behave --no-capture -f plain` | 14 features, 344 scenarios, 1739 steps; no failures or skips |

The builder reports its existing historical resource-calibration arm as NOT RUN in both modes because the placement report is absent. The compiler-absent mode additionally reports compiled census/instruments as NOT RUN. These arms are not claimed as executed passes.

The following checks also returned rc 0 at the final head:

```text
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/docs_check.py
env GIT_DIR=/nonexistent-508-a295-git python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/lint_rtl.py --check
git diff --check
```

Both documentation inventory modes passed. The installed HDL frontend ran with no new findings. Contract and naming allowances were unchanged; test-evidence remains within the existing budgets and its self-test passes 101/101. Diagram generation, raster manifest, submodule documentation and the requested-base-to-head whitespace check also pass. No assertion or ratchet was weakened.

Acceptance evidence: selector ownership and field lineage remain documented; the notify sweep checks both sinks, all four probing states, ACMP outcomes, 64-bit bridge IDs, changed/unchanged refreshes, withdrawal, requester exclusion, missing descriptors and reset. All seven GSI negative controls detect their named defects. The existing acceptance wording says PASSIVE after bind; as already recorded in round 1, the adopted processor contract and test show ACTIVE immediately on bind and PASSIVE after an unanswered retry. Round 2 preserves that distinction and makes no state-oracle change.

Handoff artifacts: `HANDOFF.md`, `PR-BODY.md`, `gates.jsonl`, `completion-check.json`, per-command logs and reproduction scripts in the assigned `508-a295` output directory. The handoff contains the five-file merge resolution, complete linked adoption table, ROM command, gate table and scope limits. Earlier setup retries and intermediate-head receipts are retained and explicitly superseded by the final-head results.

Open review items: independent reviews by [R306] and [R307], branch publication, hosted candidate checks and later merge remain pending. The firmware early return remains under #495; the #551 cold-pipeline case is unchanged and #553 owns its later flip. This comment records author validation; it does not supply a review verdict.

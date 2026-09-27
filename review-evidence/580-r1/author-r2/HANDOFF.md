[A368] Round 2 handoff for issue #580

Status: assigned local work complete; review-ready comment prepared in
`REVIEW-READY.md` for publication as a new issue comment. Independent re-review
remains pending. This report is executor evidence, not a review verdict.

Branch: `580-pp-pin-16be6768`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Starting head: `499b15f97eb0a469b7cd1308fbba7af3c64d1851`.
Final local head: `d02db63c367daf9adc7d709840bd81077e781d80`.
Final tree: `b13027cbe7f6ba11196446cb4ad3cd797a94b70f`.
Commit subject: `Remeasure capture evidence at processor pin 16be6768`.
Commit body and trailers: none. Worktree and initialized submodules: clean.
The final tree matches the pre-commit validated tree in `validated-tree.json`.
No push, PR creation/edit, merge, hardware operation, RTL/firmware edit, additional
checkout, or editing/deletion of existing comments was performed.

## Assignment and findings

The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5857045698) requires remeasurement and text corrections.
R352-1 F1 and R353-1 S1 are addressed by fresh capture evidence at the adopted pin.
R352-1 S1/S2 and R353-1 S2 are addressed by historical audit wording, processor PR
links and the explicit retained cluster minimum with parent #584 ownership.
These are executor resolutions awaiting independent re-review.

## Change list

- `tb/verilator/nvm_capture_cpu/measurements.json:2`: fresh run date, measured parent, six capture arms, recomputed hashes and commands; `:284` maxima, `:305` exact processor pins, `:310` measured tree and reproduction environment.
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1591`: section 18 measurement date, assignment, measured parent/tree/pin and timing evidence.
- `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:5`: historical audit pin; `:58`, `:134` and `:245`: retained cluster minimum and parent #584 ownership.
- `docs/reference/SUBMODULES.md:66`: processor PR 124/126 links and #122/#584 disposition.
- `CHANGELOG.md:36`: pin-adoption entry records fresh capture measurement and the cluster-minimum disposition.

## Capture provenance and old/new tables

Old measured parent: `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`.
Old measured tree: `ae5130212067a17666090f6647bcd11b0d428633`.
Its actual processor pin was `0922e43408f891fc0b84a84691df86b4fd0f1c0d`.
The starting receipt incorrectly relabelled those earlier results with `16be6768`.

New measured parent: `499b15f97eb0a469b7cd1308fbba7af3c64d1851`.
New measured tree: `83b988d3b59a398a7d0cd1977194c50be92522da`.
New processor pin: `16be6768f710e79450aace277abacd6c2c3336e5`.
The measurement source is the round-2 starting head. The final commit only updates
these five documentation/receipt files; it does not change the measured product,
firmware, harness, copy, hold, or gate. All six runs were rebuilt and executed.
Every field of all 96 fresh capture rows equals the corresponding old row.
Firmware, harness, CPU-netlist, BIOS, microcode and configuration hashes were
recomputed and also reproduce their earlier values.

The system timer is 100 MHz; each arm has 16 captures. Every capture has `ok=1`,
zero mismatches and zero open marks. ON arms have positive request, response and
read counts; OFF arms have zero counts. The census is 3,218 raw bytes / 53 records
for 1x1 and 12,634 raw bytes / 156 records for 8x8.

| Shape | CPU MHz | Traffic | Old ticks min–max | New ticks min–max | Old ms min–max | New ms min–max |
|---|---:|---|---:|---:|---:|---:|
| 8x8 | 50 | ON | 2429290–2430246 | 2429290–2430246 | 24.29290–24.30246 | 24.29290–24.30246 |
| 8x8 | 50 | OFF | 2425794–2426154 | 2425794–2426154 | 24.25794–24.26154 | 24.25794–24.26154 |
| 1x1 | 50 | ON | 659814–660642 | 659814–660642 | 6.59814–6.60642 | 6.59814–6.60642 |
| 1x1 | 50 | OFF | 658554–658857 | 658554–658857 | 6.58554–6.58857 | 6.58554–6.58857 |
| 8x8 | 100 | ON | 1899012–1900433 | 1899012–1900433 | 18.99012–19.00433 | 18.99012–19.00433 |
| 8x8 | 100 | OFF | 1978694–1979024 | 1978694–1979024 | 19.78694–19.79024 | 19.78694–19.79024 |

| Shape | CPU MHz | Old maximum ms | New maximum ms | 49 ms floor / maximum |
|---|---:|---:|---:|---:|
| 1x1 | 50 | 6.60642 | 6.60642 | 7.4170× |
| 8x8 | 50 | 24.30246 | 24.30246 | 2.0163× |
| 8x8 | 100 | 19.79024 | 19.79024 | 2.4760× |

The maximum 8x8 result is **24.30246 ms**, 0.19754 ms below the 24.5 ms STOP
threshold. No run exceeded the threshold. The hold remains nominally 50 ms,
with the unchanged 49 ms guaranteed floor.

Receipt: 25676 bytes; SHA256 `c86cd140445d253d77e8332f8763dc49a9a3ecefbf6d3d128576f4bf48728733`.
`old-measurements.json` preserves the starting receipt. `measured-tree.json`
records the measured pins and hashes; `final-state.json` identifies the final
local commit. The measured gPTP pin is `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`;
verilog-axis is `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

## Reproduction and environment

Capture used the existing product environment with its recorded component pins,
compiler 14.3.0 (RV32I, ILP32, -Os) and capture simulator 5.052. Default suites used
the pinned 5.050 simulator. Dependencies were resolved offline and each capture
ran under `unshare -Urn`. `PYTHONHASHSEED=0`, `COURSIER_MODE=offline` and
`SBT_OPTS=-Dsbt.offline=true` were set. `PYTHON` explicitly selected the same product
interpreter as `PRODUCT_PYTHON` for BIOS post-processing. The first build failed
before simulation when SDK Python was selected; a fresh build directory and the
correct interpreter resolved it. All six accepted runs completed with rc 0.

Documentation checks used the locked Markdown environment and the existing
pyslang 11.0.0 environment. Early documentation attempts found a sentence-length
violation, a missing parser in the system interpreter and disallowed duplicate
compiler wording. The sentence and receipt wording were corrected; the parser
check used the existing dependency environment. Every individual final gate
receipt is rc 0. Earlier failures remain explicitly named `*-failure` and are
not accepted evidence. Documentation runs resumed after these corrections;
`docs-gates.json` and the individual receipts identify all 33 executed checks.

`environment.json` identifies dependencies and binary hashes without copying
them. `capture-artifacts.json` records the byte count and SHA256 of each run's
capture log, measurement, source manifest, generated RTL, simulator executable,
BIOS and instrumented firmware. Build directories are under `/tmp/580-a368`.
Small run logs/manifests are retained here; generated trees and binaries are not.

Command variables below name existing dependencies: `PRODUCT_PYTHON` is the
product-environment interpreter, `PRODUCT_BIN` its bin directory, `SDK_BIN` the
recorded compiler's bin directory, `SUITE_BIN` the pinned 5.050 simulator bin,
`LOCAL_BIN` the user's utility bin, `MD_PYTHON` the locked Markdown interpreter,
`HDL_PYTHON` the interpreter with pyslang 11.0.0, and `EVIDENCE_DIR` the round-2
receipt directory. Capture used simulator 5.052 and compiler 14.3.0, RV32I/ILP32/-Os.
Commands ran in the physical `$LANES/580-pp-pin-16be6768` worktree,
in the foreground, without output pipelines. Per-gate receipts retain the exact
argv, cwd, exit status, duration, log byte count and SHA256.

- `env PATH=$SDK_BIN:$PRODUCT_BIN:$LOCAL_BIN:/usr/local/bin:/usr/bin:/bin PYTHON=$PRODUCT_PYTHON LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true unshare -Urn $PRODUCT_PYTHON -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir /tmp/580-a368/capture-8x8-50-on-retry` (rc 0; 16 captures).

- `env PATH=$SDK_BIN:$PRODUCT_BIN:$LOCAL_BIN:/usr/local/bin:/usr/bin:/bin PYTHON=$PRODUCT_PYTHON LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true unshare -Urn $PRODUCT_PYTHON -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir /tmp/580-a368/capture-8x8-50-off` (rc 0; 16 captures).

- `env PATH=$SDK_BIN:$PRODUCT_BIN:$LOCAL_BIN:/usr/local/bin:/usr/bin:/bin PYTHON=$PRODUCT_PYTHON LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true unshare -Urn $PRODUCT_PYTHON -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir /tmp/580-a368/capture-1x1-50-on` (rc 0; 16 captures).

- `env PATH=$SDK_BIN:$PRODUCT_BIN:$LOCAL_BIN:/usr/local/bin:/usr/bin:/bin PYTHON=$PRODUCT_PYTHON LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true unshare -Urn $PRODUCT_PYTHON -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir /tmp/580-a368/capture-1x1-50-off` (rc 0; 16 captures).

- `env PATH=$SDK_BIN:$PRODUCT_BIN:$LOCAL_BIN:/usr/local/bin:/usr/bin:/bin PYTHON=$PRODUCT_PYTHON LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true unshare -Urn $PRODUCT_PYTHON -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 --traffic on --build-dir /tmp/580-a368/capture-8x8-100-on` (rc 0; 16 captures).

- `env PATH=$SDK_BIN:$PRODUCT_BIN:$LOCAL_BIN:/usr/local/bin:/usr/bin:/bin PYTHON=$PRODUCT_PYTHON LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true unshare -Urn $PRODUCT_PYTHON -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 --traffic off --build-dir /tmp/580-a368/capture-8x8-100-off` (rc 0; 16 captures).

## Gate table

All six capture commands above and every gate below returned rc 0. The 33
documentation checks are listed individually. Source-affecting validation ran
on the final file content; the committed tree equals that content. Post-commit
whitespace and clean-worktree checks also returned rc 0.

| Gate | Command | rc / result | Receipt |
|---|---|---|---|
| capture-check | `python3 scripts/check_nvm_capture.py` | 0; new receipt accepted | `capture-check.json` |
| builder-rv32 | `env MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3 PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true python3 -u sw/builder/test_builder.py --require-rv32` | 0; 86 top-level tests; one calibration arm NOT RUN | `builder-rv32.json` |
| builder-absent | `env MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3 PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true python3 -u $MANAGEMENT/2026-09-23/580-a368/builder_absent.py` | 0; 86 top-level tests; calibration and RV32 instruments NOT RUN | `builder-absent.json` |
| rom-check | `syn/yosys/ooc.sh KL_chan_map_render` | 0; ROM digests accepted | `rom-check.json` |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0; classification accepted | `test-evidence.json` |
| port-contracts | `python3 scripts/check_port_contracts.py` | 0; contracts accepted | `port-contracts.json` |
| pp-shadow | `env PATH=$VALIDATION_TOOLS/verilator-v5.050/bin:$WORKSPACE_HOME/.local/bin:/usr/local/bin:/usr/bin:/bin taskset -c 0-7 make -C tb/verilator/pp_shadow` | 0; 2,068 checks; zero failures | `pp-shadow.json` |
| milan-dp | `env PATH=$VALIDATION_TOOLS/verilator-v5.050/bin:$WORKSPACE_HOME/.local/bin:/usr/local/bin:/usr/bin:/bin taskset -c 8-15 make -C tb/verilator/milan_dp VERILATOR_JOBS=8` | 0; 11,196 normal + 6 render + 4 GM-step checks; zero failures | `milan-dp.json` |
| current-artifacts-check | `python3 $MANAGEMENT/2026-09-23/580-a368/verify_artifacts.py` | 0; 65/65 hashes and sizes match public round-1 table | `current-artifacts-check.json` |
| docs_check | `python3 scripts/docs_check.py` | 0; pass | `docs_check.json` |
| docs_check-selftest | `python3 scripts/docs_check.py --selftest` | 0; pass | `docs_check-selftest.json` |
| check_doc_style | `python3 scripts/check_doc_style.py` | 0; pass | `check_doc_style.json` |
| check_doc_style-selftest | `python3 scripts/check_doc_style.py --selftest` | 0; pass | `check_doc_style-selftest.json` |
| check_gptp_docs | `python3 scripts/check_gptp_docs.py` | 0; pass | `check_gptp_docs.json` |
| check_gptp_docs-selftest | `python3 scripts/check_gptp_docs.py --selftest` | 0; pass | `check_gptp_docs-selftest.json` |
| check_solution_docs | `python3 scripts/check_solution_docs.py` | 0; pass | `check_solution_docs.json` |
| check_solution_docs-selftest | `python3 scripts/check_solution_docs.py --selftest` | 0; pass | `check_solution_docs-selftest.json` |
| check_submodule_docs | `python3 scripts/check_submodule_docs.py` | 0; pass | `check_submodule_docs.json` |
| check_submodule_docs-selftest | `python3 scripts/check_submodule_docs.py --selftest` | 0; pass | `check_submodule_docs-selftest.json` |
| check_diagram_pngs | `python3 scripts/check_diagram_pngs.py` | 0; pass | `check_diagram_pngs.json` |
| check_diagram_pngs-selftest | `python3 scripts/check_diagram_pngs.py --selftest` | 0; pass | `check_diagram_pngs-selftest.json` |
| check_archive | `python3 scripts/check_archive.py` | 0; pass | `check_archive.json` |
| check_archive-selftest | `python3 scripts/check_archive.py --selftest` | 0; pass | `check_archive-selftest.json` |
| check_em_dash-base | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/check_em_dash.py --base 682ecf0cb995473b72d5b4921088053ba753fc93` | 0; pass | `check_em_dash-base.json` |
| check_em_dash-selftest | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/check_em_dash.py --selftest` | 0; pass | `check_em_dash-selftest.json` |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0; pass | `doc-paths.json` |
| feature-status | `python3 scripts/check_feature_status.py` | 0; pass | `feature-status.json` |
| feature-status-selftest | `python3 scripts/check_feature_status.py --self-test` | 0; pass | `feature-status-selftest.json` |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0; pass | `module-matrix.json` |
| gen-hdl-reference-selftest | `/tmp/580-a366-docs-env/bin/python3 scripts/gen_hdl_reference.py --selftest` | 0; pass | `gen-hdl-reference-selftest.json` |
| baremetal-only | `python3 scripts/check_baremetal_only.py --check` | 0; pass | `baremetal-only.json` |
| rtl-source-lists | `python3 scripts/check_rtl_source_lists.py` | 0; pass | `rtl-source-lists.json` |
| timesync-check | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0; pass | `timesync-check.json` |
| timesync-selftest | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0; pass | `timesync-selftest.json` |
| doc-map-check | `python3 docs/DOC_MAP.gen.py --check` | 0; pass | `doc-map-check.json` |
| doc-map-selftest | `python3 docs/DOC_MAP.gen.py --selftest` | 0; pass | `doc-map-selftest.json` |
| submodule-boundaries-check | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0; pass | `submodule-boundaries-check.json` |
| submodule-boundaries-selftest | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0; pass | `submodule-boundaries-selftest.json` |
| gen-toc-selftest | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/gen_toc.py --selftest` | 0; pass | `gen-toc-selftest.json` |
| gen-toc-verify-anchors | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/gen_toc.py --verify-anchors` | 0; pass | `gen-toc-verify-anchors.json` |
| gen-toc-check | `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 scripts/gen_toc.py --check` | 0; pass | `gen-toc-check.json` |
| py-idiom | `python3 scripts/check_py_idiom.py` | 0; pass | `py-idiom.json` |
| diff-check | `git diff --check 682ecf0cb995473b72d5b4921088053ba753fc93` | 0; pass | `diff-check.json` |
| staged-diff-check | `git diff --cached --check` | 0; pass | `staged-diff-check.json` |
| committed-diff-check | `git diff --check 682ecf0cb995473b72d5b4921088053ba753fc93 HEAD` | 0; pass | `committed-diff-check.json` |
| worktree-diff-check | `git diff --check` | 0; pass | `worktree-diff-check.json` |

## Artifact and log evidence

All 65 regenerated current artifacts match the sizes and SHA256 values in the
[public round-1 old/new table](https://github.com/kebag-logic/milan-fpga/issues/580#issuecomment-5856703787): ten builder outputs plus the three AEM
outputs for each of five configurations. This round rebuilt only the adopted
pin and compared with that public table; it did not create an old-pin checkout.
`current-artifacts.json` contains the ten generation commands and all 65 results.
`builder-order.json` records both 86-test sequences. `suite-tallies.json` records
2,068 wrapper checks and 11,206 datapath/campaign checks, all with zero failures.

| Run or gate | Log bytes | Log SHA256 |
|---|---:|---|
| capture-8x8-50-on | 126721 | `82e8f1bd83476e155d7e1604cea16ca2d5983e768a24c2fa9dac542153756083` |
| capture-8x8-50-off | 125609 | `fd45a457766034df1eae57e420b0fb3469724234acf2d151d5d5bcc00578cb11` |
| capture-1x1-50-on | 125496 | `1c86b7981454dc7d17a8e2602ad9437b32e6da5d5b44b7d4ff43f0830415c785` |
| capture-1x1-50-off | 125562 | `e887af034c127db61e3b44626385a17759ec53f3bb48985dc5b27fabe0fe95ee` |
| capture-8x8-100-on | 125769 | `379c61fb48e888a9f47aa4aaa9c1fe4632fc8fbb83e97237ea59695b8f0380a4` |
| capture-8x8-100-off | 125803 | `5053583450a1c1de5203213ac6be41b0677b6d69a9fc7bbf719b9d1b022680fe` |
| capture-check | 324 | `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439` |
| builder-rv32 | 84499 | `25cc88c08b4282c0e8bf669ce48c9e9cec98b8a45f3492ff51621280a730e4a8` |
| builder-absent | 86751 | `1ded95cf0a8c83b75fb8a2ca83c6dc50480865d23283eb95c25051a488a2b6e2` |
| rom-check | 299 | `96813b468620e139df7f940979bc84641f5bf8519a2a70ae3334e010957bc2eb` |
| test-evidence | 10961 | `bcf70fde889a7765d72f22e992e88b6f7ce0372f2207813c2bd34dc30ba48428` |
| port-contracts | 421 | `eed4188366eced1ee727819ad607f9af837b98bee5d2ec97d18f375cdb0b00fd` |
| pp-shadow | 212846 | `aa6b1bb30b60bbfb907a49e715909c9fbaa66c03662cc9f8292b7351a9c9c58a` |
| milan-dp | 2003102 | `43cd9f69887a2afeef69474866a17b4ab3d9d740aa94978537731f4aa1134c80` |
| current-artifacts-check | 14524 | `3d6a466d2da1d043ec1d351932630817a3bb08c72e9d76420e1b14a2bcf7ea09` |

The wrapper and datapath full logs exceed 200 KB and remain under `/tmp/580-a368`;
their receipts above record size and digest. No output-directory file exceeds
200 KB. Other individual gate log hashes and sizes are in the named JSON receipts.

## Limits and delivery

Both builder modes executed all 86 top-level tests in the normal main-entry order.
The compiler-present mode records the existing external resource-calibration
report as NOT RUN. The compiler-absent mode additionally records the RV32-dependent
instruments as NOT RUN. These skips are not claimed as executed coverage.
The absent wrapper runs the entire main entry and hides only the three compiler
candidates; it asserts that all three were hidden and that the expected skip was
reported. Its source matches the method in the public round-1 evidence.

Measurements are CPU simulation evidence. Physical capture latency and hardware
behaviour remain unmeasured. The 100 MHz 8x8 point is explicitly non-contract.
The cluster-product correction remains #584's work; this round changes only its
ownership wording. Independent re-review, publication, required hosted/local CI
replication and candidate-merge validation remain for the authorized follow-up.
No review verdict or merge-completion claim is made here.

`PR-BODY.md` is the full proposed replacement body for PR #591. It has not been
applied to the PR. `REVIEW-READY.md` is the exact new issue-comment body prepared
for the final authorized publication. No other publication is requested here.

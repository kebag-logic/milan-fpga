# [A323] Round 5 handoff

Local work and assigned verification complete. Independent re-review remains due.

## Merge summary

- Branch: `400-403-declaration-truth`.
- Starting head: `c6c65e803f9eb270a11dfd65fda5814fb0b0ea55`.
- Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
- Fetched dev matched `220cb5a34507bb79bbf976b031bb55eb05543d6f`.
- Clean merge: `6d1819220f452ed9dcc086127f3f0695d14642aa`.
- Merge subject: `Merge dev into 400-403-declaration-truth`.
- Final local head: `a07a75de78b19369e228d4ab8403a52f7435fd64`.
- Submodules initialized at the merged pins.
- Only the receipt and ownership document changed after the merge.
- Firmware SHA-256: `0bf43cd4fe02b110fb1ae4f051b3bc7baa6bb62c3769962520ed1f4bd12247a6`.
- Firmware and hold behavior were unchanged by this round.

Authority: [assignment](https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5838671391),
[R249-4 F1](https://github.com/kebag-logic/milan-fpga/pull/566#issuecomment-5838668746), and
[clock/hold decision](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112).
Public review receipts were read in read-only scratch storage.

## Measurements

All six commands returned 0: 16 graded captures each, 96 total.
Every row passes census, attestation, closed ownership, byte equality and timing.
ON counters are positive; OFF counters are zero and timing still grades.
CPU rising edges align with system edges. System frequency is 100 MHz.
The 100 MHz CPU point is a non-contract comparison.

| Shape | CPU MHz | Arm | Captures | Minimum ms | Maximum ms | Command | Evidence |
|---|---|---|---|---|---|---|---|
| 8x8 | 50 | ON | 16 | 24.29290 | 24.30246 | `unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir $VALIDATION_STORAGE/400-403-a323-capture-8x8-50-on` | [capture-8x8-50-on.log](capture-8x8-50-on.log) |
| 8x8 | 50 | OFF | 16 | 24.25794 | 24.26154 | `unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir $VALIDATION_STORAGE/400-403-a323-capture-8x8-50-off` | [capture-8x8-50-off.log](capture-8x8-50-off.log) |
| 1x1 TDM8 | 50 | ON | 16 | 6.59814 | 6.60642 | `unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir $VALIDATION_STORAGE/400-403-a323-capture-1x1_tdm8-50-on` | [capture-1x1_tdm8-50-on.log](capture-1x1_tdm8-50-on.log) |
| 1x1 TDM8 | 50 | OFF | 16 | 6.58554 | 6.58857 | `unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir $VALIDATION_STORAGE/400-403-a323-capture-1x1_tdm8-50-off` | [capture-1x1_tdm8-50-off.log](capture-1x1_tdm8-50-off.log) |
| 8x8 | 100 | ON | 16 | 18.99012 | 19.00433 | `unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 --traffic on --build-dir $VALIDATION_STORAGE/400-403-a323-capture-8x8-100-on` | [capture-8x8-100-on.log](capture-8x8-100-on.log) |
| 8x8 | 100 | OFF | 16 | 19.78694 | 19.79024 | `unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 --traffic off --build-dir $VALIDATION_STORAGE/400-403-a323-capture-8x8-100-off` | [capture-8x8-100-off.log](capture-8x8-100-off.log) |

Common environment: the assigned SDK bin and installed LiteX environment lead PATH.
`LITEX_ENV_CC_TRIPLE=riscv32-linux`, `PYTHONHASHSEED=0`,
`COURSIER_MODE=offline`, and `SBT_OPTS=-Dsbt.offline=true`.
Every capture uses `unshare -Urn`; no dependency was downloaded.
Capture builds use installed Verilator 5.052; suite builds use installed 5.050.
Component revisions and the CPU netlist hash match the prior receipt.
Full identities are recorded in [environment.json](environment.json).
All simulation build trees are under `$VALIDATION_STORAGE/400-403-a323-*`.

## Old versus new maxima

Each maximum includes every row from both traffic arms.

| Shape | CPU MHz | Old ms | New ms | Delta ms | Floor margin |
|---|---|---|---|---|---|
| endstation_ax7101_1x1_tdm8 | 50 | 6.60642 | 6.60642 | +0.00000 | 7.4170x |
| endstation_ax7101_8x8 | 50 | 24.30454 | 24.30246 | -0.00208 | 2.0163x |
| endstation_ax7101_8x8 | 100 | 19.79024 | 19.79024 | +0.00000 | 2.4760x |

**Stop condition not triggered: 24.30246 ms <= 24.5 ms.**
Remaining allowance: **0.19754 ms**.
The nominal hold remains 50 ms, with its guaranteed 49 ms floor.

## Gate table

Workflow run steps were executed in order. Existing dependencies were verified
instead of downloaded or installed. The SDK step used `--verify-only`.
The SDK builder maps its fixed compiler selector to the assigned SDK and audits argv.
The absent mode hides the three cross-compiler candidates used by the builder.
The workflow-runner self-test runs inside a disposable network-disabled container,
with candidate files mounted read-only and no host credentials.
No-git checks use a scratch tree export, without an additional checkout.

| Gate | Command | Final return code | Evidence |
|---|---|---|---|
| Build the validated HDL reference | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | [docs-02-01.log](docs-02-01.log) |
| Build the validated HDL reference | `python3 scripts/gen_hdl_reference.py --output $VALIDATION_STORAGE/400-403-a323-hdl-reference` | 0 | [docs-02-02.log](docs-02-02.log) |
| Install the python gate dependencies | `python3 -c "import yaml; print(yaml.__version__)"` | 0 | [docs-04-01.log](docs-04-01.log) |
| Install the pinned Markdown renderer | `python3 -c "import importlib.metadata as m; print({n:m.version(n) for n in ['cmarkgfm','html5lib','cffi','pycparser','six','webencodings']})"` | 0 | [docs-06-01.log](docs-06-01.log) |
| Install diagram gate dependencies | `rsvg-convert --version` | 0 | [docs-07-01.log](docs-07-01.log) |
| Install diagram gate dependencies | `python3 -c "import importlib.metadata as m; assert m.version('wavedrom') == '2.0.3.post3'; print(m.version('wavedrom'))"` | 0 | [docs-07-02.log](docs-07-02.log) |
| Link health, wording, dead-reference and local-info gate | `python3 scripts/docs_check.py` | 0 | [docs-08-01.log](docs-08-01.log) |
| Added-line em-dash gate | `python3 scripts/check_em_dash.py --base 220cb5a34507bb79bbf976b031bb55eb05543d6f` | 0 | [docs-09-01.log](docs-09-01.log) |
| Concise audience documentation gate | `python3 scripts/check_doc_style.py` | 0 | [docs-10-01.log](docs-10-01.log) |
| Concise audience documentation gate | `python3 scripts/check_doc_style.py --selftest` | 0 | [docs-10-02.log](docs-10-02.log) |
| Concise audience documentation gate | `python3 scripts/check_gptp_docs.py` | 0 | [docs-10-03.log](docs-10-03.log) |
| Concise audience documentation gate | `python3 scripts/check_gptp_docs.py --selftest` | 0 | [docs-10-04.log](docs-10-04.log) |
| Audience diagram no-drift gate | `python3 docs/DOC_MAP.gen.py --check` | 0 | [docs-11-01.log](docs-11-01.log) |
| Audience diagram no-drift gate | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | [docs-11-02.log](docs-11-02.log) |
| Audience diagram no-drift gate | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | [docs-11-03.log](docs-11-03.log) |
| Audience diagram no-drift gate | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | [docs-11-04.log](docs-11-04.log) |
| Product solution source-fact gate | `python3 scripts/check_solution_docs.py` | 0 | [docs-12-01.log](docs-12-01.log) |
| Product solution source-fact gate | `python3 scripts/check_solution_docs.py --selftest` | 0 | [docs-12-02.log](docs-12-02.log) |
| Verified submodule documentation gate | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | [docs-13-01.log](docs-13-01.log) |
| Verified submodule documentation gate | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | [docs-13-02.log](docs-13-02.log) |
| Verified submodule documentation gate | `python3 scripts/check_submodule_docs.py` | 0 | [docs-13-03.log](docs-13-03.log) |
| Verified submodule documentation gate | `python3 scripts/check_submodule_docs.py --selftest` | 0 | [docs-13-04.log](docs-13-04.log) |
| HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py --selftest` | 0 | [docs-14-01.log](docs-14-01.log) |
| HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | [docs-14-02.log](docs-14-02.log) |
| HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | [docs-14-03.log](docs-14-03.log) |
| HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | [docs-14-04.log](docs-14-04.log) |
| Published diagram PNG gate | `python3 scripts/check_diagram_pngs.py` | 0 | [docs-15-01.log](docs-15-01.log) |
| Published diagram PNG gate | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | [docs-15-02.log](docs-15-02.log) |
| Milan feature-status consistency gate | `python3 scripts/check_feature_status.py --self-test` | 0 | [docs-16-01.log](docs-16-01.log) |
| Traceability matrix no-drift gate | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | [docs-17-01.log](docs-17-01.log) |
| Fetch the builder source dependencies | `git submodule update --init third_party/verilog-axis protocol-processor gptp-processor` | 0 | [docs-18-01.log](docs-18-01.log) |
| Imported gPTP documentation gate | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | [docs-19-01.log](docs-19-01.log) |
| Imported gPTP documentation gate | `make -C gptp-processor docs` | 0 | [docs-19-02.log](docs-19-02.log) |
| Code-quality measurement self-tests | `python3 scripts/measure_control_flow.py --selftest` | 0 | [docs-20-01.log](docs-20-01.log) |
| Code-quality measurement self-tests | `python3 scripts/measure_cohesion.py --selftest` | 0 | [docs-20-02.log](docs-20-02.log) |
| Install the pinned sv2v release | `sv2v --version` | 0 | [docs-21-01.log](docs-21-01.log) |
| Bare-metal scope gate | `python3 scripts/check_baremetal_only.py --check` | 0 | [docs-22-01.log](docs-22-01.log) |
| Bare-metal scope gate | `python3 scripts/check_baremetal_only.py --selftest` | 0 | [docs-22-02.log](docs-22-02.log) |
| Install and verify the pinned RV32 SDK | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | [docs-24-01.log](docs-24-01.log) |
| Install and verify the pinned RV32 SDK | `python3 scripts/ci_rv32_sdk.py --destination $VALIDATION_STORAGE/504-manager-r1/sdk-install --verify-only` | 0 | [docs-24-02.log](docs-24-02.log) |
| Compiler-absent firmware controls | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | [docs-25-01.log](docs-25-01.log) |
| Compiler-absent firmware controls | `python3 sw/builder/test_firmware_compiler.py --absent --audit $MANAGEMENT/2026-09-23/400-403-a323/rv32-absent.jsonl` | 0 | [docs-25-02.log](docs-25-02.log) |
| End-station builder gates | `python3 $VALIDATION_STORAGE/400-403-a323-builder.py sdk` | 0 | [docs-26-01.log](docs-26-01.log) |
| NVM record-space gate | `python3 scripts/check_nvm_record_space.py` | 0 | [docs-27-01.log](docs-27-01.log) |
| NVM record-space gate | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | [docs-27-02.log](docs-27-02.log) |
| Capture measurement census and clock gate | `python3 scripts/check_nvm_capture.py` | 0 | [docs-28-01.log](docs-28-01.log) |
| Saved-state writer gate | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | [docs-29-01.log](docs-29-01.log) |
| SoC source-list gate (Vivado would fail 40 min in without this) | `python3 scripts/check_soc_sources.py` | 0 | [docs-30-01.log](docs-30-01.log) |
| SoC source-list gate (Vivado would fail 40 min in without this) | `python3 scripts/check_soc_sources.py --selftest` | 0 | [docs-30-02.log](docs-30-02.log) |
| SoC source-list gate (Vivado would fail 40 min in without this) | `command -v tclsh` | 0 | [docs-30-03.log](docs-30-03.log) |
| SoC source-list gate (Vivado would fail 40 min in without this) | `python3 sw/litex/iob_pack_selftest.py` | 0 | [docs-30-04.log](docs-30-04.log) |
| RTL source-list drift gate | `python3 scripts/check_rtl_source_lists.py` | 0 | [docs-31-01.log](docs-31-01.log) |
| RTL source-list drift gate | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | [docs-31-02.log](docs-31-02.log) |
| Boundary-unit naming ratchet | `python3 scripts/measure_naming.py --check` | 0 | [docs-32-01.log](docs-32-01.log) |
| Boundary-unit naming ratchet | `python3 scripts/measure_naming.py --selftest` | 0 | [docs-32-02.log](docs-32-02.log) |
| Port contract gate | `python3 scripts/check_port_contracts.py` | 0 | [docs-33-01.log](docs-33-01.log) |
| Port contract gate | `python3 scripts/check_port_contracts.py --selftest` | 0 | [docs-33-02.log](docs-33-02.log) |
| Fail-fast ratchet | `python3 scripts/measure_fail_fast.py --check` | 0 | [docs-34-01.log](docs-34-01.log) |
| Fail-fast ratchet | `python3 scripts/measure_fail_fast.py --selftest` | 0 | [docs-34-02.log](docs-34-02.log) |
| TODO ownership gate | `python3 scripts/check_todo_ownership.py` | 0 | [docs-35-01.log](docs-35-01.log) |
| TODO ownership gate | `python3 scripts/check_todo_ownership.py --selftest` | 0 | [docs-35-02.log](docs-35-02.log) |
| Test-evidence ratchet | `python3 scripts/measure_test_evidence.py --check` | 0 | [docs-36-01.log](docs-36-01.log) |
| Test-evidence ratchet | `python3 scripts/measure_test_evidence.py --selftest` | 0 | [docs-36-02.log](docs-36-02.log) |
| Mechanical hygiene ratchet | `python3 scripts/check_hygiene.py --check` | 0 | [docs-37-01.log](docs-37-01.log) |
| Mechanical hygiene ratchet | `python3 scripts/check_hygiene.py --selftest` | 0 | [docs-37-02.log](docs-37-02.log) |
| SystemVerilog idiom gate | `python3 scripts/check_sv_idiom.py` | 0 | [docs-38-01.log](docs-38-01.log) |
| SystemVerilog idiom gate | `python3 scripts/check_sv_idiom.py --selftest` | 0 | [docs-38-02.log](docs-38-02.log) |
| C and C++ idiom gate | `python3 scripts/check_cpp_idiom.py` | 0 | [docs-39-01.log](docs-39-01.log) |
| C and C++ idiom gate | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | [docs-39-02.log](docs-39-02.log) |
| Python idiom gate | `python3 scripts/check_py_idiom.py` | 0 | [docs-40-01.log](docs-40-01.log) |
| Python idiom gate | `python3 scripts/check_py_idiom.py --selftest` | 0 | [docs-40-02.log](docs-40-02.log) |
| Shell idiom gate | `python3 scripts/check_sh_idiom.py` | 0 | [docs-41-01.log](docs-41-01.log) |
| Shell idiom gate | `python3 scripts/check_sh_idiom.py --selftest` | 0 | [docs-41-02.log](docs-41-02.log) |
| CI event and SHA contract gate | `python3 scripts/ci_events.py --check` | 0 | [docs-42-01.log](docs-42-01.log) |
| CI event and SHA contract gate | `python3 scripts/ci_events.py --selftest` | 0 | [docs-42-02.log](docs-42-02.log) |
| Local act runner contract gate | `sudo -n docker run --rm --pull never --network none --cap-drop ALL --security-opt no-new-privileges --user 1000:1000 --mount type=bind,src=$LANES/400-403-declaration-truth,dst=/candidate,readonly --workdir /candidate catthehacker/ubuntu:full-latest python3 scripts/act_ci.py --selftest` | 0 | [docs-43-01.log](docs-43-01.log) |
| Doc cited-path gate | `python3 scripts/check_doc_paths.py` | 0 | [docs-44-01.log](docs-44-01.log) |
| Archive integrity gate | `python3 scripts/check_archive.py` | 0 | [docs-45-01.log](docs-45-01.log) |
| Archive integrity gate | `python3 scripts/check_archive.py --selftest` | 0 | [docs-45-02.log](docs-45-02.log) |
| Per-page contents gate | `python3 scripts/gen_toc.py --selftest` | 0 | [docs-46-01.log](docs-46-01.log) |
| Per-page contents gate | `python3 scripts/gen_toc.py --verify-anchors` | 0 | [docs-46-02.log](docs-46-02.log) |
| Per-page contents gate | `python3 scripts/gen_toc.py --check` | 0 | [docs-46-03.log](docs-46-03.log) |
| AEM store generator self-test | `python3 avdecc/gen_aem_store.py --self-test` | 0 | [docs-47-01.log](docs-47-01.log) |
| Sweep/build shape gate | `python3 scripts/check_sweep_shape.py --self-test` | 0 | [docs-48-01.log](docs-48-01.log) |
| Deploy shape gate | `python3 scripts/check_deploy_shape.py --self-test` | 0 | [docs-49-01.log](docs-49-01.log) |
| Entity shape gate | `python3 scripts/check_entity_shape.py --self-test` | 0 | [docs-50-01.log](docs-50-01.log) |
| csr | `make -C tb/verilator/csr` | 0 | [csr.log](csr.log) |
| pp_shadow | `make -C tb/verilator/pp_shadow` | 0 | [pp_shadow.log](pp_shadow.log) |
| nvm_cosim | `make -C tb/verilator/nvm_cosim` | 0 | [nvm_cosim.log](nvm_cosim.log) |
| builder-absent | `python3 $VALIDATION_STORAGE/400-403-a323-builder.py absent` | 0 | [builder-absent.log](builder-absent.log) |
| declarations | `python3 sw/builder/test_declarations.py` | 0 | [declarations.log](declarations.log) |
| wire-accountability | `python3 scripts/check_wire_accountability.py --self-test` | 0 | [wire-accountability.log](wire-accountability.log) |
| nogit-docs_check | `python3 scripts/docs_check.py` | 0 | [nogit-docs_check.log](nogit-docs_check.log) |
| nogit-check_feature_status | `python3 scripts/check_feature_status.py` | 0 | [nogit-check_feature_status.log](nogit-check_feature_status.log) |
| final-docs | `python3 scripts/docs_check.py` | 0 | [final-docs.log](final-docs.log) |
| final-doc-style | `python3 scripts/check_doc_style.py` | 0 | [final-doc-style.log](final-doc-style.log) |
| final-em-dash | `python3 scripts/check_em_dash.py --base 220cb5a34507bb79bbf976b031bb55eb05543d6f` | 0 | [final-em-dash.log](final-em-dash.log) |
| diff-check | `git diff --check` | 0 | [diff-check.log](diff-check.log) |
| diff-base-check | `git diff --check 220cb5a34507bb79bbf976b031bb55eb05543d6f` | 0 | [diff-base-check.log](diff-base-check.log) |
| Capture mutation: bytes | `python3 scripts/check_nvm_capture.py --mutation bytes` | 1 expected; wrapper 0 | [capture-mutation-bytes.log](capture-mutation-bytes.log) |
| Capture mutation: records | `python3 scripts/check_nvm_capture.py --mutation records` | 1 expected; wrapper 0 | [capture-mutation-records.log](capture-mutation-records.log) |
| Capture mutation: clock | `python3 scripts/check_nvm_capture.py --mutation clock` | 1 expected; wrapper 0 | [capture-mutation-clock.log](capture-mutation-clock.log) |
| Capture mutation: ignore-off-timing | `python3 scripts/check_nvm_capture.py --mutation ignore-off-timing` | 1 expected; wrapper 0 | [capture-mutation-ignore-off-timing.log](capture-mutation-ignore-off-timing.log) |
| Simulation control: skip-copy | `unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation skip-copy --build-dir $VALIDATION_STORAGE/400-403-a323-control-skip-copy` | 0 | [control-skip-copy.log](control-skip-copy.log) |
| Simulation control: no-traffic | `unshare -Urn python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation no-traffic --build-dir $VALIDATION_STORAGE/400-403-a323-control-no-traffic` | 0 | [control-no-traffic.log](control-no-traffic.log) |

Co-simulation passed 465 checks and detected 39/39 mutants.
Both default register and protocol-wrapper suites passed every leg.
Declaration checks cover five configurations, 26 refusals, binding/reset
mutations and header mutations.

## Execution disclosures

- Initial dependency preflight omitted installed system package metadata.
  Adding its existing directory to the Python path resolved it.
  No dependency was downloaded or installed.
- Relocated suite builds exposed stale relative C++ dependencies.
  The wrapper resolves source/build paths and caps eight build jobs.
  Clean scratch rebuilds passed. Sources and expectations were unchanged.
  Earlier path-only failure logs remain available.
- The initial serial traffic-ON run was interrupted before grading.
  Its `abandoned-serial` partial log supplies no verdict.
  All six complete runs restarted under a foreground supervisor.
  Every child was awaited; no detached work remains.
- Explicit input mutations intentionally return 1; their wrappers require it.
  Each log names the intended refusal.

## Remaining limits and handoff

The historical placed-utilization calibration report remains unavailable.
Compiler-dependent arms are intentionally unmeasured in the absent mode;
the separate SDK mode covers them. Physical timing and memory ordering
remain UNRESOLVED 6; #565 owns configuration-clock reconciliation.
No hardware result is claimed.

Independent re-review, publication, hosted checks, trusted local workflow
replication, merge authorization and containment remain with the integration owner.
This round performs no push, PR edit, merge into dev, hardware operation,
donor edit or additional checkout.
`PR-BODY.md` contains the full proposed PR body and both close lines.
The final authorized action is `[A323] REVIEW READY` on issue #400.

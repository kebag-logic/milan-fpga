[A605]

## Contents

- **[Status](#status)** -- Source head and validation state.
- **[Linked Issue / roles](#linked-issue--roles)** -- Scope and independent reviewers.
- **[Description](#description)** -- Packet counts, notifications and Round 3 corrections.
- **[Authoritative references](#authoritative-references)** -- Requirements and rulings.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and dependencies.
- **[How to validate](#how-to-validate)** -- Commands, results and workflow ledger.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Remaining evidence.
- **[Definition of Done](#definition-of-done)** -- Review and merge obligations.

## Status

Round 3 REVIEW READY: `726-stream-counters` -> `dev`.
Local source head: `e893e4d13d99eb5ba00745f0f5cf74ee847972c2`.
Required Round 3 corrections are implemented; independent re-review is pending.
The complete documentation-workflow command ledger below records rc 0.
Behavior: 406 scenarios and 80 grader self-tests pass.
All nine parent and two mailbox detection/omission pairs pass.
The retained shipping image is 49,427 LUT (+35), 53,378 FF and 87.5 BRAM.
Round 3 changes HDL comments only; synthesis code compares unchanged.
The new commits remain local pending authorized publication.

## Linked Issue / roles

Relates to #726

Physical cadence, reference-peer reset comparison and controller display remain
merge-turn acceptance evidence. Complete issue acceptance is not claimed.

Executor: `[A605]`
Internal cleared-context reviewer: `[R628]`
External reviewer: `[R629]`

## Description

AAF and CRF Stream Output FRAMES_TX count every transmitted AVTPDU, wrap at
32 bits and reset at each talker start. Every Stream Input FRAMES_RX counts
accepted AVTPDUs, resets on binding and survives unbind. The AAF pending batch
uses 32 bits. Healthy counter changes mark each descriptor dirty for the
existing rate-limited notification path. The interface throttle is unchanged.

### Round 3

R628-2-F1: restored boundary units, declared the fixture's source-reader
contract, annotated and documented its public functions, and refactored the
C++ fixture's state and long function. All four previously failing ratchets
and every later documentation-workflow gate pass without budget increases.
The complete workflow requirement is now in the reproduction document.

R628-2-F2: both stream directions follow the per-AVTPDU law throughout the
cross-device helpers, concurrent-flow verdicts, assertion contracts and plan
steps. The ruled pair passes; an interval-rate side fails with its own finding.
A packet-rate PASS requires a measured duration. Existing assertion identifiers
remain compatible; their historical tick fields now carry packet deltas.

R629-2-F01: the valid three-packet startup snapshot, TV=3/TNV=0/FRAMES_RX=0,
is inconclusive without division by zero. Once FRAMES_RX publishes 3, the
identity passes. All-zero/unclaimed handling and measured-window rejection of
interval-rate RX remain covered. Both unchanged reviewer probes pass.

RS1-RS5 are corrected: COUNTERS is bit 3, value 8; reset wording says per-run;
harness descriptions distinguish packet totals from anomaly intervals; the
banner is wrapped; self-test descriptions follow the ruling. The prior
cross-device scope exclusion is removed. No required finding is deferred.

## Authoritative references

- Issue #726, frozen acceptance items 1-4.
- Assignment comment 6125784157 and Round 3 assignment 6131008329.
- Counter ruling 6125741685, reference-standard addendum 6125845117 and window ruling 6126028604.
- Reviews R628-2, comment 6130999022, and R629-2, comment 6130644251.
- IEEE 1722.1-2021 7.4.42.2.5, Tables 7.157 and 7.159.
- Milan v1.2 Table 5.4 reset and 5.4.5.2 Table 5.22 notification spacing.
- `docs/reference/REGISTER_MAP.md` and `docs/testing/726_STREAM_COUNTERS.md`.

## How to get into the same state

```sh
git switch 726-stream-counters
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
```

Base: `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
Use runtime 3.12.3 and the pinned simulator release 5.050.
Set TMPDIR and SCRATCH to disk storage, and VERILATOR to that executable.
Use two compiler workers and at most two simultaneous simulation builds.
Install the dependencies from `.github/workflows/docs.yml`, including its
hash-locked parser, Markdown renderer, converter and firmware SDK.
The candidate runner's offline self-test belongs inside its disposable CI job.

## How to validate

```sh
cd tests
python3 -m behave --no-capture -f plain
cd ..
python3 tb/tools/torture_campaign.py --self-test
make -C tb/verilator/milan_dp counters counters-f5 counters-mutants
python3 tb/verilator/milan_dp/stream_counters.py --shape 1 --variant before
python3 tb/verilator/milan_dp/stream_counters.py --shape 8 --variant before
python3 tb/verilator/tkdiag/mcr_mutants.py
python3 tb/verilator/avtp_rxmon/lockstep_mutants.py
python3 tb/verilator/crf_rx/mutants.py
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/lint_rtl.py --check
git diff --check c6bd08c6 HEAD
```

Use isolated scratch builds for the suite commands. The handoff records their
exact exported recipes, the unchanged reviewer probes and mutation controls.
Every plant must fail by name and escape with only its check group omitted.
Restoring the zero guard fails SNAPSHOT and escapes with 79 tests remaining.
Suppressing interval-rate findings fails XSIDE/MULTI and escapes with 78 remaining.
The existing receive-law mutation still detects and escapes.

| Validation | Result |
|---|---|
| Behavior | 14 features, 406 scenarios, 1,977 steps; no failures or skips. |
| Grader | 80 self-tests pass. |
| Native counter units | 99 talker, 14,287 CRF receive, 119 AAF NxN and 36 checks at each lockstep shape; zero failures. |
| Unit campaigns | Talker 5/5, AAF lockstep 5/5 and CRF 10/10. |
| Parent, uncertain outputs | 98 shipping / 427 largest checks pass. |
| Parent, only FRAMES_TX changing | 110 shipping / 481 largest checks pass. |
| Baseline controls | Required 20/90 named TX, RX and CADENCE failures; drivers pass. |
| Parent mutations | Nine named detection/omission pairs pass. |
| Mailbox path | Both shapes and both cadence/rate mutation pairs pass. |
| Source inventories and lint | Pass, without budget increases. |
| Capture guard | Pass; no firmware implementation change. |
| Documentation workflow | All 81 executable gate commands below return 0. |
| Whitespace | Working-tree and base-to-head checks return 0. |

Both recipients and every descriptor are measured in windows 2-4.
All corrected row-windows contain one notification. Baseline input windows
contain zero. Baseline outputs also change TIMESTAMP_UNCERTAIN; the frames-only
condition separately proves packet-event notifications with wire TU/MR clear.

| Shape | Graded row-windows | Minimum gap | Maximum gap | Maximum service |
|---|---:|---:|---:|---:|
| Shipping | 24 | 1000.996 ms | 1001.867 ms | 3.263 ms |
| Largest | 108 | 1000.982 ms | 1012.029 ms | 14.058 ms |

Each gap is within 1000 ms plus that descriptor's measured service.
Mailbox gaps are 1000-1002 ms with the existing 2 ms stall.
The handoff retains 660 individual descriptor/recipient/window records.

### Complete documentation workflow

Each command ran unpiped with the prescribed dependencies. The builder used
the pinned SDK in a disposable environment; its complete result is rc 0 with
19 explicitly NOT RUN environment-dependent arms. These optional elaboration,
local calibration and platform-dependent mutation arms remain limitations;
this is not a complete elaboration-bank claim. The final commit adds six
documentation lines only, followed by final documentation checks. Hosting
checkout/cache/upload actions are not claimed as local executions.

| Step | Gate | Command | Result |
|---|---|---|---|
| 2 | Build the validated HDL reference | `python3 scripts/gen_hdl_reference.py --selftest` | rc 0 |
| 2 | Build the validated HDL reference | `python3 scripts/gen_hdl_reference.py --output $SCRATCH/round3/milan-hdl-reference` | rc 0 |
| 8 | Link health, wording, dead-reference and local-info gate | `python3 scripts/docs_check.py` | rc 0 |
| 9 | Added-line em-dash gate | `python3 scripts/check_em_dash.py --base c6bd08c6` | rc 0 |
| 10 | Concise audience documentation gate | `python3 scripts/check_doc_style.py` | rc 0 |
| 10 | Concise audience documentation gate | `python3 scripts/check_doc_style.py --selftest` | rc 0 |
| 10 | Concise audience documentation gate | `python3 scripts/check_gptp_docs.py` | rc 0 |
| 10 | Concise audience documentation gate | `python3 scripts/check_gptp_docs.py --selftest` | rc 0 |
| 11 | Audience diagram no-drift gate | `python3 docs/DOC_MAP.gen.py --check` | rc 0 |
| 11 | Audience diagram no-drift gate | `python3 docs/DOC_MAP.gen.py --selftest` | rc 0 |
| 11 | Audience diagram no-drift gate | `python3 docs/diagrams/timesync_chain.gen.py --check` | rc 0 |
| 11 | Audience diagram no-drift gate | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | rc 0 |
| 12 | Product solution source-fact gate | `python3 scripts/check_solution_docs.py` | rc 0 |
| 12 | Product solution source-fact gate | `python3 scripts/check_solution_docs.py --selftest` | rc 0 |
| 13 | Verified submodule documentation gate | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | rc 0 |
| 13 | Verified submodule documentation gate | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | rc 0 |
| 13 | Verified submodule documentation gate | `python3 scripts/check_submodule_docs.py` | rc 0 |
| 13 | Verified submodule documentation gate | `python3 scripts/check_submodule_docs.py --selftest` | rc 0 |
| 14 | HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py --selftest` | rc 0 |
| 14 | HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | rc 0 |
| 14 | HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | rc 0 |
| 14 | HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | rc 0 |
| 15 | Published diagram PNG gate | `python3 scripts/check_diagram_pngs.py` | rc 0 |
| 15 | Published diagram PNG gate | `python3 scripts/check_diagram_pngs.py --selftest` | rc 0 |
| 16 | Milan feature-status consistency gate | `python3 scripts/check_feature_status.py --self-test` | rc 0 |
| 17 | Traceability matrix no-drift gate | `python3 docs/traceability/gen_module_matrix.py --check` | rc 0 |
| 19 | Imported gPTP documentation gate | `python3 scripts/check_gptp_docs.py --with-submodule` | rc 0 |
| 19 | Imported gPTP documentation gate | `make -C gptp-processor docs` | rc 0 |
| 20 | Code-quality measurement self-tests | `python3 scripts/measure_control_flow.py --selftest` | rc 0 |
| 20 | Code-quality measurement self-tests | `python3 scripts/measure_cohesion.py --selftest` | rc 0 |
| 22 | Bare-metal scope gate | `python3 scripts/check_baremetal_only.py --check` | rc 0 |
| 22 | Bare-metal scope gate | `python3 scripts/check_baremetal_only.py --selftest` | rc 0 |
| 24 | Install and verify the pinned RV32 SDK | `python3 scripts/ci_rv32_sdk_selftest.py` | rc 0 |
| 25 | Compiler-absent firmware controls | `python3 sw/builder/test_firmware_compiler.py --selftest` | rc 0 |
| 25 | Compiler-absent firmware controls | `python3 sw/builder/test_firmware_compiler.py --absent --audit $SCRATCH/round3/rv32-absent.jsonl` | rc 0 |
| 26 | End-station builder gates | `python3 sw/builder/test_builder.py --require-rv32` | rc 0; 19 explicit environment-dependent arms NOT RUN |
| 27 | NVM record-space gate | `python3 scripts/check_nvm_record_space.py` | rc 0 |
| 27 | NVM record-space gate | `python3 scripts/check_nvm_record_space.py --self-test` | rc 0 |
| 28 | Capture measurement census and clock gate | `python3 scripts/check_nvm_capture.py` | rc 0 |
| 29 | Saved-state writer gate | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | rc 0 |
| 30 | SoC source-list gate (Vivado would fail 40 min in without this) | `python3 scripts/check_soc_sources.py` | rc 0 |
| 30 | SoC source-list gate (Vivado would fail 40 min in without this) | `python3 scripts/check_soc_sources.py --selftest` | rc 0 |
| 30 | SoC source-list gate (Vivado would fail 40 min in without this) | `python3 sw/litex/iob_pack_selftest.py` | rc 0 |
| 31 | RTL source-list drift gate | `python3 scripts/check_rtl_source_lists.py` | rc 0 |
| 31 | RTL source-list drift gate | `python3 scripts/check_rtl_source_lists.py --selftest` | rc 0 |
| 32 | Boundary-unit naming ratchet | `python3 scripts/measure_naming.py --check` | rc 0 |
| 32 | Boundary-unit naming ratchet | `python3 scripts/measure_naming.py --selftest` | rc 0 |
| 33 | Port contract gate | `python3 scripts/check_port_contracts.py` | rc 0 |
| 33 | Port contract gate | `python3 scripts/check_port_contracts.py --selftest` | rc 0 |
| 34 | Fail-fast ratchet | `python3 scripts/measure_fail_fast.py --check` | rc 0 |
| 34 | Fail-fast ratchet | `python3 scripts/measure_fail_fast.py --selftest` | rc 0 |
| 35 | TODO ownership gate | `python3 scripts/check_todo_ownership.py` | rc 0 |
| 35 | TODO ownership gate | `python3 scripts/check_todo_ownership.py --selftest` | rc 0 |
| 36 | Test-evidence ratchet | `python3 scripts/measure_test_evidence.py --check` | rc 0 |
| 36 | Test-evidence ratchet | `python3 scripts/measure_test_evidence.py --selftest` | rc 0 |
| 37 | Mechanical hygiene ratchet | `python3 scripts/check_hygiene.py --check` | rc 0 |
| 37 | Mechanical hygiene ratchet | `python3 scripts/check_hygiene.py --selftest` | rc 0 |
| 38 | SystemVerilog idiom gate | `python3 scripts/check_sv_idiom.py` | rc 0 |
| 38 | SystemVerilog idiom gate | `python3 scripts/check_sv_idiom.py --selftest` | rc 0 |
| 39 | C and C++ idiom gate | `python3 scripts/check_cpp_idiom.py` | rc 0 |
| 39 | C and C++ idiom gate | `python3 scripts/check_cpp_idiom.py --selftest` | rc 0 |
| 40 | Python idiom gate | `python3 scripts/check_py_idiom.py` | rc 0 |
| 40 | Python idiom gate | `python3 scripts/check_py_idiom.py --selftest` | rc 0 |
| 41 | Shell idiom gate | `python3 scripts/check_sh_idiom.py` | rc 0 |
| 41 | Shell idiom gate | `python3 scripts/check_sh_idiom.py --selftest` | rc 0 |
| 42 | CI event and SHA contract gate | `python3 scripts/ci_events.py --check` | rc 0 |
| 42 | CI event and SHA contract gate | `python3 scripts/ci_events.py --selftest` | rc 0 |
| 43 | Local act runner contract gate | `python3 scripts/act_ci.py --selftest` | rc 0; offline self-test inside disposable CI job |
| 44 | Doc cited-path gate | `python3 scripts/check_doc_paths.py` | rc 0 |
| 45 | Archive integrity gate | `python3 scripts/check_archive.py` | rc 0 |
| 45 | Archive integrity gate | `python3 scripts/check_archive.py --selftest` | rc 0 |
| 46 | Per-page contents gate | `python3 scripts/gen_toc.py --selftest` | rc 0 |
| 46 | Per-page contents gate | `python3 scripts/gen_toc.py --verify-anchors` | rc 0 |
| 46 | Per-page contents gate | `python3 scripts/gen_toc.py --check` | rc 0 |
| 47 | AEM store generator self-test | `python3 avdecc/gen_aem_store.py --self-test` | rc 0 |
| 48 | Sweep/build shape gate | `python3 scripts/check_sweep_shape.py --self-test` | rc 0 |
| 49 | Deploy shape gate | `python3 scripts/check_deploy_shape.py --self-test` | rc 0 |
| 50 | Entity shape gate | `python3 scripts/check_entity_shape.py --self-test` | rc 0 |
| separate job | wire-accountability | `python3 scripts/check_wire_accountability.py --self-test` | rc 0 |
| separate job | docs-check-no-git | `python3 scripts/docs_check.py` | rc 0 |
| separate job | docs-check-no-git feature status | `python3 scripts/check_feature_status.py` | rc 0 |

## Known limitations / out of scope

- Windows 0-1 record startup; only steady windows 2-4 are graded.
- Finite compressed-time simulation does not prove physical cadence, maximum fanout or indefinite fixed-window behavior.
- The reference-peer comparison and controller display require merge-turn bench work.
- Round 3 changes no production RTL logic, firmware implementation or submodule pin.
- The interrupted redundant image run supplies no new measurement. Comment-normalized input comparison preserves the prior routed evidence: +35 LUT, below the +200 limit.
- Retained constrained-path WNS/WHS are +0.451/+0.036 ns; external I/O timing limitations remain explicit in the handoff.
- No new capture measurement is required; the capture guard passes.
- Hosted checks, authorized publication, the full current-dev candidate bank and independent re-review remain required.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

[A319] Round 3 handoff

Status: local author validation complete; independent re-review remains required.
Head: `e122f3302cf8a8e89de960233a8638b9dd1387dc`
Starting head: `7463ab0889da9a95fce7c921e386d6035d69778e`
Area and added-line base: `864b36f5e9450ef64f75ca3f0d68c44330e447d7`
Branch: `400-403-declaration-truth`
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`

Assignment: https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5834690477
Review findings: PR #566 comments 5834667344 and 5834684851.
Decisions: #400 comments 5770922734 and 5770922898.
Items 1-3 are addressed. S1 suggestions remain outside scope under #495.

## Commits

```
de36e514584573c581b1b31044f1aa9ca58691c2 test: make declaration fixtures durable and restore saved-state co-simulation
e122f3302cf8a8e89de960233a8638b9dd1387dc test: state warning flags in declaration fixture recipes
```

Both subjects are one line, with no body or trailers.

## Changes

- `docs/ENDSTATION_BUILDER.md:1018`: Correct the declaration inventory to 71 rows.
- `docs/design/AREA_BUDGET.md:41`: State that supported configurations require MAAP.
- `docs/design/MAAP_FABRIC.md:83`: Document reset zero and exact declared-output allocation.
- `hdl/common/csr/milan_csr.sv:1542`: Describe neutral AAF/MAAP resets and the distinct lwSRP VID.
- `hdl/milan/milan_datapath.sv:274`: Correct MAAP requirement and independent RX-filter presence contracts.
- `sw/litex/milan_soc.py:3466`: Correct the MAAP prune help.
- `tb/common/gen_declaration_fixture.py:1`: Generate both fixture headers with the real builder; inject the nonshipping VID only after product validation.
- `tb/verilator/csr/Makefile:82`: Run the generated reset-bits-3 leg from the default target.
- `tb/verilator/csr/fixtures/reset_bits.yaml:1`: Commit both cold-reset admission bits as explicit fixture overrides.
- `tb/verilator/csr/sim_main.cpp:103`: Describe the committed fixture recipes accurately.
- `tb/verilator/milan_dp/README.md:683`: Name the generated per-output presentation default row.
- `tb/verilator/milan_dp/sim_main.cpp:652`: Correct neutral-reset and presentation-row commentary.
- `tb/verilator/nvm_cosim/run_cases.py:110`: Derive the host header from the generated overlay and SRP table through shared boot policy.
- `tb/verilator/pp_shadow/Makefile:106`: Run generated distinct-VID and CRF-on legs from the default target.
- `tb/verilator/pp_shadow/fixtures/crf_on.yaml:1`: Commit the second declared output fixture.
- `tb/verilator/pp_shadow/fixtures/vid73.yaml:1`: Commit the distinct emitter VID fixture.
- `tb/verilator/pp_shadow/sim_main.cpp:625`: Name the durable VID recipes in the harness comment.


## Mutants

Each exact reviewer mutation was applied to the final head, run against the
suite's default target, and restored byte-for-byte. Restored defaults passed.

| Receipt | Mutation | Default target | Exit | Verdict |
|---|---|---|---:|---|
| 41 | Remove wrapper startup-VID binding | pp_shadow | 2 | DETECTED: three VID checks fail |
| 43 | Remove datapath startup-VID binding | pp_shadow | 2 | DETECTED: three VID checks fail |
| 35 | Mask both live cold-reset admission bits | csr | 2 | DETECTED: two real-output checks fail |

Exact mutation text and restoration: `run_final_mutants.py`.
Receipts: `final-mutant-41.log`, `final-mutant-43.log`, `final-mutant-35.log`.

## Wall clock

Both measurements use clean object directories, default targets and the
same tool selection. The final run enforces the unchanged deadline.

| Suite | Before, seconds | Final head, seconds | Budget, seconds |
|---|---:|---:|---:|
| pp_shadow | 18.502 | 52.735 | 1800 |
| csr | 30.480 | 35.146 | 1800 |

No changed suite exceeded its budget. No deadline was raised.

## Default sweep

All 55 default suites ran exactly once across the five native chunks.
No native chunk failed or timed out.

| Chunk | Suites | Seconds | Exit | Receipt |
|---|---:|---:|---:|---|
| 0/5 | 11 | 564.899 | 0 | [sweep-0-of-5.log](sweep-0-of-5.log) |
| 1/5 | 21 | 1470.039 | 0 | [sweep-1-of-5.log](sweep-1-of-5.log) |
| 2/5 | 10 | 709.755 | 0 | [sweep-2-of-5.log](sweep-2-of-5.log) |
| 3/5 | 12 | 442.193 | 0 | [sweep-3-of-5.log](sweep-3-of-5.log) |
| 4/5 | 1 | 1362.171 | 0 | [sweep-4-of-5.log](sweep-4-of-5.log) |

The separate expanded datapath default recipe also passed all 33 commands,
totaling 1476.120 seconds. `dp-commands.json` records the exact expansion.
Every command exit appears below. No gate command was piped.

## Area

Repository recipe: `bash syn/yosys/ooc.sh`, default Arty shape,
`synth_xilinx -family xc7 -flatten`, with no parameter override.
The CSR measurement adds only its top entry to the temporary recipe list.
For the base arm, the ten changed HDL/header inputs were read from `864b36f5e9450ef64f75ca3f0d68c44330e447d7`
into this checkout, then restored byte-for-byte. No other checkout or donor
edit was used. `run_ooc.py` records that procedure and verifies restoration.

- `KL_pp_shadow`: LUT_TOT 66991 -> 66991; FF 30187 -> 30187.
- `milan_csr`: LUT_TOT 4236 -> 4236; FF 3573 -> 3573.
- `milan_datapath`: LUT_TOT 96819 -> 96819; FF 43424 -> 43424.

All measured counter deltas:

| Module | LUT | LUTRAM | LUT_TOT | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| KL_pp_shadow | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| milan_csr | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| milan_datapath | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


Full counts: `area.json`. Receipts: `ooc-base.log`, `ooc-head-main.log`,
`ooc-head-csr.log`; executable identities: `tool-versions.log`.

## Validation notes and limits

- All 48 manager bank entries returned 0. Entry 47 uses the read-only
  helper's exact logic with only its compiler-argv receipt destination
  relocated into this packet. The pinned SDK was verified read-only.
- Both complete builder modes returned 0. The compiler-absent adapter makes
  the three cross-compiler candidates unavailable while retaining host
  compilers. Its compiler-dependent arms are explicitly unmeasured; the
  separate SDK run covers them.
- Co-simulation quick: 315 checks passed. Full: 465 checks passed and
  39/39 named mutants killed. The native sweep repeats the full target.
- All 344 behavior scenarios passed, with 1,739 steps and no skipped scenario.
- Both documentation inventory modes passed. The no-git mode uses an
  absent `GIT_DIR` to select the same filesystem walk without removing metadata.
- The installed HDL analysis front end ran: four existing pinned-processor
  findings match its ratchet; no first-party finding was added.
- An initial C++ recipe-style check failed because added flag groups did
  not individually spell both warning flags. The second commit fixes this;
  the repeated gate passes. Its initial failure remains recorded.
- Historical placed-utilization calibration was NOT RUN: its report is
  absent. Field-campaign arms report their absent generator. No hardware,
  field measurement, hosted result or candidate-merge proof is claimed.
- The changed-signature caller census is recorded in `caller-census.log`.

## Gates

| Gate / chunk | Command or recipe | Seconds | Exit |
|---|---|---:|---:|
| [before-pp-shadow, attempt 1](before-pp-shadow.log) | `make -C tb/verilator/pp_shadow` | 6.625 | 0 |
| [before-clean, attempt 1](before-clean.log) | `make -C tb/verilator/pp_shadow clean` | 0.114 | 0 |
| [before-csr-clean, attempt 1](before-csr-clean.log) | `make -C tb/verilator/csr clean` | 0.016 | 0 |
| [before-pp-shadow-cold, attempt 1](before-pp-shadow-cold.log) | `make -C tb/verilator/pp_shadow` | 18.502 | 0 |
| [before-csr-cold, attempt 1](before-csr-cold.log) | `make -C tb/verilator/csr` | 30.480 | 0 |
| [after-pp-clean, attempt 1](after-pp-clean.log) | `make -C tb/verilator/pp_shadow clean` | 0.164 | 0 |
| [after-pp-shadow-cold, attempt 1](after-pp-shadow-cold.log) | `make -C tb/verilator/pp_shadow` | 52.528 | 0 |
| [after-csr-clean, attempt 1](after-csr-clean.log) | `make -C tb/verilator/csr clean` | 0.164 | 0 |
| [declaration-gate, attempt 1](declaration-gate.log) | `python3 sw/builder/test_declarations.py` | 0.515 | 0 |
| [doc-style, attempt 1](doc-style.log) | `python3 scripts/check_doc_style.py` | 0.064 | 0 |
| [py-style, attempt 1](py-style.log) | `python3 scripts/check_py_idiom.py` | 3.320 | 0 |
| [after-csr-cold, attempt 1](after-csr-cold.log) | `make -C tb/verilator/csr` | 35.649 | 0 |
| [shape-consumers, attempt 1](shape-consumers.log) | `python3 scripts/check_entity_shape.py --self-test` | 40.412 | 0 |
| [mutant-41, attempt 1](mutant-41.log) | `make -C tb/verilator/pp_shadow` | 34.397 | 2 |
| [mutant-43, attempt 1](mutant-43.log) | `make -C tb/verilator/pp_shadow` | 35.161 | 2 |
| [mutant-35, attempt 1](mutant-35.log) | `make -C tb/verilator/csr` | 36.036 | 2 |
| [restored-pp_shadow, attempt 1](restored-pp_shadow.log) | `make -C tb/verilator/pp_shadow` | 42.113 | 0 |
| [restored-csr, attempt 1](restored-csr.log) | `make -C tb/verilator/csr` | 35.889 | 0 |
| [bank-00, attempt 1](bank-00.log) | `python3 avdecc/gen_aem_store.py --self-test` | 0.114 | 0 |
| [bank-01, attempt 1](bank-01.log) | `python3 scripts/pp_srcs.py --check --selftest` | 0.214 | 0 |
| [bank-02, attempt 1](bank-02.log) | `python3 scripts/lint_rtl.py --check --self-test` | 6.860 | 0 |
| [bank-03, attempt 1](bank-03.log) | `python3 scripts/suite_shards.py --selftest` | 0.064 | 0 |
| [bank-04, attempt 1](bank-04.log) | `python3 scripts/ci_events.py --check` | 0.214 | 0 |
| [bank-05, attempt 1](bank-05.log) | `python3 scripts/ci_scope.py --selftest` | 1.818 | 0 |
| [nvm-quick, attempt 1](nvm-quick.log) | `make -C tb/verilator/nvm_cosim quick` | 30.806 | 0 |
| [bank-06, attempt 1](bank-06.log) | `python3 scripts/ci_events.py --selftest` | 14.511 | 0 |
| [bank-07, attempt 1](bank-07.log) | `python3 docs/traceability/gen_module_matrix.py --check` | 0.967 | 0 |
| [bank-08, attempt 1](bank-08.log) | `python3 scripts/check_feature_status.py` | 0.617 | 0 |
| [bank-09, attempt 1](bank-09.log) | `python3 scripts/check_submodule_docs.py` | 0.467 | 0 |
| [bank-10, attempt 1](bank-10-initial.log) | `python3 scripts/check_cpp_idiom.py` | 1.216 | 1 |
| [bank-10, attempt 2](bank-10.log) | `python3 scripts/check_cpp_idiom.py` | 1.166 | 0 |
| [bank-11, attempt 1](bank-11.log) | `python3 scripts/check_py_idiom.py` | 3.223 | 0 |
| [bank-12, attempt 1](bank-12.log) | `python3 scripts/docs_check.py` | 4.124 | 0 |
| [bank-13, attempt 1](bank-13.log) | `python3 scripts/check_doc_style.py` | 0.067 | 0 |
| [bank-14, attempt 1](bank-14.log) | `python3 scripts/check_doc_style.py --selftest` | 0.064 | 0 |
| [bank-15, attempt 1](bank-15.log) | `python3 scripts/check_solution_docs.py` | 0.114 | 0 |
| [bank-16, attempt 1](bank-16.log) | `python3 scripts/check_doc_paths.py` | 0.065 | 0 |
| [bank-17, attempt 1](bank-17.log) | `python3 scripts/check_archive.py` | 0.264 | 0 |
| [bank-18, attempt 1](bank-18.log) | `python3 scripts/gen_toc.py --verify-anchors` | 1.623 | 0 |
| [bank-19, attempt 1](bank-19.log) | `python3 scripts/gen_toc.py --check` | 2.522 | 0 |
| [bank-20, attempt 1](bank-20.log) | `python3 scripts/check_hygiene.py --check` | 0.365 | 0 |
| [bank-21, attempt 1](bank-21.log) | `python3 scripts/check_todo_ownership.py` | 1.368 | 0 |
| [bank-22, attempt 1](bank-22.log) | `python3 scripts/check_sv_idiom.py` | 0.415 | 0 |
| [bank-23, attempt 1](bank-23.log) | `python3 scripts/check_sh_idiom.py` | 0.264 | 0 |
| [bank-24, attempt 1](bank-24.log) | `python3 scripts/check_rtl_source_lists.py` | 1.368 | 0 |
| [bank-25, attempt 1](bank-25.log) | `python3 scripts/check_soc_sources.py` | 0.115 | 0 |
| [bank-26, attempt 1](bank-26.log) | `python3 scripts/check_port_contracts.py` | 2.271 | 0 |
| [bank-27, attempt 1](bank-27.log) | `python3 scripts/check_nvm_record_space.py` | 1.970 | 0 |
| [bank-28, attempt 1](bank-28.log) | `python3 scripts/check_baremetal_only.py --check` | 14.400 | 0 |
| [bank-29, attempt 1](bank-29.log) | `python3 scripts/check_baremetal_only.py --selftest` | 4.060 | 0 |
| [bank-30, attempt 1](bank-30.log) | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 39.935 | 0 |
| [bank-31, attempt 1](bank-31.log) | `python3 scripts/check_sweep_shape.py --self-test` | 12.141 | 0 |
| [caller-census, attempt 1](caller-census.log) | `rg -n 'constants_header\(\|fabric_constants\(' --glob '*.py'` | 0.016 | 0 |
| [docs-git, attempt 1](docs-git.log) | `python3 -B scripts/docs_check.py` | 4.070 | 0 |
| [docs-no-git, attempt 1](docs-no-git.log) | `python3 -B scripts/docs_check.py` | 4.122 | 0 |
| [behave, attempt 1](behave.log) | `behave --no-capture -f plain` | 1.116 | 0 |
| [bank-32, attempt 1](bank-32.log) | `python3 scripts/xvlog_gate.py --check` | 141.674 | 0 |
| [bank-33, attempt 1](bank-33.log) | `python3 scripts/measure_control_flow.py --selftest` | 0.164 | 0 |
| [bank-34, attempt 1](bank-34.log) | `python3 scripts/measure_cohesion.py --selftest` | 0.064 | 0 |
| [bank-35, attempt 1](bank-35.log) | `python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7` | 3.074 | 0 |
| [bank-36, attempt 1](bank-36.log) | `python3 scripts/measure_fail_fast.py --check` | 1.466 | 0 |
| [bank-37, attempt 1](bank-37.log) | `python3 scripts/measure_test_evidence.py --check` | 5.275 | 0 |
| [bank-38, attempt 1](bank-38.log) | `python3 scripts/measure_naming.py --check` | 0.465 | 0 |
| [bank-39, attempt 1](bank-39.log) | `python3 scripts/measure_test_evidence.py --selftest` | 5.426 | 0 |
| [bank-40, attempt 1](bank-40.log) | `python3 scripts/gen_toc.py --selftest` | 0.815 | 0 |
| [bank-41, attempt 1](bank-41.log) | `python3 scripts/check_em_dash.py --selftest` | 3.024 | 0 |
| [bank-42, attempt 1](bank-42.log) | `python3 scripts/docs_check.py --selftest` | 0.164 | 0 |
| [bank-43, attempt 1](bank-43.log) | `git diff --check 864b36f5e9450ef64f75ca3f0d68c44330e447d7 7463ab0889da9a95fce7c921e386d6035d69778e` | 0.064 | 0 |
| [bank-44, attempt 1](bank-44.log) | `python3 scripts/check_wire_accountability.py --self-test` | 0.264 | 0 |
| [bank-45, attempt 1](bank-45.log) | `python3 scripts/check_entity_shape.py --self-test` | 41.382 | 0 |
| [bank-46, attempt 1](bank-46.log) | `python3 scripts/check_deploy_shape.py --self-test` | 0.465 | 0 |
| [nvm-full, attempt 1](nvm-full.log) | `make -C tb/verilator/nvm_cosim` | 346.247 | 0 |
| [dp-00, attempt 1](dp-00.log) | `Default datapath recipe, entry 0 in dp-commands.json` | 0.114 | 0 |
| [dp-01, attempt 1](dp-01.log) | `Default datapath recipe, entry 1 in dp-commands.json` | 13.862 | 0 |
| [dp-02, attempt 1](dp-02.log) | `Default datapath recipe, entry 2 in dp-commands.json` | 86.484 | 0 |
| [dp-03, attempt 1](dp-03.log) | `Default datapath recipe, entry 3 in dp-commands.json` | 14.293 | 0 |
| [dp-04, attempt 1](dp-04.log) | `Default datapath recipe, entry 4 in dp-commands.json` | 85.973 | 0 |
| [dp-05, attempt 1](dp-05.log) | `Default datapath recipe, entry 5 in dp-commands.json` | 0.214 | 0 |
| [dp-06, attempt 1](dp-06.log) | `Default datapath recipe, entry 6 in dp-commands.json` | 0.064 | 0 |
| [dp-07, attempt 1](dp-07.log) | `Default datapath recipe, entry 7 in dp-commands.json` | 13.106 | 0 |
| [dp-08, attempt 1](dp-08.log) | `Default datapath recipe, entry 8 in dp-commands.json` | 24.187 | 0 |
| [dp-09, attempt 1](dp-09.log) | `Default datapath recipe, entry 9 in dp-commands.json` | 11.543 | 0 |
| [dp-10, attempt 1](dp-10.log) | `Default datapath recipe, entry 10 in dp-commands.json` | 13.857 | 0 |
| [dp-11, attempt 1](dp-11.log) | `Default datapath recipe, entry 11 in dp-commands.json` | 13.382 | 0 |
| [sweep-0-of-5, attempt 1](sweep-0-of-5.log) | `scripts/run_all_suites.sh ./sweep-0-of-5 --shard 0/5` | 564.899 | 0 |
| [dp-12, attempt 1](dp-12.log) | `Default datapath recipe, entry 12 in dp-commands.json` | 13.686 | 0 |
| [dp-13, attempt 1](dp-13.log) | `Default datapath recipe, entry 13 in dp-commands.json` | 13.669 | 0 |
| [lint-check, attempt 1](lint-check.log) | `python3 scripts/lint_rtl.py --check` | 8.146 | 0 |
| [diff-final-range, attempt 1](diff-final-range.log) | `git diff --check 864b36f5e9450ef64f75ca3f0d68c44330e447d7 HEAD` | 0.064 | 0 |
| [dp-14, attempt 1](dp-14.log) | `Default datapath recipe, entry 14 in dp-commands.json` | 16.805 | 0 |
| [dp-15, attempt 1](dp-15.log) | `Default datapath recipe, entry 15 in dp-commands.json` | 12.163 | 0 |
| [dp-16, attempt 1](dp-16.log) | `Default datapath recipe, entry 16 in dp-commands.json` | 13.462 | 0 |
| [dp-17, attempt 1](dp-17.log) | `Default datapath recipe, entry 17 in dp-commands.json` | 14.565 | 0 |
| [dp-18, attempt 1](dp-18.log) | `Default datapath recipe, entry 18 in dp-commands.json` | 16.824 | 0 |
| [dp-19, attempt 1](dp-19.log) | `Default datapath recipe, entry 19 in dp-commands.json` | 17.116 | 0 |
| [dp-20, attempt 1](dp-20.log) | `Default datapath recipe, entry 20 in dp-commands.json` | 5.334 | 0 |
| [bank-47, attempt 1](bank-47.log) | `python3 -u ./full-builder-sdk.py` | 763.950 | 0 |
| [dp-21, attempt 1](dp-21.log) | `Default datapath recipe, entry 21 in dp-commands.json` | 14.857 | 0 |
| [dp-22, attempt 1](dp-22.log) | `Default datapath recipe, entry 22 in dp-commands.json` | 25.231 | 0 |
| [dp-23, attempt 1](dp-23.log) | `Default datapath recipe, entry 23 in dp-commands.json` | 16.261 | 0 |
| [dp-24, attempt 1](dp-24.log) | `Default datapath recipe, entry 24 in dp-commands.json` | 15.947 | 0 |
| [dp-25, attempt 1](dp-25.log) | `Default datapath recipe, entry 25 in dp-commands.json` | 33.874 | 0 |
| [dp-26, attempt 1](dp-26.log) | `Default datapath recipe, entry 26 in dp-commands.json` | 16.497 | 0 |
| [dp-27, attempt 1](dp-27.log) | `Default datapath recipe, entry 27 in dp-commands.json` | 5.323 | 0 |
| [dp-28, attempt 1](dp-28.log) | `Default datapath recipe, entry 28 in dp-commands.json` | 0.615 | 0 |
| [dp-29, attempt 1](dp-29.log) | `Default datapath recipe, entry 29 in dp-commands.json` | 5.924 | 0 |
| [builder-no-compiler, attempt 1](builder-no-compiler.log) | `python3 ./builder-no-compiler.py` | 556.887 | 0 |
| [dp-30, attempt 1](dp-30.log) | `Default datapath recipe, entry 30 in dp-commands.json` | 456.158 | 0 |
| [ooc-head-main, attempt 1](ooc-head-main.log) | `bash syn/yosys/ooc.sh KL_pp_shadow milan_datapath` | 546.911 | 0 |
| [dp-31, attempt 1](dp-31.log) | `Default datapath recipe, entry 31 in dp-commands.json` | 341.270 | 0 |
| [dp-32, attempt 1](dp-32.log) | `Default datapath recipe, entry 32 in dp-commands.json` | 143.460 | 0 |
| [sweep-inventory, attempt 1](sweep-inventory.log) | `scripts/run_all_suites.sh --list` | 0.214 | 0 |
| [tool-versions, attempt 1](tool-versions.log) | `python3 -c 'import subprocess; [subprocess.run([tool, "--version"], check=True) for tool in ("verilator", "yosys", "sv2v")]'` | 0.165 | 0 |
| [sweep-1-of-5, attempt 1](sweep-1-of-5.log) | `scripts/run_all_suites.sh ./sweep-1-of-5 --shard 1/5` | 1470.039 | 0 |
| [sweep-2-of-5, attempt 1](sweep-2-of-5.log) | `scripts/run_all_suites.sh ./sweep-2-of-5 --shard 2/5` | 709.755 | 0 |
| [sweep-3-of-5, attempt 1](sweep-3-of-5.log) | `scripts/run_all_suites.sh ./sweep-3-of-5 --shard 3/5` | 442.193 | 0 |
| [obsolete-default-census, attempt 1](obsolete-default-census.log) | `python3 -c 'import subprocess; r=subprocess.run(["git","grep","-n","PRES_DFLT_C","--",":!docs/history"],capture_output=True,text=True); print(r.stdout); assert r.returncode == 1; print("No obsolete presentation-default identifier outside history")'` | 0.117 | 0 |
| [declaration-row-count, attempt 1](declaration-row-count.log) | `python3 -c 'from pathlib import Path; import re; s=Path("docs/ENDSTATION_BUILDER.md").read_text().split("## 3. Config schema",1)[1].split("\n## 4.",1)[0]; n=len(re.findall(r"^\\|\s*\d+[a-z]?\s*\\|",s,re.M)); print("Numbered declaration rows:",n); assert n==71 and "71 rows." in s'` | 0.032 | 0 |
| [sweep-4-of-5, attempt 1](sweep-4-of-5.log) | `scripts/run_all_suites.sh ./sweep-4-of-5 --shard 4/5` | 1362.171 | 0 |
| [ooc-base, attempt 1](ooc-base.log) | `bash syn/yosys/ooc.sh milan_csr KL_pp_shadow milan_datapath` | 505.411 | 0 |
| [ooc-head-csr, attempt 1](ooc-head-csr.log) | `bash syn/yosys/ooc.sh milan_csr` | 11.191 | 0 |
| [final-mutant-41, attempt 1](final-mutant-41.log) | `make -C tb/verilator/pp_shadow` | 35.044 | 2 |
| [final-mutant-43, attempt 1](final-mutant-43.log) | `make -C tb/verilator/pp_shadow` | 35.193 | 2 |
| [final-mutant-35, attempt 1](final-mutant-35.log) | `make -C tb/verilator/csr` | 35.196 | 2 |
| [final-restored-pp_shadow, attempt 1](final-restored-pp_shadow.log) | `make -C tb/verilator/pp_shadow` | 41.654 | 0 |
| [final-restored-csr, attempt 1](final-restored-csr.log) | `make -C tb/verilator/csr` | 35.451 | 0 |
| [final-clean-pp_shadow, attempt 1](final-clean-pp_shadow.log) | `make -C tb/verilator/pp_shadow clean` | 0.215 | 0 |
| [final-workspace, attempt 1](final-workspace.log) | `python3 ./check_workspace.py` | 0.164 | 0 |
| [final-diff-check, attempt 1](final-diff-check.log) | `git diff --check` | 0.032 | 0 |
| [final-base-diff-check, attempt 1](final-base-diff-check.log) | `git diff --check 864b36f5e9450ef64f75ca3f0d68c44330e447d7 HEAD` | 0.064 | 0 |
| [final-cold-pp_shadow, attempt 1](final-cold-pp_shadow.log) | `timeout 1800 make -C tb/verilator/pp_shadow` | 52.735 | 0 |
| [final-clean-csr, attempt 1](final-clean-csr.log) | `make -C tb/verilator/csr clean` | 0.214 | 0 |
| [final-cold-csr, attempt 1](final-cold-csr.log) | `timeout 1800 make -C tb/verilator/csr` | 35.146 | 0 |

Exact argv, working directory, UTC start, duration and exit: `gates.jsonl`.
Expected mutant failures are separate evidence, not failed positive gates.

## Remaining duties

The manager must publish the local head and evidence, run the trusted local
workflow replica and required hosted checks, obtain independent re-review
and reviewer-owned lens coverage, then follow authorized merge and containment.
No push, PR edit, merge, hardware operation or donor edit was performed here.
`PR-BODY.md` is the complete current PR body with the Round 3 update prepared.
The final public action is the requested `[A319] REVIEW READY` issue comment.

## Public evidence source

```
Public evidence branch: 400-403-review-evidence
Commit: 31dd4fe3007633219880a2163cabd147f795e760
Reports read: R249-2, R250-2
Mutation receipt specifications: R249-2 41, 43, 35
Temporary read-only object fetch and extracted files deleted after use.
```

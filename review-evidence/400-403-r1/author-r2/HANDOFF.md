# [A313] Handoff: #400 and #403

Status: requested author validation complete at `2d61e7edafa63cff7d5f8fdca9840a969ee070a6`. The final action is the public REVIEW READY comment on #400. Independent review and publication remain pending.

## Public contract and provenance

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5831927176
- Scope decisions: #400 comments 5729726367, 5770922734 and 5781042070; #403 comment 5770922898. The owner decision of 2026-09-23 (#400 comment 5789766951) assigns actual restored PTOF to #70. Runtime SET/GET and factory declarations remain in this bundle.
- Roles: author A313; independent reviewers R249 and R250. This document is author evidence, not review approval.
- Lane: `400-403-declaration-truth`; preserved implementation `17e2cf6928865bbf1cabcec4800483bef685900f` on `483a133ed08867ea0d300d2b4a027b5b48a4282f`.
- Required remote URL was verified as `https://github.com/kebag-logic/milan-fpga.git`. `git fetch origin dev` completed, and `origin/dev` was verified as `864b36f5e9450ef64f75ca3f0d68c44330e447d7` before the merge.
- Merge `6cb112382ebe2605c78c8f0f6c9ec6a17ddaaa2e` has the required one-line subject. Dev's processor pin `990f96526bb89356c963a260ebbdcf2a77e6623a`, gPTP pin and ROM digest ledger were retained. `git submodule update --init` returned 0; missing objects were fetched from public submodule origins.
- Follow-up `4cfbb825f0082394faaec557ab8ad19d13043169` supplies four generated boot constants to the compiled census fixture. Follow-up `e7da6545` adds the new 2 ms field to the CRF overlay's exact expected dictionary. Neither changes product behavior or relaxes an assertion.
- Follow-up `2d61e7edafa63cff7d5f8fdca9840a969ee070a6` documents the existing listener-offset refusal and tests 1 ms and 2 ms listener values. The loader already refused both; the documentation-key gate exposed its missing row.
- No preserved implementation was found obsolete under the assignment's STOP rule. The follow-ups complete test fixtures and document the already implemented listener-offset refusal; no product behavior changed.

## Merge conflict hunks and resolutions

Raw conflict hunks are retained in `merge-conflicts.txt`. References below name the resolved tree.

| Conflict | Resolution |
| --- | --- |
| `protocol-processor` gitlink | Dev's `990f96526bb89356c963a260ebbdcf2a77e6623a` wins. The bundle's older pin is dropped. |
| `docs/reference/SUBMODULES.md:24` | Retain dev's pins and adoption table. Remove the superseded bundle-only pin/adoption text. Keep the bundle's historical audit disclosures at line 132. |
| `docs/reference/REGISTER_MAP.md:1172` | Keep the bundle's live cold-reset/boot-OR-3 and generated/default VID descriptions; retain dev's SRP status and slope descriptions beside them. |
| `docs/diagrams/submodule_boundaries.drawio:1` | Regenerate with `python3 docs/diagrams/submodule_boundaries.gen.py`. |
| `docs/diagrams/submodule_boundaries.svg:1` | Same generator; no manual render merge. |
| `docs/diagrams/submodule_boundaries.png` | Same generator; image inspected. |
| `docs/diagrams/PNG_MANIFEST.json:10` | Start from dev's manifest, then let the generator record the regenerated image. |

The regenerated diagram assets match dev. `syn/yosys/rom_digests.tsv` also matches dev exactly. Both sides' applicable register and submodule documentation is present.

## Changes and acceptance evidence

The public pre-implementation decisions amend the original issue examples: timers are fixed-profile assertions, factory offsets are 2 ms, observations are transmitted timestamps and GET_STREAM_INFO, and the existing receive posture is promiscuous. A 1 ms factory declaration and a changed listener acceptance window are not acceptance items. Actual persistent restore is assigned to #70 by the later owner decision.

| Acceptance item | Implementation and documentation | Executable evidence |
| --- | --- | --- |
| #400 AC1: every SRP leaf has its actual consumer, validator or explicit scratch role | `docs/ENDSTATION_BUILDER.md:1005` through row 44; `sw/builder/README-parameters.md`; `_srp_validate` at `sw/builder/endstation_builder.py:1921` | Builder gates 18a-18d, 20a and 40; 26 named declaration refusals. |
| #400 fixed class/timers/TSpec/budget | A only, VID 2 only, timers 200/5000/10000 ms, derived TSpec and interval 1, budget 1..75. `sw/builder/endstation_builder.py:1921`; docs rows 35, 36, 41-43a. LeaveAll is a randomized 10-15 s interval; the declaration is its lower bound. | `sw/builder/test_declarations.py:56` and `:157` check refusal behavior and the pinned processor timer/range constants. No timer routing is claimed. |
| #400 scratch and live ownership | Queue, numeric DMAC and derived-policy max-frame remain explicit scratch. MAAP is mandatory for declared talkers. Latency and publication ownership stay live. `sw/builder/endstation_builder.py:3209`; docs rows 37-44. | Full builder legacy-table/budget gates and declaration MAAP-removal refusal. |
| #400 AC2/3: generated startup VID path | `sw/builder/endstation_builder.py:2913` -> generated headers -> `hdl/milan/milan_datapath.sv:7411` -> `hdl/milan/KL_pp_shadow.sv:189,1056` -> pinned processor default. `docs/reference/REGISTER_MAP.md:1173` distinguishes diagnostic writes and operational Domain adoption. | Gate 40 validates every actual instance binding and rejects constant-binding mutations. Wrapper simulation uses generated VID 73 as a test-only fixture, verifies reset default and adoption; firmware boot constants use the same declaration. |
| #400 live reset bits versus boot | `hdl/common/csr/milan_csr.sv:1551`; `sw/firmware/milan_baremetal/milan_baremetal.c:1382` retains OR 3; docs row 38 and `REGISTER_MAP.md:1172`. | Five shapes x all four reset-bit combinations, 20 CSR runs; generated boot transcript gate 35. |
| #403 AC1: fixed per-output factory offset and runtime precedence | `_factory_offset` at `sw/builder/endstation_builder.py:1363`, indexed generation at `:2914`, fold at `hdl/milan/milan_datapath.sv:3265`. `docs/ENDSTATION_BUILDER.md:987`. Includes declared CRF outputs. | Gate 40 covers 1/2/5/5/9 generated rows, invalid factories, row and binding mutants. `tb/verilator/milan_dp/sim_nxn.cpp:5769,5826` observes every AAF/CRF output at 2 ms, sets one output to 1 ms, checks all GET rows and transmitted timestamps, and tests runtime boundaries/refusals. NxN 4/8, divergent and shipping four-channel legs pass. |
| #403 AC2: explicit existing promiscuous reset/boot posture | `sw/litex/boot_policy.py:58`; firmware `:1376`; builder platform validation; `docs/ENDSTATION_BUILDER.md:996`. Ambiguous `hardware` refuses with migration guidance. | Gate 35 executes the generated firmware boot transcript and rejects a restrictive-RX mutant. `tb/verilator/pp_shadow/sim_main.cpp:614` checks station/foreign unicast, broadcast and unregistered multicast on the post-filter stream at reset and boot. Listener payload acceptance remains unchanged. |
| #403 AC3: neutral reset, firmware-owned active values | Shared zero constants `hdl/common/csr/milan_csr.sv:1207`; actual reset `:1544,1552`; reset readback `:1975,1986`. Generated active words `sw/litex/boot_policy.py:55`; firmware `:1380,1383`; register rows `docs/reference/REGISTER_MAP.md:1068,1242`. | CSR matrix checks neutral words and generated active words. Gate 40 rejects old literals in actual reset and readback. Gate 35 rejects unconditional spare CRF allocation. |
| #403 exact declared MAAP allocation | `sw/litex/boot_policy.py:56` counts actual Stream Outputs; `REGISTER_MAP.md:939,1242`. | Wrapper CRF-off/on generated fixtures differ by exactly one slot; `tb/verilator/pp_shadow/sim_main.cpp:1564,1640` checks highest-valid/first-invalid source and claim boundaries. |
| Both: unchanged required regressions and documentation | `scripts/pp_srcs.py:95` permits declaration assertions to read pinned source paths, without adding compile-source entries. Dev pins/digests and historical audit disclosures retained. | Complete gates below; all-config builder/shape/elaboration; documentation checks and generated diagrams. |
| Test-fixture repairs found on current dev | `sw/builder/test_builder.py:4469` supplies the one-AAF/one-CRF census boot macros. `:18552` expects the generated 2 ms CRF overlay field. | The first two full SDK attempts exposed these omissions. The compiler-absent attempt then found the missing documentation row for the existing listener refusal. All failed logs remain; both complete final-head retries passed. |

## Behavioral tests

Both complete builder modes returned 0 at the final head. The SDK mode requires RV32 and live elaboration; the compiler-absent mode requires live elaboration. All five shipped recipes elaborate. The absent mode intentionally omits target-only identity instruments; the SDK mode runs them. Both runs report the historical placed-utilization calibration gap because the mf48 report is not installed. No placement or hardware claim is made.

| Test | Result | Evidence |
| --- | --- | --- |
| Declaration contracts | 5 configs; 26 refusals; 15 header mutants; 9 binding/reset mutants | `declarations-final.log` |
| Default CSR recipe | All five executables pass | `csr.log` |
| CSR shape/reset matrix | 20 runs, each 391 checks, zero failures | `csr-matrix.log`, `csr-matrix.py` |
| Default wrapper | 402 checks, zero failures | `pp-shadow.log` |
| Generated VID73 and CRF-on wrapper fixtures | Each 402 checks, zero failures | `pp-fixtures-retry.log`, `run-pp-fixtures.py` |
| Behavior suite | 14 features, 344 scenarios, 1739 steps, no skips | `behave.log` |

`milan-dp-dry-run.txt` is the repository default run recipe expanded with the pinned simulator. `milan-dp-commands.json` and `run-dp-chunk.py` execute every entry, split into chunks 0-10, 11-22, 23-33 and 34-45. Each entry has its own log and exit receipt; no gate output is piped. Compile commands limit parallel build jobs to eight without changing simulator version or flags.

### Complete default datapath sweep

| Default sweep entry | Invocation | rc | Evidence |
| --- | --- | --- | --- |
| 00 | `python3 ../../../protocol-processor/hdl/aecp/ucode/gen_ucode.py -o ucode.hex` | 0 | [milan-dp-00.log](milan-dp-00.log) |
| 01 | `python3 ../../../gptp-processor/hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex` | 0 | [milan-dp-01.log](milan-dp-01.log) |
| 02 | `python3 gen_divergent_shape.py` | 0 | [milan-dp-02.log](milan-dp-02.log) |
| 03 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-03.log](milan-dp-03.log) |
| 04 | `./obj_gptp/Vmilan_dp_gptp` | 0 | [milan-dp-04.log](milan-dp-04.log) |
| 05 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-05.log](milan-dp-05.log) |
| 06 | `./obj_gptplat/Vmilan_dp_gptplat` | 0 | [milan-dp-06.log](milan-dp-06.log) |
| 07 | `python3 ../../../sw/builder/endstation_builder.py ../../../configs/endstation_ax7101_1x1_tdm8.yaml -o obj_gmstep/aem-build` | 0 | [milan-dp-07.log](milan-dp-07.log) |
| 08 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-08.log](milan-dp-08.log) |
| 09 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-09.log](milan-dp-09.log) |
| 10 | `./obj_gmstep/Vmilan_dp_gmstep obj_gmstep/aemi.bin 0` | 0 | [milan-dp-10.log](milan-dp-10.log) |
| 11 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-11.log](milan-dp-11.log) |
| 12 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-12.log](milan-dp-12.log) |
| 13 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-13.log](milan-dp-13.log) |
| 14 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-14.log](milan-dp-14.log) |
| 15 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-15.log](milan-dp-15.log) |
| 16 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-16.log](milan-dp-16.log) |
| 17 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-17.log](milan-dp-17.log) |
| 18 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-18.log](milan-dp-18.log) |
| 19 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-19.log](milan-dp-19.log) |
| 20 | `echo "======================================================================"` | 0 | [milan-dp-20.log](milan-dp-20.log) |
| 21 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-21.log](milan-dp-21.log) |
| 22 | `Build command from default recipe (full argv in log)` | 0 | [milan-dp-22.log](milan-dp-22.log) |
| 23 | `./obj_dir/Vmilan_dp_sim` | 0 | [milan-dp-23.log](milan-dp-23.log) |
| 24 | `echo "---- Milan 5.4.5 notifications and the #508 GET_STREAM_INFO seam, TIMED on the compressed processor timebase ----"` | 0 | [milan-dp-24.log](milan-dp-24.log) |
| 25 | `./obj_notify/Vmilan_dp_notify` | 0 | [milan-dp-25.log](milan-dp-25.log) |
| 26 | `echo "---- #530 CRF talker licence and per-type LeaveAll, TIMED on one compressed grid ----"` | 0 | [milan-dp-26.log](milan-dp-26.log) |
| 27 | `./obj_crflic/Vmilan_dp_crflic` | 0 | [milan-dp-27.log](milan-dp-27.log) |
| 28 | `./obj_nxn/Vmilan_dp_nxn` | 0 | [milan-dp-28.log](milan-dp-28.log) |
| 29 | `echo "---- the DIVERGENT shape: input row 1 declares the 96 kHz base ----"` | 0 | [milan-dp-29.log](milan-dp-29.log) |
| 30 | `./obj_nxndv/Vmilan_dp_nxndv` | 0 | [milan-dp-30.log](milan-dp-30.log) |
| 31 | `./obj_nxn8/Vmilan_dp_nxn8` | 0 | [milan-dp-31.log](milan-dp-31.log) |
| 32 | `echo "---- the shipping Arty shape: 4 streams x 4 wire channels ----"` | 0 | [milan-dp-32.log](milan-dp-32.log) |
| 33 | `./obj_nxn4c/Vmilan_dp_nxn4c` | 0 | [milan-dp-33.log](milan-dp-33.log) |
| 34 | `echo "---- LPF_P=0 (pruned render tap, the ax7101 shipping shape) ----"` | 0 | [milan-dp-34.log](milan-dp-34.log) |
| 35 | `./obj_nolpf/Vmilan_dp_nolpf` | 0 | [milan-dp-35.log](milan-dp-35.log) |
| 36 | `echo "---- all six tier-1 blocks pruned ----"` | 0 | [milan-dp-36.log](milan-dp-36.log) |
| 37 | `./obj_prune/Vmilan_dp_prune` | 0 | [milan-dp-37.log](milan-dp-37.log) |
| 38 | `echo "---- THE SHIPPING ALINX SHAPE: 1 stream x 8 wire channels, TDM8 master ----"` | 0 | [milan-dp-38.log](milan-dp-38.log) |
| 39 | `./obj_ax1x1/Vmilan_dp_ax1x1` | 0 | [milan-dp-39.log](milan-dp-39.log) |
| 40 | `echo "---- the same shape at the TRUE clk_audio ratio (391/1591) ----"` | 0 | [milan-dp-40.log](milan-dp-40.log) |
| 41 | `./obj_aclk/Vmilan_dp_aclk` | 0 | [milan-dp-41.log](milan-dp-41.log) |
| 42 | `echo "---- #386 render law: the same leg against mutated setpoint stages and datapath ----"` | 0 | [milan-dp-42.log](milan-dp-42.log) |
| 43 | `python3 render_mutants.py` | 0 | [milan-dp-43.log](milan-dp-43.log) |
| 44 | `echo "---- #387 GM step re-base: the gmstep leg against the acceptance's controls ----"` | 0 | [milan-dp-44.log](milan-dp-44.log) |
| 45 | `python3 gmstep_mutants.py` | 0 | [milan-dp-45.log](milan-dp-45.log) |

Default leg counts: gPTP 181, gPTP latency 181, GM-step 48, default 234, notifications 381, CRF licensing 85, NxN4 1844, divergent NxN4 1846, NxN8 3524, shipping four-channel 1844, no-LPF 234, pruned 33, AX1x1 231, audio-clock 144. All zero failures. Shape-inapplicable assertions are explicitly reported by each bench. Render mutation gate: two clean controls and four detected defects. GM-step mutation gate: clean control and three detected defects.

## Gate table and provenance

The machine-readable ledger is `gate-results.jsonl`. Each log records its exact command and starting commit. Later commits repair builder fixtures and add documentation/negative tests for the existing listener-offset refusal; RTL, firmware and generated declarations are unchanged after the merge. The final gate table selects the latest receipt for each name. An earlier same-name Python-style log was superseded by the final-head run; its older ledger receipt is retained but is not used as final evidence. The first compiler-absent run started on the working bytes later committed as e7da6545 and retains its original starting-head label. Both final full runs start at 2d61e7ed and require live elaboration; the SDK mode also requires the RV32 compiler. No old pre-merge result is reused. `validated-inputs.json` records the 25 changed-file hashes at the final head. The final SDK driver was paused during gate 1b while datapath mutations compiled, to keep later builder temporary source/header mutations from overlapping those builds; `builder-serialization.json` records the pause/resume interval. The initial gPTP leg was rerun after the earlier entity-shape self-test: 181/181 pass in `milan-dp-final-04.log`.

The SDK wrapper redirects the test's existing absolute compiler selector to the supplied read-only pinned SDK and verifies its checksum first. `builder-sdk-final-argv.jsonl` records the final run's requested and executed argv. The compiler-absent wrapper makes only RV32 candidates unavailable, retaining the host compiler required by the boot-transcript tests; its final audit is `builder-absent-final-argv.jsonl`. Earlier attempt audits remain separately named. Neither wrapper changes test functions or acceptance.

Initial nonzero attempts remain disclosed: the first SDK run lacked four census fixture macros; the second reached the stale CRF exact-object expectation (it began at merge head 6cb11238 with the exact working bytes then committed as 4cfbb825). The first compiler-absent full run reached the missing documentation row for the existing listener refusal. Initial em-dash/TOC calls lacked the pinned Markdown dependency and returned 2; pinned-interpreter retries passed. The first supplemental wrapper fixture attempt expanded a submake under inherited dry-run flags; the retry takes the source list from a normal `print-srcs` call. Product code, ratchets and acceptance were not weakened.

Helper names below are relative to this output directory and run from the lane; $MEASURE abbreviates the external measurement directory recorded in each log.

| Gate | Invocation (exact argv also in log) | rc | Head at start | Evidence |
| --- | --- | --- | --- | --- |
| builder-sdk-final | `/usr/bin/python3 -u builder-sdk-final.py` | 0 | `2d61e7ed` | [builder-sdk-final.log](builder-sdk-final.log) |
| builder-absent-final | `/usr/bin/python3 -u builder-absent-final.py` | 0 | `2d61e7ed` | [builder-absent-final.log](builder-absent-final.log) |
| declarations-final | `python3 sw/builder/test_declarations.py` | 0 | `2d61e7ed` | [declarations-final.log](declarations-final.log) |
| csr | `make -C tb/verilator/csr VERILATOR=$MEASURE/bin/verilator` | 0 | `4cfbb825` | [csr.log](csr.log) |
| csr-matrix | `python3 -u csr-matrix.py` | 0 | `4cfbb825` | [csr-matrix.log](csr-matrix.log) |
| pp-shadow | `make -C tb/verilator/pp_shadow VERILATOR=$MEASURE/bin/verilator` | 0 | `4cfbb825` | [pp-shadow.log](pp-shadow.log) |
| pp-fixtures-retry | `python3 -u run-pp-fixtures.py` | 0 | `4cfbb825` | [pp-fixtures-retry.log](pp-fixtures-retry.log) |
| behave | `bash -c 'cd tests && behave --no-capture -f plain'` | 0 | `4cfbb825` | [behave.log](behave.log) |
| baremetal | `python3 scripts/check_baremetal_only.py --check` | 0 | `4cfbb825` | [baremetal.log](baremetal.log) |
| docs-git-final | `python3 -B scripts/docs_check.py` | 0 | `2d61e7ed` | [docs-git-final.log](docs-git-final.log) |
| docs-no-git-final | `env GIT_DIR=/tmp/a313-absent-git-metadata python3 -B scripts/docs_check.py` | 0 | `2d61e7ed` | [docs-no-git-final.log](docs-no-git-final.log) |
| em-dash-final | `<pinned Markdown python3> scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7` | 0 | `2d61e7ed` | [em-dash-final.log](em-dash-final.log) |
| doc-style-final | `python3 scripts/check_doc_style.py` | 0 | `2d61e7ed` | [doc-style-final.log](doc-style-final.log) |
| toc-check-final | `<pinned Markdown python3> scripts/gen_toc.py --check` | 0 | `2d61e7ed` | [toc-check-final.log](toc-check-final.log) |
| toc-anchors-final | `<pinned Markdown python3> scripts/gen_toc.py --verify-anchors` | 0 | `2d61e7ed` | [toc-anchors-final.log](toc-anchors-final.log) |
| doc-paths-final | `python3 scripts/check_doc_paths.py` | 0 | `2d61e7ed` | [doc-paths-final.log](doc-paths-final.log) |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `4cfbb825` | [module-matrix.log](module-matrix.log) |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | `4cfbb825` | [xvlog.log](xvlog.log) |
| rtl-sources | `python3 scripts/check_rtl_source_lists.py` | 0 | `4cfbb825` | [rtl-sources.log](rtl-sources.log) |
| sv-idiom | `python3 scripts/check_sv_idiom.py` | 0 | `4cfbb825` | [sv-idiom.log](sv-idiom.log) |
| rtl-lint | `python3 scripts/lint_rtl.py --check` | 0 | `4cfbb825` | [rtl-lint.log](rtl-lint.log) |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | 0 | `4cfbb825` | [cpp-idiom.log](cpp-idiom.log) |
| py-idiom-final | `python3 scripts/check_py_idiom.py` | 0 | `2d61e7ed` | [py-idiom-final.log](py-idiom-final.log) |
| port-contracts | `python3 scripts/check_port_contracts.py` | 0 | `4cfbb825` | [port-contracts.log](port-contracts.log) |
| naming | `python3 scripts/measure_naming.py --check` | 0 | `4cfbb825` | [naming.log](naming.log) |
| test-evidence-final | `python3 scripts/measure_test_evidence.py --check` | 0 | `2d61e7ed` | [test-evidence-final.log](test-evidence-final.log) |
| entity-shape | `python3 scripts/check_entity_shape.py --self-test` | 0 | `4cfbb825` | [entity-shape.log](entity-shape.log) |
| submodule-docs | `python3 scripts/check_submodule_docs.py` | 0 | `4cfbb825` | [submodule-docs.log](submodule-docs.log) |
| diagram-check | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | `4cfbb825` | [diagram-check.log](diagram-check.log) |
| pp-sources | `python3 scripts/pp_srcs.py --check` | 0 | `4cfbb825` | [pp-sources.log](pp-sources.log) |
| diff-check-final | `git diff --check` | 0 | `2d61e7ed` | [diff-check-final.log](diff-check-final.log) |
| area-base | `env OOC_TMP=$MEASURE/area-base OOC_SHAPE=$MEASURE/area-base-inputs/configs/generated/endstation_arty_current bash $MEASURE/ooc-base-with-csr.sh milan_csr KL_pp_shadow milan_datapath` | 0 | `4cfbb825` | [area-base.log](area-base.log) |
| area-head | `env OOC_TMP=$MEASURE/area-head bash $MEASURE/ooc-with-csr.sh milan_csr KL_pp_shadow milan_datapath` | 0 | `4cfbb825` | [area-head.log](area-head.log) |
| area-base-input-verified | `Exact command in the linked log` | 0 | `2d61e7ed` | [area-base-input-verified.log](area-base-input-verified.log) |
| area-head-input-verified | `env OOC_TMP=$MEASURE/area-head-recheck OOC_COMPARE_DIR=$MEASURE/area-head bash $MEASURE/ooc-head-input-recheck.sh milan_csr KL_pp_shadow milan_datapath` | 0 | `2d61e7ed` | [area-head-input-verified.log](area-head-input-verified.log) |
| final-containment | `python3 final-containment.py` | 0 | `2d61e7ed` | [final-containment.log](final-containment.log) |

## Area

All three changed RTL modules are measured before and after with the repository `syn/yosys/ooc.sh` synthesis recipe, `synth_xilinx -family xc7 -flatten`, default parameters and the Arty-current generated shape. The temporary measuring recipe adds only a missing `milan_csr` top row and absolute root/helper paths. No timing, routed utilization or wider-shape area claim is made.

Baseline files are exact changed Git blobs from dev 864b36f5, isolated outside the output directory; all remaining sources and processor pins are common. `area-base-inputs.json` records blob IDs and hashes. `ooc-recipe-adaptation.json` records the measuring-script transformation. This is not a checkout, and no candidate or donor file is swapped for area measurement. Tool prefixes, SDKs, generated netlists and isolated source blobs remain outside this output directory.

Both OOC runs returned 0. All columns are baseline -> candidate; every delta is zero.

| Module | LUT | LUTRAM | LUT total | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| milan_csr | 4236 -> 4236 | 0 -> 0 | 4236 -> 4236 | 3573 -> 3573 | 0 -> 0 | 2 -> 2 | 0 -> 0 | 43 -> 43 |
| KL_pp_shadow | 60855 -> 60855 | 6136 -> 6136 | 66991 -> 66991 | 30187 -> 30187 | 15 -> 15 | 4 -> 4 | 6 -> 6 | 2104 -> 2104 |
| milan_datapath | 90179 -> 90179 | 6640 -> 6640 | 96819 -> 96819 | 43424 -> 43424 | 17 -> 17 | 20 -> 20 | 15 -> 15 | 3614 -> 3614 |

Evidence: `area-base.log`, `area-head.log` and six `area-{base,head}-<module>.log` synthesis reports. Tool provenance is `tool-versions.json`: Yosys 0.66, sv2v 0.0.13, the same binaries before and after. Simulator runs use the repository-pinned 5.050 version.

At final head 2d61e7ed, all six frontend outputs were regenerated and compared byte for byte to the original synthesis inputs. Both comparisons returned 0, with SHA-256 hashes in `area-{base,head}-input-verified.log`; `area-recheck-method.json` describes the temporary comparison recipe. The initial comparison-helper draft selected an earlier comment inside the top list and failed shell syntax before any source processing; those two rc 2 receipts remain. The corrected helper passed shell syntax and all comparisons. It did not replace or alter synthesis results.

## Final handoff

Final local head: `2d61e7edafa63cff7d5f8fdca9840a969ee070a6`. The working tree and pinned submodules are clean. Required dev pins/ROM ledger and regenerated diagram assets match dev. All requested author-gate final receipts are 0. See `final-containment.log` and `validated-inputs.json`.

`PR-BODY.md` is ready for the publishing role. `REVIEW-READY.md` contains the exact public handoff text. The final session action posts it on #400. Reviewers R249 and R250 remain assigned; no review verdict or merge approval is claimed. Manager-owned full repository/candidate gates, PR replication, hosted contexts and merge/containment remain separate from this author handoff.

No push, PR creation/edit, merge into dev, hardware access, other checkout, donor edit or sub-agent work has been performed. Actual saved-state restore remains #70 under the owner decision.

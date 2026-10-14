# Round 8 gate table

Each row is a set of completed gate records, all rc 0. Failed, interrupted and superseded attempts are in [GATES.json](GATES.json) with their own codes and are not counted here. `$REPO` is the lane checkout, `$SCRATCH` the round-8 scratch root, `$EVIDENCE` this evidence directory, `$PYTHON` the CPython 3.12.3 environment and `$PRODUCT_PYTHON` the product build environment.

| Gate | Head | rc | Seconds | What it catches |
|---|---|---|---:|---|
| Capture recipe, six arms, Verilator 5.052 | `f3bb2014` | 0 | 13,737.00 | 96 captures. Each checks attestation, closed ownership, every destination byte and the traffic arm's counters; the contract arms are graded against 24.5 ms. |
| Capture products against round 7 | `f3bb2014` | 0 | 0.11 | Any difference in an arm's CPU netlist, instrumented firmware, BIOS, gPTP microcode or generated headers (timestamp line and build directory aside). |
| Receipt assembly, section 18 refresh | `f3bb2014` | 0 | 0.88 | The assembler refuses a dirty tree, a HEAD other than the measured commit, a run log naming another simulator, or a receipt that fails `check_receipt`. The refresher refuses a changed census, firmware digest or processor pin, and any edit that does not match exactly once. |
| Shipping writer gate | `f3bb2014` | 0 | 271.15 | 5 shapes at 3,550 cases. 61 planted firmware defects (5 writer, 18 #671 on 3 shapes, 2 boot-walk) redden, and the comparison check fails by name in its 9 arms. |
| Term census | `f3bb2014` | 0 | 0.21 | A missing class, sequence, layout or restart combination, a duplicate case, or a comparison term without a class or control. |
| Term omission matrix | `f3bb2014` | 0 | 31.14 | Each `r_omit_` control must fail all 32 of its own class's cases per shape, and no other class. |
| Instrumented term views | `f3bb2014` | 0 | 10.75 | A class case that does not hand the judgement two refusals differing in its own term alone, then `VD_OK`. |
| Full read-fault campaigns | `f3bb2014` | 0 | 1,900.43 | Each of the 18 #671 controls is run over the full standing cases on 3 shapes and must be named by its own finding. |
| Campaign comparison with round 7 | `f3bb2014` | 0 | 0.06 | Any change in the named, restart, cold or total finding counts of the 54 shape and control pairs. |
| NVM co-simulation | `f3bb2014` | 0 | 968.31 | 465 checks; 39 named mutants (stale identity, lost pending work, reload and admission ordering, unbounded hold, writer restart) killed by their named checks. |
| Service budget | `f3bb2014` | 0 | 1.67 | 55 oracle checks; product dispatch removal, duty overrun and lost backing markers. |
| Builder, 103 functions | `f3bb2014` | 0 | 1,370.23 | Product profile, RV32, shape, dispatch, descriptor, clock and capacity plants; the writer gate in part 6. Every elaboration arm ran; two arms are NOT RUN for recorded reasons and not counted. |
| Firmware tally | `f3bb2014` | 0 | 3.63 | 18 planted false-success and empty-run tally cases. |
| SDK and RV32 self-tests | `f3bb2014` | 0 | 9.71 | Wrong SDK identity, ISA or ABI, disallowed symbols, images that do not link freestanding. |
| Control firmware, four phases | `f3bb2014` | 0 | 2,748.91 | Normal suites and the ADP, ACMP, MAAP, AECP and SRP mutation phases with RV32 builds, including the lwSRP pin controls. |
| Control shard proof, CI firmware census | `f3bb2014` | 0 | 0.49 | A dropped, duplicated or unassigned suite; invalid shard options; a CI census losing a phase. |
| Saved-state store | `f3bb2014` | 0 | 3,615.41 | 5 shapes, 435 tests and 109 planted store defects, which import this lane's host gate. |
| Coverage | `f3bb2014` | 0 | 279.50 | 29 planted ratchet and exclusion cases; the live coverage check over 30 files. |
| Firmware boundary | `f3bb2014` | 0 | 874.96 | Public-header boundary, source ownership and pins over 2,854 compiled sources; missing builders or compiler inputs refused. The control-memory image builds. |
| RTL lint and source lists | `f3bb2014` | 0 | 17.84 | Lint ratchet (90 at 90) and waiver plants; forged or missing submodule inputs; source-list drift. |
| BDD | `f3bb2014` | 0 | 1.72 | 406 scenarios, 1,977 steps. |
| Docs-check replica at the merge | `f3bb2014` | 0 | 753.75 | 81 positions, base `fa820988`. The builder, capture-gate and writer-gate positions have the separate rows above. |
| CI checks at the merge | `f3bb2014` | 0 | 125.45 | `ci_scope.py --selftest` (scope history and merge-base plants), `ci_events.py --check` (2,174 contract items), and `act_ci.py --selftest` in a disposable container, checked-in and flat layouts. |
| Final capture and document gates | `d5cd8635` | 0 | 9.74 | `check_nvm_capture` passes, and its `bytes`, `records`, `clock`, `ignore-off-timing` and `receipt-opt-out` arms each exit 1 by name. C and Python idiom, hygiene, docs, TOC and anchors, doc style, paths and map, em dash against `fa820988`, feature status, `git diff --check` against the tree, `e8454e27` and `fa820988`. |
| Docs-check replica at the final head | `d5cd8635` | 0 | 655.92 | The same 81 positions, at the head that changes the design document. |
| CI checks at the final head | `d5cd8635` | 0 | 117.61 | The three requested checks again, the firmware census, and both runner self-test layouts in a disposable container. |
| Firmware size | `d5cd8635` | 0 | 0.72 | Base and head sources against the merged tree's 1x1 capture headers, make 4.3 with `MAKEFLAGS=w`. A measurement, not a mutation test. |

## Capture recipe, six arms, Verilator 5.052

```sh
unshare -Urn '$PRODUCT_PYTHON' -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir '$SCRATCH/capture52/1x1-50-on/capture-1x1-50-on'
unshare -Urn '$PRODUCT_PYTHON' -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir '$SCRATCH/capture52/1x1-50-off/capture-1x1-50-off'
unshare -Urn '$PRODUCT_PYTHON' -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir '$SCRATCH/capture52/8x8-50-on/capture-8x8-50-on'
unshare -Urn '$PRODUCT_PYTHON' -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir '$SCRATCH/capture52/8x8-50-off/capture-8x8-50-off'
unshare -Urn '$PRODUCT_PYTHON' -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 --traffic on --build-dir '$SCRATCH/capture52/8x8-100-on/capture-8x8-100-on'
unshare -Urn '$PRODUCT_PYTHON' -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 --traffic off --build-dir '$SCRATCH/capture52/8x8-100-off/capture-8x8-100-off'
```

## Capture products against round 7

```sh
python3 $EVIDENCE/scripts/r8/compare_products.py $ROUND7_SCRATCH/capture $SCRATCH/capture52 $SCRATCH/capture52-products.json
```

## Receipt assembly, section 18 refresh

```sh
python3 $EVIDENCE/scripts/r8/assemble_receipt.py $REPO $SCRATCH/capture52 f3bb2014d065141930ae1a473c966b419d1040aa 'https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6161596895' 2026-10-14
python3 $EVIDENCE/scripts/r8/refresh_section18.py
```

## Shipping writer gate

```sh
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 4
```

## Term census

```sh
python3 $EVIDENCE/scripts/r6/term_census.py $REPO
```

## Term omission matrix

```sh
python3 $EVIDENCE/scripts/r6/term_matrix.py $REPO $SCRATCH/term-matrix --jobs 4
```

## Instrumented term views

```sh
python3 $EVIDENCE/scripts/r6/term_views.py $REPO $SCRATCH/term-views
```

## Full read-fault campaigns

```sh
python3 $EVIDENCE/scripts/r6/plants_full.py $REPO $SCRATCH/full-controls-endstation_arty_4x4-1 4 endstation_arty_4x4 r_omit_verdict r_omit_byte_count r_omit_prefix_crc r_omit_trailer r_digest_with_trailer r_digest_header_only
python3 $EVIDENCE/scripts/r6/plants_full.py $REPO $SCRATCH/full-controls-endstation_arty_4x4-2 4 endstation_arty_4x4 restart_at_zero unbounded_retry generation_from_refused_slot verdict_only_agreement r_fill_from_flash r_restage_fail_offers_none
python3 $EVIDENCE/scripts/r6/plants_full.py $REPO $SCRATCH/full-controls-endstation_arty_4x4-3 4 endstation_arty_4x4 restage_fail_not_unread r_restage_any_seq r_reattach_goes_live r_judge_four_tries p_restage_unbounded r_restage_four_tries
python3 $EVIDENCE/scripts/r6/plants_full.py $REPO $SCRATCH/full-controls-endstation_ax7101_1x1_tdm8-1 4 endstation_ax7101_1x1_tdm8 r_omit_verdict r_omit_byte_count r_omit_prefix_crc r_omit_trailer r_digest_with_trailer r_digest_header_only
python3 $EVIDENCE/scripts/r6/plants_full.py $REPO $SCRATCH/full-controls-endstation_ax7101_1x1_tdm8-2 4 endstation_ax7101_1x1_tdm8 restart_at_zero unbounded_retry generation_from_refused_slot verdict_only_agreement r_fill_from_flash r_restage_fail_offers_none
python3 $EVIDENCE/scripts/r6/plants_full.py $REPO $SCRATCH/full-controls-endstation_ax7101_1x1_tdm8-3 4 endstation_ax7101_1x1_tdm8 restage_fail_not_unread r_restage_any_seq r_reattach_goes_live r_judge_four_tries p_restage_unbounded r_restage_four_tries
python3 $EVIDENCE/scripts/r6/plants_full.py $REPO $SCRATCH/full-controls-endstation_ax7101_8x8-1 4 endstation_ax7101_8x8 r_omit_verdict r_omit_byte_count r_omit_prefix_crc r_omit_trailer r_digest_with_trailer r_digest_header_only
python3 $EVIDENCE/scripts/r6/plants_full.py $REPO $SCRATCH/full-controls-endstation_ax7101_8x8-2 4 endstation_ax7101_8x8 restart_at_zero unbounded_retry generation_from_refused_slot verdict_only_agreement r_fill_from_flash r_restage_fail_offers_none
python3 $EVIDENCE/scripts/r6/plants_full.py $REPO $SCRATCH/full-controls-endstation_ax7101_8x8-3 4 endstation_ax7101_8x8 restage_fail_not_unread r_restage_any_seq r_reattach_goes_live r_judge_four_tries p_restage_unbounded r_restage_four_tries
```

## Campaign comparison with round 7

```sh
python3 $SCRATCH/scripts/campaign_compare.py $SCRATCH $EVIDENCE
```

## NVM co-simulation

```sh
make -C tb/verilator/nvm_cosim -j8 run JOBS=2 POOL=4
```

## Service budget

```sh
make -C tb/verilator/fw_service_budget -j8
```

## Builder, 103 functions

```sh
python3 $EVIDENCE/scripts/r7/builder_parts.py $REPO 0 6 --require-elaboration --require-rv32
python3 $EVIDENCE/scripts/r7/builder_parts.py $REPO 1 6 --require-elaboration --require-rv32
python3 $EVIDENCE/scripts/r7/builder_parts.py $REPO 2 6 --require-elaboration --require-rv32
python3 $EVIDENCE/scripts/r7/builder_parts.py $REPO 3 6 --require-elaboration --require-rv32
python3 $EVIDENCE/scripts/r7/builder_parts.py $REPO 4 6 --require-elaboration --require-rv32
python3 $EVIDENCE/scripts/r7/builder_parts.py $REPO 5 6 --require-elaboration --require-rv32
```

## Firmware tally

```sh
python3 sw/firmware/gtest/tally_selftest.py
```

## SDK and RV32 self-tests

```sh
python3 scripts/ci_rv32_sdk_selftest.py
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
```

## Control firmware, four phases

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2 --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2 --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2 --shard 3/4
```

## Control shard proof, CI firmware census

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
python3 scripts/ci_events.py --firmware-census
```

## Saved-state store

```sh
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 2
```

## Coverage

```sh
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 2
```

## Firmware boundary

```sh
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/litex/test_ctrl_memory.py --build-only
```

## RTL lint and source lists

```sh
python3 scripts/lint_rtl.py --check --self-test
python3 scripts/pp_srcs.py --check --selftest
```

## BDD

```sh
python3 -m behave --no-capture -f plain tests
```

## Docs-check replica at the merge

```sh
bash $SCRATCH/scripts/docs_replica.sh $REPO $PYTHON fa820988 $SCRATCH/docs-logs $SCRATCH/docs-scratch
```

## CI checks at the merge

```sh
python3 scripts/ci_scope.py --selftest
python3 scripts/ci_events.py --check
sudo -n docker run --rm --user 1000:1000 --network none --read-only --cap-drop ALL --security-opt no-new-privileges --pids-limit 256 --memory 2g --cpus 2 --mount type=bind,source=$REPO,target=/workspace,readonly --mount type=bind,source=$SCRATCH/docker,target=/scratch --workdir /workspace --env TMPDIR=/scratch/tmp --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 scripts/act_ci.py --selftest
sudo -n docker run --rm --user 1000:1000 --network none --read-only --cap-drop ALL --security-opt no-new-privileges --pids-limit 256 --memory 2g --cpus 2 --mount type=bind,source=$REPO,target=/workspace,readonly --mount type=bind,source=$SCRATCH/docker,target=/scratch --workdir /workspace --env TMPDIR=/scratch/tmp --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 /scratch/flat_selftest.py
```

## Final capture and document gates

```sh
python3 $EVIDENCE/scripts/r8/final_gates.py $REPO $SCRATCH/final-logs
```

## Docs-check replica at the final head

```sh
bash $EVIDENCE/scripts/r8/docs_replica.sh $REPO $PYTHON fa820988 $SCRATCH/docs-logs-final $SCRATCH/docs-scratch-final
```

## CI checks at the final head

```sh
python3 scripts/ci_scope.py --selftest
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --firmware-census
sudo -n docker run --rm --user 1000:1000 --network none --read-only --cap-drop ALL --security-opt no-new-privileges --pids-limit 256 --memory 2g --cpus 2 --mount type=bind,source=$REPO,target=/workspace,readonly --mount type=bind,source=$SCRATCH/docker,target=/scratch --workdir /workspace --env TMPDIR=/scratch/tmp --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 scripts/act_ci.py --selftest
sudo -n docker run --rm --user 1000:1000 --network none --read-only --cap-drop ALL --security-opt no-new-privileges --pids-limit 256 --memory 2g --cpus 2 --mount type=bind,source=$REPO,target=/workspace,readonly --mount type=bind,source=$SCRATCH/docker,target=/scratch --workdir /workspace --env TMPDIR=/scratch/tmp --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 /scratch/flat_selftest.py
```

## Firmware size

```sh
python3 $EVIDENCE/scripts/r8/fw_size.py $REPO $SCRATCH/capture52/1x1-50-on/capture-1x1-50-on $SCRATCH/size52
```

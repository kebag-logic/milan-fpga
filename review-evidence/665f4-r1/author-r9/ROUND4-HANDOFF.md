[A560]

# Historical round-4 handoff

Head: `6f7deea15a9160761b30aaa93fe152f20d416695`. The pin, publication wording and remaining-work statements below describe round 4 only. Round 5 supersedes them in HANDOFF.md.

## Round 4


Assignment: issue #665 comment 6036454509. This additive commit addresses R532-3-F1 (Tests) and R532-3-F2 (Tests, Docs). Production sources, pins, generated files, coverage ratchet and exclusions are unchanged. Independent re-review owns finding closure and the lens ledger.

| File:line | Change |
|---|---|
| `sw/firmware/ctrl/test/srp_mbx.cpp:819` | Join an ineligible binding to an already-declared StreamID in the other slot, then remove the original before polling; require Lv and reject stale Ready renewal. Both slot orders and every interface execute. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:851` | Rebind a still-registered Talker beside an unrelated Ready StreamID; require a fresh wire Ready for the rebound identity. Both slot orders and every interface execute. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:886` | Final unbind withdraws the Listener but preserves and renews the current Domain VLAN. Startup VID 2 and peer-selected VID 7 run in both slots on every interface. |
| `sw/firmware/ctrl/test/srp_mutants.py:487` | Add exact counterparts of reviewer plants RP3, RP10 and RP5, each requiring its named test and wire diagnostic. |
| `sw/firmware/ctrl/srp/README.md:65` | State the current Domain-VID exception to final-binding release. |

| New test | Planted defect | Required failed observable |
|---|---|---|
| `JoiningIneligibleBindingWithdrawsReadyWhenOriginalLeaves` | `joining-binding-loses-applicant`: inherit only from the replaced slot (RP3) | `d.event`: JoinMt renews stale Ready where only Lv is permitted; the test also requires the missing Lv. |
| `ReboundStreamCannotInheritAnotherStreamsReady` | `applicant-inherited-across-streams`: remove StreamID keying (RP10) | `ready`: no Ready emitted for the rebound identity. |
| `FinalDomainVidUnbindKeepsSrClassMembership` | `final-unbind-withdraws-domain-vid`: remove the Domain-VID guard (RP5) | `d.event`: MVRP Lv emitted for the retained SR class VLAN. |

The positive adapter suite passes 53 cases at IF=1 and IF=2. The three new plants are caught at IF=2. Coverage passes at the unchanged 15-file 100% ratchet; the full table below remains numerically current. The complete firmware command passes all 100 control plants, all 70 SRP plants and both dependency-refusal controls. Final receipts are retained in ROUND4-GATES.json and round4-receipts/. Builder bank and compiler-absent check remain with the manager under the round-4 assignment. No push, PR edit, merge, rebase, amend or hardware work occurred.

Development checks first caught two test formatting violations. Splitting the array initializers across lines matches the existing test style and clears the C++ gate. The initial RP3 campaign matched the missing-Lv diagnostic after several identical trace markers; its failure reader selected the earlier stale-renewal failure instead. The plant now requires that earlier `d.event` wire failure. Assertions and the grading function are unchanged.

The first full campaign started before the diagnostic-match correction and retained the old imported match string. It returned 1 for that same RP3 grading mismatch. A fresh complete invocation on the final committed sources returns 0. ROUND4-DEVELOPMENT.json records these preliminary failures separately; none is counted as passing final evidence.

## Coverage

`fw_coverage.py --check --jobs 4` passes at the unchanged ratchet. All 15 files remain at 100% lines and branches after existing exclusions. No ratchet regeneration or exclusion change was needed.

| File | Lines | Branches |
|---|---:|---:|
| `sw/firmware/ctrl/adp/adp.c` | 204/204 | 95/95 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/38 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 14/14 | 8/8 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 |
| `sw/firmware/ctrl/mbx/mbx.c` | 177/177 | 68/68 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 441/441 | 410/410 |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/198 | 106/106 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 |

## Gates

Every final command below returns 0 at the committed source. The firmware command includes the complete SRP campaign. ROUND4-GATES.md and ROUND4-GATES.json record durations, commands, raw log sizes and hashes; round4-receipts/ retains normalized small logs. Raw paths are replaced by `$SOURCE`, `$SCRATCH`, `$SDK` and `$DOCS_ENV` only in retained text; raw and normalized hashes are distinct.

| Command | rc | Seconds |
|---|---:|---:|
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir $SCRATCH/firmware-final` | 0 | 397.062 |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep $SCRATCH/coverage-final` | 0 | 151.755 |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 0.465 |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 4.475 |
| `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | 57.877 |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 90.736 |
| `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.166 |
| `python3 scripts/ci_rv32_sdk.py --destination $SDK` | 0 | 1.368 |
| `python3 scripts/docs_check.py` | 0 | 5.78 |
| `python3 scripts/docs_check.py --selftest` | 0 | 0.164 |
| `python3 scripts/check_doc_paths.py` | 0 | 0.114 |
| `python3 scripts/gen_toc.py --check` | 0 | 4.378 |
| `python3 scripts/check_em_dash.py --base c1049de1970e93d2c36ace62891ee9d947cd3191` | 0 | 3.277 |
| `python3 scripts/check_doc_style.py` | 0 | 0.064 |
| `python3 scripts/check_cpp_idiom.py` | 0 | 1.619 |
| `python3 scripts/check_py_idiom.py` | 0 | 4.326 |
| `python3 scripts/check_hygiene.py --check` | 0 | 0.415 |
| `python3 sw/mailbox/gen_mailbox.py --check` | 0 | 0.164 |
| `git diff --check c1049de1970e93d2c36ace62891ee9d947cd3191 HEAD` | 0 | 0.004 |

Firmware positives include 53 adapter, 3 debug, 4 latency and 5 selected processor-wire cases at each interface count, five entity shapes at IF=1/2, and the freestanding target builds. The saved-state gate passes 435 tests across five shapes. Shared controls pass 28 coverage cases, 17 RV32 checks, 18 tally mutations and 25 SDK tests. The three new SRP plants fail their named tests at IF=2; all 70 mappings are in ROUND4-TESTS.md.

The builder bank and compiler-absent check remain with the manager under assignment 6036454509. The latter passed for round 3 in the manager run (6036186046), following ruling 6036016117. No new round-4 result is claimed for either delegated check. No HDL or processor source changed in this round, so their retained round-3 gate receipts were not rerun as part of this tests-and-docs assignment.

## Integrity and resource bounds

One additive, one-line commit follows `c1049de1970e93d2c36ace62891ee9d947cd3191`; no amend or rebase. Its subject is `test: discriminate shared SRP inheritance and Domain VID retention`. The parent checkout and all four initialized submodules are clean, including ignored files and index flags. The exact parent pin for lwSRP remains `23d9a8173b07503a0ee6e8528f922fceab4e67f0`. The separate dependency clone is unchanged; its production sources equal that pin. ROUND4-INTEGRITY.json and ROUND4-SOURCE.json record the checks and source hashes.

The service memory peak was 3,023,376,384 bytes, below 9 GB; final current use was 1,621,590,016 bytes. Final free space on the data volume was 77,308,674,048 bytes, above the 30 GB floor. All commands ran in the foreground under ten-minute limits. Campaigns used at most four workers. The pinned HDL compiler was exported; no HDL build was needed. Build products and packages remain in disk scratch. The output packet contains no file above 200 KB; ROUND4-ARTIFACTS.json records hashes and sizes without copying build products.

## Prior evidence and remaining integration

ROUND3-HANDOFF.md retains the previous changes, 67-plant table, sizes and gate attempts with a ruling addendum. Its dates, heads, timeouts and resource figures are historical. The current regression tables and file locations are the round-4 sections above and ROUND4-TESTS.md.

The integration role still owns publication, fresh independent review, hosted fetch access, later upstream pin adoption, the current-dev merge candidate, the builder bank and containment. No merge approval is claimed. F3 application composition, live MAAP/stream inputs and the target licence output remain owed from the assigned base. Host timing and linked-size evidence do not replace target scheduling, whole-call-chain stack proof or physical acceptance. No default all-fabric build, RTL, register map or shipping-image input changed.

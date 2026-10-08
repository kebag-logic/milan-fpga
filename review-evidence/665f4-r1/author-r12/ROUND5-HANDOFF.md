[A560]

# F4 handoff

Relates to #665. Branch: `665-f4-srp`. Head: `500b8f64443777685e6a54049d933476710d26f0`.
Status: Round 5 REVIEW READY for publication and independent review. This head is local. PR #690 already contains reviewed round-4 head `6f7deea15a9160761b30aaa93fe152f20d416695`; this packet does not imply that PR was never published. Executor [A560]; independent reviewers [R532] and [R533]. Both round-4 reviews were POSITIVE; they do not approve the new dependency head.

## Round 5

Assignment: issue #665 comment 6037276691, “F4 round 5 (lwSRP re-pin)”. The initial remote was confirmed as the assigned HTTPS repository and the initial clean HEAD matched `6f7deea15a9160761b30aaa93fe152f20d416695`. The original assignment and cited issues were read, including #608 and processor #134. One additive parent commit, `500b8f64443777685e6a54049d933476710d26f0`, has subject `Adopt public lwSRP main and preserve allocation refusal coverage`.

The parent now builds against public lwSRP main `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`, including upstream PR #12. Its atomic receive validation reserves temporary propagation storage before delivering receive indications. Four existing exhaustion fixtures previously left room for an attribute but not that reservation, so they refused reception before exercising the intended adapter allocation. They now complete real mailbox RX with poll dispatch temporarily disabled, exhaust the same static pool, restore normal polling and require the original refusal/retry/reset behavior. All four original minimum-held-block assertions and behavioral assertions remain. Production adapter sources, pool sizing, ratchet and exclusions are unchanged; no production adaptation was needed.

| Parent file:line | Change |
|---|---|
| `.github/workflows/rtl-fast.yml:241` | Correct the dependency-fetch comment; execution is unchanged. |
| `third_party/lwSRP:1` | Pin the gitlink to public main `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`. |
| `sw/firmware/ctrl/test/ctrl_arms.py:249` | Require that exact public commit in the source-integrity guard. |
| `sw/firmware/ctrl/test/srp_fixture.hpp:142` | Add receive_before_poll: complete real mailbox reception before exhausting the pool at the adapter poll boundary. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:333` | Stage Domain exhaustion after successful RX; retain old declaration until allocation retries. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:345` | Stage Listener exhaustion after successful RX; preserve binding and retry. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:449` | Stage sink VLAN exhaustion after successful RX; preserve independent memberships. |
| `sw/firmware/ctrl/test/srp_mbx.cpp:951` | Stage refused peer Domain before restart; require the old request to be discarded. |
| `sw/firmware/ctrl/README.md:136` | Document exact public pin and anonymous fetch. |
| `sw/firmware/ctrl/srp/README.md:166` | Explain exhaustion staging and rewritten Applicant-note base; line 219 records public-main adoption. |
| `sw/firmware/gtest/README.md:397` | Correct hosted control-gate scope and local saved-state/tally obligations. |
| `docs/testing/CI_WORKFLOWS.md:54` | Correct CI scope and public dependency status. |
| `docs/reference/SUBMODULES.md:26` | Update inventory pin; line 196 onward describes public fetch and merged fixes. |
| `docs/diagrams/submodule_boundaries.drawio:1` | Regenerate boundary source with the new gitlink. |
| `docs/diagrams/submodule_boundaries.svg:1` | Regenerate vector rendering with the same pin. |
| `docs/diagrams/submodule_boundaries.png:1` | Regenerate raster rendering; binary artifact, 380433 bytes, hash in ROUND5-ARTIFACTS.json. |
| `docs/diagrams/PNG_MANIFEST.json:10` | Regenerate source/render hashes through the diagram generator. |

Generated diagrams came from `python3 docs/diagrams/submodule_boundaries.gen.py`. The PNG was inspected for label and arrow readability. Generator no-drift and self-test gates pass. No generated scratch remains in the candidate tree.

## Local Applicant-note merge

In the separate dependency clone, local branch `f4-applicant-notes-r5` is at `ced667d8ee35929ab5f9e77a1c5396e173a693d8`. It merges main with `--no-ff` into rewritten notes head `72209a53a241cd5de4786d3e1b3aefcbdf5fa5d9`. Its parents are that notes head and `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`. Subject: `Merge main into Applicant note regressions`. README count and reversal-name conflicts were resolved by retaining both changes. Production `src/` is byte-identical to public main. This test merge is not the parent gitlink; the public main pin is already fetchable.

| Dependency file:line | Difference from public main |
|---|---|
| `README.md:45` | Record 87 tests and 19901 assertions. |
| `doc/tester.md:29` | Record default totals; line 70 records enabled-profile 19889 assertions. |
| `tests/unit/integration_test.c:352` | Carry pending Applicant JoinIn discriminator through the merge; registered at line 424. |
| `tests/check_reversals.py:76` | Carry pending-condition reversal; lines 185-188 require exact note tests to fail. |

Both profiles pass 87 unit tests: OFF has 19901 assertions, ON has 19889. Each passes three behavior scenarios with ten steps, all 94 reversals and restored positive suites. The manager publishes this local branch before its dependency PR. No dependency branch was pushed.

## Tests and planted defects

The four parent tests below are in `sw/firmware/ctrl/test/srp_mbx.cpp`. The helper at `srp_fixture.hpp:142` asserts exactly one received-frame increment. All four changed tests pass at IF=1 and IF=2; the listed plants fail their required named tests at IF=2.

| Changed test and line | Plant | Defect and observable |
|---|---|---|
| `DomainExhaustionPreservesOldDeclarationUntilRetry:333` | `domain-refusal-lost` | Treat a failed Domain allocation as success; domain.vid must retain its old VID, then retry. |
| `SinkDeclarationExhaustionRetriesWithoutLosingBinding:345` | `listener-refusal-lost` | Treat failed Listener allocation as success; declared stays clear until retry, while bound stays set. |
| `SinkVlanExhaustionRetriesAndDistinctMembershipsRemainIndependent:449` | `sink-vlan-refusal-lost` | Mark failed VLAN request accepted; vlan_requested stays clear and independent VIDs survive retry. |
| `RefusedPeerDomainDoesNotSurviveLinkRestart:951` | `reset-keeps-owed-domain` | Retain domain_owed through reset; restarted link must use startup VID 2, not refused peer VID. |

| Dependency test and file:line | Plant | Required distinction |
|---|---|---|
| `tests/unit/integration_test.c:327`, `applicant_receive_conditions_follow_link_mode` | `point-to-point-condition` | Note-4 transition depends on point-to-point mode. |
| Same test at line 327 | `shared-in-condition` | Note-5 transition depends on shared-medium mode. |
| `tests/unit/integration_test.c:352`, `pending_applicant_joinin_obeys_note_four` | `point-to-point-condition`, `pending-point-to-point-condition` | Pending Applicant JoinIn takes the note-4 conditional transition. |

ROUND5-TESTS.md maps all 70 SRP plants to current test positions and required diagnostics. ROUND5-CONTROL-TESTS.md maps all 100 control plants and additional required kills. The graders reject unrelated failures and build failures. The complete firmware command also rejects edited dependency source and an off-pin dependency checkout. All campaigns finish with zero escaped plants.

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


## Gate table

All 102 final recorded commands exit 0. ROUND5-GATES.md lists every exact command, directory and duration; ROUND5-GATES.json also records raw log sizes and hashes separately from normalized retained text. The following table groups the documentation bank. No earlier failing attempt counts as final evidence.

| Gate / command or receipt group | Result | rc |
|---|---|---:|
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir $SCRATCH/firmware-final` | 100 control and 70 SRP plants caught; two refusal controls, positives and target builds pass; 443.262 s | 0 |
| Same driver without `--self-test`, separate `firmware-positive-final` directory | Final committed source positives, 153.706 s | 0 |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep $SCRATCH/coverage-final` | 15 files, unchanged 100% ratchet, 173.53 s | 0 |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 435 tests over five shapes, 98.629 s | 0 |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 28 controls | 0 |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 17 controls | 0 |
| `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 18 cases and 18 plants | 0 |
| `python3 sw/mailbox/gen_mailbox.py --check` | Generated mailbox contract has no drift | 0 |
| `make -C $SCRATCH/mailbox/tb/verilator/mbx -j2 VERILATOR=$SCRATCH_PARENT/verilator-j8` | Both buses at IF=1/2, model, 13 cosimulation checks, five plants; 61.918 s | 0 |
| Dependency positives, OFF and ON | 87 unit tests and three behavior scenarios each | 0 |
| Dependency `tests/check_reversals.py`, OFF and ON | 94/94 caught each; 87.781 / 87.870 s | 0 |
| Dependency sentence, reference, reference-self-test and link gates | 975 sentences, 79 controls, 354 local and 20 public external links | 0 |
| `docs-00` through `docs-75` | All 76 assigned documentation-bank commands, including SDK provenance and 25 SDK controls | 0 |
| `docs-selftest`, `docs-wire`, `em-dash-final`, `docs-final`, `source-diff`, `ci-scope` | Final documentation checks, 77 wire checks, whitespace and CI scope controls | 0 |
| `docs-archive`, `docs-archive-feature`, `hdl-reference-final` | Exact committed export without Git metadata; fresh reference output | 0 |
| `linked-size-final` | Four links with verified runtime provenance, 7.150 s | 0 |

Firmware positives include 53 adapter, three debug, four latency and five selected processor-wire cases at each interface count, plus all five entity shapes at IF=1/2 and freestanding target builds. The full processor-only SRP suites were not rerun in round 5; the selected firmware differential was rerun. The archive docs check explicitly skips index parity without Git metadata; it does not replace the passing repository parity check.

The builder bank, including the bare-metal profile contract test, and compiler-absent check remain with the manager under assignment 6037276691. No new lane result is claimed for these delegated checks. Hosted checks, trusted local replication after publication, candidate merge validation and containment remain integration work.

## Linked size and timing

New links use the final parent head and public dependency pin. ROUND5-SIZES.json records sections, static allocations and ELF/map hashes. ROUND5-RUNTIME.json identifies unchanged freestanding runtime inputs with verified hashes.

| Shape / IF | Prior span bytes | Round-5 span bytes | Increase | Static pool bytes | Adapter bytes | Reserved stack bytes |
|---|---:|---:|---:|---:|---:|---:|
| 1x1 / 1 | 53968 | 54592 | 624 | 9920 | 3288 | 8192 |
| 1x1 / 2 | 65216 | 65840 | 624 | 19840 | 3488 | 8192 |
| 8x8 / 1 | 68656 | 69280 | 624 | 24032 | 3696 | 8192 |
| 8x8 / 2 | 94656 | 95296 | 640 | 48064 | 4304 | 8192 |

These are linked size fixtures, not booted or routed images. The 8192-byte stack reservation is an assumption, not a whole-call-chain proof. Pools and adapter storage are unchanged. Linked span includes alignment.

ROUND5-TIMING.md records every host timing row with elapsed time, protocol wait and service time. Under the documented allowance of 100 ns per mailbox access, 1 ms total CPU/preemption time per action and 100 ns uncertainty, the largest observed service time is 1020400 ns, within the shared 10 ms budget. The 11 ms full-ring stall fails the budget predicate. Target scheduling and physical timing remain separate release evidence. D1/D2 processor differences remain documented; no equivalence beyond selected wire cases is claimed.

## Development attempts and integrity

Initial firmware and coverage runs failed four exhaustion fixtures because upstream receive reservation preceded the intended adapter allocation. The staging correction fixes the fixtures without changing expected behavior or weakening the ratchet. The first mailbox scratch invocation lacked the tracked common harness header; adding byte-identical `tb/common` inputs enabled the full gate. ROUND5-DEVELOPMENT.json retains these three non-final failures separately.

The final parent, all initialized submodules and the separate dependency clone are clean, including ignored residue and index flags. Every tracked file was checked against its HEAD blob. ROUND5-INTEGRITY.json records the parent tree and dependency heads. ROUND5-SOURCE.json records relevant per-file sizes and SHA256 values. ROUND5-MAILBOX-SOURCE.json binds the isolated mailbox inputs. Generated caches and builder outputs were moved to disk scratch after the final gates.

Service memory peaked at 3547467776 bytes, below 9 GB; final current use was 1495896064 bytes. Data-volume free space was 73505120256 bytes, above 30 GB. Commands ran in the foreground under ten-minute limits. Campaigns used at most four workers; mailbox builds permitted at most two HDL compilations with eight inner jobs each. Release 5.050 was explicitly selected. No package, environment, tree export or build binary is in the packet; each retained file is at most 200000 bytes. ROUND5-ARTIFACTS.json records unretained artifact sizes and hashes.

## Publication and remaining integration

PR-BODY.md now describes the published round-4 PR and local round-5 candidate accurately, correcting R532-2-R2's stale publication wording. The parent pin is already public; later adoption of it is no longer owed. The manager publishes the parent head and Applicant-note merge, then obtains fresh independent reviews and the reviewer-owned lens ledger. No executor review verdict or merge approval is claimed.

F3 composition, live MAAP/stream inputs and the connected target licence output remain owed from the assigned base. The default all-fabric build, shipping-image inputs, RTL, register map and production adapter source are unchanged. No parent merge, push, PR edit, rebase, amend or hardware operation occurred. The manager retains integration onto current dev and post-merge containment.

ROUND4-HANDOFF.md and earlier packets are historical. ROUND5 files contain current evidence. REVIEW-READY.md supplies the final authorized comment on #665.

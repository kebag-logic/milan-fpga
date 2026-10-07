[A560]

# F4 handoff

Relates to #665. Branch: `665-f4-srp` -> `dev`.
Round 6 REVIEW READY locally at `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`. Commits are unpushed.
The parent worktree, all four submodules and the separate dependency clone are clean.
No review verdict or finding closure is claimed.

## Round 6

The latest assignment is issue comment 6038730087. R533-5-F1 and R532-5-F1
identified the same recoverable receive-allocation defect. The Round 5 claim
that production needed no adaptation was incorrect: dropping a valid refused
PDU lost withdrawals and attributes later in a partially applied payload.

The adapter now owns one complete static mailbox record on allocation refusal.
It preserves interface, arrival timestamp and bytes across repeated failures.
Later SRP records and binding changes wait. Each poll retries after owed output,
coalesced ticks and lifecycle events. A matching link reset or destroy cancels
retained input; another interface's reset does not. Genuine invalid input alone
increments malformed. No peer retransmission is needed after storage recovers.
The unchanged R533 probe reports `active=0 received=2 malformed=0 stops=1`.

Assigned dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df` was merged with `--no-ff` as
`069874955e9c1061872d47afc3b7e57fc24e19bd`. F2 MAAP tests and coverage were
preserved. Explicit application attachment and the linked fixture compose ADP,
MAAP and SRP, including receive, event and tick enables. F2's shared `NDEBUG`
flag is explicitly undone in the SRP debug arm so assertion tests still apply.
The final test-only follow-up uses a typed byte array to satisfy C++ style.

The parent pins public lwSRP main `9197193e47a6bb1c45a56d90a18c1784123aba44`, including merged PR #15.
The separate dependency clone remains on local branch `f4-applicant-notes-r5`
at `f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152`; its production sources equal the
public pin. No dependency source edit, commit or push was made in this round.

R532-5-R1: Round 5 `500b8f64443777685e6a54049d933476710d26f0` is already published in PR #690; this new head is local.
R532-5-R2: Applicant-note tests are now recorded as published and merged.
R532-5-S1: the obsolete timer-removal statement is corrected under this assignment.
R532-5-S2: higher-version skip and whole-invalid-PDU rejection now have adapter cases.

## Changes with file locations

Positions are at the candidate head. Imported F2 files are included so the
complete delta from the published Round 5 head can be reconstructed.

| File:line or binary artifact | Change |
| --- | --- |
| `docs/design/MAILBOX_SPLIT.md:420` | Imported F2 timer-slot ownership documentation. |
| `docs/diagrams/PNG_MANIFEST.json:12` | Generator-owned image hash for the public dependency pin. |
| `docs/diagrams/submodule_boundaries.drawio:1` | Generated dependency graph at the pinned revision. |
| `docs/diagrams/submodule_boundaries.png` | Generated raster; only hash and size are retained in this packet. |
| `docs/diagrams/submodule_boundaries.svg:72` | Generated dependency graph at the pinned revision. |
| `docs/reference/SUBMODULES.md:26` | Public main pin and merged PR #12/#15 status. |
| `sw/firmware/ctrl/README.md:9` | Semantic merge of F2 MAAP documentation and the public SRP pin. |
| `sw/firmware/ctrl/app/ctrl_app.c:8` | Imported F2 optional MAAP startup. |
| `sw/firmware/ctrl/app/ctrl_app.h:26` | Imported F2 contract plus explicit SRP attachment and storage lifetime. |
| `sw/firmware/ctrl/app/ctrl_app_srp.c:1` | Compose ADP/MAAP/SRP; preserve all receive/event enables and enable ticks. |
| `sw/firmware/ctrl/maap/README.md:1` | Imported F2 MAAP implementation, interface or authoritative documentation; unchanged from assigned dev. |
| `sw/firmware/ctrl/maap/maap.c:1` | Imported F2 MAAP implementation, interface or authoritative documentation; unchanged from assigned dev. |
| `sw/firmware/ctrl/maap/maap.h:1` | Imported F2 MAAP implementation, interface or authoritative documentation; unchanged from assigned dev. |
| `sw/firmware/ctrl/maap/maap_csr.c:1` | Imported F2 MAAP implementation, interface or authoritative documentation; unchanged from assigned dev. |
| `sw/firmware/ctrl/maap/maap_csr.h:1` | Imported F2 MAAP implementation, interface or authoritative documentation; unchanged from assigned dev. |
| `sw/firmware/ctrl/maap/maap_mbx.c:1` | Imported F2 MAAP implementation, interface or authoritative documentation; unchanged from assigned dev. |
| `sw/firmware/ctrl/maap/maap_mbx.h:1` | Imported F2 MAAP implementation, interface or authoritative documentation; unchanged from assigned dev. |
| `sw/firmware/ctrl/srp/README.md:43` | Recoverable RX contract, ordering, timing limits, composition and publication corrections. |
| `sw/firmware/ctrl/srp/srp_mbx.c:266`, `:291`, `:349`, `:355`, `:400`, `:577`, `:649` | Retain allocation-refused records, retry in order and cancel on matching lifecycle reset. |
| `sw/firmware/ctrl/srp/srp_mbx.h:71` | Static owned receive record and binding-backpressure contract. |
| `sw/firmware/ctrl/test/ctrl_arms.py:16` | Preserve F2 MAAP arms and validate the public lwSRP pin. |
| `sw/firmware/ctrl/test/ctrl_build.py:36` | Imported F2 MAAP source/test build support and release flags. |
| `sw/firmware/ctrl/test/ctrl_image.c:17` | Link all three protocol paths and retain MAAP allocation state in the size fixture. |
| `sw/firmware/ctrl/test/ctrl_image.py:62` | Compile the composition and require reachable MAAP/SRP symbols. |
| `sw/firmware/ctrl/test/ctrl_mutants.py:24` | Imported F2 MAAP campaign and disjoint control sharding. |
| `sw/firmware/ctrl/test/maap_differential.py:1` | Imported F2 MAAP tests, differential or defect campaign; unchanged from assigned dev. |
| `sw/firmware/ctrl/test/maap_mutants.py:1` | Imported F2 MAAP tests, differential or defect campaign; unchanged from assigned dev. |
| `sw/firmware/ctrl/test/srp_app.cpp:1` | Positive and refusal tests for the shared loop and wake sources. |
| `sw/firmware/ctrl/test/srp_arms.py:15`, `:61` | Compile composition on host/target; explicitly restore assertions in debug arms. |
| `sw/firmware/ctrl/test/srp_latency.cpp:141` | Recovery is charged from the original arrival; an 11 ms delay fails the budget predicate. |
| `sw/firmware/ctrl/test/srp_mutants.py:512` | Twenty additional named behavioral plants; prior seventy preserved. |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:1` | Eleven mixed/partial receive, ordering, lifecycle and wire-validation cases. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:4` | Merge F2/SRP positives, coverage arms, mutation sharding and four-worker cap. |
| `sw/firmware/ctrl/test/test_maap.cpp:1` | Imported F2 MAAP tests, differential or defect campaign; unchanged from assigned dev. |
| `sw/firmware/ctrl/test/test_maap_debug.cpp:1` | Imported F2 MAAP tests, differential or defect campaign; unchanged from assigned dev. |
| `sw/firmware/ctrl/test/test_maap_differential.cpp:1` | Imported F2 MAAP tests, differential or defect campaign; unchanged from assigned dev. |
| `sw/firmware/ctrl/test/test_maap_mbx.cpp:1` | Imported F2 MAAP tests, differential or defect campaign; unchanged from assigned dev. |
| `sw/firmware/gtest/README.md:349` | Correct stale timer-removal claim; preserve coverage exclusions. |
| `sw/firmware/gtest/coverage.ratchet:7` | Generator-updated 19-file 100% floors, including F2 MAAP and new composition. |
| `tb/verilator/mbx/Makefile:20` | Imported F2 bounded mailbox build jobs. |
| `third_party/lwSRP` | Exact published main pin including merged PR #15. |

## Tests and planted defects

All new cases run at IF=1 and IF=2. The unrelated-interface reset case exercises
its body at IF=2. The following twenty plants map every new receive, composition
and timing case to a required failure. Build failures never count as catches.
`ROUND6-TESTS.md` contains the complete 90-plant SRP map;
`ROUND6-CONTROL-TESTS.md` contains all 196 control/MAAP plants and additional kills.

| Named test and file:line | Planted defect | Required failure |
|---|---|---|
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:25`: `SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission` | `receive-retry-removed` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:58`: `SrpRetry.PartialPayloadKeepsLaterAttributesAndDoesNotRepeatStop` | `partial-receive-retry-removed` | `domain.vid` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:25`: `SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission` | `receive-record-lost` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:25`: `SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission` | `receive-refusal-malformed` | `adapter.malformed` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:80`: `SrpRetry.LaterRecordsCannotOvertakeRetainedInterface` | `receive-overtakes-retained` | `loop.stats.rx_records` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:104`: `SrpRetry.LinkResetCancelsRetainedPayloadAndFencesLaterOldRecords` | `reset-keeps-retained-receive` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:122`: `SrpRetry.OtherInterfaceResetPreservesRetainedPayload` | `peer-reset-cancels-retained-receive` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:141`: `SrpRetry.DestroyCancelsRetainedPayloadBeforeReinitialization` | `destroy-keeps-retained-receive` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:25`: `SrpRetry.RefusedMixedPayloadRetriesWithoutPeerRetransmission` | `bind-overtakes-retained-receive` | `srp_mbx_bind` |
| `sw/firmware/ctrl/test/srp_app.cpp:22`: `SrpApp.AllThreeProtocolsShareTheLoopAndWakeSources` | `composition-attach-omitted` | `app.loop.n_ticks` |
| `sw/firmware/ctrl/test/srp_app.cpp:22`: `SrpApp.AllThreeProtocolsShareTheLoopAndWakeSources` | `composition-srp-irq-omitted` | `model.irq_enable` |
| `sw/firmware/ctrl/test/srp_app.cpp:22`: `SrpApp.AllThreeProtocolsShareTheLoopAndWakeSources` | `composition-srp-tick-omitted` | `app.loop.stats.ticks` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:154`: `SrpRetry.FailedParticipantRecreationRetainsFreshReceive` | `recreated-receive-retry-removed` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:172`: `SrpRetry.RetainedMvrpUsesItsOriginalParticipant` | `mvrp-receive-retry-removed` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:195`: `SrpRetry.RetainedReceiveWaitsForOwedTransmit` | `receive-retry-passes-owed` | `adapter.pending_rx.len` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:213`: `SrpRetry.RetainedReceiveWaitsForTickAndLifecycleBacklogs` | `receive-retry-passes-backlog` | `adapter.received` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:240`: `SrpRetry.WholeInvalidPduIsMalformedAndFutureUnknownMessageIsSkipped` | `future-receive-refused` | `adapter.ifs[0].active[0]` |
| `sw/firmware/ctrl/test/srp_rx_retry.cpp:240`: `SrpRetry.WholeInvalidPduIsMalformedAndFutureUnknownMessageIsSkipped` | `invalid-suffix-uncounted` | `adapter.malformed` |
| `sw/firmware/ctrl/test/srp_app.cpp:6`: `SrpApp.AttachRefusalPreservesExistingComposition` | `composition-refusal-ignored` | `ctrl_app_attach_srp` |
| `sw/firmware/ctrl/test/srp_latency.cpp:142`: `SrpLatency.ReceiveRecoveryKeepsOriginalArrivalBudget` | `recovery-latency-retry-removed` | `adapter.ifs[0].active[0]` |

The independent probe is unchanged from R533-5 `scripts/independent.cpp`.
Its four cases pass at both counts. A separate scratch-only retry-removal plant
fails `Srp.ReviewWithdrawDuringExhaustionSurvivesRecovery` on
`adapter.ifs[0].active[0]` at both counts. Its SHA and size are in
`ROUND6-ARTIFACTS.json`; positive and negative logs are retained.

## Coverage

Generated only by `fw_coverage.py --write`, then checked by `--check`.
No existing exclusion or floor is weakened. The adapter has no exclusions.
The three F2 MAAP rows remain at 100%; the composition adds the nineteenth file.
The table reports covered/total after the already documented exclusions.

| Portable file | Lines | Branches | After exclusions |
| --- | ---: | ---: | ---: |
| `sw/firmware/ctrl/adp/adp.c` | 204/204 | 95/95 | 100% / 100% |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/38 | 100% / 100% |
| `sw/firmware/ctrl/app/ctrl_app.c` | 31/31 | 20/20 | 100% / 100% |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 10/10 | 6/6 | 100% / 100% |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 | 100% / 100% |
| `sw/firmware/ctrl/maap/maap.c` | 209/209 | 140/140 | 100% / 100% |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 | 100% / 100% |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 98/98 | 60/60 | 100% / 100% |
| `sw/firmware/ctrl/mbx/mbx.c` | 177/177 | 68/68 | 100% / 100% |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100% / 100% |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100% / 100% |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100% / 100% |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100% / 100% |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100% / 100% |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 459/459 | 432/432 | 100% / 100% |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 | 100% / 100% |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/198 | 106/106 | 100% / 100% |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 | 100% / 100% |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 | 100% / 100% |

## Gate table

All 98 final recorded invocations exit 0. `ROUND6-GATES.md` expands exact
commands, environment variables and durations. `ROUND6-GATES.json` distinguishes
raw log hashes from normalized retained logs. Development failures are recorded
separately and are not counted as successful evidence. They include initial
fixture/plant diagnostics, the debug-flag merge conflict, and style corrections.
The compiler-absent entry and builder bank remain manager-owned by assignment.

| Gate | Command / receipt entry point | Result |
| --- | --- | --- |
| Firmware, RV32 and mutations | `test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard I 2 --jobs 4`, I=0,1 | Both rc 0; 196 control/MAAP and 90 SRP plants, plus two pin controls |
| Portable coverage | `fw_coverage.py --check --jobs 4` | rc 0; 19 files, 100% lines/branches after unchanged exclusions |
| NVM firmware | `test_ctrl_nvm.py --require-rv32 --jobs 4` | rc 0; 435 tests over five shapes |
| Harness controls | `fw_coverage.py --selftest`; `fw_rv32_selftest.py --require-rv32`; `tally_selftest.py --mutants` | All rc 0; 28 coverage arms, 17 target controls, 18 tally arms and 18 plants |
| Mailbox contract and integration | `gen_mailbox.py --check`; `make -C $SCRATCH/mailbox/tb/verilator/mbx -j2 VBUILD_JOBS=8 VERILATOR=$HDL_J8_WRAPPER` | All rc 0; both buses/IF counts, model, 13 cosimulation checks and five plants |
| MAAP differential | `maap_differential.py --self-test --keep $SCRATCH/maap-diff` | rc 0; 12 positives and 16 plants |
| Dependency pin | OFF/ON profiles: CMake build, CTest, unit suite and Behave | rc 0; 87 unit tests and three scenarios per profile |
| R533 independent probe | `python3 $PACKET/round6-helpers/probes.py` | rc 0; four unchanged cases at IF=1/2, no retransmission |
| Independent retry control | `python3 $PACKET/round6-helpers/probe_control.py` | rc 0; removed retry fails required active-state check at IF=1/2 |
| Linked size | `python3 $PACKET/round6-helpers/images.py` | rc 0; four exact-head links and verified runtime hashes |
| Documentation bank | 75 commands, expanded in `ROUND6-GATES.md` | All final rc 0; style corrections retain their earlier failures in the development receipt |
| Extra documentation/integrity | No-Git archive, docs selftest, wire accountability, CI scope, final diff and source scan | All rc 0; clean parent and submodules, no hidden index flags |

## Linked size and timing

All values below are bytes. Spans include alignment and an 8192-byte stack
reservation; they are not a whole-call-chain bound. Every runtime input hash was
verified, and all links use the CI-pinned RV32 SDK. Pools are unchanged.
The largest fixture remains below 128 KiB. These fixtures were not booted.

| Shape / IF | Text | Read-only | BSS | Stack | RAM span |
| --- | ---: | ---: | ---: | ---: | ---: |
| endstation_ax7101_1x1_tdm8 / 1 | 33440 | 2846 | 18072 | 8192 | 62560 |
| endstation_ax7101_1x1_tdm8 / 2 | 34676 | 2846 | 29424 | 8192 | 75152 |
| endstation_ax7101_8x8 / 1 | 33380 | 2846 | 32824 | 8192 | 77264 |
| endstation_ax7101_8x8 / 2 | 34628 | 2846 | 58928 | 8192 | 104608 |


The host timing envelope charges 100 ns per mailbox access, one total 1 ms
CPU/preemption allowance per action, and 100 ns observation uncertainty.
Actions share one 10 ms service budget. Storage recovery is measured from the
original arrival; the 1 ms recovery passes, while an 11 ms exhaustion or full
TX ring fails the budget predicate. Permanent exhaustion cannot guarantee a
finite delivery bound. Target scheduling and physical timing remain unproven.
`ROUND6-TIMING.md` retains the measured rows and explicit protocol waits.

## Integrity and remaining work

`ROUND6-INTEGRITY.json` verifies committed blobs, clean indexes/worktrees and
absence of ignored residue across the parent, four submodules and dependency clone.
Peak service memory was 5791272960 bytes, below 9 GB.
Final free disk space was 103928373248 bytes, above the 30 GB floor.
Generated images came from the repository generator. All packet files are under
200000 bytes; larger logs, ELF/maps and the diagram PNG are recorded by hash/size.
No toolchain, package, environment or source export is stored in the packet.

F3 is absent from the assigned F2 base, so ACMP binding calls remain owed.
Live stream/MAAP allocation updates and the fabric licence output remain target
integration. The default all-fabric build, shipping image, RTL and register map
are unchanged. No hardware or bench access was used. Full processor-only SRP
suites were not rerun; the selected firmware walk and wire differential were.

Both Round 5 reviews remain NEGATIVE until the reviewers re-evaluate this head.
The manager owns publication, hosted gates, trusted local replication, fresh
independent reviews and their lens ledger, candidate validation, merge approval
and post-merge containment. No push, PR operation, rebase or amend was performed.
The earlier STOP/publication wording is superseded by this Round 6 handoff.

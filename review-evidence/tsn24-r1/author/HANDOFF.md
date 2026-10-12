# ACMP DA freshness handoff

Status: REVIEW READY. All acceptance items are met, all final gates returned zero, and both commits are present in a clean working tree. No push or PR creation occurred.

Branch: `acmp-da-fresh`. Base, confirmed with `git rev-parse`: `1ba273540abbdf51ea5d235c0a7e81c0bcb5d475`. Preserved candidate commit: `917201098395f1f1acc635ea1722e6c9a91a3ec0`. Final head: `9ef7bd5281c0bb3f2967b11c5a5d8d74a75755d1`.

## Assignment and scope

- [Issue and acceptance](https://github.com/kebag-logic/tsn-c-stack/issues/24).
- [Exact assignment](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126061221).
- [Release-only size ruling](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126295947).
- [Initial TAKEN](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126084737); it was not repeated on resume.
- [Earlier size STOP](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126278688), superseded by the ruling. The uncommitted candidate was preserved and committed before the remaining campaign, as directed.
- Only ACMP core code changed. ADP, MAAP, wire helpers and existing ACMP tests are unchanged. One explicit Listener input was added. Existing clock and source callbacks provide the query's inputs; there is no new output callback or timer.

## References consulted

The read-only reference revision is `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. Its `docs/design/MAILBOX_SPLIT.md:1065` and `docs/reference/MAILBOX_CONTRACT.md:255` identify the old address-only gate. No change was made to that repository.

The processor submodule was unpopulated. Its pinned tree, `2ad2f845dd583f8310075fa2380cb60a04fd091a`, was read through the repository API; `docs/architecture/05_acmp_engine.md`, `hdl/acmp/KL_acmp_talker.sv` and `hdl/acmp/pp_acmp_pkg.sv` were retained only in scratch. `KL_acmp_talker.sv:396` uses unsigned elapsed time strictly less than the interval. The engine documentation's declaration predicate combines valid destination with fresh demand or any registered Listener.

Local Milan v1.2 clause 4.3.3.1 and IEEE 1722.1-2021 clauses 8.2.1.9–8.2.1.13 were consulted, together with repository verification, coding standard, porting, architecture and the entity generator from #20. No standards text is reproduced. The issue selects accepted probe answers as the freshness start; the normative clause and processor describe received probes. This local acceptance point is documented in `docs/PORTING.md`.

## Changes

Line numbers refer to the final working tree.

| File:line | Change |
|---|---|
| `include/acmp.h:294` | Configured freshness interval; per-source timestamp, answered flag and Listener level; one input and declaration query. |
| `src/acmp.c:113` | Record compatible probe replies only after accepted transport, using the existing clock. Query unsigned elapsed age and live destination validity; validate the Listener input without callbacks. |
| `scripts/entity_yaml.py:95` | Accept an optional ACMP mapping, validate exactly 15000 ms and emit that value into each generated initializer. |
| `configs/talker.yaml:3` | Explicit entity freshness configuration example; older documents select the normative default. |
| `examples/entities/listener/entity_config.c:35` | Regenerated Listener configuration with the normative interval. |
| `examples/entities/talker/entity_config.c:35` | Regenerated Talker configuration with the normative interval. |
| `examples/entities/duplex/entity_config.c:46` | Regenerated duplex configuration with the normative interval. |
| `examples/entities/ax7101/entity_config.c:35` | Regenerated compatibility configuration with the normative interval. |
| `examples/entity_roundtrip.c:226` | Shared generated-configuration, Listener, window, wrap and invalid-destination check. The source callback reads the local validity level. The final invalid-address probe avoids a false redundant-assignment finding without a suppression. |
| `examples/entity_roundtrip.h:11` | Expose the shared round-trip entry. |
| `examples/rv32/smoke.c:301` | Execute the shared freshness check on both freestanding configurations. |
| `tests/test_acmp.cpp:2265` | Fourteen new tests. Stale and exact-edge scenarios own their before/after-wrap checks; existing ACMP tests are unchanged. |
| `tests/test_entity.cpp:24` | Hosted invocation of the shared freshness round trip. |
| `scripts/entity_selftest.py:148` | Exercise default, emission, exact numeric value, wrong types, omitted field and unknown key. |
| `tests/mutations.json:5351` | Fifteen new named plants, one for every added hosted test; keep the existing final three golden controls in place. |
| `tests/coverage.ratchet:5` | Update the measured ACMP denominator to 792 lines and 390 branches, with all covered and no new exclusion. |
| `docs/PORTING.md:309` | Predicate, accepted-answer timestamp, Listener aggregation, source/interface isolation, exact edge, wrap and service duties. |
| `docs/ENTITY_YAML.md:51` | Optional mapping, strict normative value and shared round-trip description. |
| `docs/REQUIREMENTS.md:38` | ACMP-11 behavior, local issue origin, normative clause and both targets; add its required table row. |
| `docs/requirements.json:203` | Machine-readable requirement, clause links and issue origin. |
| `scripts/requirement_records.py:17` | Pin the new local issue origin. |
| `docs/TRACEABILITY.md:25` | Regenerate clause-to-test links and retained requirement dispositions. |
| `docs/TESTS.md:91` | Regenerate the test-to-planted-defect inventory. |
| `docs/VERIFICATION.md:24` | Update the full campaign count to 359 core and four generated-configuration plants. |
| `include/acmp.h:405` | Per-source answer timestamp, answer flag and aggregate Listener level. |
| `include/acmp.h:416` | Fixed source-state array owned by the ACMP instance. |
| `include/acmp.h:475` | Public Listener input and declaration query signatures. |
| `src/acmp.c:1237` | Refuse re-entry and invalid source/interface; update the Listener level without port calls. |
| `src/acmp.c:1250` | Expire observed probe demand and combine it with current destination validity and Listener level. |
| `scripts/entity_yaml.py:233` | Emit the validated interval into generated ACMP C configuration. |
| `examples/entity_roundtrip.c:118` | Expose the example port validity level through the existing source callback. |

The declaration query returns destination-valid AND (answered probe age less than the configured interval OR registered Listener). Successful and destination-allocation-failure replies both record demand when accepted. Refused or queued responses do not start the clock. Unknown-source, incompatible-interface and other replies do not refresh demand.

Listener registration is an aggregate level for the source's current Stream ID and configured interface, including Asking Failed. The input makes no callback; false means the final matching registration has left. It is not a media admission licence. Each source owns independent state. The integrator queries after events and on its regular service tick even when `acmp_poll` reports no owed frames. Observed expiry is sticky until another answer. The existing less-than-half-counter-range service contract remains required; a completely unobserved counter revolution cannot be inferred from a 32-bit clock.

## Tests, plants and removals

All fifteen new hosted tests have caught plants and individual physical-removal escapes. The removal control deletes the complete named test declaration from a scratch translation unit, rebuilds, reconciles executable registration, and runs every remaining test in that executable. It uses no test filter. For ACMP this is 93 tests before removal and 92 after; for the generated entity it is four before and three after. The five acceptance terms are independently covered by `NoProbe`, `StaleProbe`, `WindowEdge`, `ListenerWithoutProbe` and `InvalidAddress`.

The campaign mutates the executable arm named by each plant, as the repository driver specifies. These removal results do not claim that a global removal of checks from all targets would escape: the independent shared entity/RV32 check intentionally retains boundary and wrap coverage.

| Test | Planted defect | Catch and escape evidence |
|---|---|---|
| `AcmpFresh.NoProbe` | `dafresh-unanswered-clock` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.StaleProbe` | `dafresh-expiry-equality` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.WindowEdge` | `dafresh-inclusive-edge` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.WithinWindowAndRefresh` | `dafresh-no-renewal` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.ListenerWithoutProbe` | `dafresh-listener-needs-probe` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.InvalidAddress` | `dafresh-ignore-address` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.ClockWrap` | `dafresh-absolute-clock` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.ConfiguredWindow` | `dafresh-fixed-window` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.DeferredAnswer` | `dafresh-refused-answer` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.FailedAllocationAnswer` | `dafresh-only-success` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.OtherRepliesDoNotRefresh` | `dafresh-state-reply-demand` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.SourceAndInterfaceIsolation` | `dafresh-wrong-source` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.InputGuardsAndReentry` | `dafresh-wrong-interface` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `AcmpFresh.ListenerWithdrawalAndReset` | `dafresh-reset-retains-demand` | Full ACMP binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 92 remaining tests pass. |
| `EntityYaml.DaFreshRoundTrip` | `dafresh-generated-window` | Full entity binary: rc 1, only its named assertion/test fails. Delete that test declaration, rebuild: rc 0, 3 remaining tests pass. |
| `EntityTests.test_dafresh_configuration` | `dafresh-schema-range`: widen maximum to 15001 | Baseline: 197 pass. Plant: only this test fails. Remove it: 196 pass, rc 0. |

`removal-results.json` and `schema-results.json` hold the completed controls. `removal-controls.py` and `schema-control.py` reproduce them against a checkout and its mutation work directory. These controls use only scratch sources. The full campaign contains 363 plants; every required assertion must fail in a completed report. Crashes and compilation errors do not count as kills.

## Window edge and wrap

- At response acceptance, age 0 is fresh. `WithinWindowAndRefresh` advances the clock by 7 ms inside send, checks age 14999, sends again and checks a renewed 14999 ms window.
- `WindowEdge` checks age 15000 is false at start times 50000 and `UINT32_MAX - 999`. It repeats expiry while a Listener keeps the gate open, then withdraws that Listener and observes false immediately.
- `StaleProbe` checks age 15001 at both start times and confirms that returning to the old low clock value after observed expiry does not revive demand.
- Starting at `UINT32_MAX - 999` gives clock 13999 at age 14999, 14000 at age 15000, and 14001 at age 15001. `ClockWrap` also queries before rollover, catching an overflowing absolute deadline.
- `ConfiguredWindow` supplies 30000 ms to the low-level core and checks age 20000 is fresh, distinguishing the configured value from a mirrored 15000 constant. The YAML profile itself accepts exactly 15000.
- Backpressure retains an unanswered frame for 20000 ms. A refused retry remains closed; accepted retry advances the clock by 9 ms and only then begins its fresh interval.
- `entity_check_dafresh` verifies all generated intervals, no-probe, Listener registration/withdrawal, wrapped age 14999 and exact age 15000, and an answered invalid destination. The same function runs on Linux and both RV32 configurations.

## Gates

All 28 entries in `gates.json` have rc 0. Both RV32 results have rc 0. The post-commit privacy gate also passes. Initial setup failures were corrected; final evidence is from the completed rerun with the final tree.

| Gate | Hosted Linux | Bare-metal RV32 |
|---|---|---|
| GCC build and tests | Configure/build/test rc 0; eight binaries, 416 registered instances. | Separate freestanding GCC Debug and Release configure/build/link rc 0. |
| Clang, address/undefined sanitizers and leak detection | Configure/build/test rc 0; eight binaries. | Hosted instrumentation; no RV32 sanitizer claim. |
| Unit and shared smoke behavior | All existing tests and new freshness tests pass. | Both QEMU smoke executions rc 0, including the same generated freshness check. |
| Boundary and dependency pin | `check_boundary.py --selftest` and dependency controls rc 0, both hosted compilers. | Dependency, import, ABI, whole-archive link and unresolved-symbol audits rc 0 in Debug and Release. |
| Coverage and controls | rc 0; ACMP 792/792 lines, 390/390 branches. Every measured file remains 100% after existing exclusions. | No hosted coverage denominator claimed on RV32. |
| Comment contract and assertion needles/templates | All gates and compiling controls rc 0. | The repository source contract includes freestanding sources and cross-compile controls. |
| Conditional matrix | rc 0; 33 files, 58 region sides compiled. | Applicable RV32 source/assembly controls pass. |
| Port contracts and ACMP cache preservation | All controls rc 0. | Existing and new smoke publication checks pass; the new Listener input compiles and runs. |
| Entity golden/schema controls | rc 0; 197 schema controls. Extra range plant and removal rc 0. | Generated const entities compile and shared round trips execute. |
| Mutation and report controls | rc 0; all 363 plants caught. Fifteen added plants have individual physical-removal escapes, rc 0. | Campaign executes on Linux; RV32 uses focused shared smoke. |
| Registration, traceability and inventory | rc 0; 45 requirements, 142 declarations, 416 registered instances; every declaration has a plant. | Requirement disposition and shared test reference retain the mandatory second target. |
| Static analysis | rc 0, with no added suppression. | Includes the minimal port and freestanding smoke sources. |
| Licence, privacy, privacy controls and graphs | All rc 0; post-commit privacy rc 0. | Repository-wide gates also cover freestanding files. |
| Aggregate validation | `validate.py --jobs 16 --graphs`: rc 0, all 28 entries zero. | `baremetal.py --jobs 16`: rc 0, both configurations zero. |
| Release image growth | Not applicable. | +1304 bytes, below 2048. Debug +2208 is informational. |

Builds and campaigns were never piped. Expected rc 1 runs are confined to planted-defect catch evidence; the controls grading those runs return zero.

## Bare-metal image size

The loadable binary is measured with `objcopy -O binary`, including alignment gaps. The whole core archive is linked. The final smoke image includes the additional shared checks.

| Configuration | Before binary | Final binary | Growth | Ceiling |
|---|---:|---:|---:|---|
| Release | 35792 | 37096 | **1304 bytes** | 2048 bytes: pass; 744 bytes remain. |
| Debug | 45744 | 47952 | 2208 bytes | Informational under the ruling. |

The earlier candidate measured +1296 Release and +2168 Debug. The final example check ordering adds 8 Release bytes and 40 Debug bytes; no production behavior changed in this follow-up. Final ELF file sizes are 46784 Release and 142388 Debug. Data remains zero and BSS 65552 bytes. `sizes.json` records byte sizes and SHA-256 for baseline and final ELF and loadable images. No image is copied into this directory.

## Environment and reproduction

Scratch is `$VALIDATION_STORAGE/tsn24-a606/`; all temporary files, builds and installed dependency additions stay there. `env.sh` selects the pinned GoogleTest/GMock 1.14.0 and Clang 18.1.3. The supplied Clang launcher referenced a deleted directory. Scratch launchers use the intact pinned executable and libraries. Matching sanitizer and analysis packages plus compatible C++13 headers avoid the host's Clang23/GCC16-header mismatch. No shared installation was changed. Package byte counts and SHA-256 are in `ARTIFACTS.json`.

Independent campaigns use 16 jobs. The removal script limits simultaneous large C++ compilations to three while accepting the same jobs argument. Service memory was sampled every five seconds; its kernel peak was 5570236416 bytes, below 9 GB. No hardware or bench was used.

From the checkout, with the pinned dependencies on the search paths:

```sh
python3 scripts/entity_yaml.py --examples --check
python3 scripts/validate.py --work $VALIDATION_STORAGE/tsn24-a606/validation --jobs 16 --graphs
python3 scripts/baremetal.py --work $VALIDATION_STORAGE/tsn24-a606/rv32-final --jobs 16
python3 scripts/mutation.py --work $VALIDATION_STORAGE/tsn24-a606/mutations-new --jobs 16 --select dafresh-
python3 $MANAGEMENT/2026-09-23/tsn24-a606/removal-controls.py --root . --campaign $VALIDATION_STORAGE/tsn24-a606/mutations-new --work $VALIDATION_STORAGE/tsn24-a606/removals --jobs 16
python3 $MANAGEMENT/2026-09-23/tsn24-a606/schema-control.py --root . --work $VALIDATION_STORAGE/tsn24-a606/schema-control
riscv64-elf-objcopy -O binary $VALIDATION_STORAGE/tsn24-a606/rv32-final/release/rv32_smoke.elf $VALIDATION_STORAGE/tsn24-a606/rv32-final/release/rv32_smoke.bin
```

The manager owns the push and PR. [REVIEW READY comment](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126652895). `PR-BODY.md` starts with the lane label and uses `Closes #24` because acceptance 1–5 is complete. `CANDIDATE.patch` is the cumulative base-to-head diff. `ARTIFACTS.json` identifies retained reports and SHA-256/size records for larger scratch artifacts.

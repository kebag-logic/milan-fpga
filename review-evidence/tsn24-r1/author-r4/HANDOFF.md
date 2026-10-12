# ACMP DA freshness handoff

Status: REVIEW READY for Round 4. All 28 validation gates and both RV32 configurations return 0. All 388 registered plants are caught with zero escapes or errors. Every tested contract row has complete-suite catch and single-killer physical-removal evidence: 42 distinct plants, 424 to 423 completed instances. Post-commit privacy passes. The worktree is clean; no push or history rewrite occurred.

Branch: `acmp-da-fresh`. Main: `1ba273540abbdf51ea5d235c0a7e81c0bcb5d475`. Round 4 parent: `1edff3180c2ff435b855cc770fb8be371f2096b3`. Final head: `f13c9c16c2b300d158f980dd7c7f071dcb84df5b`. The new commit is `Complete ACMP freshness contract mutation coverage`, with the configured identity, one-line subject, no body or trailers. The Round 4 section below supersedes earlier historical results.

## Round 2

Authorities: [issue and acceptance](https://github.com/kebag-logic/tsn-c-stack/issues/24), [original assignment](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126061221), [Round 2 assignment](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6127660189), [Release-only ceiling ruling](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6126295947), [R630-1](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6127564342) and [R631-1](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6127654574). Both reviews were read in full.

R630-1-F1: the shared round trip now checks the generated 15000 ms configuration and one accepted probe opening the gate at age 1 ms. It has a dedicated clock field and no duplicate checks for no probe, stale probe, edge, wrap, Listener-without-probe or invalid destination. The previous removal claim covered individual binaries and did not prove escape across all hosted binaries. That claim is withdrawn and replaced by the complete-suite receipts below.

R630-1-F2: `AcmpFresh.ZeroWindow` protects zero's documented meaning: a probe cannot open the gate even at age zero; a Listener still opens it and withdrawal closes it. The registered `x-zero-never-expires` plant uses the reviewer's fail-open substitution. `acmp_init` now refuses values at or above 2^31 without changing the instance or calling ports. `AcmpFresh.WindowRange` accepts 2^31-1 and refuses both 2^31 and UINT32_MAX.

The positive-window plants `dafresh-inclusive-edge` and `dafresh-fixed-window` preserve zero's disabled meaning so their named positive-window tests remain their sole killers. The legacy `acmp-init-too-many-sources` substitution is unchanged; its text anchor excludes the expanded condition's closing parenthesis. Existing tests remain unchanged.

R630-1-R1: the port guide uses the exact requested attribution to this repository's reading of 'answered'. R631-D01: the configuration table now lists all four plants. Only ACMP production code changes; ADP, MAAP and wire helpers remain unchanged, and the port gains only the existing lane's one Listener input.

## Changes

Round 2 file:line inventory for the complete lane at `0868387`:

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
| `examples/entity_roundtrip.c:226` | Generated configuration and one positive freshness path; individual predicate terms, edge and wrap remain in hosted core tests. |
| `examples/entity_roundtrip.h:11` | Expose the shared round-trip entry. |
| `examples/rv32/smoke.c:301` | Execute the shared freshness check on both freestanding configurations. |
| `tests/test_acmp.cpp:2265` | Sixteen new core tests. Stale and exact-edge scenarios own their before/after-wrap checks; existing ACMP tests are unchanged. |
| `tests/test_entity.cpp:24` | Hosted invocation of the shared freshness round trip. |
| `scripts/entity_selftest.py:148` | Exercise default, emission, exact numeric value, wrong types, omitted field and unknown key. |
| `tests/mutations.json:5351` | Seventeen new named plants, one for every added hosted test; keep the existing final three golden controls in place. |
| `tests/coverage.ratchet:5` | Update the measured ACMP denominator to 792 lines and 392 branches, with all covered and no new exclusion. |
| `docs/PORTING.md:310` | Predicate, accepted-answer timestamp, Listener aggregation, source/interface isolation, exact edge, wrap and service duties. |
| `docs/ENTITY_YAML.md:51` | Optional mapping, strict normative value and shared round-trip description. |
| `docs/REQUIREMENTS.md:38` | ACMP-11 behavior, local issue origin, normative clause and both targets; add its required table row. |
| `docs/requirements.json:203` | Machine-readable requirement, clause links and issue origin. |
| `scripts/requirement_records.py:17` | Pin the new local issue origin. |
| `docs/TRACEABILITY.md:25` | Regenerate clause-to-test links and retained requirement dispositions. |
| `docs/TESTS.md:91` | Regenerate the test-to-planted-defect inventory. |
| `docs/VERIFICATION.md:24` | Update the full campaign count to 361 core and four generated-configuration plants. |
| `include/acmp.h:405` | Per-source answer timestamp, answer flag and aggregate Listener level. |
| `include/acmp.h:416` | Fixed source-state array owned by the ACMP instance. |
| `include/acmp.h:475` | Public Listener input and declaration query signatures. |
| `src/acmp.c:1237` | Refuse re-entry and invalid source/interface; update the Listener level without port calls. |
| `src/acmp.c:1250` | Expire observed probe demand and combine it with current destination validity and Listener level. |
| `scripts/entity_yaml.py:233` | Emit the validated interval into generated ACMP C configuration. |
| `examples/entity_roundtrip.c:118` | Expose the example port validity level through the existing source callback. |

Additional Round 2 locations:

| File:line | Change |
|---|---|
| `src/acmp.c:1015` | Refuse intervals at or above the unsigned clock half range. |
| `examples/entity_roundtrip.c:21` | Separate the clock from timer output. |
| `tests/test_acmp.cpp:2365` | Zero-window contract and Listener behavior. |
| `tests/test_acmp.cpp:2380` | Interval bounds, unchanged-state refusal and no port calls. |
| `tests/mutations.json:577` | Preserve the legacy source-count plant with its updated text anchor. |
| `tests/mutations.json:5351` | Register the zero-window and half-range plants. |
| `tests/mutations.json:5399` | Scope the exact-edge plant to positive windows. |
| `tests/mutations.json:5459` | Scope the mirrored-window plant to positive windows. |
| `docs/PORTING.md:246` | Add the configuration field and its accepted range. |
| `docs/PORTING.md:326` | Document initialization refusal. |
| `docs/PORTING.md:336` | Apply the exact attribution correction. |
| `docs/ENTITY_YAML.md:135` | Describe the narrow round trip and all four plants. |

## Per-test sensitivity

All eight hosted binaries execute with each plant present: 418 completed instances, only the named test fails, and its assertion-specific needle appears. Physically deleting only that test and rebuilding leaves 417 completed instances across all eight binaries, rc 0, with no failures or skips. Expected planted-suite rc 8 establishes sensitivity; the grading command returns 0. Receipts are `round2/complete-suite/results.json` and per-plant `full/` and `removed/` XML, logs and rc files.

| Test and source line | Plant | Complete suite | Only named test removed |
|---|---|---|---|
| `AcmpFresh.ZeroWindow` (`tests/test_acmp.cpp:2365`) | `x-zero-never-expires` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.WindowRange` (`tests/test_acmp.cpp:2380`) | `dafresh-half-range` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.NoProbe` (`tests/test_acmp.cpp:2283`) | `dafresh-unanswered-clock` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.StaleProbe` (`tests/test_acmp.cpp:2289`) | `dafresh-expiry-equality` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.WindowEdge` (`tests/test_acmp.cpp:2301`) | `dafresh-inclusive-edge` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.WithinWindowAndRefresh` (`tests/test_acmp.cpp:2317`) | `dafresh-no-renewal` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.ListenerWithoutProbe` (`tests/test_acmp.cpp:2329`) | `dafresh-listener-needs-probe` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.InvalidAddress` (`tests/test_acmp.cpp:2337`) | `dafresh-ignore-address` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.ClockWrap` (`tests/test_acmp.cpp:2347`) | `dafresh-absolute-clock` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.ConfiguredWindow` (`tests/test_acmp.cpp:2356`) | `dafresh-fixed-window` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.DeferredAnswer` (`tests/test_acmp.cpp:2396`) | `dafresh-refused-answer` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.FailedAllocationAnswer` (`tests/test_acmp.cpp:2411`) | `dafresh-only-success` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.OtherRepliesDoNotRefresh` (`tests/test_acmp.cpp:2419`) | `dafresh-state-reply-demand` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.SourceAndInterfaceIsolation` (`tests/test_acmp.cpp:2432`) | `dafresh-wrong-source` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.InputGuardsAndReentry` (`tests/test_acmp.cpp:2441`) | `dafresh-wrong-interface` | Named assertion caught; rc 8 | Escape; rc 0 |
| `AcmpFresh.ListenerWithdrawalAndReset` (`tests/test_acmp.cpp:2460`) | `dafresh-reset-retains-demand` | Named assertion caught; rc 8 | Escape; rc 0 |
| `EntityYaml.DaFreshRoundTrip` (`tests/test_entity.cpp:24`) | `dafresh-generated-window` | Named assertion caught; rc 8 | Escape; rc 0 |

The unchanged R630-1 scripts were obtained from the local review packet and match its `MANIFEST.sha256`. The remote branch and review-linked commit were unavailable. Copies are retained in `round2/review-scripts/`.

| Script | SHA-256 |
|---|---|
| `physical_removal.py` | `94ee3548584c95dcb0135b0be9676397896340766eb8eb9cd0e3b03a8f11b341` |
| `escape_probe.py` | `42a9e67dca97eb0aaee1ad3bbcecd904c3aace1240a6ef44bb018d5782d3aa7e` |

`physical_removal.py` supports core tests only. Its unchanged invocations cover all 16 core tests in pairs to bound memory. `escape_probe.py` covers all 16 `dafresh-*` plants, including the generated-entity case, and catches the zero-interval gap mutant. The supplementary `complete_suite.py` physically removes the entity test and independently grades all 17 complete suites from fresh XML, checking exact registration, no skips, the intended needle, and removal of exactly one test.

`EntityTests.test_dafresh_configuration` also catches the reviewer's `y-yaml-wide-range`; physically removing that Python test leaves all 196 others passing. Emission removal and default-zero plants fail the golden gate. The full registered campaign contains 365 plants; compile errors and crashes never count as kills. The review probe's `x-no-clock-refresh` and `x-signed-age` survivors remain equivalent within the documented dispatch and half-range clock contract, as recorded in R630-1. They are not registered campaign escapes.

## Window edge and wrap

The query returns current destination-valid AND (answered probe age below the configured interval OR registered Listener). SUCCESS and destination-allocation-failure answers record demand at accepted transport. Queued/refused sends and unrelated replies do not start freshness.

- `WithinWindowAndRefresh` checks ages 0 and 14999, includes 7 ms spent in send, and proves a later answer renews the window.
- `WindowEdge` checks age 15000 at starts 50000 and UINT32_MAX-999. A Listener can hide expiry; withdrawal exposes it immediately.
- `StaleProbe` checks age 15001 at both starts and prevents revival after observed expiry and a later wrap.
- Starting at UINT32_MAX-999 gives clock 13999 at age 14999, 14000 at age 15000 and 14001 at age 15001. `ClockWrap` also checks freshness before rollover, catching an overflowing absolute deadline.
- `ConfiguredWindow` sets 30000 ms and checks age 20000. YAML still requires 15000 ms.
- A response deferred for 20000 ms begins freshness only after successful retry, including 9 ms spent inside send.
- Zero is disabled even at age 0. The boundary test accepts 2^31-1 and refuses 2^31 and UINT32_MAX. Regular queries and the existing less-than-half-range service obligation still apply.
- RV32 executes the generated positive path at age 1 ms. Individual edge, wrap and negative-term evidence is hosted, not claimed for that narrowed smoke check.

## Gates

Final `validate.py --jobs 16 --graphs` returns 0, all 28 entries below return 0, and `baremetal.py --jobs 16` returns 0 for Debug and Release. The post-commit privacy gate returns 0. ACMP coverage is 792/792 lines and 392/392 branches, with no new exclusions. The registered campaign reports 365 CAUGHT, zero ESCAPED and zero ERROR. All eight GCC and Clang sanitizer binaries pass. Source snapshot hashes for all 98 tracked files match the final commit.

`round2/validation/gates.json`, per-gate log/rc files, `round2/rv32/results.json`, `round2/mutation-summary.json` and `round2/final-audit.json` hold the final receipts. Earlier setup runs exposed a positional mutation-list assumption and a stale legacy plant anchor; both were corrected without changing their defects or weakening controls. The final full rerun supersedes them.

| Gate | Hosted Linux | Bare-metal RV32 / scope |
|---|---|---|
| `entity-golden` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `entity-controls` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `boundary` | rc 0 | Both configurations pass freestanding dependency/import/ABI and unresolved-symbol audits. |
| `needles` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `assertion-templates` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `dependencies` | rc 0 | RV32 uses its compiler intrinsic headers and minimal port; final links audited. |
| `comments` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `conditionals` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `port-contracts` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `acmp-cache` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `registration-controls` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `license` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `traceability` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `test-inventory` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `coverage-controls` | rc 0 | Hosted instrumentation/control only; no RV32 sanitizer, coverage or mutation denominator claimed. |
| `privacy-selftest` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `privacy` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| `gcc-configure` | rc 0 | Separate freestanding Debug and Release configure/build/link: rc 0. |
| `gcc-build` | rc 0 | Separate freestanding Debug and Release configure/build/link: rc 0. |
| `gcc-test` | rc 0 | Both QEMU smoke executions: rc 0, including the shared positive freshness path. |
| `coverage` | rc 0 | Hosted instrumentation/control only; no RV32 sanitizer, coverage or mutation denominator claimed. |
| `clang-sanitizers-configure` | rc 0 | Hosted instrumentation/control only; no RV32 sanitizer, coverage or mutation denominator claimed. |
| `clang-sanitizers-build` | rc 0 | Hosted instrumentation/control only; no RV32 sanitizer, coverage or mutation denominator claimed. |
| `clang-sanitizers-test` | rc 0 | Hosted instrumentation/control only; no RV32 sanitizer, coverage or mutation denominator claimed. |
| `mutation` | rc 0 | Hosted instrumentation/control only; no RV32 sanitizer, coverage or mutation denominator claimed. |
| `static-analysis` | rc 0 | Source analysis includes the minimal port and shared example; no RV32 runtime-analysis claim. |
| `mutation-controls` | rc 0 | Hosted instrumentation/control only; no RV32 sanitizer, coverage or mutation denominator claimed. |
| `graphs` | rc 0 | Repository source/contract check applies to both targets; RV32 shared check executes separately. |
| Aggregate validation | rc 0, 28/28 gates | `baremetal.py`: rc 0 for both configurations. |
| Post-commit privacy | rc 0 | History/source check applies to both targets. |
| Complete-suite removal control | rc 0; 17 plants, 418 → 417 test instances, eight binaries each | Portable positive path retained and executed. |

## Bare-metal image sizes

Loadable images are measured with `riscv64-elf-objcopy -O binary`, including alignment gaps and the whole core archive. Both configurations pass dependency/import/ABI/unresolved-symbol audits and QEMU smoke. Images stay in scratch; `round2/sizes.json` records SHA-256 and byte counts.

| Configuration | Main | Round 1 | Round 2 | Growth from main | This round |
|---|---:|---:|---:|---:|---:|
| Release | 35792 | 37096 | 36864 | 1072 | -232 |
| Debug | 45744 | 47952 | 47512 | 1768 | -440 |

Release has 976 bytes remaining under the 2048-byte ceiling. Debug is informational under the ruling. ELF file sizes are 46552 Release and 141644 Debug, both with no unresolved final symbols.

## References and limits

The read-only reference is `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`. `docs/design/MAILBOX_SPLIT.md:1065` and `docs/reference/MAILBOX_CONTRACT.md:255` identify the old address-only gate. No reference repository was changed. Its unpopulated processor gitlink is `2ad2f845dd583f8310075fa2380cb60a04fd091a`. The retained pinned `docs/architecture/05_acmp_engine.md` and `hdl/acmp/KL_acmp_talker.sv` describe the same term set and unsigned age strictly below the interval (`fresh_f` at line 396). The processor records received probes; this core uses accepted response sends. That transport distinction remains explicit.

Local Milan v1.2 clause 4.3.3.1 and IEEE 1722.1-2021 clauses 8.2.1.9–8.2.1.13 were consulted, with the repository verification, coding, porting, architecture and entity-generator documentation. No standards text is reproduced.

No hardware, bench, platform repository mutation, remote push or PR operation was performed. The manager owns evidence publication, push, two final positive reviews, integration-candidate validation and merge decisions. Portable Linux/RV32 evidence does not establish hardware timing or the final integration candidate.

## Reproduction and artifacts

Scratch: `$VALIDATION_STORAGE/tsn24-a606/round2/`. Output: `$MANAGEMENT/2026-09-23/tsn24-a606/`. The parent scratch `env.sh` selects GoogleTest/GMock 1.14.0, Clang 18.1.3 and retained compatible runtime/header launchers. No shared installation changed.

```sh
source $VALIDATION_STORAGE/tsn24-a606/env.sh
python3 scripts/validate.py --work $VALIDATION_STORAGE/tsn24-a606/round2/validation --jobs 16 --graphs
python3 scripts/baremetal.py --work $VALIDATION_STORAGE/tsn24-a606/round2/rv32 --jobs 16
python3 $VALIDATION_STORAGE/tsn24-a606/round2/review-scripts/escape_probe.py --tree $VALIDATION_STORAGE/tsn24-a606/round2/tree --work $VALIDATION_STORAGE/tsn24-a606/round2/escape --jobs 4
bash $VALIDATION_STORAGE/tsn24-a606/round2/physical.sh
python3 $VALIDATION_STORAGE/tsn24-a606/round2/complete_suite.py --work $VALIDATION_STORAGE/tsn24-a606/round2 --jobs 4
```

Builds and campaigns are never piped. Long jobs have separate log/rc files and are awaited. Independent repository builds use 16 jobs; review-script concurrency is bounded separately. Memory was sampled every five seconds in `round2/memory.csv`; kernel peak was 8341245952 bytes, below 9 GB. Output contains scripts and receipts only, with size/hash records replacing binaries, trees and installed dependencies.

[Round 2 REVIEW READY comment](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6128015351) posted with head `0868387deab21bd0db414424f306c7ea62498e29`. The manager owns the push and final review.

## Round 3

Starting head, confirmed with `git rev-parse HEAD`: `0868387deab21bd0db414424f306c7ea62498e29`. Main resolves to `1ba273540abbdf51ea5d235c0a7e81c0bcb5d475`. Branch remains `acmp-da-fresh`; new commits only.

Authorities: [Round 3 assignment](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6128504411), [R630-2 negative review](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6128429366), and [R631-2 positive review](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6128499323), all read in full along with the issue and original assignment. The sole required finding is R630-2-F1: test expiry while a Listener or invalid destination hides probe demand. Production code already handles both paths correctly.

| File:line | Round 3 change |
|---|---|
| `tests/test_acmp.cpp:2301` | Add `AcmpFresh.StaleProbeAfterListenerWrap`: retain Listener registration across serviced clock wrap, then withdraw it and require the stale probe to remain closed. |
| `tests/test_acmp.cpp:2318` | Add `AcmpFresh.StaleProbeAfterInvalidAddressWrap`: keep the destination invalid across serviced wrap, restore validity and require the stale probe to remain closed. |
| `tests/mutations.json:5556` | Register `g-expiry-skipped-with-listener` with the first test's unique assertion. |
| `tests/mutations.json:5568` | Register `g-expiry-skipped-invalid-da` with the second test's unique assertion. |
| `docs/TESTS.md:103` | Regenerate both named test/plant links and shifted source anchors. |
| `docs/TRACEABILITY.md:25` | Regenerate ACMP-11 links and shifted source anchors. |
| `docs/VERIFICATION.md:24` | Update the campaign count to 363 core plus four generated configuration plants. |

Both tests answer one probe at clock 50000, then query at elapsed milliseconds 15000, 1000000000, 2000000000, 3000000000, 4000000000 and 4294967396 (`2^32 + 100`). The maximum query gap is 1000000000 ms, strictly below 2147483648. The final wrapped clock is 50100, which aliases a fresh age of 100 ms. No new answer arrives. After the hiding condition is removed, the final query must return false. The exact-edge query also preserves the existing equality-only plant's sole `StaleProbe` killer. Existing before-wrap/after-wrap age-14999, age-15000 and age-15001 tests remain unchanged.

| Test | Plant | Complete suite | Only named test physically removed |
|---|---|---|---|
| `AcmpFresh.StaleProbeAfterListenerWrap` | `g-expiry-skipped-with-listener` | 420 completed instances in eight binaries; only this test fails with its named needle; expected rc 8 | 419 completed instances in eight binaries, no failures/skips; rc 0; `escapes: true` |
| `AcmpFresh.StaleProbeAfterInvalidAddressWrap` | `g-expiry-skipped-invalid-da` | 420 completed instances in eight binaries; only this test fails with its named needle; expected rc 8 | 419 completed instances in eight binaries, no failures/skips; rc 0; `escapes: true` |

`gap_mutants.py` and `physical_removal.py` ran unchanged. The gap script reports CAUGHT for all six controls, including both new plants. A supplementary complete-suite checker verifies the two exact source substitutions and every remaining file, physical deletion of precisely one test, fresh XML from all eight binaries, complete registration and no skips. Its driver returns 0. The five original acceptance-term plants retain named catches and all-binary filtered escapes at this candidate. Earlier Round 2 physical-removal receipts above remain historical; this round's physical-removal claim covers the two new tests.

The unchanged `wrap_alias_demo.c` was compiled and executed with address and undefined-behavior sanitizers. The unplanted core closes both gates (rc 0); each exact plant reopens only its affected gate at `2^32 + 100` ms (expected rc 1). The grading driver returns 0, and no sanitizer diagnostic occurs.

The supplied evidence branch does not resolve in tsn-c-stack. The exact scripts are available read-only in [milan-fpga at evidence commit 65b32c38047cfafa92f0c870829cb74b49ee6047](https://github.com/kebag-logic/milan-fpga/tree/65b32c38047cfafa92f0c870829cb74b49ee6047/review-evidence/tsn24-r1/reviews/R630-2/scripts). Git blob hashes were checked when fetched; `round3/review-scripts/identities.json` records the verified identities. No reference repository was changed.

| RV32 configuration | Main loadable bytes | Round 2 bytes | Round 3 bytes | Growth from main | Round 3 delta |
|---|---:|---:|---:|---:|---:|
| Release | 35792 | 36864 | 36864 | 1072 | 0 |
| Debug | 45744 | 47512 | 47512 | 1768 | 0 |

Both new loadable images match the Round 2 SHA-256 byte for byte, including alignment. Baseline and Round 2 retained ELFs were remeasured; Round 3 ELFs were freshly built. `round3/sizes.json` records every size and digest; binaries stay in scratch. Both freestanding configurations pass dependency/import/ABI checks, whole-core linking, no unresolved final symbols and QEMU smoke. Individual wrap-alias assertions execute in the hosted suite; the unchanged RV32 smoke retains the generated positive freshness path.

Final head: `1edff3180c2ff435b855cc770fb8be371f2096b3`. The source snapshot matches all 98 tracked files in this commit; the only five changed files are the two test files and three documentation records listed above. No production code or port changed this round. Post-commit privacy returns 0. Scratch is `$VALIDATION_STORAGE/tsn24-a606/round3/`; the output `round3/` holds only receipts and portable scripts under the size limit.

### Round 3 gates and limits

Every command ran directly without a pipe. Long-running jobs used detached sessions with individual logs, pid files and return-code files; all jobs completed before handoff. Independent repository builds and campaigns used 16 jobs; supplied review scripts retained their own two-job inner builds with bounded outer concurrency. Sampled and kernel memory peak was 5684236288 bytes, below 9 GB.

| Gate | Linux hosted | Bare-metal RV32 / scope |
|---|---|---|
| `entity-golden` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `entity-controls` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `boundary` | rc 0 | Debug and Release dependencies, allowed imports, ELF ABI and unresolved-symbol checks: rc 0. |
| `needles` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `assertion-templates` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `dependencies` | rc 0 | RV32 uses the minimal port and compiler intrinsic headers; final links audited. |
| `comments` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `conditionals` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `port-contracts` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `acmp-cache` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `registration-controls` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `license` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `traceability` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `test-inventory` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `coverage-controls` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `privacy-selftest` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `privacy` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| `gcc-configure` | rc 0 | Separate Debug and Release freestanding configure/build/whole-core link: rc 0. |
| `gcc-build` | rc 0 | Separate Debug and Release freestanding configure/build/whole-core link: rc 0. |
| `gcc-test` | rc 0 | Debug and Release QEMU smoke: rc 0; generated positive freshness path retained. |
| `coverage` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `clang-sanitizers-configure` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `clang-sanitizers-build` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `clang-sanitizers-test` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `mutation` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `static-analysis` | rc 0 | Source analysis includes the minimal port; no runtime-analysis claim. |
| `mutation-controls` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `graphs` | rc 0 | Shared source/metadata contract applies to both targets; RV32 execution is separate. |
| Aggregate | `validate.py`: rc 0, 28/28 entries | `baremetal.py`: rc 0; both configurations rc 0. |
| Post-commit privacy | rc 0 | Source and history gate applies to both targets. |
| Supplied gap and physical-removal scripts | Both drivers rc 0; two requested plants CAUGHT and `escapes: true` | Hosted control evidence. |
| Complete-suite XML grading | rc 0; two plants, each 420 to 419 completed instances in eight binaries | Hosted control evidence. |
| Original acceptance-term sensitivity | rc 0; five named catches and all-binary filtered escapes | Earlier physical-removal receipts retained as historical. |
| Sanitized wrap harness grading | rc 0; baseline pass and both expected mutant failures | Hosted harness; no board timing claim. |

Coverage remains 792/792 ACMP lines and 392/392 branches; all ratchets meet 100% after the pre-existing exclusions. No new exclusions. The complete registered campaign reports 367 CAUGHT, zero ESCAPED, zero ERROR. Traceability records 45 requirements, 146 declarations and 420 executable instances. The unchanged production images remain below the Release-only 2048-byte ceiling.

Reproduce the repository checks with the pinned dependencies:

```sh
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
```

The portable review commands, from a workspace containing the exported source as `tree` and the verified scripts as `review-scripts`, are:

```sh
cmake -S tree -B registration -DCMAKE_BUILD_TYPE=Debug
cmake --build registration -j16
python3 review-scripts/gap_mutants.py --tree tree --work gap --jobs 4
python3 review-scripts/physical_removal.py --tree tree --work physical --plants g-expiry-skipped-with-listener,g-expiry-skipped-invalid-da
python3 complete_suite.py --work .
python3 wrap_controls.py --work .
```

`round3/validation/gates.json`, gate logs/return codes, mutation XML and `round3/mutation-summary.json` hold full-run evidence. `round3/complete-suite/` holds fresh full/removed XML and registration counts. `round3/rv32/results.json` and `round3/sizes.json` establish target builds and sizes. `round3/final-audit.json` and `round3/source-snapshot.json` tie execution to the committed bytes. Large artifacts have size/SHA-256 records in `round3/large-artifacts.json`; no binary, installed dependency or tree export is in this output directory. Root receipts predate Round 2; `round2/` and `round3/` explicitly separate the later executions. `CANDIDATE.patch` now contains the complete lane diff at the final head.

No hardware or bench access occurred. The read-only reference and processor files were consulted only; no RTL simulation or platform bank was run in Round 3. The manager owns publication, push, PR updates, final reviews, integration-candidate validation and merge. [Round 3 REVIEW READY comment](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6128674512) posted with the final head. The manager owns the push.

Artifact indexes are split into files below 200 KB. The root checksum manifest covers top-level files and the two round manifests; each round manifest covers its own receipts.

## Round 4

Final head: `f13c9c16c2b300d158f980dd7c7f071dcb84df5b`; tree `591d38854105564a5d632c18e846b0dd60c2f148`. Starting head and main were resolved with `git rev-parse`. All 98 tracked file bytes match the tested source snapshot and final tree. Exactly five files changed this round; production code, generator, headers, platform repository and target smoke are unchanged.

Authorities read in full: [Round 4 assignment](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6129059074), [R630-3 negative review](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6129031218), [R631-3 positive review](https://github.com/kebag-logic/tsn-c-stack/pull/25#issuecomment-6129053139), the issue body and original assignment. The requirement is to close the documented behavior class by enumerating every added port-contract sentence and both ACMP-11 sentences, then proving individual test necessity across the complete suite. No row demonstrated a production defect, so the STOP condition did not apply.

### Changes and source anchors

| File:line | Change |
|---|---|
| `tests/test_acmp.cpp:2372` | Valid interface 1 is refused for source 0 (configured interface 0), and the gate remains false. |
| `tests/test_acmp.cpp:2380` | A probe remains fresh after Listener registration and withdrawal at age 100 ms. |
| `tests/test_acmp.cpp:2390` | A still-registered Listener is present immediately before initialization and cannot open the gate afterwards. |
| `tests/test_acmp.cpp:2400` | Repeated declaration queries use the existing clock/source ports only, with no timer, SRP or publication effects. |
| `tests/test_acmp.cpp:2364` | The no-probe Listener test now explicitly uses Asking Failed. |
| `tests/test_acmp.cpp:2477` | Deferred acceptance retains its queue/refusal coverage; send-duration accounting belongs to the separate immediate-answer test, preserving its single-killer evidence. |
| `tests/test_acmp.cpp:2507` | Unknown-source replies do not sample the demand timestamp. |
| `tests/test_acmp.cpp:2529` | Accepted Listener register/withdraw calls join refused inputs in the no-port-call assertion. |
| `tests/test_acmp.cpp:2556` | Initialization clears the saved timestamp itself, in addition to the observable gate. |
| `tests/mutations.json:5519` | Narrow the older interface plant to out-of-range acceptance; valid-but-wrong interface has its own exact review plant. |
| `tests/mutations.json:5531` | Narrow the older reset plant to answer fields; Listener and timestamp-only retention have separate plants. |
| `tests/mutations.json:5580` | Add 21 registered plants, including all three exact requested review substitutions and adjacent documented guard/callback/reset behaviors. |
| `docs/VERIFICATION.md:215` | Add 31 sentence rows, with all 42 distinct registered plants and their killers; five caller/authority rows give explicit no-test reasons. |
| `docs/VERIFICATION.md:24` | Update inventory to 384 core plus four generated-configuration plants. |
| `docs/TESTS.md:103` | Regenerate test/plant links and changed line anchors. |
| `docs/TRACEABILITY.md:25` | Regenerate requirement links for 150 declarations and 424 executable instances. |

The extra timestamp plant initially sampled every send and also broke unrelated clock-budget checks. The first independent grade correctly failed; `round4/attempt1/` retains that receipt. Its replacement, `dafresh-answer-stamped-before-send` at `tests/mutations.json:5676`, moves only counted probe-response timing before send. The complete 42-plant check and all 28 repository gates were repeated after that correction. No assertion was removed; the unrelated pre-existing ACMP tests are unchanged. The supplied reviewer script and supplied gap list remain byte-for-byte unchanged.

### Per-test catch and removal evidence

The table below covers every distinct plant used by the sentence table, including all current freshness plants and two pre-existing response-field witnesses. Every row completes all eight binaries. With its killer present, 424 instances complete and only the named test fails on its registered message. After physically deleting just that test declaration, 423 instances complete with no failures, skips or disabled tests; all binary return codes are 0. The expected planted failing binary returns 1; the grading drivers return 0.

| Test | Registered plant | Full suite | Only its killer removed |
|---|---|---|---|
| `AcmpFresh.NoProbe` | `dafresh-unanswered-clock` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.ListenerWithoutProbe` | `dafresh-listener-needs-probe` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.InvalidAddress` | `dafresh-ignore-address` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.FreshProbeAfterListenerWithdrawal` | `r630-3-withdrawal-clears-probe` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.QueryPorts` | `dafresh-query-source-twice` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.QueryPorts` | `dafresh-query-calls-srp` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.InputGuardsAndReentry` | `dafresh-listener-calls-clock` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.InputGuardsAndReentry` | `r630-3-listener-bound-off-by-one` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.InputGuardsAndReentry` | `dafresh-wrong-interface` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.ListenerInterfaceMismatch` | `r630-3-listener-range-only` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.InputGuardsAndReentry` | `r630-3-listener-no-entry-guard` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.ListenerWithoutProbe` | `dafresh-listener-rejects-asking-failed` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `EntityYaml.DaFreshRoundTrip` | `dafresh-generated-window` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.ConfiguredWindow` | `dafresh-fixed-window` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.WindowRange` | `dafresh-half-range` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.WindowRange` | `dafresh-range-wipes-instance` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.WindowRange` | `dafresh-range-calls-clock` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.ZeroWindow` | `x-zero-never-expires` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.ZeroWindow` | `dafresh-zero-blocks-listener` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.ListenerWithdrawalAndReset` | `dafresh-reset-retains-demand` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.ListenerWithdrawalAndReset` | `dafresh-reset-retains-timestamp` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.InitClearsListener` | `r630-3-init-keeps-listener` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.SourceAndInterfaceIsolation` | `dafresh-wrong-source` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.SourceAndInterfaceIsolation` | `r630-3-listener-writes-source-zero` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.WithinWindowAndRefresh` | `dafresh-answer-stamped-before-send` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.DeferredAnswer` | `dafresh-refused-answer` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.OtherRepliesDoNotRefresh` | `dafresh-incompatible-refresh` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.FailedAllocationAnswer` | `dafresh-only-success` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.OtherRepliesDoNotRefresh` | `dafresh-state-reply-demand` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpCore.A20ProbeTxIsAnsweredFromTheSource` | `acmp-probe-tx-reports-asking-failed` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpCore.A20DisconnectGetTxStateAndGetTxConnection` | `acmp-get-tx-state-unheld-mac` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.WithinWindowAndRefresh` | `dafresh-no-renewal` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.WindowEdge` | `dafresh-inclusive-edge` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.StaleProbe` | `dafresh-expiry-equality` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.ClockWrap` | `dafresh-absolute-clock` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.QueryPorts` | `dafresh-query-clock-twice` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.StaleProbeAfterListenerWrap` | `g-expiry-skipped-with-listener` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.StaleProbeAfterInvalidAddressWrap` | `g-expiry-skipped-invalid-da` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.InputGuardsAndReentry` | `r630-3-declaring-no-entry-guard` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.InputGuardsAndReentry` | `r630-3-declaring-bound-off-by-one` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.QueryPorts` | `dafresh-query-calls-timer` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |
| `AcmpFresh.QueryPorts` | `dafresh-query-calls-publish` | CAUGHT, sole named failure; 424 instances | `escapes: true`; 423 instances; rc 0 |

`round4/contract-row-results.json` reconciles every sentence row with the registry. `round4/contract-receipts/` records each plant, killer, exact needle, counts and raw XML digests. `grade_contract.py` rejects missing binaries, stale/missing registrations, incomplete XML, skips, unrelated failures, wrong exit statuses and removal of anything other than the one executable instance. It also checks the table-derived substitutions against the committed registry. The unchanged full-suite runner performs the physical deletion and restores its worker source after each run.

The exact three R630-3 plants are each CAUGHT by their corresponding new test when `full_suite_probe.py` is run unchanged against the unchanged `plants_gap.json`. All 17 exploratory plants complete 424 instances; 16 are caught. The sole survivor is the review's unregistered, equivalent `r630-3-drop-send-clock-reread`: no prior clock read exists in that production response path. It is not part of the registered campaign. The requested three are also included in the 42-plant physical-removal campaign. `round4/grade-gap.log` and `round4/review-gap-summary.json` record this distinction.

### Window edges, wrapping clock and reset

At normal clock 50000 and at `UINT32_MAX - 999`, the tests cover fresh age 14999, the closed exact age 15000 and stale age 15001. Immediate acceptance is fresh at age zero; a later answer renews the full interval. A send advancing time by 7 ms is measured from send completion, and its before-send timestamp plant fails only `WithinWindowAndRefresh`.

Both masking tests retain one answer through elapsed milliseconds 15000, 1000000000, 2000000000, 3000000000, 4000000000 and 4294967396 (`2^32 + 100`). Every service gap is at most 1000000000, below 2^31. The final clock aliases age 100 ms, but withdrawing the Listener or restoring the address cannot resurrect the expired probe. Current-head catches and physical-removal escapes for both suppression plants are in the table above. The new fresh-withdrawal case covers the complementary age-100 path before expiry. Initialization is tested separately for the answer flag, timestamp and still-registered Listener level.

### Final gates on both targets

| Gate | Linux hosted | Bare-metal RV32 / scope |
|---|---|---|
| `entity-golden` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `entity-controls` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `boundary` | rc 0 | Debug and Release dependency/import/ABI and unresolved-symbol audits: rc 0. |
| `needles` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `assertion-templates` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `dependencies` | rc 0 | Minimal port and compiler intrinsic headers only; final links audited. |
| `comments` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `conditionals` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `port-contracts` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `acmp-cache` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `registration-controls` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `license` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `traceability` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `test-inventory` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `coverage-controls` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `privacy-selftest` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `privacy` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| `gcc-configure` | rc 0 | Separate freestanding Debug and Release configure/build/whole-core link: rc 0. |
| `gcc-build` | rc 0 | Separate freestanding Debug and Release configure/build/whole-core link: rc 0. |
| `gcc-test` | rc 0 | Debug and Release QEMU smoke: rc 0, including the generated positive freshness path. |
| `coverage` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `clang-sanitizers-configure` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `clang-sanitizers-build` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `clang-sanitizers-test` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `mutation` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `static-analysis` | rc 0 | Source analysis includes the minimal port; no runtime-analysis claim. |
| `mutation-controls` | rc 0 | Hosted measurement only; no RV32 coverage, sanitizer or mutation denominator claimed. |
| `graphs` | rc 0 | Shared source/metadata obligation applies to both targets; RV32 execution is separate. |
| Aggregate validation | rc 0, 28/28 entries | `baremetal.py`: rc 0; both configurations pass. |
| Contract row grading | rc 0; 31 rows, 42 plants, 424 to 423 instances | Hosted full-suite evidence; unchanged portable smoke executes on RV32. |
| Supplied gap replay and grading | rc 0; three requested exact plants CAUGHT | Hosted sensitivity evidence. |
| Post-commit privacy | rc 0 | Applies to shared source/history on both targets. |

The registered campaign reports 388 CAUGHT, zero ESCAPED, zero ERROR. ACMP coverage remains 792/792 lines and 392/392 branches. All existing ratchets pass, with no added exclusions. TESTS and TRACEABILITY are current.

### Bare-metal image sizes

| Configuration | Main bytes | Round 3 bytes | Round 4 bytes | Growth from main | Round 4 growth |
|---|---:|---:|---:|---:|---:|
| Release | 35792 | 36864 | 36864 | 1072 | 0 |
| Debug | 45744 | 47512 | 47512 | 1768 | 0 |

Loadable images are measured with `riscv64-elf-objcopy -O binary`, including alignment gaps and the whole core. Both Round 4 loadable images match Round 3 SHA-256 byte-for-byte. Release has 976 bytes of margin below the 2048-byte ceiling; Debug is informational under the existing ruling. `round4/sizes.json` records ELF and image sizes/digests. Binaries remain in scratch. `round4/target-source-equivalence.json` confirms the final plant-metadata correction changes no RV32 build input.

### Reproduction, artifacts and limits

Run repository gates with the pinned dependencies:

```sh
python3 scripts/validate.py --work build-validation --jobs 16 --graphs
python3 scripts/baremetal.py --work build-rv32 --jobs 16
```

From a copy of the portable Round 4 packet with the source checkout named `source`:

```sh
python3 review-scripts/full_suite_probe.py --repo source --work contract --plants plants_contract.json --jobs 4 --control --out contract-results.json
python3 grade_contract.py --repo source --work .
python3 review-scripts/full_suite_probe.py --repo source --work review-gap --plants review-scripts/plants_gap.json --jobs 2 --out review-gap-results.json
python3 grade_gap.py --repo source --work .
```

Scratch is `$VALIDATION_STORAGE/tsn24-a606/round4/`; the source-side pin environment remains the parent `env.sh`. Long commands ran in detached sessions with individual logs, pid files and return-code files, then were joined before handoff. Independent repository builds/campaigns use 16 jobs; unchanged review scripts use bounded outer concurrency. Sampled MemoryCurrent peaked at 5541359616 bytes; kernel memory peak was 6478204928 bytes, both below 9 GB. The monitor and every detached runner have ended.

The supplied evidence branch does not resolve in tsn-c-stack. The exact scripts live read-only at [milan-fpga evidence commit 81f2925defe6d9047145e7567c411095bf3630b3](https://github.com/kebag-logic/milan-fpga/tree/81f2925defe6d9047145e7567c411095bf3630b3/review-evidence/tsn24-r1/reviews/R630-3). Their Git blobs and SHA-256 values are verified in `round4/review-scripts/identities.json`. The script digest is `16e45c15ef375c991fc0cfbe4329dcbc515f1e469b2610c8ba164e1cd6c4f9b0`.

The read-only reference remains `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`, processor gitlink `2ad2f845dd583f8310075fa2380cb60a04fd091a`. MAILBOX_SPLIT:1065 and MAILBOX_CONTRACT:255 describe the old address-only gate. The retained processor documentation and RTL were checked against their pinned Git blobs; `fresh_f` uses unsigned age strictly below the configured interval and `lsn_reg_f` admits any non-IGNORE Listener. The fabric records command acceptance; the core records response-send acceptance, which can occur later under backpressure. Local Milan v1.2 clause 4.3.3.1 and IEEE 1722.1-2021 clauses 8.2.1.9–8.2.1.13 were consulted; no standards text is reproduced in this packet.

`round4/source-snapshot.json` and `round4/final-audit.json` bind the receipts to the committed source. `round4/validation/gates.json` and per-gate logs/return codes establish all 28 gates. `round4/mutation-summary.json` lists every registered plant result. Raw XML is retained per contract plant and gap replay. Oversized receipts have size/SHA-256 records in `round4/large-artifacts.json`; no tree export, binary, installed dependency or file over 200 KB is copied into the output. Split manifests keep every index below the limit. Historical failed exploratory grading is separate from the final all-zero gates.

No hardware, bench access, reference-repository write, push, PR operation or dev-linux change occurred. Hosted checks and RV32 smoke do not establish deployed timing. The manager owns evidence publication, branch push, PR updates, final independent reviews and integration acceptance. [Round 4 REVIEW READY](https://github.com/kebag-logic/tsn-c-stack/issues/24#issuecomment-6129381782) was posted as a new issue #24 comment with the final head.

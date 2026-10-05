[R501] POSITIVE - exact head d763fce6f3e48fa9c468aaa835653befb8382d06

Round R501-4, external independent review of issue #665 / PR #669, F1.
Tree: `554ad4cb05ffbf9d794813990a8dfb58ec44624d`.
Source base: `fa450d301805881ad713b67521477bf042ddadfd`.
Integrated and observed remote dev: `28f9666feab2b2ba287643c63ed3a16b1e0bb863`.

All five lenses are CLEAN. R501-3-F1 and R500-3-F1 are resolved under the [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5999350068). No new BLOCKER, MAJOR, MINOR or RESIDUE remains. Retained suggestions below remain optional.

The independent source verdict and ledger were recorded before reading prior public review findings (`receipts/independent-source-pass.txt`). This final verdict includes executable checks and reconciliation. No private author material, other checkout, source fix or GitHub write was used. Short source paths below are relative to `sw/firmware/ctrl_nvm/`; design pages are under `docs/design/`.

**Round-4 findings resolved**

**R501-3-F1: RESOLVED. Conformance, RTL, Robustness, Tests, Docs.** Artifacts: `nvm_store.c:141`, `:208`, `:228`; `test/nvm_checks_write.py:573`; `test/nvm_mutants.py:184`; `README.md:141`.

Every successful delivery passes through `nvm_take`, accumulating CRC-32 and byte count. A refusal or BLANK stands only when an earlier completed read has the same verdict, count and digest. The digest includes every delivered byte: the preliminary header, subsequent container, and all chunks/trailer/additional prefix reads on the oversized path. Failed deliveries do not become content evidence. Earlier observations remain available, so matching first and third reads establish agreement. No agreement after three attempts publishes UNREAD and leads to HELD. SEQ still comes only from a validated container.

The standing `read_disagreement` check passed on all five shapes: both slot orientations, SEQ 1/5/0x80000000/0xFFFFFFFF, header/body corruption, XOR 8/16/clean and XOR 8/16/32. Every case continues through changes, commits and clean reboots, comparing the complete saved payload. The verdict-only control fails on lost saved values as well as status assertions (`receipts/campaign/refusal_by_verdict.log`). Controls removing refusal confirmation or HELD also fail.

Independent disposable injection adds XOR 8/16/8. Across 1x1, 8x8 and the 83.333-MHz shape, all 144 cases pass: a clean third read restores the saved set; three differing reads hold the writer; matching first and third corrupt reads establish a stable content refusal. Production store, codec and port hashes match the reviewed source in every probe copy. Raw commands, output and results are in `receipts/edges/`.

**R500-3-F1: RESOLVED. Conformance, RTL, Robustness, Tests, Docs.** Artifacts: `plat/nvm_flash_litespi.c:75`, `:100`, `:248`; `test/nvm_bench.py:226`; `test/nvm_checks_write.py:350`, `:394`; `test/nvm_mutants.py:352`; the five configuration files; `README.md:70`, `:329`.

The whole-MHz assertion and constant clock stand-ins are gone. Whole seconds plus the fractional remainder convert accumulated clocks to integer microseconds without truncating clocks per microsecond. The 64-bit deadline calculation yields 166,666 clocks at 83,333,000 Hz and 200,000 at 100,000,000 Hz; `ls_late` compares that actual constant. Each generated header uses its configuration's frequency, checked against the builder argument. Host execution and the RV32 arm both consume it.

All 42 checks and RV32 builds passed on all five shapes. `port_clock` checked the deadline and 120 seconds of elapsed time; `time_base` crossed each frequency's wrap. The truncation control failed with 166,000 instead of 166,666 clocks and 120,481,469 microseconds counted during 120,000,023 microseconds of independent elapsed time. Its window/backoff assertions also fail (`receipts/campaign/ticks_per_us_truncated.log`).

The independent register driver in `probe_clock.c` bypasses the supplied timer model. Python integer arithmetic grades 32 samples, including fractional-microsecond boundaries, wrap-adjacent totals and a large accumulated epoch. All equal `ticks * 1000000 // frequency`. Six deadline probes check one tick below, exactly at and one tick above the threshold, with wrapping subtraction. All pass (`receipts/edges/clock.log`).

**HELD and bounded service**

Artifacts: `nvm_store.c:431`, `:773`, `:787`, `:804`; `nvm_store.h:109`; `README.md:200`.

Boot releases normal service before setting HELD. HELD service samples time, publishes status and returns without capture or media writes; changes raise `dirty`, and console commits are refused. Nine permanent-read-failure probes each complete 1,200,000 service calls over 120 seconds. Each reports `unread=3`, `read_faults=6`, `phase=10`, `dirty=1`, one release, zero erase/program operations and two refused commits. Clearing the fault halfway through does not silently resume persistence. There is no read storm or service deadlock, and status remains visible.

Reset followed by a clean boot is the supported recovery, exercised by the standing authority tests. An unproven entity model remains separately CLOSED. These are bounded-return port results, not proof that an unresponsive physical memory-mapped bus transaction returns or that a future status consumer presents HELD correctly.

**Reviewer-owned coverage ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Scope 5993775541, decisions 5997929153, assignment 5999350068; FASTCONNECT 4.2/6/7; MATERIALIZATION 8/15.1; `nvm_store.c:141`, `:208`, `:228`; `plat/nvm_flash_litespi.c:75`, `:248`; agreement and clock receipts | R501-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |
| RTL | CLEAN | No lane-owned HDL/gitlink delta against integrated dev (`receipts/integrity.log`); pinned `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:35`; `nvm_flash.h`, `nvm_state.h`, `nvm_shape.h`; store restore/write FSM, static storage and HELD; port widths, wrap and deadline | R501-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |
| Robustness | CLEAN | `test/nvm_checks.py` refusal/fallback/rollback/CLOSED; `test/nvm_checks_write.py` retries, cuts, disagreement and clocks; 144 independent agreement cases, nine persistent HELD runs and register boundaries in `receipts/edges/` | R501-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |
| Tests | CLEAN | `test/nvm_bench.py:183`, `:226`; `test/test_ctrl_nvm.py`; `test/nvm_mutants.py`; all five 42-check populations and 82 controls, including named killers for both round-4 defects (`receipts/campaign/`); independent probes | R501-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |
| Docs | CLEAN | `README.md` clock/agreement/HELD/size/timing claims; header contracts; FASTCONNECT 7 tie; docs-index entry; current PR body and public scope/evidence; reproduced sizes/timing; `receipts/gates/docs.log` | R501-4 | d763fce6f3e48fa9c468aaa835653befb8382d06 |

**Prior public findings**

All six prior public finding comments were read after the independent pass. There were zero submitted reviews and zero inline review comments. `receipts/public-state.json` identifies the comments and observed head. Earlier resolutions stand unless touched below; none regressed in the repeated check/control population.

| Finding | Disposition at this head | Evidence |
|---|---|---|
| R501-3-F1; retained R501-2-F1 | RESOLVED | Verdict/count/digest agreement, retry and HELD; saved-set reboot checks and verdict-only control, above |
| R500-3-F1 | RESOLVED | Exact conversion, configuration clocks, builds and boundary/truncation checks, above |
| R501-2-F2; R500-2-F2 | RESOLVED, maintained | Whole-call deadline; ten/twelve/all slowed waits; 250-us nominal and 2,213-us cumulative model assertions; actual maximum 2,189 us, 2,190 at 4x4; CPU estimate remains a floor |
| R501-2-F3 | RESOLVED, maintained | FASTCONNECT 7 cites A-on-tie decision; `newer_wins` and `tie_picks_b` |
| R500-2-F1 | RESOLVED, maintained | Binding restore before model proof/D3; unproven-model check retains bindings, closes D3 and releases nothing; controls caught |
| R500-2-F3 | RESOLVED, maintained | Fallback re-stage and exact capture-cursor checks; `fallback_restage_unchecked`, `taken_off_by_one` caught |
| R500-2-F4 | RESOLVED, maintained | `nvm_heal:521` after unchanged-projection suppression and verified promotion; recovery check and `dr2b_keeps_stale` |
| R500-2-S1 | RESOLVED, maintained | Both failed re-stages publish VD_LEN/UNREAD; `fallback_restage` |
| R501-1-F1 | RESOLVED, maintained | Validated RAM supplies SEQ; re-stage checks CRC/selected SEQ; flip/alias checks and controls |
| R501-1-F2; R500-1-F2 | RESOLVED, maintained | Changed bytes alone replenish attempts; console respects backoff/exhaustion; abandonment survives success; retry/bypass controls |
| R501-1-F3; R500-1-F1 | RESOLVED, strengthened | Local accumulated timer, PHC-step independence, configuration-correct wrap/conversion; time controls |
| R501-1-F4 | RESOLVED, maintained | TX/RX/drain waits release chip select and return faults; stalled/dead/progressing checks and controls |
| R500-1-F3 | RESOLVED, maintained | Current-capture changes leave no stale debounce window; later changes get their own; boundary controls |
| R500-1-F4 | RESOLVED, maintained | Separate binding/D3 rollback; binding/apply/settle failure checks and controls |
| R500-1-F5 | RESOLVED, maintained | Verify/blank-check tails, read failures, program refusal, tie and time retain detected controls |
| R500-1-F6 | RESOLVED, maintained | README distinguishes model time, counted bytes and unmeasured CPU time |
| R500-3-R1, RESIDUE | RESOLVED | `README.md:103` uses the requested distinction between immediate-readiness model behavior and healthy on-chip RX waiting |

**Retained optional findings**

- **R500-1-S1 - SUGGESTION - Tests.** Artifact: `.github/workflows/` and `test/test_ctrl_nvm.py`. The lane gate remains absent from hosted workflows. Impact: hosted green alone need not exercise it. Optional outcome: integrate a named gate; verify a lane defect makes it fail. Retained for the manager.
- **R500-3-S1 - SUGGESTION - Robustness, Docs.** Artifact: `nvm_store.c:460`, `README.md:206`, PR limitations. The permanent consequence is now documented: a slot unread on every boot keeps persistence held on every boot. That portion is resolved. The optional narrower-hold policy remains with the owner; decision 2 requires today's hold. Any policy change needs recorded authority and permanent-fault/commit/reboot tests.
- **R500-3-S2 - SUGGESTION - Robustness.** Artifact: `nvm_store.h:109`, `nvm_store.c:787`, FASTCONNECT 9.2. HELD with changes reports phase/unread/dirty rather than a failed-commit `stale` bit. No current contract is violated. At integration, define and test its mapping to public backing/stale flags before claiming durability.

**Executable evidence and scope**

`run_campaign.py` invokes the repository's grade functions for every shape/check and mutant, plus the same RV32 build arm, using joined workers. All 87 tasks returned 0; all 82 mutants failed every check each names. The native checks include 3,126 power-cut cases and recorded-vector round trips. Separate C/Python idiom, docs, capture-receipt and whitespace gates returned 0 (`receipts/gates/`). This is the full lane population, not the full parent or builder banks.

| Shape | Clock Hz | RV32 bss | RV32 text | Longest nominal / stalled call, model us |
|---|---:|---:|---:|---:|
| endstation_arty_current | 83,333,000 | 3,160 | 12,352 | 210 / 2,189 |
| endstation_arty_4x4 | 83,333,000 | 5,452 | 12,360 | 210 / 2,190 |
| endstation_arty_8ch | 83,333,000 | 8,012 | 12,360 | 210 / 2,189 |
| endstation_ax7101_1x1_tdm8 | 100,000,000 | 4,048 | 12,368 | 210 / 2,189 |
| endstation_ax7101_8x8 | 100,000,000 | 14,408 | 12,372 | 210 / 2,189 |

The base-to-head diff includes integrated dev changes. Tree comparison proves every path outside this module and two documentation entries equals integrated dev. Round 4 adds three commits on `9412006b`. The shipping writer remains blob `1cebba0b3e4102e7d02516e5ba3b18a67bdc0c06` at source base, dev and head. Its unchanged 24.5-ms receipt passes; it is not a CPU-time measurement for this store.

The specified public evidence at `38e93660c8e2d4c190a00e8538611de01fece598`, `review-evidence/665f1-r1`, is round-1 source evidence at `215c3c0b`. Examined public handoff, cut table and receipts match their published hashes (`receipts/public-evidence/examined.json`). The builder receipt has one NOT RUN arm. Current round-4 validation is separately reported by public comment 6000120843 and the manager's assignment. This review adds the exact-head executions above; the old bundle is not round-4 or merge-candidate evidence.

**Real limits and manager duties**

- Physical calibration NOT RUN; field skips are not hardware proof. No real power cuts, CPU execution, physical flash reliability, placement/timing or physical bus-stall containment was measured.
- Count/digest agreement is the assigned CRC-32 rule, not collision-free byte equality. Identically repeated silent corruption and CRC collisions remain documented limits.
- No shipping image links this store. State-owner adapters, mailbox/time integration, actual SET judges, restore clipping and public status consumers remain integration work. The time port requires exclusive timer ownership and sampling before wrap.
- No full parent/processor/gPTP/synthesis/builder banks, containers, replica runner, shared installs, privilege or hardware actions were used. Hosted contexts were not used for the source verdict. The manager owns hosted/replica acceptance and must distinguish executed jobs from skipped contexts.
- The manager must publish/reconcile both independent reviews, retain optional integration items, validate the final candidate against then-current dev, obtain merge authorization and perform post-merge containment. The shipping writer's VD_REC/VD_LEN gap and #671 remain separate work. Issue #665 retains its other lanes.

**Integrity and reproduction**

`receipts/integrity.log` and `.rc` prove exact tracked bytes, modes and index: 1,039 superproject blobs and required submodules with 558 / 104 / 214 blobs respectively:

- protocol-processor: `ead8036035affd53ef4b29979190f2f4f67084c0`;
- gptp-processor: `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`;
- third_party/verilog-axis: `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

The optional external gitlink is unchanged and unused. No tracked source needed restoration. Initial inspection import caches were removed; final status is clean. Disposable builds and probe trees are under packet `scratch/`, excluded from publication. Every worker finished. An initial reviewer-script import-name error was corrected before the successful probe run; it was not a product failure.

From the packet, with an exact checkout and normal build prerequisites:

```sh
python3 -B run_campaign.py /path/to/checkout --jobs 8
python3 -B run_edges.py /path/to/checkout --jobs 6
python3 -B run_gates.py /path/to/checkout --jobs 4
python3 -B verify_integrity.py /path/to/checkout
sha256sum -c MANIFEST.sha256
```

Run foreground coordinators to completion; keep any overlap below 16 workers. Receipts retain individual return codes. `MANIFEST.sha256` is the publication allowlist, using packet-relative paths; it includes this report. Scratch is never published.

R501-4 FINISHED

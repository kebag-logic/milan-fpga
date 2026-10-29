[R734] NEGATIVE - exact head 99de3a023abfda5604a70832e23baf7ff73481a3

Whole-PR external independent review of #811 / #665, round R734-1. One MAJOR validation defect remains: the split boot driver accepts a failed native simulation. All five lenses were applied. RTL and Docs are clean; Conformance, Robustness and Tests remain unclean for R734-1-F1. Wording residue below does not determine this verdict.

Scope and authority

Reviewed tree `715917bbb3c732168a35124b1571a3d2f8401580`, the complete 45-file delta from `f4c9ad4f06f185378fd2646298aab51dd108e86f`, and its history. Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue and public decisions, REQUIREMENTS.md and linked interface/design authorities, then implementation and executable evidence. Boot readiness was checked against Milan v1.2 5.6.1 itself, not inferred from the implementation.

The frozen acceptance is [the scope decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6493622258), read with [D0/D3/D4/D6](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409738976) and [the four later scope rulings](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6505997821). `public-scope.txt` and `pr-body-reviewed.txt` preserve the public text examined. The target branch is `dev-soft-core`; this report does not validate a later merge candidate.

The independent verdict and lens ledger were written before inspecting prior review findings. The subsequent PR timeline contained the two public review-start comments; the reviews and review-thread collections were empty. There were no prior public findings on this PR to retain or resolve. No other review report was used.

R734-1-F1 — MAJOR — Conformance, Robustness, Tests

Artifact: `tb/verilator/ctrl_split_boot/run.py:268` through the return at line 271; `grade()` at line 198; native failure handling in `tb/verilator/ctrl_split_boot/sim_main.cpp:249`.

Authority/evidence: #665's frozen acceptance requires a successful executable split boot and console smoke check. AGENTS.md section 6 requires failure-path review and tests capable of detecting their claimed defects. The native harness records boundary failures and returns its checker's failure status. The Python driver prints that status, discards it, then grades only the earlier READY/CSR/UART observations. `grade()` also ignores the native failed tally. Regrading has no saved native-process status to check.

`probe_boot_exit.py` exercises the unchanged `point()`, subprocess invocation, `grade()` and `main()`. It replaces only the expensive build provider with a controlled executable, obtains expected CSR writes from the real baremetal oracle, and supplies valid protocol observations. The positive executable exits 0 and both normal/regrade paths return 0. With the same observations followed by `FAIL: simulation exceeded its time limit`, a failed native tally and `RESULT: FAIL`, the executable exits 1, while both normal and regrade paths still return 0. `boot-exit.log` records `COMMAND Vsim exited 1` followed by `ctrl_split_boot: PASS`; `boot-exit.rc` is 1 because the reviewer probe reproduced the defect.

Impact: a native failure after otherwise acceptable observations can produce successful boot evidence. A failing completion, exception or process failure is not discharged by successful earlier UART and CSR observations. This is a gate-behavior defect, not a wording objection and not a claim that the published positive simulations actually failed.

Required outcome: native unsuccessful execution must invalidate the normal gate, and saved evidence must allow regrade to reject unsuccessful or incomplete native execution. Preserve the existing observation checks and accepted grader differences.

Verification: retain a passing native control; add controls with valid earlier observations followed by a nonzero process result and a failed/incomplete native completion. Both normal execution and regrade must reject them. Rerun the two positive boot points and both existing boot plants after the correction, then independently re-review this finding at the corrected head.

R734-1-R1 — RESIDUE — Docs

Artifacts: new source comments/docstrings listed in `comment-residue.txt`, especially `sw/firmware/ctrl/plat/ctrl_plat_console.h:8`, `sw/firmware/ctrl/test/plat_mutants.py:12`, `sw/litex/ctrl_memory_ledger.py:7`, `sw/litex/ctrl_memory.py:210`, and `tb/verilator/ctrl_split_boot/boot_soc.py:3`.

Authority/evidence: the owner's 2026-10-15 source-comment rule requires behavior/reason with issue and requirement IDs, without lane labels or issue-comment IDs. New comments contain `#665 S3`, `S3's`, `S2's`, `lane S14`, and numbered public-comment references. This finding is confined to comments/docstrings, not executable strings, test names, measurements, or generated artifacts. Functional identifiers such as `F1` and named test cases are not independently classified as lane residue here.

Impact: comment-policy residue; no behavioral change and no unclean lens.

Exact fix: in the listed new comments/docstrings replace `#665 S3` with `#665`; `S3's` with `the platform's`; `S3: skipped, reordered, wrong` with `skipped, reordered, wrong`; `the measurement S3 owes` with `the platform measurement`; `S2's test-only split SoC` with `the CPU budget harness's test-only split SoC`; `#665, issuecomment-6409738976` with `#665, decision D6`. In `ctrl_memory.py:210`, replace `lane S14` with `hybrid XIP work (#665 decision D3)`. In the ledger module docstring, replace the parenthesized numbered rulings with `under #665's documented memory exceptions`, retaining the two image names and the 57.5/59.0 figures. Leave pre-existing instances to #746.

Verification: inspect only added/changed source comments against the owner rule; no code or numerical evidence changes are needed.

R734-1-R2 — RESIDUE — Docs

Artifact: `tb/verilator/ctrl_split_boot/README.md:96`.

Authority/evidence: the same document reports a 40.209 ms status span for 8x8 at CPU 50 MHz / bus 100 MHz. Its sentence describing approximately 26.5 ms of 115,200-baud serialization ends with the unnecessary comparison `longer than any span here`.

Impact: inaccurate comparative prose, with all underlying measured figures retained. No test, verdict, clock assumption, or clause claim is changed by the fix.

Exact fix: delete `, longer than any span here` and retain the sentence's final period and the preceding figures. Verification: compare that sentence with the existing timing table. This residue does not dirty Docs.

Applied lenses and evidence

Conformance — applied; unclean only for F1. `sw/firmware/ctrl/plat/ctrl_plat.c:226`, `ctrl_plat_main.c`, `ctrl_plat_csr.c`, `ctrl_plat_gen.py`, and `sw/firmware/ctrl/app/ctrl_app.c` implement identity, generated static policy, MAAP's single-owner invalid report, AEM CRC/image, composition, saved state, held mailbox, SRP, AECP release, then ADP. The saved-state terminal and face acceptance precede opening AECP; ADP remains held until that release. This meets Milan 5.6.1's AECP/binding readiness before announcement within the reviewed composition. Refusal leaves a console-only loop. The held-open change is also propagated into the existing composition and budget harness.

`plat_trace.py` compiles and executes the actual `milan_baremetal.c` configure_fabric source. Independently rerun equality succeeded for all five shipped configurations: endstation_arty_4x4, endstation_arty_8ch, endstation_arty_current, endstation_ax7101_1x1_tdm8, and endstation_ax7101_8x8. Each produced the same 15 writes in order. The three skipped/reordered/wrong-word plants failed as intended. Generated policy comes from boot_policy; the address map comes from the supplied SoC csr.csv, with missing-map and incompatible-UART refusals. No hand-maintained policy replacement was found. The boot trace compares the first 18 writes (15 policy plus three MAAP owner writes); its 21 total pre-ready writes include the later repeated invalid report and are not a claim of only 18 total writes.

[R734] PASS RTL — `sw/firmware/ctrl/app/ctrl_app.c`, `sw/firmware/ctrl/plat/ctrl_plat_mmio.c`, `tb/verilator/ctrl_split_boot/boot_soc.py`, `sw/litex/ctrl_memory.py`, and the complete delta in `changed-files.txt` — held-open integration, volatile aligned CSR accesses, boot/reset composition, model clock selection and exact image budgeting checked against the split architecture and mailbox contracts. No RTL, CDC primitive, product clock, or submodule gitlink changed. The simulation's stand-in CSR/face behavior is explicitly narrower than datapath integration evidence.

The memory exception matches the ruling at only platform 8x8/two interfaces. Its identifying symbols are nvm_stage=13264 and ctrl_plat=21240; the size fixture retains its distinct image_allocation=16 identification and 57.5 exception. Independent `test_ctrl_memory.py` passed, including 47 mutants and six planted ledgers; widening the platform entry to 59.5 is caught. Published exact-head image receipts match section 5 of `docs/design/SPLIT_CONTROL_MEMORY.md`:

| Image | 1x1/1if | 1x1/2if | 8x8/1if | 8x8/2if |
|---|---:|---:|---:|---:|
| Platform, RAMB36 planned | 39.0 | 42.0 | 52.0 | 59.0, named exception |
| Size fixture, RAMB36 planned | 37.0 | 40.5 | 50.5 | 57.5, prior named exception |

All other points are within 56. These are allocations from linked images, not placed-and-routed utilization measurements. The reviewed image parts and five largest BSS objects agree with the ledger documentation; the published six misuse attempts refuse the exceptions on the wrong image/point or without authorization.

Robustness — applied; unclean for F1. `ctrl_plat_console.c`, `ctrl_plat_csr.c`, `test_plat.cpp`, `test_plat_boot.cpp`, and `test_plat_mmio.cpp` cover bounded RX/TX, FIFO backpressure, command overflow/recovery, invalid identity/CRC/boot state, refusal, and one/two-interface composition. The console handles at most 16 RX bytes, one command, and 16 TX bytes per pass, reserves 320 bytes in its 512-byte output ring, and does not write a full FIFO. Time reads have three high/low/high attempts, and bounded console spinning has a fixed 128-pass cap. The successful host tests and platform mutants corroborate those bounds. They do not establish worst-case admitted-load CPU service time.

Published boot timings below all use the product split CPU at **50 MHz (milan)** and bus at **100 MHz**. The bus counter is converted with sys_hz, and the CPU-cycle report uses cpu_hz; the bus clock is not presented as the CPU clock.

| Point | Ready ms / CPU cycles at 50 MHz | Status span / first byte / max gap, ms | Worst gettime span / first byte / max gap, ms |
|---|---|---|---|
| 1x1/1if | 84.389 / 4,219,428 | 21.632 / 1.963 / 1.273 | 2.536 / 1.236 / 1.275 |
| 8x8/1if | 184.610 / 9,230,494 | 40.209 / 2.853 / 2.204 | 4.047 / 2.125 / 1.858 |

Against #397 and FR_NFR section 3.4, these quiet-model results are below the 20-second boot bound, the 500-ms heartbeat interval, and the 10-ms service bound for first-byte/inter-byte gaps. A complete multi-pass response need not fit one service pass. The simulated UART has no baud serialization. These results do not prove under-load protocol timing, physical UART timing, or hardware conformance. The console-stall plant crosses 500 ms at the same CPU 50 MHz / bus 100 MHz and is caught. CPU-budget misses are separately disclosed in the PR and remain owned by S2b; no changed product CPU clock is used to excuse them.

Tests — applied; unclean for F1. Independently ran the platform CSR/console, MMIO and boot suites; all 37 platform mutants; all five CSR trace points and three plants; the platform RV32 compile arm; and the memory suite including its 47 mutants/six planted ledgers. `platform.rc`, `mutants.rc`, `trace.rc`, `rv32.rc`, and `memory.rc` are all 0. Independent campaigns were executed concurrently through a foreground driver, at no more than 16 build jobs, with their separate logs retained. No full forbidden bank was run.

Focused coverage independently reproduces 100% of the declared covered population: ctrl_plat 130/130 lines and 42/42 arcs after exclusions, console 118/118 and 66/66, CSR 52/52 and 6/6, MMIO 5/5 and no arcs. Raw ctrl_plat is 130/132 lines and 42/48 arcs. The two lines/six arcs excluded under `sw/firmware/gtest/README.md:321` are unreachable fixed-composition refusal paths; their reasons were checked against the actual capacity and module contracts. No exclusion or ratchet finding was emitted. The fifth platform file in the published full coverage receipt is the existing mailbox MMIO implementation (10/10 lines). `ctrl_plat_main.c` is not in that host coverage population; it is exercised by the published boot simulation. Thus “100%” means this declared population after stated exclusions, not every line of all platform sources without qualification.

The published positive boot runs and both boot plants were inspected, not rebuilt by this reviewer. They report successful native execution; F1 does not retrospectively assert that those runs failed. The additional controlled-process probe demonstrates the gap their two existing plants do not test.

[R734] PASS Docs — `docs/design/SPLIT_CONTROL_MEMORY.md` section 5, `sw/firmware/ctrl/plat/README.md`, `tb/verilator/ctrl_split_boot/README.md`, `sw/firmware/gtest/README.md:321`, and `pr-body-reviewed.txt` — scope, memory exceptions, coverage exclusions, simulation limitations and public evidence reconciled with the frozen decisions. The PR body explicitly states all four accepted limit groups: split grader work owed to S12; live SRP source configuration deferred until S2b's adapter changes, with Talker Failed meanwhile; split boot retained as a recipe until #784 step 2; and deferred asking-failed, GET_AS_PATH, saved-state flash addresses and real face acknowledgement. These are visible limits, not concealed implementation gaps. R1/R2 are wording residue only.

Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | ctrl_plat.c boot, ctrl_app.c hold/release, ctrl_plat_gen.py, plat_trace.py, run.py; F1 | R734-1 | 99de3a023abfda5604a70832e23baf7ff73481a3 |
| RTL | CLEAN | ctrl_app.c, ctrl_plat_mmio.c, boot_soc.py, ctrl_memory.py, full changed-files.txt | R734-1 | 99de3a023abfda5604a70832e23baf7ff73481a3 |
| Robustness | UNCLEAN | console/CSR bounds, boot refusal and MMIO suites, native failure propagation; F1 | R734-1 | 99de3a023abfda5604a70832e23baf7ff73481a3 |
| Tests | UNCLEAN | platform suites, 37 mutants, trace plants, memory plants, coverage and boot driver; F1 | R734-1 | 99de3a023abfda5604a70832e23baf7ff73481a3 |
| Docs | CLEAN | memory/platform/boot/coverage documentation, frozen scope, public PR body and receipts | R734-1 | 99de3a023abfda5604a70832e23baf7ff73481a3 |

Evidence provenance, reproduction and remaining duties

Published source evidence was read at [commit 608e2f22](https://github.com/kebag-logic/milan-fpga/tree/608e2f2223781e7ab46cc1f2ad16c8a6563b29fa/review-evidence/665s3-r1), covering the author-r0, author-r1 and author receipt sets. All 434 extracted published receipt hashes matched MANIFEST.json (`evidence-check.log`). Only receipt material was extracted; no other review report was consumed. `evidence-inventory.txt` identifies the inspected evidence locations.

Exact-head source receipts under `author/receipts/gates-at-99de3a02/` include the builder, firmware four shards, memory tests, both image kinds at all four points, six exception refusals, boundary without native simulation, and documentation gates. Earlier receipts under `author-r1/receipts/gates-at-5edbba1d/` cover full firmware coverage, saved-state tests/109 plants, MAAP differential, native boundary, boot points and CPU-budget comparison; the retained boot self-test is under `kept-from-a697-at-5edbba1d/`. The subsequent diff changes docs, memory planning/tests and image-help wording, not those retained execution inputs. This is inherited author evidence, not an execution of those banks at 99de3a02 by the manager or this reviewer.

The builder's physical calibration is NOT RUN. Field skips and simulation stand-ins provide no hardware proof. No manager source bank exists at this exact head, and none is claimed. Hosted/act acceptance remains manager-owned; this review does not infer executed jobs from green or skipped contexts.

Portable review scripts run from the exact-head repository root. Set MILAN_RV32_CC to the existing supported compiler and supply the existing host test library through CPLUS_INCLUDE_PATH/LIBRARY_PATH. Run `python3 -B <packet>/focused.py`, then `python3 -B <packet>/collect_coverage.py`. Run `sw/litex/test_ctrl_memory.py` with the existing project Python environment and TMPDIR=<packet>/scratch. Run `python3 -B <packet>/probe_boot_exit.py` for F1 (current expected rc 1 means reproduced), and `python3 -B <packet>/verify_checkout.py` for source integrity. All disposable outputs remain in packet/scratch. The pinned simulator identity was verified as 5.050, revision v5.050; no new native boot build is claimed.

`checkout-integrity.log` verifies raw tracked blob bytes, executable/symlink modes, exact stage-zero index, HEAD/tree and all required submodule gitlinks, not merely a clean status. The checkout is clean and no source fix was made. Required links include gptp-processor 55680bff3b287b9a7b0c759f51471fa617c17335, protocol-processor ed2118035e4cec76fb1b59cfbf8a053aeacc8af8, lwSRP 08ee86e812a0eb5e1dc6cd61b494d8baf3491348, tsn-c-stack 70936b77dc41981e192438388cd0aced69954f18, and verilog-axis 48ff7a7e2ef782cf778d47910cf85835c64b1bce. The unused external link remains pinned and uninitialized.

The manager must obtain a correction and independent re-review of F1, carry R1/R2 to the residue checklist, and validate the actual current-dev merge candidate with the required builder/native banks and published receipts at merge time. Source-base evidence at f4c9ad4f is distinct from integration with live dev 1e80128f0a467b58bf884b7d9bf62e013a2fb141 or its later tip. Required positive reviews, hosted/act acceptance, candidate validation, explicit merge authorization and post-merge containment remain pending manager duties. This verdict authorizes none of them.

MANIFEST.sha256 lists every publishable receipt and script with relative paths. Scratch data is excluded. Receipt outputs preserve measured values and results; any local path-prefix substitutions are declared in RECEIPTS.txt. No GitHub write or source modification was performed.

R734-1 FINISHED

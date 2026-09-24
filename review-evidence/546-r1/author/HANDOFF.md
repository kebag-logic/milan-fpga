# [A264] Issue #546 handoff

Status: author implementation and validation complete; ready for independent review.

- Head: `39a0171c8c39e68065b14b9178b30d708a9f7645`.
- Branch: `546-crf-talker-step`.
- Base: `57456af96b3127b9d309a995bbbd35a6113ce52d`.
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/546#issuecomment-5816510279.
- One commit, one-line subject, no body or trailers.
- No push, PR operation, merge, other checkout, sub-agent or hardware operation.

## Contract and design

Read issue #546 and #387, including every manager comment, the merged PR #547, the public #539 evidence branch, repository operating rules, requirements, and SV house style. The standards text was read locally: IEEE 1722-2016 4.4.4.3, 4.4.4.7, 10.4.5 and 10.7. The assignment explicitly selects this lane despite the issue's unchanged Backlog card. Independent review and board operations remain with the manager.

IEEE 1722's `tu` indicates uncertainty; its `mr` restart is a separate mechanism. Either accepted `tu` edge restarts rate history. An unmarked adjacent timestamp jump also restarts it. Sequence gaps cannot form the fixed 256-interval measurement, so they restart the history too. Foreign or malformed frames never seed a new reference. The triggering PDU is the first timestamp of the new history. Exactly 256 further intervals produce the first valid rate. The rate register holds its last clean value while invalid.

Threshold derivation: a 2 ms interval with +/-100 ppm media and +/-200 ppm PHC rate has a maximum deviation of ceil(2,000,000 * 300 / 999,900) = 601 ns. Two PHC sampling quantization bounds below 384 ns add 768 ns. Round 1,369 ns upward to 2,048 ns. This derives from #539's rationale; it does not copy its per-cycle 4,096 ns threshold. Comparing the full 64-bit timestamp difference avoids an unmarked 2^32 ns step alias. Arrival jitter never enters this comparison.

The validity output includes the current accepted-PDU verdict, covering a servo boundary on that same edge. It gates only the servo's sample snapshot (`pp_run_r`); PI state and lock qualification hold when the sample is invalid. The servo's own local step/slew guard logic is untouched. A clean PI sequence already in flight may finish. The local PHC step still counts through the existing guard. No new CSR bit or counter is introduced; the register documentation explains the held reading.

## Change list

| File:line | Change |
|---|---|
| `hdl/ieee1722/crf/KL_crf_rx.sv:213` | Rate validity output contract |
| `hdl/ieee1722/crf/KL_crf_rx.sv:282` | Derived adjacent-timestamp threshold |
| `hdl/ieee1722/crf/KL_crf_rx.sv:386` | Full-width jump and tu detection; accept-edge validity |
| `hdl/ieee1722/crf/KL_crf_rx.sv:514` | Cancel pending publication across an event |
| `hdl/ieee1722/crf/KL_crf_rx.sv:584` | Seed/refill rate history; bind and silence invalidate it |
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:249` | Input validity port |
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:565` | Gate only remote sample consumption |
| `hdl/milan/milan_datapath.sv:1725` | Validity net; receiver connection at 5488 and servo connection at 5547 |
| `tb/verilator/crf_rx/Makefile:55` | Default unit, discontinuity and connected servo legs; explicit mutants target |
| `tb/verilator/crf_rx/sim_main.cpp:151` | Existing rate oracle observes timestamp eras; all prior counter checks retained |
| `tb/verilator/crf_rx/sim_discontinuity.cpp:14` | Directed public-output discontinuity, boundary, ordering and lifecycle checks |
| `tb/verilator/crf_rx/crf_talker_wrap.sv:6` | Real receiver wired to production-scale servo |
| `tb/verilator/crf_rx/sim_talker_step.cpp:117` | GM changes with +/-150 us steps at both ends |
| `tb/verilator/crf_rx/mutants.py:20` | Isolated tu, jump, refill and accept-edge mutants |
| `tb/verilator/mmcm_servo/sim_main.cpp:583` | U13 rejects a plausible poisoned invalid rate |
| `tb/verilator/mmcm_servo/rails_wrap.sv:138` | Synthetic clean rate validity tied high |
| `tb/verilator/mmcm_servo/sim_phc_step.cpp:270` | Synthetic clean rate validity driven high |
| `tb/verilator/mmcm_servo_autorepair/sim_autorepair.cpp:167` | Synthetic clean rate validity driven high |
| `scripts/measure_test_evidence.py:597` | Classify the new RTL-reading mutation campaign |
| `docs/design/TIME_SYNC.md:147` | Loop contract; threshold and refill explanation from line 167 |
| `docs/design/GM_LOSS_RECOVERY.md:152` | Aligner and servo rows; evidence rows at 213 |
| `docs/reference/REGISTER_MAP.md:838` | CRF_RATE holds while internal validity is low |
| `docs/testing/TESTING.md:462` | Receiver suite and explicit mutation target |
| `docs/traceability/MODULE_MATRIX.md:100` | Regenerated connected servo and CDC suite coverage |
| `hdl/common/README-tests.md:15` | Generated CDC coverage |
| `hdl/ieee1722/crf/README-tests.md:17` | Generated servo coverage |

## Tests

Commands ran in the foreground, without output pipelines. Builds used the installed 5.050 simulator. The default datapath build used four compile jobs. The exact commands below assume that version is selected through `VERILATOR` or PATH.

| Command / scenario | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/crf_rx` | rc 0; all three legs pass | `crf-rx-final.log` |
| Receiver original checks | 13,836 checks; 0 failures; 1,053 accepted PDUs | `crf-rx-initial.log` |
| Receiver discontinuity | 1,658 checks; 0 failures | `discontinuity.log` |
| Connected receiver + servo | 19 checks; 0 failures | `talker-step.log` |
| `make -C tb/verilator/mmcm_servo` | rc 0; unit 82/82, rails 8/8, PHC steps 113/113 | `mmcm-servo.log` |
| `make -C tb/verilator/mmcm_servo_autorepair` | rc 0; 47/47 | `mmcm-autorepair.log` |
| `make -C tb/verilator/milan_dp run VERILATOR_JOBS=4` | rc 0; all 13 simulation legs pass; render campaign 6/6 | `milan-dp.log` |

The receiver checks cover both tu edges with a sub-threshold 1 us step, held-high tu, +/-21 us and +/-150 us, +/-1 s, +/-2^32 ns, threshold boundaries, legitimate combined rate extremes, arbitrary arrival phase, malformed/foreign markers, sequence loss and duplication, STOP, silence, rebind, reset, a back-to-back pending-publication collision, and natural 64-bit timestamp rollover.

The connected scenario runs the servo at its default 512 ms scale with a closed-loop audio clock. Both talker and listener step by +150 us, with the listener following 100 ms later. The talker asserts tu and clears it after 250 ms. The second scenario steps both by -150 us without changing tu. Each scenario keeps LOCKED on every observed clock, adds zero receiver unlocks, restores the clean rate, and counts the local PHC step once. Integrator: +30.723 ppm unchanged for the marked positive step; +30.703..+30.723 ppm for the unmarked negative step. These are behavioral simulations, not a protocol GM-election or physical-board measurement.

## Mutants

`make -C tb/verilator/crf_rx mutants` rebuilds the clean control and each isolated source copy. Compilation errors and abnormal termination do not count as kills. Campaign rc 0; each mutant executable rc 1.

| Mutant | Failed checks | Named detection |
|---|---:|---|
| tu transition ignored | 9 | `tu edge invalidates before the sampling edge` |
| Timestamp jump backstop removed | 32 | `unmarked timestamp jump invalidates the rate` |
| Refill one interval short | 17 | `all 255 crossing intervals are withheld` |
| Accept-edge validity delayed | 2 | `tu edge invalidates before the sampling edge` |
| Servo ignores input validity | 4 total; U13 trim, lock and resumed-lock checks | `invalid remote sample holds trim` |

Receipts: `mutants-final.log`, `servo-valid-mutant.log`. The additional servo mutant is reproduced by `servo-valid-mutant.py` in this packet: it derives the compile command from the suite's Makefile and substitutes a temporary servo copy. It never edits the worktree. Its clean control is the normal servo suite above.

## Gates

Every final result below is rc 0. Initial style, generated-matrix and idiom findings were fixed; no budget was raised and no test weakened. `gates.tsv` preserves the initial results; `gates-final.tsv` records the corrected verdicts.

| Command | rc | Receipt |
|---|---:|---|
| `python3 scripts/docs_check.py` | 0 | `docs.log` |
| `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `toc.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `matrix.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | `xvlog.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `source-lists.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idiom.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `py-idiom.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `sv-idiom.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `test-evidence.log` |
| `behave --no-capture -f plain` | 0 | `behave.log` |
| `git diff --check 57456af96b3127b9d309a995bbbd35a6113ce52d HEAD` | 0 | `diff-check.log` |
| `git diff --cached --check` | 0 | `diff-cached-check.log` |
| `python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d` | 0 | `em-dash.log` |
| `python3 scripts/docs_check.py` in a no-git HEAD archive | 0 | `docs_check-no-git.log` |
| `python3 scripts/check_feature_status.py` in that archive | 0 | `check_feature_status-no-git.log` |

Behavior gate: 14 features, 344 scenarios and 1,739 steps pass. Front-end analysis actually ran: zero parent RTL findings; four pinned-processor findings equal the ratchet. The lint ratchet passes without an increase. The em-dash check uses exactly the supplied base, with 0 findings across 61 added Markdown lines and 339/339 controls.

## Area

Before and after: `bash syn/yosys/ooc.sh KL_crf_rx KL_mmcm_drp_servo`, rc 0, default parameters, `synth_xilinx -family xc7 -flatten`. Before is the supplied base; after uses the committed RTL. This is mapped per-module area, not placed whole-device utilization or timing.

| Module | LUT before -> after | FF before -> after | CARRY4 before -> after | Unchanged |
|---|---:|---:|---:|---|
| CRF receiver | 355 -> 433 (+78) | 509 -> 544 (+35) | 125 -> 147 (+22) | 1 RAMB18; no DSP |
| Servo | 862 -> 864 (+2) | 790 -> 790 (0) | 150 -> 150 (0) | 1 DSP; no BRAM |
| Sum | +80 | +35 | +22 | No BRAM/DSP delta |

Receipts: `area-before.log`, `area-after.log`.

## Limits and handoff

- No timing run or hardware activity. Hosted checks, public evidence archival and independent reviews belong to the manager.
- #545 owns local PHC slew rejection. This lane changes the servo sample input only; that guard's implementation remains untouched.
- The backstop accepts unmarked spacing deviations up to 2,048 ns. The tu marker catches the tested 1 us discontinuity; an unmarked smaller jump is indistinguishable from the allowed timing envelope.
- A held tu level permits recovery after a complete clean history. This is the assigned edge-based discontinuity policy, not a claim that tu must be low for all samples.
- No new status/tally bit. Receiver media-lock accounting remains independent of temporary rate validity.
- Final authorized action: publish `review-ready.md` as `[A264] REVIEW READY` on #546 with this head, then stop. No push or PR operation is authorized. The manager owns independent review and subsequent publication.

[A363] Round 2 handoff

Ready for independent review; final local gates returned zero.

Repository: `kebag-logic/milan-fpga`  
Working directory: `$LANES/397-service-budget`  
Branch: `397-service-budget`  
Starting head: `7f997b60d5a74d46beca5c263d27496ccce0ae4f`  
Candidate head: `ff75a70807c151517860c73a06d7ea36e2a46008`  
Commit subject: `fix: qualify service-budget timing and liveness evidence`  
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`

## Contract and disposition

The complete issue, all assignments, both full round-1 review reports, the manager bank comment,
issue #590 and the cited repository contracts were read. The
[round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5855879265)
is the implementation scope. Every listed duty has an observed marker or enclosing interval;
no STOP condition applies. This is author evidence, not a review verdict.

The round-2 measurement changes are implemented. Queued input still lapses writer backing in both
shapes; the firmware repair belongs to #590. Future duties, physical torture, the complete hart
decision, independent review and merge remain open. The replacement body uses `Refs #397`.

## Change list

| File:line | Change |
| --- | --- |
| `tb/verilator/fw_service_budget/run.py:41` | Named plans, independent device waits and immediate input refusal |
| `tb/verilator/fw_service_budget/run.py:75` | Reconstruct no-tick spans; validate compressed blocks; report phase/TX bounds and backing samples |
| `tb/verilator/fw_service_budget/run.py:259` | Tight AEM markers, 20 s boot comparison, schedule-qualified heartbeat row and UART reconstruction |
| `tb/verilator/fw_service_budget/run.py:342`, `oracle.json:1` in the same directory | Pin three traces and expected analyses; 30 portable oracle controls |
| `tb/verilator/fw_service_budget/run.py:413` | Preserve raw evidence before analysis and verify bound-log regrades |
| `tb/verilator/fw_service_budget/build.py:104`, `observe.vlt:1` in the same directory | Bind passive retirement observation to the linked ELF and unchanged CPU hierarchy |
| `tb/verilator/fw_service_budget/sim_main.cpp:32`, `:72`, `:144` | Sample committed entries, add first-AEM-read marker, pace UART and compress tick events |
| `tb/verilator/fw_service_budget/flash.hpp:101`, `flash_test.cpp:67` in the same directory | Expose AEM-read boundary; isolate the busy predicate independently of WEL |
| `tb/verilator/fw_service_budget/README.md:15` | Reproduction, supported plans/waits, evidence handling and measurement limits |
| `docs/findings/397_SERVICE_BUDGET.md:19`, `:110`, `:247`, `:292`, `:338` | Duty/schedule maxima, liveness evidence, device-max results, controls and receipt hashes |
| `docs/findings/397_SERVICE_BUDGET_1X1.json:1`, `397_SERVICE_BUDGET_8X8.json:1` at the starting head | Removed raw run receipts from the product tree; retained verbatim as round-1 packet receipts |
| `docs/integration/BAREMETAL_FIRMWARE.md:1882` | Document queued-input starvation in both shapes and the #590 repair scope |

## Results

| Observed result | 1x1 | 8x8 |
| --- | ---: | ---: |
| Longest boot to entity enable, ms | 373.97461 | 1094.48517 |
| Margin against 20,000 ms ADP comparison, ms | 19626.02539 | 18905.51483 |
| Longest AEM envelope, ms | 57.99594 | 137.01392 |
| Longest NVM status envelope, ms | 233.64297 | 814.07889 |
| Device-max whole commit, ms | 3339.59461 | 4307.68299 |
| Queued heartbeat tail, ms | 2569.49201 | 2513.33593 |
| Final queued backing sample | 0 | 0 |

These are maxima over the four executed plans, not arbitrary-stall or physical worst-case proofs.
The AEM values include the marked tail through entity enable. UART-paced boot still excludes
BIOS CRC, startup delays and memory testing. The conditional duty-period tables in the findings
combine the longest measured no-tick span, 250 ms phase and maximum full-output TX allowance.
Paced spans already include TX blocking, so that allowance is conservative; a negative bound
margin is not itself an observed violation. Actual schedule overruns are below.

| Shape / plan | Largest observed gap ms | 500 ms margin | 2,000 ms margin | Gap endpoints ms | Final tail? | Printed backing samples |
| --- | ---: | ---: | ---: | --- | --- | --- |
| 1x1 / `all` | 430.62305 | 69.37695 | 1569.37695 | 942.86687 to 1373.48992 | Yes | 1, 1, 1, 1, 1 |
| 1x1 / `uart-paced` | 332.34992 | 167.65008 | 1667.65008 | 312.74513 to 645.09505 | No | 1, 1, 1, 1, 1 |
| 1x1 / `queued-input` | 2569.49201 | -2069.49201 | -569.49201 | 252.58315 to 2822.07516 | Yes | 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0 |
| 1x1 / `device-wait` | 250.00968 | 249.99032 | 1749.99032 | 252.58315 to 502.59283 | No | 1 |
| 8x8 / `all` | 1449.77764 | -949.77764 | 550.22236 | 3390.63747 to 4840.41511 | No | 1, 1, 1, 1, 1 |
| 8x8 / `uart-paced` | 991.91598 | -491.91598 | 1008.08402 | 954.12589 to 1946.04187 | No | 1, 1, 1, 1, 1 |
| 8x8 / `queued-input` | 2513.33593 | -2013.33593 | -513.33593 | 893.96257 to 3407.29850 | Yes | 1, 1, 0, 0 |
| 8x8 / `device-wait` | 588.61054 | -88.61054 | 1411.38946 | 893.96257 to 1482.57311 | No | 1 |

| Shape / device-max duty | CPU cycles | Service ms | WIP ms | Measured ms | Budget ms | Margin ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1x1 / Erase envelope | 151,005,855 | 20.11709 | 3000 | 3020.11709 | 3,500 | 479.88291 |
| 1x1 / Journal START-to-ACK | 161,067,660 | 156.35320 | 3065 | 3221.35320 | 8,000 | 4778.64680 |
| 1x1 / Whole console commit | 166,979,731 | 274.59461 | 3065 | 3339.59461 | 8,000 | 4660.40539 |
| 8x8 / Erase envelope | 153,725,874 | 74.51747 | 3000 | 3074.51747 | 3,500 | 425.48253 |
| 8x8 / Journal START-to-ACK | 192,836,355 | 606.72710 | 3250 | 3856.72710 | 8,000 | 4143.27290 |
| 8x8 / Whole console commit | 215,384,150 | 1057.68299 | 3250 | 4307.68299 | 8,000 | 3692.31701 |

## Independent public probes and controls

| Public probe | Executed scenario | Result |
| --- | --- | --- |
| P1 | 1x1 paced full command plan | CSR gap 332.34734 ms; printed backing samples remain one |
| P2 | 1x1 full plan, 1 s erase / 5 ms page WIP | CSR gap 412.37988 ms; four heartbeats per erase, maximum spacing 250.00068 ms; printed backing samples remain one |
| P3 | 1x1 twelve queued NVM status commands, then register status | CSR tail 2569.49201 ms; backing falls to zero |
| PA | 1x1 independent full-plan observer | Original raw stream reproduced; no backing lapse; AEM read-completion-to-enable 55.76477 ms |
| PC | 8x8 independent 3 s erase / 5 ms page commit | Commit 4307.68299 ms; START-to-ACK 3856.72710 ms; fabric-kick gap 588.61054 ms; no backing lapse; twelve erase heartbeats at up to 250.00068 ms spacing |
| PD | 8x8 three queued NVM status commands | Fabric-kick tail 2505.57721 ms; direct backing lapse and final printed zero |
| PB | 8x8 independent full-plan observer | Original raw stream and rows reproduced exactly; fabric-kick gap 1449.77764 ms; no backing lapse; AEM completion-to-enable 134.76237 ms |

All public probe programs and mutation scripts were extracted with `git show FETCH_HEAD:<path>`
after fetching `397-review-evidence`, and remained byte-identical to their public sources.
The source commit and script SHA-256 values are in `receipts/public-provenance.json`.
P1/P2/P3 and both ordinary observer logs reproduce the original public/round-1 streams.
Wrappers that background jobs or pipe status were not used; their unchanged probe programs
were invoked in the foreground. The mutation scripts ran against a disposable harness fixture
mirror in temporary storage, with the two `all` receipts at their legacy lookup paths.

| Control | Result |
| --- | --- |
| Portable oracle | 30 controls, 0 failures |
| Independent flash controls | 14 controls, 0 failures |
| External public grader mutants | 11/11 rejected; unchanged control returns 0 |
| Internal public grader mutants | 15/15 rejected |
| Bitmask mutant qualification | Recorded standalone writes are equivalent; the extra combined-word control rejects the changed selector |
| Busy-check deletion | rc 1, specifically the program-while-busy check |
| Unsupported wait CLI inputs | Four refusals before a build directory is created |
| Default queued-input regrade | rc 1 with the named heartbeat-budget finding, as required |
| Reporting-mode measurement regrades | 8/8 rc 0; findings retained |
| Independent packet/table arithmetic audit | 8 receipts, 10 digests, 28 duty rows and 28 opportunity rows verified |

## Gate table

All commands used the physical working directory above and ran in the foreground without shell
pipelines. The selected environment supplies the configured BIOS-build interpreter; the two
Markdown commands use the pinned temporary environment. Complete logs and exact argument arrays
are under `receipts/gates/`; measurement commands are in `receipts/measurement-gates.json`.
For a fresh run, build the matching shape using the README recipe, then replace
`--regrade` with `--reuse-build` in the measurement command.

| Gate / exact command | rc | Result |
| --- | ---: | --- |
| `python3 -B tb/verilator/fw_service_budget/run.py --self-test` | 0 | PASS |
| `python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | PASS |
| `python3 -B scripts/check_nvm_capture.py` | 0 | PASS |
| `python3 -B scripts/check_feature_status.py --self-test` | 0 | PASS |
| `python3 -B scripts/pp_srcs.py --check` | 0 | PASS |
| `python3 -B scripts/check_baremetal_only.py --check` | 0 | PASS |
| `python3 -B scripts/check_entity_shape.py --self-test` | 0 | PASS |
| `python3 -B scripts/docs_check.py` | 0 | PASS |
| `python3 -B scripts/check_doc_paths.py` | 0 | PASS |
| `python3 -B scripts/check_doc_style.py` | 0 | PASS |
| `python3 -B scripts/check_archive.py` | 0 | PASS |
| `/tmp/a363-markdown/bin/python -B scripts/gen_toc.py --check` | 0 | PASS |
| `/tmp/a363-markdown/bin/python -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | 0 | PASS |
| `python3 -B scripts/check_py_idiom.py` | 0 | PASS |
| `python3 -B scripts/check_cpp_idiom.py` | 0 | PASS |
| `python3 -B scripts/check_hygiene.py --check` | 0 | PASS |
| `python3 -B scripts/measure_test_evidence.py --check` | 0 | PASS |
| `git diff --check ac18b50968b12efe4d15c0a06301264b35656b31` | 0 | PASS |
| `$WORKSPACE_HOME/litex-milan/venv/bin/python -B sw/builder/test_builder.py --require-elaboration` | 0 | PASS; calibration arm not run (missing physical report) |

The full bank's unavailable calibration arm is explicitly outside its verdict. No hardware was used.

## Evidence custody and execution notes

The packet retains the two original raw receipts and eight round-2 receipts, each with its raw log
and input/build hashes. The ten complete-file hashes are recorded in the findings page.
`SHA256SUMS` covers the final packet. Compact independent boundary receipts retain all UART,
input, CSR and liveness observations, all erase/program commands and first/last AEM reads.
Their companion JSON records the omitted intermediate flash reads and the full temporary
probe hash. Complete probe streams and all build trees remain in temporary storage.
`python3 -B CHECK-EVIDENCE.py $LANES/397-service-budget` independently checks the
displayed maxima, receipt identities and current measurement-source hashes against the packet.

Each final native measurement completed successfully. Some initial wrapper analyses refused
because the analysis source changed while those long native runs were executing. One paced 1x1
analysis also exposed the now-fixed split-UART-word parser issue. Its successful native log was
preserved and bound to the verified unchanged compiled inputs before regrading. All eight final
bound-log regrades return zero. No native source or compiled product input changed during those
final measurements. A sequential public wrapper started a redundant queued probe after its
successful device-max probe; that duplicate was terminated (wrapper rc 143). The separately
executed unchanged queued probe completed with rc 0 and supplies the evidence.

Ten firmware/capture files are byte-identical to the starting head; their hashes are in
`receipts/protected-inputs.json`. The commit changes no RTL or submodule pin. No private transcript,
hardware access, push, PR edit, merge, additional checkout or delegated work was used.

## Handoff state

`PR-BODY.md` is the full replacement body with a Round 2 section. It is prepared for the manager
to publish with the local commit and evidence packet. Independent reviewers must accept the
finding resolutions and coverage ledger. Issue #397 stays open for its remaining bench and
architecture work. The final issue comment will identify this exact candidate head and the
measurement/gate results; posting that comment is the last task action.

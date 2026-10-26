[R704] NEGATIVE - exact head d58c8e22e9bd96237b9a28ea1ddd55b0426380c4

External independent review R704-1 of issue #665 / PR #792. All five lenses were applied. Four MAJOR findings and one MINOR finding remain open; one comment-only RESIDUE is nonblocking. The expected T_svc miss is the measurement result, not a finding against this PR.

Reviewed tree: `e755f4dafb61b4904a8cecdf908aff3500465cc1`. Base: `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. The one-commit delta adds 14 files, all under `tb/verilator/ctrl_service_budget/`; no shipping RTL, SoC, firmware, CI or existing documentation file changes. `environment.json` records the delta and execution identities.

The independent reconstruction followed AGENTS/CONTRIBUTING, the documentation map, the frozen issue/public decisions, linked requirements and interfaces, then the diff/history and executable evidence. Authorities include [the assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409745905), [owner decisions](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409738976), FR_NFR.md 3.4.1/3.4.2, MAILBOX_SPLIT.md service and backlog tables, SPLIT_CONTROL_MEMORY.md, the mailbox contract, and the shipping CPU/memory implementation. The [manager ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6413711129) accepts a measurement STOP; it does not make incomplete load or endpoint measurements complete.

The [published author evidence](https://github.com/kebag-logic/milan-fpga/tree/90dd5bdf68f6f772a1e5907a93fe337499b10c48/review-evidence/665s2-r1) was examined after the independent diff pass. All 217 entries match its publication manifest (`published-evidence-check.json`). The source-head gate receipts are the author's. No manager source-bank execution at this head is claimed. After writing my independent verdict and ledger, I checked the public PR discussion, review submissions and inline threads: only two review-start notices, zero submitted reviews and zero review threads were present. There were no prior public findings to resolve or retain (`prior-findings-check.json`). No other reviewer's report was read.

**Independent measurements and checks**

Both formal arm-A points were built freshly and run on the native CPU model, with two concurrent campaigns using `--jobs 8` each. All children were joined in foreground drivers. Native builds used `make -j16`; simulations were paused only within this packet while necessary to respect the job cap. The selected 14 groups per point include every implemented response/timer/backlog group and the native baseline control; the separate fixture group is covered by the committed-trace self-test. Both campaigns completed with zero refusals and the expected recorded budget misses. Every selected group's probe and pass results match the published author results exactly, exceeding the stated rounded-table tolerance (`measurement-audit.json`, `measurements/A1/`, `measurements/A8/`).

| Measured arm-A figure | 1x1, one interface | 8x8, two interfaces |
|---|---:|---:|
| Worst pass, CPU cycles | 1,552,161 | 2,989,496 |
| Worst pass, ms | 31.04322 (`acmp-disc`) | 59.78992 (`acmp-notk`) |
| Claimed composed maximum, CPU cycles | 1,391,312 | 2,141,242 |
| Claimed composed maximum, ms | 27.82624 | 42.82484 |
| Event behind 15 others, ms (pass bound) | 14.12206 (27.14422) | 40.51427 (67.63610) |
| ACMP command backlog, ms (pass bound) | 60.35408 (67.07636) | 101.98212 (113.41868) |
| ENTITY_AVAILABLE backlog, ms (pass bound) | 43.89928 (52.85356) | 48.63248 (65.41566) |
| Seven responses owed ahead, ms (pass bound) | 75.75644 (78.69846) | 98.92524 (106.91706) |
| Same owed row after room returns, ms | 15.75648 | 38.92528 |

These are reproduced clock counts for the actual scripts. F1 prevents accepting their advertised maximum-load coverage. F2 also prevents accepting every response endpoint simply because its published value reproduces. The selected campaigns record 9 misses at 1x1 and 44 at 8x8. The author's 1x1 total of 10 additionally includes `fixture.entity_departing.if0` (25.17172 ms); that duplicate fixture group was checked through the committed-trace self-test rather than independently simulated here.

The freshly linked ELF hashes match the published formal images: 1x1 `d4c28047549719c4a2115674913550dd13b9d3b06074c1d577d46aeeecda3639`; 8x8 `c89a1871fd2bca2b5515492c6996b076551bbda7ccd58c773c8bc633a00224ba`. `ctrl_srp_image.py --with-aecp --layout split` links the unmodified arm-A source. The disclosed #723 runtime wrapper supplies `-fno-stack-protector`. Arm B modifies only a scratch test fixture's observation callbacks and is labelled as diagnostic, not the formal measurement; its implementation and public receipts were inspected, but it was not independently rerun.

The CPU is the shipping cacheless RV32I, one hart, without M, at 50 MHz; the bus is 100 MHz, with the shipping 32-bit bus path, idle DMA port, and shipping `add_ctrl_memory`/CtrlMemory banking. The fresh configuration, core arguments, regions and memory plans equal the published ones (`builds/A1.json`, `builds/A8.json`, `cost-audit.json`). The harness uses KL_mbx behind KL_mbx_wb; the two-interface variant is generated into its build directory. Its placeholder peripheral map and 256 KiB CPU decode cover are disclosed test accommodations. Physical CtrlMemory bank sizes still derive from the linked image. The cover/as-built generated cores differ in address-decode/PMA logic (`core-region-decode.diff`). This is not proof that the unchanged shipping split SoC boots. The observed service-code sets also reproduce: the largest individual run fetches 40,532 bytes at 1x1 and 43,060 bytes at 8x8, lower bounds on the complete hot set.

The separate as-built control reproduced #791: instruction-access fault cause 1 at committed PC `0x6880`, repeated at system cycles 330592, 661083 and 991574. The grader refused the trapped execution and the control reported caught (`controls/asbuilt/`, `logs/asbuilt-control.log`). The supplied slow-ADP control measured 24.614 ms, versus approximately 0.294 ms unplanted, and was caught. My independent 24,000-iteration ACMP receive delay changed BIND_RX from 1.62495 ms to 38.10553 ms; it crossed the unchanged 10 ms threshold and was caught (`independent-control.json`, `logs/A1-own-probe.log`, `logs/own-slow-own-probe.log`). Only disposable firmware copies were mutated.

The portable self-test passed all 19 checks and caught all 12 named marker, clock-ratio and deadline mutants (`logs/selftest.log`). Docs checks, cited paths, doc style, archive checks, em-dash checking against the reviewed base, and contents checking passed. Behave passed all 14 features, 406 scenarios and 1,977 steps, with no skips. These are independent focused results; the broader author gate receipts remain separate evidence. No prohibited full bank or hosted/local CI acceptance run was performed.

Cost evidence supports the reported optimization priorities, within the actual tested load. The 8x8 link-up pass is 2,004,666 cycles: `mrp_mad` 473,950, `memset` 361,053, `memcpy` 244,102, `__mulsi3` 111,201 and `__udivsi3` 89,954. READ_DESCRIPTOR's 1x1 `memset` counts are 153,929–156,240. The two AECP polls contribute 26,497 + 20,254 cycles at 1x1 and 73,883 + 20,254 at 8x8. Source inspection confirms the byte-loop runtime, 1,514-byte response zeroing and 1,476-byte payload zeroing, and `aecp.c:461-495` retrying at `now + 1` when the observation is unavailable, without increasing backoff. `cost-audit.json` records the measured pass modules and access totals. Flash-window loads cost approximately 263 CPU cycles versus roughly 9.1 for BRAM fetches, about 29 times; that is a measured model access-cost ratio. The projected XIP slowdown is an inference, not a flash-executed service-path measurement or hardware calibration.

**Open findings**

**R704-1-F1 — MAJOR — Conformance, Robustness, Tests, Docs**

Artifact: `tb/verilator/ctrl_service_budget/scenario.py:505`, `:518`, `:570`; `tb/verilator/ctrl_service_budget/README.md:247`.

Authority/evidence: the frozen assignment requires the composed maximum and MAILBOX_SPLIT.md:753-758 backlog rows. `backlog_groups` promises every receive ring's admitted burst; the README says each row runs with every other channel's burst too. Both fresh `backlog` traces commit ADP=8, ACMP=12, AECP=16, MAAP=0, SRP=0 between their composed markers. The MAAP addresses offered at line 518 do not pass the range-overlap filter; no SRP burst is generated. Both `backlog-adp` traces commit ADP=8 and zero records for every other receive channel. The owed-response phase also runs separately after the composed interval. See `measurement-audit.json` and the raw `backlog*.log`/scripts for both points.

Impact: the numbers are real for a reduced offered/admitted load, but do not measure the documented composed maximum or each backlog row under that load. The conclusions about admitted backlog and the proposed work cap lack that required stress evidence. A token-bucket initial burst is also not proof of the maximum queue occupancy attainable while service runs.

Required outcome: establish and assert the required concurrent admitted populations and actual queue occupancy, distinguish initial burst from full backlog, and remeasure every required row under the specified background work. Correct the resulting tables and claims. Do not bypass the shipping ingress filter to make a nominal packet count look admitted.

Verification: inspect committed RX records and queue occupancy, prove completion of the intended records on each relevant interface, and require a control dropping any required background load to fail coverage. The current zero-MAAP/zero-SRP run must not count as the composed maximum.

**R704-1-F2 — MAJOR — Conformance, Robustness, Tests, Docs**

Artifact: `tb/verilator/ctrl_service_budget/grade.py:230`; `tb/verilator/ctrl_service_budget/README.md:103`.

Authority/evidence: FR_NFR.md:341 ends notification fan-out at the last required recipient's commit. `notify` instead takes the first unsolicited AECP frame on any interface without identifying its causal command or complete recipient set. In the unmodified 8x8 campaign, `aecp.set_name.if1` starts at 192852913 and is graded to 193646246 (7.93333 ms), while the required second notification commits at 193691826 (8.38913 ms). The additional native probe independently measures 7.24969 ms against 7.70397 ms for the last commit (`native-fanout.json`). Synthetic probes place that final recipient at 14 ms or remove it; both remain reported as measured, and the late case is graded fitting at 4 ms (`grader-probes.json`, `notification-*.log`).

Impact: notification latency is understated in a real published row; a late or missing required recipient can escape the endpoint and budget check. The existing last-output mutant covers the listed output kinds, not every required notification recipient.

Required outcome: identify the causal notification and complete required recipient set, end at the last matching commit, and refuse incomplete delivery. Update affected figures and the endpoint/self-test claims.

Verification: two or more registered recipients across interfaces; late, missing, duplicate, wrong-recipient and unrelated unsolicited frames. The 14 ms last-recipient trace must miss T_svc, and a missing required recipient must be refused.

**R704-1-F3 — MAJOR — Conformance, Robustness, Tests, Docs**

Artifact: `tb/verilator/ctrl_service_budget/build.py:341`, `:355`.

Authority/evidence: the assignment requires the unmodified linked firmware and reproducible execution evidence. The reuse contract promises validation of every recorded input. Runtime `sim_rom_bank*.init` files are absent from the attestation, and generated/external basename inputs are silently skipped when they do not resolve beneath the checkout. In an isolated copied build, changing the ELF and replacing the first ROM instruction with `jal zero,0` both leave `build.reused()` successful. The unchanged native executable then runs that changed ROM, completing zero service passes (`grader-probes.json`, `changed-rom-native.json`, `logs/changed-rom-native.log`). This demonstrates execution of an unattested input; it does not claim the zero-pass execution would pass the full scenario grader.

Impact: successful reuse cannot bind a measurement to the stated linked image or all generated inputs. The executable hash alone does not protect the ROM data loaded at runtime. Fresh images in this review matched the published images, but the evidence-validation mechanism remains defective.

Required outcome: bind every runtime execution input, resolve generated inputs against their recorded build location, and refuse changed or missing inputs instead of ignoring them. Correct the reuse claim and add regression controls.

Verification: independently modify/delete each ROM bank, the ELF and generated sources. Reuse must refuse before execution; an unchanged build must remain reusable.

**R704-1-F4 — MAJOR — Robustness, Tests, Docs**

Artifact: `tb/verilator/ctrl_service_budget/run.py:169`; `tb/verilator/ctrl_service_budget/README.md:43`.

Authority/evidence: the documented run contract requires every selected probe to be measured even with budget findings recorded. Regrade silently removes selected groups whose logs are absent. An actual invocation selecting `backlog,backlog-adp` with an empty output directory returns zero and prints `0 groups graded, 0 refusals, 0 T_svc misses` (`grader-probes.json`, reproducible in `probe_graders.py`).

Impact: missing measurement evidence is reported as a successful regrade. A partial or empty receipt set can appear clean without executing the requested coverage.

Required outcome: require the logs/scripts and probes for every selected group. A deliberate partial regrade must explicitly select its subset; absence must not silently redefine it.

Verification: delete one selected log and then all selected logs. Both must fail, with and without `--record-budget-findings`; an intact explicit subset must pass.

**R704-1-F5 — MINOR — Conformance, Tests**

Artifact: `tb/verilator/ctrl_service_budget/README.md:163`; `scenario.py:227`; public author acceptance table in issuecomment-6413662864.

Authority/evidence: the frozen assignment includes every MAILBOX_SPLIT.md:495-502 ADP path, including SHUTDOWN to ENTITY_DEPARTING. The README truthfully says this path is unreachable through the fixture, and the author's acceptance table says partly met. The public STOP/manager ruling does not explicitly waive this frozen measurement criterion.

Impact: one required path remains unmeasured; its latency and endpoint checks cannot be counted complete. This finding is about coverage, not the expected budget miss, and does not ask this harness PR to repair the shipping service budget.

Required outcome: measure the linked path through an authorized test-only entry without silently changing the formal image, or obtain an explicit public amendment/disposition of the frozen criterion. Retain the incomplete status until then.

Verification: a measured shutdown/departing row and a defect-detecting control, or the explicit public scope amendment.

**R704-1-R1 — RESIDUE — Docs**

Artifact: new source comments/docstrings at `build.py:25,40,48`, `run.py:4`, `scenario.py:3`, `selftest.py:3`, `split_soc.py:13`, `sim_main.cpp:4`, all in `tb/verilator/ctrl_service_budget/`.

Authority/evidence: the owner's source-comment rule prohibits lane and review-round labels. These comments contain `S2`, `the lane's -j16`, and `the method of #397 round 2`.

Impact: comment wording only; no measurement, figure, verdict, generated artifact, conformance claim or privacy behavior changes. This residue does not make any lens unclean.

Exact fix: remove ` S2` from the listed issue references, retaining `#665`; replace `the lane's -j16` with `16 parallel compile jobs`; replace `the method of #397 round 2` with `#397`. Keep the behavioral explanations and relevant issue/requirement IDs.

Verification: inspect the added source comments for those labels; the code and executable outputs must remain unchanged. The manager carries this to the residue checklist.

**Reviewer-owned coverage ledger**

[R704] PASS RTL — `split_soc.py:159,255,288`; `milan_soc.py:2737-2785,2857-2893`; `builds/A1.json`, `builds/A8.json`; `core-region-decode.diff`; `controls/asbuilt/boot-fault.log` — checked shipping core options, clock/bus widths, memory banking, mailbox integration and the explicitly conditional decode workaround against the product implementation. No new RTL/architecture defect was found within this harness-only delta. The existing #791 fault remains a disclosed deployment limitation, not repaired by this result.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Frozen #665 assignment/decisions; FR_NFR.md 3.4.1/3.4.2; MAILBOX_SPLIT.md service/backlog tables; scenario.py, grade.py, build.py; F1/F2/F3/F5 | R704-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |
| RTL | CLEAN | Product CPU/clock/bus configuration; shipping CtrlMemory; split_soc.py; KL_mbx/KL_mbx_wb hookup; generated core delta; both fresh builds and region-fault control | R704-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |
| Robustness | UNCLEAN | Actual admitted backlog records; notification fan-out; missing/late output probes; changed runtime ROM; missing-log regrade; F1/F2/F3/F4 | R704-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |
| Tests | UNCLEAN | selftest.py, oracle.json, fixture.log; both fresh 14-group campaigns; native controls; independent slow ACMP and grader probes; docs/behave receipts; F1/F2/F3/F4/F5 | R704-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |
| Docs | UNCLEAN | README.md results, endpoints, load/reuse/regrade claims; public author receipts and scope decisions; F1/F2/F3/F4; R1 residue | R704-1 | d58c8e22e9bd96237b9a28ea1ddd55b0426380c4 |

**Limits, containment and pending duties**

Measurements are CPU simulation on the disclosed test SoC, at one stimulus phase per probe; the reported phase bounds are conditional on the same work/pass sequence. They are not exhaustive load or phase proofs. Mailbox commitment is the endpoint; wire transmission, network round trips and physical calibration are outside these figures. Flash program/erase wait modeling is not target NVM latency. The linked fixture polls and has unavailable observation ports in arm A; SHUTDOWN and START_STREAMING are not measured. Physical calibration was NOT RUN; field skips are not hardware proof. No hosted status, skipped context or software scenario is represented as hardware evidence.

No source fixes, commits, pushes, GitHub writes, merges, author contact, other-checkout edits or prohibited full verification banks were performed. Only disposable build/probe copies changed. `identity-final.json` verifies the exact HEAD/tree, every tracked blob's raw bytes, file type and executable mode, the full index, and the five required submodule gitlinks and tracked contents. `MANIFEST.sha256` lists the publishable packet files; the scratch tree is excluded. Raw simulation logs retain their bytes; build/driver path substitutions are recorded with both hashes in `receipt-index.json`. Reproduction commands and portable scripts are included in `REPRODUCE.txt`.

The manager must publish this packet, obtain fixes or an explicit frozen-scope disposition as appropriate, and commission re-review of the affected lenses at the corrected head. No coverage is transferred automatically to changed artifacts. Two independent positive reviews and the remaining completion bar are still required. The manager owns hosted/act acceptance, the final current-dev candidate build/native banks and their receipts, exact-candidate validation, and any authorized merge/post-merge containment. This source review uses base e76a755a; it does not validate a merge with the supplied live dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`. No merge is authorized by this report.

R704-1 FINISHED

[R932] NEGATIVE - exact head 166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e

External independent review, round R932-1, of kebag-logic/milan-fpga #1009 / PR #1014. Two MAJOR findings and one MINOR finding remain open. All five lenses were applied; none is clean because of the findings below. This is a source review verdict, not merge authorization or hardware acceptance.

Reviewed tree: `08861f5484fad777532ecd5faa89af199e18a87a`. Reviewed range: `5de21ff3661436ea5598718aca36934361e35340..166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e`, 18 commits and 49 changed files. The checkout was detached and isolated. No source fix, commit, push, GitHub write, hardware operation, or other checkout edit was made.

The task was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue and its public scope decisions, the linked requirements and interfaces, then the diff and history. The independent pass preceded examination of the published executable evidence. The independent verdict and ledger were written before inspecting prior public review findings. At the subsequent inspection, the PR timeline contained only two review-start notices; formal reviews and inline threads were empty. There were no prior public findings to resolve or retain. No other reviewer report was consulted; see `public-review-status.txt`.

Authority: [issue #1009](https://github.com/kebag-logic/milan-fpga/issues/1009), the [superseding scope ruling](https://github.com/kebag-logic/milan-fpga/issues/1009#issuecomment-7170938286), REQUIREMENTS.md, docs/design/SAVED_STATE_MATERIALIZATION.md DR2a/DR2c and persistence/restore contracts, docs/design/SAVED_STATE_FORMAT_32X32.md, and the store/interface documentation. The scope covers a delta frame containing what the older slot lacks, without erase, and a 100 ms first-dirty binding window. Other classes retain 1,000 ms. Bind, unbind, started and stopped belong to the binding class under Milan v1.2 5.5.3.5.3 and 5.3.8.3. Strict save-before-response belongs to #1012 and is not a finding here. This PR relates to #1009 and #876; it does not close them.

**F1 — MAJOR — Conformance, RTL, Robustness, Tests, Docs — A maintenance capture that acquires user work bypasses transaction failure accounting.**

Artifact: `sw/firmware/ctrl_nvm/nvm_store.c:987`, with the maintenance start at :770, capture at :883 and joining change at :1271; `sw/firmware/ctrl_nvm/test/test_nvm_delta.cpp:414`; `sw/firmware/ctrl_nvm/README.md:312`.

Authority/evidence: DR2c (docs/design/SAVED_STATE_MATERIALIZATION.md:2396) allows at most three transaction attempts per unchanged captured work set, separated by 1,000 ms. Failed user work must retain the stale claim and first-failure accounting. A full target starts an idle maintenance capture with `tidy=1`. A binding change arriving during that capture can join it and enter `inflight`, but `tidy` remains set. The unconditional early return in `nvm_fail` then skips stale, attempts, first failure and backoff. `probe_tidy.py` / `probe_tidy.cpp` compile the unchanged store and reproduce this through both flash ports at both AX7101 shapes. After the first erase refusal: `pending=1`, `failed=1`, `attempts=0`, `stale=0`. Persistent refusal yields four failed attempts while the counter records three. At 1x1 the first two failures are only 1.700 ms apart on the direct port and 1.911 ms on the command port; at 8x8, 5.900 and 6.114 ms. Empty-maintenance controls pass at both shapes and ports. Raw evidence: `tidy-probe.log`.

Impact: user work captured by maintenance loses its first failure record, retries immediately and receives a fourth attempt, contrary to DR2c. The no-stale maintenance description is also false for this reachable case. The existing tests cover an empty maintenance failure and a change later during maintenance, but do not cover a change joining its capture followed by failure. The probe does not demonstrate destruction of the authoritative slot.

Required outcome: limit the maintenance exception to work that has no changed user state awaiting durability. A maintenance capture that takes user work must use ordinary failure, stale, bounded-attempt and backoff handling. Update the documented exception and add regression coverage for this combination.

Verification: both ports at 1x1 and 8x8 must show stale and one charged attempt on the first failure, no retry before the required backoff, and at most three attempts for the unchanged captured work. Preserve the passing empty-maintenance controls and reboot survival of the last authoritative slot.

**F2 — MAJOR — Conformance, Robustness, Tests, Docs — The frame timing grade accepts incomplete post-program verification.**

Artifact: `tb/verilator/ctrl_service_budget/save_burst.py:349`, `save_grade.py:73`, `sim_main.cpp:296`, and the durability claims in `tb/verilator/ctrl_service_budget/README.md` and the published measurement receipt.

Authority/evidence: #1009 measures response-to-durable time, with verified promotion preserved; a blank check is not a read-back of programmed bytes. The trace and Python merging combine overlapping reads on opposite sides of programming. `frame_saves` accepts the entire merged span when its end is after the last program, even if most bytes were only read before programming. `probe_verify.py` constructs a 64-byte blank-check run, programs the frame, and reads only four bytes afterward. The grader reports the entire frame durable at cycle 1200. No-post-read and complete-post-read controls behave as expected. A second probe goes through complete save reconstruction using valid frame and container CRCs and still credits partial verification. See `verify-probe.log`.

Impact: the frame and burst timing gate cannot establish that every programmed byte was verified by the reported durable time. A missing verification tail can pass. This is an acceptance-evidence defect, not a claim that the shipping verification loop actually skips its tail: `nvm_store.c:1128` compares each chunk and promotes only after reaching `wlen`.

Required outcome: preserve read/write ordering in the trace and grade unique byte coverage read after the relevant programming and before the next save. Pre-program blank checks and repeated reads must contribute no unverified bytes. Correct the durability description and regenerate or regrade the affected timing evidence at both points.

Verification: reject absent, partial and duplicated post-program coverage, including a blank check merged across programming; accept complete post-program coverage. Apply these controls through full save reconstruction and the binding/burst gate. A passing synthetic self-test that intentionally merges across programming does not resolve this counterexample.

**F3 — MINOR — Docs — The revised store README reports obsolete numerical test coverage.**

Artifact: `sw/firmware/ctrl_nvm/README.md:589` and :762.

Authority/evidence: the changed text claims 81 checks / 136 tests and 152 planted defects plus five controls. At the reviewed head the main suite declares 95 checks: 67 on both ports, 16 on the direct port, five on the command port, five codec checks and two flash-mock checks, totaling 162 tests per shape. The executable mutation registry has 184 defects plus five controls, totaling 189. See `audit_public.py` and `public-audit.log`; the published gate receipt likewise reports 162 and 189.

Impact: the authoritative suite description misstates the numerical evidence another reviewer is asked to assess. This is MINOR rather than RESIDUE because it changes test/coverage figures under the supplied classification rule.

Required outcome: correct both totals and their breakdowns, or replace the duplicated counts with an exact reference to executable enumeration and the current receipt.

Verification: compare the updated prose with the main suite test listing and mutation/control registries at the corrected head. This finding does not allege that the executable registry omits the extra tests.

**Reviewer-owned coverage ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1, F2 | #1009 ruling; REQUIREMENTS.md; SAVED_STATE_MATERIALIZATION.md:2394 and :2396; SAVED_STATE_FORMAT_32X32.md; nvm_store.c:266, :915, :987, :1261; binding registration and window tests | R932-1 | 166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e |
| RTL | UNCLEAN — F1 | Complete 49-file diff contains no HDL change; nvm_store.c state machine and flash/state interfaces; ctrl_plat binding registration; ctrl_loop service share; nvm_shape.h; ctrl_memory.py and public ledger/image receipts | R932-1 | 166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e |
| Robustness | UNCLEAN — F1, F2 | nvm_store.c:287, :623, :1006, :1058, :1128; test_nvm_delta.cpp:140, :237, :276, :453, :486, :511, :541; test_nvm_window.cpp; maintenance and partial-verification probes | R932-1 | 166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e |
| Tests | UNCLEAN — F1, F2 | All changed store tests, fixtures, rig and mutation registry; save_burst.py; bind_save.py; selftest_bind.py and selftest_burst.py; coverage ratchet and published coverage exclusions; independent probe receipts | R932-1 | 166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e |
| Docs | UNCLEAN — F1, F2, F3 | Changed store/format/materialization/memory documentation, documentation audit, PR body, published author packet; source-comment delta inspected against the owner rule | R932-1 | 166dfdc9fd2f22a9d2acd272bac4d1a5e3462f3e |

Coverage here means the lens was applied; it grants no clean coverage while its findings remain open. No RESIDUE or SUGGESTION is filed. Existing source-comment residue tracked by #746 was not re-filed. Runtime memory-ledger debt strings are not source comments.

The normal-path examination found the delta target remains the older slot; the frame carries the union of that slot lag and newly captured bytes. CRC, sequence, bounds and page-rounded room checks precede replay/promotion. Unknown lag, previous-minor containers, poisoned/torn tails, oversized frames and full room fall back to a whole save. Blank checking and complete production read-back remain present. The newer slot stays authoritative until verified promotion. The two-slot tradeoff and full-room maintenance add eventual erase wear; the binding burst evidence reports six frames and zero erases, not indefinitely erase-free operation.

Window arithmetic uses the earliest due time rather than restarting on later dirties. Binding-range classification, first and last binding IDs, records around the range, mixed-class shortening, capture joins, changes after capture, and the 64-change burst were examined. Other-class in-flight behavior retains the previously ruled first-idle treatment. `test_nvm_delta.cpp:511` exercises the recorded 2509db68 stores at both AX7101 shapes, booting the newer state, rewriting both old-minor slots whole, then appending a frame. The cut sweep at :541 covers 0–3 s every 10 ms plus media-effect start/mid cuts, for frame, whole and post-maintenance paths. It requires old or new, never neither, new from 250/800 ms onward and a subsequent successful save. These are modeled cuts from a change event; they do not substitute for response-referenced physical power cuts.

**Evidence and execution limits**

The [published author packet](https://github.com/kebag-logic/milan-fpga/tree/e1ce9b2b0ebab8205440b0a99026fdb7d4aa6b2e/review-evidence/p1save-r1/author) is the source execution evidence. `audit_public.py` verified all 13 published files against the packet manifest. The gate receipt identifies earlier execution commits and subsequent test/document updates; it is not uniformly a new run of every bank at 166dfdc9. The separate firmware identity receipt ties the routed firmware bytes to the final head. The published coverage is 679/679 store lines and 435/444 raw branches, with nine excluded, yielding 435/435 eligible branches. These figures and 189 caught planted defects do not cover the combined state in F1 or invalidate F2.

Independent completed checks:

| Check | Result | Receipt |
|---|---|---|
| Unmodified main store suite, all five shipped shapes | PASS, 162 tests per shape; 810 test instances | native-main.log / .rc; collect_native.py |
| Maintenance/captured-change fault probe | Reproduced F1 on both ports at both AX7101 shapes; eight failed contract checks and four passing empty-maintenance controls | tidy-probe.log / .rc; probe_tidy.py and probe_tidy.cpp |
| Partial post-program verification probe | Reproduced F2; negative and complete-read controls checked; valid-CRC full reconstruction also accepts the partial verify | verify-probe.log / .rc; probe_verify.py |
| Memory policy and its negative controls | PASS in the existing project environment; initial default environment failed to import migen | memory-project-env.public.log / .rc; memory.log / .rc |
| Published evidence hashes and executable counts | PASS, 13 files; 184 defects plus five controls | public-audit.log / .rc; audit_public.py |

The main-suite binaries were built from this unchanged checkout by the concurrent campaign. Their hashes and explicit execution results were collected separately with two workers, without another build. The source campaign used 12 build/mutation jobs, the grader self-test one worker; this collection kept the combined total below 16. All disposable files are under packet/scratch. Reproduction-driver exit 0 means the counterexample was reproduced, not that its contract passed; RECEIPTS.md explains the statuses.

The optional full store mutation rerun and full timing-grader self-test are INCOMPLETE. The foreground driver exited 1 with a timing-grader TimeoutExpired at 1,800 seconds; neither campaign returned a completion verdict or status file. No full pass is credited to either rerun, and this review does not claim an independent rerun of all 189 planted defects or the entire grader self-test. Their partial raw output is retained in store.log and budget-selftest.log; campaign-status.txt records the limit and verifies that no live campaign process remained. The main-suite results above completed separately. These execution limits do not leave a review lens unapplied; all five lenses were examined and the negative findings have completed reproductions.

The public CPU/save receipt grades six save groups at each point. It reports zero per-pass-share violations among 11,148 work passes at 1x1 and 14,740 at 8x8/one interface, with a 2 ms share. Longest store steps are 79,554 and 80,763 CPU cycles respectively. Its modeled frame times are 116.067 / 134.280 ms and whole times 305.153 / 561.489 ms; the 64-command burst figures are 46.867 / 155.319 ms. The two frame/burst conclusions remain subject to F2. Other-class burst/flight figures remain below the stated five-second target. These selected groups do not establish the full last-notice 140 ms, ACMP 30 ms, or load bounds 0.70 at 1x1 and 0.76 at 8x8/one interface. No full source CPU bank was independently run or inferred.

| Platform point | ROM bytes, base → head | SRAM bytes, base → head | Planned RAMB36, base → head |
|---|---|---|---|
| 1x1 / one interface | 127,568 → 130,000 | 56,736 → 56,816 | 45.5 → 46 |
| 1x1 / two interfaces | 129,352 → 131,784 | 59,168 → 59,248 | 46.5 → 47 |
| 8x8 / one interface | 141,680 → 144,112 | 100,096 → 100,176 | 59.5 → 60 |
| 8x8 / two interfaces | 143,432 → 145,864 | 117,632 → 117,712 | 64.5 → 65 |

The +2,432 ROM / +80 SRAM / +0.5 planned-tile increments reconcile across the platform ledger. The two-interface 8x8 declaring-outputs fixture needs 62.5 tiles (137,344 ROM bytes), while its other arms remain 62.0. The raised fixture entry and S14 debt are permitted by the owner rule; an earlier refusal in the packet is not the final ledger result. The independent memory-policy check passed in the project environment.

Routed totals grow 80.5 → 82 at 1x1 (+1.5), and 98.5 → 99.5 at 8x8/one interface (+1.0), versus +0.5 planned at each. The remaining +1.0 / +0.5 tiles are unattributed in the supplied evidence and remain a manager acceptance item, not a claimed saving. Published chosen-route slow setup margins are 0.185 / 0.050 ns and fast hold margins 0.036 / 0.036 ns; these are receipt claims, not routes rerun by this reviewer. The 8x8/two-interface platform ledger is not a routed timing result.

Physical calibration is NOT RUN. Field skips are not hardware proof. Response-referenced power cuts, the four board cases including full room, burst/wear and other-class acceptance, and the stated physical latency gates remain owed. No manager source bank exists at this exact head, and none is claimed. Hosted/local acceptance belongs to the manager; this report does not treat skipped contexts as executed checks. The final current-dev merge candidate is a distinct validation object: source base `5de21ff3661436ea5598718aca36934361e35340`, supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`. The manager must build and validate that candidate and publish its required receipts at the merge turn, reconcile full CPU and routed-resource acceptance, complete the applicable gates, and obtain corrected-head independent reviews. No completion or merge is released by this report.

Final integrity: PASS in integrity-final.log / .rc. The exact head and tree, all 1,979 superproject tracked blobs, executable/symlink modes, complete index entries, and the four required registered submodule gitlinks and their tracked bytes/modes/indexes match the reviewed commits. The checkout status is clean. No campaign process remains. The prior-public-finding check was repeated at finalization and remained empty. The raw memory receipt is retained locally; its public copy redacts only a home-directory prefix, with the original hash retained as explained in RECEIPTS.md. MANIFEST.sha256 enumerates every publishable receipt and script using paths relative to this packet. The scratch directory and unlisted raw memory receipt are not for publication.

R932-1 FINISHED

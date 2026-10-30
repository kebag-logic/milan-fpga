[R734] NEGATIVE - exact head ac105b158bb740a65e0154305377fd4a7d0f6f87

The three prior source/test defects are resolved at this head. No new blocking source defect was found in the delta. This report nevertheless cannot clear the required external independent review: the findings-only access separation was breached during this session (R734-2-P1 below). The executable receipts remain useful evidence. No author code change is requested for that procedural finding.

Scope and authority

Round R734-2 examined the six commits after `99de3a023abfda5604a70832e23baf7ff73481a3`, within PR #811's change from source base `f4c9ad4f06f185378fd2646298aab51dd108e86f`. Reviewed head/tree: `ac105b158bb740a65e0154305377fd4a7d0f6f87` / `10a286051e8aa59003bfac98cf4f7d5973d241f9`. The delta changes 29 files; untouched code retains its prior technical disposition unless affected by this delta.

Reconstruction began with AGENTS.md, CONTRIBUTING.md and docs/README.md, then the issue and public scope decisions, requirements/interfaces, change inventory, history and delta. Authorities include [the frozen assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6493622258), [D3/D6](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409738976), [the four accepted limitations](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6505997821), and [the correction assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6508869822). Repository authorities examined include REQUIREMENTS.md section 1, FR_NFR.md section 3.4, ARCHITECTURE_HW_SW_SPLIT.md section 2, SPLIT_CONTROL_MEMORY.md section 5, and acmp_nvm.h's boot-order contract. No new interpretation of an IEEE/Milan clause is proposed.

Prior findings: disposition at this head

| Finding | Prior severity / lenses | Result and evidence |
|---|---|---|
| R734-F1 | MAJOR; Conformance, Robustness, Tests | RESOLVED. `tb/verilator/ctrl_split_boot/run.py:248` checks native status and tally; `saved_status()` and `point()` preserve the same decision for regrade. Original `probe_boot_exit.py` now rejects the defect in both paths and keeps the passing control. `boot-exit.log`, `native-mutants.log`, `native-edges.log`, and completed boot receipts support closure. |
| R733-F1 | MINOR; RTL, Robustness, Tests | RESOLVED. `ctrl_plat_console.c:133` stops before crossing the command terminator. `test_plat.cpp:160` supplies NUL lines; `plat_arms.py:40` enables AddressSanitizer. The original probe is clean on the fixed source and produces `global-buffer-overflow` on the revert. The shipped revert is killed by K3. See `nul-probe.log` and `new-mutants.log`. |
| R733-F2 | MINOR; Tests | RESOLVED. `test_plat_boot.cpp:208` requires flash accesses before the mailbox's first access. B10 at line 378 injects an actual mailbox bind and observes its commit/program through the loop. Both original reviewer plants now fail the boot arm; the permanent plants fail B1/B10 by their required words. See `prior-boot-probes.log` and `new-mutants.log`. |
| R734-R1 / R733-R1 | RESIDUE; Docs | Source-comment cleanup RESOLVED. The earlier location list and all new non-Markdown lines were checked. No new forbidden lane/comment/reviewer label remains. Existing executable ledger reason strings were not treated as comments or changed. See `comment-audit.txt`. |
| R734-R2 / R733-R2 | RESIDUE; Docs | RESOLVED: the inaccurate “longer than any span here” comparison is removed from the boot README. |
| R733-R3 | RESIDUE; Docs | RESOLVED: the PR's simulation and CPU-budget figures state CPU 50 MHz / bus 100 MHz. |
| R733-R5 | RESIDUE; Docs | RESOLVED: the PR's coverage row now identifies the six otherwise unchanged files whose counts were re-recorded. |
| R733-R4 | RESIDUE; Docs | RETAINED as R734-2-R1 below. |
| R733-S1, S2, S3 | SUGGESTION | RETAINED below; their causes are unchanged by the delta. |

Executed verification

All 15 top-level command receipts returned zero; negative probes assert the expected failing child result. Commands are retained in the scripts, `.command` files and logs. The foreground campaign driver waited for every child; no execution remains running.

| Check | Result | Receipts / reproduction entry point |
|---|---|---|
| Firmware self-test, four shards, RV32 required | PASS all four shards. Shard 1 caught 568/568 mutations; shards 2 and 3 passed their AECP and SRP campaigns, including the two pin controls. Normal platform, AddressSanitizer, boot/interface, image and CSR-trace checks passed. | `run_campaigns.py`, `firmware-shard{0,1,2,3}.command`, corresponding `.log` and `.rc` |
| Original native-exit probe | Passing native control preserved; nonzero native exit rejected in normal execution and regrade. | `probe_boot_exit.py`, `boot-exit.log` |
| Native-grader discrimination | Six of six mutations caught; eight independent edge cases produced the required decisions. | `native_mutants.py`, `native-mutants.log`, `probe_native_edges.py`, `native-edges.log` |
| Original NUL-line probe | Fixed source exits zero; reverted guard produces an AddressSanitizer global-buffer-overflow. | `r733_console_nul.c`, `probe_nul.py`, `nul-probe.log` |
| Three permanent new plants | Command overread, saved-state ordering and unbound store service all caught by K3/B1/B10. | `plat_quick.py`, `new-mutants.log` |
| Original saved-state and store-service probes | Both original plants now fail the boot arm at the intended assertions. | `r733_escape_check.py`, `r733_plat_campaign.py`, `prior-boot-probes.log` |
| Positive 1x1/1if boot and saved-evidence regrade | Both PASS: ready at **84.383 ms**, **4,219,150 CPU cycles at CPU 50 MHz / bus 100 MHz**. Native exit zero, one check, zero failures. | `run_boots.py`, `boot-1x1.log`, `boot-1x1-regrade.log`, `raw-boot/1x1/` |
| Positive 8x8/1if boot and saved-evidence regrade | Both PASS: ready at **184.647 ms**, **9,232,360 CPU cycles at CPU 50 MHz / bus 100 MHz**. Native exit zero, one check, zero failures. | `run_boots.py`, `boot-8x8.log`, `boot-8x8-regrade.log`, `raw-boot/8x8/` |
| Existing boot plants and native controls | Six of six native controls correct; two of two boot plants caught in completed native runs. Skipped CSR write fails TRACE; blocking console fails UART. Both native processes exit zero with one check and zero failures, so neither plant is caught merely by NATIVE. | `boot-plants.log`, `raw-boot/csr-write-skipped/`, `raw-boot/console-blocks/` |
| Final checkout restoration | Exact head/tree, 2,678 tracked blob bytes and modes across the root and five required submodules, index and gitlinks verified. Root status empty and diff whitespace check clean. | `verify_checkout.py`, `integrity-before.log`, `integrity-after.log`, `git-final.log` |

The scoped simulator identity was checked before execution (`tool-identity.txt`). Campaign parallelism stayed within the permitted limit; native compilation used `make -j16` after the firmware campaigns completed. All disposable mutations and build products reside under `scratch/`.

All timings in the boot evidence are simulated time at CPU **50 MHz**, bus **100 MHz**. Both newly linked one-interface images are byte-identical to the published exact-head images (`image-clock-comparison.txt`). The platform memory figures remain 39.0 / 42.0 / 52.0 / 59.0 RAMB36 at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if. The final point is the explicitly ledgered exception, not a fit within 56. These are planned allocations, not routed utilization. The published image/part receipts support the updated ROM increase and section 5's figures.

The original native-exit probe exercised the unchanged normal/regrade entry points. Six mutations independently removing status/tally/save/regrade checks were all caught by the new native controls. Eight additional probes covered a valid control, nonzero status with a good tally, failed tally with exit zero, absent tally, zero measured checks, truncated tally, a failure marker, and invalid saved status. Each failed case is rejected for NATIVE, with normal/regrade agreement where applicable.

Published evidence

All **799** `published_sha256` entries in the supplied [archive](https://github.com/kebag-logic/milan-fpga/tree/06c6f5d97328e8c4c684314df156d02637224341/review-evidence/665s3-r1) were verified. The archive commit has no signature field and no detached signature was located; this is hash-integrity verification, not cryptographic signature verification or proof that a receipt was executed. See `verify_packet.py` and `packet-verification.txt`.

Spot-checks covered exact-head author receipts for the four firmware shards, boot points/regrades/plants, image plans/refusals, coverage, memory mutants and builder result. The builder receipt explicitly has calibration gate 11 **NOT RUN**. No manager source bank at this head is claimed or inferred. Broader source-gate claims here are attributed to those author receipts, not to a reviewer rerun. The source receipts do not validate a future merge result.

R734-2-P1 — MAJOR — Docs — required review access separation was not maintained

Artifact: this review procedure; the public PR comment retrieval containing prior review bodies [6508854695](https://github.com/kebag-logic/milan-fpga/pull/811#issuecomment-6508854695) and [6508864388](https://github.com/kebag-logic/milan-fpga/pull/811#issuecomment-6508864388).

Authority/evidence: the assignment prohibits reading another reviewer's report before this review's verdict and ledger, allowing prior public findings only after the independent diff pass. The independent delta inspection preceded retrieval, but the response bundled full prior review bodies, and prior result/ledger text was exposed before this verdict and ledger were written. No current-round review or private author material was consulted. This is a session-procedure failure, not a defect introduced by the author.

Impact: this report must not count as the required external independent positive review, despite the successful technical checks.

Required outcome: obtain a replacement cleared-context external review that writes its own verdict and ledger before consulting other reports and confines any earlier consultation to the permitted prior findings. No source edit is required by P1.

Verification: the manager records that replacement review and its exact-head coverage before counting the external approval. The commands and raw receipts here can be reproduced independently.

R734-2-R1 — RESIDUE — Docs — qualify the allocation comment to interface 0

Artifact: `sw/firmware/ctrl/plat/ctrl_plat.c:64-65`, retained R733-R4.

Authority/evidence: `window_read/window_write` only access interface 0's window, while allocation is recorded for each interface; `ctrl_plat.h` and B8 already describe this distinction. The comment's “no source” wording is broader than the already documented behavior.

Impact: wording only; no measurement, test, generated artifact, clause claim, privacy rule or implementation changes. This residue does not dirty a lens.

Exact required fix: replace the two-line comment with: `maap_allocation_fn: interface 0's window first, then the allocation ACMP's source port reports, so no interface-0 source reports an address the window does not hold. Interface 1 has no window (ctrl_plat.h).`

Verification: compare the revised comment with the interface guard and B8; preserve executable bytes.

Retained suggestions

- **R733-S1 — SUGGESTION — Tests.** Artifact: `ctrl_plat_console.h` response reservation and `test_plat.cpp`. Evidence: the unchanged widest status response fits the current reservation, but the prior reservation-understatement plant escapes. Impact: future response growth or a reduced reservation has weak direct coverage. Optional outcome: permanently test the widest formatted response against the reservation and plant an understatement. Verification: positive maximum passes and the understatement fails by that check. No new maximum-length claim is derived from this round's NUL fix.
- **R733-S2 — SUGGESTION — RTL, Tests.** Artifact: `ctrl_plat_csr.h:77`, `CTRL_PLAT_SNAPSHOT_SPIN`, and the immediate snapshot simulation. Evidence: the prior zero-wait plant escapes because the modeled snapshot is immediate. Impact: desk evidence does not prove the hardware wait. Optional outcome: retain this as a physical-integration check. Verification: measure snapshot readiness on the integrated target and demonstrate that insufficient waiting is detected. Hardware was not used here.
- **R733-S3 — SUGGESTION — Conformance, RTL, Docs.** Artifact: `ctrl_plat_csr.c`, `ctrl_plat.c:185`, `plat/README.md` boot step 3, and the frozen exact-policy-write acceptance. Evidence: the unchanged policy writes the fabric MAAP enable before the one-owner report clears it. Impact: integrated startup behavior needs an explicit disposition; this delta does not change the frozen write sequence. Optional outcome: document that transient enable and obtain the integration decision on clearing it in split policy. Verification: integrated register/wire startup evidence under the resulting decision. No claim of hardware safety is made from the stand-in CSR trace.

Reviewer-owned ledger

Every lens was applied to the delta. The four CLEAN rows below are technical results; P1 prevents this ledger from clearing the independent-review bar. Unchanged code retains its earlier disposition only where the reviewed delta does not alter its dependencies.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_plat.c:252-273`, `acmp_nvm.h` boot-order contract, architecture section 2; B1/B10 and both saved-state plants; `ctrl_split_boot/run.py` native completion and boot gates; frozen scope exceptions | R734-2, technical coverage subject to P1 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |
| RTL | CLEAN | `ctrl_plat_console.c:129-138` indexing/termination; `ctrl_plat.h`, `boot_soc.py:70-80`, copied CPU inputs and exported clocks; image hashes/plans; no changed HDL, CDC, product clock or gitlink | R734-2, technical coverage subject to P1 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |
| Robustness | CLEAN | NUL probe/fix/revert; `run.py` native status, incomplete/failed/zero tallies and saved-status failure paths; positive controls and regrades; firmware refusal/backpressure arms | R734-2, technical coverage subject to P1 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |
| Tests | CLEAN | `plat_arms.py`, `plat_mutants.py`, `test_plat.cpp`, `test_plat_boot.cpp`; K3/B1/B10 discrimination; six native-check mutations; original probes; four firmware shards; both positive boot points and both completed boot plants | R734-2, technical coverage subject to P1 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |
| Docs | UNCLEAN (P1) | Required independent-review procedure; current platform/boot READMEs, memory section 5, ratchet, public scope/PR text, published receipts and comment cleanup otherwise checked; R1 is nonblocking residue | No clean covering round for P1 | `ac105b158bb740a65e0154305377fd4a7d0f6f87` |

Limits and pending manager duties

- Replace this external review as specified in P1; obtain the other independent verdict and reviewer-accepted final coverage ledger. No merge is authorized by this report.
- The source base is `f4c9ad4f`; the supplied live-dev tip is `1e80128f0a467b58bf884b7d9bf62e013a2fb141`. The manager must build and validate the actual current-dev merge candidate, publish its builder/native-bank receipts, accept hosted/local workflow evidence, and perform post-merge containment. None of those duties was executed or inferred here.
- No full parent/processor/gPTP/Yosys/builder bank, hosted job audit, local workflow replica, route, hardware run or shared installation was performed by this reviewer. No GitHub write, source commit, push, merge or author contact occurred.
- The boot uses a stand-in CSR window, blank flash and simulated UART. It proves firmware behavior in that composition, not datapath effects, serial baud timing, valid/torn/wrong-version journal restoration, gPTP interoperability or physical boot. Physical calibration remains NOT RUN; field skips are not hardware proof.
- The accepted deferrals remain: grader split modes, live SRP configuration, hosted boot recipe integration, named memory exception/hybrid XIP, and the documented target-face/flash/observation limitations. Existing CPU-budget misses are not discharged by this delta or by a successful console boot.
- Disposable CPU data, builds and mutation copies are confined to `scratch/`. Final tracked bytes, executable modes, index and all five required initialized gitlinks are verified independently of status flags; `external` remains intentionally uninitialized. Receipts are listed in `MANIFEST.sha256`; scratch is excluded.

R734-2 FINISHED

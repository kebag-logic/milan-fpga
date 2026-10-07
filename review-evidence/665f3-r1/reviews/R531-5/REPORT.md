[R531] POSITIVE - exact head 13e715136b0b7c8d9763e0b730d9709f2c9f5932

R531-5, external independent review of issue #665 / PR #688. All five lenses are CLEAN at this head. No open BLOCKER, MAJOR or MINOR was found or carried forward. One previously reported historical wording RESIDUE remains, with its exact correction below. This is a source-review verdict; merge acceptance and physical calibration remain separate.

Tree: `4b04d6dd962ddf0daee9cf64fc23abf5fb18f927`. Reviewed range: `021b9c1fb966e9a1a4acef6b5233edd3518f32a0..13e715136b0b7c8d9763e0b730d9709f2c9f5932`. The head contains the assigned merge of dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`. `source-scope.txt` records the history and inventories against both bases.

**Scope and reconstruction**

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README, the public issue and frozen scope decisions, requirements/interfaces, the diff and history, then public evidence. The independent verdict and ledger were written in `independent-pass.md` before prior review reports were read. Earlier findings were then checked against this head. No private author material, lane scratchpad, management checkout, or concurrent reviewer report was used.

The task is lane F3, not completion of every lane of #665. The controlling public decisions are:

- [Frozen F3 acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6026721148): Milan listener/talker connection management, discovery, persistence, ordered responses/notifications, bounded service, static bare-metal implementation, interface isolation, executable tests and fault controls.
- [Bound-talker admission](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6029368753): admit the bound talker's AVAILABLE/DEPARTING on the receiving interface; preserve the mailbox contract and close the co-simulation rebuild gap.
- [Linked-image acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), [area disposition](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6033962557), [timer/interface corrections](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6034423349), and [pinned RV32I link ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6036721467).
- [Round-6 composition assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6037650104): retain both F2/F3 sides, compose ADP/ACMP/MAAP with disjoint slots and every channel enabled, test attachment/refusals, and report both linked shapes against dev.

Authorities examined include REQUIREMENTS.md section 1; `docs/reference/FR_NFR.md:321,333` (NFR-SCOUT and H-ACMP/H-DISC); `docs/design/MAILBOX_SPLIT.md`; `docs/reference/MAILBOX_CONTRACT.md`; `sw/mailbox/mailbox.yaml`; the ACMP, MAAP, loop and saved-state public headers. The normative references are Milan v1.2 section 5.5 and 5.6.4/Table 5.54, and the cited IEEE AVTP/version and ACMP field/status clauses. I checked the repository's clause mappings and the recorded scope rulings. The original Milan v1.2 PDF could not be retrieved during this review; I do not claim a fresh full-text audit of the external standard.

The supplied immutable [c961acab packet](https://github.com/kebag-logic/milan-fpga/tree/c961acabf3a36cb17085868b5c0f779145cf97aa/review-evidence/665f3-r1) describes the original round-1 execution at `351ae81f`; it is historical evidence. The current [round-6 public handoff](https://github.com/kebag-logic/milan-fpga/blob/16497e023fd082b4dd8e9f57969d4f3b47ef053a/review-evidence/665f3-r1/author-r6/HANDOFF.md), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6040171459) and PR body were also examined. `public-evidence-extract.txt` preserves the current handoff's scope, gate table and limits. Its 465-defect campaign and mailbox campaign ran at `d7e5fee5`; the only subsequent change is the coverage-exclusion count in the harness README, whose consumers were rerun. Those reported full campaigns are distinguished from this review's focused executions.

**Applied lenses**

[R531] PASS Conformance - `sw/firmware/ctrl/acmp/acmp.c:661,749,995,1040,1090`; `acmp.h`; `test/acmp_walk.cpp`; `app/ctrl_app.c:12,32,54`; `docs/reference/FR_NFR.md:333`; issue scope decisions - Checked listener bind/unbind/get-state and probe/retry transitions, consumer UID/sequence guards, talker response fields, discovery restart/aging/interface/GM guards, boot restoration and notification ordering against the frozen contracts. The accepted send starts the full 200 ms interval, including duplicate and deferred probes. The ADP admission table follows each binding and receiving interface. The assigned three-module composition retains both sides, opens every attached channel and uses separate timer runs. The linked-image requirements reproduce at both shapes. The processor differences LD1-LD3 are executed comparisons; TD1's processor side remains explicitly source-read evidence under the recorded 5.5.2.7/5.5.4.2 ruling.

[R531] PASS RTL - `hdl/milan/mailbox/KL_mbx_rx.sv:217`; `hdl/milan/mailbox/KL_mbx.sv:118`; `sw/mailbox/mailbox_skeleton.py`; `sw/firmware/ctrl/app/ctrl_app.c:12`; `sw/firmware/ctrl/loop/ctrl_loop.c`; `mailbox.log` - Examined bound-entry readback validity, reset masking, byte order, serial compare flags, copy suspension/restart, latched frame interface and per-interface owed flags. No new clock crossing is introduced by the table. Checked firmware slot bounds, static state, callback order, bounded loop work and composed IRQ/filter wiring. Both bus adapters pass at one and two interfaces; the model and firmware/RTL co-simulation pass. The independent linked-image audit confirms RV32I/ILP32, resolved symbols and section accounting. The accepted +357 LUT/+86 FF area result is public evidence, not a measurement rerun here.

[R531] PASS Robustness - `sw/firmware/ctrl/acmp/acmp.c:251,661,995,1040,1159`; `acmp_mbx.c:68`; `test/test_acmp.cpp` A19/A24/A26-A30; `test/test_acmp_mbx.cpp:416,923,1002,1065`; `test/test_acmp_nvm.cpp:250`; `tb/verilator/mbx/suite.hpp:1562` - Applied malformed/version/length, unknown state/identity, full-queue, cancellation/rebind, wrap, reset, duplicate and feature-disabled checks. Slot rejection precedes narrowing; restored bindings survive the D3 rollback. U6/U7 cover coexistence, attachment order and refusal without opening hardware; F6 bounds the composed pass with events and ACMP/MAAP backlogs. Q22/Q23 cover adjacent frames and owed-copy isolation. Fresh image self-checks reject foreign ABI/ISA, weak undefined references and recursive helpers.

[R531] PASS Tests - `sw/firmware/ctrl/test/ctrl_reuse.py:64`; `test_acmp_mbx.cpp:923,1002,1065`; `acmp_review_mutants.py:338`; `ctrl_mutants.py`; `maap_mutants.py`; `sw/firmware/gtest/README.md:306`; `tb/verilator/mbx/Makefile`; `mutation-results.json` - Examined test oracles, processor-stimulus extraction, assertion-specific mutation grading, preservation of both arm/defect sets, and the two explained changes to mutation expectations. Executed eight focused firmware arms, real mailbox RTL/model/co-simulation, contract checks and 21 selected planted defects. Every selected defect is caught at its required test/assertion, not accepted merely because a build fails. Coverage exclusions for composition attachment failure follow the public preconditions and actual available sink/poll/channel capacity; the manager's full 100% ratchet run was not repeated here. The image self-test passes 33 checks, with an additional independent final-ELF audit importing none of the candidate auditor.

[R531] PASS Docs - `sw/firmware/ctrl/README.md:83,285`; `sw/firmware/ctrl/acmp/acmp.h:425`; `sw/firmware/ctrl/maap/README.md`; `docs/design/MAILBOX_SPLIT.md:629,692,949`; `sw/firmware/gtest/README.md:306`; current public handoff/PR - Contracts and examples reflect the actual composition, accepted-send timeout, one-frame poll, discovery filter and persisted-record behavior. Linked section figures, helpers, compiler identity and base deltas reproduce. Two-module and three-module backlog bounds are labelled separately and numerically consistent. Co-simulation's two-module scope, model-only three-module integration, stack/pool exclusions and unmeasured physical time are disclosed. Documentation and bare-metal gates pass. The historical wording residue below does not alter the current measured table or its audit evidence.

Unless fully qualified above, ACMP and test paths are under `sw/firmware/ctrl/`.

**Independent execution receipts**

| Executed here | Result | Publishable receipt |
|---|---|---|
| Focused firmware: acmp, acmpif2, acmpwalk, acmpnvm | 84, 22, 127, 7 tests PASS | corresponding `.log` / `.rc`; `focused-results.json` |
| Preserved firmware: model, maap, maap_if2, unit | 23; 37 + 12; 13; 24 + 2 tests PASS | corresponding `.log` / `.rc` |
| Mailbox Wishbone / AXI4-Lite | 382 / 427 checks PASS | `mailbox.log`, `.rc` |
| Two-interface Wishbone / AXI4-Lite / model | 384 / 429 / 369 checks PASS | `mailbox.log`, `.rc` |
| Firmware/RTL co-simulation | 32 checks PASS | `mailbox.log`, `.rc` |
| 15 new composition defects, 4 adapted defects, 2 filter controls | 21/21 caught | `mutation-results.json`, 21 `mutation-*.log` files |
| Generated mailbox crosscheck and generator self-test | PASS | `contract*.log`, `.rc` |
| Fresh digest-verified pinned SDK extraction | PASS | `sdk.log`, `.rc` |
| Linked images, both shapes and dev base | PASS; exact public totals and head ELF hashes | `image.log`, `.rc`; `independent-image-audit.json`, `.rc` |
| Linked-image self-test | 33 checks PASS | `image-selftest.log`, `.rc` |
| Bare-metal and documentation gates; diff whitespace check | PASS | `baremetal.log`, `docs.log`, `diff-check.log`, corresponding `.rc` |
| Raw bytes, modes, index and required submodules | PASS before and after | `integrity-before.json`, `integrity-after.json`, `final-worktree-status.txt` |

The scoped simulator's identity was checked before use: version 5.050, revision v5.050 (`compiler-identity.log`). The SDK archive digest is `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`; GCC 14.3.0, build `2021.11-18033-g83947c7bb6`; unlinked libgcc digest `d8ebca8cf6ad31cd50695f79e91e86a716d3b1761fbbefd5ee7b0627a2d0af58`.

| Linked shape | Inputs/outputs | text | rodata | data | bss | total | dev total | delta | of 131,072 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `endstation_ax7101_1x1_tdm8` | 2/2 | 33,444 | 748 | 0 | 12,416 | 46,608 | 30,960 | +15,648 | 35.6% |
| `endstation_ax7101_8x8` | 9/9 | 33,448 | 748 | 0 | 22,784 | 56,980 | 41,332 | +15,648 | 43.5% |

The independent audit checks ELF32 little-endian executable/RISC-V headers, flags 0, architecture `rv32i2p1`, final undefined symbols, and a complete no-alias disassembly against the RV32I base mnemonic set, accounting for every executable byte. Counts are 8,361/8,362 words at the head and 5,669/5,670 at the base. The candidate also audits input objects for weak unresolved references. Helpers are 508 bytes and runtime stand-ins 64 bytes. The composed app is 7,904 bytes: ACMP 4,720, MAAP 1,104, loop 1,748, pool 204 and ADP 124. This is section accounting of the disclosed measurement fixture; it excludes the stack and final integration owners/pool sizing.

**Prior public findings: explicit disposition at this head**

Read after the independent pass: PR comments [6029581606](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6029581606), [6030054402](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6030054402), [6034240520](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6034240520), [6034419826](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6034419826), [6036619302](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6036619302), [6036713241](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6036713241), [6037644394](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6037644394) and [6037645915](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6037645915). No submitted review bodies or inline findings were returned. The table preserves the original severity/lens ownership; resolutions rest on examined current artifacts and the executions above.

| ID, original severity and lenses | Disposition and current evidence |
|---|---|
| R531-1-F1, MAJOR, Conformance/RTL/Robustness/Tests | RESOLVED. Both receive entries reject unsupported AVTP versions before decode (`acmp.c:1002,1050`); A26/B9 pass. |
| R531-1-F2, MAJOR, Conformance/RTL/Robustness/Tests; R531-2-F1, MAJOR, all five lenses | RESOLVED. `no_resp_from_send` invalidates the cached clock after accepted transmission; deferred probes match sink and sequence. A27/A30 cover immediate/deferred initial and duplicate sends, 199/200 ms boundaries and a clock advanced inside send; wrap/cancel/rebind cases pass. Access figures include the fresh clock read. |
| R531-1-F3, MINOR, Conformance/RTL/Robustness/Tests | RESOLVED. `acmp_mbx.c:71` uses the subtractive upper-bound comparison before narrowing. B7 passes legal/illegal, truncating and UINT_MAX cases at both interface counts. |
| R531-1-F4, MINOR, Docs | RESOLVED. `MAILBOX_SPLIT.md:663` gives the two-module owed bound as 9,108 accesses, 9.108 ms at 1 us, excluding wait for room; the separately labelled three-module bound is 14,220. |
| R531-1-F5, MINOR, Docs | RESOLVED. `acmp.h:425` promises at most one oldest owed frame per poll; A19/E2 and `acmp_poll` agree. |
| R530-1-F1, MINOR, Tests/Robustness | RESOLVED. The actual two-interface adapter arm passes 22 tests, including per-interface slots/admission/discovery/latency and composed operation. |
| R530-1-F2, MINOR, Tests | RESOLVED. A24 uses literal, one-flag-at-a-time 20-byte BINDING vectors and refuses other lengths; the core arm passes. |
| R530-1-F3, MINOR, Tests | RESOLVED. N7 proves a D3 rollback preserves bindings at the port and through real store boot; all seven NVM integration tests pass. |
| R530-1-F4, MINOR, Tests/Robustness | RESOLVED. A28 covers connection/discovery timers and earliest-deadline selection across 32-bit wrap; core arm passes. |
| R530-1-F5, MINOR, Conformance/Docs | RESOLVED. `MAILBOX_SPLIT.md:712`, `acmp_walk.cpp` and the PR distinguish LD1-LD3 executed differences from TD1's source-read processor behavior and record why 5.5.4.2 governs. The 127-test walk passes. |
| R530-2-F1, MINOR, Tests | RESOLVED. `suite.hpp:1562` Q22/Q23 grade the latched arrival interface with the next frame presented, and nonzero-interface owed-copy gating. Current mutation definitions target both mechanisms. Both adapters at both interface counts pass here; the public full campaign records all 147 caught. |
| R531-2-F2, MINOR, Conformance/Tests/Docs; R530-2-F2, MINOR, Conformance/Docs | RESOLVED. Both composed shapes and exact dev deltas reproduce with MAAP and ACMP linked; sections/static objects are reported explicitly. |
| R531-3-F1 / R530-3-F1, MINOR, Conformance/Tests/Docs | RESOLVED. Fresh pinned extraction, four successful links and independent ISA/ABI/section audits, 33 self-checks including incompatible-library controls, correct provenance and exact current table. |
| R530-2-F3, MINOR, Docs | RESOLVED. Table and open-item text agree: two-module access limits 0.89/0.44 us; three-module limits 0.57/0.28 us, respectively ACMP/ADP backlog. |
| R530-1-R1; R530-2-R1/R2/R3, RESIDUE, Docs | RESOLVED. Current design/README/PR name the implemented admission decision and accepted +357 LUT/+86 FF area result. Historical sections are labelled by round. |
| R530-3-R1, RESIDUE, Docs | RESOLVED. The PR title is “Mark II F3: bare-metal ACMP core on the mailbox”. |
| Earlier co-simulation relink obligation | RESOLVED. The Makefile tracks firmware headers and relinks when its archive changes; this review used a fresh export and passed 32 checks. A dirty-tree relink probe was not repeated here. |
| R530-4-R1, RESIDUE, Docs | RETAINED. The historical round-5 tool-selection sentence is copied into the public round-6 handoff at line 483. Exact correction below. |
| R530-2-S1/S2/S3, SUGGESTION | RETAINED as optional: publish detailed area excerpts; expand contract copy-window/general multi-interface bound wording; reconcile the area table's omitted small blocks. No lens effect. |
| R530-4-S1/S2, SUGGESTION, Robustness | RETAINED as optional: compare printed SDK identity with the pin; support isolated-interpreter invocation of the image command. The documented explicit-compiler command works. No lens effect. |

**Retained residue**

ID: R530-4-R1. Severity: RESIDUE. All attributable lenses: Docs.

Artifact: [public round-6 HANDOFF.md:480-483](https://github.com/kebag-logic/milan-fpga/blob/16497e023fd082b4dd8e9f57969d4f3b47ef053a/review-evidence/665f3-r1/author-r6/HANDOFF.md#L480), in its historical round-5 section; also the separate `author-r5/HANDOFF.md`.

Authority/evidence: the prior public finding records that the alternate build prints another identity but passes the audit with the same figures when no library is linked. The historical handoff still says its images “would fail the audit”. Current source, measurement, ISA audit and pinned-compiler instructions are correct; this retained tool-selection aside changes none of those executable outcomes or normative claims.

Impact: historical prose gives the wrong expectation for that optional local compiler selection. It does not invalidate the current pinned-compiler evidence.

Required outcome / exact fix: replace `and its images would fail the audit (as round 4's do)` with `and, since no library is linked, its images pass the audit with the same figures; only round 4's library-linked images fail it`. Apply to the surviving public handoff copies, or publish an explicit historical erratum.

Verification: inspect the corrected public text against the already published alternate-compiler receipt in R530-4. This round did not invoke an alternate compiler. Carry to the manager's residue checklist; it does not make Docs unclean under the assigned residue rule.

**Reviewer-owned ledger**

Every lens below was applied in R531-5 at the exact head. None is banked solely from an earlier verdict or from an unexecuted CI context.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue decisions; REQUIREMENTS.md; FR_NFR.md:333; acmp.c:661,749,995,1040; acmp_walk.cpp; ctrl_app.c:32; image.log | R531-5 | 13e715136b0b7c8d9763e0b730d9709f2c9f5932 |
| RTL | CLEAN | KL_mbx_rx.sv:217; KL_mbx.sv:118; mailbox.yaml and generator; ctrl_app.c:12; ctrl_loop.c; mailbox.log; independent-image-audit.json | R531-5 | 13e715136b0b7c8d9763e0b730d9709f2c9f5932 |
| Robustness | CLEAN | acmp.c:251,661,995,1159; acmp_mbx.c:68; A19/A24/A26-A30, B7/B9, N7, U6/U7, Q22/Q23; focused logs and image-selftest.log | R531-5 | 13e715136b0b7c8d9763e0b730d9709f2c9f5932 |
| Tests | CLEAN | ctrl_reuse.py:64; test_acmp_mbx.cpp:923,1002,1065; mutation definitions; gtest/README.md:306; mutation-results.json; mailbox.log; contract-selftest.log | R531-5 | 13e715136b0b7c8d9763e0b730d9709f2c9f5932 |
| Docs | CLEAN, historical residue carried | ctrl/README.md:83,285; acmp.h:425; MAILBOX_SPLIT.md:629,692,949; gtest/README.md:306; current handoff/PR; docs.log | R531-5 | 13e715136b0b7c8d9763e0b730d9709f2c9f5932 |

**Real limits and pending manager duties**

- Physical calibration was NOT RUN. Field skips are not hardware proof. Mailbox counts are analytic/model bounds, not measured target microseconds. The three-module pass limit is 1,580 accesses at one interface and 1,659 at two. Full ACMP/ADP backlog bounds of 17,380/34,760 accesses require at most 0.57/0.28 us per access for T_svc = 10 ms. A4 calibration, end-to-end H-ACMP wire timing and the F2-F5 bench acceptance remain pending.
- MAAP allocation reaches the stream-address port. Connecting it to ACMP's integrator-owned `source` destination state remains disclosed integration work. The RTL co-simulation composes ADP/ACMP; the three-module composition is exercised on the model at one and two interfaces. No target firmware execution or hardware acceptance is inferred.
- The linked image is a measurement fixture with stub owners, 64-byte runtime stand-ins, explicit arithmetic helpers and a temporary 256-byte pool arena. It does not measure the final stack, full F4 pool, all integration owners or the final platform runtime. It does not change the default-off mailbox or shipping image.
- The supplied manager full source-bank success is external evidence. This reviewer did not rerun the full parent/processor/gPTP/builder/synthesis banks, the full 465/147 campaigns, the store campaign or the coverage ratchet. The public handoff explicitly reports the store campaign as stopped with no verdict; its implementation/tests are unchanged from dev except documentation. Focused reviewer executions above are separate from those reported results.
- `hosted-checks.json` is an exact-head snapshot, not hosted acceptance. Completed successful jobs include firmware-unit, verilator-lint, bdd-conformance, changes, full-ci-gate, docs-check-no-git, wire-accountability and all four Yosys shards. Five Verilator shards, yosys-elaboration, elaborate and docs-check were still in progress. Physical gPTP was skipped. The manager owns hosted aggregate and local-replica acceptance; no polling loop or local replica was run here.
- The manager must carry the residue, obtain the other independent verdict and ensure no review remains in flight, validate the final merge candidate against live dev, obtain explicit merge authorization, and perform post-merge containment/public workflow updates. Source validation against FC is distinct from that current-dev candidate. This verdict grants no merge authorization and does not close the multi-lane issue.

**Reproduction and integrity**

`REPRODUCE.md` gives the exact focused commands. Portable drivers and execution receipts are listed in `MANIFEST.sha256`. The mailbox log replaces only its host-specific compiler installation prefix with `$SIM_ROOT`; its original remains in unpublished scratch. Independent work within each campaign/build group ran concurrently, using at most twelve firmware compiler jobs or the mailbox `make -j16` with bounded inner builds. Every driver waited for its children in the foreground. No build remains running. SDK extractions, probe copies and builds stayed under this packet's unpublished `scratch/`.

No candidate source was edited. Generated interpreter caches were removed. The final verification hashes raw bytes, checks executable/symlink modes, verifies the complete stage-zero index and checks required registered submodules. All 1,186 parent blobs equal the requested tree; the final worktree status is empty. Required gitlinks and submodule contents are exact: protocol processor `ead8036035affd53ef4b29979190f2f4f67084c0`, gPTP processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused external gitlink is unchanged and remains uninitialized.

No commit, push, GitHub write, merge, author contact, shared installation, privilege escalation or hardware action occurred. Only REPORT.md and the files listed in MANIFEST.sha256 are publishable; scratch is excluded.

R531-5 FINISHED

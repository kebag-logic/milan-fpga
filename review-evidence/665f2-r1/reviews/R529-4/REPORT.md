[R529] POSITIVE - exact head 5968967e19411428b71dde5c4712d4a8fa528cfb

R529-4 is complete. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains open on this delta. Two prose residues remain for the manager's checklist; neither changes the verdict.

Reviewed tree: `df2c47e21f7c068b245236ab477b5c6313036538`. Source base: `021b9c1fb966e9a1a4acef6b5233edd3518f32a0`. Authorized dev parent: `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`. Merge `d4bc335c20ad764fdcda7ebef6a6cd64dc60af93` has ordered parents `8b78a8fd36864246336c71c061ac4f21d629952f` and that dev parent, followed by two documentation commits.

The reconstruction followed the requested order: operating contract and contribution rules, documentation index, public frozen scope and decisions, requirements/interfaces, assigned diff/history, then executable evidence. Authorities include [F2 scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6026720272), [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6033552374), [linked-size addition](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), REQUIREMENTS product ownership, FR_NFR Sections 3.4.1/3.4.2, MAILBOX_SPLIT and REGISTER_MAP. The [public author-r4 archive](https://github.com/kebag-logic/milan-fpga/tree/d56236ac26ee2f7f5f01a8cfe5305ff19eec77b1/review-evidence/665f2-r1/author-r4) was read; both published document hashes match the executor's receipts.

Earlier reviewer reports were opened only after the independent verdict and five-lens ledger were written in [the checkpoint](receipts/independent-verdict-before-reconciliation.md). Six prior public rounds were then reconciled. Formal reviews and inline review comments were empty in the read-only inventory. No private author material or other active review report was used.

**Merge retention and check meaning**

The four conflict files preserve both sides: the MAAP arms, generated two-interface arm, normal/coverage dispatch, mutation partitions, ADP debug/release re-entry arms and assertion runtime allowance. The NVM erased-prefix sanitizer binary remains in the default and coverage gates. The assertion header matches dev.

The [catalog audit](receipts/final-campaign-audit.json) proves 196 unchanged definitions are the exact union of round 3's 193 and dev's 100. All 96 MAAP definitions survive. Seams, named tests and failure needles are unchanged. Four disjoint partitions each caught 49 controls. No named check was relaxed or accepted with a different failure meaning.

One build-profile distinction matters: the merged regular controller RV32 arm retains F2's `-DNDEBUG`, whereas dev had assertion-enabled objects. Its release scope is now explicit. I reran the same twelve-object arm with `-DNDEBUG` removed, preserving dev's debug ABI, dependency and static-frame checks. It passes. MAAP's debug object references `__assert_fail`, `__lshrdi3`, `__umodsi3`, `memcpy` and `memset`; the header supplies no assertion handler. This proves debug compilation only. See [debug receipt](receipts/debug-rv32.log).

[R529] PASS Conformance - `sw/firmware/ctrl/maap/maap.c:106`, `:185`, `:279`; `ctrl_app.c:34`; FR_NFR H-MAAP - preserved Annex B state/wire/timer behavior, original-deadline service checks, per-interface ownership and opt-in composition; linked-size acceptance examined separately below.

[R529] PASS RTL - `maap_csr.c:43`, `maap_mbx.c:94`, `tb/verilator/mbx/Makefile:44`; REGISTER_MAP:953,1086,1258,1541 - retained CSR direction, allocation ordering and mailbox integration. HDL, shipping firmware, configurations, builder inputs and gitlinks have no F2 delta against authorized dev.

[R529] PASS Robustness - `adp/adp.c:22`, `ctrl_nvm/nvm_klj2.c:299`, `test_maap_mbx.cpp:273`, `:324` - imported re-entry and erased-record protections survive the merge; malformed, stale, wrap, loss, backpressure and interface-isolation cases pass. Seven reviewer-defined faults are caught.

[R529] PASS Tests - `test_ctrl_firmware.py:86`, `:119`, `ctrl_mutants.py:515`, `fw_coverage.py:424`, `test_nvm_prefix.cpp:17` - both normal and measured populations execute; complete controller catalog, differential controls, exact-sized sanitizer checks and named-failure grading survive.

[R529] PASS Docs - `maap/README.md:144`, `:156`, `gtest/README.md:345`, `ctrl/README.md:58` - selector, assertion limits, retained arm inventory and coverage reasons agree with execution. Existing ADP exclusions now cite the enforced no-callback contract; thresholds and exclusion coordinates were not loosened.

**Executed evidence**

| Check | Result | Receipt |
|---|---|---|
| Controller gate, required RV32, complete mutation catalog | PASS; 196/196, including 96 MAAP; every partition runs all positive arms | `ctrl-shard-0.log`, `ctrl-shard-1-retry.log`, `ctrl-shard-2.log`, `ctrl-shard-3.log`; [audit](receipts/final-campaign-audit.json) |
| Coverage | PASS; 17 files at 100% lines/branches after existing exclusions; MAAP has no exclusions | [coverage](receipts/coverage.log) |
| Saved-state gate | PASS; 435 tests across five shapes, required RV32 builds | [NVM baseline](receipts/nvm-baseline.log) |
| Differential | PASS; 12 baseline cases and 16/16 named controls, including 1/500/600 ms probe defects | [differential](receipts/differential.log) |
| Mailbox | PASS; one-interface Wishbone 316, AXI4-Lite 361; co-simulation 13; two-interface 316/361/model 316; 5/5 controls | [mailbox](receipts/mailbox.log) |
| Four independent controller faults | All caught after clean controls: missing ADP gPTP guard, missing ADP stop guard, lost MAAP RX wake, interface-1 poll replaced by interface-0 poll | [fault definitions/results](receipts/probes.json), individual `probe-*.log` |
| Three independent erased-record faults | All caught: use total end instead of loaded end, allow eight-byte overread, reject exact payload end; positive exact-sized case passes | [results](receipts/nvm-probes.json), `nvm-probe-*.log` |
| Compiler selector | Documented variable selects the requested executable with absent and competing defaults; obsolete selector absent under sw/docs/scripts | [selector](receipts/selector.log), [scan](receipts/scope-and-retention.json) |
| Harness self-checks | RV32 17/17; coverage 28/28; tally/listener 18/18 controls | `rv32-selftest.log`, `coverage-selftest.log`, `tally-selftest.log` |
| Focused documentation/generation | docs check, Contents check, em-dash delta gate, mailbox generation/crosscheck all exit 0 | corresponding logs and command receipts |
| Exact restoration | Root 1,164 blobs; processor 558; gPTP 104; axis 214; bytes, executable modes, index entries and gitlinks match committed objects | [integrity](receipts/final-integrity.json) |

All log names above are under `receipts/`. Commands, durations and return codes accompany the coordinated gates. The simulator identifies as pinned version 5.050. Every campaign driver exposing jobs received an explicit bound; mailbox used `make -j16 VBUILD_JOBS=1`. Foreground coordinators joined concurrent children, with at most 16 compile workers and an observed unit peak of 5,763,059,712 bytes below its 12 GiB cap, with zero OOM events.

Two attempts reached the 570-second command limit: initial controller partition 1 and the inherited full 109-mutant NVM campaign. Those rc=124 receipts are retained and supply no pass. Controller partition 1 subsequently completed with all 49 catches. This review freshly completes the NVM five-shape gate and focused boundary probes, rather than claiming a fresh completed 109-mutant campaign. The manager's full source-bank evidence remains distinct.

**Linked RV32 composition**

The public report supplies text, rodata, data, bss, static pools and dev deltas for shipping and maximum shapes. Its archived directory exposes the handoff and PR body, but not the original sizing helper or ELFs. I therefore constructed [an independent portable linker harness](measure_link.py). It compiles actual controller, ADP/MAAP, loop, MMIO and CSR allocation sources, generated entity constants, real RV32I memory routines and arithmetic helpers. Symbol tables retain the application and protocol paths. Each output is an ELF32 executable with no unresolved symbol or heap dependency; [ELF/symbol evidence](receipts/linked-elf-evidence.json) and [archive-member evidence](receipts/link-runtime-members.json) establish an actual link.

Independent section results, bytes:

| Shape / image | text | rodata | data | bss | Sum before stack |
|---|---:|---:|---:|---:|---:|
| Shipping 1x1, shipped 8x8, maximum entity; dev | 8,324 | 180 | 0 | 2,156 | 10,660 |
| Same one-interface shapes; head | 14,284 | 188 | 0 | 3,296 | 17,768 |
| Head minus dev | +5,960 | +8 | 0 | +1,140 | +7,108 |
| Maximum entity, two interfaces; dev | 8,716 | 180 | 0 | 2,248 | 11,144 |
| Maximum entity, two interfaces; head | 15,004 | 188 | 0 | 4,448 | 19,640 |
| Head minus dev | +6,288 | +8 | 0 | +2,200 | +8,496 |

The maximum entity contains 15 AAF listeners and 16 AAF talkers plus CRF; the real generator accepts it. `ctrl_app` is 3,184 bytes at one interface (dev 2,076) and 4,336 at two (dev 2,168). MAAP occupies 1,104/2,168 contained bytes, including 960 queue bytes per interface. Pool control is 204 contained bytes; the unused minimum valid arena is 32 separate bytes; CSR context is 32 separate bytes. ADP/MAAP make no dynamic pool allocations. Contained objects are not added twice.

These storage figures agree with the public report. Small text/rodata differences reflect the independent entry/linker scaffold; this is not verification of the author's ELF hash. The two-interface section sum plus a separate 4 KiB stack reserve is 23,736 bytes. No whole-call-chain stack or routed-fit claim follows. Maximum-entity linking measures storage only: the existing CSR adapter accepts at most eight AAF outputs, and this experiment does not establish functional support for sixteen. Board startup and later F1/F3/F4/F5 composition remain outside this sizing experiment.

**Earlier findings at this head**

Original severity and lens assignments are retained. [Round 3 external](https://github.com/kebag-logic/milan-fpga/pull/687#issuecomment-6030412663) and [round 3 internal](https://github.com/kebag-logic/milan-fpga/pull/687#issuecomment-6030528869) were reconciled with the two earlier rounds from each role.

| ID; original severity; lenses | Disposition and exact-head evidence |
|---|---|
| R529-3-F1; MINOR; Docs, Tests. R528-3-F1; MINOR; Docs | BOTH RESOLVED. README:156 names `MILAN_RV32_CC`; absent/competing-default probes pass; old selector scan is empty; documentation gates pass. |
| R528-3-S1; SUGGESTION; Docs | ADDRESSED. All twelve debug RV32 objects compile; README:144-146 states the remaining assertion-handler linkage obligation. |
| R529-1-F1; MAJOR; Conformance, RTL, Robustness, Tests | RESOLVED retained. `ctrl_app.c:55` and `test_maap_mbx.cpp:273` are unchanged from round 3. Both interface counts pass actual wait/wake; independently removing the MAAP interrupt is caught. |
| R529-1-F2; MINOR; Conformance, Tests, Docs. R528-1-F2; MINOR; Tests, Docs | BOTH RESOLVED retained. Differential:133 and its controls still observe strict core intervals, parent bounds/count and wire differences; all 16 controls caught; README:169-174 preserves the documented deltas. |
| R528-1-F1; MINOR; Conformance, Robustness, Tests | RESOLVED retained. `maap.c:190,235` and `test_maap.cpp:311` preserve the supplied range until the first operational port, then consume it. |
| R528-1-F3; MINOR; Tests | RESOLVED retained. `test_maap.cpp:179,195` and unchanged named controls pin every priority octet and the fixed-seed restart draw; complete campaign passes. |
| R528-1-F4; MINOR; Tests, Docs | RESOLVED retained. Direction-aware model and destination-before-enable assertions at `test_maap.cpp:391,446` pass; named defects remain caught. |
| R528-1-F5; MINOR; Tests | RESOLVED retained. Interface-1 stall case at `test_maap_mbx.cpp:324` passes; independent lost-poll defect fails it. |
| R528-1-F6; MINOR; RTL, Docs | RESOLVED retained. README:101-109 and PR body retain the allocation-to-processor/F3 prerequisite. Checked against `KL_pp_maap_shim.sv:76` and `milan_datapath.sv:1999`. |
| R528-1-S1; SUGGESTION; Tests | ADDRESSED retained. Generic predicate controls remain caught; debug target compilation now supplements the stated release evidence. |
| R528-2-S1; SUGGESTION; Tests | ADDRESSED retained. `test_maap.cpp:331` and the retained-preference defect still pin one-use preference across link bounce. |
| R528-2-R1; RESIDUE; Docs | RESOLVED retained. Controller README:25 now uses an unnumbered firmware-arm description; its table includes both new re-entry arms and MAAP arms. |
| R529-3-R1; RESIDUE; Docs | RETAINED, wording only; precise current fix below. |

**Open prose residues**

R529-3-R1 - RESIDUE - Docs - PR #687 Status paragraph. The published body still says `This head is not pushed.` The read-only PR metadata identifies this exact published head. Impact: stale publication wording only. Required outcome / exact fix: replace that sentence with `The branch is published at the exact head above.` Historical executor statements about not personally pushing remain valid. Verification: compare the revised Status paragraph with the public head. This retains the prior residue; no measurement, test, verdict, source, conformance or privacy claim changes.

R529-4-R1 - RESIDUE - Docs - PR #687 Contents, ten entry separators. CONTRIBUTING Section 6.1 prohibits new em-dash separators; all ten remain in the public PR body. Impact: typography only. Required outcome / exact fix: replace each Contents separator `U+0020 U+2014 U+0020` with ` -- `, leaving labels, targets and descriptions unchanged. Verification: scan that Contents block after editing. This changes no measurement, figure, verdict, executable artifact, conformance or privacy claim.

**Reviewer-owned completion ledger**

Every row is clean at the reviewed head. Round 3 is cited only for unchanged MAAP behavior/interfaces; its Tests and Docs findings are cleared by this round, not carried as clean coverage. The exact round-3 head is `8b78a8fd36864246336c71c061ac4f21d629952f`.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | MAAP core/adapter/app, H-MAAP/differential, frozen scope, placement retention and linked-image sections | R529-4 delta/size; R529-3 unchanged Annex B scope | 5968967e19411428b71dde5c4712d4a8fa528cfb; retained scope at 8b78a8fd36864246336c71c061ac4f21d629952f |
| RTL | CLEAN | CSR/REGISTER_MAP/shim contracts, unchanged HDL and pins, real mailbox bus/co-simulation | R529-4 integration; R529-3 unchanged F2 architecture | 5968967e19411428b71dde5c4712d4a8fa528cfb; retained scope at 8b78a8fd36864246336c71c061ac4f21d629952f |
| Robustness | CLEAN | ADP guard matrix, exact-sized NVM boundary cases, MAAP wake/stall/loss/wrap/re-entry, seven independent faults | R529-4 imported protections and controls; R529-3 unchanged MAAP state paths | 5968967e19411428b71dde5c4712d4a8fa528cfb; retained scope at 8b78a8fd36864246336c71c061ac4f21d629952f |
| Tests | CLEAN | 196-definition union and catches; normal/coverage dispatch; 17-file ratchet; 435 NVM tests; 16 differential and 5 mailbox controls; selector reproduction | R529-4 | 5968967e19411428b71dde5c4712d4a8fa528cfb |
| Docs | CLEAN | MAAP/compiler/assertion recipes, arm inventory, coverage reasons, public scope/size evidence and explicit limits; two nonblocking residues | R529-4 | 5968967e19411428b71dde5c4712d4a8fa528cfb |

**Real limits and manager duties**

This source review is distinct from final current-dev candidate acceptance. The supplied manager source-bank passes are not relabelled as candidate proof. The manager must complete the independent review bar, carry both residues, obtain exact-head required hosted/local-replica evidence, construct and validate the candidate against live dev, record source/base/candidate tree identities, obtain explicit merge authorization, then run containment and update public workflow state. No merge or default flip is authorized by this review.

The single [hosted snapshot](receipts/hosted-snapshot.json) records successful executed `rtl-fast`, firmware, lint, elaboration helper, BDD, wire-accountability, no-Git documentation, selector and four synthesis shards. Four simulation shards, docs-check and elaborate were still running. Physical gPTP was SKIPPED. No final exhaustive aggregate is inferred. Hosted/local-replica acceptance remains manager-owned.

Physical calibration was NOT RUN; field/vendor skips provide no hardware proof. H-MAAP charges simulated 100 ns accesses with 1 ms timer resolution. Target CPU service, arbitration, NVM overlap, egress, media quiescence, all placement combinations, bench acceptance, redundancy, debug runtime linkage, whole-program stack and routed resource acceptance remain unproved here. The documented allocation-to-ACMP prerequisite and parent deviations in #686 remain outside this opt-in delta.

No full parent/processor/gPTP/synthesis/builder bank, container/replica operation, source fix, commit, push, GitHub write, merge, delegation, privileged operation or hardware access occurred. All probes and builds stayed below packet scratch. The root logical index digest is unchanged from entry; required submodule heads, raw blobs, modes and indices are verified. The unused external submodule remains uninitialized. All started campaigns are joined.

[Reproduction notes](REPRODUCE.md) identify the portable helpers and proof boundaries. `MANIFEST.sha256` enumerates every publishable receipt and helper; scratch is excluded. One mailbox receipt normalizes a home-directory prefix only; [original/published hashes](receipts/path-normalization.json) are recorded, with original bytes retained in scratch.

R529-4 FINISHED

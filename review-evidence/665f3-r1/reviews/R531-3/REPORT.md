[R531] NEGATIVE - exact head abb3a78a12c29ff13ee7f71a00b387a6c91dc361

R531-3, external independent source review of issue #665 / PR #688. One MINOR remains open: the linked-footprint evidence is not a valid RV32I measurement with the stated pinned SDK. The timer repair, interface fault coverage, merge resolutions and assigned documentation corrections pass this review. All five lenses were applied. This verdict supplies no merge authorization.

Tree: `d85f5361950dbf3f8deff0d45f4cb4fe7ff1e7fd`. Reconstructed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, requirements and interface authorities, the FC-to-head diff and history, then public executable evidence. The independent source pass and provisional ledger preceded inspection of prior public findings. No private author material or concurrent review report was used.

Scope: the delta from FC `021b9c1fb966e9a1a4acef6b5233edd3518f32a0`, with focused re-review of round 4 from `4f6216abff01b6f859d348aaf6a71e47c5a5a2a8`. The latter is merge `72597d223606ee9c3174dd7d68267921e40a8f3a`, whose ordered parents are the previous head and dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`, plus nine commits. Authorities include [F3 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6026721148), [bound-talker decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6029368753), [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6034423349), [linked-size acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), REQUIREMENTS.md section 1, FR_NFR.md 3.4.1/3.4.2, Milan v1.2 5.5/5.6.4, the mailbox contract and saved-state interface. Identities are in `receipts/scope-history.json` and `identities.json`. Public author evidence was read at archives `c961acabf3a36cb17085868b5c0f779145cf97aa` and `487861597b8d73e4478ed09f9a3fb2168874612e`, including `author-r4/HANDOFF.md`.

**R531-3-F1 | MINOR | Conformance, Tests, Docs | `sw/firmware/ctrl/test/ctrl_image.py:178-182`, `sw/firmware/ctrl/README.md:246-252`, PR #688 linked-image table | The link neither reproduces with the pinned SDK nor validates the advertised RV32I image.**

Authority/evidence: acceptance comments 6030870481 and 6034423349 require a linked composed image, shipping/largest shapes, section/static allocation and a base delta. REQUIREMENTS.md and NFR-SCOUT-01 specify RV32I; the new harness and published table expressly claim RV32I and the pinned SDK. The harness compiles first-party objects with RV32I flags, but links the selected SDK's prebuilt `-lgcc` and checks section sizes without checking the final architecture or ABI.

Two independent reproductions establish the problem:

1. The default compiler available to this review, GCC 14.3.0 / Buildroot 2026.05, reproduces every published section and delta. These are real ELF32 RISC-V `EXEC` files with load segments and no undefined symbols, not object sums. However, all four images (head/base, both shapes) advertise `rv32i2p1_m2p0_a2p1_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0`. Each contains 58 actual M-extension instructions in retained library helpers, including `divu`, `remu` and `mul`. In the shipping head, examples are `__udivdi3` at `0x6b34` (`divu`), `__umoddi3` and `__muldi3`. The maps attribute them to SDK library members used by the LiteSPI implementation. This is not merely conservative metadata. The size reporter exits 0; the independent ELF audit exits 1. See `receipts/image.log`, `elf-audit.log`, and the four `link-map-*.txt` receipts.
2. An independent extraction of the repository's pinned archive, SHA-256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`, passes installer/provenance verification. Its identity is GCC 14.3.0 / Buildroot 2021.11-18033-g83947c7bb6. Explicitly selecting it through `MILAN_RV32_CC` makes `ctrl_image.py` exit 2 at the link for both required shapes: `can't link double-float modules with soft-float modules`, naming `libgcc.a` members. See `receipts/sdk-install.log`, `image-pinned.log`, `image-pinned-largest.log` and exit receipts. The documented pinned-SDK reproduction therefore fails independently of the incompatible default-compiler output.

Impact: the footprint and percentage describe a real but incompatible artifact. They cannot discharge the required RV32I block-RAM comparison or substantiate the stated SDK provenance. This does not demonstrate a block-RAM overflow, and no shipping image is changed by this measurement harness. It retains the evidence obligation from R531-2-F2 / R530-2-F2 rather than reopening repaired ACMP behavior.

Required outcome: provide a reproducible link whose complete dependency set satisfies RV32I/ILP32, including arithmetic helpers; verify the final ELF's architecture, ABI and resolved dependencies before accepting its size; report both shapes and base deltas with accurate compiler/library provenance. Correct the table and public claims as needed. Keep disclosed owner/runtime/stack limitations separate from target compatibility.

Verification: both documented shape invocations must link under the stated reproducible setup; final images must pass an independent RV32I/ILP32 audit with no forbidden instructions or unresolved symbols. An incompatible-library control must be rejected by the measurement gate. Reconcile sections and static objects against maps, then update documentation and public evidence. `scripts/elf_audit.py` reproduces the current architecture failure. This is a measurement and executable-evidence defect, not RESIDUE.

**Prior public findings: disposition at this exact head**

Original severities and lens ownership are preserved. Prior findings were read after the independent diff pass from PR comments 6029581606, 6030054402, 6034240520 and 6034419826. Dispositions rest on current source and this round's probes.

| Finding | Disposition | Current evidence |
|---|---|---|
| R531-1-F1, MAJOR, Conformance/RTL/Robustness/Tests: unsupported versions | RESOLVED | `acmp.c` rejects AVTP version before both decoders. A26/B9 pass. Removing either check fails its named test in `fw-focus.json`. |
| R531-1-F2 and R531-2-F1, MAJOR, Conformance/RTL/Robustness/Tests; R531-2 also Docs: accepted-send interval | RESOLVED | `acmp.c:658-712` invalidates the clock cache after every accepted initial/duplicate probe, including `probe_left`. The unchanged four reviewer tests pass. The previous core fails the two immediate-send tests. A30 checks 199 ms success, exactly 200 ms expiry, cached expiry time and zero-delay work after another sink's send. Three timing regressions are caught. |
| R531-1-F3, MINOR, Conformance/RTL/Robustness/Tests: slot overflow | RESOLVED | `acmp_mbx.c:71` compares before narrowing. B7 covers last legal/first illegal, UINT_MAX and truncating values; restoring the overflowing addition is caught. |
| R531-1-F4, MINOR, Docs: owed-frame arithmetic | RESOLVED | `MAILBOX_SPLIT.md:663-681` gives 9,108 accesses and 9.108 ms at 1 us/access, excluding waiting for room. All four rows were independently recomputed. |
| R531-1-F5, MINOR, Docs: poll contract | RESOLVED | `acmp.h` promises at most one owed frame, oldest first; `acmp_poll`, A19 and E2 agree. |
| R530-1-F1, MINOR, Tests/Robustness: two-interface adapter | RESOLVED | `acmpif2` passes 19 tests, including B3/B4/B6 and latency paths. A shared-slot fault fails B3 on interface 1. |
| R530-1-F2, MINOR, Tests: BINDING layout/length | RESOLVED | A24 pins individual flags and 20 payload bytes against the processor layout; symmetric flag-swap and overlength-acceptance faults are caught. |
| R530-1-F3, MINOR, Tests: D3 rollback | RESOLVED | N7 keeps a binding through the port and real store boot. The binding-dropping D3 fault fails both required assertions. |
| R530-1-F4, MINOR, Tests/Robustness: clock wrap | RESOLVED | A28 covers all connection timers, discovery aging and earliest deadline across wrap. Unsigned due/earliest faults are caught. |
| R530-1-F5, MINOR, Conformance/Docs: TD1 authority/evidence | RESOLVED | The design, header, walk and PR explain the 5.5.2.7 overview / 5.5.4.2 procedure ruling. LD1-LD3 are executed model comparisons; TD1's processor half is source-read at `KL_acmp_talker.sv:1301-1306`, confirmed at the required gitlink. |
| R530-1-R1, RESIDUE, Docs: undecided ingress term | RESOLVED | Current design, ctrl README and PR identify decision 6029368753 and the implemented per-interface bound-talker term. |
| R530-2-F1, MINOR, Tests: interface mix-ups | RESOLVED | Q22/Q23 in `suite.hpp:1562-1617` pass on both adapters at one/two interfaces. All six live-interface/other-interface-owed faults fail their named assertions. |
| R531-2-F2, MINOR, Conformance/Tests/Docs; R530-2-F2, MINOR, Conformance/Docs: linked footprint | RETAINED through R531-3-F1 | A real link and section/pool table now exist, but target compatibility and pinned-SDK reproduction fail. |
| R530-2-F3, MINOR, Docs: stale access limit | RESOLVED | The open item and table consistently give 0.89 us for acmp backlog and 0.44 us for adp backlog, rounded down from the new counts. |
| R530-2-R1/R2/R3, RESIDUE, Docs: area ruling/contents/PR status | RESOLVED | Current open item, contents and PR record acceptance of +357 LUT/+86 FF and that the contract-changing alternatives were not taken. |
| Earlier run-cosim relink obligation | RESOLVED, retained | `tb/verilator/mbx/Makefile:65-80` retains dependency/relink repair through the merge; clean copied-tree co-simulation passes 32 checks. No new relink change is claimed. |

R530-2 S1/S3 remain optional area-publication/presentation suggestions. S2 was declined for this round and is not a finding. Historical sections of the archived handoff remain historical evidence.

**Applied lenses and executable evidence**

Conformance: compared changed send/expiry ordering with Milan 5.5.3.5.3 steps 5-7, 5.5.3.5.16 steps 1-2 and 5.5.3.5.23/.25. Checked saved-probe identity, same sequence, one duplicate, response-before-notification, discovery aging and per-interface admission against the API and H-ACMP/H-DISC hooks. The 127-case processor walk passes; it reuses pinned test models/constants and is not a fresh processor RTL run. Placement stays default-off. Linked-image acceptance remains unfulfilled under F1.

[R531] PASS RTL - `acmp.c:658-712,1090-1113`; `KL_mbx_rx.sv:220-379`; `KL_mbx.sv`; `acmp_mbx.c`; `ctrl_app.c`; `receipts/rtl-focus.log`, `cosim.log` - Applied the architecture lens to fresh-clock ownership, timer holds, FIFO/rebind cancellation, slot/tag routing, static composition and register-to-byte comparison. The table uses the latched arrival interface at FIN and that interface's owed flags. RAM reset validity, rewrite/copy suppression, byte indexing and stale-match handling pass Q12-Q23. No new crossing/reset topology is introduced. Mailbox RTL is byte-identical to round 3.

[R531] PASS Robustness - `test_acmp.cpp` A19/A24/A26-A30; `test_acmp_mbx.cpp` B3/B7/B9 and C/E/F paths; `test_acmp_nvm.cpp` N7; `suite.hpp` Q12-Q23; `receipts/independent-timers.log`, `fw-focus.json`, `rtl-focus.log` - Applied malformed-version, boundary, wrap, backpressure, cancel/rebind, lost-probe, saved-state failure, reset and interface-isolation checks. Queued probes start their timer when sent; stale queued probes cannot arm a replaced binding's timer. All 16 selected firmware faults and six interface RTL faults are detected by named assertions.

Tests: examined the changed test/fixture pairs, the image harness, and merge preservation. Independently executed:

| Run | Result | Receipt under `receipts/` |
|---|---|---|
| Native baseline | All 13 arms pass; ACMP 81, ACMP walk 127, binding integration 7, two-interface adapter 19; incoming debug/release re-entry arms 122 each | `firmware.log` before the first mutation; `firmware-scope.json` |
| Coverage | 17 files at 100% after documented exclusions; ACMP 734/734 lines, 342/342 branches | `coverage.log` |
| Unchanged R531-2 timer probes | 4/4 pass | `independent-timers.log` |
| Previous-core sensitivity control | Immediate initial/duplicate failures reproduced; queued/zero-duration controls pass | `timer-old.log`, `timer-old-child.rc` |
| Focused firmware faults | 16/16 caught; unchanged baseline test objects, only faulty C units rebuilt | `fw-focus.json`, `fw-focus.log`, `fw-*.log` |
| Mailbox controls, Wishbone / AXI4-Lite | 382/427 checks; two-interface variant 384/429 | `rtl-control-*.log` |
| Q22/Q23 faults | 6/6 caught, both adapters/relevant interface counts | `rtl-focus.log`, `rtl-rx-*.log` |
| Firmware/RTL co-simulation | 32 checks, 14 matching frames | `cosim.log` |
| Generator consistency/self-test | 0 findings; 0 failed arms | `generator-check.log`, `generator-selftest.log` |
| Documentation checks | Wording/privacy, added em-dashes and contents gates pass | `docs.log`, `em-dash.log`, `toc.log` |
| Link/architecture | Default link reproduces figures; four incompatible images fail audit; pinned SDK fails both shape links | `image.log`, `elf-audit.log`, `image-pinned*.log` |

Successful controls exit 0, deliberately faulty children exit 1, and pinned image links exit 2. The optional broad firmware mutation run was stopped after its complete 13-arm baseline and 48 caught mutations, with no escape observed; its receipt is `-15`, not a completed campaign pass. The required roots were then tested by the completed focused campaign. No full 354/354 or 147/147 claim is made. Independent campaigns/builds overlapped with at most 16 compilation jobs in aggregate. Commands remained foreground children and all were reaped. Retained builds and disposable source copies are under unpublished `scratch/`.

Docs: cross-checked `MAILBOX_SPLIT.md`, ctrl/gtest/ctrl_nvm/mailbox READMEs, interfaces, generated contract, issue decisions and PR body. Timer-to-probe cost is 35 accesses; the pass bound recomputes to 1,012, giving 3,036 / 11,132 / 22,264 / 9,108 for the four backlogs (`latency-arithmetic.json`). Executed C5/C8 report 35, and H-DISC enters through filtered ADP `RX_HEAD`. Corrected table/open-item and area wording agree. The target/provenance claim leaves Docs unclean under F1. No new RESIDUE is recorded.

The six conflicted files were checked with the actual merge-resolution diff (`receipts/merge-resolution.diff`): ctrl README, `ctrl_arms.py`, `ctrl_mutants.py`, `test_ctrl_firmware.py`, gtest README and `coverage.ratchet`. Both sides survive: ACMP arms/slices, incoming re-entry arms, `--jobs`, assertion support and both coverage populations. Thirteen-arm and fifteen-exclusion descriptions reflect the combined result. Native and coverage execution exercise both sides.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: R531-3-F1 | Milan 5.5.3.5.3/.16/.23/.25; FR_NFR 3.4; `acmp.c`; `ctrl_image.py:178-182`; linked-size acceptance and ELF audit | R531-3 applied; no clean covering round | abb3a78a12c29ff13ee7f71a00b387a6c91dc361 |
| RTL | CLEAN | `acmp.c:658-712,1090-1113`; mailbox RTL/table/copier; adapter/app; four RTL controls and co-simulation | R531-3 | abb3a78a12c29ff13ee7f71a00b387a6c91dc361 |
| Robustness | CLEAN | A19/A24/A26-A30, B3/B7/B9, N7, Q12-Q23; independent timer and 22 fault probes | R531-3 | abb3a78a12c29ff13ee7f71a00b387a6c91dc361 |
| Tests | UNCLEAN: R531-3-F1 | Changed tests/mutations; merge resolution; native/coverage receipts; `ctrl_image.py` and independent final-ELF audit | R531-3 applied; no clean covering round | abb3a78a12c29ff13ee7f71a00b387a6c91dc361 |
| Docs | UNCLEAN: R531-3-F1 | `MAILBOX_SPLIT.md`; API headers; ctrl README:225-261; gtest/mbx docs; issue/PR and public handoff | R531-3 applied; no clean covering round | abb3a78a12c29ff13ee7f71a00b387a6c91dc361 |

**Limits, reproduction and pending manager duties**

Accepted area remains +357 LUT / +86 FF with previously published WNS +0.402 ns and recipe. Exact blob comparisons prove unchanged mailbox RTL since that measurement. Physical implementation was not rerun. Inherited changes in the full FC-to-head history are distinguished from F3; round 4 changes no RTL, `sw/litex`, configuration, builder, constraints or synthesis input. Shipping/default integration sources also have no F3 delta against integrated dev.

This review does not replace manager-owned full source banks or final current-dev candidate validation. Full parent/processor/gPTP/synthesis/builder banks, hosted execution, local container replication and hardware were not run here. No executed or skipped hosted context is claimed. Physical calibration: NOT RUN. Field skips are not hardware proof. A4 access time, full-backlog T_svc, H-ACMP wire round trip and bench acceptance remain pending. Runtime stand-ins, absent final owners, provisional lwSRP pool and uncounted stack remain measurement-composition limits even after F1 is repaired.

Portable scripts take `CHECKOUT` and `PACKET` arguments. Set `TMPDIR="$PACKET/scratch"`, `PYTHONDONTWRITEBYTECODE=1`, and `VERILATOR` to the verified scoped executable. `run_receipt.py PACKET NAME COMMAND...` preserves foreground output and status. Reproduce baseline with `test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir "$PACKET/scratch/firmware"`, then `firmware_focus.py "$CHECKOUT" "$PACKET" --jobs 4`. Run `run_timer_probes.py`, `timer_negative_control.py` and `rtl_focus.py` with those same positional paths (RTL adds `--jobs 2`); `run_cosim.py` also takes the simulator executable. `elf_audit.py` takes an image-output directory and compiler binutils prefix. Produce images with `ctrl_image.py --base d51b373ad7e8e8381af2797be3ebb8ee45c62e3c --out DIR`; explicitly select the verified SDK with `MILAN_RV32_CC`. The SDK receipt identifies its pinned archive and extraction inputs.

Final integrity verification checks 1,171 parent blobs and 876 required-submodule blobs directly against committed bytes, executable modes, complete stage-0 index entries and gitlinks. Before/after receipts pass and match; the tracked checkout is unchanged. Required pins: protocol-processor `ead8036035affd53ef4b29979190f2f4f67084c0`, gptp-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused external gitlink is verified in the parent index but not initialized. No source fix, commit, push, GitHub write or merge was performed.

`MANIFEST.sha256` enumerates every publishable script and receipt. Local path prefixes in logs/maps are replaced by neutral placeholders; `receipts/path-redactions.json` records original/published hashes, and originals remain in unpublished scratch. No binaries or private standard text are published. Claims distinguish successful controls, detected faults, failed links and the intentionally incomplete broad campaign.

The manager must carry R531-3-F1 to correction and independent re-review, preserve the resolved timer/interface checks, then obtain the complete review bar and validated current-dev candidate. The manager owns hosted/local acceptance, any authorized merge, post-merge containment and publication. Processor #168 remains separately tracked; this lane changes no processor gitlink.

R531-3 FINISHED

[R531] POSITIVE - exact head 39adc58f8e63c7f41e12c79207a45bcc91a658d0

R531-4, external independent delta review of issue #665 / PR #688, lane round 5. All five lenses are CLEAN. No new finding or residue remains. The shared linked-image finding R531-3-F1 / R530-3-F1 is RESOLVED. This is source-review evidence, not merge authorization or hardware acceptance.

Tree: `6e677bcdf9e401d538e362e6e1ef534cb084eb7d`. Source base: `021b9c1fb966e9a1a4acef6b5233edd3518f32a0`. Previous reviewed head, lane round 4: `abb3a78a12c29ff13ee7f71a00b387a6c91dc361`. The delta contains seven commits and four files: the ctrl README, `ctrl_image.py`, `ctrl_image_selftest.py` and `rv32_image/image_arith.c`. Protocol implementation, mailbox RTL/contracts, existing suites, platform configuration and submodule gitlinks are unchanged. `scope-retention.txt` records exact tree/blob identity for 22 relevant paths and the FC-to-head inventory.

Reconstruction followed the assigned order: AGENTS/CONTRIBUTING, documentation index, issue scope and decisions, requirements/interfaces, diff/history, then public evidence. Authorities include [F3 scope](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6026721148), [linked-size acceptance](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481), [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6034423349), [round-5 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6036721467), REQUIREMENTS.md section 1, NFR-SCOUT-01/03/08, and the mailbox and split architecture contracts.

The supplied archive `c961acabf3a36cb17085868b5c0f779145cf97aa` contains the original author packet. The round-5 packet was examined at immutable evidence revision [24bc7989d0b98b46efe070cb3f612ff3017192e6](https://github.com/kebag-logic/milan-fpga/tree/24bc7989d0b98b46efe070cb3f612ff3017192e6/review-evidence/665f3-r1/author-r5), alongside the current PR body and public REVIEW READY comment 6037365656. `independent-verdict.txt` records the verdict and ledger written before reading prior review findings. No private author material or concurrent review report was read.

**Image finding resolved**

The documented command ran with `MILAN_RV32_CC` selecting a fresh SDK extraction under this packet's scratch directory. The installer verified archive SHA-256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`, relocation, inventory and compiler identity. Its version line is `riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`; `libgcc.a` SHA-256 is `d8ebca8cf6ad31cd50695f79e91e86a716d3b1761fbbefd5ee7b0627a2d0af58`. No library is linked. The README identifies the same build by revision and archive/library hashes; the PR body and handoff carry the complete version line. The final README passes the bare-metal gate.

Both required shapes reproduce every section and delta from dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`:

| Shape | Inputs/outputs | text | rodata | data | bss | total | Base total | Delta | Budget |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Shipping, `endstation_ax7101_1x1_tdm8` | 2/2 | 27,700 | 736 | 0 | 11,280 | 39,716 | 23,980 | +15,736 | 30.3% |
| Largest, `endstation_ax7101_8x8` | 9/9 | 27,704 | 736 | 0 | 21,648 | 50,088 | 34,336 | +15,752 | 38.2% |

The 131,072-byte comparison is the disclosed section-total measurement, with the stack excluded. Each image includes 64 bytes of runtime stand-ins and 412 bytes of arithmetic helpers, reported separately. The latter are `__lshrdi3` 56, `__muldi3` 100, `__mulsi3` 44, `__udivdi3` 28, `__umoddi3` 36, and their shared divide loop 148 bytes. No floating-point helper is reached.

The independent auditor imports none of the candidate's checking code. It reads ELF fields/sections and checks the complete disassembly against a base-instruction whitelist, accounting for every executable byte. All four head/base images are little-endian ELF32 RISC-V executables, flags 0, soft-float ILP32, attribute `rv32i2p1`, with no undefined ELF symbols. Counts are 6,925/6,926 words at the head and 4,212/4,213 at the base. All four ELF hashes equal the public handoff's hashes. Maps show only object inputs, no archives; section sizes agree with ELF accounting. The candidate additionally checks input objects for undefined weak references that can disappear during linking.

**Applied lenses and local receipts**

[R531] PASS Conformance - `REQUIREMENTS.md:4`, `docs/reference/FR_NFR.md:321`, `ctrl_image.py:328`, `ctrl/README.md:285`, `image.log`, `independent-audit.log`, `map-accounting.txt` - The composed image, both shapes, base comparison, section/static allocation and accurately identified pinned compiler satisfy the linked-size acceptance and RV32I ruling. Existing protocol acceptance is retained through unchanged source identities.

[R531] PASS RTL - `ctrl_image.py:93,204,281`, `rv32_image/image_arith.c:35,122,172`, `scope-retention.txt`, four `*.readelf.txt` receipts - Applied the architecture lens to RV32I/ILP32 compatibility, resolved dependencies, helper lowering and static composition. Helpers use unsigned words/halves and explicit carry/sign handling. No mailbox RTL, reset/CDC topology, register contract or shipping-build input changes. Round-4 RTL coverage remains valid.

[R531] PASS Robustness - `image_arith.c:35-213`, `ctrl_image_selftest.py:61,237,245,385`, `selftest.log`, `helper-mutations.log` - Checked division/sign/carry boundaries, shifts at 0/31/32/63, every shift count, edge pairs and 200,000 random pairs. Documented C-undefined divide cases are excluded deliberately. Wrong ABI/ISA, weak references and recursive helper lowering are rejected. Unchanged protocol reset, stalls, cancellation, rebind, wrap and interface isolation retain round-4 coverage.

[R531] PASS Tests - `ctrl_image_selftest.py:280-431`, `helper_mutations.py`, `audit_images.py`, `selftest.log`, `helper-mutations.log` - All 33 self-test checks pass. Six independent arithmetic mutations each make the actual self-test exit 1 with named mismatches: 32-bit multiply low bit, 64-bit multiply carry, 32-bit and 64-bit divide equality, 64-bit shift upper half, and signed remainder. These fail on wrong results, not compilation. The independent audit confirms accepted images without reusing the candidate decoder. Existing protocol tests/campaigns are unchanged.

[R531] PASS Docs - `ctrl/README.md:225-318`, public `author-r5/HANDOFF.md`, PR #688 body/title, `sdk.log`, `image.log`, `baremetal.log` - Toolchain provenance, regenerated table, helper accounting, audit claim and measurement limits agree with execution. Both intermediate README wording commits leave a compliant final result. Historical round-4 figures are superseded by explicitly labelled round-5 figures.

Paths abbreviated above under ctrl mean `sw/firmware/ctrl`; image scripts and `rv32_image` are under its `test/` directory.

| Executed here | Result | Receipt |
|---|---|---|
| Fresh pinned SDK installation/verification | PASS | `sdk.log`, `sdk.rc` |
| `ctrl_image.py --base d51b373ad7e8e8381af2797be3ebb8ee45c62e3c --out <scratch>/images` | PASS, both shapes and base | `image.log`, `image.rc` |
| `ctrl_image_selftest.py --require-rv32 --out <scratch>/selftest` | 33 checks PASS | `selftest.log`, `selftest.rc` |
| Independent ELF/ISA/section/helper audit | 4/4 PASS | `independent-audit.log`, `.rc`, `*.readelf.txt` |
| Six helper defects through actual self-test | 6/6 caught; each child exit 1 | `helper-mutations.log`, `.rc` |
| `check_baremetal_only.py --check` | PASS, zero findings | `baremetal.log`, `.rc` |
| `check_py_idiom.py` | PASS | `python-idiom.log`, `.rc` |
| Raw blob/mode/index and required submodule verification | PASS before/after probes | `tree-before.log`, `tree-after.log` |

**Prior public findings: disposition at this head**

Read after the independent pass: PR comments [6029581606](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6029581606), [6030054402](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6030054402), [6034240520](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6034240520), [6034419826](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6034419826), [6036619302](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6036619302) and [6036713241](https://github.com/kebag-logic/milan-fpga/pull/688#issuecomment-6036713241). There were no submitted review bodies or inline comments. Original severities and lens ownership are preserved. Retained resolutions mean repaired source/tests are identical to the head re-reviewed by R531-3 and R530-3; those tests were not rerun here.

| ID, severity, attributable lenses | Disposition and evidence |
|---|---|
| R531-3-F1 / R530-3-F1, MINOR, Conformance/Tests/Docs | RESOLVED here: pinned-SDK link, four independent audits, incompatible-library controls, corrected provenance and tables. |
| R531-2-F2, MINOR, Conformance/Tests/Docs; R530-2-F2, MINOR, Conformance/Docs | RESOLVED here through the complete linked-image evidence, sections, static objects and base deltas. |
| R531-1-F1, MAJOR, Conformance/RTL/Robustness/Tests | Resolution retained: both receive paths reject unsupported AVTP versions; A26/B9 and fault controls unchanged. |
| R531-1-F2, MAJOR, Conformance/RTL/Robustness/Tests; R531-2-F1, MAJOR, all five lenses | Resolution retained: `acmp.c:658-712` reads a fresh clock after accepted initial/duplicate probes; A30, queued/cancelled/rebound/wrap tests and corrected access figures unchanged. |
| R531-1-F3, MINOR, Conformance/RTL/Robustness/Tests | Resolution retained: `acmp_mbx.c:71` compares before narrowing; B7 covers legal/illegal, UINT_MAX and truncating ranges. |
| R531-1-F4, MINOR, Docs | Resolution retained: `MAILBOX_SPLIT.md:663-681` correctly gives 9,108 accesses and 9.108 ms, excluding room wait. |
| R531-1-F5, MINOR, Docs | Resolution retained: `acmp.h:425` promises at most one owed frame, oldest first; implementation and A19/E2 agree. |
| R530-1-F1, MINOR, Tests/Robustness | Resolution retained: `acmpif2` runs adapter/latency paths at two interfaces with shared-slot fault control. |
| R530-1-F2, MINOR, Tests | Resolution retained: A24 pins BINDING flags/20-byte layout and rejects excess length; symmetric-swap/overlength controls unchanged. |
| R530-1-F3, MINOR, Tests | Resolution retained: N7 verifies D3 rollback preserves bindings, with binding-dropping control. |
| R530-1-F4, MINOR, Tests/Robustness | Resolution retained: A28 covers connection/discovery timers and earliest deadline across wrap, with unsigned-comparison controls. |
| R530-1-F5, MINOR, Conformance/Docs | Resolution retained: `MAILBOX_SPLIT.md:685-717`, `acmp_walk.cpp` and current PR retain the 5.5.2.7/5.5.4.2 ruling; LD1-LD3 are executed comparisons, TD1's processor half is source-read evidence. |
| R530-2-F1, MINOR, Tests | Resolution retained: `suite.hpp:1562-1617` Q22/Q23 and interface-selection/owed-copy faults unchanged from passing round-4 review. |
| R530-2-F3, MINOR, Docs | Resolution retained: design table/open items consistently give 0.89 us/acmp and 0.44 us/adp backlog. |
| R530-1-R1; R530-2-R1/R2/R3, RESIDUE, Docs | Resolved status retained: ingress decision, area acceptance and contents current; PR retains accepted +357 LUT/+86 FF ruling. |
| R530-3-R1, RESIDUE, Docs | RESOLVED: current title is “Mark II F3: bare-metal ACMP core on the mailbox”. |
| Earlier run-cosim relink obligation | Resolution retained: `tb/verilator/mbx/Makefile:65-80` and round-4 relink/co-simulation coverage unchanged. |

R530-2-S1/S3 remain optional area-evidence/presentation suggestions, with no lens effect. S2 remains outside this round's assigned change. No unresolved BLOCKER, MAJOR or MINOR is moved to another issue to obtain this verdict.

**Reviewer-owned ledger**

“Round 4” means lane round 4, reviewed by R531-3/R530-3 at `abb3a78a12c29ff13ee7f71a00b387a6c91dc361`. R531-4 checks changed artifacts and accepts retention only for untouched artifacts proved by `scope-retention.txt`. Earlier image-related negative verdicts are cleared by new evidence, not treated as blanket approvals.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6036721467; requirements; linked composition, both shapes/base; unchanged ACMP/discovery contracts | R531-4; round-4 protocol coverage retained | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |
| RTL | CLEAN | Four-file delta; helper arithmetic/ABI; independent ELF audit; unchanged `KL_mbx_rx.sv`, `KL_mbx.sv`, ACMP/app and platform trees | R531-4 image architecture; R531-3 round-4 firmware/RTL coverage retained | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |
| Robustness | CLEAN | Helper edge/shift/carry/sign cases; incompatible-image controls; unchanged A19/A24/A26-A30, B3/B7/B9, N7, Q12-Q23 | R531-4 helpers/audit; R531-3 round-4 protocol coverage retained | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |
| Tests | CLEAN | New self-test, six independent defects, four independent image audits; unchanged protocol tests/campaigns/ratchet | R531-4; unaffected round-4 evidence retained | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |
| Docs | CLEAN | README size section, public round-5 handoff/PR, identity/table receipts; unchanged mailbox/interface docs | R531-4; unaffected round-4 checks retained | `39adc58f8e63c7f41e12c79207a45bcc91a658d0` |

**Limits and pending manager duties**

- This measures a test composition with stub owners, runtime stand-ins and explicit helpers. It does not size the final platform runtime, F4 pool, every integrator component, stack or routed shipping image. No target execution is claimed.
- Physical calibration was NOT RUN. Field skips are not hardware proof. A4 access time, H-ACMP wire round trip and F2-F5 bench acceptance remain pending. Backlog conditions remain 0.89 us/acmp and 0.44 us/adp per access.
- Accepted area (+357 LUT/+86 FF) is unchanged and was not remeasured. Full parent, processor, gPTP, builder, synthesis and native banks were not rerun here; source-bank success is manager-reported evidence. No RTL simulator was used this round. Protocol clause coverage is retained from round 4; no fresh standards-text review or hardware proof is claimed.
- No hosted workflow runs `ctrl_image.py` or its self-test. This is explicitly not a finding under the assignment. The manager owns workflow follow-up.
- `hosted-snapshot.json` is an exact-head observation, not acceptance. Executed successful jobs include firmware-unit, verilator-lint, all four Yosys shards, bdd-conformance, changes, full-ci-gate, docs-check-no-git and wire-accountability. All five Verilator shards, yosys-elaboration, elaborate and docs-check were running. The rtl-fast/verilator-suites/yosys-portability aggregates were not yet reported. Physical gPTP was skipped. The manager owns final hosted/local-replica acceptance.
- The manager must obtain the other independent verdict, ensure no review remains in flight, build/gate the final candidate against live dev, obtain explicit merge authorization, then prove containment and complete public workflow state. Source validation against FC is distinct from that candidate. This review does not claim completion of merge gates.

Reproduce with `python3 reproduce.py <exact-head-checkout> <new-output-directory>`. The driver installs the pinned SDK into scratch, runs focused checks with separate logs/return codes, and joins every child. Individual portable scripts are `audit_images.py`, `helper_mutations.py` and `verify_tree.py`. Independent image/self-test work ran concurrently; the mutation driver used six workers, below sixteen jobs. Disposable trees, SDK files and builds stayed under packet `scratch/` and are excluded from publication.

No candidate source was edited. Final verification proves 1,173 parent blobs, executable modes and complete index equal the requested tree. Required registered submodules, raw blobs/modes and indexes match gitlinks: protocol processor `ead8036035affd53ef4b29979190f2f4f67084c0`, gPTP processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused external submodule remains uninitialized. No GitHub write, commit, push, merge, shared installation or hardware operation occurred. Only REPORT.md and receipts named by MANIFEST.sha256 are publishable.

R531-4 FINISHED

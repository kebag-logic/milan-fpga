[R938] NEGATIVE - exact head a6864a49293ba3d0df37029abfa581468ef78dce

R938-1, external independent review of issue #1013 / PR #1016. All five lenses were applied. Three MINOR findings remain under Tests and Docs. No production implementation defect was demonstrated. One presentation residue is also recorded.

Reviewed tree: `282773485cda391903a7e3bf8b1a0374bb882563`. Diff base: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`. The independent diff pass preceded examination of the public validation packet and PR discussion. No other review report or private author material was consulted.

The [issue's public ruling](https://github.com/kebag-logic/milan-fpga/issues/1013#issuecomment-7178757153) freezes the gPTP target at `3ce71b768a2f6f6a5274c127080146e755d02275`, replacing the original `3009f9a2`. The stack target is `a795471c0abc4e38f7e5146b4e539dd607b6f501`. The [donor ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/109#issuecomment-7123290416) requires signed use with a -800 ns floor and zero clamping only at the platform's public bank. [Stack issue #37](https://github.com/kebag-logic/tsn-c-stack/issues/37) requires accepting control lengths above 56 using the readable fixed prefix.

Authorities examined: `AGENTS.md` sections 6-7; `CONTRIBUTING.md` sections 2-3 and 6; `docs/README.md`; `REQUIREMENTS.md` sections 1, 3, 4 and 8; `docs/overview/ARCHITECTURE.md`; `docs/design/GPTP_PLANE.md`; the pinned engine's `docs/INTEGRATION.md`; stack `docs/REQUIREMENTS.md` ADP-01 and `docs/PORTING.md`; `docs/design/MAILBOX_SPLIT.md`; `docs/reference/REGISTER_MAP.md:2132`; and `docs/integration/BUILDING.md:614`. Clause interpretation follows the public decisions citing IEEE 802.1AS-2020 11.2.13.7, 11.2.19.3.4 and 11.2.14.2.1, Milan v1.2 4.2.6.2.7, IEEE 1722.1-2021 6.2.2.6 and 6.2.7.1.3, and Milan v1.2 5.6.3.1. The floor is an explicit project decision.

**Findings**

[R938] R938-1-F1 MINOR Tests, Docs - `tb/verilator/gptp_shadow/sim_main.cpp:3039` and `tb/verilator/gptp_shadow/README.md` phase 22 - A stale offset satisfies the claimed new Follow_Up check.

Authority/evidence: AGENTS section 6 requires each new test to detect its claimed defect. `delay_trial()` sends a pair, then checks only that the published offset is near zero, no step occurred, and the election remained intact. Earlier pairs already establish an offset near zero. The disposable probe removed only `gm_pair_on_link(m, used_delay(d));`, retaining every assertion. The entire suite still completed `483 checks: 483 PASS, 0 FAIL`. See `shadow_probe.py` and `receipts/shadow-graded-pair-omitted.log`; the clean control also passed 483/483.

Impact: the phase claims that the next Follow_Up was used even when none was sent. It does not establish fresh consumption through the transport after each changed delay. The direct-engine phase separately checks consumption and exact arithmetic, so this is a bounded consumer-test weakness, not evidence of defective production arithmetic.

Required outcome: observe a fresh, attributable result from each graded pair and fail if that pair is absent or unconsumed. Keep the phase documentation consistent with the assertions.

Verification: the clean phase passes; the omitted-pair probe fails a named freshness/consumption assertion with a completed tally. Preserve the public-clamp and delay controls.

[R938] R938-1-F2 MINOR Tests, Docs - PR #1016, “The gPTP platform regression” opening paragraph - The old-generator failure claim includes an unexecuted datapath comparison.

Authority/evidence: the paragraph says of three suites, “Each is red against the 1213ac5b generator”. Its own table explicitly marks the `milan_dp` comparison “Not run there”. The public packet's `author/receipts/gptp/old-generator-red.log` records only the direct-engine and shadow runs. The relevant PR text is preserved in `receipts/public-claims.txt`.

Impact: readers are told a consumer regression experiment was executed when the detailed evidence says otherwise. This changes a test-result claim and is not wording-only RESIDUE.

Required outcome: restrict the failure claim to the two executed suites, leaving the datapath comparison explicitly NOT RUN, or supply the missing executed comparison. Correcting the claim accurately requires no additional experiment.

Verification: the revised PR summary, table and receipts agree about every claimed execution.

[R938] R938-1-F3 MINOR Tests, Docs - `docs/reference/SUBMODULES.md:1135`, PR #1016 route summary, and public `author/REVIEW-READY.md` route row - Route equality is claimed beyond the paired measurements.

Authority/evidence: “Every figure equals the base's at the same directive” includes the preceding 8x8 `AltSpreadLogic_high` row. The packet supplies that directive only for the head. Its base chain stops after `ExtraTimingOpt`; no base `AltSpreadLogic_high` signoff/utilization receipt is published. `receipts/evidence-audit.log` verifies equality for the three available head/base pairs and records the missing counterpart.

Impact: the claimed scope of measured equality exceeds the evidence. The selected 1x1 and 8x8 routes have matching base receipts and meet the governing floors. This finding does not invalidate those selected routes. It concerns a measurement claim and cannot be carried as wording-only RESIDUE.

Required outcome: state equality for the three paired routes and mark the head's `AltSpreadLogic_high` result as unpaired, or publish its matching base measurement. Correct the authoritative adoption record and PR summary consistently.

Verification: every equality statement identifies a published pair whose corner and utilization figures agree. Existing selected-image measurements may remain unchanged.

[R938] R938-1-R1 RESIDUE Docs - `tb/verilator/gptp_plane/README.md:24` - Phase 6 is separated from its table.

Authority/evidence: the blank line between phases 5 and 6 terminates the Markdown table. The phase 6 text renders outside it. Impact is presentation only; its measurement and clause claims are unchanged. Exact fix: delete that blank line. Verification: render the page and confirm phase 6 is the sixth body row. This residue does not leave a lens unclean.

**Artifact-specific results**

[R938] PASS Conformance - `gptp-processor/hdl/ucode/gen_gptp_ucode.py:2238`, `third_party/tsn-c-stack/src/adp.c:301`, issue #1013 and its ruling - Both pins implement the frozen behavior. Negative delays remain good; signed use is floored at -800 ns, +800 remains good and +801 bad. The platform alone clamps its unsigned word. ADP preserves the 82-byte minimum, 11-bit masking, version and target checks, while accepting lengths at least 56. The 128-byte mailbox limit is unchanged. Selected route and ledger evidence supports the acceptance criteria within the limits below.

[R938] PASS RTL - `gptp-processor/hdl/ucode/gen_gptp_ucode.py:2254`, `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:745`, `hdl/milan/milan_datapath.sv:1848` and `:6460` - Reviewed arithmetic width, floor ordering, threshold branch, publication commit and consumer wiring. Arithmetic halving bounds D before adding 800; the floor cannot overflow and leaves negative published values representable in 32 bits. The verdict subtracts 801 after the floor using the full width. Scratch and engine publication receive the same signed value. The committed public bank clamps it, and CSR plus GET_AVB_INFO consume that bank. Firmware `aecp_face.c:192` and `aecp_commands.c:523` preserve the unsigned value. No port, clock, reset, CDC primitive, state-owner or interface change was introduced. The regenerated ROM has 1,024 words, 1,013 real, and the recorded digest.

[R938] PASS Robustness - `tb/verilator/gptp_plane/sim_main.cpp:585`, `sw/firmware/ctrl/test/test_adp.cpp:876`, pinned stack `tests/test_adp.cpp`, and pinned engine `tb/verilator/engine/sim_main.cpp:8597` - Applied boundary, malformed-input, ordering and recovery checks. Independently executed negative delays through -5 ms, -800/-801, +800/+801 and requalification, plus all 69 ADP core/adapter tests. Those include states, truncated frames, version/target refusals, advertised lengths and protected-page reads. Reviewed donor extreme wire-delay tests and unchanged pairing, late-response, PHC-step and port-disable guards. Shadow execution covered transport stalls, resets and recovery. No new production robustness defect was found; the new pair-freshness claim remains F1 under Tests/Docs.

[R938] Tests applied, UNCLEAN - `tb/verilator/gptp_plane/link_delay.py`, `tb/verilator/gptp_shadow/mutants.py`, `sw/firmware/ctrl/test/ctrl_mutants.py`, all three consumer harnesses and the public receipts - Positive controls and required planted defects execute and detect their faults. The independent freshness probe exposes F1; evidence claims F2/F3 remain open.

[R938] Docs applied, UNCLEAN - `docs/reference/SUBMODULES.md`, `CHANGELOG.md`, `docs/design/GPTP_PLANE.md`, changed pin permalinks, both generated diagrams and `syn/yosys/rom_digests.tsv` - Pins, signed/public distinction, generated artifacts and budgets agree with source. Both generated PNGs were visually inspected. No new prohibited review or lane identifier was found in changed source comments. F1-F3 prevent clean coverage; R1 is presentation residue only.

**Independent execution**

| Check | Result | Receipt / portable driver |
|---|---|---|
| Scoped simulator identity | 5.050, revision v5.050 | `receipts/plane.log`; `run_focused.py` |
| Direct-engine consumer | 102/102 PASS | `receipts/plane.log` |
| Delay mutations | Clean image passes; all eight named defects caught | `receipts/plane.log`, `receipts/link-delay/` |
| ADP core and adapter | 69/69 PASS | `receipts/adp.log`; `adp_probe.py` |
| ADP length controls | 5/5 caught: omitted bound, valid_time contamination, narrow mask, exact-length rejection, rejection of 56 | `receipts/adp.log` |
| Shadow clean | 483/483 PASS | `receipts/shadow-clean.log`; `shadow_probe.py` |
| Public clamp removed | Eight assertion failures, including the named -263 ns check | `receipts/shadow-clamp-removed.log` |
| Graded shadow pairs omitted | 483/483 still PASS: F1 | `receipts/shadow-graded-pair-omitted.log` |
| Python idiom ratchet | PASS | `receipts/docs.log` |
| Test evidence ratchet, `--check` | PASS: 69 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 | `receipts/evidence-ratchet.log` |
| Submodule and gPTP documentation gates | PASS: six gitlinks, eight current pages | `receipts/docs.log` |
| Both diagram generators, `--check` | PASS, decoded PNGs current | `receipts/diagrams.log` |
| Default gPTP ROM generation | Digest `52293128994c886d91a4390b73b4cc1fa3c6a330ffae12aac985df750be9be61`, matches ledger | `receipts/rom.log` |
| Public hashes and carry-forward | 81 manifest entries match; both budgets unchanged; image-input trees match | `receipts/evidence-audit.log`; `audit.py` |
| Final checkout integrity | Both checkouts match tracked blobs, modes, indexes and initialized gitlinks | `receipts/source-integrity.log`, `receipts/probe-integrity.log`; `audit.py` |

All builds and probes stayed below the packet's `scratch/` directory. A foreground supervisor joined concurrent children: eight native compilation workers, four firmware compilation workers and a documentation scan. Shadow controls ran sequentially because they restore the same disposable files; the evidence ratchet ran beside them. Every probe has finished. The original checkout was not edited, and disposable source edits were restored before the byte-level audit. The historical `external` submodule remains uninitialized; its gitlink/index were verified, and it has no active product consumer.

Reproduce in a fresh packet directory with `setup.py <exact-head-checkout>`, then `run_focused.py <scoped-simulator>` and `shadow_probe.py <scoped-simulator>`. Drivers retain logs and return codes. `audit.py <checkout> integrity` checks all tracked bytes/modes/index entries without trusting status flags. `audit.py <checkout> evidence` checks the public packet extracted under `scratch/review-evidence/pins1125-r1`.

**Public evidence and limits**

The evidence authority is the immutable [pins1125-r1 packet](https://github.com/kebag-logic/milan-fpga/tree/86ac1ed8f385db77988c43e20318aff9c7a1a667/review-evidence/pins1125-r1/author). All published hashes were verified. Its condensed logs were inspected as author receipts; the full firmware, boundary, resource and routing campaigns were not repeated here.

At `a6864a49`, published pin receipts report 102 direct-engine checks with eight PHC-step campaign arms and nine link-delay campaign arms; 483 shadow checks with 14 detected controls and lifecycle checks; and 242 checks for each datapath leg. Both datapath receipts print -3, -80, -81, -263 and -5,000,000 ns predictions. Their harness reads CSR zero, retained asCapable and GET_AVB_INFO propagation-delay zero at every trial. These are author executions, distinct from the independent subset above.

At `d0483d08`, all four firmware shards report exit zero; the control campaign records 847/847 caught plants. Both boundary legs report zero findings: 4,085 and 1,208 compiled-source records, with their boundary/pin/figure controls. The table/launch suites, field campaign, grandmaster-step suite and physical-path simulation have passing receipts. The unchanged firmware, configurations and parent HDL, and identical donor `hdl/` and `syn/`, support carrying those image-input results forward. The excluded donor change concerns only its test runner and documentation.

The seven egress ledger rows are identical at source head/base and pass the non-regression ledger; its 18 controls pass. The underlying service run returns 1 and retains pre-existing budget/STATED failures, including the srp-bound-alone qualification. It is not a complete service-budget pass. All four platform memory ledger points also match the base and pass their recorded budgets.

The selected 1x1 route is ExtraPostPlacementOpt: worst setup +0.178 ns, hold +0.021 ns, 32,582 LUTs, 42,803 FFs, 13,590 slices and 80.5 RAMB36-equivalent tiles. The selected 8x8 route is ExtraTimingOpt: +0.283 ns, +0.036 ns, 45,810 LUTs, 53,378 FFs, 15,600 slices and 98.5 tiles. Each has 13 DSPs. All four corner measurements and utilization figures match the paired base. The governing [#818 policy](https://github.com/kebag-logic/milan-fpga/issues/818) uses setup >= +0.030 ns and hold >= 0; the 1x1 receipt's separate stricter hold test returning 1 does not invalidate those policy floors. The initial 8x8 directive has only +0.008 ns setup at both head/base and is not selected. The extra head directive passes but is unpaired, as F3 records. Matching metrics do not independently prove byte-identical placements.

The author docs replay reports 56 passed steps, 24 skips and three SDK provenance refusals. This is not an all-executed green workflow. The two relevant ratchets were independently checked here without budget changes. Hosted execution versus skipped contexts, and local workflow-replica acceptance, remain the manager's responsibility; neither was executed or accepted by this reviewer.

The licensed full standard editions were not independently reopened in this session. Conformance was checked against normative repository contracts and linked public decisions with their clause interpretations; this is not independent standards certification. Physical calibration is NOT RUN. Physical-path simulation and field skips are not hardware proof.

Prior public findings: after the independent diff pass, the PR discussion snapshot contained only two review-start comments and no earlier finding or review submission. There were no prior published PR findings to clear or retain. Concurrent reviewer reports were not consulted.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #1013/ruling; donor #109 ruling; ADP-01; generator:2238; adp.c:301; selected routes | R938-1 | a6864a49293ba3d0df37029abfa581468ef78dce |
| RTL | CLEAN | Generator floor/verdict/Sync use; KL_gptp_shadow.sv:745; milan_datapath.sv:1848/:6460; firmware face; ROM ledger | R938-1 | a6864a49293ba3d0df37029abfa581468ef78dce |
| Robustness | CLEAN | Plane boundaries/recovery; ADP states/protected-page tests; shadow reset/stall tests; donor extreme-delay source | R938-1 | a6864a49293ba3d0df37029abfa581468ef78dce |
| Tests | UNCLEAN | Consumer harnesses, controls, independent probes, public receipts; F1-F3 open | None; applied in R938-1 | a6864a49293ba3d0df37029abfa581468ef78dce |
| Docs | UNCLEAN | Adoption/PR/phase claims, generated pin sites/diagrams, ROM digest; F1-F3 open; R1 residue | None; applied in R938-1 | a6864a49293ba3d0df37029abfa581468ef78dce |

The manager must arrange correction and independent re-review of F1-F3, carry R1 on the residue checklist, obtain the other independent verdict, and ensure no review remains in flight. No manager source-head bank exists at this head, and none is inferred. The final merge candidate must be built against then-current dev, with builder/native receipts published at the merge turn. The supplied live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`, distinct from this review's source base. Required hosted/replica acceptance, merge authorization, post-merge containment, issue closure and project state remain pending manager duties. This verdict does not authorize merging or hardware qualification.

Publishable receipts and scripts are listed in `MANIFEST.sha256`. `RECEIPT-PROVENANCE.json` records raw/published hashes; publication copies redact installation and packet paths only. Raw originals and disposable builds remain under unpublished `scratch/`. No source fix, commit, push, GitHub write, merge, shared install or hardware operation was performed.

R938-1 FINISHED

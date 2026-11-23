[R894] POSITIVE - exact head 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e

External independent review R894-3, issue #584 / PR #975. Exact tree: `718c4adfc7e6cd76aa1b414c18abdcb1b64c291d`.

Both round-2 correction requests close at this head. The freshness record now covers recovery, including the lead before the later steady window; stale replay fails the named checks. The published current and corrected historical indexes match their actual files. No BLOCKER, MAJOR or MINOR remains in this narrow delta. Three wording residues and two carried suggestions are recorded below. They do not change a measurement, test expectation, protocol obligation, clause disposition or coverage verdict.

This is source-review approval only. The owner's backing disposition remains PENDING and is not a finding of this round. It is not merge authorization.

**Scope and independence**

Reconstructed repository rules and the documentation map, frozen issue acceptance and public decisions, then descriptor and render authorities. Examined the change structure/history from `dd163e41438acb86e0c4d4e76df90f3f91ace1c0` and the complete two-commit delta from `64d539f12532b2591f734b8e756f8a9358bb742c`. The latter changes only CHANGELOG.md, TESTING.md, `_plan_ports`, the ship8 harness and its mutation driver. No RTL, firmware, configuration, generated shape or gitlink changes occur in round 3. Untouched implementation retains its prior verdict, subject to the dependency checks below.

An independent verdict and five-lens ledger were written before reading the two prior reports. Their public findings were then reconciled explicitly. No private author material, management checkout, unpublished lane material or current peer report was read. No source fix, commit, push, GitHub write, author contact, sub-agent, container operation, hardware operation or privileged action occurred.

Authorities and public state:

- [Issue #584 acceptance and decisions](https://github.com/kebag-logic/milan-fpga/issues/584), including the cluster-minimum approval, one-cluster fallback, parking decision and November decision; [round-3 source evidence statement](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-7086448470).
- Milan v1.2 5.3.3.7-5.3.3.9 and 5.4.2.26-5.4.2.28; IEEE 1722.1-2021 6.2.2.8, 7.2.13, 7.2.16 and 7.2.19, as applied by the linked repository contracts. [Processor #122's public disposition](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/122#issuecomment-5853884588) retains the cluster minimum; zero dynamic maps does not permit zero clusters. No new interpretation of those clauses is introduced here.
- REQUIREMENTS.md, REQ-VER-01/03/04; ENDSTATION_BUILDER D7/D8/D10; PP_DESCRIPTOR_OWNERSHIP L1; CHANNEL_MAP_64 section 3.1; CONTRIBUTING verification and documentation rules.
- [Immutable evidence publication](https://github.com/kebag-logic/milan-fpga/tree/82a41140e1a7cc7779ab05eef732e569cb8a6157/review-evidence/584-r1), especially `author-r3`.
- [R894-2](https://github.com/kebag-logic/milan-fpga/pull/975#issuecomment-7085655489) and [R893-2](https://github.com/kebag-logic/milan-fpga/pull/975#issuecomment-7085887977), read after the independent pass.

**Closure at the cause**

| Prior item and attributable lenses | Disposition and exact-head evidence |
|---|---|
| R894 F2-R2 / R893 F6: Conformance, Robustness, Tests, Docs | CLOSED. `sim_ship8_render.cpp:1262` opens the record before unbind; `:1293` opens it immediately after reset release. Collection remains active through commands, the rebind and `kLeadPdus + kWindowPdus`. `grade_the_record` at `:1156` examines every decoded frame. `prove_the_recovery` at `:1215` distinguishes permitted in-flight pre-loss audio, closed-epoch silence, leading silence and every nonzero word after rebind. It checks the actual first rendered event, every subsequent source/event, gap/order, zero tail, pad and framing. The later steady windows remain. |
| F2-R2 / F6 negative controls | CLOSED. `ship8_mutants.py:94` supplies both replay arms with named B3/Z3 failure requirements. Published `rebind1.log` has 12 stale words, first event 1080 below cursor 1092, and B3 FRESHNESS failures; `reset1.log` has 12 stale words despite a fresh first word, and Z3 FRESHNESS fails. Both return 1. The second arm specifically proves that checking only the first word would be insufficient. My exact-grader probes independently reject a stale first word and a later stale word, closed-epoch leakage, a wrong stream, a nonzero tail and a rendering gap. |
| R894 F5-R2 / R893 F7: Tests, Docs | CLOSED. Independent hashing directly from Git blobs gives 159/159 current receipt rows, 80/80 replacement round-1 rows and 16/16 replacement round-2 rows, with complete file coverage and no duplicates. All 267 author files in the publication manifest match their published SHA-256; all 163 round-3 files have unchanged original/published hashes. The current index also authenticates the nested historical correction. |
| Historical original indexes | Explicitly superseded, not silently repaired. The original round-1 index remains 77/80; the original round-2 index remains 14/16. `author-r3/receipts/f5/round2-INDEX-corrected.md` supersedes the latter and identifies the round-1 replacement. The independent audit reproduces all five historical mismatches and verifies the replacements against this publication. |
| R894 R4 / R893 R4: generated plan names | CLOSED. `_plan_ports` at `sw/builder/endstation_builder.py:6046` adds `Unrouted S<p>` only when an input pool has that role. My five-configuration probe shows exactly a 17-byte addition for 8x8 and zero change for the other four configurations. Published artifact hashes independently compare 153/155 identical, with only the two 8x8 placement-specific build plans differing by 17 bytes. |
| R894 R5 / R893 RS2: pending TDM wording and silent ports | CLOSED. CHANGELOG.md:81-82 explicitly includes the TDM32 interpretation among the three pending points; :72 names port 0; :86-87 distinguishes zero bus slots from mappings that reach no slot. |
| R894 R6: normalized path explanation | CLOSED by the current explanation. `author-r3/receipts/f5/index-audit.md` describes home-path redaction in words, without examples that normalize into identical placeholders. The historical files remain historical; corrected indexes identify their exact published bytes. |
| R893 RS1: timing paragraph referent | CLOSED. TESTING.md:430-431 puts the follow_ring acceptance sentence directly after its original measurement paragraph; the ship8 planning estimate follows separately at :433-437. |
| R893 RS3: internal taps description | PARTIALLY addressed, with wording-only remainder R9-R3 below. The banner now names enable masks and stream IDs. The absolute word `only` and the old section title still need cleanup. |
| R893 S3: bank three additional plants | CLOSED. The zero-tail, unqualified epoch-mask and REMOVE-as-ADD plants are in `ship8_mutants.py:80-92`; the exact-head campaign records all three caught by their named checks. |
| R894/R893 F1: input backing | Statement remains disclosed, disposition PENDING. D8/D10, ownership page, PR and changelog state port 0 = TDM32 slot 0, ports 1-7 unrouted, no loopback-backed input cluster and loopback disabled at 8x8. No new finding or owner approval is inferred. |
| Earlier R894/R893 F3, R894 F4, R893 R1-R3 | Prior closures stand. Round 3 does not touch their memory accounting, waiver/census authorities, render-port ownership or loopback-on README artifacts. `_plan_ports` changes only its explanatory name list; recorded model identities, descriptor geometry, binaries and other artifacts remain unchanged. |

**Remaining findings: wording residue only**

[R894] RESIDUE Docs - R7-R3 - CHANGELOG.md:88-89 - Preserve the flush qualifier in the short recovery summary

Authority/evidence: the short text says the record spans a fall/reset to rebind and only post-loss/post-reset events may render in it. The detailed source banner (:47-59), TESTING.md ship8 row and PR correctly distinguish graceful closure and post-rebind freshness. The published clean `ship8.log:117` records one permitted pre-loss frame before closure; the independent grader control accepts the same case.

Impact: the compressed changelog wording loses that qualifier and the record's end point. This is a non-authoritative summary wording defect: the detailed contract, executable assertion, measurement and clause disposition already agree. No test, measurement or conformance outcome is to change.

Exact required wording: replace the two bullets with “One record spans loss/reset through recovery after rebind.” and “Pre-loss audio ends at epoch closure; rebind requires freshness.” Verification: those bullets agree with the existing source banner and clean record; retain the present tests and verdicts.

[R894] RESIDUE Docs - R8-R3 - tb/verilator/milan_dp_render/sim_ship8_render.cpp:45 - Remove the newly added bench phase label from the source comment

Authority/evidence: the owner's comment rule asks for behavior and reason rather than bench labels. The new banner continuation names `P2` instead of the operation it describes. Runtime check names are unchanged and are not the requested edit. The inherited T22 reference is not reopened as a new delta defect.

Impact: comment-maintenance residue only. Exact fix: replace “graded in P2 against the ids the bench's own answers carried” with “checked during listener binding against the IDs carried by the generated responses.” Keep the file's #584 authority and describe the same check. Verification: the added comment carries behavior rather than a phase token; executable bytes remain unchanged.

[R894] RESIDUE Docs - R9-R3 - tb/verilator/milan_dp_render/sim_ship8_render.cpp:42 and :411 - Finish the internal-tap wording correction

Authority/evidence: the banner now enumerates enable masks and stream IDs, but still introduces them as “timestamp and counter sources only”; the section title repeats that absolute. `bound_streams()` and `table_sid()` at :422-427 expose state/identity too. This is the remaining wording part of RS3.

Impact: contradictory labeling, with the actual taps now explicitly enumerated. Exact fix: use “Internal taps supply timestamps, counters, masks and stream IDs” for the banner and “Taps: timestamps, counters and stream state” for the section title. Verification: the labels describe the unchanged accessors and pin-only sample decoder. No oracle, test or clause claim changes.

**Carried optional suggestions**

[R894] SUGGESTION Tests, Docs - S1 (R893-2) - scripts/suite_shards.py:122; milan_dp_render/Makefile:47-62; TESTING.md:433-437

Evidence/impact: the aggregate historical timing predates ship8; its 240-second piece allocation is a scaled local estimate, explicitly not a hosted measurement. Desired outcome: update scheduling figures when the manager obtains the owed hosted timing. Verification: use measured current-head execution and distinguish pieces from the serial default suite. No new timing result is claimed here; this remains optional and does not unclean a lens.

[R894] SUGGESTION Tests, Robustness - S2 (R893-2) - tb/verilator/milan_dp_render/ship8_params.py

Evidence/impact: the unchanged parser intentionally ignores argv outside its recognized/refused prefixes. A future render-relevant flag outside those prefixes could escape its guard. Optional outcome: explicitly inventory ignored flags so a future relevant addition requires disposition. Verification: a future unsupported render-relevant flag fails by name while intended control/clock differences remain documented. This is future hardening, not a defect introduced by this delta.

**Independent lens results and reviewer-owned ledger**

[R894] PASS Conformance - Issue #584 acceptance/decisions; ENDSTATION_BUILDER D8/D10; PP_DESCRIPTOR_OWNERSHIP L1; CHANNEL_MAP_64 section 3.1; `_plan_ports:6046`; `plan-probe.log` - Cluster minimum, mapping semantics and pending input backing remain unchanged. The regenerated plan wording names an existing role. The recovery check now covers the temporal interval required by F2-R2. Earlier descriptor, identity, bounds and byte-identity results carry where untouched; no whole-product conformance claim is made.

[R894] PASS RTL - `hdl/ieee1722/aaf/KL_tdm_render_master.sv:430-443`; `hdl/milan/milan_datapath.sv:8641-8662`, `:8729-8742`; `source-range.txt`; `checkout-final.log` - Inspected the bus/lane split and dependency context from the source base. No round-3 RTL, interface, clock/reset, configuration or gitlink change invalidates prior coverage. The added controls exercise the same adapter, serializer, epoch mask and edit direction. No new RTL implementation defect found.

[R894] PASS Robustness - `sim_ship8_render.cpp:1156-1311`; `ship8_mutants.py:80-104`; published `rebind1.log`, `reset1.log`; `recovery-probe.log` - Collection includes loss/reset recovery and permits only the explicitly allowed pre-close frame. First and later stale words fail. Leakage, wrong source, zero-tail violation and gaps fail independently. Existing invalid-offset, unrouted-port and REMOVE behavior retains its covered result.

[R894] PASS Tests - published `ship8.log`, `ship8-mutants.txt`, `milan_dp_render-suite.txt`; `evidence-check.log`; `probe_recovery.py`; `check_receipts.py` - Source-head receipts state 130/0 ship8, 11/11 campaign and 263/0 + 79/0 + 130/0 full-suite checks with 5/5 leg-side controls. The mutation driver requires nonzero/failure output and the named checks, and rejects unrelated build failure as a catch. Current and corrected historical receipt hashes independently match the published blobs. Exact-grader controls exercise failure power without rerunning unchanged banks.

[R894] PASS Docs - all five round-3 delta files; PR body; corrected receipt indexes; `receipt-audit.log`; `plan-probe.log` - The backing decision stays pending; publication provenance and code limitations are explicit. Historical indexes are identified as superseded. The corrected timing referent and build-plan list agree with their evidence. R7-R9 are wording residue under the owner's rule, with no change required to a measured figure, test, verdict, generated artifact, conformance or clause disposition.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue/descriptor/render authorities; recovery interval; five-config plan probe | R894-3; untouched prior implementation carried | 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e |
| RTL | CLEAN | Serializer/adapter/epoch dependency context; no round-3 RTL/config/gitlink delta; byte audit | R894-3 dependency check; R894-1/R894-2 untouched RTL carried | 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e |
| Robustness | CLEAN | Continuous recovery grader, replay arms, seven RTL plants and refusal; nine independent controls | R894-3 | 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e |
| Tests | CLEAN | Three source-head gate receipts; replay logs; grader controls; publication hashes | R894-3 | 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e |
| Docs | CLEAN | Five-file delta, PR and issue status, current and superseding indexes, plan probe | R894-3; R7-R9 RESIDUE only | 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e |

**Reproducible receipts**

Run these portable scripts from the reviewed checkout, with this packet as `PACKET`. They do not edit source. The publication object must be available locally. Every invoked command completed in a foreground session; independent checks were run concurrently where useful. Generated grader source/binary and the extracted public corpus remain under this packet's unpublished `scratch/`.

| Command | Raw receipt | Result |
|---|---|---|
| `python3 "$PACKET/check_receipts.py"` | receipt-audit.log | 267/267 manifest author files; 159/159 current index; 80/80 and 16/16 corrected historical indexes; complete coverage |
| `python3 "$PACKET/check_evidence.py"` | evidence-check.log | Published named replay failures and all three exact-head suite/campaign results verified; recorded artifacts 153/155 identical, two 17-byte plan changes |
| `python3 "$PACKET/probe_recovery.py"` | recovery-probe.log | 9/9 independent decoded-frame controls pass against the extracted exact-head grader |
| `python3 "$PACKET/probe_plan.py"` | plan-probe.log | Five tracked configs; only the 8x8 plan section changes, by its 17-byte name example |
| `python3 "$PACKET/check_checkout.py"` | checkout-before.log, checkout-final.log | Raw tracked bytes/modes/index and all required initialized gitlinks exact |
| Required simulator identity, read-only | simulator-identity.txt | Pinned 5.050 identity and executable hash recorded; no simulation rerun claimed |
| Source-base diff inventory and commit history | source-range.txt | Review boundaries preserved; round 3 has two commits and five changed files |

The recovery probe compiles the unmodified `Recovery` structure and the exact `grade_the_record` / `prove_the_recovery` methods into a small decoded-frame driver. It is a checker-sensitivity test, not a hardware or full simulation result. The plan probe executes the exact current and prior `_plan_ports` functions against current normalized configurations. The artifact comparison checks published hash metadata; it is not an independent regeneration of all 155 files.

**Real limits and pending manager duties**

- The source-head ship8, ship8-mutants and full milan_dp_render executions are the author's published receipts, inspected and authenticated here; those complete builds/campaigns were not rerun. Their runtime excerpts are public; omitted compilation transcripts remain outside this review's evidence. No full parent, processor, timing-processor, synthesis or builder bank was run.
- The additional freshness gate is not isolated by this shape: the render stage already flushes the fallen stream. The published forced-open/uncleared-gate probes both pass; they are expressly not mutation catches. The replay arms prove the pin-record check rejects stale sample identities when delivered.
- The harness drives the all-fabric control face and uses model clocks. Its connection to the split product is the previously reviewed shared edit-server/media path, not a fresh CPU-to-pins execution or board-rate measurement.
- The published builder union reports 113 gates exactly once with two existing NOT RUN arms. Physical calibration is NOT RUN. The docs workflow reports 99/103 passing commands; four commands require the hosted environment and fail locally. Skipped field contexts are not hardware proof.
- No manager source bank ran at this head, and none is claimed or inferred. Route, firmware, saved-state and resource evidence retain their original provenance; this review supplies no new route, firmware link or hardware result.
- The evidence commit has no signature header. Its MANIFEST is a hash inventory, not a detached signature. Immutable object identity and every relevant published hash were checked; cryptographic signer authentication is not claimed.
- Final byte verification covers 1,944 superproject blobs, five initialized submodules and their raw tracked files/modes/indexes: protocol-processor `801ef2283ec793e35a2590fc6593c90313a64041`, gptp-processor `1616fc8f062fbf58c35ad31674b5b233207bbdb8`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`, tsn-c-stack `715589c1db7cf67e2f3259fd7083ebc7f0923376`, lwSRP `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. The uninitialized legacy external entry is checked as gitlink `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` only. No tracked source needed restoration.
- The manager must obtain the owner's public backing disposition, carry R7-R9 onto the residue checklist, retain optional S1/S2, and obtain the owed hosted runtime and exact-head hosted/local-replica acceptance. Hosted job state was not inspected or certified here.
- At merge, the manager must build and validate the current-dev candidate with the builder and native banks and publish its receipts. Source base `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`, reviewed source head and live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` are distinct. This source verdict does not validate that future merge result.
- Complete the remaining independent review/coverage bar, obtain explicit maintainer merge authorization, then perform post-merge containment and Issue/Project closure. If the backing disposition changes implementation or a reviewed artifact changes, re-cover the affected lenses.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Nothing under scratch/ is included.

R894-3 FINISHED

[R854] NEGATIVE - exact head 6ceed75374210935cff4f10d014b9a5ef137615e

Independent composition review R854-1 of issue #665 / PR #934.
Tree: 340fd990b4a7873d00d173ba3e357d920a8d7437.

All five lenses were applied independently to the composition delta. One MAJOR finding remains open. RTL is clean within this scope; Conformance, Robustness, Tests and Docs are unclean because the new LeaveAll gate can accept a skipped opportunity. No firmware defect is inferred from that test-oracle defect.

## R854-001: LeaveAll expiries can be assigned to the wrong participant

Severity: MAJOR. Lenses: Conformance, Robustness, Tests, Docs.
Artifact: tb/verilator/ctrl_service_budget/mrpdu_grade.py:247; sim_main.cpp:336; selftest_leaveall.py:72; README.md:148; docs/reference/FR_NFR.md:388.

Authority/evidence: issue #665 comment 6930885185 Q1 and IEEE 802.1Q-2018 10.7.4.1 require each participant to send its LeaveAll at its own first transmit opportunity. The log records a timer callback name and time but no participant. leave_alls selects the earliest future unconsumed LeaveAll across every participant, then uses that frame to infer which participant owned the expiry. This reverses the required association.

Reproducer: python3 -B probe_leaveall.py REPOSITORY. In participant_swap.log, MSRP sends at 1000 ms and MVRP at 1040 ms. MSRP's LeaveAll expires at 1050 ms; its join opportunity is 1180 ms, but its 1181 ms MRPDU omits LeaveAll. MVRP's LeaveAll expires at 1190 ms and correctly sends at 1221 ms after its 1220 ms opportunity. MSRP sends its delayed LeaveAll only at 1371 ms. The grader pairs the 1050 expiry with MVRP and the 1190 expiry with MSRP, reports two sent and zero skipped/late/absent, no stated_misses, and 1 ms rows. The independent expected result is a skipped MSRP opportunity and LeaveAll 191 ms after its first opportunity. The matching clean overlapping-timer control passes. A single-participant 60 ms late control fails as expected. The raw logs, probe script and detailed grader output are included in this packet.

Impact: the new conformance gate and service rows can accept a real skipped transmit opportunity under overlapping participant timers. The eight new mutants exercise single-owner cases or removal of EtherType distinction; they do not prove timer ownership. The claims of participant-specific first-opportunity verification in README/FR_NFR and the published all-44 result exceed the grader's evidence. This is a test-oracle defect, not a demonstrated firmware transmission defect.

Required outcome: bind every timer expiry to its interface and application using evidence independent of the future output selected to satisfy it. Use that binding consistently for the opportunity, missing/late output and first-MRPDU checks. Reject or report unresolvable ownership rather than infer it from whichever LeaveAll arrives first. Add overlapping-expiry, reordered-output and skipped/late/absent controls for both applications and interfaces, then regrade the eleven phases and valid-destinations leg. Keep the 49 ms bound unchanged.

Verification: the supplied overlap must fail by the actual MSRP participant and its original opportunity, with correctly ordered and legitimately reordered clean controls passing. Existing single-participant controls and eight new mutants must remain effective.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, R854-001 | #665 rulings 6899740728 and 6930885185; FR_NFR 3.4.1; mrpdu_grade.py; #843 engine changes and board/AEM identity | R854-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |
| RTL | CLEAN | milan_datapath.sv station-MAC gate and both generate branches; a563a83d; 9715a30a bench paths; both merge resolutions; pinned processor changes | R854-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |
| Robustness | UNCLEAN, R854-001 | held ready/valid handshake; split gate plants; overlapping-participant and late-control raw logs; LeaveAll absent/unresolved parser arms | R854-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |
| Tests | UNCLEAN, R854-001 | selftest_leaveall.py and eight mutations; split_mutants.py; twin owed-row removals against processor fixing commits; published sweep/workflow receipts | R854-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |
| Docs | UNCLEAN, R854-001 | FR_NFR:388, budget README:148; both merges' document resolutions; PR ledger; published normalized release-export evidence and route corners | R854-1 | 6ceed75374210935cff4f10d014b9a5ef137615e |


## Scope and public reconstruction

Read AGENTS.md / CONTRIBUTING.md, docs/README.md, issue #665's body and public decisions, the linked requirement and interface contracts, then the source range `659d7687..6ceed753`, first-parent history, both merge resolutions against both parents, and published executable evidence. The incoming already-reviewed histories were inspected for integration effects; this is not a new review of every inherited feature.

Authorities: [sync scope and counterpart ledger](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6899740728), [takeover and validation contract](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6899809056), [phase-spread and composition ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6907491626), [transmit-opportunity and timing-floor ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6930885185), and [review-ready evidence](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6932432594). Interface authorities examined include REQUIREMENTS.md, FR_NFR.md 3.4.1, MAILBOX_SPLIT.md, ARCHITECTURE_HW_SW_SPLIT.md, SPLIT_CONTROL_MEMORY.md and GPTP_PLANE.md.

The published evidence examined is pinned to [archive 2b4066ca](https://github.com/kebag-logic/milan-fpga/tree/2b4066cafdd14e0351f6d73d0f59608f93577ce1/review-evidence/sync1115-r1), author-r1 through author-r3. No private author material or another review report was used. After the independent diff pass, the PR's combined public discussion/review timeline was checked: it contained only the two review-start notices, no previous FINDINGS to resolve or retain. The public STOP and manager rulings were reconciled as below.

## Composition checks

`composition-audit.txt` records both ordered parents, the ten first-merge conflict paths and two second-merge paths, hashes of their diffs against each parent, all submodule gitlinks and the fast-forward checks.

| Artifact / resolution | Independent result |
|---|---|
| 62625941, MAILBOX_SPLIT.md | The incoming sentence-per-line status retains the split's S1 faces and S6 placement switch; the transition/default condition remains explicit. |
| 62625941, MARK_II_AREA_PLAN.md | The new Mark II target summary retains the measured integrated split route. b84d095a/d2da3159 correctly distinguish #810's merged state and the split's approved 20 ms from the older dev wording. |
| 62625941, FR_NFR.md | RV32IM/cache ownership from the split, firmware-only end state from dev, and the approved 20 ms budget coexist. Audio and gPTP deadline ownership remain separate. |
| 62625941, endstation_builder.py | Both return keys survive: split `nvm_split` and dev `warnings`. Both parents' consumers remain connected. |
| 62625941, milan_dp/Makefile and README | Both split and bootsa execution cases survive, with both option definitions and clean targets; both documentation sections survive. |
| Submodule diagram / PNG_MANIFEST | Generated boundaries represent all six exact merged gitlinks. Independent generator --check passes, including decoded PNG verification. |
| flash_layout.png | Independent rendering from the merged SVG at width 1800 matches the tracked PNG byte for byte. |
| 10b2fe21, SPLIT_CONTROL_MEMORY.md | #901's section-5 rewrite is retained along with the sync's image delta. 30c5d3d6 restates that delta as 32-40 B ROM, no tile movement. |
| 10b2fe21, milan_dp/README | The 28 split plants, 14 remaining twin plants and #901 srptx description all survive. No code conflict in this merge. |
| f5750b3d / 4cb7d7ab audit regeneration | Independent docs_inventory --check reports the 540-line audit current at the reviewed head. |

Pins at the reviewed head: gptp-processor `1616fc8f062fbf58c35ad31674b5b233207bbdb8`; protocol-processor `801ef2283ec793e35a2590fc6593c90313a64041`; tsn-c-stack `715589c1db7cf67e2f3259fd7083ebc7f0923376`. The processor pair fast-forward from the split pins to dev's pins. The stack retains the split pin, descended from dev's 70936b77. No other gitlink changes; the second merge changes none.

The semantic conflict repairs are necessary and locally coherent:

- **a563a83d / dfcd8eed:** the merged split producer drove the post-gate net while dev's gate read undriven `pp_txs_tvalid_w`. The producer now drives the held valid/ready pair, just as the fabric producer does. Both ready and valid are suppressed before both MAC halves are written; the gate never drops during a frame. The split firmware writes both halves in ctrl_plat_csr.c:38. The focused split simulation passes 84 checks. Both new source plants were independently rebuilt and caught by the named pre-MAC and low-half-only checks in sim_split.cpp:546/549.
- **d8c8c4b7 / 1facd42e:** the twin's identity-derived stimulus follows the config's new MAC. The changed MAC also changes the LeaveAll random phase. The published twin plant receipt catches `leave-all-omission` at 27510 ms by the Domain's missing Table 10-3 txLA message; the identity-only receipt exposes the old owed rows as no longer true.
- **3c94c76c:** deletion of four owed rows and their six “fix-the-old-defect” plants is supported by actual processor fixes, not merely a pin label. Processor commit `db131cb2` adds per-interface last-advertised index capture in KL_adp_engine, routes it through protocol_processor_top and overlays ENTITY bytes 36-39 in the microcode generator (#858). Commit `f2475333` adds Domain/VID Table 10-3 Applicants, per-VID registration and MVRP LeaveAll transmission without a pending VID (#857/#860); `b655100` completes link-edge reset behavior. All are ancestors of 801ef228. The normal comparison/Applicant grading remains, so removal does not create an allowance for those old defects.
- **9715a30a:** the five new private hierarchy reads correctly use `g_af_pp.pp_shadow`, matching the actual generate branch at milan_datapath.sv:9703 and the other existing reads. Published replacement runs pass pp_shadow and bootsa; no RTL is changed by this repair.
- **6ceed753:** no firmware, RTL or numeric bound changes. The basic single-participant opportunity calculation and late/absent/skipped controls work. R854-001 prevents acceptance of its multi-participant conformance claim.

[R854] PASS RTL - hdl/milan/milan_datapath.sv:9010 and :10214; tb/verilator/milan_dp/sim_split.cpp:546; composition-audit.txt; split-clean.log; split-plants.log - both ownership branches retain the transmit gate, its held handshake, reset behavior and station-address initialization order. The sync adds no CDC primitive or crossing. The split remains on the existing mailbox crossings, and fabric gPTP remains independently enabled.

## Processor-fix counterparts and image propagation

| Incoming fix | Split counterpart examined | Test evidence examined |
|---|---|---|
| #847, pre-settle Talker registration and link changes | srp_mbx.c binding invalidation/snapshot, registration refresh and reset/reopen paths | srp_mbx.cpp:1430, HeldRegistrationsAreWhatAWalkCopiesAfterEveryStep; srp_mutants.py:903 binding-change-not-copied. The test includes binding an already registered Talker and both link edges. |
| #852, one vector per value | lwSRP mrp_mad.c's attribute iteration and mrp_transmit packing | srptx wire uniqueness grade and doubled-declaration plant. Overall srptx timing failure is the explicitly excluded #916; it is not represented here as a passing whole leg. |
| #893 / #857, LeaveAll with nothing declared | lwSRP LeaveAll state and empty-attribute transmission path, mrp_mad.c:779 and :1435 | twin's per-participant LeaveAll grade; published plant receipts. |
| #893 / #860, second New and JoinIn only while registered | lwSRP Applicant table and event selection, mrp_mad.c:149 and :1278 | twin Table 10-3 grade, mvrp-join-in and mvrp-received-join plants. |
| #893 / #858, ENTITY available_index | ctrl_app_aecp.c:113 reads the last advertised index | test_aecp.cpp:533 App.EntityReadSeesTheLastAdvertisedIndex; app-available-index-next and app-available-index-unguarded mutations. |

For #843, inspected gPTP changes `c0bb53b` (received-Announce deadline/timeout ordering), `434527a` (Follow_Up TLV-chain walk), `13670a0` and `711ff07` (late Pdelay bound and tolerance), and their engine/parser tests. They are contained in 1616fc8f. milan_datapath.sv:9160 builds the engine on GPTP_PLANE_EN_P independently of CTRL_SPLIT_P, so the split retains these fixes.

Independent in-memory image derivation (`check_identity.py`, `identity.log`) confirms **both split configs** emit the MAC 02:4b:4c:4b:4c:01 and clockAccuracy 0x22 to engine generation. It also reads the generated AEM bytes: AVB_INTERFACE MAC, EUI-64 clock identity 024b4cfffe4b4c01 and accuracy 0x22. This checks bytes, not just YAML text. The firmware serves that image and its platform initialization writes the matching station MAC. #919's split MDIO/1000BASE-T-only work remains outside this sync.

## Executable evidence and its limits

Own focused execution, with raw logs and rc files in this packet:

| Command / probe | Result |
|---|---|
| ctrl_service_budget/selftest.py | 871 PASS checks; 254 mutants caught; self-test 0 failures, rc 0. The eight new mutant receipts are also extracted separately. |
| probe_leaveall.py | Overlapping-participant skipped LeaveAll escapes; matching clean control passes; single-participant late control fails. Reproducer assertions pass, rc 0. |
| make -j16 milan_dp build-split, then split binary | Build rc 0; 84 checks, 0 failures. |
| probe_split_gates.py | Two independent builds, six compilation jobs each; both source plants caught by name, each simulation rc 1 as required; campaign rc 0. |
| flip_grade.py --check --point 1x1/1if | PASS; tx 34.00 ms and txL 48.58 ms within 49 ms. |
| load_grade.py --check | PASS; 1x1/1if 0.517 at pin and 0.514 with the stated alternative stack costs, below 0.70. |
| check_identity.py | Both split AEM images and engine arguments pass. |
| docs_inventory.py --check; submodule_boundaries.gen.py --check | Both pass. |
| merged flash SVG rendering; git diff --check | Exact PNG match; no diff whitespace errors. |
| verify_source.py before and after | Exact tracked blob bytes, executable/symlink modes, complete index and all initialized submodule gitlinks match. No tracked edits required restoration. |

The scoped compiler identity was verified as version 5.050 before the focused build. No full parent, processor, gPTP, synthesis or builder bank was executed by this review.

Published gates were read as **author source-head evidence**, not manager execution:

- Independent rc census: all four workflows at 9715a30a have 154 executed steps with rc 0; 256 other steps have recorded NOT RUN reasons. Exact-head documentation receipts at 6ceed753 have 63 executed steps with rc 0 and 34 NOT RUN reasons. Skipped or orchestration-only steps are not counted as executed jobs.
- The four sweep shards contain 65 suites. At 4cb7d7ab, 62 pass, milan_dp and pp_shadow fail to compile, and milan_dp_gm_steps times out. Replacement receipts at 9715a30a clear all three: 14,018 / 2,571 / 202 checks respectively, zero failures. Thus the combined source evidence supports 65 passing suites; the interrupted/failed attempts themselves do not. The final 6ceed753 delta changes only the budget grader, self-tests and documentation; its own self-test was rerun independently here.
- The published model self-tests record 585 flip controls, 26 load controls, 11 record-class controls and 1,033 tier-model controls refused. The live flip/load checks were also rerun here.
- The author-r3 regrade receipts report all eleven 8x8/1if phases, 44 LeaveAlls, with maxima 1.64 ms LeaveAll, 2.97 ms periodic and 1.86 ms join. The 1x1/1if valid-destinations leg reports rc 0. These receipts exist and use the new grading; **R854-001 means their “first opportunity for every participant” conclusion is not established**. Raw CPU executions were not reproduced by this review.
- Published image receipts show each image's ROM growth of 32-40 B, unchanged tile allocations, and platform 8x8/1if at 56 tiles with 848 B ROM headroom. These are build measurements, not physical calibration.

Independent regrading of all 15 route receipts checks four corners per directive and #818's actual floors, +0.030 ns setup / 0 ns hold, best of three:

| Image | Best directive | Worst setup / hold across corners, ns | Result |
|---|---|---|---|
| split 1x1/1if, second-merge image | ExtraTimingOpt | +0.196 / +0.036 | Meets |
| split 8x8/1if | AltSpreadLogic_high | +0.140 / +0.036 | Meets; only this directive meets setup |
| release AX7101 1x1 | AltSpreadLogic_high | +0.209 / +0.016 | Meets |

The split 8x8 alternatives are +0.014 and -0.595 ns setup and do not meet the floor. Positive hold values below +0.030 are passes under the corrected ruling. Earlier signoff “ruling floor” failures were regraded; they were not silently treated as green. No new route was run here.

The release export evidence has a precise limit: gateware matches **after path/generation normalization and exclusion of comment-only hierarchy ordering**, backed by identical six-shape placement digests. It is not literal equality of every raw export file or of the complete firmware/CSR export; the receipts explicitly show software/path differences and the split branch's journal reservation. No bitstream equality or hardware behavior is inferred.

## Pending manager duties and exclusions

This is a completed negative source review, not merge authorization. Fix R854-001 and independently re-review its four affected lenses at the new exact head. Regrade the eleven phases and #901 valid-destinations evidence with participant ownership established.

The known 305-versus-300 us paced SET_CONFIGURATION mismatch awaits #898 and the required composed regrade; this sync does not alter the constants. The 8x8/1if STATED lines belong to #914. #929 twin, #916 srptx and #919 split PHY work remain the explicitly excluded issues, not new findings. The public phase-spread STOP is reconciled through the Q1 ruling and published regrades, subject to R854-001.

There is **no manager source-bank execution at this head**. The manager still owns hosted/act acceptance, the final live-dev/train merge-candidate builder and native banks, receipt publication, independent review completion, authorized merge and post-merge containment. Source base 659d7687 and incoming live dev 6b66f66d89cf25d2717687bcc2c3bf617685a99a are distinct from that future candidate. No GitHub writes, source fixes, commits, pushes, merges, author contact, delegation, containers or hardware operations were performed here.

Physical calibration remains NOT RUN. Field skips, simulation, route timing and image derivation do not provide hardware proof. This packet contains only focused review evidence; scratch trees are excluded from publication. MANIFEST.sha256 lists every publishable file. Three compilation logs retain command/output text with the home-directory prefix replaced by <home>; original logs remain unpublished under scratch/. No result or measurement was changed.

R854-1 FINISHED

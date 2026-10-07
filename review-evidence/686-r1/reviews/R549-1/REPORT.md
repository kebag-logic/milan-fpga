[R549] NEGATIVE - exact head c7b69cd0fb2bdf980546ab413b3b82198267cbd8

Round R549-1, external independent review of issue #686 / PR #695. Tree: `f391905e7afd3485edc9d21ab317dd0802959c45`. Source base: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.

All five lenses were applied. One MAJOR timer-randomization defect, two MINOR documentation-contract findings and one MAJOR public-evidence gap remain open. This is a source-head review, not approval of a current-dev merge candidate or hardware acceptance.

The repository's 120 checks pass, all 22 planted RTL defects fail their named checks, and the differential passes its 12 cases and catches all 16 controls. The independent range/state matrix passes 144 cases. These positive results do not cover the failing reset-MAC boundary described below.

**Reconstruction and independence**

The review read AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, linked requirements and interfaces, the complete 19-path diff and five-commit history, then public evidence. The authority was the IEEE 1722-2016 PDF, including visual inspection of Table B.7 on printed page 159 / PDF page 171. Its SHA-256 is `ba20762d444e6f7795ffc000bcaf6144e9618eff81cadd867863ed58000f8a8c`. Clauses are cited here without reproducing the standard.

Public scope: [issue #686](https://github.com/kebag-logic/milan-fpga/issues/686), [assignment 6043036997](https://github.com/kebag-logic/milan-fpga/issues/686#issuecomment-6043036997), [TAKEN 6043296747](https://github.com/kebag-logic/milan-fpga/issues/686#issuecomment-6043296747), and [review start](https://github.com/kebag-logic/milan-fpga/pull/695#issuecomment-6047116152). The fourth-PROBE addition is comment 6029233665. Bench interoperability is explicitly the manager's post-merge duty.

No private author material, other checkout, or other reviewer's report was read. The independent pass was recorded before querying prior public findings. At that query, PR #695 had zero submitted reviews, zero inline comments, and only the two review-start comments. There were no prior public PR findings to resolve or retain. `receipts/public-evidence-inventory.txt` records that observation.

**Findings**

[R549] R549-1-F1 MAJOR Conformance, RTL, Robustness, Tests, Docs - `hdl/ieee1722/maap/KL_maap.sv:161`, `:278`; `tb/verilator/maap/sim_main.cpp:45`; `docs/design/MAAP_FABRIC.md:85` - A legal reset MAC freezes both timer draws.

Authority/evidence: B.3.4.1 and B.3.4.2 require random timer values within their respective bounds. With `station_mac_i = 02:00:00:00:AC:E1` during reset, the seed expression is `ACE1 XOR ACE1 XOR 0000 = 0000`. The feedback at `KL_maap.sv:139` preserves zero forever. Consequently the in-scope timer draws at lines 161-162 remain 518 ms and 30,488 ms. The independent probe uses a valid provisioned offset `0x4000` and count 8, bypassing initial random address generation. Over 24 announcements, after excluding the first tick-phase transient, every interval is 304,880 scaled cycles. The normal-MAC control produces 23 distinct intervals in the same window. Both configurations remain numerically inside the strict timer bounds. See `scripts/probe.cpp` and `receipts/probe.log`; the latter returns 1 and explicitly fails `zero-state MAC randomized announce`.

Impact: item 2 is only partially conformed. For this valid input class the intervals are deterministic constants, preserving synchronized transmissions instead of randomizing them. The existing default-MAC harness and its constant-announcement mutant do not exercise this reset boundary. The new statement that successive intervals differ is false for it.

Scope: the reset expression predates this PR. This finding does not demand the deferred B.3.6.1 generator-period, uniform-address-distribution or real-time-clock-seed redesign. It concerns the timer draws expressly covered by item 2, including when a provisioned address avoids `generate_address`. The public deferred-address-generator list does not establish a clause justification for a constant timer sequence.

Required outcome: timer randomness must remain live for every supported reset identity, with the zero-state boundary explicitly tested. Preserve the strict timer bounds. Any proposed exclusion of this input or of timer randomness needs a public requirements/scope decision; it cannot be inferred from the address-generator deferral.

Verification: rerun the normal and zero-state identity controls, require nonconstant timer draws in both, retain strict 500/600 ms and 30/32 s checks, and rerun the named mutation campaign. A clean re-review must cover this boundary at the corrected head.

[R549] R549-1-F2 MINOR Docs - `docs/design/MAAP_FABRIC.md:62`; `hdl/ieee1722/maap/KL_maap.sv:213`; PR #695 Description - The new all-fields snapshot claim exceeds the implemented snapshot.

Authority/evidence: the new contract says every per-frame field is latched at the send request. The builder reads `station_mac_i` live at line 229 and `count_i` live at line 238. In the independent probe, a DEFEND is stopped at beat 4 with valid asserted and ready low. Changing count from 8 to 9 changes that held word from `004000f0e0910800` to `004000f0e0910900`. The CSR write path does not clamp or freeze this field (`hdl/common/csr/milan_csr.sv:1705`, `:2818`). The requested offset and DEFEND destination snapshots do pass their existing checks.

Impact: an integrator cannot rely on the documented all-fields snapshot during configuration changes. The unchanged live inputs are broader than the Restart/next-PDU protection actually added. This is a new contract overstatement, not an assertion that this PR introduced the old live-input behavior.

Required outcome: qualify all three new claims. A precise correction is: the message type, DEFEND destination and conflict fields, and requested offset are latched at send; station MAC and count remain live configuration inputs, so this snapshot does not protect their reconfiguration during a frame. If the intended contract instead promises full snapshot protection, implement and test that contract through the public scope process.

Verification: compare the corrected banner, MAAP_FABRIC contract and PR description with the builder's actual dependencies; retain the destination/offset stability checks. The probe provides a reproducible counterexample to the current prose. This is MINOR rather than RESIDUE because it changes an interface guarantee.

[R549] R549-1-F3 MINOR Docs - `docs/design/MAAP_FABRIC.md:52` - The new unconditional pool-containment claim excludes the supplied-seed path.

Authority/evidence: the paragraph cites Table B.9 and says the claimed block always fits inside the dynamic pool. `KL_maap.sv:268` passes a supplied seed through unchanged. With `seed_valid_i=1`, offset `0xFEFF` and count 8, the four-PROBE walk completes and `addr_valid_o=1` while the block lies beyond the `0xFE00` dynamic pool. See `receipts/probe.log`. The clipped unseeded generator at lines 153-157 does not protect this path.

Impact: the new B.4 contract claims input validation the module does not provide. Provisioning software could rely on that claim and advertise an invalid dynamic-pool allocation. This inherited supplied-seed behavior is not being relabelled as a new generator implementation change.

Required outcome: replace the unconditional claim with its actual bounds: randomly generated blocks are clipped to the pool; supplied seeds are used without range validation and require a valid provisioned range. If unconditional containment is intended, settle and implement the necessary validation explicitly.

Verification: review the corrected claim against both arms of `new_off_w`; retain the invalid-seed counterexample. This is MINOR, not RESIDUE: the false sentence makes a substantive clause/conformance claim.

[R549] R549-1-F4 MAJOR Conformance, RTL, Tests, Docs - [pinned public evidence tree](https://github.com/kebag-logic/milan-fpga/tree/942a9f718ba3b2ba472bd3750935dc84b33a9938/review-evidence/686-r1); `syn/ooc/pp_resource_baseline.json` - The replacement resource records cannot be matched to public executable receipts.

Authority/evidence: the assignment requires recipe re-recording; AGENTS.md sections 1, 5 and 6 require reconstructible public evidence. The specified commit contains only MANIFEST.json, author/HANDOFF.md and author/PR-BODY.md under this packet. Its manifest lists the two prose files. HANDOFF's Area section lists hashes and sizes and explicitly says the measurement artifacts remain in scratch, not copied. No raw route/OOC reports, executed Tcl, input/image manifests, primitive census or manager bank receipts were available at this public snapshot. The issue had the assignment, TAKEN and REVIEW READY statements; the PR had only the two review-start comments. The missing public location was requested while independent checks continued; none was supplied during this review.

Impact: the three newly committed records, particularly their new input digests and per-scope figures, cannot be independently derived from the provided public evidence. Matching the prose totals to the JSON is not a measurement audit. This does not assert that the manager's reported source banks failed or that the area/timing numbers are wrong.

Required outcome: publish or link the raw recipe receipts, preserving an independently checkable association with the measured source tree and processor pins. Supply enough input evidence to regenerate each record, then compare all three regenerated records with the committed JSON. Publish the stated manager source-validation receipts as well. No implementation rerun is requested from this reviewer.

Verification: reconstruct `route-1x1`, `ooc-1x1` and `ooc-8x8` through `pp_resource_gate.py` from those receipts; require record equality including identity, inputs, figures and scopes, and verify route status and timing floors. Re-review the public evidence at the same source head if only evidence publication changes.

No RESIDUE-only finding is reported.

**Clause and architecture results**

| Item / cell | Independent comparison | Result and limits |
|---|---|---|
| B.2.1, Figure B.1: CDL and destinations | `KL_maap.sv:114`, `:223`, `:320`, `:372`; golden frames and destination mutants | CDL is 16 for all three types. PROBE/ANNOUNCE stay multicast; DEFEND uses the triggering source snapshot, including a later-PDU/stall case. |
| B.2.5-B.2.8 / Table B.7 note b | `KL_maap.sv:187`, `:194`, `:330`; unit checks and 144-case independent matrix | PROBE/ANNOUNCE select requested fields; DEFEND selects conflict fields. Half-open comparison, zero counts, both adjacency edges, one-address overlap and 17-bit end sums pass. DEFEND overlap count uses the shared interval correctly. |
| rAnnounce!/INITIAL | `rx_hit_w` at `KL_maap.sv:253`; differential INITIAL cells | No conflict event/state change while disabled. |
| rAnnounce!/PROBE | `KL_maap.sv:261`; unit check, named compare-while-probing mutant and independent matrix | Overlap restarts regardless of MAC ordering. |
| rAnnounce!/DEFEND, note d / B.3.6.4 | `KL_maap.sv:208`, `:260`; below/equal/above MAC matrix and reversed-order mutant | Octet-reversed unsigned comparison; local-lower ignores, equal/higher restarts. No ordinary-order substitution. |
| Table B.8 / B.3.4.1-2 | `KL_maap.sv:120`, `:161`, `:304`; 456 unit PROBE intervals, 24 unit ANNOUNCE intervals, 1024 differential start phases | Strict bounds pass for exercised traffic. Unit PROBE intervals 5172..5810 scaled cycles; differential 5172..5811. Zero-state randomization fails F1. Unbounded downstream stalls are not timing proof. |
| Begin!/ReserveAddress!, Table B.7 | `KL_maap.sv:350`; named first-send/count mutants | Immediate initial PROBE, followed by three retransmissions. Seeded Begin! also checked. |
| Restart!/ReserveAddress! | `KL_maap.sv:363`; restart-delay mutant and conflict checks | Conflict changes range and requests a first PROBE without an interval delay. |
| probetimer!/probeCount! | `KL_maap.sv:379`; fourth-PROBE and immediate-ANNOUNCE checks | Four-PROBE sequence and back-to-back first ANNOUNCE pass under ready transport. |
| Release!, reset and same-cycle priority | `KL_maap.sv:271`, `:306`, `:345`; disable/re-enable checks and independent reset-under-stall | Synchronous active-low reset clears allocation/TX. Disable outranks restart, which outranks DEFEND and scheduled send. NBA ordering preserves a pending frame's captured offset across restart. |
| Interface and integration | unchanged module port list; `milan_datapath.sv:7064`, `:7086`; REGISTER_MAP MAAP rows | Single axis clock; no added CDC, port, CSR/filter/mailbox or state encoding change. Feature-off ties remain inert. Config-dependent limitations are F1-F3. |

The Table B.7 row comparison also identified the already declared exceptions: compare_MAC is absent in rProbe!/PROBE and rDefend!/DEFEND; DEFEND requested fields echo the local range instead of the triggering range; no PortOperational input; address-generator period/distribution/seed limitations; busy-TX PROBEs are dropped; tagged reception is unsupported. These are the public pre-existing scope exclusions, not clause-equivalent behavior and not evidence of complete Annex B compliance. The independent matrix grades the two excluded compare_MAC cells only against their declared retained behavior. RX completion checks beat count, not every header/keep validity condition; this review supplies no comprehensive malformed-frame proof.

**Test and consumer evidence**

| Receipt | Result |
|---|---|
| `receipts/unit.log`, `unit.rc` | 120 checks, zero failures, rc 0. |
| `receipts/mutants.log`, `mutants.rc` | Clean control passes; 22/22 named defects rejected; 23 campaign rows, zero failures, rc 0. Build failure or abnormal exit cannot count as a kill. |
| `receipts/differential.log`, `differential.rc` | 12 clean cases pass; all 16 controls rejected; campaign rc 0. Expected mutant failures in this log are not failures of the clean candidate. |
| `receipts/coverage.log`, `coverage.rc` | Repository line gate 167/167, 100%, passes 95% threshold. Other coverage categories are separately visible; this is not exhaustive path coverage. |
| `receipts/probe.log`, `probe.rc` | Independent 144-case matrix passes; ordinary-MAC control and reset-under-stall pass. Three claim checks fail as detailed in F1-F3; executable rc 1. |
| `receipts/baseline-policy.log`, `baseline-policy.rc` | All endpoint tolerances, floors, ceilings and measurement identities equal the source-base versions. |
| `receipts/check-baseline.log`, `check-baseline.rc` | Repository baseline-policy validation passes all three endpoints. |
| `receipts/tree-integrity.log`, `tree-integrity.rc` | Exact tracked bytes, filesystem modes, full index and all required pins pass. |

`test_maap_differential.cpp:112` now requires equality for the corrected initial frames and `:223` for its DEFEND stimulus. Retry comparisons at `:230` still exclude independently allocated requested-address bytes 26-31; they do not prove literal equality of all retry addresses. Both programs are subjects; Annex B supplied the expectations. The DEFEND equality stimulus uses coincident ranges and does not close the expressly deferred requested-field echo deviation.

The crflic change at `tb/verilator/milan_dp/sim_crf_licence.cpp:832` moves stimulus to the probing interval. It retains the first-probe failure-status assertion and moves the ANNOUNCE assertion/offset read into phase A at line 868. That is a stimulus correction, not a weakened assertion. The reported 417-check/7-row crflic results and broader integration banks were not rerun here. The manager reports full source static/builder/native banks passed at this head; F4 records the limit of public receipt inspection.

**Area, source base and merge collision**

The committed route record and the published summary agree on 50,088 LUT, 54,188 FF, 15,843 slices, 74 RAMB36, 27 RAMB18, 14 DSP, WNS +0.317 ns and WHS +0.036 ns. The stated Yosys OOC change is 637/268 to 474/278, or -163 LUT/+10 FF, within +40/+40. These are reported measurements, not measurements rerun by this review. Raw equality remains open under F4.

The two standalone records retain their figures (23,178/19,776 and 29,853/27,370 LUT/FF), but all three input hashes change. Both OOC timing estimates are negative and are not routed timing closure. The route's asserted recipe is shipping 1x1, ExtraPostPlacementOpt, default seed; its reported route status is 100,981/100,981 nets, zero errors. The route has seven slices of device headroom. The source-base policy remains unchanged, including the +80-slice tolerance and setup/hold floors; the image delta includes earlier dev changes as the updated area documentation states.

Issue #682 independently adopts processor `2ad2f845` and replaces the resource records with baseline F. The second lane to merge must re-record on the actual merge result. Do not choose either lane's JSON by textual conflict resolution. This reviewed source uses base `e21c1ca0`; the supplied live-dev tip `d8b355fe0f41d49dca6cae1cd8b3826e2edde364` is distinct. Current-dev candidate construction and its full validation belong to the manager's merge turn.

**Reviewer-owned completion ledger**

Every row was applied in R549-1; UNCLEAN means an open attributable finding, not an omitted lens. No lens is banked against another head.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F4) | IEEE 1722-2016 B.2.1/B.2.5-B.2.8, Table B.7/B.8, B.3.4/B.3.6.4; issue acceptance; `KL_maap.sv:114`, `:161`, `:194`, `:253`, `:350`; `receipts/probe.log` | R549-1 | c7b69cd0fb2bdf980546ab413b3b82198267cbd8 |
| RTL | UNCLEAN (F1, F4) | Full `KL_maap.sv` diff and state/TX/RX/timer logic; `milan_datapath.sv:7064`; CSR connections; baseline identities/policy | R549-1 | c7b69cd0fb2bdf980546ab413b3b82198267cbd8 |
| Robustness | UNCLEAN (F1) | `sim_main.cpp:324`, `:366`, `:410`, `:451`, `:519`; 144 matrix cases, reset and configuration probes in `scripts/probe.cpp` | R549-1 | c7b69cd0fb2bdf980546ab413b3b82198267cbd8 |
| Tests | UNCLEAN (F1, F4) | `tb/verilator/maap/{Makefile,sim_main.cpp,mutants.py}`; differential sources and controls; crflic diff; raw local campaign/coverage receipts; public evidence inventory | R549-1 | c7b69cd0fb2bdf980546ab413b3b82198267cbd8 |
| Docs | UNCLEAN (F1-F4) | All changed Markdown, RTL banner, reader disposition, issue/PR/HANDOFF claims, MAAP contract and area-budget records | R549-1 | c7b69cd0fb2bdf980546ab413b3b82198267cbd8 |

**Limits and pending manager duties**

No source fix, commit, push, GitHub write, merge, author contact, delegated review, full parent/processor/gPTP/Yosys/builder bank, container run, implementation run or hardware operation was performed. Two compile lanes were used at most, each capped at four jobs, with foreground supervision. The supplied simulator identity was verified as 5.050 before use. All disposable build/probe data is in unpublished `scratch/`. No tracked source bytes needed restoration.

The final integrity check verifies parent HEAD/tree, all 1,169 parent entries, and registered submodules: protocol-processor `ead8036035affd53ef4b29979190f2f4f67084c0` (558 entries), gptp-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104), verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214). Filesystem bytes/modes and index entries match, with no assume-unchanged/skip-worktree flags. The intentionally uninitialized external submodule is not a required build input.

`receipts/hosted-snapshot.json` binds observed jobs to this head. At inspection, some jobs had executed successfully, others were queued/running, and the physical gPTP job was skipped. No skipped context is treated as execution evidence, and no aggregate hosted acceptance is claimed. The manager owns hosted/local-replica acceptance and any required reruns.

The manager must resolve/re-review the findings, supply the missing public measurement receipts, obtain both independent positive verdicts with no review in flight, validate the current-dev candidate, reconcile the #682 baseline collision through fresh recording, and complete authorized merge/containment duties. Bench MAAP interoperability remains acceptance item 4 after merge. Physical calibration is NOT RUN; field skips and simulation/resource results are not hardware proof. Issue closure/Done remains subject to those duties.

Portable reproduction is in REPRODUCE.md. MANIFEST.sha256 lists every publishable receipt and script with packet-relative paths. Scratch, the standard PDF/extraction/rendering and other unlisted files are excluded from publication. Logs have only local path spellings replaced by role placeholders; results and diagnostics are retained.

R549-1 FINISHED

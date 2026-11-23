[R890] POSITIVE - exact head 77a74b2f4e289c5a5a89687e07a6925cfedf6860

External independent review, R890-2, issue #972 / PR #974. Source tree: `83462698a273b938f8cc108da7c6581acda83573`. Review baseline: `0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b`; full task range inspected against `dd163e41438acb86e0c4d4e76df90f3f91ace1c0`. This is a source-delta verdict, not merge authorization or physical acceptance.

The independent pass found no open BLOCKER, MAJOR or MINOR. The BMCR correction and reset-down qualification satisfy the public source scope. The independent verdict and ledger below were written before opening either prior reviewer report. Prior findings have now been reconciled below. Untouched code retains its prior verdict; changed dependencies and both prior causes were re-reviewed under every attributable lens.

## Scope and authority

- [Issue #972](https://github.com/kebag-logic/milan-fpga/issues/972): retain a correct negotiation, prevent transmission before verified publication, exercise restart/no-restart with plants, preserve #840, and physically measure discovery at both shipping shapes.
- [Manager scope decision](https://github.com/kebag-logic/milan-fpga/issues/972#issuecomment-7083292610): effective link unqualified from reset in managed split builds, including retained-link reload and refused boot; preserve other configurations; BMCR must enable negotiation before skipping restart.
- [Discovery ruling](https://github.com/kebag-logic/milan-fpga/issues/970#issuecomment-7080789556), [#840](https://github.com/kebag-logic/milan-fpga/issues/840), `REQUIREMENTS.md:311` (REQ-MAC-03), `docs/reference/FR_NFR.md:198`, `docs/reference/REGISTER_MAP.md:519`, and the platform PHY interface govern the review. BMCR interpretation is consistent with IEEE 802.3 Clause 22.2.4.1: enable bit 12, reset bit 15, isolate bit 10; advertised abilities alone do not establish negotiation. The IEEE text was also spot-checked in the [published 2015 Section Two copy](https://www.onetel.de/wp-content/uploads/2016/11/802.3-2015_SECTION2.pdf), clauses 22.2.4.1.4 and 22.2.4.1.6; this is corroboration, not a claim to have independently obtained the complete 2022 edition.
- Only public issue/PR state, repository authorities, committed sources and published evidence were used. No other current-round report was read.

## Results by lens

[R890] PASS Conformance - `sw/firmware/ctrl/plat/ctrl_plat_phy.c:120,204,255`; `docs/reference/FR_NFR.md:198` - The boot skip requires AN enabled and reset/isolate clear plus the retained advertisement. Managed forced/isolate/reset states publish down and owe renegotiation; non-target PHY compatibility remains. The unchanged outcome/readback checks reject the lower-speed negotiation. ADP production constants and the stack pin are unchanged; the 4,311 ms derivation remains distinct from the unmeasured physical 6.0 s acceptance.

[R890] PASS RTL - `sw/litex/mac_link_status.py:28`; `sw/litex/milan_soc.py:2031,2062,3930`; `hdl/milan/milan_datapath.sv:3407,8812,10221`; published `author-r3/receipts/gateware/` and `vivado/` - The real split MAC receives ownership from `ctrl_mailbox`, further conditioned on MDIO presence, and initializes link status to 12. The existing two-flop link crossing starts down. In the effective-link AND expression neither LINK_CTRL nor the guard can override that zero. Leaving those two existing factors unchanged satisfies the effective-link decision. The split has firmware MAAP through mailbox LINK. No new clock/reset cone or CDC mechanism is introduced. Generated/routed status receipts and both shipping-shape timing receipts support the wiring and fit.

[R890] PASS Robustness - `sw/firmware/ctrl/test/test_plat_phy.cpp:940`; `sw/firmware/ctrl/test/test_plat_boot.cpp:1327`; `tb/verilator/milan_dp/sim_link_reset.cpp:218`; `phy-head.log`, `phy-prior.log` - Inspected forced 10/100/1000, reset/isolate, loss, dropped restart, read failure, healthy retained negotiation, no-MDIO, identity refusal, CPU-only arm publication and retained-clock reload paths. The isolated current suite passes all 57 tests; the prior PHY implementation fails exactly P22/P23 under the same current suite. The integration arms keep effective link and mailbox LINK down until publication and send no frame on refused boot.

[R890] PASS Tests - `sw/firmware/ctrl/test/plat_mutants.py:599`; `tb/verilator/milan_dp/Makefile:910`; `tb/verilator/milan_dp/linkreset_plants.py:33`; published `author-r3/receipts/tests/`, `linkreset/`, `gates/77a74b2f/` - New tests fail at the former cause, not merely on a changed expected value. The independent prior-code run gives 27 failing P22 assertions and 13 P23 assertions, two failed tests, with the other 55 passing. Published plants cover ignored BMCR, ignored isolate/reset, forced publication and over-broad refusal. Both retained-link models execute the real datapath and firmware CSR policy, observe actual MAC frames and require post-publication progress. Reset-up plants fail on an actual early frame at both shapes. Counter expectations change consistently with removal of the spurious boot down/up pair; P20 still catches a removed arm write.

[R890] PASS Docs - `sw/firmware/ctrl/plat/ctrl_plat_phy.h:49`; platform README; `docs/reference/REGISTER_MAP.md:519`; `scripts/register_descriptions.json:1266`; `tb/verilator/milan_dp/README.md:1977`; published REVIEW-READY and HANDOFF-r3 - The operative reset, BMCR and ownership contracts, generated register descriptions, integration boundary and evidence limits are documented. Reviewed the full delta and source-comment additions. Pure wording corrections below do not change code, test results, measurements or conformance decisions.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | PHY negotiation/publication paths; #972/#840 decisions; REQ-MAC-03; FR_NFR discovery derivation; unchanged stack gitlink | R890-2 | 77a74b2f4e289c5a5a89687e07a6925cfedf6860 |
| RTL | CLEAN | MilanMAC reset and crossing; effective-link consumers; generated/routed reset receipts; six route/corner receipts | R890-2 | 77a74b2f4e289c5a5a89687e07a6925cfedf6860 |
| Robustness | CLEAN | P19-P23, B11/L2/L4; refused/published retained-clock integration arms; prior/current platform probes | R890-2 | 77a74b2f4e289c5a5a89687e07a6925cfedf6860 |
| Tests | CLEAN | PHY plants; linkreset harness/Makefile/plants; firmware shards; split boot; twin; CPU/image evidence and source ancestry | R890-2 | 77a74b2f4e289c5a5a89687e07a6925cfedf6860 |
| Docs | CLEAN | PHY interface/README; register generator/map; FR_NFR; changelog; integration README; published evidence and public scope | R890-2 | 77a74b2f4e289c5a5a89687e07a6925cfedf6860 |

## New wording findings

R890-2-F1 - RESIDUE - Docs - PR #974, Linked Issue / roles.
Authority/evidence: public review starts identify R889 as internal and R890 as external. The PR body reverses their previous roles and retains unassigned placeholders.
Impact: stale review-role prose; no verdict or coverage is changed by this correction.
Required outcome: write `Internal cleared-context reviewer: [R889]` and `External reviewer: [R890]`.
Verification: compare the revised role lines with the two public review-start comments.

R890-2-F2 - RESIDUE - Docs - `sw/litex/mac_link_status.py:18`.
Authority/evidence: `docs/reference/REGISTER_MAP.md:532` and the all-fabric PHY path state that all-fabric firmware publishes link status. The helper's introductory description groups all-fabric with no-MDIO and says nothing publishes there.
Impact: imprecise description of the compatibility branch; the actual ownership predicate, reset values and all-fabric code are correct and unchanged.
Required outcome: replace that paragraph with: `Without this split PHY poll, the word keeps its reset at link up. The all-fabric placement retains its separate firmware publication path. Boards without an MDIO pair retain the reset value.`
Verification: prose agrees with the register contract; no source expression, generated reset or behavior changes.

R890-2-F3 - RESIDUE - Docs - published `author-r3/HANDOFF-r3.md`, changed-files row for `tb/verilator/milan_dp/gen_gptp_leg_ucode.py`.
Authority/evidence: the diff adds `--clk-hz`; the handoff calls it stream-count parameterization.
Impact: the changed-files description names the wrong option; commands and recorded results already use the correct clock option.
Required outcome: replace the reason with `Parameterize the generated image clock for the linkreset leg.`
Verification: compare the revised sentence with the `--clk-hz` diff.

R890-2-F4 - RESIDUE - Docs - `tb/verilator/milan_dp/Makefile:915`.
Authority/evidence: the introductory comment says publication at 200 ms; the actual `LINKRESET_PUBLISH_MS` at line 936, invocation, README and published receipts consistently use 1,500 ms.
Impact: stale explanatory comment only. The executed schedule, measured early-frame result and test verdict are already consistent.
Required outcome: replace `(the firmware's publication at 200 ms)` with `(the firmware's publication at LINKRESET_PUBLISH_MS)`. Leave the executable parameter and receipts unchanged.
Verification: the comment refers to the existing parameter; no test, measurement or generated artifact changes.

## Prior public findings reconciled

Read after the independent verdict/ledger checkpoint: [R890-1](https://github.com/kebag-logic/milan-fpga/pull/974#issuecomment-7083175046) and [R889-1](https://github.com/kebag-logic/milan-fpga/pull/974#issuecomment-7083285446), including their reports at the named evidence snapshot. No current-round report was consulted.

| Prior finding | Original severity and lenses | Disposition at this head | Verification |
|---|---|---|---|
| R890-1-F1 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED | `negotiating()` guards both retained-advertisement skip and managed-PHY publication. Public BMCR scope decision recorded. P19/P21/P22/P23 pass in the independent 57-test run; prior implementation fails P22/P23. Published exact prior scenario now gives BMCR 0x3100, publication 0, one restart; five BMCR plants caught. Header/README describe the condition. |
| R889-1-F1 | MINOR; Conformance, Robustness, Tests, Docs | RESOLVED | Same cause and correction; forced and isolated cases covered. No relabeling of its original lenses. |
| R890-1-F2 | MAJOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED | Manager kept the no-transmit acceptance; actual managed split CSR resets to 12, both existing qualifying factors cannot override it. B11 covers identity refusal; P20 retains arm-write sensitivity. Four real-datapath arms and both actual early-frame plants cover both shipping shapes; generated/routed CSR receipts confirm the product reset. |
| R889-1-F2 | MINOR; Conformance, RTL, Robustness | RESOLVED | Public scope decision and same reset-to-publication correction/evidence; no acceptance waiver or deferred defect. |
| R890-1-F3 / R889-1-F3 | RESIDUE; Docs | RESOLVED | `sw/firmware/ctrl/test/adp_first_mutants.py:40` now starts `# #970:` and retains the behavior/clause explanation. |
| R889-1-S1 | SUGGESTION; Tests | RETAINED, optional; does not unclean Tests | G1/G5/G2 spread tests remain unchanged. PR limitations now explicitly distinguish fixed-seed regression coverage from statistical proof. |

R889-1-S1 - SUGGESTION - Tests - `sw/firmware/ctrl/test/test_adp.cpp:715,747` (G1/G5/G2 spread checks).
Authority/evidence: tests use fixed clock/entity seeds and finite bin thresholds; the source delta leaves them unchanged. Original suggestion remains optional.
Impact: changing the seed can change whether a correct generator meets these finite regression thresholds.
Optional outcome: make the fixed regression seed explicit, or separately design a less seed-sensitive distribution check without weakening the required narrowing plants.
Verification if taken: repeat the named ADP plants and fixed-seed controls; keep production 4,000/2,000 ms intervals and both GM orders intact. No statistical rate is independently remeasured in this round.

## Evidence provenance and verification

The evidence snapshot is [f6dd644d](https://github.com/kebag-logic/milan-fpga/tree/f6dd644d37fe4035aa263fc05e8da3524f3c3fcc/review-evidence/972-r1). `verify_packet.py` verified all 339 author-file SHA-256 values against `MANIFEST.json`'s published hashes. Redacted published bytes are checked against published hashes, not original unredacted hashes. The commit contains no cryptographic signature; no separate signature was supplied. This proves consistency with the named public snapshot, not signer authentication or independent execution of all gates.

Independent execution: `python3 -B probe_phy.py <review-clone>` ran current and prior PHY implementations concurrently in disposable trees, eight compile jobs each (16 total). Current: rc 0, 57/57 tests. Prior: rc 1, 55/57 tests, exactly P22/P23 fail. No candidate source was edited. The scoped simulation executable identity was inspected as version 5.050 before any potential simulation use; no additional full simulation bank was run.

Published receipts were inspected by section and spot-checked against their executable causes:

| Evidence | Result and scope |
|---|---|
| Firmware four shards at 77a74b2f | All conclude PASS/rc 0; 75 suite verdicts; control campaign 837/837 caught, including five BMCR plants. |
| Linkreset at 77a74b2f | Four arms pass; zero frames before publication; first frame 0.032 ms after it. Two reset-up plants emit an early frame at 1200.069 ms and fail. |
| Split boot at 77a74b2f | Both shapes pass; ready 27.940/67.214 ms; 6/6 native controls, 7/7 plants, 8/8 placement controls. This measures the PHY code separately from CPU budget rows. |
| Twin and coverage at d9e1d728 | All four twin targets pass; coverage checks pass for 40 files. Later changes do not change their production inputs. |
| CPU rows at fc7504f1 | Nine groups per shipping shape; 63/63 paired probes equal per shape; no changed verdicts or misses. Harness images identical. This harness excludes the platform PHY. |
| Images at production code 93d9eaaf / ledger fc7504f1 | Four platform points fit 45/46/58/63 RAMB36; ROM +40 B versus prior round; only the PHY object changes; size fixtures unchanged. 8x8/1if uses exactly 139,264/139,264 ROM bytes. |
| Routes at 93d9eaaf | Six recipes meet the +0.030 ns setup / nonnegative hold floor at all four corners. Selected ExtraPostPlacementOpt: 1x1 +0.331/+0.031 ns; 8x8 +0.176/+0.036 ns. Production gateware/firmware are unchanged afterward; later edits affect comments, tests and documentation. |
| Parent native source sweep at 77a74b2f | Author receipts: 65/65 suites, 2,713,969 checks. Interrupted shard 2 is not counted; its completed whole-shard rerun is. No manager source bank is claimed. |
| Other source gates | Published synthesis portability, lint, 511 behavior scenarios, front-end and 104 documentation steps pass. Builder legs retain two explicitly NOT RUN arms; neither is counted as executed. |

## Limits and pending manager duties

- This is the source-head review, separate from the current-dev merge candidate. Exact-head hosted jobs were not independently adjudicated; no skipped context is counted as executed here. The manager must construct and validate that candidate, including builder/native banks, publish its exact commit/tree and receipts, complete hosted/act acceptance, obtain the independent review bar, then perform authorized merge and containment. The recorded PR base is not the live validation base. The supplied live-dev tip is `e275d7950ef3385753e6a15d2e191ba855b171ed`; refresh it at the merge turn. This review did not run a manager source bank or infer one from author receipts.
- Physical calibration NOT RUN and field skips are not hardware proof. The first-ENTITY_AVAILABLE measurement at 1x1/1if and 8x8/1if, including both GM orders, remains pending. No physical discovery acceptance, power-cycle result or hardware timing measurement is claimed.
- The linkreset leg models status crossing/retained clocks and omits physical PHY, full CPU and mailbox internals. It observes the actual datapath's mailbox LINK output and transmit boundary. It runs by name outside the hosted ordinary-case inventory. Host models are not silicon evidence.
- CPU-only reset retains the CSR until the arm writes down; the proved reset-to-publication barrier is for datapath/SoC reset and configuration reload. The existing arm-write test covers the separate CPU-only behavior without claiming that CPU reset itself resets the datapath CSR.
- ADP finite fixed-seed spread checks are regression evidence, not a general statistical proof. The production stack stays pinned at `715589c1db7cf67e2f3259fd7083ebc7f0923376`; separate stack test-only PR #36 requires no parent pin movement.
- No source fixes, commits, pushes, GitHub writes, hardware access or merge were performed. Final raw-byte, executable-mode and complete stage-zero index checks pass for the parent (1,940 blobs) and all five initialized submodules (1,362 blobs). Required gitlinks and the unused, uninitialized external gitlink are unchanged from the task base. `checkout-integrity.txt` records this; `MANIFEST.sha256` lists every publishable receipt and script, excluding all disposable trees.

R890-2 FINISHED

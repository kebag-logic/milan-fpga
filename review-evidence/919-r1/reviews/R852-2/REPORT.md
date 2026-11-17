[R852] POSITIVE - exact head 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84

External independent review R852-2, issue #919 / PR #933. All five lenses are CLEAN for this source-head delta. The prior MAJOR and MINOR findings are resolved at their causes. No new BLOCKER, MAJOR, MINOR or RESIDUE was found. Previously published optional suggestions remain optional below. This is source review, not a declaration that the issue's physical acceptance or merge bar is complete.

Tree: `6a9d88680c7222514a0186e8ba8351e62b2d3514`. Delta baseline: `afa3ea19d6a1075382c63e4fc1e188a9aadf33bb`. Original source base: `659d76871221847cfcdaad0ff01e860c2583fd56`. Seven delta commits change eleven paths; no RTL, mailbox implementation, CPU-budget harness or release-firmware input changed in that delta.

Authority and independence

Reconstruction used AGENTS.md / CONTRIBUTING.md, docs/README.md, [issue #919](https://github.com/kebag-logic/milan-fpga/issues/919), its [advertisement scope addition](https://github.com/kebag-logic/milan-fpga/issues/919#issuecomment-6907491954), [#840's gigabit-only decision](https://github.com/kebag-logic/milan-fpga/issues/840), REQ-MAC-03, REGISTER_MAP.md:415-428, ctrl_loop.h:121-144 and the split-memory contract. The original-base change inventory/history and relevant integration diff were distinguished from the seven later commits. Untouched dependencies retain the previous review's examination; the repaired restart mechanism was assessed through all five lenses.

The IEEE 802.3 Clause-22/28 mechanisms applied here are the advertisement/restart relationship, restart's self-clearing bit, BMSR's latched-low link and autonegotiation-complete indication, and the register-9/10 common-mode relationship. This round does not claim a fresh audit of a complete IEEE edition. Milan v1.2 4.2.6.2.5 and the AVB_INTERFACE counter contract remain the unchanged downstream duties.

Public execution evidence is the author archive [d8bc5057](https://github.com/kebag-logic/milan-fpga/tree/d8bc5057f25ee85a2f19bd3a4149e7919dd7465d/review-evidence/919-r1), specifically `author-r3/receipts` and `author-r4/receipts`, and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/919#issuecomment-6934522568). Paths beginning `author-r4/` below are relative to that immutable archive directory.

The independent verdict and five-lens ledger were written before reading the prior public review bodies. Only then were [R852-1](https://github.com/kebag-logic/milan-fpga/pull/933#issuecomment-6929889363) and [R851-1](https://github.com/kebag-logic/milan-fpga/pull/933#issuecomment-6930496445) read to reconcile findings. No current-round peer report, private author material or private management material was read. No source fix or GitHub write was made.

Prior findings resolved at this head

| ID and original severity | All attributable lenses | Resolution and verification |
|---|---|---|
| R852-F1 / R851-F1, MAJOR | Conformance, RTL, Robustness, Tests, Docs | `sw/firmware/ctrl/plat/ctrl_plat_phy.c:223-243` no longer suppresses repairs with an already-restarted flag. Each repaired advertisement is restarted; retained advertisements avoid redundant restarts. `phy_peer.hpp:159-184` latches active abilities separately. P15/P17 exercise dropped writes and recovery at boot and after loss. P17 additionally requires zero outcome-check retries, so the later fallback cannot mask the repair rule's failure. The corresponding campaign plant is caught. Header and README describe the corrected distinction. |
| R851-F2, MINOR | Tests | `sw/firmware/ctrl/test/test_plat_phy.cpp:557-592` separately loses register 4, register 9, and both. Each requires three writes, one restart, and no subsequent restart. Campaign plants `plat-phy-lost-local-not-restarted` and `plat-phy-lost-gig-not-restarted` fail on their register-specific assertions. The public renamed-anchor receipt catches m3, m3b and m8; the original script's three anchor refusals are not counted as successful mutations. |
| R851-F3, MINOR | Docs | `docs/design/SPLIT_CONTROL_MEMORY.md:142-148` now states 60.0, 60.5 through #895, then 61.0 through #919/#840, refused at 61.5. The obsolete round-1 sentence is removed. Section 5 and `sw/litex/ctrl_memory.py:273` agree. |
| R852-F2 / R851-F4, MINOR | Conformance, Docs | `ctrl_plat_phy.h:77-83` and `plat/README.md:95` state six additional reads (15,4,9,0,4,9), three writes (9,4,0), and 64 bit periods per frame. Recounted against the stage/register table and frame loop. A retained advertisement omits the restart write. |
| R852-R1 / R851-R1, RESIDUE | Docs | `sw/litex/ctrl_memory.py:237` uses `product_point`, #919 and #923; `:255` names hybrid XIP work and #665 decision D3. The prohibited issue-comment ID and lane name are removed from those comments. No new such instance was found in the reviewed source-comment delta. Existing reason strings are data, not the reported comments. |

Five-lens results

[R852] PASS Conformance — `sw/firmware/ctrl/plat/ctrl_plat_phy.c:223-265`, `ctrl_plat_phy.h:40-83`, P14-P18 — repair and outcome recovery satisfy the added advertisement scope. After restart, `resume = CTRL_PLAT_PHY_CURRENT` forces a fresh BMSR read. A completed, up autonegotiated link with no common 1000BASE-T mode while the advertisement is verified owes a forced restart for the next poll. Registers 4/5 then contain no permitted lower common mode and publish down. An incomplete negotiation is not judged; forced mode retains the release's explicitly accepted behavior.

[R852] PASS RTL — `ctrl_plat_phy.c:233-238,290-329`, `ctrl_plat_phy.h:245-252`, `sw/litex/milan_soc.py:1985-2014`, `hdl/milan/milan_datapath.sv:3351,4033,4058,9129,10081` — the firmware FSM remains bounded to one frame per admitted call, with unsigned wrap-safe pacing and save-step exclusion unchanged. The new 16-bit counter saturates and occupies existing structure padding. The unchanged status/CDC/effective-link path still serves counters, counter-change notifications, gPTP port enable and mailbox LINK. New retry behavior does not bypass it. No new clock/reset or CDC logic exists in this delta. ROM banking and allocation are unchanged by rounds 3/4; evidence detail follows.

[R852] PASS Robustness — `sw/firmware/ctrl/test/phy_peer.hpp:159-184`, `test_plat_phy.cpp:557-842`, `receipts/focused.log` — checked individual advertisement-register loss, repeated dropped writes, restart writes lost once and three times, counter saturation, retained advertisement, incomplete negotiation, unsupported PHY ability and an already-gigabit outcome. With a 100BASE-TX-only partner, successful recovery leaves active speed zero and ten further periods do not restart. The restart's own latched loss does not create a loop. The peer keeps register 0, active abilities, link and restart count unchanged when it drops a restart. These are model assertions, not measurements of a physical PHY.

[R852] PASS Tests — `sw/firmware/ctrl/test/plat_mutants.py:377-417`, `coverage.ratchet:30`, exact-head campaign/coverage receipts — the new oracles observe active negotiation, not merely configuration readback. P17 proves the repair itself restarts; P18 proves outcome recovery if the restart write is lost. `plat-phy-outcome-unchecked` requires the named “P18 no link at 100 after recovery” failure; the other outcome plants cover missing restart, count omission/wrap, wrong gigabit/unsupported-PHY classification and stale pre-restart BMSR resolution. The public campaign catches them. The independent focused platform arm passes 36/36, including the composed boot/consumer tests and all 20 PHY tests.

[R852] PASS Docs — `docs/design/SPLIT_CONTROL_MEMORY.md:142-148,396-410`, `sw/firmware/ctrl/plat/README.md:91-96,128-143`, `tb/verilator/ctrl_split_boot/README.md:94-109`, PR #933 body — the restart rules, numerical frame counts, single memory history, measured sizes and costs agree with code and final receipts. The release restart gap and forced-mode behavior are explicitly disclosed. Bench acceptance is still assigned to the gating run, rather than claimed from a stand-in's registers.

Execution and evidence audit

`receipts/audit.log` verifies all 471 published round-3/4 receipt hashes against `MANIFEST.json`'s `published_sha256`, the workflow table's 89 executed / 159 NOT RUN entries, and all 89 individual zero rc files. The archive commit has no signature header and the supplied manifest provides hashes, not a cryptographic signature. Integrity was verified against the specified public commit; signer authenticity is not asserted.

`receipts/public-evidence.log` records immutable artifact paths, full hashes and selected raw lines. The executions below are the author's unless explicitly marked reviewer execution.

| Evidence | Verified result and practical limit |
|---|---|
| Reviewer execution: `scripts/focused.py <clone>` | rc 0, 36/36 platform boot/PHY tests. Eight compilation workers; all outputs under packet scratch. No tracked source mutation. |
| `author-r4/receipts/workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.log` | 769/769 caught, PASS. Includes the individual-register plants, repaired-advertisement plant and seven outcome plants. |
| `author-r4/receipts/workflows/logs/rtl-fast__firmware-unit__ci_step_12.log` | `ctrl_plat_phy.c`: 178/178 lines, 164/164 branches; 40-file ratchet PASS. The row at this head matches. The earlier missing saturation branch was tested and the wrapping mutation added. |
| Final boot logs at 1x1/1if and 8x8/1if | Both rc 0. 59 frames, 10 publications, seven advertisement writes. Latched/down/return publications `[0,13]`, `[0,0]`, `[13]`. Return published after 126.231 / 126.515 ms. Longest frames 14,537 / 14,545 cycles, 145.37 / 145.45 us, below 155 us. The maximum plus 5%, rounded up to 5 us, remains 155 us. |
| Boot self-test and ledger | Six native controls, six plants, eight placement controls; ledger four points and eight controls pass. Memory-test receipt reports zero failures. These are not physical tests. |
| Prior retry probes, rerun by author | R852 fault: `advertised-at-last-restart=0001 active-Mbps=0 restarts=2`; control: same abilities/no link, `restarts=1`. R851 retry receipt: 21/21 pass. Renamed-anchor receipt catches m3/m3b/m8; m6 remains the previously identified equivalent mutation. |
| Workflow inventory | 89 zero-rc steps, 159 explicitly NOT RUN, including 29 steps carried from the earlier reviewed head on unchanged inputs. This is not 248 executed passes or hosted acceptance. No manager source bank exists at this exact head. |

The final platform ROM sizes are 119,500 / 121,084 / 132,204 / 133,772 B; allocations 43.5 / 44.5 / 56.5 / 61.0 RAMB36. Remaining ROM space is 916 B at 8x8/1if and 1,396 B at 8x8/2if. `rom-banking.txt`, `rom-per-file.txt` and the final ledger log agree: round 4 adds 64 B solely in `ctrl_plat_phy.o`; round 3 removed 8 B, so the net delta from round 2 is +56 B. Structure sizes, ROM/SRAM banks and tile counts stay fixed.

The budget-image identity receipt gives unchanged ELFs at both shapes: `10684d74b0023aa7b4326a0d1d66150fe2a0b495068c5819935d5f1cb1464fc8` and `2cf4e51a33e43e2103f366385e8e5370e9fa5c6e213b9cce77b89806261560ae`. The source delta does not touch that harness or its implementation inputs. Its inherited results remain 0/130,341 and 0/270,769 passes over the share; seven held-egress row misses at each shape and the 8x8/1if eleven stated-cost failures remain the publicly ruled base result. The harness does not compose the PHY; the PHY's cost is measured by boot simulation and admitted through the exclusive step contract. No new budget-bank execution is claimed.

Timing uses the [corrected public floor](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6930885185): best of three directives, +0.030 ns setup and 0 ns hold at every signoff corner. The routed-head receipts therefore pass at both shapes: 1x1 on all three and 8x8 on ExtraPostPlacementOpt (+0.189/+0.031 ns). The other 8x8 directives' +0.005/+0.002 ns setup are recorded misses. No route was repeated at this head; unchanged bank geometry supports the stated carry-forward, not a claim of an exact-head physical implementation run. Release-image inputs remain unchanged; the previous byte-identity evidence carries. The old review's +0.030 ns hold interpretation is superseded.

Retained optional suggestions

These are prior public suggestions on unchanged causes, not newly discovered defects or conditions for this verdict.

- **R851-S1, SUGGESTION, Robustness — `ctrl_plat_phy.c:41-46`.** Authority/evidence: the calibration fallback uses `CYCLES_HALF` while admission uses 155 us; the measured supported CPU takes the calibrated one-turn path. Impact: a future environment taking the slower fallback may exceed that admission estimate. Optional required outcome: bound the fallback's cost or refuse polling there. Verification: deliberately select that calibration branch and measure whole-frame cost against admission. Retained as optional; no physical calibration was run.
- **R851-S2, SUGGESTION, Robustness — `ctrl_plat_gen.py:148-153`.** Authority/evidence: the documented all-or-none map accepts absent MDIO rows and arms no poll. Impact: a future board export could omit a management path it intended to provide. Optional required outcome: add a board-specific required-row check where MDIO is mandatory. Verification: remove those rows from that board's export and require a named refusal. The existing generic no-MDIO contract is unchanged.
- **R851-S3, SUGGESTION, Conformance — [#665 ruling, item 4](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6899740728), `ctrl_plat_phy.c:316-328`.** Authority/evidence: the ruling's “store step” wording is broader than the published implementation's save-step exclusion; OFF/IDLE/HELD calls only check whether a save is due. Impact: readers can interpret the scheduling sentence differently. Optional required outcome: manager records that distinction in the ruling if clarification is wanted. Verification: compare it with the step contract and existing B12 exclusion tests. No changed scheduling behavior is introduced by this delta.

Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #919/#840 scope, REQ-MAC-03; `sw/firmware/ctrl/plat/ctrl_plat_phy.c:223-265`; P14-P18; frame counts | R852-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| RTL | CLEAN | `ctrl_plat_phy.c:233-238,290-329`; `ctrl_plat_phy.h:245-252`; `sw/litex/milan_soc.py:2013`; memory-bank receipts | R852-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| Robustness | CLEAN | `sw/firmware/ctrl/test/phy_peer.hpp:159-184`; `test_plat_phy.cpp:557-842`; focused 36/36 receipt | R852-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| Tests | CLEAN | `sw/firmware/ctrl/test/plat_mutants.py:377-417`; `coverage.ratchet:30`; final campaign/coverage/boot receipts | R852-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |
| Docs | CLEAN | `docs/design/SPLIT_CONTROL_MEMORY.md:142-148,396-410`; platform/boot READMEs; `sw/litex/ctrl_memory.py:234-296`; PR body | R852-2 | 1a1e6665fcfd57943f2721cd3bd024eb16b0aa84 |

Limits and pending manager duties

Physical calibration: **NOT RUN**. No hardware was accessed. Field skips, boot stand-in gPTP words and simulated MDC timing do not prove hardware behavior. The issue still requires the gating run's LINK_UP/LINK_DOWN increments, both notifications and gPTP resume within five seconds. A forced-mode PHY before boot and the unchanged release firmware's lost-restart gap are the explicitly accepted limitations, not findings here.

This reviewer ran no full parent, processor, gPTP, synthesis or builder bank, no container/local-workflow runner, no routing and no hosted execution audit. No pinned simulation executable was used. Broad source evidence is the author's published receipts, not a manager source run. Hosted and local workflow acceptance belongs to the manager and must distinguish execution from skipped contexts.

The manager must publish this packet, obtain the other independent verdict, reconcile the train's overlapping memory-entry/helper changes, build and gate the actual current-dev merge candidate, and link builder/native receipts. The recorded live-dev input is `6b66f66d89cf25d2717687bcc2c3bf617685a99a`; it must be refreshed at the merge turn. PR metadata currently targets `dev-soft-core`; that staging base and the original source base are not the final current-dev candidate. Complete the physical gating, authorized merge and post-merge containment before closing the acceptance ledger. This source verdict authorizes none of those actions.

Final integrity: 1,630 superproject tracked blobs match exact bytes/modes, and the index tree matches the requested head. All five required initialized submodules match gitlinks, blob bytes/modes and index. `external` remains uninitialized and was not used. Fetching public archive objects only changed clone metadata. No tracked source restoration was needed. `git status --porcelain` is empty.

Reproduce the packet checks from a clone with the required pins using `python3 -B scripts/focused.py <clone>`, `python3 -B scripts/audit.py <clone>` and `python3 -B scripts/evidence.py <clone>`, with scripts resolved within this packet. Build products are under `scratch/`; only REPORT.md and MANIFEST.sha256-listed files are for publication.

R852-2 FINISHED

[R497] POSITIVE - exact head e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d

R497-4 is the external independent source review of issue #665, lane F0, PR #668. Tree: `ce7e90ddd1263ec89751eca6d836e451a87ecded`. All five lenses are CLEAN. R497-3 F1 and R496-3 F1/F2 are resolved against the public round-4 assignment. No BLOCKER, MAJOR or MINOR remains from this review. One previously recorded wording-only RESIDUE remains for the manager's checklist.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue's frozen acceptance and public decisions, requirements and interface authorities, the requested `fa450d301805881ad713b67521477bf042ddadfd..e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d` range and history, then public evidence. The source-base range includes earlier dev integrations; the round-4 delta is exactly four commits on `3ebd6ca30106a006c20fd2879dcad9c79bf51dca`, eight files, with no new dev merge. Detailed examination covered that delta and its ADP, loop, mailbox, test and documentation dependencies. Earlier unaffected conclusions were checked for continued applicability.

The independent source pass, verdict and five-lens ledger were written in `independent-pass.md` before reading earlier reviewer reports. Previous public findings were then reconciled and their focused probes rerun. No private author material, management checkout, lane scratchpad or other current-round report was consulted. Public references and receipt provenance are recorded in `public-artifacts.json` and `source-provenance.json`.

The governing scope is the [F0 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5991862788), [bare-metal directive](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5992455815), and [round-4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5999248955). The default-off mailbox and ADP slice remain the subject of this verdict; activation of the shipping split and subsequent protocol lanes remain outside it.

| Round-4 item | Disposition at this head | Examined evidence |
|---|---|---|
| R497-3 F1: silently lost SHUTDOWN at counter capacity | RESOLVED under the assignment's authorized coalescing option | `adp.c:153-175`, `adp.h:33-57,160-170`: at most two owed DEPARTINGs; the oldest keeps its shutdown index, the queued one carries zero, and further SHUTDOWNs increment `departing_coalesced`. `test_adp.c:470` A21 checks the second place, subsequent coalescing, retained oldest index, 100,001 counted shutdowns and ordered recovery. All four capacity/order mutations fail. `capacity-rule.log` independently exercises 4,294,967,296 public enable/disable pairs: 2 owed plus 4,294,967,294 coalesced, zero unrecorded. |
| R496-3 F1: incorrect first-pass latency claim | RESOLVED | `ctrl_loop.h:28-53`, `adp_mbx.h:22-91,121-124`, `MAILBOX_SPLIT.md:345-384` and the PR body's round-4 table agree: with k departures owed ahead, AVAILABLE commits in pass k+1 after room returns, or the input's processing pass if later. Here k is at most 2, yielding 3 passes and a conservative 1,628 accesses including an already-running pass. E5 exercises 1, 2 and 64 shutdowns, expiry before/after room. The original R496-3 probe gives passes 1, 2, 3, 3, 3, 3 for 0, 1, 2, 3, 16, 64 shutdowns; maximum 99 accesses. `prior-bound.log`, `firmware.log`. |
| R496-3 F2: three unguarded owed-frame legs | RESOLVED | `test_adp.c:391-468` A18 keeps DEPARTING across link loss/recovery, A19 preserves owed AVAILABLE across GM/DISCOVER/stray expiry, and A20 drops AVAILABLE on link loss before any poll. A16 also grades later SHUTDOWN index preservation. All eight R496-3 reviewer mutants compile and fail completed tests, including the three previously escaping copies. `prior-probes-summary.txt`, individual `mutant-*.log/.rc`; L1-L3 remain correct in `prior-rules.log`. |
| Merge current dev if it moved | SATISFIED for this source round | The four commits have no merge; the reviewed head already contains `28f9666feab2b2ba287643c63ed3a16b1e0bb863`. The later merge-candidate decision remains manager-owned. |

The coalescing argument was checked directly against the standards, not inferred from passing tests. `advertise()` refuses to pass any owed departure (`adp.c:121-131`), and SHUTDOWN resets the current run's index. Thus a later run ending behind that queue has advertised nothing and its departure index is zero. The oldest index remains separately preserved. A receiver that accepted the preceding matching departure is already undiscovered: Milan v1.2 Table 5.54 ignores another RCV_ADP_DEPARTING in TK_NOT_DISCOVERED; section 5.6.4.5.3 removes discovery on the first matching interface. IEEE 1722.1-2021 6.2.6.3.5 removes the matching entity record, leaving none for a repeat. These support the authorized rule's receiver-state argument. It does not claim equal delivery probability under packet loss: omitted duplicates would have been additional transmission opportunities, as the public ready comment acknowledges. Edition hashes and examined clauses are in `standards-consulted.txt`; the [Milan v1.2 specification](https://avnu.org/wp-content/uploads/2023/12/Milan_Specification_Consolidated_v1.2_Final_Approved-20231130.pdf) is the cited Milan authority.

`departing_coalesced` is explicitly a modulo-2^32 diagnostic (`adp.h:162`). That diagnostic wrapping does not wrap or enlarge the owed queue. The independent boundary probe also checks this boundary and recovery from initial indices 0, 1, 2^32-2 and 2^32-1, with repeated shutdowns and link flaps. Its 40 scenarios preserve departure order and restart AVAILABLE 0, then WAITING with TMR_ADVERTISE. No target timing claim is inferred from host runtime.

The original R496-3 `second-shutdown-overwrites-index` mutation targets the removed UINT32_MAX guard. This round relocates only that patch site to `ADP_DEPARTING_OWED_MAX`, preserving the erroneous index assignment; A16 kills it. A patch-site mismatch is not counted as a killed mutant. The original public probe sources and blob identities are retained under `prior-probes/`. The capacity probe's earlier “every shutdown stays separately owed” oracle is superseded by the public coalescing decision; `capacity_rule_probe.c` changes its reporting/oracle accordingly while keeping the public-API workload and unchanged candidate core.

Earlier public findings are explicitly disposed as follows. Their findings are not silently cleared by this overall verdict.

| Prior item | Disposition | Evidence at this head |
|---|---|---|
| R497-2 F1 | Resolution stands | Separate `departing_owed` / `available_owed`, departures first, A15-A17 and E4. Replacement, overtaking, missing second departure and reviewer order mutants are killed. |
| R497-2 F2 / R496-2 N3 | Resolution stands | Design and test READMEs reference executable inventories. Current PR totals match 46 RTL and 51 firmware mutants. |
| R496-2 N1 | Resolution stands | `test_port_loop.c:438` L8 and `carried-ticks-overwritten` still require accumulated ticks; mutant killed. |
| R496-2 N2 | Resolution stands | `axil_checks.hpp:386` A7 pairs each W/AW through readback; both drain-cycle READY mutants killed. No adapter or harness delta this round. |
| R497-1 F1 / R496-1 F2 | Resolution stands | Registered independent AXI slots, held responses and reset paths in `KL_mbx_axil.sv:84-157`; A0-A7 pass, adapter mutants killed. |
| R497-1 F2 | Remains withdrawn under ruling 5994972330 | Current-index DEPARTING / next-run AVAILABLE 0 matches the public ruling, IEEE Figures 6-2/6-3 and 6.2.5.2.2; A10-A14 and index mutants remain effective. |
| R497-1 F3 | Resolution stands | `ctrl_loop.c:132-155`, `adp_mbx.c:123-133`, E0-E4 keep owed output runnable; the real waiting-HAL checks and owed-output mutants pass their expected outcomes. |
| R497-1 F4 | Resolution stands, with round-4 owed-frame qualification | A1-A4 and F0-F7 preserve events-first, bounded callbacks/backlogs and access limits; the newly corrected owed-output bound is graded above. |
| R497-1 F5 | Resolution stands for the existing driver | Global TX SEQ and X2/D3 preserve tested commit order; RTL/model round-robin and driver stamping mutants killed. The earlier optional request to document the current driver's scan-timing premise remains optional. |
| R496-1 F1 | Source defect resolved; hosted acceptance pending manager | Generated reference remains in `ci_scope.py:57`; its self-test passes. Hosted/local-replica completion is not asserted by this source review. |
| R496-1 F3 | Prior resolution stands, unchanged | `ctrl_arms.py:191-222` records the library pin and refuses changed source/revision; README includes retrieval recipe. Optional library integration was not rerun here. |
| R496-1 F4 | Resolution stands | H0-H2 and all three counter-guard removal mutants pass their expected outcomes on both adapters/model. |
| R496-1 F5 | Resolution stands | `own-discover-discarded` fails the reused own-entity DISCOVER walk row. |
| R496-1 F6 | Resolution stands | `MAILBOX_SPLIT.md:422-430` and PR body name CPU netlist regeneration from the enabled memory region. No export input changed this round. |
| Round-2 EOF item | Resolution stands | Both source-base and integrated-dev `git diff --check` exit 0. |
| R497-3 R1 / R496-2 R1 | RETAINED as RESIDUE below | CI policy wording unchanged. |
| R496-2 S1-S5 | Remain optional suggestions | Hosted firmware-gate wiring, a dedicated W-only mutation entry, scan timing premise, tighter backlog explanation, and long ring-counter wrap coverage remain optional. Earlier adopted platform interrupt/memory-ordering suggestions stay documented. |

**R497-4-R1 - RESIDUE - Docs - retained generated-page classification explanation.**

- Artifact: `docs/testing/CI_WORKFLOWS.md:58` and `:75`.
- Authority/evidence: the six-page classification and self-test are correct; the introduction still attributes every reader to a classifier-gated hosted job, although the mailbox generator has no hosted job. The classifier self-test passes at this head.
- Impact: wording only; no measurement, figure, verdict, test, code, generated artifact, conformance/clause claim or privacy rule changes.
- Exact required outcome: replace the introduction with “Six pages under `docs/` are relevant because Python that the classifier's self-test scans names them; five of those readers run in a classifier-gated job.” Replace the mailbox sentence with “(#665). No hosted job runs it yet; the page is relevant because its reader is Python under `sw/`.”
- Verification: compare those sentences against the classifier and workflow inventory; carry the same item on the residue checklist. It does not unclean Docs or change this verdict.

Executed evidence is distinguished from inherited or reported evidence:

| Execution | Result | Receipt |
|---|---|---|
| Firmware host/freestanding gate | 744 checks: model 134, port 81, ADP 163, reused walk 320, entity 45, RV32I 1; 51/51 mutants caught | `firmware.log/.rc` |
| Mailbox RTL campaign, `--jobs 3` | Wishbone 134 and AXI4-Lite 179 checks; 46/46 mutants caught | `mailbox-mutants.log/.rc` |
| Firmware/RTL/model co-simulation, `make -j16`, inner compilation capped at 2 | 13 checks; five matching frames and NOW_MS values | `cosim.log/.rc` |
| Contract generator | No drift/crosscheck findings; positive control, eight output mutations and seven invalid-contract controls pass | `contract.log/.rc` |
| Scope and whitespace checks | Self-test PASS; both diff checks rc 0 | `ci-scope.*`, `diff-check-source.*`, `diff-check-dev.*` |
| Independent core boundary probe with undefined-behavior instrumentation | 40 recovery cases and one diagnostic-wrap boundary pass | `boundary.log/.rc` |
| Earlier reviewer probes | 12 latency rows agree; three wire-rule legs pass; eight mutations killed; 2^32 public shutdown calls fully accounted under the new rule | `prior-bound.*`, `prior-rules.*`, `mutant-*`, `capacity-rule.*` |

The six-arm firmware total excludes the optional 13-check library integration; the published seven-arm total of 757 is consistent. Campaigns ran concurrently under a foreground parent, at most sixteen compilation jobs. Every started process completed before this report. Disposable trees and builds stayed under `scratch/`. No prohibited full banks, hardware run, source fix, commit, push, GitHub write, merge, shared installation, container workflow or delegation occurred.

The reviewer-owned completion ledger records coverage at the actual reviewed commit. The residue above does not affect clean coverage under the owner's rule.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `adp.c:106-175`, `adp.h:33-57`, `adp_mbx.h:69-84`; public coalescing/index rulings against Milan Tables 5.51/5.54 and IEEE 6.2.5.2.2/6.2.6.3.5; observed wire order and bound | R497-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |
| RTL | CLEAN | Firmware architecture in `adp.c:153-175,267-280`, `adp_mbx.c:123-133`, `ctrl_loop.c:132-155`; static bounded state, no new CDC; unchanged `KL_mbx_axil.sv`, `KL_mbx_tx.sv`, `KL_mbx_evt.sv` and default-off `milan_soc.py`; RTL controls/campaign and co-simulation | R497-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |
| Robustness | CLEAN | `test_adp.c:391-495,768-820`; saturated TX, repeated shutdown/restart, link/GM/stray inputs, cancellation, wrap, held responses and malformed counter guards; boundary/capacity/rule receipts | R497-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |
| Tests | CLEAN | `ctrl_mutants.py:37-87`, A15-A21/E4/E5/F0-F7, L8, AXI A0-A7; 51 firmware and 46 RTL mutants plus eight prior reviewer copies all killed; positive controls and raw receipts retained | R497-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |
| Docs | CLEAN | `ctrl_loop.h:28-53`, `adp_mbx.h:22-91`, `MAILBOX_SPLIT.md:289-384`, firmware/test indexes and PR round-4 table agree with executable counts and bound; `CI_WORKFLOWS.md:58,75` residue explicitly retained | R497-4 | e6420c0ff2cc51059bbe9cd58f9d101e1cb54a8d |

Final integrity proof in `integrity.json` checks raw blob bytes, file kinds/executable modes and every stage-zero index entry independently of status flags: 1,077 root blobs, 558 processor blobs, 104 timing-processor blobs and 214 stream-library blobs. Required registered gitlinks are `ead8036035affd53ef4b29979190f2f4f67084c0`, `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. Detached HEAD/tree and clean tracked checkout are unchanged. No source restoration was necessary.

Reproduction: `run_campaigns.py REPO PACKET VERILATOR`, `run_boundary.py REPO PACKET`, `run_prior_probes.py REPO PACKET`, and `verify_integrity.py REPO PACKET`. Use a fresh packet scratch directory, the scoped compiler reporting version 5.050, and the existing RV32I compiler for the freestanding arm. `prior-probes/origin.json` binds downloaded public source blobs. `receipt-policy.txt` documents local-path normalization; no result or measurement text is altered. `MANIFEST.sha256` lists every publishable receipt and script. `scratch/` is excluded.

Real limits and pending manager duties:

- This is source validation, distinct from the final current-dev candidate. Source base is `fa450d301805881ad713b67521477bf042ddadfd`; integrated live dev is `28f9666feab2b2ba287643c63ed3a16b1e0bb863`. The manager must construct and validate the merge candidate at the merge turn.
- Full source static/builder/native banks are reported passing by the manager; they were not rerun here. The supplied immutable round-1 directory contains historical handoff/PR/ready text, not raw current-head bank logs. Its hashes were verified. The [round-4 ready comment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5999860712) identifies current-head execution and limitations. Historical counts were not treated as current results.
- `hosted-snapshot.json` confirms the published exact head and ready state. At capture, changes, selector, lint, behavior, wire, no-git docs and four synthesis shards had completed successfully; five simulation shards, synthesis elaboration, docs and elaboration remained in progress. The physical context was skipped. Final required aggregates were not accepted by this reviewer; hosted/local-replica acceptance remains manager-owned.
- Physical calibration NOT RUN. Field skips are not hardware proof. No target cycles or bus-time calibration, routed-area rerun, full shipping build, or new default-export comparison was performed. The unchanged prior Arty comparison uses a 100 MHz proxy after both shipping-clock exports were refused. The default-off datapath seam remains idle; later protocol integration is outside F0.
- The manager should publish this packet, carry R1 on the residue checklist, obtain the second independent positive review and accepted exact-head coverage, finish hosted/local-replica and candidate validation, obtain explicit merge authorization, then perform containment and appropriate F0/project updates. The broader issue's later lanes remain outstanding.

R497-4 FINISHED

[R680] POSITIVE - exact head 7b424cdfe111a426f00517ff471246b4b9650726

The round-2 delta closes the parked-applicant defect. A sink declaring a parked StreamID takes over its applicant through New!, without a stale Lv beside its declaration. All named prior findings are resolved. No BLOCKER, MAJOR or MINOR remains in this review. One optional wording suggestion is recorded below; no new RESIDUE is retained.

Reviewed tree: `4142dcfe858d04687f3f37847a67f7c69d6ae0ea`. Source base: `21601694880efdfc4be3028afa3525fbc8f29c03`. Delta base: previously reviewed `6ddfcda4c3170b8f463c8623833f7541ca8c1faf`. The five commits are `e38c535`, `acd65be`, `c7c8825`, `57fb7dd`, `7b424cd`. Unchanged behavior keeps its previous coverage; dependencies affected by parked grouping, arbitration and handover were examined again. The merged #192 changes are inherited, not attributed to this round.

The independent verdict and five-lens ledger were written in [independent-pass.txt](independent-pass.txt) before reading either prior public review. [prior-findings-audit.txt](prior-findings-audit.txt) records the subsequent reconciliation, including the one classification correction described below. No private author material, private management material or other current-round report was read. No source changes, commits, pushes, GitHub writes or other-checkout edits were made.

**Scope and authorities examined**

The supplied AGENTS instruction and its referenced command convention were read; no repository AGENTS.md or CONTRIBUTING.md exists. Repository authorities examined include `docs/README.md`, the root and HDL READMEs, the REQ-ACMP-018/022 and REQ-SRP-001…006 matrix rows, architecture 02's SRP operations/status contract, architecture 10 §5.1/§6.4, and the unchanged interface and memory-map documents. The full base-to-head diff/history was separated from the five-commit delta, with unrelated merged code retaining prior coverage.

The public acceptance sources are [issue #193](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/193), its [owner-election ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/193#issuecomment-6290012163), the [manager answers](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/193#issuecomment-6299223806), the exact [round-2 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/198#issuecomment-6300041102), and the exact [area/restart ruling](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/198#issuecomment-6310654578). Issues [#188](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/188) and [#189](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/189) supply the preserved owed-Leave and per-sink registered-type obligations. The accepted single-sink unchanged-type request behavior remains unchanged.

Normative basis: IEEE 802.1Q-2018 §10.7.7, Table 10-3, §35.1.2.2, §35.2.4.4.3 Table 35-14 and the §35.2.6 NOTE/in-place-change rule; Milan v1.2 §4.2.7.2.2. The full copyrighted standards were not independently re-audited; this delta review uses the frozen public requirements and repository authorities.

**Prior findings, resolved at this head**

| Prior ID | Disposition and verification |
|---|---|
| R679-1-F1 / R680-1-F1 — MAJOR | Resolved at the cause. `hdl/srp/KL_srp_listener_fsm.sv:587` includes parked recorded sinks; `:594-608` selects leave-copy pairs for parked members; `:942-954` updates those pairs; `:1038` releases the giver's park. Existing handover applies LA/LO + New! = VN. SH10–SH13/SW4–SW7 cover both orders and both rebind forms. Exact-head probes have no FAIL PR/PW, one value per tick, no stale Lv and uninterrupted peer registration. SH14–SH16 preserve owed messages without demand and the one-transmission walk rule. Banner `:103-114` and architecture 10 `:648-660` describe the parked case. All attributable lenses are clean. |
| R679-1-F2 / R680-1-F2 — MINOR | Resolved. The current [PR body](pr-body.txt) states module-default 8 Stream Inputs × 8 Stream Outputs beside the area result, explicitly says no 1×1 figure was measured, and assigns shipped cost to the fourth adoption's route-1x1. Public parent defaults and OOC invocation agree. Revised deltas reproduce below. Docs clean. |
| R680-1-F3 — RESIDUE | Applied exactly: `tb/srp_top/sim_main.cpp:3000` uses the plain behavior heading and `:3170` has no SW3 prefix. No outstanding residue from this finding. |
| R680-1-F4 — MINOR; R679-1-S1 — SUGGESTION | Resolved. `tb/srp_stream_fsms/sim_main.cpp:1794-1796` and `tb/srp_top/sim_main.cpp:3172-3173` cite §35.1.2.2 and §35.2.4.4.3 Table 35-14 for the type sum, retaining §35.2.6 for the in-place change. Docs and Conformance clean. |
| R679-1-S2 — SUGGESTION | Resolved by recorded probe and documentation. Independently rerun at this head: 17/17 PASS. Transfer to a lower slot already passed by the walk postpones its message to the next tx!; nothing is lost or duplicated. Banner `:111-112` and architecture 10 `:644-645` state the delay. |

The two prior public reports were issue comments 6299632354 and 6300027310. The later audit found zero submitted reviews and zero inline review comments. Their differing initial treatment of the citation and SW wording does not leave an unresolved item: the explicit round-2 assignment is implemented.

**Independent executable evidence**

All runs use disposable exports of the exact head, ordinary control/receive faces and unchanged RTL. [run-probes.py](run-probes.py) reproduces them with the clone path as its argument. It verifies the scoped simulator identity before building, records each child return code, and bounds concurrent compilation to 16 workers. [probe-summary.txt](probe-summary.txt) indexes the raw receipts.

| Exact-head run | Result and evidence |
|---|---|
| Four parked-value variants at the FSM interface | [fsm.log](fsm.log): 1,414/1,414 PASS, including the committed 1,410 checks and four PR probes. Both index orders, direct A15 and A8+A15, produce `0/2`, `0/2`, `3/2` over successive ticks: one value, no Lv while declaring. All existing SH and #188 checks in this suite pass. |
| Wire probes plus committed share group | [wire.log](wire.log): 11/11 PASS: nine committed checks plus two PW probes. Committed SW4–SW7 cover both index orders and both rebind forms, compare the complete first frame byte-for-byte, count later values, and feed every MSRP frame to the peer registrar. PW probes print 35-byte single-value frames, peer IN before/after, zero deregistrations and zero Lv. No FAIL PR/PW appears. |
| Separate withdrawal-then-settle reproductions | [parked-fsm.log](parked-fsm.log) and [parked-wire.log](parked-wire.log): 2/2 PASS each, one value, zero Lv, peer IN in both index orders. |
| Lower-index handover timing | [lower-index.log](lower-index.log): 17/17 PASS. Live transfer at clocks 1–4 waits one tick; clocks 5–6 carry the already-issued walk mark. Parked cases distinguish takeover before the old Lv from registration after that Lv was legitimately sent. |
| Broadcast/control/transmit collisions | [collisions.log](collisions.log): 32/32 PASS. Both index orders, periodic/received LeaveAll/join timing, repeated rebind, rider withdrawal, withdrawal before tx!, and LO takeover. At most one value per tick. Lv followed by later New occurs only where the old applicant was walked before a new declaration became effective. |

A representative first frame is:

```
01 80 c2 00 00 0e 0a 0b 0c 0d 0e 0f 22 ea 00 03 08 00 0e
00 01 11 22 33 44 55 66 00 01 00 80 00 00 00 00
```

It contains one Listener value `1122334455660001`, New/Ready. The previous 47-byte New-plus-Lv failure is absent.

RTL inspection independently checks the reasons those runs pass. A parked slot belongs to its held value, not its new matcher value. Nondeclaring riders remain quiet; declaration requests wait for their own park to clear. A transfer clears the giver's park and retains applicant state, parameter, pending broadcasts and walk mark. Retiring a parked message marks its old group (`:989-996`), preventing a later declaration in that walk from transmitting twice. The new unreset compare copies are meaningful only through valid parked membership; the single-sink generate branch has no cross-sink comparison. Per-sink registrar logic, notification strobes and interface definitions are unchanged by this delta.

**Published controls, broader gates and provenance**

The [public packet](https://github.com/kebag-logic/milan-fpga/tree/cbc4bd9f9b7348d6298adbd5c505bf138e0012eb/review-evidence/pp193-r1) supplies author execution evidence. [fetch-evidence.py](fetch-evidence.py) checked 963 round-2 public files against `published_sha256`; [evidence-hashes.txt](evidence-hashes.txt) records every match. Redacted published bytes are checked against published hashes, not original private-file hashes. The archive commit is unsigned: [archive-authenticity.txt](archive-authenticity.txt). No cryptographic signature is claimed.

[audit-evidence.py](audit-evidence.py) recomputes the figures and audits the return codes and named controls; [evidence-audit.txt](evidence-audit.txt) and [public-receipts/](public-receipts/) preserve the results and selected raw public receipts.

| Control | Named checks KILLED in the published clean head campaign |
|---|---|
| `listener-parked-outside-groups` | SH10–SH16; SW4–SW7 |
| `listener-settle-skips-leave-copies` | SH10–SH15; SW4–SW7 |
| `listener-merge-keeps-park` | SH10–SH13 |
| `listener-retire-skips-group-mark` | SH15 |
| `listener-park-drops-matcher-pairs` | SH16 |

The campaign reports 203/203 PASS, assertion coverage 124/124. Raw failure receipts reproduce duplicate values and peer deregistration under the relevant controls. The re-anchored settle-compare control retains the same edit; the remaining earlier controls keep their verdicts and required tags. Dual-suite controls' additional FSM receipts are in `head-extra`, not inferred from an overwritten wire log.

The public broad suite tally changes from 1,030,356 to 1,030,367, exactly seven added FSM checks and four added wire checks. All recorded processor gate and campaign return codes are zero. The other ten affected campaigns retain their passing results. These are published source receipts, not independently rerun full banks.

HANDOFF R2.6 was read exactly. [restart-provenance.txt](restart-provenance.txt), `campaigns/head/RUNNER.txt`, the two replacement runner scripts, head gate identity, consumer STATE records and final rerun identity consistently identify the clean replacement runs. Passing head conclusions use `57fb7dd21d316ce49c305c22812de5c16d6770f6` receipts plus final documentation reruns at `7b424cdf`. Independently verified: the final commit changes only six README lines; every executable input is identical. No passing-head conclusion uses the pre-commit `dev` campaign, the aborted duplicate campaign or either void directory. Original runner processes were not observed independently; attribution rests on the public provenance, receipt set and source equivalence. The intermediate `c7c8825f` area statistics below are historical cost evidence only.

Scratch-parent source validation is recorded on dev `78ca9bdf104819265588726bce4322696c38b8c2` with the four adoption patches: evidence classification, milan_dp-67, per-slot TSpec and milan_dp-gsi-g9. Consumer STATE records identify the committed processor pins, unchanged other gitlinks and empty working-tree diff. Consumer return codes are zero except `check_submodule_docs`, which is 1 at base, head and final for the same documented-pin/diagram mismatch. This known adoption-doc exception is retained, not represented as a green gate.

The public milan_dp summary gives 10,559 `[ok]`, 1,127 `[PASS]`, zero `[FAIL]`, identical sorted check lines. pp_shadow returns zero at both pins; the author reports 609+609+649+317 = 2,184 checks. Its parallel output interleaves: the public line extractor counts 2,182/2,183, so that extractor is not an independent 2,184-check proof. Oversized original logs are listed by size/hash in EXTERNAL-RECORDS.csv and were not accessed. The builder receipt says “ALL GATES PASS EXCEPT 1 NOT RUN”; its physical-report gate 11 is not executed evidence. ROM digest rows are unchanged.

**Area, reproduced from receipts**

The public parent module defaults are 8×8; the OOC invocation has no shape override. [public-parent-defaults.sv](public-parent-defaults.sv), [public-parent-run.sh](public-parent-run.sh) and the published `run_ooc.sh` establish that measurement context.

| Processor pin, same scratch parent | LUT | FF |
|---|---:|---:|
| main `08023123` | 56,743 | 26,331 |
| round-2 base `6ddfcda4` | 57,266 | 26,381 |
| head executable inputs `57fb7dd2` | 58,078 | 26,949 |
| Entire PR delta | +1,335 | +618 |
| Round-2 share | +812 | +568 |

LUTRAM 4,236, RAMB36 15, RAMB18 4, DSP 10 and CARRY4 2,392 are unchanged. Summing LUT1–LUT6 in the standalone listener statistics gives 9,428 at base, 11,679 before commit 4 and 9,750 after it: +2,251 becomes +322, removing 1,929 LUT. The indexed packed-array write is replaced by a constant-index write with a per-sink enable (`hdl/srp/KL_srp_listener_fsm.sv:827-831`). These figures are reproduced by arithmetic over receipts, not by a new synthesis run. The manager's accepted area ruling is not reopened. No 1×1 parent OOC figure was measured; the separate single-listener characterization is not that figure.

**New suggestion**

R680-2-S1 — SUGGESTION — Docs. Artifact: `tb/srp_stream_fsms/sim_main.cpp:1587,1589`. The new explanatory comment refers to `(RB)` and `(RB5)`. For consistency with the requested plain-behavior SW comments, optionally remove those two parentheticals: “Leave. A sink …” and “as one sink's re-probe. So …”. Keep assertion IDs, expectations and requirement citations unchanged. Impact is editorial only; no required correction for acceptance. Verification is a comment-only diff, with no changed code, check, measurement or clause claim.

The independent snapshot initially classified this as RESIDUE. The subsequent public [#746 rule](https://github.com/kebag-logic/milan-fpga/issues/746) expressly distinguishes behavior IDs from workflow/bench-lane labels. RB/RB5 identify behavior checks here, so the final classification is SUGGESTION. The earlier specifically assigned SW edits remain applied; no new forbidden lane, review-round, reviewer or issue-comment label was found in the reviewed source delta.

**Reviewer-owned lens ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen #193/#188/#189 obligations; parked grouping and LA/LO+New! transfer; SH10–SH16/SW4–SW7; exact-head frame/peer receipts; corrected type-sum citations | R680-2 delta and prior-finding closure; unchanged coverage inherited from R680-1 | 7b424cdfe111a426f00517ff471246b4b9650726 |
| RTL | CLEAN | Listener owner_map/app_arb/handover/settle/walk; lq/lcp writes and validity; constant-index commit-4 write; preserved registrar and interface headers | R680-2 delta and dependencies; R680-1 unchanged coverage retained | 7b424cdfe111a426f00517ff471246b4b9650726 |
| Robustness | CLEAN | Both index orders and rebind forms; no-declarer owed Leave; 17 timing probes; 32 collision cases; LO and repeated-settle behavior | R680-2 exact-head probes and prior retained cases | 7b424cdfe111a426f00517ff471246b4b9650726 |
| Tests | CLEAN | Independent table model and wire builder/parser; exact-head 1414/11/2/2/17/32 passing runs; named KILLED controls; public 203/203 and gate/consumer receipts with stated exceptions | R680-2; earlier unchanged tests retain prior verdict | 7b424cdfe111a426f00517ff471246b4b9650726 |
| Docs | CLEAN | Banner; architecture 10 §5.1/§6.4; suite READMEs and counts; PR 8×8 provenance; area arithmetic; corrected citations/comments; S1 optional | R680-2 and resolution of R680-1-F2/F3/F4 | 7b424cdfe111a426f00517ff471246b4b9650726 |

**Limits, integrity and pending manager duties**

No full processor, parent, gPTP, portability or builder bank was run by this review. No synthesis, routing, hardware, privileged action or shared install was performed. Physical calibration is NOT RUN; field skips are not hardware proof. No hosted acceptance is asserted and no skipped context is counted as execution. No manager source bank exists at this exact head and none is inferred.

The manager owns final current-dev candidate validation with builder/native banks, publication of those receipts on the PR, hosted/act acceptance, adoption documentation, and the fourth adoption's route-1x1 resource result. Source base `21601694`, historical consumer dev `78ca9bdf`, and live dev `d77a8afdbc960d70d1ceeee9af1163624f102b16` are distinct. If the shipped route fails its resource gate, adoption stops and area returns to this PR under the public ruling.

[verify-source.py](verify-source.py) confirms all 697 tracked blob bytes and executable modes, HEAD/tree, index and clean status including ignored files. There are zero nested gitlinks in this processor tree. [source-integrity.txt](source-integrity.txt) also confirms unchanged listener/SRP-top/processor-top port and parameter headers and unchanged architecture 02/07, against both source base and round-2 base. The source clone never required restoration because all probe modifications were confined to disposable exports.

Every process was foreground-owned and completed. Disposable exports, downloaded evidence and builds are under `scratch/`, excluded from publication. `MANIFEST.sha256` lists every publishable file with packet-relative paths. Reproduction: run `fetch-evidence.py`, `audit-evidence.py`, `run-probes.py <isolated-clone>`, and `verify-source.py <isolated-clone>`; the probe runner accepts the exact reviewed head only.

R680-2 FINISHED

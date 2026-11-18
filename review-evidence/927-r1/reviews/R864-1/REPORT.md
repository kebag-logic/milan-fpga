[R864] POSITIVE - exact head 0297a19a056ee3d5d705bc502c4ae7808689ede7

Round R864-1, external independent review of issue #927 / PR #939. Reviewed tree: `e3e4dbefc89e29cc646fd5e2cf757338ba3877a9`; source base: `70f4056f`. The complete delta is thirteen commits, twenty files, 313 insertions and 48 deletions. All five lenses are CLEAN. No BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION finding is raised.

This verdict covers the published source head. It does not approve a merge or establish timing for a composition with current dev.

The contract was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body and its public scope decisions, requirements and interface authorities, then the complete diff and history. Public executable evidence was examined after that independent pass. No other reviewer's report or private author material was read before this verdict and ledger were written.

Public authorities and evidence:

- [Issue #927](https://github.com/kebag-logic/milan-fpga/issues/927): frozen acceptance, [scope widening](https://github.com/kebag-logic/milan-fpga/issues/927#issuecomment-6908876362), [authorization of the DMA cut and ROM-fill measurement](https://github.com/kebag-logic/milan-fpga/issues/927#issuecomment-6914223799), [corrected timing floor](https://github.com/kebag-logic/milan-fpga/issues/927#issuecomment-6930885657), and [best-of-three clarification](https://github.com/kebag-logic/milan-fpga/issues/927#issuecomment-6933111168).
- `REQUIREMENTS.md` sections 1, 3 and 8; `docs/reference/FR_NFR.md` FR-CLK-04, FR-STR-02 and NFR-SCOUT-03; `docs/design/MAILBOX_SPLIT.md` record mover, face block and crossing; `docs/reference/MAILBOX_CONTRACT.md` EDIT window and 64-cycle bound; `docs/design/MEDIA_CLOCK_FOLLOWING.md` timestamp pick and loss rules.
- `docs/design/MARK_II_AREA_PLAN.md` timing comparison and M8a-2 recipe; `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` selected-placement measurements. IEEE 1722-2016 AAF and Milan v1.2 remain the wire authorities. This delta changes no wire format, acceptance filter or protocol timer.
- [Published author receipts, immutable archive e83ed7065bf3f4206797561fe5a3a6b631860985](https://github.com/kebag-logic/milan-fpga/tree/e83ed7065bf3f4206797561fe5a3a6b631860985/review-evidence/927-r1) and [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/927#issuecomment-6933066988). All 646 extracted receipt files match their published manifest hashes. Author narrative handoffs were not needed.

[R864] PASS Conformance - `hdl/milan/milan_datapath.sv:4638`, `hdl/milan/mailbox/KL_mbx_dma.sv:182`, `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:489`, and archived `author-r2/receipts/route/*/signoff.txt` - The cuts preserve the applicable interfaces and satisfy the authorized source-head timing acceptance.

The EDIT encode is a pure function of cluster offset, descriptor index and elaboration constants. `KL_mbx_cdc_window.sv:110` loads fields while leaving request low; IDLE, PRE, REQ replacement and ANS replacement paths all preserve a preparation edge before the new request. The registered word is therefore current whenever the split transaction server consumes it. The internal map-restoration requester cannot bypass this premise: the split branch ties `amr_own_r` low at `milan_datapath.sv:6175`. The all-fabric branch keeps the original combinational encode. No response cycle or 64-cycle window allowance changes.

The meter's reference is `old.grp_ts0_r + old.grp_off_r`, modulo 2^32. Opening adds one 125,000 ns PDU; each accepted interior PDU advances the same amount; closing subtracts the fifteenth-PDU offset to recover the original first timestamp. The active-group, gap, deviation, uncertainty, selection and timeout guards remain the same. The group mean, signed deviation, rate history and output pulse timing consequently retain their previous meaning. No new AAF or Milan interpretation is introduced.

The published per-corner values were independently regraded against WNS >= +0.030 ns and WHS >= 0. Every listed route has four passing corners, zero failing endpoints, all routable nets routed and zero routing errors:

| Image | Directive | Minimum WNS / WHS, ns |
|---|---|---|
| Split 8x8/1if | ExtraPostPlacementOpt | +0.293 / +0.033 |
| Split 8x8/1if | ExtraTimingOpt | +0.073 / +0.029 |
| Split 8x8/1if | AltSpreadLogic_high | +0.058 / +0.034 |
| Split 1x1/1if | ExtraPostPlacementOpt | +0.081 / +0.036 |
| Split 1x1/1if | ExtraTimingOpt | +0.135 / +0.033 |
| Split 1x1/1if | AltSpreadLogic_high | +0.126 / +0.033 |
| Release all-fabric 1x1 TDM8 | ExtraPostPlacementOpt | +0.553 / +0.023 |
| Split 8x8/1if, padded to 56.5 ROM tiles | ExtraPostPlacementOpt | +0.213 / +0.033 |
| Split 1x1/1if, padded to 43.5 ROM tiles | ExtraPostPlacementOpt | +0.049 / +0.036 |

The historical helper's rc=1 for two rows reflects its superseded +0.030 hold threshold; neither is a failure under the corrected authority. No new placement constraint, pblock, directive, seed or floor exception appears in the source delta. The ROM experiment's padding and temporary capacity allowance are confined to the measurement copy; they are not product changes.

The 8x8 routes were executed at `5d098172`, and the other routes at `338ece89`. The intervening HDL delta is comments only, independently checked; the last commit changes the render mutation. These are carried source-route receipts, not fresh routes executed on `0297a19a` or on current dev. The release netlist changes are disclosed and routed. The published release resource gate passes, including the RAMB36 decrease from 74 to 71. Release `bios.bin` and disassembly hashes are unchanged; ELF and library identity is after stripping debug sections, not raw ELF identity.

[R864] PASS RTL - `hdl/milan/mailbox/KL_mbx_dma.sv:294`, `hdl/milan/milan_datapath.sv:4638`, `hdl/common/cdc_pair_fifo.sv:103`, and `hdl/ieee1722/aaf/KL_tdm_render_master.sv:368` - Assignment sites, reset behavior, arithmetic widths, consumers and storage latency preserve the existing contracts.

For the DMA, reset establishes `ring_addr_r = base_r + (index_r & mask_r)`. An accepted start loads all operands and their address together. The only subsequent index changes are the FILL and R answer branches, both advancing the address with the same 16-bit next index. Every other branch holds both. Thus overflow, wrapping, zero-length starts, refused starts, CPU ownership, stalls and response errors preserve the invariant. An independent comparison ran the base and head concurrently on identical suite inputs: all 35 output ports and the internal address invariant matched throughout 520,041 checks.

The meter comparison matched all seven output ports and the internal reference invariant throughout the existing 465-check suite. The FIFO's two generated storage branches are identical except for `ram_style`; moving the memory processes preserves reset-qualified writes, read enable, registered read output, pointer updates and synchronizers. The TDM instance selects distributed RAM without changing its epoch/reset choreography or serializer prefetch. An independent three-way base/default/distributed comparison passed 200,000 stimulus steps at widths 192 and 48, depths 4 and 16, and a 5:7 clock ratio.

[R864] PASS Robustness - `tb/verilator/mbx/dma_main.cpp`, `tb/verilator/aaf_clock_meter/sim_main.cpp`, `tb/verilator/milan_dp/sim_split.cpp:461`, and `equivalence_checks.py` - Boundary, refusal, repeated-request, stall, wrap and reset paths were examined and exercised without a new mismatch.

The DMA suite covers every length of its 12-bit field, alignment refusal, partial final words, line boundaries, pending CPU requests, two-cycle register answers, busy starts and error responses. The meter suite exercises timestamp/sequence wrap, gaps, invalid formats, uncertainty transitions, source changes and timeout/holdover behavior. EDIT tests alternate accepted and refused cluster offsets, abort a transaction, remove and add mappings through all phases, check the live map and restore it. The FIFO comparison also exercises full/empty stretches, producer/consumer stalls and independently timed resets; this proves equivalence of simulated behavior, not that arbitrary independent resets form a supported lossless protocol. The production TDM epoch discipline remains unchanged.

[R864] PASS Tests - `tb/verilator/mbx/dma_mutants.py:52`, `tb/verilator/aaf_clock_meter/mutants.py:220`, `tb/verilator/milan_dp/split_mutants.py:83`, and `tb/verilator/milan_dp_render/tdm8_render_mutants.py:297` - The new plants compile and fail meaningful named checks; no assertion or acceptance threshold was weakened.

Independent execution at the reviewed head:

| Check | Result | Receipt |
|---|---|---|
| DMA positive control and full DMA mutation campaign | 520,041 checks, zero failures; 25/25 caught, including the step-behind address | `dma.log`, `dma.rc` |
| Meter positive control and both new reference plants | 465 checks, zero failures; both plants fail `[M2 indep] no history restart` | `meter.log`, `meter.rc` |
| Split integration control | 143 checks, zero failures, including EDIT DONE/tag/verdict and committed map contents | `split.log`, `split.rc` |
| Render serial control and distributed FIFO read-pointer plant | Control passes; plant fails both T6 FIRST EVENT and T6 PRESENTATION | `render.log`, `render.rc` |
| Base/head comparisons and FIFO three-way comparison | All output comparisons and arithmetic invariants pass | `equivalence.log`, `equivalence.rc` |

The render plant still passes frame identity while failing presentation timing, which is the defect it claims to detect. Replacing the ineffective write-at-read-pointer plant changes the injected defect; the original presentation checks remain unchanged. `PAIRFIFO_SRC` reaches the actual render build through both Makefiles. The published exact-head render campaign reports **32 checks, 32 PASS**, including controls and defect arms; that aggregate is not a claim of 32 distinct RTL mutations. Published carried receipts also show split mutations 29/29, dynamic-map campaign 71/71, meter campaign 38/38, CDC 13 checks and map-record suites at both shapes. The exact-head author native summary reports 65/65 suites and 2,713,101 checks. Those full banks were inspected, not independently rerun.

The CPU budget receipts at both shapes bind all eleven recorded checkout inputs to the reviewed head; only `KL_mbx_dma.sv` differs from their base checkout inputs. The control firmware ELF hash is identical at each shape. The completed head campaigns contain 96 and 95 groups, zero refusals and zero work passes over the share. All seven backlog BUDGET lines at each shape match the published base samples verbatim. Nine of eleven 8x8 STATED lines also match; `save-held` and `save-starved` at 23,756 cycles are not directly paired in those base samples. This is not evidence of a newly introduced regression: the changed DMA is cycle-equivalent by the complete assignment-site argument and the independent output comparison, and no service bound changes. It is a limit on the evidence: this review does **not** claim an exhaustive paired base CPU campaign or a verbatim base counterpart for those two lines. The source head remains rc=1 at 8x8 on the disclosed STATED debt, not an unconditional all-budget pass.

[R864] PASS Docs - `docs/design/MAILBOX_SPLIT.md:311` and `:1621`, `docs/design/MEDIA_CLOCK_FOLLOWING.md:2498`, both suite READMEs, the generated module matrix, PR #939 and the archived receipts - Changed interface assumptions, storage choice, release impact, test scope and measured resource effects are publicly reconstructable.

The documentation distinguishes the split's advance-held EDIT inputs from the all-fabric requester and records the cycle-free ring address. Traceability adds the render suite's direct FIFO source dependency. The code-comment delta contains behavior/reason and issue references without a new bench-lane or reviewer identity. No historical protocol requirement was restored. The increased slice counts beside decreased LUT counts are disclosed; this review does not treat a LUT reduction as a proof of lower placement pressure. The native and workflow receipts are author source evidence. The workflow summary explicitly separates 118 executed steps from 130 NOT RUN steps; neither those skips nor physical calibration NOT RUN supplies hardware proof.

Reviewer-owned completion ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #927 rulings; mailbox and meter authorities; four-corner route summaries; release and budget receipts | R864-1 | 0297a19a056ee3d5d705bc502c4ae7808689ede7 |
| RTL | CLEAN | Complete HDL delta; DMA assignments and output comparison; meter reference comparison; EDIT requester/mux/server; FIFO branches and TDM consumer | R864-1 | 0297a19a056ee3d5d705bc502c4ae7808689ede7 |
| Robustness | CLEAN | DMA and meter negative/boundary stimuli; EDIT invalid/repeated/abort/commit cases; FIFO clock/stall/reset comparison | R864-1 | 0297a19a056ee3d5d705bc502c4ae7808689ede7 |
| Tests | CLEAN | Complete test delta; independent positive controls and named mutations; archived campaigns, source hashes and native summaries | R864-1 | 0297a19a056ee3d5d705bc502c4ae7808689ede7 |
| Docs | CLEAN | Complete documentation/comment delta; PR and issue; receipt manifest/provenance; generated matrix | R864-1 | 0297a19a056ee3d5d705bc502c4ae7808689ede7 |

Prior public findings: the PR discussion fetched after the independent diff pass contained only the two public review-start notices, with no prior finding to resolve or retain. A subsequent direct read of review submissions and inline review threads returned empty lists for both. The twin's `split-talker-failed` and `srp-plus-k` lines are the explicitly excluded base-owned results, not findings from this round. The scheduling decision to pull reviews forward is also not a finding.

Limits and pending manager duties: no manager source bank ran at this exact head, and none is claimed. No full parent, processor, synthesis or builder bank, physical test, Docker/local workflow replica, source fix, commit, push or GitHub write was performed by this review. The timing audit reads published summaries and checkpoint/report hashes; the large routed checkpoints were not independently rerouted. The manager must construct and validate the actual merge candidate against live dev, obtain its builder/native and applicable physical-timing evidence, satisfy hosted/local workflow acceptance while distinguishing executed and skipped jobs, reconcile the independent reviews, and perform authorized merge and post-merge containment. Live dev supplied for this round was `e275d7950ef3385753e6a15d2e191ba855b171ed`; a later dev tip requires a fresh candidate. The source routes do not prove that candidate, and desk checks do not establish field or physical calibration acceptance.

`checkout-integrity.log` verifies the original clone's 1,626 tracked blobs, modes and complete index against the reviewed tree, plus every tracked blob/mode/index and exact gitlink in the four required submodules. No source restoration was necessary: all probes and builds were confined to disposable paths under this packet's `scratch/`. `MANIFEST.sha256` identifies the publishable scripts and receipts. Nothing under `scratch/` is publishable.

R864-1 FINISHED

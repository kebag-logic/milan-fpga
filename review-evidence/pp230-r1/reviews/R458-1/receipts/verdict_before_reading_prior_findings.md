[R458] NEGATIVE - exact head 65324390d1b83c4587f299d06597f7a571d7fa61

**Round:** R458-1, the internal cleared-context review of kebag-logic/milan-fpga#230 / Mister-M-alt/protocol-processor-control-plane-avb-milan PR #154.

- **Head:** `65324390d1b83c4587f299d06597f7a571d7fa61`, tree `2fb3aabcf7eecc4589dcf19f637e99a57431772a`.
- **Diff:** base `c4cb84ff8cecad19bedaa85dde594a8ed68012f6`, two one-line commits with no trailers.
- **Lenses applied:** all five (Conformance, RTL, Robustness, Tests, Docs).

**Verdict: NEGATIVE, on three MINOR findings. None is in the RTL.**
- **The RTL change is cycle-exact.** I checked it by reading the code, with my own lockstep benches, against the committed suites and through both SRP campaigns. In every check base and head behave identically.
- **What fails is the evidence trail:**
  - the new storage paths are not protected by committed tests (F1);
  - the Vivado figures cannot be re-derived from anything public (F2);
  - the PR body overstates what the planted controls showed (F3).

No prior public review finding exists on PR #154: at review time it carries only the two review-start comments. There is nothing to resolve or retain.

## Reconstruction

- **Authorities.** milan-fpga `AGENTS.md` and `CONTRIBUTING.md` (at dev `241f9184`), the processor `README.md`, and `docs/architecture/10_srp_engine.md`.
- **Issue #230.**
  - The body's acceptance criteria are frozen.
  - The lane assignment is 5974045353: levers 2 and 4, behaviour identical, a lockstep bench with planted controls, and the #638 recipe.
  - The executor's STOP is 5977826098.
  - The ruling is 5977836860: (b), the parallel evaluation is final for #230 and (a) goes to #640.
- **Scope rulings respected.** Lever 4's shared evaluator is out of scope and is not judged here. The issue closes by hand at the processor merge.
- **Public evidence.** milan-fpga `8dca0983`, `review-evidence/pp230-r1`. It holds the executor's HANDOFF.md, PR-BODY.md and the two parent patches. Their sha256 match `MANIFEST.json` (`receipts/evidence_digests.txt`).
- **PR body.** The live body equals the published PR-BODY.md, apart from one blank line.
- **Hosted contexts at the exact head.** `docs-gates` and `portability` succeeded. `suites` was still in progress at review time (`receipts/hosted_checks_at_review_start.tsv`). The manager owns hosted acceptance.

## What I ran (all at the exact head; base = `c4cb84ff`)

Verilator 5.050 was the pinned tool; its wrapper sha256 is `905795b9...979e92f`. I ran no repository bank. Receipts are under `receipts/`, scripts under `lockstep/` and `vivado/`.

| Check | Result | Receipt |
|---|---|---|
| `tb/srp_top`, `tb/srp_stream_fsms`, `tb/srp_admission` (all five shapes), base and head | All rc 0. 2,200, 1,219 and 1,138 / 12,615 / 41,012 / 201,073 / 991,231 checks, all PASS. Result lines byte-identical between base and head | `suites_base_head.txt` |
| `scripts/lint_hdl.sh`; the three changed modules and `KL_srp_top` linted at N = 1, 2, 3, 9 | rc 0, 41 of 41 LINT OK. 0 diagnostics at every shape | `lint_head.txt` |
| `tb/srp_top/mutants.py --jobs 4`, base and head | rc 0, 90 checks: 90 PASS at both. 73 patches in the tree, none failed to apply. The record is identical (sorted, paths normalised) | `campaigns_base_head.txt` |
| `tb/srp_admission/mutants.py --jobs 4`, base and head | rc 0, 12 / 12 at both. Identical record | `campaigns_base_head.txt` |
| My top lockstep: the committed `tb/srp_top` stimulus, all groups, through base and head `KL_srp_top` together (8/8). 51 outputs and 24 internal signals compared every cycle. Unreset state random and different per copy, 4 seeds | 4 x 185,012,669 cycles: **0 output and 0 internal mismatches** | `top_lockstep.txt` |
| My module-level random lockstep: talker, listener and admission at N = 1, 2, 3, 4, 5, 8, 9, 8 seeds x 4,000,000 cycles each. Pooled values, re-declarations with a new TSpec, settles and teardowns, back-pressure, 884 mid-run resets per shape | 224,000,000 cycles: **0 mismatches** in all three modules at every N, over both elaboration arms. 1.6M to 9.6M talker walk pushes per shape | `fsm_lockstep_campaign.txt` |
| 17 one-edit fault probes of the new storage paths: committed suites plus both lockstep benches | Every non-vacuous probe is caught by my benches. **8 survive every committed processor suite** (F1) | `probe_results.txt` |
| My Vivado 2026.1 out-of-context synthesis of `KL_srp_top` alone (`vivado/srp_map.tcl`): head at 2/2 and 9/9, base at 2/2. One instance, under the shared lock. A mapping check, not the #638 recipe | Head maps every new memory to distributed RAM with **0 flip-flops**: FIFOs `RAM32M x 8` each, `wtsp_r` x 12, `g_wid_ram.wid_r` x 21 and `g_wsid_ram.wsid_r` x 11 (9/9 only), `slope_q_r` x 6. The only block RAM is the decoder's RAMB18. Base 2/2 keeps 2,240 FIFO flip-flops and 64 slope flip-flops, plus the talker's TSpec fields. This matches the RAM rows HANDOFF section 3 quotes | `vivado_srp_mapping.txt`, `vivado-*/` |
| Committed `tb/srp_top` alone, with unreset state randomised | Base and head fail the same 4 checks on seeds 1, 2 and 4 and pass on seed 3: pre-existing, outside this diff (observation O1) | `xinit_srp_top_base_head.txt`, `xinit_localisation.txt` |

## Findings

### F1: MINOR (Tests). The new storage paths and the N <= 2 arm have no committed test; equivalence rests on an unpublished bench

- **Where.**
  - `hdl/srp/KL_srp_talker_fsm.sv:500-518`: `wtsp_r` always, then `g_wid_ram` or `g_wid_flops`.
  - `hdl/srp/KL_srp_listener_fsm.sv:541-551`: `g_wsid_ram` or `g_wsid_flops`.
  - The committed benches, which elaborate the FSMs only at 8:
    - `tb/srp_top/srp_top_wrap.sv:253-254` (only `SLOT_AW_P` is overridden, so the defaults 8/8 apply);
    - `tb/srp_stream_fsms/srp_stream_fsms_wrap.sv:22` (`N_STREAMS_P = 8`);
    - `tb/pp_top/pp_top_wrap.sv:529` (top defaults `N_STREAM_IN_P`/`N_STREAM_OUT_P` = 8, `hdl/top/protocol_processor_top.sv:83,85`).
- **Evidence.**
  - Probes that survive `tb/srp_top` and `tb/srp_stream_fsms` (rc 0), yet are caught by my lockstep (`receipts/probe_results.txt`):
    - `wtsp-read-at-gate-source`: the walk TSpec read at the gate source;
    - `wtsp-first-open-only`: a re-declaration keeps the stale TSpec, published in the Talker Advertise;
    - `wid-ram-first-open-only`;
    - `wsid-ram-first-settle-only`;
    - `wsid-ram-written-on-teardown`.
  - Three more survivors sit in the **N <= 2 flop arms, the shipping 1x1 shape**, which no processor suite elaborates: `wid-flops-da-of-gate-source`, `wid-flops-sid-of-source-0` and `wsid-flops-of-control-sink`.
  - The executor's lockstep bench and its sixteen controls are "scratch, not committed" (HANDOFF section 4.1 and section 10). They are not in the public evidence, so the equivalence claim cannot be re-run by a cold reviewer from public state.
- **Authority.**
  - AGENTS section 5: add or update self-checking tests, and test boundary and configuration paths.
  - AGENTS section 6, Tests: each test can fail for the defect it claims to detect.
  - AGENTS section 2: a cold reviewer reconstructs from GitHub and the repository alone.
  - CONTRIBUTING section 3: every RTL change ships with a self-checking harness.
  - The #232 precedent: manager round 2, item 1, for R452-1 F1 = R453-1 F2: "Every reviewer probe, run unchanged, must be caught by a committed test."
- **Impact.** A later edit can do any of these and still pass every processor suite and campaign:
  - break re-declaration TSpec capture;
  - break the listener walk copy;
  - break the 1x1 flop-arm read path.
- **Required outcome.**
  - Committed, self-checking coverage that kills each of the eight surviving probes: a committed lockstep against a frozen reference, or directed arms.
  - It runs at both arms (N <= 2 and N >= 3).
  - The probes are planted as killed controls in a committed campaign (`tb/srp_top/mutants.py` or `tb/srp_stream_fsms`), and recorded in the README.
- **Verification.** Run `lockstep/probes.py` unchanged against the new head. Every non-vacuous probe must be caught by a committed suite or campaign.

### F2: MINOR (Conformance, Docs). The before/after Vivado evidence is not public, so the figures cannot be re-derived

- **Where.**
  - The PR body's Vivado table.
  - HANDOFF sections 3, 5.2-5.6 and 10.
  - `docs/architecture/10_srp_engine.md:234-248`: the normative per-context figures.
- **Evidence.**
  - The evidence packet holds no report, log or extract.
  - HANDOFF section 5.6 names `baseline.log` / `elaborate.log` files by a 16-hex-digit prefix only, and section 10 places them in the executor's scratch.
  - The review brief asks for these to be re-derived from the published reports. I could not re-derive any of them:
    - route 51,434 -> 51,005 LUT, 59,691 -> 57,262 FF, WNS +0.079 -> +0.354;
    - the 1x1 and 8x8 standalone figures;
    - the `u_srp` sub-block table;
    - the "no SRP structure in block RAM or flops" mapping lines (`:2031-2052`, `:3704-3709`).
  - What I could check holds:
    - every published delta;
    - the logic + memory LUT splits;
    - the `u_srp` LUTRAM sums (route 298, 1x1 310, 8x8 438);
    - the per-context divisions behind 10 section 5.1 (talker 129/168, listener 208/278, admission 69/69, engine 475/538, base 213/221, 227/278, 73/101, 592/679).
- **Authority.**
  - Issue #230 acceptance: "Before-and-after hierarchical Vivado reports show a material reduction" and "Timing ... does not regress below zero WNS".
  - AGENTS section 6, Docs: the PR and Issue contain enough evidence for a cold reviewer.
  - CONTRIBUTING section 3: measure, don't assume.
  - The #232 precedent: R453-1 F1; manager round 2, item 2, "Publish the Vivado evidence ... each file with its full sha256".
- **What I could confirm independently.** My out-of-context mapping check of `KL_srp_top` alone (`receipts/vivado_srp_mapping.txt`) agrees with the mapping rows HANDOFF quotes. It cannot confirm the product-level LUT, FF or WNS figures or the per-context costs.
- **Impact.** Two acceptance criteria, and the figures written into a normative document, rest on files that no reviewer can open.
- **Required outcome.**
  - Publish extracts in the evidence packet for base and head, for the route, 1x1 and 8x8, each with its full sha256:
    - hierarchical utilization including the `u_srp` sub-blocks;
    - the RAM mapping report rows, both distributed and block;
    - the timing summary;
    - the route status;
    - the flip-flop census lines HANDOFF section 3 cites.
- **Verification.** A reviewer re-derives every figure in the PR body table, HANDOFF sections 3 and 5.2-5.4, and 10 section 5.1 from the published extracts.

### F3: MINOR (Tests, Docs). The PR body overstates what the planted controls showed

- **Where.** PR #154 body, Validation: "Sixteen planted controls were each caught at every shape where the edited code is elaborated."
- **Evidence.** The executor's own HANDOFF section 4.2 shows zeros at shapes where the edited code *is* elaborated:
  - `tf-head-at-write-pointer` and `tf-listener-push-dropped` at 1/1. The FIFOs exist at every shape; HANDOFF says "the situation ... did not arise".
  - `slope-stored-at-stage-2-index`, `slope-store-source-0-only` and `wsid-flops-of-control-sink` at 1/1. These are equivalent by construction.
  
  HANDOFF's own wording, "each at three or four shapes", is accurate. The PR body's is not.
- **Authority.** AGENTS section 6, Docs: evidence for a cold reviewer must be accurate. This is a claim about test results, so under the owner rule of 2026-10-02 it is not wording-only residue.
- **Impact.** The claim overstates the controls' coverage of the FIFO edits at the 1/1 shape.
- **Required outcome.** The PR body states what HANDOFF section 4.2 shows. That is: each control was caught at three or four shapes; a zero means not elaborated, equivalent by construction, or (for the two FIFO controls at 1/1) the needed situation did not arise.
- **Verification.** Compare the PR body line against the published control table.

### Suggestions and observations (not counted)

- **S1 (SUGGESTION): the timer-arm FIFO full boundary is never exercised.**
  - The committed `tb/srp_top` stimulus peaks at 6 of 32 entries. The FIFO counts below are per FIFO, talker then listener:
    - full cycles: 0;
    - pushes at full: 0;
    - pushes to empty at the read pointer: 234 and 253;
    - same-cycle push and pop: 109 and 1;
    - write-pointer wraps: 3 and 2.
  - `tf-full-guard-31` survives the committed suite and my lockstep. The HANDOFF bench reports no FIFO occupancy at all.
  - Full looks unreachable by the depth argument at `KL_srp_top.sv:940-941`. The guard `:963-964` and every memory enable, address and data are textually unchanged, so equivalence at full holds by construction.
  - A directed arm that fills a FIFO would make the guard testable. This is pre-existing and not a defect of this PR.
- **O1 (observation, outside this diff; for the manager to file).**
  - The committed `tb/srp_top` suite fails 4 checks ("0: no malformed PDUs", "F3/F4/F5: no PDU we fed was tolerance-discarded") when unreset state starts random. That is `--x-initial unique` plus `randReset(2)`; seeds 1, 2 and 4 fail and seed 3 passes.
  - Base `c4cb84ff` fails identically, and my base/head lockstep shows identical outputs, so this PR does not cause it.
  - Zeroing the TX-slot memory, or the decoder/encoder/VLAN/timer-service memories, does not remove it (`receipts/xinit_localisation.txt`). The dependency is elsewhere: in flop initial state or the harness.

## Lens results

- **[R458] PASS RTL.**
  - Artifacts:
    - `hdl/srp/KL_srp_top.sv:944-984`;
    - `hdl/srp/KL_srp_talker_fsm.sv:352-372,495-537,540-596`;
    - `hdl/srp/KL_srp_listener_fsm.sv:531-559,620-635`;
    - `hdl/srp/KL_srp_admission.sv:100-260`.
  - **Writers and readers.** Each RAM copy has exactly the flop record's writer and condition:
    - the talker: `rst_n && gate_acc_w && gate_open_i`, matching `:587-592`;
    - the listener: `rst_n && ctl_acc_w && ctl_settle_i`, matching `:622-626`;
    - the slopes: every non-reset cycle at `cidx_q2_r`, as at base.
    
    Each copy is read only under the valid bit written in the same edge (`:615`, `:655`, `fit_w` / `refuse_w` / `pend_w`), and neither `rec_valid_r` nor the record is ever cleared outside reset. So the missing reset is unobservable.
  - **FIFO.** Same pointers, guard and enables. A registered read of an asynchronous memory read gives pre-edge data in simulation and in distributed RAM alike.
  - **Indices.** Out-of-range indices cannot reach the FSMs (`KL_srp_top.sv:847-880`).
  - **Timing and resources.** The published deltas are internally consistent. My mapping check shows every new memory as distributed RAM, no new block RAM and no flip-flop spill at 2/2 or 9/9 (`receipts/vivado_srp_mapping.txt`).
- **[R458] PASS Robustness.**
  - **Reset during activity.** 884 mid-run resets per shape in the module lockstep, plus the committed bench's per-group resets at top level, with unreset memories carried across them.
  - **Unreset memories** were randomised differently in each copy.
  - **Minimum and maximum shapes:** N = 1..9.
  - **Invalid ordering:** random re-declarations and teardowns.
  - **Back-pressure:** `ev_ready`.
  - **Configuration-dependent arms:** N <= 2 and N >= 3 are both equal to base.
  - **FIFO boundaries:** pushes to empty at the read pointer and same-cycle push/pop were reached; full is covered by construction (S1).
  - Receipts: `fsm_lockstep_campaign.txt`, `top_lockstep.txt`.
- **[R458] UNCLEAN Tests:** F1 and F3. The committed suites and campaigns are green and equal at base and head, but they do not protect the new paths.
- **[R458] UNCLEAN Conformance:** F2.
  - Acceptance criteria 1, 3 and 4 are otherwise supported:
    - the SRP suites pass;
    - every per-stream structure is sized by `N_SOURCES_P`/`N_SINKS_P`, which the top binds from `N_STREAM_OUT_P`/`N_STREAM_IN_P` (`hdl/top/protocol_processor_top.sv:2484-2485`), so a 1x1 binding of 2 elaborates no inactive slot (the census itself is in the unpublished reports, F2);
    - WNS is reported positive.
  - Criterion 2 and the WNS figure are not publicly verifiable. Criterion 5 ("documented in #229") is outside the lane, as recorded in the STOP.
  - Clause 35 behaviour is unchanged because outputs are cycle-identical.
- **[R458] UNCLEAN Docs:** F2 and F3.
  - **10 section 5.1** (`docs/architecture/10_srp_engine.md:194-248`) matches the RTL:
    - FIFO width 41 + `SLOT_AW_P`;
    - `wtsp_r` M x 68;
    - `wid_r` M x 124 from M = 3;
    - `wsid_r` N x 64;
    - slopes M x 32;
    - the banners updated in both FSMs.
  - **No stale storage description** remains in 10 sections 4, 5 and 11.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | issue #230 acceptance, 5974045353, 5977826098, 5977836860; PR body Vivado table; HANDOFF sections 3 and 5; lockstep receipts | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| RTL | CLEAN | `hdl/srp/KL_srp_top.sv:944-984`, `KL_srp_talker_fsm.sv:352-618`, `KL_srp_listener_fsm.sv:531-659`, `KL_srp_admission.sv:100-260`; lint at N = 1, 2, 3, 9; both lockstep benches | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| Robustness | CLEAN | module lockstep at N = 1..9 with resets and randomised memories; top lockstep 4 seeds; FIFO boundary counters; index guards `KL_srp_top.sv:847-880` | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| Tests | UNCLEAN (F1, F3) | `tb/srp_top`, `tb/srp_stream_fsms`, `tb/srp_admission` (all shapes); `srp_top` and `srp_admission` campaigns at base and head; 17 probes; HANDOFF section 4; PR body Validation | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| Docs | UNCLEAN (F2, F3) | `docs/architecture/10_srp_engine.md:147-260,736-760`; RTL banners and comments in the four files; PR body; HANDOFF | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |

## Real limits

- **Vivado.** I could not re-derive the Vivado figures: no report is public (F2). My own out-of-context synthesis of `KL_srp_top` alone checks the RAM mapping only. It does not stand in for the #638 recipe, the integrated route or the timing figures.
- **Not run, by assignment:** the full processor bank (`run_suites.sh`), `make check`, `gen_matrix --check`, the Yosys gate, and the parent consumer set or builder. The `tb/pp_top`, maap and adp campaigns were not run either. Their SRP inputs are cycle-identical by both lockstep benches.
- **The executor's lockstep bench** (56 internal compares, its MRPDU generator) was not inspected: it is not public (F1). My benches are independent reconstructions.
- **Out of scope.** Physical calibration was not run. Field or hardware behaviour is not proven by any of the above.

## Pending manager duties

- **Hosted acceptance** at the exact head: `suites` was in progress when I looked.
- **Bank evidence.** The source static/builder and native bank receipts the brief cites were not visible on #230, PR #154 or evidence `8dca0983` at review time; publish them.
- **The candidate merge build** on live dev `241f91845230ae410506dffb16b71937127fd175`. The executor's consumer record is at dev `5fabb46e`. Gate 16's two T30 checks belong to #643 / PR #648.
- **Filing.** File O1 as a new issue if accepted.

## Restoration

I made no edit to the clone. Every probe ran on copies under the packet's scratch. After the round:
- the clone's HEAD is the exact head;
- `git status` is clean;
- the index tree equals the HEAD tree;
- the repository has no submodule gitlinks (see `receipts/restore_check.txt`).

R458-1 FINISHED

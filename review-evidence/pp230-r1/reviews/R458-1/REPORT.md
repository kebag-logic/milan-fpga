[R458] NEGATIVE - exact head 65324390d1b83c4587f299d06597f7a571d7fa61

**Round:** R458-1, the internal cleared-context review of kebag-logic/milan-fpga#230 / Mister-M-alt/protocol-processor-control-plane-avb-milan PR #154.

- **Head:** `65324390d1b83c4587f299d06597f7a571d7fa61`, tree `2fb3aabcf7eecc4589dcf19f637e99a57431772a`.
- **Diff:** base `c4cb84ff8cecad19bedaa85dde594a8ed68012f6`, two one-line commits with no trailers.
- **Lenses applied:** all five (Conformance, RTL, Robustness, Tests, Docs).

**Verdict: NEGATIVE, on two open MINOR findings. Neither is in the RTL.**
- **The RTL change is cycle-exact.** I checked it by reading the code, with my own lockstep benches, against the committed suites, through both SRP campaigns and with an independent synthesis mapping check. In every check base and head behave identically.
- **The two open findings:**
  - the new storage paths are not protected by committed tests (F1);
  - the PR body still overstates how many shapes the planted controls caught (F3).
- **Resolved during the round:** the Vivado evidence finding (F2), by the publication at milan-fpga `06fe795b`. I re-derived every figure from it.

**Order of work.** My verdict and ledger were written first, from my own independent pass. That draft is kept as `receipts/verdict_before_reading_prior_findings.md` (sha256 `fb8f412e...5f3266`). Only then did I read the prior public review on this PR, R459-1 (comment 5978360032), and the manager's response (5978368336). Both arrived during my round. Their findings are resolved or retained below, and F2 and F3 were re-judged against the public state the response created. The head did not change.

## Reconstruction

- **Authorities.** milan-fpga `AGENTS.md` and `CONTRIBUTING.md` (at dev `241f9184`), the processor `README.md`, `docs/architecture/10_srp_engine.md` and `docs/guides/hdl-engineer.md` section 3.1.
- **Issue #230.**
  - The body's acceptance criteria are frozen.
  - The lane assignment is 5974045353: levers 2 and 4, behaviour identical, a lockstep bench with planted controls, and the #638 recipe at 50 MHz.
  - The executor's STOP is 5977826098.
  - The ruling is 5977836860: (b), the parallel evaluation is final for #230 and (a) goes to #640.
- **Scope rulings respected.** Lever 4's shared evaluator is out of scope and is not judged here. #230 closes by hand at the processor merge.
- **Public evidence.**
  - milan-fpga `8dca0983`, `review-evidence/pp230-r1`: HANDOFF.md, PR-BODY.md and two parent patches. Their sha256 match `MANIFEST.json`.
  - milan-fpga `06fe795b`, the same directory plus `author-r1/vivado/`: the eight Vivado runs. All 58 files match that `MANIFEST.json`, and the eight logs' original digests equal the HANDOFF section 5.6 prefixes. Receipts: `evidence_digests.txt` and `vivado_rederivation_06fe795b.txt`.
- **PR body.** I read it at review start. It was edited at 09:06 UTC, and the version judged here is that edited one (see F3).
- **Hosted contexts at the exact head.** `docs-gates` and `portability` succeeded. `suites` was still in progress at my last read (`hosted_checks_at_review_end.tsv`). The manager owns hosted acceptance.

## What I ran (all at the exact head; base = `c4cb84ff`)

Verilator 5.050 was the pinned tool; its wrapper sha256 is `905795b9...979e92f`. I ran no repository bank. Receipts are under `receipts/`, scripts under `lockstep/` and `vivado/`.

| Check | Result | Receipt |
|---|---|---|
| `tb/srp_top`, `tb/srp_stream_fsms`, `tb/srp_admission` (all five shapes), base and head | All rc 0. 2,200, 1,219 and 1,138 / 12,615 / 41,012 / 201,073 / 991,231 checks, all PASS. Result lines byte-identical between base and head | `suites_base_head.txt` |
| `scripts/lint_hdl.sh`; the three changed modules and `KL_srp_top` linted at N = 1, 2, 3, 9 | rc 0, 41 of 41 LINT OK. 0 diagnostics at every shape | `lint_head.txt` |
| `tb/srp_top/mutants.py --jobs 4`, base and head | rc 0, 90 checks: 90 PASS at both. 73 patches, none failed to apply. The record is identical (sorted, paths normalised) | `campaigns_base_head.txt` |
| `tb/srp_admission/mutants.py --jobs 4`, base and head | rc 0, 12 / 12 at both. Identical record | `campaigns_base_head.txt` |
| My top lockstep: the committed `tb/srp_top` stimulus, all groups, through base and head `KL_srp_top` together (8/8). 51 outputs and 24 internal signals compared every cycle. Unreset state random and different per copy, 4 seeds | 4 x 185,012,669 cycles: **0 output and 0 internal mismatches** | `top_lockstep.txt` |
| My module-level random lockstep: talker, listener and admission at N = 1, 2, 3, 4, 5, 8, 9, 8 seeds x 4,000,000 cycles each. Pooled values, re-declarations with a new TSpec, settles and teardowns, back-pressure, 884 mid-run resets per shape | 224,000,000 cycles: **0 mismatches** in all three modules at every N, over both elaboration arms. 1.6M to 9.6M talker walk pushes per shape | `fsm_lockstep_campaign.txt` |
| 17 one-edit fault probes of the new storage paths: committed suites plus both lockstep benches | Every non-vacuous probe is caught by my benches. **8 survive every committed processor suite** (F1) | `probe_results.txt` |
| My Vivado 2026.1 out-of-context synthesis of `KL_srp_top` alone (`vivado/srp_map.tcl`): head at 2/2 and 9/9, base at 2/2. One instance, under the shared lock. A mapping check, not the #638 recipe | Head maps every new memory to distributed RAM with **0 flip-flops**: FIFOs `RAM32M x 8` each, `wtsp_r` x 12, `g_wid_ram.wid_r` x 21 and `g_wsid_ram.wsid_r` x 11 (9/9 only), `slope_q_r` x 6. The only block RAM is the decoder's RAMB18. Base 2/2 keeps 2,240 FIFO flip-flops and 64 slope flip-flops, plus the talker's TSpec fields | `vivado_srp_mapping.txt`, `vivado-*/` |
| The published Vivado runs (`06fe795b`), re-derived | Every figure in the PR body table, HANDOFF sections 5.2-5.4 and 10 section 5.1 matches the reports (F2 resolution) | `vivado_rederivation_06fe795b.txt` |
| Committed `tb/srp_top` alone, with unreset state randomised | Base and head fail the same 4 checks on seeds 1, 2 and 4 and pass on seed 3: pre-existing, outside this diff (O1) | `xinit_srp_top_base_head.txt`, `xinit_localisation.txt` |

## Findings

### F1: MINOR (Tests), OPEN. The new storage paths and the N <= 2 arm have no committed test; equivalence rests on an unpublished bench

- **Where.**
  - `hdl/srp/KL_srp_talker_fsm.sv:500-518`: `wtsp_r` always, then `g_wid_ram` or `g_wid_flops`.
  - `hdl/srp/KL_srp_listener_fsm.sv:541-551`: `g_wsid_ram` or `g_wsid_flops`.
  - The committed benches, which elaborate the FSMs only at 8:
    - `tb/srp_top/srp_top_wrap.sv:253-254` (only `SLOT_AW_P` is overridden, so the defaults 8/8 apply);
    - `tb/srp_stream_fsms/srp_stream_fsms_wrap.sv:22` (`N_STREAMS_P = 8`);
    - `tb/pp_top/pp_top_wrap.sv:529`, through the top's binding `hdl/top/protocol_processor_top.sv:2484-2485` and its defaults of 8 (`:83,85`).
- **Evidence.**
  - Probes that survive `tb/srp_top` and `tb/srp_stream_fsms` (rc 0), yet are caught by my lockstep (`receipts/probe_results.txt`):
    - `wtsp-read-at-gate-source`: the walk TSpec read at the gate source;
    - `wtsp-first-open-only`: a re-declaration keeps the stale TSpec, published in the Talker Advertise;
    - `wid-ram-first-open-only`;
    - `wsid-ram-first-settle-only`;
    - `wsid-ram-written-on-teardown`.
  - Three more survivors sit in the **N <= 2 flop arms, the shipping 1x1 shape**, which no processor suite elaborates: `wid-flops-da-of-gate-source`, `wid-flops-sid-of-source-0` and `wsid-flops-of-control-sink`.
  - The executor's lockstep bench and its sixteen controls stay "in scratch" (HANDOFF sections 4.1 and 10; the edited PR body says the same). A cold reviewer cannot re-run the equivalence claim from public state.
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

### F2: MINOR (Conformance, Docs). RESOLVED at this head by evidence `06fe795b`

- **As raised.** The before/after Vivado reports behind acceptance criteria 2 and 4 were not public, and neither were the figures in `docs/architecture/10_srp_engine.md:234-248`. Only 16-hex digests in HANDOFF section 5.6 were available.
- **Resolution.** milan-fpga `06fe795b` publishes the eight runs, and the eight logs' original sha256 equal the HANDOFF section 5.6 prefixes. From those reports I re-derived (`receipts/vivado_rederivation_06fe795b.txt`):
  - **Route 1x1:**
    - LUT 51,434 (49,158 + 2,276) -> 51,005 (48,611 + 2,394);
    - FF 59,691 -> 57,262;
    - slices 15,847 -> 15,837;
    - RAMB36 79 (92.5 tiles less 27 RAMB18) and DSP 14 at both;
    - WNS/WHS +0.079/+0.014 -> +0.354/+0.036;
    - 107,053 and 104,430 nets, all fully routed, 0 with routing errors.
  - **Standalone 1x1:** 24,930 -> 24,258 LUT, 25,465 -> 23,130 FF, estimate -2.059 -> -1.874.
  - **Standalone 8x8:** 32,584 -> 31,109 LUT, 34,211 -> 30,648 FF, estimate -2.161 -> -1.495.
  - **The whole `u_srp` sub-block table** of HANDOFF section 5.3, including top glue `(u_srp)` 921 -> 350, 907 -> 354 and 1,053 -> 297.
  - **The per-context divisions** in 10 section 5.1.
  - **The RAM mapping lines** HANDOFF section 3 cites (head 1x1 `:2030-2036`, 8x8 `:2045-2052`, route `:3704-3709`; base 1x1 `:1827`). The only SRP block RAM is the decoder's `tp_ram` RAMB18 at all three head endpoints.
  - These agree with my own mapping check.
- **Residual limit (not a finding).** The flip-flop census file HANDOFF section 3 cites (`baseline_cells.tsv`, e.g. `tf_ram_r` 2,304) is not published. It is corroborated twice over: the published top-glue FF drops by 2,291 at 1x1, and my own standalone census finds 2,240 base FIFO flip-flops and 0 at head.

### F3: MINOR (Tests, Docs), OPEN (retained in amended form). The PR body overstates how many shapes the planted controls caught

- **Where.** PR #154 body, Validation, as edited at 09:06 UTC: "Sixteen planted controls were each caught at three or four of the four shapes."
- **Evidence.** In the executor's own control table (HANDOFF section 4.2) six of the sixteen controls are caught at fewer than three shapes:
  - at two shapes: `wid-ram-first-open-only`, `wid-ram-read-at-gate-source` (9/9 and 3/5), `wid-flops-da-of-gate-source` (2/2 and 1/1), `wsid-ram-written-on-teardown` and `wsid-ram-first-settle-only` (9/9 and 3/5);
  - at one shape: `wsid-flops-of-control-sink` (2/2).
  
  HANDOFF's own "each at three or four shapes" is wrong in the same way. My draft (receipt above) wrongly called that HANDOFF wording accurate; I correct that here.
  
  What the edit did fix: the body's second sentence now explains each zero correctly (not elaborated, equivalent at one source or sink, or two FIFO controls at 1/1), and the original "every shape where the edited code is elaborated" is gone.
- **Authority.** AGENTS section 6, Docs: evidence for a cold reviewer must be accurate. This is a claim about test results, so under the owner rule of 2026-10-02 it is not wording-only residue.
- **Impact.** The public description claims broader control coverage than the executor's own table shows.
- **Required outcome.** The count matches HANDOFF section 4.2. For example: "Sixteen planted controls were each caught at every shape where the edited arm is elaborated and the edit is not equivalent by construction, except two FIFO controls at 1/1, whose situation the runs did not produce (one to four shapes each; HANDOFF section 4.2)."
- **Verification.** Compare the body sentence against the published control table row by row.

### Suggestions and observations (not counted)

- **S1 (SUGGESTION): the timer-arm FIFO full boundary is never exercised by committed stimulus.**
  - The committed `tb/srp_top` stimulus peaks at 6 of 32 entries. The FIFO counts below are per FIFO, talker then listener:
    - full cycles: 0;
    - pushes at full: 0;
    - pushes to empty at the read pointer: 234 and 253;
    - same-cycle push and pop: 109 and 1;
    - write-pointer wraps: 3 and 2.
  - `tf-full-guard-31` survives the committed suite and my lockstep.
  - The guard (`KL_srp_top.sv:963-964`) and every memory enable, address and data are textually unchanged, so equivalence at full holds by construction.
  - A directed arm that fills a FIFO would make the guard testable. This is pre-existing.
- **O1 (observation, outside this diff; for the manager to file).**
  - The committed `tb/srp_top` suite fails 4 checks ("0: no malformed PDUs", "F3/F4/F5: no PDU we fed was tolerance-discarded") when unreset state starts random. That is `--x-initial unique` plus `randReset(2)`; seeds 1, 2 and 4 fail and seed 3 passes.
  - Base fails identically, and base and head outputs are identical, so this PR does not cause it.
  - Zeroing the TX-slot, decoder, encoder, VLAN and timer-service memories does not remove it.

## Prior public review findings at this head (R459-1, comment 5978360032)

| Finding | Status at this head | Basis |
|---|---|---|
| R459-1-F1 (MINOR, Conformance/Docs): area figures on unpublished receipts | **Resolved** | Same as my F2: re-derived from `06fe795b` |
| R459-1-F2 (MINOR, Tests/Docs): PR body overstates control coverage | **Retained (amended)** | The 09:06 edit fixed the original clause but introduced "three or four of the four shapes", which six controls contradict. Carried as my F3 |
| R459-1-R1 (RESIDUE, Docs): "10 section 5.1" ambiguous in the PR body | **Retained as RESIDUE** | Still at body lines 23, 62 and 71. Exact fix: write "`docs/architecture/10_srp_engine.md` section 5.1". Wording only |
| R459-1-R2 (RESIDUE, Docs): "## Validation (all rc 0, no pipes)" while gate 16 exits 2 | **Retained as RESIDUE** | Still at body line 106. The same section states gate 16's rc 2, so no reader is left with a wrong result. Exact fix: "## Validation (all rc 0 except parent gate 16, recorded against #643; no pipes)" |
| R459-1-S1 (SUGGESTION): name the new memories in `docs/guides/hdl-engineer.md:72-88` | **Agreed, SUGGESTION** | The CAM-shaped matcher is still the flop exception. Async-read distributed RAM has precedent at base (`KL_aecp_notify` `rows_r`) |
| R459-1-S2 (SUGGESTION): commit a lockstep bench | **Superseded by my F1 (MINOR)** | I hold it at MINOR on direct probe evidence (8 faults survive every committed suite, 3 of them in the shipping 1x1 arm) and on the #232 precedent |

## Lens results

- **[R458] PASS RTL.**
  - Artifacts:
    - `hdl/srp/KL_srp_top.sv:944-984`;
    - `hdl/srp/KL_srp_talker_fsm.sv:352-372,495-537,540-618`;
    - `hdl/srp/KL_srp_listener_fsm.sv:531-559,620-659`;
    - `hdl/srp/KL_srp_admission.sv:100-260`.
  - **Writers and readers.** Each RAM copy has exactly the flop record's writer and condition:
    - the talker: `rst_n && gate_acc_w && gate_open_i`, matching `:587-592`;
    - the listener: `rst_n && ctl_acc_w && ctl_settle_i`, matching `:622-626`;
    - the slopes: every non-reset cycle at `cidx_q2_r`, as at base.
    
    Each copy is read only under the valid bit written in the same edge (`:615`, `:655`, `fit_w` / `refuse_w` / `pend_w`), and neither the bit nor the record is cleared outside reset. So the missing reset is unobservable.
  - **FIFO.** Same pointers, guard and enables. The registered read of an asynchronous memory read gives pre-edge data in simulation and in distributed RAM alike.
  - **Indices.** Out-of-range indices cannot reach the FSMs (`KL_srp_top.sv:847-880`).
  - **Resources.** Distributed RAM everywhere, no new block RAM, no flip-flop spill. Shown by my mapping check and by the published reports.
- **[R458] PASS Robustness.**
  - **Reset during activity.** 884 mid-run resets per shape in the module lockstep, plus the committed bench's per-group resets at top level, with unreset memories carried across them.
  - **Unreset memories** were randomised differently in each copy.
  - **Minimum and maximum shapes:** N = 1..9.
  - **Invalid ordering:** random re-declarations and teardowns.
  - **Back-pressure:** `ev_ready`.
  - **Configuration-dependent arms:** N <= 2 and N >= 3 are both equal to base.
  - **FIFO boundaries:** pushes to empty at the read pointer and same-cycle push/pop were reached; full is covered by construction (S1).
- **[R458] PASS Conformance.**
  - **Acceptance criterion 1:** the SRP suites pass at both shapes they run, and at 1x1 through the parent consumer set (a manager duty).
  - **Criterion 2:** a material reduction, re-derived from the published hierarchical reports.
  - **Criterion 3:** per-stream sizing is bound from `N_STREAM_OUT_P`/`N_STREAM_IN_P` (`protocol_processor_top.sv:2484-2485`), so a 1x1 binding of 2 elaborates no inactive slot.
  - **Criterion 4:** route WNS +0.354 ns at the declared 50 MHz, per the assignment.
  - **Criterion 5** ("documented in #229") is outside the lane, as recorded in the STOP.
  - **Clause 35 behaviour** is unchanged, since outputs are cycle-identical. Ruling (b) is honoured.
- **[R458] UNCLEAN Tests:** F1 and F3.
- **[R458] UNCLEAN Docs:** F3.
  - **10 section 5.1** (`docs/architecture/10_srp_engine.md:194-248`) matches the RTL and the published reports.
  - **The RTL banners** are updated in both FSMs.
  - **No stale storage description** remains in 10 sections 4, 5 and 11.
  - **Residue:** R459-1-R1 and R2.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #230 acceptance, 5974045353, 5977826098, 5977836860; published Vivado runs at milan-fpga `06fe795b` (re-derived); lockstep receipts; `protocol_processor_top.sv:2484-2485` | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| RTL | CLEAN | `hdl/srp/KL_srp_top.sv:944-984`, `KL_srp_talker_fsm.sv:352-618`, `KL_srp_listener_fsm.sv:531-659`, `KL_srp_admission.sv:100-260`; lint at N = 1, 2, 3, 9; both lockstep benches; my synthesis mapping check | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| Robustness | CLEAN | module lockstep at N = 1..9 with resets and randomised memories; top lockstep 4 seeds; FIFO boundary counters; index guards `KL_srp_top.sv:847-880` | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| Tests | UNCLEAN (F1, F3) | `tb/srp_top`, `tb/srp_stream_fsms`, `tb/srp_admission` (all shapes); `srp_top` and `srp_admission` campaigns at base and head; 17 probes; HANDOFF section 4; PR body Validation (09:06 edit) | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| Docs | UNCLEAN (F3) | `docs/architecture/10_srp_engine.md:147-260,736-760`; `docs/guides/hdl-engineer.md:72-88`; RTL banners and comments in the four files; PR body (09:06 edit); HANDOFF | R458-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |

## Real limits

- **Vivado runs.** My Vivado run is a standalone mapping check only. Product figures were re-derived from the published reports, not re-run. The flip-flop census file is unpublished (corroborated; see F2).
- **Not run, by assignment:** the full processor bank (`run_suites.sh`), `make check`, `gen_matrix --check`, the Yosys gate, and the parent consumer set or builder. The `tb/pp_top`, maap and adp campaigns were not run either. Their SRP inputs are cycle-identical by both lockstep benches. Hosted `docs-gates` and `portability` succeeded at this head.
- **The executor's lockstep bench** (56 internal compares, its MRPDU generator) was not inspected: it is not public (F1). My benches are independent reconstructions, and they are simulation, not formal equivalence.
- **Out of scope.** Physical calibration was not run. Field or hardware behaviour is not proven by any of the above.

## Pending manager duties

- **Hosted acceptance** at the exact head: `suites` was in progress at my last read.
- **Bank evidence.** The source static/builder and native bank receipts the brief cites were not visible on #230, PR #154 or the evidence branch during the round; publish them.
- **The candidate merge build** on live dev `241f91845230ae410506dffb16b71937127fd175`, with the consumer set of 17. The executor's record is at dev `5fabb46e`. Gate 16's two T30 checks belong to #643 / PR #648.
- **The residue checklist:** R459-1-R1 and R2 (exact fixes above).
- **Filing.** File O1 as a new issue if accepted.

## Restoration

I made no edit to the clone. Every probe ran on copies under the packet's scratch. After the round:
- the clone's HEAD is the exact head;
- `git status --ignored` is empty;
- the index tree equals the HEAD tree;
- every work-tree blob hashes to its HEAD blob;
- no file carries an assume-unchanged or skip-worktree flag;
- the repository has no submodule gitlinks (`receipts/restore_check.txt`).

R458-1 FINISHED

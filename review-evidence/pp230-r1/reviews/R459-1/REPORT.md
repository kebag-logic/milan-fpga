[R459] NEGATIVE - exact head 65324390d1b83c4587f299d06597f7a571d7fa61

# R459-1: external independent review of milan-fpga #230 / processor PR #154

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #154 (`pp230-srp-area` -> `main`).
- Exact head `65324390d1b83c4587f299d06597f7a571d7fa61`, tree `2fb3aabcf7eecc4589dcf19f637e99a57431772a`.
  Base `c4cb84ff8cecad19bedaa85dde594a8ed68012f6`. Two commits: `25847d0` (RTL) and `6532439` (docs).
- Review role: external reviewer, cleared context, isolated detached clone. Round R459-1.
- Verdict: **NEGATIVE**, on two MINOR evidence and claim findings only. The RTL is behaviour-identical to base, cycle for
  cycle. My own lockstep bench, planted controls, full-boundary probe and module-level synthesis independently confirm
  this, and I found no RTL, robustness or conformance defect in the code. No source change is required. The two MINORs
  close with evidence publication (F1) and one PR-body sentence (F2).

## 1. What was reconstructed (in order)

1. Repository guidance. There is no `AGENTS.md` or `CONTRIBUTING.md` at this head. I used `README.md` and
   `docs/README.md` (conventions, single-source rules, `make check`) and `docs/guides/hdl-engineer.md` §3 (the storage
   rule).
2. Issue kebag-logic/milan-fpga#230: body (scope, acceptance criteria) and every comment.
   - The scope addition of lever 2 (5967853024).
   - The lane assignment (5974045353): behaviour identical, lockstep bench with planted controls, 100 MHz criterion
     judged at 50 MHz.
   - The author's STOP (5977826098).
   - The manager's ruling (b) (5977836860): the parallel per-stream evaluation stays; option (a) is recorded for #640.
3. PR #154: body, comments, reviews. Its only comments are the two review-start notices; there are 0 reviews and 0
   review comments.
4. Interfaces and authorities. `KL_srp_top` ports and parameters, the processor top's binding
   (`hdl/top/protocol_processor_top.sv:2484-2495`), and the parent's shape derivation at dev `241f9184`
   (`hdl/milan/milan_datapath.sv:1619-1642`, `ACMP_SRC_C` / `ACMP_SINKS_C`: streams plus CRF).
5. `git diff c4cb84ff..65324390` (5 files, +168/-43) and history (two one-line commits on `main`).
6. Public evidence: milan-fpga `8dca0983` `review-evidence/pp230-r1`. Its `MANIFEST.json` lists four files: HANDOFF.md,
   PR-BODY.md, and two parent patches. The digests match the manifest's published hashes, and PR-BODY.md equals the
   live PR body apart from a trailing newline. There are no manager evidence comments on the issue or PR beyond the
   review-start notices.
7. Hosted checks at the exact head, inspected read-only:
   - docs-gates: success (push and pull_request).
   - portability: success (push and pull_request).
   - suites: in progress on both at my last read, so not an executed result.

Prior public review findings on PR #154: **none exist** at this head (0 reviews, 0 review comments, no reviewer finding
on the issue). Nothing is resolved or retained. I read no other reviewer's report.

## 2. Findings

### R459-1-F1 (MINOR): the area acceptance figures rest on unpublished receipts

- **Lenses:** Conformance, Docs.
- **Artifact:**
  - The published evidence (milan-fpga `8dca0983` `review-evidence/pp230-r1/MANIFEST.json`) holds no Vivado report or
    log.
  - The PR body (line 128) says: "Raw Vivado reports, logs, the lockstep bench and its controls stay in scratch, with
    their digests in HANDOFF".
  - HANDOFF §5.6 and §10 give only SHA-256 prefixes of logs held in lane scratch.
  - The committed figures that depend on them: `docs/architecture/10_srp_engine.md:234-248` (the marginal-cost table
    and the "about 200 LUTs and 240 flip-flops" sentence) and the PR body's Vivado table.
- **Authority:**
  - Issue #230 acceptance: "Before-and-after hierarchical Vivado reports show a material reduction against the same
    baseline" and "Timing at 100 MHz does not regress below zero WNS" (judged at 50 MHz per the assignment).
  - The review brief requires re-deriving the figures from the published reports.
- **Evidence:**
  - These figures cannot be re-derived from any public artifact:
    - route 51,434 -> 51,005 LUT, 59,691 -> 57,262 FF, WNS +0.079 -> +0.354 ns;
    - `KL_pp_shadow` standalone 1x1 and 8x8;
    - the `u_srp` sub-block table;
    - the per-context cost (592 -> 475 LUT, 679 -> 538 FF).
  - I verified that these numbers are arithmetically consistent with one another (§4.5).
  - My own module-level synthesis reproduces the author's module-level variant table (HANDOFF §4.3) to the unit
    (§4.5). That corroborates the method, but it does not cover the integrated route, `KL_pp_shadow` standalone, or
    route timing.
- **Impact:** two acceptance criteria (the material reduction on the recipe's endpoints, and route WNS at least 0) and
  one committed doc table are attested only by the author.
- **Required outcome:** publish the eight run receipts of HANDOFF §5.6 in the manager's public evidence for this issue,
  for base and head. Each run needs:
  - the log whose SHA-256 prefix §5.6 lists;
  - the hierarchical utilization report;
  - the route timing summary;
  - the RAM final mapping report.

  No source change is needed.
- **Verification:** the published log digests match §5.6. A reviewer re-derives HANDOFF §5.2, §5.3 and §5.4, the PR-body
  Vivado table, and `10_srp_engine.md:234-248` from the reports.

### R459-1-F2 (MINOR): the PR body overstates the planted-control coverage

- **Lenses:** Tests, Docs.
- **Artifact:** PR #154 body, line 114: "Sixteen planted controls were each caught at every shape where the edited code
  is elaborated."
- **Evidence:** the author's own control table (HANDOFF §4.2) shows 0 mismatching cycles at 1/1 for
  `tf-head-at-write-pointer` and `tf-listener-push-dropped`.
  - Both edit `KL_srp_top`'s FIFO path, which is elaborated at every shape.
  - HANDOFF itself explains these zeros as "the situation the edit needs ... did not arise in those six runs".
  - Three more 1/1 zeros are edits equivalent at one source or sink: `slope-stored-at-stage-2-index`,
    `slope-store-source-0-only` and `wsid-flops-of-control-sink`.
  - The issue comment ("Sixteen planted controls were each caught") and HANDOFF ("each at three or four shapes") are
    accurate; only the PR body overclaims.
- **Impact:** the public description of the equivalence evidence claims coverage at 1/1 that the author's bench did not
  have for two FIFO controls. My own bench does catch FIFO edits at 1x1 (§4.3: 29,825 / 48,513 / 19 mismatching
  cycles), so the underlying coverage holds and only the claim is wrong.
- **Required outcome:** amend line 114 to match HANDOFF §4.2. Suggested text: "Sixteen planted controls were each caught
  at three or four of the four shapes. Every zero is an arm not elaborated, an edit equivalent at one source or sink,
  or, for two FIFO controls at 1/1, a situation the runs did not produce (HANDOFF §4.2)."
- **Verification:** the PR-body text agrees with HANDOFF §4.2.

### R459-1-R1 (RESIDUE): "10 section 5.1" is ambiguous

- **Lenses:** Docs.
- **Artifact:** PR #154 body lines 23, 62 and 71 ("10 section 5.1"). The commit subject of `6532439` says the same.
- **Problem:** `docs/README.md` §1 warns that "10 Resource and effort" is a different document from
  `architecture/10_srp_engine.md`.
- **Exact fix:** in the PR body, write "`docs/architecture/10_srp_engine.md` §5.1" at lines 23, 62 and 71. The commit
  subject is left as is; rewriting history for this is not proportionate.

### R459-1-R2 (RESIDUE): the validation header says "all rc 0"

- **Lenses:** Docs.
- **Artifact:** PR #154 body, line 106: "## Validation (all rc 0, no pipes)". The same section states that parent gate 16
  exits 2.
- **Exact fix:** "## Validation (all rc 0 except parent gate 16, recorded against #643; no pipes)". This matches the
  issue comment's "all rc 0, no pipes, except gate 16 below".

### R459-1-S1 (SUGGESTION): name the new memories in the storage-rule exceptions

- **Artifact:** `docs/guides/hdl-engineer.md:72-88` (§3.1).
- **Problem:** §3.1 says per-index records are sync-read RAMs with one cycle of read latency, and lists the SRP
  stream-FSM arrays as flops. The new walk copies (`wtsp_r`, `g_wid_ram.wid_r`, `g_wsid_ram.wsid_r`) and the admission
  `slope_q_r` are distributed RAMs with an asynchronous read.
- **Why only a suggestion:** async-read distributed RAM already exists at base (`KL_aecp_notify.sv:337` `rows_r`), and
  "flops" still holds for the CAM-shaped matcher, so this is not a defect of this PR.
- **Suggestion:** name these memories in §3.1's exception paragraph.

### R459-1-S2 (SUGGESTION): commit a lockstep bench

- Behaviour-identical area work is recurring (#232, #230). Committing a lockstep bench like the one under `scripts/`
  here (base modules renamed, a checker bound into `KL_srp_top`) would let the next lane and its reviewers rerun the
  equivalence argument instead of re-building it.

## 3. Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Issue #230 acceptance and ruling (b); "behaviour identical" against base, by my lockstep (§4.3); no port, parameter or register change (`gen_lockstep.py` asserts identical port and parameter lists); the inactive-slot check (§4.1); the area criteria (F1) | R459-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| RTL | CLEAN | The full diff of `KL_srp_top.sv:947-984`, `KL_srp_talker_fsm.sv:352-372,495-537,540-596`, `KL_srp_listener_fsm.sv:534-560,621-635`, and `KL_srp_admission.sv:106-169,193-264`; single-writer and valid-gating proofs; X-safety; index ranges; module-level Vivado mapping; Yosys inference | R459-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| Robustness | CLEAN | Mid-run resets with unreset memories randomised differently in the two models; FIFO full and empty boundaries (stall probe); same-entry write and read; out-of-range indices; noisy and truncated MRPDUs; spurious expiries; 10 shapes including both sides of the 2-vs-3 threshold and mixed arms (2x9, 9x2) | R459-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| Tests | UNCLEAN (F2) | Author bench claims (HANDOFF §4) against my independent bench; 16 controls plus 3 full-boundary controls; the srp_top and srp_admission campaigns; SRP suites; lint; `make check`; hosted check runs | R459-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |
| Docs | UNCLEAN (F1, F2; R1, R2 residue; S1) | `docs/architecture/10_srp_engine.md:194-248`; RTL banners and comments; PR body; HANDOFF; `docs/guides/hdl-engineer.md` §3.1; `docs/10_RESOURCE_AND_EFFORT.md` (no SRP storage figure made stale) | R459-1 | 65324390d1b83c4587f299d06597f7a571d7fa61 |

## 4. Lens evidence

### 4.1 Conformance

- **Ruling (b) honoured.** The diff touches only storage. Matchers, Table 10-3/10-4 transitions and published levels
  are unchanged; the shared evaluator is not attempted.
- **No port, parameter or register change.**
  - `gen_lockstep.py` parses the base and head `KL_srp_top` headers and asserts identical port and parameter lists
    (81 ports, 51 outputs).
  - Only `hdl/srp` RTL and one doc changed; `tb/` is byte-identical (`diff -rq`).
- **Behaviour identical:** §4.3.
- **The 1x1 shape has no inactive slots.**
  - The processor top binds `N_SOURCES_P`/`N_SINKS_P` from `N_STREAM_OUT_P`/`N_STREAM_IN_P`.
  - The parent at dev `241f9184` elaborates the processor at the ACMP shape (`milan_datapath.sv:1619-1642`: streams
    plus CRF), consistent with the author's 2/2 at 1x1.
  - My 2/2 synthesis maps `wtsp_r` as 2 x 68 and `slope_q_r` as 2 x 32 (2 words).
  - The parent's `KL_pp_shadow.sv:251` comment ("the shipping board elaborates this at N_STREAM_OUT_P = 1") is
    parent-side wording, outside this PR.
- **Material reduction and timing:** module level is verified exactly (§4.5); the integrated endpoints are F1.
- **"Documented in #229":** not done in this lane, by assignment. This is a pending manager duty (§6).

### 4.2 RTL

- **FIFOs** (`KL_srp_top.sv:947-984`).
  - Splitting `tf_ram_r[0:1][0:31]` into `tf_tk_ram_r` and `tf_ls_ram_r` keeps every write (same `tf_push_w[u]`, same
    `tf_wptr_r[u]`, same word) and every read (`tf_q_r[u] <= ram[u][tf_rptr_r[u]]` each cycle). Pointers, count, full
    guard (`:963-964`) and the TM_SEL/TM_POP rhythm (`:1103-1129`, `tf_pop_w` `:1256-1257`) are untouched.
  - `tf_q_r` is consumed only in TM_POP after a TM_SEL that saw `tf_cnt_r != 0`.
  - A same-entry write and read (`wptr == rptr` with a push) happens only when empty, since a push is blocked when full.
    The registered read then returns the old word, and the old word is never consumed. My equivalent-edit control
    `tf-tk-same-entry-bypass` (forward the new word) stays at 0 mismatches at every shape, including with the FIFO full.
- **Talker walk record** (`KL_srp_talker_fsm.sv:361-372,495-537`).
  - `wtsp_r` and `g_wid_ram.wid_r` are written under `gate_open_acc_w = rst_n && gate_acc_w && gate_open_i` (`:498`).
    This is exactly the base capture condition: base captured the five fields beside `sid_r`/`da_r`/`vid_r` in the
    else branch of `!rst_n` (the head's remaining capture block, `:587-592`).
  - The walk captures `wval_w` only when `rec_valid_r[wsrc_r]` is set (`:615`). Only a gate open sets it (`:589`), and
    nothing but reset clears it.
  - The gate source is range-checked upstream (`KL_srp_top.sv:848`, `:857`), and `wsrc_r < N` by construction, so no
    out-of-range address reaches the RAMs. Non-power-of-2 depths (3, 9) are safe.
  - Both models read the pre-edge value in a cycle where the gate and the walk name the same source, and the applicant
    arbitration gives the gate priority (`:471`, `:487`).
- **Listener walk stream_id** (`KL_srp_listener_fsm.sv:534-560`): written under `rst_n && ctl_acc_w && ctl_settle_i`,
  the same condition as the only `sid_r` writer (`:622-626`), and read only under `rec_valid_r` (`:655`).
- **Admission slopes** (`KL_srp_admission.sv:111-169,193-211`).
  - The stage-3 write moved to its own process with the same `rst_n` guard and index.
  - `slope_valid_r[s]` is set only at the edge that writes `slope_q_r[s]` (`:147`).
  - Every consumer of `slope_q_r[aidx_r]` (`cand_w`, `wgslope_now_w`, `acc_r`, `sum_r`) is masked by `fit_w`, which
    requires `slope_valid_r[aidx_r]`.
- **X-safety under 4-state semantics:** every unreset word reaches a register only through a mask that is 0 while the
  word is unwritten.
- **2-vs-3 threshold.** `N > 2` selects between two equivalent read paths. My controls `wid-threshold-ram-from-1` (RAM
  arm at every N) and `wid-threshold-flops-always` (flop arm at every N) are silent at 1x1, 2x2, 3x5 and 9x9. Both arms
  are therefore functionally interchangeable, and the choice is purely an area one.
- **Lint and portability.**
  - `scripts/lint_hdl.sh`: rc 0, 41/41.
  - The three changed FSM/admission modules at 1, 2, 3 and 9 contexts, plus `KL_srp_top` at 1/1, 2/2, 3/5 and 9/9:
    16/16 clean (`receipts/scoped/lint_shapes.log`).
  - sv2v plus Yosys infer exactly `wtsp_r` (always), `g_wid_ram.wid_r` (from 3), `g_wsid_ram.wsid_r` (from 3) and
    `slope_q_r` (always) as memories (`receipts/scoped/yosys_scoped.log`).

### 4.3 Robustness and equivalence: an independent lockstep, built from scratch

- **Method** (`scripts/gen_lockstep.py`).
  - Base `c4cb84ff`'s eight SRP modules are renamed `_ref`.
  - A checker holding `KL_srp_top_ref` is bound (SystemVerilog `bind`) into every head `KL_srp_top`.
  - From the edge after the first reset, it compares every clock:
    - all 51 outputs;
    - 40 internal signal groups: both FSMs' applicant and registrar states, encoder intake faces, timer-arm faces,
      VLAN face, `rec_valid_r`, walk state;
    - the walk FirstValue `wval_w`, gated by `rec_valid_r[wsrc_r]` (the RAM read path itself);
    - the admission slope at the read point, gated by `slope_valid_r`, plus the working and published grant state;
    - the FIFO push, pop, count and pointers, the TM state, and the consumed head.
  - Verilator 5.050 (identity checked: `verilator --version` and the wrapper's SHA-256 `905795b9...`), with
    `--x-initial unique --x-assign unique +verilator+rand+reset+2`, so every unreset memory starts with different random
    contents in the two models.
- **Committed suites, driven unchanged, with the checker bound in** (`scripts/lockstep_suites.sh`):
  - `tb/srp_top`: 2,200/2,200 PASS; 185,012,669 compared cycles, 0 mismatching, 454 resets.
  - `tb/pp_top`: 10,390/10,390 PASS; 30 model instances, 162,116,017 compared cycles, 0 mismatching, 706 resets.
- **Random campaign** (`scripts/ls_rand/main.cpp`, `scripts/run_campaign.sh`).
  - Scale: 120 runs x 3,000,000 cycles = 360,000,000 cycles, with 0 mismatching and 2,453 mid-run resets.
  - Shapes: 1/1, 2/2, 3/3, 3/5, 5/3, 4/4, 8/8, 9/9, 2/9 and 9/2, at the default and a compressed cadence; half the runs
    use noisy (corrupted or truncated) MRPDUs.
  - Traffic:
    - 2,411,496 MRPDUs, 1,800,532 requests, 456,699 frames;
    - 1,847,611 timer arms, 320,826 registrations;
    - 350.5 M talker and 346.3 M listener cycles comparing the RAM-read walk value, and 245.1 M gated slope reads.
- **Planted controls** (16, `scripts/make_controls.py`; mismatching cycles over 3 x 500,000 per cell):

  | control | expect | 1x1 | 2x2 | 3x5 | 9x9 |
  |---|---|---:|---:|---:|---:|
  | `tf-ls-head-reads-tk-ram` | catch | 29,825 | 79,826 | 171,924 | 222,406 |
  | `tf-tk-head-reads-next` | catch | 48,513 | 127,179 | 163,322 | 284,571 |
  | `tf-ls-write-ignores-full` | catch at full | 0 | 0 | 0 | 0 |
  | `tf-tk-write-at-rptr` | catch | 19 | 8,394 | 16,217 | 105,187 |
  | `tf-tk-same-entry-bypass` | equivalent | 0 | 0 | 0 | 0 |
  | `wtsp-written-on-close` | catch | 590,938 | 524,261 | 437,001 | 362,187 |
  | `wtsp-prio-rank-swapped` | catch | 1,457,202 | 1,427,692 | 1,290,321 | 1,360,851 |
  | `wtsp-read-at-source-0` | catch | 0 (one source) | 463,230 | 422,941 | 397,127 |
  | `wid-ram-read-neighbour` | catch | 0 (n/e) | 0 (n/e) | 1,439,285 | 1,372,666 |
  | `wid-flops-vid-of-source-0` | catch | 0 (one source) | 170,918 | 0 (n/e) | 0 (n/e) |
  | `wid-threshold-ram-from-1` | equivalent | 0 | 0 | 0 | 0 |
  | `wid-threshold-flops-always` | equivalent | 0 | 0 | 0 | 0 |
  | `wsid-ram-written-on-teardown` | catch | 0 (n/e) | 0 (n/e) | 661,857 | 639,966 |
  | `wsid-flops-read-sink-0` | catch | 0 (one sink) | 452,768 | 0 (n/e) | 0 (n/e) |
  | `slope-store-at-stage-1-index` | catch | 0 (one source) | 1,303,054 | 1,432,287 | 1,473,217 |
  | `slope-read-source-0` | catch | 0 (one source) | 955,467 | 1,234,497 | 1,470,642 |

  Every defect control is caught wherever its arm is elaborated and the edit is not equivalent by construction. The
  three equivalent edits stay silent. Natural traffic never fills a FIFO (peak 8 of 32), so the write-ignores-full
  control needs the probe below.
- **Full-boundary probe.** The same edit is made in base and head: TM_SEL issues nothing while `now_ms_i[6]`, or
  `now_ms_i[8]`, is set.
  - At 9/9 the talker FIFO reaches 32 in every run: 161 to 45,852 full cycles, and up to 184 blocked pushes per run.
  - With the longer stall the listener FIFO reaches 32 in 3 of 4 runs.
  - Plain head against base: 0 mismatching in all runs.
  - `tf-tk-write-ignores-full`: caught in 4/4 runs.
  - `tf-ls-write-ignores-full` with the longer stall: caught in exactly the 3 runs where the listener FIFO filled.
  - The same-entry bypass stays silent with the FIFO full.
- **Comparison with the author's bench** (HANDOFF §4.1-4.2).
  - Its scope (51 outputs and 56 internals, the 2/2, 9/9, 1/1, 3/5 and 8/8 shapes, resets, randomised memories, 16
    controls) is plausible and consistent with mine.
  - Its full-boundary coverage was never exercised: it reports no full-FIFO figure, and its FIFO controls cannot reach
    full. My probe closes that gap.
  - Its 1/1 FIFO-control gaps are F2.

### 4.4 Tests at head (scoped, all rc 0)

- `tb/srp_admission` 991,231, `tb/srp_stream_fsms` 1,219, `tb/srp_decoder` 190 and `tb/srp_encoder` 581 checks,
  exactly HANDOFF §7's figures. `tb/srp_top` 2,200 and `tb/pp_top` 10,390 are under the lockstep, also equal.
- `tb/srp_top/mutants.py --jobs 6`: 90 checks, 90 PASS, assertion coverage 65/65. All 73 patches pass
  `git apply --check` (the driver runs it with `check=True`).
- `tb/srp_admission/mutants.py --jobs 3`: 12/12 PASS.
- `make check`: rc 0, with 41 mermaid and 18 wavedrom blocks, 1,114 links, 115 REQ rows, 94 matrix rows with 0
  untested, and 28 parameters. This includes `gen_matrix --check`.
- Hosted at the exact head:
  - docs-gates and portability: success (executed).
  - suites: in progress (not counted).

### 4.5 Area

- **Module-level synthesis.** This is a reviewer probe that mirrors HANDOFF §4.3, not the #638 recipe
  (`scripts/srp_ooc.tcl`).
  - Setup: Vivado 2026.1, `xc7a100tfgg484-2`, out of context, `AreaOptimized_high`, 20 ns, a wrapper tying
    `req_max_interval_i` to 1.
  - It ran alone under the shared Vivado lock (10:38:51-10:58:14), with no heavy build of mine running beside it.
  - Results, LUT (LUTRAM) / FF:

    | Variant | N | `u_srp` | top glue | `u_talker` | `u_listener` | `u_admission` | F7 |
    |---|---:|---:|---:|---:|---:|---:|---:|
    | base | 2 | 4,460 (186) / 6,395 | 881 (0) / 2,785 | 636 (0) / 715 | 395 (0) / 666 | 269 (0) / 271 | 331 |
    | head | 2 | 3,856 (310) / 4,000 | 327 (64) / 560 | 604 (36) / 609 | 364 (0) / 666 | 276 (24) / 207 | 53 |
    | base | 9 | 8,249 (186) / 10,973 | 931 (0) / 3,167 | 2,144 (0) / 2,263 | 1,800 (0) / 2,612 | 782 (0) / 977 | 377 |
    | head | 9 | 6,962 (438) / 7,760 | 339 (64) / 720 | 1,697 (120) / 1,783 | 1,558 (44) / 2,612 | 761 (24) / 689 | 76 |

  - Every cell equals HANDOFF §4.3's v0 and vF rows.
- **Primitive mapping** (head, RAM final mapping report).
  - At 2/2: `tf_tk_ram_r` and `tf_ls_ram_r` are 32 x 47 RAM32M x 8 each, `wtsp_r` 2 x 68 RAM32M x 12, `slope_q_r` 2 x 32
    RAM32M x 6.
  - At 9/9: the FIFOs are 32 x 48 RAM32M x 8 each, `wtsp_r` 16 x 68 x 12, `g_wid_ram.wid_r` 16 x 124 x 21,
    `g_wsid_ram.wsid_r` 16 x 64 x 11, `slope_q_r` 16 x 32 x 6.
  - Flip-flop census at head: 0 for each moved structure. The base had 2,240 flops on `tf_ram_r` at 2/2 and 64 on
    `slope_q_r`.
  - The only block RAM at either shape is the decoder's RAMB18 (`tp_ram`).
  - So no SRP structure lands in block RAM or spills to flops, and this matches HANDOFF §3 line for line.
- **Arithmetic re-derivation of every derived figure** in the PR body, HANDOFF §1 and §5.3-5.4, and 10 §5.1, from their
  source tables. All are consistent, for example:
  - talker (1,549 - 648)/7 = 129 LUT and (1,787 - 610)/7 = 168 FF;
  - whole engine (7,313 - 3,988)/7 = 475 LUT and (7,747 - 3,979)/7 = 538 FF;
  - lever 4 at 1x1: -15 - 37 + 15 = -37 LUT and -104 + 0 - 64 = -168 FF;
  - route: -429 LUT, -2,429 FF, +0.275 ns WNS.
- The integrated route, `KL_pp_shadow` standalone and route timing are not re-derivable from public material (F1).

### 4.6 Docs

- `10_srp_engine.md` §5.1 storage table checks against the RTL:
  - FIFO words of 41 + `SLOT_AW_P` bits, since `TFW_C = 1 + SLOT_AW_P + 8 + 32`;
  - 68-bit `wtsp_r` and 124-bit `wid_r`;
  - 104-bit registration data;
  - the rows for the threshold and the reset-free reasoning.
- `make check` passes, and the single-source rules are respected: no timing or parameter value is restated.
- The RTL banners (talker `:56-67`, listener `:54-61`) and the comments state the matcher/walk split and the no-reset
  reasoning correctly.
- `docs/10_RESOURCE_AND_EFFORT.md` carries no SRP storage figure that this change makes stale.
- F1, F2, R1, R2 and S1 above.

## 5. Real limits

- **No published Vivado report** (F1). I could not re-derive the integrated route, `KL_pp_shadow` standalone 1x1 and
  8x8, the `u_srp` route breakdown, or route WNS/WHS. My synthesis is module-level only, and I did not run the #638
  recipe (a parent bank, not allowed here).
- **The author's lockstep bench and controls are unpublished.** I did not inspect them; my bench is independent.
- **Not run by me** (full banks not allowed here):
  - `run_suites.sh` (only the six SRP-relevant suites);
  - `syn/yosys/run.sh` (the hosted portability job executed and passed at this head);
  - the pp_top campaigns (maap, adp, ctr, notify, acmp, aecp, dispatch, d3, gsi, name_wr);
  - the parent consumer set and builder gate.

  Since `KL_srp_top` is cycle-identical to base on all outputs (§4.3), these cannot differ through this change, but
  they were not executed here.
- **Lockstep scope.** It is simulation. It is not a formal equivalence proof, and the FIFO full state is reached only
  through an identical stall edit in both models (natural traffic peaks at 8 of 32).
- **Hosted `suites` job** was in progress at my last read; the manager owns hosted acceptance.
- **No hardware or physical calibration** was run. Field skips are not hardware proof.

## 6. Pending manager duties

- **F1:** publish the eight Vivado run receipts (HANDOFF §5.6 digests) as public evidence.
- **F2, R1 and R2:** amend the PR body (no new head needed).
- **The final current-dev candidate** at the merge turn: source base `c4cb84ff` onto live dev `241f9184` with the
  c8-bbf704ec and p2-p1 patches. It includes the parent consumer set of 17; gate 16's two T30 INTERNAL-law checks
  belong to #643 / PR #648.
- **Hosted acceptance:** the `suites` job at the exact head.
- **#230's "documented in #229"** item, and closing #230 manually at the processor merge, per ruling 5977836860.

## 7. Receipts

`MANIFEST.sha256` lists every published file, with paths relative to this packet. Local paths, user and host names are
redacted as `<PACKET>`, `<CLONE>`, `<HOME>`, `<VERILATOR_IMAGE>`, `<VIVADO_ROOT>`, `<USER>` and `<HOST>`.

- **Scripts:**
  - `scripts/gen_lockstep.py`: the checker generator.
  - `scripts/lockstep_suites.sh`: the committed suites under lockstep.
  - `scripts/ls_rand/{main.cpp,build.sh}` and `scripts/run_campaign.sh`: the random campaign, controls and stall
    probes.
  - `scripts/make_controls.py`.
  - `scripts/summarize.py`, which rebuilds `receipts/SUMMARY.md`.
  - `scripts/srp_ooc.tcl`, `scripts/srp_ooc.xdc` and `scripts/srp_area_wrap.sv`.
- **Generated checker:** `receipts/generated/`.
- **Raw logs and rc files:**
  - `receipts/lockstep/{srp_top,pp_top,random,controls,stall}/`;
  - `receipts/scoped/`: lint, shape lint, Yosys, suites, campaigns, `make check`;
  - `receipts/vivado_ooc/`: per-run utilization, hierarchical utilization, RAM report, census, and the Vivado log.
- **Public inputs as fetched:** `receipts/issue230*.json`, `receipts/pr154*.json`, `receipts/check_runs.json`,
  `receipts/commit_status.json`, and `receipts/evidence/` (the four published evidence files and their manifest).
- **Clone integrity after the review:**
  - `git status` is clean;
  - HEAD is `65324390d1b83c4587f299d06597f7a571d7fa61` and its tree is `2fb3aabcf7eecc4589dcf19f637e99a57431772a`;
  - the index and work tree equal HEAD;
  - this repository has no gitlinks;
  - no file in the clone was edited. All probes ran on `git archive` copies under the packet's scratch directory.

R459-1 FINISHED

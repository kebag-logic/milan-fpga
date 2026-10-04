[R459] POSITIVE - exact head b59e99cb928939f5c4089964dea8f4628d06ede7

# R459-3: external independent review of milan-fpga #230 / processor PR #154 (round 2b)

- **Repository and PR:** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #154 (`pp230-srp-area` -> `main`).
- **Exact head and base:** head `b59e99cb928939f5c4089964dea8f4628d06ede7`, tree `06d80d967d2c7baa550a66dd2572a787e8adead6`. Source
  base `c4cb84ff8cecad19bedaa85dde594a8ed68012f6`.
- **Role:** external reviewer, cleared context, isolated detached clone. The whole range
  `c4cb84ff..b59e99cb` was reviewed from scratch, with the round-2b delta `9160f7d7..b59e99cb` checked against the
  prior findings.
- **Verdict: POSITIVE.** All five lenses are clean, and no BLOCKER, MAJOR, MINOR or RESIDUE is open.
  - Every prior MINOR and RESIDUE on this PR is resolved at this head (section 2).
  - Three SUGGESTIONS remain (section 3). None affects the verdict.

## 1. Reconstruction (in order)

1. **Repository guidance.** The processor repository has no `AGENTS.md` or `CONTRIBUTING.md` at this head.
   - I used `README.md`, `docs/README.md` (single-source rules, editing workflow) and `docs/guides/hdl-engineer.md` §3.
2. **Issue kebag-logic/milan-fpga#230.** I read the body and all 7 comments (`receipts/issue230*.json`).
   - **Frozen acceptance:**
     1. SRP tests pass for 1x1 and 8x8;
     2. before/after hierarchical Vivado reports show a material reduction against the same baseline;
     3. 1x1 has no logic for seven inactive slots;
     4. no WNS regression below zero at 100 MHz;
     5. scaling documented in #229.
   - **Scope decisions:**
     - scope addition 5967853024 (timer-arm FIFOs);
     - lane 5974045353 (behaviour identical, no port, parameter or register change, lockstep proof; 100 MHz judged at
       the declared 50 MHz);
     - ruling (b) 5977836860 (the parallel per-stream evaluation is final, (a) goes to #640, #230 closes manually at
       the processor merge);
     - round-2 assignment 5978448959;
     - REVIEW READY 5979936594.
3. **PR #154.** I read the body at the exact head, which is byte-identical to the evidence branch's
   `author-r2b/PR-BODY.md`, and all 14 comments.
   - The manager's comments: 5978368336, 5980393974 (round 2b), and the review starts.
   - The PR has 0 reviews and 0 review comments.
   - I read the prior reviews (R459-1/2, R458-1/2) only after my own pass. My provisional verdict was written first:
     `receipts/OWN-PASS-BEFORE-PRIOR-FINDINGS.md`.
4. **Interfaces and authorities.** I read these against the diff:
   - `KL_srp_top` (service FSM, gate/ctl faces, timer-arm FIFOs);
   - `KL_srp_talker_fsm`, `KL_srp_listener_fsm`, `KL_srp_admission`;
   - the processor top's `N_STREAM_*` binding;
   - 802.1Q §35.2.2.8 FirstValue layout (as transcribed in the harness and in `docs/architecture/10_srp_engine.md`
     F10.7/F10.8).
5. **Diff and history.**
   - `git diff c4cb84ff..b59e99cb`: 86 files, 53 commits (9 merges, most of them brought in from `main`). The lane's
     first-parent line is 12 commits: two merges of `main` (`4994ada`, `9160f7d7`) and ten lane or manager commits.
   - The PR's net delta against current `main` `c050d971` is 48 files: 4 SRP HDL files, 2 docs, and SRP tests and
     controls.
   - `hdl/srp` is byte-identical to `25847d07`, the round-1 RTL commit (`git diff 25847d07 b59e99cb -- hdl/srp`
     is empty).
   - The round-2b delta is two prose edits: `docs/guides/hdl-engineer.md:88-90` and `tb/srp_top/README.md:621-625`.
6. **Public executable evidence.**
   - milan-fpga `8dca0983` `review-evidence/pp230-r1` holds the round-1 author packet only.
   - The evidence branch `pp230-review-evidence` at `fd1ef4bf` holds:
     - `author-r1/vivado/` (`06fe795b`, the eight Vivado runs);
     - `author-r2/` (HANDOFF, PR-BODY, `lockstep-r1/` bench);
     - `author-r2b/` (HANDOFF, PR-BODY for this head).
   - Three `lockstep-r1` files differ from their own `MANIFEST.sha256` only by the archive's declared path redaction
     (`path_redacted: true` in `MANIFEST.json`).
7. **Hosted contexts at the exact head** (read-only, last read 2026-10-04 13:45 UTC, `receipts/hosted_checks_final.txt`):
   - docs-gates: success on both runs (executed).
   - portability: success on both runs (executed).
   - suites: `in_progress` on both runs. That is not an executed result.

## 2. Prior public review findings at this head

| Finding | Disposition at `b59e99cb` | Evidence |
|---|---|---|
| R459-2 F1 (MINOR, Tests and Docs): the srp_top README's coverage sentence overstates the 1/1 cell of `wsid-flops-of-control-sink` | **Resolved** | `tb/srp_top/README.md:621-625` now names the exception, with the simulator cause, and says 2/2 catches those edits. The table row (`:611` "0 (equivalent in simulation)") and the legend agree. My campaign run (section 4.4) gives that control failing checks only at 2/2 |
| R458-2 F1 (MINOR, Tests and Docs): the same 1/1 zero, misattributed in three places | **Resolved** | README as above. The PR body's round-1 table row reads "0 (equivalent in simulation: the out-of-range control index reads sink 0 in Verilator)". The evidence `author-r2b/HANDOFF.md:146` matches the body, and `:155-156` lists the case beside the equivalent ones |
| R459-2 R1 (RESIDUE): the body's "head" wording | **Resolved** | The body's head line names `b59e99cb`, `9160f7d7` and `1199255`. The suites line reads "at `7365022` (the lane's head before the manager's merge; `1199255` adds only a README)", and the campaigns line reads "(their inputs equal `1199255`'s)". `git diff 7365022 1199255` touches only `tb/srp_top/README.md`, so the wording is true |
| R458-2 R2-R1 (RESIDUE): body line 9 | **Resolved** | As R459-2 R1 |
| R458-2 R2-R2 (RESIDUE): `hdl-engineer.md` attributed `slope_q_r` to the stream-FSM arrays' walks | **Resolved** | `docs/guides/hdl-engineer.md:88-89` reads "the SRP walks ... (the stream FSMs' tick walks and the admission walk)" |
| R458-2 S1 (SUGGESTION): randomise unreset memory in the FIFO arms | **Not taken; retained as a SUGGESTION** (S1 below) | `tb/srp_top/Makefile` storage build: no `--x-initial unique`, no `+verilator+rand+reset+2` |
| R458-2 S2 (SUGGESTION): name the 1/1 limit next to WK6 | **Not taken; retained as a SUGGESTION** (S2 below) | `tb/srp_stream_fsms/README.md` has no mention of the out-of-range alias |
| R458-1 O1 (observation, outside the diff): `tb/srp_top` fails 4 checks with unreset state randomised, at base and head alike | **Retained as an observation**, not this PR's | Not re-measured. It is outside the diff |
| R458-1 F1, F2, F3; R459-1 F1, F2 (MINOR) | **Resolved** (round 2), and still resolved | No regression in `9160f7d7..b59e99cb` (docs only). I re-derived the area figures myself from `06fe795b` (section 4.1). The committed WK/TF arms and the 33 storage controls pass and kill at this head (section 4.4) |
| R459-1 R1, R2 (RESIDUE); R459-1 S1, S2; R458-1 S1 | **Resolved or taken** (round 2), and still so | The PR body names `docs/architecture/10_srp_engine.md` section 5.1 in full, and the Validation header carries the gate-16 exception. `hdl-engineer.md:88-93` names the memories. The FIFO full guard is exercised by TF4/TF5. The bench is published as `lockstep-r1/` |

## 3. Findings

There is no BLOCKER, MAJOR, MINOR or RESIDUE. The suggestions below do not affect the verdict.

### R459-3-S1 (SUGGESTION, Tests): randomise unreset memory in the timer-arm FIFO arms (carries R458-2 S1)

- **Artifact:** `tb/srp_top/Makefile` (`SFLAGS`, `storage` target).
- **Evidence.** The walk arms build with `--x-initial unique` and run with `+verilator+rand+reset+2`. The store arms do
  neither, so `tf_tk_ram_r` and `tf_ls_ram_r` start at zero.
- **Impact.** None today. Every committed FIFO control is killed (section 4.4), as are my three FIFO probes.
- **Outcome (optional):** build the store arms the way the walk arms are built.
- **Verification:** `make RUN_ARGS=storage` stays 15/15 per shape.

### R459-3-S2 (SUGGESTION, Docs): name the 1/1 out-of-range alias where WK6 is defined (carries R458-2 S2)

- **Artifact:** `tb/srp_stream_fsms/README.md`, the WK table.
- **Outcome (optional):** one sentence pointing at the srp_top README's note.

### R459-3-S3 (SUGGESTION, Docs): rewrap `docs/guides/hdl-engineer.md:90`

- **Evidence.** The round-2b edit left line 90 at 125 characters. The paragraph around it wraps at about 85.
- **Impact.** Formatting only. `make lint` and `links` pass.

## 4. Lens evidence

### 4.1 Conformance: CLEAN

- **Acceptance 1 (SRP tests at 1x1 and 8x8).** The 1x1 product binds `N_STREAM_IN_P = N_STREAM_OUT_P = 2` (stream plus
  CRF), and 8x8 binds 9 (published `ooc-*/baseline_chparam.txt`).
  - At the head, the default `make` runs the new arms at sources/sinks 1/1, 2/2, 3/5 and 9/9, then the suites. All
    are rc 0:
    - `srp_top`: TF 15/15 at each shape, then 2,200/2,200;
    - `srp_stream_fsms`: WK 23/30/43/79, then 1,219/1,219;
    - `srp_admission`: 1,138 / 12,615 / 41,012 / 201,073 / 991,231 at N = 1/2/3/5/8.
  - Receipts: `receipts/suites/`.
- **Acceptance 2 (material reduction, same baseline).** I re-derived every figure from the published reports
  (`06fe795b`), using `scripts/marginal.py` and `receipts/marginal.txt`.
  - **`u_srp` LUT / FF:**

    | Run | Base | Head |
    |---|---|---|
    | 1x1 | 4,558 / 6,438 | 3,988 / 3,979 |
    | 8x8 | 8,705 / 11,192 | 7,313 / 7,747 |
    | Route | 4,340 (180 LUTRAM) / 6,263 | 3,711 (298) / 3,839 |

  - **Whole design, route:** LUT 51,434 -> 51,005, FF 59,691 -> 57,262, slice 15,847 -> 15,837.
  - **Whole design, OOC:**
    - 1x1: 24,930 / 25,465 -> 24,258 / 23,130;
    - 8x8: 32,584 / 34,211 -> 31,109 / 30,648.
  - **F7 muxes at 1x1:** 639 -> 343 (the body's "296 fewer").
  - **Top glue at 1x1:** 907 / 2,836 -> 354 / 545.
  - **Talker, listener and admission together:** 1x1 -37 LUT / -168 FF, 8x8 -791 / -762.
  - Every figure equals the PR body and `10_srp_engine.md` §5.1.
  - Base and head share one recipe and baseline (dev `5fabb46e` + c8 + p2-p1, processor `c4cb84ff` against this
    RTL). `hdl/srp` has not changed since the measured `25847d07`.
- **Acceptance 3 (no logic for inactive slots at 1x1).** Every per-stream structure is sized by `N_SOURCES_P` or
  `N_SINKS_P`, which the top binds from `N_STREAM_OUT_P` and `N_STREAM_IN_P` (= 2 at 1x1). The new memories are sized
  `[0:N-1]`, and the RAM copies are generate-gated (`N > 2`).
- **Acceptance 4 (timing).** Judged at the declared 50 MHz, as the lane ruled. The routed WNS/WHS go from
  +0.079/+0.014 to +0.354/+0.036 ns (`route-1x1/baseline_timing.rpt`, "Physopt postRoute"), with 0 nets with routing
  errors on both sides.
- **Acceptance 5 ("documented in #229").** Not done by the lane, which posts only on #230. The scaling is recorded in
  `docs/architecture/10_srp_engine.md:237-251` and on #230. This is a pending manager duty (section 7). The PR
  correctly says "Relates to", not "Closes".
- **Lane rules.**
  - No port, parameter or register change: the HDL diff touches only internal declarations and processes.
  - Ruling (b) is honoured: the matcher, the transitions and the published levels stay parallel.
  - Behaviour identity is shown in section 4.2.

### 4.2 RTL: CLEAN

- **Talker** (`hdl/srp/KL_srp_talker_fsm.sv:361-372, 495-537, 586-596, 615-619`).
  - `wtsp_r` and `g_wid_ram.wid_r` are written under `rst_n && gate_acc_w && gate_open_i`. That is exactly the old
    flop write condition (the reset-else branch, then `gate_acc_w`, then `gate_open_i`), at the same index
    `gate_src_i`.
  - They are read asynchronously at `wsrc_r`, as the flops were, so write-to-read timing is unchanged.
  - The FirstValue slices map {mfs 67:52, mif 51:36, prio 35:33, rank 32, lat 31:0} and {sid 123:60, DA 59:12,
    VLAN 11:0}. These match the write concatenations and widths (68 and 124 bits).
  - `wval_w` has one consumer, `push_val_r`, written only when `rec_valid_r[wsrc_r]` is set. Only a gate open sets
    that bit, and the open writes every word; a close never clears it. So the dropped reset is unobservable.
  - The matcher's `sid_r`, `da_r` and `vid_r` keep their reset (the VLAN logic also reads `vid_r`).
- **Listener** (`KL_srp_listener_fsm.sv:540-559, 622-628, 655-658`). `wsid_r` is written under
  `rst_n && ctl_acc_w && ctl_settle_i` at `ctl_sink_i`. That is the only write of `sid_r`, so the two copies track
  each other. The read is likewise gated by `rec_valid_r`.
- **Admission** (`KL_srp_admission.sv:115, 162-169, 195-210`). The slope store keeps its unconditional per-cycle
  write at `cidx_q2_r` (as before, minus the reset). Every use of `slope_q_r[aidx_r]` is masked by `slope_valid_r`
  (`fit_w`, `refuse_w`, `wgslope_now_w`, `sum_r`). `cand_w` alone has no mask, but it is only consumed through
  `fit_w`.
- **Top** (`KL_srp_top.sv:947-984`). The two one-dimensional memories have the same push enables, pointers and
  registered read as the old `tf_ram_r[0:1]`. The old array was unreset too, so behaviour is identical.
- **Index ranges.** The service FSM raises S_GATE/S_CTL only for `req_index_i < N_SOURCES_P` / `< N_SINKS_P`
  (`KL_srp_top.sv:847-880`). So no out-of-range write reaches a new memory inside the engine, and walk and slope
  indices stay in `0..N-1`.
- **Lint.** Lint with the repository's flags (whole `hdl/` visible) is clean for the four changed modules at the
  default shape and at N = 1, 2, 3, 5, 9: 24/24, rc 0 (`receipts/lint_focus.log`).

### 4.3 Robustness: CLEAN

- **Independent lockstep replay** (`receipts/lockstep/`). I ran the published round-1 bench files unmodified, with
  base `c4cb84ff`'s `KL_srp_top` beside the head's. I chose **seven shapes the round-1 campaign did not run** and
  **my own seeds**:
  - 4/4, 5/3, 2/7 (talker flop arm with listener RAM arm), 7/2, 1/9, 16/16, and 2/2 at the default cadences;
  - 4 runs x 400,000 cycles each, with 120 mid-run resets and unreset memories randomised differently in each model.
  - Result: **0 top and 0 internal mismatching cycles** in all 28 runs.
  - A planted control (talker VLAN slice off by one bit) mismatches in every run at 4/4 and 2/7 (417-1,941 top
    cycles per run), so the replay is not vacuous.
- **Reset.** The new memories are unreset by design. Synchronous reset clears every valid bit that guards them (WK5
  covers this; the replay applied 120 resets).
  - Probe `wtsp-write-during-reset` drops the `rst_n` term from the write. It survives, as it must: it is
    equivalent by construction.
- **Configuration corners.**
  - The N <= 2 flop arm and the N >= 3 RAM arm are both elaborated by the committed arms and by the replay (1/9, 2/7
    and 7/2 mix the arms within one engine).
  - Non-power-of-two depths (3, 5, 7, 9) are exercised.
- **The test-only force** in `tb/srp_store_wrap.sv:164-169` holds only `tm_st_r`, and it is documented
  (`:20-27`, README).

### 4.4 Tests: CLEAN

- **Committed campaign** (`tb/srp_top/mutants.py --jobs 6`, unmodified, at the head):
  - rc 0, **126 checks: 126 PASS**, assertion coverage **78/78**;
  - 14 positive controls pass;
  - all 111 arms are KILLED by their named check, including the 33 #230 storage controls (TF1-TF5, WK1-WK8 and the
    admission named check).
  - Receipt: `receipts/campaign/srp_top-campaign.log`.
- **Reviewer probes** (`scripts/probes.py`, `receipts/probes/SUMMARY.txt`). These are 12 new edits, none of them in
  the committed set, each run against the committed suite target at every shape.

  | Probe | Target | Result |
  |---|---|---|
  | `tf-ls-head-read-ahead` (listener head at `rptr + 1`) | srp_top storage | CAUGHT |
  | `tf-ls-write-at-rptr` | srp_top storage | CAUGHT |
  | `tf-tk-push-dropped-when-both` | srp_top storage | CAUGHT |
  | `wtsp-mfs-mif-swapped-on-write` | srp_stream_fsms walk | CAUGHT |
  | `wid-vlan-slice-off-by-one` | srp_stream_fsms walk | CAUGHT |
  | `wid-ram-write-at-walk-source` | srp_stream_fsms walk | CAUGHT |
  | `wsid-ram-read-at-control-sink` | srp_stream_fsms walk | CAUGHT |
  | `slope-cand-reads-neighbour` | srp_admission | CAUGHT |
  | `slope-store-skips-last-source` | srp_admission | CAUGHT |
  | `wtsp-write-during-reset` | srp_stream_fsms walk | survives: equivalent by construction (4.3) |
  | `wtsp-write-ignores-ready` (write on `gate_valid_i`, not on acceptance) | srp_stream_fsms walk | survives: equivalent in the engine, because S_GATE holds the latched face until accepted, so the last write is the accept cycle's (`KL_srp_top.sv:791-793, 903-927`) |
  | `wsid-ram-write-ignores-ready` | srp_stream_fsms walk | survives: equivalent in the engine (S_CTL, as above) |

- **Expectations are independent.** `walk_main.cpp` builds each FirstValue from its own 802.1Q §35.2.2.8
  transcription (priority bits 7:5, rank bit 4) and from per-source, per-phase distinct records, never from DUT
  logic. The TF scoreboard models the FIFO contract.
- **Unreset start.** Walk arms randomise unreset memories. FIFO arms do not (S1).

### 4.5 Docs: CLEAN

- **`docs/architecture/10_srp_engine.md` §5.1 (`:194-251`).** Every number checks out against the RTL and the
  published reports:
  - word widths: TF `41 + SLOT_AW_P`; matcher 124; `wtsp_r` 68; `wsid_r` 64; listener registration data 104;
    slopes 32; encoder 285/19; VLAN 17 (`REFCNT_W_P = 5`); `cad_dl_r` 5 x 32;
  - two contexts at 1x1, nine at 8x8;
  - the marginal table: 129/168 (base 213/221), 208/278 (227/278), 69/69 (73/101), 475/538 (592/679);
  - "about 200 / 240" and "about 210 / 280".
  - The reasons given for what stays per stream match ruling (b).
- **`docs/guides/hdl-engineer.md:88-93`.** Accurate: the walk copies are asynchronous-read RAM, and the FIFO read is
  registered.
- **READMEs.** `tb/srp_top/README.md` and `tb/srp_stream_fsms/README.md` agree with my runs:
  - tallies 15 per shape, 23/30/43/79, 2,200 and 1,219;
  - the campaign table's kill pattern;
  - the 1/1 exception sentence.
- **PR body.** Byte-identical to the published `author-r2b/PR-BODY.md`. Its figures, tables and summaries agree with
  my receipts and re-derivations.
- **Documentation gates** (in the clone): `make links` (1,131 links), `matrix` (115 REQ / 17 GAP), `modmatrix`
  (94 rows, 0 untested), `params` (28), `stale` and `lint` (41 mermaid + 18 wavedrom blocks) are all rc 0
  (`receipts/docs-*.log`).
  - `wavedrom-check` was not run: no WaveDrom fence changed.

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #230 body and 7 comments (scope addition, lane, ruling (b), round 2, REVIEW READY); PR body and manager comments; `06fe795b` Vivado reports (1x1/8x8 OOC, route, timing, chparam) re-derived by `scripts/marginal.py`; `hdl/srp` identity to `25847d07` | R459-3 | b59e99cb928939f5c4089964dea8f4628d06ede7 |
| RTL | CLEAN | `KL_srp_talker_fsm.sv:356-372,495-537,586-596,615-619`; `KL_srp_listener_fsm.sv:540-559,622-628,655-658`; `KL_srp_admission.sv:106-169,195-210`; `KL_srp_top.sv:791-794,847-880,942-984`; focused lint 24/24 | R459-3 | b59e99cb928939f5c4089964dea8f4628d06ede7 |
| Robustness | CLEAN | lockstep replay at 7 new shapes x 4 own seeds (0 mismatches, 120 resets) with a non-vacuous control; reset and valid-bit analysis; index range guard; flop and RAM arms mixed in one engine; `srp_store_wrap.sv:20-27,164-169` | R459-3 | b59e99cb928939f5c4089964dea8f4628d06ede7 |
| Tests | CLEAN | default `make` of srp_top, srp_stream_fsms, srp_admission (all shapes); `mutants.py` 126/126, 78/78; 12 reviewer probes (9 caught, 3 equivalent with reasons); `walk_main.cpp`, `srp_walk_wrap.sv`, `srp_store_wrap.sv`, both Makefiles | R459-3 | b59e99cb928939f5c4089964dea8f4628d06ede7 |
| Docs | CLEAN | `10_srp_engine.md:194-251`; `hdl-engineer.md:80-93`; `tb/srp_top/README.md` (#230 sections, `:621-625`); `tb/srp_stream_fsms/README.md`; PR body (live = `author-r2b`); `author-r2b/HANDOFF.md:146-156`; docs gates | R459-3 | b59e99cb928939f5c4089964dea8f4628d06ede7 |

## 6. Real limits

- **Not run by me** (not allowed in this round):
  - the full `run_suites.sh`, the Yosys gate, and the pp_top/adp/maap/notify/d3 campaigns;
  - the parent consumer set of 17, the builder, and gate 16;
  - Vivado;
  - Docker/act.
- **Lint scope.** Only the four changed SRP modules, not `lint_hdl.sh` over all 41.
- **Manager's bank receipts.** The brief states that the manager's full source static/builder and native banks
  passed at this head. I found no public receipt for them at this head: the evidence branch at `fd1ef4bf` holds only
  `author-r2b/HANDOFF.md` and `PR-BODY.md` for round 2b.
- **Simulation only.**
  - The equivalence evidence is randomized lockstep simulation plus directed arms, not formal equivalence.
  - One simulator (Verilator 5.050) was used.
  - Vivado's treatment of out-of-range indices was not examined: the engine never presents one (4.2).
- **Area figures.** They are the published round-1 Vivado runs (`hdl/srp` unchanged since). I did not rerun them.
- **Hosted `suites`** were `in_progress` at my last read, so they are not an executed result.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof.

## 7. Pending manager duties

- **Hosted acceptance:** both `suites` jobs at the exact head.
- **Publish the bank receipts:** the manager's static/builder and native bank receipts at `b59e99cb`.
- **The final current-dev candidate at the merge turn:** source base `c4cb84ff` onto live dev `fea346e7`, with the
  consumer set and its patches (c8, p2-p1, c10, and the #232 xvlog patch, as recorded by the lane and earlier
  rounds).
- **Acceptance item 5:** record the #230 scaling in #229 ("documented in #229"). The figures are in
  `10_srp_engine.md` §5.1 and on #230.
- **Close #230 manually** at the processor merge (ruling 5977836860).
- **Optional:** the suggestions S1-S3, and the R458-1 O1 observation (outside this diff).

## 8. Receipts

`MANIFEST.sha256` lists every published file, with paths relative to this packet. Local paths are redacted as
`<PACKET>`, `<CLONE>`, `<HOME>`, `<DATA>`, `<TOOLS>`, `<USER>`, `<HOST>` and `<VERILATOR_IMAGE>`.

- **Scripts:** `scripts/` (see `scripts/README.md`).
- **Simulator identity:** Verilator 5.050, `--version` "Verilator 5.050 2026-07-01 rev v5.050", wrapper sha256
  `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`.
- **Raw logs and rc files:**
  - `receipts/suites/`
  - `receipts/campaign/`
  - `receipts/probes/`
  - `receipts/lockstep/`
  - `receipts/lint_focus.*`
  - `receipts/docs-*.log`
  - `receipts/marginal.txt`
- **Public inputs as fetched:**
  - `receipts/issue230*.json`
  - `receipts/pr154*.json`
  - `receipts/check_runs*.json`
  - `receipts/commit_status.json`
  - `receipts/hosted_checks_final.txt`
- **Clone integrity after the review** (`receipts/clone_integrity.txt`):
  - HEAD `b59e99cb...` with tree `06d80d96...`, and the index tree is equal;
  - all 552 tracked blobs re-hashed equal in bytes and exec mode;
  - work tree and index equal HEAD;
  - 0 gitlinks, none required.
  - Two reviewer-created `__pycache__` directories, from importing the campaign driver to count its arms, were
    removed. After that, `git status --porcelain --ignored` is empty.
  - Every suite, campaign and probe ran on `git archive` copies under the packet's scratch directory.

R459-3 FINISHED

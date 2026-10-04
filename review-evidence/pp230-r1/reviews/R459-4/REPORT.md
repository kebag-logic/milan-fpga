[R459] POSITIVE - exact head d18270d69eea9cdf35f846c77821d5488dab97cc

# R459-4: external independent review of milan-fpga #230 / processor PR #154 (round 4)

- **Exact head:** `d18270d69eea9cdf35f846c77821d5488dab97cc`, tree `5ff7ea39fc74c21be0d6a1df92f07496513c5fab`
  (verified in the clone; `receipts/restore-verification.txt`).
- **PR base:** `main` `c050d971`. **Instructed source base:** `c4cb84ff`.
  - The range `c4cb84ff..d18270d6` also carries PRs #149, #152 and #153, which are already on `main`.
  - The PR's own diff is `c050d971..d18270d6`: 50 files, 14 lane commits, plus the manager's docs-only commit `b59e99cb`
    and merge `9160f7d7`.
  - `hdl/srp` is the same at `c4cb84ff` and `c050d971`.
- **Verdict:** POSITIVE.
  - No BLOCKER, MAJOR, MINOR or RESIDUE is open.
  - Three SUGGESTIONs, which do not affect the verdict.
  - Every prior public finding on this PR is resolved at this head (section 3).

## 1. Scope, reconstructed from public sources

These were read in this order. The repository has no `AGENTS.md` or `CONTRIBUTING.md`; `docs/README.md` is the
document index.

**The issue's frozen acceptance criteria (milan-fpga #230 body):**
1. SRP tests pass at 1x1 and 8x8.
2. Before and after hierarchical Vivado reports show a material reduction against the same baseline.
3. The 1x1 configuration has no logic for inactive slots.
4. WNS does not drop below zero.
5. Scaling and latency trade-offs are documented in #229.

**Public scope decisions (manager comments on #230):**
- **5967853024:** the timer-arm FIFOs join this issue (lever 2).
- **5974045353, the assignment:**
  - Behaviour is identical: no port, parameter-meaning, register or protocol-timing change.
  - Equivalence is proven with planted controls.
  - The 100 MHz criterion is judged at the declared 50 MHz.
- **5977836860, ruling (b):** the parallel per-stream evaluation is final for #230.
  - The shared evaluator (a) goes to #640.
  - #230 closes manually at the processor merge.
- **Rounds 2 and 3:**
  - 5978448959: committed coverage at both elaboration arms, and every probe planted as a killed control.
  - 5980793710: WK9/WK10 and the two handshake controls.

**Interface authorities checked:**
- `KL_srp_top`'s service plane admits a gate or control op only for `req_index_i < N` (`hdl/srp/KL_srp_top.sv:848-877`).
- The FSMs are instantiated only there (`KL_srp_top.sv:460,513,604`).
- `protocol_processor_top` binds `N_SOURCES_P = N_STREAM_OUT_P` and `N_SINKS_P = N_STREAM_IN_P`. The published Vivado
  runs use 2/2 for 1x1 and 9/9 for 8x8 (`baseline_chparam.txt`).

**Evidence examined:**
- The milan-fpga evidence branch `pp230-review-evidence`:
  - `8dca0983` (round-1 author packet);
  - `06fe795b` (the eight Vivado runs; all 32 files I used match the published SHA-256 in its `MANIFEST.json`);
  - `933388a4` (`author-r2/lockstep-r1/controls-final.log` and the round-3 `PR-BODY.md`, which equals the live PR body).
- Prior reviewers' reports were read only after my own pass (section 3).

## 2. Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### R459-4-S1 (SUGGESTION; RTL, Docs): the FIFO comment's flip-flop formula is the pre-trim size

- **Where:** `hdl/srp/KL_srp_top.sv:947-950`: "a two-dimensional array written for both FIFOs in one process mapped to
  2 x 32 x TFW_C flip-flops".
- **Evidence:**
  - At 1x1, TFW_C is 47: the head's final mapping is `32 x 47 | RAM32M x 8` (`receipts/vivado-figures.log`).
  - 2 x 32 x 47 = 3,008, while base synthesis kept 2,304 flip-flops after trimming constant bits.
    `docs/architecture/10_srp_engine.md:203` correctly states the measured 2,304.
- **Impact:** none on behaviour, tests or figures.
- **Optional outcome:** "up to 2 x 32 x TFW_C flip-flops (2,304 after synthesis at 1x1)".

### R459-4-S2 (SUGGESTION; Tests): randomise unreset memory in the FIFO arms

- This carries R459-3-S1 / R458-3-S1, which were not taken.
- **Where:** `tb/srp_top/Makefile:58-62` (`storage`). It does not use `--x-initial unique` or
  `+verilator+rand+reset+2`, unlike the walk arms.
- **Impact:** none today.
  - TF1/TF2 already fail on any invented word.
  - All 10 FIFO controls and my three FIFO probes (p07-p09) are killed.

### R459-4-S3 (SUGGESTION; Tests): the smallest listener RAM arm is not elaborated by a committed suite

- The walk arms run the listener at 1, 2, 5 and 9 sinks. `g_wsid_ram` at N = 3, its smallest shape, is not built by
  any committed suite. The talker's smallest RAM arm, 3, is built.
- My lockstep covers listener N = 3:
  - 0 mismatches over 4 x 1M cycles;
  - planted control c3 is caught there with about 320,000 mismatching cycles per seed.
- So this is coverage hygiene only. A 5/3 shape in `WALK_SHAPES` would close it.

### Observation (not a finding): valid ops with an out-of-range index

- With the driver allowed to offer a *valid* gate or control op at an index of N or above, the lockstep diverges at
  non-power-of-two shapes:
  - talker N = 1, 5 and 9 (`ev_value_o`, `user_vid_o`);
  - listener N = 5 and 9 (`user_vid_o`).
  - Receipt: `receipts/lockstep-anyindex.log`.
- Such an op reads and writes outside the declared range in both the base and the head. SystemVerilog leaves those
  reads undefined, and the two copies diverge even in code this PR does not touch (`user_vid_o` of the listener).
- `KL_srp_top` never offers such an op (`KL_srp_top.sv:848-877`). With in-range op indices, and idle faces left free
  to hold any index, every shape gives 0 mismatches (section 4.3).

## 3. Prior public findings at this head (read after my own pass)

| Finding | Status at `d18270d6` | Basis (this review) |
|---|---|---|
| R459-1-F1 (Vivado receipts unpublished) | RESOLVED | Published at `06fe795b`. I re-derived 32 figures, all equal (`receipts/vivado-figures.log`, rc 0). |
| R459-1-F2 / R458-1-F3 (control-coverage overclaim) | RESOLVED | The PR body has row-by-row tables. All 16 round-1 rows equal the published `controls-final.log` (`receipts/lockstep-r1-table-check.log`). All 35 campaign rows equal my receipts (`receipts/tabulate-controls.log`, rc 0). The summaries 6/4/5/1 and 19/1/7/4 recount correctly. |
| R459-1-R1, R459-1-R2 (residue) | RESOLVED | The body names `docs/architecture/10_srp_engine.md` section 5.1 in full. The header reads "all rc 0 except parent gate 16". Commit `6532439`'s subject is kept by decision. |
| R459-1-S1 | TAKEN | `docs/guides/hdl-engineer.md:88-94`. |
| R459-1-S2 | Answered by committed arms instead | WK1-WK10 and TF1-TF5. The round-1 bench is published at `author-r2/lockstep-r1`. |
| R458-1-F1 (no committed test of the new storage paths at N <= 2) | RESOLVED | WK1-WK10 at 1/1, 2/2, 3/5, 9/9 and TF1-TF5 at the same shapes pass at head. 31 storage controls are killed, and all 12 of my own probes are caught (section 4.4). |
| R458-1-F2 | RESOLVED | As for R459-1-F1. |
| R459-2-F1 / R458-2-F1 (README coverage sentence; 1/1 zero misattributed) | RESOLVED | `tb/srp_top/README.md:623-628` names the `wsid-flops-of-control-sink` exception and the simulator cause. The PR body row says "equivalent in simulation". |
| R459-2-R1 / R458-2 R2-R1 (stale "head") | RESOLVED | The body says "Head `d18270d6`", "Processor suites (round 2), at `7365022`" and "their inputs equal `1199255`'s". |
| R458-2 R2-R2 / R458-3-R1 (storage-rule lead-in) | RESOLVED | The text is exactly as required, spanning lines 88-90, and rewrapped (all lines <= 86 columns). |
| R459-3-S3 (rewrap line 90) | TAKEN | As above. |
| R459-3-S1, R458-3-S1 | Not taken (optional) | Carried as R459-4-S2. |
| R459-3-S2, R458-3-S2 (WK6 alias note) | Not taken (optional) | The srp_top README carries the note; this is not a defect. |
| R458-3-F1 (walk-copy handshake term pinned by no test) | RESOLVED | WK9/WK10 at head. `wtsp-write-ignores-ready` is KILLED at 4 of 4; `wsid-write-ignores-ready` at 3/5 and 9/9 (n/e at 1/1 and 2/2). My extra probe p01 (only the `wid_r` write ignores ready) is caught by WK9 at 3/5 and 9/9. My lockstep controls c1 and c5 are caught. |

## 4. Lens evidence

### 4.1 Conformance: CLEAN

| Acceptance (issue #230) | Status | Evidence |
|---|---|---|
| 1. SRP tests pass at 1x1 and 8x8 | Met | All SRP suites pass at head (section 4.4). The product shapes 2/2 and 9/9 are exercised by WK1-WK10 and TF1-TF5. The equivalence to base holds at 1, 2, 3, 5, 8 and 9 contexts in my lockstep and at the author's published top-level lockstep shapes. The end-to-end suites themselves run at 8 contexts only, as at base. |
| 2. Material reduction, same baseline | Met | `u_srp`: 1x1 4,558 -> 3,988 LUT, 6,438 -> 3,979 FF. 8x8 8,705 -> 7,313 LUT, 11,192 -> 7,747 FF. Route 4,340 -> 3,711 LUT, 6,263 -> 3,839 FF. Same recipe and base for both. Re-derived from the published reports. |
| 3. No logic for inactive slots at 1x1 | Met | Every per-stream structure is sized by `N_STREAM_OUT_P`/`N_STREAM_IN_P` = 2 at 1x1 (`baseline_chparam.txt`). The final mapping shows 2-deep `wtsp_r` and `slope_q_r`. |
| 4. WNS >= 0 (judged at 50 MHz) | Met | Route WNS +0.079 -> +0.354 ns, WHS +0.014 -> +0.036 ns, 0 routing errors. The out-of-context estimates are negative at base and head alike (-2.059 -> -1.874, -2.161 -> -1.495) and are not the criterion. |
| 5. Scaling documented in #229 | Pending manager duty | The lane may post only on #230. `docs/architecture/10_srp_engine.md` section 5.1 records the scaling, and the PR body records ruling (b)'s latency trade-off. The PR uses "Relates to", not a closing keyword. |

Further conformance checks:
- **Ruling (b):** no shared evaluator was attempted. The matcher, transitions and published levels stay parallel.
- **No port, parameter or register change.** The diff to the four SRP modules is internal: only localparams inside the
  module body, and no header change. `lint_hdl.sh` gives 41/41 LINT OK.
- **Behaviour identity:** 0 lockstep mismatches (section 4.3).

### 4.2 RTL: CLEAN

- **Timer-arm FIFOs (`KL_srp_top.sv:947-984`).**
  - Two one-dimensional memories, each written in its own process under the unchanged `tf_push_w` guards.
  - The registered head read `tf_q_r` is unchanged, and so are the pointers, counts, depth and full guard.
  - The old array had no reset either.
- **Talker (`KL_srp_talker_fsm.sv:361-372`, `:495-537`, `:586-596`).**
  - `gate_open_acc_w = rst_n && gate_acc_w && gate_open_i` equals the flop record's enable: the `else` branch of the
    synchronous reset, `gate_acc_w`, `gate_open_i`.
  - `rec_valid_r` is set only there and cleared only by reset, and the walk pushes only when
    `rec_valid_r[wsrc_r]` (`:615`). So no unwritten word is ever published.
  - Field slices `[123:60]`/`[59:12]`/`[11:0]` and `[67:52]`/`[51:36]`/`[35:32]`/`[31:0]` match the write
    concatenations.
  - A same-cycle write and walk read returns the pre-write value in both versions.
- **Listener (`KL_srp_listener_fsm.sv:534-558`).** The `wsid_r` enable equals the A15 settle branch (`:622-631`).
  `sid_r` has no other writer.
- **Admission (`KL_srp_admission.sv:111-115`, `:162-169`, `:195-211`).**
  - `slope_q_r` is written every non-reset cycle at `cidx_q2_r`, as before.
  - Every consumer of `slope_q_r[aidx_r]` is gated by `slope_valid_r`, which is written in the same cycle as the slope.
- **Mapping (Vivado final mapping, head 1x1):**
  - `tf_tk_ram_r`/`tf_ls_ram_r` 32 x 47, `RAM32M x 8` each;
  - `wtsp_r` 2 x 68, `RAM32M x 12`;
  - `slope_q_r` 2 x 32, `RAM32M x 6`.
  - The `Synth 8-7186` "ram_style ignored" warnings name only `KL_aecp_notify` `rows_r`, also present at base (16).
  - SRP's only block RAM is still the decoder's RAMB18.

### 4.3 Robustness: CLEAN

- **Independent lockstep** (`scripts/lockstep/`):
  - It generates a wrapper per module and shape, holding the base module (renamed) beside the head module, and
    compares every output port each cycle after the first reset.
  - Stimulus is seeded random: shared stream_id/DA/VLAN pools across the gate, control and decoder faces, ready
    back-pressure, ticks and LeaveAlls, admission TSpec changes with and without `invalidate_i`, and mid-run resets.
  - Unreset state starts random and independent per variable (`--x-initial unique`, `+verilator+rand+reset+2`).
- **Result (`receipts/lockstep-matrix.log`):**
  - Talker and listener at N = 1, 2, 3, 5, 8, 9 and admission at N = 1, 2, 3, 5, 8, 9.
  - 72 runs x 1,000,000 cycles, 1,837 mid-run resets, **0 mismatching cycles**.
  - The stimulus was active throughout. For example, at talker N = 9, seed 11, `ev_valid_o` was high on 148,942
    cycles; at admission N = 9, `round_done_o` fired 80,221 times.
- **Planted controls in the same matrix:** all five are caught wherever their arm is elaborated, with between 170,000
  and 907,000 mismatching cycles per seed.
  - c1 `wtsp` write ignores ready: N = 2, 3, 9.
  - c2 `wid_r` read neighbour: N = 3, 9 (0 at N = 2, n/e).
  - c3 `wsid` write ignores ready: N = 3, 9 (0 at N = 2, n/e).
  - c4 slope read source 0: N = 2, 3, 9.
  - c5 only the `wid_r` write ignores ready: N = 3, 9 (0 at N = 2, n/e).
- **Out-of-range valid ops:** see the observation in section 2.

### 4.4 Tests: CLEAN

All runs used the pinned Verilator 5.050 (`receipts/tool-identity.txt`) on a copy whose 554 blobs equal the head tree.

- **Suites at head.**
  - `tb/srp_stream_fsms`: walk arms 35, 46, 67 and 123 checks at 1/1, 2/2, 3/5 and 9/9, then the suite's 1,219, all PASS.
  - `tb/srp_top`: TF arms 15 x 4, then 2,200, all PASS.
  - `tb/srp_admission`: 1,138, 12,615, 41,012, 201,073 and 991,231, all PASS.
  - `tb/pp_top`: 10,416 checks, 0 FAIL.
  - Every rc is 0.
- **Campaign at head.** `tb/srp_top/mutants.py --jobs 6`: **128 checks, 128 PASS, assertion coverage 80/80**, rc 0
  (`receipts/campaign-srp_top.log`, per-label logs in `receipts/campaign-out/`).
- **Control tables.** Every row of the README's 31-row walk/FIFO table and 4-row slope table equals my receipts,
  cell for cell, including each "Caught at" (`scripts/tabulate_controls.py`, rc 0).
  - The README itself says the slope counts at N = 3, 5 and 8 come from separate per-shape runs, because the suite
    stops at its first failing shape. I re-ran them one shape at a time (`scripts/slope_shapes.sh`,
    `receipts/slopes/`), and every count matches.
- **My own 12 probes** (`scripts/probes.py`, none of them in the committed set) are **all CAUGHT** by committed
  suites (`receipts/probes-summary.log`):

  | Probe | Caught by |
  |---|---|
  | p01 only the `wid_r` write ignores ready | WK9 at 3/5 and 9/9 |
  | p02 MaxFrameSize/MaxIntervalFrames swapped | WK1-WK5, WK9 at 4 of 4 |
  | p03 VLAN slice off by one | 4 of 4 |
  | p04 DA slice off by one | 4 of 4 |
  | p05 `wsid_r` read at the control sink | WK6, WK8, WK10 at 3/5 and 9/9 |
  | p06 `wsid_r` read at the neighbour | 3/5 and 9/9 |
  | p07 listener head read ahead | TF2, TF5 at 4 of 4 |
  | p08 listener write at the read pointer | 4 of 4 |
  | p09 talker FIFO written with the listener word | TF1-TF5 at 4 of 4 |
  | p10 slope read at the store index | admission N = 2 |
  | p11 granted slope of source 0 | admission N = 2 |
  | p12 `wtsp_r` written at the walk source | 2/2, 3/5, 9/9; equivalent at 1/1 |

- **Hygiene.**
  - `git diff --check` is clean.
  - New sources carry SPDX lines. The 35 patches follow the existing patch convention.
  - The walk-arm and FIFO-arm `make` targets keep each suite's tally as the last line and exit non-zero if any part
    fails.

### 4.5 Docs: CLEAN

- **`docs/architecture/10_srp_engine.md` section 5.1 (lines 194-252, before section 6 at 253).**
  - The storage table matches the RTL: widths 124, 68, 64, 104, 32 x M; `N_CAD_C` = 5; encoder 285/19; VLAN 17.
  - It also matches the Vivado mapping.
  - The marginal-cost table re-derives exactly: talker 129/168 (base 213/221), listener 208/278 (227/278), admission
    69/69 (73/101), engine 475/538 (592/679).
  - The device and tool version match the reports: xc7a100tfgg484-2, Vivado 2026.1.
- **`docs/guides/hdl-engineer.md:88-94`:** the storage-rule exception names exactly the new memories.
- **READMEs:** the counts and tables are verified (section 4.4).
- **`make check` at head:** rc 0 — lint 41 mermaid + 18 wavedrom blocks, 1,131 links, matrix, params, stale.
- **PR body.** Spot-checked against receipts:
  - the Vivado table, F7 delta 296, the lever-2 and lever-4 deltas and the per-context costs;
  - the commit counts per round;
  - both control tables and their summaries.
  - All agree. The live body equals the published round-3 `PR-BODY.md` apart from a trailing newline.

## 5. Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #230 acceptance and rulings; `KL_srp_top.sv:848-877`; the four SRP module headers; `protocol_processor_top` binding; Vivado `chparam`, utilization, timing, route status (32 files, digests verified) | R459-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |
| RTL | CLEAN | `hdl/srp/KL_srp_{top,talker_fsm,listener_fsm,admission}.sv` diff and context; Vivado final RAM mapping; `lint_hdl.sh` 41/41 | R459-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |
| Robustness | CLEAN | own base-versus-head lockstep, 72M cycles, 0 mismatches, 5 controls caught; out-of-range characterization | R459-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |
| Tests | CLEAN | `tb/srp_stream_fsms`, `tb/srp_top`, `tb/srp_admission`, `tb/pp_top` suites; the srp_top campaign 128/128 (80/80); 35 control rows re-tabulated; 12 own probes; per-shape slope runs | R459-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |
| Docs | CLEAN | `10_srp_engine.md` section 5.1, `hdl-engineer.md` section 3.1, both READMEs, PR body, `make check` | R459-4 | `d18270d69eea9cdf35f846c77821d5488dab97cc` |

## 6. Real limits

- **Banks not run, as the brief requires:** `run_suites.sh`, the Yosys gate, the parent consumer set, the builder, and
  every campaign other than srp_top.
  - The manager's source static/builder and native banks are said to pass at this head. I found no public receipt for
    them in the evidence I examined, and they do not enter this verdict.
- **No Vivado run.** The area and timing figures were re-derived from the published round-1 runs, made with processor
  `65324390`.
  - `hdl/srp` is byte-identical between `65324390` and this head.
  - The `KL_pp_shadow` totals predate the `main` merges (#149, #152, #153), which change non-SRP HDL. The `u_srp`
    deltas are unaffected.
- **My lockstep runs at the FSM-module level** (talker, listener, admission), not `KL_srp_top`.
  - The FIFO change is covered by the TF arms, 10 killed FIFO controls and my probes p07-p09.
  - It is also covered by the author's published top-level lockstep log (16 rows checked, bench not re-run).
- **The stimulus is random, not exhaustive.**
  - Verilator is two-state, so X propagation is approximated by random initial values.
  - The out-of-range valid-op space is unreachable through `KL_srp_top` and is characterized, not graded.
- **Hosted checks at this head** (`receipts/hosted-checks-snapshot.txt`, 15:03 UTC):
  - executed and successful: `docs-gates` x2 and `portability` x2;
  - still in progress: `suites` x2.
  - Hosted and act acceptance is the manager's.
- **Physical calibration NOT RUN.** Field skips are not hardware proof, and no hardware was used.

## 7. Pending manager duties

1. **Acceptance item 5:** document the scaling and ruling (b)'s latency trade-off on #229 before #230 is closed. The
   material is in `docs/architecture/10_srp_engine.md` section 5.1 and the PR body's "What remains".
2. **Merge-turn checks:** build the final current-dev candidate (source base `c4cb84ff`, live dev `fea346e7`) and run
   the parent consumer set at the merge turn.
3. **Hosted acceptance:** the hosted `suites` jobs were in progress at my snapshot.
4. **Issue closure:** close milan-fpga #230 manually at the processor merge (ruling 5977836860). The PR body uses
   "Relates to".
5. **Optional:** carry R459-4-S1..S3.
6. **Publication:** archive this packet. Receipts are sanitised: host paths are replaced by `<SIM_ROOT>`, `<PACKET>`,
   `<CLONE>`, `<PINNED_SIM>` and `<HOME>`, and the per-shape slope logs are gzip-compressed.

## 8. Receipts and scripts

Every file is listed in `MANIFEST.sha256`.

**Scripts** (`scripts/`):
- `lockstep/` (`gen_lockstep.py`, `drive.hpp`, `ls_main.cpp`, `build_run.sh`, `matrix.sh`);
- `probes.py`, `slope_shapes.sh`, `tabulate_controls.py`, `vivado_figures.py`.

**Reproduce, with `VERILATOR` set to the pinned 5.050:**
- `scripts/lockstep/matrix.sh <head-tree> <base-tree> <work> 1000000 <jobs>`. Add `LS_CFLAGS=-DLS_ANY_INDEX` for the
  any-index characterization.
- `scripts/probes.py <head-tree> <work> <receipts>`.
- `scripts/slope_shapes.sh <head-tree> <work> <receipts> <jobs>`.
- `scripts/tabulate_controls.py <campaign-out> <tb/srp_top/README.md> <slope-receipts>`, after gunzipping the slope logs.
- `scripts/vivado_figures.py <vivado-dir> <MANIFEST.json of 06fe795b>`.

**Clone state after review:**
- HEAD `d18270d6`, tree `5ff7ea39`;
- index equals HEAD (modes and blobs), worktree equals index, 0 untracked or ignored files;
- no gitlinks (no `.gitmodules` at this head).
- Every build and probe ran in copies under `scratch/`; the clone was never written.

R459-4 FINISHED

[R452] NEGATIVE - exact head 6e950fea861d76664dc2f7396c980b1ada2e47c1

# R452-1: internal independent review of PR #153 (milan-fpga #232, area lane)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #153, exact head
  `6e950fea861d76664dc2f7396c980b1ada2e47c1`, tree `b0baec9241197c6b5071243bba67f550ef951d7e`
  (both verified in the reviewer's detached clone; worktree clean before and after).
- Source base `f4167536d358c996f4e1b70b875879c1651f85d3`; merged main `5c71928ad2bf1a854a5538d69b77214dfdf1697f`.
- Review start: PR #153 comment 5976228848. Round R452-1.
- Verdict: **NEGATIVE**, because one MINOR finding (R452-1-F1, Tests) is open. The RTL change itself
  is correct: an independent lockstep run of main against the head found no difference.

## 1. What was reconstructed (in order)

1. Repository rules: the processor repository has no AGENTS.md or CONTRIBUTING.md. The rules
   applied are `hdl/README.md` (rules 1 to 5: vendor-neutral SV, Verilator plus Yosys tool floor,
   "a module is not done until its testbench is"), `docs/README.md` and `docs/guides/hdl-engineer.md`.
2. Issue kebag-logic/milan-fpga#232: the frozen scope and acceptance in the issue body, and the
   public decisions in its comments: the lever-5 scope addition (5967852823), the lane assignment
   and rules (5970460015: identical behaviour, every count unchanged, 100 MHz judged at the
   declared 50 MHz), the STOP (5973996744), the lever-5 ruling (c) (5974004216: stamps stay in
   flops without their reset; "Closes milan-fpga#232" allowed), the round-1b assignment
   (5974077269), and REVIEW READY (5976213371).
3. Authorities: Milan SS5.3.4.2 (registry entry) and SS5.4.5.3 (availability monitor), as cited
   in the `KL_aecp_notify` banner. The 06 F06.5 registry lifecycle. The 01 F01.5 parameter
   table (`P-NOTIF-QUEUE-DEPTH`). The port list of `KL_aecp_notify` (unchanged by the lane).
4. History and diff: `git diff f4167536..6e950fea` (37 files, mostly main's P1/C10 work arriving
   through the merge). The lane's own content is `git diff 5c71928a..6e950fea`: 7 files,
   `KL_aecp_notify.sv`, `tb/aecp_notify/{sim_main.cpp,README.md}`, `tb/pp_top/notify_mutants.py`,
   `tb/pp_top/README.md`, docs 06 and 09.
5. Public evidence: milan-fpga `ed9f5f46:review-evidence/pp232-r1` (MANIFEST.json, the author's
   HANDOFF.md and PR-BODY.md, and five parent patches); the PR body; and the exact-head hosted
   check runs. The issue and PR carry no manager evidence comment beyond what is listed above.
   The lockstep bench and the raw Vivado logs are not published (HANDOFF §11 and R1b.9 give only
   16-hex log digests).
6. Prior public review findings on PR #153: **none exist**. The PR has two review-start notices
   and no review or review comment. Issue #232 carries no review findings. So there is nothing to
   resolve or retain.

## 2. Findings

### R452-1-F1 - MINOR - Tests

- **Where.** `hdl/aecp/KL_aecp_notify.sv:578-579`, `:598-600`: in the re-index window, the hit mux
  selects `ix_own_w` for row `wr_ix_r` during both `ix_clr_r` (the row write's own cycle, T+1) and
  `ix_set_r` (T+2). `ix_own_w` compares the command against `rows_r[wr_ix_r]` as read.
  `tb/aecp_notify/sim_main.cpp:262-279` (IX4) presents its command and failed probe only in the
  set cycle. The comment at `:263` reads "the row write's own cycle", then `tick()`.
- **Authority.** `hdl/README.md` rule 3 ("a module is not done until its testbench is"). The
  lane's own convention: each new behaviour has a check with a killed control
  (`tb/aecp_notify/README.md:83-90`). The assignment rule "Behaviour is identical" (5970460015).
  The PR's equivalence proof is a lockstep bench kept "in lane scratch, not committed", and it is
  not in the public evidence either.
- **Evidence.** Two one-line planted faults in the clear-cycle half of the window (reviewer copies
  from `scripts/lockstep/plant.py`) pass every committed suite that grades the block:
  - `override_set_only`: the comparator covers only T+2, and T+1 reads the index.
    `tb/aecp_notify`: 20/20 PASS. `tb/pp_top` (all builds and sections): 10,416/10,416 PASS.
  - `own_compare_new_row`: the window comparator reads `wr_row_r` (the incoming row) instead of
    what `rows_r` holds. `tb/aecp_notify`: 20/20 PASS. `tb/pp_top`: 10,416/10,416 PASS.
  - Receipts: `receipts/probe/clearprobe-*.log`, `receipts/runs/clearprobe.log`,
    `receipts/probe/u_*.log`. The control `no_override` (both cycles removed) is caught, by IX4
    only (`receipts/probe/u_no_override.log`).
  - Both faults change observable behaviour. In the reviewer's lockstep bench they gave
    2,100,593 and 38,639,026 mismatches, each caught in 8 of 8 runs (`receipts/runs/lockstep.log`).
    `own_compare_new_row` shows without any reset: in T+1, a command carrying the reused row's
    previous identity hits that row in main (848,558 such commands, all hits, over the head runs).
    So a failed probe for the row in that cycle is ignored in main but parks an expiry under the
    fault.
- **Impact.** Half of the new rewrite-window logic, the part that keeps T+1 equal to main's
  comparator bank (including after a reset inside the window), is held only by an unpublished,
  uncommitted bench. A later edit that narrows the mux to `ix_set_r`, or compares the incoming
  row, would pass every committed suite and campaign.
- **Required outcome.** A committed check that fails on both faults, recorded with its controls.
  Either:
  - extend `tb/aecp_notify` section IX with a clear-cycle case: in the row write's own cycle,
    present a failed probe for the row together with a command carrying the row's current
    `rows_r` identity (for a reused row, its previous controller), and add a case with a reset
    inside the window followed by re-registration; or
  - commit the lockstep differential bench as a suite.
  Add both faults (or equivalents) to `tb/pp_top/notify_mutants.py` and to the
  `tb/aecp_notify` and `tb/pp_top` README mutation records, KILLED.
- **Verification.** `python3 tb/pp_top/notify_mutants.py --only <the new controls>` reports
  KILLED. The goldens and the other arms stay at their README counts.

### R452-1-F2 - RESIDUE - Docs (PR body wording only)

- **Where.** The PR body's storage inventory, row "Registry identity index (new)". The quoted
  report text reads "`64 x 1 | RAM64M x 1`" and "`16 x 1 | RAM16X1D x 1`". Item 1 of the same body
  says "288 RAM64X1D and 16 RAM32X1D". HANDOFF §5 has the same pair.
- **Why only wording.** The figures agree once the two sources are named. `u_notify`'s 960 LUTRAM
  (route and standalone) is 64 x 4 (`rows_r` RAM32M) + 24 x 4 (`cmdq_*`) + 288 x 2 (RAM64X1D) +
  16 x 2 (RAM32X1D) = 960. That fits only the two-LUT cells; 288 RAM64M alone would be 1,152.
  The reviewer's Yosys cross-check also maps the index as 304 64x1 memories, beside 88 RAM32M
  (`receipts/yosys/head-stat.txt`). No measurement, figure or verdict changes.
- **Exact fix.** In that row's Head cell, prefix the quotes with "synthesis mapping report:" and
  append "; implemented cells after optimization: 288 RAM64X1D (576 LUTs) and 16 RAM32X1D
  (32 LUTs), which with `rows_r`'s 64 and `cmdq_*`'s 24 RAM32M make `u_notify`'s 960 LUTRAM".

### R452-1-S1 - SUGGESTION - Docs

06 §7 "Storage (issue #232)", the identity-index row: add that the index's correctness relies
on its configuration-time zero content (the explicit `initial`, as the ROM images rely on
`$readmemh`), and that `rst_n` leaves both the index and `rows_r` as they are. Today only the
RTL comment (`KL_aecp_notify.sv:566-568`) says so. This is an integration assumption the row
table did not need before. It holds on the shipping FPGA, and the reviewer's lockstep included
294,625 reset cycles, 166,167 of them inside the window, with no mismatch.

## 3. Lens evidence

### Conformance: CLEAN

- No port, parameter or register change: the lane's hunks start after the port list and touch no
  `parameter`. Behaviour is unchanged, so every Milan/IEEE clause the block implements behaves as
  at main. The lockstep below compares every output and `rx_cmd_hit_w`.
- #232 scope against the PR and the rulings:
  - Registry: lever 1, done.
  - Throttle stamps: lever 5, ruled (c). `ctr_last_r` keeps flops and only its reset loop is
    removed (`git diff`, the base's `:934` line). `ctr_sent_r` gates every read
    (`:1096-1098`, `:1297-1298`). The `stamp_without_valid` control shows the gate matters
    (27.9 M mismatches).
  - Command queue: unchanged, `CMDQ_N_C` 16 = `P-NOTIF-QUEUE-DEPTH`.
  - Exhaustion: NO_RESOURCES, the `cmdq_drop_r` counted drop and per-class coalescing are
    pre-existing and unchanged.
  - Response buffer: `KL_aecp_resp_buf.sv` declares no unpacked array. `:336`/`:339` address main
    memory at `RESP_BASE_P`.
  - Valid/bulk split: recorded.
  - "Closes milan-fpga#232" is allowed by ruling 5974004216.
- 100 MHz is judged at the declared 50 MHz, per the assignment. Route closure is the author's
  figure (WNS +0.274 / WHS +0.023 ns), not re-derivable here (see Limits).

### RTL: CLEAN

- Re-index window (`KL_aecp_notify.sv:551-602`, `:1046-1056`, `:1364`):
  - `N_APPLY` is the only identity writer. It goes to `N_ANS`, which writes nothing, so no other
    row write can be decided in T+1 or T+2. `wr_ix_r` and `wr_row_r` are stable through the
    window. The reviewer's coverage counter "other writes in window" is 0 over 448 M cycles.
  - The emission write-back (`:1452-1454`) re-latches `hold_*` at `N_EMIT_RD` with no row write
    possible before `N_EMIT_WB`. So it rewrites the row's own identity, and the index stays exact.
  - A reset in T+1 lets the row write and the clear land but suppresses the set, and clears
    `valid_r`. The index stays a subset of the row's identity, and the next claim re-indexes it.
  - The clear reads the old row through the write port's read (`ix_wr_row_w`), which is
    read-before-write in both simulation and LUTRAM.
  - Last chunk: the 112-bit key is zero-extended to 114 bits on both sides, so chunk 18 carries 4
    live bits.
- Mapping intent: `rows_r` is now read at three addresses (`rd_ix_w`, `ca_pick_ix_w`, `wr_ix_r`),
  and the third shares the write address, which fits RAM32M's three read ports plus one
  read/write port.
- #22 (`6e950fe`): a pure move of two declarations plus one comment line. A scripted scan finds
  no module-level `logic` used before its declaration in the head file.
- Merge `823fc20` keeps both sides. The merge's change set over main equals the lane's over the
  base (`f4167536..3ab2e4d`), except the single `tb/pp_top/README.md` conflict, resolved as the
  PR describes. No HDL file was changed by both sides.
- `scripts/lint_hdl.sh`: 41 of 41 LINT OK (`receipts/runs/lint.log`).

### Robustness: CLEAN

- Exercised by the reviewer's lockstep (below):
  - resets at random and biased into the window: 84,010 reset cycles in T+1 and 82,157 in T+2;
  - reused rows: 2,716,353 identity-changing re-indexes and 637,318 same-identity refreshes;
  - the all-zero identity and chunk-sharing identity families, which would expose a doubled or
    stale index row (caught by `no_clear` and `clear_new_identity`);
  - `now_ms_i` wrap and arbitrary jumps;
  - out-of-range probe owners;
  - shapes N_CTRL 1, 2, 3 and 5 (non-power-of-two) as well as 16.
- Exhaustion behaviour is unchanged: equivalence covers it.
- Index initial content: see S1.

### Tests: UNCLEAN (R452-1-F1)

All runs below use pinned Verilator 5.050 (`verilator` wrapper sha256 `905795b9...e92f`; the
host's 5.052 was kept off PATH), on `git archive` trees of the exact head.

- **Reviewer lockstep** (`scripts/lockstep/`, independent of the author's unpublished bench):
  - Setup: main's `KL_aecp_notify` renamed `_ref`, beside the head's, with identical inputs.
    Compared: every output, concatenated, plus each instance's `rx_cmd_hit_w`, before and after
    every clock edge.
  - Runs: seven shapes (16/2/2, 16/9/9, 2/1/1, 16/2/2 with identify, 5/8/8, 1/1/1, 3/1/2 with
    identify), 16 seeds each, 4,000,000 cycles. Odd seeds are protocol-shaped, even seeds drive
    every input at random.
  - **Result: 112 runs, 448 M cycles, 0 mismatches.** 16/8/8 with identify off and on adds
    16 runs x 4 M, 0 mismatches (`receipts/runs/lockstep-extra.log`).
  - Window coverage: 2,550,063 commands in T+1 (1,241,380 hitting the row, 848,558 carrying its
    previous identity) and 2,486,879 in T+2 (2,003,906 hitting).
  - Ten planted controls, 8 runs x 4 M each, every one caught in 8 of 8 runs: `no_override`,
    `override_set_only`, `override_clr_only`, `no_clear`, `no_set`, `last_chunk_ignored`,
    `clear_new_identity`, `own_compare_new_row`, `register_not_reindexed`,
    `stamp_without_valid`.
  - The author's description of their own bench (40 x 1 M, five shapes, seven controls) is
    consistent with this, but it cannot be judged from public material.
- `tb/aecp_notify` IX:
  - 20/20 at head (`receipts/runs/suites.log`).
  - The head's IX bench on main's RTL: 20/20 (`receipts/probe/ixmain.log`), so IX describes
    unchanged behaviour.
  - The four `ix_*` controls are KILLED at their README counts: IX1; IX3 + IX4; IX2; IX4.
  - Gap: F1.
- `scripts/run_suites.sh`: rc 0, 33 suites, **1,021,455 checks**, 0 failing (`aecp_notify` 20,
  `pp_top` 10,416), equal to the PR's figure.
- Campaigns, each arm's verdict and failing-check count compared by script
  (`scripts/compare_counts.py`) with the README records:
  - `notify_mutants.py --jobs 6`: rc 0, 44/44 KILLED, six goldens PASS, 50 of 50 records at
    their counts.
  - `ctr_mutants.py --jobs 3`: rc 0, control PASS, 17/17 at their counts.
  - `aecp_mutants.py --jobs 2`: rc 0, 5 controls PASS, 55/55 at their counts.
  - `aecp_dispatch_mutants.py --jobs 2`: rc 0, 4 controls PASS, 40/40 at their counts.
  - `acmp_mutants.py --jobs 2`: rc 0, 19/19 KILLED, goldens PASS.
  - `d3_mutants.py --jobs 3`: rc 0, 110/110 KILLED, six goldens PASS. The 98 `tb/pp_top`
    arms are at their README counts. The 12 graded in `tb/acmp_nvm` and `tb/rx_validator` are
    KILLED; they are recorded there under other names, which the script does not map, as the PR
    states (`receipts/runs/d3-compare.txt`).
- `gsi_mutants.py` and `name_wr_mutant.py` were not run (see Limits).

### Docs: CLEAN (R452-1-F2 is RESIDUE, R452-1-S1 a suggestion)

- 06 §7 "Storage (issue #232)" matches the RTL:
  - shapes: 128-bit rows; 19 chunks; queue 132 bits = 4 + 4 x 16 + 64;
  - read indices;
  - flags in flops;
  - stamps in flops with no reset;
  - the exhaustion paragraph, against `amap_busy_o` (`:955-957`) and `cmdq_drop_r`
    (`:1089-1091`).
- 09's IX row, the `tb/aecp_notify` README (10 + 6 + 4 = 20 checks) and the `tb/pp_top` README
  record ("44 of 44") match the measured runs.
- Every line citation in the PR body and HANDOFF inventory resolves at head. Checked:
  - `KL_aecp_notify.sv` `:336`, `:337`, `:379-384`, `:404`, `:410`, `:551-602`, `:581-593`,
    `:584`, `:604-606`, `:608`, `:617`, `:726`, `:1098`, `:1364`;
  - `KL_pp_rx_slots.sv:193`, `KL_aecp_resp_buf.sv:336-339`, `KL_aecp_ucpu.sv:149`/`:159`;
  - `KL_aecp_desc_store.sv:285`/`:297`/`:309`, `KL_aecp_engine.sv:1195`;
  - `KL_pp_trace_ring.sv:86`, `KL_pp_tx_slots.sv:263`, `KL_pp_timer_service.sv:108`,
    `KL_pp_dispatch.sv:303`.
- `make check`: rc 0 (1,114 links, 115 REQ rows, 94 matrix rows with 0 untested, 28 parameters).
  `scripts/gen_matrix.py --check`: rc 0.

## 4. Area figures (re-derived from the published tables)

The raw Vivado reports are not published and no Vivado is available to the reviewer. What could
be done was re-derive every delta from the author's published tables (PR body, HANDOFF §4 and
R1b.6) and check it against an independent mapping signal.

Re-derived deltas:

- Route at the merge, head minus main: LUT 50,671 - 51,434 = **-763** (logic 47,533 - 49,158 =
  -1,625; memory 3,138 - 2,276 = +862). FF 57,660 - 59,691 = **-2,031**. Slices -6.
  WNS 0.274 - 0.079 = **+0.195**.
- `u_notify`: LUT 2,343 - 3,270 = **-927**; FF 1,287 - 3,299 = **-2,012**.
- Round 1 route: -650 / -1,950.
- Standalone: 1x1 -894 / -2,042; 8x8 -925 / -2,175.
- `u_notify` standalone: 1x1 -933 / -2,046; 8x8 -450 / -2,046.
- #638 gate: head minus A = 50,671 - 50,128 = +543; main minus A = +1,306.

All of these are arithmetically consistent.

Independent signals:

- LUTRAM: 960 = 256 + 96 + 576 + 32, as in F2.
- Yosys `synth_xilinx` cross-check of the block alone at 16/2/2 (`scripts/yosys_notify_probe.sh`,
  `receipts/yosys/`):
  - head: 88 RAM32M (`rows_r` 64 + `cmdq_*` 24, as the author's census), 304 64x1 index
    memories, 1,295 FDRE;
  - main: 1,048 RAM32M, because Yosys replicates the 16-read table rather than spilling it, so
    Yosys does not reproduce Vivado's flop spill;
  - the head's row-table mapping matches the census the PR reports.
- Zero `Synth 8-7186` at head, the WNS/WHS corners and the per-hierarchy figures are the author's
  report quotes. They are not independently verified (Limits).

## 5. #232 inventory

The PR body and HANDOFF §5 give, for every structure #232 names:

- the intended primitive;
- the actual primitive at base and at head, with report lines;
- the exhaustion behaviour.

The source-side facts were verified at head: declarations at the cited lines, attributes, and no
array in the response buffer. "No AECP or notification data buffer maps into flops" holds for
the source shapes. The measured side rests on the author's unpublished logs (Limits).

## 6. Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #232 body and rulings (5967852823, 5970460015, 5973996744, 5974004216, 5974077269); `KL_aecp_notify.sv` ports, parameters and banner clauses; lever-5 diff; `KL_aecp_resp_buf.sv`; PR closing keywords | R452-1 | 6e950fea861d76664dc2f7396c980b1ada2e47c1 |
| RTL | CLEAN | `KL_aecp_notify.sv:330-357`, `:551-620`, `:955-1468`; `6e950fe`; merge `823fc20` change-set equality; lint 41/41; reviewer lockstep 448 M + 64 M cycles, 0 mismatches | R452-1 | 6e950fea861d76664dc2f7396c980b1ada2e47c1 |
| Robustness | CLEAN | reset in window (166,167 cycles), reused rows, zero identity, chunk-sharing identities, `now_ms_i` wrap, shapes 1/2/3/5/16, exhaustion paths (unchanged) | R452-1 | 6e950fea861d76664dc2f7396c980b1ada2e47c1 |
| Tests | UNCLEAN (F1) | `tb/aecp_notify` IX and README; `notify_mutants.py` `IDENTITY_INDEX`; suites 1,021,455; notify, ctr, aecp, dispatch, acmp and D3 campaigns compared with the README records; clear-cycle probes on `tb/aecp_notify` and `tb/pp_top` | R452-1 | 6e950fea861d76664dc2f7396c980b1ada2e47c1 |
| Docs | CLEAN | 06 §7 and realization note; 09 §8.4 row; `tb/aecp_notify` and `tb/pp_top` READMEs; PR body and HANDOFF citations and figures; `make check`, `gen_matrix --check` | R452-1 | 6e950fea861d76664dc2f7396c980b1ada2e47c1 |

## 7. Real limits

- **No Vivado is available here.** The route and standalone figures, the per-hierarchy cells,
  zero `Synth 8-7186`, the four signoff corners and the RAM mapping report lines are re-derived
  only arithmetically from published tables, plus a Yosys analogue. The raw logs are not public
  (16-hex digests only).
- **The author's lockstep bench is not public,** so its completeness cannot be judged. The
  reviewer's own bench substitutes for it.
- **Not run:**
  - `gsi_mutants.py` and `name_wr_mutant.py`. They build the top but grade no lane-touched
    behaviour, and the block is proven output-identical.
  - The Yosys repository gate, all parent, gPTP and builder banks, and xvlog (prohibited or
    unavailable). For xvlog the reviewer relies on the scripted declaration-order scan.
- **Hosted checks at the exact head:** `docs-gates` and `portability` completed with success in
  both event contexts. `suites` was still in progress at 06:26 CEST. Hosted acceptance is the
  manager's.
- Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof.
- Source validation here is distinct from the final current-dev candidate.

## 8. Pending manager duties

- F1 must be resolved, and F2 carried to the residue checklist, before a positive verdict.
- The merge-turn candidate is the manager's: source base `f4167536`, live dev `241f9184`.
  - Run the parent consumer set (17) at dev `241f9184` with c8-bbf704ec + p2-p1 + c10 and the
    lane's `parent-adoption-pp232-xvlog-c10-5fabb46e.patch`. Gate 9 needs the `pd_ix_w` budget
    line banked.
  - Gate 16's T30 INTERNAL law checks belong to #643 / PR #648. The author's record shows them
    failing identically at main and at head.
- Hosted/act acceptance, including the in-progress `suites` job at the exact head.
- If the manager relies on acceptance criterion 1 ("Vivado hierarchy and RAM reports match the
  documented storage mapping"), publish or attest the head route's mapping-report lines and its
  zero `Synth 8-7186` count. The reviewer could not inspect them.
- Recording a new #638 baseline A is the merge bank's step, per the PR.

## 9. Receipts

- `scripts/`: `lockstep/` (harness, driver, build, controls, campaign), `compare_counts.py`,
  `clear_cycle_probe.sh`, `yosys_notify_probe.sh`, `run_bg.sh`, `collect_receipts.sh`.
- `receipts/`: run logs and rc files (`runs/`), probe logs (`probe/`), Yosys stats (`yosys/`),
  and campaign `results.json` (`campaigns/`). Local paths are replaced by `$PACKET`, `$CLONE` and
  `$HOME`.
- Every published file is listed in `MANIFEST.sha256`.
- After all probes: the reviewer clone is at the exact head, with a clean worktree, an untouched
  index and no submodules required (see the closing check in `receipts/runs/final_state.txt`).

R452-1 FINISHED

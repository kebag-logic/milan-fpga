[R863] POSITIVE - exact head 0297a19a056ee3d5d705bc502c4ae7808689ede7

Internal cleared-context review, round R863-1, of kebag-logic/milan-fpga PR #939 for issue #927 (split images'
timing floor). Head `0297a19a056ee3d5d705bc502c4ae7808689ede7`, tree `e3e4dbefc89e29cc646fd5e2cf757338ba3877a9`,
thirteen one-line commits on `dev-soft-core` `70f4056f`. All five lenses were applied. Each is CLEAN at this head:
no BLOCKER, MAJOR or MINOR is open. One RESIDUE (wording in a source comment) and two SUGGESTIONs are recorded.

## 1. What was reconstructed, and from where

- Contract: AGENTS.md (sections 3, 5 to 8), CONTRIBUTING.md (section 1 house style and CDC primitives, section 3
  verification bar), docs/README.md.
- Issue #927: the body's frozen acceptance criteria, plus the public scope decisions:
  - 6908876362: the scope widened to every split image at both shapes (four paths), with the ROM banking each image
    plans.
  - 6914223799: the third cut (`KL_mbx_dma`'s ring address) taken in this lane, under the timing-flow rule.
  - 6930885657: the floor is #818's, setup +0.030 ns and hold 0.
  - 6933111168: #818 grades a route set on the best of the three directives.
  - The REVIEW READY, 6933066988.
- Authorities: IEEE 1722.1-2021 7.4.45/7.4.46 (ADD/REMOVE_AUDIO_MAPPINGS through the EDIT window); IEEE 1722-2016
  and Milan v1.2 for the AAF meter's timestamps and group (Milan v1.2 7.3.2, 6 samples per PDU at 48 kHz);
  MAILBOX_SPLIT.md (contract 2.3, the EDIT window and its bound, the crossing, the record mover).
- Diff and history: `git diff 70f4056f..0297a19a` (20 files, +313 / -48), each commit's content, and the deltas from
  the route heads to this head (`5d098172..0297a19a`, `338ece89..0297a19a`).
- Author evidence: `review-evidence/927-r1/author-r1` and `author-r2` at archive `e83ed706` (route signoffs, worst
  paths, budget tables and regrades, release receipts, area, identity).
- Prior public review findings: at this head the PR carries only the two review-start notices (R863-1, R864-1). It
  has no prior review findings, so none is resolved or retained here. No other reviewer's report was read.

## 2. Independent execution at the exact head (this round)

Every run used the pinned Verilator 5.050 (identity checked: `Verilator 5.050 2026-07-01 rev v5.050`), each in a
disposable copy of this clone at `0297a19a` under the packet's scratch, with Verilator builds bounded to 4 jobs per
run. Four runs at a time was the plan; for a few minutes seven overlapped, when the three probe runs (small `mbx`
and meter builds and one datapath build) started beside the four campaigns. The `t1`/`t2` wrappers run two targets in sequence and print each target's own rc as a
`## <target> rc=` line; that is the rc quoted below.

| Run | Result | Receipt |
|---|---|---|
| `milan_dp split` | checks 143, failures 0, rc 0 | `receipts/t1-milan_dp-split-then-mutants.log` |
| `milan_dp split-mutants` | 29 of 29 caught by the check each names, control passes, rc 0 | same |
| `mbx all` | wb 546, axil 591, cosim 32, 2-if 553/598/490, mover 520,041 checks, 0 failures; mbx mutants 12/12; mover mutants 25/25; rc 0 | `receipts/t3-mbx-all.log` |
| `aaf_clock_meter all` | 465 + 6 checks, 0 failures; mutants 38/38 as required; rc 0 | `receipts/t3-meter-all.log` |
| `milan_dp_render tdm8render` | checks 263, failures 0, rc 0 | `receipts/t2-render-then-mutants.log` |
| `milan_dp_render tdm8render-mutants` (full) | 32 checks: 32 PASS, 0 FAIL (5 positive controls, 3 leg defects, 3 skew clean controls, 21 mutants, the FIFO arm among them), rc 0 | same |
| The render FIFO's arm alone, through the campaign's own `run_mutations` | caught: `T6 FIRST EVENT: ...in the frame its timestamp names` and `T6 PRESENTATION` fail | `receipts/t5-render-fifo-arm.log` |
| The render campaign's anchors | all 21 file-sourced arms anchor exactly once | `receipts/render_anchor_check.log` |
| `scripts/lint_rtl.py --check` | LINT GATE: PASS (89 <= 89) | `receipts/lint_rtl-check.log` |
| `docs/traceability/gen_module_matrix.py --check` | up to date (84 modules, 0 untested), rc 0 | `receipts/gen_module_matrix-check.log` |
| `cdc_pair_fifo` branch identity | PASS: the two `g_mem` branches differ only in `ram_style`; the base's write and read statements reappear once per branch | `receipts/fifo_branches.log` |

**Equivalence probes.** `scripts/apply_probes.py` inserts sim-only assertions into a copy of the tree. Each one
compares a cut register with the expression it replaced, every clock, and stops with `$fatal` on the first
difference:

- `KL_mbx_dma`: `ring_addr_r == base_r + (index_r & mask_r)` in every cycle out of reset. Run under `mbx run-dma`:
  520,041 checks pass, over 278,529 mover-owned cycles, with 0 mismatches (`receipts/t4-probe-dma.log`).
- `milan_datapath` (split): in every cycle `pp_amap_edit_req_w` is high, `enc_r ==
  amap_edit_out_encode(amap_edit_co_w, pp_amap_edit_desc_index_w)`. Run under `milan_dp split`: 143 checks pass, over
  26 req-high cycles (cluster offsets 0, 1, 2, 17 and 18), with 0 mismatches (`receipts/t4-probe-split.log`).
- `KL_aaf_clock_meter`: the replaced `grp_ts0_r` / 21-bit `grp_off_r` pair runs under the replaced conditions.
  `grp_ref_r == ts0 + off` holds in every cycle, and `pc_ts0_r` equals the old value at every group end. Run under
  `aaf_clock_meter run` (cases and servo): 465 + 6 checks pass, with 0 mismatches, over 229 meter runs and up to
  3,073 group ends in one run (`receipts/t4-probe-meter.log`).

**Reviewer plants.** `scripts/reviewer_plants.py` plants defects the PR does not, each through the suite's own
override (`receipts/rp-*.log`):

| Plant | Verdict |
|---|---|
| `KL_mbx_dma`: the start's load of `ring_addr_r` removed | caught: `D1 memory holds the record's bytes in ring order`, D2 |
| `KL_mbx_dma`: `ring_addr_r` not advanced on the to-ring branch alone | caught: `D2 the ring holds the record's words...` |
| all-fabric `milan_datapath`: the split's registered encode given to `g_af_amap_enc` | caught by `maprec8`: `[MAPREC] first boot: PP_STAT fail`, `[MAPREC] transfers: port 0 REMOVE s0.c1 SUCCESS` |
| meter: `pc_ts0_r` one PDU early (`GRP_NS_C` for `GRP_LAST_NS_C`) | not caught, and output-equivalent (below) |
| meter: `pc_ts0_r <= grp_ref_r` (no subtraction) | not caught, and output-equivalent (below) |

The two meter escapes are not a test gap. A constant offset on `pc_ts0_r` moves every pick and midpoint by the same
amount. Every output (`rate_ns_o` from `g_snap_val_r - g_snap_old_r`, the spacing from `g_pick_r - last_pick_r`,
`max_dev_ns_o` from the deviations, `status_o`, the lock and pulses) reads differences or deviations, so no output
can show it (`KL_aaf_clock_meter.sv:519-566`, outputs at 146-162). The head's value is shown exact by the meter probe
above.

## 3. The five checks the round was asked to make

1. **Each register cut is cycle-equivalent where the PR claims it.**
   - `KL_mbx_dma`:
     - Every write of `index_r` carries the matching write of `ring_addr_r`: reset at :297, the start at :318-321,
       and the answers at :335-337 (FILL_S) and :382-385 (R_S). `base_r` and `mask_r` move only at the start.
     - `host_mux` (:227-250) puts `ring_addr_r` on `host_addr_o` only while `mover_w`, exactly where the old
       `ring_addr_w` showed.
     - The probe confirms equality in every cycle. The plant `ring-address-a-step-behind` is caught by `D1` (25/25).
   - The meter reference:
     - `grp_ref_r = ts0 + off` is preserved by both of its updates (:489-511). The old 21-bit `grp_off_r` never
       wrapped: its maximum is 15 x 125,000 = 1,875,000 < 2^21, with `FS_HZ_C` fixed at 48 kHz (:173-179).
     - `pc_ts0_r = grp_ref_r - 15 x PDU_NS` equals the old `grp_ts0_r` at every group end.
     - The probe confirms both; the two plants are caught by `[M2 indep] no history restart` (38/38).
   - The edit-claim search:
     - `KL_mbx_cdc_window.sv:85-125` loads `rq_r` only on an edge that leaves the state out of REQ_S (IDLE to PRE,
       PRE to PRE, REQ to PRE, ANS to ANS/PRE/IDLE). REQ_S is entered only from PRE_S, on an edge with `in_p_w` low.
       So in every req-high cycle the fields are a clock old, and `enc_r` (`milan_datapath.sv:4642-4648`) holds
       their word.
     - In the split, `ppo_amap_edit_*` are wired straight from `i_ctl_edit_*` (:10074-10081). Those come from
       `KL_mbx_cdc` (`KL_mbx_cdc.sv:311-319`; SoC map `milan_soc.py:2964`) with no stage between.
     - The map restore, which changes the record while req stays high, is not built in the split (`g_sp_amr`, :6175,
       `amr_own_r = 0`).
     - The beat is taken in the first req-high cycle (`amap_edit_beat_w`, :4846-4849; :5150-5205), so the answer
       leaves on the cycle it did before. The window's 64-cycle bound is unchanged, and `[EDIT] each beat closes DONE
       under its own tag, not TIMEOUT` passes.
     - The window and the datapath share one reset (`milan_soc.py:872, 3273`, `~ResetSignal(milan_cd)`), so no
       req-high cycle meets `enc_r` at its reset value.
     - The all-fabric branch keeps the word combinational. My plant shows why it must: registered, `maprec8` fails.
2. **`cdc_pair_fifo` `DIST_RAM_P`.**
   - The branches differ only in `(* ram_style = "distributed" *)` (`receipts/fifo_branches.log`). Moving the write
     and read into `g_mem` keeps the base's guards (`wrst_n && wen_i && !wfull_o`; `!rrst_n` reset, then
     `ren_i && !rempty_o`), so every other user (default 0) is unchanged.
   - The render crossing's behaviour is unchanged: `tdm8render` 263/0.
   - The crossing's safety still rests on the gray pointers. Each entry is read at least two synchronizer stages after
     its write, and `wfull_o` blocks a write over an unread entry. The distributed RAM's asynchronous read of a
     settled address is safe.
   - The plant (the storage read at the write pointer) is caught by `T6 FIRST EVENT` and `T6 PRESENTATION`. The PR
     reports the first plant's survival and why, openly; it was replaced, not hidden.
3. **The plants.**
   - Ring address a step behind: caught (`mbx` mover mutants 25 of 25). The render FIFO plant: caught (full campaign:
     32 of 32).
   - No test was weakened. The changed `dma_mutants.py` anchors keep their defects:
     - `ring-index-unwrapped` now unmasks inside `ring_word`, which feeds both the start and the next address.
     - `hold-address-moves` gates both `index_r` and `ring_addr_r` on `ring_wr_w`.
   - No check, bound or expected value was relaxed anywhere in the diff.
4. **The routes** (author receipts, `author-r2/receipts/route/*/signoff.txt`). Each was checked against #818's floor
   (+0.030 / 0) at all four corners:

   | Shape | Directive | WNS / WHS, ns | Head of the route |
   |---|---|---|---|
   | 8x8/1if | ExtraPostPlacementOpt | +0.293 / +0.033 | `5d098172` |
   | 8x8/1if | ExtraTimingOpt | +0.073 / +0.029 | `5d098172` |
   | 8x8/1if | AltSpreadLogic_high | +0.058 / +0.034 | `5d098172` |
   | 1x1/1if | ExtraPostPlacementOpt | +0.081 / +0.036 | `338ece89` |
   | 1x1/1if | ExtraTimingOpt | +0.135 / +0.033 | `338ece89` |
   | 1x1/1if | AltSpreadLogic_high | +0.126 / +0.033 | `338ece89` |
   | 8x8/1if, ROM 56.5 | ExtraPostPlacementOpt | +0.213 / +0.033 | `338ece89` |
   | 1x1/1if, ROM 43.5 | ExtraPostPlacementOpt | +0.049 / +0.036 | `338ece89` |
   | release `1x1_tdm8` | integrated | +0.553 / +0.023 | `338ece89` |

   - Every route has 0 failing endpoints. The release meets its own floor (WNS >= +0.03, WHS >= 0), and
     `pp_resource_gate.py` passes.
   - The routes apply to this head. `git diff 338ece89..0297a19a` is one test file. `git diff 5d098172..0297a19a --
     hdl/` is comment lines in `cdc_pair_fifo.sv` and a generated README row.
   - The `signoff.py` line "ruling floors NOT met" grades the superseded +0.030 hold floor (6930885657), so it is not
     a miss.
5. **CPU service-budget harness.**
   - The harness's recorded inputs (`author-r2/receipts/budget/*/build.json`) are the mailbox files, `KL_mbx_dma.sv`
     among them, the CPU netlist and the SoC `sim.v`. Of those files, this PR changes only `KL_mbx_dma.sv`, which is
     cycle-identical to the base (check 1 and the probe).
   - 1x1/1if: rc 0, 96 groups, 0 refusals, 0 of 130,341 passes over the share, and the 7 `backlog-owed` probe misses,
     as at the base (`base-1x1-owed.log`).
   - 8x8/1if: rc 1 on STATED lines only. The base's `save-second` and `backlog-owed` give the same lines and the same
     durable time, 22,829.732 ms (`base-8x8-1if-r.log`).
   - The head's `save-held` / `save-starved` polls-base lines (23,756 cycles) were not re-run at the base. They fall in
     #914's polls-base class, under the base's recorded 24,499 cycles (#932 records it as 244.99 us at 100 MHz).

## 4. Findings

**R863-1-RES1** — RESIDUE — lenses: Docs, RTL — `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:310-312`
- Authority/evidence: the source comment says PDU 0's copied timestamp was held "under the hold floor". #927
  issuecomment-6930885657 sets the floor to #818's, hold 0 ns. Under that floor the base's +0.014 ns met it, as the
  same issue's re-grade records.
- Impact: wording only. No code, figure, test or verdict depends on it.
- Required outcome: replace `held it under the hold floor` with `left it about +0.014 ns of hold at the fast corner`,
  the form `cdc_pair_fifo.sv` and `KL_tdm_render_master.sv` already use.
- Verification: read the comment at the next head.

**R863-1-SUG1** — SUGGESTION — lenses: Tests, RTL — `syn/ooc/pp_resource_baseline.json` (unchanged), and
`KL_tdm_render_master.sv:368` `.DIST_RAM_P(1)`
- Evidence: the 1x1/1if hold fix rests on the render crossing mapping to distributed RAM. The resource record still
  says 74 RAMB36, so a silent revert to block RAM would pass the resource gate. Only a later route would show it.
- Required outcome (optional): the record owner re-baselines RAMB36 to 71, which the gate already recommends and
  which the PR leaves out of #927's scope. Alternatively, a structural check (for example the elaborated FIFO's
  `ram_style`) could pin the mapping.
- Verification: `pp_resource_gate.py check --endpoint route-1x1 --shipping-selection` against the new record.

**R863-1-SUG2** — SUGGESTION — lenses: Conformance, Docs — PR #939 body, section "CPU service-budget harness"
- Evidence: the claim "each is the base's" is measured for `save-second` and `backlog-owed`. For `save-held` /
  `save-starved` it is inferred, from the polls-base class and the base's 24,499-cycle record.
- Required outcome (optional): either run the base's `save-held` and `save-starved` groups, or state in the body that
  the harness's only changed input is the cycle-identical mover. The claim itself holds (section 3, check 5).
- Verification: the base runs' STATED lines `diff` empty against the head's.

Considered and not raised:
- `enc_r`'s asynchronous reset deviates from CONTRIBUTING's synchronous house rule. It matches the edit server it
  feeds (`amap_edit_commit` :5106, `amap_boot_walk` :5052) and that server's reset tree. A synchronous reset there
  would split one consumer path across two reset styles.
- The distributed RAM's write-clock-to-read inter-clock timing arc is new. The crossing's safety is structural, and
  the 1x1 and release routes have 0 failing endpoints. Their full timing reports are in the packet only as hashes
  (see limits).
- `lint_rtl_policy.py:80`'s note that `milan_datapath` has no `negedge` was already stale at the base (13 blocks).
  It is not this PR's.
- The comment-rule scan of every added line found no bench lane label, lane name, round, reviewer ID or comment ID
  in a source comment. The one comment link on an added line, `MEDIA_CLOCK_FOLLOWING.md:2498`, sits in a doc table
  and is carried over from the base.

## 5. Lens results (each with what was examined at this head)

[R863] PASS Conformance — issue #927 acceptance and rulings 6908876362, 6914223799, 6930885657, 6933111168; `author-r2/receipts/route/{h2-*,f2-*,rel2-*}/signoff.txt`; `git diff 5d098172..0297a19a`, `338ece89..0297a19a`; `author-r2/receipts/budget/units/{regrade-*,base-*}.log`; `author-r2/receipts/release/*`; `tb/verilator/milan_dp/sim_split.cpp:464-540` against IEEE 1722.1-2021 7.4.45/7.4.46 — every criterion met: three directives at both shapes under #818, the ROM spread, the release floor and resource gate, the edit path's suites and a plant per cut, and no budget row moved. EDIT and meter behaviour are cycle-exact to the base (probes).

[R863] PASS RTL — `KL_mbx_dma.sv:182-195,227-250,291-403`; `milan_datapath.sv:3526-3535,4625-4650,4846-4849,5150-5205,5669,6163-6219,10074-10081`; `KL_mbx_cdc_window.sv:85-125`; `KL_mbx_cdc.sv:311-319`; `milan_soc.py:872,2964,3273`; `cdc_pair_fifo.sv:27-131`; `KL_tdm_render_master.sv:338-380`; `KL_aaf_clock_meter.sv:173-184,306-330,414-512` — clocks and resets valid; CDC through the blessed primitives only; widths exact (21-bit offset never wraps); the FSM's field-hold property holds on every transition; no latency added; the all-fabric path is left combinational where the restore needs it.

[R863] PASS Robustness — the same RTL plus the probe runs (`receipts/t4-probe-*.log`) — reset during activity: the mover, meter and window clear together, and the window shares the datapath's reset. A newer request pre-empts only through PRE_S. A start while busy or misaligned loads nothing. The 16-bit index wraps through `ring_word` exactly as before. The meter's gaps, tu edges and jump-bound restarts were exercised with 0 probe mismatches. FIFO full and empty are unchanged. The feature-disabled path (`DIST_RAM_P = 0`, all other users) is unchanged.

[R863] PASS Tests — `split_mutants.py:83-98`, `dma_mutants.py:52-82`, `aaf_clock_meter/mutants.py:220-228`, `tdm8_render_mutants.py:123,143-153,297-309`, `sim_split.cpp:464-540,769`, `tb_split_top.sv:112-123,417-424`; runs `receipts/t1-*`, `t2-*`, `t3-*`, `t5-*`, `rp-*` — every new plant fails on the check it names at this head (29/29, 25/25, 38/38, the render arm caught). The reviewer plants are caught, or output-equivalent (meter `pc_ts0_r` offsets). No anchor was lost and no test was weakened. The `[EDIT]` checks use independent oracles: the shape's capture-source table and alternating verdicts.

[R863] PASS Docs — `docs/design/MAILBOX_SPLIT.md:311-313,1621-1633,1645`; `docs/design/MEDIA_CLOCK_FOLLOWING.md:2498` against `author-r1/receipts/area/meter-ooc-*.log` (559/617 against 574/636); `tb/verilator/milan_dp/README.md:1136,1162-1172,1189-1191`; `tb/verilator/mbx/README.md:40-45`; `docs/traceability/MODULE_MATRIX.md` (`gen_module_matrix.py --check` rc 0); `hdl/milan/milan_datapath.sv:764-768` port doc; PR body — the changed contracts are documented, the plant counts match the campaigns (29, 25, 38), and no obsolete document was restored. One RESIDUE (RES1) does not leave the lens unclean.

## 6. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #927 AC and rulings; route signoffs h2/f2/rel2; budget regrade and base logs; release receipts; `sim_split.cpp` `[EDIT]`; diffs from the route heads | R863-1 | `0297a19a056ee3d5d705bc502c4ae7808689ede7` |
| RTL | CLEAN | `KL_mbx_dma.sv`, `milan_datapath.sv` (edit encode, restore gating, split wiring), `KL_mbx_cdc_window.sv`, `KL_mbx_cdc.sv`, `cdc_pair_fifo.sv`, `KL_tdm_render_master.sv`, `KL_aaf_clock_meter.sv`, `milan_soc.py` resets; equivalence probes | R863-1 | `0297a19a056ee3d5d705bc502c4ae7808689ede7` |
| Robustness | CLEAN | the same RTL's reset, pre-emption, wrap, gap and full/empty paths; probe runs over the suites | R863-1 | `0297a19a056ee3d5d705bc502c4ae7808689ede7` |
| Tests | CLEAN | split-mutants 29/29, mbx 12/12 and 25/25, meter 38/38, render arm and full campaign, reviewer plants, anchor check | R863-1 | `0297a19a056ee3d5d705bc502c4ae7808689ede7` |
| Docs | CLEAN (RES1 carried as residue) | MAILBOX_SPLIT, MEDIA_CLOCK_FOLLOWING, the milan_dp and mbx READMEs, MODULE_MATRIX check, port doc, comment-rule scan, PR body | R863-1 | `0297a19a056ee3d5d705bc502c4ae7808689ede7` |

## 7. Real limits

- **Routes not reproduced.** No Vivado run was made here; the timing figures are the author's receipts. The full
  timing reports (and `check_timing`) are in the packet only as sha256 hashes. So the distributed RAM's inter-clock
  arc was judged from 0 failing endpoints, not read in the report.
- **CPU service-budget harness not re-run.** Section 3, check 5 rests on the author's tables, plus my proof that
  the harness's only changed input is cycle-identical.
- **Not run by me at this head:** the twin (KNOWN base lines), `dynmap`/`maprec4` positive legs and
  `dynmap-mutants`, `split-cdc` (needs the pinned sv2v and Yosys), the workflow replays, the native sweep, the
  xvlog gate, and the release firmware hash comparison. My `maprec8`/`dynmap` builds ran only with my plant. For
  these I rely on the author's receipts at `338ece89`/`5d098172`/`0297a19a`.
- **Hosted evidence at this head.** All four workflows (rtl-fast, rtl-full, docs, elaborate) were cancelled. Every
  failing context is cancellation fallout ("dependent job failed, cancelled or skipped"; "expected 19 shard
  directories, found 5"; "found 0"), not an executed test failure. The executed jobs that completed passed:
  docs-gates-0/1, docs-check-no-git, wire-accountability, elaborate gates, verilator-lint, Verilator shards 3, 11
  and 14, bdd-conformance and changes (`receipts/hosted-*`).
- **The render legs' own threads.** The campaign's leg binaries run an internal thread pool (96 threads in one
  process). That is the suite's own design and was not changed; it ran alone, beside small builds.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. No manager source bank ran at this head, and
  none is claimed.

## 8. Pending manager duties

- The current-dev merge candidate (source base `70f4056f`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`):
  builder and native banks, with receipts linked on the PR.
- Hosted and act acceptance at the exact head: a successful `rtl-fast` verdict, and exact-head `verilator-suites`
  and `yosys-portability` evidence after ready. Every one of these was cancelled at `0297a19a`.
- The composed flip train: confirm at the composed head that this PR's cut takes the
  `KL_mbx_cdc/u_edit/rq_r -> amap_edit_oclaim_expect_r / amap_out_owner_r` family off the 8x8/1if worst list, and
  that the train meets #818's floor on the best of its three directives. This head's own 8x8/1if routes put the
  datapath clock at +0.771 or better.
- Carry R863-1-RES1 to the residue checklist. Route R863-1-SUG1's re-baseline to the resource record's owner.
- The external review (R864-1) and the second positive the merge bar requires. Post-merge containment.

## 9. Packet

`REPORT.md`, `MANIFEST.sha256`, `scripts/` (`run_job.sh`, `apply_probes.py`, `reviewer_plants.py`,
`render_one_arm.py`, `render_anchor_check.py`, `fifo_branches.py`, `restore_check.sh`) and `receipts/`. The
receipts are path-sanitised: `<packet>`, `<clone>`, `<pinned-root>`, `<tools>`, `<home>` and `<tmp>` stand for host
paths. Hosted job logs are tails only. The
review clone was verified after the probes: HEAD and tree exact, the index writes the tree, every tracked file
re-hashes to its blob, there are no hidden-change entries, the five initialised gitlinks match (`external` is not
initialised in the clone), and nothing is untracked or ignored (`receipts/restore_check.log`).

R863-1 FINISHED

[R462] NEGATIVE - exact head 9e8699105c126db7764820916a827ef0538bc4b2

# R462-1: internal independent review, processor PR #155 / milan-fpga #639

- **Head:** `9e8699105c126db7764820916a827ef0538bc4b2`, tree `8c9839731f0bfbda66d3d70c4b088115324d0c66`. The clone was verified byte-exact after every probe.
- **Source base:** `5c71928ad2bf1a854a5538d69b77214dfdf1697f`. Processor `main` is now `c050d971`.
- **Scope:** area levers 3 and 6 of epic #229.
  - Lever 3: the top's eight timer arm-port queues become 4-entry distributed-RAM rings.
  - Lever 6: the ACMP listener records become distributed RAM with no read register.
  - The diff also carries two `--no-ff` merges of `main`: `83999eba` (PR #152) and `c050d971` (PR #153).

## Verdict

**NEGATIVE.** One MINOR finding is open: F1, on the Tests, Robustness and Docs lenses.

Everything else held at this head:
- Both levers are cycle-exact against `main`. Independent lockstep benches show this, including the full-queue, drop and reset paths.
- Every Vivado figure in the PR re-derives exactly from the published reports.
- Every campaign that builds the top or the listener is at its recorded count. The only exceptions are the two ADP rows that are stale on `main`, and their FAIL lines are identical on `main` `c050d971`.
- Both merges keep both sides exactly.

The open point is test completeness, not behaviour:
- The full-queue / overrun path of the new rings, and every ring state holding two or more arms, are reached by no committed test.
- A real defect planted in that path passes every committed check.
- The only evidence the PR cites for that path is a lockstep bench that is not committed and not published.

## Findings

### F1: MINOR (Tests, Robustness, Docs). The arm-port rings' full-queue path has no committed or reproducible check

**Where:**
- `tb/pp_top/sim_main.cpp:722` (`ArmQueueModel`, AQ) and `:13812` (`run_arm_queue`).
- `tb/pp_top/README.md:2009` and `:2028`.
- `tb/pp_top/acmp_mutants.py:165-168`.
- `docs/architecture/09_verification.md:393` (§8.8: "they are recorded in the issue's pull request, not kept in `tb/`").
- The new contract text: `docs/architecture/08_timing.md:119` ("an arm offered to a full queue is dropped and counted") and the banner at `hdl/top/protocol_processor_top.sv:2933`.

**Evidence:**

1. **Committed coverage stops at depth one.** At the head, the committed AQ section reports its own reach as: 71,258,305 edges; 8,270 arms; 28 clocks with two faces held; 4,288 pushes as a face's one arm left; **0** pushes onto a face still holding an arm; **0** fills; **0** drop clocks. Reproduced exactly: `receipts/lockstep_lsn/pp_top-shadow-arm-queue-only.log`, and the acmp campaign's `golden-pp_top--arm-queue-only` run.
   - The new ring logic that differs from a depth-one queue is never reached: a write at head + 2 or head + 3, the overwrite of a leaving head on a full pop+push, and the gating of a refused push.
2. **A planted defect in that path passes.** Each reviewer probe was planted into a disposable copy of the head and run with `--arm-queue-only` (`scripts/aq_probe.sh`):
   - `write_refused`: the ring is written on the offer, not on acceptance, so a refused push overwrites the head of a full queue. This is the control the author's own handoff records as surviving.
   - `wr_wrap_hi`: the write lands one entry wrong when the queue holds three or more.

   Both exit rc 0 with AQ 2 of 2 and 1,653 checks, 0 failures: `receipts/aq-probe-write_refused.log`, `receipts/aq-probe-wr_wrap_hi.log`. The reviewer's lockstep bench catches both in 8 of 8 runs (`receipts/lockstep_armq/controls-summary.txt`).
3. **The cited evidence cannot be re-run.** The PR body and 09 §8.8 rest that path on "the issue's lockstep bench". The author's handoff §12 places those benches in the author's private scratch. They are not in the tree, and not in the published evidence (milan-fpga `f0e730f8` / `28663f5a` `review-evidence/pp639-r1/`). The PR records only their results. So 09 §8.8's "recorded in the issue's pull request" is not accurate for the benches themselves.

**Impact:**
- This PR documents the overrun contract anew (08 §3), and the banner states it: drop the newest, count, keep order. That contract is now implemented by new index arithmetic.
- No committed test reaches that arithmetic. A later edit that corrupts or loses a queued timer arm under overload would pass every suite and campaign in the tree, and the result is protocol-visible (a lost or wrong timer arm).
- Equivalence at this head is not in doubt; the reviewer's own lockstep establishes it (below). That is why this is MINOR, not MAJOR.

**Decision on "is a committed check required":** yes, for these reasons:
- The repository's mutation practice (09 §8, every suite README) grades each planted control in the tree, or argues it equivalent.
- `write_refused` is a real defect, not an equivalent, and it survives every committed check.
- The bench that kills it is not available to any later maintainer.

**Required outcome:**
- Commit a check that drives at least one face full. It must cover:
  - counts 2 to 4;
  - a full queue that pops and pushes in one clock (the leaving head overwritten);
  - a refused push with its drop;
  - two faces dropping in one clock;
  - counter saturation;
  - a reset with arms queued.

  Either of these would serve: the arm-port lockstep bench as a `tb/` suite, or an AQ sub-section that drives the faces directly against `ArmQueueModel`.
- Add `write_refused` and a depth-two-or-more write-index control to `acmp_mutants.py`, each KILLED by a named check.
- Record them in `tb/pp_top/README.md` section AQ.
- Correct 09 §8.8, `tb/pp_top/README.md:2009` / `:2028` and the `acmp_mutants.py:165-168` comment, so they no longer point at an unpublished bench.

**Verification:**
- The new check fails on both reviewer edits (`scripts/aq_probe.sh` `write_refused` and `wr_wrap_hi`, or `scripts/lockstep_armq/gen.py` `--mutant`).
- It passes on the head and on `main`'s RTL.
- `acmp_mutants.py` reports the new arms KILLED.

### S1: SUGGESTION (Docs). Name the source of "1,153 flops"

`hdl/top/protocol_processor_top.sv:3002` says the shift queue "held 1,153 flops at the 1x1 shape". That is the #234 baseline's figure as issue #639 quotes it (dev `1269cdaf`). The lane's own census at its base is 1,152 `armq_r` flops (PR body; handoff §5.5). Naming the revision would stop the two readings looking inconsistent. This does not affect the verdict.

### Prior public findings

PR #155 had no review, no review comment and no finding before this round. Its three comments are the evidence note and two review-start notes. Issue #639's comments are the assignment, TAKEN and REVIEW READY. Nothing is carried in to resolve or retain.

## Evidence by lens

### Conformance: CLEAN

- No port, parameter or register change:
  - The top's port list does not change.
  - The listener's module header is byte-identical between `main` and the head (checked by `scripts/lockstep_lsn/gen_shadow.py`, which refuses differing headers).
  - Snapshot word 24 (the drop counter) keeps its rule. One rise per clock is the landed behaviour; it is recorded out of scope.
- Timer expiry order and latency are unchanged in every cycle:
  - The drain order, the 4-deep per-face depth, newest-dropped-and-counted, and arm-port register timing are identical in the lockstep runs below.
  - The listener consumes each record in the same cycle as on `main`.
- "Relates to milan-fpga#639" is right: the acceptance's "resource gate's baseline is re-recorded in the same reviewed change" lives in the parent's `syn/ooc/pp_resource_baseline.json`. "Relates to milan-fpga#229" is right too.

### RTL: CLEAN

**Arm-port rings** (`protocol_processor_top.sv:2994-3046`):
- A push writes at old head + old count (mod 4). That is the append position whether or not the same clock pops, because after a pop the survivors are at head+1 .. head+count-1.
- With count 4 and a pop, the write lands on the leaving head. The read is asynchronous and the arm-port register samples it before the write lands, both in simulation and in a RAM32M (synchronous write, asynchronous read).
- A refused push (count after the pop = 4) does not write.
- The unreset entries are read only after a post-reset push wrote them: count and head reset, and the first push writes `mem[head + 0]`.
- A push accepted during reset writes an entry that is overwritten before it can be read.

**Listener records** (`KL_pp_acmp_listener.sv:379-412`, `:746`, `:1033-1079`):
- `sink_r` is written only in reset and X_IDLE.
- X_STRT_AP and X_LATCH are entered only from X_STRT_RD and X_RDREC.
- `recwr_en_w` is true only in X_INIT, X_PRELOAD and X_WB.
- So the asynchronous read in the consuming state equals the read-first register value of one edge earlier. `rec_rd_w` has no other consumer.

**Inference** at all three endpoints, from the published logs:
- `g_armq[k].mem_r_reg | User Attribute | 4 x 47 | RAM32M x 8`; 4 x 48 at 8x8.
- `u_listener | rec_ram_r_reg | User Attribute | 2 x 376 | RAM32M x 63`; 16 x 376 at 8x8.
- No `armq_r_reg` cell remains at the head.
- The base shows `2 x 376(READ_FIRST) ... | 1 | 5` block RAM.

**Lint and merges:**
- Lint with the repository's own flags, pinned simulator 5.050: `protocol_processor_top` and `KL_pp_acmp_listener` rc 0, no warnings (`receipts/static/lint-*.log`).
- Each merge's tree equals `git merge-tree --write-tree` of its parents (`993fbd72…`, `8c983973…`).
- `git diff c050d971 9e86991` equals the lane's own `git diff 5c71928 cfd62e8` line for line (hunk offsets aside).
- `git diff cfd62e8 9e86991` equals `git diff 5c71928 c050d971` the same way.
- Both sides are kept. The lane's RTL and test files are byte-identical through both merges.

### Robustness: UNCLEAN (F1)

**Arm-port lockstep** (reviewer-written, `scripts/lockstep_armq/`). `main`'s block is cut byte for byte from `5c71928a`'s top, beside the head's block, on identical random arms. Settings: uninitialised state randomised; resets of 1 to 4 clocks taken mid-run with arms still offered.

- 32 runs x 1,000,000 cycles, slot widths 5, 6 (1x1), 7 (8x8) and 8, distinct seeds: **0 mismatches**. Coverage:

  | Event | Count |
  |---|---:|
  | arms issued | 29,779,244 |
  | offers to a full face, dropped | 105,284,606 |
  | drop clocks | 22,032,432 |
  | clocks with two or more faces dropping | 19,218,883 |
  | full-queue pop+push clocks | 3,906,290 |
  | resets | 1,033 |
  | offers during reset | 2,471 |
  | runs reaching counter saturation | 27 of 32 |

  Receipts: `receipts/lockstep_armq/equivalence.txt` and `equivalence-summary.txt`.
- Nine planted controls, 8 seeds x 1,000,000 cycles each:
  - Caught in 8 of 8: `write_refused`, `wr_at_head`, `wr_at_mid`, `head_stuck`, `read_tail`, `ring_of_three`, `full_pop_refuses`, `wr_wrap_hi`.
  - Caught in 7 of 8: `drop_skip_sat`. The eighth seed never saturates the counter (`sat_clocks 0`), so it has nothing to see.
  - `hd_not_reset` is an equivalence probe: 0 of 8, as expected.
  - Receipts: `receipts/lockstep_armq/controls.txt` and `controls-summary.txt`.

**Listener lockstep** (reviewer-written shadow, `scripts/lockstep_lsn/`). `main`'s listener and the head's sit side by side under the suite's own top name, driven by the suites' own stimulus. Every output, `rec_r`, `xs_r` and (in the consuming states) the record read bus are compared at every edge.

| Run | Edges | Mismatching edges | X_LATCH reads | X_STRT_AP reads | Reset edges |
|---|---:|---:|---:|---:|---:|
| `tb/acmp_listener` (8 sinks; 3,111 of 3,111 checks pass inside it) | 46,168 | 0 | 509 | 8 | 8 |
| `tb/pp_top --arm-queue-only` (top shape, main harness) | 71,258,485 | 0 | 49 | 13 | 180 |
| `tb/pp_top --acmp-only` | 1,892,463 | 0 | 18 | 0 | 20 |

The other harness models in those runs also show 0 mismatching edges. Controls:
- `read_in_idle` (the stale read): 19,977 mismatching edges, and the suite fails RV8.
- `read_write_first` (a write-through bypass in the consuming cycle) is an equivalence probe: 0. This confirms that no record write coincides with a consuming state.
- Receipts: `receipts/lockstep_lsn/`.

**Reset of the unreset RAM:**
- RS passes, and kills `rec_sweep_misaddressed` (37 of 3,111), in this round's campaign.
- The arm rings hold no reset dependency: see the 1,033 mid-run resets with randomised entries above.

**Not proven in the tree:** the full-queue path. That is F1.

### Tests: UNCLEAN (F1)

**`acmp_mutants.py --jobs 4`** (`receipts/campaigns/acmp_mutants.log`, `acmp_results.json`): rc 0.
- 29 of 29 KILLED; four goldens PASS: `acmp_listener`, `pp_top --acmp-only`, `pp_top --arm-queue-only`, `rx_validator`.
- Every arm fails exactly its README count:
  - The ten #639 arms: `rec_read_sink_zero` 645 of 3,080; `rec_read_in_idle` 1; `rec_started_unstored` 91; `rec_settled_vlan_unstored` 25; `rec_sweep_misaddressed` 37; `armq_read_tail` 71; `armq_head_stuck` 2; `armq_ring_of_three` 11; `armq_write_at_head` 2; `armq_write_at_mid` 2.
  - The 19 earlier arms, at their records, with totals of 3,111 and 3,107 checks as the listener README says.
- The keying of one golden per run mode (`5828bb8`) is exercised: four goldens ran.

**Every other campaign that builds the top or the listener**, from an export of the exact head, each with its own log and rc (`receipts/campaigns/`):

| Campaign | rc | Result | Against the record |
|---|---:|---|---|
| `notify_mutants.py` | 0 | 47 of 47 KILLED, goldens PASS | 47 of 47 at count |
| `ctr_mutants.py` | 0 | control PASS, 17 KILLED (18 checks) | 17 of 17 |
| `aecp_mutants.py` | 0 | 60 checks: 5 controls, 55 KILLED | 55 of 55 |
| `aecp_dispatch_mutants.py` | 0 | 44 checks: 4 controls, 40 KILLED | 40 of 40 |
| `d3_mutants.py --jobs 3` | 0 | 110 of 110 KILLED, goldens PASS | 110 of 110 (`validator_admits_held_aecp` against `tb/rx_validator` M4, 4) |
| `gsi_mutants.py` | 0 | 20 detected by named checks; golden and restored PASS | as recorded (no counts) |
| `name_wr_mutant.py` | 0 | decode killed; golden and restored PASS | as recorded |
| `tb/maap/mutants.py` | 0 | 32 checks: 3 controls, 29 KILLED | 29 of 29 ("N FAIL of M" rows; pp_top arms 5 and 4 of 34) |
| `tb/adp_engine/mutants.py` | 0 | 43 checks: 2 controls, 41 KILLED | 39 of 41; the two stale rows below |

The two stale `tb/adp_engine` rows:
- `cfg-valid-no-reset` fails 9 against the README's 5; `gate-enable-dropped-top` fails 7 against the README's 3. That README cell itself notes 7 at the head of lane P1.
- Both re-run on `main` `c050d971` give byte-identical FAIL lines (`receipts/campaigns/adp_mutants-main-c050d971-two-arms.log`). The records are stale on `main`, not changed by this lane.

**Committed tests:**
- AQ checks the arm port and drop counter against an independent eight-FIFO model after every edge. It passes and kills its five controls.
- RS grades the X_INIT sweep through the RAM, and kills `rec_sweep_misaddressed`.
- AQ's model also states the drop rule correctly; the reviewer's lockstep confirms it.
- The gap is F1.

### Docs: UNCLEAN (F1)

Checks run on the head export (`receipts/static/`):

| Check | rc | Result |
|---|---:|---|
| `check-links.py` | 0 | 1,123 links |
| `check-matrix.py` | 0 | 115 REQ rows |
| `gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `check-integrator-params.py` | 0 | 28 parameters |

Checked against the measurements:
- 07 §6, 08 §3 and `docs/guides/hdl-engineer.md` §3.1. The µCPU operand file is indeed distributed RAM read asynchronously: `KL_aecp_ucpu.sv:159`.
- The listener README: 3,111 checks, and the five #639 rows' counts.
- The `tb/pp_top` README AQ coverage figures and control counts.

09 §8.8, the AQ README and the `acmp_mutants.py` comment point the full-queue proof at a bench that is not available (F1).

## Vivado figures, re-derived

Sources:
- The published reports at milan-fpga `28663f5a`, `review-evidence/pp639-r1/author-r1/vivado/`. All 63 MANIFEST entries hash to their `published_sha256`, and no file is unlisted.
- Re-derived with `scripts/vivado/rederive.py`; output in `receipts/vivado-rederive.txt`.

| Endpoint | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | WNS / WHS ns |
|---|---|---|---|---|---|---|
| route 1x1 | 51,434 -> 51,152 (-282) | 59,691 -> 58,598 (-1,093) | 15,847 -> 15,803 | 79 -> 74 / 27 -> 27 | 14 | +0.079 / +0.014 -> +0.093 / +0.036 |
| ooc 1x1 | 24,930 -> 24,648 (-282) | 25,465 -> 24,278 (-1,187) | - | 21 -> 16 / 3 | 8 | -2.059 -> -0.743 (estimate) |
| ooc 8x8 | 32,584 -> 32,154 (-430) | 34,211 -> 32,858 (-1,353) | - | 26 -> 21 / 5 | 8 | -2.161 -> -2.153 (estimate) |

**Route:**
- LUT as logic 49,158 -> 48,450; LUT as memory 2,276 -> 2,702.
- Both routes are complete with 0 routing errors (107,053 and 105,954 nets).
- Global routing ran iterations 0 to 6 at the base and 0 to 1 at the head, matching "seven" and "two".
- The four sign-off "operating" files are operating-condition metadata, identical in base and head and Slow = Fast by design. The grade file says so. They carry no timing.

**Per block** (hierarchy reports):

| Scope | route | 1x1 | 8x8 |
|---|---|---|---|
| top's own logic `(u_pp)`, LUT (LUTRAM) | 390 (0) -> 654 (218) | 447 (0) -> 769 (246) | 465 (0) -> 880 (256) |
| top's own logic `(u_pp)`, FF | 2,968 -> 1,972 | 3,167 -> 2,034 | 4,735 -> 3,433 |
| `u_listener`, LUT | 1,301 -> 1,496 (+195) | 1,434 -> 1,557 (+123) | 1,630 -> 1,668 (+38) |
| `u_listener`, RAMB36 | 5 -> 0 | 5 -> 0 | 5 -> 0 |

- The engines at 1x1: `u_notify` -201, `u_originator` -136, `u_adp` -109, `u_maap` -87, `u_srp` -87, for **-620** in total.
- Wrapper `pp_shadow` (route): LUT 24,485 -> 24,516.
- Lever 3's LUT saving at 1x1: -282 - (+123) ≈ -405, which matches "about -400".
- The routed LUTRAM counts fit the cell census claims: 218 = 54 RAM32M x 4 + 1 RAM32X1D x 2; 208 = 52 RAM32M x 4.

**Gate policy** (`scripts/vivado/gate_policy.py`, `receipts/vivado-gate-policy.txt`). This applies dev `241f9184`'s `pp_resource_baseline.json` tolerances and `judge()` rules. Every exit status and re-baseline list in the PR re-derives:

| Endpoint | head vs base | base vs committed record | head vs committed record |
|---|---|---|---|
| route 1x1 | exit 0, re-baseline recommended (FF, RAMB36) | exit 1, LUT +667 over 500 | exit 0, re-baseline recommended (FF, RAMB36) |
| ooc 1x1 | exit 0, re-baseline recommended (LUT, FF, RAMB36) | exit 1, LUT +598 | exit 1, LUT +316 over 250 |
| ooc 8x8 | exit 0, re-baseline recommended (LUT, FF, RAMB36) | exit 1, LUT +1,028 | exit 1, LUT +598 over 316 |

The gate's identity and input-digest checks need the scratch parent and were not re-run.

Note: the Vivado head is processor `9eebc61`, as the PR body states, not `9e86991`. The final head also carries PR #153's `KL_aecp_notify` change, which neither the base nor the head measured. The figures are therefore the lane's own delta. The parent re-baseline must be measured at the adopted pin.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #639 body and assignment comment 5976100204; the top's port list and the listener's header at `main` vs head; drain order, depth, drop rule; closing keywords | R462-1 | `9e8699105c126db7764820916a827ef0538bc4b2` |
| RTL | CLEAN | `hdl/top/protocol_processor_top.sv:2924-3046`, `hdl/acmp/KL_pp_acmp_listener.sv:379-412,744-771,914-1079`; Vivado mapping lines (3 endpoints x base/head); lint of both tops; both merges (`git merge-tree`, patch identity) | R462-1 | `9e8699105c126db7764820916a827ef0538bc4b2` |
| Robustness | UNCLEAN (F1) | reviewer arm-port lockstep (32 x 1M, 9 controls + 1 probe); listener shadow lockstep (3 runs + 2 probes); reset paths; in-tree probes `write_refused`, `wr_wrap_hi` | R462-1 | `9e8699105c126db7764820916a827ef0538bc4b2` |
| Tests | UNCLEAN (F1) | `tb/pp_top` AQ, `tb/acmp_listener` RS; acmp, notify, ctr, aecp, aecp_dispatch, d3, gsi, name_wr, maap, adp campaigns at head, every arm against its README record; two ADP arms on `main` `c050d971` | R462-1 | `9e8699105c126db7764820916a827ef0538bc4b2` |
| Docs | UNCLEAN (F1) | 07 §6, 08 §3, 09 §8.8, hdl-engineer §3.1, `tb/pp_top/README.md` AQ, `tb/acmp_listener/README.md`, PR body, code comments; links/matrix/params checks | R462-1 | `9e8699105c126db7764820916a827ef0538bc4b2` |

## Real limits

- **The author's lockstep benches were not available** (author scratch). The reviewer wrote independent ones.
  - The arm-port bench uses `main`'s block cut from `5c71928a` (the same cut rule).
  - The listener bench uses the two suites' own stimulus, not random faces. It covers 8 sinks and the top's shape, not 1, 3 or 9 sinks; for those, equivalence rests on the structural argument above, which does not depend on N_SINKS_P.
  - X_STRT_AP was exercised 21 times in total.
- **Vivado was not re-run.** The figures are re-derived from the published reports. The author's cell census (`baseline_cells.tsv`) and gate `compare.json` are not published. RAM32M counts are checked only for consistency with the LUTRAM counts, and gate verdicts only through the tolerance policy.
- **Not run (out of this reviewer's allowance):** `run_suites.sh`, `syn/yosys/run.sh`, the full `tb/pp_top` five-build `make`, and the parent consumer set.
  - Focused suites run: `tb/acmp_listener` (3,111 checks), and `tb/pp_top` `--arm-queue-only` and `--acmp-only` (campaign goldens and shadow runs).
- **Per-arm count comparison** used small parsers over the README tables (`scripts/compare_counts.py` and inline checks; outputs in `receipts/campaigns/*counts*`). Rows grouped under one name were checked by hand.
- **Redaction:** in three listener-shadow logs, a home-directory install prefix of the pinned simulator was replaced by `<VERILATOR_ROOT>`. Nothing else in the receipts was edited.
- **Shared host:** other lanes' jobs ran on the host throughout. This unit's memory reached its 12 GB limit through reclaimable cache, with 0 OOM kills (`memory.events`). Every campaign's goldens passed.

## Pending manager duties

- **Parent consumer set of 17 at dev `fea346e7` + c8, p2-p1, c10 and the #232 adoption patches:** gate 16 is expected to pass now that #643 is fixed. This review did not run it.
  - The author's run was at dev `241f9184`, where gate 16 failed T30 identically to `main`.
- **The resource gate's baseline re-recording at the adoption pin** (the acceptance's "same reviewed change"). Re-measure there: this PR's figures exclude PR #153's `KL_aecp_notify` change.
- **PR #153's xvlog finding banked in the parent** (`scripts/xvlog.budget`) when the pin moves past `c050d971` (#232's adoption line).
- **Hosted CI at the exact head:** `portability` and `docs-gates` succeeded in both workflow runs (`37203780628`, `37203777361`). Both `suites` jobs were still in progress when read (`receipts/github/checkruns.json`). Hosted and act acceptance belong to the manager.
- **The final current-dev candidate build at the merge turn** (source base `5c71928a`, live dev `fea346e7`).
- **Physical calibration NOT RUN.** No hardware was used; field skips are not hardware proof.

R462-1 FINISHED

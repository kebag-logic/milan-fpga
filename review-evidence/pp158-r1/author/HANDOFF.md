# [A541] #158 lane handoff (pp158-dereg-round)

## Round 1b (resume after the area ruling)

Status: **REVIEW READY** with head `79571006b803a4ab4af65358f0d87bc3af73180e`. Posted on #158 (comment 5999645465,
2026-10-05 17:29 UTC). PR-BODY.md says "Closes #158": the ruling puts the change within the area limit, and every acceptance
item of #158 is met. Nothing was pushed; no PR was opened. The lane tree is clean (`git status --porcelain --ignored` empty).

- Ruling: issue #158 comment 5997990838 (2026-10-05 15:50 UTC). The change is within the area limit, because the limit counts the
  change's own logic. Variance in modules with unchanged RTL is recorded, not counted. The PR body states both figures (whole
  OOC delta with the per-row table, and the own-logic delta).
- Merge: `7957100` (`79571006b803a4ab4af65358f0d87bc3af73180e`), `git merge --no-ff` of main `21c6f709` (C11, PR #156) on
  top of `e3c9f0b5`. One-line subject, no body. No conflicts (09 auto-merged). No rebase, no amend, not pushed. No further
  notify edit was made, so no new pre-edit grep was needed. C11 does not touch `KL_aecp_notify.sv`, and no arm names a file
  C11 changed (`git grep` of every `tb/**/*.patch` and `tb/**/*.py` for the four changed source files: no match).
- Scratch: `$VALIDATION_STORAGE/pp158-a541/r1b` (`logs/`, `camp/`, `pgates/`, `iso/`, `scripts/`). Relative log paths in this
  section are under it.

### 1b.1 The merge changes neither delta

- `git diff 054d01c e3c9f0b5` and `git diff 21c6f709 7957100` (the lane's delta) have the same patch-id (`7fee3918...`). Their
  only textual difference is two hunk offsets in `09_verification.md` (+10 lines from C11).
- `git diff 054d01c 21c6f709` and `git diff e3c9f0b5 7957100` (C11's delta) have the same patch-id (`dd11bb40...`).
- C11's source edits are comment-only. `verilator -E -P` (pinned 5.050) of `KL_pp_side_port.sv`, `KL_pp_trace_ring.sv` and
  `KL_pp_tx_slots.sv` gives byte-identical output at `e3c9f0b5` and `7957100`. `gcc -fpreprocessed -dD -E -P` of
  `tb/tx_slots/sim_main.cpp` is byte-identical too. The three RTL files keep their line counts. So no synthesis or simulation
  input changes. The OOC 1x1 (round 1, section 5) was not re-run.

### 1b.2 Every arm plants at the head

| Check | `054d01c7` | `e3c9f0b5` | `21c6f709` | `7957100` |
|---|---|---|---|---|
| `plant_check.py`: every `tb/**/*.patch` (`git apply --check`), every notify/d3/acmp exact-text arm (driver's `plant()`) | 473 of 473 | 476 of 476 | 473 of 473 (list identical to `054d01c7`) | **476 of 476** (list identical to `e3c9f0b5`) |
| `scripts/text_anchor_check.py` (new): the other text drivers' arms under each driver's own count rule (acmp_talker retry 70 + 2 bench probes, gsi 20, name_wr 1, srp_admission 3) | 96 of 96 | 96 of 96 | 96 of 96 | **96 of 96** |

`text_anchor_check.py` fails when an anchor moves: with `name_wr_mutant.py`'s anchor perturbed by one space in a scratch copy, it
reports `REFUSED tb/pp_top/name_wr_mutant.py:decode (anchor count 0 != 1)`, rc 1 (`logs/text-anchor-selftest.log`).
`tb/desc_store/lint_mutations.py` edits descriptor models, not sources, so it has no anchor. Logs: `logs/plant-check-{base,head}.log`,
`logs/text-anchor-*.log`.

Planted-design identity (round 1, 54 notify-planting arms) carries over: `KL_aecp_notify.sv`, every patch and every mutant
table are byte-identical between `e3c9f0b5` and `7957100`, and between `054d01c7` and `21c6f709`.

### 1b.3 Gates, base `21c6f709` vs head `7957100`

All rc 0, unpiped, pinned Verilator 5.050, in `git archive` extractions except the in-tree docs gates.

| Gate | Base `21c6f709` | Head `7957100` | Record |
|---|---|---|---|
| `make ids` (in the tree) | 30 self-test cases; 531 files, 91 IDs, F01.5 47 P-IDs, F08.1 36 T-IDs | the same | logs identical |
| `make check` (in the tree) | lint 41 Mermaid + 18 WaveDrom; WaveDrom 18; links 1,168; 115 REQ, 17 GAP; 94 rows, 0 untested; 28 parameters; ids as above; figures 17 self-test cases, 3 draw.io + 18 WaveDrom + 5 hand-authored; staleness | the same | logs identical |
| `python3 scripts/gen_matrix.py --check` (in the tree) | 94 rows, 0 untested | the same | identical |
| `./scripts/run_suites.sh` | 33 suites, 1,021,640 checks, 0 failing | 33 suites, 1,021,651 checks, 0 failing | base log byte-identical to `054d01c7`'s; head log byte-identical to `e3c9f0b5`'s |
| `tb/pp_top` `make` (six builds), each in its own extraction | 10,444 (9,956 / 20 / 178 / 231 / 56 / 3) | the same | 82 graded lines identical at base, head and both round-1 runs (the fresh build adds compiler warning context, filtered) |
| `tb/aecp_notify` `make` | 34 (30 + 4) | 45 (41 + 4) | each log identical to its round-1 counterpart but for Verilator's timing line |
| `./scripts/lint_hdl.sh` | 41 `LINT OK` | 41 `LINT OK` | logs byte-identical to each other and to round 1 |
| `./syn/yosys/run.sh` | 42 `YOSYS OK` + 1 `YOSYS XILINX OK`, `all.v` parsed once | the same | byte-identical to each other and to round 1 |
| `notify_mutants.py --jobs 2` | 53 of 53 KILLED, goldens PASS | 56 of 56 KILLED, goldens PASS | base: 61 of 61 per-arm files identical to `054d01c7`'s; head: 64 of 64 identical to `e3c9f0b5`'s; the base-vs-head difference report is byte-identical to round 1's |
| `ctr_mutants.py --jobs 2` | control PASS, 17 of 17 KILLED | the same | 113-line driver logs and 18 of 18 per-arm files identical (base vs head, and each vs round 1) |

The three controls at `7957100` (`camp/head/notify`): `dereg_mid_round_no_hold` fails DR1, DR2, DR3 (`41 checks, 3 failures`);
`dereg_pending_stops_follow` fails DR3 (D's next at ms 31512, 8 ms after D's send; `1 failures`); `dereg_lost_at_round_end` fails
DR1b and DR2b (`2 failures`).

**A raced run, re-run.** The first head `tb/pp_top` `make` ran in the same extraction as the head suites, whose `pp_top`
suite runs the same `make` there. Both appended to `obj_dir/build_tally.txt`, and the full make failed (rc 2) with
`FAIL: 12 build tallies, expected 6` (`logs/head-pp_top-full-raced.log`). That was my scheduling, not the design. The suites'
own `pp_top` passed in that run (10,444). The head suites and both `tb/pp_top` makes were then re-run, each in a fresh
extraction (`iso/`) with nothing else in it. Those are the records above. The raced suites log is byte-identical to the clean
one. The campaign drivers copy their trees to temporary directories, so they were not exposed.

**Not re-run** (the ruling scopes the re-measurement to what C11 feeds; their inputs at the merged head differ from round 1's only by
the comment-only edits of 1b.1, and every arm plants): the d3, aecp, aecp_dispatch, acmp, gsi, name_wr, adp and maap
campaigns, the OOC 1x1, and parent gates 10, 15 and 16.

### 1b.4 Parent consumer set, pins `21c6f709` and `7957100`

Same scratch parent (dev `fa450d30`, the five patches, uncommitted), pin moved by `switch.sh` (toplevel checks first). A stale
`hdl/aecp/desc/__pycache__/` (ignored, from round 1) was removed from the scratch parent's processor worktree first.

| # | Gate | Base `21c6f709` | Head `7957100` | Record |
|---:|---|---|---|---|
| 1-8, 3b, 11 | `pgates.sh light` | rc 0 | rc 0 | identical at both and to round 1, except gate 2's line count: 317 modules, 200,087 to 200,111 lines (`notify_mutants.py` +24; C11's script changes add 2 modules and 550 lines at both) |
| 13 | `nvm_cosim lint` | rc 0 | rc 0 | identical but for Verilator's timing lines |
| 12 | `pp_shadow -j8` | rc 0; legs 606, 606, 646, 311, 0 failures | the same | 2,169 `[PAS` markers and 0 `[FAIL]` at both. The complete `[PASS]` token count (2,168 / 2,167) varies because `-j8` compiler output splits some tokens; round 1 counted 2,167 at both |
| 14 | `nvm_cosim quick` | rc 0; 315 of 315 | the same | graded lines identical to each other and to round 1 |
| 9 | `flock $VIVADO_LOCK xvlog_gate.py --check` | rc 0, 1,109 s (mostly waiting for the lock); PASS, 2 findings == ratchet | rc 0, 1,574 s (the same) | logs identical to each other and to round 1 but for the pinned sha line. Nothing else of the lane ran during either run |

## Round 1 (STOP, ruled within the limit)

## Round 1 (STOP, ruled within the limit)

Status: **STOP (item 4, area).** The OOC 1x1 `KL_pp_shadow` delta is **+50 LUT** (-6 FF), above the assignment's 40 LUT stop.
The lane's own block does not grow: the `u_notify` row moves -1 LUT and -3 FF, and `KL_aecp_notify` synthesized alone moves
-3 LUT and +2 FF. The +50 sits in rows whose RTL is unchanged (section 5). Every other gate is green and every other record is
identical except the ones the new check names. STOP posted with the head on #158 (comment 5997973952, 2026-10-05 15:49 UTC);
the area ruling is the manager's. Nothing was pushed; no PR was opened.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, branch `pp158-dereg-round`.
- Base: `main` 054d01c79e59c3f80454ad9cdefd8e914b540bb4 (#148 merged). Head: e3c9f0b5facc7ff7a0092c72e5d40319741736b3 (not pushed).
- Assignment: issue #158 comment 5991577974. TAKEN: issue #158 comment 5991597818 (2026-10-05 09:18 UTC).
- Pinned Verilator 5.050 (wrapper sha256 905795b9...e92f), exported on PATH; the host default 5.052 was not used.
  A local wrapper admits three Verilator builds at once and sets the C++ build's `-j 0` to `-j 8`. It changes only build parallelism.
- Scratch directory: `$VALIDATION_STORAGE/pp158-a541` (`logs/`, `camp/`, `pgates/`, `meas/`, `scripts/`, the scratch parent `parent/`).
  Every relative log path below is under it.
- Every gate ran in `git archive` extractions of base and head, outside the tree. The lane tree was used only for
  `make check` and `gen_matrix.py --check` (both need git). After every run, `git status --porcelain --ignored` was empty.

## Commits (base..head)

| Commit | What |
|---|---|
| `5343cd7` | Item 1, red first: `tb/aecp_notify` section DR (DR1, DR1b, DR2, DR2b, DR3), bench only |
| `27992ce` | Item 2, the fix: `KL_aecp_notify.sv` (+7 -3, one logic line) and 06 section 7 |
| `3dbc229` | The three controls in `tb/pp_top/notify_mutants.py` |
| `e3c9f0b` | The READMEs (`tb/aecp_notify`, `tb/pp_top` notify record), 09 section 8.4, and a 06 reflow |

## 1. Red run at main

The check was committed first (`5343cd7`, bench only). Its `KL_aecp_notify.sv` is byte-identical to `main`'s. `make run` in
`tb/aecp_notify`, rc 2: `[build default] 41 checks, 3 failures`. The DR1b and DR2b checks pass on `main`.

```
  [i] DR1: after the drain, ms 20009: kind 0, 0000:0, args 0/0, seq 1, to 020000000003
  [i] DR1: after the drain, ms 20013: kind 0, 0000:0, args 0/0, seq 0, to 020000000004
FAIL: DR1: in a GET_COUNTERS round on 0009:0, C's registration expires while its job waits, and the round's remaining controller D still receives the round's GET_COUNTERS 0009:0 (2 jobs after the drain)
  [i] DR2: after the drain, ms 25008: kind 0, 0000:0, args 0/0, seq 1, to 020000000003
  [i] DR2: after the drain, ms 25012: kind 0, 0000:0, args 0/0, seq 0, to 020000000004
FAIL: DR2: in a SET_NAME round on 0005:1 (arguments 2 and 3), C's CONTROLLER_AVAILABLE retry fails while its job waits, and the round's remaining controller D still receives the round's notification (2 jobs after the drain)
  [i] DR3: the job after the drain (kind 0 to 020000000003) sent at ms 31504; D's GET_COUNTERS sent at ms 31513 and next presented at ms 0
FAIL: DR3: C's registration expires in a GET_COUNTERS round, the job after the drain waits for the TX slot until ms 31504 and a change arrives at ms 30104: D's GET_COUNTERS sent at ms 31513, the next at ms 0, want 32513 to 32521 (1 of D's GET_COUNTERS seen)
[build default] 41 checks, 3 failures
```

DR1 is the issue's probe (`evidence/probe-dereg-mid-round.diff`, kebag-logic/milan-fpga `1de9179a`). It reproduces the probe's trace
exactly: C gets its DEREGISTER (seq 1), and D gets kind 0, 0000:0 (seq 0).

## 2. The change

`hdl/aecp/KL_aecp_notify.sv`, one logic line. The rest is comments.
- `:1253`: `if (dh_v_r) begin` becomes `if (dh_v_r && !em_active_r) begin`. A drained DEREGISTER now waits for the round's boundary.
  Until then, `N_IDLE` takes the round's next job (the existing `else` arm, `wk_ix_r <= em_ix_r`), so `em_kind_r`, `em_dt_r`,
  `em_di_r` and `em_arg*_r` are never rewritten mid-round. After the round's last job (`em_active_r` falls in `N_EMIT_WB` or
  `N_EMIT_RD`), the DEREGISTER still goes before any new round's claim. Its arm is checked first, as before.
- `:1254-1257`: the comment on that arm. `:129-130`: the banner's DEREGISTER sentence.
- 06 section 7 (`docs/architecture/06_aecp_engine.md:887-889`) gains one sentence.

**Why hold rather than save/restore.** The assignment allows either. A save/restore of `em_kind_r`, `em_dt_r`, `em_di_r` and
`em_arg0/1_r` needs 68 more flops. That is above the 60 FF stop on its own. The hold is a single gate on an existing condition.

**The targeted controller's own DEREGISTER semantics are unchanged.** It still goes to that controller alone, with the tuple and
sequence_id latched at drain (`dh_*`), kind 0, 0000:0, args 0. Its frame is built from the same `em_*` constants. Only its time
moves: from right after the drain to right after the round's remaining jobs (at most `P-N-CONTROLLERS` - 1 jobs).

**#148's rule and R477-1 S2.** With the hold, no DEREGISTER job runs inside a round. So the GET_COUNTERS stamp follows every job of
the round to its send, as #148 made it, and nothing interleaves to stop it. DR3 grades this. In a GET_COUNTERS round, C's
registration expires, the next job waits 1.5 s for the TX slot, and a change arrives in that wait. D's next GET_COUNTERS must be
presented 1,000 to 1,008 ms after D's send. The control `dereg_pending_stops_follow` stops the follow while the DEREGISTER is
pending, which is S2's hazard in this design. It fails DR3 at ms 31512, 8 ms after D's send.

No port, register or parameter changed. The module header is untouched by the diff.

## 3. Tests and their failing mutants

`tb/aecp_notify` section DR (`sim_main.cpp:540-702`), 11 checks: the five named checks below plus six REGISTER checks. The checks
accept D's job and C's DEREGISTER in either order, so they grade the outcome, not the order the fix chose.

| Check | What | Failing control(s) at head |
|---|---|---|
| DR1 (`:613`) | GET_COUNTERS round 0009:0; C's TIME_LIMITED expiry while its job waits; D still gets the round's GET_COUNTERS | `dereg_mid_round_no_hold` |
| DR1b (`:618`) | C alone gets its own DEREGISTER (kind 0, 0000:0, seq 1), once | `dereg_lost_at_round_end` |
| DR2 (`:654`) | SET_NAME round 0005:1, args 2/3; C's failed CONTROLLER_AVAILABLE retry; D still gets the round's notification | `dereg_mid_round_no_hold` |
| DR2b (`:659`) | as DR1b | `dereg_lost_at_round_end` |
| DR3 (`:696`) | TW with the drain (R477-1 S2): D's next GET_COUNTERS a second after D's send | `dereg_mid_round_no_hold`, `dereg_pending_stops_follow`, and #148's three TW controls |

Controls (`tb/pp_top/notify_mutants.py:330-353`), driver run at the head:

| Control | Planted | Failing checks |
|---|---|---|
| `dereg_mid_round_no_hold` | `if (dh_v_r) begin`, `main`'s rule (the "no restore" mutant) | 3: DR1, DR2, DR3 |
| `dereg_pending_stops_follow` | the stamp's follow gated with `&& !dh_v_r` | 1: DR3 (ms 31512) |
| `dereg_lost_at_round_end` | the round's last write-back also clears `dh_v_r` | 2: DR1b, DR2b |

## 4. Pre-edit git grep and planting

Before the RTL edit, every changed line and its neighbours (`:128-130`, `:1251-1254` at `5343cd7`) was searched across
`tb/**/*.patch` and every `tb/**/*.py` table. There were no matches (`logs/pre-edit-grep.log`). No reviewed patch has a hunk
near either edit.

Plant check (scratch script; each patch through `git apply --check` at an extraction root, and each exact-text arm of the notify,
d3 and acmp drivers through the driver's own `plant()`):
- base: 473 of 473 plant;
- head: 476 of 476 plant: the same 473 plus the three new controls.

Planted-design identity: all 54 arms that plant into `KL_aecp_notify.sv` (10 patches, 42 notify arms, 2 d3 arms) plant the same
design at base and head. For each, the lane's RTL diff applied to the planted base file gives the planted head file byte for
byte (`logs/planted-identity.log`).

## 5. OOC 1x1 before/after (#638's recipe) - STOP

Recipe: `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` in the scratch parent (dev `fa450d30` + the five patches), shape ax7101 (1x1).
- Export with the launcher's preview (`--build` dropped), with the builder output and ROMs redirected outside the checkout.
- RTL elaboration (`synth_design -rtl -rtl_skip_mlo`, `Synth 8-4445` promoted to error) as the integrated log.
- `syn/ooc/pp_baseline.py ... --integrated-log ... --integrated-clock` (20 ns, from `CLK_HZ_P`), then `baseline_ooc.tcl`.
- Vivado 2026.1 (SW Build 6511674), `xc7a100t-fgg484-2`, every run under `flock $VIVADO_LOCK`.
- Base pin `054d01c7`, head pin `e3c9f0b5`; the parameters (`baseline_parameters.json`) are identical; every image hash in
  `baseline_images.json` is identical (only the paths differ).
- Nothing else of this lane ran during any Vivado run. Other lanes' jobs were running on the host at the time.

| `KL_pp_shadow` standalone 1x1 | LUT | FF | RAMB36 / 18 | DSP | whole-design WNS (20 ns) |
|---|---:|---:|---:|---:|---:|
| base `054d01c7` | 23,161 | 19,783 | 16 / 3 | 8 | -2.685 ns |
| head `e3c9f0b5` | 23,211 | 19,777 | 16 / 3 | 8 | -1.571 ns |
| delta | **+50** | **-6** | 0 | 0 | |

**+50 LUT is above the 40 LUT stop.** The FF delta is within the 60 FF limit.

Where it sits (`baseline_hierarchy.rpt`, rows that moved). The rows whose RTL changed are `u_notify` alone:

| Row | dLUT | dFF | RTL changed? |
|---|---:|---:|---|
| `u_notify` (`KL_aecp_notify`) | -1 | -3 | yes (the one gate) |
| `u_tx_slots` | +121 | 0 | no |
| `u_timer` | +44 | 0 | no |
| `u_srp` (`u_admission` +17, `u_encoder` +14, ...) | +30 | 0 | no |
| `u_dispatch` (`u_acmp_q` +12, ...) | +19 | 0 | no |
| `u_originator` | +14 | 0 | no |
| `u_aecp` (`u_ucpu` +11, `u_dyn` -8, ...) | -5 | 0 | no |
| `u_pp` own logic | -79 | -1 | no |
| `u_normalizer`, `u_scoreboard`, `u_rx_validator`, `u_maap`, `u_trace`, `u_ca_builder` | -27, -17, -16, -15, -10, -8 | 0 | no |

These are the rebuilt hierarchy's cross-boundary moves. The head synthesis also logs 12 fewer `Synth 8-3917` warnings, all
of them constant-driven ports of `protocol_processor_top__GCB0`; that is a different partition of the top's glue.

**Diagnostic: `KL_aecp_notify` synthesized alone** at the 1x1 binding (`N_CTRL_P` 16, `N_STREAM_IN_P`/`OUT_P` 2, the timer
slots of the integrated log, `EN_IDENTIFY_NOTIF_P` 0), `AreaOptimized_high`, out of context, 20 ns clock:
- base: 2,474 LUT (1,514 logic, 960 LUTRAM), 1,280 FF;
- head: 2,471 LUT (1,511 logic, 960 LUTRAM), 1,282 FF;
- delta -3 LUT, +2 FF. The base figures equal #148's measured head (2,474 / 1,280).

**#638's gate** (`pp_resource_gate.py check ... --endpoint ooc-1x1`): rc 0, PASS at base and at head, "re-baseline
recommended" at both (LUT, FF and RAMB36 below the recorded baseline). There is no `Synth 8-7186` and no `Synth 8-4445`
diagnostic (only the echoed severity command). Logs, reports and checkpoints are in the scratch `meas/{base,head}` and
`meas/module/{base,head}`.

**What the manager can decide.** Either accept the measurement as attribution noise, since the module's own delta is -3 LUT
and its row -1, or ask for a different measurement. No RTL change was made to chase the figure.

## 6. Suites (base vs head)

All rc 0, unpiped, pinned Verilator 5.050, in `git archive` extractions of `054d01c7` and `e3c9f0b5`.

| Gate | Base `054d01c7` | Head `e3c9f0b5` |
|---|---|---|
| `./scripts/run_suites.sh` | 33 suites, 1,021,640 checks, 0 failing | 33 suites, 1,021,651 checks, 0 failing: `aecp_notify` 34 to 45 (DR +11); the other 32 tallies identical |
| `tb/pp_top` `make` (six builds), full log | 10,444 (9,956 / 20 / 178 / 231 / 56 / 3) | the same; the 281-line logs are byte-identical |
| `tb/aecp_notify` `make`, full log | 34 (30 + 4) | 45 (41 + 4); the only difference is the five DR `[i]` lines and the tallies (TW, FT lines identical) |
| `./scripts/lint_hdl.sh` | 41 `LINT OK` | 41 `LINT OK`; logs identical |
| `./syn/yosys/run.sh` | 42 tops, 42 `YOSYS OK` + 1 `YOSYS XILINX OK`, `all.v` parsed once | the same; logs byte-identical |
| `make check` (in the tree) | lint 41 mermaid + 18 wavedrom; 1,136 links; 115 REQ, 17 GAP; 94 rows, 0 untested; 28 parameters | identical log |
| `python3 scripts/gen_matrix.py --check` (in the tree) | 94 rows, 0 untested | identical |

## 7. Campaigns (base vs head)

Every campaign that builds a changed file: `KL_aecp_notify.sv` is built by every `tb/pp_top` driver and by the `tb/pp_top`
arms of `tb/adp_engine` and `tb/maap`; `tb/aecp_notify/sim_main.cpp` by the notify driver's INDEX and TIMEBASE suites; the
notify driver itself changed. Base and head ran from extractions, all rc 0. Records were compared by a scratch script
(`scripts/cmp_camp.py`): the driver output (sorted, paths normalized) and every per-arm file's graded lines (FAIL / PASS /
tallies / `[i]` figures / verdicts).

| Driver (`--jobs`) | Base | Head | Records |
|---|---|---|---|
| `notify_mutants.py` (2) | 53 of 53 KILLED, 7 goldens PASS | 56 of 56 KILLED, 7 goldens PASS | 57 of 60 identical; the three TW controls each add DR3 (below); three new controls |
| `ctr_mutants.py` (2) | control PASS, 17 of 17 KILLED | the same | driver logs byte-identical (113 lines); 18 of 18 per-arm files identical |
| `d3_mutants.py` (3) | 110 of 110 KILLED, 6 goldens PASS | the same | 116 of 116 identical (the unbound `%d` of `d3_phases.hpp:2963` and `:2993` masked; it prints garbage at base and head alike) |
| `aecp_mutants.py` (2) | 6 controls PASS, 61 KILLED | the same | 67 of 67 identical |
| `aecp_dispatch_mutants.py` (2) | 4 controls PASS, 40 KILLED | the same | 45 of 45 files identical (same masking) |
| `acmp_mutants.py` (2) | 33 of 33 KILLED, goldens PASS | the same | 38 of 38 identical (`results.json` differs only in record order) |
| `gsi_mutants.py` (2), `name_wr_mutant.py` | 20 detected, golden and restored PASS; decode killed, golden and restored PASS | the same | 45 and 7 files identical |
| `tb/adp_engine/mutants.py` (2), `tb/maap/mutants.py` (2) | 2 + 41 and 3 + 29 PASS | the same | 43 and 32 identical |

**The only record moves are the new check's.** `counter_spacing_from_selection_tw` (2 to 3), `counter_stamp_at_send_only`
(1 to 2) and `counter_stamp_first_job_only` (2 to 3) each keep their TW failures exactly and add DR3, at ms 31512. None of them
follows D's wait after the drain. Every other notify arm that runs `tb/aecp_notify` differs only by the five DR `[i]` lines
and the build tally (`logs`, checked line by line). The ten patch arms of `ctr`/`mutations` that plant into the notify file,
and the d3 arms, give identical records.

## 8. Parent consumer set (17) at milan-fpga dev `fa450d30`

Scratch parent: kebag-logic/milan-fpga cloned under the lane's scratch directory, detached at
`fa450d301805881ad713b67521477bf042ddadfd`, never committed or pushed. Submodules `external` `efeb541a`, `gptp-processor`
`5dce647a`, `third_party/verilog-axis` `48ff7a7e` (each at its gitlink) and `protocol-processor`, whose worktree and index
gitlink (`git update-index --cacheinfo`) were moved to base `054d01c7` or head `e3c9f0b5` by a script that first checks
`git -C <dir> rev-parse --show-toplevel` for the parent and the submodule. The five patches, each `git apply --check` clean and
then applied, in order:

| Patch | sha256 | bytes |
|---|---|---|
| `parent-adoption-c8-bbf704ec.patch` | `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c` | 8,546 |
| `parent-adoption-p2-p1-1269cdaf.patch` | `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84` | 24,711 |
| `parent-adoption-c10-1269cdaf.patch` | `55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9` | 7,133 |
| `parent-adoption-232-241f9184.patch` | `88ee5e9643a453f8c31dc76e5f8d57e8deec89bcbbf9d4a4a8ca005757b72560` | 587 |
| `parent-adoption-148-6c22d3ca.patch` | `bbd0301dc7e576f51f92d24c8d140eda0666f9c6699806649365110e7ecfea83` | 966 |

Pinned Verilator 5.050 first on PATH (`VERILATOR` = the bounded wrapper). GNU Make 4.3 (a copy of another lane's build, the
earlier lanes' convention) first on PATH for every gate except the 4.4.1 builder runs. Head ran first, then base.

| # | Command | Base `054d01c7`: rc, s | Head `e3c9f0b5`: rc, s | Result (identical at both unless stated) |
|---:|---|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | 0, 1 | 0, 1 | every ratchet held (long function 0 <= 0, ...); it scans `protocol-processor/tb/`, the new DR code included |
| 2 | `scripts/check_py_idiom.py` | 0, 5 | 0, 4 | every ratchet held; the module line count moves 199,537 to 199,561 (`notify_mutants.py` +24), the only difference in gates 1-8 and 11 |
| 3 | `scripts/check_rtl_source_lists.py` | 0, 1 | 0, 2 | 108 files, 4 of 4 consumer lists; protocol-processor 42/42 tops, 0 recorded |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0, 4 | 0, 6 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0, 0 | 0, 1 | sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0, 3 | 0, 3 | 3,824 first-party ports, **protocol-processor 1,759** (no port change); undocumented 111 <= 111 |
| 6 | `scripts/measure_naming.py --check` | 0, 1 | 0, 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0, 7 | 0, 7 | 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |
| 8 | `scripts/docs_check.py` | 0, 5 | 0, 6 | 0 findings |
| 9 | `flock $VIVADO_LOCK scripts/xvlog_gate.py --check` | 0, 1,215 (most of it waiting for the lock) | 0, 153 | PASS, 2 findings == ratchet (the two #22 lines in `KL_pp_originator.sv` and `KL_pp_rx_validator.sv`); identical but for the pinned sha. Both ran with nothing else of the lane running |
| 10 | `sw/builder/test_builder.py` | 0, 1,265 (Make 4.3); 0, 1,213 (Make 4.4.1) | 0, 1,528 (Make 4.3); 0, 1,408 (Make 4.4.1) | 4.3: "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 1b's `MAKEFLAGS += -e` arm, gate 11's mf48 tree); 4.4.1: "EXCEPT 1 NOT RUN" (gate 11) |
| 11 | `scripts/lint_rtl.py --check` | 0, 12 | 0, 10 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0, 388 | 0, 427 | legs 606, 606, 646 and 311 checks, 0 failures; 2,167 `[PASS]`, 0 `[FAIL]` at both |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0, 1 | 0, 1 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0, 32 | 0, 53 | identical graded lines |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0, 2,870 | 0, 2,903 | every leg passes, with the same tallies at both: 236 x2, 233, aclk 193, 1,961 x3, 3,746, 416, 421, gmstep 104, 33, 182 x2, 6 of 6 x2; all 1,236 check, result and verdict lines identical (sorted; `-j` interleaves them) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0, 818 | 0, 851 | identical tallies (5 of 5, 24 of 42) and 109 graded lines; the AEM image's two `checksum` lines print only in the first (head) run, where make regenerated it |

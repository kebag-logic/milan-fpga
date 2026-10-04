[A520]

Closes milan-fpga#232
Relates to milan-fpga#229
Relates to #22

The #232 area lane: the first lever of epic milan-fpga#229, as ranked by the #234 baseline
(milan-fpga PR #638) (assignment: milan-fpga #232 comment 5970460015; round 1b, comment
5974077269; round 2, comment 5976892215). Branch `pp232-notify-ram` from `main` `f4167536`,
merged with `main` `5c71928a` and `83999eba`; eight commits, head `2ea3dee`.

The notification controller registry no longer spills into flip-flops. Its row table carried
a distributed-RAM attribute that Vivado ignored (`Synth 8-7186`, 2,048 flops), because the
availability monitor compared every row with each command in one cycle, a 16-way comparator
bank. A LUTRAM identity index now gives the same match in the same cycle, so the row table
maps to distributed RAM. Every output of `KL_aecp_notify` is cycle-identical to `main`'s. No
port, parameter or register changes.

Lever 5, the counter throttle stamps, stays in flops without its redundant reset: ruled
final for #232 (milan-fpga #232 comment 5974004216, option (c)). The rest of #232's scope is
recorded below: the storage inventory, the valid-versus-bulk split, the command queue and
the exhaustion behaviour. In passing, `KL_aecp_notify.sv` now declares `pd_ix_w` before its
first use, so Vivado's xvlog analyses the module (#22's line for this file).

| Commit | Item |
|---|---|
| `9e29e2a` | the identity index; the row table in LUTRAM; the counter stamps lose their redundant reset |
| `0c76b21` | `tb/aecp_notify` section IX, and its four controls in `tb/pp_top/notify_mutants.py` |
| `3ab2e4d` | 06 section 7: the block's storage, intended primitives and exhaustion behaviour; 09 section 8.4 |
| `823fc20` | merge of `main` `5c71928a` (P1 #150, C10 #149), `--no-ff` |
| `6e950fe` | `pd_any_w`/`pd_ix_w` declared above `ca_request`, their first use (#22); a reorder only |
| `f3abfc6` | `tb/aecp_notify` IX5, IX6 (the rewrite's first cycle, and a reset in it) and section TS (the stamps' valid bit); the three review faults as controls in `notify_mutants.py`; the READMEs and 09 |
| `0d9e5e7` | review residue: the index comment and 06 say the rewrite spans the row write's own cycle and the cycle after it; 06 records the index's configuration-time zero content |
| `2ea3dee` | merge of `main` `83999eba` (PR #152, processor #85, the ADP walk's tests), `--no-ff` |

## Round 1b

Round 1 ended at a STOP on lever 5. The manager ruled (c), final for #232, and assigned the
merge (milan-fpga #232 comments 5974004216 and 5974077269).
- **Merge** `823fc20`: `--no-ff` merge of `main` `5c71928a`.
  - One conflict, in the `tb/pp_top` README's notify mutation record. P1's re-run note is
    kept, and this lane's sentence on the four `ix_*` controls follows it. `06` and `09`
    merged cleanly.
  - Both sides' contracts are kept: P1's name stage, D3 amendment and D3KR; C10's census,
    declaration order and citations; this lane's registry index.
  - Neither side's code touches a file the other changed. The only line citations into a
    file both sides changed (`09_verification.md:56`, from the `tb/nvm_port` README) still
    hold.
  - Both ROMs regenerate byte-equal at `main` and at the head.
- **#22** `6e950fe`: the declaration reorder (item 4).
- **Re-measured at the head:**
  - every processor suite, the Yosys gate (42 tops, one parse), and every `tb/pp_top`
    campaign, with notify, ctr and D3 at their recorded counts;
  - the lockstep bench of `main` against the head over its five shapes;
  - the integrated route, beside `main`'s route on the same scratch parent.
- **Parent consumer set** at dev `5fabb46e` with the c8, p2-p1 and c10 patches (all three
  apply).
  - Gate 9 needs the #22 fix banked in the parent's xvlog ratchet (Parent-visible list).
  - Gate 16 fails #643's two T30 checks, exactly as it does at `main`.

## Round 2

R452-1 and R453-1 (PR #153 comments 5976816563 and 5976889224) found the RTL change clean,
and were NEGATIVE on MINOR findings: missing committed coverage, and unpublished Vivado
evidence. Round 2 (milan-fpga #232 comment 5976892215):
- **Committed coverage for the three dependencies** (R452-1 F1, R453-1 F2), `f3abfc6`.
  `tb/aecp_notify` grows from 20 to 30 checks, and all 30 pass on `main`'s RTL too:
  - IX5: the rewrite's first cycle, the one in which the row write lands. A command from
    the reused row's previous controller, which `rows_r` still holds, keeps the row against
    a failed probe in that cycle.
  - IX6: a reset in that cycle, then a REGISTER of the same identity into the same row.
    Only the comparator can match in its first cycle, because the index then holds nothing
    for the row.
  - TS1 to TS3: a counter change in the same second is held, and after a warm reset it goes
    out at once. The stamps' valid bit `ctr_sent_r` carries that.
  - The reviewers' faults are planted as controls in `notify_mutants.py`, with the
    reviewers' own edits. `override_set_only` fails IX6 and IX6b; `own_compare_new_row` fails
    IX5; `stamp_read_without_valid` fails TS3. The campaign is 47 of 47 KILLED, every arm at
    its README count.
  - Every reviewer probe, run unchanged (R452-1's `plant.py` and `clear_cycle_probe.sh`,
    R453-1's `make_controls.py` and `probe_committed.sh`), now fails a committed check:
    22 of 22 controls (Validation).
- **Vivado evidence published** (R453-1 F1): extracts and small reports from the eight runs
  the figures come from, each with its raw file's full sha256, and a script that re-derives
  every quoted figure from them alone: `evidence-r2/vivado/` in the lane's round-2 evidence
  packet, which the manager archives on milan-fpga's evidence branch.
- **The lockstep bench published**, with its control table corrected (R453-1 F2). Round
  1b's "comparator only in the set cycle" control also dropped the clear: its edit was
  `ix_busy_w = ix_set_r`. It is in the same packet, under `evidence-r2/lockstep/`.
- **Parent adoption** at dev `241f9184`: `parent-adoption-232-241f9184.patch` banks the
  vanished `pd_ix_w` finding in `scripts/xvlog.budget` (Parent-visible list).
- **Merge** `2ea3dee`: `--no-ff` merge of `main` `83999eba` (PR #152, tests and comments in
  the ADP walk). There were no conflicts. `09_verification.md` is the only file both sides
  changed, and it keeps both sides' hunks. The merge's two HDL changes since `6e950fea` are
  comment-only (the index comment, and `KL_adp_engine.sv`'s comments). With comments
  stripped, both files are equal, so the round-1b routes stand for this head.
- **Residue**, `0d9e5e7` and this body:
  - R453-1 R1: the rewrite spans "the cycle in which the row write lands (`wr_en_r` high)
    ... and the cycle after it". This wording is now in the RTL comment, in 06 and in item
    1.
  - R452-1 F2: the inventory's index row names both the synthesis mapping report and the
    implemented cells.
  - R452-1 S1: 06 records that the index relies on its configuration-time zero content,
    and that `rst_n` leaves the index and `rows_r` alone.

## Items

### 1. Lever 1: the registry (`KL_aecp_notify.sv:329` on `f4167536`)

`command_registry_hit` (`f4167536` `:539-546`) is the availability monitor's "a valid
command from a registered controller" (06 F06.5). It compared every row's {eid, mac} with the
command in one cycle, so every row was read at once and the table could not be a RAM.

The replacement keeps the same answer in every cycle:
- **The identity index.** The 112-bit {eid, mac} is cut into 19 six-bit chunks. Row i keeps
  one 64x1 LUTRAM per chunk, holding a 1 at that chunk's value. A row matches when all 19
  memories read 1 at the command's chunks (`KL_aecp_notify.sv:551-603`).
- **The rewrite.** A REGISTER (`N_APPLY`, `:1365`) is the only writer of an identity. It
  re-indexes its row over two cycles: the cycle in which the row write lands (`wr_en_r`
  high) clears the old identity's bits, and the cycle after it sets the new identity's. In
  the first, the write-index read port (`ix_wr_row_w = rows_r[wr_ix_r]`) still returns the
  old row.
- **The two rewrite cycles.** The row's match is one 112-bit comparator against that read
  port, which returns exactly what `rows_r` holds in each cycle.
- **What the index needs.** The emission write-back rewrites a row's own {eid, mac} with
  seq + 1 and leaves the index alone. The index starts empty (LUTRAM INIT 0, an explicit
  `initial`), and bits enter only through a row write, so a clear always empties a row.

`rows_r` is now read at three indices (walk or drain, probe pick, write) and infers
`RAM32M x 64`. The index is 288 RAM64X1D and 16 RAM32X1D (`KL_aecp_notify.sv:336`, `:585`).

Why not the walk #638 estimated: a serial walk over the table for each command would delay
the monitor's re-arm, cancel and race arms by up to 16 clocks, a timing change the
assignment's rules exclude. The index costs about 600 LUTs of LUTRAM. That is why the
measured LUT saving is lower than #638's estimate, while the flop saving matches it.

### 2. Lever 5: the counter throttle stamps (`KL_aecp_notify.sv:404`)

They stay in flops, and only their reset goes. `ctr_sent_r` is each stamp's valid bit, so
dropping the reset is the "valid metadata separated from bulk arrays" item for this array.
It changes no behaviour and frees no resource (192 / 640 flops at 1x1 / 8x8, before and
after). The window check (`:1098-1099`) reads every stamp against `now_ms_i` in every cycle, and
the port admits any `now_ms_i` sequence, so exact behaviour needs every stamp each cycle.
Shrinking them needed either a timing change (a serialized check) or a narrower `now_ms_i`
contract (a precomputed next-ms ripeness). The manager ruled (c), flops without reset, final
for #232 (comment 5974004216); the narrower contract is not filed, and the redesign
milestone (milan-fpga #640) can take it from there.

### 3. The rest of #232's scope

- **Storage inventory.** The notification block is in 06 section 7 ("Storage"). The AECP
  and packet structures, with their Vivado report lines, are in the table under Validation.
- **Valid metadata versus bulk arrays.** `rows_r`, the index and `cmdq_*` carry no reset;
  their valid state (`valid_r`, the queue pointers and count) is the reset state. The stamps
  join them (item 2).
- **The 16-entry command queue** is already distributed RAM (`cmdq_*`, 24 RAM32M). Its depth
  is `P-NOTIF-QUEUE-DEPTH`. No change.
- **Exhaustion** is defined for every structure; none needed a new behaviour. A REGISTER into
  a full registry answers NO_RESOURCES. `amap_busy_o` holds the engine's next command while
  anything is pending, so the queue holds at most one command's pushes. A push into a full
  queue would be dropped and counted (`cmdq_drop_r`). The other classes coalesce into one
  pending bit per class or descriptor.
- **The AECP response buffer** cannot spill: `KL_aecp_resp_buf` holds no array and writes
  main memory at `RESP_BASE_P` (`:336-339`). `u_resp` is 260 FF and no RAM in every run
  below.
- **"Meets 100 MHz"** is judged at the shipping configuration's declared 50 MHz, as ruled for
  #234: the route closes at 50 MHz in all four signoff corners (Validation).

### 4. #22 in passing (`KL_aecp_notify.sv:605-607`)

`pd_any_w` and `pd_ix_w` are declared above `ca_request` (`:609`), whose cancel term
(`:618`) is their first use; `pend_pick` (`:727`) still drives them. No logic change. xvlog
(Vivado 2026.1, `pp_pkg.sv` then `KL_aecp_notify.sv`): at the merge `823fc20`, rc 1 with
`ERROR: [VRFC 10-3380] identifier 'pd_ix_w' is used before its declaration
[.../KL_aecp_notify.sv:613]`; at `6e950fe`, rc 0 with no error or warning. #22 stays open
for `KL_pp_originator.sv` and `KL_pp_rx_validator.sv`.

## Validation

Round 1 measured base `f4167536` against `3ab2e4da`; round 1b re-measured at the merge
(`6e950fea`, the merge plus the declaration reorder) against `main` `5c71928a`; round 2 ran
every gate again at `2ea3dee`.

**Behaviour.**
- **`tb/aecp_notify` sections IX and TS** (16 checks; 20 to 30 in the suite). On `main`'s
  RTL (`83999eba`'s `KL_aecp_notify.sv`, byte-equal to `f4167536`'s) the bench passes 30 of
  30 too, so these sections describe behaviour that did not change.
  - IX1: a reused row refuses its previous controller. IX2: none of the 112 one-bit
    neighbours of a registered identity matches. IX3: the identity matches in the command's
    cycle.
  - IX4a/IX4/IX4b: in the rewrite's second cycle the command beats a failed probe in the
    same cycle; the failure alone removes the row.
  - IX5/IX5b: in the rewrite's first cycle, the row write's own cycle, a command from the
    reused row's previous controller, which `rows_r` still holds, beats a failed probe.
  - IX6a/IX6/IX6b: after a reset in that cycle, the same identity re-registered into the
    same row is matched by the comparator in its first cycle, and by the index after it.
  - TS1 to TS3: a change in the same second is held, and after a warm reset it goes out at
    once.
  - Seven killed controls in `notify_mutants.py`: `ix_old_identity_kept` (IX1),
    `ix_last_chunk_ignored` (IX2), `ix_new_identity_unset` (IX3, IX4, IX6b),
    `ix_rewrite_unmatched` (IX4, IX6, IX6b), and the reviewers' `override_set_only` (IX6,
    IX6b), `own_compare_new_row` (IX5) and `stamp_read_without_valid` (TS3).
- **The reviewers' probes, run unchanged at `2ea3dee`.** R452-1's `plant.py` (10 controls)
  and R453-1's `make_controls.py` (12) plant every control on the head file, and their
  `clear_cycle_probe.sh` and `probe_committed.sh` run `tb/aecp_notify` and `tb/pp_top`
  against each one. Result: **22 of 22 controls fail a named committed check**, each in
  `tb/aecp_notify`. `override_set_only` fails IX6 and IX6b, `own_compare_new_row` (and
  R453-1's identical `own_vs_new_row`) IX5, and both stamp edits TS3. `tb/pp_top` alone
  still catches only the four controls that break every match after a REGISTER.
- **Lockstep differential bench** (rounds 1 and 1b; published with round 2 in the lane's
  evidence packet). `main`'s `KL_aecp_notify`, renamed, ran beside the head's, with the same
  inputs every cycle.
  - Compared: every output and the internal `rx_cmd_hit_w`, every cycle.
  - Coverage: 40 runs of 1,000,000 cycles. Shapes (controllers / inputs / outputs) 16/2/2,
    16/9/9, 2/1/1, 16/2/2 with identify, and 5/8/8. Protocol-shaped and fully random inputs,
    with resets mid-run.
  - Result: **0 mismatches**, in round 1 (`f4167536` against `3ab2e4da`) and again at round
    1b (`5c71928a` against `6e950fea`). The round-2 head changes no HDL logic.
  - Controls, mismatches over 8 runs at 16/2/2 (round 1b): no rewrite comparator 118,069; no
    clear 14,840,381; no set 10,944,924; the rewrite window cut to the set cycle (no clear,
    and the compare only in the set cycle; corrected label, R453-1) 14,848,035; last chunk
    ignored 545,407; REGISTER not re-indexed 10,945,711; a stamp read without its valid bit
    161,278.
  - Round 2 adds the reviewers' own edits on the same bench: `override_set_only` 8
    mismatches, in 4 of 8 runs (the random-input seeds only); `own_compare_new_row` 4,611, in
    8 of 8. The bench's protocol-shaped stimulus aims no reset at the rewrite window, and
    IX6 now does.

**Processor gates** (from a `git archive`; pinned Verilator 5.050).

| Gate | Round 1b head `6e950fea` | Round 2 head `2ea3dee` |
|---|---|---|
| ROMs (`gen_ucode.py`, `gen_ltn_rom.py`) | `ucode.hex` `518b900c...`, `ltn_rom.hex` `23cc67ee...`, equal to `main`'s | rc 0 each; the same two images (2,048 and 129 lines) |
| `./scripts/lint_hdl.sh` | rc 0, 41 of 41 | rc 0, 41 of 41 |
| `./scripts/run_suites.sh` | rc 0, 33 suites, 1,021,455 checks (`main` `5c71928a`: 1,021,449) | rc 0, 33 suites, 1,021,485 checks, 0 failing. Against round 1b only two suites move: `aecp_notify` 20 to 30 (this round) and `adp_engine` 1,328 to 1,348 (`main`'s PR #152; 1,348 at `83999eba` alone). `pp_top` 10,416 both |
| `make check`, `scripts/gen_matrix.py --check` | rc 0: 1,114 links, 94 matrix rows, 0 untested, 28 parameters | rc 0: 1,120 links, 115 REQ rows, 94 matrix rows, 0 untested, 28 parameters |
| `./syn/yosys/run.sh` | rc 0: 42 tops, `all.v` parsed once | rc 0: 42 tops, `all.v` parsed once; engine Xilinx mapping OK |
| `notify_mutants.py --jobs 4` | rc 0, 44 of 44 KILLED | rc 0, 47 of 47 KILLED, six goldens PASS; 47 of 47 at their README counts |
| `ctr_mutants.py --jobs 4` | rc 0, control PASS, 17 of 17 | rc 0, control PASS, 17 of 17 KILLED; 17 of 17 at their README counts, identical to round 1b |
| `d3_mutants.py --jobs 4` | rc 0, 110 of 110 KILLED, six goldens PASS | rc 0, 110 of 110 KILLED, six goldens PASS; the 98 `tb/pp_top` arms at their README counts; all 116 records identical to round 1b |
| `aecp_mutants.py --jobs 4` | rc 0, 5 controls PASS, 55 KILLED | rc 0, 60 checks PASS (5 controls, 55 KILLED); 55 of 55 at their README counts, identical to round 1b |
| `aecp_dispatch_mutants.py --jobs 4` | rc 0, 4 controls PASS, 40 KILLED | rc 0, 44 checks PASS (4 controls, 40 KILLED); 40 of 40 at their README counts, identical to round 1b |
| `acmp_mutants.py --jobs 4` | rc 0, 19 of 19 KILLED | rc 0, 19 of 19 KILLED, three goldens PASS; 22 of 22 records identical to round 1b |
| `gsi_mutants.py --jobs 4`, `name_wr_mutant.py` | rc 0 each | rc 0 each: 20 detected by named checks, golden and restored PASS (record identical to round 1b); decode killed, golden and restored PASS |
| `make -C tb/adp_engine mutants JOBS=4` (the merge's campaign) | | rc 0, 43 checks PASS: both controls PASS, 41 of 41 KILLED, as `main`'s README records; 41 of 41 at their README counts (`cfg-valid-no-reset` 9 and `gate-enable-dropped-top` 7, the counts their rows give since lane P1) |

"At its README count" means each arm's verdict and failing-check count equal the count the
`tb/pp_top` README records (P1's re-runs included).

**Vivado** (#638's recipe and gate at milan-fpga `79e53831`). Scratch parent, never
committed. Vivado 2026.1, `xc7a100t-fgg484-2`, 50 MHz.
- Round 1: dev `bbf704ec` plus `parent-adoption-c8-bbf704ec.patch` and
  `parent-adoption-p2-p1-1269cdaf.patch`; processor `f4167536` for base, `3ab2e4da` for head.
- Round 1b, the integrated route only: dev `5fabb46e` plus those two and
  `parent-adoption-c10-1269cdaf.patch`; processor `6e950fea`, and `main` `5c71928a` on the
  same parent.
- Round 2 runs no Vivado: the head's HDL is `6e950fea`'s with comments changed only (the
  index comment, and `main`'s `KL_adp_engine.sv` comments). With comments stripped, both
  files are equal.
- **Published** (R453-1 F1): `evidence-r2/vivado/` in the lane's evidence packet holds the
  eight runs below. It has #638's utilization, hierarchy and timing reports, the flow's
  route status and four signoff corners, both final RAM mapping reports, every
  `Synth 8-7186` / `8-4445` / `8-6901` line, and a cell census. Each extract records its
  raw file's full sha256: the round-1b route logs are `3345c0ac...9079073` (`main`) and
  `4d18c290...3eca3f37` (head). Its `tools/rederive.py` re-derives every figure in this
  section from the packet alone.

| Endpoint | LUT | FF | Slice | RAMB36 / 18 | DSP | WNS / WHS ns | `u_notify` LUT (LUTRAM) / FF |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shipping route at the merge, `main` `5c71928a` | 51,434 | 59,691 | 15,847 | 79 / 27 | 14 | +0.079 / +0.014 | 3,270 (96) / 3,299 |
| Shipping route at the merge, head `6e950fea` | 50,671 | 57,660 | 15,841 | 79 / 27 | 14 | +0.274 / +0.023 | 2,343 (960) / 1,287 |
| Shipping route, round 1 base `f4167536` | 50,740 | 59,631 | 15,839 | 79 / 27 | 14 | +0.116 / +0.012 | 3,171 (96) / 3,299 |
| Shipping route, round 1 head `3ab2e4da` | 50,090 | 57,681 | 15,824 | 79 / 27 | 14 | +0.143 / +0.027 | 2,327 (960) / 1,276 |
| Standalone 1x1, base | 24,494 | 25,471 | | 21 / 3 | 8 | -0.496 (estimate) | 3,194 (96) / 3,299 |
| Standalone 1x1, head | 23,600 | 23,429 | | 21 / 3 | 8 | -4.409 (estimate) | 2,261 (960) / 1,253 |
| Standalone 8x8, base | 31,383 | 33,968 | | 26 / 5 | 8 | -2.222 (estimate) | 2,846 (96) / 3,799 |
| Standalone 8x8, head | 30,458 | 31,793 | | 26 / 5 | 8 | -2.728 (estimate) | 2,396 (960) / 1,753 |

- **Deltas, head minus base.** Route at the merge: -763 LUT, -2,031 FF, -6 slices, -150
  CARRY4, WNS +0.195 ns. Round 1 route: -650 LUT, -1,950 FF, -15 slices, -147 CARRY4, WNS
  +0.027 ns. Standalone 1x1: -894 LUT, -2,042 FF. Standalone 8x8: -925 LUT, -2,175 FF.
- **The route at the merge.** Round 1b measures the route only, and the standalone figures
  stand unless it moves materially. Against round 1's head, the image moved +581 LUT, all in
  P1's D3 writer (`u_aecp/u_d3`, +619 LUT and +96 FF). The lane's effect did not move: head
  minus `main` (-763 LUT, -2,031 FF; `u_notify` -927 LUT, -2,012 FF) matches round 1's head
  minus base. So the standalone figures stand. The merge's base, `main` on the same parent, was
  routed for this comparison.
- **Timing.** Every route is complete, with 0 routing errors, and closes at 50 MHz in all four
  signoff corners. At the merge, head's worst setup path is in P1's D3 writer (`u_ucpu` ->
  `u_d3`, 33 levels). `main`'s is the `rx_cmd_hit_w` chain from `u_rx_validator` into
  `u_tx_arbiter` (39 levels), round 1 base's chain. `u_notify`'s own worst slack at head is
  +6.058 ns.
- **The standalone timing figure** is a synthesis estimate without I/O constraints.
- **#638's gate** against its recorded A:
  - at the merge: `main` rc 1 (+1,306 LUT, +685 FF; `u_d3` +605 LUT). Head rc 1 on LUT
    alone (+543), from that growth. Head against `main`: rc 0, "re-baseline recommended".
  - round 1: base route rc 1 (+612 LUT, +625 FF, the next adoption); head route, 1x1 and 8x8
    rc 0 each, "re-baseline recommended".
  - recording a new A is the merge bank's step.
- **Every log** at head has zero `Synth 8-7186` (16 at each base) and zero `Synth 8-4445`
  diagnostics. `Synth 8-6901` for `pd_ix_w` (#22): 3 at `main`, 0 at head.

Storage inventory, 1x1. The quoted text is from the head runs' "Distributed RAM: Final
Mapping Report" (the route at the merge and round 1's standalone run agree), except where a
row says otherwise:

| Structure | Source (head) | Intended | Base | Head |
|---|---|---|---|---|
| Registry rows `rows_r` | `KL_aecp_notify.sv:336` | distributed RAM | 2,048 FF; `Synth 8-7186 ... 'rows_r[0]' is not inferred as ram due to incorrect usage` (x16) | `u_notify \| rows_r_reg \| User Attribute \| 16 x 128 \| RAM32M x 64` |
| Registry identity index (new) | `:582-594` | distributed RAM | | synthesis mapping report: `u_notify \| g_ix_row[0].g_ix_chunk[0].mem_r_reg \| User Attribute \| 64 x 1 \| RAM64M x 1` (288 rows) and `... g_ix_chunk[18] ... 16 x 1 \| RAM16X1D x 1` (16); implemented cells after optimization: 288 RAM64X1D (576 LUTs) and 16 RAM32X1D (32 LUTs), which with `rows_r`'s 64 and `cmdq_*`'s 24 RAM32M make `u_notify`'s 960 LUTRAM |
| Registry flags | `:337`, `:410` | flops | flops | flops |
| Command queue `cmdq_*` | `:379-384` | distributed RAM | 24 RAM32M | 24 RAM32M (`u_notify \| cmdq_excl_r_reg \| Implied \| 16 x 64 \| RAM32M x 11`, ...) |
| Counter stamps `ctr_last_r` | `:404` | flops | 192 FF (640 at 8x8) | 192 FF (640), no reset |
| RX pools | `KL_pp_rx_slots.sv:193` | block RAM | 5 RAMB36 | 5 RAMB36 |
| AECP response buffer | `KL_aecp_resp_buf.sv:336-339` | main memory | `u_resp` 260 FF | 260 FF |
| Microcode `rom_r` | `KL_aecp_ucpu.sv:149` | block RAM | 3 RAMB36 | 3 RAMB36 |
| Register file `rf_r` | `KL_aecp_ucpu.sv:159` | distributed RAM | `RAM32M x 33` | `RAM32M x 33` |
| Descriptor index `idx_r` | `KL_aecp_desc_store.sv:285` | distributed RAM | `RAM32M x 22` | `RAM32M x 22` |
| Descriptor lines, names | `KL_aecp_desc_store.sv:297`, `:309` | block RAM | 1 + 1 RAMB36 | 1 + 1 RAMB36 |
| Map staging `amap_stage_r` | `KL_aecp_engine.sv:1195` | block RAM | 1 RAMB36 | 1 RAMB36 |
| Trace ring, TX slots, timer slots | `KL_pp_trace_ring.sv:86`, `KL_pp_tx_slots.sv:263`, `KL_pp_timer_service.sv:108` | block RAM | 1 RAMB36 each | 1 each |
| Dispatch queues | `KL_pp_dispatch.sv:303` | distributed RAM | 4 x `RAM32M x 66` | 4 x `RAM32M x 66` |

No AECP or notification data buffer maps into flops at head. The flags and the stamps are
flops by design, because each is read in parallel every cycle.

**Parent consumer set** (round 2: dev `241f9184`, PR #638's merge, + the c8, p2-p1 and c10
patches + `parent-adoption-232-241f9184.patch`, processor at `2ea3dee`; GNU Make 4.3 first
on PATH). Round 2's "consumer gate 3", the xvlog ratchet, is gate 9 below.

| # | Gate | rc | Result |
|---:|---|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | every ratchet held |
| 3 | `check_rtl_source_lists.py`, and `--selftest` | 0, 0 | 108 files, 4 of 4 lists; processor 42/42 tops, 0 recorded; self-test 50 of 50 |
| 4 | `pp_srcs.py --check --selftest` | 0 | 46 sources derived |
| 5 | `check_port_contracts.py` | 0 | processor 1,759 ports (as at `main`); undocumented 111 <= 111 |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | |
| 8 | `docs_check.py` | 0 | 0 findings, 187 md + 975 files |
| 9 | `xvlog_gate.py --check` | 1, then **0** | without the fourth patch: `BANK IT ... KL_aecp_notify.sv\|VRFC 10-3380\|pd_ix_w no longer occurs`, the #22 fix the parent banks (Parent-visible list). With `parent-adoption-232-241f9184.patch`: `PASS (2 finding(s) == ratchet; 0 hdl/, 2 pinned processors)`, pinned at `protocol-processor@2ea3dee2`. Gates 1 to 8, 3b and 11 re-ran with it: all rc 0 |
| 10 | `sw/builder/test_builder.py` | 0 | Make 4.4.1: all gates pass except gate 11, not run (it needs a local board build tree). Make 4.3 also leaves gate 1b's `MAKEFLAGS += -e` arm unexercised. As in rounds 1 and 1b |
| 11 | `lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks (and the 606, 606, 646 legs), 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches PASS; 4 render mutants caught; gmstep controls 6 of 6 |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | **2** | two-stream leg 65 checks, 0 failures; shipping leg 155 checks, 2 failures, the two T30 INTERNAL law checks (227 and 285 of 292 PDUs; first-event delay 8.830..9.034 ticks). Its leg-defect step, run directly: 5 of 5 |

Gate 16's two failures are milan-fpga #643, as the assignment records them. All 48 of the
gate's result lines are identical to round 1b's at `6e950fea`, and those were identical to
`main` `5c71928a`'s: the lane does not move the boot timing. Round 1's set (dev `bbf704ec`,
processor `3ab2e4da`) passed all 17, gate 16 included, because that processor predates P1's
longer boot walk.

## Parent-visible list

- No port, parameter or register change. `KL_aecp_notify`'s behaviour is cycle-identical
  (lockstep, and the new IX and TS checks pass on `main`'s RTL), and the port gate counts
  1,759 processor ports at `main` and at this head.
- One line of parent adoption: the parent's xvlog ratchet must bank `pd_ix_w`'s vanished
  finding (`scripts/xvlog.budget`, 3 to 2 findings). `xvlog_gate.py --check` fails until it
  is banked; the gate's own default run produces the change. The lane's handoff carries it
  as `parent-adoption-232-241f9184.patch`, which applies at dev `241f9184` after the c10
  patch.
- The routed image's worst setup path at this head is in P1's D3 writer (`u_ucpu` ->
  `u_d3`, +0.274 ns). At `main` it is the `rx_cmd_hit_w` chain into `u_tx_arbiter`
  (+0.079 ns). `u_notify` is off the critical path (+6.058 ns).
- #638's gate: this head against `main` passes and recommends a re-baseline. Against #638's
  recorded A it fails on LUT (+543), from `main`'s growth in P1's D3 writer (`main` alone:
  +1,306 LUT, +685 FF). Recording a new A is the merge bank's step.

## What remains

- milan-fpga #643: gate 16's two T30 INTERNAL law checks fail at this head and at `main`
  `5c71928a` alike (P1's boot length moves the feed's phase). Recorded there, not here.
- #22 stays open for `KL_pp_originator.sv` and `KL_pp_rx_validator.sv`.
- #229 continues with #230 and #639. The 1x1 image is still near full in slices: the flops
  and LUTs this lane frees move the slice count only a little.
- For the manager, as both reviews list: link #232's results from epic #229 (acceptance
  criterion 5); archive this round's evidence packet; record a new #638 baseline A at the
  merge bank; build the final current-dev candidate with the four parent patches.

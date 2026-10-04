[A525]

Relates to milan-fpga#639
Relates to milan-fpga#229

The #639 area lane: levers 3 and 6 of epic milan-fpga#229, from the #234 baseline
(milan-fpga PR #638) (assignment: milan-fpga #639 comment 5976100204). Branch
`pp639-armq-lsnrec` from `main` `5c71928a`, with `main` merged four times as it moved
(`83999eba`, `c050d971`, `07b1469d` by the manager, then `b0a74196` in round 2b);
thirteen commits, head `c725be12`. Round 2 (below) adds four: tests, their controls and
docs, and one HDL comment. Round 2b (below) is the merge of `main` `b0a74196` (PR #157)
alone.

Two storage structures move into distributed RAM. No port, parameter or register changes,
and no output changes in any cycle:

- **Lever 3, the top's timer arm-port queues.** The eight 4-deep queues in front of the
  timer service's one arm port were a packed shift queue: 1,152 flops at the 1x1 shape, and
  a LUT per flop to shift them (`protocol_processor_top.sv`, `armq_r`). Each queue is now a
  4-entry ring in distributed RAM: entries never move, a pop advances a head index, and a
  push writes at head + count. The drain order, depth, count, drop counter and arm-port
  registers are untouched.
- **Lever 6, the ACMP listener records.** Two 384-bit records made Vivado band five RAMB36
  side by side (`KL_pp_acmp_listener.sv`, `rec_ram_r`). The records are now distributed RAM,
  read without a read register. The walk still spends its read-issue state and reads the
  record in the next one, where nothing has written it.

| Commit | Item |
|---|---|
| `b42066c` | the arm-port rings; `tb/pp_top` section AQ, an eight-FIFO model of the arm port checked after every edge |
| `1bb3ba4` | the listener records in distributed RAM with no read register; `tb/acmp_listener` check RS (the reset sweep, read back through the RAM) |
| `9eebc61` | ten controls in `tb/pp_top/acmp_mutants.py` (issue #639 group) |
| `5828bb8` | one `acmp_mutants.py` golden per suite and run mode (`tb/pp_top` now has two modes) |
| `cfd62e8` | docs: the two suite READMEs, 09 §8.8, the HDL engineer guide §3.1, 07 §6, 08 §3 |
| `b845d01` | merge of `main` `83999eba` (PR #152), `--no-ff`, no conflict |
| `9e86991` | merge of `main` `c050d971` (PR #153), `--no-ff`, no conflict |
| `89b000c` | round 2: section AQ's drive from the bench (AQ3, AQ4) |
| `b1b6a5a` | round 2: the review's four full-queue controls in `acmp_mutants.py` |
| `6b82f9b` | round 2: section AQ, the ACMP controls paragraph and 09 §8.8 |
| `2ff8183` | round 2: the ring banner names the revisions behind its flop count (comment only) |
| `1cba30c` | merge of `main` `07b1469d` (PR #154) by the manager, `--no-ff`, no conflict |
| `c725be1` | round 2b: merge of `main` `b0a74196` (PR #157), `--no-ff`, no conflict |

## Results

Vivado 2026.1 with #638's recipe and gate on milan-fpga dev `241f9184`, in a scratch parent
that is never pushed. Base: dev `241f9184` + processor `5c71928a` + the c8 (`-bbf704ec`),
p2-p1 and c10 patches. Head: the same with the processor at `9eebc61`. 50 MHz, one Vivado
at a time under the host lock.

| Endpoint | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|
| Route base | 51,434 | 59,691 | 15,847 | 79 / 27 | 14 | +0.079 / +0.014 |
| Route head | 51,152 | 58,598 | 15,803 | 74 / 27 | 14 | +0.093 / +0.036 |
| Route head - base | -282 | -1,093 | -44 | -5 / 0 | 0 | +0.014 / +0.022 |
| Standalone 1x1 base / head | 24,930 / 24,648 | 25,465 / 24,278 | - | 21 / 16; 3 / 3 | 8 | estimate -2.059 / -0.743 |
| Standalone 8x8 base / head | 32,584 / 32,154 | 34,211 / 32,858 | - | 26 / 21; 5 / 5 | 8 | estimate -2.161 / -2.153 |

- **Routing.** Both routes are complete (0 routing errors) and meet the build gate at
  50 MHz. The base needed seven global routing iterations and the head two.
- **Per sub-block (1x1 standalone).**
  - The top's own logic: 447 -> 769 LUTs (246 of them the rings), 3,167 -> 2,034 FFs.
  - The listener: 1,434 -> 1,557 LUTs (208 the records), 1,106 -> 1,051 FFs, 5 -> 0 RAMB36.
  - The rest of lever 3's LUT saving appears in the engines that drive the faces (notify,
    originator, ADP, MAAP, SRP: -620 LUTs at 1x1). Vivado had pulled part of the shift
    queue's logic into them.
- **Against #638's estimates.**
  - Lever 3: FFs as estimated (about -1,100). LUTs about -400 at 1x1, not -1,000: the ring
    keeps a read mux and pointers, and adds 218 to 256 LUTs of RAM32M.
  - Lever 6: the five RAMB36 for 38 to 195 more LUTs in the listener, inside "about 250".
- **Routed.** The wrapper's LUTs are flat (+31) while its FFs drop by 1,046. So the route's
  LUT delta is within optimization noise; its FF, block RAM and slice deltas are the effect.
- **#638's gate, head against base.** Base's three endpoints were recorded into a scratch
  copy of the baseline. The head then exits 0 on all three, with "re-baseline recommended":
  for FF and RAMB36 on the route, and for LUT, FF and RAMB36 on the standalone endpoints.
- **#638's gate, against the committed record (dev C, processor `631eeb34`).** The route
  exits 0. The standalone endpoints exit 1 on LUT, but the base, the next adoption, exits 1
  by more: +598 and +1,028 at base, against +316 and +598 at head.

Mapping, from the synthesis reports at head:
- `g_armq[k].mem_r_reg | User Attribute | 4 x 47 | RAM32M x 8` for each of the eight faces
  (`4 x 48` at 8x8).
- `u_listener | rec_ram_r_reg | User Attribute | 2 x 376 | RAM32M x 63` (`16 x 376` at 8x8).

At base, `armq_r` is 1,152 flops (1x1), and the records are
`2 x 376(READ_FIRST) ... | 1 | 5` block RAM. The routed head holds 0 `armq_r` flops, 54
RAM32M and a RAM32X1D for the rings, and 52 RAM32M for the records.

## Behaviour

Both lockstep benches are published, with digests, in the review evidence packet (round
2).

- **Lockstep, the arm-port block.** `main`'s block, cut byte for byte from the top, beside
  the head's, with identical random arms.
  - 32 runs x 1,000,000 cycles over four slot widths: **0 mismatches**.
  - The runs covered 23,976,104 arms, 41,742,164 offers to a full face, 8,003,108
    full-queue pops with a push, and 412 resets.
  - Six planted controls (write at head, write at head + count after the pop, head stuck,
    read at the tail, write on a refused push, ring of three) are each caught in 8 of 8
    runs.
- **Lockstep, the listener.** `main`'s `KL_pp_acmp_listener` beside the head's, with
  emulated faces and matching probe responses so that streams settle.
  - 40 runs x 1,000,000 cycles over 1, 2, 3, 8 and 9 sinks: **0 mismatches**.
  - The runs covered 614,189 X_LATCH and 141,062 X_STRT_AP record reads, 31,686 settles and
    375 resets.
  - Five planted controls (read sink 0, a stale read sampled in X_IDLE, two unstored bits,
    a misaddressed sweep) are each caught in 8 of 8 runs.
- **Section AQ in `tb/pp_top`.** The arm port and the drop counter are checked against an
  independent model after every edge of the main harness.
  - Traffic from outside the top never puts a second arm behind a waiting one (0 of 8,270
    arms). Since round 2, a drive from the bench covers the full-queue path (AQ3, AQ4).
  - Nine ring controls are KILLED: the five round-1 controls by AQ2 and AQ3, and the
    review's four full-queue controls by AQ3.
  - AQ passes on `main`'s RTL with identical coverage.
- **Check RS in `tb/acmp_listener`.** A reset taken with records bound must leave every
  record zero in the RAM.
  - The misaddressed-sweep control survived the suite before RS and fails 37 checks with it.
  - Five record controls are KILLED.
  - RS passes on `main`'s RTL.

## Validation (round 1)

All rc 0 unless stated, foreground drivers each with their own log, never piped.

- **Processor suites.**
  - `run_suites.sh` at `9eebc61`: 1,021,449 -> 1,021,574 checks; only `acmp_listener`
    (2,988 -> 3,111, RS) and `pp_top` (10,416 -> 10,418, AQ) moved.
  - At `b845d01`: 1,021,594 checks (+20 in `adp_engine`, PR #152's own).
  - At `9e86991`: 1,021,610 checks (+16 in `aecp_notify`, PR #153's own).
  - `lint_hdl.sh` 41/41, `make check`, `gen_matrix --check`, and `syn/yosys/run.sh` (42
    tops, one parse) pass at every head.
- **Campaigns.** Every driver that builds the top or the listener, at the code head:
  - acmp 29/29 KILLED with four goldens;
  - notify 40/40, ctr 17/17, aecp 55 + 5 controls, aecp_dispatch 40 + 4 controls;
  - d3 110/110, gsi 20, name_wr, adp 30 + 2, maap 29 + 3.
  - Every pre-existing arm fails the count its README records, except two `tb/adp_engine`
    rows whose record is stale at `main`: their FAIL lines are identical on `main` and at
    the head.
  - At the merges: adp 41 + 2 (PR #152's arms); acmp 29/29 and notify 47/47 at
    `9e86991`, every arm at its record. AQ's coverage is unchanged through PR #153.
- **Parent consumer set of 17** at dev `241f9184` + the three patches, processor `9eebc61`:
  - 16 of 17 rc 0.
  - Gate 16 fails #643's two T30 INTERNAL law checks (first-event delay 8.830..9.034
    ticks). With the processor at `main`, its 48 result lines are identical: recorded
    against milan-fpga #643 (PR #648).
  - Gate 16's leg-defect step passes 5 of 5.
  - At both merges the light gates (1 to 8, 3b, 11) pass. Every heavy gate reads `hdl/`,
    and this lane's RTL is byte-identical at both merges.

## Round 2

Assignment: milan-fpga #639 comment 5981052216. The internal review (R462-1) found one
MINOR, F1: no committed check reached the rings' full-queue path. A defect planted there
passed every committed check, and the only evidence was an unpublished lockstep bench. It also suggested naming the source of the
banner's "1,153 flops" (S1). The external review (R463-1) was positive. Round 2 adds four
commits on `9e86991`. They change tests, controls and docs, plus one HDL comment; behaviour
does not change.

| Commit | Item |
|---|---|
| `89b000c` | `tb/pp_top` section AQ ends with a drive from the bench (the details follow this table). AQ3 checks the arm port and the drop counter against the model at every edge of the drive. AQ4 checks that the drive reached every state the rings add. |
| `b1b6a5a` | `acmp_mutants.py` carries the review's four full-queue controls as `armq_write_refused`, `armq_write_wrap_hi`, `armq_full_pop_refuses` and `armq_drop_skip_sat`. Each is KILLED by AQ3, and each planted top is byte-identical to the one the review's bench plants. The five round-1 ring arms now name both AQ2 and AQ3. |
| `6b82f9b` | Section AQ, the ACMP controls paragraph and 09 §8.8 describe the drive and the nine controls. Nothing in the tree points at an unpublished bench any more. |
| `2ff8183` | S1, a comment in the ring banner. It now reads 1,152 flops at the 1x1 shape at this change's base `5c71928a`, and 1,153 at `631eeb34`, the figure of milan-fpga's #234 area baseline. |

**The drive.**
- The wrap forces the eight faces' own nets to the bench's arms.
- It holds the timer service's arm input idle, so no engine sees an arm the drive queues.
- The force is never released: the drive is the run's last stimulus.
- A fixed-seed draw redraws per-face rates every 64 clocks, at light or heavy rates.
- After every eighth block it takes a reset of 1 to 4 clocks, with arms still queued and
  offered.
- Then every face runs at heavy rates until the drop counter has held 0xFFFF for 4,096
  drop clocks.
- Then a reset with the faces full, and the draw again.
- Every arm's deadline is its serial number, so a misplaced, overwritten, lost or repeated
  arm differs from the model.

The drive's reach is the same in `--arm-queue-only` and in the full default run:

| Required by the review | Reached |
|---|---:|
| counts 2 to 4: pushes onto a face holding 1, 2, 3 arms (writes at head + 1, + 2, + 3) | 48,239 / 3,636 / 5,594 |
| a full queue that pops and pushes in one clock, the leaving head overwritten | 12,481 |
| refused pushes and their drop clocks | 352,294 in 80,719 clocks |
| two or more faces dropping in one clock | 78,930 clocks |
| counter saturation (drop clocks with the counter held at 0xFFFF) | 4,096 |
| resets with arms queued / arms offered in reset | 36 / 366 |

**Controls.** The nine `armq_*` arms are KILLED, all at `2ff8183`:

| Arm | Named checks | Failing checks, round 1 -> round 2 |
|---|---|---|
| `armq_read_tail` | AQ2, AQ3 | 71 -> 72 |
| `armq_head_stuck` | AQ2, AQ3 | 2 -> 3 |
| `armq_ring_of_three` | AQ2, AQ3 | 11 -> 12 |
| `armq_write_at_head` | AQ2, AQ3 | 2 -> 3 |
| `armq_write_at_mid` | AQ2, AQ3 | 2 -> 3 |
| `armq_write_refused` (the review's `write_refused`) | AQ3 | survived -> 1 |
| `armq_write_wrap_hi` (`wr_wrap_hi`) | AQ3 | survived -> 1 |
| `armq_full_pop_refuses` (`full_pop_refuses`) | AQ3 | survived -> 1 |
| `armq_drop_skip_sat` (`drop_skip_sat`) | AQ3 | survived -> 1 |

- **Red proof.** The last four each pass round 1's bench: AQ 2 of 2, 1,653 checks, 0
  failures.
- **The review's probes.** Its `aq_probe.sh`, run unchanged at `2ff8183`, exits 1 for both
  probes: AQ3 fails on 8,272 edges for `write_refused` and on 19,343 for `wr_wrap_hi`.
- **The review's other controls.** Every control of its `gen.py --mutant` table fails AQ3.
  Its `hd_not_reset` probe passes, as an equivalent should.
- **On `main`'s RTL.** The drive passes on `main` `c050d971`'s RTL (the shift queue) with
  the same coverage, so AQ3 and AQ4 grade behaviour the change kept.
- **AQ4 is a guard against a vacuous drive.** It reads only the model, so it fails only if
  the drive stops reaching a state.

**Lockstep benches.** Both round-1 benches are published in this round's evidence packet as
run, with their cited result sets, digests (`SHA256SUMS`), and the regeneration steps for the
inputs they cut from processor sources (`GENERATED.sha256`). Each input was checked to
regenerate byte for byte.

**Validation at `2ff8183`.** All rc 0 unless stated. Each driver ran in the foreground with
its own log and was never piped.
- **Suites and static gates.**
  - `run_suites.sh`: 33 suites, 1,021,612 checks. Only `pp_top` moved (10,418 -> 10,420).
  - `lint_hdl.sh` 41 of 41.
  - `make check`: 1,123 links, 115 REQ rows, 94 matrix rows with 0 untested, 28 parameters.
  - `gen_matrix --check` passes.
  - `syn/yosys/run.sh`: 42 tops, one parse.
- **Campaigns.** Every arm's verdict and failing count is identical to round 1's run, apart
  from the nine ring arms above:
  - acmp 33 of 33 KILLED, with four goldens;
  - notify 47 of 47;
  - ctr 17 + 1 control;
  - aecp 55 + 5 controls;
  - aecp_dispatch 40 + 4 controls;
  - d3 110 of 110;
  - gsi 20;
  - name_wr;
  - adp 41 + 2 controls;
  - maap 29 + 3 controls.
- **Parent consumer set of 17.** The parent is milan-fpga dev `241f9184` with the same three
  patches, and the processor at `2ff8183`.
  - 15 of 17 pass, and gate 16's leg-defect step passes 5 of 5.
  - Gate 16 fails #643's two T30 checks, with result lines identical to round 1's (and
    `main`'s).
  - Gate 9 (xvlog) exits 1 only to bank PR #153's removed `pd_ix_w` finding in the parent's
    `scripts/xvlog.budget`. It does exactly the same with the processor at `main`
    `c050d971`. This is the adoption's step past `c050d971`.
  - Every other gate's figures match round 1, apart from the port-contract inventory below.
    `milan_dp`, for example, has 1,150 verdict lines, all identical.

## Round 2b

Assignment: milan-fpga #639 comment 5983576287. Both round-2 reviews (R462-2, R463-2) are
positive at `1cba30c9`. `main` then moved to `b0a74196` (PR #157, #81/#84), which changes
`protocol_processor_top.sv`, `tb/pp_top/sim_main.cpp`, `pp_top_wrap.sv`, the `tb/pp_top`
README and 08/09, as this lane does. Round 2b is that merge alone: `c725be1`, `--no-ff`
on `1cba30c9`.

- **The merge.** Its tree is `git merge-tree --write-tree`'s, so nothing was hand-merged.
  Each side's change reaches it unchanged: `hdl/` and `docs/` by patch-id, and `tb/` by
  its changed lines. This lane's RTL is byte-identical to `1cba30c`'s. The only HDL `main`
  adds is PR #157's GET_DYNAMIC_INFO classifier hunk.
- **Area.** A merge changes neither side's synthesized logic, so this lane's Vivado figures
  stand. No Vivado run was made.
- **Where the two sides meet.** The two timers PR #157's section TD grades, T-LOCK-UNLOCK
  and T-NOTIF-TIMELIMITED, are `KL_aecp_notify`'s. They are armed through the notification
  face, which is now a ring. In the merged sixth build TD passes with PR #157's own
  measurements: the auto-unlock 60,003 ms after the LOCK_ENTITY, the expiry 300,002 ms
  after the REGISTER, and 6 monitor probes answered.
  - TD's harness steps its own arm-port model ungraded. A scratch probe (not committed)
    printed its tally after TD: 30,003,382 edges, 3,456 arms issued, 0 edges differing.
  - HZ never reads the arm port. AQ's drive is still the first build's last stimulus: HZ8's
    batch check and HZ13 run inside `run_hazards`, before `run_arm_queue`. The sixth build
    never runs AQ.
  - No test depends on the other side's behaviour.

**Validation at `c725be1`.** All rc 0 unless stated. Each driver ran with its own log and
was never piped. Each record equals the union of the two sides.

| Gate | Result | The two sides |
|---|---|---|
| `run_suites.sh` | 33 suites, 1,021,627 checks | `1cba30c9` 1,021,612, + PR #157's 15 in `pp_top` (HZ +12, TD +3); every other suite line identical |
| `make -C tb/pp_top`, six builds | 10,435: default 9,947, fixture 20, identify 178, line 231, timebase 56, defaults 3 | Against `b0a74196`'s run (10,431), only AQ's three lines and the totals differ. Against `1cba30c`'s (10,420), only HZ 177 -> 189, the sixth build and the totals differ |
| AQ on `main` `b0a74196`'s RTL | AQ 4 of 4, both coverage lines equal to the README's | 09 §8.8's claim holds at the new `main` |
| `make check` | 1,136 links, 94 matrix rows with 0 untested, 28 parameters | base 1,131 + this lane's 3 + PR #157's 2 |
| `lint_hdl.sh`, `gen_matrix --check`, `syn/yosys/run.sh` | 41 of 41; 94 rows; 42 tops, one parse | |

| Campaign | Result | Against round 2 (`2ff8183`) |
|---|---|---|
| acmp `--jobs 3` | 33 of 33 KILLED, four goldens | identical: every arm's FAIL, AQ and tally lines, and `results.json` |
| aecp `--jobs 2` (HZ and TD arms) | 6 controls PASS, 61 KILLED | exactly PR #157's record: the `timer-defaults` control, its six arms, and `hz-stub-restored` 74 -> 81, `hz-acmp-reads-as-steps` 26 -> 27, `hz-barrier-no-priority` 127 -> 139 |
| notify `--jobs 2` | 47 of 47 | identical |
| d3 `--jobs 2` | 110 of 110, goldens PASS | identical, once the undefined `%d` already noted is ignored |
| ctr, aecp_dispatch, gsi, name_wr, adp, maap | 17 + 1; 40 + 4; 20; killed; 41 + 2; 29 + 3 | identical (aecp_dispatch but for the undefined `%d` already noted) |

**Docs.** The two sides' docs agree, and no doc commit was needed. Checked: 08 F08.1's
T-NOTIF-TIMELIMITED and T-LOCK-UNLOCK rows against 08 §3's arm-port bullet; 09 §3 TIM, §8.3
(TD, HZ) and §8.8 (AQ); and the `tb/pp_top` README's TD, HZ, AQ, six-build tables and both
campaign records.

**Parent consumer set** at milan-fpga dev `6c22d3ca` with four patches applied in order:
c8 (`-bbf704ec`), p2-p1, c10, and #232's `parent-adoption-232-241f9184.patch`
(`88ee5e96...`). The processor is at `c725be1`, in a scratch clone that was never
committed or pushed.
- All 17 gates are rc 0, plus gate 16's leg-defect step and `check_sh_idiom.py`.
  `milan_dp` reports 9 benches `RESULT: PASS`, 4 render mutants caught and gmstep 6 of 6.
- Each gate was compared with the manager's run at `1cba30c9` on the same parent. There
  are three differences: py-idiom's line count (+21, PR #157's arms), the xvlog pin line,
  and the builder's second not-run arm. That arm is gate 1b's `MAKEFLAGS += -e`, which
  this host's GNU Make 4.3 cannot exercise. Gate 16's 109 verdict lines and gate 15's
  1,174 are identical.
- Gate 9 passes (2 findings, equal to the ratchet), because #232's patch banks PR #153's
  `pd_ix_w`.
- Gate 16 passes too: 65 and 245 checks, and 5 of 5 leg defects. This dev carries #643's
  fix.
- The port gate counts 1,759 processor ports at the base, at both sides and at the head.
  It also counts test-only hierarchical observations: 230 at the base and at `b0a74196`,
  317 at `1cba30c9` and at the head. That count is an inventory, not a ratchet.

## Parent-visible list

- No port, parameter, register or behaviour change: the port gate counts 1,759 processor
  ports at `main` and at the head. This lane needs no parent patch.
- #639 asks for the resource gate's baseline to be re-recorded "in the same reviewed
  change". That file lives in the parent, so it is the pin adoption's re-baseline (#638's
  round-7 rule), and this PR says "Relates". The gate recommends it on all three endpoints.
- Past `c050d971` the pin carries PR #153. Its xvlog finding must be banked in the parent
  (#232's adoption line), not this lane's. With #232's patch applied, as in round 2b's
  consumer set, gate 9 passes at the head.
- Round 2 changes `hdl/` by one comment (`protocol_processor_top.sv:3002-3007`), so
  synthesis is unchanged. The resource gate's input digests do change, and the adoption's
  re-baseline measures the pin it adopts anyway.
- The parent's port-contract gate counts 297 test-only hierarchical observations, up from
  256: these are the drive's 41 `force` targets in `tb/pp_top/pp_top_wrap.sv`. The count is
  an inventory, not a ratchet, and the gate still passes. The test-evidence ratchet is
  unchanged (72 <= 77). At dev `6c22d3ca` the gate counts each reference. This lane's
  `tb/pp_top` adds 87, its 46 AQ taps and 41 `force` targets (230 -> 317), and PR #157
  adds none.
- Round 2b (the merge of `main` `b0a74196`) adds no parent-visible change of its own: no
  port, parameter or register, and the merged `hdl/` is this lane's plus PR #157's
  classifier hunk.

## Findings outside the scope

- **The drop counter counts a clock, not an arm.** Two faces overrunning in one clock read
  the same old `arm_drop_r`, so they add one (snapshot word 24). This is kept as it is,
  because a behaviour change is outside this lane. Section AQ records the rule.
- **#638's gate hashes sources from the parent tree at check time.** A check is only
  meaningful with the parent's processor at the measured revision.
- **`tb/pp_top/d3_phases.hpp:2963` and `:2993`** (on `main`): two D3 check messages have a
  `%d` with no argument (the build's two `-Wformat` warnings). The checks are unaffected;
  only the printed number is undefined.

## How to validate

```sh
./scripts/run_suites.sh
./scripts/lint_hdl.sh
make check && python3 scripts/gen_matrix.py --check
./syn/yosys/run.sh
python3 tb/pp_top/acmp_mutants.py --output DIR --jobs 2
make -C tb/pp_top gsi-build && (cd tb/pp_top && ./obj_dir/Vpp_top_sim --arm-queue-only)
make -C tb/pp_top
```

Expected: every command exits 0. The ACMP campaign reports 33 of 33 KILLED and four
goldens PASS. `--arm-queue-only` prints its two coverage lines and `AQ: 4 checks, 0
failures`: traffic reaches 8,270 arms and 0 pushes onto a face still holding one, and the
drive reaches every state listed in Round 2. `make -C tb/pp_top` ends with `10435
checks: 10435 PASS, 0 FAIL` over its six builds. For the area figures, run milan-fpga's
`docs/testing/PP_SHADOW_BASELINE_RECIPE.md` on a parent with this head pinned.

**Manager merge (round 2).** Processor `main` `07b1469d` (PR #154) merged at `1cba30c9` with no conflicts; the one shared file, `docs/guides/hdl-engineer.md`, merged in separate hunks. Donor and parent consumer re-run at that head.

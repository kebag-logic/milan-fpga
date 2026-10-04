[A525]

Relates to milan-fpga#639
Relates to milan-fpga#229

The #639 area lane: levers 3 and 6 of epic milan-fpga#229, from the #234 baseline
(milan-fpga PR #638) (assignment: milan-fpga #639 comment 5976100204). Branch
`pp639-armq-lsnrec` from `main` `5c71928a`, with `main` merged twice as it moved
(`83999eba`, then `c050d971`); seven commits, head `9e86991`.

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
    arms), so the full-queue path is the lockstep bench's.
  - Five ring controls are KILLED by AQ2.
  - AQ passes on `main`'s RTL with identical coverage.
- **Check RS in `tb/acmp_listener`.** A reset taken with records bound must leave every
  record zero in the RAM.
  - The misaddressed-sweep control survived the suite before RS and fails 37 checks with it.
  - Five record controls are KILLED.
  - RS passes on `main`'s RTL.

## Validation

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

## Parent-visible list

- No port, parameter, register or behaviour change: the port gate counts 1,759 processor
  ports at `main` and at the head. This lane needs no parent patch.
- #639 asks for the resource gate's baseline to be re-recorded "in the same reviewed
  change". That file lives in the parent, so it is the pin adoption's re-baseline (#638's
  round-7 rule), and this PR says "Relates". The gate recommends it on all three endpoints.
- Past `c050d971` the pin carries PR #153. Its xvlog finding must be banked in the parent
  (#232's adoption line), not this lane's.

## Findings outside the scope

- **The drop counter counts a clock, not an arm.** Two faces overrunning in one clock read
  the same old `arm_drop_r`, so they add one (snapshot word 24). This is kept as it is,
  because a behaviour change is outside this lane. Section AQ records the rule.
- **#638's gate hashes sources from the parent tree at check time.** A check is only
  meaningful with the parent's processor at the measured revision.

## How to validate

```sh
./scripts/run_suites.sh
./scripts/lint_hdl.sh
make check && python3 scripts/gen_matrix.py --check
./syn/yosys/run.sh
python3 tb/pp_top/acmp_mutants.py --output DIR --jobs 2
make -C tb/pp_top gsi-build && (cd tb/pp_top && ./obj_dir/Vpp_top_sim --arm-queue-only)
```

Expected: every command exits 0. The ACMP campaign reports 29 of 29 KILLED and four
goldens PASS. `--arm-queue-only` prints `AQ: 2 checks, 0 failures` and its coverage line
(8,270 arms, 0 pushes onto a face still holding one). For the area figures, run milan-fpga's
`docs/testing/PP_SHADOW_BASELINE_RECIPE.md` on a parent with this head pinned.

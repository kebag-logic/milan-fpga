[A756]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN — every round 2 gate rc 0 on a clean clone of the head: `pp_shadow` in every leg (base 738, vid73 738, crf 778, pending 317 checks, 0 failures), `drops-mutant` 8 of 8, the resource gate, docs.yml 65 steps 0 bad; the sixteenth resource record fits (15,820 of 15,850 slices, WNS +0.166 ns) — `854-shadow-drop-count` -> `dev`. Base `dev` `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`, the live `dev`
tip, so the head is its own merge result. Head `de71984e4fc1b568065dffec483ea3ff51518604` (five commits; round 2 adds
the last four to round 1's `e87f2179`).

## Linked Issue / roles

Closes #854
Relates to #853, #495

Executor: `[A756]`
Internal cleared-context reviewer: `[R803]`
External reviewer: `[R804]`

## Description

`KL_pp_shadow`'s control-frame drop counter (`rx_drops_o`, `PP_DIAG[15:8]`) could not count. The all-fabric tap's FIFO
is `axis_fifo` with `FRAME_FIFO=1, DROP_WHEN_FULL=1`. In that configuration verilog-axis holds `s_axis_tready` at 1
and drops by itself a frame it has no room for. The old `drop_evt_w = fw_valid_w & ~fw_ready_w` was therefore
constant 0. This PR applies #853's counting method, written for the split placement's tap, to this tap. Round 2
(the ruling on #854 of R803-1 and R804-1) re-baselines the area, corrects the area text and two wordings, and adds a
runt leg and an oversize leg to `[DR]`. The RTL logic is round 1's; round 2 changes RTL comments only.

| Commit | Change |
|---|---|
| `e87f2179` | `hdl/milan/KL_pp_shadow.sv`: `drop_evt_w` reads the FIFO's own `status_overflow` (now connected), counted only after the last beat of a frame the tap kept (`last_kept_r`: an `FW_BODY` frame, or an `FW_HEAD1` frame with `accept_w`); a refused frame or a runt ends marked bad and is not counted; the existing `!= 8'hFF` guard saturates at 255. `pp_shadow` section `[DR]` (`--drops-only`), `drops_probes.vlt`, `drops_mutant.py` with six arms, README, `TESTING.md`, `REGISTER_MAP.md` prose. |
| `7a19f62b` | Comment lines only: the banner, the drop-logic comment and the `rx_drops_o` port comment of `KL_pp_shadow.sv`, `milan_csr.sv`'s `i_pp_rx_drops` port comment, and the `PP_DIAG` register row now say "lost to a full FIFO, or longer than the FIFO" (R803-1-F3). These are the measured synthesis inputs. |
| `4d6a165c` | `[DR]` gains a runt sub-leg, run in every build, and an oversize sub-leg. The Makefile's `RXFILT=0` builds the base leg with `rx_mac_filter` pruned (`RXFILT_P = 0`, the builder's `--no-rx-mac-filter`). `drops-mutant` runs two clean controls (the base leg, and the base leg with `RXFILT=0`) and eight arms, two of them new: `misses-oversize` and `counts-runts` (R804-1-S1). README (including R803-1-F2 / R804-1-R2) and `TESTING.md`. |
| `3a7660b1` | `syn/ooc/pp_resource_baseline.json`: all three endpoints re-recorded by `pp_resource_gate.py record --write` at `7a19f62b`, with the `measured` notes naming #854 (R804-1-F1, option a). |
| `de71984e` | The area pages, as earlier re-baselines did: `docs/design/AREA_BUDGET.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` (a new section for the sixteenth record), `docs/findings/README.md`, `docs/design/MARK_II_AREA_PLAN.md`, `CHANGELOG.md`. |

No processor or submodule change. `KL_gptp_shadow.sv` is unchanged, because its tap already counts from
`status_overflow`.

### `[DR]` at the head

The same figures in each of the base, vid73 and crf legs:

- **Burst:** 108 frames offered (100 of 64 bytes, then 8 of 16 bytes), 77 handed out, 31 lost, and the count reads 31.
- **Refused frames:** 69 kept frames lost and the count rises by 69. The FIFO raised 158 overflows; the other 89
  were refused frames that met the full FIFO.
- **Runts:** 100 frames of 64 bytes, then 100 pairs of a 16-byte frame and an 8-byte, one-beat runt. 108 kept
  frames lost and the count rises by 108. In the suite's builds `rx_mac_filter` drops every runt ahead of the tap, so
  the FIFO raised 108 overflows, one per kept frame lost. In the `RXFILT=0` build runts reach the tap: 157 overflows,
  and still a count of +108.
- **Longer than the FIFO:** a 4,096-byte ADP frame (512 words, the FIFO's depth) into the empty FIFO is kept, handed
  out whole and not counted. A 4,097-byte one is dropped by the FIFO although it is empty: one overflow, the count
  rises by one, and the 64-byte frame behind it is handed out.
- **Saturation:** 501 frames lost in all, and the count reads 255 and holds there.

| Arm | Leg | Plant | Named check that fails |
|---|---|---|---|
| `count-removed` | base | the count's increment ANDed with 0 | DR a burst past the FIFO loses frames and counts them |
| `count-from-tready` | base | `drop_evt_w = fw_valid_w & ~fw_ready_w`, the construction #854 reported | the same |
| `counts-refused` | base | every FIFO overflow counted | DR ...and are not counted: the kept frames lost equal the count |
| `misses-second-beat` | base | a frame kept at `FW_HEAD1` not counted | DR the burst's lost frames equal the drop count |
| `wraps` | base | the `!= 8'hFF` guard removed | DR the count saturates at 255 |
| `diag-tied-off` | base | `milan_datapath`'s `.i_pp_rx_drops` ANDed with 0 | DR a burst past the FIFO loses frames and counts them |
| `misses-oversize` | base | a beat counter leaves uncounted a frame of more than 512 words | DR the frame longer than the FIFO is counted |
| `counts-runts` | `RXFILT=0` | `last_kept_r` also set at `FW_HEAD0`, so a runt the full FIFO turns away is counted | DR ...and runts are not counted: the kept frames lost equal the count |

Both clean controls pass, and all eight arms are KILLED by their named checks.

### Area: the sixteenth resource record

On `dev`, `drop_evt_w` is constant 0, so synthesis removes the 8-bit count and the FIFO's overflow register. Both now
exist, with `last_kept_r`, so the change moves the shipping image, and `docs/design/AREA_BUDGET.md` (the re-baseline
rule) has its PR re-measure the three endpoints on its merge result. From the fifteenth record's measured commit
`e44a4d20` to `dev` `ac0a01e3` no synthesis input moves (the diff holds documentation, testbench files and the
baseline JSON only), so the differences below are this change's, and on the route the selected directive's.

All six Vivado runs used the recipe (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`) at `7a19f62b`, with
`--single-thread-synthesis`. They were: the 1x1 route at all three placement directives from one synthesis
checkpoint, `ooc-1x1`, and `ooc-8x8` with its RTL elaboration. Each ran under the slot wrapper, at most three at once,
and each returned rc 0.

| Directive | WNS / WHS, worst corner | LUT | FF | Slice | Free |
|---|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt, selected | +0.166 / +0.032 ns | 53,534 | 54,850 | 15,820 | 30 |
| AltSpreadLogic_high | +0.147 / +0.036 ns | 53,513 | 54,847 | 15,846 | 4 |
| ExtraTimingOpt | +0.127 / +0.036 ns | 53,512 | 54,847 | 15,846 | 4 |

The gate selects ExtraPostPlacementOpt, the shipping directive. Its corners are Slow_0C and Slow_85C at WNS +0.166 ns
and WHS +0.050 ns, and Fast_0C and Fast_85C at WNS +1.633 ns and WHS +0.032 ns. Every route is complete, with no
unrouted net and no routing error. **No STOP:** 15,820 slices is under 15,850, and WNS +0.166 ns is above the
+0.030 ns floor at every corner. These figures equal round 1's single route at `e87f2179`, whose synthesis inputs
differ from `7a19f62b` only in comment lines.

**The change at one directive (R803-1-F1).** Record 15 selected AltSpreadLogic_high, so a comparison against the
record crosses directives. Record 15's own ExtraPostPlacementOpt route
(`docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, the fifteenth record's section) is the same directive on the same
base:

| Figure | Record 15, ExtraPostPlacementOpt | Head, ExtraPostPlacementOpt | Change |
|---|---:|---:|---:|
| LUT | 53,383 | 53,534 | +151 |
| FF | 54,837 | 54,850 | +13 |
| Slice | 15,848 | 15,820 | -28 |
| WNS / WHS, worst corner | +0.112 / +0.036 ns | +0.166 / +0.032 ns | +0.054 / -0.004 ns |

At one directive WNS rose by 0.054 ns. So the 0.044 ns fall against the record (below) belongs to the change of
selected directive, not to this RTL.

**The tap's own share (R803-1-F1).** The gate's `wrapper` row is the `KL_pp_shadow` instance total, its children
included (`u_pp`, `ctl_fifo`, `u_nvm`). The tap's own logic is the wrapper less those children:

| Scope | `route-1x1` LUT / FF | `ooc-1x1` LUT / FF | `ooc-8x8` LUT / FF |
|---|---:|---:|---:|
| the wrapper, the instance total | +35 / +10 | +10 / +10 | +10 / +10 |
| `u_pp`, the processor (RTL unchanged) | +27 / 0 | 0 / 0 | 0 / 0 |
| `ctl_fifo` | +1 / +1 | +3 / +1 | +4 / +1 |
| `u_nvm` | -1 / 0 | 0 / 0 | 0 / 0 |
| the tap's own logic | +8 / +9 | +7 / +9 | +6 / +9 |

The tap's own share is +9 FF, the 8-bit count and `last_kept_r`, and about +8 LUT (+6 to +8 across the three
endpoints). `ctl_fifo` adds +1 FF, its overflow register. Out of context the processor does not move, so the
standalone rows are the change alone. On the route, `u_pp`'s +27 LUT is placement and optimization across two
directives, and the area budget counts it against the change all the same.

**The new record against record 15.** `pp_resource_gate.py check` against record 15 gives exit 0 on all three
endpoints:

| Endpoint | LUT | FF | Slice | RAMB36 / RAMB18 / DSP | WNS ns | WHS ns |
|---|---:|---:|---:|---:|---:|---:|
| `route-1x1` (ExtraPostPlacementOpt against record 15's AltSpreadLogic_high) | 53,534 (+106 of 500) | 54,850 (+13 of 600) | 15,820 (-9 of 80) | 74 / 27 / 15 (0) | +0.166 (-0.044) | +0.032 (-0.004) |
| `ooc-1x1` | 25,209 (+10 of 250) | 21,020 (+10 of 250) | - | 16 / 3 / 8 (0) | +3.327 (0) | +0.159 (0) |
| `ooc-8x8` | 37,058 (+10 of 316) | 32,126 (+10 of 339) | - | 21 / 5 / 8 (0) | +1.139 (0) | +0.159 (0) |

Then `record --write` wrote all three endpoints, and the `measured` notes name #854, `7a19f62b` and the
one-directive comparison. `check-baseline` passes, and `check` exits 0 on all three against the new record. Every
tolerance, floor and ceiling is unchanged. All 18 image-manifest entries were rehashed after measurement and match,
and no log carries `Synth 8-4445`. The routed critical setup path has 37 logic levels on the processor's 20 ns
clock, inside the wrapper and outside the tap: `u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][1]` to
`u_pp/u_aecp/u_d3/deb_cnt_r_reg[13]`, with 19.393 ns of data delay, of which 12.899 ns is routing.

## Authoritative references

- #854, its Required items; the round 2 ruling on #854; #853, the counting method for the split tap.
- The counter is a project diagnostic, and no standard defines it. The frames it counts are the tap's classified
  set: EtherType 0x22F0 (IEEE 1722-2016), which carries IEEE 1722.1-2021 clause 6 ADP, clause 8 ACMP and clause 9
  AECP, and MSRP (IEEE 802.1Q-2022 clause 35.2) and MVRP (IEEE 802.1Q-2022 clause 11.2) at their group addresses.
- `third_party/verilog-axis/rtl/axis_fifo.v` at the pinned revision: `s_axis_tready` is held at 1 when
  `DROP_WHEN_FULL` is set (`:217`); a frame that meets a full FIFO, or that is longer than its whole depth (`full_wr`
  with `DROP_OVERSIZE_FRAME`), is dropped, and `overflow_reg` rises the cycle after its last beat (`:271-284`).
- `docs/reference/REGISTER_MAP.md`, `PP_DIAG[15:8]`.
- `docs/design/AREA_BUDGET.md`, the re-baseline rule; `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, the recipe and
  the resource gate.

## How to get into the same state

```sh
git fetch origin 854-shadow-drop-count
git checkout --detach de71984e4fc1b568065dffec483ea3ff51518604
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
make -C tb/verilator/pp_shadow build-base exec-base SIM_ARGS=--drops-only
make -C tb/verilator/pp_shadow build-base exec-base RXFILT=0 BUILD_DIR=obj_rxfilt0 SIM_ARGS=--drops-only
make -C tb/verilator/pp_shadow drops-mutant
make -C tb/verilator/pp_shadow
python3 syn/ooc/pp_resource_gate.py --selftest
python3 syn/ooc/pp_resource_gate_mutants.py
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 scripts/docs_inventory.py --check
git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD
```

Expected result / pass criteria: every command exits 0. Each `--drops-only` run prints the `[DR]` figures above,
with no failing check. `drops-mutant` ends `PASS: [DR] catches every arm (8 of 8); both clean controls pass`. The
area figures need the recipe's Vivado runs (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, Resource gate).

Local gates on a clean clone of the head:

| Gate | rc | Result |
|---|---:|---|
| `make -C tb/verilator/pp_shadow` (every leg: base, vid73, crf, pending) | 0 | base 738, vid73 738, crf 778 and pending 317 checks, 0 failures; `[DR]` runs in base, vid73 and crf with the figures above, and the pending leg (`--pending-only`) does not run it |
| `make -C tb/verilator/pp_shadow drops-mutant` | 0 | `PASS: [DR] catches every arm (8 of 8); both clean controls pass` |
| `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | `resource gate selftest: 312 arms and 500 generated cases PASS` |
| `python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py` | 0 | `resource gate mutants: control passes, all 236 mutants fail` |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` |
| every `run:` step of `.github/workflows/docs.yml`, each job on its own clean clone | 0 | 65 steps ran, 31 not run with a reason (hosted orchestration, or provisioning this host already carries), 0 bad; every job's tree clean after it |
| `python3 scripts/docs_inventory.py --check` | 0 | `documentation inventory: OK` |
| `git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD` | 0 | no output |
| `python3 syn/ooc/pp_resource_gate.py check` on `route-1x1` (route set), `ooc-1x1`, `ooc-8x8`, against record 15 and then against the new record | 0 (each) | `RESULT: PASS` |

The RTL logic is round 1's (round 2 changes comment lines only), so, per the ruling, the full sweep was not re-run in
round 2. Round 1's full sweep at `e87f2179` passed 65 of 65 suites as four shards.

## Known limitations / out of scope

- **The consumer is not stalled in the test.** The #853 probe stalled the mailbox. This tap's consumer is the
  serializer into the processor, which has no ready (`ff_ready_w = ~ser_busy_r`). It pops a word in one cycle and
  sends it one byte a cycle, so it drains eight bytes every nine cycles. The test keeps the probe's burst (100
  back-to-back 64-byte ADP frames), and at eight bytes a cycle the burst outruns the drain. Frames lost are measured
  as frames offered less frames handed out.
- **The runt leg is not a default leg.** In the suite's builds `rx_mac_filter` drops every runt ahead of the tap, so
  `[DR]`'s runt sub-leg in the three legs that run it shows only that no runt reaches the FIFO, and `counts-runts` is an equivalent
  mutant in those builds. The build where runts reach the tap is the base leg with `RXFILT=0`, and `drops-mutant`
  builds and runs it, as a clean control and as `counts-runts`' leg. It is not a fifth case of `make run`, because a
  new case re-targets the hosted `pp_shadow` piece windows (`scripts/suite_shards.py`, `PIECE_SECONDS`, #804).
- **Reset during an overflow burst is not graded.** The ruling moves it to the residue checklist #495 (R803-1-F4).
- No change to `KL_gptp_shadow`, to the processor or to any submodule.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

# 854-a756b HANDOFF (round 2)

**Status: REVIEW READY. Every round 2 gate is rc 0 on a clean clone of the head, and the sixteenth resource record fits (no STOP).** Lane `854-shadow-drop-count`, base `dev` `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36` (the live
`dev` tip, so the head is its own merge result). Round 1 head `e87f2179`; round 2 head
**`de71984e4fc1b568065dffec483ea3ff51518604`** (four commits on round 1). Nothing pushed. TAKEN posted on #854
(issuecomment-6740009884); REVIEW READY posted (issuecomment-6743149561). `PR-BODY.md` is ready for the manager, with `Closes #854`.

## 1. Authority

The round 2 ruling on #854 (issuecomment-6739837279), on R803-1 (PR #862 issuecomment-6739803406) and R804-1
(issuecomment-6739815400). Its five items and where each is met:

| Ruling item | Met by |
|---|---|
| 1. Re-baseline: the 1x1 route set at three directives, `ooc-1x1`, `ooc-8x8`, `record --write`, area page and findings entries; `check-baseline` passes; STOP if over 15,850 slices or under the WNS floor | `3a7660b1`, `de71984e`; section 4. No STOP: 15,820 slices, WNS +0.166 ns |
| 2. Area text (R803-1-F1): wrapper as the instance total, the tap's own share, the same-directive comparison, then the new record against record 15 | `PR-BODY.md` "Area"; findings section; AREA_BUDGET paragraph |
| 3. Drain-rate wording (R803-1-F2, R804-1-R2) and per-leg tally (R804-1-R1) | README `:175`, `sim_main.cpp:94-95`, PR-BODY limitations; PR-BODY gate table per leg |
| 4. Runt leg in a `-GRXFILT_P=0` build killing `counts-runts`; oversize frame graded in `[DR]`; port comment and register row | `4d6a165c`, `7a19f62b` |
| 5. Reset during an overflow burst: residue (#495), not this round | not done, by the ruling; PR-BODY limitations |

## 2. Changes (round 2)

| File:line | Change | Why |
|---|---|---|
| `hdl/milan/KL_pp_shadow.sv:72-75` (banner), `:752` (`rx_drops_o`), `:857-866` (drop logic) | comments only: "lost to a full FIFO, or longer than the FIFO"; the drop comment names `DROP_OVERSIZE_FRAME` | R803-1-F3, ruling 4. `axis_fifo.v:275` drops a frame for `full && DROP_WHEN_FULL` or `full_wr && DROP_OVERSIZE_FRAME`, and `:283` raises `overflow_reg` for both |
| `hdl/common/csr/milan_csr.sv:699` | comment only: `i_pp_rx_drops` "control frames lost to a full FIFO, or longer than the FIFO" | the same contract at the CSR port |
| `docs/reference/REGISTER_MAP.md:2456` (`PP_DIAG` row), `:2469-2472` | "or longer than the FIFO"; the row's em dash becomes `--` (the added-line gate) | ruling 4 |
| `tb/verilator/pp_shadow/sim_main.cpp:144-149` | `RXFILT_PRUNED` default 0 | the build define |
| `sim_main.cpp:2057-2058` | `kRuntsReachTheTap` | |
| `sim_main.cpp:2062-2098` `grade_runts_at_a_full_fifo_are_not_counted()` | 100 x 64 B, then 100 x (16 B kept + 8 B runt). Filtered build: overflows == kept lost (no runt reaches the FIFO). Pruned build: overflows > kept lost. Both: count == kept lost; kept frames whole and in order | R804-1-S1, ruling 4 |
| `sim_main.cpp:2100-2126` `grade_a_frame_longer_than_the_fifo_is_counted()` | a 4,096-byte frame (512 words) into the empty FIFO: kept, whole, 0 overflows, not counted; a 4,097-byte one, then 64 B: 1 overflow, count +1, the 64 B frame handed out | R803-1-F3, ruling 4 (the boundary both sides) |
| `sim_main.cpp:2181-2189` | `[DR]` calls both; the flood's total includes their losses | |
| `sim_main.cpp:89-105` | the section banner: drain rate, runts, oversize | R803-1-F2 / R804-1-R2 |
| `tb/verilator/pp_shadow/Makefile:163-171` | `RXFILT ?= 1`; `RXFILT=0` adds `-GRXFILT_P=0 -CFLAGS "-DRXFILT_PRUNED=1 -Wall -Wextra"` to `build-base`; `clean` removes `obj_rxfilt0` | the pruned build, one knob for both flags; the C++ idiom gate wants `-Wall -Wextra` in every `-CFLAGS` |
| `tb/verilator/pp_shadow/drops_mutant.py` | two controls (`RXFILT=1`, `RXFILT=0`); each arm carries its leg; two new arms | ruling 4 |
| `tb/verilator/pp_shadow/README.md:14`, `:165-211` | the section: drain rate (R803-1-F2's exact fix), runts, oversize, the `RXFILT=0` command, the eight-arm table with legs | |
| `docs/testing/TESTING.md:748` | the pp_shadow row | |
| `syn/ooc/pp_resource_baseline.json` | three records by `record --write`; the `measured` notes by `receipts/scripts/set_measured.py` (refuses unless only the notes differ from the recorder's output) | ruling 1 |
| `docs/design/AREA_BUDGET.md:13`, `:133-138`, `:152-160`, `:224`, `:241-264`, `:278-281`, `:693-698` | header pointer, the record chain, the gate table, the #854 paragraph (route set, one-directive comparison, the tap's share, critical path), the allocation figures, the sixteenth ledger entry | ruling 1, 2 |
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:15-16`, `:22`, `:28-29`, `:53-172` | pointers, Contents, the new section "Re-baseline of 2026-11-09, the control-frame drop count" | ruling 1, 2 |
| `docs/findings/README.md:25`, `docs/design/MARK_II_AREA_PLAN.md:59`, `:940-941`, `CHANGELOG.md:11`, `:59-84` | the current record's pointers; the +0.166 ns WNS record; the CHANGELOG section | ruling 1 |

The counter is a project diagnostic, and no standard defines it. The frames it counts are the tap's classified set:
EtherType 0x22F0 (IEEE 1722-2016, carrying IEEE 1722.1-2021 clause 6 ADP, clause 8 ACMP and clause 9 AECP), and
MSRP (IEEE 802.1Q-2022 35.2) and MVRP (IEEE 802.1Q-2022 11.2) at their group addresses.

**The RTL logic is unchanged** from round 1 (`git diff e87f2179 7a19f62b -- hdl` is comment lines only), so per the
ruling no full sweep was run.

**Decision made public (PR-BODY limitations):** the `RXFILT=0` leg is built and run by `drops-mutant` (as a clean
control and as `counts-runts`' leg), not added as a fifth `make run` case: a new case re-targets the hosted
`pp_shadow` piece windows (`scripts/suite_shards.py` `PIECE_SECONDS`, keyed by leg index, #804). In the three default
legs that run `[DR]` (base, vid73, crf) the runt sub-leg still runs and grades that no runt reaches the FIFO.

## 3. New checks, their planted mutants and failing words

| Check (failing words) | Arm | Leg | Plant |
|---|---|---|---|
| `DR the frame longer than the FIFO is counted` | `misses-oversize` | base | a 10-bit beat counter; `drop_evt_w` also ANDed with "the frame had over 512 words" negated |
| `DR ...and runts are not counted: the kept frames lost equal the count` | `counts-runts` | `RXFILT=0` | `last_kept_r` also set at `FW_HEAD0` |
| `DR the runt burst loses kept frames`, `DR with the filter pruned the runts meet the full FIFO` / `DR the filter drops every runt ahead of the tap: one overflow per kept frame lost`, `DR ...the kept frames of the runt burst handed out whole and in order` | (any arm removing the count also fails the count check) | both | |
| `DR a frame as long as the FIFO is kept and handed out whole`, `DR ...and is not counted`, `DR a frame longer than the FIFO is lost and the frame behind it handed out` | | base | |

Result at the head on the clean clone (`gates/final/drops_mutant.log`): both clean controls PASS; 8 of 8 KILLED by
their named checks (count-removed 7 failing checks, count-from-tready 7, counts-refused 3, misses-second-beat 3, wraps
2, diag-tied-off 7, misses-oversize 1, counts-runts 2). `counts-runts` in a filtered build is an equivalent mutant
(R804-1's finding), which is why its leg is `RXFILT=0`.

## 4. Area: the sixteenth record (no STOP)

Six Vivado runs at `7a19f62b` (clean clones `aclone`, `aclone8`), recipe form, `--single-thread-synthesis`, each
under `vivado-slot.sh` in its own scope (MemoryMax 14G), at most three at once, on this unit's CPUs. All rc 0
(`receipts/area/runs/runs.md`, peak 8,537 MB). Units `milan-854-a756b-chain1`, `-chain8`
(`receipts/scripts/chain1.sh`, `chain8.sh`).

| Directive | WNS / WHS worst | LUT | FF | Slice | Free |
|---|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt, **selected** | +0.166 / +0.032 | 53,534 | 54,850 | 15,820 | 30 |
| AltSpreadLogic_high | +0.147 / +0.036 | 53,513 | 54,847 | 15,846 | 4 |
| ExtraTimingOpt | +0.127 / +0.036 | 53,512 | 54,847 | 15,846 | 4 |

- **STOP conditions:** not met. 15,820 <= 15,850 slices; WNS +0.166 ns >= 0.03 ns at every corner (Slow +0.166,
  Fast +1.633); WHS +0.032 >= 0.
- **Against record 15** (`area/record/check-r15-*.log`, all rc 0): route +106 LUT, +13 FF, -9 slices, RAM/DSP 0,
  WNS -0.044, WHS -0.004; `ooc-1x1` +10 / +10; `ooc-8x8` +10 / +10.
- **Same directive** (record 15's own EPPO row, 53,383 / 54,837 / 15,848 / +0.112 / +0.036): +151 LUT, +13 FF, -28
  slices, WNS +0.054, WHS -0.004.
- **The tap's own share** (wrapper less `u_pp`, `ctl_fifo`, `u_nvm`, from the records' scopes): route +8 LUT / +9
  FF, `ooc-1x1` +7 / +9, `ooc-8x8` +6 / +9; `ctl_fifo` +1/+1, +3/+1, +4/+1; `u_pp` +27 LUT on the route only.
- **Determinism:** the EPPO figures equal round 1's route at `e87f2179` (same corners too).
- **Record:** `area/record/record-*.log` rc 0; `set-measured.log`; `after-check-baseline` rc 0 (`baseline PASS: 3
  endpoints`); `after-*` checks rc 0.
- **Inputs:** `area/input-diffs.txt`: `e44a4d20..ac0a01e3` documentation, testbench and the JSON only;
  `ac0a01e3..7a19f62b` synthesis inputs `KL_pp_shadow.sv`, `milan_csr.sv` (comment); `7a19f62b..HEAD` no synthesis
  input. 18 of 18 image entries rehashed and match (`area/runs/images.md`). `Synth 8-4445`: 0. `Synth 8-6901`: one
  per synthesis log, `crft_emit_en_w`.
- **Paths** (`area/paths/<directive>/summary.md`, each PASS): EPPO worst setup 37 levels,
  `u_aecp/u_ucpu/uop_e_r_reg[imm][1]` to `u_aecp/u_d3/deb_cnt_r_reg[13]` R, 19.393 ns (12.899 routing), 20 ns clock;
  worst hold in the SoC at +0.032 (fast).

## 5. Gates (clean clone `fclone` of the head `de71984e`, all rc 0)

Receipts: `receipts/gates/final/` (`gates.sh`; logs over 200 KB by sha256 and size in `LARGE-FILES.sha256`, with
`pp_shadow.excerpt.txt` holding each leg's exec line, `[DR]` lines and tally) and `receipts/gates/docsyml-de71984e/`
(`docsyml_all.sh`, `run_docs_yml.py`, `verify_docs_yml.py`, `not_run.json`). Units `milan-854-a756b-final` (CPUs
40-47) and `milan-854-a756b-finaldocs` (8-15), each booked with `cpu_ranges.py pick`.

| Gate | Command | rc | Log shows |
|---|---|---:|---|
| diff check | `git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD` | 0 | no output |
| docs inventory | `python3 scripts/docs_inventory.py --check` | 0 | `documentation inventory: OK (547 lines, docs/DOCUMENTATION_AUDIT.md is fresh)` |
| resource gate self-test | `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 | `resource gate selftest: 312 arms and 500 generated cases PASS` |
| resource gate mutants | `python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py` | 0 | `resource gate mutants: control passes, all 236 mutants fail` |
| check-baseline | `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` |
| pp_shadow, every leg | `make -C tb/verilator/pp_shadow run` (`MAKEFLAGS=-j8 --no-print-directory --output-sync=target`) | 0 | vid73 738, base 738, crf 778, pending 317 checks, 0 failures (the order they finished); `[DR]` in base, vid73 and crf: burst 31/31, refused +69/+69 (158 overflows), runts +108/+108 (108 overflows, filtered), 4,096 B kept, 4,097 B lost and counted, 501 lost in all, 255 |
| drops-mutant | `make -C tb/verilator/pp_shadow drops-mutant` | 0 | `PASS: [DR] catches every arm (8 of 8); both clean controls pass` |
| docs.yml | every `run:` step, each job on its own fresh clone | 0 | `65 steps ran, 31 not run with a reason, 0 bad`; verify.rc 0; every job's tree clean after it |
| resource gate on the measurements | `pp_resource_gate.py check` x3 against record 15, `record --write` x3, `check-baseline`, `check` x3 against the new record (in the lane) | 0 (each) | `area/record/*.log` |

The clone's tree after the gates (`gates/final/tree-after.txt`) shows only ignored build products (`obj_*`,
`__pycache__`, the two generated ROM images); nothing tracked changed.

**Pre-checks at `4d6a165c`** (not the head, superseded): the same non-docs gates rc 0
(`gates/pre-4d6a165c/`), and docs.yml `65 steps ran, 31 not run with a reason, 0 bad` (`gates/docsyml-4d6a165c-pre/`).
**Dev runs in the lane** (`gates/dev-lane/`): the first `drops-mutant` 8 of 8 and the full base leg 738 checks, before the
`[DR]` helpers were split for the C++ idiom gate's 100-line function limit (`check_cpp_idiom.py` rc 0 after).

## 6. Timeline (CET, 2026-11-09)

- 13:18: started round 2. Read both reports and the ruling.
- 13:25: commit `7a19f62b` (comments); Vivado chains launched; TAKEN posted.
- 13:3x-13:4x: `[DR]` legs, arms; dev `drops-mutant` 8 of 8; C++ idiom fix; commit `4d6a165c`; pre-check gates.
- 14:04: EPPO synthesis done (37.5 min); ooc-8x8 rc 0; comparison routes and ooc-1x1 started.
- 14:33 / 14:50: EPPO, then ETO done; all six rc 0; no STOP.
- 14:5x: record, notes, check-baseline; commits `3a7660b1`, `de71984e`.
- 14:58: final gates launched on `fclone`.
- 15:53: final gates all rc 0 (docs.yml 65 ran, 0 bad); receipts collected; REVIEW READY posted on #854 with the head `de71984e` (issuecomment-6743149561; the text is `REVIEW-READY.md`). Round complete; nothing pushed.

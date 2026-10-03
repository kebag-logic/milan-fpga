[A516]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY: 44/44 touched local gates rc 0 under GNU Make 4.3; gate self-test 51 arms, 25/25 mutants killed -- `234-area-baseline` -> `dev`. Head `2a765a6c3868400c20ede2e357876f28a811c811`. No RTL, processor or interface change.

## Linked Issue / roles

Relates to #234
Relates to #229

Executor: `[A516]`
Internal cleared-context reviewer: `[R446]`
External reviewer: `[R447]`

## Description

Issue #234's first step under epic #229: the authoritative baseline, the 1x1 ranking, the budget and a resource-regression gate.

| Piece | Change |
|---|---|
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` | New. Vivado baseline of the current head (A: dev `1269cdaf`, processor `631eeb34`) and of the next adoption (B: processor `ddb3119d` with the C8 and P2 parent patches, a scratch tree). Integrated 1x1 route, standalone 1x1 and 8x8 synthesis at the build's 50 MHz clock, per-sub-block LUT/FF/RAMB/DSP/CARRY4, storage mapping with source lines, Yosys reconciliation, the 1x1 reduction ranking and run receipts. |
| `docs/design/AREA_BUDGET.md` | New section: NFR-RES-01's 60 % LUT target against the measured image, the open allocation decision, the gate's policy and where it runs. Contents separator switched to `--` (CONTRIBUTING 6.1). |
| `syn/ooc/pp_resource_gate.py`, `_selftest.py`, `_mutants.py` | New gate. Reads one recipe measurement directory into a record (identity, input digest, figures, sub-blocks) and judges it against the recorded baseline: exit 0 within tolerance, 1 material regression, 2 not comparable (tool, device, flow, thread count or clock changed; identical inputs measured differently; unreadable reports). 51 planted arms; 25 enforcement-removal mutants all fail. |
| `syn/ooc/pp_resource_baseline.json` | New. A's three endpoints (`route-1x1`, `ooc-1x1`, `ooc-8x8`), written only by `record --write`, plus policy (tolerances about 1 %, zero for RAMB/DSP, WNS at least +0.030 ns and WHS at least 0, 121.5-tile BRAM ceiling). |
| `syn/ooc/pp_baseline.py`, `pp_baseline_mutants.py` | `--integrated-clock`: the standalone clock from the bound `CLK_HZ_P` instead of the fixed 10 ns (default unchanged); one self-test function and four killed mutants. |
| `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` | The new flag, the elaboration route to 8x8 parameters, and the gate commands. |
| `.github/workflows/rtl-fast.yml`, `scripts/ci_events.py` | The gate's self-test, mutants and `check-baseline` join the existing OOC step; the pinned step list moves with them. No new job, runner or tool. |

Headline figures (A / B):

| Measurement (A / B) | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | CARRY4 | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shipping route, whole image | 50,128 / 50,753 | 59,006 / 59,014 | 15,815 / 15,827 | 79 / 27 both | 14 | 3,405 / 3,423 | +0.063 / +0.036; +0.101 / +0.036 |
| Standalone wrapper 1x1, 20 ns | 24,343 / 24,505 | 25,344 / 25,470 | - | 21 / 3 both | 8 | 1,623 / 1,638 | estimate only |
| Standalone wrapper 8x8, 20 ns | 31,562 / 31,390 | 33,929 / 33,844 | - | 26 / 5 both | 8 | 2,001 / 2,016 | estimate only |

The image uses 79.07 % of the LUTs and 99.78 % of the slices (35 free). Two buffers still spill into flops at 1x1: the notification registry (2,048 FF, against its own distributed-RAM attribute) and the SRP timer-arm FIFOs (2,304 FF). Ranked levers (registry, SRP FIFOs, timer-arm queues, #230 sharing, throttle stamps) estimate about 5,600 FF and 3,600 LUT; #233 is not needed for placement headroom.

Gate on real data: B against A's baseline exits 1 on the route (+625 LUT over the 500-LUT tolerance; 366 of them outside the wrapper, where no RTL changed) and 0 on both standalone endpoints (+162 / -172 LUT).

Decisions needed (details in the issue thread and the findings page):

1. NFR-RES-01 (at most 60 % LUT) is 12,088 LUT short at dev; #229's 30 % non-CPU milestone is exceeded by the wrapper alone. The allocation, the proposed 13.5-tile block RAM reserve and the gate tolerances need the owner's ruling.
2. #234's first criterion says 100 MHz; the shipping configuration runs the Milan clock at 50 MHz, where both routes were measured.
3. The Vivado half of the gate runs in the manager's local bank; whether that counts as the CI of #234's fourth criterion is the owner's call. No hosted Vivado runner is proposed.
4. The next adoption needs a reviewed re-baseline of the route, and two `syn/yosys/rom_digests.tsv` rows for `ddb3119d` that its patches do not carry.
5. Child issues are recommended for the processor levers; none were opened here.

## Authoritative references

- #234 and its [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5966260488); #229 workstream 1; #230, #232, #233.
- NFR-RES-01, `docs/reference/FR_NFR.md`.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `docs/findings/PP_SHADOW_BASELINE.md` (#231, #587).
- `docs/integration/BUILDING.md` section 5 (WNS at least +0.03 ns, WHS at least 0).
- `syn/yosys/README.md`, "The cells= record" (no checked-in Yosys cell baseline).

## How to get into the same state

```sh
git fetch origin 234-area-baseline
git switch --detach 2a765a6c3868400c20ede2e357876f28a811c811
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

The measurements follow `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` with Vivado 2026.1 build 6511674; B additionally needs the processor at `ddb3119d` and the two parent-adoption patches applied in a scratch tree.

## How to validate

```sh
python3 syn/ooc/pp_resource_gate.py --selftest
python3 syn/ooc/pp_resource_gate_mutants.py
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 syn/ooc/pp_baseline.py --selftest
python3 syn/ooc/pp_baseline_mutants.py
python3 scripts/ci_events.py --check
```

Expected result / pass criteria: every command exits 0; the self-test reports 51 arms, the mutant campaigns report every mutant failing and the control passing. With Vivado, `pp_resource_gate.py check <dir> --endpoint route-1x1|ooc-1x1|ooc-8x8` on a fresh measurement of this head exits 0.

## Known limitations / out of scope

- No RTL change: every ranked lever is a processor change for its own lane (STOP rule of the assignment).
- The Vivado half of the gate runs in the manager's local bank; making it part of the merge bar is an owner decision. No hosted Vivado runner is proposed.
- No Yosys-based hosted ratchet is proposed: the Yosys gate's documentation records a deliberate decision against a checked-in cell baseline, Yosys does not predict Vivado and has no timing, and the hosted Yosys top is the 8-stream default, not the shipping shape.
- Savings in the ranking are estimates; only matched before-and-after routes measure them, and no slice saving is claimed.
- B was measured from a scratch tree; its ROM digest rows for `ddb3119d` were recorded only there.
- No bitstream, hardware, flashing or bench result.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

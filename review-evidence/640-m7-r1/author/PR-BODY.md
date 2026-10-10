[A587]

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

Green, review ready at `9d42762c`. Draft until both reviews are positive.
`640-m7` -> `dev`.
The gPTP processor gitlink names `18dd997b` on that repository's `640-m7` branch. Push the submodule branch first.

- New suite `gptp_tables`: 21/21 checks, and all 15 planted-defect controls caught, each by its table's named check.
- Full sweep: 61/61 suites, 2,173,804 checks, 0 failures; `milan_dp` 12,065; `milan_dp_gptp` (physical) 197.
- Integrated route (M0s recipe): gate `check` PASS against `route-1x1`. All endpoints met, route complete, no exception added.
- Resource: LUT 49,898 (-369), FF 53,220 (-1,193), RAMB18 25 (-2), RAMB36 74, DSP 14, WNS +0.122 ns, WHS +0.019 ns.
- Measured plane saving: 107-253 LUTs. This is below the plan's estimate of 500 (300-700). One block-RAM tile is freed.

## Linked Issue / roles

Relates to #640

Executor: `[A587]`
Internal cleared-context reviewer: `[R592]`
External reviewer: `[R593]`

## Description

Lane M7 (plan L10a) changes how five fabric gPTP plane tables are stored.
Their function, register map, timestamp path and read latency are unchanged.

| Table | Before | After |
|---|---|---|
| Tap frame FIFO, 256 beats | eight `tkeep` bits: RAMB36 + RAMB18 | highest enabled lane: one RAMB36 |
| Transmit frame FIFO, 256 beats | eight `tkeep` bits: RAMB36 + RAMB18 | lane count: one RAMB36 |
| Egress ledger type, sequence, tag (8 x 21) | flip-flops, LUT read muxes | distributed RAM, one read port at the head |
| Egress result queue (8 x 89) | flip-flops, LUT read muxes | distributed RAM, read at the head |
| Engine timer deadlines (8 x 32) | flip-flops, LUT read mux | distributed RAM, read at the sweep slot |

Both FIFO consumers already read `tkeep` only as a lane, so the FIFOs now carry the lane. The plane decodes `tx_tkeep_o` from the count.
No reader of the three converted register tables samples an entry not written since reset, so their reset clears go.
Each table keeps one write port and a combinational read.

The engine's message bank was routed in block RAM on the two freed RAMB18 first (`ba350298`).
Its output had to merge with the state port's read register. That merge cost the engine 165 logic LUTs for 86 LUTRAM sites freed.
The submodule reverts it (`861e8f80`), so the engine RTL equals the current pin.
The other LUTRAM tables are dual-read, multi-write or parallel-read, or sit at their primitive's depth already. The HANDOFF table lists the reason for each.

Commits, oldest first:
- `2ad1528b` plane FIFOs: lane fields, one RAMB36 each
- `17952792` egress ledger tags and result queue: distributed RAM
- `ba350298` pin: bank in block RAM (`f61b90c6`, `4f9fb19b`), timer deadlines in distributed RAM (`8b8d0beb`)
- `7c200939` one named ledger read port; the two anchors that quote it follow
- `0a2fef79` donor links, diagrams, ROM digest row
- `817247fa`, `633c178a` new suite `gptp_tables`, ledger graded at its read port
- `8a299ee1`, `9c7ad7f4` bank back in distributed RAM (`861e8f80`), suite and pin follow
- `74e7e6d5` module test matrix regenerated
- `49e1ce48` pin: measured engine snapshot (`18dd997b`)
- `9d42762c` M7 measurement in the Mark II plan and the area budget

The integrated route moves mapping by hundreds of LUTs in untouched blocks. The unchanged processor wrapper moved by -414. So the plane's saving is read from three views: routed -229, post-synthesis -253, out of context -107.
The FF saving (1,149) and the freed tile reproduce in every view.

## Authoritative references

- Assignment: [#640 lane M7](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6097272538).
- [Mark II area plan](../docs/design/MARK_II_AREA_PLAN.md): L10 Fabric gPTP, the ledger and the firmware block-RAM ledger.
- [Area budget](../docs/design/AREA_BUDGET.md): the resource gate, its zero-growth block-RAM policy and the D7 exception.
- Manager rulings D1, D3, D7 and D8: [#640 comment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268).
- [M0s recipe](../docs/testing/PP_SHADOW_BASELINE_RECIPE.md): integrated measurements and the resource gate.
- [gPTP plane design](../docs/design/GPTP_PLANE.md) and the donor engine's interface guide.
- IEEE 802.1AS-2011 and Milan v1.2 4.2.6: unchanged behaviour; no clause is reinterpreted.

## How to get into the same state

```sh
git fetch origin
git switch --detach 640-m7
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
git submodule status
```

The gPTP processor gitlink must name the pushed donor commit (`18dd997b`).

## How to validate

Same state as above, then from the repository root. `$LITEX_PYTHON` names the LiteX environment's interpreter:

```sh
make -C tb/verilator/gptp_tables
make -C tb/verilator/gptp_shadow
MILAN_LITEX_PYTHON="$LITEX_PYTHON" make -C tb/verilator/gptp_txts
make -C tb/verilator/gptp_plane
OUT=$(mktemp -d)
scripts/run_all_suites.sh "$OUT" --physical-gptp
make -C gptp-processor tb
syn/yosys/run.sh
python3 scripts/check_gptp_docs.py
python3 docs/traceability/gen_module_matrix.py --check
```

Expected:
- `gptp_tables`: 21/21 checks pass. All 15 controls caught, each by its own table's lockstep check: wrong depth, wrong read latency, and index or lane aliasing for each table.
- `gptp_shadow` 309/309 with 9/9 controls; `gptp_txts` 85/85 with 6/6; `gptp_plane` 29/29; `milan_dp_gptp` 197; all rc 0.
- The route follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` "Integrated measurements". It is then checked with `syn/ooc/pp_resource_gate.py check` against `route-1x1`: PASS, with the figures under Status.

The lane's full gate table (80 commands at the head, all rc 0) is posted on the Issue with the hand-off.

## Known limitations / out of scope

- The saving is below the plan's range. The LUTRAM tables are already at their primitives' density. The one block-RAM target that fits the zero-growth tile budget costs more in its output merge than it saves.
- The gate record is not re-recorded (D7). The gate recommends a re-baseline for FF and RAMB18; that is M9's step.
- Not taken: `tsf_r` into the freed RAMB18 (at most 44 LUTRAM sites). Its debug output would lag one cycle after a push into an empty ring. The tile is left to the firmware block-RAM ledger.
- Pre-existing, unchanged: `KL_gptp_shadow` pops `tx_fifo` on ready while the departure fence holds valid low. A frame admitted then is lost with no departure, and the event queue can wedge. The dev RTL and this lane's RTL behave identically there. It needs its own Issue.
- M10's shared execution and the #117 bench evidence are out of scope (bench after merge).
- `syn/yosys/rom_digests.tsv` keeps rows for the intermediate pins; the generator retains rows, and the image digest is unchanged.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the saving is below the estimate; see Status)
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

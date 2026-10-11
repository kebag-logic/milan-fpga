[A590]

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

GREEN at head `988ec7f653d0a21e0f7b40b03b8c74155d8962cf`. Nine Verilator suites: 38,033 checks, 0 failures. Firmware host tests, builder, register-map checks and every repository gate the change touches: rc 0. Integrated route gate `route-1x1`: PASS. Branch `640-m5` -> `dev`.

## Linked Issue / roles

Relates to #640

Executor: `[A590]`
Internal cleared-context reviewer: `[R598]`
External reviewer: `[R599]`

## Description

Lane M5 of #640 (Mark II plan lever L8): the CSR read path, restructured for area with identical function. No port, parameter, register address, width, reset value, access semantic or snapshot contract changes. AXI-Lite read latency is unchanged: the AR handshake, then `rd_pend`, `rd_pend2` and RVALID, three cycles as before.

| Piece | Change |
|---|---|
| `hdl/common/csr/milan_csr.sv` | The 0x800 window (0x800-0x86F) becomes one range leaf of the live read tree, so stage 1 holds one word (`live_mux_q`). `strm_mux_q` and its three hit flags are gone. |
| | Stage 2 is `r_data <= live_mux_q \| shadow_qq`. The shadow word is zeroed in the block RAM's output register unless the shadow serves the read. Before, a four-way select did this. |
| | Stage 1 keeps the old select's order: `(strm_hit \|\| rd_in_window) ? live_mux : 0`. A live arm above 0x800 without a read-window term still reads 0. |
| | The window's SNAP count words load raw. A two-bit kind per word (`snap_kind_r`: zero, raw, POISON), written in the same cycle from the same branch, is applied on read. A one-listener build loads each word straight from its one source. |
| `tb/verilator/csr/` | Read-path lockstep legs at the 1x1 and 8x8 shipping parameters against `milan_csr_ref.sv`, the dev `e8454e27` block byte for byte. Its SHA-256 is checked, and the top is generated from the block's own port list. Every output is compared on every cycle, with five named checks. `lock_mutants.py` plants seven defects, each failing its named check. |
| `scripts/measure_test_evidence_readers.py` | One reader disposition for `lock_mutants.py`. |
| `hdl/common/csr/doc/milan_csr.md` | Signals and processes of the new read path. |
| `docs/design/MARK_II_AREA_PLAN.md` | One line in L8 and the ledger's "M5 intermediate measurement" (D7 publishes lane measurements there). |

Measured (M0s recipe, both routes in fresh directories under the exclusive lock, same flow identity):

| Measurement | LUT | FF | Slices | RAMB36 / RAMB18 | WNS / WHS, ns |
|---|---:|---:|---:|---:|---|
| Base route, dev `e8454e27` | 50,267 | 54,413 | 15,779 | 74 / 27 | +0.299 / +0.031 |
| M5 route, `1abe18eb` (RTL of the head) | 49,577 | 54,226 | 15,791 | 74 / 27 | +0.097 / +0.036 |
| `csr` scope, routed | 3,037 -> 2,916 (-121) | 2,143 -> 2,110 (-33) | - | 0 / 2 both | - |
| `csr` scope, post-synthesis | 3,130 -> 3,003 (-127) | 2,143 -> 2,110 (-33) | - | 0 / 2 both | - |

- The base route equals the `route-1x1` record in every gated figure.
- The M5 route passes the gate: 0 failing setup, hold and pulse-width endpoints, and no negative-slack path in any of the four signoff corners. All 100,776 routable nets are routed, and WNS sits above the 0.03 ns floor with no exception added. XDC and shipping Tcl are identical apart from the checkout path.
- The worst setup path is in the CPU's DMA write bridge, which this change does not touch. Paths into and out of `csr` gained slack: worst +2.559 ns, against +1.353 ns at base.
- Routed primitive census of the `csr` scope: LUT3 -333, LUT5 -213, LUT6 +245, LUT2 +18, LUT4 -17, FDRE -33, MUXF7 +13, MUXF8 +2. CARRY4, RAMB18E1, LUTRAM and DSP are unchanged.
- Out of context, `milan_csr` alone: -440 LUT at 1x1 and -179 at 8x8. Inside a wrapper tying what `milan_datapath` ties: -155 and -199.
- **Saving against the plan:** about 125 LUTs and 33 FFs reproducible in the integrated image, below L8's 600 (400-1,000). The routed whole image moved -690 LUT, but about -686 of that is in untouched blocks (`u_pp`, the processor wrapper) and is not credited. What remains is the live mux over about 3,000 live status bits that the register map fixes. Two larger restructurings were measured and rejected: one case on the word index (+532 in the proxy) and two trees ORed into one stage 1 (+232).
- Not re-recorded: AREA_BUDGET's D7 keeps the record until M9.

## Authoritative references

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6098404907
- `docs/design/MARK_II_AREA_PLAN.md`: "L8 CSR read path" and the ledger.
- `docs/design/AREA_BUDGET.md`: the resource gate policy and the Mark II exception D7.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: "Integrated measurements", "Selected-placement measurements" and "Resource gate".
- `REQUIREMENTS.md`: REQ-CSR-01 (the map matches the RTL decode) and REQ-CSR-02 (no torn multiword snapshot).
- `docs/reference/REGISTER_MAP.md` (unchanged) and `hdl/common/csr/doc/milan_csr.md`.
- Owner decisions on #640: [5991591637](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991591637), [5993114362](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5993114362), [6081706413](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413); manager rulings D1, D3 and D7: [5990755268](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268).

## How to get into the same state

```sh
git fetch origin
git switch 640-m5
git rev-parse HEAD   # 988ec7f653d0a21e0f7b40b03b8c74155d8962cf
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

Tools: Verilator 5.050 (the pinned build), GNU make 4.3 for the CSR suite's Makefile check, CPython 3.12.3, Yosys 0.66 with sv2v (the hosted job pins 0.0.12; the local runs used 0.0.13), the pinned RV32 SDK for the firmware tests, and Vivado 2026.1 for the route.

## How to validate

```sh
MAKEFLAGS=w make -C tb/verilator/csr
make -C tb/verilator/tcam_csr
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp_mclk
make -C tb/verilator/milan_dp_render
make -C tb/verilator/capture_coherence
make -C tb/verilator/follow_ring
make -C tb/verilator/pp_shadow
make -C tb/verilator/milan_dp_gptp
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 sw/builder/test_builder.py --require-elaboration --require-rv32
(cd tests && behave --no-capture -f plain)
python3 scripts/check_feature_status.py
python3 scripts/check_entity_shape.py --self-test
python3 scripts/lint_rtl.py --check --self-test
python3 scripts/measure_test_evidence.py --check
syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
syn/yosys/run.sh --top milan_csr
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Integrated route: follow `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` ("Export the shipping builds", "Integrated measurements") at the head, then:

```sh
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1
```

Expected result / pass criteria:
- Every command exits 0.
- The CSR suite prints for both lockstep legs `checks: 5   failures: 0` with 0 mismatching cycles and a nonzero `lockstep` read count (1x1: 28,167; 8x8: 22,750). `lock_mutants.py` prints `8 checks: 8 PASS, 0 FAIL`, each planted defect failing its named check: wrong decode -> `decode`; torn snapshot -> `snapshot-coherence`; two stale snapshots -> `snapshot-freshness`; reset-value drift -> `reset-values`; two stage-1 claim defects -> `decode`.
- `milan_dp_mclk` prints `31 checks: 31 PASS, 0 FAIL`, including mutant 13 ("the read-window terms missing"), caught.
- The route gate prints `RESULT: PASS` with every figure `ok` and "route status: complete".

## Known limitations / out of scope

- The measured saving, about 125 LUTs, is below the plan's 600 (400-1,000). Reaching the range would need fewer live status bits, which is a register-map change that this lane excludes. The ledger's cumulative tables keep the planning figure until the week-4 re-measure.
- WNS fell from +0.299 to +0.097 ns. That is within tolerance and above the floor, and the worst path is in the CPU's DMA bridge, but it leaves less margin for later lanes.
- The recipe's 8x8 integrated synthesis was stopped before it finished, to keep the host's per-lane memory under its limit. The 8x8 shape rests on the out-of-context runs, the `lock8` lockstep leg and `milan_dp`'s 8x8 leg.
- The selected-split route is not measured (the M0s step-1 STOP stands). Split-face parity is shown by elaboration: under `--ctrl-mailbox`, `milan_datapath` gets a byte-identical parameter block and port map from the same `milan_csr.sv`.
- No re-record of the gate baseline (D7). The plan's boot readback on the bench comes after merge.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
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

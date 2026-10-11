[A590]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — The docs corrections answering the first two reviews.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).
- **[Composition repair](#composition-repair)** — The dev merge after M6 and the corrected partial-central sentence.

## Status

GREEN at head `2bef9e50`. Since the reviewed head `c0cba330`, the manager merged dev `6bfeeb13` (M2 and M6; an automatic merge) and corrected one plan sentence. With M2's and M6's measured savings, the partial-central scenario is about 38,784, 744 over 38,040 (R598-3-F1, see [Composition repair](#composition-repair)). Round 2 at `c0cba330`: docs and one RTL comment, see [Round 2](#round-2). Nine Verilator suites at round 1's head `988ec7f6`: 38,033 checks, 0 failures; the CSR suite was re-run at `c0cba330` with the same figures. Firmware host tests, builder, register-map checks and every repository gate the change touches: rc 0. Integrated route gate `route-1x1`: PASS. Branch `640-m5` -> `dev`.

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
| `tb/verilator/csr/` | Read-path lockstep legs at the 1x1 and 8x8 shipping parameters against `milan_csr_ref.sv`, the dev `e8454e27` block byte for byte apart from the module name. Its SHA-256 is checked, and the top is generated from the block's own port list. Every output is compared on every cycle, with five named checks. `lock_mutants.py` plants seven defects, each failing its named check. |
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
- **Saving against the plan:** about 125 LUTs and 33 FFs reproducible in the integrated image, below L8's 600 (400-1,000). The routed whole image moved -690 LUT, in three disjoint parts: `csr` -121 (credited); the processor wrapper -342, nearly all of it in `u_pp` (-344, nested inside the wrapper, not added); and about -227 in other untouched blocks. Only the `csr` part is credited. What remains is the live mux over about 3,000 live status bits that the register map fixes. Two larger restructurings were measured and rejected: one case on the word index (+532 in the proxy) and two trees ORed into one stage 1 (+232).
- Not re-recorded: AREA_BUDGET's D7 keeps the record until M9.

## Round 2

Answers [R598-1](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105288411) and [R599-1](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6105370578) under the [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105372796). Docs and one RTL comment only: no logic change, no re-route. Three new commits on `988ec7f6`, no rebase or amend:

| Commit | Answers | Change |
|---|---|---|
| `5747be31` | R599-1 RES-1 | `hdl/common/csr/milan_csr.sv:1066-1068`: the `rd_pend2` banner says stage 2 is an OR of the two stage-1 words, in RES-1's exact text. |
| `80e41fc1` | R599-1-F1, R598-1-S1, R599-1 RES-2 | `docs/design/MARK_II_AREA_PLAN.md:1023-1024`: each per-stream figure carries its scope, in R599-1's text; no reproduction claim remains. `:1027`: the partial-central consequence of the measured 121. `:538`: "M5 saved 121 LUTs routed". |
| `c0cba330` | - | Reflows the same banner so no line runs past the file's width. The file keeps its 3,225 lines, so every line cited at `988ec7f6` is unchanged. |

- R598-1-F1 = R599-1-F2 (disjoint attribution): the "Saving against the plan" bullet above now gives `csr` -121, wrapper -342 (`u_pp` -344 nested inside it) and about -227 elsewhere, summing to -690. These are the route gate's own sub-block figures for the M5 route.
- R599-1 RES-3: the `tb/verilator/csr/` row says "byte for byte apart from the module name".
- R599-1-S1 (alternate placement directives) is optional and was not run: this round runs no route.
- Comment-only check: `git diff 988ec7f6 HEAD -- hdl` changes six lines, all `//!` comment lines in one banner. `git diff 1abe18eb HEAD -- syn sw configs` is empty.

Gates at `c0cba330`, clean tree, each unpiped with its own log, all rc 0: `docs_check.py` (with and without git metadata), `check_em_dash.py --base e8454e27` and `--selftest`, `check_doc_style.py` and `--selftest`, `check_gptp_docs.py` and `--selftest`, `gen_toc.py --selftest`, `--verify-anchors` and `--check`, `check_doc_paths.py` and `gen_module_matrix.py --check` (the Markdown gates under the pinned renderer). Also, for the touched RTL file: `check_sv_idiom.py`, `check_hygiene.py --check`, `measure_naming.py --check`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `measure_test_evidence.py --check`, `check_port_contracts.py`, `check_rtl_source_lists.py`, `lint_rtl.py --check` (90 <= 90) and `git diff --check e8454e27 HEAD`. Under GNU make 4.3, `MAKEFLAGS=w make -C tb/verilator/csr`: rc 0, with lock1 at 28,167 random-traffic reads and lock8 at 22,750, 0 mismatching cycles, and `lock_mutants.py` 8/8. These are the same as round 1.

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
git rev-parse HEAD   # c0cba330fd485e52fcb90d5ccc69169edf9f0c2b
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

- The measured saving, about 125 LUTs, is below the plan's 600 (400-1,000). Reaching the range would need fewer live status bits, which is a register-map change that this lane excludes. The ledger's cumulative tables keep the planning figure until the week-4 re-measure. At the measured 121, the partial-central scenario becomes about 38,436, 396 over 38,040, pending that re-measure (D8).
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

## Composition repair

The composition review [R598-3](https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6108060229) found that the merged plan's partial-central sentence counted only M5's measured saving. After M6 merged, `da341a15` merges dev `6bfeeb13`; its tree equals the reviewed candidate tree `0fc0841b`. `2bef9e50` rewrites `docs/design/MARK_II_AREA_PLAN.md:1106`: 37,957 + (200 - 34) + (600 - 121) + (600 - 418) = 38,784, 744 over 38,040. `docs_check.py`, `check_em_dash.py --base 6bfeeb13`, `gen_toc.py --check` and `--verify-anchors`, `check_doc_style.py` and `check_doc_paths.py` pass at `2bef9e50`. The gate record stays unchanged under D7.

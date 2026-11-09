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

GREEN — 65/65 suites pass, every local gate rc 0 — `854-shadow-drop-count` -> `dev`. Base `dev` `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`, head
`e87f2179f8d84b3eb89dea0148bb63d64319bc38` (one commit).

## Linked Issue / roles

Closes #854
Relates to #853

Executor: `[A756]`
Internal cleared-context reviewer: `[R803]`
External reviewer: `[R804]`

## Description

`KL_pp_shadow`'s control-frame drop counter (`rx_drops_o`, `PP_DIAG[15:8]`) could not count. The all-fabric tap's FIFO
is `axis_fifo` with `FRAME_FIFO=1, DROP_WHEN_FULL=1`. In that configuration verilog-axis holds `s_axis_tready` at 1
and drops a frame it has no room for by itself. The old `drop_evt_w = fw_valid_w & ~fw_ready_w` was therefore
constant 0. This PR applies #853's counting method, written for the split placement's tap, to this tap.

| Piece | Change |
|---|---|
| `hdl/milan/KL_pp_shadow.sv` (`drop_evt_w`, `last_kept_r`) | The count reads the FIFO's own `status_overflow`, which rises for the cycle after the last beat of a frame the FIFO dropped. It counts that strobe only when the frame was one the tap kept: `last_kept_r` is set on the last accepted beat of an `FW_BODY` frame, or of an `FW_HEAD1` frame with `accept_w`. A refused frame or a runt also ends marked bad, and is reclaimed whether or not the FIFO is full, so its overflow loses no control frame and is not counted. The existing `!= 8'hFF` guard keeps the saturation at 255. |
| `hdl/milan/KL_pp_shadow.sv` (`axis_fifo` instance) | `.status_overflow` is connected; it was left open before. |
| `hdl/milan/KL_pp_shadow.sv` (banner, `rx_drops_o` port comment) | The contract now states that the count comes from the FIFO's own overflow indication and saturates at 255. |
| `tb/verilator/pp_shadow/sim_main.cpp`, `drops_probes.vlt` | New section `[DR]`, also run on its own with `--drops-only`. The harness counts each frame the serializer hands to the processor from the serializer's own byte stream, and grades the counter against frames offered less frames handed out. |
| `tb/verilator/pp_shadow/drops_mutant.py`, `Makefile` | `make drops-mutant`: a clean control, then six planted arms, each of which must fail its named check. |
| `tb/verilator/pp_shadow/README.md`, `docs/testing/TESTING.md`, `docs/reference/REGISTER_MAP.md` | The section, its commands and its arm table. The `PP_DIAG[15:8]` description. |

`[DR]` at the head:

- **Burst:** 108 frames offered (100 of 64 bytes, then 8 of 16 bytes), 77 handed out, 31 lost, and the count reads 31.
- **Refused frames:** 69 kept frames lost and the count rises by 69. The FIFO raised 158 overflows; the other 89
  were refused frames that met the full FIFO.
- **Saturation:** 392 frames lost in all, and the count reads 255 and holds there.

| Arm | Plant | Named check that fails |
|---|---|---|
| `count-removed` | the count's increment ANDed with 0 | DR a burst past the FIFO loses frames and counts them |
| `count-from-tready` | `drop_evt_w = fw_valid_w & ~fw_ready_w`, the construction #854 reported | the same |
| `counts-refused` | every FIFO overflow counted | DR ...and are not counted: the kept frames lost equal the count |
| `misses-second-beat` | a frame kept at `FW_HEAD1` not counted | DR the burst's lost frames equal the drop count |
| `wraps` | the `!= 8'hFF` guard removed | DR the count saturates at 255 |
| `diag-tied-off` | `milan_datapath`'s `.i_pp_rx_drops` ANDed with 0 | DR a burst past the FIFO loses frames and counts them |

The clean control passes, and all six arms are KILLED by their named checks.

No processor or submodule change. `KL_gptp_shadow.sv` is unchanged, because its tap already counts from
`status_overflow`.

### Area: the shipping AX7101 1x1 route at the head

On `dev`, `drop_evt_w` is constant 0, so synthesis can remove the counter and the FIFO's overflow register. Both now
exist, so the route moves. The route was run once at the head, with one directive, ExtraPostPlacementOpt, in the form
given by `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`. `pp_resource_gate.py check --endpoint route-1x1
--shipping-selection` returned RESULT PASS.

| Figure | Baseline (record 15) | Head | Delta |
|---|---:|---:|---:|
| LUT | 53,428 | 53,534 | +106 |
| FF | 54,837 | 54,850 | +13 |
| SLICE | 15,829 | 15,820 | -9 |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 15 | 74 / 27 / 15 | 0 |
| WNS (worst corner) | +0.210 ns | +0.166 ns | -0.044 |
| WHS (worst corner) | +0.036 ns | +0.032 ns | -0.004 |

Signoff corners: Slow_0C and Slow_85C give WNS +0.166 ns and WHS +0.050 ns; Fast_0C and Fast_85C give WNS +1.633 ns
and WHS +0.032 ns. The route is complete, with no unrouted net. The baseline's selected directive is
AltSpreadLogic_high, so the deltas include the change of directive as well as this diff. Inside the wrapper the
change accounts for +35 LUT and +10 FF (the counter and `last_kept_r`), and for +1 LUT and +1 FF in `ctl_fifo`
(`overflow_reg`). `syn/ooc/pp_resource_baseline.json` is not re-recorded in this PR.

## Authoritative references

- #854, its Required items; #853, the counting method for the split tap.
- The counter is a project diagnostic, and no standard defines it. The frames it counts are the tap's classified
  set: EtherType 0x22F0 (IEEE 1722-2016), which carries IEEE 1722.1-2021 clause 6 ADP, clause 8 ACMP and clause 9
  AECP, and MSRP (IEEE 802.1Q-2022 clause 35.2) and MVRP (IEEE 802.1Q-2022 clause 11.2) at their group addresses.
- `third_party/verilog-axis/rtl/axis_fifo.v` at the pinned revision: `s_axis_tready` is held at 1 when
  `DROP_WHEN_FULL` is set (`:217`), and `overflow_reg` rises the cycle after the last beat of a dropped frame
  (`:275-284`).
- `docs/reference/REGISTER_MAP.md`, `PP_DIAG[15:8]`.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, the area recipe.

## How to get into the same state

```sh
git fetch origin 854-shadow-drop-count
git checkout --detach e87f2179f8d84b3eb89dea0148bb63d64319bc38
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
make -C tb/verilator/pp_shadow build-base exec-base SIM_ARGS=--drops-only
make -C tb/verilator/pp_shadow drops-mutant
make -C tb/verilator/pp_shadow
bash scripts/run_all_suites.sh /tmp/suites --wait
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/builder/test_builder.py --require-rv32
cd tests && behave
python3 scripts/docs_inventory.py --check
git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD
```

Expected result / pass criteria: every command exits 0. `--drops-only` prints the `[DR]` figures above, with no
failing check. `drops-mutant` ends `PASS: [DR] catches every arm (6 of 6); clean control passes`.

Local gates on a clean clone of the head:

| Gate | rc | Result |
|---|---:|---|
| `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, k = 0..3 | 0 (each) | 65 of 65 suites passed, 0 failed, 0 timed out (15, 17, 17 and 16 per shard). `pp_shadow`: 317 checks, 0 failures, with the `[DR]` figures above |
| `make -C tb/verilator/pp_shadow drops-mutant` | 0 | `PASS: [DR] catches every arm (6 of 6); clean control passes` |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test` | 0 | `test_ctrl_firmware: PASS` |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest` then `--check` | 0 | `firmware coverage: PASS (30 files)` |
| `python3 sw/builder/test_builder.py --require-rv32` | 0 | `ALL GATES PASS EXCEPT 17 NOT RUN` (the 17 need a LiteX interpreter) |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| every `run:` step of `.github/workflows/docs.yml` | 0 | 65 steps ran, 31 not run (hosted orchestration only), 0 bad |
| `python3 scripts/docs_inventory.py --check` | 0 | `documentation inventory: OK` |
| `git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD` | 0 | no output |
| `python3 scripts/lint_rtl.py --check --self-test` | 0 | `LINT GATE: PASS (89 violation(s) <= ratchet 89; ...)` |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | pass |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `TEST-EVIDENCE RATCHET: PASS` |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 | 3 of 3 tops pass |
| the `syn/ooc` self-tests and mutants (`dp_srcs`, `ooc_tcl_selftest`, `pp_baseline`, `pp_resource_gate`, `check-baseline`) | 0 | `resource gate mutants: control passes, all 236 mutants fail`, `baseline PASS: 3 endpoints` |

On the first run, `test_builder.py`, `behave` and one docs.yml step each failed on the local environment: the SDK
was not at the path CI provisions, PyYAML was missing, and the `wavedrom` pin the workflow installs was absent. Each
passed when re-run with that provisioning in place, and the rows above are those re-runs.

## Known limitations / out of scope

- **The consumer is not stalled in the test.** The #853 probe stalled the mailbox. This tap's consumer is the
  serializer into the processor, which has no ready (`ff_ready_w = ~ser_busy_r`) and drains one byte a cycle. The
  test keeps the probe's burst (100 back-to-back 64-byte ADP frames), and at eight bytes a cycle the burst outruns
  the drain. Frames lost are measured as frames offered less frames handed out.
- **Runts are not graded.** `rx_mac_filter`, ahead of the tap, drops every runt
  (`hdl/ieee8021q/filtering/rx_mac_filter.sv:26`, `:239`), so a runt never reaches the tap in this build. The RTL
  still qualifies runts, as #853 does, for a build that prunes the filter (`RXFILT_P=0`). No arm plants a runt count.
- **The resource baseline is not re-recorded.** Re-recording `syn/ooc/pp_resource_baseline.json`, with its comparison
  routes, the CHANGELOG and the area pages, is left to a separate decision. Only one route was run.
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

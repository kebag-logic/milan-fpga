# 854-a756 HANDOFF

**Status: REVIEW READY. Every gate is rc 0 on a clean clone of the head, and the route fits (no STOP).** The full sweep
(run 4, four native-shards units) passed 65 of 65 suites after the host reboot killed serial run 3. Lane
`854-shadow-drop-count`, base `dev`
`ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`, head `e87f2179f8d84b3eb89dea0148bb63d64319bc38` (one commit). Nothing
pushed. TAKEN posted on #854 (issuecomment-6731838794); REVIEW READY posted at 12:38 (issuecomment-6739132449, the
text is `REVIEW-READY.md`). `PR-BODY.md` is ready for the manager, with `Closes #854`: every Required item is met.

## 1. Assignment

Issue #854, every Required item:

- count the all-fabric tap's lost control frames from the FIFO's own drop or overflow indication, not from
  `tready`, saturating at 255 as documented;
- a self-checking overflow test where the frames lost equal the counter;
- a planted mutant that removes the count, caught.

The method is PR #853's (split tap, `hdl/milan/KL_ctrl_split.sv` at `e6d27f3a`, read only).

## 2. Changes

The counter is a project diagnostic, and no standard defines it. The frames it counts are the tap's classified set:
EtherType 0x22F0 (IEEE 1722-2016, carrying IEEE 1722.1-2021 clause 6 ADP, clause 8 ACMP and clause 9 AECP), and
MSRP (IEEE 802.1Q-2022 35.2) and MVRP (IEEE 802.1Q-2022 11.2) at their group addresses.

| File:line | Change | Why |
|---|---|---|
| `hdl/milan/KL_pp_shadow.sv:857-874` | `drop_evt_w` = the FIFO's `status_overflow` & `last_kept_r`. `last_kept_r` is set on the last beat the FIFO accepts, and only for a frame the tap kept (`FW_BODY`, or `FW_HEAD1` with `accept_w`). The old `fw_valid & ~fw_ready` is removed. | With `FRAME_FIFO=1, DROP_WHEN_FULL=1`, verilog-axis holds `s_axis_tready` at 1 (`third_party/verilog-axis/rtl/axis_fifo.v:217`), so the old term was constant 0. The FIFO drops the frame itself and raises `overflow_reg` the cycle after its last beat (`axis_fifo.v:275-284`). A refused frame (terminated at `FW_HEAD1` and marked bad) or a runt (marked bad at `FW_HEAD0`) also raises that strobe when it meets a full FIFO, but it loses no control frame, so it is not counted. This is #853's construction. |
| `hdl/milan/KL_pp_shadow.sv:915` | `.status_overflow (ff_overflow_w)` (was open) | the indication the count reads |
| `hdl/milan/KL_pp_shadow.sv:73-75`, `:752` | banner and port comment: counted from the FIFO's own overflow indication, saturating at 255 | the documented contract (#854 cites `:73` and `:751`) |
| `hdl/milan/KL_pp_shadow.sv:1638` | unchanged: `if (drop_evt_w & (rx_drops_o != 8'hFF))` | the 255 saturation already existed |
| `tb/verilator/pp_shadow/sim_main.cpp:89-100`, `:1956-2112`, `:150`, `:162-163`, `:199-202`, `:4731-4732` | section `[DR]`, the `--drops-only` mode, and `[DR]` in the default run after every check that reads the drop count as 0 | the overflow test |
| `tb/verilator/pp_shadow/drops_probes.vlt` (new) | read-only probes: the serializer's `pp_rx_valid_w`, `pp_rx_data_w`, `pp_rx_last_w`, and `ff_overflow_w` | the harness counts frames handed out by its own observation, not from the DUT's counter |
| `tb/verilator/pp_shadow/drops_mutant.py` (new), `Makefile:96`, `:118`, `:204-208` | six planted arms, `make drops-mutant` | the mutant requirement |
| `tb/verilator/pp_shadow/README.md:14`, `:165-200` | the section, its run commands, the arm table (contents line written by `gen_toc.py --write`, description filled in) | docs |
| `docs/testing/TESTING.md:748` | the pp_shadow row names `[DR]` and `drops-mutant` | docs |
| `docs/reference/REGISTER_MAP.md:2469-2472` | `PP_DIAG[15:8]`: counted from the FIFO's own overflow indication, saturating at 255 | docs (the table row is unchanged; the added-line em-dash gate) |

No processor or submodule change. No change to `KL_gptp_shadow.sv`: its tap already counts from `status_overflow`
(`hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:415-430`).

### 2.1 What the test cannot do here, stated plainly

- **The consumer is not stalled.** #853's probe stalled the mailbox. The all-fabric tap's consumer is the
  serializer into the processor, which has no ready (`ff_ready_w = ~ser_busy_r`) and drains one byte a cycle. The
  burst keeps the probe's shape (100 back-to-back 64-byte ADP frames), and at eight bytes a cycle it outruns that
  drain. The frames lost are measured as the frames offered less the frames the harness saw leave the serializer.
- **Runts are not graded.** `rx_mac_filter` ahead of the tap drops every runt (`hdl/ieee8021q/filtering/rx_mac_filter.sv:26`,
  `:239`). A trace confirmed that an 8-byte frame offered at the MAC never reaches the tap. The RTL still qualifies
  runts, as #853 does, which covers a build that prunes the filter (`RXFILT_P=0`). No arm plants a runt count.

## 3. New checks, their planted mutants and failing words

`[DR]` at the head, run alone (`--drops-only`), and the same figures inside the default base run:

- **Burst:** 108 offered (100 of 64 bytes, then 8 of 16 bytes), 77 handed out, 31 lost, count 31.
- **Refused burst:** 69 kept frames lost, count +69, and 158 FIFO overflows: the 89 overflows above the frames lost
  are refused frames that met the full FIFO.
- **Flood:** 392 lost in all, and the count reads 255 and holds there.

| Check (failing words) | Arm (`make drops-mutant`) | Plant |
|---|---|---|
| `DR a burst past the FIFO loses frames and counts them` | `count-removed` | the count's increment ANDed with 0 |
| the same | `count-from-tready` | `drop_evt_w = fw_valid_w & ~fw_ready_w`, the construction #854 reports |
| `DR ...and are not counted: the kept frames lost equal the count` | `counts-refused` | `drop_evt_w = ff_overflow_w` |
| `DR the burst's lost frames equal the drop count` | `misses-second-beat` | `last_kept_r` false for a frame kept at `FW_HEAD1` |
| `DR the count saturates at 255` | `wraps` | the `!= 8'hFF` guard removed |
| `DR a burst past the FIFO loses frames and counts them` | `diag-tied-off` | `milan_datapath`'s `.i_pp_rx_drops` ANDed with 0, so the count never reaches `PP_DIAG[15:8]` |

Result in the lane: clean control PASS, 6 of 6 KILLED by their named checks. The clean-clone result is in the gate
table.

## 4. Area

The change moves the shipping route. On `dev`, `drop_evt_w` is constant 0, so synthesis can remove the 8-bit counter
and the FIFO's overflow register. Both now exist, with `last_kept_r`.

The shipping AX7101 1x1 route was run at the head `e87f2179` in the recipe's form
(`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: the export, `pp_baseline.py --single-thread-synthesis`,
`baseline_integrated.tcl`). It used one directive, ExtraPostPlacementOpt, through `vivado-slot.sh` (slot 0, in a
scope with MemoryMax 12G), and took rc 0 in 3,447 s. No comparison route was run.
`pp_resource_gate.py check <gateware> --endpoint route-1x1 --shipping-selection` gave rc 0, RESULT PASS:

| Figure | Baseline (record 15) | Head | Delta |
|---|---:|---:|---:|
| LUT | 53,428 | 53,534 | +106 |
| FF | 54,837 | 54,850 | +13 |
| SLICE | 15,829 | **15,820** | -9 |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 15 | 74 / 27 / 15 | 0 |
| WNS (worst corner) | +0.210 ns | **+0.166 ns** | -0.044 |
| WHS (worst corner) | +0.036 ns | +0.032 ns | -0.004 |

- **Signoff corners** (floors: WNS 0.03 ns, WHS 0.0 ns): Slow_0C and Slow_85C WNS +0.166 / WHS +0.050; Fast_0C and
  Fast_85C WNS +1.633 / WHS +0.032.
- **Route status:** complete, no unrouted net and no routing error.
- **Sub-blocks, not gated:** the wrapper +35 LUT and +10 FF (the counter, `last_kept_r`); `ctl_fifo` +1 LUT and +1
  FF (`overflow_reg`). The rest is placement noise inside `u_pp` (+27 LUT net).
- **STOP conditions:** neither met. Slices are 15,820, at or under 15,850, and WNS +0.166 ns is above the 0.03 ns
  floor at every corner.
- **Directive:** the baseline's selected route is AltSpreadLogic_high and this one is ExtraPostPlacementOpt, so the
  deltas include the directive change as well as this diff.

`syn/ooc/pp_resource_baseline.json` was **not** re-written. The record the gate prints
(`pp_resource_gate.py record ... --shipping-selection`, no `--write`) is `receipts/area/record-route-1x1.json`.
Re-recording the baseline, with its comparison routes, CHANGELOG and area pages, is the manager's decision.

Receipts: `receipts/area/` (the gate's output and rc, the printed record); `receipts/route/` (route status,
utilization, the processor-boundary reports, signoff negative-slack summaries, `baseline.log.rc`, and
`LARGE-FILES.sha256`, which holds sha256 and size for the checkpoints, the full timing reports and the log).

## 5. Gates (clean clone of the head `e87f2179`)

Receipts are under `receipts/gates/`, copied by `receipts/scripts/collect_gates.sh`, which also writes
`receipts/INDEX.md` from the files present. A log over 200 KB is not copied: its sha256 and size are in that
directory's `LARGE-FILES.sha256`. Lane gates: `gates/lane/` (`lane_gates.sh`, then `lane_gates_rerun.sh` for two
gates whose first run failed on the environment). docs.yml: `gates/docsyml-e87f2179/` (run 1) and
`gates/docsyml-e87f2179-2/` (run 2), from `docsyml_all.sh`. Its runner and verifier are the reference copies with
only the lane, venv and home paths changed. Sweep: `gates/sweep-run1/` to `gates/sweep-run3/` (serial), and
`gates/sweep-shards/` (run 4).

| Gate | Command | rc | Log shows |
|---|---|---:|---|
| diff check | `git diff --check ac0a01e3 HEAD` | 0 | no output |
| docs inventory | `python3 scripts/docs_inventory.py --check` | 0 | `documentation inventory: OK` |
| test evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | `TEST-EVIDENCE RATCHET: PASS (67 <= 77 suite(s) without a mutation arm, ...)`, and the advisory `the mutation ratchet can be lowered to 67`. The ratchet is not lowered here (out of scope) |
| RTL lint | `python3 scripts/lint_rtl.py --check --self-test --jobs 8` | 0 | `LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off)` |
| pp sources | `python3 scripts/pp_srcs.py --check --selftest` | 0 | self-test passed |
| yosys elaborate | `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 | 3 of 3 PASS |
| OOC self-tests | `dp_srcs`, `ooc_tcl_selftest`, `pp_baseline` (+mutants, reports), `pp_resource_gate` (+mutants, check-baseline) | 0 | `resource gate mutants: control passes, all 236 mutants fail`, `baseline PASS: 3 endpoints` |
| drops mutant | `make -C tb/verilator/pp_shadow drops-mutant` | 0 | `PASS: [DR] catches every arm (6 of 6); clean control passes` |
| firmware self-test | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8` | 0 | `test_ctrl_firmware: PASS` |
| firmware coverage | `fw_coverage.py --selftest`, `fw_coverage.py --check --jobs 8` | 0 | `firmware coverage: PASS (30 files)` |
| builder | `python3 sw/builder/test_builder.py --require-rv32` | run 1: 1; run 2: 0 | run 1: `the provisioned absolute SDK selector must be adopted` (the SDK not at the path CI provisions); run 2 with the pinned SDK there: `ALL GATES PASS EXCEPT 17 NOT RUN` (the 17 need a LiteX interpreter) |
| behave | `cd tests && behave` | run 1: 1; run 2: 0 | run 1: `PyYAML required`; run 2 with PyYAML beside behave: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| docs.yml run 1 | every `run:` step | 1 | 65 ran, 1 bad: `docs-gates-0/gate_13` `the 'wavedrom' package is missing` (the venv lacked the pin the workflow installs at `ci_step_10`) |
| docs.yml run 2 | every `run:` step, wavedrom==2.0.3.post3 installed in the venv | 0 | `65 steps ran, 31 not run with a reason, 0 bad`; every job's tree clean after it |
| full sweep run 1 | `bash scripts/run_all_suites.sh <logs> --wait`, serial | 2 | preflight `ABORTING: sweep cancellation controls failed.` (`owner-survivor: CLEANUP FAILED`, and `hard-HUP` timed out after 60 seconds). **Invalid launch**, see below |
| full sweep run 2 | the same, the same launch | 2 | the same two failures. **Invalid launch** |
| full sweep run 3 | the same, as its own systemd unit | none | killed by the planned host reboot at 10:34: `CANCELLED: TERM; no completed sweep result`. 40 of 65 suites had printed `PASS`, none had failed, and `milan_dp` was running. **No result** |
| full sweep run 4 | `native-shards.py 854-a756 <spec> <out> 4 104-111 96-103 88-91 80-87`, each shard `bash scripts/run_all_suites.sh <logs> --wait --shard k/4` | 0, 0, 0, 0 | shard 0: `suites: 15 passed: 15 failed: 0 timed out: 0`, `checks: 361228 in-suite failures: 0`; shard 1: 17 of 17, 1,525,512 checks; shard 2 (capture_coherence, 4 CPUs): 17 of 17, 284,230 checks; shard 3: 16 of 16, 21,575 checks. **65 of 65 suites, 0 failed, 0 timed out**; every preflight passed, so there was no #833 re-run |

**Runs 1 to 3 were serial, not four shards.** At 07:24 `cpu_ranges.py show` printed `busy 128 cpus; free16 []
free12 [] half8 []`, so no range could be booked for a shard. Those runs used this lane's own unit, on four of its
eight CPUs (64-67) with `-j4`, which kept capture_coherence on at most four CPUs. docs.yml ran on the other four.

**Run 4 is the four shards.** At 10:59, MemAvailable was 45 GB, and `cpu_ranges.py show` printed `free16 ['64-79',
'80-95', '96-111']`. Four successive `pick8` results, each treated as booked before the next pick
(`receipts/scripts/book_shards.py`), gave 104-111, 96-103, 88-95 and 80-87. Shard 2 holds capture_coherence
(`run_all_suites.sh --shard 2/4 --list`), so it runs on 88-91, four CPUs of its booked range. The spec carries Make's
`--no-print-directory` (`MAKEFLAGS=-j4 --no-print-directory`). Receipts: `gates/sweep-shards/`. The shards ran
10:59 to 12:36 (3,449 s to 5,776 s each, `shard-k/results.json`).

The `pp_shadow` suite in shard 0 shows `[DR]` on the clean clone: `DR burst: 108 offered, 77 handed out, 31 lost,
count 31`, `DR refused burst: 69 kept lost, count +69, 158 FIFO overflows`, `DR flood: 392 frames lost in all`, and
the count `got=0x000000FF exp=0x000000FF`, then `pp_shadow: 317 checks, 0 failures`
(`gates/sweep-shards/shard-0/logs/pp_shadow.log`).

**The shard clones' trees after the sweep** (`gates/sweep-shards/tree-after.txt`): shards 0 to 2 are clean. In shard
3, `tsn_fuzz` rewrote the timestamp line of its two generated status pages, `hdl/ieee1722/avtp/doc/TEST_RESULTS.md`
and `hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md`. The counts are unchanged (164 pass and 675 pass, 0 fail). This is
the suite's existing behaviour, it is not from this diff, and nothing was committed.

**Runs 1 and 2 are not #833 results.** They were launched with `setsid nohup`, and `nohup` sets SIGHUP to ignored
for the whole sweep. The launch receipt `sigign-nohup-launch.txt` shows `SigIgn: 0000000000000001` (SIGHUP) for
that launch, while a `systemd-run` unit shows `0000000000001000`. With SIGHUP ignored, the `hard-HUP` control
cannot pass. Run 3 was started the way `native-shards.py` starts a shard, as its own unit (`milan-854-a756-sweep`,
MemoryMax 10G, `taskset -c 64-67`), and its preflight passed. The docs.yml run 2 was launched with `nohup` and
passed, 0 bad.

## 6. Timeline (CET, 2026-11-09)

- 04:51: started. Read the issue, PR #853's method and the axis_fifo write path.
- 05:0x: TAKEN posted. RTL and `[DR]`. The first runt arm was vacuous, because a frame behind a dropped one finds
  that frame's words reclaimed, and a trace then showed runts never reach the tap. The refused arm was reshaped so
  each refused frame follows a 16-byte kept frame that fills the FIFO.
- 05:0x: `drops-mutant` 6 of 6 in the lane; the full base leg 730 checks, 0 failures.
- 05:1x: committed `e87f2179`. Clean clones for the gates and the route. The route started in slot 0 at 05:12.
  The lane gates started beside it. The sweep waits for the route (one at a time).
- 05:1x-06:48: lane gates on `gclone`; `test_builder` and `behave` re-run after the environment fixes; docs.yml run 1.
- 06:4x: the session host's authentication failed and the session ended (not a STOP).
- 07:23: resumed. Route receipts already in place (rc 0). Installed wavedrom==2.0.3.post3 into the docs venv and
  started docs.yml run 2. No CPU range was free, so the sweep started serially at 07:25 on a fresh clone `sclone`.
- 07:35: sweep run 1 aborted in the cancellation preflight; run 2, the same at 07:38. Traced to the `nohup` launch
  (SIGHUP ignored). Run 3 started at 07:38 as its own systemd unit; its preflight passed.
- 08:32: docs.yml run 2: 65 ran, 0 bad.
- 10:34: the owner's planned host reboot ended the session (not a STOP) and killed sweep run 3 after 40 of 65 suites,
  all 40 PASS.
- 10:58: resumed. TAKEN is on #854 once, and REVIEW READY has not been posted. Re-read the issue's Required items
  against the RTL and `axis_fifo.v`.
- 10:59: sweep run 4 started as four native-shards units (`milan-854-a756-shard0..3`).
- 11:57 to 12:36: the shards finished in the order 3, 1, 0, 2, all rc 0, with 65 of 65 suites. Receipts collected.
- 12:38: REVIEW READY posted on #854 with the head `e87f2179`. Round complete; nothing pushed.

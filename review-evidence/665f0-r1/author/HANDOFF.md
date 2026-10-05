# HANDOFF: lane F0 of #665 (mailbox contract, harness, ADP slice), [A542]

Status: REVIEW READY at the head below (local, not pushed).

- Branch: `665-f0-mailbox` from dev `fa450d301805881ad713b67521477bf042ddadfd`
- Head: `0bfef4987eede4b022b17c7b2f56d079ff84893b` (9 one-line commits, no trailers)
- Assignment: #665 comment 5991862788, amended by the owner directive 5992455815
  (bare-metal first, lwSRP's port layer in the HAL, protocols as portable
  ports-and-adapters modules). The session pointer named #658 comment
  5988328859, which is the #658 lane; noted in TAKEN.
- TAKEN: #665 comment 5992024623 (posted once, before the restart; not reposted)
- REVIEW READY: #665 comment 5994496304
- Reviewers named by the assignment: [R496] internal, [R497] external.

Commits (`fa450d30..0bfef498`):

| SHA | Subject |
|---|---|
| d4cbb27b | the contract, generator, fabric skeleton and leaves, C header, reference page |
| 7ab3cd72 | the firmware (driver, port layer, loop, ADP) and the mailbox suite, model, co-simulation, planted defects |
| ae6d7138 | the default-off `--ctrl-mailbox` SoC switch and the design page |
| 763e88ca | lwSRP's tick registration rule in the design page |
| 5ebc1998 | the routed area; eight more RTL and two more firmware planted defects |
| 397e2d3b | docs brought to 27 RTL and 25 firmware planted defects |
| f2187633 | "receive"/"transmit ring" wording (the bare-metal scope gate refuses "TX ring") |
| f9a99f51 | three more RTL planted defects (closed channel, second EtherType, past deadline) |
| 0bfef498 | one firmware planted defect per remaining walked row (TMR_ADVERTISE, TMR_DELAY, LINK_UP) |

## 0. What the restart kept and what it changed

Kept from the first session (re-read line by line, found sound): the YAML
contract and its generator (model, emitters, skeleton emitter, self-test), the
hand-written leaves `KL_mbx_ring/rx/tx/evt`, both bus adapters, and the
mailbox driver.

Changed for the directive:

- **Contract.** A centisecond `TICK` event (type 4: COUNT of ticks since the
  previous TICK record, coalesced, saturating; NOW_MS) and `TICK_CTL.EN`
  (reset 0), so the firmware drives lwSRP's `shlan_timer_tick()` from the
  fabric and loses no tick when late. The SRP channel's record is stated as
  the MRPDU form lwSRP's `mrp_rx()`/`mrpdu_parse()` take (frame bytes 14
  onward, IF as port_id). Contract stays 1.0 (never published).
- **RTL.** `KL_mbx_evt` gains the tick source (lowest priority, coalesced);
  the skeleton wires `ms_tick_p_i` and `TICK_CTL.EN` to it.
- **Firmware rebuilt in layers** (no OS, no heap, static state): wire layer;
  driver; lwSRP's port layer (static block pool, bounded debug sink); a
  bare-metal event loop with bounded passes and the TICK fan-out; ADP split
  into a core that knows no mailbox (ports struct, like lwSRP) and a mailbox
  adapter; a static app composition; an MMIO platform file.
- **Harness.** A C model of the fabric side, graded by the same checks as the
  RTL; the processor's ADP walk reused from the pinned submodule; the
  firmware co-simulated on the RTL; lwSRP's own MRP core on the port layer.

## 1. The contract and its layouts

`sw/mailbox/mailbox.yaml` is the single source. Byte order stated once: every
register, record header word and event word is one 32-bit value with fields
at fixed bit positions; frame bytes travel four to a ring word in
little-endian lanes (byte k in word k/4 at bits 8*(k%4)); wire fields keep
network order. Full tables: `docs/reference/MAILBOX_CONTRACT.md` (generated);
design: `docs/design/MAILBOX_SPLIT.md`.

- Window 0x8000 bytes: registers below 0x400 (global block; interface block
  at 0x040, stride 0x10; channel blocks at 0x100, stride 0x20), event ring at
  0x400 (64 words), channel rings above (receive/transmit words: adp 256/128,
  acmp 256/256, aecp 512/512, maap 128/128, srp 1024/512).
- Global registers: ID (magic 0x4D42, major 1, minor 0), CAPS, IRQ_STATUS (RX
  levels, EVT level, sticky ERR rw1c), IRQ_ENABLE, NOW_MS, LINK, TICK_CTL,
  OWN_EID_LO/HI, FILTER_EN, MAAP_BASE_LO/HI, MAAP_COUNT, TMR_DEADLINE, TMR_CMD
  (slot, tag, op arm/cancel), EVT_HEAD, EVT_TAIL, BUS_ERR.
- Interface registers: GM_LO (reading it snapshots GM_HI and DOMAIN), GM_HI,
  DOMAIN. Channel registers: RX_HEAD, RX_TAIL (receive doorbell), TX_HEAD
  (transmit doorbell), TX_TAIL, RX_DROP, RATE_DROP, TX_ERR, RX_PASS.
- Records: RX frame (w0 LEN[15:0]/IF[19:16]/KIND[31:28]=1, w1 ARRIVAL_MS, then
  ceil(LEN/4) payload words); TX frame (w0 LEN/IF/KIND=2, w1 reserved 0,
  payload); event (4 words; w0 TYPE[7:0]/IF[11:8]/SEQ[31:16]; TIMER w1
  TAG[15:0]/SLOT[23:16], w2 deadline, w3 now; LINK w1 UP, w3 now; GM w1/w2 id,
  w3 domain; TICK w1 COUNT, w3 now). Every event source coalesced.
- Channels and filter: adp (0x22F0/0xFA: ENTITY_DISCOVER to 0 or own entity),
  acmp (0xFC: own talker or listener), aecp (0xFB: own target), maap (0xFE:
  PROBE/DEFEND/ANNOUNCE overlapping own range), srp (0x22EA, 0x88F5: all), each
  with a token bucket and a largest frame; untagged frames only.

## 2. The generator and its self-test

`sw/mailbox/gen_mailbox.py` emits `hdl/milan/mailbox/KL_mbx_pkg.sv`,
`hdl/milan/mailbox/KL_mbx.sv`, `sw/firmware/ctrl/mbx/mbx_contract.h` and
`docs/reference/MAILBOX_CONTRACT.md`. `--check` (byte drift), `--crosscheck`
(every constant by name in all three carriers, run-time tables in channel
order, every register decoded by the skeleton), `--selftest` (a positive
control, 8 planted output mismatches, 7 planted contract defects: 16 [ok]).
The model refuses overlapping fields, non-power-of-two or overlapping rings,
two channels on one classification, a register outside its block, a filter
field past the frame, a read-only field without a fabric source.

## 3. The HAL and the lwSRP port layer

- Bus port `mbx_hal.h`: read32, write32, wait. `plat/mbx_plat_mmio.c`
  (volatile 32-bit accesses at `CTRL_MBX_BASE`, the very name LiteX's
  generated `mem.h` emits for the switch-on region); `host/mbx_plat_host.c`
  (the model, plus an access trace hook).
- Driver `mbx/mbx.h`: contract check, filter setup, RX take (validated,
  resynchronised on a bad record), TX send (room check), all four event types,
  timers, tick enable, link, coherent GM read, IRQ.
- Port layer `port/`: `shlan_port.h` restates lwSRP's `src/ports/alloc.h`
  prototypes; `ctrl_pool` is a static size-class block pool (no heap
  fallback, refusals counted, double/interior/foreign frees refused,
  high-water marks); `ctrl_debug` one 120-byte line via `vsnprintf`.
- Loop `loop/ctrl_loop.h`: RX handler per channel, event sinks, centisecond
  consumers (`void (*)(void)`, `shlan_timer_tick`'s shape), polls; at most 8
  events and 2 RX records per channel per pass; bring-up order: contract,
  OWN_EID, IRQ_ENABLE, TICK_CTL (only with a tick consumer), FILTER_EN.
  Register `shlan_timer_tick` once, not `mrp_tick()` per application.
- RV32I freestanding build (pinned SDK gcc 14.3, `-march=rv32i -mabi=ilp32
  -ffreestanding -fno-stack-protector -Os`): portable set + MMIO platform,
  text 11040 B, bss 168 B; undefined only `memcpy memset vsnprintf` and libgcc
  `__lshrdi3 __mulsi3 __udivsi3 __umodsi3`.

## 4. The host mailbox model and harness (stimulus reuse)

- `host/mbx_model.c`: the fabric side at transaction level (registers, rings,
  filter and buckets, TX merge, timers, coalescing poster, interrupt), from
  the generated header; counts accesses, logs TMR_CMDs, captures TX frames.
- **The model is graded by the RTL's checks**: `tb/verilator/mbx/suite.hpp`
  is a template over a bench; the Verilator bench runs it through KL_mbx_wb
  and KL_mbx_axil (120 + 120), the model bench runs the same 120.
- **Co-simulation** (`tb/verilator/mbx/cosim_main.cpp`): the firmware on the
  RTL via Wishbone and on the model, one 21 s scenario: 5 frames (4
  ENTITY_AVAILABLE at index 0 to 3, ENTITY_DEPARTING at 4), identical bytes at
  identical NOW_MS (117, 7542, 14570, 18907, 20000). 13 checks.
- **Processor stimulus reused** (`sw/firmware/ctrl/test/ctrl_reuse.py`,
  `adp_walk.cpp`): proves the gitlink (`631eeb34`), the checkout and the blob
  of `protocol-processor/tb/adp_engine/sim_main.cpp`, then cuts its entity
  constants, its `model_frame` builder and its `ADV` Table 5.51
  transcription. 36 cells walked (N 10, I 16, S 4, C 6); the 9 "DELAY, draw in
  flight" cells are not applicable (the firmware draws and arms in one call).
  Plus the carried-over P1, P2, P3, P5, P7, P11, P12. 320 checks.
- **lwSRP port arm** (`--lwsrp <checkout>`, lwSRP `19f5796b`, not vendored):
  mrp_mad.c, mrp_pdu.c, timer.c, mvrp.c unmodified, alloc.c left out:
  `mvrp_app_create` on the pool; a JoinIn through the SRP channel registers
  VID 100; a Lv's leavetimer expires on fabric TICKs at 60 cs (not by 59, by
  61); destroy returns every block. Pool high-water 1 x 64 B and 3 x 256 B.
  13 checks.

Host test arms (`test_ctrl_firmware.py --require-rv32 --self-test --lwsrp`):
model 120, port 72, adp 47, walk 320, entity 45, rv32 1, lwsrp 13 (618).

## 5. The ADP slice: clauses, latency bounds, mutants

Milan v1.2 5.6.2, 5.6.3 (5.6.3.1, 5.6.3.5.1 to 5.6.3.5.11, Tables 5.49 to
5.51) over IEEE 1722.1-2021 6.2 (6.2.2.1 to 6.2.2.21; 6.2.2.15). Fields from
the entity model through `adp/adp_entity.py` (builder ADP identity and shape,
AEM overlay model id, `pp_adp_pkg::ADP_ENTITY_CAPS_C` via `gen_aemi_image`'s
reader, identify index 0 = ADP_IDX0's reset). Entity arm: 45 field checks over
the 5 shipped configs against `boot_policy.fabric_constants`, the builder's
ADP shape include and the processor package.

Latency bounds (`adp/adp_mbx.h`, mailbox accesses in the pass that takes the
input; measured = derived): DISCOVER 31, TMR_DELAY 39, TMR_ADVERTISE 11, GM 11,
LINK up 11 (down 9), SHUTDOWN 29. Response committed within two passes.

Planted defects: firmware 28 of 28 caught (`ctrl_mutants.py`: walk 10, one per
walked Table 5.51 row except the foreign DISCOVER, which the fabric filter
already drops and adp's A4 catches; adp 4, port 9, model 3, entity 1, rv32 1);
RTL 30 of 30 caught
(`tb/verilator/mbx/mutants.py`, after both positive controls; the suite's
default `make` runs a 4-arm subset, one per leaf). Every check group of the
suite has an arm except C4 (tagged, foreign and short frames) and E2 (link
coalescing while full), which no single-line defect isolates. Lists in the
READMEs.

## 6. Default build unchanged: proof

`--ctrl-mailbox` (default off) in `sw/litex/milan_soc.py`. Gateware exports
(`milan_soc.py <builder argv> --entity-gen-dir configs/generated/<cfg>
--no-compile`, LiteX venv, PYTHONHASHSEED=0) of every shipped config with the
base `milan_soc.py` (`git show fa450d30:sw/litex/milan_soc.py`, run from the
same directory, deleted after) and the head one, compared by `normdiff.py`
(drops timestamps, output paths and LiteX's comment-only hierarchy tree, whose
order varies between runs). Re-run at the head `f2187633`:

| Config | Argv | Files | Differ |
|---|---|---:|---:|
| ax7101_1x1_tdm8 (shipping) | shipping | 22 | 0 |
| ax7101_8x8 | shipping | 22 | 0 |
| arty_4x4 | shipping + `--sys-clk-freq 100e6` | 22 | 0 |
| arty_8ch | same proxy | 22 | 0 |
| arty_current | same proxy | 22 | 0 |

This LiteX checkout refuses the Arty configs at 83.333 MHz ("No PLL config
found") at the base exactly as at the head, hence the proxy. Switch on (1x1):
8 files differ, exactly: 7 mailbox sources in the tcl, the `KL_mbx_wb` and
`KL_mbx` instances, region `ctrl_mbx` 0x90100000 size 0x8000, CSR bank
`ctrl_mbx` at 0xf000f000 (pinned loc 30; no existing bank moved), interrupt 3.
Scratch scripts: normdiff.py sha256 0c66396311514ff7..., run_exports.sh
8b69b6c9d94d7ed6..., run_arty_proxy.sh eb9cf442fb13ed60....

Generated fragments: running the builder for the five configs leaves `git
status` clean, and the builder bank's elaboration gates (23f, 23g) reach
`Instance("milan_datapath")` for all five recipes.

Switch-on area (Vivado 2026.1, OOC, xc7a100tfgg484-2, 10 ns, KL_mbx behind
KL_mbx_wb via `tb_mbx_top HOST_P=0`, synth + place + route, run under the host
Vivado lock): 2,756 LUT, 2,713 FF, 1 RAMB36 + 10 RAMB18, 0 DSP; rx 1,006 / 994,
evt 711 / 978, tx 678 / 256, KL_mbx own 276 / 484, wb 66 / 1; 5636 of 5636 nets
routed, WNS +0.311 ns. Above #640's 1,500 to 2,000 LUT estimate; levers: the
timer bank (flip-flops, fits distributed RAM) and the per-term 64-bit filter
field registers. Digests: mbx_ooc.tcl 6b7b4388b872ec6d..., util_route.rpt
9a5b912dffa716cc..., util_route_hier.rpt fe4442a4e352e283...,
timing_route.rpt 65c03dcd11f5b7bb..., route_status.rpt 80e5afaa18cfb79b....

## 7. Gate table

All at `f21876336b91` and, for the gates the last two commits (test drivers
and docs only) touch, again at the head `0bfef4987eed`; foreground, logs and rc files
kept in the lane's scratch directory; every rc 0 except the one noted.

| Gate | rc | Result |
|---|---:|---|
| `gen_mailbox.py --check --crosscheck` | 0 | 0 finding(s) |
| `gen_mailbox.py --selftest` | 0 | 0 arm(s) failed (16 [ok]) |
| `make -C tb/verilator/mbx` (pinned Verilator 5.050) | 0 | 120 + 120 + 13 checks, 0 failures; quick mutants 4 of 4 |
| `tb/verilator/mbx/mutants.py` | 0 | both controls ok; 30 of 30 caught |
| `suite_tally.py --verdict` on the suite log | 0 | 253 checks, 0 failures, 3 tallies |
| `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp` | 0 | 7 arms ok (618 checks); 28 of 28 caught |
| `test_nvm_firmware.py --self-test` (existing firmware host test) | 0 | OK across 5 shapes |
| `test_builder.py --require-rv32` (LiteX interpreter given) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs an Arty route report absent on this host); 23f and 23g elaborate all five recipes |
| `lint_rtl.py --check --self-test` | 0 | PASS (90 <= ratchet 90) |
| `xvlog_gate.py --check` / `--selftest` (Vivado 2026.1) | 0 / 0 | PASS, 0 findings in hdl/ |
| `syn/yosys/run.sh --top KL_mbx --top KL_mbx_wb --top KL_mbx_axil` | 0 | 3 PASS; tied-input and tap-purity PASS |
| same, `--mode elaborate` | 0 | PASS |
| `check_soc_sources.py` / `--selftest` | 0 / 0 | OK / 25 of 25 |
| `check_rtl_source_lists.py` / `--selftest` | 0 / 0 | OK, 4 of 4 consumers / 49 of 49 |
| `check_baremetal_only.py --check` / `--selftest` | 0 / 0 | 0 findings / 700 arms |
| `check_sweep_shape.py`, `check_deploy_shape.py`, `check_entity_shape.py` (`--self-test`) | 0 | OK / OK / PASS |
| `check_wire_accountability.py --self-test` | 0 | PASS |
| sw/litex `test_pp_boot_bus_freeze`, `test_pp_mem_bridge`, `test_cpu_memory_port_cdc`, `test_gptp_tx_timestamp`, `iob_pack_selftest` | 0 | PASS |
| `check_sv_idiom.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sh_idiom.py` (+ `--selftest`) | 0 | OK, every ratchet holds |
| `check_hygiene.py --check`, `check_todo_ownership.py` | 0 | PASS |
| `measure_test_evidence.py --check` | 0 | PASS (ratchet could drop to 72) |
| `measure_naming.py --check`, `check_port_contracts.py`, `measure_fail_fast.py --check` | 0 | PASS |
| `gen_module_matrix.py --check` | 0 | 77 modules, 0 untested |
| `pp_srcs.py --check --selftest` | 0 | OK |
| `ci_events.py --check` / `--selftest` | 0 / 0 | OK (1655 items) / PASS |
| `docs_check.py` | 0 | 0 findings |
| `check_em_dash.py --base fa450d30` / `--selftest` | 0 / 0 | 0 findings over 1233 added lines / 339 arms |
| `check_doc_style.py`, `check_gptp_docs.py`, `DOC_MAP.gen.py --check` | 0 | OK |
| `check_solution_docs.py`, `check_submodule_docs.py`, `check_diagram_pngs.py`, `check_feature_status.py --self-test`, `check_archive.py` | 0 | OK |
| `check_doc_paths.py` | 0 | 924 cited paths resolve |
| `gen_toc.py --selftest` / `--verify-anchors` / `--check` | 0 | 1501 arms / 340 anchors / OK |
| `gen_hdl_reference.py --selftest` / build (pinned pyslang 11.0.0, scratch venv) | 0 / 0 | 44 of 44 / written |
| `git diff --check fa450d30 HEAD` | 2 | one line: `hdl/milan/mailbox/README-tests.md:21: new blank line at EOF`, the trailing blank `gen_module_matrix.py` writes into every per-family index (existing ones included); editing it would make `--check` stale |

Not run: `act` (the branch is not pushed; no PR head exists), the full
Verilator sweep (no existing suite compiles a changed file; the new suite is
auto-discovered and its log reads as 253 checks, 0 failures), `behave` (no
file under `tests/` or the processor model changed).

## 8. Open questions and risks

- **CI wiring.** The two firmware-side gates (`gen_mailbox.py --check
  --crosscheck --selftest`, `test_ctrl_firmware.py --require-rv32
  --self-test`) are not in hosted CI: `scripts/ci_events.py` pins the docs
  job's step list and each step's canonical script (tried and reverted), so
  wiring them is a reviewed change to that contract and `CI_WORKFLOWS.md`.
  The mailbox suite (RTL, co-simulation, quick mutants) is in the Verilator
  sweep.
- **The datapath side** of the skeleton is held idle under the switch; the
  protocol lanes connect it, with the clock crossing it needs.
- **Listener discovery** (Milan 5.6.4, F3) needs ADP AVAILABLE/DEPARTING from
  bound talkers: one more accept term (minor contract change).
- **lwSRP transmit**: no PDU transmit hook yet; F4 adds one upstream.
- **CPU cycles**: latency is stated in mailbox accesses; the shipping-core
  cycle figure needs the switch-on SoC in the CPU simulation.
- **Area** is above #640's estimate (no bar yet); two levers named above.
- `scripts/test_evidence.budget` could be lowered to 72 (not done here).
- **Seam with F1** (#665 comment 5993775541 gives F1 its own flash port: read,
  program, erase, busy-wait, time). F0's ports are the mailbox bus
  (`mbx/mbx_hal.h`), lwSRP's allocation and print (`port/shlan_port.h`) and the
  loop's centisecond tick. Reconciliation proposed: one platform layer
  (`sw/firmware/ctrl/plat/`) that implements every port for a target, F1's
  `time` backed by NOW_MS (`mbx_now_ms()`) where the mailbox exists, F1's
  busy-wait yielding to `ctrl_loop_service()` rather than spinning, F1's
  buffers sized statically from the shape (the block pool is only for
  lwSRP's attribute churn), and `ctrl_app` composing both.

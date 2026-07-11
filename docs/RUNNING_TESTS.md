# Running the tests  -  the complete guide

*2026-07-10. Every verification layer in this repo, how to run each one, what it
covers, how long it takes, and the traps that have actually bitten. Written from a
session that used all of them to root-cause two RTL bugs and a livelock.*

The layers, cheapest-first (run them in this order when iterating):

| # | Layer | Tool | Time | Catches |
|---|-------|------|------|---------|
| 1 | Import/elaboration smoke | python | ~2 s / ~2 min | syntax, width/name errors, Migen codegen traps |
| 2 | LiteX/Migen behavioral suites | migen sim | 1–20 min | protocol/ordering/pairing logic, driver-contract breaks |
| 3 | Verilator harnesses | verilator | ~1 min each | standalone SV modules (ADP, CBS, classifier, CDC…) |
| 4 | Yosys portability | yosys+sv2v | minutes | Xilinx-primitive leakage, device portability |
| 5 | P&R + timing | Vivado | ~50 min | timing, congestion, utilization |
| 6 | Silicon §V | board | ~15 min | everything the models missed |

---

## 1. Elaboration smoke test (ALWAYS before committing RTL to P&R)

```sh
cd sw/litex
/home/alex/litex-milan/venv/bin/python -c "import milan_soc"       # ~2 s: syntax/widths
```

Full elaboration without Vivado (generates verilog + csr.csv, no bitstream, ~2 min):
run the intended build script with `--build` REMOVED (run=False path). Then the
**mandatory Migen-codegen grep**  -  Migen can emit ILLEGAL Verilog that only Vivado
rejects (Synth 8-2716), from three known constructs:

- nested Array proxies: `arr[sig_a[sig_b]]`  -  resolve the inner index into a plain
  comb Signal first (the "single-level hop" pattern, see `cq_of_*` in milan_soc.py);
- computed array-WRITE indices: `arr[(tail+1)[:n]]`  -  precompute into a Signal;
- FSM `NextValue` on packed 1-bit Arrays  -  use a `Signal(N)` bit-vector with RMW.

Check the generated build dir: `grep -nE "^\s*\(.*\+.*\) *(<=|=) " <build>/gateware/*.v`
(any arithmetic on the LHS = miscompile). Sim will NOT catch these  -  the Python
simulator evaluates the intent, not the emitted Verilog.

## 2. The LiteX/Migen behavioral suites (sw/litex/test_*.py)

These are plain scripts  -  **no pytest** (not installed in the venv). Two ways to run:

```sh
cd sw/litex
/home/alex/litex-milan/venv/bin/python test_ring_bd.py          # full suite (~10-20 min)
/home/alex/litex-milan/venv/bin/python -c "
import test_ring_bd as t
t.test_hs_livelock_orphan()"                                    # one test
```

Suites and what they own:

- **test_ring_bd.py**  -  THE regression net for the RX BD/RSC/header-split engine
  (~40 tests: +full-gate, +hs CQ pressure, cut-through ordering since hsq12). Ordering invariants (BD order == posted-pop order), the drops/v2-alias
  regression, half-BD guards, multi-slot RSC, hs split/crossing/interleave/famine,
  reload flush, storm models, the livelock probe, the BD-ring full-gate (hsq6: drain
  stalls at wr+16==rd instead of lapping the driver). `ALL PASS` on success; each test
  prints a `PASS <name>` line. NOTE the driver contract the models mirror since hsq6:
  every mid-sim reap ends with a RING_RD write (`BDHarness.rd_sync(m.bd_rd)`), every
  heal with `rd_sync(0)`  -  a model that reaps without advancing rd_ptr wedges the
  gated HW exactly like a dead driver.
- **test_ring_dma.py**  -  the base `Harness` (ring mode) + AXI slave memory model.
  Imported by test_ring_bd via `importlib` (module name `trd`), also runnable alone.
- **test_ring_tx.py / test_tx_bd.py**  -  TX ring + TX BD engines (HW-TSO era).
- **test_ring_writeback.py**  -  pointer-writeback.
- **test_rx_steer.py**  -  the 2-queue flow-steering front-end.

Run the WHOLE ring suite after ANY RingDMAWriter change; it is the contract net that
caught the s_cq width relic shrink and would catch a CQ regression.

### 2.1 Harness architecture (what a test looks like)

```python
h = BDHarness(ring_size=4096, max_frame_beats=256, fifo_beats=2048,
              burst_beats=16, cycles=150000)
def stim():                       # ONE generator = the test body
    yield from h.init_bd(bd_entries=64)
    yield h.dut.rsc_en.storage.eq(1)          # poke CSRs directly
    yield from h.post_buf(0x100000)           # post an RX buffer (the driver's job)
    yield from h.send_frame(words)            # inject a frame (64-bit beats)
    ...
h.run(stim)                       # wraps stim + axi_slave + ready_monitor
```

- `h.mem` is a plain dict = the AXI slave memory. Read it mid-sim (`h.mem.get(addr)`)
  or via `h.read_bd(idx)` / `h.read_buf(addr, beats)`. BDs land at `BD_BASE`.
- `tcp_frame()/tcp_tagged()` build real TCP frames (flags/doff/seq/ports) so the RSC
  eligibility decode runs authentically.
- Checkers: `DriverModel`/`StormModel` MIRROR kl-eth's reap (incl. the half-BD guard
  and w1-clear). **They mirror the CONTRACT, not the C code**  -  a bug in the driver's
  own control flow (e.g. the hsplit consume fall-through) is invisible here. When
  silicon disagrees with a green sim, suspect the driver C first.

### 2.2 Timing budgets and geometry traps

- `cycles=` is the hard sim budget. The 100 MHz silicon values scale 1:1 (rsc_tout
  500 µs = 50 000 cycles, agemax 2 ms = 200 000)  -  size `cycles` to cover the phases
  you need, not more: python sim runs ~10-50k cycles/min depending on watchers.
- `Harness` DEFAULT `max_frame_beats=16` TRUNCATES MTU frames  -  a 1448-byte frame
  needs `max_frame_beats>=190`; use 256. Symptom of the trap: phantom "wedges" from
  silently clipped frames.
- Bounded posted pools must be REPLENISHED if the regime is supposed to model the
  driver (kl-eth reposts what it consumes). A fixed pool that dries up produces
  convincing-but-fake famine failures (this session's first false repro).

### 2.3 Cycle-exact introspection (the livelock toolkit)

`RingDMAWriter` exposes zero-cost debug aliases (plain attribute refs, no hardware):
`dbg_cq_head/tail/done`, `dbg_s_open/s_cq/s_cqm`, `dbg_pv3_pend/pv3_cqi/meta_cqi`,
`dbg_head_open_hit`, `dbg_cq_level`. Read them in any generator:
`hd = yield h.dut.dbg_cq_head`, arrays per-element: `yield h.dut.dbg_cq_done[i]`.
FSM state: `st = yield h.dut.fsm.state`; decode numbers with
`h.dut.fsm.encoding` (dict name→code; build a dut + `.finalize()` to print it).

For 1-cycle pulses (e.g. `pv3_pend` set one cycle, consumed the next) a sampler
INSIDE stim aliases  -  you MUST use an independent full-rate generator:

```python
def watcher():
    while not state["stop"]:      # MUST be stoppable  -  see trap below
        yield
        ... read dbg signals, print transitions with a cycle counter ...
h.run(stim, extra_gens=[watcher()])   # Harness.run grew extra_gens for this
```

**Trap:** a `while True` watcher never exhausts, so `run_simulation` runs to the FULL
`cycles=` budget even after stim returns (a 2M-cycle budget turned a 10-minute test
into 4+ hours). Always share a stop flag that stim sets on every exit path.

**Trap:** printed event ORDER from sparse samplers is meaningless  -  batch prints
lag. Only the full-rate watcher's cycle numbers are ordering-trustworthy.

## 3. Verilator harnesses (tb/verilator/*, 18 of them)

Standalone self-checking C++ harnesses for the pure-SV modules (adp, adp_tx, cbs,
cdc, classifier, csr, datapath, ptp, …). Each dir:

```sh
cd tb/verilator/adp && make        # builds + runs; self-checking, prints PASS/checks
```

No Xilinx dependencies (the RTL is XPM-free). Run the affected module's harness after
touching its SV; run all 18 before a release-ish commit (`for d in tb/verilator/*/;
do make -C "$d" || break; done`).

## 4. Yosys device-portability check (syn/yosys)

```sh
cd syn/yosys && ./run.sh           # sv2v + yosys generic-cell mapping, per-module
```

Proves the RTL maps to a generic cell library (no silent Xilinx-primitive
dependences); historically 17-18/18 green (ECP5 target as the neutral device).

## 5. P&R (Vivado)  -  see the build scripts

`~/litex-milan/work/build_*.sh` are the reproducible build recipes (each one = a
documented experiment). Conventions: `source /home/alex/Xilinx2/2026.1/Vivado/settings64.sh`,
venv on PATH, `--vivado-max-threads 32` (hard cap  -  more aborts P&R), launch via
`nohup <script> > <log> &`, watch for the bitstream file. ~50 min. Read the LAST
"Design Timing Summary" (post-physopt)  -  mid-router WNS lines are pessimistic.
Utilization headroom is thin (~81-98% LUT/slice depending on build): big register
arrays (e.g. CQ depth) can overflow placement  -  check
`<build>/gateware/*utilization_place.rpt`.

## 6. Silicon §V (board validation checklist)

After flashing/JTAG-loading any new bitstream, BEFORE trusting any number:
1. `MILN` ID probe (driver prints it at insmod), CBS `en=0` at reset,
2. correct driver + params (`cat /sys/module/kl_eth/version`; rsc/rsc_clk_mhz/hwtso/hwcs/hsplit),
3. known-good single-flow cell vs the build's baseline, `dmesg` clean
   (no pairing/realign/resync), drop counters sane (`devmem 0xf000303c`),
4. throughput claims ONLY from the peer-side tx_bytes 5 s time-series
   (`ssh amx-pw0 cat /sys/class/net/enp6s0/statistics/tx_bytes`, delta/5 s ×8)  - 
   short cells are slow-start-flattered,
5. verify the PEER is real: board `ip neigh` for 192.168.127.2 must show the pw0
   i210 MAC (68:05:ca:95:b2:d1)  -  a stale ARP to a ghost host invalidates everything.

## The debug playbook that worked (for the next hard bug)

1. Reproduce on silicon with counters (CSR probes)  -  capture the fingerprint.
2. Reproduce in sim at the same regime  -  INCLUDING the driver's behavior (reap+repost),
   or you will chase harness artifacts.
3. Bisect with the layered monitors: transition sampler → full-rate watcher →
   FSM-state tags on events → (if needed) new dbg aliases. Every iteration is
   minutes, not builds.
4. Name the exact state/cycle, read that RTL path, fix, suite, ONE build, silicon.

# Session handoff — goals, topology, harness (read this first)

*2026-07-10 end-of-campaign snapshot. Companion docs: RUNNING_TESTS.md (test layers),
HEADER_SPLIT_DESIGN.md (hs design + silicon history), QSPI_FLASHBOOT.md (boot),
GIGABIT_HEADROOM_ANALYSIS.md + PERFORMANCE_GOAL.md (the why), PERF_ON_MILAN.md
(profiling method).*

## 1. Goals — where the campaign stands

**Standing goal: >500 Mbit/s best-effort TCP BOTH directions at MTU 1500** on the
fully-FPGA Milan NIC (AX7101, 2× VexiiRiscv RV64 @100 MHz — clock LOCKED at 100 by
user decision), reaching toward line rate (941). Scoreboard:

| Metric | State |
|---|---|
| TX | **✓ 525–536** (done since r2slots era) |
| RX socket-TCP, mslot keeper | 368–407 steady -P8 (2-queue, hsq3+mslot60d/hsplit9-legacy) |
| RX single-flow record | **340 steady** (header-split, hsq4/hsq5) — aligned-copy win |
| RX hs multi-flow | **negative scaling ROOT-CAUSED+FIXED (hsq6)**: P4 295 / P8 240, 0 desyncs |
| Zero-copy | works (86.5% zc) but slower than aligned copy at 100 MHz — parked |

**2026-07-10 (late): hs multi-flow scaling SOLVED** — the collapse was the un-gated
BD-ring drain (HW lapped the driver's rd → "RX BD desync" resync-storm blackouts;
silent seq-aliased corruption at 256 entries = why e251a0c's 256-ring failed). Fix:
hsq6 gates the drain at wr+16==rd + kl-eth **hsplit10** (BD 256, POST 60). Same-day
A/B: P4 231→**295** (+28%), P8 183→**240** (+31%), P1 unregressed, 0 desyncs
everywhere. **NEVER load hsplit10 on ≤hsq5 gateware** (silent lap by construction).
Full story: HEADER_SPLIT_DESIGN.md §build_hsq6; memory bd-ring-lap-rootcause.

**Next work, in order of value:**
1. **2-queue header-split** — re-add rx1+steer with hs (needs slice diet or CQ-width
   work; hsq4/5/6 are 1-queue to fit CQD=32). mslot's 368-407 aggregate is a 2-queue
   number; hs at 295-312 per-queue is knocking on it.
2. **Residual drop shaving** — ~58/flow/s constant reap-gap drops remain (194-319/s
   at P4/P8): opens blocked in µs windows while bursts outrun the poll. Levers:
   pressure-close covering the open-slot-PAGE-at-head case (close_prs never fires —
   head_open_hit only matches the META entry), poll cadence, POST >63 (needs HW post
   FIFO deepening past 64).
3. **AREA-70 campaign (user directive 2026-07-10)** — after the 2-queue work:
   slices 96.8% → ~70% (reclaim ≥4250, more once 2-queue lands). Levers: more
   Array→LUTRAM diets (CQ-swap pattern), strip-probes ship build (tlm block +
   Phase-0 probes behind a flag), legacy byte-ring path removal (kills driver
   bd=0 fallback — decide consciously), Vivado area strategies. The point:
   headroom for the ADP/AVDECC product blocks.
4. **XDP / AF_PACKET data plane** (user-approved endgame) — copy-free consumer path
   toward 941; hs page-aligned delivery is the substrate.
5. Residual single-flow drops (~51/s, lap-independent) — refinement.

## 2. Topology — what plugs into what

```
┌─────────────── dev VM (this machine) ───────────────┐
│ /home/alex/prjs-avb-on-fpga/milan-fpga   (RTL repo)  │
│ /home/alex/milan-tests-avb               (driver)    │
│ /home/alex/litex-milan/work/build_*      (builds)    │
│ /home/alex/br-milan-output               (buildroot) │
│                                                      │
│  USB: ttyUSB0 = FT232H JTAG ──────────┐              │
│       ttyUSB1 = CP2102N console ────┐ │              │
└─────────────────────────────────────┼─┼──────────────┘
                                      │ │
                       ┌──────────────▼─▼───┐   1 GbE copper   ┌──────────────┐
                       │  AX7101 board      │◄────────────────►│  amx-pw0     │
                       │  192.168.127.1     │                  │ i210 enp6s0  │
                       │  MAC 02:00:..:01   │                  │ 192.168.127.2│
                       └────────────────────┘                  │ (ssh, sudo -n)│
                                                               └──────────────┘
```

- **Data-plane peer = `ssh amx-pw0`** (passwordless, passwordless sudo). Its i210
  (`enp6s0`, MAC `68:05:ca:95:b2:d1`) is the wire peer at **192.168.127.2**.
  **`amx-pw1` is RESERVED — never touch it.**
- The VM has NO data-plane path to the board (its NICs are virtio/isolated). JTAG +
  serial only. Do NOT add 192.168.127.x addresses on the VM.
- **Ghost-peer check before trusting ANY number**: on the board,
  `ip neigh | grep 127.2` must show `68:05:ca:95:b2:d1`. Stale services answering
  .2 from elsewhere invalidated a whole night once.

## 3. How to connect

**Console** (tmux session `milan_qspi_boot`, recreate if dead — litex_term needs the
venv path):
```sh
tmux new-session -d -s milan_qspi_boot \
  "/home/alex/litex-milan/venv/bin/litex_term /dev/ttyUSB1 --speed 115200"
```
Scripted exec on it: `scratchpad/conx.sh '<cmd>' <timeout>` (unique-tag markers;
survives garbled output). `dmesg -n 1` first on the board. NEVER
`pkill -f litex_term` / `tmux kill-server` — kill exact PIDs only.

**Load a bitstream (JTAG SRAM — flash holds NO bitstream by design):**
```sh
openFPGALoader -c ft232 ~/litex-milan/work/build_hsq5/gateware/alinx_ax7101.bit
```
Boot is hands-free from QSPI images (SPIFLASH_SKIP_FREQ_INIT validated; ~75 s to
login incl. 35 s initramfs unpack; the "invalid magic" line at ~35 s is benign).
**Power-cycle ⇒ FPGA blank ⇒ JTAG load required.** NEVER `openFPGALoader -f <bit>`
(clobbers the kernel at flash offset 0 — recovery recipe in QSPI_FLASHBOOT.md;
manual flashboot fallback: `scratchpad/manual_flashboot.sh`).

**Board network + driver (fresh boot):**
```sh
# on the console (root, no password):
ip addr add 192.168.127.1/24 dev eth0; ip link set eth0 up
wget -O /tmp/kl10.ko http://192.168.127.2:8000/kl-eth-hsplit10.ko
rmmod kl_eth; insmod /tmp/kl10.ko rsc=1 rsc_clk_mhz=100 hwtso=1 hwcs=1 hsplit=1
ip addr add 192.168.127.1/24 dev eth0; ip link set eth0 up
echo 0 > /sys/class/net/eth0/threaded; ethtool -C eth0 rx-usecs 500
wget -O /tmp/recv_spin http://192.168.127.2:8000/recv_spin; chmod +x /tmp/recv_spin
```
`hsplit=0` = legacy/mslot-equivalent mode (same .ko). **Driver↔gateware pairing is
STRICT**: hsplit10 (BD ring 256) needs the hsq6+ full-gate — on ≤hsq5 it laps the
ring SILENTLY (8-bit seq aliases at 256). hsplit9 (BD 64) is the ≤hsq5 driver. On
2-queue gateware (hsq3) also `devmem 0xf0003094 32 1` (hash_sel→q0) BEFORE TCP; on
1-queue hs builds (hsq4/5/6) that CSR does not exist — don't poke it.

**Peer services (amx-pw0, serve dir /tmp/serve):**
```sh
ssh amx-pw0 'cd /tmp/serve && setsid nohup python3 -m http.server 8000 --bind 0.0.0.0 \
  >/tmp/serve/http2.log 2>&1 & setsid nohup /tmp/serve/blast2 5202 >>/tmp/serve/blast2.log 2>&1 &'
```
`blast2` = instrumented TCP sender (logs bytes+errno per connection death). Kill
STALE listeners by exact PID first — a wedged old blast produced a fake "collapse."
Stage new driver builds: `scp kl-eth.ko amx-pw0:/tmp/serve/kl-eth-<ver>.ko`.

## 4. How to harness

**Sim/test layers:** see **RUNNING_TESTS.md** (elab smoke + Migen-codegen grep →
`test_ring_bd.py` suite (39 tests incl. the livelock regression; plain python, no
pytest) → 18 Verilator harnesses (`tb/verilator/*/make`) → Yosys (`syn/yosys/run.sh`)
→ Vivado build scripts (`~/litex-milan/work/build_*.sh`, ≤32 threads, read the LAST
timing summary) → silicon §V checklist). Cycle-exact debugging: `dbg_*` aliases on
RingDMAWriter + the stoppable full-rate watcher via `h.run(stim, extra_gens=[...])`.

**Driver build** (kl-eth, out-of-tree against the buildroot kernel):
```sh
cp /home/alex/milan-tests-avb/fpga/kl-eth/kl-eth.c /home/alex/br-milan-output/build/kl-eth-1.0/
cd /home/alex/br-milan-output/build/kl-eth-1.0 && \
PATH=/home/alex/br-milan-output/host/bin:$PATH make -C /home/alex/br-milan-output/build/linux-7.0.11 \
  M=$PWD ARCH=riscv CROSS_COMPILE=riscv64-buildroot-linux-gnu- modules
strings kl-eth.ko | grep version=        # ALWAYS verify before staging
```

**Measurement discipline** (the rules that kept this campaign honest):
- Sustain metric = peer tx_bytes 5 s deltas ×5+ (`ssh amx-pw0 cat
  /sys/class/net/enp6s0/statistics/tx_bytes`); short cells are slow-start-flattered.
- Cells: `recv_spin <ip> 5202 <cport|0> <secs> 0 0 1 262144` on the board; -PN =
  N instances with distinct cports. `recv_zc` for zerocopy (same args).
- Every cell: drop delta (`devmem 0xf000303c`), `dmesg | grep -c pairing`,
  close-reason deltas when diagnosing (@0xf00040cc..d8: psh/cap/tout/park).
- perf on the board: timer-only (`-F 250`), symbolize on the host via System.map —
  full method in PERF_ON_MILAN.md.
- Measure, don't assume — probe first, before AND after (measure-dont-assume rule).

**Current board state:** hsq7 (JTAG-SRAM, WNS+0.028, BD-ring gate + CQ LUTRAM
diet, LUTs 74.2%) + hsplit10 hsplit=1, network up. Gateware ladder: hsq3 =
2-queue keeper (mslot aggregate best), hsq4 = CQD=32 1-queue, hsq5 = + livelock
fix, hsq6 = + BD-ring full-gate (WNS+0.243), **hsq7 = + CQ diet = the 1-queue
hs keeper** (P1 312 / P4 ~283±6, silicon-unregressed, pairs with hsplit10
ONLY); hsq7t = 2-queue diet canary (q0-hs+q1-legacy, 99.4% slices, +0.028) —
FITS+CLOSES but no room for rx1-hs until strip-probes lands.

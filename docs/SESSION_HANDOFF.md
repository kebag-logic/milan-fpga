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
| RX hs multi-flow | best: **hsq10-16K P4 381/374soak** (~375 plateau, ACK-hold). hsq12+hsplit14 CUT-THROUGH first silicon: **P1 329 = new single-flow record** (mechanism engages) but P2 324 / P4 281 REGRESS — q1-heavy drops (190/s), per-unit cost, partial-page HOL under interleave = the next investigation |
| Zero-copy | works (86.5% zc) but slower than aligned copy at 100 MHz — parked |

**2026-07-10 (late): hs multi-flow scaling SOLVED** — the collapse was the un-gated
BD-ring drain (HW lapped the driver's rd → "RX BD desync" resync-storm blackouts;
silent seq-aliased corruption at 256 entries = why e251a0c's 256-ring failed). Fix:
hsq6 gates the drain at wr+16==rd + kl-eth **hsplit10** (BD 256, POST 60). Same-day
A/B: P4 231→**295** (+28%), P8 183→**240** (+31%), P1 unregressed, 0 desyncs
everywhere. **NEVER load hsplit10 on ≤hsq5 gateware** (silent lap by construction).
Full story: HEADER_SPLIT_DESIGN.md §build_hsq6; memory bd-ring-lap-rootcause.

**NAPI topology verdict (2026-07-11 pm, closes the q1-asymmetry thread):** the
2-hart winner is the PIPELINE (all NAPI softirq on cpu0, receivers on cpu1) —
measured P4: softirq 281-381 vs threaded-unpinned 220 vs threaded-PINNED 206
(hsplit15 binds each queue's kthread to its hart; STILL loses: symmetric
queue-fanout fights the copy stage for both harts). cpu1 softirq ==~0 in every
cell = the "2-queue fanout" never fanned RX compute; q1's drops are the
pipeline's tail latency (q1 NAPI runs after q0 per round), not a placement bug.
threaded=0 stays the recipe. Cut-through (hsq12+hsplit14/15): single-flow
RECORD 329, multi-flow loses to the keeper => parked as the P1 lane until the
staircase (8K pages) or chunk batching is explored.

**NEXT CAMPAIGN (decided 2026-07-11 pm, builds on the full map): the AF_PACKET
data plane on hs pages — the measured RX>500 lane.** Socket-TCP RX has consumed
its knob space (381/374 keeper; ACK-hold plateau physics + pipeline topology +
famine + every latency knob all measured); the no-copy consumer lane measured
481 at -P2 in the MSG_TRUNC ceiling test BEFORE this campaign's improvements,
and it is both the user-approved endgame and the actual AVTP product path.
**CEILING RE-BASELINED (2026-07-11 pm, the campaign's first datum): MSG_TRUNC
on today's keeper = P2 585 / P4 594 peer-sustained (was 481 pre-hs-era)** — the
no-copy lane is ABOVE the 500 goal NOW; the socket copy costs exactly
585->374. Step 1 (next): `tools_recv_ring.c` (AF_PACKET TPACKET_V3 mmap RX,
~1ms block timeout, cpu1-pinned A/B) on the keeper -> P2/P4 vs the 585-594
ceiling; the ring taps POST-GRO so TCP traffic arrives as 57KB units (amortized).
**AF_PACKET RING REFUTED (measured 124/139 vs trunc 585): TPACKET rings are
copy-INTO-ring on RX** (kernel memcpys every unit into the ring on cpu0) —
consumer-side zero-copy only. **ZC-FLIP MEASURED (hsq13 @4K + hsplit14, WNS+0.147, pairing correct, 0 panics):
110-113 Mbit at 87% zero-copied — REFUTED as a throughput lane.** The flip
MECHANISM works (hs 4K pages qualify exactly as designed) but the LIVE kernel
zc path costs ~290us/page on this 100MHz sv39 core (cpu1 100% sys-saturated;
no-zap + 64MB-window variants identical => not the DONTNEED zap, not syscall
batching — the per-page vm-insert path itself). The 1.22us/page pricing was
the RAW mapbench, not the live path. CONSUMER LADDER FINAL: copy 363-381 |
MSG_TRUNC ceiling 585-594 | AF_PACKET ring 124 | zc-flip 110@87% — every
no-copy consumer API on kernel 7.0.11 LOSES to the plain copy at 100 MHz.
KERNEL ARCHAEOLOGY DONE (2026-07-11 pm): 7.0.11's zc path IS batched
(vm_insert_pages, TCP_ZEROCOPY_PAGE_BATCH_SIZE=32) — the cost is the
equilibrium economics, not missing batching: at low rate the queue never
deepens (1-2 pages/call, per-call overhead lands per-page); pacing to force
depth hits the rcv-window wall instead (paced variants: 2.7 @default-rcvbuf,
19.5 @4MB-rcvbuf+10ms — worse, not better). FOUR variants measured: 110 / 113
no-zap / 2.7 / 19.5. **zc lane CLOSED on this core+kernel.** Remaining >500
lane: AF_XDP ZC driver (true zero-copy, campaign-scale). The AVTP PRODUCT
plane is unblocked regardless (media streams are Mbit-class). HARDENING
SHIPPED: hsq14 capability CSR @0xf000311c + hsplit16 probe-check (refuses
lethal pairings); hsq14 sweep building = the next keeper.
**⚠⚠ PAGE-SIZE PAIRING IS LETHAL: hs_pgsz (driver) MUST equal hs_page_bytes
(gateware). Mismatch = the writer DMAs gateware-page strides into smaller
driver pages = KERNEL MEMORY OVERWRITE => Bad page map + panic (2026-07-11:
hsq12@16K + hs_pgsz=4096 panicked on first wget). There is NO capability CSR
yet — a gateware hs_page_bytes readback CSR + driver probe-check is the
required hardening (add to hsq13 follow-up).**
Step 2: fanout (PACKET_FANOUT_HASH) across 2 sockets/harts. Step 3: if the
stack tax (netif_receive->packet_rcv) binds, THEN driver XDP (bigger lift).
TCP numbers stay the regression net; TX gate discipline unchanged.

**Older next-work list (dawn), still valid below the campaign:**
1. **RX 381 -> 500 on hsq10** — the knob space is EXHAUSTED (2026-07-11 am):
   rx-usecs FLAT 359-381 across 100-1000us; segcap=10 HARMFUL (256, chaotic);
   PAYCAP poke blocked (RING_RSC_BUFSZ CSR truncates at 16 bits). TCP state at
   P4-16K: cwnd HEALTHY 88-212 segs, **rtt inflated 7-55 ms = the binder**
   (RSC fill-time ~4.6ms/aggregate is only part; cutting aggregates costs more
   than it buys). NEXT INSTRUMENT, not next knob: the R1-era latency
   decomposition (wake/delivery legs) on the 16K regime — find where the
   ~10ms base delivery rtt lives (NAPI batch? GRO hold? recv wake? ACK-tx
   batching?). Then: 32K pages for the P6/P8 interleave tail; PAYCAP CSR
   widening (RTL) only after the rtt story is decomposed. Steer_q* counters
   misreport under dual-active = telemetry bug (single-active deltas only).
   Beware cport TIME_WAIT: back-to-back cells MUST use fresh cport bases.
   **PLATEAU CLOSED-FORM (2026-07-11 am): per-flow ~95 Mbit = PAYCAP/fill-cycle**
   — RSC holds a flow's aggregate during fill (~5ms at 57KB), ACKs wait for
   close, the peer paces at cwnd/(rtt incl. fill): self-limiting equilibrium.
   Knob ledger v2 (all refuted at P4-16K): fastpoll-decouple 377 (poll cadence
   =/= binder), quickack 294 HARMFUL (streaming-kills rule holds; q1 drops 94/s),
   napi_w=16 355 (batch depth =/= binder). EXITS: (a) flow-count path = 32K
   pages (hsq11, building) => P8 drops->0 => 8x~60-90 CPU-capped ~500; (b)
   **hsplit14 per-page delivery** (LRO-style): deliver each 16K v3 as a
   synthesized TCP segment as it LANDS instead of waiting for the meta =>
   effective rtt /4 at unchanged aggregate efficiency. Blocker: v3s carry
   tag+addr but hdr_idx arrives only in the META (close) — under interleave the
   first-v3 order can differ from open order, so the driver cannot safely bind
   headers early. RTL assist: put hdr_idx (5b) into v3 w0 spare bits => hsq12 +
   hsplit14 STRICT pair. Design sketch committed here; execute next session.
2. **TX 2-proc fairness lottery** (one iperf3 starves at ~82; capability 582-646
   intact): CONFIG_NET_SCH_FQ kernel rebuild (fq pacing), or BQL. NOT a gateware
   bug — measured across hsq7t..hsq10, ACK steering constant-on-q0.
3. **AREA-70 campaign (user directive)** — slices to ~70%; banked: CQ LUTRAM diet
   -4866 LUTs + strip-probes -1135 LUTs/-4267 FFs. Next: legacy byte-ring
   removal, CBS 4.4K/datapath-CSR 5.9K audits, Vivado area strategies.
4. **XDP / AF_PACKET data plane** (user-approved endgame) — copy-free consumer
   toward 941; hs page-aligned delivery is the substrate.
5. Refinements: single-flow residual ~50/s; hs delivery-latency shave (the
   remaining gap per flow); per-queue hs capability bit CSR (replace the STRICT
   hsplit pairing convention).

## 2. Topology — what plugs into what

```
┌─────────────── dev VM (this machine) ───────────────┐
│ /home/alex/prjs-avb-on-fpga/milan-fpga   (RTL repo)  │
│ /home/alex/the-private-test-repo               (driver)    │
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
cp /home/alex/the-private-test-repo/fpga/kl-eth/kl-eth.c /home/alex/br-milan-output/build/kl-eth-1.0/
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

**Current board state:** hsq10_epo (JTAG-SRAM, WNS+0.114, 2q-hs + strip-probes +
16K hs pages) + **hsplit12 hsplit=2 hs_pgsz=16384**, network up. RX record P4 381
(374 soak); TX gate 582-637. Overnight ladder + forensics: HEADER_SPLIT_DESIGN
§hsq8/9/10; cells in scratchpad results_hs2q.csv. Gateware ladder: hsq3 =
2-queue keeper (mslot aggregate best), hsq4 = CQD=32 1-queue, hsq5 = + livelock
fix, hsq6 = + BD-ring full-gate (WNS+0.243), **hsq7 = + CQ diet = the 1-queue
hs keeper** (P1 312 / P4 ~283±6, silicon-unregressed, pairs with hsplit10
ONLY); hsq7t = 2-queue diet canary (q0-hs+q1-legacy, 99.4% slices, +0.028) —
FITS+CLOSES but no room for rx1-hs until strip-probes lands.

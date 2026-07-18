# HANDOVER — machine, topology, live state, tasks

Updated 2026-07-15 (post Milan v1.2 AEM/AECP mandatory-set + ACMP listener
SM close-out; lwSRP fabric engine landed 07-14 @ `b19287e`).
This is THE entry point for a fresh session or person: everything needed to
operate the bench, trust the current state, and pick the next task. Detail
lives in the named normative docs; this file states what is true NOW.

**Project in one paragraph:** a fully-FPGA Milan v1.2 AVB endstation — the
whole TSN datapath AND the AVDECC control plane (ADP + AECP/AEM + ACMP talker
SM) run in fabric, zero-CPU; a VexiiRiscv 2-hart Linux softcore does only
provisioning, linuxptp and ops (USER DIRECTIVE rev 2: "everything goes FPGA,
use lwSRP" — normative split: `docs/design/ARCHITECTURE_HW_SW_SPLIT.md`).
Roles: AX7101 = the full endstation (:01), Arty A7-100 = a small endstation
(:02), nothing bridge-side in scope. Both boards are silicon-validated
**Milan=1 CLEAN** (la_avdecc) as of 2026-07-14.

---

## 0. BENCH SESSION 2026-07-18 (audio quality root-caused) — results + open items

**User-audible bug ("pumping") root-caused end to end.** The morning silence
("nothing on the Arty PMOD") and the afternoon pitch-pumping were TWO
distinct defects, both now fixed in RTL (milanfinal9, build pending):

1. **Silence** = format mismatch, NOT the switch: the AX transmits 2ch
   frames (framer hardwired stereo) while its AEM STREAM_OUTPUT *declared*
   8ch; Hive format-matched the arty listener to the declared 8ch → RX
   monitor rejected every frame UNSUPPORTED (0x6C0 mid-byte counting).
   Diagnosis path: `ip -s link` showed ~7 kpkt/s arriving while FRAMES_RX
   sat at 0 → wire capture → chans=2 on the wire. Fix = **talker truth**
   (`fd11b4d`): STREAM_OUTPUT declares + accepts ONLY the wire format
   (2ch 48k); listener stays adaptive (1..8ch). Controller gained
   `--bind TALKER_SFX LISTENER_SFX` (talker fmt → listener fmt →
   CONNECT_RX) — user bug 5.
2. **Pumping** = media-clock rate: wire cadence measured EXACTLY 122,880 ns
   /frame = clk/2^N = **48,828.125 Hz** (+1.725%), outside the playback
   servo's ±1.56% range → servo limit-cycled (trim swept −412→+510, fill
   68→351, ~4 s period). Fix = `KL_media_adv` fractional-N advance
   (`c9f0e8b`), sim-measured 48,000.000 Hz. Digital wire quality itself is
   PRISTINE: **THD+N −149.7 dB** (pw0 capture, 20k frames, 0 gaps).
3. **Second stream discovered**: the ARTY was also transmitting (Hive
   cross-connect probe-activated its talker) −132 dBFS noise into the SAME
   DMAC. Cleared via DISCONNECT_RX on the AX listener; MAAP enable is the
   structural guard (still en=0).
4. **gPTP dynamic info now live** (user bugs 1-4, `eca5510`): GM regs
   0x624/0x628 already existed (daemon-writable); NEW `GPTP_PDELAY` 0x6E4
   (RW ns) feeds GET_AVB_INFO propagation_delay; flags |0x02 when GM
   present; GET_AS_PATH is GM-aware ([GM,us] on foreign GM). Board daemon:
   milan-tests-avb `fpga/tools/gptp2csr.sh` (pmc → devmem, 5 s poll).
5. **Media-lock semantics per clock source** (USER rule, `f4eaf52`):
   internal = lock on first valid PDU (buffer position); external
   (stream/CRF) = lock gated on servo convergence (fill mid±64/100 ms,
   exit ±128; unlock on divergence). rxmon TB 69.
6. Format-change lock loss (user bug 6) DISPROVEN in fabric (TB [27]:
   relock on next matching PDU after silence-unlock) — the silicon symptom
   was controller-left mismatched formats = bug 5.

**Traps burned this session:**
- **Build launcher env — TWO requirements** (cost 4 wasted launches):
  (1) venv on PATH (`export PATH="$HOME/litex-milan/venv/bin:$PATH"`) —
  the BIOS Makefile invokes bare `python3 -m litex...crcfbigen`, so
  calling the venv python explicitly is NOT enough; (2) `source
  /home/alex/Xilinx/2026.1/Vivado/settings64.sh` — nohup/scripted envs
  have no Vivado (LiteX dies post-BIOS with "Unable to find or source
  Vivado toolchain"). Interactive shells get both from the profile,
  which is why manual runs always worked. Scratchpad `launch_ax9.sh` /
  `launch_arty9.sh` are the canonical templates. Also: `pkill -f` with a
  plain build-tag pattern kills YOUR OWN shell and any monitor whose
  command text contains the tag (exit 144) — use a bracket pattern like
  `pkill -f "output-dir.*milanfinal[9]"`.
- pw0 can NEVER see the boards' ACMP responses (fabric TX doesn't cross
  Linux tcpdump on-board; the switch doesn't relay board ACMP multicast
  uplink) — verify ACMP effects via CSRs (0x6A4/0x6B0), not pcap.
- ADP GM/AS_PATH/AVB_INFO were all correct RTL-side but nothing ever
  WROTE the GM CSRs — "displays wrong GM" class bugs are provisioning.
- STREAM_OUTPUT format ≠ wire format is a silent trap: TBs used the
  generator as oracle so declared-vs-wire divergence was invisible to
  every suite; only a format-matching controller (Hive) exposed it.

**MILANFINAL9 AX ON SILICON (later 07-18):** all 3 seeds timing-met
(eto **+0.057** = keeper, JTAG-SRAM loaded; asl +0.043, eppo +0.004);
wire cadence measured **median 125,000 ns/frame = 48,000.000 Hz PASS**
(was 122,880 / 48,828.125). Talker-truth live: GET_STREAM_FORMAT(out0)
returns the 2ch wire format; `--bind 0001 0002` matched the listener and
locked (RATE ~8.1k). **Mirror bug found by that very test**: the arty
PLAYER's nominal NCO step (0x8000) is the same clk/2^N = 48,828 Hz
architecture — vs the now-true 48k source its trim pegged **−512 with
fill 5** (floor 48,065 Hz, still +65 Hz fast → periodic underrun dumps).
Fix `10f3616`: NOM_STEP from CLK_FREQ_HZ (32212, −8 ppm, same value on
both boards). Arty milanfinal9 sweep carries it + TONE_CTRL[3:1] tone
attenuation (`fbf19eb`; the analog loopback clips the Pmod ADC at
0 dBFS — H3 within 1 dB of H1 measured). NOTE: the AX build is 2 commits
behind arty (no attenuation/player-step — AX player unused; analog
THD+N acceptance needs an AX round with attenuation or a passive pad).
**Loopback instrument**: PMOD line-out→line-in loop; arty talker in
bypass (0x654=0x3, tone OFF) streams the played audio back as sid :02 →
pw0 capture = frequency-vs-time of what the DAC actually plays (this
measured the wobble: ±1.5 % @ ~2 s period = exactly the servo clamp).
**Post-power-cycle rebuild traps:** pw0 /tmp wiped (redeploy
milan_controller.py + gptp2csr.sh), scratchpad tooling wiped (con.sh /
daemons / numpy venv), AX JTAG reload = fresh boot → console needs
`root` login + `dmesg -n 1` (kl-eth bd-stage spam buries it), and
board-side ramfs deployments are lost on the reloaded board.

**OPEN INVESTIGATION (late 07-18): ACMP LISTENER DEAF ON SILICON.**
Both boards, milanfinal8 AND 9/10, accept ~0-2 listener commands then
nothing (CC frozen; responders/AECP/ADP/streaming all fine on the same
multicast stream). Eliminated WITH EVIDENCE: switch aging (responders
answer multicast live), allmulti (MAC_CTRL=0x1B has bit3), bypass mode,
lwSRP off, entity provisioning (responder matches the same eid net),
frame length/padding (byte-exact + flood-interleave sim replays PASS),
seed dependence, synthesis pruning (1091 LUTs), RESPOND_S wedge
(milanfinal10 watchdog: WEDGE=0 while deaf). Sim CANNOT reproduce
except zero-gap back-to-back frames ([STORM] loss - real but the
quiet-network silicon test also failed, so not the whole story).
Morning CC=84 on arty-8 is best explained as Hive retry persistence
over hours, i.e. the loss has likely been chronic; the walkers sample
bare tvalid (no tready qualify - OK only if rx_axis_to_dma never
stalls; aecp shares the pattern and works). NEXT: milanfinal11 (in
flight) adds ACMPL_DBG 0x6E8 RO-live {classify_cnt, fc_cnt,
fc_flags{dst,etype,sv0,len,ovfl,lstnr_hi,lstnr_lo,is_cmd}, base_hits}
- one read after a poke says whether the walker classifies frames at
all and which accept term fails. Watchdog (b8e4613) + forensics
(c0360bb) both ride it. Audio is DOWN until a bind lands (AX streams
true 48k regardless; arty QSPI currently milanfinal10-asl).

**Open (ranked):** (a) flash milanfinal9 both boards + re-drill (cadence
125,000 ns, servo converged, la_avdecc 41/41, Milan=1 CLEAN ×2);
(b) deploy gptp2csr.sh + ptp4l pair → GM/pdelay live (clears
LATE_TIMESTAMP too); (c) lwSRP TA-propagation vs switch (listener stuck
SETTLED_NO_RSV, ~3.6k re-probes logged); (d) PCM-ring formal THD+N
(reserved-memory rebuild); (e) MAAP enable + bind-follow flow.

## 0b. BENCH SESSION 2026-07-17 (milanfinal2 silicon) — results + open items

Both boards run `*_eppo_milanfinal2` (arty: QSPI bitstream@0 REFLASHED —
survives the serial-DTR reset; AX: JTAG-SRAM, volatile). Old 2-hart QSPI
images boot fine on the 1-hart gateware (cpu1 timeout, degraded-OK).

**PASSED on silicon:** CSR identity + all 11 new registers exact ·
**MAAP live**: probe→ANNOUNCE, claim 91:E0:F0:00:9F:60, byte-perfect
announces at pw0 through the switch (fe 03 / 08 1c / cadence 3.7-4.1 s) ·
la_avdecc-style controller drill **41/41** on the new AECP · **full ACMP
listener ladder**: BIND_RX → ADP discovery → PROBE_TX → SETTLED, bound
talker = AX EID, VLAN learned · MSRP dialogue live (both engines ~109 TX /
~730 RX MRPDUs with the switch).

**FINDING 1 (product bug, caught by the new counters on first exposure):**
`aaf_talker_i2s` emits 2-ch AAF while STREAM_OUTPUT advertises the 8-ch
format ⇒ the arty monitor rejects every PDU (UNSUPPORTED_FORMAT 0x6C0
counting, FRAMES_RX 0). Fix = task #23 (framer 8-ch zero-fill), then the
tone/ring/servo acceptance completes.

**FINDING 2 (lwSRP↔switch, needs a dedicated session):** with lwSRP enabled
both sides: domain OK both; AX TalkerAdvertise declared; **TA never
registers at the arty** (0x6A4[6]=0) ⇒ bound listener declares AskingFailed
⇒ switch propagates it back to AX (0x694=0x35: lstn-reg=1, decl=asking-
failed) ⇒ no reservation, gate closed. MRP is link-local — debug needs the
switch's own MSRP view (d&b tooling) or a direct-cable peer (pw0 mrpd).
Workaround in force for streaming drills: AAF bypass=1 + VID0 (0x654=0x3).

**✅ FINAL STATE 07-17 LATE: MILAN=1 CLEAN + AUDIO LOCKED.** la_avdecc
verdict CLEAN rc=0 complaints=0 (both entities; clock-domain counters in).
Acceptance drill on milanfinal8/milanfinal7: rate nominal, servo CONVERGED
(trim +248 ≈ +0.76 % steady-state inter-board rate residual, fill
mid-range), ZERO overruns/underruns since lock, ZERO stream errors.
KEEPERS: arty asl_milanfinal8 +0.189 (QSPI-flashed), AX asl_milanfinal7
+0.040 (JTAG-SRAM). Remaining niceties: ring-dump THD+N measurement
(needs the 1-hart image/reserved-mem rebuild), lwSRP TA-propagation
session, arty/AX keeper re-unification on one tag.

**🔊 AUDIO E2E ON SILICON (07-17, after the OUT4 switch power-cycle):**
AX tone talker → switch → arty listener: **FRAMES_RX 376k PDUs / 46 s,
locked once and stayed locked, ZERO seq/format errors, PCM ring
committing, I2S serializing on the jack.** Adaptive 2-ch SET verified on
hardware. **Servo finding:** trim PEGGED at +80 (≈+1200 ppm clamp) with
fill riding the top rail (509/512) — the talker's media clock outruns the
arty's local 48 kHz by MORE than the clamp; widen the trim range
(KL_i2s_playback ±80 localparam) and/or quantify via 0x6D8 overrun rate
next session. Bench traps: the AX POWER outlet = powerstrip OUT0 (cut it
once — JTAG-SRAM lost, reload needed); switch = OUT4; AX serial login
resets provisioning after each reboot (0x654/0x6DC re-poke needed).

**SILICON FINDS 4+5 (audio-rate arc):** `d05546a` the AX framer's I2S
divider was fixed for 50 MHz — at 100 MHz it sampled 97.7 kHz while
advertising 48 k (measured 16.9k fr/s; servo pegged at BOTH clamps
chasing a 2× stream); dividers now scale with MILAN_CLK_FREQ_HZ.
`9d213a1` the playback NCO's 0x10000 nominal step carried EVERY cycle —
the divider could slow but never exceed nominal, so positive trim was a
no-op and a high FIFO could never drain; now 0x8000 half-rate nominal,
trim ±1.56 % both directions. AX keeper = asl_milanfinal7 +0.040
(rate fix); arty milanfinal8 (NCO fix) = the final acceptance build.

**FIELD FIXES from the user's Hive/la_avdecc session (post-drill):**
`a387e6b` AUDIO_CLUSTER 90→87 B (stray aes3_* tail; la_avdecc "Remaining
bytes: 3" — invisible to our TBs since the generator is their oracle) ·
`651fd4b` ACMP sink 1 (CRF) now valid-always-unbound on GET_RX_STATE
(UNKNOWN_ID for an ADVERTISED sink = la_avdecc Fatal Enumeration Error;
sink-0 state masked out of sink-1 replies) · `c6fc7c8` adaptive listener
formats (1..8ch on the base rates — the 2ch-talker rejection was correct
counting, the GAP was no way to adapt). ALL THREE ride milanfinal4
(arty sweep in flight; AX needs the same build after — its 41/41 drill
doesn't exercise these paths, Hive does).

**Bench traps:** arty serial-open DTR = board reset (QSPI reconfigures —
JTAG-SRAM images do not survive; hence the bitstream reflash); use the
persistent console daemons (scratchpad con.sh) + `dmesg -n 1`.

## 1. Topology

```
┌──────────────── dev VM (this machine) ──────────────────────────┐
│ repos + Vivado + buildroot + build tree (see §2)                │
│                                                                 │
│ USB passthrough (BY-ID ONLY, numbers shuffle on every replug):  │
│  FT232H  210512180081 = AX7101 JTAG                             │
│  CP2102N 66e0ce96...  = AX7101 console (115200)                 │
│  FT2232  210319AFEED0 = Arty JTAG (if00) + console (if01)       │
└──────┬──────────────────┬───────────────────────────────────────┘
       │ JTAG+serial      │ JTAG+serial          (VM has NO data
       ▼                  ▼                       plane; mgmt ssh
┌──────────────┐   ┌──────────────┐               to amx-pw0 only)
│ AX7101       │   │ Arty A7-100  │
│ full endstn  │   │ small endstn │
│ EID ...:01   │   │ EID ...:02   │
│ 192.168.127.1│   │ .3           │
│ 1G GMII      │   │ 100M MII     │
└──────┬───────┘   └──────┬───────┘
       │ 1G               │ 100M
     ┌─▼──────────────────▼─┐   d&b audiotechnik AVB switch
     │      AVB SWITCH      │   (OUI 3c:c0:c6, clock 3cc0c6.fffe.fe0210)
     └──────────┬───────────┘   remote power-cycle via amx-pi
                │ 1G (uplink = the only full-control-plane port)
        ┌───────▼──────┐
        │ amx-pw0 i210 │  192.168.127.2  enp6s0  68:05:ca:95:b2:d1
        │ (ssh, sudo)  │  controller drills + la_avdecc live here
        └──────────────┘
```

- **amx-pw1 is RESERVED — never touch it.** The VM never gets a
  192.168.127.x address.
- Entities: AX EID `02:00:00:ff:fe:00:00:01` (MAC 02:00:00:00:00:01),
  Arty EID `...:02` (MAC ...:02). stream_id = {station_mac, uid16} —
  byte-identical across ACMP/AECP/AVTP by construction (bug fixed 07-14).
- Switch behavior is DEFINITIVE (docs/findings/GPTP_RXPAD_ROOTCAUSE.md):
  edge ports are GM-source+pdelay BY DESIGN — boards never receive
  Sync/Announce through it; board-as-slave = direct cable only. Relay recipe
  = exactly ONE strong GM claimant (port 8, prio1 100, cc6). It forwards only
  registered AVB multicast between edge ports and INGRESS-FILTERS VLAN 2
  (hence the VID0 priority-tag policy until lwSRP/MVRP registers VLANs).
- A second session may drive the bench concurrently (attribute ptp4l deaths
  via ps before debugging "crashes").

## 2. Machine (dev VM)

Arch Linux VM, **96 vCPU / 31 GB RAM**. No data-plane NIC (rule above);
bench reach = ssh amx-pw0 (passwordless sudo) + USB serial/JTAG.

| Path | What |
|---|---|
| `~/prjs-avb-on-fpga/milan-fpga` | THIS repo: RTL (`hdl/`), testbenches (`tb/`), LiteX SoC + build system (`sw/litex/`), controller (`avdecc/`), docs |
| `~/milan-tests-avb` | kl-eth Linux driver, DTs, boot images, buildroot glue (`fpga/`) |
| `~/prjs-avb-on-fpga/fpga-ps-tools` | BSP/DT extraction tools (main AHEAD-5 UNPUSHED — user's call) |
| `~/litex-milan` | LiteX env: **venv** `~/litex-milan/venv` + **work/** = all build dirs (~525) |
| `~/br-milan-output` | buildroot output: `images/` (Image, rootfs.cpio.xz), host toolchain, linux-7.0.11 tree; rootfs overlay incl. `.../board/milan_naxriscv/rootfs_overlay/etc/init.d/S50milan` (dir name is historical — CPU is VexiiRiscv) |
| `~/refs/AX7101` | Alinx board repo clone — reference ONLY, push disabled |
| `~/Xilinx`, `~/Xilinx2` | Vivado 2026.1 ×2; **build.sh sources `~/Xilinx2/2026.1/Vivado/settings64.sh`** (has Artix-7 + Zynq-7000) |

- Build env: `source ~/Xilinx2/2026.1/Vivado/settings64.sh` +
  `export PATH=~/litex-milan/venv/bin:$PATH`; long jobs via `setsid nohup`
  with a log under `~/litex-milan/work/` (plain bg jobs die with the session).
- `rtk` proxies/dedups CLI output (token filter); for forensics read raw
  files or `rtk proxy <cmd>`.
- git identities: milan-fpga = default (hackerman-kl); milan-tests-avb
  commits use `-c user.name="Alexandre Malki" -c user.email="alexandremalki89@gmail.com"`.
- pw0 tools: `/tmp/milan_controller.py` (deployed copy of
  `avdecc/milan_controller.py` — REDEPLOY after edits),
  `~/la_avdecc_work/enum-probe` (built with la_avdecc's OWN feature defines —
  ABI trap, see §8), tcpdump, iperf3.

## 3. Boards — facts + live state (2026-07-14)

| | AX7101 | Arty A7-100T |
|---|---|---|
| FPGA | xc7a100t-2fgg484 | xc7a100t-1csg324 (slower die) |
| CPU | VexiiRiscv 2-hart @100 MHz | VexiiRiscv 2-hart @83.333 MHz |
| Milan datapath clk | 100 MHz (`--milan-clk-freq 100e6`) | 50 MHz |
| PHY | RTL8211E GMII 1G | MII 100M |
| EID / IP | ...:01 / 192.168.127.1 | ...:02 / .3 |
| Gateware NOW | `build_ax7101_eto_miltalk` WNS +0.072, **JTAG-SRAM** | `build_arty_eppo_miltick` WNS +0.381, **in QSPI** |
| QSPI (16 MB) | policy `images`: Linux images only, kernel @0 — **NEVER flash a bitstream** (kernel-clobber trap; deploy.sh refuses without FORCE_BITSTREAM_FLASH=1). Image set = hwts4-era per-board rootfs + fixed opensbi/dtb | policy `boot` (v3): bitstream @0 (4 MiB) + xz kernel @0x400000 + opensbi @0x700000 + dtb @0x760000 + rootfs @0x780000; **JP1=QSPI, fully self-hosting** |
| Power-cycle | FPGA goes BLANK → JTAG reload needed | reboots to full Milan endstation hands-free |
| Driver | kl-eth auto-loads; `kl,rsc-clk-mhz` from DT (AX 100 / Arty 50); RSC on @250 µs | same |
| Talker | AAF present but **off** (talker half idle) | **TRUE Milan mode**: S50milan writes `0x654=0x1` → silent until PROBE_TX, then 8138 fr/s AAF from the Pmod I2S2, hard stop 15 s after last probe |

Both boards: probe window 14–15 s measured, ADP cadence 31 s (×2 periods),
dormancy self-heal ≤5 s proven, controller drill 41/41, la_avdecc Milan=1
CLEAN. Bench cosmetics: AX console needs `dmesg -n 1` under talker RX;
initramfs "invalid magic" after the real unpack is benign.

**gPTP bench end-state:** reflash bounces re-triggered the switch's port
flap-suppression → the Arty's cc6 announces are not relayed uplink; pw0 is
SLAVE ~5 ns to the SWITCH HOLDOVER (3cc0c6, cc248). Arty GM itself runs
clean (txto=0). Remedy is physical: switch power-cycle (amx-pi) or direct
cable. Data plane unaffected.

**Fallback builds** (all in `~/litex-milan/work/`):

| Build | What | WNS |
|---|---|---|
| build_arty_eto_lwsrp | Arty lwSRP keeper CANDIDATE (not yet loaded; asl −0.287 fail, eppo died in route — sweep variance) | +0.121 |
| build_ax7101_*_lwsrp | ALL 3 SEEDS FAIL PLACEMENT (Place 30-487: LUTs 62408/63400 = 98.4 %). AX was ~97 % before lwSRP | — |
| build_arty_*_milanv12 | ALL 3 SEEDS FAIL PLACEMENT (66599/63400 LUTs = 105 % — the v1.2 close-out logic tipped ARTY too). **Root cause found by hierarchical synth report: aecp u_ingress = 8197 LUTs** (128-byte register fbuf with unaligned byte write decoders + replay muxes) — vs the lwSRP BRAM-FIFO ingress at 106 LUTs | — |
| build_ax7101_asl_milanv12d | **AX7101 Milan-v1.2 KEEPER** — closes at 100 MHz after area-70 round 1 (`42fdc6f`+`f018fd0`+`a6976dc`, −15.3K placed LUTs → 51284/63400 = 80.9 %, slices 97.6 %); all 3 seeds ≥ +0.023 (eto +0.082, eppo +0.023). NOT loaded | +0.123 |
| build_arty_eppo_milanv12d | **Arty Milan-v1.2 KEEPER** — area-fixed netlist, all 3 seeds close (asl +0.117, eto +0.022), LUTs 51306 = 80.9 % (supersedes eppo_milanv12b +0.001). NOT loaded | +0.154 |
| build_arty_*_milanv12e | **DO NOT USE** — csr shadow-RAM regressed it: 2 if-arm writes inferred 2 write ports → Synth 8-6849 BRAM-infeasible → +704 LUTRAM, LUTs 51542-69 = 81.3 %, best eppo +0.077. Fix `95a82f7` (single muxed write port → RAMB18 SDP). **Rule: grep new builds for 8-6849** | +0.077 |
| build_arty_asl_milanv12f | **Arty Milan-v1.2 KEEPER (supersedes eppo_milanv12d)** — csr shadow in BRAM (`16fe234`+`95a82f7`): LUTs 50720 = 80.0 % (−586 vs v12d), slices 96.9 %, 8-6849 clean; all 3 seeds close (eto +0.126, eppo +0.094 @ slices 96.3 %). NOT loaded | +0.174 |
| build_ax7101_asl_milanv12f | **AX7101 Milan-v1.2 KEEPER (RTL-current, supersedes asl_milanv12d)** — same shadow-BRAM netlist: LUTs 50723 = 80.0 % (−561 vs v12d), slices 97.7 %, 8-6849 clean; all 3 seeds close (eto +0.011, eppo +0.001 — thin, sweep variance; v12d asl +0.123 remains the higher-margin fallback on the pre-shadow RTL). NOT loaded | +0.076 |
| build_arty_eto_rxmon | Arty rxmon fallback — AVTP-RX monitor netlist (`832aa19`): LUTs 51630 = 81.4 %, all 3 close (asl +0.118, eppo +0.068); +0.396 = best margin ever on this design. NOT loaded | +0.396 |
| build_ax7101_eto_rxmon | AX rxmon fallback — same netlist: eto closes thin (eppo −0.050 / asl −0.088 FAIL; slices 97.6 % = space-bound; USER 07-17 authorized --l2-bytes 32768 when space-bound). NOT loaded | +0.027 |
| build_arty_eppo_pcmring2 | Arty 2-hart fallback — + AAF RX depacketizer + PCM ring (`e8efecc`+`53042cc`+hold_r-64b fix): LUTs 51860 = 81.8 %, slices 98.4 %; all 3 close (eto +0.087, asl +0.069). Traps: pcmring(1) sweep died on Vivado 8-524 out-of-range part-select in the unrolled hold_r byte mux — Verilator/yosys tolerated it; only Vivado is the Vivado oracle. NOT loaded | +0.162 |
| build_ax7101_eto_pcm1h | **AX KEEPER (RTL-current, 1-HART — USER 07-17 "keep 1 hart for now")** — same PCM-ring netlist, `--cpu-count 1`: LUTs 45545 = 71.8 % (−6.2K vs 2-hart), slices 95.8 %; ALL 3 close (eppo +0.069, asl +0.041) where 2-hart was 2/3 FAIL. L2 kept 64 KB (32 KB authorization unused). ⚠ 1-hart dtb pairs with this bitstream; 2-hart NAPI perf records don't apply. NOT loaded | +0.127 |
| build_arty_asl_pcm1h | Arty 1-hart fallback (pre-MAAP) — LUTs 45206 = 71.3 %; all 3 close (eppo +0.313, eto +0.088). NOT loaded | +0.386 |
| build_arty_asl_milanfull2 | **Arty KEEPER (RTL-current, 1-hart, FULL feature set)** — + MAAP, I2S playback, SET-replays, pilot tone (`668c179`): LUTs 46489 = 73.3 %; all 3 close (eppo +0.072, eto +0.048). E2E audio acceptance ready: TONE_CTRL 0x6DC + pcm_ring_dump + tone_thdn.py (digital −149.9 dB vs −120 limit). NOT loaded | +0.240 |
| build_ax7101_asl_milanfull2 | AX full-feature fallback (pre-0x4B/servo) — LUTs 46805 = 73.8 %; all 3 close (eppo +0.149, eto +0.029). NOT loaded | +0.172 |
| build_arty_eto_milanfinal | Arty complete-end-station fallback (pre cum-pipeline) — LUTs 47010 = 74.2 %; all 3 close (asl +0.267, eppo +0.183). ⚠ its netlist carries the 15-term cum chain: fine at 50 MHz, NEVER port to 100 MHz | +0.334 |
| build_ax7101_*_milanfinal | **DO NOT USE** — the segment-growth 15-term single-cycle cum chain = WNS −5.64/−5.88 at 100 MHz (hidden by arty's 20 ns period; found via report_timing on the failed seed). Fix `b99d56c` = 4-segs/cycle ×4 pipeline | −5.64 |
| build_ax7101_eppo_milanfinal2 | **AX KEEPER (COMPLETE end-station, cum-pipelined)** — LUTs 47239 = 74.5 %; ALL 3 close (eto +0.066, asl +0.042). THE AX bench bitstream. NOT loaded | +0.076 |
| build_arty_eppo_milanfinal2 | **Arty KEEPER (COMPLETE end-station, RTL-identical to the AX keeper)** — LUTs 46924 = 74.0 %; ALL 3 close (asl +0.077, eto +0.068). THE Arty bench bitstream (QSPI-flashable, v3.1 flow). NOT loaded | +0.143 |
| build_arty_eppo_miltick | Arty KEEPER (param-fixed tick, flashed) | +0.381 |
| build_ax7101_eto_miltalk | AX KEEPER (talker SM; eppo/asl failed — sweep variance) | +0.072 |
| build_arty_asl_adpfix | Arty pre-talker fallback (dormancy fix) | +0.243 |
| build_ax7101_asl_adpfix | AX pre-talker fallback | +0.158 |
| build_ax7101_eto_hwts_ax2 / arty asl_hwts5 | HW-timestamp keepers | +0.118 / — |
| build_ax7101_eto_acmp2 | first Milan=1 CLEAN control plane | +0.096 |
| build_arty_asl_arty_v8 | first Arty AVDECC stack (probes stripped) | +0.312 |
| build_ax7101_adp2 / build_arty_v7 | AECP-less / probes-only floors | +0.102 / +0.018 |

**Branches (all pushed unless noted):** milan-fpga `milan-arty-bringup` =
b19287e local (the working line, this doc; push on request); `main` = f51a27b (PR #12 AECP/AEM
merged). milan-tests-avb `milan-avb-stabilizing-milan` = c03c139.
fpga-ps-tools main ahead-5 unpushed. Never commit `graphify-out/`/.gitprep.

## 4. What works on silicon today (and how it was proven)

| Feature | State | Proof / normative doc |
|---|---|---|
| ADP advertise + depart + **dormancy self-re-arm** | DONE both boards | drill 0x00020001→0x00020101 ≤5 s; `docs/findings/ADP_DORMANCY.md` |
| AECP/AEM Milan entity (5 descriptors, getters/setters, LOCK, MVU, COUNTERS, AS_PATH) | DONE | la_avdecc Milan=1 CLEAN; `hdl/aecp/doc/atdecc_architecture.drawio` |
| AECP streaming cmds (GET/SET_STREAM_INFO Milan semantics, START/STOP=NOT_SUPPORTED, **real unsolicited** 4-slot engine) | DONE | 121-check TB + drill §7/7b; `docs/design/MILAN_TALKER_SM.md` |
| ACMP Milan talker SM (CONNECT_TX==PROBE_TX, 15 s window, near-stateless) | DONE | 71-check TB + wire probe→stream→expiry; same doc |
| AAF talker (48 kHz I2S2 → class-A frames, probe-gated, VID0) | DONE | 8138 fr/s, seq+1/122 µs; `docs/design/MVP_TALKER.md` |
| gPTP PHC + **HW timestamps** | DONE both boards | pdelay 1.3 µs, pw0 rms 2–5 ns through floods; `docs/findings/PTP_TS_METADATA_FIX.md`, `GPTP_RXPAD_ROOTCAUSE.md` |
| QSPI v3 self-hosted boot (Arty) | DONE | flash→login hands-free; `docs/integration/QSPI_FLASHBOOT.md` |
| TCP perf (separate perf-lineage gateware) | TX >500, RX 316 practical ceiling | `docs/findings/PERFORMANCE_GOAL.md` |
| Portability | XPM-free HDL; Yosys/sv2v 22/22 tops (ECP5 check) | `syn/yosys/run.sh` |
| **lwSRP fabric engine** (MSRP talker-adv + domain + **Listener attr declare**, MVRP, both-side registrars, 75 % bw gate → CBS slope + TX gate + listener_observed) | **RTL+TB DONE `b19287e`+07-15; silicon vs switch/pw0 PENDING** | 445+96+36-check TBs; `docs/LWSRP_FPGA_ARCHITECTURE.md` |
| **AEM/AECP Milan v1.2 mandatory set** (full 34-descriptor ROM FR-ENUM-02, SET/GET_CLOCK_SOURCE, CONTROL IDENTIFY → LED, GET_AUDIO_MAP, MVU SYSTEM_UNIQUE_ID + MEDIA_CLOCK_REF_INFO, live GET_COUNTERS, MAX_TRANSIT_TIME 0x4C/4D, STREAM_INPUT stream-info/format/start-stop) | **RTL+TB DONE 07-15; silicon re-cert PENDING** | aecp TB 345; `hdl/aecp/doc/README.md` |
| **ACMP listener SM** (BIND_RX/UNBIND_RX/GET_RX_STATE + probe ladder + SRP binding via lwSRP TA registrar; CSR 0x6A4 RO group) | **RTL+TB DONE 07-15; silicon vs a real talker PENDING** | acmp_lstn TB 89; pipewire acmp-milan-v12.c contract |

Regression: 25 Verilator harnesses under `tb/verilator/<name>/` (latest
counts: acmp 71, acmp_lstn 89, aecp 345, milan_dp 53, csr 98, lwsrp_tx 445,
lwsrp_rx 96, lwsrp 36, cls 200024) + Yosys 22/22. PLUS the behave BDD tier
(`tests/`, 8 features / 57 scenarios green — run
`~/litex-milan/venv/bin/behave tests`): two 2026-07-15 `@tsn_gen` features
drive the tsn-gen packet_gen binary (the AM65x-validation recipe) — seeded
frame generation, bit-exact field patches cross-checked via `--decode`,
Milan semantic models for SET_CLOCK_SOURCE/IDENTIFY + the ACMP listener SM,
the tsn-gen CDL+8 deviation pinned, and a repo-carried ACMPDU YAML
(`tests/protocols/acmp/`).
`docs/testing/RUNNING_TESTS.md` / `PROTOCOL_VALIDATION_MATRIX.md`.

**The reference that decides Milan semantics:** pipewire module-avb
(`acmp-milan-v12.c` etc.) — ALWAYS extract the contract from it before
writing RTL; it overturned every assumption (probe model, count=0,
DISCONNECT no-op, stream_id formula).

## 5. CSR quickref (milan_csr AXI-Lite @ **0x90000000**, both boards)

Full map: `docs/reference/REGISTER_MAP.md`. The ones you touch on the bench:

| Offset | Reg | Notes |
|---|---|---|
| 0x100 | MAC_CTRL | bit3 allmulti (`ip link set eth0 allmulticast on` — reboot reverts) |
| 0x400+q*0x20 | CBS q0-3 | +0 idle +4 hi +8 lo +C en; reset en=0. Shaper is NEVER removed (user rule) |
| 0x520 | A_PTP_CMD | PHC discipline strobes (0x500 group = INCR/ADJ hooks) |
| 0x600 | ADP_CTRL | 0x1F01 = enabled, valid_time 31; 0x1F00 = silence (single-entity drills) |
| 0x604.. | identity | programmed by `avdecc/aecp_csr_setup.sh` (caps 0x8588) |
| 0x640 | ADP_CMD | bit1 = depart strobe (nothing in SW writes it — see dormancy forensics) |
| 0x644 | ADP_STATUS | available_index; healthy = +1 per 31 s (measure ≥2 periods) |
| 0x648/0x64C | AECP cmd/resp counters | balanced ⇒ no responder mid-frame |
| 0x650 | ACMP counters | |
| 0x654 | AAF_CTRL | {vid[27:16], bypass[1], enable[0]}; reset 0x0002_0002 (VID 2, bypass on). S50milan → 0x1 = TRUE Milan mode (probe-gated, VID0); legacy always-on = `devmem 0x90000654 32 0x3` |
| 0x658/0x65C | AAF DMAC | 0x660 frames / 0x664 pairs counters |
| 0x668 | A_ADP_DIAG RO | {[17:16] last depart src, [15:8] rearm_cnt, [7:0] depart_cnt} |
| 0x66C | A_ACMP_TALKER RO | {bit3 aaf_gate, bit2 lobs, bit1 talker_active, bit0 probe_armed} |
| 0x670 | A_ACMP_LOBS RW | bit0 = listener_observed (manual); with lwSRP on, effective lobs = this OR SRP listener-ready |
| 0x680 | LWSRP_CTRL | {qidx[3:2] (reset q3), talker[1], enable[0]}; reset 0xC = **disabled** (zero behavior change) |
| 0x684–0x690 | LWSRP VID/DMAC/TSPEC | VID (reset 2), stream DMAC, {interval[31:16], max_frame[15:0]} |
| 0x694 | LWSRP_STATUS RO | drops/tfail+code/slope_en/gate/over_limit/active/domain_ok/declared/ready/reg/decl — see REGISTER_MAP |
| 0x698/0x69C/0x6A0 | LWSRP slope/cnt/latency | granted idleSlope bps RO; {rx_pdus[31:16], tx_count[15:0]}; accum latency |
| 0x6A4–0x6B4 | ACMPL_* RO | listener SM: state[2:0]/bound/active/declared/ta_reg/ta_fail/status/probing/tk_avail/vlan · talker EID lo/hi · {probes,cmds} · {fail_code, tuid} |

NIC ring/perf/debug CSRs live in the LiteX region (0xf0003xxx ring/steer,
0xf0004xxx probes) — perf-era docs in `docs/findings/`. devmem trap: 64-bit
CSRs read high-word-first.

## 6. Operating recipes

```sh
# Consoles (tmux; litex_term needs the venv path)
tmux new-session -d -s milan_qspi_boot \
  "~/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_66e0ce968c16f011808241adb887153e-if00-port0 --speed 115200"
tmux new-session -d -s arty_console \
  "~/litex-milan/venv/bin/litex_term /dev/serial/by-id/usb-Digilent_Digilent_USB_Device_210319AFEED0-if01-port0 --speed 115200"
# scripted console exec: send-keys + sentinel; grep '^MARKER' (line-anchored,
# else it matches the echoed command). Board busybox has NO timeout/pgrep.

# JTAG loads (SRAM)
openFPGALoader --ftdi-serial 210512180081 -c ft232    <ax7101.bit>
openFPGALoader --ftdi-serial 210319AFEED0 -c digilent <arty.bit>
# Arty: reconfigure from QSPI without power touch:
openFPGALoader --ftdi-serial 210319AFEED0 -c digilent --reset

# Builds (sw/litex/build.sh; docs/integration/BUILDING.md)
./sw/litex/build.sh ax7101 --sweep      # 3-directive place sweep, keep best WNS
./sw/litex/build.sh arty   --sweep
# Flash (policy-aware; board_facts in build.sh):
KERNEL=~/br-milan-output/images/Image ROOTFS=~/br-milan-output/images/rootfs.cpio.xz \
DTB=~/milan-tests-avb/fpga/dts/milan_arty_vexii.dtb OPENSBI=~/milan-tests-avb/fpga/boot/opensbi_arty.bin \
PYTHON=~/litex-milan/venv/bin/python3 ./sw/litex/build.sh flash arty:<builddir>

# Milan validation drill (from pw0: ssh amx-pw0)
sudo python3 /tmp/milan_controller.py enp6s0 --eid 01   # AX   -> 41 pass, 0 fail
sudo python3 /tmp/milan_controller.py enp6s0 --eid 02   # Arty -> 41 pass, 0 fail
sudo ~/la_avdecc_work/enum-probe enp6s0 40              # Milan=1, verdict CLEAN
# enum-probe exits at its FIRST clean enumeration -> for a single-entity
# verdict, silence the other board first: devmem 0x90000600 32 0x1F00 (restore 0x1F01)

# ADP census — MUST filter, AVTP shares ethertype 0x22F0 (the arty's 8.1k fr/s
# AAF stream otherwise reads as an ADP flood / drowns :01):
sudo timeout 45 tcpdump -i enp6s0 'ether proto 0x22f0 and ether[14] = 0xfa'

# Probe the talker from pw0 (what activates the arty's stream):
#   milan_controller.py section 9 does it; window = 15 s after the last probe.

# Recovery one-liners (board console)
devmem 0x90000600 32 0x1F00; devmem 0x90000600 32 0x1F01   # ADP re-arm (pre-fix gw only)
dmesg -n 1                                                  # unbury console under RX
ip link set eth0 allmulticast on                            # gPTP RX (reverts on reboot)

# gPTP direct-cable session (Arty-as-slave validation, physical cable move):
sw/litex/gptp_direct_cable.sh   # AX=GM cc6/prio100; gates: SLAVE+rms, pdelay ~1-3us, txto=0
```

## 7. The rules (each one was paid for)

**USB / cables**
1. Serial consoles by `/dev/serial/by-id/` only, never ttyUSBn.
2. Every openFPGALoader call carries `--ftdi-serial` (two FTDI cables; a
   flash op on the wrong board is destructive).
3. VM USB passthrough is pinned by vendor:product (0403:6014, 0403:6010,
   10c4:ea60); a replug without the rule silently drops the device.

**Network / measurement**
4. amx-pw1 RESERVED; VM never gets a .127.x address.
5. Ghost-peer check before trusting any number: board `ip neigh | grep 127.2`
   must show `68:05:ca:95:b2:d1`.
6. A gate number is only valid with its FULL cell recipe; A/B in-session on
   the same cell (the cbsf_epo "TX regression" was a phantom baseline).
7. **Cadence claims need ≥2 periods** (the adpfix "31 s measured" was a
   single-period coin flip that hid the CLK-param gap for a day). ADP capture
   windows ≥70 s.
8. Measure, don't assume: no lever before its HW counter exists; decompose
   the symptom; measure before AND after (`docs/findings/` is full of
   refuted-plausible stories). OOC-synth a module before believing a
   hierarchical utilization line; read the LAST (physopt) timing summary.
9. Busybox `timeout` doesn't exist on the boards — a piped
   `timeout N tcpdump` dies instantly and fakes an empty capture.

**Pairing (LETHAL class)**
10. Driver `hs_pgsz` MUST equal gateware `--hs-page-bytes` (DMA overrun =
    panic). Capability CSR @0xf000311c + probe-check guard new pairs.
11. Ship gateware folds the legacy byte-ring; `bd=0` drivers park with
    counted drops. Arty driver domain = 50 MHz (DT `kl,rsc-clk-mhz` now
    carries it — zero-override boots).

**Flash policies (16 MB QSPI each; `board_facts` in sw/litex/build.sh)**
12. AX7101 = `images`: kernel at offset 0, NEVER flash a bitstream
    (deploy.sh refuses without FORCE_BITSTREAM_FLASH=1). Gateware JTAG-SRAM;
    power-cycle blanks the FPGA.
13. Arty = `boot` (v3): bitstream @0 + image set at shifted offsets; JP1=QSPI
    self-hosting. `build.sh flash arty:<dir>` does both stages + verify;
    sweep dirs get their layout reconstructed from soc.h.
14. OpenSBI is BOARD-SPECIFIC and EMBEDS a DTB (FW_FDT_PATH bypasses the
    flashed dtb slot). Build per board via build_opensbi.sh env; ALWAYS from
    a clean build dir (warm-tree rebuilds embedded the previous board's dtb —
    panic@0.000000; script force-cleans now).

**Builds**
15. 32 Vivado threads per build (hard cap), max 3 parallel on the 96-core
    box (USER RULE: saturate it — important configs = 3-seed sweeps, keep
    best WNS), launches staggered 90 s, always setsid.
16. Gate: WNS ≥ 0 (QSPI corrupted below +0.03 at 112.5 MHz once). Arty die
    is -1: sys 83.333 + datapath 50 is the closing clocking.
17. Elaborate WITHOUT --build first (~2 min) before burning 40 min of P&R.
    After scripted SV edits: grep the result AND read synth warnings —
    an undriven data input is silicon-silent (o_ptp_now trap; milan_dp TB
    now runs -Werror-UNDRIVEN).

**Repo / HDL**
18. Commits: ONE short line, no attribution trailers, both repos.
19. New HDL is ALWAYS SystemVerilog; Python only for soft-CPU SoC plumbing
    (USER RULE).
20. The CBS traffic shaper is never REMOVED from a build (USER RULE);
    bit-exact internal optimization is allowed.
21. Workstreams on separate branches; main receives merges. Push only on
    request.

## 8. Traps index (verified, still-live)

- **la_avdecc enum-probe ABI**: build against the lib's own feature defines
  (CBR/JSON/REDUNDANCY/STRICT_2018 + nlohmann) or the vtable mismatches and
  it SIGSEGVs on the first virtual call.
- available_index must +1 on EVERY ADPDU (bump-on-change reads as
  offline/online cycling to la_avdecc).
- ADP entity_id sits at wire byte 18 (not 16); ADP census filter
  `ether[14] = 0xfa`; CDL = frame_len − 26 (tsn-gen's model is WRONG).
- VID0 policy: stream_vlan_id legitimately reads 0 in ACMP/AECP responses —
  never assert vlan≠0 in drills; assert dmac≠0 + ACMP/AECP vlan consistency.
- Milan windows: poll at 0.2 s when measuring the 15 s probe window (1 s
  polls race the expiry and read short).
- kl-eth multicast RX: kl_set_rx_mode ignores mc groups — standalone ptp4l
  is DEAF without allmulti; reboot reverts it (proper fix = open task).
- Switch: multi-GM-claimant makes it announce-SILENT everywhere; one strong
  claimant only. Port flap-suppression from reflash bounces needs a physical
  remedy (power-cycle via amx-pi).
- LiteX `Instance(...)`: parameters are only passed if you pass them —
  `p_MILAN_CLK_FREQ_HZ` was silently defaulted for a week (2 s ticks).
  Grep the generated verilog for every new p_/i_/o_ hookup.
- iperf3/console orchestration: one-off servers (`-s -1`), fresh ports per
  cell, unique grep tags, `ssh -n` inside while-read loops.
- QSPI images from sweep dirs: `layout_from_soch.py` reconstructs the
  manifest (soc.h is the source of truth).
- Canonical Arty images: `br-milan-output/images/rootfs.cpio.xz` (Jul-13
  turnkey). `boot/rootfs.cpio.gz` is a STALE Jul-5 copy without S50milan.

## 9. Tasks

### Closed arcs (chronological; proof in §4)
M-A1..A5 bring-up → perf campaign (TX>500/RX 316, every remaining lever
measured-refuted) → area-70 phase 1 (CBS slope engine −8K LUTs) → de-Xilinx
track 1 (XPM-free + Yosys) → QSPI v3 flashboot → ADP advertiser → AECP/AEM
entity (Milan=1) → ACMP stateless responder → gPTP Phase A (PHC) + Phase B
(HW timestamps, rms 2–5 ns) → MVP AAF talker → ADP dormancy fix → Milan
talker SM (ACMP PROBE_TX + AECP streaming + unsolicited), both boards
Milan=1 CLEAN → lwSRP fabric engine `b19287e` → **Milan v1.2 mandatory-set
close-out 2026-07-15: full 34-descriptor AEM ROM + every mandatory AEM/MVU
command + live counters + ACMP LISTENER SM with lwSRP SRP-binding**
(silicon validation = open task #1).

### Open, ranked (next work; 1–3 are the USER-directed rev-2 order)
1. **Silicon validation of the 07-14/07-15 arcs** (one bench session):
   (a) lwSRP vs the AVB switch registration DB + a real SRP peer (pw0
   module-avb or OpenAvnu mrpd): STATUS 0x694 declared→ready→active,
   granted slope @0x698, Ready withdraw closes the gate ≤600 ms, MVRP gets
   VLAN 2 registered (retires VID0 — verify switch ingress filter first).
   (b) AECP re-cert: milan_controller drill + la_avdecc enum (rebuild
   enum-probe — ~/la_avdecc_work is GONE from the VM) against the full
   descriptor ROM; aecp_csr_setup.sh now writes caps 0xC588 (identify bit
   is BACK — CONTROL[0] exists); Hive identify → user_led0.
   (c) ACMP listener: BIND_RX from pw0 controller → board probes the AX
   talker → SETTLED_RSV_OK with real SRP; CSR 0x6A4 state walk.
   Mind: with LWSRP_CTRL[0]=1 and no listener Ready, the talker stays
   silent BY DESIGN. TCAM explicit entries for 01:80:C2:00:00:0E/21
   (default-pass covers today).
2. **pw0 PipeWire listener (BIND_RX)** — module-avb listener against the
   arty talker = the audible end-to-end; then media clock recovery (NCO from
   gPTP) per `docs/design/MVP_TALKER.md`. Natural pairing with #1.
3. **Listener media path — IMPLEMENTATION COMPLETE 07-17** (this entry kept
   for lineage; see the keeper table + audio-e2e-tone memory): monitor with
   ALL Table 7-156 counters real (incl. LATE/EARLY/MEDIA_RESET via the
   playback NCO servo, trim @0x6E0), depacketizer -> PCM ring + I2S DAC
   playback, pilot tone acceptance path. Control plane (ACMP listener SM) + diagnostics
   (AVTP-RX monitor 07-17) + **fabric/SoC media plumbing DONE 07-17
   (`e8efecc`)**: KL_aaf_rx_depacketizer (hdl/avtp) strips 38/42-byte
   headers off monitor-accepted PDUs and streams full-word S32BE payload
   out m_axis_pcm into a WishboneDMAWriter loop-mode DRAM ring
   (milan_dma_pcm_* CSRs @0xf0003120, additions-only; offset = wr pointer;
   tlast NOT forwarded — the TS-ring phase-B trap). CSR 0x6C4 pdus/drops +
   0x6C8 last avtp_ts (media-clock hook). milan_dp proves BIND->AAF->
   byte-exact 64B payload (untagged rotate-2 AND tagged rotate-6) + reject
   isolation. REMAINS: the Linux/PipeWire consumer (mmap the ring, chase
   offset — bench), CRF clock recovery + dynamic audio maps.
4. **gPTP direct-cable session** — Arty-as-slave validation; script ready
   (`sw/litex/gptp_direct_cable.sh`), needs the physical cable move.
5. **Switch power-cycle via amx-pi** — clear flap suppression, restore the
   Arty-GM→pw0 relay.
6. **kl-eth set_rx_mode** — honor mc groups (allmulti workaround reverts
   every reboot).
7. **is_1g CBS slopes on the Arty** — true class-A shaping at 100M (today
   the talker injects post-shaper, unshaped).
8. **One-opensbi durable form** — BIOS passes a1=dtb, platform reads
   timebase from FDT (removes the per-board opensbi class).
9. **Priority TX ring / doorbell in kl-eth** — the gPTP TX-flood delay is
   the single 256-slot TX ring.
10. **Area-70 continuation** (USER directive 07-15: back below ~70 %,
    config-in-RAM approach). **ROUND 1 EXECUTED 07-15 late** (yosys LC
    before/after): aecp ingress 8.2K→0.1K (`42fdc6f`) · acmp responder
    4647→498 + listener 4860→1127 (`f018fd0`) · aecp builder buf_r
    3865→3018 (`a6976dc`) ≈ **−17K banked**, all byte-exact-gated.
    Recipe: beat-aligned word writes → distributed RAM, fixed-lane
    register captures for decode fields, per-beat lane overrides at
    emit (async LUTRAM reads = zero FSM change). REMAINING:
    (a) milan_csr 2348 LCs — read-shadow RAM (CAREFUL: shadow must
    store the READBACK value, masked fields/W1C differ from wdata);
    (b) byte-ring fold (rule-11 pairing checklist); (c) walker shared
    subtractor + control sets + accessor dir → RAM. Quantifying
    arty/AX resweep pends on build slots (AX round-2 occupying).
    CBS shaper NEVER removed. Success = arty WNS ≥ +0.1 and AX closing
    100 MHz with margin.
11. **Perf follow-ups** (perf lineage): ~220-vs-525 cell-recipe gap, TX
    mid-flow stall, AF_XDP ZC (the RX>500 lane).
12. **Arty listener half — media** (AAF RX sink/I2S out/CRF): the control
    plane (descriptors, ACMP listener SM, SRP binding) landed 07-15; the
    audio path is what remains.
13. **AECP deferred (small tail)**: NV persistence of SET_* (volatile
    mirror today), GET_DYNAMIC_INFO 0x4B (SHOULD), dynamic audio-map edits
    (ADD/REMOVE — static maps shipped), MAAP dynamic allocation,
    unsolicited pushes for clock/control changes. **DONE 07-17:
    STREAM_INPUT counters** — KL_avtp_rx_monitor (hdl/1722) on the RX tap
    matched to the ACMP-listener bound sid: valid=0xF3F live (lock/settle/
    mismatch/interrupt/100ms-unlock/format-compare per the pipewire
    stream.c contract), GET_COUNTERS(in0/in1) full-size, unsolicited
    counters push 1/s, CSR 0x6B8-0x6C0, 26 suites + yosys 23/23.
    MEDIA_RESET/LATE/EARLY advertised-zero (= reference; land with the
    media path / media clock).
14. fpga-ps-tools: push main (ahead-5) — user's call.

### Doc index (normative first)
`docs/design/ARCHITECTURE_HW_SW_SPLIT.md` (rev 2 split) ·
`docs/design/MILAN_TALKER_SM.md` (talker contract + SM) ·
`docs/LWSRP_FPGA_ARCHITECTURE.md` (lwSRP as-built; CSR 0x680 map) ·
`docs/design/MVP_TALKER.md` · `docs/overview/FULL_FPGA_SOLUTION.md` ·
`docs/reference/REGISTER_MAP.md` · `docs/integration/BUILDING.md` ·
`docs/integration/QSPI_FLASHBOOT.md` · `docs/testing/RUNNING_TESTS.md` ·
`docs/testing/PROTOCOL_VALIDATION_MATRIX.md` · findings:
`ADP_DORMANCY.md`, `GPTP_RXPAD_ROOTCAUSE.md`, `PTP_TS_METADATA_FIX.md`,
`PERFORMANCE_GOAL.md` (perf lineage), `SESSION_HANDOFF.md` (historical).

### History anchors (git, newest first)
`2d700ec` AECP Milan v1.2 mandatory-set close-out (34-descriptor ROM + all
mandatory commands) ·
`b19287e` lwSRP fabric engine (hdl/lwsrp ×9, CSR 0x680, 3 TB suites) ·
`3fce652` miltick close-out (window 15 s exact, cadence 31 s ×2, 41/41,
Milan=1) · `c3b0e82` MILAN_CLK_FREQ_HZ never passed — plumbed ·
`165d57c` talker SM RTL · `ba76908` ADP dormancy self-re-arm + DIAG ·
PR #12 AECP/AEM merge (`f51a27b`).

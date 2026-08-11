# HANDOVER 08-01 — the fit endgame + flash-ready software + harness truth fixes

Continues [HANDOVER_0731.md](HANDOVER_0731.md). DUT = ALINX AX7101 ONLY (Arty retired by USER).
Shape fixed by USER: 8 talkers + 8 listeners, 8ch/stream, RV32 VexiiRiscv.

## Contents

- **[1. The fit (task #51) — where it stands](#1-the-fit-task-51--where-it-stands)** — how much of the device the design occupies and what the remaining pressure is
- **[2. csr round CLOSED-REFUTED (the fifth same-class refutation)](#2-csr-round-closed-refuted-the-fifth-same-class-refutation)** — a suspected register defect investigated and cleared, for the fifth time in its class
- **[3. Flash inputs — ALL READY except the bitstream (verified)](#3-flash-inputs--all-ready-except-the-bitstream-verified)** — everything a flash needs, and the one input that was still missing
- **[4. Harness truth fixes (both committed, pushed where remotes exist, DEPLOYED to pw0)](#4-harness-truth-fixes-both-committed-pushed-where-remotes-exist-deployed-to-pw0)** — corrections to the test harness itself, where it had been reporting something other than what happened
- **[5. Campaign triage (torture-ax-postoutage.jsonl on pw0, STILL RUNNING vs 0x0016)](#5-campaign-triage-torture-ax-postoutagejsonl-on-pw0-still-running-vs-0x0016)** — the running soak campaign and what its failures were traced to
- **[6. Open (unchanged priorities)](#6-open-unchanged-priorities)** — what was still unfinished when this session ended

## 1. The fit (task #51) — where it stands

All numbers are `Place 30-487` "require/available slices" unless noted.

| build (work/) | directive | verdict |
|---|---|---|
| build_ax7101_x32expl | plain rv32 flow floor | 11,339 vs 11,162 = 177 short |
| build_ax7101_x32lean_asl / _eto | AltSpreadLogic_high / ExtraTimingOpt + lean CPU | **15 short** (11,196/11,181) |
| build_ax7101_x32lean (eppo) | ExtraPostPlacementOpt | passed place, routing-refuted (18,532 residual overlaps) |
| build_ax7101_x32lean_end | ExtraNetDelay_high | **ONLY seed to pass placement**; routing iter-2, overlaps 92,161→52,462→35,376→26,652, still descending |
| build_ax7101_x32csr | csr LUTRAM trim + asl | 106 short — WORSE, see §2 |
| build_ax7101_x32lean_aslm / _ebp / _expl | AltSpreadLogic_medium / EarlyBlockPlacement / Explore | LAUNCHED 08-01 (directive lottery, 4×32 full house) |

Lean CPU tuning = `--lsu-l1-refill-count=2 --l2-down-pending=4
--l2-general-slots=8`, L2 16K, AreaOptimized_high + ExploreArea. The full
launch command is recoverable from any `build_*_x32lean_*.launch.log` or
`/proc/<pid>/cmdline` of a live build. TRAP: launching several seeds
simultaneously races sbt on the SHARED VexiiRiscv dir — the loser dies in
`generate_netlist` (expl did; relaunch solo, the netlist cache then serves).

## 2. csr round CLOSED-REFUTED (the fifth same-class refutation)

Agent's measured result: OOC 2500→2200 (−300 LUT, real and behaviour-identical,
bite-proven both ways) yet the FIT got WORSE: baseline gains +107 LUT of
synth→place LUT-combining, the LUTRAM version LOSES 535 (RAMD32 occupies
SLICEM, cannot combine; design already 15% SLICEM). **The fit is
PACKING/LUT-COMBINING-bound, not LUT-count-bound — LUT trims in csr-land are
the wrong currency.** RTL reverted (30c4e949) keeping the new SNAP-walk wipe
test (a genuine pre-existing coverage hole; passes on original RTL).

## 3. Flash inputs — ALL READY except the bitstream (verified)

- `br-milan-rv32/images/Image.xz` 2,409,444 B (slot 3 MiB) and
  `rootfs.cpio.xz` 7,715,920 B (slot 7,733,248 B — **17 KB slack**), xz per
  flash_verify.sh (1 stream/1 block/CRC32).
- Overlay ring blobs (`pcm_ring_dump`, `pw-milan-ring-source`) rebuilt rv32 +
  STRIPPED (unstripped was 75 KB over slot); zero 64-bit ELFs in the final
  cpio; gptp2csr.sh 16,054 B present. rv64 originals in
  `board/milan_naxriscv/rv64-archive/` — **SHARED overlay: restore them
  before any rv64 rebuild**. milan-tests-avb commit d346b8a.
- `fpga/boot/opensbi_ax_vexii_rv32.bin` (07-31 20:24) embeds the rv32 DTB
  WITH the PCM node (audio@f0003120 + pcmring) — the stale-dtb foot-gun does
  NOT apply to the rv32 path.
- Sequence on a fitting bitstream: full image set (1→2 RXQ window shift),
  `AX_FTDI=210512180081 ./sw/litex/build.sh flash ax7101:<dir>`, cold cycle
  via `ssh the bench host 'powerstrip off 0; sleep 6; powerstrip on 0'`, verify
  `devmem 0x90000004` == 0x00010021 and a 32-bit boot, then the campaign.

## 4. Harness truth fixes (both committed, pushed where remotes exist, DEPLOYED to pw0)

- `xside.unlicensed-silent-everywhere` now SKIPs when NO device side is
  readable (wire-only movers are the test host's own traffic) —
  milan-fpga 1ac6d490, bite-proven against HEAD.
- `instrument.test-machine-lossless` no longer counts `rx_dropped` as
  instrument loss: measured live, the switch's MVRP heartbeat (1/s,
  0x88f5 → 01:80:C2:00:00:21, no handler on pw0) ticks rx_dropped ~0.1/s =
  "+2 per window", which had poisoned 146 windows with INSTRUMENT-SUSPECT.
  rx_dropped is post-`rx_packets`, post-capture-tap kernel demux → recorded
  as `demux_dropped`, never a verdict. Verdict lanes = rx_missed/over/fifo/
  errors + tx lanes. milan-fpga c3c00ee8 + milan-tests-avb e0bb2b9
  (runner + 68/68 tests incl. the new demux control).

## 5. Campaign triage (torture-ax-postoutage.jsonl on pw0, STILL RUNNING vs 0x0016)

5,055 records: 985 PASS / 340 FAIL / 33 INSTRUMENT-SUSPECT. The 340 decompose
COMPLETELY: 159 unlicensed-artifact (§4a) + 146 instrument-artifact (§4b) +
35 real-but-known 0x0016-era gaps — every one involves axt0 (the only
egressing talker on 0x0016; idx>0 egress stack #45 + SRP-only licence #17
landed after 0x0016) + mandatory-mask fails = features awaiting the new
bitstream. NOTHING in the run indicts trunk RTL.

## 6. Open (unchanged priorities)

#51 the fit (4 seeds live) → flash → campaign at 0x0021; then #37 listener
per-interval counters, #48, #53 LOCK index bound (+~8 LUT, post-fit), #49 GM
torn latch + #50 STREAM_OUTPUT unsolicited (USER: after audio), #21 DS20D
return leg (bench idle only — campaign owns the bench), #42 TCAM hazard,
#31 KL_pcm_tx. snd-kl-milan WC-read artifact re-measure on rv32 silicon.

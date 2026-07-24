# Small handover — 2026-07-23 (servo bring-up + ALSA + SRP-repair round)

Full history: `HANDOVER.md` + `BENCH_TOPOLOGY.md` + `MILAN_COMPLIANCE_GAPS.md`
(§5b/5c/5d + the USER attack order, now with AX42 as item 0). Memory:
`servo-bringup-round-0723`. Audio budget: `AUDIO_THDN_BUDGET.md` (private repo).

## Consoles — `~/bench-console/` (unchanged)
TRAP: (re)opening the ARTY serial port RESETS the board (DTR). AX port safe.
`strings` on console logs DROPS <4-char lines — prefix reads (`echo X=$(...)`).
Board scp via pw0 dropbear (`sudo -u alex ssh/scp -O root@192.168.127.{1 AX,3 ARTY}`);
reflash regenerates host keys → `ssh-keygen -R` on pw0 (accept-new does NOT
cover CHANGED keys). Taps on amx-ubuntu-server (tap1=AX enxe8eb1b37e2c0,
tap2=ARTY enxe8eb1b39111a); NEVER `tcpdump -e` on ProfiShark links (pseudo-
header MAC artifacts) — use `-w` + offset-28 python, or the srp_qna.py dissector.

## Boards (QSPI self-boot, milan CSR 0x90000000)
- **ARTY = `asl_milanfinal53e` (+0.174, VERSION 0x000A)** — the everything-build:
  N×N + TDM + dynamic maps + bind-restore + servo + CDC-128 ring lane +
  servo step-guard + 0x8F8/0x8FC + stream-table alias protection. Rootfs has
  snd-kl-milan (.copy op) + alsa-utils (arecord/aplay). ★ CERT 63/63 + 323/323
  single clean run ★.
- **ALINX = AX39 + fixed flash images (PHC fix now PERMANENT)** — the DTB
  carries `kl,rsc-clk-mhz=100`; survives reboots with no manual step. ★ CERT
  63/63 ★. e2 port (`--eth-port e2`). Still the 16-deep ring CDC + the e2 TX
  wedge (AX42 fixes both).

## Proven this session
- ★ SERVO (roadmap 6) SILICON-PROVEN: LOCKED at the true +6.7 ppm, rails ZERO,
  HOLDOVER + re-acquire proven, step-guard (U10) hardened. Analog loop
  **−83.9 dB = the CS4344⊕CS5343 datasheet power-sum limit (−83.8)** — the
  loop is at the converter silicon floor; the gateware's contribution is
  below it. (Old −73.4 = ~10 dB of NCO-era clock artifacts, now gone.)
  The mf51 "wrong-way" verdict was an INCOHERENT-CHAIN confounder; polarity
  is correct, 0x8FC ps_invert default stays 0.
- ★ Saved-state M-ACMP-9 exit: reboot → S51 journal restore → 0x7A0 inject →
  fast-connect → stream re-locks with NO controller.
- ★ ALSA (roadmap 7) functional on silicon: card `Milan`, arecord rw byte-
  exact (.copy op), mmap path clean, digital wire −149.6 dB.
- ★ SRP/gPTP repair: AX 2× PHC (missing DT prop) cascaded to code-8/pruning;
  fixed → switch relays AX as GM, reservation ACTIVE end-to-end.
- Test coverage grew: migen `test_pcm_ring.py` (reproduces the shed at
  depth-16, proves depth-128 zero-drop byte-exact), dp-TB SERVO + 0x8FC +
  nxn-sid-0 legs, aecp clk_src_o pin, servo U10. Gates: dp 172/0, nxn 63/0,
  aecp 490/0, servo 52/0, csr 41/0, yosys 39/39.

## The USER-ordered 12-item roadmap — status
(the canonical list; the "open items" below are the delta of what's left)

|  # | Item                                             | Status |
|----|--------------------------------------------------|--------|
|  1 | AX timing/residuals (dp-CDCs, MDIO, e2 migration)| ✅ DONE (silicon) |
|  2 | RTL fixes for the workaround items (GMII CDC reinit, shadow invalidate, I2SPB W1C) | ✅ DONE — **except the e2 TX wedge → re-scoped as AX42, gaps item 0** |
|  3 | Spec-aligned module tree + tsn_gen traceability matrix | ✅ DONE (204 rows, 163✅/17🟡/7❌ + 17 ➖ N/A) |
|  4 | Software-defined End-Station builder (clusters, EUI-64, estimator, TDM/I2S/AES3/SPDIF) | ✅ DONE |
|  5 | N×N AAF streams (AX 8×8 / Arty 4×4), shared engines + ctx RAM | 🟡 4×4 silicon-proven; 8×8 sim 82/0 (PR #16); **8×8 Vivado ship build TIMING-MET (WNS +0.61/+0.40 ns); compressed full-flashboot rebuild in flight → matched-image QSPI flash + silicon verify pending** (07-24: gateware-only SRAM load did NOT boot — needs compressed bit + matched images) |
|  6 | MMCM-DRP media-clock servo | ✅ DONE — **silicon-proven this session** (LOCKED, rails zero, HOLDOVER, −83.9 dB at the converter floor); polish left: bless auto_repair + rails soak |
|  7 | ALSA driver record/play over-Milan via PipeWire | 🟡 record functional; **`snd-kl-milan` ALSA card driver EXISTS in-repo but NOT in the deployed rootfs (aplay/arecord = 0 cards on both boards — PipeWire-only today); playback KL_pcm_tx PR #18; the card deploys with the 8×8 reflash** |
|  8 | Dynamic audio maps (ADD/REMOVE + es-4.16) | ✅ DONE |
|  9 | Milan saved-state fast-connect | ✅ DONE — M-ACMP-9 exit proven; **left: acmp-persist save-wedge fix + the CRF-flags journal drill leg** |
| 10 | Spec-matrix peer-validation (human 1:1 + behaves per row) | 🟡 human 1:1 still USER-gated; **per-command tsn_gen behave fixtures landed (unmerged PRs): CLOCK_SOURCE/CONTROL/CONFIGURATION/SAMPLING_RATE/STREAM_FORMAT/READ_DESCRIPTOR/NAME/STREAM_INFO (#14-24) + AUDIO_MAPS (#28) + MAX_TRANSIT_TIME/GET_MILAN_INFO/ACQUIRE/LOCK (#33)** — each self-tested + independently reproduced |
| 11 | AAF end-to-end per-stage latency taps (CSR + DDR3 history) | 🟡 **CSR taps PR #17 + `KL_lat_history_ring` DDR3 time-series ring PR #32 (TB 84/0, PCM-ring CSR ABI); live E2E latency MEASURED (ts_delta 0x6EC = +633 µs stable, 0 LATE/EARLY)** |
| 12 | es-1.1/1.2 BMCA variants | ⏳ NOT STARTED (very end, switch-gated) — **USER-excluded from the 07-24 "finish the roadmap" push** |
| 13 | **Reduce E2E latency to EQUAL the pto** (USER 07-24) | ⏳ NEW — the measured capture→accept pipeline is ~1.37 ms of overhead atop the presentation buffer; decompose with the item-11 taps, cut talker-side batching/FIFO so pto=500 µs → real 500 µs E2E, 0 LATE |

Cross-cutting adds this session (not in the original 12): **AX42** bug-fix
round (gaps item 0) and the **PCM-ring-in-BRAM** proposal (gaps §2), both in
the prioritized open items below.

**chmap64 — 64-in/64-out channel-map fabric (USER 07-23/24, major feature):**
8×8 streams × up to 8 ch = 64 stream-channels each way, mapped to/from ALSA
(8× 8-ch subdevices) and TDM8/I2S physical I/O. Delivered as 6 verified-unmerged
PRs: `KL_chan_map_render` (RX (stream,ch)→phys crossbar, #26 58/0), `KL_chan_map_capture`
(per-pair-slot TX source mux + `pair_slot`→[4:0], #29 43/0), `KL_tdm_render`
(TDM8 out serializer, #30 37/0), the es-4.16 dynamic-audio-map→fabric binding
behave fixture (#28 9/9), the architecture doc (#27), and the datapath
**integration** (#31, add-alongside + bypass-by-default, milan_dp **172/0**
byte-exact, 8×8 elaborates, CSR 0x900 map window). Map word = 16-bit
{en,src,idx}; AEM `ADD/REMOVE_AUDIO_MAPPINGS` (0x2C/0x2D) owns the write port,
CSR 0x900 = debug override. Default-off = bit-identical CERT audio path.

**E2E latency + flash findings (07-24):** live E2E on AX→Arty = `ts_delta`
(0x6EC) +633 µs, 0 LATE ⇒ samples held to `avtp_timestamp`, E2E = `pres_offset`
(NOT ts_delta — that is only the residual buffer headroom). pto lever
(SET_STREAM_INFO/MSRP_ACC_LAT, or SET_MAX_TRANSIT_TIME 0x4C) = NOT_SUPPORTED on
the deployed bitstream (feature newer than the flash). Flash lessons: a
QSPI-bootable AX bitstream MUST be built with `--with-spiflash --flashboot full`
(pins `BITSTREAM.GENERAL.COMPRESS`; raw 100t frame is 3.65 MiB, slot is 2.25 MiB)
AND flashed as a **matched image set** (bitstream+kernel+dtb+rootfs) — a
gateware-only SRAM load does NOT boot. Recovery = `amx-pi powerstrip off/on 0`.

## Open items (prioritized)
1. **AX42 — ROADMAP BUG FIX (USER, gaps item 0):** the e2 MAC-TX wedge fixed
   IN THE LOGIC. Link bounce wedges e2 TX permanently (internal counters
   tick, WIRE empty — RMON blind, only the tap tells truth); the link guard
   DETECTS + fires reinit but the wedge lives OUTSIDE the reset scope (the
   PHY-side eth_tx/gtx clock path). TB-first with a clock-stop model; extend
   the guard's sequenced reset to cover the gtx output primitive. Carry
   CDC-128 to the AX. Then the 8×8 stream round + area levers (L2 32K in;
   crf_rx ts-ring→BRAM; pruning) on top.
2. **★ PCM ring → on-chip BRAM (NEW, USER 2026-07-23):** move the PCM ring
   from the LiteDRAM window to a dual-port BRAM. Kills BOTH open ring
   failures at the root — the BRAM write port never stalls (no shed, CDC
   depth moot) and there is no DRAM arbitration / write-posting ambiguity
   (I6 cannot exist on that path). BUDGET FITS: mf53e uses 99/135 RAMB36
   (73%), 36 free; a period-latency ring needs only ~16–32 KB (4–8 RAMB36 =
   42–85 ms stereo/48k). Design: replace the WishboneDMAWriter target with a
   BRAM + the same offset/enable/loop CSR ABI so the driver is unchanged
   (or a thin base-address swap). This SUPERSEDES both #3 and the CDC-128
   carry if taken.
3. **I6 — the 1-in-24 ring artifact** (if BRAM ring not taken): NOT the CDC
   depth (survives on CDC-128 silicon). Needs a purpose-built ONE-SHOT mmap
   prober (every existing tool pointer-chases and confounds), engine frozen,
   known pattern; then fabric-fence vs driver-pointer-guard. rw+mmap OTHERWISE
   WORK — not a CERT blocker.
4. **acmp-persist save wedge** (3/6 wedge, not load-dependent; Ctrl-C
   recovers): timeout+retry in the script, or move the journal write into
   the driver. Blocks the drill-7 CRF-flags journal leg.
5. **Servo polish**: bless auto_repair (one bench ClkReg readback to confirm
   the expected divider encoding, then flip the 0-tie), hour-long rails soak.
6. **ALSA completion**: PHC LINK-timestamp leg, on-board PipeWire via the
   stock ALSA source, playback direction (KL_pcm_tx gateware — record exists,
   play doesn't).

## Human-gated (USER)
- **Roadmap 10 — spec-matrix peer review**: the 204-row traceability matrix
  one-to-one with a human, then a behave per confirmed row.
- e1 exoneration retest (needs a cable move).

## Deliberately last (USER ordering)
- Roadmap 11 — AAF per-stage latency taps (CSR + DDR3 history).
- Roadmap 12 — es-1.1/1.2 BMCA variants (switch-gated).

## Traps burned this session
- CSR reads ≥0x800 returned 0 unless the window claimed them (rd_in_window
  cut at 0x800): 0x8F8/0x8FC needed explicit carve-outs. Any new ≥0x800 reg
  needs BOTH a live_mux arm AND the rd_in_window term; the 512-word shadow
  aliases addr[10:2] so ≥0x800 plain-RW must be dedicated flops.
- Stream-table override arms PERMANENTLY on first window write: stage
  SID 0x814/8 before ANY 0x810 CTRL write at a live idx (a route-only commit
  with sid=0 hijacked the ACMP alias and froze a locked stream).
- vexii `update_repo` build-time git pull ABORTS when upstream dev touches the
  locally-patched Soc.scala → killed 4 sweep launches; pinned
  `update_repo="no"` in the _vex_args namespace (milan_soc.py). Manual repo
  update only.
- Rootfs is 23 KB from its 8.91 MB flash slot — next growth needs a relayout
  (alsa fit only after trimming alsamixer/alsactl/ncurses/terminfo/fputest/
  iproute2-extras/unused-modules).
- worktree stale-fork trap struck again (agent worktree cut from an ancient
  base f51a27b) — always `git log --oneline -1` verify, `git checkout -B <br>
  <good-hash>` to fix.
- ProfiShark tap leg can go physically dead on a bounce (zero frames both
  directions) — needs a power-cycle/reseat; not a board fault.
- CERT needs a reset-defaults pre-step: a leftover clock_source=2 cost a
  rerun (the suite correctly pins the default). Reset before every CERT run.

## Standing rules (unchanged)
One-line commits, no trailers, hackerman-kl, both repos, push `--force` on USER
ask · the-private-test-repo is PRIVATE, CERT suite at tests/cert-recreate/, the
A-word NEVER in committed text (say CERT) · every round grows the TB suite ·
always parallelize (worktree lanes; serial only Vivado 3×32-thread + the bench)
· amx-pw1 = NEVER TOUCH · measure before AND after, HW counter not comment.

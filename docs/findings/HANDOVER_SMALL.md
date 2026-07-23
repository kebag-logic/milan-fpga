# Small handover — 2026-07-23 morning (servo bring-up + SRP-cascade repair)

Full history: `HANDOVER.md` + `MILAN_COMPLIANCE_GAPS.md` (item-6 updated) +
memory `servo-bringup-round-0723`. Consoles `~/bench-console/` (ARTY
serial-open TRAP stands). Wire truth via the taps (tools redeployed to
tap-host /tmp; **never `tcpdump -e` on ProfiShark links** — pseudo-header
artifacts; use `-w` + offset-28 python or the srp_qna.py dissector).

## Boards
- **ARTY** = `eto_milanfinal51` (VERSION 0x000A, the everything-build).
  KNOWN mf51 SILICON QUIRKS (all fixed in RTL, land with mf52):
  0x8F8 reads 0 (CSR dead-zone bug — the servo runs invisibly);
  stage SID 0x814/8 before ANY 0x810 CTRL write at a live idx (override
  arming trap froze a locked stream); servo steps the WRONG WAY
  (rails 25x worse at clock_source=2 — set 0x8FC[0] ps_invert on mf52).
- **ALINX** = AX39 (0x0009) + LIVE `modprobe kl-eth rsc_clk_mhz=100`
  (the dts lacked kl,rsc-clk-mhz -> 2x PHC -> switch dropped asCapable ->
  TalkerFailed code 8 -> pruning; fixed dts+dtb+opensbi committed, land
  with the AX41 flash). After the fix: AX = GM (relayed by the switch),
  clean TalkerAdvertise, ARTY Listener Ready, reservation ACTIVE.
- A REBOOT of the AX before the AX41 images flash REVERTS the PHC fix
  (rerun the modprobe with rsc_clk_mhz=100).

## Proven this round
- Saved-state drills 1-6, 8-10 ★ incl. **M-ACMP-9 exit**: reboot ->
  S51 journal restore -> 0x7A0 injection -> fast-connect -> stream
  re-locks with NO controller. CRF-flags save retry pending (saves take
  minutes under full datapath load and can wedge — Ctrl-C recovers).
- Digital wire THD+N -149.6 dB PASS. Analog loop on mf51 = -21 dB
  EXPECTED (NCO actuator removed by USER exact-recovery rule): the valid
  loop = AX tone 0x6DC + CRF + ARTY clock_source=2 + a WORKING servo
  (mf52 + ps_invert).
- dp-TB grew: SERVO integration leg, 0x8FC RW leg, nxn sid-0 alias leg,
  aecp clk_src_o pin, servo U9 inverted-model leg. Gates: dp 172/0,
  nxn 63/0, aecp 490/0, servo 43/0, csr 41/0, yosys 39/39.

## In flight / next
1. mf52 ARTY 3-seed (all fixes) -> flash bitstream + images (rootfs has
   snd-kl-milan + alsa-utils; fresh crc32 xz ready) -> servo drill WITH
   0x8FC (set invert, rails cease, trim vs crystal, bake RTL default) ->
   coherent-chain THD -> ALSA arecord drill (card `Milan` probes ✓).
2. AX41 3-seed (AX40 was pre-fix and all-negative -0.5-class, sys-domain
   milandma cs_lanes cone; if AX41 misses -> sweep_extra exp/asm/enl,
   then levers: crf_rx ts-ring->BRAM, pruning).
3. CERT vs ARTY mf51 running (pw0 run_mf51_postfix.log; launch
   run_alinx.sh after). Then the pair CERT on mf52+AX41.
4. SR VID = 2 ONLY (USER: "638" never existed - memories + HANDOVER
   retraction done).

## LATE-MORNING ADDENDUM (07-23 ~07:30)
- ★ SERVO SILICON-PROVEN on mf52: 0x8F8 visible, state LOCKED, trim
  +7.3 ppm (= the known CRF offset), **rails ZERO** on the coherent
  chain, analog loop **-83.9 dB NEW RECORD** (+10 dB over the NCO era),
  HOLDOVER proven (state 5, trim frozen +8.1 ppm when the AX died).
  The mf51 "wrong-way" was an INCOHERENT-CHAIN confounder (pw0 talker
  rendered while the servo tracked the AX CRF) - polarity is CORRECT,
  0x8FC knob default stays 0.
- ★ PAIR CERT 63/63 + 63/63 (323/323 both) post-SRP-repair. run_alinx.sh
  had the WRONG FLAP TARGET (127.3 = the ARTY - fixed to 127.1).
- **AX IS NETWORK-DEAD, NEEDS HANDS**: the CERT link-flaps re-fired the
  historic MAC-TX wedge (e2: the link guard DETECTS - 12 events - but
  its auto macsys-reset never fires on e2, EPOCH stayed 1). JTAG
  reconfig rebooted it but the LINK never returned: the PHY reports
  no-link and the tap-1 leg carries ZERO frames both directions ->
  physical: power-cycle/reseat the ProfiShark tap-1 leg (or bypass it).
  After link returns: `modprobe kl-eth rsc_clk_mhz=100` + ifconfig
  192.168.127.1 (the flashed rootfs still has the 50-default until the
  AX41 images land). AX41 must add: e2 link-guard reset-path fix.
- **ALSA rw-capture root cause = GATEWARE**: the 16-deep PCM CDC lane
  sheds 1 beat in 24 when the CPU reads the ring region concurrently
  (ring idle-clean, loaded-holed - proven by a concurrent
  pcm_ring_dump). Fix committed: lane depth 128 (80ee795) -> needs the
  mf53 build (chained after AX41 in Vivado). arecord itself works
  (driver .copy op landed, d5c23b3); mmap mode clean even today.
- mf52-asl (+0.155) FLASHED on the ARTY with the slim rootfs (alsa
  fits: alsamixer/alsactl/ncurses/terminfo/fputest/iproute2-extras/
  unused-modules trimmed; slot 8.89 of 8.91 MB - nearly full, next
  growth needs a flash relayout).

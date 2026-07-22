# Small handover — 2026-07-22 (counter-fix + ethtool/MDIO round)

Full history: `HANDOVER.md` + `BENCH_TOPOLOGY.md` + `MILAN_COMPLIANCE_GAPS.md`
(§5b/5c = this round's findings; attack order = the USER-reordered list).

## Consoles — `/home/alex/bench-console/` (unchanged)
`arty_in`/`arty.log`, `ax_in`/`ax.log` (write a line, read the log).
**TRAP: (re)opening the ARTY serial port RESETS the board** (DTR). The AX
port is safe.

## Boards (both QSPI self-boot, milan CSR base 0x90000000)
- **ARTY** = `eto_milanfinal46` (**+0.378, new record margin**): VERSION
  0x0006 + buffered dp-CDCs + the LINK_UP/DOWN counter fix (cnt_link =
  phy+guard, linkmon term excluded — Milan-correct +1 per flap) + images
  reflashed (rootfs with kl-eth `mdio1`, DTB with the "phy" reg block,
  litex_nax opensbi with that DTB embedded).
- **ALINX** = `eto_milanfinal34` (+0.076): VERSION 0x0006 — **guard on AX,
  silicon-drilled** (freeze byte-exact, real phy_crg_reset bounce, TX alive
  after). Driver `mdio1` live via insmod (NOT persistent — rootfs reflash
  pending with AX35). **AX35 = mf46-parity + e1 MDIO pads (K16/J17) in
  flight**; on a keeper: flash bitstream + images (opensbi_arty pattern!)
  → `ethtool -r` on the RTL8211E becomes real.

## This round (all silicon-verified unless noted)
1. **AX timing CLOSED**: buffered dp-CDCs (AsyncFIFOBuffered) — AX34 3/3
   keep after 12 missed draws; violator was the mac_rx_cdc BRAM CLK→Q cone
   (LiteX storage_N names RESHUFFLE — map in the .v before chasing).
2. **Loop THD+N −73.4/−73.3 dB @ −20.0 dBFS** (record) re-verified on mf44
   AND mf45 with the replugged DAC/ADC. Non-disruptive method: swap the pw0
   aaf_stream.py source file to a tone — same SID, no rebind.
3. **CERT re-run (mf45+AX34): 59/61 plain + 2/2 tap features.** The 2
   link-flap fails root-caused the LINK_UP double-count (§5c) → RTL fix in
   mf46; re-run of the flap feature on mf46 = the pending proof.
4. **ethtool ops in kl-eth (`mdio1`)**: -r / ksettings / -S / -i via a
   clause-22 MDIO bitbang (one-TA-cycle sampling trap, §5c). ARTY DP83848
   verified byte-exact. AX needed the pads WIRED (platform edit, AX35).
5. **Boot-images trap re-burned**: buildroot's generic fw_jump.bin =
   SILENT hang at "Liftoff!" — always the litex_nax opensbi
   (fpga/boot/build_opensbi.sh, embeds the DTB; per-board HARTS/TIMER_HZ).

## Next steps
1. mf46 boot-verify → rebind music (acmp_bind connect, no set_fmt needed)
   → re-run the link-flap feature (runner: `sudo run_arty.sh
   features/link-flap.feature` in the CERT recreate dir in pw0's home —
   legacy-named, exact path in session memory; flap cmds need
   `sudo -u alex ssh` — root has no dropbear key). Expect 2/2 → 61/61.
2. AX35 keeper → flash AX bitstream + images (build opensbi for AX:
   DTB=milan_ax7101_vexii.dtb, TIMER_HZ=100000000) → ethtool drills on the
   RTL8211E → full CERT on the final pair.
3. Then the USER-reordered roadmap: spec-aligned module tree →
   software-defined End-Station build → **NxN AAF streams (AX 8x8,
   Arty 4x4, via command parameters)** → MMCM-DRP servo → … (gaps doc).

## CERT harness (rebuilt after the pw0 /tmp wipe — now persistent)
CERT recreate harness in pw0's home (legacy-named dir; exact path in session memory) (runner scripts
run_arty.sh / run_alinx.sh, DUT :02/:01), venv = the legacy-named one in
pw0's home; tap helpers (gptp_cadence.py / srp_domain.py) on
amx-ubuntu-server /tmp AND persisted in the private recreate snapshot
(tools-tap/). pcap2s32.py rebuilt → the-private-test-repo fpga/tests/.

## Fresh traps
`ssh -f` + setsid for detached pw0 daemons (plain `&` dies with the ssh) ·
scp scripts to pw0, never ssh-heredoc them (nested quotes silently strip
exports) · dropbear host keys REGENERATE on reflash+reboot (ssh-keygen -R) ·
the switch has NO IP/UI management (AX eth0 = 192.168.127.1 is fine;
BENCH_TOPOLOGY's switch-ssh row was stale) · deploy/flash needs the litex
venv on PATH (BIOS make + crcfbigen shell out to bare python3).

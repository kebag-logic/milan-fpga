[OBSOLETE + 2026-08-16]

# MVP Milan Talker (Arty, flash-standalone)

Status: 2026-07-12. Goal: a discoverable, la_avdecc-clean Milan endstation that
STREAMS AAF-PCM audio from the Pmod I2S2 (JA) with zero CPU in the media path —
running entirely from QSPI flash on power-up.

> **STATUS SUPERSEDED (media clock):** the free-running media-clock caveats
> below are a MILESTONE RECORD. The media clock is now recovered in silicon by
> the MMCM-DRP servo ([`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`](../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv), MCSRV CSR
> `0x8F8`/`0x8FC`): coherent CS4344+CS5343 chain, analog loop measured
> **-83.9 dB** (the converter floor). Read this doc as the flash-standalone MVP
> talker milestone; the AAF frame/CSR content below is unchanged and accurate.
>
> **STATUS SUPERSEDED (the control plane, 2026-08-13):** "discoverable,
> la_avdecc-clean" no longer follows from the boot sequence below. ADP, ACMP and
> SRP are the pinned `protocol-processor` submodule's, and its AECP µCPU answers
> `READ_DESCRIPTOR` while returning a conformant `NOT_IMPLEMENTED` echo to every
> other AECP command. Those descriptor reads come from an image in DRAM at a
> compile-time base which **must be loaded before the entity is enabled** —
> nothing in this repository builds or writes it, and `S50milan` does not, so a
> board booted exactly as described below is discovered over ADP and then
> answers `BAD_ARGUMENTS` to every enumeration read. The media path is
> unaffected: the talker streams regardless.

## Contents

- **[Signal chain (all fabric, cd_milan 50 MHz on the Arty)](#signal-chain-all-fabric-cd_milan-50-mhz-on-the-arty)** — ADC to wire in one line, and the MVP decision that made it work: injection moved AFTER the shaper because CBS credit math scaled for 1 Gb/s gated the 100 M Arty link to one frame per 30 s.
- **[Frame (90 B, ~5.8 Mbit/s at 48k class A)](#frame-90-b-58-mbits-at-48k-class-a)** — The exact AVTPDU layout in one paragraph: tag, subtype, stream_id composition, the +2 ms timestamp offset, and 2ch x 6 samples x INT32 per 125 us.
- **[MVP tradeoffs (documented, not hidden)](#mvp-tradeoffs-documented-not-hidden)** — Four named shortcuts, including the one this page's banner supersedes: fs = clk/1024 = 48.828 kHz declared as 48 kHz. Also the two levels of "working" — frames-on-the-wire needs no gPTP, a listener playing in sync does.
- **[CSR (milan_csr 0x654 group)](#csr-milan_csr-0x654-group)** — AAF_CTRL enable + VID field and the AAF_DMAC pair, plus which init script turns them on at boot.
- **[Verification](#verification)** — The 2026-07-12 silicon numbers: 8.1k frames/s, avtp_timestamp advancing exactly 122,880 ns per sequence number with zero jitter, and why captures show untagged 86-byte frames.
- **[Flash (v3 QSPI-boot, one verb)](#flash-v3-qspi-boot-one-verb)** — The single `build.sh flash` command and the jumper position for power-on standalone streaming.

## Signal chain (all fabric, cd_milan 50 MHz on the Arty)

Pmod I2S2 ADC (CS5343, JA/pmoda) -> aaf_talker_i2s (I2S master; MCLK=clk/4,
SCLK=64fs, LRCK=clk/1024) -> IEEE 1722 AAF-PCM frames -> injected at the final
datapath merge (post-shaper) -> MAC -> wire.

**Injection point (MVP decision, 2026-07-12):** the AAF stream carries its own
802.1Q PCP-3 tag and was designed to flow classifier -> class-A CBS queue. On
silicon the CBS credit math is scaled for 1 Gb/s while the Arty wire is 100 M
(the known `is_1g=0` pending item), so the CBS credit-gated the stream to ~1
frame per 30 s. For the MVP the talker is injected AFTER the shaper (the same
post-shaper path the control plane uses -> today that is the protocol
processor's packed TX plus MAAP on the one control lane; when this was written
it was the separate ADP/AECP/ACMP legs) -> continuous emission, UNSHAPED. Proper
class-A shaping (classifier + CBS at 100 M) is the `is_1g` follow-up; the
frame FORMAT and content are identical either way.

## Frame (90 B, ~5.8 Mbit/s at 48k class A)

Eth + 802.1Q{PCP3,VID2} + 0x22F0 + AAF hdr (subtype 0x02, sv|tv, seq++,
stream_id={MAC,uid0}, avtp_timestamp = PHC ns + 2 ms) + 2ch x 6 samples x
INT32 (24-bit left-justified). One AVTPDU per 6/48k = 125 us nominal.

## MVP tradeoffs (documented, not hidden)

- **Media clock**: fs = clk/1024 = 48.828 kHz at 50 MHz, DECLARED 48 kHz
  (+1.7 %). A listener that recovers clock from presentation time tolerates
  it for a demo. The real fix is a gPTP-recovered media clock or a CRF stream (see
  the media-clock note below) — NOT just a cleaner oscillator.
- **Backpressure**: if a frame is still serialising, incoming sample pairs
  are dropped (no elastic buffer). At 90 B / 125 us on a 100 M wire this
  never triggers, but it is not a jitter-proof design.
- **avtp_timestamp**: low 32 bits of the PHC + 2 ms transit. The talker
  stamps from the SAME counter ptp4l disciplines to the grandmaster (kl-eth
  adjfine/adjtime), so timestamps ARE in gPTP time ONCE gPTP IS LOCKED. Two
  levels of "working":
    - frames-on-the-wire (validates the RTL: subtype 0x02, format, seq,
      PCP3): needs NO gPTP — emission never blocks;
    - a listener PLAYING IN SYNC: REQUIRES gPTP locked, else the
      presentation times are in an undisciplined private time base and
      playout drifts. Do NOT read "MVP" as "gPTP optional for audio".
- **media clock NOT locked to the network clock**: even with gPTP up, the
  I2S sample clock is free-running (clk/1024 = 48.828 kHz) while the frame
  declares 48 kHz. Samples are produced at one rate, timestamped as another
  -> a real Milan talker recovers the media clock FROM gPTP (media clock
  recovery) or ships CRF; the listener otherwise needs async SRC. This is
  the biggest gap between the MVP and a glitch-free Milan stream.

## CSR (milan_csr 0x654 group)

| off | field |
|-----|-------|
| 0x654 | AAF_CTRL: [0] enable, [27:16] VID (reset VID2, disabled) |
| 0x658/0x65C | AAF_DMAC lo/hi (reset MAAP-range 91:E0:F0:00:FE:01) |

Brought up by `/etc/init.d/S50milan` (rootfs overlay): identity :02, ADP
enable, AAF_CTRL enable. Fully autonomous after boot for the media path. Note
that the ADP enable bit is now one of two — `ADP_CTRL[0]` (`0x600` bit 0) is
ORed with `PP_CTRL[0]` (`0x920`), either enables the entity — and that enabling
it without first loading the descriptor image into DRAM leaves the entity
discoverable but unreadable (banner above).

## Verification

- [tb/verilator/aaf](../tb/verilator/aaf): 19/19 byte-exact frame (header, payload, seq, timestamp).
- milan_dp: 26/26 (talker integrated, no datapath regression).
- **Silicon (arty_v10/eppo, WNS +0.258, flashed 2026-07-12): ALL GATES PASS.**
  Counters: 8.1k frames/s + 48.9k pairs/s (exact design cadence). At the peer:
  seq +1 per frame @ ~122 us, payload = live ADC noise, avtp_timestamp
  advances EXACTLY 122,880 ns per seq (= 6 x 1024 x 20 ns, zero jitter) on
  live PHC time. Boots standalone from QSPI (BIOS xz decode verified).
  Note: the switch strips the VID-0 priority tag on its untagged egress
  ports, so captures show untagged 86-B frames — expected .1Q behavior.

## Flash (v3 QSPI-boot, one verb)

`build.sh flash arty:build_arty_<seed>_arty_v9` -> bitstream@0 + Image.xz +
opensbi + dtb + rootfs. Set Arty JP1 -> QSPI at the bench; power-cycle boots
gateware + Linux + S50milan -> streaming.

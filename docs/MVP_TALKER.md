# MVP Milan Talker (Arty, flash-standalone)

Status: 2026-07-12. Goal: a discoverable, la_avdecc-clean Milan endstation that
STREAMS AAF-PCM audio from the Pmod I2S2 (JA) with zero CPU in the media path —
running entirely from QSPI flash on power-up.

## Signal chain (all fabric, cd_milan 50 MHz on the Arty)

Pmod I2S2 ADC (CS5343, JA/pmoda) -> aaf_talker_i2s (I2S master; MCLK=clk/4,
SCLK=64fs, LRCK=clk/1024) -> IEEE 1722 AAF-PCM frames -> injected at the final
datapath merge (post-shaper) -> MAC -> wire.

**Injection point (MVP decision, 2026-07-12):** the AAF stream carries its own
802.1Q PCP-3 tag and was designed to flow classifier -> class-A CBS queue. On
silicon the CBS credit math is scaled for 1 Gb/s while the Arty wire is 100 M
(the known `is_1g=0` pending item), so the CBS credit-gated the stream to ~1
frame per 30 s. For the MVP the talker is injected AFTER the shaper (the same
post-shaper path ADP/AECP/ACMP use) -> continuous emission, UNSHAPED. Proper
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
enable, AAF_CTRL enable. Fully autonomous after boot.

## Verification

- tb/verilator/aaf: 19/19 byte-exact frame (header, payload, seq, timestamp).
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

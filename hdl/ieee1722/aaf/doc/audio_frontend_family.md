# Audio capture front-end family — interface contract

<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

Item-4 audio-interface subtask (docs/NXN_ARCHITECTURE.md §2.1 "physical
interface x1"). One capture front-end exists per build, selected by the
`milan_datapath` `AUDIO_IF_SLOTS_P` generate (`milan_soc.py
--audio-interface`, emitted by `sw/builder` from `audio_interface.kind`).
Every member implements the SAME output contract toward the shared
`KL_aaf_packetizer`, so the packetizer, TCTX partitioning and the TB
harnesses never change per interface.

## The pair-stream contract (all members)

Datapath-clock (`clk_i`) outputs:

| port | meaning |
|------|---------|
| `pair_valid_o` | one-cycle pulse per emitted L/R pair |
| `pair_slot_o[3:0]` | pair index: the pair carries physical channels `{2k, 2k+1}` |
| `pair_l_o/pair_r_o[23:0]` | samples, MSB-justified into the 24-bit pipeline width |
| `pairs_captured_o[31:0]` | free-running liveness counter (CSR-observable) |

Clock-domain discipline (the KL_aaf_capture_i2s 07-18 clean-clock lineage):

* serial capture runs in the interface's own bit-clock domain (I2S: the
  clean MMCM dividers we master; TDM: the external `tdm_bclk_i`; AES3:
  the RECOVERED biphase-mark clock) with a locally synchronized reset;
* pairs cross into `clk_i` exclusively through the gray-pointer
  `cdc_pair_fifo` (52-bit `{slot, L, R}` payload), popped one at a time;
* any Philips-style data delay is applied ONCE, in the front-end — never
  again in a TB chip model (the DOUBLE-Philips-delay history, 78bbabe).

Stream mapping downstream: `KL_aaf_packetizer` partitions the pair-slot
space by the TCTX `chans` prefix sum (talker *t* owns `chans_t/2`
consecutive pair slots; `channels_per_frame` even 2..8 per stream).

## Members

| member | status | slots/pairs | notes |
|--------|--------|-------------|-------|
| `KL_aaf_capture_i2s` | RTL, silicon-proven | pair 0 only | stereo I2S master for the Pmod I2S2 (CS5343), pilot-tone override |
| `KL_tdm_capture` | RTL (this round) | `SLOTS_P/2` pairs (TDM8/16/32) | TDM slave: pulse or 50%-duty fsync (edge-armed), data delay 0/1, 32/24/16-bclk words, MSB first; `tdm_mclk_o` = clk_audio/2 convenience MCLK |
| `KL_aes3_capture` | contract only | pair 0 only | AES3 (AES3-2009 / IEC 60958-4 professional) |
| `KL_spdif_capture` | contract only | pair 0 only | S/PDIF (IEC 60958-3 consumer) |

## AES3 / S-PDIF contract (the later biphase-mark members)

Both are the same 2-channel biphase-mark transport and SHALL share one
deserializer core, parameterized by channel-status interpretation only:

* **Ports**: `clk_i/rst_n`, `clk_audio_i` (oversampling reference),
  `aes_rx_i` (the biphase-mark line), the pair-stream contract above, plus
  `locked_o` (subframe-sync acquired) and a channel-status/validity
  snapshot for CSR export (`cs_bits_o[31:0]` = first 32 channel-status
  bits: sample-rate/emphasis words a provisioning daemon needs).
* **Clock recovery IN the module**: the biphase-mark (BMC) line is
  oversampled with `clk_audio_i` (24.576 MHz = 4x the 128·fs bit rate at
  48 kHz); edge-interval discrimination separates half-bit/full-bit cells,
  and X/Y/Z preambles (which deliberately violate BMC) give subframe/
  block sync. No external bit clock exists — this is the family member
  where the "interface bit-clock domain" is the recovered symbol stream
  inside the `clk_audio_i` domain, so the `cdc_pair_fifo` crossing stays
  IDENTICAL (write side = `clk_audio_i`).
* **Framing**: subframe = preamble(4) + aux(4) + sample(20|24) + V/U/C/P;
  subframe A → `pair_l`, subframe B → `pair_r`, emitted on B completion
  with `pair_slot_o = 0` (stereo members own pair 0, exactly like I2S).
  24-bit mode takes aux+sample MSB-justified; 20-bit mode left-justifies
  into 24 (word_length_bits 16/20/24 per the builder schema).
* **Sample gating**: a subframe with V (validity) set flags the sample
  invalid; contract = emit the pair anyway and count it in an
  `invalid_frames` CSR counter (wire truth: the AAF talker never
  synthesizes silence — policy belongs to the listener/provisioning).
* **Parity/lock**: P-parity errors and preamble loss drop lock
  (`locked_o` low, no pairs emitted) until two clean blocks re-arm —
  the same "never trust a level as an edge" arming rule the TDM fsync
  detector uses.

The packetizer needs NO change for these members: 2-channel wire truth is
today's default TCTX shape (`chans = 2`).

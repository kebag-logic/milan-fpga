# README-parameters — `KL_i2s_playback`

<!-- Filled instance of docs/templates/README-parameters.template.md
     (gaps attack item 4, pilot module). The other hdl/avtp modules get
     their own sections/files as the item-4 round proceeds. -->

Module(s): `hdl/avtp/KL_i2s_playback.sv`
Instantiated by: `hdl/common/milan_datapath.sv` (`i2s_player`), datapath
elaborated by `sw/litex/milan_soc.py` (`Instance("milan_datapath", ...)`).

Selected by the end-station config as `audio_interface.kind: i2s_philips`
(schema `kebag-logic/milan-endstation-config`, see
`configs/endstation_arty_current.yaml`); the item-4 audio subtask makes the
TDM/AES3/SPDIF ser/des families sibling selections of this module.

## Parameters

| Parameter | Type / valid range | Default | Set by (instantiation site) | Config-schema origin | Notes |
|-----------|--------------------|---------|-----------------------------|----------------------|-------|
| `MCLK_DIV_LOG2` | int >= 0 | 2 | `milan_datapath.sv:i2s_player`, `MCLK_DIV_LOG2_C = $clog2(MILAN_CLK_FREQ_HZ / 12_500_000)` | `board.constraints.milan_clk_hz` (via `--milan-clk-freq` -> `p_MILAN_CLK_FREQ_HZ`) | LEGACY: unused by the clean-clock path (serializer runs on `clk_audio_i` dividers); kept only for the instantiation interface. Do not size anything from it. |
| `CLK_FREQ_HZ` | int, = the real `clk_i` frequency (50e6 arty / 100e6 ax7101) | 50_000_000 | `milan_datapath.sv:i2s_player`, `.CLK_FREQ_HZ(MILAN_CLK_FREQ_HZ)` | `board.constraints.milan_clk_hz` | Derives the per-ms servo/convergence tick. Wrong value skews the 100 ms converged window (media-lock condition), not the audio rate. CLK-PARAM GAP lesson: ALWAYS pass it explicitly. |
| `FIFO_LOG2` | int 4..12 (2^N sample pairs; RAM cost 2^N x 64 b) | 9 (512 pairs) | not overridden (module default) | (not yet driven — candidate `audio_interface.render_fifo_log2`) | Producer-side pair FIFO. Midpoint = the converged_o center and the default prefill release level; shrinking below ~2 ms of pairs tightens the underrun rail. |
| `PREFILL_C` | int 0..2^FIFO_LOG2-1 (0 = FIFO midpoint) | 0 | `milan_datapath.sv:i2s_player`, `.PREFILL_C(PB_PREFILL_C)`; `PB_PREFILL_C` is a `milan_datapath` top parameter (default 0) | (builder policy — TBs shrink it to keep injections short; silicon uses midpoint) | Underrun-recenter release level in pairs: after a rail event playback holds until fill reaches this level (one bounded gap instead of a per-sample repeat storm). Boot prefill included. |

## Derived localparams that matter

| Localparam | Derivation | Why it matters |
|------------|------------|----------------|
| `MCLK_DIV_LOG2_C` (parent) | `$clog2(MILAN_CLK_FREQ_HZ / 12_500_000)` | Shared with `KL_tone_gen` / `aaf_talker_i2s` (their MCLK dividers ARE still sys-clock derived); the 100 MHz AX build needs it re-derived — the un-parameterized value sampled wrong there. |
| FIFO midpoint | `2**(FIFO_LOG2-1)` | converged_o window center (MID±64 enter, ±128 exit, 100 ms sustain) = the EXTERNAL media-lock condition (USER rule). |

## Config-driven ports (not parameters, still schema-owned)

| Port | Config-schema origin | Notes |
|------|----------------------|-------|
| `clk_audio_i` | `clocking.audio_pll_hz` (24_576_000) | Clean MMCM audio clock; MCLK = /2, SCLK = /8, LRCK = /512 → fs = `audio_pll_hz` / 512. Any other fs (item 6 DRP servo) retunes this clock, not the module. |
| `servo_en_i` | `clocking.media_clock_sources` selection (runtime `aecp_clk_src != 0`) | USER rule hook: exact recovery only for bound-stream clock sources; no NCO actuator remains (future MMCM-DRP servo). |
| `wire_chans_i` | wire truth (runtime, from `KL_avtp_rx_monitor`) | NOT config: channels/frame of the last accepted PDU drives the 1-to-1 render mapping regardless of declared formats. |

## Cross-parameter / cross-module pairings (STRICT)

| This parameter | Must pair with | Failure mode when violated |
|----------------|----------------|----------------------------|
| `CLK_FREQ_HZ` | actual `--milan-clk-freq` of the build | ms-tick off by the ratio → convergence window / media-lock timing wrong (silent). |
| `clk_audio_i` frequency | MMCM `audio_pll_hz` = 512 x fs | Audio plays at the wrong rate; FIFO drifts to a permanent under/overrun rail. |
| `PREFILL_C` | `FIFO_LOG2` (must be < 2^FIFO_LOG2) | Release level unreachable → playback never restarts after a rail event. |

## Validation

- `board.constraints.milan_clk_hz`, `clocking.audio_pll_hz`: checked by
  `sw/builder/endstation_builder.py` (ConfigError on inconsistency with the
  board table).
- `FIFO_LOG2` / `PREFILL_C` bounds: UNCHECKED in RTL today (no elaboration
  assert) — flagged for the item-4 parameterization round.

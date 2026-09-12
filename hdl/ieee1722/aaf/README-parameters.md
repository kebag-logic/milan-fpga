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

## Contents

- **[Parameters](#parameters)** -- The four parameters with their ranges, who sets them and which config-schema key they come from, `SETPOINT_P` among them since #390 made it the prefill release level. Two warnings live here: `MCLK_DIV_LOG2` is LEGACY and nothing may be sized from it, and `CLK_FREQ_HZ` must always be passed explicitly (the CLK-PARAM GAP lesson) because a wrong value skews media-lock timing silently.
- **[Derived localparams that matter](#derived-localparams-that-matter)** -- Two derivations worth knowing: the parent's `MCLK_DIV_LOG2_C`, which `KL_tone_gen` and `aaf_talker_i2s` still depend on and which sampled wrong on the 100 MHz build, and the FIFO midpoint, the media-lock window centre at `SETPOINT_P = 0`.
- **[Config-driven ports (not parameters, still schema-owned)](#config-driven-ports-not-parameters-still-schema-owned)** -- Three inputs that behave like configuration but arrive as ports, including `wire_chans_i` - which is explicitly *not* config: the render mapping follows channels-per-frame off the last accepted PDU regardless of declared format.
- **[Cross-parameter / cross-module pairings (STRICT)](#cross-parameter--cross-module-pairings-strict)** -- Three must-match pairs and the failure each produces, all of them quiet: a wrong `CLK_FREQ_HZ` skews the convergence window silently, a wrong audio clock drifts the FIFO to a permanent rail, and a `SETPOINT_P` at or above the FIFO depth means playback never restarts after a rail event.
- **[Validation](#validation)** -- What the builder actually checks versus what it does not: clock consistency raises `ConfigError`, but the `FIFO_LOG2` and `SETPOINT_P` bounds have no elaboration assert today.

## Parameters

| Parameter | Type / valid range | Default | Set by (instantiation site) | Config-schema origin | Notes |
|-----------|--------------------|---------|-----------------------------|----------------------|-------|
| `MCLK_DIV_LOG2` | int >= 0 | 2 | `milan_datapath.sv:i2s_player`, `MCLK_DIV_LOG2_C = $clog2(MILAN_CLK_FREQ_HZ / 12_500_000)` | `board.constraints.milan_clk_hz` (via `--milan-clk-freq` -> `p_MILAN_CLK_FREQ_HZ`) | LEGACY: unused by the clean-clock path (serializer runs on `clk_audio_i` dividers); kept only for the instantiation interface. Do not size anything from it. |
| `CLK_FREQ_HZ` | int, = the real `clk_i` frequency (50e6 arty / 100e6 ax7101) | 50_000_000 | `milan_datapath.sv:i2s_player`, `.CLK_FREQ_HZ(MILAN_CLK_FREQ_HZ)` | `board.constraints.milan_clk_hz` | Derives the per-ms servo/convergence tick. Wrong value skews the 100 ms converged window (media-lock condition), not the audio rate. CLK-PARAM GAP lesson: ALWAYS pass it explicitly. |
| `FIFO_LOG2` | int 4..12 (2^N sample pairs; RAM cost 2^N x 64 b) | 9 (512 pairs) | not overridden (module default) | (not yet driven - candidate `audio_interface.render_fifo_log2`) | Producer-side pair FIFO. Its midpoint is the converged_o centre and the prefill release level only at `SETPOINT_P = 0`; with a setpoint the RAM's full depth is transient margin above it. Shrinking below ~2 ms of pairs tightens the underrun rail. |
| `SETPOINT_P` | int 0..2^FIFO_LOG2-1, in pair-FIFO ENTRIES (one entry = one L/R sample pair; 0 = legacy FIFO midpoint) | 0 | `milan_datapath.sv:i2s_player`, `.SETPOINT_P((6 * 2) + 4)` = 16 entries. Read the value in the entry unit throughout: `SETPOINT_C` substitutes it with no conversion and every consumer compares it to the entry-counting `fill_w`, one entry leaves per 48 kHz frame, so 16 entries is a 333 us steady-state fill. The instantiation derives the 16 in the SAMPLE unit (one class-A frame of the stereo lane, 6 events x 2 samples, plus a 4-sample CDC/jitter allowance) and its comment reads the result back as 167 us, which the entry unit does not support. OPEN, and NOT settled by this page: whether `(6 * 2) + 4` is the intended level or twice it belongs to the render-latency lane (PR #435, issue #386). Until that lane answers, no latency band is claimed for this value here | (derived in the datapath; not a schema key) | Steady-state fill = the constant input-to-cluster latency (task #28). Since #390 the prefill / underrun-recenter release level IS this setpoint (`PREFILL_LVL_C = SETPOINT_C`): after a rail event playback holds until fill reaches it, and the bench override that shrank it (`PREFILL_C` / `PB_PREFILL_C`) is retired. The convergence bands follow it: +/-12 converged, 24 reset in the same unit (64 / 128 at the legacy midpoint). |

## Derived localparams that matter

| Localparam | Derivation | Why it matters |
|------------|------------|----------------|
| `MCLK_DIV_LOG2_C` (parent) | `$clog2(MILAN_CLK_FREQ_HZ / 12_500_000)` | Shared with `KL_tone_gen` / `aaf_talker_i2s` (their MCLK dividers ARE still sys-clock derived); the 100 MHz AX build needs it re-derived — the un-parameterized value sampled wrong there. |
| FIFO midpoint | `2**(FIFO_LOG2-1)` | The converged_o window centre and the prefill release level at `SETPOINT_P = 0` only (MID +/-64 enter, +/-128 exit, 100 ms sustain); with a setpoint the centre is `SETPOINT_C`, +/-12 enter and +/-24 exit. The window is the EXTERNAL media-lock condition: lock is judged from observed FIFO behaviour, never self-declared by the servo, so a broken servo cannot vouch for its own convergence. |

## Config-driven ports (not parameters, still schema-owned)

The runtime clock-consumption claim is checked against the
[Milan feature status ledger](../../../docs/reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `crf.media-clock-consumption` | `implemented` | - |
<!-- milan-feature-status:end -->

| Port | Config-schema origin | Notes |
|------|----------------------|-------|
| `clk_audio_i` | `clocking.audio_pll_hz` (24_576_000) | Clean MMCM audio clock; MCLK = /2, SCLK = /8, LRCK = /512 → fs = `audio_pll_hz` / 512. Any other fs (item 6 DRP servo) retunes this clock, not the module. |
| `servo_en_i` | `crf_clk_selected_r` (the live resolve, #74) | Follows the stored AECP clock-source selection: low at INTERNAL (the power-on state - free-run by the standing rule), high when a controller selects the CRF source, arming the MMCM-DRP servo and the packet-grid alignment chain. |
| `wire_chans_i` | wire truth (runtime, from `KL_avtp_rx_monitor`) | NOT config: channels/frame of the last accepted PDU drives the 1-to-1 render mapping regardless of declared formats. |

## Cross-parameter / cross-module pairings (STRICT)

| This parameter | Must pair with | Failure mode when violated |
|----------------|----------------|----------------------------|
| `CLK_FREQ_HZ` | actual `--milan-clk-freq` of the build | ms-tick off by the ratio → convergence window / media-lock timing wrong (silent). |
| `clk_audio_i` frequency | MMCM `audio_pll_hz` = 512 x fs | Audio plays at the wrong rate; FIFO drifts to a permanent under/overrun rail. |
| `SETPOINT_P` | `FIFO_LOG2` (must be < 2^FIFO_LOG2) | Release level unreachable: playback never restarts after a rail event (the prefill hazard the retired `PREFILL_C` row carried, now on the setpoint). |

## Validation

- `board.constraints.milan_clk_hz`, `clocking.audio_pll_hz`: checked by
  `sw/builder/endstation_builder.py` (ConfigError on inconsistency with the
  board table).
- `FIFO_LOG2` / `SETPOINT_P` bounds: UNCHECKED in RTL today (no elaboration
  assert) - flagged for the item-4 parameterization round.

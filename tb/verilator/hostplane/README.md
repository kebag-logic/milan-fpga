<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# `tb/verilator/hostplane` — host-plane lanes in the SILICON SHAPE

> **Historical note.** This suite was born (2026-07-25) on a tree with a live
> silicon regression (host RX dead, zero ts records, every fabric-autonomous
> path perfect) and carried a KNOWN-FAIL banner for the LTAP DEPKT→RING
> same-cycle case. That case was fixed 2026-07-26: `KL_aaf_latency_taps` now
> cascade-walks same-cycle stage pulses (combinational hops like
> `KL_pcm_route` record an honest 0-cycle delta). The suite is expected
> green everywhere.

## Contents

- **[Why this suite exists](#why-this-suite-exists)** — The gap it closes, stated precisely: the wrapper suite proves the *default* shape and its NxN variant asserts only on media lanes, so nothing asserted on host-facing lanes in the elaboration silicon actually ships — which is where a real regression sat while every existing harness stayed green.
- **[Silicon-shape derivation (drift-visible mapping)](#silicon-shape-derivation-drift-visible-mapping)** — A four-column table tracing each ship-config flag through to the parameter this suite pins, so drift has exactly one place to show up. Read the drift notes under it: `milan_soc.py` passes `p_AAF_PLAYBACK` while the SV parameter is `AAF_PLAYBACK_P`, so a playback build would silently never reach the generate.
- **[Cases](#cases)** — Five lettered cases and the claim each owns. D is the interesting one: backpressure the host lane for long windows and the stream must keep flowing byte-exact, with the tap enable knob provably unable to perturb stream data — the behavioural half of a purity claim whose structural half is a synthesis check.
- **[Status on main as of 2026-07-25 (the honest record)](#status-on-main-as-of-2026-07-25-the-honest-record)** — A frozen record, and its failure was fixed 2026-07-26 (see the banner). Worth reading anyway for the reasoning: the host-frame and ts-record cases passing *at datapath level* is what independently exonerated the RTL and pointed the incident at a stale DTB.
- **[Running](#running)** — Two make targets (full run, or build-only as a gate), plus the harness conventions that decide whether your new case works: little-endian byte lanes, and one universal tick pump that the CSR BFM shares so no beat is double-presented while a poll loop spins.

## Why this suite exists

The wrapper-level suite (`milan_dp`) proves `milan_datapath` at the RTL
**default** shape (`N_STREAMS=1`, `PB_PREFILL_C` shrunk for short runs), and
its NxN variant asserts only on the media lanes. Neither asserts on the
**host-facing** lanes (host RX AXIS, ts-record lane) in the elaboration
silicon actually ships — which is exactly where the 2026-07-25 regression
lived while every existing harness stayed green. This suite closes that
class: every case drives the real wiring path of a host lane **with stream
traffic running concurrently**, in the shipped parameterization.

## Silicon-shape derivation (drift-visible mapping)

`sw/litex/build.sh` `cfg_ax8x8` → `milan_soc.py` argv → `Instance("milan_datapath")`
parameters. The suite pins these with `-G` overrides; if the config or the
mapping moves, this table (and the Makefile) is the place drift shows up:

| build.sh cfg_ax8x8 flag | milan_soc.py argv/kwarg | datapath parameter | suite value |
|---|---|---|---|
| `--num-streams 8` | `num_streams=8` | `N_STREAMS` | `8` |
| `--milan-clk-freq 100e6` | `milan_clk_hz=100000000` | `MILAN_CLK_FREQ_HZ` | `100000000` |
| *(no `--audio-interface`)* | `audio_if_slots=0` (`i2s_philips`) | `AUDIO_IF_SLOTS_P` | `0` |
| *(no `--aaf-playback`)* | `aaf_playback=False` (param not passed) | `AAF_PLAYBACK_P` | `0` (SV default) |
| *(no `--no-*` optional-block flag)* | `board.features` all `true` | `MCSERVO_P` `LTAP_P` `MAAP_P` `I2SPB_P` `RXFILT_P` `LPF_P` | `1` each (SV defaults; every tier-1 block PRESENT) |
| *(never emitted by the SoC)* | — | `PB_PREFILL_C` | `0` (SV default — `milan_dp` shrinks it to 2; we keep the silicon value) |
| `--rx-queues 1`, `--strip-probes`, … | SoC-layer only | — | out of scope (no datapath parameter) |

Drift notes observed while deriving the mapping (2026-07-25):

* `milan_soc.py` passes `p_AAF_PLAYBACK` when `--aaf-playback` is set, but
  the SV parameter is named `AAF_PLAYBACK_P` — a playback build would not
  reach the generate. Not part of the shipped `cfg_ax8x8` shape (flag off),
  flagged for the SoC lane; this suite keeps the silicon default (0).
* `KL_pcm_ring_bram.sv` sits in the SoC source list but is not instantiated
  inside `milan_datapath` (SoC-layer `--pcm-ring bram` glue) — excluded here.

## Cases

* **[S] bring-up** — ID/VERSION, station MAC (kl-eth packing), PHC armed,
  the driver's TCAM shield (blacklist the MAAP dynamic pool
  `91:E0:F0:00:xx:xx`, `default_pass=1`), listener stream bound through the
  0x800 window (stage SID → commit CTRL), AAF talker t0 armed (`0x00020003`).
* **[A] host-frame delivery** — broadcast ARP + unicast-to-station + gPTP
  peer-multicast each enter MAC-RX interleaved with bound-stream AAF PDUs;
  all three MUST emerge byte-exact and in order on the host RX AXIS lane,
  the AAF lands on the PCM ring, and the fabric talker keeps emitting.
* **[B] ts-record production** — one 2-beat record per PTP EVENT frame on RX
  (pdelay_req) and on TX through the host DMA port (pdelay_resp), field-exact
  per record contract v2.1
  ([PTP_TS_METADATA_FIX.md](../../../docs/findings/PTP_TS_METADATA_FIX.md));
  general messages (follow_up RX, announce TX) produce none.
* **[C] filter correctness both ways** — bound AVTP never leaks to the host
  lane (shield in force, fabric still consumes); host frames and unknown-sid
  AVTP never leak into the media path; plus a WHITELIST-mode round
  (`default_pass=0` + accept entries) with a foreign unicast dropped.
* **[D] observer purity under stress** — host lane backpressured for long
  windows: shield-dropped stream traffic keeps flowing to the ring in order
  (byte-exact), LTAP telemetry keeps sampling; a wedged host frame delivers
  byte-exact on release with zero loss/reorder behind it; the LTAP enable
  knob provably cannot perturb stream data. Structural half of the purity
  claim: `syn/yosys/check_tap_purity.sh`.
* **[E] cfg-sweep smoke** (`sim_smoke.cpp`) — the case-A/B kernel re-run at
  `small-1x-50MHz` (cfg_arty family), `mid-4x-100MHz`, `tdm8-8x-100MHz`
  (`AUDIO_IF_SLOTS_P=8`). The runtime taps-off variant lives in case D.
  An elaboration-level taps-off parameter **now exists** (`LTAP_P`,
  [AREA_BUDGET.md](../../../docs/design/AREA_BUDGET.md) tier 1, default
  `1` = taps PRESENT) and composes with the runtime knob: `LTAP_P` decides
  whether the block is *built*, `LTAP_CTRL[1]` whether the built block
  *runs*. This suite keeps the silicon default (taps present) and does not
  sweep it; the pruned shape is covered by `tb/verilator/milan_dp`'s
  `obj_prune` build, which elaborates all six tier-1 prunes at once.

## Status on `main` as of 2026-07-25 (the honest record)

First built and run at `7be497d`, re-verified after the `1d1d425` flash-gate
round. Mid-round, the silicon root cause landed on `main`: the host-plane
death was a **stale DTB** (index-mapped `kl,dma-ether` reg windows onto
wrong-but-writable CSRs — see
[TROUBLESHOOTING.md](../../../docs/limitations/TROUBLESHOOTING.md) section
20), i.e. NOT a `milan_datapath` source regression — which is exactly what
this suite's datapath-level results below said independently. The dedicated
`rtl-hostplane-fix` branch was never pushed; the fix landed on `main` as the
DTB/flash gates. Result state on current `main`:

* `Vhostplane_ax8x8` — **51 checks, 1 failure**:

  ```text
  [FAIL] single-frame RX token completes (DEPKT/RING same-cycle) got=0x0 exp=0x1
  info: LTAP_CTRL status after single frame = 0x00007302 (bit12 rx_active, [15:13] awaited stage)
  RESULT: FAIL
  ```

  Root cause (RTL, datapath shape): `KL_pcm_route` is fully combinational,
  so the DEPKT and PCM_RING tap stages pulse on the **same cycle**; the
  `KL_aaf_latency_taps` chain credits one stage per cycle, strands the token
  awaiting RING, and RX samples only advance when the **next** frame's ring
  edge arrives — `LTAP_RX_D2` measures inter-frame gap and the last frame of
  any burst is never sampled (or burns a 0.5 ms timeout). Fix belongs to the
  RTL lane (stage-pulse staging or per-stage pending bits in the chain).
* The host-frame delivery / ts-record / filter cases **pass at datapath
  level in this shape** — independent evidence the silicon regression lived
  outside `milan_datapath`'s RTL (confirmed by the stale-DTB post-mortem
  above). This suite now pins the datapath side shut, and
  `scripts/hostplane_smoke.sh` institutionalizes the board-level diagnosis
  that cracked the incident (`rx_packets`, dma-ts offset, CSR wire-truth).
* All three [E] smoke shapes: `RESULT: PASS`.

The KNOWN-FAIL banner was dropped 2026-07-26 with the `KL_aaf_latency_taps`
same-cycle cascade fix — `make` runs green here (73/73 in the dedicated taps
TB, 51 + 8 in this suite), and the dedicated TB pins the cascade cases
(`cascade *` / `armcascade *` checks).

## Running

```sh
cd tb/verilator/hostplane
make          # build all shapes + run (banner first; nonzero exit on any FAIL)
make build    # elaboration/build only (the "suite BUILDS" gate)
```

Conventions: little-endian byte lanes everywhere (first wire byte in
`tdata[7:0]` — the silicon-proven MAC-side truth); one universal `tick()`
pump drives all AXIS masters and samples all sinks pre-edge, and the CSR BFM
runs on the same tick so no in-flight beat can be double-presented while a
poll loop spins.

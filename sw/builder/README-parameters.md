# README-parameters — endstation builder (`sw/builder/`)

<!-- gaps attack item 4: the software-defined End-Station generator.
     Documents the config schema knobs the builder owns, the hash-derived
     entity_model_id recipe, and the sweep.sh single-source contract.
     Companion of the per-module README-parameters.md files
     (docs/templates/README-parameters.template.md). -->

Module(s): `sw/builder/endstation_builder.py` (generator),
`avdecc/gen_aem_store.py --overlay` (AEM-overlay consumer),
`sw/litex/sweep.sh` (sweep-opts consumer).
Configs: `configs/endstation_*.yaml`
(schema `kebag-logic/milan-endstation-config` 1.1.x; the annotated normative
form is `configs/endstation_arty_current.yaml`).
Gate: `python3 sw/builder/test_builder.py` (10 gates, incl. the ROM
byte-identity no-regression gate).

## Pipeline

```
configs/endstation_<x>.yaml
   └─ endstation_builder.py
        ├─ out/<x>/soc_params.json      milan_soc.py DESIGN argv
        ├─ out/<x>/aem_overlay.json     kebag-logic/aem-overlay 2.x
        │     └─ avdecc/gen_aem_store.py --overlay ...
        │            └─ aecp_aem_rom.svh / aem_golden.h / aem_rom.json
        ├─ out/<x>/build_plan.md        human-readable, "planned" marks
        └─ configs/generated/sweep_opts_<board>.sh   (board-level)
              └─ sourced by sw/litex/sweep.sh (inline tables = fallback)
```

## Schema 1.1 deltas (vs the 1.0 scaffold)

| Field | Type / values | Default | Consumed by | Notes |
|-------|---------------|---------|-------------|-------|
| `audio_interface.cluster_mapping.policy` | `cap-at-interface` \| `cluster-per-stream-channel` | `cluster-per-stream-channel` | overlay emitter (`cluster_layout`) | Replaces 1.0 `rule` (now rejected). `cluster-per-stream-channel`: the stream's `clusters` field verbatim (legacy/pipewire-reference). `cap-at-interface`: per stream `min(clusters, interface channels/direction)` — clusters model real endpoints only. Both generators implemented; 4x4/8x8 examples choose `cap-at-interface`, `arty_current` keeps the deployed legacy layout. |
| `streams.talkers[].clusters` | int 1..32 | `channels` | overlay emitter | SINGLE AUTHORITY for the talker's cluster count (pre-policy). Example configs ship the wire-truth 2 (today's framer RTL is stereo); `arty_current` expresses the deployed legacy-8. |
| `streams.listeners[].clusters` | int 1..32 | `channels` | overlay emitter | Same authority, listener side. |
| `board.constraints.eth_port` | board's `eth_ports` (`ax7101`: `e1`\|`e2`) | absent | soc argv + sweep opts | Multi-PHY boards only (arty rejects it). `ax7101` ships `e2` (e1 GMII-RX hardware fault, 2026-07-22). |
| `entity.entity_model_id` | `hash-derived` \| EUI-64 hex | required | model-id resolution | `hash-derived` = the default path (recipe below); a hex literal stays expressible. |
| `entity.model_id_pin` | EUI-64 hex | absent | model-id resolution | WINS over everything: pins already-flashed silicon to its deployed identity (`arty_current` → `0x001BC50AC1000001`). Remove only with a model-changing reflash. |

## entity_model_id: hash-derived recipe (normative)

Resolution order: `model_id_pin` > `entity_model_id: hash-derived` >
`entity_model_id: <hex literal>`.

1. **shape** = `model_shape(cfg)`: the model-shaping fields ONLY — cluster
   policy; interface kind/channels/word length; sampling rates + current
   rate; CRF sink + format; per-listener channels/formats/clusters/buffer;
   per-talker channels/formats/clusters; the derived per-stream port layout
   (`[base_cluster, clusters, base_map]` per port, both directions). NO
   board flags, names or serials: two boards with the same audio shape share
   one model id (AEM semantics — same model, different instances).
2. **canon** = `json.dumps(shape, sort_keys=True, separators=(",", ":"))`
   (UTF-8).
3. **id** = `(MODEL_ID_OUI << 40) | (int.from_bytes(sha256(canon).digest()[:8], "big") & (2**40 - 1))`
   — top 8 bytes of the sha256, folded under the base EUI-64 prefix
   `MODEL_ID_OUI = 0x001BC5` (Kebag Logic OUI, 24 bits; 40 hash bits).
   Constants live in `endstation_builder.py` and are schema-level: changing
   them (or `model_shape`'s key set) re-identifies every hash-derived model
   — that is exactly what `model_id_pin` protects deployed silicon from.

Properties (test-gated): deterministic (same config → same id),
shape-sensitive (any `model_shape` field change → new id),
instance-insensitive (name/serial/board flags don't change it).

## Per-stream STREAM_PORT layout (overlay 2.x)

USER decision: ONE `STREAM_PORT_INPUT` per listener stream, ONE
`STREAM_PORT_OUTPUT` per talker stream (the CRF sink is a `STREAM_INPUT`
without an audio port). Every port owns

- a contiguous `AUDIO_CLUSTER` block (`base_cluster`, mono MBLA clusters;
  all input blocks precede all output blocks; the physical interface
  channels bind in order to the first clusters per direction — wire-truth
  1-to-1 rule), and
- exactly ONE `AUDIO_MAP` (`base_map`; input ports take map indexes
  `0..L-1`, output ports `L..L+T-1`) whose rows carry cluster offsets
  RELATIVE to the port's `base_cluster` (IEEE 1722.1-2021 §7.2.19).

Descriptor counts follow: `STREAM_PORT_INPUT = L`, `STREAM_PORT_OUTPUT = T`,
`AUDIO_MAP = L + T`, `AUDIO_CLUSTER = Σ per-port clusters`.

## sweep.sh single-source contract

`endstation_builder.py` emits `configs/generated/sweep_opts_<board>.sh` — a
sh fragment defining exactly `OPTS` (the board design-flag prefix:
`--board`, non-default `--sys-clk-freq`, `--milan-clk-freq`,
`--gtx-tx-invert`, `--floorplan`, `--eth-port`) and `L2`. `sw/litex/sweep.sh`
sources the fragment when present and only falls back to its inline case
tables (loudly commented as FALLBACK) when it is absent. The test gate
asserts fragment `OPTS`/`L2` == the inline tables byte-for-byte for both
boards, and `sh -n` on sweep.sh + fragments. The fragment is board-level:
every config of a board emits the same content as long as its
`board.constraints` agree.

## gen_aem_store consumption + current limits

`gen_aem_store.py --overlay out/<x>/aem_overlay.json [--out-dir D]` builds
the ROM/goldens from the overlay through the same `build_model()` used by
the builtin (deployed) shape; for `endstation_arty_current` the emitted
`aecp_aem_rom.svh` is byte-identical to the tracked ROM (THE no-regression
gate). Known single-stream reach, planned item 5 (NxN AAF streams):

- svh validation tables (`AEM_FMTS_C`) cover the FIRST AAF `STREAM_INPUT`'s
  formats only; `WB_STREAM_FORMAT_C` reaches `STREAM_OUTPUT[0]` only.
- a CRF sink is REQUIRED (`AEM_CRF_FMTS_C` cannot be empty).
- the svh consumer RTL (`KL_aecp_*`) itself is single-stream today; NxN
  overlays (4x4/8x8) build structurally valid multi-port ROMs, but nothing
  consumes them in fabric yet.

## Resource estimator (approximate, pre-Vivado)

Every build plan carries a `## Resource estimate` section: per-module
LUT/FF/BRAM36/DSP costs x instance counts from the config, summed against
the xc7a100t budget (63400 LUT / 126800 FF / 135 BRAM36 / 240 DSP;
BRAM36 = RAMB36 + RAMB18/2 equivalents). The cost table
(`RESOURCE_COSTS` in `endstation_builder.py`) is calibrated 2026-07-22
from the REAL hierarchical place report of the shipping Arty build
(`build_arty_eto_milanfinal48`, cross-checked `build_ax7101_eppo_milanfinal38`,
totals within 2.4%); every entry states its provenance row. Confidence
labels, per the area-70 house rule (hierarchical figures mislead for small
modules):

- `measured` - large blocks read straight from the report (cpu subtree,
  soc_infra top leaf incl MAC/DMA/DDR, milan_datapath major children);
- `low` - small-module hierarchical rows, aggregated into `datapath_misc`;
- `UPPER BOUND` - config-scaling rows (per AAF listener/talker engine,
  MAAP claim, ACMP listener context, lwSRP attribute context) charge
  TODAY's single-instance module cost per instance because the NxN
  engines do not exist yet (item 5) - full replication, no sharing;
- `model` - derived, not measured: L2 BRAM = 1 RAMB36 per 4 KB vs the
  64 KB calibration build (32 KB cross-check exact), AEM ROM growth =
  128 B per cluster beyond 16 (tracked ROM = 3653 B / 34 descriptors).

Verdict = worst category vs the part: **OK** (<70%), **TIGHT** (70-80%,
area-70 directive: keep slice headroom), **OVER** (>80%). Calibration gate
(test_builder gate 11): the `arty_current` estimate must land within
+/-15% of the real mf48 place totals, parsed from the report at test time
(SKIPs when the build tree is absent); current deltas are +0.21% LUT /
-0.13% FF / 0% BRAM36 / 0% DSP. The NxN shapes come out OVER on
xc7a100t (4x4 ~108% LUT, 8x8 ~142% LUT, upper bounds) - that is the
point: sizing before burning sweeps.

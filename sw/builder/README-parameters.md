# End-station builder parameters

`endstation_builder.py` turns one `configs/endstation_*.yaml` definition into
the product artifacts consumed by the SoC, protocol processor, firmware, and
verification gates.

The dynamic-map command and persistence claims are checked against the
[Milan feature status ledger](../../docs/reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `soc.baremetal-profile` | `implemented` | - |
| `state.nonvolatile-persistence` | `missing` | - |
<!-- milan-feature-status:end -->

## Contents

- **[Pipeline](#pipeline)** — The generated artifacts and the single configuration source that feeds them.
- **[Product profile](#product-profile)** — The accepted RV32I bare-metal CPU, cache, and flash values.
- **[Platform shape](#platform-shape)** — The processor-memory reservation shared by configuration and gateware.
- **[Optional fabric blocks](#optional-fabric-blocks)** — The supported synthesis-time pruning switches and their dependencies.
- **[Audio and stream model](#audio-and-stream-model)** — Cluster policies, static and dynamic maps, and physical role-pool validation.
- **[Entity identity](#entity-identity)** — Model-ID derivation and the identity facts baked into the descriptor image.
- **[Reservation table and resource estimate](#reservation-table-and-resource-estimate)** — SRP validation and the pre-place capacity warning.
- **[Validation](#validation)** — Commands that check every configuration, generated artifact, recipe, patch, and elaboration.

## Pipeline

```
configs/endstation_<name>.yaml
  └─ endstation_builder.py
      ├─ soc_params.json
      ├─ aem_overlay.json
      │   └─ aem_desc.bin / aem_desc.json / aem_desc.map
      ├─ platform_shape.json
      ├─ gptp_ucode.hex
      ├─ lwsrp_table.json / lwsrp_table.svh
      ├─ build_plan.md
      └─ configs/generated/sweep_opts_<board>.sh
```

The named SoC build places the descriptor image beside the bitstream and binds
the pair by length, CRC32, SHA-256, CPU width, and parsed bitstream identity.

## Product profile

| Field | Accepted value | Meaning |
|---|---|---|
| `soc.software_profile` | `baremetal` | The single firmware contract. |
| `soc.cpu` | `vexiiriscv` | The cacheless product core. |
| `soc.xlen` | `32` | RV32I machine-mode execution. |
| `soc.cpu_count` | `1` | One firmware hart. |
| `soc.full` | `true` | Elaborate the complete bare-metal SoC (`--full`). |
| `soc.scala_args` | `[]` | No cache or supervisor-mode tuning. |
| `board.constraints.l2_bytes` | `0` | No CPU cache. |
| `board.constraints.flashboot` | `none` or `baremetal` | No persistent image, or the bitstream/AEM pair. |

Unknown values and keys are rejected; there are no compatibility aliases.

## Platform shape

`platform:` supplies product identity, filtering posture, and the one memory
placement fact shared with gateware:

| Field | Type | Notes |
|---|---|---|
| `mac_address` | EUI-48 | Required, unicast, and nonzero. |
| `pp_mem_phys` | aligned address | Base of the protocol-processor descriptor window. |
| `rx_address_filter` | `hardware` or `promiscuous` | Whether the fabric filters destination addresses. |

The emitted `platform_shape.json` is schema 2.x and contains only `pp_mem.phys`
and the builder-owned fixed extent, plus provenance metadata. Its real product
consumer is `milan_soc.py`, which derives `PP_DESC_BASE_P` and
`PP_RESP_BASE_P` from that reservation. All other SoC facts come from the SoC's
own generated headers; this artifact does not mirror them. Retired platform
keys fail as unknown input rather than acting as compatibility aliases.

## Optional fabric blocks

The remaining `board.features:` switches are synthesis-time prunes. They
default to present and emit a `--no-*` argument only when disabled.

| Key | Datapath parameter when pruned | Dependency |
|---|---|---|
| `media_clock_servo` | `MCSERVO_P=0` | Only valid with an internal media-clock source. |
| `latency_taps` | `LTAP_P=0` | May be pruned independently. |
| `maap` | `MAAP_P=0` | Requires provisioned multicast addresses. |
| `i2s_playback` | `I2SPB_P=0` | Cannot be pruned when the physical interface needs it. |
| `rx_mac_filter` | `RXFILT_P=0` | Cannot be pruned with hardware filtering selected. |
| `render_lpf` | `LPF_P=0` | Cannot remain when its render consumer is pruned. |

`fabric_gptp` has one product value, `true`. The builder emits
`--fabric-gptp`, generates the per-config microcode image, and records owner
`fabric` in the layout. A fabric-off elaboration is verification-only and is
not represented by a YAML configuration or launcher recipe.

## Audio and stream model

`audio_interface.cluster_mapping.policy` selects one of:

- `cluster-per-stream-channel`: use each stream's declared cluster count;
- `cap-at-interface`: cap clusters at the routed interface width; or
- `role-pools`: compose physical, pilot, loopback, and virtual sources.

Each listener and talker owns one stream port. Static ports own one map with
port-relative cluster offsets. Dynamic ports advertise zero maps and are
served by the live map engine. Every listener is dynamic under the Milan
profile; talkers may be consistently static or dynamic across the image.

`physical_channels.capture` and `physical_channels.render` state the channels
actually routed by the board. Role-pool widths and the `loopback_lane` fabric
fact are validated separately so the model cannot advertise a power-on source
that the built datapath cannot provide.

## Entity identity

`entity.model_id_pin`, when present, wins. Otherwise a literal
`entity_model_id` is used or `hash-derived` folds the canonical model shape
under the Kebag Logic OUI. Instance-only fields such as the station MAC,
serial, and display name do not affect a hash-derived model ID.

The descriptor image bakes the derived entity ID, resolved model ID, stream
counts, capabilities, MAC, and clock identity. No runtime companion file
restates those values.

## Reservation table and resource estimate

`srp:` owns the emitted class-A reservation defaults and derived TSpec. The
builder rejects an invalid VID, queue, multicast base, class, or a total slope
above the configured class bandwidth limit.

Each build plan includes an approximate pre-place resource estimate. It is a
capacity warning, not a timing or placement result; final acceptance still
requires the configured synthesis and implementation sweep.

## Validation

```sh
python3 sw/builder/test_builder.py --require-elaboration
python3 scripts/check_sweep_shape.py
python3 scripts/check_baremetal_only.py --check
```

The builder gate checks every tracked configuration, generated shape, AEM
image, launcher recipe, patch series, and real `milan_datapath` elaboration.

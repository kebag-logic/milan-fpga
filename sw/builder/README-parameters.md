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
| `state.nonvolatile-persistence` | `partial` | - |
<!-- milan-feature-status:end -->

## Contents

- **[Pipeline](#pipeline)** -- The generated artifacts and the single configuration source that feeds them.
- **[Product profile](#product-profile)** -- The accepted RV32I bare-metal CPU, cache, and flash values.
- **[Platform shape](#platform-shape)** -- The processor-memory reservation shared by configuration and gateware.
- **[Optional fabric blocks](#optional-fabric-blocks)** -- The supported synthesis-time pruning switches and their dependencies.
- **[Audio and stream model](#audio-and-stream-model)** -- Cluster policies, static and dynamic maps, and physical role-pool validation.
- **[Entity identity](#entity-identity)** -- Model-ID derivation and the identity facts baked into the descriptor image.
- **[Reservation table and resource estimate](#reservation-table-and-resource-estimate)** -- SRP validation and the pre-place capacity warning.
- **[Validation](#validation)** -- Commands that check every configuration, generated artifact, recipe, patch, and elaboration.
- **[Key reference](#key-reference)** -- Every key with its need, default, limits, refusing check, clause and contract row, generated from the builder.

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

The product is one cacheless RV32I bare-metal core with one hart.
The [`soc`](#soc) and [`board`](#board) rows of the key reference give each accepted value.
The Milan clock is `CPU_HZ` in [recipe.py](../../tb/verilator/nvm_capture_cpu/recipe.py); divergent values refuse.

Unknown values are rejected; there are no compatibility aliases.
The [unknown-key table](#unknown-keys) says, per section, whether an undeclared key is refused or dropped.

## Platform shape

`platform:` supplies product identity, filtering posture, and the one memory
placement fact shared with gateware. The [`platform`](#platform) rows of the
key reference give each key's need, default and refusal.

The emitted `platform_shape.json` is schema 2.x and contains only `pp_mem.phys`
and the builder-owned fixed extent, plus provenance metadata. Its real product
consumer is `milan_soc.py`, which derives `PP_DESC_BASE_P` and
`PP_RESP_BASE_P` from that reservation. All other SoC facts come from the SoC's
own generated headers; this artifact does not mirror them. Retired platform
keys fail as unknown input rather than acting as compatibility aliases.

## Optional fabric blocks

The remaining `board.features:` switches are synthesis-time prunes. They
default to present and emit a `--no-*` argument only when disabled. The
[`board`](#board) rows of the key reference give each prune's flag, its
datapath parameter and the check that refuses a prune another element needs.

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

Every AAF or CRF output requires `internal` in `clocking.media_clock_sources`.
Milan v1.2 5.3.3.6 requires its availability, not its selection.
`default_source: crf` remains valid with both sources available.
Input-only clock loading retains CRF-only support.
Empty source lists raise a named L6 refusal.
`input_stream` adds one INPUT_STREAM source per AAF listener (#629).
The builder emits the classes in one order: INTERNAL, CRF, then listener k.
So CRF is index 1 and listener k is index 2 + k where both lead.
`[internal]` remains valid.
Complete product configurations still require AAF listeners and talkers.

AAF declarations accept only AAF formats; CRF declarations accept only CRF.
Each declared AAF `formats` value must be a list.
Scalar strings, numbers, booleans, nulls and mappings refuse.
Omitting `formats` or declaring `[]` retains derived defaults.
Quote each hexadecimal list entry.
Milan v1.2 5.3.3.4 forbids mixing these families.
Both CRF directions require `0x041060010000BB80` (Milan 7.3.2, Table 7.1).
IEEE 1722.1-2021 Table 7-8 limits each list to 46 formats.
The limit includes derived listener family entries (Milan 6.4).

Every listener `buffer_length_ns` must be an integer, at least `2126000`.
The default equals this Milan v1.2 5.3.3.4 floor.
Values above `0xFFFFFFFF` exceed Table 7-8 and refuse.
Accepted values reach the descriptor without truncation.

Every Stream Output declares `presentation_time_offset_ns`, defaulting to `2000000`.
AAF uses `streams.talkers[]`; CRF uses `clocking.crf_output`.
Other factory values refuse under Milan v1.2 5.3.7.6.
Legal runtime SET_STREAM_INFO values override only their addressed output.
Generated firmware claims exactly the declared output count through MAAP.
AAF_CTRL and MAAP_CTRL reset neutral; firmware supplies active values.

## Entity identity

`entity.model_id_pin`, when present, wins. Otherwise a literal
`entity_model_id` is used or `hash-derived` folds the canonical model shape
under the vendor OUI, `entity.vendor_oui`. Instance-only fields such as the
station MAC, serial, and display name do not affect a hash-derived model ID.

Literal, pinned and hash-derived IDs reject zero and all ones.
A pin cannot hide an invalid literal.
Hexadecimal identity, destination and format values require YAML strings.
Quote `entity_id`, `entity_model_id`, `model_id_pin` and `srp.stream_dmac_base`.
Also quote `platform.mac_address`, `entity.vendor_oui` and `entity.entity_capabilities`.
Quote AAF `formats` entries, `clocking.crf_format` and `clocking.crf_output.format`.
Hexadecimal text is hex digits with an optional `0x` or `0X` prefix.
A single underscore may stand between two digits, as in `"0x001B_C50A_C100_0005"`.
For example, `"1234567890123456"` retains those hexadecimal digits.
The digit count, leading zeros included, must fit the field's width.
`entity.vendor_oui` holds 6 digits, `entity.entity_capabilities` 8, `srp.stream_dmac_base` 12, and the identity and format fields 16.
Signs, leading or trailing whitespace, and leading, trailing or doubled underscores refuse.
YAML numbers and other non-strings receive a named quote instruction.
This includes octal, base-60 integers, booleans and explicit nulls.
A MAC is six two-digit hex octets with one `:` or `-` separator throughout, or twelve digits of hexadecimal text.
For example, `"020000000002"`, `"0x0200_0000_0002"`, `"02:00:00:00:00:02"` and `"02-00-00-00-00-02"` name the same MAC.
Short or unpadded octets such as `"0:2"` and `"2:0:0:0:0:2"`, mixed separators, and an underscore beside a separator refuse.
Unquoted `020000000002` and `10:20:30:40:50:02` refuse before YAML reinterpretation propagates.
The `hash-derived`, `mac-derived` and `maap` selectors remain supported.
Milan v1.2 5.3.3.1 reserves both endpoints for ENTITY.
Section 5.6.2 repeats this rule for ADPDUs.

The descriptor image bakes the derived entity ID, resolved model ID, stream
counts, capabilities, MAC, and clock identity. No runtime companion file
restates those values.

Schema 1.2 (the version the tracked configs declare) added the `names:`
block, `entity.locale`, `entity.vendor_oui` and `entity.entity_capabilities`.
Every one is optional and defaults to what every earlier image carried, so a
config that states none, including any 1.1 config, builds the same image byte
for byte. The [`names`](#names) and [`entity`](#entity) rows of the key
reference give each default and limit. A name or locale is non-empty UTF-8
with no NUL. A `names.clock_sources` name is refused unless the config emits
that source.

Names and the locale are not model-shape inputs, so they never move a
hash-derived model ID. `entity.vendor_oui` is part of the model ID by
construction: changing it re-identifies the entity, and every controller
cache keyed by the old ID misses. A pinned or literal model ID that carries
another OUI refuses the key, as does an OUI outside 24 bits or with the I/G
bit of its first octet set. `entity.entity_capabilities` never chooses a
value: a declaration that differs from
`protocol-processor/hdl/adp/pp_adp_pkg.sv` is refused with that file and
line. `names.clock_sources.stream` names every per-listener Stream Clock
source; with several listeners each name gains ` <k>`, and must still fit.

Three descriptor fields are generator-owned and have no key: AVB_INTERFACE
`interface_flags` (`0x0007`) and `port_number` (the gPTP engine's
`OUR_PORTNUM_C`, `1` today, derived rather than stated), and the IDENTIFY
CONTROL's `reset_time` (`0`: nothing returns that control to its default).
[ENDSTATION_BUILDER.md](../../docs/ENDSTATION_BUILDER.md#3-config-schema--aem-descriptor-mapping)
section 3 rows 33a to 33c state why.

## Reservation table and resource estimate

`srp:` owns the emitted class-A reservation defaults and derived TSpec. The
builder requires startup VID 2 and fixed MRP timer assertions.
The timers are join 200, leave 5000, LeaveAll lower-bound 10000 ms.
Only derived TSpec and one interval frame are supported.
The build budget accepts 1 through 75 percent.
Numeric destination addresses, queue selection and max-frame bytes are legacy scratch.
Live reset admission bits remain distinct from firmware OR-3 boot policy.
[The leaf inventory](../../docs/ENDSTATION_BUILDER.md#3-config-schema--aem-descriptor-mapping) names every consumer.

Each build plan includes an approximate pre-place resource estimate. It is a
capacity warning, not a timing or placement result; final acceptance still
requires the configured synthesis and implementation sweep.

## Validation

```sh
python3 sw/builder/test_builder.py --require-elaboration
python3 scripts/check_sweep_shape.py
python3 scripts/check_baremetal_only.py --check
python3 sw/builder/gen_key_reference.py --check
python3 sw/builder/gen_key_reference.py --selftest
```

The builder gate checks every tracked configuration, generated shape, AEM
image, launcher recipe, patch series, and real `milan_datapath` elaboration.

## Key reference

Generated by [`gen_key_reference.py`](gen_key_reference.py) from the builder
itself; edit [`key_reference.yaml`](key_reference.yaml) for a meaning or a
probe, never the table. The key set is the one `test_builder.py` gate 32
records, with its bound: a key read only on a loader branch that no tracked
configuration takes is not recorded, and gate 32 prints those branches. Each
requirement, default, limit and refusal is probed by loading the reference
configuration with the key removed, set or broken. A refusal is the builder's
own message, cut to one cell.

<!-- key-reference:start (generated by sw/builder/gen_key_reference.py; do not edit) -->
Every key `load_config` reads, 114 in all, probed against `configs/endstation_ax7101_1x1_tdm8.yaml` unless the row says otherwise.
The contract row is the key's row in
[`docs/ENDSTATION_BUILDER.md` section 3](../../docs/ENDSTATION_BUILDER.md#3-config-schema--aem-descriptor-mapping).

### Unknown keys

| Mapping | An undeclared key there is |
|---|---|
| top level | ignored: the key is dropped silently |
| `audio_interface` | ignored: the key is dropped silently |
| `audio_interface.cluster_mapping` | ignored: the key is dropped silently |
| `audio_interface.cluster_mapping.fabric` | refused by `_load_cluster_pools` |
| `audio_interface.cluster_mapping.pools` | refused by `_load_cluster_pools` |
| `audio_interface.physical_channels` | refused by `_load_cluster_pools` |
| `board` | ignored: the key is dropped silently |
| `board.constraints` | refused by `_load_board` |
| `board.features` | refused by `load_features` |
| `clocking` | ignored: the key is dropped silently |
| `clocking.crf_output` | ignored: the key is dropped silently |
| `entity` | ignored: the key is dropped silently |
| `gptp` | refused by `_load_gptp` |
| `names` | refused by `_load_names` |
| `names.clock_sources` | refused by `_load_names` |
| `platform` | refused by `load_platform` |
| `soc` | refused by `_load_soc` |
| `srp` | ignored: the key is dropped silently |
| `srp.timers_ms` | ignored: the key is dropped silently |
| `srp.tspec` | ignored: the key is dropped silently |
| `streams` | ignored: the key is dropped silently |
| `streams.listeners[]` | ignored: the key is dropped silently |
| `streams.talkers[]` | ignored: the key is dropped silently |

### `audio_interface`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `audio_interface.channel_names` | Names for each port channel; never model shape. | optional | absent, clusters are named for their role | a list of non-empty strings, one per channel of the widest physical pool | `_load_channel_names`: audio_interface.channel_names has 2 names but this shape's widest named pool needs 8 | 1722.1 7.2.16, 6.2.2.8 | 16e |
| `audio_interface.cluster_mapping.fabric.loopback_lane` | Build the receive-to-talker loopback lane. | optional | `false` | a boolean; needs loopback clusters | - (any value is read as a boolean) | - | 16d |
| `audio_interface.cluster_mapping.policy` | How AUDIO_CLUSTERs are laid out per stream port. | optional | `cluster-per-stream-channel` | `cap-at-interface`, `cluster-per-stream-channel`, `role-pools` | `_load_interface`: cluster_mapping.policy 'one-cluster' not in ('cap-at-interface', 'cluster-per-stream-channel', 'role-pools') | 1722.1 7.2.16, 7.2.19; Milan 5.3.9.1/5.3.10.1 | 16 |
| `audio_interface.cluster_mapping.pools.loopback` | Loopback clusters per talker port (role pools only). | optional | `0` | an integer; non-zero when the loopback lane is built | `_load_cluster_pools`: cluster_mapping.fabric.loopback_lane is set but pools.loopback is 0: the build would carry the rx -> talker ... | 1722.1 7.2.13, 7.2.16, 7.2.19 | 16b |
| `audio_interface.cluster_mapping.pools.pilot` | One pilot-tone cluster per talker port (role pools only). | optional | `false` | a boolean | - (any value is read as a boolean) | 1722.1 7.2.13, 7.2.16, 7.2.19 | 16b |
| `audio_interface.cluster_mapping.rule` | Retired name of `policy`; declaring it is refused. | optional | absent | none; declaring it is refused | `_load_interface`: cluster_mapping.rule was replaced by cluster_mapping.policy in schema 1.1 (choices ('cap-at-interface', ... | 1722.1 7.2.16, 7.2.19; Milan 5.3.9.1/5.3.10.1 | 16 |
| `audio_interface.kind` | Physical audio interface family. | required | - | `i2s_philips`, `tdm8`, `tdm16`, `tdm32`, `aes3`, `spdif` | `_load_interface`: audio_interface.kind 'adat' not in ['aes3', 'i2s_philips', 'spdif', 'tdm16', 'tdm32', 'tdm8'] | 1722.1 7.2.7 (Table 7-12), 7.2.14, 7.2.3 | 14 |
| `audio_interface.physical_channels.capture` | Capture channels the board really routes. | optional | the interface family's width | zero up to the family's width | `_load_cluster_pools`: audio_interface.physical_channels.capture 9 outside 0..8 (the tdm8 interface width) - a board cannot route ... | - (platform truth; the wire-truth 1-to-1 rule) | 16a |
| `audio_interface.physical_channels.render` | Render channels the board really routes. | optional | the interface family's width | zero up to the family's width | `_load_cluster_pools`: audio_interface.physical_channels.render 9 outside 0..8 (the tdm8 interface width) - a board cannot route ... | - (platform truth; the wire-truth 1-to-1 rule) | 16a |
| `audio_interface.word_length_bits` | Valid sample bits; the slot stays the family's width. | optional | `24` | the family's word lengths | `_load_interface`: word_length_bits 20 invalid for tdm8 (allowed (16, 24, 32)) | 1722 7.3.4 | 15 |

### `board`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `board.constraints.eth_port` | Which Ethernet port the image is built for. | optional | absent, the board's default port | one of the board's ports: `e1`, `e2` on `ax7101`, none on `arty` | `_load_board`: board.constraints.eth_port 'e3' invalid for ax7101 (choices ('e1', 'e2')) | - | 5a |
| `board.constraints.flashboot` | What the QSPI flash boots. | optional | `baremetal` | `none` or `baremetal` | `_load_board`: flashboot 'rom' not none\|baremetal | - | 5a |
| `board.constraints.floorplan` | Apply the board floorplan constraints. | optional | `false` | a boolean | - (any value is read as a boolean) | - | 5a |
| `board.constraints.gtx_tx_invert` | GMII transmit clock inversion knob. | optional | `false` | a boolean; GMII boards only | - (any truthy value is read as true on a GMII board) | - | 5a |
| `board.constraints.l2_bytes` | CPU cache size; the bare-metal product core has none. | required | - | zero only | `_load_soc`: baremetal SoC requires l2_bytes: 0 and no scala_args overrides | - | 5a |
| `board.constraints.milan_clk_hz` | Milan datapath and bare-metal CPU clock. | required | - | only `50000000`, the capture recipe's `CPU_HZ` | `_load_soc`: baremetal clock: milan_clk_hz must be 50000000 Hz ([docs/integration/BAREMETAL_FIRMWARE.md](../../docs/integration/BAREMETAL_FIRMWARE.md) build contract) | - | 5a |
| `board.constraints.num_queues` | Shaper queue count; must equal the RTL's queue count. | optional | `5` | an integer above `srp.class_queue` | `_load_board`: num_queues 9 outside 1..8 | - | 5c |
| `board.constraints.phy` | PHY kind; checked against the board table, not emitted. | required | - | the board's own: `arty` `mii-100`, `ax7101` `gmii-1g` | `_load_board`: board.constraints.phy 'mii-100' contradicts ax7101 (gmii-1g) | - | 5b |
| `board.constraints.sys_clk_hz` | System clock; must not be below the Milan clock. | optional | `100000000` | at least `milan_clk_hz` | `_load_board`: milan_clk_hz must not exceed sys_clk_hz | - | 5a |
| `board.constraints.uart_baudrate` | Console UART rate. | optional | `115200` | an integer | no named refusal: `ValueError` in `_load_board` | - | 5a |
| `board.features.datapath_probes` | Keep the datapath probe registers. | optional | `true` | a boolean; `false` emits `--no-datapath-probes` and sets `DPROBES_P` to zero | `load_features`: board.features.datapath_probes must be a boolean (got 'yes'); true = PRESENT (the default) | - (engineering budget; area-70 directive) | 28 |
| `board.features.fabric_gptp` | The fabric gPTP plane, the product's only time owner. | optional | `true` | `true`; it needs a `gptp:` section | `load_config`: board.features.fabric_gptp: false is retired (#259): the product has NO PHC owner without the fabric plane, ... | Milan v1.2 / 802.1AS ownership; #114/#116 | 29 |
| `board.features.i2s_playback` | Keep the I2S DAC playback path. | optional | `true` | a boolean; the render lane decides which value loads; `false` emits `--no-i2s-playback` and sets `I2SPB_P` to zero | `validate_render_lane`: audio_interface.physical_channels.render 8 exceeds the i2s render lane's 2 crossbar key(s). The render lane ... | - (engineering budget; area-70 directive) | 28 |
| `board.features.latency_taps` | Keep the AAF latency taps. | optional | `true` | a boolean; `false` emits `--no-latency-taps` and sets `LTAP_P` to zero | `load_features`: board.features.latency_taps must be a boolean (got 'yes'); true = PRESENT (the default) | - (engineering budget; area-70 directive) | 28 |
| `board.features.maap` | Keep MAAP; every declared talker needs it. | optional | `true` | `true`; `false`, which would emit `--no-maap`, is refused | `validate_features`: board.features.maap: false removes the allocator required by every declared talker (Milan v1.2 4.3.3.1 and ... | - (engineering budget; area-70 directive) | 28 |
| `board.features.media_clock_servo` | Keep the media-clock servo; pruning needs internal-only clocking. | optional | `true` | a boolean; `false` emits `--no-media-clock-servo` and sets `MCSERVO_P` to zero | `validate_features`: board.features.media_clock_servo: false prunes KL_mmcm_drp_servo, but clocking.media_clock_sources offers ... | - (engineering budget; area-70 directive) | 28 |
| `board.features.render_lpf` | Keep the render low-pass filter; needs I2S playback. | optional | `true` | a boolean; `false` when playback is pruned; `false` emits `--no-render-lpf` and sets `LPF_P` to zero | `validate_features`: board.features: render_lpf is true but i2s_playback is false. KL_pcm_lpf's only consumer is KL_i2s_playback, ... | - (engineering budget; area-70 directive) | 28 |
| `board.features.rx_mac_filter` | Keep the receive MAC filter hardware. | optional | `true` | a boolean; `false` emits `--no-rx-mac-filter` and sets `RXFILT_P` to zero | `load_features`: board.features.rx_mac_filter must be a boolean (got 'yes'); true = PRESENT (the default) | - (engineering budget; area-70 directive) | 28 |
| `board.target` | The board; every constraint is checked against its table. | required | - | `arty`, `ax7101` | `_load_board`: board.target 'nexys' not in ['arty', 'ax7101'] | - | 5 |

### `clocking`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `clocking.audio_pll_hz` | AES3 serial-clock reference; must equal the fabric's audio clock. | optional | `24576000` | only the SoC's `AUDIO_CLK_HZ` | `_load_clocking`: clocking.audio_pll_hz 22579200 is not the audio clock this fabric produces (24576000 Hz, ... | - | 13 |
| `clocking.audio_unit_rates_hz` | AUDIO_UNIT sample rate list; part of the model shape. | optional | the list holding `sampling_rate_hz` | at most `8` distinct base rates, including `sampling_rate_hz` | `_load_clocking`: sampling_rate_hz must appear in audio_unit_rates_hz | 1722.1 7.2.3 | 8 |
| `clocking.crf_format` | CRF STREAM_INPUT format word. | optional | `0x041060010000BB80` | only `0x041060010000BB80`, quoted | `_validate_stream_formats`: clocking.crf_format: CRF format must be 0x041060010000BB80 (Milan v1.2 7.3.2 Table 7.1) | Milan 7.3.2 | 12 |
| `clocking.crf_output.enabled` | The CRF Media Clock Output; required with two or more AAF listeners. | optional; probed on `endstation_ax7101_8x8` | `false` | a boolean | `_load_streams`: 8 AAF listener streams require a CRF Media Clock Output (Milan v1.2 7.2.3) - set clocking.crf_output: ... | CLASS_A (0x0003); domain wiring = the STREAM descriptor's own `clock_domain_index` 0 (7.2.9.2 defines no OUTPUT_STREAM CLOCK_SOURCE type, so the CLOCK_SOURCE/CLOCK_DOMAIN sets are unchanged); ADPDU `talker_stream_sources` +1 and MEDIA_CLOCK_SOURCE in the shape header (`adp_shape`, lines 2302 to 2307); both keys join the model hash. No argv flag carries the key: the overlay's CRF STREAM_OUTPUT becomes `MILAN_CRF_TX_CTRL_BOOT` (`boot_policy.py` line 57), which the firmware writes to `CRFT_CTRL` (`milan_baremetal.c` line 1005): `0x3`, talker enable and class-A declare, when the output is declared, and `0x0` when it is not, so an undeclared output is neither transmitted nor declared (#398). The model half is live and the provisioning half is *planned*: the build plan marks the output `planned (item 5 - NxN AAF streams)` on every config that enables it (`_marks_streams`, lines 3788 to 3795: the CRF STREAM_OUTPUT is advertised and the fabric talker `KL_crf_tx` exists; the stream's provisioning and its ACMP talker context ride with the item-5 NxN integration). **RULE ENFORCED**: >=2 AAF listener streams reject without it, citing Milan 7.2.3 | 27 |
| `clocking.crf_output.format` | CRF STREAM_OUTPUT format word. | optional | `0x041060010000BB80` | only `0x041060010000BB80`, quoted | `_validate_stream_formats`: clocking.crf_output.format: CRF format must be 0x041060010000BB80 (Milan v1.2 7.3.2 Table 7.1) | CLASS_A (0x0003); domain wiring = the STREAM descriptor's own `clock_domain_index` 0 (7.2.9.2 defines no OUTPUT_STREAM CLOCK_SOURCE type, so the CLOCK_SOURCE/CLOCK_DOMAIN sets are unchanged); ADPDU `talker_stream_sources` +1 and MEDIA_CLOCK_SOURCE in the shape header (`adp_shape`, lines 2302 to 2307); both keys join the model hash. No argv flag carries the key: the overlay's CRF STREAM_OUTPUT becomes `MILAN_CRF_TX_CTRL_BOOT` (`boot_policy.py` line 57), which the firmware writes to `CRFT_CTRL` (`milan_baremetal.c` line 1005): `0x3`, talker enable and class-A declare, when the output is declared, and `0x0` when it is not, so an undeclared output is neither transmitted nor declared (#398). The model half is live and the provisioning half is *planned*: the build plan marks the output `planned (item 5 - NxN AAF streams)` on every config that enables it (`_marks_streams`, lines 3788 to 3795: the CRF STREAM_OUTPUT is advertised and the fabric talker `KL_crf_tx` exists; the stream's provisioning and its ACMP talker context ride with the item-5 NxN integration). **RULE ENFORCED**: >=2 AAF listener streams reject without it, citing Milan 7.2.3 | 27 |
| `clocking.crf_output.presentation_time_offset_ns` | Factory presentation time offset of the CRF output. | optional | `2000000` | only `2000000` | `_factory_offset`: clocking.crf_output.presentation_time_offset_ns must be 2000000: Milan v1.2 5.3.7.6 requires a 2 ms factory ... | Milan v1.2 5.3.7.6, 5.4.2.9/.10 | 22a |
| `clocking.crf_sink` | The CRF STREAM_INPUT and its clock source; must agree with `crf` in the source set. | optional | `true` | a boolean; `true` exactly when `media_clock_sources` offers `crf` | `_load_clocking`: media_clock_sources offers 'crf' but clocking.crf_sink is false - the CRF CLOCK_SOURCE is located on that ... | Milan 7.2.2; 1722.1 7.2.9.2 | 11 |
| `clocking.default_source` | Validated against the source set and printed; selects nothing. | optional | the first entry of `media_clock_sources` | a member of `media_clock_sources` | `_load_clocking`: default_source 'word_clock' not in media_clock_sources | 1722.1 7.2.32; Milan 5.3.11.1 | 10 |
| `clocking.media_clock_sources` | The CLOCK_SOURCE set, emitted in class order whatever the listed order. | optional | `internal`, `crf` | a non-empty subset of `internal`, `crf`, `input_stream`; outputs need `internal` | `_load_clocking`: clocking.media_clock_sources: L6 requires at least one source (Milan v1.2 5.3.3.6) | 1722.1 7.2.9, 7.2.9.2, 7.2.32; Milan 5.3.3.6, 7.2.2 | 9 |
| `clocking.sampling_rate_hz` | Current media clock rate of the AUDIO_UNIT. | required | - | one of `48000`, `96000`, `192000` | `_load_clocking`: sampling_rate_hz 44100 not an AAF base rate (Milan v1.2 6.2: [48000, 96000, 192000]) | 1722.1 7.2.3; Milan 5.3.3.3, 6.2 | 7 |

### `entity`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `entity.entity_capabilities` | Declared and verified copy of the ADP engine's capability word. | optional | the ADP engine's `ADP_ENTITY_CAPS_C` | only the ADP engine's `ADP_ENTITY_CAPS_C` | `_verify_entity_capabilities`: entity.entity_capabilities 0x00000000 diverges from ADP_ENTITY_CAPS_C = 0x0000C588 at ... | 1722.1 7.2.1 Table 7-2, Table 6-3 | 3a |
| `entity.entity_id` | Entity identity, expanded from the station MAC or a literal. | optional | `mac-derived` | `mac-derived`, or a quoted `64`-bit hex string | `_hex_text`: entity.entity_id: quote the hexadecimal value as a YAML string | 1722.1 6.2.2.7 | 3 |
| `entity.entity_model_id` | Model identity, hash-derived from the model shape or a literal. | required | - | `hash-derived`, or a quoted `64`-bit hex string, not zero nor all ones | `_model_id`: entity.entity_model_id: entity_model_id must not be zero or all ones (Milan v1.2 5.3.3.1 ENTITY; 5.6.2 ADPDU) | 1722.1 6.2.2.8 | 2 |
| `entity.firmware_rev` | Firmware respin appended to the gateware-derived firmware version. | optional | `0` | a non-negative integer | `_load_entity`: entity.firmware_rev: -1 is not a non-negative integer | 1722.1 7.2.1 Table 7-2 (offset 116, 64 octets), 7.2 (zero padding), 6.2.2.8 | 4b |
| `entity.firmware_version` | Not a key; the version is derived from the gateware. | optional | absent | none; declaring it is refused | `_load_entity`: entity.firmware_version: remove it. The firmware version is derived from the gateware's VERSION parameter ... | 1722.1 7.2.1 Table 7-2 (offset 116, 64 octets), 7.2 (zero padding), 6.2.2.8 | 4b |
| `entity.group_name` | ENTITY group name string. | optional | `""` | at most `63` octets | `_load_entity`: entity.group_name: exceeds 63 bytes (AEM cstr64) | 1722.1 7.2.1, 7.2.11-12 | 4 |
| `entity.locale` | LOCALE identifier. | optional | the descriptor layer's `LOCALE_IDENTIFIER` | at most `64` octets | `_aem_string`: entity.locale: must be a non-empty string | 1722.1 7.2.11 | 4c |
| `entity.model_id_pin` | A fixed model identity that wins over every other source. | optional | absent | a quoted `64`-bit hex string, not zero nor all ones | `_model_id`: entity.model_id_pin: entity_model_id must not be zero or all ones (Milan v1.2 5.3.3.1 ENTITY; 5.6.2 ADPDU) | 1722.1 6.2.2.8 | 2 |
| `entity.name` | ENTITY name a controller shows; never model shape. | required | - | at most `63` octets | `_load_entity`: entity.name: exceeds 63 bytes (AEM cstr64) | 1722.1 7.2.1, 6.2.2.8 | 1 |
| `entity.serial_number` | ENTITY serial number string; per board. | required | - | at most `63` octets | `_load_entity`: entity.serial_number: exceeds 63 bytes (AEM cstr64) | 1722.1 7.2.1, 7.2.11-12 | 4 |
| `entity.vendor_name` | ENTITY vendor name string. | optional | `Kebag Logic` | a string | - (no length check; a longer name reaches the overlay uncut) | 1722.1 7.2.1, 7.2.11-12 | 4 |
| `entity.vendor_oui` | OUI prefix of a hash-derived model identity. | optional | `0x001BC5` | a quoted hex OUI with the I/G bit clear; it must match a pinned or literal identity | `_vendor_oui`: entity.vendor_oui 0x010000 sets the I/G bit of its first octet: that is a group address, not an OUI, and it ... | 1722.1 6.2.2.8 | 2a |

### `gptp`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `gptp.clock_accuracy` | Announced by the fabric engine from a constant; stated only to match it. | optional | the engine's constant | only the fabric engine's value | `_gp_pinned`: gptp.clock_accuracy 77 diverges from the fabric engine's 254: the engine generator consumes only priority1 ... | 1722.1 7.2.8; 802.1AS-2011 8.6.2 | 32 |
| `gptp.clock_class` | Announced by the fabric engine from a constant; stated only to match it. | optional | the engine's constant | only the fabric engine's value | `_gp_pinned`: gptp.clock_class 77 diverges from the fabric engine's 248: the engine generator consumes only priority1 (plus ... | 1722.1 7.2.8; 802.1AS-2011 8.6.2 | 32 |
| `gptp.domain` | gPTP domain number. | optional | `0` | zero only | `_gptp_domain_key`: gptp.domain 1 is not 0: Milan v1.2 section 2 pins 802.1AS-2011, whose 8.1 says 'The domain number of a gPTP ... | 1722.1 7.2.8; 802.1AS-2011 8.1 | 33 |
| `gptp.egress_latency_ns` | Measured board timestamp correction; no default, by design. | required | - | `0` to `65535` | `_gptp_latency_key`: gptp.egress_latency_ns -1 outside 0..65535 ns: the applied pair is published as one read-only CSR word with ... | 802.1AS-2011 8.4.3 / 11.1.2 (ingressLatency, egressLatency); #358, #64 | 33d |
| `gptp.ingress_latency_ns` | Measured board timestamp correction; no default, by design. | required | - | `0` to `65535` | `_gptp_latency_key`: gptp.ingress_latency_ns -1 outside 0..65535 ns: the applied pair is published as one read-only CSR word with ... | 802.1AS-2011 8.4.3 / 11.1.2 (ingressLatency, egressLatency); #358, #64 | 33d |
| `gptp.log_announce_interval` | Announced by the fabric engine from a constant; stated only to match it. | optional | the engine's constant | only the fabric engine's value | `_gp_pinned`: gptp.log_announce_interval 77 diverges from the fabric engine's 0: the engine generator consumes only ... | 1722.1 7.2.8; 802.1AS-2011 8.6.2 | 32 |
| `gptp.log_pdelay_interval` | Announced by the fabric engine from a constant; stated only to match it. | optional | the engine's constant | only the fabric engine's value | `_gp_pinned`: gptp.log_pdelay_interval 77 diverges from the fabric engine's 0: the engine generator consumes only priority1 ... | 1722.1 7.2.8; 802.1AS-2011 8.6.2 | 32 |
| `gptp.log_sync_interval` | Announced by the fabric engine from a constant; stated only to match it. | optional | the engine's constant | only the fabric engine's value | `_gp_pinned`: gptp.log_sync_interval 77 diverges from the fabric engine's -3: the engine generator consumes only priority1 ... | 1722.1 7.2.8; 802.1AS-2011 8.6.2 | 32 |
| `gptp.offset_scaled_log_variance` | Announced by the fabric engine from a constant; stated only to match it. | optional | the engine's constant | only the fabric engine's value | `_gp_pinned`: gptp.offset_scaled_log_variance 77 diverges from the fabric engine's 17258: the engine generator consumes ... | 1722.1 7.2.8; 802.1AS-2011 8.6.2 | 32 |
| `gptp.priority1` | Announce priority1 of the fabric engine; part of the model shape. | optional | `248` | `0` to `255` | `_gp_u8`: gptp.priority1 256 outside 0..255 | 1722.1 7.2.8; 802.1AS-2011 8.6.2.1 | 31 |
| `gptp.priority2` | Announced by the fabric engine from a constant; stated only to match it. | optional | the engine's constant | only the fabric engine's value | `_gp_pinned`: gptp.priority2 77 diverges from the fabric engine's 248: the engine generator consumes only priority1 (plus ... | 1722.1 7.2.8; 802.1AS-2011 8.6.2 | 32 |

### `model_lint_waivers`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `model_lint_waivers` | Processor model-lint waivers, passed through to the packer. | optional | `[]` | a list of waivers the packer validates | - (the builder passes them unread; the packer refuses a bad one) | protocol-processor docs/architecture/07 section 3.1 (model lint) | 45 |

### `names`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `names.audio_unit` | Object name of that singleton descriptor; never model shape. | optional | `Audio Unit` | at most `64` octets | `_aem_string`: names.audio_unit: must be a non-empty string | 1722.1 7.2.2, 7.2.3, 7.2.8, 7.2.22, 7.2.32, 6.2.2.8 | 4d |
| `names.avb_interface` | Object name of that singleton descriptor; never model shape. | optional | `AVB Interface 0` | at most `64` octets | `_aem_string`: names.avb_interface: must be a non-empty string | 1722.1 7.2.2, 7.2.3, 7.2.8, 7.2.22, 7.2.32, 6.2.2.8 | 4d |
| `names.clock_domain` | Object name of that singleton descriptor; never model shape. | optional | `Clock Reference Format` | at most `64` octets | `_aem_string`: names.clock_domain: must be a non-empty string | 1722.1 7.2.2, 7.2.3, 7.2.8, 7.2.22, 7.2.32, 6.2.2.8 | 4d |
| `names.clock_sources.crf` | Object name of that CLOCK_SOURCE class; never model shape. | optional | `CRF Clock` | at most `64` octets | `_aem_string`: names.clock_sources.crf: must be a non-empty string | 1722.1 7.2.9, 6.2.2.8 | 9a |
| `names.clock_sources.internal` | Object name of that CLOCK_SOURCE class; never model shape. | optional | `Internal` | at most `64` octets | `_aem_string`: names.clock_sources.internal: must be a non-empty string | 1722.1 7.2.9, 6.2.2.8 | 9a |
| `names.clock_sources.stream` | Object name of that CLOCK_SOURCE class; never model shape. | optional | `Stream Clock` | at most `64` octets | `_aem_string`: names.clock_sources.stream: must be a non-empty string | 1722.1 7.2.9, 6.2.2.8 | 9a |
| `names.configuration` | Object name of that singleton descriptor; never model shape. | optional | `Default` | at most `64` octets | `_aem_string`: names.configuration: must be a non-empty string | 1722.1 7.2.2, 7.2.3, 7.2.8, 7.2.22, 7.2.32, 6.2.2.8 | 4d |
| `names.control_identify` | Object name of that singleton descriptor; never model shape. | optional | `Identify` | at most `64` octets | `_aem_string`: names.control_identify: must be a non-empty string | 1722.1 7.2.2, 7.2.3, 7.2.8, 7.2.22, 7.2.32, 6.2.2.8 | 4d |

### `platform`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `platform.mac_address` | Station MAC; becomes the entity ID and the gPTP clock identity. | required | - | a quoted unicast non-zero MAC, colon, dash or plain hex | `_mac48`: platform.mac_address: '01:00:00:00:00:01' has the I/G bit set - a station MAC must be UNICAST (it becomes the ... | 1722.1 7.2.8; 802-2014 8.2 | 6a |
| `platform.pp_mem_phys` | Base of the protocol-processor DRAM window. | optional | `0x4FE00000` | a positive, page-aligned address; the window is `0x100000` octets | `load_platform`: platform.pp_mem_phys must be a positive 4 KiB-aligned address | - | 6 |
| `platform.rx_address_filter` | Receive address filter posture at reset and boot. | optional | `promiscuous` | `promiscuous` | `load_platform`: platform.rx_address_filter 'hardware' is unsupported. Migrate hardware to promiscuous: the existing TCAM ... | REQ-MAC-02, REQ-CLS-03 | 30 |

### `schema`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `schema` | Schema identity; anything else is refused before a section is read. | required | - | `kebag-logic/milan-endstation-config` | `_load_document`: configs/endstation_ax7101_1x1_tdm8.yaml: schema must be 'kebag-logic/milan-endstation-config' | - | 0 |

### `schema_version`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `schema_version` | Schema version; the major must match the builder's. | required | - | a version whose major is `1` | `_load_document`: configs/endstation_ax7101_1x1_tdm8.yaml: schema_version 2.0.0 (need 1.x) | - | 0 |

### `soc`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `soc.cpu` | CPU core. | optional | `vexiiriscv` | `vexiiriscv` | `_load_soc`: baremetal SoC requires VexiiRiscv RV32 and one hart | - | 34 |
| `soc.cpu_count` | Firmware hart count. | optional | `1` | `1` | `_load_soc`: baremetal SoC requires VexiiRiscv RV32 and one hart | - | 34 |
| `soc.full` | Elaborate the complete SoC. | optional | `true` | `true` | `_load_soc`: soc.full must be true for the product SoC | - | 34 |
| `soc.scala_args` | CPU generator arguments. | optional | `[]` | `[]` | `_load_soc`: baremetal SoC requires l2_bytes: 0 and no scala_args overrides | - | 34 |
| `soc.software_profile` | Firmware contract. | optional | `baremetal` | `baremetal` | `_load_soc`: soc.software_profile 'hosted' is retired (#259): the product and repository are bare-metal only | - | 34 |
| `soc.timing_opt` | Emit the timing-optimisation flag. | optional | `true` | a boolean | - (any value is passed to the argv decision) | - | 34 |
| `soc.xlen` | CPU word width. | optional | `32` | `32` | `_load_soc`: baremetal SoC requires VexiiRiscv RV32 and one hart | - | 34 |

### `srp`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `srp.accumulated_latency_ns` | Reset value of the accumulated latency register. | optional | `0` | an unsigned integer that fits the register | `load_srp`: srp.accumulated_latency_ns -1 outside 32 bits | IEEE 802.1Q 35.2.2.8.6 | 40 |
| `srp.bandwidth_limit_pct` | Build-time class A budget; not the live admission ceiling. | optional | `75` | an integer up to `75`, and enough for this shape's reservation | `_srp_validate`: srp.bandwidth_limit_pct 76 outside 1..75 (build-time budget, not the live admission ceiling; IEEE 802.1Q ... | IEEE 802.1Q 34.3.1 | 41 |
| `srp.class_queue` | Class A queue select reset value; legacy scratch. | optional | `4` | below `num_queues`; it must fit `3` bits | `_srp_validate`: srp.class_queue 5 >= the board's 5 shaper queues | Queue ownership | 37 |
| `srp.enable_at_reset` | Reset admission bit of the reservation control word. | optional | `false` | a boolean | `_srp_reset_bits`: srp.enable_at_reset must be a boolean (got 2) - it is ONE BIT of the LWSRP_CTRL reset word ... | Milan v1.2 5.3.7.3 | 38 |
| `srp.rtl_table` | This config owns the tracked reservation CSR header. | optional | `false` | a boolean | `_srp_reset_bits`: srp.rtl_table must be a boolean (got 'yes') - it decides whether this config OWNS the tracked generated RTL ... | Builder artifact ownership | 44 |
| `srp.sr_class` | Stream reservation class. | optional | `A` | `A` | `_srp_validate`: srp.sr_class 'B' unknown - Milan v1.2 5.6 defines ['A'] for a Milan end station | Milan v1.2 4.2.7.2.1, 4.3.3.2 | 35 |
| `srp.stream_dmac_base` | Legacy table destination base; MAAP allocates the live addresses. | optional | `0x91E0F000FE01` | `maap`, or a quoted multicast MAC-format hex string | `_srp_dmac`: srp.stream_dmac_base 0x90E0F000FE01 is not a MULTICAST address (I/G bit clear) - an AAF stream DMAC must come ... | Milan v1.2 4.3.3.1, 4.3.5.1 | 39 |
| `srp.talker_declare_at_reset` | Reset talker-declare bit of the reservation control word. | optional | `false` | a boolean | `_srp_reset_bits`: srp.talker_declare_at_reset must be a boolean (got 2) - it is ONE BIT of the LWSRP_CTRL reset word ... | Milan v1.2 5.3.7.3 | 38 |
| `srp.timers_ms.join` | Fixed MRP join timer assertion. | optional | `200` | only `200` | `_srp_validate`: srp.timers_ms.join must be 200: fixed Milan v1.2 4.2.7.1.1 Table 4.3 profile; leaveall names the 10000 ms ... | Milan v1.2 4.2.7.1.1 Table 4.3 | 42 |
| `srp.timers_ms.leave` | Fixed MRP leave timer assertion. | optional | `5000` | only `5000` | `_srp_validate`: srp.timers_ms.leave must be 5000: fixed Milan v1.2 4.2.7.1.1 Table 4.3 profile; leaveall names the 10000 ms ... | Milan v1.2 4.2.7.1.1 Table 4.3 | 42 |
| `srp.timers_ms.leaveall` | Lower bound of the randomized LeaveAll interval. | optional | `10000` | only `10000` | `_srp_validate`: srp.timers_ms.leaveall must be 10000: fixed Milan v1.2 4.2.7.1.1 Table 4.3 profile; leaveall names the 10000 ... | Milan v1.2 4.2.7.1.1 Table 4.3 | 42 |
| `srp.tspec.interval_frames` | TSpec MaxIntervalFrames assertion. | optional | `1` | only `1` | `_srp_validate`: srp.tspec.interval_frames must be 1: Milan v1.2 4.3.3.2 Table 4.4 fixed wire TSpec | Milan v1.2 4.3.3.2 Table 4.4 | 43a |
| `srp.tspec.max_frame_bytes` | Legacy TSpec scratch word; changes neither wire nor budget. | optional | `224` | `1` to `65535` | `_srp_validate`: srp.tspec.max_frame_bytes 0 outside 1..65535 (TSpec MaxFrameSize is 16 bit) | Register map | 43b |
| `srp.tspec.policy` | How the talker TSpec is formed. | optional | `derived` | `derived` | `_srp_validate`: srp.tspec.policy must be derived: the processor uses wire TSpec (Milan v1.2 4.3.3.2 Table 4.4); pinned policy ... | Milan v1.2 4.3.3.2 Table 4.4 | 43 |
| `srp.vid` | Startup SR VLAN identifier. | optional | `2` | only `2` | `_srp_validate`: srp.vid must be 2 at startup: Milan v1.2 4.2.7.2.1; runtime Domain adoption is independent | Milan v1.2 4.2.7.2.1 | 36 |

### `streams`

| Key | Meaning | Need | Default | Allowed and limits | Refused by | Clause | Row |
|---|---|---|---|---|---|---|---|
| `streams.listeners[].buffer_length_ns` | STREAM_INPUT buffer length; part of the model shape. | optional | `2126000` | an integer from `2126000` up to `4294967295` | `_stream_buffer_ns`: streams.listeners[0].buffer_length_ns: must be an integer >= 2126000 ns (Milan v1.2 5.3.3.4 listener buffer ... | 1722.1 7.2.6 (Table 7-8) | 19 |
| `streams.listeners[].channels` | Listener channel count; sets the default current format. | required | - | `1` to `32` | `_streams`: streams.listeners[0]: channels 0 outside 1..32 | 1722.1 7.2.6; 1722 7.3.3; Milan 6.4 | 17 |
| `streams.listeners[].clusters` | Listener AUDIO_CLUSTER count under the legacy policies. | optional | the stream's `channels` | `1` to `32` | `_streams`: streams.listeners[0]: clusters 0 outside 1..32 | 1722.1 7.2.13, 7.2.16, 7.2.19 | 20 |
| `streams.listeners[].formats` | Current format first; the builder derives the rest of the family. | optional | `[]` | a list of quoted AAF format words, at most `46` after derivation | `_streams`: streams.listeners[0].formats: must be a list of quoted hexadecimal strings | 1722.1 7.2.6; Milan 5.3.8.1, 6.2, 6.4, 6.5; 1722 I.2.4 | 18 |
| `streams.listeners[].map_mode` | Listener audio map mode; Milan requires dynamic. | optional | `dynamic` | `dynamic` | `_streams`: streams.listeners[0]: map_mode static is forbidden for a Stream Port Input; Milan v1.2 5.3.3.9 requires ... | 1722.1 7.2.13, 7.2.19; Milan 5.3.3.9, 5.4.2.26-28 | 20a |
| `streams.listeners[].map_page` | Dynamic map scratch page. | optional | absent | `1` to `11` | `_streams`: streams.listeners[0]: map_page 12 outside 1..11 (RTL GET scratch bound) | 1722.1 7.2.13, 7.2.19; Milan 5.3.3.9, 5.4.2.26-28 | 20a |
| `streams.listeners[].name` | STREAM_INPUT name; never model shape. | optional | `Stream In` and the listener's index | a string | - (the name is not length-checked here) | 1722.1 7.2.6, 6.2.2.8 | 17a |
| `streams.listeners[].presentation_time_offset_ns` | Not a listener key; declaring it is refused. | optional | absent | none; declaring it is refused | `_streams`: streams.listeners[0].presentation_time_offset_ns belongs to Stream Outputs, not listener acceptance | Milan v1.2 5.3.7.6 | 22b |
| `streams.talkers[].buffer_length_ns` | Read but dropped; only a STREAM_INPUT carries a buffer length. | optional | `2126000` | any value | - (a talker value reaches no descriptor) | 1722.1 7.2.6 (an input-only field) | 19a |
| `streams.talkers[].channels` | Talker channel count; sets the framer's wire width. | required | - | `1` to `32`; the wire width derived from it is clamped to `2` to `8` | `_streams`: streams.talkers[0]: channels 0 outside 1..32 | 1722.1 7.2.6, 7.4.10.2; Milan 5.3.7.1; 1722 7.3.3 | 21 |
| `streams.talkers[].clusters` | Talker AUDIO_CLUSTER count under the legacy policies. | optional | the stream's `channels` | `1` to `32` | `_streams`: streams.talkers[0]: clusters 0 outside 1..32 | 1722.1 7.2.13, 7.2.16, 7.2.19; Milan 5.3.9.1 | 23 |
| `streams.talkers[].formats` | Talker formats; no family completion. | optional | `[]` | a list of quoted AAF format words | `_validate_stream_formats`: streams.talkers[0].formats: must contain only AAF formats (Milan v1.2 5.3.3.4; AAF/CRF families must not mix) | 1722.1 7.2.6; Milan 6.3 | 22 |
| `streams.talkers[].map_mode` | Talker audio map mode; one mode for every talker. | optional | `static` | `static` or `dynamic`, the same on every talker | `_streams`: streams.talkers[0]: map_mode 'both' not static\|dynamic | 1722.1 7.2.13, 7.2.19; Milan 5.3.3.9, 5.4.2.26-28 | 20a |
| `streams.talkers[].map_page` | Dynamic map scratch page. | optional | absent | `1` to `11` | `_streams`: streams.talkers[0]: map_page 12 outside 1..11 (RTL GET scratch bound) | 1722.1 7.2.13, 7.2.19; Milan 5.3.3.9, 5.4.2.26-28 | 20a |
| `streams.talkers[].name` | STREAM_OUTPUT name; never model shape. | optional | `Stream Out` and the talker's index | a string | - (the name is not length-checked here) | 1722.1 7.2.6, 6.2.2.8 | 17a |
| `streams.talkers[].presentation_time_offset_ns` | Factory presentation time offset of the stream output. | optional | `2000000` | only `2000000` | `_factory_offset`: streams.talkers[0].presentation_time_offset_ns must be 2000000: Milan v1.2 5.3.7.6 requires a 2 ms factory ... | Milan v1.2 5.3.7.6, 5.4.2.9/.10 | 22a |
<!-- key-reference:end -->

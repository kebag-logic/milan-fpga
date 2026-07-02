# AVDECC entity model (IEEE 1722.1-2021 / Milan v1.2)

This directory holds the **AEM entity model** for the Milan endpoint as a single,
tool-agnostic JSON file, plus the notes to turn it into an implementation.

| File | What it is |
|------|-----------|
| [`milan-v12-entity-small-48k.json`](milan-v12-entity-small-48k.json) | **Small baseline** entity: stereo (2-ch) talker+listener, 48 kHz, non-redundant. The scale-from baseline in [`../docs/FR_NFR.md`](../docs/FR_NFR.md). |
| [`milan-v12-entity.json`](milan-v12-entity.json) | **Full/scaled** entity: 8-ch, 48/96/192 kHz. The **single source of truth** for the larger descriptor tree. |
| [`../docs/FR_NFR.md`](../docs/FR_NFR.md) | Functional & Non-Functional Requirements for the Milan v1.2 endpoint, incl. **scale-up / scale-out (multi-softcore)** and the Milan-compliance procedure. |
| [`../aem-and-aecp.md`](../aem-and-aecp.md) / `../aem-and-aecp.pdf` | Prior design of the **FPGA AEM memory (4-level block)** and the **AECP state machines / MVU**. The JSON is the data that design consumes. |

## Why a JSON model

The entity model is *static data* (the descriptor tree) plus a small amount of
*live state*. Rather than hand-code it three times (FPGA memory image, software
entity, and test controller), we keep **one** JSON and generate the rest:

```
                         milan-v12-entity.json
                                  │
        ┌─────────────────────────┼──────────────────────────┐
        ▼                         ▼                           ▼
  FPGA AEM memory           software entity              test controller
  (4-level L0..L3 image,    (PipeWire module-avb /       (avdecc_l2.py,
   aem-and-aecp.md)          la_avdecc descriptors)       tsn-gen READ_DESCRIPTOR)
```

It is a **byte-accurate mirror** of the reference software entity in
`srcs/.../module-avb/entity-model-milan-v12.h` +
`aecp-vendor-unique-milan-v12.h` (entity_id `0xDEAD00BEEF00FEED`, 8-channel AAF +
CRF media clock, manufacturer "Kebag Logic"), so the FPGA and the software
advertise the *same* entity.

**Current scope (per project decision):** a **single configuration**, sample
rates **48 / 96 / 192 kHz** only, and **no seamless redundancy** (single AVB
interface). See the notes below.

## Schema

Top-level keys: `spec`, `avtp_subtypes`, `milan_mvu`, `adp`, `counters`,
`entity`. The `entity` holds the ENTITY descriptor `fields` and a
`configurations[]` array; each configuration has `descriptor_counts` and a flat
`descriptors[]` list addressed by **`(configuration_index, descriptor_type,
descriptor_index)`** — exactly the READ_DESCRIPTOR key and the L1/L2/L3 levels of
the `aem-and-aecp.md` memory.

### Field classes (the important convention)

Every field is one of four **classes** (see `spec.field_class_legend`). A field
written as a bare scalar is `static`; a field written as
`{ "value": …, "class": …, "access": … }` declares its class and the AEM command
that touches it:

| class | storage | example | written by |
|-------|---------|---------|-----------|
| `static` | factory ROM / read-only NVM | `talker_stream_sources`, descriptor topology | never |
| `semi_static` | NVM, provisioned once | `entity_id`, `mac_address`, `serial_number` | build/first-boot |
| `nonvolatile` | writable NVM, persisted | `entity_name`, `current_configuration` | `SET_NAME`, `SET_CONFIGURATION` |
| `dynamic` | volatile mirror | stream `current_format`, `clock_source_index`, IDENTIFY value, gPTP fields, counters | `SET_STREAM_FORMAT`, `SET_CLOCK_SOURCE`, `SET_CONTROL`, gPTP, GET_COUNTERS |

This is the exact split the FPGA design needs: `static`/`semi_static` land in the
read-only factory NVM, `nonvolatile` in the modifiable overlay, `dynamic` in the
volatile mirror that the AECP memory-mapped module updates
(`aem-and-aecp.md` §"Overall Design of the volatile part").

## How to use it

### A. Generate the FPGA AEM memory image
Feed the JSON to a small generator (to be written under `hdl/aecp/` or a
`tools/aem_gen.py`) that emits the L0..L3 memory per `aem-and-aecp.md`:
- **L0** ENTITY + current-configuration/current-entity-id pointers.
- **L1** per-configuration table of descriptor-type addresses (ordered from
  CONFIGURATION).
- **L2** per-descriptor-type tables: `[count, addr(index0), addr(index1), …]`.
- **L3** per-descriptor payloads `[static_size, dynamic_size, payload…]`, with
  `dynamic` fields pointing at the multiplexed register mirror.
Addresses are 16-bit (32-bit via a 16-bit-aligned offset), per the doc.

### B. Cross-check the software entity
`entity-model-milan-v12.h` must stay equal to this JSON. A CI check can parse
both and diff the descriptor values (entity_id, capabilities, stream formats,
counts, strings). When they diverge, this JSON wins and the header is regenerated.

### C. Drive READ_DESCRIPTOR tests
`srcs/the-private-test-repo/controller/avdecc_l2.py` and
`software-defined-tsn-stack/.../aecp/aecp_aem_read_descriptor.yaml` read
descriptors off the wire; this JSON is the expected-value oracle for those tests
(descriptor type codes and counter names already match — see `counters`).

## Stream formats (AAF / CRF)

`current_format` / `formats[]` carry the **raw 8-byte** IEEE 1722-2016 stream
format (authoritative) plus a `decoded` convenience view. **Scope: 48/96/192 kHz
only**, 8-channel, AAF PCM INT-32. Encoding (verified — the 48 kHz value matches
the reference SW byte-for-byte):

| field | bits | 48 kHz | 96 kHz | 192 kHz |
|-------|------|--------|--------|---------|
| subtype (byte 0) | AAF=0x02 | 0x02 | 0x02 | 0x02 |
| **nsr** (byte 1) | 1722-2016 Table 18 | 0x05 | 0x07 | 0x09 |
| format (byte 2) | INT_32BIT=0x02 | 0x02 | 0x02 | 0x02 |
| bit_depth (byte 3) | | 0x20 | 0x20 | 0x20 |
| channels_per_frame | bits[31:22] of bytes 4–7 | 8 | 8 | 8 |
| **samples_per_frame** | bits[21:12], = rate/8000 (Class A) | 6 | 12 | 24 |

- AAF 8-ch: 48 k `0x0205022002006000`, 96 k `0x020702200200C000`, 192 k `0x0209022002018000`.
- CRF media clock (base_frequency = bytes 4–7, low 29 bits): 48 k `0x041060010000BB80`,
  96 k `0x0410600100017700`, 192 k `0x041060010002EE00`. *(CRF `timestamp_interval`
  bytes 1–3 are carried over from the 48 k reference — confirm against IEEE
  1722-2016 CRF if the media-clock packet rate must change with sample rate.)*

The `raw_hex` is normative; `decoded` is informational. Additional channel counts
per rate can be added later (dropped from the earlier 1/2/4/6/8-ch list to keep
scope to the three sample rates).

## Milan v1.2 conformance notes (what makes this a *Milan* entity, not just AVDECC)

- **MVU** (`milan_mvu`): protocol_id `00-1B-C5-0A-C1-00`, `GET_MILAN_INFO`
  returns `protocol_version`, `features_flags` (`MILAN_REDUNDANCY`), and
  `certification_version`. `GET/SET_SYSTEM_UNIQUE_ID` and
  `GET/SET_MEDIA_CLOCK_REFERENCE_INFO` are the other Milan MVU commands.
- **entity_capabilities** include `AEM_SUPPORTED`, `CLASS_A_SUPPORTED`,
  `GPTP_SUPPORTED`, `VENDOR_UNIQUE_SUPPORTED` (raw `0x0000C588`).
- **AVB_INTERFACE** advertises `GPTP_SUPPORTED` + `SRP_SUPPORTED` (Class A / gPTP
  are mandatory in Milan).
- **CRF media clock**: a CRF `STREAM_INPUT` + a `CLOCK_SOURCE` of type
  `INPUT_STREAM` located on it, selectable via the `CLOCK_DOMAIN`.
- **IDENTIFY** CONTROL present and referenced by ADP `identify_control_index`.
- **GET_COUNTERS** exposes the Milan/1722.1-2021 counter sets (`counters`).
- **Redundancy — OUT OF SCOPE for now.** Milan Seamless Network Redundancy (a
  second CONFIGURATION with 2× AVB_INTERFACE + redundant stream pairs) is
  intentionally **not** modeled. This entity is **single-configuration,
  single-interface**, `configurations_count = 1`, `MILAN_REDUNDANCY = 0`. The
  AX7101 has two PHYs, so it can be added later — the JSON's `_redundancy_note`
  records exactly how (append CONFIGURATION[1], bump the count, flip the flag).
- **Sample rates — 48 / 96 / 192 kHz only.** Handled within the single
  configuration via the AUDIO_UNIT `sampling_rates` + `SET_SAMPLING_RATE` and the
  three per-rate AAF/CRF stream formats above.
- **Talker fixed, listener adaptive (Milan v1.2 §5.4).** A **talker** sources a
  **fixed** format (e.g. stereo) — its `STREAM_OUTPUT.current_format`. A **listener**
  MUST be **adaptive**: its `STREAM_INPUT` advertises multiple formats (the Milan
  Base Audio Formats) and its `current_format` is set to the *connected talker's*
  format via `SET_STREAM_FORMAT` at connection — never a fixed single format.
  Confirmed by `module-avb/stream.c` (`stream.c:1244/1512`): the listener re-reads
  the descriptor's `current_format` (which `SET_STREAM_FORMAT` wrote) and matches
  incoming AAF against it. So a listener's `formats[]` MUST have `> 1` entry;
  only the talker's source format is singular.

## Open items to confirm against the Milan v1.2 PDF

1. Exact MVU command codes for `SYSTEM_UNIQUE_ID` / `MEDIA_CLOCK_REFERENCE_INFO`
   (only `GET_MILAN_INFO=0x0000` is confirmed in the reference SW header).
2. ADP `valid_time` per Milan timing (the JSON carries a placeholder; Milan wants
   fast re-advertise).
3. CRF stream-format `timestamp_interval` (bytes 1–3) at 96/192 kHz — the base
   frequency is updated but the interval is carried from the 48 kHz reference.

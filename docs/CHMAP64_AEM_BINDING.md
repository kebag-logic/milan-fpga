<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# chmap64 — AEM dynamic-audio-map → fabric map-word binding contract

The `chmap64` feature adds a **render crossbar** (listener side: incoming AAF
stream channels → physical render/DAC channels) and a **capture mux** (talker
side: physical capture/ADC channels → outgoing stream channels), both
programmed by a small **map RAM**. Each RAM entry is a *map word*:

```
map word  = { en, stream[2:0], ch[2:0] }      // 7 bits
              en      1 = this physical channel is driven
              stream  source stream index      (0..7, the 8x8 lanes)
              ch      source channel in stream  (0..7)
```

The **canonical programmer** of that RAM is the IEEE 1722.1 / Milan dynamic
audio-map command set, not a bespoke register poke. This document is the
normative binding between the two; the executable form lives in
`tests/features/item10_audio_maps.feature` +
`tests/steps/tsn_gen_steps.py::MilanAudioMapModel` (item-10 row
`item-10-audio-maps`, matrix `M-AECP-4`).

## Commands (codes verified against `hdl/ieee17221/aecp/aecp_pkg.sv`)

| Command | `aecp_pkg.sv` | code | Spec | Milan |
|---|---|---|---|---|
| `GET_AUDIO_MAP` | `CMD_GET_AUDIO_MAP = 15'd43` | **0x2B** | §7.4.44 | 5.4.2.26 |
| `ADD_AUDIO_MAPPINGS` | `CMD_ADD_AUDIO_MAPPINGS = 15'd44` | **0x2C** | §7.4.45 | 5.4.2.27 |
| `REMOVE_AUDIO_MAPPINGS` | `CMD_REMOVE_AUDIO_MAPPINGS = 15'd45` | **0x2D** | §7.4.46 | 5.4.2.28 |

> The values are the AEM `command_type` (Table 7.128) — decimal 43/44/45.
> They are **not** 0x1A/0x1B/0x1C; always read `aecp_pkg.sv`, never a comment.

A mapping record (8 bytes on the wire) is
`(stream_index, stream_channel, cluster_offset, cluster_channel)`. Clusters
model the physical channels; per Milan 5.4.2.26 the deployed clusters are
**mono** (one channel each), so `cluster_channel == 0` and the store key is the
`cluster_offset` alone — *at most one dynamic mapping per Audio-Cluster
channel*.

## The projection rule (AEM → map word)

The dynamic map lives on `STREAM_PORT_INPUT[0]` (the render side). The RTL
responder is `KL_aecp_response_builder` under ``` `AEM_DYNMAP ```; the store is
`dmap_v_r[key]` / `dmap_ch_r[key]` with `key = cluster_offset`, sized
`AEM_DMAP_KEYS_C` (generated from the end-station JSON by
`avdecc/gen_aem_store.py`; builder self-test defaults `KEYS=8`, `NMAPS=2`,
`PAGE=4`).

For every mapping record `(si, sc, co, cc)`:

```
address  = co                         // cluster-offset = physical render channel
                                      //   (cc == 0, mono clusters)

ADD    (accepted)  →  RAM[address] = { en=1, stream=si, ch=sc }
REMOVE (matched)   →  RAM[address] = { en=0, stream=0,  ch=0  }
```

Packed: `word = (en<<6) | (stream<<3) | ch`. Example: adding `si=0, sc=3, co=0`
yields `RAM[0] = 0x43` (`en=1, stream=0, ch=3`).

### Validity (ADD, 5.4.2.27 — all-or-nothing)

A record is valid iff **all** hold; any invalid record fails the *whole*
command with `BAD_ARGUMENTS` and **nothing** is written:

| Check | Rule | RTL term |
|---|---|---|
| single audio input | `stream_index == 0` | `w_dm_shape_ok` |
| mono cluster | `cluster_channel == 0` | `w_dm_shape_ok` |
| key in range | `cluster_offset < AEM_DMAP_KEYS_C` | `w_dm_key_ok` |
| channel in format | `stream_channel < channels(STREAM_INPUT[0])` | `w_dm_ch_ok` |
| no intra-command dup | same `cluster_offset` used twice in one command → reject | `dmap_claim_r[key]` |

A valid ADD to an already-mapped key **replaces** it (the 5.4.2.27 accept-and-
replace option). `stream_index` is fixed at 0 in the current single-input build;
the chmap64 8×8 build widens `KEYS` and the `stream` field — the projection rule
above is unchanged.

### REMOVE (5.4.2.28 — lenient)

REMOVE clears an **exact** `(cluster_offset, stream_channel)` match and *ignores*
everything else (unmatched, duplicate); it always returns `SUCCESS` on the input
port. GET then shows the key gone / the word disabled.

### GET_AUDIO_MAP (getter)

`STREAM_PORT_INPUT[0]` pages the live store: `number_of_maps` is the fixed
partition count `AEM_DMAP_NMAPS_C`; each page emits `PAGE` keys, listing the
mapped ones as `(stream_index=0, stream_channel, cluster_offset, cluster_channel=0)`.
`map_index >= NMAPS` → `BAD_ARGUMENTS` (§7.4.44.1). `STREAM_PORT_OUTPUT[0]` is
the static capture map (well-formed, `number_of_maps=1`). Any other
descriptor/index → `NO_SUCH_DESCRIPTOR`.

### Status codes returned (as the RTL actually returns them)

| Situation | Status | value |
|---|---|---|
| accepted ADD/REMOVE/GET | `SUCCESS` | 0 |
| unknown descriptor/index | `NO_SUCH_DESCRIPTOR` | 2 |
| invalid record / dup key / bad map_index | `BAD_ARGUMENTS` | 7 |
| ADD/REMOVE on the static output map | `NOT_SUPPORTED` | 11 |
| locked/acquired by another controller | `ENTITY_LOCKED` / `ENTITY_ACQUIRED` | 3 / 4 |

## Cluster ↔ physical-channel table (I2S 2ch + TDM8 8ch)

The `AUDIO_CLUSTER` descriptors of the end-station
(`avdecc/milan-v12-entity.json`) enumerate the physical channels; the render
crossbar addresses them by flattened `cluster_offset` (mono clusters):

| cluster_offset | physical render channel | interface |
|---|---|---|
| 0 | render L | I2S stereo, ch 0 |
| 1 | render R | I2S stereo, ch 1 |
| 2 | render 2 | TDM8 slot 0 |
| 3 | render 3 | TDM8 slot 1 |
| 4 | render 4 | TDM8 slot 2 |
| 5 | render 5 | TDM8 slot 3 |
| 6 | render 6 | TDM8 slot 4 |
| 7 | render 7 | TDM8 slot 5 |
| … | … | TDM8 slots 6-7 when `KEYS ≥ 10` |

`AEM_DMAP_KEYS_C` is generated to cover the deployed physical channel count
(I2S 2 + TDM8 8 = 10 for the full render; the builder unit-test fixture uses 8).
The capture mux mirrors this on `STREAM_PORT_OUTPUT` (static in the current
RTL: I2S/TDM8 capture channels → outgoing stream channels).

## Arbitration — who owns the map write port

- **The AEM engine owns the map RAM write port.** `ADD`/`REMOVE_AUDIO_MAPPINGS`
  is the authoritative, spec-visible programmer; every accepted edit projects to
  a map word as above, and `GET_AUDIO_MAP` is the read-back of record.
- **The CSR window is a debug-override**, not the normal control path. It exists
  for bring-up / bench pokes and is subordinate to the AEM engine: a controller
  issuing dynamic maps is the source of truth, and any CSR scribble is expected
  to be re-asserted by the next AEM edit / `GET_AUDIO_MAP` reconciliation. Do not
  drive both concurrently in production; the CSR path carries no lock semantics.

## Traceability — `PDU_GETTER_SETTER_VERIFICATION.md` audio-maps row

The item-10 plan doc `docs/testing/PDU_GETTER_SETTER_VERIFICATION.md` is owned
by the sibling open PR `item-10-pdu-getter-setter-verify` and is **not present on
`main`** (this PR's base), so its table cannot be appended here without an
add/add collision. When that PR lands, its AECP/AEM table row

> `GET_AUDIO_MAP + ADD/REMOVE_AUDIO_MAPPINGS | getter + action (es-4.16) | matrix M-AECP-4 | item-10-audio-maps`

is satisfied by this fixture; update its "Existing coverage" cell to
`item10_audio_maps (getter + action + fabric)` and mark the row done.

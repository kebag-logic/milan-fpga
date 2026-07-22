# README-parameters — `<module name(s)>` (TEMPLATE)

<!--
Gaps attack item 4: every leaf module dir carries a README-parameters.md
(this template) + README-tests.md; each spec-family dir (1722 / 1722_1 /
802_1Q / 802_1AS) carries a rolled-up index of both. Filled reference
instance: hdl/avtp/README-parameters.md (KL_i2s_playback).

Fill every section; delete nothing. "Config-schema origin" ties each
parameter to the end-station config (configs/endstation_*.yaml, schema
kebag-logic/milan-endstation-config) so the builder
(sw/builder/endstation_builder.py) composes the module correctly — write
`(builder policy)` for values the builder fixes, `(not yet driven)` for
parameters the config cannot reach yet, and name the exact schema key
otherwise.
-->

Module(s): `<hdl/.../KL_x.sv>`
Instantiated by: `<parent module / milan_soc.py>`

## Parameters

| Parameter | Type / valid range | Default | Set by (instantiation site) | Config-schema origin | Notes |
|-----------|--------------------|---------|-----------------------------|----------------------|-------|
| `<NAME>` | `<int, 2^N, enum…>` + hard limits | `<val>` | `<file:instance, expression>` | `<schema key / builder policy / not yet driven>` | `<what breaks outside the range; area/timing cost>` |

## Derived localparams that matter

| Localparam | Derivation | Why it matters |
|------------|------------|----------------|
| `<NAME_C>` | `<expression>` | `<e.g. divider target, FIFO sizing>` |

## Cross-parameter / cross-module pairings (STRICT)

<!-- Pairs that MUST move together (e.g. hs_page_bytes <-> kl-eth hsplit12).
     One row per pairing, with the failure mode when violated. -->

| This parameter | Must pair with | Failure mode when violated |
|----------------|----------------|----------------------------|

## Validation

<!-- Where the value is checked: builder ConfigError, SV assertion,
     elaboration-time $error, or UNCHECKED (call it out). -->

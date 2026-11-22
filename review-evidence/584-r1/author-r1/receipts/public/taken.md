[A818] TAKEN
Branch: `pf-584-1` at `dd163e41438acb86e0c4d4e76df90f3f91ace1c0` (PR #960's reviewed head); the PR's base is `dev-soft-core` and its diff is this lane's commits only.
Authoritative references: Milan v1.2 5.3.3.7-5.3.3.9 (printed p. 27) and 5.4.2.26-5.4.2.28; IEEE 1722.1-2021 6.2.2.8, 7.2.13, 7.2.16, 7.2.19; this issue's approved design ([proposal](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-5854191783), [approval](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-5854199817), [one-cluster fallback](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-5857155362), [parking](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-5857540091)); the owner's decision of 2026-11-22 (back the input model with the loopback lane and the first TDM render channel only, nothing more); `docs/ENDSTATION_BUILDER.md` D1, D2, D8.
Interpreted scope: every STREAM_PORT_INPUT of every tracked configuration owns at least one mono AUDIO_CLUSTER, derived by the builder from the configuration, with its meaning stated and, where the board routes a sink, backed. The September area and capture STOPs priced the all-fabric processor; on the split placement the descriptors, AECP and saved state are firmware, so this lane gates the split's own budgets (below). Output ports keep their clusters. No input AUDIO_MAP (Milan 5.3.3.9): the builder already refuses a static listener map, so D1's "one AUDIO_MAP per port" text is corrected, not the code.
Validation plan: builder suite and the five-configuration artifact comparison (1x1/1if TDM8 and the three Arty configurations byte-identical); the firmware host suites (AECP, saved state) including the entity-model check and REMOVE_AUDIO_MAPPINGS of a non-empty list on every 8x8 input port; the render-master unit bench and the datapath 8x8 legs (loopback lane off, as shipped, and on); the split saved-state measurement at 8x8 against T_svc and the all-fabric capture against 24.5 ms; the CPU-budget flip check at 8x8/1if (0.75) and 1x1/1if; the control-memory ledger (within the 8x8/1if entry or a recorded debt); an 8x8/1if route on the recipe's three placement directives against #818's floor, best of three, with fit. STOP with the measured cost if it does not fit or close.
Blockers: none.

**DECISION** (this comment carries it; the lane posts one more comment, REVIEW READY or STOP)

Sinks the fabric offers received audio:

| Sink | Selected by an input mapping? | 1x1/1if TDM8 | 8x8/1if today |
|---|---|---|---|
| TDM render lane: the crossbar's 8-key TDM window (keys 2-9) serialized on `tdm.dout` (J11.5) | yes: an input cluster projects onto one render key | built, 8 slots | not built: `render: 0`, `tdm_dout_o` driven low; a TDM32 bus could back only a full 32-slot lane, which the 8-key window cannot |
| loopback lane (depacketizer payload clone into the talkers' `SRC_LOOP` holds) | no: it takes every received stream regardless of input maps; OUTPUT mappings to a talker's loopback clusters select it | built: the talker's 8 loopback clusters carry received stream 0 | not built (`loopback_lane: false`): those clusters carry silence |
| RX monitor and PCM depacketizer consumption | no | built | built |
| stereo I2S DAC | - | pruned (no pads) | pruned (no pads) |

Cluster pool per port, derived by the builder:

- Physical render channels bind in order to the first input clusters of the direction (D2's wire-truth rule, now also under `role-pools`), so one physical channel is never projected from two clusters.
- An input port left with none owns exactly one mono cluster `Unrouted S<p>`: `signal_type` INVALID and `signal_index` 0, as every input cluster here, and no physical projection (the approved fallback).
- The builder refuses either direction's port with zero clusters by name, `STREAM_PORT_CLUSTER_MINIMUM` (Milan 5.3.3.8), with a test; the input exception goes.

| Configuration | Input ports' pools |
|---|---|
| 1x1/1if TDM8 | port 0: 8 physical, `TDM8 Out FL..SR`, unchanged and byte-identical |
| 8x8/1if | port 0: 1 physical, `TDM32 Out 0`, the TDM bus's slot 0 (the first key of the TDM render lane, crossbar key 2); ports 1-7: one `Unrouted S<p>` each. 8 clusters in all, so 8 more writable names and 8 input map keys |
| Arty (three) | unchanged (legacy policies) |

The 8x8 configuration declares `physical_channels.render: 1`, since the AX7101 routes the TDM header (`board_audio_routing.routes_tdm('ax7101')`). That needs fabric. `KL_tdm_render_master` frames the bus's 32 slots, stores only slot 0 and serializes zero in slots 1-31. The datapath and the builder then accept a master render lane narrower than its bus; a slave lane stays full-width. The 1x1 elaborates as before: its lane is its bus's 8 slots.

What a mapping does:

- **8x8 port 0, `TDM32 Out 0`.** ADD of stream channel c at cluster offset 0, channel 0: the firmware stores it, so GET_AUDIO_MAP returns it and saved state keeps it. The face commits it through the EDIT window to input key 0, which projects onto render key 2. The render crossbar then places listener 0's channel c, once per media tick, in slot 0 of the 32-slot frame on `tdm.dout`, 24-in-32 MSB first. REMOVE clears it, and slot 0 renders zero. On Ethernet: the AECP response and the unsolicited notification only, with no AVTP change.
- **8x8 ports 1-7, `Unrouted S<p>`.** The mapping is stored, returned, saved and committed to input key p, whose projection is invalid. No render, monitor, loopback or talker payload changes; that stream's PCM is consumed and discarded as today. On Ethernet: AECP only.
- **1x1.** Unchanged: cluster k is TDM8 slot k.
- **Loopback lane.** No input cluster is named for it, because no input mapping steers it; that is the approved design's rejected alternative. It stays the backing of the output ports' loopback clusters where the build has it.

Identity: the 8x8 `entity_model_id` rotates through the model-shape hash (IEEE 6.2.2.8; #495), and is carried consistently through ENTITY, ADP and the firmware image. The 1x1 and Arty identities and artifacts stay unchanged. The 8x8 model-lint waiver is removed.

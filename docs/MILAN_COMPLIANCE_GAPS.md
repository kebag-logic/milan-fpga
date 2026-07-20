# Milan v1.2 — remaining gaps to FULL compliance

Status date: 2026-07-20, after the dual-board CERT certification
(ARTY 41/41 on `asl_milanfinal33`, ALINX 41/41 on `eto_milanfinal19`).
This file lists ONLY what is still missing or approximate. What already
passes is recorded in `docs/findings/HANDOVER.md` (certification section)
and is not repeated here.

## 1. AECP / AEM

- **GET_DYNAMIC_INFO (0x4B) is NON-CONFORMANT (upgraded from
  "partial" after reading 1722.1-2021 7.4.76, 2026-07-20):** the spec
  defines 0x4B as a BATCH command - the controller packs an array of
  fixed-size GET sub-commands (8-byte record header: len u16, rsvd u16,
  status u8, rsvd u8, command_type u16, then the command's payload) and
  the entity processes each as an independent command. Our response is
  a fixed 116-byte aggregate modeled on the pipewire reference that
  IGNORES the request records - a parsing controller (la_avdecc
  getDynamicInfo) would read garbage. Milan 5.4.2.29 makes 7.4.76
  SHALL. Fix in progress: batch engine in the response builder.
- ~~Dynamic audio maps~~ **RESOLVED AS COMPLIANT (2026-07-20 spec
  read):** Milan v1.2 5.4.2.27/28 requires ADD/REMOVE_AUDIO_MAPPINGS
  only for stream ports **that have no Audio Map descriptor**, and
  REMOVE on a port WITH Audio Maps SHALL return NOT_SUPPORTED. Our
  ports carry static AUDIO_MAP descriptors, and the entity answers
  NOT_SUPPORTED - exactly the specified behavior for this topology.
  Dynamic maps only become mandatory if the static maps are dropped
  (which the future 8ch/dynamic-routing work would do).
- **No-change SET suppression covers only SET_STREAM_INFO and
  SET_CONFIGURATION** (`nochg_q`). A same-value SET_NAME /
  SET_SAMPLING_RATE / SET_CLOCK_SOURCE still replays u=1. Same 1722.1
  state-change rule applies; extend `nochg_q` per command (compare old
  vs new before arming the replay).
- **SET_STREAM_INFO supports only the MSRP_ACC_LAT sub-command**; every
  other spec-defined flag is NOT_SUPPORTED. Milan talker requirements are
  met, but a controller writing e.g. STREAM_VLAN_ID gets refused.
- **Declared capability counts exceed reality.** ADP/AEM advertise
  `talker_stream_sources = 8` and `listener_stream_sinks = 8`, but the
  entity implements ONE talker stream, ONE media listener sink (+ a CRF
  input descriptor with no engine behind it). Strict conformance wants
  the declared counts to match the implemented descriptors — either
  reduce the ADP caps/AEM counts to the real 1–2, or implement the rest.

## 2. Streaming / media

- **CRF media clocking is absent.** The AEM carries a CRF STREAM_INPUT
  descriptor and CRF stream formats in the ROM, but there is no CRF
  talker/listener engine in fabric — the clock domain cannot be driven
  by (or export) a CRF stream. This is the biggest functional gap for a
  "fully compliant Milan end-station" (standing user goal). Today media
  clocking = internal clock, STREAM input recovery, or the gPTP-locked
  servo.
- **Channel width is stereo end-to-end.** The talker framer is hardwired
  2ch (declared truthfully); the listener ACCEPTS 1..8 ch via the
  adaptive monitor, but the I2S playback renders the first 2 channels
  only. Declaring the 8ch input formats is fine per Milan, but a bound
  8ch stream silently plays as its first stereo pair — full support
  needs a channel-select/mixdown or true 8ch render path plus the
  dynamic-map work above.

## 3. SRP (lwSRP)

- **Single-stream engine.** lwSRP declares/handles ONE talker attribute
  and ONE listener attribute. Multiple simultaneous streams (or the
  declared-8) would need per-stream registrar/declaration instances.
- **Class B untested.** The engine and the bench run SR class A only;
  class-B declarations/domain and the 250 µs observation interval have
  never been exercised.

## 4. gPTP

- **es-1.1 / es-1.2 (gPTP + SRP default parameters and timings) were
  never recreated** — linuxptp's defaults are believed conformant but
  are unverified against the official test's tolerances.
- **ingressLatency constants are bench-calibrated** (tap-measured 3511 ns
  Arty / 1490 ns AX; egressLatency 0). A production story needs a
  per-board calibration procedure, and the split between ingress/egress
  was never measured separately — only the sum.

## 5. Robustness items carried as workarounds (not spec gaps)

- **AX GMII link-bounce CDC desync**: recovered by the linkmon software
  self-heal (LINK_CTRL[1] MAC reinit + phy reset). The RTL-level fix —
  decoupling/re-initializing the LiteEth CDC on clock-loss — remains
  owed; until then a link event costs the ~5–20 s recovery path.
- **Arty link detection is an RX-liveness heuristic** (the MII-PMOD MDIO
  floats). No true carrier state; a totally idle-but-up network segment
  would read as link-down after the quiet threshold (gPTP makes this
  practically impossible on an AVB network, but it is a heuristic).
- **CSR config shadow serves stale values across an unnoticed fabric
  reset**; mitigated by the RST_EPOCH canary + daemon reconfig, not
  fixed in hardware (a shadow invalidate-on-reset would be the RTL fix).

## 6. Certification scope

- **Our CERT suite is a recreation, not the official ATL run.** The 13
  behave features cover the commands the official 1299 run exercised
  plus Hive-derived checks; the OFFICIAL plan also includes es-1.1/1.2,
  es-4.1/4.2/4.6/4.11/4.14/4.15/4.16/4.17/4.18 which we implement (all
  but 4.16 dynamic maps) but have not recreated as features. A formal
  Avnu certification (and one clean interactive Hive diagnostics pass)
  is the final word.
- **PipeWire consumer topology** (pw0 as the Milan listener rendering to
  the host audio stack): the milan_listener_* behave features for that
  topology still fail on the pw0 pipewire environment (greeter-session
  pipewire cannot be stopped by the harness). Bench goal, not DUT
  compliance.

## Suggested order of attack

1. CRF engine (listener side first: recover the media clock from a CRF
   stream) — unlocks the "fully compliant" clocking story.
2. Dynamic audio maps (ADD/REMOVE + es-4.16 feature).
3. Honest capability counts (ADP caps + AEM vs implemented streams).
4. GET_DYNAMIC_INFO segment growth to the full record set.
5. Generalize `nochg_q` to all replayed SETs.
6. Recreate the missing CERT features (es-1.1/1.2 first — they only
   need wire observation, no new DUT code).
7. RTL fixes for the workaround items (CDC reinit, shadow invalidate).

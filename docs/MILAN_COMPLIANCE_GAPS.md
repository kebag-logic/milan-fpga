# Milan v1.2 — remaining gaps to FULL compliance

Status date: 2026-07-20, after the dual-board CERT certification
(ARTY 41/41 on `asl_milanfinal33`, ALINX 41/41 on `eto_milanfinal19`).
This file lists ONLY what is still missing or approximate. What already
passes is recorded in `docs/findings/HANDOVER.md` (certification section)
and is not repeated here.

## 1. AECP / AEM

- **GET_DYNAMIC_INFO (0x4B): batch engine IN, silicon re-verify on
  ≥mf39/AX24 (2026-07-20 night).** The 7.4.76 batch semantics landed
  (512 B capture, BSCAN validate/size pass, per-record dispatch through
  the segment engine, NOT_SUPPORTED+echo for legal-unimplemented,
  whole-cmd BAD_ARGUMENTS for illegal/truncated records; byte-exact TB
  vs classic responses). TWO silicon-only defects were then caught by
  the wire probe and fixed: (a) the BSCAN capture race (a4c0630 -
  frame_ok leads the builder's beat consumption; cap_done gate) and
  (b) the cbuf RAM written inside the async-reset engine block - Vivado
  refuses RAM inference (Synth 8-4767) and falls back to flops with
  mangled set/reset priority (Synth 8-7137 "may cause simulation
  mismatches"): silicon read garbage on every record scan while every
  TB passed (empty batch SUCCESS / 1-record 0-for-50 was the
  discriminator). Fixed f3f4b15 (own sync-only write process). mf38 and
  earlier remain non-conformant on 0x4B on silicon.
  **2026-07-21 update: mf39 (cbuf fix in, 8-4767 gone) STILL fails the
  same way** — defect (c): the live suspect is the block-local
  `automatic` temporaries in the scan/parse clocked phases (Vivado
  materializes such locals as sequential elements); hoisted to comb
  wires + BDBG forensics CSRs 0x768-0x770 (latch the scanned header/
  cmd/dlen/ptr at every verdict) ride mf40/AX25 — a still-failing probe
  plus one BDBG read names the mechanism definitively.
- ~~Dynamic audio maps~~ **RESOLVED AS COMPLIANT (2026-07-20 spec
  read):** Milan v1.2 5.4.2.27/28 requires ADD/REMOVE_AUDIO_MAPPINGS
  only for stream ports **that have no Audio Map descriptor**, and
  REMOVE on a port WITH Audio Maps SHALL return NOT_SUPPORTED. Our
  ports carry static AUDIO_MAP descriptors, and the entity answers
  NOT_SUPPORTED - exactly the specified behavior for this topology.
  Dynamic maps only become mandatory if the static maps are dropped
  (which the future 8ch/dynamic-routing work would do).
- ~~No-change SET suppression covers only SET_STREAM_INFO and
  SET_CONFIGURATION~~ **RESOLVED (2026-07-20):** WRITE_S reads the old
  store byte before writing (2-phase) and `wb_diff` gates the u=1
  replay for every replayed SET (NAME/SAMPLING_RATE/CLOCK_SOURCE/
  STREAM_FORMAT beyond the original two).
- **SET_STREAM_INFO supports only the MSRP_ACC_LAT sub-command**; every
  other spec-defined flag is NOT_SUPPORTED. Milan talker requirements are
  met, but a controller writing e.g. STREAM_VLAN_ID gets refused.
- ~~Declared capability counts exceed reality~~ **RESOLVED
  (2026-07-20):** S50 provisions honest ADP counts (talker sources 1,
  listener sinks 2 = media + CRF; 0x618/0x61C) and the ENTITY
  descriptor overlays follow the same values.

## 2. Streaming / media

- **CRF media clocking: the measurement half is IN (2026-07-20).**
  KL_crf_rx validates the Avnu Pro Audio CRF stream (Milan 7.3.2:
  subtype 4/type 1/pull 0/48k/interval 96/1 ts) selected by CSRs
  0x738-0x74C, and produces the phase delta (0x744, ts_delta contract),
  the 512-ms frequency error (0x748), lock state + CLOCK_DOMAIN
  LOCKED/UNLOCKED events (muxed in when clock_source = CRF descriptor
  2). **The talker half is IN too (2026-07-20 night, USER-requested):**
  KL_crf_tx sources the Avnu Pro Audio CRF stream (500 PDU/s, one
  gPTP-ns timestamp per PDU captured on the REAL audio-MMCM 96-sample
  event grid — the wire carries the true media-clock rate), CSRs
  0x750-0x764 {en, sid, dmac, RO count}, 6th low-rate control-merge
  source; S50 provisions the ALINX with DMAC = MAAP claim+1 on
  gateware >= 0x0005. Rx silicon-proven against a synthetic pw0 source
  (lock, 13000/13000 counted, rate-from-field, timeout unlock);
  board-to-board e2e = the AX24/mf39 wire test.
  **The sink-1 bind SM is IN (2026-07-21, b692395):** listener uid=1 is
  a real bind record (fast-connect sid/dmac, {eid,tuid} fallback), the
  datapath drives the CRF engine's en/sid from the bind, GET_RX_STATE/
  GET_STREAM_INFO(input 1) reflect it (dp-TB closure: CONNECT_RX →
  lock on the bound sid → DISCONNECT cuts); silicon verify rides
  mf40/AX25.
  REMAINING for the full chain: a second lwSRP listener attribute for
  the CRF reservation (until then the CRF stream rides untagged
  best-effort — an SR-tagged unregistered stream is pruned to zero
  ports by the bridge), and the **clock-recovery ACTUATOR: the
  clean-clock rework retired the playback NCO (trim_o = 0) in favour of
  a future MMCM-DRP servo — that DRP engine (audio-MMCM fractional
  reprogramming steered by CRF_DELTA/RATE at clock_source==2) is the
  remaining hardware; measurement, bind and CLOCK_DOMAIN counter muxing
  are all in place.**
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
  never recreated** — linuxptp's defaults are believed conformant
  (checked 2026-07-20 against the official es-1.1 text: announce 0,
  sync -3, pdelay 0 all match) but the timing tolerances are unverified.
  **BLOCKED ON THE BENCH SWITCH**: es-1.1 requires the DUT to win the
  BMCA against a 255-claimant test machine and free-run its Announce/
  Sync cadence; our switch claims priority1=246 clockClass=248
  clockAccuracy=0x20 (tap-read) and outranks every Milan-legal
  end-station value (246|248 tie loses on clockAccuracy). Until the
  switch's gPTP claim is weakened (mgmt ssh at 192.168.127.1), the
  recreation cannot run and the bench ships the 100 override to keep
  the ALINX-GM one-oscillator media architecture. **The shipping
  priority1 for certification must be 246** (Milan es-1.1; 100 is
  bench-only).
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
- **Synthesis-style landmines (2026-07-20 cbuf lesson):** `fword_r`
  (KL_acmp_responder) and `nochg_q` (response builder) draw the same
  Vivado Synth 8-7137 "set/reset same priority - may cause simulation
  mismatches" warning that broke cbuf_r on silicon; both happen to be
  silicon-proven today. Standing gate: any RAM-like array must live in
  its own sync-only process, and every new build log gets
  `grep "Synth 8-4767"` - a hit on our modules means Vivado refused RAM
  inference and the fallback semantics are suspect.

## 6. Certification scope

- **Our CERT suite is a recreation, not the official ATL run.**
  **2026-07-21: the recreation gap is closed to this bench's limits** —
  es-4.1/4.2/4.6/4.11/4.14/4.15/4.17/4.18 are now features (suite 43 →
  63 scenarios; ARTY mf39 = 61/61 + the 2 tap features green), es-1.1's
  ALINX-GM half (tap-measured cadences + announce fields) and es-1.2's
  SRP wire half (Domain {A,3,2}) are features too. Still not recreated:
  the es-1.1/1.2 DUT-wins-BMCA/marker variants (gated on weakening the
  bench switch's gPTP claim — user credentials) and es-4.16 (dynamic
  maps — NOT_SUPPORTED by design with static maps, see §1). A formal
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

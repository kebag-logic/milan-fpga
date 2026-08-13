# Minimal Milan v1.2 talker — ACMP state machine + AECP streaming (design)

Reference truth (measure-don't-assume): every behavior below was extracted
from the pipewire module-avb Milan v1.2 implementation (the project's
normative reference) — `acmp-cmds-resps/acmp-milan-v12.c`,
`aecp-aem-cmds-resps/cmd-get-set-stream-info.c`, `cmd-start-stop-streaming.c`,
`cmd-register-unsolicited-notifications.c`, `reply-unsol-helpers.c`,
`stream.c` — plus the reservation gating contract the SRP plane publishes.
Wire message types are IEEE 1722.1-2021; semantics are Milan v1.2.

> **WHO OWNS THIS STATE MACHINE NOW (2026-08-13).** The talker connection SM
> described here is no longer this repository's RTL. `KL_acmp_responder`,
> `KL_acmp_tlkr_ctx` and `acmp_pkg.sv` are **DELETED**; the talker half of
> ACMP is `KL_acmp_talker` inside the pinned `protocol-processor` submodule
> (architecture of record v2.0), wrapped for this fabric by
> [`hdl/milan/KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv) and
> instantiated unconditionally by
> [`hdl/milan/milan_datapath.sv`](../../hdl/milan/milan_datapath.sv). There is
> no parameter, no fallback and no shadow arm.
>
> **The AECP half of this page moved to the processor's µCPU, which has now
> LANDED.** An earlier revision of this banner said this entity answers no
> AECP command at all. That is no longer true and the correction matters: the
> submodule's AECP µCPU is in, the AECP pop face is live, and the entity
> **answers `READ_DESCRIPTOR`** — `SUCCESS` with the configuration index, the
> reserved field and the descriptor; `NO_SUCH_DESCRIPTOR` on a locate miss;
> `BAD_ARGUMENTS` on a bad configuration index, both errors carrying the
> IEEE 1722.1 §7.4.5 4-byte `{descriptor_type, descriptor_index}` stub. It also
> answers **every other AECP command — every other opcode, and AA and MVU
> alike — with a conformant `NOT_IMPLEMENTED` echo**: right `message_type`,
> right length, right `controller_data_length`. Never silence, never malformed.
> Two inputs are refused silently by design: a command whose `target_entity_id`
> is not ours, and any AECP *response* arriving as input. And an
> `IDENTIFY_NOTIFICATION` arriving as a command is `BAD_ARGUMENTS` — the
> opcode-specific rule of §7.4.39.2 beats the generic §9.3.5.3.3 path.
>
> So this entity discovers over ADP, connects over ACMP, reserves over SRP, and
> **can be enumerated over AECP** — once a descriptor image is in DRAM, which
> nothing in this repository builds or writes yet (see below). What it still
> does not do, image or no image, is any of the
> talker-facing AECP *functions* in the matrix below. Every one of those rows
> stays **NOT IMPLEMENTED**, because an echo is not an implementation: no
> GET/SET_STREAM_INFO, no START/STOP_STREAMING status, no unsolicited
> notifications, no SET_MAX_TRANSIT_TIME. One known gap belongs here too —
> Milan Δ7 `ACQUIRE_ENTITY` is **not** distinguished from the generic echo, so
> a controller gets `NOT_IMPLEMENTED` instead of the `NOT_SUPPORTED` with
> `owner_id` = 0 that Milan asks for. Read the page as the *behavioural
> contract* the connection model rests on, with each section's status marked.
>
> The descriptors those reads return are an image in DDR3 at a **compile-time
> base** — no base register, not relocatable at runtime; the LiteX SoC derives
> the base as the top 1 MiB of `main_ram`. Software must load the image
> **before enabling the entity**; otherwise every `READ_DESCRIPTOR` answers
> `BAD_ARGUMENTS`. **On a stock build of this repository that is exactly
> what happens**, and it is worth naming why rather than assuming a pipeline:
> the image generator lives in the `protocol-processor` submodule, and no step
> in `sw/builder/`, `scripts/`, the LiteX SoC builder or the boot path turns an
> `endstation_*.yaml` into the generator's JSON or writes the resulting image
> to DRAM. The `aecp_aem_rom.svh` that `endstation_builder.py` still emits is
> an orphan of the deleted `KL_aecp_aem_store`, not this image. A zeroed region
> reads as *image not loaded* — the header magic `"AEMI"` fails to compare
> before version or checksum matter — the store's watchdog abandons a stalled
> burst instead of hanging, and a late load heals **without a reset**, because
> every locate against an invalid image re-arms the header probe.

## Contents

- **[The Milan v1.2 talker connection model (what surprised us)](#the-milan-v12-talker-connection-model-what-surprised-us)** — The finding that shaped the whole design: `CONNECT_TX` *is* Milan's PROBE_TX, so the talker keeps almost no ACMP state. It activates on the first probe, re-arms a 15 s window on each one, always answers `connection_count = 0`, and treats DISCONNECT_TX as a SUCCESS that changes nothing. Still the model the processor implements.
- **[Command/response matrix (talker-relevant)](#commandresponse-matrix-talker-relevant)** — Per-message guard and exact response for the four ACMP messages, then the AECP commands Milan changes — every one of which this build answers with a well-formed `NOT_IMPLEMENTED` echo and none of which it implements. Includes the `stream_id = {station_mac, unique_id}` formula and the defect it corrected.
- **[Activation state machine (the processor's KL_acmp_talker)](#activation-state-machine-the-processors-kl_acmp_talker)** — What the fabric can still observe: `acmp_declaring_o` per source, which IS the talker-active level, and the fact that `PROBE_ARMED` has become a **structural zero** because the processor publishes no equivalent.
- **[AAF gate (milan_datapath)](#aaf-gate-milan_datapath)** — The one-line gate expression, unchanged in shape, and where its terms come from now: the DA gate lives inside `acmp_declaring_o` (an ALLOC_DA success through `KL_pp_maap_shim`), the reservation term comes from the processor's class-D SRP face.
- **[CSR additions](#csr-additions)** — `AAF_CTRL[1]`, `ACMP_TALKER 0x66C`, `ACMP_LOBS 0x670`, and which bits of `0x66C` are live versus structurally zero after the substitution.
- **[Explicitly out of scope (this increment)](#explicitly-out-of-scope-this-increment)** — Historical, and banner-corrected twice: items that landed, and items that landed and have since been deleted.
- **[Gates](#gates)** — What each tier proved, what can no longer be proved here because the RTL it tested is gone, and the slice of the AECP drill that is testable again now that enumeration answers.

## The Milan v1.2 talker connection model (what surprised us)

Milan v1.2 does NOT use CONNECT_TX as talker-side connection bookkeeping.
The talker is **near-stateless in ACMP**:

- `CONNECT_TX_COMMAND` **is** Milan's `PROBE_TX_COMMAND` (§4.3.3.1, §5.5.4.1):
  the listener probes the talker for stream parameters. The talker ACTIVATES
  its stream source on the first probe and re-arms a **15 s freshness
  window** on every probe.
- The talker DEACTIVATES only when BOTH conditions lapse: no probe in 15 s
  AND no SRP Listener attribute registered for the stream (periodic sweep).
- `connection_count` in every talker response is **always 0** (the reference
  hard-codes it; listeners/controllers derive connection state elsewhere).
- `DISCONNECT_TX_COMMAND` (§5.5.4.2): always SUCCESS, zeroed stream fields,
  NO state change (not even deactivation).
- `GET_TX_CONNECTION_COMMAND` (§5.5.4.4): NOT_SUPPORTED for talkers.

This model is unchanged by the substitution — it is what `KL_acmp_talker`
implements. What changed is which module holds it.

## Command/response matrix (talker-relevant)

### ACMP (multicast 91:E0:F0:01:00:00, subtype 0xFC, 70 B frames) — SERVED

| Wire message (in) | Milan meaning | Guard | Response |
|---|---|---|---|
| CONNECT_TX_COMMAND (0) | PROBE_TX | talker_guid==EID else IGNORE; unique_id!=0 -> TALKER_UNKNOWN_ID | CONNECT_TX_RESPONSE (1), SUCCESS: live stream_id/dmac/vlan, count=0, clear FAST_CONNECT+STREAMING_WAIT flags; side effect: the source declares (`acmp_declaring_o`) and the freshness window re-arms |
| DISCONNECT_TX_COMMAND (2) | unbind notification | same guards | DISCONNECT_TX_RESPONSE (3), SUCCESS, stream fields ZERO, count=0; NO state change |
| GET_TX_STATE_COMMAND (4) | state query | same guards | GET_TX_STATE_RESPONSE (5), SUCCESS: live stream_id/dmac/vlan, count=0, clear FAST_CONNECT+STREAMING_WAIT+SRP_REG_FAILED |
| GET_TX_CONNECTION_COMMAND (6) | n/a for talkers | — | NOT_SUPPORTED echo |

Live stream parameters (single source of truth — MUST byte-match the AVTP
frames the AAF talker emits):
- `stream_id = {station_mac[47:0], talker_unique_id[15:0]}` — the reference
  formula (stream.c: mac<<16|index) and exactly what the AAF talker puts on
  the wire (`{station_mac_i, 16'd0}` at uid 0).
  **BUG FIXED BY THIS WORK: the old GET_STREAM_INFO reported
  stream_id = entity_id (02:00:00:FF:FE:...), which can NEVER match the
  AVTP stream — a listener binding on it would fail.** The fix is historical in
  the sense that GET_STREAM_INFO is no longer implemented (it draws the
  `NOT_IMPLEMENTED` echo, see below), so the defect has no wire to appear on.
  The formula itself still governs: it is what the framer emits and what the
  processor's ACMP responses carry.
- `stream_dest_mac` = the address MAAP allocated for that source, resolved
  through [`hdl/milan/KL_pp_maap_shim.sv`](../../hdl/milan/KL_pp_maap_shim.sv)
  out of the one `KL_maap` block claim; `stream_vlan_id` = the operational
  VID the SRP domain adopted (`A_AAF_CTRL[27:16]` remains the static lever
  when MAAP/SRP are off). The framer reads the same values; there is no
  second copy.

### AECP additions/corrections (Milan §5.4.2) — **NOT IMPLEMENTED**

Every row below was designed, and most of them shipped, against
`hdl/ieee17221/aecp/**`. That whole tree is deleted and the processor's µCPU
did not reimplement any of these functions, so the status column records what
the entity *would* owe a controller, not what it does. What a controller
actually sees is the µCPU's conformant `NOT_IMPLEMENTED` echo — a well-formed
answer at the right length with the right `controller_data_length`, which
satisfies IEEE 1722.1 §9.3.5's duty to respond and satisfies nothing else.
**Do not read the echo as coverage**: none of the behaviour in the "Milan
rule" column happens.

| Command | Milan rule | Status in this build |
|---|---|---|
| GET_STREAM_INFO (STREAM_OUTPUT) | §5.4.2.10.2, Tables 5.11/5.12: fixed 56 B payload; flags STREAM_FORMAT_VALID\|CONNECTED\|MSRP_ACC_LAT_VALID\|STREAM_ID_VALID\|STREAM_DEST_MAC_VALID\|STREAM_VLAN_ID_VALID always 1 (0xF6000000); pbsta=acmpsta=0; flags_ex.REGISTERING = declaring && listener_observed | **NOT IMPLEMENTED.** The same live values are readable over the CSR plane (`A_ACMP_TALKER 0x66C`, the `0x800` stream window, the `0x680` SRP group) — over ssh, never over the wire |
| SET_STREAM_INFO (STREAM_OUTPUT) | §5.4.2.9: ONLY the MSRP_ACC_LAT_VALID sub-command is supported; while listener_observed -> STREAM_IS_RUNNING; range 0..0x7FFFFFFF else BAD_ARGUMENTS | **NOT IMPLEMENTED.** With `SET_MAX_TRANSIT_TIME` and this sub-command both unimplemented — echoed, never executed — the presentation-time offset is **pinned at the Milan 2 ms default** for every Stream Output. That is a DEFAULT, not a zero: 0 ns would be a presentation time in the past and every listener would drop every frame as late |
| SET_STREAM_INFO (STREAM_INPUT) | not implemented for inputs | NOT IMPLEMENTED (as is everything else) |
| START_STREAMING / STOP_STREAMING | §5.4.2.19/20: Stream-INPUT-only commands; **NOT_SUPPORTED on Stream Outputs** | **NOT IMPLEMENTED.** Milan 5.3.7.3 forbids stopping a Stream Output anyway, so nothing in the media path regressed — but the required *status* is not emitted either |
| REGISTER_UNSOLICITED_NOTIFICATION | §5.4.2.21: dedup by controller_id -> SUCCESS; table full -> NO_RESOURCES | **NOT IMPLEMENTED.** No registration table exists |
| DEREGISTER_UNSOLICITED_NOTIFICATION | clear the slot -> SUCCESS | **NOT IMPLEMENTED** |
| Unsolicited pushes | on stream-output state change, send a full GET_STREAM_INFO response, u=1, UNICAST per registered controller with its own sequence_id++ | **NOT IMPLEMENTED**, and with it the whole Milan Table 5.22 push duty. A controller would learn of a state change only by polling, and the poll (GET_STREAM_INFO) is unimplemented too — enumeration reads the model, not the live stream state |

## Activation state machine (the processor's `KL_acmp_talker`)

```
                 probe (valid PROBE_TX for this source's uid)
   IDLE ────────────────────────────────────────► DECLARING
    ▲     freshness window := 15 s                  │ probe -> re-arm
    │                                               │
    └── window expired && no Listener registered ───┘
```

- **`acmp_declaring_o[src]` IS the talker-active level.** `milan_datapath`
  assigns `acmp_talker_active_v = pp_cd_acmp_declaring_w` and consumes it
  every clock off the class-D face — no side-port read transaction, no
  software pacing.
- **`PROBE_ARMED` is a STRUCTURAL ZERO.** It was the legacy SM's "a probe
  window is open" level and its only reader was a forensics word; the
  processor publishes no equivalent through the class-D face, so
  `milan_datapath` ties it to 0 rather than inventing a plausible value. It
  reads 0 in the `0x648` AECP/ACMP status group and at `A_ACMP_TALKER`
  `0x66C[0]` — a *structural* zero, not "no probe seen".
- `listener_observed` is still an input to the composed gate, but its real
  source is now the processor's SRP Listener declaration state
  (`pp_cd_srp_lstn_decl_state`), with `A_ACMP_LOBS 0x670[0]` kept as the
  manual override socket for the bench.

## AAF gate (milan_datapath)

```
aaf_gate = cfg_aaf_enable & (~cfg_maap_enable | maap_addr_valid) &
           (cfg_aaf_bypass |
            (acmp_talker_active & (~cfg_lwsrp_enable | srp_admitted[0])))
```

- **The DA gate is the talker gate.** `acmp_declaring_o` asserts only after a
  MAAP `ALLOC_DA` success through `KL_pp_maap_shim`, so the composed
  admission above is still exactly *"a destination address exists AND the
  source is declaring"* — the same decision, made once, inside the plane that
  owns it instead of twice in this file.
- `cfg_aaf_bypass` (`A_AAF_CTRL` bit 1) **resets to 1** = stream-whenever-
  enabled, the legacy escape hatch for flash-boot benches; probe-gated
  transmit is opt-in until the flow is silicon-proven on a given build.
- The talker's `TRANSIT_NS` is the presentation-time offset, and with
  SET_MAX_TRANSIT_TIME gone it holds the **Milan 2 ms default** for the life
  of the build (see the AECP matrix above).

## CSR additions

- `A_AAF_CTRL[1]` = bypass (reset 1). `[0]` enable unchanged.
- `A_ACMP_TALKER = 0x66C` (RO): `{aaf_gate, listener_observed, talker_active,
  probe_armed}` in bits `[3:0]`. After the substitution: `[0] probe_armed` is
  a **structural zero**, `[1] talker_active` is **live**
  (`acmp_declaring_o[0]`), `[2]` mirrors the override socket and `[3]` the
  composed gate above.
- `A_ACMP_LOBS = 0x670` (RW): `[0]` listener_observed override.
- The per-word verdict for every register whose source moved or died is
  [`reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md); the group-level
  classification is
  [`reference/REGISTER_MAP_CLASSES.md`](../reference/REGISTER_MAP_CLASSES.md).

## Explicitly out of scope (this increment)

> **UPDATE 1 (2026-07):** this "out of scope" list is from the original
> talker-SM increment. Since then **lwSRP**, **fabric MAAP** and the **ACMP
> listener** all LANDED in fabric.
>
> **UPDATE 2 (2026-08-13):** two of those three have since been *deleted*.
> The lwSRP applicant and the fabric ACMP listener are gone; SRP and the ACMP
> listener are the protocol processor's now. **`KL_maap` survives** and is
> still this fabric's allocator — see
> [`MAAP_FABRIC.md`](MAAP_FABRIC.md).

- lwSRP itself (MSRP TA declare / Listener Ready registrar) — the
  `listener_observed` input is its socket. **(Landed, then deleted; the
  socket is now fed by the processor's class-D SRP face.)**
- STREAM_INPUT / listener side, BIND_RX/UNBIND_RX/GET_RX_STATE. **(Landed,
  then deleted; served by the processor's listener half.)**
- MAAP dynamic allocation (static MAAP-range dmac from CSR). **(Landed and
  still here.)**
- GET_DYNAMIC_INFO (Milan §5.4.2.24) — la_avdecc enum passes without it.
  **(Landed in the AECP response builder, then deleted with it. Still NOT
  IMPLEMENTED: the µCPU echoes `NOT_IMPLEMENTED` at it, which returns no
  dynamic info. This one is a real loss, not a formality.)**
- Talker counters STREAM_START/STREAM_STOP wiring into GET_COUNTERS.
  **(Moot: GET_COUNTERS is gone and the Milan Table 5.4 per-STREAM_OUTPUT
  counter context is no longer instantiated — nothing could read it. The
  STREAM_INPUT counters at `0x6B8` are unaffected and still live.)**

## Gates

**What was proven, and against what.** The `acmp` and `aecp` Verilator suites
that gated this design are deleted with the RTL they drove: probe→armed and
byte-exact response fields, the 15 s expiry, `listener_observed` hold,
disconnect no-op, GET_TX_STATE live fields, unknown-uid/foreign-guid ignores,
the SET_STREAM_INFO accept/reject matrix, START/STOP → NOT_SUPPORTED, and
unsolicited register/dedup/full/dereg + push sequencing. **None of that
evidence transfers to the processor's implementation** — the processor's own
verification is in the pinned submodule, and the datapath-level checks live
in [`tb/verilator/milan_dp`](../../tb/verilator/milan_dp).

**What still gates here.** The end-to-end property that survives is the one
this page exists for: a real controller `PROBE_TX` through the real datapath
must open the AAF gate and put the probed `stream_id` / `dmac` / `vlan` on
the wire, byte-for-byte, and the gate must close when the declaration drops.
That is a silicon drill (controller probe from the peer host, ADP census,
`la_avdecc` Milan=1 re-cert) plus the standard yosys + full-regression +
3-seed sweeps. The AECP half of the old drill can partly run again, and it is
worth being exact about which part: `READ_DESCRIPTOR` and its three status
paths — `SUCCESS`, `NO_SUCH_DESCRIPTOR`, `BAD_ARGUMENTS` with the §7.4.5
stub — are testable on silicon, though the `SUCCESS` path needs a descriptor
image placed in DRAM by hand first, since no build step here produces one. The
un-loaded case is testable for free and is the one a bench will hit by default:
every read answers `BAD_ARGUMENTS`, because an invalid image reports zero
configurations and the argument check precedes the locate. `NO_SUCH_DESCRIPTOR`
is therefore only reachable against a loaded image, which makes the pair a
discriminator: `BAD_ARGUMENTS` everywhere means no image, `NO_SUCH_DESCRIPTOR`
means the image is there and that descriptor is not. Also testable is the conformance of
the `NOT_IMPLEMENTED` echo (length,
`message_type`, `controller_data_length`) and the `IDENTIFY_NOTIFICATION`-as-
command `BAD_ARGUMENTS`. What still cannot be exercised anywhere is every
*function* the old suites covered: the SET_STREAM_INFO accept/reject matrix,
START/STOP → NOT_SUPPORTED, the unsolicited register/dedup/full/dereg and push
sequencing. Those have no implementation to test, only an echo, and the echo
proves the responder is well-formed rather than that the talker obeys Milan.

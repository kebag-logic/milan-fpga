[OBSOLETE + 2026-08-17]

# Item-10 — PDU getter/setter verification (the plan, and what the AECP half can and cannot run)

> ## STATUS 2026-08-13 — **THIS DEVICE ANSWERS AECP: READ_DESCRIPTOR, PLUS A CONFORMANT NOT_IMPLEMENTED ECHO FOR EVERYTHING ELSE.**
>
> An earlier revision of this page, written the same day, said the device
> answered **no** AECP/AEM command at all. **That premise was false and is
> corrected here**: the `protocol-processor` submodule landed its **AECP uCPU**.
> The device is reachable on AECP. It is not silent.
>
> The repository's own AECP/AEM engine, ACMP talker/listener, ADP advertiser and
> lwSRP applicant are still **DELETED** — no parameter, no fallback, no shadow
> arm (USER, explicit and repeated: *"remove the old code AECP/ACMP/ADP the
> lwSRP shall be removed as well. Only use the uCPU code"*). The control plane is
> the protocol processor, wrapped by `hdl/milan/KL_pp_shadow.sv` and
> instantiated unconditionally by `hdl/milan/milan_datapath.sv`. It owns **ADP,
> ACMP (talker and listener), SRP — and AECP.**
>
> What the AECP uCPU answers, exactly:
>
> * **`READ_DESCRIPTOR` (0x0004)** — `SUCCESS` carrying `configuration_index`,
>   the reserved field and the descriptor; `NO_SUCH_DESCRIPTOR` on a locate miss;
>   `BAD_ARGUMENTS` on a bad configuration index. Both error paths carry the
>   IEEE 1722.1 §7.4.5 4-byte `{descriptor_type, descriptor_index}` stub.
> * **`IDENTIFY_NOTIFICATION` (0x0026) arriving as a COMMAND → `BAD_ARGUMENTS`**
>   — IEEE 1722.1 §7.4.39.2's opcode-specific rule wins over §9.3.5.3.3.
> * **Every other opcode, and every other message type** (AEM,
>   ADDRESS_ACCESS/AA, VENDOR_UNIQUE/MVU) → a **conformant `NOT_IMPLEMENTED`
>   echo**: correct `message_type`+1, correct length, correct
>   `controller_data_length`. Never silence, never malformed. That discharges
>   IEEE 1722.1 §9.3.5's duty to respond, and nothing beyond it.
> * **Silently refused** — freed, counted, no reply: a command whose
>   `target_entity_id` is not ours, and any AECP **response** arriving as input.
>
> **An echo is not an implementation.** Every row below whose *function* is
> absent stays **NOT IMPLEMENTED**: the controller now receives a well-formed
> `NOT_IMPLEMENTED` instead of silence, and still receives no value, no state
> change and no notification. Do not re-grade a row as covered because the
> entity answered.
>
> **Descriptor enumeration is reachable once the descriptor image is in
> DRAM.** The tracked builder handoff supplies it on an explicit
> deployment transfer; inspection-only/custom flows that skip that handoff
> remain empty. In that state every
> `READ_DESCRIPTOR` answers `BAD_ARGUMENTS` — the microprogram range-checks
> `configuration_index` against `configurations_count` **before** it locates,
> and an invalid image reports a count of zero, so no index passes and the
> locate is never reached.
>
> **KNOWN GAP, kept visible:** Milan Δ7 `ACQUIRE_ENTITY` (`NOT_SUPPORTED` with
> `owner_id` = 0) is **NOT** distinguished from the generic echo.

Roadmap item 10 (spec-matrix peer-validation) decomposed into **one verification
per command**, grouped by PDU family (ADP · ACMP · AECP/AEM+MVU · AAF) and by
**fixture class**. The decomposition and the fixture-class argument survive the
plane deletion unchanged — they are statements about how a getter and a setter
fail, not about which RTL serves them. What changed is the *verdict column*: a
small, exactly-bounded part of the AECP/AEM family now has an implementation to
verify, and the rest has a well-formed refusal and no function.

## Contents

- **[What is gone, and what replaced it](#what-is-gone-and-what-replaced-it)** — The boundary in one table: which PDU family a controller can exercise against this device and who serves it now, ending with the descriptor-image supply gap that makes every `READ_DESCRIPTOR` on a stock build answer `BAD_ARGUMENTS`. Read it before any row below.
- **[Why a command needs a \*fixture class\* (not one generic test)](#why-a-command-needs-a-fixture-class-not-one-generic-test)** — The reasoning plus five ready-to-copy Gherkin skeletons, re-triaged against the landed uCPU: class 1 is buildable for `READ_DESCRIPTOR` alone, classes 2 and 3 still are not. The argument in one line: a getter fails by shape, cross-check and non-idempotence; a setter fails by no-op writes emitting spurious notifications, or by notifying the requester instead of the *other* controllers — nothing generic catches both.
- **[AECP / AEM + MVU — what the uCPU answers, and what is still absent](#aecp--aem--mvu--what-the-ucpu-answers-and-what-is-still-absent)** — Two tables and the line between them: the handful of behaviours the AECP uCPU really implements (the three `READ_DESCRIPTOR` status paths, the `IDENTIFY_NOTIFICATION`-as-command refusal, the echo contract, the two silent-refusal rules), then every command whose function is still absent — with the reason a reader must not read the echo they all return as coverage.
- **[ACMP — owned by the protocol processor](#acmp--owned-by-the-protocol-processor)** — The five connection-management commands that a controller really can still issue, with the verification lane that survives.
- **[ADP — owned by the protocol processor](#adp--owned-by-the-protocol-processor)** — Advertise, depart, discover; plus the one ADP diagnostic surface that is now a structural zero.
- **[AAF — unaffected](#aaf--unaffected)** — The two wire-observation rows the media plane still backs.
- **[Prerequisites & running](#prerequisites--running)** — What can actually be run today, the note that nothing here has yet been run against the landed uCPU, and the honest caveat on what a green local run does not prove.
- **[The order now that the uCPU has landed](#the-order-now-that-the-ucpu-has-landed)** — Branch/PR conventions kept, plus the merge order the landing changes: `read-descriptor` and the three protocol-conformance branches are buildable now, and every other AECP branch is still blocked on a missing *function* rather than a missing response.

## What is gone, and what replaced it

| PDU family | Who serves it today | What a controller sees |
|---|---|---|
| **ADP** | the protocol processor (`hdl/milan/KL_pp_shadow.sv`) | advertise, depart and discover-response all on the wire; `available_index` published by the processor |
| **ACMP** talker + listener | the protocol processor | BIND_RX / PROBE_TX / GET_*_STATE answered; the bind record is republished as a class-D wire face the fabric consumes every clock |
| **SRP (MSRP/MVRP)** | the protocol processor | Talker Advertise / Listener Ready / Domain, and the granted idleSlope that drives CBS |
| **MAAP** | this fabric (`KL_maap`, bridged by `hdl/milan/KL_pp_maap_shim.sv`) | probe / defend / announce — the processor implements no MAAP by design |
| **AECP / AEM** | the protocol processor's **AECP uCPU** | `READ_DESCRIPTOR` answered (SUCCESS / NO_SUCH_DESCRIPTOR / BAD_ARGUMENTS); `IDENTIFY_NOTIFICATION`-as-command answered BAD_ARGUMENTS; **every other command answered with a conformant `NOT_IMPLEMENTED` echo** — a well-formed response, never a function |
| **MVU** (Milan vendor unique) | the same uCPU, as an unimplemented message type | MVU rides AECP, so it gets the same `NOT_IMPLEMENTED` echo. **No MVU command is implemented** — `GET_MILAN_INFO` included |
| **AAF / CRF** | the media plane, unchanged | streams on the wire |

The ACMP **DA gate is the talker gate**: `acmp_declaring_o` asserts only after a
MAAP `ALLOC_DA` success, so AAF admission is still "a destination address exists
AND the source is declaring".

**The descriptor image, and the supply gap.** The processor's descriptor store
fetches the entity model over a **read-only master** with a **compile-time
base** — `DESC_BASE_P` in the submodule's `KL_aecp_desc_store`, surfaced in the
parent as `milan_datapath`'s `PP_DESC_BASE_P`, which the LiteX SoC **derives**
as the top 1 MiB of `main_ram` (`main_ram.origin + main_ram.size - 0x100000`).
There is no base register; software cannot relocate it at runtime, and it must
load the image at that base **before** enabling the entity. The image header
carries magic `"AEMI"` (`0x41454D49`), layout version 1 and a checksum, so a
zeroed region reads as *image not loaded* rather than as an empty model.

**Nothing in this repository builds or loads that image.** The generator lives
in the submodule (`protocol-processor/hdl/aecp/desc/gen_desc_image.py`,
vendor-neutral JSON in, flat memory image out), and **no step** in `sw/builder/`,
`scripts/`, the LiteX SoC builder or the boot path turns an `endstation_*.yaml`
config into that JSON or writes the result into DRAM.
`sw/builder/endstation_builder.py` still emits `aecp_aem_rom.svh`, the ROM for
the **deleted** `KL_aecp_aem_store` — an orphaned artifact, not the image the
processor reads. So on a stock build the region is unloaded and **every
`READ_DESCRIPTOR` answers `BAD_ARGUMENTS`** — not `NO_SUCH_DESCRIPTOR`. The
microprogram range-checks `configuration_index` against `configurations_count`
**before** it attempts the locate, and a store whose image failed its
magic/version/checksum deliberately reports a `configurations_count` of zero
rather than the garbage its header walk read, so the check fails for every
configuration index including 0 and the locate is never reached. The response
still carries the §7.4.5 4-byte `{descriptor_type, descriptor_index}` stub.
**Read the two statuses as a diagnostic discriminator:** every read answering
`BAD_ARGUMENTS` means the image was never loaded or is corrupt; a read answering
`NO_SUCH_DESCRIPTOR` means the image *is* loaded and that descriptor is genuinely
absent from the model. Either way it is a clean refusal, not a
lockup: the store's watchdog (`MEM_TIMEOUT_CYC_P` = 4096 cycles, about 41 us at
100 MHz) abandons a stalled burst and covers the request handshake too, and a
late load **heals without a reset** because every locate against an invalid image
re-arms the header probe. Write "enumeration is reachable once the image is in
DRAM", never "enumeration works".

## Why a command needs a *fixture class* (not one generic test)

A getter and a setter have fundamentally different failure surfaces, so they get
different fixtures. Five classes cover the whole PDU universe. Classes 4 and 5
are live. Re-triaged against the landed uCPU:

* **Class 1 (getter) is buildable for `READ_DESCRIPTOR` only**, and only once a
  descriptor image is in DRAM — until then the "unknown descriptor is refused"
  half runs (it is what the whole address space answers) and the "returns the
  provisioned value" half cannot, because there is no provisioned value to
  return. For every other getter the class is still unbuildable: the response
  is a `NOT_IMPLEMENTED` echo carrying no value to cross-check.
* **Classes 2 and 3 (setter, paired) remain unbuildable.** There is no setter,
  so there is no write to read back, no unsolicited to observe and no
  no-change gate to trip. What *is* now buildable in their place is a much
  weaker, protocol-only check: that the refusal is a well-formed
  `NOT_IMPLEMENTED` response with the right `message_type`, length and
  `controller_data_length`. That grades §9.3.5's duty to respond. It grades
  nothing about the command.

### 1. GETTER fixture — read-only, idempotent, model-cross-checked
Failure surface: wrong payload shape, wrong value vs the descriptor/state, missing
reject-on-unknown, non-idempotence.
```gherkin
@class:getter
Scenario: <GET_X> returns the provisioned value and is well-formed
  Given the entity is discovered and <descriptor>/<index> is provisioned to a KNOWN value
  When controller C reads <GET_X>(<descriptor_type>, <index>)
  Then the response status is SUCCESS
  And control_data_length matches the <GET_X> response layout
  And every field equals the AEM-golden / provisioned model value      # cross-check, not self-consistency
  And a second identical read returns byte-identical payload            # idempotent, no state change
Scenario: <GET_X> on an unknown descriptor/index is refused
  When controller C reads <GET_X>(<descriptor_type>, out-of-range)
  Then the response status is NO_SUCH_DESCRIPTOR (or BAD_ARGUMENTS)
```

### 2. SETTER fixture — write + read-back + notify + no-change-gate + range + lock + restore
Failure surface (all distinct): the write not taking effect, no unsolicited to *other*
controllers, an unsolicited to the *requester*, a spurious unsolicited on a no-op write,
out-of-range accepted, writing while locked/acquired by another controller.
```gherkin
@class:setter
Scenario: <SET_X> changes state, notifies others, and read-back reflects it
  Given controllers "C1" and "C2" are registered and the baseline <GET_X> == V0
  When "C1" sends <SET_X>(V1)
  Then the response status is SUCCESS
  And <GET_X> == V1                                                     # read-back
  And "C2" receives an unsolicited notification of the change
  And "C1" (the requester) receives NO unsolicited notification
Scenario: a no-op <SET_X> emits no unsolicited (no-change gate)
  When "C1" sends <SET_X>(V1) again with the same value
  Then no controller receives an unsolicited notification               # wb_diff / two-phase-read gate
Scenario: <SET_X> out of range is refused and state is unchanged
  When "C1" sends <SET_X>(<out-of-range>)
  Then the response status is BAD_ARGUMENTS (or NOT_SUPPORTED) and <GET_X> == V1
Scenario: <SET_X> under another controller's lock/acquire is refused
  Given the entity is locked by "C2"
  When "C1" sends <SET_X>(V2)
  Then the response status is ENTITY_LOCKED and <GET_X> == V1
  # teardown: restore V0
```

### 3. PAIRED fixture ("getter *or* setter" — the GET/SET twins)
For the commands that come as a GET_X/SET_X pair sharing one descriptor/state, the highest-
value fixture is the **round-trip**: it proves the getter *reflects* the setter (the coupling
neither alone tests), then folds in both negatives. Used for CONFIGURATION, STREAM_FORMAT,
STREAM_INFO, NAME, SAMPLING_RATE, CLOCK_SOURCE, CONTROL, MAX_TRANSIT_TIME, SYSTEM_UNIQUE_ID,
MEDIA_CLOCK_REFERENCE_INFO.
```gherkin
@class:paired
Scenario: GET/SET_<X> round-trip — the getter reflects the setter
  Given baseline B = GET_<X>            # getter shape asserted here
  When SET_<X>(V1) succeeds and notifies C2 (not C1)
  Then GET_<X> == V1                    # the coupling: SET is visible through GET
  And SET_<X>(V1) again → no unsolicited (no-change gate)
  And SET_<X>(out-of-range) → refused, GET_<X> == V1
  And GET_<X>(unknown index) → NO_SUCH_DESCRIPTOR
  # teardown: SET_<X>(B)
```

### 4. ACTION / state-machine fixture (ACMP connect/disconnect)
Neither get nor set — a protocol action; verify the **state transition + side effects**
(SRP reservation, PROBE ladder, GET_*_STATE readback) and the auth negatives. Note the
Milan renames: `CONNECT_RX_*` is `BIND_RX_*` and `CONNECT_TX_*` is `PROBE_TX_*` on a
PAAD-AE (Milan v1.2 5.5.3), and the readback leg that used to run through
`GET_STREAM_INFO` is gone with AECP — the bind truth is now the processor's class-D
bind record, read at the `0x6A4` CSR group's `bound` / `active` bits.
```gherkin
@class:action
Scenario: BIND_RX binds, probes, reserves, and the bind record reflects it
  Given the listener sink is UNBOUND
  When a BIND_RX_COMMAND(talker, listener) is processed
  Then the response is SUCCESS with stream_id/dest_mac/vlan_id zeroed (Milan Table 5.32)
  And the SRP Listener attribute registers and the granted idleSlope appears
  And the 0x6A4 bind record reads bound = 1        # NOT ACMPL_STATE — see the note below
Scenario: a wrong controller_entity_id UNBIND is refused with no state change
  ...  → CONTROLLER_NOT_AUTHORIZED ;  nonzero listener_unique_id → LISTENER_UNKNOWN_ID
```
**`ACMPL_STATE` no longer tracks PROBING/SETTLED** — those fields were the deleted
listener state machine's and now read structural zeros. A reader must take `bound`
as the truth.

### 5. PDU-FORMAT fixture (AAF-PCM, ADP advertise/depart)
No request/response — **observe the emitted PDU** on the tap and validate every field vs the
spec constants (the "getter" of the wire).
```gherkin
@class:pdu @tier:t2 @bench
Scenario: every AAF-PCM PDU carries the Milan class-A field set
  Given the talker is streaming
  When I capture N 0x22F0 subtype-0x02 PDUs on the tap
  Then each has sv=1, tv=1, format/nsr/channels/bit_depth per the stream, monotonic seq,
       stream_id == {station_mac, uid}, and avtp_timestamp within the presentation window
```

## AECP / AEM + MVU — what the uCPU answers, and what is still absent

The AECP uCPU is in this build. **A short, exactly-bounded set of behaviours is
IMPLEMENTED and testable (owner: the protocol processor's AECP uCPU) — one
command, one opcode-specific refusal rule, one response contract and two
silent-refusal rules; every other row is still NOT IMPLEMENTED**, and the
conformant `NOT_IMPLEMENTED` echo those rows now receive
is a *protocol-conformance* behaviour, not coverage of the command. The fixture
class is retained on every row because it remains the specification the
function-landing round is verified against. The "coverage before the deletion"
column is history, not coverage — the engine it names (`KL_aecp_top` and its
response builder, AEM store, timers, accessor, validator, dynamic-map mux, AEM
patch port and persistence journal) is deleted, together with its Verilator
suite and its `tsn_fuzz` campaign.

**Implemented, and what a fixture may assert:**

| Behaviour | Class | Status today | Fixture is buildable? |
|---|---|---|---|
| `READ_DESCRIPTOR` (0x0004) → `SUCCESS` with `configuration_index` + reserved + descriptor | getter | **IMPLEMENTED (protocol processor / AECP uCPU)** | only with a descriptor image in DRAM — nothing in this repo loads one, so on a stock build this path is never taken |
| `READ_DESCRIPTOR` → `NO_SUCH_DESCRIPTOR` on a locate miss, carrying the §7.4.5 4-byte `{descriptor_type, descriptor_index}` stub | getter (negative) | **IMPLEMENTED (protocol processor / AECP uCPU)** | only with a descriptor image in DRAM: the locate is reached only after the configuration range check passes, and on a stock build that check fails first, so this status is *unreachable* until an image is loaded |
| `READ_DESCRIPTOR` → `BAD_ARGUMENTS` on a bad configuration index, same 4-byte stub | getter (negative) | **IMPLEMENTED (protocol processor / AECP uCPU)** | yes — and on a stock build it is the answer to *every* `READ_DESCRIPTOR`, because an invalid image reports `configurations_count` = 0; a fixture must not read a pass here as "enumeration works" |
| `IDENTIFY_NOTIFICATION` (0x0026) arriving as a **COMMAND** → `BAD_ARGUMENTS` | negative | **IMPLEMENTED (protocol processor / AECP uCPU)** — IEEE 1722.1 §7.4.39.2 beats §9.3.5.3.3 | yes. This is *not* IDENTIFY: `SET_CONTROL`-driven identification is not implemented and `o_identify` is tied 0 |
| the conformant `NOT_IMPLEMENTED` echo for every other opcode and message type (AEM, AA, MVU) | protocol-conformance | **IMPLEMENTED as a RESPONSE CONTRACT ONLY** — correct `message_type`+1, correct length, correct `controller_data_length`; IEEE 1722.1 §9.3.5's duty to respond is met | yes — assert the frame shape. **It says nothing about any command below** |
| silent refusal: command whose `target_entity_id` is not ours; any AECP **response** arriving as input | negative | **IMPLEMENTED (protocol processor / AECP uCPU)** — freed, counted, no reply | yes — assert absence of a reply, with the counter as the corroborating side |

**Still NOT IMPLEMENTED — the function is absent in every row.** Each of these
now draws a well-formed `NOT_IMPLEMENTED` echo (except where noted); that is the
§9.3.5 duty being met and is **not** coverage of the command:

| Command | Class | Status today | Coverage before the deletion (history) | PR branch |
|---|---|---|---|---|
| WRITE_DESCRIPTOR | setter (refusal → NOT_IMPLEMENTED) | **NOT IMPLEMENTED** — but the owed refusal *is* now delivered, as the conformant echo | — | `item-10-write-descriptor` |
| GET/SET_CONFIGURATION | paired | **NOT IMPLEMENTED** | es-4.3, aecp_l0_state | `item-10-configuration` |
| GET/SET_STREAM_FORMAT | paired | **NOT IMPLEMENTED** — and with it the FR-STR-03 listener format adaptation | es-4.4 | `item-10-stream-format` |
| GET/SET_STREAM_INFO | paired | **NOT IMPLEMENTED** | es-4.6/4.5 | `item-10-stream-info` |
| GET/SET_NAME | paired | **IMPLEMENTED** with fixed cdl 84 bodies and READ_DESCRIPTOR coherence | compliant name-access tests | generated named descriptors |
| GET/SET_SAMPLING_RATE | paired | **NOT IMPLEMENTED** | es-4.8 | `item-10-sampling-rate` |
| GET/SET_CLOCK_SOURCE | paired | **NOT IMPLEMENTED — and this one has teeth.** `SET_CLOCK_SOURCE` was the only writer of the live CLOCK_DOMAIN `clock_source_index`, now pinned at 0 (INTERNAL) for the life of the build: **the CRF media clock can never be selected** | es-4.9, aecp_milan_v12_tsn_gen | `item-10-clock-source` |
| GET/SET_CONTROL (IDENTIFY) | paired | **NOT IMPLEMENTED** — `o_identify` is tied 0, so the LED is structurally dark | es-4.10 | `item-10-control` |
| GET/SET_MAX_TRANSIT_TIME | paired | **NOT IMPLEMENTED** — every Stream Output holds the Milan **2 ms default** presentation offset. That is a DEFAULT, not a zero: 0 ns would be a presentation time in the past and every listener would drop every frame as late | — (was already a gap) | `item-10-max-transit-time` |
| GET_AVB_INFO | getter | **NOT IMPLEMENTED** | es-4.13 | `item-10-avb-info` |
| GET_AS_PATH | getter | **NOT IMPLEMENTED**; the `0x7DC` AS_PATH staging port accepts writes and discards them | es-4.14 | `item-10-as-path` |
| GET_COUNTERS | getter | **IMPLEMENTED FOR SUPPORTED TARGETS**. Every declared STREAM_OUTPUT has a `KL_talker_diag_ctx` bank and returns the Milan Table 5.17 mask with STREAM_START, STREAM_STOP, MEDIA_RESET, TIMESTAMP_UNCERTAIN and FRAMES_TX in the compact layout. Missing indices return `NO_SUCH_DESCRIPTOR` with the fixed empty body. The Table 5.22 unsolicited change producer remains open | `pp_top`, `milan_dp`, `tkdiag`, pinned la_avdecc decoder | closed by issue 73 |
| GET_AUDIO_MAP + ADD/REMOVE_AUDIO_MAPPINGS | getter + action | **NOT IMPLEMENTED**; the AEM dynamic-map write ports are tied off | matrix M-AECP-4 | `item-10-audio-maps` |
| GET_DYNAMIC_INFO (0x4B) | getter | **NOT IMPLEMENTED**; the `0x768` BDBG scan-forensics words read structural zeros | CMD-22 | `item-10-dynamic-info` |
| ACQUIRE_ENTITY | setter (acquire sem) | **NOT IMPLEMENTED**; `0x648` `aecp_locked` is tied 0 (no lock manager is wired). **KNOWN GAP — do not smooth this over:** Milan Δ7 wants `NOT_SUPPORTED` with `owner_id` = 0, and this build does **not** distinguish that from the generic `NOT_IMPLEMENTED` echo. The Δ7 microprogram exists in the ucode (`E_ACQ`); nothing dispatches to it, so opcode 0x0000 falls into the generic echo | aecp_l0_state, es-4.1 | `item-10-acquire` |
| LOCK_ENTITY | setter (lock sem) | **NOT IMPLEMENTED** | es-4.18, aecp_stack_lock_acquire | `item-10-lock` |
| START/STOP_STREAMING | action | **NOT IMPLEMENTED**. Milan 5.3.7.3 forbids implementing STREAMING_WAIT anyway, so the streaming licence stays what it always was on this device: Talker Advertise declared **and** a Listener Ready received | es-4.11 | `item-10-streaming` |
| ENTITY_AVAILABLE | getter (liveness) | **NOT IMPLEMENTED** | es-4.2 | `item-10-entity-available` |
| CONTROLLER_AVAILABLE | getter (liveness) | **NOT IMPLEMENTED** | — | `item-10-controller-available` |
| REGISTER / DEREGISTER_UNSOLICITED_NOTIFICATION | action (notification registry) | **NOT IMPLEMENTED**, and with it the whole Milan **Table 5.22** unsolicited push duty. The processor's **unsolicited** TX lane has no producer at all — the solicited lane is the one the landed engine drives | aecp_unsolicited | `item-10-unsolicited-reg` |
| GET_MILAN_INFO (MVU) | getter | **NOT IMPLEMENTED** — MVU rides AECP. A controller cannot complete the Milan identity handshake | es-4.17 | `item-10-milan-info` |
| GET/SET_SYSTEM_UNIQUE_ID (MVU) | paired | **NOT IMPLEMENTED** | — | `item-10-system-unique-id` |
| GET/SET_MEDIA_CLOCK_REFERENCE_INFO (MVU) | paired | **NOT IMPLEMENTED** (was already unimplemented as M-AECP-9) | matrix ❌ | `item-10-media-clock-ref` |

**Where a reader will be tempted to mistake the echo for coverage.** A
controller run against this build gets a response to every row above. That
response is the same well-formed `NOT_IMPLEMENTED` in every case: no value, no
state change, no notification, no persistence. `GET_COUNTERS` does not return a
counter, `GET_MILAN_INFO` does not complete the Milan identity handshake,
`SET_SAMPLING_RATE` changes no rate, `SET_STREAM_FORMAT` adapts no listener. A
fixture that only checks "a response arrived" or "the status is not a timeout"
will pass against every one of these rows and prove nothing about any of them.

**Two register-map facts a fixture must not trip over.** The engine's own
counters — command, response, drop, locate-miss, last status, last length,
image-valid, image-fault — live in the protocol processor's **side-port snapshot
window**, reached through `KL_pp_shadow`'s side-port host bridge; they are **not**
at parent CSR `0x648`, which stays a structural zero. And `0x648`'s two fields
are hard zeros for narrow reasons: `aecp_locked` because there is no
ACQUIRE/LOCK and the lock manager is unwired, `current_config` because there is
no `SET_CONFIGURATION`.

**Saved state is gone too**, and it is a separate loss from any single command:
`KL_persist_journal` is deleted and the processor's NVM face is answered by a
BLANK-FLASH responder (reads `0xFF`, writes accepted and discarded, erase
completes). **Nothing in this device persists a binding across a power cycle** —
a restore walk always finds blank flash and completes with zero records. The
`0x7A0` ACMP bind-restore port accepts writes and never asserts its ack; the
`0x7B8`–`0x7C4` journal group and the `0x7C8`–`0x7D4` AEM dynamic-state patch
port accept writes and discard them.

## ACMP — owned by the protocol processor

Served by `hdl/milan/KL_pp_shadow.sv`, whose packed TX rides the control lane.
The surviving verification lane is the `pp_shadow` Verilator suite
(`tb/verilator/pp_shadow`) plus the datapath integration suite
(`tb/verilator/milan_dp`); the deleted `acmp` / `acmp_lstn` suites and the
`tsn_fuzz` ACMP campaign are gone.

| Command | Class | Status | PR branch |
|---|---|---|---|
| BIND_RX / UNBIND_RX (1722.1 CONNECT_RX / DISCONNECT_RX) | action/SM | owned by the protocol processor | `item-10-acmp-connect-rx` |
| PROBE_TX / DISCONNECT_TX (1722.1 CONNECT_TX) | action/SM | owned by the protocol processor | `item-10-acmp-connect-tx` |
| GET_RX_STATE | getter | owned by the protocol processor | `item-10-acmp-get-rx-state` |
| GET_TX_STATE | getter | owned by the protocol processor | `item-10-acmp-get-tx-state` |
| GET_TX_CONNECTION | getter (→ NOT_SUPPORTED per Milan) | owned by the protocol processor | `item-10-acmp-get-tx-connection` |

Two forensics surfaces that a fixture must NOT assert against any more: the
`0x648` group's acmp cmd/resp counts and `probe_armed`, and the whole `0x6E8`
`ACMPL_DBG` walker window, are **structural zeros** — their sources are deleted.
`acmp talker_active` at `0x648` is still live (it is the processor's
`acmp_declaring_o`), and so are `bound`, `active` and bit 31 (CRF sink bound)
in the `0x6A4` group.

## ADP — owned by the protocol processor

| Command | Class | Status | PR branch |
|---|---|---|---|
| ENTITY_AVAILABLE (advertise) | pdu-format | owned by the protocol processor | `item-10-adp-advertise` |
| ENTITY_DEPARTING | pdu-format | owned by the protocol processor | `item-10-adp-departing` |
| ENTITY_DISCOVER (response) | action | owned by the protocol processor | `item-10-adp-discover` |

Two traps for anyone writing these fixtures:

* the whole `0x600` **`A_ADP_DIAG` / `A_ADP_DIAG2`** group (depart count, rearm
  count, depart source, sent count, discover-rx count, discover-seen, last
  message, advertiser state) is a **structural zero** — the advertiser that fed
  it is deleted. `A_ADP` `available_index` is **still live**, published by the
  processor. A fixture must observe the wire, not those counters;
* the `0x600` provisioning words **entity_capabilities, valid_time,
  association_id, controller_capabilities, interface_index** and the
  advertise/depart strobes are **write-only scratch**: they read back what
  software wrote and the value **no longer reaches the wire**, because the
  processor's own ADP engine holds these as internal constants and exposes no
  port. Writing them changes nothing observable. `entity_id` is not in that set —
  it is still handed to the processor.

## AAF — unaffected

| Command | Class | Status | PR branch |
|---|---|---|---|
| AAF-PCM talker PDU (`hdl/ieee1722/aaf/`) | pdu-format | live; the `tsn_fuzz` **AAF** campaign is the one that survived | `item-10-aaf-pdu` |
| AAF version gate / mr (AVTP-3/5) | pdu-format @rtl-defect | live | `item-10-avtp-version-mr` |

## Prerequisites & running

The processor owns the live AECP engine and its `pp_top` suite grades that RTL.
The root `milan_dp` suite grades the integrated AECP wire path, including the
Stream Output GET_COUNTERS bank. The BDD features grade the standards-facing
contract and keep their served inventory synchronized with the RTL dispatch.
What can be run today:

```bash
make -C protocol-processor/tb/pp_top run
make -C tb/verilator/pp_shadow
make -C tb/verilator/milan_dp
cd tests && behave
```

Judge every one of these by **exit code**, and read the harness's own
`checks: <n>  failures: 0` line rather than a count quoted in prose. A green
local `behave` run is not proof that a bench-tagged scenario ran — scenarios that
need hardware or a generator skip cleanly when it is absent.

## The order now that the uCPU has landed

Base = `main`. Per command: `git checkout -b item-10-<cmd> main`, add the feature
(`tests/features/item10/<cmd>.feature`) + any new steps, run the suite green,
`gh pr create -R kebag-logic/milan-fpga --base main --head item-10-<cmd>`. Tag each scenario
`@class:<getter|setter|paired|action|pdu>` + `@cmd:<X>` + `@matrix:<row>` so the PRs slice by
class and roll up into [`SPEC_TRACEABILITY.md`](../SPEC_TRACEABILITY.md).

Merge order: the ACMP, ADP and AAF branches are buildable **now** against the
protocol processor and the media plane. `item-10-read-descriptor` is buildable
now too, and it merges first among the AECP branches, because the descriptor
read is the model every other AECP fixture asserts against — with the caveat
that until a descriptor image is loaded into DRAM its only reachable verdict is
`BAD_ARGUMENTS` — the configuration range check precedes the locate, so
`NO_SUCH_DESCRIPTOR` cannot be provoked without an image. Alongside it, three
protocol-conformance branches are buildable: the `NOT_IMPLEMENTED` echo contract
(`message_type`, length, `controller_data_length`), the
`IDENTIFY_NOTIFICATION`-as-command `BAD_ARGUMENTS` rule, and the two
silent-refusal rules. **Every remaining AECP/AEM branch is still blocked**, not
on a response but on a function: there is no getter to read and no setter to
write, so a fixture on one of them can only re-assert the echo. Do not open one
and call the row covered.

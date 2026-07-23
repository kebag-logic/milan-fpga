# Item-10 — PDU getter/setter verification (per-command, one PR each)

Roadmap item 10 (spec-matrix peer-validation) decomposed into **one verification per
command**, grouped by PDU family (ADP · ACMP · AECP/AEM+MVU · AAF) and by **fixture class**.
Each command lands as its own branch `item-10-<cmd>` → PR against `main`, reviewed one-by-one.
Builds on the existing host-sim + tsn_gen infra (`tests/steps/aecp_common_steps.py`,
`tests/steps/tsn_gen_steps.py`) and the real-wire CERT `es-4.x` suite.

## Why a command needs a *fixture class* (not one generic test)

A getter and a setter have fundamentally different failure surfaces, so they get different
fixtures. Five classes cover the whole PDU universe:

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

### 4. ACTION / state-machine fixture (ACMP connect/disconnect, START/STOP_STREAMING)
Neither get nor set — a protocol action; verify the **state transition + side effects**
(SRP reservation, PROBE ladder, GET_*_STATE readback, counters) and the auth negatives.
```gherkin
@class:action
Scenario: CONNECT_RX binds, probes, reserves, and GET_RX_STATE reflects it
  Given the listener sink is UNBOUND
  When a CONNECT_RX_COMMAND(talker, listener) is processed
  Then the response is SUCCESS and the listener SM walks BIND→PROBING→SETTLED
  And the lwSRP listener attribute registers and STREAM_START increments
  And GET_RX_STATE reports connected with the bound talker
Scenario: a wrong controller_entity_id UNBIND is refused with no state change
  ...  → CONTROLLER_NOT_AUTHORIZED ;  nonzero listener_unique_id → LISTENER_UNKNOWN_ID
```

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

## Command decomposition → fixture → PR (the backlog)

**AECP/AEM + MVU** (`hdl/ieee17221/aecp/`)

| Command | Class | Existing coverage | PR branch |
|---|---|---|---|
| READ_DESCRIPTOR | getter | aecp_stack_descriptor_walk (partial) | `item-10-read-descriptor` |
| GET/SET_CONFIGURATION | paired | es-4.3, aecp_l0_state | `item-10-configuration` |
| GET/SET_STREAM_FORMAT | paired | es-4.4 | `item-10-stream-format` |
| GET/SET_STREAM_INFO | paired (Listener SET unsupported) | es-4.6/4.5 | `item-10-stream-info` |
| GET/SET_NAME | paired | es-4.7 | `item-10-name` |
| GET/SET_SAMPLING_RATE | paired | es-4.8 | `item-10-sampling-rate` |
| GET/SET_CLOCK_SOURCE | paired | es-4.9, aecp_milan_v12_tsn_gen | `item-10-clock-source` |
| GET/SET_CONTROL (IDENTIFY) | paired | es-4.10 | `item-10-control` |
| GET/SET_MAX_TRANSIT_TIME | paired | — (gap) | `item-10-max-transit-time` |
| GET_AVB_INFO | getter | es-4.13 | `item-10-avb-info` |
| GET_AS_PATH | getter | es-4.14 | `item-10-as-path` |
| GET_COUNTERS | getter | es-4.15, hive | `item-10-counters` |
| GET_AUDIO_MAP + ADD/REMOVE_AUDIO_MAPPINGS | getter + action (es-4.16) | matrix M-AECP-4 | `item-10-audio-maps` |
| GET_DYNAMIC_INFO (0x4B) | getter | CMD-22 | `item-10-dynamic-info` |
| WRITE_DESCRIPTOR | setter (refusal → NOT_IMPLEMENTED) | — | `item-10-write-descriptor` |
| ACQUIRE_ENTITY | setter (acquire sem) | aecp_l0_state, es-4.1 | `item-10-acquire` |
| LOCK_ENTITY | setter (lock sem) | es-4.18, aecp_stack_lock_acquire | `item-10-lock` |
| START/STOP_STREAMING | action | es-4.11 | `item-10-streaming` |
| ENTITY_AVAILABLE | getter (liveness) | es-4.2 | `item-10-entity-available` |
| GET_MILAN_INFO (MVU) | getter | es-4.17 | `item-10-milan-info` |
| GET/SET_SYSTEM_UNIQUE_ID (MVU) | paired | — | `item-10-system-unique-id` |
| GET/SET_MEDIA_CLOCK_REFERENCE_INFO (MVU) | paired **@wip** (M-AECP-9 unimpl.) | matrix ❌ | `item-10-media-clock-ref` |

**ACMP** (`hdl/ieee17221/acmp/`)

| Command | Class | PR branch |
|---|---|---|
| CONNECT_RX / DISCONNECT_RX | action/SM | `item-10-acmp-connect-rx` |
| CONNECT_TX / DISCONNECT_TX | action/SM | `item-10-acmp-connect-tx` |
| GET_RX_STATE | getter | `item-10-acmp-get-rx-state` |
| GET_TX_STATE | getter | `item-10-acmp-get-tx-state` |
| GET_TX_CONNECTION | getter (→ NOT_SUPPORTED per Milan) | `item-10-acmp-get-tx-connection` |

**ADP** (`hdl/ieee17221/adp/`)

| Command | Class | PR branch |
|---|---|---|
| ENTITY_AVAILABLE (advertise) | pdu-format | `item-10-adp-advertise` |
| ENTITY_DEPARTING | pdu-format | `item-10-adp-departing` |
| ENTITY_DISCOVER (response) | action | `item-10-adp-discover` |

**AAF** (`hdl/ieee1722/aaf/`)

| Command | Class | PR branch |
|---|---|---|
| AAF-PCM talker PDU | pdu-format | `item-10-aaf-pdu` |
| AAF version gate / mr (AVTP-3/5) | pdu-format @rtl-defect | `item-10-avtp-version-mr` |

## Workflow

Base = `main`. Per command: `git checkout -b item-10-<cmd> main`, add the feature
(`tests/features/item10/<cmd>.feature`) + any new steps, run the host-sim/tsn_gen suite green,
`gh pr create -R kebag-logic/milan-fpga --base main --head item-10-<cmd>`. Tag each scenario
`@class:<getter|setter|paired|action|pdu>` + `@cmd:<X>` + `@matrix:<row>` so the PRs slice by
class and roll up into `SPEC_TRACEABILITY.md`. Merge order roughly follows the table
(descriptor/getters first — they are the read-model other fixtures assert against).

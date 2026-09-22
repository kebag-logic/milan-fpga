# IEEE 1722.1 Hardware Protocol Processor
## Generalized architecture for ADP, ACMP, AECP/AEM and Milan

> ## ⚠ Historical document — superseded, kept as the reviewed input
>
> This is the **original concept sketch**. It was reviewed clause by clause in
> [`docs/00_MILAN_COMPLIANCE_REVIEW.md`](docs/00_MILAN_COMPLIANCE_REVIEW.md) and replaced
> by the architecture under [`docs/architecture/`](docs/architecture/), which is the
> specification of record. It is kept because the review credits its surviving ideas and
> cites it, not because it describes the tree.
>
> **Do not design against this file.** The parts that no longer match the implementation
> include, at least:
>
> | This document says | The tree does |
> |---|---|
> | the processor should not contain SRP (§21) | it contains a full MSRP/MVRP endpoint participant — [`hdl/srp/`](hdl/srp/), [10](docs/architecture/10_srp_engine.md) |
> | a micro-ISA with `READ_MEMORY`, `WRITE_DESCRIPTOR`, `CHECK_ACQUIRE`, `ALLOCATE_CONNECTION`, `SEND_UNSOLICITED` and others (§9) | a different 29-operation ISA in [`hdl/aecp/ucpu_pkg.sv`](hdl/aecp/ucpu_pkg.sv); [06 §8](docs/architecture/06_aecp_engine.md) records which sketch operations were dropped and why |
> | descriptor, state and response **RAM** interfaces (§12, §19) | two main-memory masters with compile-time bases; nothing is a RAM port — [integrator guide](docs/guides/integrator.md) |
> | ACMP talker state, `connection_count`, an "ACMP µEngine" (§7) | Milan makes the talker **stateless**, and the listener is a transition-ROM walker, not a microcoded engine — [05](docs/architecture/05_acmp_engine.md) |
> | an ADP entity table with aging (§6) | discovery is per bound sink, with no cached entity database — [04](docs/architecture/04_adp_engine.md) |
> | a single 187.5 ms response target (§20) | per-class budgets — [08 §4](docs/architecture/08_timing.md) |
>
> For where to start instead, see [`docs/guides/`](docs/guides/README.md).

## 1. Objective

The original concept was to implement a small **AECP processor in HDL** using a pipelined architecture:

```text
FETCH → DECODE → EXECUTE → WRITE-BACK
```

The recommended evolution is to generalize this into a small **IEEE 1722.1 protocol processor**, rather than building an AECP-only CPU.

The processor should support:

- ADP — discovery
- ACMP — connection management
- AECP/AEM — Entity Model control
- Milan AECP/MVU extensions
- Milan connection-management extensions

The key architectural recommendation is:

> **Generalize the infrastructure and execution model, but do not force ADP, ACMP and AECP into an identical processor implementation.**

ADP is naturally a small deterministic state machine. ACMP benefits from a state-machine/microcode engine. AECP/AEM is the strongest candidate for a small microcoded processor.

---

# 2. High-level architecture

```text
                         IEEE 1722.1 PROCESSOR
                                  │
                    ┌─────────────┴─────────────┐
                    │ Common Packet Engine       │
                    │                            │
                    │ RX buffer                  │
                    │ Frame validation           │
                    │ Protocol detection         │
                    │ Transaction context        │
                    │ Deadline/timer management   │
                    └─────────────┬─────────────┘
                                  │
                         Normalized transaction
                                  │
               ┌──────────────────┼──────────────────┐
               │                  │                  │
               ▼                  ▼                  ▼
          ADP ENGINE         ACMP ENGINE        AECP ENGINE
          small FSM          FSM + µcode         µcoded CPU
               │                  │                  │
               └──────────────────┼──────────────────┘
                                  │
                           Shared datapath
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
                Entity state   Stream state   Control state
                    │             │             │
                    └─────────────┼─────────────┘
                                  ▼
                            TX scheduler
                                  │
                                  ▼
                             Ethernet TX
```

The expensive/common hardware should be shared:

- Ethernet/1722.1 packet buffering
- protocol parser infrastructure
- transaction context
- timers/deadlines
- state RAM interfaces
- response buffering
- TX arbitration
- diagnostics and trace infrastructure

---

# 3. Why generalize beyond AECP?

The three protocols occupy complementary parts of IEEE 1722.1:

| Protocol | Main function | Recommended implementation |
|---|---|---|
| ADP | Entity discovery | Small deterministic FSM |
| ACMP | Stream connection management | FSM + microcode |
| AECP/AEM | Entity Model/control | Microcoded execution engine |
| Milan MVU | Milan-specific AECP operations | AECP execution extension |
| Milan connection management | Milan-specific ACMP behavior | ACMP profile/microcode |

This avoids building three independent processors.

Instead, use one common execution infrastructure with protocol-specific front ends and operations.

---

# 4. Common transaction abstraction

A common internal transaction representation allows ADP, ACMP and AECP to share the execution infrastructure.

```text
1722.1_TRANSACTION
{
    protocol
    message_type
    source
    destination
    sequence_id

    operation

    operand[0..N]

    status

    context
}
```

Examples:

### AECP

```text
protocol = AECP
operation = READ_DESCRIPTOR

operand0 = configuration_index
operand1 = descriptor_type
operand2 = descriptor_index
```

### ACMP

```text
protocol = ACMP
operation = CONNECT_RX

operand0 = talker_entity_id
operand1 = listener_entity_id
operand2 = talker_unique_id
operand3 = listener_unique_id
```

### ADP

```text
protocol = ADP
operation = ENTITY_DISCOVER

operand0 = entity_id
```

The protocol-specific decoder converts the received packet into this normalized representation.

---

# 5. Common packet-processing pipeline

The generalized pipeline should be:

```text
Ethernet RX
     │
     ▼
┌───────────────────────┐
│ 1. FETCH / VALIDATE   │
│                       │
│ • frame buffering     │
│ • length validation   │
│ • protocol validation │
│ • header validation   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 2. DECODE / ADDRESS   │
│                       │
│ • ADP / ACMP / AECP   │
│ • operation decode    │
│ • operand extraction  │
│ • context generation  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 3. EXECUTE / COMMIT   │
│                       │
│ • FSM / µcode         │
│ • state checks        │
│ • RAM access          │
│ • state modification  │
│ • atomic commit       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 4. WRITE-BACK / TX    │
│                       │
│ • response creation   │
│ • response buffering  │
│ • TX arbitration      │
│ • Ethernet TX         │
└───────────────────────┘
```

The four stages should be viewed as **architectural stages**, not necessarily four clock cycles.

The Execute stage can be variable-latency.

---

# 6. ADP engine

ADP is substantially simpler than AECP.

It should not consume the full AECP microcoded CPU.

A suitable implementation is:

```text
                  ADP ENGINE

ADP RX
  │
  ▼
Validate
  │
  ├── ENTITY_DISCOVER
  ├── ENTITY_AVAILABLE
  └── ENTITY_DEPARTING
           │
           ▼
      Entity Table
           │
           ▼
       Timer / aging
           │
           ▼
         ADP TX
```

The ADP engine can therefore be:

- small FSM
- entity table
- timers
- packet formatter
- TX request interface

This keeps FPGA utilization low.

---

# 7. ACMP engine

ACMP is a better match for the processor concept.

Typical operations include:

```text
CONNECT_TX
DISCONNECT_TX
GET_TX_STATE

CONNECT_RX
DISCONNECT_RX
GET_RX_STATE
```

The engine needs connection state such as:

```text
talker_entity_id
listener_entity_id
talker_unique_id
listener_unique_id
connection_count
stream_id
stream_dest_mac
stream_vlan_id
...
```

Conceptually:

```text
ACMP command
      │
      ▼
   Validate
      │
      ▼
   Decode
      │
      ▼
┌───────────────┐
│ ACMP µEngine  │
└──────┬────────┘
       │
       ├── Talker state
       ├── Listener state
       ├── Connection state
       ├── Stream descriptor
       └── Response
```

---

# 8. Do not create three independent CPUs

Avoid:

```text
ADP CPU
ACMP CPU
AECP CPU
```

Instead use:

```text
                     1722.1 COMMAND ENGINE
                              │
                       Instruction ROM
                              │
                    ┌─────────┴─────────┐
                    │                   │
                 Common µISA       Protocol units
                    │                   │
          ┌─────────┼──────────┐        │
          │         │          │        │
       register   memory      ALU    ADP/ACMP/AECP
          │         │          │       operations
          └─────────┼──────────┘
                    │
                 State RAM
```

Protocol-specific behavior becomes either:

1. a small protocol FSM, or
2. a microcode operation / accelerator.

This minimizes duplicated hardware.

---

# 9. Proposed common micro-ISA

A possible common instruction set is:

```text
NOP

READ_MEMORY
WRITE_MEMORY

READ_DESCRIPTOR
WRITE_DESCRIPTOR

READ_STATE
WRITE_STATE

CHECK_ENTITY_ID
CHECK_CONTROLLER
CHECK_LOCK
CHECK_ACQUIRE
CHECK_CONNECTION
CHECK_ARGUMENT

COMPARE
MOVE
COPY

ALLOCATE_CONNECTION
RELEASE_CONNECTION

UPDATE_ENTITY_TABLE
UPDATE_STREAM_STATE

SET_STATUS
SET_LENGTH

BUILD_HEADER
BUILD_FIELD
COPY_BUFFER

COMMIT

SEND_RESPONSE
SEND_UNSOLICITED

BRANCH
BRANCH_IF_STATUS

END
```

This is intentionally small.

AECP commands should not become individual CPU instructions.

Instead:

```text
AECP command
      │
      ▼
Decoder
      │
      ▼
micro-program
      │
      ▼
common execution primitives
```

For example:

### GET_SAMPLING_RATE

```text
CHECK_TARGET
CHECK_DESCRIPTOR
READ_STATE sampling_rate
SET_STATUS SUCCESS
BUILD_RESPONSE
TX_RESPONSE
```

### SET_SAMPLING_RATE

```text
CHECK_TARGET
CHECK_CONTROLLER
CHECK_LOCK
CHECK_DESCRIPTOR
CHECK_ARGUMENT
WRITE_STATE sampling_rate
SET_STATUS SUCCESS
BUILD_RESPONSE
TX_RESPONSE
NOTIFY_STATE_CHANGE
```

---

# 10. AECP engine

AECP/AEM remains the largest and most flexible part.

Recommended structure:

```text
                 AECP
                   │
         ┌─────────┴──────────┐
         │                    │
       AEM                  MVU
         │                    │
         ▼                    ▼
     AEM decoder          MVU decoder
         │                    │
         └─────────┬──────────┘
                   ▼
             common µ-op
                   │
                EXECUTE
```

The AEM decoder converts:

- message_type
- command_type
- command-specific data
- controller ID
- target Entity ID
- sequence ID
- descriptor addressing fields

into the normalized internal transaction.

---

# 11. AECP descriptor addressing

Do not model the Entity Model as a simple `descriptor_id → RAM` mapping.

For example, `READ_DESCRIPTOR` uses:

```text
configuration_index
descriptor_type
descriptor_index
```

Other commands have different operands.

Therefore the Decode stage should create an internal operand record:

```text
AECP_OPERAND
{
    command_type
    message_type

    controller_entity_id
    target_entity_id
    sequence_id

    configuration_index
    descriptor_type
    descriptor_index

    operand_0
    operand_1
    operand_2
    ...
}
```

This normalized representation is one of the most important parts of the architecture.

---

# 12. AECP microcoded Execute stage

The Execute stage should contain:

```text
┌─────────────────────────────┐
│ AECP µCPU                   │
│                             │
│ µPC                         │
│ µInstruction ROM            │
│ operand registers           │
│ ALU                         │
│ branch/status logic         │
│ descriptor RAM interface    │
│ state RAM interface         │
│ response RAM interface      │
└─────────────────────────────┘
```

Conceptually:

```text
                ┌──────────────┐
                │     µPC      │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ µInstruction │
                │     ROM      │
                └──────┬───────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Descriptor        State         Response
      RAM             RAM             RAM
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                    ALU/FSM
```

---

# 13. State hazards

Pipelining introduces a significant issue: state-changing commands cannot always execute concurrently.

For example:

```text
SET_CONFIGURATION
        ↓
SET_STREAM_FORMAT
```

The second command may depend on state modified by the first.

Likewise:

```text
LOCK_ENTITY(controller A)
        ↓
SET_CONTROL(controller B)
```

must respect controller ownership and locking rules.

Therefore implement a command scoreboard/arbitration mechanism:

```text
                ┌──────────────────────┐
Decode ────────►│ Command scoreboard   │
                │                      │
                │ READ  → parallel     │
                │ WRITE → serialized   │
                │ LOCK  → serialized   │
                │ CONFIG → serialized  │
                │ MAPPING → serialized │
                └──────────┬───────────┘
                           │
                           ▼
                       EXECUTE
```

Recommended classification:

| Command class | Execution |
|---|---|
| Pure GET | Highly parallel |
| Descriptor READ | Parallel where safe |
| State READ | Parallel where safe |
| State WRITE | Serialized |
| LOCK/ACQUIRE | Serialized |
| Configuration | Serialized |
| Mapping | Serialized |
| Streaming state | Serialized |
| Notification | Independent TX path |

The goal is not maximum theoretical parallelism.

The goal is **deterministic safe parallelism**.

---

# 14. Shared state architecture

The shared state should be separated conceptually:

```text
                    1722.1 STATE
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
   Discovery         Entity Model       Connection
    State               State             State
       │                 │                  │
   ADP table          AECP descriptors      ACMP
   timers             dynamic state       connections
   entity info        controllers         stream state
```

This is preferable to a single generic "descriptor RAM."

---

# 15. Controller table

Milan v1.2 requires support for a minimum of 16 controllers.

Therefore reserve a small controller table:

```text
CONTROLLER_TABLE[16]

controller_entity_id
registered
last_seen
notification_enabled
lock_owner
...
```

This can be implemented in registers or BRAM depending on the target device.

---

# 16. Unsolicited notification path

Unsolicited responses should not depend entirely on an incoming command.

Use a dedicated notification path:

```text
                       ┌───────────────┐
normal response ──────►│               │
                       │  TX ARBITER   ├────► Ethernet TX
notification ─────────►│               │
                       │               │
                       └───────────────┘
```

This allows:

- normal command responses
- unsolicited notifications
- ADP messages
- ACMP responses
- AECP responses

to share the Ethernet TX interface safely.

---

# 17. Milan extensions

The architecture should support Milan as a **profile**, rather than creating a separate processor.

For example:

```text
ACMP µcode
     │
     ├── IEEE ACMP profile
     │
     └── Milan connection-management profile
```

Likewise:

```text
AECP
 │
 ├── AEM
 │
 └── Milan MVU
```

This allows protocol behavior to be changed primarily through:

- microcode
- command tables
- profile configuration
- small protocol-specific accelerators

rather than redesigning the datapath.

---

# 18. GET_DYNAMIC_INFO

`GET_DYNAMIC_INFO` is a particularly good use case for the micro-sequencer.

Conceptually:

```text
GET_DYNAMIC_INFO
        │
        ▼
 ┌───────────────┐
 │ read element  │
 └───────┬───────┘
         ▼
     dispatch µ-op
         │
         ▼
     execute GET
         │
         ▼
     append result
         │
         ├──── next element
         │
         └──── end → TX
```

This is a natural fit for a small microcoded processor.

---

# 19. Response buffering

The response path needs a configurable response buffer.

Use:

```text
MAX_AECP_RESPONSE_SIZE
```

as a synthesis/configuration parameter.

Recommended structure:

```text
             RESPONSE RAM

             Header
                │
                ▼
        command-specific data
                │
                ▼
             response
                │
                ▼
          TX scheduler
```

Do not assume every response has a fixed size.

Milan operations such as descriptor and mapping operations can require variable-sized responses.

---

# 20. Timing architecture

The processor should have a generic deadline engine:

```text
                 DEADLINE ENGINE
                       │
       ┌───────────────┼────────────────┐
       ▼               ▼                ▼
      ADP             ACMP             AECP
       │               │                │
   profile           profile          profile
   timeout           timeout          timeout
```

For AECP, the design target can be:

```text
Protocol timeout       = 250 ms
Entity response limit  = 240 ms
Design target          = 187.5 ms
Margin to timeout      = 62.5 ms
```

The design requirement should therefore be:

> **Every supported command shall complete and produce its response within 187.5 ms under the defined worst-case operating conditions.**

For Milan connection management, use the corresponding Milan timeout/profile requirements.

The deadline should start at a well-defined point, preferably reception of the complete command or RX start according to the implementation's timing contract.

---

# 21. Do not put AVTP/gPTP into this processor

The generalized architecture should remain a **control-plane processor**.

Do not turn it into:

```text
1722.1 CPU
+
AVTP
+
gPTP
+
SRP
+
audio processing
```

Instead:

```text
                    CONTROL PLANE
        ┌─────────────────────────────────┐
        │                                 │
        │ ADP     ACMP     AECP           │
        │  │        │        │            │
        │  └────────┼────────┘            │
        │           │                     │
        │     1722.1 Processor            │
        └───────────┼─────────────────────┘
                    │
              Hardware API
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
    AVTP engine   gPTP engine   TSN switch
```

The processor controls these engines but does not implement their datapaths.

---

# 22. Implementation options

## Option A — Pure FSM

```text
RX → FSM → RAM → TX
```

### Pros

- Smallest area
- Highly deterministic
- Easy timing closure
- Easy formal verification

### Cons

- State-machine explosion
- Adding commands becomes increasingly difficult
- Multi-cycle commands become cumbersome
- Poor reuse

### Best use

Very small fixed Milan profile.

---

## Option B — Microcoded 1722.1 processor

```text
RX → Decode → µCPU → TX
```

### Pros

- Small instruction set
- Commands become microprograms
- Easy to add commands
- Shared datapath/RAM
- Good fit for FPGA

### Cons

- Microcode tooling required
- Branching and hazard handling required
- More complex verification than pure FSM

### Best use

General-purpose compact 1722.1 control engine.

---

## Option C — Four-stage pipeline + microcoded Execute

```text
FETCH → DECODE → EXECUTE(µCPU) → WRITEBACK
```

### Pros

- Good throughput
- Flexible
- Deterministic
- Shared hardware
- Supports safe pipelining
- Easy to add commands
- Good future-proofing

### Cons

- State hazards
- Arbitration required
- Response ordering needs attention
- More verification effort

### Recommendation

**This is the preferred architecture.**

---

## Option D — Dedicated accelerator per command

```text
                 ┌── GET_DESCRIPTOR
                 ├── GET_CONFIGURATION
RX → DECODE ─────┼── SET_STREAM
                 ├── SET_CONTROL
                 └── ...
```

### Pros

- Maximum performance for specific operations

### Cons

- High FPGA area
- Duplicated logic
- Difficult shared-state consistency
- Poor scalability

### Recommendation

Use accelerators selectively for genuinely performance-critical operations.

---

# 23. Recommended final architecture

The preferred architecture is:

```text
                         1722.1 PROCESSOR
                                │
                    ┌───────────┴───────────┐
                    │ Common packet engine  │
                    └───────────┬───────────┘
                                │
                     Normalize transaction
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
          ADP engine       ACMP engine       AECP engine
          tiny FSM         µcode + FSM       µcode CPU
              │                 │                 │
              └─────────────────┼─────────────────┘
                                ▼
                         Shared datapath
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
             Entity          Stream          Control
              state           state            state
```

The key design principle is:

> **ADP stays tiny, ACMP gets a medium-sized state/microcode engine, and AECP gets the full microcoded engine. All three share the packet, memory, timing, transaction and TX infrastructure.**

---

# 24. Recommended project definition

Instead of:

> Small AECP CPU

I recommend defining the project as:

> **Small hardware IEEE 1722.1 protocol processor optimized for AECP/AEM and Milan, with shared ADP and ACMP execution infrastructure.**

More formally:

> Develop a compact, deterministic hardware IEEE 1722.1 protocol execution engine implementing ADP, ACMP and AECP/AEM, together with Milan v1.2 protocol extensions. The architecture shall use a four-stage packet-processing pipeline consisting of Fetch/Validate, Decode/Address, Execute/Commit and Write-back/Transmit. The Execute stage shall combine protocol-specific finite-state machines with a small microcoded processor operating on a normalized internal transaction representation.
>
> The architecture shall share packet buffering, protocol parsing infrastructure, transaction context, state-memory interfaces, response buffering, deadline management, TX arbitration and verification infrastructure between ADP, ACMP and AECP. State-changing operations shall be serialized when required by protocol dependencies, while independent read-only operations may be pipelined.
>
> The design shall remain a control-plane processor and shall interface to dedicated AVTP, gPTP and TSN datapath engines rather than implementing those protocols internally.

---

# 25. Main advantages

The generalized approach gives:

1. **Reusable FPGA IP**
2. One packet-processing infrastructure
3. One transaction/context mechanism
4. One TX scheduler
5. Shared timers
6. Shared verification infrastructure
7. Microcode-driven extensibility
8. Milan profile support without duplicating hardware
9. ADP with very low area cost
10. ACMP and AECP sharing the same datapath
11. Better long-term support for future 1722.1 revisions
12. A clean interface to AVTP/gPTP/TSN hardware engines

The key is to **generalize the execution infrastructure, not force every protocol into the same state machine or instruction sequence**.

---

# 26. Suggested next design phase

The next useful engineering step is to define the actual **common µISA and hardware interfaces**.

A good sequence would be:

```text
1. Define normalized 1722.1 transaction format
                 ↓
2. Define common µISA (~20–30 instructions)
                 ↓
3. Define ADP operations
                 ↓
4. Define ACMP operations
                 ↓
5. Define AECP/AEM operations
                 ↓
6. Define Milan MVU operations
                 ↓
7. Define Milan ACMP profile
                 ↓
8. Define state RAM organization
                 ↓
9. Define pipeline/scoreboard
                 ↓
10. Generate HDL architecture
                 ↓
11. Build reference software model
                 ↓
12. Co-verify HDL vs software model
```

This approach should allow the same command description to eventually generate:

- HDL decoder tables
- microcode
- command validation
- protocol documentation
- software reference implementation
- verification vectors

which is particularly attractive for a vendor-neutral FPGA implementation.

# Egress queue map

The classifier, queue bank, and 802.1Qav credit logic remain implemented and
independently verified, but the bare-metal product boundary supplies no packet
source to them. Their input valid is tied low in `milan_datapath`. Product AAF,
CRF, MAAP, protocol, and fabric-gPTP traffic joins downstream of this chain.

The notification claim is checked against the
[Milan feature status ledger](MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `notifications.change-events` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[Reset map](#reset-map)** — The stable five-queue roles and the checked CBS reset-slope table.
- **[Credit-based shaping](#credit-based-shaping)** — How admitted class-D reservations control slope and enable state atomically.
- **[Why gPTP sits below the shaped classes](#why-gptp-sits-below-the-shaped-classes)** — Why the fabric timer source cannot be delayed by the inactive generic queue chain.
- **[Where the fabric bypasses all of this](#where-the-fabric-bypasses-all-of-this)** — The live AAF, CRF, MAAP, protocol, and time sources merged downstream.
- **[Verification boundary](#verification-boundary)** — What the focused queue tests prove and what the release integration deliberately leaves inactive.

## Reset map

The five-queue CSR geometry remains stable:

| queue | reset role | shaping at reset |
|---:|---|---|
| q4 | class A | disabled until a valid admitted slope is supplied |
| q3 | gPTP classification target | disabled |
| q2 | class B | disabled until configured |
| q1 | control | disabled |
| q0 | best effort/default | disabled |

`CLS_CTRL`, `CLS_PCP_TC_MAP`, `CLS_PRIO_REGEN`, and
`CLS_TC_QUEUE_MAP` define the pure classification function. Queue indices
outside the elaborated count clamp to q0. The focused classifier, queue, and
CBS suites are the authority for this retained generic logic.

### CBS reset slopes

This table is a checked copy of `ethernet_packet_pkg::IDLE_SLOPE_1G` and the
credit functions used by `milan_csr`:

| Queue | idleSlope @ 1 Gb/s | share | hiCredit | loCredit |
|---|---:|---:|---:|---:|
| q4 SR class A | 450 Mb/s | 45 % | 684 | −837 |
| q3 SR class B | 150 Mb/s | 15 % | 228 | −1293 |
| q2 gPTP | 50 Mb/s | 5 % | 76 | −1445 |
| q1 control | 50 Mb/s | 5 % | 76 | −1445 |
| q0 best effort | 25 Mb/s | 2.5 % | 38 | −1483 |

The sum is 725 Mb/s (72.5% of the port), below the 75% ceiling. Every queue
still powers up unshaped.

## Credit-based shaping

An admitted SRP class-D source supplies the granted idle slope and enable bit
to the configured class-A queue. The active reservation overrides the matching
CSR slope without writing it back; release restores the CSR value. Opening a
source and accounting its slope occur on the same admission-round edge.
Teardown closes the source first and may retain its slope until the next round,
which is conservative: no stream can transmit against an unbudgeted slope.

## Why gPTP sits below the shaped classes

Fabric gPTP has its own timer-driven transmit source and merges after the
inactive classifier/shaper chain. It therefore cannot be delayed by queue
occupancy or firmware service. TX/RX event timestamps are captured at the MAC
boundary, and the fabric plane consumes its dedicated timestamp handshake.

The `0x88F7` classifier rule remains a tested generic mapping but is not the
release gPTP path.

## Where the fabric bypasses all of this

The live egress sources are:

- AAF talkers and CRF through the data-side merges;
- protocol-processor ADP/ACMP/AECP/SRP plus MAAP through the control merge and
  minimum-gap gasket;
- fabric gPTP at the final MAC-facing merge.

The live ingress media tap is before the destination filter; the filtered copy
feeds the protocol processor's control-frame observation. No ingress queue is
exposed to target software.

## Verification boundary

Use the focused `classifier`, `queues`, and CBS harnesses for the generic
blocks. Use `tb/verilator/milan_dp` and generated wire campaigns for product
traffic ordering and time ownership. A CSR reset map alone is not evidence that
a release packet traverses these queues.

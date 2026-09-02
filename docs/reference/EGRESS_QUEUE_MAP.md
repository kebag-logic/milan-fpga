# Egress queue map

The classifier, queue bank, and 802.1Qav credit logic remain implemented and
independently verified, but the bare-metal product boundary supplies no packet
source to them, and since VERSION `0x0056` `milan_datapath` **does not
instantiate them at all**: the retired transmit path that was their only source left
with #259, so an elaborated chain would have been silicon on a tied-off input
and a CSR face advertising a shaper no frame could reach. Product AAF, CRF,
MAAP, protocol, and fabric-gPTP traffic joins the trunk at the merges that sat
below the chain. The CSR words below are write-only scratch and `CAP.CBS` reads
0 ([REGISTER_MAP.md](REGISTER_MAP.md)); the blocks are building material for a
class-A shaping lane over the fabric's own sources, which is a separate lane.

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

Fabric gPTP has its own timer-driven transmit source and merges directly onto
the control lane; there is no classifier/shaper chain in the shipped trunk for
it to sit below. It therefore cannot be delayed by queue occupancy or firmware
service. TX/RX event timestamps are captured at the MAC boundary
(`KL_gptp_txstamp`) and off the RX tap, and the fabric plane consumes its
dedicated timestamp handshake. The rule this section is named for - gPTP
must never queue behind a shaped class - is what any future class-A shaping
lane over the fabric's own sources has to preserve.

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

Use the focused `classifier`, `queues`, `cbs`, `shaper_core`, `datapath` and
`controller_rate` harnesses for the generic blocks (and the `datapath_wrap` /
`credit_based_shaper` Yosys tops for their portability). Use
`tb/verilator/milan_dp` and generated wire campaigns for product traffic
ordering and time ownership. A CSR reset map is not evidence that a release
packet traverses these queues: none does, and none can - the chain is not in
the shipped datapath.

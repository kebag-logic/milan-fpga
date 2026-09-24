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

- **[Reset map](#reset-map)** -- The stable five-queue roles and the checked CBS reset-slope table.
- **[Credit-based shaping](#credit-based-shaping)** -- How the retained chain took slope and enable from SRP, and why the #530 gate does not.
- **[Why gPTP sits below the shaped classes](#why-gptp-sits-below-the-shaped-classes)** -- Why the fabric timer source cannot be delayed by the inactive generic queue chain.
- **[Where the fabric bypasses all of this](#where-the-fabric-bypasses-all-of-this)** -- The live AAF, CRF, MAAP, protocol, and time sources merged downstream.
- **[Verification boundary](#verification-boundary)** -- What the focused queue tests prove and what the release integration deliberately leaves inactive.

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

This section records how the retained chain was integrated with SRP. None of it
is instantiated in the shipping datapath (see the top of this page), so no
shaper consumes a slope or an admission verdict on the wire. An admitted SRP
class-D source supplied the granted idle slope and enable bit to the configured
class-A queue. The active reservation overrode the matching CSR slope without
writing it back; release restored the CSR value. While the stream gate was the
raw admission verdict, until #530, opening a source and accounting its slope
occurred on the same admission-round edge. Teardown closed the source first and
could retain its slope until the next round, which is conservative: no stream
could transmit against an unbudgeted slope.

The shipping licence now requires ACTIVE and the real grant (#551).
ACTIVE alone includes three admission rounds of optimistic admission.
The real grant excludes that optimistic term.
Each declaration clears its registered Listener first.
An early Listener Ready can still raise ACTIVE inside that window.
The licence waits for the real grant; see its residual below.

- **Admitted.** The licence opens when both terms hold.
  Normal Listener Ready arrivals follow admission, adding no delay.
  An earlier arrival waits for the real per-source grant.
- **Refused, same TSpec preloaded.** ACTIVE can pulse; licences stay closed.
  No STREAM_START/STREAM_STOP pair or Table 5.4 counter reset follows.
  No PDU leaves from the refused re-declaration.
  ACTIVE falls when optimism expires; Talker Failed follows.

**Residual: changed TSpec.** The refused TSpec differs from that source's previous one.
The first-round grant still uses the previous slope.
With an early Listener Ready, about one round's licence remains.
A STREAM_START/STREAM_STOP pair and Table 5.4 resets remain possible.
So does a PDU if its media event lands inside.
[Processor issue #112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112) owns the pending fix.
Its fix must be pinned before #551 can close.

`CRFT_CTRL[6]`/`[7]` and source 0's `LWSRP_STATUS[8]` require the grant.
`LWSRP_STATUS[6]` remains the OR of raw ACTIVE across sources.
It can therefore rise while every licence stays closed.
The snapshot gate bits follow their corresponding source licences.
See [REGISTER_MAP.md](REGISTER_MAP.md) for the per-index distinction.

No shaper consumes `LWSRP_SLOPE`; it remains diagnostic.
A future shaping implementation must prove its own slope/gate ordering.

## Why gPTP sits below the shaped classes

Fabric gPTP has its own timer-driven transmit source and merges directly onto
the control lane; there is no classifier/shaper chain in the shipped trunk for
it to sit below. It therefore cannot be delayed by queue occupancy or firmware
service. The RX event timestamp is captured off the RX tap; the TX one is not
captured at this boundary at all - since #360 it is the frame's observed
LAUNCH, reported back from the MAC's own transmit stream, so whatever the
merge and the MAC queue cost the frame is outside the timestamp. The rule this section is named for - gPTP
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

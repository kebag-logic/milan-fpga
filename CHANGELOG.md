# Milan FPGA product changelog

This file records current bare-metal product revisions. Older platform and
performance campaigns remain available in Git history (#259).

## Contents

- **[Release 0x0002_0056 — ownerless gPTP verification form](#release-0x0002_0056--ownerless-gptp-verification-form)** — Makes option OFF verification-only, write-inert and fail-safe while retaining the fabric-owned product path.
- **[Release 0x0002_0055 — fabric gPTP product ownership](#release-0x0002_0055--fabric-gptp-product-ownership)** — Selects the fabric engine as the sole shipping PHC and publication owner.
- **[Release 0x0002_0054 — generated names](#release-0x0002_0054--generated-names)** — Serves coherent generated descriptor names and writable overlays.
- **[Release 0x0002_0053 — stream setters](#release-0x0002_0053--stream-setters)** — Adds the supported stream-format and accumulated-latency setter behavior.

## Release 0x0002_0056 — ownerless gPTP verification form

- The fabric gPTP plane remains the sole shipping PHC, protocol, servo, and
  publication owner.
- `GPTP_PLANE_EN_P=0` remains buildable only for verification. Its GM, parent,
  PathTrace and peer-delay publications are zero, sync/asCapable are zero,
  `tu` is one, and writes to retained compatibility addresses are inert.
- Bare-metal UART status exposes GM, parent, PathTrace count/generation,
  peer delay, sync, asCapable and `tu`; the smoke grader requires and validates
  that complete record.
- The repository-wide bare-metal gate covers retired runtime-service tokens
  and tracked path classes with mutation-style self-tests.
- Removed from the tracked tree under #259 (163 files, 57,135 lines,
  recoverable from Git history at `59ba6ffb`): the unattended campaign runner
  (36 files), the Vivado block-design sources, the Zynq-era top wrapper and PS
  DMA wrapper, the software-audio staging RTL with its benches, 13 dated
  findings and 7 silicon evidence logs of the retired host stack, 9 product
  pages superseded by the bare-metal architecture pages, 5 testing pages, 9
  diagrams and 20 root diagram sources and renders, and the archive folder's
  last 10 pages together with its folder gate. Every retired markdown basename
  is registered in the docs gate's retired set.
- Documentation retirement rule: an obsolete page stays in the tree under an
  `[OBSOLETE + date]` first line and is cited by current pages only as
  labelled historical evidence, enforced by the docs gate's rule 7; #259 is
  the recorded exception for pages whose subject is the retired stack. Two
  protocol pages removed outside that directive are restored (the AECP
  compliance matrix and the PDU getter/setter verification record), 27 links
  from current pages into obsolete pages are labelled, and six pages rewritten
  as current authorities dropped their obsolete marker: the task list, the
  at-a-glance overview, the systems-engineer guide, the known issues and
  limitations page, the Milan compliance gaps ledger and the audio streaming
  design.

Physical closure still requires #70 persistence and #117's exact-candidate
two-board evidence.

## Release 0x0002_0055 — fabric gPTP product ownership

- Product configurations select the integrated fabric gPTP engine.
- GM, parent, PathTrace, peer delay, sync/asCapable and AVTP `tu` share one
  atomic publication bank.
- Fabric publication writes cannot be forged through the CSR surface.

## Release 0x0002_0054 — generated names

- `SET_NAME` and `GET_NAME` serve the generated AEM name inventory.
- Responses and `READ_DESCRIPTOR` observe one writable overlay.

## Release 0x0002_0053 — stream setters

- Stream-format and supported stream-info setters execute with
  descriptor-specific validation.
- Accepted presentation offsets and formats reach their fabric consumers.

The complete earlier revision record is preserved in the history of
`hdl/common/csr/milan_csr.sv` and this file.

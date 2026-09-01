# Milan FPGA product changelog

This file records current bare-metal product revisions.

Older campaigns remain available in Git history.

## Contents

- **[Release 0x0002_0056 — ownerless gPTP verification form](#release-0x0002_0056--ownerless-gptp-verification-form)** — Verification only.
- **[Release 0x0002_0055 — fabric gPTP product ownership](#release-0x0002_0055--fabric-gptp-product-ownership)** — Shipping time owner.
- **[Release 0x0002_0054 — generated names](#release-0x0002_0054--generated-names)** — Serves generated names and writable overlays.
- **[Release 0x0002_0053 — stream setters](#release-0x0002_0053--stream-setters)** — Adds supported stream setters.

## Release 0x0002_0056 — ownerless gPTP verification form

- The fabric gPTP plane remains the sole shipping time owner.
- It owns protocol, servo, and publication state.
- `GPTP_PLANE_EN_P=0` remains buildable only for verification.
- Its GM, parent, PathTrace, and peer-delay publications remain zero.
- Sync and asCapable remain zero.
- `tu` remains one.
- Compatibility writes remain inert.
- Bare-metal UART status exposes the complete timing record.
- The smoke grader validates every published field.
- The bare-metal gate rejects superseded runtime surfaces.
- Mutation controls cover every tracked path class.
- `milan_datapath` no longer instantiates classifier or queue stages.
- It also omits credit shaping and record stamping.
- Their only packet source left under #259.
- Product sources already join the downstream trunk.
- CSR addresses remain stable.
- Retained classifier and shaping registers are scratch.
- Retired capability and diagnostic bits read structural zero.
- The builder drops `--cbs-queues-mask`.
- Standalone suites and Yosys tops retain block coverage.
- Fabric credit shaping remains separately scoped.
- `milan_datapath` shrinks by 180,840 Yosys cells.
- Issue #259 removes 163 files and 57,135 lines.
- Commit `59ba6ffb` preserves them in Git history.
- Removed surfaces include campaign and vendor-build infrastructure.
- They also include superseded audio staging and benches.
- Target-era findings, logs, product pages, tests, and diagrams left.
- The archive lost only material covered by #259.
- The bare-metal scanner guards future reintroduction.
- General archives retain visibly labelled obsolete evidence.
- Issue #259 keeps target-only material solely in Git history.
- Other protocol records remain in the general archive.
- Current authorities replace stale status pages.

Physical closure still requires #70 and #117 evidence.

## Release 0x0002_0055 — fabric gPTP product ownership

- Product configurations select the integrated fabric gPTP engine.
- One atomic bank publishes GM, parent, and PathTrace.
- It also publishes delay, sync, asCapable, and AVTP `tu`.
- Fabric publication writes cannot be forged through CSRs.

## Release 0x0002_0054 — generated names

- `SET_NAME` and `GET_NAME` serve generated AEM names.
- Responses and `READ_DESCRIPTOR` share one writable overlay.

## Release 0x0002_0053 — stream setters

- Stream-format setters apply descriptor-specific validation.
- Supported stream-info setters apply equivalent validation.
- Accepted presentation offsets reach their fabric consumers.
- Accepted stream formats reach their fabric consumers.

Earlier revisions remain in this file's Git history.

The CSR RTL history provides the version source.

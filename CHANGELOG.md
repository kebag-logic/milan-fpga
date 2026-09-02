# Milan FPGA product changelog

This file records current bare-metal product revisions.

Older campaigns remain available in Git history.

The [archived throughput record](docs/history/v1/findings/PERFORMANCE_GOAL.md) preserves closed campaign measurements.

## Contents

- **[Release 0x0002_0057 — live media-clock selection](#release-0x0002_0057--live-media-clock-selection)** — CRF selection steers the grids.
- **[Release 0x0002_0056 — ownerless gPTP verification form](#release-0x0002_0056--ownerless-gptp-verification-form)** — Verification only.
- **[Release 0x0002_0055 — fabric gPTP product ownership](#release-0x0002_0055--fabric-gptp-product-ownership)** — Shipping time owner.
- **[Release 0x0002_0054 — generated names](#release-0x0002_0054--generated-names)** — Serves generated names and writable overlays.
- **[Release 0x0002_0053 — stream setters](#release-0x0002_0053--stream-setters)** — Adds supported stream setters.

## Release 0x0002_0057 — live media-clock selection

- The stored `SET_CLOCK_SOURCE` index reaches the media plane (#74).
- One registered resolve compares it against the generated CRF index.
- A CRF-less shape resolves structurally false through the `16'hFFFF` fold.
- The verdict arms the MMCM servo, the align chain, and `mr`.
- `KL_media_grid_align` holds the packet grid on the physical fsync grid.
- The chain runs CRF, MMCM, fsync, then tick.
- The MMCM status slice belongs to the MMCM alone.
- INTERNAL remains bit-exact free-run with slips accepted and now counted.
- `KL_chan_map_capture` gains TDM junction slip counters.
- The true-ratio leg proves the INTERNAL drift.
- The same leg proves its close under CRF.
- Received toggles and source changes both fire `mr`.
- The 10.4.3 scoping negative holds at INTERNAL.
- The CLOCK_SOURCE shape constants join `adp_shape_defaults.svh`, derived.
- Every shape carries its own CRF index.
- The 8-listener shapes read index 9.
- No CSR addresses move.

The bench probe stays open on issue #74.

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

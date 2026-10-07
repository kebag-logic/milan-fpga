<!-- SPDX-License-Identifier: Apache-2.0 -->
Use the frozen source head identified in [REPORT.md](REPORT.md).
Set LWSRP_SOURCE to its checkout and PACKET to this packet.
All disposable work belongs under PACKET/scratch.
Supply the test dependency through CGREEN_PREFIX.
This review used [release 1.7.0](https://github.com/cgreen-devs/cgreen/releases/tag/1.7.0), installed only inside scratch.
The downloaded archive hash is in [the dependency receipt](receipts/dependency.log).
The compiler, build system, scenario runner and graph renderer must already be available.

Run the [profile driver](scripts/baselines.py) and [edge probes](scripts/run_edge_probes.py):

```sh
python3 "$PACKET/scripts/baselines.py" --source "$LWSRP_SOURCE" --packet "$PACKET" --prefix "$CGREEN_PREFIX" --jobs 16
python3 "$PACKET/scripts/run_edge_probes.py" --source "$LWSRP_SOURCE" --packet "$PACKET" --library "$PACKET/scratch/build-default" --label default
python3 "$PACKET/scripts/run_edge_probes.py" --source "$LWSRP_SOURCE" --packet "$PACKET" --library "$PACKET/scratch/build-milan" --label milan
```

Both profile suites return zero.
The independent edge drivers return one at the reviewed head.
Their legal boundary controls return zero; their other groups reproduce the reported deviations.
The inherited extra Join indication is a separate nonblocking observation.
The [literal payload source](scripts/edge_probes.c) contains the precise checks.

The [mutation driver](scripts/mutations.py) requires a fresh scratch/mutations directory:

```sh
python3 "$PACKET/scripts/mutations.py" --source "$LWSRP_SOURCE" --packet "$PACKET" --prefix "$CGREEN_PREFIX"
python3 "$PACKET/scripts/audit.py" --source "$LWSRP_SOURCE"
```

The campaign changes only its disposable source copy.
All 42 faults are detected at this head, followed by a passing restored suite.
The [named failure ledger](receipts/mutation-ledger.md) separates behavioral failures from intentional compile or dependency failures.

The public-finding reconciliation has separate portable drivers:

```sh
python3 "$PACKET/scripts/reconcile_probes.py" --source "$LWSRP_SOURCE" --packet "$PACKET"
python3 "$PACKET/scripts/survivors.py" --source "$LWSRP_SOURCE" --packet "$PACKET" --prefix "$CGREEN_PREFIX" --jobs 16
```

The first driver returns zero when the expected module-link failure and both propagation failures reproduce alongside passing controls.
The second requires a fresh scratch/survivors directory.
It confirms nine surviving faults and one detected timing fault, then restores and checks its source copy.
Individual failing probe and mutation return codes are preserved in their receipts.

Use the repository commands in [the documentation guide](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/tools/README.md) to repeat rendering and link checks.
The [view script](scripts/graph_views.mjs) accepts a rendered graph directory and an installed browser-library module file.
It produces native views and page-width sheets without modifying the source.

Receipts preserve process output and exit codes.
Absolute source, packet, user, temporary and system executable prefixes are replaced with SOURCE, PACKET, USER_HOME, TEMP and SYSTEM_BIN.
This is location redaction only; counts, failures and diagnostics are retained.
Original transcripts and disposable dependencies stay in unpublished scratch.
No standard text is redistributed.

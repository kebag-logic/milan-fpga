<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# Using a PipeWire host as the AVB peer — and binding the pilot tone to a stream

How to stand up a plain Linux box as a **PipeWire-native AVB endpoint**
(listener/talker) against the boards, and how to get the pilot tone flowing
from the talker's CSRs into a bound stream. Everything here was verified on
the bench 2026-07-25; the fault list at the end is real history, not theory.

## Contents

- **[1. The endpoint stack, in order](#1-the-endpoint-stack-in-order)** — Three pieces in a mandatory order — ptp4l, then a PipeWire core, then `pipewire-avb` — each checkable before the next, plus the two config keys that bite when a conf is copied between machines.
- **[2. What "working" looks like (log signals)](#2-what-working-looks-like-log-signals)** — The five `-v` log lines to look for and what each proves, including how to read `offset_from_master`: it is scaled-ns, so −393216 is −6 ns.
- **[3. Binding the pilot tone to a stream](#3-binding-the-pilot-tone-to-a-stream)** — Talker-side CSR recipe (with the VID-clobber warning: a bare `AAF_CTRL` enable zeroes VID[27:16] and floods the stream as best-effort), the three ways to connect a listener, and where the pilot's acceptance limit is written down.
- **[4. The fault dictionary (all hit on 2026-07-25, in this order)](#4-the-fault-dictionary-all-hit-on-2026-07-25-in-this-order)** — Six real symptom→cause→fix rows from one bench day, including two misleading errors: "Host is down" means no core in the runtime dir, and hanging registry tools mean the AVB core has no session manager and a broken metadata marshal.
- **[5. The bind, as it actually ran (2026-07-25, late)](#5-the-bind-as-it-actually-ran-2026-07-25-late)** — The full transcript, and the diagnosis that unblocked it: nothing was ever *commanding* the peer's listener. Kills two long-standing beliefs — the 68-byte ACMPDU era is over (the peer emits 72 now and the fabric accepts it), and the peer's AVB core is a protocol engine, not a recording surface.
- **[6. The peer as an ATDECC controller (2026-07-26)](#6-the-peer-as-an-atdecc-controller-2026-07-26)** — The third role: a small la_avdecc tool that issues one `CONNECT_RX` and exits, making board↔board binds scriptable. Four notes that cost time, chiefly that ACMP `SUCCESS` is a control-plane verdict only and says nothing about the listener datapath accepting frames — and that the peer's own talker stays silent by design.
- **[Status (2026-07-25, end of campaign day)](#status-2026-07-25-end-of-campaign-day)** — What was proven on the bench that day, in one paragraph: gPTP client-locked at two hops, both board entities discovered, the listener bind, and the peer consuming the stream on the VLAN-2 sub-interface.

## 1. The endpoint stack, in order

A PipeWire AVB endpoint is three cooperating pieces — bring them up in this
order, each one checkable before the next:

1. **gPTP first.** `module-avb` reads clock state from a running `ptp4l`
   through its **read-only management socket**; without it the module retries
   forever and never creates a device. Run ptp4l with the gPTP profile,
   client-only (the board stays grandmaster), and a world-connectable RO
   socket. The peer keeps a launch helper for exactly this
   (`ptp-start.sh <iface>` — the argument is the interface). Check:
   `pmc -u -s <ro-socket> "GET PARENT_DATA_SET"` answers, and the reported GM
   is the board's clockIdentity.
2. **A running PipeWire core.** `pipewire-avb` is a **client** of an existing
   core — launch it in the runtime dir of the session whose core it should
   join (`XDG_RUNTIME_DIR=/run/user/<uid>`). A missing core surfaces as the
   confusing error "can't connect: Host is down".
3. **The AVB daemon.** `pipewire-avb -v`, from a build whose binary and
   `libpipewire` **versions match** (see Section 4). It needs raw-socket privilege
   (run as root, or grant `CAP_NET_RAW`); it still joins the user's core via
   the runtime dir.

Two config keys bite (in `pipewire-avb.conf`):

- `ifname` — the AVB-facing interface of THIS host. A conf copied from
  another machine carries the wrong one.
- `ptp.management-socket` — must be the path ptp4l **actually binds today**;
  a stale path produces an endless
  `Failed to connect PTP management socket` loop.

## 2. What "working" looks like (log signals)

In the `-v` log, in order:

- the management-socket retry loop **stops**;
- `GM ID: IEEE1588-2008:<the board's clockIdentity>` — the endpoint follows
  the fabric grandmaster;
- `PTP currentDS: steps_removed=<hops> offset_from_master=<scaled-ns>` —
  scaled-ns is ns·2^16, so −393216 ≈ −6 ns; two hops = board → bridge → peer;
- `entity 68:...  advertise` — the endpoint's own ADP advertise;
- `entity 02:00:00:ff:fe:00:0001 available` (and `...:0002`) — it discovers
  the boards.

## 3. Binding the pilot tone to a stream

The tone is fabric-generated; the peer only ever sees a normal AAF stream.

**Talker side (board CSRs — the [`REGISTER_MAP.md`](../reference/REGISTER_MAP.md)
rows):**

1. `TONE_CTRL 0x6DC = 1` — the 1 kHz 0 dBFS exact-period pilot replaces the
   ADC samples on the talker channels (boot provisioning enables it on the
   talker board).
2. The stream must be armed: `AAF_CTRL 0x654` enable — **always write the
   VID-preserving value** (`0x00020003`-style; a bare enable that zeroes
   VID[27:16] floods the stream as best-effort — the recorded clobber
   incident).
3. Addressing + reservation are automatic in fabric: MAAP claims the DMAC
   (`eff_aaf_dmac`), lwSRP declares the stream and gates bandwidth. See
   [Section 1 of the dataplane walkthrough](../fpga/DATAPLANE_WALKTHROUGH.md#1-egress-a-captured-sample-becomes-an-aaf-frame-the-fabric-talker) for the
   full talker chain.

**Connecting the listener — three paths:**

- **An ATDECC controller** (Hive or la_avdecc from any allowed host) sends
  `CONNECT_RX` binding the peer's listener sink to the board talker — the
  peer itself can play that role (Section 6).
- **Milan fast-connect** (board-as-listener direction): the saved-state
  restore binds with no controller at all.
- **The peer's own ACMP** (PipeWire-initiated): supported by `module-avb`,
  but check frame length first — PipeWire-lineage stacks historically
  emitted **68-byte ACMPDUs**, and the fabric rejects anything under the
  1722.1 70-byte minimum by design (the length-validation rule in
  [testing guide](../testing/TESTING.md)'s field-validation notes). A
  silent no-bind from the peer is this, not a board fault.

**Recording + acceptance:** `pw-record` the AVB capture node on the peer,
move the wav off-host, analyze with the private test repo's `tone_thdn.py`.
The digital-path acceptance for the pilot is on the
[`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) `TONE_CTRL` row
(≤ −120 dBFS end-to-end; the generator itself is −148.1 dB).

## 4. The fault dictionary (all hit on 2026-07-25, in this order)

| Symptom | Cause | Fix |
|---|---|---|
| `pipewire` segfaults in `libpipewire-module-client-node.so` at AVB load | binary compiled against one libpipewire, linking another (version skew); `pipewire-avb` may be a symlink to the skewed binary | run a **matched-version** build (the peer keeps a self-contained prefix install); check `pipewire --version` — "Compiled with" must equal "Linked with" |
| `can't connect: Host is down` at module load | no PipeWire core socket in the runtime dir the daemon was pointed at | launch with `XDG_RUNTIME_DIR` of a session with a live core |
| `SIOCGIFINDEX <iface> failed: No such device` | `ifname` in the conf names another machine's interface | set this host's interface |
| `Failed to connect PTP management socket` loop | ptp4l not running, or `ptp.management-socket` points at a path ptp4l no longer binds | start gPTP first; make the conf path match `ss -xl` truth |
| Daemon healthy but no bind from the peer | nobody commanded the listener - the peer never fast-connects to a talker it has no saved state for | send one `CONNECT_RX_COMMAND` from any host on the AVB LAN (Section 5) |
| Registry tools (`pw-dump`, `pw-cli ls`, `pw-link`) hang or return an empty list against the AVB core | the daemon's own core has no session manager; also its metadata global has a broken protocol marshal that aborts full-registry clients | don't manage the AVB core with registry tools; the AVB/Milan plane needs none of them (Section 5) |

## 5. The bind, as it actually ran (2026-07-25, late)

The missing piece was never the peer's ACMP - it was that **nothing ever
commanded its listener**. A Milan listener fast-connects only to a talker it
has *saved state* for; a first-ever bind needs one `CONNECT_RX_COMMAND` from
a controller. The bench had no controller host on the AVB LAN, so the talker
board itself played controller: a ~100-line one-shot tool (raw `AF_PACKET`,
spec-exact 70-byte ACMPDU - the 2 reserved tail bytes included) sent the
command from the board's own Linux.

The exchange, end to end:

```
board ctl  > CONNECT_RX_COMMAND  len=70  listener=<peer>.0  talker=<board>.0
peer log   > got ACMP connect-rx-command
peer log   > Listener probe complete: stream_id=0x0200000000010000
             dest_mac=91:e0:f0:00:9e:f5 vlan=2          (talker answered in 165 us)
peer log   > listener RX via VLAN sub-iface <iface>.2 (vid 2)
peer log   > join 91:e0:f0:00:9e:f5
peer log   > pw stream created
board ctl  < CONNECT_RX_RESPONSE len=72  status=0 (SUCCESS)
```

Two long-standing beliefs died that night:

- **The 68-byte era is over.** The peer's stack emits 72-byte ACMPDUs now -
  past the 1722.1 70-byte minimum - and the fabric's length-validating
  parser accepts them. Peer-initiated probes bind fine.
- The peer's AVB core is a **protocol engine, not a desktop audio host**: its
  stream nodes live in-process, the registry tooling around it is broken
  (metadata marshal defect), and `pw-record` against it is not a supported
  surface in the current bench build. Record at a **board's PCM ring**
  instead (`pcm_ring_dump` → `tone_thdn.py`, the analyzer's canonical
  input) - that is also the measurement the acceptance limits are written
  against.

## 6. The peer as an ATDECC controller (2026-07-26)

The peer host has a third role beyond listener and talker: **controller**.
Nothing in the fabric needs it — Milan fast-connect and the board-side
one-shot of Section 5 both work -- but a controller on the AVB LAN is what makes
*board ↔ board* binds scriptable, and it exercises the same ACMP surface a
real deployment would use.

The shape that works: a small **la_avdecc** command-line tool (the library's
`Controller` entity, built from the peer's own checkout) that issues one
`CONNECT_RX` / `DISCONNECT_RX` and exits:

```
bind-ctl <iface> <talker_entity_id> <talker_uid> <listener_entity_id> <listener_uid> [disconnect]
```

Notes that cost time to rediscover:

- **The controller is a full entity.** It advertises itself and discovers
  before it commands. Its socket must actually receive the ATDECC
  multicast (`91:E0:F0:01:00:00`) — raw-socket tools that skip the
  promiscuous/multicast join see their responses dropped by the NIC, the
  rule recorded in
  [`../findings/BENCH_TOPOLOGY.md`](../findings/BENCH_TOPOLOGY.md).
- **Trust the response, not the exit code.** The status that matters is the
  `SUCCESS` in the printed `CONNECT_RX_RESPONSE`; a wrapper's exit code can
  be inverted or lose the ACMP status entirely.
- **A talker uid > 0 is a real probe, not a shortcut.** Since
  `VERSION 0x0001_000C` the fabric answers `CONNECT_TX`/`PROBE_TX` for
  every talker uid `0..N-1` with `dmac = MAAP base + uid`, so binding a
  listener to uid *j* is the honest per-stream path — that is how the
  64-slot channel-map walk arms one stream at a time
  ([Section 12 of `../CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md#12-silicon-validation-the-first-crossbar-walk-2026-07-25)).
- **`SUCCESS` is a control-plane verdict only.** ACMP success means the
  binding was accepted; it says nothing about frames being accepted by the
  listener datapath. Confirm on the listener with `AVTPRX_STAT`/`FRX` and
  the RX latency taps — see the accept blocker in
  [troubleshooting guide](../limitations/TROUBLESHOOTING.md#section-21-acmp-says-success-the-listener-declares-itself-bound---and-not-one-frame-is-accepted-root-caused-and-fixed-version-0x000f-mechanism-confirmed-on-silicon-2026-07-26).

**The peer's own talker stays silent by design.** `module-avb` creates the
talker stream node, but the AVB core runs **without a session manager**, so
until an audio client is routed into that sink it produces no AVTP at all.
Waiting for peer-originated frames as a test stimulus is a dead end; drive
the experiment from a board talker (whose t0 is always-on once armed)
instead.

## Status (2026-07-25, end of campaign day)

Proven on the bench, all through PipeWire on the peer: gPTP client-locked to
the board grandmaster through the bridge (`steps_removed=2`, ≈ −6 ns), both
board entities discovered, **the Milan listener bind transcript above**, and
the peer consuming the stream (VLAN-2 sub-interface, stream DMAC joined).
The all-channels pilot sweep and per-channel identity ran on the
channel-map bitstream the same night - results live with the campaign notes
(see [`../CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md) for the map ABI).

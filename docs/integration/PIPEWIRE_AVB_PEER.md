<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->
# Using a PipeWire host as the AVB peer — and binding the pilot tone to a stream

How to stand up a plain Linux box as a **PipeWire-native AVB endpoint**
(listener/talker) against the boards, and how to get the pilot tone flowing
from the talker's CSRs into a bound stream. Everything here was verified on
the bench 2026-07-25; the fault list at the end is real history, not theory.

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
   `libpipewire` **versions match** (see §4). It needs raw-socket privilege
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
   [`../design/AUDIO_STREAMING.md`](../design/AUDIO_STREAMING.md) §2 for the
   full talker chain.

**Connecting the listener — three paths:**

- **An ATDECC controller** (Hive or la_avdecc from any allowed host) sends
  `CONNECT_RX` binding the peer's listener sink to the board talker.
- **Milan fast-connect** (board-as-listener direction): the saved-state
  restore binds with no controller at all.
- **The peer's own ACMP** (PipeWire-initiated): supported by `module-avb`,
  but check frame length first — PipeWire-lineage stacks historically
  emitted **68-byte ACMPDUs**, and the fabric rejects anything under the
  1722.1 70-byte minimum by design (the length-validation rule in
  [`../SPEC_TRACEABILITY.md`](../SPEC_TRACEABILITY.md)'s tsn_gen notes). A
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
| Daemon healthy but no bind from the peer | nobody commanded the listener - the peer never fast-connects to a talker it has no saved state for | send one `CONNECT_RX_COMMAND` from any host on the AVB LAN (§5) |
| Registry tools (`pw-dump`, `pw-cli ls`, `pw-link`) hang or return an empty list against the AVB core | the daemon's own core has no session manager; also its metadata global has a broken protocol marshal that aborts full-registry clients | don't manage the AVB core with registry tools; the AVB/Milan plane needs none of them (§5) |

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

## Status (2026-07-25, end of campaign day)

Proven on the bench, all through PipeWire on the peer: gPTP client-locked to
the board grandmaster through the bridge (`steps_removed=2`, ≈ −6 ns), both
board entities discovered, **the Milan listener bind transcript above**, and
the peer consuming the stream (VLAN-2 sub-interface, stream DMAC joined).
The all-channels pilot sweep and per-channel identity ran on the
channel-map bitstream the same night - results live with the campaign notes
(see [`../CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md) for the map ABI).

# Gateware `0x000B` → `0x0013` — what changed, and what you must do

*Written 2026-07-26, for someone whose board is running `VERSION 0x0001_000B`.*

> **Superseded in part by `0x0014` (2026-07-27): the egress map is FIVE queues,
> not six — and `0x0014` is now BUILT, PLACED, TIMING-MET AND FLASHED**
> (3 seeds, best WNS +0.147 ns, 99.65 % slice occupancy, running on the AX7101;
> [`../findings/FLASH_0x0014_0727.md`](../findings/FLASH_0x0014_0727.md)).
> The six-queue map of Section 2 did not fit the AX7101 -- three Vivado seeds
> failed placement 282 slices short with LUTs at 99.84 % of capacity — so the
> spare queue was dropped and the map was compactly renumbered: **q4** CBS SR
> class A · **q3** CBS SR class B · **q2** gPTP · **q1** control · **q0** best
> effort. Everything Section 2 says about *why* the order changed still holds; the
> indices, `CAP.num_queues` (5), the CBS window (`0x400`–`0x49F`), the
> `CLS_TC_QUEUE_MAP` reset (`0x004898C0`) and the `LWSRP_CTRL` reset (`0x10`,
> queue 4) do not. Current values are in
> [`../reference/EGRESS_QUEUE_MAP.md`](../reference/EGRESS_QUEUE_MAP.md) and
> [`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md), which win over
> this page.

Eight minor versions landed in one day. This page is organised by **what you
have to do differently**, not by what was built. Each section says whether it
changes behaviour at reset, whether it needs a reflash, and where the real
detail lives — this page is a router, not a second copy of the reference docs.

Read `VERSION` at CSR offset `0x004` to find out where you are. The full
per-version changelog is the `VERSION` parameter comment in
[`hdl/common/csr/milan_csr.sv`](../../hdl/common/csr/milan_csr.sv) and the
`0x004` row of [`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) —
both are maintained with the RTL and win over this page.

---

## Contents

- **[The short version](#the-short-version)** -- A six-row "if you… then…" router. Find your situation, jump to the one section that concerns you, and note the line under it: everything in Sections 1–7 is gateware and reaches no board without a reflash.
- **[1. The listener blocker is fixed — and your board is probably still on the workaround](#1-the-listener-blocker-is-fixed--and-your-board-is-probably-still-on-the-workaround)** -- The two layers that only bite together -- a globally shared staging pair, and an arm latch that clears only on reset. Read the proof paragraph carefully: silicon proves the *bug* (by causation on a pre-fix board), the *fix* is proven by two Verilator regressions, so the stage-before-commit workaround stays load-bearing until you confirm `VERSION ≥ 0x000F` on the board itself.
- **[2. Six egress queues, in 802.1Q order — a breaking ABI change](#2-six-egress-queues-in-8021q-order--a-breaking-abi-change)** -- Partly superseded, and the section says which part: the convention (higher index = higher priority) is permanent, but every index and reset word here is one version stale -- `0x0014` dropped the spare queue and renumbered. Still current: any code writing `CLS_TC_QUEUE_MAP` must be rewritten, and every queue powers up unshaped on purpose.
- **[3. Control traffic is classified by destination MAC — and it ships ON](#3-control-traffic-is-classified-by-destination-mac--and-it-ships-on)** -- Why a documented queue row was dead on the wire for months: MAAP/MSRP/MVRP and the 1722.1 trio are untagged and carry no PCP, so a PCP-keyed table could never route them. Now keyed on reserved DMAC. `CLS_CTRL` reads `0x5` at reset, and clearing bit 2 restores the old wire behaviour bit-for-bit -- a clean bisect lever.
- **[4. lwSRP NxN — every t>0 talker row had been refused](#4-lwsrp-nxn--every-t0-talker-row-had-been-refused)** -- An off-by-a-table-size: rows sized `max(L,T)` while the window maps talker *t* to row `(L−1)+t`, so every talker above t=0 sat past the end and had its admission gate pinned shut. The observable improvement is that an out-of-range row now reads `0xDEAD` instead of silently aliasing row 0's reservation.
- **[5. RMON counts again — and now tells you when it does not](#5-rmon-counts-again--and-now-tells-you-when-it-does-not)** -- `i_mac_events` was tied to 0 at both SoC wiring sites, so the whole STAT window read zero for months while every testbench passed. The durable half is `STATS_CAP` (`0x204`): a per-lane mask saying whose zero is a measurement. Also the counter views now saturate rather than truncate -- a real 51,523 mismatch was 79 % of the way to a roll that would have counted *down*.
- **[6. The playback chain reaches the line-out](#6-the-playback-chain-reaches-the-line-out)** -- The ALSA playback ring previously had no route to the DAC at all. The crossbar gained a host-ring source and the feed mux now picks the DAC's source *and its pace*, so a playback ring reaches the line-out with no inbound stream. Additive: `CHMAP_CTRL[0] = 0` is bit- and cycle-identical to before.
- **[7. New instrumentation you did not have](#7-new-instrumentation-you-did-not-have)** -- Three read-only probe groups in one table. The important one is `APRB` at `0x8B4`: every other RX counter lives *downstream* of the stream-table match, so a listener accepting nothing read zero everywhere with no way to separate parse failure from match failure -- which is why Section 1 took so long.
- **[8. Landed but not reachable from software yet](#8-landed-but-not-reachable-from-software-yet)** -- Three things in the tree that you cannot use yet, stated so nobody hunts for a missing register: the persistence journal (CSR group specified, not wired), the CTF fault trace (its target partition has never been booted), and AES3 (no shipping board config selects it).
- **[9. Build, CI and the builder](#9-build-ci-and-the-builder)** -- Four gate changes. Verilator is pinned and built from source for a measured reason -- 5.020 cannot build four suites and 5.032 reads back zeros on six `aecp` checks. The builder now writes the `0x680` reset words into a header `` `include ``-d by `milan_csr.sv`, so config and register resets cannot drift, and the tie-off check went from informational to failing.
- **[10. Requirements closed this round](#10-requirements-closed-this-round)** -- The eight `REQ-*` ids that closed, and where their normative text and status live.
- **[Upgrade checklist](#upgrade-checklist)** -- Six ordered steps for the actual upgrade, including the one people skip: run the host-plane smoke test *first*, because a build with perfect fabric paths can still ship with a dead host plane.

## The short version

| If you… | then… |
|---|---|
| have a board on `0x000B` and it listens fine today | you are running the **workaround**, not a fix. See Section 1. |
| have software that reads `CAP.num_queues` or writes `CLS_TC_QUEUE_MAP` | **it will break.** The queue count and the field packing both changed. See Section 2. |
| have software that trusts a zero in the `0x210`–`0x230` STAT window | read the new `STATS_CAP` (`0x204`) first. See Section 5. |
| run more than one talker with lwSRP enabled | every `t>0` talker row was being refused. See Section 4. |
| want audio out of the line-out from an ALSA playback ring | that path did not exist before `0x000E`. See Section 6. |
| just want your CI green | the sweep, the yosys check and the conformance suite are all gates now. See Section 9. |

**Everything in Sections 1–7 is gateware.** None of it reaches a board without a
rebuild and a reflash.

---

## 1. The listener blocker is fixed — and your board is probably still on the workaround

**What was wrong.** A bound listener would report `SUCCESS`, declare itself
connected, and accept **not one frame**. It was blamed on the parser and on
place-and-route (that bitstream placed at 99.93 % slice occupancy, which made
"correct in sim, wrong in silicon" a plausible story). Both were wrong.

The fault was **entry-0 provisioning**, in two layers that only bite together:

1. `win_commit_glue` in `milan_datapath.sv` staged the `0x800` window's
   `SID_LO`/`SID_HI` in **one global register pair shared by every index**, and
   its commit guard asked *"is some sid staged?"* rather than *"was a sid staged
   for **this** index?"*. So a route-flags-only `CTRL` write at index 0 armed
   entry 0 with whatever sid another listener had staged earlier.
2. `KL_stream_table` set `ovr_armed_r[idx]` on **any** write and cleared it
   **only on reset**. Once index 0 was armed, entry 0 permanently stopped
   aliasing the ACMP bound record — **there was no runtime path back**.

**What was done.** `VERSION 0x000F` tags the staging with the index it was
staged for, and makes `{en=0, sid=0}` a **release-to-alias** so entry 0 returns
to the ACMP record at runtime.

**How well it is proven, precisely.** The *mechanism* is confirmed on silicon by
**causation** — the trap was triggered deliberately on the deployed board, the
listener went deaf, and re-staging recovered it
([`../findings/STRESS_0726.md`](../findings/STRESS_0726.md) Section D). That board was
still carrying the pre-fix `0x000B`, so what silicon proves is the *bug*, not
the *fix*. The fix is proven by two Verilator regressions with negative legs:
[`tb/verilator/milan_dp`](../../tb/verilator/milan_dp) `sim_nxn.cpp` TRAP-1 (N=4 and N=8, through the real CSR
window) and [`tb/verilator/avtp_parser`](../../tb/verilator/avtp_parser) `sim_tbl.cpp` T6 (table level, from
reset).

**What you must do.**

* **On a board still at `0x000B`–`0x000E`:** the workaround stands — always
  stage `SID_LO`/`SID_HI` *for the index you are about to commit*, then write
  `CTRL`. Never issue a route-flags-only `CTRL` at an index you did not stage.
* **After reflashing past `0x000F`:** the ordering rule stops being load-bearing,
  and an `en=0` eviction now hands entry 0 back to ACMP instead of detaching it.

Full symptom→cause walk, with the register reads:
[`../limitations/TROUBLESHOOTING.md`](../limitations/TROUBLESHOOTING.md) Section 21.

## 2. Six egress queues, in 802.1Q order — a breaking ABI change

> **Read the banner at the top of this page before this section.** `0x0014`
> made it **five** queues. The *convention* below (higher index = higher
> priority) is current and permanent; every *index, reset word and address* in
> this section is one version out of date. Current values:
> [`../reference/EGRESS_QUEUE_MAP.md`](../reference/EGRESS_QUEUE_MAP.md).

`VERSION 0x0011` took the egress from 4 queues to **6**, and reversed the
priority convention: **higher index is now higher priority**, which is what
802.1Q says and what the credit shaper needs.

| Register / constant | was | is |
|---|---|---|
| `CAP.num_queues` (`0x008[3:0]`) | 4 | **6** |
| CBS window at `0x400`, stride `0x20` | `0x400`–`0x47F` | **`0x400`–`0x4BF`** |
| `CLS_TC_QUEUE_MAP` (`0x310`) packing | 2 bits/entry, reset `0xE4` | **3 bits/entry, reset `0x006D2B00`** |
| `LWSRP_CTRL` class-A queue field (`0x680`) | `[3:2]`, reset 3 | **`[4:2]`, reset 5** (whole register reset `0x14`) |
| `CBS_EN_RST` | `4'b0000` | `6'b000000` — **still all-unshaped at reset** |
| AXIS `tdest` where routed | 2 bits | **3 bits** (`$clog2(6)`) |
| class-A queue | q0 | **q5** |
| best effort | q3 | **q0** |

The map `0x0011` introduced, top to bottom: **q5** CBS SR class A · **q4** CBS
SR class B · **q3** gPTP · **q2** control · **q1** deliberate spare · **q0**
best effort. The per-queue CBS reset slopes were re-derived —
450/150/50/50/25/25 Mb/s for q5…q0, still summing to the 75 % `REQ-CBS-03`
ceiling.

**`0x0014` dropped the spare and renumbered** (it did not fit the part): **q4**
class A · **q3** class B · **q2** gPTP · **q1** control · **q0** best effort;
`CAP.num_queues` 5, CBS window `0x400`–`0x49F`, `CLS_TC_QUEUE_MAP` reset
`0x004898C0` (still 3 bits/entry), `LWSRP_CTRL` reset `0x10` (queue 4), slopes
450/150/50/50/25 = 725 Mb/s. If you are upgrading straight from `0x000B`,
target those, not the table above.

**What you must do.**

* Any code that writes `CLS_TC_QUEUE_MAP` **must be rewritten** — the same 32-bit
  word means something else now. An entry naming a queue ≥ 6 is clamped to q0
  (it is not a power of two any more, so the clamp is load-bearing).
* Anything that hard-codes "q0 is class A" or "the lowest index wins" is inverted.
* `ndo_setup_tc` / `tc mqprio` mappings on the host need re-deriving against six
  traffic classes.
* **Every queue still powers up unshaped**, on purpose — shaping q0 at reset once
  paced all best-effort TX to ~250 Mbit/s
  ([`../findings/CBS_DEFAULT_SHAPING_BUG.md`](../findings/CBS_DEFAULT_SHAPING_BUG.md)).
  That has not changed.

Authority for all of this, including the argument for why gPTP sits *below* the
shaped classes: [`../reference/EGRESS_QUEUE_MAP.md`](../reference/EGRESS_QUEUE_MAP.md).

## 3. Control traffic is classified by destination MAC — and it ships ON

`VERSION 0x0012` implemented the q2 control row, which had been documented but
**dead on the wire**.

The reason it was dead is worth internalising: MAAP, MSRP, MVRP and the 1722.1
trio are **untagged link-local PDUs that carry no PCP at all**. Every classifier
table in the design keys on PCP, so an untagged control frame got the port
default `CLS_DEFAULT_PCP` and fell through to **best effort**. Expressing those
rows as a PCP mapping was fiction.

They are now keyed on the **reserved destination MAC**, with **no EtherType
precondition** — the same thing a bridge keys on, and the shape that leaves room
for RSTP BPDUs, which have no EtherType at all (their two octets at that offset
are an 802.3 length). The EtherType refines exactly one address:
`01-80-C2-00-00-0E` carries both gPTP `0x88F7` (→ q3) and MSRP `0x22EA` (→ q2).

**The behaviour change at reset:** new `CLS_CTRL[2]` (`ctrl_class`) **resets to
1**, so `CLS_CTRL` reads **`0x5`**, not `0x1`. This is the house pattern
inverted, deliberately: `CLS_CTRL[1]` ships off because it *restricts* an arm
silicon depends on; `CLS_CTRL[2]` ships on because it *implements* a row that
was never on the wire, and the frames it moves are on q0 today — q2 outranks q0,
so it cannot take service away from anything.

**What you must do.** Nothing, unless control traffic on q2 surprises you —
in which case clearing `CLS_CTRL[2]` restores `0x0011` wire behaviour
**bit-for-bit**, which makes it a clean bisect lever. Note the honest bound:
the fabric already emits ADP/ACMP/AECP/MAAP and the lwSRP PDUs **downstream** of
the classifier, so those never touched a queue. What actually moves from q0 to
q2 is **software**-originated control traffic.

Also new here: `REQ-CLS-05` (DEI sideband), `REQ-CLS-06` (back-to-back
line-rate parsing) and `REQ-CLS-07` (reserved-DMAC validation on the gPTP fast
path, `CLS_CTRL[1]`, still reset 0) all closed this round.

## 4. lwSRP NxN — every `t>0` talker row had been refused

`VERSION 0x0010`. The lwSRP context table was sized `max(L,T)`, but the `0x800`
window maps listener *k* to ctx row *k* and talker *t* to ctx row *(L−1)+t*. So
on any NxN shape **every talker row above t=0 sat past `N_CTX_P` and was
refused**, pinning those admission gates shut whenever lwSRP was enabled.

Rows are now sized **`L+T−1`**. Consequences you can observe:

* an out-of-range row reads **`0xDEAD`** at `A_STRMW_SRP` (`0x85C`) instead of
  silently aliasing row 0's live status and stream_id — the old behaviour
  reported the legacy pair's reservation for a row that was never provisioned;
* `LWSRP_STATUS[11]` is a **sticky shortfall flag** that latches whenever that
  happens;
* `LWSRP_TSPEC` (`0x690`) MaxFrameSize is now per-stream: a talker row derives
  `24 + 24*C` from its own TCTX channel count under the packetizer's clamp,
  instead of one global figure;
* the CRF media clock output became a bindable ACMP talker source at
  `talker_unique_id = N_STREAMS`.

Historical detail: [historical NxN architecture](../NXN_ARCHITECTURE.md) Section 3.4.1.

## 5. RMON counts again — and now tells you when it does not

`VERSION 0x0013`. `i_mac_events` was tied to **0 at both SoC wiring sites**, so
the whole `0x210`–`0x230` STAT window read zero on both boards for months —
while every testbench passed, because the testbenches drove the port the SoC
never drove.

Two things changed:

* **`KL_mac_rmon_events`** synthesises the event vector at the SoC's MAC
  boundary from what a soft MAC actually exposes: the TX/RX frame AXIS
  handshakes, the per-frame bad-frame flag (FCS failure or runt) and the
  monotonic FCS/preamble error counts. `RX_ERROR_BAD_FCS`, `RX_ERROR_BAD_FRAME`
  and `RX_FIFO_BAD_FRAME` now count on LiteEth builds, alongside the two
  good-frame lanes the datapath already derived.
* **`STATS_CAP` (`0x204`, RO, live)** is a per-lane capability mask. Bit *n* = 1
  means lane *n* at `0x210 + 4n` has a real source in this build; bit *n* = 0
  means it is **structurally silent** and its zero is *not a measurement*. The
  four MAC-internal lanes that genuinely have no source
  (`TX_ERROR_UNDERFLOW`, `TX_FIFO_OVERFLOW`, `TX_FIFO_BAD_FRAME`,
  `RX_FIFO_OVERFLOW`) are declared unsupported rather than faked from AXIS
  backpressure.

**What you must do.** **Read `STATS_CAP` before believing a zero.** An
`ethtool -S` implementation should surface unsupported lanes as unsupported, not
as 0.

Separately, `AVTPRX_STAT` (`0x6B8`) and `AVTPRX_ERR` (`0x6C0`) now **saturate**
their packed byte/half-word views of the underlying 32-bit STREAM_INPUT counters
instead of truncating. All-ones means *"at least this many — read the full
32-bit value at `A_STRMW_CNT` `0x830 + 4k`"*. Every value below the ceiling is
bit-identical to `0x0012`. This was not theoretical: on 2026-07-26 silicon a
`SEQ_NUM_MISMATCH` of 51 523 was 79 % of the way to a 16-bit roll that would
have counted **down**.

## 6. The playback chain reaches the line-out

`VERSION 0x000E`. `KL_pcm_tx` — the ALSA playback ring — had **no route to the
DAC at all**. The render crossbar gained a host-ring source (a `src` bit in the
map entry), and `KL_i2s_feed_mux` now picks the DAC source **and its pace**: the
listener tap, or the render crossbar driven by the 48 kHz media tick. So a
playback ring reaches the line-out with **no inbound AVB stream**.

`CHMAP_CTRL[0] = 0` passes the old listener render tap through bit- and
cycle-identically, so this is additive.

New probe group `0x8C8`–`0x8D0` (`PBK_STAT` / `PBK_FEEDS` / `PBK_RAILS`) reports
delivered frames, disarmed-render frames and the `KL_pcm_tx` rails.
Historical detail: [historical audio-streaming design](../design/AUDIO_STREAMING.md),
[`../CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md).

## 7. New instrumentation you did not have

Three probe groups landed, all read-only, all cheap:

| group | offsets | answers |
|---|---|---|
| `APRB` RX stream-parser probe (`0x000D`) | `0x8B4`–`0x8C4` | frames parsed, frames matched, and **the stream_id as lifted off the wire** — the first view *upstream* of the stream-table match |
| `PBK` playback probe (`0x000E`) | `0x8C8`–`0x8D0` | the host-ring → DAC path |
| `STATS_CAP` (`0x0013`) | `0x204` | which STAT lanes are real |

`APRB` matters more than its size suggests: **every other RX counter in the
datapath lives downstream of the stream-table match**, so a bound listener that
accepts nothing read zero everywhere with no way to tell parse failure from
match failure. That is precisely why Section 1 took so long. The ordered fault-finding
walk is in [`../fpga/DATAPLANE_WALKTHROUGH.md`](../fpga/DATAPLANE_WALKTHROUGH.md) Section 3.

## 8. Landed but not reachable from software yet

Stated plainly so nobody goes looking for a register that is not there:

* **The persistence journal.** At the time of this release the `KLJ1` record
  format, the journal engine and the replay path were in the tree and
  Verilator-proven, with the CSR ingest group `0x7B8`–`0x7C4` specified but not
  yet wired. **All of it was deleted on 2026-08-13** together with the AECP
  plane it lived in. Nothing in this device persists a binding across a power
  cycle today: the protocol processor's NVM face is answered by a blank-flash
  responder, so a restore walk always completes with zero records, and Milan
  v1.2 5.3.8.2 is not met. This release note is kept as the dated record of what
  was true at `0x0013`.
* **The CTF fault trace.** Design + host tooling are in [`sw/trace/`](../../sw/trace)
  (`test_trace_roundtrip.py` is a gate). The write target is a `/user` jffs2
  partition that **no board has yet been booted with**. The flash-wear budget is
  computed, not measured. See
  [`../design/TRACE_LOGGING.md`](../design/TRACE_LOGGING.md) and the generated
  [`../reference/TRACE_EVENTS.md`](../reference/TRACE_EVENTS.md).
* **AES3 / S-PDIF.** `KL_aes3_rx` and `KL_aes3_tx` exist, have a Verilator suite
  ([`tb/verilator/aes3`](../../tb/verilator/aes3)) and are yosys tops. They are not yet a selectable front
  end in a shipping board config — the builder validates AES3 shapes and marks
  unclockable ones as `ConfigError` (gate 21b).

## 9. Build, CI and the builder

* **CI now runs the RTL gates.** [`rtl.yml`](../../.github/workflows/rtl.yml)
  runs the full Verilator sweep ([`scripts/run_all_suites.sh`](../../scripts/run_all_suites.sh)), the Yosys
  portability sweep, **and the BDD conformance suite** as a gate.
  [`docs.yml`](../../.github/workflows/docs.yml) keeps the paper gates. Nothing
  on hardware runs automatically.
* **Verilator is pinned, and built from source.** CI builds `v5.050` at a pinned
  tag and caches it rather than trusting `apt`. This is not fussiness: 5.020
  (Ubuntu 24.04) **cannot build** four of the suites, and 5.032 (Debian trixie)
  builds but reads back zeros on six `aecp` checks. The RTL was deliberately not
  contorted to satisfy 5.020 — the construct it rejects is legal and synthesises.
  The measured table is in
  [`../testing/TESTING.md`](../testing/TESTING.md) Section 7.
* **The builder emits more, and `milan_csr` now consumes it.**
  `endstation_builder.py` gained the lwSRP reservation-table emitter
  (`lwsrp_table.json` / `.svh`) and the DT/driver-shape emitter
  (`platform_shape.json` / `milan-nic.dtsi`). Critically, the CSR-facing subset
  — the `0x680` reset words and the PriorityAndRank byte — is written to
  [`hdl/common/csr/gen/lwsrp_csr_defaults.svh`](../../hdl/common/csr/gen/lwsrp_csr_defaults.svh) and **`` `include ``-d by
  `milan_csr.sv`**, so the config and the register resets cannot drift apart.
  [`../ENDSTATION_BUILDER.md`](../ENDSTATION_BUILDER.md).
* **The tie-off allowlist is a gate.** [`scripts/check_tied_inputs.sh`](../../scripts/check_tied_inputs.sh) used to be
  informational; since 2026-07-26 it **fails** the yosys run on a
  never-overridden tie with no justified-tie entry. That is the RMON class of
  defect (Section 5) turned into a check -- it was informational precisely because three
  of its four warnings were expected, which is why the fourth went unread.

## 10. Requirements closed this round

`REQ-CLS-05` (DEI sideband) · `REQ-CLS-06` (back-to-back line-rate parsing) ·
`REQ-CLS-07` (reserved-DMAC validation) · `REQ-CLS-10` (untagged control
classified by destination MAC) · `REQ-MAC-02` (RX station-MAC address filter) ·
`REQ-PTP-05` (event-only timestamping) · `REQ-PTP-09` (C-VLAN-tagged gPTP
offsets) · `REQ-CBS-06` (slope fixed-point rounding).

Status at this release is preserved in [historical `TODO.md`](../../TODO.md);
the normative text is
[`../../REQUIREMENTS.md`](../../REQUIREMENTS.md).

---

## Upgrade checklist

1. **Rebuild and reflash.** Everything in Sections 1–7 is gateware. A gateware-only
   load will not boot — flash a matched image set
   ([`../integration/QSPI_FLASHBOOT.md`](../integration/QSPI_FLASHBOOT.md)).
2. **Run [`scripts/hostplane_smoke.sh`](../../scripts/hostplane_smoke.sh) on the board shell first**, before any
   other procedure. A build whose fabric paths are perfect can still ship with a
   dead host plane.
3. **Read back `VERSION` (`0x004`), `CAP` (`0x008`), `CLS_CTRL` (`0x300`) and
   `STATS_CAP` (`0x204`).** Expect `0x0001_0013`, `num_queues` = 6,
   `CLS_CTRL` = `0x5` — or, on a `0x0014` build, `0x0001_0014` and
   `num_queues` = **5** (Section 2 banner).
4. **Re-derive every `CLS_TC_QUEUE_MAP` write** against 3-bit packing (Section 2).
5. **Check `rx_queues` for your board.** The AX7101 8×8 config ships **1**
   because that is the layout its flashed boot chain maps; raising it to 2 moves
   every DMA window from `dma-ts` onward and is a reflash-gated change the
   builder refuses against a pinned `boot_chain_pin`
   ([`../reference/EGRESS_QUEUE_MAP.md`](../reference/EGRESS_QUEUE_MAP.md)).
6. **Stop relying on the stage-before-commit workaround** only once you have
   confirmed `VERSION ≥ 0x000F` on the board itself.

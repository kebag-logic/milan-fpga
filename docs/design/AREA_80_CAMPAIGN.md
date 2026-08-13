# The 80% campaign — what may go static, by clause

**Trigger (USER 2026-07-28):** if the m0019f reference builds (L2-32K,
`AreaOptimized_high` + `ExploreArea`) still fail placement, this campaign
executes. Target: **~80% LUT utilization** (≈50,700 of 63,400 on the
xc7a100t) — real headroom, not scraping under the DRC. From the measured
~61,000 that means **≈−10,300 LUTs**, which no single lever delivers: the
method is *static-conversion first* (this page), block diets second.

> **OUTCOME (2026-08-13): the biggest levers on this page were spent, but not
> by this campaign.** The whole legacy IEEE 1722.1 / SRP plane — AECP/AEM,
> ADP, ACMP talker and listener, the persistence journal and the lwSRP
> applicant — was **DELETED** and replaced by the pinned
> `protocol-processor` submodule. That is neither the static-conversion route
> of the verdict table nor the software route of the latency table: it is a
> **substitution**, and it is measured, in context, both sides on the same
> instrument, in
> [`../findings/PP_SHADOW_AREA_0812.md`](../findings/PP_SHADOW_AREA_0812.md)
> — **+6,956 LUT for the processor plane against −15,474 LUT removed.**
>
> Read the rest of this page as the *analysis record* it always was. Rows
> below that name a deleted module are marked; the razors themselves still
> apply to what is left, and the arithmetic at the bottom must **not** be
> combined with the findings figures — different instrument, different
> design, different shape.

**The razor:** for every runtime-configurable surface, ask what the
governing standard actually requires to be settable at run time on an
END STATION. Anything the clauses leave static — or explicitly declare
inert in our operating mode — becomes an elaboration-time constant from
`configs/endstation_*.yaml`, per the SW-defined-endstation directive
("Shape is STATIC, not a runtime poke"). A conversion NEVER changes wire
behaviour; it removes the machinery for changing behaviour nobody — not
software, not a controller, not a clause — is entitled to use.

## Contents

- **[Verdict table](#verdict-table)** — every runtime-configurable surface ruled MAY-STATIC or MUST-DYNAMIC with the governing clause quoted on the row; honest static total ≈0.9–1.9k LUTs, so the block-diet ledger follows. Rows whose block was deleted on 2026-08-13 are marked in place.
- **[AMENDED 2026-07-28 evening (USER): AECP STAYS IN FABRIC](#amended-2026-07-28-evening-user-aecp-stays-in-fabric)** — the software-AECP lane started and stopped the same evening on USER instruction: the 6.2k lever is off the table, its desk-proven responder skeleton parked unused.
- **[The latency axis (USER 2026-07-28, tightened same day): 100 ms is the line](#the-latency-axis-user-2026-07-28-tightened-same-day-100-ms-is-the-line)** — the second razor: planes with protocol deadlines ≤100 ms stay fabric, slower ones (AECP, ACMP, MAAP, ADP) run as software over CSRs; the arithmetic lands at ≈48.6k / 76.6%.

## Verdict table

| surface (CSR / fabric) | governing clause, verbatim where it decides | verdict | est. LUTs |
|---|---|---|---|
| CBS `adminIdleSlope`/credit words (`0x400`–`0x49F` RW paths into `traffic_shaping_core`) | 802.1Q-2018 34.3(c): "adminIdleSlope(N): The bandwidth … requested by management … **If SRP is in operation, this parameter has no effect**"; 34.3(d): operIdleSlope "is used by the credit-based shaper … as the idleSlope" | **MAY-STATIC.** lwSRP *is* SRP-in-operation and the granted slope already muxes into the shaped queue (`LWSRP_CTRL[4:2]` path). The admin words become constants (reset table), the slope engine folds; the words stay readable from the defaults ROM. | ~300–600 |
| Classifier maps `CLS_TC_QUEUE_MAP` / `CLS_PCP_TC_MAP` / `prio_regen` | 802.1Q 6.9.4 priority regeneration is a **Bridge Port** function; the PCP→class→queue association on an end station follows the SR class assignment fixed by the config (`srp.class_queue`) — no clause makes it management-settable on a PAAD | **MAY-STATIC** (keep `CLS_CTRL` mode bits — the 0x0012 ctrl_class enable is a documented behaviour toggle). Tables become the config-derived constants they already reset to. | ~200–400 |
| Datapath probe groups (parser 0x8B4–0x8C4, PBK 0x8C8–0x8D0, APRB) | none — diagnostics; the finding class they served (fabric-listener blocker, item-7 chain) is closed and TB-pinned | **PRUNABLE tier-1** (`--no-datapath-probes`), same discipline as LTAP: absent block declares itself | ~300–600 |
| Legacy flat regs aliasing window index 0 (the 0x0008 note) | none — a compatibility alias for pre-window software; the deployed boot chain uses the window | **DROP-CANDIDATE** (needs a deployed-software sweep first — gptp2csr.sh/S50milan grep) | ~100–300 |
| `MAAP` claim engine | IEEE 1722-2016 Annex B — dynamic allocation and defence IS the function | MUST-DYNAMIC | — |
| TCAM / rx_filter runtime entries | stream DMACs follow MAAP; the kernel shield installs at runtime | MUST-DYNAMIC | — |
| AEM dynamic surfaces (SET_STREAM_FORMAT, SET_NAME, SET_STREAM_INFO(MSRP_ACC_LAT), START/STOP, counters, GET_STREAM_INFO fields) | Milan v1.2 5.4.2.x "shall implement" table; 5.4.2.25 "shall implement and return" | MUST-DYNAMIC (this is the compliance surface itself). **2026-08-13: NOT IMPLEMENTED — the engine is deleted and the processor's AECP µCPU did not reimplement any of these commands. The device is reachable on AECP (it answers `READ_DESCRIPTOR` when a descriptor image is loaded, and echoes a conformant `NOT_IMPLEMENTED` at everything else), but an echo executes nothing: no format, no name, no transit time, no start/stop, no counters. The verdict was right; the surface is absent, which is a stated capability boundary and not a static conversion** | — |
| Channel-map crossbars (0x900 window) | no clause — but USER chmap64 directive (ALSA/PipeWire runtime mapping) | MUST-DYNAMIC (directive). **2026-08-13: the window is now the ONLY programmer of the map RAMs, so this verdict became structural** | — |
| lwSRP window CFG overrides | fabric self-provisions since 0x0015/0x0019; overrides are bring-up/test paths exercised by sim_nxn and bench recipes | KEEP (test surface). **2026-08-13: the applicant that read the provisioning words is deleted — DMAC / MaxFrameSize / MaxIntervalFrames / declare-bypass are now WRITE-ONLY SCRATCH that reach nothing. The policy words that still bite are the domain, slope and admission ones on the processor's face** | — |
| CLKV lease, `AAF_CTRL`, `CRFT_CTRL`, journal group | Milan 4.3.5.2 (tu shall), 5.3.7.3, 5.3.8.2 — the runtime-ness is the point | MUST-DYNAMIC | — |

A MUST-DYNAMIC verdict above answers *static vs runtime* only — it does
NOT award fabric. Where the dynamic behaviour lives is the latency table
below (MAAP is the example: its allocation MUST stay dynamic per Annex B,
AND it moves to software, because its fastest cadence is 500 ms).

Static-conversion honest total: **≈0.9–1.9k LUTs.** It does NOT reach −10.3k
alone; the campaign's second half is the block-diet ledger (in priority
order, from the measured hierarchy): `KL_aecp_response_builder` 5.7k (the
whale; already RAM-dieted once — the remaining mass is emit-engine source
selection and the batch rlen tables), `lwsrp` walker 2.6k, `milan_csr`
write-decode ~1–1.5k of its 4.5k (readback is ALREADY BRAM — `shadow_ram
[0:511]`, [`milan_csr.sv:1546`](../../hdl/common/csr/milan_csr.sv#L1546) — so the naive "move CSR to BRAM" is done;
what remains is decode sharing), depacketizer `frame_fifo` 1.2k (un-folded
by the rxq2 dynamic keep path — worth one focused look), and the
rxq2-sans-RSC SoC split (+4.3k went in with rx_queues 2; the D7 fix needs
the *steered second queue*, not the TCP-coalescing engine — separability
unverified).

**Ledger status 2026-08-13:** the first two entries — the response-builder
whale and the lwSRP walker, ~8.3k of the diet target — were not dieted, they
were **deleted with their planes**. Nobody wrote a smaller emit engine; the
engine left the design. `milan_csr`'s write-decode, the depacketizer FIFO and
the rxq2 split are untouched and still the open items.

## AMENDED 2026-07-28 evening (USER): AECP STAYS IN FABRIC

The AECP-to-software lane was started on the USER's instruction and STOPPED
the same evening on the USER's instruction, before any fabric change landed.
The 6.2k-LUT lever is OFF the table; the latency table below remains as the
*analysis* record, not a plan. What the lane produced stays PARKED and
harmless: [`avdecc/pack_aem_bin.py`](../../avdecc/pack_aem_bin.py) and `milan-tests-avb/fpga/aecpd/` (a
byte-exact, 283-check desk-proven software responder skeleton - never
packaged, never deployed, no fabric hook). The fit path is therefore the
m0019f reference flow (L2-32K + `AreaOptimized_high` + `ExploreArea`) plus
the static-conversion rows above; ACMP/MAAP moves are NOT pursued either
without an explicit USER instruction.

## The latency axis (USER 2026-07-28, tightened same day): 100 ms is the line

**The second razor, final form:** a plane earns fabric ONLY if the protocol
gives it a deadline at or under **100 ms**. Everything whose governing
timeout/cadence is above 100 ms is management by definition and runs as
SOFTWARE on the softcore out of DDR3, reading and writing fabric truth
through the CSRs. This REVISES the rev-2 "everything in fabric" direction;
the sub-100 ms plane stays fully fabric.

| plane | protocol deadline, from the PDF | verdict |
|---|---|---|
| AAF/CRF framing, zero-fill, packetizer/depacketizer, shaping, licence/admission gates | 125 µs class-A intervals; per-frame gating | FABRIC |
| gPTP timestamping | ns-scale capture | FABRIC |
| CLKV/tu stamping | per-frame (Milan 4.3.5.2 shall) | FABRIC |
| Table 5.4/5.16 counter ACCUMULATION | per-frame events (the 1 s observation interval is the reporting bin, not the event) | FABRIC (harvest/serve may be read by anything) |
| stream table, chan-map crossbars, PCM rings | per-frame / per-sample consumers | FABRIC (chmap also a USER directive) |
| lwSRP | MRP joinTime is 200 ms — ABOVE the line — but the rev-2 USER directive names lwSRP fabric explicitly, and its per-frame ADMISSION GATE is sub-100 ms regardless | FABRIC by NAME (the walker/registrar ~2.6k become eligible the day the name is released; the gate stays fabric either way) |
| **AECP/AEM command handling** | 1722.1-2021 inflight ~250 ms per command, controller retries | **SOFTWARE + DDR3** — returns **6,206 LUT + 9 RAMB36** |
| **ACMP protocol SMs** (probe/command/response, timeouts, fast-connect orchestration) | 1722.1-2021 Table 8-1 verbatim: CONNECT_TX 2000 ms, DISCONNECT_TX 200 ms, GET_TX_STATE 200 ms, CONNECT_RX 4500 ms, DISCONNECT_RX 500 ms, GET_RX_STATE 200 ms — **the FASTEST ACMP deadline is 200 ms** | **SOFTWARE + DDR3** — the SM writes binds into the fabric stream table over the proven CSR window path (the 4-devmem workaround was the existence proof); returns ~**2.6k LUT** (`KL_acmp_listener` 2.1k + responder 0.5k) |
| **MAAP** | 1722-2016 Table B.8: MAAP_PROBE_INTERVAL_BASE **500 ms**, ANNOUNCE_INTERVAL_BASE 30 s; defence rides the probe cadence | **SOFTWARE + DDR3** — software defence answers in ms against a 500 ms cadence; claim results program the TCAM exactly as today; returns ~**634 LUT** |
| ADP advertise/depart/discover | 2 s cadence (valid_time/2) | SOFTWARE (~200 LUT, do with the AECP move) |
| persistence journal fabric verify | boot-time replay, no runtime deadline | SOFTWARE-eligible (~408 LUT) — the CRC/shape refusal logic moves into the boot script that already drives 0x7B8; the E1 bind port stays as the fabric write surface |
| IDENTIFY, unsolicited notifications | human-scale | SOFTWARE with the AECP move |

**What "software" means concretely:** the control lane already classifies
these PDUs to the CPU queue; the responder is one C daemon owning the
protocol state machines, with `aem_overlay.json`/the builder outputs as its
model source (the ONE config still defines the entity) and the CSR windows
as its only view of live truth. The fabric keeps every per-frame effect
(gates, tables, counters, stamps); software keeps every conversation.

> **What actually happened instead (2026-08-13).** The conversations did not
> move to a Linux daemon on the softcore — they moved to a **second processor
> in fabric**: the pinned `protocol-processor` submodule, which owns ADP,
> ACMP and SRP in RTL and publishes its state to this fabric as class-D
> wires, consumed every clock rather than through a software-paced read. The
> latency table's premise ("above 100 ms ⇒ management ⇒ software") therefore
> did not decide this; the deciding facts were that the old planes cost
> 15,474 LUT in context and the replacement costs 6,956, and that a shadow
> (coexistence) build **did not place at all** — 12,530 slices required
> against 11,286 available. Two rows of that table are also now moot rather
> than pending: **MAAP stayed in fabric** (`KL_maap`, because the processor
> implements none by design), and **AECP is not in software either — it is a
> µCPU in that same fabric processor**. That µCPU has since landed: the device
> answers `READ_DESCRIPTOR` and returns a conformant `NOT_IMPLEMENTED` echo to
> every other AECP command. So the 6.2k row did not become a Linux daemon and
> did not stay empty; it became a micro-coded engine, and its cost is **not**
> inside the 6,956 LUT the findings page measures — that figure was taken with
> the AECP pop face tied off, and nothing has re-synthesised the plane since.
>
> One area consequence is worth stating because it changes the shape of the
> row, not just its size: **the entity model is no longer in fabric at all.**
> The µCPU's descriptor store reads it from DDR3 over a read-only master at a
> compile-time base, so any accounting on this page that still charges LUT or
> BRAM for an AEM descriptor ROM is stale. The reciprocal duty is a software
> one nothing in this repository discharges yet: no step turns an
> `endstation_*.yaml` into the image or writes it to DRAM, so on a stock build
> the region is unloaded and every `READ_DESCRIPTOR` answers
> `BAD_ARGUMENTS`. What the µCPU does **not** buy back either way is the
> AEM dynamic surface in the verdict table above — those functions remain
> unimplemented.

**Arithmetic at the 100 ms razor** (from the measured 61,039):
−6.2k AECP −2.6k ACMP −0.63k MAAP −0.2k ADP −0.4k journal-verify
−1.4k static conversions −1.0k probes/aliases ≈ **48.6k ≈ 76.6%** —
UNDER the 80% target with lwSRP still fabric by name, before touching
the walker, the csr decode, or the RSC split.

Every conversion lands with: the config key that pins it, the gate that
refuses a build whose constant disagrees with the config, a TB case where
behaviour could conceivably move, and its row here flipped to DONE with the
measured (not estimated) recovery.

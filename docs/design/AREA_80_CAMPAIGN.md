# The 80% campaign — what may go static, by clause

**Trigger (USER 2026-07-28):** if the m0019f reference builds (L2-32K,
`AreaOptimized_high` + `ExploreArea`) still fail placement, this campaign
executes. Target: **~80% LUT utilization** (≈50,700 of 63,400 on the
xc7a100t) — real headroom, not scraping under the DRC. From the measured
~61,000 that means **≈−10,300 LUTs**, which no single lever delivers: the
method is *static-conversion first* (this page), block diets second.

**The razor:** for every runtime-configurable surface, ask what the
governing standard actually requires to be settable at run time on an
END STATION. Anything the clauses leave static — or explicitly declare
inert in our operating mode — becomes an elaboration-time constant from
`configs/endstation_*.yaml`, per the SW-defined-endstation directive
("Shape is STATIC, not a runtime poke"). A conversion NEVER changes wire
behaviour; it removes the machinery for changing behaviour nobody — not
software, not a controller, not a clause — is entitled to use.

## Verdict table

| surface (CSR / fabric) | governing clause, verbatim where it decides | verdict | est. LUTs |
|---|---|---|---|
| CBS `adminIdleSlope`/credit words (`0x400`–`0x49F` RW paths into `traffic_shaping_core`) | 802.1Q-2018 34.3(c): "adminIdleSlope(N): The bandwidth … requested by management … **If SRP is in operation, this parameter has no effect**"; 34.3(d): operIdleSlope "is used by the credit-based shaper … as the idleSlope" | **MAY-STATIC.** lwSRP *is* SRP-in-operation and the granted slope already muxes into the shaped queue (`LWSRP_CTRL[4:2]` path). The admin words become constants (reset table), the slope engine folds; the words stay readable from the defaults ROM. | ~300–600 |
| Classifier maps `CLS_TC_QUEUE_MAP` / `CLS_PCP_TC_MAP` / `prio_regen` | 802.1Q 6.9.4 priority regeneration is a **Bridge Port** function; the PCP→class→queue association on an end station follows the SR class assignment fixed by the config (`srp.class_queue`) — no clause makes it management-settable on a PAAD | **MAY-STATIC** (keep `CLS_CTRL` mode bits — the 0x0012 ctrl_class enable is a documented behaviour toggle). Tables become the config-derived constants they already reset to. | ~200–400 |
| Datapath probe groups (parser 0x8B4–0x8C4, PBK 0x8C8–0x8D0, APRB) | none — diagnostics; the finding class they served (fabric-listener blocker, item-7 chain) is closed and TB-pinned | **PRUNABLE tier-1** (`--no-datapath-probes`), same discipline as LTAP: absent block declares itself | ~300–600 |
| Legacy flat regs aliasing window index 0 (the 0x0008 note) | none — a compatibility alias for pre-window software; the deployed boot chain uses the window | **DROP-CANDIDATE** (needs a deployed-software sweep first — gptp2csr.sh/S50milan grep) | ~100–300 |
| `MAAP` claim engine | IEEE 1722-2016 Annex B — dynamic allocation and defence IS the function | MUST-DYNAMIC | — |
| TCAM / rx_filter runtime entries | stream DMACs follow MAAP; the kernel shield installs at runtime | MUST-DYNAMIC | — |
| AEM dynamic surfaces (SET_STREAM_FORMAT, SET_NAME, SET_STREAM_INFO(MSRP_ACC_LAT), START/STOP, counters, GET_STREAM_INFO fields) | Milan v1.2 5.4.2.x "shall implement" table; 5.4.2.25 "shall implement and return" | MUST-DYNAMIC (this is the compliance surface itself) | — |
| Channel-map crossbars (0x900 window) | no clause — but USER chmap64 directive (ALSA/PipeWire runtime mapping) | MUST-DYNAMIC (directive) | — |
| lwSRP window CFG overrides | fabric self-provisions since 0x0015/0x0019; overrides are bring-up/test paths exercised by sim_nxn and bench recipes | KEEP (test surface; revisit only if the table above under-delivers) | — |
| CLKV lease, `AAF_CTRL`, `CRFT_CTRL`, journal group | Milan 4.3.5.2 (tu shall), 5.3.7.3, 5.3.8.2 — the runtime-ness is the point | MUST-DYNAMIC | — |

Static-conversion honest total: **≈0.9–1.9k LUTs.** It does NOT reach −10.3k
alone; the campaign's second half is the block-diet ledger (in priority
order, from the measured hierarchy): `KL_aecp_response_builder` 5.7k (the
whale; already RAM-dieted once — the remaining mass is emit-engine source
selection and the batch rlen tables), `lwsrp` walker 2.6k, `milan_csr`
write-decode ~1–1.5k of its 4.5k (readback is ALREADY BRAM — `shadow_ram
[0:511]`, `milan_csr.sv:1546` — so the naive "move CSR to BRAM" is done;
what remains is decode sharing), depacketizer `frame_fifo` 1.2k (un-folded
by the rxq2 dynamic keep path — worth one focused look), and the
rxq2-sans-RSC SoC split (+4.3k went in with rx_queues 2; the D7 fix needs
the *steered second queue*, not the TCP-coalescing engine — separability
unverified).

## The latency axis (USER 2026-07-28): what earns fabric at all

**The second razor:** classify every plane by its real deadline. At or
under ~1 s — media, timing, reservation reaction, counter accumulation —
stays in fabric. Over ~1 s — management, enumeration, "a human clicked
something" — has no claim on LUTs: it runs as SOFTWARE on the softcore out
of DDR3, reading fabric truth through the CSRs. This REVISES the rev-2
"everything in fabric" direction for the latency-insensitive plane only;
the media/timing planes stay fully fabric.

| plane | real deadline, by clause | verdict |
|---|---|---|
| AAF/CRF framing, zero-fill, packetizer/depacketizer, shaping | 125 µs class-A intervals (Milan 7.3.3, 802.1Q 34.6) | FABRIC, untouchable |
| gPTP timestamping | ns-scale capture | FABRIC |
| lwSRP registration + streaming licence reaction | joins/TA→LR reaction well under 1 s (802.1Q 35 timers; Milan 5.3.7.3 licence) | FABRIC (also an explicit rev-2 USER directive) |
| ACMP listener/talker SMs, fast-connect restore | Milan 5.5.3 command timeouts (sub-second), boot replay | FABRIC |
| Table 5.4/5.16 counter ACCUMULATION | 1 s observation interval, "shall implement and return" (5.4.2.25) | FABRIC counts; anything may read |
| CLKV/tu stamping | per-frame (4.3.5.2 shall) | FABRIC |
| MAAP defence | Annex B probe/defend windows (~hundreds of ms) | FABRIC (634 LUTs, mandatory, borderline — revisit last) |
| **AECP/AEM command handling** (enumeration, GET/SET descriptors, names, stream info composition) | 1722.1-2021 inflight timeout ~250 ms per command, controller retries; every command is a management action | **SOFTWARE + DDR3.** A softcore answers in single-digit ms from a DDR3-resident descriptor model, reading live words (counters, stream state) from the CSRs the fabric already exports. `aecp_listener` = **6,206 LUTs + 9 RAMB36 back** — the single biggest lever this campaign has, bigger than every static-conversion row combined |
| ADP advertise/depart/discover | 2 s advertise cadence (valid_time), discovery is user-visible but second-scale | SOFTWARE-eligible (only ~200 LUTs — do it for coherence when AECP moves, not for area) |
| Persistence journal writer | 5 s poll (already software); fabric ingest = boot-time verify | keep the small fabric verify (it is the torn-image guarantee) |

**The AECP-to-software lane, sketched honestly:** the control lane already
classifies AECP to the CPU-facing queue; the move is (1) stop diverting AEM
commands into `KL_aecp_top` — route them up the existing control RX path,
(2) a small C responder (the raw-socket tooling's serializer + the builder's
`aem_overlay.json` as its model source, so the ONE config still defines the
entity), (3) live fields keep coming from fabric CSRs (`A_STRMW_*`, diag
counters, ADP shape words), (4) the fabric keeps ONLY what has a sub-second
deadline: ACMP, the identify LED hook, and the unsolicited-notification
tickle if its timing demands it. The desk suites that pin the fabric
builder migrate to behave-on-board scenarios against the software responder
— the byte-exact oracle survives, it just tests the new home. This is a
FULL LANE (driver routing + daemon + test migration), not a tonight edit;
it runs only under this campaign's trigger.

With the AECP move, the ledger reaches the target arithmetic honestly:
~61,000 − 6,200 (AECP) − ~1,400 (static conversions above) − ~1,000
(probe/alias prunes) ≈ **52,400 ≈ 82.7%**, before touching the walker,
the csr decode, or the RSC split.

Every conversion lands with: the config key that pins it, the gate that
refuses a build whose constant disagrees with the config, a TB case where
behaviour could conceivably move, and its row here flipped to DONE with the
measured (not estimated) recovery.

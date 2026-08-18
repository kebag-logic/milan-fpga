[OBSOLETE + 2026-08-16]

# Milan v1.2 → FR/NFR dependency matrix

> ## STATUS 2026-08-13 — a `Today` column, because the control plane changed
>
> Every table in sections **A–H** now carries a **`Today`** column, and it is
> the first thing to read. The verdicts it uses:
>
> * **PP** — **OWNED BY THE PROTOCOL PROCESSOR.** This repository's own ADP
>   advertiser, ACMP talker/listener and lwSRP applicant are DELETED and their
>   duties moved to the protocol processor, wrapped by
>   `hdl/milan/KL_pp_shadow.sv` and instantiated unconditionally by
>   `hdl/milan/milan_datapath.sv`. It publishes a class-D wire face the fabric
>   consumes every clock (bind record, talker declaration, SRP
>   reservation/slope/domain). **The processor's AECP uCPU has now landed too**,
>   and it owns `READ_DESCRIPTOR` (0x0004) with all three status paths —
>   `SUCCESS` carrying `configuration_index` + reserved + descriptor,
>   `NO_SUCH_DESCRIPTOR` on a locate miss, `BAD_ARGUMENTS` on a bad
>   configuration index, both errors carrying the IEEE 1722.1 §7.4.5 4-byte
>   `{descriptor_type, descriptor_index}` stub — plus
>   `IDENTIFY_NOTIFICATION`-as-command → `BAD_ARGUMENTS` (§7.4.39.2 beats
>   §9.3.5.3.3) and the silent refusals (wrong `target_entity_id`; an AECP
>   *response* arriving as input: freed, counted, no reply).
> * **SERVABLE, NOT SUPPLIED** — the engine would answer, and this repository
>   builds nothing for it to answer FROM. It applies to the descriptor model:
>   the store fetches the entity model from main memory at a compile-time base
>   (`PP_DESC_BASE_P`, derived by the SoC as the top 1 MiB of `main_ram`), the
>   image generator lives in the submodule
>   (`protocol-processor/hdl/aecp/desc/gen_desc_image.py`), and **no step in
>   `sw/builder/`, `scripts/`, the SoC builder or the boot path produces its
>   JSON or loads DRAM**. On a stock build the header magic fails, the store
>   reports `configurations_count` = 0, and every `READ_DESCRIPTOR` answers
>   `BAD_ARGUMENTS` — the configuration range check runs before the locate, so
>   `NO_SUCH_DESCRIPTOR` (the locate-miss status) needs a loaded image to appear
>   at all. Enumeration is reachable — it is not working. Use the pair as a
>   discriminator: `BAD_ARGUMENTS` everywhere = no image or a corrupt one;
>   `NO_SUCH_DESCRIPTOR` = image loaded, that descriptor genuinely absent.
> * **❌ NOT IMPL** — **the command's FUNCTION is absent.** It is *answered*: the
>   uCPU replies to every unimplemented opcode, and to every unimplemented
>   message type (AEM, ADDRESS_ACCESS, VENDOR_UNIQUE/MVU), with a conformant
>   `NOT_IMPLEMENTED` echo — `message_type` + 1, correct length, correct
>   `controller_data_length`, `controller_entity_id` and `sequence_id` verbatim.
>   **That echo is a refusal, not coverage**: it discharges IEEE 1722.1 §9.3.5's
>   duty to respond and does nothing else. No ❌ row below is softened by it.
> * **live** — unchanged by the substitution.
>
> 🔴 **Milan Δ7 `ACQUIRE_ENTITY` (`NOT_SUPPORTED`, `owner_id` = 0) is NOT
> distinguished from the generic echo.** The microprogram for it EXISTS in the
> processor's ucode (`E_ACQ`) and nothing dispatches to it, so opcode 0x0000
> falls into `NOT_IMPLEMENTED` with everything else. A wiring gap, named as one.
>
> A **MANDATES** row that reads ❌ is a Milan v1.2 conformance gap, stated as
> such. That is the point of the column: this page's job is to say *why Milan
> forces a requirement*, and a requirement Milan forces does not stop being
> forced because the implementation was removed. The gap ledger is
> [`../MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md).
>
> **`Verify` tokens on a ❌ row still do not exercise the requirement.** Fired at
> this build they measure the `NOT_IMPLEMENTED` echo, which is worth asserting
> once as the conformance floor and is not the row's behaviour. The
> `tsn-gen` AECP/ACMP/ADP campaigns and the AECP/ACMP/ADP/lwSRP Verilator suites
> were deleted with the RTL; the **AAF** campaign survived, and the AECP
> behaviour above is graded by the submodule's own benches, which this
> repository's gates do not run.

This matrix traces each **Milan v1.2** requirement to the
[functional/non-functional requirements](FR_NFR.md) it drives, states **why the
Milan requirement makes that FR/NFR necessary**, and gives the **verification /
test** that proves it.

Read the pair [`FR_NFR.md`](FR_NFR.md) ⇄ this file: [`FR_NFR.md`](FR_NFR.md) says *what* the system must do
(+ the `Ver` method letter); this file says *why Milan v1.2 forces it* and *how it
is verified*, and which requirements are **not** Milan-driven.

## Contents

- **[How to read  -  dependency types](#how-to-read-----dependency-types)** — The three-way distinction the whole matrix turns on: MANDATES (omit it and you are non-conformant), CONSTRAINS (optional, but must respect a Milan invariant if built), ENABLES (informational).
- **[Verification method letters (as in FR_NFR.md)](#verification-method-letters-as-in-fr_nfrmd)** — One line expanding T / A / D / I, shared with the requirements page.
- **[Verification artifacts (tokens used in the \*Verify\* column)](#verification-artifacts-tokens-used-in-the-verify-column)** — The legend for every token in the tables below: what each script, harness or daemon is and where it lives. Note the superseded row — the OpenAvnu `mrpd`/`maap` daemons are peer-side only — and the two 2026-08-13 corrections: the `tsn-gen` AECP campaigns have a responder again but mostly measure its `NOT_IMPLEMENTED` echo, and the Verilator legend now names `pp_shadow` in place of the deleted control-plane suites. Also the caveat on clause numbers: AEM and MVU are evidence-backed, the rest are by topic.
- **[A. Discovery  -  ADP  \*(Milan v1.2 Discovery; IEEE 1722.1-2021 §6)\*](#a-discovery-----adp--milan-v12-discovery-ieee-17221-2021-6)** — Four mandated behaviours, the three ADP ones now the protocol processor's, and the consequence of skipping each: no advertise means invisible, a wrong `available_index` means controllers act on stale models, an unstable `entity_id` breaks fast-connect.
- **[B. AEM descriptor model  \*(Milan v1.2 §5.3.3.1–5.3.3.11)\*](#b-aem-descriptor-model--milan-v12-533153311)** — Why the descriptor tree is not negotiable. The mandatory-set row is now **servable, not supplied** — the uCPU serves descriptors and nothing here builds the image — while IDENTIFY, names/config and the media-clock model stay ❌, the last of them being what leaves the CRF source unselectable.
- **[C. Enumeration & control  -  AECP/AEM  \*(Milan v1.2 §5.4)\*](#c-enumeration--control-----aecpaem--milan-v12-54)** — Seven rows against an engine that answers everything and implements one command. `READ_DESCRIPTOR` is the processor's; the rest draw a conformant `NOT_IMPLEMENTED` echo, which the AECP-status row grades honestly as the §9.3.5 duty met and per-command validation absent. Carries the Δ7 ACQUIRE_ENTITY wiring gap, and keeps `GET_DYNAMIC_INFO` marked SHOULD, not SHALL.
- **[D. Milan Vendor Unique  -  MVU  \*(Milan v1.2 §5.4.3.2)\*](#d-milan-vendor-unique-----mvu--milan-v12-5432)** — The Milan identity handshake, **NOT IMPLEMENTED in its entirety**: the engine recognises no vendor `protocol_id`, so it meets IEEE 1722.1 §9.6.2's unknown-protocol duty by construction and still refuses Milan's own — no MVU, not a Milan device.
- **[E. Connection management  -  ACMP  \*(Milan v1.2 §5.5)\*](#e-connection-management-----acmp--milan-v12-55)** — Connect/disconnect and the on-connect datapath programming, both now the protocol processor's class-D face; and fast-connect, which is ❌ — nothing in this device persists a binding across a power cycle.
- **[F. Streaming & stream formats  -  AVTP AAF  \*(Milan v1.2 §5.4 format match; §6 Base Audio Formats)\*](#f-streaming--stream-formats-----avtp-aaf--milan-v12-54-format-match-6-base-audio-formats)** — The format-adaptation pair: the talker's wire format is fixed (structurally), while `SET_STREAM_FORMAT` (served since 0x0053) stores, publishes and serves a controller's format choice per row - the wire reshape is the deferred half. Also where the 2 ms presentation-offset default is stated, and where the format DECLARATION is graded servable-but-unsupplied.
- **[G. Reservation & addressing  -  MAAP, SRP  \*(Milan v1.2 §5.6; 802.1Qat/Qak)\*](#g-reservation--addressing-----maap-srp--milan-v12-56-8021qatqak)** — Three rows tying dynamic multicast allocation, MSRP/MVRP registration and the ≤ 75 % SR limit together, with the reason they are one topic: the reservation grant is what gates transmit and sets the CBS slope. MAAP stays this fabric's; SRP moved to the protocol processor, along with one honest slope-ordering change.
- **[H. Media clocking & time  -  gPTP  \*(Milan v1.2 §5.7; 802.1AS; 1722-2016 §10 CRF)\*](#h-media-clocking--time-----gptp--milan-v12-57-8021as-1722-2016-10-crf)** — The ≤ 1 µs sync target, SFD-accurate hardware timestamps, the speed-independent PHC — and the sharpest single loss on the page: the CRF media clock can never be selected, so clock recovery is measured and never actuated.
- **[I. QoS datapath  -  802.1Q / 802.1Qav  \*(required by Milan for Class A)\*](#i-qos-datapath-----8021q--8021qav--required-by-milan-for-class-a)** — Two rows only, both fully covered by Verilator today: PCP classification into the shaped queue, and CBS bounding queuing latency to the 2 ms budget while isolating media from best-effort.
- **[J. Timing / performance NFRs  \*(Milan Class A service class)\*](#j-timing--performance-nfrs--milan-class-a-service-class)** — The Class A service class expressed as testable numbers — 2 ms bound, 8000 pkt/s per stream, media undisturbed by injected best-effort load — and how each is measured.
- **[K. Milan features intentionally OUT OF SCOPE](#k-milan-features-intentionally-out-of-scope)** — The three declared exclusions (seamless redundancy, rates above 192 kHz, AEM authentication), each with where the exclusion is recorded and how a controller can confirm it.
- **[L. Requirements NOT Milan-driven (project / platform)](#l-requirements-not-milan-driven-project--platform)** — The scale-up/scale-out and platform requirements Milan does not ask for, and the invariants it nonetheless imposes on them — notably that every softcore must see one coherent PHC.
- **[Coverage & test summary](#coverage--test-summary)** — The closing claim, its evidence split, and the two lists a reviewer usually wants: every MANDATES row that reads ❌ (the Milan v1.2 conformance gap this build ships with), and the one missing build step — nothing turns an endstation config into the descriptor image the AECP engine reads.

## How to read  -  dependency types

| Type | Meaning |
|------|---------|
| **MANDATES** | Milan v1.2 **requires** this behavior. Omitting the FR/NFR ⇒ **non-conformant**. |
| **CONSTRAINS** | Milan does **not** require the feature, but *if built* it must respect a Milan invariant. |
| **ENABLES** | A Milan capability a project NFR leverages (informational). |

## Verification method letters (as in [`FR_NFR.md`](FR_NFR.md))
**T** = test/interop · **A** = analysis · **D** = demonstration · **I** = inspection.

## Verification artifacts (tokens used in the *Verify* column)

| Token | Artifact | Location |
|-------|----------|----------|
| `avdecc_l2` | ADP watch / GET_COUNTERS / ACMP connect script | `srcs/the-private-test-repo/controller/avdecc_l2.py` |
| `tap_acmp` / `tap_sniff` | ACMP + frame taps | `srcs/the-private-test-repo/controller/` |
| `thdn` | audio THD+N quality check | `.../controller/pipewire_avb_thdn.py` |
| `soak` | peer-host-pair stream + clock-recovery soak (between the two bench PipeWire hosts) | `srcs/the-private-test-repo/scripts/pw1-pw0-clockrec-soak.sh` |
| `latency.md` / `gptp-phc-clock.md` | measurement methodology | `srcs/the-private-test-repo/docs/` |
| `tsn-gen` | byte-exact AECP PDU specs + BDD features. **There is an AECP responder again**: `aecp_read_descriptor` is a real byte-exact test once a descriptor image is in DRAM (against a stock build it measures `BAD_ARGUMENTS`, i.e. the image gap), and every other AECP yaml measures the `NOT_IMPLEMENTED` echo's header discipline — the conformance floor, never command coverage. The repo-side AECP/ACMP/ADP/legacy fuzz campaigns are deleted; only the **AAF** campaign survives | `software-defined-tsn-stack/.../1722_1/aecp/*.yaml`, `.../tests/aecp_behave/features/*.feature`, `protocols/milan/aecp_read_descriptor.yaml` |
| `vtb:<n>` | Verilator self-checking harness. `ls tb/verilator/` is authoritative; `pp_shadow` is the protocol processor's lane, and the `aecp` / `acmp` / `acmp_lstn` / `adp` / `lwsrp*` / `persist` / `aempatch` suites are deleted with their RTL | `tb/verilator/<n>` (`cbs`, `shaper_core`, `cls`, `ptp`, `ptp_sync`, `csr`, `pp_shadow`, `milan_dp`) |
| `Hive` | AVDECC controller (enumerate/lock/connect/identify) | external |
| `ptp4l`/`phc2sys`, `ethtool`, `tc cbs` | linuxptp + Linux net tooling | on-target |
| `mrpd` / `maap` | OpenAvnu daemons — SUPERSEDED 2026-07-12: SRP/MAAP left software. **Re-pointed 2026-08-13**: SRP is now the **protocol processor's** (the lwSRP engine is deleted), MAAP is still this fabric's `KL_maap`; see [ARCHITECTURE_HW_SW_SPLIT.md](../ARCHITECTURE_HW_SW_SPLIT.md) | peer-side only |
| `CONF` | the **Milan conformance plan** as recreated by the private bench suite | private test repo |

> Clause numbers for AEM (§5.3.3.x) and MVU (§5.4.3.2) are evidence-backed; other
> Milan clause numbers are by **topic**  -  verify against the Milan v1.2 PDF.

---

## A. Discovery  -  ADP  *(Milan v1.2 Discovery; IEEE 1722.1-2021 §6)*

| Milan requirement | Dep | FR/NFR | Today | Why necessary | Verify |
|-------------------|-----|--------|-------|---------------|--------|
| Periodic `ENTITY_AVAILABLE`, `available_index` monotonic per state change | MANDATES | FR-DISC-01, FR-DISC-04 | **PP** — the processor's ADP engine; `adp_next_avail_index_o` is the one live word of the `0x600` `A_ADP` group | No advertise / wrong index ⇒ device invisible or controllers act on **stale** models. | T  -  `avdecc_l2 listen`; `vtb:pp_shadow`; `CONF` |
| Answer `ENTITY_DISCOVER` (global + targeted) | MANDATES | FR-DISC-02 | **PP** | Controllers probe; ignoring DISCOVER ⇒ can't be brought online on demand. | T  -  `Hive` discover; `avdecc_l2 listen`; `vtb:pp_shadow` |
| `ENTITY_DEPARTING` on shutdown/link-down | MANDATES | FR-DISC-03 | **PP** — note the `A_ADP_DIAG` depart counters are **structural zeros** now, so this is a wire observation only | Otherwise controllers keep dead entities/connections. | T  -  `avdecc_l2 listen` + `tap_sniff` (observe departing on link down) |
| Stable EUI-64 `entity_id` (MAC-derived) | MANDATES | FR-DISC-05 | **live** — `entity_id` is still written once per boot at `0x600` and handed to the processor. Note the rest of that group (entity_capabilities, valid_time, association_id, controller_capabilities, interface_index) is **write-only scratch**: it reads back what software wrote and no longer reaches the wire | Fast-connect keys on a stable id; a changing id breaks reconnection. | A,T  -  inspect derivation; power-cycle, confirm id unchanged (`avdecc_l2 listen`) |

## B. AEM descriptor model  *(Milan v1.2 §5.3.3.1–5.3.3.11)*

| Milan requirement | Dep | FR/NFR | Today | Why necessary | Verify |
|-------------------|-----|--------|-------|---------------|--------|
| Mandatory descriptor set (ENTITY…STRINGS) | MANDATES | FR-ENUM-02 | **SERVABLE, NOT SUPPLIED** — the uCPU's descriptor store serves `READ_DESCRIPTOR` out of main memory, and nothing in this repository builds or loads the image it reads (the fabric AEM ROM and its consumer are deleted; the image generator is the submodule's and no build step drives it). On a stock build enumeration answers `BAD_ARGUMENTS` for every descriptor (the configuration range check precedes the locate, and an invalid image reports a count of zero), so **Milan's mandatory set is unmet today** — by a missing build step, not a missing engine | Milan fixes the tree a PAAD exposes; missing descriptors ⇒ unusable/non-conformant. | T,I  -  `Hive` enumerate + `tsn-gen aecp_read_descriptor` (needs an image in DRAM first); inspect vs entity JSON |
| Media-clock model: CLOCK_DOMAIN over CLOCK_SOURCEs (Internal/stream/CRF) | MANDATES | FR-CLK-03 | **❌ NOT IMPL, with teeth.** The descriptors are servable-not-supplied like the rest of the tree; the SELECTION is simply absent. `SET_CLOCK_SOURCE` is unimplemented — it draws the `NOT_IMPLEMENTED` echo — and it was the only writer of the live `clock_source_index`; it is pinned at 0 (INTERNAL) for the life of the build, so **the CRF media clock can never be selected**, `KL_mmcm_drp_servo` and the `KL_media_nco` packet-grid servo are structurally off, and `A_MCSRV_STAT` (`0x8F8`) reads its idle. `KL_crf_rx` still parses, counts and reports — it just cannot steer | Nothing to select/lock without the model. | T  -  `Hive` read + SET_CLOCK_SOURCE; `avdecc_l2` |
| IDENTIFY CONTROL (§5.3.3.10) | MANDATES | FR-MGT-01 | **❌ NOT IMPL** — `o_identify` is tied 0, so the indicator is structurally dark, and SET_CONTROL is unimplemented (it draws the `NOT_IMPLEMENTED` echo), so nothing can light it. Unrelated and not a substitute: `IDENTIFY_NOTIFICATION` arriving as a COMMAND is answered `BAD_ARGUMENTS`, which is an inbound-refusal rule, not identification | User must physically locate the device. | T,D  -  `Hive` SET_CONTROL identify; observe device |
| Names/config settable & persist | MANDATES/SHOULD | FR-CTRL-02, FR-MGT-02 | **❌ NOT IMPL** on both halves: SET_NAME and SET_CONFIGURATION are unimplemented (both draw the `NOT_IMPLEMENTED` echo, which changes nothing), and there is no persistence — `KL_persist_journal` is deleted and the processor's NVM face is a BLANK-FLASH responder (reads `0xFF`, writes accepted and discarded) | Configuration model + labelling. | T  -  `tsn-gen aecp_set_name / set_configuration`; reboot + re-read |

## C. Enumeration & control  -  AECP/AEM  *(Milan v1.2 §5.4)*

**Section C is answered and almost entirely UNIMPLEMENTED.** There IS an AECP
engine now — the protocol processor's uCPU — and it implements exactly one of
these rows' commands, `READ_DESCRIPTOR`, which has no image to serve on a stock
build. Every other row's command draws a conformant `NOT_IMPLEMENTED` echo:
well-formed, correctly sized, correctly addressed, and **not the behaviour the
row requires**. The rows are kept with their clause, their FR and their reason
intact — that is what makes each one a *named* conformance gap rather than an
absence.

🔴 **Milan Δ7 `ACQUIRE_ENTITY` — `NOT_SUPPORTED` with `owner_id` = 0 — is NOT
distinguished from that generic echo.** The microprogram exists in the
processor's ucode (`E_ACQ`); nothing dispatches to it. A controller cannot tell
"this entity refuses acquisition, as Milan says it may" from "this entity does
not know the opcode".

| Milan requirement | Dep | FR/NFR | Today | Why necessary | Verify |
|-------------------|-----|--------|-------|---------------|--------|
| `READ_DESCRIPTOR` returns the exact model | MANDATES | FR-ENUM-01 | **PP, SERVABLE NOT SUPPLIED** — the uCPU implements it: `SUCCESS` carries `configuration_index` + reserved + the descriptor, a locate miss is `NO_SUCH_DESCRIPTOR`, a bad configuration index is `BAD_ARGUMENTS`, and both errors carry the §7.4.5 4-byte `{descriptor_type, descriptor_index}` stub. **Nothing in this repository builds or loads the descriptor image**, so on a stock build every read takes the `BAD_ARGUMENTS` path — the invalid image reports `configurations_count` = 0 and the range check precedes the locate — and "the exact model" is unproven on this build | Byte-wrong descriptors desync controllers. | T  -  `tsn-gen aecp_read_descriptor` (byte-exact) vs entity JSON, **after** loading an image at `PP_DESC_BASE_P`; `Hive` |
| `ACQUIRE_ENTITY` / `LOCK_ENTITY` (Milan timeouts) | MANDATES | FR-CTRL-01 | **❌ NOT IMPL** — both draw the generic `NOT_IMPLEMENTED` echo and the processor's lock manager is unwired, so no controller can hold this entity; `0x648` `aecp_locked` is a structural zero *because* of that. 🔴 Milan Δ7's `NOT_SUPPORTED` + `owner_id` = 0 answer for ACQUIRE **exists in ucode (`E_ACQ`) and is never dispatched** | Two controllers must not make conflicting changes. | T  -  `tsn-gen aecp_acquire_lock_entity.feature`; two-controller `Hive` test |
| SET/GET config, name, stream_format, clock_source, sampling_rate | MANDATES | FR-CTRL-02 | **❌ NOT IMPL** — all ten commands draw the `NOT_IMPLEMENTED` echo, and each one takes a capability with it: no configuration switch, no labelling, **no listener format adaptation** (FR-STR-03), **no CRF media clock selection**, no rate change. A refused SET changes nothing, so the pinned values below (`clock_source_index` = 0, the 2 ms transit-time default) are pinned for the life of the build | Connection setup depends on these SETs. | T  -  `tsn-gen aecp_aem_set_{stream_format,clock_source,sampling_rate,name,configuration}` |
| Unsolicited notifications, ≥16 controllers | MANDATES | FR-CTRL-03 | **❌ NOT IMPL** — no registry (REGISTER/DEREGISTER_UNSOLICITED_NOTIFICATION draw the echo), no trigger path, and while the processor's **solicited** AECP TX lane is driven and reaches the wire, the **unsolicited lane has no producer at all**. The whole Milan **Table 5.22** push duty is open | Controllers show stale state without it. | T  -  register (`Hive`), induce change, observe unsolicited response |
| `GET_COUNTERS` (stream/interface sets) | MANDATES | FR-CTRL-04, NFR-OBS-01 | **✅ IMPLEMENTED FOR SUPPORTED TARGETS**. Every declared STREAM_OUTPUT has a live `KL_talker_diag_ctx` bank and returns the Milan Table 5.17 mask and compact five-counter layout. STREAM_INPUT, AVB_INTERFACE and CLOCK_DOMAIN retain their processor counter paths. An undeclared index returns `NO_SUCH_DESCRIPTOR` with the fixed empty body | Used in Milan adverse-network/fault tests. | T - `milan_dp`, `tkdiag`, pinned la_avdecc decoder, `avdecc_l2 counters` |
| AECP validation & correct status | MANDATES | FR-CTRL-06 | **PP, IN PART — grade this one carefully.** What IS met is the §9.3.5 duty to respond and the shape of the response: every command gets an answer with `message_type` + 1, the correct length, the correct `controller_data_length`, and `controller_entity_id` / `sequence_id` echoed verbatim; a command whose `target_entity_id` is not ours is silently refused (freed and counted), as is an AECP *response* arriving as input; `IDENTIFY_NOTIFICATION`-as-command returns `BAD_ARGUMENTS` per §7.4.39.2, and `READ_DESCRIPTOR` returns `NO_SUCH_DESCRIPTOR` / `BAD_ARGUMENTS` on its own two error paths. What is NOT met is per-command validation — `ENTITY_LOCKED`, payload `BAD_ARGUMENTS`, `NOT_SUPPORTED` where Milan names it — because the commands that would raise those statuses do not exist. **A uniform `NOT_IMPLEMENTED` is a correct status only for a command that is genuinely not implemented** | Wrong status on bad commands = conformance fail. | T  -  `tsn-gen aecp_non_aem` / malformed-PDU features |
| `GET_DYNAMIC_INFO` fast enumeration | MANDATES | FR-CTRL-05 | **IMPLEMENTED.** The protocol processor validates the complete record list before execution, accepts exactly the 13 fixed-get commands in IEEE 1722.1-2021 section 7.4.76.2, reports status independently per record, copies legal unsupported command data, and silently omits results that would exceed cdl 524 while continuing. The legacy `0x768` BDBG words remain structural zeros because they belong to the deleted fabric engine, not this processor implementation | Milan v1.2 section 5.4.2.29 makes the fixed-get subset mandatory. | T - processor `pp_top` W8 batch cases and the root Behave command inventory |

## D. Milan Vendor Unique  -  MVU  *(Milan v1.2 §5.4.3.2)*

**Section D is NOT IMPLEMENTED in its entirety** — the uCPU recognises no
VENDOR_UNIQUE `protocol_id` at all, so MVU is one more unimplemented message
type. **Grade the two standards apart.** IEEE 1722.1 §9.6.2 requires an
*unknown* `protocol_id` to be answered `NOT_IMPLEMENTED`, and the engine
satisfies that **by construction**: it echoes the `protocol_id` bytes unaltered
inside a conformant `NOT_IMPLEMENTED` response. Milan's own `protocol_id`
00-1B-C5-0A-C1-00 gets exactly the same treatment as a stranger's, so **the
1722.1 win does not close a single Milan row here**: *no MVU ⇒ not a Milan
device*, and this build cannot complete the Milan identity handshake.

| Milan requirement | Dep | FR/NFR | Today | Why necessary | Verify |
|-------------------|-----|--------|-------|---------------|--------|
| MVU (`00-1B-C5-0A-C1-00`) + `GET_MILAN_INFO` | MANDATES | FR-MVU-01 | **❌ NOT IMPL** — answered `NOT_IMPLEMENTED` like any unknown vendor protocol | The Milan identity handshake; no MVU ⇒ not a Milan device. | T  -  `tsn-gen aecp_vendor_unique.yaml`; `Hive` Milan-info; `CONF` |
| `GET/SET_SYSTEM_UNIQUE_ID`, `…_MEDIA_CLOCK_REFERENCE_INFO` | MANDATES | FR-MVU-02 | **❌ NOT IMPL** — same echo, no stored system id, no media-clock-reference state (the media-clock-reference half was already unimplemented as M-AECP-9) | Media-clock-reference mgmt + system grouping. | T  -  MVU command exchange (custom `tsn-gen` case) |
| `features_flags` truthful | MANDATES | FR-MVU-03 | **❌ NOT IMPL** — nothing publishes the bits, because nothing answers GET_MILAN_INFO. The truthfulness obligation returns in full whenever MVU dispatch is written, and the open item it inherits is the TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING bit | Controllers plan features from these bits. | I,T  -  inspect + read `GET_MILAN_INFO` (`MILAN_REDUNDANCY=0`) |

## E. Connection management  -  ACMP  *(Milan v1.2 §5.5)*

| Milan requirement | Dep | FR/NFR | Today | Why necessary | Verify |
|-------------------|-----|--------|-------|---------------|--------|
| `CONNECT/DISCONNECT/GET_*_STATE` (talker & listener) | MANDATES | FR-CONN-01 | **PP** — talker and listener both. Milan renames these `BIND_RX_*` / `PROBE_TX_*` (5.5.3). The `0x6A4` group's `bound`, `active` and bit 31 are real; its state-machine fields (state, probing, acmp_status, tk_avail, lstn_declare) and the `0x6E8` walker window are **structural zeros** — a reader must take `bound` as the truth | No stream without ACMP. | T  -  `avdecc_l2 connect/disconnect`; `tap_acmp` |
| Program datapath (classifier queue + CBS) on connect | MANDATES | FR-CONN-02 | **PP** — this is exactly what the class-D wire face is for: the bind record, the talker declaration and `srp_granted_slope_bps_o` are consumed by the fabric every clock rather than through a software-paced side port | Stream needs SR class + shaped bandwidth or it misses latency. | T  -  connect, then read CBS/classifier CSR (`vtb:csr` semantics) / `tc cbs` |
| **Fast-connect / saved-state restore** on power/link-up | MANDATES | FR-CONN-03, FR-CONN-04 | **❌ NOT IMPL.** `KL_persist_journal` is deleted and the processor's NVM face is a BLANK-FLASH responder, so a restore walk always finds blank flash and completes with zero records: **nothing in this device persists a binding across a power cycle**. The `0x7A0` bind-restore port accepts writes and never asserts its ack | Installed systems must recover without a controller. | T,D  -  save connection, power-cycle, observe auto-reconnect (`tap_acmp` + `avdecc_l2 listen`) |

> **The ACMP DA gate is the talker gate.** `acmp_declaring_o` asserts only after
> a MAAP `ALLOC_DA` success, so AAF admission is still "a destination address
> exists AND the source is declaring" — the composed gate did not weaken when
> the plane changed hands.

## F. Streaming & stream formats  -  AVTP AAF  *(Milan v1.2 §5.4 format match; §6 Base Audio Formats)*

| Milan requirement | Dep | FR/NFR | Today | Why necessary | Verify |
|-------------------|-----|--------|-------|---------------|--------|
| Talker AAF encapsulation + valid presentation time | MANDATES | FR-STR-01 | **live** — the presentation-time **offset** resets to the Milan **2 ms default** per Stream Output and is settable since 0x0053 by `SET_STREAM_INFO`'s `MSRP_ACC_LAT` sub-command (the folded entry is what the AAF and CRF framers stamp); `SET_MAX_TRANSIT_TIME` remains unimplemented. The default is a DEFAULT, not a zero: 0 ns would be a presentation time in the past and every listener would drop every frame as late | Presentation time aligns listener playout. | T  -  `soak` (peer-host pair); `tap_sniff` AVTP; `thdn` |
| Listener de-encapsulation + de-jitter to presentation time | MANDATES | FR-STR-02, NFR-LAT-01 | **live** | Must render at the presentation instant within Class A. | T  -  `soak`; `thdn`; `latency.md` |
| **Listener format-adaptive** (`SET_STREAM_FORMAT` → talker's format; match incoming AAF) | MANDATES | FR-STR-03, FR-STR-03b | **SERVED at 0x0053; wire reshape deferred** — `SET_STREAM_FORMAT` stores a supported family member per row, the served current format and STREAM_INPUT 0's acceptance follow it, and refusals carry the current format. The render path still adapts by wire truth; the framers do not yet re-shape from the stored format | A format-locked listener can't connect to a differing talker. | T  -  set talker format, connect, confirm listener `current_format` follows (`Hive`+`avdecc_l2`); packet-match per `stream.c` |
| Talker format is fixed | MANDATES | FR-STR-03a | **live** — and it is now fixed structurally: `TALKER_WIRE_CHANS_P` drives the packetizer at elaboration and nothing can write it at runtime | Only the talker source is singular. | I,T  -  inspect `STREAM_OUTPUT`; `tap_sniff` transmitted format |
| Base Audio Formats (6/12/24 spp @48/96/192k) | MANDATES | FR-STR-03, FR-STR-05 | **live on the wire**; as a *declaration* it is **servable, not supplied** — the format lists live in the descriptor image the uCPU would serve, and this repository builds no image, so a controller reading them gets `BAD_ARGUMENTS` | Cross-vendor interop. | I,T  -  inspect `raw_hex`; interop against a reference talker |
| Stream counters + fault recovery | MANDATES | FR-STR-04, NFR-REL-01 | **✅ SOLICITED COUNTERS LIVE**. GET_COUNTERS serves Stream Input and Stream Output banks. Stream Output sources cover STREAM_START, STREAM_STOP, MEDIA_RESET, TIMESTAMP_UNCERTAIN and FRAMES_TX with wrap and reset-on-start behavior. The Table 5.22 unsolicited change producer remains open; fault recovery itself is unaffected | Milan adverse-network conformance. | T - `milan_dp`, `tkdiag`, `avdecc_l2 counters` during induced link flap; `CONF` |

## G. Reservation & addressing  -  MAAP, SRP  *(Milan v1.2 §5.6; 802.1Qat/Qak)*

| Milan requirement | Dep | FR/NFR | Today | Why necessary | Verify |
|-------------------|-----|--------|-------|---------------|--------|
| MAAP dynamic multicast allocation + defend | MANDATES | FR-MAAP-01 | **live, and still this fabric's** — `KL_maap` claims one BLOCK; the protocol processor implements no MAAP by design and publishes a per-source ALLOC/RELEASE face instead, bridged by `hdl/milan/KL_pp_maap_shim.sv` | Avoids stream dest-MAC clashes. | T  -  `maap` daemon + `tap_sniff` (PROBE/DEFEND/ANNOUNCE) |
| MSRP Talker Advertise / Listener Ready; MVRP VLAN reg | MANDATES | FR-SRP-01, FR-SRP-02 | **PP** — the whole lwSRP engine is deleted. The `0x680` group's MRPDU tx/rx counts and rx drops are **structural zeros**; the DOMAIN word, granted slope and over-limit bit are **live**, repointed to the processor's class-D SRP face. Its provisioning words (DMAC, MaxFrameSize, MaxIntervalFrames, declare-bypass) are **write-only scratch** and change nothing observable | Class A needs end-to-end bandwidth reservation. | T  -  observe reservation on the bridge; `tap_sniff` MRPDUs |
| Reservation gates tx; CBS from the grant; ≤75 % SR | MANDATES | FR-SRP-03, FR-QOS-02, FR-QOS-03 | **PP** — `srp_active_o` gates TX and `srp_granted_slope_bps_o` sets the slope. Honest ordering change: `KL_lwsrp_bw_gate` joined the slope into the sum *before* opening the gate and closed the gate *before* removing it, while the processor asserts both in the SAME cycle. Opening edge: at worst equal. Closing edge: the sum is briefly high for zero traffic — conservative, not permissive. Neither edge lets a stream transmit against an un-budgeted slope | Over-transmit breaks other streams' guarantees. | T,A  -  `tc cbs offload`; `vtb:cbs` (idleSlope/credit); no-tx-on-fail case |

## H. Media clocking & time  -  gPTP  *(Milan v1.2 §5.7; 802.1AS; 1722-2016 §10 CRF)*

| Milan requirement | Dep | FR/NFR | Today | Why necessary | Verify |
|-------------------|-----|--------|-------|---------------|--------|
| 802.1AS time-aware endpoint (Class A), GM tracking | MANDATES | FR-CLK-01, NFR-TIME-01 | **live** | Presentation times live on the gPTP timebase (≤1 µs). | T  -  `ptp4l`/`phc2sys` lock; `ethtool -T`; `gptp-phc-clock.md` (offset ≤1 µs) |
| Media clock from CRF / input stream; CRF talker+recovery | MANDATES | FR-CLK-04, NFR-TIME-02 | **❌ NOT IMPL — this is the sharpest single loss on the page.** The CRF *talker* still emits and `KL_crf_rx` still parses, counts and reports, but **the CRF media clock can never be SELECTED**: `SET_CLOCK_SOURCE` is unimplemented (answered `NOT_IMPLEMENTED`, and a refusal writes nothing) and it was the only writer of `clock_source_index`, pinned at 0 (INTERNAL) for the life of the build. `KL_mmcm_drp_servo` and the `KL_media_nco` packet-grid servo are structurally off; `A_MCSRV_STAT` (`0x8F8`) reads its idle. Recovery is measured and not actuated | Drift ⇒ periodic MEDIA_RESET / artifacts. | T  -  `soak` (clock-recovery); `tap_sniff` CRF |
| HW timestamps at the SFD | MANDATES | FR-CLK-05 | **live** | gPTP/AVTP accuracy needs HW capture. | T  -  `ethtool -T` + timestamp capture; `vtb:ptp` |
| PHC on a fixed (speed-independent) clock | MANDATES(impl) | FR-CLK-02, NFR-TIME-03 | **live** | Speed-switched PHC ⇒ wrong ns rate at 10/100/1000. | A,T  -  `vtb:ptp` (rate at each speed); analysis (REQ-PTP-07) |

## I. QoS datapath  -  802.1Q / 802.1Qav  *(required by Milan for Class A)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| PCP classification into SR/BE queues | MANDATES | FR-QOS-01 | Class A must land in its shaped queue. | T  -  `vtb:cls` (PCP→TC→queue over random configs) |
| CBS shaping of SR; strict priority for BE | MANDATES | FR-QOS-02, NFR-LAT-01, NFR-DET-01 | CBS bounds queuing latency to the 2 ms budget and isolates media from BE. | T  -  `vtb:cbs`, `vtb:shaper_core`; `tc qdisc … cbs offload` |

## J. Timing / performance NFRs  *(Milan Class A service class)*

| Milan requirement | Dep | FR/NFR | Why necessary | Verify |
|-------------------|-----|--------|---------------|--------|
| Class A latency bound (≈2 ms), configurable | MANDATES | NFR-LAT-01 | Exceeding the presentation offset drops samples. | T  -  `latency.md` (end-to-end measurement) |
| Sustain Class A packet rate (8000 pkt/s/stream) | MANDATES | NFR-PERF-02 | Under-delivery starves the listener ⇒ MEDIA_RESET. | T  -  `soak` (sustained) + `avdecc_l2 counters` |
| Media path undisturbed by control/BE load | MANDATES | NFR-DET-01 | Deterministic streaming regardless of mgmt activity. | T  -  `soak` under injected BE load |
| Control RTT within 1722.1 inflight timeouts | SHOULD | NFR-LAT-02 | Slow responses trigger retries. | T  -  measure AECP/ACMP RTT (`avdecc_l2`/`Hive`) |

---

## K. Milan features intentionally OUT OF SCOPE

| Milan feature | Status | Recorded | Verify |
|---------------|--------|----------|--------|
| Seamless **redundancy** | Out of scope; `MILAN_REDUNDANCY=0` | FR-MVU-03, entity `_redundancy_note` | I  -  `GET_MILAN_INFO` reports 0; single AVB_INTERFACE |
| Rates **> 192 kHz** | Out of scope | entity scope | I  -  AUDIO_UNIT `sampling_rates` |
| **AEM authentication** | Not mandated by Milan | NFR-SEC-01 | I  -  advertises not-required; behaves safely unauthenticated |

## L. Requirements NOT Milan-driven (project / platform)

Milan only **CONSTRAINS** these; it does not require them.

| FR/NFR | Driver | Milan relationship | Verify |
|--------|--------|--------------------|--------|
| NFR-SCUP-01..04 (scale-up) | one design, small↔large | CONSTRAINS: growing `P_CH/P_SR` must not change the control plane / break Class A | A,D  -  build full entity, re-run the whole T-suite at 8-ch/48-96-192k |
| NFR-SCOUT-01..07 (scale-out, >1 softcore) | capacity via N softcores | CONSTRAINS: all cores see **one coherent PHC** (FR-CLK-01) + media stays deterministic (NFR-DET-01) | A,D  -  build `P_CORES=2..N` (SMP **and** AMP), re-run T-suite; single-PHC check; per-core sizing benchmark |
| NFR-RES-01 (fit xc7a100t) | FPGA budget | none | A  -  Vivado utilization report ≤ target |
| NFR-REL-02 (media-core watchdog) | AMP robustness | ENABLES: keeps Milan planes alive on media-core fault | T  -  hang a media core, observe restart w/o dropping control |
| NFR-MAINT-01 (single-source model) | engineering | ENABLES: HW+SW+tests stay Milan-consistent | I  -  CI diff entity JSON vs `entity-model-milan-v12.h` |
| NFR-PORT-01 (RV64/RV32 build) | platform | none | A  -  build both targets |
| NFR-OBS-01 (observability) | ops | ENABLES: surfaces Milan counters (FR-CTRL-04) | D  -  `ethtool -S`/`-T`, per-core load, AVDECC counters |

---

## Coverage & test summary

- **Every Milan area (A–J) maps to ≥1 MANDATES FR** with a named test artifact.
  That mapping is unchanged; what changed is that **area C (AECP/AEM) answers
  everything and implements one command**, area **D (MVU) is refused in its
  entirety**, and named rows in B, E, F and H are ❌ alongside them.
- **The MANDATES rows that read ❌ are the Milan v1.2 conformance gap, in one
  list:** every AECP command except `READ_DESCRIPTOR`, including the
  unsolicited-notification duty (C), the entire MVU identity handshake (D),
  fast-connect / saved-state restore (E), listener format adaptation (F), and
  media-clock **selection** including CRF recovery as an actuated loop (H).
  The AEM descriptor model (B) is the one row that is neither implemented nor
  absent: **servable, not supplied** — the engine serves descriptors and this
  repository builds no image, so enumeration answers `BAD_ARGUMENTS` on a
  stock build. Three losses deserve restating on their own because they are
  functional, not just protocol, losses: **the CRF media clock can never be
  selected**; the **presentation offset is pinned at the Milan 2 ms default** (a
  default, not a zero). The Milan Table 5.4 per-STREAM_OUTPUT counters are live
  for solicited GET_COUNTERS reads. The Table 5.22 unsolicited counter-change
  producer remains open.
- **The missing link is a build step, and naming it is the point.** The image
  generator exists (`protocol-processor/hdl/aecp/desc/gen_desc_image.py`); what
  does not exist is anything that turns an `endstation_*.yaml` into its JSON and
  writes the result to `PP_DESC_BASE_P` before the entity is enabled.
  `sw/builder/endstation_builder.py` still emits `aecp_aem_rom.svh` — the ROM of
  the deleted fabric store, an orphan, not this image.
- **HW-verifiable now (Verilator, no controller):** FR-QOS-\* (`vtb:cbs/shaper_core/cls`),
  FR-CLK-02/05 (`vtb:ptp`), CSR/IRQ (`vtb:csr`), FR-DISC/FR-CONN/FR-SRP through
  the protocol processor (`vtb:pp_shadow`, `vtb:milan_dp`).
- **Interop/system:** ADP/ACMP via `avdecc_l2`/`tap_acmp`/`Hive`; gPTP via
  `ptp4l`; streaming via `soak`/`thdn`; reservation observed on the bridge.
  AECP/MVU: a controller reaches the entity and gets well-formed refusals; it
  enumerates nothing until a descriptor image is loaded, and it can set nothing
  at all.
- **Conformance:** the `CONF` plan (the private bench suite) is the acceptance
  gate, and it cannot pass while section D and all but one row of section C read
  ❌. That is a stated capability boundary, not a pending fix — it lifts command
  by command as microprograms are written and dispatched, starting with the
  descriptor image that makes `READ_DESCRIPTOR` mean something.
- **Scale (L):** the same T-suite is re-run at the full profile and at `P_CORES=2..N`
  (SMP, AMP)  -  passing there proves scale-up/out without re-proving Milan logic.

See [`FR_NFR.md`](FR_NFR.md) §6 (forward traceability to milestones) and §7
(verification approach), and [`avdecc/README.md`](../../avdecc/README.md) for the entity
model the descriptors trace to.

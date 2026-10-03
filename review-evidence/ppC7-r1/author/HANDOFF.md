# [A508] Lane C7 (counters): handoff

Branch `c7-counters` from `main` `88969246`. Issues #44, #78, #79.
Assignment: #79 comment 5962255629. TAKEN posted 2026-10-03 (#79 comment 5962267176).
Reviewers: [R442] (internal), [R443] (external).

Status: DONE. Head `751e1c0` (local branch, not pushed). REVIEW READY posted on #79 (comment 5963690172, 2026-10-03 02:36).
No STOP condition met: no top-level port, parameter or register; nothing the parent
drives or reads changes.
Base sweep at `88969246` (scratch `git archive`): rc 0, 33 suites, 1,019,127 checks.

| Commit | Item |
|---|---|
| `b8df34e` | 1. #79: the `ctr_*` face contract per descriptor type; GAP-05's decision recorded |
| `2b2af6c` | 2. #44: the dead tick removed; K9 to K16 and their 13 mutants |
| `cbc4816` | 3. #78: 02 §4.3 to §4.5, §5 and F02.10 to the landed top |
| `dce60db` | the parent's C++ idiom gate on the new header (two tables as arrays of pairs) |
| `315cc94` | #78 acceptance 1 read strictly: no removed op or event named in 02 |
| `751e1c0` | the out-of-context record in `syn/ooc/README.md` |

## 0. Design

### 0.1 What the owner already ruled

Owner decision 2026-09-19 (#44 comment 5740180072, #79 comment 5740180166): the
integrator owns counter storage behind the `ctr_*` face. No counter bank is added
to `hdl/`. REQ-NET-004 and REQ-AEM-019 are graded on that face, not on processor
storage. #79's residue is therefore (b) of its "What remains": the face contract,
the export of every event the integrator must count, and a pp_top check that the
events arrive.

The design below needs **no new top-level port, parameter or register** and
**changes nothing the parent drives or reads** (the `ctr_*` face, `KL_pp_shadow`,
the parent's GET_COUNTERS path). So no STOP condition is met.

### 0.2 #79: where every Milan counter lives today

Clauses: IEEE 1722.1-2021 §7.4.42 (Figures 7-66/7-67; counters_valid and offset
Tables 7-150/7-151 ENTITY, 7-152/7-153 AVB_INTERFACE, 7-154/7-155 CLOCK_DOMAIN,
7-156/7-157 STREAM_INPUT, 7-158/7-159 STREAM_OUTPUT, 7-160/7-161 PTP_PORT);
Milan v1.2 §5.4.2.25 (Tables 5.13 to 5.17), §5.3.6.3 Table 5.1, §5.3.7.7
Table 5.4, §5.3.8.10 Table 5.6, §5.3.11.2 Table 5.7, Table 5.22 (GET_COUNTERS row).

The processor holds none of them. What it owns is the command and the push:

| Processor part | Where (main `88969246`) |
|---|---|
| parse, locate-first existence, type gate {STREAM_INPUT, STREAM_OUTPUT, AVB_INTERFACE, CLOCK_DOMAIN}, fixed 160-byte body for every status | `hdl/aecp/ucode/gen_ucode.py:823-863` (`E_GCTRS`, `E_GCTRSNS`), `KL_aecp_engine` A_PLD-exit re-dispatch |
| the read face, one quadlet per beat, word 32 = counters_valid first, then 0..31; `ctr_wait_i` is a HOLD; watchdog `DESC_MEM_TMO_CYC_P` -> ENTITY_MISBEHAVING | `hdl/top/protocol_processor_top.sv:366-386`, wired `:3789-3794` |
| the change strobe -> Table 5.22 push, coalesced per descriptor, at most one emission per descriptor per second (`T-CTR-NOTIF`) | `protocol_processor_top.sv:3984-3986` -> `hdl/aecp/KL_aecp_notify.sv:385-394, 489-506, 1033-1039, 1233-1237` |

Each counter Milan makes the processor report, with its owner today. "Parent" is
milan-fpga dev `cdf49d1a` (read-only checkout), all behind the same `ctr_*` face.

| Descriptor (mask Milan claims) | Counter | quadlet / mask | Owner today |
|---|---|---|---|
| AVB_INTERFACE (Table 5.13: 0x23) | LINK_UP | 0 / 0x01 | parent `hdl/milan/milan_datapath.sv:3485-3518` (edges of `eff_link_w`, the level it drives on `link_up_i`, `:7642`), served `:3529-3540` |
| | LINK_DOWN | 1 / 0x02 | same block |
| | GPTP_GM_CHANGED | 5 / 0x20 | same block, on `pp_gm_id_change_p_w` (identity edges only, `:7248-7278`), not on the wider `gm_change_i` duty |
| | FRAMES_TX / FRAMES_RX / RX_CRC_ERROR (Table 5.14, optional) | 2, 3, 4 | nowhere (unclaimed by the parent, `:3536`) |
| CLOCK_DOMAIN (Table 5.15: 0x03) | LOCKED / UNLOCKED | 0, 1 | parent `milan_datapath.sv:3497-3516` (edges of `~clkv_tu_w`), served `:3542-3550` |
| STREAM_INPUT (Table 5.16: 0xF3F) | MEDIA_LOCKED ... FRAMES_RX (ten) | 0-5, 8-11 | parent AAF inputs: `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv` (observation interval `:110`, bind wipe `:136`, `:849`), served `milan_datapath.sv:3414-3432` with mask 0xFFF (`:3357`); CRF input: `KL_crf_rx`, served `:3583-3603`, mask 0xF3F |
| | TIMESTAMP_VALID / NOT_VALID (IEEE only) | 6, 7 | parent AAF inputs only (0xFFF); not Milan-mandatory |
| STREAM_OUTPUT (Table 5.17: 0x1F, compacted, Δ9) | STREAM_START, STREAM_STOP, MEDIA_RESET, TIMESTAMP_UNCERTAIN, FRAMES_TX | 0-4 | parent `KL_talker_diag_ctx` (`milan_datapath.sv:3210-3232`), served `:3552-3569` |
| ENTITY | ENTITY_SPECIFIC only (Table 7-150) | - | none; the processor answers NOT_SUPPORTED in the full body |
| PTP_PORT (IEEE §7.4.42.1, not Milan) | Table 7-160 | - | none; outside the type gate (NOT_SUPPORTED) |

The parent's change strobe: per-descriptor dirty pulses serialized by a lossless
arbiter (`milan_datapath.sv:7428-7429`) onto `ctr_change_i` (`:7556-7558`).

**Decision per counter: the integrator feeds every one through the documented
face; the processor owns no bank.** This is the owner's ruling; it also fits the
evidence: every one of these events happens in the integrator's datapath (link
PHY, gPTP, media clock, AVTP talker/listener), and the parent already keeps all of
them. The face is keyed by {descriptor_type, descriptor_index}, so a second AVB
interface (Milan ch. 8 redundancy) is AVB_INTERFACE index 1 on the same face.

**Semantics the integrator must give each counter** (written into the integrator
guide). All counters: 32-bit unsigned, **wrap** to 0 past 0xFFFFFFFF (Milan
§5.3.6.3, §5.3.7.7, §5.3.8.10, §5.3.11.2: "wraps over to zero"), never saturate;
all reset to 0 at the integrator's reset (power-up, "since boot").

| Counter | Counts | Extra reset |
|---|---|---|
| LINK_UP / LINK_DOWN | each down->up / up->down change of the level driven on `link_up_i`; the edge detector's previous value resets to down, so UP = DOWN or DOWN+1 holds by construction (Table 5.1) | none |
| GPTP_GM_CHANGED | each publication of a grandmaster identity that differs from the one in force (Table 5.1 "GM changes"); a domain-only `gm_change_i` does not count | none |
| LOCKED / UNLOCKED | each lock / unlock edge of the integrator's own media-clock lock level; previous value resets to unlocked; LOCKED = UNLOCKED or +1 (Table 5.7) | none |
| MEDIA_LOCKED / MEDIA_UNLOCKED | edges of the input's media lock, same invariant (Table 5.6) | whole STREAM_INPUT bank to 0 on not-bound->bound, never on unbind (§5.3.8.10) |
| STREAM_INTERRUPTED | each playback interruption except a controller unbind | as above |
| SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, UNSUPPORTED_FORMAT, LATE_TIMESTAMP, EARLY_TIMESTAMP, FRAMES_RX | +1 at the end of each observation interval (<= 1 s, implementation-specific) in which the event was seen at least once | as above |
| STREAM_START / STREAM_STOP | each talker start / stop; START = STOP or +1 (Table 5.4) | none |
| MEDIA_RESET, TIMESTAMP_UNCERTAIN, FRAMES_TX (output) | per observation interval (<= 1 s), on transmitted AVTPDUs | to 0 each time the talker starts streaming (Table 5.4) |

counters_valid: claim exactly the quadlets the build keeps (mask bit n = quadlet n,
Milan's 0x00000001 = quadlet 0). A clear bit's quadlet reads 0. The Milan masks are
the floor: AVB_INTERFACE 0x23, CLOCK_DOMAIN 0x03, STREAM_INPUT 0xF3F (0xFFF with
the two IEEE tallies), STREAM_OUTPUT 0x1F in Milan's compacted layout (not IEEE
Tables 7-158/7-159, Δ9). The change strobe: one cycle per changed served
descriptor, naming its {type, index}, for an increment or a reset rule that clears
a non-zero value.

`T-CTR-OBSERVE` (F08.1) becomes the integrator's observation interval: the
processor keeps no tick for it (its timer singleton already stays reserved and
unused, 08 §5).

**Docs**: 00 §7 records the decision (GAP-05 row: Resolution, Addressed in,
Verified by, residue); REQ-AEM-018/019 and REQ-NET-004 point at the guide's
counters section; 06 §6.6 loses "tracked separately" and states the landed
`ctr_change_*` -> notify wiring; F06.15 becomes the integrator's bank table;
F07.10 is corrected to "no counter bank in this repository" (the integrator's
banks, behind the face), with F07.1, the access-rights rule, the side-port row and
the §6 sizing row following; 01 §4, 03 §5, 06 §1/F06.1, 08 F08.1/F08.2 follow.

### 0.3 #44: AVB_INTERFACE LINK_UP, LINK_DOWN, GPTP_GM_CHANGED

Owner: the **integrator** (owner ruling). The processor's two inputs are the
integrator's own levels, so the integrator counts what it drives:

- LINK_UP / LINK_DOWN: edges of the level on `link_up_i` (Milan §5.3.6.3 Table 5.1).
- GPTP_GM_CHANGED: identity changes of the grandmaster published on `gm_id_i`.

**The tied-off tick.** `KL_adp_engine.gm_changed_tick_o` (`hdl/adp/KL_adp_engine.sv:181-182,
237, 256-265`) is `gm_change_i` delayed one clock, landed on
`adp_gm_tick_nc_w` (`protocol_processor_top.sv:1841, 1935`). It is **removed**,
not exported:
1. it carries no information the integrator lacks: it is a copy of the
   integrator's own input;
2. it is the wrong event for the counter: `gm_change_i` is the ADP/GET_AVB_INFO
   duty and is raised for a domain-only change too (integrator guide §6;
   top `:250-254`), while Table 5.1 counts grandmaster changes only (the parent
   keeps exactly this split, `milan_datapath.sv:3459-3468`);
3. exporting it would be a new top-level port, a STOP condition.
#44 acceptance 2 allows "exported or removed"; the owner's "where the tied-off
GM-changed tick must be exported" is answered in the guide: the event to count is
the integrator's own identity edge, the one on which it raises `gm_change_i` (and
`gsi_asp_chg_i`) for a new grandmaster.

Stale in-processor "counters" consumers removed: 02 §5 event catalog and F02.10
`link_up`, 04 §2 and §6 (GPTP_GM_CHANGED tick), 02 §4.3.

**Grading on the wire** (`tb/pp_top`):
- section K (main run): the harness's counter store becomes a live integrator
  model for AVB_INTERFACE 0 (mask 0x23; LINK_UP/LINK_DOWN from the `link_up_i`
  edges it drives, GPTP_GM_CHANGED from identity changes at its `gm_change_i`
  strobes) and CLOCK_DOMAIN 0 (mask 0x03, a harness media-lock level). K4c/K4d
  become byte-exact against it.
- new section K-AVB on a fresh model (`--counters-only`, `make counters`):
  link flaps and GM changes to distinct counts, byte-exact AVB_INTERFACE 0 at
  block offsets 0, 4, 20, the invariant at every sample, a domain-only strobe that
  moves nothing, AVB_INTERFACE pushes through `ctr_change_i` byte-exact at a
  registered controller carrying the counts at emission, coalesced within the
  second, throttled independently of a STREAM_INPUT push, and CLOCK_DOMAIN 0
  likewise.
- mutants (`tb/pp_top/ctr_mutants.py`, reviewed patches in
  `tb/pp_top/ctr_mutations/`): processor arms (type gate, notify decode, slot
  alias, strobe wiring, rate-limit sharing) and integrator-model arms (a store that
  counts domain-only strobes, a link edge detector reset "up").

### 0.4 #78: 02 §4.3-4.5 and §5

Exposing the gptp/avtp/mclk class-B adapters is **not required for Milan
conformance**: Milan v1.2 states the wire behaviour (GET_AVB_INFO §5.4.2.23,
GET_AS_PATH §5.4.2.24, GET_COUNTERS §5.4.2.25, GET_STREAM_INFO §5.4.2.10,
START/STOP_STREAMING §5.4.2.19/.20, SET/GET_CLOCK_SOURCE §5.4.2.15/.16, the
§5.3.x state and the Table 5.22 notifications), not an internal adapter API, and
the landed level outputs plus the `gsi_*`/`ctr_*` read faces serve each of them
(graded in `tb/pp_top` V, G, K, W, U). So **the text is corrected** to the landed
top:
- §1 taxonomy and F02.1/F02.9: class B = `srp` (`svc_*`), `maap`; gptp/avtp/mclk
  are class-D levels plus read faces;
- §4.3 gptp, §4.4 avtp, §4.5 mclk: one landed-shape table each, mapping what each
  old op/event did to the port or gsi/ctr word that serves it now, and naming no op
  or event that no port serves;
- new §4.6: the `ctr_*` face (moved out of §4.4, `ctr_change_*` added), per-type
  contract in the integrator guide;
- §5: the class-C template is the event router's internal contract; a landed
  table lists every event with the port or internal module that produces it;
- F02.10 gains a "Landed as" column; as_capable, prop_delay_ns, path_count,
  streaming[src], mc_locked[domain] name their gsi/ctr word.

#78 acceptance 3 and 4 are already met on main by PR #133 (issue #29 closed;
`tb/srp_top` Q1-Q4 measure T-MRP-JOIN 180-240 ms, T-MRP-PERIODIC 900-1500 ms and
the leavealltimer 10-15 s from both sides, `tb/srp_top/sim_main.cpp:1710-1789`).

### 0.5 What the PR closes

- #79: all four acceptance items -> Closes.
- #44: re-scoped acceptance (owner) items 1-3 and the original items 1-3 -> Closes
  (item 4 applies only if processor-owned).
- #78: acceptance 1-2 here, 3-4 on main -> Closes.

## 1. Item 1: #79 counter face (commit `b8df34e`)

#79 is met through its integrator arm (b): the decision is recorded, the face contract is
written per descriptor type, and the stale text is gone. No code: the processor's half
already existed and is graded by K1 to K8 and U9, and item 2 adds the counts on the wire.

| Change | Where | Clause |
|---|---|---|
| the face contract: ports, the five read-face rules (which objects reach it, order, wrong object, hold and watchdog, counters_valid), the per-type mask and quadlet table, what every counter counts with wrap and reset rules, the invariants by construction, the AVB_INTERFACE duty, the change strobe and its slots | `docs/guides/integrator.md:406-510` (§7.1, anchor `counters-face`); tie-off row `:388` | IEEE 1722.1-2021 §7.4.42, Figures 7-66/7-67, Tables 7-150 to 7-159; Milan v1.2 §5.4.2.25 Tables 5.13 to 5.17, §5.3.6.3 Table 5.1, §5.3.7.7 Table 5.4, §5.3.8.10 Table 5.6, §5.3.11.2 Table 5.7, Table 5.22 |
| #79 acceptance 1, the decision in 00 §7 | `docs/00_MILAN_COMPLIANCE_REVIEW.md:539` (GAP-05 row) and the GAP-05 disposition `:159-166` | owner decision 2026-09-19 |
| #79 acceptance 3: REQ-AEM-019 and REQ-NET-004 point at the guide (and REQ-AEM-018) | `docs/00_MILAN_COMPLIANCE_REVIEW.md:422, 423, 483` | Milan Tables 5.1/5.4/5.6/5.7/5.13 |
| #79 acceptance 3: F07.10 corrected (no bank here; the integrator's banks and their reset rules) | `docs/architecture/07_memory_maps.md:529-544`; F07.1, the access rule, §1, the side-port row `:836`, the §6 sizing row removed | — |
| #79 acceptance 4: 06 §6.6 states the landed `ctr_change_*` -> `KL_aecp_notify` push instead of "tracked separately" | `docs/architecture/06_aecp_engine.md:624-633`; who keeps the counters `:591-598`; F06.15 retitled `:600` | Milan Table 5.22 |
| the `ctr_*` landed-shape table moved to its own 02 §4.6 with the `ctr_change_*` rows it lacked | `docs/architecture/02_interfaces.md:409-443` (anchor `sec-02-ctr`) | — |
| T-CTR-OBSERVE is the integrator's; its timer singleton stays reserved | `docs/architecture/08_timing.md:32, 232`; F08.2 node removed | Milan §5.3.7.7, §5.3.8.10 |
| the stale "counters subsystem" rows and nodes | `01_overview.md:84`, `03_packet_engine.md:223`, `06_aecp_engine.md` §1, F06.1, §9 | — |

Tests: none in this commit (the existing K1 to K8 and U9 already grade the processor's
half; item 2 adds K9 to K16).

## 2. Item 2: #44 AVB_INTERFACE counters (commit `2b2af6c`)

| Change | Where | Clause |
|---|---|---|
| `gm_changed_tick_o` removed (a one-clock-late copy of `gm_change_i`, landed on `adp_gm_tick_nc_w`): no port, and the wrong event for the counter because `gm_change_i` also fires on a domain-only change | `hdl/adp/KL_adp_engine.sv:104-107` (the strobe now documents it counts nothing), the port, `gm_tick_r` and its assign removed; `hdl/top/protocol_processor_top.sv` (the `_nc_` wire at main `:1841` and its connection at main `:1935` removed) | Milan §5.3.6.3 Table 5.1 ("Number of gPTP GM changes") |
| stale in-processor "counters" consumers removed | `docs/architecture/04_adp_engine.md:23-28, 161`; 02 §5 catalog, F02.10 `link_up`, §4.3 (then rewritten in item 3) | — |
| the harness's counter store keeps AVB_INTERFACE 0 (mask 0x23) and CLOCK_DOMAIN 0 (mask 0x03) live, per the guide's contract, from the `link_up_i`, `gm_change_i`/`gm_id_i` it drives and a harness media-lock level | `tb/pp_top/sim_main.cpp:878-941` (`ItfCounters`, `ctr_mask`/`ctr_value` now per instance, `count_interface_events`), `:1388`, `:1919-1921`; the three body helpers read the instance's store (`:3663`, `:4633`, `:5673`, `notify_phases.hpp:1227`) | Milan Tables 5.1, 5.7, 5.13, 5.15 |
| K4c/K4d: the populated blocks byte-exact with their masks | `tb/pp_top/sim_main.cpp:3786-3806` | IEEE Figure 7-67 |
| new section K9 to K16 on a fresh model (`--counters-only`, `make counters`) | `tb/pp_top/counters_phases.hpp` (new), wired at `sim_main.cpp:13607, 13647, 13670`, `Makefile:132` | IEEE Tables 7-152 to 7-155; Milan Tables 5.1, 5.7, 5.13, 5.15, 5.22 |
| the mutation campaign | `tb/pp_top/ctr_mutants.py`, `tb/pp_top/ctr_mutations/` (13 patches), `Makefile:137` | — |
| adp_engine suite: the tick's observable removed (P5 and the F04.2 walk's GPTP_GM_CHANGED column) | `tb/adp_engine/sim_main.cpp:761-768`, `tb_adp_top.sv`, `README.md` (1,367 -> 1,328 checks: P5's one check and the walk's 38 advertise cells) | — |
| docs | 06 §6.6 push paragraph (K13 to K16), 00 GAP-05 Verified by, `09_verification.md:325` (§8.6), `tb/pp_top/README.md` section K and the campaign record | — |

Each test and the mutant(s) that fail it (`ctr_mutants.py`, all 13 KILLED, control PASS):

| Check | What it grades | Killed by |
|---|---|---|
| K4c, K4d | AVB_INTERFACE 0 and CLOCK_DOMAIN 0 byte-exact with masks 0x23/0x03 (main run) | `ctr-avb-not-supported` fails K4c and `ctr-ckd-not-supported` fails K4d when planted into the default build's main run (scratch copies of head, rc 1: 10 failures, K4c and K9 to K12; 4 failures, K4d and K16 x3) |
| K9 | after boot: mask 0x23, LINK_UP 1, LINK_DOWN 0, GPTP_GM_CHANGED 0, byte-exact | `ctr-avb-not-supported`, `ctr-index-from-type`, `store-link-detector-resets-up` (named) |
| K10 | four flaps: 1/1, 2/1, 2/2, 3/2 and the Table 5.1 invariant read off the wire | `ctr-avb-not-supported`, `ctr-index-from-type`, `store-link-detector-resets-up` |
| K11 | five GM changes count; a domain-only strobe does not; 3/2/5 byte-exact at block offsets 0, 4, 20 (#44 acceptance 3) | `ctr-block-beats-swapped` (named: offset 20), `store-counts-domain-strobes` (named: the domain-only arm), `ctr-avb-not-supported`, `ctr-index-from-type`, `store-link-detector-resets-up` |
| K12 | AVB_INTERFACE 1 (absent from the image) NO_SUCH_DESCRIPTOR, face not asked | `ctr-locate-ignored` (named), `ctr-avb-not-supported` |
| K13 | a flap + one strobe: one push per controller within 300 ms, byte-exact, counts of that moment | `ctr-notify-avb-dropped`, `ctr-notify-avb-as-clock`, `ctr-change-type-from-index` (named), `ctr-index-from-type`, `ctr-block-beats-swapped`, `store-*` |
| K14 | two changes inside the second: nothing for 850 ms, then one push >= 900 ms later with the latest counts, then nothing | `ctr-notify-no-window` (named), `ctr-notify-avb-dropped`, `ctr-notify-avb-as-clock`, `ctr-change-type-from-index`, `ctr-index-from-type`, `ctr-block-beats-swapped`, `store-*` |
| K15 | a fresh window opens at once; inside it a STREAM_INPUT push goes at once while the interface waits | `ctr-notify-one-window` (named), `ctr-notify-no-window`, `ctr-notify-avb-dropped`, `ctr-notify-avb-as-clock`, `ctr-change-type-from-index`, `ctr-index-from-type`, `ctr-block-beats-swapped`, `store-*` |
| K16 | CLOCK_DOMAIN 0: 1/0, 1/1, 2/1 with the Table 5.7 invariant, byte-exact, and its push | `ctr-ckd-not-supported` (named), `ctr-notify-ckd-dropped` (named), `ctr-notify-avb-as-clock`, `ctr-notify-one-window`, `ctr-change-type-from-index`, `ctr-index-from-type` |

The two `store-*` arms plant into the harness, not the RTL: they show the checks refuse
an integrator store that breaks the guide's contract (a domain-only strobe counted; a
link edge detector reset up, which loses the boot's LINK_UP and breaks the invariant).

## 3. Item 3: #78 docs (commits `cbc4816`, `315cc94`)

Decision: **correct the text**. Exposing class-B gptp/avtp/mclk adapters is not required
for Milan conformance: Milan v1.2 states wire behaviour (§5.4.2.10, §5.4.2.15/.16,
§5.4.2.19/.20, §5.4.2.23 to .25, Table 5.22), not an internal adapter API, and the landed
levels and read faces serve all of it (graded in `tb/pp_top` G, V, W, K, U and NP).

| Change | Where | Acceptance |
|---|---|---|
| §1 taxonomy: class B = `srp` (`svc_*`), `maap`; class C = the router's internal events, at the top only the MAAP conflict pair; the landed-shape paragraph; F02.1 and F02.9 redrawn (with `gsi` and `ctr` rows) | `docs/architecture/02_interfaces.md:10-69` | 1 |
| §4 intro: the template applies to the two class-B instances; the read-face rule (hold, unwired answers zero, watchdog) | `02_interfaces.md:198-212` | 1 |
| §4.3 gptp: landed-shape table (every need -> port or gsi word) and the `gsi_*` signal table | `02_interfaces.md:344-378` | 1 |
| §4.4 avtp: every need mapped to its landed level (`acmp_bound_*`, `aecp_strm_started_o`, `aecp_fmt_*`, `aecp_pt_offset_*`, the licence trio, gsi kind 0) | `02_interfaces.md:380-395` | 1 |
| §4.5 mclk: `aecp_clk_src_index_o`, the MVU waiver, lock as the integrator's level and counters | `02_interfaces.md:397-407` | 1 |
| §5: the class-C template is the router's; the landed catalog lists every event with its producing port or internal module and form | `02_interfaces.md:445-496` | 1 |
| F02.10 gains "Landed as"; as_capable, prop_delay_ns, path_count, streaming[src], mc_locked[domain] each name their gsi/ctr word | `02_interfaces.md:505-527` | 2 |
| the former op names removed from 05 (§2, A15, the BIND_RX sequence) and 06 §2; explicit anchors `sec-06-stri`, `sec-06-gsi` | `05_acmp_engine.md:23-26, 293, 510`; `06_aecp_engine.md:24-27, 312, 825` | — |
| 00: GAP-04 disposition and row, REQ-NET-001/005; 01 block list | `00_MILAN_COMPLIANCE_REVIEW.md:142-149, 480, 484, 538`; `01_overview.md:90` | — |

`315cc94` reads acceptance 1 strictly: no removed op or event is named anywhere in 02
(the first version kept a "former op or event" column). The mapping, for readers of the
earlier text: READ_AS_PATH -> the `gsi` kind 2 words; AS_CAPABLE_CHANGE / PATH_CHANGE ->
`gsi_avb_chg_i` / `gsi_asp_chg_i`; INPUT_CONFIGURE/ENABLE/DISABLE -> `acmp_bound_*`;
INPUT_START/STOP -> `aecp_strm_started_o`; SET_INPUT/OUTPUT_FORMAT -> `aecp_fmt_*` and the
kind 0 selector 15 verdict; OUTPUT_SET_PT_OFFSET -> `aecp_pt_offset_*`; OUTPUT_STATUS ->
the `gsi` kind 0 words; SET_CLOCK_SOURCE -> `aecp_clk_src_index_o`; GET_MCR_DEFAULTS ->
waived; the stream-health events and MC_LOCKED/UNLOCKED -> the integrator's counters.

#78 acceptance 3 and 4 were met on main by PR #133 (#29 closed; `tb/srp_top` Q1 to Q4,
`tb/srp_top/sim_main.cpp:1710-1789`, measure T-MRP-JOIN 180-240 ms, T-MRP-PERIODIC
900-1500 ms and the own leavealltimer 10-15 s from both sides). Tests for item 3: none
(text only; `make check` renders F02.1 and checks every link and anchor).

## 4. Item 4: parent-visible list

- **No interface change.** No port, parameter or register of `protocol_processor_top`
  changes; the `ctr_*` face, `KL_pp_shadow` and the parent's GET_COUNTERS path are
  untouched. The parent consumer gates pass with both adoption patches unchanged.
- **One internal port removed:** `KL_adp_engine.gm_changed_tick_o`. No parent file
  instantiates `KL_adp_engine` or names the tick (searched at `cdf49d1a`); the parent's
  `scripts/pp_srcs.py:92` lists the file, which still exists, and `test_builder.py`'s
  regex on it (`:26137-26144`) reads a line this change does not touch.
- **The parent already meets the documented contract** (`hdl/milan/milan_datapath.sv`):
  AVB_INTERFACE LINK_UP/LINK_DOWN on the edges of `eff_link_w`, the level it drives on
  `link_up_i` (`:3485-3518`, `:7642`); GPTP_GM_CHANGED on `pp_gm_id_change_p_w`, identity
  edges only (`:3459-3468`, `:7248-7278`), mask 0x23; CLOCK_DOMAIN 0x03; STREAM_INPUT
  0xFFF (AAF) and 0xF3F (CRF); STREAM_OUTPUT 0x1F; the lossless change-strobe arbiter
  (`:7428-7429`, `:7556-7558`). Nothing to change there.
- **Text the parent cites moves**: 02 §4.3 to §4.6, §5 and F02.10 (new column), 06 §6.6
  (retitled; new anchors `sec-06-counters`, `sec-06-stri`, `sec-06-gsi`), 07 F07.10, 08
  T-CTR-OBSERVE, the 00 GAP-04/GAP-05 rows and REQ-AEM-018/019, REQ-NET-001/004/005, the
  integrator guide's new §7.1 (`counters-face`), 09 §8.6.
- **Parent doc nits for the pin-adoption lane** (not changed here): `milan_datapath.sv:3478`
  numbers the AVB_INTERFACE valid bits "Table 7-158"; IEEE 1722.1-2021 numbers them Table
  7-152 (offsets Table 7-153), and Table 7-158 is STREAM_OUTPUT's.
- **Tallies the parent may quote**: `tb/pp_top` 9,168 -> 9,191 (+23, K9 to K16);
  `tb/adp_engine` 1,367 -> 1,328 (-39, the tick's observable).
- **New processor files the parent's gates see**: `tb/pp_top/counters_phases.hpp` (C++,
  inside the idiom gate's population), `tb/pp_top/ctr_mutants.py` (Python; reads only
  patches and logs, so `measure_test_evidence.py` does not classify it as a DUT reader)
  and `tb/pp_top/ctr_mutations/*.patch`.

## 5. Gates

All runs with the pinned Verilator 5.050, every command run directly (never piped into
another command that could hide its status), each with its own log and rc file in
scratch (`$VALIDATION_STORAGE/c7-a508/`).

### 5.1 Processor suites and entry points

| Command | Base `88969246` (scratch `git archive`) | Head |
|---|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 suites, 1,019,127 checks, 0 failing | rc 0: 33 suites, **1,019,111** checks, 0 failing (code of `dce60db`, the final code head; `315cc94` and `751e1c0` change only text) |
| — of which `tb/pp_top` | 9,168 | **9,191** (+23: K9 to K16; builds default 8,719, fixture 20, identify 178, line 218, timebase 56) |
| — of which `tb/adp_engine` | 1,367 | **1,328** (-39: P5's tick check and the F04.2 walk's 38 tick cells) |
| every other suite | — | identical counts |
| `./scripts/lint_hdl.sh` | — | rc 0, 41 of 41 tops LINT OK |
| `make check` | rc 0 (1,050 links) | rc 0: 41 mermaid + 18 wavedrom blocks, 1,087 links, 115 REQ rows, 17 GAP findings, 94 module rows 0 untested, 27 parameters |
| `python3 scripts/gen_matrix.py --check` | — | rc 0 |
| `git apply --check`, every campaign patch in `tb/` | — | 220 of 220 apply (207 + this lane's 13) |

### 5.2 Mutants

| Campaign | Result |
|---|---|
| `tb/pp_top/ctr_mutants.py` (new; `make -C tb/pp_top ctr-mutants`), at head | control PASS, **13 of 13 KILLED** by their named checks (per-arm table in section 2 and the `tb/pp_top` README); identical failure counts at `2b2af6c` and at head |
| `tb/adp_engine` `make mutants` (its walk lost the tick column) | 32 of 32 (two controls PASS, 30 arms KILLED); every arm's failure count equals its README record, so the record is unchanged |
| `tb/pp_top/notify_mutants.py --jobs 2` (the harness store now feeds ST's expected bodies), at head | goldens PASS, 40 of 40 KILLED (`counter_limit_500ms` among them) |
| other campaigns (`aecp_mutants`, `aecp_dispatch_mutants`, `d3_mutants`, `acmp_mutants`, `gsi_mutants`, `name_wr_mutant`, the unit suites') | not re-run. Several plant into `protocol_processor_top.sv` (27 of the 42 `mutations/` patches, 1 of the 37 `aecp_dispatch_mutations/`, and the exact edits of `d3`, `acmp`, `gsi`), but no patch or edit names the removed tick or its wire (searched: only `tb/adp_engine` did, and it is updated), every patch still applies, and no target of theirs reads AVB_INTERFACE or CLOCK_DOMAIN counters |

### 5.3 Parent consumer gates (cdf49d1a + c4c6 + c8 patches)

Scratch parent: `git archive` of the trusted checkout at `cdf49d1a`, made a git repo,
with its submodules as real git checkouts at their pins (`external` `efeb541a`,
`gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, fetched into
scratch) and `protocol-processor` a scratch clone of this branch with its gitlink
recorded at the lane head; then `parent-adoption-c4c6-ea3fb388.patch` (sha256
`67bcd698…`) and `parent-adoption-c8-cdf49d1a.patch` (`aa5a88eb…`) applied with
`git apply`, in that order, both unchanged. The trusted checkout was never modified.

Every gate at `315cc94`, the head whose code is final (gates 1, 2, 4, 5 and 8 to 12 re-ran at
`751e1c0`, all rc 0); the light gates, then the heavy ones in turn; `test_builder.py` alone before the `milan_dp` family, whose header it removes
and restores while it runs; `xvlog_gate.py` alone and last):

| # | Gate | Result |
|---|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | rc 0, every ratchet held; 168 first-party translation units (the new `counters_phases.hpp` among them) |
| 2 | `python3 scripts/check_py_idiom.py` | rc 0, every ratchet held (`ctr_mutants.py` in the population) |
| 3 | `python3 scripts/xvlog_gate.py --check` | rc 0, 4 findings == ratchet (0 hdl/, 4 pinned processors: the same four as before) |
| 4 | `python3 scripts/check_rtl_source_lists.py` | rc 0: 107 files in the milan_datapath closure; protocol-processor 36/42 tops, 6 recorded |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | rc 0 |
| 6 | `python3 sw/builder/test_builder.py` | rc 0: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, a board report not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 646, 606, 606 and 311 checks, 0 failures |
| 8 | `python3 scripts/check_port_contracts.py` | rc 0: protocol-processor 1,756 ports (1,757 at main: the removed tick); its "ratchet can be lowered" note is the same at main |
| 9 | `python3 scripts/measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `python3 scripts/measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT readers (`ctr_mutants.py` is not one) |
| 11 | `python3 scripts/docs_check.py` | rc 0, 0 findings |
| 12 | `python3 scripts/lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13 | `make -C tb/verilator/nvm_cosim lint` | rc 0 |
| 14 | `make -C tb/verilator/nvm_cosim quick` | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS; its `[CTRS2]` legs read AVB_INTERFACE mask 0x23 and LINK_UP = LINK_DOWN + 1 through this processor |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

Both adoption patches are unchanged: this lane needs no parent change. Before they were
applied, `measure_test_evidence.py` named exactly the two readers the c4c6 patch
dispositions (`acmp_mutants.py`, `notify_mutants.py`), from main's C4 and C6 lanes.

## 6. Out-of-context cost

The only RTL change removes `KL_adp_engine.gm_changed_tick_o` (one flip-flop per
interface) and the top's `_nc_` wire. Measured with the repository's instrument of
record, `syn/ooc/protocol_processor_ooc.tcl` (complete processor, default 8x8 shape,
all ports present, `xc7a100tfgg484-2`, 10 ns, Vivado 2026.1), each run alone in its own
empty build directory, base `88969246` and head RTL (`315cc94` = `751e1c0`):

| Resource | Base | Head | Delta |
|---|---:|---:|---:|
| Slice LUTs | 30,375 | 30,375 | 0 |
| Registers | 31,951 | 31,951 | 0 |
| LUT as distributed RAM | 1,222 | 1,222 | 0 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |
| `u_adp` LUTs / registers | 852 / 507 | 852 / 507 | 0 |
| WNS at 10 ns, OOC | -9.656 ns | -9.656 ns | 0 |

Zero: the dangling flop was already trimmed in the base netlist. The hierarchical
reports differ only in their date lines. Reports kept in scratch, not here: `util.rpt`
9,205 B (base sha256 `f2e106ca8876f71a…`, head `60b26eb0587fcf11…`), `util_hier.rpt`
8,333 B (`80cce79f12364c02…`, `c13d7e61b7783e24…`), `timing.rpt` 42,394 B
(`cbfbd9b6e6c832d9…`, `5c9b145bdd6595b5…`); the digests differ by the date lines alone.
Recorded in `syn/ooc/README.md` (commit `751e1c0`).

## Notes for the reviewers

- **The tick: removed, not exported.** The owner's re-scope on #44 says "where the
  tied-off GM-changed tick must be exported". The tick was `gm_change_i` one clock late,
  and `gm_change_i` also fires on a domain-only change, so exporting it would have handed
  the integrator a copy of its own input with the wrong meaning for GPTP_GM_CHANGED. It
  would also have been a new top-level port, a STOP condition. #44 acceptance 2 allows
  "exported or removed"; the guide (§7.1) says which event to count instead.
- **The redundancy seam** is open at the face, which is indexed, and closed at
  `KL_aecp_notify`'s slots and at the interface-0 inputs (see "What remains" in the PR
  body). Nothing in this lane narrows it further.
- **Final head vs gated head:** the heavy parent gates and the suite sweep ran at
  `315cc94` (`dce60db`'s code). `751e1c0` adds a README section only; the light parent
  gates and `make check` re-ran there, all rc 0.
- **Checks removed:** `tb/adp_engine` loses 39 checks, every one an observation of the
  removed tick (P5, and the F04.2 walk's tick column). Its 30-arm mutation record is
  unchanged arm by arm.

## Scratch and housekeeping

- Scratch: `$VALIDATION_STORAGE/c7-a508/` (standards text, logs, parent copy).
- Every ignored file the session created in the tree (the wavedrom venv `make check`
  bootstraps, the suites' build outputs) was removed at the end with `git clean -fdX`
  after checking that all 51 entries were created during the session; the tree is clean.

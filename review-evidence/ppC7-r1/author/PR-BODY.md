[A508]

Closes #79
Closes #44
Closes #78

Lane C7 of the PP program: counters (assignment: #79 comment 5962255629). Branch
`c7-counters` from `main` `88969246`, six commits, head `751e1c0`.

The design follows the owner decision of 2026-09-19 (#44 comment 5740180072, #79
comment 5740180166): **the integrator keeps every counter behind the `ctr_*` face, and
the processor keeps none.** The processor owns the GET_COUNTERS command and its Table
5.22 push. The design needs no new top-level port, parameter or register, and changes
nothing the parent drives or reads (the `ctr_*` face, `KL_pp_shadow`, the parent's
GET_COUNTERS path). No STOP condition was met.

| Commit | Item |
|---|---|
| `b8df34e` | 1. #79: the `ctr_*` face contract per descriptor type, and GAP-05's decision recorded |
| `2b2af6c` | 2. #44: the dead GPTP_GM_CHANGED tick removed; the integrator's AVB_INTERFACE and CLOCK_DOMAIN counters graded on the wire (K9 to K16), with 13 mutants |
| `cbc4816` | 3. #78: 02 §4.3 to §4.5, §5 and F02.10 rewritten to the landed top |
| `dce60db` | the parent's C++ idiom gate on the new test code: two expected-count tables spelled as arrays of pairs |
| `315cc94` | #78 acceptance 1 read strictly: no removed op or event is named in 02's landed-shape tables |
| `751e1c0` | the out-of-context record in `syn/ooc/README.md` |

## Design

Where each counter lives today. The processor holds none. On the reference platform
(milan-fpga dev `cdf49d1a`) every counter lives in `milan_datapath`, behind the same face:

| Descriptor (Milan mask) | Counters | Owner today |
|---|---|---|
| AVB_INTERFACE (Table 5.13, `0x23`) | LINK_UP, LINK_DOWN, GPTP_GM_CHANGED | parent `milan_datapath.sv:3485-3540`: edges of the level it drives on `link_up_i`; the GM count on grandmaster identity edges only |
| | FRAMES_TX, FRAMES_RX, RX_CRC_ERROR (Table 5.14, optional) | nowhere (unclaimed) |
| CLOCK_DOMAIN (Table 5.15, `0x03`) | LOCKED, UNLOCKED | parent `:3497-3550` |
| STREAM_INPUT (Table 5.16, `0xF3F`) | the ten Table 5.6 counters (AAF inputs also keep TIMESTAMP_VALID/NOT_VALID, `0xFFF`) | parent `KL_avtp_rx_monitor_ctx` (AAF) and `KL_crf_rx` (CRF), served `:3414-3432`, `:3583-3603` |
| STREAM_OUTPUT (Table 5.17, `0x1F`, Δ9) | STREAM_START, STREAM_STOP, MEDIA_RESET, TIMESTAMP_UNCERTAIN, FRAMES_TX | parent `KL_talker_diag_ctx`, served `:3552-3569` |
| ENTITY, PTP_PORT | — | none; the processor refuses NOT_SUPPORTED in the full body |

Semantics, now the integrator guide's contract: every counter is 32-bit unsigned and
**wraps** (Milan v1.2 §5.3.6.3, §5.3.7.7, §5.3.8.10, §5.3.11.2), never saturates, and
resets with the integrator's reset. The STREAM_INPUT bank also resets on every not-bound
to bound change, never on unbind (§5.3.8.10). The output's MEDIA_RESET,
TIMESTAMP_UNCERTAIN and FRAMES_TX reset at each stream start (Table 5.4). Interval
counters commit once per observation interval of at most 1 s (`T-CTR-OBSERVE`, now the
integrator's). Each pair keeps its invariant by construction when it counts the two
edges of one level whose edge detector resets inactive.

The face is keyed by `{descriptor_type, descriptor_index}`, so a second AVB interface is
AVB_INTERFACE index 1 on the same face. Nothing in the design assumes a single port.

## 1. #79: the face contract (`b8df34e`)

- `docs/guides/integrator.md` §7.1 (`counters-face`): the ports; the five read-face
  rules (which objects reach the face: the four supported types at indices the image
  holds; order; the wrong-object answer; the hold and its watchdog; counters_valid);
  the per-type mask and quadlet table (Milan Tables 5.13 to 5.17; IEEE 1722.1-2021
  Tables 7-152 to 7-159); what every counter counts, its wrap and its reset rules; the
  AVB_INTERFACE duty; the change strobe and the slots it has. The §7 tie-off table
  gains the counters row: honest, and not Milan-conformant.
- 00 §7 GAP-05: the decision recorded (acceptance 1). REQ-AEM-018, REQ-AEM-019 and
  REQ-NET-004 point at the guide (acceptance 3).
- 07 F07.10 corrected: no counter bank in this repository. F07.1, the access rule, the
  side-port row and the §6 sizing row follow (acceptance 3).
- 06 §6.6: the "tracked separately" sentence replaced by the landed `ctr_change_*` to
  `KL_aecp_notify` push (acceptance 4). F06.15 is retitled as the integrator's banks.
- 02 §4.6 (new): the `ctr_*` landed shape, with the `ctr_change_*` rows it lacked.
- 08: T-CTR-OBSERVE is the integrator's; its timer singleton stays reserved. 01, 03 and
  06's stale "counters subsystem" rows and nodes are corrected.

## 2. #44: AVB_INTERFACE counters (`2b2af6c`)

- **The tick is removed, not exported.** `KL_adp_engine.gm_changed_tick_o` was
  `gm_change_i` one clock late and ended on `adp_gm_tick_nc_w`. It is the wrong event
  for GPTP_GM_CHANGED: `gm_change_i` is the ADP and GET_AVB_INFO duty and fires for a
  domain-only change too, while Milan Table 5.1 counts grandmaster changes. Exporting it
  would also have been a new top-level port. #44 acceptance 2 allows either. The guide
  names the event to count: the integrator's own identity change, the update for which
  it raises `gm_change_i` and `gsi_asp_chg_i`.
- 04 §2 and §6, and the 02 event catalog and F02.10, no longer list "counters" as an
  in-processor consumer (acceptance 1).
- `tb/pp_top`: the harness's counter store keeps AVB_INTERFACE 0 (`0x23`) and
  CLOCK_DOMAIN 0 (`0x03`) live, per the guide, from the `link_up_i` and `gm_change_i`
  it drives. K4c and K4d check them byte-exact. A new section, K9 to K16
  (`counters_phases.hpp`, a fresh model, `make counters`):

| Check | Grades |
|---|---|
| K9 | after boot: mask 0x23, LINK_UP 1, LINK_DOWN 0, GPTP_GM_CHANGED 0, byte-exact |
| K10 | four flaps, 1/1, 2/1, 2/2, 3/2, with the Table 5.1 invariant read off the wire |
| K11 | five grandmaster changes count; a domain-only `gm_change_i` does not; the distinct counts 3, 2, 5 byte-exact at block offsets 0, 4, 20 (acceptance 3) |
| K12 | AVB_INTERFACE 1, absent from the image: NO_SUCH_DESCRIPTOR, and the face is never asked |
| K13 | one flap and one strobe: one push per registered controller within 300 ms, byte-exact, with the counts of that moment (Milan Table 5.22) |
| K14 | two changes inside that second: nothing for 850 ms, then one push 900 ms or more later with the latest counts, then nothing |
| K15 | a Stream Input's push is not held by the interface's one-second window |
| K16 | CLOCK_DOMAIN 0: 1/0, 1/1, 2/1 with the Table 5.7 invariant, byte-exact, and its push |

- `tb/adp_engine`: the tick's observable is removed (P5 and the F04.2 walk's tick
  column), 1,367 to 1,328 checks.

## 3. #78: 02 to the landed top (`cbc4816`, `315cc94`)

Decision: **correct the text.** Exposing gptp, avtp and mclk class-B adapters is not
required for Milan conformance. Milan v1.2 states the wire behaviour (§5.4.2.10,
§5.4.2.15/.16, §5.4.2.19/.20, §5.4.2.23 to .25, Table 5.22), not an internal adapter API.
The landed levels and read faces serve all of it, and `tb/pp_top` grades them (G, V, W,
K, U, NP).

- §1: class B is `srp` (`svc_*`) and `maap`. Class C is the event router's internal
  events; at the top only the MAAP conflict pair is class C. F02.1 and F02.9 are redrawn,
  adding the `gsi` and `ctr` faces.
- §4.3 gptp, §4.4 avtp, §4.5 mclk: a landed-shape table each, mapping what Milan needs
  to the port or `gsi`/`ctr` word that serves it, plus the `gsi_*` signal table.
  Acceptance 1.
- §5: the class-C template is the router's. The landed catalog lists every event with
  its producing port or internal module, and its form. Acceptance 1.
- F02.10 gains a "Landed as" column. as_capable, prop_delay_ns, path_count,
  streaming[src] and mc_locked[domain] name their `gsi`/`ctr` word. Acceptance 2.
- Old to new, for readers of earlier text: READ_AS_PATH became the `gsi` kind 2 words;
  AS_CAPABLE_CHANGE and PATH_CHANGE became `gsi_avb_chg_i` and `gsi_asp_chg_i`;
  INPUT_CONFIGURE/ENABLE/DISABLE became `acmp_bound_*`; INPUT_START/STOP became
  `aecp_strm_started_o`; SET_INPUT/OUTPUT_FORMAT became `aecp_fmt_*` and the `gsi` kind 0
  selector 15 verdict; OUTPUT_SET_PT_OFFSET became `aecp_pt_offset_*`; OUTPUT_STATUS is
  now answered on the `gsi` kind 0 words; SET_CLOCK_SOURCE became `aecp_clk_src_index_o`;
  GET_MCR_DEFAULTS is waived; the stream-health events and MC_LOCKED/UNLOCKED are the
  integrator's counters.
- 05 (§2, A15, the BIND_RX sequence), 06 §2, 01 and 00 (GAP-04, REQ-NET-001/005)
  follow.
- Acceptance 3 and 4 were already met on main by #133 (#29 closed; `tb/srp_top` Q1 to
  Q4 measure T-MRP-JOIN, T-MRP-PERIODIC and the leavealltimer from both sides).

## Validation

All with the pinned Verilator 5.050.

| Command | Result |
|---|---|
| `./scripts/run_suites.sh`, base `88969246` | rc 0: 33 suites, 1,019,127 checks |
| `./scripts/run_suites.sh`, head (the code of `dce60db`; `315cc94` and `751e1c0` change only text) | rc 0: 33 suites, **1,019,111** checks, 0 failing. `tb/pp_top` 9,168 -> 9,191 (+23, K9 to K16); `tb/adp_engine` 1,367 -> 1,328 (-39, the tick's observable); every other suite unchanged |
| `./scripts/lint_hdl.sh` | rc 0, 41 of 41 |
| `make check` | rc 0: 41 mermaid + 18 wavedrom blocks, 1,087 links, 115 REQ rows, 17 GAP findings, 94 module rows 0 untested, 27 parameters |
| `python3 scripts/gen_matrix.py --check` | rc 0 |
| `git apply --check`, every campaign patch in `tb/` | 220 of 220 |
| `make -C tb/pp_top ctr-mutants` (new) | control PASS, 13 of 13 KILLED by their named checks (the per-arm record is in the `tb/pp_top` README) |
| `make -C tb/adp_engine mutants` | 32 of 32; every arm's failure count equals its README record |
| `tb/pp_top/notify_mutants.py --jobs 2` | goldens PASS, 40 of 40 KILLED |

The mutants for the new checks:

| Arm | Broken | Named check |
|---|---|---|
| `ctr-avb-not-supported` | the type gate refuses AVB_INTERFACE | K9 |
| `ctr-ckd-not-supported` | the type gate refuses CLOCK_DOMAIN | K16 |
| `ctr-index-from-type` | `ctr_desc_index_o` driven from the type | K9 |
| `ctr-block-beats-swapped` | quadlets 4 to 7 and 8 to 11 swapped | K11 (offset 20) |
| `ctr-locate-ignored` | a locate miss falls through to the face | K12 |
| `ctr-notify-avb-dropped` | the notify block ignores an AVB_INTERFACE strobe | K13 |
| `ctr-notify-avb-as-clock` | an AVB_INTERFACE strobe marks the CLOCK_DOMAIN slot | K13 |
| `ctr-notify-ckd-dropped` | the notify block ignores a CLOCK_DOMAIN strobe | K16 |
| `ctr-notify-one-window` | one emission starts every descriptor's window | K15 |
| `ctr-notify-no-window` | the one-second limit removed | K14 |
| `ctr-change-type-from-index` | the strobe's type wired from its index | K13 |
| `store-counts-domain-strobes` | (harness store) counts every `gm_change_i` | K11 (the domain-only arm) |
| `store-link-detector-resets-up` | (harness store) link edge detector resets up | K9 |

Planted into the default build's main run, `ctr-avb-not-supported` also fails K4c and
`ctr-ckd-not-supported` K4d (10 and 4 failures).

Parent consumer gates, all 16 rc 0, at milan-fpga dev `cdf49d1a`. The scratch copy is
a `git archive` of dev with its submodules as real checkouts at their pins, with
`parent-adoption-c4c6-ea3fb388.patch` and then `parent-adoption-c8-cdf49d1a.patch`
applied (both unchanged), and `protocol-processor` at `315cc94` with its gitlink
recorded (`751e1c0` adds only a README section; gates 1, 2, 4, 5 and 8 to 12 re-ran there, all rc 0):

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held (the new header and driver in the population) |
| 3 | `xvlog_gate.py --check` (alone, last) | rc 0, 4 findings == ratchet |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded) |
| 6 | `sw/builder/test_builder.py` | rc 0, all gates pass except 1 not run (a board report not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 646, 606, 606 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0 (one processor port fewer: the removed tick) |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT readers |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS; its `[CTRS2]` legs read AVB_INTERFACE mask 0x23 and LINK_UP = LINK_DOWN + 1 through this processor |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

Out-of-context cost of the RTL change, measured with `syn/ooc/protocol_processor_ooc.tcl`
(the complete processor, default shape, all ports present, `xc7a100tfgg484-2`, 10 ns),
base `88969246` against head, each run alone:

| Resource | Base | Head | Delta |
|---|---:|---:|---:|
| Slice LUTs | 30,375 | 30,375 | 0 |
| Registers | 31,951 | 31,951 | 0 |
| LUT as distributed RAM | 1,222 | 1,222 | 0 |
| RAMB36 / RAMB18 / DSP | 23 / 2 / 4 | 23 / 2 / 4 | 0 |
| `u_adp` LUTs / registers | 852 / 507 | 852 / 507 | 0 |

Zero, as expected: the unconnected flop was already trimmed. Both builds have the
same OOC slack (-9.656 ns), so this makes no timing claim. Recorded in
`syn/ooc/README.md`.

## Parent-visible list

- **No interface change.** No port, parameter or register of `protocol_processor_top`
  changes. The `ctr_*` face, `KL_pp_shadow` and the parent's GET_COUNTERS path are
  untouched, and both adoption patches are unchanged.
- **One internal port removed:** `KL_adp_engine.gm_changed_tick_o`. No parent file
  instantiates the engine or names the tick. `scripts/pp_srcs.py` lists the file, which
  still exists.
- **The parent already meets the documented contract** in `milan_datapath`: LINK_UP and
  LINK_DOWN on the level it drives on `link_up_i`; GPTP_GM_CHANGED on grandmaster
  identity edges only; masks 0x23, 0x03, 0xFFF/0xF3F and 0x1F; a lossless change-strobe
  arbiter. Nothing to change.
- **Text the parent cites moves:** 02 §4.3 to §4.6, §5 and F02.10 (new column); 06
  §6.6 (retitled, with the new anchors `sec-06-counters`, `sec-06-stri` and
  `sec-06-gsi`); 07 F07.10; 08 T-CTR-OBSERVE; the 00 GAP-04/GAP-05 rows,
  REQ-AEM-018/019 and REQ-NET-001/004/005; the integrator guide's new §7.1
  (`counters-face`); 09 §8.6.
- **Tallies:** `tb/pp_top` 9,191, `tb/adp_engine` 1,328, sweep 1,019,111.
- **New processor files the parent's gates see:** `tb/pp_top/counters_phases.hpp`,
  `tb/pp_top/ctr_mutants.py` (reads only patches and logs, so it is not a DUT reader)
  and `tb/pp_top/ctr_mutations/`.

## What remains

- **The redundancy seam.** The read face is keyed by descriptor index and needs nothing
  for a second interface. The notify block, though, keeps one AVB_INTERFACE slot and one
  CLOCK_DOMAIN slot (`KL_aecp_notify.sv:385`), and `link_up_i`, `gm_id_i`,
  `gptp_domain_i` and `gm_change_i` are interface 0 (`P-N-AVB-INTERFACES` is 1). Growing
  those to the parameter is the redundancy lane's work, and its input half is a
  top-level port change that needs a ruling. CLOCK_DOMAIN indices beyond 0 have the same
  single slot.
- The counters' own semantics (invariants, reset rules, observation intervals) are the
  integrator's to keep and grade; on the reference platform, `milan_dp`'s CTRS legs do
  that. This repository grades carriage and the push.
- Diagram 21 (the integrator's one-page contract) does not draw the read faces (`gsi_*`,
  `ctr_*`, `amap_*`). The guide carries them (§7 and §7.1).
- The optional AVB_INTERFACE FRAMES_TX, FRAMES_RX and RX_CRC_ERROR (Milan Table 5.14)
  are unclaimed on the reference platform.
- A parent comment nit for the pin-adoption lane: `milan_datapath.sv:3478` numbers the
  AVB_INTERFACE valid bits "Table 7-158"; IEEE 1722.1-2021 numbers them Table 7-152
  (offsets Table 7-153).
- GAP-04's remaining residue is not #78's acceptance: the Domain (F10.2) and VLAN
  (F10.3) machines are graded by directed cases, not a cell walk.
- Mutation campaigns not re-run: `aecp_mutants`, `aecp_dispatch_mutants`, `d3_mutants`,
  `acmp_mutants`, `gsi_mutants` and `name_wr_mutant`, plus the unit suites' own. Several
  plant into `protocol_processor_top.sv`, but none of their patches or exact edits names
  the removed tick or its wire, every patch still applies, and none of their targets
  reads the AVB_INTERFACE or CLOCK_DOMAIN counters.

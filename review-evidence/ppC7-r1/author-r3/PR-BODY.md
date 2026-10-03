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

## Merge of main

[A10] After REVIEW READY at `751e1c0`, the manager merged `main` `c74711d4` (PR #146, `--jobs` for the mutation drivers) into this branch as `e2c7d97d` (`--no-ff`).
- The files both sides changed are `tb/adp_engine/README.md` and `tb/pp_top/README.md`, at different lines, and they merged without a conflict.
- The GPTP_GM_CHANGED removal is ruled on #79 (comment 5963704232).
- The manager's banks and the reviews run at the merge head.

## Round 2

[A510] Round 2 (assignment: #79 comment 5963890173; addendum, item 5: #79 comment
5963896239), answering R442-1 (2 MINOR) and R443-1 (1 MINOR). Branch `c7-counters` from
`e2c7d97d`, nine commits, head `81edaaa`. Every finding was documentation. The RTL changes
only comment lines in two files (proved below); no port, parameter or register changes, so
no STOP condition was met.

| Commit | Item |
|---|---|
| `459f2fd` | 5 (the addendum, done first as it asks): `.gitattributes` for `tb/pp_top/ctr_mutations/*.patch` |
| `9078094` | 1. R442-1 F1: the GPTP_GM_CHANGED rule |
| `5599879` | 2. R442-1 F2 and R443-1 F1: no removed op and no in-processor counter block in 01, 05 and 06 |
| `52bf47b` | 3. R442-1 S1: the stale GET_COUNTERS paragraph |
| `d3f9e0f` | 3. R442-1 S2 = R443-1 F3: `ctr_mutants.py --jobs N` |
| `e27c070` | 3. R443-1 F2: the notify slot decode graded (K17, four arms) |
| `a34c505` | 3. R443-1 F4: STREAM_INPUT quadlets 6 and 7 |
| `274b424` | 4. R443-1 F5 and F6, the reviewer's exact text |
| `81edaaa` | the campaign record at `--jobs 1` and `--jobs 8` |

### 5. `.gitattributes`

`tb/pp_top/ctr_mutations/*.patch whitespace=-blank-at-eol,-blank-at-eof`, beside the other
campaigns' entries. `git diff --check c74711d4 HEAD` was rc 2 (three patches: blank context
lines as a single space, a blank line at EOF); it is rc 0 at `459f2fd` and at `81edaaa`.

### 1. GPTP_GM_CHANGED (R442-1 F1)

The AVB_INTERFACE duty in the integrator guide §7.1 now states the rule only as the identity
comparison: at each update the integrator publishes, count one when the grandmaster
identity on `gm_id_i` differs from the identity in force before it; the first identity
published out of reset counts nothing. It says outright that neither `gm_change_i`, nor
`gsi_asp_chg_i`, nor their coincidence identifies a grandmaster change: the first also
marks a domain-only update, the second any changed PathTrace (a tail-only one included),
and an integrator that publishes no path never raises it.

- It agrees with the guide's own table row, F06.15, the harness store
  (`tb/pp_top/sim_main.cpp:930-937`, graded by K11 and its arm
  `store-counts-domain-strobes`), the reference parent (`milan_datapath.sv:7267` at
  `cdf49d1a`, a change only against a prior identity) and the ruling (#79 comment
  5963704232).
- Clauses: Milan v1.2 §5.3.6.3 Table 5.1 ("Number of gPTP GM changes, since boot"); IEEE
  1722.1-2021 §7.4.42.2.2, Table 7-152 (mask `0x20`) and Table 7-153 (offset 20, "gPTP
  grandmaster change count"). The assignment and the ruling cite Table 7-112; in the
  printed IEEE 1722.1-2021 that is the IEEE 802.3 passive-optical-network media-subtype
  table, so the guide cites Tables 7-152 and 7-153.
- This supersedes item 2's wording above, "the update for which it raises `gm_change_i`
  and `gsi_asp_chg_i`".

### 2. 01, 05 and 06 (R442-1 F2, R443-1 F1)

- F01.3: the `counters` node and the `adapters --> ctrs` edge are gone. The 02 node names
  the landed faces ("srp/maap faces · gptp/avtp/mclk levels · gsi/ctr read faces ·
  side-port · nvm port") and reaches the µCPU as `gsi / ctr read words`. The block table's
  event-router row, the scope rows, §2's "adapter interfaces" sentence and §7's profile-ROM
  list (no STREAM_OUTPUT counter-mask ROM) follow.
- 05: F05.1's edge reads `srp declare/withdraw; the bound view` to
  `srp face + acmp_bound levels`. A8 issues `WITHDRAW_LISTENER` and no stream-datapath
  request; A9 says that it withdraws the bound view; F05.6's nodes follow.
- 06: F06.14's SET_CLOCK_SOURCE row ends in the committed index on the
  `aecp_clk_src_index_o` level (02 §4.5), not `mclk.SET_CLOCK_SOURCE`.
- The same rule beyond the three documents: 03's state-RAM row, the guide index row for
  06, docs/README's GPTP/AVTP/MCLK participants, and the listener's RTL comments
  (`KL_pp_acmp_listener.sv:25, :184, :188, :1162`, comment lines only).
- **A8 against the suggested wording.** A8 does not drop the bound view. It drives the
  `srp` withdrawal (`protocol_processor_top.sv:2615-2621`) and clears the record's settled
  fields; A9's discovery disarm clears the bound view (`:1808-1819`), and `acmp_bound_o`
  is its debounced copy. A8 without A9 is a settled sink re-probing, which keeps its
  binding. So A8 points at A9, and A9 states it. "`acmp_bound_o` falls" holds for the
  UNBIND_RX teardown (A8 then A9, F05.6), which `tb/pp_top` AS6 grades.
- Verification: R442-1's `stale_names.sh` prints nothing over `docs`, `hdl` and `tb`;
  R443-1's `grep -rnE 'avtp\.[A-Z_]+|srp \+ avtp adapters|gptp · avtp · mclk adapters' docs`
  finds nothing; `make check` rc 0.
- **Corrected in Round 3:** this item held for the Markdown and Mermaid sources only. The
  draw.io figures F01.1, F01.2 and F03.1 still drew an in-processor counter block (F01.2),
  counter banks (F03.1) and the gPTP, AVTP and media-clock adapters (R442-2 F1). Round 3
  redraws them.

### 3. Suggestions

- **R442-1 S1.** 06's "GET_COUNTERS keeps no counters" paragraph describes the landed
  `E_GCTRS`: the locate, a 17-µop hit path (eight four-beat `READ_CTRS`), an 11-µop miss
  arm that lays the zero body without asking the face, `E_GCTRSNS` falling into it, and
  ENTITY refused NOT_SUPPORTED. The two phrases S1 also names are corrected:
  `docs/10_RESOURCE_AND_EFFORT.md` ("the µCPU serves and latches counters") and the top's
  face comment (Table 5.6 alone).
- **R442-1 S2 = R443-1 F3.** `tb/pp_top/ctr_mutants.py --jobs N` through
  `tb/common/mutant_pool.py` (default 4, which the make target runs). Each unit runs in a
  scratch copy of its own, and results print in the declared order.
- **R443-1 F2, graded.** K17 strobes AVB_INTERFACE 1, CLOCK_DOMAIN 1, STREAM_INPUT 8 and
  STREAM_OUTPUT 8 (none has a slot at the default 8-by-8 shape), each alone. Each must
  push no unsolicited GET_COUNTERS for 1.5 s, past every window K13 to K16 left open.
  Then AVB_INTERFACE 0's own strobe must still push it, byte-exact. Four arms each remove
  one term of the decode (`KL_aecp_notify.sv:491-506`); the AVB_INTERFACE arm is the
  reviewer's probe P3. Each arm fails only its own K17 check.
- **R443-1 F4.** The guide names STREAM_INPUT quadlets 6 TIMESTAMP_VALID and 7
  TIMESTAMP_NOT_VALID, kept under `0x00000FFF` only. Its counts table gains a row: one per
  received stream data AVTPDU with the tv bit set / clear (IEEE 1722.1-2021 Tables 7-156
  and 7-157), reset with the input bank.

### 4. Residue (R443-1 F5, F6)

The reviewer's exact text, in 02:
- "`DESC_MEM_TMO_CYC_P` (the engine's `MEM_TIMEOUT_CYC_P`, 06 §8.1)" at both watchdog
  mentions (§4 and §4.6).
- "the internal MAAP engine (PortOperational!, [11](11_maap_engine.md)); the PRNG seed
  latch (first rise)", appended to the §5 `LINK_UP/DOWN` row's Consumers cell.

The posted comment renders F6's link against a milan-fpga evidence path that does not
exist. The text and its relative link are taken from the reviewer's packet.

### Validation (round 2)

All with the pinned Verilator 5.050.

| Command | Result |
|---|---|
| `./scripts/run_suites.sh` at `274b424` (all the code; `81edaaa` adds a README record) | rc 0: 33 suites, **1,019,116** checks, 0 failing. `tb/pp_top` 9,191 -> **9,196** (+5: K17; its counters build 23 -> 28); every other suite unchanged (`tb/adp_engine` 1,328) |
| `./scripts/run_suites.sh` at `81edaaa` | rc 0: the same 33 suites and per-suite tallies, 1,019,116 checks, 0 failing |
| `./scripts/lint_hdl.sh` (`274b424`, `81edaaa`) | rc 0, 41 of 41 |
| `make check` (`81edaaa`) | rc 0: 41 mermaid + 18 wavedrom blocks, 1,095 links, 115 REQ rows, 17 GAP findings, 94 module rows 0 untested, 27 parameters |
| `python3 scripts/gen_matrix.py --check` | rc 0 |
| `git diff --check c74711d4 HEAD` | rc 0 |
| `git apply --check`, every campaign patch in `tb/` | 224 of 224 (220 + this round's four) |
| `python3 tb/pp_top/ctr_mutants.py --jobs 1` | rc 0: control PASS, 17 of 17 KILLED, 940 s |
| `python3 tb/pp_top/ctr_mutants.py --jobs 8` | rc 0: control PASS, 17 of 17 KILLED, 699 s. Its printed record is byte-identical to `--jobs 1` (sha256 `0fd23cc6…` both) |

Both campaign runs used a `git archive` of `274b424`, each run alone and pinned to 4 of the
host's 16 CPUs. The per-arm record, also in the `tb/pp_top` README:

| Arm | Failing checks |
|---|---|
| `ctr-avb-not-supported` | 9: K9 (named), K10 x4, K11 x3, K12 |
| `ctr-ckd-not-supported` | 3: K16 x3 (named) |
| `ctr-index-from-type` | 18: K9 (named), K10 x4, K11 x3, K13, K14, K15 x3, K16 x4, K17 |
| `ctr-block-beats-swapped` | 9: K11 x3 (named), K13, K14, K15 x3, K17 |
| `ctr-locate-ignored` | 1: K12 (named) |
| `ctr-notify-avb-dropped` | 6: K13 (named), K14 x2, K15 x2, K17 |
| `ctr-notify-avb-as-clock` | 8: K13 (named), K14 x2, K15 x2, K16, K17 x2 |
| `ctr-notify-ckd-dropped` | 1: K16 (named) |
| `ctr-notify-one-window` | 3: K15 (named), K16, K17 |
| `ctr-notify-no-window` | 5: K14 x3 (named), K15 x2 |
| `ctr-change-type-from-index` | 8: K13 (named), K14 x2, K15 x3, K16, K17 |
| `ctr-notify-avb-any-index` (new) | 1: K17 AVB_INTERFACE 1 (named) |
| `ctr-notify-ckd-any-index` (new) | 1: K17 CLOCK_DOMAIN 1 (named) |
| `ctr-notify-stri-past-shape` (new) | 1: K17 STREAM_INPUT 8 (named) |
| `ctr-notify-stro-past-shape` (new) | 1: K17 STREAM_OUTPUT 8 (named) |
| `store-counts-domain-strobes` | 7: K11 x2 (named), K13, K14, K15 x2, K17 |
| `store-link-detector-resets-up` | 11: K9 (named), K10 x4, K11, K13, K14, K15 x2, K17 |

K17 adds failing checks to eight of round 1's thirteen arms, because its last check sees
their broken push or counts. No other count moved from round 1's record.

Parent consumer gates, all 16 rc 0, at milan-fpga dev `cdf49d1a`, set up as in round 1:
- a `git archive` of dev, made a repository, with its submodules as real checkouts at
  their pins;
- `protocol-processor` at `81edaaa`, its gitlink committed;
- `parent-adoption-c4c6-ea3fb388.patch` and then `parent-adoption-c8-cdf49d1a.patch`
  applied with `git apply`, both unchanged.

The light gates also passed at `274b424`.

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held (168 translation units, K17 among them; the multi-declarator count 0) |
| 3 | `xvlog_gate.py --check` (alone, last) | rc 0, 4 findings == ratchet |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded) |
| 6 | `sw/builder/test_builder.py` (alone) | rc 0, all gates pass except 1 not run (a board report not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0, protocol-processor 1,756 ports (unchanged from round 1) |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT readers |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS; its `[CTRS2]` legs read AVB_INTERFACE mask 0x23 and LINK_UP = LINK_DOWN + 1 through this processor |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

**Out-of-context cost: 0, by construction.** The two RTL files changed only comment
lines. `verilator -E -P` output, with comments stripped, is byte-identical at `e2c7d97d`
and at the head:
- `KL_pp_acmp_listener.sv`: 41,467 bytes, sha256 `5134a80a…`;
- `protocol_processor_top.sv`: 155,115 bytes, sha256 `dc511d2d…`.

The elaborator therefore sees the same source, and no synthesis was run. Round 1's
measured zero for the tick removal stands.

### Parent-visible list (round 2)

- **No interface change.** No port, parameter or register changes. The `ctr_*` face,
  `KL_pp_shadow` and the parent's GET_COUNTERS path are untouched. Both adoption patches
  are unchanged and apply.
- **RTL:** comment lines only, in `KL_pp_acmp_listener.sv` and `protocol_processor_top.sv`.
  The preprocessed source is identical.
- **Text the parent cites moves:**
  - the integrator guide §7.1: the GPTP_GM_CHANGED rule, and the STREAM_INPUT quadlets 6
    and 7 with their row;
  - 01 F01.3: the 02 node is now `faces`, and `ctrs` is gone;
  - 05: F05.1, F05.3's A8 and A9, and F05.6;
  - 06: F06.14's SET_CLOCK_SOURCE row, the §6.6 push paragraph (K17), and the GET_COUNTERS
    design paragraph;
  - 02: §4's read-face paragraph, §4.6, and the §5 `LINK_UP/DOWN` row;
  - 09 §8.6, and the 00 GAP-05 "Verified by".

  No anchor is removed. The `tb/pp_top` README heading "K9 to K16" is now "K9 to K17".
- **Tallies:** `tb/pp_top` 9,196; sweep 1,019,116; the ctr campaign has 17 arms.
- **New processor files the parent's gates see:** four patches in
  `tb/pp_top/ctr_mutations/`. `ctr_mutants.py` now imports `tb/common/mutant_pool.py`;
  gates 2 and 10 pass with it.

### What remains (round 2)

- **Mutation campaigns not re-run:** `aecp_mutants`, `aecp_dispatch_mutants`,
  `d3_mutants`, `acmp_mutants`, `gsi_mutants`, `notify_mutants`, `name_wr_mutant`, and the
  unit suites' own (`adp_engine`, `srp_top`, `maap` among them). The RTL is
  preprocessed-identical. No patch or exact-edit anchor touches a changed line, and every
  patch applies (224 of 224).
- **Not run:** the `tb/nvm_port` figures gate and the off-vendor yosys elaboration (CI
  jobs). Their inputs are untouched.
- **Unchanged from round 1:** the redundancy seam (one AVB_INTERFACE and one
  CLOCK_DOMAIN notification slot, interface-0 inputs, recorded for processor #69). K17
  now grades the slot rule as it stands.

## Round 3

[A513] Round 3 (assignment: #79 comment 5965236068), answering R442-2 (NEGATIVE on one
MINOR, F1; its S1 is taken). R443-2 is POSITIVE. Branch `c7-counters` from `81edaaa`, two
commits, head `9758a98`. The round changes three draw.io figures, their SVG exports and four
rows of F01.5, and nothing else: `git diff 81edaaa 9758a98 -- hdl tb scripts syn Makefile
.github` is empty. No STOP condition was met.

| Commit | Item |
|---|---|
| `0bcf856` | 1. R442-2 F1: F01.1, F01.2 and F03.1 redrawn to the landed top |
| `9758a98` | 2. R442-2 S1: F01.5 names no "counters" |

### 1. The figures (R442-2 F1)

Each figure was edited in its draw.io source (`docs/diagrams/src/`) and re-exported with the
repository's own rule, `make docs/diagrams/<name>.svg`: the draw.io CLI under `xvfb-run`,
which completes on this host. No SVG was edited by hand. Each export was rendered to PNG and
checked for overlap, clipped text and edges through boxes, as `docs/diagrams/README.md` asks.

- **F01.2, processor top level** (`01-top-level.drawio`):
  - The "Counters subsystem" block and its edge from the AECP engine are gone.
  - The "External-engine adapters" group (the gPTP, SRP/MAAP, AVTP and media-clock adapters)
    is now "External-engine faces (02 §4)". It holds three faces, the same split as 01's
    block-table row and F01.3's `faces` node:
    - "srp · maap faces (class B)", served in core by the SRP engine (10, the default) and
      the MAAP engine (11, opt-in);
    - "gPTP · AVTP · media clock", class-D levels and change strobes;
    - "gsi · ctr read faces", the GET_* words and change strobes.
  - A new `words` edge runs from the read faces into the AECP engine. It draws the block
    table's "GET_COUNTERS read path" and F01.3's `gsi / ctr read words`.
  - The group's `events` edge into the event router stays.
- **F03.1, shared datapath** (`03-shared-datapath.drawio`):
  - The "counter banks" store is gone. The state-RAM complex holds the image and overlay,
    the dynamic state and the registry, as 03's table row says.
  - The "adapter events" source now reads "integrator strobes + level edges · SRP · MAAP ·
    ADP engine events", the producers in 02 §5's catalog.
  - The router's output reads "to SMs / notifications".
- **F01.1, system context** (`01-system-context.drawio`):
  - The processor box lists "GET_COUNTERS reporting", as 01 §1 and §2 say.
  - The gPTP, AVTP and media-clock edges were tagged `B/C/D`, which implies a class-B face
    the landed top does not have. They now carry their landed classes: `D · gsi · ctr`,
    `D · gsi · ctr` and `D · ctr` (02 §4.3 to §4.6). The srp/maap edge keeps `B/C/D`.
  - The legend gains one line for the gsi and ctr read faces.
- **Verification:**
  - R442-2's grep (`grep -o 'value="[^"]*"' docs/diagrams/src/{01-top-level,03-shared-datapath,01-system-context}.drawio | grep -iE 'counter|gptp.*adapter|avtp|media-clock.*adapter'`)
    prints four labels at the head:
    - F01.2's "gPTP · AVTP · media clock" levels face;
    - three in F01.1: the processor box with "GET_COUNTERS reporting", the external
      "AVTP streaming engine" box, and the legend line.

    None of them is an in-processor counter block or an adapter.
  - No SVG export contains "adapter", "Counters subsystem", "counter banks" or "to SMs /
    counters". The five hand-drawn SVGs (20 to 24) contain none of them either.
  - `make check` rc 0, including `stale`.
  - `stale` negative control: an uncommitted edit to `01-top-level.drawio` makes it fail
    (rc 2, "uncommitted source edit newer than the export").

### 2. F01.5 (R442-2 S1)

The processor scales only its GET_COUNTERS notification slots: one per stream index, plus
AVB_INTERFACE 0 and CLOCK_DOMAIN 0 (`KL_aecp_notify.sv:382-385`, graded by K17).
- P-N-STREAM-IN and P-N-STREAM-OUT now affect "counter-notification slots", not "counters".
- The P-N-AUDIO-UNITS / P-N-CLOCK-DOMAINS / P-N-CLOCK-SOURCES row drops "counters": there is
  one CLOCK_DOMAIN slot, whatever the parameter is.
- S1 also names P-N-AVB-INTERFACES, whose "counters" is in its redundancy-seam note. That
  note now reads "counter-notification slots": the single AVB_INTERFACE slot is the seam
  #69 owns.

### Correction to Round 2, item 2

Round 2's item 2 ("no removed op and no in-processor counter block in 01, 05 and 06")
held for the Markdown and Mermaid sources only. The draw.io figures F01.1, F01.2 and F03.1
still drew the counter block, counter banks and the gPTP, AVTP and media-clock adapters
(R442-2 F1). Round 1's "01, 03 and 06's stale 'counters subsystem' rows and nodes are
corrected" had the same gap. This round's item 1 closes it.

### Validation (round 3)

All runs used the pinned Verilator 5.050 and a scratch copy at `9758a98`.

| Command | Result |
|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 suites, **1,019,116** checks, 0 failing; every per-suite tally equals round 2's (`tb/pp_top` 9,196, `tb/adp_engine` 1,328) |
| `./scripts/lint_hdl.sh` | rc 0, 41 of 41 |
| `make check` | rc 0: 41 mermaid + 18 wavedrom blocks, 1,095 links, 115 REQ rows, 17 GAP findings, 94 module rows 0 untested, 27 parameters; `stale` passes |
| `make stale`, negative control | rc 2 on an uncommitted edit to `01-top-level.drawio`; rc 0 once reverted |
| `make -C tb/nvm_port figures` (the CI figure gate) | rc 0, "all measured figures agree with the tree" |
| `git diff --check c74711d4 HEAD`; `git diff --check 81edaaa HEAD` | rc 0; rc 0 |
| `git apply --check`, every campaign patch in `tb/` | 224 of 224 |
| `python3 tb/pp_top/ctr_mutants.py --jobs 8` | rc 0: control PASS, 17 of 17 KILLED, 341 s. Its printed record is byte-identical to round 2's (sha256 `0fd23cc6…`, 11,104 bytes) |

Parent consumer gates, all 16 rc 0, at milan-fpga dev `cdf49d1a`. The scratch copy was
set up as in rounds 1 and 2:
- a `git archive` of dev, made a repository, with its submodules as real checkouts at
  their pins;
- `protocol-processor` at `9758a98`, its gitlink committed;
- `parent-adoption-c4c6-ea3fb388.patch` and then `parent-adoption-c8-cdf49d1a.patch`
  applied with `git apply`, both unchanged.

| # | Gate | Result |
|---|---|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | rc 0, every ratchet held (168 translation units) |
| 3 | `xvlog_gate.py --check` (alone, last) | rc 0, 4 findings == ratchet |
| 4, 5 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | rc 0 (36/42 tops, 6 recorded) |
| 6 | `sw/builder/test_builder.py` | rc 0, all gates pass except 1 not run (gate 11, a board report not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | rc 0, protocol-processor 1,756 ports |
| 9 | `measure_naming.py --check` | rc 0, 96 recorded |
| 10 | `measure_test_evidence.py --check` | rc 0, 0 <= 0 unexplained DUT readers |
| 11 | `docs_check.py` | rc 0, 0 findings |
| 12 | `lint_rtl.py --check` | rc 0, 90 <= 90 |
| 13, 14 | `nvm_cosim` lint and quick | rc 0, 315/315 |
| 15 | `make -C tb/verilator/milan_dp -j16` | rc 0, 9 RESULT PASS; its `[CTRS2]` legs read AVB_INTERFACE mask 0x23 and LINK_UP = LINK_DOWN + 1 through this processor |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | rc 0, leg defects 5/5 |

**Out-of-context cost: 0, by construction.** No RTL changes (`git diff 81edaaa 9758a98 --
hdl` is empty), so no synthesis was run. Round 1's measured record stands.

### Parent-visible list (round 3)

- **No interface change.** No port, parameter or register changes. The `ctr_*` face,
  `KL_pp_shadow` and the parent's GET_COUNTERS path are untouched. Both adoption patches
  are unchanged and apply.
- **No RTL, test or script change.**
- **Figures and text the parent cites move:**
  - F01.1, F01.2 and F03.1: the draw.io sources and their SVG exports;
  - F01.5's P-N-AVB-INTERFACES, P-N-STREAM-IN, P-N-STREAM-OUT and P-N-CLOCK-DOMAINS rows.

  No anchor changes.
- **Tallies:** unchanged. `tb/pp_top` 9,196; sweep 1,019,116; the ctr campaign has 17 arms.

### What remains (round 3)

- **Outside this round's scope** (the assignment stops at the figures and F01.5), and left
  as found:
  - `docs/00_MILAN_COMPLIANCE_REVIEW.md:366`: REQ-ADP-009's mechanism cell still reads
    "GPTP adapter event". The landed source is the `gm_change_i` strobe (02 §4.3, §5).
    This is text, not a figure, and no review has named it. It is left for a docs pass.
  - F03.1 still draws the descriptor image on chip. That older divergence is stated in the
    note under the figure and in `docs/guides/hdl-engineer.md:255`. Moving the image off
    chip in the drawing would make both texts wrong, and correcting them is text beyond
    this round.
  - R443-2's two SUGGESTIONs were not taken by the assignment: the zero-identity case of
    the GPTP_GM_CHANGED rule, and F09.1's "mask ROMs".
- **Not re-run:** every mutation campaign except the ctr one, and the off-vendor yosys
  elaboration. Their inputs are byte-identical to `81edaaa`.

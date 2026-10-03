# [A515] Lane P1 handoff: persistence beyond BINDING

Branch `p1-persistence` from `main` `ddb3119d`. Issues #52, #59, #61, #62, #63 and #83.
Assignment: issue #83, comment 5965788915. Ruling on the lane's STOP: #83 comment
5967611704. Parent: milan-fpga dev `1269cdaf`, with `parent-adoption-c8-cdf49d1a.patch`
and then `parent-adoption-p2-p1-1269cdaf.patch`, the successor of
`parent-adoption-p2-cdf49d1a.patch` (section 3, item 10).

Status: **round 2, REVIEW READY** at `5960d8f` (section "Round 2" at the end): the
three MINOR documentation findings of R444-1 and R445-1 on PR #150, docs and comments
only. Round 1b stopped at `c066dd8` after the merge of `main` `f4167536` (section
"Round 1b"): parent gate 16 fails at dev `bbf704ec` (R1b.4), ruled (b) on #83
(5969246536) and recorded against milan-fpga #643; every other gate and every processor
suite and campaign passes. Round 1 was **REVIEW READY**
at `53e1474` (gates in section 4), posted on #83 (comment 5968343520). History:
- Items 1 to 3, item 4's name stage and item 5 were implemented and validated at
  `4b02d4f`, where the lane stopped on the channel maps ("[A515] STOP", comment
  5967588719).
- The manager ruled option (b): the integrator owns the maps' persistence (comment
  5967611704).
- The lane resumed at `4b02d4f` and finished the ruling's items (section 2, R1 to R3):
  - R1, the D3 contract amendment (docs only, no RTL), `b88240a`;
  - R2, the standing seeded-random reset-cut campaign with its two controls, `53e1474`;
  - R3, the Closes lines: the PR now closes all six issues.

## 1. Design

### 1.1 What main already persists, per issue, at `ddb3119d`

The issues were filed against main `6a878f6`. Since then main has gained D3 save/restore
(#131, the parent's #70 lanes 1 and 2), the D3 writer `KL_aecp_nvm_writer`, P141's
ten-source clock domain, and P2's port deadline. Main at `ddb3119d` now has the
following:

- **Two record producers on one port.** Manager 0 is the binding manager
  (`hdl/acmp/KL_acmp_nvm_shadow.sv`, records `0x20`+sink). Manager 1 is the D3 writer
  (`hdl/aecp/KL_aecp_nvm_writer.sv`, instantiated at `hdl/aecp/KL_aecp_engine.sv:1987`). Both
  sit behind `KL_pp_nvm_mgr_arb` (`hdl/top/protocol_processor_top.sv:2855`).
- **The D3 writer's records** (`KL_aecp_nvm_writer.sv:97-109`): `0x00` configuration,
  `0x02`+AUDIO_UNIT rate, `0x0A`+CLOCK_DOMAIN clock source, `0x30`/`0x40`+stream format
  in/out, `0x50`+STREAM_OUTPUT presentation offset. They are framed as F07.8.
- **Triggers.** A record's dirty bit is set by the live changing write on the µCPU's side of the
  state-bus selection (`KL_aecp_engine.sv:1980`, `KL_aecp_nvm_writer.sv:897-903`).
  IDENTIFY (selector 7) is never a trigger.
- **The restore.** Two agreeing passes, value rules and a roll-back
  (`KL_aecp_nvm_writer.sv:626-819`). AECP is held until the D3 terminal. ADP is enabled only at
  `restore_done_o` (`protocol_processor_top.sv:1861`, `:2781`).
- **Completion marks.** `aecp_nvm_stb_o` and `aecp_nvm_mark_o` are top outputs carrying the
  marks as completion notifications (`protocol_processor_top.sv:766-779`). They are no
  longer `_nc_` nets. The parent reads them as unused (`KL_pp_shadow.sv:968`).

Per issue (each acceptance line, and what is MET or MISSING):

| Issue | Acceptance line | At `ddb3119d` |
|---|---|---|
| #52 | 1. CLKSRC committed after an accepted SET through the debounced port | MET: `tb/pp_top/d3_phases.hpp` D3S1 `clks` (:527-553), D3C3 save (:2873-2892) |
| #52 | 2. GET_CLOCK_SOURCE and `aecp_clk_src_index_o` report the saved index before entity enable; a blank or torn record falls back to the image value | PARTLY MET: D3C3 restore (:2939-2958) grades GET, the row and the export. D3R1 (:1137-1142) grades that the enable waits for the terminal. No check reads the export at the enable's rising edge. No check grades a blank, torn or corrupt **CLKSRC** record's fallback through GET and the export |
| #52 | 3. Commit bytes and the restored value are graded; a refused SET commits nothing | MET: D3S1, D3C3; D3C2 (:2894-2934) |
| #52 | 4. `eff_nvm_*` consumed or removed; REQ-AEM-013 updated | MET: exported as completion marks (`protocol_processor_top.sv:778-779`); `docs/00_MILAN_COMPLIANCE_REVIEW.md:407` |
| #59 | 1. Two controllers registered, one TIME_LIMITED; rst_n; a third controller's change reaches neither | MISSING. D3R1 (`d3_phases.hpp:1160-1174`) registers one non-TIME_LIMITED controller only |
| #59 | 2. No CONTROLLER_AVAILABLE and no expiry DEREGISTER toward the pre-reset controllers | MISSING |
| #59 | 3. Sixteen fresh REGISTERs succeed; a re-registered controller starts at sequence_id 0 | MISSING |
| #59 | 4. Mutant: `valid_r <= '0` removed from the reset arm (`KL_aecp_notify.sv:916`), recorded in the README | MISSING |
| #62 | 1. Lock, two registrations, IDENTIFY 255, then rst_n and restore_go over media holding a valid BINDING record | PARTLY: D3R1 has the lock, one registration and IDENTIFY 255, but no binding record |
| #62 | 2. LOCK_ENTITY from a second controller succeeds; `aecp_lock_held_o` 0; no notification to the former controllers; IDENTIFY 0; the binding preload arrives | PARTLY: D3R1 has the lock free, no notification to the one controller and IDENTIFY 0. There is no LOCK_ENTITY from a second controller and no binding preload in the same cycle |
| #62 | 3. Mutants removing `lk_held_r`, the registry valid bits or `ident_r` from the reset branch, recorded in the README | MISSING (`KL_aecp_notify.sv:916-919`, `KL_aecp_dyn_state.sv:311`) |
| #63 | 1. CFG_IDX committed debounced and restored with its valid flag before entity_enable | MET: D3S1 `cfg`, D3R1 `cfg` (:1179-1182), D3R1 enable (:1137-1142) |
| #63 | 2. SET 1, debounce, rst_n, restore: GET_CONFIGURATION and ENTITY.current_configuration read it; a blank or corrupt record falls back to the image default | PARTLY MET: `tb/pp_top/sim_main.cpp` AD5 (:11050-11073) does the save, reboot and restore and checks GET, ENTITY and the ADPDU. AD7 (:11107-11124) covers a blank record and AD6 a roll-back. No check grades a **corrupt** (crc) or torn record 0x00 |
| #63 | 3. Delivered inside the REQ-PER-001 ticket, listing CFG_IDX | MET: the D3 inventory lists `0x00` (07 §5.2) |
| #61 / #83 | Scalars: RATE, FMT_IN/OUT, PT_OFS, CLKSRC committed and restored | MET (#131, D3S1/D3R1) |
| #61 / #83 | NAMES[n]: committed and restored after the image walk | MISSING: `07_memory_maps.md:590` says "accepted, not implemented (name stage)". `KL_aecp_desc_store.sv:41-44` says the same |
| #61 / #83 | MAPS_IN/OUT[p]: committed and restored | MISSING: `07_memory_maps.md:588-589`; the map plane is the parent's |
| #61 / #83 | Every record type cut mid-commit; randomized cut points; a real rst_n cut | PARTLY: `tb/nvm_port` T25 does rst_n mid-commit at six stages; D3S4/D3S5 cover taint; `tb/nvm_port` FZ* is the randomized harness for the port. No D3 record type is cut by rst_n mid-commit |
| #61 / #83 | GAP-08/GAP-09, REQ-AEM-011/-021 and 06 stop pointing at an open item | PARTLY: they point at the name and map stages, which are open |

This table is main's state. The state at the head, line by line, is section 2 (items 1
to 4) and R3, its acceptance table for #61 and #83.

### 1.2 What Milan requires

| State | Requirement | Clause |
|---|---|---|
| Clock source (#52) | "The current clock source shall be saved in a non-volatile memory and restored after a power cycle." | Milan v1.2 §5.3.11.1; SET/GET_CLOCK_SOURCE §5.4.2.15/.16, IEEE 1722.1-2021 §7.4.23/§7.4.24 |
| Sampling rate, stream formats, presentation offset (#61) | saved and restored | Milan v1.2 §5.3.5.1, §5.3.7.1, §5.3.8.1, §5.3.7.6 |
| Output and input channel maps (#61, #83) | "This list shall be saved in a non-volatile memory and restored after a power cycle." | Milan v1.2 §5.3.9.1 (output), §5.3.10.1 (input) |
| User names (#61, #83) | the eleven name kinds "shall have a default value which is vendor-specific and shall be modifiable by the user. The PAAD-AE shall save them in a non-volatile memory and restore them after a power cycle." | Milan v1.2 §5.3.13; SET/GET_NAME §5.4.2.11/.12, IEEE 1722.1-2021 §7.4.17/§7.4.18 |
| Current configuration (#63) | Milan is silent. Persisting it is a design decision (review §8 item 1), retained by the parent D3 contract §16 | none; IEEE 1722.1-2021 §7.4.7/§7.4.8 |
| Lock (#62) | "The locked state is cleared by a power cycle." | Milan v1.2 §5.3.4.1; IEEE 1722.1-2021 §7.4.2 |
| Controller registry (#59, #62) | "The list of registered controllers is cleared by a power cycle." Each entry carries "the Sequence ID of the next unsolicited notification" | Milan v1.2 §5.3.4.2; IEEE 1722.1-2021 §7.4.37 (TIME_LIMITED §7.4.37.2) |
| IDENTIFY (#62) | "value 0 when the entity is not in identification mode (default mode after reset)" | Milan v1.2 §5.3.12 |
| Restore before advertising | the restored binding starts in PRB_W_AVAIL; the restore precedes the entity's advertisement | Milan v1.2 §5.5.3.5.2, §5.6.1 |

### 1.3 The record format, census and saved-state size

No record format changes. Every record keeps the F07.8 framing `{magic 0x1722,
layout_version 0x02, record_id, payload_length, crc16 CCITT-FALSE}` (07 §5.2), at the
id the parent allocation already assigns (FASTCONNECT §4.2, restated at
`07_memory_maps.md:577-590`).

**The one new record class: NAME[n], ids `0x80 + n`, payload 64 bytes, the AEM
string verbatim.** It is written by the D3 writer, with one record per writable-name ordinal n in
`0 .. DESC_NAME_ENTRIES_P - 1`:

- **Trigger.** The descriptor store's accepted live name-lane write (`name_wr_o`, the top's
  `aecp_name_wr_o`), taken while the µCPU drives the state bus, sets dirty[n] for
  `n = st_addr[15:6]`. SET_NAME writes only the lanes that change (`gen_ucode.py:2370-2379`).
  So an unchanged name sets nothing (DR2b), and a restore write is never a change.
- **Latch.** ACQUIRE holds dispatch until no program runs. Then the writer reads the entry's
  eight 64-bit lanes over the state bus (the name region, `st_name`) into a 64-byte
  buffer, releases dispatch, frames the record and writes it. A change after the latch
  taints the write, and the clear rule is the scalars'.
- **Restore.** The restore walk reads the name records after the scalar records, in both passes.
  Pass 1 keeps the 64-byte payload. A framed record is judged by SET_NAME's rule:
  the name index exists. Under the one-record-per-ordinal mapping that means
  `n < n_names`, the image's name count. The store publishes that count on a new read
  region `0xA` (internal address map, no port). The eight lanes are then written back over
  the state bus. The image is always proven first (W_IMG/W_IMGLOC), so a name written
  back is never overwritten by the store's walk (parent D3 §8.5). A roll-back resets
  the store, which walks the image again: every name returns to the image default.
- **Census.** Unchanged. The parent's inventory already holds one NAME row per name-store
  entry (`scripts/nvm_shape.py:246-247`). The backend backs `N_NAME_P =
  DESC_NAME_ENTRIES_P` records (`KL_pp_shadow.sv:1007`). The capture copies every
  allocated record whether written or not (`tb/verilator/nvm_capture_cpu/README.md`).

| Shape | D3 writer records before → after | Of which names | Census (records, framed bytes) | 8x8 capture vs 24.5 ms |
|---|---|---|---|---|
| 1x1 TDM8 | 9 → 47 | 38 × 72 B = 2,736 B | 53, 3,218 B (unchanged) | n/a (3.89 ms measured) |
| 8x8 | 30 → 129 | 99 × 72 B = 7,128 B | 156, 12,634 B (unchanged) | unchanged: 13.23 ms measured at 50 MHz, margin 3.70 against the 49 ms floor |
| processor bench (`DESC_NAME_ENTRIES_P` 32) | 27 → 59 | 32 | n/a | n/a |

Saved-state size impact: none. The NAME span `0x80..0xFF` is already allocated and
already copied. What changes is how many of those records a power cycle can bring
back. The restore reads 2 × (9 + 38) records at 1x1 and 2 × (30 + 99) at 8x8. An erased
record costs its header read only. The per-wait deadline (20 ms) bounds each wait, not
the walk. The restore's added length is measured in `tb/pp_top` and reported in
section 3, item 7, against the ratified 1,000 ms aggregate.

**Channel maps (MAPS_IN/OUT[p], ids `0x60`/`0x70` + port): the integrator's.** The
manager ruled on STOP item M1 (section 1.4) that the integrator persists them. The
processor writes and reads no map record. Its census, record space and capture are
unchanged: the records are already allocated and copied. Section 2, R1 has the amended
contract.

### 1.4 STOP review

| Candidate | New top port, parameter or register? | Census, record space, capture timing or saved-state contract moved? | `KL_pp_shadow` or parent gate change? | Verdict |
|---|---|---|---|---|
| Items 1 to 3 (tests, docs) | no | no | no | proceed |
| Item 4, names | no: the writer and the store are internal to `KL_aecp_engine`; their ports are not instantiated by the parent (`nvm_cosim` instantiates `KL_aecp_dyn_state`, `KL_acmp_nvm_shadow`, `KL_pp_nvm_mgr_arb` and `KL_pp_nvm_port`, which are all unchanged) | no: names are stage 2 of the accepted contract (parent D3 §3.1, §10, §18.3); the ids are allocated and copied | none needed: `pend_i` keeps the sticky live-name term until the parent's own adoption lane transfers it (D3 §10, §18.3). Verified by running the 16 gates | proceed |
| Item 4, maps | **yes**: the contract's roll-back resets the parent's map plane from the processor's roll-back strobe (D3 §5.1 roll-back row, §5.2), which no top port carries today. The record lengths are the parent's per-port capacities (#501), which are not top parameters | no census growth (records `0x60`/`0x70` already allocated and copied), but the alternative, assigning maps to the integrator (#83 acceptance 1's "or"), moves the saved-state contract (D3 §3 rule 1, §18.4) | **yes**: `milan_datapath.sv` and `KL_chan_map_capture.sv` take the strobe via `KL_pp_shadow` | **STOP item M1**, ruled (b) |
| R1, the amendment (after the ruling) | no: documents only. The integrator's restore uses existing top ports (`restore_done_o`, `restore_rb_o`, `aecp_fmt_in/out_o` and their valid bits, the `amap_*` faces and their waits) | no: the records stay allocated and copied as they are; the saved-state contract changes as the ruling decided | no gate change. The parent's D3 page states the old rule, so its patch has a successor (section 3, item 10) | proceed (ruled) |
| R2, the campaign | no: bench only (`tb/pp_top`) | no | no | proceed |

**STOP item M1: channel maps** (posted at `4b02d4f`; ruled (b), comment 5967611704).
Parent impact, as posted:
- Census growth: none. 1x1 has 2 map records; 8x8 has 16, including 72-entry output records
  of 584 framed bytes and 4,672 output-map bytes. These already sit inside the 156-record,
  12,634-byte copy.
- Effect on the 8x8 capture against the 24.5 ms limit: none. The measured 13.23 ms at
  50 MHz (`measurements.json`) stands, because the capture copies every allocated record
  whether written or not.
- What it needs from the parent, either way:
  - (a) A new top output carrying the D3 roll-back to the map plane, through
    `KL_pp_shadow` into `milan_datapath.sv`/`KL_chan_map_capture.sv`.
  - (b) Per-port map capacities in the processor, as new top parameters or as an
    image derivation that must equal the backend's table (#501).
  - (c) The coupled format/map restore of D3 §8.4 over the parent's edit face.
- Or, instead: a ruling that assigns maps to the integrator, which amends the D3 contract.

## 2. Items

Commits, in item order (one-line subjects):

| Commit | Items |
|---|---|
| `ca49b56` | 1 (#59, #62), 2 (#63), 3 (#52) |
| `a1f5cd5` | 4 (#61, #83): the name stage, and every D3 record type cut mid-commit |
| `084be15` | 4: two lines the parent's idiom gates refused |
| `0c98b22` | 5: every D3 control re-measured at the head (108 killed); the HDL guide |
| `2b2ad18` | 5: the name-write mutant re-anchored on the gated export |
| `4b02d4f` | 5: the hazard and ADP campaigns re-run, with the counts the lane moved |
| `b88240a` | R1 (ruling item 1): the D3 contract amendment, the maps the integrator's (docs only) |
| `53e1474` | R2 (ruling item 2): the standing seeded-random reset-cut campaign D3KR and its two controls |

### Item 1: #59 and #62, the volatile set graded across a reset

- **Change.** A new section, D3V, in `tb/pp_top/d3_phases.hpp:3574`, run by `--volatile-only` (`make volatile`,
  `tb/pp_top/sim_main.cpp:10769`) and in the default run. No RTL change: main's reset
  arms already clear the state (`hdl/aecp/KL_aecp_notify.sv:916-919`,
  `hdl/aecp/KL_aecp_dyn_state.sv:298,311`).
- **Clauses.** Milan v1.2 §5.3.4.1 (lock), §5.3.4.2 (registry), §5.3.12 (IDENTIFY 0
  after reset), §5.4.2.21 (a new entry's sequence_id 0); IEEE 1722.1-2021 §7.4.2,
  §7.4.37.2 (TIME_LIMITED).

| Check | What it grades | Failing mutant (`tb/pp_top/d3_mutants.py`) |
|---|---|---|
| D3V1 | premise: a saved BINDING record restored; one controller registered and a second TIME_LIMITED, each notified at sequence_id 0 by a third controller's change; the first holds the lock (the second refused ENTITY_LOCKED) and IDENTIFY reads 255 | (premise) |
| D3V2 | after `rst_n` and `restore_go_i` over the same media, the binding preload still arrives: sink 0 bound, GET_RX_STATE answers the saved talker | no D3V control: the preload is the binding manager's, whose own controls grade it (`tb/acmp_nvm` F-section, mutation record M1 to M6; `tb/pp_top` D3R11) |
| D3V3 | IDENTIFY 0 in every cycle from `restore_go_i`, GET_CONTROL reads 0 | `identify_survives_reset` (`ident_r` deleted from the reset branch) |
| D3V4 | `aecp_lock_held_o` 0 in every cycle from `restore_go_i` | `lock_survives_reset` (`lk_held_r`) |
| D3V5 | a third controller's change notifies neither former controller | `registry_survives_reset` (`valid_r`), `lock_survives_reset` |
| D3V6 | for 66,000 ms (the monitor's longest 60 s draw, U10's margin) no frame reaches either former controller: no CONTROLLER_AVAILABLE, no expiry DEREGISTER | `registry_survives_reset` |
| D3V7 | LOCK_ENTITY from the second controller SUCCESS, then its UNLOCK | `lock_survives_reset` |
| D3V8 | sixteen new controllers all register | `registry_survives_reset` |
| D3V9 | a former controller re-registers and its first notification carries sequence_id 0, byte-exact | `registry_survives_reset`, `lock_survives_reset` |

### Item 2: #63, the current configuration index

Main already saves record `0x00` and restores it before the enable (D3S1, D3R1, AD5,
AD6, AD7). The lane adds the corrupt and torn arms of acceptance 2.

- **Change.** AD8 and AD9 in `tb/pp_top/sim_main.cpp:11163,11178` (section AD,
  `--adp-only`).
- **Clauses.** The design decision of review §8 item 1 (Milan is silent); IEEE
  1722.1-2021 §7.4.7/§7.4.8; F07.8 framing (07 §5.2).

| Check | What it grades | Failing mutant |
|---|---|---|
| AD8 | record `0x00` carrying configuration 0 (legal, not the default) with a wrong crc is refused by the frame; COMPLETE, row unset; the first ADPDU, GET_CONFIGURATION and READ_DESCRIPTOR(ENTITY).current_configuration carry the image default 1 | `cfg_crc_ignored` |
| AD9 | the same record read torn (pass 0's payload READ ended after one byte): the walk fails whole, cause 1; the three views carry 1 | `torn_read_not_an_abort_cfg` |
| AD7 (main's, newly controlled) | a blank record keeps the image default | `blank_applies_zero_cfg` |

### Item 3: #52, the clock-source selection

Main already met acceptance lines 1, 3 and 4 (D3S1 `clks`, D3C1 to D3C4). Line 4's marks
are exported as completion notifications, `aecp_nvm_stb_o`/`aecp_nvm_mark_o`, no longer
`_nc_`. The lane adds line 2's fallback and before-enable arms.

- **Change.** D3C5 and D3C6 in `tb/pp_top/d3_phases.hpp:3012,3055`.
- **Clauses.** Milan v1.2 §5.3.11.1, §5.4.2.15/.16; IEEE 1722.1-2021 §7.4.23/.24,
  §7.2.32.

| Check | What it grades | Failing mutant |
|---|---|---|
| D3C5 blank | record `0x0A` erased: row unset, GET_CLOCK_SOURCE and `aecp_clk_src_index_o` read the image's 0 | `blank_applies_zero` |
| D3C5 corrupt | index 2 with a wrong crc: refused, the same three read 0 | `clks_crc_ignored` |
| D3C5 torn | pass 0's payload READ torn: DEFAULTS, cause 1, the same three read 0 | `torn_read_not_an_abort` |
| D3C6 | the saved index 2 is exported, its row valid, in every cycle the ADP engine's enable is high, the first included | `enable_not_released_by_restore` |

### Item 4: #61 and #83, the AECP dynamic state, maps and names

The dynamic state (scalar stage) was already done on main (#131). The lane implements
the **name stage**. The **maps** were STOP item M1; the ruling assigns them to the
integrator (R1 below).

**RTL** (clauses: Milan v1.2 §5.3.13, §5.4.2.11/.12; IEEE 1722.1-2021 §7.4.17/.18;
parent D3 §3.1, §8.5, §18.3):

- `hdl/aecp/KL_aecp_nvm_writer.sv`:
  - `N_NAME_P` (`:185`; 1 to 128, refused past the `0x80..0xFF` block at `:311`), so
    records number `OFF_NAME_C + N_NAME_P`.
  - The name group 6 in the record geometry: id `0x80` + ordinal, payload 64.
  - The name snoop `nchg_i` (`:1003`).
  - The service latch S_NLATCH (`:1144`), eight lanes read over the state bus with the
    name table selected (`sb_name_o`, `:1224`), into the name buffer (`:522`, eight
    64-bit lanes, a LUT RAM).
  - The framing reads payload bytes from that buffer.
  - The restore captures a name record's payload lanes (`rd_lane_w`, `:531`).
  - SET_NAME's rule W_NNAME (`:686`: ordinal below the image's name count) and the
    eight-lane write-back W_NAPPLY (`:839`).
- `hdl/aecp/KL_aecp_desc_store.sv`: region 0xA reads the image's writable-name count, 0
  while the image is invalid (`:254`, `:899`).
- `hdl/aecp/KL_aecp_engine.sv`: the writer drives the name select (`:1628`). The name
  snoop and the exported `name_wr_o` are both the store's acceptance gated off the
  writer's bus (`:1993-1994`). `N_NAME_P = NAME_ENTRIES_P` (`:2006`).
- `hdl/top/protocol_processor_top.sv`: comments only (`DESC_NAME_ENTRIES_P`,
  `d3_unflushed_o`, `aecp_name_wr_o`, the marks). No port or parameter added.

**Tests** (D3N `tb/pp_top/d3_phases.hpp:3104`, D3K `:3426`; region 0xA in
`tb/desc_store/sim_main.cpp` G1/U1):

| Check | What it grades | Failing mutant |
|---|---|---|
| D3N1 | a real SET_NAME of both ENTITY names (the group name a full 64 bytes), CLOCK_DOMAIN 0's EMPTY name, the IDENTIFY CONTROL's name and the last ordinal each becomes one ERASE and one WRITE of `0x80`+ordinal, byte-exact; no other record; nothing unflushed | `TRG_name`, `name_record_id_shifted` |
| D3N2 | an unchanged SET_NAME writes no lane, nothing pending, no device operation (DR2b) | no dedicated control: what makes it hold is SET_NAME's own lane compare (`gen_ucode.py` E_SNAME), whose no-pulse arm section NW grades |
| D3N3 | across a power cycle: the entries hold the image's names at the image proof (cleared first); COMPLETE with the five applied; entries, GET_NAME (byte-exact) and READ_DESCRIPTOR(ENTITY) carry the saved names; the restore pulses no `aecp_name_wr_o` and makes no change | `RPL_name`, `name_entry_shifted`, `name_lanes_partial`, `name_empty_refused`, `name_restore_pulses`, `name_restore_is_a_change` |
| D3N4 | ordinal 20 (past the image's 11) refused by the rule; a corrupt crc and an 8-byte payload refused by the frame; a neighbour applied | `name_rule_ignored` |
| D3N5 | a pass-1 abort after a name applied rolls the name back with the descriptor store | `store_not_rolled_back` |
| D3N6 | a SET_NAME while the record's WRITE is held taints it: two WRITEs, the record ends with the second | `name_taint_ignored`, `taint_ignored` |
| D3N7 | an image loaded late is walked at the writer's LOCATE before the name is written back | `names_before_the_image` |
| D3K (140 checks) | every D3 record type (cfg, rate, clks, fmti, fmto, ptof, name) cut by `rst_n` with the device carried: on the ERASE's grant, at the WRITE's grant, after the header, one byte short, and at a byte drawn from seed `0xD3C0FFEE`. The restore never fails; a cut before the ERASE completed keeps A; erased or torn keeps the image's value (blank, or the crc's refusal); the saved binding is restored and probes PASSIVE (PRB_W_AVAIL); a later SET persists | `frame_crc_ignored` (one byte short, ptof and name) |
| desc_store G1/U1 | region 0xA: the name count from a loaded image, 0 from an unloaded one | manual: region 0xA answers `configurations_count`; region 0xA ungated (`tb/desc_store/README.md`) |

**Existing checks moved by the 32 name records** (the bench keeps the top's
`DESC_NAME_ENTRIES_P` default 32):
- the record-count literals of D3R1, D3R2, D3R6, D3C3 and D3C4 now derive from
  `D3_RECORDS = 27 + 32` (`d3_phases.hpp:379`);
- D3R13's pass-1 arm spaces its grants from the record count so the bound still falls
  in pass 1;
- D3R15's steered READ count adds the 32 erased headers of pass 0;
- the wrap's dirty tap widens to 59 bits, and a name-RAM lane tap is added.

The writer's new activity after a SET_NAME (a debounce later, ACQUIRE holding dispatch
while a program runs) and its longer boot walk moved three timing-sensitive sections:
- S0 now waits (bounded) for `restore_done_o` after the link rise.
- HZ9 and ST1 let the name saves drain before their timed arms.
- ST restores the churn's original phase of the millisecond tick (finding F1, section 6).

### Item 5: the parent-visible list

Section 3.

### R1 (ruling item 1): the D3 contract amendment, the maps the integrator's

The ruling (#83 comment 5967611704): "the integrator restores the maps from
`0x60`/`0x70` and resets them on a roll-back, and the processor's roll-back strobe no
longer covers them. No RTL." Commit `b88240a`, documents only. Clauses: Milan v1.2
§5.3.9.1 and §5.3.10.1 (each list "shall be saved in a non-volatile memory and restored
after a power cycle"), §5.6.1 (restore before advertising); parent D3 §8.4 and §8.6.

- `docs/architecture/07_memory_maps.md`:
  - :554, §5.1 **Who persists what**: the processor's two producers persist every
    persisted group but the maps. The maps are the integrator's (#83 acceptance 1's
    "07 5.1 explicitly assigns"), with its three obligations:
    - **save**: `0x60`/`0x70` + port from the phase-5 commit beat, under its own
      pending, never `d3_unflushed_o`;
    - **restore**: after `restore_done_o` and before it requests the enable, judged
      against the formats the D3 walk restored (`aecp_fmt_in_o`/`aecp_fmt_out_o` and
      their valid bits). The walk judges formats by the integrator's judge alone, so
      parent D3 §8.4's coupling is the integrator's. A map command that arrives early
      may be held on `amap_wait_i`/`amap_edit_wait_i` (before phase 5), within the
      AECP watchdog;
    - **roll-back**: on `restore_rb_o` every port keeps or regains its reset set. The
      D3 roll-back resets the two AECP stores only.
  - :451 and :461, §3.4: the map row and the paragraph after it;
  - :624-625, §5.2 inventory: writer "the integrator (§5.1); the processor never writes
    or reads it";
  - :703 and :835, §5.3: the runtime paragraph and the roll-back paragraph.
- `docs/architecture/02_interfaces.md:605`, §8.1: the maps paragraph.
- `docs/architecture/06_aecp_engine.md:181` (writer faces: "No map face"; the
  roll-back never touches the integrator's map plane) and `:545` (§6.5).
- `docs/guides/integrator.md`:
  - :435, the marks row: group 6's records are yours;
  - :470, bring-up step 3: your map plane is not in the D3 roll-back;
  - :518, new bring-up step 4: restore the channel maps yourself;
  - :529, step 6: the enable after step 4.
- `docs/00_MILAN_COMPLIANCE_REVIEW.md`: GAP-08 (:219), GAP-09 (:253), REQ-AEM-021
  (:423) and REQ-PER-001 (:470) now say the maps are the integrator's (#83 acceptance
  4). None of them points at an open processor item.
- `docs/architecture/09_verification.md:217`: the map stage's controls are the
  integrator's.

No test changes with R1: the processor's behaviour is unchanged. Gates: `make check`
(links, matrix) and the parent's `docs_check` with the successor patch (section 4.3).

### R2 (ruling item 2): #83's seeded-random reset cuts as a standing campaign

The ruling: "at least 32 seeds per record type, with the seed printed on any failure,
and keep the four fixed cuts. A mutant must fail it." Commit `53e1474`. Clauses: #83
acceptance 3; 09 §3 NVM ("cut at randomized commit points"); Milan v1.2 §5.5.3.5.2
(PRB_W_AVAIL), §5.5.3.5.6 (BIND_RX rebinds and saves); F07.8 framing.

- **Change.** Section D3KR, `tb/pp_top/d3_phases.hpp:3561` (`D3CutCampaignPhase`). It
  runs with `--cuts-only` (`make cuts`, `tb/pp_top/Makefile:131`) and in the default run
  (`tb/pp_top/sim_main.cpp:13711`). `--cut-seed S` reruns one seed (`:13712`). D3K's
  fixed cuts are unchanged.
- **Record types.** All eight both producers write: cfg, rate, clks, fmti, fmto, ptof,
  name (D3K's rows) and the binding manager's sink record `0x20`. The binding's change
  is a BIND_RX of sink 0 to another talker, which a sink in PRB_W_AVAIL saves.
- **Draw.** A calibration commit of each type (`:3673`) writes B whole and measures the
  clocks from the ERASE's grant to the WRITE's done: cfg 15, rate 17, clks 15, fmti 21,
  fmto 21, ptof 17, name 77, bind 33. For each of the 32 standing seeds
  (`0xD3C0FFEE + k * 0x9E3779B9`) and each type, `rst_n` falls with the device carried
  at a clock drawn by xorshift32 from the seed and the record id (`:3611`), anywhere from
  the ERASE's grant to two clocks past the done.
- **Oracle.** The bytes the device holds at the cut, never the RTL:
  - A whole comes back;
  - B whole comes back;
  - any other bytes (erased, a torn header, a torn payload) must frame no record (the
    oracle's own premise) and keep the default: the image's value or an unbound sink.
- **Checks per cut** (`:3694`): the premise; the restore never fails and holds the
  oracle's value; for a D3 type, sink 0's saved binding probes PASSIVE (PRB_W_AVAIL);
  a later change to B persists. Every check names its seed and its cut clock.
- **Size.** 1,000 checks in about 83 s.
- **Reach.** Per type, the cuts left A whole / erased / a torn header / a torn payload /
  B whole:

  | Type | A / erased / torn header / torn payload / B |
  |---|---|
  | cfg | 3 / 7 / 13 / 1 / 8 |
  | rate | 5 / 3 / 8 / 8 / 8 |
  | clks | 5 / 5 / 9 / 5 / 8 |
  | fmti | 5 / 2 / 11 / 8 / 6 |
  | fmto | 4 / 3 / 9 / 9 / 7 |
  | ptof | 3 / 4 / 12 / 4 / 9 |
  | name | 0 / 2 / 2 / 27 / 1 |
  | bind | 3 / 2 / 7 / 18 / 2 |

  The name's A-whole window is 2 of 77 clocks; D3K's fixed ERASE cut covers it.

| Control (`tb/pp_top/d3_mutants.py:598`, run `--cuts-only`) | Planted | Fails |
|---|---|---|
| `cut_binding_crc_ignored` | the binding manager's crc compare removed (`KL_acmp_nvm_shadow.sv:395`), so a torn binding record is restored | 20 checks, `D3KR bind seed ...` (every seed whose cut left a torn binding record) |
| `cut_frame_crc_ignored` | the D3 writer's frame crc compare removed for every group | 30 checks, `D3KR ptof seed ...` and `D3KR name seed ...`; a torn configuration, rate, clock-source or format record stays refused by its value rule |

The first run of `cut_frame_crc_ignored` named `D3KR rate seed` and SURVIVED on that
name alone: it failed 30 checks, none of them rate's. The named checks were corrected to
the offset's and the name's, and the re-run KILLED it. Both controls were then re-run in
the full campaign at the head (section 4.2).

### R3 (ruling item 3): #61 and #83

With the maps the integrator's, both issues' acceptance is met in full, so the PR closes
all six. Each acceptance line:

| Issue | Acceptance line | Met by |
|---|---|---|
| #61 | 1. a manager commits RATE, FMT_IN/OUT, PT_OFS, CLKSRC, MAPS_IN/OUT and NAMES records through `KL_pp_nvm_port`; `aecp_eff_nvm_mark` no longer `_nc_` | the D3 writer, manager 1 behind the arbiter: the scalars (#131) and the names (this lane). MAPS_IN/OUT are the integrator's (R1). The marks are top outputs (`aecp_nvm_stb_o`/`aecp_nvm_mark_o`). The trigger is the accepted changing write, not the mark and not the sticky dirty pulse, under the parent contract's §3.1 ("replaces mark-based acceptance", §15 item 1 RESOLVED) and DR2b |
| #61 | 2. boot restore before `entity_enable` writes the validated records into the rows with their valid flags and into the name table; a bad crc or version gives the default | D3R1 and D3R2 (frame and version refusals); D3N3 and D3N4; D3C5 and AD7 to AD9; D3R1 and D3C6 (the enable) |
| #61 | 3. a suite sets each group over AECP, cuts power after the debounce, restores, reads back byte-exact via GET_* and READ_DESCRIPTOR; every record type cut mid-commit | D3S1/D3R1 (GET of each group), D3N1/D3N3 (GET_NAME and READ_DESCRIPTOR), AD5; D3K (fixed cuts), D3KR (seeded) |
| #61 | 4. GAP-08/GAP-09 and 06 updated | #131 and this lane (R1) |
| #83 | 1. a manager commits RATE, FMT_IN/OUT, PT_OFS, CLKSRC, CFG_IDX and NAMES and replays them before the entity may be enabled (or 07 5.1 assigns a group to the integrator) | as #61's line 1, CFG_IDX included; 07 §5.1 assigns the maps |
| #83 | 2. a suite sets each persisted field over AECP, power-cycles and reads it back with GET_* while lock, registry and IDENTIFY read their defaults | D3R1 (every group, and the volatile exclusions), D3N3, AD5, D3V |
| #83 | 3. every record type cut at seeded-random commit points with a real `rst_n`; crc fallback to the per-record default; restored bindings in PRB_W_AVAIL | D3KR (all eight record types, 32 seeds each) beside D3K |
| #83 | 4. GAP-08/GAP-09 and the REQ-AEM-011/-021 Finding cells stop pointing at an open item | R1: the maps are the integrator's in GAP-08, GAP-09 and REQ-AEM-021; REQ-AEM-011 is the name stage |

## 3. Parent-visible list

1. **No top-level port, parameter or register added.** `KL_pp_shadow` needs no edit.
   The modules the parent instantiates by name (`KL_aecp_dyn_state`,
   `KL_acmp_nvm_shadow`, `KL_pp_nvm_mgr_arb`, `KL_pp_nvm_port`, in `nvm_cosim`) are
   unchanged. Internal ports are added on `KL_aecp_nvm_writer` only (`sb_name_o`,
   `nchg_i`, `nchg_ord_i`, each documented). `KL_aecp_desc_store`'s region 0xA is an
   address, not a port.
2. **`DESC_NAME_ENTRIES_P` is now also the D3 writer's name-record count.** Its legal
   range narrows to 1 to 128 (the writer refuses more at elaboration). The parent's
   backend already refuses `N_NAME_P` past 128, and the parent builds 38 (1x1) and 99
   (8x8).
3. **On the device face.** A changed name is written as record `0x80` + ordinal (72
   framed bytes) through manager 1 a debounce after the accepted lane write.
   `d3_unflushed_o` covers it. At boot the D3 walk reads `2 × DESC_NAME_ENTRIES_P` more
   records, an erased one costing its header read, and writes saved names back after the
   image proof. The backend already backs `N_NAME_P = DESC_NAME_ENTRIES_P` name records
   (`KL_pp_shadow.sv:1007`).
4. **Pending.** The parent's `pend_i` still ORs the sticky live-name term
   (`aecp_live_wr_w | aecp_live_pend_r`), so after a name write it reads pending until
   reset, as today. Transferring names to `d3_unflushed_o` is the parent's adoption
   lane (D3 §10 stage 2, §18.3).
5. **`aecp_name_wr_o`.** It still pulses for every accepted live lane write. It does
   not pulse for the writer's restore of a saved name.
6. **Census, record space and capture: unchanged.** The 8x8 capture stays at its
   measured 13.23 ms (50 MHz) against 24.5 ms.
7. **DR3a.** In the bench, a blank restore's D3 terminal moves from 1,286 to 2,182
   clocks after the release, about 28 clocks per erased name record over both passes.
   The longest per-wait stays 405 (DRAM 31) and 853 (DRAM 143) clocks. The parent's
   lane 3 re-measures on its product (§18.3).
8. **DR4 (1x1 TDM8 names-stage ceiling 750 LUT-eq / 400 FF, processor and parent
   glue together).** The processor side is +705 LUT-eq and +92 FF (section 5), which
   leaves 45 LUT-eq and 308 FF for the parent's glue.
9. **Processor documents the parent reads:**
   - 07 §3.3 region map, §3.4, §5.2 inventory row (`0x80..0xFF`: D3 writer), §5.3
     (F07.9, value rules, roll-back);
   - 02 §8.1 and the following paragraph;
   - 06 writer faces and SET_NAME;
   - the integrator guide's `DESC_NAME_ENTRIES_P`, `d3_unflushed_o`,
     `aecp_name_wr_o` and marks rows;
   - 00 GAP-08, GAP-09, REQ-AEM-011, REQ-AEM-013, REQ-NOT-005, REQ-PER-001/2/3;
   - 09 §8.1, §8.2.

   The parent's own D3 page (§1's table, its status line "User names ... not
   implemented") becomes stale for the processor side. The manager assigned that
   update to the next pin adoption (ruling item 4), so this lane's patch leaves the
   names alone.
10. **The maps are the integrator's** (the ruling on STOP item M1; R1).
    - **Processor documents the parent reads.** 07 §3.4, §5.1 ("Who persists what"),
      §5.2 (the `0x60`..`0x7F` rows), §5.3; 02 §8.1; 06 (writer faces, §6.5); the
      integrator guide's marks row and bring-up steps 3, 4 and 6; 00 GAP-08, GAP-09,
      REQ-AEM-021, REQ-PER-001.
    - **What the parent owns.**
      - It writes `0x60`/`0x70` + port from its phase-5 commit beat, under its own
        pending, at #501's capacity.
      - It restores them after `restore_done_o` and before it requests the enable,
        judged against `aecp_fmt_in_o`/`aecp_fmt_out_o` and their valid bits.
      - It keeps or puts back each port's reset set on `restore_rb_o`.
      - It may hold an early map command on `amap_wait_i`/`amap_edit_wait_i` (before
        phase 5) within the AECP watchdog.
      - Its restore and roll-back are milan-fpga #637.
    - **No port, parameter, register, census or capture change.** `KL_pp_shadow` is
      unchanged.
    - **The parent's D3 page quotes the old rule**, so `parent-adoption-p2-cdf49d1a.patch`
      has a successor: **`parent-adoption-p2-p1-1269cdaf.patch`** (24,711 bytes, sha256
      `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84`). It is cut on
      trusted `1269cdaf` with c8 applied, and replaces p2: apply c8, then it. It carries
      p2's hunks unchanged plus the amendment in
      `docs/design/SAVED_STATE_MATERIALIZATION.md` (28 lines added, 13 removed against
      p2):
      - the status block;
      - §3 item 9;
      - §5.1's roll-back seam row: the map plane is no longer on `rb_rst`;
      - §5.2: the map plane resets on `restore_rb_o`;
      - §8.4: the walk does step 1, the parent steps 2 to 4;
      - §8.6: `rb_rst` resets the two stores;
      - §10's stage-3 bullet and row: the parent's own writer; tickets T4, #501, #637;
      - §15 item 2, AMENDED: the map writer is the parent's;
      - §18.4's capacity and roll-back lines.
    - The parent's `MILAN_COMPLIANCE_MATRIX.md` row ("no record writer (#70 lane 4)")
      quotes no processor rule and is left alone.
11. **Finding F1.** Section 6; now processor #148 (ruling item 4).
12. **D3KR** is bench-only (`tb/pp_top`). It adds no file the parent consumes, and the
    processor's default `tb/pp_top` run is about 83 s longer.

## 4. Gates

Final head: **`53e1474b633ee31de2ce1c1436b6b61920c9c8b2`** (`p1-persistence`, not pushed).
The gates of the stop head `4b02d4f` are kept where the ruling's items did not move them.

### 4.1 Processor suites and entry points (pinned Verilator 5.050)

The baseline ran in a `git archive` export of `ddb3119d`; the heads ran in this tree.

| Command | Baseline `ddb3119d` | Stop head `4b02d4f` | Final head `53e1474` |
|---|---|---|---|
| `./scripts/run_suites.sh` | rc 0: 33 of 33 suites, 1,020,238 checks | rc 0: 33 of 33, 1,020,434 checks | **rc 0: 33 of 33 suites, 1,021,434 checks**, 0 failing |
| `./scripts/lint_hdl.sh` | | rc 0, 41 modules | **rc 0**, 41 modules LINT OK |
| `make check` | | rc 0, 1,062 links | **rc 0**: 41 mermaid + 18 wavedrom blocks, 1,069 links, 115 REQ rows and 17 GAPs, 94 matrix rows (0 untested), parameters 28 = 28 = 28 |
| `python3 scripts/gen_matrix.py --check` | | rc 0 | **rc 0** |
| `tb/pp_top` (`make`, five builds) | 9,168 | 9,362 | **10,362** |
| of which `--d3-only` | 150 | 319 (D3C5, D3C6, D3N, D3K) | 319 |
| of which `--adp-only` | 55 | 67 (AD8, AD9) | 67 |
| of which `--volatile-only` | (none) | 11 (D3V) | 11 |
| of which `--cuts-only` | (none) | (none) | **1,000 (D3KR)**, about 83 s |
| `tb/desc_store` | 584 | 586 (G1, U1) | 586 |

Correction: the stop-head records and the STOP comment said "34 of 34 suites". `tb/`
holds 33 suites with a Makefile, and both suite logs (baseline and stop head) list 33.
The checks totals were right.

### 4.2 Mutation campaigns (pinned Verilator 5.050, each control in its own extract)

| Driver | Head | Scope | Result |
|---|---|---|---|
| `tb/pp_top/d3_mutants.py --jobs 3` | `53e1474` | all 110 controls: the 87 main had, the 21 of the stop head, and R2's two (`cut_binding_crc_ignored`, `cut_frame_crc_ignored`); 6 goldens (`--d3-only`, `--adp-only`, `--volatile-only`, `--cuts-only`, `tb/acmp_nvm`, `tb/rx_validator`) | **110 of 110 KILLED** by their named checks, 6 goldens PASS, rc 0; 55 min at `--jobs 3`. Every failing-check count equals the recorded one: the 98 rows of `tb/pp_top/README.md`, the 11 of `tb/acmp_nvm/README.md` and the 1 of `tb/rx_validator/README.md`. So no record moved, and R2's two failed 20 and 30 |
| `tb/pp_top/d3_mutants.py --only cut_binding_crc_ignored cut_frame_crc_ignored` | working tree of `53e1474`, before the commit | R2's two, first run | golden PASS; `cut_binding_crc_ignored` KILLED (20); `cut_frame_crc_ignored` SURVIVED on its first named check, `D3KR rate seed`, which no torn rate fails (a torn rate is refused by its rule), though it failed 30 others. Renamed to `D3KR ptof seed`/`D3KR name seed` and re-run: KILLED (30) |
| `tb/pp_top/name_wr_mutant.py` | `4b02d4f` | NW, the export driven by command decode (re-anchored on the gated export) | decode KILLED; golden and restored PASS |
| `tb/pp_top/aecp_mutants.py --only <27 hazards arms> --jobs 3` | `4b02d4f` | HZ, because HZ9 now drains its name saves | control PASS, **27 of 27 KILLED**; 3 rows' counts moved and are recorded |
| `tb/pp_top/notify_mutants.py --only counter_limit_500ms fan_out_skips_row_0` | `4b02d4f` | ST, because ST now drains and keeps its tick phase | golden PASS, **2 of 2 KILLED**, counts unchanged (12, 9) |
| `tb/adp_engine/mutants.py --jobs 3` | `4b02d4f` | the 30 arms, AD among them | both controls PASS, **30 of 30 KILLED**; 4 pp_top rows' counts moved and are recorded |
| `tb/desc_store` region 0xA, by hand in a scratch copy | `4b02d4f` | the count answers `configurations_count`; ungated | 1 of 586 each, recorded |

The ruling's items changed no RTL, and R2 adds a section that only `--cuts-only` and the
default run reach. So the campaigns re-run at `4b02d4f` (other than D3's) were not run
again: none of their runs reaches D3KR. Still not re-run, because nothing they plant or
grade changed:
- the other arms of `aecp_mutants.py` (DL, the `d3` target), `notify_mutants.py` (NP,
  RN, ID), `gsi_mutants.py`, `acmp_mutants.py` and `aecp_dispatch_mutants.py`. Every
  one of their plants still applies exactly once (checked with `git apply --check` and
  each driver's own count rule);
- `tb/nvm_port` and `tb/acmp_nvm`'s own campaigns: their modules are unchanged.

### 4.3 Parent consumer set (16) at milan-fpga dev `1269cdaf`

The scratch parent, under `$VALIDATION_STORAGE`:
- a `git archive` of the trusted checkout, 983 index entries plus the processor gitlink,
  984 in all. Its blobs equal the trusted `1269cdaf` tree's, checked with `ls-tree`;
- `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e` and `external`
  `efeb541a`. The trusted checkout carries no submodule contents, so each was fetched
  from its `.gitmodules` URL at exactly its gitlink sha;
- `protocol-processor` a read-only scratch clone of this tree, sharing its objects, at
  `53e1474`, its gitlink set to that head;
- all four submodules registered and absorbed (`git submodule status` clean, no `-`);
- `parent-adoption-c8-cdf49d1a.patch` then **`parent-adoption-p2-p1-1269cdaf.patch`**
  (p2's successor, section 3 item 10) applied with `git apply` (`--check` clean) and
  committed, porcelain empty.

| # | Command | rc | Result at `53e1474` (c8, then the successor) |
|---:|---|---:|---|
| 1, 2 | `scripts/check_cpp_idiom.py`, `scripts/check_py_idiom.py` | 0, 0 | every ratchet within budget (multi-declarator 0 <= 0, over-long line 0 <= 0, too many parameters 7 <= 7, ...); D3KR's code included |
| 3, 4 | `scripts/check_rtl_source_lists.py`, `scripts/pp_srcs.py --check --selftest` | 0, 0 | 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `scripts/check_port_contracts.py` | 0 | processor 1,760 ports, undocumented 111 <= 111 (unchanged: no RTL since `4b02d4f`) |
| 6, 7 | `scripts/measure_naming.py --check`, `scripts/measure_test_evidence.py --check` | 0, 0 | 96 candidates, all recorded; 72 <= 77, **10 <= 10 unseeded draw sites** (D3KR's draws are seeded), 0 <= 0, 3 <= 3 |
| 8, 9 | `scripts/docs_check.py`, `scripts/xvlog_gate.py --check` | 0, 0 | **0 findings over 185 md + 956 files with the amended D3 page**; 4 findings == ratchet |
| 10, 11 | `sw/builder/test_builder.py`, `scripts/lint_rtl.py --check` | 0, 0 | "ALL GATES PASS EXCEPT 1 NOT RUN": the builder's gate 11, which needs the local mf48 build tree, as at `4b02d4f`; the log is the stop head's, line for line, but for temporary paths. `lint_rtl` 90 <= 90 (run twice: in the group, and alone) |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS; 4 render mutants caught; the gmstep controls 6 of 6 |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65 + 152 checks, 0 failures; 5 of 5 leg-defect arms caught |

At `4b02d4f`, with c8 and p2, the same 16 passed (rc 0 each). The first run, at
`a1f5cd5`, failed only the two idiom ratchets on the lane's own lines, which `084be15`
fixed.

## 5. Out-of-context cost

The parent's DR4 instrument: sv2v, then Yosys 0.66 `synth_xilinx -flatten -family xc7`,
with distributed RAM priced as LUTs (RAM32M = 4). Per module, `ddb3119d` against the head,
at the parent's shapes (1x1: 2 in, 2 out, 38 names; 8x8: 9 in, 9 out, 99 names). The
engine's glue (one select, one AND) is below the instrument's noise.

| Module, shape | Baseline LUT / FF | Head LUT (+ LUTRAM) / FF | Delta |
|---|---|---|---|
| `KL_aecp_nvm_writer` 1x1 | 928 / 505 | 1,541 (+11 RAM32M) / 597 | +613 LUT +44 LUT-eq LUTRAM, +92 FF |
| `KL_aecp_desc_store` 1x1 (38 names) | 1,326 / 774 | 1,374 / 774 | +48 LUT |
| **processor, 1x1 (shipping)** | | | **+705 LUT-eq, +92 FF** (DR4 ceiling 750 / 400) |
| `KL_aecp_nvm_writer` 8x8 (diagnostic) | 1,220 / 550 | 2,740 (+11 RAM32M) / 767 | +1,520 LUT +44, +217 FF |

No block RAM or DSP added. These are synthesis counts, not placed.

## 6. What remains

- **The parent's adoption** of the lane, in its own lanes:
  - the name stage: pending transfer, its D3 page (the next pin adoption, ruling item
    4), DR3a re-measurement, the DR4 placed comparison, and a cold cycle of every
    writable name on silicon;
  - the map amendment: `parent-adoption-p2-p1-1269cdaf.patch` replaces p2, and the
    parent's map writer, restore and roll-back are milan-fpga #637.
- **Finding F1** is processor #148 (ruling item 4): `KL_aecp_notify` stamps a
  GET_COUNTERS round's one-second limit at selection, not at departure. It is recorded
  in `tb/pp_top/README.md` (limits).
- **Unchanged from main**: issue #15's reusable-port criterion; `tb/nvm_port`'s three
  uncovered `*REQ` arms.

## Round 1b: merge of `main` `f4167536` (merge only)

Assignment: #83 comment 5968352676. Head: **`c066dd83a2004f9b3640a933860c4d9e677d017e`**
(`p1-persistence`, not pushed). Status: **STOP** on item 3 (gate 16, section R1b.4),
posted on #83 as "[A515] STOP" (comment 5969239148).

| Commit | Item |
|---|---|
| `9ca7468` | 1: `--no-ff` merge of `main` `f4167536` (parents `53e1474`, `f4167536`) |
| `c066dd8` | 2: the notify record at the merge (one count moved with round 1) and the default build's section order |

### R1b.1 Item 1: the merge

- **Conflicts.** Two textual ones, both resolved as the union of the two sides:
  - the `.PHONY` list of `tb/pp_top/Makefile` (`volatile cuts` beside `counters
    ctr-mutants`);
  - `one_section` in `tb/pp_top/sim_main.cpp` (`ctr_only` beside `volatile_only`,
    `cuts_only` and `one_seed`).

  Every other shared file merged without a conflict: `protocol_processor_top.sv`
  (C7 removes the dead GM-tick wire; the lane's edits are comments), `notify_phases.hpp`
  (C7's `counter_body(io, ...)` beside the lane's ST drain), the two READMEs, 00, 02,
  06, 07, 09 and the integrator guide. Main's `counter_body` and `ctr_mask` became
  members; no lane line calls them.
- **Contracts kept.** C7's: the counters are the integrator's (02 §4.6, 06 §6.6, 07
  F07.10, integrator guide §7.1), and 09 §8.6 (the NVM port) and §8.7 (the counters
  face) as `main` has them. The lane's: the D3 amendment (07 §5.1, the maps the
  integrator's; 02 §8.1; 06; integrator guide bring-up step 4; 00 GAP-08, GAP-09,
  REQ-AEM-021, REQ-PER-001) and 09 §8.2.
- **RTL.** The lane's HDL delta on `f4167536` is line-identical to its delta on
  `ddb3119d` (compared as diffs of the two diffs). The top's edits are still comments.
  No port, parameter or register: the parent's port gate counts 1,759 processor ports
  (1,760 in round 1: C7 removed `KL_adp_engine`'s internal `gm_changed_tick_o`),
  undocumented 111 <= 111.
- **ROMs, regenerated.** Each was generated at `ddb3119d`, `53e1474`, `f4167536` and the
  merge, and compared byte for byte:
  - `ucode.hex` (2,048 words, `gen_ucode.py`);
  - `ltn_rom.hex` (129, `gen_ltn_rom.py`);
  - the descriptor images and maps of `milan_min.json` and `example_milan_8.json`
    (`gen_desc_image.py`).

  All four trees are byte-identical: neither side touched a generator.
- **ROM-word overlaps beyond text.** Every ROM word either side's records cite (the
  M14 to M24 rows, the `ctr_mutations` beat and locate arms) is the same word at the
  merge. All 224 tracked mutation patches apply (`git apply --check`): ctr 17, aecp 42,
  aecp_dispatch 37, adp_engine 28, maap 27, srp_top 73. Every substitution driver's
  plant occurs exactly as its rule requires: d3 119 edits, notify 43, acmp 19, gsi 20.
- **Builds.** `tb/pp_top` builds the bench five times everywhere it is described
  (Makefile, README, `sim_main.cpp`, 00, 06, 08, 09): 1 default, 2 the DV fixture, 3 ID
  identify, 4 AX line, 5 TB timebase. The README's build table said the default build
  runs "RN last", stale on `main` since C7 added K9 to K17 after RN. `c066dd8` lists
  D3, D3V, D3KR, and C7's K9 to K17 last.

### R1b.2 Item 2: the targeted re-measure at the merge

Pinned Verilator 5.050, merge `9ca7468`. `c066dd8` changes only `tb/pp_top/README.md`.

| Command | Result |
|---|---|
| `./scripts/run_suites.sh` | **rc 0: 33 of 33 suites, 1,021,423 checks**, 0 failing. Against round 1's 1,021,434: `adp_engine` 1,367 → 1,328 (C7 removed the GM-tick checks), `pp_top` 10,362 → 10,390 (C7's K9 to K17); every other suite as in round 1 |
| `./scripts/lint_hdl.sh` | rc 0, 41 modules LINT OK |
| `make check`, `scripts/gen_matrix.py --check` | rc 0 at the merge and at `c066dd8`: 1,114 links, 115 REQ rows, 17 GAPs, 94 matrix rows (0 untested), parameters 28 = 28 = 28 |
| `make -C tb/pp_top` (five builds) | rc 0, **10,390** = default 9,918 + fixture 20 + identify 178 + line 218 + timebase 56 |

`tb/pp_top` per section: `main` `f4167536` alone runs 9,196 (rc 0, in a `git archive`
export). Every section of the merge carries `main`'s count or the lane's:
- `main`'s: GI 5,568, NW 85, ACMP 43, AX 218, DL 64, ID0 3, NP 47, RN 4, K-AVB (K9 to
  K17) 28; the fixture, identify, line and timebase builds;
- the lane's: D3 150 → 319, AD 55 → 67, HZ 176 → 177, ST 18 → 19, D3V 11, D3KR 1,000.

10,390 = 9,196 + 1,194 (the lane's round-1 growth) = 10,362 + 28. No section lost.

**Campaigns**, each control in its own extract, each driver at the merge:

| Driver | Result | Every count against its README record | Time |
|---|---|---|---|
| `tb/pp_top/d3_mutants.py --jobs 3` | 6 goldens PASS, **110 of 110 KILLED** | all 110 (109 in `tb/pp_top/README.md`, `validator_admits_held_aecp` in `tb/rx_validator/README.md` M4: 4) | 64 min |
| `tb/pp_top/notify_mutants.py --jobs 2` | 5 goldens PASS, **40 of 40 KILLED** | 39; `ident_burst_from_t0` fails 21, recorded 20 (below) | 10 min |
| `tb/pp_top/ctr_mutants.py --jobs 2` | control PASS, **17 of 17 KILLED** | all 17 | 4 min |
| `tb/pp_top/aecp_mutants.py --jobs 2` | 5 controls PASS, **55 of 55 KILLED** (DL, HZ, the MVU and µCPU arms) | all 55 (six on "the same N" rows) | 13 min |
| `tb/pp_top/aecp_dispatch_mutants.py --jobs 2` | 4 controls PASS, **37 of 37 KILLED** | all 37 | 11 min |
| `tb/pp_top/acmp_mutants.py --jobs 2` | 3 goldens PASS, **19 of 19 KILLED** | all 19 (`tb/pp_top`, `tb/acmp_listener`, `tb/rx_validator` M6) | 4 min |
| `tb/pp_top/gsi_mutants.py --jobs 2` | golden and restored PASS, **20 of 20** fail their named checks | named checks, as recorded | 11 min |
| `tb/pp_top/name_wr_mutant.py` | decode KILLED; golden and restored PASS | as recorded | 1 min |
| `tb/adp_engine/mutants.py --jobs 2` | 2 controls PASS, **30 of 30 KILLED** (its `pp_top adp-config` arms) | all 30 (two at their lane-P1 counts, as round 1 recorded) | 4 min |
| `tb/maap/mutants.py --jobs 2` | 3 controls PASS, **27 of 27 KILLED** (29 arm-suite pairs, `pp_top maap-internal` among them) | all 29 | 2 min |

No arm lost. Every driver ran its whole declared list. The arm lists at the merge are
`main`'s with the lane's added: d3 87 + 23, ctr 17, the rest unchanged on both sides.

**The one count that moved: `ident_burst_from_t0` 20 → 21** (identify build, ID6d
added). Run alone with `--only` at three trees:

| Tree | Failing checks |
|---|---|
| `main` `f4167536` | 20, as recorded |
| the lane's round-1 head `53e1474` | 21 |
| the merge | 21 |

So the move came with round 1, not the merge. Round 1 had not re-run the ID arms,
reasoning that nothing they plant or grade changed. That was wrong for this
timing-sensitive arm. Cause: ID6 holds a burst until the D3 terminal, and the name
stage's longer walk moves the burst's phase. Under the mutant, frame 3 (still due at
t0 + 300 ms) then leaves 14,979 clocks after frame 2, which ID6d refuses. `c066dd8`
records 21, with the reason and `main`'s 20.

**Out-of-context cost at 1x1 against `main` `f4167536`.** Same instrument as round 1:
sv2v, then Yosys 0.66 `synth_xilinx -flatten -family xc7`, LUT RAM priced as LUTs.
`KL_aecp_nvm_writer`, `KL_aecp_desc_store` and `KL_aecp_engine` are byte-identical at
`f4167536` and `ddb3119d`, and at the merge and `53e1474`.

| Module | `f4167536` LUT / FF | Merge LUT (+ LUTRAM) / FF | Delta |
|---|---|---|---|
| writer, 38 names (round 1's 1x1) | 928 / 505 | 1,541 (+11 RAM32M) / 597 | +613 +44, +92 FF |
| store, 38 names | 1,326 / 774 | 1,374 / 774 | +48 |
| **processor, 38 names** | | | **+705 LUT-eq, +92 FF**: round 1's figures exactly |
| writer, 39 names (the 1x1 shape at dev `bbf704ec`, #629) | 928 / 505 | 1,589 (+11 RAM32M) / 599 | +661 +44, +94 FF |
| store, 39 names | 1,362 / 774 | 1,340 / 774 | −22 (synthesis noise) |
| **processor, 39 names** | | | **+683 LUT-eq, +94 FF** |

Both are within the DR4 names-stage ceiling (750 LUT-eq / 400 FF). No block RAM or DSP
added (the store's three are on both sides).

### R1b.3 Item 3: the parent consumer set at milan-fpga dev `bbf704ec`

- **Dev.** Fetched from the parent's origin into a scratch clone of the trusted
  checkout. `dev` is `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352` (Merge PR #634), 30
  commits past `1269cdaf`. The submodule pins are unchanged: `external` `efeb541a`,
  `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, processor
  `631eeb34`.
- **c8.** `parent-adoption-c8-cdf49d1a.patch` does not apply at `bbf704ec`: `git apply
  --check` fails at `avdecc/aem_assemble.py:600`. This is **not** because #634 carries
  the hunk: `LINT_WAIVERS` and `lint_waivers` appear nowhere at `bbf704ec`. #629 D1
  (`0b0742981`, inside #634) added `CLKSRC_TABLE=clock_source_table(...)` to the
  hunk's leading context. The re-based patch is **`parent-adoption-c8-bbf704ec.patch`**
  (8,546 bytes, sha256
  `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c`). It keeps all
  11 hunks (7 files), every `+`/`-` line identical to the `cdf49d1a` original; only
  that hunk's first context line and the line offsets moved. **No hunk dropped.**
  (Round 1b said "13 hunks"; corrected in round 2, R2.1.)
- **The p2 successor.** `parent-adoption-p2-p1-1269cdaf.patch` applies at `bbf704ec`
  over the re-based c8 unchanged, with no offset: `SAVED_STATE_MATERIALIZATION.md` is
  untouched on dev since `1269cdaf`. So there is no `-bbf704ec` copy of it.
- **C7 needs no parent patch at `bbf704ec`, confirmed:**
  - no parent file names `gm_changed_tick` or `adp_gm_tick`;
  - the port gate counts the one internal port C7 removed;
  - gates 1 to 15 pass with C7 in the processor;
  - gate 16 passes with `main` `f4167536` (C7 alone) as the processor (R1b.4).
- **Scratch parent** (as round 1):
  - a `git archive` of `bbf704ec`, 998 index entries with the 4 gitlinks; its `ls-tree`
    equals `bbf704ec`'s but for the processor gitlink;
  - the three submodules at their pins;
  - the processor a scratch clone of this tree, at `9ca7468` for the run, then
    `c066dd8`;
  - all four absorbed, `git submodule status` clean;
  - the re-based c8, then the p2 successor, applied with `git apply` and committed;
    porcelain empty.

| # | Command | rc | Result (dev `bbf704ec`, c8-bbf704ec then the p2 successor) |
|---:|---|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | every ratchet within budget (too many parameters 7 <= 7, over-long line 0 <= 0, ...) |
| 3, 4 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 | 108 files in the `milan_datapath` closure (107 at `1269cdaf`: dev's own AAF meter), 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 5 | `check_port_contracts.py` | 0 | 3,824 first-party ports, processor 1,759; undocumented 111 <= 111 |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | 95 candidates, all recorded; 72 <= 77, 10 <= 10 unseeded draw sites, 0 <= 0, 3 <= 3 |
| 8, 9 | `docs_check.py`, `xvlog_gate.py --check` | 0, 0 | 0 findings over 186 md + 970 files (the amended D3 page included); 4 findings == ratchet |
| 10, 11 | `sw/builder/test_builder.py`, `lint_rtl.py --check` | 0, 0 | "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11 needs the local mf48 build tree, as in round 1); `lint_rtl` 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS; 4 render mutants caught; the gmstep controls 6 of 6 |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | **2** | two-stream leg 65 checks PASS; shipping leg **155 checks, 2 FAIL** (T30 INTERNAL LAW); make stops there, so the 5 leg-defect arms did not run |

Gates 1 to 16 ran with the processor at `9ca7468`. Gates 1 to 11 were re-run at `c066dd8` (the README-only follow-up): all rc 0, with the same results. Gates 12 to 16 elaborate the RTL and the benches, which `c066dd8` does not touch.

**The parent's census at `bbf704ec`** (its own change, #629's clock-source names;
`d81198c20`):
- 1x1: 54 records, 3,290 B (53 and 3,218 at `1269cdaf`);
- 8x8: 164 records, 13,210 B (156 and 12,634); the 8x8 capture maximum is 13.86484 ms
  against 24.5 ms (13.23).

The name entries (`AEM_NAME_ENTRIES_C`, the parent's `DESC_NAME_ENTRIES_P`) are 39 at
1x1 and 107 at 8x8 (38 and 99 at `1269cdaf`). So the D3 writer's records at the
parent's shapes are 9 → 48 and 30 → 137, all within the writer's 128-name bound. The
census and capture are the parent's own measurements; the lane changes neither.

### R1b.4 STOP: parent gate 16, `tdm8_render` T30 INTERNAL LAW

The two failing checks are new on dev with #634 (#629 A2-a, "align the grid at
INTERNAL"). Round 1's gate 16 at `1269cdaf` had 152 shipping-leg checks; dev has 155.
- `T30 INTERNAL LAW: the fill at accept is the 8-event setpoint for every PDU`: got
  227 of 292.
- `T30 INTERNAL LAW: every PDU's first event is inside the law band`: got 285 of 292.
  The first-event delay is 18,396..18,821 cycles, 8.830..9.034 media ticks, against
  the law (8, 9] ticks plus 64 cycles of slack.

**Attribution.** `make -C tb/verilator/milan_dp_render tdm8render` in scratch copies of
the same parent, only the processor checkout differing:

| Processor | Result | First-event delay (ticks) |
|---|---|---|
| `631eeb34` (dev's pin; dev exactly, no patches) | PASS, 155 | 8.385..8.589 |
| `ddb3119d` (the lane's base) | PASS | 8.385..8.589 |
| `f4167536` (`main`, C7) | PASS | 8.385..8.589 |
| `53e1474` (round 1's head) | FAIL, 2 (227, 285) | 8.830..9.034 |
| `9ca7468` (the merge; gate 16) | FAIL, 2 (227, 285) | 8.830..9.034 |

So it comes with the lane's round 1, not with the merge or C7. The simulation is
deterministic: the round-1 head and the merge print identical numbers.

**Mechanism: the feed's phase against the INTERNAL grid.** In a scratch copy of the
bench, only T30's feed start was moved (`phase_crf`'s `next_pdu_at = axis_cycle + 64`):

| Processor | Feed start moved by | Result |
|---|---|---|
| `631eeb34` | +1,156 cycles (the lane's +927-cycle delay shift, mod one 2,083.3-cycle tick) | FAIL, the same two checks (227, 284), 8.830..9.035 |
| `f4167536` | +1,156 | FAIL, the same (227, 284) |
| `53e1474` | +927 | PASS, 155; 8.385..8.589, dev's own numbers |

So T30's INTERNAL law holds at some phases of the feed against the free-running
INTERNAL grid and not at others. The window is graded while the aligner still walks:
−106.8 ppm in every run, passing or failing, against T31's 0.0 later. The processor's
boot length sets that phase. The name stage reads `2 × DESC_NAME_ENTRIES_P` more
records at boot (78 at this 1x1 shape; round 1's DR3a: about 28 clocks each), which
moves it. The processor's behaviour on the wire is otherwise unchanged; the bench
depends on its timing.

**Why STOP.** None of the round-1b STOP conditions applies: no port, parameter,
register, census, capture or parent-contract change. But item 3's 16 gates do not all
pass, and the lane cannot make them:
- the bench is the parent's;
- in a merge-only round the processor has no change to make;
- a shorter walk would only move the phase again.

What the manager can decide:
- (a) The parent makes T30's INTERNAL law independent of the feed's phase, for example
  by grading it after the aligner settles. The lane then re-runs gate 16 at this head.
- (b) Accept gate 16's two checks as a parent finding against #634 and take the PR to
  review with it recorded.

Ruled (b) on #83 (5969246536): the two checks are recorded against milan-fpga #643,
which lands before the second pin adoption; the PR does not wait for it.

### R1b.5 Parent-visible list, round 1b additions

1. The merge adds no port, parameter or register, and no census, capture or
   saved-state contract change. C7 removed one internal ADP port (port gate: 1,759).
2. At dev `bbf704ec` the parent builds 39 (1x1) and 107 (8x8) name entries, so the D3
   writer writes and restores up to 39 and 107 name records (the bound is 128). The
   restore reads `2 × 39` more headers at 1x1.
3. **`parent-adoption-c8-bbf704ec.patch`** replaces `parent-adoption-c8-cdf49d1a.patch`
   at `bbf704ec` (no hunk dropped). Apply it, then `parent-adoption-p2-p1-1269cdaf.patch`
   unchanged.
4. Gate 16's T30 INTERNAL law depends on the feed's phase, which the processor's boot
   length moves (R1b.4).
5. DR4 at the 39-name 1x1 shape: +683 LUT-eq, +94 FF.

### R1b.6 Out-of-context cost

R1b.2: unchanged by the merge (+705 LUT-eq, +92 FF at 38 names); +683 LUT-eq, +94 FF at
the 39 names of dev `bbf704ec`.

## Round 2: the reviews' three MINOR documentation findings (docs only)

Assignment: #83 comment 5969765075, answering R444-1 (PR #150 comment 5969549669) and
R445-1 (PR #150 comment 5969760336), both NEGATIVE at `c066dd83` on the same three MINOR
documentation findings. Both found the code, the tests and the merge clean. Head:
**`5960d8fc7e4f6ef2d7551bb224154ef2c265d894`** (`p1-persistence`, not pushed), two
one-line commits on `c066dd83`. Status: **REVIEW READY** at this head, posted on #83
(comment 5969914780).

| Commit | Item |
|---|---|
| `219cd67` | 2: the top, engine and writer banners and `tb/pp_top/README.md`, the amended map rule |
| `5960d8f` | 3: `tb/nvm_port/README.md`, the randomized cuts delivered by D3KR |

Items 1, 4 and 5 are in this file and PR-BODY.md (outside the tree), and item 1's
correction comment is on #83.

Where the two reviews give different exact texts for one place (R1 and R2 below), the
assignment's rule decides: R445-1 carries the exact texts. R444-1's text is applied
wherever it adds to R445-1's without contradicting it.

### R2.1 Item 1: the hunk count (R444-1 F3 = R445-1 F1)

- **Fixed.** PR-BODY.md, Round 1b, "Parent consumer set at milan-fpga dev `bbf704ec`",
  first bullet, and this file's R1b.3 now read: `parent-adoption-c8-bbf704ec.patch`
  keeps all 11 hunks (7 files), every `+`/`-` line identical to the `cdf49d1a`
  original, so no hunk dropped. Round 1b's "13" was wrong; the substantive claim (no
  hunk dropped) held.
- **Measured** on the two files in this directory:
  - `grep -c '^@@'`: 11 and 11;
  - `grep -c '^diff --git'`: 7 and 7;
  - the `+`/`-` lines (headers excluded) of the two patches compare identical;
  - `parent-adoption-c8-bbf704ec.patch`: 8,546 bytes, sha256
    `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c`, unchanged.
- **Correction on #83:** comment 5969802215, naming 11 hunks across 7 files. The STOP
  comment 5969239148 is not edited.

### R2.2 Item 2: the amended map contract in the banners (R444-1 F1 = R445-1 F2)

Authority: the manager's ruling 5967611704 item 1; 07 §5.1 "Who persists what" and §5.2
(records `0x60`/`0x70`: "the processor never writes or reads it"); the integrator guide's
marks row. Commit `219cd67`, R445-1's five exact replacements:

| Place (head) | Was | Now |
|---|---|---|
| `hdl/top/protocol_processor_top.sv:779-782` (`aecp_nvm_stb_o`/`aecp_nvm_mark_o` banner) | "group 6 is the saved-state contract's map stage, triggered by map edit phase 5, and not implemented in this release." | "group 6's records, the channel maps, are the integrator's to persist (07 §5.1, the ruling on #83): it saves a port's set from map edit phase 5, and the processor writes and restores no map record." |
| `hdl/aecp/KL_aecp_engine.sv:469-470` (`amap_edit_*` banner) | "Phase 5 is also the saved-state contract's map trigger (its map stage, not implemented here yet)." | "Phase 5 is also the integrator's map-persistence trigger (07 §5.1); the processor writes no map record." |
| `hdl/aecp/KL_aecp_nvm_writer.sv:94-97` (the value rules, stream format) | "the maps it will be checked against reset EMPTY in this stage, so nothing restored can be orphaned" | "the maps are the integrator's, restored after restore_done_o and judged against the formats this walk restored (07 §5.1), so the format/map coupling is the integrator's" |
| `hdl/aecp/KL_aecp_nvm_writer.sv:119-121` (the records) | "Channel maps are a later stage." | "Channel maps are the integrator's (07 §5.1); this writer never writes or reads them." |
| `tb/pp_top/README.md:665` (R21) | "maps are a later stage" | "maps are the integrator's, 07 §5.1" |

- **No logic change.** All 28 changed `hdl/` lines (`git diff -U0 c066dd8 HEAD -- hdl/`)
  are `//` or `//!` comment lines. The writer's sentence after the replacement
  (`:97-101`) is re-wrapped, its words unchanged.
- **The reviewers' grep** (`grep -rn "map stage\|later stage\|not implemented" hdl/
  tb/pp_top/README.md`) finds one line, `hdl/aecp/ucode/gen_ucode.py:1545` ("deliberately
  not implemented — grading a MAY as a SHALL would refuse rates"), which is the
  sampling-rate rule, not maps. No claim of a processor map stage is left.
- **Whole tree.** The only other "map stage" lines are 00:264, 02:683 and 07:564, each
  saying the ruling amends the parent D3 contract's map stage, which is correct.
- **Nothing anchors on the old text.** None of the 15 removed lines occurs in any tracked
  `.py`, `.patch`, `.sh`, `.cpp` or `.hpp` file (mutation drivers, plants, benches), and
  all 224 tracked mutation patches still apply (`git apply --check`).

### R2.3 Item 3: the randomized cuts are delivered (R444-1 F2 = R445-1 F3)

Authority: #83 acceptance 3; 09 F09.3's NVM row ("cut at randomized commit points ...
every record type cut ≥ once", `09_verification.md:56`), delivered by D3KR, which 09 §8.2
lists (`09_verification.md:193`). Commit `5960d8f`, R445-1's text appended to both
passages:

- `tb/nvm_port/README.md:1062-1067` (the coverage gaps, after "so the randomized half is
  still owed");
- `tb/nvm_port/README.md:1347-1351` (the limits, after "T15-T18 and T25 cut at fixed
  points named on the bus").

The text: "(delivered at the top by `tb/pp_top` section D3KR, issue #83: every record
type both producers write, cut by `rst_n` at 32 seeded-random points each, `--cut-seed
S` reruns one; this suite's own cuts stay fixed)".

**What stays port-local and owed:** no randomized cut. The 09 bar is met at the top,
where the port runs under both producers. The first passage's other outstanding item,
the three `*REQ` arms not armed with `gnt_err` (ERASE, WRITE, payload READ), is
unchanged from `main` and stays named there.

The suite's figures gate (`make -C tb/nvm_port figures`, the CI step that holds this
README to the tree) ran at the head: **rc 0**, "all measured figures agree with the
tree" (160 Verilator builds, 154 rows `[ok ]`, baseline 393 checks, 393 PASS),
about 14 minutes. It needs the two pre-fix revisions behind `refs/pull/13/head`, which
were fetched into this checkout's object store as CI does (`git fetch --no-tags origin
refs/pull/13/head`; only `FETCH_HEAD` moved, no branch or tag).

### R2.4 Item 4: PR-body residue (R445-1 R1, R2, R3; R444-1 R1, R2)

All in PR-BODY.md:
- **R445-1 R1 and R444-1 R1 (gate 16 is ruled).** "What remains" now carries R445-1's
  text verbatim: "Parent gate 16 at dev `bbf704ec`: ruled (b) (#83 comment 5969246536);
  its two T30 INTERNAL LAW checks are recorded against milan-fpga #643, which lands
  before the second pin adoption." R444-1's text for the same bullet adds one fact,
  kept as a closing sentence: "The PR does not wait for it." R444-1's second fix is
  applied verbatim after the Round 1b (a)/(b) list: "Ruled (b) on #83 (5969246536)."
  The same ruling line is added after this file's R1b.4 list.
- **R445-1 R2 and R444-1 R2 (area, item 12).** A new parent-visible item 12, R445-1's
  text verbatim, followed by the one sentence R444-1's adds (its 38- and 39-name figures
  are the same): "The 8x8 writer, a diagnostic, adds +1,520 LUT and +217 FF."
- **R445-1 R3 (the `tb/pp_top` growth).** Appended verbatim: ", HZ 176 to 177 and ST 18
  to 19 (the name saves' drain checks HZ9 and ST1)". The sum is now complete: 169 + 12
  + 11 + 1,000 + 1 + 1 = 1,194.

### R2.5 Item 5: suggestions, not taken in this round

Listed in PR-BODY.md as open:
- **R444-1 S1 / R445-1 S1 (Tests).** A checked floor per (type, class) in D3KR, or
  stratified seeds: at the 32 standing seeds `name` never lands A whole (D3K's fixed
  ERASE-grant cut covers it) and `cfg` lands one torn payload. R445-1 adds that for the
  five small scalar types the value rule masks a torn-acceptance defect.
- **R444-1 S2 (Robustness, Tests).** Model a non-atomic ERASE in the cut device, so the
  oracle covers a partly erased A explicitly.
- **R445-1 S2 (Docs).** The 8x8 writer diagnostic "+1,520 LUT, +217 FF" reproduces as
  +1,549 / +217 under the stated instrument; record the sv2v version and the full
  parameter set beside it, or state it as approximate.
- **R445-1 S3 (Robustness, Docs).** Name records are keyed by the writable-name ordinal
  alone; 07 §5.2 and the integrator guide could state that an image change that
  renumbers names requires erasing records `0x80`+, or what guards it.

### R2.6 Gates at the head (pinned Verilator 5.050)

| Command | Result at `5960d8f` |
|---|---|
| `./scripts/run_suites.sh` | **rc 0: 33 of 33 suites, 1,021,423 checks**, 0 failing (the UPC map and M9 opcode gates PASS), 12.5 min; every suite's count as at `c066dd8` (`pp_top` 10,390, `nvm_port` 1,219, `desc_store` 586, `adp_engine` 1,328) |
| `./scripts/lint_hdl.sh` (pinned simulator first on `PATH`) | rc 0, 41 modules LINT OK |
| `make check` | rc 0: 41 mermaid + 18 wavedrom blocks, 1,114 links, 115 REQ rows and 17 GAPs, 94 matrix rows (0 untested), parameters 28 = 28 = 28 |
| `python3 scripts/gen_matrix.py --check` | rc 0 (94 rows, 0 untested) |
| the docs gates as CI runs them (`check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `render-wavedrom.py --check`, `make stale`) | rc 0 |
| `make -C tb/nvm_port figures` (the README figures gate) | rc 0, all measured figures agree with the tree (R2.3) |
| `git apply --check` of every tracked mutation patch | 224 of 224 apply |

**ROMs, regenerated** from `git archive` exports of `c066dd8` and the head (generators
run as `syn/yosys/run.sh` and `tb/desc_store` do), compared by sha256: byte-identical.

| ROM | sha256 (both trees) |
|---|---|
| `ucode.hex` (2,048 words, `gen_ucode.py`) | `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8` |
| `ltn_rom.hex` (129, `gen_ltn_rom.py`) | `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` |
| `milan_min.json` image (`gen_desc_image.py`) | `11d6491b7f16642392961a0c2c9c04a91dfeab9b626169cac3a32b6c0843a8fb` |
| `milan_min.json` map | `6da275d26d64f89b1ae87245fedc514c05f662b94adddc98403de92af977da0e` |
| `example_milan_8.json` image (`--no-lint`) | `20356f5967e45a9eafcf8a63c5c933dca75fccb5d6bbc16941dc91dc2483b62c` |
| `example_milan_8.json` map | `4d20db2d00ff3478c5620696c39292eab65750d82a235eeb3dc725d6bb3d9db5` |

No generator or generator input changed (`git diff --stat c066dd8 HEAD`: the three HDL
files' comments and the two READMEs).

**Not re-run, by the assignment:** the parent consumer set (no parent-visible change)
and the mutation campaigns (the manager's banks re-run at the new head). The head
changes comments and README text only.

### R2.7 Record census, saved-state size, parent-visible list and cost

- **Census and saved-state size:** unchanged (no record, layout or port change).
- **Parent-visible:** nothing new. No port, parameter, register, census or capture
  change; the four parent patches in this directory are unchanged (the c8 patch's
  description is corrected, R2.1). PR-BODY.md's parent-visible list gains item 12, the
  area this file already carried (section 3 item 8, R1b.5 item 5).
- **Out-of-context cost:** unchanged, comments only: +705 LUT-eq / +92 FF at 1x1 with 38
  names, +683 / +94 at 39.

### R2.8 Seen, not fixed in this round

Two line citations in `tb/nvm_port/README.md:100-101`, outside this round's items, point
at the wrong lines. Neither review raised them:
- `hdl/aecp/KL_aecp_nvm_writer.sv:482-485` for `frame_ok_w`: right at the base
  `ddb3119d` (`:483`), stale since round 1's name stage (`:547` at `c066dd8`, `:550-553`
  at the head, the three added comment lines included).
- `hdl/top/protocol_processor_top.sv:2714` for the `KL_acmp_nvm_shadow` instance: already
  stale on `main` (`:2727` at `ddb3119d`, `:2730` at the head).

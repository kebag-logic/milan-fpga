# #658 stage 1 — [A539] handoff

Role: executor (author). Lane `658-dynmap-default` from dev `e617275074e370cec342af99b929e2588fc8d43f`.
Assignment: issue #658 comment 5988328859; ruling 5988293154.
TAKEN: issue #658 comment 5988336708.
Head: `c36bfb03077a467eeacec7de5e25de9635e0d015` (one commit on the base, not pushed).

Status: STOP posted on #658 (see section 8). Stage 1 complete; nothing pushed.

## 0. Summary

- Every store a GET_AUDIO_MAP reads resets EMPTY. Nothing writes a map at boot:
  no seeder, no firmware step, no saved-state restore of maps. The legacy control
  plane (deleted 2026-08-13, `eff99a9c6`) reset to an identity image and seeded
  both crossbar RAMs. The processor-era store (`a3cac8669`, 2026-08-17) resets to zero.
- Simulated on the AX7101 1x1 TDM8 shape: 0 mappings on SPI 0 and SPO 0 at
  power-on, after 8 -> 4 and after 4 -> 8. SET_STREAM_FORMAT never edits a map.
- The bench state (input 1 mapping s0.c0 -> cluster 0, output none, input at
  4 ch) arises only from ADD/REMOVE (or the CSR debug window). In simulation,
  SET 4 ch + ADD four identity + REMOVE channels 1..3 reproduces it exactly. The
  public record dates it: lane B9 left both maps empty at 05:27Z on 2026-10-04,
  and the owner's 14:30 read already showed the one mapping. Lanes B10 and B11
  then "restored as found".
- **Ruling item 2 conflicts with Milan v1.2 5.4.2.7.** That clause says a
  SET_STREAM_FORMAT that drops a mapped channel SHALL be refused with
  BAD_ARGUMENTS, and the tree implements and tests that refusal (#67). With the
  identity default in place, the ruled 8 -> 4 removal is a deviation, and it
  needs device-originated ADD/REMOVE notifications that the processor cannot
  send today. This needs a decision before stage 2.
- Recommendation: option A, an RTL reset image in the parent, for item 1. It
  needs no processor change for the default itself and costs 0 LUT (measured).
  Item 2 needs the owner's decision; my recommendation is Milan-conformant
  refusal (2b). Two boot-time consequences of option A have to be carried by
  stage 2 whichever way item 2 goes: see section 4.

## 1. Map stores (reset value, file:line) at e6172750

Shape: AX7101 1x1 TDM8 (`configs/endstation_ax7101_1x1_tdm8.yaml`). The tracked
`hdl/common/gen/adp_shape_defaults.svh` is byte-identical to this shape's
generated copy. Relevant constants: `ADP_DMAP_IN_KEYS_C=8`, `ADP_DMAP_IN_PCLS_C={8}`,
`ADP_DMAP_IN_PNMAPS_C={1}`, `ADP_DMAP_IN_SCH_C={8,0}`, `ADP_DMAP_IN_RPHYS_C`
= render keys 2..9; `ADP_DMAP_OUT_PCLS_C={17}` (8 TDM8 In, Pilot, 8 Loopback),
`ADP_DMAP_OUT_SCH_C={8}`, `ADP_DMAP_OUT_CSRC_C` (17 capture-source words).

| Store | What reads it | Writers | Reset value | file:line |
|---|---|---|---|---|
| `amap_in_store_r` (8 x 8 bit, protocol input store, key = global cluster) | GET_AUDIO_MAP on STREAM_PORT_INPUT (`amap_page_slot`), the SET_STREAM_FORMAT survives sweep (`sfv_ent_w`), ADD/REMOVE validation | ADD/REMOVE phase 5 (`amap_edit_commit`); CSR 0x900 debug window, side 0 | all zero = no mapping | decl `hdl/milan/milan_datapath.sv:3762`; reset `:4408`; phase-5 write `:4479`; CSR write `:4520-4527`; GET read `:3935`; sweep `:4820` |
| `amap_out_owner_v_r`, `amap_out_owner_r`, `amap_out_cluster_r` (per stream channel: owner port, cluster offset) | GET_AUDIO_MAP on STREAM_PORT_OUTPUT (`amap_out_slot`/`amap_out_fmt`: a record exists iff owner_v and owner == port) | ADD/REMOVE phase 5; CSR window side 1 (`:4508-4518`) | all zero = no mapping | decl `milan_datapath.sv:1218-1220`; reset `:4409-4411`; phase-5 write `:4494-4500` |
| Capture map RAM `map_r` (13 bit per stream channel, `KL_chan_map_capture`) | the talker's media path; ADD/REMOVE validation (`cmap_flat_w`); SET_STREAM_FORMAT output survives (`sfv_out_need`). NOT read by GET_AUDIO_MAP | ADD/REMOVE phase 5 via `aecp_odmap_wr_*`; CSR window side 1 | 13'h0000 = silence | decl `hdl/ieee1722/aaf/KL_chan_map_capture.sv:492`; reset `:500`; write mux `milan_datapath.sv:1252-1267` |
| Render map RAM `map_r` (8 bit per physical render key, `KL_chan_map_render`) = physical projection of the input store through `ADP_DMAP_IN_RPHYS_C` | the listener's render path only (CHMAP_LOOP 0x914 readback) | ADD/REMOVE phase 5 via `aecp_dmap_wr_*`; CSR window side 0 | 8'h00 = unmapped | decl `hdl/ieee1722/aaf/KL_chan_map_render.sv:139`; reset `:143`; write mux `milan_datapath.sv:6543-6559` |
| Generated `AEM_DYNMAP` / `AEM_ODYNMAP` constants (incl. the `AEM_ODMAP_INIT_C` identity image) | nothing in RTL since `eff99a9c6` (2026-08-13): `aecp_aem_rom.svh` is review-only (`sw/builder/endstation_builder.py:16`) | `avdecc/aem_assemble.py:406-469` (`_dynmap_tables`), `:472-551` (`_odmap_tables`, INIT at `:530-539`); `avdecc/aem_emit.py:311-391` | n/a (not compiled) | as named |
| Input stream-format row `fmtin_r`/`fmtin_v_r` (processor `KL_aecp_dyn_state`) | GET_STREAM_FORMAT; the record bound in ADD validation (`milan_datapath.sv:4231-4238`) | SET_STREAM_FORMAT only (`gen_ucode.py:2170-2195`, `WRITE_ST` to `SEL_FMTIN`), and the saved-state restore of a set format | invalid, so GET serves `ADP_STRIN_FMT_C` = 8 ch | `protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv:295,306,335` |
| Firmware boot step | - | none: `configure_fabric()` and `milan_init()` write no CHMAP register | - | `sw/firmware/milan_baremetal/milan_baremetal.c:1582-1604,1656-1677` |
| Saved-state map records `0x60`-`0x7F` | - | not materialized (stage 3 of #70); the AECP engine is the only driver of the edit face (`KL_aecp_engine.sv:2241-2251`) | - | `docs/design/SAVED_STATE_MATERIALIZATION.md:13,188` |

History: until `eff99a9c6` the legacy builder reset its input store to an identity
image (`dmap_init_key`) and seeded both crossbar RAMs after reset
(`git show eff99a9c6^:hdl/ieee17221/aecp/KL_aecp_response_builder.sv`, lines
1082-1100 and 2430-2470). The parent store that replaced it (`a3cac8669`,
2026-08-17) resets to zero. The same legacy file records an earlier "prune on
format change" decision. Milan 5.4.2.7 overturned it, and the file then
refused instead (lines 1260-1281).

## 2. Simulated readbacks (reset; 8 -> 4 -> 8 on STREAM_INPUT 0)

Vehicle: `make -C tb/verilator/milan_dp dynmap` (committed, `c36bfb03`). This
is `sim_nxn.cpp`'s new `[DYNMAP]` section on the cfg_ax7101 geometry
(`SHAPE_AX1x1`, `TALKER_WIRE_CHANS_P=8`, `AUDIO_IF_SLOTS_P=8`, master,
`LOOPBACK_P=1`, `I2SPB_P=0`, `LPF_P=0`). It serves the shipped AEMI image
generated from the config, and starts the restore walk the way firmware does.
"Power-on" is the first answer after the walk releases AECP; no controller can
read earlier.

| Step | STREAM_INPUT 0 format | GET_AUDIO_MAP SPI 0 (page 0) | GET_AUDIO_MAP SPO 0 (page 0) | Ruled |
|---|---|---|---|---|
| power-on | `0205022002006000` (8 ch) | SUCCESS, number_of_maps 1, **0 mappings** | SUCCESS, number_of_maps 1, **0 mappings** | SPI 8 identity, SPO 8 identity |
| SET_STREAM_FORMAT 4 ch: SUCCESS | `0205022001006000` | 0 mappings | 0 mappings | SPI 4 identity, SPO 8 |
| SET_STREAM_FORMAT 8 ch: SUCCESS | `0205022002006000` | 0 mappings | 0 mappings | SPI 8, SPO 8 |

The image declares SPI 0 with 8 clusters and SPO 0 with 17. STREAM_OUTPUT 0 is 8 ch.
All 12 ruled checks are red; the 77 other checks pass.
Excerpts: `sim_dynmap_red_at_c36bfb03.txt` (red marker, rc 0) and
`sim_dynmap_unmarked.txt` (`DYNMAP_RED=0`: 12 failures, binary rc 1, make rc 2).

The committed check, and why it is shaped this way:
- Counts are read from the device and the image (GET_STREAM_FORMAT, STREAM_PORT
  `number_of_clusters`); only the scenario's 8 -> 4 -> 8 is a literal.
- Red marker `DYNMAP_RED=1` (default): a differing ruled check prints `[red]`.
  One that AGREES fails, so the marker cannot outlive the behaviour. Stage 2
  builds `DYNMAP_RED=0`.
- The 8 -> 4 SET status is a plain check expecting SUCCESS (the ruling). It
  passes at this head only because the map is empty. Under the identity default
  it is exactly where Milan 5.4.2.7 bites (section 4).
- Outside `run` (`TESTING.md`, suite README row `obj_dynmap`); stage 2 adds it
  to `run` when green.

Can the check pass? Scratch prototype `scratch_protoA_milan_datapath.diff`
(identity reset of the two protocol stores only) through the same recipe:
- Unmarked: both power-on pages read 8 identity records and pass. 8 -> 4 is
  then **refused BAD_ARGUMENTS (status 7)** by today's Milan 5.4.2.7 verdict:
  format unchanged, map still 8 (`sim_protoA_unmarked.txt`, 4 failures).
- Under the red marker: 10 stale-marker failures, 2 red
  (`sim_protoA_red_marker.txt`).

## 3. How the observed bench state arises

Static reading and simulation agree:

| Sequence (scratch `[DIAG]`, `sim_diag_bench_state.txt`) | SPI 0 | SPO 0 |
|---|---|---|
| reset; 8 -> 4 -> 8 (section 2) | 0 | 0 |
| B1 SET 4 ch (the bench lanes' binding rule) | 0 | 0 |
| B2 ADD four identity mappings | 4: c0..c3 -> o0..o3 | 0 |
| B3 REMOVE channels 1..3 ("restore as found" of a 1-mapping start) | **1: s0.c0 -> o0.c0** | **0** |
| B4/B5 SET 8 ch, SET 4 ch | 1 (survives both) | 0 |
| C1/C2 REMOVE it, then one ADD from empty | 1: s0.c0 -> o0.c0 | 0 |
| D1 ADD 8 identity under 4 ch | refused 7 (7.4.45.2 current-format bound) | - |
| D3/D4 ADD 8 identity under 8 ch, then SET 4 ch | refused 7 (Milan 5.4.2.7), map keeps 8 | - |

So reset gives 0/0 and a format change never moves a map. Only an ADD (or the
CSR debug window, `milan_datapath.sv:4520-4527`) can create the bench's one
input mapping; the 4 ch format is a controller SET_STREAM_FORMAT.
Public trail:
- Lane B9 left "both maps empty" (#629 comment 5976928373, 2026-10-04 05:27Z).
- The owner's read at 14:30 the same day saw the one input mapping (#658 body).
- Lane B10 found it (#629 5983219870, 18:47Z). It put four identity mappings on
  (one of them already present) and restored "its one as-found input mapping".
- Lane B11 found and left it (`docs/findings/653_DISCONNECT_ORDER_BENCH.md:71-77,295`).

The one mapping is therefore a leftover of a controller action between 05:27Z
and 14:30Z on 2026-10-04, carried forward by "restore as found". It is not a
reset value. It also implies no power cycle since that ADD: maps are not
materialized, so a power cycle would have emptied the map. The 4 ch format, by
contrast, is a stage-1 materialized group (`TRG_fmti`,
`SAVED_STATE_MATERIALIZATION.md:429`) and survives power cycles. Read at
power-on, the bench board should therefore show 4 ch and an empty map. That is
for the manager's bench read to confirm.

## 4. Options

### Item 1: power-on identity on both stream ports

**A. RTL reset image in the parent (recommended).**
- Files:
  - `hdl/milan/milan_datapath.sv`: reset `amap_in_store_r` and the three output
    owner registers to an identity image. Constant functions over the
    `ADP_DMAP_IN_*`/`ADP_DMAP_OUT_*` constants compute it; those constants are
    already in `gen/adp_shape_defaults.svh`, so no new generated value is
    needed. The prototype diff shows the store half.
  - The media path must agree from the first tick. Either give
    `hdl/ieee1722/aaf/KL_chan_map_capture.sv` (word = `ADP_DMAP_OUT_CSRC_C`
    of the cluster) and `KL_chan_map_render.sv` (through
    `ADP_DMAP_IN_RPHYS_C`) a reset-image parameter each (a leaf parameter
    change, ports unchanged), or replay the image into both RAMs after reset
    through their existing write ports, as the legacy `dmseed_r`/`odseed_r`
    seeders did.
  - Processor files: none for the default itself.
- Area: a reset-value change costs **0 LUT, 0 FF**, measured. Yosys
  `synth_xilinx` on a 64-bit store, zero vs identity reset: LUT and MUXF counts
  identical; 20 of 64 FDCE become FDPE (`area_reset_image_microbench.txt`). The
  crossbar RAMs are flop arrays with reset, so a reset image there costs the
  same. A seeder instead: estimate up to 20 LUT + 4 FF, not measured.
- Protocol-visible:
  - GET_AUDIO_MAP: SPI 0 and SPO 0 each read 8 identity records from the first
    answer after AECP release (prototype, measured).
  - Notification: none. No controller can be registered before AECP is
    released.
  - Media: TDM8 In slot c rides stream channel c; listener channel c renders
    to TDM slot c.
  - ADD of a different mapping onto an identity-held cluster (input) or stream
    channel (output) is BAD_ARGUMENTS under today's validation
    (`milan_datapath.sv:4278-4282,4309-4318`), which Milan 5.4.2.27 allows
    ("may"). Controllers must REMOVE first; the render harness's M4 case
    already pins that rule.
  - The SET_STREAM_FORMAT verdict sees channels 0..7 mapped, so 8 -> 4 is
    refused (measured) unless item 2 changes it.
- Consequences stage 2 must carry, whatever item 2 decides:
  1. **Restored formats.** The stage-1 restore judges a saved format on verdict
     bit 0 ("supported") alone, because "the maps it will be checked against
     reset EMPTY in this stage" (`protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:91-94,620`).
     With an identity reset, a saved narrower input format would restore beside
     orphaned mappings 4..7, breaking the standing invariant of Milan 5.3.10.1.
     The bench board's NVM very likely holds such a format (section 3). Fix
     with one of:
     - the restore judges both bits, so the format reverts to the image
       default. That is the rule #70 section 8.4 step 4 already sets. One
       processor file, under #661.
     - item 2's adaptation applied to the restored format before release
       (parent).
  2. **#70 text.** The design says the map plane's reset value and roll-back
     target is "the EMPTY set" (`SAVED_STATE_MATERIALIZATION.md:188,595-597`).
     It becomes the identity set; see section 6.
  3. **Existing tests assume an empty start.** They must be re-based (assert
     the identity, or REMOVE it first), never relaxed:
     - `sim_nxn.cpp:3725` (8x8 capture key 0 EMPTY; its own comment says it
       must change the day a seeder returns);
     - `:5080` `[AMAP]` (exact record count 2 after CSR provisioning);
     - `:6316` `#67` (ADD on cluster 0);
     - `:7373` `[T66]` (8x8 output rows);
     - the ADD sequences of `tb/verilator/milan_dp_render/sim_tdm8_render.cpp`.
- Test plan:
  - `make dynmap DYNMAP_RED=0`: the power-on checks go green, proven on the
    prototype; the adaptation checks follow the item 2 decision.
  - Re-base the sections above.
  - End to end, with no map command issued:
    - listener: `milan_dp_render` proves per-channel markers on stream
      channel c reach TDM render slot c;
    - talker: the `obj_ax1x1` capture path proves TDM capture slot c reaches
      AAF stream channel c.
  - Boot consistency: a saved 4 ch input format leaves no orphaned mapping
    after the restore (nvm_cosim, or a milan_dp leg with an NVM image).
  - Full milan_dp, milan_dp_render, pp_shadow; yosys gate.

**B. Generated initial content.**
- B1, builder-emitted reset image:
  - Files: `sw/builder/endstation_builder.py` emits identity words per key
    (`ADP_DMAP_IN_INIT_C`, `ADP_DMAP_OUT_INIT_C`) into
    `gen/adp_shape_defaults.svh`, regenerated for the 5 configs plus the
    tracked `hdl/common/gen` copy; `sw/builder/test_builder.py` gets a gate
    pinning the image to the geometry. The RTL change sites are A's, reading
    the table instead of computing it. This is the legacy `AEM_ODMAP_INIT_C`
    route (`aem_assemble.py:530-539`), whose image has no consumer today.
    Processor: none.
  - Area: same as A, 0.
  - Protocol-visible: same as A.
  - For: the default becomes a config fact, so a product could select identity
    or empty without an RTL edit, and the generator can keep the legacy "only
    where the source projects" rule.
  - Against: the min(channels, clusters) rule then lives in Python as well as
    in the RTL validators, plus six regenerated headers and a new pin.
  - Test plan: A's, plus the builder gate.
- B2, factory record in the AEM image, written by the processor at boot
  through the edit face:
  - This is #70 stage 3's map-restore path with a factory record.
  - Milan 5.3.3.9 forbids AUDIO_MAP descriptors on a Stream Port Input, so the
    record would be vendor data.
  - Files: processor (writer), `avdecc/gen_aemi_image.py`; touches the
    processor (#661). Area: stage-3 writer cost (#70 section 12), not estimated
    here.
  - Not a stage-2 option.

**C. Firmware step at boot.**
- Files:
  - `sw/firmware/milan_baremetal/milan_baremetal.c`: in `configure_fabric()`,
    arm `CHMAP_CTRL[0]`, write `CHMAP_SEL`/`CHMAP_WORD` per key, disarm. It runs
    before `nvm_boot()`, so before AECP release.
  - `sw/litex/boot_policy.py` (the generated words), `sw/litex/milan_soc.py`
    (publishes them).
  - `sw/builder/test_builder.py` gate 35 (host run), `sw/firmware/nvm_hosttest`
    stubs.
  - `docs/reference/REGISTER_MAP.md`: 0x900 becomes a product path.
  - RTL and processor: none.
- Area: 0 fabric. Firmware: about 100-200 B of code plus 16 generated words
  (estimate).
- Protocol-visible: same readback as A once the firmware has run.
- Against:
  - The window is documented bring-up-only (`milan_datapath.sv:4811`).
  - #70's roll-back `rb_rst` returns the map plane to the RTL reset value
    (EMPTY), so an aborted restore loses the default unless firmware runs
    again.
  - On the CSR path the output owner registers come from a first-match CSRC
    search (`amap_out_cluster`).
  - It cannot implement item 2: a non-ATDECC change while unlocked must notify
    (Milan 5.4.5.2), and the CSR writer is refused while locked.
- Test plan: gate 35 checks the CSR write sequence. `[DYNMAP]` would need a
  prelude imitating the firmware, which tests a copy of the sequence rather
  than the firmware; the CPU cosim (`tb/verilator/nvm_capture_cpu`) avoids
  that.

### Item 2: the input map follows a format adaptation (needs a decision)

- **2a, the ruling as written.** On SET_STREAM_FORMAT to N channels, remove the
  input mappings with stream channel >= N; on widening, add identity where the
  cluster is unmapped.
  - Conflict: Milan v1.2 5.4.2.7 says "before accepting a SET_STREAM_FORMAT
    command, the PAAD-AE shall check that all channels ... referenced by
    existing mappings (static or dynamic) still exist in the new format. If
    not, the PAAD-AE shall refuse the command with the BAD_ARGUMENTS error
    code." 1722.1-2021 7.4.9.2 makes the refusal optional ("may"); Milan makes
    it a SHALL. The tree implements it in `gen_ucode.py:2152-2195` (verdict
    bit 1) and grades it in `sim_nxn.cpp` `#67` ("a 1ch format that orphans
    channel 2 is BAD_ARGUMENTS").
  - Work:
    - µprogram `_sfmt` stops refusing on bit 1 for STREAM_INPUT;
    - a parent prune/identity engine reusing the edit commit paths and the
      render projection (estimate 30-60 LUT, not measured);
    - device-originated unsolicited REMOVE/ADD_AUDIO_MAPPINGS notifications to
      the registered controllers (Milan 5.4.5.2). Today's map notification
      echoes the staged command payload (`KL_aecp_engine.sv:2904-2907`,
      `KL_aecp_notify.sv:896`), so the records must be synthesized (processor
      estimate 100-300 LUT plus µcode, not measured);
    - the #70 map trigger raised for these writes.
  - Processor files: yes (`gen_ucode.py`, `KL_aecp_engine.sv`,
    `KL_aecp_notify.sv`), under #661.
- **2b, Milan-conformant.** Keep the refusal.
  - A controller adapting 8 -> 4 must first REMOVE channels 4..7, then SET; on
    widening it SETs and ADDs.
  - The bench's binding rule changes accordingly. A controller that adapts
    without removing gets BAD_ARGUMENTS, the Milan-specified answer.
  - No RTL or processor change beyond A. `[DYNMAP]`'s 8 -> 4 expectation
    becomes BAD_ARGUMENTS with the map and format unchanged.
- A parent-only silent prune is not an option. It changes GET_AUDIO_MAP with no
  notification (Milan 5.4.5.2) and with no #70 map trigger.

## 5. Recommendation

- Item 1: **option A**.
  - Identity reset image in `milan_datapath.sv` from the existing `ADP_DMAP_*`
    constants, plus reset images for the two crossbar RAMs. 0 LUT.
  - No processor change for the default itself.
  - Re-base the five empty-start test sections.
- Item 2: decision needed before stage 2. I recommend **2b**: keep Milan
  5.4.2.7, free and conformant. If the owner chooses 2a, do it in one lane
  with the notifications and the #70 trigger.
- Boot consistency, stage 2 either way: under 2b the restore judges both
  verdict bits, so a saved narrower format reverts to the image default
  (#70 8.4 step 4); this is one processor file, `KL_aecp_nvm_writer.sv`, under
  #661. Under 2a the restored format is pruned to instead.

## 6. Persistence (#70) needs

- Records `0x60 + STREAM_PORT_INPUT index` and `0x70 + STREAM_PORT_OUTPUT
  index` are already allocated (`SAVED_STATE_MATERIALIZATION.md:188,431-432`).
  Both are triggered by the phase-5 edit commit (`amap_edit_live_wr_p` ->
  `amap_live_wr_i`). Under 2a, device-originated prune/identity writes must
  raise the same trigger.
- The reset set becomes the identity set. Update the document (`:188`,
  `:595-597` "reset value, the EMPTY set") and the processor comment
  `KL_aecp_nvm_writer.sv:91-94`. The roll-back `rb_rst` then returns to
  identity.
- Section 8.4: with a non-empty reset set, a saved narrower format with no saved
  map record reverts to the image default (step 4), or is pruned to under 2a.
  The bench board's persisted 4 ch input format exercises this on the first boot
  of a stage-2 image.
- Capacity: input record = the port's cluster count (8 for SPI 0). Output
  record per FASTCONNECT section 4.2. The unused-entry and framing rules are
  unchanged.

## 7. Gate table (head c36bfb03)

Committed: `tb/verilator/milan_dp/sim_nxn.cpp` (`[DYNMAP]` section),
`tb/verilator/milan_dp/Makefile` (`dynmap`, `dynmap-build`, `DYNMAP_BUILD`,
clean list), `tb/verilator/milan_dp/README.md` (objdir row),
`docs/testing/TESTING.md` (one line). No RTL, processor, port, register-map or
parameter change.

Pinned Verilator 5.050 throughout (`$VALIDATION_TOOLS/pinned-verilator-5.050`).

| Gate | Command | rc | Result |
|---|---|---|---|
| new leg, red marker | `make -C tb/verilator/milan_dp dynmap VERILATOR_JOBS=16` | 0 | 89 checks, 0 failures; 12 of 12 ruled checks red |
| full milan_dp suite (5 legs compile `sim_nxn.cpp`) | `make -C tb/verilator/milan_dp VERILATOR_JOBS=16` | 0 | `suite_tally.py`: 11877 checks, 0 failures, 16 tallies; wall 1839 s; log 2,139,391 B, sha256 `36637bf5266e2d3db9b4b0ffa8850e535508757db07663441690d46606914f5c` |
| tally verdict | `python3 scripts/suite_tally.py --verdict milan_dp.log` | 0 | - |
| docs | `python3 scripts/docs_check.py` | 0 | 0 findings, 189 md + 988 text files |
| em dash | `python3 scripts/check_em_dash.py --base e6172750` (pinned renderer in a scratch venv) | 0 | 0 findings over 2 added lines |
| doc style | `python3 scripts/check_doc_style.py` | 0 | OK |
| submodule source literals | `python3 scripts/pp_srcs.py --check` | 0 | - |
| lint ratchet (RTL untouched) | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| render suite inputs | `print-srcs`, `print-pp-srcs`, `print-dp-vflags` base vs head | - | byte-identical, so `milan_dp_render` is unaffected |

Evidence runs (not gates; they are meant to fail):
- `DYNMAP_RED=0`: 12 failures, binary rc 1, make rc 2.
- Prototype A unmarked: make rc 2, 4 failures (the Milan 5.4.2.7 refusal).
- Prototype A under the marker: make rc 2, 10 stale-marker failures.

Not run, with reason:
- `scripts/run_all_suites.sh` and `syn/yosys/run.sh`: only `milan_dp` is
  touched, and no RTL.
- `xvlog_gate.py`: no RTL.
- `act_ci.py`: no PR head; this stage does not push.

In-tree build products were removed after the runs (`make clean`); the tree is
clean. Scratch builds were removed from `$VALIDATION_STORAGE/658-a539`.

Files here: the `sim_*.txt` excerpts, `scratch_protoA_milan_datapath.diff`,
`scratch_diag_sim_nxn.diff`, `scratch_build_diag.sh`, the area micro-bench
(`store_*.v`, `area_reset_image_microbench.txt`).

## 8. Public record

- TAKEN: #658 comment 5988336708 (`TAKEN.md` here).
- STOP: #658 comment 5988813022 (`STOP.md` here; the readback is identical but for
  a trailing newline). It carries the head, the store table, the readbacks, the
  bench-state finding, the options, the Milan 5.4.2.7 decision request, the
  recommendation, the #70 needs and the gate summary.
- Nothing pushed; no PR. Branch `658-dynmap-default` at `c36bfb03` is local to
  `$LANES/658-dynmap-default`.

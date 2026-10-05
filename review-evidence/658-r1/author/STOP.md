[A539] STOP
Head: `c36bfb03077a467eeacec7de5e25de9635e0d015` on `658-dynmap-default`. It is one commit on dev `e6172750`, not pushed: a standing test only, with no RTL or processor change.

**Decision needed before stage 2.** Ruling item 2 (remove input mappings past the new channel count on an adaptation) conflicts with Milan v1.2 5.4.2.7: *"before accepting a SET_STREAM_FORMAT command, the PAAD-AE shall check that all channels ... referenced by existing mappings (static or dynamic) still exist in the new format. If not, the PAAD-AE shall refuse the command with the BAD_ARGUMENTS error code."* The tree implements that refusal (`gen_ucode.py` `_sfmt`, verdict bit 1) and grades it (`sim_nxn.cpp` #67: "a 1ch format that orphans channel 2 is BAD_ARGUMENTS"). With the identity default in place, every 8 -> 4 adaptation hits it. A prototype of the identity reset measured exactly this: SET 4 ch is refused with status 7, and the map and format stay at 8.

**1. Stores.** Everything a GET_AUDIO_MAP reads resets empty, and nothing writes a map at boot.

| Store | Read by | Reset | file:line |
|---|---|---|---|
| `amap_in_store_r` (input, key = global cluster) | GET on STREAM_PORT_INPUT, the SET_STREAM_FORMAT survives sweep, ADD/REMOVE validation | 0 | `milan_datapath.sv:3762`, reset `:4408` |
| `amap_out_owner_v_r` / `_owner_r` / `amap_out_cluster_r` | GET on STREAM_PORT_OUTPUT | 0 | `milan_datapath.sv:1218-1220`, reset `:4409-4411` |
| capture map RAM (talker media path, ADD validation; not read by GET) | - | 13'h0 | `KL_chan_map_capture.sv:492`, reset `:500` |
| render map RAM (physical projection of the input store) | - | 8'h0 | `KL_chan_map_render.sv:139`, reset `:143` |

Writers: ADD/REMOVE phase 5 (`amap_edit_commit`) and the CSR 0x900 debug window (`milan_datapath.sv:4508-4527`).
- Firmware: no step (`milan_baremetal.c:1582-1604,1656-1677`).
- Saved state: the map records `0x60`-`0x7F` are not materialized.
- The generated `AEM_DYNMAP`/`AEM_ODMAP_INIT_C` identity image (`aem_assemble.py:530-539`) has had no RTL consumer since `eff99a9c6` (2026-08-13). Until then the legacy plane reset to identity and seeded both RAMs. The processor-era store (`a3cac8669`) resets to zero.

**2. Red check.** New focused leg: `make -C tb/verilator/milan_dp dynmap`, the AX7101 1x1 TDM8 shape at the cfg_ax7101 geometry, serving the shipped image.

| Step | STREAM_INPUT 0 | SPI 0 | SPO 0 | Ruled |
|---|---|---|---|---|
| power-on (first answer after the restore walk releases AECP) | `0205022002006000` | SUCCESS, 1 map, **0 mappings** | **0** | 8 identity / 8 identity |
| SET 4 ch: SUCCESS | `0205022001006000` | 0 | 0 | 4 / 8 |
| SET 8 ch: SUCCESS | `0205022002006000` | 0 | 0 | 8 / 8 |

The test expects the ruled behaviour and is marked red at this head (`DYNMAP_RED=1`):
- with the marker: 12 of 12 ruled checks red, 77 others pass, rc 0;
- a ruled check that agrees fails as a stale marker (shown with the prototype: 10 such failures);
- `DYNMAP_RED=0`: 12 failures, rc 2.

The leg stays outside `run` until stage 2 turns it green. All counts are read from GET_STREAM_FORMAT and the image (SPI 0: 8 clusters; SPO 0: 17).

**3. Bench state.** Reset gives 0/0, and SET_STREAM_FORMAT never edits a map. Only ADD/REMOVE, or the CSR debug window, produce the bench state. In simulation, SET 4 ch, then ADD four identity mappings, then REMOVE channels 1..3 reproduces the bench read exactly: SPI 0 holds one mapping s0.c0 -> o0.c0 and SPO 0 none.

Public trail:
- lane B9 left both maps empty (#629, 5976928373, 05:27Z 2026-10-04);
- the owner's 14:30 read already showed the mapping;
- lanes B10 (5983219870) and B11 (`653_DISCONNECT_ORDER_BENCH.md`) restored it "as found".

So it is a leftover of a controller action, not a reset value. Input formats are stage-1 persisted and maps are not, so a power-on read should show 4 ch and an empty map.

**4. Options**
- **A. RTL reset image in the parent (recommended).**
  - Files: `milan_datapath.sv` (identity reset of the input store and the output owner registers, computed from the existing `ADP_DMAP_*` constants) plus matching reset images for the capture and render RAMs (`KL_chan_map_capture.sv`, `KL_chan_map_render.sv`, or a post-reset seeder). No processor file for the default itself.
  - Area: **0 LUT / 0 FF**, measured on xc7. A store with an identity reset maps to identical LUT/MUXF counts; only FDCE becomes FDPE.
  - Protocol-visible: GET reads 8 identity records on both ports from the first answer. No notification is needed, because nothing can register before AECP is released. Re-pointing an identity-held cluster or stream channel needs a REMOVE first (BAD_ARGUMENTS otherwise, which Milan 5.4.2.27 allows).
  - Test plan: `dynmap DYNMAP_RED=0`. Re-base, not relax, the tests that assume an empty start: `sim_nxn.cpp` `:3725`, `[AMAP]` `:5080`, `#67` `:6316`, `[T66]` `:7373`, and the ADD sequences in `sim_tdm8_render.cpp`. End to end with no map command: stream channel c reaches TDM slot c (`milan_dp_render`), and TDM capture slot c reaches stream channel c (`obj_ax1x1`).
  - Must carry: the stage-1 restore judges a saved format on verdict bit 0 alone, "because the maps ... reset EMPTY" (`KL_aecp_nvm_writer.sv:91-94,620`). With an identity reset, a saved 4 ch input format, which the bench board likely holds, would restore beside orphaned mappings 4..7 (Milan 5.3.10.1). Either the restore judges both bits (one processor file, under #661; the format reverts to the image default per #70 section 8.4 step 4), or item 2's adaptation is applied to the restored format before release.
- **B. Generated initial content.**
  - B1: the builder emits per-key identity words into `gen/adp_shape_defaults.svh` (5 configs plus the tracked copy, with a `test_builder.py` pin), and the RTL resets to them. Same RTL, area and wire behaviour as A. The rule then lives in Python too.
  - B2: a factory record in the AEM image, walked through the edit face by the processor. This is #70 stage 3's path (processor files), and it is not a stage-2 option.
- **C. Firmware step at boot.**
  - Files: `configure_fabric()` writes the 0x900 window before `nvm_boot()`; `boot_policy.py`/`milan_soc.py` generate the words; gate 35 tests it. Fabric 0 LUT; about 100-200 B of code (estimate).
  - Against: the window is documented bring-up-only (`milan_datapath.sv:4811`). #70's roll-back resets the map plane to the RTL value, EMPTY. The firmware cannot do item 2: Milan 5.4.5.2 requires notifications, and the window is refused while locked.
- **Item 2.**
  - 2a, the ruling: the µprogram stops refusing on bit 1; a parent prune/identity engine (estimate 30-60 LUT); device-originated unsolicited REMOVE/ADD_AUDIO_MAPPINGS notifications. Today's map notification echoes the staged command (`KL_aecp_engine.sv:2904-2907`), so the records must be synthesized (estimate 100-300 LUT plus µcode). The #70 map trigger must fire for these writes. Processor files: `gen_ucode.py`, `KL_aecp_engine.sv`, `KL_aecp_notify.sv`, under #661.
  - 2b, Milan-conformant: keep the refusal, so a controller removes channels 4..7 before SET 4 ch. No change beyond A, and `[DYNMAP]`'s 8 -> 4 expectation becomes BAD_ARGUMENTS.
  - A silent parent-only prune is excluded: no notification, and no #70 trigger.

**Recommendation:** A for item 1. For item 2, 2b plus the restore judging both bits, unless the owner accepts a Milan 5.4.2.7 deviation; in that case 2a, as one lane with its notifications.

**5. #70 needs**
- Records `0x60+SPI`/`0x70+SPO` are already allocated, triggered by the phase-5 commit; under 2a, device-originated edits must trigger them too.
- The reset set and the roll-back target change from EMPTY to identity: `SAVED_STATE_MATERIALIZATION.md:188,595-597`, and the processor comment above.
- Section 8.4: a saved narrower format with no map record reverts, or under 2a prunes.

**Gates at the head**, all rc 0, pinned Verilator 5.050:
- `make dynmap`: 89 checks / 0 failures, 12 red;
- full `make -C tb/verilator/milan_dp`: `suite_tally` 11877 checks, 0 failures, 1839 s;
- `docs_check.py`, `check_em_dash.py --base e6172750`, `check_doc_style.py`, `pp_srcs.py --check`, `lint_rtl.py --check` (90 <= 90).

The render suite's inputs (`print-srcs`/`print-dp-vflags`) are byte-identical to the base. Not run: the full sweep and yosys (no RTL); `act_ci.py` (no PR head).

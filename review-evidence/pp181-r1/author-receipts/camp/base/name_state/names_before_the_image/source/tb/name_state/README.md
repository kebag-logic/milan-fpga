# Complete saved-name inventory

This suite covers processor issue #170, saved-state lane 3. It exercises the
existing name writer through real SET_NAME and GET_NAME frames, the real NVM
port, retained media and reset. Milan v1.2 §5.3.13 requires the user names to
survive reset; IEEE 1722.1-2021 §7.4.17.1 and §7.4.18.2 define the 64-byte values
and name selectors. Milan v1.2 §5.3.12 keeps the IDENTIFY value volatile; the
CONTROL descriptor's name remains part of this inventory.

The production name path already implements eight-lane capture, framed
records and replay after image initialization. This suite extends the existing
five-name D3N proof to both fixed generated populations. It adds no product
port, parameter, register, name allocation or writable descriptor.

## Running

From the processor root:

```sh
make -j16 -C tb/name_state
python3 tb/name_state/mutants.py --jobs 2 --output /tmp/name-state-mutants
python3 tb/name_state/run.py --image /tmp/1x1.img.bin --aaf 1
python3 tb/name_state/run.py --image /tmp/8x8.img.bin --aaf 8
python3 tb/name_state/run.py --image /tmp/8x8.img.bin --aaf 8 --measure
```

Select the required simulation compiler with `VERILATOR` for make or
`--verilator` for either Python entry point. Builds and generated images live
in an external temporary directory; `--work` retains a normal run there.
The mutation output directory must be new; an existing one is refused before
anything runs. A compiler failure, crash or missing completion tally never
kills a mutant.

The normal run uses synthetic descriptor bodies with the fixed parent
populations below. They isolate the name path and are not shipping descriptor
models. Acceptance also runs the generated parent images through `--image`.
Both populations correspond to parent `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.
There, the builder's AEM overlay for `configs/endstation_ax7101_1x1_tdm8.yaml`
or `configs/endstation_ax7101_8x8.yaml` (`sw/builder/endstation_builder.py`),
packed by `avdecc/gen_aemi_image.py --overlay`, gives the 1x1 image (7,512
bytes, SHA-256
`4fc8d61582a965fe648abc0c15d0551153ff2b27f202d1fbc8319fbb4bdb396d`) and the
8x8 image (19,520 bytes, SHA-256
`d8296833b03fe12405e75fe6b9c9690abc968fa6c15b25e4f698c4010b8aa7bc`).

Geometry: every run, synthetic or generated, first builds the shared harness
with `DESC_NAME_ENTRIES_P` equal to the population's name count, 39 for 1x1
TDM8 and 107 for the 8x8 diagnostic. That is the capacity the parent binds
(`AEM_NAME_ENTRIES_C`), so the last ordinal is the name table's last entry.
The same population then runs again at 128 entries, the earlier observation
geometry, as an extra run. The harness's observation address is widened to
cover all lanes. Product parameters and ports stay as declared.

## Inventory and oracle

| Descriptor class | 1x1 TDM8 | 8x8 diagnostic |
| --- | ---: | ---: |
| ENTITY names | 2 | 2 |
| CONFIGURATION | 1 | 1 |
| AUDIO_UNIT | 1 | 1 |
| STREAM_INPUT, including CRF | 2 | 9 |
| STREAM_OUTPUT, including CRF | 2 | 9 |
| AVB_INTERFACE | 1 | 1 |
| CLOCK_SOURCE | 3 | 10 |
| AUDIO_CLUSTER | 25 | 72 |
| CONTROL | 1 | 1 |
| CLOCK_DOMAIN | 1 | 1 |
| Total | 39 | 107 |

The C++ oracle enumerates descriptor type, index and semantic name index from
this population, independently of the image directory and RTL. Descriptor
order determines each ordinal. Its independently encoded expected record
contains the complete eight-byte frame and 64-byte name at `0x80 + ordinal`.
Full-length values are distinct for every ordinal of the 1x1 population; the
pattern repeats with period 90, so in the 8x8 diagnostic ordinals 90–106
repeat the values of ordinals 0–16, and only each saved frame's record ID and
CRC distinguish them. Every seventh ordinal beginning at two receives an empty
name. Both ENTITY selectors and the final ordinal are always exercised.
Factory values alone are read from the image name table, for reset
comparison.

## Checks and negative controls

Each run of the 1x1 population contains 173 checks and each run of the 8x8
population 445. The normal run executes both populations at their bound
capacity and again at 128 entries, 1,236 checks in total. N0, the
boot/terminal checks and N9's first check establish their premises. Existing
processor suite expectations are unchanged.

| Check | Observable assertion | Planted defect |
| --- | --- | --- |
| N1 | GET_NAME returns each image default | `image_names_zeroed` |
| N2 | SET_NAME and GET_NAME preserve all 64 bytes | `live_name_lane_dropped` |
| N3 | Every saved frame matches its ordinal/name oracle | `TRG_name`, `name_record_id_shifted`; `name_table_last_entry_dropped` at the last ordinal (38 at 39 entries, 106 at 107) |
| N4 | Every entry is reset to its image default before replay | `image_names_zeroed`, `names_before_the_image` |
| N5 | GET_NAME returns every saved value after reset | `RPL_name`, `name_entry_shifted`, `name_empty_refused`, `name_lanes_partial` |
| N6 | Completing the first record keeps the last name's saved value | `pending_clears_other_name` |
| N7 | Every WRITE contains one coherent eight-lane name and retains the latest value | `latch_ignores_program` |
| N8 | CONTROL name survives the same reset that clears its IDENTIFY value | `identify_survives_reset` |
| N9 | After a late descriptor burst outlasts the roll-back minimum, every name is at its image default, READ_DESCRIPTOR serves the image ENTITY names and a later SET_NAME saves | `rollback_ignores_debt` |
| D3N5 | Failed restoration returns the name to its image default | `store_not_rolled_back` |
| D3N6 | A change after capture is retained in the next complete record | `name_taint_ignored` |
| D3N7 | Late image initialization precedes replay and preserves the saved name | `names_before_the_image` |

N7 measures the fourth lane's phase in a repeated SET, then moves a following
SET across the first change's debounce expiry. It compares every WRITE,
including the first; a later retry cannot hide mixed old/new lanes.
N6 places changes at opposite ends of the population before either completes.
The three D3N arms retain the existing wire-level rollback, taint and healing
checks. N9 saves every name and seeds a rate record whose AUDIO_UNIT fetch
answers 16,000 clocks late. Pass 1 aborts (cause 6), and only the descriptor
debt holds both stores in reset until the abandoned burst arrives. N9 grades
that protection on name values; lane 1's debt timing (D3R10) and
volatile-state checks remain in `pp_top`.

The campaign reuses twelve existing defect definitions and plants four further
controls. It grades each against the named value assertion above, after a
passing full golden run at both bound capacities. Every control is graded in
the 1x1 population at 39 entries; `name_table_last_entry_dropped` is graded
there and in the 8x8 population at 107 entries, and must fail in both. An
assertion ending in an ordinal matches that ordinal alone. It reads source
only to construct isolated builds and plant exact edits; expected name values
never come from source text.

## Timing and scope

`--measure` reports accepted restore start to terminal, longest binding and
D3 waits, and longest D3 record operation. It measures all names, late image
loading and failure on the last name's pass-1 header, at descriptor latencies
of 31 and 143 clocks, at the bound capacity and then at 128 entries. The NVM
model transfers one byte per cycle.
The bench retains the top's derived 20 ms per-wait and 1,000 ms aggregate
deadlines at 1,000,001 Hz. Printed timings are model measurements, not new
deadline constants or a hardware service guarantee.

Window completion transfers producer ownership; it does not prove a durable
flash slot. Parent adoption, physical cold-cycle evidence and lane 5's combined
fault campaign retain their separate acceptance. The 8x8 run is diagnostic
and does not establish shipping fit or placed timing.

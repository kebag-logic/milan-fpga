# Saved-state format for shapes up to 32x32

Status: **ruled; the record space and framing implemented for the split placement** (#823).
Decisions 1 to 7 were ruled as recommended ([round 2](https://github.com/kebag-logic/milan-fpga/issues/823#issuecomment-6730773797)).
The [round 3 ruling](https://github.com/kebag-logic/milan-fpga/issues/823#issuecomment-6730985093) scopes them to the split placement.
Section 4, the append-only save path (decisions 3, 4, 5 and 7), is designed here and built under #876.
Until then the split store saves by the whole-image commit (section 3).

**The format is the split placement's.**
The 32x32 shape is split-only, and the processor goes away in Mark II.
So the F1 store (`sw/firmware/ctrl_nvm`) carries layout 3 and KLJ3.
**The all-fabric placement keeps KLJ2** and today's limits: the processor, `KL_nvm_backend` and `milan_baremetal.c` are unchanged.

The Mark II target is 32x32 streams (#640): 16x16 logical streams, each redundant on two networks.
The [#859 census](https://github.com/kebag-logic/milan-fpga/issues/859#issuecomment-6727746272) found the saved-state format blocks that shape.
This page sizes the format for every shape up to 32x32 with two interfaces, for the TDM8 cluster model.
The owner's bound is a save of at most 0.5 s, worst case, from the change to durable in flash ([#823](https://github.com/kebag-logic/milan-fpga/issues/823#issuecomment-6545924397)).

Every figure on this page is recomputed from the tree:

- [`scripts/nvm_format_32x32.py`](../../scripts/nvm_format_32x32.py) builds the shapes and does the arithmetic.
- [`scripts/check_nvm_format_32x32.py`](../../scripts/check_nvm_format_32x32.py) fails when a figure here drifts.
- A table between `nvm-format` markers is generated; so is each number marked `fig`.

## Contents

- **[1. The shapes and the two name models](#1-the-shapes-and-the-two-name-models)** -- The four sizing points as the builder builds them, and why #823's name count and the census's differ.
- **[2. The record space](#2-the-record-space)** -- The derived allocation: every block, its first and last id and its count rule, the id width, and the packed alternative.
- **[3. The image, the slot and the window](#3-the-image-the-slot-and-the-window)** -- The byte arithmetic at each point, the derived slot and journal, the ppmem window and the F1 stage.
- **[4. The save path and its 0.5 s bound](#4-the-save-path-and-its-05-s-bound)** -- The append-only journal, designed here and built under #876: its rules, the worst case from datasheet maxima, the assumptions it needs and the deadlines.
- **[5. Compatibility and the VERSION chain](#5-compatibility-and-the-version-chain)** -- Refusing today's journal with a recorded reason, the import alternative, and the container, layout and VERSION steps.
- **[6. Every layer that carries record_id](#6-every-layer-that-carries-record_id)** -- Every layer by file and the line's own text, what it holds today and its change, each checked by the gate.
- **[7. Area and timing risk, ESTIMATE](#7-area-and-timing-risk-estimate)** -- The fabric backend's change at each point, labelled as an estimate for round 2 to measure.
- **[8. Test plan](#8-test-plan)** -- The issue's tests, one rule per row, each with the planted mutant that must be caught.
- **[9. Decisions ruled](#9-decisions-ruled)** -- The seven decisions as ruled, the split placement they apply to, and the gateware VERSION, not moved, as ruled.
- **[10. Reproduce](#10-reproduce)** -- The commands that recompute and check every figure on this page.

## 1. The shapes and the two name models

The page sizes the format at four points.
Each is built by `sw/builder/endstation_builder.py`, never assumed:

- **1x1/1if** is `configs/endstation_ax7101_1x1_tdm8.yaml`, the shipping shape.
- **8x8/2if** is `configs/endstation_ax7101_8x8.yaml`.
- **32x32/2if** is the 8x8 config with 32 listener and 32 talker rows: the census's shape.
- **32x32/2if TDM8** is the 1x1 TDM8 config with 32 rows of each: #823's model, and the bound.

The two 32x32 points are built with three builder limits lifted in memory, as the census did.
They are the 16-stream cap (<!-- fig:lift_stream_cap -->16<!-- /fig -->), the 5-bit SRP row index (<!-- fig:lift_srp_bits -->5<!-- /fig --> bits) and the NAME capacity (<!-- fig:lift_name_capacity -->128<!-- /fig -->).
Each lift first reads its limit, so a moved limit refuses the run.
The interface count changes no saved record: the model has one AVB_INTERFACE either way.

<!-- nvm-format: begin points -->
| Quantity | 1x1/1if | 8x8/2if | 32x32/2if | 32x32/2if TDM8 |
|---|---:|---:|---:|---:|
| AAF streams per direction | 1 | 8 | 32 | 32 |
| STREAM_INPUT / STREAM_OUTPUT | 2 / 2 | 9 / 9 | 33 / 33 | 33 / 33 |
| STREAM_PORT_INPUT / OUTPUT | 1 / 1 | 8 / 8 | 32 / 32 | 32 / 32 |
| AUDIO_CLUSTER | 25 | 72 | 288 | 800 |
| CLOCK_SOURCE | 3 | 10 | 34 | 34 |
| Clusters per input port | 8 | 0 | 0 | 8 |
| Clusters per output port | 17 | 9 | 9 | 17 |
| Map entries per output port | 17 | 72 | 264 | 264 |
| Descriptors | 42 | 124 | 460 | 972 |
| Writable names, the builder's count | 39 | 107 | 395 | 907 |
| Writable names, the AEMI header | 39 | 107 | 395 | refused |
| Descriptor image bytes | 7,512 | 19,520 | 69,488 | refused |
<!-- nvm-format: end points -->

The 32x32 TDM8 overlay builds, but its descriptor image does not.
The packer refuses an AEM ROM of <!-- fig:t32_rom_bytes -->87,545<!-- /fig --> B against its <!-- fig:rom_space_bytes -->65,536<!-- /fig --> B store.
That limit is outside #823, which sizes the record space for this model anyway, as the assignment asks.

### Which name model the builder uses

The builder uses neither formula.
It counts the writable names of the exact model it builds: one plus every named descriptor (`def aem_name_count(` in `sw/builder/endstation_builder.py`).
The two formulas are that count for two config families:

<!-- nvm-format: begin rule -->
| Family | N: names, as built | Rule | First refusal, names |
|---|---|---|---:|
| `endstation_ax7101_1x1_tdm8` rows | 1: 39, 2: 67, 3: 95, 4: 123 | 11 + 28 x N | 151 |
| `endstation_ax7101_8x8` rows | 1: 23, 2: 35, 4: 59, 8: 107, 9: 119 | 11 + 12 x N | 131 |
<!-- nvm-format: end rule -->

- **#823's <!-- fig:t32_names -->907<!-- /fig -->** is the TDM8 family: <!-- fig:tdm8_const -->11<!-- /fig --> + <!-- fig:tdm8_per_stream -->28<!-- /fig --> per stream pair.
  Each listener port carries <!-- fig:t32_in_cl -->8<!-- /fig --> physical clusters, and each talker port <!-- fig:t32_out_cl -->17<!-- /fig -->: a pilot, 8 physical and 8 loopback.
- **The census's <!-- fig:p32_names -->395<!-- /fig -->** is the 8x8 family: <!-- fig:census_const -->11<!-- /fig --> + <!-- fig:census_per_stream -->12<!-- /fig --> per pair.
  That board routes no physical audio, so a listener port carries no cluster (the L1 waiver, until #584) and a talker port <!-- fig:p32_out_cl -->9<!-- /fig -->.
- The difference is <!-- fig:per_stream_diff -->16<!-- /fig --> clusters per stream pair.
  #584 adds input clusters to the 8x8 family, so its count grows toward the TDM8 one.

## 2. The record space

**Decision 1, ruled: one derived allocation, sized by the bound shape.**
Each block holds the bound shape's count for its group, in today's order.
The ids are the same for every shape, so a decoder's bases are constants.

<!-- nvm-format: begin space -->
| Block | Count rule | Sized by | First id | Last id | Ids |
|---|---|---|---:|---:|---:|
| CFG_IDX | 1 | singleton | 0 | 0 | 1 |
| SUID | 1 | singleton | 1 | 1 | 1 |
| RATE | AUDIO_UNIT | the backend's bound | 2 | 9 | 8 |
| CLKSRC | CLOCK_DOMAIN | the backend's bound | 10 | 17 | 8 |
| MCR | CLOCK_DOMAIN | the backend's bound | 18 | 25 | 8 |
| BINDING | STREAM_INPUT | the bound shape | 26 | 58 | 33 |
| FMT_IN | STREAM_INPUT | the bound shape | 59 | 91 | 33 |
| FMT_OUT | STREAM_OUTPUT | the bound shape | 92 | 124 | 33 |
| PT_OFS | STREAM_OUTPUT | the bound shape | 125 | 157 | 33 |
| MAPS_IN | STREAM_PORT_INPUT | the bound shape | 158 | 189 | 32 |
| MAPS_OUT | STREAM_PORT_OUTPUT | the bound shape | 190 | 221 | 32 |
| NAME | writable names | the bound shape | 222 | 1,128 | 907 |
| **all** | 11-bit id |  | 0 | 1,128 | 1,129 |
<!-- nvm-format: end space -->

- The record id needs <!-- fig:id_bits -->11<!-- /fig --> bits for <!-- fig:ids_total -->1,129<!-- /fig --> ids.
  The F07.8 header carries it in a <!-- fig:rid_field_bits -->16<!-- /fig -->-bit field (section 5).
- RATE, CLKSRC and MCR keep the backend's present bounds of <!-- fig:au_max -->8<!-- /fig --> and <!-- fig:cd_max -->8<!-- /fig -->, read from `g_refuse_units`.
- The NAME block runs from id <!-- fig:name_first -->222<!-- /fig --> to <!-- fig:name_last -->1,128<!-- /fig -->.
- No 8-bit allocation can hold 32x32: the census shape needs <!-- fig:p32_records -->596<!-- /fig --> records, the bound <!-- fig:t32_records -->1,108<!-- /fig -->.

<!-- nvm-format: begin ids -->
| Quantity | 1x1/1if | 8x8/2if | 32x32/2if | 32x32/2if TDM8 |
|---|---:|---:|---:|---:|
| Records | 54 | 164 | 596 | 1,108 |
| Highest id, derived space | 260 | 328 | 616 | 1,128 |
| Records within today's 256 ids | yes | yes | no | no |
| Inside the derived space | yes | yes | yes | yes |
<!-- nvm-format: end ids -->

**One declaration, two readers.**
The block sizes are stated once, in `sw/firmware/ctrl_nvm/nvm_layout3.h`.
Each base is the sum of the capacities before it.
- **The F1 store's codec** compiles it, and refuses at compile time a shape whose count outgrows a block.
- **The builder's split output** reads it through `scripts/nvm_layout3.py`: `emit_nvm_split` writes `nvm_split.json` beside the overlay and refuses a model over any block.
- The split SoC (`milan_soc.py --ctrl-mailbox`) and the F1 host bench build the store from that file.

The gate fails when the declaration is not the table above, as the builder derives it from the bound shape.
The bound shape fills every stream block and the NAME block exactly.

The split reads no RTL `$error` for this space: its store is firmware.
The all-fabric placement keeps its own bounds.
`KL_nvm_backend` still refuses above <!-- fig:lift_name_capacity -->128<!-- /fig --> names, and the builder's shape header with it (`def nvm_name_capacity(` in `sw/builder/endstation_builder.py`).
The builder's <!-- fig:lift_stream_cap -->16<!-- /fig -->-stream cap stays too: it is a #859 census limit, not this format's.

**The alternative not taken: a packed allocation per shape.**
Blocks would hold only the shape's own counts, so the 1x1 would keep <!-- fig:p1_records -->54<!-- /fig --> ids below 256.
Bases would then vary with the shape, and every producer would take them as parameters.

## 3. The image, the slot and the window

<!-- nvm-format: begin image -->
| Quantity | 1x1/1if | 8x8/2if | 32x32/2if | 32x32/2if TDM8 |
|---|---:|---:|---:|---:|
| Fixed groups, framed | 266 | 770 | 2,498 | 2,498 |
| Input maps, framed | 72 | 64 | 256 | 2,304 |
| Output maps, framed | 144 | 4,672 | 67,840 | 67,840 |
| Names, framed | 2,808 | 7,704 | 28,440 | 65,304 |
| Record area, 8-byte headers | 3,290 | 13,210 | 99,034 | 137,946 |
| KLJ2 image today | 3,336 | 13,256 | 99,080 | 137,992 |
| Share of one 64 KiB slot | 5% | 20% | 151% | 211% |
| Largest payload (cap 1,024) | 136 | 576 | 2,112 | 2,112 |
| Record area, 10-byte headers | 3,398 | 13,538 | 100,226 | 140,162 |
| Base segment | 3,444 | 13,584 | 100,272 | 140,208 |
| Base segment, pages | 14 | 54 | 392 | 548 |
<!-- nvm-format: end image -->

Three things this arithmetic shows:

- **Output maps dominate at 32x32.**
  They are <!-- fig:p32_maps_out_pct -->69<!-- /fig -->% of the census record area and <!-- fig:t32_maps_out_pct -->49<!-- /fig -->% of the bound's.
  Each output port reserves every stream-channel key (the #501 decision), so the group grows as ports times keys.
- **The largest payload is <!-- fig:t32_max_payload -->2,112<!-- /fig --> B**, one output map at 32x32.
  The port refuses any payload over its <!-- fig:max_payload_cap -->1,024<!-- /fig --> B default, so `MAX_PAYLOAD_P` must be derived too (section 6).
- **No <!-- fig:slot_now_kib -->64<!-- /fig --> KiB slot holds 32x32.**
  The census image is <!-- fig:p32_klj2_pct -->151<!-- /fig -->% of a slot, the bound's <!-- fig:t32_klj2_pct -->211<!-- /fig -->%.

### The slot: derived size, no compact name encoding

**Decision 3, ruled: derive the slot size, and keep names at 64 bytes.**

- A compact name encoding cannot lower the worst case.
  Every writable name may hold all 64 octets (IEEE 1722.1-2021 SET_NAME), and Milan 5.3.13 persists each one.
- A compact map encoding could: one owner per output key bounds all ports together to one port's keys (`owner register only ever holds` in `hdl/milan/milan_datapath.sv`).
  It would reverse #501's per-port capacity, so this page leaves it as an alternative (decision 3).

The slot holds a base image and an append log (section 4).
Its size is the smallest erase-block count holding twice the bound's base:

<!-- nvm-format: begin slot -->
| Item | Value | Rule |
|---|---|---|
| Erase blocks per slot | 5 | smallest count holding twice the bound's base |
| Slot | 320 KiB | today 64 KiB |
| Log after the bound's base | 732 pages | at least one base |
| Compaction reserve | 366 pages | half the log |
| Journal, two slots | 640 KiB | today 128 KiB |
| New journal | 14,592 to 15,232 KiB | directly below today's |
| Free flash below it | 10,432 KiB | after the AEM slot |
<!-- nvm-format: end slot -->

The new journal sits directly below today's, as `journal_klj3` in `FLASHBOOT_RESERVED` (`"journal_klj3": {"offset": 0xE4_0000` in `sw/litex/milan_soc.py`).
That is the flash map's one source, so every build reserves it.
Today's <!-- fig:old_journal_kib -->128<!-- /fig --> KiB journal is never written by the split store, so an all-fabric image still finds its own after a rollback.

**The journal is placed; the append path fills its log, under #876.**
The F1 store's two slots are the journal's halves.
Its whole-image commit is unchanged: it erases the blocks its container spans, from the slot's first, then programs and verifies.
At the shipped shapes that is one block, as today.

### The ppmem window and the F1 stage

This subsection is the all-fabric placement's, which keeps KLJ2: nothing in it is implemented.
The all-fabric window keeps two sub-windows below the response buffer: the live image and the private stage.
Each would grow from <!-- fig:sub_now_kib -->64<!-- /fig --> KiB to <!-- fig:sub_new_kib -->192<!-- /fig --> KiB, the bound's base rounded to erase blocks.
The <!-- fig:window_kib -->1,024<!-- /fig --> KiB window would then leave <!-- fig:desc_room -->651,264<!-- /fig --> B for the descriptor image.

<!-- nvm-format: begin window -->
| Quantity | 1x1/1if | 8x8/2if | 32x32/2if | 32x32/2if TDM8 |
|---|---:|---:|---:|---:|
| Descriptor image | 7,512 | 19,520 | 69,488 | refused |
| Base fits today's 64 KiB sub-window | yes | yes | no | no |
| Window use, proposal | 404,824 | 416,832 | 466,800 | -- |
| F1 stage today | 3,344 | 13,264 | 99,088 | 138,000 |
| F1 stage, proposal | 402 | 842 | 2,378 | 2,378 |

Today the window holds the image plus 135,168 B; the proposal, plus 397,312 B, of 1,048,576 B.
<!-- nvm-format: end window -->

The split's F1 store has no DDR3, so its stage is block RAM (#640 D4).
Until the append path it holds the whole container, now KLJ3: its ten-byte headers add two bytes a record.
In KLJ2 that was <!-- fig:p32_f1_stage_now -->99,088<!-- /fig --> B at the census shape.
The append needs only one page and one record, <!-- fig:t32_f1_stage_new -->2,378<!-- /fig --> B at 32x32.
Compaction streams record by record from the owners, so it needs no more.

## 4. The save path and its 0.5 s bound

**This section is designed here and built under #876.**
Its rules, its worst case and its deadlines are the ruled design.
The split store at this format still saves by the whole-image commit.

**The journal.** A slot is a log of segments, each starting on a page.

- Segment 0 is the **base**: every record of the shape, as one KLJ container.
- Every later segment is a **delta**: only changed records, with the next sequence number.
- Each segment carries the container header, KLJ3 in the split, and closes with its own CRC-32 trailer.
  The trailer is the commit mark, as it is today.
- A record's latest closing segment holds its value.
- The live window keeps today's layout, every record at its derived offset.
  Only the flash copy becomes a log; firmware replays it into the window at boot.

**The rules.** They carry FASTCONNECT's A/B guarantee over to appends:

1. A save appends one delta to the authoritative slot. It never erases.
2. A boot walks the base, then each delta whose CRC closes, in sequence order. It stops at the first that does not.
3. After a boot that found a torn delta, the next write is a compaction. Nothing appends past a torn segment.
4. **Compaction** writes a fresh base into the other slot. Authority moves only when that base verifies with a higher sequence.
5. Compaction yields to a save between pages. A record changed after its copy is appended to the new slot.
6. The old slot is erased in the background after the move, one erase block at a time.
7. A save that arrives during an erase **suspends** it, programs, then resumes it.
8. A save never waits for compaction while the active slot keeps its reserve.

A power cut at any page of an append leaves the last closing delta authoritative.
A cut during compaction leaves the old slot authoritative, with every delta it holds.
So nothing durable is lost, which is the owner's condition for compaction.

### The worst case at 32x32, from datasheet maxima

The figures are the N25Q128 maxima the tree already cites (`Micron N25Q128 Table 32` in `scripts/nvm_contract.py`): tSE <!-- fig:t_se_s -->3<!-- /fig --> s per <!-- fig:slot_now_kib -->64<!-- /fig --> KiB block, tPP <!-- fig:t_pp_ms -->5<!-- /fig --> ms per page.
Every SPI byte costs 8 clocks at <!-- fig:spi_mhz -->12.5<!-- /fig --> MHz on the 1x link (`clk_freq=int(12.5e6)` in `sw/litex/milan_soc.py`).
Unlike FASTCONNECT section 9.4, this counts the command and page bytes on the link too.
The bound is graded at the AX7101's part; the Arty's S25FL128S has no maxima in the tree (`S25FL128S(SpiCodes.READ_1_1_1)` in `sw/litex/milan_soc.py`).

<!-- nvm-format: begin save -->
| Term | Value | Source |
|---|---|---|
| Producer first-dirty window | 100 ms | today 500 ms |
| Firmware first-dirty window | 150 ms | today 1,000 ms |
| One page programmed | 5.168 ms | tPP 5 ms, and 263 B on the 1x link |
| One page read back | 0.166 ms | 260 B on the 1x link |
| One page, both | 5.335 ms |  |
| Segment cap | 28 pages | a segment ends before the next window |
| Records per segment | 7,124 B | less the 44-byte frame |
| Ahead of it: one compaction page | 5.335 ms | compaction yields per page |
| The segment itself | 149.37 ms |  |
| **Worst case, all-fabric** | **404.71 ms** + suspend | both windows |
| **Worst case, split** | **304.71 ms** + suspend | firmware window only |
| Room left for the suspend latency | 95.29 ms | not in the tree |
| Without erase suspend | 3,399.37 ms | tSE 3,000 ms ahead |
<!-- nvm-format: end save -->

**The windows.** The bound runs from the change, so the first-dirty windows count.
DR2a, in the [materialization register](SAVED_STATE_MATERIALIZATION.md#151-manager-decision-register), rules them at <!-- fig:prod_window_now_ms -->500<!-- /fig --> ms in each producer and <!-- fig:fw_window_now_ms -->1,000<!-- /fig --> ms in firmware.
Together they already exceed the bound, before any flash work.
This page proposes <!-- fig:w_prod_ms -->100<!-- /fig --> ms and <!-- fig:w_fw_ms -->150<!-- /fig --> ms (decision 4).

**The segment cap.** A segment holds at most <!-- fig:p_cap -->28<!-- /fig --> pages, so it ends inside one firmware window.
A change then never waits for an earlier segment, only for the page in flight.

**The erase.** Without erase suspend a save can land behind a whole tSE: <!-- fig:no_suspend_ms -->3,399.37<!-- /fig --> ms.
With it, the bound holds if the suspend latency stays under <!-- fig:susp_allow_ms -->95.29<!-- /fig --> ms.
Assumption A3 below grades it.

<!-- nvm-format: begin limits -->
| Case | Value | Basis |
|---|---|---|
| One name alone | 5.335 ms | 74 B record, one page |
| The largest record alone | 48.01 ms | 2,122 B output map, 9 pages |
| Names in one segment | 96 | 7,124 B |
| Largest records in one segment | 3 | 7,124 B |
| Compaction at the bound | 2,923.43 ms | off the save path |
| Background erase of one slot | 15 s | 5 x tSE 3 s |
| Sustained save volume | 24.4 pages/s | 6,246 B/s, assumption A2 |
| Boot read, both slots once | 419.43 ms | 1x link |
| Boot read, three reads each | 1,258.29 ms | FASTCONNECT section 7, two of three reads |
<!-- nvm-format: end limits -->

The bound holds under three stated assumptions:

- **A1.** The records dirty when a window closes fit one segment: <!-- fig:cap_bytes -->7,124<!-- /fig --> B.
  That is <!-- fig:names_per_save -->96<!-- /fig --> names or <!-- fig:bigs_per_save -->3<!-- /fig --> of the largest maps. A larger burst drains at the flash's rate.
- **A2.** Averaged over a compaction and the following erase, saves fill at most the reserve: <!-- fig:rate_pages_s -->24.4<!-- /fig --> pages a second.
  Past that, a save waits for compaction and is published pending, never lost.
- **A3.** The flash suspends an erase for a program in another block, within the room above.
  The part has erase suspend (N25Q128 datasheet, section 9.1.20 and Table 17).
  Its suspend latency is <!-- fig:susp_typ_us -->15<!-- /fig --> us **typical, with no maximum given**: the bound's one typical term, as ruled (#823).
  The split's worst save is then <!-- fig:split_typ_ms -->304.72<!-- /fig --> ms.
  The room, taken from the all-fabric worst case (<!-- fig:fabric_ms -->404.71<!-- /fig --> ms) and so conservative for the split, is <!-- fig:susp_allow_ms -->95.29<!-- /fig --> ms.
  So a suspend <!-- fig:susp_margin -->6,352<!-- /fig --> times its typical value would still fit.
  The writer that #876 builds times every suspend and reports a slow one.

No design meets the bound for an arbitrary burst.
At tPP <!-- fig:t_pp_ms -->5<!-- /fig --> ms the flash programs one page per <!-- fig:t_pp_ms -->5<!-- /fig --> ms, so a whole 32x32 rewrite takes seconds.

<!-- nvm-format: begin compaction -->
| Quantity | 1x1/1if | 8x8/2if | 32x32/2if | 32x32/2if TDM8 |
|---|---:|---:|---:|---:|
| Base segment, pages | 14 | 54 | 392 | 548 |
| Compaction, ms | 74.69 | 288.07 | 2,091.21 | 2,923.43 |
| Today's whole-image commit, ms | 3,072.14 | 3,268.48 | 5,003.41 | 5,788.31 |
<!-- nvm-format: end compaction -->

Today's whole-image commit is <!-- fig:t32_commit_now_ms -->5,788.31<!-- /fig --> ms at the bound, so an append is the only way under 0.5 s.

### The deadlines, restated

- **`T-NVM-COMMIT-TIMEOUT`** applies to an append, the only transaction on the save path.
  It must cover twice the worst append, <!-- fig:commit_min_ms -->309.41<!-- /fig --> ms.
  This page proposes <!-- fig:commit_timeout_ms -->500<!-- /fig --> ms, the bound itself, against today's <!-- fig:commit_now_ms -->8,000<!-- /fig --> ms.
- Today's <!-- fig:commit_now_ms -->8,000<!-- /fig --> ms would not cover two whole commits at 32x32 either: twice <!-- fig:t32_commit_now_ms -->5,788.31<!-- /fig --> ms is over it.
- Compaction and the background erase carry no durability claim, so no commit deadline applies to them.
  `T-NVM-WRITER-ALIVE` still supervises them: the heartbeat is serviced from the same poll loop.
- The same bound and deadline apply to the F1 store (#665).

A boot reads both slots at most three times each, FASTCONNECT section 7's rule: <!-- fig:boot_all_ms -->1,258.29<!-- /fig --> ms.
A boot that finds a torn delta also owes one compaction before its next append.

## 5. Compatibility and the VERSION chain

**Decision 2, ruled and implemented in the split's store: refuse today's journal and boot blank, with the reason recorded.**

- A KLJ2 container is refused with `VD_VER` and never reinterpreted, as KLJ1 was (FASTCONNECT section 6.2).
  The F1 codec recognises the KLJ2 magic before it reads anything else.
- The split store never writes today's journal: its port refuses a program or erase outside `journal_klj3`.
  So a rollback to an all-fabric image finds its journal intact.
- At boot the store reads the two headers of today's journal.
  A KLJ2 header sets its bit in the status field `legacy`.
  When the store's own slots are blank, the boot's verdict is `VD_VER`, not `VD_BLANK`.
- A read of today's journal that fails records nothing: that journal is never the split store's authority.
- The cost is one lost saved state per upgraded board: it boots unbound, as from blank flash.

**The alternative not taken: import today's journal once.**
Both writers would keep a KLJ2 decoder and an id translation for one boot.

**The VERSION chain step.**

- The container's magic becomes `KLJ3` and its `FMT_VER` major 3; acceptance rule 3's cap becomes the slot. Done.
- A KLJ2 header in either journal is recognised as the previous format, hence `VD_VER`. Done.
- F07.8 `layout_version` goes from 2 to 3: a <!-- fig:rec_hdr_bytes -->10<!-- /fig -->-byte header with a 16-bit `record_id`. Done.
- **The gateware VERSION is not moved, as ruled (#823).**
  It stays at minor <!-- fig:version_minor -->96<!-- /fig -->.
  The VERSION step is the format's own chain, above, which is done.
  This format changes no gateware, and the all-fabric placement must stay unchanged.
  [The split architecture's section 7](../ARCHITECTURE_HW_SW_SPLIT.md#7-version-and-default-flip) binds VERSION to the placement an image runs.
  VERSION 3 lands with the default flip, with these five assertions:

<!-- nvm-format: begin version -->
| Assertion | File | Line carrying |
|---|---|---|
| CSR | `hdl/common/csr/milan_csr.sv` | `VERSION = 32'h0002_0060` |
| CSR suite | `tb/verilator/csr/sim_main.cpp` | `0x00020060` |
| Datapath | `tb/verilator/milan_dp/sim_main.cpp` | `0x00020060` |
| Every stream shape | `tb/verilator/milan_dp/sim_nxn.cpp` | `0x00020060` |
| gPTP option | `tb/verilator/milan_dp/sim_gptp.cpp` | `0x00020060` |
| Pruning | `tb/verilator/milan_dp/sim_prune.cpp` | `0x00020060` |
<!-- nvm-format: end version -->

## 6. Every layer that carries record_id

Each row cites a file and a token that only one of its lines carries.
The gate fails when the token is gone or on more than one line.
It cites no line number, so an edit that moves the line leaves the row true.
The split's rows are what the split's format changed.
The all-fabric rows are unchanged: that placement keeps KLJ2.

<!-- nvm-format: begin layers -->
| Layer | File | Line carrying | Holds | Change |
|---|---|---|---|---|
| Declaration | `sw/firmware/ctrl_nvm/nvm_layout3.h` | `#define NVM3_CAP_NAME 907u` | NAME block, 907 ids | the one declaration, every block's capacity |
| Declaration | `sw/firmware/ctrl_nvm/nvm_layout3.h` | `#define NVM3_ID_SPACE (NVM3_ID_NAME` | 1,129 ids | bases chained from the capacities |
| F1 codec | `sw/firmware/ctrl_nvm/nvm_shape.h` | `#define NVM_REC_HDR    NVM3_REC_HDR` | 10-byte header | layout 3 |
| F1 codec | `sw/firmware/ctrl_nvm/nvm_shape.h` | `_Static_assert(MILAN_NVM3_N_NAME <= NVM3_CAP_NAME` | the NAME block's refusal | compile time, from the declaration |
| F1 codec | `sw/firmware/ctrl_nvm/nvm_shape.h` | `#define NVM_JOURNAL_OFFSET MILAN_FLASH_JOURNAL_KLJ3_OFFSET` | journal_klj3 | the 640 KiB journal |
| F1 codec | `sw/firmware/ctrl_nvm/nvm_shape.h` | `#define NVM_KLJ3_MAX       NVM_SLOT_BYTES` | container up to a slot | KLJ3 rule 3 |
| F1 codec | `sw/firmware/ctrl_nvm/nvm_klj2.c` | `static const uint16_t nvm_mapout_entries[NVM_MAP_PORTS]` | 32 ports, 16-bit counts | done |
| F1 codec | `sw/firmware/ctrl_nvm/nvm_klj2.c` | `if (nvm_rd32le(hdr) == NVM_KLJ2_MAGIC)` | KLJ2 refused `VD_VER` | decision 2 |
| F1 codec | `sw/firmware/ctrl_nvm/nvm_klj2.h` | `uint16_t id;` | 16-bit id | done |
| F1 store | `sw/firmware/ctrl_nvm/nvm_store.c` | `rec[4] == (uint8_t)(r.id >> 8)` | 16-bit id at bytes 4 and 5 | done |
| F1 store | `sw/firmware/ctrl_nvm/nvm_store.c` | `#define NVM_WORDS ((NVM_ID_SPACE + 31u) / 32u)` | open bits, 36 words | decision 6 |
| F1 store | `sw/firmware/ctrl_nvm/nvm_store.c` | `v->count++;` | the open records' count | decision 6 |
| F1 store | `sw/firmware/ctrl_nvm/nvm_store.c` | `nvm_legacy_check();` | today's journal read, never written | decision 2 |
| F1 store | `sw/firmware/ctrl_nvm/nvm_store.c` | `(++nvm.block < NVM_ERASE_BLOCKS)` | every block the container spans | the whole-image commit |
| F1 port | `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | `return addr >= NVM_JOURNAL_OFFSET &&` | writes only journal_klj3 | done |
| F1 link | `sw/litex/ctrl_memory.py` | `def stage_bytes(shape: object)` | stage = KLJ3 container | whole container until the append path |
| F1 link | `sw/litex/milan_soc.py` | `split_constants(_nvm_split, _nvm_shape)` | the split SoC's constants | from the builder's split output |
| F1 link | `sw/litex/milan_soc.py` | `"journal_klj3": {"offset": 0xE4_0000` | 640 KiB journal | below today's |
| Builder | `sw/builder/endstation_builder.py` | `def emit_nvm_split(` | nvm_split.json | refused over a layout 3 block |
| Scripts | `scripts/nvm_klj3.py` | `hdr = struct.pack(">HBBHH"` | 16-bit id frame | the split's reference |
| Scripts | `scripts/nvm_layout3.py` | `def read(` | the declaration's reader | done |
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv` | `HDR_LEN_C  = 16'd8` | 8-byte header | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv` | `[7:0]  nvm_record_id_i` | 8-bit record id in | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv` | `[7:0]  dev_region_o` | 8-bit region out | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv` | `MAX_PAYLOAD_P = 1024` | 1,024-byte payload cap | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv` | `REC_ID_BASE_P = 8'h20` | BINDING base 32 | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv` | `LAYOUT_VER_P  = 8'h02` | layout 2 | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv` | `DEB_TICKS_P   = 500` | 500 ms window | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv` | `function automatic logic [7:0] sel_base_f` | fixed bases 0, 2, 10, 48, 64, 80, 128 | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv` | `DEB_MS_P       = 500` | 500 ms window | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_mgr_arb.sv` | `[7:0]  m0_rid_i` | 8-bit ids, both managers | unchanged: the all-fabric placement keeps KLJ2 |
| F07.8 framing | `protocol-processor/hdl/top/protocol_processor_top.sv` | `[7:0]  nvm_dev_region_o` | 8-bit region at the top | unchanged: the all-fabric placement keeps KLJ2 |
| `dev_region_i` | `hdl/milan/KL_nvm_backend.sv` | `[7:0]  dev_region_i` | 8-bit region in | unchanged: the all-fabric placement keeps KLJ2 |
| `dev_region_i` | `hdl/milan/KL_pp_shadow.sv` | `logic [7:0]  pp_dev_region_w` | 8-bit wire to the backend | unchanged: the all-fabric placement keeps KLJ2 |
| `dev_region_i` | `hdl/milan/KL_pp_shadow.sv` | `[7:0]  mrec_region_i` | 8-bit map-writer id | unchanged: the all-fabric placement keeps KLJ2 |
| Backend decode | `hdl/milan/KL_nvm_backend.sv` | `ID_NAME_C  = 'h80` | fixed id blocks | unchanged: the all-fabric placement keeps KLJ2 |
| Backend decode | `hdl/milan/KL_nvm_backend.sv` | `REC_HDR_C = 8` | 8-byte header | unchanged: the all-fabric placement keeps KLJ2 |
| Backend decode | `hdl/milan/KL_nvm_backend.sv` | `logic [255:0]          open_r` | 256 ownership bits | unchanged: the all-fabric placement keeps KLJ2 |
| Backend refusals | `hdl/milan/KL_nvm_backend.sv` | `N_NAME_MAX_C = 128` | 128 names | unchanged: the all-fabric placement keeps KLJ2 |
| Backend refusals | `hdl/milan/KL_nvm_backend.sv` | `N_STREAM_IN_P > 16` | 16 streams per direction | unchanged: the all-fabric placement keeps KLJ2 |
| Map writer | `hdl/milan/milan_datapath.sv` | `amr_rid_w  = 8'h60 + 8'(p)` | ids 96 + port | unchanged: the all-fabric placement keeps KLJ2 |
| Map writer | `hdl/milan/milan_datapath.sv` | `debounce (DR2a,` | 500 ms window | unchanged: the all-fabric placement keeps KLJ2 |
| Firmware, shipping writer | `sw/firmware/milan_baremetal/milan_baremetal.c` | `NVM_ID_NAME  0x80u` | fixed id blocks | unchanged: the all-fabric placement keeps KLJ2 |
| Firmware, shipping writer | `sw/firmware/milan_baremetal/milan_baremetal.c` | `NVM_SLOT_BYTES (MILAN_FLASH_JOURNAL_SIZE / 2u)` | two 64 KiB slots | unchanged: the all-fabric placement keeps KLJ2 |
| Builder | `sw/builder/endstation_builder.py` | `if len(lst) > 16:` | 16 streams per direction | kept: a #859 census limit, not this format's |
| Builder | `sw/builder/endstation_builder.py` | `if aem_name_entries > capacity:` | 128 names, the all-fabric shape header | unchanged: the all-fabric placement keeps KLJ2 |
| Builder | `sw/builder/endstation_builder.py` | `"nvm_base": base +` | 64 KiB sub-windows | unchanged: the all-fabric placement keeps KLJ2 |
| Scripts | `scripts/nvm_contract.py` | `ALLOC = {` | layout 2's fixed blocks | unchanged: the all-fabric placement keeps KLJ2 |
| Scripts | `scripts/nvm_klj2.py` | `struct.pack(">HBBH"` | 8-bit id frame | unchanged: the all-fabric placement keeps KLJ2 |
| Mailbox contract | `sw/mailbox/mailbox.yaml` | `bound_talkers: 16` | 16 bound talkers, as the BINDING block | a #859 decision, not this format |
<!-- nvm-format: end layers -->

The mailbox row is not this format's to change.
Its 16 bound talkers follow the BINDING block today, and the census puts its tables under its own decision.

## 7. Area and timing risk, ESTIMATE

**Every number in this section is an estimate, for the all-fabric placement's backend.**
That placement keeps KLJ2, so none of it is built; the section stays as the ruling's record.
In the split, decision 6's open bits are the F1 store's: two word arrays of 36 words at layout 3, each with a count of its bits set.
The store asks the count, not the words, whether any record is open.
Area under #818's gate is waived for this format, which changes no HDL, gitlink or generated SoC RTL ([round 6 ruling](https://github.com/kebag-logic/milan-fpga/pull/863#issuecomment-6767385787)).
Its area evidence is [the split memory plan](SPLIT_CONTROL_MEMORY.md#5-fit), 57.5 RAMB36 at the ledgered point.
The append path's memory is #876's.

- **At 1x1 and 8x8 the change is small.**
  The ownership vector keeps one bit per record: <!-- fig:p1_open_ff -->54<!-- /fig --> and <!-- fig:p8_open_ff -->164<!-- /fig -->, as today.
  Wider id compares, a 10-byte header and one more map index bit add about <!-- fig:width_lut -->40<!-- /fig --> LUT and <!-- fig:width_ff -->24<!-- /fig --> FF.
- **At 32x32 the ownership vector is the risk.**
  Flop-held, it is <!-- fig:t32_open_ff -->1,108<!-- /fig --> FF and about <!-- fig:t32_open_lut -->3,612<!-- /fig --> LUT at the bound.
  Held in distributed RAM with a count of open records, it is about <!-- fig:ram_open_lut -->100<!-- /fig --> LUT (decision 6).
- **The map tables stay in LUTRAM.** Thirty-two ports fit the same 32-deep cells as eight.
- The last measurement in the tree is <!-- fig:meas_8x8_lut -->993<!-- /fig --> LUT and <!-- fig:meas_8x8_ff -->313<!-- /fig --> FF at 8x8, LUT-only (FASTCONNECT section 8.3).

<!-- nvm-format: begin area -->
| Quantity | 1x1/1if | 8x8/2if | 32x32/2if | 32x32/2if TDM8 |
|---|---:|---:|---:|---:|
| Ownership bits, one per record | 54 | 164 | 596 | 1,108 |
| Ownership read words | 2 | 6 | 19 | 35 |
| ESTIMATE flop-held LUT, 3 per bit and the read mux | 194 | 556 | 1,948 | 3,612 |
| ESTIMATE OR-reduce depth, LUT6 levels | 3 | 3 | 4 | 4 |
| ESTIMATE read-mux depth, levels | 1 | 2 | 3 | 3 |
<!-- nvm-format: end area -->

Timing: the deepest new paths are the ownership OR-reduce and its read mux, both a few LUT levels.
The region decode adds only compare width, so its depth is unchanged.

## 8. Test plan

The issue's scope item 4, with one plant per rule.
Each plant is a mutant of the implementation that its test must catch.

<!-- nvm-format: begin tests -->
| # | Rule | Test | Plant that must be caught | State |
|---|---|---|---|---|
| T1 | NAME first id 222 | F1 `name_block_ends`; builder gate 39 pins it; the reference gate holds every id in its block | `name_base_moved`; a block before NAME grown | done, split |
| T2 | NAME last id 1,128 | F1 at 907 names: `name_block_ends`; `capacity_round_trip` over two erase blocks; `capacity_commit_over_stale`, a commit over an older container, each erase at its block's address | `name_last_dropped`; `first_block_only`; `erase_first_block_every_time` | done, split |
| T3 | NAME one past, 1,129 | F1 `one_past_refused` and the parity table, `VD_REC`; 908 names do not compile | `id_space_unbounded`; the NAME assert removed | done, split |
| T4 | Every other block | each block's first id read from the declaration; the reference gate's ledger at every shape | the last name left out of the reference's inventory | done, split |
| T5 | Capacity | builder gate 39: the 32x32 TDM8 overlay's 907 names accepted, one more refused; the all-fabric header still refuses it | capacity 906 and 908; the all-fabric bound read from the split's | done, split |
| T6 | Old journal on boot | F1 `klj2_journal_refused`, `klj2_in_slot_refused`, `klj2_journal_unreadable`: blank, `VD_VER` recorded, today's journal unwritten; `legacy_other_format_not_recorded`, `own_refusal_kept_over_legacy`; `klj2_journal_at_its_flash_map_address`, today's slots from the flash map | `klj2_not_recognised`, `klj2_reinterpreted`, `legacy_not_read`, `legacy_reason_dropped`, `legacy_any_nonblank_header`, `ver_overrides_own_refusal`, `legacy_b_wrong_place` | done, split |
| T7 | Append order | a delta over the base: the last value wins | segments applied in reverse | built under #876 |
| T8 | Torn append | a cut at every page restores the last closing segment | a segment accepted without its CRC | built under #876 |
| T9 | Torn compaction | a cut at every page boots the old slot, losing nothing | authority moved before the new trailer verifies | built under #876 |
| T10 | Erase in progress | a save during the background erase suspends it | the save waits for the erase | built under #876 |
| T11 | Save bound | model time, change to verified, at most 500 ms at 32x32 TDM8 | a 1,000 ms firmware window | built under #876 |
| T12 | Reserve exhausted | the save waits, is published pending and is not lost | the save dropped | built under #876 |
| T13 | Commit deadline | at least twice the worst append at every shape | a 300 ms deadline | built under #876 |
| T14 | Payload cap | the F1 store sizes its payload buffer from the shape (`NVM_PAYLOAD_MAX`) | none: the 1,024 B `MAX_PAYLOAD_P` is the processor's | all-fabric unchanged |
| T15 | Fit | the container within one slot, asserted at compile time; base and log | a two-block slot | built under #876 |
| T16 | VERSION | the format's chain: KLJ3 major 3, layout 3, KLJ2 `VD_VER` (`wrong_version_falls_back`, majors 2 and 4) | `no_version_check` | done, split; the gateware VERSION not moved, as ruled (#823) |
| T17 | Map entry widths | a count past the codec's table does not compile: 256 entries on an input port, 65,536 on an output port | either width assert removed | done, split |
<!-- nvm-format: end tests -->

Each done row names the F1 host suite's tests (`sw/firmware/ctrl_nvm/test`), builder gate 39 or the reference gate (`scripts/check_nvm_klj3.py`).
Each plant is planted by that suite's self-test.

## 9. Decisions ruled

The seven decisions were ruled as recommended, and the round 3 ruling scopes them to the split placement.

- **1. The record space:** the derived allocation of section 2, 11 bits in a 16-bit field. Implemented.
- **2. Compatibility:** refuse KLJ2 with `VD_VER`, boot blank, record the reason. Implemented.
- **3. The slot:** <!-- fig:sectors -->5<!-- /fig --> erase blocks, a <!-- fig:journal_kib -->640<!-- /fig --> KiB journal below today's. The journal is placed; its log is built under #876.
- **4. The windows:** <!-- fig:w_prod_ms -->100<!-- /fig --> ms producer and <!-- fig:w_fw_ms -->150<!-- /fig --> ms firmware first-dirty windows. Built under #876, for the split's firmware window.
- **5. The erase:** background erase with suspend, graded at the typical latency (A3). Built under #876.
- **6. Ownership:** open bits with a count. Implemented in the split's store.
- **7. The commit deadline:** <!-- fig:commit_timeout_ms -->500<!-- /fig --> ms for an append. Built under #876.

**The gateware VERSION: not moved, as ruled (#823)** (section 5).
VERSION 3 lands with the default flip.

## 10. Reproduce

```sh
python3 scripts/nvm_format_32x32.py
python3 scripts/nvm_format_32x32.py --blocks
python3 scripts/check_nvm_format_32x32.py
python3 scripts/check_nvm_format_32x32.py --self-test
python3 scripts/check_nvm_klj3.py --self-test
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test
python3 sw/builder/test_builder.py --gates test_split_record_space_bounds_the_split_output
```

After a change to a definition, `python3 scripts/check_nvm_format_32x32.py --write` regenerates every figure here.

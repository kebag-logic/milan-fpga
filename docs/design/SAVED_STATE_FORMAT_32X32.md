# Saved-state format for shapes up to 32x32

Status: **proposed, design only** (#823, round 1).
Nothing in the tree implements it, and nothing here changes RTL, firmware or the builder.
The choices are hard to reverse, so section 9 asks for a ruling first.

The Mark II target is 32x32 streams (#640): 16x16 logical streams, each redundant on two networks.
The [#859 census](https://github.com/kebag-logic/milan-fpga/issues/859#issuecomment-6727746272) found the saved-state format blocks that shape.
This page proposes the format for every shape up to 32x32 with two interfaces, sized for the TDM8 cluster model.
The owner's bound is a save of at most 0.5 s, worst case, from the change to durable in flash ([#823](https://github.com/kebag-logic/milan-fpga/issues/823#issuecomment-6545924397)).

Every figure on this page is recomputed from the tree:

- [`scripts/nvm_format_32x32.py`](../../scripts/nvm_format_32x32.py) builds the shapes and does the arithmetic.
- [`scripts/check_nvm_format_32x32.py`](../../scripts/check_nvm_format_32x32.py) fails when a figure here drifts.
- A table between `nvm-format` markers is generated; so is each number marked `fig`.

## Contents

- **[1. The shapes and the two name models](#1-the-shapes-and-the-two-name-models)** -- The four sizing points as the builder builds them, and why #823's name count and the census's differ.
- **[2. The record space](#2-the-record-space)** -- The derived allocation: every block, its first and last id and its count rule, the id width, and the packed alternative.
- **[3. The image, the slot and the window](#3-the-image-the-slot-and-the-window)** -- The byte arithmetic at each point, the derived slot and journal, the ppmem window and the F1 stage.
- **[4. The save path and its 0.5 s bound](#4-the-save-path-and-its-05-s-bound)** -- The append-only journal and its rules, the worst case from datasheet maxima, the assumptions it needs and the deadlines.
- **[5. Compatibility and the VERSION chain](#5-compatibility-and-the-version-chain)** -- Refusing today's journal with a recorded reason, the import alternative, and the container, layout and VERSION steps.
- **[6. Every layer that carries record_id](#6-every-layer-that-carries-record_id)** -- Every layer by file:line, what it holds today and its change, each line checked by the gate.
- **[7. Area and timing risk, ESTIMATE](#7-area-and-timing-risk-estimate)** -- The fabric backend's change at each point, labelled as an estimate for round 2 to measure.
- **[8. Test plan](#8-test-plan)** -- The issue's tests, one rule per row, each with the planted mutant that must be caught.
- **[9. Decisions requested](#9-decisions-requested)** -- The rulings the design needs before any implementation, each with its recommendation and its alternative.
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
It counts the writable names of the exact model it builds: one plus every named descriptor (`_adp_name_entries`, `sw/builder/endstation_builder.py:2714`).
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

**Recommendation: one derived allocation, sized by the bound shape.**
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
The block sizes are stated once, as RTL parameters beside today's `N_NAME_MAX_C`.
The builder reads them as it reads `N_NAME_MAX_C` today (`sw/builder/endstation_builder.py:2694`).
So the builder's refusal and the RTL `$error` bound by the same numbers.
The builder's <!-- fig:lift_stream_cap -->16<!-- /fig -->-stream cap becomes the BINDING block's size, less the CRF stream.

**Alternative: a packed allocation per shape.**
Blocks would hold only the shape's own counts, so the 1x1 would keep <!-- fig:p1_records -->54<!-- /fig --> ids below 256.
Bases would then vary with the shape, and every producer would take them as parameters.
That buys nothing a format change can keep: the new framing changes every shape's bytes anyway.

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

**Recommendation: derive the slot size, and keep names at 64 bytes.**

- A compact name encoding cannot lower the worst case.
  Every writable name may hold all 64 octets (IEEE 1722.1-2021 SET_NAME), and Milan 5.3.13 persists each one.
- A compact map encoding could: one owner per output key bounds all ports together to one port's keys (`hdl/milan/milan_datapath.sv:5211`).
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

The new journal sits directly below today's.
Today's <!-- fig:old_journal_kib -->128<!-- /fig --> KiB journal is never written, so the release image still finds its own after a rollback.
The region is stated in `FLASHBOOT_RESERVED` (`sw/litex/milan_soc.py:173`), the flash map's one source.

### The ppmem window and the F1 stage

The all-fabric window keeps two sub-windows below the response buffer: the live image and the private stage.
Each grows from <!-- fig:sub_now_kib -->64<!-- /fig --> KiB to <!-- fig:sub_new_kib -->192<!-- /fig --> KiB, the bound's base rounded to erase blocks.
The <!-- fig:window_kib -->1,024<!-- /fig --> KiB window then leaves <!-- fig:desc_room -->651,264<!-- /fig --> B for the descriptor image.

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
Today it holds the whole container: <!-- fig:p32_f1_stage_now -->99,088<!-- /fig --> B at the census shape.
An append needs only one page and one record, <!-- fig:t32_f1_stage_new -->2,378<!-- /fig --> B at 32x32.
Compaction streams record by record from the owners, so it needs no more.

## 4. The save path and its 0.5 s bound

**The journal.** A slot is a log of segments, each starting on a page.

- Segment 0 is the **base**: every record of the shape, as one KLJ container.
- Every later segment is a **delta**: only changed records, with the next sequence number.
- Each segment carries the KLJ2 header and closes with its own CRC-32 trailer.
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

The figures are the N25Q128 maxima the tree already cites (`scripts/nvm_contract.py:112`): tSE <!-- fig:t_se_s -->3<!-- /fig --> s per <!-- fig:slot_now_kib -->64<!-- /fig --> KiB block, tPP <!-- fig:t_pp_ms -->5<!-- /fig --> ms per page.
Every SPI byte costs 8 clocks at <!-- fig:spi_mhz -->12.5<!-- /fig --> MHz on the 1x link (`sw/litex/milan_soc.py:3361`).
Unlike FASTCONNECT section 9.4, this counts the command and page bytes on the link too.
The bound is graded at the AX7101's part; the Arty's S25FL128S has no maxima in the tree (`sw/litex/milan_soc.py:3346`).

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
The tree cites no suspend figure, so round 2 sources it from the datasheet (decision 5).

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

**Recommendation: refuse today's journal and boot blank, with the reason recorded.**

- A KLJ2 image is refused with `VD_VER` and never reinterpreted, as KLJ1 was (FASTCONNECT section 6.2).
- The new writer never writes today's journal, so a rollback to the release image finds its journal intact.
- At boot, a valid KLJ2 header in today's region is reported: the verdict, a console line and a status bit.
- The cost is one lost saved state per upgraded board: it boots unbound, as from blank flash.

**Alternative: import today's journal once.**
Both writers would keep a KLJ2 decoder and an id translation for one boot.
That keeps saved bindings across the upgrade, at the cost of a second decoder in the F1 store's block RAM.

**The VERSION chain step.**

- The container's magic becomes `KLJ3` and its `FMT_VER` major 3; acceptance rule 3's cap becomes the slot.
- A KLJ2 header in today's region is recognised as the previous format, hence `VD_VER`.
- F07.8 `layout_version` goes from 2 to 3: a <!-- fig:rec_hdr_bytes -->10<!-- /fig -->-byte header with a 16-bit `record_id`.
- The gateware VERSION minor advances by one at round 2's head, from today's <!-- fig:version_minor -->96<!-- /fig -->.
  Its five simulation assertions move together, as [the split architecture's section 7](../ARCHITECTURE_HW_SW_SPLIT.md#7-version-and-default-flip) lists:

<!-- nvm-format: begin version -->
| Assertion | Where | Reads today |
|---|---|---|
| CSR | `hdl/common/csr/milan_csr.sv:201` | `VERSION = 32'h0002_0060` |
| CSR suite | `tb/verilator/csr/sim_main.cpp:355` | `0x00020060` |
| Datapath | `tb/verilator/milan_dp/sim_main.cpp:291` | `0x00020060` |
| Every stream shape | `tb/verilator/milan_dp/sim_nxn.cpp:3189` | `0x00020060` |
| gPTP option | `tb/verilator/milan_dp/sim_gptp.cpp:860` | `0x00020060` |
| Pruning | `tb/verilator/milan_dp/sim_prune.cpp:351` | `0x00020060` |
<!-- nvm-format: end version -->

## 6. Every layer that carries record_id

Each row is cited by file:line, and the gate checks that each line still reads what it was cited for.

<!-- nvm-format: begin layers -->
| Layer | Where | Today | Change |
|---|---|---|---|
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv:182` | 8-byte header | 10-byte header, layout 3 |
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv:135` | 8-bit record id in | 16-bit field, 11 bits decoded |
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv:160` | 8-bit region out | widen with the id |
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_port.sv:115` | 1,024-byte payload cap | derived: the shape's largest payload |
| F07.8 framing | `protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv:127` | BINDING base 32 | derived BINDING base |
| F07.8 framing | `protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv:137` | layout 2 | layout 3 |
| F07.8 framing | `protocol-processor/hdl/acmp/KL_acmp_nvm_shadow.sv:139` | 500 ms window | the producer window of section 5 |
| F07.8 framing | `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:397` | fixed bases 0, 2, 10, 48, 64, 80, 128 | derived bases |
| F07.8 framing | `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:193` | 500 ms window | the producer window of section 5 |
| F07.8 framing | `protocol-processor/hdl/packet_engine/KL_pp_nvm_mgr_arb.sv:79` | 8-bit ids, both managers | widen with the id |
| F07.8 framing | `protocol-processor/hdl/top/protocol_processor_top.sv:598` | 8-bit region at the top | widen with the id |
| `dev_region_i` | `hdl/milan/KL_nvm_backend.sv:156` | 8-bit region in | widen with the id |
| `dev_region_i` | `hdl/milan/KL_pp_shadow.sv:1064` | 8-bit wire to the backend | widen with the id |
| `dev_region_i` | `hdl/milan/KL_pp_shadow.sv:417` | 8-bit map-writer id | widen with the id |
| Backend decode | `hdl/milan/KL_nvm_backend.sv:243` | fixed id blocks | derived blocks of section 2 |
| Backend decode | `hdl/milan/KL_nvm_backend.sv:228` | 8-byte header | 10-byte header |
| Backend decode | `hdl/milan/KL_nvm_backend.sv:311` | 9-bit compare | 12-bit compare |
| Backend decode | `hdl/milan/KL_nvm_backend.sv:194` | 16 map ports per table | 32 ports: one more index bit |
| Backend decode | `hdl/milan/KL_nvm_backend.sv:531` | 256 ownership bits | one bit per id, section 7 |
| Backend decode | `hdl/milan/KL_nvm_backend.sv:1124` | 256-id ownership loop | the derived id count |
| Backend refusals | `hdl/milan/KL_nvm_backend.sv:248` | 128 names | the derived NAME block |
| Backend refusals | `hdl/milan/KL_nvm_backend.sv:285` | 16 streams per direction | the derived stream blocks |
| Backend refusals | `hdl/milan/KL_nvm_backend.sv:288` | 16 stream ports | the derived map blocks |
| Map writer | `hdl/milan/milan_datapath.sv:5252` | ids 96 + port | derived MAPS_IN base |
| Map writer | `hdl/milan/milan_datapath.sv:5262` | ids 112 + port | derived MAPS_OUT base |
| Map writer | `hdl/milan/milan_datapath.sv:5229` | 127-entry cursors | cursors for 264 output keys |
| Map writer | `hdl/milan/milan_datapath.sv:318` | 500 ms window | the producer window of section 5 |
| Firmware, shipping writer | `sw/firmware/milan_baremetal/milan_baremetal.c:258` | fixed id blocks | generated bases |
| Firmware, shipping writer | `sw/firmware/milan_baremetal/milan_baremetal.c:373` | 8-bit block base and count | 16-bit |
| Firmware, shipping writer | `sw/firmware/milan_baremetal/milan_baremetal.c:329` | two 64 KiB slots | the slot and log of section 4 |
| Firmware, F1 store | `sw/firmware/ctrl_nvm/nvm_shape.h:132` | 256 ids | the derived id count |
| Firmware, F1 store | `sw/firmware/ctrl_nvm/nvm_shape.h:133` | 128 names | the derived NAME block |
| Firmware, F1 store | `sw/firmware/ctrl_nvm/nvm_shape.h:134` | image within one slot | base within one slot |
| Firmware, F1 store | `sw/firmware/ctrl_nvm/nvm_shape.h:136` | one erase block | the derived slot |
| Firmware, F1 store | `sw/firmware/ctrl_nvm/nvm_shape.h:33` | 64 KiB container | format 3 bound |
| Firmware, F1 store | `sw/firmware/ctrl_nvm/nvm_klj2.c:37` | 16 ports, 8-bit counts | 32 ports, 16-bit counts |
| Firmware, F1 store | `sw/firmware/ctrl_nvm/nvm_klj2.h:62` | 8-bit id | 16-bit |
| Firmware, F1 store | `sw/firmware/ctrl_nvm/nvm_store.c:490` | id at header byte 3 | 16-bit id at bytes 4 and 5 |
| Firmware, F1 store | `sw/firmware/ctrl_nvm/nvm_store.c:54` | 8 ownership words | the derived id count |
| F1 link | `sw/litex/ctrl_memory.py:384` | stage = container | stage = one page and one record |
| F1 link | `sw/litex/milan_soc.py:4653` | 64 KiB image | the base bound |
| F1 link | `sw/litex/milan_soc.py:3547` | 64 KiB live window | the derived sub-window |
| F1 link | `sw/litex/milan_soc.py:173` | 128 KiB journal | kept; a new journal below it |
| Builder | `sw/builder/endstation_builder.py:1464` | 16 streams per direction | read from the record space |
| Builder | `sw/builder/endstation_builder.py:2740` | 128 names | the derived NAME block |
| Builder | `sw/builder/endstation_builder.py:2353` | 64 KiB sub-windows | the derived sub-windows |
| Scripts | `scripts/nvm_contract.py:60` | 256 ids | the derived id count |
| Scripts | `scripts/nvm_contract.py:152` | fixed blocks | derived blocks |
| Scripts | `scripts/nvm_contract.py:34` | 8-byte header | 10-byte header |
| Scripts | `scripts/nvm_shape.py:131` | 16 map ports | the shape's ports |
| Scripts | `scripts/nvm_klj2.py:89` | 8-bit id frame | 16-bit id frame |
| Mailbox contract | `sw/mailbox/mailbox.yaml:93` | 16 bound talkers, as the BINDING block | a #859 decision, not this format |
<!-- nvm-format: end layers -->

The mailbox row is not this format's to change.
Its 16 bound talkers follow the BINDING block today, and the census puts its tables under its own decision.

## 7. Area and timing risk, ESTIMATE

**Every number in this section is an estimate.** Round 2 measures them under the #818 gate.

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
| # | Rule | Test | Plant that must be caught |
|---|---|---|---|
| T1 | NAME first id 222 | accepted by the builder, the backend decode, F1 and the codec | NAME base off by one |
| T2 | NAME last id 1,128 | the 32x32 TDM8 overlay's 907 names round trip | block end taken as exclusive |
| T3 | NAME one past, 1,129 | backend `dev_err`, F1 refusal, builder `ConfigError`, RTL `$error` | the refusal removed |
| T4 | Every other block | first, last and one-past id of each block in section 2 | one block sized by the wrong count |
| T5 | Capacity | 907 names accepted, one more refused, in the builder and the RTL | the builder reads a second copy of the bound |
| T6 | Old journal on boot | a KLJ2 journal boots blank with `VD_VER` recorded; its slots stay unwritten | a reader that reinterprets major 2 |
| T7 | Append order | a delta over the base: the last value wins | segments applied in reverse |
| T8 | Torn append | a cut at every page restores the last closing segment | a segment accepted without its CRC |
| T9 | Torn compaction | a cut at every page boots the old slot, losing nothing | authority moved before the new trailer verifies |
| T10 | Erase in progress | a save during the background erase suspends it | the save waits for the erase |
| T11 | Save bound | model time, change to verified, at most 500 ms at 32x32 TDM8 | a 1,000 ms firmware window |
| T12 | Reserve exhausted | the save waits, is published pending and is not lost | the save dropped |
| T13 | Commit deadline | at least twice the worst append at every shape | a 300 ms deadline |
| T14 | Payload cap | `MAX_PAYLOAD_P` covers 2,112 B | the 1,024 B default |
| T15 | Fit | base, log and window fit at every shape | a two-block slot |
| T16 | VERSION | the five assertions read the new VERSION | one left at today's |
<!-- nvm-format: end tests -->

Round 2 also runs the full sweep, rtl-fast, the builder bank and the LiteX simulations, as #823 asks.

## 9. Decisions requested

- **1. The record space.** Recommended: the derived allocation of section 2, 11 bits in a 16-bit field.
  Alternative: a packed allocation per shape.
- **2. Compatibility.** Recommended: refuse KLJ2 with `VD_VER`, boot blank, record the reason.
  Alternative: import a KLJ2 journal once at boot.
- **3. The slot.** Recommended: a derived slot of <!-- fig:sectors -->5<!-- /fig --> erase blocks, a <!-- fig:journal_kib -->640<!-- /fig --> KiB journal below today's.
  Alternative: a compact output-map encoding, reversing #501's per-port capacity.
- **4. The windows.** Recommended: <!-- fig:w_prod_ms -->100<!-- /fig --> ms producer and <!-- fig:w_fw_ms -->150<!-- /fig --> ms firmware first-dirty windows, superseding DR2a.
  Alternative: keep DR2a and measure the bound from the window's close, not the change.
- **5. The erase.** Recommended: background erase with erase suspend, its latency sourced in round 2.
  Alternative: no suspend, and a save behind an erase allowed <!-- fig:no_suspend_ms -->3,399.37<!-- /fig --> ms.
- **6. Ownership at 32x32.** Recommended: open bits in distributed RAM with a count.
  Alternative: flop-held bits, as today.
- **7. The commit deadline.** Recommended: <!-- fig:commit_timeout_ms -->500<!-- /fig --> ms for an append.
  Alternative: keep <!-- fig:commit_now_ms -->8,000<!-- /fig --> ms, which no longer detects a stalled append inside the bound.

## 10. Reproduce

```sh
python3 scripts/nvm_format_32x32.py
python3 scripts/nvm_format_32x32.py --blocks
python3 scripts/check_nvm_format_32x32.py
python3 scripts/check_nvm_format_32x32.py --self-test
```

After a change to a definition, `python3 scripts/check_nvm_format_32x32.py --write` regenerates every figure here.

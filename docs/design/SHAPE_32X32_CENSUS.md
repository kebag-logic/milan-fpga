# The 32x32 two-interface shape: limits census

Status: **census only** (#859, part of #665).
No 32x32 configuration is in the tree.
The saved-state record space, the mailbox contract's per-interface tables and the datapath's fixed-width stream fields need decisions first ([section 4](#4-what-needs-a-decision)).

The Mark II target is 32x32 streams (#640): 16x16 logical streams, each redundant on two networks.
This page lists every per-shape limit such a shape crosses at `dev-soft-core` `a9d69c77`, where each limit is stated, what bounds it and the rule it follows.

## Contents

- **[1. The shape](#1-the-shape)** -- The streams, their interfaces, what is kept from the 8x8 config, and how each limit was found.
- **[2. Census](#2-census)** -- Every limit the shape crosses, by area, with where it is stated and each point's figure against it.
  - [Generators](#generators) -- The builder's stream cap, its SRP row index, its name capacity, bandwidth and the resource estimate.
  - [Firmware](#firmware) -- ACMP's sink and source tables, the F1 store's record set and slot, the SRP pool, and where the link stops.
  - [Mailbox contract](#mailbox-contract) -- The per-interface tables, full at 16, the bit-per-source fields, the counter events, and the rings and buckets.
  - [AEM descriptor image](#aem-descriptor-image) -- The packed image's size against the firmware's rom and the 64 KiB flash slot.
  - [Name store](#name-store) -- The 395 writable names against the NAME block's 128 ids.
  - [Saved-state records](#saved-state-records) -- The record count, each 16-id block and the image against one 64 KiB slot.
  - [Stream DMAC and ID ranges](#stream-dmac-and-id-ranges) -- The MAAP allocation, its counts and the stream IDs, none crossed.
  - [Firmware memory map](#firmware-memory-map) -- The 224 KiB regions and the 56-RAMB36 budget against the measured points and the shape's two largest objects.
  - [Datapath RTL](#datapath-rtl) -- The five elaboration guards at 32 streams and the ones behind them.
  - [Harness, gates and image build](#harness-gates-and-image-build) -- The point lists, the gates that take every config, and why nothing refuses to route a shape.
- **[3. Rules for the limits that state none](#3-rules-for-the-limits-that-state-none)** -- The rule each unruled limit would follow at 32x32, and why.
- **[4. What needs a decision](#4-what-needs-a-decision)** -- The three limits no rule can lift: the record space, the contract's tables and the datapath's stream fields.

## 1. The shape

- **Streams.** 32 AAF talker and 32 AAF listener streams of eight channels, plus the CRF Media Clock Output and the CRF sink.
  That is 33 STREAM_OUTPUT and 33 STREAM_INPUT descriptors.
- **Interfaces.** Two. Stream n is on interface n mod 2, as in the two-interface build today (`sw/firmware/ctrl/test/ctrl_aecp_image.c:93-94`, `sw/firmware/ctrl/plat/ctrl_plat.c:203-206`).
  Odd streams are on the secondary interface, so each interface carries 16 AAF streams of each direction, and the two CRF streams, index 32, are on the primary.
- **Everything else** is `configs/endstation_ax7101_8x8.yaml`'s: the TDM32 master, the role pools (one pilot cluster and an eight-channel loopback pool per talker port), one AUDIO_UNIT and one CLOCK_DOMAIN.
  So the 8x8 two-interface measurement groups scale by the stream count alone.
- **The AEM model** has 460 descriptors: 288 AUDIO_CLUSTER, 34 CLOCK_SOURCE (internal, CRF and one per AAF input), 32 STREAM_PORT of each direction and one AVB_INTERFACE.
  It has 395 writable names.
  The two-interface model describes one AVB_INTERFACE, as the 8x8 two-interface build does. A second AVB_INTERFACE and stream redundancy are Milan v1.2 clause 8 (#394).

Each limit was found by running the generator, the firmware link or the datapath elaboration at the shape, lifting the limit it reported in a scratch copy, and running again.
No lift is in the tree.
Every figure below is from those runs, or from the formula a row cites.

## 2. Census

The columns give each point's figure against the limit: 1x1 with one interface (the shipping point), 8x8 with two, and 32x32 with two.

### Generators

| Limit | Where | 1x1/1if | 8x8/2if | 32x32/2if | What bounds it, and its rule |
|---|---|---:|---:|---:|---|
| At most 16 streams per direction | `sw/builder/endstation_builder.py:1464` | 1 | 8 | **32** | No stated rule: the cap dates from the builder's first version. In effect it is the saved-state blocks' 16 ids ([saved-state records](#saved-state-records)) |
| SRP attribute rows, 32 at most | `sw/builder/endstation_builder.py:332`, `:2221-2235`; `hdl/common/csr/milan_csr.sv:614` | 3 | 17 | **65** | Rows are L + T + the CRF output (`:2221`). The CSR window's row index `o_srp_ctx_idx` is a fixed 5 bits |
| Writable names, 128 at most | `sw/builder/endstation_builder.py:2740`, reading `hdl/milan/KL_nvm_backend.sv:248` | 39 | 107 | **395** | Each writable name is one saved record in the NAME block, ids 0x80 to 0xFF (#823) |
| SRP bandwidth, 75 % of the port | `bandwidth_limit_pct` of each config | 2.22 % | 13.82 % | 53.61 % | Not crossed. The builder charges every talker to one port |
| Resource estimate against the XC7A100T | `sw/builder/endstation_builder.py:717-724` | LUT 79.4 % | LUT 85.4 % | **LUT 111.1 %** | The verdict labels a shape and refuses nothing ([harness, gates and image build](#harness-gates-and-image-build)) |

### Firmware

| Limit | Where | 1x1/1if | 8x8/2if | 32x32/2if | What bounds it, and its rule |
|---|---|---:|---:|---:|---|
| ACMP sinks and sources, 16 each over every interface | `third_party/tsn-c-stack/include/acmp.h:157-162`, checked at `third_party/tsn-c-stack/src/acmp.c:1014`; arrays at `sw/firmware/ctrl/test/ctrl_aecp_image.c:93-94`, `sw/firmware/ctrl/app/ctrl_app.h:73`, `:98`, `sw/firmware/ctrl/app/ctrl_app_aecp.h:18`, `sw/firmware/ctrl/maap/maap_mbx.h:19-21`; `sw/firmware/ctrl/plat/ctrl_plat.c:35` | 2 / 2 | 9 / 9 | **33 / 33** | No rule ties 16 to a shape. The default is overridable at build time; changing it is a tsn-c-stack change |
| F1 record set, 256 ids; names, 128 | `sw/firmware/ctrl_nvm/nvm_shape.h:132-133` | 54 / 39 | 164 / 107 | **596 / 395** | The F07.8 `record_id[7:0]` and its NAME block (#823) |
| F1 container, one 64 KiB slot | `sw/firmware/ctrl_nvm/nvm_shape.h:134`, `:136` | 3,336 B | 13,256 B | **99,080 B** | One erase block per slot (#823) |
| The SRP pool (`image_arena`) | `sw/firmware/ctrl/srp/srp_mbx.h:94-98` | 9,920 B | 48,064 B | 144,832 B, from the formula | Per interface: two small blocks of 96 B, 16 + 3 per source + 4 per sink medium blocks of 288 B, and two large blocks of 544 B. Every interface's participant is sized for every stream of the entity. The first two figures are the linked images' |

The firmware link at 32x32/2if stops at `nvm_shape.h:132-133`.
With those two lifted it stops at `ctrl_aecp_image.c:93-94`, which fills ACMP's sink and source tables past 16.
With ACMP's maxima at 33 it stops at `sw/firmware/ctrl/acmp/acmp_mbx.c:14-15`, the contract's tables below.

### Mailbox contract

| Limit | Where | 1x1/1if | 8x8/2if | 32x32/2if | What bounds it, and its rule |
|---|---|---:|---:|---:|---|
| Bound-talker entries per interface, 16 | `sw/mailbox/mailbox.yaml:93`, `:304-307`; `sw/mailbox/mailbox_model.py:421-425`; `sw/firmware/ctrl/acmp/acmp_mbx.c:14`, `:57-63` | 2 | 9 | **33** | One entry per listener stream, equal to `ACMP_MAX_SINKS` and the saved-state binding block (`mailbox.yaml:93-94`). Sink k is entry k of its interface's table, so each table holds every sink of the entity. The 0x100 stride holds 16 entries of 0x10 |
| Publication source and sink entries per interface, 16 each | `sw/mailbox/mailbox.yaml:96-97`, `:340-346`; `sw/mailbox/mailbox_model.py:452-465`; `sw/firmware/ctrl/acmp/acmp_mbx.c:15` | 2 | 9 | **33** | As above. Source entries fill 0x080 to 0x100 and sink entries 0x100 to 0x200, the whole 0x200 stride |
| One bit per source, 16 bits | `sw/mailbox/mailbox.yaml:361` (`DA_GATE.OPEN`), `:372` (`LICENCE.ACTIVE`), `:406` (`TALKER_DECL.DECLARED`) | 2 | 9 | **33** | Bit s is source s. 33 sources need more than a 32-bit register |
| Face block source entries per interface, 16 | `sw/mailbox/mailbox.yaml:496-499`; `sw/mailbox/mailbox_model.py:499-501` | 2 | 9 | **33** | Source entries fill 0x100 to 0x200, where the sink entries start |
| COUNTERS_CHANGED bits, 16 STREAM_INPUT and 16 STREAM_OUTPUT per interface | `sw/mailbox/mailbox.yaml:857-863`, `:1033-1034` | 2 | 9 | 33 | Not refused: a change naming a descriptor with no bit posts ALL, so every served descriptor may have moved. One record per descriptor per second (Milan v1.2 Table 5.22) |
| Interfaces, 1 to 4 | `sw/mailbox/mailbox_model.py:681` | 1 | 2 | 2 | Not crossed |
| Rings and token buckets | `sw/mailbox/mailbox.yaml:1133-1210` | | | | The same constants at every shape. The contract states no derivation from a protocol rate, a timer or a stream count; the backlog bounds take each ring as given ([assumption A1](MAILBOX_SPLIT.md#service-latency)) |

Each per-interface table above is full at 16, and the contract's own rule makes any growth that moves a field a major change (`sw/mailbox/mailbox.yaml:28-33`).
Indexing a stream by its ordinal on its own interface would need 17 entries on the primary and 16 on the secondary: still over 16, because both CRF streams are on the primary.

### AEM descriptor image

| Limit | Where | 1x1/1if | 8x8/2if | 32x32/2if | What bounds it, and its rule |
|---|---|---:|---:|---:|---|
| The packed image | `avdecc/gen_aemi_image.py` | 7,512 B | 19,520 B | 69,488 B | It is linked into the firmware's `rom` |
| The `aem` flash slot, 64 KiB at 0x400000 | `sw/litex/flash_map.py` | 7,512 B | 19,520 B | **69,488 B** | One erase block. Only a flashed image needs it, and a simulation-only shape is never flashed |
| Descriptors | `avdecc/gen_aemi_image.py` | 42 | 124 | 460 | Not crossed |

### Name store

| Limit | Where | 1x1/1if | 8x8/2if | 32x32/2if | What bounds it, and its rule |
|---|---|---:|---:|---:|---|
| NAME records, 128 | `hdl/milan/KL_nvm_backend.sv:248`, `:294-295`; `sw/firmware/ctrl_nvm/nvm_shape.h:133` | 39 | 107 | **395** | The rest of the 8-bit record_id space, 0x80 to 0xFF. 395 names of 64 octets are 25,280 B. #823 owns the capacity, the slot size or a compact name encoding |

### Saved-state records

| Limit | Where | 1x1/1if | 8x8/2if | 32x32/2if | What bounds it, and its rule |
|---|---|---:|---:|---:|---|
| Records, 256 ids | `sw/firmware/ctrl_nvm/nvm_shape.h:132`; `scripts/check_nvm_record_space.py` | 54 | 164 | **596** | F07.8 frames one record per item group and index, so the count is fixed by the shape |
| BINDING and FMT_IN, one per STREAM_INPUT, 16 ids each | `hdl/milan/KL_nvm_backend.sv:285-287`; `scripts/nvm_shape.py:221-226` | 2 | 9 | **33** | The 0x20 and 0x30 blocks |
| FMT_OUT and PT_OFS, one per STREAM_OUTPUT, 16 ids each | as above | 2 | 9 | **33** | The 0x40 and 0x50 blocks |
| MAPS_IN and MAPS_OUT, one per STREAM_PORT, 16 ids each | `hdl/milan/KL_nvm_backend.sv:288-290`; `scripts/nvm_shape.py:131` | 1 | 8 | **32** | The 0x60 and 0x70 blocks; the backend's tables are indexed by `csr_addr_i[3:0]` |
| The image, one 64 KiB slot | `sw/firmware/ctrl_nvm/nvm_shape.h:134`, `:136` | 3,336 B (5 %) | 13,256 B (20 %) | **99,080 B (151 %)** | Two slots of one erase block each in the 128 KiB `journal` region |

### Stream DMAC and ID ranges

| Limit | Where | 1x1/1if | 8x8/2if | 32x32/2if | What bounds it, and its rule |
|---|---|---:|---:|---:|---|
| Stream t's destination, from the MAAP allocation | `sw/builder/endstation_builder.py:361`, `:2067-2078`; `sw/firmware/ctrl/app/ctrl_app.c:28` | 2 | 9 | 33 | Not crossed: one address per talker stream, inside the MAAP dynamic allocation pool (IEEE 1722-2016 Annex B) |
| MAAP_COUNT and the range test's count, 16 bits | `sw/mailbox/mailbox.yaml:193`, `:1123` | 2 | 9 | 33 | Not crossed |
| Each source's stream_id | `sw/mailbox/mailbox.yaml:408-426` | 2 | 9 | 33 | Not crossed: one 64-bit ID per source entry (IEEE 1722-2016 4.4.4.8) |

### Firmware memory map

| Limit | Where | 1x1/1if | 8x8/2if | 32x32/2if | What bounds it, and its rule |
|---|---|---:|---:|---:|---|
| `rom` and `sram`, 224 KiB each | `sw/litex/ctrl_memory.py:132-133` | 104,448 / 46,272 B | 119,824 / 113,008 B | **`sram` at least 243,920 B** | Each region spans the whole budget ([memory map](SPLIT_CONTROL_MEMORY.md#1-memory-map)). At 32x32 two objects alone exceed `sram`: the SRP pool's 144,832 B and the F1 stage's 99,088 B (the container plus one record header, `sw/litex/ctrl_memory.py:384-399`) |
| 56 RAMB36 | `sw/litex/ctrl_memory.py:53`; the ledgered points `:212-221` | 37.0 | 57.5, ledgered | not linked | The owner's 224 KB (#640). The 8x8/2if point is ledgered to the hybrid XIP lane ([fit](SPLIT_CONTROL_MEMORY.md#5-fit)) |

The 1x1/1if and 8x8/2if figures are the size fixture linked at `a9d69c77` (`ctrl_srp_image.py --with-aecp --layout split`), `rom` then `sram` need, and the plan's tiles.

### Datapath RTL

The datapath elaborated at 32 streams (Verilator lint-only, the `obj_nxn8` recipe of `tb/verilator/milan_dp/Makefile` with `-GN_STREAMS=32` and the 32x32 shape include) stops on five guards, in 0.99 s at 142 MB:

| Guard | Bound | 32x32 | Rule |
|---|---|---:|---|
| `hdl/milan/KL_nvm_backend.sv:285-287` | 16 streams per direction | 33 | The record blocks above (#823) |
| `hdl/ieee1722/aaf/KL_render_queue.sv:324-325` | 8 streams | 32 | The render crossbar's 3-bit stream field |
| `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:131-132` | 16 contexts | 33 | A 4-bit context index |
| `hdl/ieee1722/avtp/KL_media_clock_restart.sv:196-197` | 16 talkers | 33 | A 4-bit talker index |
| `hdl/milan/milan_datapath.sv:5228-5232` | 127 map entries | 256 output keys | The channel-map writer's 8-bit cursors and its record: `AMR_OK_C`, the output keys, is one key per stream and channel, N_STREAMS x 8 (`:4121`) |

Behind them, not reached by the elaboration: `hdl/milan/KL_nvm_backend.sv:288-290` (stream ports) and `:294-295` (names), and `hdl/common/csr/milan_csr.sv:614` (SRP rows).

### Harness, gates and image build

| List | Where | Holds |
|---|---|---|
| The split CPU budget harness's points | `tb/verilator/ctrl_service_budget/run.py:30`; `tb/verilator/ctrl_service_budget/build.py:179` | 1x1/1if and 8x8/2if; 8x8/2if ledgered |
| The fabric service budget's shapes | `tb/verilator/fw_service_budget/run.py:18` | 1x1 and 8x8 |
| The hook harness, the split store target | `tb/verilator/ctrl_service_hooks/hooks_build.py:37`, `:40`; `tb/verilator/nvm_split_target/run.py:53` | 1x1/1if and 8x8/2if |
| The F5 stream counters | `sw/firmware/ctrl/test/ctrl_configs.py:123-125` | 1 and 8 streams |
| The builder bank's configs | `sw/builder/test_builder.py:352-358` | the five shipped configs |
| The image build's recipes | `sw/litex/build.sh:195-197`; `scripts/check_sweep_shape.py:66-68` | 1x1, 8x8 and the Arty; `BUILD_CFG` takes any config under `configs/` |

These gates take every `configs/endstation_*.yaml`, so a new config joins each with no edit: `scripts/check_entity_shape.py:834`, `scripts/check_wire_accountability.py:444`, `scripts/check_nvm_record_space.py:962`, `scripts/audit_pp_descriptors.py:144`, the generated diagram `docs/diagrams/nxn_window_map.gen.py:42`, and the publication census, whose shapes are every config's datapath (`sw/mailbox/census_elab.py:166`).
At 32x32 the record-space gate reports 386 findings, and the census reaches the datapath guards above.
Nothing refuses to route a shape for its size: the resource verdict only labels it.

## 3. Rules for the limits that state none

- **16 streams per direction.** No rule of its own; the record blocks set it. The rule for 32x32 is the record space's capacity once #823 parametrises it.
- **ACMP's 16 sinks and sources.** No rule tied to a shape. The rule for 32x32: the stack holds the shape's sinks and sources, the CRF streams included, as the generated `CTRL_SRP_SINKS` and `CTRL_SRP_SOURCES` state them (`sw/firmware/ctrl/srp/srp_entity.py:20-21`), which `ctrl_plat.c:35` already compares.
  33 each at 32x32.
- **Rings and token buckets.** No per-stream rule.
  The rule for 32x32: each bucket's refill at least the channel's arrival rate at the shape, each burst at least its largest legal back-to-back arrival, and each ring at least that burst in the channel's largest frame, each from a cited protocol rate or timer.
  The backlog bounds charge a full ring, so the ring is what those bounds pay for, and the bucket is what holds arrivals to the rate.
- **The memory map.** The regions span the budget by design. A simulation-only map with larger regions, stated in `sw/litex/ctrl_memory.py`, is what the shape's link needs once it can compile.

## 4. What needs a decision

1. **The saved-state record space and slot (#823).**
   It blocks the builder, the firmware's F1 store and the fabric backend, and it fixes the contract's bound-talker rule at 16.
   #823's scope already names 32x32 and owns the choices: the record-ID width or allocation, the slot size or a compact name encoding, compatibility with today's journals, and the VERSION chain.
   No 32x32 config can be generated before it.
2. **The contract's per-interface tables.**
   33 entries and 33-bit source masks do not fit the contract's layout, and growth moves fields, a major change to every shape's contract.
   Per-interface ordinals in the firmware leave 17 on the primary.
3. **The datapath's fixed-width stream fields.**
   The render crossbar's 3-bit stream field, the 4-bit talker indices, the map writer's cursors and the SRP row index.
   Widening them changes the datapath at every shape; #640's redesign replaces the per-stream engines they belong to.

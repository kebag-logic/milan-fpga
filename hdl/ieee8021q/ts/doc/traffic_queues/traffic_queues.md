<!--
TerosHDL documenter output (docs/DOC_GENERATION.md section 2): the Diagram /
Generics / Ports / Signals / Constants / Instantiations sections and
traffic_queues.svg are MACHINE-EMITTED from traffic_queues.sv and are
DISCARDED on the next "Save documentation" run - do not invest prose in them.
The masters are the //! comments in the RTL. There is no headless CLI on this
box (Node is absent), so a stale table is fixed by an editor session, not by a
script; the "Signals" table below is stale in exactly that way and says so.
The Contents block is gen_toc.py's and does survive.
-->

# Entity: traffic_queues 
- **File**: traffic_queues.sv

## Contents

- **[Diagram](#diagram)** — The generated schematic: one demux fanning frames out by `tdest`, a FIFO per queue, and a single egress selector.
- **[Generics](#generics)** — Three, and the depth is the one to read carefully — the default here is not what gets built; `traffic_controller_802_1q` instantiates it far shallower.
- **[Ports](#ports)** — The whole contract with the shaper is two one-hot vectors: `queue_grant_i` in, `queue_has_data_o` out. Everything else is the AXIS pair and clock/reset.
- **[Signals](#signals)** — **Stale generated table, banner-flagged**: it lists a pre-`axis_demux` naming (`mux_to_fifo_*`/`fifo_to_demux_*` plus `*_array` views) that the RTL no longer has — today the buses are `dm_*` and `ff_*` and there is no `tdest` bus. Plumbing only; read the source if you are matching signals.
- **[Constants](#constants)** — The three localparams, and the one that bites: `TDEST_WIDTH` is `$clog2` of the queue count, **not** the queue count — 3 bits at the shipping 5 queues. Also the `KW` byte width and the `PROG_EMPTY_THRESH = 5` that preserves the CBS scheduler's underrun margin.
- **[Instantiations](#instantiations)** — The three children, each annotated with what it replaced: a vendor-free demux instead of generated switch IP, `axis_fifo` instead of `xpm_fifo_axis`, and — the important one — a grant-indexed **combinational** mux on egress instead of `axis_arb_mux`, because a second arbiter stacked on the CBS grant deadlocked TX.

## Diagram
![Diagram](traffic_queues.svg "Diagram")
## Generics

| Generic name     | Type | Value | Description              |
| ---------------- | ---- | ----- | ------------------------ |
| TDATA_WIDTH      | int  | 64    | Widht of tdata bus       |
| NUMBER_OF_QUEUES | int  | 5     | Number of network queues |
| FIFO_DEPTH       | int  | 16384 | Buffer depth (default; `traffic_controller_802_1q` instantiates it with `BUFFER_FIFO_DEPTH = 1024`) |

## Ports

| Port name        | Direction | Type                        | Description                      |
| ---------------- | --------- | --------------------------- | -------------------------------- |
| clk              | input     | wire                        | clock signal                     |
| resetn           | input     | wire                        | syncronous active low reset      |
| queue_grant_i    | input     | wire [NUMBER_OF_QUEUES-1:0] | One-hot: indicates granted queue |
| queue_has_data_o | output    | wire [NUMBER_OF_QUEUES-1:0] | One-hot: queue data availability |
| s_axis           |           | axi_stream_if.slave         | slave interface of AXIS          |
| m_axis           |           | axi_stream_if.master        | master interface of AXIS         |

## Signals

> **STALE — do not match signals against this table.** It is TerosHDL output
> from a pre-`axis_demux` revision of `traffic_queues.sv`. In the current RTL
> the buses are named `dm_*` (demux → FIFO) and `ff_*` (FIFO → egress mux),
> there are no `*_array` unpacked views and no `*_tdest` bus at all
> (`traffic_queues.sv` lines 65-72). A TerosHDL regeneration replaces this
> table wholesale; until then read the source.

| Name                                             | Type                                          | Description                                              |
| ------------------------------------------------ | --------------------------------------------- | -------------------------------------------------------- |
| mux_to_fifo_tdata                                | wire [(NUMBER_OF_QUEUES*TDATA_WIDTH)-1:0]     | Packed signals for mux switch outputs (to FIFOs)         |
| mux_to_fifo_tkeep                                | wire [(NUMBER_OF_QUEUES*(TDATA_WIDTH/8))-1:0] |                                                          |
| mux_to_fifo_tvalid                               | wire [NUMBER_OF_QUEUES-1:0]                   |                                                          |
| mux_to_fifo_tready                               | wire [NUMBER_OF_QUEUES-1:0]                   |                                                          |
| mux_to_fifo_tlast                                | wire [NUMBER_OF_QUEUES-1:0]                   |                                                          |
| mux_to_fifo_tdest                                | wire [(NUMBER_OF_QUEUES*TDEST_WIDTH)-1:0]     |                                                          |
| fifo_to_demux_tdata                              | wire [(NUMBER_OF_QUEUES*TDATA_WIDTH)-1:0]     | Packed signals for FIFO outputs (to demux)               |
| fifo_to_demux_tkeep                              | wire [(NUMBER_OF_QUEUES*(TDATA_WIDTH/8))-1:0] |                                                          |
| fifo_to_demux_tvalid                             | wire [NUMBER_OF_QUEUES-1:0]                   |                                                          |
| fifo_to_demux_tready                             | wire [NUMBER_OF_QUEUES-1:0]                   |                                                          |
| fifo_to_demux_tlast                              | wire [NUMBER_OF_QUEUES-1:0]                   |                                                          |
| fifo_to_demux_tdest                              | wire [(NUMBER_OF_QUEUES*TDEST_WIDTH)-1:0]     |                                                          |
| mux_to_fifo_tdata_array[NUMBER_OF_QUEUES-1:0]    | wire [TDATA_WIDTH-1:0]                        | Unpacked array views for easier indexing inside generate |
| mux_to_fifo_tkeep_array[NUMBER_OF_QUEUES-1:0]    | wire [(TDATA_WIDTH/8)-1:0]                    |                                                          |
| mux_to_fifo_tvalid_array[NUMBER_OF_QUEUES-1:0]   | wire                                          |                                                          |
| mux_to_fifo_tready_array[NUMBER_OF_QUEUES-1:0]   | wire                                          |                                                          |
| mux_to_fifo_tlast_array[NUMBER_OF_QUEUES-1:0]    | wire                                          |                                                          |
| mux_to_fifo_tdest_array[NUMBER_OF_QUEUES-1:0]    | wire [TDEST_WIDTH-1:0]                        |                                                          |
| fifo_to_demux_tdata_array[NUMBER_OF_QUEUES-1:0]  | wire [TDATA_WIDTH-1:0]                        |                                                          |
| fifo_to_demux_tkeep_array[NUMBER_OF_QUEUES-1:0]  | wire [(TDATA_WIDTH/8)-1:0]                    |                                                          |
| fifo_to_demux_tdest_array[NUMBER_OF_QUEUES-1:0]  | wire [TDEST_WIDTH-1:0]                        |                                                          |
| fifo_to_demux_tvalid_array[NUMBER_OF_QUEUES-1:0] | wire                                          |                                                          |
| fifo_to_demux_tready_array[NUMBER_OF_QUEUES-1:0] | wire                                          |                                                          |
| fifo_to_demux_tlast_array[NUMBER_OF_QUEUES-1:0]  | wire                                          |                                                          |
| fifo_empty[NUMBER_OF_QUEUES-1:0]                 | wire                                          |                                                          |

## Constants

| Name              | Type | Value                                                     | Description                                                    |
| ----------------- | ---- | --------------------------------------------------------- | -------------------------------------------------------------- |
| TDEST_WIDTH       |      | `(NUMBER_OF_QUEUES <= 1) ? 1 : $clog2(NUMBER_OF_QUEUES)`   | Width of `tdest` field. It is `$clog2` of the queue count, **not** the queue count — at the shipping `NUMBER_OF_QUEUES = 5` that is 3 bits, not 5. The `<= 1` arm keeps a 1-queue build from asking for a zero-width bus (`traffic_queues.sv:49`) |
| KW                | int  | `TDATA_WIDTH/8`                                            | Bytes per beat = `tkeep` width                                 |
| PROG_EMPTY_THRESH | int  | `5`                                                        | A queue reports "has data" only above this depth — the old xpm `PROG_EMPTY_THRESH`, kept so the CBS scheduler's underrun margin is unchanged |

## Instantiations

- demux_queues: axis_demux (verilog-axis; replaced the generated axis_switch_1in_4out IP)
  -  1-to-4 routing by `tdest` into the per-queue FIFOs- queue FIFOs: axis_fifo (verilog-axis; replaced xpm_fifo_axis)
  -  per-queue buffering; egress is a grant-indexed combinational mux
     (replaced axis_arb_mux after the CBS cross-lock fix,
     [docs/findings/CBS_DATAPATH_BUG.md](../../../../../docs/findings/CBS_DATAPATH_BUG.md))
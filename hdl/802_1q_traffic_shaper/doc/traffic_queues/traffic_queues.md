
# Entity: traffic_queues 
- **File**: traffic_queues.sv

## Diagram
![Diagram](traffic_queues.svg "Diagram")
## Generics

| Generic name     | Type | Value | Description              |
| ---------------- | ---- | ----- | ------------------------ |
| TDATA_WIDTH      | int  | 64    | Widht of tdata bus       |
| NUMBER_OF_QUEUES | int  | 4     | Number of network queues |
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

| Name        | Type | Value              | Description            |
| ----------- | ---- | ------------------ | ---------------------- |
| TDEST_WIDTH |      | (NUMBER_OF_QUEUES) | Width of `tdest` field |

## Instantiations

- demux_queues: axis_demux (verilog-axis; replaced the generated axis_switch_1in_4out IP)
  -  1-to-4 routing by `tdest` into the per-queue FIFOs- queue FIFOs: axis_fifo (verilog-axis; replaced xpm_fifo_axis)
  -  per-queue buffering; egress is a grant-indexed combinational mux
     (replaced axis_arb_mux after the CBS cross-lock fix,
     docs/findings/CBS_DATAPATH_BUG.md)
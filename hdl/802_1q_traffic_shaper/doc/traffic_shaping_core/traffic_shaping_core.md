
# Entity: traffic_shaping_core 
- **File**: traffic_shaping_core.sv

## Diagram
![Diagram](traffic_shaping_core.svg "Diagram")
## Generics

| Generic name     | Type | Value | Description              |
| ---------------- | ---- | ----- | ------------------------ |
| TDATA_WIDTH      | int  | 64    | Widht of tdata bus       |
| NUMBER_OF_QUEUES | int  | 4     | Number of network queues |

## Ports

| Port name        | Direction | Type                        | Description                                  |
| ---------------- | --------- | --------------------------- | -------------------------------------------- |
| clk              | input     | wire                        | clock signal                                 |
| resetn           | input     | wire                        | syncronous active low reset                  |
| queue_has_data_i | input     | wire [NUMBER_OF_QUEUES-1:0] | One-hot: indicates which queues contain data |
| is_1g_i          | input     | wire                        | High when the link rate is 1GBps             |
| grant_queue_o    | output    | [NUMBER_OF_QUEUES-1:0]      | One-hot: indicates which queue is granted    |
| s_axis           |           | axi_stream_if.slave         | slave interface of AXIS                      |
| m_axis           |           | axi_stream_if.master        | master interface of AXIS                     |

## Signals

| Name                               | Type                                | Description                                                  |
| ---------------------------------- | ----------------------------------- | ------------------------------------------------------------ |
| is_transmitting = 0                | logic [NUMBER_OF_QUEUES-1:0]        | Indicates whether each queue is currently transmitting       |
| bytes_sent      [NUMBER_OF_QUEUES] | logic [15:0]                        | Number of bytes transmitted in the current cycle (per queue) |
| allow_transmit                     | logic [NUMBER_OF_QUEUES-1:0]        | Credit-based decision signal from CBS modules                |
| active_queue                       | logic [clog2(NUMBER_OF_QUEUES)-1:0] | Currently active queue index                                 |
| hold_grant                         | logic                               | Latch to hold current grant until end of packet (tlast)      |

## Processes
- unnamed: ( @(posedge clk) )
  - **Type:** always_ff
  - **Description**
  Queue grant logic - one queue should be grant a time 

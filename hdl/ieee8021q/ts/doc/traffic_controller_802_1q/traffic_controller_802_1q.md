
# Entity: traffic_controller_802_1q 
- **File**: traffic_controller_802_1q.sv

## Contents

- **[Diagram](#diagram)** — The generated block picture of the classify → queue → shape chain.
- **[Generics](#generics)** — The five elaboration parameters with their defaults: 64-bit AXIS, big-endian classification, `NUMBER_OF_QUEUES` = 5 (the 802.1Q-ordered egress map) and an 8192-deep per-queue FIFO.
- **[Ports](#ports)** — A slave AXIS in, a master AXIS out, and one sideband that matters: `is_1g_i`, the link-rate input the CBS sendSlope denominator depends on.
- **[Signals](#signals)** — The two internal buses between the queues and the shaper — one-hot `queue_grant` and `queue_has_data`, one bit per traffic class.
- **[Constants](#constants)** — One derived constant: `TDEST_WIDTH` follows `NUMBER_OF_QUEUES`, so `tdest` is the queue selector the classifier writes and the queue block decodes.
- **[Instantiations](#instantiations)** — The four children and the two AXIS interfaces between them, in datapath order: classifier assigns `tdest`, `traffic_queues` buffers one FIFO per queue, `traffic_shaping_core` applies CBS on egress.

## Diagram
![Diagram](traffic_controller_802_1q.svg "Diagram")
## Generics

| Generic name          | Type | Value | Description                          |
| --------------------- | ---- | ----- | ------------------------------------ |
| TDATA_WIDTH           | int  | 64    | AXI-Stream data bus width            |
| BIG_ENDIAN            | bit  | 1     | Determines byte order for classifier |
| CLASSIFIER_FIFO_DEPTH | int  | 64    | FIFO depth for classification stage  |
| NUMBER_OF_QUEUES      | int  | 5     | Number of traffic classes/queues     |
| BUFFER_FIFO_DEPTH     | int  | 8192  | Per-queue FIFO depth                 |

## Ports

| Port name | Direction | Type                 | Description                      |
| --------- | --------- | -------------------- | -------------------------------- |
| clk       | input     | wire                 | Clock signal                     |
| resetn    | input     | wire                 | Active-low synchronous reset     |
| is_1g_i   | input     | wire                 | High when the link rate is 1GBps |
| s_axis    |           | axi_stream_if.slave  | slave interface of AXIS          |
| m_axis    |           | axi_stream_if.master | master interface of AXIS         |

## Signals

| Name           | Type                        | Description                     |
| -------------- | --------------------------- | ------------------------------- |
| queue_grant    | wire [NUMBER_OF_QUEUES-1:0] | One-hot queue grant signals     |
| queue_has_data | wire [NUMBER_OF_QUEUES-1:0] | One-hot queue data availability |

## Constants

| Name        | Type | Value              | Description            |
| ----------- | ---- | ------------------ | ---------------------- |
| TDEST_WIDTH |      | (NUMBER_OF_QUEUES) | Width of `tdest` field |

## Instantiations

- classifier_to_queue: axi_stream_if
  -  AXIS interface from traffic_classifier to traffic_queues- queue_to_shaper: axi_stream_if
  -  AXIS interface from traffic_queues to traffic_shaping_core- classifier: traffic_classifier
  -  Classifier: Extracts priority and assigns `tdest` value- buffer_queues: traffic_queues
  -  buffer_queues: One FIFO per queue, stores packets based on `tdest`- traffic_shaper: traffic_shaping_core
  -  Shaper: Applies Credit-Based Shaping (CBS) to regulate egress flow
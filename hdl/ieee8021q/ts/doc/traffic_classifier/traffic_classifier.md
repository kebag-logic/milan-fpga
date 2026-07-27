
# Entity: traffic_classifier 
- **File**: traffic_classifier.sv

## Contents

- **[Diagram](#diagram)** — Generated block symbol (`traffic_classifier.svg`).
- **[Description](#description)** — The only prose on the page, and the one rule worth carrying away: parsing is *always* done big-endian internally (converted if `BIG_ENDIAN=0`), while the payload is forwarded byte-unmodified in its original order.
- **[Generics](#generics)** — `TDATA_WIDTH` (32/64/128 all tested), the `BIG_ENDIAN` conversion switch, and the buffer FIFO depth.
- **[Ports](#ports)** — Clock, active-low sync reset, and a straight AXIS slave-to-master pass-through; the classification verdict leaves on `tdest`, not on a port of its own.
- **[Signals](#signals)** — The header-capture path (`eth_header` comb vs `eth_header_buf` registered, so a back-to-back packet cannot overwrite it mid-decode) plus the tdata/tkeep/tvalid/tlast delay arrays that hold data back until tdest is ready.
- **[Constants](#constants)** — `LATENCY` per tdata width and `LATENCY_SAFE`, which forces a depth of 1 so the delay arrays never degenerate to zero length.
- **[Processes](#processes)** — Four always blocks: slice bytes into the header buffer, register it, decode it combinationally, and delay the master interface so tdest lands on the right beat.
- **[Instantiations](#instantiations)** — The packet buffer that holds a frame while its headers are parsed — now `axis_fifo` from verilog-axis, the de-Xilinx replacement for `xpm_fifo_axis`.

## Diagram
![Diagram](traffic_classifier.svg "Diagram")
## Description

This module implements an Ethernet packet classifier that parses incoming AXIS frames and
assigns traffic priority based on the VLAN PCP field or Ethertype (e.g., PTP detection).
The module is working with different tdata_widths, 32,64,128 are tested.
Parsing is always performed in **big endian** byte order for consistent decoding.
If `BIG_ENDIAN` is set to 0 (little endian system), the module automatically converts input
data to big endian internally for parsing. Output data remains in its original endian format
and is forwarded unmodified.

## Generics

| Generic name | Type | Value | Description        |
| ------------ | ---- | ----- | ------------------ |
| TDATA_WIDTH  | int  | 64    | Widht of tdata bus |
| BIG_ENDIAN   | bit  | 1     | Big endian logic   |
| FIFO_DEPTH   | int  | 64    | FIFO depth         |

## Ports

| Port name | Direction | Type                 | Description                 |
| --------- | --------- | -------------------- | --------------------------- |
| clk       | input     | wire                 | clock signal                |
| resetn    | input     | wire                 | syncronous active low reset |
| s_axis    |           | axi_stream_if.slave  | slave interface of AXIS     |
| m_axis    |           | axi_stream_if.master | master interface of AXIS    |

## Signals

| Name                             | Type                                | Description                                                       |
| -------------------------------- | ----------------------------------- | ----------------------------------------------------------------- |
| header_ready                     | logic                               | Flag indicates ethernet headers are received.                     |
| eth_header                       | logic [ETH_HEADER_BUFFER_WIDTH-1:0] | Ethernet header buffer assigned combinationally.                  |
| eth_header_buf                   | logic [ETH_HEADER_BUFFER_WIDTH-1:0] | Ethernet header buffer assigned sequentially.                     |
| byte_counter                     | logic [clog2(ETH_HEADER_WIDTH):0]   | Counter for detecting whether ethernet header is captured or not. |
| eth_type_raw                     | logic [ETH_TYPE_BIT_WIDTH-1:0]      | ethernet type register when VLAN tag exists it is 8100.           |
| packet_in_progress               | logic                               | Flag that indicates a packet is being sent currently.             |
| tdata_delay   [0:LATENCY_SAFE-1] | logic [TDATA_WIDTH-1:0]             | tdata delay register.                                             |
| tkeep_delay [0:LATENCY_SAFE-1]   | logic [TDATA_WIDTH/8-1:0]           | tkeep delay register.                                             |
| tvalid_delay [0:LATENCY_SAFE-1]  | logic                               | tvalid delay register.                                            |
| tlast_delay  [0:LATENCY_SAFE-1]  | logic                               | tlast delay register.                                             |

## Constants

| Name         | Type | Value                         | Description                                                                   |
| ------------ | ---- | ----------------------------- | ----------------------------------------------------------------------------- |
| LATENCY      |      | (TDATA_WIDTH == 32) ? 'd3 : ( | Latency assignment to make aligment with tdest in master axis interface.      |
| LATENCY_SAFE |      | (LATENCY > 0) ? LATENCY : 1   | When Latency is 0, t*_delay ports will be invalid therefore safe calculation. |

## Processes
- data_slice: ( @(posedge clk) )
  - **Type:** always_ff
  - **Description**
  If headers are not ready add tdata into the eth_header slice, if the module is instantiated  little endian, parser logic will convert into big endian for ONLY parsing logic, data will be  conveyed little endian again. 
- eth_hdr_buffer: ( @(posedge clk) )
  - **Type:** always_ff
  - **Description**
  register eth_header content to not lose due to immediate new packet override. 
- parse_eth_header: (  )
  - **Type:** always_comb
  - **Description**
  Immediately decode eth_header_buf combinationally. 
- m_axis_allignment: ( @(posedge clk) )
  - **Type:** always_ff
  - **Description**
  Delay master interface for tdest alignment. 

## Instantiations

- m_axis_fifo: axi_stream_if
  -  Master axis interface from fifo.- eth_packet_buffer: axis_fifo (verilog-axis; replaced xpm_fifo_axis)
  -  Storing incoming packets in the fifo till headers parsing is completed.
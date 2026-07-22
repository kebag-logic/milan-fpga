
# Entity: ethernet_events 
- **File**: ethernet_events.sv

## Diagram
![Diagram](ethernet_events.svg "Diagram")
## Description

This module instantiates multiple `event_counter` modules, one for each
Ethernet event defined in `ethernet_events.svh`. Event pulses are fed
into each counter, and the resulting values are assigned to individually
named debug registers.

**Key Features**
- Parameterizable counter width (`WIDTH`).
- All counters reset synchronously when `resetn` is low.

## Generics

| Generic name | Type | Value | Description                  |
| ------------ | ---- | ----- | ---------------------------- |
| WIDTH        | int  | 32    | Width of the counter in bits |

## Ports

| Port name   | Direction | Type                           | Description                         |
| ----------- | --------- | ------------------------------ | ----------------------------------- |
| clk         | input     | wire                           | Clock signal                        |
| resetn      | input     | wire                           | Synchronous active-low global reset |
| stats_reset | input     | wire                           | 1-bit reset for all stats           |
| events      | input     | wire  [_ETH_EVENT_COUNTER-1:0] | Event pulses                        |

## Signals

| Name                          | Type              | Description    |
| ----------------------------- | ----------------- | -------------- |
| counters [_ETH_EVENT_COUNTER] | logic [WIDTH-1:0] | counter values |
| tx_error_underflow_cnt = '0   | logic [WIDTH-1:0] | Debug purpose  |
| tx_fifo_overflow_cnt = '0     | logic [WIDTH-1:0] |                |
| tx_fifo_bad_frame_cnt = '0    | logic [WIDTH-1:0] |                |
| tx_fifo_good_frame_cnt = '0   | logic [WIDTH-1:0] |                |
| rx_error_bad_frame_cnt = '0   | logic [WIDTH-1:0] |                |
| rx_error_bad_fcs_cnt = '0     | logic [WIDTH-1:0] |                |
| rx_fifo_overflow_cnt = '0     | logic [WIDTH-1:0] |                |
| rx_fifo_bad_frame_cnt = '0    | logic [WIDTH-1:0] |                |
| rx_fifo_good_frame_cnt = '0   | logic [WIDTH-1:0] |                |

## Processes
- counter_assignment: ( @( posedge clk ) )
  - **Type:** always_ff

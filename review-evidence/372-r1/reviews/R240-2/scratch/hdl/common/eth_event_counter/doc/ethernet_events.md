
# Entity: ethernet_events 
- **File**: ethernet_events.sv

## Contents

- **[Diagram](#diagram)** — The rendered block diagram (`ethernet_events.svg`), if you want the shape before the tables.
- **[Description](#description)** — What the module is in one paragraph: a bank of `event_counter` instances, one per event declared in `ethernet_events.svh`, each landing in its own named register.
- **[Generics](#generics)** — Just `WIDTH` (32) — the counter width, hence where they saturate.
- **[Ports](#ports)** — Four signals. Worth noting `stats_reset` is separate from `resetn`, so software can zero the statistics without resetting the block, and `events` is one pulse lane per counter.
- **[Signals](#signals)** — The list of counter names, which is effectively the RMON lane inventory this block can produce: TX underflow / FIFO overflow / bad-frame / good-frame and their four RX counterparts.
- **[Processes](#processes)** — One `always_ff` that maps the counter array onto the named registers.

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

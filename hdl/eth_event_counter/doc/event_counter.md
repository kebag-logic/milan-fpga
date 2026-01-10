
# Entity: event_counter 
- **File**: event_counter.sv

## Diagram
![Diagram](event_counter.svg "Diagram")
## Description

This module implements a simple synchronous event counter.
The counter width is configurable via the `WIDTH` parameter.
When `incr` is high for one or more clock cycles, the counter
increments by 1 on each high cycle.

Two types of reset are available:
- **Global reset (`resetn`)**: Clears all counters at system reset.
- **Stats reset (`stats_reset`)**: Clears counters without affecting
the rest of the logic (useful for periodic stats collection).

## Generics

| Generic name | Type | Value | Description                  |
| ------------ | ---- | ----- | ---------------------------- |
| WIDTH        | int  | 32    | Width of the counter in bits |

## Ports

| Port name   | Direction | Type        | Description                         |
| ----------- | --------- | ----------- | ----------------------------------- |
| clk         | input     | wire        | Clock signal                        |
| resetn      | input     | wire        | Synchronous active-low global reset |
| stats_reset | input     | wire        | Counter-only reset (active high)    |
| incr        | input     | wire        | Increment signal                    |
| count       | output    | [WIDTH-1:0] | Current counter value               |

## Processes
- count_event: ( @( posedge clk ) )
  - **Type:** always_ff


# Entity: timestamp_counter 
- **File**: timestamp_counter.sv

## Diagram
![Diagram](timestamp_counter.svg "Diagram")
## Generics

| Generic name  | Type | Value | Description                                                        |
| ------------- | ---- | ----- | ------------------------------------------------------------------ |
| COUNTER_WIDTH | int  | 64    | Width of the counter                                               |
| STEP_SIZE     | int  | 8     | Step size per clock cycle (e.g., 8 for 125 MHz = 8 ns resolution). |

## Ports

| Port name     | Direction | Type                     | Description                             |
| ------------- | --------- | ------------------------ | --------------------------------------- |
| clk           | input     | wire                     | src clock input                         |
| resetn        | input     | wire                     | Active low synchronous reset            |
| timestamp_out | output    | wire [COUNTER_WIDTH-1:0] | Current timestamp output (nanoseconds). |

## Signals

| Name      | Type                      | Description               |
| --------- | ------------------------- | ------------------------- |
| timestamp | logic [COUNTER_WIDTH-1:0] | Internal counter register |

## Processes
- timestamp_counter: ( @(posedge clk ) )
  - **Type:** always_ff
  - **Description**
  Assign output.  Timestamp coutner logic: increment on each clock cycle and overflows. 


# Entity: KL_advertise_controller 
- **File**: KL_advertise_controller.sv

## Diagram
![Diagram](KL_advertise_controller.svg "Diagram")
## Ports

| Port name          | Direction | Type                  | Description                                                                             |
| ------------------ | --------- | --------------------- | --------------------------------------------------------------------------------------- |
| clk_i              | input     | wire                  | Global clock                                                                            |
| rst_n              | input     | wire                  | Active-low Reset                                                                        |
| rcv_entity_id_i    | input     | wire [63:0]           | entity_info.rcv_entity_id - from KL_adp_parser                                          |
| entity_id_i        | input     | wire [63:0]           | entity_id of the ATDECC entity - from memory map                                        |
| grandmaster_id_i   | input     | wire [63:0]           | grandmaster_id - from PTP module                                                        |
| rcv_adp_discover_i | input     | wire                  | ADP Discovery packet is received and rcv_entity_id_i field is valid- from KL_adp_parser |
| link_status_i      | input     | link_status_t         | Link Status related inputs from Upper Management Module                                 |
| tmr_events_i       | input     | tmr_events_t          | ADP Timer events inputs                                                                 |
| advertise_event_o  | output    | adp_advertise_event_t | All Advertise related event - to KL_advertise_state                                     |

## Signals

| Name                      | Type                        | Description                                    |
| ------------------------- | --------------------------- | ---------------------------------------------- |
| grandmaster_id_r          | reg [63:0]                  | GM_EVENT related registers                     |
| zero_four_sec_cnt_r       | reg [clog2(MAX_SECOND)-1:0] | TMR_DELAY and TMR_ADVERTISE related registers. |
| delay_value_r             | reg [clog2(MAX_SECOND)-1:0] | Register that takes the value from 0 to 4.     |
| start_tmr_delay_cnt_r     | reg                         | Start signal for KL_counter.                   |
| tmr_advertise_completed_r | reg                         | TMR_ADVERTISE_COUNTER finished counting.       |
| tmr_delay_completed_r     | reg                         | TMR_DELAY_COUNTER finished counting.           |

## Processes
- counter_logic: ( @(posedge clk_i) )
  - **Type:** always_ff
  - **Description**
  Free-running counter logic - value in between 0-4
 
- tmr_delay_process: ( @(posedge clk_i) )
  - **Type:** always_ff
  - **Description**
  Process for assigning the delay value for TMR_DELAY_COUNTER
 
- grandmaster_control: ( @(posedge clk_i) )
  - **Type:** always_ff
  - **Description**
  Process for checking whether grandmaster_id has changed
  for the ATDECC Entity.
 

## Instantiations

- TMR_ADVERTISE_COUNTER: KL_counter
  -  Advertise counter - Static 5 sec delay
- TMR_DELAY_COUNTER: KL_counter
  -  Delay counter - random value between 0-4 delay

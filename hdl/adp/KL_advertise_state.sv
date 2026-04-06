/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_advertise_state.sv
  Author      : Cemal Dogan

                cemal.dogan@kebag-logic.com

  Date        : 2025-05-10
  Description : Responsible for taking care of the Advertise State Machine in Milan
                Specs v1.2 Clause 5.6.3.
                Having three states, namely, DOWN, WAITING and DELAY

  Company     : Kebag Logic
  Project     : Milan ADP

------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import adp_pkg::*;

module KL_advertise_state
  (
    input wire clk_i,
    input wire rst_n,
    input entity_info_t mmap_entity_info_i,
    input adp_advertise_event_t advertise_event_i,
    input wire [63:0] grandmaster_id_i,
    input wire [7:0] gptp_domain_number_i,

    output tmr_events_t tmr_events_o,
    axi_stream_if.master m_axis
  );

  //! Expected data count on ADP packet.
  localparam [3:0] MAX_DATA_CNT_C = 4'd8;

  typedef enum bit [1:0] {
    LINK_DOWN_S,
    DELAY_S,
    WAITING_S
  } state_advertise_t;

  typedef enum bit {
    COMMAND_S,
    ENCAPSULATE_S
  } state_encap_t;

  state_advertise_t state_advertise, state_advertise_next;
  state_encap_t state_encap;
  entity_info_t mmap_entity_info_r;
  reg [3:0] data_counter_r;

  wire send_available_w;
  wire send_departing_w;
  //! Send ADP Entity Departing when shutdown event received
  //! in WAITING or DELAY state
  assign send_departing_w = ((state_advertise == WAITING_S || state_advertise == DELAY_S) && advertise_event_i.SHUTDOWN);
  //! Send the Entity_available packet, when TMR_DELAY event received
  //! in DELAY state
  assign send_available_w = (state_advertise == DELAY_S && advertise_event_i.TMR_DELAY);

  //! Start the TMR DELAY counter when;
  //! LINK_UP event received in LINK_DOWN state ||
  //! RCV_ADP_DISCOVER event received in WAITING state ||
  //! TMR_ADVERTISE event received in WAITING state ||
  //! GM_CHANGE event received in WAITING state
  assign tmr_events_o.start_tmr_delay = ((state_advertise == LINK_DOWN_S && advertise_event_i.LINK_UP) || 
  (state_advertise == WAITING_S && (advertise_event_i.RCV_ADP_DISCOVER || advertise_event_i.TMR_ADVERTISE || advertise_event_i.GM_CHANGE)));

  //! Stop the TMR DELAY counter when;
  //! LINK_DOWN or SHUTDOWN event occur in DELAY state
  assign tmr_events_o.stop_tmr_delay = (state_advertise == DELAY_S && (advertise_event_i.LINK_DOWN || 
                             advertise_event_i.SHUTDOWN));

  //! Start the TMR ADVERTISE counter when;
  //! TMR_DELAY event received in DELAY state
  assign tmr_events_o.start_tmr_advertise = (state_advertise == DELAY_S && advertise_event_i.TMR_DELAY);

  //! Stop the TMR ADVERTISE counter when;
  //! RCV_ADP_DISCOVER or LINK_DOWN or SHUTDOWN event received
  //! in WAITING STATE
  assign tmr_events_o.stop_tmr_advertise = ((state_advertise == WAITING_S && (advertise_event_i.RCV_ADP_DISCOVER ||
                                 advertise_event_i.LINK_DOWN || advertise_event_i.SHUTDOWN)));

  assign m_axis.tlast = (data_counter_r == MAX_DATA_CNT_C);
  assign m_axis.tkeep = (data_counter_r == MAX_DATA_CNT_C) ? 8'hFC : 8'hFF;


  always_ff @(posedge clk_i) begin
    if (!rst_n) state_advertise <= LINK_DOWN_S;
    else state_advertise <= state_advertise_next;
  end

  always_comb begin : advertise_state_machine
    state_advertise_next = state_advertise;
    case (state_advertise)

      LINK_DOWN_S : begin
        if (advertise_event_i.LINK_UP)
          state_advertise_next = DELAY_S;
      end

      DELAY_S : begin
        if (advertise_event_i.LINK_DOWN || advertise_event_i.SHUTDOWN)
          state_advertise_next = LINK_DOWN_S;
        else if (advertise_event_i.TMR_DELAY)
          state_advertise_next = WAITING_S;
        else 
          state_advertise_next = DELAY_S;
      end

      WAITING_S : begin
        if (advertise_event_i.LINK_DOWN || advertise_event_i.SHUTDOWN)
          state_advertise_next = LINK_DOWN_S;
        else if (advertise_event_i.RCV_ADP_DISCOVER || advertise_event_i.TMR_ADVERTISE || advertise_event_i.GM_CHANGE)
          state_advertise_next = DELAY_S;
        else 
          state_advertise_next = WAITING_S;
      end

      default : state_advertise_next = LINK_DOWN_S;

    endcase
  end


  /*
    Process for ensapsulation of ENTITY_AVAILABLE/ENTITY_DEPARTING packets
  */

  always_ff @(posedge clk_i) begin : encapsulation_state
    if (!rst_n) begin
      m_axis.tdata <= '0;
      m_axis.tvalid <= 1'd0;
      data_counter_r <= 4'd0;
      state_encap <= COMMAND_S;
    end
    else begin
      case (state_encap)

        COMMAND_S : begin
          if (send_available_w) begin
            m_axis.tdata[63:40] <= {AVTP_ETHERNET_TYPE_C, ADP_SUBTYPE_C};
            m_axis.tdata[39:0] <= {SV_VER_MSG_TYPE_AVAILABLE_C, mmap_entity_info_r.valid_time, CTRL_DATA_LENGTH_C, mmap_entity_info_r.entity_id[63:48]};
            m_axis.tvalid <= 1'd1;
            state_encap <= ENCAPSULATE_S;
          end
          if (send_departing_w) begin
            m_axis.tdata[63:40] <= {AVTP_ETHERNET_TYPE_C, ADP_SUBTYPE_C};
            m_axis.tdata[39:0] <= {SV_VER_MSG_TYPE_DEPARTING_C, mmap_entity_info_r.valid_time, CTRL_DATA_LENGTH_C, mmap_entity_info_r.entity_id[63:48]};
            m_axis.tvalid <= 1'd1;
            state_encap <= ENCAPSULATE_S;
          end
        end

        ENCAPSULATE_S : begin
          if (m_axis.tvalid & m_axis.tready) begin
            case (data_counter_r)

              0 : begin // 4th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_r.entity_id[47:0], mmap_entity_info_r.entity_model_id[63:48]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              1 : begin // 5th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_r.entity_model_id[47:0], mmap_entity_info_r.entity_capabilities[31:16]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              2 : begin // 6th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_r.entity_capabilities, mmap_entity_info_r.talker_stream_sources, mmap_entity_info_r.talker_capabilities, mmap_entity_info_i.listener_stream_sinks};
                data_counter_r <= data_counter_r + 4'd1;
              end

              3 : begin // 7th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_r.listener_capabilities, mmap_entity_info_r.controller_capabilities, mmap_entity_info_r.available_index[31:16]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              4 : begin // 8th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_r.available_index[15:0], grandmaster_id_i[63:16]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              5 : begin // 9th 64-bit transaction
                m_axis.tdata <= {grandmaster_id_i[15:0], gptp_domain_number_i, 8'd0, mmap_entity_info_r.current_configuration_index, mmap_entity_info_i.identify_control_index};
                data_counter_r <= data_counter_r + 4'd1;
              end

              6 : begin // 10th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_r.interface_index, mmap_entity_info_r.association_id[63:16]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              7 : begin // 11th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_r.association_id[15:0], 48'd0};
                data_counter_r <= data_counter_r + 4'd1;
              end

              8 : begin
                data_counter_r <= 4'd0;
                m_axis.tvalid <= 1'd0;
                m_axis.tdata <= '0;
                state_encap <= COMMAND_S;
              end
              default data_counter_r <= 4'd0;
            endcase
          end
        end
        default : state_encap <= COMMAND_S;
      endcase
    end
  end

  //! Catch the entity_info_tvalid strobe from input and register the mmap structure
  always_ff @(posedge clk_i) begin : mmap_entity_info
    if (!rst_n) mmap_entity_info_r <= '0;
    else begin
      if (mmap_entity_info_i.entity_info_valid) 
      mmap_entity_info_r <= mmap_entity_info_i;
    end
  end

endmodule

`default_nettype wire
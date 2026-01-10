/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_avtp_common_parser.sv
  Author      : Cemal Dogan, Oguz Kahraman

                cemal.dogan@kebag-logic.com
                oguz.kahraman@kebag-logic.com

  Date        : 2025-03-20
  Description : Get the AVTP common header (Big endian ETH packets - 
                Starting from the EthernetType - 22F0 + AVTPDU common headers + ...
                e.g first STREAM DATA contains --> S_AXIS_TDATA[63:48]= EthernetType, S_AXIS_TDATA[47:40]=subtype)
                to identify the received packets, convey
                the following control/stream and alternative packets to the logic;
                  Supported Control Packets -- ADP, AECP, ACPM and MAAP
                  Supported Stream Packets -- 61883_IIDC, MMA_STREAM, AAF
                  Supported Alternative Packets -- CRF
                Discard the rest of the AVTP packets received.
                TDEST port of the AXI4-Stream Master indicates the packet type;
                0 - Supported Control Packet 
                1 - Supported Stream Packet
                2 - Supported Alternative Packet
                3 - Others
                TUSER port of the AXI4-Stream Master dedicated for the Received Subtype

  Company     : Kebag Logic
  Project     : Milan ADP

------------------------------------------------------------------------------
*/

`default_nettype none
import avtp_subtype_pkg::*;

module KL_avtp_common_parser #(
  parameter int TDATA_WIDTH = 64,
  parameter int PIPELINE_DELAY = 1
)(
  input wire clk_i, //! Global clock
  input wire rst_n, //! Active-low Reset
    
  axi_stream_if.slave s_axis, //! AXI4-Stream Slave interface
  axi_stream_if.master m_axis //! AXI4-Stream Master interface for FIFO
);

  initial begin
      assert (PIPELINE_DELAY >= 1) else $error("PIPELINE_DELAY must be >= 1");
  end

  //! Supported Control Packets;
  //! ADP - AECP - ACMP - MAAP

  //! Supported Stream Packets;
  //! IIDC, MMA_STREAM, AAF

  //! Supported Alternative Packets;
  //! CRF

  typedef enum bit {
    IDLE_S,
    WAIT_S
  } state_t;

  state_t parser_state;
  //! Received subtype field from Slave AXIS
  reg [7:0] rcvd_subtype_r;

  //! Create pipeline registers
  logic [TDATA_WIDTH-1:0] tdata_pipe [0:PIPELINE_DELAY];
  logic [TDATA_WIDTH/8-1:0] tkeep_pipe [0:PIPELINE_DELAY];
  logic tvalid_pipe [0:PIPELINE_DELAY];
  logic tlast_pipe [0:PIPELINE_DELAY];
  logic tready_pipe [0:PIPELINE_DELAY];

  //! Skid buffer for backward path
  logic [TDATA_WIDTH-1:0] skid_data;
  logic [TDATA_WIDTH/8-1:0] skid_keep;
  logic skid_last;
  logic skid_valid;
  //! For loop constant
  int i;
  int k;
  //! Registered downstream ready
  logic m_ready_reg;

  assign m_axis.tdata = skid_valid ? skid_data : tdata_pipe[PIPELINE_DELAY];
  assign m_axis.tlast = (m_axis.tdest != 'h3) ? (skid_valid ? skid_last : tlast_pipe[PIPELINE_DELAY]) : 0;
  assign m_axis.tkeep = skid_valid ? skid_keep : tkeep_pipe[PIPELINE_DELAY];
  assign m_axis.tvalid = ((m_axis.tdest != 'h3) && (skid_valid || tvalid_pipe[PIPELINE_DELAY]));
  assign m_axis.tuser = rcvd_subtype_r;
  assign s_axis.tready = tready_pipe[0];
  assign tready_pipe[PIPELINE_DELAY] = !skid_valid || m_axis.tready;

  always_ff @(posedge clk_i) begin : skid_buffer_logic
    if(!rst_n)begin
      skid_data <= 'd0;
      skid_keep <= 'd0;
      skid_last <= 'd0;
      skid_valid <= 'd0;
    end
    else begin
      m_ready_reg <= m_axis.tready;
      if(tvalid_pipe[PIPELINE_DELAY] && !m_ready_reg && !skid_valid)begin
        skid_data <= tdata_pipe[PIPELINE_DELAY];
        skid_keep <= tkeep_pipe[PIPELINE_DELAY];
        skid_last <= tlast_pipe[PIPELINE_DELAY];
        skid_valid <= 'd1;
      end
      else if(skid_valid && m_axis.tready)begin
        skid_valid <= 'd0;
      end
    end
  end : skid_buffer_logic

  always_ff @(posedge clk_i)begin : input_pipeline
    if(!rst_n)begin
      for(i=0; i<=PIPELINE_DELAY; i++)begin
        tdata_pipe[i] <= 'd0;
        tkeep_pipe[i] <= 'd0;
        tvalid_pipe[i] <= 'd0;
        tlast_pipe[i] <= 'd0;
      end
    end
    else begin
      if(tready_pipe[0])begin
        tdata_pipe[0] <= s_axis.tdata;
        tkeep_pipe[0] <= s_axis.tkeep;
        tvalid_pipe[0] <= s_axis.tvalid;
        tlast_pipe[0] <= s_axis.tlast;
      end
      for(i=1; i<=PIPELINE_DELAY; i++)begin
        if(tready_pipe[i])begin
          tdata_pipe[i] <= tdata_pipe[i-1];
          tkeep_pipe[i] <= tkeep_pipe[i-1];
          tvalid_pipe[i] <= tvalid_pipe[i-1];
          tlast_pipe[i] <= tlast_pipe[i-1];
        end
      end
    end
  end : input_pipeline

  //! Propagate tready backward through pipeline
  always_comb begin : tready_pipeline
    for (k = 0; k < PIPELINE_DELAY; k++) begin
      //! Stage can accept data if it is empty or next stage is ready
      tready_pipe[k] = !tvalid_pipe[k] || tready_pipe[k+1];
    end
  end : tready_pipeline

  //! Handle the TDEST[1:0] w.r.t control, alternative or stream
  //! h0 : Packet Control 
  //! h1 : Packet Stream
  //! h2 : Packet Alternative
  //! h3 : Not supported, not transmitted
  always_comb begin : tdest_assign
    case (rcvd_subtype_r)
      ADP, AECP, ACMP, MAAP: m_axis.tdest = 'h0;
      IIDC, MMA_STREAM, AAF: m_axis.tdest = 'h1;
      CRF : m_axis.tdest = 'h2;
      default : m_axis.tdest = 'h3;
    endcase
  end : tdest_assign

  //! Receive the AVTP packets starting from the EthernetType
  //! Transmit the supported AVTP packets, discard the ones not
  //! supported in this version of the code.
  always_ff @(posedge clk_i) begin : subtype_save_logic
    if (!rst_n) begin
      parser_state <= IDLE_S;
      rcvd_subtype_r <= 8'd0;
    end
    else begin
      case (parser_state)
        IDLE_S : begin
          if (s_axis.tvalid) begin
            rcvd_subtype_r <= s_axis.tdata[47:40];
            parser_state <= WAIT_S;
          end
        end

        WAIT_S : begin
          if (s_axis.tready & s_axis.tvalid & s_axis.tlast) parser_state <= IDLE_S;
        end

        default : begin
          parser_state <= IDLE_S;
        end
      endcase
    end
  end : subtype_save_logic

endmodule

`default_nettype wire

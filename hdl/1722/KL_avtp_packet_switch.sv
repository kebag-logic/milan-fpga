/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_avtp_common_parser.sv
  Author      : Cemal Dogan, Maximilien Pinaud

                cemal.dogan@kebag-logic.com

  Date        : 2025-03-20
  Description : The module is used to route the AXI stream packets depending on their TDEST value to the matching destinations port. Each output AXI master interface has an associated TDEST value that is being parsed in real time.

  Company     : Kebag Logic
  Project     : Milan ADP

------------------------------------------------------------------------------
*/
`default_nettype none
module KL_avtp_packet_switch # (
    parameter bit IN_REG                     = 1,          //! Enable input stream registering
    parameter bit OUT_REG                    = 1,          //! Enable output stream registering
    parameter int FIFO_DEPTH                 = 128,        //! The depth in terms of samples of the FIFO
    parameter int NUM_M_AXIS_IF              = 3,          //! Number of axis stream master interfaces
    parameter int PORT_VALUES[NUM_M_AXIS_IF] = '{1, 2, 3}  //! Array defining the tdest values for each master axis interface 
    )(
    input wire              clk_i, resetn_i,               //! Clock and Reset Signals 
    axi_stream_if.slave     s_axis,                        //! AXI4-Stream Slave interface
    axi_stream_if.master    m_axis[NUM_M_AXIS_IF]          //! AXI4-Stream Master interface
);


localparam int TDATA_WIDTH = $bits(s_axis.tdata);
localparam int TUSER_WIDTH = $bits(s_axis.tuser);
localparam int TDEST_WIDTH = $bits(s_axis.tdest);
localparam int TID_WIDTH   = $bits(s_axis.tid);
localparam int TKEEP_WIDTH = TDATA_WIDTH/8;

typedef struct packed{
    logic [TDATA_WIDTH-1:0]     tdata;
    logic [TKEEP_WIDTH-1:0]     tkeep;
    logic [TDEST_WIDTH-1:0]     tdest;
    logic [TUSER_WIDTH-1:0]     tuser;
    logic [TID_WIDTH-1:0]       tid;
    logic [TKEEP_WIDTH-1:0]     tstrb;
    logic                       tvalid;
    logic                       tlast;
    logic                       tready;
} axis_t;

initial begin 
    //! Check for duplicate port values on instantiation of the module
    for (int i = 0; i < NUM_M_AXIS_IF; i++) begin
        for (int j = i + 1; j < NUM_M_AXIS_IF; j++) begin
            if (PORT_VALUES[i] == PORT_VALUES[j]) begin
                $fatal(1,
                    "ERROR: PORT_VALUES has duplicate entries: [%0d]=%0d and [%0d]=%0d",
                    i, PORT_VALUES[i], j, PORT_VALUES[j]);
            end
        end
    end
    //! Check that the number of axi interfaces is grater than 0
    assert (NUM_M_AXIS_IF > 0) else  
    $error("There should be at least on PORT value to instantiate one output port");
    //! Check that fifo depth value is correct
    assert (FIFO_DEPTH > 0 && (FIFO_DEPTH%16 == 0)) else 
    $error("FIFO size should be larger than 0 and a power of 2");
end 

axis_t wi_fifo, wo_fifo;
logic fifo_ready;

generate
    if(|IN_REG)
    begin
        //! When the input registering is enable a skid buffer is generated
        axis_t fifo_data, fifo_hold;
        logic in_full;
        always_ff@(posedge clk_i)
        begin
            if(!resetn_i)
            begin
                in_full         <= 'b0;
            end
            else
            begin
                fifo_data.tdata <= s_axis.tdata;
                fifo_data.tkeep <= s_axis.tkeep;
                fifo_data.tdest <= s_axis.tdest;
                fifo_data.tuser <= s_axis.tuser;
                fifo_data.tid   <= s_axis.tid;
                fifo_data.tstrb <= s_axis.tstrb;
                fifo_data.tvalid<= s_axis.tvalid;
                fifo_data.tlast <= s_axis.tlast;
                if(wi_fifo.tready)
                begin
                    in_full     <= 'b0;
                end
                else if (fifo_data.tvalid && !wi_fifo.tready && !in_full)
                begin
                    in_full     <= 1'b1;
                    fifo_hold   <= fifo_data;
                end
            end
        end
        always_comb begin
            wi_fifo        <= (in_full) ? fifo_hold : fifo_data;
            wi_fifo.tready <= fifo_ready;
        end
        assign s_axis.tready = !in_full;
    end
    else
    begin
        //! When the input registering is disabled connect to port directly
        assign wi_fifo.tdata = s_axis.tdata;
        assign wi_fifo.tkeep = s_axis.tkeep;
        assign wi_fifo.tdest = s_axis.tdest;
        assign wi_fifo.tuser = s_axis.tuser;
        assign wi_fifo.tid   = s_axis.tid;
        assign wi_fifo.tstrb = s_axis.tstrb;
        assign wi_fifo.tvalid= s_axis.tvalid;
        assign wi_fifo.tlast = s_axis.tlast;
        assign wi_fifo.tready= fifo_ready;
        assign s_axis.tready = wi_fifo.tready;
    end
endgenerate

//! axi streaming fifo instantiation
xpm_fifo_axis #(
.CLOCKING_MODE("common_clock"),
.FIFO_DEPTH(FIFO_DEPTH),
.FIFO_MEMORY_TYPE("auto"),
.PACKET_FIFO("false"),
.TDATA_WIDTH(TDATA_WIDTH),
.TUSER_WIDTH(TUSER_WIDTH),
.TDEST_WIDTH(TDEST_WIDTH),
.TID_WIDTH(TID_WIDTH)

)
xpm_fifo_axis_inst_A(
.s_aclk(clk_i),
.s_aresetn(resetn_i),

.s_axis_tdata   (wi_fifo.tdata),
.s_axis_tkeep   (wi_fifo.tkeep),
.s_axis_tlast   (wi_fifo.tlast),
.s_axis_tready  (fifo_ready),
.s_axis_tvalid  (wi_fifo.tvalid),
.s_axis_tdest   (wi_fifo.tdest),
.s_axis_tuser   (wi_fifo.tuser),
.s_axis_tid     (wi_fifo.tid),
.s_axis_tstrb   (wi_fifo.tstrb),

.m_axis_tdata   (wo_fifo.tdata),
.m_axis_tkeep   (wo_fifo.tkeep),
.m_axis_tlast   (wo_fifo.tlast),
.m_axis_tready  (wo_fifo.tready),
.m_axis_tvalid  (wo_fifo.tvalid),
.m_axis_tdest   (wo_fifo.tdest),
.m_axis_tuser   (wo_fifo.tuser),
.m_axis_tid     (wo_fifo.tid),
.m_axis_tstrb   (wo_fifo.tstrb)
);

//! Function used to verify if one hot encoding can be used on the output
function automatic bit is_contiguous(input int arr[], input int n);
    for (int i = 1; i < n; i++) begin
        if (arr[i-1] != i)
            return 0;
    end
    return 1;
endfunction

//! If data is not contiguous the user is warned
initial begin
    if (!is_contiguous(PORT_VALUES, NUM_M_AXIS_IF)) begin
        $warning(1, "WARNING: PORT_VALUES are not contiguous. Cannot use shift-based one-hot decode.");
    end
end
localparam bit USE_SHIFT_DECODE = is_contiguous(PORT_VALUES, NUM_M_AXIS_IF);

//! Based on the tdest value a interface is selected via the sel variable
logic [NUM_M_AXIS_IF:0] sel;
logic [NUM_M_AXIS_IF-1:0] hold_sel, out_sel,valid_sel;
assign valid_sel = sel[NUM_M_AXIS_IF:1] & {NUM_M_AXIS_IF{wo_fifo.tvalid}};
generate
    if(|USE_SHIFT_DECODE)
    begin
        //! one hot encoding to select the output port
        assign sel = (1 << wo_fifo.tdest);
    end
    else
    begin
        //! comparator to select the output port (less performance)
        for (genvar i = 0; i < NUM_M_AXIS_IF; i++) 
        begin : GEN_DECODE
            assign sel[i+1] = (wo_fifo.tdest == PORT_VALUES[i]);
        end
    end
endgenerate

//! skid buffer in order to register data and avoid a high fanout
logic full, m_axis_tready;
assign wo_fifo.tready = !full;
axis_t hold_data, r_data;
always_ff@(posedge clk_i)
begin
    if(!resetn_i)
    begin
        full <= 'b0;
    end
    else
    begin
        r_data          <= (!full) ? wo_fifo : r_data;
        out_sel         <= (!full) ? valid_sel : out_sel;
        if (m_axis_tready)
        begin
            full        <= 'b0;
        end
        else if (r_data.tvalid && !m_axis_tready && !full)
        begin
            full        <= 1'b1;
            hold_data   <= r_data;
            hold_sel    <= out_sel;
        end
    end
end

//! Combinatorial tready check
logic [NUM_M_AXIS_IF-1:0] tready_vec, out_full;
axis_t [NUM_M_AXIS_IF-1:0] r_axis;
generate 
    if(|OUT_REG)
    begin
        for (genvar i = 0; i < NUM_M_AXIS_IF; i++) begin
            assign tready_vec[i] = (full) ? 
                                   !out_full[i] && hold_sel[i] : 
                                   !out_full[i] && out_sel[i];
        end
    end
    else
    begin
        for (genvar i = 0; i < NUM_M_AXIS_IF; i++) begin
            assign tready_vec[i] = (full) ? 
                                   r_axis[i].tready && hold_sel[i] : 
                                   r_axis[i].tready && out_sel[i];
        end
    end
endgenerate
assign m_axis_tready = |tready_vec;

generate 
    for (genvar i = 0; i < NUM_M_AXIS_IF; i++) begin : GEN_PORTS
        always_comb begin
            r_axis[i].tdata  <= (full) ? hold_data.tdata : r_data.tdata;
            r_axis[i].tuser  <= (full) ? hold_data.tuser : r_data.tuser;
            r_axis[i].tlast  <= (full) ? hold_data.tlast : r_data.tlast;
            r_axis[i].tdest  <= (full) ? hold_data.tdest : r_data.tdest;
            r_axis[i].tid    <= (full) ? hold_data.tid   : r_data.tid;
            r_axis[i].tstrb  <= (full) ? hold_data.tstrb : r_data.tstrb;
            r_axis[i].tvalid <= (full) ? hold_sel[i]     : out_sel[i];
            r_axis[i].tkeep  <= (full) ? hold_data.tkeep : r_data.tkeep;
        end
        if(|OUT_REG)
        begin
            //! When the output registering is enable a skid buffer is generated for each interface
            axis_t [NUM_M_AXIS_IF-1:0] out_hold, out_data;
            always_ff@(posedge clk_i)
            begin
                if(!resetn_i)
                begin
                    out_full[i]         <= 'b0;
                end
                else
                begin
                    out_data[i] <= (!out_full[i])? r_axis[i] : out_data[i]; 
                    if(r_axis[i].tready)
                    begin
                        out_full[i]     <= 'b0;
                    end
                    else if (out_data[i].tvalid && !r_axis[i].tready && !out_full[i])
                    begin
                        out_full[i]     <= 1'b1;
                        out_hold[i]     <= out_data[i];
                    end
                end
            end
            assign m_axis[i].tdata  = (out_full[i]) ? out_hold[i].tdata  : out_data[i].tdata;
            assign m_axis[i].tuser  = (out_full[i]) ? out_hold[i].tuser  : out_data[i].tuser; 
            assign m_axis[i].tlast  = (out_full[i]) ? out_hold[i].tlast  : out_data[i].tlast; 
            assign m_axis[i].tdest  = (out_full[i]) ? out_hold[i].tdest  : out_data[i].tdest; 
            assign m_axis[i].tid    = (out_full[i]) ? out_hold[i].tid    : out_data[i].tid;   
            assign m_axis[i].tstrb  = (out_full[i]) ? out_hold[i].tstrb  : out_data[i].tstrb; 
            assign m_axis[i].tvalid = (out_full[i]) ? out_hold[i].tvalid : out_data[i].tvalid;
            assign m_axis[i].tkeep  = (m_axis[i].tvalid) ? (out_full[i]) ? out_hold[i].tkeep  : out_data[i].tkeep : 'b0;
            assign r_axis[i].tready = m_axis[i].tready;
        end
        else
        begin
            assign m_axis[i].tdata  = r_axis[i].tdata;
            assign m_axis[i].tuser  = r_axis[i].tuser; 
            assign m_axis[i].tlast  = r_axis[i].tlast; 
            assign m_axis[i].tdest  = r_axis[i].tdest; 
            assign m_axis[i].tid    = r_axis[i].tid;   
            assign m_axis[i].tstrb  = r_axis[i].tstrb; 
            assign m_axis[i].tvalid = r_axis[i].tvalid;
            assign m_axis[i].tkeep  = (m_axis[i].tvalid) ? r_axis[i].tkeep : 'b0;
            assign r_axis[i].tready = m_axis[i].tready;
        end
    end
endgenerate

endmodule
`default_nettype wire

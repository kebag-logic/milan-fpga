

//                          / /  (_) /____ | |/_/
//                         / /__/ / __/ -_)>  <
//                        /____/_/\__/\__/_/|_|
//                     Build your hardware, easily!
//                   https://github.com/enjoy-digital/litex
//
// Filename   : bench.v
// Top        : Unknown
// Device     : Unknown
// Hierarchy  : disabled




`timescale 1ns / 1ps


// Module


module bench (
    input  wire          ar_first,
    output wire          ar_first_1,
    input  wire          ar_last,
    output wire          ar_last_1,
    input  wire   [31:0] ar_payload_addr,
    output wire   [31:0] ar_payload_addr_1,
    input  wire    [2:0] ar_payload_prot,
    output wire    [2:0] ar_payload_prot_1,
    output wire          ar_ready,
    input  wire          ar_ready_1,
    input  wire          ar_valid,
    output wire          ar_valid_1,
    input  wire          aw_first,
    output wire          aw_first_1,
    input  wire          aw_last,
    output wire          aw_last_1,
    input  wire   [31:0] aw_payload_addr,
    output wire   [31:0] aw_payload_addr_1,
    input  wire    [2:0] aw_payload_prot,
    output wire    [2:0] aw_payload_prot_1,
    output wire          aw_ready,
    input  wire          aw_ready_1,
    input  wire          aw_valid,
    output wire          aw_valid_1,
    output wire          b_first,
    input  wire          b_first_1,
    output wire          b_last,
    input  wire          b_last_1,
    output wire    [1:0] b_payload_resp,
    input  wire    [1:0] b_payload_resp_1,
    input  wire          b_ready,
    output wire          b_ready_1,
    output wire          b_valid,
    input  wire          b_valid_1,
    input  wire          macdp_clk,
    input  wire          macdp_rst,
    input  wire          macsys_clk,
    input  wire          macsys_rst,
    input  wire          milan_clk,
    input  wire          milan_rst,
    input  wire          r_first,
    output wire          r_first_1,
    input  wire          r_last,
    output wire          r_last_1,
    input  wire   [31:0] r_payload_data,
    output wire   [31:0] r_payload_data_1,
    input  wire    [1:0] r_payload_resp,
    output wire    [1:0] r_payload_resp_1,
    input  wire          r_ready,
    output wire          r_ready_1,
    output wire          r_valid,
    input  wire          r_valid_1,
    input  wire          sys_clk,
    input  wire          sys_rst,
    input  wire          w_first,
    output wire          w_first_1,
    input  wire          w_last,
    output wire          w_last_1,
    input  wire   [31:0] w_payload_data,
    output wire   [31:0] w_payload_data_1,
    input  wire    [3:0] w_payload_strb,
    output wire    [3:0] w_payload_strb_1,
    output wire          w_ready,
    input  wire          w_ready_1,
    input  wire          w_valid,
    output wire          w_valid_1
);



// Hierarchy




// Signals


wire   [36:0] ar_cdc_cdc_asyncfifo_din;
wire   [36:0] ar_cdc_cdc_asyncfifo_dout;
wire          ar_cdc_cdc_asyncfifo_re;
wire          ar_cdc_cdc_asyncfifo_readable;
wire          ar_cdc_cdc_asyncfifo_we;
wire          ar_cdc_cdc_asyncfifo_writable;
wire    [2:0] ar_cdc_cdc_consume_wdomain;
wire          ar_cdc_cdc_fifo_in_first;
wire          ar_cdc_cdc_fifo_in_last;
wire   [31:0] ar_cdc_cdc_fifo_in_payload_addr;
wire    [2:0] ar_cdc_cdc_fifo_in_payload_prot;
wire          ar_cdc_cdc_fifo_out_first;
wire          ar_cdc_cdc_fifo_out_last;
wire   [31:0] ar_cdc_cdc_fifo_out_payload_addr;
wire    [2:0] ar_cdc_cdc_fifo_out_payload_prot;
wire          ar_cdc_cdc_graycounter0_ce;
reg     [2:0] ar_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] ar_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] ar_cdc_cdc_graycounter0_q_next;
reg     [2:0] ar_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          ar_cdc_cdc_graycounter1_ce;
reg     [2:0] ar_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] ar_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] ar_cdc_cdc_graycounter1_q_next;
reg     [2:0] ar_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] ar_cdc_cdc_produce_rdomain;
wire    [1:0] ar_cdc_cdc_rdport_adr;
wire   [36:0] ar_cdc_cdc_rdport_dat_r;
wire          ar_cdc_cdc_sink_first;
wire          ar_cdc_cdc_sink_last;
wire   [31:0] ar_cdc_cdc_sink_payload_addr;
wire    [2:0] ar_cdc_cdc_sink_payload_prot;
wire          ar_cdc_cdc_sink_ready;
wire          ar_cdc_cdc_sink_valid;
wire          ar_cdc_cdc_source_first;
wire          ar_cdc_cdc_source_last;
wire   [31:0] ar_cdc_cdc_source_payload_addr;
wire    [2:0] ar_cdc_cdc_source_payload_prot;
wire          ar_cdc_cdc_source_ready;
wire          ar_cdc_cdc_source_valid;
wire    [1:0] ar_cdc_cdc_wrport_adr;
wire   [36:0] ar_cdc_cdc_wrport_dat_r;
wire   [36:0] ar_cdc_cdc_wrport_dat_w;
wire          ar_cdc_cdc_wrport_we;
wire          ar_cdc_sink_sink_first;
wire          ar_cdc_sink_sink_last;
wire   [31:0] ar_cdc_sink_sink_payload_addr;
wire    [2:0] ar_cdc_sink_sink_payload_prot;
wire          ar_cdc_sink_sink_ready;
wire          ar_cdc_sink_sink_valid;
wire          ar_cdc_source_source_first;
wire          ar_cdc_source_source_last;
wire   [31:0] ar_cdc_source_source_payload_addr;
wire    [2:0] ar_cdc_source_source_payload_prot;
wire          ar_cdc_source_source_ready;
wire          ar_cdc_source_source_valid;
wire   [36:0] aw_cdc_cdc_asyncfifo_din;
wire   [36:0] aw_cdc_cdc_asyncfifo_dout;
wire          aw_cdc_cdc_asyncfifo_re;
wire          aw_cdc_cdc_asyncfifo_readable;
wire          aw_cdc_cdc_asyncfifo_we;
wire          aw_cdc_cdc_asyncfifo_writable;
wire    [2:0] aw_cdc_cdc_consume_wdomain;
wire          aw_cdc_cdc_fifo_in_first;
wire          aw_cdc_cdc_fifo_in_last;
wire   [31:0] aw_cdc_cdc_fifo_in_payload_addr;
wire    [2:0] aw_cdc_cdc_fifo_in_payload_prot;
wire          aw_cdc_cdc_fifo_out_first;
wire          aw_cdc_cdc_fifo_out_last;
wire   [31:0] aw_cdc_cdc_fifo_out_payload_addr;
wire    [2:0] aw_cdc_cdc_fifo_out_payload_prot;
wire          aw_cdc_cdc_graycounter0_ce;
reg     [2:0] aw_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] aw_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] aw_cdc_cdc_graycounter0_q_next;
reg     [2:0] aw_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          aw_cdc_cdc_graycounter1_ce;
reg     [2:0] aw_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] aw_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] aw_cdc_cdc_graycounter1_q_next;
reg     [2:0] aw_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] aw_cdc_cdc_produce_rdomain;
wire    [1:0] aw_cdc_cdc_rdport_adr;
wire   [36:0] aw_cdc_cdc_rdport_dat_r;
wire          aw_cdc_cdc_sink_first;
wire          aw_cdc_cdc_sink_last;
wire   [31:0] aw_cdc_cdc_sink_payload_addr;
wire    [2:0] aw_cdc_cdc_sink_payload_prot;
wire          aw_cdc_cdc_sink_ready;
wire          aw_cdc_cdc_sink_valid;
wire          aw_cdc_cdc_source_first;
wire          aw_cdc_cdc_source_last;
wire   [31:0] aw_cdc_cdc_source_payload_addr;
wire    [2:0] aw_cdc_cdc_source_payload_prot;
wire          aw_cdc_cdc_source_ready;
wire          aw_cdc_cdc_source_valid;
wire    [1:0] aw_cdc_cdc_wrport_adr;
wire   [36:0] aw_cdc_cdc_wrport_dat_r;
wire   [36:0] aw_cdc_cdc_wrport_dat_w;
wire          aw_cdc_cdc_wrport_we;
wire          aw_cdc_sink_sink_first;
wire          aw_cdc_sink_sink_last;
wire   [31:0] aw_cdc_sink_sink_payload_addr;
wire    [2:0] aw_cdc_sink_sink_payload_prot;
wire          aw_cdc_sink_sink_ready;
wire          aw_cdc_sink_sink_valid;
wire          aw_cdc_source_source_first;
wire          aw_cdc_source_source_last;
wire   [31:0] aw_cdc_source_source_payload_addr;
wire    [2:0] aw_cdc_source_source_payload_prot;
wire          aw_cdc_source_source_ready;
wire          aw_cdc_source_source_valid;
wire    [3:0] b_cdc_cdc_asyncfifo_din;
wire    [3:0] b_cdc_cdc_asyncfifo_dout;
wire          b_cdc_cdc_asyncfifo_re;
wire          b_cdc_cdc_asyncfifo_readable;
wire          b_cdc_cdc_asyncfifo_we;
wire          b_cdc_cdc_asyncfifo_writable;
wire    [2:0] b_cdc_cdc_consume_wdomain;
wire          b_cdc_cdc_fifo_in_first;
wire          b_cdc_cdc_fifo_in_last;
wire    [1:0] b_cdc_cdc_fifo_in_payload_resp;
wire          b_cdc_cdc_fifo_out_first;
wire          b_cdc_cdc_fifo_out_last;
wire    [1:0] b_cdc_cdc_fifo_out_payload_resp;
wire          b_cdc_cdc_graycounter0_ce;
reg     [2:0] b_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] b_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] b_cdc_cdc_graycounter0_q_next;
reg     [2:0] b_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          b_cdc_cdc_graycounter1_ce;
reg     [2:0] b_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] b_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] b_cdc_cdc_graycounter1_q_next;
reg     [2:0] b_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] b_cdc_cdc_produce_rdomain;
wire    [1:0] b_cdc_cdc_rdport_adr;
wire    [3:0] b_cdc_cdc_rdport_dat_r;
wire          b_cdc_cdc_sink_first;
wire          b_cdc_cdc_sink_last;
wire    [1:0] b_cdc_cdc_sink_payload_resp;
wire          b_cdc_cdc_sink_ready;
wire          b_cdc_cdc_sink_valid;
wire          b_cdc_cdc_source_first;
wire          b_cdc_cdc_source_last;
wire    [1:0] b_cdc_cdc_source_payload_resp;
wire          b_cdc_cdc_source_ready;
wire          b_cdc_cdc_source_valid;
wire    [1:0] b_cdc_cdc_wrport_adr;
wire    [3:0] b_cdc_cdc_wrport_dat_r;
wire    [3:0] b_cdc_cdc_wrport_dat_w;
wire          b_cdc_cdc_wrport_we;
wire          b_cdc_sink_sink_first;
wire          b_cdc_sink_sink_last;
wire    [1:0] b_cdc_sink_sink_payload_resp;
wire          b_cdc_sink_sink_ready;
wire          b_cdc_sink_sink_valid;
wire          b_cdc_source_source_first;
wire          b_cdc_source_source_last;
wire    [1:0] b_cdc_source_source_payload_resp;
wire          b_cdc_source_source_ready;
wire          b_cdc_source_source_valid;
reg     [2:0] multiregimpl00 = 3'd0;
reg     [2:0] multiregimpl01 = 3'd0;
reg     [2:0] multiregimpl10 = 3'd0;
reg     [2:0] multiregimpl11 = 3'd0;
reg     [2:0] multiregimpl20 = 3'd0;
reg     [2:0] multiregimpl21 = 3'd0;
reg     [2:0] multiregimpl30 = 3'd0;
reg     [2:0] multiregimpl31 = 3'd0;
reg     [2:0] multiregimpl40 = 3'd0;
reg     [2:0] multiregimpl41 = 3'd0;
reg     [2:0] multiregimpl50 = 3'd0;
reg     [2:0] multiregimpl51 = 3'd0;
reg     [2:0] multiregimpl60 = 3'd0;
reg     [2:0] multiregimpl61 = 3'd0;
reg     [2:0] multiregimpl70 = 3'd0;
reg     [2:0] multiregimpl71 = 3'd0;
reg     [2:0] multiregimpl80 = 3'd0;
reg     [2:0] multiregimpl81 = 3'd0;
reg     [2:0] multiregimpl90 = 3'd0;
reg     [2:0] multiregimpl91 = 3'd0;
wire   [35:0] r_cdc_cdc_asyncfifo_din;
wire   [35:0] r_cdc_cdc_asyncfifo_dout;
wire          r_cdc_cdc_asyncfifo_re;
wire          r_cdc_cdc_asyncfifo_readable;
wire          r_cdc_cdc_asyncfifo_we;
wire          r_cdc_cdc_asyncfifo_writable;
wire    [2:0] r_cdc_cdc_consume_wdomain;
wire          r_cdc_cdc_fifo_in_first;
wire          r_cdc_cdc_fifo_in_last;
wire   [31:0] r_cdc_cdc_fifo_in_payload_data;
wire    [1:0] r_cdc_cdc_fifo_in_payload_resp;
wire          r_cdc_cdc_fifo_out_first;
wire          r_cdc_cdc_fifo_out_last;
wire   [31:0] r_cdc_cdc_fifo_out_payload_data;
wire    [1:0] r_cdc_cdc_fifo_out_payload_resp;
wire          r_cdc_cdc_graycounter0_ce;
reg     [2:0] r_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] r_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] r_cdc_cdc_graycounter0_q_next;
reg     [2:0] r_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          r_cdc_cdc_graycounter1_ce;
reg     [2:0] r_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] r_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] r_cdc_cdc_graycounter1_q_next;
reg     [2:0] r_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] r_cdc_cdc_produce_rdomain;
wire    [1:0] r_cdc_cdc_rdport_adr;
wire   [35:0] r_cdc_cdc_rdport_dat_r;
wire          r_cdc_cdc_sink_first;
wire          r_cdc_cdc_sink_last;
wire   [31:0] r_cdc_cdc_sink_payload_data;
wire    [1:0] r_cdc_cdc_sink_payload_resp;
wire          r_cdc_cdc_sink_ready;
wire          r_cdc_cdc_sink_valid;
wire          r_cdc_cdc_source_first;
wire          r_cdc_cdc_source_last;
wire   [31:0] r_cdc_cdc_source_payload_data;
wire    [1:0] r_cdc_cdc_source_payload_resp;
wire          r_cdc_cdc_source_ready;
wire          r_cdc_cdc_source_valid;
wire    [1:0] r_cdc_cdc_wrport_adr;
wire   [35:0] r_cdc_cdc_wrport_dat_r;
wire   [35:0] r_cdc_cdc_wrport_dat_w;
wire          r_cdc_cdc_wrport_we;
wire          r_cdc_sink_sink_first;
wire          r_cdc_sink_sink_last;
wire   [31:0] r_cdc_sink_sink_payload_data;
wire    [1:0] r_cdc_sink_sink_payload_resp;
wire          r_cdc_sink_sink_ready;
wire          r_cdc_sink_sink_valid;
wire          r_cdc_source_source_first;
wire          r_cdc_source_source_last;
wire   [31:0] r_cdc_source_source_payload_data;
wire    [1:0] r_cdc_source_source_payload_resp;
wire          r_cdc_source_source_ready;
wire          r_cdc_source_source_valid;
wire   [37:0] w_cdc_cdc_asyncfifo_din;
wire   [37:0] w_cdc_cdc_asyncfifo_dout;
wire          w_cdc_cdc_asyncfifo_re;
wire          w_cdc_cdc_asyncfifo_readable;
wire          w_cdc_cdc_asyncfifo_we;
wire          w_cdc_cdc_asyncfifo_writable;
wire    [2:0] w_cdc_cdc_consume_wdomain;
wire          w_cdc_cdc_fifo_in_first;
wire          w_cdc_cdc_fifo_in_last;
wire   [31:0] w_cdc_cdc_fifo_in_payload_data;
wire    [3:0] w_cdc_cdc_fifo_in_payload_strb;
wire          w_cdc_cdc_fifo_out_first;
wire          w_cdc_cdc_fifo_out_last;
wire   [31:0] w_cdc_cdc_fifo_out_payload_data;
wire    [3:0] w_cdc_cdc_fifo_out_payload_strb;
wire          w_cdc_cdc_graycounter0_ce;
reg     [2:0] w_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] w_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] w_cdc_cdc_graycounter0_q_next;
reg     [2:0] w_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          w_cdc_cdc_graycounter1_ce;
reg     [2:0] w_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] w_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] w_cdc_cdc_graycounter1_q_next;
reg     [2:0] w_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] w_cdc_cdc_produce_rdomain;
wire    [1:0] w_cdc_cdc_rdport_adr;
wire   [37:0] w_cdc_cdc_rdport_dat_r;
wire          w_cdc_cdc_sink_first;
wire          w_cdc_cdc_sink_last;
wire   [31:0] w_cdc_cdc_sink_payload_data;
wire    [3:0] w_cdc_cdc_sink_payload_strb;
wire          w_cdc_cdc_sink_ready;
wire          w_cdc_cdc_sink_valid;
wire          w_cdc_cdc_source_first;
wire          w_cdc_cdc_source_last;
wire   [31:0] w_cdc_cdc_source_payload_data;
wire    [3:0] w_cdc_cdc_source_payload_strb;
wire          w_cdc_cdc_source_ready;
wire          w_cdc_cdc_source_valid;
wire    [1:0] w_cdc_cdc_wrport_adr;
wire   [37:0] w_cdc_cdc_wrport_dat_r;
wire   [37:0] w_cdc_cdc_wrport_dat_w;
wire          w_cdc_cdc_wrport_we;
wire          w_cdc_sink_sink_first;
wire          w_cdc_sink_sink_last;
wire   [31:0] w_cdc_sink_sink_payload_data;
wire    [3:0] w_cdc_sink_sink_payload_strb;
wire          w_cdc_sink_sink_ready;
wire          w_cdc_sink_sink_valid;
wire          w_cdc_source_source_first;
wire          w_cdc_source_source_last;
wire   [31:0] w_cdc_source_source_payload_data;
wire    [3:0] w_cdc_source_source_payload_strb;
wire          w_cdc_source_source_ready;
wire          w_cdc_source_source_valid;


// Combinatorial Logic


assign aw_cdc_sink_sink_valid = aw_valid;
assign aw_ready = aw_cdc_sink_sink_ready;
assign aw_cdc_sink_sink_first = aw_first;
assign aw_cdc_sink_sink_last = aw_last;
assign aw_cdc_sink_sink_payload_addr = aw_payload_addr;
assign aw_cdc_sink_sink_payload_prot = aw_payload_prot;
assign aw_valid_1 = aw_cdc_source_source_valid;
assign aw_cdc_source_source_ready = aw_ready_1;
assign aw_first_1 = aw_cdc_source_source_first;
assign aw_last_1 = aw_cdc_source_source_last;
assign aw_payload_addr_1 = aw_cdc_source_source_payload_addr;
assign aw_payload_prot_1 = aw_cdc_source_source_payload_prot;
assign w_cdc_sink_sink_valid = w_valid;
assign w_ready = w_cdc_sink_sink_ready;
assign w_cdc_sink_sink_first = w_first;
assign w_cdc_sink_sink_last = w_last;
assign w_cdc_sink_sink_payload_data = w_payload_data;
assign w_cdc_sink_sink_payload_strb = w_payload_strb;
assign w_valid_1 = w_cdc_source_source_valid;
assign w_cdc_source_source_ready = w_ready_1;
assign w_first_1 = w_cdc_source_source_first;
assign w_last_1 = w_cdc_source_source_last;
assign w_payload_data_1 = w_cdc_source_source_payload_data;
assign w_payload_strb_1 = w_cdc_source_source_payload_strb;
assign b_cdc_sink_sink_valid = b_valid_1;
assign b_ready_1 = b_cdc_sink_sink_ready;
assign b_cdc_sink_sink_first = b_first_1;
assign b_cdc_sink_sink_last = b_last_1;
assign b_cdc_sink_sink_payload_resp = b_payload_resp_1;
assign b_valid = b_cdc_source_source_valid;
assign b_cdc_source_source_ready = b_ready;
assign b_first = b_cdc_source_source_first;
assign b_last = b_cdc_source_source_last;
assign b_payload_resp = b_cdc_source_source_payload_resp;
assign ar_cdc_sink_sink_valid = ar_valid;
assign ar_ready = ar_cdc_sink_sink_ready;
assign ar_cdc_sink_sink_first = ar_first;
assign ar_cdc_sink_sink_last = ar_last;
assign ar_cdc_sink_sink_payload_addr = ar_payload_addr;
assign ar_cdc_sink_sink_payload_prot = ar_payload_prot;
assign ar_valid_1 = ar_cdc_source_source_valid;
assign ar_cdc_source_source_ready = ar_ready_1;
assign ar_first_1 = ar_cdc_source_source_first;
assign ar_last_1 = ar_cdc_source_source_last;
assign ar_payload_addr_1 = ar_cdc_source_source_payload_addr;
assign ar_payload_prot_1 = ar_cdc_source_source_payload_prot;
assign r_cdc_sink_sink_valid = r_valid_1;
assign r_ready_1 = r_cdc_sink_sink_ready;
assign r_cdc_sink_sink_first = r_first;
assign r_cdc_sink_sink_last = r_last;
assign r_cdc_sink_sink_payload_resp = r_payload_resp;
assign r_cdc_sink_sink_payload_data = r_payload_data;
assign r_valid = r_cdc_source_source_valid;
assign r_cdc_source_source_ready = r_ready;
assign r_first_1 = r_cdc_source_source_first;
assign r_last_1 = r_cdc_source_source_last;
assign r_payload_resp_1 = r_cdc_source_source_payload_resp;
assign r_payload_data_1 = r_cdc_source_source_payload_data;
assign aw_cdc_cdc_sink_valid = aw_cdc_sink_sink_valid;
assign aw_cdc_sink_sink_ready = aw_cdc_cdc_sink_ready;
assign aw_cdc_cdc_sink_first = aw_cdc_sink_sink_first;
assign aw_cdc_cdc_sink_last = aw_cdc_sink_sink_last;
assign aw_cdc_cdc_sink_payload_addr = aw_cdc_sink_sink_payload_addr;
assign aw_cdc_cdc_sink_payload_prot = aw_cdc_sink_sink_payload_prot;
assign aw_cdc_source_source_valid = aw_cdc_cdc_source_valid;
assign aw_cdc_cdc_source_ready = aw_cdc_source_source_ready;
assign aw_cdc_source_source_first = aw_cdc_cdc_source_first;
assign aw_cdc_source_source_last = aw_cdc_cdc_source_last;
assign aw_cdc_source_source_payload_addr = aw_cdc_cdc_source_payload_addr;
assign aw_cdc_source_source_payload_prot = aw_cdc_cdc_source_payload_prot;
assign aw_cdc_cdc_asyncfifo_din = {aw_cdc_cdc_fifo_in_last, aw_cdc_cdc_fifo_in_first, aw_cdc_cdc_fifo_in_payload_prot, aw_cdc_cdc_fifo_in_payload_addr};
assign {aw_cdc_cdc_fifo_out_last, aw_cdc_cdc_fifo_out_first, aw_cdc_cdc_fifo_out_payload_prot, aw_cdc_cdc_fifo_out_payload_addr} = aw_cdc_cdc_asyncfifo_dout;
assign aw_cdc_cdc_sink_ready = aw_cdc_cdc_asyncfifo_writable;
assign aw_cdc_cdc_asyncfifo_we = aw_cdc_cdc_sink_valid;
assign aw_cdc_cdc_fifo_in_first = aw_cdc_cdc_sink_first;
assign aw_cdc_cdc_fifo_in_last = aw_cdc_cdc_sink_last;
assign aw_cdc_cdc_fifo_in_payload_addr = aw_cdc_cdc_sink_payload_addr;
assign aw_cdc_cdc_fifo_in_payload_prot = aw_cdc_cdc_sink_payload_prot;
assign aw_cdc_cdc_source_valid = aw_cdc_cdc_asyncfifo_readable;
assign aw_cdc_cdc_source_first = aw_cdc_cdc_fifo_out_first;
assign aw_cdc_cdc_source_last = aw_cdc_cdc_fifo_out_last;
assign aw_cdc_cdc_source_payload_addr = aw_cdc_cdc_fifo_out_payload_addr;
assign aw_cdc_cdc_source_payload_prot = aw_cdc_cdc_fifo_out_payload_prot;
assign aw_cdc_cdc_asyncfifo_re = aw_cdc_cdc_source_ready;
assign aw_cdc_cdc_graycounter0_ce = (aw_cdc_cdc_asyncfifo_writable & aw_cdc_cdc_asyncfifo_we);
assign aw_cdc_cdc_graycounter1_ce = (aw_cdc_cdc_asyncfifo_readable & aw_cdc_cdc_asyncfifo_re);
assign aw_cdc_cdc_asyncfifo_writable = (((aw_cdc_cdc_graycounter0_q[2] == aw_cdc_cdc_consume_wdomain[2]) | (aw_cdc_cdc_graycounter0_q[1] == aw_cdc_cdc_consume_wdomain[1])) | (aw_cdc_cdc_graycounter0_q[0] != aw_cdc_cdc_consume_wdomain[0]));
assign aw_cdc_cdc_asyncfifo_readable = (aw_cdc_cdc_graycounter1_q != aw_cdc_cdc_produce_rdomain);
assign aw_cdc_cdc_wrport_adr = aw_cdc_cdc_graycounter0_q_binary[1:0];
assign aw_cdc_cdc_wrport_dat_w = aw_cdc_cdc_asyncfifo_din;
assign aw_cdc_cdc_wrport_we = aw_cdc_cdc_graycounter0_ce;
assign aw_cdc_cdc_rdport_adr = aw_cdc_cdc_graycounter1_q_next_binary[1:0];
assign aw_cdc_cdc_asyncfifo_dout = aw_cdc_cdc_rdport_dat_r;
always @(*) begin
    aw_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (aw_cdc_cdc_graycounter0_ce) begin
        aw_cdc_cdc_graycounter0_q_next_binary = (aw_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        aw_cdc_cdc_graycounter0_q_next_binary = aw_cdc_cdc_graycounter0_q_binary;
    end
end
assign aw_cdc_cdc_graycounter0_q_next = (aw_cdc_cdc_graycounter0_q_next_binary ^ aw_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    aw_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (aw_cdc_cdc_graycounter1_ce) begin
        aw_cdc_cdc_graycounter1_q_next_binary = (aw_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        aw_cdc_cdc_graycounter1_q_next_binary = aw_cdc_cdc_graycounter1_q_binary;
    end
end
assign aw_cdc_cdc_graycounter1_q_next = (aw_cdc_cdc_graycounter1_q_next_binary ^ aw_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign w_cdc_cdc_sink_valid = w_cdc_sink_sink_valid;
assign w_cdc_sink_sink_ready = w_cdc_cdc_sink_ready;
assign w_cdc_cdc_sink_first = w_cdc_sink_sink_first;
assign w_cdc_cdc_sink_last = w_cdc_sink_sink_last;
assign w_cdc_cdc_sink_payload_data = w_cdc_sink_sink_payload_data;
assign w_cdc_cdc_sink_payload_strb = w_cdc_sink_sink_payload_strb;
assign w_cdc_source_source_valid = w_cdc_cdc_source_valid;
assign w_cdc_cdc_source_ready = w_cdc_source_source_ready;
assign w_cdc_source_source_first = w_cdc_cdc_source_first;
assign w_cdc_source_source_last = w_cdc_cdc_source_last;
assign w_cdc_source_source_payload_data = w_cdc_cdc_source_payload_data;
assign w_cdc_source_source_payload_strb = w_cdc_cdc_source_payload_strb;
assign w_cdc_cdc_asyncfifo_din = {w_cdc_cdc_fifo_in_last, w_cdc_cdc_fifo_in_first, w_cdc_cdc_fifo_in_payload_strb, w_cdc_cdc_fifo_in_payload_data};
assign {w_cdc_cdc_fifo_out_last, w_cdc_cdc_fifo_out_first, w_cdc_cdc_fifo_out_payload_strb, w_cdc_cdc_fifo_out_payload_data} = w_cdc_cdc_asyncfifo_dout;
assign w_cdc_cdc_sink_ready = w_cdc_cdc_asyncfifo_writable;
assign w_cdc_cdc_asyncfifo_we = w_cdc_cdc_sink_valid;
assign w_cdc_cdc_fifo_in_first = w_cdc_cdc_sink_first;
assign w_cdc_cdc_fifo_in_last = w_cdc_cdc_sink_last;
assign w_cdc_cdc_fifo_in_payload_data = w_cdc_cdc_sink_payload_data;
assign w_cdc_cdc_fifo_in_payload_strb = w_cdc_cdc_sink_payload_strb;
assign w_cdc_cdc_source_valid = w_cdc_cdc_asyncfifo_readable;
assign w_cdc_cdc_source_first = w_cdc_cdc_fifo_out_first;
assign w_cdc_cdc_source_last = w_cdc_cdc_fifo_out_last;
assign w_cdc_cdc_source_payload_data = w_cdc_cdc_fifo_out_payload_data;
assign w_cdc_cdc_source_payload_strb = w_cdc_cdc_fifo_out_payload_strb;
assign w_cdc_cdc_asyncfifo_re = w_cdc_cdc_source_ready;
assign w_cdc_cdc_graycounter0_ce = (w_cdc_cdc_asyncfifo_writable & w_cdc_cdc_asyncfifo_we);
assign w_cdc_cdc_graycounter1_ce = (w_cdc_cdc_asyncfifo_readable & w_cdc_cdc_asyncfifo_re);
assign w_cdc_cdc_asyncfifo_writable = (((w_cdc_cdc_graycounter0_q[2] == w_cdc_cdc_consume_wdomain[2]) | (w_cdc_cdc_graycounter0_q[1] == w_cdc_cdc_consume_wdomain[1])) | (w_cdc_cdc_graycounter0_q[0] != w_cdc_cdc_consume_wdomain[0]));
assign w_cdc_cdc_asyncfifo_readable = (w_cdc_cdc_graycounter1_q != w_cdc_cdc_produce_rdomain);
assign w_cdc_cdc_wrport_adr = w_cdc_cdc_graycounter0_q_binary[1:0];
assign w_cdc_cdc_wrport_dat_w = w_cdc_cdc_asyncfifo_din;
assign w_cdc_cdc_wrport_we = w_cdc_cdc_graycounter0_ce;
assign w_cdc_cdc_rdport_adr = w_cdc_cdc_graycounter1_q_next_binary[1:0];
assign w_cdc_cdc_asyncfifo_dout = w_cdc_cdc_rdport_dat_r;
always @(*) begin
    w_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (w_cdc_cdc_graycounter0_ce) begin
        w_cdc_cdc_graycounter0_q_next_binary = (w_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        w_cdc_cdc_graycounter0_q_next_binary = w_cdc_cdc_graycounter0_q_binary;
    end
end
assign w_cdc_cdc_graycounter0_q_next = (w_cdc_cdc_graycounter0_q_next_binary ^ w_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    w_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (w_cdc_cdc_graycounter1_ce) begin
        w_cdc_cdc_graycounter1_q_next_binary = (w_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        w_cdc_cdc_graycounter1_q_next_binary = w_cdc_cdc_graycounter1_q_binary;
    end
end
assign w_cdc_cdc_graycounter1_q_next = (w_cdc_cdc_graycounter1_q_next_binary ^ w_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign b_cdc_cdc_sink_valid = b_cdc_sink_sink_valid;
assign b_cdc_sink_sink_ready = b_cdc_cdc_sink_ready;
assign b_cdc_cdc_sink_first = b_cdc_sink_sink_first;
assign b_cdc_cdc_sink_last = b_cdc_sink_sink_last;
assign b_cdc_cdc_sink_payload_resp = b_cdc_sink_sink_payload_resp;
assign b_cdc_source_source_valid = b_cdc_cdc_source_valid;
assign b_cdc_cdc_source_ready = b_cdc_source_source_ready;
assign b_cdc_source_source_first = b_cdc_cdc_source_first;
assign b_cdc_source_source_last = b_cdc_cdc_source_last;
assign b_cdc_source_source_payload_resp = b_cdc_cdc_source_payload_resp;
assign b_cdc_cdc_asyncfifo_din = {b_cdc_cdc_fifo_in_last, b_cdc_cdc_fifo_in_first, b_cdc_cdc_fifo_in_payload_resp};
assign {b_cdc_cdc_fifo_out_last, b_cdc_cdc_fifo_out_first, b_cdc_cdc_fifo_out_payload_resp} = b_cdc_cdc_asyncfifo_dout;
assign b_cdc_cdc_sink_ready = b_cdc_cdc_asyncfifo_writable;
assign b_cdc_cdc_asyncfifo_we = b_cdc_cdc_sink_valid;
assign b_cdc_cdc_fifo_in_first = b_cdc_cdc_sink_first;
assign b_cdc_cdc_fifo_in_last = b_cdc_cdc_sink_last;
assign b_cdc_cdc_fifo_in_payload_resp = b_cdc_cdc_sink_payload_resp;
assign b_cdc_cdc_source_valid = b_cdc_cdc_asyncfifo_readable;
assign b_cdc_cdc_source_first = b_cdc_cdc_fifo_out_first;
assign b_cdc_cdc_source_last = b_cdc_cdc_fifo_out_last;
assign b_cdc_cdc_source_payload_resp = b_cdc_cdc_fifo_out_payload_resp;
assign b_cdc_cdc_asyncfifo_re = b_cdc_cdc_source_ready;
assign b_cdc_cdc_graycounter0_ce = (b_cdc_cdc_asyncfifo_writable & b_cdc_cdc_asyncfifo_we);
assign b_cdc_cdc_graycounter1_ce = (b_cdc_cdc_asyncfifo_readable & b_cdc_cdc_asyncfifo_re);
assign b_cdc_cdc_asyncfifo_writable = (((b_cdc_cdc_graycounter0_q[2] == b_cdc_cdc_consume_wdomain[2]) | (b_cdc_cdc_graycounter0_q[1] == b_cdc_cdc_consume_wdomain[1])) | (b_cdc_cdc_graycounter0_q[0] != b_cdc_cdc_consume_wdomain[0]));
assign b_cdc_cdc_asyncfifo_readable = (b_cdc_cdc_graycounter1_q != b_cdc_cdc_produce_rdomain);
assign b_cdc_cdc_wrport_adr = b_cdc_cdc_graycounter0_q_binary[1:0];
assign b_cdc_cdc_wrport_dat_w = b_cdc_cdc_asyncfifo_din;
assign b_cdc_cdc_wrport_we = b_cdc_cdc_graycounter0_ce;
assign b_cdc_cdc_rdport_adr = b_cdc_cdc_graycounter1_q_next_binary[1:0];
assign b_cdc_cdc_asyncfifo_dout = b_cdc_cdc_rdport_dat_r;
always @(*) begin
    b_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (b_cdc_cdc_graycounter0_ce) begin
        b_cdc_cdc_graycounter0_q_next_binary = (b_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        b_cdc_cdc_graycounter0_q_next_binary = b_cdc_cdc_graycounter0_q_binary;
    end
end
assign b_cdc_cdc_graycounter0_q_next = (b_cdc_cdc_graycounter0_q_next_binary ^ b_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    b_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (b_cdc_cdc_graycounter1_ce) begin
        b_cdc_cdc_graycounter1_q_next_binary = (b_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        b_cdc_cdc_graycounter1_q_next_binary = b_cdc_cdc_graycounter1_q_binary;
    end
end
assign b_cdc_cdc_graycounter1_q_next = (b_cdc_cdc_graycounter1_q_next_binary ^ b_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign ar_cdc_cdc_sink_valid = ar_cdc_sink_sink_valid;
assign ar_cdc_sink_sink_ready = ar_cdc_cdc_sink_ready;
assign ar_cdc_cdc_sink_first = ar_cdc_sink_sink_first;
assign ar_cdc_cdc_sink_last = ar_cdc_sink_sink_last;
assign ar_cdc_cdc_sink_payload_addr = ar_cdc_sink_sink_payload_addr;
assign ar_cdc_cdc_sink_payload_prot = ar_cdc_sink_sink_payload_prot;
assign ar_cdc_source_source_valid = ar_cdc_cdc_source_valid;
assign ar_cdc_cdc_source_ready = ar_cdc_source_source_ready;
assign ar_cdc_source_source_first = ar_cdc_cdc_source_first;
assign ar_cdc_source_source_last = ar_cdc_cdc_source_last;
assign ar_cdc_source_source_payload_addr = ar_cdc_cdc_source_payload_addr;
assign ar_cdc_source_source_payload_prot = ar_cdc_cdc_source_payload_prot;
assign ar_cdc_cdc_asyncfifo_din = {ar_cdc_cdc_fifo_in_last, ar_cdc_cdc_fifo_in_first, ar_cdc_cdc_fifo_in_payload_prot, ar_cdc_cdc_fifo_in_payload_addr};
assign {ar_cdc_cdc_fifo_out_last, ar_cdc_cdc_fifo_out_first, ar_cdc_cdc_fifo_out_payload_prot, ar_cdc_cdc_fifo_out_payload_addr} = ar_cdc_cdc_asyncfifo_dout;
assign ar_cdc_cdc_sink_ready = ar_cdc_cdc_asyncfifo_writable;
assign ar_cdc_cdc_asyncfifo_we = ar_cdc_cdc_sink_valid;
assign ar_cdc_cdc_fifo_in_first = ar_cdc_cdc_sink_first;
assign ar_cdc_cdc_fifo_in_last = ar_cdc_cdc_sink_last;
assign ar_cdc_cdc_fifo_in_payload_addr = ar_cdc_cdc_sink_payload_addr;
assign ar_cdc_cdc_fifo_in_payload_prot = ar_cdc_cdc_sink_payload_prot;
assign ar_cdc_cdc_source_valid = ar_cdc_cdc_asyncfifo_readable;
assign ar_cdc_cdc_source_first = ar_cdc_cdc_fifo_out_first;
assign ar_cdc_cdc_source_last = ar_cdc_cdc_fifo_out_last;
assign ar_cdc_cdc_source_payload_addr = ar_cdc_cdc_fifo_out_payload_addr;
assign ar_cdc_cdc_source_payload_prot = ar_cdc_cdc_fifo_out_payload_prot;
assign ar_cdc_cdc_asyncfifo_re = ar_cdc_cdc_source_ready;
assign ar_cdc_cdc_graycounter0_ce = (ar_cdc_cdc_asyncfifo_writable & ar_cdc_cdc_asyncfifo_we);
assign ar_cdc_cdc_graycounter1_ce = (ar_cdc_cdc_asyncfifo_readable & ar_cdc_cdc_asyncfifo_re);
assign ar_cdc_cdc_asyncfifo_writable = (((ar_cdc_cdc_graycounter0_q[2] == ar_cdc_cdc_consume_wdomain[2]) | (ar_cdc_cdc_graycounter0_q[1] == ar_cdc_cdc_consume_wdomain[1])) | (ar_cdc_cdc_graycounter0_q[0] != ar_cdc_cdc_consume_wdomain[0]));
assign ar_cdc_cdc_asyncfifo_readable = (ar_cdc_cdc_graycounter1_q != ar_cdc_cdc_produce_rdomain);
assign ar_cdc_cdc_wrport_adr = ar_cdc_cdc_graycounter0_q_binary[1:0];
assign ar_cdc_cdc_wrport_dat_w = ar_cdc_cdc_asyncfifo_din;
assign ar_cdc_cdc_wrport_we = ar_cdc_cdc_graycounter0_ce;
assign ar_cdc_cdc_rdport_adr = ar_cdc_cdc_graycounter1_q_next_binary[1:0];
assign ar_cdc_cdc_asyncfifo_dout = ar_cdc_cdc_rdport_dat_r;
always @(*) begin
    ar_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (ar_cdc_cdc_graycounter0_ce) begin
        ar_cdc_cdc_graycounter0_q_next_binary = (ar_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        ar_cdc_cdc_graycounter0_q_next_binary = ar_cdc_cdc_graycounter0_q_binary;
    end
end
assign ar_cdc_cdc_graycounter0_q_next = (ar_cdc_cdc_graycounter0_q_next_binary ^ ar_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    ar_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (ar_cdc_cdc_graycounter1_ce) begin
        ar_cdc_cdc_graycounter1_q_next_binary = (ar_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        ar_cdc_cdc_graycounter1_q_next_binary = ar_cdc_cdc_graycounter1_q_binary;
    end
end
assign ar_cdc_cdc_graycounter1_q_next = (ar_cdc_cdc_graycounter1_q_next_binary ^ ar_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign r_cdc_cdc_sink_valid = r_cdc_sink_sink_valid;
assign r_cdc_sink_sink_ready = r_cdc_cdc_sink_ready;
assign r_cdc_cdc_sink_first = r_cdc_sink_sink_first;
assign r_cdc_cdc_sink_last = r_cdc_sink_sink_last;
assign r_cdc_cdc_sink_payload_resp = r_cdc_sink_sink_payload_resp;
assign r_cdc_cdc_sink_payload_data = r_cdc_sink_sink_payload_data;
assign r_cdc_source_source_valid = r_cdc_cdc_source_valid;
assign r_cdc_cdc_source_ready = r_cdc_source_source_ready;
assign r_cdc_source_source_first = r_cdc_cdc_source_first;
assign r_cdc_source_source_last = r_cdc_cdc_source_last;
assign r_cdc_source_source_payload_resp = r_cdc_cdc_source_payload_resp;
assign r_cdc_source_source_payload_data = r_cdc_cdc_source_payload_data;
assign r_cdc_cdc_asyncfifo_din = {r_cdc_cdc_fifo_in_last, r_cdc_cdc_fifo_in_first, r_cdc_cdc_fifo_in_payload_data, r_cdc_cdc_fifo_in_payload_resp};
assign {r_cdc_cdc_fifo_out_last, r_cdc_cdc_fifo_out_first, r_cdc_cdc_fifo_out_payload_data, r_cdc_cdc_fifo_out_payload_resp} = r_cdc_cdc_asyncfifo_dout;
assign r_cdc_cdc_sink_ready = r_cdc_cdc_asyncfifo_writable;
assign r_cdc_cdc_asyncfifo_we = r_cdc_cdc_sink_valid;
assign r_cdc_cdc_fifo_in_first = r_cdc_cdc_sink_first;
assign r_cdc_cdc_fifo_in_last = r_cdc_cdc_sink_last;
assign r_cdc_cdc_fifo_in_payload_resp = r_cdc_cdc_sink_payload_resp;
assign r_cdc_cdc_fifo_in_payload_data = r_cdc_cdc_sink_payload_data;
assign r_cdc_cdc_source_valid = r_cdc_cdc_asyncfifo_readable;
assign r_cdc_cdc_source_first = r_cdc_cdc_fifo_out_first;
assign r_cdc_cdc_source_last = r_cdc_cdc_fifo_out_last;
assign r_cdc_cdc_source_payload_resp = r_cdc_cdc_fifo_out_payload_resp;
assign r_cdc_cdc_source_payload_data = r_cdc_cdc_fifo_out_payload_data;
assign r_cdc_cdc_asyncfifo_re = r_cdc_cdc_source_ready;
assign r_cdc_cdc_graycounter0_ce = (r_cdc_cdc_asyncfifo_writable & r_cdc_cdc_asyncfifo_we);
assign r_cdc_cdc_graycounter1_ce = (r_cdc_cdc_asyncfifo_readable & r_cdc_cdc_asyncfifo_re);
assign r_cdc_cdc_asyncfifo_writable = (((r_cdc_cdc_graycounter0_q[2] == r_cdc_cdc_consume_wdomain[2]) | (r_cdc_cdc_graycounter0_q[1] == r_cdc_cdc_consume_wdomain[1])) | (r_cdc_cdc_graycounter0_q[0] != r_cdc_cdc_consume_wdomain[0]));
assign r_cdc_cdc_asyncfifo_readable = (r_cdc_cdc_graycounter1_q != r_cdc_cdc_produce_rdomain);
assign r_cdc_cdc_wrport_adr = r_cdc_cdc_graycounter0_q_binary[1:0];
assign r_cdc_cdc_wrport_dat_w = r_cdc_cdc_asyncfifo_din;
assign r_cdc_cdc_wrport_we = r_cdc_cdc_graycounter0_ce;
assign r_cdc_cdc_rdport_adr = r_cdc_cdc_graycounter1_q_next_binary[1:0];
assign r_cdc_cdc_asyncfifo_dout = r_cdc_cdc_rdport_dat_r;
always @(*) begin
    r_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (r_cdc_cdc_graycounter0_ce) begin
        r_cdc_cdc_graycounter0_q_next_binary = (r_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        r_cdc_cdc_graycounter0_q_next_binary = r_cdc_cdc_graycounter0_q_binary;
    end
end
assign r_cdc_cdc_graycounter0_q_next = (r_cdc_cdc_graycounter0_q_next_binary ^ r_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    r_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (r_cdc_cdc_graycounter1_ce) begin
        r_cdc_cdc_graycounter1_q_next_binary = (r_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        r_cdc_cdc_graycounter1_q_next_binary = r_cdc_cdc_graycounter1_q_binary;
    end
end
assign r_cdc_cdc_graycounter1_q_next = (r_cdc_cdc_graycounter1_q_next_binary ^ r_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign aw_cdc_cdc_produce_rdomain = multiregimpl01;
assign aw_cdc_cdc_consume_wdomain = multiregimpl11;
assign w_cdc_cdc_produce_rdomain = multiregimpl21;
assign w_cdc_cdc_consume_wdomain = multiregimpl31;
assign b_cdc_cdc_produce_rdomain = multiregimpl41;
assign b_cdc_cdc_consume_wdomain = multiregimpl51;
assign ar_cdc_cdc_produce_rdomain = multiregimpl61;
assign ar_cdc_cdc_consume_wdomain = multiregimpl71;
assign r_cdc_cdc_produce_rdomain = multiregimpl81;
assign r_cdc_cdc_consume_wdomain = multiregimpl91;



// Synchronous Logic


always @(posedge milan_clk) begin
    aw_cdc_cdc_graycounter1_q_binary <= aw_cdc_cdc_graycounter1_q_next_binary;
    aw_cdc_cdc_graycounter1_q <= aw_cdc_cdc_graycounter1_q_next;
    w_cdc_cdc_graycounter1_q_binary <= w_cdc_cdc_graycounter1_q_next_binary;
    w_cdc_cdc_graycounter1_q <= w_cdc_cdc_graycounter1_q_next;
    b_cdc_cdc_graycounter0_q_binary <= b_cdc_cdc_graycounter0_q_next_binary;
    b_cdc_cdc_graycounter0_q <= b_cdc_cdc_graycounter0_q_next;
    ar_cdc_cdc_graycounter1_q_binary <= ar_cdc_cdc_graycounter1_q_next_binary;
    ar_cdc_cdc_graycounter1_q <= ar_cdc_cdc_graycounter1_q_next;
    r_cdc_cdc_graycounter0_q_binary <= r_cdc_cdc_graycounter0_q_next_binary;
    r_cdc_cdc_graycounter0_q <= r_cdc_cdc_graycounter0_q_next;
    if (milan_rst) begin
        aw_cdc_cdc_graycounter1_q <= 3'd0;
        aw_cdc_cdc_graycounter1_q_binary <= 3'd0;
        w_cdc_cdc_graycounter1_q <= 3'd0;
        w_cdc_cdc_graycounter1_q_binary <= 3'd0;
        b_cdc_cdc_graycounter0_q <= 3'd0;
        b_cdc_cdc_graycounter0_q_binary <= 3'd0;
        ar_cdc_cdc_graycounter1_q <= 3'd0;
        ar_cdc_cdc_graycounter1_q_binary <= 3'd0;
        r_cdc_cdc_graycounter0_q <= 3'd0;
        r_cdc_cdc_graycounter0_q_binary <= 3'd0;
    end
    multiregimpl00 <= aw_cdc_cdc_graycounter0_q;
    multiregimpl01 <= multiregimpl00;
    multiregimpl20 <= w_cdc_cdc_graycounter0_q;
    multiregimpl21 <= multiregimpl20;
    multiregimpl50 <= b_cdc_cdc_graycounter1_q;
    multiregimpl51 <= multiregimpl50;
    multiregimpl60 <= ar_cdc_cdc_graycounter0_q;
    multiregimpl61 <= multiregimpl60;
    multiregimpl90 <= r_cdc_cdc_graycounter1_q;
    multiregimpl91 <= multiregimpl90;
end

always @(posedge sys_clk) begin
    aw_cdc_cdc_graycounter0_q_binary <= aw_cdc_cdc_graycounter0_q_next_binary;
    aw_cdc_cdc_graycounter0_q <= aw_cdc_cdc_graycounter0_q_next;
    w_cdc_cdc_graycounter0_q_binary <= w_cdc_cdc_graycounter0_q_next_binary;
    w_cdc_cdc_graycounter0_q <= w_cdc_cdc_graycounter0_q_next;
    b_cdc_cdc_graycounter1_q_binary <= b_cdc_cdc_graycounter1_q_next_binary;
    b_cdc_cdc_graycounter1_q <= b_cdc_cdc_graycounter1_q_next;
    ar_cdc_cdc_graycounter0_q_binary <= ar_cdc_cdc_graycounter0_q_next_binary;
    ar_cdc_cdc_graycounter0_q <= ar_cdc_cdc_graycounter0_q_next;
    r_cdc_cdc_graycounter1_q_binary <= r_cdc_cdc_graycounter1_q_next_binary;
    r_cdc_cdc_graycounter1_q <= r_cdc_cdc_graycounter1_q_next;
    if (sys_rst) begin
        aw_cdc_cdc_graycounter0_q <= 3'd0;
        aw_cdc_cdc_graycounter0_q_binary <= 3'd0;
        w_cdc_cdc_graycounter0_q <= 3'd0;
        w_cdc_cdc_graycounter0_q_binary <= 3'd0;
        b_cdc_cdc_graycounter1_q <= 3'd0;
        b_cdc_cdc_graycounter1_q_binary <= 3'd0;
        ar_cdc_cdc_graycounter0_q <= 3'd0;
        ar_cdc_cdc_graycounter0_q_binary <= 3'd0;
        r_cdc_cdc_graycounter1_q <= 3'd0;
        r_cdc_cdc_graycounter1_q_binary <= 3'd0;
    end
    multiregimpl10 <= aw_cdc_cdc_graycounter1_q;
    multiregimpl11 <= multiregimpl10;
    multiregimpl30 <= w_cdc_cdc_graycounter1_q;
    multiregimpl31 <= multiregimpl30;
    multiregimpl40 <= b_cdc_cdc_graycounter0_q;
    multiregimpl41 <= multiregimpl40;
    multiregimpl70 <= ar_cdc_cdc_graycounter1_q;
    multiregimpl71 <= multiregimpl70;
    multiregimpl80 <= r_cdc_cdc_graycounter0_q;
    multiregimpl81 <= multiregimpl80;
end



// Specialized Logic



// Memory storage: 4-words x 37-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [36:0] storage[0:3];
reg [36:0] storage_dat0;
reg [36:0] storage_dat1;
always @(posedge sys_clk) begin
	if (aw_cdc_cdc_wrport_we)
		storage[aw_cdc_cdc_wrport_adr] <= aw_cdc_cdc_wrport_dat_w;
	storage_dat0 <= storage[aw_cdc_cdc_wrport_adr];
end
always @(posedge milan_clk) begin
	storage_dat1 <= storage[aw_cdc_cdc_rdport_adr];
end
assign aw_cdc_cdc_wrport_dat_r = storage_dat0;
assign aw_cdc_cdc_rdport_dat_r = storage_dat1;



// Memory storage_1: 4-words x 38-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [37:0] storage_1[0:3];
reg [37:0] storage_1_dat0;
reg [37:0] storage_1_dat1;
always @(posedge sys_clk) begin
	if (w_cdc_cdc_wrport_we)
		storage_1[w_cdc_cdc_wrport_adr] <= w_cdc_cdc_wrport_dat_w;
	storage_1_dat0 <= storage_1[w_cdc_cdc_wrport_adr];
end
always @(posedge milan_clk) begin
	storage_1_dat1 <= storage_1[w_cdc_cdc_rdport_adr];
end
assign w_cdc_cdc_wrport_dat_r = storage_1_dat0;
assign w_cdc_cdc_rdport_dat_r = storage_1_dat1;



// Memory storage_2: 4-words x 4-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [3:0] storage_2[0:3];
reg [3:0] storage_2_dat0;
reg [3:0] storage_2_dat1;
always @(posedge milan_clk) begin
	if (b_cdc_cdc_wrport_we)
		storage_2[b_cdc_cdc_wrport_adr] <= b_cdc_cdc_wrport_dat_w;
	storage_2_dat0 <= storage_2[b_cdc_cdc_wrport_adr];
end
always @(posedge sys_clk) begin
	storage_2_dat1 <= storage_2[b_cdc_cdc_rdport_adr];
end
assign b_cdc_cdc_wrport_dat_r = storage_2_dat0;
assign b_cdc_cdc_rdport_dat_r = storage_2_dat1;



// Memory storage_3: 4-words x 37-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [36:0] storage_3[0:3];
reg [36:0] storage_3_dat0;
reg [36:0] storage_3_dat1;
always @(posedge sys_clk) begin
	if (ar_cdc_cdc_wrport_we)
		storage_3[ar_cdc_cdc_wrport_adr] <= ar_cdc_cdc_wrport_dat_w;
	storage_3_dat0 <= storage_3[ar_cdc_cdc_wrport_adr];
end
always @(posedge milan_clk) begin
	storage_3_dat1 <= storage_3[ar_cdc_cdc_rdport_adr];
end
assign ar_cdc_cdc_wrport_dat_r = storage_3_dat0;
assign ar_cdc_cdc_rdport_dat_r = storage_3_dat1;



// Memory storage_4: 4-words x 36-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [35:0] storage_4[0:3];
reg [35:0] storage_4_dat0;
reg [35:0] storage_4_dat1;
always @(posedge milan_clk) begin
	if (r_cdc_cdc_wrport_we)
		storage_4[r_cdc_cdc_wrport_adr] <= r_cdc_cdc_wrport_dat_w;
	storage_4_dat0 <= storage_4[r_cdc_cdc_wrport_adr];
end
always @(posedge sys_clk) begin
	storage_4_dat1 <= storage_4[r_cdc_cdc_rdport_adr];
end
assign r_cdc_cdc_wrport_dat_r = storage_4_dat0;
assign r_cdc_cdc_rdport_dat_r = storage_4_dat1;


endmodule






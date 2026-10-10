

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
    output wire          aw_first,
    input  wire          aw_first_1,
    output wire          aw_last,
    input  wire          aw_last_1,
    output wire   [31:0] aw_payload_addr,
    input  wire   [31:0] aw_payload_addr_1,
    output wire    [2:0] aw_payload_prot,
    input  wire    [2:0] aw_payload_prot_1,
    input  wire          aw_ready,
    output wire          aw_ready_1,
    output wire          aw_valid,
    input  wire          aw_valid_1,
    output wire          b_first,
    input  wire          b_first_1,
    output wire          b_last,
    input  wire          b_last_1,
    output wire    [1:0] b_payload_resp,
    input  wire    [1:0] b_payload_resp_1,
    output wire          b_ready,
    input  wire          b_ready_1,
    input  wire          b_valid,
    output wire          b_valid_1,
    input  wire          macdp_clk,
    input  wire          macdp_rst,
    input  wire          macsys_clk,
    input  wire          macsys_rst,
    input  wire          milan_clk,
    input  wire          milan_rst,
    output wire          r_first,
    input  wire          r_first_1,
    output wire          r_last,
    input  wire          r_last_1,
    output wire   [31:0] r_payload_data,
    input  wire   [31:0] r_payload_data_1,
    output wire    [1:0] r_payload_resp,
    input  wire    [1:0] r_payload_resp_1,
    input  wire          r_ready,
    output wire          r_ready_1,
    output wire          r_valid,
    input  wire          r_valid_1,
    input  wire          sys_clk,
    input  wire          sys_rst,
    output wire          w_first,
    input  wire          w_first_1,
    output wire          w_last,
    input  wire          w_last_1,
    output wire   [31:0] w_payload_data,
    input  wire   [31:0] w_payload_data_1,
    output wire    [3:0] w_payload_strb,
    input  wire    [3:0] w_payload_strb_1,
    input  wire          w_ready,
    output wire          w_ready_1,
    output wire          w_valid,
    input  wire          w_valid_1
);



// Hierarchy




// Signals


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
wire   [36:0] slave_ar_cdc_cdc_asyncfifo_din;
wire   [36:0] slave_ar_cdc_cdc_asyncfifo_dout;
wire          slave_ar_cdc_cdc_asyncfifo_re;
wire          slave_ar_cdc_cdc_asyncfifo_readable;
wire          slave_ar_cdc_cdc_asyncfifo_we;
wire          slave_ar_cdc_cdc_asyncfifo_writable;
wire    [2:0] slave_ar_cdc_cdc_consume_wdomain;
wire          slave_ar_cdc_cdc_fifo_in_first;
wire          slave_ar_cdc_cdc_fifo_in_last;
wire   [31:0] slave_ar_cdc_cdc_fifo_in_payload_addr;
wire    [2:0] slave_ar_cdc_cdc_fifo_in_payload_prot;
wire          slave_ar_cdc_cdc_fifo_out_first;
wire          slave_ar_cdc_cdc_fifo_out_last;
wire   [31:0] slave_ar_cdc_cdc_fifo_out_payload_addr;
wire    [2:0] slave_ar_cdc_cdc_fifo_out_payload_prot;
wire          slave_ar_cdc_cdc_graycounter0_ce;
reg     [2:0] slave_ar_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] slave_ar_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] slave_ar_cdc_cdc_graycounter0_q_next;
reg     [2:0] slave_ar_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          slave_ar_cdc_cdc_graycounter1_ce;
reg     [2:0] slave_ar_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] slave_ar_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] slave_ar_cdc_cdc_graycounter1_q_next;
reg     [2:0] slave_ar_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] slave_ar_cdc_cdc_produce_rdomain;
wire    [1:0] slave_ar_cdc_cdc_rdport_adr;
wire   [36:0] slave_ar_cdc_cdc_rdport_dat_r;
wire          slave_ar_cdc_cdc_sink_first;
wire          slave_ar_cdc_cdc_sink_last;
wire   [31:0] slave_ar_cdc_cdc_sink_payload_addr;
wire    [2:0] slave_ar_cdc_cdc_sink_payload_prot;
wire          slave_ar_cdc_cdc_sink_ready;
wire          slave_ar_cdc_cdc_sink_valid;
wire          slave_ar_cdc_cdc_source_first;
wire          slave_ar_cdc_cdc_source_last;
wire   [31:0] slave_ar_cdc_cdc_source_payload_addr;
wire    [2:0] slave_ar_cdc_cdc_source_payload_prot;
wire          slave_ar_cdc_cdc_source_ready;
wire          slave_ar_cdc_cdc_source_valid;
wire    [1:0] slave_ar_cdc_cdc_wrport_adr;
wire   [36:0] slave_ar_cdc_cdc_wrport_dat_r;
wire   [36:0] slave_ar_cdc_cdc_wrport_dat_w;
wire          slave_ar_cdc_cdc_wrport_we;
wire          slave_ar_cdc_sink_sink_first;
wire          slave_ar_cdc_sink_sink_last;
wire   [31:0] slave_ar_cdc_sink_sink_payload_addr;
wire    [2:0] slave_ar_cdc_sink_sink_payload_prot;
wire          slave_ar_cdc_sink_sink_ready;
wire          slave_ar_cdc_sink_sink_valid;
wire          slave_ar_cdc_source_source_first;
wire          slave_ar_cdc_source_source_last;
wire   [31:0] slave_ar_cdc_source_source_payload_addr;
wire    [2:0] slave_ar_cdc_source_source_payload_prot;
wire          slave_ar_cdc_source_source_ready;
wire          slave_ar_cdc_source_source_valid;
wire    [1:0] slave_array_read_memory0_adr;
wire   [35:0] slave_array_read_memory0_dat_r;
wire    [1:0] slave_array_read_memory1_adr;
wire    [1:0] slave_array_read_memory1_dat_r;
wire    [1:0] slave_array_read_memory2_adr;
wire   [33:0] slave_array_read_memory2_dat_r;
wire    [1:0] slave_array_read_memory3_adr;
wire    [1:0] slave_array_read_memory3_dat_r;
wire    [1:0] slave_array_write_memory0_adr;
wire   [35:0] slave_array_write_memory0_dat_r;
wire   [35:0] slave_array_write_memory0_dat_w;
wire          slave_array_write_memory0_we;
wire    [1:0] slave_array_write_memory1_adr;
wire    [1:0] slave_array_write_memory1_dat_r;
wire    [1:0] slave_array_write_memory1_dat_w;
wire          slave_array_write_memory1_we;
wire    [1:0] slave_array_write_memory2_adr;
wire   [33:0] slave_array_write_memory2_dat_r;
wire   [33:0] slave_array_write_memory2_dat_w;
wire          slave_array_write_memory2_we;
wire    [1:0] slave_array_write_memory3_adr;
wire    [1:0] slave_array_write_memory3_dat_r;
wire    [1:0] slave_array_write_memory3_dat_w;
wire          slave_array_write_memory3_we;
wire   [36:0] slave_aw_cdc_cdc_asyncfifo_din;
wire   [36:0] slave_aw_cdc_cdc_asyncfifo_dout;
wire          slave_aw_cdc_cdc_asyncfifo_re;
wire          slave_aw_cdc_cdc_asyncfifo_readable;
wire          slave_aw_cdc_cdc_asyncfifo_we;
wire          slave_aw_cdc_cdc_asyncfifo_writable;
wire    [2:0] slave_aw_cdc_cdc_consume_wdomain;
wire          slave_aw_cdc_cdc_fifo_in_first;
wire          slave_aw_cdc_cdc_fifo_in_last;
wire   [31:0] slave_aw_cdc_cdc_fifo_in_payload_addr;
wire    [2:0] slave_aw_cdc_cdc_fifo_in_payload_prot;
wire          slave_aw_cdc_cdc_fifo_out_first;
wire          slave_aw_cdc_cdc_fifo_out_last;
wire   [31:0] slave_aw_cdc_cdc_fifo_out_payload_addr;
wire    [2:0] slave_aw_cdc_cdc_fifo_out_payload_prot;
wire          slave_aw_cdc_cdc_graycounter0_ce;
reg     [2:0] slave_aw_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] slave_aw_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] slave_aw_cdc_cdc_graycounter0_q_next;
reg     [2:0] slave_aw_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          slave_aw_cdc_cdc_graycounter1_ce;
reg     [2:0] slave_aw_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] slave_aw_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] slave_aw_cdc_cdc_graycounter1_q_next;
reg     [2:0] slave_aw_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] slave_aw_cdc_cdc_produce_rdomain;
wire    [1:0] slave_aw_cdc_cdc_rdport_adr;
wire   [36:0] slave_aw_cdc_cdc_rdport_dat_r;
wire          slave_aw_cdc_cdc_sink_first;
wire          slave_aw_cdc_cdc_sink_last;
wire   [31:0] slave_aw_cdc_cdc_sink_payload_addr;
wire    [2:0] slave_aw_cdc_cdc_sink_payload_prot;
wire          slave_aw_cdc_cdc_sink_ready;
wire          slave_aw_cdc_cdc_sink_valid;
wire          slave_aw_cdc_cdc_source_first;
wire          slave_aw_cdc_cdc_source_last;
wire   [31:0] slave_aw_cdc_cdc_source_payload_addr;
wire    [2:0] slave_aw_cdc_cdc_source_payload_prot;
wire          slave_aw_cdc_cdc_source_ready;
wire          slave_aw_cdc_cdc_source_valid;
wire    [1:0] slave_aw_cdc_cdc_wrport_adr;
wire   [36:0] slave_aw_cdc_cdc_wrport_dat_r;
wire   [36:0] slave_aw_cdc_cdc_wrport_dat_w;
wire          slave_aw_cdc_cdc_wrport_we;
wire          slave_aw_cdc_sink_sink_first;
wire          slave_aw_cdc_sink_sink_last;
wire   [31:0] slave_aw_cdc_sink_sink_payload_addr;
wire    [2:0] slave_aw_cdc_sink_sink_payload_prot;
wire          slave_aw_cdc_sink_sink_ready;
wire          slave_aw_cdc_sink_sink_valid;
wire          slave_aw_cdc_source_source_first;
wire          slave_aw_cdc_source_source_last;
wire   [31:0] slave_aw_cdc_source_source_payload_addr;
wire    [2:0] slave_aw_cdc_source_source_payload_prot;
wire          slave_aw_cdc_source_source_ready;
wire          slave_aw_cdc_source_source_valid;
wire    [3:0] slave_b_cdc_cdc_asyncfifo_din;
wire    [3:0] slave_b_cdc_cdc_asyncfifo_dout;
wire          slave_b_cdc_cdc_asyncfifo_re;
wire          slave_b_cdc_cdc_asyncfifo_readable;
wire          slave_b_cdc_cdc_asyncfifo_we;
wire          slave_b_cdc_cdc_asyncfifo_writable;
wire    [2:0] slave_b_cdc_cdc_consume_wdomain;
wire          slave_b_cdc_cdc_fifo_in_first;
wire          slave_b_cdc_cdc_fifo_in_last;
wire    [1:0] slave_b_cdc_cdc_fifo_in_payload_resp;
wire          slave_b_cdc_cdc_fifo_out_first;
wire          slave_b_cdc_cdc_fifo_out_last;
wire    [1:0] slave_b_cdc_cdc_fifo_out_payload_resp;
wire          slave_b_cdc_cdc_graycounter0_ce;
reg     [2:0] slave_b_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] slave_b_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] slave_b_cdc_cdc_graycounter0_q_next;
reg     [2:0] slave_b_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          slave_b_cdc_cdc_graycounter1_ce;
reg     [2:0] slave_b_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] slave_b_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] slave_b_cdc_cdc_graycounter1_q_next;
reg     [2:0] slave_b_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] slave_b_cdc_cdc_produce_rdomain;
wire    [1:0] slave_b_cdc_cdc_rdport_adr;
wire    [3:0] slave_b_cdc_cdc_rdport_dat_r;
wire          slave_b_cdc_cdc_sink_first;
wire          slave_b_cdc_cdc_sink_last;
wire    [1:0] slave_b_cdc_cdc_sink_payload_resp;
wire          slave_b_cdc_cdc_sink_ready;
wire          slave_b_cdc_cdc_sink_valid;
wire          slave_b_cdc_cdc_source_first;
wire          slave_b_cdc_cdc_source_last;
wire    [1:0] slave_b_cdc_cdc_source_payload_resp;
wire          slave_b_cdc_cdc_source_ready;
wire          slave_b_cdc_cdc_source_valid;
wire    [1:0] slave_b_cdc_cdc_wrport_adr;
wire    [3:0] slave_b_cdc_cdc_wrport_dat_r;
wire    [3:0] slave_b_cdc_cdc_wrport_dat_w;
wire          slave_b_cdc_cdc_wrport_we;
wire          slave_b_cdc_sink_sink_first;
wire          slave_b_cdc_sink_sink_last;
wire    [1:0] slave_b_cdc_sink_sink_payload_resp;
wire          slave_b_cdc_sink_sink_ready;
wire          slave_b_cdc_sink_sink_valid;
wire          slave_b_cdc_source_source_first;
wire          slave_b_cdc_source_source_last;
wire    [1:0] slave_b_cdc_source_source_payload_resp;
wire          slave_b_cdc_source_source_ready;
wire          slave_b_cdc_source_source_valid;
wire   [35:0] slave_r_cdc_cdc_asyncfifo_din;
wire   [35:0] slave_r_cdc_cdc_asyncfifo_dout;
wire          slave_r_cdc_cdc_asyncfifo_re;
wire          slave_r_cdc_cdc_asyncfifo_readable;
wire          slave_r_cdc_cdc_asyncfifo_we;
wire          slave_r_cdc_cdc_asyncfifo_writable;
wire    [2:0] slave_r_cdc_cdc_consume_wdomain;
wire          slave_r_cdc_cdc_fifo_in_first;
wire          slave_r_cdc_cdc_fifo_in_last;
wire   [31:0] slave_r_cdc_cdc_fifo_in_payload_data;
wire    [1:0] slave_r_cdc_cdc_fifo_in_payload_resp;
wire          slave_r_cdc_cdc_fifo_out_first;
wire          slave_r_cdc_cdc_fifo_out_last;
wire   [31:0] slave_r_cdc_cdc_fifo_out_payload_data;
wire    [1:0] slave_r_cdc_cdc_fifo_out_payload_resp;
wire          slave_r_cdc_cdc_graycounter0_ce;
reg     [2:0] slave_r_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] slave_r_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] slave_r_cdc_cdc_graycounter0_q_next;
reg     [2:0] slave_r_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          slave_r_cdc_cdc_graycounter1_ce;
reg     [2:0] slave_r_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] slave_r_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] slave_r_cdc_cdc_graycounter1_q_next;
reg     [2:0] slave_r_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] slave_r_cdc_cdc_produce_rdomain;
wire    [1:0] slave_r_cdc_cdc_rdport_adr;
wire   [35:0] slave_r_cdc_cdc_rdport_dat_r;
wire          slave_r_cdc_cdc_sink_first;
wire          slave_r_cdc_cdc_sink_last;
wire   [31:0] slave_r_cdc_cdc_sink_payload_data;
wire    [1:0] slave_r_cdc_cdc_sink_payload_resp;
wire          slave_r_cdc_cdc_sink_ready;
wire          slave_r_cdc_cdc_sink_valid;
wire          slave_r_cdc_cdc_source_first;
wire          slave_r_cdc_cdc_source_last;
wire   [31:0] slave_r_cdc_cdc_source_payload_data;
wire    [1:0] slave_r_cdc_cdc_source_payload_resp;
wire          slave_r_cdc_cdc_source_ready;
wire          slave_r_cdc_cdc_source_valid;
wire    [1:0] slave_r_cdc_cdc_wrport_adr;
wire   [35:0] slave_r_cdc_cdc_wrport_dat_w;
wire          slave_r_cdc_cdc_wrport_we;
wire          slave_r_cdc_sink_sink_first;
wire          slave_r_cdc_sink_sink_last;
wire   [31:0] slave_r_cdc_sink_sink_payload_data;
wire    [1:0] slave_r_cdc_sink_sink_payload_resp;
wire          slave_r_cdc_sink_sink_ready;
wire          slave_r_cdc_sink_sink_valid;
wire          slave_r_cdc_source_source_first;
wire          slave_r_cdc_source_source_last;
wire   [31:0] slave_r_cdc_source_source_payload_data;
wire    [1:0] slave_r_cdc_source_source_payload_resp;
wire          slave_r_cdc_source_source_ready;
wire          slave_r_cdc_source_source_valid;
wire   [37:0] slave_w_cdc_cdc_asyncfifo_din;
wire   [37:0] slave_w_cdc_cdc_asyncfifo_dout;
wire          slave_w_cdc_cdc_asyncfifo_re;
wire          slave_w_cdc_cdc_asyncfifo_readable;
wire          slave_w_cdc_cdc_asyncfifo_we;
wire          slave_w_cdc_cdc_asyncfifo_writable;
wire    [2:0] slave_w_cdc_cdc_consume_wdomain;
wire          slave_w_cdc_cdc_fifo_in_first;
wire          slave_w_cdc_cdc_fifo_in_last;
wire   [31:0] slave_w_cdc_cdc_fifo_in_payload_data;
wire    [3:0] slave_w_cdc_cdc_fifo_in_payload_strb;
wire          slave_w_cdc_cdc_fifo_out_first;
wire          slave_w_cdc_cdc_fifo_out_last;
wire   [31:0] slave_w_cdc_cdc_fifo_out_payload_data;
wire    [3:0] slave_w_cdc_cdc_fifo_out_payload_strb;
wire          slave_w_cdc_cdc_graycounter0_ce;
reg     [2:0] slave_w_cdc_cdc_graycounter0_q = 3'd0;
reg     [2:0] slave_w_cdc_cdc_graycounter0_q_binary = 3'd0;
wire    [2:0] slave_w_cdc_cdc_graycounter0_q_next;
reg     [2:0] slave_w_cdc_cdc_graycounter0_q_next_binary = 3'd0;
wire          slave_w_cdc_cdc_graycounter1_ce;
reg     [2:0] slave_w_cdc_cdc_graycounter1_q = 3'd0;
reg     [2:0] slave_w_cdc_cdc_graycounter1_q_binary = 3'd0;
wire    [2:0] slave_w_cdc_cdc_graycounter1_q_next;
reg     [2:0] slave_w_cdc_cdc_graycounter1_q_next_binary = 3'd0;
wire    [2:0] slave_w_cdc_cdc_produce_rdomain;
wire    [1:0] slave_w_cdc_cdc_rdport_adr;
wire   [37:0] slave_w_cdc_cdc_rdport_dat_r;
wire          slave_w_cdc_cdc_sink_first;
wire          slave_w_cdc_cdc_sink_last;
wire   [31:0] slave_w_cdc_cdc_sink_payload_data;
wire    [3:0] slave_w_cdc_cdc_sink_payload_strb;
wire          slave_w_cdc_cdc_sink_ready;
wire          slave_w_cdc_cdc_sink_valid;
wire          slave_w_cdc_cdc_source_first;
wire          slave_w_cdc_cdc_source_last;
wire   [31:0] slave_w_cdc_cdc_source_payload_data;
wire    [3:0] slave_w_cdc_cdc_source_payload_strb;
wire          slave_w_cdc_cdc_source_ready;
wire          slave_w_cdc_cdc_source_valid;
wire    [1:0] slave_w_cdc_cdc_wrport_adr;
wire   [37:0] slave_w_cdc_cdc_wrport_dat_w;
wire          slave_w_cdc_cdc_wrport_we;
wire          slave_w_cdc_sink_sink_first;
wire          slave_w_cdc_sink_sink_last;
wire   [31:0] slave_w_cdc_sink_sink_payload_data;
wire    [3:0] slave_w_cdc_sink_sink_payload_strb;
wire          slave_w_cdc_sink_sink_ready;
wire          slave_w_cdc_sink_sink_valid;
wire          slave_w_cdc_source_source_first;
wire          slave_w_cdc_source_source_last;
wire   [31:0] slave_w_cdc_source_source_payload_data;
wire    [3:0] slave_w_cdc_source_source_payload_strb;
wire          slave_w_cdc_source_source_ready;
wire          slave_w_cdc_source_source_valid;


// Combinatorial Logic


assign slave_aw_cdc_sink_sink_valid = aw_valid_1;
assign aw_ready_1 = slave_aw_cdc_sink_sink_ready;
assign slave_aw_cdc_sink_sink_first = aw_first_1;
assign slave_aw_cdc_sink_sink_last = aw_last_1;
assign slave_aw_cdc_sink_sink_payload_addr = aw_payload_addr_1;
assign slave_aw_cdc_sink_sink_payload_prot = aw_payload_prot_1;
assign aw_valid = slave_aw_cdc_source_source_valid;
assign slave_aw_cdc_source_source_ready = aw_ready;
assign aw_first = slave_aw_cdc_source_source_first;
assign aw_last = slave_aw_cdc_source_source_last;
assign aw_payload_addr = slave_aw_cdc_source_source_payload_addr;
assign aw_payload_prot = slave_aw_cdc_source_source_payload_prot;
assign slave_w_cdc_sink_sink_valid = w_valid_1;
assign w_ready_1 = slave_w_cdc_sink_sink_ready;
assign slave_w_cdc_sink_sink_first = w_first_1;
assign slave_w_cdc_sink_sink_last = w_last_1;
assign slave_w_cdc_sink_sink_payload_data = w_payload_data_1;
assign slave_w_cdc_sink_sink_payload_strb = w_payload_strb_1;
assign w_valid = slave_w_cdc_source_source_valid;
assign slave_w_cdc_source_source_ready = w_ready;
assign w_first = slave_w_cdc_source_source_first;
assign w_last = slave_w_cdc_source_source_last;
assign w_payload_data = slave_w_cdc_source_source_payload_data;
assign w_payload_strb = slave_w_cdc_source_source_payload_strb;
assign slave_b_cdc_sink_sink_valid = b_valid;
assign b_ready = slave_b_cdc_sink_sink_ready;
assign slave_b_cdc_sink_sink_first = b_first_1;
assign slave_b_cdc_sink_sink_last = b_last_1;
assign slave_b_cdc_sink_sink_payload_resp = b_payload_resp_1;
assign b_valid_1 = slave_b_cdc_source_source_valid;
assign slave_b_cdc_source_source_ready = b_ready_1;
assign b_first = slave_b_cdc_source_source_first;
assign b_last = slave_b_cdc_source_source_last;
assign b_payload_resp = slave_b_cdc_source_source_payload_resp;
assign slave_ar_cdc_sink_sink_valid = ar_valid;
assign ar_ready = slave_ar_cdc_sink_sink_ready;
assign slave_ar_cdc_sink_sink_first = ar_first;
assign slave_ar_cdc_sink_sink_last = ar_last;
assign slave_ar_cdc_sink_sink_payload_addr = ar_payload_addr;
assign slave_ar_cdc_sink_sink_payload_prot = ar_payload_prot;
assign ar_valid_1 = slave_ar_cdc_source_source_valid;
assign slave_ar_cdc_source_source_ready = ar_ready_1;
assign ar_first_1 = slave_ar_cdc_source_source_first;
assign ar_last_1 = slave_ar_cdc_source_source_last;
assign ar_payload_addr_1 = slave_ar_cdc_source_source_payload_addr;
assign ar_payload_prot_1 = slave_ar_cdc_source_source_payload_prot;
assign slave_r_cdc_sink_sink_valid = r_valid_1;
assign r_ready_1 = slave_r_cdc_sink_sink_ready;
assign slave_r_cdc_sink_sink_first = r_first_1;
assign slave_r_cdc_sink_sink_last = r_last_1;
assign slave_r_cdc_sink_sink_payload_resp = r_payload_resp_1;
assign slave_r_cdc_sink_sink_payload_data = r_payload_data_1;
assign r_valid = slave_r_cdc_source_source_valid;
assign slave_r_cdc_source_source_ready = r_ready;
assign r_first = slave_r_cdc_source_source_first;
assign r_last = slave_r_cdc_source_source_last;
assign r_payload_resp = slave_r_cdc_source_source_payload_resp;
assign r_payload_data = slave_r_cdc_source_source_payload_data;
assign slave_aw_cdc_cdc_sink_valid = slave_aw_cdc_sink_sink_valid;
assign slave_aw_cdc_sink_sink_ready = slave_aw_cdc_cdc_sink_ready;
assign slave_aw_cdc_cdc_sink_first = slave_aw_cdc_sink_sink_first;
assign slave_aw_cdc_cdc_sink_last = slave_aw_cdc_sink_sink_last;
assign slave_aw_cdc_cdc_sink_payload_addr = slave_aw_cdc_sink_sink_payload_addr;
assign slave_aw_cdc_cdc_sink_payload_prot = slave_aw_cdc_sink_sink_payload_prot;
assign slave_aw_cdc_source_source_valid = slave_aw_cdc_cdc_source_valid;
assign slave_aw_cdc_cdc_source_ready = slave_aw_cdc_source_source_ready;
assign slave_aw_cdc_source_source_first = slave_aw_cdc_cdc_source_first;
assign slave_aw_cdc_source_source_last = slave_aw_cdc_cdc_source_last;
assign slave_aw_cdc_source_source_payload_addr = slave_aw_cdc_cdc_source_payload_addr;
assign slave_aw_cdc_source_source_payload_prot = slave_aw_cdc_cdc_source_payload_prot;
assign slave_aw_cdc_cdc_asyncfifo_din = {slave_aw_cdc_cdc_fifo_in_last, slave_aw_cdc_cdc_fifo_in_first, slave_aw_cdc_cdc_fifo_in_payload_prot, slave_aw_cdc_cdc_fifo_in_payload_addr};
assign {slave_aw_cdc_cdc_fifo_out_last, slave_aw_cdc_cdc_fifo_out_first, slave_aw_cdc_cdc_fifo_out_payload_prot, slave_aw_cdc_cdc_fifo_out_payload_addr} = slave_aw_cdc_cdc_asyncfifo_dout;
assign slave_aw_cdc_cdc_sink_ready = slave_aw_cdc_cdc_asyncfifo_writable;
assign slave_aw_cdc_cdc_asyncfifo_we = slave_aw_cdc_cdc_sink_valid;
assign slave_aw_cdc_cdc_fifo_in_first = slave_aw_cdc_cdc_sink_first;
assign slave_aw_cdc_cdc_fifo_in_last = slave_aw_cdc_cdc_sink_last;
assign slave_aw_cdc_cdc_fifo_in_payload_addr = slave_aw_cdc_cdc_sink_payload_addr;
assign slave_aw_cdc_cdc_fifo_in_payload_prot = slave_aw_cdc_cdc_sink_payload_prot;
assign slave_aw_cdc_cdc_source_valid = slave_aw_cdc_cdc_asyncfifo_readable;
assign slave_aw_cdc_cdc_source_first = slave_aw_cdc_cdc_fifo_out_first;
assign slave_aw_cdc_cdc_source_last = slave_aw_cdc_cdc_fifo_out_last;
assign slave_aw_cdc_cdc_source_payload_addr = slave_aw_cdc_cdc_fifo_out_payload_addr;
assign slave_aw_cdc_cdc_source_payload_prot = slave_aw_cdc_cdc_fifo_out_payload_prot;
assign slave_aw_cdc_cdc_asyncfifo_re = slave_aw_cdc_cdc_source_ready;
assign slave_aw_cdc_cdc_graycounter0_ce = (slave_aw_cdc_cdc_asyncfifo_writable & slave_aw_cdc_cdc_asyncfifo_we);
assign slave_aw_cdc_cdc_graycounter1_ce = (slave_aw_cdc_cdc_asyncfifo_readable & slave_aw_cdc_cdc_asyncfifo_re);
assign slave_aw_cdc_cdc_asyncfifo_writable = (((slave_aw_cdc_cdc_graycounter0_q[2] == slave_aw_cdc_cdc_consume_wdomain[2]) | (slave_aw_cdc_cdc_graycounter0_q[1] == slave_aw_cdc_cdc_consume_wdomain[1])) | (slave_aw_cdc_cdc_graycounter0_q[0] != slave_aw_cdc_cdc_consume_wdomain[0]));
assign slave_aw_cdc_cdc_asyncfifo_readable = (slave_aw_cdc_cdc_graycounter1_q != slave_aw_cdc_cdc_produce_rdomain);
assign slave_aw_cdc_cdc_wrport_adr = slave_aw_cdc_cdc_graycounter0_q_binary[1:0];
assign slave_aw_cdc_cdc_wrport_dat_w = slave_aw_cdc_cdc_asyncfifo_din;
assign slave_aw_cdc_cdc_wrport_we = slave_aw_cdc_cdc_graycounter0_ce;
assign slave_aw_cdc_cdc_rdport_adr = slave_aw_cdc_cdc_graycounter1_q_next_binary[1:0];
assign slave_aw_cdc_cdc_asyncfifo_dout = slave_aw_cdc_cdc_rdport_dat_r;
always @(*) begin
    slave_aw_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (slave_aw_cdc_cdc_graycounter0_ce) begin
        slave_aw_cdc_cdc_graycounter0_q_next_binary = (slave_aw_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        slave_aw_cdc_cdc_graycounter0_q_next_binary = slave_aw_cdc_cdc_graycounter0_q_binary;
    end
end
assign slave_aw_cdc_cdc_graycounter0_q_next = (slave_aw_cdc_cdc_graycounter0_q_next_binary ^ slave_aw_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    slave_aw_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (slave_aw_cdc_cdc_graycounter1_ce) begin
        slave_aw_cdc_cdc_graycounter1_q_next_binary = (slave_aw_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        slave_aw_cdc_cdc_graycounter1_q_next_binary = slave_aw_cdc_cdc_graycounter1_q_binary;
    end
end
assign slave_aw_cdc_cdc_graycounter1_q_next = (slave_aw_cdc_cdc_graycounter1_q_next_binary ^ slave_aw_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign slave_w_cdc_cdc_sink_valid = slave_w_cdc_sink_sink_valid;
assign slave_w_cdc_sink_sink_ready = slave_w_cdc_cdc_sink_ready;
assign slave_w_cdc_cdc_sink_first = slave_w_cdc_sink_sink_first;
assign slave_w_cdc_cdc_sink_last = slave_w_cdc_sink_sink_last;
assign slave_w_cdc_cdc_sink_payload_data = slave_w_cdc_sink_sink_payload_data;
assign slave_w_cdc_cdc_sink_payload_strb = slave_w_cdc_sink_sink_payload_strb;
assign slave_w_cdc_source_source_valid = slave_w_cdc_cdc_source_valid;
assign slave_w_cdc_cdc_source_ready = slave_w_cdc_source_source_ready;
assign slave_w_cdc_source_source_first = slave_w_cdc_cdc_source_first;
assign slave_w_cdc_source_source_last = slave_w_cdc_cdc_source_last;
assign slave_w_cdc_source_source_payload_data = slave_w_cdc_cdc_source_payload_data;
assign slave_w_cdc_source_source_payload_strb = slave_w_cdc_cdc_source_payload_strb;
assign slave_w_cdc_cdc_asyncfifo_din = {slave_w_cdc_cdc_fifo_in_last, slave_w_cdc_cdc_fifo_in_first, slave_w_cdc_cdc_fifo_in_payload_strb, slave_w_cdc_cdc_fifo_in_payload_data};
assign {slave_w_cdc_cdc_fifo_out_last, slave_w_cdc_cdc_fifo_out_first, slave_w_cdc_cdc_fifo_out_payload_strb, slave_w_cdc_cdc_fifo_out_payload_data} = slave_w_cdc_cdc_asyncfifo_dout;
assign slave_w_cdc_cdc_sink_ready = slave_w_cdc_cdc_asyncfifo_writable;
assign slave_w_cdc_cdc_asyncfifo_we = slave_w_cdc_cdc_sink_valid;
assign slave_w_cdc_cdc_fifo_in_first = slave_w_cdc_cdc_sink_first;
assign slave_w_cdc_cdc_fifo_in_last = slave_w_cdc_cdc_sink_last;
assign slave_w_cdc_cdc_fifo_in_payload_data = slave_w_cdc_cdc_sink_payload_data;
assign slave_w_cdc_cdc_fifo_in_payload_strb = slave_w_cdc_cdc_sink_payload_strb;
assign slave_w_cdc_cdc_source_valid = slave_w_cdc_cdc_asyncfifo_readable;
assign slave_w_cdc_cdc_source_first = slave_w_cdc_cdc_fifo_out_first;
assign slave_w_cdc_cdc_source_last = slave_w_cdc_cdc_fifo_out_last;
assign slave_w_cdc_cdc_source_payload_data = slave_w_cdc_cdc_fifo_out_payload_data;
assign slave_w_cdc_cdc_source_payload_strb = slave_w_cdc_cdc_fifo_out_payload_strb;
assign slave_w_cdc_cdc_asyncfifo_re = slave_w_cdc_cdc_source_ready;
assign slave_w_cdc_cdc_graycounter0_ce = (slave_w_cdc_cdc_asyncfifo_writable & slave_w_cdc_cdc_asyncfifo_we);
assign slave_w_cdc_cdc_graycounter1_ce = (slave_w_cdc_cdc_asyncfifo_readable & slave_w_cdc_cdc_asyncfifo_re);
assign slave_w_cdc_cdc_asyncfifo_writable = (((slave_w_cdc_cdc_graycounter0_q[2] == slave_w_cdc_cdc_consume_wdomain[2]) | (slave_w_cdc_cdc_graycounter0_q[1] == slave_w_cdc_cdc_consume_wdomain[1])) | (slave_w_cdc_cdc_graycounter0_q[0] != slave_w_cdc_cdc_consume_wdomain[0]));
assign slave_w_cdc_cdc_asyncfifo_readable = (slave_w_cdc_cdc_graycounter1_q != slave_w_cdc_cdc_produce_rdomain);
assign slave_w_cdc_cdc_wrport_adr = slave_w_cdc_cdc_graycounter0_q_binary[1:0];
assign slave_w_cdc_cdc_wrport_dat_w = slave_w_cdc_cdc_asyncfifo_din;
assign slave_w_cdc_cdc_wrport_we = slave_w_cdc_cdc_graycounter0_ce;
assign slave_w_cdc_cdc_rdport_adr = slave_w_cdc_cdc_graycounter1_q_next_binary[1:0];
assign slave_w_cdc_cdc_asyncfifo_dout = slave_w_cdc_cdc_rdport_dat_r;
assign slave_array_write_memory0_adr = slave_w_cdc_cdc_wrport_adr;
assign slave_array_write_memory0_we = slave_w_cdc_cdc_wrport_we;
assign slave_array_write_memory0_dat_w = slave_w_cdc_cdc_wrport_dat_w[35:0];
assign slave_array_read_memory0_adr = slave_w_cdc_cdc_rdport_adr;
assign slave_array_write_memory1_adr = slave_w_cdc_cdc_wrport_adr;
assign slave_array_write_memory1_we = slave_w_cdc_cdc_wrport_we;
assign slave_array_write_memory1_dat_w = slave_w_cdc_cdc_wrport_dat_w[37:36];
assign slave_array_read_memory1_adr = slave_w_cdc_cdc_rdport_adr;
assign slave_w_cdc_cdc_rdport_dat_r = {slave_array_read_memory1_dat_r, slave_array_read_memory0_dat_r};
always @(*) begin
    slave_w_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (slave_w_cdc_cdc_graycounter0_ce) begin
        slave_w_cdc_cdc_graycounter0_q_next_binary = (slave_w_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        slave_w_cdc_cdc_graycounter0_q_next_binary = slave_w_cdc_cdc_graycounter0_q_binary;
    end
end
assign slave_w_cdc_cdc_graycounter0_q_next = (slave_w_cdc_cdc_graycounter0_q_next_binary ^ slave_w_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    slave_w_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (slave_w_cdc_cdc_graycounter1_ce) begin
        slave_w_cdc_cdc_graycounter1_q_next_binary = (slave_w_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        slave_w_cdc_cdc_graycounter1_q_next_binary = slave_w_cdc_cdc_graycounter1_q_binary;
    end
end
assign slave_w_cdc_cdc_graycounter1_q_next = (slave_w_cdc_cdc_graycounter1_q_next_binary ^ slave_w_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign slave_b_cdc_cdc_sink_valid = slave_b_cdc_sink_sink_valid;
assign slave_b_cdc_sink_sink_ready = slave_b_cdc_cdc_sink_ready;
assign slave_b_cdc_cdc_sink_first = slave_b_cdc_sink_sink_first;
assign slave_b_cdc_cdc_sink_last = slave_b_cdc_sink_sink_last;
assign slave_b_cdc_cdc_sink_payload_resp = slave_b_cdc_sink_sink_payload_resp;
assign slave_b_cdc_source_source_valid = slave_b_cdc_cdc_source_valid;
assign slave_b_cdc_cdc_source_ready = slave_b_cdc_source_source_ready;
assign slave_b_cdc_source_source_first = slave_b_cdc_cdc_source_first;
assign slave_b_cdc_source_source_last = slave_b_cdc_cdc_source_last;
assign slave_b_cdc_source_source_payload_resp = slave_b_cdc_cdc_source_payload_resp;
assign slave_b_cdc_cdc_asyncfifo_din = {slave_b_cdc_cdc_fifo_in_last, slave_b_cdc_cdc_fifo_in_first, slave_b_cdc_cdc_fifo_in_payload_resp};
assign {slave_b_cdc_cdc_fifo_out_last, slave_b_cdc_cdc_fifo_out_first, slave_b_cdc_cdc_fifo_out_payload_resp} = slave_b_cdc_cdc_asyncfifo_dout;
assign slave_b_cdc_cdc_sink_ready = slave_b_cdc_cdc_asyncfifo_writable;
assign slave_b_cdc_cdc_asyncfifo_we = slave_b_cdc_cdc_sink_valid;
assign slave_b_cdc_cdc_fifo_in_first = slave_b_cdc_cdc_sink_first;
assign slave_b_cdc_cdc_fifo_in_last = slave_b_cdc_cdc_sink_last;
assign slave_b_cdc_cdc_fifo_in_payload_resp = slave_b_cdc_cdc_sink_payload_resp;
assign slave_b_cdc_cdc_source_valid = slave_b_cdc_cdc_asyncfifo_readable;
assign slave_b_cdc_cdc_source_first = slave_b_cdc_cdc_fifo_out_first;
assign slave_b_cdc_cdc_source_last = slave_b_cdc_cdc_fifo_out_last;
assign slave_b_cdc_cdc_source_payload_resp = slave_b_cdc_cdc_fifo_out_payload_resp;
assign slave_b_cdc_cdc_asyncfifo_re = slave_b_cdc_cdc_source_ready;
assign slave_b_cdc_cdc_graycounter0_ce = (slave_b_cdc_cdc_asyncfifo_writable & slave_b_cdc_cdc_asyncfifo_we);
assign slave_b_cdc_cdc_graycounter1_ce = (slave_b_cdc_cdc_asyncfifo_readable & slave_b_cdc_cdc_asyncfifo_re);
assign slave_b_cdc_cdc_asyncfifo_writable = (((slave_b_cdc_cdc_graycounter0_q[2] == slave_b_cdc_cdc_consume_wdomain[2]) | (slave_b_cdc_cdc_graycounter0_q[1] == slave_b_cdc_cdc_consume_wdomain[1])) | (slave_b_cdc_cdc_graycounter0_q[0] != slave_b_cdc_cdc_consume_wdomain[0]));
assign slave_b_cdc_cdc_asyncfifo_readable = (slave_b_cdc_cdc_graycounter1_q != slave_b_cdc_cdc_produce_rdomain);
assign slave_b_cdc_cdc_wrport_adr = slave_b_cdc_cdc_graycounter0_q_binary[1:0];
assign slave_b_cdc_cdc_wrport_dat_w = slave_b_cdc_cdc_asyncfifo_din;
assign slave_b_cdc_cdc_wrport_we = slave_b_cdc_cdc_graycounter0_ce;
assign slave_b_cdc_cdc_rdport_adr = slave_b_cdc_cdc_graycounter1_q_next_binary[1:0];
assign slave_b_cdc_cdc_asyncfifo_dout = slave_b_cdc_cdc_rdport_dat_r;
always @(*) begin
    slave_b_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (slave_b_cdc_cdc_graycounter0_ce) begin
        slave_b_cdc_cdc_graycounter0_q_next_binary = (slave_b_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        slave_b_cdc_cdc_graycounter0_q_next_binary = slave_b_cdc_cdc_graycounter0_q_binary;
    end
end
assign slave_b_cdc_cdc_graycounter0_q_next = (slave_b_cdc_cdc_graycounter0_q_next_binary ^ slave_b_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    slave_b_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (slave_b_cdc_cdc_graycounter1_ce) begin
        slave_b_cdc_cdc_graycounter1_q_next_binary = (slave_b_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        slave_b_cdc_cdc_graycounter1_q_next_binary = slave_b_cdc_cdc_graycounter1_q_binary;
    end
end
assign slave_b_cdc_cdc_graycounter1_q_next = (slave_b_cdc_cdc_graycounter1_q_next_binary ^ slave_b_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign slave_ar_cdc_cdc_sink_valid = slave_ar_cdc_sink_sink_valid;
assign slave_ar_cdc_sink_sink_ready = slave_ar_cdc_cdc_sink_ready;
assign slave_ar_cdc_cdc_sink_first = slave_ar_cdc_sink_sink_first;
assign slave_ar_cdc_cdc_sink_last = slave_ar_cdc_sink_sink_last;
assign slave_ar_cdc_cdc_sink_payload_addr = slave_ar_cdc_sink_sink_payload_addr;
assign slave_ar_cdc_cdc_sink_payload_prot = slave_ar_cdc_sink_sink_payload_prot;
assign slave_ar_cdc_source_source_valid = slave_ar_cdc_cdc_source_valid;
assign slave_ar_cdc_cdc_source_ready = slave_ar_cdc_source_source_ready;
assign slave_ar_cdc_source_source_first = slave_ar_cdc_cdc_source_first;
assign slave_ar_cdc_source_source_last = slave_ar_cdc_cdc_source_last;
assign slave_ar_cdc_source_source_payload_addr = slave_ar_cdc_cdc_source_payload_addr;
assign slave_ar_cdc_source_source_payload_prot = slave_ar_cdc_cdc_source_payload_prot;
assign slave_ar_cdc_cdc_asyncfifo_din = {slave_ar_cdc_cdc_fifo_in_last, slave_ar_cdc_cdc_fifo_in_first, slave_ar_cdc_cdc_fifo_in_payload_prot, slave_ar_cdc_cdc_fifo_in_payload_addr};
assign {slave_ar_cdc_cdc_fifo_out_last, slave_ar_cdc_cdc_fifo_out_first, slave_ar_cdc_cdc_fifo_out_payload_prot, slave_ar_cdc_cdc_fifo_out_payload_addr} = slave_ar_cdc_cdc_asyncfifo_dout;
assign slave_ar_cdc_cdc_sink_ready = slave_ar_cdc_cdc_asyncfifo_writable;
assign slave_ar_cdc_cdc_asyncfifo_we = slave_ar_cdc_cdc_sink_valid;
assign slave_ar_cdc_cdc_fifo_in_first = slave_ar_cdc_cdc_sink_first;
assign slave_ar_cdc_cdc_fifo_in_last = slave_ar_cdc_cdc_sink_last;
assign slave_ar_cdc_cdc_fifo_in_payload_addr = slave_ar_cdc_cdc_sink_payload_addr;
assign slave_ar_cdc_cdc_fifo_in_payload_prot = slave_ar_cdc_cdc_sink_payload_prot;
assign slave_ar_cdc_cdc_source_valid = slave_ar_cdc_cdc_asyncfifo_readable;
assign slave_ar_cdc_cdc_source_first = slave_ar_cdc_cdc_fifo_out_first;
assign slave_ar_cdc_cdc_source_last = slave_ar_cdc_cdc_fifo_out_last;
assign slave_ar_cdc_cdc_source_payload_addr = slave_ar_cdc_cdc_fifo_out_payload_addr;
assign slave_ar_cdc_cdc_source_payload_prot = slave_ar_cdc_cdc_fifo_out_payload_prot;
assign slave_ar_cdc_cdc_asyncfifo_re = slave_ar_cdc_cdc_source_ready;
assign slave_ar_cdc_cdc_graycounter0_ce = (slave_ar_cdc_cdc_asyncfifo_writable & slave_ar_cdc_cdc_asyncfifo_we);
assign slave_ar_cdc_cdc_graycounter1_ce = (slave_ar_cdc_cdc_asyncfifo_readable & slave_ar_cdc_cdc_asyncfifo_re);
assign slave_ar_cdc_cdc_asyncfifo_writable = (((slave_ar_cdc_cdc_graycounter0_q[2] == slave_ar_cdc_cdc_consume_wdomain[2]) | (slave_ar_cdc_cdc_graycounter0_q[1] == slave_ar_cdc_cdc_consume_wdomain[1])) | (slave_ar_cdc_cdc_graycounter0_q[0] != slave_ar_cdc_cdc_consume_wdomain[0]));
assign slave_ar_cdc_cdc_asyncfifo_readable = (slave_ar_cdc_cdc_graycounter1_q != slave_ar_cdc_cdc_produce_rdomain);
assign slave_ar_cdc_cdc_wrport_adr = slave_ar_cdc_cdc_graycounter0_q_binary[1:0];
assign slave_ar_cdc_cdc_wrport_dat_w = slave_ar_cdc_cdc_asyncfifo_din;
assign slave_ar_cdc_cdc_wrport_we = slave_ar_cdc_cdc_graycounter0_ce;
assign slave_ar_cdc_cdc_rdport_adr = slave_ar_cdc_cdc_graycounter1_q_next_binary[1:0];
assign slave_ar_cdc_cdc_asyncfifo_dout = slave_ar_cdc_cdc_rdport_dat_r;
always @(*) begin
    slave_ar_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (slave_ar_cdc_cdc_graycounter0_ce) begin
        slave_ar_cdc_cdc_graycounter0_q_next_binary = (slave_ar_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        slave_ar_cdc_cdc_graycounter0_q_next_binary = slave_ar_cdc_cdc_graycounter0_q_binary;
    end
end
assign slave_ar_cdc_cdc_graycounter0_q_next = (slave_ar_cdc_cdc_graycounter0_q_next_binary ^ slave_ar_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    slave_ar_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (slave_ar_cdc_cdc_graycounter1_ce) begin
        slave_ar_cdc_cdc_graycounter1_q_next_binary = (slave_ar_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        slave_ar_cdc_cdc_graycounter1_q_next_binary = slave_ar_cdc_cdc_graycounter1_q_binary;
    end
end
assign slave_ar_cdc_cdc_graycounter1_q_next = (slave_ar_cdc_cdc_graycounter1_q_next_binary ^ slave_ar_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign slave_r_cdc_cdc_sink_valid = slave_r_cdc_sink_sink_valid;
assign slave_r_cdc_sink_sink_ready = slave_r_cdc_cdc_sink_ready;
assign slave_r_cdc_cdc_sink_first = slave_r_cdc_sink_sink_first;
assign slave_r_cdc_cdc_sink_last = slave_r_cdc_sink_sink_last;
assign slave_r_cdc_cdc_sink_payload_resp = slave_r_cdc_sink_sink_payload_resp;
assign slave_r_cdc_cdc_sink_payload_data = slave_r_cdc_sink_sink_payload_data;
assign slave_r_cdc_source_source_valid = slave_r_cdc_cdc_source_valid;
assign slave_r_cdc_cdc_source_ready = slave_r_cdc_source_source_ready;
assign slave_r_cdc_source_source_first = slave_r_cdc_cdc_source_first;
assign slave_r_cdc_source_source_last = slave_r_cdc_cdc_source_last;
assign slave_r_cdc_source_source_payload_resp = slave_r_cdc_cdc_source_payload_resp;
assign slave_r_cdc_source_source_payload_data = slave_r_cdc_cdc_source_payload_data;
assign slave_r_cdc_cdc_asyncfifo_din = {slave_r_cdc_cdc_fifo_in_last, slave_r_cdc_cdc_fifo_in_first, slave_r_cdc_cdc_fifo_in_payload_data, slave_r_cdc_cdc_fifo_in_payload_resp};
assign {slave_r_cdc_cdc_fifo_out_last, slave_r_cdc_cdc_fifo_out_first, slave_r_cdc_cdc_fifo_out_payload_data, slave_r_cdc_cdc_fifo_out_payload_resp} = slave_r_cdc_cdc_asyncfifo_dout;
assign slave_r_cdc_cdc_sink_ready = slave_r_cdc_cdc_asyncfifo_writable;
assign slave_r_cdc_cdc_asyncfifo_we = slave_r_cdc_cdc_sink_valid;
assign slave_r_cdc_cdc_fifo_in_first = slave_r_cdc_cdc_sink_first;
assign slave_r_cdc_cdc_fifo_in_last = slave_r_cdc_cdc_sink_last;
assign slave_r_cdc_cdc_fifo_in_payload_resp = slave_r_cdc_cdc_sink_payload_resp;
assign slave_r_cdc_cdc_fifo_in_payload_data = slave_r_cdc_cdc_sink_payload_data;
assign slave_r_cdc_cdc_source_valid = slave_r_cdc_cdc_asyncfifo_readable;
assign slave_r_cdc_cdc_source_first = slave_r_cdc_cdc_fifo_out_first;
assign slave_r_cdc_cdc_source_last = slave_r_cdc_cdc_fifo_out_last;
assign slave_r_cdc_cdc_source_payload_resp = slave_r_cdc_cdc_fifo_out_payload_resp;
assign slave_r_cdc_cdc_source_payload_data = slave_r_cdc_cdc_fifo_out_payload_data;
assign slave_r_cdc_cdc_asyncfifo_re = slave_r_cdc_cdc_source_ready;
assign slave_r_cdc_cdc_graycounter0_ce = (slave_r_cdc_cdc_asyncfifo_writable & slave_r_cdc_cdc_asyncfifo_we);
assign slave_r_cdc_cdc_graycounter1_ce = (slave_r_cdc_cdc_asyncfifo_readable & slave_r_cdc_cdc_asyncfifo_re);
assign slave_r_cdc_cdc_asyncfifo_writable = (((slave_r_cdc_cdc_graycounter0_q[2] == slave_r_cdc_cdc_consume_wdomain[2]) | (slave_r_cdc_cdc_graycounter0_q[1] == slave_r_cdc_cdc_consume_wdomain[1])) | (slave_r_cdc_cdc_graycounter0_q[0] != slave_r_cdc_cdc_consume_wdomain[0]));
assign slave_r_cdc_cdc_asyncfifo_readable = (slave_r_cdc_cdc_graycounter1_q != slave_r_cdc_cdc_produce_rdomain);
assign slave_r_cdc_cdc_wrport_adr = slave_r_cdc_cdc_graycounter0_q_binary[1:0];
assign slave_r_cdc_cdc_wrport_dat_w = slave_r_cdc_cdc_asyncfifo_din;
assign slave_r_cdc_cdc_wrport_we = slave_r_cdc_cdc_graycounter0_ce;
assign slave_r_cdc_cdc_rdport_adr = slave_r_cdc_cdc_graycounter1_q_next_binary[1:0];
assign slave_r_cdc_cdc_asyncfifo_dout = slave_r_cdc_cdc_rdport_dat_r;
assign slave_array_write_memory2_adr = slave_r_cdc_cdc_wrport_adr;
assign slave_array_write_memory2_we = slave_r_cdc_cdc_wrport_we;
assign slave_array_write_memory2_dat_w = slave_r_cdc_cdc_wrport_dat_w[33:0];
assign slave_array_read_memory2_adr = slave_r_cdc_cdc_rdport_adr;
assign slave_array_write_memory3_adr = slave_r_cdc_cdc_wrport_adr;
assign slave_array_write_memory3_we = slave_r_cdc_cdc_wrport_we;
assign slave_array_write_memory3_dat_w = slave_r_cdc_cdc_wrport_dat_w[35:34];
assign slave_array_read_memory3_adr = slave_r_cdc_cdc_rdport_adr;
assign slave_r_cdc_cdc_rdport_dat_r = {slave_array_read_memory3_dat_r, slave_array_read_memory2_dat_r};
always @(*) begin
    slave_r_cdc_cdc_graycounter0_q_next_binary = 3'd0;
    if (slave_r_cdc_cdc_graycounter0_ce) begin
        slave_r_cdc_cdc_graycounter0_q_next_binary = (slave_r_cdc_cdc_graycounter0_q_binary + 1'd1);
    end else begin
        slave_r_cdc_cdc_graycounter0_q_next_binary = slave_r_cdc_cdc_graycounter0_q_binary;
    end
end
assign slave_r_cdc_cdc_graycounter0_q_next = (slave_r_cdc_cdc_graycounter0_q_next_binary ^ slave_r_cdc_cdc_graycounter0_q_next_binary[2:1]);
always @(*) begin
    slave_r_cdc_cdc_graycounter1_q_next_binary = 3'd0;
    if (slave_r_cdc_cdc_graycounter1_ce) begin
        slave_r_cdc_cdc_graycounter1_q_next_binary = (slave_r_cdc_cdc_graycounter1_q_binary + 1'd1);
    end else begin
        slave_r_cdc_cdc_graycounter1_q_next_binary = slave_r_cdc_cdc_graycounter1_q_binary;
    end
end
assign slave_r_cdc_cdc_graycounter1_q_next = (slave_r_cdc_cdc_graycounter1_q_next_binary ^ slave_r_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign slave_aw_cdc_cdc_produce_rdomain = multiregimpl01;
assign slave_aw_cdc_cdc_consume_wdomain = multiregimpl11;
assign slave_w_cdc_cdc_produce_rdomain = multiregimpl21;
assign slave_w_cdc_cdc_consume_wdomain = multiregimpl31;
assign slave_b_cdc_cdc_produce_rdomain = multiregimpl41;
assign slave_b_cdc_cdc_consume_wdomain = multiregimpl51;
assign slave_ar_cdc_cdc_produce_rdomain = multiregimpl61;
assign slave_ar_cdc_cdc_consume_wdomain = multiregimpl71;
assign slave_r_cdc_cdc_produce_rdomain = multiregimpl81;
assign slave_r_cdc_cdc_consume_wdomain = multiregimpl91;



// Synchronous Logic


always @(posedge milan_clk) begin
    slave_aw_cdc_cdc_graycounter1_q_binary <= slave_aw_cdc_cdc_graycounter1_q_next_binary;
    slave_aw_cdc_cdc_graycounter1_q <= slave_aw_cdc_cdc_graycounter1_q_next;
    slave_w_cdc_cdc_graycounter1_q_binary <= slave_w_cdc_cdc_graycounter1_q_next_binary;
    slave_w_cdc_cdc_graycounter1_q <= slave_w_cdc_cdc_graycounter1_q_next;
    slave_b_cdc_cdc_graycounter0_q_binary <= slave_b_cdc_cdc_graycounter0_q_next_binary;
    slave_b_cdc_cdc_graycounter0_q <= slave_b_cdc_cdc_graycounter0_q_next;
    slave_ar_cdc_cdc_graycounter1_q_binary <= slave_ar_cdc_cdc_graycounter1_q_next_binary;
    slave_ar_cdc_cdc_graycounter1_q <= slave_ar_cdc_cdc_graycounter1_q_next;
    slave_r_cdc_cdc_graycounter0_q_binary <= slave_r_cdc_cdc_graycounter0_q_next_binary;
    slave_r_cdc_cdc_graycounter0_q <= slave_r_cdc_cdc_graycounter0_q_next;
    if (milan_rst) begin
        slave_aw_cdc_cdc_graycounter1_q <= 3'd0;
        slave_aw_cdc_cdc_graycounter1_q_binary <= 3'd0;
        slave_w_cdc_cdc_graycounter1_q <= 3'd0;
        slave_w_cdc_cdc_graycounter1_q_binary <= 3'd0;
        slave_b_cdc_cdc_graycounter0_q <= 3'd0;
        slave_b_cdc_cdc_graycounter0_q_binary <= 3'd0;
        slave_ar_cdc_cdc_graycounter1_q <= 3'd0;
        slave_ar_cdc_cdc_graycounter1_q_binary <= 3'd0;
        slave_r_cdc_cdc_graycounter0_q <= 3'd0;
        slave_r_cdc_cdc_graycounter0_q_binary <= 3'd0;
    end
    multiregimpl00 <= slave_aw_cdc_cdc_graycounter0_q;
    multiregimpl01 <= multiregimpl00;
    multiregimpl20 <= slave_w_cdc_cdc_graycounter0_q;
    multiregimpl21 <= multiregimpl20;
    multiregimpl50 <= slave_b_cdc_cdc_graycounter1_q;
    multiregimpl51 <= multiregimpl50;
    multiregimpl60 <= slave_ar_cdc_cdc_graycounter0_q;
    multiregimpl61 <= multiregimpl60;
    multiregimpl90 <= slave_r_cdc_cdc_graycounter1_q;
    multiregimpl91 <= multiregimpl90;
end

always @(posedge sys_clk) begin
    slave_aw_cdc_cdc_graycounter0_q_binary <= slave_aw_cdc_cdc_graycounter0_q_next_binary;
    slave_aw_cdc_cdc_graycounter0_q <= slave_aw_cdc_cdc_graycounter0_q_next;
    slave_w_cdc_cdc_graycounter0_q_binary <= slave_w_cdc_cdc_graycounter0_q_next_binary;
    slave_w_cdc_cdc_graycounter0_q <= slave_w_cdc_cdc_graycounter0_q_next;
    slave_b_cdc_cdc_graycounter1_q_binary <= slave_b_cdc_cdc_graycounter1_q_next_binary;
    slave_b_cdc_cdc_graycounter1_q <= slave_b_cdc_cdc_graycounter1_q_next;
    slave_ar_cdc_cdc_graycounter0_q_binary <= slave_ar_cdc_cdc_graycounter0_q_next_binary;
    slave_ar_cdc_cdc_graycounter0_q <= slave_ar_cdc_cdc_graycounter0_q_next;
    slave_r_cdc_cdc_graycounter1_q_binary <= slave_r_cdc_cdc_graycounter1_q_next_binary;
    slave_r_cdc_cdc_graycounter1_q <= slave_r_cdc_cdc_graycounter1_q_next;
    if (sys_rst) begin
        slave_aw_cdc_cdc_graycounter0_q <= 3'd0;
        slave_aw_cdc_cdc_graycounter0_q_binary <= 3'd0;
        slave_w_cdc_cdc_graycounter0_q <= 3'd0;
        slave_w_cdc_cdc_graycounter0_q_binary <= 3'd0;
        slave_b_cdc_cdc_graycounter1_q <= 3'd0;
        slave_b_cdc_cdc_graycounter1_q_binary <= 3'd0;
        slave_ar_cdc_cdc_graycounter0_q <= 3'd0;
        slave_ar_cdc_cdc_graycounter0_q_binary <= 3'd0;
        slave_r_cdc_cdc_graycounter1_q <= 3'd0;
        slave_r_cdc_cdc_graycounter1_q_binary <= 3'd0;
    end
    multiregimpl10 <= slave_aw_cdc_cdc_graycounter1_q;
    multiregimpl11 <= multiregimpl10;
    multiregimpl30 <= slave_w_cdc_cdc_graycounter1_q;
    multiregimpl31 <= multiregimpl30;
    multiregimpl40 <= slave_b_cdc_cdc_graycounter0_q;
    multiregimpl41 <= multiregimpl40;
    multiregimpl70 <= slave_ar_cdc_cdc_graycounter1_q;
    multiregimpl71 <= multiregimpl70;
    multiregimpl80 <= slave_r_cdc_cdc_graycounter0_q;
    multiregimpl81 <= multiregimpl80;
end



// Specialized Logic



// Memory storage: 4-words x 37-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [36:0] storage[0:3];
reg [36:0] storage_dat0;
reg [36:0] storage_dat1;
always @(posedge sys_clk) begin
	if (slave_aw_cdc_cdc_wrport_we)
		storage[slave_aw_cdc_cdc_wrport_adr] <= slave_aw_cdc_cdc_wrport_dat_w;
	storage_dat0 <= storage[slave_aw_cdc_cdc_wrport_adr];
end
always @(posedge milan_clk) begin
	storage_dat1 <= storage[slave_aw_cdc_cdc_rdport_adr];
end
assign slave_aw_cdc_cdc_wrport_dat_r = storage_dat0;
assign slave_aw_cdc_cdc_rdport_dat_r = storage_dat1;



// Memory storage_1: 4-words x 4-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [3:0] storage_1[0:3];
reg [3:0] storage_1_dat0;
reg [3:0] storage_1_dat1;
always @(posedge milan_clk) begin
	if (slave_b_cdc_cdc_wrport_we)
		storage_1[slave_b_cdc_cdc_wrport_adr] <= slave_b_cdc_cdc_wrport_dat_w;
	storage_1_dat0 <= storage_1[slave_b_cdc_cdc_wrport_adr];
end
always @(posedge sys_clk) begin
	storage_1_dat1 <= storage_1[slave_b_cdc_cdc_rdport_adr];
end
assign slave_b_cdc_cdc_wrport_dat_r = storage_1_dat0;
assign slave_b_cdc_cdc_rdport_dat_r = storage_1_dat1;



// Memory storage_2: 4-words x 37-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [36:0] storage_2[0:3];
reg [36:0] storage_2_dat0;
reg [36:0] storage_2_dat1;
always @(posedge sys_clk) begin
	if (slave_ar_cdc_cdc_wrport_we)
		storage_2[slave_ar_cdc_cdc_wrport_adr] <= slave_ar_cdc_cdc_wrport_dat_w;
	storage_2_dat0 <= storage_2[slave_ar_cdc_cdc_wrport_adr];
end
always @(posedge milan_clk) begin
	storage_2_dat1 <= storage_2[slave_ar_cdc_cdc_rdport_adr];
end
assign slave_ar_cdc_cdc_wrport_dat_r = storage_2_dat0;
assign slave_ar_cdc_cdc_rdport_dat_r = storage_2_dat1;


(* ram_style = "block" *)

// Memory storage_3: 4-words x 36-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [35:0] storage_3[0:3];
reg [35:0] storage_3_dat0;
reg [35:0] storage_3_dat1;
always @(posedge sys_clk) begin
	if (slave_array_write_memory0_we)
		storage_3[slave_array_write_memory0_adr] <= slave_array_write_memory0_dat_w;
	storage_3_dat0 <= storage_3[slave_array_write_memory0_adr];
end
always @(posedge milan_clk) begin
	storage_3_dat1 <= storage_3[slave_array_read_memory0_adr];
end
assign slave_array_write_memory0_dat_r = storage_3_dat0;
assign slave_array_read_memory0_dat_r = storage_3_dat1;


(* ram_style = "distributed" *)

// Memory storage_4: 4-words x 2-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [1:0] storage_4[0:3];
reg [1:0] storage_4_dat0;
reg [1:0] storage_4_dat1;
always @(posedge sys_clk) begin
	if (slave_array_write_memory1_we)
		storage_4[slave_array_write_memory1_adr] <= slave_array_write_memory1_dat_w;
	storage_4_dat0 <= storage_4[slave_array_write_memory1_adr];
end
always @(posedge milan_clk) begin
	storage_4_dat1 <= storage_4[slave_array_read_memory1_adr];
end
assign slave_array_write_memory1_dat_r = storage_4_dat0;
assign slave_array_read_memory1_dat_r = storage_4_dat1;


(* ram_style = "block" *)

// Memory storage_5: 4-words x 34-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [33:0] storage_5[0:3];
reg [33:0] storage_5_dat0;
reg [33:0] storage_5_dat1;
always @(posedge milan_clk) begin
	if (slave_array_write_memory2_we)
		storage_5[slave_array_write_memory2_adr] <= slave_array_write_memory2_dat_w;
	storage_5_dat0 <= storage_5[slave_array_write_memory2_adr];
end
always @(posedge sys_clk) begin
	storage_5_dat1 <= storage_5[slave_array_read_memory2_adr];
end
assign slave_array_write_memory2_dat_r = storage_5_dat0;
assign slave_array_read_memory2_dat_r = storage_5_dat1;


(* ram_style = "distributed" *)

// Memory storage_6: 4-words x 2-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [1:0] storage_6[0:3];
reg [1:0] storage_6_dat0;
reg [1:0] storage_6_dat1;
always @(posedge milan_clk) begin
	if (slave_array_write_memory3_we)
		storage_6[slave_array_write_memory3_adr] <= slave_array_write_memory3_dat_w;
	storage_6_dat0 <= storage_6[slave_array_write_memory3_adr];
end
always @(posedge sys_clk) begin
	storage_6_dat1 <= storage_6[slave_array_read_memory3_adr];
end
assign slave_array_write_memory3_dat_r = storage_6_dat0;
assign slave_array_read_memory3_dat_r = storage_6_dat1;


endmodule






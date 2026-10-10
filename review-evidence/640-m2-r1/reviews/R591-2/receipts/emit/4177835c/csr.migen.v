/* Machine-generated using Migen */
module bench(
	input sys_clk,
	input sys_rst,
	input milan_clk,
	input milan_rst,
	input macsys_clk,
	input macsys_rst,
	input macdp_clk,
	input macdp_rst,
	input aw_valid,
	output aw_ready,
	input aw_first,
	input aw_last,
	input [31:0] aw_payload_addr,
	input [2:0] aw_payload_prot,
	input w_valid,
	output w_ready,
	input w_first,
	input w_last,
	input [31:0] w_payload_data,
	input [3:0] w_payload_strb,
	output b_valid,
	input b_ready,
	output b_first,
	output b_last,
	output [1:0] b_payload_resp,
	input ar_valid,
	output ar_ready,
	input ar_first,
	input ar_last,
	input [31:0] ar_payload_addr,
	input [2:0] ar_payload_prot,
	output r_valid,
	input r_ready,
	output r_first,
	output r_last,
	output [1:0] r_payload_resp,
	output [31:0] r_payload_data,
	output aw_valid_1,
	input aw_ready_1,
	output aw_first_1,
	output aw_last_1,
	output [31:0] aw_payload_addr_1,
	output [2:0] aw_payload_prot_1,
	output w_valid_1,
	input w_ready_1,
	output w_first_1,
	output w_last_1,
	output [31:0] w_payload_data_1,
	output [3:0] w_payload_strb_1,
	input b_valid_1,
	output b_ready_1,
	input b_first_1,
	input b_last_1,
	input [1:0] b_payload_resp_1,
	output ar_valid_1,
	input ar_ready_1,
	output ar_first_1,
	output ar_last_1,
	output [31:0] ar_payload_addr_1,
	output [2:0] ar_payload_prot_1,
	input r_valid_1,
	output r_ready_1,
	input r_first_1,
	input r_last_1,
	input [1:0] r_payload_resp_1,
	input [31:0] r_payload_data_1
);

wire slave_aw_cdc_sink_sink_valid;
wire slave_aw_cdc_sink_sink_ready;
wire slave_aw_cdc_sink_sink_first;
wire slave_aw_cdc_sink_sink_last;
wire [31:0] slave_aw_cdc_sink_sink_payload_addr;
wire [2:0] slave_aw_cdc_sink_sink_payload_prot;
wire slave_aw_cdc_source_source_valid;
wire slave_aw_cdc_source_source_ready;
wire slave_aw_cdc_source_source_first;
wire slave_aw_cdc_source_source_last;
wire [31:0] slave_aw_cdc_source_source_payload_addr;
wire [2:0] slave_aw_cdc_source_source_payload_prot;
wire slave_aw_cdc_cdc_sink_valid;
wire slave_aw_cdc_cdc_sink_ready;
wire slave_aw_cdc_cdc_sink_first;
wire slave_aw_cdc_cdc_sink_last;
wire [31:0] slave_aw_cdc_cdc_sink_payload_addr;
wire [2:0] slave_aw_cdc_cdc_sink_payload_prot;
wire slave_aw_cdc_cdc_source_valid;
wire slave_aw_cdc_cdc_source_ready;
wire slave_aw_cdc_cdc_source_first;
wire slave_aw_cdc_cdc_source_last;
wire [31:0] slave_aw_cdc_cdc_source_payload_addr;
wire [2:0] slave_aw_cdc_cdc_source_payload_prot;
wire slave_aw_cdc_cdc_asyncfifo_we;
wire slave_aw_cdc_cdc_asyncfifo_writable;
wire slave_aw_cdc_cdc_asyncfifo_re;
wire slave_aw_cdc_cdc_asyncfifo_readable;
wire [36:0] slave_aw_cdc_cdc_asyncfifo_din;
wire [36:0] slave_aw_cdc_cdc_asyncfifo_dout;
wire slave_aw_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] slave_aw_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] slave_aw_cdc_cdc_graycounter0_q_next;
reg [2:0] slave_aw_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] slave_aw_cdc_cdc_graycounter0_q_next_binary;
wire slave_aw_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] slave_aw_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] slave_aw_cdc_cdc_graycounter1_q_next;
reg [2:0] slave_aw_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] slave_aw_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] slave_aw_cdc_cdc_produce_rdomain;
wire [2:0] slave_aw_cdc_cdc_consume_wdomain;
wire [1:0] slave_aw_cdc_cdc_wrport_adr;
wire [36:0] slave_aw_cdc_cdc_wrport_dat_r;
wire slave_aw_cdc_cdc_wrport_we;
wire [36:0] slave_aw_cdc_cdc_wrport_dat_w;
wire [1:0] slave_aw_cdc_cdc_rdport_adr;
wire [36:0] slave_aw_cdc_cdc_rdport_dat_r;
wire [31:0] slave_aw_cdc_cdc_fifo_in_payload_addr;
wire [2:0] slave_aw_cdc_cdc_fifo_in_payload_prot;
wire slave_aw_cdc_cdc_fifo_in_first;
wire slave_aw_cdc_cdc_fifo_in_last;
wire [31:0] slave_aw_cdc_cdc_fifo_out_payload_addr;
wire [2:0] slave_aw_cdc_cdc_fifo_out_payload_prot;
wire slave_aw_cdc_cdc_fifo_out_first;
wire slave_aw_cdc_cdc_fifo_out_last;
wire slave_w_cdc_sink_sink_valid;
wire slave_w_cdc_sink_sink_ready;
wire slave_w_cdc_sink_sink_first;
wire slave_w_cdc_sink_sink_last;
wire [31:0] slave_w_cdc_sink_sink_payload_data;
wire [3:0] slave_w_cdc_sink_sink_payload_strb;
wire slave_w_cdc_source_source_valid;
wire slave_w_cdc_source_source_ready;
wire slave_w_cdc_source_source_first;
wire slave_w_cdc_source_source_last;
wire [31:0] slave_w_cdc_source_source_payload_data;
wire [3:0] slave_w_cdc_source_source_payload_strb;
wire slave_w_cdc_cdc_sink_valid;
wire slave_w_cdc_cdc_sink_ready;
wire slave_w_cdc_cdc_sink_first;
wire slave_w_cdc_cdc_sink_last;
wire [31:0] slave_w_cdc_cdc_sink_payload_data;
wire [3:0] slave_w_cdc_cdc_sink_payload_strb;
wire slave_w_cdc_cdc_source_valid;
wire slave_w_cdc_cdc_source_ready;
wire slave_w_cdc_cdc_source_first;
wire slave_w_cdc_cdc_source_last;
wire [31:0] slave_w_cdc_cdc_source_payload_data;
wire [3:0] slave_w_cdc_cdc_source_payload_strb;
wire slave_w_cdc_cdc_asyncfifo_we;
wire slave_w_cdc_cdc_asyncfifo_writable;
wire slave_w_cdc_cdc_asyncfifo_re;
wire slave_w_cdc_cdc_asyncfifo_readable;
wire [37:0] slave_w_cdc_cdc_asyncfifo_din;
wire [37:0] slave_w_cdc_cdc_asyncfifo_dout;
wire slave_w_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] slave_w_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] slave_w_cdc_cdc_graycounter0_q_next;
reg [2:0] slave_w_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] slave_w_cdc_cdc_graycounter0_q_next_binary;
wire slave_w_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] slave_w_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] slave_w_cdc_cdc_graycounter1_q_next;
reg [2:0] slave_w_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] slave_w_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] slave_w_cdc_cdc_produce_rdomain;
wire [2:0] slave_w_cdc_cdc_consume_wdomain;
wire [1:0] slave_w_cdc_cdc_wrport_adr;
wire slave_w_cdc_cdc_wrport_we;
wire [37:0] slave_w_cdc_cdc_wrport_dat_w;
wire [1:0] slave_w_cdc_cdc_rdport_adr;
wire [37:0] slave_w_cdc_cdc_rdport_dat_r;
wire [31:0] slave_w_cdc_cdc_fifo_in_payload_data;
wire [3:0] slave_w_cdc_cdc_fifo_in_payload_strb;
wire slave_w_cdc_cdc_fifo_in_first;
wire slave_w_cdc_cdc_fifo_in_last;
wire [31:0] slave_w_cdc_cdc_fifo_out_payload_data;
wire [3:0] slave_w_cdc_cdc_fifo_out_payload_strb;
wire slave_w_cdc_cdc_fifo_out_first;
wire slave_w_cdc_cdc_fifo_out_last;
wire slave_b_cdc_sink_sink_valid;
wire slave_b_cdc_sink_sink_ready;
wire slave_b_cdc_sink_sink_first;
wire slave_b_cdc_sink_sink_last;
wire [1:0] slave_b_cdc_sink_sink_payload_resp;
wire slave_b_cdc_source_source_valid;
wire slave_b_cdc_source_source_ready;
wire slave_b_cdc_source_source_first;
wire slave_b_cdc_source_source_last;
wire [1:0] slave_b_cdc_source_source_payload_resp;
wire slave_b_cdc_cdc_sink_valid;
wire slave_b_cdc_cdc_sink_ready;
wire slave_b_cdc_cdc_sink_first;
wire slave_b_cdc_cdc_sink_last;
wire [1:0] slave_b_cdc_cdc_sink_payload_resp;
wire slave_b_cdc_cdc_source_valid;
wire slave_b_cdc_cdc_source_ready;
wire slave_b_cdc_cdc_source_first;
wire slave_b_cdc_cdc_source_last;
wire [1:0] slave_b_cdc_cdc_source_payload_resp;
wire slave_b_cdc_cdc_asyncfifo_we;
wire slave_b_cdc_cdc_asyncfifo_writable;
wire slave_b_cdc_cdc_asyncfifo_re;
wire slave_b_cdc_cdc_asyncfifo_readable;
wire [3:0] slave_b_cdc_cdc_asyncfifo_din;
wire [3:0] slave_b_cdc_cdc_asyncfifo_dout;
wire slave_b_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] slave_b_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] slave_b_cdc_cdc_graycounter0_q_next;
reg [2:0] slave_b_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] slave_b_cdc_cdc_graycounter0_q_next_binary;
wire slave_b_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] slave_b_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] slave_b_cdc_cdc_graycounter1_q_next;
reg [2:0] slave_b_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] slave_b_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] slave_b_cdc_cdc_produce_rdomain;
wire [2:0] slave_b_cdc_cdc_consume_wdomain;
wire [1:0] slave_b_cdc_cdc_wrport_adr;
wire [3:0] slave_b_cdc_cdc_wrport_dat_r;
wire slave_b_cdc_cdc_wrport_we;
wire [3:0] slave_b_cdc_cdc_wrport_dat_w;
wire [1:0] slave_b_cdc_cdc_rdport_adr;
wire [3:0] slave_b_cdc_cdc_rdport_dat_r;
wire [1:0] slave_b_cdc_cdc_fifo_in_payload_resp;
wire slave_b_cdc_cdc_fifo_in_first;
wire slave_b_cdc_cdc_fifo_in_last;
wire [1:0] slave_b_cdc_cdc_fifo_out_payload_resp;
wire slave_b_cdc_cdc_fifo_out_first;
wire slave_b_cdc_cdc_fifo_out_last;
wire slave_ar_cdc_sink_sink_valid;
wire slave_ar_cdc_sink_sink_ready;
wire slave_ar_cdc_sink_sink_first;
wire slave_ar_cdc_sink_sink_last;
wire [31:0] slave_ar_cdc_sink_sink_payload_addr;
wire [2:0] slave_ar_cdc_sink_sink_payload_prot;
wire slave_ar_cdc_source_source_valid;
wire slave_ar_cdc_source_source_ready;
wire slave_ar_cdc_source_source_first;
wire slave_ar_cdc_source_source_last;
wire [31:0] slave_ar_cdc_source_source_payload_addr;
wire [2:0] slave_ar_cdc_source_source_payload_prot;
wire slave_ar_cdc_cdc_sink_valid;
wire slave_ar_cdc_cdc_sink_ready;
wire slave_ar_cdc_cdc_sink_first;
wire slave_ar_cdc_cdc_sink_last;
wire [31:0] slave_ar_cdc_cdc_sink_payload_addr;
wire [2:0] slave_ar_cdc_cdc_sink_payload_prot;
wire slave_ar_cdc_cdc_source_valid;
wire slave_ar_cdc_cdc_source_ready;
wire slave_ar_cdc_cdc_source_first;
wire slave_ar_cdc_cdc_source_last;
wire [31:0] slave_ar_cdc_cdc_source_payload_addr;
wire [2:0] slave_ar_cdc_cdc_source_payload_prot;
wire slave_ar_cdc_cdc_asyncfifo_we;
wire slave_ar_cdc_cdc_asyncfifo_writable;
wire slave_ar_cdc_cdc_asyncfifo_re;
wire slave_ar_cdc_cdc_asyncfifo_readable;
wire [36:0] slave_ar_cdc_cdc_asyncfifo_din;
wire [36:0] slave_ar_cdc_cdc_asyncfifo_dout;
wire slave_ar_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] slave_ar_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] slave_ar_cdc_cdc_graycounter0_q_next;
reg [2:0] slave_ar_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] slave_ar_cdc_cdc_graycounter0_q_next_binary;
wire slave_ar_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] slave_ar_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] slave_ar_cdc_cdc_graycounter1_q_next;
reg [2:0] slave_ar_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] slave_ar_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] slave_ar_cdc_cdc_produce_rdomain;
wire [2:0] slave_ar_cdc_cdc_consume_wdomain;
wire [1:0] slave_ar_cdc_cdc_wrport_adr;
wire [36:0] slave_ar_cdc_cdc_wrport_dat_r;
wire slave_ar_cdc_cdc_wrport_we;
wire [36:0] slave_ar_cdc_cdc_wrport_dat_w;
wire [1:0] slave_ar_cdc_cdc_rdport_adr;
wire [36:0] slave_ar_cdc_cdc_rdport_dat_r;
wire [31:0] slave_ar_cdc_cdc_fifo_in_payload_addr;
wire [2:0] slave_ar_cdc_cdc_fifo_in_payload_prot;
wire slave_ar_cdc_cdc_fifo_in_first;
wire slave_ar_cdc_cdc_fifo_in_last;
wire [31:0] slave_ar_cdc_cdc_fifo_out_payload_addr;
wire [2:0] slave_ar_cdc_cdc_fifo_out_payload_prot;
wire slave_ar_cdc_cdc_fifo_out_first;
wire slave_ar_cdc_cdc_fifo_out_last;
wire slave_r_cdc_sink_sink_valid;
wire slave_r_cdc_sink_sink_ready;
wire slave_r_cdc_sink_sink_first;
wire slave_r_cdc_sink_sink_last;
wire [1:0] slave_r_cdc_sink_sink_payload_resp;
wire [31:0] slave_r_cdc_sink_sink_payload_data;
wire slave_r_cdc_source_source_valid;
wire slave_r_cdc_source_source_ready;
wire slave_r_cdc_source_source_first;
wire slave_r_cdc_source_source_last;
wire [1:0] slave_r_cdc_source_source_payload_resp;
wire [31:0] slave_r_cdc_source_source_payload_data;
wire slave_r_cdc_cdc_sink_valid;
wire slave_r_cdc_cdc_sink_ready;
wire slave_r_cdc_cdc_sink_first;
wire slave_r_cdc_cdc_sink_last;
wire [1:0] slave_r_cdc_cdc_sink_payload_resp;
wire [31:0] slave_r_cdc_cdc_sink_payload_data;
wire slave_r_cdc_cdc_source_valid;
wire slave_r_cdc_cdc_source_ready;
wire slave_r_cdc_cdc_source_first;
wire slave_r_cdc_cdc_source_last;
wire [1:0] slave_r_cdc_cdc_source_payload_resp;
wire [31:0] slave_r_cdc_cdc_source_payload_data;
wire slave_r_cdc_cdc_asyncfifo_we;
wire slave_r_cdc_cdc_asyncfifo_writable;
wire slave_r_cdc_cdc_asyncfifo_re;
wire slave_r_cdc_cdc_asyncfifo_readable;
wire [35:0] slave_r_cdc_cdc_asyncfifo_din;
wire [35:0] slave_r_cdc_cdc_asyncfifo_dout;
wire slave_r_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] slave_r_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] slave_r_cdc_cdc_graycounter0_q_next;
reg [2:0] slave_r_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] slave_r_cdc_cdc_graycounter0_q_next_binary;
wire slave_r_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] slave_r_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] slave_r_cdc_cdc_graycounter1_q_next;
reg [2:0] slave_r_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] slave_r_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] slave_r_cdc_cdc_produce_rdomain;
wire [2:0] slave_r_cdc_cdc_consume_wdomain;
wire [1:0] slave_r_cdc_cdc_wrport_adr;
wire slave_r_cdc_cdc_wrport_we;
wire [35:0] slave_r_cdc_cdc_wrport_dat_w;
wire [1:0] slave_r_cdc_cdc_rdport_adr;
wire [35:0] slave_r_cdc_cdc_rdport_dat_r;
wire [1:0] slave_r_cdc_cdc_fifo_in_payload_resp;
wire [31:0] slave_r_cdc_cdc_fifo_in_payload_data;
wire slave_r_cdc_cdc_fifo_in_first;
wire slave_r_cdc_cdc_fifo_in_last;
wire [1:0] slave_r_cdc_cdc_fifo_out_payload_resp;
wire [31:0] slave_r_cdc_cdc_fifo_out_payload_data;
wire slave_r_cdc_cdc_fifo_out_first;
wire slave_r_cdc_cdc_fifo_out_last;
wire [1:0] slave_array_write_memory0_adr;
wire [35:0] slave_array_write_memory0_dat_r;
wire slave_array_write_memory0_we;
wire [35:0] slave_array_write_memory0_dat_w;
wire [1:0] slave_array_read_memory0_adr;
wire [35:0] slave_array_read_memory0_dat_r;
wire [1:0] slave_array_write_memory1_adr;
wire [1:0] slave_array_write_memory1_dat_r;
wire slave_array_write_memory1_we;
wire [1:0] slave_array_write_memory1_dat_w;
wire [1:0] slave_array_read_memory1_adr;
wire [1:0] slave_array_read_memory1_dat_r;
wire [1:0] slave_array_write_memory2_adr;
wire [33:0] slave_array_write_memory2_dat_r;
wire slave_array_write_memory2_we;
wire [33:0] slave_array_write_memory2_dat_w;
wire [1:0] slave_array_read_memory2_adr;
wire [33:0] slave_array_read_memory2_dat_r;
wire [1:0] slave_array_write_memory3_adr;
wire [1:0] slave_array_write_memory3_dat_r;
wire slave_array_write_memory3_we;
wire [1:0] slave_array_write_memory3_dat_w;
wire [1:0] slave_array_read_memory3_adr;
wire [1:0] slave_array_read_memory3_dat_r;
(* no_retiming = "true" *) reg [2:0] multiregimpl00 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl01 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl10 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl11 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl20 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl21 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl30 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl31 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl40 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl41 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl50 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl51 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl60 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl61 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl70 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl71 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl80 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl81 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl90 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl91 = 3'd0;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign slave_aw_cdc_sink_sink_valid = aw_valid;
assign aw_ready = slave_aw_cdc_sink_sink_ready;
assign slave_aw_cdc_sink_sink_first = aw_first;
assign slave_aw_cdc_sink_sink_last = aw_last;
assign slave_aw_cdc_sink_sink_payload_addr = aw_payload_addr;
assign slave_aw_cdc_sink_sink_payload_prot = aw_payload_prot;
assign aw_valid_1 = slave_aw_cdc_source_source_valid;
assign slave_aw_cdc_source_source_ready = aw_ready_1;
assign aw_first_1 = slave_aw_cdc_source_source_first;
assign aw_last_1 = slave_aw_cdc_source_source_last;
assign aw_payload_addr_1 = slave_aw_cdc_source_source_payload_addr;
assign aw_payload_prot_1 = slave_aw_cdc_source_source_payload_prot;
assign slave_w_cdc_sink_sink_valid = w_valid;
assign w_ready = slave_w_cdc_sink_sink_ready;
assign slave_w_cdc_sink_sink_first = w_first;
assign slave_w_cdc_sink_sink_last = w_last;
assign slave_w_cdc_sink_sink_payload_data = w_payload_data;
assign slave_w_cdc_sink_sink_payload_strb = w_payload_strb;
assign w_valid_1 = slave_w_cdc_source_source_valid;
assign slave_w_cdc_source_source_ready = w_ready_1;
assign w_first_1 = slave_w_cdc_source_source_first;
assign w_last_1 = slave_w_cdc_source_source_last;
assign w_payload_data_1 = slave_w_cdc_source_source_payload_data;
assign w_payload_strb_1 = slave_w_cdc_source_source_payload_strb;
assign slave_b_cdc_sink_sink_valid = b_valid_1;
assign b_ready_1 = slave_b_cdc_sink_sink_ready;
assign slave_b_cdc_sink_sink_first = b_first_1;
assign slave_b_cdc_sink_sink_last = b_last_1;
assign slave_b_cdc_sink_sink_payload_resp = b_payload_resp_1;
assign b_valid = slave_b_cdc_source_source_valid;
assign slave_b_cdc_source_source_ready = b_ready;
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

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	slave_aw_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (slave_aw_cdc_cdc_graycounter0_ce) begin
		slave_aw_cdc_cdc_graycounter0_q_next_binary <= (slave_aw_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		slave_aw_cdc_cdc_graycounter0_q_next_binary <= slave_aw_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end
assign slave_aw_cdc_cdc_graycounter0_q_next = (slave_aw_cdc_cdc_graycounter0_q_next_binary ^ slave_aw_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_1;
// synthesis translate_on
always @(*) begin
	slave_aw_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (slave_aw_cdc_cdc_graycounter1_ce) begin
		slave_aw_cdc_cdc_graycounter1_q_next_binary <= (slave_aw_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		slave_aw_cdc_cdc_graycounter1_q_next_binary <= slave_aw_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_1 <= dummy_s;
// synthesis translate_on
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

// synthesis translate_off
reg dummy_d_2;
// synthesis translate_on
always @(*) begin
	slave_w_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (slave_w_cdc_cdc_graycounter0_ce) begin
		slave_w_cdc_cdc_graycounter0_q_next_binary <= (slave_w_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		slave_w_cdc_cdc_graycounter0_q_next_binary <= slave_w_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_2 <= dummy_s;
// synthesis translate_on
end
assign slave_w_cdc_cdc_graycounter0_q_next = (slave_w_cdc_cdc_graycounter0_q_next_binary ^ slave_w_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_3;
// synthesis translate_on
always @(*) begin
	slave_w_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (slave_w_cdc_cdc_graycounter1_ce) begin
		slave_w_cdc_cdc_graycounter1_q_next_binary <= (slave_w_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		slave_w_cdc_cdc_graycounter1_q_next_binary <= slave_w_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_3 <= dummy_s;
// synthesis translate_on
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

// synthesis translate_off
reg dummy_d_4;
// synthesis translate_on
always @(*) begin
	slave_b_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (slave_b_cdc_cdc_graycounter0_ce) begin
		slave_b_cdc_cdc_graycounter0_q_next_binary <= (slave_b_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		slave_b_cdc_cdc_graycounter0_q_next_binary <= slave_b_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_4 <= dummy_s;
// synthesis translate_on
end
assign slave_b_cdc_cdc_graycounter0_q_next = (slave_b_cdc_cdc_graycounter0_q_next_binary ^ slave_b_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_5;
// synthesis translate_on
always @(*) begin
	slave_b_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (slave_b_cdc_cdc_graycounter1_ce) begin
		slave_b_cdc_cdc_graycounter1_q_next_binary <= (slave_b_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		slave_b_cdc_cdc_graycounter1_q_next_binary <= slave_b_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_5 <= dummy_s;
// synthesis translate_on
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

// synthesis translate_off
reg dummy_d_6;
// synthesis translate_on
always @(*) begin
	slave_ar_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (slave_ar_cdc_cdc_graycounter0_ce) begin
		slave_ar_cdc_cdc_graycounter0_q_next_binary <= (slave_ar_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		slave_ar_cdc_cdc_graycounter0_q_next_binary <= slave_ar_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_6 <= dummy_s;
// synthesis translate_on
end
assign slave_ar_cdc_cdc_graycounter0_q_next = (slave_ar_cdc_cdc_graycounter0_q_next_binary ^ slave_ar_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_7;
// synthesis translate_on
always @(*) begin
	slave_ar_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (slave_ar_cdc_cdc_graycounter1_ce) begin
		slave_ar_cdc_cdc_graycounter1_q_next_binary <= (slave_ar_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		slave_ar_cdc_cdc_graycounter1_q_next_binary <= slave_ar_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_7 <= dummy_s;
// synthesis translate_on
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

// synthesis translate_off
reg dummy_d_8;
// synthesis translate_on
always @(*) begin
	slave_r_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (slave_r_cdc_cdc_graycounter0_ce) begin
		slave_r_cdc_cdc_graycounter0_q_next_binary <= (slave_r_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		slave_r_cdc_cdc_graycounter0_q_next_binary <= slave_r_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_8 <= dummy_s;
// synthesis translate_on
end
assign slave_r_cdc_cdc_graycounter0_q_next = (slave_r_cdc_cdc_graycounter0_q_next_binary ^ slave_r_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_9;
// synthesis translate_on
always @(*) begin
	slave_r_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (slave_r_cdc_cdc_graycounter1_ce) begin
		slave_r_cdc_cdc_graycounter1_q_next_binary <= (slave_r_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		slave_r_cdc_cdc_graycounter1_q_next_binary <= slave_r_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_9 <= dummy_s;
// synthesis translate_on
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

reg [36:0] storage[0:3];
reg [1:0] memadr;
reg [1:0] memadr_1;
always @(posedge sys_clk) begin
	if (slave_aw_cdc_cdc_wrport_we)
		storage[slave_aw_cdc_cdc_wrport_adr] <= slave_aw_cdc_cdc_wrport_dat_w;
	memadr <= slave_aw_cdc_cdc_wrport_adr;
end

always @(posedge milan_clk) begin
	memadr_1 <= slave_aw_cdc_cdc_rdport_adr;
end

assign slave_aw_cdc_cdc_wrport_dat_r = storage[memadr];
assign slave_aw_cdc_cdc_rdport_dat_r = storage[memadr_1];

reg [3:0] storage_1[0:3];
reg [1:0] memadr_2;
reg [1:0] memadr_3;
always @(posedge milan_clk) begin
	if (slave_b_cdc_cdc_wrport_we)
		storage_1[slave_b_cdc_cdc_wrport_adr] <= slave_b_cdc_cdc_wrport_dat_w;
	memadr_2 <= slave_b_cdc_cdc_wrport_adr;
end

always @(posedge sys_clk) begin
	memadr_3 <= slave_b_cdc_cdc_rdport_adr;
end

assign slave_b_cdc_cdc_wrport_dat_r = storage_1[memadr_2];
assign slave_b_cdc_cdc_rdport_dat_r = storage_1[memadr_3];

reg [36:0] storage_2[0:3];
reg [1:0] memadr_4;
reg [1:0] memadr_5;
always @(posedge sys_clk) begin
	if (slave_ar_cdc_cdc_wrport_we)
		storage_2[slave_ar_cdc_cdc_wrport_adr] <= slave_ar_cdc_cdc_wrport_dat_w;
	memadr_4 <= slave_ar_cdc_cdc_wrport_adr;
end

always @(posedge milan_clk) begin
	memadr_5 <= slave_ar_cdc_cdc_rdport_adr;
end

assign slave_ar_cdc_cdc_wrport_dat_r = storage_2[memadr_4];
assign slave_ar_cdc_cdc_rdport_dat_r = storage_2[memadr_5];

(* ram_style = "block" *) reg [35:0] storage_3[0:3];
reg [1:0] memadr_6;
reg [1:0] memadr_7;
always @(posedge sys_clk) begin
	if (slave_array_write_memory0_we)
		storage_3[slave_array_write_memory0_adr] <= slave_array_write_memory0_dat_w;
	memadr_6 <= slave_array_write_memory0_adr;
end

always @(posedge milan_clk) begin
	memadr_7 <= slave_array_read_memory0_adr;
end

assign slave_array_write_memory0_dat_r = storage_3[memadr_6];
assign slave_array_read_memory0_dat_r = storage_3[memadr_7];

(* ram_style = "distributed" *) reg [1:0] storage_4[0:3];
reg [1:0] memadr_8;
reg [1:0] memadr_9;
always @(posedge sys_clk) begin
	if (slave_array_write_memory1_we)
		storage_4[slave_array_write_memory1_adr] <= slave_array_write_memory1_dat_w;
	memadr_8 <= slave_array_write_memory1_adr;
end

always @(posedge milan_clk) begin
	memadr_9 <= slave_array_read_memory1_adr;
end

assign slave_array_write_memory1_dat_r = storage_4[memadr_8];
assign slave_array_read_memory1_dat_r = storage_4[memadr_9];

(* ram_style = "block" *) reg [33:0] storage_5[0:3];
reg [1:0] memadr_10;
reg [1:0] memadr_11;
always @(posedge milan_clk) begin
	if (slave_array_write_memory2_we)
		storage_5[slave_array_write_memory2_adr] <= slave_array_write_memory2_dat_w;
	memadr_10 <= slave_array_write_memory2_adr;
end

always @(posedge sys_clk) begin
	memadr_11 <= slave_array_read_memory2_adr;
end

assign slave_array_write_memory2_dat_r = storage_5[memadr_10];
assign slave_array_read_memory2_dat_r = storage_5[memadr_11];

(* ram_style = "distributed" *) reg [1:0] storage_6[0:3];
reg [1:0] memadr_12;
reg [1:0] memadr_13;
always @(posedge milan_clk) begin
	if (slave_array_write_memory3_we)
		storage_6[slave_array_write_memory3_adr] <= slave_array_write_memory3_dat_w;
	memadr_12 <= slave_array_write_memory3_adr;
end

always @(posedge sys_clk) begin
	memadr_13 <= slave_array_read_memory3_adr;
end

assign slave_array_write_memory3_dat_r = storage_6[memadr_12];
assign slave_array_read_memory3_dat_r = storage_6[memadr_13];

endmodule


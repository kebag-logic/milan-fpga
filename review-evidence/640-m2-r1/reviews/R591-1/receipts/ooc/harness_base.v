/* Machine-generated using Migen */
module r591_crossings(
	input sys_clk,
	input sys_rst,
	input milan_clk,
	input milan_rst,
	input macsys_clk,
	input macsys_rst,
	input macdp_clk,
	input macdp_rst,
	input sink_valid,
	output sink_ready,
	input sink_first,
	input sink_last,
	input [63:0] sink_payload_data,
	input [7:0] sink_payload_keep,
	output source_valid,
	input source_ready,
	output source_first,
	output source_last,
	output [63:0] source_payload_data,
	output [7:0] source_payload_keep,
	input sink_valid_1,
	output sink_ready_1,
	input sink_first_1,
	input sink_last_1,
	input [63:0] sink_payload_data_1,
	input [7:0] sink_payload_keep_1,
	output source_valid_1,
	input source_ready_1,
	output source_first_1,
	output source_last_1,
	output [63:0] source_payload_data_1,
	output [7:0] source_payload_keep_1,
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

wire tx_cdc_sink_valid;
wire tx_cdc_sink_ready;
wire tx_cdc_sink_first;
wire tx_cdc_sink_last;
wire [63:0] tx_cdc_sink_payload_data;
wire [7:0] tx_cdc_sink_payload_keep;
wire tx_cdc_source_valid;
wire tx_cdc_source_ready;
wire tx_cdc_source_first;
wire tx_cdc_source_last;
wire [63:0] tx_cdc_source_payload_data;
wire [7:0] tx_cdc_source_payload_keep;
wire tx_cdc_re;
reg tx_cdc_readable = 1'd0;
reg [73:0] tx_cdc_dout = 74'd0;
wire tx_cdc_asyncfifo_we;
wire tx_cdc_asyncfifo_writable;
wire tx_cdc_asyncfifo_re;
wire tx_cdc_asyncfifo_readable;
wire [73:0] tx_cdc_asyncfifo_din;
wire [73:0] tx_cdc_asyncfifo_dout;
wire tx_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [4:0] tx_cdc_graycounter0_q = 5'd0;
wire [4:0] tx_cdc_graycounter0_q_next;
reg [4:0] tx_cdc_graycounter0_q_binary = 5'd0;
reg [4:0] tx_cdc_graycounter0_q_next_binary;
wire tx_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [4:0] tx_cdc_graycounter1_q = 5'd0;
wire [4:0] tx_cdc_graycounter1_q_next;
reg [4:0] tx_cdc_graycounter1_q_binary = 5'd0;
reg [4:0] tx_cdc_graycounter1_q_next_binary;
wire [4:0] tx_cdc_produce_rdomain;
wire [4:0] tx_cdc_consume_wdomain;
wire [3:0] tx_cdc_wrport_adr;
wire [73:0] tx_cdc_wrport_dat_r;
wire tx_cdc_wrport_we;
wire [73:0] tx_cdc_wrport_dat_w;
wire [3:0] tx_cdc_rdport_adr;
wire [73:0] tx_cdc_rdport_dat_r;
wire [63:0] tx_cdc_fifo_in_payload_data;
wire [7:0] tx_cdc_fifo_in_payload_keep;
wire tx_cdc_fifo_in_first;
wire tx_cdc_fifo_in_last;
wire [63:0] tx_cdc_fifo_out_payload_data;
wire [7:0] tx_cdc_fifo_out_payload_keep;
wire tx_cdc_fifo_out_first;
wire tx_cdc_fifo_out_last;
wire rx_cdc_sink_valid;
wire rx_cdc_sink_ready;
wire rx_cdc_sink_first;
wire rx_cdc_sink_last;
wire [63:0] rx_cdc_sink_payload_data;
wire [7:0] rx_cdc_sink_payload_keep;
wire rx_cdc_source_valid;
wire rx_cdc_source_ready;
wire rx_cdc_source_first;
wire rx_cdc_source_last;
wire [63:0] rx_cdc_source_payload_data;
wire [7:0] rx_cdc_source_payload_keep;
wire rx_cdc_re;
reg rx_cdc_readable = 1'd0;
reg [73:0] rx_cdc_dout = 74'd0;
wire rx_cdc_asyncfifo_we;
wire rx_cdc_asyncfifo_writable;
wire rx_cdc_asyncfifo_re;
wire rx_cdc_asyncfifo_readable;
wire [73:0] rx_cdc_asyncfifo_din;
wire [73:0] rx_cdc_asyncfifo_dout;
wire rx_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [4:0] rx_cdc_graycounter0_q = 5'd0;
wire [4:0] rx_cdc_graycounter0_q_next;
reg [4:0] rx_cdc_graycounter0_q_binary = 5'd0;
reg [4:0] rx_cdc_graycounter0_q_next_binary;
wire rx_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [4:0] rx_cdc_graycounter1_q = 5'd0;
wire [4:0] rx_cdc_graycounter1_q_next;
reg [4:0] rx_cdc_graycounter1_q_binary = 5'd0;
reg [4:0] rx_cdc_graycounter1_q_next_binary;
wire [4:0] rx_cdc_produce_rdomain;
wire [4:0] rx_cdc_consume_wdomain;
wire [3:0] rx_cdc_wrport_adr;
wire [73:0] rx_cdc_wrport_dat_r;
wire rx_cdc_wrport_we;
wire [73:0] rx_cdc_wrport_dat_w;
wire [3:0] rx_cdc_rdport_adr;
wire [73:0] rx_cdc_rdport_dat_r;
wire [63:0] rx_cdc_fifo_in_payload_data;
wire [7:0] rx_cdc_fifo_in_payload_keep;
wire rx_cdc_fifo_in_first;
wire rx_cdc_fifo_in_last;
wire [63:0] rx_cdc_fifo_out_payload_data;
wire [7:0] rx_cdc_fifo_out_payload_keep;
wire rx_cdc_fifo_out_first;
wire rx_cdc_fifo_out_last;
wire aw_cdc_sink_sink_valid;
wire aw_cdc_sink_sink_ready;
wire aw_cdc_sink_sink_first;
wire aw_cdc_sink_sink_last;
wire [31:0] aw_cdc_sink_sink_payload_addr;
wire [2:0] aw_cdc_sink_sink_payload_prot;
wire aw_cdc_source_source_valid;
wire aw_cdc_source_source_ready;
wire aw_cdc_source_source_first;
wire aw_cdc_source_source_last;
wire [31:0] aw_cdc_source_source_payload_addr;
wire [2:0] aw_cdc_source_source_payload_prot;
wire aw_cdc_cdc_sink_valid;
wire aw_cdc_cdc_sink_ready;
wire aw_cdc_cdc_sink_first;
wire aw_cdc_cdc_sink_last;
wire [31:0] aw_cdc_cdc_sink_payload_addr;
wire [2:0] aw_cdc_cdc_sink_payload_prot;
wire aw_cdc_cdc_source_valid;
wire aw_cdc_cdc_source_ready;
wire aw_cdc_cdc_source_first;
wire aw_cdc_cdc_source_last;
wire [31:0] aw_cdc_cdc_source_payload_addr;
wire [2:0] aw_cdc_cdc_source_payload_prot;
wire aw_cdc_cdc_asyncfifo_we;
wire aw_cdc_cdc_asyncfifo_writable;
wire aw_cdc_cdc_asyncfifo_re;
wire aw_cdc_cdc_asyncfifo_readable;
wire [36:0] aw_cdc_cdc_asyncfifo_din;
wire [36:0] aw_cdc_cdc_asyncfifo_dout;
wire aw_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] aw_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] aw_cdc_cdc_graycounter0_q_next;
reg [2:0] aw_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] aw_cdc_cdc_graycounter0_q_next_binary;
wire aw_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] aw_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] aw_cdc_cdc_graycounter1_q_next;
reg [2:0] aw_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] aw_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] aw_cdc_cdc_produce_rdomain;
wire [2:0] aw_cdc_cdc_consume_wdomain;
wire [1:0] aw_cdc_cdc_wrport_adr;
wire [36:0] aw_cdc_cdc_wrport_dat_r;
wire aw_cdc_cdc_wrport_we;
wire [36:0] aw_cdc_cdc_wrport_dat_w;
wire [1:0] aw_cdc_cdc_rdport_adr;
wire [36:0] aw_cdc_cdc_rdport_dat_r;
wire [31:0] aw_cdc_cdc_fifo_in_payload_addr;
wire [2:0] aw_cdc_cdc_fifo_in_payload_prot;
wire aw_cdc_cdc_fifo_in_first;
wire aw_cdc_cdc_fifo_in_last;
wire [31:0] aw_cdc_cdc_fifo_out_payload_addr;
wire [2:0] aw_cdc_cdc_fifo_out_payload_prot;
wire aw_cdc_cdc_fifo_out_first;
wire aw_cdc_cdc_fifo_out_last;
wire w_cdc_sink_sink_valid;
wire w_cdc_sink_sink_ready;
wire w_cdc_sink_sink_first;
wire w_cdc_sink_sink_last;
wire [31:0] w_cdc_sink_sink_payload_data;
wire [3:0] w_cdc_sink_sink_payload_strb;
wire w_cdc_source_source_valid;
wire w_cdc_source_source_ready;
wire w_cdc_source_source_first;
wire w_cdc_source_source_last;
wire [31:0] w_cdc_source_source_payload_data;
wire [3:0] w_cdc_source_source_payload_strb;
wire w_cdc_cdc_sink_valid;
wire w_cdc_cdc_sink_ready;
wire w_cdc_cdc_sink_first;
wire w_cdc_cdc_sink_last;
wire [31:0] w_cdc_cdc_sink_payload_data;
wire [3:0] w_cdc_cdc_sink_payload_strb;
wire w_cdc_cdc_source_valid;
wire w_cdc_cdc_source_ready;
wire w_cdc_cdc_source_first;
wire w_cdc_cdc_source_last;
wire [31:0] w_cdc_cdc_source_payload_data;
wire [3:0] w_cdc_cdc_source_payload_strb;
wire w_cdc_cdc_asyncfifo_we;
wire w_cdc_cdc_asyncfifo_writable;
wire w_cdc_cdc_asyncfifo_re;
wire w_cdc_cdc_asyncfifo_readable;
wire [37:0] w_cdc_cdc_asyncfifo_din;
wire [37:0] w_cdc_cdc_asyncfifo_dout;
wire w_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] w_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] w_cdc_cdc_graycounter0_q_next;
reg [2:0] w_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] w_cdc_cdc_graycounter0_q_next_binary;
wire w_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] w_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] w_cdc_cdc_graycounter1_q_next;
reg [2:0] w_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] w_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] w_cdc_cdc_produce_rdomain;
wire [2:0] w_cdc_cdc_consume_wdomain;
wire [1:0] w_cdc_cdc_wrport_adr;
wire [37:0] w_cdc_cdc_wrport_dat_r;
wire w_cdc_cdc_wrport_we;
wire [37:0] w_cdc_cdc_wrport_dat_w;
wire [1:0] w_cdc_cdc_rdport_adr;
wire [37:0] w_cdc_cdc_rdport_dat_r;
wire [31:0] w_cdc_cdc_fifo_in_payload_data;
wire [3:0] w_cdc_cdc_fifo_in_payload_strb;
wire w_cdc_cdc_fifo_in_first;
wire w_cdc_cdc_fifo_in_last;
wire [31:0] w_cdc_cdc_fifo_out_payload_data;
wire [3:0] w_cdc_cdc_fifo_out_payload_strb;
wire w_cdc_cdc_fifo_out_first;
wire w_cdc_cdc_fifo_out_last;
wire b_cdc_sink_sink_valid;
wire b_cdc_sink_sink_ready;
wire b_cdc_sink_sink_first;
wire b_cdc_sink_sink_last;
wire [1:0] b_cdc_sink_sink_payload_resp;
wire b_cdc_source_source_valid;
wire b_cdc_source_source_ready;
wire b_cdc_source_source_first;
wire b_cdc_source_source_last;
wire [1:0] b_cdc_source_source_payload_resp;
wire b_cdc_cdc_sink_valid;
wire b_cdc_cdc_sink_ready;
wire b_cdc_cdc_sink_first;
wire b_cdc_cdc_sink_last;
wire [1:0] b_cdc_cdc_sink_payload_resp;
wire b_cdc_cdc_source_valid;
wire b_cdc_cdc_source_ready;
wire b_cdc_cdc_source_first;
wire b_cdc_cdc_source_last;
wire [1:0] b_cdc_cdc_source_payload_resp;
wire b_cdc_cdc_asyncfifo_we;
wire b_cdc_cdc_asyncfifo_writable;
wire b_cdc_cdc_asyncfifo_re;
wire b_cdc_cdc_asyncfifo_readable;
wire [3:0] b_cdc_cdc_asyncfifo_din;
wire [3:0] b_cdc_cdc_asyncfifo_dout;
wire b_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] b_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] b_cdc_cdc_graycounter0_q_next;
reg [2:0] b_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] b_cdc_cdc_graycounter0_q_next_binary;
wire b_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] b_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] b_cdc_cdc_graycounter1_q_next;
reg [2:0] b_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] b_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] b_cdc_cdc_produce_rdomain;
wire [2:0] b_cdc_cdc_consume_wdomain;
wire [1:0] b_cdc_cdc_wrport_adr;
wire [3:0] b_cdc_cdc_wrport_dat_r;
wire b_cdc_cdc_wrport_we;
wire [3:0] b_cdc_cdc_wrport_dat_w;
wire [1:0] b_cdc_cdc_rdport_adr;
wire [3:0] b_cdc_cdc_rdport_dat_r;
wire [1:0] b_cdc_cdc_fifo_in_payload_resp;
wire b_cdc_cdc_fifo_in_first;
wire b_cdc_cdc_fifo_in_last;
wire [1:0] b_cdc_cdc_fifo_out_payload_resp;
wire b_cdc_cdc_fifo_out_first;
wire b_cdc_cdc_fifo_out_last;
wire ar_cdc_sink_sink_valid;
wire ar_cdc_sink_sink_ready;
wire ar_cdc_sink_sink_first;
wire ar_cdc_sink_sink_last;
wire [31:0] ar_cdc_sink_sink_payload_addr;
wire [2:0] ar_cdc_sink_sink_payload_prot;
wire ar_cdc_source_source_valid;
wire ar_cdc_source_source_ready;
wire ar_cdc_source_source_first;
wire ar_cdc_source_source_last;
wire [31:0] ar_cdc_source_source_payload_addr;
wire [2:0] ar_cdc_source_source_payload_prot;
wire ar_cdc_cdc_sink_valid;
wire ar_cdc_cdc_sink_ready;
wire ar_cdc_cdc_sink_first;
wire ar_cdc_cdc_sink_last;
wire [31:0] ar_cdc_cdc_sink_payload_addr;
wire [2:0] ar_cdc_cdc_sink_payload_prot;
wire ar_cdc_cdc_source_valid;
wire ar_cdc_cdc_source_ready;
wire ar_cdc_cdc_source_first;
wire ar_cdc_cdc_source_last;
wire [31:0] ar_cdc_cdc_source_payload_addr;
wire [2:0] ar_cdc_cdc_source_payload_prot;
wire ar_cdc_cdc_asyncfifo_we;
wire ar_cdc_cdc_asyncfifo_writable;
wire ar_cdc_cdc_asyncfifo_re;
wire ar_cdc_cdc_asyncfifo_readable;
wire [36:0] ar_cdc_cdc_asyncfifo_din;
wire [36:0] ar_cdc_cdc_asyncfifo_dout;
wire ar_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] ar_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] ar_cdc_cdc_graycounter0_q_next;
reg [2:0] ar_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] ar_cdc_cdc_graycounter0_q_next_binary;
wire ar_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] ar_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] ar_cdc_cdc_graycounter1_q_next;
reg [2:0] ar_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] ar_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] ar_cdc_cdc_produce_rdomain;
wire [2:0] ar_cdc_cdc_consume_wdomain;
wire [1:0] ar_cdc_cdc_wrport_adr;
wire [36:0] ar_cdc_cdc_wrport_dat_r;
wire ar_cdc_cdc_wrport_we;
wire [36:0] ar_cdc_cdc_wrport_dat_w;
wire [1:0] ar_cdc_cdc_rdport_adr;
wire [36:0] ar_cdc_cdc_rdport_dat_r;
wire [31:0] ar_cdc_cdc_fifo_in_payload_addr;
wire [2:0] ar_cdc_cdc_fifo_in_payload_prot;
wire ar_cdc_cdc_fifo_in_first;
wire ar_cdc_cdc_fifo_in_last;
wire [31:0] ar_cdc_cdc_fifo_out_payload_addr;
wire [2:0] ar_cdc_cdc_fifo_out_payload_prot;
wire ar_cdc_cdc_fifo_out_first;
wire ar_cdc_cdc_fifo_out_last;
wire r_cdc_sink_sink_valid;
wire r_cdc_sink_sink_ready;
wire r_cdc_sink_sink_first;
wire r_cdc_sink_sink_last;
wire [1:0] r_cdc_sink_sink_payload_resp;
wire [31:0] r_cdc_sink_sink_payload_data;
wire r_cdc_source_source_valid;
wire r_cdc_source_source_ready;
wire r_cdc_source_source_first;
wire r_cdc_source_source_last;
wire [1:0] r_cdc_source_source_payload_resp;
wire [31:0] r_cdc_source_source_payload_data;
wire r_cdc_cdc_sink_valid;
wire r_cdc_cdc_sink_ready;
wire r_cdc_cdc_sink_first;
wire r_cdc_cdc_sink_last;
wire [1:0] r_cdc_cdc_sink_payload_resp;
wire [31:0] r_cdc_cdc_sink_payload_data;
wire r_cdc_cdc_source_valid;
wire r_cdc_cdc_source_ready;
wire r_cdc_cdc_source_first;
wire r_cdc_cdc_source_last;
wire [1:0] r_cdc_cdc_source_payload_resp;
wire [31:0] r_cdc_cdc_source_payload_data;
wire r_cdc_cdc_asyncfifo_we;
wire r_cdc_cdc_asyncfifo_writable;
wire r_cdc_cdc_asyncfifo_re;
wire r_cdc_cdc_asyncfifo_readable;
wire [35:0] r_cdc_cdc_asyncfifo_din;
wire [35:0] r_cdc_cdc_asyncfifo_dout;
wire r_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [2:0] r_cdc_cdc_graycounter0_q = 3'd0;
wire [2:0] r_cdc_cdc_graycounter0_q_next;
reg [2:0] r_cdc_cdc_graycounter0_q_binary = 3'd0;
reg [2:0] r_cdc_cdc_graycounter0_q_next_binary;
wire r_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [2:0] r_cdc_cdc_graycounter1_q = 3'd0;
wire [2:0] r_cdc_cdc_graycounter1_q_next;
reg [2:0] r_cdc_cdc_graycounter1_q_binary = 3'd0;
reg [2:0] r_cdc_cdc_graycounter1_q_next_binary;
wire [2:0] r_cdc_cdc_produce_rdomain;
wire [2:0] r_cdc_cdc_consume_wdomain;
wire [1:0] r_cdc_cdc_wrport_adr;
wire [35:0] r_cdc_cdc_wrport_dat_r;
wire r_cdc_cdc_wrport_we;
wire [35:0] r_cdc_cdc_wrport_dat_w;
wire [1:0] r_cdc_cdc_rdport_adr;
wire [35:0] r_cdc_cdc_rdport_dat_r;
wire [1:0] r_cdc_cdc_fifo_in_payload_resp;
wire [31:0] r_cdc_cdc_fifo_in_payload_data;
wire r_cdc_cdc_fifo_in_first;
wire r_cdc_cdc_fifo_in_last;
wire [1:0] r_cdc_cdc_fifo_out_payload_resp;
wire [31:0] r_cdc_cdc_fifo_out_payload_data;
wire r_cdc_cdc_fifo_out_first;
wire r_cdc_cdc_fifo_out_last;
(* no_retiming = "true" *) reg [4:0] multiregimpl00 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl01 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl10 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl11 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl20 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl21 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl30 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl31 = 5'd0;
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
(* no_retiming = "true" *) reg [2:0] multiregimpl100 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl101 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl110 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl111 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl120 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl121 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl130 = 3'd0;
(* no_retiming = "true" *) reg [2:0] multiregimpl131 = 3'd0;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign tx_cdc_sink_valid = sink_valid;
assign sink_ready = tx_cdc_sink_ready;
assign tx_cdc_sink_first = sink_first;
assign tx_cdc_sink_last = sink_last;
assign tx_cdc_sink_payload_data = sink_payload_data;
assign tx_cdc_sink_payload_keep = sink_payload_keep;
assign source_valid = tx_cdc_source_valid;
assign tx_cdc_source_ready = source_ready;
assign source_first = tx_cdc_source_first;
assign source_last = tx_cdc_source_last;
assign source_payload_data = tx_cdc_source_payload_data;
assign source_payload_keep = tx_cdc_source_payload_keep;
assign tx_cdc_asyncfifo_din = {tx_cdc_fifo_in_last, tx_cdc_fifo_in_first, tx_cdc_fifo_in_payload_keep, tx_cdc_fifo_in_payload_data};
assign {tx_cdc_fifo_out_last, tx_cdc_fifo_out_first, tx_cdc_fifo_out_payload_keep, tx_cdc_fifo_out_payload_data} = tx_cdc_dout;
assign tx_cdc_sink_ready = tx_cdc_asyncfifo_writable;
assign tx_cdc_asyncfifo_we = tx_cdc_sink_valid;
assign tx_cdc_fifo_in_first = tx_cdc_sink_first;
assign tx_cdc_fifo_in_last = tx_cdc_sink_last;
assign tx_cdc_fifo_in_payload_data = tx_cdc_sink_payload_data;
assign tx_cdc_fifo_in_payload_keep = tx_cdc_sink_payload_keep;
assign tx_cdc_source_valid = tx_cdc_readable;
assign tx_cdc_source_first = tx_cdc_fifo_out_first;
assign tx_cdc_source_last = tx_cdc_fifo_out_last;
assign tx_cdc_source_payload_data = tx_cdc_fifo_out_payload_data;
assign tx_cdc_source_payload_keep = tx_cdc_fifo_out_payload_keep;
assign tx_cdc_re = tx_cdc_source_ready;
assign tx_cdc_asyncfifo_re = (tx_cdc_re | (~tx_cdc_readable));
assign tx_cdc_graycounter0_ce = (tx_cdc_asyncfifo_writable & tx_cdc_asyncfifo_we);
assign tx_cdc_graycounter1_ce = (tx_cdc_asyncfifo_readable & tx_cdc_asyncfifo_re);
assign tx_cdc_asyncfifo_writable = (((tx_cdc_graycounter0_q[4] == tx_cdc_consume_wdomain[4]) | (tx_cdc_graycounter0_q[3] == tx_cdc_consume_wdomain[3])) | (tx_cdc_graycounter0_q[2:0] != tx_cdc_consume_wdomain[2:0]));
assign tx_cdc_asyncfifo_readable = (tx_cdc_graycounter1_q != tx_cdc_produce_rdomain);
assign tx_cdc_wrport_adr = tx_cdc_graycounter0_q_binary[3:0];
assign tx_cdc_wrport_dat_w = tx_cdc_asyncfifo_din;
assign tx_cdc_wrport_we = tx_cdc_graycounter0_ce;
assign tx_cdc_rdport_adr = tx_cdc_graycounter1_q_next_binary[3:0];
assign tx_cdc_asyncfifo_dout = tx_cdc_rdport_dat_r;

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	tx_cdc_graycounter0_q_next_binary <= 5'd0;
	if (tx_cdc_graycounter0_ce) begin
		tx_cdc_graycounter0_q_next_binary <= (tx_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		tx_cdc_graycounter0_q_next_binary <= tx_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end
assign tx_cdc_graycounter0_q_next = (tx_cdc_graycounter0_q_next_binary ^ tx_cdc_graycounter0_q_next_binary[4:1]);

// synthesis translate_off
reg dummy_d_1;
// synthesis translate_on
always @(*) begin
	tx_cdc_graycounter1_q_next_binary <= 5'd0;
	if (tx_cdc_graycounter1_ce) begin
		tx_cdc_graycounter1_q_next_binary <= (tx_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		tx_cdc_graycounter1_q_next_binary <= tx_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_1 <= dummy_s;
// synthesis translate_on
end
assign tx_cdc_graycounter1_q_next = (tx_cdc_graycounter1_q_next_binary ^ tx_cdc_graycounter1_q_next_binary[4:1]);
assign rx_cdc_sink_valid = sink_valid_1;
assign sink_ready_1 = rx_cdc_sink_ready;
assign rx_cdc_sink_first = sink_first_1;
assign rx_cdc_sink_last = sink_last_1;
assign rx_cdc_sink_payload_data = sink_payload_data_1;
assign rx_cdc_sink_payload_keep = sink_payload_keep_1;
assign source_valid_1 = rx_cdc_source_valid;
assign rx_cdc_source_ready = source_ready_1;
assign source_first_1 = rx_cdc_source_first;
assign source_last_1 = rx_cdc_source_last;
assign source_payload_data_1 = rx_cdc_source_payload_data;
assign source_payload_keep_1 = rx_cdc_source_payload_keep;
assign rx_cdc_asyncfifo_din = {rx_cdc_fifo_in_last, rx_cdc_fifo_in_first, rx_cdc_fifo_in_payload_keep, rx_cdc_fifo_in_payload_data};
assign {rx_cdc_fifo_out_last, rx_cdc_fifo_out_first, rx_cdc_fifo_out_payload_keep, rx_cdc_fifo_out_payload_data} = rx_cdc_dout;
assign rx_cdc_sink_ready = rx_cdc_asyncfifo_writable;
assign rx_cdc_asyncfifo_we = rx_cdc_sink_valid;
assign rx_cdc_fifo_in_first = rx_cdc_sink_first;
assign rx_cdc_fifo_in_last = rx_cdc_sink_last;
assign rx_cdc_fifo_in_payload_data = rx_cdc_sink_payload_data;
assign rx_cdc_fifo_in_payload_keep = rx_cdc_sink_payload_keep;
assign rx_cdc_source_valid = rx_cdc_readable;
assign rx_cdc_source_first = rx_cdc_fifo_out_first;
assign rx_cdc_source_last = rx_cdc_fifo_out_last;
assign rx_cdc_source_payload_data = rx_cdc_fifo_out_payload_data;
assign rx_cdc_source_payload_keep = rx_cdc_fifo_out_payload_keep;
assign rx_cdc_re = rx_cdc_source_ready;
assign rx_cdc_asyncfifo_re = (rx_cdc_re | (~rx_cdc_readable));
assign rx_cdc_graycounter0_ce = (rx_cdc_asyncfifo_writable & rx_cdc_asyncfifo_we);
assign rx_cdc_graycounter1_ce = (rx_cdc_asyncfifo_readable & rx_cdc_asyncfifo_re);
assign rx_cdc_asyncfifo_writable = (((rx_cdc_graycounter0_q[4] == rx_cdc_consume_wdomain[4]) | (rx_cdc_graycounter0_q[3] == rx_cdc_consume_wdomain[3])) | (rx_cdc_graycounter0_q[2:0] != rx_cdc_consume_wdomain[2:0]));
assign rx_cdc_asyncfifo_readable = (rx_cdc_graycounter1_q != rx_cdc_produce_rdomain);
assign rx_cdc_wrport_adr = rx_cdc_graycounter0_q_binary[3:0];
assign rx_cdc_wrport_dat_w = rx_cdc_asyncfifo_din;
assign rx_cdc_wrport_we = rx_cdc_graycounter0_ce;
assign rx_cdc_rdport_adr = rx_cdc_graycounter1_q_next_binary[3:0];
assign rx_cdc_asyncfifo_dout = rx_cdc_rdport_dat_r;

// synthesis translate_off
reg dummy_d_2;
// synthesis translate_on
always @(*) begin
	rx_cdc_graycounter0_q_next_binary <= 5'd0;
	if (rx_cdc_graycounter0_ce) begin
		rx_cdc_graycounter0_q_next_binary <= (rx_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		rx_cdc_graycounter0_q_next_binary <= rx_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_2 <= dummy_s;
// synthesis translate_on
end
assign rx_cdc_graycounter0_q_next = (rx_cdc_graycounter0_q_next_binary ^ rx_cdc_graycounter0_q_next_binary[4:1]);

// synthesis translate_off
reg dummy_d_3;
// synthesis translate_on
always @(*) begin
	rx_cdc_graycounter1_q_next_binary <= 5'd0;
	if (rx_cdc_graycounter1_ce) begin
		rx_cdc_graycounter1_q_next_binary <= (rx_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		rx_cdc_graycounter1_q_next_binary <= rx_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_3 <= dummy_s;
// synthesis translate_on
end
assign rx_cdc_graycounter1_q_next = (rx_cdc_graycounter1_q_next_binary ^ rx_cdc_graycounter1_q_next_binary[4:1]);
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
assign r_cdc_sink_sink_first = r_first_1;
assign r_cdc_sink_sink_last = r_last_1;
assign r_cdc_sink_sink_payload_resp = r_payload_resp_1;
assign r_cdc_sink_sink_payload_data = r_payload_data_1;
assign r_valid = r_cdc_source_source_valid;
assign r_cdc_source_source_ready = r_ready;
assign r_first = r_cdc_source_source_first;
assign r_last = r_cdc_source_source_last;
assign r_payload_resp = r_cdc_source_source_payload_resp;
assign r_payload_data = r_cdc_source_source_payload_data;
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

// synthesis translate_off
reg dummy_d_4;
// synthesis translate_on
always @(*) begin
	aw_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (aw_cdc_cdc_graycounter0_ce) begin
		aw_cdc_cdc_graycounter0_q_next_binary <= (aw_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		aw_cdc_cdc_graycounter0_q_next_binary <= aw_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_4 <= dummy_s;
// synthesis translate_on
end
assign aw_cdc_cdc_graycounter0_q_next = (aw_cdc_cdc_graycounter0_q_next_binary ^ aw_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_5;
// synthesis translate_on
always @(*) begin
	aw_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (aw_cdc_cdc_graycounter1_ce) begin
		aw_cdc_cdc_graycounter1_q_next_binary <= (aw_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		aw_cdc_cdc_graycounter1_q_next_binary <= aw_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_5 <= dummy_s;
// synthesis translate_on
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

// synthesis translate_off
reg dummy_d_6;
// synthesis translate_on
always @(*) begin
	w_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (w_cdc_cdc_graycounter0_ce) begin
		w_cdc_cdc_graycounter0_q_next_binary <= (w_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		w_cdc_cdc_graycounter0_q_next_binary <= w_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_6 <= dummy_s;
// synthesis translate_on
end
assign w_cdc_cdc_graycounter0_q_next = (w_cdc_cdc_graycounter0_q_next_binary ^ w_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_7;
// synthesis translate_on
always @(*) begin
	w_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (w_cdc_cdc_graycounter1_ce) begin
		w_cdc_cdc_graycounter1_q_next_binary <= (w_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		w_cdc_cdc_graycounter1_q_next_binary <= w_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_7 <= dummy_s;
// synthesis translate_on
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

// synthesis translate_off
reg dummy_d_8;
// synthesis translate_on
always @(*) begin
	b_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (b_cdc_cdc_graycounter0_ce) begin
		b_cdc_cdc_graycounter0_q_next_binary <= (b_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		b_cdc_cdc_graycounter0_q_next_binary <= b_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_8 <= dummy_s;
// synthesis translate_on
end
assign b_cdc_cdc_graycounter0_q_next = (b_cdc_cdc_graycounter0_q_next_binary ^ b_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_9;
// synthesis translate_on
always @(*) begin
	b_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (b_cdc_cdc_graycounter1_ce) begin
		b_cdc_cdc_graycounter1_q_next_binary <= (b_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		b_cdc_cdc_graycounter1_q_next_binary <= b_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_9 <= dummy_s;
// synthesis translate_on
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

// synthesis translate_off
reg dummy_d_10;
// synthesis translate_on
always @(*) begin
	ar_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (ar_cdc_cdc_graycounter0_ce) begin
		ar_cdc_cdc_graycounter0_q_next_binary <= (ar_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		ar_cdc_cdc_graycounter0_q_next_binary <= ar_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_10 <= dummy_s;
// synthesis translate_on
end
assign ar_cdc_cdc_graycounter0_q_next = (ar_cdc_cdc_graycounter0_q_next_binary ^ ar_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_11;
// synthesis translate_on
always @(*) begin
	ar_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (ar_cdc_cdc_graycounter1_ce) begin
		ar_cdc_cdc_graycounter1_q_next_binary <= (ar_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		ar_cdc_cdc_graycounter1_q_next_binary <= ar_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_11 <= dummy_s;
// synthesis translate_on
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

// synthesis translate_off
reg dummy_d_12;
// synthesis translate_on
always @(*) begin
	r_cdc_cdc_graycounter0_q_next_binary <= 3'd0;
	if (r_cdc_cdc_graycounter0_ce) begin
		r_cdc_cdc_graycounter0_q_next_binary <= (r_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		r_cdc_cdc_graycounter0_q_next_binary <= r_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_12 <= dummy_s;
// synthesis translate_on
end
assign r_cdc_cdc_graycounter0_q_next = (r_cdc_cdc_graycounter0_q_next_binary ^ r_cdc_cdc_graycounter0_q_next_binary[2:1]);

// synthesis translate_off
reg dummy_d_13;
// synthesis translate_on
always @(*) begin
	r_cdc_cdc_graycounter1_q_next_binary <= 3'd0;
	if (r_cdc_cdc_graycounter1_ce) begin
		r_cdc_cdc_graycounter1_q_next_binary <= (r_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		r_cdc_cdc_graycounter1_q_next_binary <= r_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_13 <= dummy_s;
// synthesis translate_on
end
assign r_cdc_cdc_graycounter1_q_next = (r_cdc_cdc_graycounter1_q_next_binary ^ r_cdc_cdc_graycounter1_q_next_binary[2:1]);
assign tx_cdc_produce_rdomain = multiregimpl01;
assign tx_cdc_consume_wdomain = multiregimpl11;
assign rx_cdc_produce_rdomain = multiregimpl21;
assign rx_cdc_consume_wdomain = multiregimpl31;
assign aw_cdc_cdc_produce_rdomain = multiregimpl41;
assign aw_cdc_cdc_consume_wdomain = multiregimpl51;
assign w_cdc_cdc_produce_rdomain = multiregimpl61;
assign w_cdc_cdc_consume_wdomain = multiregimpl71;
assign b_cdc_cdc_produce_rdomain = multiregimpl81;
assign b_cdc_cdc_consume_wdomain = multiregimpl91;
assign ar_cdc_cdc_produce_rdomain = multiregimpl101;
assign ar_cdc_cdc_consume_wdomain = multiregimpl111;
assign r_cdc_cdc_produce_rdomain = multiregimpl121;
assign r_cdc_cdc_consume_wdomain = multiregimpl131;

always @(posedge macdp_clk) begin
	tx_cdc_graycounter0_q_binary <= tx_cdc_graycounter0_q_next_binary;
	tx_cdc_graycounter0_q <= tx_cdc_graycounter0_q_next;
	if ((rx_cdc_re | (~rx_cdc_readable))) begin
		rx_cdc_dout <= rx_cdc_asyncfifo_dout;
		rx_cdc_readable <= rx_cdc_asyncfifo_readable;
	end
	rx_cdc_graycounter1_q_binary <= rx_cdc_graycounter1_q_next_binary;
	rx_cdc_graycounter1_q <= rx_cdc_graycounter1_q_next;
	if (macdp_rst) begin
		tx_cdc_graycounter0_q <= 5'd0;
		tx_cdc_graycounter0_q_binary <= 5'd0;
		rx_cdc_readable <= 1'd0;
		rx_cdc_graycounter1_q <= 5'd0;
		rx_cdc_graycounter1_q_binary <= 5'd0;
	end
	multiregimpl10 <= tx_cdc_graycounter1_q;
	multiregimpl11 <= multiregimpl10;
	multiregimpl20 <= rx_cdc_graycounter0_q;
	multiregimpl21 <= multiregimpl20;
end

always @(posedge macsys_clk) begin
	if ((tx_cdc_re | (~tx_cdc_readable))) begin
		tx_cdc_dout <= tx_cdc_asyncfifo_dout;
		tx_cdc_readable <= tx_cdc_asyncfifo_readable;
	end
	tx_cdc_graycounter1_q_binary <= tx_cdc_graycounter1_q_next_binary;
	tx_cdc_graycounter1_q <= tx_cdc_graycounter1_q_next;
	rx_cdc_graycounter0_q_binary <= rx_cdc_graycounter0_q_next_binary;
	rx_cdc_graycounter0_q <= rx_cdc_graycounter0_q_next;
	if (macsys_rst) begin
		tx_cdc_readable <= 1'd0;
		tx_cdc_graycounter1_q <= 5'd0;
		tx_cdc_graycounter1_q_binary <= 5'd0;
		rx_cdc_graycounter0_q <= 5'd0;
		rx_cdc_graycounter0_q_binary <= 5'd0;
	end
	multiregimpl00 <= tx_cdc_graycounter0_q;
	multiregimpl01 <= multiregimpl00;
	multiregimpl30 <= rx_cdc_graycounter1_q;
	multiregimpl31 <= multiregimpl30;
end

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
	multiregimpl40 <= aw_cdc_cdc_graycounter0_q;
	multiregimpl41 <= multiregimpl40;
	multiregimpl60 <= w_cdc_cdc_graycounter0_q;
	multiregimpl61 <= multiregimpl60;
	multiregimpl90 <= b_cdc_cdc_graycounter1_q;
	multiregimpl91 <= multiregimpl90;
	multiregimpl100 <= ar_cdc_cdc_graycounter0_q;
	multiregimpl101 <= multiregimpl100;
	multiregimpl130 <= r_cdc_cdc_graycounter1_q;
	multiregimpl131 <= multiregimpl130;
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
	multiregimpl50 <= aw_cdc_cdc_graycounter1_q;
	multiregimpl51 <= multiregimpl50;
	multiregimpl70 <= w_cdc_cdc_graycounter1_q;
	multiregimpl71 <= multiregimpl70;
	multiregimpl80 <= b_cdc_cdc_graycounter0_q;
	multiregimpl81 <= multiregimpl80;
	multiregimpl110 <= ar_cdc_cdc_graycounter1_q;
	multiregimpl111 <= multiregimpl110;
	multiregimpl120 <= r_cdc_cdc_graycounter0_q;
	multiregimpl121 <= multiregimpl120;
end

reg [73:0] storage[0:15];
reg [3:0] memadr;
reg [3:0] memadr_1;
always @(posedge macdp_clk) begin
	if (tx_cdc_wrport_we)
		storage[tx_cdc_wrport_adr] <= tx_cdc_wrport_dat_w;
	memadr <= tx_cdc_wrport_adr;
end

always @(posedge macsys_clk) begin
	memadr_1 <= tx_cdc_rdport_adr;
end

assign tx_cdc_wrport_dat_r = storage[memadr];
assign tx_cdc_rdport_dat_r = storage[memadr_1];

reg [73:0] storage_1[0:15];
reg [3:0] memadr_2;
reg [3:0] memadr_3;
always @(posedge macsys_clk) begin
	if (rx_cdc_wrport_we)
		storage_1[rx_cdc_wrport_adr] <= rx_cdc_wrport_dat_w;
	memadr_2 <= rx_cdc_wrport_adr;
end

always @(posedge macdp_clk) begin
	memadr_3 <= rx_cdc_rdport_adr;
end

assign rx_cdc_wrport_dat_r = storage_1[memadr_2];
assign rx_cdc_rdport_dat_r = storage_1[memadr_3];

reg [36:0] storage_2[0:3];
reg [1:0] memadr_4;
reg [1:0] memadr_5;
always @(posedge sys_clk) begin
	if (aw_cdc_cdc_wrport_we)
		storage_2[aw_cdc_cdc_wrport_adr] <= aw_cdc_cdc_wrport_dat_w;
	memadr_4 <= aw_cdc_cdc_wrport_adr;
end

always @(posedge milan_clk) begin
	memadr_5 <= aw_cdc_cdc_rdport_adr;
end

assign aw_cdc_cdc_wrport_dat_r = storage_2[memadr_4];
assign aw_cdc_cdc_rdport_dat_r = storage_2[memadr_5];

reg [37:0] storage_3[0:3];
reg [1:0] memadr_6;
reg [1:0] memadr_7;
always @(posedge sys_clk) begin
	if (w_cdc_cdc_wrport_we)
		storage_3[w_cdc_cdc_wrport_adr] <= w_cdc_cdc_wrport_dat_w;
	memadr_6 <= w_cdc_cdc_wrport_adr;
end

always @(posedge milan_clk) begin
	memadr_7 <= w_cdc_cdc_rdport_adr;
end

assign w_cdc_cdc_wrport_dat_r = storage_3[memadr_6];
assign w_cdc_cdc_rdport_dat_r = storage_3[memadr_7];

reg [3:0] storage_4[0:3];
reg [1:0] memadr_8;
reg [1:0] memadr_9;
always @(posedge milan_clk) begin
	if (b_cdc_cdc_wrport_we)
		storage_4[b_cdc_cdc_wrport_adr] <= b_cdc_cdc_wrport_dat_w;
	memadr_8 <= b_cdc_cdc_wrport_adr;
end

always @(posedge sys_clk) begin
	memadr_9 <= b_cdc_cdc_rdport_adr;
end

assign b_cdc_cdc_wrport_dat_r = storage_4[memadr_8];
assign b_cdc_cdc_rdport_dat_r = storage_4[memadr_9];

reg [36:0] storage_5[0:3];
reg [1:0] memadr_10;
reg [1:0] memadr_11;
always @(posedge sys_clk) begin
	if (ar_cdc_cdc_wrport_we)
		storage_5[ar_cdc_cdc_wrport_adr] <= ar_cdc_cdc_wrport_dat_w;
	memadr_10 <= ar_cdc_cdc_wrport_adr;
end

always @(posedge milan_clk) begin
	memadr_11 <= ar_cdc_cdc_rdport_adr;
end

assign ar_cdc_cdc_wrport_dat_r = storage_5[memadr_10];
assign ar_cdc_cdc_rdport_dat_r = storage_5[memadr_11];

reg [35:0] storage_6[0:3];
reg [1:0] memadr_12;
reg [1:0] memadr_13;
always @(posedge milan_clk) begin
	if (r_cdc_cdc_wrport_we)
		storage_6[r_cdc_cdc_wrport_adr] <= r_cdc_cdc_wrport_dat_w;
	memadr_12 <= r_cdc_cdc_wrport_adr;
end

always @(posedge sys_clk) begin
	memadr_13 <= r_cdc_cdc_rdport_adr;
end

assign r_cdc_cdc_wrport_dat_r = storage_6[memadr_12];
assign r_cdc_cdc_rdport_dat_r = storage_6[memadr_13];

endmodule


/* Machine-generated using Migen */
module mac_tx_chain(
	input sys_clk,
	input sys_rst,
	input dp_clk,
	input dp_rst,
	input eth_tx_clk,
	input eth_rx_clk,
	input eth_phy_rst,
	input reinit,
	input eth_rst,
	input loopback,
	input [63:0] dp_tdata,
	input [7:0] dp_tkeep,
	input dp_tvalid,
	input dp_tlast,
	output dp_tready,
	output gmii_tx_en,
	output [7:0] gmii_tx_data,
	output gmii_tx_er,
	output phy_sink_valid,
	output phy_sink_ready,
	output [7:0] phy_sink_data,
	output phy_sink_last,
	output maceth_tx_rst
);

wire eth_tx_clk_1;
reg eth_tx_rst = 1'd0;
wire eth_rx_clk_1;
reg eth_rx_rst = 1'd0;
wire macsys_clk;
reg macsys_rst = 1'd0;
wire macdp_clk;
reg macdp_rst = 1'd0;
wire maceth_tx_clk;
reg maceth_tx_rst_1 = 1'd0;
wire maceth_rx_clk;
reg maceth_rx_rst = 1'd0;
reg pads_tx_en = 1'd0;
reg [7:0] pads_tx_data = 8'd0;
reg pads_tx_er = 1'd0;
reg pads_rx_dv = 1'd0;
reg [7:0] pads_rx_data = 8'd0;
wire phy_sink_valid1;
reg phy_sink_ready1 = 1'd0;
wire phy_sink_first;
wire phy_sink_last1;
wire [7:0] phy_sink_payload_data;
wire phy_sink_payload_last_be;
wire phy_sink_payload_error;
reg phy_source_valid = 1'd0;
wire phy_source_ready;
reg phy_source_first = 1'd0;
wire phy_source_last;
reg [7:0] phy_source_payload_data = 8'd0;
reg phy_source_payload_last_be = 1'd0;
reg phy_source_payload_error = 1'd0;
reg phy_dv_d = 1'd0;
wire liteethmaccore_sink_valid;
wire liteethmaccore_sink_ready;
wire liteethmaccore_sink_first;
wire liteethmaccore_sink_last;
wire [63:0] liteethmaccore_sink_payload_data;
wire [7:0] liteethmaccore_sink_payload_last_be;
wire [7:0] liteethmaccore_sink_payload_error;
wire liteethmaccore_source_valid;
reg liteethmaccore_source_ready;
wire liteethmaccore_source_first;
wire liteethmaccore_source_last;
wire [63:0] liteethmaccore_source_payload_data;
wire [7:0] liteethmaccore_source_payload_last_be;
wire [7:0] liteethmaccore_source_payload_error;
wire liteethmaccore_tx_cdc_sink_sink_valid;
wire liteethmaccore_tx_cdc_sink_sink_ready;
wire liteethmaccore_tx_cdc_sink_sink_first;
wire liteethmaccore_tx_cdc_sink_sink_last;
wire [63:0] liteethmaccore_tx_cdc_sink_sink_payload_data;
wire [7:0] liteethmaccore_tx_cdc_sink_sink_payload_last_be;
wire [7:0] liteethmaccore_tx_cdc_sink_sink_payload_error;
wire liteethmaccore_tx_cdc_source_source_valid;
wire liteethmaccore_tx_cdc_source_source_ready;
wire liteethmaccore_tx_cdc_source_source_first;
wire liteethmaccore_tx_cdc_source_source_last;
wire [63:0] liteethmaccore_tx_cdc_source_source_payload_data;
wire [7:0] liteethmaccore_tx_cdc_source_source_payload_last_be;
wire [7:0] liteethmaccore_tx_cdc_source_source_payload_error;
wire liteethmaccore_tx_cdc_cdc_sink_valid;
wire liteethmaccore_tx_cdc_cdc_sink_ready;
wire liteethmaccore_tx_cdc_cdc_sink_first;
wire liteethmaccore_tx_cdc_cdc_sink_last;
wire [63:0] liteethmaccore_tx_cdc_cdc_sink_payload_data;
wire [7:0] liteethmaccore_tx_cdc_cdc_sink_payload_last_be;
wire [7:0] liteethmaccore_tx_cdc_cdc_sink_payload_error;
wire liteethmaccore_tx_cdc_cdc_source_valid;
wire liteethmaccore_tx_cdc_cdc_source_ready;
wire liteethmaccore_tx_cdc_cdc_source_first;
wire liteethmaccore_tx_cdc_cdc_source_last;
wire [63:0] liteethmaccore_tx_cdc_cdc_source_payload_data;
wire [7:0] liteethmaccore_tx_cdc_cdc_source_payload_last_be;
wire [7:0] liteethmaccore_tx_cdc_cdc_source_payload_error;
wire liteethmaccore_tx_cdc_cdc_asyncfifo_we;
wire liteethmaccore_tx_cdc_cdc_asyncfifo_writable;
wire liteethmaccore_tx_cdc_cdc_asyncfifo_re;
wire liteethmaccore_tx_cdc_cdc_asyncfifo_readable;
wire [81:0] liteethmaccore_tx_cdc_cdc_asyncfifo_din;
wire [81:0] liteethmaccore_tx_cdc_cdc_asyncfifo_dout;
wire liteethmaccore_tx_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [5:0] liteethmaccore_tx_cdc_cdc_graycounter0_q = 6'd0;
wire [5:0] liteethmaccore_tx_cdc_cdc_graycounter0_q_next;
reg [5:0] liteethmaccore_tx_cdc_cdc_graycounter0_q_binary = 6'd0;
reg [5:0] liteethmaccore_tx_cdc_cdc_graycounter0_q_next_binary;
wire liteethmaccore_tx_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [5:0] liteethmaccore_tx_cdc_cdc_graycounter1_q = 6'd0;
wire [5:0] liteethmaccore_tx_cdc_cdc_graycounter1_q_next;
reg [5:0] liteethmaccore_tx_cdc_cdc_graycounter1_q_binary = 6'd0;
reg [5:0] liteethmaccore_tx_cdc_cdc_graycounter1_q_next_binary;
wire [5:0] liteethmaccore_tx_cdc_cdc_produce_rdomain;
wire [5:0] liteethmaccore_tx_cdc_cdc_consume_wdomain;
wire [4:0] liteethmaccore_tx_cdc_cdc_wrport_adr;
wire [81:0] liteethmaccore_tx_cdc_cdc_wrport_dat_r;
wire liteethmaccore_tx_cdc_cdc_wrport_we;
wire [81:0] liteethmaccore_tx_cdc_cdc_wrport_dat_w;
wire [4:0] liteethmaccore_tx_cdc_cdc_rdport_adr;
wire [81:0] liteethmaccore_tx_cdc_cdc_rdport_dat_r;
wire [63:0] liteethmaccore_tx_cdc_cdc_fifo_in_payload_data;
wire [7:0] liteethmaccore_tx_cdc_cdc_fifo_in_payload_last_be;
wire [7:0] liteethmaccore_tx_cdc_cdc_fifo_in_payload_error;
wire liteethmaccore_tx_cdc_cdc_fifo_in_first;
wire liteethmaccore_tx_cdc_cdc_fifo_in_last;
wire [63:0] liteethmaccore_tx_cdc_cdc_fifo_out_payload_data;
wire [7:0] liteethmaccore_tx_cdc_cdc_fifo_out_payload_last_be;
wire [7:0] liteethmaccore_tx_cdc_cdc_fifo_out_payload_error;
wire liteethmaccore_tx_cdc_cdc_fifo_out_first;
wire liteethmaccore_tx_cdc_cdc_fifo_out_last;
wire liteethmaccore_tx_converter_sink_valid;
wire liteethmaccore_tx_converter_sink_ready;
wire liteethmaccore_tx_converter_sink_first;
wire liteethmaccore_tx_converter_sink_last;
wire [63:0] liteethmaccore_tx_converter_sink_payload_data;
wire [7:0] liteethmaccore_tx_converter_sink_payload_last_be;
wire [7:0] liteethmaccore_tx_converter_sink_payload_error;
wire liteethmaccore_tx_converter_source_valid;
wire liteethmaccore_tx_converter_source_ready;
wire liteethmaccore_tx_converter_source_first;
wire liteethmaccore_tx_converter_source_last;
wire [7:0] liteethmaccore_tx_converter_source_payload_data;
wire liteethmaccore_tx_converter_source_payload_last_be;
wire liteethmaccore_tx_converter_source_payload_error;
wire liteethmaccore_tx_converter_converter_sink_valid;
wire liteethmaccore_tx_converter_converter_sink_ready;
wire liteethmaccore_tx_converter_converter_sink_first;
wire liteethmaccore_tx_converter_converter_sink_last;
reg [79:0] liteethmaccore_tx_converter_converter_sink_payload_data;
wire liteethmaccore_tx_converter_converter_source_valid;
wire liteethmaccore_tx_converter_converter_source_ready;
wire liteethmaccore_tx_converter_converter_source_first;
wire liteethmaccore_tx_converter_converter_source_last;
reg [9:0] liteethmaccore_tx_converter_converter_source_payload_data;
wire liteethmaccore_tx_converter_converter_source_payload_valid_token_count;
reg [2:0] liteethmaccore_tx_converter_converter_mux = 3'd0;
wire liteethmaccore_tx_converter_converter_first;
wire liteethmaccore_tx_converter_converter_last;
wire liteethmaccore_tx_converter_source_source_valid;
wire liteethmaccore_tx_converter_source_source_ready;
wire liteethmaccore_tx_converter_source_source_first;
wire liteethmaccore_tx_converter_source_source_last;
wire [9:0] liteethmaccore_tx_converter_source_source_payload_data;
reg liteethmaccore_tx_converter_last_be_drop = 1'd0;
wire liteethmaccore_tx_converter_last_be_packet_end;
wire liteethmaccore_tx_last_be_sink_sink_valid;
wire liteethmaccore_tx_last_be_sink_sink_ready;
wire liteethmaccore_tx_last_be_sink_sink_first;
wire liteethmaccore_tx_last_be_sink_sink_last;
wire [7:0] liteethmaccore_tx_last_be_sink_sink_payload_data;
wire liteethmaccore_tx_last_be_sink_sink_payload_last_be;
wire liteethmaccore_tx_last_be_sink_sink_payload_error;
wire liteethmaccore_tx_last_be_source_source_valid;
wire liteethmaccore_tx_last_be_source_source_ready;
wire liteethmaccore_tx_last_be_source_source_first;
wire liteethmaccore_tx_last_be_source_source_last;
wire [7:0] liteethmaccore_tx_last_be_source_source_payload_data;
wire liteethmaccore_tx_last_be_source_source_payload_last_be;
wire liteethmaccore_tx_last_be_source_source_payload_error;
wire liteethmaccore_tx_last_be_last_handler_sink_valid;
reg liteethmaccore_tx_last_be_last_handler_sink_ready;
wire liteethmaccore_tx_last_be_last_handler_sink_first;
wire liteethmaccore_tx_last_be_last_handler_sink_last;
wire [7:0] liteethmaccore_tx_last_be_last_handler_sink_payload_data;
wire liteethmaccore_tx_last_be_last_handler_sink_payload_last_be;
wire liteethmaccore_tx_last_be_last_handler_sink_payload_error;
reg liteethmaccore_tx_last_be_last_handler_source_valid;
wire liteethmaccore_tx_last_be_last_handler_source_ready;
reg liteethmaccore_tx_last_be_last_handler_source_first;
reg liteethmaccore_tx_last_be_last_handler_source_last;
reg [7:0] liteethmaccore_tx_last_be_last_handler_source_payload_data;
reg liteethmaccore_tx_last_be_last_handler_source_payload_last_be;
reg liteethmaccore_tx_last_be_last_handler_source_payload_error;
wire liteethmaccore_tx_padding_sink_valid;
reg liteethmaccore_tx_padding_sink_ready;
wire liteethmaccore_tx_padding_sink_first;
wire liteethmaccore_tx_padding_sink_last;
wire [7:0] liteethmaccore_tx_padding_sink_payload_data;
wire liteethmaccore_tx_padding_sink_payload_last_be;
wire liteethmaccore_tx_padding_sink_payload_error;
reg liteethmaccore_tx_padding_source_valid;
wire liteethmaccore_tx_padding_source_ready;
reg liteethmaccore_tx_padding_source_first;
reg liteethmaccore_tx_padding_source_last;
reg [7:0] liteethmaccore_tx_padding_source_payload_data;
reg liteethmaccore_tx_padding_source_payload_last_be;
reg liteethmaccore_tx_padding_source_payload_error;
reg [15:0] liteethmaccore_tx_padding_counter = 16'd0;
wire liteethmaccore_tx_padding_counter_done;
wire liteethmaccore_tx_crc_sink_valid;
reg liteethmaccore_tx_crc_sink_ready;
wire liteethmaccore_tx_crc_sink_first;
wire liteethmaccore_tx_crc_sink_last;
wire [7:0] liteethmaccore_tx_crc_sink_payload_data;
wire liteethmaccore_tx_crc_sink_payload_last_be;
wire liteethmaccore_tx_crc_sink_payload_error;
reg liteethmaccore_tx_crc_source_valid;
wire liteethmaccore_tx_crc_source_ready;
reg liteethmaccore_tx_crc_source_first;
reg liteethmaccore_tx_crc_source_last;
reg [7:0] liteethmaccore_tx_crc_source_payload_data;
reg liteethmaccore_tx_crc_source_payload_last_be;
reg liteethmaccore_tx_crc_source_payload_error;
reg [31:0] liteethmaccore_tx_crc_crc_packet = 32'd0;
reg liteethmaccore_tx_crc_last_be = 1'd0;
wire [7:0] liteethmaccore_tx_crc_data0;
wire liteethmaccore_tx_crc_be;
reg [31:0] liteethmaccore_tx_crc_value;
reg liteethmaccore_tx_crc_error;
wire [7:0] liteethmaccore_tx_crc_data1;
wire [31:0] liteethmaccore_tx_crc_crc_prev;
reg [31:0] liteethmaccore_tx_crc_crc_next;
reg [31:0] liteethmaccore_tx_crc_reg = 32'd4294967295;
reg liteethmaccore_tx_crc_ce;
reg liteethmaccore_tx_crc_reset;
reg [1:0] liteethmaccore_tx_crc_cnt = 2'd3;
wire liteethmaccore_tx_crc_cnt_done;
reg liteethmaccore_tx_crc_is_ongoing0;
reg liteethmaccore_tx_crc_is_ongoing1;
wire liteethmaccore_tx_crc_sink_sink_valid;
wire liteethmaccore_tx_crc_sink_sink_ready;
wire liteethmaccore_tx_crc_sink_sink_first;
wire liteethmaccore_tx_crc_sink_sink_last;
wire [7:0] liteethmaccore_tx_crc_sink_sink_payload_data;
wire liteethmaccore_tx_crc_sink_sink_payload_last_be;
wire liteethmaccore_tx_crc_sink_sink_payload_error;
wire liteethmaccore_tx_crc_source_source_valid;
wire liteethmaccore_tx_crc_source_source_ready;
wire liteethmaccore_tx_crc_source_source_first;
wire liteethmaccore_tx_crc_source_source_last;
wire [7:0] liteethmaccore_tx_crc_source_source_payload_data;
wire liteethmaccore_tx_crc_source_source_payload_last_be;
wire liteethmaccore_tx_crc_source_source_payload_error;
wire liteethmaccore_tx_crc_pipe_valid_sink_valid;
wire liteethmaccore_tx_crc_pipe_valid_sink_ready;
wire liteethmaccore_tx_crc_pipe_valid_sink_first;
wire liteethmaccore_tx_crc_pipe_valid_sink_last;
wire [7:0] liteethmaccore_tx_crc_pipe_valid_sink_payload_data;
wire liteethmaccore_tx_crc_pipe_valid_sink_payload_last_be;
wire liteethmaccore_tx_crc_pipe_valid_sink_payload_error;
reg liteethmaccore_tx_crc_pipe_valid_source_valid = 1'd0;
wire liteethmaccore_tx_crc_pipe_valid_source_ready;
reg liteethmaccore_tx_crc_pipe_valid_source_first = 1'd0;
reg liteethmaccore_tx_crc_pipe_valid_source_last = 1'd0;
reg [7:0] liteethmaccore_tx_crc_pipe_valid_source_payload_data = 8'd0;
reg liteethmaccore_tx_crc_pipe_valid_source_payload_last_be = 1'd0;
reg liteethmaccore_tx_crc_pipe_valid_source_payload_error = 1'd0;
wire liteethmaccore_tx_preamble_sink_valid;
reg liteethmaccore_tx_preamble_sink_ready;
wire liteethmaccore_tx_preamble_sink_first;
wire liteethmaccore_tx_preamble_sink_last;
wire [7:0] liteethmaccore_tx_preamble_sink_payload_data;
wire liteethmaccore_tx_preamble_sink_payload_last_be;
wire liteethmaccore_tx_preamble_sink_payload_error;
reg liteethmaccore_tx_preamble_source_valid;
wire liteethmaccore_tx_preamble_source_ready;
reg liteethmaccore_tx_preamble_source_first;
reg liteethmaccore_tx_preamble_source_last;
reg [7:0] liteethmaccore_tx_preamble_source_payload_data;
wire liteethmaccore_tx_preamble_source_payload_last_be;
reg liteethmaccore_tx_preamble_source_payload_error;
reg [63:0] liteethmaccore_tx_preamble_preamble = 64'd15372286728091293013;
reg [2:0] liteethmaccore_tx_preamble_count = 3'd0;
wire liteethmaccore_tx_gap_sink_valid;
reg liteethmaccore_tx_gap_sink_ready;
wire liteethmaccore_tx_gap_sink_first;
wire liteethmaccore_tx_gap_sink_last;
wire [7:0] liteethmaccore_tx_gap_sink_payload_data;
wire liteethmaccore_tx_gap_sink_payload_last_be;
wire liteethmaccore_tx_gap_sink_payload_error;
reg liteethmaccore_tx_gap_source_valid;
wire liteethmaccore_tx_gap_source_ready;
reg liteethmaccore_tx_gap_source_first;
reg liteethmaccore_tx_gap_source_last;
reg [7:0] liteethmaccore_tx_gap_source_payload_data;
reg liteethmaccore_tx_gap_source_payload_last_be;
reg liteethmaccore_tx_gap_source_payload_error;
reg [3:0] liteethmaccore_tx_gap_counter = 4'd0;
reg [31:0] liteethmaccore_preamble_errors_status = 32'd0;
reg [31:0] liteethmaccore_crc_errors_status = 32'd0;
wire liteethmaccore_rx_preamble_sink_valid;
reg liteethmaccore_rx_preamble_sink_ready;
wire liteethmaccore_rx_preamble_sink_first;
wire liteethmaccore_rx_preamble_sink_last;
wire [7:0] liteethmaccore_rx_preamble_sink_payload_data;
wire liteethmaccore_rx_preamble_sink_payload_last_be;
wire liteethmaccore_rx_preamble_sink_payload_error;
reg liteethmaccore_rx_preamble_source_valid;
wire liteethmaccore_rx_preamble_source_ready;
reg liteethmaccore_rx_preamble_source_first;
reg liteethmaccore_rx_preamble_source_last;
wire [7:0] liteethmaccore_rx_preamble_source_payload_data;
wire liteethmaccore_rx_preamble_source_payload_last_be;
reg liteethmaccore_rx_preamble_source_payload_error;
reg liteethmaccore_rx_preamble_error;
reg [63:0] liteethmaccore_rx_preamble_preamble = 64'd15372286728091293013;
wire liteethmaccore_pulsesynchronizer0_i;
wire liteethmaccore_pulsesynchronizer0_o;
reg liteethmaccore_pulsesynchronizer0_toggle_i = 1'd0;
wire liteethmaccore_pulsesynchronizer0_toggle_o;
reg liteethmaccore_pulsesynchronizer0_toggle_o_r = 1'd0;
wire liteethmaccore_liteethmaccrc32checker_sink_sink_valid;
reg liteethmaccore_liteethmaccrc32checker_sink_sink_ready;
wire liteethmaccore_liteethmaccrc32checker_sink_sink_first;
wire liteethmaccore_liteethmaccrc32checker_sink_sink_last;
wire [7:0] liteethmaccore_liteethmaccrc32checker_sink_sink_payload_data;
wire liteethmaccore_liteethmaccrc32checker_sink_sink_payload_last_be;
wire liteethmaccore_liteethmaccrc32checker_sink_sink_payload_error;
reg liteethmaccore_liteethmaccrc32checker_source_source_valid;
wire liteethmaccore_liteethmaccrc32checker_source_source_ready;
wire liteethmaccore_liteethmaccrc32checker_source_source_first;
reg liteethmaccore_liteethmaccrc32checker_source_source_last;
wire [7:0] liteethmaccore_liteethmaccrc32checker_source_source_payload_data;
reg liteethmaccore_liteethmaccrc32checker_source_source_payload_last_be;
reg liteethmaccore_liteethmaccrc32checker_source_source_payload_error;
reg liteethmaccore_liteethmaccrc32checker_error;
wire [7:0] liteethmaccore_liteethmaccrc32checker_crc_data0;
wire liteethmaccore_liteethmaccrc32checker_crc_be;
reg liteethmaccore_liteethmaccrc32checker_crc_error0;
reg [7:0] liteethmaccore_liteethmaccrc32checker_crc_data1;
wire [31:0] liteethmaccore_liteethmaccrc32checker_crc_crc_prev;
reg [31:0] liteethmaccore_liteethmaccrc32checker_crc_crc_next;
reg [31:0] liteethmaccore_liteethmaccrc32checker_crc_reg = 32'd4294967295;
reg liteethmaccore_liteethmaccrc32checker_crc_ce;
reg liteethmaccore_liteethmaccrc32checker_crc_reset;
reg liteethmaccore_liteethmaccrc32checker_syncfifo_sink_valid;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_sink_ready;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_sink_first;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_sink_last;
wire [7:0] liteethmaccore_liteethmaccrc32checker_syncfifo_sink_payload_data;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_sink_payload_last_be;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_sink_payload_error;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_source_valid;
reg liteethmaccore_liteethmaccrc32checker_syncfifo_source_ready;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_source_first;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_source_last;
wire [7:0] liteethmaccore_liteethmaccrc32checker_syncfifo_source_payload_data;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_source_payload_last_be;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_source_payload_error;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_we;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_writable;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_re;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_readable;
wire [11:0] liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_din;
wire [11:0] liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_dout;
reg [2:0] liteethmaccore_liteethmaccrc32checker_syncfifo_level = 3'd0;
reg liteethmaccore_liteethmaccrc32checker_syncfifo_replace = 1'd0;
reg [2:0] liteethmaccore_liteethmaccrc32checker_syncfifo_produce = 3'd0;
reg [2:0] liteethmaccore_liteethmaccrc32checker_syncfifo_consume = 3'd0;
reg [2:0] liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_adr;
wire [11:0] liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_dat_r;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_we;
wire [11:0] liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_dat_w;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_do_read;
wire [2:0] liteethmaccore_liteethmaccrc32checker_syncfifo_rdport_adr;
wire [11:0] liteethmaccore_liteethmaccrc32checker_syncfifo_rdport_dat_r;
wire [7:0] liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_payload_data;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_payload_last_be;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_payload_error;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_first;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_last;
wire [7:0] liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_payload_data;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_payload_last_be;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_payload_error;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_first;
wire liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_last;
reg liteethmaccore_liteethmaccrc32checker_fifo_reset;
wire liteethmaccore_liteethmaccrc32checker_fifo_in;
wire liteethmaccore_liteethmaccrc32checker_fifo_out;
wire liteethmaccore_liteethmaccrc32checker_fifo_full;
reg liteethmaccore_liteethmaccrc32checker_last_be = 1'd0;
reg liteethmaccore_liteethmaccrc32checker_crc_error1 = 1'd0;
wire liteethmaccore_bufferizeendpoints_sink_sink_valid;
wire liteethmaccore_bufferizeendpoints_sink_sink_ready;
wire liteethmaccore_bufferizeendpoints_sink_sink_first;
wire liteethmaccore_bufferizeendpoints_sink_sink_last;
wire [7:0] liteethmaccore_bufferizeendpoints_sink_sink_payload_data;
wire liteethmaccore_bufferizeendpoints_sink_sink_payload_last_be;
wire liteethmaccore_bufferizeendpoints_sink_sink_payload_error;
wire liteethmaccore_bufferizeendpoints_source_source_valid;
wire liteethmaccore_bufferizeendpoints_source_source_ready;
wire liteethmaccore_bufferizeendpoints_source_source_first;
wire liteethmaccore_bufferizeendpoints_source_source_last;
wire [7:0] liteethmaccore_bufferizeendpoints_source_source_payload_data;
wire liteethmaccore_bufferizeendpoints_source_source_payload_last_be;
wire liteethmaccore_bufferizeendpoints_source_source_payload_error;
wire liteethmaccore_bufferizeendpoints_pipe_valid_sink_valid;
wire liteethmaccore_bufferizeendpoints_pipe_valid_sink_ready;
wire liteethmaccore_bufferizeendpoints_pipe_valid_sink_first;
wire liteethmaccore_bufferizeendpoints_pipe_valid_sink_last;
wire [7:0] liteethmaccore_bufferizeendpoints_pipe_valid_sink_payload_data;
wire liteethmaccore_bufferizeendpoints_pipe_valid_sink_payload_last_be;
wire liteethmaccore_bufferizeendpoints_pipe_valid_sink_payload_error;
reg liteethmaccore_bufferizeendpoints_pipe_valid_source_valid = 1'd0;
wire liteethmaccore_bufferizeendpoints_pipe_valid_source_ready;
reg liteethmaccore_bufferizeendpoints_pipe_valid_source_first = 1'd0;
reg liteethmaccore_bufferizeendpoints_pipe_valid_source_last = 1'd0;
reg [7:0] liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_data = 8'd0;
reg liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_last_be = 1'd0;
reg liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_error = 1'd0;
wire liteethmaccore_pulsesynchronizer1_i;
wire liteethmaccore_pulsesynchronizer1_o;
reg liteethmaccore_pulsesynchronizer1_toggle_i = 1'd0;
wire liteethmaccore_pulsesynchronizer1_toggle_o;
reg liteethmaccore_pulsesynchronizer1_toggle_o_r = 1'd0;
wire liteethmaccore_rx_padding_sink_valid;
wire liteethmaccore_rx_padding_sink_ready;
wire liteethmaccore_rx_padding_sink_first;
wire liteethmaccore_rx_padding_sink_last;
wire [7:0] liteethmaccore_rx_padding_sink_payload_data;
wire liteethmaccore_rx_padding_sink_payload_last_be;
wire liteethmaccore_rx_padding_sink_payload_error;
wire liteethmaccore_rx_padding_source_valid;
wire liteethmaccore_rx_padding_source_ready;
wire liteethmaccore_rx_padding_source_first;
wire liteethmaccore_rx_padding_source_last;
wire [7:0] liteethmaccore_rx_padding_source_payload_data;
wire liteethmaccore_rx_padding_source_payload_last_be;
reg liteethmaccore_rx_padding_source_payload_error;
reg [10:0] liteethmaccore_rx_padding_length = 11'd0;
reg [3:0] liteethmaccore_rx_padding_length_inc;
wire liteethmaccore_rx_last_be_sink_valid;
wire liteethmaccore_rx_last_be_sink_ready;
wire liteethmaccore_rx_last_be_sink_first;
wire liteethmaccore_rx_last_be_sink_last;
wire [7:0] liteethmaccore_rx_last_be_sink_payload_data;
wire liteethmaccore_rx_last_be_sink_payload_last_be;
wire liteethmaccore_rx_last_be_sink_payload_error;
wire liteethmaccore_rx_last_be_source_valid;
wire liteethmaccore_rx_last_be_source_ready;
wire liteethmaccore_rx_last_be_source_first;
wire liteethmaccore_rx_last_be_source_last;
wire [7:0] liteethmaccore_rx_last_be_source_payload_data;
reg liteethmaccore_rx_last_be_source_payload_last_be;
wire liteethmaccore_rx_last_be_source_payload_error;
wire liteethmaccore_rx_converter_sink_valid;
wire liteethmaccore_rx_converter_sink_ready;
wire liteethmaccore_rx_converter_sink_first;
wire liteethmaccore_rx_converter_sink_last;
wire [7:0] liteethmaccore_rx_converter_sink_payload_data;
wire liteethmaccore_rx_converter_sink_payload_last_be;
wire liteethmaccore_rx_converter_sink_payload_error;
wire liteethmaccore_rx_converter_source_valid;
wire liteethmaccore_rx_converter_source_ready;
wire liteethmaccore_rx_converter_source_first;
wire liteethmaccore_rx_converter_source_last;
reg [63:0] liteethmaccore_rx_converter_source_payload_data;
reg [7:0] liteethmaccore_rx_converter_source_payload_last_be;
reg [7:0] liteethmaccore_rx_converter_source_payload_error;
wire liteethmaccore_rx_converter_converter_sink_valid;
wire liteethmaccore_rx_converter_converter_sink_ready;
wire liteethmaccore_rx_converter_converter_sink_first;
wire liteethmaccore_rx_converter_converter_sink_last;
wire [9:0] liteethmaccore_rx_converter_converter_sink_payload_data;
wire liteethmaccore_rx_converter_converter_source_valid;
wire liteethmaccore_rx_converter_converter_source_ready;
reg liteethmaccore_rx_converter_converter_source_first = 1'd0;
reg liteethmaccore_rx_converter_converter_source_last = 1'd0;
reg [79:0] liteethmaccore_rx_converter_converter_source_payload_data = 80'd0;
reg [3:0] liteethmaccore_rx_converter_converter_source_payload_valid_token_count = 4'd0;
reg [2:0] liteethmaccore_rx_converter_converter_demux = 3'd0;
wire liteethmaccore_rx_converter_converter_load_part;
reg liteethmaccore_rx_converter_converter_strobe_all = 1'd0;
wire liteethmaccore_rx_converter_source_source_valid;
wire liteethmaccore_rx_converter_source_source_ready;
wire liteethmaccore_rx_converter_source_source_first;
wire liteethmaccore_rx_converter_source_source_last;
wire [79:0] liteethmaccore_rx_converter_source_source_payload_data;
wire liteethmaccore_rx_cdc_sink_sink_valid;
wire liteethmaccore_rx_cdc_sink_sink_ready;
wire liteethmaccore_rx_cdc_sink_sink_first;
wire liteethmaccore_rx_cdc_sink_sink_last;
wire [63:0] liteethmaccore_rx_cdc_sink_sink_payload_data;
wire [7:0] liteethmaccore_rx_cdc_sink_sink_payload_last_be;
wire [7:0] liteethmaccore_rx_cdc_sink_sink_payload_error;
wire liteethmaccore_rx_cdc_source_source_valid;
wire liteethmaccore_rx_cdc_source_source_ready;
wire liteethmaccore_rx_cdc_source_source_first;
wire liteethmaccore_rx_cdc_source_source_last;
wire [63:0] liteethmaccore_rx_cdc_source_source_payload_data;
wire [7:0] liteethmaccore_rx_cdc_source_source_payload_last_be;
wire [7:0] liteethmaccore_rx_cdc_source_source_payload_error;
wire liteethmaccore_rx_cdc_cdc_sink_valid;
wire liteethmaccore_rx_cdc_cdc_sink_ready;
wire liteethmaccore_rx_cdc_cdc_sink_first;
wire liteethmaccore_rx_cdc_cdc_sink_last;
wire [63:0] liteethmaccore_rx_cdc_cdc_sink_payload_data;
wire [7:0] liteethmaccore_rx_cdc_cdc_sink_payload_last_be;
wire [7:0] liteethmaccore_rx_cdc_cdc_sink_payload_error;
wire liteethmaccore_rx_cdc_cdc_source_valid;
wire liteethmaccore_rx_cdc_cdc_source_ready;
wire liteethmaccore_rx_cdc_cdc_source_first;
wire liteethmaccore_rx_cdc_cdc_source_last;
wire [63:0] liteethmaccore_rx_cdc_cdc_source_payload_data;
wire [7:0] liteethmaccore_rx_cdc_cdc_source_payload_last_be;
wire [7:0] liteethmaccore_rx_cdc_cdc_source_payload_error;
wire liteethmaccore_rx_cdc_cdc_asyncfifo_we;
wire liteethmaccore_rx_cdc_cdc_asyncfifo_writable;
wire liteethmaccore_rx_cdc_cdc_asyncfifo_re;
wire liteethmaccore_rx_cdc_cdc_asyncfifo_readable;
wire [81:0] liteethmaccore_rx_cdc_cdc_asyncfifo_din;
wire [81:0] liteethmaccore_rx_cdc_cdc_asyncfifo_dout;
wire liteethmaccore_rx_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [5:0] liteethmaccore_rx_cdc_cdc_graycounter0_q = 6'd0;
wire [5:0] liteethmaccore_rx_cdc_cdc_graycounter0_q_next;
reg [5:0] liteethmaccore_rx_cdc_cdc_graycounter0_q_binary = 6'd0;
reg [5:0] liteethmaccore_rx_cdc_cdc_graycounter0_q_next_binary;
wire liteethmaccore_rx_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [5:0] liteethmaccore_rx_cdc_cdc_graycounter1_q = 6'd0;
wire [5:0] liteethmaccore_rx_cdc_cdc_graycounter1_q_next;
reg [5:0] liteethmaccore_rx_cdc_cdc_graycounter1_q_binary = 6'd0;
reg [5:0] liteethmaccore_rx_cdc_cdc_graycounter1_q_next_binary;
wire [5:0] liteethmaccore_rx_cdc_cdc_produce_rdomain;
wire [5:0] liteethmaccore_rx_cdc_cdc_consume_wdomain;
wire [4:0] liteethmaccore_rx_cdc_cdc_wrport_adr;
wire [81:0] liteethmaccore_rx_cdc_cdc_wrport_dat_r;
wire liteethmaccore_rx_cdc_cdc_wrport_we;
wire [81:0] liteethmaccore_rx_cdc_cdc_wrport_dat_w;
wire [4:0] liteethmaccore_rx_cdc_cdc_rdport_adr;
wire [81:0] liteethmaccore_rx_cdc_cdc_rdport_dat_r;
wire [63:0] liteethmaccore_rx_cdc_cdc_fifo_in_payload_data;
wire [7:0] liteethmaccore_rx_cdc_cdc_fifo_in_payload_last_be;
wire [7:0] liteethmaccore_rx_cdc_cdc_fifo_in_payload_error;
wire liteethmaccore_rx_cdc_cdc_fifo_in_first;
wire liteethmaccore_rx_cdc_cdc_fifo_in_last;
wire [63:0] liteethmaccore_rx_cdc_cdc_fifo_out_payload_data;
wire [7:0] liteethmaccore_rx_cdc_cdc_fifo_out_payload_last_be;
wire [7:0] liteethmaccore_rx_cdc_cdc_fifo_out_payload_error;
wire liteethmaccore_rx_cdc_cdc_fifo_out_first;
wire liteethmaccore_rx_cdc_cdc_fifo_out_last;
reg packetfifo_sink_sink_valid;
wire packetfifo_sink_sink_ready;
reg packetfifo_sink_sink_first = 1'd0;
wire packetfifo_sink_sink_last;
wire [63:0] packetfifo_sink_sink_payload_data;
wire [7:0] packetfifo_sink_sink_payload_last_be;
reg [7:0] packetfifo_sink_sink_payload_error = 8'd0;
wire packetfifo_source_source_valid;
wire packetfifo_source_source_ready;
reg packetfifo_source_source_first;
wire packetfifo_source_source_last;
wire [63:0] packetfifo_source_source_payload_data;
wire [7:0] packetfifo_source_source_payload_last_be;
wire [7:0] packetfifo_source_source_payload_error;
wire packetfifo_payload_fifo_sink_valid;
wire packetfifo_payload_fifo_sink_ready;
wire packetfifo_payload_fifo_sink_first;
wire packetfifo_payload_fifo_sink_last;
wire [63:0] packetfifo_payload_fifo_sink_payload_data;
wire [7:0] packetfifo_payload_fifo_sink_payload_last_be;
wire [7:0] packetfifo_payload_fifo_sink_payload_error;
wire packetfifo_payload_fifo_source_valid;
wire packetfifo_payload_fifo_source_ready;
wire packetfifo_payload_fifo_source_first;
wire packetfifo_payload_fifo_source_last;
wire [63:0] packetfifo_payload_fifo_source_payload_data;
wire [7:0] packetfifo_payload_fifo_source_payload_last_be;
wire [7:0] packetfifo_payload_fifo_source_payload_error;
wire packetfifo_payload_fifo_re;
reg packetfifo_payload_fifo_readable = 1'd0;
wire packetfifo_payload_fifo_syncfifo_we;
wire packetfifo_payload_fifo_syncfifo_writable;
wire packetfifo_payload_fifo_syncfifo_re;
wire packetfifo_payload_fifo_syncfifo_readable;
wire [81:0] packetfifo_payload_fifo_syncfifo_din;
wire [81:0] packetfifo_payload_fifo_syncfifo_dout;
reg [9:0] packetfifo_payload_fifo_level0 = 10'd0;
reg packetfifo_payload_fifo_replace = 1'd0;
reg [8:0] packetfifo_payload_fifo_produce = 9'd0;
reg [8:0] packetfifo_payload_fifo_consume = 9'd0;
reg [8:0] packetfifo_payload_fifo_wrport_adr;
wire [81:0] packetfifo_payload_fifo_wrport_dat_r;
wire packetfifo_payload_fifo_wrport_we;
wire [81:0] packetfifo_payload_fifo_wrport_dat_w;
wire packetfifo_payload_fifo_do_read;
wire [8:0] packetfifo_payload_fifo_rdport_adr;
wire [81:0] packetfifo_payload_fifo_rdport_dat_r;
wire packetfifo_payload_fifo_rdport_re;
wire [9:0] packetfifo_payload_fifo_level1;
wire [63:0] packetfifo_payload_fifo_fifo_in_payload_data;
wire [7:0] packetfifo_payload_fifo_fifo_in_payload_last_be;
wire [7:0] packetfifo_payload_fifo_fifo_in_payload_error;
wire packetfifo_payload_fifo_fifo_in_first;
wire packetfifo_payload_fifo_fifo_in_last;
wire [63:0] packetfifo_payload_fifo_fifo_out_payload_data;
wire [7:0] packetfifo_payload_fifo_fifo_out_payload_last_be;
wire [7:0] packetfifo_payload_fifo_fifo_out_payload_error;
wire packetfifo_payload_fifo_fifo_out_first;
wire packetfifo_payload_fifo_fifo_out_last;
wire packetfifo_param_fifo_sink_valid;
wire packetfifo_param_fifo_sink_ready;
reg packetfifo_param_fifo_sink_first = 1'd0;
reg packetfifo_param_fifo_sink_last = 1'd0;
reg packetfifo_param_fifo_sink_param_dummy = 1'd0;
wire packetfifo_param_fifo_source_valid;
wire packetfifo_param_fifo_source_ready;
wire packetfifo_param_fifo_source_first;
wire packetfifo_param_fifo_source_last;
wire packetfifo_param_fifo_source_param_dummy;
wire packetfifo_param_fifo_re;
reg packetfifo_param_fifo_readable = 1'd0;
wire packetfifo_param_fifo_syncfifo_we;
wire packetfifo_param_fifo_syncfifo_writable;
wire packetfifo_param_fifo_syncfifo_re;
wire packetfifo_param_fifo_syncfifo_readable;
wire [2:0] packetfifo_param_fifo_syncfifo_din;
wire [2:0] packetfifo_param_fifo_syncfifo_dout;
reg [3:0] packetfifo_param_fifo_level0 = 4'd0;
reg packetfifo_param_fifo_replace = 1'd0;
reg [3:0] packetfifo_param_fifo_produce = 4'd0;
reg [3:0] packetfifo_param_fifo_consume = 4'd0;
reg [3:0] packetfifo_param_fifo_wrport_adr;
wire [2:0] packetfifo_param_fifo_wrport_dat_r;
wire packetfifo_param_fifo_wrport_we;
wire [2:0] packetfifo_param_fifo_wrport_dat_w;
wire packetfifo_param_fifo_do_read;
wire [3:0] packetfifo_param_fifo_rdport_adr;
wire [2:0] packetfifo_param_fifo_rdport_dat_r;
wire packetfifo_param_fifo_rdport_re;
wire [3:0] packetfifo_param_fifo_level1;
wire packetfifo_param_fifo_fifo_in_param_dummy;
wire packetfifo_param_fifo_fifo_in_first;
wire packetfifo_param_fifo_fifo_in_last;
wire packetfifo_param_fifo_fifo_out_param_dummy;
wire packetfifo_param_fifo_fifo_out_first;
wire packetfifo_param_fifo_fifo_out_last;
wire tx_dp_sink_sink_valid;
wire tx_dp_sink_sink_ready;
reg tx_dp_sink_sink_first = 1'd0;
wire tx_dp_sink_sink_last;
wire [63:0] tx_dp_sink_sink_payload_data;
wire [7:0] tx_dp_sink_sink_payload_keep;
wire tx_dp_source_source_valid;
reg tx_dp_source_source_ready;
wire tx_dp_source_source_first;
wire tx_dp_source_source_last;
wire [63:0] tx_dp_source_source_payload_data;
wire [7:0] tx_dp_source_source_payload_keep;
wire tx_dp_cdc_sink_valid;
wire tx_dp_cdc_sink_ready;
wire tx_dp_cdc_sink_first;
wire tx_dp_cdc_sink_last;
wire [63:0] tx_dp_cdc_sink_payload_data;
wire [7:0] tx_dp_cdc_sink_payload_keep;
wire tx_dp_cdc_source_valid;
wire tx_dp_cdc_source_ready;
wire tx_dp_cdc_source_first;
wire tx_dp_cdc_source_last;
wire [63:0] tx_dp_cdc_source_payload_data;
wire [7:0] tx_dp_cdc_source_payload_keep;
wire tx_dp_cdc_re;
reg tx_dp_cdc_readable = 1'd0;
reg [73:0] tx_dp_cdc_dout = 74'd0;
wire tx_dp_cdc_asyncfifo_we;
wire tx_dp_cdc_asyncfifo_writable;
wire tx_dp_cdc_asyncfifo_re;
wire tx_dp_cdc_asyncfifo_readable;
wire [73:0] tx_dp_cdc_asyncfifo_din;
wire [73:0] tx_dp_cdc_asyncfifo_dout;
wire tx_dp_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [4:0] tx_dp_cdc_graycounter0_q = 5'd0;
wire [4:0] tx_dp_cdc_graycounter0_q_next;
reg [4:0] tx_dp_cdc_graycounter0_q_binary = 5'd0;
reg [4:0] tx_dp_cdc_graycounter0_q_next_binary;
wire tx_dp_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [4:0] tx_dp_cdc_graycounter1_q = 5'd0;
wire [4:0] tx_dp_cdc_graycounter1_q_next;
reg [4:0] tx_dp_cdc_graycounter1_q_binary = 5'd0;
reg [4:0] tx_dp_cdc_graycounter1_q_next_binary;
wire [4:0] tx_dp_cdc_produce_rdomain;
wire [4:0] tx_dp_cdc_consume_wdomain;
wire [3:0] tx_dp_cdc_wrport_adr;
wire [73:0] tx_dp_cdc_wrport_dat_r;
wire tx_dp_cdc_wrport_we;
wire [73:0] tx_dp_cdc_wrport_dat_w;
wire [3:0] tx_dp_cdc_rdport_adr;
wire [73:0] tx_dp_cdc_rdport_dat_r;
wire [63:0] tx_dp_cdc_fifo_in_payload_data;
wire [7:0] tx_dp_cdc_fifo_in_payload_keep;
wire tx_dp_cdc_fifo_in_first;
wire tx_dp_cdc_fifo_in_last;
wire [63:0] tx_dp_cdc_fifo_out_payload_data;
wire [7:0] tx_dp_cdc_fifo_out_payload_keep;
wire tx_dp_cdc_fifo_out_first;
wire tx_dp_cdc_fifo_out_last;
reg txdatapath_liteethmactxlastbe_state = 1'd0;
reg txdatapath_liteethmactxlastbe_next_state;
reg txdatapath_liteethmacpaddinginserter_state = 1'd0;
reg txdatapath_liteethmacpaddinginserter_next_state;
reg [15:0] liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value;
reg liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value_ce;
reg [1:0] txdatapath_bufferizeendpoints_state = 2'd0;
reg [1:0] txdatapath_bufferizeendpoints_next_state;
reg [31:0] liteethmaccore_tx_crc_crc_packet_clockdomainsrenamer1_next_value0;
reg liteethmaccore_tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0;
reg liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value1;
reg liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value_ce1;
reg [1:0] txdatapath_liteethmacpreambleinserter_state = 2'd0;
reg [1:0] txdatapath_liteethmacpreambleinserter_next_state;
reg [2:0] liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value;
reg liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value_ce;
reg txdatapath_liteethmacgap_state = 1'd0;
reg txdatapath_liteethmacgap_next_state;
reg [3:0] liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value;
reg liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value_ce;
reg rxdatapath_liteethmacpreamblechecker_state = 1'd0;
reg rxdatapath_liteethmacpreamblechecker_next_state;
reg [1:0] rxdatapath_bufferizeendpoints_state = 2'd0;
reg [1:0] rxdatapath_bufferizeendpoints_next_state;
reg liteethmaccore_liteethmaccrc32checker_last_be_next_value0;
reg liteethmaccore_liteethmaccrc32checker_last_be_next_value_ce0;
reg liteethmaccore_liteethmaccrc32checker_crc_error1_next_value1;
reg liteethmaccore_liteethmaccrc32checker_crc_error1_next_value_ce1;
wire [39:0] slice_proxy;
wire resync_clk;
reg simasyncresetsynchronizerimpl0_rst1 = 1'd0;
wire resync_clk_1;
reg simasyncresetsynchronizerimpl1_rst1 = 1'd0;
wire resync_clk_2;
reg simasyncresetsynchronizerimpl2_rst1 = 1'd0;
wire resync_clk_3;
reg simasyncresetsynchronizerimpl3_rst1 = 1'd0;
wire resync_clk_4;
reg simasyncresetsynchronizerimpl4_rst1 = 1'd0;
wire resync_clk_5;
reg simasyncresetsynchronizerimpl5_rst1 = 1'd0;
(* no_retiming = "true" *) reg [5:0] multiregimpl00 = 6'd0;
(* no_retiming = "true" *) reg [5:0] multiregimpl01 = 6'd0;
(* no_retiming = "true" *) reg [5:0] multiregimpl10 = 6'd0;
(* no_retiming = "true" *) reg [5:0] multiregimpl11 = 6'd0;
(* no_retiming = "true" *) reg multiregimpl20 = 1'd0;
(* no_retiming = "true" *) reg multiregimpl21 = 1'd0;
(* no_retiming = "true" *) reg multiregimpl30 = 1'd0;
(* no_retiming = "true" *) reg multiregimpl31 = 1'd0;
(* no_retiming = "true" *) reg [5:0] multiregimpl40 = 6'd0;
(* no_retiming = "true" *) reg [5:0] multiregimpl41 = 6'd0;
(* no_retiming = "true" *) reg [5:0] multiregimpl50 = 6'd0;
(* no_retiming = "true" *) reg [5:0] multiregimpl51 = 6'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl60 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl61 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl70 = 5'd0;
(* no_retiming = "true" *) reg [4:0] multiregimpl71 = 5'd0;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign eth_tx_clk_1 = eth_tx_clk;
assign eth_rx_clk_1 = eth_rx_clk;
assign macsys_clk = sys_clk;
assign macdp_clk = dp_clk;
assign maceth_tx_clk = eth_tx_clk;
assign maceth_rx_clk = eth_rx_clk;
assign liteethmaccore_sink_valid = packetfifo_source_source_valid;
assign packetfifo_source_source_ready = liteethmaccore_sink_ready;
assign liteethmaccore_sink_first = packetfifo_source_source_first;
assign liteethmaccore_sink_last = packetfifo_source_source_last;
assign liteethmaccore_sink_payload_data = packetfifo_source_source_payload_data;
assign liteethmaccore_sink_payload_last_be = packetfifo_source_source_payload_last_be;
assign liteethmaccore_sink_payload_error = packetfifo_source_source_payload_error;
assign tx_dp_sink_sink_payload_data = dp_tdata;
assign tx_dp_sink_sink_payload_keep = dp_tkeep;
assign tx_dp_sink_sink_valid = dp_tvalid;
assign tx_dp_sink_sink_last = dp_tlast;
assign dp_tready = tx_dp_sink_sink_ready;
assign packetfifo_sink_sink_payload_data = tx_dp_source_source_payload_data;
assign packetfifo_sink_sink_last = tx_dp_source_source_last;
assign packetfifo_sink_sink_payload_last_be = (tx_dp_source_source_last ? (tx_dp_source_source_payload_keep & (~(tx_dp_source_source_payload_keep >>> 1'd1))) : 1'd0);

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	liteethmaccore_source_ready <= 1'd0;
	packetfifo_sink_sink_valid <= 1'd0;
	tx_dp_source_source_ready <= 1'd0;
	if (loopback) begin
		packetfifo_sink_sink_valid <= 1'd0;
		liteethmaccore_source_ready <= 1'd0;
	end else begin
		packetfifo_sink_sink_valid <= tx_dp_source_source_valid;
		tx_dp_source_source_ready <= packetfifo_sink_sink_ready;
		liteethmaccore_source_ready <= 1'd1;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end
assign phy_sink_valid = phy_sink_valid1;
assign phy_sink_ready = phy_sink_ready1;
assign phy_sink_data = phy_sink_payload_data;
assign phy_sink_last = phy_sink_last1;
assign gmii_tx_en = pads_tx_en;
assign gmii_tx_data = pads_tx_data;
assign gmii_tx_er = pads_tx_er;
assign maceth_tx_rst = maceth_tx_rst_1;
assign phy_source_last = ((~pads_rx_dv) & phy_dv_d);
assign liteethmaccore_tx_cdc_cdc_sink_valid = liteethmaccore_tx_cdc_sink_sink_valid;
assign liteethmaccore_tx_cdc_sink_sink_ready = liteethmaccore_tx_cdc_cdc_sink_ready;
assign liteethmaccore_tx_cdc_cdc_sink_first = liteethmaccore_tx_cdc_sink_sink_first;
assign liteethmaccore_tx_cdc_cdc_sink_last = liteethmaccore_tx_cdc_sink_sink_last;
assign liteethmaccore_tx_cdc_cdc_sink_payload_data = liteethmaccore_tx_cdc_sink_sink_payload_data;
assign liteethmaccore_tx_cdc_cdc_sink_payload_last_be = liteethmaccore_tx_cdc_sink_sink_payload_last_be;
assign liteethmaccore_tx_cdc_cdc_sink_payload_error = liteethmaccore_tx_cdc_sink_sink_payload_error;
assign liteethmaccore_tx_cdc_source_source_valid = liteethmaccore_tx_cdc_cdc_source_valid;
assign liteethmaccore_tx_cdc_cdc_source_ready = liteethmaccore_tx_cdc_source_source_ready;
assign liteethmaccore_tx_cdc_source_source_first = liteethmaccore_tx_cdc_cdc_source_first;
assign liteethmaccore_tx_cdc_source_source_last = liteethmaccore_tx_cdc_cdc_source_last;
assign liteethmaccore_tx_cdc_source_source_payload_data = liteethmaccore_tx_cdc_cdc_source_payload_data;
assign liteethmaccore_tx_cdc_source_source_payload_last_be = liteethmaccore_tx_cdc_cdc_source_payload_last_be;
assign liteethmaccore_tx_cdc_source_source_payload_error = liteethmaccore_tx_cdc_cdc_source_payload_error;
assign liteethmaccore_tx_cdc_cdc_asyncfifo_din = {liteethmaccore_tx_cdc_cdc_fifo_in_last, liteethmaccore_tx_cdc_cdc_fifo_in_first, liteethmaccore_tx_cdc_cdc_fifo_in_payload_error, liteethmaccore_tx_cdc_cdc_fifo_in_payload_last_be, liteethmaccore_tx_cdc_cdc_fifo_in_payload_data};
assign {liteethmaccore_tx_cdc_cdc_fifo_out_last, liteethmaccore_tx_cdc_cdc_fifo_out_first, liteethmaccore_tx_cdc_cdc_fifo_out_payload_error, liteethmaccore_tx_cdc_cdc_fifo_out_payload_last_be, liteethmaccore_tx_cdc_cdc_fifo_out_payload_data} = liteethmaccore_tx_cdc_cdc_asyncfifo_dout;
assign liteethmaccore_tx_cdc_cdc_sink_ready = liteethmaccore_tx_cdc_cdc_asyncfifo_writable;
assign liteethmaccore_tx_cdc_cdc_asyncfifo_we = liteethmaccore_tx_cdc_cdc_sink_valid;
assign liteethmaccore_tx_cdc_cdc_fifo_in_first = liteethmaccore_tx_cdc_cdc_sink_first;
assign liteethmaccore_tx_cdc_cdc_fifo_in_last = liteethmaccore_tx_cdc_cdc_sink_last;
assign liteethmaccore_tx_cdc_cdc_fifo_in_payload_data = liteethmaccore_tx_cdc_cdc_sink_payload_data;
assign liteethmaccore_tx_cdc_cdc_fifo_in_payload_last_be = liteethmaccore_tx_cdc_cdc_sink_payload_last_be;
assign liteethmaccore_tx_cdc_cdc_fifo_in_payload_error = liteethmaccore_tx_cdc_cdc_sink_payload_error;
assign liteethmaccore_tx_cdc_cdc_source_valid = liteethmaccore_tx_cdc_cdc_asyncfifo_readable;
assign liteethmaccore_tx_cdc_cdc_source_first = liteethmaccore_tx_cdc_cdc_fifo_out_first;
assign liteethmaccore_tx_cdc_cdc_source_last = liteethmaccore_tx_cdc_cdc_fifo_out_last;
assign liteethmaccore_tx_cdc_cdc_source_payload_data = liteethmaccore_tx_cdc_cdc_fifo_out_payload_data;
assign liteethmaccore_tx_cdc_cdc_source_payload_last_be = liteethmaccore_tx_cdc_cdc_fifo_out_payload_last_be;
assign liteethmaccore_tx_cdc_cdc_source_payload_error = liteethmaccore_tx_cdc_cdc_fifo_out_payload_error;
assign liteethmaccore_tx_cdc_cdc_asyncfifo_re = liteethmaccore_tx_cdc_cdc_source_ready;
assign liteethmaccore_tx_cdc_cdc_graycounter0_ce = (liteethmaccore_tx_cdc_cdc_asyncfifo_writable & liteethmaccore_tx_cdc_cdc_asyncfifo_we);
assign liteethmaccore_tx_cdc_cdc_graycounter1_ce = (liteethmaccore_tx_cdc_cdc_asyncfifo_readable & liteethmaccore_tx_cdc_cdc_asyncfifo_re);
assign liteethmaccore_tx_cdc_cdc_asyncfifo_writable = (((liteethmaccore_tx_cdc_cdc_graycounter0_q[5] == liteethmaccore_tx_cdc_cdc_consume_wdomain[5]) | (liteethmaccore_tx_cdc_cdc_graycounter0_q[4] == liteethmaccore_tx_cdc_cdc_consume_wdomain[4])) | (liteethmaccore_tx_cdc_cdc_graycounter0_q[3:0] != liteethmaccore_tx_cdc_cdc_consume_wdomain[3:0]));
assign liteethmaccore_tx_cdc_cdc_asyncfifo_readable = (liteethmaccore_tx_cdc_cdc_graycounter1_q != liteethmaccore_tx_cdc_cdc_produce_rdomain);
assign liteethmaccore_tx_cdc_cdc_wrport_adr = liteethmaccore_tx_cdc_cdc_graycounter0_q_binary[4:0];
assign liteethmaccore_tx_cdc_cdc_wrport_dat_w = liteethmaccore_tx_cdc_cdc_asyncfifo_din;
assign liteethmaccore_tx_cdc_cdc_wrport_we = liteethmaccore_tx_cdc_cdc_graycounter0_ce;
assign liteethmaccore_tx_cdc_cdc_rdport_adr = liteethmaccore_tx_cdc_cdc_graycounter1_q_next_binary[4:0];
assign liteethmaccore_tx_cdc_cdc_asyncfifo_dout = liteethmaccore_tx_cdc_cdc_rdport_dat_r;

// synthesis translate_off
reg dummy_d_1;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_cdc_cdc_graycounter0_q_next_binary <= 6'd0;
	if (liteethmaccore_tx_cdc_cdc_graycounter0_ce) begin
		liteethmaccore_tx_cdc_cdc_graycounter0_q_next_binary <= (liteethmaccore_tx_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		liteethmaccore_tx_cdc_cdc_graycounter0_q_next_binary <= liteethmaccore_tx_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_1 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_tx_cdc_cdc_graycounter0_q_next = (liteethmaccore_tx_cdc_cdc_graycounter0_q_next_binary ^ liteethmaccore_tx_cdc_cdc_graycounter0_q_next_binary[5:1]);

// synthesis translate_off
reg dummy_d_2;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_cdc_cdc_graycounter1_q_next_binary <= 6'd0;
	if (liteethmaccore_tx_cdc_cdc_graycounter1_ce) begin
		liteethmaccore_tx_cdc_cdc_graycounter1_q_next_binary <= (liteethmaccore_tx_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		liteethmaccore_tx_cdc_cdc_graycounter1_q_next_binary <= liteethmaccore_tx_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_2 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_tx_cdc_cdc_graycounter1_q_next = (liteethmaccore_tx_cdc_cdc_graycounter1_q_next_binary ^ liteethmaccore_tx_cdc_cdc_graycounter1_q_next_binary[5:1]);
assign liteethmaccore_tx_converter_converter_sink_valid = liteethmaccore_tx_converter_sink_valid;
assign liteethmaccore_tx_converter_converter_sink_first = liteethmaccore_tx_converter_sink_first;
assign liteethmaccore_tx_converter_converter_sink_last = liteethmaccore_tx_converter_sink_last;
assign liteethmaccore_tx_converter_sink_ready = liteethmaccore_tx_converter_converter_sink_ready;

// synthesis translate_off
reg dummy_d_3;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_converter_converter_sink_payload_data <= 80'd0;
	liteethmaccore_tx_converter_converter_sink_payload_data[7:0] <= liteethmaccore_tx_converter_sink_payload_data[7:0];
	liteethmaccore_tx_converter_converter_sink_payload_data[8] <= liteethmaccore_tx_converter_sink_payload_last_be[0];
	liteethmaccore_tx_converter_converter_sink_payload_data[9] <= liteethmaccore_tx_converter_sink_payload_error[0];
	liteethmaccore_tx_converter_converter_sink_payload_data[17:10] <= liteethmaccore_tx_converter_sink_payload_data[15:8];
	liteethmaccore_tx_converter_converter_sink_payload_data[18] <= liteethmaccore_tx_converter_sink_payload_last_be[1];
	liteethmaccore_tx_converter_converter_sink_payload_data[19] <= liteethmaccore_tx_converter_sink_payload_error[1];
	liteethmaccore_tx_converter_converter_sink_payload_data[27:20] <= liteethmaccore_tx_converter_sink_payload_data[23:16];
	liteethmaccore_tx_converter_converter_sink_payload_data[28] <= liteethmaccore_tx_converter_sink_payload_last_be[2];
	liteethmaccore_tx_converter_converter_sink_payload_data[29] <= liteethmaccore_tx_converter_sink_payload_error[2];
	liteethmaccore_tx_converter_converter_sink_payload_data[37:30] <= liteethmaccore_tx_converter_sink_payload_data[31:24];
	liteethmaccore_tx_converter_converter_sink_payload_data[38] <= liteethmaccore_tx_converter_sink_payload_last_be[3];
	liteethmaccore_tx_converter_converter_sink_payload_data[39] <= liteethmaccore_tx_converter_sink_payload_error[3];
	liteethmaccore_tx_converter_converter_sink_payload_data[47:40] <= liteethmaccore_tx_converter_sink_payload_data[39:32];
	liteethmaccore_tx_converter_converter_sink_payload_data[48] <= liteethmaccore_tx_converter_sink_payload_last_be[4];
	liteethmaccore_tx_converter_converter_sink_payload_data[49] <= liteethmaccore_tx_converter_sink_payload_error[4];
	liteethmaccore_tx_converter_converter_sink_payload_data[57:50] <= liteethmaccore_tx_converter_sink_payload_data[47:40];
	liteethmaccore_tx_converter_converter_sink_payload_data[58] <= liteethmaccore_tx_converter_sink_payload_last_be[5];
	liteethmaccore_tx_converter_converter_sink_payload_data[59] <= liteethmaccore_tx_converter_sink_payload_error[5];
	liteethmaccore_tx_converter_converter_sink_payload_data[67:60] <= liteethmaccore_tx_converter_sink_payload_data[55:48];
	liteethmaccore_tx_converter_converter_sink_payload_data[68] <= liteethmaccore_tx_converter_sink_payload_last_be[6];
	liteethmaccore_tx_converter_converter_sink_payload_data[69] <= liteethmaccore_tx_converter_sink_payload_error[6];
	liteethmaccore_tx_converter_converter_sink_payload_data[77:70] <= liteethmaccore_tx_converter_sink_payload_data[63:56];
	liteethmaccore_tx_converter_converter_sink_payload_data[78] <= liteethmaccore_tx_converter_sink_payload_last_be[7];
	liteethmaccore_tx_converter_converter_sink_payload_data[79] <= liteethmaccore_tx_converter_sink_payload_error[7];
// synthesis translate_off
	dummy_d_3 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_tx_converter_last_be_packet_end = (liteethmaccore_tx_converter_sink_last & (liteethmaccore_tx_converter_source_payload_last_be != 1'd0));
assign liteethmaccore_tx_converter_source_valid = (liteethmaccore_tx_converter_source_source_valid & (~liteethmaccore_tx_converter_last_be_drop));
assign liteethmaccore_tx_converter_source_first = (liteethmaccore_tx_converter_source_source_first & (~liteethmaccore_tx_converter_last_be_drop));
assign liteethmaccore_tx_converter_source_last = (liteethmaccore_tx_converter_source_source_last | liteethmaccore_tx_converter_last_be_packet_end);
assign liteethmaccore_tx_converter_source_source_ready = (liteethmaccore_tx_converter_source_ready | liteethmaccore_tx_converter_last_be_drop);
assign {liteethmaccore_tx_converter_source_payload_error, liteethmaccore_tx_converter_source_payload_last_be, liteethmaccore_tx_converter_source_payload_data} = liteethmaccore_tx_converter_source_source_payload_data;
assign liteethmaccore_tx_converter_source_source_valid = liteethmaccore_tx_converter_converter_source_valid;
assign liteethmaccore_tx_converter_converter_source_ready = liteethmaccore_tx_converter_source_source_ready;
assign liteethmaccore_tx_converter_source_source_first = liteethmaccore_tx_converter_converter_source_first;
assign liteethmaccore_tx_converter_source_source_last = liteethmaccore_tx_converter_converter_source_last;
assign liteethmaccore_tx_converter_source_source_payload_data = liteethmaccore_tx_converter_converter_source_payload_data;
assign liteethmaccore_tx_converter_converter_first = (liteethmaccore_tx_converter_converter_mux == 1'd0);
assign liteethmaccore_tx_converter_converter_last = (liteethmaccore_tx_converter_converter_mux == 3'd7);
assign liteethmaccore_tx_converter_converter_source_valid = liteethmaccore_tx_converter_converter_sink_valid;
assign liteethmaccore_tx_converter_converter_source_first = (liteethmaccore_tx_converter_converter_sink_first & liteethmaccore_tx_converter_converter_first);
assign liteethmaccore_tx_converter_converter_source_last = (liteethmaccore_tx_converter_converter_sink_last & liteethmaccore_tx_converter_converter_last);
assign liteethmaccore_tx_converter_converter_sink_ready = (liteethmaccore_tx_converter_converter_last & liteethmaccore_tx_converter_converter_source_ready);

// synthesis translate_off
reg dummy_d_4;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_converter_converter_source_payload_data <= 10'd0;
	case (liteethmaccore_tx_converter_converter_mux)
		1'd0: begin
			liteethmaccore_tx_converter_converter_source_payload_data <= liteethmaccore_tx_converter_converter_sink_payload_data[9:0];
		end
		1'd1: begin
			liteethmaccore_tx_converter_converter_source_payload_data <= liteethmaccore_tx_converter_converter_sink_payload_data[19:10];
		end
		2'd2: begin
			liteethmaccore_tx_converter_converter_source_payload_data <= liteethmaccore_tx_converter_converter_sink_payload_data[29:20];
		end
		2'd3: begin
			liteethmaccore_tx_converter_converter_source_payload_data <= liteethmaccore_tx_converter_converter_sink_payload_data[39:30];
		end
		3'd4: begin
			liteethmaccore_tx_converter_converter_source_payload_data <= liteethmaccore_tx_converter_converter_sink_payload_data[49:40];
		end
		3'd5: begin
			liteethmaccore_tx_converter_converter_source_payload_data <= liteethmaccore_tx_converter_converter_sink_payload_data[59:50];
		end
		3'd6: begin
			liteethmaccore_tx_converter_converter_source_payload_data <= liteethmaccore_tx_converter_converter_sink_payload_data[69:60];
		end
		default: begin
			liteethmaccore_tx_converter_converter_source_payload_data <= liteethmaccore_tx_converter_converter_sink_payload_data[79:70];
		end
	endcase
// synthesis translate_off
	dummy_d_4 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_tx_converter_converter_source_payload_valid_token_count = liteethmaccore_tx_converter_converter_last;
assign liteethmaccore_tx_last_be_last_handler_sink_valid = liteethmaccore_tx_last_be_sink_sink_valid;
assign liteethmaccore_tx_last_be_sink_sink_ready = liteethmaccore_tx_last_be_last_handler_sink_ready;
assign liteethmaccore_tx_last_be_last_handler_sink_first = liteethmaccore_tx_last_be_sink_sink_first;
assign liteethmaccore_tx_last_be_last_handler_sink_last = liteethmaccore_tx_last_be_sink_sink_last;
assign liteethmaccore_tx_last_be_last_handler_sink_payload_data = liteethmaccore_tx_last_be_sink_sink_payload_data;
assign liteethmaccore_tx_last_be_last_handler_sink_payload_last_be = liteethmaccore_tx_last_be_sink_sink_payload_last_be;
assign liteethmaccore_tx_last_be_last_handler_sink_payload_error = liteethmaccore_tx_last_be_sink_sink_payload_error;
assign liteethmaccore_tx_last_be_source_source_valid = liteethmaccore_tx_last_be_last_handler_source_valid;
assign liteethmaccore_tx_last_be_last_handler_source_ready = liteethmaccore_tx_last_be_source_source_ready;
assign liteethmaccore_tx_last_be_source_source_first = liteethmaccore_tx_last_be_last_handler_source_first;
assign liteethmaccore_tx_last_be_source_source_last = liteethmaccore_tx_last_be_last_handler_source_last;
assign liteethmaccore_tx_last_be_source_source_payload_data = liteethmaccore_tx_last_be_last_handler_source_payload_data;
assign liteethmaccore_tx_last_be_source_source_payload_last_be = liteethmaccore_tx_last_be_last_handler_source_payload_last_be;
assign liteethmaccore_tx_last_be_source_source_payload_error = liteethmaccore_tx_last_be_last_handler_source_payload_error;

// synthesis translate_off
reg dummy_d_5;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_last_be_last_handler_sink_ready <= 1'd0;
	liteethmaccore_tx_last_be_last_handler_source_valid <= 1'd0;
	liteethmaccore_tx_last_be_last_handler_source_first <= 1'd0;
	liteethmaccore_tx_last_be_last_handler_source_last <= 1'd0;
	liteethmaccore_tx_last_be_last_handler_source_payload_data <= 8'd0;
	liteethmaccore_tx_last_be_last_handler_source_payload_last_be <= 1'd0;
	liteethmaccore_tx_last_be_last_handler_source_payload_error <= 1'd0;
	txdatapath_liteethmactxlastbe_next_state <= 1'd0;
	txdatapath_liteethmactxlastbe_next_state <= txdatapath_liteethmactxlastbe_state;
	case (txdatapath_liteethmactxlastbe_state)
		1'd1: begin
			liteethmaccore_tx_last_be_last_handler_sink_ready <= 1'd1;
			if ((liteethmaccore_tx_last_be_last_handler_sink_valid & liteethmaccore_tx_last_be_last_handler_sink_last)) begin
				txdatapath_liteethmactxlastbe_next_state <= 1'd0;
			end
		end
		default: begin
			liteethmaccore_tx_last_be_last_handler_source_valid <= liteethmaccore_tx_last_be_last_handler_sink_valid;
			liteethmaccore_tx_last_be_last_handler_sink_ready <= liteethmaccore_tx_last_be_last_handler_source_ready;
			liteethmaccore_tx_last_be_last_handler_source_first <= liteethmaccore_tx_last_be_last_handler_sink_first;
			liteethmaccore_tx_last_be_last_handler_source_last <= liteethmaccore_tx_last_be_last_handler_sink_last;
			liteethmaccore_tx_last_be_last_handler_source_payload_data <= liteethmaccore_tx_last_be_last_handler_sink_payload_data;
			liteethmaccore_tx_last_be_last_handler_source_payload_last_be <= liteethmaccore_tx_last_be_last_handler_sink_payload_last_be;
			liteethmaccore_tx_last_be_last_handler_source_payload_error <= liteethmaccore_tx_last_be_last_handler_sink_payload_error;
			liteethmaccore_tx_last_be_last_handler_source_last <= (liteethmaccore_tx_last_be_last_handler_sink_payload_last_be != 1'd0);
			if ((liteethmaccore_tx_last_be_last_handler_sink_valid & liteethmaccore_tx_last_be_last_handler_sink_ready)) begin
				if ((liteethmaccore_tx_last_be_last_handler_source_last & (~liteethmaccore_tx_last_be_last_handler_sink_last))) begin
					txdatapath_liteethmactxlastbe_next_state <= 1'd1;
				end
			end
		end
	endcase
// synthesis translate_off
	dummy_d_5 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_tx_padding_counter_done = (liteethmaccore_tx_padding_counter >= 6'd59);

// synthesis translate_off
reg dummy_d_6;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_padding_sink_ready <= 1'd0;
	liteethmaccore_tx_padding_source_valid <= 1'd0;
	liteethmaccore_tx_padding_source_first <= 1'd0;
	liteethmaccore_tx_padding_source_last <= 1'd0;
	liteethmaccore_tx_padding_source_payload_data <= 8'd0;
	liteethmaccore_tx_padding_source_payload_last_be <= 1'd0;
	liteethmaccore_tx_padding_source_payload_error <= 1'd0;
	txdatapath_liteethmacpaddinginserter_next_state <= 1'd0;
	liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value <= 16'd0;
	liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd0;
	txdatapath_liteethmacpaddinginserter_next_state <= txdatapath_liteethmacpaddinginserter_state;
	case (txdatapath_liteethmacpaddinginserter_state)
		1'd1: begin
			liteethmaccore_tx_padding_source_valid <= 1'd1;
			if (liteethmaccore_tx_padding_counter_done) begin
				liteethmaccore_tx_padding_source_payload_last_be <= 1'd1;
				liteethmaccore_tx_padding_source_last <= 1'd1;
			end
			liteethmaccore_tx_padding_source_payload_data <= 1'd0;
			if ((liteethmaccore_tx_padding_source_valid & liteethmaccore_tx_padding_source_ready)) begin
				liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value <= (liteethmaccore_tx_padding_counter + 1'd1);
				liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd1;
				if (liteethmaccore_tx_padding_counter_done) begin
					liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value <= 1'd0;
					liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd1;
					txdatapath_liteethmacpaddinginserter_next_state <= 1'd0;
				end
			end
		end
		default: begin
			liteethmaccore_tx_padding_source_valid <= liteethmaccore_tx_padding_sink_valid;
			liteethmaccore_tx_padding_sink_ready <= liteethmaccore_tx_padding_source_ready;
			liteethmaccore_tx_padding_source_first <= liteethmaccore_tx_padding_sink_first;
			liteethmaccore_tx_padding_source_last <= liteethmaccore_tx_padding_sink_last;
			liteethmaccore_tx_padding_source_payload_data <= liteethmaccore_tx_padding_sink_payload_data;
			liteethmaccore_tx_padding_source_payload_last_be <= liteethmaccore_tx_padding_sink_payload_last_be;
			liteethmaccore_tx_padding_source_payload_error <= liteethmaccore_tx_padding_sink_payload_error;
			if ((liteethmaccore_tx_padding_source_valid & liteethmaccore_tx_padding_source_ready)) begin
				liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value <= (liteethmaccore_tx_padding_counter + 1'd1);
				liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd1;
				if (liteethmaccore_tx_padding_sink_last) begin
					if ((~liteethmaccore_tx_padding_counter_done)) begin
						liteethmaccore_tx_padding_source_last <= 1'd0;
						liteethmaccore_tx_padding_source_payload_last_be <= 1'd0;
						txdatapath_liteethmacpaddinginserter_next_state <= 1'd1;
					end else begin
						if (((liteethmaccore_tx_padding_counter == 6'd59) & (liteethmaccore_tx_padding_sink_payload_last_be < 1'd1))) begin
							liteethmaccore_tx_padding_source_payload_last_be <= 1'd1;
						end else begin
							liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value <= 1'd0;
							liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd1;
						end
					end
				end
			end
		end
	endcase
// synthesis translate_off
	dummy_d_6 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_tx_crc_data0 = liteethmaccore_tx_crc_sink_payload_data;
assign liteethmaccore_tx_crc_be = liteethmaccore_tx_crc_sink_payload_last_be;
assign liteethmaccore_tx_crc_cnt_done = (liteethmaccore_tx_crc_cnt == 1'd0);
assign liteethmaccore_tx_crc_sink_valid = liteethmaccore_tx_crc_source_source_valid;
assign liteethmaccore_tx_crc_source_source_ready = liteethmaccore_tx_crc_sink_ready;
assign liteethmaccore_tx_crc_sink_first = liteethmaccore_tx_crc_source_source_first;
assign liteethmaccore_tx_crc_sink_last = liteethmaccore_tx_crc_source_source_last;
assign liteethmaccore_tx_crc_sink_payload_data = liteethmaccore_tx_crc_source_source_payload_data;
assign liteethmaccore_tx_crc_sink_payload_last_be = liteethmaccore_tx_crc_source_source_payload_last_be;
assign liteethmaccore_tx_crc_sink_payload_error = liteethmaccore_tx_crc_source_source_payload_error;
assign liteethmaccore_tx_crc_data1 = liteethmaccore_tx_crc_data0;
assign liteethmaccore_tx_crc_crc_prev = liteethmaccore_tx_crc_reg;

// synthesis translate_off
reg dummy_d_7;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_crc_value <= 32'd0;
	liteethmaccore_tx_crc_error <= 1'd0;
	if (liteethmaccore_tx_crc_be) begin
		liteethmaccore_tx_crc_value <= ({liteethmaccore_tx_crc_crc_next[0], liteethmaccore_tx_crc_crc_next[1], liteethmaccore_tx_crc_crc_next[2], liteethmaccore_tx_crc_crc_next[3], liteethmaccore_tx_crc_crc_next[4], liteethmaccore_tx_crc_crc_next[5], liteethmaccore_tx_crc_crc_next[6], liteethmaccore_tx_crc_crc_next[7], liteethmaccore_tx_crc_crc_next[8], liteethmaccore_tx_crc_crc_next[9], liteethmaccore_tx_crc_crc_next[10], liteethmaccore_tx_crc_crc_next[11], liteethmaccore_tx_crc_crc_next[12], liteethmaccore_tx_crc_crc_next[13], liteethmaccore_tx_crc_crc_next[14], liteethmaccore_tx_crc_crc_next[15], liteethmaccore_tx_crc_crc_next[16], liteethmaccore_tx_crc_crc_next[17], liteethmaccore_tx_crc_crc_next[18], liteethmaccore_tx_crc_crc_next[19], liteethmaccore_tx_crc_crc_next[20], liteethmaccore_tx_crc_crc_next[21], liteethmaccore_tx_crc_crc_next[22], liteethmaccore_tx_crc_crc_next[23], liteethmaccore_tx_crc_crc_next[24], liteethmaccore_tx_crc_crc_next[25], liteethmaccore_tx_crc_crc_next[26], liteethmaccore_tx_crc_crc_next[27], liteethmaccore_tx_crc_crc_next[28], liteethmaccore_tx_crc_crc_next[29], liteethmaccore_tx_crc_crc_next[30], liteethmaccore_tx_crc_crc_next[31]} ^ 32'd4294967295);
		liteethmaccore_tx_crc_error <= (liteethmaccore_tx_crc_crc_next != 32'd3338984827);
	end
// synthesis translate_off
	dummy_d_7 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_8;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_crc_crc_next <= 32'd0;
	liteethmaccore_tx_crc_crc_next[0] <= (((liteethmaccore_tx_crc_crc_prev[24] ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[1] <= (((((((liteethmaccore_tx_crc_crc_prev[25] ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_data1[6]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[2] <= (((((((((liteethmaccore_tx_crc_crc_prev[26] ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_data1[6]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[3] <= (((((((liteethmaccore_tx_crc_crc_prev[27] ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_data1[6]);
	liteethmaccore_tx_crc_crc_next[4] <= (((((((((liteethmaccore_tx_crc_crc_prev[28] ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[5] <= (((((((((((((liteethmaccore_tx_crc_crc_prev[29] ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_data1[6]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[6] <= (((((((((((liteethmaccore_tx_crc_crc_prev[30] ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_data1[6]);
	liteethmaccore_tx_crc_crc_next[7] <= (((((((((liteethmaccore_tx_crc_crc_prev[31] ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[8] <= ((((((((liteethmaccore_tx_crc_crc_prev[0] ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_data1[6]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[9] <= ((((((((liteethmaccore_tx_crc_crc_prev[1] ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_data1[6]);
	liteethmaccore_tx_crc_crc_next[10] <= ((((((((liteethmaccore_tx_crc_crc_prev[2] ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[11] <= ((((((((liteethmaccore_tx_crc_crc_prev[3] ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_data1[6]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[12] <= ((((((((((((liteethmaccore_tx_crc_crc_prev[4] ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_data1[6]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[13] <= ((((((((((((liteethmaccore_tx_crc_crc_prev[5] ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_data1[6]);
	liteethmaccore_tx_crc_crc_next[14] <= ((((((((((liteethmaccore_tx_crc_crc_prev[6] ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]);
	liteethmaccore_tx_crc_crc_next[15] <= ((((((((liteethmaccore_tx_crc_crc_prev[7] ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]);
	liteethmaccore_tx_crc_crc_next[16] <= ((((((liteethmaccore_tx_crc_crc_prev[8] ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[17] <= ((((((liteethmaccore_tx_crc_crc_prev[9] ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_data1[6]);
	liteethmaccore_tx_crc_crc_next[18] <= ((((((liteethmaccore_tx_crc_crc_prev[10] ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]);
	liteethmaccore_tx_crc_crc_next[19] <= ((((liteethmaccore_tx_crc_crc_prev[11] ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]);
	liteethmaccore_tx_crc_crc_next[20] <= ((liteethmaccore_tx_crc_crc_prev[12] ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]);
	liteethmaccore_tx_crc_crc_next[21] <= ((liteethmaccore_tx_crc_crc_prev[13] ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]);
	liteethmaccore_tx_crc_crc_next[22] <= ((liteethmaccore_tx_crc_crc_prev[14] ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[23] <= ((((((liteethmaccore_tx_crc_crc_prev[15] ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_data1[6]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[24] <= ((((((liteethmaccore_tx_crc_crc_prev[16] ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_data1[6]);
	liteethmaccore_tx_crc_crc_next[25] <= ((((liteethmaccore_tx_crc_crc_prev[17] ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]);
	liteethmaccore_tx_crc_crc_next[26] <= ((((((((liteethmaccore_tx_crc_crc_prev[18] ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]) ^ liteethmaccore_tx_crc_crc_prev[24]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_data1[7]);
	liteethmaccore_tx_crc_crc_next[27] <= ((((((((liteethmaccore_tx_crc_crc_prev[19] ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]) ^ liteethmaccore_tx_crc_crc_prev[25]) ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_data1[6]);
	liteethmaccore_tx_crc_crc_next[28] <= ((((((liteethmaccore_tx_crc_crc_prev[20] ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]) ^ liteethmaccore_tx_crc_crc_prev[26]) ^ liteethmaccore_tx_crc_data1[5]);
	liteethmaccore_tx_crc_crc_next[29] <= ((((((liteethmaccore_tx_crc_crc_prev[21] ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_crc_prev[30]) ^ liteethmaccore_tx_crc_data1[1]) ^ liteethmaccore_tx_crc_crc_prev[27]) ^ liteethmaccore_tx_crc_data1[4]);
	liteethmaccore_tx_crc_crc_next[30] <= ((((liteethmaccore_tx_crc_crc_prev[22] ^ liteethmaccore_tx_crc_crc_prev[31]) ^ liteethmaccore_tx_crc_data1[0]) ^ liteethmaccore_tx_crc_crc_prev[28]) ^ liteethmaccore_tx_crc_data1[3]);
	liteethmaccore_tx_crc_crc_next[31] <= ((liteethmaccore_tx_crc_crc_prev[23] ^ liteethmaccore_tx_crc_crc_prev[29]) ^ liteethmaccore_tx_crc_data1[2]);
// synthesis translate_off
	dummy_d_8 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_9;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_crc_sink_ready <= 1'd0;
	liteethmaccore_tx_crc_source_valid <= 1'd0;
	liteethmaccore_tx_crc_source_first <= 1'd0;
	liteethmaccore_tx_crc_source_last <= 1'd0;
	liteethmaccore_tx_crc_source_payload_data <= 8'd0;
	liteethmaccore_tx_crc_source_payload_last_be <= 1'd0;
	liteethmaccore_tx_crc_source_payload_error <= 1'd0;
	liteethmaccore_tx_crc_ce <= 1'd0;
	liteethmaccore_tx_crc_reset <= 1'd0;
	liteethmaccore_tx_crc_is_ongoing0 <= 1'd0;
	liteethmaccore_tx_crc_is_ongoing1 <= 1'd0;
	txdatapath_bufferizeendpoints_next_state <= 2'd0;
	liteethmaccore_tx_crc_crc_packet_clockdomainsrenamer1_next_value0 <= 32'd0;
	liteethmaccore_tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0 <= 1'd0;
	liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value1 <= 1'd0;
	liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value_ce1 <= 1'd0;
	txdatapath_bufferizeendpoints_next_state <= txdatapath_bufferizeendpoints_state;
	case (txdatapath_bufferizeendpoints_state)
		1'd1: begin
			liteethmaccore_tx_crc_ce <= (liteethmaccore_tx_crc_sink_valid & liteethmaccore_tx_crc_source_ready);
			liteethmaccore_tx_crc_source_valid <= liteethmaccore_tx_crc_sink_valid;
			liteethmaccore_tx_crc_sink_ready <= liteethmaccore_tx_crc_source_ready;
			liteethmaccore_tx_crc_source_first <= liteethmaccore_tx_crc_sink_first;
			liteethmaccore_tx_crc_source_last <= liteethmaccore_tx_crc_sink_last;
			liteethmaccore_tx_crc_source_payload_data <= liteethmaccore_tx_crc_sink_payload_data;
			liteethmaccore_tx_crc_source_payload_last_be <= liteethmaccore_tx_crc_sink_payload_last_be;
			liteethmaccore_tx_crc_source_payload_error <= liteethmaccore_tx_crc_sink_payload_error;
			liteethmaccore_tx_crc_source_last <= 1'd0;
			liteethmaccore_tx_crc_source_payload_last_be <= 1'd0;
			if (liteethmaccore_tx_crc_sink_last) begin
				if (liteethmaccore_tx_crc_sink_payload_last_be) begin
					liteethmaccore_tx_crc_source_payload_data <= slice_proxy[7:0];
				end
				if ((1'd0 & (liteethmaccore_tx_crc_sink_payload_last_be <= 4'd15))) begin
					liteethmaccore_tx_crc_source_last <= 1'd1;
					liteethmaccore_tx_crc_source_payload_last_be <= (liteethmaccore_tx_crc_sink_payload_last_be <<< 3'sd5);
				end
			end
			if (((liteethmaccore_tx_crc_sink_valid & liteethmaccore_tx_crc_sink_last) & liteethmaccore_tx_crc_source_ready)) begin
				if ((1'd0 & (liteethmaccore_tx_crc_sink_payload_last_be <= 4'd15))) begin
					txdatapath_bufferizeendpoints_next_state <= 1'd0;
				end else begin
					liteethmaccore_tx_crc_crc_packet_clockdomainsrenamer1_next_value0 <= liteethmaccore_tx_crc_value;
					liteethmaccore_tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0 <= 1'd1;
					if (1'd0) begin
						liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value1 <= (liteethmaccore_tx_crc_sink_payload_last_be >>> 3'd4);
						liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value_ce1 <= 1'd1;
					end else begin
						liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value1 <= liteethmaccore_tx_crc_sink_payload_last_be;
						liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value_ce1 <= 1'd1;
					end
					txdatapath_bufferizeendpoints_next_state <= 2'd2;
				end
			end
		end
		2'd2: begin
			liteethmaccore_tx_crc_source_valid <= 1'd1;
			case (liteethmaccore_tx_crc_cnt)
				1'd0: begin
					liteethmaccore_tx_crc_source_payload_data <= liteethmaccore_tx_crc_crc_packet[31:24];
				end
				1'd1: begin
					liteethmaccore_tx_crc_source_payload_data <= liteethmaccore_tx_crc_crc_packet[23:16];
				end
				2'd2: begin
					liteethmaccore_tx_crc_source_payload_data <= liteethmaccore_tx_crc_crc_packet[15:8];
				end
				default: begin
					liteethmaccore_tx_crc_source_payload_data <= liteethmaccore_tx_crc_crc_packet[7:0];
				end
			endcase
			if (liteethmaccore_tx_crc_cnt_done) begin
				liteethmaccore_tx_crc_source_last <= 1'd1;
				if (liteethmaccore_tx_crc_source_ready) begin
					txdatapath_bufferizeendpoints_next_state <= 1'd0;
				end
			end
			liteethmaccore_tx_crc_is_ongoing1 <= 1'd1;
		end
		default: begin
			liteethmaccore_tx_crc_reset <= 1'd1;
			liteethmaccore_tx_crc_sink_ready <= 1'd1;
			if (liteethmaccore_tx_crc_sink_valid) begin
				liteethmaccore_tx_crc_sink_ready <= 1'd0;
				txdatapath_bufferizeendpoints_next_state <= 1'd1;
			end
			liteethmaccore_tx_crc_is_ongoing0 <= 1'd1;
		end
	endcase
// synthesis translate_off
	dummy_d_9 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_tx_crc_pipe_valid_sink_ready = ((~liteethmaccore_tx_crc_pipe_valid_source_valid) | liteethmaccore_tx_crc_pipe_valid_source_ready);
assign liteethmaccore_tx_crc_pipe_valid_sink_valid = liteethmaccore_tx_crc_sink_sink_valid;
assign liteethmaccore_tx_crc_sink_sink_ready = liteethmaccore_tx_crc_pipe_valid_sink_ready;
assign liteethmaccore_tx_crc_pipe_valid_sink_first = liteethmaccore_tx_crc_sink_sink_first;
assign liteethmaccore_tx_crc_pipe_valid_sink_last = liteethmaccore_tx_crc_sink_sink_last;
assign liteethmaccore_tx_crc_pipe_valid_sink_payload_data = liteethmaccore_tx_crc_sink_sink_payload_data;
assign liteethmaccore_tx_crc_pipe_valid_sink_payload_last_be = liteethmaccore_tx_crc_sink_sink_payload_last_be;
assign liteethmaccore_tx_crc_pipe_valid_sink_payload_error = liteethmaccore_tx_crc_sink_sink_payload_error;
assign liteethmaccore_tx_crc_source_source_valid = liteethmaccore_tx_crc_pipe_valid_source_valid;
assign liteethmaccore_tx_crc_pipe_valid_source_ready = liteethmaccore_tx_crc_source_source_ready;
assign liteethmaccore_tx_crc_source_source_first = liteethmaccore_tx_crc_pipe_valid_source_first;
assign liteethmaccore_tx_crc_source_source_last = liteethmaccore_tx_crc_pipe_valid_source_last;
assign liteethmaccore_tx_crc_source_source_payload_data = liteethmaccore_tx_crc_pipe_valid_source_payload_data;
assign liteethmaccore_tx_crc_source_source_payload_last_be = liteethmaccore_tx_crc_pipe_valid_source_payload_last_be;
assign liteethmaccore_tx_crc_source_source_payload_error = liteethmaccore_tx_crc_pipe_valid_source_payload_error;
assign liteethmaccore_tx_preamble_source_payload_last_be = liteethmaccore_tx_preamble_sink_payload_last_be;

// synthesis translate_off
reg dummy_d_10;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_preamble_sink_ready <= 1'd0;
	liteethmaccore_tx_preamble_source_valid <= 1'd0;
	liteethmaccore_tx_preamble_source_first <= 1'd0;
	liteethmaccore_tx_preamble_source_last <= 1'd0;
	liteethmaccore_tx_preamble_source_payload_data <= 8'd0;
	liteethmaccore_tx_preamble_source_payload_error <= 1'd0;
	txdatapath_liteethmacpreambleinserter_next_state <= 2'd0;
	liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value <= 3'd0;
	liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value_ce <= 1'd0;
	liteethmaccore_tx_preamble_source_payload_data <= liteethmaccore_tx_preamble_sink_payload_data;
	txdatapath_liteethmacpreambleinserter_next_state <= txdatapath_liteethmacpreambleinserter_state;
	case (txdatapath_liteethmacpreambleinserter_state)
		1'd1: begin
			liteethmaccore_tx_preamble_source_valid <= 1'd1;
			case (liteethmaccore_tx_preamble_count)
				1'd0: begin
					liteethmaccore_tx_preamble_source_payload_data <= liteethmaccore_tx_preamble_preamble[7:0];
				end
				1'd1: begin
					liteethmaccore_tx_preamble_source_payload_data <= liteethmaccore_tx_preamble_preamble[15:8];
				end
				2'd2: begin
					liteethmaccore_tx_preamble_source_payload_data <= liteethmaccore_tx_preamble_preamble[23:16];
				end
				2'd3: begin
					liteethmaccore_tx_preamble_source_payload_data <= liteethmaccore_tx_preamble_preamble[31:24];
				end
				3'd4: begin
					liteethmaccore_tx_preamble_source_payload_data <= liteethmaccore_tx_preamble_preamble[39:32];
				end
				3'd5: begin
					liteethmaccore_tx_preamble_source_payload_data <= liteethmaccore_tx_preamble_preamble[47:40];
				end
				3'd6: begin
					liteethmaccore_tx_preamble_source_payload_data <= liteethmaccore_tx_preamble_preamble[55:48];
				end
				default: begin
					liteethmaccore_tx_preamble_source_payload_data <= liteethmaccore_tx_preamble_preamble[63:56];
				end
			endcase
			if (liteethmaccore_tx_preamble_source_ready) begin
				if ((liteethmaccore_tx_preamble_count == 3'd7)) begin
					txdatapath_liteethmacpreambleinserter_next_state <= 2'd2;
				end else begin
					liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value <= (liteethmaccore_tx_preamble_count + 1'd1);
					liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value_ce <= 1'd1;
				end
			end
		end
		2'd2: begin
			liteethmaccore_tx_preamble_source_valid <= liteethmaccore_tx_preamble_sink_valid;
			liteethmaccore_tx_preamble_sink_ready <= liteethmaccore_tx_preamble_source_ready;
			liteethmaccore_tx_preamble_source_first <= liteethmaccore_tx_preamble_sink_first;
			liteethmaccore_tx_preamble_source_last <= liteethmaccore_tx_preamble_sink_last;
			liteethmaccore_tx_preamble_source_payload_error <= liteethmaccore_tx_preamble_sink_payload_error;
			if (((liteethmaccore_tx_preamble_sink_valid & liteethmaccore_tx_preamble_sink_last) & liteethmaccore_tx_preamble_source_ready)) begin
				txdatapath_liteethmacpreambleinserter_next_state <= 1'd0;
			end
		end
		default: begin
			liteethmaccore_tx_preamble_sink_ready <= 1'd1;
			liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value <= 1'd0;
			liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value_ce <= 1'd1;
			if (liteethmaccore_tx_preamble_sink_valid) begin
				liteethmaccore_tx_preamble_sink_ready <= 1'd0;
				txdatapath_liteethmacpreambleinserter_next_state <= 1'd1;
			end
		end
	endcase
// synthesis translate_off
	dummy_d_10 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_11;
// synthesis translate_on
always @(*) begin
	liteethmaccore_tx_gap_sink_ready <= 1'd0;
	liteethmaccore_tx_gap_source_valid <= 1'd0;
	liteethmaccore_tx_gap_source_first <= 1'd0;
	liteethmaccore_tx_gap_source_last <= 1'd0;
	liteethmaccore_tx_gap_source_payload_data <= 8'd0;
	liteethmaccore_tx_gap_source_payload_last_be <= 1'd0;
	liteethmaccore_tx_gap_source_payload_error <= 1'd0;
	txdatapath_liteethmacgap_next_state <= 1'd0;
	liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value <= 4'd0;
	liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value_ce <= 1'd0;
	txdatapath_liteethmacgap_next_state <= txdatapath_liteethmacgap_state;
	case (txdatapath_liteethmacgap_state)
		1'd1: begin
			liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value <= (liteethmaccore_tx_gap_counter - 1'd1);
			liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value_ce <= 1'd1;
			if ((liteethmaccore_tx_gap_counter == 1'd1)) begin
				txdatapath_liteethmacgap_next_state <= 1'd0;
			end
		end
		default: begin
			liteethmaccore_tx_gap_source_valid <= liteethmaccore_tx_gap_sink_valid;
			liteethmaccore_tx_gap_sink_ready <= liteethmaccore_tx_gap_source_ready;
			liteethmaccore_tx_gap_source_first <= liteethmaccore_tx_gap_sink_first;
			liteethmaccore_tx_gap_source_last <= liteethmaccore_tx_gap_sink_last;
			liteethmaccore_tx_gap_source_payload_data <= liteethmaccore_tx_gap_sink_payload_data;
			liteethmaccore_tx_gap_source_payload_last_be <= liteethmaccore_tx_gap_sink_payload_last_be;
			liteethmaccore_tx_gap_source_payload_error <= liteethmaccore_tx_gap_sink_payload_error;
			if (((liteethmaccore_tx_gap_sink_valid & liteethmaccore_tx_gap_sink_last) & liteethmaccore_tx_gap_sink_ready)) begin
				liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value <= 4'd12;
				liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value_ce <= 1'd1;
				txdatapath_liteethmacgap_next_state <= 1'd1;
			end
		end
	endcase
// synthesis translate_off
	dummy_d_11 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_tx_cdc_sink_sink_valid = liteethmaccore_sink_valid;
assign liteethmaccore_sink_ready = liteethmaccore_tx_cdc_sink_sink_ready;
assign liteethmaccore_tx_cdc_sink_sink_first = liteethmaccore_sink_first;
assign liteethmaccore_tx_cdc_sink_sink_last = liteethmaccore_sink_last;
assign liteethmaccore_tx_cdc_sink_sink_payload_data = liteethmaccore_sink_payload_data;
assign liteethmaccore_tx_cdc_sink_sink_payload_last_be = liteethmaccore_sink_payload_last_be;
assign liteethmaccore_tx_cdc_sink_sink_payload_error = liteethmaccore_sink_payload_error;
assign liteethmaccore_tx_converter_sink_valid = liteethmaccore_tx_cdc_source_source_valid;
assign liteethmaccore_tx_cdc_source_source_ready = liteethmaccore_tx_converter_sink_ready;
assign liteethmaccore_tx_converter_sink_first = liteethmaccore_tx_cdc_source_source_first;
assign liteethmaccore_tx_converter_sink_last = liteethmaccore_tx_cdc_source_source_last;
assign liteethmaccore_tx_converter_sink_payload_data = liteethmaccore_tx_cdc_source_source_payload_data;
assign liteethmaccore_tx_converter_sink_payload_last_be = liteethmaccore_tx_cdc_source_source_payload_last_be;
assign liteethmaccore_tx_converter_sink_payload_error = liteethmaccore_tx_cdc_source_source_payload_error;
assign liteethmaccore_tx_last_be_sink_sink_valid = liteethmaccore_tx_converter_source_valid;
assign liteethmaccore_tx_converter_source_ready = liteethmaccore_tx_last_be_sink_sink_ready;
assign liteethmaccore_tx_last_be_sink_sink_first = liteethmaccore_tx_converter_source_first;
assign liteethmaccore_tx_last_be_sink_sink_last = liteethmaccore_tx_converter_source_last;
assign liteethmaccore_tx_last_be_sink_sink_payload_data = liteethmaccore_tx_converter_source_payload_data;
assign liteethmaccore_tx_last_be_sink_sink_payload_last_be = liteethmaccore_tx_converter_source_payload_last_be;
assign liteethmaccore_tx_last_be_sink_sink_payload_error = liteethmaccore_tx_converter_source_payload_error;
assign liteethmaccore_tx_padding_sink_valid = liteethmaccore_tx_last_be_source_source_valid;
assign liteethmaccore_tx_last_be_source_source_ready = liteethmaccore_tx_padding_sink_ready;
assign liteethmaccore_tx_padding_sink_first = liteethmaccore_tx_last_be_source_source_first;
assign liteethmaccore_tx_padding_sink_last = liteethmaccore_tx_last_be_source_source_last;
assign liteethmaccore_tx_padding_sink_payload_data = liteethmaccore_tx_last_be_source_source_payload_data;
assign liteethmaccore_tx_padding_sink_payload_last_be = liteethmaccore_tx_last_be_source_source_payload_last_be;
assign liteethmaccore_tx_padding_sink_payload_error = liteethmaccore_tx_last_be_source_source_payload_error;
assign liteethmaccore_tx_crc_sink_sink_valid = liteethmaccore_tx_padding_source_valid;
assign liteethmaccore_tx_padding_source_ready = liteethmaccore_tx_crc_sink_sink_ready;
assign liteethmaccore_tx_crc_sink_sink_first = liteethmaccore_tx_padding_source_first;
assign liteethmaccore_tx_crc_sink_sink_last = liteethmaccore_tx_padding_source_last;
assign liteethmaccore_tx_crc_sink_sink_payload_data = liteethmaccore_tx_padding_source_payload_data;
assign liteethmaccore_tx_crc_sink_sink_payload_last_be = liteethmaccore_tx_padding_source_payload_last_be;
assign liteethmaccore_tx_crc_sink_sink_payload_error = liteethmaccore_tx_padding_source_payload_error;
assign liteethmaccore_tx_preamble_sink_valid = liteethmaccore_tx_crc_source_valid;
assign liteethmaccore_tx_crc_source_ready = liteethmaccore_tx_preamble_sink_ready;
assign liteethmaccore_tx_preamble_sink_first = liteethmaccore_tx_crc_source_first;
assign liteethmaccore_tx_preamble_sink_last = liteethmaccore_tx_crc_source_last;
assign liteethmaccore_tx_preamble_sink_payload_data = liteethmaccore_tx_crc_source_payload_data;
assign liteethmaccore_tx_preamble_sink_payload_last_be = liteethmaccore_tx_crc_source_payload_last_be;
assign liteethmaccore_tx_preamble_sink_payload_error = liteethmaccore_tx_crc_source_payload_error;
assign liteethmaccore_tx_gap_sink_valid = liteethmaccore_tx_preamble_source_valid;
assign liteethmaccore_tx_preamble_source_ready = liteethmaccore_tx_gap_sink_ready;
assign liteethmaccore_tx_gap_sink_first = liteethmaccore_tx_preamble_source_first;
assign liteethmaccore_tx_gap_sink_last = liteethmaccore_tx_preamble_source_last;
assign liteethmaccore_tx_gap_sink_payload_data = liteethmaccore_tx_preamble_source_payload_data;
assign liteethmaccore_tx_gap_sink_payload_last_be = liteethmaccore_tx_preamble_source_payload_last_be;
assign liteethmaccore_tx_gap_sink_payload_error = liteethmaccore_tx_preamble_source_payload_error;
assign phy_sink_valid1 = liteethmaccore_tx_gap_source_valid;
assign liteethmaccore_tx_gap_source_ready = phy_sink_ready1;
assign phy_sink_first = liteethmaccore_tx_gap_source_first;
assign phy_sink_last1 = liteethmaccore_tx_gap_source_last;
assign phy_sink_payload_data = liteethmaccore_tx_gap_source_payload_data;
assign phy_sink_payload_last_be = liteethmaccore_tx_gap_source_payload_last_be;
assign phy_sink_payload_error = liteethmaccore_tx_gap_source_payload_error;
assign liteethmaccore_pulsesynchronizer0_i = liteethmaccore_rx_preamble_error;
assign liteethmaccore_pulsesynchronizer1_i = liteethmaccore_liteethmaccrc32checker_error;
assign liteethmaccore_rx_preamble_source_payload_data = liteethmaccore_rx_preamble_sink_payload_data;
assign liteethmaccore_rx_preamble_source_payload_last_be = liteethmaccore_rx_preamble_sink_payload_last_be;

// synthesis translate_off
reg dummy_d_12;
// synthesis translate_on
always @(*) begin
	liteethmaccore_rx_preamble_sink_ready <= 1'd0;
	liteethmaccore_rx_preamble_source_valid <= 1'd0;
	liteethmaccore_rx_preamble_source_first <= 1'd0;
	liteethmaccore_rx_preamble_source_last <= 1'd0;
	liteethmaccore_rx_preamble_source_payload_error <= 1'd0;
	liteethmaccore_rx_preamble_error <= 1'd0;
	rxdatapath_liteethmacpreamblechecker_next_state <= 1'd0;
	rxdatapath_liteethmacpreamblechecker_next_state <= rxdatapath_liteethmacpreamblechecker_state;
	case (rxdatapath_liteethmacpreamblechecker_state)
		1'd1: begin
			liteethmaccore_rx_preamble_source_valid <= liteethmaccore_rx_preamble_sink_valid;
			liteethmaccore_rx_preamble_sink_ready <= liteethmaccore_rx_preamble_source_ready;
			liteethmaccore_rx_preamble_source_first <= liteethmaccore_rx_preamble_sink_first;
			liteethmaccore_rx_preamble_source_last <= liteethmaccore_rx_preamble_sink_last;
			liteethmaccore_rx_preamble_source_payload_error <= liteethmaccore_rx_preamble_sink_payload_error;
			if (((liteethmaccore_rx_preamble_source_valid & liteethmaccore_rx_preamble_source_last) & liteethmaccore_rx_preamble_source_ready)) begin
				rxdatapath_liteethmacpreamblechecker_next_state <= 1'd0;
			end
		end
		default: begin
			liteethmaccore_rx_preamble_sink_ready <= 1'd1;
			if (((liteethmaccore_rx_preamble_sink_valid & (~liteethmaccore_rx_preamble_sink_last)) & (liteethmaccore_rx_preamble_sink_payload_data == liteethmaccore_rx_preamble_preamble[63:56]))) begin
				rxdatapath_liteethmacpreamblechecker_next_state <= 1'd1;
			end
			if ((liteethmaccore_rx_preamble_sink_valid & liteethmaccore_rx_preamble_sink_last)) begin
				liteethmaccore_rx_preamble_error <= 1'd1;
			end
		end
	endcase
// synthesis translate_off
	dummy_d_12 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_pulsesynchronizer0_o = (liteethmaccore_pulsesynchronizer0_toggle_o ^ liteethmaccore_pulsesynchronizer0_toggle_o_r);
assign liteethmaccore_liteethmaccrc32checker_fifo_full = (liteethmaccore_liteethmaccrc32checker_syncfifo_level == 3'd4);
assign liteethmaccore_liteethmaccrc32checker_fifo_in = (liteethmaccore_liteethmaccrc32checker_sink_sink_valid & ((~liteethmaccore_liteethmaccrc32checker_fifo_full) | liteethmaccore_liteethmaccrc32checker_fifo_out));
assign liteethmaccore_liteethmaccrc32checker_fifo_out = (liteethmaccore_liteethmaccrc32checker_source_source_valid & liteethmaccore_liteethmaccrc32checker_source_source_ready);
assign liteethmaccore_liteethmaccrc32checker_syncfifo_sink_first = liteethmaccore_liteethmaccrc32checker_sink_sink_first;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_sink_last = liteethmaccore_liteethmaccrc32checker_sink_sink_last;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_sink_payload_data = liteethmaccore_liteethmaccrc32checker_sink_sink_payload_data;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_sink_payload_last_be = liteethmaccore_liteethmaccrc32checker_sink_sink_payload_last_be;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_sink_payload_error = liteethmaccore_liteethmaccrc32checker_sink_sink_payload_error;

// synthesis translate_off
reg dummy_d_13;
// synthesis translate_on
always @(*) begin
	liteethmaccore_liteethmaccrc32checker_syncfifo_sink_valid <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_syncfifo_sink_valid <= liteethmaccore_liteethmaccrc32checker_sink_sink_valid;
	liteethmaccore_liteethmaccrc32checker_syncfifo_sink_valid <= liteethmaccore_liteethmaccrc32checker_fifo_in;
// synthesis translate_off
	dummy_d_13 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_14;
// synthesis translate_on
always @(*) begin
	liteethmaccore_liteethmaccrc32checker_sink_sink_ready <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_sink_sink_ready <= liteethmaccore_liteethmaccrc32checker_syncfifo_sink_ready;
	liteethmaccore_liteethmaccrc32checker_sink_sink_ready <= liteethmaccore_liteethmaccrc32checker_fifo_in;
// synthesis translate_off
	dummy_d_14 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_liteethmaccrc32checker_crc_data0 = liteethmaccore_liteethmaccrc32checker_sink_sink_payload_data;
assign liteethmaccore_liteethmaccrc32checker_crc_be = liteethmaccore_liteethmaccrc32checker_sink_sink_payload_last_be;
assign liteethmaccore_liteethmaccrc32checker_source_source_first = liteethmaccore_liteethmaccrc32checker_syncfifo_source_first;
assign liteethmaccore_liteethmaccrc32checker_source_source_payload_data = liteethmaccore_liteethmaccrc32checker_syncfifo_source_payload_data;
assign liteethmaccore_liteethmaccrc32checker_sink_sink_valid = liteethmaccore_bufferizeendpoints_source_source_valid;
assign liteethmaccore_bufferizeendpoints_source_source_ready = liteethmaccore_liteethmaccrc32checker_sink_sink_ready;
assign liteethmaccore_liteethmaccrc32checker_sink_sink_first = liteethmaccore_bufferizeendpoints_source_source_first;
assign liteethmaccore_liteethmaccrc32checker_sink_sink_last = liteethmaccore_bufferizeendpoints_source_source_last;
assign liteethmaccore_liteethmaccrc32checker_sink_sink_payload_data = liteethmaccore_bufferizeendpoints_source_source_payload_data;
assign liteethmaccore_liteethmaccrc32checker_sink_sink_payload_last_be = liteethmaccore_bufferizeendpoints_source_source_payload_last_be;
assign liteethmaccore_liteethmaccrc32checker_sink_sink_payload_error = liteethmaccore_bufferizeendpoints_source_source_payload_error;
assign liteethmaccore_liteethmaccrc32checker_crc_crc_prev = liteethmaccore_liteethmaccrc32checker_crc_reg;

// synthesis translate_off
reg dummy_d_15;
// synthesis translate_on
always @(*) begin
	liteethmaccore_liteethmaccrc32checker_crc_error0 <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_crc_data1 <= 8'd0;
	liteethmaccore_liteethmaccrc32checker_crc_data1 <= liteethmaccore_liteethmaccrc32checker_crc_data0;
	if (liteethmaccore_liteethmaccrc32checker_crc_be) begin
		liteethmaccore_liteethmaccrc32checker_crc_data1 <= (liteethmaccore_liteethmaccrc32checker_crc_data0 & 8'd255);
		liteethmaccore_liteethmaccrc32checker_crc_error0 <= (liteethmaccore_liteethmaccrc32checker_crc_crc_next != 32'd3338984827);
	end
// synthesis translate_off
	dummy_d_15 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_16;
// synthesis translate_on
always @(*) begin
	liteethmaccore_liteethmaccrc32checker_crc_crc_next <= 32'd0;
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[0] <= (((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[1] <= (((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[2] <= (((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26] ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[3] <= (((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27] ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[4] <= (((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28] ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[5] <= (((((((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29] ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[6] <= (((((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30] ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[7] <= (((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31] ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[8] <= ((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[0] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[9] <= ((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[1] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[10] <= ((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[2] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[11] <= ((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[3] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[12] <= ((((((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[4] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[13] <= ((((((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[5] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[14] <= ((((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[6] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[15] <= ((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[7] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[16] <= ((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[8] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[17] <= ((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[9] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[18] <= ((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[10] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[19] <= ((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[11] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[20] <= ((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[12] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[21] <= ((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[13] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[22] <= ((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[14] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[23] <= ((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[15] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[24] <= ((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[16] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[25] <= ((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[17] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[26] <= ((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[18] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[7]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[27] <= ((((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[19] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[6]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[28] <= ((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[20] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[5]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[29] <= ((((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[21] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[4]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[30] <= ((((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[22] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[3]);
	liteethmaccore_liteethmaccrc32checker_crc_crc_next[31] <= ((liteethmaccore_liteethmaccrc32checker_crc_crc_prev[23] ^ liteethmaccore_liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccore_liteethmaccrc32checker_crc_data1[2]);
// synthesis translate_off
	dummy_d_16 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_din = {liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_last, liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_first, liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_payload_error, liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_payload_last_be, liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_payload_data};
assign {liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_last, liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_first, liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_payload_error, liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_payload_last_be, liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_payload_data} = liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_dout;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_sink_ready = liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_writable;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_we = liteethmaccore_liteethmaccrc32checker_syncfifo_sink_valid;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_first = liteethmaccore_liteethmaccrc32checker_syncfifo_sink_first;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_last = liteethmaccore_liteethmaccrc32checker_syncfifo_sink_last;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_payload_data = liteethmaccore_liteethmaccrc32checker_syncfifo_sink_payload_data;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_payload_last_be = liteethmaccore_liteethmaccrc32checker_syncfifo_sink_payload_last_be;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_in_payload_error = liteethmaccore_liteethmaccrc32checker_syncfifo_sink_payload_error;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_source_valid = liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_readable;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_source_first = liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_first;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_source_last = liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_last;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_source_payload_data = liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_payload_data;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_source_payload_last_be = liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_payload_last_be;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_source_payload_error = liteethmaccore_liteethmaccrc32checker_syncfifo_fifo_out_payload_error;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_re = liteethmaccore_liteethmaccrc32checker_syncfifo_source_ready;

// synthesis translate_off
reg dummy_d_17;
// synthesis translate_on
always @(*) begin
	liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_adr <= 3'd0;
	if (liteethmaccore_liteethmaccrc32checker_syncfifo_replace) begin
		liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_adr <= (liteethmaccore_liteethmaccrc32checker_syncfifo_produce - 1'd1);
	end else begin
		liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_adr <= liteethmaccore_liteethmaccrc32checker_syncfifo_produce;
	end
// synthesis translate_off
	dummy_d_17 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_dat_w = liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_din;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_we = (liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_we & (liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_writable | liteethmaccore_liteethmaccrc32checker_syncfifo_replace));
assign liteethmaccore_liteethmaccrc32checker_syncfifo_do_read = (liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_readable & liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_re);
assign liteethmaccore_liteethmaccrc32checker_syncfifo_rdport_adr = liteethmaccore_liteethmaccrc32checker_syncfifo_consume;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_dout = liteethmaccore_liteethmaccrc32checker_syncfifo_rdport_dat_r;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_writable = (liteethmaccore_liteethmaccrc32checker_syncfifo_level != 3'd5);
assign liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_readable = (liteethmaccore_liteethmaccrc32checker_syncfifo_level != 1'd0);

// synthesis translate_off
reg dummy_d_18;
// synthesis translate_on
always @(*) begin
	liteethmaccore_liteethmaccrc32checker_source_source_valid <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_source_source_last <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_source_source_payload_last_be <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_source_source_payload_error <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_error <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_crc_ce <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_crc_reset <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_syncfifo_source_ready <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_fifo_reset <= 1'd0;
	rxdatapath_bufferizeendpoints_next_state <= 2'd0;
	liteethmaccore_liteethmaccrc32checker_last_be_next_value0 <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_last_be_next_value_ce0 <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_crc_error1_next_value1 <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_crc_error1_next_value_ce1 <= 1'd0;
	liteethmaccore_liteethmaccrc32checker_source_source_payload_error <= liteethmaccore_liteethmaccrc32checker_syncfifo_source_payload_error;
	rxdatapath_bufferizeendpoints_next_state <= rxdatapath_bufferizeendpoints_state;
	case (rxdatapath_bufferizeendpoints_state)
		1'd1: begin
			if ((liteethmaccore_liteethmaccrc32checker_sink_sink_valid & liteethmaccore_liteethmaccrc32checker_sink_sink_ready)) begin
				liteethmaccore_liteethmaccrc32checker_crc_ce <= 1'd1;
				rxdatapath_bufferizeendpoints_next_state <= 2'd2;
			end
		end
		2'd2: begin
			liteethmaccore_liteethmaccrc32checker_syncfifo_source_ready <= liteethmaccore_liteethmaccrc32checker_fifo_out;
			liteethmaccore_liteethmaccrc32checker_source_source_valid <= (liteethmaccore_liteethmaccrc32checker_sink_sink_valid & liteethmaccore_liteethmaccrc32checker_fifo_full);
			if (1'd1) begin
				liteethmaccore_liteethmaccrc32checker_source_source_last <= liteethmaccore_liteethmaccrc32checker_sink_sink_last;
				liteethmaccore_liteethmaccrc32checker_source_source_payload_last_be <= liteethmaccore_liteethmaccrc32checker_sink_sink_payload_last_be;
			end else begin
				if ((liteethmaccore_liteethmaccrc32checker_sink_sink_payload_last_be & 4'd15)) begin
					liteethmaccore_liteethmaccrc32checker_source_source_last <= liteethmaccore_liteethmaccrc32checker_sink_sink_last;
					liteethmaccore_liteethmaccrc32checker_source_source_payload_last_be <= (liteethmaccore_liteethmaccrc32checker_sink_sink_payload_last_be <<< 3'sd5);
				end else begin
					liteethmaccore_liteethmaccrc32checker_last_be_next_value0 <= (liteethmaccore_liteethmaccrc32checker_sink_sink_payload_last_be >>> 3'd4);
					liteethmaccore_liteethmaccrc32checker_last_be_next_value_ce0 <= 1'd1;
					liteethmaccore_liteethmaccrc32checker_crc_error1_next_value1 <= liteethmaccore_liteethmaccrc32checker_crc_error0;
					liteethmaccore_liteethmaccrc32checker_crc_error1_next_value_ce1 <= 1'd1;
				end
			end
			liteethmaccore_liteethmaccrc32checker_source_source_payload_error <= (liteethmaccore_liteethmaccrc32checker_sink_sink_payload_error | {1{(liteethmaccore_liteethmaccrc32checker_crc_error0 & liteethmaccore_liteethmaccrc32checker_sink_sink_last)}});
			liteethmaccore_liteethmaccrc32checker_error <= ((liteethmaccore_liteethmaccrc32checker_sink_sink_valid & liteethmaccore_liteethmaccrc32checker_sink_sink_last) & liteethmaccore_liteethmaccrc32checker_crc_error0);
			if ((liteethmaccore_liteethmaccrc32checker_sink_sink_valid & liteethmaccore_liteethmaccrc32checker_sink_sink_ready)) begin
				liteethmaccore_liteethmaccrc32checker_crc_ce <= 1'd1;
				if ((liteethmaccore_liteethmaccrc32checker_sink_sink_last & (liteethmaccore_liteethmaccrc32checker_sink_sink_payload_last_be > 4'd15))) begin
					rxdatapath_bufferizeendpoints_next_state <= 2'd3;
				end else begin
					if (liteethmaccore_liteethmaccrc32checker_sink_sink_last) begin
						rxdatapath_bufferizeendpoints_next_state <= 1'd0;
					end
				end
			end
		end
		2'd3: begin
			liteethmaccore_liteethmaccrc32checker_source_source_valid <= liteethmaccore_liteethmaccrc32checker_syncfifo_source_valid;
			liteethmaccore_liteethmaccrc32checker_syncfifo_source_ready <= liteethmaccore_liteethmaccrc32checker_source_source_ready;
			liteethmaccore_liteethmaccrc32checker_source_source_last <= liteethmaccore_liteethmaccrc32checker_syncfifo_source_last;
			liteethmaccore_liteethmaccrc32checker_source_source_payload_error <= (liteethmaccore_liteethmaccrc32checker_syncfifo_source_payload_error | {1{liteethmaccore_liteethmaccrc32checker_crc_error1}});
			liteethmaccore_liteethmaccrc32checker_source_source_payload_last_be <= liteethmaccore_liteethmaccrc32checker_last_be;
			if ((liteethmaccore_liteethmaccrc32checker_source_source_valid & liteethmaccore_liteethmaccrc32checker_source_source_ready)) begin
				rxdatapath_bufferizeendpoints_next_state <= 1'd0;
			end
		end
		default: begin
			liteethmaccore_liteethmaccrc32checker_crc_reset <= 1'd1;
			liteethmaccore_liteethmaccrc32checker_fifo_reset <= 1'd1;
			rxdatapath_bufferizeendpoints_next_state <= 1'd1;
		end
	endcase
// synthesis translate_off
	dummy_d_18 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_bufferizeendpoints_pipe_valid_sink_ready = ((~liteethmaccore_bufferizeendpoints_pipe_valid_source_valid) | liteethmaccore_bufferizeendpoints_pipe_valid_source_ready);
assign liteethmaccore_bufferizeendpoints_pipe_valid_sink_valid = liteethmaccore_bufferizeendpoints_sink_sink_valid;
assign liteethmaccore_bufferizeendpoints_sink_sink_ready = liteethmaccore_bufferizeendpoints_pipe_valid_sink_ready;
assign liteethmaccore_bufferizeendpoints_pipe_valid_sink_first = liteethmaccore_bufferizeendpoints_sink_sink_first;
assign liteethmaccore_bufferizeendpoints_pipe_valid_sink_last = liteethmaccore_bufferizeendpoints_sink_sink_last;
assign liteethmaccore_bufferizeendpoints_pipe_valid_sink_payload_data = liteethmaccore_bufferizeendpoints_sink_sink_payload_data;
assign liteethmaccore_bufferizeendpoints_pipe_valid_sink_payload_last_be = liteethmaccore_bufferizeendpoints_sink_sink_payload_last_be;
assign liteethmaccore_bufferizeendpoints_pipe_valid_sink_payload_error = liteethmaccore_bufferizeendpoints_sink_sink_payload_error;
assign liteethmaccore_bufferizeendpoints_source_source_valid = liteethmaccore_bufferizeendpoints_pipe_valid_source_valid;
assign liteethmaccore_bufferizeendpoints_pipe_valid_source_ready = liteethmaccore_bufferizeendpoints_source_source_ready;
assign liteethmaccore_bufferizeendpoints_source_source_first = liteethmaccore_bufferizeendpoints_pipe_valid_source_first;
assign liteethmaccore_bufferizeendpoints_source_source_last = liteethmaccore_bufferizeendpoints_pipe_valid_source_last;
assign liteethmaccore_bufferizeendpoints_source_source_payload_data = liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_data;
assign liteethmaccore_bufferizeendpoints_source_source_payload_last_be = liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_last_be;
assign liteethmaccore_bufferizeendpoints_source_source_payload_error = liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_error;
assign liteethmaccore_pulsesynchronizer1_o = (liteethmaccore_pulsesynchronizer1_toggle_o ^ liteethmaccore_pulsesynchronizer1_toggle_o_r);

// synthesis translate_off
reg dummy_d_19;
// synthesis translate_on
always @(*) begin
	liteethmaccore_rx_padding_length_inc <= 4'd0;
	case (liteethmaccore_rx_padding_sink_payload_last_be)
		1'd1: begin
			liteethmaccore_rx_padding_length_inc <= 1'd1;
		end
		2'd2: begin
			liteethmaccore_rx_padding_length_inc <= 2'd2;
		end
		3'd4: begin
			liteethmaccore_rx_padding_length_inc <= 2'd3;
		end
		4'd8: begin
			liteethmaccore_rx_padding_length_inc <= 3'd4;
		end
		5'd16: begin
			liteethmaccore_rx_padding_length_inc <= 3'd5;
		end
		6'd32: begin
			liteethmaccore_rx_padding_length_inc <= 3'd6;
		end
		7'd64: begin
			liteethmaccore_rx_padding_length_inc <= 3'd7;
		end
		default: begin
			liteethmaccore_rx_padding_length_inc <= 1'd1;
		end
	endcase
// synthesis translate_off
	dummy_d_19 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_rx_padding_source_valid = liteethmaccore_rx_padding_sink_valid;
assign liteethmaccore_rx_padding_sink_ready = liteethmaccore_rx_padding_source_ready;
assign liteethmaccore_rx_padding_source_first = liteethmaccore_rx_padding_sink_first;
assign liteethmaccore_rx_padding_source_last = liteethmaccore_rx_padding_sink_last;
assign liteethmaccore_rx_padding_source_payload_data = liteethmaccore_rx_padding_sink_payload_data;
assign liteethmaccore_rx_padding_source_payload_last_be = liteethmaccore_rx_padding_sink_payload_last_be;

// synthesis translate_off
reg dummy_d_20;
// synthesis translate_on
always @(*) begin
	liteethmaccore_rx_padding_source_payload_error <= 1'd0;
	if (((liteethmaccore_rx_padding_sink_valid & liteethmaccore_rx_padding_sink_last) & ((liteethmaccore_rx_padding_length + liteethmaccore_rx_padding_length_inc) < 6'd60))) begin
		liteethmaccore_rx_padding_source_payload_error <= {1{1'd1}};
	end else begin
		liteethmaccore_rx_padding_source_payload_error <= liteethmaccore_rx_padding_sink_payload_error;
	end
// synthesis translate_off
	dummy_d_20 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_rx_last_be_source_valid = liteethmaccore_rx_last_be_sink_valid;
assign liteethmaccore_rx_last_be_sink_ready = liteethmaccore_rx_last_be_source_ready;
assign liteethmaccore_rx_last_be_source_first = liteethmaccore_rx_last_be_sink_first;
assign liteethmaccore_rx_last_be_source_last = liteethmaccore_rx_last_be_sink_last;
assign liteethmaccore_rx_last_be_source_payload_data = liteethmaccore_rx_last_be_sink_payload_data;
assign liteethmaccore_rx_last_be_source_payload_error = liteethmaccore_rx_last_be_sink_payload_error;

// synthesis translate_off
reg dummy_d_21;
// synthesis translate_on
always @(*) begin
	liteethmaccore_rx_last_be_source_payload_last_be <= 1'd0;
	liteethmaccore_rx_last_be_source_payload_last_be <= liteethmaccore_rx_last_be_sink_payload_last_be;
	if (1'd1) begin
		liteethmaccore_rx_last_be_source_payload_last_be <= liteethmaccore_rx_last_be_sink_last;
	end
// synthesis translate_off
	dummy_d_21 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_rx_converter_converter_sink_valid = liteethmaccore_rx_converter_sink_valid;
assign liteethmaccore_rx_converter_converter_sink_first = liteethmaccore_rx_converter_sink_first;
assign liteethmaccore_rx_converter_converter_sink_last = liteethmaccore_rx_converter_sink_last;
assign liteethmaccore_rx_converter_sink_ready = liteethmaccore_rx_converter_converter_sink_ready;
assign liteethmaccore_rx_converter_converter_sink_payload_data = {liteethmaccore_rx_converter_sink_payload_error, liteethmaccore_rx_converter_sink_payload_last_be, liteethmaccore_rx_converter_sink_payload_data};
assign liteethmaccore_rx_converter_source_valid = liteethmaccore_rx_converter_source_source_valid;
assign liteethmaccore_rx_converter_source_first = liteethmaccore_rx_converter_source_source_first;
assign liteethmaccore_rx_converter_source_last = liteethmaccore_rx_converter_source_source_last;
assign liteethmaccore_rx_converter_source_source_ready = liteethmaccore_rx_converter_source_ready;

// synthesis translate_off
reg dummy_d_22;
// synthesis translate_on
always @(*) begin
	liteethmaccore_rx_converter_source_payload_data <= 64'd0;
	liteethmaccore_rx_converter_source_payload_data[7:0] <= liteethmaccore_rx_converter_source_source_payload_data[7:0];
	liteethmaccore_rx_converter_source_payload_data[15:8] <= liteethmaccore_rx_converter_source_source_payload_data[17:10];
	liteethmaccore_rx_converter_source_payload_data[23:16] <= liteethmaccore_rx_converter_source_source_payload_data[27:20];
	liteethmaccore_rx_converter_source_payload_data[31:24] <= liteethmaccore_rx_converter_source_source_payload_data[37:30];
	liteethmaccore_rx_converter_source_payload_data[39:32] <= liteethmaccore_rx_converter_source_source_payload_data[47:40];
	liteethmaccore_rx_converter_source_payload_data[47:40] <= liteethmaccore_rx_converter_source_source_payload_data[57:50];
	liteethmaccore_rx_converter_source_payload_data[55:48] <= liteethmaccore_rx_converter_source_source_payload_data[67:60];
	liteethmaccore_rx_converter_source_payload_data[63:56] <= liteethmaccore_rx_converter_source_source_payload_data[77:70];
// synthesis translate_off
	dummy_d_22 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_23;
// synthesis translate_on
always @(*) begin
	liteethmaccore_rx_converter_source_payload_last_be <= 8'd0;
	liteethmaccore_rx_converter_source_payload_last_be[0] <= liteethmaccore_rx_converter_source_source_payload_data[8];
	liteethmaccore_rx_converter_source_payload_last_be[1] <= liteethmaccore_rx_converter_source_source_payload_data[18];
	liteethmaccore_rx_converter_source_payload_last_be[2] <= liteethmaccore_rx_converter_source_source_payload_data[28];
	liteethmaccore_rx_converter_source_payload_last_be[3] <= liteethmaccore_rx_converter_source_source_payload_data[38];
	liteethmaccore_rx_converter_source_payload_last_be[4] <= liteethmaccore_rx_converter_source_source_payload_data[48];
	liteethmaccore_rx_converter_source_payload_last_be[5] <= liteethmaccore_rx_converter_source_source_payload_data[58];
	liteethmaccore_rx_converter_source_payload_last_be[6] <= liteethmaccore_rx_converter_source_source_payload_data[68];
	liteethmaccore_rx_converter_source_payload_last_be[7] <= liteethmaccore_rx_converter_source_source_payload_data[78];
// synthesis translate_off
	dummy_d_23 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_24;
// synthesis translate_on
always @(*) begin
	liteethmaccore_rx_converter_source_payload_error <= 8'd0;
	liteethmaccore_rx_converter_source_payload_error[0] <= liteethmaccore_rx_converter_source_source_payload_data[9];
	liteethmaccore_rx_converter_source_payload_error[1] <= liteethmaccore_rx_converter_source_source_payload_data[19];
	liteethmaccore_rx_converter_source_payload_error[2] <= liteethmaccore_rx_converter_source_source_payload_data[29];
	liteethmaccore_rx_converter_source_payload_error[3] <= liteethmaccore_rx_converter_source_source_payload_data[39];
	liteethmaccore_rx_converter_source_payload_error[4] <= liteethmaccore_rx_converter_source_source_payload_data[49];
	liteethmaccore_rx_converter_source_payload_error[5] <= liteethmaccore_rx_converter_source_source_payload_data[59];
	liteethmaccore_rx_converter_source_payload_error[6] <= liteethmaccore_rx_converter_source_source_payload_data[69];
	liteethmaccore_rx_converter_source_payload_error[7] <= liteethmaccore_rx_converter_source_source_payload_data[79];
// synthesis translate_off
	dummy_d_24 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_rx_converter_source_source_valid = liteethmaccore_rx_converter_converter_source_valid;
assign liteethmaccore_rx_converter_converter_source_ready = liteethmaccore_rx_converter_source_source_ready;
assign liteethmaccore_rx_converter_source_source_first = liteethmaccore_rx_converter_converter_source_first;
assign liteethmaccore_rx_converter_source_source_last = liteethmaccore_rx_converter_converter_source_last;
assign liteethmaccore_rx_converter_source_source_payload_data = liteethmaccore_rx_converter_converter_source_payload_data;
assign liteethmaccore_rx_converter_converter_sink_ready = ((~liteethmaccore_rx_converter_converter_strobe_all) | liteethmaccore_rx_converter_converter_source_ready);
assign liteethmaccore_rx_converter_converter_source_valid = liteethmaccore_rx_converter_converter_strobe_all;
assign liteethmaccore_rx_converter_converter_load_part = (liteethmaccore_rx_converter_converter_sink_valid & liteethmaccore_rx_converter_converter_sink_ready);
assign liteethmaccore_rx_cdc_cdc_sink_valid = liteethmaccore_rx_cdc_sink_sink_valid;
assign liteethmaccore_rx_cdc_sink_sink_ready = liteethmaccore_rx_cdc_cdc_sink_ready;
assign liteethmaccore_rx_cdc_cdc_sink_first = liteethmaccore_rx_cdc_sink_sink_first;
assign liteethmaccore_rx_cdc_cdc_sink_last = liteethmaccore_rx_cdc_sink_sink_last;
assign liteethmaccore_rx_cdc_cdc_sink_payload_data = liteethmaccore_rx_cdc_sink_sink_payload_data;
assign liteethmaccore_rx_cdc_cdc_sink_payload_last_be = liteethmaccore_rx_cdc_sink_sink_payload_last_be;
assign liteethmaccore_rx_cdc_cdc_sink_payload_error = liteethmaccore_rx_cdc_sink_sink_payload_error;
assign liteethmaccore_rx_cdc_source_source_valid = liteethmaccore_rx_cdc_cdc_source_valid;
assign liteethmaccore_rx_cdc_cdc_source_ready = liteethmaccore_rx_cdc_source_source_ready;
assign liteethmaccore_rx_cdc_source_source_first = liteethmaccore_rx_cdc_cdc_source_first;
assign liteethmaccore_rx_cdc_source_source_last = liteethmaccore_rx_cdc_cdc_source_last;
assign liteethmaccore_rx_cdc_source_source_payload_data = liteethmaccore_rx_cdc_cdc_source_payload_data;
assign liteethmaccore_rx_cdc_source_source_payload_last_be = liteethmaccore_rx_cdc_cdc_source_payload_last_be;
assign liteethmaccore_rx_cdc_source_source_payload_error = liteethmaccore_rx_cdc_cdc_source_payload_error;
assign liteethmaccore_rx_cdc_cdc_asyncfifo_din = {liteethmaccore_rx_cdc_cdc_fifo_in_last, liteethmaccore_rx_cdc_cdc_fifo_in_first, liteethmaccore_rx_cdc_cdc_fifo_in_payload_error, liteethmaccore_rx_cdc_cdc_fifo_in_payload_last_be, liteethmaccore_rx_cdc_cdc_fifo_in_payload_data};
assign {liteethmaccore_rx_cdc_cdc_fifo_out_last, liteethmaccore_rx_cdc_cdc_fifo_out_first, liteethmaccore_rx_cdc_cdc_fifo_out_payload_error, liteethmaccore_rx_cdc_cdc_fifo_out_payload_last_be, liteethmaccore_rx_cdc_cdc_fifo_out_payload_data} = liteethmaccore_rx_cdc_cdc_asyncfifo_dout;
assign liteethmaccore_rx_cdc_cdc_sink_ready = liteethmaccore_rx_cdc_cdc_asyncfifo_writable;
assign liteethmaccore_rx_cdc_cdc_asyncfifo_we = liteethmaccore_rx_cdc_cdc_sink_valid;
assign liteethmaccore_rx_cdc_cdc_fifo_in_first = liteethmaccore_rx_cdc_cdc_sink_first;
assign liteethmaccore_rx_cdc_cdc_fifo_in_last = liteethmaccore_rx_cdc_cdc_sink_last;
assign liteethmaccore_rx_cdc_cdc_fifo_in_payload_data = liteethmaccore_rx_cdc_cdc_sink_payload_data;
assign liteethmaccore_rx_cdc_cdc_fifo_in_payload_last_be = liteethmaccore_rx_cdc_cdc_sink_payload_last_be;
assign liteethmaccore_rx_cdc_cdc_fifo_in_payload_error = liteethmaccore_rx_cdc_cdc_sink_payload_error;
assign liteethmaccore_rx_cdc_cdc_source_valid = liteethmaccore_rx_cdc_cdc_asyncfifo_readable;
assign liteethmaccore_rx_cdc_cdc_source_first = liteethmaccore_rx_cdc_cdc_fifo_out_first;
assign liteethmaccore_rx_cdc_cdc_source_last = liteethmaccore_rx_cdc_cdc_fifo_out_last;
assign liteethmaccore_rx_cdc_cdc_source_payload_data = liteethmaccore_rx_cdc_cdc_fifo_out_payload_data;
assign liteethmaccore_rx_cdc_cdc_source_payload_last_be = liteethmaccore_rx_cdc_cdc_fifo_out_payload_last_be;
assign liteethmaccore_rx_cdc_cdc_source_payload_error = liteethmaccore_rx_cdc_cdc_fifo_out_payload_error;
assign liteethmaccore_rx_cdc_cdc_asyncfifo_re = liteethmaccore_rx_cdc_cdc_source_ready;
assign liteethmaccore_rx_cdc_cdc_graycounter0_ce = (liteethmaccore_rx_cdc_cdc_asyncfifo_writable & liteethmaccore_rx_cdc_cdc_asyncfifo_we);
assign liteethmaccore_rx_cdc_cdc_graycounter1_ce = (liteethmaccore_rx_cdc_cdc_asyncfifo_readable & liteethmaccore_rx_cdc_cdc_asyncfifo_re);
assign liteethmaccore_rx_cdc_cdc_asyncfifo_writable = (((liteethmaccore_rx_cdc_cdc_graycounter0_q[5] == liteethmaccore_rx_cdc_cdc_consume_wdomain[5]) | (liteethmaccore_rx_cdc_cdc_graycounter0_q[4] == liteethmaccore_rx_cdc_cdc_consume_wdomain[4])) | (liteethmaccore_rx_cdc_cdc_graycounter0_q[3:0] != liteethmaccore_rx_cdc_cdc_consume_wdomain[3:0]));
assign liteethmaccore_rx_cdc_cdc_asyncfifo_readable = (liteethmaccore_rx_cdc_cdc_graycounter1_q != liteethmaccore_rx_cdc_cdc_produce_rdomain);
assign liteethmaccore_rx_cdc_cdc_wrport_adr = liteethmaccore_rx_cdc_cdc_graycounter0_q_binary[4:0];
assign liteethmaccore_rx_cdc_cdc_wrport_dat_w = liteethmaccore_rx_cdc_cdc_asyncfifo_din;
assign liteethmaccore_rx_cdc_cdc_wrport_we = liteethmaccore_rx_cdc_cdc_graycounter0_ce;
assign liteethmaccore_rx_cdc_cdc_rdport_adr = liteethmaccore_rx_cdc_cdc_graycounter1_q_next_binary[4:0];
assign liteethmaccore_rx_cdc_cdc_asyncfifo_dout = liteethmaccore_rx_cdc_cdc_rdport_dat_r;

// synthesis translate_off
reg dummy_d_25;
// synthesis translate_on
always @(*) begin
	liteethmaccore_rx_cdc_cdc_graycounter0_q_next_binary <= 6'd0;
	if (liteethmaccore_rx_cdc_cdc_graycounter0_ce) begin
		liteethmaccore_rx_cdc_cdc_graycounter0_q_next_binary <= (liteethmaccore_rx_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		liteethmaccore_rx_cdc_cdc_graycounter0_q_next_binary <= liteethmaccore_rx_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_25 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_rx_cdc_cdc_graycounter0_q_next = (liteethmaccore_rx_cdc_cdc_graycounter0_q_next_binary ^ liteethmaccore_rx_cdc_cdc_graycounter0_q_next_binary[5:1]);

// synthesis translate_off
reg dummy_d_26;
// synthesis translate_on
always @(*) begin
	liteethmaccore_rx_cdc_cdc_graycounter1_q_next_binary <= 6'd0;
	if (liteethmaccore_rx_cdc_cdc_graycounter1_ce) begin
		liteethmaccore_rx_cdc_cdc_graycounter1_q_next_binary <= (liteethmaccore_rx_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		liteethmaccore_rx_cdc_cdc_graycounter1_q_next_binary <= liteethmaccore_rx_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_26 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccore_rx_cdc_cdc_graycounter1_q_next = (liteethmaccore_rx_cdc_cdc_graycounter1_q_next_binary ^ liteethmaccore_rx_cdc_cdc_graycounter1_q_next_binary[5:1]);
assign liteethmaccore_rx_preamble_sink_valid = phy_source_valid;
assign phy_source_ready = liteethmaccore_rx_preamble_sink_ready;
assign liteethmaccore_rx_preamble_sink_first = phy_source_first;
assign liteethmaccore_rx_preamble_sink_last = phy_source_last;
assign liteethmaccore_rx_preamble_sink_payload_data = phy_source_payload_data;
assign liteethmaccore_rx_preamble_sink_payload_last_be = phy_source_payload_last_be;
assign liteethmaccore_rx_preamble_sink_payload_error = phy_source_payload_error;
assign liteethmaccore_bufferizeendpoints_sink_sink_valid = liteethmaccore_rx_preamble_source_valid;
assign liteethmaccore_rx_preamble_source_ready = liteethmaccore_bufferizeendpoints_sink_sink_ready;
assign liteethmaccore_bufferizeendpoints_sink_sink_first = liteethmaccore_rx_preamble_source_first;
assign liteethmaccore_bufferizeendpoints_sink_sink_last = liteethmaccore_rx_preamble_source_last;
assign liteethmaccore_bufferizeendpoints_sink_sink_payload_data = liteethmaccore_rx_preamble_source_payload_data;
assign liteethmaccore_bufferizeendpoints_sink_sink_payload_last_be = liteethmaccore_rx_preamble_source_payload_last_be;
assign liteethmaccore_bufferizeendpoints_sink_sink_payload_error = liteethmaccore_rx_preamble_source_payload_error;
assign liteethmaccore_rx_padding_sink_valid = liteethmaccore_liteethmaccrc32checker_source_source_valid;
assign liteethmaccore_liteethmaccrc32checker_source_source_ready = liteethmaccore_rx_padding_sink_ready;
assign liteethmaccore_rx_padding_sink_first = liteethmaccore_liteethmaccrc32checker_source_source_first;
assign liteethmaccore_rx_padding_sink_last = liteethmaccore_liteethmaccrc32checker_source_source_last;
assign liteethmaccore_rx_padding_sink_payload_data = liteethmaccore_liteethmaccrc32checker_source_source_payload_data;
assign liteethmaccore_rx_padding_sink_payload_last_be = liteethmaccore_liteethmaccrc32checker_source_source_payload_last_be;
assign liteethmaccore_rx_padding_sink_payload_error = liteethmaccore_liteethmaccrc32checker_source_source_payload_error;
assign liteethmaccore_rx_last_be_sink_valid = liteethmaccore_rx_padding_source_valid;
assign liteethmaccore_rx_padding_source_ready = liteethmaccore_rx_last_be_sink_ready;
assign liteethmaccore_rx_last_be_sink_first = liteethmaccore_rx_padding_source_first;
assign liteethmaccore_rx_last_be_sink_last = liteethmaccore_rx_padding_source_last;
assign liteethmaccore_rx_last_be_sink_payload_data = liteethmaccore_rx_padding_source_payload_data;
assign liteethmaccore_rx_last_be_sink_payload_last_be = liteethmaccore_rx_padding_source_payload_last_be;
assign liteethmaccore_rx_last_be_sink_payload_error = liteethmaccore_rx_padding_source_payload_error;
assign liteethmaccore_rx_converter_sink_valid = liteethmaccore_rx_last_be_source_valid;
assign liteethmaccore_rx_last_be_source_ready = liteethmaccore_rx_converter_sink_ready;
assign liteethmaccore_rx_converter_sink_first = liteethmaccore_rx_last_be_source_first;
assign liteethmaccore_rx_converter_sink_last = liteethmaccore_rx_last_be_source_last;
assign liteethmaccore_rx_converter_sink_payload_data = liteethmaccore_rx_last_be_source_payload_data;
assign liteethmaccore_rx_converter_sink_payload_last_be = liteethmaccore_rx_last_be_source_payload_last_be;
assign liteethmaccore_rx_converter_sink_payload_error = liteethmaccore_rx_last_be_source_payload_error;
assign liteethmaccore_rx_cdc_sink_sink_valid = liteethmaccore_rx_converter_source_valid;
assign liteethmaccore_rx_converter_source_ready = liteethmaccore_rx_cdc_sink_sink_ready;
assign liteethmaccore_rx_cdc_sink_sink_first = liteethmaccore_rx_converter_source_first;
assign liteethmaccore_rx_cdc_sink_sink_last = liteethmaccore_rx_converter_source_last;
assign liteethmaccore_rx_cdc_sink_sink_payload_data = liteethmaccore_rx_converter_source_payload_data;
assign liteethmaccore_rx_cdc_sink_sink_payload_last_be = liteethmaccore_rx_converter_source_payload_last_be;
assign liteethmaccore_rx_cdc_sink_sink_payload_error = liteethmaccore_rx_converter_source_payload_error;
assign liteethmaccore_source_valid = liteethmaccore_rx_cdc_source_source_valid;
assign liteethmaccore_rx_cdc_source_source_ready = liteethmaccore_source_ready;
assign liteethmaccore_source_first = liteethmaccore_rx_cdc_source_source_first;
assign liteethmaccore_source_last = liteethmaccore_rx_cdc_source_source_last;
assign liteethmaccore_source_payload_data = liteethmaccore_rx_cdc_source_source_payload_data;
assign liteethmaccore_source_payload_last_be = liteethmaccore_rx_cdc_source_source_payload_last_be;
assign liteethmaccore_source_payload_error = liteethmaccore_rx_cdc_source_source_payload_error;
assign packetfifo_payload_fifo_sink_first = packetfifo_sink_sink_first;
assign packetfifo_payload_fifo_sink_last = packetfifo_sink_sink_last;
assign packetfifo_payload_fifo_sink_payload_data = packetfifo_sink_sink_payload_data;
assign packetfifo_payload_fifo_sink_payload_last_be = packetfifo_sink_sink_payload_last_be;
assign packetfifo_payload_fifo_sink_payload_error = packetfifo_sink_sink_payload_error;
assign packetfifo_param_fifo_sink_valid = ((packetfifo_sink_sink_valid & packetfifo_sink_sink_last) & packetfifo_payload_fifo_sink_ready);
assign packetfifo_payload_fifo_sink_valid = (packetfifo_sink_sink_valid & packetfifo_param_fifo_sink_ready);
assign packetfifo_sink_sink_ready = (packetfifo_param_fifo_sink_ready & packetfifo_payload_fifo_sink_ready);
assign packetfifo_source_source_valid = packetfifo_param_fifo_source_valid;

// synthesis translate_off
reg dummy_d_27;
// synthesis translate_on
always @(*) begin
	packetfifo_source_source_first <= 1'd0;
	packetfifo_source_source_first <= packetfifo_param_fifo_source_first;
	packetfifo_source_source_first <= packetfifo_payload_fifo_source_first;
// synthesis translate_off
	dummy_d_27 <= dummy_s;
// synthesis translate_on
end
assign packetfifo_source_source_last = packetfifo_payload_fifo_source_last;
assign packetfifo_source_source_payload_data = packetfifo_payload_fifo_source_payload_data;
assign packetfifo_source_source_payload_last_be = packetfifo_payload_fifo_source_payload_last_be;
assign packetfifo_source_source_payload_error = packetfifo_payload_fifo_source_payload_error;
assign packetfifo_param_fifo_source_ready = ((packetfifo_source_source_valid & packetfifo_source_source_last) & packetfifo_source_source_ready);
assign packetfifo_payload_fifo_source_ready = (packetfifo_source_source_valid & packetfifo_source_source_ready);
assign packetfifo_payload_fifo_syncfifo_din = {packetfifo_payload_fifo_fifo_in_last, packetfifo_payload_fifo_fifo_in_first, packetfifo_payload_fifo_fifo_in_payload_error, packetfifo_payload_fifo_fifo_in_payload_last_be, packetfifo_payload_fifo_fifo_in_payload_data};
assign {packetfifo_payload_fifo_fifo_out_last, packetfifo_payload_fifo_fifo_out_first, packetfifo_payload_fifo_fifo_out_payload_error, packetfifo_payload_fifo_fifo_out_payload_last_be, packetfifo_payload_fifo_fifo_out_payload_data} = packetfifo_payload_fifo_syncfifo_dout;
assign packetfifo_payload_fifo_sink_ready = packetfifo_payload_fifo_syncfifo_writable;
assign packetfifo_payload_fifo_syncfifo_we = packetfifo_payload_fifo_sink_valid;
assign packetfifo_payload_fifo_fifo_in_first = packetfifo_payload_fifo_sink_first;
assign packetfifo_payload_fifo_fifo_in_last = packetfifo_payload_fifo_sink_last;
assign packetfifo_payload_fifo_fifo_in_payload_data = packetfifo_payload_fifo_sink_payload_data;
assign packetfifo_payload_fifo_fifo_in_payload_last_be = packetfifo_payload_fifo_sink_payload_last_be;
assign packetfifo_payload_fifo_fifo_in_payload_error = packetfifo_payload_fifo_sink_payload_error;
assign packetfifo_payload_fifo_source_valid = packetfifo_payload_fifo_readable;
assign packetfifo_payload_fifo_source_first = packetfifo_payload_fifo_fifo_out_first;
assign packetfifo_payload_fifo_source_last = packetfifo_payload_fifo_fifo_out_last;
assign packetfifo_payload_fifo_source_payload_data = packetfifo_payload_fifo_fifo_out_payload_data;
assign packetfifo_payload_fifo_source_payload_last_be = packetfifo_payload_fifo_fifo_out_payload_last_be;
assign packetfifo_payload_fifo_source_payload_error = packetfifo_payload_fifo_fifo_out_payload_error;
assign packetfifo_payload_fifo_re = packetfifo_payload_fifo_source_ready;
assign packetfifo_payload_fifo_syncfifo_re = (packetfifo_payload_fifo_syncfifo_readable & ((~packetfifo_payload_fifo_readable) | packetfifo_payload_fifo_re));
assign packetfifo_payload_fifo_level1 = (packetfifo_payload_fifo_level0 + packetfifo_payload_fifo_readable);

// synthesis translate_off
reg dummy_d_28;
// synthesis translate_on
always @(*) begin
	packetfifo_payload_fifo_wrport_adr <= 9'd0;
	if (packetfifo_payload_fifo_replace) begin
		packetfifo_payload_fifo_wrport_adr <= (packetfifo_payload_fifo_produce - 1'd1);
	end else begin
		packetfifo_payload_fifo_wrport_adr <= packetfifo_payload_fifo_produce;
	end
// synthesis translate_off
	dummy_d_28 <= dummy_s;
// synthesis translate_on
end
assign packetfifo_payload_fifo_wrport_dat_w = packetfifo_payload_fifo_syncfifo_din;
assign packetfifo_payload_fifo_wrport_we = (packetfifo_payload_fifo_syncfifo_we & (packetfifo_payload_fifo_syncfifo_writable | packetfifo_payload_fifo_replace));
assign packetfifo_payload_fifo_do_read = (packetfifo_payload_fifo_syncfifo_readable & packetfifo_payload_fifo_syncfifo_re);
assign packetfifo_payload_fifo_rdport_adr = packetfifo_payload_fifo_consume;
assign packetfifo_payload_fifo_syncfifo_dout = packetfifo_payload_fifo_rdport_dat_r;
assign packetfifo_payload_fifo_rdport_re = packetfifo_payload_fifo_do_read;
assign packetfifo_payload_fifo_syncfifo_writable = (packetfifo_payload_fifo_level0 != 10'd512);
assign packetfifo_payload_fifo_syncfifo_readable = (packetfifo_payload_fifo_level0 != 1'd0);
assign packetfifo_param_fifo_syncfifo_din = {packetfifo_param_fifo_fifo_in_last, packetfifo_param_fifo_fifo_in_first, packetfifo_param_fifo_fifo_in_param_dummy};
assign {packetfifo_param_fifo_fifo_out_last, packetfifo_param_fifo_fifo_out_first, packetfifo_param_fifo_fifo_out_param_dummy} = packetfifo_param_fifo_syncfifo_dout;
assign packetfifo_param_fifo_sink_ready = packetfifo_param_fifo_syncfifo_writable;
assign packetfifo_param_fifo_syncfifo_we = packetfifo_param_fifo_sink_valid;
assign packetfifo_param_fifo_fifo_in_first = packetfifo_param_fifo_sink_first;
assign packetfifo_param_fifo_fifo_in_last = packetfifo_param_fifo_sink_last;
assign packetfifo_param_fifo_fifo_in_param_dummy = packetfifo_param_fifo_sink_param_dummy;
assign packetfifo_param_fifo_source_valid = packetfifo_param_fifo_readable;
assign packetfifo_param_fifo_source_first = packetfifo_param_fifo_fifo_out_first;
assign packetfifo_param_fifo_source_last = packetfifo_param_fifo_fifo_out_last;
assign packetfifo_param_fifo_source_param_dummy = packetfifo_param_fifo_fifo_out_param_dummy;
assign packetfifo_param_fifo_re = packetfifo_param_fifo_source_ready;
assign packetfifo_param_fifo_syncfifo_re = (packetfifo_param_fifo_syncfifo_readable & ((~packetfifo_param_fifo_readable) | packetfifo_param_fifo_re));
assign packetfifo_param_fifo_level1 = (packetfifo_param_fifo_level0 + packetfifo_param_fifo_readable);

// synthesis translate_off
reg dummy_d_29;
// synthesis translate_on
always @(*) begin
	packetfifo_param_fifo_wrport_adr <= 4'd0;
	if (packetfifo_param_fifo_replace) begin
		packetfifo_param_fifo_wrport_adr <= (packetfifo_param_fifo_produce - 1'd1);
	end else begin
		packetfifo_param_fifo_wrport_adr <= packetfifo_param_fifo_produce;
	end
// synthesis translate_off
	dummy_d_29 <= dummy_s;
// synthesis translate_on
end
assign packetfifo_param_fifo_wrport_dat_w = packetfifo_param_fifo_syncfifo_din;
assign packetfifo_param_fifo_wrport_we = (packetfifo_param_fifo_syncfifo_we & (packetfifo_param_fifo_syncfifo_writable | packetfifo_param_fifo_replace));
assign packetfifo_param_fifo_do_read = (packetfifo_param_fifo_syncfifo_readable & packetfifo_param_fifo_syncfifo_re);
assign packetfifo_param_fifo_rdport_adr = packetfifo_param_fifo_consume;
assign packetfifo_param_fifo_syncfifo_dout = packetfifo_param_fifo_rdport_dat_r;
assign packetfifo_param_fifo_rdport_re = packetfifo_param_fifo_do_read;
assign packetfifo_param_fifo_syncfifo_writable = (packetfifo_param_fifo_level0 != 4'd9);
assign packetfifo_param_fifo_syncfifo_readable = (packetfifo_param_fifo_level0 != 1'd0);
assign tx_dp_cdc_sink_valid = tx_dp_sink_sink_valid;
assign tx_dp_sink_sink_ready = tx_dp_cdc_sink_ready;
assign tx_dp_cdc_sink_first = tx_dp_sink_sink_first;
assign tx_dp_cdc_sink_last = tx_dp_sink_sink_last;
assign tx_dp_cdc_sink_payload_data = tx_dp_sink_sink_payload_data;
assign tx_dp_cdc_sink_payload_keep = tx_dp_sink_sink_payload_keep;
assign tx_dp_source_source_valid = tx_dp_cdc_source_valid;
assign tx_dp_cdc_source_ready = tx_dp_source_source_ready;
assign tx_dp_source_source_first = tx_dp_cdc_source_first;
assign tx_dp_source_source_last = tx_dp_cdc_source_last;
assign tx_dp_source_source_payload_data = tx_dp_cdc_source_payload_data;
assign tx_dp_source_source_payload_keep = tx_dp_cdc_source_payload_keep;
assign tx_dp_cdc_asyncfifo_din = {tx_dp_cdc_fifo_in_last, tx_dp_cdc_fifo_in_first, tx_dp_cdc_fifo_in_payload_keep, tx_dp_cdc_fifo_in_payload_data};
assign {tx_dp_cdc_fifo_out_last, tx_dp_cdc_fifo_out_first, tx_dp_cdc_fifo_out_payload_keep, tx_dp_cdc_fifo_out_payload_data} = tx_dp_cdc_dout;
assign tx_dp_cdc_sink_ready = tx_dp_cdc_asyncfifo_writable;
assign tx_dp_cdc_asyncfifo_we = tx_dp_cdc_sink_valid;
assign tx_dp_cdc_fifo_in_first = tx_dp_cdc_sink_first;
assign tx_dp_cdc_fifo_in_last = tx_dp_cdc_sink_last;
assign tx_dp_cdc_fifo_in_payload_data = tx_dp_cdc_sink_payload_data;
assign tx_dp_cdc_fifo_in_payload_keep = tx_dp_cdc_sink_payload_keep;
assign tx_dp_cdc_source_valid = tx_dp_cdc_readable;
assign tx_dp_cdc_source_first = tx_dp_cdc_fifo_out_first;
assign tx_dp_cdc_source_last = tx_dp_cdc_fifo_out_last;
assign tx_dp_cdc_source_payload_data = tx_dp_cdc_fifo_out_payload_data;
assign tx_dp_cdc_source_payload_keep = tx_dp_cdc_fifo_out_payload_keep;
assign tx_dp_cdc_re = tx_dp_cdc_source_ready;
assign tx_dp_cdc_asyncfifo_re = (tx_dp_cdc_re | (~tx_dp_cdc_readable));
assign tx_dp_cdc_graycounter0_ce = (tx_dp_cdc_asyncfifo_writable & tx_dp_cdc_asyncfifo_we);
assign tx_dp_cdc_graycounter1_ce = (tx_dp_cdc_asyncfifo_readable & tx_dp_cdc_asyncfifo_re);
assign tx_dp_cdc_asyncfifo_writable = (((tx_dp_cdc_graycounter0_q[4] == tx_dp_cdc_consume_wdomain[4]) | (tx_dp_cdc_graycounter0_q[3] == tx_dp_cdc_consume_wdomain[3])) | (tx_dp_cdc_graycounter0_q[2:0] != tx_dp_cdc_consume_wdomain[2:0]));
assign tx_dp_cdc_asyncfifo_readable = (tx_dp_cdc_graycounter1_q != tx_dp_cdc_produce_rdomain);
assign tx_dp_cdc_wrport_adr = tx_dp_cdc_graycounter0_q_binary[3:0];
assign tx_dp_cdc_wrport_dat_w = tx_dp_cdc_asyncfifo_din;
assign tx_dp_cdc_wrport_we = tx_dp_cdc_graycounter0_ce;
assign tx_dp_cdc_rdport_adr = tx_dp_cdc_graycounter1_q_next_binary[3:0];
assign tx_dp_cdc_asyncfifo_dout = tx_dp_cdc_rdport_dat_r;

// synthesis translate_off
reg dummy_d_30;
// synthesis translate_on
always @(*) begin
	tx_dp_cdc_graycounter0_q_next_binary <= 5'd0;
	if (tx_dp_cdc_graycounter0_ce) begin
		tx_dp_cdc_graycounter0_q_next_binary <= (tx_dp_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		tx_dp_cdc_graycounter0_q_next_binary <= tx_dp_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_30 <= dummy_s;
// synthesis translate_on
end
assign tx_dp_cdc_graycounter0_q_next = (tx_dp_cdc_graycounter0_q_next_binary ^ tx_dp_cdc_graycounter0_q_next_binary[4:1]);

// synthesis translate_off
reg dummy_d_31;
// synthesis translate_on
always @(*) begin
	tx_dp_cdc_graycounter1_q_next_binary <= 5'd0;
	if (tx_dp_cdc_graycounter1_ce) begin
		tx_dp_cdc_graycounter1_q_next_binary <= (tx_dp_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		tx_dp_cdc_graycounter1_q_next_binary <= tx_dp_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_31 <= dummy_s;
// synthesis translate_on
end
assign tx_dp_cdc_graycounter1_q_next = (tx_dp_cdc_graycounter1_q_next_binary ^ tx_dp_cdc_graycounter1_q_next_binary[4:1]);
assign slice_proxy = {liteethmaccore_tx_crc_value, liteethmaccore_tx_crc_sink_payload_data[7:0]};
assign resync_clk = eth_tx_clk_1;
assign resync_clk_1 = eth_rx_clk_1;
assign resync_clk_2 = macsys_clk;
assign resync_clk_3 = macdp_clk;
assign resync_clk_4 = maceth_tx_clk;
assign resync_clk_5 = maceth_rx_clk;
assign liteethmaccore_tx_cdc_cdc_produce_rdomain = multiregimpl01;
assign liteethmaccore_tx_cdc_cdc_consume_wdomain = multiregimpl11;
assign liteethmaccore_pulsesynchronizer0_toggle_o = multiregimpl21;
assign liteethmaccore_pulsesynchronizer1_toggle_o = multiregimpl31;
assign liteethmaccore_rx_cdc_cdc_produce_rdomain = multiregimpl41;
assign liteethmaccore_rx_cdc_cdc_consume_wdomain = multiregimpl51;
assign tx_dp_cdc_produce_rdomain = multiregimpl61;
assign tx_dp_cdc_consume_wdomain = multiregimpl71;

always @(posedge eth_rx_clk_1) begin
	phy_dv_d <= pads_rx_dv;
	phy_source_valid <= pads_rx_dv;
	phy_source_payload_data <= pads_rx_data;
	if (eth_rx_rst) begin
		phy_source_valid <= 1'd0;
		phy_source_payload_data <= 8'd0;
		phy_dv_d <= 1'd0;
	end
end

always @(posedge eth_tx_clk_1) begin
	pads_tx_er <= 1'd0;
	pads_tx_en <= phy_sink_valid1;
	pads_tx_data <= phy_sink_payload_data;
	phy_sink_ready1 <= 1'd1;
	if (eth_tx_rst) begin
		phy_sink_ready1 <= 1'd0;
	end
end

always @(posedge macdp_clk) begin
	tx_dp_cdc_graycounter0_q_binary <= tx_dp_cdc_graycounter0_q_next_binary;
	tx_dp_cdc_graycounter0_q <= tx_dp_cdc_graycounter0_q_next;
	if (macdp_rst) begin
		tx_dp_cdc_graycounter0_q <= 5'd0;
		tx_dp_cdc_graycounter0_q_binary <= 5'd0;
	end
	multiregimpl70 <= tx_dp_cdc_graycounter1_q;
	multiregimpl71 <= multiregimpl70;
end

always @(posedge maceth_rx_clk) begin
	rxdatapath_liteethmacpreamblechecker_state <= rxdatapath_liteethmacpreamblechecker_next_state;
	if (liteethmaccore_pulsesynchronizer0_i) begin
		liteethmaccore_pulsesynchronizer0_toggle_i <= (~liteethmaccore_pulsesynchronizer0_toggle_i);
	end
	if (liteethmaccore_liteethmaccrc32checker_crc_ce) begin
		liteethmaccore_liteethmaccrc32checker_crc_reg <= liteethmaccore_liteethmaccrc32checker_crc_crc_next;
	end
	if (liteethmaccore_liteethmaccrc32checker_crc_reset) begin
		liteethmaccore_liteethmaccrc32checker_crc_reg <= 32'd4294967295;
	end
	if (((liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_we & liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_writable) & (~liteethmaccore_liteethmaccrc32checker_syncfifo_replace))) begin
		if ((liteethmaccore_liteethmaccrc32checker_syncfifo_produce == 3'd4)) begin
			liteethmaccore_liteethmaccrc32checker_syncfifo_produce <= 1'd0;
		end else begin
			liteethmaccore_liteethmaccrc32checker_syncfifo_produce <= (liteethmaccore_liteethmaccrc32checker_syncfifo_produce + 1'd1);
		end
	end
	if (liteethmaccore_liteethmaccrc32checker_syncfifo_do_read) begin
		if ((liteethmaccore_liteethmaccrc32checker_syncfifo_consume == 3'd4)) begin
			liteethmaccore_liteethmaccrc32checker_syncfifo_consume <= 1'd0;
		end else begin
			liteethmaccore_liteethmaccrc32checker_syncfifo_consume <= (liteethmaccore_liteethmaccrc32checker_syncfifo_consume + 1'd1);
		end
	end
	if (((liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_we & liteethmaccore_liteethmaccrc32checker_syncfifo_syncfifo_writable) & (~liteethmaccore_liteethmaccrc32checker_syncfifo_replace))) begin
		if ((~liteethmaccore_liteethmaccrc32checker_syncfifo_do_read)) begin
			liteethmaccore_liteethmaccrc32checker_syncfifo_level <= (liteethmaccore_liteethmaccrc32checker_syncfifo_level + 1'd1);
		end
	end else begin
		if (liteethmaccore_liteethmaccrc32checker_syncfifo_do_read) begin
			liteethmaccore_liteethmaccrc32checker_syncfifo_level <= (liteethmaccore_liteethmaccrc32checker_syncfifo_level - 1'd1);
		end
	end
	if (liteethmaccore_liteethmaccrc32checker_fifo_reset) begin
		liteethmaccore_liteethmaccrc32checker_syncfifo_level <= 3'd0;
		liteethmaccore_liteethmaccrc32checker_syncfifo_produce <= 3'd0;
		liteethmaccore_liteethmaccrc32checker_syncfifo_consume <= 3'd0;
	end
	rxdatapath_bufferizeendpoints_state <= rxdatapath_bufferizeendpoints_next_state;
	if (liteethmaccore_liteethmaccrc32checker_last_be_next_value_ce0) begin
		liteethmaccore_liteethmaccrc32checker_last_be <= liteethmaccore_liteethmaccrc32checker_last_be_next_value0;
	end
	if (liteethmaccore_liteethmaccrc32checker_crc_error1_next_value_ce1) begin
		liteethmaccore_liteethmaccrc32checker_crc_error1 <= liteethmaccore_liteethmaccrc32checker_crc_error1_next_value1;
	end
	if (((~liteethmaccore_bufferizeendpoints_pipe_valid_source_valid) | liteethmaccore_bufferizeendpoints_pipe_valid_source_ready)) begin
		liteethmaccore_bufferizeendpoints_pipe_valid_source_valid <= liteethmaccore_bufferizeendpoints_pipe_valid_sink_valid;
		liteethmaccore_bufferizeendpoints_pipe_valid_source_first <= liteethmaccore_bufferizeendpoints_pipe_valid_sink_first;
		liteethmaccore_bufferizeendpoints_pipe_valid_source_last <= liteethmaccore_bufferizeendpoints_pipe_valid_sink_last;
		liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_data <= liteethmaccore_bufferizeendpoints_pipe_valid_sink_payload_data;
		liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_last_be <= liteethmaccore_bufferizeendpoints_pipe_valid_sink_payload_last_be;
		liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_error <= liteethmaccore_bufferizeendpoints_pipe_valid_sink_payload_error;
	end
	if (liteethmaccore_pulsesynchronizer1_i) begin
		liteethmaccore_pulsesynchronizer1_toggle_i <= (~liteethmaccore_pulsesynchronizer1_toggle_i);
	end
	if ((liteethmaccore_rx_padding_sink_valid & liteethmaccore_rx_padding_sink_ready)) begin
		if (liteethmaccore_rx_padding_sink_last) begin
			liteethmaccore_rx_padding_length <= 1'd0;
		end else begin
			liteethmaccore_rx_padding_length <= (liteethmaccore_rx_padding_length + liteethmaccore_rx_padding_length_inc);
		end
	end
	if ((liteethmaccore_rx_converter_converter_sink_valid & liteethmaccore_rx_converter_converter_sink_ready)) begin
	end
	if (liteethmaccore_rx_converter_converter_source_ready) begin
		liteethmaccore_rx_converter_converter_strobe_all <= 1'd0;
	end
	if (liteethmaccore_rx_converter_converter_load_part) begin
		if (((liteethmaccore_rx_converter_converter_demux == 3'd7) | liteethmaccore_rx_converter_converter_sink_last)) begin
			liteethmaccore_rx_converter_converter_demux <= 1'd0;
			liteethmaccore_rx_converter_converter_strobe_all <= 1'd1;
		end else begin
			liteethmaccore_rx_converter_converter_demux <= (liteethmaccore_rx_converter_converter_demux + 1'd1);
		end
	end
	if ((liteethmaccore_rx_converter_converter_source_valid & liteethmaccore_rx_converter_converter_source_ready)) begin
		if ((liteethmaccore_rx_converter_converter_sink_valid & liteethmaccore_rx_converter_converter_sink_ready)) begin
			liteethmaccore_rx_converter_converter_source_first <= liteethmaccore_rx_converter_converter_sink_first;
			liteethmaccore_rx_converter_converter_source_last <= liteethmaccore_rx_converter_converter_sink_last;
		end else begin
			liteethmaccore_rx_converter_converter_source_first <= 1'd0;
			liteethmaccore_rx_converter_converter_source_last <= 1'd0;
		end
	end else begin
		if ((liteethmaccore_rx_converter_converter_sink_valid & liteethmaccore_rx_converter_converter_sink_ready)) begin
			liteethmaccore_rx_converter_converter_source_first <= (liteethmaccore_rx_converter_converter_sink_first | liteethmaccore_rx_converter_converter_source_first);
			liteethmaccore_rx_converter_converter_source_last <= (liteethmaccore_rx_converter_converter_sink_last | liteethmaccore_rx_converter_converter_source_last);
		end
	end
	if (liteethmaccore_rx_converter_converter_load_part) begin
		case (liteethmaccore_rx_converter_converter_demux)
			1'd0: begin
				liteethmaccore_rx_converter_converter_source_payload_data[9:0] <= liteethmaccore_rx_converter_converter_sink_payload_data;
			end
			1'd1: begin
				liteethmaccore_rx_converter_converter_source_payload_data[19:10] <= liteethmaccore_rx_converter_converter_sink_payload_data;
			end
			2'd2: begin
				liteethmaccore_rx_converter_converter_source_payload_data[29:20] <= liteethmaccore_rx_converter_converter_sink_payload_data;
			end
			2'd3: begin
				liteethmaccore_rx_converter_converter_source_payload_data[39:30] <= liteethmaccore_rx_converter_converter_sink_payload_data;
			end
			3'd4: begin
				liteethmaccore_rx_converter_converter_source_payload_data[49:40] <= liteethmaccore_rx_converter_converter_sink_payload_data;
			end
			3'd5: begin
				liteethmaccore_rx_converter_converter_source_payload_data[59:50] <= liteethmaccore_rx_converter_converter_sink_payload_data;
			end
			3'd6: begin
				liteethmaccore_rx_converter_converter_source_payload_data[69:60] <= liteethmaccore_rx_converter_converter_sink_payload_data;
			end
			3'd7: begin
				liteethmaccore_rx_converter_converter_source_payload_data[79:70] <= liteethmaccore_rx_converter_converter_sink_payload_data;
			end
		endcase
	end
	if (liteethmaccore_rx_converter_converter_load_part) begin
		liteethmaccore_rx_converter_converter_source_payload_valid_token_count <= (liteethmaccore_rx_converter_converter_demux + 1'd1);
	end
	liteethmaccore_rx_cdc_cdc_graycounter0_q_binary <= liteethmaccore_rx_cdc_cdc_graycounter0_q_next_binary;
	liteethmaccore_rx_cdc_cdc_graycounter0_q <= liteethmaccore_rx_cdc_cdc_graycounter0_q_next;
	if (maceth_rx_rst) begin
		liteethmaccore_liteethmaccrc32checker_crc_reg <= 32'd4294967295;
		liteethmaccore_liteethmaccrc32checker_syncfifo_level <= 3'd0;
		liteethmaccore_liteethmaccrc32checker_syncfifo_produce <= 3'd0;
		liteethmaccore_liteethmaccrc32checker_syncfifo_consume <= 3'd0;
		liteethmaccore_liteethmaccrc32checker_last_be <= 1'd0;
		liteethmaccore_liteethmaccrc32checker_crc_error1 <= 1'd0;
		liteethmaccore_bufferizeendpoints_pipe_valid_source_valid <= 1'd0;
		liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_data <= 8'd0;
		liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_last_be <= 1'd0;
		liteethmaccore_bufferizeendpoints_pipe_valid_source_payload_error <= 1'd0;
		liteethmaccore_rx_padding_length <= 11'd0;
		liteethmaccore_rx_converter_converter_source_payload_data <= 80'd0;
		liteethmaccore_rx_converter_converter_source_payload_valid_token_count <= 4'd0;
		liteethmaccore_rx_converter_converter_demux <= 3'd0;
		liteethmaccore_rx_converter_converter_strobe_all <= 1'd0;
		liteethmaccore_rx_cdc_cdc_graycounter0_q <= 6'd0;
		liteethmaccore_rx_cdc_cdc_graycounter0_q_binary <= 6'd0;
		rxdatapath_liteethmacpreamblechecker_state <= 1'd0;
		rxdatapath_bufferizeendpoints_state <= 2'd0;
	end
	multiregimpl50 <= liteethmaccore_rx_cdc_cdc_graycounter1_q;
	multiregimpl51 <= multiregimpl50;
end

always @(posedge maceth_tx_clk) begin
	liteethmaccore_tx_cdc_cdc_graycounter1_q_binary <= liteethmaccore_tx_cdc_cdc_graycounter1_q_next_binary;
	liteethmaccore_tx_cdc_cdc_graycounter1_q <= liteethmaccore_tx_cdc_cdc_graycounter1_q_next;
	if ((liteethmaccore_tx_converter_source_source_valid & liteethmaccore_tx_converter_source_source_ready)) begin
		if (liteethmaccore_tx_converter_last_be_drop) begin
			if (liteethmaccore_tx_converter_source_source_last) begin
				liteethmaccore_tx_converter_last_be_drop <= 1'd0;
			end
		end else begin
			if ((liteethmaccore_tx_converter_last_be_packet_end & (~liteethmaccore_tx_converter_source_source_last))) begin
				liteethmaccore_tx_converter_last_be_drop <= 1'd1;
			end
		end
	end
	if ((liteethmaccore_tx_converter_converter_source_valid & liteethmaccore_tx_converter_converter_source_ready)) begin
		if (liteethmaccore_tx_converter_converter_last) begin
			liteethmaccore_tx_converter_converter_mux <= 1'd0;
		end else begin
			liteethmaccore_tx_converter_converter_mux <= (liteethmaccore_tx_converter_converter_mux + 1'd1);
		end
	end
	txdatapath_liteethmactxlastbe_state <= txdatapath_liteethmactxlastbe_next_state;
	txdatapath_liteethmacpaddinginserter_state <= txdatapath_liteethmacpaddinginserter_next_state;
	if (liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value_ce) begin
		liteethmaccore_tx_padding_counter <= liteethmaccore_tx_padding_counter_clockdomainsrenamer0_next_value;
	end
	if (liteethmaccore_tx_crc_is_ongoing0) begin
		liteethmaccore_tx_crc_cnt <= 2'd3;
	end else begin
		if ((liteethmaccore_tx_crc_is_ongoing1 & (~liteethmaccore_tx_crc_cnt_done))) begin
			liteethmaccore_tx_crc_cnt <= (liteethmaccore_tx_crc_cnt - liteethmaccore_tx_crc_source_ready);
		end
	end
	if (liteethmaccore_tx_crc_ce) begin
		liteethmaccore_tx_crc_reg <= liteethmaccore_tx_crc_crc_next;
	end
	if (liteethmaccore_tx_crc_reset) begin
		liteethmaccore_tx_crc_reg <= 32'd4294967295;
	end
	txdatapath_bufferizeendpoints_state <= txdatapath_bufferizeendpoints_next_state;
	if (liteethmaccore_tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0) begin
		liteethmaccore_tx_crc_crc_packet <= liteethmaccore_tx_crc_crc_packet_clockdomainsrenamer1_next_value0;
	end
	if (liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value_ce1) begin
		liteethmaccore_tx_crc_last_be <= liteethmaccore_tx_crc_last_be_clockdomainsrenamer1_next_value1;
	end
	if (((~liteethmaccore_tx_crc_pipe_valid_source_valid) | liteethmaccore_tx_crc_pipe_valid_source_ready)) begin
		liteethmaccore_tx_crc_pipe_valid_source_valid <= liteethmaccore_tx_crc_pipe_valid_sink_valid;
		liteethmaccore_tx_crc_pipe_valid_source_first <= liteethmaccore_tx_crc_pipe_valid_sink_first;
		liteethmaccore_tx_crc_pipe_valid_source_last <= liteethmaccore_tx_crc_pipe_valid_sink_last;
		liteethmaccore_tx_crc_pipe_valid_source_payload_data <= liteethmaccore_tx_crc_pipe_valid_sink_payload_data;
		liteethmaccore_tx_crc_pipe_valid_source_payload_last_be <= liteethmaccore_tx_crc_pipe_valid_sink_payload_last_be;
		liteethmaccore_tx_crc_pipe_valid_source_payload_error <= liteethmaccore_tx_crc_pipe_valid_sink_payload_error;
	end
	txdatapath_liteethmacpreambleinserter_state <= txdatapath_liteethmacpreambleinserter_next_state;
	if (liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value_ce) begin
		liteethmaccore_tx_preamble_count <= liteethmaccore_tx_preamble_count_clockdomainsrenamer2_next_value;
	end
	txdatapath_liteethmacgap_state <= txdatapath_liteethmacgap_next_state;
	if (liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value_ce) begin
		liteethmaccore_tx_gap_counter <= liteethmaccore_tx_gap_counter_clockdomainsrenamer3_next_value;
	end
	if (maceth_tx_rst_1) begin
		liteethmaccore_tx_cdc_cdc_graycounter1_q <= 6'd0;
		liteethmaccore_tx_cdc_cdc_graycounter1_q_binary <= 6'd0;
		liteethmaccore_tx_converter_converter_mux <= 3'd0;
		liteethmaccore_tx_converter_last_be_drop <= 1'd0;
		liteethmaccore_tx_padding_counter <= 16'd0;
		liteethmaccore_tx_crc_reg <= 32'd4294967295;
		liteethmaccore_tx_crc_cnt <= 2'd3;
		liteethmaccore_tx_crc_pipe_valid_source_valid <= 1'd0;
		liteethmaccore_tx_crc_pipe_valid_source_payload_data <= 8'd0;
		liteethmaccore_tx_crc_pipe_valid_source_payload_last_be <= 1'd0;
		liteethmaccore_tx_crc_pipe_valid_source_payload_error <= 1'd0;
		txdatapath_liteethmactxlastbe_state <= 1'd0;
		txdatapath_liteethmacpaddinginserter_state <= 1'd0;
		txdatapath_bufferizeendpoints_state <= 2'd0;
		txdatapath_liteethmacpreambleinserter_state <= 2'd0;
		txdatapath_liteethmacgap_state <= 1'd0;
	end
	multiregimpl00 <= liteethmaccore_tx_cdc_cdc_graycounter0_q;
	multiregimpl01 <= multiregimpl00;
end

always @(posedge macsys_clk) begin
	liteethmaccore_tx_cdc_cdc_graycounter0_q_binary <= liteethmaccore_tx_cdc_cdc_graycounter0_q_next_binary;
	liteethmaccore_tx_cdc_cdc_graycounter0_q <= liteethmaccore_tx_cdc_cdc_graycounter0_q_next;
	if (liteethmaccore_pulsesynchronizer0_o) begin
		liteethmaccore_preamble_errors_status <= (liteethmaccore_preamble_errors_status + 1'd1);
	end
	if (liteethmaccore_pulsesynchronizer1_o) begin
		liteethmaccore_crc_errors_status <= (liteethmaccore_crc_errors_status + 1'd1);
	end
	liteethmaccore_pulsesynchronizer0_toggle_o_r <= liteethmaccore_pulsesynchronizer0_toggle_o;
	liteethmaccore_pulsesynchronizer1_toggle_o_r <= liteethmaccore_pulsesynchronizer1_toggle_o;
	liteethmaccore_rx_cdc_cdc_graycounter1_q_binary <= liteethmaccore_rx_cdc_cdc_graycounter1_q_next_binary;
	liteethmaccore_rx_cdc_cdc_graycounter1_q <= liteethmaccore_rx_cdc_cdc_graycounter1_q_next;
	if (packetfifo_payload_fifo_syncfifo_re) begin
		packetfifo_payload_fifo_readable <= 1'd1;
	end else begin
		if (packetfifo_payload_fifo_re) begin
			packetfifo_payload_fifo_readable <= 1'd0;
		end
	end
	if (((packetfifo_payload_fifo_syncfifo_we & packetfifo_payload_fifo_syncfifo_writable) & (~packetfifo_payload_fifo_replace))) begin
		packetfifo_payload_fifo_produce <= (packetfifo_payload_fifo_produce + 1'd1);
	end
	if (packetfifo_payload_fifo_do_read) begin
		packetfifo_payload_fifo_consume <= (packetfifo_payload_fifo_consume + 1'd1);
	end
	if (((packetfifo_payload_fifo_syncfifo_we & packetfifo_payload_fifo_syncfifo_writable) & (~packetfifo_payload_fifo_replace))) begin
		if ((~packetfifo_payload_fifo_do_read)) begin
			packetfifo_payload_fifo_level0 <= (packetfifo_payload_fifo_level0 + 1'd1);
		end
	end else begin
		if (packetfifo_payload_fifo_do_read) begin
			packetfifo_payload_fifo_level0 <= (packetfifo_payload_fifo_level0 - 1'd1);
		end
	end
	if (packetfifo_param_fifo_syncfifo_re) begin
		packetfifo_param_fifo_readable <= 1'd1;
	end else begin
		if (packetfifo_param_fifo_re) begin
			packetfifo_param_fifo_readable <= 1'd0;
		end
	end
	if (((packetfifo_param_fifo_syncfifo_we & packetfifo_param_fifo_syncfifo_writable) & (~packetfifo_param_fifo_replace))) begin
		if ((packetfifo_param_fifo_produce == 4'd8)) begin
			packetfifo_param_fifo_produce <= 1'd0;
		end else begin
			packetfifo_param_fifo_produce <= (packetfifo_param_fifo_produce + 1'd1);
		end
	end
	if (packetfifo_param_fifo_do_read) begin
		if ((packetfifo_param_fifo_consume == 4'd8)) begin
			packetfifo_param_fifo_consume <= 1'd0;
		end else begin
			packetfifo_param_fifo_consume <= (packetfifo_param_fifo_consume + 1'd1);
		end
	end
	if (((packetfifo_param_fifo_syncfifo_we & packetfifo_param_fifo_syncfifo_writable) & (~packetfifo_param_fifo_replace))) begin
		if ((~packetfifo_param_fifo_do_read)) begin
			packetfifo_param_fifo_level0 <= (packetfifo_param_fifo_level0 + 1'd1);
		end
	end else begin
		if (packetfifo_param_fifo_do_read) begin
			packetfifo_param_fifo_level0 <= (packetfifo_param_fifo_level0 - 1'd1);
		end
	end
	if ((tx_dp_cdc_re | (~tx_dp_cdc_readable))) begin
		tx_dp_cdc_dout <= tx_dp_cdc_asyncfifo_dout;
		tx_dp_cdc_readable <= tx_dp_cdc_asyncfifo_readable;
	end
	tx_dp_cdc_graycounter1_q_binary <= tx_dp_cdc_graycounter1_q_next_binary;
	tx_dp_cdc_graycounter1_q <= tx_dp_cdc_graycounter1_q_next;
	if (macsys_rst) begin
		liteethmaccore_tx_cdc_cdc_graycounter0_q <= 6'd0;
		liteethmaccore_tx_cdc_cdc_graycounter0_q_binary <= 6'd0;
		liteethmaccore_preamble_errors_status <= 32'd0;
		liteethmaccore_crc_errors_status <= 32'd0;
		liteethmaccore_rx_cdc_cdc_graycounter1_q <= 6'd0;
		liteethmaccore_rx_cdc_cdc_graycounter1_q_binary <= 6'd0;
		packetfifo_payload_fifo_readable <= 1'd0;
		packetfifo_payload_fifo_level0 <= 10'd0;
		packetfifo_payload_fifo_produce <= 9'd0;
		packetfifo_payload_fifo_consume <= 9'd0;
		packetfifo_param_fifo_readable <= 1'd0;
		packetfifo_param_fifo_level0 <= 4'd0;
		packetfifo_param_fifo_produce <= 4'd0;
		packetfifo_param_fifo_consume <= 4'd0;
		tx_dp_cdc_readable <= 1'd0;
		tx_dp_cdc_graycounter1_q <= 5'd0;
		tx_dp_cdc_graycounter1_q_binary <= 5'd0;
	end
	multiregimpl10 <= liteethmaccore_tx_cdc_cdc_graycounter1_q;
	multiregimpl11 <= multiregimpl10;
	multiregimpl20 <= liteethmaccore_pulsesynchronizer0_toggle_i;
	multiregimpl21 <= multiregimpl20;
	multiregimpl30 <= liteethmaccore_pulsesynchronizer1_toggle_i;
	multiregimpl31 <= multiregimpl30;
	multiregimpl40 <= liteethmaccore_rx_cdc_cdc_graycounter0_q;
	multiregimpl41 <= multiregimpl40;
	multiregimpl60 <= tx_dp_cdc_graycounter0_q;
	multiregimpl61 <= multiregimpl60;
end

always @(posedge resync_clk) begin
	simasyncresetsynchronizerimpl0_rst1 <= (eth_phy_rst | eth_rst);
	eth_tx_rst <= ((eth_phy_rst | eth_rst) | simasyncresetsynchronizerimpl0_rst1);
	simasyncresetsynchronizerimpl1_rst1 <= (eth_phy_rst | eth_rst);
	eth_rx_rst <= ((eth_phy_rst | eth_rst) | simasyncresetsynchronizerimpl1_rst1);
	simasyncresetsynchronizerimpl2_rst1 <= (sys_rst | reinit);
	macsys_rst <= ((sys_rst | reinit) | simasyncresetsynchronizerimpl2_rst1);
	simasyncresetsynchronizerimpl3_rst1 <= (dp_rst | reinit);
	macdp_rst <= ((dp_rst | reinit) | simasyncresetsynchronizerimpl3_rst1);
	simasyncresetsynchronizerimpl4_rst1 <= (eth_tx_rst | eth_rst);
	maceth_tx_rst_1 <= ((eth_tx_rst | eth_rst) | simasyncresetsynchronizerimpl4_rst1);
	simasyncresetsynchronizerimpl5_rst1 <= (eth_rx_rst | eth_rst);
	maceth_rx_rst <= ((eth_rx_rst | eth_rst) | simasyncresetsynchronizerimpl5_rst1);
end

reg [81:0] storage[0:31];
reg [4:0] memadr;
reg [4:0] memadr_1;
always @(posedge macsys_clk) begin
	if (liteethmaccore_tx_cdc_cdc_wrport_we)
		storage[liteethmaccore_tx_cdc_cdc_wrport_adr] <= liteethmaccore_tx_cdc_cdc_wrport_dat_w;
	memadr <= liteethmaccore_tx_cdc_cdc_wrport_adr;
end

always @(posedge maceth_tx_clk) begin
	memadr_1 <= liteethmaccore_tx_cdc_cdc_rdport_adr;
end

assign liteethmaccore_tx_cdc_cdc_wrport_dat_r = storage[memadr];
assign liteethmaccore_tx_cdc_cdc_rdport_dat_r = storage[memadr_1];

reg [11:0] storage_1[0:4];
reg [11:0] memdat;
always @(posedge maceth_rx_clk) begin
	if (liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_we)
		storage_1[liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_adr] <= liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_dat_w;
	memdat <= storage_1[liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_adr];
end

always @(posedge maceth_rx_clk) begin
end

assign liteethmaccore_liteethmaccrc32checker_syncfifo_wrport_dat_r = memdat;
assign liteethmaccore_liteethmaccrc32checker_syncfifo_rdport_dat_r = storage_1[liteethmaccore_liteethmaccrc32checker_syncfifo_rdport_adr];

reg [81:0] storage_2[0:31];
reg [4:0] memadr_2;
reg [4:0] memadr_3;
always @(posedge maceth_rx_clk) begin
	if (liteethmaccore_rx_cdc_cdc_wrport_we)
		storage_2[liteethmaccore_rx_cdc_cdc_wrport_adr] <= liteethmaccore_rx_cdc_cdc_wrport_dat_w;
	memadr_2 <= liteethmaccore_rx_cdc_cdc_wrport_adr;
end

always @(posedge macsys_clk) begin
	memadr_3 <= liteethmaccore_rx_cdc_cdc_rdport_adr;
end

assign liteethmaccore_rx_cdc_cdc_wrport_dat_r = storage_2[memadr_2];
assign liteethmaccore_rx_cdc_cdc_rdport_dat_r = storage_2[memadr_3];

reg [81:0] storage_3[0:511];
reg [81:0] memdat_1;
reg [81:0] memdat_2;
always @(posedge macsys_clk) begin
	if (packetfifo_payload_fifo_wrport_we)
		storage_3[packetfifo_payload_fifo_wrport_adr] <= packetfifo_payload_fifo_wrport_dat_w;
	memdat_1 <= storage_3[packetfifo_payload_fifo_wrport_adr];
end

always @(posedge macsys_clk) begin
	if (packetfifo_payload_fifo_rdport_re)
		memdat_2 <= storage_3[packetfifo_payload_fifo_rdport_adr];
end

assign packetfifo_payload_fifo_wrport_dat_r = memdat_1;
assign packetfifo_payload_fifo_rdport_dat_r = memdat_2;

reg [2:0] storage_4[0:8];
reg [2:0] memdat_3;
reg [2:0] memdat_4;
always @(posedge macsys_clk) begin
	if (packetfifo_param_fifo_wrport_we)
		storage_4[packetfifo_param_fifo_wrport_adr] <= packetfifo_param_fifo_wrport_dat_w;
	memdat_3 <= storage_4[packetfifo_param_fifo_wrport_adr];
end

always @(posedge macsys_clk) begin
	if (packetfifo_param_fifo_rdport_re)
		memdat_4 <= storage_4[packetfifo_param_fifo_rdport_adr];
end

assign packetfifo_param_fifo_wrport_dat_r = memdat_3;
assign packetfifo_param_fifo_rdport_dat_r = memdat_4;

reg [73:0] storage_5[0:15];
reg [3:0] memadr_4;
reg [3:0] memadr_5;
always @(posedge macdp_clk) begin
	if (tx_dp_cdc_wrport_we)
		storage_5[tx_dp_cdc_wrport_adr] <= tx_dp_cdc_wrport_dat_w;
	memadr_4 <= tx_dp_cdc_wrport_adr;
end

always @(posedge macsys_clk) begin
	memadr_5 <= tx_dp_cdc_rdport_adr;
end

assign tx_dp_cdc_wrport_dat_r = storage_5[memadr_4];
assign tx_dp_cdc_rdport_dat_r = storage_5[memadr_5];

endmodule


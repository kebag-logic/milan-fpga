/* Machine-generated using Migen */
module mac_tx_chain_mii(
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
reg [3:0] pads_tx_data = 4'd0;
reg pads_rx_dv = 1'd0;
reg [3:0] pads_rx_data = 4'd0;
wire liteethphymiitx_sink_valid;
wire liteethphymiitx_sink_ready;
wire liteethphymiitx_sink_first;
wire liteethphymiitx_sink_last;
wire [7:0] liteethphymiitx_sink_payload_data;
wire liteethphymiitx_sink_payload_last_be;
wire liteethphymiitx_sink_payload_error;
wire liteethphymiitx_converter_sink_valid;
wire liteethphymiitx_converter_sink_ready;
reg liteethphymiitx_converter_sink_first = 1'd0;
reg liteethphymiitx_converter_sink_last = 1'd0;
wire [7:0] liteethphymiitx_converter_sink_payload_data;
wire liteethphymiitx_converter_source_valid;
wire liteethphymiitx_converter_source_ready;
wire liteethphymiitx_converter_source_first;
wire liteethphymiitx_converter_source_last;
reg [3:0] liteethphymiitx_converter_source_payload_data;
wire liteethphymiitx_converter_source_payload_valid_token_count;
reg liteethphymiitx_converter_mux = 1'd0;
wire liteethphymiitx_converter_first;
wire liteethphymiitx_converter_last;
wire liteethphymiitx_source_source_valid;
wire liteethphymiitx_source_source_ready;
wire liteethphymiitx_source_source_first;
wire liteethphymiitx_source_source_last;
wire [3:0] liteethphymiitx_source_source_payload_data;
wire liteethphymiirx_source_valid;
wire liteethphymiirx_source_ready;
wire liteethphymiirx_source_first;
wire liteethphymiirx_source_last;
wire [7:0] liteethphymiirx_source_payload_data;
reg liteethphymiirx_source_payload_last_be = 1'd0;
reg liteethphymiirx_source_payload_error = 1'd0;
reg liteethphymiirx_converter_sink_valid = 1'd0;
wire liteethphymiirx_converter_sink_ready;
reg liteethphymiirx_converter_sink_first = 1'd0;
wire liteethphymiirx_converter_sink_last;
reg [3:0] liteethphymiirx_converter_sink_payload_data = 4'd0;
wire liteethphymiirx_converter_source_valid;
wire liteethphymiirx_converter_source_ready;
reg liteethphymiirx_converter_source_first = 1'd0;
reg liteethphymiirx_converter_source_last = 1'd0;
reg [7:0] liteethphymiirx_converter_source_payload_data = 8'd0;
reg [1:0] liteethphymiirx_converter_source_payload_valid_token_count = 2'd0;
reg liteethphymiirx_converter_demux = 1'd0;
wire liteethphymiirx_converter_load_part;
reg liteethphymiirx_converter_strobe_all = 1'd0;
wire liteethphymiirx_source_source_valid;
wire liteethphymiirx_source_source_ready;
wire liteethphymiirx_source_source_first;
wire liteethphymiirx_source_source_last;
wire [7:0] liteethphymiirx_source_source_payload_data;
reg liteethphymiirx_reset = 1'd0;
wire sink_valid;
wire sink_ready;
wire sink_first;
wire sink_last;
wire [63:0] sink_payload_data;
wire [7:0] sink_payload_last_be;
wire [7:0] sink_payload_error;
wire source_valid;
reg source_ready;
wire source_first;
wire source_last;
wire [63:0] source_payload_data;
wire [7:0] source_payload_last_be;
wire [7:0] source_payload_error;
wire tx_cdc_sink_sink_valid;
wire tx_cdc_sink_sink_ready;
wire tx_cdc_sink_sink_first;
wire tx_cdc_sink_sink_last;
wire [63:0] tx_cdc_sink_sink_payload_data;
wire [7:0] tx_cdc_sink_sink_payload_last_be;
wire [7:0] tx_cdc_sink_sink_payload_error;
wire tx_cdc_source_source_valid;
wire tx_cdc_source_source_ready;
wire tx_cdc_source_source_first;
wire tx_cdc_source_source_last;
wire [63:0] tx_cdc_source_source_payload_data;
wire [7:0] tx_cdc_source_source_payload_last_be;
wire [7:0] tx_cdc_source_source_payload_error;
wire tx_cdc_cdc_sink_valid;
wire tx_cdc_cdc_sink_ready;
wire tx_cdc_cdc_sink_first;
wire tx_cdc_cdc_sink_last;
wire [63:0] tx_cdc_cdc_sink_payload_data;
wire [7:0] tx_cdc_cdc_sink_payload_last_be;
wire [7:0] tx_cdc_cdc_sink_payload_error;
wire tx_cdc_cdc_source_valid;
wire tx_cdc_cdc_source_ready;
wire tx_cdc_cdc_source_first;
wire tx_cdc_cdc_source_last;
wire [63:0] tx_cdc_cdc_source_payload_data;
wire [7:0] tx_cdc_cdc_source_payload_last_be;
wire [7:0] tx_cdc_cdc_source_payload_error;
wire tx_cdc_cdc_asyncfifo_we;
wire tx_cdc_cdc_asyncfifo_writable;
wire tx_cdc_cdc_asyncfifo_re;
wire tx_cdc_cdc_asyncfifo_readable;
wire [81:0] tx_cdc_cdc_asyncfifo_din;
wire [81:0] tx_cdc_cdc_asyncfifo_dout;
wire tx_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [5:0] tx_cdc_cdc_graycounter0_q = 6'd0;
wire [5:0] tx_cdc_cdc_graycounter0_q_next;
reg [5:0] tx_cdc_cdc_graycounter0_q_binary = 6'd0;
reg [5:0] tx_cdc_cdc_graycounter0_q_next_binary;
wire tx_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [5:0] tx_cdc_cdc_graycounter1_q = 6'd0;
wire [5:0] tx_cdc_cdc_graycounter1_q_next;
reg [5:0] tx_cdc_cdc_graycounter1_q_binary = 6'd0;
reg [5:0] tx_cdc_cdc_graycounter1_q_next_binary;
wire [5:0] tx_cdc_cdc_produce_rdomain;
wire [5:0] tx_cdc_cdc_consume_wdomain;
wire [4:0] tx_cdc_cdc_wrport_adr;
wire [81:0] tx_cdc_cdc_wrport_dat_r;
wire tx_cdc_cdc_wrport_we;
wire [81:0] tx_cdc_cdc_wrport_dat_w;
wire [4:0] tx_cdc_cdc_rdport_adr;
wire [81:0] tx_cdc_cdc_rdport_dat_r;
wire [63:0] tx_cdc_cdc_fifo_in_payload_data;
wire [7:0] tx_cdc_cdc_fifo_in_payload_last_be;
wire [7:0] tx_cdc_cdc_fifo_in_payload_error;
wire tx_cdc_cdc_fifo_in_first;
wire tx_cdc_cdc_fifo_in_last;
wire [63:0] tx_cdc_cdc_fifo_out_payload_data;
wire [7:0] tx_cdc_cdc_fifo_out_payload_last_be;
wire [7:0] tx_cdc_cdc_fifo_out_payload_error;
wire tx_cdc_cdc_fifo_out_first;
wire tx_cdc_cdc_fifo_out_last;
wire tx_converter_sink_valid;
wire tx_converter_sink_ready;
wire tx_converter_sink_first;
wire tx_converter_sink_last;
wire [63:0] tx_converter_sink_payload_data;
wire [7:0] tx_converter_sink_payload_last_be;
wire [7:0] tx_converter_sink_payload_error;
wire tx_converter_source_valid;
wire tx_converter_source_ready;
wire tx_converter_source_first;
wire tx_converter_source_last;
wire [7:0] tx_converter_source_payload_data;
wire tx_converter_source_payload_last_be;
wire tx_converter_source_payload_error;
wire tx_converter_converter_sink_valid;
wire tx_converter_converter_sink_ready;
wire tx_converter_converter_sink_first;
wire tx_converter_converter_sink_last;
reg [79:0] tx_converter_converter_sink_payload_data;
wire tx_converter_converter_source_valid;
wire tx_converter_converter_source_ready;
wire tx_converter_converter_source_first;
wire tx_converter_converter_source_last;
reg [9:0] tx_converter_converter_source_payload_data;
wire tx_converter_converter_source_payload_valid_token_count;
reg [2:0] tx_converter_converter_mux = 3'd0;
wire tx_converter_converter_first;
wire tx_converter_converter_last;
wire tx_converter_source_source_valid;
wire tx_converter_source_source_ready;
wire tx_converter_source_source_first;
wire tx_converter_source_source_last;
wire [9:0] tx_converter_source_source_payload_data;
reg tx_converter_last_be_drop = 1'd0;
wire tx_converter_last_be_packet_end;
wire tx_last_be_sink_sink_valid;
wire tx_last_be_sink_sink_ready;
wire tx_last_be_sink_sink_first;
wire tx_last_be_sink_sink_last;
wire [7:0] tx_last_be_sink_sink_payload_data;
wire tx_last_be_sink_sink_payload_last_be;
wire tx_last_be_sink_sink_payload_error;
wire tx_last_be_source_source_valid;
wire tx_last_be_source_source_ready;
wire tx_last_be_source_source_first;
wire tx_last_be_source_source_last;
wire [7:0] tx_last_be_source_source_payload_data;
wire tx_last_be_source_source_payload_last_be;
wire tx_last_be_source_source_payload_error;
wire tx_last_be_last_handler_sink_valid;
reg tx_last_be_last_handler_sink_ready;
wire tx_last_be_last_handler_sink_first;
wire tx_last_be_last_handler_sink_last;
wire [7:0] tx_last_be_last_handler_sink_payload_data;
wire tx_last_be_last_handler_sink_payload_last_be;
wire tx_last_be_last_handler_sink_payload_error;
reg tx_last_be_last_handler_source_valid;
wire tx_last_be_last_handler_source_ready;
reg tx_last_be_last_handler_source_first;
reg tx_last_be_last_handler_source_last;
reg [7:0] tx_last_be_last_handler_source_payload_data;
reg tx_last_be_last_handler_source_payload_last_be;
reg tx_last_be_last_handler_source_payload_error;
wire tx_padding_sink_valid;
reg tx_padding_sink_ready;
wire tx_padding_sink_first;
wire tx_padding_sink_last;
wire [7:0] tx_padding_sink_payload_data;
wire tx_padding_sink_payload_last_be;
wire tx_padding_sink_payload_error;
reg tx_padding_source_valid;
wire tx_padding_source_ready;
reg tx_padding_source_first;
reg tx_padding_source_last;
reg [7:0] tx_padding_source_payload_data;
reg tx_padding_source_payload_last_be;
reg tx_padding_source_payload_error;
reg [15:0] tx_padding_counter = 16'd0;
wire tx_padding_counter_done;
wire tx_crc_sink_valid;
reg tx_crc_sink_ready;
wire tx_crc_sink_first;
wire tx_crc_sink_last;
wire [7:0] tx_crc_sink_payload_data;
wire tx_crc_sink_payload_last_be;
wire tx_crc_sink_payload_error;
reg tx_crc_source_valid;
wire tx_crc_source_ready;
reg tx_crc_source_first;
reg tx_crc_source_last;
reg [7:0] tx_crc_source_payload_data;
reg tx_crc_source_payload_last_be;
reg tx_crc_source_payload_error;
reg [31:0] tx_crc_crc_packet = 32'd0;
reg tx_crc_last_be = 1'd0;
wire [7:0] tx_crc_data0;
wire tx_crc_be;
reg [31:0] tx_crc_value;
reg tx_crc_error;
wire [7:0] tx_crc_data1;
wire [31:0] tx_crc_crc_prev;
reg [31:0] tx_crc_crc_next;
reg [31:0] tx_crc_reg = 32'd4294967295;
reg tx_crc_ce;
reg tx_crc_reset;
reg [1:0] tx_crc_cnt = 2'd3;
wire tx_crc_cnt_done;
reg tx_crc_is_ongoing0;
reg tx_crc_is_ongoing1;
wire tx_crc_sink_sink_valid;
wire tx_crc_sink_sink_ready;
wire tx_crc_sink_sink_first;
wire tx_crc_sink_sink_last;
wire [7:0] tx_crc_sink_sink_payload_data;
wire tx_crc_sink_sink_payload_last_be;
wire tx_crc_sink_sink_payload_error;
wire tx_crc_source_source_valid;
wire tx_crc_source_source_ready;
wire tx_crc_source_source_first;
wire tx_crc_source_source_last;
wire [7:0] tx_crc_source_source_payload_data;
wire tx_crc_source_source_payload_last_be;
wire tx_crc_source_source_payload_error;
wire tx_crc_pipe_valid_sink_valid;
wire tx_crc_pipe_valid_sink_ready;
wire tx_crc_pipe_valid_sink_first;
wire tx_crc_pipe_valid_sink_last;
wire [7:0] tx_crc_pipe_valid_sink_payload_data;
wire tx_crc_pipe_valid_sink_payload_last_be;
wire tx_crc_pipe_valid_sink_payload_error;
reg tx_crc_pipe_valid_source_valid = 1'd0;
wire tx_crc_pipe_valid_source_ready;
reg tx_crc_pipe_valid_source_first = 1'd0;
reg tx_crc_pipe_valid_source_last = 1'd0;
reg [7:0] tx_crc_pipe_valid_source_payload_data = 8'd0;
reg tx_crc_pipe_valid_source_payload_last_be = 1'd0;
reg tx_crc_pipe_valid_source_payload_error = 1'd0;
wire tx_preamble_sink_valid;
reg tx_preamble_sink_ready;
wire tx_preamble_sink_first;
wire tx_preamble_sink_last;
wire [7:0] tx_preamble_sink_payload_data;
wire tx_preamble_sink_payload_last_be;
wire tx_preamble_sink_payload_error;
reg tx_preamble_source_valid;
wire tx_preamble_source_ready;
reg tx_preamble_source_first;
reg tx_preamble_source_last;
reg [7:0] tx_preamble_source_payload_data;
wire tx_preamble_source_payload_last_be;
reg tx_preamble_source_payload_error;
reg [63:0] tx_preamble_preamble = 64'd15372286728091293013;
reg [2:0] tx_preamble_count = 3'd0;
wire tx_gap_sink_valid;
reg tx_gap_sink_ready;
wire tx_gap_sink_first;
wire tx_gap_sink_last;
wire [7:0] tx_gap_sink_payload_data;
wire tx_gap_sink_payload_last_be;
wire tx_gap_sink_payload_error;
reg tx_gap_source_valid;
wire tx_gap_source_ready;
reg tx_gap_source_first;
reg tx_gap_source_last;
reg [7:0] tx_gap_source_payload_data;
reg tx_gap_source_payload_last_be;
reg tx_gap_source_payload_error;
reg [3:0] tx_gap_counter = 4'd0;
reg [31:0] preamble_errors_status = 32'd0;
reg [31:0] crc_errors_status = 32'd0;
wire rx_preamble_sink_valid;
reg rx_preamble_sink_ready;
wire rx_preamble_sink_first;
wire rx_preamble_sink_last;
wire [7:0] rx_preamble_sink_payload_data;
wire rx_preamble_sink_payload_last_be;
wire rx_preamble_sink_payload_error;
reg rx_preamble_source_valid;
wire rx_preamble_source_ready;
reg rx_preamble_source_first;
reg rx_preamble_source_last;
wire [7:0] rx_preamble_source_payload_data;
wire rx_preamble_source_payload_last_be;
reg rx_preamble_source_payload_error;
reg rx_preamble_error;
reg [63:0] rx_preamble_preamble = 64'd15372286728091293013;
wire pulsesynchronizer0_i;
wire pulsesynchronizer0_o;
reg pulsesynchronizer0_toggle_i = 1'd0;
wire pulsesynchronizer0_toggle_o;
reg pulsesynchronizer0_toggle_o_r = 1'd0;
wire liteethmaccrc32checker_sink_sink_valid;
reg liteethmaccrc32checker_sink_sink_ready;
wire liteethmaccrc32checker_sink_sink_first;
wire liteethmaccrc32checker_sink_sink_last;
wire [7:0] liteethmaccrc32checker_sink_sink_payload_data;
wire liteethmaccrc32checker_sink_sink_payload_last_be;
wire liteethmaccrc32checker_sink_sink_payload_error;
reg liteethmaccrc32checker_source_source_valid;
wire liteethmaccrc32checker_source_source_ready;
wire liteethmaccrc32checker_source_source_first;
reg liteethmaccrc32checker_source_source_last;
wire [7:0] liteethmaccrc32checker_source_source_payload_data;
reg liteethmaccrc32checker_source_source_payload_last_be;
reg liteethmaccrc32checker_source_source_payload_error;
reg liteethmaccrc32checker_error;
wire [7:0] liteethmaccrc32checker_crc_data0;
wire liteethmaccrc32checker_crc_be;
reg liteethmaccrc32checker_crc_error0;
reg [7:0] liteethmaccrc32checker_crc_data1;
wire [31:0] liteethmaccrc32checker_crc_crc_prev;
reg [31:0] liteethmaccrc32checker_crc_crc_next;
reg [31:0] liteethmaccrc32checker_crc_reg = 32'd4294967295;
reg liteethmaccrc32checker_crc_ce;
reg liteethmaccrc32checker_crc_reset;
reg liteethmaccrc32checker_syncfifo_sink_valid;
wire liteethmaccrc32checker_syncfifo_sink_ready;
wire liteethmaccrc32checker_syncfifo_sink_first;
wire liteethmaccrc32checker_syncfifo_sink_last;
wire [7:0] liteethmaccrc32checker_syncfifo_sink_payload_data;
wire liteethmaccrc32checker_syncfifo_sink_payload_last_be;
wire liteethmaccrc32checker_syncfifo_sink_payload_error;
wire liteethmaccrc32checker_syncfifo_source_valid;
reg liteethmaccrc32checker_syncfifo_source_ready;
wire liteethmaccrc32checker_syncfifo_source_first;
wire liteethmaccrc32checker_syncfifo_source_last;
wire [7:0] liteethmaccrc32checker_syncfifo_source_payload_data;
wire liteethmaccrc32checker_syncfifo_source_payload_last_be;
wire liteethmaccrc32checker_syncfifo_source_payload_error;
wire liteethmaccrc32checker_syncfifo_syncfifo_we;
wire liteethmaccrc32checker_syncfifo_syncfifo_writable;
wire liteethmaccrc32checker_syncfifo_syncfifo_re;
wire liteethmaccrc32checker_syncfifo_syncfifo_readable;
wire [11:0] liteethmaccrc32checker_syncfifo_syncfifo_din;
wire [11:0] liteethmaccrc32checker_syncfifo_syncfifo_dout;
reg [2:0] liteethmaccrc32checker_syncfifo_level = 3'd0;
reg liteethmaccrc32checker_syncfifo_replace = 1'd0;
reg [2:0] liteethmaccrc32checker_syncfifo_produce = 3'd0;
reg [2:0] liteethmaccrc32checker_syncfifo_consume = 3'd0;
reg [2:0] liteethmaccrc32checker_syncfifo_wrport_adr;
wire [11:0] liteethmaccrc32checker_syncfifo_wrport_dat_r;
wire liteethmaccrc32checker_syncfifo_wrport_we;
wire [11:0] liteethmaccrc32checker_syncfifo_wrport_dat_w;
wire liteethmaccrc32checker_syncfifo_do_read;
wire [2:0] liteethmaccrc32checker_syncfifo_rdport_adr;
wire [11:0] liteethmaccrc32checker_syncfifo_rdport_dat_r;
wire [7:0] liteethmaccrc32checker_syncfifo_fifo_in_payload_data;
wire liteethmaccrc32checker_syncfifo_fifo_in_payload_last_be;
wire liteethmaccrc32checker_syncfifo_fifo_in_payload_error;
wire liteethmaccrc32checker_syncfifo_fifo_in_first;
wire liteethmaccrc32checker_syncfifo_fifo_in_last;
wire [7:0] liteethmaccrc32checker_syncfifo_fifo_out_payload_data;
wire liteethmaccrc32checker_syncfifo_fifo_out_payload_last_be;
wire liteethmaccrc32checker_syncfifo_fifo_out_payload_error;
wire liteethmaccrc32checker_syncfifo_fifo_out_first;
wire liteethmaccrc32checker_syncfifo_fifo_out_last;
reg liteethmaccrc32checker_fifo_reset;
wire liteethmaccrc32checker_fifo_in;
wire liteethmaccrc32checker_fifo_out;
wire liteethmaccrc32checker_fifo_full;
reg liteethmaccrc32checker_last_be = 1'd0;
reg liteethmaccrc32checker_crc_error1 = 1'd0;
wire bufferizeendpoints_sink_sink_valid;
wire bufferizeendpoints_sink_sink_ready;
wire bufferizeendpoints_sink_sink_first;
wire bufferizeendpoints_sink_sink_last;
wire [7:0] bufferizeendpoints_sink_sink_payload_data;
wire bufferizeendpoints_sink_sink_payload_last_be;
wire bufferizeendpoints_sink_sink_payload_error;
wire bufferizeendpoints_source_source_valid;
wire bufferizeendpoints_source_source_ready;
wire bufferizeendpoints_source_source_first;
wire bufferizeendpoints_source_source_last;
wire [7:0] bufferizeendpoints_source_source_payload_data;
wire bufferizeendpoints_source_source_payload_last_be;
wire bufferizeendpoints_source_source_payload_error;
wire bufferizeendpoints_pipe_valid_sink_valid;
wire bufferizeendpoints_pipe_valid_sink_ready;
wire bufferizeendpoints_pipe_valid_sink_first;
wire bufferizeendpoints_pipe_valid_sink_last;
wire [7:0] bufferizeendpoints_pipe_valid_sink_payload_data;
wire bufferizeendpoints_pipe_valid_sink_payload_last_be;
wire bufferizeendpoints_pipe_valid_sink_payload_error;
reg bufferizeendpoints_pipe_valid_source_valid = 1'd0;
wire bufferizeendpoints_pipe_valid_source_ready;
reg bufferizeendpoints_pipe_valid_source_first = 1'd0;
reg bufferizeendpoints_pipe_valid_source_last = 1'd0;
reg [7:0] bufferizeendpoints_pipe_valid_source_payload_data = 8'd0;
reg bufferizeendpoints_pipe_valid_source_payload_last_be = 1'd0;
reg bufferizeendpoints_pipe_valid_source_payload_error = 1'd0;
wire pulsesynchronizer1_i;
wire pulsesynchronizer1_o;
reg pulsesynchronizer1_toggle_i = 1'd0;
wire pulsesynchronizer1_toggle_o;
reg pulsesynchronizer1_toggle_o_r = 1'd0;
wire rx_padding_sink_valid;
wire rx_padding_sink_ready;
wire rx_padding_sink_first;
wire rx_padding_sink_last;
wire [7:0] rx_padding_sink_payload_data;
wire rx_padding_sink_payload_last_be;
wire rx_padding_sink_payload_error;
wire rx_padding_source_valid;
wire rx_padding_source_ready;
wire rx_padding_source_first;
wire rx_padding_source_last;
wire [7:0] rx_padding_source_payload_data;
wire rx_padding_source_payload_last_be;
reg rx_padding_source_payload_error;
reg [10:0] rx_padding_length = 11'd0;
reg [3:0] rx_padding_length_inc;
wire rx_last_be_sink_valid;
wire rx_last_be_sink_ready;
wire rx_last_be_sink_first;
wire rx_last_be_sink_last;
wire [7:0] rx_last_be_sink_payload_data;
wire rx_last_be_sink_payload_last_be;
wire rx_last_be_sink_payload_error;
wire rx_last_be_source_valid;
wire rx_last_be_source_ready;
wire rx_last_be_source_first;
wire rx_last_be_source_last;
wire [7:0] rx_last_be_source_payload_data;
reg rx_last_be_source_payload_last_be;
wire rx_last_be_source_payload_error;
wire rx_converter_sink_valid;
wire rx_converter_sink_ready;
wire rx_converter_sink_first;
wire rx_converter_sink_last;
wire [7:0] rx_converter_sink_payload_data;
wire rx_converter_sink_payload_last_be;
wire rx_converter_sink_payload_error;
wire rx_converter_source_valid;
wire rx_converter_source_ready;
wire rx_converter_source_first;
wire rx_converter_source_last;
reg [63:0] rx_converter_source_payload_data;
reg [7:0] rx_converter_source_payload_last_be;
reg [7:0] rx_converter_source_payload_error;
wire rx_converter_converter_sink_valid;
wire rx_converter_converter_sink_ready;
wire rx_converter_converter_sink_first;
wire rx_converter_converter_sink_last;
wire [9:0] rx_converter_converter_sink_payload_data;
wire rx_converter_converter_source_valid;
wire rx_converter_converter_source_ready;
reg rx_converter_converter_source_first = 1'd0;
reg rx_converter_converter_source_last = 1'd0;
reg [79:0] rx_converter_converter_source_payload_data = 80'd0;
reg [3:0] rx_converter_converter_source_payload_valid_token_count = 4'd0;
reg [2:0] rx_converter_converter_demux = 3'd0;
wire rx_converter_converter_load_part;
reg rx_converter_converter_strobe_all = 1'd0;
wire rx_converter_source_source_valid;
wire rx_converter_source_source_ready;
wire rx_converter_source_source_first;
wire rx_converter_source_source_last;
wire [79:0] rx_converter_source_source_payload_data;
wire rx_cdc_sink_sink_valid;
wire rx_cdc_sink_sink_ready;
wire rx_cdc_sink_sink_first;
wire rx_cdc_sink_sink_last;
wire [63:0] rx_cdc_sink_sink_payload_data;
wire [7:0] rx_cdc_sink_sink_payload_last_be;
wire [7:0] rx_cdc_sink_sink_payload_error;
wire rx_cdc_source_source_valid;
wire rx_cdc_source_source_ready;
wire rx_cdc_source_source_first;
wire rx_cdc_source_source_last;
wire [63:0] rx_cdc_source_source_payload_data;
wire [7:0] rx_cdc_source_source_payload_last_be;
wire [7:0] rx_cdc_source_source_payload_error;
wire rx_cdc_cdc_sink_valid;
wire rx_cdc_cdc_sink_ready;
wire rx_cdc_cdc_sink_first;
wire rx_cdc_cdc_sink_last;
wire [63:0] rx_cdc_cdc_sink_payload_data;
wire [7:0] rx_cdc_cdc_sink_payload_last_be;
wire [7:0] rx_cdc_cdc_sink_payload_error;
wire rx_cdc_cdc_source_valid;
wire rx_cdc_cdc_source_ready;
wire rx_cdc_cdc_source_first;
wire rx_cdc_cdc_source_last;
wire [63:0] rx_cdc_cdc_source_payload_data;
wire [7:0] rx_cdc_cdc_source_payload_last_be;
wire [7:0] rx_cdc_cdc_source_payload_error;
wire rx_cdc_cdc_asyncfifo_we;
wire rx_cdc_cdc_asyncfifo_writable;
wire rx_cdc_cdc_asyncfifo_re;
wire rx_cdc_cdc_asyncfifo_readable;
wire [81:0] rx_cdc_cdc_asyncfifo_din;
wire [81:0] rx_cdc_cdc_asyncfifo_dout;
wire rx_cdc_cdc_graycounter0_ce;
(* no_retiming = "true" *) reg [5:0] rx_cdc_cdc_graycounter0_q = 6'd0;
wire [5:0] rx_cdc_cdc_graycounter0_q_next;
reg [5:0] rx_cdc_cdc_graycounter0_q_binary = 6'd0;
reg [5:0] rx_cdc_cdc_graycounter0_q_next_binary;
wire rx_cdc_cdc_graycounter1_ce;
(* no_retiming = "true" *) reg [5:0] rx_cdc_cdc_graycounter1_q = 6'd0;
wire [5:0] rx_cdc_cdc_graycounter1_q_next;
reg [5:0] rx_cdc_cdc_graycounter1_q_binary = 6'd0;
reg [5:0] rx_cdc_cdc_graycounter1_q_next_binary;
wire [5:0] rx_cdc_cdc_produce_rdomain;
wire [5:0] rx_cdc_cdc_consume_wdomain;
wire [4:0] rx_cdc_cdc_wrport_adr;
wire [81:0] rx_cdc_cdc_wrport_dat_r;
wire rx_cdc_cdc_wrport_we;
wire [81:0] rx_cdc_cdc_wrport_dat_w;
wire [4:0] rx_cdc_cdc_rdport_adr;
wire [81:0] rx_cdc_cdc_rdport_dat_r;
wire [63:0] rx_cdc_cdc_fifo_in_payload_data;
wire [7:0] rx_cdc_cdc_fifo_in_payload_last_be;
wire [7:0] rx_cdc_cdc_fifo_in_payload_error;
wire rx_cdc_cdc_fifo_in_first;
wire rx_cdc_cdc_fifo_in_last;
wire [63:0] rx_cdc_cdc_fifo_out_payload_data;
wire [7:0] rx_cdc_cdc_fifo_out_payload_last_be;
wire [7:0] rx_cdc_cdc_fifo_out_payload_error;
wire rx_cdc_cdc_fifo_out_first;
wire rx_cdc_cdc_fifo_out_last;
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
wire [3:0] array_write_memory0_adr;
wire [71:0] array_write_memory0_dat_r;
wire array_write_memory0_we;
wire [71:0] array_write_memory0_dat_w;
wire [3:0] array_read_memory0_adr;
wire [71:0] array_read_memory0_dat_r;
wire [3:0] array_write_memory1_adr;
wire [1:0] array_write_memory1_dat_r;
wire array_write_memory1_we;
wire [1:0] array_write_memory1_dat_w;
wire [3:0] array_read_memory1_adr;
wire [1:0] array_read_memory1_dat_r;
reg txdatapath_liteethmactxlastbe_state = 1'd0;
reg txdatapath_liteethmactxlastbe_next_state;
reg txdatapath_liteethmacpaddinginserter_state = 1'd0;
reg txdatapath_liteethmacpaddinginserter_next_state;
reg [15:0] tx_padding_counter_clockdomainsrenamer0_next_value;
reg tx_padding_counter_clockdomainsrenamer0_next_value_ce;
reg [1:0] txdatapath_bufferizeendpoints_state = 2'd0;
reg [1:0] txdatapath_bufferizeendpoints_next_state;
reg [31:0] tx_crc_crc_packet_clockdomainsrenamer1_next_value0;
reg tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0;
reg tx_crc_last_be_clockdomainsrenamer1_next_value1;
reg tx_crc_last_be_clockdomainsrenamer1_next_value_ce1;
reg [1:0] txdatapath_liteethmacpreambleinserter_state = 2'd0;
reg [1:0] txdatapath_liteethmacpreambleinserter_next_state;
reg [2:0] tx_preamble_count_clockdomainsrenamer2_next_value;
reg tx_preamble_count_clockdomainsrenamer2_next_value_ce;
reg txdatapath_liteethmacgap_state = 1'd0;
reg txdatapath_liteethmacgap_next_state;
reg [3:0] tx_gap_counter_clockdomainsrenamer3_next_value;
reg tx_gap_counter_clockdomainsrenamer3_next_value_ce;
reg rxdatapath_liteethmacpreamblechecker_state = 1'd0;
reg rxdatapath_liteethmacpreamblechecker_next_state;
reg [1:0] rxdatapath_bufferizeendpoints_state = 2'd0;
reg [1:0] rxdatapath_bufferizeendpoints_next_state;
reg liteethmaccrc32checker_last_be_next_value0;
reg liteethmaccrc32checker_last_be_next_value_ce0;
reg liteethmaccrc32checker_crc_error1_next_value1;
reg liteethmaccrc32checker_crc_error1_next_value_ce1;
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
assign sink_valid = packetfifo_source_source_valid;
assign packetfifo_source_source_ready = sink_ready;
assign sink_first = packetfifo_source_source_first;
assign sink_last = packetfifo_source_source_last;
assign sink_payload_data = packetfifo_source_source_payload_data;
assign sink_payload_last_be = packetfifo_source_source_payload_last_be;
assign sink_payload_error = packetfifo_source_source_payload_error;
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
	source_ready <= 1'd0;
	packetfifo_sink_sink_valid <= 1'd0;
	tx_dp_source_source_ready <= 1'd0;
	if (loopback) begin
		packetfifo_sink_sink_valid <= 1'd0;
		source_ready <= 1'd0;
	end else begin
		packetfifo_sink_sink_valid <= tx_dp_source_source_valid;
		tx_dp_source_source_ready <= packetfifo_sink_sink_ready;
		source_ready <= 1'd1;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end
assign phy_sink_valid = liteethphymiitx_sink_valid;
assign phy_sink_ready = liteethphymiitx_sink_ready;
assign phy_sink_data = liteethphymiitx_sink_payload_data;
assign phy_sink_last = liteethphymiitx_sink_last;
assign gmii_tx_en = pads_tx_en;
assign gmii_tx_data = pads_tx_data;
assign gmii_tx_er = 1'd0;
assign maceth_tx_rst = maceth_tx_rst_1;
assign liteethphymiitx_converter_sink_valid = liteethphymiitx_sink_valid;
assign liteethphymiitx_converter_sink_payload_data = liteethphymiitx_sink_payload_data;
assign liteethphymiitx_sink_ready = liteethphymiitx_converter_sink_ready;
assign liteethphymiitx_source_source_ready = 1'd1;
assign liteethphymiitx_source_source_valid = liteethphymiitx_converter_source_valid;
assign liteethphymiitx_converter_source_ready = liteethphymiitx_source_source_ready;
assign liteethphymiitx_source_source_first = liteethphymiitx_converter_source_first;
assign liteethphymiitx_source_source_last = liteethphymiitx_converter_source_last;
assign liteethphymiitx_source_source_payload_data = liteethphymiitx_converter_source_payload_data;
assign liteethphymiitx_converter_first = (liteethphymiitx_converter_mux == 1'd0);
assign liteethphymiitx_converter_last = (liteethphymiitx_converter_mux == 1'd1);
assign liteethphymiitx_converter_source_valid = liteethphymiitx_converter_sink_valid;
assign liteethphymiitx_converter_source_first = (liteethphymiitx_converter_sink_first & liteethphymiitx_converter_first);
assign liteethphymiitx_converter_source_last = (liteethphymiitx_converter_sink_last & liteethphymiitx_converter_last);
assign liteethphymiitx_converter_sink_ready = (liteethphymiitx_converter_last & liteethphymiitx_converter_source_ready);

// synthesis translate_off
reg dummy_d_1;
// synthesis translate_on
always @(*) begin
	liteethphymiitx_converter_source_payload_data <= 4'd0;
	case (liteethphymiitx_converter_mux)
		1'd0: begin
			liteethphymiitx_converter_source_payload_data <= liteethphymiitx_converter_sink_payload_data[3:0];
		end
		default: begin
			liteethphymiitx_converter_source_payload_data <= liteethphymiitx_converter_sink_payload_data[7:4];
		end
	endcase
// synthesis translate_off
	dummy_d_1 <= dummy_s;
// synthesis translate_on
end
assign liteethphymiitx_converter_source_payload_valid_token_count = liteethphymiitx_converter_last;
assign liteethphymiirx_converter_sink_last = (~pads_rx_dv);
assign liteethphymiirx_source_valid = liteethphymiirx_source_source_valid;
assign liteethphymiirx_source_source_ready = liteethphymiirx_source_ready;
assign liteethphymiirx_source_first = liteethphymiirx_source_source_first;
assign liteethphymiirx_source_last = liteethphymiirx_source_source_last;
assign liteethphymiirx_source_payload_data = liteethphymiirx_source_source_payload_data;
assign liteethphymiirx_source_source_valid = liteethphymiirx_converter_source_valid;
assign liteethphymiirx_converter_source_ready = liteethphymiirx_source_source_ready;
assign liteethphymiirx_source_source_first = liteethphymiirx_converter_source_first;
assign liteethphymiirx_source_source_last = liteethphymiirx_converter_source_last;
assign liteethphymiirx_source_source_payload_data = liteethphymiirx_converter_source_payload_data;
assign liteethphymiirx_converter_sink_ready = ((~liteethphymiirx_converter_strobe_all) | liteethphymiirx_converter_source_ready);
assign liteethphymiirx_converter_source_valid = liteethphymiirx_converter_strobe_all;
assign liteethphymiirx_converter_load_part = (liteethphymiirx_converter_sink_valid & liteethphymiirx_converter_sink_ready);
assign tx_cdc_cdc_sink_valid = tx_cdc_sink_sink_valid;
assign tx_cdc_sink_sink_ready = tx_cdc_cdc_sink_ready;
assign tx_cdc_cdc_sink_first = tx_cdc_sink_sink_first;
assign tx_cdc_cdc_sink_last = tx_cdc_sink_sink_last;
assign tx_cdc_cdc_sink_payload_data = tx_cdc_sink_sink_payload_data;
assign tx_cdc_cdc_sink_payload_last_be = tx_cdc_sink_sink_payload_last_be;
assign tx_cdc_cdc_sink_payload_error = tx_cdc_sink_sink_payload_error;
assign tx_cdc_source_source_valid = tx_cdc_cdc_source_valid;
assign tx_cdc_cdc_source_ready = tx_cdc_source_source_ready;
assign tx_cdc_source_source_first = tx_cdc_cdc_source_first;
assign tx_cdc_source_source_last = tx_cdc_cdc_source_last;
assign tx_cdc_source_source_payload_data = tx_cdc_cdc_source_payload_data;
assign tx_cdc_source_source_payload_last_be = tx_cdc_cdc_source_payload_last_be;
assign tx_cdc_source_source_payload_error = tx_cdc_cdc_source_payload_error;
assign tx_cdc_cdc_asyncfifo_din = {tx_cdc_cdc_fifo_in_last, tx_cdc_cdc_fifo_in_first, tx_cdc_cdc_fifo_in_payload_error, tx_cdc_cdc_fifo_in_payload_last_be, tx_cdc_cdc_fifo_in_payload_data};
assign {tx_cdc_cdc_fifo_out_last, tx_cdc_cdc_fifo_out_first, tx_cdc_cdc_fifo_out_payload_error, tx_cdc_cdc_fifo_out_payload_last_be, tx_cdc_cdc_fifo_out_payload_data} = tx_cdc_cdc_asyncfifo_dout;
assign tx_cdc_cdc_sink_ready = tx_cdc_cdc_asyncfifo_writable;
assign tx_cdc_cdc_asyncfifo_we = tx_cdc_cdc_sink_valid;
assign tx_cdc_cdc_fifo_in_first = tx_cdc_cdc_sink_first;
assign tx_cdc_cdc_fifo_in_last = tx_cdc_cdc_sink_last;
assign tx_cdc_cdc_fifo_in_payload_data = tx_cdc_cdc_sink_payload_data;
assign tx_cdc_cdc_fifo_in_payload_last_be = tx_cdc_cdc_sink_payload_last_be;
assign tx_cdc_cdc_fifo_in_payload_error = tx_cdc_cdc_sink_payload_error;
assign tx_cdc_cdc_source_valid = tx_cdc_cdc_asyncfifo_readable;
assign tx_cdc_cdc_source_first = tx_cdc_cdc_fifo_out_first;
assign tx_cdc_cdc_source_last = tx_cdc_cdc_fifo_out_last;
assign tx_cdc_cdc_source_payload_data = tx_cdc_cdc_fifo_out_payload_data;
assign tx_cdc_cdc_source_payload_last_be = tx_cdc_cdc_fifo_out_payload_last_be;
assign tx_cdc_cdc_source_payload_error = tx_cdc_cdc_fifo_out_payload_error;
assign tx_cdc_cdc_asyncfifo_re = tx_cdc_cdc_source_ready;
assign tx_cdc_cdc_graycounter0_ce = (tx_cdc_cdc_asyncfifo_writable & tx_cdc_cdc_asyncfifo_we);
assign tx_cdc_cdc_graycounter1_ce = (tx_cdc_cdc_asyncfifo_readable & tx_cdc_cdc_asyncfifo_re);
assign tx_cdc_cdc_asyncfifo_writable = (((tx_cdc_cdc_graycounter0_q[5] == tx_cdc_cdc_consume_wdomain[5]) | (tx_cdc_cdc_graycounter0_q[4] == tx_cdc_cdc_consume_wdomain[4])) | (tx_cdc_cdc_graycounter0_q[3:0] != tx_cdc_cdc_consume_wdomain[3:0]));
assign tx_cdc_cdc_asyncfifo_readable = (tx_cdc_cdc_graycounter1_q != tx_cdc_cdc_produce_rdomain);
assign tx_cdc_cdc_wrport_adr = tx_cdc_cdc_graycounter0_q_binary[4:0];
assign tx_cdc_cdc_wrport_dat_w = tx_cdc_cdc_asyncfifo_din;
assign tx_cdc_cdc_wrport_we = tx_cdc_cdc_graycounter0_ce;
assign tx_cdc_cdc_rdport_adr = tx_cdc_cdc_graycounter1_q_next_binary[4:0];
assign tx_cdc_cdc_asyncfifo_dout = tx_cdc_cdc_rdport_dat_r;

// synthesis translate_off
reg dummy_d_2;
// synthesis translate_on
always @(*) begin
	tx_cdc_cdc_graycounter0_q_next_binary <= 6'd0;
	if (tx_cdc_cdc_graycounter0_ce) begin
		tx_cdc_cdc_graycounter0_q_next_binary <= (tx_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		tx_cdc_cdc_graycounter0_q_next_binary <= tx_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_2 <= dummy_s;
// synthesis translate_on
end
assign tx_cdc_cdc_graycounter0_q_next = (tx_cdc_cdc_graycounter0_q_next_binary ^ tx_cdc_cdc_graycounter0_q_next_binary[5:1]);

// synthesis translate_off
reg dummy_d_3;
// synthesis translate_on
always @(*) begin
	tx_cdc_cdc_graycounter1_q_next_binary <= 6'd0;
	if (tx_cdc_cdc_graycounter1_ce) begin
		tx_cdc_cdc_graycounter1_q_next_binary <= (tx_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		tx_cdc_cdc_graycounter1_q_next_binary <= tx_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_3 <= dummy_s;
// synthesis translate_on
end
assign tx_cdc_cdc_graycounter1_q_next = (tx_cdc_cdc_graycounter1_q_next_binary ^ tx_cdc_cdc_graycounter1_q_next_binary[5:1]);
assign tx_converter_converter_sink_valid = tx_converter_sink_valid;
assign tx_converter_converter_sink_first = tx_converter_sink_first;
assign tx_converter_converter_sink_last = tx_converter_sink_last;
assign tx_converter_sink_ready = tx_converter_converter_sink_ready;

// synthesis translate_off
reg dummy_d_4;
// synthesis translate_on
always @(*) begin
	tx_converter_converter_sink_payload_data <= 80'd0;
	tx_converter_converter_sink_payload_data[7:0] <= tx_converter_sink_payload_data[7:0];
	tx_converter_converter_sink_payload_data[8] <= tx_converter_sink_payload_last_be[0];
	tx_converter_converter_sink_payload_data[9] <= tx_converter_sink_payload_error[0];
	tx_converter_converter_sink_payload_data[17:10] <= tx_converter_sink_payload_data[15:8];
	tx_converter_converter_sink_payload_data[18] <= tx_converter_sink_payload_last_be[1];
	tx_converter_converter_sink_payload_data[19] <= tx_converter_sink_payload_error[1];
	tx_converter_converter_sink_payload_data[27:20] <= tx_converter_sink_payload_data[23:16];
	tx_converter_converter_sink_payload_data[28] <= tx_converter_sink_payload_last_be[2];
	tx_converter_converter_sink_payload_data[29] <= tx_converter_sink_payload_error[2];
	tx_converter_converter_sink_payload_data[37:30] <= tx_converter_sink_payload_data[31:24];
	tx_converter_converter_sink_payload_data[38] <= tx_converter_sink_payload_last_be[3];
	tx_converter_converter_sink_payload_data[39] <= tx_converter_sink_payload_error[3];
	tx_converter_converter_sink_payload_data[47:40] <= tx_converter_sink_payload_data[39:32];
	tx_converter_converter_sink_payload_data[48] <= tx_converter_sink_payload_last_be[4];
	tx_converter_converter_sink_payload_data[49] <= tx_converter_sink_payload_error[4];
	tx_converter_converter_sink_payload_data[57:50] <= tx_converter_sink_payload_data[47:40];
	tx_converter_converter_sink_payload_data[58] <= tx_converter_sink_payload_last_be[5];
	tx_converter_converter_sink_payload_data[59] <= tx_converter_sink_payload_error[5];
	tx_converter_converter_sink_payload_data[67:60] <= tx_converter_sink_payload_data[55:48];
	tx_converter_converter_sink_payload_data[68] <= tx_converter_sink_payload_last_be[6];
	tx_converter_converter_sink_payload_data[69] <= tx_converter_sink_payload_error[6];
	tx_converter_converter_sink_payload_data[77:70] <= tx_converter_sink_payload_data[63:56];
	tx_converter_converter_sink_payload_data[78] <= tx_converter_sink_payload_last_be[7];
	tx_converter_converter_sink_payload_data[79] <= tx_converter_sink_payload_error[7];
// synthesis translate_off
	dummy_d_4 <= dummy_s;
// synthesis translate_on
end
assign tx_converter_last_be_packet_end = (tx_converter_sink_last & (tx_converter_source_payload_last_be != 1'd0));
assign tx_converter_source_valid = (tx_converter_source_source_valid & (~tx_converter_last_be_drop));
assign tx_converter_source_first = (tx_converter_source_source_first & (~tx_converter_last_be_drop));
assign tx_converter_source_last = (tx_converter_source_source_last | tx_converter_last_be_packet_end);
assign tx_converter_source_source_ready = (tx_converter_source_ready | tx_converter_last_be_drop);
assign {tx_converter_source_payload_error, tx_converter_source_payload_last_be, tx_converter_source_payload_data} = tx_converter_source_source_payload_data;
assign tx_converter_source_source_valid = tx_converter_converter_source_valid;
assign tx_converter_converter_source_ready = tx_converter_source_source_ready;
assign tx_converter_source_source_first = tx_converter_converter_source_first;
assign tx_converter_source_source_last = tx_converter_converter_source_last;
assign tx_converter_source_source_payload_data = tx_converter_converter_source_payload_data;
assign tx_converter_converter_first = (tx_converter_converter_mux == 1'd0);
assign tx_converter_converter_last = (tx_converter_converter_mux == 3'd7);
assign tx_converter_converter_source_valid = tx_converter_converter_sink_valid;
assign tx_converter_converter_source_first = (tx_converter_converter_sink_first & tx_converter_converter_first);
assign tx_converter_converter_source_last = (tx_converter_converter_sink_last & tx_converter_converter_last);
assign tx_converter_converter_sink_ready = (tx_converter_converter_last & tx_converter_converter_source_ready);

// synthesis translate_off
reg dummy_d_5;
// synthesis translate_on
always @(*) begin
	tx_converter_converter_source_payload_data <= 10'd0;
	case (tx_converter_converter_mux)
		1'd0: begin
			tx_converter_converter_source_payload_data <= tx_converter_converter_sink_payload_data[9:0];
		end
		1'd1: begin
			tx_converter_converter_source_payload_data <= tx_converter_converter_sink_payload_data[19:10];
		end
		2'd2: begin
			tx_converter_converter_source_payload_data <= tx_converter_converter_sink_payload_data[29:20];
		end
		2'd3: begin
			tx_converter_converter_source_payload_data <= tx_converter_converter_sink_payload_data[39:30];
		end
		3'd4: begin
			tx_converter_converter_source_payload_data <= tx_converter_converter_sink_payload_data[49:40];
		end
		3'd5: begin
			tx_converter_converter_source_payload_data <= tx_converter_converter_sink_payload_data[59:50];
		end
		3'd6: begin
			tx_converter_converter_source_payload_data <= tx_converter_converter_sink_payload_data[69:60];
		end
		default: begin
			tx_converter_converter_source_payload_data <= tx_converter_converter_sink_payload_data[79:70];
		end
	endcase
// synthesis translate_off
	dummy_d_5 <= dummy_s;
// synthesis translate_on
end
assign tx_converter_converter_source_payload_valid_token_count = tx_converter_converter_last;
assign tx_last_be_last_handler_sink_valid = tx_last_be_sink_sink_valid;
assign tx_last_be_sink_sink_ready = tx_last_be_last_handler_sink_ready;
assign tx_last_be_last_handler_sink_first = tx_last_be_sink_sink_first;
assign tx_last_be_last_handler_sink_last = tx_last_be_sink_sink_last;
assign tx_last_be_last_handler_sink_payload_data = tx_last_be_sink_sink_payload_data;
assign tx_last_be_last_handler_sink_payload_last_be = tx_last_be_sink_sink_payload_last_be;
assign tx_last_be_last_handler_sink_payload_error = tx_last_be_sink_sink_payload_error;
assign tx_last_be_source_source_valid = tx_last_be_last_handler_source_valid;
assign tx_last_be_last_handler_source_ready = tx_last_be_source_source_ready;
assign tx_last_be_source_source_first = tx_last_be_last_handler_source_first;
assign tx_last_be_source_source_last = tx_last_be_last_handler_source_last;
assign tx_last_be_source_source_payload_data = tx_last_be_last_handler_source_payload_data;
assign tx_last_be_source_source_payload_last_be = tx_last_be_last_handler_source_payload_last_be;
assign tx_last_be_source_source_payload_error = tx_last_be_last_handler_source_payload_error;

// synthesis translate_off
reg dummy_d_6;
// synthesis translate_on
always @(*) begin
	tx_last_be_last_handler_sink_ready <= 1'd0;
	tx_last_be_last_handler_source_valid <= 1'd0;
	tx_last_be_last_handler_source_first <= 1'd0;
	tx_last_be_last_handler_source_last <= 1'd0;
	tx_last_be_last_handler_source_payload_data <= 8'd0;
	tx_last_be_last_handler_source_payload_last_be <= 1'd0;
	tx_last_be_last_handler_source_payload_error <= 1'd0;
	txdatapath_liteethmactxlastbe_next_state <= 1'd0;
	txdatapath_liteethmactxlastbe_next_state <= txdatapath_liteethmactxlastbe_state;
	case (txdatapath_liteethmactxlastbe_state)
		1'd1: begin
			tx_last_be_last_handler_sink_ready <= 1'd1;
			if ((tx_last_be_last_handler_sink_valid & tx_last_be_last_handler_sink_last)) begin
				txdatapath_liteethmactxlastbe_next_state <= 1'd0;
			end
		end
		default: begin
			tx_last_be_last_handler_source_valid <= tx_last_be_last_handler_sink_valid;
			tx_last_be_last_handler_sink_ready <= tx_last_be_last_handler_source_ready;
			tx_last_be_last_handler_source_first <= tx_last_be_last_handler_sink_first;
			tx_last_be_last_handler_source_last <= tx_last_be_last_handler_sink_last;
			tx_last_be_last_handler_source_payload_data <= tx_last_be_last_handler_sink_payload_data;
			tx_last_be_last_handler_source_payload_last_be <= tx_last_be_last_handler_sink_payload_last_be;
			tx_last_be_last_handler_source_payload_error <= tx_last_be_last_handler_sink_payload_error;
			tx_last_be_last_handler_source_last <= (tx_last_be_last_handler_sink_payload_last_be != 1'd0);
			if ((tx_last_be_last_handler_sink_valid & tx_last_be_last_handler_sink_ready)) begin
				if ((tx_last_be_last_handler_source_last & (~tx_last_be_last_handler_sink_last))) begin
					txdatapath_liteethmactxlastbe_next_state <= 1'd1;
				end
			end
		end
	endcase
// synthesis translate_off
	dummy_d_6 <= dummy_s;
// synthesis translate_on
end
assign tx_padding_counter_done = (tx_padding_counter >= 6'd59);

// synthesis translate_off
reg dummy_d_7;
// synthesis translate_on
always @(*) begin
	tx_padding_sink_ready <= 1'd0;
	tx_padding_source_valid <= 1'd0;
	tx_padding_source_first <= 1'd0;
	tx_padding_source_last <= 1'd0;
	tx_padding_source_payload_data <= 8'd0;
	tx_padding_source_payload_last_be <= 1'd0;
	tx_padding_source_payload_error <= 1'd0;
	txdatapath_liteethmacpaddinginserter_next_state <= 1'd0;
	tx_padding_counter_clockdomainsrenamer0_next_value <= 16'd0;
	tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd0;
	txdatapath_liteethmacpaddinginserter_next_state <= txdatapath_liteethmacpaddinginserter_state;
	case (txdatapath_liteethmacpaddinginserter_state)
		1'd1: begin
			tx_padding_source_valid <= 1'd1;
			if (tx_padding_counter_done) begin
				tx_padding_source_payload_last_be <= 1'd1;
				tx_padding_source_last <= 1'd1;
			end
			tx_padding_source_payload_data <= 1'd0;
			if ((tx_padding_source_valid & tx_padding_source_ready)) begin
				tx_padding_counter_clockdomainsrenamer0_next_value <= (tx_padding_counter + 1'd1);
				tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd1;
				if (tx_padding_counter_done) begin
					tx_padding_counter_clockdomainsrenamer0_next_value <= 1'd0;
					tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd1;
					txdatapath_liteethmacpaddinginserter_next_state <= 1'd0;
				end
			end
		end
		default: begin
			tx_padding_source_valid <= tx_padding_sink_valid;
			tx_padding_sink_ready <= tx_padding_source_ready;
			tx_padding_source_first <= tx_padding_sink_first;
			tx_padding_source_last <= tx_padding_sink_last;
			tx_padding_source_payload_data <= tx_padding_sink_payload_data;
			tx_padding_source_payload_last_be <= tx_padding_sink_payload_last_be;
			tx_padding_source_payload_error <= tx_padding_sink_payload_error;
			if ((tx_padding_source_valid & tx_padding_source_ready)) begin
				tx_padding_counter_clockdomainsrenamer0_next_value <= (tx_padding_counter + 1'd1);
				tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd1;
				if (tx_padding_sink_last) begin
					if ((~tx_padding_counter_done)) begin
						tx_padding_source_last <= 1'd0;
						tx_padding_source_payload_last_be <= 1'd0;
						txdatapath_liteethmacpaddinginserter_next_state <= 1'd1;
					end else begin
						if (((tx_padding_counter == 6'd59) & (tx_padding_sink_payload_last_be < 1'd1))) begin
							tx_padding_source_payload_last_be <= 1'd1;
						end else begin
							tx_padding_counter_clockdomainsrenamer0_next_value <= 1'd0;
							tx_padding_counter_clockdomainsrenamer0_next_value_ce <= 1'd1;
						end
					end
				end
			end
		end
	endcase
// synthesis translate_off
	dummy_d_7 <= dummy_s;
// synthesis translate_on
end
assign tx_crc_data0 = tx_crc_sink_payload_data;
assign tx_crc_be = tx_crc_sink_payload_last_be;
assign tx_crc_cnt_done = (tx_crc_cnt == 1'd0);
assign tx_crc_sink_valid = tx_crc_source_source_valid;
assign tx_crc_source_source_ready = tx_crc_sink_ready;
assign tx_crc_sink_first = tx_crc_source_source_first;
assign tx_crc_sink_last = tx_crc_source_source_last;
assign tx_crc_sink_payload_data = tx_crc_source_source_payload_data;
assign tx_crc_sink_payload_last_be = tx_crc_source_source_payload_last_be;
assign tx_crc_sink_payload_error = tx_crc_source_source_payload_error;
assign tx_crc_data1 = tx_crc_data0;
assign tx_crc_crc_prev = tx_crc_reg;

// synthesis translate_off
reg dummy_d_8;
// synthesis translate_on
always @(*) begin
	tx_crc_value <= 32'd0;
	tx_crc_error <= 1'd0;
	if (tx_crc_be) begin
		tx_crc_value <= ({tx_crc_crc_next[0], tx_crc_crc_next[1], tx_crc_crc_next[2], tx_crc_crc_next[3], tx_crc_crc_next[4], tx_crc_crc_next[5], tx_crc_crc_next[6], tx_crc_crc_next[7], tx_crc_crc_next[8], tx_crc_crc_next[9], tx_crc_crc_next[10], tx_crc_crc_next[11], tx_crc_crc_next[12], tx_crc_crc_next[13], tx_crc_crc_next[14], tx_crc_crc_next[15], tx_crc_crc_next[16], tx_crc_crc_next[17], tx_crc_crc_next[18], tx_crc_crc_next[19], tx_crc_crc_next[20], tx_crc_crc_next[21], tx_crc_crc_next[22], tx_crc_crc_next[23], tx_crc_crc_next[24], tx_crc_crc_next[25], tx_crc_crc_next[26], tx_crc_crc_next[27], tx_crc_crc_next[28], tx_crc_crc_next[29], tx_crc_crc_next[30], tx_crc_crc_next[31]} ^ 32'd4294967295);
		tx_crc_error <= (tx_crc_crc_next != 32'd3338984827);
	end
// synthesis translate_off
	dummy_d_8 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_9;
// synthesis translate_on
always @(*) begin
	tx_crc_crc_next <= 32'd0;
	tx_crc_crc_next[0] <= (((tx_crc_crc_prev[24] ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[1] <= (((((((tx_crc_crc_prev[25] ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_data1[6]) ^ tx_crc_crc_prev[24]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[2] <= (((((((((tx_crc_crc_prev[26] ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[25]) ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_data1[6]) ^ tx_crc_crc_prev[24]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[3] <= (((((((tx_crc_crc_prev[27] ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[25]) ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_data1[6]);
	tx_crc_crc_next[4] <= (((((((((tx_crc_crc_prev[28] ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[24]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[5] <= (((((((((((((tx_crc_crc_prev[29] ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[25]) ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_data1[6]) ^ tx_crc_crc_prev[24]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[6] <= (((((((((((tx_crc_crc_prev[30] ^ tx_crc_data1[1]) ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[25]) ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_data1[6]);
	tx_crc_crc_next[7] <= (((((((((tx_crc_crc_prev[31] ^ tx_crc_data1[0]) ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[24]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[8] <= ((((((((tx_crc_crc_prev[0] ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[25]) ^ tx_crc_data1[6]) ^ tx_crc_crc_prev[24]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[9] <= ((((((((tx_crc_crc_prev[1] ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[25]) ^ tx_crc_data1[6]);
	tx_crc_crc_next[10] <= ((((((((tx_crc_crc_prev[2] ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[24]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[11] <= ((((((((tx_crc_crc_prev[3] ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[25]) ^ tx_crc_data1[6]) ^ tx_crc_crc_prev[24]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[12] <= ((((((((((((tx_crc_crc_prev[4] ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[25]) ^ tx_crc_data1[6]) ^ tx_crc_crc_prev[24]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[13] <= ((((((((((((tx_crc_crc_prev[5] ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[25]) ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_data1[6]);
	tx_crc_crc_next[14] <= ((((((((((tx_crc_crc_prev[6] ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]);
	tx_crc_crc_next[15] <= ((((((((tx_crc_crc_prev[7] ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]);
	tx_crc_crc_next[16] <= ((((((tx_crc_crc_prev[8] ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[24]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[17] <= ((((((tx_crc_crc_prev[9] ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[25]) ^ tx_crc_data1[6]);
	tx_crc_crc_next[18] <= ((((((tx_crc_crc_prev[10] ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]);
	tx_crc_crc_next[19] <= ((((tx_crc_crc_prev[11] ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]);
	tx_crc_crc_next[20] <= ((tx_crc_crc_prev[12] ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]);
	tx_crc_crc_next[21] <= ((tx_crc_crc_prev[13] ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]);
	tx_crc_crc_next[22] <= ((tx_crc_crc_prev[14] ^ tx_crc_crc_prev[24]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[23] <= ((((((tx_crc_crc_prev[15] ^ tx_crc_crc_prev[25]) ^ tx_crc_data1[6]) ^ tx_crc_crc_prev[24]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[24] <= ((((((tx_crc_crc_prev[16] ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]) ^ tx_crc_crc_prev[25]) ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_data1[6]);
	tx_crc_crc_next[25] <= ((((tx_crc_crc_prev[17] ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]);
	tx_crc_crc_next[26] <= ((((((((tx_crc_crc_prev[18] ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]) ^ tx_crc_crc_prev[24]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_data1[7]);
	tx_crc_crc_next[27] <= ((((((((tx_crc_crc_prev[19] ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]) ^ tx_crc_crc_prev[25]) ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_data1[6]);
	tx_crc_crc_next[28] <= ((((((tx_crc_crc_prev[20] ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]) ^ tx_crc_crc_prev[26]) ^ tx_crc_data1[5]);
	tx_crc_crc_next[29] <= ((((((tx_crc_crc_prev[21] ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_crc_prev[30]) ^ tx_crc_data1[1]) ^ tx_crc_crc_prev[27]) ^ tx_crc_data1[4]);
	tx_crc_crc_next[30] <= ((((tx_crc_crc_prev[22] ^ tx_crc_crc_prev[31]) ^ tx_crc_data1[0]) ^ tx_crc_crc_prev[28]) ^ tx_crc_data1[3]);
	tx_crc_crc_next[31] <= ((tx_crc_crc_prev[23] ^ tx_crc_crc_prev[29]) ^ tx_crc_data1[2]);
// synthesis translate_off
	dummy_d_9 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_10;
// synthesis translate_on
always @(*) begin
	tx_crc_sink_ready <= 1'd0;
	tx_crc_source_valid <= 1'd0;
	tx_crc_source_first <= 1'd0;
	tx_crc_source_last <= 1'd0;
	tx_crc_source_payload_data <= 8'd0;
	tx_crc_source_payload_last_be <= 1'd0;
	tx_crc_source_payload_error <= 1'd0;
	tx_crc_ce <= 1'd0;
	tx_crc_reset <= 1'd0;
	tx_crc_is_ongoing0 <= 1'd0;
	tx_crc_is_ongoing1 <= 1'd0;
	txdatapath_bufferizeendpoints_next_state <= 2'd0;
	tx_crc_crc_packet_clockdomainsrenamer1_next_value0 <= 32'd0;
	tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0 <= 1'd0;
	tx_crc_last_be_clockdomainsrenamer1_next_value1 <= 1'd0;
	tx_crc_last_be_clockdomainsrenamer1_next_value_ce1 <= 1'd0;
	txdatapath_bufferizeendpoints_next_state <= txdatapath_bufferizeendpoints_state;
	case (txdatapath_bufferizeendpoints_state)
		1'd1: begin
			tx_crc_ce <= (tx_crc_sink_valid & tx_crc_source_ready);
			tx_crc_source_valid <= tx_crc_sink_valid;
			tx_crc_sink_ready <= tx_crc_source_ready;
			tx_crc_source_first <= tx_crc_sink_first;
			tx_crc_source_last <= tx_crc_sink_last;
			tx_crc_source_payload_data <= tx_crc_sink_payload_data;
			tx_crc_source_payload_last_be <= tx_crc_sink_payload_last_be;
			tx_crc_source_payload_error <= tx_crc_sink_payload_error;
			tx_crc_source_last <= 1'd0;
			tx_crc_source_payload_last_be <= 1'd0;
			if (tx_crc_sink_last) begin
				if (tx_crc_sink_payload_last_be) begin
					tx_crc_source_payload_data <= slice_proxy[7:0];
				end
				if ((1'd0 & (tx_crc_sink_payload_last_be <= 4'd15))) begin
					tx_crc_source_last <= 1'd1;
					tx_crc_source_payload_last_be <= (tx_crc_sink_payload_last_be <<< 3'sd5);
				end
			end
			if (((tx_crc_sink_valid & tx_crc_sink_last) & tx_crc_source_ready)) begin
				if ((1'd0 & (tx_crc_sink_payload_last_be <= 4'd15))) begin
					txdatapath_bufferizeendpoints_next_state <= 1'd0;
				end else begin
					tx_crc_crc_packet_clockdomainsrenamer1_next_value0 <= tx_crc_value;
					tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0 <= 1'd1;
					if (1'd0) begin
						tx_crc_last_be_clockdomainsrenamer1_next_value1 <= (tx_crc_sink_payload_last_be >>> 3'd4);
						tx_crc_last_be_clockdomainsrenamer1_next_value_ce1 <= 1'd1;
					end else begin
						tx_crc_last_be_clockdomainsrenamer1_next_value1 <= tx_crc_sink_payload_last_be;
						tx_crc_last_be_clockdomainsrenamer1_next_value_ce1 <= 1'd1;
					end
					txdatapath_bufferizeendpoints_next_state <= 2'd2;
				end
			end
		end
		2'd2: begin
			tx_crc_source_valid <= 1'd1;
			case (tx_crc_cnt)
				1'd0: begin
					tx_crc_source_payload_data <= tx_crc_crc_packet[31:24];
				end
				1'd1: begin
					tx_crc_source_payload_data <= tx_crc_crc_packet[23:16];
				end
				2'd2: begin
					tx_crc_source_payload_data <= tx_crc_crc_packet[15:8];
				end
				default: begin
					tx_crc_source_payload_data <= tx_crc_crc_packet[7:0];
				end
			endcase
			if (tx_crc_cnt_done) begin
				tx_crc_source_last <= 1'd1;
				if (tx_crc_source_ready) begin
					txdatapath_bufferizeendpoints_next_state <= 1'd0;
				end
			end
			tx_crc_is_ongoing1 <= 1'd1;
		end
		default: begin
			tx_crc_reset <= 1'd1;
			tx_crc_sink_ready <= 1'd1;
			if (tx_crc_sink_valid) begin
				tx_crc_sink_ready <= 1'd0;
				txdatapath_bufferizeendpoints_next_state <= 1'd1;
			end
			tx_crc_is_ongoing0 <= 1'd1;
		end
	endcase
// synthesis translate_off
	dummy_d_10 <= dummy_s;
// synthesis translate_on
end
assign tx_crc_pipe_valid_sink_ready = ((~tx_crc_pipe_valid_source_valid) | tx_crc_pipe_valid_source_ready);
assign tx_crc_pipe_valid_sink_valid = tx_crc_sink_sink_valid;
assign tx_crc_sink_sink_ready = tx_crc_pipe_valid_sink_ready;
assign tx_crc_pipe_valid_sink_first = tx_crc_sink_sink_first;
assign tx_crc_pipe_valid_sink_last = tx_crc_sink_sink_last;
assign tx_crc_pipe_valid_sink_payload_data = tx_crc_sink_sink_payload_data;
assign tx_crc_pipe_valid_sink_payload_last_be = tx_crc_sink_sink_payload_last_be;
assign tx_crc_pipe_valid_sink_payload_error = tx_crc_sink_sink_payload_error;
assign tx_crc_source_source_valid = tx_crc_pipe_valid_source_valid;
assign tx_crc_pipe_valid_source_ready = tx_crc_source_source_ready;
assign tx_crc_source_source_first = tx_crc_pipe_valid_source_first;
assign tx_crc_source_source_last = tx_crc_pipe_valid_source_last;
assign tx_crc_source_source_payload_data = tx_crc_pipe_valid_source_payload_data;
assign tx_crc_source_source_payload_last_be = tx_crc_pipe_valid_source_payload_last_be;
assign tx_crc_source_source_payload_error = tx_crc_pipe_valid_source_payload_error;
assign tx_preamble_source_payload_last_be = tx_preamble_sink_payload_last_be;

// synthesis translate_off
reg dummy_d_11;
// synthesis translate_on
always @(*) begin
	tx_preamble_sink_ready <= 1'd0;
	tx_preamble_source_valid <= 1'd0;
	tx_preamble_source_first <= 1'd0;
	tx_preamble_source_last <= 1'd0;
	tx_preamble_source_payload_data <= 8'd0;
	tx_preamble_source_payload_error <= 1'd0;
	txdatapath_liteethmacpreambleinserter_next_state <= 2'd0;
	tx_preamble_count_clockdomainsrenamer2_next_value <= 3'd0;
	tx_preamble_count_clockdomainsrenamer2_next_value_ce <= 1'd0;
	tx_preamble_source_payload_data <= tx_preamble_sink_payload_data;
	txdatapath_liteethmacpreambleinserter_next_state <= txdatapath_liteethmacpreambleinserter_state;
	case (txdatapath_liteethmacpreambleinserter_state)
		1'd1: begin
			tx_preamble_source_valid <= 1'd1;
			case (tx_preamble_count)
				1'd0: begin
					tx_preamble_source_payload_data <= tx_preamble_preamble[7:0];
				end
				1'd1: begin
					tx_preamble_source_payload_data <= tx_preamble_preamble[15:8];
				end
				2'd2: begin
					tx_preamble_source_payload_data <= tx_preamble_preamble[23:16];
				end
				2'd3: begin
					tx_preamble_source_payload_data <= tx_preamble_preamble[31:24];
				end
				3'd4: begin
					tx_preamble_source_payload_data <= tx_preamble_preamble[39:32];
				end
				3'd5: begin
					tx_preamble_source_payload_data <= tx_preamble_preamble[47:40];
				end
				3'd6: begin
					tx_preamble_source_payload_data <= tx_preamble_preamble[55:48];
				end
				default: begin
					tx_preamble_source_payload_data <= tx_preamble_preamble[63:56];
				end
			endcase
			if (tx_preamble_source_ready) begin
				if ((tx_preamble_count == 3'd7)) begin
					txdatapath_liteethmacpreambleinserter_next_state <= 2'd2;
				end else begin
					tx_preamble_count_clockdomainsrenamer2_next_value <= (tx_preamble_count + 1'd1);
					tx_preamble_count_clockdomainsrenamer2_next_value_ce <= 1'd1;
				end
			end
		end
		2'd2: begin
			tx_preamble_source_valid <= tx_preamble_sink_valid;
			tx_preamble_sink_ready <= tx_preamble_source_ready;
			tx_preamble_source_first <= tx_preamble_sink_first;
			tx_preamble_source_last <= tx_preamble_sink_last;
			tx_preamble_source_payload_error <= tx_preamble_sink_payload_error;
			if (((tx_preamble_sink_valid & tx_preamble_sink_last) & tx_preamble_source_ready)) begin
				txdatapath_liteethmacpreambleinserter_next_state <= 1'd0;
			end
		end
		default: begin
			tx_preamble_sink_ready <= 1'd1;
			tx_preamble_count_clockdomainsrenamer2_next_value <= 1'd0;
			tx_preamble_count_clockdomainsrenamer2_next_value_ce <= 1'd1;
			if (tx_preamble_sink_valid) begin
				tx_preamble_sink_ready <= 1'd0;
				txdatapath_liteethmacpreambleinserter_next_state <= 1'd1;
			end
		end
	endcase
// synthesis translate_off
	dummy_d_11 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_12;
// synthesis translate_on
always @(*) begin
	tx_gap_sink_ready <= 1'd0;
	tx_gap_source_valid <= 1'd0;
	tx_gap_source_first <= 1'd0;
	tx_gap_source_last <= 1'd0;
	tx_gap_source_payload_data <= 8'd0;
	tx_gap_source_payload_last_be <= 1'd0;
	tx_gap_source_payload_error <= 1'd0;
	txdatapath_liteethmacgap_next_state <= 1'd0;
	tx_gap_counter_clockdomainsrenamer3_next_value <= 4'd0;
	tx_gap_counter_clockdomainsrenamer3_next_value_ce <= 1'd0;
	txdatapath_liteethmacgap_next_state <= txdatapath_liteethmacgap_state;
	case (txdatapath_liteethmacgap_state)
		1'd1: begin
			tx_gap_counter_clockdomainsrenamer3_next_value <= (tx_gap_counter - 1'd1);
			tx_gap_counter_clockdomainsrenamer3_next_value_ce <= 1'd1;
			if ((tx_gap_counter == 1'd1)) begin
				txdatapath_liteethmacgap_next_state <= 1'd0;
			end
		end
		default: begin
			tx_gap_source_valid <= tx_gap_sink_valid;
			tx_gap_sink_ready <= tx_gap_source_ready;
			tx_gap_source_first <= tx_gap_sink_first;
			tx_gap_source_last <= tx_gap_sink_last;
			tx_gap_source_payload_data <= tx_gap_sink_payload_data;
			tx_gap_source_payload_last_be <= tx_gap_sink_payload_last_be;
			tx_gap_source_payload_error <= tx_gap_sink_payload_error;
			if (((tx_gap_sink_valid & tx_gap_sink_last) & tx_gap_sink_ready)) begin
				tx_gap_counter_clockdomainsrenamer3_next_value <= 4'd12;
				tx_gap_counter_clockdomainsrenamer3_next_value_ce <= 1'd1;
				txdatapath_liteethmacgap_next_state <= 1'd1;
			end
		end
	endcase
// synthesis translate_off
	dummy_d_12 <= dummy_s;
// synthesis translate_on
end
assign tx_cdc_sink_sink_valid = sink_valid;
assign sink_ready = tx_cdc_sink_sink_ready;
assign tx_cdc_sink_sink_first = sink_first;
assign tx_cdc_sink_sink_last = sink_last;
assign tx_cdc_sink_sink_payload_data = sink_payload_data;
assign tx_cdc_sink_sink_payload_last_be = sink_payload_last_be;
assign tx_cdc_sink_sink_payload_error = sink_payload_error;
assign tx_converter_sink_valid = tx_cdc_source_source_valid;
assign tx_cdc_source_source_ready = tx_converter_sink_ready;
assign tx_converter_sink_first = tx_cdc_source_source_first;
assign tx_converter_sink_last = tx_cdc_source_source_last;
assign tx_converter_sink_payload_data = tx_cdc_source_source_payload_data;
assign tx_converter_sink_payload_last_be = tx_cdc_source_source_payload_last_be;
assign tx_converter_sink_payload_error = tx_cdc_source_source_payload_error;
assign tx_last_be_sink_sink_valid = tx_converter_source_valid;
assign tx_converter_source_ready = tx_last_be_sink_sink_ready;
assign tx_last_be_sink_sink_first = tx_converter_source_first;
assign tx_last_be_sink_sink_last = tx_converter_source_last;
assign tx_last_be_sink_sink_payload_data = tx_converter_source_payload_data;
assign tx_last_be_sink_sink_payload_last_be = tx_converter_source_payload_last_be;
assign tx_last_be_sink_sink_payload_error = tx_converter_source_payload_error;
assign tx_padding_sink_valid = tx_last_be_source_source_valid;
assign tx_last_be_source_source_ready = tx_padding_sink_ready;
assign tx_padding_sink_first = tx_last_be_source_source_first;
assign tx_padding_sink_last = tx_last_be_source_source_last;
assign tx_padding_sink_payload_data = tx_last_be_source_source_payload_data;
assign tx_padding_sink_payload_last_be = tx_last_be_source_source_payload_last_be;
assign tx_padding_sink_payload_error = tx_last_be_source_source_payload_error;
assign tx_crc_sink_sink_valid = tx_padding_source_valid;
assign tx_padding_source_ready = tx_crc_sink_sink_ready;
assign tx_crc_sink_sink_first = tx_padding_source_first;
assign tx_crc_sink_sink_last = tx_padding_source_last;
assign tx_crc_sink_sink_payload_data = tx_padding_source_payload_data;
assign tx_crc_sink_sink_payload_last_be = tx_padding_source_payload_last_be;
assign tx_crc_sink_sink_payload_error = tx_padding_source_payload_error;
assign tx_preamble_sink_valid = tx_crc_source_valid;
assign tx_crc_source_ready = tx_preamble_sink_ready;
assign tx_preamble_sink_first = tx_crc_source_first;
assign tx_preamble_sink_last = tx_crc_source_last;
assign tx_preamble_sink_payload_data = tx_crc_source_payload_data;
assign tx_preamble_sink_payload_last_be = tx_crc_source_payload_last_be;
assign tx_preamble_sink_payload_error = tx_crc_source_payload_error;
assign tx_gap_sink_valid = tx_preamble_source_valid;
assign tx_preamble_source_ready = tx_gap_sink_ready;
assign tx_gap_sink_first = tx_preamble_source_first;
assign tx_gap_sink_last = tx_preamble_source_last;
assign tx_gap_sink_payload_data = tx_preamble_source_payload_data;
assign tx_gap_sink_payload_last_be = tx_preamble_source_payload_last_be;
assign tx_gap_sink_payload_error = tx_preamble_source_payload_error;
assign liteethphymiitx_sink_valid = tx_gap_source_valid;
assign tx_gap_source_ready = liteethphymiitx_sink_ready;
assign liteethphymiitx_sink_first = tx_gap_source_first;
assign liteethphymiitx_sink_last = tx_gap_source_last;
assign liteethphymiitx_sink_payload_data = tx_gap_source_payload_data;
assign liteethphymiitx_sink_payload_last_be = tx_gap_source_payload_last_be;
assign liteethphymiitx_sink_payload_error = tx_gap_source_payload_error;
assign pulsesynchronizer0_i = rx_preamble_error;
assign pulsesynchronizer1_i = liteethmaccrc32checker_error;
assign rx_preamble_source_payload_data = rx_preamble_sink_payload_data;
assign rx_preamble_source_payload_last_be = rx_preamble_sink_payload_last_be;

// synthesis translate_off
reg dummy_d_13;
// synthesis translate_on
always @(*) begin
	rx_preamble_sink_ready <= 1'd0;
	rx_preamble_source_valid <= 1'd0;
	rx_preamble_source_first <= 1'd0;
	rx_preamble_source_last <= 1'd0;
	rx_preamble_source_payload_error <= 1'd0;
	rx_preamble_error <= 1'd0;
	rxdatapath_liteethmacpreamblechecker_next_state <= 1'd0;
	rxdatapath_liteethmacpreamblechecker_next_state <= rxdatapath_liteethmacpreamblechecker_state;
	case (rxdatapath_liteethmacpreamblechecker_state)
		1'd1: begin
			rx_preamble_source_valid <= rx_preamble_sink_valid;
			rx_preamble_sink_ready <= rx_preamble_source_ready;
			rx_preamble_source_first <= rx_preamble_sink_first;
			rx_preamble_source_last <= rx_preamble_sink_last;
			rx_preamble_source_payload_error <= rx_preamble_sink_payload_error;
			if (((rx_preamble_source_valid & rx_preamble_source_last) & rx_preamble_source_ready)) begin
				rxdatapath_liteethmacpreamblechecker_next_state <= 1'd0;
			end
		end
		default: begin
			rx_preamble_sink_ready <= 1'd1;
			if (((rx_preamble_sink_valid & (~rx_preamble_sink_last)) & (rx_preamble_sink_payload_data == rx_preamble_preamble[63:56]))) begin
				rxdatapath_liteethmacpreamblechecker_next_state <= 1'd1;
			end
			if ((rx_preamble_sink_valid & rx_preamble_sink_last)) begin
				rx_preamble_error <= 1'd1;
			end
		end
	endcase
// synthesis translate_off
	dummy_d_13 <= dummy_s;
// synthesis translate_on
end
assign pulsesynchronizer0_o = (pulsesynchronizer0_toggle_o ^ pulsesynchronizer0_toggle_o_r);
assign liteethmaccrc32checker_fifo_full = (liteethmaccrc32checker_syncfifo_level == 3'd4);
assign liteethmaccrc32checker_fifo_in = (liteethmaccrc32checker_sink_sink_valid & ((~liteethmaccrc32checker_fifo_full) | liteethmaccrc32checker_fifo_out));
assign liteethmaccrc32checker_fifo_out = (liteethmaccrc32checker_source_source_valid & liteethmaccrc32checker_source_source_ready);
assign liteethmaccrc32checker_syncfifo_sink_first = liteethmaccrc32checker_sink_sink_first;
assign liteethmaccrc32checker_syncfifo_sink_last = liteethmaccrc32checker_sink_sink_last;
assign liteethmaccrc32checker_syncfifo_sink_payload_data = liteethmaccrc32checker_sink_sink_payload_data;
assign liteethmaccrc32checker_syncfifo_sink_payload_last_be = liteethmaccrc32checker_sink_sink_payload_last_be;
assign liteethmaccrc32checker_syncfifo_sink_payload_error = liteethmaccrc32checker_sink_sink_payload_error;

// synthesis translate_off
reg dummy_d_14;
// synthesis translate_on
always @(*) begin
	liteethmaccrc32checker_syncfifo_sink_valid <= 1'd0;
	liteethmaccrc32checker_syncfifo_sink_valid <= liteethmaccrc32checker_sink_sink_valid;
	liteethmaccrc32checker_syncfifo_sink_valid <= liteethmaccrc32checker_fifo_in;
// synthesis translate_off
	dummy_d_14 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_15;
// synthesis translate_on
always @(*) begin
	liteethmaccrc32checker_sink_sink_ready <= 1'd0;
	liteethmaccrc32checker_sink_sink_ready <= liteethmaccrc32checker_syncfifo_sink_ready;
	liteethmaccrc32checker_sink_sink_ready <= liteethmaccrc32checker_fifo_in;
// synthesis translate_off
	dummy_d_15 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccrc32checker_crc_data0 = liteethmaccrc32checker_sink_sink_payload_data;
assign liteethmaccrc32checker_crc_be = liteethmaccrc32checker_sink_sink_payload_last_be;
assign liteethmaccrc32checker_source_source_first = liteethmaccrc32checker_syncfifo_source_first;
assign liteethmaccrc32checker_source_source_payload_data = liteethmaccrc32checker_syncfifo_source_payload_data;
assign liteethmaccrc32checker_sink_sink_valid = bufferizeendpoints_source_source_valid;
assign bufferizeendpoints_source_source_ready = liteethmaccrc32checker_sink_sink_ready;
assign liteethmaccrc32checker_sink_sink_first = bufferizeendpoints_source_source_first;
assign liteethmaccrc32checker_sink_sink_last = bufferizeendpoints_source_source_last;
assign liteethmaccrc32checker_sink_sink_payload_data = bufferizeendpoints_source_source_payload_data;
assign liteethmaccrc32checker_sink_sink_payload_last_be = bufferizeendpoints_source_source_payload_last_be;
assign liteethmaccrc32checker_sink_sink_payload_error = bufferizeendpoints_source_source_payload_error;
assign liteethmaccrc32checker_crc_crc_prev = liteethmaccrc32checker_crc_reg;

// synthesis translate_off
reg dummy_d_16;
// synthesis translate_on
always @(*) begin
	liteethmaccrc32checker_crc_error0 <= 1'd0;
	liteethmaccrc32checker_crc_data1 <= 8'd0;
	liteethmaccrc32checker_crc_data1 <= liteethmaccrc32checker_crc_data0;
	if (liteethmaccrc32checker_crc_be) begin
		liteethmaccrc32checker_crc_data1 <= (liteethmaccrc32checker_crc_data0 & 8'd255);
		liteethmaccrc32checker_crc_error0 <= (liteethmaccrc32checker_crc_crc_next != 32'd3338984827);
	end
// synthesis translate_off
	dummy_d_16 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_17;
// synthesis translate_on
always @(*) begin
	liteethmaccrc32checker_crc_crc_next <= 32'd0;
	liteethmaccrc32checker_crc_crc_next[0] <= (((liteethmaccrc32checker_crc_crc_prev[24] ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[1] <= (((((((liteethmaccrc32checker_crc_crc_prev[25] ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[2] <= (((((((((liteethmaccrc32checker_crc_crc_prev[26] ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[3] <= (((((((liteethmaccrc32checker_crc_crc_prev[27] ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_data1[6]);
	liteethmaccrc32checker_crc_crc_next[4] <= (((((((((liteethmaccrc32checker_crc_crc_prev[28] ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[5] <= (((((((((((((liteethmaccrc32checker_crc_crc_prev[29] ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[6] <= (((((((((((liteethmaccrc32checker_crc_crc_prev[30] ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_data1[6]);
	liteethmaccrc32checker_crc_crc_next[7] <= (((((((((liteethmaccrc32checker_crc_crc_prev[31] ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[8] <= ((((((((liteethmaccrc32checker_crc_crc_prev[0] ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[9] <= ((((((((liteethmaccrc32checker_crc_crc_prev[1] ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_data1[6]);
	liteethmaccrc32checker_crc_crc_next[10] <= ((((((((liteethmaccrc32checker_crc_crc_prev[2] ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[11] <= ((((((((liteethmaccrc32checker_crc_crc_prev[3] ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[12] <= ((((((((((((liteethmaccrc32checker_crc_crc_prev[4] ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[13] <= ((((((((((((liteethmaccrc32checker_crc_crc_prev[5] ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_data1[6]);
	liteethmaccrc32checker_crc_crc_next[14] <= ((((((((((liteethmaccrc32checker_crc_crc_prev[6] ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]);
	liteethmaccrc32checker_crc_crc_next[15] <= ((((((((liteethmaccrc32checker_crc_crc_prev[7] ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]);
	liteethmaccrc32checker_crc_crc_next[16] <= ((((((liteethmaccrc32checker_crc_crc_prev[8] ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[17] <= ((((((liteethmaccrc32checker_crc_crc_prev[9] ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_data1[6]);
	liteethmaccrc32checker_crc_crc_next[18] <= ((((((liteethmaccrc32checker_crc_crc_prev[10] ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]);
	liteethmaccrc32checker_crc_crc_next[19] <= ((((liteethmaccrc32checker_crc_crc_prev[11] ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]);
	liteethmaccrc32checker_crc_crc_next[20] <= ((liteethmaccrc32checker_crc_crc_prev[12] ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]);
	liteethmaccrc32checker_crc_crc_next[21] <= ((liteethmaccrc32checker_crc_crc_prev[13] ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]);
	liteethmaccrc32checker_crc_crc_next[22] <= ((liteethmaccrc32checker_crc_crc_prev[14] ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[23] <= ((((((liteethmaccrc32checker_crc_crc_prev[15] ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_data1[6]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[24] <= ((((((liteethmaccrc32checker_crc_crc_prev[16] ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_data1[6]);
	liteethmaccrc32checker_crc_crc_next[25] <= ((((liteethmaccrc32checker_crc_crc_prev[17] ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]);
	liteethmaccrc32checker_crc_crc_next[26] <= ((((((((liteethmaccrc32checker_crc_crc_prev[18] ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]) ^ liteethmaccrc32checker_crc_crc_prev[24]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_data1[7]);
	liteethmaccrc32checker_crc_crc_next[27] <= ((((((((liteethmaccrc32checker_crc_crc_prev[19] ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]) ^ liteethmaccrc32checker_crc_crc_prev[25]) ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_data1[6]);
	liteethmaccrc32checker_crc_crc_next[28] <= ((((((liteethmaccrc32checker_crc_crc_prev[20] ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]) ^ liteethmaccrc32checker_crc_crc_prev[26]) ^ liteethmaccrc32checker_crc_data1[5]);
	liteethmaccrc32checker_crc_crc_next[29] <= ((((((liteethmaccrc32checker_crc_crc_prev[21] ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_crc_prev[30]) ^ liteethmaccrc32checker_crc_data1[1]) ^ liteethmaccrc32checker_crc_crc_prev[27]) ^ liteethmaccrc32checker_crc_data1[4]);
	liteethmaccrc32checker_crc_crc_next[30] <= ((((liteethmaccrc32checker_crc_crc_prev[22] ^ liteethmaccrc32checker_crc_crc_prev[31]) ^ liteethmaccrc32checker_crc_data1[0]) ^ liteethmaccrc32checker_crc_crc_prev[28]) ^ liteethmaccrc32checker_crc_data1[3]);
	liteethmaccrc32checker_crc_crc_next[31] <= ((liteethmaccrc32checker_crc_crc_prev[23] ^ liteethmaccrc32checker_crc_crc_prev[29]) ^ liteethmaccrc32checker_crc_data1[2]);
// synthesis translate_off
	dummy_d_17 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccrc32checker_syncfifo_syncfifo_din = {liteethmaccrc32checker_syncfifo_fifo_in_last, liteethmaccrc32checker_syncfifo_fifo_in_first, liteethmaccrc32checker_syncfifo_fifo_in_payload_error, liteethmaccrc32checker_syncfifo_fifo_in_payload_last_be, liteethmaccrc32checker_syncfifo_fifo_in_payload_data};
assign {liteethmaccrc32checker_syncfifo_fifo_out_last, liteethmaccrc32checker_syncfifo_fifo_out_first, liteethmaccrc32checker_syncfifo_fifo_out_payload_error, liteethmaccrc32checker_syncfifo_fifo_out_payload_last_be, liteethmaccrc32checker_syncfifo_fifo_out_payload_data} = liteethmaccrc32checker_syncfifo_syncfifo_dout;
assign liteethmaccrc32checker_syncfifo_sink_ready = liteethmaccrc32checker_syncfifo_syncfifo_writable;
assign liteethmaccrc32checker_syncfifo_syncfifo_we = liteethmaccrc32checker_syncfifo_sink_valid;
assign liteethmaccrc32checker_syncfifo_fifo_in_first = liteethmaccrc32checker_syncfifo_sink_first;
assign liteethmaccrc32checker_syncfifo_fifo_in_last = liteethmaccrc32checker_syncfifo_sink_last;
assign liteethmaccrc32checker_syncfifo_fifo_in_payload_data = liteethmaccrc32checker_syncfifo_sink_payload_data;
assign liteethmaccrc32checker_syncfifo_fifo_in_payload_last_be = liteethmaccrc32checker_syncfifo_sink_payload_last_be;
assign liteethmaccrc32checker_syncfifo_fifo_in_payload_error = liteethmaccrc32checker_syncfifo_sink_payload_error;
assign liteethmaccrc32checker_syncfifo_source_valid = liteethmaccrc32checker_syncfifo_syncfifo_readable;
assign liteethmaccrc32checker_syncfifo_source_first = liteethmaccrc32checker_syncfifo_fifo_out_first;
assign liteethmaccrc32checker_syncfifo_source_last = liteethmaccrc32checker_syncfifo_fifo_out_last;
assign liteethmaccrc32checker_syncfifo_source_payload_data = liteethmaccrc32checker_syncfifo_fifo_out_payload_data;
assign liteethmaccrc32checker_syncfifo_source_payload_last_be = liteethmaccrc32checker_syncfifo_fifo_out_payload_last_be;
assign liteethmaccrc32checker_syncfifo_source_payload_error = liteethmaccrc32checker_syncfifo_fifo_out_payload_error;
assign liteethmaccrc32checker_syncfifo_syncfifo_re = liteethmaccrc32checker_syncfifo_source_ready;

// synthesis translate_off
reg dummy_d_18;
// synthesis translate_on
always @(*) begin
	liteethmaccrc32checker_syncfifo_wrport_adr <= 3'd0;
	if (liteethmaccrc32checker_syncfifo_replace) begin
		liteethmaccrc32checker_syncfifo_wrport_adr <= (liteethmaccrc32checker_syncfifo_produce - 1'd1);
	end else begin
		liteethmaccrc32checker_syncfifo_wrport_adr <= liteethmaccrc32checker_syncfifo_produce;
	end
// synthesis translate_off
	dummy_d_18 <= dummy_s;
// synthesis translate_on
end
assign liteethmaccrc32checker_syncfifo_wrport_dat_w = liteethmaccrc32checker_syncfifo_syncfifo_din;
assign liteethmaccrc32checker_syncfifo_wrport_we = (liteethmaccrc32checker_syncfifo_syncfifo_we & (liteethmaccrc32checker_syncfifo_syncfifo_writable | liteethmaccrc32checker_syncfifo_replace));
assign liteethmaccrc32checker_syncfifo_do_read = (liteethmaccrc32checker_syncfifo_syncfifo_readable & liteethmaccrc32checker_syncfifo_syncfifo_re);
assign liteethmaccrc32checker_syncfifo_rdport_adr = liteethmaccrc32checker_syncfifo_consume;
assign liteethmaccrc32checker_syncfifo_syncfifo_dout = liteethmaccrc32checker_syncfifo_rdport_dat_r;
assign liteethmaccrc32checker_syncfifo_syncfifo_writable = (liteethmaccrc32checker_syncfifo_level != 3'd5);
assign liteethmaccrc32checker_syncfifo_syncfifo_readable = (liteethmaccrc32checker_syncfifo_level != 1'd0);

// synthesis translate_off
reg dummy_d_19;
// synthesis translate_on
always @(*) begin
	liteethmaccrc32checker_source_source_valid <= 1'd0;
	liteethmaccrc32checker_source_source_last <= 1'd0;
	liteethmaccrc32checker_source_source_payload_last_be <= 1'd0;
	liteethmaccrc32checker_source_source_payload_error <= 1'd0;
	liteethmaccrc32checker_error <= 1'd0;
	liteethmaccrc32checker_crc_ce <= 1'd0;
	liteethmaccrc32checker_crc_reset <= 1'd0;
	liteethmaccrc32checker_syncfifo_source_ready <= 1'd0;
	liteethmaccrc32checker_fifo_reset <= 1'd0;
	rxdatapath_bufferizeendpoints_next_state <= 2'd0;
	liteethmaccrc32checker_last_be_next_value0 <= 1'd0;
	liteethmaccrc32checker_last_be_next_value_ce0 <= 1'd0;
	liteethmaccrc32checker_crc_error1_next_value1 <= 1'd0;
	liteethmaccrc32checker_crc_error1_next_value_ce1 <= 1'd0;
	liteethmaccrc32checker_source_source_payload_error <= liteethmaccrc32checker_syncfifo_source_payload_error;
	rxdatapath_bufferizeendpoints_next_state <= rxdatapath_bufferizeendpoints_state;
	case (rxdatapath_bufferizeendpoints_state)
		1'd1: begin
			if ((liteethmaccrc32checker_sink_sink_valid & liteethmaccrc32checker_sink_sink_ready)) begin
				liteethmaccrc32checker_crc_ce <= 1'd1;
				rxdatapath_bufferizeendpoints_next_state <= 2'd2;
			end
		end
		2'd2: begin
			liteethmaccrc32checker_syncfifo_source_ready <= liteethmaccrc32checker_fifo_out;
			liteethmaccrc32checker_source_source_valid <= (liteethmaccrc32checker_sink_sink_valid & liteethmaccrc32checker_fifo_full);
			if (1'd1) begin
				liteethmaccrc32checker_source_source_last <= liteethmaccrc32checker_sink_sink_last;
				liteethmaccrc32checker_source_source_payload_last_be <= liteethmaccrc32checker_sink_sink_payload_last_be;
			end else begin
				if ((liteethmaccrc32checker_sink_sink_payload_last_be & 4'd15)) begin
					liteethmaccrc32checker_source_source_last <= liteethmaccrc32checker_sink_sink_last;
					liteethmaccrc32checker_source_source_payload_last_be <= (liteethmaccrc32checker_sink_sink_payload_last_be <<< 3'sd5);
				end else begin
					liteethmaccrc32checker_last_be_next_value0 <= (liteethmaccrc32checker_sink_sink_payload_last_be >>> 3'd4);
					liteethmaccrc32checker_last_be_next_value_ce0 <= 1'd1;
					liteethmaccrc32checker_crc_error1_next_value1 <= liteethmaccrc32checker_crc_error0;
					liteethmaccrc32checker_crc_error1_next_value_ce1 <= 1'd1;
				end
			end
			liteethmaccrc32checker_source_source_payload_error <= (liteethmaccrc32checker_sink_sink_payload_error | {1{(liteethmaccrc32checker_crc_error0 & liteethmaccrc32checker_sink_sink_last)}});
			liteethmaccrc32checker_error <= ((liteethmaccrc32checker_sink_sink_valid & liteethmaccrc32checker_sink_sink_last) & liteethmaccrc32checker_crc_error0);
			if ((liteethmaccrc32checker_sink_sink_valid & liteethmaccrc32checker_sink_sink_ready)) begin
				liteethmaccrc32checker_crc_ce <= 1'd1;
				if ((liteethmaccrc32checker_sink_sink_last & (liteethmaccrc32checker_sink_sink_payload_last_be > 4'd15))) begin
					rxdatapath_bufferizeendpoints_next_state <= 2'd3;
				end else begin
					if (liteethmaccrc32checker_sink_sink_last) begin
						rxdatapath_bufferizeendpoints_next_state <= 1'd0;
					end
				end
			end
		end
		2'd3: begin
			liteethmaccrc32checker_source_source_valid <= liteethmaccrc32checker_syncfifo_source_valid;
			liteethmaccrc32checker_syncfifo_source_ready <= liteethmaccrc32checker_source_source_ready;
			liteethmaccrc32checker_source_source_last <= liteethmaccrc32checker_syncfifo_source_last;
			liteethmaccrc32checker_source_source_payload_error <= (liteethmaccrc32checker_syncfifo_source_payload_error | {1{liteethmaccrc32checker_crc_error1}});
			liteethmaccrc32checker_source_source_payload_last_be <= liteethmaccrc32checker_last_be;
			if ((liteethmaccrc32checker_source_source_valid & liteethmaccrc32checker_source_source_ready)) begin
				rxdatapath_bufferizeendpoints_next_state <= 1'd0;
			end
		end
		default: begin
			liteethmaccrc32checker_crc_reset <= 1'd1;
			liteethmaccrc32checker_fifo_reset <= 1'd1;
			rxdatapath_bufferizeendpoints_next_state <= 1'd1;
		end
	endcase
// synthesis translate_off
	dummy_d_19 <= dummy_s;
// synthesis translate_on
end
assign bufferizeendpoints_pipe_valid_sink_ready = ((~bufferizeendpoints_pipe_valid_source_valid) | bufferizeendpoints_pipe_valid_source_ready);
assign bufferizeendpoints_pipe_valid_sink_valid = bufferizeendpoints_sink_sink_valid;
assign bufferizeendpoints_sink_sink_ready = bufferizeendpoints_pipe_valid_sink_ready;
assign bufferizeendpoints_pipe_valid_sink_first = bufferizeendpoints_sink_sink_first;
assign bufferizeendpoints_pipe_valid_sink_last = bufferizeendpoints_sink_sink_last;
assign bufferizeendpoints_pipe_valid_sink_payload_data = bufferizeendpoints_sink_sink_payload_data;
assign bufferizeendpoints_pipe_valid_sink_payload_last_be = bufferizeendpoints_sink_sink_payload_last_be;
assign bufferizeendpoints_pipe_valid_sink_payload_error = bufferizeendpoints_sink_sink_payload_error;
assign bufferizeendpoints_source_source_valid = bufferizeendpoints_pipe_valid_source_valid;
assign bufferizeendpoints_pipe_valid_source_ready = bufferizeendpoints_source_source_ready;
assign bufferizeendpoints_source_source_first = bufferizeendpoints_pipe_valid_source_first;
assign bufferizeendpoints_source_source_last = bufferizeendpoints_pipe_valid_source_last;
assign bufferizeendpoints_source_source_payload_data = bufferizeendpoints_pipe_valid_source_payload_data;
assign bufferizeendpoints_source_source_payload_last_be = bufferizeendpoints_pipe_valid_source_payload_last_be;
assign bufferizeendpoints_source_source_payload_error = bufferizeendpoints_pipe_valid_source_payload_error;
assign pulsesynchronizer1_o = (pulsesynchronizer1_toggle_o ^ pulsesynchronizer1_toggle_o_r);

// synthesis translate_off
reg dummy_d_20;
// synthesis translate_on
always @(*) begin
	rx_padding_length_inc <= 4'd0;
	case (rx_padding_sink_payload_last_be)
		1'd1: begin
			rx_padding_length_inc <= 1'd1;
		end
		2'd2: begin
			rx_padding_length_inc <= 2'd2;
		end
		3'd4: begin
			rx_padding_length_inc <= 2'd3;
		end
		4'd8: begin
			rx_padding_length_inc <= 3'd4;
		end
		5'd16: begin
			rx_padding_length_inc <= 3'd5;
		end
		6'd32: begin
			rx_padding_length_inc <= 3'd6;
		end
		7'd64: begin
			rx_padding_length_inc <= 3'd7;
		end
		default: begin
			rx_padding_length_inc <= 1'd1;
		end
	endcase
// synthesis translate_off
	dummy_d_20 <= dummy_s;
// synthesis translate_on
end
assign rx_padding_source_valid = rx_padding_sink_valid;
assign rx_padding_sink_ready = rx_padding_source_ready;
assign rx_padding_source_first = rx_padding_sink_first;
assign rx_padding_source_last = rx_padding_sink_last;
assign rx_padding_source_payload_data = rx_padding_sink_payload_data;
assign rx_padding_source_payload_last_be = rx_padding_sink_payload_last_be;

// synthesis translate_off
reg dummy_d_21;
// synthesis translate_on
always @(*) begin
	rx_padding_source_payload_error <= 1'd0;
	if (((rx_padding_sink_valid & rx_padding_sink_last) & ((rx_padding_length + rx_padding_length_inc) < 6'd60))) begin
		rx_padding_source_payload_error <= {1{1'd1}};
	end else begin
		rx_padding_source_payload_error <= rx_padding_sink_payload_error;
	end
// synthesis translate_off
	dummy_d_21 <= dummy_s;
// synthesis translate_on
end
assign rx_last_be_source_valid = rx_last_be_sink_valid;
assign rx_last_be_sink_ready = rx_last_be_source_ready;
assign rx_last_be_source_first = rx_last_be_sink_first;
assign rx_last_be_source_last = rx_last_be_sink_last;
assign rx_last_be_source_payload_data = rx_last_be_sink_payload_data;
assign rx_last_be_source_payload_error = rx_last_be_sink_payload_error;

// synthesis translate_off
reg dummy_d_22;
// synthesis translate_on
always @(*) begin
	rx_last_be_source_payload_last_be <= 1'd0;
	rx_last_be_source_payload_last_be <= rx_last_be_sink_payload_last_be;
	if (1'd1) begin
		rx_last_be_source_payload_last_be <= rx_last_be_sink_last;
	end
// synthesis translate_off
	dummy_d_22 <= dummy_s;
// synthesis translate_on
end
assign rx_converter_converter_sink_valid = rx_converter_sink_valid;
assign rx_converter_converter_sink_first = rx_converter_sink_first;
assign rx_converter_converter_sink_last = rx_converter_sink_last;
assign rx_converter_sink_ready = rx_converter_converter_sink_ready;
assign rx_converter_converter_sink_payload_data = {rx_converter_sink_payload_error, rx_converter_sink_payload_last_be, rx_converter_sink_payload_data};
assign rx_converter_source_valid = rx_converter_source_source_valid;
assign rx_converter_source_first = rx_converter_source_source_first;
assign rx_converter_source_last = rx_converter_source_source_last;
assign rx_converter_source_source_ready = rx_converter_source_ready;

// synthesis translate_off
reg dummy_d_23;
// synthesis translate_on
always @(*) begin
	rx_converter_source_payload_data <= 64'd0;
	rx_converter_source_payload_data[7:0] <= rx_converter_source_source_payload_data[7:0];
	rx_converter_source_payload_data[15:8] <= rx_converter_source_source_payload_data[17:10];
	rx_converter_source_payload_data[23:16] <= rx_converter_source_source_payload_data[27:20];
	rx_converter_source_payload_data[31:24] <= rx_converter_source_source_payload_data[37:30];
	rx_converter_source_payload_data[39:32] <= rx_converter_source_source_payload_data[47:40];
	rx_converter_source_payload_data[47:40] <= rx_converter_source_source_payload_data[57:50];
	rx_converter_source_payload_data[55:48] <= rx_converter_source_source_payload_data[67:60];
	rx_converter_source_payload_data[63:56] <= rx_converter_source_source_payload_data[77:70];
// synthesis translate_off
	dummy_d_23 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_24;
// synthesis translate_on
always @(*) begin
	rx_converter_source_payload_last_be <= 8'd0;
	rx_converter_source_payload_last_be[0] <= rx_converter_source_source_payload_data[8];
	rx_converter_source_payload_last_be[1] <= rx_converter_source_source_payload_data[18];
	rx_converter_source_payload_last_be[2] <= rx_converter_source_source_payload_data[28];
	rx_converter_source_payload_last_be[3] <= rx_converter_source_source_payload_data[38];
	rx_converter_source_payload_last_be[4] <= rx_converter_source_source_payload_data[48];
	rx_converter_source_payload_last_be[5] <= rx_converter_source_source_payload_data[58];
	rx_converter_source_payload_last_be[6] <= rx_converter_source_source_payload_data[68];
	rx_converter_source_payload_last_be[7] <= rx_converter_source_source_payload_data[78];
// synthesis translate_off
	dummy_d_24 <= dummy_s;
// synthesis translate_on
end

// synthesis translate_off
reg dummy_d_25;
// synthesis translate_on
always @(*) begin
	rx_converter_source_payload_error <= 8'd0;
	rx_converter_source_payload_error[0] <= rx_converter_source_source_payload_data[9];
	rx_converter_source_payload_error[1] <= rx_converter_source_source_payload_data[19];
	rx_converter_source_payload_error[2] <= rx_converter_source_source_payload_data[29];
	rx_converter_source_payload_error[3] <= rx_converter_source_source_payload_data[39];
	rx_converter_source_payload_error[4] <= rx_converter_source_source_payload_data[49];
	rx_converter_source_payload_error[5] <= rx_converter_source_source_payload_data[59];
	rx_converter_source_payload_error[6] <= rx_converter_source_source_payload_data[69];
	rx_converter_source_payload_error[7] <= rx_converter_source_source_payload_data[79];
// synthesis translate_off
	dummy_d_25 <= dummy_s;
// synthesis translate_on
end
assign rx_converter_source_source_valid = rx_converter_converter_source_valid;
assign rx_converter_converter_source_ready = rx_converter_source_source_ready;
assign rx_converter_source_source_first = rx_converter_converter_source_first;
assign rx_converter_source_source_last = rx_converter_converter_source_last;
assign rx_converter_source_source_payload_data = rx_converter_converter_source_payload_data;
assign rx_converter_converter_sink_ready = ((~rx_converter_converter_strobe_all) | rx_converter_converter_source_ready);
assign rx_converter_converter_source_valid = rx_converter_converter_strobe_all;
assign rx_converter_converter_load_part = (rx_converter_converter_sink_valid & rx_converter_converter_sink_ready);
assign rx_cdc_cdc_sink_valid = rx_cdc_sink_sink_valid;
assign rx_cdc_sink_sink_ready = rx_cdc_cdc_sink_ready;
assign rx_cdc_cdc_sink_first = rx_cdc_sink_sink_first;
assign rx_cdc_cdc_sink_last = rx_cdc_sink_sink_last;
assign rx_cdc_cdc_sink_payload_data = rx_cdc_sink_sink_payload_data;
assign rx_cdc_cdc_sink_payload_last_be = rx_cdc_sink_sink_payload_last_be;
assign rx_cdc_cdc_sink_payload_error = rx_cdc_sink_sink_payload_error;
assign rx_cdc_source_source_valid = rx_cdc_cdc_source_valid;
assign rx_cdc_cdc_source_ready = rx_cdc_source_source_ready;
assign rx_cdc_source_source_first = rx_cdc_cdc_source_first;
assign rx_cdc_source_source_last = rx_cdc_cdc_source_last;
assign rx_cdc_source_source_payload_data = rx_cdc_cdc_source_payload_data;
assign rx_cdc_source_source_payload_last_be = rx_cdc_cdc_source_payload_last_be;
assign rx_cdc_source_source_payload_error = rx_cdc_cdc_source_payload_error;
assign rx_cdc_cdc_asyncfifo_din = {rx_cdc_cdc_fifo_in_last, rx_cdc_cdc_fifo_in_first, rx_cdc_cdc_fifo_in_payload_error, rx_cdc_cdc_fifo_in_payload_last_be, rx_cdc_cdc_fifo_in_payload_data};
assign {rx_cdc_cdc_fifo_out_last, rx_cdc_cdc_fifo_out_first, rx_cdc_cdc_fifo_out_payload_error, rx_cdc_cdc_fifo_out_payload_last_be, rx_cdc_cdc_fifo_out_payload_data} = rx_cdc_cdc_asyncfifo_dout;
assign rx_cdc_cdc_sink_ready = rx_cdc_cdc_asyncfifo_writable;
assign rx_cdc_cdc_asyncfifo_we = rx_cdc_cdc_sink_valid;
assign rx_cdc_cdc_fifo_in_first = rx_cdc_cdc_sink_first;
assign rx_cdc_cdc_fifo_in_last = rx_cdc_cdc_sink_last;
assign rx_cdc_cdc_fifo_in_payload_data = rx_cdc_cdc_sink_payload_data;
assign rx_cdc_cdc_fifo_in_payload_last_be = rx_cdc_cdc_sink_payload_last_be;
assign rx_cdc_cdc_fifo_in_payload_error = rx_cdc_cdc_sink_payload_error;
assign rx_cdc_cdc_source_valid = rx_cdc_cdc_asyncfifo_readable;
assign rx_cdc_cdc_source_first = rx_cdc_cdc_fifo_out_first;
assign rx_cdc_cdc_source_last = rx_cdc_cdc_fifo_out_last;
assign rx_cdc_cdc_source_payload_data = rx_cdc_cdc_fifo_out_payload_data;
assign rx_cdc_cdc_source_payload_last_be = rx_cdc_cdc_fifo_out_payload_last_be;
assign rx_cdc_cdc_source_payload_error = rx_cdc_cdc_fifo_out_payload_error;
assign rx_cdc_cdc_asyncfifo_re = rx_cdc_cdc_source_ready;
assign rx_cdc_cdc_graycounter0_ce = (rx_cdc_cdc_asyncfifo_writable & rx_cdc_cdc_asyncfifo_we);
assign rx_cdc_cdc_graycounter1_ce = (rx_cdc_cdc_asyncfifo_readable & rx_cdc_cdc_asyncfifo_re);
assign rx_cdc_cdc_asyncfifo_writable = (((rx_cdc_cdc_graycounter0_q[5] == rx_cdc_cdc_consume_wdomain[5]) | (rx_cdc_cdc_graycounter0_q[4] == rx_cdc_cdc_consume_wdomain[4])) | (rx_cdc_cdc_graycounter0_q[3:0] != rx_cdc_cdc_consume_wdomain[3:0]));
assign rx_cdc_cdc_asyncfifo_readable = (rx_cdc_cdc_graycounter1_q != rx_cdc_cdc_produce_rdomain);
assign rx_cdc_cdc_wrport_adr = rx_cdc_cdc_graycounter0_q_binary[4:0];
assign rx_cdc_cdc_wrport_dat_w = rx_cdc_cdc_asyncfifo_din;
assign rx_cdc_cdc_wrport_we = rx_cdc_cdc_graycounter0_ce;
assign rx_cdc_cdc_rdport_adr = rx_cdc_cdc_graycounter1_q_next_binary[4:0];
assign rx_cdc_cdc_asyncfifo_dout = rx_cdc_cdc_rdport_dat_r;

// synthesis translate_off
reg dummy_d_26;
// synthesis translate_on
always @(*) begin
	rx_cdc_cdc_graycounter0_q_next_binary <= 6'd0;
	if (rx_cdc_cdc_graycounter0_ce) begin
		rx_cdc_cdc_graycounter0_q_next_binary <= (rx_cdc_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		rx_cdc_cdc_graycounter0_q_next_binary <= rx_cdc_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_26 <= dummy_s;
// synthesis translate_on
end
assign rx_cdc_cdc_graycounter0_q_next = (rx_cdc_cdc_graycounter0_q_next_binary ^ rx_cdc_cdc_graycounter0_q_next_binary[5:1]);

// synthesis translate_off
reg dummy_d_27;
// synthesis translate_on
always @(*) begin
	rx_cdc_cdc_graycounter1_q_next_binary <= 6'd0;
	if (rx_cdc_cdc_graycounter1_ce) begin
		rx_cdc_cdc_graycounter1_q_next_binary <= (rx_cdc_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		rx_cdc_cdc_graycounter1_q_next_binary <= rx_cdc_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_27 <= dummy_s;
// synthesis translate_on
end
assign rx_cdc_cdc_graycounter1_q_next = (rx_cdc_cdc_graycounter1_q_next_binary ^ rx_cdc_cdc_graycounter1_q_next_binary[5:1]);
assign rx_preamble_sink_valid = liteethphymiirx_source_valid;
assign liteethphymiirx_source_ready = rx_preamble_sink_ready;
assign rx_preamble_sink_first = liteethphymiirx_source_first;
assign rx_preamble_sink_last = liteethphymiirx_source_last;
assign rx_preamble_sink_payload_data = liteethphymiirx_source_payload_data;
assign rx_preamble_sink_payload_last_be = liteethphymiirx_source_payload_last_be;
assign rx_preamble_sink_payload_error = liteethphymiirx_source_payload_error;
assign bufferizeendpoints_sink_sink_valid = rx_preamble_source_valid;
assign rx_preamble_source_ready = bufferizeendpoints_sink_sink_ready;
assign bufferizeendpoints_sink_sink_first = rx_preamble_source_first;
assign bufferizeendpoints_sink_sink_last = rx_preamble_source_last;
assign bufferizeendpoints_sink_sink_payload_data = rx_preamble_source_payload_data;
assign bufferizeendpoints_sink_sink_payload_last_be = rx_preamble_source_payload_last_be;
assign bufferizeendpoints_sink_sink_payload_error = rx_preamble_source_payload_error;
assign rx_padding_sink_valid = liteethmaccrc32checker_source_source_valid;
assign liteethmaccrc32checker_source_source_ready = rx_padding_sink_ready;
assign rx_padding_sink_first = liteethmaccrc32checker_source_source_first;
assign rx_padding_sink_last = liteethmaccrc32checker_source_source_last;
assign rx_padding_sink_payload_data = liteethmaccrc32checker_source_source_payload_data;
assign rx_padding_sink_payload_last_be = liteethmaccrc32checker_source_source_payload_last_be;
assign rx_padding_sink_payload_error = liteethmaccrc32checker_source_source_payload_error;
assign rx_last_be_sink_valid = rx_padding_source_valid;
assign rx_padding_source_ready = rx_last_be_sink_ready;
assign rx_last_be_sink_first = rx_padding_source_first;
assign rx_last_be_sink_last = rx_padding_source_last;
assign rx_last_be_sink_payload_data = rx_padding_source_payload_data;
assign rx_last_be_sink_payload_last_be = rx_padding_source_payload_last_be;
assign rx_last_be_sink_payload_error = rx_padding_source_payload_error;
assign rx_converter_sink_valid = rx_last_be_source_valid;
assign rx_last_be_source_ready = rx_converter_sink_ready;
assign rx_converter_sink_first = rx_last_be_source_first;
assign rx_converter_sink_last = rx_last_be_source_last;
assign rx_converter_sink_payload_data = rx_last_be_source_payload_data;
assign rx_converter_sink_payload_last_be = rx_last_be_source_payload_last_be;
assign rx_converter_sink_payload_error = rx_last_be_source_payload_error;
assign rx_cdc_sink_sink_valid = rx_converter_source_valid;
assign rx_converter_source_ready = rx_cdc_sink_sink_ready;
assign rx_cdc_sink_sink_first = rx_converter_source_first;
assign rx_cdc_sink_sink_last = rx_converter_source_last;
assign rx_cdc_sink_sink_payload_data = rx_converter_source_payload_data;
assign rx_cdc_sink_sink_payload_last_be = rx_converter_source_payload_last_be;
assign rx_cdc_sink_sink_payload_error = rx_converter_source_payload_error;
assign source_valid = rx_cdc_source_source_valid;
assign rx_cdc_source_source_ready = source_ready;
assign source_first = rx_cdc_source_source_first;
assign source_last = rx_cdc_source_source_last;
assign source_payload_data = rx_cdc_source_source_payload_data;
assign source_payload_last_be = rx_cdc_source_source_payload_last_be;
assign source_payload_error = rx_cdc_source_source_payload_error;
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
reg dummy_d_28;
// synthesis translate_on
always @(*) begin
	packetfifo_source_source_first <= 1'd0;
	packetfifo_source_source_first <= packetfifo_param_fifo_source_first;
	packetfifo_source_source_first <= packetfifo_payload_fifo_source_first;
// synthesis translate_off
	dummy_d_28 <= dummy_s;
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
reg dummy_d_29;
// synthesis translate_on
always @(*) begin
	packetfifo_payload_fifo_wrport_adr <= 9'd0;
	if (packetfifo_payload_fifo_replace) begin
		packetfifo_payload_fifo_wrport_adr <= (packetfifo_payload_fifo_produce - 1'd1);
	end else begin
		packetfifo_payload_fifo_wrport_adr <= packetfifo_payload_fifo_produce;
	end
// synthesis translate_off
	dummy_d_29 <= dummy_s;
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
reg dummy_d_30;
// synthesis translate_on
always @(*) begin
	packetfifo_param_fifo_wrport_adr <= 4'd0;
	if (packetfifo_param_fifo_replace) begin
		packetfifo_param_fifo_wrport_adr <= (packetfifo_param_fifo_produce - 1'd1);
	end else begin
		packetfifo_param_fifo_wrport_adr <= packetfifo_param_fifo_produce;
	end
// synthesis translate_off
	dummy_d_30 <= dummy_s;
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
assign array_write_memory0_adr = tx_dp_cdc_wrport_adr;
assign array_write_memory0_we = tx_dp_cdc_wrport_we;
assign array_write_memory0_dat_w = tx_dp_cdc_wrport_dat_w[71:0];
assign array_read_memory0_adr = tx_dp_cdc_rdport_adr;
assign array_write_memory1_adr = tx_dp_cdc_wrport_adr;
assign array_write_memory1_we = tx_dp_cdc_wrport_we;
assign array_write_memory1_dat_w = tx_dp_cdc_wrport_dat_w[73:72];
assign array_read_memory1_adr = tx_dp_cdc_rdport_adr;
assign tx_dp_cdc_rdport_dat_r = {array_read_memory1_dat_r, array_read_memory0_dat_r};

// synthesis translate_off
reg dummy_d_31;
// synthesis translate_on
always @(*) begin
	tx_dp_cdc_graycounter0_q_next_binary <= 5'd0;
	if (tx_dp_cdc_graycounter0_ce) begin
		tx_dp_cdc_graycounter0_q_next_binary <= (tx_dp_cdc_graycounter0_q_binary + 1'd1);
	end else begin
		tx_dp_cdc_graycounter0_q_next_binary <= tx_dp_cdc_graycounter0_q_binary;
	end
// synthesis translate_off
	dummy_d_31 <= dummy_s;
// synthesis translate_on
end
assign tx_dp_cdc_graycounter0_q_next = (tx_dp_cdc_graycounter0_q_next_binary ^ tx_dp_cdc_graycounter0_q_next_binary[4:1]);

// synthesis translate_off
reg dummy_d_32;
// synthesis translate_on
always @(*) begin
	tx_dp_cdc_graycounter1_q_next_binary <= 5'd0;
	if (tx_dp_cdc_graycounter1_ce) begin
		tx_dp_cdc_graycounter1_q_next_binary <= (tx_dp_cdc_graycounter1_q_binary + 1'd1);
	end else begin
		tx_dp_cdc_graycounter1_q_next_binary <= tx_dp_cdc_graycounter1_q_binary;
	end
// synthesis translate_off
	dummy_d_32 <= dummy_s;
// synthesis translate_on
end
assign tx_dp_cdc_graycounter1_q_next = (tx_dp_cdc_graycounter1_q_next_binary ^ tx_dp_cdc_graycounter1_q_next_binary[4:1]);
assign slice_proxy = {tx_crc_value, tx_crc_sink_payload_data[7:0]};
assign resync_clk = eth_tx_clk_1;
assign resync_clk_1 = eth_rx_clk_1;
assign resync_clk_2 = macsys_clk;
assign resync_clk_3 = macdp_clk;
assign resync_clk_4 = maceth_tx_clk;
assign resync_clk_5 = maceth_rx_clk;
assign tx_cdc_cdc_produce_rdomain = multiregimpl01;
assign tx_cdc_cdc_consume_wdomain = multiregimpl11;
assign pulsesynchronizer0_toggle_o = multiregimpl21;
assign pulsesynchronizer1_toggle_o = multiregimpl31;
assign rx_cdc_cdc_produce_rdomain = multiregimpl41;
assign rx_cdc_cdc_consume_wdomain = multiregimpl51;
assign tx_dp_cdc_produce_rdomain = multiregimpl61;
assign tx_dp_cdc_consume_wdomain = multiregimpl71;

always @(posedge eth_rx_clk_1) begin
	liteethphymiirx_reset <= (~pads_rx_dv);
	liteethphymiirx_converter_sink_valid <= 1'd1;
	liteethphymiirx_converter_sink_payload_data <= pads_rx_data;
	if (liteethphymiirx_converter_source_ready) begin
		liteethphymiirx_converter_strobe_all <= 1'd0;
	end
	if (liteethphymiirx_converter_load_part) begin
		if (((liteethphymiirx_converter_demux == 1'd1) | liteethphymiirx_converter_sink_last)) begin
			liteethphymiirx_converter_demux <= 1'd0;
			liteethphymiirx_converter_strobe_all <= 1'd1;
		end else begin
			liteethphymiirx_converter_demux <= (liteethphymiirx_converter_demux + 1'd1);
		end
	end
	if ((liteethphymiirx_converter_source_valid & liteethphymiirx_converter_source_ready)) begin
		if ((liteethphymiirx_converter_sink_valid & liteethphymiirx_converter_sink_ready)) begin
			liteethphymiirx_converter_source_first <= liteethphymiirx_converter_sink_first;
			liteethphymiirx_converter_source_last <= liteethphymiirx_converter_sink_last;
		end else begin
			liteethphymiirx_converter_source_first <= 1'd0;
			liteethphymiirx_converter_source_last <= 1'd0;
		end
	end else begin
		if ((liteethphymiirx_converter_sink_valid & liteethphymiirx_converter_sink_ready)) begin
			liteethphymiirx_converter_source_first <= (liteethphymiirx_converter_sink_first | liteethphymiirx_converter_source_first);
			liteethphymiirx_converter_source_last <= (liteethphymiirx_converter_sink_last | liteethphymiirx_converter_source_last);
		end
	end
	if (liteethphymiirx_converter_load_part) begin
		case (liteethphymiirx_converter_demux)
			1'd0: begin
				liteethphymiirx_converter_source_payload_data[3:0] <= liteethphymiirx_converter_sink_payload_data;
			end
			1'd1: begin
				liteethphymiirx_converter_source_payload_data[7:4] <= liteethphymiirx_converter_sink_payload_data;
			end
		endcase
	end
	if (liteethphymiirx_converter_load_part) begin
		liteethphymiirx_converter_source_payload_valid_token_count <= (liteethphymiirx_converter_demux + 1'd1);
	end
	if (liteethphymiirx_reset) begin
		liteethphymiirx_converter_source_payload_data <= 8'd0;
		liteethphymiirx_converter_source_payload_valid_token_count <= 2'd0;
		liteethphymiirx_converter_demux <= 1'd0;
		liteethphymiirx_converter_strobe_all <= 1'd0;
	end
	if (eth_rx_rst) begin
		liteethphymiirx_converter_sink_valid <= 1'd0;
		liteethphymiirx_converter_sink_payload_data <= 4'd0;
		liteethphymiirx_converter_source_payload_data <= 8'd0;
		liteethphymiirx_converter_source_payload_valid_token_count <= 2'd0;
		liteethphymiirx_converter_demux <= 1'd0;
		liteethphymiirx_converter_strobe_all <= 1'd0;
		liteethphymiirx_reset <= 1'd0;
	end
end

always @(posedge eth_tx_clk_1) begin
	pads_tx_en <= liteethphymiitx_source_source_valid;
	pads_tx_data <= liteethphymiitx_source_source_payload_data;
	if ((liteethphymiitx_converter_source_valid & liteethphymiitx_converter_source_ready)) begin
		if (liteethphymiitx_converter_last) begin
			liteethphymiitx_converter_mux <= 1'd0;
		end else begin
			liteethphymiitx_converter_mux <= (liteethphymiitx_converter_mux + 1'd1);
		end
	end
	if (eth_tx_rst) begin
		liteethphymiitx_converter_mux <= 1'd0;
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
	if (pulsesynchronizer0_i) begin
		pulsesynchronizer0_toggle_i <= (~pulsesynchronizer0_toggle_i);
	end
	if (liteethmaccrc32checker_crc_ce) begin
		liteethmaccrc32checker_crc_reg <= liteethmaccrc32checker_crc_crc_next;
	end
	if (liteethmaccrc32checker_crc_reset) begin
		liteethmaccrc32checker_crc_reg <= 32'd4294967295;
	end
	if (((liteethmaccrc32checker_syncfifo_syncfifo_we & liteethmaccrc32checker_syncfifo_syncfifo_writable) & (~liteethmaccrc32checker_syncfifo_replace))) begin
		if ((liteethmaccrc32checker_syncfifo_produce == 3'd4)) begin
			liteethmaccrc32checker_syncfifo_produce <= 1'd0;
		end else begin
			liteethmaccrc32checker_syncfifo_produce <= (liteethmaccrc32checker_syncfifo_produce + 1'd1);
		end
	end
	if (liteethmaccrc32checker_syncfifo_do_read) begin
		if ((liteethmaccrc32checker_syncfifo_consume == 3'd4)) begin
			liteethmaccrc32checker_syncfifo_consume <= 1'd0;
		end else begin
			liteethmaccrc32checker_syncfifo_consume <= (liteethmaccrc32checker_syncfifo_consume + 1'd1);
		end
	end
	if (((liteethmaccrc32checker_syncfifo_syncfifo_we & liteethmaccrc32checker_syncfifo_syncfifo_writable) & (~liteethmaccrc32checker_syncfifo_replace))) begin
		if ((~liteethmaccrc32checker_syncfifo_do_read)) begin
			liteethmaccrc32checker_syncfifo_level <= (liteethmaccrc32checker_syncfifo_level + 1'd1);
		end
	end else begin
		if (liteethmaccrc32checker_syncfifo_do_read) begin
			liteethmaccrc32checker_syncfifo_level <= (liteethmaccrc32checker_syncfifo_level - 1'd1);
		end
	end
	if (liteethmaccrc32checker_fifo_reset) begin
		liteethmaccrc32checker_syncfifo_level <= 3'd0;
		liteethmaccrc32checker_syncfifo_produce <= 3'd0;
		liteethmaccrc32checker_syncfifo_consume <= 3'd0;
	end
	rxdatapath_bufferizeendpoints_state <= rxdatapath_bufferizeendpoints_next_state;
	if (liteethmaccrc32checker_last_be_next_value_ce0) begin
		liteethmaccrc32checker_last_be <= liteethmaccrc32checker_last_be_next_value0;
	end
	if (liteethmaccrc32checker_crc_error1_next_value_ce1) begin
		liteethmaccrc32checker_crc_error1 <= liteethmaccrc32checker_crc_error1_next_value1;
	end
	if (((~bufferizeendpoints_pipe_valid_source_valid) | bufferizeendpoints_pipe_valid_source_ready)) begin
		bufferizeendpoints_pipe_valid_source_valid <= bufferizeendpoints_pipe_valid_sink_valid;
		bufferizeendpoints_pipe_valid_source_first <= bufferizeendpoints_pipe_valid_sink_first;
		bufferizeendpoints_pipe_valid_source_last <= bufferizeendpoints_pipe_valid_sink_last;
		bufferizeendpoints_pipe_valid_source_payload_data <= bufferizeendpoints_pipe_valid_sink_payload_data;
		bufferizeendpoints_pipe_valid_source_payload_last_be <= bufferizeendpoints_pipe_valid_sink_payload_last_be;
		bufferizeendpoints_pipe_valid_source_payload_error <= bufferizeendpoints_pipe_valid_sink_payload_error;
	end
	if (pulsesynchronizer1_i) begin
		pulsesynchronizer1_toggle_i <= (~pulsesynchronizer1_toggle_i);
	end
	if ((rx_padding_sink_valid & rx_padding_sink_ready)) begin
		if (rx_padding_sink_last) begin
			rx_padding_length <= 1'd0;
		end else begin
			rx_padding_length <= (rx_padding_length + rx_padding_length_inc);
		end
	end
	if ((rx_converter_converter_sink_valid & rx_converter_converter_sink_ready)) begin
	end
	if (rx_converter_converter_source_ready) begin
		rx_converter_converter_strobe_all <= 1'd0;
	end
	if (rx_converter_converter_load_part) begin
		if (((rx_converter_converter_demux == 3'd7) | rx_converter_converter_sink_last)) begin
			rx_converter_converter_demux <= 1'd0;
			rx_converter_converter_strobe_all <= 1'd1;
		end else begin
			rx_converter_converter_demux <= (rx_converter_converter_demux + 1'd1);
		end
	end
	if ((rx_converter_converter_source_valid & rx_converter_converter_source_ready)) begin
		if ((rx_converter_converter_sink_valid & rx_converter_converter_sink_ready)) begin
			rx_converter_converter_source_first <= rx_converter_converter_sink_first;
			rx_converter_converter_source_last <= rx_converter_converter_sink_last;
		end else begin
			rx_converter_converter_source_first <= 1'd0;
			rx_converter_converter_source_last <= 1'd0;
		end
	end else begin
		if ((rx_converter_converter_sink_valid & rx_converter_converter_sink_ready)) begin
			rx_converter_converter_source_first <= (rx_converter_converter_sink_first | rx_converter_converter_source_first);
			rx_converter_converter_source_last <= (rx_converter_converter_sink_last | rx_converter_converter_source_last);
		end
	end
	if (rx_converter_converter_load_part) begin
		case (rx_converter_converter_demux)
			1'd0: begin
				rx_converter_converter_source_payload_data[9:0] <= rx_converter_converter_sink_payload_data;
			end
			1'd1: begin
				rx_converter_converter_source_payload_data[19:10] <= rx_converter_converter_sink_payload_data;
			end
			2'd2: begin
				rx_converter_converter_source_payload_data[29:20] <= rx_converter_converter_sink_payload_data;
			end
			2'd3: begin
				rx_converter_converter_source_payload_data[39:30] <= rx_converter_converter_sink_payload_data;
			end
			3'd4: begin
				rx_converter_converter_source_payload_data[49:40] <= rx_converter_converter_sink_payload_data;
			end
			3'd5: begin
				rx_converter_converter_source_payload_data[59:50] <= rx_converter_converter_sink_payload_data;
			end
			3'd6: begin
				rx_converter_converter_source_payload_data[69:60] <= rx_converter_converter_sink_payload_data;
			end
			3'd7: begin
				rx_converter_converter_source_payload_data[79:70] <= rx_converter_converter_sink_payload_data;
			end
		endcase
	end
	if (rx_converter_converter_load_part) begin
		rx_converter_converter_source_payload_valid_token_count <= (rx_converter_converter_demux + 1'd1);
	end
	rx_cdc_cdc_graycounter0_q_binary <= rx_cdc_cdc_graycounter0_q_next_binary;
	rx_cdc_cdc_graycounter0_q <= rx_cdc_cdc_graycounter0_q_next;
	if (maceth_rx_rst) begin
		liteethmaccrc32checker_crc_reg <= 32'd4294967295;
		liteethmaccrc32checker_syncfifo_level <= 3'd0;
		liteethmaccrc32checker_syncfifo_produce <= 3'd0;
		liteethmaccrc32checker_syncfifo_consume <= 3'd0;
		liteethmaccrc32checker_last_be <= 1'd0;
		liteethmaccrc32checker_crc_error1 <= 1'd0;
		bufferizeendpoints_pipe_valid_source_valid <= 1'd0;
		bufferizeendpoints_pipe_valid_source_payload_data <= 8'd0;
		bufferizeendpoints_pipe_valid_source_payload_last_be <= 1'd0;
		bufferizeendpoints_pipe_valid_source_payload_error <= 1'd0;
		rx_padding_length <= 11'd0;
		rx_converter_converter_source_payload_data <= 80'd0;
		rx_converter_converter_source_payload_valid_token_count <= 4'd0;
		rx_converter_converter_demux <= 3'd0;
		rx_converter_converter_strobe_all <= 1'd0;
		rx_cdc_cdc_graycounter0_q <= 6'd0;
		rx_cdc_cdc_graycounter0_q_binary <= 6'd0;
		rxdatapath_liteethmacpreamblechecker_state <= 1'd0;
		rxdatapath_bufferizeendpoints_state <= 2'd0;
	end
	multiregimpl50 <= rx_cdc_cdc_graycounter1_q;
	multiregimpl51 <= multiregimpl50;
end

always @(posedge maceth_tx_clk) begin
	tx_cdc_cdc_graycounter1_q_binary <= tx_cdc_cdc_graycounter1_q_next_binary;
	tx_cdc_cdc_graycounter1_q <= tx_cdc_cdc_graycounter1_q_next;
	if ((tx_converter_source_source_valid & tx_converter_source_source_ready)) begin
		if (tx_converter_last_be_drop) begin
			if (tx_converter_source_source_last) begin
				tx_converter_last_be_drop <= 1'd0;
			end
		end else begin
			if ((tx_converter_last_be_packet_end & (~tx_converter_source_source_last))) begin
				tx_converter_last_be_drop <= 1'd1;
			end
		end
	end
	if ((tx_converter_converter_source_valid & tx_converter_converter_source_ready)) begin
		if (tx_converter_converter_last) begin
			tx_converter_converter_mux <= 1'd0;
		end else begin
			tx_converter_converter_mux <= (tx_converter_converter_mux + 1'd1);
		end
	end
	txdatapath_liteethmactxlastbe_state <= txdatapath_liteethmactxlastbe_next_state;
	txdatapath_liteethmacpaddinginserter_state <= txdatapath_liteethmacpaddinginserter_next_state;
	if (tx_padding_counter_clockdomainsrenamer0_next_value_ce) begin
		tx_padding_counter <= tx_padding_counter_clockdomainsrenamer0_next_value;
	end
	if (tx_crc_is_ongoing0) begin
		tx_crc_cnt <= 2'd3;
	end else begin
		if ((tx_crc_is_ongoing1 & (~tx_crc_cnt_done))) begin
			tx_crc_cnt <= (tx_crc_cnt - tx_crc_source_ready);
		end
	end
	if (tx_crc_ce) begin
		tx_crc_reg <= tx_crc_crc_next;
	end
	if (tx_crc_reset) begin
		tx_crc_reg <= 32'd4294967295;
	end
	txdatapath_bufferizeendpoints_state <= txdatapath_bufferizeendpoints_next_state;
	if (tx_crc_crc_packet_clockdomainsrenamer1_next_value_ce0) begin
		tx_crc_crc_packet <= tx_crc_crc_packet_clockdomainsrenamer1_next_value0;
	end
	if (tx_crc_last_be_clockdomainsrenamer1_next_value_ce1) begin
		tx_crc_last_be <= tx_crc_last_be_clockdomainsrenamer1_next_value1;
	end
	if (((~tx_crc_pipe_valid_source_valid) | tx_crc_pipe_valid_source_ready)) begin
		tx_crc_pipe_valid_source_valid <= tx_crc_pipe_valid_sink_valid;
		tx_crc_pipe_valid_source_first <= tx_crc_pipe_valid_sink_first;
		tx_crc_pipe_valid_source_last <= tx_crc_pipe_valid_sink_last;
		tx_crc_pipe_valid_source_payload_data <= tx_crc_pipe_valid_sink_payload_data;
		tx_crc_pipe_valid_source_payload_last_be <= tx_crc_pipe_valid_sink_payload_last_be;
		tx_crc_pipe_valid_source_payload_error <= tx_crc_pipe_valid_sink_payload_error;
	end
	txdatapath_liteethmacpreambleinserter_state <= txdatapath_liteethmacpreambleinserter_next_state;
	if (tx_preamble_count_clockdomainsrenamer2_next_value_ce) begin
		tx_preamble_count <= tx_preamble_count_clockdomainsrenamer2_next_value;
	end
	txdatapath_liteethmacgap_state <= txdatapath_liteethmacgap_next_state;
	if (tx_gap_counter_clockdomainsrenamer3_next_value_ce) begin
		tx_gap_counter <= tx_gap_counter_clockdomainsrenamer3_next_value;
	end
	if (maceth_tx_rst_1) begin
		tx_cdc_cdc_graycounter1_q <= 6'd0;
		tx_cdc_cdc_graycounter1_q_binary <= 6'd0;
		tx_converter_converter_mux <= 3'd0;
		tx_converter_last_be_drop <= 1'd0;
		tx_padding_counter <= 16'd0;
		tx_crc_reg <= 32'd4294967295;
		tx_crc_cnt <= 2'd3;
		tx_crc_pipe_valid_source_valid <= 1'd0;
		tx_crc_pipe_valid_source_payload_data <= 8'd0;
		tx_crc_pipe_valid_source_payload_last_be <= 1'd0;
		tx_crc_pipe_valid_source_payload_error <= 1'd0;
		txdatapath_liteethmactxlastbe_state <= 1'd0;
		txdatapath_liteethmacpaddinginserter_state <= 1'd0;
		txdatapath_bufferizeendpoints_state <= 2'd0;
		txdatapath_liteethmacpreambleinserter_state <= 2'd0;
		txdatapath_liteethmacgap_state <= 1'd0;
	end
	multiregimpl00 <= tx_cdc_cdc_graycounter0_q;
	multiregimpl01 <= multiregimpl00;
end

always @(posedge macsys_clk) begin
	tx_cdc_cdc_graycounter0_q_binary <= tx_cdc_cdc_graycounter0_q_next_binary;
	tx_cdc_cdc_graycounter0_q <= tx_cdc_cdc_graycounter0_q_next;
	if (pulsesynchronizer0_o) begin
		preamble_errors_status <= (preamble_errors_status + 1'd1);
	end
	if (pulsesynchronizer1_o) begin
		crc_errors_status <= (crc_errors_status + 1'd1);
	end
	pulsesynchronizer0_toggle_o_r <= pulsesynchronizer0_toggle_o;
	pulsesynchronizer1_toggle_o_r <= pulsesynchronizer1_toggle_o;
	rx_cdc_cdc_graycounter1_q_binary <= rx_cdc_cdc_graycounter1_q_next_binary;
	rx_cdc_cdc_graycounter1_q <= rx_cdc_cdc_graycounter1_q_next;
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
		tx_cdc_cdc_graycounter0_q <= 6'd0;
		tx_cdc_cdc_graycounter0_q_binary <= 6'd0;
		preamble_errors_status <= 32'd0;
		crc_errors_status <= 32'd0;
		rx_cdc_cdc_graycounter1_q <= 6'd0;
		rx_cdc_cdc_graycounter1_q_binary <= 6'd0;
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
	multiregimpl10 <= tx_cdc_cdc_graycounter1_q;
	multiregimpl11 <= multiregimpl10;
	multiregimpl20 <= pulsesynchronizer0_toggle_i;
	multiregimpl21 <= multiregimpl20;
	multiregimpl30 <= pulsesynchronizer1_toggle_i;
	multiregimpl31 <= multiregimpl30;
	multiregimpl40 <= rx_cdc_cdc_graycounter0_q;
	multiregimpl41 <= multiregimpl40;
	multiregimpl60 <= tx_dp_cdc_graycounter0_q;
	multiregimpl61 <= multiregimpl60;
end

always @(posedge resync_clk) begin
	simasyncresetsynchronizerimpl0_rst1 <= eth_phy_rst;
	eth_tx_rst <= (eth_phy_rst | simasyncresetsynchronizerimpl0_rst1);
	simasyncresetsynchronizerimpl1_rst1 <= eth_phy_rst;
	eth_rx_rst <= (eth_phy_rst | simasyncresetsynchronizerimpl1_rst1);
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
	if (tx_cdc_cdc_wrport_we)
		storage[tx_cdc_cdc_wrport_adr] <= tx_cdc_cdc_wrport_dat_w;
	memadr <= tx_cdc_cdc_wrport_adr;
end

always @(posedge maceth_tx_clk) begin
	memadr_1 <= tx_cdc_cdc_rdport_adr;
end

assign tx_cdc_cdc_wrport_dat_r = storage[memadr];
assign tx_cdc_cdc_rdport_dat_r = storage[memadr_1];

reg [11:0] storage_1[0:4];
reg [11:0] memdat;
always @(posedge maceth_rx_clk) begin
	if (liteethmaccrc32checker_syncfifo_wrport_we)
		storage_1[liteethmaccrc32checker_syncfifo_wrport_adr] <= liteethmaccrc32checker_syncfifo_wrport_dat_w;
	memdat <= storage_1[liteethmaccrc32checker_syncfifo_wrport_adr];
end

always @(posedge maceth_rx_clk) begin
end

assign liteethmaccrc32checker_syncfifo_wrport_dat_r = memdat;
assign liteethmaccrc32checker_syncfifo_rdport_dat_r = storage_1[liteethmaccrc32checker_syncfifo_rdport_adr];

reg [81:0] storage_2[0:31];
reg [4:0] memadr_2;
reg [4:0] memadr_3;
always @(posedge maceth_rx_clk) begin
	if (rx_cdc_cdc_wrport_we)
		storage_2[rx_cdc_cdc_wrport_adr] <= rx_cdc_cdc_wrport_dat_w;
	memadr_2 <= rx_cdc_cdc_wrport_adr;
end

always @(posedge macsys_clk) begin
	memadr_3 <= rx_cdc_cdc_rdport_adr;
end

assign rx_cdc_cdc_wrport_dat_r = storage_2[memadr_2];
assign rx_cdc_cdc_rdport_dat_r = storage_2[memadr_3];

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

(* ram_style = "block" *) reg [71:0] storage_5[0:15];
reg [3:0] memadr_4;
reg [71:0] memdat_5;
always @(posedge macdp_clk) begin
	if (array_write_memory0_we)
		storage_5[array_write_memory0_adr] <= array_write_memory0_dat_w;
	memadr_4 <= array_write_memory0_adr;
end

always @(posedge macsys_clk) begin
	memdat_5 <= storage_5[array_read_memory0_adr];
end

assign array_write_memory0_dat_r = storage_5[memadr_4];
assign array_read_memory0_dat_r = memdat_5;

(* ram_style = "distributed" *) reg [1:0] storage_6[0:15];
reg [3:0] memadr_5;
reg [1:0] memdat_6;
always @(posedge macdp_clk) begin
	if (array_write_memory1_we)
		storage_6[array_write_memory1_adr] <= array_write_memory1_dat_w;
	memadr_5 <= array_write_memory1_adr;
end

always @(posedge macsys_clk) begin
	memdat_6 <= storage_6[array_read_memory1_adr];
end

assign array_write_memory1_dat_r = storage_6[memadr_5];
assign array_read_memory1_dat_r = memdat_6;

endmodule


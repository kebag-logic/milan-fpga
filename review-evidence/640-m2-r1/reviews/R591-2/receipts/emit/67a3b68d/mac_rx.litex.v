

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
    input  wire          macdp_clk,
    input  wire          macdp_rst,
    input  wire          macsys_clk,
    input  wire          macsys_rst,
    input  wire          milan_clk,
    input  wire          milan_rst,
    input  wire          sink_first,
    input  wire          sink_last,
    input  wire   [63:0] sink_payload_data,
    input  wire    [7:0] sink_payload_keep,
    output wire          sink_ready,
    input  wire          sink_valid,
    output wire          source_first,
    output wire          source_last,
    output wire   [63:0] source_payload_data,
    output wire    [7:0] source_payload_keep,
    input  wire          source_ready,
    output wire          source_valid,
    input  wire          sys_clk,
    input  wire          sys_rst
);



// Hierarchy




// Signals


wire    [3:0] array_read_memory0_adr;
wire   [71:0] array_read_memory0_dat_r;
wire    [3:0] array_read_memory1_adr;
wire    [1:0] array_read_memory1_dat_r;
wire    [3:0] array_write_memory0_adr;
wire   [71:0] array_write_memory0_dat_r;
wire   [71:0] array_write_memory0_dat_w;
wire          array_write_memory0_we;
wire    [3:0] array_write_memory1_adr;
wire    [1:0] array_write_memory1_dat_r;
wire    [1:0] array_write_memory1_dat_w;
wire          array_write_memory1_we;
wire   [73:0] cdc_asyncfifo_din;
wire   [73:0] cdc_asyncfifo_dout;
wire          cdc_asyncfifo_re;
wire          cdc_asyncfifo_readable;
wire          cdc_asyncfifo_we;
wire          cdc_asyncfifo_writable;
wire    [4:0] cdc_consume_wdomain;
reg    [73:0] cdc_dout = 74'd0;
wire          cdc_fifo_in_first;
wire          cdc_fifo_in_last;
wire   [63:0] cdc_fifo_in_payload_data;
wire    [7:0] cdc_fifo_in_payload_keep;
wire          cdc_fifo_out_first;
wire          cdc_fifo_out_last;
wire   [63:0] cdc_fifo_out_payload_data;
wire    [7:0] cdc_fifo_out_payload_keep;
wire          cdc_graycounter0_ce;
reg     [4:0] cdc_graycounter0_q = 5'd0;
reg     [4:0] cdc_graycounter0_q_binary = 5'd0;
wire    [4:0] cdc_graycounter0_q_next;
reg     [4:0] cdc_graycounter0_q_next_binary = 5'd0;
wire          cdc_graycounter1_ce;
reg     [4:0] cdc_graycounter1_q = 5'd0;
reg     [4:0] cdc_graycounter1_q_binary = 5'd0;
wire    [4:0] cdc_graycounter1_q_next;
reg     [4:0] cdc_graycounter1_q_next_binary = 5'd0;
wire    [4:0] cdc_produce_rdomain;
wire    [3:0] cdc_rdport_adr;
wire   [73:0] cdc_rdport_dat_r;
wire          cdc_re;
reg           cdc_readable = 1'd0;
wire          cdc_sink_first;
wire          cdc_sink_last;
wire   [63:0] cdc_sink_payload_data;
wire    [7:0] cdc_sink_payload_keep;
wire          cdc_sink_ready;
wire          cdc_sink_valid;
wire          cdc_source_first;
wire          cdc_source_last;
wire   [63:0] cdc_source_payload_data;
wire    [7:0] cdc_source_payload_keep;
wire          cdc_source_ready;
wire          cdc_source_valid;
wire    [3:0] cdc_wrport_adr;
wire   [73:0] cdc_wrport_dat_w;
wire          cdc_wrport_we;
reg     [4:0] multiregimpl00 = 5'd0;
reg     [4:0] multiregimpl01 = 5'd0;
reg     [4:0] multiregimpl10 = 5'd0;
reg     [4:0] multiregimpl11 = 5'd0;


// Combinatorial Logic


assign cdc_sink_valid = sink_valid;
assign sink_ready = cdc_sink_ready;
assign cdc_sink_first = sink_first;
assign cdc_sink_last = sink_last;
assign cdc_sink_payload_data = sink_payload_data;
assign cdc_sink_payload_keep = sink_payload_keep;
assign source_valid = cdc_source_valid;
assign cdc_source_ready = source_ready;
assign source_first = cdc_source_first;
assign source_last = cdc_source_last;
assign source_payload_data = cdc_source_payload_data;
assign source_payload_keep = cdc_source_payload_keep;
assign cdc_asyncfifo_din = {cdc_fifo_in_last, cdc_fifo_in_first, cdc_fifo_in_payload_keep, cdc_fifo_in_payload_data};
assign {cdc_fifo_out_last, cdc_fifo_out_first, cdc_fifo_out_payload_keep, cdc_fifo_out_payload_data} = cdc_dout;
assign cdc_sink_ready = cdc_asyncfifo_writable;
assign cdc_asyncfifo_we = cdc_sink_valid;
assign cdc_fifo_in_first = cdc_sink_first;
assign cdc_fifo_in_last = cdc_sink_last;
assign cdc_fifo_in_payload_data = cdc_sink_payload_data;
assign cdc_fifo_in_payload_keep = cdc_sink_payload_keep;
assign cdc_source_valid = cdc_readable;
assign cdc_source_first = cdc_fifo_out_first;
assign cdc_source_last = cdc_fifo_out_last;
assign cdc_source_payload_data = cdc_fifo_out_payload_data;
assign cdc_source_payload_keep = cdc_fifo_out_payload_keep;
assign cdc_re = cdc_source_ready;
assign cdc_asyncfifo_re = (cdc_re | (~cdc_readable));
assign cdc_graycounter0_ce = (cdc_asyncfifo_writable & cdc_asyncfifo_we);
assign cdc_graycounter1_ce = (cdc_asyncfifo_readable & cdc_asyncfifo_re);
assign cdc_asyncfifo_writable = (((cdc_graycounter0_q[4] == cdc_consume_wdomain[4]) | (cdc_graycounter0_q[3] == cdc_consume_wdomain[3])) | (cdc_graycounter0_q[2:0] != cdc_consume_wdomain[2:0]));
assign cdc_asyncfifo_readable = (cdc_graycounter1_q != cdc_produce_rdomain);
assign cdc_wrport_adr = cdc_graycounter0_q_binary[3:0];
assign cdc_wrport_dat_w = cdc_asyncfifo_din;
assign cdc_wrport_we = cdc_graycounter0_ce;
assign cdc_rdport_adr = cdc_graycounter1_q_next_binary[3:0];
assign cdc_asyncfifo_dout = cdc_rdport_dat_r;
assign array_write_memory0_adr = cdc_wrport_adr;
assign array_write_memory0_we = cdc_wrport_we;
assign array_write_memory0_dat_w = cdc_wrport_dat_w[71:0];
assign array_read_memory0_adr = cdc_rdport_adr;
assign array_write_memory1_adr = cdc_wrport_adr;
assign array_write_memory1_we = cdc_wrport_we;
assign array_write_memory1_dat_w = cdc_wrport_dat_w[73:72];
assign array_read_memory1_adr = cdc_rdport_adr;
assign cdc_rdport_dat_r = {array_read_memory1_dat_r, array_read_memory0_dat_r};
always @(*) begin
    cdc_graycounter0_q_next_binary = 5'd0;
    if (cdc_graycounter0_ce) begin
        cdc_graycounter0_q_next_binary = (cdc_graycounter0_q_binary + 1'd1);
    end else begin
        cdc_graycounter0_q_next_binary = cdc_graycounter0_q_binary;
    end
end
assign cdc_graycounter0_q_next = (cdc_graycounter0_q_next_binary ^ cdc_graycounter0_q_next_binary[4:1]);
always @(*) begin
    cdc_graycounter1_q_next_binary = 5'd0;
    if (cdc_graycounter1_ce) begin
        cdc_graycounter1_q_next_binary = (cdc_graycounter1_q_binary + 1'd1);
    end else begin
        cdc_graycounter1_q_next_binary = cdc_graycounter1_q_binary;
    end
end
assign cdc_graycounter1_q_next = (cdc_graycounter1_q_next_binary ^ cdc_graycounter1_q_next_binary[4:1]);
assign cdc_produce_rdomain = multiregimpl01;
assign cdc_consume_wdomain = multiregimpl11;



// Synchronous Logic


always @(posedge macdp_clk) begin
    if ((cdc_re | (~cdc_readable))) begin
        cdc_dout <= cdc_asyncfifo_dout;
        cdc_readable <= cdc_asyncfifo_readable;
    end
    cdc_graycounter1_q_binary <= cdc_graycounter1_q_next_binary;
    cdc_graycounter1_q <= cdc_graycounter1_q_next;
    if (macdp_rst) begin
        cdc_readable <= 1'd0;
        cdc_graycounter1_q <= 5'd0;
        cdc_graycounter1_q_binary <= 5'd0;
    end
    multiregimpl00 <= cdc_graycounter0_q;
    multiregimpl01 <= multiregimpl00;
end

always @(posedge macsys_clk) begin
    cdc_graycounter0_q_binary <= cdc_graycounter0_q_next_binary;
    cdc_graycounter0_q <= cdc_graycounter0_q_next;
    if (macsys_rst) begin
        cdc_graycounter0_q <= 5'd0;
        cdc_graycounter0_q_binary <= 5'd0;
    end
    multiregimpl10 <= cdc_graycounter1_q;
    multiregimpl11 <= multiregimpl10;
end



// Specialized Logic


(* ram_style = "block" *)

// Memory storage: 16-words x 72-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [71:0] storage[0:15];
reg [71:0] storage_dat0;
reg [71:0] storage_dat1;
always @(posedge macsys_clk) begin
	if (array_write_memory0_we)
		storage[array_write_memory0_adr] <= array_write_memory0_dat_w;
	storage_dat0 <= storage[array_write_memory0_adr];
end
always @(posedge macdp_clk) begin
	storage_dat1 <= storage[array_read_memory0_adr];
end
assign array_write_memory0_dat_r = storage_dat0;
assign array_read_memory0_dat_r = storage_dat1;


(* ram_style = "distributed" *)

// Memory storage_1: 16-words x 2-bit

// Port 0 | Read: Sync  | Write: Sync | Mode: Read-First 

reg [1:0] storage_1[0:15];
reg [1:0] storage_1_dat0;
reg [1:0] storage_1_dat1;
always @(posedge macsys_clk) begin
	if (array_write_memory1_we)
		storage_1[array_write_memory1_adr] <= array_write_memory1_dat_w;
	storage_1_dat0 <= storage_1[array_write_memory1_adr];
end
always @(posedge macdp_clk) begin
	storage_1_dat1 <= storage_1[array_read_memory1_adr];
end
assign array_write_memory1_dat_r = storage_1_dat0;
assign array_read_memory1_dat_r = storage_1_dat1;


endmodule






/* Machine-generated using Migen */
module probe_ctrl_mailbox(
	input [29:0] bus_adr,
	input [31:0] bus_dat_w,
	output [31:0] bus_dat_r,
	input [3:0] bus_sel,
	input bus_cyc,
	input bus_stb,
	output bus_ack,
	input bus_we,
	output bus_err,
	output trigger,
	input sys_clk,
	input sys_rst
);

wire ctrlmailbox_irq;
wire ctrlmailbox_mbx_status;
wire ctrlmailbox_mbx_pending;
reg ctrlmailbox_mbx_clear;
wire ctrlmailbox_eventmanager_mbx0;
wire ctrlmailbox_eventmanager_mbx1;
reg ctrlmailbox_eventmanager_status = 1'd0;
reg ctrlmailbox_eventmanager_wr_stb = 1'd0;
reg ctrlmailbox_eventmanager_wr_data = 1'd0;
reg ctrlmailbox_eventmanager_storage = 1'd0;
reg [16:0] ctrlmailbox_ms_cnt = 17'd0;
reg ctrlmailbox_ms_tick = 1'd0;
wire ctrlmailbox0;
wire ctrlmailbox1;
wire ctrlmailbox2;
wire ctrlmailbox3;
wire [12:0] ctrlmailbox4;
wire [31:0] ctrlmailbox5;
wire [31:0] ctrlmailbox6;
wire [3:0] ctrlmailbox7;
wire ctrlmailbox8;
wire ctrlmailbox9;
wire [7:0] ctrlmailbox10;
wire ctrlmailbox11;
wire ctrlmailbox12;
wire [2:0] ctrlmailbox13;
wire [15:0] ctrlmailbox14;
wire [15:0] ctrlmailbox15;
wire [31:0] ctrlmailbox16;
wire [11:0] ctrlmailbox17;
wire [2:0] ctrlmailbox18;
wire ctrlmailbox19;
wire [15:0] ctrlmailbox20;
wire [15:0] ctrlmailbox21;
wire [15:0] ctrlmailbox22;
wire [15:0] ctrlmailbox23;
wire [1023:0] ctrlmailbox24;

// synthesis translate_off
reg dummy_s;
initial dummy_s <= 1'd0;
// synthesis translate_on

assign trigger = ctrlmailbox3;
assign ctrlmailbox_eventmanager_mbx0 = ctrlmailbox_mbx_status;
assign ctrlmailbox_eventmanager_mbx1 = ctrlmailbox_mbx_pending;

// synthesis translate_off
reg dummy_d;
// synthesis translate_on
always @(*) begin
	ctrlmailbox_mbx_clear <= 1'd0;
	if ((ctrlmailbox_eventmanager_wr_stb & ctrlmailbox_eventmanager_wr_data)) begin
		ctrlmailbox_mbx_clear <= 1'd1;
	end
// synthesis translate_off
	dummy_d <= dummy_s;
// synthesis translate_on
end
assign ctrlmailbox_irq = (ctrlmailbox_eventmanager_status & ctrlmailbox_eventmanager_storage);
assign ctrlmailbox_mbx_status = trigger;
assign ctrlmailbox_mbx_pending = trigger;

always @(posedge sys_clk) begin
	if ((ctrlmailbox_ms_cnt == 17'd99999)) begin
		ctrlmailbox_ms_cnt <= 1'd0;
		ctrlmailbox_ms_tick <= 1'd1;
	end else begin
		ctrlmailbox_ms_cnt <= (ctrlmailbox_ms_cnt + 1'd1);
		ctrlmailbox_ms_tick <= 1'd0;
	end
	if (sys_rst) begin
		ctrlmailbox_ms_cnt <= 17'd0;
		ctrlmailbox_ms_tick <= 1'd0;
	end
end

KL_mbx_wb KL_mbx_wb(
	.clk_i(sys_clk),
	.host_ack_i(ctrlmailbox2),
	.host_rdata_i(ctrlmailbox6),
	.rst_n((~sys_rst)),
	.wb_adr_i(bus_adr),
	.wb_cyc_i(bus_cyc),
	.wb_dat_i(bus_dat_w),
	.wb_sel_i(bus_sel),
	.wb_stb_i(bus_stb),
	.wb_we_i(bus_we),
	.host_addr_o(ctrlmailbox4),
	.host_be_o(ctrlmailbox7),
	.host_req_o(ctrlmailbox0),
	.host_wdata_o(ctrlmailbox5),
	.host_we_o(ctrlmailbox1),
	.wb_ack_o(bus_ack),
	.wb_dat_o(bus_dat_r),
	.wb_err_o(bus_err)
);

KL_mbx KL_mbx(
	.clk_i(sys_clk),
	.gm_change_p_i(1'd0),
	.gm_id_i(1'd0),
	.gptp_domain_i(1'd0),
	.host_addr_i(ctrlmailbox4),
	.host_be_i(ctrlmailbox7),
	.host_req_i(ctrlmailbox0),
	.host_wdata_i(ctrlmailbox5),
	.host_we_i(ctrlmailbox1),
	.link_up_i(1'd0),
	.ms_tick_p_i(ctrlmailbox_ms_tick),
	.rst_n((~sys_rst)),
	.rx_data_i(1'd0),
	.rx_if_i(1'd0),
	.rx_last_i(1'd0),
	.rx_valid_i(1'd0),
	.tx_ready_i(1'd1),
	.host_ack_o(ctrlmailbox2),
	.host_rdata_o(ctrlmailbox6),
	.irq_o(ctrlmailbox3),
	.pub_bound_o(ctrlmailbox21),
	.pub_da_gate_o(ctrlmailbox14),
	.pub_dom_adopted_o(ctrlmailbox19),
	.pub_dom_prio_o(ctrlmailbox18),
	.pub_dom_vid_o(ctrlmailbox17),
	.pub_idle_slope_bps_o(ctrlmailbox16),
	.pub_licence_o(ctrlmailbox15),
	.pub_sid_o(ctrlmailbox24),
	.pub_sid_valid_o(ctrlmailbox22),
	.pub_started_o(ctrlmailbox23),
	.pub_talker_decl_o(ctrlmailbox20),
	.rx_ready_o(ctrlmailbox8),
	.tx_ch_o(ctrlmailbox13),
	.tx_data_o(ctrlmailbox10),
	.tx_if_o(ctrlmailbox12),
	.tx_last_o(ctrlmailbox11),
	.tx_valid_o(ctrlmailbox9)
);

endmodule

